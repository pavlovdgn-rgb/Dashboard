import { chromium, expect } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[],results=[];
page.on('pageerror',error=>errors.push(error.message));
try {
  await page.goto('http://127.0.0.1:6006/iframe.html?id=ds-153-1605--default&viewMode=story');
  const table=page.getByRole('table',{name:'Участники исследования',exact:true});
  const card=page.locator('[data-component-id="153:1605"] section').first();
  const pager=page.getByRole('navigation',{name:'Страницы таблицы'});
  await expect(table.locator('tbody tr')).toHaveCount(4);await page.evaluate(()=>document.fonts.ready);
  const geometry=async()=>({card:await card.boundingBox(),surface:await table.locator('..').boundingBox(),pager:await pager.boundingBox(),columns:await table.locator('th').evaluateAll(es=>es.map(e=>({x:e.getBoundingClientRect().x,width:e.getBoundingClientRect().width}))),filters:await page.getByRole('button',{name:/^(Исход задания|Полнота данных)$/}).evaluateAll(es=>es.map(e=>({x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y,width:e.getBoundingClientRect().width,height:e.getBoundingClientRect().height})))});
  const initial=await geometry();
  const searchBox=await page.getByRole('textbox',{name:'Поиск по ID'}).boundingBox();
  for(const filter of initial.filters){expect(filter.height).toBe(searchBox.height);expect(filter.y).toBe(searchBox.y);}
  results.push('Search and filter buttons have equal heights and aligned top edges');
  const stable=async label=>{expect(await geometry(),label).toEqual(initial);results.push(label);};
  await page.getByRole('button',{name:'Следующая страница',exact:true}).click();await expect(table.locator('tbody tr').first().locator('td').first()).toHaveText('001');await stable('Next page: card, columns, filters and pager remain fixed');
  const search=page.getByRole('textbox',{name:'Поиск по ID'});
  await search.fill('00');await expect(table.locator('tbody tr')).toHaveCount(4);await stable('Search results');
  await page.getByRole('button',{name:'Следующая страница',exact:true}).click();await page.getByRole('button',{name:'Следующая страница',exact:true}).click();await expect(table.locator('tbody tr')).toHaveCount(1);await stable('Last page with fewer rows');
  await search.fill('018');await expect(table.locator('tbody tr')).toHaveCount(1);await stable('One result');
  await search.fill('no-match');await expect(page.getByRole('heading',{name:'Ничего не найдено'})).toBeVisible();await stable('Empty result keeps table header and pager');
  for(const button of await pager.getByRole('button').all())await expect(button).toBeDisabled();
  await page.screenshot({path:'.tmp/storybook/participants-stable-empty.png',animations:'disabled'});
  await page.getByRole('button',{name:'Сбросить фильтры'}).click();
  await page.getByRole('button',{name:'Исход задания',exact:true}).click();await page.getByRole('menuitemradio',{name:'Цель не достигнута',exact:true}).click();await stable('Long filter label');
  await page.getByRole('button',{name:'Полнота данных',exact:true}).click();await page.getByRole('menuitemradio',{name:'Неполные',exact:true}).click();await expect(page.getByRole('heading',{name:'Ничего не найдено'})).toBeVisible();await stable('Combined filters with no matches');
  await page.getByRole('button',{name:'Сбросить фильтры'}).click();await stable('Reset');
  await page.screenshot({path:'.tmp/storybook/participants-stable.png',animations:'disabled'});
  await page.setViewportSize({width:390,height:844});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
  results.push('Mobile: table scroll is confined to its surface');
  if(errors.length)throw new Error(errors.join('\n'));
}catch(error){errors.push(error.message);process.exitCode=1;}
finally{await writeFile('.tmp/storybook/participants-layout-audit.json',JSON.stringify({results,errors},null,2));console.log(JSON.stringify({results,errors}));await browser.close();}
