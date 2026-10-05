import { viewContext } from './view'
import { captureSnapshot } from './snapshot'

let collecting=false,clicks=false,visits=false,video=false
let mode='video'
let scenario='',studyTitle='',studyMode='free'
let tasks:Array<{id:string;title:string;instruction:string}>=[]
export const studyInstructions=()=>({scenario,studyTitle,mode:studyMode,tasks})
export const collectionEnabled=()=>collecting
export const clicksEnabled=()=>collecting&&clicks
export const videoEnabled=()=>collecting&&video&&mode==='video'
export const screenshotsEnabled=()=>collecting&&mode==='screenshots'
export const recordingMode=()=>mode

/** Page visits share the click session; no fields, personal identifiers or input values. */
export function startActivity(study:string,session:string,routes:Map<string,string>) {
  collecting=false;clicks=false;visits=false;video=false;scenario='';studyTitle='';tasks=[];studyMode='free'
  const key=`ux-lab-visits:${study}:${session}`
  type Visit={id:string;study:string;session:string;page:string;timestamp:number;vw:number;vh:number;context:ReturnType<typeof viewContext>}
  let pending:Visit[]=[]
  try {pending=JSON.parse(sessionStorage.getItem(key)||'[]')}catch { /* Start a fresh queue. */ }
  let busy=false,disposed=false,lastPath=''
  const persist=()=>{try{sessionStorage.setItem(key,JSON.stringify(pending))}catch{/* Keep memory queue. */}}
  const record=()=>{
    const path=(location.pathname.replace(/^\/participant(?=\/|$)/,'')||'/'),page=routes.get(path)
    if(disposed||!collecting||!visits||!page||path===lastPath)return
    const context=viewContext();context.snapshot=captureSnapshot(context.signature)
    pending.push({id:crypto.randomUUID(),study,session,page:`leed-${page}`,timestamp:Date.now(),vw:innerWidth,vh:innerHeight,context})
    lastPath=path;persist()
  }
  // Observe SPA transitions after React commits, including back/forward navigation.
  const afterNavigation=()=>requestAnimationFrame(()=>requestAnimationFrame(()=>{record();dispatchEvent(new Event('ux-lab-navigation'))}))
  const push=history.pushState,replace=history.replaceState
  const pushWrapper:History['pushState']=function(this:History,...args){push.apply(this,args);afterNavigation()}
  const replaceWrapper:History['replaceState']=function(this:History,...args){replace.apply(this,args);afterNavigation()}
  history.pushState=pushWrapper;history.replaceState=replaceWrapper
  addEventListener('popstate',afterNavigation)
  async function tick() {
    if(busy||disposed)return
    busy=true
    try {
      try {
        const response=await fetch(`/api/project/config?study=${encodeURIComponent(study)}`,{signal:AbortSignal.timeout(20000)})
        if(response.ok) {
          const data=await response.json()
          if(disposed)return
          if((!collecting||!visits)&&data.enabled&&data.collectVisits!==false)lastPath=''
          collecting=Boolean(data.enabled)
          clicks=data.collectClicks!==false;visits=data.collectVisits!==false;video=data.allowVideo!==false
          mode=data.recordingMode==='screenshots'?'screenshots':'video'
          scenario=data.scenario||'';studyTitle=data.studyTitle||'';studyMode=data.mode||(scenario?'scenario':'free');tasks=data.tasks||[]
          dispatchEvent(new Event('ux-lab-policy'))
        } else if(response.status===400||response.status===404){
          collecting=false;clicks=false;visits=false;video=false;scenario='';studyTitle=''
        }
      }catch{/* Keep the last collection state; still queue visits while offline. */}
      record()
      for(const visit of [...pending].slice(0,20)) {
        const response=await fetch('/api/project/visit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(visit),signal:AbortSignal.timeout(20000)})
        if(!response.ok)break
        pending=pending.filter(item=>item.id!==visit.id);persist()
      }
    }catch{/* Keep visits and last known collection state while the local API is offline. */}
    finally{busy=false}
  }
  const timer=setInterval(()=>void tick(),1000);void tick()
  return()=>{disposed=true;clearInterval(timer);removeEventListener('popstate',afterNavigation);if(history.pushState===pushWrapper)history.pushState=push;if(history.replaceState===replaceWrapper)history.replaceState=replace}
}
