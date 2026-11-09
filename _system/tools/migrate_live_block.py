"""Replace the hand-copied "## Topics" and "## Connected from" lists on backbone pages with a live ```atlas``` block.

Claude, 2026-11-08, AGENTS A2. Dry run by default; pass --write to apply.

Safety: a section is removed only if it contains nothing but link items AND its link targets are exactly what the
note properties already say (children via `parent`, incoming links via prerequisite_for / applied_in / related).
Any page that fails this check is left untouched and reported. Idempotent: pages that already have the block are skipped.
"""
import collections, pathlib, re, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from validate import load_yaml  # same frontmatter parser as the validator (PyYAML or its fallback)

root = pathlib.Path(__file__).resolve().parents[2]
write = '--write' in sys.argv
FM = re.compile(r'^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)')
TYPED = ('prerequisite_for', 'applied_in', 'related')
BLOCK = '```atlas\n```\n'


def target(link):
    return str(link).strip().removeprefix('[[').removesuffix(']]').split('|')[0].split('#')[0]


pages = {}
for f in sorted((root / 'Backbone').rglob('*.md')):
    text = f.read_text(encoding='utf-8')
    m = FM.match(text)
    fm = load_yaml(m.group(1)) if m else {}
    if fm.get('layer') == 'backbone':
        pages[f.relative_to(root).with_suffix('').as_posix()] = (f, text, m, fm)

children, inbound = collections.defaultdict(set), collections.defaultdict(set)
for key, (_, _, _, fm) in pages.items():
    if fm.get('parent'):
        children[target(fm['parent'])].add(key)
    for prop in TYPED:
        for link in fm.get(prop) or []:
            inbound[target(link)].add(key)


def cut_section(body, heading, expected, problems):
    """Remove `## heading` + its list if the list is a pure copy of `expected` link targets."""
    lines = body.split('\n')
    try:
        start = lines.index('## ' + heading)
    except ValueError:
        if expected:
            problems.append(f'no "{heading}" section but properties imply {len(expected)} entries (nothing lost)')
        return body
    end = start + 1
    while end < len(lines) and not lines[end].startswith('## ') and not lines[end].startswith('```'):
        end += 1
    section = [l for l in lines[start + 1:end] if l.strip()]
    if not all(l.startswith('- [[') for l in section):
        problems.append(f'"{heading}" contains non-link text; left untouched')
        return None
    listed = {target(re.match(r'- \[\[([^\]]+)\]\]', l).group(1)) for l in section}
    if listed != expected:
        problems.append(f'"{heading}" differs from properties: extra={sorted(listed - expected)} missing={sorted(expected - listed)}')
        return None
    return '\n'.join(lines[:start] + lines[end:])


changed = skipped = 0
failures = []
removed = collections.Counter()
for key, (f, text, m, fm) in pages.items():
    body = text[m.end():]
    if '```atlas' in body:
        skipped += 1
        continue
    problems = []
    new = body
    for heading, expected in (('Topics', children[key]), ('Connected from', inbound[key])):
        had = ('\n## ' + heading + '\n') in ('\n' + new)
        out = cut_section(new, heading, expected, problems)
        if out is None:
            break
        if had:
            removed[heading] += 1
        new = out
    else:
        new = re.sub(r'\n{3,}', '\n\n', new).rstrip('\n') + '\n\n' + BLOCK
        if write:
            f.write_bytes((text[:m.end()] + new).encode('utf-8'))
        changed += 1
        continue
    failures.append((key, problems))

print(f"{'wrote' if write else 'would change'} {changed} pages; skipped {skipped} already migrated; "
      f"removed Topics from {removed['Topics']}, Connected from from {removed['Connected from']}; failures {len(failures)}")
for key, problems in failures:
    print('  FAIL', key, '|', '; '.join(problems))
sys.exit(1 if failures else 0)
