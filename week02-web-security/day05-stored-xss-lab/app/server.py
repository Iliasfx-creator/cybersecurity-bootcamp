from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import html

HOST = "127.0.0.1"
PORT = 8003

comments = []

class Handler(BaseHTTPRequestHandler):
    def send_html(self, status_code, body):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def render_page(self):
        vulnerable_comments = ""
        safe_comments = ""

        for comment in comments:
            vulnerable_comments += f"<li>{comment}</li>"
            safe_comments += f"<li>{html.escape(comment)}</li>"

        body = f"""
        <html>
            <head>
                <title>Stored XSS Lab</title>
            </head>
            <body>
                <h1>Stored XSS Lab</h1>

                <h2>Add Comment</h2>
                <form method="POST" action="/comment">
                    <input type="text" name="comment" value="hello">
                    <button type="submit">Submit</button>
                </form>

                <h2>Vulnerable Comments</h2>
                <ul>
                    {vulnerable_comments}
                </ul>

                <h2>Safe Comments</h2>
                <ul>
                    {safe_comments}
                </ul>
            </body>
        </html>
        """
        self.send_html(200, body)

    def do_GET(self):
        if self.path == "/":
            self.render_page()
        else:
            self.send_html(404, "<h1>404 Not Found</h1>")

    def do_POST(self):
        if self.path == "/comment":
            length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(length).decode("utf-8")
            params = parse_qs(raw_body)

            comment = params.get("comment", [""])[0]
            comments.append(comment)

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()
        else:
            self.send_html(404, "<h1>404 Not Found</h1>")

server = HTTPServer((HOST, PORT), Handler)
print(f"Serving on http://{HOST}:{PORT}")
server.serve_forever()
