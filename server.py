import http.server, socketserver, os

class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Connection', 'close')
        super().end_headers()
    def log_message(self, *a): pass

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with socketserver.TCPServer(('127.0.0.1', 4202), Handler) as httpd:
    httpd.serve_forever()
