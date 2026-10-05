import { useEffect, type ReactNode } from 'react';
import { EuiProvider } from '@elastic/eui';
import { EuiThemeAmsterdam } from '@elastic/eui/lib/themes/amsterdam';
import { elasticTheme } from '../tokens/elasticTheme';
export function ThemeFrame({children,mode,scale,product=false}:{children:ReactNode;mode:'light'|'dark';scale:string;product?:boolean}) {
  useEffect(()=>{document.documentElement.dataset.colorMode=mode;document.documentElement.dataset.typeScale=scale;document.body.style.backgroundColor=product?'var(--background-canvas)':'var(--elastic-backgrounds-opaque-plain)';document.body.style.color=product?'var(--text-primary)':'var(--elastic-text-default)';},[mode,scale,product]);
  return <EuiProvider theme={EuiThemeAmsterdam} colorMode={mode==='dark'?'DARK':'LIGHT'} modify={elasticTheme(scale)}>{children}</EuiProvider>;
}
