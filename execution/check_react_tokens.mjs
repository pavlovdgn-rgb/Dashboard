import { chromium } from '@playwright/test';
import { readFile,writeFile } from 'node:fs/promises';
const manifest=JSON.parse(await readFile('src/tokens/manifest.json','utf8'));
const source=JSON.parse(await readFile('ds/index.json','utf8'));
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage();
const errors=[];page.on('pageerror',error=>errors.push(error.message));
try {
  await page.goto('http://127.0.0.1:5173/?tab=typography');
  const tokenFailures=[];
  for(const color of ['Light','Dark'])for(const scale of ['Medium','Small','X-small']){
    const results=await page.evaluate(({color,scale,tokens})=>{
      document.documentElement.dataset.colorMode=color.toLowerCase();document.documentElement.dataset.typeScale=scale.toLowerCase();
      const styles=getComputedStyle(document.documentElement);
      return tokens.map(token=>({id:token.id,value:styles.getPropertyValue(token.css).trim()}));
    },{color,scale,tokens:manifest.tokens});
    for(const [index,result] of results.entries()){
      const token=manifest.tokens[index];
      const expected=token.values[color]??token.values[scale]??Object.values(token.values)[0];
      if(result.value!==expected)tokenFailures.push({name:token.name,color,scale,expected,actual:result.value});
    }
  }
  const fonts=await page.evaluate(async styles=>{
    const unique=[...new Map(styles.map(style=>[style.font.family+style.font.style,style])).values()];
    return await Promise.all(unique.map(async style=>{
      const weight=style.font.variationSettings?.wght??(style.font.style.includes('Bold')?700:400);
      const query=`${style.font.style==='Italic'?'italic ':''}${weight} ${style.size}px "${style.font.family}"`;
      const faces=await document.fonts.load(query,'Исследование Research 0123');
      return {query,loaded:faces.length>0};
    }));
  },source.textStyles);
  const report={tokenCount:manifest.tokens.length,modeCombinations:6,tokenFailures,fonts,errors};
  await writeFile('.tmp/react-base/token-audit.json',JSON.stringify(report,null,2));
  console.log(JSON.stringify(report));
  if(tokenFailures.length||fonts.some(font=>!font.loaded)||errors.length)process.exitCode=1;
}finally{await browser.close();}
