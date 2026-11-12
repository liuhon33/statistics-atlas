// Run via: Obsidian.com vault=stats_ML_rebuild eval code=<this source>.
// Temporary offscreen DOM only; no note, setting, workspace, or active-pane writes.
(async()=>{
  if(app.vault.getName()!=='stats_ML_rebuild')throw new Error('Wrong vault');
  const plugin=app.plugins.plugins['statistics-atlas'];
  if(!plugin)throw new Error('Atlas plugin unavailable');
  const host=document.createElement('div');
  host.style.cssText='position:fixed;left:-12000px;top:0;width:760px;';
  document.body.appendChild(host);
  const children=[];
  const context={addChild(child){children.push(child);child.load();}};
  try{
    const results=[];
    for(const width of [760,420]){
      const container=document.createElement('div');host.appendChild(container);
      container.style.width=width+'px';
      plugin.renderInteractive('path: assets/figures/2026-11-11-pca/explorer.html\ntitle: PCA explorer\nheight: 800',container,context);
      await new Promise(resolve=>setTimeout(resolve,1800));
      results.push({
        width,
        frames:[...container.querySelectorAll('iframe')].map(f=>({
          title:f.title,sandbox:f.getAttribute('sandbox'),height:f.style.height,
          ready:f.parentElement.dataset.atlasInteractive==='ready'
        }))
      });
    }
    return {vault:app.vault.getName(),results,pass:
      results.every(r=>r.frames.length===1&&r.frames[0].ready&&r.frames[0].sandbox==='allow-scripts')};
  }finally{children.forEach(child=>child.unload());host.remove();}
})()
