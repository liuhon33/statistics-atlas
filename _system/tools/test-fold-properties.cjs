// A14: isolated lifecycle/interaction regression; does not write vault files.
const assert=require('node:assert/strict'),Module=require('node:module'),path=require('node:path');
const file=path.resolve(__dirname,'../plugin-src/plugin.js');
const original=Module.prototype.require;
Module.prototype.require=function(id){return id==='obsidian'?{Plugin:class{},ItemView:class{},MarkdownRenderChild:class{},FuzzySuggestModal:class{},Modal:class{}}:original.apply(this,arguments);};
const Plugin=require(file);Module.prototype.require=original;
let calls=0;
function leaf(path,mode='source',connected=true){
  const classes=new Set();
  const metadata={containerEl:{isConnected:connected,classList:{contains:k=>classes.has(k)}},
    setCollapse(value,animate){assert.equal(value,true);assert.equal(animate,false);calls++;classes.add('is-collapsed');}};
  const view={file:{path},metadataEditor:metadata,getMode:()=>mode};
  return {view,classes,mode:value=>{mode=value;}};
}
const learning=leaf('Learning/a.md'),backbone=leaf('Backbone/b.md'),aux=leaf('_system/c.md','preview');
const late=leaf('new.md','source',false),leaves=[learning,backbone,aux,late];
const plugin=new Plugin();plugin.app={workspace:{getLeavesOfType:()=>leaves}};
plugin.propertyFoldDefaults=new WeakMap();plugin.propertyFoldTimers=[];
plugin.applyPropertyFoldDefaults();assert.equal(calls,3); // every layer, including background panes
learning.classes.delete('is-collapsed');plugin.applyPropertyFoldDefaults();
assert.equal(calls,3);assert(!learning.classes.has('is-collapsed')); // user's expansion survives layout events
late.view.metadataEditor.containerEl.isConnected=true;plugin.applyPropertyFoldDefaults();assert.equal(calls,4);
learning.view.file.path='Learning/new.md';plugin.applyPropertyFoldDefaults();assert.equal(calls,5);
learning.mode('preview');plugin.applyPropertyFoldDefaults();assert.equal(calls,6);
// Unsupported native method: use the actual pane's fold control, never the active-pane command.
delete aux.view.metadataEditor.setCollapse;aux.view.file.path='_system/new.md';aux.classes.clear();
aux.view.metadataEditor.containerEl.querySelector=()=>({click:()=>aux.classes.add('is-collapsed')});
plugin.applyPropertyFoldDefaults();assert(aux.classes.has('is-collapsed'));
plugin.queuePropertyFoldDefaults();assert.equal(plugin.propertyFoldTimers.length,3);plugin.onunload();
console.log('PASS: all layers, both modes, manual expansion, delayed mount, navigation, fallback and unload.');
