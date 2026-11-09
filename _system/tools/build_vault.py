"""Build the agreed minimal atlas in a fresh output directory; never overwrite edits."""
import argparse, collections, hashlib, html, json, math, pathlib, re, shutil
import yaml

HERE=pathlib.Path(__file__).resolve().parent
VAULT_ROOT=HERE.parent.parent if HERE.name=='tools' and HERE.parent.name=='_system' else None
BASELINE=(VAULT_ROOT/'_system/baseline') if VAULT_ROOT else pathlib.Path(r'D:\CodexStorage\codex-home\visualizations\2026\11\08\01a1ba3b-79ee-7411-844f-f9725f9a364e')
PLUGIN_SOURCE=(VAULT_ROOT/'_system/plugin-src') if VAULT_ROOT else HERE
SOP_SOURCE=(VAULT_ROOT/'AGENTS.md') if VAULT_ROOT else HERE/'AGENTS.md'
DATE='2026-11-08'
VALIDATION_BODY='''# Validation report

Completed on 2026-11-08 for the initial build in `D:\\obsidian_centre\\stats_ML_rebuild`.

## Backbone and files

- 756 backbone pages: L1 3; L2 22; L3 51; L4 104; L5 576.
- All 843 typed, directed baseline connections preserved: 753 hierarchy edges and 90 cross-links.
- All stable IDs, parents, study bands, subjects, breadcrumbs, and connection reasons matched against the frozen baseline. The approved display-title change is ELBO, retaining Calculate the ELBO as its alias.
- 28 source records. No broken generated wikilinks, duplicate IDs, or case-insensitive path collisions. The longest absolute backbone path is 234 characters.
- Backbone coordinates matched the original JavaScript layout formula to within 1e-8, with its original ordering and color families.
- Zero personal learning notes and no migrated raw files. The source-vault audit covered 158 files across wiki/, raw/, and AGENTS.md; all hashes remained unchanged. Five of the six tracked pre-existing rebuild files matched their original hashes, including the SOP draft and Welcome page. Obsidian's native graph.json changed during the live app session; the installer and plugin do not write that file, and its current app state was preserved.
- The preserved Welcome.md tutorial and historical SOP draft are outside the generated-content link audit. Their original content was retained.

## Graph behavior and interface

- Model tests passed for the complete backbone and level filters.
- Two synthetic learning notes and a shared PDF were tested outside the vault: one primary home each, three selected backbone links, a note-to-note link, one shared source dot, and no line from an incidental body mention. No fixture was installed as user learning material.
- The first two modes exclude auxiliary records. Sources appear only in Everything. Adding those fixtures did not change any backbone coordinate. Invalid primary homes were reported.
- Browser checks covered all three switches, fixed camera on mode changes, title/alias search, branch focus, level filtering, note-open callback, source visibility, and a 390-pixel layout without horizontal overflow. The final preview had no browser console errors.
- The JavaScript plugin bundle passed Node syntax checking.

## Live Obsidian check

Verified in Obsidian 1.15.0 after the user enabled the plugin at Obsidian's first-use trust prompt. The plugin loaded and displayed 756 backbone topics. Backbone showed 756 nodes and 843 edges; My learning showed the same backbone with the explicit zero-notes message; Everything showed 799 nodes and 2293 total conceptual/provenance connections, including the preserved administrative files.

Searching Calculate the ELBO returned ELBO. Selecting it showed its full five-level path and connection reasons. Open note opened the actual nested ELBO.md page, displaying the approved title/alias, level, subject, study band, tags, parent, sources, and plain-text breadcrumb.

The standalone [[_system/Previews/backbone-map.jpg|map preview]] uses the same renderer. It is a preview of this initial scaffold, not an imported learning note.

## Scope and rerunning

These are structural and application checks, not verification of mathematical explanations on every page. The initial reference pages intentionally contain titles and relationships rather than full lessons. Personal-note behavior was checked with synthetic fixtures; existing-note migration has not started.

Initial-build checks (Python with PyYAML and Node.js required):

```powershell
python _system/tools/validate.py . --export "$env:TEMP/statistics-atlas-check.json"
node _system/tools/test-model.cjs "$env:TEMP/statistics-atlas-check.json"
node --check .obsidian/plugins/statistics-atlas/main.js
```

The initial-build validator intentionally expects the frozen 756-node scaffold and no personal notes. Adapt its expectations during a separately authorized expansion or migration. The plugin's own Map checks report current metadata/link issues. Do not rerun the initial page generator over edited content; its hash guard refuses overwriting changed files.
'''

def build(out):
    baseline=json.loads((BASELINE/'statistics-backbone.json').read_text(encoding='utf-8'))
    nodes=baseline['nodes']; by={n['id']:n for n in nodes}; edges=baseline['edges']
    titles={n['id']:('ELBO' if n['id']=='elbo' else n['label']) for n in nodes}
    counts=collections.Counter(t.casefold() for t in titles.values())
    def safe(text):
        text=re.sub(r'[<>:"/\\|?*\x00-\x1f]',lambda m:' - ' if m.group() in '/\\|:' else '',text)
        text=re.sub(r'\s+',' ',text).strip(' .')
        if re.fullmatch(r'(?i)(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?',text):text+=' - topic'
        return text
    def lineage(n):
        chain=[]
        while n:chain.insert(0,n);n=by.get(n['parent'])
        return chain
    paths={}
    for n in nodes:
        filename=safe(titles[n['id']])+(f" (L{n['level']})" if counts[titles[n['id']].casefold()]>1 else '')+'.md'
        paths[n['id']]=pathlib.PurePosixPath('Backbone',*(safe(titles[a['id']]) for a in lineage(n) if a['level']<5),filename).as_posix()
    assert len({p.casefold() for p in paths.values()})==len(nodes)
    outputs={}
    def put(path,text):outputs[path]=text.encode('utf-8') if isinstance(text,str) else text
    def md(path,props,body):put(path,'---\n'+yaml.safe_dump(props,sort_keys=False,allow_unicode=True,width=100000)+'---\n\n'+body.rstrip()+'\n')
    def link(id):return '[['+paths[id][:-3]+']]'
    def displaylink(id):return '[['+paths[id][:-3]+'|'+titles[id]+']]'
    sources={k:f'_system/Sources/{k}.md' for k in baseline['sources']}
    for n in nodes:
        nid=n['id']; chain=lineage(n); outgoing=[e for e in edges if e['source']==nid and e['type']!='contains']
        props=dict(id=nid,title=titles[nid],layer='backbone',level=n['level'],subject=n['core'],study_band=n['stage'],backbone_path=' → '.join(titles[a['id']] for a in chain),created=DATE,updated=DATE)
        props['aliases']=[n['label']] if nid=='elbo' else []
        props['tags']=['atlas/backbone','subject/'+n['core'],'level/'+str(n['level']),'study/'+{'Foundation':'foundation','U':'undergraduate','U–M':'undergraduate-masters','M':'masters','M elective':'masters-elective','U–M elective':'shared-elective'}[n['stage']]]
        props['node_kind']=n.get('kind','group')
        if n['parent']:props['parent']=link(n['parent'])
        props['connections']=[link(e['target']) for e in outgoing]
        props['sources']=['[['+sources[s][:-3]+']]' for s in n['sources']]
        body=f"# {titles[nid]}\n\n{props['backbone_path']}\n\n"
        if n['parent']:body+='Parent: '+displaylink(n['parent'])+'\n\n'
        children=[c for c in nodes if c['parent']==nid]
        if children:body+='## Topics\n\n'+'\n'.join('- '+displaylink(c['id']) for c in children)+'\n\n'
        if outgoing:body+='## Connections\n\n'+'\n'.join('- '+displaylink(e['target'])+' — '+e['reason'] for e in outgoing)+'\n\n'
        incoming=[e for e in edges if e['target']==nid and e['type']!='contains']
        if incoming:body+='## Connected from\n\n'+'\n'.join('- '+displaylink(e['source'])+' — '+e['reason'] for e in incoming)+'\n\n'
        md(paths[nid],props,body)
    for sid,s in baseline['sources'].items():
        md(sources[sid],dict(id='source:'+sid,title=s['title'],layer='auxiliary',role='source',url=s['url'],created=DATE,tags=['atlas/auxiliary','source/curriculum']),f"# {s['title']}\n\n[Read the source]({s['url']})\n\nCoverage: {s['scope']}.\n\nThis reference supports the backbone's topic coverage. It is not a verification of detailed mathematics on the initially empty pages.")
    put('AGENTS.md',SOP_SOURCE.read_bytes())
    md('CLAUDE.md',dict(id='system-claude',title='Instructions for Claude',layer='auxiliary',connections=['[[AGENTS]]']), '# Instructions for Claude\n\nRead and follow [[AGENTS|the authoritative SOP]]. The prior `_system/SOP draft.md` is historical. Do not use it as the active SOP.\n\nExisting-note migration is not authorized in the initial build.')
    md('_system/Final SOP.md',dict(id='system-final-sop',title='Final SOP',layer='auxiliary',connections=['[[AGENTS]]']), '# Final SOP\n\nThe complete approved SOP is [[AGENTS|Statistics vault SOP]]. Maintain that single authoritative version.\n\nIt is the Codex SOP confirmed by the user, with all approved amendments. The earlier SOP draft is preserved as historical material.')
    md('Start Here.md',dict(id='system-start',title='Start here',layer='auxiliary',connections=['[[AGENTS]]','[[_system/Build status]]']), '# Statistics atlas\n\nOpen **Statistics atlas: Open statistics atlas** from the command palette, or select the network icon in the ribbon.\n\n- **Backbone** shows all 756 reference topics and 843 connections.\n- **My learning** adds personal notes and selected connections. It initially has no personal notes.\n- **Everything** adds source records and administrative material. Use **Fit visible** to include the outer auxiliary cluster.\n\nSearch a title or alias to focus a branch. Select a dot to inspect its path and connections; double-click a dot or choose **Open note** to open its page. Zoom with the wheel, drag to pan, and use **Whole web** to return.\n\nThe map reads note properties. Plain-text breadcrumbs do not create edges. Backbone positions are frozen across view switches and personal-note additions.\n\n[[AGENTS|Read the agreed SOP]] · [[_system/Build status|Build status]] · [[_system/Catalog|Topic catalog]]\n\nYour existing notes have not been migrated. The ELBO personal-note example is a future supervised migration, not a note created by this build.')
    md('_system/Build status.md',dict(id='system-build-status',title='Build status',layer='auxiliary',connections=['[[AGENTS]]','[[_system/Map implementation]]']), '# Build status\n\nInitial backbone and local three-view map constructed on 2026-11-08.\n\n- Backbone: 756 pages; 753 hierarchy edges; 90 cross-links.\n- Sources: 28 curriculum/reference records.\n- Approved title: ELBO, alias Calculate the ELBO; stable ID preserved.\n- Personal learning notes: zero.\n- Migration: not started; requires a separate user instruction.\n\nSee [[_system/Validation report|the validation report]] for performed checks and limits. The old SOP draft remains historical; [[AGENTS]] is authoritative.')
    md('_system/Digest Checkpoints.md',dict(id='system-checkpoints',title='Digest checkpoints',layer='auxiliary'), '# Digest checkpoints\n\nNo learning digests have been performed in this rebuild. No old chat boundaries have been imported or advanced. Future digests must record actual chat/source keys, precise excluded/included boundaries, covered sources, destinations, and pending gaps.')
    md('_system/Review Queue.md',dict(id='system-review',title='Review queue',layer='auxiliary'), '# Review queue\n\nNo learning material has been migrated. Do not treat absent old review items as resolved. Retain and reconcile their provenance during an authorized supervised migration.')
    md('_system/Validation report.md',dict(id='system-validation',title='Validation report',layer='auxiliary'),VALIDATION_BODY)
    md('_system/Log.md',dict(id='system-log',title='Activity log',layer='auxiliary'), '# Activity log\n\n## [2026-11-08] setup | Statistics backbone and three-view atlas\n\nUser explicitly authorized the final Codex SOP and the complete initial backbone/map, excluding migration. Generated all 756 minimal reference pages from the frozen researched baseline and preserved its 843 connections. Added the approved ELBO title/alias, safe names, nested folders, plain-text paths, source records, and a local map plugin. Existing learning notes and raw sources were not migrated. See [[_system/Validation report|validation]] and [[AGENTS|the active SOP]].')
    md('_system/Migration ledger.md',dict(id='system-migration',title='Migration ledger',layer='auxiliary'), '# Migration ledger\n\nMigration has not started. During supervised migration, record each original page/source, its hash or precise locator, destination note(s), retained reasoning and images, consolidation decisions, and unresolved gaps. Do not invent historical coverage.')
    md('_system/Templates/Learning note.md',dict(id='template-learning',title='Learning note template',layer='auxiliary'), '# Learning note template\n\nUse only during an authorized digest; this template is not a learning note.\n\n```yaml\nlayer: learning\nid: unique-stable-id\ntitle: A useful question or topic\nprimary_home: "[[full/vault/path/to/backbone/page]]"\nsubject: computing\nbackbone_path: Plain text full ancestry\nnote_types: [question, derivation]\nquestion_roles: [reconcile-approaches]\nsource_format: handwriting\nconnections:\n  - "[[full/vault/path/to/selected/connection]]"\nsources:\n  - "[[raw/path/to/original]]"\n```\n\nLead with the substantive content. Embed selected handwriting beside its explanation. Keep the coherent topic together. Give each declared connection one line in a Connections section: `- [[full/path|Title]] — why the connection matters`. Ask the user about uncertain selections. Preserve originals and provenance.')
    md('_system/Map implementation.md',dict(id='system-implementation',title='Map implementation',layer='auxiliary',connections=['[[AGENTS]]']), '# Map implementation\n\nPlugin: `statistics-atlas`, local, no external dependencies or network requests. The plugin reads Markdown properties and shows a custom ItemView using the documented Obsidian API. It does not rewrite notes.\n\nLive authority: note properties. `_system/baseline/statistics-backbone.json` is the frozen original; `_system/layout.json` preserves original ordering, coordinates, colors and the baseline edge metadata. `connections` declares extra edges; one-line body reasons explain them. The baseline supplies original prerequisite/application types and directions. `sources` creates separate provenance edges visible only in Everything. Plain-text paths, body links, and tags create no conceptual edges.\n\nThe original all-level radial layout is retained. Depth filters hide nodes without moving their saved positions. Branch focus zooms the same fixed geometry. A new backbone ID without a saved position is shown as a provisional placement with a warning; approving and recording a new layout is a separate maintenance decision.\n\nThe native Obsidian graph remains available and follows its own wikilink behavior. This plugin does not modify graph.json.\n\nSource: `_system/plugin-src/`. Checks: `_system/tools/validate.py` and `_system/tools/test-model.cjs`. Rebuild the plugin by concatenating core.js, ui.js, plugin.js in that order into `.obsidian/plugins/statistics-atlas/main.js`, then reload the plugin. Preserve changes to notes; do not rerun the initial page generator over an edited vault.\n\nReferences: [Obsidian custom views](https://github.com/obsidianmd/obsidian-developer-docs/blob/main/en/Plugins/User%20interface/Views.md), [plugin installation](https://docs.obsidian.md/Plugins/Getting%20started/Build%20a%20plugin).')
    body='# Topic catalog\n\nAll 756 reference nodes. Paths and links are organizational; they are not study completion records.\n\n'
    for root in [n for n in nodes if n['level']==1]:
        body+='## '+titles[root['id']]+'\n\n'
        body+='\n'.join('- L'+str(n['level'])+' · '+displaylink(n['id'])+' · '+n['stage'] for n in nodes if n['core']==root['id'])+'\n\n'
    md('_system/Catalog.md',dict(id='system-catalog',title='Topic catalog',layer='auxiliary'),body)
    put('_system/catalog.json',json.dumps({'created':DATE,'nodes':[{'id':n['id'],'title':titles[n['id']],'path':paths[n['id']],'level':n['level'],'order':i} for i,n in enumerate(nodes)]},ensure_ascii=False,indent=2))
    children={n['id']:[c for c in nodes if c['parent']==n['id']] for n in nodes}
    def leafcount(n):return 1 if n['level']==5 else sum(leafcount(c) for c in children[n['id']])
    positions={};order={n['id']:i for i,n in enumerate(nodes)}
    def place(n,a,b):
        mid=(a+b)/2;r=[0,420,740,1040,1330,1620][n['level']];j=35*math.sin(order[n['id']]*2.4) if n['level']==5 else 0
        positions[n['id']]={'x':math.cos(mid)*(r+j),'y':math.sin(mid)*(r+j)}
        kids=children[n['id']];total=sum(max(1,leafcount(c)) for c in kids);t=a
        for c in kids:
            w=(b-a)*max(1,leafcount(c))/total;place(c,t,t+w);t+=w
    roots=[n for n in nodes if n['level']==1];weights=[leafcount(n)**.65 for n in roots];angle=-math.pi*.83
    for n,w in zip(roots,weights):
        span=(math.pi*2-.085*3)*w/sum(weights);place(n,angle,angle+span);angle+=span+.085
    put('_system/layout.json',json.dumps({'version':1,'created':DATE,'colors':{'probability':'#339cff','statistics':'#f3883b','computing':'#5dc977'},'order':[n['id'] for n in nodes],'positions':positions},indent=2))
    for name in ['statistics-backbone.json','atlas-template.html','build_atlas.py']:
        put('_system/baseline/'+name,(BASELINE/name).read_bytes())
    for name in ['core.js','ui.js','plugin.js','styles.css']:
        put('_system/plugin-src/'+name,(PLUGIN_SOURCE/name).read_bytes())
    plugin='.obsidian/plugins/statistics-atlas/'
    put(plugin+'main.js','\n'.join((PLUGIN_SOURCE/n).read_text(encoding='utf-8') for n in ['core.js','ui.js','plugin.js']))
    put(plugin+'styles.css',(PLUGIN_SOURCE/'styles.css').read_bytes())
    put(plugin+'manifest.json',json.dumps({'id':'statistics-atlas','name':'Statistics atlas','version':'1.0.0','minAppVersion':'1.5.0','description':'A fixed five-level statistics backbone with learning and auxiliary views.','author':'Local vault project','isDesktopOnly':False},indent=2))
    for name in ['validate.py','test-model.cjs']:
        if (HERE/name).exists():put('_system/tools/'+name,(HERE/name).read_bytes())
    put('_system/tools/build_vault.py',pathlib.Path(__file__).read_bytes())
    preview=(VAULT_ROOT/'_system/Previews/backbone-map.jpg') if VAULT_ROOT else HERE/'atlas-preview.jpg'
    if preview.exists():put('_system/Previews/backbone-map.jpg',preview.read_bytes())
    # Only refresh files still byte-identical to this builder's previous output.
    previous_path=out/'_system/build-manifest.json'
    previous=json.loads(previous_path.read_text(encoding='utf-8')).get('files',{}) if previous_path.exists() else {}
    for path,data in outputs.items():
        file=out/path
        if file.exists() and file.read_bytes()!=data and hashlib.sha256(file.read_bytes()).hexdigest()!=previous.get(path):raise RuntimeError('Refusing to overwrite changed file: '+str(file))
    for path,data in outputs.items():
        file=out/path;file.parent.mkdir(parents=True,exist_ok=True)
        if not file.exists() or file.read_bytes()!=data:file.write_bytes(data)
    for folder in ['raw/assets','raw/conversations','raw/notes','raw/articles','raw/books','raw/papers','assets/figures','Learning']:(out/folder).mkdir(parents=True,exist_ok=True)
    for n in nodes:
        if n['level']==2:(out/'Learning'/safe(titles[n['parent']])/safe(titles[n['id']])).mkdir(parents=True,exist_ok=True)
    manifest={'created':DATE,'files':{p:hashlib.sha256(b).hexdigest() for p,b in outputs.items()},'backbone_nodes':len(nodes),'backbone_edges':len(edges),'migrated_learning_notes':0}
    (out/'_system/build-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps({'output':str(out),'files':len(outputs),'backbone_nodes':len(nodes),'edges':len(edges),'longest_backbone_path':max(len(str(out/p)) for p in paths.values())}))
    return baseline

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args();build(pathlib.Path(args.output).resolve())
