// Run through Obsidian's local developer eval command. No vault files/settings are changed.
// Exercises the same component as the registered atlas-interactive block, in an offscreen
// container, so testing does not navigate away from a note the user is reading.
(async()=>{
  const plugin=app.plugins.plugins['statistics-atlas'];
  const host=document.createElement('div');
  host.style.cssText='position:fixed;left:-12000px;top:0;width:760px;';
  document.body.appendChild(host);
  const children=[];
  const ctx={addChild(child){children.push(child);child.load();}};
  try{
    for(const mode of ['1d','2d']){
      const block=document.createElement('div');host.appendChild(block);
      plugin.renderInteractive(`path: assets/figures/2026-11-11-fisher/fisher-${mode}.html\ntitle: Fisher ${mode}\nheight: 1100`,block,ctx);
    }
    const invalid=document.createElement('div');host.appendChild(invalid);
    plugin.renderInteractive('path: ../outside.html',invalid,ctx);
    await new Promise(r=>setTimeout(r,1800));
    const frames=[...host.querySelectorAll('iframe')].map(frame=>({title:frame.title,sandbox:frame.getAttribute('sandbox'),height:frame.style.height,ready:frame.parentElement.dataset.atlasInteractive==='ready',htmlBytes:frame.srcdoc.length}));
    return {vault:app.vault.getName(),frames,pathTraversalRejected:invalid.textContent.includes('Use a local HTML file'),pass:frames.length===2&&frames.every(x=>x.ready&&x.sandbox==='allow-scripts')&&invalid.querySelector('iframe')===null};
  }finally{children.forEach(child=>child.unload());host.remove();}
})()
