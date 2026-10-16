/** Reset through the built dashboard, including late real mobile writes and responses. */
import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';

const api=process.env.LIVE_TEST_API,app=process.env.MOBILE_TEST_APP;
if(!api?.startsWith('http://127.0.0.1:')||!app?.startsWith('http://127.0.0.1:'))throw Error('Explicit isolated local servers required');
const out=new URL('../.tmp/reset-study/',import.meta.url);await mkdir(out,{recursive:true});
const auth=await fetch(api+'/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:'test-password-cloud-123'})});
assert.equal(auth.status,200);const cookie=auth.headers.get('set-cookie').split(';')[0];
async function request(path,data){
 const response=await fetch(api+path,{headers:{Cookie:cookie,'Content-Type':'application/json'},...(data===undefined?{}:{method:'POST',body:JSON.stringify(data)})});
 assert.ok(response.ok,await response.clone().text());return response.json();
}
const template=await request('/api/project/config?study=biletberu-retest-2026-10-15');
let config=await request('/api/project/studies',{studyTitle:'Сброс перед тестом '+crypto.randomUUID().slice(0,8)});
const study=config.studyId;
config=await request('/api/project/config?study='+study,{mode:'scenario',enabled:true,collectClicks:true,collectVisits:true,
 tasks:template.tasks.map(({revision,...task})=>task),funnel:['bb-main','bb-done']});
const other=await request('/api/project/studies',{studyTitle:'Контрольное исследование'});
await request('/api/project/config?study='+other.studyId,{enabled:true});
await request('/api/project/visit',{id:crypto.randomUUID(),study:other.studyId,session:'keep-this',page:'bb-main',timestamp:Date.now(),vw:393,vh:812,context:{signature:'1234567890abcdef',scrolls:[]}});
const browser=await chromium.launch({channel:'chrome',headless:true});const errors=[];
let hold=false,release;const gate=new Promise(resolve=>{release=resolve;}),late=[];
const bridge=async route=>{
 const req=route.request(),url=new URL(req.url());
 const cors={'access-control-allow-origin':app,'access-control-allow-headers':'Content-Type,X-UXLab-Participant,X-UXLab-Collection-Version','access-control-allow-methods':'GET,POST,OPTIONS'};
 if(req.method()==='OPTIONS')return route.fulfill({status:204,headers:cors});
 const body=req.method()==='POST'?req.postDataJSON():null;
 const earlySuccess=hold&&body?.kind==='prototype_event'&&body.value==='activity_favourited';
 const delayed=hold&&req.method()==='POST';
 if(delayed&&!earlySuccess)await gate;
 const response=await fetch(api+url.pathname+url.search,{method:req.method(),headers:{Origin:'https://biletberu-mobile.vercel.app','Content-Type':'application/json','X-UXLab-Participant':req.headers()['x-uxlab-participant']||'',
  ...(req.headers()['x-uxlab-collection-version']?{'X-UXLab-Collection-Version':req.headers()['x-uxlab-collection-version']}:{})},...(req.method()==='POST'?{body:req.postDataBuffer()}: {})});
 const payload=Buffer.from(await response.arrayBuffer());
 if(earlySuccess)await gate;
 if(delayed)late.push({path:url.pathname,status:response.status,earlySuccess});
 await route.fulfill({status:response.status,headers:{...cors,'content-type':'application/json'},body:payload});
};
try{
 const mobile=await browser.newContext({viewport:{width:393,height:852},isMobile:true,hasTouch:true});
 await mobile.route('https://dashboard-woad-one-64.vercel.app/**',bridge);
 const participant=await mobile.newPage();participant.on('pageerror',error=>errors.push(error.message));
 const original=new URL(config.url),link=new URL('/app/main',app);link.search=original.search;
 const fragment=new URLSearchParams(original.hash.slice(1));fragment.set('ux_api','https://dashboard-woad-one-64.vercel.app');link.hash=fragment.toString();
 await participant.goto(link.href);await expect(participant.locator('.uxlab-study-count')).toHaveText('1/6');
 const nav=path=>participant.evaluate(path=>{history.pushState({},'',path);dispatchEvent(new PopStateEvent('popstate'));},'/app'+path);
 await nav('/activity?id=nook&event=weekend');await expect(participant.locator('.uxlab-study-count')).toHaveText('2/6');
 const oldSession=await participant.evaluate(study=>sessionStorage.getItem('uxlab-bb-session:'+study),study);
 hold=true;await participant.getByRole('button',{name:'В избранное',exact:true}).click();
 await expect(participant.locator('.uxlab-study-goal')).toHaveText('✓ Выполнено · сохраняем…');
 await expect.poll(async()=>(await request('/api/project?study='+study)).sessions[0]?.task?.succeededTasks).toBe(2);

 const dashboard=await browser.newContext({viewport:{width:1440,height:1100}});
 await dashboard.addCookies([{name:'uxlab_session',value:cookie.slice(cookie.indexOf('=')+1),url:api}]);
 const page=await dashboard.newPage();page.on('pageerror',error=>errors.push(error.message));
 await page.goto(api+'/#/setup?study='+study);
 await page.getByRole('button',{name:'Обнулить статистику',exact:true}).click();
 const modal=page.getByRole('dialog',{name:'Обнулить статистику исследования?',exact:true});
 await expect(modal).toContainText(config.studyTitle);await expect(modal).toContainText('Сбор данных будет приостановлен');
 await page.screenshot({path:new URL('confirmation.png',out).pathname,animations:'disabled'});
 await modal.getByRole('button',{name:'Отмена',exact:true}).click();await expect(modal).not.toBeVisible();
 assert.equal((await request('/api/project?study='+study)).total.sessions,1);
 let fail=true;const resetIds=[];
 await page.route('**/api/project/studies/reset*',async route=>{
  resetIds.push(route.request().postDataJSON().resetId);
  if(fail){fail=false;return route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({error:'Не удалось обнулить статистику. Повторите попытку.'})});}
  await new Promise(resolve=>setTimeout(resolve,300));await route.continue();
 });
 await page.getByRole('button',{name:'Обнулить статистику',exact:true}).click();
 await modal.getByRole('button',{name:'Обнулить статистику',exact:true}).click();await expect(modal.getByRole('alert')).toBeVisible();
 const response=page.waitForResponse(response=>response.url().includes('/api/project/studies/reset')&&response.status()===200);
 await modal.getByRole('button',{name:'Обнулить статистику',exact:true}).click();
 await expect(modal.getByRole('button',{name:'Отмена',exact:true})).toBeDisabled();
 const reset=await (await response).json();await expect(modal).not.toBeVisible();
 await expect(page.getByRole('status').filter({hasText:'Статистика обнулена.'})).toBeVisible();
 assert.equal(resetIds[0],resetIds[1],'A failed confirmation must reuse its reset ID');
 assert.deepEqual(reset.tasks,config.tasks);assert.deepEqual(reset.funnel,config.funnel);assert.equal(reset.studyId,study);assert.equal(reset.enabled,false);
 assert.equal((await request('/api/project?study='+study)).total.sessions,0);
 await expect.poll(()=>participant.evaluate(study=>sessionStorage.getItem('uxlab-bb-session:'+study+':version'),study)).toBe(reset.collectionVersion);
 await expect(participant.locator('.uxlab-study')).toHaveCount(0);
 const newSession=await participant.evaluate(study=>sessionStorage.getItem('uxlab-bb-session:'+study),study);assert.notEqual(newSession,oldSession);
 hold=false;release();
 await expect.poll(()=>late.some(item=>item.earlySuccess&&item.status===200)&&late.some(item=>item.path==='/api/heatmap/snapshots'&&item.status===409)).toBe(true);
 assert.equal(await participant.evaluate(study=>sessionStorage.getItem('uxlab-bb-session:'+study+':run'),study),null,'A late old success response must not restore the old run');
 assert.equal((await request('/api/project?study='+study)).total.sessions,0);
 assert.equal((await request('/api/project?study='+other.studyId)).total.sessions,1);
 await page.goto(api+'/#/overview?study='+study);await expect(page.getByText('Откройте «Билет Беру». Первое посещение появится здесь автоматически.',{exact:true})).toBeVisible();
 await page.screenshot({path:new URL('zero-results.png',out).pathname,animations:'disabled'});
 await nav('/main');await request('/api/project/config?study='+study,{enabled:true});
 await expect(participant.locator('.uxlab-study-count')).toHaveText('1/6',{timeout:15000});
 await nav('/activity?id=nook&event=weekend');await expect(participant.locator('.uxlab-study-count')).toHaveText('2/6');
 const fresh=await request('/api/project?study='+study);assert.equal(fresh.sessions.length,1);assert.equal(fresh.sessions[0].id,newSession);assert.equal(fresh.sessions[0].task.succeededTasks,1);
 const handoff=await browser.newContext({viewport:{width:393,height:852}});await handoff.route('https://dashboard-woad-one-64.vercel.app/**',bridge);
 const external=await handoff.newPage();external.on('pageerror',error=>errors.push(error.message));await external.goto(participant.url());
 await expect(external.locator('.uxlab-study-count')).toHaveText('2/6');
 assert.equal(await external.evaluate(study=>sessionStorage.getItem('uxlab-bb-session:'+study),study),newSession,'Browser handoff must retain the new session after a reset');
 assert.deepEqual(errors,[]);
 await writeFile(new URL('result.json',out),JSON.stringify({confirmation:true,cancelPreservesData:true,errorRetry:true,settingsAndTasksPreserved:true,zeroResults:true,otherStudyPreserved:true,oldRequestsRejected:true,lateSuccessIgnored:true,freshFirstTask:true,browserHandoff:true},null,2));
 console.log('PASS confirmed reset, zero results, unchanged tasks/settings, paused collection, stale queued writes rejected, late success ignored, clean restart and browser handoff.');
}finally{release();await browser.close();}
