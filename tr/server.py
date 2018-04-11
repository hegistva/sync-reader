
import http.server
import socketserver
import os

from tr.libs.utils import config

PORT = 8000

os.chdir(config.LIBRARY)

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()