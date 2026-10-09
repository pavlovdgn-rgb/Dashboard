import assert from 'node:assert/strict';
import {chromium,expect} from '@playwright/test';

// Run only against a disposable API database started on port 5174.
const api=process.env.ROUND_TEST_API;
if(api!=='http://127.0.0.1:5174')throw Error('ROUND_TEST_API must point to the disposable local API on port 5174');
const post=async(path,data)=>{
  const response=await fetch(api+path,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  if(!response.ok)throw Error(`${response.status}: ${await response.text()}`);
  return response.json();
};
const read=async(path)=>(await fetch(api+path)).json();
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
  const study=await post('/api/project/studies',{studyTitle:'Проверка сайдбара'});
  await post('/api/project/config?study='+study.studyId,{enabled:true});
  await post('/api/project/visit',{id:'round-ui-'+study.studyId,study:study.studyId,session:'tester',
    page:'leed-dashboard',timestamp:Date.now(),vw:1280,vh:900,context:{signature:'1234567890abcdef',scrolls:[]}});
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  const errors=[];page.on('pageerror',error=>errors.push(error.message));
  await page.goto('http://127.0.0.1:5173/#/overview?device=all&study='+study.studyId);
  const footer=page.locator('section[aria-label="Состояние сбора и раунда"]');
  await expect(footer.getByText('сбор подключён')).toBeVisible();
  await expect(footer.getByText('раунд 1 · 1 респ.')).toBeVisible();
  await expect(footer.getByRole('button',{name:'Обновить'})).toBeVisible();
  await expect(footer.getByRole('button',{name:'Зафиксировать раунд'})).toBeEnabled();
  const box=await footer.boundingBox();
  assert.ok(box&&box.y+box.height<=900&&box.y+box.height>=870,'Footer should stay at the bottom of the sidebar');
  await page.screenshot({path:'.tmp/round-sidebar-before.png'});
  await footer.getByRole('button',{name:'Зафиксировать раунд'}).click();
  const modal=page.getByRole('dialog');
  await expect(modal).toContainText('отдельной ссылкой');
  await modal.getByRole('button',{name:'Зафиксировать раунд'}).click();
  await expect(page).toHaveURL(/#\/launch\?/);
  await expect(page.locator('nav button[data-selected="true"]')).toHaveCount(1);
  const next=new URLSearchParams(page.url().split('?')[1]).get('study');
  assert.ok(next&&next!==study.studyId);
  await expect(footer.getByText('раунд не начат · 0 респ.')).toBeVisible();
  assert.equal((await read('/api/project?study='+next)).total.sessions,0);
  assert.equal((await read('/api/project?study='+study.studyId)).total.sessions,1);
  await page.screenshot({path:'.tmp/round-sidebar-after.png'});
  assert.deepEqual(errors,[]);
  console.log('PASS sidebar status, bottom placement, confirmation, new link and empty round');
}finally{await browser.close();}
