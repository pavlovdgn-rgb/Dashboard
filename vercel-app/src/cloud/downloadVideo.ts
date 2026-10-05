/** Assemble bounded authenticated range responses; never request a 256 MB Function response. */
export async function downloadVideo(url:string):Promise<void> {
  const pieces:Blob[]=[];let position=0,total=1;
  while(position<total){
    const response=await fetch(url,{headers:{Range:`bytes=${position}-${position+1024*1024-1}`},signal:AbortSignal.timeout(30000)});
    if(response.status!==206)throw Error('Не удалось скачать запись. Повторите попытку.');
    const match=/^bytes (\d+)-(\d+)\/(\d+)$/.exec(response.headers.get('Content-Range')||'');
    if(!match||Number(match[1])!==position)throw Error('Неверный фрагмент видеозаписи.');
    const part=await response.blob();
    if(part.size!==Number(match[2])-position+1)throw Error('Неполный фрагмент видеозаписи.');
    total=Number(match[3]);position=Number(match[2])+1;pieces.push(part);
  }
  const object=URL.createObjectURL(new Blob(pieces,{type:'video/webm'}));
  const link=document.createElement('a');link.href=object;link.download='test-recording.webm';link.click();
  setTimeout(()=>URL.revokeObjectURL(object),60000);
}
