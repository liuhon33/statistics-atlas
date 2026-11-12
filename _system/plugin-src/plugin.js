const {Plugin, ItemView, MarkdownView, Notice, TFile, parseYaml, MarkdownRenderChild, Keymap, setIcon, FuzzySuggestModal, Modal} = require('obsidian');
const ATLAS_VIEW='statistics-atlas-view',LAYOUT_PATH='_system/layout.json',PICKER_COMMAND='open-attached-note';
// A note link that opens in place (Ctrl/Cmd-click: new tab) and shows Obsidian's hover preview.
function atlasLink(app,parent,node,sourcePath,hoverParent){
  const a=parent.createEl('a',{cls:'atlas-block-link',text:node.label,href:'#'});
  const target=node.path.replace(/\.md$/i,'');
  a.addEventListener('mousedown',e=>e.stopPropagation());
  a.addEventListener('click',e=>{e.preventDefault();e.stopPropagation();app.workspace.openLinkText(target,sourcePath,Keymap.isModEvent(e));});
  a.addEventListener('mouseover',e=>app.workspace.trigger('hover-link',{event:e,source:'preview',hoverParent,targetEl:a,linktext:target,sourcePath}));
  return a;
}
// Attached-notes picker (Claude, 2026-11-09, AGENTS A16). Notes attached to the page come first, then notes
// attached below it, then notes that only link to it. Enter opens in this tab; Ctrl/Cmd+Enter opens a new tab.
// Title prompt for "New learning note here" (Claude, 2026-11-09, AGENTS A17).
class NewNoteModal extends Modal {
  constructor(app,home,onSubmit){super(app);this.home=home;this.onSubmit=onSubmit;}
  onOpen(){
    this.setTitle?.('New learning note');
    const {contentEl}=this;
    contentEl.createDiv({cls:'atlas-newnote-home',text:'Home: '+(this.home.fm.backbone_path||this.home.label)});
    const input=contentEl.createEl('input',{type:'text',cls:'atlas-newnote-input',attr:{placeholder:'A useful question or topic'}});
    const err=contentEl.createDiv({cls:'atlas-newnote-error'});
    const row=contentEl.createDiv({cls:'modal-button-container'});
    const go=row.createEl('button',{cls:'mod-cta',text:'Create draft'});
    const submit=async()=>{const msg=await this.onSubmit(input.value);if(msg)err.setText(msg);else this.close();};
    go.addEventListener('click',submit);
    input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.isComposing){e.preventDefault();submit();}});
    setTimeout(()=>input.focus(),0);
  }
  onClose(){this.contentEl.empty();}
}
class AttachedNotesModal extends FuzzySuggestModal {
  constructor(plugin,data){
    super(plugin.app);this.data=data;
    this.items=[...data.here.map(x=>({...x,group:'here'})),...data.below.map(x=>({...x,group:'below'})),...data.linked.map(x=>({...x,group:'linked'}))];
    this.setPlaceholder(`Learning notes for ${data.node.label}`);
    this.setInstructions([{command:'↑↓',purpose:'to navigate'},{command:'↵',purpose:'to open'},{command:'ctrl ↵',purpose:'to open in a new tab'},{command:'esc',purpose:'to dismiss'}]);
    this.scope.register(['Mod'],'Enter',evt=>{this.selectActiveSuggestion(evt);return false;});
  }
  getItems(){return this.items;}
  // The home topic is searchable too, so typing a sub-topic finds the notes attached there.
  getItemText(x){return x.node.label+(x.home?' · '+x.home.label:'');}
  renderSuggestion(match,el){
    const x=match.item,ranges=match.match?.matches||[],offset=x.node.label.length+3;
    const mark=(target,text,shift)=>{let i=0;for(const [s0,e0] of ranges){const s=Math.max(0,s0-shift),e=Math.min(text.length,e0-shift);if(e<=s)continue;if(s>i)target.appendText(text.slice(i,s));target.createSpan({cls:'suggestion-highlight',text:text.slice(s,e)});i=e;}if(i<text.length)target.appendText(text.slice(i));};
    el.addClass('mod-complex','atlas-pick');
    const content=el.createDiv({cls:'suggestion-content'});
    mark(content.createDiv({cls:'suggestion-title'}),x.node.label,0);
    const note=content.createDiv({cls:'suggestion-note'});
    if(x.group==='here')note.setText('attached here');
    else if(x.group==='below'){note.appendText('in ');mark(note.createSpan(),x.home.label,offset);note.appendText(` · L${x.home.level}`);}
    else note.setText('links here'+(x.reason?' — '+x.reason:''));
  }
  onChooseItem(x,evt){
    const file=this.app.vault.getAbstractFileByPath(x.node.path);
    if(!(file instanceof TFile)){new Notice('Note is unavailable: '+x.node.path);return;}
    this.app.workspace.getLeaf(Keymap.isModEvent(evt)).openFile(file);
  }
}
// Live ```atlas``` block (Claude, 2026-11-08, AGENTS A2): replaces the hand-copied "Topics" and
// "Connected from" lists. Rendered from the current model; re-rendered whenever the model refreshes.
class AtlasPageBlock extends MarkdownRenderChild {
  constructor(el,plugin,sourcePath){super(el);this.plugin=plugin;this.sourcePath=sourcePath;}
  onload(){this.plugin.blocks.add(this);this.render();}
  onunload(){this.plugin.blocks.delete(this);}
  link(parent,node){return atlasLink(this.plugin.app,parent,node,this.sourcePath,this);}
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
  constructor(leaf,plugin){
    super(leaf);this.plugin=plugin;
    // One layer of preview (user request, 2026-11-11). Obsidian sets view.hoverPopover when it opens a preview for this
    // view (the hover peek). A capture-phase guard on that preview stops mouseover from reaching the links inside it,
    // so they cannot open nested previews, and tells the preview instead that the pointer is on it, so it stays open.
    // Clicking those links still works. Other previews in Obsidian keep their normal nesting.
    let popover=null;
    const guard=p=>{const el=p?.hoverEl;if(!el||el.atlasOneLayer)return;el.atlasOneLayer=true;
      el.addEventListener('mouseover',e=>{if(e.target!==el&&e.target.closest?.('a,.internal-link,[data-href]')){e.stopPropagation();el.dispatchEvent(new MouseEvent('mouseover',{bubbles:true,relatedTarget:e.relatedTarget}));}},true);};
    Object.defineProperty(this,'hoverPopover',{configurable:true,get:()=>popover,set:p=>{popover=p;guard(p);if(p)setTimeout(()=>guard(p),0);}});
  }
  getViewType(){return ATLAS_VIEW;}
  getDisplayText(){return 'Statistics atlas';}
  getIcon(){return 'network';}
  async onOpen(){await this.plugin.ready;this.ui=new AtlasUI(this.contentEl,this.plugin.model,{openNote:(path,heading)=>this.plugin.openNote(path,heading),onPeek:(path,targetEl,event)=>this.app.workspace.trigger('hover-link',{event,source:ATLAS_VIEW,hoverParent:this,targetEl,linktext:path.replace(/\.md$/i,''),sourcePath:''}),onFollow:on=>{if(on)this.plugin.followFile(this.plugin.lastNote,true);},setIcon,onStateChange:()=>this.app.workspace.requestSaveLayout()},AtlasCore);if(this.pendingState)this.restore(this.pendingState);}
  async onClose(){this.ui?.destroy();this.ui=null;}
  // stage: the map size the saved camera belongs to, so a restore during tab layout is not shifted off-centre (Claude, 2026-11-11).
  getState(){return this.ui?{mode:this.ui.mode,depth:this.ui.depth,focus:this.ui.focus,selected:this.ui.selected,camera:this.ui.camera,stage:this.ui._stageSize,panel:this.ui.panelOpen,follow:!!this.ui.follow,coverage:!!this.ui.coverage,minimap:!!this.ui.minimap}:{};}
  async setState(state,result){this.pendingState=state;if(this.ui)this.restore(state);await super.setState(state,result);}
  restore(s){if(typeof s.follow==='boolean')this.ui.setFollow(s.follow);if(typeof s.coverage==='boolean')this.ui.setCoverage(s.coverage);if(typeof s.minimap==='boolean')this.ui.setMinimap(s.minimap);if(typeof s.panel==='boolean')this.ui.setPanel(s.panel);if(AtlasCore.MODES.includes(s.mode))this.ui.mode=s.mode;if(s.depth>=1&&s.depth<=5)this.ui.depth=s.depth;this.ui.depthSelect.value=this.ui.depth;if(this.plugin.model.byId.has(s.focus))this.ui.focus=s.focus;if(this.plugin.model.byId.has(s.selected))this.ui.selected=s.selected;if(s.camera&&Number.isFinite(s.camera.k)&&s.camera.k>0){this.ui.camera={...s.camera};this.ui.fitted=true;this.ui.autoFit=false;this.ui.glide=null;if(s.stage?.w>0&&s.stage?.h>0)this.ui._stageSize={w:s.stage.w,h:s.stage.h};}this.ui.update();this.ui.ensureVisible();}
}
// Offline mathematical explorers authored in assets/figures. The iframe is isolated
// from Obsidian (no same-origin permission); the HTML supplies its own restrictive CSP.
class AtlasInteractiveBlock extends MarkdownRenderChild {
  constructor(el,plugin,source){super(el);this.plugin=plugin;this.source=source;}
  async onload(){
    this.alive=true;
    try{
      const cfg=parseYaml(this.source)||{},path=String(cfg.path||'');
      if(!/^assets\/figures\/[A-Za-z0-9_./-]+\.html$/.test(path)||path.split('/').includes('..'))throw new Error('Use a local HTML file under assets/figures/.');
      const html=await this.plugin.app.vault.adapter.read(path);
      if(!this.alive)return;
      const frame=this.containerEl.createEl('iframe');
      frame.setAttribute('sandbox','allow-scripts');frame.setAttribute('referrerpolicy','no-referrer');
      frame.title=String(cfg.title||'Interactive mathematical illustration');
      frame.style.cssText='width:100%;border:0;border-radius:12px;display:block;';
      frame.style.height=Math.max(320,Math.min(2200,Number(cfg.height)||1100))+'px';
      this.registerDomEvent(window,'message',event=>{
        if(event.source!==frame.contentWindow||event.data?.type!=='atlas-interactive-ready')return;
        const height=Number(event.data.height);
        if(Number.isFinite(height)&&height>0)frame.style.height=Math.max(320,Math.min(5000,height))+'px';
        this.containerEl.dataset.atlasInteractive='ready';
      });
      frame.srcdoc=html;
    }catch(e){if(this.alive)this.containerEl.createDiv({text:'Interactive illustration unavailable: '+e.message+' The static figure below remains available.'});}
  }
  onunload(){this.alive=false;this.containerEl.empty();}
}
module.exports=class StatisticsAtlasPlugin extends Plugin {
  async onload(){
    this.store=new AtlasCore.RecordStore();this.dirty=new Set();this.layout=null;this.blocks=new Set();this.registerView(ATLAS_VIEW,leaf=>new StatisticsAtlasView(leaf,this));
    // Hover peek (extra idea 1): the atlas is a page-preview source, so Settings → Page preview lists it with its own
    // "require Ctrl/Cmd" choice; off by default.
    this.registerHoverLinkSource?.(ATLAS_VIEW,{display:'Statistics atlas',defaultMod:false});
    this.registerMarkdownCodeBlockProcessor('atlas',(source,el,ctx)=>ctx.addChild(new AtlasPageBlock(el,this,ctx.sourcePath)));
    this.registerMarkdownCodeBlockProcessor('atlas-interactive',(source,el,ctx)=>this.renderInteractive(source,el,ctx));
    this.addRibbonIcon('network','Open statistics atlas',()=>this.activate());
    this.addCommand({id:'open-atlas',name:'Open statistics atlas',callback:()=>this.activate()});
    this.addCommand({id:'refresh-atlas',name:'Refresh statistics atlas',callback:async()=>{this.layout=null;this.fullPending=true;await this.refresh();new Notice('Statistics atlas refreshed.');}});
    // A16: default hotkey only; the user can rebind it in Settings → Hotkeys.
    // Phase 3 (Claude, 2026-11-11): the note in front of the user, spotlit on the atlas in a split to its right.
    this.addCommand({id:'where-am-i',name:'Where am I in the atlas',hotkeys:[{modifiers:['Mod','Shift'],key:'M'}],callback:()=>this.whereAmI()});
    this.addCommand({id:PICKER_COMMAND,name:'Open a learning note attached to this page',hotkeys:[{modifiers:['Mod','Shift'],key:'L'}],callback:()=>this.openAttachedPicker()});
    // A17: a draft learning note homed on the current backbone page (or the topic selected in the atlas).
    this.addCommand({id:'new-learning-note',name:'New learning note here',hotkeys:[{modifiers:['Mod','Alt'],key:'N'}],callback:()=>this.newNoteHere()});
    this.stripTimers=[];this.modelVersion=0;this.whereActions=new WeakMap();
    this.app.workspace.onLayoutReady(()=>{
      for(const event of ['file-open','layout-change','active-leaf-change'])
        this.registerEvent(this.app.workspace.on(event,()=>this.queueNoteStrips()));
      this.registerEvent(this.app.workspace.on('file-open',file=>this.followFile(file)));
      // A Reading view rendered for the first time can finish after those events; its render triggers one more pass.
      this.registerMarkdownPostProcessor((el,ctx)=>{if(this.nodeAt(ctx.sourcePath)?.layer!=='backbone')return;clearTimeout(this.stripSoon);this.stripSoon=setTimeout(()=>this.applyNoteStrips(),50);});
      this.queueNoteStrips();
    });
    this.ready=this.refresh();
    // A14: presentation only. Keep real YAML intact and allow manual expansion.
    this.propertyFoldDefaults=new WeakMap();this.propertyFoldTimers=[];
    this.app.workspace.onLayoutReady(()=>{
      for(const event of ['file-open','layout-change','active-leaf-change'])
        this.registerEvent(this.app.workspace.on(event,()=>this.queuePropertyFoldDefaults()));
      this.queuePropertyFoldDefaults();
    });
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
  renderInteractive(source,el,ctx){ctx.addChild(new AtlasInteractiveBlock(el,this,source));}
  markDirty(path){this.dirty.add(path);this.queueRefresh();}
  queuePropertyFoldDefaults(){
    for(const timer of this.propertyFoldTimers)clearTimeout(timer);
    // File-open can precede rendering; bounded retries, never a polling loop.
    // Let Obsidian restore the view's saved fold state first; a zero-delay fold is overwritten.
    this.propertyFoldTimers=[300,600,1200].map(delay=>setTimeout(()=>this.applyPropertyFoldDefaults(),delay));
  }
  applyPropertyFoldDefaults(){
    for(const leaf of this.app.workspace.getLeavesOfType('markdown')){
      const view=leaf.view,metadata=view.metadataEditor;
      if(!view.file||!metadata?.containerEl?.isConnected)continue;
      const key=view.file.path+'\0'+view.getMode();
      if(this.propertyFoldDefaults.get(metadata)===key)continue;
      // Native API verified in the running app; guarded DOM fallback for other versions.
      // false avoids animation and persisting a fold-state change to the note.
      if(typeof metadata.setCollapse==='function')metadata.setCollapse(true,false);
      else if(!metadata.containerEl.classList.contains('is-collapsed'))
        metadata.containerEl.querySelector('.metadata-properties-heading')?.click();
      if(metadata.containerEl.classList.contains('is-collapsed'))this.propertyFoldDefaults.set(metadata,key);
    }
  }
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
    this.modelVersion++;this.applyNoteStrips();
    return true;
  }
  nodeAt(path){
    if(!this.model||!path)return null;
    if(this.pathIndexFor!==this.model){this.pathIndex=new Map(this.model.nodes.map(n=>[n.path,n]));this.pathIndexFor=this.model;}
    return this.pathIndex.get(path)||null;
  }
  // The backbone page in front of the user: the active Markdown page, or the topic selected in the atlas view.
  activeBackbone(){
    const atlas=this.app.workspace.getActiveViewOfType?.(StatisticsAtlasView);
    const node=atlas?this.model?.byId.get(atlas.ui?.selected):this.nodeAt(this.app.workspace.getActiveFile()?.path);
    return node?.layer==='backbone'?node:null;
  }
  async newNoteHere(node){
    await this.ready;node=node||this.activeBackbone();
    if(!node){new Notice('Open a backbone page, or select a topic in the atlas, to add a learning note there.');return;}
    new NewNoteModal(this.app,node,async title=>{
      const today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
      const draft=AtlasCore.newNoteDraft(this.model,node.id,title,today);if(draft.error)return draft.error;
      if(this.app.vault.getAbstractFileByPath(draft.path))return 'A file already exists at '+draft.path;
      try{
        if(!this.app.vault.getAbstractFileByPath(draft.folder))await this.app.vault.createFolder(draft.folder);
        const file=await this.app.vault.create(draft.path,draft.content);
        await this.app.workspace.getLeaf('tab').openFile(file,{active:true});
        new Notice(`Draft created at ${node.label}. Review it, then "approve" to commit.`);
      }catch(e){return 'Could not create the note: '+e.message;}
      return null;
    }).open();
  }
  async openAttachedPicker(node){
    await this.ready;node=node||this.activeBackbone();
    if(!node){new Notice('Open a backbone page, or select a topic in the atlas, to list its learning notes.');return;}
    const data=AtlasCore.attachedNotes(this.model,node.id);
    if(!data.here.length&&!data.below.length&&!data.linked.length){new Notice(`No learning notes are attached to ${node.label} or its sub-topics yet.`);return;}
    new AttachedNotesModal(this,data).open();
  }
  // "My notes" strip under the title of every backbone page that has notes (Claude, 2026-11-09, AGENTS A16).
  // Presentation only: drawn into the open view, never written to the note, redrawn when the model or file changes.
  queueNoteStrips(){
    for(const timer of this.stripTimers)clearTimeout(timer);
    this.applyNoteStrips();
    // A view can finish rendering after file-open (e.g. switching to Reading view); bounded retries, never polling.
    this.stripTimers=[150,600].map(delay=>setTimeout(()=>this.applyNoteStrips(),delay));
  }
  applyNoteStrips(){
    for(const leaf of this.app.workspace.getLeavesOfType('markdown')){
      const view=leaf.view,root=view?.containerEl;
      if(!view?.file||!root?.querySelector)continue;
      const node=this.nodeAt(view.file.path),data=node?.layer==='backbone'?AtlasCore.attachedNotes(this.model,node.id):null;
      // "Where am I" button in the header of every backbone page and learning note (Phase 3). Display only.
      const wants=!!node&&node.layer!=='auxiliary'&&typeof view.addAction==='function';let action=this.whereActions.get(view);
      if(wants&&!action){action=view.addAction('locate-fixed','Where am I in the atlas',()=>this.whereAmI(view.file,leaf));this.whereActions.set(view,action);}
      else if(!wants&&action){action.remove();this.whereActions.delete(view);}
      const show=!!data&&(data.here.length+data.below.length+data.linked.length)>0,key=view.file.path+'\0'+this.modelVersion;
      // Live Preview/Source: between Properties and the text. Reading view: end of the title header.
      for(const [hostSel,beforeSel] of [['.markdown-source-view .cm-sizer','.cm-contentContainer'],['.markdown-reading-view .mod-header',null]]){
        const host=root.querySelector(hostSel);if(!host)continue;
        let strip=[...host.children].find(c=>c.classList.contains('atlas-note-strip'));
        if(!show){strip?.remove();continue;}
        if(strip?.dataset.key===key)continue;
        if(!strip){
          const before=beforeSel&&[...host.children].find(c=>c.matches(beforeSel));
          if(beforeSel&&!before)continue;
          strip=host.ownerDocument.createElement('div');strip.className='atlas-note-strip';
          strip.addEventListener('mousedown',e=>e.stopPropagation());
          host.insertBefore(strip,before||null);
        }
        strip.dataset.key=key;this.renderStrip(strip,data,view);
      }
    }
  }
  renderStrip(el,data,view){
    el.empty();
    el.createSpan({cls:'atlas-note-strip-label',text:'My notes'});
    const list=el.createSpan({cls:'atlas-note-strip-list'});
    data.here.forEach((x,i)=>{if(i)list.createSpan({cls:'atlas-note-strip-sep',text:'·'});atlasLink(this.app,list,x.node,view.file.path,view);});
    if(!data.here.length)list.createSpan({cls:'atlas-note-strip-muted',text:'none attached here'});
    const pick=()=>this.openAttachedPicker(data.node),more=[];
    if(data.below.length)more.push(`${data.below.length} in sub-topics`);
    if(data.linked.length)more.push(data.linked.length===1?'1 note links here':`${data.linked.length} notes link here`);
    if(more.length){const b=el.createEl('button',{cls:'atlas-note-strip-more',text:more.join(' · ')});b.addEventListener('click',pick);}
    const keys=this.app.hotkeyManager?.printHotkeyForCommand?.(`${this.manifest?.id||'statistics-atlas'}:${PICKER_COMMAND}`);
    const open=el.createEl('button',{cls:'atlas-note-strip-open clickable-icon',attr:{'aria-label':'Open an attached learning note'+(keys?` (${keys})`:'')}});
    setIcon(open,'search');open.addEventListener('click',pick);
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
  // Where am I (Claude, 2026-11-11, Phase 3). Shows the note in front of the user on the atlas, in a split to the right
  // of the note; an atlas already open in another tab group is reused. Its backbone path goes into the spotlight and
  // follow mode is turned on there. Run again on the same note, it switches between the whole path and a close-up;
  // run from the atlas itself, it spotlights the selected dot. The note keeps the focus.
  async whereAmI(file,noteLeaf){
    await this.ready;if(!this.model)return;
    const atlas=!file&&this.app.workspace.getActiveViewOfType?.(StatisticsAtlasView);
    if(atlas){const ui=atlas.ui;if(ui?.spot)ui.toggleFrame();else if(ui?.selected)ui.spotlight(ui.selected);else new Notice('Select a dot first, or run Where am I from a note.');return;}
    noteLeaf=noteLeaf||(MarkdownView&&this.app.workspace.getActiveViewOfType?.(MarkdownView)?.leaf)||null;file=file||noteLeaf?.view?.file||this.app.workspace.getActiveFile();
    const node=this.nodeAt(file?.path);if(!node||node.layer==='auxiliary'){new Notice('This note is not on the atlas map.');return;}
    this.lastNote=file;
    let leaf=this.app.workspace.getLeavesOfType(ATLAS_VIEW).find(l=>!noteLeaf||l.parent!==noteLeaf.parent);
    if(!leaf){leaf=noteLeaf?this.app.workspace.createLeafBySplit(noteLeaf,'vertical'):this.app.workspace.getLeaf('split','vertical');await leaf.setViewState({type:ATLAS_VIEW,active:false});}
    else this.app.workspace.revealLeaf(leaf);
    const ui=await this.atlasUi(leaf);if(!ui)return;
    if(ui.spot?.kind==='node'&&ui.spot.id===node.id)ui.toggleFrame();else ui.spotlight(node.id,'path');
    ui.setFollow(true);this.app.workspace.requestSaveLayout();
    if(noteLeaf)this.app.workspace.setActiveLeaf(noteLeaf,{focus:true});
  }
  async atlasUi(leaf){for(let i=0;i<60&&!leaf.view?.ui;i++)await new Promise(r=>setTimeout(r,25));return leaf.view?.ui||null;}
  // Follow mode (Phase 3): every atlas view with follow on spotlights each atlas note opened in front of the user.
  followFile(file,force=false){
    const node=file?.path?this.nodeAt(file.path):null;if(!node||node.layer==='auxiliary')return;this.lastNote=file;
    for(const leaf of this.app.workspace.getLeavesOfType(ATLAS_VIEW)){const ui=leaf.view?.ui;if(ui?.follow&&(force||!(ui.spot?.kind==='node'&&ui.spot.id===node.id)))ui.spotlight(node.id,'path');}
  }
  // heading: open at that heading when the note has it (the link panel's "Open where it's written").
  async openNote(path,heading){
    const file=this.app.vault.getAbstractFileByPath(path);if(!(file instanceof TFile)){new Notice('Note is unavailable: '+path);return;}
    if(heading&&this.app.metadataCache.getFileCache(file)?.headings?.some(h=>h.heading===heading)){await this.app.workspace.openLinkText(file.path.replace(/\.md$/i,'')+'#'+heading,'','tab');return;}
    await this.app.workspace.getLeaf('tab').openFile(file);
  }
  onunload(){
    for(const leaf of this.app.workspace.getLeavesOfType?.('markdown')||[])this.whereActions?.get(leaf.view)?.remove();
    clearTimeout(this.timer);clearTimeout(this.stripSoon);for(const timer of [...(this.propertyFoldTimers||[]),...(this.stripTimers||[])])clearTimeout(timer);
    for(const leaf of this.app.workspace.getLeavesOfType?.('markdown')||[])leaf.view?.containerEl?.querySelectorAll?.('.atlas-note-strip').forEach(el=>el.remove());
  }
};
