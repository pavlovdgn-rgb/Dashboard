import type { Meta, StoryObj } from '@storybook/react-vite';
import manifest from '../tokens/manifest.json';
import primitives from '../tokens/primitives.css?raw';
import semantics from '../tokens/semantics.css?raw';
import styles from './catalog.module.css';

const declarations=(css:string)=>[...css.matchAll(/(--[\w-]+)\s*:\s*([^;]+);/g)].map(match=>({name:match[1],value:match[2].trim()}));
const primitiveTokens=declarations(primitives);
const semanticTokens=declarations(semantics);
const names=new Map(manifest.tokens.map(token=>[token.css,token.name]));
function TokenCatalog({kind,colorMode='light',typeScale='medium'}:{kind:'Primitive'|'Semantic'|'Typography';colorMode?:string;typeScale?:string}) {
  const globals={colorMode,typeScale};
  if(kind==='Typography')return <section className={styles.foundation} data-foundation="Typography"><h1>Типографика · {manifest.textStyles.length}</h1><p>Шкала: {globals.typeScale}. Исходные Text Styles с пометкой Deprecated сохранены.</p>{manifest.textStyles.map(style=><article className={styles.typeSample} key={style.id} data-text-style={style.id}><small>{style.name} · .{style.className}</small><p className={style.className}>UX-Lab — исследуем интерфейсы. Съешь ещё этих мягких французских булок. 0123456789</p></article>)}</section>;
  const rows=kind==='Primitive'?primitiveTokens:semanticTokens;
  const grouped=[...new Set(rows.map(row=>row.name))].map(name=>({name,values:[...new Set(rows.filter(row=>row.name===name).map(row=>row.value))]}));
  return <section className={styles.foundation} data-foundation={kind}><h1>{kind==='Primitive'?'Глобальные переменные':'Смысловые переменные'} · {grouped.length}</h1><p>{kind==='Primitive'?'Точные значения из primitives.css: цвета, размеры, начертания и остальные примитивы.':'Все объявления semantics.css. Ниже указаны связи с примитивами и aliases, включая разные режимы.'}</p><p>Elastic UI: {globals.colorMode} · UX-Lab использует свою светлую палитру.</p><div className={styles.tokens}>{grouped.map(row=>{
    const token=manifest.tokens.find(t=>t.css===row.name);
    const color=token?.type==='COLOR'||row.values.some(value=>/^#|^rgb/.test(value));
    return <article className={styles.token} key={row.name} data-token={row.name}><strong>{names.get(row.name)||row.name}</strong><code>{row.name}</code>{color?<div className={styles.swatch} style={{background:`var(${row.name})`}}/>:null}<div>{row.values.map(value=><p key={value}><code>{value}</code></p>)}</div>{token?<small>{token.collection}{token.external?' · внешняя зависимость':''}</small>:null}</article>;
  })}</div></section>;
}
/** Все переменные берутся из файлов действующей React-базы. */
const meta={title:'Foundation/Tokens and typography',id:'foundation',component:TokenCatalog,tags:['autodocs'],argTypes:{kind:{control:'inline-radio',options:['Primitive','Semantic','Typography']}},render:(args,context)=><TokenCatalog {...args} colorMode={context.globals.colorMode} typeScale={context.globals.typeScale}/>,parameters:{layout:'padded'}} satisfies Meta<typeof TokenCatalog>;
export default meta;
type Story=StoryObj<typeof meta>;
/** Все глобальные значения. */
export const Primitive:Story={args:{kind:'Primitive'}};
/** Все смысловые значения и их связи. */
export const Semantic:Story={args:{kind:'Semantic'}};
/** Каждый исходный Text Style. */
export const Typography:Story={args:{kind:'Typography'}};
