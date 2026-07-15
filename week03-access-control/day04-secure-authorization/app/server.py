from __future__ import annotations

from http.cookies import CookieError, SimpleCookie
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
import secrets

from authorization import Action, is_authorized

HOST, PORT = "127.0.0.1", 8011

USERS = {
    "alice": {"id": 1, "display_name": "Alice", "role": "user"},
    "bob": {"id": 2, "display_name": "Bob", "role": "user"},
    "admin": {
        "id": 3,
        "display_name": "Administrator",
        "role": "admin",
    },
}

DOCUMENTS = {
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

SESSIONS: dict[str, str] = {}

GET_ROUTES = {
    "/documents",
    "/document",
}

POST_ROUTES = {
    "/demo-login",
    "/logout",
    "/document/update",
    "/admin/users/role",
}

ALLOWED = {
    **{path: "GET" for path in GET_ROUTES},
    **{path: "POST" for path in POST_ROUTES},
}


def path_and_params(raw_path: str):
    parsed = urlparse(raw_path)
    parameters = parse_qs(
        parsed.query,
        keep_blank_values=True,
    )
    return parsed.path, parameters


def parse_id(raw_id: str | None) -> int:
    if raw_id is None or raw_id == "":
        raise ValueError("Document ID is required")

    if not raw_id.isdecimal() or int(raw_id) <= 0:
        raise ValueError(
            "Document ID must be a positive integer"
        )

    return int(raw_id)


def cookie_token(
    cookie_header: str | None,
) -> str | None:
    if not cookie_header:
        return None

    cookies = SimpleCookie()

    try:
        cookies.load(cookie_header)
    except CookieError:
        return None

    cookie = cookies.get("session")

    if cookie is None or cookie.value == "":
        return None

    return cookie.value


class Handler(BaseHTTPRequestHandler):
    def reply(
        self,
        status,
        payload=None,
        headers=None,
    ):
        body = (
            b""
            if payload is None
            else json.dumps(
                payload,
                separators=(",", ":"),
            ).encode()
        )

        self.send_response(status)

        if payload is not None:
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8",
            )

        self.send_header(
            "Content-Length",
            str(len(body)),
        )

        for name, value in (headers or {}).items():
            self.send_header(name, value)

        self.end_headers()

        if body:
            self.wfile.write(body)

    def form(self):
        try:
            length = int(
                self.headers.get(
                    "Content-Length",
                    "0",
                )
            )
        except ValueError as error:
            raise ValueError(
                "Invalid Content-Length"
            ) from error

        if length < 0:
            raise ValueError(
                "Content-Length cannot be negative"
            )

        raw_body = self.rfile.read(length).decode(
            "utf-8",
            errors="replace",
        )

        return parse_qs(
            raw_body,
            keep_blank_values=True,
        )

    def actor(self):
        token = cookie_token(
            self.headers.get("Cookie")
        )

        username = (
            SESSIONS.get(token)
            if token
            else None
        )

        user = (
            USERS.get(username)
            if username
            else None
        )

        if user is None:
            return None

        return {
            "username": username,
            **user,
        }

    def require_actor(self):
        actor = self.actor()

        if actor is None:
            self.reply(
                401,
                {"error": "Authentication required"},
            )

        return actor

    def get_document(
        self,
        actor,
        raw_id,
        action,
    ):
        try:
            document_id = parse_id(raw_id)
        except ValueError as error:
            self.reply(
                400,
                {"error": str(error)},
            )
            return None

        document = DOCUMENTS.get(document_id)

        if (
            document is None
            or not is_authorized(
                actor,
                action,
                document,
            )
        ):
            self.reply(
                404,
                {"error": "Document not found"},
            )
            return None

        return document

    def method_denied(self, path):
        self.reply(
            405,
            {"error": "Method not allowed"},
            {"Allow": ALLOWED[path]},
        )

    def do_GET(self):
        path, parameters = path_and_params(
            self.path
        )

        if path in POST_ROUTES:
            self.method_denied(path)
            return

        if path not in GET_ROUTES:
            self.reply(
                404,
                {"error": "Route not found"},
            )
            return

        actor = self.require_actor()

        if actor is None:
            return

        if path == "/documents":
            if not is_authorized(
                actor,
                Action.LIST_DOCUMENTS,
            ):
                self.reply(
                    403,
                    {"error": "Forbidden"},
                )
                return

            visible_documents = [
                document.copy()
                for document in DOCUMENTS.values()
                if is_authorized(
                    actor,
                    Action.READ_DOCUMENT,
                    document,
                )
            ]

            visible_documents.sort(
                key=lambda document: document["id"]
            )

            self.reply(
                200,
                {
                    "user": actor["username"],
                    "documents": visible_documents,
                },
            )
            return

        document = self.get_document(
            actor,
            parameters.get("id", [None])[0],
            Action.READ_DOCUMENT,
        )

        if document is not None:
            self.reply(
                200,
                {"document": document.copy()},
            )

    def do_POST(self):
        path, _ = path_and_params(self.path)

        if path in GET_ROUTES:
            self.method_denied(path)
            return

        if path not in POST_ROUTES:
            self.reply(
                404,
                {"error": "Route not found"},
            )
            return

        try:
            form = self.form()
        except ValueError as error:
            self.reply(
                400,
                {"error": str(error)},
            )
            return

        if path == "/demo-login":
            username = form.get(
                "username",
                [""],
            )[0].strip().lower()

            if username not in USERS:
                self.reply(
                    400,
                    {"error": "Unknown demo user"},
                )
                return

            token = secrets.token_urlsafe(24)
            SESSIONS[token] = username

            self.reply(
                200,
                {
                    "message": "Demo login successful",
                    "user": username,
                    "role": USERS[username]["role"],
                },
                {
                    "Set-Cookie": (
                        f"session={token}; "
                        "Path=/; "
                        "HttpOnly; "
                        "SameSite=Lax"
                    )
                },
            )
            return

        if path == "/logout":
            token = cookie_token(
                self.headers.get("Cookie")
            )

            if token:
                SESSIONS.pop(token, None)

            self.reply(
                204,
                headers={
                    "Set-Cookie": (
                        "session=; "
                        "Path=/; "
                        "Max-Age=0; "
                        "HttpOnly; "
                        "SameSite=Lax"
                    )
                },
            )
            return

        actor = self.require_actor()

        if actor is None:
            return

        if path == "/document/update":
            document = self.get_document(
                actor,
                form.get("id", [None])[0],
                Action.UPDATE_DOCUMENT,
            )

            if document is None:
                return

            if "content" not in form:
                self.reply(
                    400,
                    {"error": "Content is required"},
                )
                return

            document["content"] = form["content"][0]

            self.reply(
                200,
                {
                    "message": "Document updated",
                    "document": document.copy(),
                },
            )
            return

        if not is_authorized(
            actor,
            Action.CHANGE_USER_ROLE,
        ):
            self.reply(
                403,
                {"error": "Forbidden"},
            )
            return

        username = form.get(
            "username",
            [""],
        )[0].strip().lower()

        role = form.get(
            "role",
            [""],
        )[0].strip().lower()

        if username not in USERS:
            self.reply(
                404,
                {"error": "User not found"},
            )
            return

        if role not in {"user", "admin"}:
            self.reply(
                400,
                {"error": "Invalid role"},
            )
            return

        USERS[username]["role"] = role

        self.reply(
            200,
            {
                "message": "User role updated",
                "user": {
                    "username": username,
                    "role": role,
                },
            },
        )

    def alternative_method(self):
        path, _ = path_and_params(self.path)

        if path in ALLOWED:
            self.method_denied(path)
        else:
            self.reply(
                404,
                {"error": "Route not found"},
            )

    do_PUT = alternative_method
    do_PATCH = alternative_method
    do_DELETE = alternative_method


def main():
    server = HTTPServer(
        (HOST, PORT),
        Handler,
    )

    print(
        "Serving secure authorization lab on "
        f"http://{HOST}:{PORT}"
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
