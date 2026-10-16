/** Verify study duplication through the built UI and an isolated real API. */
import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';

const api=process.env.LIVE_TEST_API;
if(!api?.startsWith('http://127.0.0.1:'))throw Error('An explicit isolated local API is required');
const output=new URL('../.tmp/duplicate-study/',import.meta.url);await mkdir(output,{recursive:true});
const auth=await fetch(api+'/api/auth',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({password:'test-password-cloud-123'})});
assert.equal(auth.status,200);const cookie=auth.headers.get('set-cookie').split(';')[0];
async function request(path,data){
 const response=await fetch(api+path,{headers:{Cookie:cookie,'Content-Type':'application/json'},...(data===undefined?{}:{method:'POST',body:JSON.stringify(data)})});
 assert.ok(response.ok,await response.clone().text());return response.json();
}
const template=await request('/api/project/config?study=biletberu-retest-2026-10-15');
let source=await request('/api/project/studies',{studyTitle:'Проверка дублирования '+crypto.randomUUID().slice(0,8)});
source=await request('/api/project/config?study='+source.studyId,{
 mode:'scenario',tasks:template.tasks.map(({revision,...task})=>task),enabled:true,
 collectClicks:false,collectVisits:true,recordingMode:'video',allowVideo:false,funnel:['bb-main','bb-done']
});
await request('/api/project/visit',{id:crypto.randomUUID(),study:source.studyId,session:'original-visit',page:'bb-main',timestamp:Date.now(),vw:393,vh:812,context:{signature:'1234567890abcdef',scrolls:[]}});

const browser=await chromium.launch({channel:'chrome',headless:true});const errors=[];
try{
 const context=await browser.newContext({viewport:{width:1440,height:1100}});
 await context.addCookies([{name:'uxlab_session',value:cookie.slice(cookie.indexOf('=')+1),url:api}]);
 const page=await context.newPage();page.on('pageerror',error=>errors.push(error.message));
 let fail=true,requests=0;
 await page.route('**/api/project/studies/duplicate*',async route=>{
  requests++;
  if(fail)return route.fulfill({status:503,contentType:'application/json',body:JSON.stringify({error:'Не удалось создать копию. Повторите попытку.'})});
  await new Promise(resolve=>setTimeout(resolve,400));await route.continue();
 });
 await page.goto(api+'/#/studies?study='+source.studyId);
 const actions=()=>page.getByRole('button',{name:`Действия с исследованием «${source.studyTitle}»`,exact:true});
 await actions().click();
 const menu=page.getByRole('menu',{name:`Действия с исследованием «${source.studyTitle}»`,exact:true});
 await expect(menu.getByRole('menuitem')).toHaveText(['Дублировать','Удалить']);
 await expect(menu).toBeVisible();await page.screenshot({path:new URL('menu.png',output).pathname,animations:'disabled'});
 await menu.getByRole('menuitem',{name:'Дублировать',exact:true}).click();
 await expect(page.getByRole('alert')).toContainText('Не удалось создать копию');await expect(menu).not.toBeVisible();
 const before=(await request('/api/project/studies')).studies.length;
 fail=false;await actions().click();
 const copied=page.waitForResponse(response=>response.url().includes('/api/project/studies/duplicate')&&response.status()===200);
 await page.getByRole('menuitem',{name:'Дублировать',exact:true}).click();
 await expect(actions()).toBeDisabled();await expect(actions()).toHaveAttribute('aria-busy','true');
 const copy=await (await copied).json();
 await expect(page).toHaveURL(new RegExp('/setup\\?.*study='+copy.studyId));
 await expect(page.getByLabel('Название исследования',{exact:true})).toHaveValue(source.studyTitle+' — копия');
 await expect(page.getByLabel('Название задания',{exact:true})).toHaveCount(6);
 for(let i=0;i<6;i++)await expect(page.getByLabel('Название задания',{exact:true}).nth(i)).toHaveValue(source.tasks[i].title);
 assert.deepEqual(copy.tasks,source.tasks);assert.equal(copy.enabled,source.enabled);
 assert.equal((await request('/api/project/studies')).studies.length,before+1);assert.equal(requests,2,'One failed request and one successful copy');
 await page.screenshot({path:new URL('copy-settings.png',output).pathname});
 await page.goto(api+'/#/studies?study='+copy.studyId);
 const row=page.getByRole('row').filter({has:page.getByRole('button',{name:copy.studyTitle,exact:true})});
 await expect(row.getByRole('cell').nth(2)).toHaveText('0');
 await page.getByRole('button',{name:`Действия с исследованием «${copy.studyTitle}»`,exact:true}).click();
 await page.getByRole('menuitem',{name:'Удалить',exact:true}).click();
 const confirm=page.getByRole('dialog',{name:'Удалить исследование?',exact:true});
 await expect(confirm).toContainText(copy.studyTitle);
 await confirm.getByRole('button',{name:'Отмена',exact:true}).click();
 await expect(row).toBeVisible();
 assert.equal((await request('/api/project/config?study='+source.studyId)).studyTitle,source.studyTitle);
 assert.equal((await request('/api/project?study='+source.studyId)).total.sessions,1);
 assert.equal((await request('/api/project?study='+copy.studyId)).total.sessions,0);
 assert.deepEqual(errors,[]);
 await writeFile(new URL('result.json',output),JSON.stringify({menu:true,copySettings:true,sixTasks:true,ownLink:true,emptyResults:true,originalPreserved:true,errorRetry:true,busyGuard:true,deleteConfirmationPreserved:true},null,2));
 console.log('PASS duplicate from study menu, all settings and six tasks, own link, zero sessions, error retry, busy state and original study preserved.');
}finally{await browser.close();}
