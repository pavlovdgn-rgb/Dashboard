/** Render the same read-only React map at source resolution; invoked by serve_heatmap.py. */
import { chromium } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
import path from 'node:path';

let input='';for await(const chunk of process.stdin)input+=chunk;
const config=JSON.parse(input);
const api=`http://127.0.0.1:${config.port}`;
async function read(params) {
  const response=await fetch(`${api}/api/heatmap?${new URLSearchParams({study:config.study,session:config.session||'',mode:config.mode,aggregation:'page',...params})}`);
  if(!response.ok)throw Error('Click data unavailable');
  return response.json();
}
const data=await read({});
const groups=data.groups.filter(group=>group.page.startsWith('leed-')&&(!config.group||group.layout===config.group));
if(!groups.length)throw Error('No maps to export');
if(groups.length>100)throw Error('Too many maps for a single local export');
// Capture each screen/viewport once; viewport variants are deliberately not superimposed.
const maps=[];
for(const group of groups) {
  if(group.vw*group.vh>24000000)throw Error('Map resolution exceeds local export limit');
  const {points}=await read({group:group.layout});
  maps.push({group,points:config.layer===false?[]:points.filter(point=>!config.target||point.target===config.target)});
}
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  const context=await browser.newContext({deviceScaleFactor:1});
  for(const map of maps) {
    const page=await context.newPage();
    page.setDefaultTimeout(15000);page.setDefaultNavigationTimeout(20000);
    await page.setViewportSize({width:map.group.vw,height:map.group.vh});
    await page.route('**/__heatmap_export_payload',route=>route.fulfill({json:map}));
    // Support a separately configured collector port in verification environments.
    if(config.port!==5174)await page.route('http://127.0.0.1:5174/**',route=>route.continue({url:route.request().url().replace(':5174',`:${config.port}`)}));
    await page.goto('http://127.0.0.1:5173/?screen=heatmap-export',{waitUntil:'domcontentloaded'});
    await page.addStyleTag({content:'html{scrollbar-gutter:auto}body{overflow:hidden}'});
    const host=page.getByTestId('captured-heatmap');
    await host.waitFor();
    await page.waitForFunction(()=>{
      const state=document.querySelector('[data-testid="captured-heatmap"]')?.getAttribute('data-background');
      return state==='saved'||state==='fallback';
    });
    const iframe=await host.locator('iframe').elementHandle();
    const frame=await iframe.contentFrame();
    if(await host.getAttribute('data-background')==='saved')await frame.waitForURL('about:srcdoc',{waitUntil:'domcontentloaded'});
    await frame.waitForLoadState('domcontentloaded');
    if(await host.getAttribute('data-background')==='fallback') {
      await frame.locator('#root > *').first().waitFor();
      // The target demo's initial skeleton resolves after 600 ms.
      await page.waitForTimeout(900);
    }
    // The static iframe forbids scripts: timers/rAF inside it cannot be used as readiness signals.
    // Poll its resource state from the trusted parent instead, with a finite deadline.
    for(let attempt=0;attempt<40;attempt++) {
      if(await frame.evaluate(()=>document.fonts.status==='loaded'&&[...document.images].every(img=>img.complete)))break;
      await page.waitForTimeout(150);
    }
    if(!await frame.evaluate(()=>Boolean(document.body.textContent?.trim())&&[...document.images].every(img=>img.complete&&img.naturalWidth>0)))throw Error('Background is not ready for export');
    await page.waitForTimeout(100);
    const name=`${map.group.page}-${map.group.vw}x${map.group.vh}-${config.mode}${config.session?'-session-'+config.session.slice(0,8):''}.png`;
    await page.getByTestId('heatmap-export-surface').screenshot({path:path.join(config.output,name),animations:'disabled',timeout:30000});
    await page.close();
  }
  await writeFile(path.join(config.output,'manifest.json'),JSON.stringify(maps.map(({group})=>({page:group.page,width:group.vw,height:group.vh,session:config.session||null}))), 'utf8');
} finally {await browser.close();}
