import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
const api=process.env.PILOT_TEST_API,site=process.env.PILOT_TEST_SITE,connection=JSON.parse(process.env.PILOT_TEST_CONNECTION);
const browser=await chromium.launch({channel:'chrome',headless:true});
const context=await browser.newContext({viewport:{width:1440,height:1000}});
const errors=[];context.on('page',page=>page.on('pageerror',error=>errors.push(error.message)));
const request=async(path,body)=>{const response=await fetch(api+path,{headers:{Origin:'http://127.0.0.1:5173','Content-Type':'application/json'},...(body===undefined?{}:{method:'POST',body:JSON.stringify(body)})});assert.equal(response.status,200,await response.clone().text());return response.json();};
const results=()=>request('/api/results?project='+connection.id);
await fs.mkdir('.tmp/integration-pilot',{recursive:true});
try{
  const page=await context.newPage();await page.goto(site+'/');await page.waitForTimeout(600);
  await page.getByRole('button',{name:'Следующий экран'}).click();assert.equal((await results()).total.events,0,'No participant link: no collection');
  await page.goto(site+'/?ux_study='+connection.study);
  await expect.poll(async()=>(await results()).total.events).toBe(1);
  // Simulate a lost acknowledgement after committing the event. Retry must deduplicate.
  let lost=false;
  await page.route(api+'/api/events?*',async route=>{if(!lost){lost=true;await route.fetch();await route.abort();}else await route.continue();});
  await page.getByRole('button',{name:'Следующий экран'}).click();
  await expect.poll(async()=>(await results()).total.events).toBe(3);
  await page.waitForTimeout(2000);assert.equal((await results()).total.events,3);
  let events=(await results()).events;
  const click=events.find(event=>!event.kind);assert.equal(click.page,'demo-home');assert.equal(click.target,'next-screen');assert.ok(click.x>0&&click.x<1);
  assert.ok(events.some(event=>event.kind==='visit'&&event.page==='demo-details'));
  const session=click.session;
  await page.getByPlaceholder('Тестовое значение').fill('SECRET-DO-NOT-COLLECT');await page.getByPlaceholder('Тестовое значение').click();
  await page.waitForTimeout(300);assert.equal((await results()).total.events,3);assert.ok(!JSON.stringify(await results()).includes('SECRET'));
  // Loading the same snippet twice must not install a second collector.
  await page.addScriptTag({url:api+'/sdk.js'});
  await page.evaluate(async config=>{await window.UXLabSDK.start(config);},{project:connection.id,api});
  await page.getByRole('button',{name:'Следующий экран'}).click();await expect.poll(async()=>(await results()).total.events).toBe(5);
  await page.reload();await expect.poll(async()=>(await results()).total.events).toBe(6);assert.equal((await results()).total.sessions,1);assert.ok((await results()).events.every(event=>event.session===session));
  await request('/api/policy',{project:connection.id,enabled:false});await page.waitForTimeout(2600);
  await page.getByRole('button',{name:'Следующий экран'}).click();await page.waitForTimeout(300);assert.equal((await results()).total.events,6);
  await request('/api/policy',{project:connection.id,enabled:true});await expect.poll(async()=>(await results()).total.events).toBe(7);
  const second=await context.newPage();await second.goto(site+'/?ux_study='+connection.study);await expect.poll(async()=>(await results()).total.sessions).toBe(2);
  const dashboard=await context.newPage();
  await dashboard.route('http://127.0.0.1:5176/**',async route=>{await route.fulfill({response:await route.fetch({url:route.request().url().replace('http://127.0.0.1:5176',api)})});});
  await dashboard.goto('http://127.0.0.1:5173/?screen=connections&connection='+connection.id);
  await expect(dashboard.getByRole('table',{name:'События подключения'})).toContainText('demo-home');
  await dashboard.screenshot({path:'.tmp/integration-pilot/web-desktop.png',fullPage:true});
  await dashboard.setViewportSize({width:390,height:844});
  assert.ok(await dashboard.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),'No mobile overflow');
  await dashboard.screenshot({path:'.tmp/integration-pilot/web-mobile.png',fullPage:true});
  await dashboard.setViewportSize({width:1440,height:1000});
  // Contract fixtures, explicitly not a live Figma integration test.
  const adapter=await dashboard.evaluate(async()=>{
    const {embedURL,figmaEvent}=await import('/src/connections/figma.ts');
    const frame=document.createElement('iframe');document.body.append(frame);const source=frame.contentWindow;
    const message={type:'PRESENTED_NODE_CHANGED',data:{presentedNodeId:'1:2',isStoredInHistory:true}};
    const received=(origin,from,data=message)=>figmaEvent(new MessageEvent('message',{origin,source:from,data}),source);
    const result={good:received('https://www.figma.com',source),wrongOrigin:received('https://evil.example',source),wrongSource:received('https://www.figma.com',window),invalid:received('https://www.figma.com',source,{type:'PRESENTED_NODE_CHANGED',data:{presentedNodeId:123}}),url:embedURL('https://www.figma.com/proto/Example/Test?node-id=1-2&t=private','test-client')};frame.remove();return result;
  });
  assert.equal(adapter.good.page,'1:2');assert.equal(adapter.wrongOrigin,null);assert.equal(adapter.wrongSource,null);assert.equal(adapter.invalid,null);assert.ok(!adapter.url.includes('private'));assert.ok(adapter.url.includes('client-id=test-client'));
  await dashboard.getByRole('button',{name:'Тип интерфейса',exact:true}).click();await dashboard.getByRole('menuitemradio',{name:'Прототип Figma',exact:true}).click();
  await dashboard.getByLabel('Название подключения',{exact:true}).fill('Figma · тест контракта');
  await dashboard.getByLabel('Ссылка на Figma-прототип',{exact:true}).fill('https://www.figma.com/proto/Example/Test?node-id=1-2');
  await dashboard.getByLabel('Client ID приложения Figma',{exact:true}).fill('test-client');
  await dashboard.getByRole('button',{name:'Создать подключение',exact:true}).click();
  await expect(dashboard.getByRole('heading',{name:'Figma · тест контракта',exact:true})).toBeVisible();
  // Replace the remote frame only in this isolated test; no claim of live Figma events.
  await dashboard.route('https://embed.figma.com/**',route=>route.fulfill({contentType:'text/html',body:'<!doctype html><p>Тестовая замена iframe, не настоящий прототип Figma</p>'}));
  await dashboard.getByRole('button',{name:'Открыть прототип для проверки'}).click();
  await expect(dashboard.getByTitle('Тестируемый прототип Figma')).toBeVisible();
  await dashboard.evaluate(()=>{const source=document.querySelector('iframe[title="Тестируемый прототип Figma"]').contentWindow;for(const data of [{type:'INITIAL_LOAD',data:{}},{type:'PRESENTED_NODE_CHANGED',data:{presentedNodeId:'1:2',isStoredInHistory:true}}])window.dispatchEvent(new MessageEvent('message',{origin:'https://www.figma.com',source,data}));});
  await expect(dashboard.getByRole('table',{name:'События подключения'})).toContainText('Переход на экран');
  await expect(dashboard.getByRole('button',{name:'Начать заново'})).toBeEnabled();
  await dashboard.screenshot({path:'.tmp/integration-pilot/figma-contract-fixture.png',fullPage:true});
  assert.deepEqual(errors,[]);
  await fs.writeFile('.tmp/integration-pilot/result.json',JSON.stringify({web:'PASS: standalone snippet, opt-in, SPA, reload, private fields, lost acknowledgement, duplicate script, pause/resume, tab isolation, desktop/mobile',figma:'PASS: URL and message contract fixtures, origin/source rejection, UI delivery; live prototype NOT tested',errors},null,2));
  console.log('PASS standalone SDK + isolated persistence + Figma contract fixtures (not live Figma).');
}finally{await browser.close();}
