"""Keep catalogue controls inside the actual Figma variant matrix."""
from pathlib import Path

root=Path(__file__).resolve().parents[1]
path=root/'src/pages/Showcase.tsx'
s=path.read_text(encoding='utf-8')
if "from '../tokens/elasticTheme'" not in s:
    s=s.replace("import styles from './Showcase.module.css';", "import styles from './Showcase.module.css';\nimport { elasticTheme } from '../tokens/elasticTheme';")
s=s.replace("modify={{font:{family: 'Inter, sans-serif'}}}", "modify={elasticTheme(scale)}")
if 'const changeVariant=' not in s:
    anchor="  return <EuiProvider"
    s=s.replace(anchor,"""  const changeVariant=(key:string,value:string)=>{
    const current={...entry.defaults,...overrides} as Record<string,unknown>;
    const candidates=entry.variants.filter(variant=>(variant as Record<string,string>)[key]===value);
    const score=(variant:Record<string,string>)=>Object.entries(variant).filter(([axis,option])=>axis!==key&&current[axis]===option).length;
    const candidate=[...candidates].sort((a,b)=>score(b)-score(a))[0];
    if(candidate)setOverrides(candidate as Record<string,string>);
  };
"""+anchor)
s=s.replace('<select value={overrides[key]||String(prop.defaultValue)} onChange={e=>setOverrides({...overrides,[key]:e.target.value})}>', '<select aria-label={key} value={overrides[key]||String(prop.defaultValue)} onChange={e=>changeVariant(key,e.target.value)}>')
path.write_text(s,encoding='utf-8')
