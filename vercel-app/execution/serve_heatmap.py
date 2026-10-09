"""Loopback-only click ingestion and SQLite query service for the local UX-Lab trial."""
import argparse
import hashlib
import json
import math
import re
import sqlite3
import shutil
import subprocess
import tempfile
import threading
import zipfile
import io
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
import live_project
import session_video

ROOT = Path(__file__).resolve().parents[1]
ID = re.compile(r"^[a-zA-Z0-9_.:-]{1,120}$")
PAGES = {"product", "cart", "checkout", "success"}
LEED_ROUTES = {'index':'/', 'showcase':'/showcase', 'leads-table':'/leads-table', 'leads-kanban':'/leads-kanban',
    'dashboard':'/dashboard', 'lead-card':'/lead-card', 'chat-panel':'/chat-panel', 'chat-widget':'/chat-widget',
    'call-log-modal':'/call-log-modal', 'incoming-call-popup':'/incoming-call-popup',
    'user-roles-settings':'/settings/roles', 'auto-assignment-settings':'/settings/auto-assignment',
    'telephony-settings':'/settings/telephony', 'chat-widget-settings':'/settings/chat-widget',
    'access-denied':'/access-denied', 'error-state':'/error', 'not-found-404':'/not-found',
    'empty-leads-table':'/leads-table/empty', 'loading-state':'/leads-table/loading',
    'empty-leads-kanban':'/leads-kanban/empty', 'empty-dashboard':'/dashboard/empty',
    'loading-dashboard':'/dashboard/loading', 'empty-user-roles-settings':'/settings/roles/empty',
    'loading-user-roles-settings':'/settings/roles/loading'}
PAGES.update('leed-'+name for name in LEED_ROUTES)
MOBILE_PATHS = ('main','events','filter','event','sessions','seats','seats/confirm','seats/selected',
    'order-form','order-form/filled','payment','done','profile','profile/data','tickets','refund',
    'refund/done','orders','ticket','no-ticket','plan','plan/add','map','map/route','story',
    'gallery','reviews','review','activity','person','venue','favourites')
MOBILE_ROUTES = {path.replace('/','--'):'/'+path for path in MOBILE_PATHS}
PAGES.update('bb-'+name for name in MOBILE_ROUTES)
MAX_BODY = 131072
MAX_SNAPSHOT = 4 * 1024 * 1024
EXPORT_LOCK = threading.Lock()


@contextmanager
def connect(path):
    db = sqlite3.connect(path, timeout=10)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()


def initialize(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.execute("PRAGMA journal_mode=WAL")
        db.executescript('''
            CREATE TABLE IF NOT EXISTS snapshots (
                id TEXT PRIMARY KEY, html TEXT NOT NULL, width INTEGER NOT NULL, height INTEGER NOT NULL
            );
            CREATE TABLE IF NOT EXISTS clicks (
                id TEXT PRIMARY KEY, study TEXT NOT NULL, session TEXT NOT NULL,
                seq INTEGER NOT NULL, page TEXT NOT NULL, version TEXT NOT NULL,
                layout TEXT NOT NULL, target TEXT NOT NULL, x REAL NOT NULL, y REAL NOT NULL,
                vw INTEGER NOT NULL, vh INTEGER NOT NULL, rw REAL NOT NULL, rh REAL NOT NULL,
                scroll_x REAL NOT NULL, scroll_y REAL NOT NULL, timestamp INTEGER NOT NULL,
                received TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(study,session,seq)
            );
            CREATE INDEX IF NOT EXISTS clicks_study_layout ON clicks(study,layout);
        ''')
        if 'context' not in {row['name'] for row in db.execute('PRAGMA table_info(clicks)')}:
            db.execute("ALTER TABLE clicks ADD COLUMN context TEXT NOT NULL DEFAULT ''")
        live_project.initialize(db)
        session_video.initialize(db)


def identifier(value):
    if not isinstance(value, str) or not ID.fullmatch(value):
        raise ValueError("Invalid identifier")
    return value


def number(data, key, minimum, maximum, integer=False):
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"Invalid {key}")
    if not minimum <= value <= maximum or (integer and int(value) != value):
        raise ValueError(f"Out of range: {key}")
    return int(value) if integer else round(value, 5)


def validate(event):
    if not isinstance(event, dict):
        raise ValueError("Invalid event")
    keys = {'id','study','session','seq','page','version','target','x','y','vw','vh','rw','rh','scroll_x','scroll_y','timestamp'}
    if set(event) not in (keys, keys | {'context'}):
        raise ValueError("Unexpected or missing fields")
    data = {key:identifier(event.get(key)) for key in ('id','study','session','version','target')}
    if event.get('page') not in PAGES:
        raise ValueError("Unknown page")
    data['page'] = event['page']
    context = event.get('context')
    data['context'] = ''
    if data['page'].startswith(('leed-','bb-')) and context is None:
        raise ValueError('Viewport context is required')
    if context is not None:
        if not isinstance(context,dict) or not {'signature','scrolls'} <= set(context) or set(context)-{'signature','scrolls','snapshot','element'}:
            raise ValueError('Invalid viewport context')
        if 'element' in context:
            element=context['element']
            if not isinstance(element,dict) or set(element)!={'label','rect'}:
                raise ValueError('Invalid element')
            if not isinstance(element['label'],str) or not 1<=len(element['label'])<=120 or any(ord(c)<32 for c in element['label']):
                raise ValueError('Invalid element label')
            if not isinstance(element['rect'],list) or len(element['rect'])!=4:
                raise ValueError('Invalid element bounds')
            for value in element['rect']: number({'rect':value},'rect',0,1)
        if 'snapshot' in context:
            identifier(context['snapshot'])
        if not isinstance(context['signature'],str) or not re.fullmatch(r'[a-f0-9]{16}',context['signature']):
            raise ValueError('Invalid signature')
        if not isinstance(context['scrolls'],list) or len(context['scrolls'])>100:
            raise ValueError('Invalid scrolls')
        for scroll in context['scrolls']:
            if not isinstance(scroll,list) or len(scroll)!=3:
                raise ValueError('Invalid scroll')
            for index,value in enumerate(scroll):
                number({'scroll':value},'scroll',-1 if index==0 else -10000,100000,True)
        data['context'] = json.dumps(context,sort_keys=True,separators=(',',':'))
    for key, low, high, integer in [('seq',1,1e9,True),('x',0,1,False),('y',0,1,False),
            ('vw',240,10000,True),('vh',200,10000,True),('rw',1,10000,False),('rh',1,50000,False),
            ('scroll_x',-10000,100000,False),('scroll_y',-10000,100000,False),('timestamp',0,1e14,True)]:
        data[key] = number(event,key,low,high,integer)
    layout = [data[key] for key in ('page','version','vw','vh','rw','rh')]
    if context is not None:
        layout.append(data['context'])
    data['layout'] = hashlib.sha256(json.dumps(layout).encode()).hexdigest()[:24]
    return data


def page_groups(db, study, session=''):
    """Aggregate viewport click density by screen, not volatile DOM/snapshot fingerprints."""
    where='study=?'+(' AND session=?' if session else '')
    args=(study,session) if session else (study,)
    rows=db.execute('SELECT * FROM clicks WHERE '+where+' ORDER BY timestamp DESC,seq DESC',args).fetchall()
    grouped={}
    ready={row['id'] for row in db.execute('SELECT id FROM snapshots')}
    for row in rows:
        if row['page'].startswith(('leed-','bb-')):
            key='page-'+hashlib.sha256(json.dumps([row['page'],row['vw'],row['vh']]).encode()).hexdigest()[:20]
        else:
            key=row['layout']
        grouped.setdefault(key,[]).append(row)
    result=[]
    members={}
    for key, items in grouped.items():
        # Prefer the most frequently observed background that actually reached storage.
        backgrounds={}
        for row in items:
            context=json.loads(row['context']) if row['context'] else None
            snapshot=context.get('snapshot') if context else None
            if snapshot in ready:
                if snapshot not in backgrounds:
                    html=db.execute('SELECT html FROM snapshots WHERE id=?',(snapshot,)).fetchone()['html']
                    body=html.split('</head>',1)[-1]
                    overlays=len(re.findall(r'position:\s*fixed',body))
                    backgrounds[snapshot]={'count':0,'row':row,'overlays':overlays}
                candidate=backgrounds[snapshot]
                candidate['count']+=1
        chosen=min(backgrounds.values(),key=lambda item:(item['overlays'],-item['count']))['row'] if backgrounds else items[0]
        group={field:chosen[field] for field in ('page','version','vw','vh','rw','rh')}
        group.update(layout=key,context=json.loads(chosen['context']) if chosen['context'] else None,
            clicks=len(items),sessions=len({row['session'] for row in items}),aggregation='page')
        if group['page'].startswith('leed-'):
            group['path']=LEED_ROUTES[group['page'][5:]]
        elif group['page'].startswith('bb-'):
            group['path']=MOBILE_ROUTES[group['page'][3:]]
            if not backgrounds:
                group['context']={'signature':'0000000000000000','scrolls':[]}
            else:
                group['backgroundResponsive']=True # Legacy IDs omitted viewport but preserve the same HTML/CSS.
        result.append(group)
        members[key]={row['layout'] for row in items}
    return result,members


def make_handler(db_path):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass  # Never log event payloads or form data.

        def allowed(self):
            origin = self.headers.get('Origin')
            if not origin:
                return True
            parsed = urlparse(origin)
            return parsed.scheme == 'http' and parsed.hostname in ('localhost','127.0.0.1') and parsed.port in (5173,5175,6006)

        def reply(self, status, payload, mime='application/json; charset=utf-8', headers=None):
            body = payload if isinstance(payload,bytes) else payload.encode() if isinstance(payload,str) else json.dumps(payload,ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            origin = self.headers.get('Origin')
            if origin and self.allowed():
                self.send_header('Access-Control-Allow-Origin',origin)
                self.send_header('Vary','Origin')
            self.send_header('Content-Type',mime)
            for key,value in (headers or {}).items():self.send_header(key,value)
            if mime in ('image/png','application/zip'):
                self.send_header('Content-Disposition','attachment; filename="heatmap.'+('png' if mime=='image/png' else 'zip')+'"')
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Length',str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_OPTIONS(self):
            if not self.allowed():
                return self.reply(403,{'error':'Origin is not allowed'})
            self.send_response(204)
            self.send_header('Access-Control-Allow-Origin',self.headers.get('Origin','http://127.0.0.1:5173'))
            self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers','Content-Type')
            self.end_headers()

        def do_POST(self):
            if not self.allowed():
                return self.reply(403,{'error':'Origin is not allowed'})
            request_path = urlparse(self.path).path
            if self.path.startswith('/api/recordings/'):
                try:
                    path=urlparse(self.path);query=parse_qs(path.query)
                    length=int(self.headers.get('Content-Length','0'))
                    limit=session_video.MAX_CHUNK if path.path.endswith('/chunk') else MAX_BODY
                    if not 0<length<=limit:return self.reply(413,{'error':'Recording request too large'})
                    body=self.rfile.read(length)
                    with connect(db_path) as db:
                        if path.path=='/api/recordings/start':result=session_video.start(db,json.loads(body),identifier)
                        elif path.path=='/api/recordings/chunk':result=session_video.chunk(db,identifier(query.get('id',[''])[0]),int(query.get('seq',['-1'])[0]),body)
                        elif path.path=='/api/recordings/finish':result=session_video.finish(db,json.loads(body),identifier)
                        else:return self.reply(404,{'error':'Not found'})
                    return self.reply(200,result)
                except (ValueError,TypeError,UnicodeDecodeError):return self.reply(400,{'error':'Invalid recording request'})
                except sqlite3.Error:return self.reply(503,{'error':'Storage unavailable'})
            if self.path.startswith('/api/project/'):
                try:
                    length=int(self.headers.get('Content-Length','0'))
                    if not 0<length<=MAX_BODY:raise ValueError('Invalid request size')
                    data=json.loads(self.rfile.read(length))
                    path=urlparse(self.path);query=parse_qs(path.query)
                    with connect(db_path) as db: result=live_project.post(db,path.path,data,identifier,PAGES,identifier(query.get('study',[live_project.STUDY])[0]))
                    return self.reply(200,result) if result is not None else self.reply(404,{'error':'Not found'})
                except (ValueError,TypeError,UnicodeDecodeError):return self.reply(400,{'error':'Invalid project request'})
                except sqlite3.Error:return self.reply(503,{'error':'Storage unavailable'})
            if request_path == '/api/heatmap/snapshots':
                try:
                    length=int(self.headers.get('Content-Length','0'))
                    if not 0<length<=MAX_SNAPSHOT:
                        return self.reply(413,{'error':'Snapshot too large or empty'})
                    data=json.loads(self.rfile.read(length))
                    if not isinstance(data,dict) or set(data)!={'id','html','width','height'}:
                        raise ValueError('Invalid snapshot')
                    identifier(data['id'])
                    if not isinstance(data['html'],str) or not data['html'].startswith('<!doctype html>'):
                        raise ValueError('Invalid snapshot HTML')
                    number(data,'width',240,10000,True);number(data,'height',200,10000,True)
                    with connect(db_path) as db:
                        previous=db.execute('SELECT * FROM snapshots WHERE id=?',(data['id'],)).fetchone()
                        # v2 IDs were based on HTML only. Identical HTML can reflow at another viewport;
                        # acknowledge such legacy retries so they do not poison an upload queue.
                        legacy_same_html=previous and data['id'].startswith('s-') and previous['html']==data['html']
                        if previous and not legacy_same_html and any(previous[key]!=value for key,value in data.items()):
                            raise ValueError('Conflicting snapshot ID')
                        db.execute('INSERT OR IGNORE INTO snapshots (id,html,width,height) VALUES (?,?,?,?)',
                            (data['id'],data['html'],data['width'],data['height']))
                    return self.reply(200,{'accepted':data['id']})
                except (ValueError,TypeError,UnicodeDecodeError):
                    return self.reply(400,{'error':'Invalid snapshot'})
                except sqlite3.Error:
                    return self.reply(503,{'error':'Storage unavailable'})
            if request_path != '/api/heatmap/events':
                return self.reply(404,{'error':'Not found'})
            try:
                length = int(self.headers.get('Content-Length','0'))
                if length <= 0 or length > MAX_BODY:
                    return self.reply(413,{'error':'Batch too large or empty'})
                batch = json.loads(self.rfile.read(length))
                if not isinstance(batch,dict) or set(batch) != {'events'} or not isinstance(batch['events'],list) or not 1 <= len(batch['events']) <= 100:
                    raise ValueError('Invalid batch')
                events = [validate(event) for event in batch['events']]
                with connect(db_path) as db:
                    closed={study:live_project.round_closed(db,study) for study in {event['study'] for event in events}}
                    for event in events:
                        if closed[event['study']]:continue # Acknowledge stale queued events without changing fixed statistics.
                        if not live_project.page_allowed(db,event['study'],event['page'],PAGES):raise ValueError('Page belongs to another project')
                        if not live_project.collection_enabled(db,event['study'],'click'):continue
                        previous = db.execute('SELECT * FROM clicks WHERE id=? OR (study=? AND session=? AND seq=?)',
                            (event['id'],event['study'],event['session'],event['seq'])).fetchone()
                        if previous and any(previous[key] != value for key,value in event.items()):
                            raise ValueError('Conflicting event identity')
                        db.execute('INSERT OR IGNORE INTO clicks ('+','.join(event)+') VALUES ('+','.join('?' for _ in event)+')',tuple(event.values()))
                return self.reply(200,{'accepted':[event['id'] for event in events]})
            except (ValueError,TypeError,UnicodeDecodeError):
                return self.reply(400,{'error':'Invalid click batch'})
            except sqlite3.Error:
                return self.reply(503,{'error':'Storage unavailable; retry later'})

        def do_GET(self):
            if not self.allowed():
                return self.reply(403,{'error':'Origin is not allowed'})
            path = urlparse(self.path)
            if path.path in ('/api/recordings','/api/recordings/media'):
                try:
                    query=parse_qs(path.query)
                    with connect(db_path) as db:
                        study=identifier(query.get('study',[live_project.STUDY])[0])
                        live_project.settings(db,study)
                        if path.path=='/api/recordings':return self.reply(200,session_video.metadata(db,identifier(query.get('session',[''])[0]),study))
                        status,headers,body=session_video.media(db,identifier(query.get('id',[''])[0]),self.headers.get('Range'),study)
                    mime=headers.pop('Content-Type','application/octet-stream')
                    if query.get('download')==['1']:headers['Content-Disposition']='attachment; filename="test-recording.webm"'
                    return self.reply(status,body,mime,headers)
                except (ValueError,TypeError):return self.reply(400,{'error':'Invalid recording query'})
                except sqlite3.Error:return self.reply(503,{'error':'Storage unavailable'})
            if path.path.startswith('/api/project'):
                try:
                    if path.path=='/api/project/report-pdf':
                        query=parse_qs(path.query)
                        with connect(db_path) as db:
                            report=live_project.get(db,'/api/project/report',query,identifier)
                        with EXPORT_LOCK: body=live_project.project_reports.render_pdf(report,{})
                        return self.reply(200,body,'application/pdf',{'Content-Disposition':'attachment; filename="ux-lab-report-'+report['id']+'.pdf"'})
                    with connect(db_path) as db: result=live_project.get(db,path.path,parse_qs(path.query),identifier)
                    return self.reply(200,result) if result is not None else self.reply(404,{'error':'Not found'})
                except (ValueError,TypeError):return self.reply(400,{'error':'Invalid project query'})
                except sqlite3.Error:return self.reply(503,{'error':'Storage unavailable'})
            if path.path == '/api/heatmap/export':
                try:
                    query=parse_qs(path.query)
                    study=identifier(query.get('study',[''])[0])
                    session=query.get('session',[''])[0]
                    if session:identifier(session)
                    group=query.get('group',[''])[0]
                    target=query.get('target',[''])[0]
                    if group: identifier(group)
                    if target: identifier(target)
                    mode=query.get('mode',['all'])[0]
                    fmt=query.get('format',['png'])[0]
                    layer=query.get('layer',['1'])[0]
                    if mode not in ('all','first') or fmt not in ('png','zip') or layer not in ('0','1') or (fmt=='png' and not group):
                        raise ValueError('Invalid export')
                    with connect(db_path) as db:
                        groups,_=page_groups(db,study,session)
                    if not any(item['page'].startswith('leed-') and (not group or item['layout']==group) for item in groups):
                        return self.reply(404,{'error':'No maps to export'})
                except (ValueError,sqlite3.Error):
                    return self.reply(400,{'error':'Invalid export request'})
                if not EXPORT_LOCK.acquire(blocking=False):
                    return self.reply(409,{'error':'Another export is running'})
                try:
                    node=shutil.which('node') or str(Path('C:/Program Files/nodejs/node.exe'))
                    with tempfile.TemporaryDirectory(prefix='ux-heatmap-') as output:
                        config={'study':study,'session':session,'group':group,'target':target,'mode':mode,'layer':layer=='1',
                            'output':output,'port':self.server.server_port}
                        subprocess.run([node,str(ROOT/'execution/export_heatmaps.mjs')],input=json.dumps(config),
                            text=True,encoding='utf-8',capture_output=True,check=True,timeout=180,cwd=ROOT,
                            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
                        files=sorted(Path(output).glob('*.png'))
                        if not files: raise RuntimeError('No screenshots rendered')
                        if fmt=='png':
                            payload=files[0].read_bytes()
                        else:
                            buffer=io.BytesIO()
                            with zipfile.ZipFile(buffer,'w',zipfile.ZIP_DEFLATED) as archive:
                                for file in files: archive.write(file,file.name)
                            payload=buffer.getvalue()
                    return self.reply(200,payload,'image/png' if fmt=='png' else 'application/zip')
                except (OSError,subprocess.SubprocessError,RuntimeError):
                    return self.reply(503,{'error':'Export failed. Check that UX-Lab and Lead Generation are running.'})
                finally:
                    EXPORT_LOCK.release()
            if path.path == '/health':
                return self.reply(200,{'ok':True})
            if path.path == '/sdk.js':
                source='\n'.join((ROOT/'public'/name).read_text(encoding='utf-8') for name in ('ux-lab-collector.js','ux-lab-sdk-bootstrap.js'))
                return self.reply(200,source,'application/javascript; charset=utf-8')
            if path.path == '/collector.js':
                return self.reply(200,(ROOT/'public/ux-lab-collector.js').read_text(encoding='utf-8'),'application/javascript; charset=utf-8')
            if path.path == '/api/heatmap/snapshots':
                try:
                    snapshot_id=identifier(parse_qs(path.query).get('id',[''])[0])
                    with connect(db_path) as db:
                        row=db.execute('SELECT * FROM snapshots WHERE id=?',(snapshot_id,)).fetchone()
                    return self.reply(200,dict(row)) if row else self.reply(404,{'error':'Background not received yet'})
                except (ValueError,sqlite3.Error):
                    return self.reply(400,{'error':'Invalid snapshot query'})
            if path.path != '/api/heatmap':
                return self.reply(404,{'error':'Not found'})
            query = parse_qs(path.query)
            try:
                study = identifier(query.get('study',[''])[0])
                session=query.get('session',[''])[0]
                if session:identifier(session)
                where='study=?'+(' AND session=?' if session else '')
                args=(study,session) if session else (study,)
                group = query.get('group',[''])[0]
                mode = query.get('mode',['all'])[0]
                aggregation=query.get('aggregation',['layout'])[0]
                if aggregation not in ('layout','page'):
                    raise ValueError('Invalid aggregation')
                if mode not in ('all','first'):
                    raise ValueError('Invalid mode')
                with connect(db_path) as db:
                    members={}
                    groups = [dict(row) for row in db.execute('''SELECT layout,page,version,vw,vh,rw,rh,context,COUNT(*) clicks,
                        COUNT(DISTINCT session) sessions FROM clicks WHERE '''+where+' GROUP BY layout ORDER BY MAX(received) DESC, layout',args)]
                    for group_info in groups:
                        group_info['context'] = json.loads(group_info['context']) if group_info['context'] else None
                        if group_info['page'].startswith('leed-'):
                            group_info['path'] = LEED_ROUTES[group_info['page'][5:]]
                    if aggregation=='page':
                        groups,members=page_groups(db,study,session)
                    total = dict(db.execute('SELECT COUNT(*) clicks,COUNT(DISTINCT session) sessions FROM clicks WHERE '+where,args).fetchone())
                    available_sessions=[dict(row) for row in db.execute('''SELECT session id,MIN(timestamp) startedAt,SUM(click) clicks FROM
                        (SELECT session,timestamp,1 click FROM clicks WHERE study=? UNION ALL SELECT session,timestamp,0 click FROM visits WHERE study=?)
                        GROUP BY session ORDER BY startedAt DESC,session''',(study,study))]
                    points = []
                    selected_sessions = []
                    if group:
                        identifier(group)
                        # Rank BEFORE filtering layout: resizing never creates another first click.
                        layouts=sorted(members.get(group,[])) if aggregation=='page' else [group]
                        placeholders=','.join('?' for _ in layouts) or 'NULL'
                        partition='study,session,page' if aggregation=='page' else 'study,session,page,version'
                        cte = 'WITH ranked AS (SELECT *,ROW_NUMBER() OVER (PARTITION BY '+partition+' ORDER BY seq) n FROM clicks WHERE '+where+') SELECT * FROM ranked WHERE layout IN ('+placeholders+')'+(' AND n=1' if mode=='first' else '')
                        rows = db.execute(cte,(*args,*layouts)).fetchall()
                        # Aggregate coordinates to 1/1000 of the surface, never fabricate sample points.
                        bins = {}
                        for row in rows:
                            element=(json.loads(row['context']) if row['context'] else {}).get('element')
                            key = (round(row['x'],3),round(row['y'],3),row['target'],json.dumps(element,sort_keys=True))
                            entry = bins.setdefault(key,{'x':key[0],'y':key[1],'target':key[2],'count':0,'sessions':set()})
                            if element: entry['element']=element
                            entry['count'] += 1
                            entry['sessions'].add(row['session'])
                        points = [{**entry,'sessions':sorted(entry['sessions'])} for entry in bins.values()]
                        selected_sessions = sorted({row['session'] for row in rows})
                return self.reply(200,{'groups':groups,'total':total,'points':points,'sessions':selected_sessions,'availableSessions':available_sessions})
            except (ValueError,sqlite3.Error):
                return self.reply(400,{'error':'Invalid query'})
    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port',type=int,default=5174)
    parser.add_argument('--db',type=Path,default=ROOT/'.local/heatmap.sqlite3')
    args = parser.parse_args()
    initialize(args.db)
    print(f'UX-Lab click API: http://127.0.0.1:{args.port} | SQLite: {args.db}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),make_handler(args.db)).serve_forever()
