/* Refresh regression test for the statistics-atlas plugin (Claude, 2026-11-08, review fix 8).
 *
 * Loads the real bundle (.obsidian/plugins/statistics-atlas/main.js) against a minimal fake Obsidian app,
 * fed with the live vault export from validate.py, and replays editing events. It checks that the map is
 * rebuilt only when something it draws changed, that layout.json is read once, and that the incremental
 * model always equals a from-scratch compile.
 *
 *   python _system/tools/validate.py . --export "$TEMP/atlas-check.json"
 *   node _system/tools/test-refresh.cjs "$TEMP/atlas-check.json"
 */
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),Module=require('node:module');
const root=path.join(__dirname,'../..');
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const bundle=process.argv[3]||path.join(root,'.obsidian/plugins/statistics-atlas/main.js');
const layoutText=fs.readFileSync(path.join(root,'_system/layout.json'),'utf8');

// ---- fake Obsidian -------------------------------------------------------------------------------------
class TAbstractFile{constructor(p){this.path=p;}}
class TFile extends TAbstractFile{constructor(p){super(p);this.extension=p.includes('.')?p.split('.').pop():'';this.basename=p.split('/').pop().replace(/\.[^.]*$/,'');}}
class TFolder extends TAbstractFile{}
class Events{constructor(){this.h={};}on(n,f){(this.h[n]=this.h[n]||[]).push(f);return {n,f};}trigger(n,...a){for(const f of this.h[n]||[])f(...a);}}
const files=new Map(),meta=new Map(),texts=new Map(),counts={layoutReads:0,textReads:0};
const vault=Object.assign(new Events(),{
  getFiles:()=>[...files.values()],getAbstractFileByPath:p=>files.get(p)||null,
  cachedRead:async f=>{counts.textReads++;return texts.get(f.path)||'';},
  adapter:{read:async p=>{assert.equal(p,'_system/layout.json');counts.layoutReads++;return layoutText;}}});
const metadataCache=Object.assign(new Events(),{getFileCache:f=>meta.has(f.path)?{frontmatter:meta.get(f.path)}:null});
const workspace={getLeavesOfType:()=>[],onLayoutReady:()=>{},trigger:()=>{}};
// Lifecycle methods mirror Obsidian's Plugin/Component: Obsidian starts a plugin with load(), not onload().
const LIFECYCLE=['load','unload','loadCSS','onUserEnable','loadData','saveData','register','addChild','removeChild'];
class Plugin{constructor(app){this.app=app;}async load(){if(this._loaded)return;this._loaded=true;await this.onload();}unload(){}async loadCSS(){}onUserEnable(){}loadData(){}saveData(){}register(){}addChild(){}removeChild(){}registerView(){}registerMarkdownCodeBlockProcessor(){}addRibbonIcon(){}addCommand(c){(this.commands=this.commands||{})[c.id]=c;}registerEvent(){}}
const notices=[];
const obsidian={Plugin,ItemView:class{},Notice:class{constructor(m){notices.push(m);}},TFile,TFolder,MarkdownRenderChild:class{},Keymap:{isModEvent:()=>false},
  parseYaml:()=>{throw new Error('parseYaml should not be needed: every note is in the metadata cache');}};
const realRequire=Module.prototype.require;
Module.prototype.require=function(id){return id==='obsidian'?obsidian:realRequire.apply(this,arguments);};
const src=fs.readFileSync(bundle,'utf8')+'\nmodule.exports.__core=AtlasCore;';
const m=new Module(bundle);m.filename=bundle;m.paths=Module._nodeModulePaths(path.dirname(bundle));m._compile(src,bundle);
Module.prototype.require=realRequire;
const PluginClass=m.exports,core=m.exports.__core;

// ---- vault contents from the export -------------------------------------------------------------------
const put=(p,fm,body='')=>{files.set(p,new TFile(p));if(fm)meta.set(p,fm);else meta.delete(p);texts.set(p,'---\nx: 1\n---\n'+body);};
for(const r of data.records)put(r.path,r.frontmatter||{},r.body||'');
let compiles=0;const realCompile=core.compile;core.compile=(...a)=>{compiles++;return realCompile(...a);};
const fresh=()=>realCompile([...files.values()].filter(f=>f.extension==='md'||f.path.startsWith('raw/')||f.path.startsWith('assets/')||(f.extension==='json'&&f.path.startsWith('_system/Migrations/'))).map(f=>({path:f.path,frontmatter:meta.get(f.path)||{},body:(texts.get(f.path)||'').replace(/^---\nx: 1\n---\n/,'')})),JSON.parse(layoutText));
const same=(a,b)=>{
  const ids=x=>x.nodes.map(n=>[n.id,n.path,n.label,n.layer,n.parent,n.home].join('|')).sort();
  const es=x=>x.edges.map(e=>[e.type,e.source,e.target,e.reason,e.scope].join('|')).sort();
  assert.deepEqual(ids(a),ids(b));assert.deepEqual(es(a),es(b));assert.deepEqual([...a.issues].sort(),[...b.issues].sort());
  for(const n of b.nodes)assert.deepEqual(a.positions[n.id],b.positions[n.id]);
};

(async()=>{
  const app={vault,metadataCache,workspace},plugin=new PluginClass(app);
  // A subclass method with a lifecycle name would replace Obsidian's and break startup (it happened with load(file)).
  for(const name of LIFECYCLE)assert(!Object.prototype.hasOwnProperty.call(PluginClass.prototype,name),`plugin class overrides Obsidian's ${name}()`);
  await plugin.load();await plugin.ready;
  const step=async()=>{clearTimeout(plugin.timer);await plugin.refresh();clearTimeout(plugin.timer);return plugin.stats;};
  const results={};
  assert.equal(compiles,1);assert.equal(counts.layoutReads,1);same(plugin.model,fresh());
  // Publication regression: file-backed sources must survive the initial model load.
  for(const r of data.records.filter(r=>r.frontmatter?.role==='source'))
    assert(plugin.model.nodes.some(n=>n.path===r.path),`Source record not loaded: ${r.path}`);
  const kept=[...plugin.store.map.values()].reduce((s,r)=>s+r.body.length,0),total=data.records.reduce((s,r)=>s+(r.body||'').length,0);
  results.bodyCharsKept=kept;results.bodyCharsInVault=total;assert(kept<total/10);

  const plain=data.records.find(r=>r.frontmatter?.layer==='backbone'&&!core.needsBody(r.frontmatter)).path;
  const linked=data.records.find(r=>r.frontmatter?.layer==='backbone'&&core.needsBody(r.frontmatter)&&/ — /.test(r.body)).path;

  // 1. Typing in a note's text: no rebuild, and a note without link properties is not even read.
  let reads=counts.textReads;
  texts.set(plain,texts.get(plain)+'\nSome new prose.\n');metadataCache.trigger('changed',files.get(plain));
  assert.equal((await step()).rebuilt,false);assert.equal(counts.textReads,reads);
  // 2. Prose edit on a note that declares links: read, but no rebuild.
  texts.set(linked,texts.get(linked)+'\nA paragraph that is not a reason line.\n');metadataCache.trigger('changed',files.get(linked));
  assert.equal((await step()).rebuilt,false);
  // 3. Property order changes but values do not: no rebuild.
  meta.set(plain,Object.fromEntries(Object.entries(meta.get(plain)).reverse()));metadataCache.trigger('changed',files.get(plain));
  assert.equal((await step()).rebuilt,false);
  assert.equal(compiles,1);
  // 4. A reason line changes: rebuild, and the new reason is on the edge.
  texts.set(linked,texts.get(linked).replace(/ — .*/,' — Edited reason for the refresh test.'));metadataCache.trigger('changed',files.get(linked));
  assert.equal((await step()).rebuilt,true);assert(plugin.model.edges.some(e=>e.reason==='Edited reason for the refresh test.'));same(plugin.model,fresh());
  // 5. A property changes: rebuild, label updated.
  meta.set(plain,{...meta.get(plain),title:'Retitled in refresh test'});metadataCache.trigger('changed',files.get(plain));
  assert.equal((await step()).rebuilt,true);assert(plugin.model.nodes.some(n=>n.label==='Retitled in refresh test'));same(plugin.model,fresh());
  // 6. Obsidian finishes indexing: one full rescan with nothing new, so no rebuild; later 'resolved' events do nothing.
  metadataCache.trigger('resolved');let s=await step();assert.equal(s.full,true);assert.equal(s.rebuilt,false);
  metadataCache.trigger('resolved');assert.equal(plugin.fullPending,false);s=await step();assert.equal(s.full,false);assert.equal(s.rebuilt,false);
  // 7. A new learning note arrives (create, then the metadata cache entry): rebuild, attached to its home.
  const home=plugin.model.nodes.find(n=>n.id==='elbo').path.replace(/\.md$/,''),note='Learning/Refresh test note.md';
  put(note,{id:'refresh-test',layer:'learning',primary_home:`[[${home}]]`,note_types:['derivation']});
  vault.trigger('create',files.get(note));metadataCache.trigger('changed',files.get(note));
  assert.equal((await step()).rebuilt,true);assert.equal(plugin.model.byId.get('refresh-test').home,'elbo');same(plugin.model,fresh());
  // 8. Rename it: old path gone, new path present.
  const renamed='Learning/Renamed refresh note.md',f=files.get(note);files.delete(note);f.path=renamed;files.set(renamed,f);meta.set(renamed,meta.get(note));meta.delete(note);texts.set(renamed,texts.get(note));texts.delete(note);
  vault.trigger('rename',f,note);assert.equal((await step()).rebuilt,true);assert.equal(plugin.model.byId.get('refresh-test').path,renamed);same(plugin.model,fresh());
  // 9. Delete it.
  files.delete(renamed);meta.delete(renamed);texts.delete(renamed);vault.trigger('delete',f);
  assert.equal((await step()).rebuilt,true);assert(!plugin.model.byId.has('refresh-test'));same(plugin.model,fresh());
  // 10. A folder is renamed: full rescan of the moved notes.
  const folder=new TFolder('Learning/Moved');put('Learning/Moved/A.md',{id:'moved-a',layer:'learning',primary_home:`[[${home}]]`,note_types:['insight']});
  metadataCache.trigger('changed',files.get('Learning/Moved/A.md'));await step();
  const g=files.get('Learning/Moved/A.md');files.delete(g.path);meta.set('Learning/Moved2/A.md',meta.get(g.path));meta.delete(g.path);texts.set('Learning/Moved2/A.md',texts.get(g.path));g.path='Learning/Moved2/A.md';files.set(g.path,g);folder.path='Learning/Moved2';
  vault.trigger('rename',folder,'Learning/Moved');s=await step();assert.equal(s.full,true);assert.equal(plugin.model.byId.get('moved-a').path,'Learning/Moved2/A.md');same(plugin.model,fresh());
  // 11. layout.json is read once, and again only when it changes.
  assert.equal(counts.layoutReads,1);
  vault.trigger('modify',new TFile('_system/layout.json'));assert.equal((await step()).rebuilt,true);assert.equal(counts.layoutReads,2);
  vault.trigger('modify',new TFile('Backbone/whatever.md'));await step();assert.equal(counts.layoutReads,2);
  // 12. The manual Refresh command forces a full rescan and a layout re-read.
  await plugin.commands['refresh-atlas'].callback();assert.equal(counts.layoutReads,3);
  assert.deepEqual(notices,['Statistics atlas refreshed.']);
  // 13. Store semantics.
  const st=new core.RecordStore();
  assert.equal(st.set('a.md',{b:1,a:[1,2]},'x'),true);assert.equal(st.set('a.md',{a:[1,2],b:1},'y'),false);
  assert.equal(st.set('a.md',{a:[2,1],b:1},''),true);assert.equal(st.delete('a.md'),true);assert.equal(st.delete('a.md'),false);
  st.set('L/x.md',{},'');st.set('L/y.md',{},'');st.set('Lz.md',{},'');assert.equal(st.deletePrefix('L/'),true);assert.deepEqual(st.paths(),['Lz.md']);
  results.compiles=compiles;results.layoutReads=counts.layoutReads;
  console.log(JSON.stringify({passed:true,...results}));
})().catch(e=>{console.error(e);process.exit(1);});
