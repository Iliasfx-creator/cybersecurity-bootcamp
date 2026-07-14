from http.cookiejar import CookieJar
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import (
    HTTPCookieProcessor,
    Request,
    build_opener,
)
import json
import sys

BASE_URL = "http://127.0.0.1:8011"

ALICE_DOC = 101
BOB_DOC = 201

ALICE_ORIGINAL = "Alice document 101"
BOB_ORIGINAL = "Bob document 201"


class Client:
    def __init__(self):
        cookie_jar = CookieJar()

        self.opener = build_opener(
            HTTPCookieProcessor(cookie_jar)
        )

    def request(
        self,
        method,
        path,
        form=None,
        headers=None,
    ):
        body = (
            urlencode(form).encode()
            if form is not None
            else None
        )

        request_headers = dict(headers or {})

        if form is not None:
            request_headers["Content-Type"] = (
                "application/x-www-form-urlencoded"
            )

        request = Request(
            BASE_URL + path,
            data=body,
            headers=request_headers,
            method=method,
        )

        try:
            response = self.opener.open(
                request,
                timeout=5,
            )
        except HTTPError as error:
            response = error

        with response:
            raw_body = response.read().decode()

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

    def get(self, path, headers=None):
        return self.request(
            "GET",
            path,
            headers=headers,
        )

    def post(
        self,
        path,
        form=None,
        headers=None,
    ):
        return self.request(
            "POST",
            path,
            form,
            headers,
        )

    def login(
        self,
        username,
        extra=None,
        headers=None,
    ):
        form = {
            "username": username,
            **(extra or {}),
        }

        status, payload, _ = self.post(
            "/demo-login",
            form,
            headers,
        )

        assert status == 200, (
            status,
            payload,
        )

        return payload


def logged_in(
    username,
    extra=None,
    headers=None,
):
    client = Client()
    client.login(username, extra, headers)
    return client


def read_document(client, document_id):
    return client.get(
        f"/document?id={document_id}"
    )


def update_document(
    client,
    document_id,
    content,
):
    return client.post(
        "/document/update",
        {
            "id": str(document_id),
            "content": content,
        },
    )


def change_role(
    client,
    username,
    role,
):
    return client.post(
        "/admin/users/role",
        {
            "username": username,
            "role": role,
        },
    )


def restore_document(
    owner,
    document_id,
    content,
):
    owner_client = logged_in(owner)

    status, payload, _ = update_document(
        owner_client,
        document_id,
        content,
    )

    assert status == 200, (
        status,
        payload,
    )


def unauthenticated_denied():
    client = Client()

    status, payload, _ = client.get(
        "/documents"
    )

    assert status == 401
    assert payload == {
        "error": "Authentication required"
    }


def alice_own_allowed():
    restore_document(
        "alice",
        ALICE_DOC,
        ALICE_ORIGINAL,
    )

    alice = logged_in("alice")

    status, payload, _ = read_document(
        alice,
        ALICE_DOC,
    )

    assert status == 200
    assert (
        payload["document"]["owner"]
        == "alice"
    )

    try:
        status, _, _ = update_document(
            alice,
            ALICE_DOC,
            "alice-update",
        )

        assert status == 200

    finally:
        restore_document(
            "alice",
            ALICE_DOC,
            ALICE_ORIGINAL,
        )


def alice_to_bob_denied():
    alice = logged_in("alice")

    status, payload, _ = read_document(
        alice,
        BOB_DOC,
    )

    assert status == 404
    assert payload == {
        "error": "Document not found"
    }

    status, payload, _ = update_document(
        alice,
        BOB_DOC,
        "forbidden-update",
    )

    assert status == 404
    assert payload == {
        "error": "Document not found"
    }


def denied_update_unchanged():
    restore_document(
        "bob",
        BOB_DOC,
        BOB_ORIGINAL,
    )

    alice = logged_in("alice")

    status, _, _ = update_document(
        alice,
        BOB_DOC,
        "must-not-save",
    )

    assert status == 404

    bob = logged_in("bob")

    status, payload, _ = read_document(
        bob,
        BOB_DOC,
    )

    assert status == 200
    assert (
        payload["document"]["content"]
        == BOB_ORIGINAL
    )


def bob_own_allowed():
    restore_document(
        "bob",
        BOB_DOC,
        BOB_ORIGINAL,
    )

    bob = logged_in("bob")

    status, payload, _ = read_document(
        bob,
        BOB_DOC,
    )

    assert status == 200
    assert payload["document"]["owner"] == "bob"

    try:
        status, _, _ = update_document(
            bob,
            BOB_DOC,
            "bob-update",
        )

        assert status == 200

    finally:
        restore_document(
            "bob",
            BOB_DOC,
            BOB_ORIGINAL,
        )


def non_admin_operation_denied():
    admin = logged_in("admin")

    change_role(
        admin,
        "alice",
        "user",
    )

    alice = logged_in("alice")

    status, payload, _ = change_role(
        alice,
        "bob",
        "admin",
    )

    assert status == 403
    assert payload == {
        "error": "Forbidden"
    }


def admin_operation_allowed():
    admin = logged_in("admin")

    try:
        status, payload, _ = change_role(
            admin,
            "bob",
            "admin",
        )

        assert status == 200
        assert (
            payload["user"]["role"]
            == "admin"
        )

    finally:
        status, _, _ = change_role(
            admin,
            "bob",
            "user",
        )

        assert status == 200


def client_role_ignored():
    admin = logged_in("admin")

    change_role(
        admin,
        "alice",
        "user",
    )

    change_role(
        admin,
        "bob",
        "user",
    )

    alice = Client()

    login_payload = alice.login(
        "alice",
        {"role": "admin"},
        {"X-Role": "admin"},
    )

    assert login_payload["role"] == "user"

    status, payload, _ = alice.post(
        "/admin/users/role?role=admin",
        {
            "username": "bob",
            "role": "admin",
        },
        {"X-Role": "admin"},
    )

    assert status == 403
    assert payload == {
        "error": "Forbidden"
    }


def admin_all_documents():
    restore_document(
        "bob",
        BOB_DOC,
        BOB_ORIGINAL,
    )

    admin = logged_in("admin")

    status, payload, _ = admin.get(
        "/documents"
    )

    document_ids = {
        document["id"]
        for document in payload["documents"]
    }

    assert status == 200
    assert document_ids == {
        101,
        102,
        201,
        202,
    }

    try:
        status, _, _ = update_document(
            admin,
            BOB_DOC,
            "admin-update",
        )

        assert status == 200

    finally:
        restore_document(
            "bob",
            BOB_DOC,
            BOB_ORIGINAL,
        )


def alternative_method_rejected():
    restore_document(
        "bob",
        BOB_DOC,
        BOB_ORIGINAL,
    )

    admin = logged_in("admin")

    status, payload, headers = (
        admin.request(
            "PUT",
            "/document/update",
            {
                "id": str(BOB_DOC),
                "content": "method-bypass",
            },
        )
    )

    assert status == 405
    assert payload == {
        "error": "Method not allowed"
    }
    assert headers.get("Allow") == "POST"

    bob = logged_in("bob")

    status, payload, _ = read_document(
        bob,
        BOB_DOC,
    )

    assert status == 200
    assert (
        payload["document"]["content"]
        == BOB_ORIGINAL
    )


def invalid_and_missing_ids_safe():
    alice = logged_in("alice")

    invalid_values = [
        "",
        "abc",
        "20.1",
        "-1",
    ]

    for value in invalid_values:
        status, _, _ = alice.get(
            f"/document?id={value}"
        )

        assert status == 400

    status, payload, _ = alice.get(
        "/document?id=999"
    )

    assert status == 404
    assert payload == {
        "error": "Document not found"
    }


TESTS = [
    (
        "Unauthenticated request denied",
        unauthenticated_denied,
    ),
    (
        "Alice to Alice document allowed",
        alice_own_allowed,
    ),
    (
        "Alice to Bob document denied",
        alice_to_bob_denied,
    ),
    (
        "Denied update leaves data unchanged",
        denied_update_unchanged,
    ),
    (
        "Bob to Bob document allowed",
        bob_own_allowed,
    ),
    (
        "Non-admin operation denied",
        non_admin_operation_denied,
    ),
    (
        "Admin operation allowed",
        admin_operation_allowed,
    ),
    (
        "Client-supplied admin role ignored",
        client_role_ignored,
    ),
    (
        "Admin can access all documents",
        admin_all_documents,
    ),
    (
        "Alternative method rejected",
        alternative_method_rejected,
    ),
    (
        "Invalid and nonexistent IDs handled safely",
        invalid_and_missing_ids_safe,
    ),
]


def main():
    passed = 0

    for name, test in TESTS:
        try:
            test()
            print(f"[PASS] {name}")
            passed += 1

        except Exception as error:
            print(f"[FAIL] {name}: {error}")

    failed = len(TESTS) - passed

    print()
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
