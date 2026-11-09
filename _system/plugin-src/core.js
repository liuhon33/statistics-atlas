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
