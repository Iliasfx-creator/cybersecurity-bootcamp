from __future__ import annotations

from copy import deepcopy
from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse
import json
import secrets

from authorization import Action, authorize
from data import (
    AUDIT_LOG,
    DOCUMENTS,
    SESSIONS,
    USERS,
    V2_DOCUMENT_WRITE_FIELDS,
    public_document,
    record_audit,
)


HOST = "127.0.0.1"
PORT = 8012
MAX_BODY_BYTES = 65_536


class RequestError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def session_token(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None

    cookies = SimpleCookie()

    try:
        cookies.load(cookie_header)
    except CookieError:
        return None

    cookie = cookies.get("session")

    if cookie is None or not cookie.value:
        return None

    return cookie.value


class Handler(BaseHTTPRequestHandler):
    server_version = "AcmeDocsLocal/1.0"

    def log_message(self, message: str, *args: object) -> None:
        if getattr(self.server, "quiet", False):
            return

        print(
            f"{self.client_address[0]} "
            f"{self.command} {self.path} - "
            f"{message % args}"
        )

    def reply(
        self,
        status: int,
        payload: object | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        body = (
            b""
            if payload is None
            else json.dumps(
                payload,
                separators=(",", ":"),
            ).encode("utf-8")
        )

        self.send_response(status)

        if payload is not None:
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8",
            )

        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")

        for name, value in (headers or {}).items():
            self.send_header(name, value)

        self.end_headers()
        self.close_connection = True

        if body and self.command != "HEAD":
            self.wfile.write(body)

    def json_body(self) -> dict[str, object]:
        content_type = self.headers.get("Content-Type", "")

        if not content_type.lower().startswith("application/json"):
            raise RequestError(415, "Content-Type must be application/json")

        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise RequestError(400, "Invalid Content-Length") from error

        if length <= 0:
            raise RequestError(400, "A JSON request body is required")

        if length > MAX_BODY_BYTES:
            raise RequestError(413, "Request body is too large")

        raw_body = self.rfile.read(length)

        try:
            payload = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise RequestError(400, "Invalid JSON request body") from error

        if not isinstance(payload, dict):
            raise RequestError(400, "JSON body must be an object")

        return payload

    def actor(self) -> dict[str, object] | None:
        token = session_token(self.headers.get("Cookie"))

        if token is None:
            return None

        username = SESSIONS.get(token)

        if username is None:
            return None

        user = USERS.get(username)

        if user is None:
            return None

        return deepcopy(user)

    def require_actor(self) -> dict[str, object] | None:
        actor = self.actor()

        if actor is None:
            self.reply(401, {"error": "Authentication required"})

        return actor

    def match_route(
        self,
        path: str,
    ) -> tuple[str, dict[str, str], set[str]] | None:
        exact_routes = {
            "/demo-login": ("login", {}, {"POST"}),
            "/logout": ("logout", {}, {"POST"}),
            "/api/v1/documents": ("v1-list", {}, {"GET"}),
            "/api/v2/documents": ("v2-list", {}, {"GET"}),
            "/api/v2/audit": ("v2-audit", {}, {"GET"}),
        }

        if path in exact_routes:
            return exact_routes[path]

        parts = [
            unquote(part)
            for part in path.split("/")
            if part
        ]

        if (
            len(parts) == 4
            and parts[:3] == ["api", "v1", "documents"]
        ):
            return (
                "v1-document",
                {"document_id": parts[3]},
                {"GET", "PATCH"},
            )

        if (
            len(parts) == 4
            and parts[:3] == ["api", "v2", "documents"]
        ):
            return (
                "v2-document",
                {"document_id": parts[3]},
                {"GET", "PATCH"},
            )

        if (
            len(parts) == 5
            and parts[:3] == ["api", "v1", "organizations"]
            and parts[4] == "export"
        ):
            return (
                "v1-export",
                {"tenant_id": parts[3]},
                {"GET"},
            )

        if (
            len(parts) == 5
            and parts[:3] == ["api", "v2", "organizations"]
            and parts[4] == "export"
        ):
            return (
                "v2-export",
                {"tenant_id": parts[3]},
                {"GET"},
            )

        if (
            len(parts) == 6
            and parts[:4] == ["api", "v1", "support", "tenants"]
            and parts[5] == "unlock"
        ):
            return (
                "v1-support",
                {"tenant_id": parts[4]},
                {"POST"},
            )

        if (
            len(parts) == 6
            and parts[:4] == ["api", "v2", "support", "tenants"]
            and parts[5] == "unlock"
        ):
            return (
                "v2-support",
                {"tenant_id": parts[4]},
                {"POST"},
            )

        return None

    def dispatch(self, method: str) -> None:
        path = urlparse(self.path).path
        route = self.match_route(path)

        if route is None:
            self.reply(404, {"error": "Route not found"})
            return

        route_name, parameters, allowed_methods = route

        if method not in allowed_methods:
            self.reply(
                405,
                {"error": "Method not allowed"},
                {"Allow": ", ".join(sorted(allowed_methods))},
            )
            return

        handlers = {
            "login": self.handle_login,
            "logout": self.handle_logout,
            "v1-list": self.handle_v1_list,
            "v1-document": self.handle_v1_document,
            "v1-export": self.handle_v1_export,
            "v1-support": self.handle_v1_support,
            "v2-list": self.handle_v2_list,
            "v2-document": self.handle_v2_document,
            "v2-export": self.handle_v2_export,
            "v2-support": self.handle_v2_support,
            "v2-audit": self.handle_v2_audit,
        }

        try:
            handlers[route_name](method=method, **parameters)
        except RequestError as error:
            self.reply(error.status, {"error": error.message})

    def handle_login(self, method: str) -> None:
        del method
        payload = self.json_body()
        username = payload.get("username")

        if not isinstance(username, str) or username not in USERS:
            self.reply(401, {"error": "Invalid demo user"})
            return

        token = secrets.token_urlsafe(24)
        SESSIONS[token] = username

        actor = USERS[username]

        self.reply(
            200,
            {
                "actor": {
                    "username": actor["username"],
                    "tenant_id": actor["tenant_id"],
                    "role": actor["role"],
                }
            },
            {
                "Set-Cookie": (
                    f"session={token}; Path=/; "
                    "HttpOnly; SameSite=Strict"
                )
            },
        )

    def handle_logout(self, method: str) -> None:
        del method
        token = session_token(self.headers.get("Cookie"))

        if token is not None:
            SESSIONS.pop(token, None)

        self.reply(
            200,
            {"status": "logged out"},
            {
                "Set-Cookie": (
                    "session=; Path=/; Max-Age=0; "
                    "HttpOnly; SameSite=Strict"
                )
            },
        )

    def handle_v1_list(self, method: str) -> None:
        del method

        if self.require_actor() is None:
            return

        self.reply(
            200,
            {"documents": deepcopy(list(DOCUMENTS.values()))},
        )

    def handle_v1_document(
        self,
        method: str,
        document_id: str,
    ) -> None:
        if self.require_actor() is None:
            return

        document = DOCUMENTS.get(document_id)

        if document is None:
            self.reply(404, {"error": "Document not found"})
            return

        if method == "GET":
            self.reply(200, {"document": deepcopy(document)})
            return

        payload = self.json_body()

        if not payload:
            raise RequestError(400, "At least one property is required")

        for name, value in payload.items():
            if name != "id":
                document[name] = value

        self.reply(200, {"document": deepcopy(document)})

    def handle_v1_export(
        self,
        method: str,
        tenant_id: str,
    ) -> None:
        del method

        if self.require_actor() is None:
            return

        documents = [
            deepcopy(document)
            for document in DOCUMENTS.values()
            if document.get("tenant_id") == tenant_id
        ]

        self.reply(
            200,
            {
                "tenant_id": tenant_id,
                "documents": documents,
            },
        )

    def handle_v1_support(
        self,
        method: str,
        tenant_id: str,
    ) -> None:
        del method

        if self.require_actor() is None:
            return

        self.reply(
            200,
            {
                "tenant_id": tenant_id,
                "status": "tenant unlocked",
            },
        )

    def handle_v2_list(self, method: str) -> None:
        del method
        actor = self.require_actor()

        if actor is None:
            return

        if not authorize(actor, Action.LIST_DOCUMENTS):
            self.reply(403, {"error": "Forbidden"})
            return

        documents = [
            public_document(document)
            for document in DOCUMENTS.values()
            if authorize(actor, Action.READ_DOCUMENT, document)
        ]

        documents.sort(key=lambda document: str(document["id"]))
        self.reply(200, {"documents": documents})

    def handle_v2_document(
        self,
        method: str,
        document_id: str,
    ) -> None:
        actor = self.require_actor()

        if actor is None:
            return

        document = DOCUMENTS.get(document_id)
        action = (
            Action.READ_DOCUMENT
            if method == "GET"
            else Action.UPDATE_DOCUMENT
        )

        if document is None or not authorize(actor, action, document):
            self.reply(404, {"error": "Document not found"})
            return

        if method == "GET":
            self.reply(200, {"document": public_document(document)})
            return

        payload = self.json_body()
        supplied_fields = set(payload)

        if not supplied_fields:
            raise RequestError(400, "At least one property is required")

        unsupported_fields = supplied_fields - V2_DOCUMENT_WRITE_FIELDS

        if unsupported_fields:
            raise RequestError(
                400,
                "Unsupported document properties: "
                + ", ".join(sorted(unsupported_fields)),
            )

        for name in supplied_fields:
            value = payload[name]

            if not isinstance(value, str) or not value.strip():
                raise RequestError(
                    400,
                    f"{name} must be a non-empty string",
                )

        for name in supplied_fields:
            document[name] = payload[name]

        self.reply(200, {"document": public_document(document)})

    def handle_v2_export(
        self,
        method: str,
        tenant_id: str,
    ) -> None:
        del method
        actor = self.require_actor()

        if actor is None:
            return

        allowed = authorize(
            actor,
            Action.EXPORT_ORGANIZATION,
            target_tenant=tenant_id,
        )

        record_audit(
            actor,
            Action.EXPORT_ORGANIZATION.value,
            tenant_id,
            "allowed" if allowed else "denied",
        )

        if not allowed:
            self.reply(403, {"error": "Forbidden"})
            return

        documents = [
            public_document(document)
            for document in DOCUMENTS.values()
            if document.get("tenant_id") == tenant_id
        ]

        self.reply(
            200,
            {
                "tenant_id": tenant_id,
                "documents": documents,
            },
        )

    def handle_v2_support(
        self,
        method: str,
        tenant_id: str,
    ) -> None:
        del method
        actor = self.require_actor()

        if actor is None:
            return

        allowed = authorize(
            actor,
            Action.RUN_SUPPORT_OPERATION,
            target_tenant=tenant_id,
        )

        record_audit(
            actor,
            Action.RUN_SUPPORT_OPERATION.value,
            tenant_id,
            "allowed" if allowed else "denied",
        )

        if not allowed:
            self.reply(403, {"error": "Forbidden"})
            return

        self.reply(
            200,
            {
                "tenant_id": tenant_id,
                "status": "tenant unlocked",
            },
        )

    def handle_v2_audit(self, method: str) -> None:
        del method
        actor = self.require_actor()

        if actor is None:
            return

        allowed = authorize(actor, Action.READ_AUDIT_LOG)

        record_audit(
            actor,
            Action.READ_AUDIT_LOG.value,
            "audit-log",
            "allowed" if allowed else "denied",
        )

        if not allowed:
            self.reply(403, {"error": "Forbidden"})
            return

        self.reply(200, {"events": deepcopy(AUDIT_LOG)})

    def do_GET(self) -> None:
        self.dispatch("GET")

    def do_POST(self) -> None:
        self.dispatch("POST")

    def do_PATCH(self) -> None:
        self.dispatch("PATCH")

    def do_PUT(self) -> None:
        self.dispatch("PUT")

    def do_DELETE(self) -> None:
        self.dispatch("DELETE")

    def do_OPTIONS(self) -> None:
        self.dispatch("OPTIONS")

    def do_HEAD(self) -> None:
        self.dispatch("HEAD")

    def do_TRACE(self) -> None:
        self.dispatch("TRACE")


def create_server(
    host: str = HOST,
    port: int = PORT,
) -> ThreadingHTTPServer:
    if host != "127.0.0.1":
        raise ValueError("AcmeDocs must bind only to 127.0.0.1")

    return ThreadingHTTPServer((host, port), Handler)


def main() -> None:
    server = create_server()

    print(f"AcmeDocs listening on http://{HOST}:{PORT}")
    print("Local lab only. /api/v1 is intentionally vulnerable.")
    print("Demo actors: alice, bob, admin_alpha, support_admin")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping AcmeDocs")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
