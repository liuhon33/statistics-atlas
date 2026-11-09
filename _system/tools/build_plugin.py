"""Bundle the statistics-atlas plugin: core.js + ui.js + plugin.js -> .obsidian/plugins/statistics-atlas/main.js.

Same concatenation Codex documented in _system/Map implementation.md (files joined by one newline).
Use --check to fail if the installed bundle has drifted from the sources. Added by Claude, 2026-11-08.
"""
import pathlib, shutil, sys

root = pathlib.Path(__file__).resolve().parents[2]
src = root / '_system/plugin-src'
dest = root / '.obsidian/plugins/statistics-atlas'
bundle = b'\n'.join((src / f'{name}.js').read_bytes() for name in ('core', 'ui', 'plugin'))
if '--check' in sys.argv:
    ok = (dest / 'main.js').read_bytes() == bundle and (dest / 'styles.css').read_bytes() == (src / 'styles.css').read_bytes()
    print('bundle up to date' if ok else 'bundle differs from _system/plugin-src'); sys.exit(not ok)
(dest / 'main.js').write_bytes(bundle)
shutil.copyfile(src / 'styles.css', dest / 'styles.css')
print(f'wrote {dest / "main.js"} ({len(bundle)} bytes)')
