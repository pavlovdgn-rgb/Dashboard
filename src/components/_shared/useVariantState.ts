import { useState, type Dispatch, type SetStateAction } from 'react';

// A catalogue property is also the reset value for an interactive example.
// Synchronize during render so changing a variant never paints stale state.
export function useVariantState<T>(source:T):[T,Dispatch<SetStateAction<T>>] {
  const [snapshot,setSnapshot]=useState({source,value:source});
  const changed=!Object.is(source,snapshot.source);
  if(changed)setSnapshot({source,value:source});
  const setValue:Dispatch<SetStateAction<T>>=value=>setSnapshot(previous=>({
    source:previous.source,
    value:typeof value==='function'?(value as (previous:T)=>T)(previous.value):value,
  }));
  return [changed?source:snapshot.value,setValue];
}
