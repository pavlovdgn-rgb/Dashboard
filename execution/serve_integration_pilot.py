"""Isolated loopback integration pilot; no writes to the Lead Generation database."""
import argparse
import json
import re
import sqlite3
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from serve_heatmap import connect, identifier, number

ROOT = Path(__file__).resolve().parents[1]
ADMIN_ORIGINS = {'http://127.0.0.1:5173', 'http://localhost:5173'}


def sdk_source():
    return '\n'.join((ROOT/'public'/name).read_text(encoding='utf-8') for name in
                     ('ux-lab-collector.js', 'ux-lab-sdk-bootstrap.js'))


def initialize(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.executescript('''
            CREATE TABLE IF NOT EXISTS pilot_connections (
                id TEXT PRIMARY KEY, study TEXT UNIQUE NOT NULL, name TEXT NOT NULL,
                kind TEXT NOT NULL, url TEXT NOT NULL, origin TEXT NOT NULL,
                client_id TEXT NOT NULL, enabled INTEGER NOT NULL DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS pilot_events (
                project TEXT NOT NULL, id TEXT NOT NULL, session TEXT NOT NULL, seq INTEGER NOT NULL,
                payload TEXT NOT NULL, PRIMARY KEY(project,id), UNIQUE(project,session,seq)
            );
        ''')


def url_origin(value):
    if not isinstance(value,str) or len(value)>4096:
        raise ValueError('Укажите адрес интерфейса')
    parsed=urlparse(value)
    if parsed.scheme not in ('http','https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Нужна ссылка http или https без пароля')
    host=parsed.hostname
    if ':' in host: host='['+host+']'
    port=parsed.port
    suffix=f':{port}' if port and port!={'http':80,'https':443}[parsed.scheme] else ''
    return f'{parsed.scheme}://{host}{suffix}'


def create_connection(db, data):
    if not isinstance(data,dict) or set(data)-{'name','kind','url','clientId'}:
        raise ValueError('Некорректное подключение')
    name=data.get('name','').strip()
    if not 1<=len(name)<=120: raise ValueError('Укажите название до 120 символов')
    kind=data.get('kind');url=data.get('url','');origin=url_origin(url)
    client=data.get('clientId','').strip()
    if kind not in ('web','figma'): raise ValueError('Выберите тип интерфейса')
    if kind=='figma':
        parsed=urlparse(url)
        if parsed.scheme!='https' or parsed.hostname not in ('figma.com','www.figma.com','embed.figma.com') or not re.match(r'^/proto/[a-zA-Z0-9]+(?:/|$)',parsed.path):
            raise ValueError('Нужна ссылка Figma из режима презентации: /proto/…')
        if client and not re.fullmatch(r'[a-zA-Z0-9_-]{1,120}',client): raise ValueError('Некорректный Client ID')
    elif client: raise ValueError('Client ID нужен только для Figma')
    project='connection-'+uuid.uuid4().hex;study='trial-'+uuid.uuid4().hex
    db.execute('INSERT INTO pilot_connections VALUES (?,?,?,?,?,?,?,1)',(project,study,name,kind,url,origin,client))
    return dict(db.execute('SELECT * FROM pilot_connections WHERE id=?',(project,)).fetchone())


def validate_event(event, connection):
    if not isinstance(event,dict): raise ValueError('Invalid event')
    common={'id','study','session','seq','version','timestamp','page'}
    for field in ('id','study','session','version','page'): identifier(event.get(field))
    if event['study']!=connection['study']: raise ValueError('Wrong study')
    number(event,'seq',1,1e9,True);number(event,'timestamp',0,1e14,True)
    if connection['kind']=='web':
        if event.get('kind')=='visit':
            if set(event)!=common|{'kind','vw','vh'}: raise ValueError('Invalid visit')
        else:
            if set(event)!=common|{'target','x','y','vw','vh','rw','rh','scroll_x','scroll_y'}: raise ValueError('Invalid click')
            identifier(event['target'])
            for key in ('x','y'): number(event,key,0,1)
            for key in ('rw','rh'): number(event,key,1,50000)
            for key in ('scroll_x','scroll_y'): number(event,key,-10000,100000)
        for key in ('vw','vh'): number(event,key,1,10000,True)
    else:
        if set(event)!=common|{'kind','data'}: raise ValueError('Invalid Figma event')
        kind=event['kind'];data=event['data']
        if not isinstance(data,dict): raise ValueError('Invalid Figma data')
        fields={
            'INITIAL_LOAD':set(), 'LOGIN_SCREEN_SHOWN':set(), 'PASSWORD_SCREEN_SHOWN':set(),
            'PRESENTED_NODE_CHANGED':{'node','history'},
            'NEW_STATE':{'node','before','after','timed'},
            'MOUSE_PRESS_OR_RELEASE':{'node','target','handled','x','y','scrollFrame','scrollX','scrollY','frameX','frameY'},
        }
        if kind not in fields or set(data)!=fields[kind]: raise ValueError('Unsupported Figma event')
        for key,value in data.items():
            if key in ('history','timed','handled'):
                if type(value) is not bool: raise ValueError('Invalid boolean')
            elif key in ('x','y','scrollX','scrollY','frameX','frameY'): number(data,key,-1000000,1000000)
            else: identifier(value)
    return json.dumps(event,sort_keys=True,separators=(',',':'),ensure_ascii=False)


def make_handler(path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass

        def reply(self,status,payload,mime='application/json; charset=utf-8'):
            body=(json.dumps(payload,ensure_ascii=False) if not isinstance(payload,str) else payload).encode('utf-8')
            self.send_response(status)
            origin=self.headers.get('Origin')
            if origin and self.permitted():
                self.send_header('Access-Control-Allow-Origin',origin)
                self.send_header('Vary','Origin')
            self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers','Content-Type')
            self.send_header('Content-Type',mime);self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.end_headers();self.wfile.write(body)

        def selected_connection(self):
            query=parse_qs(urlparse(self.path).query)
            project=identifier(query.get('project',[''])[0]);study=identifier(query.get('study',[''])[0])
            with connect(path) as db:
                row=db.execute('SELECT * FROM pilot_connections WHERE id=? AND study=?',(project,study)).fetchone()
            if not row: raise ValueError('Подключение или исследование не найдено')
            return dict(row)

        def permitted(self):
            route=urlparse(self.path).path;origin=self.headers.get('Origin')
            if route=='/sdk.js': return True
            if route in ('/api/events','/api/config'):
                try: row=self.selected_connection()
                except ValueError: return False
                return origin in ADMIN_ORIGINS if row['kind']=='figma' else origin==row['origin']
            # Management and result reads are accessible only from the local dashboard.
            return origin is None or origin in ADMIN_ORIGINS

        def do_OPTIONS(self): self.reply(204 if self.permitted() else 403, '')

        def do_GET(self):
            if not self.permitted(): return self.reply(403,{'error':'Origin is not allowed'})
            route=urlparse(self.path).path
            try:
                if route=='/sdk.js': return self.reply(200,sdk_source(),'application/javascript; charset=utf-8')
                if route=='/health': return self.reply(200,{'ok':True,'service':'integration-pilot'})
                if route=='/api/config':
                    row=self.selected_connection();return self.reply(200,{'kind':row['kind'],'enabled':bool(row['enabled'])})
                if route=='/api/connections':
                    with connect(path) as db:
                        rows=[dict(row) for row in db.execute('SELECT * FROM pilot_connections ORDER BY rowid DESC')]
                    return self.reply(200,{'connections':rows})
                if route=='/api/results':
                    project=identifier(parse_qs(urlparse(self.path).query).get('project',[''])[0])
                    with connect(path) as db:
                        events=[json.loads(row['payload']) for row in db.execute('SELECT payload FROM pilot_events WHERE project=? ORDER BY rowid DESC LIMIT 100',(project,))]
                        total=db.execute('SELECT COUNT(*) AS events,COUNT(DISTINCT session) AS sessions FROM pilot_events WHERE project=?',(project,)).fetchone()
                    return self.reply(200,{'events':events,'total':dict(total)})
                return self.reply(404,{'error':'Not found'})
            except (ValueError,TypeError): return self.reply(400,{'error':'Некорректный запрос'})
            except sqlite3.Error: return self.reply(503,{'error':'Хранилище недоступно'})

        def do_POST(self):
            if not self.permitted(): return self.reply(403,{'error':'Origin is not allowed'})
            route=urlparse(self.path).path
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=131072: return self.reply(413,{'error':'Request too large'})
                data=json.loads(self.rfile.read(size))
                with connect(path) as db:
                    if route=='/api/connections': result=create_connection(db,data)
                    elif route=='/api/policy':
                        if not isinstance(data,dict) or set(data)!={'project','enabled'} or type(data['enabled']) is not bool: raise ValueError('Некорректная настройка')
                        cursor=db.execute('UPDATE pilot_connections SET enabled=? WHERE id=?',(int(data['enabled']),identifier(data['project'])))
                        if not cursor.rowcount: raise ValueError('Подключение не найдено')
                        result={'ok':True}
                    elif route=='/api/events':
                        row=self.selected_connection()
                        if not isinstance(data,dict) or set(data)!={'events'} or not isinstance(data['events'],list) or not 1<=len(data['events'])<=50: raise ValueError('Invalid batch')
                        for event in data['events']:
                            payload=validate_event(event,row)
                            previous=db.execute('SELECT payload FROM pilot_events WHERE project=? AND (id=? OR (session=? AND seq=?))',(row['id'],event['id'],event['session'],event['seq'])).fetchone()
                            if previous and previous['payload']!=payload: raise ValueError('Conflicting identity')
                            if not row['enabled'] and not previous: raise ValueError('Collection paused')
                            db.execute('INSERT OR IGNORE INTO pilot_events VALUES (?,?,?,?,?)',(row['id'],event['id'],event['session'],event['seq'],payload))
                        result={'accepted':[event['id'] for event in data['events']]}
                    else: return self.reply(404,{'error':'Not found'})
                return self.reply(200,result)
            except (ValueError,TypeError,AttributeError,UnicodeDecodeError) as error: return self.reply(400,{'error':str(error)})
            except sqlite3.Error: return self.reply(503,{'error':'Хранилище недоступно'})
    return Handler


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=5176)
    parser.add_argument('--db',type=Path,default=ROOT/'.local/integration-pilot.sqlite3')
    args=parser.parse_args();initialize(args.db)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),make_handler(args.db))
    print(f'Integration pilot: http://127.0.0.1:{server.server_port}',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()


if __name__=='__main__': main()
