from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import html

HOST = "127.0.0.1"
PORT = 8005

comments: list[str] = []


def parse_query(path: str) -> tuple[str, dict[str, list[str]]]:
    """Return the URL path and parsed query parameters."""
    parsed = urlparse(path)
    return parsed.path, parse_qs(parsed.query)


def render_home() -> str:
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>XSS Capstone</title>
</head>
<body>
    <h1>XSS Capstone</h1>

    <h2>Reflected XSS</h2>

    <form method="GET" action="/reflected-vuln">
        <label>Vulnerable search:</label>
        <input type="text" name="q" value="test">
        <button type="submit">Submit</button>
    </form>

    <form method="GET" action="/reflected-safe">
        <label>Safe search:</label>
        <input type="text" name="q" value="test">
        <button type="submit">Submit</button>
    </form>

    <h2>Stored XSS</h2>
    <p><a href="/comments">Open comments lab</a></p>

    <h2>DOM XSS</h2>
    <p><a href="/dom?name=student">Open DOM lab</a></p>
</body>
</html>
"""


def render_reflected(value: str, safe: bool) -> str:
    rendered_value = html.escape(value) if safe else value
    page_type = "Safe" if safe else "Vulnerable"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{page_type} Reflected XSS</title>
</head>
<body>
    <h1>{page_type} Reflected Search</h1>
    <p id="reflected-output">You searched for: {rendered_value}</p>
    <p><a href="/">Back home</a></p>
</body>
</html>
"""


def render_comments() -> str:
    vulnerable_items = "".join(
        f"<li>{comment}</li>"
        for comment in comments
    )

    safe_items = "".join(
        f"<li>{html.escape(comment)}</li>"
        for comment in comments
    )

    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Stored XSS Comments</title>
</head>
<body>
    <h1>Stored XSS Comments</h1>

    <h2>Add comment</h2>

    <form method="POST" action="/comments">
        <input type="text" name="comment" value="hello">
        <button type="submit">Submit</button>
    </form>

    <h2>Vulnerable comments</h2>
    <ul id="vulnerable-comments">
        {vulnerable_items}
    </ul>

    <h2>Safe comments</h2>
    <ul id="safe-comments">
        {safe_items}
    </ul>

    <p><a href="/">Back home</a></p>
</body>
</html>
"""


def render_dom() -> str:
    return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>DOM XSS Lab</title>
</head>
<body>
    <h1>DOM XSS Lab</h1>

    <h2>Vulnerable DOM sink</h2>
    <div id="vulnerable-output"></div>

    <h2>Safe DOM sink</h2>
    <div id="safe-output"></div>

    <p><a href="/">Back home</a></p>

    <script>
        const params = new URLSearchParams(window.location.search);
        const name = params.get("name") || "guest";

        document.getElementById("vulnerable-output").innerHTML =
            "Hello " + name;

        document.getElementById("safe-output").textContent =
            "Hello " + name;
    </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def send_html(
        self,
        status_code: int,
        body: str,
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        encoded_body = body.encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded_body)))

        if extra_headers:
            for header_name, header_value in extra_headers.items():
                self.send_header(header_name, header_value)

        self.end_headers()
        self.wfile.write(encoded_body)

    def do_GET(self) -> None:
        request_path, params = parse_query(self.path)

        if request_path == "/":
            self.send_html(200, render_home())

        elif request_path == "/reflected-vuln":
            value = params.get("q", [""])[0]
            self.send_html(
                200,
                render_reflected(value, safe=False),
            )

        elif request_path == "/reflected-safe":
            value = params.get("q", [""])[0]
            self.send_html(
                200,
                render_reflected(value, safe=True),
            )

        elif request_path == "/comments":
            self.send_html(200, render_comments())

        elif request_path == "/dom":
            self.send_html(200, render_dom())

        else:
            self.send_html(404, "<h1>404 Not Found</h1>")

    def do_POST(self) -> None:
        request_path, _ = parse_query(self.path)

        if request_path != "/comments":
            self.send_html(404, "<h1>404 Not Found</h1>")
            return

        try:
            content_length = int(
                self.headers.get("Content-Length", "0")
            )
        except ValueError:
            self.send_html(400, "<h1>400 Bad Request</h1>")
            return

        raw_body = self.rfile.read(content_length).decode(
            "utf-8",
            errors="replace",
        )

        params = parse_qs(raw_body)
        comment = params.get("comment", [""])[0]
        comments.append(comment)

        self.send_response(303)
        self.send_header("Location", "/comments")
        self.send_header("Content-Length", "0")
        self.end_headers()


def main() -> None:
    server = HTTPServer((HOST, PORT), Handler)
    print(f"Serving on http://{HOST}:{PORT}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
