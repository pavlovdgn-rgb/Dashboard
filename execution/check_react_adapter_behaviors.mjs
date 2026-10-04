import { chromium, expect } from '@playwright/test';
import { readFile, writeFile } from 'node:fs/promises';

const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1000}});
const errors=[];const results=[];
page.on('pageerror',error=>errors.push(error.message));
const select=async id=>{await page.goto(`http://127.0.0.1:5173/?component=${id}`);return page.locator('main section').first();};
try {
  const scenario=await select('136:715');
  const rows=scenario.locator('tbody tr');
  await expect(rows).toHaveCount(3);
  await rows.nth(2).getByRole('radio').check();
  await expect(rows.nth(2).getByRole('radio')).toBeChecked();
  await expect(rows.nth(0).getByRole('radio')).not.toBeChecked();
  await expect(scenario.getByText('Выбран сценарий: Оформить заказ',{exact:true})).toBeVisible();
  await expect(rows.nth(2).getByRole('progressbar')).toHaveAttribute('aria-valuenow','67');
  const radio=await rows.first().getByRole('radio').boundingBox();
  const title=await rows.first().locator('strong').boundingBox();
  if(!radio||!title||title.x<=radio.x||Math.abs(title.y-radio.y)>20)throw new Error('Scenario radio and title lost horizontal layout');
  await scenario.getByRole('combobox',{name:'State',exact:true}).selectOption('OverviewUnselected');
  await expect(scenario.locator('input:checked')).toHaveCount(0);
  await scenario.getByRole('combobox',{name:'State',exact:true}).selectOption('Error');
  await scenario.getByRole('button',{name:'Повторить загрузку'}).click();
  await expect(scenario.locator('tbody tr')).toHaveCount(3);
  results.push('Scenario: exclusive selection, matching totals, variant reset, retry, horizontal radio layout');

  const choice=await select('260:3028');
  await choice.getByRole('radio').check();
  await expect(choice.getByText('Выбрано',{exact:true})).toBeVisible();
  await choice.getByRole('combobox',{name:'State',exact:true}).selectOption('Disabled');
  await expect(choice.getByRole('radio')).toBeDisabled();
  results.push('Choice card: selection indicator and disabled state');

  const metric=await select('132:574');
  await metric.getByRole('combobox',{name:'Data',exact:true}).selectOption('NoData');
  await expect(metric.getByRole('progressbar')).toHaveCount(0);
  await metric.getByRole('combobox',{name:'Data',exact:true}).selectOption('Zero');
  await expect(metric.getByRole('progressbar')).toHaveAttribute('aria-valuenow','0');
  results.push('Success metric: missing data is distinct from zero');

  const footer=await select('20307:328531');
  await expect(footer.getByRole('button',{name:'Применить',exact:true})).toBeEnabled();
  await footer.getByRole('combobox',{name:'Disabled',exact:true}).selectOption('True');
  await expect(footer.getByRole('button',{name:'Применить',exact:true})).toBeDisabled();
  results.push('Date footer: independent switch and disabled action');

  const thumb=await select('14757:83542');
  await thumb.getByRole('slider').press('ArrowRight');
  await expect(thumb.getByRole('slider')).toHaveAttribute('aria-valuenow','41');
  results.push('Range thumb: keyboard updates value');

  const info=await select('16160:207356');
  await expect(info.getByRole('textbox')).toHaveCount(0);
  await expect(info.getByText('Selects have no readonly or placeholder state')).toBeVisible();
  results.push('Info box: annotation is not an editable field');

  const catalog=JSON.parse(await readFile('src/components/catalog.json','utf8'));
  const list=await select(catalog.find(entry=>entry.source==='elastic'&&entry.sourceIndex===196).id);
  await expect(list.locator('.euiToast')).toHaveCount(3);
  await list.getByRole('combobox',{name:'showClearAllButtonAt',exact:true}).selectOption('true');
  await list.getByRole('button',{name:'Очистить все',exact:true}).click();
  await expect(list.locator('.euiToast')).toHaveCount(0);
  results.push('Notifications: clear list removes all toasts');
  if(errors.length)throw new Error(errors.join('\n'));
} finally {
  await writeFile('.tmp/react-base/adapter-behavior-audit.json',JSON.stringify({results,errors},null,2));
  console.log(JSON.stringify({results,errors}));
  await browser.close();
}
