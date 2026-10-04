// Documented Embed Kit 2.0 messages; validate both origin and the selected iframe.
export type PilotEvent={kind:string;page:string;data:Record<string,string|number|boolean>};
const identifier=(value:unknown):value is string=>typeof value==='string'&&/^[a-zA-Z0-9_.:-]{1,120}$/.test(value);
const finite=(value:unknown):value is number=>typeof value==='number'&&Number.isFinite(value)&&Math.abs(value)<=1000000;
export function embedURL(link:string,clientId:string){
  const input=new URL(link);
  if(input.protocol!=='https:'||!['www.figma.com','figma.com','embed.figma.com'].includes(input.hostname)||!/^\/proto\/[a-zA-Z0-9]+(?:\/|$)/.test(input.pathname))throw Error('Вставьте ссылку на Figma-прототип из режима презентации.');
  const output=new URL('https://embed.figma.com'+input.pathname);
  for(const key of ['node-id','starting-point-node-id','page-id','version-id','scaling','content-scaling']){const value=input.searchParams.get(key);if(value)output.searchParams.set(key,value);}
  output.searchParams.set('embed-host','ux-lab');output.searchParams.set('footer','false');output.searchParams.set('disable-default-keyboard-nav','true');
  if(clientId)output.searchParams.set('client-id',clientId);
  return output.href;
}
export function figmaEvent(event:MessageEvent,source:Window|null):PilotEvent|null{
  if(!source||event.source!==source||event.origin!=='https://www.figma.com')return null;
  const message=event.data;
  if(!message||typeof message!=='object')return null;
  const kind=message.type,data=message.data;
  if(['INITIAL_LOAD','LOGIN_SCREEN_SHOWN','PASSWORD_SCREEN_SHOWN'].includes(kind))return {kind,page:'figma-prototype',data:{}};
  if(!data||typeof data!=='object')return null;
  if(kind==='PRESENTED_NODE_CHANGED'&&identifier(data.presentedNodeId)&&typeof data.isStoredInHistory==='boolean')return {kind,page:data.presentedNodeId,data:{node:data.presentedNodeId,history:data.isStoredInHistory}};
  if(kind==='NEW_STATE'&&[data.nodeId,data.currentVariantId,data.newVariantId].every(identifier)&&typeof data.isTimedChange==='boolean')return {kind,page:data.nodeId,data:{node:data.nodeId,before:data.currentVariantId,after:data.newVariantId,timed:data.isTimedChange}};
  if(kind==='MOUSE_PRESS_OR_RELEASE'){
    const p=data.targetNodeMousePosition,f=data.nearestScrollingFrameMousePosition,s=data.nearestScrollingFrameOffset;
    if(!identifier(data.presentedNodeId)||typeof data.handled!=='boolean'||!p||!f||!s||![p.x,p.y,f.x,f.y,s.x,s.y].every(finite))return null;
    return {kind,page:data.presentedNodeId,data:{node:data.presentedNodeId,target:identifier(data.targetNodeId)?data.targetNodeId:data.presentedNodeId,handled:data.handled,x:p.x,y:p.y,scrollFrame:identifier(data.nearestScrollingFrameId)?data.nearestScrollingFrameId:data.presentedNodeId,scrollX:s.x,scrollY:s.y,frameX:f.x,frameY:f.y}};
  }
  return null;
}
