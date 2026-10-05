import { CLICK_API } from '../heatmap/types';
export const currentStudy=()=>new URLSearchParams(location.hash.split('?')[1]||'').get('study')||'leed-local';
export async function liveApi<T>(path:string,data?:unknown):Promise<T> {
  const url=new URL(`${CLICK_API}/api/project${path}`);
  if(!url.searchParams.has('study')&&currentStudy()!=='leed-local')url.searchParams.set('study',currentStudy());
  const response=await fetch(url,data===undefined?{signal:AbortSignal.timeout(30000)}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal:AbortSignal.timeout(30000)});
  if(!response.ok){const failure=await response.json().catch(()=>({}));throw Error(failure.error||(response.status===400?'Проверьте заполненные поля.':'Нет связи с сервером. Повторите попытку.'));}
  return response.json() as Promise<T>;
}
