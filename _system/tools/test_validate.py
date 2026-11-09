"""Regression test for validate.py (Claude, 2026-11-08, AGENTS A3; see _system/Claude/Validator.md).

Copies the vault to a temporary folder outside the vault once per case, applies one realistic change,
runs the validator and checks the exact set of error rules it reports. Valid changes must pass;
broken ones must fail for the right reason. No fixture is ever written into the live vault (AGENTS §11).

Usage: python _system/tools/test_validate.py [vault]     (default: this vault)
"""
import os, pathlib, shutil, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate  # noqa: E402

LONG = (lambda p: '\\\\?\\' + os.path.abspath(p)) if os.name == 'nt' else (lambda p: os.path.abspath(p))


def main():
    vault = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parents[1]).resolve()
    live = validate.run(vault)
    if live.out['error']:
        raise AssertionError('The starting vault must pass validation before fixture checks.')
    baseline_findings = {severity: set(items) for severity, items in live.out.items()}
    by_id = {n['fm'].get('id'): n for n in live.notes.values() if n['fm'].get('id')}
    page = lambda i: by_id[i]['path'][:-3]                      # vault path without .md
    chain = lambda i: by_id[i]['chain']
    vi, elbo, kl, jensen, imp, pp = page('variational'), page('elbo'), page('kl'), page('jensen'), page('importance'), page('posterior-prior-and-posterior')
    folder = elbo.rsplit('/', 1)[0]
    l3 = live.note_at(by_id['variational']['fm']['parent'])     # level-3 grandparent of the ELBO page
    note_path = 'Learning/Statistical computing & learning/Simulation & approximate inference/My four approaches to the ELBO'

    def note(homes=(elbo,), layer=True, reasons=True, types=('derivation',), embed=None):
        fm = ['---', 'id: test-elbo-four-approaches', 'title: My four approaches to the ELBO']
        if layer: fm.append('layer: learning')
        if len(homes) == 1: fm.append(f"primary_home: '[[{homes[0]}]]'")
        elif homes: fm += ['primary_home:'] + [f"- '[[{h}]]'" for h in homes]
        fm += ['note_types:'] + [f'- {t}' for t in types]
        fm += ['question_roles:', '- reconcile-approaches', f'backbone_path: {chain("elbo")}',
               'connections:', f"- '[[{jensen}]]'", f"- '[[{kl}]]'", f"- '[[{imp}]]'", '---', '',
               '# My four approaches to the ELBO', '', 'Four routes to the same lower bound on log p(x).', '']
        if embed: fm += [f'![[{embed}]]', '']
        fm += ['## Connections', '']
        why = [' — route 1: concavity of log', ' — route 2: log p(x) = ELBO + KL(q || p(z|x))', ' — route 4: importance weights'] if reasons else ['', '', '']
        fm += [f'- [[{t}|{t.rsplit("/", 1)[-1]}]]{w}' for t, w in zip((jensen, kl, imp), why)]
        return '\n'.join(fm) + '\n'

    def backbone(title, parent, level, path_text):
        return '\n'.join(['---', f'id: test-{title.lower().replace(" ", "-")}', f'title: {title}', 'layer: backbone',
                          f'level: {level}', 'subject: computing', 'study_band: M', f'backbone_path: {path_text}',
                          f"parent: '[[{parent}]]'", '---', '', f'# {title}', '', path_text, '', '```atlas', '```', ''])

    def write(root, rel, text):
        p = pathlib.Path(LONG(root / rel)); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

    def edit(root, rel, old, new):
        p = pathlib.Path(LONG(root / rel)); t = p.read_text(encoding='utf-8')
        assert old in t, f'fixture setup: {old!r} not found in {rel}'
        p.write_text(t.replace(old, new, 1), encoding='utf-8')

    long_title = 'Pathwise gradient estimators for reparameterizable continuous latent-variable models in amortized inference'
    cases = [
        # (name, change, expected error rules, expected warning rules, expected change kinds)
        ('vault as it is', lambda r: None, set(), None, None),
        ('add a valid learning note', lambda r: write(r, note_path + '.md', note()), set(), None, None),
        ('add a backbone node', lambda r: write(r, f'{folder}/Reparameterization trick.md',
            backbone('Reparameterization trick', vi, 5, chain('variational') + ' → Reparameterization trick')), set(), {'W1'}, {'added node'}),
        ('add a typed cross-link', lambda r: (
            edit(r, kl + '.md', '\nsources:', f"\n- '[[{pp}]]'\nsources:"),
            edit(r, kl + '.md', '\n```atlas', f'\n- [[{pp}|Prior and posterior]] — data fit minus KL from the prior\n\n```atlas')), set(), None, {'added link'}),
        ('retitle with alias', lambda r: [edit(r, page('variational-posterior-kl-gap') + '.md', a, b) for a, b in (
            ('title: Posterior KL gap', 'title: KL gap to the posterior'), ('aliases: []', 'aliases:\n- Posterior KL gap'),
            ('→ Posterior KL gap', '→ KL gap to the posterior'))], set(), None, {'retitled'}),
        ('duplicate property key', lambda r: (
            edit(r, kl + '.md', '\nsources:', f"\nrelated:\n- '[[{pp}]]'\nsources:"),
            edit(r, kl + '.md', '\n```atlas', f'\n- [[{pp}|Prior and posterior]] — data fit minus KL from the prior\n\n```atlas')), {'F0'}, None, {'added link', 'removed link'}),   # report shows the dropped link
        ('two primary homes', lambda r: write(r, note_path + '.md', note(homes=(elbo, kl))), {'L2'}, None, None),
        ('no layer, no home', lambda r: write(r, note_path + '.md', note(homes=(), layer=False)), {'L1', 'L2'}, None, None),
        ('connections without reasons', lambda r: write(r, note_path + '.md', note(reasons=False)), {'C2'}, None, None),
        ('unknown note type', lambda r: write(r, note_path + '.md', note(types=('summary',))), {'L3'}, None, None),
        ('aliased link inside a table', lambda r: write(r, note_path + '.md', note() + f'\n| Route | Page |\n|---|---|\n| 1 | [[{jensen}\\|Jensen]] |\n'), set(), None, None),
        ('broken image embed',lambda r: write(r, note_path + '.md', note(embed='raw/assets/missing.png')), {'F1'}, None, None),
        ('backbone links to a learning note', lambda r: (
            write(r, note_path + '.md', note()),
            edit(r, elbo + '.md', '\nsources:', f"\nrelated:\n- '[[{note_path}]]'\nsources:"),
            edit(r, elbo + '.md', '\n```atlas', f'\n- [[{note_path}|My four approaches]] — my derivations\n\n```atlas')), {'C5'}, None, {'added link'}),
        ('L5 node under a level-3 parent', lambda r: write(r, f'{folder}/Misplaced point.md',
            backbone('Misplaced point', l3['path'][:-3], 5, l3['chain'] + ' → Misplaced point')), {'B3'}, {'W1'}, {'added node'}),
        ('path over the Windows limit', lambda r: write(r, f'{folder}/{long_title}.md',
            backbone(long_title, vi, 5, chain('variational') + ' → ' + long_title)), {'F3'}, {'W1'}, {'added node'}),
    ]

    tmp = pathlib.Path(tempfile.mkdtemp(prefix='vault-validate-'))
    failures = 0
    try:
        for name, change, want_err, want_warn, want_chg in cases:
            root = tmp / 'case'
            if os.path.exists(LONG(root)):
                shutil.rmtree(LONG(root))
            shutil.copytree(LONG(vault), LONG(root), ignore=shutil.ignore_patterns('.git', '.obsidian', '.trash', '.claudian', '.claude', '__pycache__'))
            change(root)
            v = validate.run(root, display_root=str(vault))
            got_err = {r for r, _ in v.out['error']}
            # Compare complete findings before reducing to rule names: an existing W1
            # must not hide a new W1 from the synthetic node.
            got_warn = {r for r, _ in set(v.out['warning']) - baseline_findings['warning']}
            got_chg = {r for r, _ in set(v.out['change']) - baseline_findings['change']}
            ok = got_err == want_err and got_warn == (want_warn or set()) and got_chg == (want_chg or set())
            failures += not ok
            print(f'{"ok  " if ok else "FAIL"} {name:36} errors={sorted(got_err) or "-"} warnings={sorted(got_warn) or "-"} changes={sorted(got_chg) or "-"}')
            if not ok:
                print(f'     expected errors={sorted(want_err)} warnings={sorted(want_warn or [])} changes={sorted(want_chg or [])}')
                for r, m in v.out['error'][:6]:
                    print(f'       {r}: {m}')
    finally:
        shutil.rmtree(LONG(tmp), ignore_errors=True)
    print(f'{len(cases) - failures}/{len(cases)} cases passed')
    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())
