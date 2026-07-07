from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import html

HOST = "127.0.0.1"
PORT = 8001

USERS = {
    "student": "password123"
}

class Handler(BaseHTTPRequestHandler):
    def send_html(self, status_code, body):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/":
            body = """
            <html>
                <head><title>Tiny Backend App</title></head>
                <body>
                    <h1>Tiny Backend App</h1>

                    <h2>Search</h2>
                    <form method="GET" action="/search">
                        <input type="text" name="q" value="test">
                        <button type="submit">Search</button>
                    </form>

                    <h2>Login</h2>
                    <form method="POST" action="/login">
                        <input type="text" name="username" value="student">
                        <input type="password" name="password" value="password123">
                        <button type="submit">Login</button>
                    </form>
                </body>
            </html>
            """
            self.send_html(200, body)

        elif parsed.path == "/search":
            params = parse_qs(parsed.query)
            q = params.get("q", [""])[0]
            safe_q = html.escape(q)

            body = f"""
            <html>
                <body>
                    <h1>Search Results</h1>
                    <p>You searched for: {safe_q}</p>
                </body>
            </html>
            """
            self.send_html(200, body)

        else:
            self.send_html(404, "<h1>404 Not Found</h1>")

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/login":
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length).decode("utf-8")
            params = parse_qs(raw_body)

            username = params.get("username", [""])[0]
            password = params.get("password", [""])[0]

            if USERS.get(username) == password:
                self.send_html(200, "<h1>Login successful</h1>")
            else:
                self.send_html(401, "<h1>Login failed</h1>")
        else:
            self.send_html(404, "<h1>404 Not Found</h1>")

server = HTTPServer((HOST, PORT), Handler)
print(f"Serving on http://{HOST}:{PORT}")
server.serve_forever()
