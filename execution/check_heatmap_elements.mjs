import { chromium,expect } from '@playwright/test';
const study=`leed-verify-names-${Date.now()}`,api='http://127.0.0.1:5174/api/heatmap';
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  const context=await browser.newContext({viewport:{width:1440,height:900}});
  const target=await context.newPage();
  await target.goto(`http://127.0.0.1:5175/leads-table?ux_study=${study}`);
  await target.waitForFunction(()=>window.__uxLabStatus?.session);
  const search=target.getByPlaceholder('Найти лида');await search.click();
  await search.fill('PRIVATE-VALUE-92814');await search.fill('');
  await target.getByRole('button',{name:'Новый лид',exact:true}).click();
  await expect.poll(async()=>{
    const data=await (await fetch(`${api}?study=${study}&aggregation=page`)).json();return data.total.clicks;
  }).toBe(2);
  const groups=await (await fetch(`${api}?study=${study}&aggregation=page`)).json();
  const data=await (await fetch(`${api}?study=${study}&aggregation=page&group=${groups.groups[0].layout}`)).json();
  expect(data.points.map(point=>point.element?.label)).toEqual(expect.arrayContaining(['Поле «Найти лида»','Кнопка «Новый лид»']));
  expect(JSON.stringify(data)).not.toContain('PRIVATE-VALUE');
  const page=await context.newPage();
  await page.route('**/api/heatmap?*',async route=>{const url=new URL(route.request().url());url.searchParams.set('study',study);await route.fulfill({response:await route.fetch({url:url.href})});});
  await page.goto(`http://127.0.0.1:5173/?screen=results-overview#/heatmap-live?link=${study}`);
  const table=page.getByRole('table',{name:'Собранные клики по элементам'});
  const link=table.getByRole('button',{name:'Кнопка «Новый лид»',exact:true});
  await link.hover();
  await expect(page.getByTestId('heatmap-element-highlight').locator('rect')).toHaveCount(1);
  const row=link.locator('xpath=ancestor::tr');
  expect((await row.boundingBox()).height).toBeLessThanOrEqual(42);
  await link.click();await expect(page.getByTestId('real-click-count')).toContainText('1 кликов');
  await page.getByRole('button',{name:'Показать все клики',exact:true}).click();
  await expect(page.getByTestId('real-click-count')).toContainText('2 кликов');
  await expect(page.getByTestId('heatmap-element-highlight')).toHaveCount(0);
  await page.screenshot({path:'.tmp/heatmap/element-names.png',fullPage:true});
  console.log(JSON.stringify({study,labels:true,hoverBounds:true,filter:true,compactRows:true}));
}finally{await browser.close();}
