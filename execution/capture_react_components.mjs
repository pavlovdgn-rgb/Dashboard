import { chromium } from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
try {
  for(const id of process.argv.slice(2)){
    await page.goto(`http://127.0.0.1:5173/?component=${id}`);
    await page.locator('main section').first().waitFor();
    await page.evaluate(()=>document.fonts.ready);
    // EUI accordions animate their initial height; capture the settled state.
    await page.waitForTimeout(400);
    await page.locator('main section').first().screenshot({path:`.tmp/react-base/component-${id.replace(':','-')}.png`});
  }
}finally{await browser.close();}
