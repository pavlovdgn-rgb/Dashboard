"""Serve the built cloud edition and real API locally against an explicitly supplied test DB."""
import importlib.util
import mimetypes
import os
from pathlib import Path
from urllib.parse import unquote, urlparse
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cloud_api', ROOT / 'api/index.py')
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class Preview(api.handler):
    def do_GET(self):
        path = unquote(urlparse(self.path).path)
        if path.startswith('/api/') or path in ('/sdk.js', '/health'):
            return super().do_GET()
        root = (ROOT / 'dist').resolve()
        file = (root / path.lstrip('/')).resolve()
        if not file.is_relative_to(root):
            return self.reply(403, b'Forbidden')
        if not file.is_file():
            file = root / ('participant/index.html' if path.startswith('/participant/') else 'index.html')
        return self.reply(200, file.read_bytes(), mimetypes.guess_type(str(file))[0] or 'application/octet-stream')


if __name__ == '__main__':
    if not os.environ.get('UXLAB_TEST_DB'):
        raise SystemExit('Set UXLAB_TEST_DB to an isolated test database path.')
    port = int(os.environ.get('UXLAB_TEST_PORT', '5184'))
    print(f'Cloud edition test preview: http://127.0.0.1:{port}', flush=True)
    ThreadingHTTPServer(('127.0.0.1', port), Preview).serve_forever()
