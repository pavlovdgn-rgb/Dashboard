import type { VariantValues } from './CatalogComponent';
import { ProductAction } from './ProductComponent';
import { ProductDropdown } from './ProductDropdown';

export function AttemptActionPreview({values:p}:{values:VariantValues}) {
  const mode=String(p.Mode||'Single');
  const emit=(attempt:number)=>{if(typeof p.onSelectAttempt==='function')p.onSelectAttempt(attempt);if(typeof p.onOpenRecording==='function')p.onOpenRecording({attempt});else if(typeof p.onClick==='function')p.onClick();};
  if(mode!=='Multiple')return <ProductAction kind={mode==='Single'?'Primary':'Secondary'} onClick={()=>{if(mode==='Single')emit(1);else if(typeof p.onClick==='function')p.onClick();}}>{mode==='Single'?'Открыть запись':'К участнику'}</ProductAction>;
  const attempts=Array.isArray(p.attempts)?p.attempts as number[]:[1,2];
  return <ProductDropdown label="Выбрать попытку" placeholder="Выбрать попытку" icon="layers" value="" options={attempts.map(attempt=>({value:String(attempt),label:`Попытка ${attempt}`}))} onChange={value=>emit(Number(value))}/>;
}
