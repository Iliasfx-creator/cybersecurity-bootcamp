"""Loopback-only HTTP server for session-management engineering tests."""

from __future__ import annotations

import argparse
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from typing import Any, Optional
from urllib.parse import urlsplit

from session_manager import SessionManager


USERS: dict[str, dict[str, str]] = {
    "alice": {"tenant_id": "alpha", "role": "user"},
    "bob": {"tenant_id": "beta", "role": "user"},
    "admin": {"tenant_id": "alpha", "role": "admin"},
}


def extract_session_cookie(raw_cookie: Optional[str]) -> Optional[str]:
    """Read the session identifier only from the Cookie header."""

    if not raw_cookie:
        return None
    jar = SimpleCookie()
    try:
        jar.load(raw_cookie)
    except Exception:
        return None
    morsel = jar.get("session")
    return morsel.value if morsel is not None and morsel.value else None


def build_session_cookie(token: str, *, secure: bool) -> str:
    parts = [f"session={token}", "Path=/", "HttpOnly", "SameSite=Lax"]
    if secure:
        parts.append("Secure")
    return "; ".join(parts)


def build_clear_cookie(*, secure: bool) -> str:
    parts = ["session=", "Max-Age=0", "Path=/", "HttpOnly", "SameSite=Lax"]
    if secure:
        parts.append("Secure")
    return "; ".join(parts)


class SessionLabServer(ThreadingHTTPServer):
    daemon_threads = True

    def __init__(
        self,
        server_address: tuple[str, int],
        handler: type[BaseHTTPRequestHandler],
        *,
        manager: SessionManager,
        secure_cookie: bool,
    ) -> None:
        super().__init__(server_address, handler)
        self.manager = manager
        self.secure_cookie = secure_cookie


class SessionLabHandler(BaseHTTPRequestHandler):
    server: SessionLabServer
    protocol_version = "HTTP/1.1"

    def log_message(self, _format: str, *_args: object) -> None:
        # BaseHTTPRequestHandler normally logs the full request target, which
        # could leak a query token.  Session events are logged safely by the
        # manager using keyed fingerprints instead.
        return

    @property
    def route(self) -> str:
        return urlsplit(self.path).path

    def _token_from_cookie(self) -> Optional[str]:
        return extract_session_cookie(self.headers.get("Cookie"))

    def _read_json(self) -> Optional[dict[str, Any]]:
        raw_length = self.headers.get("Content-Length", "0")
        try:
            length = int(raw_length)
        except ValueError:
            return None
        if length < 0 or length > 8_192:
            return None
        raw = self.rfile.read(length) if length else b"{}"
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None
        return value if isinstance(value, dict) else None

    def _send_json(
        self,
        status: int,
        payload: Optional[dict[str, Any]] = None,
        *,
        set_cookie: Optional[str] = None,
    ) -> None:
        body = b"" if payload is None else json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Cache-Control", "no-store")
        self.send_header("Pragma", "no-cache")
        if payload is not None:
            self.send_header("Content-Type", "application/json; charset=utf-8")
        if set_cookie is not None:
            self.send_header("Set-Cookie", set_cookie)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _require_session(self):
        token = self._token_from_cookie()
        record = self.server.manager.resolve(token)
        if record is None or record.state != "authenticated":
            self._send_json(401, {"error": "Authentication required"})
            return None, None
        return token, record

    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if self.route == "/health":
            self._send_json(200, {"status": "ok"})
            return

        if self.route == "/me":
            _token, record = self._require_session()
            if record is None:
                return
            self._send_json(
                200,
                {
                    "user_id": record.user_id,
                    "tenant_id": record.tenant_id,
                    "role": record.role,
                    "auth_level": record.auth_level,
                },
            )
            return

        if self.route == "/admin":
            _token, record = self._require_session()
            if record is None:
                return
            if record.role != "admin" or record.auth_level != "elevated":
                self._send_json(403, {"error": "Elevated administrator required"})
                return
            self._send_json(200, {"result": "privileged operation allowed"})
            return

        self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        if self.route == "/session/prelogin":
            token = self.server.manager.start_anonymous(self._token_from_cookie())
            self._send_json(
                201,
                {"state": "anonymous"},
                set_cookie=build_session_cookie(
                    token, secure=self.server.secure_cookie
                ),
            )
            return

        if self.route == "/login":
            payload = self._read_json()
            if payload is None:
                self._send_json(400, {"error": "Valid JSON object required"})
                return
            username = payload.get("username")
            trusted_user = USERS.get(username) if isinstance(username, str) else None
            if trusted_user is None:
                self._send_json(401, {"error": "Login failed"})
                return

            # This local lab deliberately simplifies authentication.  Identity
            # selection is followed by a trusted server-side lookup; role and
            # tenant values sent by the client are ignored.
            token = self.server.manager.authenticate(
                presented_token=self._token_from_cookie(),
                user_id=username,
                tenant_id=trusted_user["tenant_id"],
                role=trusted_user["role"],
            )
            self._send_json(
                200,
                {"status": "authenticated"},
                set_cookie=build_session_cookie(
                    token, secure=self.server.secure_cookie
                ),
            )
            return

        if self.route == "/session/step-up":
            old_token, record = self._require_session()
            if record is None:
                return
            if record.role != "admin":
                self._send_json(403, {"error": "Administrator required"})
                return
            new_token = self.server.manager.rotate_for_privilege_change(
                old_token,
                trusted_role=record.role,
                new_auth_level="elevated",
            )
            if new_token is None:
                self._send_json(401, {"error": "Session is no longer valid"})
                return
            self._send_json(
                200,
                {"status": "rotated", "auth_level": "elevated"},
                set_cookie=build_session_cookie(
                    new_token, secure=self.server.secure_cookie
                ),
            )
            return

        if self.route == "/logout":
            self.server.manager.revoke(
                self._token_from_cookie(), reason="logout"
            )
            self._send_json(
                200,
                {"status": "logged_out"},
                set_cookie=build_clear_cookie(
                    secure=self.server.secure_cookie
                ),
            )
            return

        self._send_json(404, {"error": "Not found"})

    def do_PUT(self) -> None:  # noqa: N802 - stdlib handler API
        self._send_json(405, {"error": "Method not allowed"})

    def do_PATCH(self) -> None:  # noqa: N802 - stdlib handler API
        self._send_json(405, {"error": "Method not allowed"})

    def do_DELETE(self) -> None:  # noqa: N802 - stdlib handler API
        self._send_json(405, {"error": "Method not allowed"})


def create_server(
    *,
    port: int = 8013,
    manager: Optional[SessionManager] = None,
    secure_cookie: bool = False,
) -> SessionLabServer:
    """Create a server bound only to the IPv4 loopback interface."""

    manager = manager or SessionManager()
    return SessionLabServer(
        ("127.0.0.1", port),
        SessionLabHandler,
        manager=manager,
        secure_cookie=secure_cookie,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8013)
    parser.add_argument(
        "--secure-cookie",
        action="store_true",
        help="Add Secure to cookies (requires HTTPS; leave off for local HTTP)",
    )
    parser.add_argument("--idle-timeout", type=float, default=300.0)
    parser.add_argument("--absolute-timeout", type=float, default=1_800.0)
    args = parser.parse_args()

    manager = SessionManager(
        idle_timeout=args.idle_timeout,
        absolute_timeout=args.absolute_timeout,
    )
    server = create_server(
        port=args.port,
        manager=manager,
        secure_cookie=args.secure_cookie,
    )
    mode = "HTTPS-only cookie mode" if args.secure_cookie else "local HTTP mode"
    print(f"Session lab listening on http://127.0.0.1:{args.port} ({mode})")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
