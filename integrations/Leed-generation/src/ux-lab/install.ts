import { screens } from '../screens/registry'
import { restoreScroll, viewContext, type ViewContext } from './view'
import { captureSnapshot } from './snapshot'
import { describeElement } from './element'
import { clicksEnabled, startActivity } from './activity'
import {startTaskTracking,taskElement} from './task'
import { startReplay } from './replay'

const VERSION='leed-local-v2'
const params=new URLSearchParams(location.search)
const preview=params.get('ux_preview')==='1'
const origins=['http://127.0.0.1:5173','http://localhost:5173','http://127.0.0.1:6006','http://localhost:6006']
const requested=params.get('parentOrigin')||origins[0]
const parentOrigin=origins.includes(requested)?requested:origins[0]
const routes=new Map(screens.map(screen=>[screen.route,screen.id]))
routes.set('/','index');routes.set('/showcase','showcase')
type Point={x:number;y:number;count:number}
type Payload={type:string;version:string;rw:number;rh:number;context:ViewContext;points:Point[];palette:string[]}
type Collector={attach(config:Record<string,unknown>):{dispose():void;session:string}}
declare global {interface Window {UXLabCollector?:Collector;__uxLabStatus?:unknown}}

if(preview) {
  // The preview is read-only and never starts a collection session.
  const canvas=document.createElement('canvas')
  canvas.dataset.uxOverlay='true'
  canvas.setAttribute('aria-label','Плотность кликов')
  Object.assign(canvas.style,{position:'fixed',inset:'0',zIndex:'2147483647',pointerEvents:'none'})
  document.body.append(canvas)
  let payload:Payload|undefined
  function render() {
    if(!payload)return
    restoreScroll(payload.context?.scrolls||[])
    const view=viewContext()
    const matches=payload.version===VERSION && payload.rw===innerWidth && payload.rh===innerHeight && payload.context?.signature===view.signature
    canvas.width=innerWidth;canvas.height=innerHeight
    const ctx=canvas.getContext('2d')
    if(matches&&ctx) {
      const maximum=Math.max(1,...payload.points.map(p=>p.count))
      for(const p of payload.points) {
        const x=p.x*innerWidth,y=p.y*innerHeight,r=28
        const gradient=ctx.createRadialGradient(x,y,0,x,y,r)
        ctx.globalAlpha=.35+.65*p.count/maximum
        gradient.addColorStop(0,payload.palette[0])
        gradient.addColorStop(.5,payload.palette[1]);gradient.addColorStop(.8,payload.palette[2]);gradient.addColorStop(1,'transparent')
        ctx.fillStyle=gradient;ctx.fillRect(x-r,y-r,r*2,r*2)
      }
    }
    parent.postMessage({type:'ux-lab-preview-status',matches},parentOrigin)
  }
  addEventListener('message',event=>{
    if(event.origin!==parentOrigin||event.source!==parent||event.data?.type!=='ux-lab-heatmap')return
    payload=event.data as Payload;render()
  })
  void document.fonts.ready.then(()=>parent.postMessage({type:'ux-lab-preview-ready'},parentOrigin))
  const timer=setInterval(render,750)
  import.meta.hot?.dispose(()=>{clearInterval(timer);canvas.remove()})
} else if(['localhost','127.0.0.1'].includes(location.hostname)) {
  const supplied=params.get('ux_study')
  if(supplied&&/^[a-zA-Z0-9_.:-]{1,120}$/.test(supplied))sessionStorage.setItem('ux-lab-leed-study',supplied)
  const study=sessionStorage.getItem('ux-lab-leed-study')||'leed-local'
  const script=document.createElement('script')
  script.src='http://127.0.0.1:5174/sdk.js'
  script.onload=()=>{
    const collector=window.UXLabCollector?.attach({root:document.body,study,version:VERSION,
      endpoint:'http://127.0.0.1:5174/api/heatmap/events',
      onStatus:(status:unknown)=>{window.__uxLabStatus=status},
      getContext:(target:Element)=>{
        if(!clicksEnabled())return null
        const id=routes.get(location.pathname)
        if(!id)return null
        const described=describeElement(target)
        taskElement(described.target,described.info.label)
        const view=viewContext()
        view.snapshot=captureSnapshot(view.signature)
        view.element=described.info
        return {page:`leed-${id}`,target:described.target,view}
      }})
    const stopActivity=collector?startActivity(study,collector.session,routes):undefined
    const stopTask=collector?startTaskTracking(study,collector.session,routes):undefined
    const stopReplay=collector?startReplay(study,collector.session,routes):undefined
    import.meta.hot?.dispose(()=>{collector?.dispose();stopActivity?.();stopReplay?.();stopTask?.()})
  }
  document.head.append(script)
}
