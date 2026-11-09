/* Statistics Atlas data model. No DOM, filesystem, network, or Obsidian dependency. */
const AtlasCore = (() => {
  const list = value => value == null ? [] : Array.isArray(value) ? value : [value];
  const clean = value => String(value || '').replace(/^!?\[\[/, '').replace(/\]\]$/, '').split('|')[0].split('#')[0].replace(/\\/g, '/').replace(/^\.\//, '').replace(/\.md$/i, '');
  const short = path => path.split('/').pop().replace(/\.md$/i, '');
  const hash = text => [...text].reduce((v, c) => Math.imul(v ^ c.charCodeAt(0), 16777619) >>> 0, 2166136261);
  const defaultColors = {probability:'#339cff', statistics:'#f3883b', computing:'#5dc977'};
  const createdKey = n => {const v=n.fm?.created; return v==null||v===''?'￿':v instanceof Date?v.toISOString().slice(0,10):String(v);};
  // Fixed learning-note slots on a halo outside the backbone (AGENTS A7). Slot i of a home is always in the same
  // place: rows step outward, columns fill the home's slice centre-out. A level-5 home gets one column; a broader
  // home spreads across the arc of its descendant leaves. Units: HALO_GAP and ROW radial, SLOT tangential.
  const HALO_GAP=60, ROW=20, SLOT=18, JOG=5;
  function haloSlots(backbone,positions){
    const kids=new Map();backbone.forEach(n=>{if(n.parent){if(!kids.has(n.parent))kids.set(n.parent,[]);kids.get(n.parent).push(n.id);}});
    const angle=id=>Math.atan2(positions[id].y,positions[id].x), wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
    const leaves=id=>{const k=(kids.get(id)||[]).filter(c=>positions[c]);return k.length?k.flatMap(leaves):[id];};
    const R0=Math.max(0,...backbone.filter(n=>positions[n.id]).map(n=>Math.hypot(positions[n.id].x,positions[n.id].y)))+HALO_GAP;
    const slices=new Map();
    const slice=home=>{if(!slices.has(home)){const h=angle(home),d=leaves(home).map(id=>wrap(angle(id)-h)),lo=Math.min(...d),hi=Math.max(...d);
      slices.set(home,{centre:h+(lo+hi)/2,cols:Math.max(1,Math.floor(((hi-lo)*R0+SLOT)/SLOT))});}return slices.get(home);};
    return (home,i)=>{const {centre,cols}=slice(home),row=Math.floor(i/cols),c=i%cols,k=c===0?0:c%2?(c+1)/2:-c/2;
      const r=R0+row*ROW,t=k*SLOT+(cols===1?(row%2?-JOG:JOG):0),a=centre+t/r;return {x:r*Math.cos(a),y:r*Math.sin(a)};};
  }
  function referenceLayout(nodes) {
    const children = new Map(nodes.map(n => [n.id, []]));
    nodes.forEach(n => {if(n.parent && children.has(n.parent)) children.get(n.parent).push(n);});
    const leaves = id => {const n = nodes.find(v=>v.id===id); return n.level===5 ? 1 : children.get(id).reduce((s,c)=>s+leaves(c.id),0);};
    const roots = nodes.filter(n=>n.level===1), weights=roots.map(n=>Math.pow(leaves(n.id),.65)), total=weights.reduce((a,b)=>a+b,0);
    const positions={}; let angle=-Math.PI*.83;
    function place(n,a,b) {
      const mid=(a+b)/2, r=[0,420,740,1040,1330,1620][n.level], j=n.level===5?35*Math.sin(nodes.indexOf(n)*2.4):0;
      positions[n.id]={x:Math.cos(mid)*(r+j),y:Math.sin(mid)*(r+j)};
      const kids=children.get(n.id), sum=kids.reduce((s,c)=>s+Math.max(1,leaves(c.id)),0);let t=a;
      kids.forEach(c=>{const w=(b-a)*Math.max(1,leaves(c.id))/sum;place(c,t,t+w);t+=w;});
    }
    roots.forEach((n,i)=>{const span=(Math.PI*2-.085*3)*weights[i]/total;place(n,angle,angle+span);angle+=span+.085;});
    return positions;
  }
  // Typed links live in note properties (Claude, 2026-11-08). The property is written on the page
  // where the arrow starts; `related` and `connections` are undirected conceptual links.
  const LINK_PROPERTIES={prerequisite_for:'prerequisite',applied_in:'application',related:'connection',connections:'connection'};
  const REASON_LINE=/^\s*-\s*\[\[([^\]]+)\]\]\s*[—–-]\s*(.*)$/;
  // Incremental record store (Claude, 2026-11-08, review fix 8). The map needs only a note's properties and
  // its "- [[target]] — reason" lines. Each record keeps just those, plus a signature of them; set() reports
  // whether anything the map uses actually changed, so edits to ordinary note text never trigger a rebuild.
  const reasonLines=body=>String(body||'').split(/\r?\n/).filter(line=>REASON_LINE.test(line)).join('\n');
  const stable=v=>Array.isArray(v)?'['+v.map(stable).join(',')+']':v&&typeof v==='object'?'{'+Object.keys(v).sort().filter(k=>v[k]!==undefined).map(k=>JSON.stringify(k)+':'+stable(v[k])).join(',')+'}':JSON.stringify(v===undefined?null:v);
  const needsBody=fm=>!!fm&&Object.keys(LINK_PROPERTIES).some(k=>fm[k]!=null&&fm[k]!=='');
  class RecordStore {
    constructor(){this.map=new Map();this.version=0;}
    set(path,frontmatter,body){
      const fm=frontmatter||{},reasons=needsBody(fm)?reasonLines(body):'',sig=stable(fm)+'\0'+reasons,old=this.map.get(path);
      if(old&&old.sig===sig)return false;
      this.map.set(path,{path,frontmatter:fm,body:reasons,sig});this.version++;return true;
    }
    delete(path){if(!this.map.delete(path))return false;this.version++;return true;}
    deletePrefix(prefix){let changed=false;for(const path of [...this.map.keys()])if(path.startsWith(prefix))changed=this.delete(path)||changed;return changed;}
    has(path){return this.map.has(path);}
    paths(){return [...this.map.keys()];}
    records(){return [...this.map.values()];}
  }
  function compile(records, layout) {
    const issues=[], nodes=[], byId=new Map(), byPath=new Map(), byName=new Map();
    const originals=new Map((layout.order||[]).map((id,i)=>[id,{order:i}]));
    for(const record of records) {
      const fm=record.frontmatter||{}, path=record.path.replace(/\\/g,'/');
      if(path.startsWith('.')) continue;
      const system=path.startsWith('_system/') || path.startsWith('raw/') || path.startsWith('assets/') || ['AGENTS.md','CLAUDE.md','Start Here.md','Welcome.md'].includes(path);
      // Layer: an explicit `layer:` wins; when it is missing the folder fills the gap (Claude, 2026-11-08, review fix 5).
      const folderLayer=system?'auxiliary':path.startsWith('Learning/')?'learning':path.startsWith('Backbone/')?'backbone':'auxiliary';
      const declared=fm.layer==null||fm.layer===''?null:String(fm.layer);
      let layer=folderLayer;
      if(!system&&declared){
        if(!['backbone','learning','auxiliary'].includes(declared))issues.push(`Unknown layer "${declared}" in ${path}; using its folder (${folderLayer}) instead`);
        else{layer=declared;if(declared!==folderLayer)issues.push(`Layer "${declared}" does not match its folder (${folderLayer}): ${path}`);}
      }else if(!system&&folderLayer!=='auxiliary')issues.push(`Missing layer property; treated as ${folderLayer} from its folder: ${path}`);
      const id=String(fm.id || 'file:'+path), original=originals.get(id);
      if(byId.has(id)){issues.push(`Duplicate ID ${id}: ${path}`);continue;}
      const n={id,path,label:String(fm.title||short(path)),layer,level:layer==='backbone'?Number(fm.level):null,
        core:String(fm.subject||''),stage:String(fm.study_band||''),aliases:list(fm.aliases).map(String),
        noteTypes:list(fm.note_types).map(String),order:original?.order??(10000+hash(id)/1e9),
        fm, body:record.body||'', raw:path.startsWith('raw/'), source:fm.role==='source' || path.startsWith('raw/'), url:fm.url||null};
      if(layer==='backbone' && (!Number.isInteger(n.level)||n.level<1||n.level>5)) issues.push(`Invalid backbone level: ${path}`);
      nodes.push(n);byId.set(id,n);byPath.set(clean(path).toLowerCase(),n);
      const key=short(path).toLowerCase();if(!byName.has(key))byName.set(key,[]);byName.get(key).push(n);
    }
    const resolve=(value,source)=>{
      if(value==null || value==='')return null;
      const key=clean(value), exact=byId.get(key)||byPath.get(key.toLowerCase());
      if(exact)return exact;
      const names=byName.get(key.toLowerCase())||[];
      if(names.length===1)return names[0];
      issues.push(`${names.length?'Ambiguous':'Missing'} link ${value} in ${source}`);return null;
    };
    for(const n of nodes) {
      n.parent=n.layer==='backbone'?resolve(n.fm.parent,n.path)?.id||null:null;
      n.home=n.layer==='learning'?resolve(n.fm.primary_home,n.path)?.id||null:null;
      if(n.layer==='backbone' && n.level>1 && (!n.parent||byId.get(n.parent)?.level!==n.level-1))issues.push(`Parent/level mismatch: ${n.path}`);
      if(n.layer==='learning' && (!n.home||byId.get(n.home)?.layer!=='backbone'))issues.push(`Learning note needs one backbone primary_home: ${n.path}`);
    }
    const lineage=id=>{
      const result=[],seen=new Set();let n=byId.get(id);
      if(n?.layer==='learning'){const note=n;n=byId.get(n.home);result.unshift(note);}
      while(n){if(seen.has(n.id)){issues.push(`Parent cycle at ${n.id}`);break;}seen.add(n.id);result.unshift(n);n=byId.get(n.parent);}
      return result;
    };
    for(const n of nodes){
      if(n.layer!=='auxiliary'){
        const chain=lineage(n.id), root=chain.find(v=>v.layer==='backbone'&&v.level===1);
        if(root)n.core=root.id;
        n.ancestry=chain.map(v=>v.label).join(' → ');
      }else n.ancestry='Auxiliary material';
    }
    const edges=[], keys=new Set();
    const add=(source,target,type,reason='')=>{
      const a=byId.get(source),b=byId.get(target);if(!a||!b||source===target)return;
      const key=type==='connection'?[type,...[source,target].sort()].join('\0'):[type,source,target].join('\0');
      if(keys.has(key))return;keys.add(key);
      const scope=a.layer==='auxiliary'||b.layer==='auxiliary'?'auxiliary':a.layer==='learning'||b.layer==='learning'?'learning':'backbone';
      edges.push({source,target,type,reason,scope});
    };
    function reasonFor(n,target){
      for(const line of n.body.split(/\r?\n/)){
        const match=line.match(REASON_LINE);
        if(match && clean(match[1]).toLowerCase()===clean(target.path).toLowerCase())return match[2];
      }
      return '';
    }
    for(const n of nodes){
      if(n.parent)add(n.parent,n.id,'contains','Contains this topic.');
      if(n.home)add(n.home,n.id,'attachment','Primary backbone home.');
      if(n.layer==='backbone'&&list(n.fm.connections).length)issues.push(`Backbone links need a type (prerequisite_for, applied_in or related), not connections: ${n.path}`);
      for(const [property,type] of Object.entries(LINK_PROPERTIES))for(const value of list(n.fm[property])){
        const other=resolve(value,n.path);if(!other)continue;
        const reason=reasonFor(n,other);
        add(n.id,other.id,type,reason);
        if(!reason && n.layer!=='auxiliary')issues.push(`Connection needs a one-line reason: ${n.label} → ${other.label}`);
      }
      for(const value of list(n.fm.sources)){
        if(/^https?:\/\//i.test(value))continue;
        const source=resolve(value,n.path);if(source)add(n.id,source.id,'source','Source / provenance.');
      }
    }
    const rank={backbone:0,learning:1,auxiliary:2};
    nodes.sort((a,b)=>rank[a.layer]-rank[b.layer]||(a.layer==='backbone'?a.order-b.order:a.id.localeCompare(b.id)));
    const positions={};
    for(const n of nodes.filter(n=>n.layer==='backbone')){
      if(layout.positions[n.id])positions[n.id]={...layout.positions[n.id]};
      else {
        const home=positions[n.parent]||layout.positions[n.parent]||{x:0,y:0},a=hash(n.id)/4294967296*Math.PI*2;
        positions[n.id]={x:home.x+70*Math.cos(a),y:home.y+70*Math.sin(a)};
        issues.push(`Layout preview only; approve and save a position for new backbone node: ${n.label}`);
      }
    }
    const attached=new Map();
    for(const n of nodes.filter(n=>n.layer==='learning')){const key=n.home||'_unassigned';if(!attached.has(key))attached.set(key,[]);attached.get(key).push(n);}
    // Learning-note halo (Claude, 2026-11-08, AGENTS A7, review item 11). Notes sit on a ring just outside the
    // outermost backbone dot, inside their home's own slice, in fixed slots ordered by `created` then id, so a
    // newer note takes the next slot and never moves older ones. Slot geometry depends only on the backbone.
    const slotOf=haloSlots(nodes.filter(n=>n.layer==='backbone'),positions);
    for(const [home,group] of attached){
      group.sort((a,b)=>createdKey(a).localeCompare(createdKey(b))||a.id.localeCompare(b.id));
      if(!positions[home]){const p={x:2200,y:1200};group.forEach((n,i)=>{const a=i*2.3999632297,r=65+22*Math.sqrt(i);positions[n.id]={x:p.x+r*Math.cos(a),y:p.y+r*Math.sin(a)};});continue;}
      group.forEach((n,i)=>{positions[n.id]=slotOf(home,i);});
    }
    const sourceCounts=new Map(),admin=[];
    for(const n of nodes.filter(n=>n.layer==='auxiliary')){
      const citing=edges.filter(e=>e.type==='source'&&e.target===n.id).map(e=>byId.get(e.source)).sort((a,b)=>(a.layer==='learning'?0:1)-(b.layer==='learning'?0:1)||(b.level||0)-(a.level||0)||a.id.localeCompare(b.id));
      if(n.source&&citing.length&&positions[citing[0].id]){
        const home=citing[0],p=positions[home.id],i=sourceCounts.get(home.id)||0;sourceCounts.set(home.id,i+1);
        const a=Math.atan2(p.y,p.x)+.6+i*.75;positions[n.id]={x:p.x+(105+16*i)*Math.cos(a),y:p.y+(105+16*i)*Math.sin(a)};
      }else admin.push(n);
    }
    // Administration cluster (Claude, 2026-11-08, review item 15). It used to sit at x≈2400, far right of the web, so
    // Fit in Everything shrank the web by about a fifth. It now fills the empty top-right corner just outside
    // everything placed so far, so the web plus the cluster still fit in roughly the web's own bounding square.
    if(admin.length){
      const placed=Object.values(positions),R=placed.length?Math.max(...placed.map(p=>Math.hypot(p.x,p.y))):0,step=44;
      const D=R+70+step*Math.sqrt(admin.length),cx=D*Math.SQRT1_2,cy=-D*Math.SQRT1_2;
      admin.forEach((n,i)=>{const a=i*2.3999632297,r=step*Math.sqrt(i+.5);positions[n.id]={x:cx+r*Math.cos(a),y:cy+r*Math.sin(a)};});
    }
    const children=new Map(nodes.map(n=>[n.id,[]]));nodes.forEach(n=>{if(n.parent&&children.has(n.parent))children.get(n.parent).push(n.id);});
    return {nodes,edges,positions,byId,children,lineage,issues:[...new Set(issues)],colors:layout.colors||defaultColors};
  }
  // Views: backbone ⊂ learning ⊂ everything, plus 'notes' (Claude, 2026-11-08, AGENTS A12): learning notes alone and
  // only the links between them. The backbone is hidden, not removed, so every note keeps its My learning position;
  // a focused branch still limits the view to notes homed in that branch.
  const MODES=['backbone','learning','everything','notes'];
  function visible(model,mode='backbone',depth=5,focus=null){
    const roots=new Set();
    if(focus){const visit=id=>{if(roots.has(id))return;roots.add(id);(model.children.get(id)||[]).forEach(visit);};visit(focus);}
    const allowed=new Set(model.nodes.filter(n=>{
      if(n.layer==='backbone')return mode!=='notes'&&n.level<=depth&&(!focus||roots.has(n.id));
      if(n.layer==='learning')return mode!=='backbone'&&(!focus||roots.has(n.home));
      return mode==='everything';
    }).map(n=>n.id));
    const nodes=model.nodes.filter(n=>allowed.has(n.id)),edges=model.edges.filter(e=>allowed.has(e.source)&&allowed.has(e.target));
    return {nodes,edges};
  }
  // Live page block (Claude, 2026-11-08, AGENTS A2). Everything here is derived from note properties at
  // render time, so the page can never disagree with the map. Nothing is written back to the note.
  const LINKED_TYPES=new Set(['prerequisite','application','connection']);
  function pageLinks(model,id){
    const n=model.byId.get(id);if(!n)return null;
    const topics=(model.children.get(id)||[]).map(c=>model.byId.get(c)).filter(Boolean);
    const inbound=[],notes=new Map();
    for(const e of model.edges){
      if(e.target!==id)continue;
      const other=model.byId.get(e.source);if(!other||other.layer==='auxiliary')continue;
      if(e.type==='attachment')continue;
      if(!LINKED_TYPES.has(e.type))continue;
      if(other.layer==='learning'&&n.layer==='backbone'){if(!notes.has(other.id))notes.set(other.id,{node:other,how:'linked',reason:e.reason});}
      else inbound.push({node:other,type:e.type,reason:e.reason});
    }
    for(const other of model.nodes)if(other.layer==='learning'&&other.home===id)notes.set(other.id,{node:other,how:'home',reason:''});
    const rank={home:0,linked:1};
    return {node:n,topics,inbound,notes:[...notes.values()].sort((a,b)=>rank[a.how]-rank[b.how]||a.node.label.localeCompare(b.node.label))};
  }
  return {compile,visible,MODES,referenceLayout,clean,hash,pageLinks,RecordStore,reasonLines,needsBody,stable};
})();
if(typeof module!=='undefined')module.exports=AtlasCore;

/* Shared canvas interface, used unchanged by the Obsidian view and browser QA. */
const AtlasUI = (() => {
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n;};
  class Atlas {
    constructor(host,model,options={},core){
      this.host=host;this.model=model;this.options=options;this.core=core;
      this.mode='backbone';this.depth=5;this.focus=null;this.selected=null;this.hover=null;this.camera={x:0,y:0,k:1};this.fitted=false;
      host.classList.add('statistics-atlas');host.replaceChildren();this.panelOpen=true;
      // Review item 15 (Claude, 2026-11-08): one compact toolbar row, the map takes all remaining height, legend and
      // status float in the map's empty bottom corners, and topic browser and map checks live in a collapsible panel.
      // The old stack (title, count, controls, results, legend, status, map, outline, checks) took about 270 px.
      const bar=el('div','sa-toolbar');bar.setAttribute('role','toolbar');bar.setAttribute('aria-label','Atlas controls');
      const switcher=el('div','sa-switch');switcher.setAttribute('role','group');switcher.setAttribute('aria-label','Map view');this.modes={};
      for(const [id,label,tip] of [['backbone','Backbone','The 756-topic backbone only'],['learning','My learning','Backbone plus my learning notes'],['everything','Everything','Also sources and vault administration'],['notes','Notes only','Only my learning notes and the links between them, without the backbone']]){const b=this.button(label,()=>{this.mode=id;this.update();});b.title=tip;b.setAttribute('aria-pressed',String(id===this.mode));this.modes[id]=b;switcher.append(b);}bar.append(switcher);
      const find=el('div','sa-find');this.search=el('input','sa-search');this.search.type='search';this.search.placeholder='Find a topic, alias or note…';this.search.setAttribute('aria-label','Search the atlas');
      this.results=el('div','sa-results');this.results.setAttribute('aria-label','Search results');this.results.addEventListener('mousedown',e=>e.preventDefault());find.append(this.search,this.results);bar.append(find);
      this.search.addEventListener('input',()=>this.searchResults());this.search.addEventListener('focus',()=>this.searchResults());this.search.addEventListener('blur',()=>this.results.replaceChildren());
      this.search.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();this.results.querySelector('button')?.click();}else if(e.key==='Escape'){this.search.value='';this.results.replaceChildren();}});
      this.depthSelect=el('select','sa-depth');this.depthSelect.setAttribute('aria-label','Visible levels');this.depthSelect.title='Visible levels';for(let i=1;i<=5;i++){const o=el('option','',i===5?'All levels':i===1?'Level 1':`Levels 1–${i}`);o.value=i;this.depthSelect.append(o);}this.depthSelect.value=5;
      this.depthSelect.addEventListener('change',()=>{this.depth=Number(this.depthSelect.value);if(this.focus&&this.model.byId.get(this.focus)?.level>this.depth)this.focus=null;this.update();});bar.append(this.depthSelect);
      const tools=el('div','sa-tools');this.panelToggle=this.iconButton('panel-right','▥','Show or hide the side panel',()=>{this.setPanel(!this.panelOpen);this.options.onStateChange?.();});
      tools.append(this.iconButton('home','⌂','Whole web',()=>{this.focus=null;this.selected=null;this.depth=5;this.depthSelect.value=5;this.update();this.fit();}),this.iconButton('maximize','⤢','Fit visible',()=>this.fit()),this.iconButton('zoom-out','−','Zoom out',()=>this.zoom(.75,this.width/2,this.height/2)),this.iconButton('zoom-in','+','Zoom in',()=>this.zoom(1.33,this.width/2,this.height/2)),this.panelToggle);
      bar.append(tools);host.append(bar);
      const main=el('div','sa-main');this.stage=el('div','sa-stage');this.canvas=el('canvas');this.canvas.setAttribute('role','img');const desc=el('span','sa-sr','Statistics network. Search and the topic browser provide keyboard navigation.');desc.id='sa-desc-'+Math.random().toString(36).slice(2);this.stage.append(desc);this.canvas.setAttribute('aria-labelledby',desc.id);this.stage.append(this.canvas);this.tooltip=el('div','sa-tooltip');this.stage.append(this.tooltip);
      const overlay=el('div','sa-overlay'),legend=el('div','sa-legend');for(const [id,label] of [['probability','Probability & foundations'],['statistics','Inference & modeling'],['computing','Computing & learning']]){const item=el('span','');const dot=el('i','sa-dot');dot.style.background=model.colors[id];item.append(dot,document.createTextNode(label));legend.append(item);}
      legend.append(el('span','sa-shapes','● backbone · ○ learning · ■ auxiliary'));this.status=el('div','sa-status');this.status.setAttribute('aria-live','polite');overlay.append(legend,this.status);this.stage.append(overlay);main.append(this.stage);
      this.panel=el('aside','sa-panel');this.panel.setAttribute('aria-label','Selected topic details');this.panelBody=el('div','sa-panel-body');this.panel.append(this.panelBody);
      this.outline=el('details','sa-outline');this.outline.append(el('summary','','Browse all topics'));this.tree=el('div','sa-tree');this.outline.append(this.tree);this.panel.append(this.outline);
      this.outline.addEventListener('toggle',()=>{if(this.outline.open&&!this.tree.childElementCount)this.buildTree();});
      this.issues=el('details','sa-issues');this.issueSummary=el('summary','','Map checks');this.issues.append(this.issueSummary);this.issueBody=el('div');this.issues.append(this.issueBody);this.panel.append(this.issues);
      main.append(this.panel);host.append(main);
      this.ctx=this.canvas.getContext('2d');this.attachCanvas();
      this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(this.stage);
      this.themeObserver=new MutationObserver(()=>{this._theme=null;this._labels=null;this.draw();});this.themeObserver.observe(document.body,{attributes:true,attributeFilter:['class','style']});
      this.update();this.resize();
    }
    button(label,fn,aria){const b=el('button','sa-button',label);b.type='button';if(aria)b.setAttribute('aria-label',aria);b.addEventListener('click',fn);return b;}
    // Icon from Obsidian's set when the host passes setIcon; plain text glyph otherwise (browser QA).
    iconButton(icon,glyph,label,fn){const b=this.button('',fn,label);b.classList.add('sa-icon');b.title=label;if(this.options.setIcon)this.options.setIcon(b,icon);if(!b.firstChild)b.textContent=glyph;return b;}
    setPanel(open){this.panelOpen=!!open;this.host.classList.toggle('sa-panel-closed',!this.panelOpen);this.panelToggle.setAttribute('aria-pressed',String(this.panelOpen));}
    updateModel(model){this.model=model;if(this.selected&&!model.byId.has(this.selected))this.selected=null;if(this.focus&&!model.byId.has(this.focus))this.focus=null;this.tree.replaceChildren();if(this.outline.open)this.buildTree();this.update();this.searchResults();}
    update(){
      const selectedNode=this.model.byId.get(this.selected);
      if(selectedNode&&((this.mode==='backbone'&&selectedNode.layer!=='backbone')||(this.mode==='learning'&&selectedNode.layer==='auxiliary')))this.selected=selectedNode.home||null;
      // Notes only (Claude, 2026-11-08, AGENTS A12): a selected topic or record is not on this view, so it is cleared.
      const notesOnly=this.mode==='notes';if(selectedNode&&notesOnly&&selectedNode.layer!=='learning')this.selected=null;
      this.visible=this.core.visible(this.model,this.mode,this.depth,this.focus);
      for(const [id,b] of Object.entries(this.modes))b.setAttribute('aria-pressed',String(id===this.mode));
      this.depthSelect.disabled=notesOnly;this.depthSelect.title=notesOnly?'Levels apply to backbone topics, which this view hides':'Visible levels';
      this.search.placeholder=notesOnly?'Find one of my notes…':'Find a topic, alias or note…';
      const counts={backbone:0,learning:0,auxiliary:0};this.model.nodes.forEach(n=>counts[n.layer]++);
      this.status.textContent=`${counts.backbone} topics · ${counts.learning} notes · showing ${this.visible.nodes.length} nodes, ${this.visible.edges.length} links`+(this.focus?' · focused branch':'')+((this.mode==='learning'||notesOnly)&&!counts.learning?' · no learning notes yet':'')+(notesOnly&&this.focus&&counts.learning&&!this.visible.nodes.length?' · no notes in this branch':'');
      const issues=this.model.issues.length;this.issueBody.replaceChildren();for(const issue of this.model.issues)this.issueBody.append(el('p','',issue));this.issues.hidden=!issues;this.issueSummary.textContent=`Map checks (${issues})`;
      this.panelToggle.classList.toggle('sa-flag',!!issues);this.panelToggle.title=issues?`Show or hide the side panel · ${issues} map check${issues>1?'s':''}`:'Show or hide the side panel';
      this.renderPanel();this.draw();
    }
    select(id,focus=false){
      const n=this.model.byId.get(id);if(!n)return;this.selected=id;this.hover=null;
      if(n.layer==='learning'&&this.mode==='backbone')this.mode='learning';if(n.layer==='auxiliary')this.mode='everything';
      if(n.layer==='backbone'&&this.mode==='notes')this.mode='learning'; // a topic picked from the panel is shown with its notes
      if(n.layer==='backbone')this.depth=Math.max(this.depth,n.level);else if(n.home)this.depth=Math.max(this.depth,this.model.byId.get(n.home)?.level||5);
      this.depthSelect.value=this.depth;
      if(focus){this.focus=n.layer==='backbone'?(n.level===5?n.parent:n.id):null;}
      else if(this.focus&&!this.core.visible(this.model,this.mode,this.depth,this.focus).nodes.some(v=>v.id===id))this.focus=null;
      this.update();if(focus)this.fit();else {const p=this.screen(id);if(p&&(p.x<30||p.x>this.width-30||p.y<30||p.y>this.height-30))this.center(id);}
    }
    searchResults(){
      this.results.replaceChildren();const q=this.search.value.trim().toLowerCase();if(!q)return;
      const notesOnly=this.mode==='notes',pool=notesOnly?this.model.nodes.filter(n=>n.layer==='learning'):this.model.nodes;
      const matches=pool.filter(n=>[n.label,...n.aliases,n.id].some(s=>s.toLowerCase().includes(q))).sort((a,b)=>(a.label.toLowerCase()===q?-1:0)-(b.label.toLowerCase()===q?-1:0)).slice(0,24);
      if(!matches.length)this.results.append(el('span','sa-muted',notesOnly?'No matching notes.':'No matching topics.'));
      matches.forEach(n=>this.results.append(this.button(`${n.label} · ${n.layer==='backbone'?'L'+n.level:n.layer}`,()=>{this.select(n.id,n.layer==='backbone');this.search.value='';this.results.replaceChildren();})));
    }
    renderPanel(){
      this.panelBody.replaceChildren();const n=this.model.byId.get(this.selected);
      if(!n&&this.mode==='notes'){
        // Notes only (Claude, 2026-11-08, AGENTS A12): the panel lists the visible notes by subject instead of the backbone roots.
        const notes=this.visible.nodes.filter(v=>v.layer==='learning'),roots=this.model.nodes.filter(v=>v.layer==='backbone'&&v.level===1),focus=this.model.byId.get(this.focus);
        this.panelBody.append(el('div','sa-eyebrow',`MY LEARNING · ${notes.length} NOTE${notes.length===1?'':'S'}`),el('h3','','My notes'));
        this.panelBody.append(el('p','sa-muted',notes.length?'Only your learning notes, each where it sits in My learning. Dotted lines join notes that link to each other. Select a note to see its home and links to backbone topics.':focus?'None of your notes is homed in this branch.':'No learning notes yet.'));
        if(focus){this.panelBody.append(el('p','sa-muted',`Showing notes in ${focus.label}.`),this.button('Show all my notes',()=>{this.focus=null;this.update();}));}
        const byLabel=(a,b)=>a.label.localeCompare(b.label),known=new Set(roots.map(r=>r.id));
        for(const [title,group] of [...roots.map(r=>[r.label,notes.filter(v=>v.core===r.id)]),['Unattached',notes.filter(v=>!known.has(v.core))]]){
          if(!group.length)continue;this.panelBody.append(el('h4','',title));group.sort(byLabel).forEach(v=>this.panelBody.append(this.button(v.label,()=>this.select(v.id))));}
        return;
      }
      if(!n){
        this.panelBody.append(el('div','sa-eyebrow','THREE SUBJECTS · FIVE LEVELS'),el('h3','','Explore the backbone'),el('p','sa-muted','Select a dot to inspect its path and connections. Search opens a focused branch. Double-click a dot to open its note.'));
        const roots=this.model.nodes.filter(n=>n.layer==='backbone'&&n.level===1);roots.forEach(n=>this.panelBody.append(this.button(n.label,()=>this.select(n.id,true))));
        this.panelBody.append(el('p','sa-muted','Hierarchy is solid. Prerequisites and applications are dashed lines with chevrons pointing toward the dependent topic. Conceptual connections are dotted.'));
        if(this.mode==='everything'){const d=el('details');d.append(el('summary','','Auxiliary records'));this.model.nodes.filter(v=>v.layer==='auxiliary').forEach(v=>d.append(this.button(v.label,()=>this.select(v.id))));this.panelBody.append(d);}return;
      }
      const tag=n.layer==='backbone'?`LEVEL ${n.level} · ${n.stage}`:n.layer==='learning'?`MY LEARNING · ${n.noteTypes.join(' · ')}`:'AUXILIARY';
      this.panelBody.append(el('div','sa-eyebrow',tag),el('h3','',n.label));
      const path=el('div','sa-path');this.model.lineage(n.id).forEach((p,i)=>{if(i)path.append(document.createTextNode(' › '));path.append(this.button(p.label,()=>this.select(p.id)));});this.panelBody.append(path);
      this.panelBody.append(this.button('Open note',()=>this.options.openNote?.(n.path)));
      if(n.layer==='backbone')this.panelBody.append(this.button('Focus this branch',()=>this.select(n.id,true)));
      if(n.home){const home=this.model.byId.get(n.home);this.panelBody.append(el('p','sa-muted','Primary home'),this.button(home.label,()=>this.select(home.id,true)));}
      const children=(this.model.children.get(n.id)||[]).map(id=>this.model.byId.get(id));if(children.length){this.panelBody.append(el('h4','','Topics'));children.forEach(c=>this.panelBody.append(this.button(`L${c.level} · ${c.label}`,()=>this.select(c.id,c.level<5))));}
      const links=this.model.edges.filter(e=>e.type!=='contains'&&e.type!=='source'&&(e.source===n.id||e.target===n.id)&&((this.mode!=='backbone')||e.scope==='backbone'));
      if(links.length){this.panelBody.append(el('h4','','Connections'));links.forEach(e=>{const other=this.model.byId.get(e.source===n.id?e.target:e.source),d=el('div','sa-connection');d.append(this.button(other.label,()=>this.select(other.id,true)),el('div','sa-muted',`${e.type} · ${e.reason||'Selected connection'}`));this.panelBody.append(d);});}
      const sources=this.model.edges.filter(e=>e.type==='source'&&e.source===n.id);if(sources.length){const d=el('details');d.append(el('summary','','Sources'));sources.forEach(e=>{const s=this.model.byId.get(e.target);d.append(this.button(s.label,()=>this.options.openNote?.(s.path)));});this.panelBody.append(d);}
      if(n.url){const a=el('a','', 'Read source');a.href=n.url;a.target='_blank';a.rel='noopener noreferrer';this.panelBody.append(a);}
      this.panelBody.append(el('div','sa-file',n.path));
    }
    buildTree(){
      const build=n=>{if(n.level===5)return this.button(n.label,()=>this.select(n.id,true));const d=el('details'),s=el('summary','',`L${n.level} · ${n.label}`);d.append(s,this.button('Explore '+n.label,()=>this.select(n.id,true)));for(const id of this.model.children.get(n.id)||[])d.append(build(this.model.byId.get(id)));return d;};
      this.model.nodes.filter(n=>n.layer==='backbone'&&n.level===1).forEach(n=>this.tree.append(build(n)));
    }
    // Keeps the map centre fixed when the stage changes size (side panel toggled, pane resized). (Claude, review item 15)
    resize(){const prev=this._stageSize;if(!this.syncSize())return;this._stageSize={w:this.width,h:this.height};if(!this.fitted){this.fit();this.fitted=true;}else{if(prev){this.camera.x+=(this.width-prev.w)/2;this.camera.y+=(this.height-prev.h)/2;}this.draw();}}
    // Claude, 2026-11-08: size and pixel ratio are re-checked on every paint, and the backing store is only reallocated when it changes.
    syncSize(){const w=this.stage.clientWidth,h=this.stage.clientHeight;if(!w||!h)return false;const dpr=window.devicePixelRatio||1,W=Math.round(w*dpr),H=Math.round(h*dpr);this.width=w;this.height=h;this.dpr=dpr;if(this.canvas.width!==W)this.canvas.width=W;if(this.canvas.height!==H)this.canvas.height=H;return true;}
    fit(){const pts=this.visible.nodes.map(n=>this.model.positions[n.id]).filter(Boolean);if(!pts.length||!this.width)return;let minX=Math.min(...pts.map(p=>p.x)),maxX=Math.max(...pts.map(p=>p.x)),minY=Math.min(...pts.map(p=>p.y)),maxY=Math.max(...pts.map(p=>p.y));const pad=70;
      this.camera.k=Math.min((this.width-pad*2)/Math.max(250,maxX-minX),(this.height-pad*2)/Math.max(250,maxY-minY));this.camera.x=this.width/2-(minX+maxX)/2*this.camera.k;this.camera.y=this.height/2-(minY+maxY)/2*this.camera.k;this.draw();}
    center(id){const p=this.model.positions[id];if(!p)return;this.camera.x=this.width/2-p.x*this.camera.k;this.camera.y=this.height/2-p.y*this.camera.k;this.draw();}
    zoom(factor,x,y){const old=this.camera.k;this.camera.k=Math.max(.04,Math.min(7,old*factor));this.camera.x=x-(x-this.camera.x)*this.camera.k/old;this.camera.y=y-(y-this.camera.y)*this.camera.k/old;this.draw();}
    screen(id){const p=this.model.positions[id];return p?{x:p.x*this.camera.k+this.camera.x,y:p.y*this.camera.k+this.camera.y}:null;}
    radius(n){return n.layer==='auxiliary'?3.3:n.layer==='learning'?4.2:n.level===1?12:Math.max(n.level===5?1.9:3,[0,15,9,6,4,2.7][n.level]*Math.min(1,this.camera.k*2));}
    // Claude, 2026-11-08: coalesce redraws to one per animation frame (dragging fired a full redraw per pointer event).
    // Direction chevrons spaced along a directed (prerequisite/application) edge, pointing from source to
    // target, so the direction reads along the whole line instead of only at the crowded target end. (Claude, 2026-11-08)
    chevrons(ctx,a,b,ra,rb,size){
      const dx=b.x-a.x,dy=b.y-a.y,len=Math.hypot(dx,dy),start=ra+size+4,end=len-rb-size-4;if(end<=start)return;
      const ux=dx/len,uy=dy/len,span=end-start,spacing=Math.max(34,size*8),count=Math.max(1,Math.floor(span/spacing)),step=span/count;
      ctx.setLineDash([]);ctx.beginPath();
      for(let i=0;i<count;i++){
        const t=start+step*(i+.5),x=a.x+ux*t,y=a.y+uy*t;
        if(x<-10||y<-10||x>this.width+10||y>this.height+10)continue;
        ctx.moveTo(x+ux*size,y+uy*size);ctx.lineTo(x-ux*size-uy*size*.75,y-uy*size+ux*size*.75);ctx.lineTo(x-ux*size*.35,y-uy*size*.35);ctx.lineTo(x-ux*size+uy*size*.75,y-uy*size-ux*size*.75);ctx.closePath();
      }
      ctx.fill();
    }
    // Review item 14 (Claude, 2026-11-08): theme colours and wrapped label sizes are cached between frames
    // (reset when Obsidian's theme changes) instead of re-reading styles and re-measuring every label per frame.
    theme(){if(!this._theme){const s=getComputedStyle(this.host);this._theme={fg:s.getPropertyValue('--sa-fg').trim()||'#dedede',bg:s.getPropertyValue('--sa-bg').trim()||'#202126',muted:s.getPropertyValue('--sa-muted').trim()||'#9497a3',font:s.fontFamily};}return this._theme;}
    labelBox(ctx,text,font){const cache=this._labels||(this._labels=new Map()),key=font+'\0'+text;let m=cache.get(key);
      if(!m){const lines=[];for(const fragment of text.split('\n')){let line='';for(const word of fragment.split(' ')){if(ctx.measureText(line+' '+word).width>155&&line){lines.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)lines.push(line);}
        m={lines,w:Math.max(...lines.map(l=>ctx.measureText(l).width))};cache.set(key,m);}return m;}
    draw(){if(this.frame)return;this.frame=requestAnimationFrame(()=>{this.frame=0;this.paint();});}
    // Review item 14 (Claude, 2026-11-08): while a dot is hovered or selected, the dimmed web does not change from
    // one hovered dot to the next, so it is drawn once into an off-screen bitmap (rebuilt when the camera, view,
    // size or theme changes) and each frame only copies it and draws the highlighted neighbourhood on top.
    paint(){
      if(!this.ctx||!this.visible||!this.syncSize())return;const active=this.hover||this.selected;this.theme();
      if(!active)this.paintScene(this.ctx,'full',null);
      else{const c=this.camera,key=[this.canvas.width,this.canvas.height,this.dpr,c.x,c.y,c.k,this.mode,this.depth,this.focus].join('|');
        if(!this._base||this._baseKey!==key||this._baseFor!==this.visible||this._baseTheme!==this._theme){
          const b=this._base||(this._base=document.createElement('canvas'));b.width=this.canvas.width;b.height=this.canvas.height;
          this.paintScene(b.getContext('2d'),'base',null);this._baseKey=key;this._baseFor=this.visible;this._baseTheme=this._theme;}
        const ctx=this.ctx;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.setLineDash([]);ctx.clearRect(0,0,this.canvas.width,this.canvas.height);ctx.drawImage(this._base,0,0);
        this.paintScene(ctx,'overlay',active);}
      this.canvas.dataset.mode=this.mode;this.canvas.dataset.visibleNodes=this.visible.nodes.length;this.canvas.dataset.visibleEdges=this.visible.edges.length;
      this.canvas.dataset.camera=JSON.stringify(this.camera);
    }
    // layer: 'full' (nothing highlighted), 'base' (the whole web dimmed, no labels: cached while hovering),
    // 'overlay' (only the highlighted neighbourhood and labels, drawn over the cached base).
    paintScene(ctx,layer,active){
      const {fg,bg,muted,font}=this.theme(),style={fontFamily:font},lit=layer==='base'||!!active;
      if(layer!=='overlay'){ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.setLineDash([]);ctx.clearRect(0,0,ctx.canvas.width,ctx.canvas.height);}ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.lineWidth=1.6;ctx.textBaseline='middle';const neighborhood=new Set(active?[active]:[]);
      const admin=this.visible.nodes.filter(n=>n.layer==='auxiliary'&&!n.source).map(n=>this.screen(n.id)).filter(Boolean);
      if(admin.length&&layer!=='overlay'){const x=Math.min(...admin.map(p=>p.x))-14,y=Math.min(...admin.map(p=>p.y))-14,w=Math.max(...admin.map(p=>p.x))-x+14,h=Math.max(...admin.map(p=>p.y))-y+14;ctx.strokeStyle=muted;ctx.globalAlpha=.35;ctx.setLineDash([3,4]);ctx.strokeRect(x,y,w,h);ctx.setLineDash([]);ctx.globalAlpha=1;ctx.fillStyle=fg;ctx.font=`12px ${style.fontFamily}`;ctx.textAlign='center';ctx.fillText('Vault administration',x+w/2,y-20);ctx.font=`10px ${style.fontFamily}`;ctx.fillStyle=muted;ctx.fillText(admin.length+' records',x+w/2,y-6);ctx.textAlign='left';}
      if(active)this.visible.edges.forEach(e=>{if(e.source===active||e.target===active){neighborhood.add(e.source);neighborhood.add(e.target);}});
      for(const e of this.visible.edges){const a=this.screen(e.source),b=this.screen(e.target);if(!a||!b)continue;const hit=!!active&&(e.source===active||e.target===active);if(layer==='overlay'&&!hit)continue;ctx.globalAlpha=lit?(hit?.85:.07):(e.type==='contains'?.27:e.scope==='auxiliary'?.13:.25);ctx.strokeStyle=hit?fg:muted;ctx.lineWidth=hit?1.8:.8;ctx.setLineDash(['contains','attachment'].includes(e.type)?[]:e.type==='connection'?[2,4]:[6,4]);ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke();
        if(['prerequisite','application'].includes(e.type)){ctx.globalAlpha=lit?(hit?.95:.07):.55;ctx.fillStyle=ctx.strokeStyle;this.chevrons(ctx,a,b,this.radius(this.model.byId.get(e.source)),this.radius(this.model.byId.get(e.target)),hit?5.5:3.5);}}
      ctx.setLineDash([]);
      for(const n of [...this.visible.nodes].sort((a,b)=>(b.level||6)-(a.level||6))){const p=this.screen(n.id);if(layer==='overlay'&&!neighborhood.has(n.id))continue;if(!p||p.x<-20||p.x>this.width+20||p.y<-20||p.y>this.height+20)continue;const hit=n.id===active,r=this.radius(n)+(hit?1:0);ctx.globalAlpha=lit&&!neighborhood.has(n.id)?.24:1;ctx.fillStyle=this.model.colors[n.core]||muted;ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=hit?2:1.6;ctx.beginPath();if(n.layer==='auxiliary')ctx.rect(p.x-r,p.y-r,r*2,r*2);else ctx.arc(p.x,p.y,r,0,Math.PI*2);if(n.layer==='learning')ctx.stroke();else ctx.fill();if(hit){ctx.beginPath();ctx.arc(p.x,p.y,r+5,0,Math.PI*2);ctx.stroke();}}
      if(layer==='base')return;ctx.globalAlpha=1;ctx.textBaseline='middle';const boxes=[];
      const priority=n=>n.id===active?-100:neighborhood.has(n.id)?-50:(n.level||6);
      const labels=this.visible.nodes.filter(n=>n.level<=2||this.focus||this.camera.k>.36||neighborhood.has(n.id)).sort((a,b)=>priority(a)-priority(b));
      for(const n of labels){const p=this.screen(n.id);if(!p||p.x<0||p.x>this.width||p.y<0||p.y>this.height)continue;if(active&&!neighborhood.has(n.id)&&n.level!==1)continue;
        if(n.layer==='auxiliary'&&!n.source&&this.camera.k<.5&&n.id!==active)continue;
        const major=n.level===1&&!this.focus,size=major?13:12;ctx.font=`${major?'600':'400'} ${size}px ${style.fontFamily}`;
        const full=major?{probability:'Probability\n& foundations',statistics:'Inference\n& modeling',computing:'Computing\n& learning'}[n.id]||n.label:n.label;
        const {lines,w}=this.labelBox(ctx,full,ctx.font),h=lines.length*15,off=this.radius(n)+6;
        const candidates=major?[{x:p.x-w/2,y:p.y+19}]:[{x:p.x+off,y:p.y-h/2},{x:p.x-w-off,y:p.y-h/2},{x:p.x-w/2,y:p.y+off},{x:p.x-w/2,y:p.y-h-off}];
        let choice=candidates.find(c=>c.x>=3&&c.y>=3&&c.x+w<this.width-3&&c.y+h<this.height-3&&!boxes.some(b=>c.x-3<b.x+b.w&&c.x+w+3>b.x&&c.y-2<b.y+b.h&&c.y+h+2>b.y));
        if(!choice){if(!major&&n.id!==active)continue;choice={x:Math.max(3,Math.min(this.width-w-3,candidates[0].x)),y:Math.max(3,Math.min(this.height-h-3,candidates[0].y))};}
        boxes.push({x:choice.x-3,y:choice.y-2,w:w+6,h:h+4});ctx.fillStyle=bg;ctx.globalAlpha=.92;ctx.fillRect(choice.x-3,choice.y-2,w+6,h+4);ctx.globalAlpha=1;ctx.fillStyle=fg;lines.forEach((l,i)=>ctx.fillText(l,choice.x,choice.y+7+i*15));
      }
    }
    hit(x,y){let id=null,best=Infinity;for(const n of this.visible.nodes){const p=this.screen(n.id);if(!p)continue;const d=Math.hypot(p.x-x,p.y-y);if(d<Math.max(8,this.radius(n)+4)&&d<best){best=d;id=n.id;}}return id;}
    attachCanvas(){
      const local=e=>{const b=this.canvas.getBoundingClientRect();return{x:e.clientX-b.left,y:e.clientY-b.top};};
      this.canvas.addEventListener('pointerdown',e=>{const p=local(e);this.drag={...p,cx:this.camera.x,cy:this.camera.y,moved:false};this.canvas.setPointerCapture(e.pointerId);});
      this.canvas.addEventListener('pointermove',e=>{const p=local(e);if(this.drag){const dx=p.x-this.drag.x,dy=p.y-this.drag.y;if(Math.hypot(dx,dy)>5)this.drag.moved=true;if(this.drag.moved){this.camera.x=this.drag.cx+dx;this.camera.y=this.drag.cy+dy;this.draw();}}else{const id=this.hit(p.x,p.y);this.tooltip.style.left=Math.min(p.x+12,this.width-230)+'px';this.tooltip.style.top=Math.max(3,p.y-35)+'px';if(id===this.hover)return;this.hover=id;const n=this.model.byId.get(id);this.tooltip.textContent=n?`${n.label} · ${n.layer==='backbone'?'L'+n.level+' · '+n.stage:n.layer}`:'';this.tooltip.hidden=!n;this.canvas.style.cursor=n?'pointer':'grab';this.draw();}});
      this.canvas.addEventListener('pointerup',e=>{const p=local(e),moved=this.drag?.moved;this.drag=null;if(!moved){const id=this.hit(p.x,p.y);if(id)this.select(id);}});
      this.canvas.addEventListener('contextrestored',()=>this.draw());
      this.canvas.addEventListener('pointercancel',()=>this.drag=null);
      this.canvas.addEventListener('pointerleave',()=>{this.hover=null;this.tooltip.hidden=true;this.draw();});
      this.canvas.addEventListener('dblclick',e=>{const p=local(e),n=this.model.byId.get(this.hit(p.x,p.y));if(n)this.options.openNote?.(n.path);});
      this.canvas.addEventListener('wheel',e=>{e.preventDefault();const p=local(e);this.zoom(Math.exp(-e.deltaY*.0015),p.x,p.y);},{passive:false});
    }
    destroy(){if(this.frame)cancelAnimationFrame(this.frame);this.resizeObserver?.disconnect();this.themeObserver?.disconnect();this.host.replaceChildren();}
  }
  return Atlas;
})();
if(typeof module!=='undefined')module.exports=AtlasUI;

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
