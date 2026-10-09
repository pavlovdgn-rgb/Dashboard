import { useEffect, useState } from 'react';
import { type Device } from '../data/research';
import { screenRegistry, type ScreenId } from './registry';

export type WireRoute={screen:ScreenId;study:string;device:Device;scenario:string;coverage:'all'|'partial';reportId:string;item:string;participant:string;heatmapSession:string;time:number;link:string;control:boolean;clean:boolean};
function readRoute():WireRoute {
  const [path,query='']=location.hash.replace(/^#\/?/,'').split('?');
  const params=new URLSearchParams(query);
  return {screen:Object.hasOwn(screenRegistry,path)?path as ScreenId:'overview',study:params.get('study')||'biletberu-mobile',device:params.get('device')==='mobile'?'mobile':params.get('device')==='desktop'?'desktop':'all',
    scenario:params.get('scenario')||'',coverage:params.get('coverage')==='partial'?'partial':'all',reportId:params.get('report')||'',item:params.get('item')||'',participant:params.get('participant')||'014',heatmapSession:params.get('session')||'',time:Math.max(0,Number(params.get('time'))||0),link:params.get('link')||'',control:params.get('control')==='true',clean:params.get('clean')==='true'};
}
function routeHash(route:WireRoute) {
  const params=new URLSearchParams({device:route.device});
  if(route.study!=='biletberu-mobile')params.set('study',route.study);
  if(route.scenario)params.set('scenario',route.scenario);
  if(route.coverage==='partial')params.set('coverage','partial');
  if(route.reportId)params.set('report',route.reportId);
  if(route.item)params.set('item',route.item);
  if(route.participant!=='014')params.set('participant',route.participant);
  if(route.heatmapSession)params.set('session',route.heatmapSession);
  if(route.time)params.set('time',String(route.time));
  if(route.link)params.set('link',route.link);
  if(route.control)params.set('control','true');
  if(route.clean)params.set('clean','true');
  return `#/${route.screen}?${params}`;
}
export function useWireRoute() {
  const [route,setRoute]=useState(readRoute);
  useEffect(()=>{const update=()=>setRoute(readRoute());addEventListener('popstate',update);addEventListener('hashchange',update);return()=>{removeEventListener('popstate',update);removeEventListener('hashchange',update);};},[]);
  const navigate=(patch:Partial<WireRoute>,replace=false)=>{
    const next={...route,...patch};
    if(patch.study&&patch.study!==route.study){next.participant='014';next.heatmapSession='';next.item='';next.time=0;next.reportId='';next.link='';}
    if(patch.screen&&patch.screen!==route.screen&&!('reportId'in patch))next.reportId='';
    const hash=routeHash(next);
    if(location.hash!==hash)history[replace?'replaceState':'pushState'](null,'',hash);
    setRoute(next);
    dispatchEvent(new HashChangeEvent('hashchange'));
  };
  return {route,navigate};
}
