"""Wrap provenance sections in collapsed callouts, retaining headings and source bytes.

Scans authored Markdown only; never edits raw/, frozen baseline, or hidden folders.
--apply requires an external backup directory. Without it, reports pending changes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
TITLES = {
    'origin', 'origins', 'provenance', 'origin and provenance',
    'sources and provenance', 'source notes and checks',
    'sources and access', 'source coverage', 'preserved original bytes',
}
MARKER = '> [!info]- Source details'


def transform(text):
    lines = text.splitlines(keepends=True)
    headings, fence = [], None
    for i, line in enumerate(lines):
        stripped = line.strip()
        f = re.match(r'^(`{3,}|~{3,})', stripped)
        if f:
            token = f[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence:
            continue
        h = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if h:
            headings.append((i, len(h[1]), h[2].casefold()))
    changed = []
    for j in range(len(headings) - 1, -1, -1):
        start, level, title = headings[j]
        if level == 1 or title not in TITLES:
            continue
        end = next((idx for idx, lev, _ in headings[j + 1:] if lev <= level), len(lines))
        first, last = start + 1, end
        while first < last and not lines[first].strip():
            first += 1
        while last > first and not lines[last - 1].strip():
            last -= 1
        if first == last or lines[first].strip() == MARKER:
            continue
        nl = '\r\n' if lines[start].endswith('\r\n') else '\n'
        original = lines[first:last]
        quoted = [('> ' + line if line.strip() else '>' + line) for line in original]
        # This reversibility assertion catches accidental changes to the source prose.
        assert [line[2:] if line.startswith('> ') else line[1:] for line in quoted] == original
        lines[first:last] = [MARKER + nl] + quoted
        changed.append(title)
    return ''.join(lines), changed


def notes():
    for path in ROOT.rglob('*.md'):
        rel = path.relative_to(ROOT)
        if any(part.startswith('.') for part in rel.parts):
            continue
        if rel.parts[0] == 'raw' or rel.parts[:2] == ('_system', 'baseline'):
            continue
        yield path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--backup', type=Path)
    args = parser.parse_args()
    if args.apply and (not args.backup or not args.backup.is_absolute() or args.backup.is_relative_to(ROOT)):
        parser.error('--apply needs an absolute backup directory outside the vault')
    report, scanned = [], 0
    for path in notes():
        scanned += 1
        before = path.read_bytes()
        text = before.decode('utf-8')
        after, sections = transform(text)
        if not sections:
            continue
        encoded = after.encode('utf-8')
        # The actual YAML frontmatter must stay byte-for-byte unchanged.
        fm = re.match(r'\A(?:\ufeff)?---\r?\n[\s\S]*?\r?\n---(?:\r?\n|$)', text)
        if fm:
            assert after.startswith(fm[0])
        rel = path.relative_to(ROOT)
        report.append({'path': rel.as_posix(), 'sections': sections,
                       'before_sha256': hashlib.sha256(before).hexdigest(),
                       'after_sha256': hashlib.sha256(encoded).hexdigest()})
        if args.apply:
            backup = args.backup / rel
            backup.parent.mkdir(parents=True, exist_ok=True)
            if backup.exists():
                raise RuntimeError(f'Refusing to overwrite backup: {backup}')
            backup.write_bytes(before)
            if path.read_bytes() != before:
                raise RuntimeError(f'Concurrent edit detected: {path}')
            path.write_bytes(encoded)
    result = {'scanned': scanned, 'changed_notes': len(report),
              'sections': sum(len(x['sections']) for x in report), 'changes': report}
    if args.apply:
        (args.backup / 'manifest.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
