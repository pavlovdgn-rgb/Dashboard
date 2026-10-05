import {toCanvas} from 'html-to-image';
import {zipSync} from 'fflate';
import {inertDocument} from '../heatmap/CapturedHeatmap';
import {drawHeatmap} from '../heatmap/drawHeatmap';
import type {ClickData,ClickGroup} from '../heatmap/types';

async function get<T>(url:string):Promise<T>{const response=await fetch(url,{signal:AbortSignal.timeout(30000)});if(!response.ok)throw Error('Не удалось получить данные для выгрузки.');return response.json() as Promise<T>;}

async function render(group:ClickGroup,query:URLSearchParams):Promise<Uint8Array>{
  if(group.vw*group.vh>24000000)throw Error('Размер карты слишком велик для выгрузки.');
  const id=group.context?.snapshot;
  if(!id)throw Error('Для этого экрана ещё нет сохранённого снимка. Откройте интерфейс и выполните действие.');
  const snapshot=await get<{html:string}>(`/api/heatmap/snapshots?id=${encodeURIComponent(id)}`);
  const params=new URLSearchParams(query);params.set('group',group.layout);params.set('aggregation','page');
  const data=await get<ClickData>(`/api/heatmap?${params}`);
  const frame=document.createElement('iframe');frame.setAttribute('sandbox','allow-same-origin');
  Object.assign(frame.style,{position:'fixed',left:'-20000px',top:'0',width:`${group.vw}px`,height:`${group.vh}px`,border:'0'});
  try{
    const loaded=new Promise<void>((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('Не удалось подготовить снимок.')),15000);frame.onload=()=>{clearTimeout(timer);resolve();};});
    frame.srcdoc=inertDocument(snapshot.html);document.body.append(frame);await loaded;
    const doc=frame.contentDocument!;await doc.fonts.ready;
    // Snapshots retain scroll coordinates as data attributes. Move the cloned
    // scroll content before rasterizing, since SVG foreignObject has no scroll state.
    doc.querySelectorAll<HTMLElement>('[data-ux-scroll]').forEach(element=>{
      const [x,y]=(element.dataset.uxScroll||'0,0').split(',').map(Number);
      if(!x&&!y)return;
      const content=doc.createElement('div');
      while(element.firstChild)content.append(element.firstChild);
      Object.assign(content.style,{transform:`translate(${-x}px, ${-y}px)`,width:`${element.scrollWidth}px`});
      element.append(content);element.style.overflow='hidden';
    });
    const canvas=await toCanvas(doc.documentElement,{width:group.vw,height:group.vh,canvasWidth:group.vw,canvasHeight:group.vh,pixelRatio:1,cacheBust:false});
    if(query.get('layer')!=='0'){
      const overlay=document.createElement('canvas');
      const styles=getComputedStyle(document.querySelector('[data-testid="captured-heatmap"]')||document.documentElement);
      for(const name of ['--heatmap-spot-outer','--heatmap-spot-middle','--heatmap-spot-core'])overlay.style.setProperty(name,styles.getPropertyValue(name));
      overlay.hidden=true;document.body.append(overlay);
      const points=data.points.filter(point=>!query.get('target')||point.target===query.get('target'));
      try{drawHeatmap(overlay,points,group.vw,group.vh);canvas.getContext('2d')!.drawImage(overlay,0,0);}finally{overlay.remove();}
    }
    const blob=await new Promise<Blob>((resolve,reject)=>canvas.toBlob(value=>value?resolve(value):reject(Error('Не удалось создать PNG.')),'image/png'));
    return new Uint8Array(await blob.arrayBuffer());
  }finally{frame.remove();}
}

export async function exportHeatmap(query:URLSearchParams):Promise<Blob>{
  const data=await get<ClickData>(`/api/heatmap?${new URLSearchParams({study:query.get('study')||'',session:query.get('session')||'',aggregation:'page'})}`);
  const groups=data.groups.filter(group=>group.page.startsWith('leed-')&&(!query.get('group')||group.layout===query.get('group')));
  if(!groups.length)throw Error('Нет карт для выгрузки.');
  if(groups.length>100)throw Error('В одной выгрузке допускается до 100 карт.');
  if(query.get('format')==='png')return new Blob([new Uint8Array(await render(groups[0],query))],{type:'image/png'});
  const files:Record<string,Uint8Array>={};
  for(const group of groups)files[`${group.page}-${group.vw}x${group.vh}-${group.layout}.png`]=await render(group,query);
  return new Blob([new Uint8Array(zipSync(files,{level:0}))],{type:'application/zip'});
}
