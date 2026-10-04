import {chromium,expect} from '@playwright/test';
import assert from 'node:assert/strict';
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
 const page=await browser.newPage({viewport:{width:1600,height:1050}});
 const live=await(await fetch('http://127.0.0.1:5174/api/project?device=all')).json();
 await page.route('**/api/project?*',r=>r.fulfill({json:live}));
 let release,requests=[];
 const report={...live,id:'test-report',createdAt:Date.now(),device:'mobile',findings:[]};await page.route('**/api/project/reports**',async r=>{if(r.request().method()==='GET'){await r.fulfill({json:{reports:[]}});return;}requests.push(r.request().postDataJSON());await new Promise(resolve=>release=resolve);await r.fulfill({json:report});});await page.route('**/api/project/report?*',r=>r.fulfill({json:report}));
 await page.goto('http://127.0.0.1:5173/#/overview');
 const device=page.getByRole('button',{name:'Размер экрана',exact:true});
 await expect(device).toBeVisible();const initial=await device.boundingBox();
 const toolbar=page.locator('[class*="toolbar"]');const status=toolbar.locator('>span');const statusBox=await status.boundingBox();
 for(const label of ['От 768 px','До 768 px','Все размеры экрана']){
   await device.click();const option=page.getByRole('menuitemradio',{name:label,exact:true});
   await expect(option).toBeVisible();assert.ok((await option.boundingBox()).height<48,'Menu label must fit on one line');
   await option.click();const current=await device.boundingBox();assert.equal(current.width,initial.width);assert.equal(current.height,initial.height);
   assert.equal((await status.boundingBox()).x,statusBox.x);
 }
 await page.screenshot({path:'.tmp/stable-device-filter.png'});
 await page.goto('http://127.0.0.1:5173/#/report?device=mobile');
 const generate=page.getByRole('button',{name:'Создать отчёт',exact:true});await expect(generate).toBeEnabled();
 assert.equal((await generate.boundingBox()).height,56);await expect(generate.locator('svg')).toHaveCount(1);
 await expect(page.getByRole('button',{name:'Обновить',exact:true})).toHaveCount(0);
 const h=await page.getByRole('heading',{name:'Отчёты',exact:true}).boundingBox();assert.ok(Math.abs((await generate.boundingBox()).y-h.y)<40);
 await generate.click();const submit=page.getByRole('button',{name:'Сформировать PDF',exact:true});await submit.click();await expect(submit).toBeDisabled();await expect.poll(()=>requests.length).toBe(1);assert.equal(requests[0].device,'mobile');release();
 await expect(page.getByRole('button',{name:'Скачать PDF',exact:true})).toBeVisible();
 await page.screenshot({path:'.tmp/report-header.png'});
 await page.goto('http://127.0.0.1:5173/#/heatmap');await expect(page.locator('[data-background="saved"]')).toBeVisible();
 await page.locator('[data-background="saved"]').screenshot({path:'.tmp/heatmap-context.jpg',type:'jpeg',quality:40});
 await page.setViewportSize({width:760,height:1000});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 console.log('PASS fixed-width dropdown, one-line options, stable status, report header action/icon/56px, mocked generation, narrow heatmap');
} finally {await browser.close();}
