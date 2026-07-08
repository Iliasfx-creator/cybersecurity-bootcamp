from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import html

HOST = "127.0.0.1"
PORT = 8002

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
                <head><title>Reflected XSS Lab</title></head>
                <body>
                    <h1>Reflected XSS Lab</h1>

                    <h2>Vulnerable Search</h2>
                    <form method="GET" action="/vuln-search">
                        <input type="text" name="q" value="test">
                        <button type="submit">Search vulnerable</button>
                    </form>

                    <h2>Safe Search</h2>
                    <form method="GET" action="/safe-search">
                        <input type="text" name="q" value="test">
                        <button type="submit">Search safe</button>
                    </form>
                </body>
            </html>
            """
            self.send_html(200, body)

        elif parsed.path == "/vuln-search":
            params = parse_qs(parsed.query)
            q = params.get("q", [""])[0]

            body = f"""
            <html>
                <body>
                    <h1>Vulnerable Search Results</h1>
                    <p>You searched for: {q}</p>
                </body>
            </html>
            """
            self.send_html(200, body)

        elif parsed.path == "/safe-search":
            params = parse_qs(parsed.query)
            q = params.get("q", [""])[0]
            safe_q = html.escape(q)

            body = f"""
            <html>
                <body>
                    <h1>Safe Search Results</h1>
                    <p>You searched for: {safe_q}</p>
                </body>
            </html>
            """
            self.send_html(200, body)

        else:
            self.send_html(404, "<h1>404 Not Found</h1>")

server = HTTPServer((HOST, PORT), Handler)
print(f"Serving on http://{HOST}:{PORT}")
server.serve_forever()
