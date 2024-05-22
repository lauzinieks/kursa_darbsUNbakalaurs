import http.server
import socketserver

PORT = 8000  # You can change this port if needed

# Replace with the actual path to your df-messenger.js file
SCRIPT_PATH = "extension2\df-messenger.js"

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/df-messenger.js":
            with open(SCRIPT_PATH, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", "text/javascript")
                self.end_headers()
                self.wfile.write(f.read())
        else:
            super().do_GET()

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving Dialogflow Messenger script on port {PORT}")
    httpd.serve_forever()