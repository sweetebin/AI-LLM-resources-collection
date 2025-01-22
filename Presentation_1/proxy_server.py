from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve agent_demo.html when root path is requested
        if path == '/' or path == '/index.html':
            return SimpleHTTPRequestHandler.translate_path(self, '/agent_demo.html')
        return SimpleHTTPRequestHandler.translate_path(self, path)

    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

def run_server(port=8080):
    while True:
        try:
            server_address = ('', port)
            httpd = HTTPServer(server_address, CORSRequestHandler)
            print(f"Server running on http://localhost:{port}")
            httpd.serve_forever()
        except OSError as e:
            if e.errno == 98:  # Address already in use
                print(f"Port {port} is already in use, trying port {port + 1}")
                port += 1
            else:
                raise e

if __name__ == '__main__':
    run_server()
