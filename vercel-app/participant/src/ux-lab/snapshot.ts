/** Static local backgrounds. Scripts, handlers and field values are never included. */
import { hash } from './view'

const API='/api/heatmap/snapshots'
const enabled=true&&new URLSearchParams(location.search).get('ux_preview')!=='1'
const saved=new Map<string,string>()
const values=new Map<EventTarget,string>()
const redactions=new Set<string>()
const rememberInput=(event:Event)=>{
  const el=event.target
  if(el instanceof HTMLInputElement||el instanceof HTMLTextAreaElement)values.set(el,el.value)
}
const rememberChange=(event:Event)=>{
  const value=values.get(event.target!)
  if(value)redactions.add(value)
}
if(enabled){document.addEventListener('input',rememberInput,true);document.addEventListener('change',rememberChange,true)}

type Snapshot={id:string;html:string;width:number;height:number}
const database:Promise<IDBDatabase|null>=enabled?new Promise<IDBDatabase>((resolve,reject)=>{
  const request=indexedDB.open('ux-lab-backgrounds',1)
  request.onupgradeneeded=()=>request.result.createObjectStore('pending',{keyPath:'id'})
  request.onsuccess=()=>resolve(request.result)
  request.onerror=()=>reject(request.error)
}).catch(()=>null):Promise.resolve(null)
const pending=new Map<string,Snapshot>()
let flushing=false
async function flush() {
  if(flushing)return
  flushing=true
  try {
    const db=await database
    const stored=db?await new Promise<Snapshot[]>((resolve,reject)=>{
      const request=db.transaction('pending').objectStore('pending').getAll()
      request.onsuccess=()=>resolve(request.result);request.onerror=()=>reject(request.error)
    }):[]
    for(const item of new Map([...stored,...pending.values()].map(item=>[item.id,item])).values()) {
      try {
        const response=await fetch(API,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(item),signal:AbortSignal.timeout(5000)})
        if(!response.ok)continue // One rejected background must never block later ones.
        pending.delete(item.id)
        db?.transaction('pending','readwrite').objectStore('pending').delete(item.id)
      } catch { /* Other backgrounds may still be deliverable. */ }
    }
  } catch { /* Retry separately from clicks; a missing background is shown explicitly. */ }
  finally {flushing=false}
}
const timer=enabled?setInterval(()=>void flush(),2000):undefined
if(enabled)addEventListener('online',flush)
import.meta.hot?.dispose(()=>{clearInterval(timer);removeEventListener('online',flush);document.removeEventListener('input',rememberInput,true);document.removeEventListener('change',rememberChange,true)})

export function captureSnapshot(signature:string,fresh=false):string {
  const key=[(location.pathname.replace(/^\/participant(?=\/|$)/,'')||'/'),innerWidth,innerHeight,signature].join(':')
  const previous=saved.get(key)
  if(previous&&!fresh)return previous
  const source=document.body
  const clone=source.cloneNode(true) as HTMLBodyElement
  const originals=[source,...source.querySelectorAll('*')]
  const copies=[clone,...clone.querySelectorAll('*')]
  const hiddenValues=new Set([...redactions,...values.values()].filter(Boolean))
  originals.forEach((el,index)=>{
    const copy=copies[index]
    if(el instanceof HTMLInputElement||el instanceof HTMLTextAreaElement) {
      if(el.value)hiddenValues.add(el.value)
      copy.removeAttribute('value')
      if(copy instanceof HTMLInputElement) {copy.value='';copy.placeholder=el instanceof HTMLInputElement?el.placeholder:'';copy.toggleAttribute('checked',el instanceof HTMLInputElement&&el.checked)}
      if(copy instanceof HTMLTextAreaElement) {copy.value='';copy.textContent=''}
    }
    if(el instanceof HTMLElement&&(el.scrollLeft||el.scrollTop)) {
      copy.setAttribute('data-ux-scroll',`${el.scrollLeft},${el.scrollTop}`)
    }
    // Preserve the actual font metrics, including fallback fonts in this browser.
    if(copy instanceof HTMLElement) {
      const style=getComputedStyle(el)
      copy.style.fontFamily=style.fontFamily
    }
    for(const attr of [...copy.attributes]) {
      if(attr.name.startsWith('on')||['srcdoc','action','formaction','autofocus','value'].includes(attr.name))copy.removeAttribute(attr.name)
    }
    if(copy instanceof HTMLAnchorElement)copy.removeAttribute('href')
    if(el instanceof HTMLOptionElement)copy.toggleAttribute('selected',el.selected)
    if(copy instanceof HTMLImageElement) {copy.src=(el as HTMLImageElement).currentSrc|| (el as HTMLImageElement).src;copy.removeAttribute('srcset')}
    if(copy instanceof SVGElement&&copy.hasAttribute('href')) {
      const href=copy.getAttribute('href')!
      if(!href.startsWith('#'))copy.setAttribute('href',new URL(href,location.origin).href)
    }
  })
  clone.querySelectorAll('script,style,link,iframe,object,embed,meta,base,[data-ux-overlay]').forEach(el=>el.remove())
  clone.querySelectorAll('[data-ux-private],[contenteditable]').forEach(el=>{el.textContent='•••'})
  for(const value of [...hiddenValues])if(value.trim())hiddenValues.add(value.trim())
  const secrets=[...hiddenValues].sort((a,b)=>b.length-a.length)
  // Redact typed values also if the application has copied them into a message or card.
  const walker=document.createTreeWalker(clone,NodeFilter.SHOW_TEXT)
  while(walker.nextNode()) {
    let text=walker.currentNode.textContent||''
    for(const value of secrets)text=text.split(value).join('•••')
    walker.currentNode.textContent=text
  }
  clone.querySelectorAll('*').forEach(el=>{
    for(const attr of [...el.attributes]) {
      if(!['title','aria-label','aria-description','placeholder'].includes(attr.name))continue
      let value=attr.value
      for(const secret of secrets)value=value.split(secret).join('•••')
      el.setAttribute(attr.name,value)
    }
  })
  let css=''
  for(const sheet of [...document.styleSheets]) {
    try {css += [...sheet.cssRules].map(rule=>rule.cssText).join('\n')}catch { /* Cross-origin font CSS is handled by the existing font import. */ }
  }
  css=css.replace(/url\((['"]?)(?!data:|https?:|#)([^)'"\s]+)\1\)/g,(_all,quote,path)=>`url(${quote}${new URL(path,location.origin).href}${quote})`)
  css+='\n*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}body{overflow:hidden!important}'
  clone.dataset.uxScroll=`${scrollX},${scrollY}`
  const html=`<!doctype html><html><head><meta charset="utf-8"><style>${css.replace(/<\/style/gi,'<\\/style')}</style></head>${clone.outerHTML}</html>`
  const id=`s2-${hash(`${innerWidth}:${innerHeight}:${html}`)}`
  const snapshot={id,html,width:innerWidth,height:innerHeight}
  saved.set(key,id);pending.set(id,snapshot)
  void database.then(db=>{db?.transaction('pending','readwrite').objectStore('pending').put(snapshot)}).catch(()=>{})
  void flush()
  return id
}
