from __future__ import annotations

from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import secrets

HOST = "127.0.0.1"
PORT = 8010


USERS = {
    "alice": {
        "id": 1,
        "display_name": "Alice",
    },
    "bob": {
        "id": 2,
        "display_name": "Bob",
    },
}


INITIAL_DOCUMENTS = {
    101: {
        "id": 101,
        "owner": "alice",
        "title": "Alice private notes",
        "content": "Alice document 101",
    },
    102: {
        "id": 102,
        "owner": "alice",
        "title": "Alice project plan",
        "content": "Alice document 102",
    },
    201: {
        "id": 201,
        "owner": "bob",
        "title": "Bob private notes",
        "content": "Bob document 201",
    },
    202: {
        "id": 202,
        "owner": "bob",
        "title": "Bob project plan",
        "content": "Bob document 202",
    },
}


DOCUMENTS = {
    document_id: document.copy()
    for document_id, document in INITIAL_DOCUMENTS.items()
}


SESSIONS: dict[str, str] = {}


def reset_documents() -> None:
    DOCUMENTS.clear()

    for document_id, document in INITIAL_DOCUMENTS.items():
        DOCUMENTS[document_id] = document.copy()


def parse_request_path(
    raw_path: str,
) -> tuple[str, dict[str, list[str]]]:
    parsed = urlparse(raw_path)

    parameters = parse_qs(
        parsed.query,
        keep_blank_values=True,
    )

    return parsed.path, parameters


def parse_document_id(raw_value: str | None) -> int:
    if raw_value is None or raw_value == "":
        raise ValueError("Document ID is required")

    if not raw_value.isdecimal():
        raise ValueError("Document ID must be a positive integer")

    document_id = int(raw_value)

    if document_id <= 0:
        raise ValueError("Document ID must be greater than zero")

    return document_id


def encode_json(payload: dict | list) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def parse_form_body(
    raw_body: bytes,
) -> dict[str, list[str]]:
    decoded_body = raw_body.decode(
        "utf-8",
        errors="replace",
    )

    return parse_qs(
        decoded_body,
        keep_blank_values=True,
    )


def create_demo_session(username: str) -> str:
    if username not in USERS:
        raise ValueError("Unknown demo user")

    token = secrets.token_urlsafe(24)
    SESSIONS[token] = username
    return token


def destroy_session(token: str | None) -> None:
    if token is not None:
        SESSIONS.pop(token, None)


def parse_session_token(
    cookie_header: str | None,
) -> str | None:
    if not cookie_header:
        return None

    cookies = SimpleCookie()

    try:
        cookies.load(cookie_header)
    except CookieError:
        return None

    session_cookie = cookies.get("session")

    if session_cookie is None:
        return None

    token = session_cookie.value

    if token == "":
        return None

    return token


def user_owns_document(
    username: str,
    document: dict,
) -> bool:
    return document["owner"] == username


class Handler(BaseHTTPRequestHandler):
    def send_json(
        self,
        status_code: int,
        payload: dict | list | None,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        if payload is None:
            encoded_body = b""
        else:
            encoded_body = encode_json(payload)

        self.send_response(status_code)

        if payload is not None:
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8",
            )

        self.send_header(
            "Content-Length",
            str(len(encoded_body)),
        )

        if extra_headers:
            for header_name, header_value in extra_headers.items():
                self.send_header(
                    header_name,
                    header_value,
                )

        self.end_headers()

        if encoded_body:
            self.wfile.write(encoded_body)

    def read_form(self) -> dict[str, list[str]]:
        raw_content_length = self.headers.get(
            "Content-Length",
            "0",
        )

        try:
            content_length = int(raw_content_length)
        except ValueError as error:
            raise ValueError(
                "Invalid Content-Length"
            ) from error

        if content_length < 0:
            raise ValueError(
                "Content-Length cannot be negative"
            )

        raw_body = self.rfile.read(content_length)

        return parse_form_body(raw_body)


    def get_session_token(self) -> str | None:
        cookie_header = self.headers.get("Cookie")
        return parse_session_token(cookie_header)

    def get_current_user(self) -> str | None:
        token = self.get_session_token()

        if token is None:
            return None

        return SESSIONS.get(token)

    def require_authenticated_user(self) -> str | None:
        username = self.get_current_user()

        if username is None:
            self.send_json(
                401,
                {"error": "Authentication required"},
            )
            return None

        return username

    def handle_demo_login(self) -> None:
        try:
            form = self.read_form()
        except ValueError as error:
            self.send_json(
                400,
                {"error": str(error)},
            )
            return

        username = form.get(
            "username",
            [""],
        )[0].strip().lower()

        if username not in USERS:
            self.send_json(
                400,
                {"error": "Unknown demo user"},
            )
            return

        token = create_demo_session(username)

        self.send_json(
            200,
            {
                "message": "Demo login successful",
                "user": username,
            },
            {
                "Set-Cookie": (
                    f"session={token}; "
                    "Path=/; "
                    "HttpOnly; "
                    "SameSite=Lax"
                ),
            },
        )

    def handle_logout(self) -> None:
        token = self.get_session_token()
        destroy_session(token)

        self.send_json(
            204,
            None,
            {
                "Set-Cookie": (
                    "session=; "
                    "Path=/; "
                    "Max-Age=0; "
                    "HttpOnly; "
                    "SameSite=Lax"
                ),
            },
        )

    def handle_documents(self) -> None:
        username = self.require_authenticated_user()

        if username is None:
            return

        owned_documents = [
            document.copy()
            for document in DOCUMENTS.values()
            if document["owner"] == username
        ]

        owned_documents.sort(
            key=lambda document: document["id"]
        )

        self.send_json(
            200,
            {
                "user": username,
                "documents": owned_documents,
            },
        )

    def handle_document_read(
        self,
        parameters: dict[str, list[str]],
        enforce_ownership: bool,
    ) -> None:
        username = self.require_authenticated_user()

        if username is None:
            return

        raw_document_id = parameters.get(
            "id",
            [None],
        )[0]

        try:
            document_id = parse_document_id(
                raw_document_id
            )
        except ValueError as error:
            self.send_json(
                400,
                {"error": str(error)},
            )
            return

        document = DOCUMENTS.get(document_id)

        if document is None:
            self.send_json(
                404,
                {"error": "Document not found"},
            )
            return

        if (
            enforce_ownership
            and not user_owns_document(
                username,
                document,
            )
        ):
            self.send_json(
                404,
                {"error": "Document not found"},
            )
            return

        self.send_json(
            200,
            {
                "document": document.copy(),
            },
        )

    def do_GET(self) -> None:
        request_path, parameters = parse_request_path(
            self.path
        )

        if request_path == "/documents":
            self.handle_documents()
            return

        if request_path == "/vuln/document":
            self.handle_document_read(
                parameters,
                enforce_ownership=False,
            )
            return

        if request_path == "/safe/document":
            self.handle_document_read(
                parameters,
                enforce_ownership=True,
            )
            return

        self.send_json(
            404,
            {"error": "Route not found"},
        )

    def handle_document_update(
        self,
        enforce_ownership: bool,
    ) -> None:
        username = self.require_authenticated_user()

        if username is None:
            return

        try:
            form = self.read_form()
        except ValueError as error:
            self.send_json(
                400,
                {"error": str(error)},
            )
            return

        raw_document_id = form.get(
            "id",
            [None],
        )[0]

        try:
            document_id = parse_document_id(
                raw_document_id
            )
        except ValueError as error:
            self.send_json(
                400,
                {"error": str(error)},
            )
            return

        content_values = form.get("content")

        if content_values is None:
            self.send_json(
                400,
                {"error": "Content is required"},
            )
            return

        new_content = content_values[0]

        document = DOCUMENTS.get(document_id)

        if document is None:
            self.send_json(
                404,
                {"error": "Document not found"},
            )
            return

        if (
            enforce_ownership
            and not user_owns_document(
                username,
                document,
            )
        ):
            self.send_json(
                404,
                {"error": "Document not found"},
            )
            return

        document["content"] = new_content

        self.send_json(
            200,
            {
                "message": "Document updated",
                "document": document.copy(),
            },
        )

    def do_POST(self) -> None:
        request_path, _ = parse_request_path(self.path)

        if request_path == "/demo-login":
            self.handle_demo_login()
            return

        if request_path == "/logout":
            self.handle_logout()
            return

        if request_path == "/vuln/document/update":
            self.handle_document_update(
                enforce_ownership=False,
            )
            return

        if request_path == "/safe/document/update":
            self.handle_document_update(
                enforce_ownership=True,
            )
            return

        self.send_json(
            404,
            {"error": "Route not found"},
        )


def main() -> None:
    server = HTTPServer(
        (HOST, PORT),
        Handler,
    )

    print(
        f"Serving IDOR lab on http://{HOST}:{PORT}"
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
