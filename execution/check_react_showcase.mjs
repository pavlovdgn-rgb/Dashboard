import { chromium } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';

const only=process.argv[2];
const catalog=JSON.parse(await readFile('src/components/catalog.json','utf8')).filter(entry=>!only||only.split(',').includes(entry.id));
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const logs=[];let current='';
page.on('pageerror',error=>logs.push({component:current,type:'pageerror',message:error.message}));
page.on('console',message=>{if(message.type()==='error'||message.type()==='warning')logs.push({component:current,type:message.type(),message:message.text()});});
await page.goto('http://127.0.0.1:5173/');
const failures=[];let variantCount=0;
for(const [i,entry] of catalog.entries()){
  current=entry.name;
  await page.locator(`[data-catalog-select="${entry.id}"]`).click();
  await page.locator(`[data-current-component="${entry.id}"]`).waitFor();
  await page.waitForTimeout(40);
  for(let batch=0;batch<Math.ceil(entry.variants.length/8);batch++){
    if(batch>0){await page.getByRole('button',{name:'Следующие варианты',exact:true}).click();await page.waitForTimeout(30);}
    const errors=await page.locator('[data-render-error]').allTextContents();
    if(errors.length)failures.push({id:entry.id,name:entry.name,batch,errors:[...new Set(errors)]});
    variantCount+=Math.min(8,entry.variants.length-batch*8);
  }
  if(i%25===0)console.log(`Checked ${i+1}/${catalog.length}`);
}
await writeFile(`.tmp/react-base/render-audit${only?'-'+only.replaceAll(':','-').replaceAll(',','_'):''}.json`,JSON.stringify({count:catalog.length,variantCount,failures,logs},null,2));
console.log(JSON.stringify({count:catalog.length,variantCount,failures,logCount:logs.length}));
await browser.close();
if(failures.length||logs.length)process.exitCode=1;
