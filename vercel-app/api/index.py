"""One Vercel Python Function serving the existing research API with cloud persistence."""
import hashlib
import hmac
import json
import os
import sys
import threading
import time
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'execution'))
import cloud_db
import cloud_video
import serve_heatmap
import session_video

serve_heatmap.connect = cloud_db.connect
session_video.MAX_CHUNK = cloud_video.MAX_CHUNK
session_video.chunk = cloud_video.chunk
session_video.finish = cloud_video.finish
session_video.media = cloud_video.media
_migrated = False
_lock = threading.Lock()


def password():
    return os.environ.get('UXLAB_ACCESS_PASSWORD', '')


def signature(value):
    return hmac.new(password().encode(), value.encode(), hashlib.sha256).hexdigest()


def signed_in(headers):
    if len(password()) < 12:
        return False
    try:
        cookie = SimpleCookie(headers.get('Cookie', ''))
        expires, digest = cookie['uxlab_session'].value.split('.')
        return time.time() < int(expires) <= time.time() + 8 * 86400 and hmac.compare_digest(digest, signature(expires))
    except (KeyError, ValueError):
        return False


class handler(serve_heatmap.make_handler(None)):
    def route(self):
        parsed = urlparse(self.path)
        pairs = parse_qsl(parsed.query, keep_blank_values=True)
        destination = next((value for key, value in pairs if key == '__path'), '')
        path = parsed.path
        if parsed.path == '/api/index.py' and (destination.startswith('/api/') or destination in ('/sdk.js', '/health')):
            path = destination
        # Vercel may retain the public URL while adding the rewrite's query.
        # Strip routing metadata for both URL forms, keeping the actual filters.
        query = urlencode([(key, value) for key, value in pairs if key != '__path'])
        self.path = path + ('?' + query if query else '')

    def allowed(self):
        origin = self.headers.get('Origin')
        if not origin:
            return True
        # Host is supplied by Vercel, not an Origin reflected back without checking.
        scheme = 'https' if os.environ.get('VERCEL') else 'http'
        own = f"{scheme}://{self.headers.get('Host', '')}"
        additional = set(filter(None, os.environ.get('UXLAB_ALLOWED_ORIGINS', '').split(',')))
        return origin == own or origin in additional

    def reply(self, status, payload, mime='application/json; charset=utf-8', headers=None):
        def public_links(value):
            if isinstance(value, dict):
                result = {key: public_links(item) for key, item in value.items()}
                if isinstance(result.get('url'), str) and result['url'].startswith('/participant/'):
                    scheme = 'https' if os.environ.get('VERCEL') else 'http'
                    result['url'] = f"{scheme}://{self.headers.get('Host', '')}{result['url']}"
                return result
            if isinstance(value, list):
                return [public_links(item) for item in value]
            return value
        payload = public_links(payload)
        extra = {'Cache-Control': 'no-store', **(headers or {})}
        return super().reply(status, payload, mime, extra)

    def authorized(self):
        if not self.allowed():
            self.reply(403, {'error': 'Этот адрес интерфейса не разрешён.'})
            return False
        if len(password()) < 12:
            self.reply(503, {'error': 'В настройках Vercel задайте UXLAB_ACCESS_PASSWORD длиной от 12 символов и выполните Redeploy.'})
            return False
        if not signed_in(self.headers):
            self.reply(401, {'error': 'Войдите в рабочее пространство.'})
            return False
        return True

    def ready(self):
        global _migrated
        if not cloud_db.configured() and not (os.environ.get('UXLAB_TEST_DB') and not os.environ.get('VERCEL')):
            self.reply(503, {'error': 'Подключите базу Turso: задайте TURSO_DATABASE_URL и TURSO_AUTH_TOKEN в Vercel и выполните Redeploy.'})
            return False
        if not _migrated:
            with _lock:
                if not _migrated:
                    cloud_db.migrate()
                    _migrated = True
        return True

    def do_GET(self):
        self.route()
        path = urlparse(self.path).path
        if path in ('/health', '/api/health'):
            return self.reply(200, {'ok': True, 'service': 'ux-lab', 'storageConfigured': cloud_db.configured()})
        if path == '/api/auth':
            if len(password()) < 12:
                return self.reply(503, {'error': 'В Vercel задайте UXLAB_ACCESS_PASSWORD длиной от 12 символов и выполните Redeploy.'})
            return self.reply(200 if signed_in(self.headers) else 401, {'authenticated': signed_in(self.headers)})
        if not self.authorized():
            return
        if path == '/api/heatmap/export':
            return self.reply(410, {'error': 'В облачной версии выгрузка карт выполняется кнопкой «Скачать» в браузере.'})
        try:
            if self.ready():
                return super().do_GET()
        except Exception:
            return self.reply(503, {'error': 'Не удалось обратиться к облачному хранилищу. Проверьте подключение Turso и повторите запрос.'})

    def do_POST(self):
        self.route()
        if not self.allowed():
            return self.reply(403, {'error': 'Origin is not allowed'})
        if urlparse(self.path).path == '/api/auth':
            try:
                length = int(self.headers.get('Content-Length', 0))
                if not 0 < length <= 2048 or len(password()) < 12:
                    return self.reply(503, {'error': 'Пароль рабочего пространства ещё не настроен.'})
                data = json.loads(self.rfile.read(length))
                if not isinstance(data, dict) or not isinstance(data.get('password'), str) or not hmac.compare_digest(data['password'].encode(), password().encode()):
                    return self.reply(401, {'error': 'Неверный пароль.'})
                expires = str(int(time.time()) + 7 * 86400)
                secure = '; Secure' if os.environ.get('VERCEL') else ''
                cookie = f'uxlab_session={expires}.{signature(expires)}; Path=/; Max-Age=604800; HttpOnly; SameSite=Lax{secure}'
                return self.reply(200, {'authenticated': True}, headers={'Set-Cookie': cookie})
            except (ValueError, TypeError):
                return self.reply(400, {'error': 'Некорректный запрос.'})
        if not self.authorized():
            return
        try:
            if self.ready():
                return super().do_POST()
        except Exception:
            return self.reply(503, {'error': 'Не удалось сохранить данные в облачном хранилище. Повторите отправку.'})

    def do_OPTIONS(self):
        if not self.allowed():
            return self.reply(403, {'error': 'Origin is not allowed'})
        return self.reply(204, b'', headers={'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type, Range'})


if __name__ == '__main__':
    from http.server import ThreadingHTTPServer
    ThreadingHTTPServer(('127.0.0.1', 5184), handler).serve_forever()
