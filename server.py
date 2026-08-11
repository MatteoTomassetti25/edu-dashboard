#!/usr/bin/env python3
"""Minimal HTTP server: serves static files + allows POST to update data.json and config.json."""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json, os, sys

PORT      = int(os.environ.get('PORT', 8800))
DATA_DIR  = os.environ.get('DATA_DIR', '.')  # dir where writable files live; use a bind-mounted DIR (not a single file) so os.replace works
WRITABLE  = {'data.json', 'config.json'}

def data_path(name): return os.path.join(DATA_DIR, name)

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        name = self.path.split('?')[0].lstrip('/')
        if name in WRITABLE:
            try:
                with open(data_path(name), 'rb') as f:
                    body = f.read()
            except FileNotFoundError:
                self.send_response(404); self.end_headers(); return
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.split('?')[0].endswith('.html'):
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.end_headers()
            with open(self.translate_path(self.path), 'rb') as f:
                self.wfile.write(f.read())
            return
        super().do_GET()

    def do_POST(self):
        name = self.path.lstrip('/')
        if name not in WRITABLE:
            self.send_response(403); self.end_headers(); return
        try:
            n    = int(self.headers.get('Content-Length', 0))
            data = json.loads(self.rfile.read(n))
            target = data_path(name)
            tmp    = target + '.tmp'
            with open(tmp, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, target)  # atomic; requires DATA_DIR to be a dir (bind a directory, not the file)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":true}')
        except Exception as e:
            self.send_response(500); self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, fmt, *args):
        if os.environ.get('LOG'):
            super().log_message(fmt, *args)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for f in ('config.json', 'data.json'):
    if not os.path.exists(data_path(f)):
        print(f'⚠  {f} not found in {DATA_DIR} — copy {f.replace(".json",".example.json")} → {f} and edit it.')
        sys.exit(1)

print(f'→ http://localhost:{PORT}  (DATA_DIR={os.path.abspath(DATA_DIR)})')
HTTPServer(('0.0.0.0', PORT), Handler).serve_forever()
