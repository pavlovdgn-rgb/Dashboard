// Regression checks for the source variants corrected in the final audit.
import { chromium, expect } from '@playwright/test';
import { writeFile } from 'node:fs/promises';

const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1600,height:1100}});
const errors=[],results=[];
page.on('pageerror',e=>errors.push(e.message));
const select=async id=>{await page.goto(`http://127.0.0.1:5173/?component=${id}`);return page.locator('main section').first();};
const variant=(section,name,value)=>section.getByRole('combobox',{name,exact:true}).selectOption(value);
try {
  let s=await select('84:713');
  const seek=s.getByRole('slider',{name:'Позиция записи'});
  await expect(seek).toHaveValue('138');
  await s.getByRole('button',{name:'+5 с',exact:true}).click();
  await expect(seek).toHaveValue('143');
  await s.getByRole('button',{name:'−5 с',exact:true}).click();
  await seek.press('Home');
  await s.getByRole('button',{name:'−5 с',exact:true}).click();
  await expect(seek).toHaveValue('0');
  await seek.press('End');
  await s.getByRole('button',{name:'+5 с',exact:true}).click();
  await expect(seek).toHaveValue('272');
  await s.getByRole('button',{name:'Воспроизвести',exact:true}).click();
  await expect(s.getByRole('button',{name:'Пауза',exact:true})).toBeVisible();
  await variant(s,'Coverage','Gap');
  await expect(s.getByText('Нет данных с 01:40 до 02:05 · разрыв записи сессии')).toBeVisible();
  const track=await s.locator('[class*="timeline"]').boundingBox();
  const gap=await s.locator('[class*="gap"]').boundingBox();
  if(Math.abs(gap.width/track.width-25/272)>.002)throw new Error('Recording gap is not proportional to duration');
  results.push('Replay: keyboard, seek bounds, playback state and proportional gap');

  s=await select('14795:111805');
  await s.getByRole('button',{name:'Last 15 min',exact:true}).click();
  await expect(s.getByRole('button',{name:'Last 15 min',exact:true})).toHaveAttribute('aria-expanded','true');
  await expect(page.getByRole('group',{name:'Quick select',exact:true}).first()).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(s.getByRole('button',{name:'Last 15 min',exact:true})).toHaveAttribute('aria-expanded','false');
  results.push('Compact date picker: two controls, real popup and Escape');

  s=await select('23938:281323');
  await variant(s,'Open','true');
  await expect(s.getByRole('button',{name:'Auto refresh',exact:true})).toHaveAttribute('aria-expanded','true');
  await expect(page.getByRole('switch',{name:'Toggle refresh',exact:true}).first()).toBeVisible();
  await page.keyboard.press('Escape');
  results.push('Auto refresh: Open source property opens native interval controls');

  s=await select('36238:395271');
  await variant(s,'Checkable','Radio');
  await expect(s.getByRole('radio')).toHaveCount(1);
  await expect(s.getByRole('checkbox')).toHaveCount(0);
  await s.getByRole('radio').check();
  await expect(s.getByRole('radio')).toBeChecked();
  await variant(s,'Checkable','Checkbox');
  await expect(s.getByRole('checkbox')).toHaveCount(1);
  await variant(s,'Disabled','true');
  await expect(s.getByRole('checkbox')).toBeDisabled();
  results.push('Source card: Radio and Checkbox differ semantically, disabled preserved');

  s=await select('13580:25572');
  await variant(s,'Type','Text');
  await variant(s,'State','Filled');
  await variant(s,'Clearble','True');
  await s.getByRole('button',{name:'Очистить значение',exact:true}).click();
  await expect(s.getByRole('textbox',{name:'Пример',exact:true})).toHaveValue('');
  results.push('Form control: source Clearble property clears entered content');

  s=await select('14645:214');
  await variant(s,'Nested level','3');
  const indent=await s.locator('[data-nested-level]').evaluate(el=>parseFloat(getComputedStyle(el).paddingInlineStart));
  if(indent!==48)throw new Error(`Unexpected nested indentation ${indent}`);
  results.push('Side navigation: source nested level changes indentation');

  s=await select('22907:283773');
  await variant(s,'Type','Multiple');
  await s.getByRole('button',{name:'Композиция Multiple',exact:true}).click();
  await expect(s.getByRole('button',{name:'Композиция Multiple',exact:true})).toHaveAttribute('aria-pressed','true');
  results.push('Layout thumbnail: composition and selected state');

  s=await select('26803:282479');
  await variant(s,'State','Filled');
  await expect(s.getByText('example.txt',{exact:true})).toBeVisible();
  await s.getByRole('button',{name:'Удалить файл',exact:true}).click();
  await expect(s.getByText('example.txt',{exact:true})).toHaveCount(0);
  results.push('File field: filled fixture and clear action');

  s=await select('26768:281544');
  await expect(s.locator('.euiAvatar')).toHaveCount(10);
  const avatarColors=await s.locator('.euiAvatar').evaluateAll(nodes=>nodes.map(el=>getComputedStyle(el).backgroundColor));
  if(new Set(avatarColors).size!==10)throw new Error('Source avatar palette was overridden by EUI');
  await s.getByRole('button',{name:'Показать участников'}).click();
  await expect(page.getByText('Shared with',{exact:true})).toBeVisible();
  results.push('Avatar group: ten overlapping avatars and participant list');

  s=await select('15213:169');
  const nav=s.getByRole('navigation',{name:'Навигация',exact:true});
  const groups=nav.locator('.euiAccordion__childWrapper');
  await expect.poll(async()=>(await groups.first().boundingBox()).height).toBeGreaterThan(40);
  const nextGroup=nav.getByRole('button',{name:'Первый раздел',exact:true});
  await expect(nextGroup).toHaveAttribute('aria-expanded','false');
  await nextGroup.click();
  await expect(nextGroup).toHaveAttribute('aria-expanded','true');
  await expect.poll(async()=>(await groups.nth(1).boundingBox()).height).toBeGreaterThan(40);
  await nextGroup.click();
  await expect.poll(async()=>(await groups.nth(1).boundingBox()).height).toBe(0);
  results.push('Collapsible navigation: initial content visible, expand and collapse change actual height');
  s=await select('152:996');
  await variant(s,'Mode','Multiple');
  await s.getByRole('button',{name:'Выбрать попытку',exact:true}).click();
  await expect(page.getByRole('button',{name:'Попытка 2',exact:true})).toBeVisible();
  await page.getByRole('button',{name:'Попытка 2',exact:true}).click();
  await expect(page.getByRole('button',{name:'Попытка 2',exact:true})).toHaveCount(0);
  results.push('Attempt action: multiple attempts open a menu and selection closes it');
  if(errors.length)throw new Error(errors.join('\n'));
} catch(error) {
  errors.push(error.message);
  process.exitCode=1;
} finally {
  await writeFile('.tmp/react-base/completion-audit.json',JSON.stringify({results,errors},null,2));
  console.log(JSON.stringify({results,errors}));
  await browser.close();
}
