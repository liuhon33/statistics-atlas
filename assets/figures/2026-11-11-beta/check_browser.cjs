/* Offline headless browser checks. Uses a fresh, unsigned-in Edge context.
   Requirements: Node, playwright on NODE_PATH, installed Edge (or BETA_BROWSER_EXE).
   No persistent user browser/profile, server, remote request or Obsidian pane used. */
const {chromium}=require('playwright');
const fs=require('node:fs');const path=require('node:path');const {pathToFileURL}=require('node:url');
const assert=require('node:assert/strict');
(async()=>{
  const browser=await chromium.launch({headless:true,executablePath:process.env.BETA_BROWSER_EXE||'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe'});
  const cases=[],errors=[],network=[];
  try{
    const page=await browser.newPage({viewport:{width:900,height:1000},deviceScaleFactor:1});
    page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(/^https?:/.test(r.url()))network.push(r.url());});
    for(const mode of ['shapes','update']){
      await page.goto(pathToFileURL(path.join(__dirname,mode+'.html')).href);
      await page.waitForFunction(()=>document.querySelector('#plot path'));
      const buttons=page.locator('[data-preset]');
      for(let i=0;i<await buttons.count();i++){
        const expected=(await buttons.nth(i).getAttribute('data-preset')).split(',').map(Number);
        await buttons.nth(i).click();
        const actual=await page.locator('input').evaluateAll(es=>es.map(e=>+e.value));
        assert.deepEqual(actual,expected);
        assert(!/NaN|undefined/.test(await page.locator('main').innerText()));
        cases.push({mode,preset:expected,pass:true});
      }
      await buttons.nth(0).click();
      await page.locator('#alpha').focus();await page.keyboard.press('ArrowRight');
      assert.equal(await page.locator('#alpha-value').innerText(),'1.25');
      await page.keyboard.press('Home');assert.equal(await page.locator('#alpha-value').innerText(),'0.25');
      assert.match(await page.locator('#warning').innerText(),/∞/);
      await page.keyboard.press('End');assert.equal(await page.locator('#alpha-value').innerText(),'20');
      assert.match(await page.locator('#warning').innerText(),/clipped/);
      cases.push({mode,keyboard_range_and_clipping:true,pass:true});
      if(mode==='update'){
        await buttons.nth(0).click();assert.match(await page.locator('#readout').innerText(),/0.6667/);
        await page.locator('#success').focus();await page.keyboard.press('End');
        await page.locator('#failure').focus();await page.keyboard.press('End');
        assert.match(await page.locator('#readout').innerText(),/Beta\(51, 51\)/);
        assert.match(await page.locator('#readout').innerText(),/0.5/);
        cases.push({mode,maximum_counts:true,pass:true});
      }
      await buttons.nth(0).click();
      for(const width of [900,420]){
        await page.setViewportSize({width,height:1100});
        await page.waitForFunction(()=>{const s=document.querySelector('#plot');return Math.abs(s.viewBox.baseVal.width-s.clientWidth)<1;});
        const layout=await page.evaluate(()=>({width:innerWidth,bodyWidth:document.body.scrollWidth,height:document.body.getBoundingClientRect().height,paths:document.querySelectorAll('#plot path').length}));
        assert(layout.bodyWidth<=width);assert(layout.height<1800);
        await page.screenshot({path:path.join(__dirname,`${mode}-browser-${width}.png`),fullPage:true});
        cases.push({mode,layout,pass:true});
      }
      if(mode==='shapes'){
        await page.getByRole('button',{name:'U-shape (½, ½)',exact:true}).click();
        await page.screenshot({path:path.join(__dirname,'shapes-u-browser.png'),fullPage:true});
      }
    }
    // Generic sandbox/auto-height handshake, not a live Obsidian test.
    for(const mode of ['shapes','update']){
      const html=fs.readFileSync(path.join(__dirname,mode+'.html'),'utf8');
      await page.goto('about:blank');
      await page.setViewportSize({width:900,height:1100});
      await page.setContent('<body style="margin:0"><iframe sandbox="allow-scripts" style="width:760px;border:0;height:900px"></iframe></body>');
      await page.evaluate(html=>{
        const frame=document.querySelector('iframe');window.heights=[];
        window.addEventListener('message',e=>{if(e.source===frame.contentWindow&&e.data.type==='atlas-interactive-ready'){window.heights.push(e.data.height);frame.style.height=e.data.height+'px';}});
        frame.srcdoc=html;
      },html);
      await page.waitForFunction(()=>window.heights.length>0);
      for(const width of [760,420,760]){
        await page.locator('iframe').evaluate((f,w)=>f.style.width=w+'px',width);
        await page.waitForTimeout(300); // Explicit bounded resize-stability test, not an availability wait.
        const first=await page.evaluate(()=>window.heights.at(-1));
        await page.waitForTimeout(300);
        const second=await page.evaluate(()=>window.heights.at(-1));
        assert.equal(first,second);assert(first>300&&first<1800);
        cases.push({mode,sandbox_width:width,height:first,stable:true,pass:true});
      }
    }
    assert.deepEqual(errors,[]);assert.deepEqual(network,[]);
    const report={pass:true,engine:'Fresh headless Edge through Playwright; Browser plugin had no connected browsers',cases,console_errors:errors,remote_requests:network,live_obsidian:'Not tested: CLI could not reach the running app. Generic sandbox checks are not live-app verification.'};
    fs.writeFileSync(path.join(__dirname,'browser-checks.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report,null,2));
  }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
