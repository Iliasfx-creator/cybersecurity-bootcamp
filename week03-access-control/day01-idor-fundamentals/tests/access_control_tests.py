from __future__ import annotations

from http.cookiejar import CookieJar
import json
import sys
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import (
    HTTPCookieProcessor,
    Request,
    build_opener,
)

BASE_URL = "http://127.0.0.1:8010"

BOB_DOCUMENT_ID = 201
ORIGINAL_BOB_CONTENT = "Bob document 201"


class Client:
    def __init__(self) -> None:
        self.cookie_jar = CookieJar()
        self.opener = build_opener(
            HTTPCookieProcessor(self.cookie_jar)
        )

    def request(
        self,
        method: str,
        path: str,
        form: dict[str, str] | None = None,
    ) -> tuple[int, dict | list | None, dict[str, str]]:
        data = None
        headers: dict[str, str] = {}

        if form is not None:
            data = urlencode(form).encode("utf-8")
            headers["Content-Type"] = (
                "application/x-www-form-urlencoded"
            )

        request = Request(
            BASE_URL + path,
            data=data,
            headers=headers,
            method=method,
        )

        try:
            with self.opener.open(
                request,
                timeout=5,
            ) as response:
                raw_body = response.read().decode("utf-8")
                payload = (
                    json.loads(raw_body)
                    if raw_body.strip()
                    else None
                )

                return (
                    response.status,
                    payload,
                    dict(response.headers),
                )

        except HTTPError as error:
            raw_body = error.read().decode("utf-8")
            payload = (
                json.loads(raw_body)
                if raw_body.strip()
                else None
            )

            return (
                error.code,
                payload,
                dict(error.headers),
            )

    def get(
        self,
        path: str,
    ) -> tuple[int, dict | list | None, dict[str, str]]:
        return self.request("GET", path)

    def post(
        self,
        path: str,
        form: dict[str, str] | None = None,
    ) -> tuple[int, dict | list | None, dict[str, str]]:
        return self.request("POST", path, form)

    def login(self, username: str) -> None:
        status, payload, _ = self.post(
            "/demo-login",
            {"username": username},
        )

        assert status == 200, (
            f"Login failed for {username}: "
            f"status={status}, payload={payload}"
        )


def logged_in_client(username: str) -> Client:
    client = Client()
    client.login(username)
    return client


def restore_bob_document() -> None:
    bob = logged_in_client("bob")

    status, payload, _ = bob.post(
        "/safe/document/update",
        {
            "id": str(BOB_DOCUMENT_ID),
            "content": ORIGINAL_BOB_CONTENT,
        },
    )

    assert status == 200, (
        f"Could not restore Bob document: "
        f"status={status}, payload={payload}"
    )


def test_protected_list_without_session() -> None:
    client = Client()

    status, _, _ = client.get("/documents")

    assert status == 401


def test_vulnerable_read_without_session() -> None:
    client = Client()

    status, _, _ = client.get(
        "/vuln/document?id=201"
    )

    assert status == 401


def test_alice_list_excludes_bob_documents() -> None:
    alice = logged_in_client("alice")

    status, payload, _ = alice.get("/documents")

    assert status == 200
    assert isinstance(payload, dict)

    document_ids = {
        document["id"]
        for document in payload["documents"]
    }

    assert document_ids == {101, 102}
    assert 201 not in document_ids
    assert 202 not in document_ids


def test_alice_reads_own_document_vulnerable() -> None:
    alice = logged_in_client("alice")

    status, payload, _ = alice.get(
        "/vuln/document?id=101"
    )

    assert status == 200
    assert isinstance(payload, dict)
    assert payload["document"]["owner"] == "alice"


def test_alice_reads_bob_document_vulnerable() -> None:
    alice = logged_in_client("alice")

    status, payload, _ = alice.get(
        "/vuln/document?id=201"
    )

    assert status == 200
    assert isinstance(payload, dict)
    assert payload["document"]["owner"] == "bob"


def test_alice_reads_bob_document_safe_denied() -> None:
    alice = logged_in_client("alice")

    status, payload, _ = alice.get(
        "/safe/document?id=201"
    )

    assert status == 404
    assert payload == {"error": "Document not found"}


def test_bob_reads_own_document_safe() -> None:
    bob = logged_in_client("bob")

    status, payload, _ = bob.get(
        "/safe/document?id=201"
    )

    assert status == 200
    assert isinstance(payload, dict)
    assert payload["document"]["owner"] == "bob"


def test_vulnerable_update_changes_bob_document() -> None:
    restore_bob_document()

    try:
        alice = logged_in_client("alice")

        status, payload, _ = alice.post(
            "/vuln/document/update",
            {
                "id": "201",
                "content": "changed-by-alice-test",
            },
        )

        assert status == 200
        assert isinstance(payload, dict)
        assert payload["document"]["owner"] == "bob"

        bob = logged_in_client("bob")

        status, payload, _ = bob.get(
            "/safe/document?id=201"
        )

        assert status == 200
        assert isinstance(payload, dict)
        assert (
            payload["document"]["content"]
            == "changed-by-alice-test"
        )

    finally:
        restore_bob_document()


def test_safe_update_of_bob_document_denied() -> None:
    restore_bob_document()
    alice = logged_in_client("alice")

    status, payload, _ = alice.post(
        "/safe/document/update",
        {
            "id": "201",
            "content": "unauthorized-change",
        },
    )

    assert status == 404
    assert payload == {"error": "Document not found"}


def test_safe_update_preserves_bob_document() -> None:
    restore_bob_document()
    alice = logged_in_client("alice")

    alice.post(
        "/safe/document/update",
        {
            "id": "201",
            "content": "must-not-be-stored",
        },
    )

    bob = logged_in_client("bob")

    status, payload, _ = bob.get(
        "/safe/document?id=201"
    )

    assert status == 200
    assert isinstance(payload, dict)
    assert (
        payload["document"]["content"]
        == ORIGINAL_BOB_CONTENT
    )


def test_invalid_read_ids_return_400() -> None:
    alice = logged_in_client("alice")

    invalid_values = [
        "",
        "abc",
        "20.1",
        "-1",
    ]

    for value in invalid_values:
        status, _, _ = alice.get(
            f"/safe/document?id={value}"
        )

        assert status == 400, (
            f"Expected 400 for id={value!r}, "
            f"received {status}"
        )


def test_invalid_update_id_returns_400() -> None:
    alice = logged_in_client("alice")

    status, _, _ = alice.post(
        "/safe/document/update",
        {
            "id": "abc",
            "content": "test",
        },
    )

    assert status == 400


def test_missing_document_returns_404() -> None:
    alice = logged_in_client("alice")

    status, _, _ = alice.get(
        "/safe/document?id=999"
    )

    assert status == 404


def test_unknown_get_route_returns_404() -> None:
    client = Client()

    status, _, _ = client.get("/unknown")

    assert status == 404


def test_unknown_post_route_returns_404() -> None:
    client = Client()

    status, _, _ = client.post(
        "/unknown",
        {"value": "test"},
    )

    assert status == 404


def test_logout_invalidates_session() -> None:
    alice = logged_in_client("alice")

    status, _, _ = alice.post("/logout")

    assert status == 204

    status, _, _ = alice.get("/documents")

    assert status == 401


def test_unknown_demo_user_rejected() -> None:
    client = Client()

    status, payload, _ = client.post(
        "/demo-login",
        {"username": "charlie"},
    )

    assert status == 400
    assert payload == {"error": "Unknown demo user"}


def run_test(name: str, test_function) -> bool:
    try:
        test_function()
        print(f"[PASS] {name}")
        return True

    except Exception as error:
        print(f"[FAIL] {name}: {error}")
        return False


def main() -> int:
    tests = [
        (
            "Protected list without session returns 401",
            test_protected_list_without_session,
        ),
        (
            "Vulnerable read still requires authentication",
            test_vulnerable_read_without_session,
        ),
        (
            "Alice list excludes Bob documents",
            test_alice_list_excludes_bob_documents,
        ),
        (
            "Alice reads own document through vulnerable route",
            test_alice_reads_own_document_vulnerable,
        ),
        (
            "Alice reads Bob document through vulnerable route",
            test_alice_reads_bob_document_vulnerable,
        ),
        (
            "Safe route denies Alice access to Bob document",
            test_alice_reads_bob_document_safe_denied,
        ),
        (
            "Bob reads own document through safe route",
            test_bob_reads_own_document_safe,
        ),
        (
            "Vulnerable update changes Bob document",
            test_vulnerable_update_changes_bob_document,
        ),
        (
            "Safe update of Bob document is denied",
            test_safe_update_of_bob_document_denied,
        ),
        (
            "Safe update leaves Bob document unchanged",
            test_safe_update_preserves_bob_document,
        ),
        (
            "Invalid read identifiers return 400",
            test_invalid_read_ids_return_400,
        ),
        (
            "Invalid update identifier returns 400",
            test_invalid_update_id_returns_400,
        ),
        (
            "Missing document returns 404",
            test_missing_document_returns_404,
        ),
        (
            "Unknown GET route returns 404",
            test_unknown_get_route_returns_404,
        ),
        (
            "Unknown POST route returns 404",
            test_unknown_post_route_returns_404,
        ),
        (
            "Logout invalidates session",
            test_logout_invalidates_session,
        ),
        (
            "Unknown demo user is rejected",
            test_unknown_demo_user_rejected,
        ),
    ]

    results = [
        run_test(name, test_function)
        for name, test_function in tests
    ]

    passed = sum(results)
    failed = len(results) - passed

    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
