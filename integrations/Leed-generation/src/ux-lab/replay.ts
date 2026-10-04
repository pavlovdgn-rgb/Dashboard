/** Event-driven, inert interface snapshots. Never captures other tabs or field values. */
import {screenshotsEnabled} from './activity'
import {captureSnapshot} from './snapshot'
import {describeElement} from './element'
import {viewContext} from './view'

type Frame={id:string;study:string;session:string;seq:number;timestamp:number;page:string;snapshot:string;vw:number;vh:number;kind:'screen'|'click'|'change'|'scroll';label:string;target:{x?:number;y?:number;rect?:[number,number,number,number]}}
const API='http://127.0.0.1:5174/api/project/frames'

export function startReplay(study:string,session:string,routes:Map<string,string>){
  const sequenceKey=`ux-lab-frames-seq:${study}:${session}`
  let seq=Number(sessionStorage.getItem(sequenceKey)||(study==='leed-local'?sessionStorage.getItem(`ux-lab-frames-seq:${session}`):null)||0),disposed=false,busy=false,active=false
  let lastPage='',lastSnapshot='',recentUntil=0,settle:ReturnType<typeof setTimeout>|undefined,scroll:ReturnType<typeof setTimeout>|undefined
  const memory=new Map<string,Frame>()
  const database=new Promise<IDBDatabase>((resolve,reject)=>{
    const request=indexedDB.open('ux-lab-frames',1)
    request.onupgradeneeded=()=>request.result.createObjectStore('pending',{keyPath:'id'})
    request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error)
  }).catch(()=>null)
  const write=(frame:Frame)=>{
    memory.set(frame.id,frame)
    void database.then(db=>{db?.transaction('pending','readwrite').objectStore('pending').put(frame)})
  }
  async function flush(){
    if(busy||disposed)return;busy=true
    try{
      const db=await database
      const stored=db?await new Promise<Frame[]>((resolve,reject)=>{const request=db.transaction('pending').objectStore('pending').getAll();request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error)}):[]
      const items=[...new Map([...stored,...memory.values()].map(frame=>[frame.id,frame])).values()].sort((a,b)=>a.timestamp-b.timestamp||a.seq-b.seq)
      for(const frame of items.slice(0,30)){
        const response=await fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(frame),signal:AbortSignal.timeout(5000)})
        if(!response.ok)break
        memory.delete(frame.id);db?.transaction('pending','readwrite').objectStore('pending').delete(frame.id)
      }
    }catch{/* Durable frames retry when the local server returns. */}finally{busy=false}
  }
  function capture(kind:Frame['kind'],label='',target:Frame['target']={}){
    if(disposed||!screenshotsEnabled())return
    const page=routes.get(location.pathname);if(!page)return
    const context=viewContext(),snapshot=captureSnapshot(context.signature,true)
    if(kind!=='click'&&snapshot===lastSnapshot&&page===lastPage)return
    if(page!==lastPage&&kind!=='click'){kind='screen';label=''}
    lastPage=page;lastSnapshot=snapshot;seq++
    sessionStorage.setItem(sequenceKey,String(seq))
    write({id:crypto.randomUUID(),study,session,seq,timestamp:Date.now(),page:`leed-${page}`,snapshot,vw:innerWidth,vh:innerHeight,kind,label,target})
    void flush()
  }
  function afterAction(){
    clearTimeout(settle)
    settle=setTimeout(()=>capture('change'),180)
  }
  const relevant=(event:Event)=>event.target instanceof Element&&!event.target.closest('[data-ux-overlay],[data-ux-private]')
  const click=(event:MouseEvent)=>{
    if(!screenshotsEnabled()||!relevant(event))return
    // Flush a prior action before this one changes the DOM; retain fast consecutive actions.
    clearTimeout(settle);capture('change')
    const info=describeElement(event.target as Element).info
    capture('click',info.label,{x:Math.max(0,Math.min(1,event.clientX/innerWidth)),y:Math.max(0,Math.min(1,event.clientY/innerHeight)),...(info.rect[2]>0&&info.rect[3]>0?{rect:info.rect}:{})})
    recentUntil=Date.now()+2000;afterAction()
  }
  const change=(event:Event)=>{if(relevant(event)&&screenshotsEnabled()){recentUntil=Date.now()+2000;afterAction()}}
  const navigation=()=>{if(screenshotsEnabled()){recentUntil=Date.now()+2000;afterAction()}}
  const policy=()=>{
    const next=screenshotsEnabled()
    if(next&&!active){lastPage='';lastSnapshot='';recentUntil=Date.now()+2000;capture('screen')}
    if(!next){clearTimeout(settle);clearTimeout(scroll)}
    active=next
  }
  const scrolled=(event:Event)=>{if(screenshotsEnabled()&&!(event.target instanceof Element&&event.target.closest('[data-ux-overlay]'))){clearTimeout(scroll);scroll=setTimeout(()=>capture('scroll'),300)}}
  const observer=new MutationObserver(changes=>{
    if(!screenshotsEnabled()||Date.now()>recentUntil)return
    if(changes.some(change=>!(change.target instanceof Element&&change.target.closest('[data-ux-overlay]'))))afterAction()
  })
  observer.observe(document.body,{childList:true,subtree:true,attributes:true,characterData:true})
  document.addEventListener('click',click,true);document.addEventListener('change',change,true);document.addEventListener('scroll',scrolled,true)
  addEventListener('ux-lab-navigation',navigation);addEventListener('ux-lab-policy',policy);addEventListener('online',flush)
  const timer=setInterval(()=>void flush(),1000);policy();void flush()
  return()=>{disposed=true;clearInterval(timer);clearTimeout(settle);clearTimeout(scroll);observer.disconnect();document.removeEventListener('click',click,true);document.removeEventListener('change',change,true);document.removeEventListener('scroll',scrolled,true);removeEventListener('ux-lab-navigation',navigation);removeEventListener('ux-lab-policy',policy);removeEventListener('online',flush)}
}
