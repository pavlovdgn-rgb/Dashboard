import { chromium, expect } from '@playwright/test';
import { writeFile } from 'node:fs/promises';

const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
page.setDefaultTimeout(10000);
const errors=[];page.on('pageerror',error=>errors.push(error.message));
const results=[];
async function select(id){await page.goto(`http://127.0.0.1:5173/?component=${id}`);return page.locator('main section').first();}
try {
  const table=await select('153:1605');
  const rows=()=>table.locator('tbody tr');
  await expect(rows().first().locator('td').first()).toHaveText('014');
  await table.getByRole('button',{name:'Следующая страница',exact:true}).click();
  await expect(rows().first().locator('td').first()).toHaveText('001');
  await table.getByRole('button',{name:'Исход задания',exact:true}).click();
  await page.getByRole('menuitemradio',{name:'Цель достигнута',exact:true}).click();
  await expect(rows()).toHaveCount(4);
  await expect(table.getByLabel('Предыдущая страница',{exact:true})).toBeDisabled();
  await table.getByRole('button',{name:'Полнота данных',exact:true}).click();
  await page.getByRole('menuitemradio',{name:'Неполные',exact:true}).click();
  await expect(table.getByRole('heading',{name:'Ничего не найдено',exact:true})).toBeVisible();
  await table.getByRole('button',{name:'Сбросить фильтры',exact:true}).click();
  await table.getByRole('textbox',{name:'Поиск по ID'}).fill('018');
  await expect(rows()).toHaveCount(1);
  await expect(rows().first().locator('td').first()).toHaveText('018');
  await expect(table.getByRole('button',{name:'Следующая страница',exact:true})).toBeDisabled();
  results.push('Table: distinct pages, combined filters, empty state, reset, search and page boundaries');

  const checkbox=await select('282:2918');
  await checkbox.getByRole('combobox',{name:/^Value/}).selectOption('Mixed');
  await expect(checkbox.getByRole('checkbox')).toHaveJSProperty('indeterminate',true);
  await checkbox.getByRole('checkbox').click();
  await expect(checkbox.getByRole('checkbox')).toBeChecked();
  await checkbox.getByRole('checkbox').press('Space');
  await expect(checkbox.getByRole('checkbox')).not.toBeChecked();
  await expect(checkbox.getByRole('checkbox')).toHaveJSProperty('indeterminate',false);
  await checkbox.getByRole('combobox',{name:/^Value/}).selectOption('On');
  await expect(checkbox.getByRole('checkbox')).toBeChecked();
  await checkbox.getByRole('combobox',{name:/^State/}).selectOption('Disabled');
  await expect(checkbox.getByRole('checkbox')).toBeDisabled();
  results.push('Checkbox: Mixed → On → Off, keyboard, prop changes, Disabled');

  await select('125:450');
  const result=page.getByRole('heading',{name:'Выбор результата и переход дальше'}).locator('..');
  await expect(result.getByRole('button',{name:'Далее',exact:true})).toBeDisabled();
  await result.getByRole('radio',{name:'Не удалось выполнить'}).check();
  await expect(result.getByRole('button',{name:'Далее',exact:true})).toBeEnabled();
  await result.getByRole('radio',{name:'Не удалось выполнить'}).press('ArrowUp');
  await expect(result.getByRole('radio',{name:'Выполнил задание'})).toBeChecked();
  await expect(result.getByRole('radio',{name:'Не удалось выполнить'})).not.toBeChecked();
  await result.getByRole('button',{name:'Далее',exact:true}).click();
  await expect(result.getByRole('status')).toBeVisible();
  await result.screenshot({path:'.tmp/react-base/task-result-control.png'});
  results.push('Result: equal radio options, keyboard, exclusive choice, disabled Next, submission');
  await page.screenshot({path:'.tmp/react-base/showcase-current.png',fullPage:false});
  await page.setViewportSize({width:390,height:844});
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth)).toBe(true);
  results.push('Showcase: no document overflow at 390px');
  await writeFile('.tmp/react-base/interaction-audit.json',JSON.stringify({results,errors},null,2));
  console.log(JSON.stringify({results,errors}));
} finally {await browser.close();}
