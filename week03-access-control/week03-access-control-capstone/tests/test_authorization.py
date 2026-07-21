from __future__ import annotations

from http.cookiejar import CookieJar
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import (
    HTTPCookieProcessor,
    Request,
    build_opener,
)
import json
import sys
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_DIRECTORY = PROJECT_ROOT / "app"
sys.path.insert(0, str(APP_DIRECTORY))

from authorization import Action, authorize  # noqa: E402
from data import (  # noqa: E402
    AUDIT_LOG,
    DOCUMENTS,
    USERS,
    reset_state,
)
from server import create_server  # noqa: E402


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.cookie_jar = CookieJar()
        self.opener = build_opener(
            HTTPCookieProcessor(self.cookie_jar)
        )

    def request(
        self,
        method: str,
        path: str,
        payload: dict[str, object] | None = None,
        headers: dict[str, str] | None = None,
        raw_body: bytes | None = None,
    ) -> tuple[int, object | None, dict[str, str]]:
        request_headers = dict(headers or {})
        body = raw_body

        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            request_headers.setdefault(
                "Content-Type",
                "application/json",
            )
        elif raw_body is not None:
            request_headers.setdefault(
                "Content-Type",
                "application/json",
            )

        request = Request(
            self.base_url + path,
            data=body,
            headers=request_headers,
            method=method,
        )

        try:
            response = self.opener.open(request, timeout=5)
        except HTTPError as error:
            response = error

        with response:
            raw_response = response.read().decode("utf-8")
            parsed_response = (
                json.loads(raw_response)
                if raw_response.strip()
                else None
            )

            return (
                response.status,
                parsed_response,
                dict(response.headers.items()),
            )

    def login(
        self,
        username: str,
        extra: dict[str, object] | None = None,
    ) -> object:
        status, payload, _ = self.request(
            "POST",
            "/demo-login",
            {
                "username": username,
                **(extra or {}),
            },
        )
        self_test = unittest.TestCase()
        self_test.assertEqual(status, 200, payload)
        return payload


class AuthorizationCapstoneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.http_server = create_server(port=0)
        cls.http_server.quiet = True
        cls.server_thread = Thread(
            target=cls.http_server.serve_forever,
            daemon=True,
        )
        cls.server_thread.start()

        port = cls.http_server.server_address[1]
        cls.base_url = f"http://127.0.0.1:{port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.http_server.shutdown()
        cls.http_server.server_close()
        cls.server_thread.join(timeout=5)

    def setUp(self) -> None:
        reset_state()

    def client(self, username: str | None = None) -> Client:
        client = Client(self.base_url)

        if username is not None:
            client.login(username)

        return client

    # Central policy tests

    def test_01_policy_denies_missing_actor(self) -> None:
        self.assertFalse(
            authorize(
                None,
                Action.READ_DOCUMENT,
                DOCUMENTS["alpha-1001"],
            )
        )

    def test_02_policy_denies_unknown_action(self) -> None:
        self.assertFalse(
            authorize(USERS["alice"], "unknown:action")
        )

    def test_03_policy_allows_alice_own_document(self) -> None:
        self.assertTrue(
            authorize(
                USERS["alice"],
                Action.READ_DOCUMENT,
                DOCUMENTS["alpha-1001"],
            )
        )

    def test_04_policy_denies_alice_beta_document(self) -> None:
        self.assertFalse(
            authorize(
                USERS["alice"],
                Action.READ_DOCUMENT,
                DOCUMENTS["beta-2001"],
            )
        )

    def test_05_policy_allows_admin_alpha_document(self) -> None:
        self.assertTrue(
            authorize(
                USERS["admin_alpha"],
                Action.UPDATE_DOCUMENT,
                DOCUMENTS["alpha-1001"],
            )
        )

    def test_06_policy_denies_admin_alpha_beta_document(self) -> None:
        self.assertFalse(
            authorize(
                USERS["admin_alpha"],
                Action.READ_DOCUMENT,
                DOCUMENTS["beta-2001"],
            )
        )

    def test_07_policy_allows_support_operation(self) -> None:
        self.assertTrue(
            authorize(
                USERS["support_admin"],
                Action.RUN_SUPPORT_OPERATION,
                target_tenant="beta",
            )
        )

    def test_08_policy_denies_user_support_operation(self) -> None:
        self.assertFalse(
            authorize(
                USERS["alice"],
                Action.RUN_SUPPORT_OPERATION,
                target_tenant="alpha",
            )
        )

    # Authentication and server-side identity tests

    def test_09_unauthenticated_v1_request_denied(self) -> None:
        status, payload, _ = self.client().request(
            "GET",
            "/api/v1/documents/alpha-1001",
        )
        self.assertEqual(status, 401)
        self.assertEqual(payload, {"error": "Authentication required"})

    def test_10_unauthenticated_v2_request_denied(self) -> None:
        status, payload, _ = self.client().request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 401)
        self.assertEqual(payload, {"error": "Authentication required"})

    def test_11_invalid_demo_user_denied(self) -> None:
        status, _, _ = self.client().request(
            "POST",
            "/demo-login",
            {"username": "unknown-user"},
        )
        self.assertEqual(status, 401)

    def test_12_client_identity_attributes_are_ignored(self) -> None:
        client = Client(self.base_url)
        payload = client.login(
            "alice",
            {
                "role": "support_admin",
                "tenant_id": "beta",
            },
        )
        self.assertEqual(
            payload,
            {
                "actor": {
                    "username": "alice",
                    "tenant_id": "alpha",
                    "role": "user",
                }
            },
        )

    def test_13_logout_invalidates_session(self) -> None:
        client = self.client("alice")
        status, _, _ = client.request("POST", "/logout")
        self.assertEqual(status, 200)

        status, _, _ = client.request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 401)

    # Intentionally vulnerable v1 proof tests

    def test_14_v1_bola_read_allows_cross_tenant_access(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v1/documents/beta-2001",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["document"]["tenant_id"], "beta")

    def test_15_v1_bola_update_allows_cross_tenant_change(self) -> None:
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v1/documents/beta-2001",
            {"content": "changed through vulnerable v1"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            DOCUMENTS["beta-2001"]["content"],
            "changed through vulnerable v1",
        )

    def test_16_v1_mass_assignment_changes_owner(self) -> None:
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v1/documents/alpha-1001",
            {"owner_id": "bob"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(DOCUMENTS["alpha-1001"]["owner_id"], "bob")

    def test_17_v1_mass_assignment_changes_tenant(self) -> None:
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v1/documents/alpha-1001",
            {"tenant_id": "beta"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(DOCUMENTS["alpha-1001"]["tenant_id"], "beta")

    def test_18_v1_response_exposes_internal_property(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v1/documents/alpha-1001",
        )
        self.assertEqual(status, 200)
        self.assertIn("internal_label", payload["document"])

    def test_19_v1_bfla_allows_user_organization_export(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v1/organizations/beta/export",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["tenant_id"], "beta")

    def test_20_v1_bfla_allows_user_support_operation(self) -> None:
        status, _, _ = self.client("alice").request(
            "POST",
            "/api/v1/support/tenants/beta/unlock",
        )
        self.assertEqual(status, 200)
        self.assertEqual(AUDIT_LOG, [])

    def test_21_v1_list_exposes_other_tenant_documents(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v1/documents",
        )
        self.assertEqual(status, 200)
        returned_ids = {
            document["id"]
            for document in payload["documents"]
        }
        self.assertIn("beta-2001", returned_ids)

    # Secure v2 positive tests

    def test_22_v2_allows_alice_own_read(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["document"]["owner_id"], "alice")

    def test_23_v2_allows_alice_own_update(self) -> None:
        status, payload, _ = self.client("alice").request(
            "PATCH",
            "/api/v2/documents/alpha-1001",
            {"content": "secure Alice update"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(
            payload["document"]["content"],
            "secure Alice update",
        )

    def test_24_v2_allows_bob_own_read(self) -> None:
        status, _, _ = self.client("bob").request(
            "GET",
            "/api/v2/documents/beta-2001",
        )
        self.assertEqual(status, 200)

    def test_25_v2_allows_admin_alpha_tenant_read(self) -> None:
        status, _, _ = self.client("admin_alpha").request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 200)

    def test_26_v2_allows_admin_alpha_tenant_update(self) -> None:
        status, _, _ = self.client("admin_alpha").request(
            "PATCH",
            "/api/v2/documents/alpha-1001",
            {"title": "Updated by Alpha administrator"},
        )
        self.assertEqual(status, 200)

    def test_27_v2_allows_admin_alpha_export(self) -> None:
        status, payload, _ = self.client("admin_alpha").request(
            "GET",
            "/api/v2/organizations/alpha/export",
        )
        self.assertEqual(status, 200)
        self.assertEqual(payload["tenant_id"], "alpha")

    def test_28_v2_allows_support_admin_operation(self) -> None:
        status, _, _ = self.client("support_admin").request(
            "POST",
            "/api/v2/support/tenants/beta/unlock",
        )
        self.assertEqual(status, 200)

    def test_29_v2_privileged_operation_has_audit_attribution(self) -> None:
        client = self.client("support_admin")
        status, _, _ = client.request(
            "POST",
            "/api/v2/support/tenants/beta/unlock",
        )
        self.assertEqual(status, 200)
        self.assertEqual(AUDIT_LOG[-1]["actor"], "support_admin")
        self.assertEqual(AUDIT_LOG[-1]["target"], "beta")
        self.assertEqual(AUDIT_LOG[-1]["outcome"], "allowed")

    def test_30_v2_support_admin_can_read_audit_log(self) -> None:
        client = self.client("support_admin")
        client.request(
            "POST",
            "/api/v2/support/tenants/alpha/unlock",
        )
        status, payload, _ = client.request("GET", "/api/v2/audit")
        self.assertEqual(status, 200)
        self.assertGreaterEqual(len(payload["events"]), 2)

    def test_31_v2_list_is_scoped_to_authorized_documents(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents",
        )
        self.assertEqual(status, 200)
        returned_ids = [
            document["id"]
            for document in payload["documents"]
        ]
        self.assertEqual(returned_ids, ["alpha-1001"])

    def test_32_v2_response_uses_property_allowlist(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 200)
        self.assertNotIn("tenant_id", payload["document"])
        self.assertNotIn("internal_label", payload["document"])

    # Secure v2 negative tests

    def test_33_v2_denies_alice_cross_tenant_read(self) -> None:
        status, _, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents/beta-2001",
        )
        self.assertEqual(status, 404)

    def test_34_v2_denies_alice_unowned_same_tenant_read(self) -> None:
        status, _, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents/alpha-1002",
        )
        self.assertEqual(status, 404)

    def test_35_v2_denies_bob_alpha_read(self) -> None:
        status, _, _ = self.client("bob").request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 404)

    def test_36_v2_denies_admin_alpha_beta_read(self) -> None:
        status, _, _ = self.client("admin_alpha").request(
            "GET",
            "/api/v2/documents/beta-2001",
        )
        self.assertEqual(status, 404)

    def test_37_denied_v2_update_leaves_document_unchanged(self) -> None:
        original = DOCUMENTS["beta-2001"]["content"]
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v2/documents/beta-2001",
            {"content": "must never be stored"},
        )
        self.assertEqual(status, 404)
        self.assertEqual(DOCUMENTS["beta-2001"]["content"], original)

    def test_38_v2_rejects_mass_assignment_atomically(self) -> None:
        original = dict(DOCUMENTS["alpha-1001"])
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v2/documents/alpha-1001",
            {
                "content": "must not be partially stored",
                "owner_id": "bob",
                "tenant_id": "beta",
            },
        )
        self.assertEqual(status, 400)
        self.assertEqual(DOCUMENTS["alpha-1001"], original)

    def test_39_client_supplied_role_in_body_is_rejected(self) -> None:
        original = dict(DOCUMENTS["alpha-1001"])
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v2/documents/alpha-1001",
            {
                "content": "attempted update",
                "role": "support_admin",
            },
        )
        self.assertEqual(status, 400)
        self.assertEqual(DOCUMENTS["alpha-1001"], original)

    def test_40_query_and_header_role_cannot_bypass_policy(self) -> None:
        status, _, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents/beta-2001?role=support_admin",
            headers={"X-Role": "support_admin"},
        )
        self.assertEqual(status, 404)

    def test_41_v2_denies_user_organization_export(self) -> None:
        status, _, _ = self.client("alice").request(
            "GET",
            "/api/v2/organizations/alpha/export",
        )
        self.assertEqual(status, 403)
        self.assertEqual(AUDIT_LOG[-1]["outcome"], "denied")

    def test_42_v2_denies_admin_alpha_beta_export(self) -> None:
        status, _, _ = self.client("admin_alpha").request(
            "GET",
            "/api/v2/organizations/beta/export",
        )
        self.assertEqual(status, 403)

    def test_43_v2_denies_user_support_operation(self) -> None:
        status, _, _ = self.client("alice").request(
            "POST",
            "/api/v2/support/tenants/alpha/unlock",
        )
        self.assertEqual(status, 403)
        self.assertEqual(AUDIT_LOG[-1]["actor"], "alice")
        self.assertEqual(AUDIT_LOG[-1]["outcome"], "denied")

    def test_44_v2_denies_support_admin_document_read(self) -> None:
        status, _, _ = self.client("support_admin").request(
            "GET",
            "/api/v2/documents/alpha-1001",
        )
        self.assertEqual(status, 404)

    def test_45_alternative_method_is_rejected(self) -> None:
        status, _, headers = self.client("alice").request(
            "PUT",
            "/api/v2/documents/alpha-1001",
            {"content": "method bypass"},
        )
        self.assertEqual(status, 405)
        self.assertEqual(headers.get("Allow"), "GET, PATCH")

    def test_46_nonexistent_document_is_handled_safely(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v2/documents/not-a-real-document",
        )
        self.assertEqual(status, 404)
        self.assertEqual(payload, {"error": "Document not found"})

    def test_47_invalid_json_does_not_change_state(self) -> None:
        original = dict(DOCUMENTS["alpha-1001"])
        status, _, _ = self.client("alice").request(
            "PATCH",
            "/api/v2/documents/alpha-1001",
            raw_body=b"{invalid-json",
        )
        self.assertEqual(status, 400)
        self.assertEqual(DOCUMENTS["alpha-1001"], original)

    def test_48_unknown_route_is_denied(self) -> None:
        status, payload, _ = self.client("alice").request(
            "GET",
            "/api/v2/unknown",
        )
        self.assertEqual(status, 404)
        self.assertEqual(payload, {"error": "Route not found"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
