/** A content-free fingerprint: only the hash and numeric scroll offsets leave the page. */
import type { ElementInfo } from './element'
export type ViewContext = {signature:string;scrolls:number[][];snapshot?:string;element?:ElementInfo}
function elements() {
  return [...document.body.querySelectorAll<HTMLElement>('*')].filter(el=>!el.closest('[data-ux-overlay]') && !['SCRIPT','STYLE','LINK'].includes(el.tagName))
}
export function hash(value:string) {
  let a=2166136261,b=3335557771
  for(let i=0;i<value.length;i++) { a=Math.imul(a^value.charCodeAt(i),16777619);b=Math.imul(b^value.charCodeAt(i),2246822519) }
  return (a>>>0).toString(16).padStart(8,'0')+(b>>>0).toString(16).padStart(8,'0')
}
export function viewContext():ViewContext {
  const nodes=elements(),scrolls:number[][]=[],parts:string[]=[]
  if(scrollX||scrollY)scrolls.push([-1,Math.round(scrollX),Math.round(scrollY)])
  nodes.forEach((el,index)=>{
    if(el.scrollLeft||el.scrollTop)scrolls.push([index,Math.round(el.scrollLeft),Math.round(el.scrollTop)])
    const r=el.getBoundingClientRect()
    if(!r.width||!r.height||r.bottom<0||r.right<0||r.top>innerHeight||r.left>innerWidth)return
    // Values of inputs and editable text are deliberately excluded.
    const text=el.matches('input,textarea,[contenteditable]')?'':[...el.childNodes].filter(node=>node.nodeType===Node.TEXT_NODE).map(node=>node.textContent?.trim()).join('')
    parts.push([index,el.tagName,...[r.x,r.y,r.width,r.height].map(Math.round),el.getAttribute('aria-expanded'),el.getAttribute('aria-selected'),text].join(':'))
  })
  return {signature:hash(parts.join('|')),scrolls}
}
export function restoreScroll(scrolls:number[][]) {
  const nodes=elements()
  for(const [index,x,y] of scrolls) { if(index===-1)window.scrollTo(x,y);else nodes[index]?.scrollTo(x,y) }
}
