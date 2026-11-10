"""Read-only vault validator: checks rules that must always hold, however much the vault grows.

Rewritten by Claude (Opus 5.5) on 2026-11-08, AGENTS A3; documented in _system/Claude/Validator.md.
The previous version compared the vault with the frozen 756-node snapshot, so every legitimate digest,
new backbone node, new cross-link or retitle failed, and some real mistakes passed.

Three result levels:
  error    a rule is broken; exit code 1
  warning  allowed, but a follow-up is needed (e.g. save a map position for a new backbone node)
  change   a deliberate difference from the frozen 2026-11-08 baseline; listed for review, never fails

Usage:
  python _system/tools/validate.py .                      human-readable report
  python _system/tools/validate.py . --json               machine-readable report
  python _system/tools/validate.py . --export FILE.json   also write records for test-model.cjs
  --display-root PATH   real vault root for the path-length rule when checking a copy elsewhere
"""
import argparse, collections, json, os, pathlib, re, sys

try:
    import yaml
    load_yaml = yaml.safe_load
except ImportError:
    # Fallback (Claude, 2026-11-08): PyYAML is not installed on this machine. This parser covers the flat
    # frontmatter used in this vault (scalars, [] / [a, b] flow lists, '- item' block lists) and raises on anything else.
    def _scalar(v):
        v = v.strip()
        if v.startswith("'") and v.endswith("'"): return v[1:-1].replace("''", "'")
        if v.startswith('"') and v.endswith('"'): return json.loads(v)
        if re.fullmatch(r'-?\d+', v): return int(v)
        return v

    def load_yaml(text):
        data, key = {}, None
        for line in text.splitlines():
            if not line.strip(): continue
            if line.startswith('- ') and key is not None: data[key].append(_scalar(line[2:])); continue
            m = re.match(r'^([A-Za-z_][\w-]*):(?: (.*))?$', line)
            if not m: raise ValueError('Unsupported frontmatter line: ' + line)
            key, value = m.group(1), (m.group(2) or '').strip()
            if value == '': data[key] = []
            elif value.startswith('[') and value.endswith(']'): data[key] = [_scalar(v) for v in value[1:-1].split(',') if v.strip()]; key = None
            else: data[key] = _scalar(value); key = None
        return data

# Vocabulary agreed in AGENTS.md (§3, §6). Change these together with the SOP.
LINK_TYPES = {'prerequisite_for': 'prerequisite', 'applied_in': 'application', 'related': 'connection'}
NOTE_TYPES = {'question', 'practice', 'derivation', 'insight', 'topic-note', 'conversation-digest'}
QUESTION_ROLES = {'concept-distinction', 'cross-topic-connection', 'reconcile-approaches', 'assumption-boundary',
                  'surprising-result', 'special-to-general', 'mechanism', 'modeling-consequence'}
SYSTEM_FILES = {'AGENTS.md', 'CLAUDE.md', 'Start Here.md', 'Welcome.md'}
SKIP_LINK_CHECK = ('Welcome.md', '_system/SOP/history/', '_system/Templates/')   # historical text and placeholders
MAX_PATH = 240                      # Windows' limit is 260; keep headroom for longer titles
ILLEGAL = re.compile(r'[<>:"/\\|?*]')
LINK_RE = re.compile(r'!?\[\[([^\]]+)\]\]')
REASON_RE = re.compile(r'^\s*-\s*\[\[([^\]]+)\]\]\s*[—–]\s*\S')

# Rule codes, also listed in _system/Claude/Validator.md.
RULES = {
    'F0': 'properties parse, and no property key appears twice',
    'F1': 'every link and embed resolves',
    'F3': f'full path is at most {MAX_PATH} characters',
    'F4': 'no character Windows forbids in a file name',
    'B1': 'backbone and learning notes have a unique id',
    'B2': 'backbone level is 1-5',
    'B3': 'level 1 has no parent; other levels have a backbone parent one level up',
    'B4': 'no parent cycles',
    'B5': 'subject matches the level-1 root',
    'B6': 'backbone_path matches the parent chain',
    'B7': 'no two Markdown files share a file name',
    'B9': 'backbone page has exactly one ```atlas block',
    'L1': 'layer property is present and matches the folder',
    'L2': 'learning note has exactly one primary_home, and it is a backbone page',
    'L3': 'note_types / question_roles use the agreed vocabulary',
    'L4': "learning note's backbone_path matches its home's path",
    'C1': 'every connection target exists',
    'C2': 'every connection has a "- [[target]] — reason" line',
    'C3': 'no note links to itself',
    'C4': 'backbone pages use typed links, not connections',
    'C5': 'backbone pages never link to learning notes',
    'W1': 'new backbone node has no saved map position yet',
    'W2': 'several pages share one display title',
}


def clean(link):
    # `[[page\|alias]]` is how Obsidian writes an aliased link inside a table; drop the escaping backslash.
    return str(link).strip().removeprefix('!').removeprefix('[[').removesuffix(']]').split('|')[0].removesuffix('\\').split('#')[0].strip()


def as_list(v):
    return [] if v in (None, '') else v if isinstance(v, list) else [v]


class Vault:
    def __init__(self, root, display_root):
        self.root, self.display_root = root, display_root
        self.notes, self.by_path, self.by_name, self.files = {}, {}, collections.defaultdict(list), set()
        self.out = {'error': [], 'warning': [], 'change': []}
        self.counts = {}

    def add(self, sev, rule, msg):
        self.out[sev].append((rule, msg))

    def load(self):
        for dirpath, dirnames, filenames in os.walk(self.root):
            dirnames[:] = sorted(d for d in dirnames if not d.startswith('.'))
            for name in sorted(filenames):
                full = pathlib.Path(dirpath, name)
                rel = full.relative_to(self.root).as_posix()
                self.files.add(rel)
                self.by_name[name.lower()].append(rel)
                length = len(self.display_root) + 1 + len(rel)
                if length > MAX_PATH:
                    self.add('error', 'F3', f'{length} chars > {MAX_PATH}: {rel}')
                if not name.endswith('.md'):
                    continue
                text = full.read_text(encoding='utf-8')
                m = re.match(r'^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)', text)
                fm = {}
                if m:
                    keys = re.findall(r'^([A-Za-z_][\w-]*):', m.group(1), re.M)
                    for k in sorted({k for k in keys if keys.count(k) > 1}):
                        self.add('error', 'F0', f'property "{k}" appears twice; only the last one is kept: {rel}')
                    try:
                        fm = load_yaml(m.group(1)) or {}
                    except Exception as e:
                        self.add('error', 'F0', f'properties do not parse ({e}): {rel}')
                self.notes[rel] = {'path': rel, 'fm': fm, 'body': text[m.end():] if m else text, 'stem': name[:-3]}
                self.by_path[rel[:-3].lower()] = rel

    def resolve(self, link):
        """Obsidian-style: full vault path first, then a unique file name (shortest-path links)."""
        t = clean(link)
        if not t:
            return None
        if t.lower() in self.by_path:
            return self.by_path[t.lower()]
        if t in self.files:
            return t
        last = t.split('/')[-1]
        hits = self.by_name.get((last if '.' in last else last + '.md').lower(), [])
        return hits[0] if len(hits) == 1 else None

    def folder_layer(self, path):
        if path in SYSTEM_FILES or path.startswith(('_system/', 'raw/', 'assets/')):
            return 'auxiliary'
        return 'learning' if path.startswith('Learning/') else 'backbone' if path.startswith('Backbone/') else 'auxiliary'

    def note_at(self, link):
        r = self.resolve(link)
        return self.notes.get(r) if r else None

    def check(self, baseline, layout):
        ids, titles = {}, collections.defaultdict(list)
        for n in self.notes.values():
            fm, folder = n['fm'], self.folder_layer(n['path'])
            declared = fm.get('layer')
            n['layer'] = declared if declared in ('backbone', 'learning', 'auxiliary') and folder != 'auxiliary' else folder
            if folder != 'auxiliary':
                if not declared:
                    self.add('error', 'L1', f'missing layer property (folder says {folder}): {n["path"]}')
                elif declared != folder:
                    self.add('error', 'L1', f'layer "{declared}" but the file is in the {folder} folder: {n["path"]}')
                if not fm.get('id'):
                    self.add('error', 'B1', f'missing id: {n["path"]}')
            if fm.get('id'):
                if fm['id'] in ids:
                    self.add('error', 'B1', f'id {fm["id"]} used by {ids[fm["id"]]["path"]} and {n["path"]}')
                ids[fm['id']] = n
            if n['layer'] in ('backbone', 'learning'):
                titles[str(fm.get('title') or n['stem']).casefold()].append(n['path'])
            if ILLEGAL.search(n['stem']):
                self.add('error', 'F4', f'illegal character in file name: {n["path"]}')
        for t, ps in titles.items():
            if len(ps) > 1:
                self.add('warning', 'W2', f'"{t}" is the title of {len(ps)} pages; their file names keep them apart')
        for name, ps in self.by_name.items():
            if name.endswith('.md') and len(ps) > 1:
                self.add('error', 'B7', f'{name} exists {len(ps)} times, so [[{name[:-3]}]] is ambiguous: {ps}')

        bb = {p: n for p, n in self.notes.items() if n['layer'] == 'backbone'}
        ln = {p: n for p, n in self.notes.items() if n['layer'] == 'learning'}

        # Backbone tree
        def parent_of(n):
            return self.note_at(n['fm'].get('parent', ''))
        for n in bb.values():
            fm, lvl = n['fm'], n['fm'].get('level')
            if not isinstance(lvl, int) or not 1 <= lvl <= 5:
                self.add('error', 'B2', f'level must be 1-5, got {lvl!r}: {n["path"]}')
                continue
            par = parent_of(n)
            if lvl == 1 and fm.get('parent'):
                self.add('error', 'B3', f'level-1 page has a parent: {n["path"]}')
            if lvl > 1:
                if not par or par['layer'] != 'backbone':
                    self.add('error', 'B3', f'parent missing or not a backbone page ({fm.get("parent")}): {n["path"]}')
                elif par['fm'].get('level') != lvl - 1:
                    self.add('error', 'B3', f'level {lvl} page under a level {par["fm"].get("level")} parent: {n["path"]}')
            chain, cur, seen = [], n, set()
            while cur and cur['path'] not in seen:
                seen.add(cur['path'])
                chain.insert(0, cur)
                cur = parent_of(cur) if cur['fm'].get('level') != 1 else None
            if cur:
                self.add('error', 'B4', f'parent cycle through {n["path"]}')
            n['chain'] = ' → '.join(str(c['fm'].get('title') or c['stem']) for c in chain)
            root = chain[0]['fm']
            if root.get('level') == 1:
                if fm.get('backbone_path') != n['chain']:
                    self.add('error', 'B6', f'backbone_path should be "{n["chain"]}": {n["path"]}')
                if fm.get('subject') != root.get('id'):
                    self.add('error', 'B5', f'subject "{fm.get("subject")}" but the root is "{root.get("id")}": {n["path"]}')
            if fm.get('connections'):
                self.add('error', 'C4', f'backbone page uses untyped connections: {n["path"]}')
            if len(re.findall(r'^```atlas\s*$', n['body'], re.M)) != 1:
                self.add('error', 'B9', f'needs exactly one ```atlas block: {n["path"]}')

        # Learning notes
        for n in ln.values():
            fm = n['fm']
            homes = as_list(fm.get('primary_home'))
            home = self.note_at(homes[0]) if len(homes) == 1 else None
            if len(homes) != 1:
                self.add('error', 'L2', f'needs exactly one primary_home, has {len(homes)}: {n["path"]}')
            elif not home or home['layer'] != 'backbone':
                self.add('error', 'L2', f'primary_home must be a backbone page ({homes[0]}): {n["path"]}')
            types = as_list(fm.get('note_types'))
            if not types or set(types) - NOTE_TYPES:
                self.add('error', 'L3', f'note_types {types} must be from {sorted(NOTE_TYPES)}: {n["path"]}')
            roles = as_list(fm.get('question_roles'))
            if set(roles) - QUESTION_ROLES:
                self.add('error', 'L3', f'question_roles {roles} must be from {sorted(QUESTION_ROLES)}: {n["path"]}')
            if home and home.get('chain') and fm.get('backbone_path') and fm['backbone_path'] != home['chain']:
                self.add('error', 'L4', f'backbone_path should be the home path "{home["chain"]}": {n["path"]}')

        # Deliberate connections: resolve, carry a reason, respect the leaves-only rule
        for n in list(bb.values()) + list(ln.values()):
            props = LINK_TYPES if n['layer'] == 'backbone' else {'connections': 'connection'}
            reasons = {self.resolve(m.group(1)) for m in map(REASON_RE.match, n['body'].splitlines()) if m}
            for prop in props:
                for link in as_list(n['fm'].get(prop)):
                    r = self.resolve(link)
                    if not r:
                        self.add('error', 'C1', f'{prop} target not found ({clean(link)}): {n["path"]}')
                        continue
                    if r == n['path']:
                        self.add('error', 'C3', f'links to itself: {n["path"]}')
                    if n['layer'] == 'backbone' and self.notes.get(r, {}).get('layer') == 'learning':
                        self.add('error', 'C5', f'backbone page links to a learning note ({r}) in {prop}: {n["path"]}')
                    if r not in reasons:
                        self.add('error', 'C2', f'{prop} → {r.rsplit("/", 1)[-1][:-3]} has no "- [[...]] — reason" line: {n["path"]}')

        # Every link and embed, in properties and body
        for n in self.notes.values():
            if n['path'].startswith(SKIP_LINK_CHECK):
                continue
            body = re.sub(r'`[^`\n]+`', '', re.sub(r'```[\s\S]*?```', '', n['body']))
            links = [m.group(1) for m in LINK_RE.finditer(body)]
            for v in n['fm'].values():
                links += [x for x in as_list(v) if isinstance(x, str) and x.strip().startswith('[[')]
            for link in dict.fromkeys(clean(x) for x in links):
                if not link:
                    continue
                target = self.resolve(link)
                if not target:
                    self.add('error', 'F1', f'[[{link}]] not found: {n["path"]}')
                elif n['layer'] == 'backbone' and self.notes.get(target, {}).get('layer') == 'learning':
                    self.add('error', 'C5', f'backbone page links to a learning note ({target}) in its text: {n["path"]}')

        # Map positions and differences from the frozen baseline (never errors)
        positions = layout.get('positions', {})
        original = {x['id']: x for x in baseline['nodes']}
        live = {n['fm'].get('id'): n for n in bb.values() if n['fm'].get('id')}
        for i, n in live.items():
            title = n['fm'].get('title') or n['stem']
            if i not in positions:
                self.add('warning', 'W1', f'new backbone node "{title}" has no saved map position: {n["path"]}')
            if i not in original:
                self.add('change', 'added node', f'L{n["fm"].get("level")} {title} under {clean(n["fm"].get("parent", "")).rsplit("/", 1)[-1]}')
            elif str(title) != original[i]['label']:
                self.add('change', 'retitled', f'{original[i]["label"]} → {title}')
            elif original[i].get('parent') and live.get(original[i]['parent']) is not parent_of(n):
                self.add('change', 'moved', f'{title} has a new parent')
        for i in original:
            if i not in live:
                self.add('change', 'removed node', original[i]['label'])
        base_links = {(e['source'], e['target'], e['type']) for e in baseline['edges'] if e['type'] != 'contains'}
        live_links = set()
        for n in bb.values():
            for prop, kind in LINK_TYPES.items():
                for link in as_list(n['fm'].get(prop)):
                    t = self.note_at(link)
                    if t and t['fm'].get('id'):
                        live_links.add((n['fm'].get('id'), t['fm']['id'], kind))
        for s, t, k in sorted(live_links - base_links):
            self.add('change', 'added link', f'{k}: {s} → {t}')
        for s, t, k in sorted(base_links - live_links):
            if s in live and t in live:
                self.add('change', 'removed link', f'{k}: {s} → {t}')
        self.counts = {'backbone': len(bb), 'learning': len(ln),
                       'levels': dict(sorted(collections.Counter(n['fm'].get('level') for n in bb.values()).items()))}


def run(vault, display_root=None):
    absolute = os.path.abspath(vault)
    root = pathlib.Path('\\\\?\\' + absolute) if os.name == 'nt' else pathlib.Path(absolute)   # long-path safe on Windows
    v = Vault(root, (display_root or absolute).rstrip('/\\'))
    v.load()
    baseline = json.loads((root / '_system/baseline/statistics-backbone.json').read_text(encoding='utf-8'))
    layout = json.loads((root / '_system/layout.json').read_text(encoding='utf-8'))
    v.check(baseline, layout)
    v.baseline, v.layout = baseline, layout
    return v


def main(argv=None):
    if hasattr(sys.stdout, 'reconfigure'):  # titles contain → etc.; a piped Windows console defaults to cp1252
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('vault')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--export', help='write records + baseline + layout for test-model.cjs')
    ap.add_argument('--display-root', help='real vault root, for the path-length rule when checking a copy')
    a = ap.parse_args(argv)
    v = run(a.vault, a.display_root)
    status = 'fail' if v.out['error'] else 'pass'
    if a.export:
        records = [{'path': n['path'], 'frontmatter': n['fm'], 'body': n['body']} for n in v.notes.values()]
        # Match the plugin's source records so image/PDF links resolve in model tests.
        records += [{'path': path, 'frontmatter': {'layer': 'auxiliary', 'role': 'source'}, 'body': ''}
                    for path in sorted(v.files - v.notes.keys())
                    if path.startswith(('raw/', 'assets/')) or
                    (path.startswith('_system/Migrations/') and path.endswith('.json'))]
        pathlib.Path(a.export).write_text(json.dumps({'records': records, 'baseline': v.baseline, 'layout': v.layout},
                                                     ensure_ascii=False, default=str), encoding='utf-8')
    if a.json:
        print(json.dumps({'status': status, 'counts': v.counts,
                          **{sev: [{'rule': r, 'message': m} for r, m in items] for sev, items in v.out.items()}},
                         ensure_ascii=False))
    else:
        c = v.counts
        print(f'{c["backbone"]} backbone pages · {c["learning"]} learning notes · levels {c["levels"]}')
        for sev in ('error', 'warning', 'change'):
            groups = collections.defaultdict(list)
            for r, m in v.out[sev]:
                groups[r].append(m)
            for r, ms in groups.items():
                label = f'{r} {RULES[r]}' if r in RULES else r
                print(f'{sev.upper():8} {label}: {len(ms)}')
                for m in ms[:5]:
                    print(f'           - {m}')
                if len(ms) > 5:
                    print(f'           … {len(ms) - 5} more')
        print('RESULT', status.upper())
    return 1 if status == 'fail' else 0


if __name__ == '__main__':
    sys.exit(main())
