export const API='http://127.0.0.1:5176';
export type Connection={id:string;study:string;name:string;kind:'web'|'figma';url:string;client_id:string;enabled:number};
export type StoredEvent={id:string;page:string;session:string;timestamp:number;kind?:string;target?:string;data?:Record<string,unknown>};
export type Result={events:StoredEvent[];total:{events:number;sessions:number}};
export async function request<T>(path:string,body?:unknown):Promise<T>{
  const response=await fetch(API+path,{...(body===undefined?{}:{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}),signal:AbortSignal.timeout(5000)});
  const result=await response.json();if(!response.ok)throw Error(result.error||'Не удалось выполнить запрос');return result;
}
