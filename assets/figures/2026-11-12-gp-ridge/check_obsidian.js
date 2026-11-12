// Offscreen integration check via the local Obsidian CLI. No note navigation or settings writes.
(async()=>{
  const plugin=app.plugins.plugins['statistics-atlas'];
  if(!plugin)return {pass:false,reason:'statistics-atlas plugin unavailable'};
  const host=document.createElement('div');host.style.cssText='position:fixed;left:-12000px;top:0;width:760px;';document.body.appendChild(host);
  const children=[];const ctx={addChild(child){children.push(child);child.load();}};
  try{
    plugin.renderInteractive('path: assets/figures/2026-11-12-gp-ridge/explorer.html\ntitle: Ridge prior explorer\nheight: 1350',host,ctx);
    await new Promise(r=>setTimeout(r,1600));
    const f=host.querySelector('iframe');const h1=f?.style.height;
    host.style.width='520px';await new Promise(r=>setTimeout(r,900));const h2=f?.style.height;
    await new Promise(r=>setTimeout(r,500));const h3=f?.style.height;
    return {vault:app.vault.getName(),sandbox:f?.getAttribute('sandbox'),ready:f?.parentElement.dataset.atlasInteractive==='ready',heights:[h1,h2,h3],htmlBytes:f?.srcdoc.length,pass:!!f&&f.parentElement.dataset.atlasInteractive==='ready'&&f.getAttribute('sandbox')==='allow-scripts'&&h2===h3&&parseInt(h3)<5000};
  }finally{children.forEach(c=>c.unload());host.remove();}
})()
