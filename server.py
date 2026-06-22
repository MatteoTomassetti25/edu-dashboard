#!/usr/bin/env python3
"""Minimal HTTP server: serves static files + allows POST to update data.json and config.json."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, os, sys

PORT      = int(os.environ.get('PORT', 8800))
WRITABLE  = {'data.json', 'config.json'}

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.split('?')[0].endswith('.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            path = self.translate_path(self.path)
            with open(path, 'rb') as f:
                self.wfile.write(f.read())
        else:
            super().do_GET()

    def do_POST(self):
        filename = self.path.lstrip('/')
        if filename not in WRITABLE:
            self.send_response(403); self.end_headers(); return
        try:
            n    = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(n))
            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(500); self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, fmt, *args):
        pass  # ponytail: silent — set LOG=1 to enable
        if os.environ.get('LOG'):
            super().log_message(fmt, *args)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if not os.path.exists('config.json'):
    print('⚠  config.json not found — copy config.example.json → config.json and edit it.')
    sys.exit(1)
if not os.path.exists('data.json'):
    print('⚠  data.json not found — copy data.example.json → data.json and edit it.')
    sys.exit(1)

print(f'→ http://localhost:{PORT}')
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
