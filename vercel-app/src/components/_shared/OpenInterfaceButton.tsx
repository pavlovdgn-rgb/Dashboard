import { ProductButton } from '../ProductButton/ProductButton';
import s from './OpenInterfaceButton.module.css';

export function OpenInterfaceButton({url,label='Открыть Lead Generation'}:{url:string;label?:string}) {
  return <ProductButton className={s.root} Kind="Primary" iconRight="arrowRight" onClick={()=>window.open(url,'_blank','noopener')}>{label}</ProductButton>;
}
