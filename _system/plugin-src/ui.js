/* Shared canvas interface, used unchanged by the Obsidian view and browser QA. */
const AtlasUI = (() => {
  const el=(tag,cls,text)=>{const n=document.createElement(tag);if(cls)n.className=cls;if(text!=null)n.textContent=text;return n;};
  // Smooth drawing (Claude, 2026-11-11, Phase 1). IDLE_MS: quiet time after the last camera move before the map
  // redraws sharp and re-places labels. FADE_MS: label and highlight fades. WHEEL_TAU: wheel-zoom smoothing time
  // constant. MAX_LABELS: label budget per frame. CELL: overlap-grid cell (px). PAD: off-screen margin (px).
  // MOTION_PAD: margin of the motion bitmap, as a share of the stage on each side; MOTION_ZOOM: zoom range around
  // that bitmap's own zoom within which moving frames copy it instead of drawing the web.
  const IDLE_MS=120,FADE_MS=160,WHEEL_TAU=60,MAX_LABELS=160,CELL=80,PAD=40,MOTION_PAD=.4,MOTION_ZOOM=[.5,1.8];
  // Semantic zoom (Claude, 2026-11-11, Phase 2). A label group starts to show once its dots are LABEL_GAP px apart on
  // screen (median distance to the nearest dot of the same group), and fades in over a further LABEL_RAMP zoom factor.
  // Levels 1-2 always show. FOCUS_RELAX lowers the thresholds inside a focused branch. LABEL_STYLE: [px, weight, wrap px].
  // QUIET: zoom range over which level-5 dots and links rise from quiet (whole web) to full strength.
  const LABEL_GAP={L3:30,L4:30,L5:30,learning:40,source:50,record:80},LABEL_RAMP=1.35,FOCUS_RELAX=.6,QUIET=[.15,.5];
  const LABEL_STYLE={L1:[15,650,170],L2:[13,600,165],L3:[12,500,155],L4:[11.5,400,150],L5:[11,400,145],learning:[11,400,150],source:[11,400,150],record:[11,400,150]};
  // Label priority: learning notes come before level-5 topics, which share the outer ring with them.
  const LABEL_GROUPS=['L1','L2','L3','L4','learning','L5','source','record'];
  const groupOf=n=>n.layer==='backbone'?(n.level>=2&&n.level<=5?'L'+n.level:n.level===1?'L1':'L5'):n.layer==='learning'?'learning':n.source?'source':'record';
  // Spotlight (Claude, 2026-11-11, Phase 3). SPOT_DIM: strength of the rest of the web under a spotlight (raised from
  // 0.1 at the user's request: the surroundings were too dim). SPOT_LABEL: strength of the ordinary labels that stay
  // around the lit path. SPOT_MS: fade time. PULSES x PULSE_MS: how long the spotlit dot pulses before it holds still.
  const SPOT_DIM=.35,SPOT_LABEL=.5,SPOT_MS=260,PULSES=3,PULSE_MS=800;
  // Dive (Claude, 2026-11-11, Phase 4). FOG[i]: strength of a branch left i steps up the dive's path (1 = the branch
  // itself, then sibling branches, then branches left earlier). FOG_OUT: everything outside the dive's subject.
  const FOG=[1,.4,.2,.1],FOG_OUT=.06;
  // Hover peek (Claude, 2026-11-11, extra idea 1): how long the pointer rests on a dot before its preview is asked for
  // (Obsidian's page preview then adds its own short delay).
  const PEEK_MS=180;
  // Coverage glow (Claude, 2026-11-11, extra idea 3): strength of topics with none of the user's notes under them.
  const COVER_FADE=.28;
  const LINK_META={contains:{name:'Hierarchy',arrow:'›',says:(a,b)=>`${a} contains ${b}.`},attachment:{name:'Primary home',arrow:'›',says:(a,b)=>`${a} is the primary home of ${b}.`},prerequisite:{name:'Prerequisite',arrow:'→',says:(a,b)=>`${a} is a prerequisite for ${b}.`},application:{name:'Application',arrow:'→',says:(a,b)=>`${a} is applied in ${b}.`},connection:{name:'Related',arrow:'—',says:(a,b)=>`${a} and ${b} are related.`},source:{name:'Source',arrow:'→',says:(a,b)=>`${a} cites ${b}.`}};
  const toRgba=(c,a)=>{let h=String(c).trim();if(/^#[0-9a-f]{3}$/i.test(h))h='#'+[...h.slice(1)].map(x=>x+x).join('');const m=/^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(h);return m?`rgba(${parseInt(m[1],16)},${parseInt(m[2],16)},${parseInt(m[3],16)},${a})`:c;};
  const dashOf=type=>type==='contains'||type==='attachment'?null:type==='connection'?[2,4]:[6,4];
  const ease=u=>u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2;
  // Smooth zoom-and-pan path (van Wijk & Nuij 2003; the same formula as d3-interpolate's interpolateZoom). A view is
  // [cx,cy,w]: the world point at the screen centre and the world width shown. A long jump zooms out, travels, zooms in.
  function zoomPath([ux0,uy0,w0],[ux1,uy1,w1]){
    const rho=Math.SQRT2,dx=ux1-ux0,dy=uy1-uy0,d2=dx*dx+dy*dy;
    if(d2<1e-12){const S=Math.log(w1/w0)/rho;return {S:Math.abs(S),at:t=>[ux0+t*dx,uy0+t*dy,w0*Math.exp(rho*t*S)]};}
    const d1=Math.sqrt(d2),b0=(w1*w1-w0*w0+4*d2)/(4*w0*d1),b1=(w1*w1-w0*w0-4*d2)/(4*w1*d1),r0=Math.log(Math.sqrt(b0*b0+1)-b0),r1=Math.log(Math.sqrt(b1*b1+1)-b1),S=(r1-r0)/rho;
    return {S,at:t=>{const s=t*S,c0=Math.cosh(r0),u=w0/(2*d1)*(c0*Math.tanh(rho*s+r0)-Math.sinh(r0));return [ux0+u*dx,uy0+u*dy,w0*c0/Math.cosh(rho*s+r0)];}};
  }
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
      const tools=el('div','sa-tools');this.coverageToggle=this.iconButton('sprout','✿','Coverage: glow where your notes are, fade topics with none yet',()=>{this.setCoverage(!this.coverage);this.options.onStateChange?.();});this.followToggle=this.iconButton('locate','◎','Follow: spotlight each atlas note you open',()=>{this.setFollow(!this.follow);this.options.onFollow?.(this.follow);this.options.onStateChange?.();});this.panelToggle=this.iconButton('panel-right','▥','Show or hide the side panel',()=>{this.setPanel(!this.panelOpen);this.options.onStateChange?.();});
      tools.append(this.iconButton('home','⌂','Whole web',()=>{this.focus=null;this.selected=null;this.spot=null;this.dive=null;this.selectedLink=null;this.depth=5;this.depthSelect.value=5;this.update();this.fit();}),this.iconButton('maximize','⤢','Fit visible',()=>this.fit()),this.iconButton('zoom-out','−','Zoom out',()=>this.zoom(.75,this.width/2,this.height/2)),this.iconButton('zoom-in','+','Zoom in',()=>this.zoom(1.33,this.width/2,this.height/2)),this.coverageToggle,this.followToggle,this.panelToggle);
      bar.append(tools);host.append(bar);
      const main=el('div','sa-main');this.stage=el('div','sa-stage');this.canvas=el('canvas');this.canvas.setAttribute('role','img');const desc=el('span','sa-sr','Statistics network. Search and the topic browser provide keyboard navigation.');desc.id='sa-desc-'+Math.random().toString(36).slice(2);this.stage.append(desc);this.canvas.setAttribute('aria-labelledby',desc.id);this.stage.append(this.canvas);this.tooltip=el('div','sa-tooltip');this.stage.append(this.tooltip);this.crumbs=el('div','sa-crumbs');this.crumbs.hidden=true;this.crumbs.setAttribute('aria-label','Spotlight path');this.stage.append(this.crumbs);
      const overlay=el('div','sa-overlay'),legend=el('div','sa-legend');for(const [id,label] of [['probability','Probability & foundations'],['statistics','Inference & modeling'],['computing','Computing & learning']]){const item=el('span','');const dot=el('i','sa-dot');dot.style.background=model.colors[id];item.append(dot,document.createTextNode(label));legend.append(item);}
      legend.append(el('span','sa-shapes','● backbone · ○ learning · ■ auxiliary'));this.coverageKey=el('span','sa-coverage-key','✿ glow: your notes under a topic · faded: none yet');this.coverageKey.hidden=true;legend.append(this.coverageKey);this.status=el('div','sa-status');this.status.setAttribute('aria-live','polite');overlay.append(legend,this.status);this.stage.append(overlay);main.append(this.stage);
      this.panel=el('aside','sa-panel');this.panel.setAttribute('aria-label','Selected topic details');this.panelBody=el('div','sa-panel-body');this.panel.append(this.panelBody);
      this.outline=el('details','sa-outline');this.outline.append(el('summary','','Browse all topics'));this.tree=el('div','sa-tree');this.outline.append(this.tree);this.panel.append(this.outline);
      this.outline.addEventListener('toggle',()=>{if(this.outline.open&&!this.tree.childElementCount)this.buildTree();});
      this.issues=el('details','sa-issues');this.issueSummary=el('summary','','Map checks');this.issues.append(this.issueSummary);this.issueBody=el('div');this.issues.append(this.issueBody);this.panel.append(this.issues);
      main.append(this.panel);host.append(main);
      this.ctx=this.canvas.getContext('2d');this.attachCanvas();
      this.resizeObserver=new ResizeObserver(()=>this.resize());this.resizeObserver.observe(this.stage);
      // Theme observer (Claude, 2026-11-11): Obsidian touches body class and style often; cached colours, label sizes,
      // label bitmaps and the scene are reset only when a colour or the font really changed. motionDpr: pixel-ratio cap while moving.
      this.motionDpr=1.5;this.themeObserver=new MutationObserver(()=>{const old=this._theme;this._theme=null;const t=this.theme();if(old&&['fg','bg','muted','font'].every(k=>old[k]===t[k])){this._theme=old;return;}this._labels=null;this._sprites=null;this.draw();});this.themeObserver.observe(document.body,{attributes:true,attributeFilter:['class','style']});
      this.update();this.resize();
    }
    button(label,fn,aria){const b=el('button','sa-button',label);b.type='button';if(aria)b.setAttribute('aria-label',aria);b.addEventListener('click',fn);return b;}
    // Icon from Obsidian's set when the host passes setIcon; plain text glyph otherwise (browser QA).
    iconButton(icon,glyph,label,fn){const b=this.button('',fn,label);b.classList.add('sa-icon');b.title=label;if(this.options.setIcon)this.options.setIcon(b,icon);if(!b.firstChild)b.textContent=glyph;return b;}
    setPanel(open){this.panelOpen=!!open;this.host.classList.toggle('sa-panel-closed',!this.panelOpen);this.panelToggle.setAttribute('aria-pressed',String(this.panelOpen));}
    updateModel(model){this.model=model;const ol=this.selectedLink;this.selectedLink=ol&&model.edges.find(e=>e.type===ol.type&&e.source===ol.source&&e.target===ol.target)||null;const os=this.spot;this.spot=!os?null:os.kind==='link'?(this.selectedLink?this.linkSpot(this.selectedLink):null):(model.byId.has(os.id)?this.buildSpot(model.byId.get(os.id),os):null);if(this.dive)this.dive=model.byId.has(this.dive.id)?this.buildDive(this.dive.id,this.dive.visited):null;if(this.selected&&!model.byId.has(this.selected))this.selected=null;if(this.focus&&!model.byId.has(this.focus))this.focus=null;this.tree.replaceChildren();if(this.outline.open)this.buildTree();this.update();this.searchResults();}
    update(){
      const selectedNode=this.model.byId.get(this.selected);
      if(selectedNode&&((this.mode==='backbone'&&selectedNode.layer!=='backbone')||(this.mode==='learning'&&selectedNode.layer==='auxiliary')))this.selected=selectedNode.home||null;
      // Notes only (Claude, 2026-11-08, AGENTS A12): a selected topic or record is not on this view, so it is cleared.
      const notesOnly=this.mode==='notes';if(selectedNode&&notesOnly&&selectedNode.layer!=='learning')this.selected=null;
      // Same view, depth, focus and model: keep the same visible set, so caches keyed on it survive a selection (Claude, 2026-11-11).
      const vkey=this.mode+'|'+this.depth+'|'+this.focus;if(!this.visible||this.visibleKey!==vkey||this.visibleModel!==this.model){this.visible=this.core.visible(this.model,this.mode,this.depth,this.focus);this.visibleKey=vkey;this.visibleModel=this.model;}
      for(const [id,b] of Object.entries(this.modes))b.setAttribute('aria-pressed',String(id===this.mode));
      this.depthSelect.disabled=notesOnly;this.depthSelect.title=notesOnly?'Levels apply to backbone topics, which this view hides':'Visible levels';
      this.search.placeholder=notesOnly?'Find one of my notes…':'Find a topic, alias or note…';
      const counts={backbone:0,learning:0,auxiliary:0};this.model.nodes.forEach(n=>counts[n.layer]++);
      this.status.textContent=`${counts.backbone} topics · ${counts.learning} notes · showing ${this.visible.nodes.length} nodes, ${this.visible.edges.length} links`+(this.focus?' · focused branch':'')+((this.mode==='learning'||notesOnly)&&!counts.learning?' · no learning notes yet':'')+(notesOnly&&this.focus&&counts.learning&&!this.visible.nodes.length?' · no notes in this branch':'');
      const issues=this.model.issues.length;this.issueBody.replaceChildren();for(const issue of this.model.issues)this.issueBody.append(el('p','',issue));this.issues.hidden=!issues;this.issueSummary.textContent=`Map checks (${issues})`;
      this.panelToggle.classList.toggle('sa-flag',!!issues);this.panelToggle.title=issues?`Show or hide the side panel · ${issues} map check${issues>1?'s':''}`:'Show or hide the side panel';
      this.renderPanel();this.renderCrumbs();this.draw();
    }
    select(id,focus=false){
      if((this.spot||this.dive)&&!focus)return this.spotlight(id,'auto'); // inside a spotlight or a dive, a pick moves the light (Phases 3-4)
      if(focus)this.dive=null;
      const n=this.model.byId.get(id);if(!n)return;this.selected=id;this.hover=null;this.autoFit=false;this.spot=null;this.selectedLink=null;
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
      this.panelBody.replaceChildren();if(this.selectedLink)return this.renderLinkPanel();const n=this.model.byId.get(this.selected);
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
        this.panelBody.append(el('div','sa-eyebrow','THREE SUBJECTS · FIVE LEVELS'),el('h3','','Explore the backbone'),el('p','sa-muted','Select a dot to inspect its path and connections. Search opens a focused branch. Double-click a dot to open its note. With the map clicked, the arrow keys move between topics, Space dives into a branch and Enter opens the note.'));
        const roots=this.model.nodes.filter(n=>n.layer==='backbone'&&n.level===1);roots.forEach(n=>this.panelBody.append(this.button(n.label,()=>this.select(n.id,true))));
        this.panelBody.append(el('p','sa-muted','Hierarchy is solid. Prerequisites and applications are dashed lines with chevrons pointing toward the dependent topic. Conceptual connections are dotted.'));
        if(this.mode==='everything'){const d=el('details');d.append(el('summary','','Auxiliary records'));this.model.nodes.filter(v=>v.layer==='auxiliary').forEach(v=>d.append(this.button(v.label,()=>this.select(v.id))));this.panelBody.append(d);}return;
      }
      const tag=n.layer==='backbone'?`LEVEL ${n.level} · ${n.stage}`:n.layer==='learning'?`MY LEARNING · ${n.noteTypes.join(' · ')}`:'AUXILIARY';
      this.panelBody.append(el('div','sa-eyebrow',tag),el('h3','',n.label));
      const path=el('div','sa-path');this.model.lineage(n.id).forEach((p,i)=>{if(i)path.append(document.createTextNode(' › '));path.append(this.button(p.label,()=>this.select(p.id)));});this.panelBody.append(path);
      if(this.coverage&&n.layer==='backbone')this.panelBody.append(el('p','sa-muted',`Coverage: ${this.notesUnder(n.id)} in this branch.`));
      this.panelBody.append(this.button('Open note',()=>this.options.openNote?.(n.path)));
      if(n.layer==='backbone')this.panelBody.append(this.button('Focus this branch',()=>this.select(n.id,true)));
      if(n.layer!=='auxiliary')this.panelBody.append(this.button('Dive in (Space)',()=>this.diveInto(n.id)));
      if(this.dive)this.panelBody.append(this.button('Up one level (Backspace)',()=>this.climb()),this.button('Leave the dive (Esc)',()=>this.exitDive()));
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
    // Smooth drawing (Claude, 2026-11-11, Phase 1). Measured in the live vault before this change (1637x749 px pane,
    // pixel ratio 2.25): a whole-web frame took 12-27 ms and a frame just past 0.36x zoom 18-38 ms, most of it links,
    // dashed ones worst, each re-styled one by one. Batching all links into one path was tried and measured slower in
    // Chromium (contains links 5.6 vs 2.0 ms), so each link stays its own short path; styles are set once per group and
    // dashed links are cut to the screen. Labels are cached bitmaps placed with a grid overlap test, the camera glides,
    // wheel zoom is smoothed, and while the camera moves each frame skips label placement and the scene cache, at a
    // capped pixel ratio; IDLE_MS after it stops the map redraws sharp. Labels and the highlight fade instead of popping.
    // Real on-screen frames (144 Hz screen, animated pan, learning view) showed the limit is GPU fill, not JavaScript
    // (under 2 ms): old code 18.9 ms per frame at the whole web and 23 ms at 0.4x; drawing at 1.5x pixel ratio while
    // moving gave 11 and 14 ms. So moving frames now copy a motion bitmap (see buildMotionCache) when they can.
    // Keeps the map centre fixed when the stage changes size (side panel toggled, pane resized). (Claude, review item 15)
    // Until the user moves the camera or picks a dot, an automatic fit is redone on every resize: a new atlas tab can
    // report a tiny stage first, and fitting that left the web as a speck (seen at 0.016x; Claude, 2026-11-11).
    resize(){const prev=this._stageSize;if(!this.syncSize(false))return;this._stageSize={w:this.width,h:this.height};if(this.pendingFrame&&this.spot){const f=this.pendingFrame;this.pendingFrame=null;this.fitted=true;this.frameSpot(f,false);return;}if(this.pendingVisible){this.ensureVisible();if(!this.pendingVisible)return this.draw();}if(!this.fitted||this.autoFit){this.fit(false);this.fitted=true;this.autoFit=true;}else{if(prev){this.camera={...this.camera,x:this.camera.x+(this.width-prev.w)/2,y:this.camera.y+(this.height-prev.h)/2};}this.draw();}}
    // Size and pixel ratio are re-checked on every paint; the backing store is only reallocated when it changes.
    // While the camera moves the pixel ratio is capped at motionDpr (Claude, 2026-11-11).
    syncSize(moving){const w=this.stage.clientWidth,h=this.stage.clientHeight;if(!w||!h)return false;const full=window.devicePixelRatio||1,dpr=moving?Math.min(full,this.motionDpr||full):full,W=Math.round(w*dpr),H=Math.round(h*dpr);this.width=w;this.height=h;this.dpr=dpr;this.fullDpr=full;if(this.canvas.width!==W)this.canvas.width=W;if(this.canvas.height!==H)this.canvas.height=H;return true;}
    fitCamera(){if(!this.width)return null;let minX=Infinity,maxX=-Infinity,minY=Infinity,maxY=-Infinity;for(const n of this.visible.nodes){const p=this.model.positions[n.id];if(!p)continue;if(p.x<minX)minX=p.x;if(p.x>maxX)maxX=p.x;if(p.y<minY)minY=p.y;if(p.y>maxY)maxY=p.y;}if(minX===Infinity)return null;const pad=70,k=Math.min((this.width-pad*2)/Math.max(250,maxX-minX),(this.height-pad*2)/Math.max(250,maxY-minY));return {k,x:this.width/2-(minX+maxX)/2*k,y:this.height/2-(minY+maxY)/2*k};}
    // Refits when no visible dot lies inside the stage (Claude, 2026-11-11), e.g. a restored camera that does not match
    // the restored focus. Waits for the first measured stage size.
    ensureVisible(){if(!this.width){this.pendingVisible=true;return;}this.pendingVisible=false;const P=this.model.positions,{x:cx,y:cy,k}=this.camera;for(const n of this.visible.nodes){const p=P[n.id];if(!p)continue;const x=p.x*k+cx,y=p.y*k+cy;if(x>=0&&x<=this.width&&y>=0&&y<=this.height)return;}this.fit(false);this.autoFit=true;}
    fit(animate=true){const c=this.fitCamera();if(c)this.moveCamera(c,animate);}
    center(id,animate=true){const p=this.model.positions[id];if(!p||!this.width)return;const k=this.camera.k;this.moveCamera({k,x:this.width/2-p.x*k,y:this.height/2-p.y*k},animate);}
    // Zoom buttons: repeated presses add up from the glide's destination, not from wherever the glide has reached.
    zoom(factor,x,y,animate=true){const c=this.glide?.to||this.camera,k=Math.max(.04,Math.min(7,c.k*factor));this.moveCamera({k,x:x-(x-c.x)*k/c.k,y:y-(y-c.y)*k/c.k},animate,220);}
    zoomAt(factor,x,y){const old=this.camera.k,k=Math.max(.04,Math.min(7,old*factor));this.camera={k,x:x-(x-this.camera.x)*k/old,y:y-(y-this.camera.y)*k/old};}
    // Camera glide (Claude, 2026-11-11): Fit, Home, search, selection and the zoom buttons travel along zoomPath
    // instead of jumping. A drag or wheel cancels a glide where it is. animate=false jumps (first fit, restored state).
    moveCamera(to,animate=true,duration){
      this.wheel=null;
      if(!animate||!this.width){this.glide=null;this.camera={...to};this.draw();return;}
      const w=this.width,h=this.height,view=c=>[(w/2-c.x)/c.k,(h/2-c.y)/c.k,w/c.k],path=zoomPath(view(this.camera),view(to));
      if(!(path.S>1e-4)){this.glide=null;this.camera={...to};this.draw();return;}
      this.glide={path,to:{...to},t0:performance.now(),dur:duration??Math.max(260,Math.min(850,path.S*420))};this.markMotion();this.draw();
    }
    markMotion(){this.autoFit=false;this.cancelMotionCache();this.lastMotion=performance.now();clearTimeout(this.idleTimer);this.idleTimer=setTimeout(()=>this.draw(),IDLE_MS+20);}
    // Advances a glide or the smoothed wheel zoom by one frame. True while either is still running.
    stepCamera(now,dt){
      let busy=false,moved=false;
      if(this.glide){const g=this.glide,u=Math.max(0,Math.min(1,(now-g.t0)/g.dur));moved=true;if(u>=1){this.camera={...g.to};this.glide=null;}else{const [ux,uy,vw]=g.path.at(ease(u)),k=this.width/vw;this.camera={k,x:this.width/2-ux*k,y:this.height/2-uy*k};busy=true;}}
      if(this.wheel){const w=this.wheel,gap=Math.log(w.k/this.camera.k);moved=true;if(Math.abs(gap)<.002){this.zoomAt(w.k/this.camera.k,w.x,w.y);this.wheel=null;}else{this.zoomAt(Math.exp(gap*(1-Math.exp(-dt/WHEEL_TAU))),w.x,w.y);busy=true;}}
      if(moved)this.markMotion();return busy;
    }
    screen(id){const p=this.model.positions[id];return p?{x:p.x*this.camera.k+this.camera.x,y:p.y*this.camera.k+this.camera.y}:null;}
    radius(n){return n.layer==='auxiliary'?3.3:n.layer==='learning'?4.2:n.level===1?12:Math.max(n.level===5?1.9:3,[0,15,9,6,4,2.7][n.level]*Math.min(1,this.camera.k*2));}
    // Direction chevrons spaced along a directed (prerequisite/application) edge, pointing from source to
    // target, so the direction reads along the whole line instead of only at the crowded target end. (Claude, 2026-11-08)
    // Appends to the current path; the caller begins and fills it (Claude, 2026-11-11).
    chevrons(ctx,ax,ay,bx,by,ra,rb,size){
      const dx=bx-ax,dy=by-ay,len=Math.hypot(dx,dy),start=ra+size+4,end=len-rb-size-4;if(end<=start)return;
      const ux=dx/len,uy=dy/len,span=end-start,spacing=Math.max(34,size*8),count=Math.max(1,Math.floor(span/spacing)),step=span/count;
      for(let i=0;i<count;i++){
        const t=start+step*(i+.5),x=ax+ux*t,y=ay+uy*t;
        if(x<-10||y<-10||x>this.width+10||y>this.height+10)continue;
        ctx.moveTo(x+ux*size,y+uy*size);ctx.lineTo(x-ux*size-uy*size*.75,y-uy*size+ux*size*.75);ctx.lineTo(x-ux*size*.35,y-uy*size*.35);ctx.lineTo(x-ux*size+uy*size*.75,y-uy*size-ux*size*.75);ctx.closePath();
      }
    }
    // Visible part of a link as [t0,t1] along it (Liang-Barsky against the screen plus PAD), or null when off-screen.
    clipSeg(ax,ay,bx,by){
      const dx=bx-ax,dy=by-ay,m=PAD;let t0=0,t1=1;
      const clip=(p,q)=>{if(p===0)return q>=0;const r=q/p;if(p<0){if(r>t1)return false;if(r>t0)t0=r;}else{if(r<t0)return false;if(r<t1)t1=r;}return true;};
      return clip(-dx,ax+m)&&clip(dx,this.width+m-ax)&&clip(-dy,ay+m)&&clip(dy,this.height+m-ay)?[t0,t1]:null;
    }
    // One link as its own short path (Claude, 2026-11-11). A dashed link is cut to its visible part and the dash offset
    // keeps the pattern counted from the link's start, so dashes stay put while the map pans. The caller sets the dash.
    strokeLink(ctx,ax,ay,bx,by,dash){
      if(dash){const t=this.clipSeg(ax,ay,bx,by);if(!t)return;const dx=bx-ax,dy=by-ay;ctx.lineDashOffset=t[0]*Math.hypot(dx,dy)%(dash[0]+dash[1]);ctx.beginPath();ctx.moveTo(ax+dx*t[0],ay+dy*t[0]);ctx.lineTo(ax+dx*t[1],ay+dy*t[1]);ctx.stroke();}
      else{ctx.beginPath();ctx.moveTo(ax,ay);ctx.lineTo(bx,by);ctx.stroke();}
    }
    // Review item 14 (Claude, 2026-11-08): theme colours and wrapped label sizes are cached between frames
    // (reset when Obsidian's theme changes) instead of re-reading styles and re-measuring every label per frame.
    // The fallback colours are never cached (Claude, 2026-11-11): after a plugin reload the view can paint before
    // Obsidian applies styles.css, and a cached fallback kept dark label boxes on the light theme until the next body change.
    theme(){if(!this._theme){const s=getComputedStyle(this.host),fg=s.getPropertyValue('--sa-fg').trim(),t={fg:fg||'#dedede',bg:s.getPropertyValue('--sa-bg').trim()||'#202126',muted:s.getPropertyValue('--sa-muted').trim()||'#9497a3',font:s.fontFamily};if(!fg)return t;this._theme=t;}return this._theme;}
    labelBox(text,font,lh=15,wrap=155){const cache=this._labels||(this._labels=new Map()),key=font+'\0'+lh+'\0'+wrap+'\0'+text;let m=cache.get(key);
      if(!m){const ctx=this._measure||(this._measure=document.createElement('canvas').getContext('2d'));ctx.font=font;const lines=[];for(const fragment of text.split('\n')){let line='';for(const word of fragment.split(' ')){if(ctx.measureText(line+' '+word).width>wrap&&line){lines.push(line);line=word;}else line+=(line?' ':'')+word;}if(line)lines.push(line);}
        m={lines,w:Math.max(...lines.map(l=>ctx.measureText(l).width)),h:lines.length*lh};cache.set(key,m);}return m;}
    // A label (background box and text) drawn once into a small bitmap at the screen's full pixel ratio, then copied
    // each frame instead of filling a box and text per line. (Claude, 2026-11-11)
    sprite(text,font,lh=15,wrap=155){
      const th=this.theme();if(this._spritesFor!==th){this._sprites=new Map();this._spritesFor=th;}
      const d=this.fullDpr||window.devicePixelRatio||1,cache=this._sprites,key=d+'\0'+font+'\0'+lh+'\0'+wrap+'\0'+text;let s=cache.get(key);if(s)return s;
      if(cache.size>1500)cache.clear();
      const {fg,bg}=th,box=this.labelBox(text,font,lh,wrap),w=box.w+6,h=box.h+4,c=document.createElement('canvas');c.width=Math.ceil(w*d);c.height=Math.ceil(h*d);
      const x=c.getContext('2d');x.scale(d,d);x.globalAlpha=.92;x.fillStyle=bg;x.fillRect(0,0,w,h);x.globalAlpha=1;x.fillStyle=fg;x.font=font;x.textBaseline='middle';box.lines.forEach((l,i)=>x.fillText(l,3,2+lh/2+i*lh));
      s={canvas:c,w:c.width/d,h:c.height/d};cache.set(key,s);return s;
    }
    // Zoom at which each label group starts to show: LABEL_GAP over the median distance from each of its dots to the
    // nearest dot of the same group, so thresholds follow the backbone as it grows. Rebuilt per model. (Phase 2)
    labelPlan(){
      if(this._plan?.for===this.model)return this._plan;
      const P=this.model.positions,pts=new Map(),start={L1:0,L2:0};
      for(const n of this.model.nodes){const p=P[n.id];if(!p)continue;const g=groupOf(n);if(!pts.has(g))pts.set(g,[]);pts.get(g).push(p);}
      for(const [g,list] of pts){if(!(g in LABEL_GAP))continue;const d=[];for(let i=0;i<list.length;i++){let best=Infinity;for(let j=0;j<list.length;j++)if(i!==j){const v=Math.hypot(list[i].x-list[j].x,list[i].y-list[j].y);if(v<best)best=v;}if(best<Infinity)d.push(best);}d.sort((a,b)=>a-b);start[g]=d.length?LABEL_GAP[g]/Math.max(1,d[d.length>>1]):0;}
      return this._plan={for:this.model,start};
    }
    // How far a label has faded in at zoom k: 0 below its group's start, 1 from LABEL_RAMP times the start.
    // In Notes only, learning-note labels always qualify (no backbone competes with them).
    zoomAlpha(n,k){
      if(this.mode==='notes'&&n.layer==='learning')return 1;
      const s=(this.labelPlan().start[groupOf(n)]||0)*(this.focus||this.dive?FOCUS_RELAX:1);
      return !s||k>=s*LABEL_RAMP?1:k<=s?0:(k-s)/(s*(LABEL_RAMP-1));
    }
    // Per-visible-set lookups, rebuilt only when the visible set changes. Draw order matches the old sort by
    // (level||6) descending: learning and auxiliary first, then levels 5 to 1. groups: label groups in priority order.
    // linkClass: hierarchy links by the child's level (c2-c5), attachments, provenance (aux) and typed links (Phase 2).
    prepared(){
      if(this.prep?.for===this.visible)return this.prep;
      const levels=[[],[],[],[],[],[]],ids=new Set(),groups=new Map(LABEL_GROUPS.map(g=>[g,[]]));
      for(const n of this.visible.nodes){ids.add(n.id);levels[n.layer==='backbone'&&n.level>=1&&n.level<=5?n.level:0].push(n);groups.get(groupOf(n)).push(n);}
      const linkClass=this.visible.edges.map(e=>e.type==='contains'?'c'+Math.max(2,Math.min(5,this.model.byId.get(e.target)?.level||5)):e.scope==='auxiliary'?'aux':e.type==='attachment'?'att':'typed');
      return this.prep={for:this.visible,ids,draw:[levels[0],levels[5],levels[4],levels[3],levels[2],levels[1]],groups,linkClass,admin:this.visible.nodes.filter(n=>n.layer==='auxiliary'&&!n.source),neighbors:new Map()};
    }
    neighborhood(id){const prep=this.prepared();let nb=prep.neighbors.get(id);if(!nb){const set=new Set([id]),edges=[];for(const e of this.visible.edges)if(e.source===id||e.target===id){set.add(e.source);set.add(e.target);edges.push(e);}nb={set,edges};prep.neighbors.set(id,nb);}return nb;}
    draw(){if(this.frame)return;this.frame=requestAnimationFrame(t=>{this.frame=0;this.paint(t);});}
    // One frame (Claude, 2026-11-11; replaces the review item 14 base/overlay split). At rest the labelless web is kept
    // in an off-screen canvas keyed on camera, size, pixel ratio, visible set and theme, so hover changes and fades only
    // copy it. A highlight draws that web faded to a quarter, then the neighbourhood on top. While the camera moves the
    // web is drawn directly at the capped pixel ratio, and labels keep their places relative to their dots.
    paint(now=performance.now()){
      if(!this.ctx||!this.visible)return;
      const dt=Math.max(0,Math.min(64,now-(this.lastPaint??now))),fdt=Math.min(dt,25);this.lastPaint=now;
      let more=this.stepCamera(now,dt);const moving=more||now-(this.lastMotion||-1e9)<IDLE_MS;
      if(!this.syncSize(moving))return;const theme=this.theme(),active=this.spot?null:(this.hover||this.selected);
      if(active)this.litId=active;
      const goal=active?1:0,lit=this.litT=goal>(this.litT||0)?Math.min(1,(this.litT||0)+fdt/FADE_MS):Math.max(0,(this.litT||0)-fdt/FADE_MS);
      if(lit!==goal)more=true;else if(!active)this.litId=null;
      if(this.spot)this.spotOut=this.spot;
      const sGoal=this.spot?1:0,sT=this.spotT=sGoal>(this.spotT||0)?Math.min(1,(this.spotT||0)+fdt/SPOT_MS):Math.max(0,(this.spotT||0)-fdt/SPOT_MS);
      if(sT!==sGoal)more=true;else if(!this.spot)this.spotOut=null;
      const ctx=this.ctx,dim=(1-.75*lit)*(1-sT)+(this.dive?1:SPOT_DIM)*sT;ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=1;ctx.clearRect(0,0,this.canvas.width,this.canvas.height); // in a dive the fog already sets the strengths
      if(moving){if(!this.blitMotion(ctx,dim,theme))this.paintScene(ctx,dim);}
      else{
        const cam=this.camera,key=[this.canvas.width,this.canvas.height,this.dpr,cam.x,cam.y,cam.k,this.styleKey()].join('|');
        if(!this.scene||this.sceneKey!==key||this.sceneFor!==this.visible||this.sceneTheme!==theme){
          const b=this.scene||(this.scene=document.createElement('canvas'));if(b.width!==this.canvas.width)b.width=this.canvas.width;if(b.height!==this.canvas.height)b.height=this.canvas.height;
          const bctx=b.getContext('2d');bctx.setTransform(1,0,0,1,0,0);bctx.globalAlpha=1;bctx.clearRect(0,0,b.width,b.height);this.paintScene(bctx,1);this.sceneKey=key;this.sceneFor=this.visible;this.sceneTheme=theme;}
        ctx.globalAlpha=dim;ctx.drawImage(this.scene,0,0);ctx.globalAlpha=1;
      }
      if(this.litId&&lit>0)this.paintOverlay(ctx,this.litId,lit);
      if(this.dive)this.paintDive(ctx);
      if(this.spotOut&&sT>0&&this.paintSpot(ctx,this.spotOut,sT,now))more=true;
      if(this.hoverLink&&this.hoverLink!==this.selectedLink)this.paintHoverLink(ctx,this.hoverLink);
      // Labels are re-placed at rest when anything they depend on changed, and during a move only when the zoom has
      // changed by a quarter since the last placement (so zooming out does not pile labels on top of each other).
      const c=this.camera,lkey=[c.x,c.y,c.k,this.width,this.height,active,this.focus,this.spot?.key,this.dive?.key,this.coverage].join('|');
      if(!this.labelFx||this.placedFor!==this.visible||(moving?Math.abs(Math.log(c.k/this.placedK))>.223:this.placedKey!==lkey))this.placeLabels(active,lkey);
      if(this.drawLabels(ctx,fdt))more=true;
      if(!moving&&!more)this.queueMotionCache();
      // Camera settled somewhere new: ask Obsidian to save the view state (Claude, 2026-11-11). Camera moves never did,
      // so a saved focus could be restored with a camera from another moment, pointing at empty space.
      if(!moving){const ck=c.x+'|'+c.y+'|'+c.k;if(this.savedCam!==ck){if(this.savedCam!==undefined)this.options.onStateChange?.();this.savedCam=ck;}}
      if(!moving){this.canvas.dataset.mode=this.mode;this.canvas.dataset.visibleNodes=this.visible.nodes.length;this.canvas.dataset.visibleEdges=this.visible.edges.length;this.canvas.dataset.camera=JSON.stringify(this.camera);}
      if(more)this.draw();
    }
    // Motion bitmap (Claude, 2026-11-11). At idle after the map settles, the labelless web is drawn once into a bitmap
    // that reaches MOTION_PAD of the stage beyond each edge, at the capped pixel ratio. While the camera moves, frames
    // copy it shifted and scaled to the current camera, about a millisecond of GPU work instead of redrawing ~1,800
    // links and dots. Panning past its margin or zooming outside MOTION_ZOOM falls back to drawing the web directly.
    // A bitmap left from an earlier position stays usable: the copy is placed by camera, not by when it was drawn.
    queueMotionCache(){if(this.mcHandle!=null)return;const run=()=>{this.mcHandle=null;if(performance.now()-(this.lastMotion||-1e9)>=IDLE_MS)this.buildMotionCache();};this.mcHandle=window.requestIdleCallback?window.requestIdleCallback(run,{timeout:600}):setTimeout(run,200);}
    cancelMotionCache(){if(this.mcHandle==null)return;(window.cancelIdleCallback||clearTimeout)(this.mcHandle);this.mcHandle=null;}
    buildMotionCache(){
      if(!this.visible||!this.width||!this.ctx)return;const theme=this.theme(),c=this.camera,old=this.motionCache,d=Math.min(this.fullDpr||1,this.motionDpr||Infinity);
      if(old&&old.for===this.visible&&old.theme===theme&&old.fog===this.styleKey()&&old.k===c.k&&old.x===c.x&&old.y===c.y&&old.sw===this.width&&old.sh===this.height&&old.d===d)return;
      const ox=Math.round(this.width*MOTION_PAD),oy=Math.round(this.height*MOTION_PAD),w=this.width+2*ox,h=this.height+2*oy,canvas=old?.canvas||document.createElement('canvas'),W=Math.round(w*d),H=Math.round(h*d);
      if(canvas.width!==W)canvas.width=W;if(canvas.height!==H)canvas.height=H;
      const saved={width:this.width,height:this.height,camera:this.camera,dpr:this.dpr},x=canvas.getContext('2d');
      try{this.width=w;this.height=h;this.camera={k:c.k,x:c.x+ox,y:c.y+oy};this.dpr=d;x.setTransform(1,0,0,1,0,0);x.globalAlpha=1;x.clearRect(0,0,W,H);this.paintScene(x,1);}
      finally{Object.assign(this,saved);}
      this.motionCache={canvas,for:this.visible,theme,fog:this.styleKey(),k:c.k,x:c.x,y:c.y,ox,oy,w,h,d,sw:this.width,sh:this.height};
    }
    // Copies the motion bitmap for the current camera at alpha a. False when it is missing, stale, or does not cover the view.
    blitMotion(ctx,a,theme){
      const mc=this.motionCache;if(!mc||mc.for!==this.visible||mc.theme!==theme||mc.fog!==this.styleKey())return false;
      const c=this.camera,s=c.k/mc.k;if(s<MOTION_ZOOM[0]||s>MOTION_ZOOM[1])return false;
      const x0=c.x-(mc.x+mc.ox)*s,y0=c.y-(mc.y+mc.oy)*s,w=mc.w*s,h=mc.h*s;
      if(x0>0.5||y0>0.5||x0+w<this.width-.5||y0+h<this.height-.5)return false;
      ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.globalAlpha=a;ctx.imageSmoothingEnabled=true;ctx.drawImage(mc.canvas,x0,y0,w,h);ctx.globalAlpha=1;return true;
    }
    // The web without labels. Links and dots are grouped by style so colour, alpha and dash are set once per group,
    // but each is still drawn as its own path (see the note above resize). mul scales every alpha (the faded web
    // under a highlight).
    paintScene(ctx,mul){
      const {fg,muted,font}=this.theme(),W=this.width,H=this.height,{x:cx,y:cy,k}=this.camera,P=this.model.positions,prep=this.prepared(),m=PAD;
      // Per-dot strength: dive fog (Phase 4) times coverage (extra idea 3); links take their fainter end.
      const fog=this.dive?.fog,cov=this.coverage?this.coverageMap():null,fo=id=>(fog?(fog.get(id)??FOG_OUT):1)*(cov?(cov.factor.get(id)??COVER_FADE):1);
      ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.setLineDash([]);ctx.textBaseline='middle';
      if(prep.admin.length){let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;for(const n of prep.admin){const p=P[n.id];if(!p)continue;const sx=p.x*k+cx,sy=p.y*k+cy;if(sx<x0)x0=sx;if(sx>x1)x1=sx;if(sy<y0)y0=sy;if(sy>y1)y1=sy;}
        if(x0!==Infinity){const x=x0-14,y=y0-14,w=x1-x+14,h=y1-y+14;ctx.lineWidth=1.6;ctx.strokeStyle=muted;const am=mul*(fog?FOG_OUT:1)*(cov?COVER_FADE:1);ctx.globalAlpha=.35*am;ctx.setLineDash([3,4]);ctx.strokeRect(x,y,w,h);ctx.setLineDash([]);ctx.globalAlpha=am;ctx.fillStyle=fg;ctx.font=`12px ${font}`;ctx.textAlign='center';ctx.fillText('Vault administration',x+w/2,y-20);ctx.font=`10px ${font}`;ctx.fillStyle=muted;ctx.fillText(prep.admin.length+' records',x+w/2,y-6);ctx.textAlign='left';}}
      // Hierarchy links are stronger nearer the centre (Phase 2), so the level 1-4 skeleton reads at the whole-web
      // zoom; level-5 links and attachments stay quiet there and reach full strength by QUIET[1].
      const q=Math.max(0,Math.min(1,(k-QUIET[0])/(QUIET[1]-QUIET[0]))),quiet=.35+.65*q;
      const LINK={c2:[.42,1.5],c3:[.34,1.15],c4:[.28,.9],c5:[.24*quiet,.75],att:[.25*(.5+.5*q),.8],aux:[.13,.8],typed:[.25,.8]};
      const groups=new Map(),arrows=[],edges=this.visible.edges,cls=prep.linkClass;
      for(let i=0;i<edges.length;i++){
        const e=edges[i],a=P[e.source],b=P[e.target];if(!a||!b)continue;const ax=a.x*k+cx,ay=a.y*k+cy,bx=b.x*k+cx,by=b.y*k+cy;
        if((ax<-m&&bx<-m)||(ax>W+m&&bx>W+m)||(ay<-m&&by<-m)||(ay>H+m&&by>H+m))continue;
        const c=cls[i],f=fog||cov?Math.min(fo(e.source),fo(e.target)):1;if(LINK[c][0]*f*mul<.012)continue; // too faint to see: skipped
        const dash=dashOf(e.type),key=c+(dash?':'+dash[0]:'')+':'+f;
        let g=groups.get(key);if(!g)groups.set(key,g={alpha:LINK[c][0]*f,width:LINK[c][1],dash,pts:[]});g.pts.push(ax,ay,bx,by);
        if(e.type==='prerequisite'||e.type==='application')arrows.push({e,ax,ay,bx,by,f});
      }
      ctx.strokeStyle=muted;
      for(const g of groups.values()){ctx.globalAlpha=g.alpha*mul;ctx.lineWidth=g.width;ctx.setLineDash(g.dash||[]);const p=g.pts;for(let i=0;i<p.length;i+=4)this.strokeLink(ctx,p[i],p[i+1],p[i+2],p[i+3],g.dash);}
      ctx.setLineDash([]);ctx.lineDashOffset=0;ctx.lineWidth=.8;
      if(arrows.length){ctx.fillStyle=muted;for(const {e,ax,ay,bx,by,f} of arrows){ctx.globalAlpha=.55*mul*f;ctx.beginPath();this.chevrons(ctx,ax,ay,bx,by,this.radius(this.model.byId.get(e.source)),this.radius(this.model.byId.get(e.target)),3.5);ctx.fill();}}
      // Coverage glow: a soft halo in the subject colour under each topic with notes, wider for more notes.
      if(cov)for(const n of this.visible.nodes){const c=cov.count.get(n.id);if(!c||n.layer!=='backbone')continue;const p=P[n.id];if(!p)continue;const x=p.x*k+cx,y=p.y*k+cy,r=this.radius(n),R=r+6+5*Math.log2(1+c);if(x<-R||x>W+R||y<-R||y>H+R)continue;const col=this.model.colors[n.core]||muted,g=ctx.createRadialGradient(x,y,r*.5,x,y,R);g.addColorStop(0,toRgba(col,.42));g.addColorStop(1,toRgba(col,0));ctx.globalAlpha=mul*(fog?(fog.get(n.id)??FOG_OUT):1);ctx.fillStyle=g;ctx.beginPath();ctx.arc(x,y,R,0,Math.PI*2);ctx.fill();}
      ctx.lineWidth=1.6;ctx.globalAlpha=mul;
      for(const level of prep.draw){
        const la=mul*(level===prep.draw[1]?.55+.45*q:1); // level-5 dots are quieter at the whole-web zoom (Phase 2)
        const dots=new Map();
        for(const n of level){const p=P[n.id];if(!p)continue;const x=p.x*k+cx,y=p.y*k+cy;if(x<-20||x>W+20||y<-20||y>H+20)continue;const color=this.model.colors[n.core]||muted,kind=n.layer==='learning'?'s':n.layer==='auxiliary'?'r':'f',f=fo(n.id),key=kind+color+':'+f;let g=dots.get(key);if(!g)dots.set(key,g={kind,color,f,pts:[]});g.pts.push(x,y,this.radius(n));}
        for(const g of dots.values()){ctx.globalAlpha=la*g.f;ctx.fillStyle=ctx.strokeStyle=g.color;const p=g.pts;for(let i=0;i<p.length;i+=3){const x=p[i],y=p[i+1],r=p[i+2];ctx.beginPath();if(g.kind==='r')ctx.rect(x-r,y-r,r*2,r*2);else ctx.arc(x,y,r,0,Math.PI*2);if(g.kind==='s')ctx.stroke();else ctx.fill();}}
      }
      ctx.globalAlpha=1;
    }
    // The highlighted dot, its links and its neighbours over the faded web, at strength t (fades in and out).
    paintOverlay(ctx,id,t){
      const {fg,muted}=this.theme(),P=this.model.positions,{x:cx,y:cy,k}=this.camera,W=this.width,H=this.height,m=PAD,nb=this.neighborhood(id),ids=this.prepared().ids;
      ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.setLineDash([]);ctx.strokeStyle=fg;ctx.fillStyle=fg;ctx.lineWidth=1.8;
      const groups=new Map();
      for(const e of nb.edges){const a=P[e.source],b=P[e.target];if(!a||!b)continue;const d=dashOf(e.type),key=d?d[0]:0;let g=groups.get(key);if(!g)groups.set(key,g={dash:d,list:[]});g.list.push({e,ax:a.x*k+cx,ay:a.y*k+cy,bx:b.x*k+cx,by:b.y*k+cy});}
      ctx.globalAlpha=.85*t;
      for(const g of groups.values()){ctx.setLineDash(g.dash||[]);for(const {ax,ay,bx,by} of g.list)if(!((ax<-m&&bx<-m)||(ax>W+m&&bx>W+m)||(ay<-m&&by<-m)||(ay>H+m&&by>H+m)))this.strokeLink(ctx,ax,ay,bx,by,g.dash);}
      ctx.setLineDash([]);ctx.lineDashOffset=0;ctx.globalAlpha=.95*t;
      for(const g of groups.values())for(const {e,ax,ay,bx,by} of g.list)if(e.type==='prerequisite'||e.type==='application'){ctx.beginPath();this.chevrons(ctx,ax,ay,bx,by,this.radius(this.model.byId.get(e.source)),this.radius(this.model.byId.get(e.target)),5.5);ctx.fill();}
      const nodes=[...nb.set].filter(i=>ids.has(i)).map(i=>this.model.byId.get(i)).sort((a,b)=>(b.level||6)-(a.level||6));
      for(const n of nodes){const p=P[n.id];if(!p)continue;const x=p.x*k+cx,y=p.y*k+cy;if(x<-20||x>W+20||y<-20||y>H+20)continue;const hit=n.id===id,r=this.radius(n)+(hit?1:0);ctx.globalAlpha=t;ctx.fillStyle=ctx.strokeStyle=this.model.colors[n.core]||muted;ctx.lineWidth=hit?2:1.6;ctx.beginPath();if(n.layer==='auxiliary')ctx.rect(x-r,y-r,r*2,r*2);else ctx.arc(x,y,r,0,Math.PI*2);if(n.layer==='learning')ctx.stroke();else ctx.fill();if(hit){ctx.beginPath();ctx.arc(x,y,r+5,0,Math.PI*2);ctx.stroke();}}
      ctx.globalAlpha=1;
    }
    // Chooses labels and their sides (Claude, 2026-11-11; semantic zoom, Phase 2). Groups go in LABEL_GROUPS order:
    // levels 1-4, learning notes, level 5, sources, records. A group qualifies once zoomAlpha is above zero; the highlighted dot and its
    // neighbours always do, and under a highlight only they and the subjects are labelled. Within a group, labels
    // already showing come first (so they stop hopping while the map pans), then those nearest the view's centre.
    // A grid replaces the test against every placed label, and MAX_LABELS caps the count.
    placeLabels(active,key){
      const W=this.width,H=this.height,{x:cx,y:cy,k}=this.camera,P=this.model.positions,prep=this.prepared(),{font}=this.theme();
      const nb=active?this.neighborhood(active).set:new Set(),fx=this.labelFx||new Map(),grid=new Map(),placed=new Map(),order=[],seen=new Set();
      const cells=(b,fn)=>{for(let i=Math.floor(b.x/CELL),i1=Math.floor((b.x+b.w)/CELL);i<=i1;i++)for(let j=Math.floor(b.y/CELL),j1=Math.floor((b.y+b.h)/CELL);j<=j1;j++)if(fn(i*1e4+j))return true;return false;};
      const hits=b=>cells(b,c=>grid.get(c)?.some(o=>b.x<o.x+o.w&&b.x+b.w>o.x&&b.y<o.y+o.h&&b.y+b.h>o.y));
      const add=b=>cells(b,c=>{const list=grid.get(c);if(list)list.push(b);else grid.set(c,[b]);});
      const push=n=>{if(n&&!seen.has(n.id)&&prep.ids.has(n.id)){seen.add(n.id);order.push(n);}};
      // Labels also keep off the dots of levels 1-2, of level 3 once its labels qualify, and of the highlighted
      // neighbourhood (Phase 2): a level-2 label used to cover half of a subject dot. Level-3 dots are not obstacles
      // at the whole-web zoom, where they are too dense and blocked most level-2 labels.
      const dot=n=>{const p=P[n.id];if(!p)return;const x=p.x*k+cx,y=p.y*k+cy,r=this.radius(n)+2;if(x>-r&&x<W+r&&y>-r&&y<H+r)add({x:x-r,y:y-r,w:2*r,h:2*r});};
      for(const g of ['L1','L2','L3']){const list=prep.groups.get(g);if(list.length&&(g!=='L3'||this.zoomAlpha(list[0],k)>0))list.forEach(dot);}for(const id of nb){const n=this.model.byId.get(id);if(n&&prep.ids.has(id)&&n.layer==='backbone'&&n.level>3)dot(n);}
      // Under a spotlight the lit dots are labelled first: the dot (or both ends of a link), then its path from the
      // deepest level up, then its typed links and its sub-topics and notes, nearest the centre first. The ordinary
      // labels for the zoom follow at SPOT_LABEL strength in the space left (Phase 3).
      const spot=this.spot,role=id=>spot?.lit.get(id);
      if(spot){
        for(const [id,r] of spot.lit)if(r==='star'||r==='path'||r==='end'){const n=this.model.byId.get(id);if(n&&prep.ids.has(id))dot(n);}
        if(spot.kind==='node')push(this.model.byId.get(spot.id));else{push(this.model.byId.get(spot.edge.source));push(this.model.byId.get(spot.edge.target));}
        for(let i=spot.path.length-1;i>=0;i--)push(this.model.byId.get(spot.path[i]));
        for(const want of ['cast','chorus']){const c=[];for(const [id,r] of spot.lit){if(r!==want||seen.has(id))continue;const p=P[id];if(!p)continue;c.push({id,d:(p.x*k+cx-W/2)**2+(p.y*k+cy-H/2)**2});}c.sort((a,b)=>a.d-b.d);c.forEach(x=>push(this.model.byId.get(x.id)));}
      }
      // In a dive its path is labelled (pinned) after the spotlight's dots; then only the dive's own branch at full
      // strength and its sibling branches at half; fainter branches get no labels (Phase 4).
      const dive=this.dive,fogOf=id=>dive?(dive.fog.get(id)??FOG_OUT):1,cov=this.coverage?this.coverageMap():null,covered=n=>!cov||(cov.factor.get(n.id)??COVER_FADE)===1;
      if(dive)for(let i=dive.trail.length-1;i>=0;i--){const n=this.model.byId.get(dive.trail[i]);if(n&&prep.ids.has(n.id)){dot(n);push(n);}}
      if(active){push(this.model.byId.get(active));for(const n of this.visible.nodes)if(nb.has(n.id))push(n);}
      for(const [g,list] of prep.groups){
        if(!list.length||(active&&g!=='L1')||this.zoomAlpha(list[0],k)<=0)continue;
        const cand=[];
        for(const n of list){if(seen.has(n.id)||(dive&&fogOf(n.id)<.3))continue;const p=P[n.id];if(!p)continue;const px=p.x*k+cx,py=p.y*k+cy;if(px<0||px>W||py<0||py>H)continue;cand.push({n,d:(fx.get(n.id)?.target===1?0:1e9)+(covered(n)?0:5e8)+(px-W/2)**2+(py-H/2)**2});}
        cand.sort((a,b)=>a.d-b.d);for(const c of cand)push(c.n);
      }
      const majors={probability:'Probability\n& foundations',statistics:'Inference\n& modeling',computing:'Computing\n& learning'};
      for(const n of order){
        if(placed.size>=MAX_LABELS)break;
        const isActive=n.id===active,near=nb.has(n.id);
        const p=P[n.id];if(!p)continue;const px=p.x*k+cx,py=p.y*k+cy;if(px<0||px>W||py<0||py>H)continue;
        const major=n.level===1&&!this.focus,[size,weight,wrap]=LABEL_STYLE[groupOf(n)],lh=Math.round(size*1.3),f=`${weight} ${size}px ${font}`,text=major?majors[n.id]||n.label:n.label;
        const box=this.labelBox(text,f,lh,wrap),w=box.w,h=box.h,r=this.radius(n),off=r+6;
        const cands=major?[[-w/2,r+7]]:[[off,-h/2],[-w-off,-h/2],[-w/2,off],[-w/2,-h-off]],old=fx.get(n.id),tries=cands.map((_,i)=>i);
        if(old?.target===1&&old.cand>0&&old.cand<cands.length){tries.splice(old.cand,1);tries.unshift(old.cand);}
        let ci=-1,bx=0,by=0;
        for(const i of tries){const x=px+cands[i][0],y=py+cands[i][1];if(x>=3&&y>=3&&x+w<W-3&&y+h<H-3&&!hits({x:x-3,y:y-2,w:w+6,h:h+4})){ci=i;bx=x;by=y;break;}}
        if(ci<0){if(!major&&!isActive&&!['star','path','end'].includes(role(n.id))&&!dive?.trailSet.has(n.id))continue;ci=0;bx=Math.max(3,Math.min(W-w-3,px+cands[0][0]));by=Math.max(3,Math.min(H-h-3,py+cands[0][1]));}
        add({x:bx-3,y:by-2,w:w+6,h:h+4});placed.set(n.id,{dx:bx-3-px,dy:by-2-py,cand:ci,text,font:f,lh,wrap,node:n,always:near||major||!!role(n.id)||!!dive?.trailSet.has(n.id),dim:(dive?(fogOf(n.id)<1&&!role(n.id)):(!!spot&&!role(n.id)))||(!covered(n)&&!role(n.id)&&!near)});
      }
      for(const [id,s] of fx)if(!placed.has(id))s.target=0;
      for(const [id,p] of placed){const s=fx.get(id);if(s){Object.assign(s,p);s.target=1;}else fx.set(id,{...p,alpha:0,target:1});}
      this.labelFx=fx;this.placedKey=key;this.placedFor=this.visible;this.placedK=k;
    }
    // Draws placed labels at their dots and advances their fades. True while any label is still fading.
    drawLabels(ctx,dt){
      if(!this.labelFx)return false;
      const P=this.model.positions,{x:cx,y:cy,k}=this.camera,ids=this.prepared().ids,W=this.width,H=this.height,d=this.dpr,step=dt/FADE_MS;let fading=false;
      ctx.setTransform(d,0,0,d,0,0);
      for(const [id,s] of this.labelFx){
        if(s.alpha!==s.target){s.alpha=s.target?Math.min(1,s.alpha+step):Math.max(0,s.alpha-step);if(s.alpha!==s.target)fading=true;}
        if(!s.alpha){if(!s.target)this.labelFx.delete(id);continue;}
        const p=P[id];if(!p||!ids.has(id))continue;
        const a=s.alpha*(s.always||!s.node?1:this.zoomAlpha(s.node,k))*(s.dim?SPOT_LABEL:1);if(a<=0)continue; // zoom fade follows the camera every frame (Phase 2)
        const sp=this.sprite(s.text,s.font,s.lh,s.wrap),x=Math.round((p.x*k+cx+s.dx)*d)/d,y=Math.round((p.y*k+cy+s.dy)*d)/d;
        if(x>W||y>H||x+sp.w<0||y+sp.h<0)continue;
        ctx.globalAlpha=a;ctx.drawImage(sp.canvas,x,y,sp.w,sp.h);
      }
      ctx.globalAlpha=1;return fading;
    }
    // Dive (Claude, 2026-11-11, Phase 4): explore from the centre outwards. Diving into a branch frames it; the branch
    // stays at full strength, its sibling branches fade to FOG[1], branches left earlier fade further, and other subjects
    // nearly vanish. The path from the subject stays lit as a thread, and branches dived into earlier this session keep a
    // footprint ring (forgotten when the view closes). A leaf or a learning note dives into its parent branch and stays
    // lit there. The fogged web is cached like the rest of the scene, so it is drawn once per dive step.
    diveInto(id,star){
      let n=this.model.byId.get(id);if(!n||n.layer==='auxiliary')return;
      if(n.layer==='learning'){star=star||n.id;n=this.model.byId.get(n.home);if(!n)return;}
      if(!(this.model.children.get(n.id)||[]).length&&n.parent){star=star||n.id;n=this.model.byId.get(n.parent);}
      if(this.mode==='notes'||(this.mode==='backbone'&&this.model.byId.get(star)?.layer==='learning'))this.mode='learning';
      this.focus=null;this.depth=5;this.depthSelect.value=5;this.autoFit=false;
      const visited=this.dive?.visited||this.visited||(this.visited=new Set());visited.add(n.id);
      this.dive=this.buildDive(n.id,visited);
      const keep=star||(this.spot?.kind==='node'?this.spot.id:null),lit=keep&&this.dive.fog.get(keep)===1?keep:n.id;
      this.spot=this.buildSpot(this.model.byId.get(lit),this.spot?.id===lit?this.spot:null);this.selected=lit;this.selectedLink=null;
      this.update();this.frameDive();
    }
    climb(){const n=this.dive&&this.model.byId.get(this.dive.id);if(!n)return;if(n.parent)this.diveInto(n.parent);else this.exitDive();}
    exitDive(){this.dive=null;this.spot=null;this.selected=null;this.selectedLink=null;this.update();}
    buildDive(id,visited){
      const m=this.model,trail=m.lineage(id).filter(v=>v.layer==='backbone').map(v=>v.id),at=new Map(trail.map((t,i)=>[t,i])),last=trail.length-1,fog=new Map();
      const step=n=>{let x=n.layer==='learning'?m.byId.get(n.home):n.layer==='backbone'?n:null;while(x&&!at.has(x.id))x=m.byId.get(x.parent);return x?at.get(x.id):-1;};
      for(const n of m.nodes){if(at.has(n.id)){fog.set(n.id,1);continue;}const i=step(n);fog.set(n.id,i<0?FOG_OUT:FOG[Math.min(last-i,FOG.length-1)]);}
      return {id,key:'d:'+id,trail,trailSet:new Set(trail),fog,visited:visited||new Set([id])};
    }
    commonAncestor(a,b){const A=this.model.lineage(a).filter(v=>v.layer==='backbone').map(v=>v.id),B=new Set(this.model.lineage(b).filter(v=>v.layer==='backbone').map(v=>v.id));for(let i=A.length-1;i>=0;i--)if(B.has(A[i]))return A[i];return null;}
    // Frames the dive's own branch (its dots and the notes homed in it), not the path above it.
    frameDive(animate=true){const d=this.dive;if(!d)return;const ids=[],vis=this.prepared().ids;for(const [id,f] of d.fog)if(f===1&&(id===d.id||!d.trailSet.has(id))&&vis.has(id))ids.push(id);this.frameIds(ids,3.5,animate);}
    // The dive's thread from the subject, a dashed ring on the branch being explored, and footprints of earlier dives.
    paintDive(ctx){
      const d=this.dive,P=this.model.positions,{x:cx,y:cy,k}=this.camera,ids=this.prepared().ids,byId=this.model.byId,col=this.model.colors[byId.get(d.id)?.core]||this.theme().fg;
      const at=id=>{const p=P[id];return p&&ids.has(id)?{x:p.x*k+cx,y:p.y*k+cy}:null;},pts=d.trail.map(at).filter(Boolean);
      ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.lineCap='round';ctx.lineJoin='round';ctx.setLineDash([]);
      if(pts.length>1){ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle=col;ctx.globalAlpha=.08;ctx.lineWidth=18;ctx.stroke();ctx.globalAlpha=.7;ctx.lineWidth=2.5;ctx.stroke();}
      const c=at(d.id);if(c){ctx.globalAlpha=.85;ctx.strokeStyle=col;ctx.lineWidth=1.6;ctx.setLineDash([3,3]);ctx.beginPath();ctx.arc(c.x,c.y,this.radius(byId.get(d.id))+7,0,Math.PI*2);ctx.stroke();ctx.setLineDash([]);}
      for(const id of d.visited){if(id===d.id)continue;const q=at(id),n=byId.get(id);if(!q||!n)continue;ctx.globalAlpha=.55;ctx.strokeStyle=this.model.colors[n.core]||col;ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(q.x,q.y,this.radius(n)+4,0,Math.PI*2);ctx.stroke();}
      ctx.globalAlpha=1;ctx.lineCap='butt';ctx.lineJoin='miter';
    }
    // Hover peek (extra idea 1): resting on a dot asks the host for Obsidian's page preview of its note, anchored on an
    // invisible box over the dot. Leaving the dot sends that box a mouseout, so the preview closes unless the pointer has
    // moved onto it. Obsidian keeps a preview open only while it believes the pointer is on its target, which it learns
    // from mouseover/mouseout on that box; the box ignores the real pointer (so the dot stays clickable), so while the
    // pointer rests on the dot the box is told so every 150 ms. Each peek gets a new box: Obsidian ignores a request for the same box while its last preview is still
    // closing, which made peeks fail at random. Old boxes are removed a few seconds later. No peek while the camera moves.
    schedulePeek(id,e){
      clearTimeout(this.peekTimer);if(!id||!this.options.onPeek)return;
      this.peekTimer=setTimeout(()=>{
        if(this.hover!==id||this.drag||this.glide||this.wheel)return;const n=this.model.byId.get(id),p=this.screen(id);if(!n||!p||!/\.md$/i.test(n.path))return;
        const r=this.radius(n)+3,a=this.peekAnchor=el('div','sa-peek-anchor');this.stage.append(a);a.style.left=(p.x-r)+'px';a.style.top=(p.y-r)+'px';a.style.width=a.style.height=2*r+'px';
        this.peekId=id;clearInterval(this.peekPulse);this.peekPulse=setInterval(()=>{if(this.peekAnchor===a&&this.hover===id)a.dispatchEvent(new MouseEvent('mouseover'));},150);this.options.onPeek(n.path,a,new MouseEvent('mouseover',{clientX:e.clientX,clientY:e.clientY,ctrlKey:e.ctrlKey,metaKey:e.metaKey,shiftKey:e.shiftKey,altKey:e.altKey})); // a fresh, untargeted event: Obsidian's preview ignored the canvas's own pointermove
      },PEEK_MS);
    }
    endPeek(){clearTimeout(this.peekTimer);clearInterval(this.peekPulse);if(!this.peekId)return;this.peekId=null;const a=this.peekAnchor;this.peekAnchor=null;a?.dispatchEvent(new MouseEvent('mouseout',{bubbles:true,relatedTarget:this.canvas}));setTimeout(()=>a?.remove(),4000);}
    // Keyboard exploring (Claude, 2026-11-11, extra idea 2), with the map focused: up ('deeper') goes further out, to the
    // sub-topic nearest in angle or else an attached note; down ('back') returns to the parent (a note's home); left/right to the previous/next sibling
    // counter-clockwise/clockwise around their parent (subjects around the centre; notes around their home). With nothing
    // lit it starts at the first subject. The light moves as a click would (selection, spotlight or dive), and the camera
    // follows only when the dot nears the edge.
    step(dir){
      const m=this.model,P=m.positions,ang=n=>Math.atan2(P[n.id].y,P[n.id].x),wrap=a=>Math.atan2(Math.sin(a),Math.cos(a)),has=n=>n&&P[n.id];
      const cur=m.byId.get(this.spot?.kind==='node'?this.spot.id:this.selected);let next=null;
      if(!cur)next=m.nodes.find(n=>n.layer==='backbone'&&n.level===1);
      else if(dir==='back')next=m.byId.get(cur.layer==='learning'?cur.home:cur.parent);
      else if(dir==='deeper'){const kids=(m.children.get(cur.id)||[]).map(id=>m.byId.get(id)).filter(has),pool=kids.length?kids:m.nodes.filter(n=>n.layer==='learning'&&n.home===cur.id&&has(n)),a0=has(cur)?ang(cur):0;next=pool.sort((a,b)=>Math.abs(wrap(ang(a)-a0))-Math.abs(wrap(ang(b)-a0)))[0];}
      else{
        const par=m.byId.get(cur.layer==='learning'?cur.home:cur.parent),a0=has(par)?ang(par):0;
        const sib=(cur.layer==='learning'?m.nodes.filter(n=>n.layer==='learning'&&n.home===cur.home):par?(m.children.get(par.id)||[]).map(id=>m.byId.get(id)):m.nodes.filter(n=>n.layer==='backbone'&&n.level===1)).filter(has);
        sib.sort((a,b)=>wrap(ang(a)-a0)-wrap(ang(b)-a0));const i=sib.indexOf(cur);if(sib.length>1&&i>=0)next=sib[(i+(dir==='right'?1:-1)+sib.length)%sib.length];
      }
      if(!next||next===cur)return;
      if(this.spot||this.dive)this.spotlight(next.id,'auto');else this.select(next.id);
    }
    // Coverage glow (Claude, 2026-11-11, extra idea 3). count: learning notes homed at a topic or anywhere below it.
    // factor: 1 for topics with notes and for notes themselves, else COVER_FADE (the not-yet-studied frontier). Per model.
    coverageMap(){
      if(this._cover?.for===this.model)return this._cover;const m=this.model,count=new Map(),factor=new Map();
      for(const n of m.nodes)if(n.layer==='learning'){factor.set(n.id,1);let x=m.byId.get(n.home),guard=0;while(x&&guard++<12){count.set(x.id,(count.get(x.id)||0)+1);x=m.byId.get(x.parent);}}
      for(const [id] of count)factor.set(id,1);
      return this._cover={for:this.model,count,factor};
    }
    notesUnder(id){const c=this.coverageMap().count.get(id)||0;return c===1?'1 note':`${c} notes`;}
    setCoverage(on){this.coverage=!!on;this.coverageToggle?.setAttribute('aria-pressed',String(this.coverage));if(this.coverageKey)this.coverageKey.hidden=!this.coverage;this.update();}
    styleKey(){return (this.dive?.key||'')+(this.coverage?'|cover':'');}
    setFollow(on){this.follow=!!on;this.followToggle?.setAttribute('aria-pressed',String(this.follow));}
    // Spotlight (Claude, 2026-11-11, Phase 3: "Where am I"). The web dims to a tenth. The backbone path from the subject
    // down to the dot is drawn thick in its subject colour over a soft beam; the dot glows and pulses a few times; its
    // typed links (prerequisite, application, related; and its home's, for a learning note) light as the supporting
    // cast; its sub-topics and attached notes stay half lit. frame: 'path' glides to show the whole path, 'close' to
    // the dot, 'auto' only when the dot is near or past the edge of the view. A focused branch is left, because the
    // path needs its ancestors.
    spotlight(id,frame='path'){
      const n=this.model.byId.get(id);if(!n)return;
      if(n.layer==='auxiliary')this.mode='everything';else if(this.mode==='notes'||(this.mode==='backbone'&&n.layer!=='backbone'))this.mode='learning';
      if(n.layer==='backbone')this.depth=Math.max(this.depth,n.level);else if(n.home)this.depth=Math.max(this.depth,this.model.byId.get(n.home)?.level||5);this.depthSelect.value=this.depth;
      this.focus=null;this.selected=id;this.selectedLink=null;this.hover=null;this.autoFit=false;
      // Where am I and follow ('path') are about the whole map, so they leave a dive. A pick outside the dive widens it
      // to the branch both share, without moving the camera (Phase 4).
      if(frame==='path')this.dive=null;else if(this.dive&&(this.dive.fog.get(id)??0)<1){const lca=this.commonAncestor(id,this.dive.id);this.dive=lca?this.buildDive(lca,this.dive.visited):null;}
      this.spot=this.buildSpot(n,this.spot?.kind==='node'&&this.spot.id===id?this.spot:null);this.update();this.frameSpot(frame);
    }
    buildSpot(n,prev){
      const lit=new Map(),edges=[],line=this.model.lineage(n.id),from=new Set([n.id]);
      line.forEach(v=>lit.set(v.id,'path'));lit.set(n.id,'star');if(n.layer==='learning'&&n.home)from.add(n.home);
      for(const e of this.model.edges){
        if((e.type==='prerequisite'||e.type==='application'||e.type==='connection')&&(from.has(e.source)||from.has(e.target))){edges.push({e,role:'cast'});for(const v of [e.source,e.target])if(!lit.has(v))lit.set(v,'cast');}
        else if(e.source===n.id&&(e.type==='contains'||e.type==='attachment')){edges.push({e,role:'chorus'});if(!lit.has(e.target))lit.set(e.target,'chorus');}
      }
      return {kind:'node',id:n.id,key:'n:'+n.id,lit,path:line.map(v=>v.id),edges,t0:prev?.t0??performance.now(),framed:prev?.framed,color:this.model.colors[n.core]};
    }
    linkSpot(e){return {kind:'link',id:e.source+'>'+e.target,key:'l:'+e.type+':'+e.source+':'+e.target,edge:e,lit:new Map([[e.source,'end'],[e.target,'end']]),path:[],edges:[{e,role:'link'}],t0:performance.now(),color:this.model.colors[this.model.byId.get(e.source)?.core]};}
    // Clicking a link selects it (Phase 3): both ends light up and the panel explains the link.
    selectLink(e){this.selectedLink=e;this.selected=null;this.hover=null;this.hoverLink=null;this.spot=this.linkSpot(e);this.update();}
    clearSpot(){this.spot=null;this.selectedLink=null;this.selected=null;this.update();}
    toggleFrame(){if(this.spot)this.frameSpot(this.spot.framed==='close'?'path':'close');}
    // Glides to show these dots, with room for their labels and the breadcrumb bar; zoom capped at maxK.
    frameIds(ids,maxK=2.5,animate=true){
      if(!this.width)return false;let x0=Infinity,y0=Infinity,x1=-Infinity,y1=-Infinity;
      for(const id of ids){const p=this.model.positions[id];if(!p)continue;if(p.x<x0)x0=p.x;if(p.x>x1)x1=p.x;if(p.y<y0)y0=p.y;if(p.y>y1)y1=p.y;}
      if(x0===Infinity)return false;const pad=Math.min(110,this.width*.12),top=(this.spot||this.dive)?44:0,k=Math.min(maxK,(this.width-pad*2)/Math.max(140,x1-x0),(this.height-pad*2-top)/Math.max(140,y1-y0));
      this.moveCamera({k,x:this.width/2-(x0+x1)/2*k,y:(this.height+top)/2-(y0+y1)/2*k},animate);return true;
    }
    frameSpot(frame='path',animate=true){
      const s=this.spot;if(!s)return;if(!this.width){this.pendingFrame=frame;return;}
      if(frame==='auto'){const p=this.screen(s.kind==='node'?s.id:s.edge.target);if(p&&p.x>this.width*.12&&p.x<this.width*.88&&p.y>this.height*.15&&p.y<this.height*.88)return;frame='path';}
      s.framed=frame;
      if(s.kind==='link'){this.frameIds([s.edge.source,s.edge.target],2.2,animate);return;}
      if(frame==='close'){const p=this.model.positions[s.id];if(p){const k=Math.max(1.6,this.camera.k);this.moveCamera({k,x:this.width/2-p.x*k,y:this.height/2-p.y*k},animate);}return;}
      this.frameIds(s.path,2.5,animate);
    }
    // Draws a spotlight over the dimmed web at strength t. True while the spotlit dot is still pulsing.
    paintSpot(ctx,s,t,now){
      const {fg,bg,muted}=this.theme(),P=this.model.positions,{x:cx,y:cy,k}=this.camera,ids=this.prepared().ids,byId=this.model.byId,W=this.width,H=this.height,m=PAD;
      const at=id=>{const p=P[id];return p&&ids.has(id)?{x:p.x*k+cx,y:p.y*k+cy}:null;},off=(a,b)=>(a.x<-m&&b.x<-m)||(a.x>W+m&&b.x>W+m)||(a.y<-m&&b.y<-m)||(a.y>H+m&&b.y>H+m);
      ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.lineCap='round';ctx.lineJoin='round';
      for(const {e,role} of s.edges){
        const a=at(e.source),b=at(e.target);if(!a||!b||off(a,b))continue;const d=role==='chorus'?null:dashOf(e.type);
        ctx.globalAlpha=(role==='chorus'?.35:role==='link'?.95:.75)*t;ctx.strokeStyle=role==='chorus'?muted:fg;ctx.lineWidth=role==='chorus'?1:role==='link'?3:1.7;ctx.setLineDash(d||[]);this.strokeLink(ctx,a.x,a.y,b.x,b.y,d);ctx.setLineDash([]);ctx.lineDashOffset=0;
        if(role!=='chorus'&&(e.type==='prerequisite'||e.type==='application')){ctx.globalAlpha=.9*t;ctx.fillStyle=fg;ctx.beginPath();this.chevrons(ctx,a.x,a.y,b.x,b.y,this.radius(byId.get(e.source)),this.radius(byId.get(e.target)),role==='link'?6.5:5);ctx.fill();}
      }
      const pts=s.path.map(at).filter(Boolean),color=s.color||fg;
      if(pts.length>1){ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.strokeStyle=color;ctx.globalAlpha=.12*t;ctx.lineWidth=26;ctx.stroke();ctx.globalAlpha=.95*t;ctx.lineWidth=3.5;ctx.stroke();}
      let pulsing=false;
      for(const want of ['chorus','cast','path','end','star'])for(const [id,r] of s.lit){
        if(r!==want)continue;const n=byId.get(id),p=at(id);if(!n||!p||p.x<-40||p.x>W+40||p.y<-40||p.y>H+40)continue;
        const c=this.model.colors[n.core]||muted,big=r==='star'||r==='end',rr=this.radius(n)+(r==='star'?3:r==='path'||r==='end'?1.5:0);
        if(big){const R=rr+(r==='star'?36:22),g=ctx.createRadialGradient(p.x,p.y,rr,p.x,p.y,R);g.addColorStop(0,toRgba(c,.5));g.addColorStop(1,toRgba(c,0));ctx.globalAlpha=t;ctx.fillStyle=g;ctx.beginPath();ctx.arc(p.x,p.y,R,0,Math.PI*2);ctx.fill();}
        ctx.globalAlpha=(r==='chorus'?.5:r==='cast'?.85:1)*t;ctx.fillStyle=ctx.strokeStyle=c;ctx.lineWidth=1.8;ctx.beginPath();
        if(n.layer==='auxiliary')ctx.rect(p.x-rr,p.y-rr,rr*2,rr*2);else ctx.arc(p.x,p.y,rr,0,Math.PI*2);
        if(n.layer==='learning'){ctx.fillStyle=bg;ctx.fill();ctx.stroke();}else ctx.fill();
        if(r==='path'||big){ctx.strokeStyle=bg;ctx.lineWidth=2;ctx.beginPath();ctx.arc(p.x,p.y,rr+1.5,0,Math.PI*2);ctx.stroke();}
        if(r==='star'){
          ctx.strokeStyle=fg;ctx.lineWidth=1.6;ctx.beginPath();ctx.arc(p.x,p.y,rr+5,0,Math.PI*2);ctx.stroke();
          const age=now-s.t0;if(age>=0&&age<PULSES*PULSE_MS){const ph=(age%PULSE_MS)/PULSE_MS;ctx.globalAlpha=(1-ph)*.7*t;ctx.strokeStyle=c;ctx.lineWidth=2;ctx.beginPath();ctx.arc(p.x,p.y,rr+5+ph*30,0,Math.PI*2);ctx.stroke();pulsing=true;}
        }
      }
      ctx.globalAlpha=1;ctx.lineCap='butt';ctx.lineJoin='miter';return pulsing;
    }
    // The link under the pointer, drawn thick with rings on its ends (Phase 3).
    paintHoverLink(ctx,e){
      const P=this.model.positions,a=P[e.source],b=P[e.target],ids=this.prepared().ids;if(!a||!b||!ids.has(e.source)||!ids.has(e.target))return;
      const {fg}=this.theme(),{x:cx,y:cy,k}=this.camera,ax=a.x*k+cx,ay=a.y*k+cy,bx=b.x*k+cx,by=b.y*k+cy,d=dashOf(e.type);
      ctx.setTransform(this.dpr,0,0,this.dpr,0,0);ctx.globalAlpha=.9;ctx.strokeStyle=fg;ctx.lineWidth=2.6;ctx.setLineDash(d||[]);this.strokeLink(ctx,ax,ay,bx,by,d);ctx.setLineDash([]);ctx.lineDashOffset=0;ctx.lineWidth=1.5;
      for(const [id,x,y] of [[e.source,ax,ay],[e.target,bx,by]]){ctx.beginPath();ctx.arc(x,y,this.radius(this.model.byId.get(id))+4,0,Math.PI*2);ctx.stroke();}
      ctx.globalAlpha=1;
    }
    // The link under the pointer: within 5 px, typed links preferred by 2 px over hierarchy links (Phase 3).
    hitLink(x,y){let best=null,bd=5;const P=this.model.positions,{x:cx,y:cy,k}=this.camera;for(const e of this.visible.edges){const a=P[e.source],b=P[e.target];if(!a||!b)continue;const ax=a.x*k+cx,ay=a.y*k+cy,dx=b.x*k+cx-ax,dy=b.y*k+cy-ay,L=dx*dx+dy*dy;if(L<1)continue;const t=((x-ax)*dx+(y-ay)*dy)/L;if(t<0||t>1)continue;const d=Math.hypot(ax+t*dx-x,ay+t*dy-y)-(e.type==='contains'?0:2);if(d<bd){bd=d;best=e;}}return best;}
    linkText(e){const a=this.model.byId.get(e.source),b=this.model.byId.get(e.target),meta=LINK_META[e.type]||{name:e.type,arrow:'→'};return `${meta.name}: ${a?.label} ${meta.arrow} ${b?.label}`+(e.reason?'\n'+e.reason:'');}
    renderLinkPanel(){
      const e=this.selectedLink,a=this.model.byId.get(e.source),b=this.model.byId.get(e.target),meta=LINK_META[e.type]||{name:e.type,arrow:'→',says:(x,y)=>`${x} → ${y}`},inProps=e.type==='contains'||e.type==='attachment',writer=inProps?b:a;
      this.panelBody.append(el('div','sa-eyebrow',`LINK · ${meta.name.toUpperCase()}`),el('h3','',`${a.label} ${meta.arrow} ${b.label}`),el('p','sa-muted',meta.says(a.label,b.label)));
      this.panelBody.append(e.reason?el('p','sa-reason',e.reason):el('p','sa-muted','No reason recorded for this link.'));
      this.panelBody.append(el('h4','','Ends'),this.button(a.label,()=>this.spotlight(a.id,'auto')),this.button(b.label,()=>this.spotlight(b.id,'auto')));
      this.panelBody.append(el('h4','','Written on'),this.button(`Open where it's written: ${writer.label}`,()=>this.options.openNote?.(writer.path,inProps?null:'Connections')),el('p','sa-muted',inProps?(e.type==='contains'?'In its parent property.':'In its primary_home property.'):'In its link property, with the reason under Connections.'));
      this.panelBody.append(this.button('Frame both ends',()=>this.frameIds([a.id,b.id],2.2)));
    }
    // Breadcrumb bar over the map while a spotlight is on: each step moves the light; × or Esc leaves it.
    renderCrumbs(){
      const s=this.spot,d=this.dive;this.crumbs.replaceChildren();this.crumbs.hidden=!s&&!d;if(!s&&!d)return;
      // In a dive: its path (each step dives there), the lit dot when it is deeper, and the keys (Phase 4).
      if(d){this.crumbs.append(el('span','sa-crumb-tag','Dive'));d.trail.forEach((id,i)=>{if(i)this.crumbs.append(el('span','sa-crumb-sep','›'));const n=this.model.byId.get(id),b=this.button(n.label,()=>this.diveInto(id));if(id===d.id)b.classList.add('is-current');this.crumbs.append(b);});
        if(s?.kind==='node'&&!d.trailSet.has(s.id)){this.crumbs.append(el('span','sa-crumb-sep','·'));const b=this.button(this.model.byId.get(s.id).label,()=>this.toggleFrame());b.classList.add('is-star');b.title='Switch between the whole path and a close-up';this.crumbs.append(b);}
        this.crumbs.append(el('span','sa-crumb-hint','Arrows move · Space dive · ⌫ up · Esc leave'));const x=this.iconButton('x','×','Leave the dive (Esc)',()=>this.exitDive());x.classList.add('sa-crumb-close');this.crumbs.append(x);return;}
      if(s.kind==='link'){const e=s.edge,a=this.model.byId.get(e.source),b=this.model.byId.get(e.target);this.crumbs.append(this.button(a.label,()=>this.spotlight(a.id,'auto')),el('span','sa-crumb-sep',(LINK_META[e.type]||{arrow:'→'}).arrow),this.button(b.label,()=>this.spotlight(b.id,'auto')));}
      else s.path.forEach((id,i)=>{if(i)this.crumbs.append(el('span','sa-crumb-sep','›'));const n=this.model.byId.get(id),cur=id===s.id,b=this.button(n.label,cur?()=>this.toggleFrame():()=>this.spotlight(id,'auto'));if(cur){b.classList.add('is-current');b.title='Switch between the whole path and a close-up';}this.crumbs.append(b);});
      if(s.kind==='node')this.crumbs.append(el('span','sa-crumb-hint','Arrows move · Space dive · Enter open'));const x=this.iconButton('x','×','Leave the spotlight (Esc)',()=>this.clearSpot());x.classList.add('sa-crumb-close');this.crumbs.append(x);
    }
    hit(x,y){let id=null,best=Infinity;const P=this.model.positions,{x:cx,y:cy,k}=this.camera;for(const n of this.visible.nodes){const p=P[n.id];if(!p)continue;const d=Math.hypot(p.x*k+cx-x,p.y*k+cy-y);if(d<Math.max(8,this.radius(n)+4)&&d<best){best=d;id=n.id;}}return id;}
    attachCanvas(){
      const local=e=>{const b=this.canvas.getBoundingClientRect();return{x:e.clientX-b.left,y:e.clientY-b.top};};
      this.canvas.tabIndex=0;
      // Esc leaves a spotlight or a selected link (Phase 3); the search box keeps its own Esc.
      // Keys (Phase 3-4 and extra idea 2; the search box keeps its own): Esc leaves a dive, else a spotlight; Backspace
      // climbs one level of a dive. With the map focused: the arrows move the light (step), Space dives into the lit or
      // selected dot's branch, Enter opens its note.
      const arrows={ArrowUp:'deeper',ArrowDown:'back',ArrowLeft:'left',ArrowRight:'right'}; // up goes further out, down comes back (user request, 2026-11-11)
      this.host.addEventListener('keydown',e=>{if(e.target.closest?.('input,select,textarea'))return;const stop=()=>{e.preventDefault();e.stopPropagation();},cur=this.spot?.kind==='node'?this.spot.id:this.selected;
        if(e.key==='Escape'&&(this.dive||this.spot||this.selectedLink)){stop();if(this.dive)this.exitDive();else this.clearSpot();}
        else if(e.key==='Backspace'&&this.dive){stop();this.climb();}
        else if(e.target!==this.canvas||e.ctrlKey||e.metaKey||e.altKey)return;
        else if(e.key===' '&&cur){stop();this.diveInto(cur);}
        else if(e.key==='Enter'&&cur){stop();const n=this.model.byId.get(cur);if(n)this.options.openNote?.(n.path);}
        else if(arrows[e.key]){stop();this.step(arrows[e.key]);}});
      this.canvas.addEventListener('pointerdown',e=>{const p=local(e);this.endPeek();this.canvas.focus({preventScroll:true});this.glide=null;this.wheel=null;this.drag={...p,cx:this.camera.x,cy:this.camera.y,moved:false};try{this.canvas.setPointerCapture(e.pointerId);}catch{}});
      this.canvas.addEventListener('pointermove',e=>{const p=local(e);if(this.drag){const dx=p.x-this.drag.x,dy=p.y-this.drag.y;if(Math.hypot(dx,dy)>5)this.drag.moved=true;if(this.drag.moved){this.camera={...this.camera,x:this.drag.cx+dx,y:this.drag.cy+dy};this.markMotion();this.draw();}}else{const id=this.hit(p.x,p.y),link=id?null:this.hitLink(p.x,p.y);this.tooltip.style.left=Math.min(p.x+12,this.width-250)+'px';this.tooltip.style.top=Math.max(3,p.y-35)+'px';if(id===this.hover&&link===this.hoverLink)return;if(id!==this.hover){this.endPeek();this.schedulePeek(id,e);}this.hover=id;this.hoverLink=link;const n=this.model.byId.get(id);this.tooltip.textContent=n?`${n.label} · ${n.layer==='backbone'?'L'+n.level+' · '+n.stage:n.layer}${this.coverage&&n.layer==='backbone'?' · '+this.notesUnder(n.id):''}`:link?this.linkText(link):'';this.tooltip.hidden=!n&&!link;this.canvas.style.cursor=n?'pointer':'grab';this.draw();}});
      // Click: a dot selects it (inside a spotlight, moves the light there); clicking the spotlit dot again, or empty map,
      // leaves the spotlight without moving the camera. Double-click a dot: open its note. (Phase 3)
      // Link clicks (select a link, double-click to frame its ends) were turned off at the user's request (2026-11-11):
      // a dot's panel already lists its links with reasons, and clicks near the dense hierarchy lines picked a link
      // instead of leaving the spotlight. Hovering a link still shows its reason. selectLink/renderLinkPanel remain unhooked.
      this.canvas.addEventListener('pointerup',e=>{const p=local(e),moved=this.drag?.moved;this.drag=null;if(moved)return;const id=this.hit(p.x,p.y);if(id){if(this.spot?.kind==='node'&&this.spot.id===id)this.clearSpot();else if(this.spot)this.spotlight(id,'auto');else this.select(id);return;}if(this.spot||this.selectedLink)this.clearSpot();});
      this.canvas.addEventListener('contextrestored',()=>{this.sceneKey=null;this.draw();});
      this.canvas.addEventListener('pointercancel',()=>this.drag=null);
      this.canvas.addEventListener('pointerleave',()=>{this.endPeek();this.hover=null;this.hoverLink=null;this.tooltip.hidden=true;this.draw();});
      this.canvas.addEventListener('dblclick',e=>{const p=local(e),n=this.model.byId.get(this.hit(p.x,p.y));if(n)this.options.openNote?.(n.path);});
      // Smoothed wheel zoom (Claude, 2026-11-11): each notch moves a target zoom; frames ease toward it around the pointer.
      this.canvas.addEventListener('wheel',e=>{e.preventDefault();this.endPeek();const p=local(e),dy=e.deltaMode===1?e.deltaY*16:e.deltaMode===2?e.deltaY*400:e.deltaY;this.glide=null;const w=this.wheel||(this.wheel={k:this.camera.k});w.k=Math.max(.04,Math.min(7,w.k*Math.exp(-dy*.0015)));w.x=p.x;w.y=p.y;this.markMotion();this.draw();},{passive:false});
    }
    destroy(){if(this.frame)cancelAnimationFrame(this.frame);clearTimeout(this.idleTimer);clearTimeout(this.peekTimer);clearInterval(this.peekPulse);this.cancelMotionCache();if(this.motionCache){this.motionCache.canvas.width=this.motionCache.canvas.height=0;this.motionCache=null;}this.glide=this.wheel=null;this.resizeObserver?.disconnect();this.themeObserver?.disconnect();if(this.scene){this.scene.width=this.scene.height=0;this.scene=null;}this._sprites=null;this.host.replaceChildren();}
  }
  return Atlas;
})();
if(typeof module!=='undefined')module.exports=AtlasUI;
