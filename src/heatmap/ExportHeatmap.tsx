import { useEffect, useState } from 'react';
import { ProductTheme } from '../tokens/ProductTheme';
import { CapturedHeatmap } from './CapturedHeatmap';
import type { ClickGroup, ClickPoint } from './types';

/** Read-only rendering surface populated by the local screenshot worker. */
export function ExportHeatmap() {
  const [data,setData]=useState<{group:ClickGroup;points:ClickPoint[]}|null>(null);
  const [error,setError]=useState(false);
  useEffect(()=>{
    const controller=new AbortController();
    fetch('/__heatmap_export_payload',{signal:controller.signal}).then(response=>{
      if(!response.ok)throw Error('Export payload unavailable');
      return response.json();
    }).then(setData).catch(()=>{if(!controller.signal.aborted)setError(true);});
    return()=>controller.abort();
  },[]);
  return <ProductTheme>{data?<CapturedHeatmap group={data.group} points={data.points} exportMode/>:error?<p role="alert">Запустите сохранение из тепловой карты.</p>:null}</ProductTheme>;
}
