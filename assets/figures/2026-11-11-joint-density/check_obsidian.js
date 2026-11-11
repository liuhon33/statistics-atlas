// Run through Obsidian CLI eval. Tests the actual component without moving the user's pane.
(async()=>{
  const plugin=app.plugins.plugins['statistics-atlas'];
  const host=document.createElement('div');host.style.cssText='position:fixed;left:-12000px;top:0;';
  document.body.appendChild(host);const children=[],messages=[];
  const receive=event=>{const frame=[...host.querySelectorAll('iframe')].find(f=>f.contentWindow===event.source);if(frame)messages.push({title:frame.title,data:event.data});};
  window.addEventListener('message',receive);
  try{
    const ctx={addChild(child){children.push(child);child.load();}};
    for(const width of [760,420]){
      const block=document.createElement('div');block.style.width=width+'px';host.appendChild(block);
      plugin.renderInteractive('path: assets/figures/2026-11-11-joint-density/joint-density.html\ntitle: Joint density '+width+'\nheight: 1400',block,ctx);
    }
    for(let i=0;i<40;i++){
      const current=[...host.querySelectorAll('iframe')];
      if(current.length===2&&current.every(frame=>frame.parentElement.dataset.atlasInteractive==='ready'))break;
      await new Promise(resolve=>setTimeout(resolve,200));
    }
    const firstHeights=[...host.querySelectorAll('iframe')].map(frame=>frame.style.height);
    await new Promise(resolve=>setTimeout(resolve,1000));
    const frames=[...host.querySelectorAll('iframe')].map((frame,i)=>({title:frame.title,width:frame.getBoundingClientRect().width,height:frame.style.height,stable:frame.style.height===firstHeights[i],ready:frame.parentElement.dataset.atlasInteractive==='ready',sandbox:frame.getAttribute('sandbox')}));
    return {vault:app.vault.getName(),frames,messages,pass:frames.length===2&&frames.every(frame=>frame.ready&&frame.stable&&frame.sandbox==='allow-scripts'&&parseInt(frame.height)>600&&parseInt(frame.height)<4000)};
  }finally{window.removeEventListener('message',receive);children.forEach(child=>child.unload());host.remove();}
})()
