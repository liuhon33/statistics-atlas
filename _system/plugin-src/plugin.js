const {Plugin, ItemView, Notice, TFile, parseYaml, MarkdownRenderChild, Keymap, setIcon} = require('obsidian');
const ATLAS_VIEW='statistics-atlas-view',LAYOUT_PATH='_system/layout.json';
// Live ```atlas``` block (Claude, 2026-11-08, AGENTS A2): replaces the hand-copied "Topics" and
// "Connected from" lists. Rendered from the current model; re-rendered whenever the model refreshes.
class AtlasPageBlock extends MarkdownRenderChild {
  constructor(el,plugin,sourcePath){super(el);this.plugin=plugin;this.sourcePath=sourcePath;}
  onload(){this.plugin.blocks.add(this);this.render();}
  onunload(){this.plugin.blocks.delete(this);}
  link(parent,node){
    const a=parent.createEl('a',{cls:'atlas-block-link',text:node.label,href:'#'});
    const target=node.path.replace(/\.md$/i,'');
    a.addEventListener('mousedown',e=>e.stopPropagation());
    a.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();this.plugin.app.workspace.openLinkText(target,this.sourcePath,Keymap.isModEvent(e));});
    a.addEventListener('mouseover',e=>this.plugin.app.workspace.trigger('hover-link',{event:e,source:'preview',hoverParent:this,targetEl:a,linktext:target,sourcePath:this.sourcePath}));
    return a;
  }
  section(title,items,fill){
    if(!items.length)return;
    const s=this.containerEl.createDiv({cls:'atlas-block-section'});
    s.createDiv({cls:'atlas-block-heading',text:`${title} (${items.length})`});
    const ul=s.createEl('ul');for(const item of items)fill(ul.createEl('li'),item);
  }
  render(){
    const el=this.containerEl;el.empty();el.addClass('atlas-block');
    const model=this.plugin.model;
    if(!model){el.createDiv({cls:'atlas-block-muted',text:'Loading statistics atlas…'});return;}
    const node=model.nodes.find(n=>n.path===this.sourcePath);
    if(!node){el.createDiv({cls:'atlas-block-muted',text:'This page is not on the atlas.'});return;}
    const data=AtlasCore.pageLinks(model,node.id);
    const label={prerequisite:'prerequisite',application:'applied here',connection:'related'};
    this.section('Topics',data.topics,(li,c)=>{this.link(li,c);li.createSpan({cls:'atlas-block-muted',text:` · L${c.level}`});});
    this.section('Connected from',data.inbound,(li,x)=>{this.link(li,x.node);li.createSpan({cls:'atlas-block-muted',text:` · ${label[x.type]||x.type}${x.reason?' — '+x.reason:''}`});});
    this.section('My notes here',data.notes,(li,x)=>{this.link(li,x.node);li.createSpan({cls:'atlas-block-muted',text:x.how==='home'?' · attached here':' · links here'+(x.reason?' — '+x.reason:'')});});
    if(!el.childElementCount)el.createDiv({cls:'atlas-block-muted',text:'No sub-topics, incoming links or notes yet.'});
  }
}
class StatisticsAtlasView extends ItemView {
  constructor(leaf,plugin){super(leaf);this.plugin=plugin;}
  getViewType(){return ATLAS_VIEW;}
  getDisplayText(){return 'Statistics atlas';}
  getIcon(){return 'network';}
  async onOpen(){await this.plugin.ready;this.ui=new AtlasUI(this.contentEl,this.plugin.model,{openNote:path=>this.plugin.openNote(path),setIcon,onStateChange:()=>this.app.workspace.requestSaveLayout()},AtlasCore);if(this.pendingState)this.restore(this.pendingState);}
  async onClose(){this.ui?.destroy();this.ui=null;}
  getState(){return this.ui?{mode:this.ui.mode,depth:this.ui.depth,focus:this.ui.focus,selected:this.ui.selected,camera:this.ui.camera,panel:this.ui.panelOpen}:{};}
  async setState(state,result){this.pendingState=state;if(this.ui)this.restore(state);await super.setState(state,result);}
  restore(s){if(typeof s.panel==='boolean')this.ui.setPanel(s.panel);if(AtlasCore.MODES.includes(s.mode))this.ui.mode=s.mode;if(s.depth>=1&&s.depth<=5)this.ui.depth=s.depth;this.ui.depthSelect.value=this.ui.depth;if(this.plugin.model.byId.has(s.focus))this.ui.focus=s.focus;if(this.plugin.model.byId.has(s.selected))this.ui.selected=s.selected;if(s.camera&&Number.isFinite(s.camera.k)&&s.camera.k>0){this.ui.camera={...s.camera};this.ui.fitted=true;}this.ui.update();}
}
module.exports=class StatisticsAtlasPlugin extends Plugin {
  async onload(){
    this.store=new AtlasCore.RecordStore();this.dirty=new Set();this.layout=null;this.blocks=new Set();this.registerView(ATLAS_VIEW,leaf=>new StatisticsAtlasView(leaf,this));
    this.registerMarkdownCodeBlockProcessor('atlas',(source,el,ctx)=>ctx.addChild(new AtlasPageBlock(el,this,ctx.sourcePath)));
    this.addRibbonIcon('network','Open statistics atlas',()=>this.activate());
    this.addCommand({id:'open-atlas',name:'Open statistics atlas',callback:()=>this.activate()});
    this.addCommand({id:'refresh-atlas',name:'Refresh statistics atlas',callback:async()=>{this.layout=null;this.fullPending=true;await this.refresh();new Notice('Statistics atlas refreshed.');}});
    this.ready=this.refresh();
    // Incremental refresh (Claude, 2026-11-08, review fix 8). Each event marks only the file it concerns;
    // a refresh re-reads those files from Obsidian's metadata cache and rebuilds the map only when a
    // property or reason line the map uses changed. Typing in a note's text no longer rebuilds the atlas.
    this.registerEvent(this.app.metadataCache.on('changed',file=>this.markDirty(file.path)));
    // The first 'resolved' after startup means Obsidian finished indexing: one full rescan catches notes whose
    // properties were not cached yet when the plugin loaded. Later 'resolved' events add nothing.
    this.registerEvent(this.app.metadataCache.on('resolved',()=>{if(this.indexed)return;this.indexed=true;this.fullPending=true;this.queueRefresh();}));
    this.registerEvent(this.app.vault.on('create',file=>{if(file instanceof TFile)this.markDirty(file.path);}));
    this.registerEvent(this.app.vault.on('modify',file=>{if(file.path===LAYOUT_PATH){this.layout=null;this.queueRefresh();}}));
    this.registerEvent(this.app.vault.on('delete',file=>{this.forget(file);this.queueRefresh();}));
    this.registerEvent(this.app.vault.on('rename',(file,oldPath)=>{this.forget(file,oldPath);if(file instanceof TFile)this.markDirty(file.path);else{this.fullPending=true;this.queueRefresh();}}));
    this.app.workspace.onLayoutReady(async()=>{try{await this.ready;await this.activate();}catch(e){console.error('Statistics atlas',e);new Notice('Statistics atlas could not load: '+e.message);}});
  }
  markDirty(path){this.dirty.add(path);this.queueRefresh();}
  forget(file,path=file.path){if(file instanceof TFile)this.store.delete(path)&&(this.storeChanged=true);else if(this.store.deletePrefix(path+'/'))this.storeChanged=true;this.dirty.delete(path);}
  relevant(file){return file instanceof TFile&&!file.path.startsWith('.')&&(file.extension==='md'||file.path.startsWith('raw/')||file.path.startsWith('assets/')||(file.extension==='json'&&file.path.startsWith('_system/Migrations/')));}
  queueRefresh(){clearTimeout(this.timer);this.timer=setTimeout(()=>this.refresh().catch(e=>{console.error(e);new Notice('Atlas refresh failed: '+e.message);}),300);}
  async refresh(){
    if(this.refreshing){this.refreshAgain=true;return this.refreshing;}
    this.refreshing=this.update();
    try{await this.refreshing;}
    finally{this.refreshing=null;if(this.refreshAgain){this.refreshAgain=false;this.queueRefresh();}}
  }
  // Returns true when the model was rebuilt. Views and page blocks are redrawn only then.
  async update(){
    const full=this.fullPending||!this.model;this.fullPending=false;
    const dirty=[...this.dirty];this.dirty.clear();
    let changed=this.storeChanged||!this.model;this.storeChanged=false;
    if(!this.layout){this.layout=JSON.parse(await this.app.vault.adapter.read(LAYOUT_PATH));changed=true;}
    if(full){
      const files=this.app.vault.getFiles().filter(f=>this.relevant(f)),present=new Set(files.map(f=>f.path));
      for(const path of this.store.paths())if(!present.has(path))changed=this.store.delete(path)||changed;
      for(let i=0;i<files.length;i+=64)if((await Promise.all(files.slice(i,i+64).map(f=>this.loadRecord(f)))).some(Boolean))changed=true;
    }else for(const path of dirty){
      const file=this.app.vault.getAbstractFileByPath(path);
      changed=(this.relevant(file)?await this.loadRecord(file):this.store.delete(path))||changed;
    }
    this.stats={full,files:full?this.store.map.size:dirty.length,rebuilt:changed};
    if(!changed)return false;
    this.model=AtlasCore.compile(this.store.records(),this.layout);
    for(const leaf of this.app.workspace.getLeavesOfType(ATLAS_VIEW))leaf.view.ui?.updateModel(this.model);
    for(const block of this.blocks)block.render();
    return true;
  }
  // Properties come from Obsidian's metadata cache (already parsed). The note text is read only for notes that
  // declare links, and only their reason lines are kept. A note Obsidian has not indexed yet is parsed directly.
  // Not named load(): that would override Obsidian's Plugin.load() lifecycle method and break plugin startup.
  async loadRecord(file){
    if(file.extension!=='md')return this.store.set(file.path,{layer:'auxiliary',role:'source'},'');
    const cache=this.app.metadataCache.getFileCache(file);
    let fm=cache?.frontmatter?{...cache.frontmatter}:null,body='';
    if(fm&&fm.position&&typeof fm.position==='object'&&'start' in fm.position)delete fm.position; // older Obsidian kept the YAML span here
    if(!cache||AtlasCore.needsBody(fm)){
      const text=await this.app.vault.cachedRead(file),match=text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
      if(!cache){try{fm=match?parseYaml(match[1])||{}:{};}catch(e){fm={title:'Invalid properties: '+file.basename};}}
      body=match?text.slice(match[0].length):text;
    }
    return this.store.set(file.path,fm||{},body);
  }
  async activate(){await this.ready;if(!this.model)return;let leaf=this.app.workspace.getLeavesOfType(ATLAS_VIEW)[0];if(!leaf){leaf=this.app.workspace.getLeaf('tab');await leaf.setViewState({type:ATLAS_VIEW,active:true});}await this.app.workspace.revealLeaf(leaf);}
  async openNote(path){const file=this.app.vault.getAbstractFileByPath(path);if(!(file instanceof TFile)){new Notice('Note is unavailable: '+path);return;}await this.app.workspace.getLeaf('tab').openFile(file);}
  onunload(){clearTimeout(this.timer);}
};
