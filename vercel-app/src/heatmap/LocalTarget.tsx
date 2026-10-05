import { useEffect, useRef, useState } from 'react';
import { Storefront } from '../screens/ParticipantSession';
import { ProductTheme } from '../tokens/ProductTheme';
import { CLICK_API, LOCAL_VERSION, pageLabels, type ClickPoint, type CollectorStatus } from './types';
import { drawHeatmap } from './drawHeatmap';
import s from './LocalHeatmap.module.css';
import workspace from '../screens/Workspace.module.css';

export function LocalTarget() {
  const params=new URLSearchParams(location.search),preview=params.get('preview')==='1';
  const study=params.get('study')||'local-demo',page=params.get('page')||'product';
  const requestedOrigin=params.get('parentOrigin')||location.origin;
  const parentOrigin=[location.origin].includes(requestedOrigin)?requestedOrigin:location.origin;
  const root=useRef<HTMLDivElement>(null),canvas=useRef<HTMLCanvasElement>(null);
  const [status,setStatus]=useState<CollectorStatus>({pending:0,error:''});
  useEffect(()=>{
    const host=root.current;if(!host)return;
    if(preview) {
      host.inert=true;
      const receive=(event:MessageEvent)=>{
        if(event.origin!==parentOrigin||event.source!==parent||event.data?.type!=='ux-lab-heatmap')return;
        const surface=host.querySelector('[data-ux-page]') as HTMLElement|null;
        if(!surface||!canvas.current)return;
        const bounds=surface.getBoundingClientRect();
        const matches=event.data.version===LOCAL_VERSION&&Math.abs(bounds.width-event.data.rw)<1&&Math.abs(bounds.height-event.data.rh)<1;
        const points=Array.isArray(event.data.points)?event.data.points as ClickPoint[]:[];
        drawHeatmap(canvas.current,matches?points:[],bounds.width,bounds.height);
        parent.postMessage({type:'ux-lab-preview-status',matches,width:bounds.width,height:bounds.height},parentOrigin);
      };
      addEventListener('message',receive);
      const ready=()=>parent.postMessage({type:'ux-lab-preview-ready'},parentOrigin);
      const observer=new ResizeObserver(ready);observer.observe(host);
      void document.fonts.ready.then(ready);
      return()=>{observer.disconnect();removeEventListener('message',receive);};
    }
    let cancelled=false,collector:ReturnType<NonNullable<Window['UXLabCollector']>['attach']>|undefined;
    const attach=()=>{
      if(cancelled)return;
      collector=window.UXLabCollector?.attach({root:host,study,version:LOCAL_VERSION,endpoint:`${CLICK_API}/api/heatmap/events`,onStatus:setStatus});
    };
    if(window.UXLabCollector)attach();
    else {
      const script=document.createElement('script');script.src='/ux-lab-collector.js';script.onload=attach;
      script.onerror=()=>setStatus({pending:0,error:'Не удалось загрузить сборщик. Обновите страницу.'});document.head.append(script);
    }
    return()=>{cancelled=true;collector?.dispose();};
  },[preview,study,parentOrigin]);
  return <ProductTheme><main className={workspace.participant}>
    <div ref={root} className={s.localSurface}><Storefront initial={page in pageLabels?page:'product'}/>{preview?<canvas ref={canvas} className={s.canvas} aria-label="Плотность собранных кликов"/>:null}</div>
    {!preview?<aside className={s.collectionStatus} aria-live="polite"><strong>Локальная проверка сбора кликов</strong><p>{status.error|| (status.pending?`Ожидают отправки: ${status.pending}`:'Сборщик подключён. Нажимайте на элементы NOVA.')}</p><p>Значения полей, имена и email не отправляются. Новая вкладка — новая сессия.</p><a href={`/?screen=results-overview#/heatmap-live?link=${encodeURIComponent(study)}`} target="_blank" rel="noreferrer">Открыть карту кликов →</a></aside>:null}
  </main></ProductTheme>;
}
