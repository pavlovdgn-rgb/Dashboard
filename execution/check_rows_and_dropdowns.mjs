import { chromium, expect } from '@playwright/test';
import { writeFile } from 'node:fs/promises';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
const errors=[],results=[];
page.on('pageerror',error=>errors.push(error.message));
try {
  await page.goto('http://127.0.0.1:6006/iframe.html?id=ds-132-634--all-variants&viewMode=story');
  const rows=page.locator('[data-component-id="132:634"] button');
  await expect(rows).toHaveCount(6);
  // Values read from the six source variants in Figma 132:634.
  for(let n=0;n<6;n++) {
    const row=rows.nth(n);
    await expect(row).toHaveAttribute('aria-pressed',String(n>=3));
    await expect(row).toHaveCSS('border-radius','4px');
    await expect(row).toHaveCSS('min-height','88px');
    await expect(row).toHaveCSS('padding','16px');
    await expect(row).toHaveCSS('column-gap','12px');
    await expect(row).toHaveCSS('background-color',n>=3?'rgb(236, 238, 220)':n===1?'rgb(243, 243, 238)':'rgb(255, 255, 255)');
    await expect(row.locator('svg')).toHaveCSS('width','20px');
    await expect(row.locator('strong')).toHaveCSS('font-weight','500');
    if(n%3===2)await expect(row).toHaveCSS('box-shadow','rgb(98, 110, 50) 0px 0px 0px 2px inset');
  }
  await page.screenshot({path:'.tmp/storybook/first-click-rows.png',animations:'disabled',fullPage:true});
  await rows.first().focus();await page.keyboard.press('Space');await expect(rows.first()).toHaveAttribute('aria-pressed','true');await page.keyboard.press('Space');await expect(rows.first()).toHaveAttribute('aria-pressed','false');
  results.push('All six rows match source radius, height, padding, gap, fill, icon, typography and focus; keyboard selection works');

  await page.goto('http://127.0.0.1:6006/iframe.html?id=ds-153-1605--default&viewMode=story');
  const trigger=page.getByRole('button',{name:'Полнота данных',exact:true});
  await trigger.click();
  const items=page.getByRole('menuitemradio');
  await expect(items).toHaveCount(4);
  await expect(items.first()).toHaveCSS('padding','8px 12px');
  await expect(items.first()).toHaveAttribute('aria-checked','true');
  await page.screenshot({path:'.tmp/storybook/participant-dropdown.png',animations:'disabled',fullPage:true});
  await page.keyboard.press('Escape');await expect(items).toHaveCount(0);await expect(trigger).toBeFocused();
  await trigger.press('Enter');await expect(items.first()).toBeFocused();await page.keyboard.press('ArrowDown');await expect(items.nth(1)).toBeFocused();await page.keyboard.press('Enter');
  const table=page.getByRole('table',{name:'Участники исследования',exact:true});
  await expect(trigger).toHaveText('Полные');await expect(table.locator('tbody tr')).toHaveCount(4);
  await page.getByRole('button',{name:'Выбрать попытку участника 009'}).click();
  await page.getByRole('menuitemradio',{name:'Попытка 2'}).click();
  await expect(table.locator('tbody tr').filter({has:page.getByRole('cell',{name:'009',exact:true})})).toContainText('2 из 2');
  results.push('Dropdown gutters, selected item, Escape focus return, arrow navigation, filters and attempt selection');
  if(errors.length)throw new Error(errors.join('\n'));
} catch(error){errors.push(error.message);process.exitCode=1;}
finally{await writeFile('.tmp/storybook/rows-dropdowns-audit.json',JSON.stringify({results,errors},null,2));console.log(JSON.stringify({results,errors}));await browser.close();}
