"""Isolated API checks; never delete the real local click database."""
import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from http.server import ThreadingHTTPServer
from serve_heatmap import initialize, make_handler


class HeatmapApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name)/'clicks.sqlite3'
        initialize(self.db)
        self.server = ThreadingHTTPServer(('127.0.0.1',0),make_handler(self.db))
        self.thread = threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.url = f'http://127.0.0.1:{self.server.server_port}'

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.temp.cleanup()

    def request(self,path,payload=None,origin='http://127.0.0.1:5173'):
        request = Request(self.url+path,data=json.dumps(payload).encode() if payload is not None else None,
            headers={'Content-Type':'application/json','Origin':origin})
        try:
            with urlopen(request,timeout=5) as response:
                return response.status,json.load(response)
        except HTTPError as error:
            return error.code,json.load(error)

    def event(self,seq=1,**values):
        return dict(id=f'event-{seq}',study='test',session='session-1',seq=seq,page='product',version='nova-local-v1',
            target='backpack',x=.2,y=.3,vw=1280,vh=900,rw=1088,rh=400,scroll_x=0,scroll_y=200,timestamp=1000,**values)

    def test_dedup_atomic_validation_and_persistence(self):
        event=self.event()
        self.assertEqual(self.request('/api/heatmap/events',{'events':[event]})[0],200)
        self.assertEqual(self.request('/api/heatmap/events',{'events':[event]})[0],200)
        # Conflicting retry IDs must not overwrite an already accepted event.
        self.assertEqual(self.request('/api/heatmap/events',{'events':[{**event,'x':.5}]})[0],400)
        self.assertEqual(self.request('/api/heatmap/events',{'events':[self.event(2),{**self.event(3),'email':'private@example.test'}]})[0],400)
        initialize(self.db)  # Restart initialization preserves the database.
        self.assertEqual(self.request('/api/heatmap?study=test')[1]['total'],{'clicks':1,'sessions':1})
        self.assertEqual(self.request('/api/heatmap?study=other')[1]['total']['clicks'],0)

    def test_first_click_before_layout_filter(self):
        events=[self.event(),{**self.event(2),'vw':390,'rw':326},self.event(3)]
        # Arrival order must not affect first-click attribution.
        self.assertEqual(self.request('/api/heatmap/events',{'events':list(reversed(events))})[0],200)
        groups=self.request('/api/heatmap?study=test')[1]['groups']
        for group in groups:
            data=self.request('/api/heatmap?study=test&mode=first&group='+group['layout'])[1]
            self.assertEqual(sum(point['count'] for point in data['points']),1 if group['vw']==1280 else 0)

    def test_origin_and_bounds(self):
        self.assertEqual(self.request('/api/heatmap?study=test',origin='https://example.com')[0],403)
        for value in [-.1,1.1,'0.3',True,None]:
            self.assertEqual(self.request('/api/heatmap/events',{'events':[{**self.event(),'x':value}]})[0],400)
        self.assertEqual(self.request('/api/heatmap/events',{'events':[]})[0],400)
        self.assertEqual(self.request('/api/heatmap/events',{'events':[self.event()]*101})[0],400)

    def test_leed_context_and_origin(self):
        context={'signature':'1234567890abcdef','scrolls':[[12,0,240]]}
        event={**self.event(), 'page':'leed-leads-table','version':'leed-local-v1','context':context}
        self.assertEqual(self.request('/api/heatmap/events',{'events':[event]},origin='http://127.0.0.1:5175')[0],200)
        groups=self.request('/api/heatmap?study=test')[1]['groups']
        self.assertEqual(groups[0]['context'],context)
        self.assertEqual(groups[0]['path'],'/leads-table')
        changed={**event,'id':'event-2','seq':2,'context':{**context,'scrolls':[[12,0,400]]}}
        self.assertEqual(self.request('/api/heatmap/events',{'events':[changed]})[0],200)
        self.assertEqual(len(self.request('/api/heatmap?study=test')[1]['groups']),2)
        for invalid in [{**context,'html':'private'},{**context,'signature':'secret'}, {**context,'scrolls':[[12,0,'private']]}]:
            self.assertEqual(self.request('/api/heatmap/events',{'events':[{**event,'context':invalid}]})[0],400)

    def test_snapshots_are_idempotent_and_persist(self):
        snapshot={'id':'s-test','html':'<!doctype html><html><body>Static background</body></html>','width':1280,'height':900}
        self.assertEqual(self.request('/api/heatmap/snapshots',snapshot)[0],200)
        self.assertEqual(self.request('/api/heatmap/snapshots',snapshot)[0],200)
        self.assertEqual(self.request('/api/heatmap/snapshots',{**snapshot,'html':'<!doctype html>different'})[0],400)
        initialize(self.db)
        self.assertEqual(self.request('/api/heatmap/snapshots?id=s-test')[1],snapshot)
        self.assertEqual(self.request('/api/heatmap/snapshots?id=missing')[0],404)
        self.assertEqual(self.request('/api/heatmap/snapshots',snapshot,origin='https://example.com')[0],403)

    def test_one_density_map_per_screen_and_viewport(self):
        base={**self.event(),'page':'leed-leads-table','version':'leed-local-v2','context':{'signature':'1234567890abcdef','scrolls':[]}}
        events=[{**base,'id':f'click-{n}','seq':n,'context':{**base['context'],'signature':f'{n:016x}'}} for n in range(1,12)]
        events.append({**base,'id':'kanban','seq':12,'page':'leed-leads-kanban'})
        self.assertEqual(self.request('/api/heatmap/events',{'events':events})[0],200)
        data=self.request('/api/heatmap?study=test&aggregation=page')[1]
        self.assertEqual(len(data['groups']),2)
        group=next(g for g in data['groups'] if g['page']=='leed-leads-table')
        self.assertEqual(group['clicks'],11)
        query='/api/heatmap?study=test&aggregation=page&group='+group['layout']
        self.assertEqual(sum(p['count'] for p in self.request(query)[1]['points']),11)
        self.assertEqual(sum(p['count'] for p in self.request(query+'&mode=first')[1]['points']),1)
        self.assertEqual(data['total']['clicks'],12)

    def test_element_names_and_bounds_survive_aggregation(self):
        info={'label':'Кнопка «Новый лид»','rect':[.1,.2,.15,.08]}
        event={**self.event(),'page':'leed-leads-table','context':{'signature':'1234567890abcdef','scrolls':[],'element':info}}
        self.assertEqual(self.request('/api/heatmap/events',{'events':[event]})[0],200)
        group=self.request('/api/heatmap?study=test&aggregation=page')[1]['groups'][0]['layout']
        points=self.request('/api/heatmap?study=test&aggregation=page&group='+group)[1]['points']
        self.assertEqual(points[0]['element'],info)
        invalid={**event,'id':'invalid','seq':2,'context':{**event['context'],'element':{**info,'rect':[0,0,2,1]}}}
        self.assertEqual(self.request('/api/heatmap/events',{'events':[invalid]})[0],400)

    def test_legacy_background_retry_does_not_block_new_viewport(self):
        snapshot={'id':'s-legacy','html':'<!doctype html><body>Same responsive DOM</body>','width':1440,'height':900}
        self.assertEqual(self.request('/api/heatmap/snapshots',snapshot)[0],200)
        self.assertEqual(self.request('/api/heatmap/snapshots',{**snapshot,'width':2327,'height':1194})[0],200)
        self.assertEqual(self.request('/api/heatmap/snapshots',{**snapshot,'id':'s2-new','width':2327,'height':1194})[0],200)


if __name__=='__main__':
    unittest.main()
