"""One-off migration (Claude, 2026-11-08): move backbone cross-link types into note properties.

Before: backbone pages listed cross-links in an untyped `connections` property, and the
plugin looked up prerequisite/application/connection types in the frozen baseline JSON.
After: each backbone page lists its outgoing cross-links in typed properties.

    prerequisite_for: [...]   # baseline type "prerequisite"  (this page -> target)
    applied_in:       [...]   # baseline type "application"   (this page -> target)
    related:          [...]   # baseline type "connection"    (undirected; listed on the source page)

Only the frontmatter `connections` block of backbone pages is rewritten; link text,
order within a type, body reasons and every other property are left byte-identical.
Run with --check to report without writing. Refuses to run if any link is not a
baseline cross-link, so it cannot invent a type.
"""
import argparse, json, pathlib, re, sys

TYPE_TO_PROP = {'prerequisite': 'prerequisite_for', 'application': 'applied_in', 'connection': 'related'}
ORDER = ['prerequisite_for', 'applied_in', 'related']


def main():
    p = argparse.ArgumentParser(); p.add_argument('vault'); p.add_argument('--check', action='store_true'); a = p.parse_args()
    root = pathlib.Path(a.vault).resolve()
    baseline = json.loads((root / '_system/baseline/statistics-backbone.json').read_text(encoding='utf-8'))
    types = {(e['source'], e['target']): e['type'] for e in baseline['edges'] if e['type'] != 'contains'}
    files = sorted((root / 'Backbone').rglob('*.md'))
    texts = {f: f.read_bytes().decode('utf-8') for f in files}
    ids = {}
    for f, t in texts.items():
        m = re.search(r'^id: (.+)$', t, re.M)
        ids[f.relative_to(root).with_suffix('').as_posix()] = m.group(1).strip().strip("'")
    block = re.compile(r'^connections:(?: \[\])?\r?\n((?:- .*\r?\n)*)', re.M)
    changed, moved, errors, pending = 0, {k: 0 for k in ORDER}, [], {}
    for f, t in texts.items():
        end = t.find('\n---', 3)
        fm, rest = t[:end], t[end:]
        m = block.search(fm)
        if not m:
            errors.append(f'No connections block: {f}'); continue
        nl = '\r\n' if '\r\n' in m.group(0) else '\n'
        nid = ids[f.relative_to(root).with_suffix('').as_posix()]
        groups = {k: [] for k in ORDER}
        for line in m.group(1).splitlines():
            link = re.match(r"- '\[\[([^\]|#]+)", line)
            if not link:
                errors.append(f'Unparsed link line in {f}: {line}'); continue
            tid = ids.get(link.group(1))
            kind = types.get((nid, tid))
            if kind is None:
                errors.append(f'Not a baseline cross-link: {nid} -> {link.group(1)}'); continue
            groups[TYPE_TO_PROP[kind]].append(line); moved[TYPE_TO_PROP[kind]] += 1
        new = ''.join(f'{k}:{nl}' + ''.join(l + nl for l in groups[k]) for k in ORDER if groups[k])
        out = fm[:m.start()] + new + fm[m.end():] + rest
        if out != t:
            changed += 1; pending[f] = out
    if not a.check and not errors:
        for f, out in pending.items():
            f.write_bytes(out.encode('utf-8'))
    print(json.dumps({'backbone_pages': len(files), 'pages_changed': changed, 'links_by_property': moved, 'errors': errors, 'written': not a.check and not errors}, indent=2))
    sys.exit(bool(errors))


if __name__ == '__main__':
    main()
