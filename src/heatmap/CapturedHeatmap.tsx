import { useEffect, useRef, useState } from 'react';
import { EuiCallOut } from '@elastic/eui';
import { CLICK_API, type ClickGroup, type ClickPoint } from './types';
import { drawHeatmap } from './drawHeatmap';
import s from './LocalHeatmap.module.css';

/** Backgrounds are inert: no script execution, forms, navigation or remote app code. */
function inertDocument(html:string) {
  const doc=new DOMParser().parseFromString(html,'text/html');
  doc.querySelectorAll('script,iframe,object,embed,meta[http-equiv],base').forEach(el=>el.remove());
  doc.querySelectorAll('*').forEach(el=>{
    for(const attr of Array.from(el.attributes))if(attr.name.startsWith('on')||['srcdoc','action','formaction'].includes(attr.name))el.removeAttribute(attr.name);
  });
  const policy=doc.createElement('meta');policy.httpEquiv='Content-Security-Policy';
  policy.content="default-src 'none'; style-src 'unsafe-inline' https://fonts.googleapis.com; font-src https://fonts.gstatic.com data: http://127.0.0.1:5175 http://localhost:5175; img-src data: http://127.0.0.1:5175 http://localhost:5175; form-action 'none'; base-uri 'none'";
  doc.head.prepend(policy);
  return '<!doctype html>'+doc.documentElement.outerHTML;
}
export function CapturedHeatmap({group,points,exportMode=false,highlightPoints=[],onlySaved=false}:{group:ClickGroup;points:ClickPoint[];exportMode?:boolean;highlightPoints?:ClickPoint[];onlySaved?:boolean}) {
  const [background,setBackground]=useState<{id:string;html:string}|null>(null),[error,setError]=useState('');
  const [scale,setScale]=useState(1);
  const host=useRef<HTMLDivElement>(null),canvas=useRef<HTMLCanvasElement>(null);
  const id=group.context?.snapshot;
  useEffect(()=>{
    if(!id)return;
    const controller=new AbortController();let busy=false;
    async function read() {
      if(busy)return;busy=true;
      try {
        const response=await fetch(`${CLICK_API}/api/heatmap/snapshots?id=${encodeURIComponent(id!)}`,{signal:controller.signal});
        if(!response.ok)throw Error('Фон ещё загружается. Координаты кликов уже доступны.');
        const data=await response.json() as {id:string;html:string;width:number;height:number};
        if(!group.backgroundResponsive&&(data.width!==group.vw||data.height!==group.vh))throw Error('Размер сохранённого фона не совпадает с картой.');
        if(!controller.signal.aborted){setBackground({id:id!,html:inertDocument(data.html)});setError('');}
      }catch(cause){if(!controller.signal.aborted)setError(cause instanceof Error?cause.message:'Не удалось загрузить фон');}
      finally{busy=false;}
    }
    void read();const timer=setInterval(()=>void read(),3000);
    return()=>{controller.abort();clearInterval(timer);};
  },[id,group.vw,group.vh,group.backgroundResponsive]);
  useEffect(()=>{
    if(!host.current)return;
    const observer=new ResizeObserver(()=>setScale(Math.min(1,host.current!.clientWidth/group.vw)));
    observer.observe(host.current);return()=>observer.disconnect();
  },[group.vw,background?.id]);
  useEffect(()=>{if(canvas.current)drawHeatmap(canvas.current,points,group.vw,group.vh);},[points,group.vw,group.vh]);
  const html=background?.id===id?background?.html:undefined;
  if(onlySaved&&!html)return <div ref={host} role="status">{error?'Снимок ещё не передан. Повторяем загрузку…':'Загружаем сохранённый снимок…'}</div>;
  return <>
    {error?<EuiCallOut color="warning" title="Используется исходный интерфейс"><p>Сохранённый фон недоступен. Клики отображаются поверх исходного экрана.</p></EuiCallOut>:null}
    <div ref={host} className={s.preview} data-testid="captured-heatmap"
      data-background={html?'saved':id&&!error?'loading':'fallback'}
      style={exportMode?{width:group.vw,maxBlockSize:'none',border:0,borderRadius:0,overflow:'hidden'}:undefined}>
      <div style={{position:'relative',width:group.vw*scale,height:group.vh*scale}}>
        <div data-testid="heatmap-export-surface" className={s.capturedViewport} style={{width:group.vw,height:group.vh,transform:`scale(${scale})`,transformOrigin:'top left'}}>
          {html?<iframe title="Сохранённый фон Lead Generation" sandbox="allow-same-origin" srcDoc={html} style={{width:group.vw,height:group.vh,pointerEvents:'none'}} onLoad={event=>{
            const frame=event.currentTarget;
            const restore=()=>{
              const doc=frame.contentDocument;
              doc?.querySelectorAll<HTMLElement>('[data-ux-scroll]').forEach(el=>{
                const [x,y]=(el.dataset.uxScroll||'0,0').split(',').map(Number);
                if(el===doc.body)frame.contentWindow?.scrollTo(x,y);else el.scrollTo(x,y);
              });
            };
            restore();void frame.contentDocument?.fonts.ready.then(restore);
          }}/>:<iframe title="Исходный интерфейс Lead Generation" src={`http://127.0.0.1:5175${group.path||'/leads-table'}?ux_preview=1&parentOrigin=${encodeURIComponent(location.origin)}`} style={{width:group.vw,height:group.vh,pointerEvents:'none'}}/>}
          <canvas ref={canvas} className={s.canvas} data-testid="captured-click-layer" aria-label="Тепловой слой реальных кликов"/>
          {highlightPoints.length?<svg className={s.elementHighlight} data-testid="heatmap-element-highlight" viewBox={`0 0 ${group.vw} ${group.vh}`} aria-hidden="true">
            {[...new Map(highlightPoints.map(point=>[point.element?JSON.stringify(point.element.rect):`${point.x}:${point.y}`,point])).values()].map((point,index)=>point.element?
              <rect key={index} x={point.element.rect[0]*group.vw} y={point.element.rect[1]*group.vh} width={point.element.rect[2]*group.vw} height={point.element.rect[3]*group.vh}/>:
              <circle key={index} cx={point.x*group.vw} cy={point.y*group.vh} r={24}/>)}
          </svg>:null}
        </div>
      </div>
    </div>
  </>;
}
