"""Session filtering must cover backgrounds, counts, first clicks and export, not just the UI."""
import os
import subprocess
import unittest
from pathlib import Path
from check_heatmap_api import HeatmapApiTests

class SessionFilterTests(HeatmapApiTests):
    def seed(self):
        events=[]
        for seq,session,page,vw in [(1,'person-a','leed-leads-table',1280),(2,'person-a','leed-leads-table',1280),(3,'person-a','leed-leads-table',1440),(1,'person-b','leed-leads-table',1280),(2,'person-b','leed-dashboard',1280)]:
            event={**self.event(seq),'id':f'{session}-{seq}','study':'leed-local','session':session,'page':page,'vw':vw,'timestamp':1000*seq,'context':{'signature':'1234567890abcdef','scrolls':[]}}
            events.append(event)
        self.assertEqual(self.request('/api/heatmap/events',{'events':events})[0],200)
        self.assertEqual(self.request('/api/project/visit',{'id':'empty-visit','study':'leed-local','session':'empty','page':'leed-leads-table','timestamp':5000,'vw':1280,'vh':900,'context':{'signature':'1234567890abcdef','scrolls':[]}})[0],200)

    def test_no_cross_session_leakage(self):
        self.seed();base='/api/heatmap?study=leed-local&aggregation=page'
        all_data=self.request(base)[1];data=self.request(base+'&session=person-a')[1]
        self.assertEqual(all_data['total'],{'clicks':5,'sessions':2})
        self.assertEqual(data['total'],{'clicks':3,'sessions':1})
        self.assertEqual({g['page'] for g in data['groups']},{'leed-leads-table'})
        self.assertEqual(len(data['availableSessions']),3)
        for group in data['groups']:
            detail=self.request(base+'&session=person-a&group='+group['layout'])[1]
            self.assertEqual(sum(point['count'] for point in detail['points']),2 if group['vw']==1280 else 1)
            self.assertEqual(detail['sessions'],['person-a'])
            first=self.request(base+'&session=person-a&mode=first&group='+group['layout'])[1]
            self.assertEqual(sum(point['count'] for point in first['points']),1 if group['vw']==1280 else 0)
        empty=self.request(base+'&session=empty')[1]
        self.assertEqual(empty['groups'],[]);self.assertEqual(empty['total']['clicks'],0)
        self.assertEqual(self.request(base+'&session=bad%20id')[0],400)
        excluded=next(g['layout'] for g in all_data['groups'] if g['page']=='leed-dashboard')
        self.assertEqual(self.request('/api/heatmap/export?study=leed-local&session=person-a&format=png&group='+excluded)[0],404)

    def test_browser_filter(self):
        self.seed()
        subprocess.run(['C:/Program Files/nodejs/node.exe','execution/check_heatmap_sessions.mjs'],cwd=Path(__file__).resolve().parents[1],env={**os.environ,'LIVE_TEST_API':self.url},check=True,timeout=120)

if __name__=='__main__':unittest.main(defaultTest='SessionFilterTests')
