const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const core=require(process.argv[3]||path.join(__dirname,'../plugin-src/core.js'));
const data=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
// Two inputs (Claude, 2026-11-08, AGENTS A4; see _system/Claude/Validator.md):
// 1. `base`: a vault rebuilt in memory from the frozen baseline JSON. Exact counts (756/843, typed-link set,
//    page lists) are asserted on it, so they test the plugin code and never break when the real vault grows.
// 2. `data.records`: the live vault. Only rules that always hold are asserted on it (see the end of this file).
const KIND={prerequisite:'prerequisite_for',application:'applied_in',connection:'related'};
const base=(()=>{
  const by=new Map(data.baseline.nodes.map(n=>[n.id,n])),ref=id=>'Backbone/'+id;
  const label=n=>n.id==='elbo'?'ELBO':n.label;
  const recs=new Map(data.baseline.nodes.map(n=>[n.id,{path:ref(n.id)+'.md',frontmatter:{id:n.id,title:label(n),layer:'backbone',level:n.level,subject:n.core,study_band:n.stage,...(n.parent?{parent:'[['+ref(n.parent)+']]'}:{})},body:''}]));
  for(const e of data.baseline.edges){if(e.type==='contains')continue;const r=recs.get(e.source),k=KIND[e.type];
    (r.frontmatter[k]=r.frontmatter[k]||[]).push('[['+ref(e.target)+']]');r.body+=`- [[${ref(e.target)}|${label(by.get(e.target))}]] — ${e.reason}\n`;}
  return [...recs.values(),{path:'_system/Fixture record.md',frontmatter:{id:'fixture-aux'},body:''}];
})();
const model=core.compile(base,data.layout);
assert.equal(model.issues.length,0,model.issues.join('\n'));
assert.equal(core.visible(model,'backbone').nodes.length,756);
assert.equal(core.visible(model,'backbone').edges.length,843);
assert.equal(core.visible(model,'learning').nodes.length,756);
assert.equal(core.visible(model,'backbone',2).nodes.length,25);
assert.equal(core.visible(model,'backbone',1).nodes.length,3);
assert(core.visible(model,'everything').nodes.length>756);
const originalPositions=core.referenceLayout(data.baseline.nodes);
for(const n of data.baseline.nodes){assert(Math.abs(originalPositions[n.id].x-data.layout.positions[n.id].x)<1e-8);assert(Math.abs(originalPositions[n.id].y-data.layout.positions[n.id].y)<1e-8);}
// Typed links come from note properties and must match the frozen baseline exactly (Claude, 2026-11-08).
const typedKey=e=>e.type==='connection'?['connection',...[e.source,e.target].sort()].join('|'):[e.type,e.source,e.target].join('|');
const expectedTyped=new Set(data.baseline.edges.filter(e=>e.type!=='contains').map(typedKey));
const actualTyped=new Set(model.edges.filter(e=>['prerequisite','application','connection'].includes(e.type)&&e.scope==='backbone').map(typedKey));
assert.deepEqual([...actualTyped].sort(),[...expectedTyped].sort());
assert.deepEqual(['prerequisite','application','connection'].map(t=>model.edges.filter(e=>e.type===t&&e.scope==='backbone').length),[24,30,36]);
const untyped=core.compile(base.map(r=>r.frontmatter.id==='jensen'?{...r,frontmatter:{...r.frontmatter,connections:r.frontmatter.prerequisite_for,prerequisite_for:undefined}}:r),data.layout);
assert(untyped.issues.some(s=>s.includes('need a type')));
const paths=Object.fromEntries(model.nodes.map(n=>[n.id,n.path.replace(/\.md$/,'')]));
const w=id=>'[['+paths[id]+']]';
const fixture=[{path:'Learning/Test/Synthetic ELBO comparison.md',frontmatter:{id:'test-learning',title:'Synthetic learning fixture',layer:'learning',primary_home:w('elbo'),note_types:['question','derivation'],connections:[w('jensen'),w('kl'),w('importance')],sources:['[[raw/test-source.pdf]]']},body:['jensen','kl','importance'].map(id=>'- [['+paths[id]+'|'+id+']] — Selected test relationship.').join('\n')+'\nUnselected reference: '+w('probability')},
 {path:'Learning/Test/Second synthetic note.md',frontmatter:{id:'test-learning-2',layer:'learning',primary_home:w('elbo'),connections:['[[Learning/Test/Synthetic ELBO comparison]]'],sources:['[[raw/test-source.pdf]]']},body:'- [[Learning/Test/Synthetic ELBO comparison|Fixture]] — Compare two personal notes.'},
 {path:'raw/test-source.pdf',frontmatter:{layer:'auxiliary',role:'source'}}];
const extended=core.compile([...base,...fixture],data.layout);
assert.deepEqual(extended.issues,[]);
assert.equal(core.visible(extended,'backbone').nodes.length,756);assert.equal(core.visible(extended,'backbone').edges.length,843);
assert.equal(core.visible(extended,'learning').nodes.length,758);
assert.equal(core.visible(extended,'learning').edges.length,849); // 2 homes + 3 cross-links + 1 note-to-note.
assert(!core.visible(extended,'learning').edges.some(e=>e.type==='source'));
assert.equal(extended.edges.filter(e=>e.type==='source'&&e.target==='file:raw/test-source.pdf').length,2);
assert.equal(extended.nodes.filter(n=>n.path==='raw/test-source.pdf').length,1);
assert(!extended.edges.some(e=>e.source==='test-learning'&&e.target==='probability'));
for(const n of data.baseline.nodes)assert.deepEqual(extended.positions[n.id],model.positions[n.id]);
assert.equal(extended.byId.get('test-learning').core,'computing');
assert(extended.byId.get('test-learning').ancestry.endsWith('ELBO → Synthetic learning fixture'));
// Notes only (Claude, 2026-11-08, AGENTS A12): learning notes alone with only note-to-note links; levels do not
// filter notes; a focused branch keeps only notes homed in it.
assert(core.MODES.includes('notes'));
assert.equal(core.visible(model,'notes').nodes.length,0);assert.equal(core.visible(model,'notes').edges.length,0);
assert.deepEqual(core.visible(extended,'notes').nodes.map(n=>n.id).sort(),['test-learning','test-learning-2']);
assert.deepEqual(core.visible(extended,'notes').edges.map(e=>[e.type,e.source,e.target]),[['connection','test-learning-2','test-learning']]);
assert.equal(core.visible(extended,'notes',1).nodes.length,2);
assert.equal(core.visible(extended,'notes',5,'computing').nodes.length,2);
assert.equal(core.visible(extended,'notes',5,'probability').nodes.length,0);
// Live page block (Claude, 2026-11-08, AGENTS A2): lists are derived from properties and cover every edge exactly once.
const idOf=label=>model.nodes.find(n=>n.layer==='backbone'&&n.label===label).id;
const post=core.pageLinks(model,'posterior');
assert.deepEqual(post.topics.map(n=>n.label),['Prior and posterior','Marginal likelihood / evidence','Conjugate updating','Posterior summaries','Credible intervals','Posterior predictive distribution']);
assert.deepEqual(post.inbound.map(x=>x.node.label),['Bayes rule']);
assert(post.inbound[0].reason.startsWith('Bayes rule updates the prior'));
assert.deepEqual(core.pageLinks(model,'elbo').inbound.map(x=>x.node.id).sort(),['importance','jensen','kl']);
const backboneIds=model.nodes.filter(n=>n.layer==='backbone').map(n=>n.id);
assert.equal(backboneIds.reduce((s,id)=>s+core.pageLinks(model,id).topics.length,0),753);
assert.equal(backboneIds.reduce((s,id)=>s+core.pageLinks(model,id).inbound.length,0),90);
assert(backboneIds.every(id=>core.pageLinks(model,id).notes.length===0));
const elboNotes=core.pageLinks(extended,'elbo').notes;
assert.deepEqual(elboNotes.map(x=>[x.node.id,x.how]),[['test-learning-2','home'],['test-learning','home']]);
assert.deepEqual(core.pageLinks(extended,'jensen').notes.map(x=>[x.node.id,x.how]),[['test-learning','linked']]);
assert.deepEqual(core.pageLinks(extended,'test-learning').inbound.map(x=>x.node.id),['test-learning-2']);
assert.equal(core.pageLinks(model,'no-such-id'),null);
// Attached-notes strip and picker (Claude, 2026-11-09, AGENTS A16): notes homed here, homed anywhere below, or only
// linking here; each note once, in that priority. Learning notes and unknown ids have no list.
const att=id=>core.attachedNotes(extended,id),attIds=xs=>xs.map(x=>x.node.id);
assert(backboneIds.every(id=>{const a=core.attachedNotes(model,id);return !a.here.length&&!a.below.length&&!a.linked.length;}));
assert.deepEqual([attIds(att('elbo').here),att('elbo').below.length,att('elbo').linked.length],[['test-learning-2','test-learning'],0,0]);
let elboAncestors=0;
for(let id=extended.byId.get('elbo').parent;id;id=extended.byId.get(id).parent,elboAncestors++){
  const a=att(id);assert.deepEqual([a.here.length,attIds(a.below),a.linked.length],[0,['test-learning-2','test-learning'],0]);
  assert(a.below.every(x=>x.home.id==='elbo'));
}
assert.equal(elboAncestors,4);
assert.deepEqual([att('jensen').here.length,att('jensen').below.length,attIds(att('jensen').linked)],[0,0,['test-learning']]);
assert.equal(att('jensen').linked[0].reason,'Selected test relationship.');
assert.equal(att('test-learning'),null);assert.equal(att('no-such-id'),null);
const malformed=core.compile([...base,{path:'Learning/Bad.md',frontmatter:{id:'bad',layer:'learning',primary_home:'[[does-not-exist-fixture]]'}}],data.layout);
assert(malformed.issues.some(s=>s.includes('primary_home')));
// Learning-note halo (Claude, 2026-11-08, AGENTS A7, review item 11): notes sit outside the backbone, inside their
// home's slice, in fixed slots ordered by `created`; adding a newer note never moves older ones.
{
  const bb=model.nodes.filter(n=>n.layer==='backbone'),P=model.positions,ang=id=>Math.atan2(P[id].y,P[id].x);
  const outer=Math.max(...bb.map(n=>Math.hypot(P[n.id].x,P[n.id].y))),wrap=a=>Math.atan2(Math.sin(a),Math.cos(a));
  const leaf5=bb.filter(n=>n.level===5),home=leaf5[Math.floor(leaf5.length/2)].id,broad=bb.find(n=>n.level===3&&model.children.get(n.id).length>=3).id;
  const note=(id,h,created)=>({path:`Learning/Halo/${id}.md`,frontmatter:{id,layer:'learning',primary_home:w(h),...(created?{created}:{})},body:''});
  const six=['2026-01-06','2026-01-01','2026-01-04','2026-01-02','2026-01-05','2026-01-03'].map((d,i)=>note('h'+i,home,d));
  const four=[1,2,3,4].map(i=>note('b'+i,broad,'2026-02-0'+i));
  const halo=core.compile([...base,...six,...four],data.layout),Q=halo.positions,R=id=>Math.hypot(Q[id].x,Q[id].y);
  assert.deepEqual(halo.issues,[]);
  for(const n of bb)assert.deepEqual(Q[n.id],P[n.id]);
  const notes=[...six,...four].map(r=>r.frontmatter.id);
  for(const id of notes)assert(R(id)>=outer+50,`${id} should sit outside the outermost backbone dot`);
  for(const id of notes){for(const n of bb)assert(Math.hypot(Q[id].x-P[n.id].x,Q[id].y-P[n.id].y)>40,`${id} overlaps ${n.id}`);
    for(const o of notes)if(o!==id)assert(Math.hypot(Q[id].x-Q[o].x,Q[id].y-Q[o].y)>10,`${id} overlaps ${o}`);}
  const nearestLeaf=id=>leaf5.reduce((b,n)=>Math.abs(wrap(Math.atan2(Q[id].y,Q[id].x)-ang(n.id)))<Math.abs(wrap(Math.atan2(Q[id].y,Q[id].x)-ang(b.id)))?n:b).id;
  for(const r of six)assert.equal(nearestLeaf(r.frontmatter.id),home,'a level-5 home keeps its notes in its own slice');
  const byCreated=[...six].sort((a,b)=>a.frontmatter.created.localeCompare(b.frontmatter.created)).map(r=>r.frontmatter.id);
  assert.deepEqual([...byCreated].sort((a,b)=>R(a)-R(b)),byCreated,'earlier notes take inner slots');
  const subtree=id=>{const k=model.children.get(id)||[];return k.length?k.flatMap(subtree):[id];},h=ang(broad),d=subtree(broad).map(id=>wrap(ang(id)-h));
  for(const r of four){const a=wrap(Math.atan2(Q[r.frontmatter.id].y,Q[r.frontmatter.id].x)-h);assert(a>=Math.min(...d)-0.02&&a<=Math.max(...d)+0.02,'a broad home spreads notes over its own subtree');}
  assert(new Set(four.map(r=>Math.round(R(r.frontmatter.id)))).size===1,'a broad home fills one row before starting the next');
  const more=core.compile([...base,...six,...four,note('h-new',home,'2026-03-01'),note('h-undated',home)],data.layout);
  for(const id of notes)assert.deepEqual(more.positions[id],Q[id],`adding newer notes moved ${id}`);
  assert(Math.hypot(more.positions['h-undated'].x,more.positions['h-undated'].y)>Math.hypot(more.positions['h-new'].x,more.positions['h-new'].y),'undated notes go last');
}
// Layer fallback (Claude, 2026-11-08, review fix 5): a missing layer is filled from the folder, with a visible hint.
const layerCase=(p,fm)=>({path:p,frontmatter:{primary_home:w('elbo'),...fm},body:''});
const layered=core.compile([...base,
  layerCase('Learning/No layer.md',{id:'t-missing'}),
  layerCase('Learning/Typo layer.md',{id:'t-typo',layer:'lerning'}),
  layerCase('Learning/Explicit.md',{id:'t-ok',layer:'learning'}),
  layerCase('Elsewhere/Loose note.md',{id:'t-loose'}),
  layerCase('Elsewhere/Declared learning.md',{id:'t-declared',layer:'learning'}),
  layerCase('_system/Fake learning.md',{id:'t-system',layer:'learning'})],data.layout);
const L=id=>layered.byId.get(id).layer, says=(text,p)=>layered.issues.some(s=>s.includes(text)&&s.includes(p));
assert.equal(L('t-missing'),'learning');assert(says('Missing layer property','Learning/No layer.md'));
assert(core.visible(layered,'learning').nodes.some(n=>n.id==='t-missing'));
assert(!core.visible(layered,'backbone').nodes.some(n=>n.id==='t-missing'));
assert.equal(L('t-typo'),'learning');assert(says('Unknown layer "lerning"','Learning/Typo layer.md'));
assert.equal(L('t-ok'),'learning');assert(!layered.issues.some(s=>s.includes('Learning/Explicit.md')));
assert.equal(L('t-loose'),'auxiliary');assert(!layered.issues.some(s=>s.includes('Elsewhere/Loose note.md')));
assert.equal(L('t-declared'),'learning');assert(says('does not match its folder','Elsewhere/Declared learning.md'));
assert.equal(L('t-system'),'auxiliary');assert(!layered.issues.some(s=>s.includes('_system/Fake learning.md')));
for(const n of data.baseline.nodes)assert.deepEqual(layered.positions[n.id],model.positions[n.id]);
// Live vault: rules that hold however much it grows. A new backbone node without a saved position is only a
// layout warning (validate.py W1), so that message is not a failure here.
const live=core.compile(data.records,data.layout);
const liveIssues=live.issues.filter(s=>!s.startsWith('Layout preview only'));
assert.deepEqual(liveIssues,[],liveIssues.join('\n'));
for(const n of live.nodes.filter(n=>n.layer==='backbone'&&data.layout.positions[n.id]))assert.deepEqual(live.positions[n.id],data.layout.positions[n.id]);
const liveView=mode=>core.visible(live,mode).nodes;
assert(liveView('backbone').every(n=>n.layer==='backbone'));
assert(liveView('learning').every(n=>n.layer!=='auxiliary'));
assert.equal(liveView('backbone').length,live.nodes.filter(n=>n.layer==='backbone').length);
assert.equal(liveView('learning').length,live.nodes.filter(n=>n.layer!=='auxiliary').length);
assert(liveView('notes').every(n=>n.layer==='learning'));
assert.equal(liveView('notes').length,live.nodes.filter(n=>n.layer==='learning').length);
assert(core.visible(live,'notes').edges.every(e=>live.byId.get(e.source).layer==='learning'&&live.byId.get(e.target).layer==='learning'));
for(const n of live.nodes.filter(n=>n.layer==='learning'))assert.deepEqual(live.positions[n.home],core.compile(data.records.filter(r=>r.frontmatter?.layer!=='learning'&&!r.path.startsWith('Learning/')),data.layout).positions[n.home]);
// A16 on the live vault: each note is listed at its home and below every ancestor; no page lists a note twice.
for(const n of live.nodes.filter(n=>n.layer==='learning')){
  assert(core.attachedNotes(live,n.home).here.some(x=>x.node.id===n.id),`not listed at its home: ${n.path}`);
  for(let id=live.byId.get(n.home).parent;id;id=live.byId.get(id).parent)assert(core.attachedNotes(live,id).below.some(x=>x.node.id===n.id),`not listed below ${id}: ${n.path}`);
}
for(const n of live.nodes.filter(n=>n.layer==='backbone')){const a=core.attachedNotes(live,n.id),all=[...a.here,...a.below,...a.linked].map(x=>x.node.id);assert.equal(new Set(all).size,all.length,`duplicate in attached notes of ${n.id}`);}
// A17 new-note drafts: a draft for a live home compiles cleanly as a learning note at that home; taken names, empty
// titles and non-backbone homes are refused.
{
  const yaml=require('node:util');const homeNode=live.nodes.find(n=>n.layer==='backbone'&&n.level===5);
  const d=core.newNoteDraft(live,homeNode.id,'Synthetic draft: a/b?','2026-11-09');
  assert(!d.error,d.error);assert(d.path.startsWith('Learning/'+homeNode.path.split('/').slice(1,3).join('/')+'/'));
  assert.equal(d.path.split('/').pop(),'Synthetic draft- a-b-.md');assert(d.content.includes('status: draft'));
  const fm={};for(const line of d.content.split('\n---')[0].split('\n').slice(1)){const m=line.match(/^(\w+): (.*)$/);if(m)fm[m[1]]=m[2].startsWith('"')?JSON.parse(m[2]):m[2].startsWith('[')?m[2].slice(1,-1).split(',').map(s=>s.trim()).filter(Boolean):m[2];}
  const withDraft=core.compile([...data.records,{path:d.path,frontmatter:fm,body:''}],data.layout);
  assert.deepEqual(withDraft.issues.filter(s=>!s.startsWith('Layout preview only')),[]);
  assert.equal(withDraft.byId.get(d.id).home,homeNode.id);assert.equal(fm.backbone_path,homeNode.fm.backbone_path);
  const existing=live.nodes.find(n=>n.layer==='learning');
  assert(core.newNoteDraft(live,homeNode.id,existing.path.split('/').pop().replace(/\.md$/,'').toUpperCase(),'2026-11-09').error);
  assert(core.newNoteDraft(live,homeNode.id,'   ','2026-11-09').error);assert(core.newNoteDraft(live,existing.id,'x','2026-11-09').error);
}
console.log(JSON.stringify({passed:true,attachedNotes:true,newNoteDraft:true,liveBackbone:live.nodes.filter(n=>n.layer==='backbone').length,liveLearning:live.nodes.filter(n=>n.layer==='learning').length,layerFallback:true,baselineNodes:756,baselineEdges:843,coordinateParity:true,syntheticLearningNodes:2,sharedSourceNodes:1,incidentalLinksExcluded:true,viewIsolation:true,notesOnlyView:true,backboneCoordinatesUnchanged:true}));
if(process.argv[4])fs.writeFileSync(process.argv[4],JSON.stringify({...data,records:[...data.records,...fixture]}));
