// Run through Obsidian CLI eval; temporary offscreen components leave the active pane alone.
(async()=>{
  const plugin=app.plugins.plugins['statistics-atlas'];
  const host=document.createElement('div');host.style.cssText='position:fixed;left:-12000px;top:0;';
  document.body.appendChild(host);const children=[],messages=[],blocks=[];
  const receive=event=>{const frame=[...host.querySelectorAll('iframe')].find(f=>f.contentWindow===event.source);if(frame)messages.push({title:frame.title,data:event.data});};
  const wait=ms=>new Promise(resolve=>setTimeout(resolve,ms));
  const snapshot=()=>[...host.querySelectorAll('iframe')].map(frame=>({title:frame.title,width:frame.getBoundingClientRect().width,height:parseInt(frame.style.height),ready:frame.parentElement.dataset.atlasInteractive==='ready',sandbox:frame.getAttribute('sandbox')}));
  window.addEventListener('message',receive);
  try{
    const ctx={addChild(child){children.push(child);child.load();}};
    for(const name of ['ci','delta'])for(const width of [760,420]){
      const block=document.createElement('div');block.style.width=width+'px';host.appendChild(block);blocks.push(block);
      plugin.renderInteractive('path: assets/figures/2026-11-11-ci-delta/'+name+'-explorer.html\ntitle: '+name+' '+width+'\nheight: 1250',block,ctx);
    }
    for(let i=0;i<40;i++){
      const current=snapshot();if(current.length===4&&current.every(f=>f.ready))break;
      await wait(200);
    }
    const frames=snapshot();await wait(1000);
    const stable=JSON.stringify(frames)===JSON.stringify(snapshot());
    const pass=frames.length===4&&stable&&frames.every(f=>f.ready&&f.sandbox==='allow-scripts'&&f.height>600&&f.height<4000);
    return{vault:app.vault.getName(),frames,stable,messages,pass,scope:'Execution, initial sizing and stability at two widths. Offscreen Chromium frames may defer later viewport relayout; interactive resizing is checked separately in the visible browser preview.'};
  }finally{window.removeEventListener('message',receive);children.forEach(child=>child.unload());host.remove();}
})()
