"""Automated security tests for the local session-management lab."""

from __future__ import annotations

from http.client import HTTPConnection
from http.cookies import SimpleCookie
import json
from pathlib import Path
import sys
import threading
import unittest
from unittest.mock import patch


APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from server import (  # noqa: E402
    build_clear_cookie,
    build_session_cookie,
    create_server,
)
from session_manager import FakeClock, SessionManager  # noqa: E402


class SessionManagementTests(unittest.TestCase):
    def setUp(self) -> None:
        self.clock = FakeClock(1_000.0)
        self.manager = SessionManager(
            idle_timeout=10.0,
            absolute_timeout=30.0,
            clock=self.clock,
            log_key=b"L" * 32,
        )
        self.server = create_server(port=0, manager=self.manager)
        self.thread = threading.Thread(
            target=lambda: self.server.serve_forever(poll_interval=0.01),
            daemon=True,
        )
        self.thread.start()
        self.port = self.server.server_address[1]

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def request(
        self,
        method: str,
        path: str,
        *,
        body: object | None = None,
        cookie: str | None = None,
        headers: dict[str, str] | None = None,
    ) -> tuple[int, dict[str, str], object | None]:
        request_headers = dict(headers or {})
        raw_body: bytes | None = None
        if body is not None:
            raw_body = json.dumps(body).encode("utf-8")
            request_headers.setdefault("Content-Type", "application/json")
        if cookie is not None:
            request_headers["Cookie"] = f"session={cookie}"

        connection = HTTPConnection("127.0.0.1", self.port, timeout=2)
        connection.request(method, path, body=raw_body, headers=request_headers)
        response = connection.getresponse()
        raw_response = response.read()
        response_headers = {name.lower(): value for name, value in response.getheaders()}
        connection.close()
        payload = json.loads(raw_response) if raw_response else None
        return response.status, response_headers, payload

    @staticmethod
    def token_from_headers(headers: dict[str, str]) -> str:
        jar = SimpleCookie()
        jar.load(headers["set-cookie"])
        return jar["session"].value

    def login(
        self,
        username: str = "alice",
        *,
        cookie: str | None = None,
        extra: dict[str, object] | None = None,
    ) -> tuple[str, dict[str, str], object]:
        body: dict[str, object] = {"username": username}
        body.update(extra or {})
        status, headers, payload = self.request(
            "POST", "/login", body=body, cookie=cookie
        )
        self.assertEqual(200, status)
        return self.token_from_headers(headers), headers, payload

    def test_01_csprng_requests_32_random_bytes(self) -> None:
        with patch("session_manager.secrets.token_bytes", return_value=b"A" * 32) as mocked:
            token = SessionManager._csprng_token()
        mocked.assert_called_once_with(32)
        self.assertEqual("41" * 32, token)

    def test_02_token_has_256_bits_before_encoding(self) -> None:
        token = self.manager.start_anonymous()
        self.assertEqual(64, len(token))
        self.assertEqual(32, len(bytes.fromhex(token)))
        self.assertEqual(256, self.manager.TOKEN_ENTROPY_BITS)

    def test_03_tokens_are_unique(self) -> None:
        tokens = {self.manager.start_anonymous() for _ in range(100)}
        self.assertEqual(100, len(tokens))

    def test_04_unknown_token_is_rejected(self) -> None:
        self.assertIsNone(self.manager.resolve("f" * 64))

    def test_05_forged_token_is_rejected(self) -> None:
        token = self.manager.start_anonymous()
        forged = ("0" if token[0] != "0" else "1") + token[1:]
        self.assertIsNone(self.manager.resolve(forged))

    def test_06_anonymous_session_is_server_side(self) -> None:
        token = self.manager.start_anonymous()
        snapshot = self.manager.safe_snapshot(token)
        self.assertEqual("anonymous", snapshot["state"])
        self.assertNotIn("token", snapshot)

    def test_07_login_issues_authenticated_session(self) -> None:
        token, _headers, _payload = self.login()
        snapshot = self.manager.safe_snapshot(token)
        self.assertEqual("authenticated", snapshot["state"])
        self.assertEqual("alice", snapshot["user_id"])

    def test_08_login_rotates_prelogin_token(self) -> None:
        status, headers, _payload = self.request("POST", "/session/prelogin")
        self.assertEqual(201, status)
        old_token = self.token_from_headers(headers)
        new_token, _headers, _payload = self.login(cookie=old_token)
        self.assertNotEqual(old_token, new_token)
        self.assertIsNone(self.manager.resolve(old_token))

    def test_09_attacker_prelogin_cookie_is_not_preserved(self) -> None:
        attacker_token = "a" * 64
        new_token, _headers, _payload = self.login(cookie=attacker_token)
        self.assertNotEqual(attacker_token, new_token)
        self.assertIsNone(self.manager.resolve(attacker_token))

    def test_10_relogin_rotates_authenticated_token(self) -> None:
        old_token, _headers, _payload = self.login()
        new_token, _headers, _payload = self.login(cookie=old_token)
        self.assertNotEqual(old_token, new_token)
        self.assertIsNone(self.manager.resolve(old_token))

    def test_11_privilege_change_rotates_token(self) -> None:
        old_token, _headers, _payload = self.login("admin")
        status, headers, payload = self.request(
            "POST", "/session/step-up", cookie=old_token
        )
        self.assertEqual(200, status)
        self.assertEqual("rotated", payload["status"])
        new_token = self.token_from_headers(headers)
        self.assertNotEqual(old_token, new_token)

    def test_12_old_token_after_privilege_change_is_rejected(self) -> None:
        old_token, _headers, _payload = self.login("admin")
        status, headers, _payload = self.request(
            "POST", "/session/step-up", cookie=old_token
        )
        self.assertEqual(200, status)
        self.assertTrue(self.token_from_headers(headers))
        status, _headers, _payload = self.request("GET", "/me", cookie=old_token)
        self.assertEqual(401, status)

    def test_13_new_token_after_privilege_change_works(self) -> None:
        old_token, _headers, _payload = self.login("admin")
        _status, headers, _payload = self.request(
            "POST", "/session/step-up", cookie=old_token
        )
        new_token = self.token_from_headers(headers)
        status, _headers, payload = self.request("GET", "/me", cookie=new_token)
        self.assertEqual(200, status)
        self.assertEqual("elevated", payload["auth_level"])

    def test_14_logout_revokes_session(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request("POST", "/logout", cookie=token)
        self.assertEqual(200, status)
        self.assertEqual("revoked", self.manager.safe_snapshot(token)["state"])

    def test_15_replay_after_logout_is_rejected(self) -> None:
        token, _headers, _payload = self.login()
        self.request("POST", "/logout", cookie=token)
        status, _headers, _payload = self.request("GET", "/me", cookie=token)
        self.assertEqual(401, status)

    def test_16_idle_timeout_expires_session(self) -> None:
        token, _headers, _payload = self.login()
        self.clock.advance(10)
        status, _headers, _payload = self.request("GET", "/me", cookie=token)
        self.assertEqual(401, status)
        self.assertEqual("idle_timeout", self.manager.safe_snapshot(token)["revocation_reason"])

    def test_17_activity_refreshes_idle_deadline(self) -> None:
        token, _headers, _payload = self.login()
        self.clock.advance(9)
        self.assertEqual(200, self.request("GET", "/me", cookie=token)[0])
        self.clock.advance(9)
        self.assertEqual(200, self.request("GET", "/me", cookie=token)[0])

    def test_18_absolute_timeout_expires_active_session(self) -> None:
        token, _headers, _payload = self.login()
        for _ in range(3):
            self.clock.advance(9)
            self.assertEqual(200, self.request("GET", "/me", cookie=token)[0])
        self.clock.advance(3)
        self.assertEqual(401, self.request("GET", "/me", cookie=token)[0])
        self.assertEqual(
            "absolute_timeout",
            self.manager.safe_snapshot(token)["revocation_reason"],
        )

    def test_19_rotation_does_not_extend_absolute_deadline(self) -> None:
        old_token, _headers, _payload = self.login("admin")
        old_deadline = self.manager.safe_snapshot(old_token)["absolute_expires_at"]
        self.clock.advance(5)
        _status, headers, _payload = self.request(
            "POST", "/session/step-up", cookie=old_token
        )
        new_token = self.token_from_headers(headers)
        new_deadline = self.manager.safe_snapshot(new_token)["absolute_expires_at"]
        self.assertEqual(old_deadline, new_deadline)

    def test_20_query_session_token_is_not_accepted(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request(
            "GET", f"/me?session={token}"
        )
        self.assertEqual(401, status)

    def test_21_custom_session_header_is_not_accepted(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request(
            "GET", "/me", headers={"X-Session-ID": token}
        )
        self.assertEqual(401, status)

    def test_22_bearer_token_is_not_accepted(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request(
            "GET", "/me", headers={"Authorization": f"Bearer {token}"}
        )
        self.assertEqual(401, status)

    def test_23_local_cookie_has_required_attributes(self) -> None:
        _token, headers, _payload = self.login()
        cookie = headers["set-cookie"]
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)
        self.assertIn("Path=/", cookie)
        self.assertNotIn("Secure", cookie)

    def test_24_production_cookie_adds_secure(self) -> None:
        cookie = build_session_cookie("opaque", secure=True)
        self.assertIn("Secure", cookie)
        self.assertIn("HttpOnly", cookie)
        self.assertIn("SameSite=Lax", cookie)

    def test_25_logout_cookie_is_cleared(self) -> None:
        token, _headers, _payload = self.login()
        _status, headers, _payload = self.request("POST", "/logout", cookie=token)
        cookie = headers["set-cookie"]
        self.assertIn("session=;", cookie)
        self.assertIn("Max-Age=0", cookie)

    def test_26_production_clear_cookie_keeps_secure(self) -> None:
        self.assertIn("Secure", build_clear_cookie(secure=True))

    def test_27_explicitly_revoked_session_is_denied(self) -> None:
        token, _headers, _payload = self.login()
        self.assertTrue(self.manager.revoke(token, reason="security_event"))
        self.assertIsNone(self.manager.resolve(token))

    def test_28_logs_contain_fingerprint_not_raw_token(self) -> None:
        token, _headers, _payload = self.login()
        self.manager.revoke(token, reason="logout")
        combined = "\n".join(self.manager.log_events())
        self.assertNotIn(token, combined)
        self.assertIn(self.manager.fingerprint(token), combined)

    def test_29_client_role_and_tenant_fields_are_ignored(self) -> None:
        token, _headers, _payload = self.login(
            extra={"role": "admin", "tenant_id": "beta"}
        )
        status, _headers, payload = self.request("GET", "/me", cookie=token)
        self.assertEqual(200, status)
        self.assertEqual("user", payload["role"])
        self.assertEqual("alpha", payload["tenant_id"])

    def test_30_query_role_does_not_grant_admin_access(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request(
            "GET", "/admin?role=admin", cookie=token
        )
        self.assertEqual(403, status)

    def test_31_header_role_does_not_grant_admin_access(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request(
            "GET", "/admin", cookie=token, headers={"X-Role": "admin"}
        )
        self.assertEqual(403, status)

    def test_32_admin_requires_server_side_step_up(self) -> None:
        token, _headers, _payload = self.login("admin")
        self.assertEqual(403, self.request("GET", "/admin", cookie=token)[0])
        _status, headers, _payload = self.request(
            "POST", "/session/step-up", cookie=token
        )
        rotated = self.token_from_headers(headers)
        self.assertEqual(200, self.request("GET", "/admin", cookie=rotated)[0])

    def test_33_normal_user_cannot_trigger_privilege_rotation(self) -> None:
        token, _headers, _payload = self.login()
        status, _headers, _payload = self.request(
            "POST", "/session/step-up", cookie=token
        )
        self.assertEqual(403, status)
        self.assertIsNotNone(self.manager.resolve(token, touch=False))

    def test_34_malformed_cookie_is_rejected(self) -> None:
        status, _headers, _payload = self.request(
            "GET", "/me", headers={"Cookie": 'session="unterminated'}
        )
        self.assertEqual(401, status)

    def test_35_invalid_login_does_not_issue_cookie(self) -> None:
        status, headers, _payload = self.request(
            "POST", "/login", body={"username": "unknown"}
        )
        self.assertEqual(401, status)
        self.assertNotIn("set-cookie", headers)

    def test_36_responses_disable_caching(self) -> None:
        status, headers, _payload = self.request("GET", "/health")
        self.assertEqual(200, status)
        self.assertEqual("no-store", headers["cache-control"])

    def test_37_unsupported_method_is_rejected(self) -> None:
        status, _headers, _payload = self.request("DELETE", "/login")
        self.assertEqual(405, status)

    def test_38_unknown_route_is_denied(self) -> None:
        status, _headers, _payload = self.request("GET", "/not-a-route")
        self.assertEqual(404, status)


if __name__ == "__main__":
    unittest.main(verbosity=2)
