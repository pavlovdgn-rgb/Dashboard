"""Reproducible independent HTML site for the SDK trial; binds only to loopback."""
import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).resolve().parents[1]


def demo_html(api, project):
    return (ROOT/'assets/integration-demo/index.html').read_text(encoding='utf-8').replace('__API__',api).replace('__PROJECT__',project)


def make_handler(html):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def do_GET(self):
            body=html.encode('utf-8');self.send_response(200)
            self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(body)))
            self.end_headers();self.wfile.write(body)
    return Handler


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=5177)
    parser.add_argument('--api',default='http://127.0.0.1:5176');args=parser.parse_args()
    url=f'http://127.0.0.1:{args.port}/'
    with urlopen(args.api+'/api/connections',timeout=5) as response:connections=json.load(response)['connections']
    connection=next((row for row in connections if row['url']==url and row['kind']=='web'),None)
    if connection is None:
        body=json.dumps({'name':'Проверка SDK · отдельный сайт','kind':'web','url':url}).encode()
        with urlopen(Request(args.api+'/api/connections',data=body,headers={'Content-Type':'application/json'}),timeout=5) as response:connection=json.load(response)
    html=demo_html(args.api,connection['id'])
    output=ROOT/'.tmp/integration-demo';output.mkdir(parents=True,exist_ok=True)
    (output/'index.html').write_text(html,encoding='utf-8')
    (output/'connection.json').write_text(json.dumps(connection,ensure_ascii=False,indent=2),encoding='utf-8')
    print(url+'?ux_study='+connection['study'],flush=True)
    server=ThreadingHTTPServer(('127.0.0.1',args.port),make_handler(html))
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()


if __name__=='__main__':main()
