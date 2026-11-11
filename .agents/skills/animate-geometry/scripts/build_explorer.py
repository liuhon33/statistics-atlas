"""Pack authored local CSS/JS/body fragments into an offline Obsidian explorer.

Uses only Python's standard library. Refuses to replace a manually changed output.
"""
from pathlib import Path
import argparse
import hashlib
import html
import json
import re

CSP = ("default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; "
       "img-src data:; connect-src 'none'; base-uri 'none'; form-action 'none'")
RESIZE = r"""
(()=>{
  let lastHeight=-1;
  const report=()=>{
    const height=Math.ceil(document.body.getBoundingClientRect().height);
    if(height>0 && height!==lastHeight){
      lastHeight=height;
      if(window.parent!==window)window.parent.postMessage({type:'atlas-interactive-ready',height},'*');
    }
  };
  // ResizeObserver already batches layout changes. Offscreen iframes may suspend
  // animation frames, so do not route either startup or later reports through rAF.
  new ResizeObserver(report).observe(document.body);
  window.addEventListener('load',report);report();
})();
"""


def sha(data):
    return hashlib.sha256(data).hexdigest()


def compile_html(title, body, css, scripts):
    """Return a standalone page; inputs are trusted, agent-authored local source."""
    styles = '\n'.join(css)
    js = '\n;\n'.join(scripts + [RESIZE])
    if re.search(r'</style\b', styles, re.I) or re.search(r'</script\b', js, re.I):
        raise ValueError('An input contains an HTML closing tag; express that literal without closing its inline element.')
    return (f'<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<meta http-equiv="Content-Security-Policy" content="{html.escape(CSP, quote=True)}">'
            f'<title>{html.escape(title)}</title><style>{styles}</style></head>'
            f'<body>{body}<script>{js}</script></body></html>\n')


def write_artifact(output, content, inputs=(), replace=False):
    output = Path(output).resolve()
    if output.suffix.lower() != '.html' or 'raw' in (part.lower() for part in output.parts):
        raise ValueError('Write a generated .html file outside raw/.')
    manifest = output.with_suffix('.build.json')
    encoded = content.encode('utf-8')
    if output.exists() and output.read_bytes() != encoded and not replace:
        previous = json.loads(manifest.read_text(encoding='utf-8')) if manifest.exists() else {}
        if previous.get('output_sha256') != sha(output.read_bytes()):
            raise FileExistsError(f'{output} was changed or has no build manifest. Review it before --replace.')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(encoded)
    record = {'output': output.name, 'output_sha256': sha(encoded),
              'inputs': [{'name': Path(p).name, 'sha256': sha(Path(p).read_bytes())} for p in inputs]}
    manifest.write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--title', required=True)
    parser.add_argument('--body', type=Path, required=True)
    parser.add_argument('--css', type=Path, action='append', default=[])
    parser.add_argument('--js', type=Path, action='append', default=[])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--replace', action='store_true', help='Replace an inspected generated output despite a changed hash.')
    args = parser.parse_args()
    read = lambda p: p.read_text(encoding='utf-8')
    content = compile_html(args.title, read(args.body), list(map(read, args.css)), list(map(read, args.js)))
    record = write_artifact(args.output, content, [args.body, *args.css, *args.js], args.replace)
    print(json.dumps({'output': str(args.output), 'sha256': record['output_sha256']}))


if __name__ == '__main__':
    main()
