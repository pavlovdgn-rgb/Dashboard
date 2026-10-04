import { chromium } from '@playwright/test';
const browser=await chromium.launch({channel:'chrome',headless:true});
const page=await browser.newPage({viewport:{width:1440,height:1000}});
await page.goto('http://127.0.0.1:5173/?component=125:450');
console.log(JSON.stringify(await page.locator('main section').first().locator('button[data-kind]').evaluateAll(nodes=>nodes.map(node=>{
const s=getComputedStyle(node);return {text:node.textContent,color:s.color,background:s.backgroundColor,font:s.font,padding:s.padding,height:s.height,children:[...node.querySelectorAll('span')].map(n=>({class:n.className,font:getComputedStyle(n).font}))};})),null,2));
await page.screenshot({path:'.tmp/react-base/showcase-top.png'});
await browser.close();
