"""Contrast and rule test for the Oath & Action tokens.

Run:  python3 -I work/build/tests/tokens/test_token_rules.py [--json PATH] [--css PATH] [--quiet] [--results PATH]
Default inputs: work/build/tokens/tokens.json and work/build/tokens/tokens.css. Exit code 1 on any failure.

What it holds the files to (work/ledger/20261021_Token-Architecture.md and the decisions since):
  A. DTCG 2025.10 shape: names, types, value shapes, aliases that resolve, no cycles, alias types agree.
  B. The locked palette, exact (Master Brief V2 section 3).
  C. The rule for adding a token, conditions 1 to 5 (section 6), for every derived color and tint, with
     the derivation recomputed in OKLab (D1-04) and every stored ratio recomputed.
  D. Tiers (section 2): primitives hold values, semantic tokens point at primitives, component tokens at
     semantic tokens.
     A deprecated token ($deprecated, Rule 26.8) points at its replacement alone, in its own tier and type, with a
     later release named for its removal, and no live token points at it.
  E. Contrast on every surface (section 3): text 4.5:1, large text and graphics 3:1, measured on the
     token's own ground, its other grounds, its keyline and the text set on a band.
  F. Rule 05.3: red never on Prussian, working red names its rank, working red on Newsprint keeps its
     keyline, no red text, no derived red, the hinge divider never red, the rule's text as the ledger has it,
     and no red reaching Prussian through the stylesheet's surface classes.
  G. Chart rules: no party token resolves to Pillar Red or Prussian and every party shares one ink
     (DR-48, DR-58); diverging pair B runs Prussian through a neutral midpoint to Verdigris with no red
     (DR-54); chart red only through data.emphasisRed; scales keep their order; fills under 3:1 print values.
  H. Type: the 13 px floor with no exceptions, rem sizes, the 13 px label at 6% tracking, the ask label at
     19 px bold (T-7, T-9).
  I. Opacity has two decorative jobs; colors are never transparent; motion keeps V5's timings, every
     duration falls to 0 ms under reduced motion and the loading mark never moves (T-10).
  J. Icons and tiles: a red accent only from 24 px (R10), the app icon and avatar on Charcoal (R13).
  K. Version: SemVer from 6.0.0 (T-11).
  L. Themes (DR-204): in the stylesheet's light and dark theme blocks, every short name resolves through its
     var() chain to the theme surface's own token, and every role passes the contrast its kind needs on the
     theme's ground (or on the ground its token names): text 4.5:1, large text, graphics and focus 3:1, the text
     set on a band 4.5:1. The theme's ink passes 4.5:1 on its ground. A version rise carries a change note.

The color math is this folder's own (token_test_lib.py), shared with no generator code.
"""

import argparse
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True       # loading the sibling modules leaves no cache folder
HERE = pathlib.Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('token_test_lib', HERE / 'token_test_lib.py')
L = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(L)

THRESH = {'text': 4.5, 'largeText': 3.0, 'graphic': 3.0, 'focus': 3.0}
KINDS = {'text', 'largeText', 'graphic', 'focus', 'decorative', 'dataFill', 'background', 'logotype', 'surface'}
TYPES = {'color', 'dimension', 'fontFamily', 'fontWeight', 'duration', 'cubicBezier', 'number', 'typography'}
FLOOR_PX = 13
RED = L.LOCKED['pillarRed']
PRUSSIAN = L.LOCKED['prussian']
V5_DURATIONS = {'fast': 120, 'standard': 200, 'slow': 320, 'stagger': 40}
SEMVER = re.compile(r'^(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?$')
NAME_BAD = re.compile(r'[{}.]|^\$')


def is_red(h):
    return isinstance(h, str) and h.upper() == RED


def close(a, b, tol=0.005):
    return a is not None and b is not None and abs(a - round(b, 2)) <= tol


# --- A. DTCG shape -------------------------------------------------------------------------------------
def shape_errors(p, t, toks):
    out = []
    typ, v = t.get('$type'), t['$value']
    if typ not in TYPES:
        out.append(f'{p}: $type {typ!r} is not a DTCG 2025.10 type this file may use')
        return out
    tgt = L.alias_target(v)
    if tgt:
        if tgt not in toks:
            out.append(f'{p}: broken alias, {{{tgt}}} names no token')
        elif L.resolved_type(tgt, toks) != typ:
            out.append(f'{p}: a {typ} token aliases a {L.resolved_type(tgt, toks)} token')
        return out
    bad = lambda why: out.append(f'{p}: {typ} value {json.dumps(v)[:80]} {why}')
    if typ == 'color':
        if not isinstance(v, dict) or v.get('colorSpace') != 'srgb' or not isinstance(v.get('components'), list) \
                or len(v['components']) != 3 or not re.fullmatch(r'#[0-9A-Fa-f]{6}', v.get('hex', '')):
            bad('is not an sRGB color object with three components and a six-digit hex')
        else:
            if any(not (0 <= c <= 1) for c in v['components']):
                bad('has a component outside 0 to 1')
            if [round(c * 255) for c in v['components']] != [round(c * 255) for c in L.rgb(v['hex'])]:
                bad('has components that do not match its hex')
            if v.get('alpha', 1) != 1:
                out.append(f'{p}: a color token is never transparent; opacity has named jobs of its own')
    elif typ in ('dimension', 'duration'):
        units = {'dimension': ('px', 'rem'), 'duration': ('ms', 's')}[typ]
        if not isinstance(v, dict) or set(v) != {'value', 'unit'} or not isinstance(v['value'], (int, float)) or v['unit'] not in units:
            bad(f'must be {{value, unit}} with unit {" or ".join(units)}')
    elif typ == 'number':
        if not isinstance(v, (int, float)) or isinstance(v, bool):
            bad('must be a JSON number')
    elif typ == 'fontWeight':
        if not isinstance(v, (int, float)) or not 1 <= v <= 1000:
            bad('must be a number from 1 to 1000')
    elif typ == 'fontFamily':
        if not (isinstance(v, str) or (isinstance(v, list) and v and all(isinstance(x, str) for x in v))):
            bad('must be a font name or a list of names')
    elif typ == 'cubicBezier':
        if not isinstance(v, list) or len(v) != 4 or not all(isinstance(x, (int, float)) for x in v) or not (0 <= v[0] <= 1 and 0 <= v[2] <= 1):
            bad('must be four numbers with x coordinates from 0 to 1')
    elif typ == 'typography':
        keys = {'fontFamily', 'fontSize', 'fontWeight', 'letterSpacing', 'lineHeight'}
        if not isinstance(v, dict) or set(v) != keys:
            bad(f'must hold exactly {sorted(keys)}')
        else:
            sub = {'fontFamily': 'fontFamily', 'fontSize': 'dimension', 'fontWeight': 'fontWeight', 'letterSpacing': 'dimension', 'lineHeight': 'number'}
            for k, kt in sub.items():
                a = L.alias_target(v[k]) if isinstance(v[k], str) else None
                if a:
                    if a not in toks:
                        out.append(f'{p}: broken alias in {k}, {{{a}}} names no token')
                    elif L.resolved_type(a, toks) != kt:
                        out.append(f'{p}: {k} aliases a {L.resolved_type(a, toks)} token, not {kt}')
                else:
                    out += shape_errors(f'{p}.{k}', {'$type': kt, '$value': v[k]}, toks)
    return out


def check(json_path, css_path=None):
    fails = []
    report = {}
    tree = L.load_json(json_path)
    toks = L.flatten(tree)
    meta = L.root_meta(tree)
    needs = meta.get('needs', {})
    X = {p: L.ext(t) for p, t in toks.items()}

    # --- A. format and structure
    if meta.get('formatVersion') != '2025.10':
        fails.append('root: formatVersion must record DTCG 2025.10')
    names = {}
    for p, t in toks.items():
        for seg in p.split('.'):
            if NAME_BAD.search(seg):
                fails.append(f'{p}: name segment "{seg}" breaks the DTCG naming rules')
        n = L.css_name(p)
        if n in names:
            fails.append(f'{p}: CSS name {n} collides with {names[n]}')
        names[n] = p
        if not t.get('$description'):
            fails.append(f'{p}: no $description (condition 5, usage notes)')
        fails += shape_errors(p, t, toks)
        try:
            L.resolve(p, toks)
        except (KeyError, ValueError) as err:
            fails.append(f'{p}: {err}')
    resolvable = {}
    for p in toks:
        try:
            resolvable[p] = L.resolve(p, toks)
        except (KeyError, ValueError):
            pass

    def hex_of(p):
        r = resolvable.get(p)
        return r[1].get('hex') if r and isinstance(r[1], dict) else None

    def ref_hex(ref, where):
        try:
            return L.ref_hex(ref, toks)
        except (KeyError, ValueError, TypeError, AttributeError) as err:
            fails.append(f'{where}: reference {ref} does not resolve ({err})')
            return None

    # every reference inside $extensions resolves
    for p, e in X.items():
        for key in ('ground', 'keyline', 'requiresType', 'fallback', 'minSize', 'edge'):
            if key in e and e[key] is not None:
                a = L.alias_target(e[key])
                if not a or a not in toks:
                    fails.append(f'{p}: {key} {e[key]} names no token')
        for key in ('groundsAlso', 'textOnIt'):
            for ref in e.get(key) or []:
                a = L.alias_target(ref)
                if not a or a not in toks:
                    fails.append(f'{p}: {key} entry {ref} names no token')

    # --- B. locked palette
    pal = {p.split('.')[-1]: t for p, t in toks.items() if p.startswith('oa.color.palette.')}
    if set(pal) != set(L.LOCKED):
        fails.append(f'palette: expected exactly {sorted(L.LOCKED)}, found {sorted(pal)}')
    for k, t in pal.items():
        h = (t['$value'] or {}).get('hex', '') if isinstance(t['$value'], dict) else ''
        if h.upper() != L.LOCKED.get(k, '').upper():
            fails.append(f'oa.color.palette.{k}: {h} differs from the locked value {L.LOCKED.get(k)}')
        if X[f'oa.color.palette.{k}'].get('status') != 'locked':
            fails.append(f'oa.color.palette.{k}: a palette color carries status locked')

    # --- held and rejected values stay unused
    held = {v['hex'].upper(): k for k, v in (meta.get('held') or {}).items() if v.get('hex')}
    for p in toks:
        h = hex_of(p)
        if h and h.upper() in held:
            fails.append(f'{p}: resolves to {h}, the {held[h.upper()]} value the register holds back')

    # --- C. the rule for adding a token, for every derived color and tint
    derived_paths = [p for p in toks if p.startswith('oa.color.derived.') or p.startswith('oa.color.tint.')]
    for p in derived_paths:
        e, t = X[p], toks[p]
        if e.get('need') not in needs:
            fails.append(f'{p}: condition 1, no measured need registered (need={e.get("need")})')
        d = e.get('derivation') or {}
        base = (L.alias_target(d.get('base') or '') or '').split('.')[-1]
        toward = (L.alias_target(d.get('toward') or '') or '').split('.')[-1]
        amt = d.get('amount')
        if d.get('method') != 'color-mix' or d.get('space') != 'oklab' or base not in L.LOCKED \
                or toward not in ('newsprint', 'charcoal') or not isinstance(amt, (int, float)) or not 0 < amt < 1:
            fails.append(f'{p}: condition 2, the derivation must mix one palette color toward Newsprint or Charcoal in OKLab (D1-04)')
        else:
            want = L.mix_oklab(L.LOCKED[base], L.LOCKED[toward], amt)
            have = (t['$value'] or {}).get('hex', '').upper() if isinstance(t['$value'], dict) else ''
            if want != have:
                fails.append(f'{p}: condition 2, {base} {amt:g} toward {toward} gives {want} but the token says {have}')
        job = e.get('job', '')
        if not job or ';' in job or len(job) > 120:
            fails.append(f'{p}: condition 3, one named job in one short sentence')
        kind, h = e.get('kind'), hex_of(p)
        if kind not in KINDS:
            fails.append(f'{p}: kind {kind!r} is not a known job kind')
        if h and kind in THRESH:
            for s in e.get('surfaces') or []:
                c = L.ratio(h, L.LOCKED[s])
                if c < THRESH[kind]:
                    fails.append(f'{p}: condition 4, {c:.2f}:1 on {s} is under {THRESH[kind]}:1')
                if not close((e.get('contrast') or {}).get(s), c):
                    fails.append(f'{p}: stored contrast on {s} ({(e.get("contrast") or {}).get(s)}) is stale; measured {c:.2f}')
        if h and kind == 'background':
            for ref in e.get('textOnIt') or []:
                th = ref_hex(ref, p)
                if th:
                    c = L.ratio(th, h)
                    if c < 4.5:
                        fails.append(f'{p}: condition 4, text {ref} on it measures {c:.2f}:1, under 4.5:1')
                    if not close((e.get('textContrast') or {}).get(L.alias_target(ref)), c):
                        fails.append(f'{p}: stored text contrast for {ref} is stale; measured {c:.2f}')
        if e.get('tier') != 'primitive' or e.get('status') not in ('adopted', 'locked'):
            fails.append(f'{p}: condition 5, registered as a primitive with status adopted (has tier={e.get("tier")}, status={e.get("status")})')
    report['derived'] = len(derived_paths)

    # --- D. tiers
    tier_of = {p: X[p].get('tier') for p in toks}
    # A deprecated token (DTCG's $deprecated) is a renamed token's old name, kept for one release of the second part
    # (section 7, step 5; Rule 26.8): it points at its new name alone, keeps its tier and record, and nothing live
    # builds on it.
    deprecated = {p for p, t in toks.items() if '$deprecated' in t}
    ver_now = SEMVER.match(meta.get('tokenSetVersion', '') or '')
    for p in sorted(deprecated):
        t, d = toks[p], X[p].get('deprecated') or {}
        tgt = L.alias_target(t['$value'])
        if not (isinstance(t['$deprecated'], str) and t['$deprecated'].strip()):
            fails.append(f'{p}: $deprecated says what replaced the token, in words')
        if not tgt or L.alias_target(d.get('replacedBy') or '') != tgt:
            fails.append(f'{p}: a deprecated token points at its replacement, {d.get("replacedBy")}, and nothing else; it holds {t["$value"]}')
        elif tgt in deprecated:
            fails.append(f'{p}: its replacement {tgt} is itself deprecated')
        elif tier_of.get(tgt) != tier_of[p] or L.resolved_type(tgt, toks) != L.resolved_type(p, toks):
            fails.append(f'{p}: a deprecated token keeps the tier and type of {tgt}')
        if tgt and tgt.split('.')[-1] != p.split('.')[-1]:
            fails.append(f'{p}: a renamed token keeps its surface; it points at {tgt}')
        rm = SEMVER.match(str(d.get('removedIn') or ''))
        if not rm or not ver_now or (int(rm.group(1)), int(rm.group(2))) <= (int(ver_now.group(1)), int(ver_now.group(2))):
            fails.append(f'{p}: removedIn {d.get("removedIn")!r} names a later release of the second part than {meta.get("tokenSetVersion")}')
        if not str(t.get('$description', '')).startswith('Deprecated'):
            fails.append(f'{p}: a deprecated token\'s description opens with "Deprecated"')
        if d.get('since') != meta.get('tokenSetVersion') and not any(d.get('since') == n.get('version') for n in meta.get('changeNotes') or []):
            fails.append(f'{p}: the release that deprecated it, {d.get("since")!r}, has no change note')
    for p, t in toks.items():
        a = L.alias_target(t['$value'])
        if a in deprecated and p not in deprecated:
            fails.append(f'{p}: points at the deprecated name {a}; point at its replacement')
    for p, t in toks.items():
        typ = L.resolved_type(p, toks)
        tier = tier_of[p]
        tgt = L.alias_target(t['$value'])
        if p in deprecated:
            continue                     # held above: a deprecated token points at its replacement, in its own tier
        if typ == 'color' and tier not in ('primitive', 'semantic', 'component'):
            fails.append(f'{p}: a color token names its tier')
        if tier == 'primitive' and tgt:
            fails.append(f'{p}: a primitive holds a literal value, not an alias')
        if tier == 'semantic' and typ == 'color':
            if not tgt:
                fails.append(f'{p}: a semantic color points at a primitive; it holds a literal')
            elif tier_of.get(tgt) != 'primitive':
                fails.append(f'{p}: a semantic token must alias a primitive, not {tgt}')
        if tier == 'component':
            if not tgt:
                fails.append(f'{p}: a component token points at a semantic token; it holds a literal')
            elif tier_of.get(tgt) != 'semantic':
                fails.append(f'{p}: a component token must alias a semantic token, not {tgt}')

    # --- E. contrast on every surface
    table = {}
    for p, t in toks.items():
        e = X[p]
        if tier_of[p] != 'semantic' or L.resolved_type(p, toks) != 'color':
            continue
        s = L.surface_of(p, t)
        h = hex_of(p)
        if not s or not h:
            continue
        kind = e.get('kind')
        if kind not in KINDS:
            fails.append(f'{p}: kind {kind!r} is not a known job kind')
            continue
        if e.get('surface') and e['surface'] != L.SURFACE_KEYS.get(p.split('.')[-1], e['surface']):
            fails.append(f'{p}: its surface record ({e["surface"]}) disagrees with its name')
        row = '.'.join(p.split('.')[:-1])
        if p in deprecated:
            row = None                   # measured as any token, and left out of the role table, which its replacement fills
        cell = {'hex': h, 'kind': kind}
        if kind == 'background':
            texts = e.get('textOnIt') or []
            if not texts:
                fails.append(f'{p}: a background names the text it carries (textOnIt)')
            worst = None
            for ref in texts:
                th = ref_hex(ref, p)
                if not th:
                    continue
                c = L.ratio(th, h)
                worst = c if worst is None else min(worst, c)
                if c < 4.5:
                    fails.append(f'{p}: text {ref} on this band measures {c:.2f}:1, under 4.5:1')
                if not close((e.get('textContrast') or {}).get(L.alias_target(ref)), c):
                    fails.append(f'{p}: stored text contrast for {ref} is stale; measured {c:.2f}')
            cell.update(ratio=worst, threshold=4.5, measuredAgainst='text on it')
            if e.get('edge'):
                eh = ref_hex(e['edge'], p)
                if eh:
                    for label, g in (('surface', L.LOCKED[s]), ('ground', h)):
                        ec = L.ratio(eh, g)
                        if ec < 3.0:
                            fails.append(f'{p}: its edge {e["edge"]} measures {ec:.2f}:1 on the {label}, under 3:1')
                        if not close((e.get('edgeContrast') or {}).get('onSurface' if label == 'surface' else 'onGround'), ec):
                            fails.append(f'{p}: stored edge contrast on the {label} is stale; measured {ec:.2f}')
        elif kind in THRESH:
            ground = ref_hex(e['ground'], p) if e.get('ground') else L.LOCKED[s]
            if not ground:
                continue
            c = L.ratio(h, ground)
            need = THRESH[kind]
            cell.update(ratio=c, threshold=need, measuredAgainst=e.get('ground') or s)
            # Gate 2 fix pass (AX-1): a graphic that repeats a state its mark and words already carry, such as the error bar
            # beside the error mark and the word "Error:", is not needed to read the state, so WCAG 1.4.11's 3 to 1 does not
            # bind it, and it takes no keyline; its description must say so
            rep = e.get('repeats') if kind == 'graphic' else None
            if rep:
                cell.update(repeats=rep)
                said = str(t.get('$description', ''))
                dep = (e.get('deprecated') or {}).get('replacedBy')
                if dep:   # a deprecated alias says so through the token that replaces it
                    said += ' ' + str(toks.get(L.alias_target(dep), {}).get('$description', ''))
                if not re.search(r'repeats|no keyline', said):
                    fails.append(f'{p}: it repeats {rep}, and its description does not say so')
            if c < need and not rep:
                kl = e.get('keyline')
                if kind == 'graphic' and kl:
                    kh = ref_hex(kl, p)
                    kc = L.ratio(kh, L.LOCKED[s]) if kh else 0
                    cell.update(keyline=kc)
                    if kc < 3.0:
                        fails.append(f'{p}: keyline {kc:.2f}:1 is under 3:1')
                    if not close(e.get('keylineContrast'), kc):
                        fails.append(f'{p}: stored keyline contrast {e.get("keylineContrast")} is stale; measured {kc:.2f}')
                else:
                    fails.append(f'{p}: {kind} measures {c:.2f}:1 on {e.get("ground") or s}, under {need}:1')
            if not close(e.get('contrast'), c):
                fails.append(f'{p}: stored contrast {e.get("contrast")} is stale; measured {c:.2f}')
            if e.get('threshold') != need:
                fails.append(f'{p}: stored threshold {e.get("threshold")} should be {need}')
            for ref in e.get('groundsAlso') or []:
                gh = ref_hex(ref, p)
                if gh:
                    c2 = L.ratio(h, gh)
                    if c2 < need:
                        fails.append(f'{p}: measures {c2:.2f}:1 on {ref}, under {need}:1')
                    if not close((e.get('contrastAlso') or {}).get(L.alias_target(ref)), c2):
                        fails.append(f'{p}: stored contrast on {ref} is stale; measured {c2:.2f}')
            # large text passes only at its size
            if kind == 'largeText':
                rt = e.get('requiresType')
                a = L.alias_target(rt or '')
                if not a or a not in resolvable:
                    fails.append(f'{p}: large text names the type style that makes it large (requiresType)')
                else:
                    ty = resolvable[a][1]
                    fs = ty['fontSize']
                    px = fs['value'] * (16 if fs['unit'] == 'rem' else 1)
                    wt = ty['fontWeight']
                    wa = L.alias_target(wt) if isinstance(wt, str) else None
                    wt = resolvable[wa][1] if wa in resolvable else wt
                    if not (px >= 24 or (px >= 18.66 and wt >= 700)):
                        fails.append(f'{p}: a large-text pass needs 24 px, or 18.66 px bold; its type is {px:g} px at {wt}')
        else:
            cell.update(ratio=L.ratio(h, L.LOCKED[s]), threshold=None, measuredAgainst=s)
            if kind == 'dataFill' and e.get('valuesPrinted') is not True:
                fails.append(f'{p}: a data fill with no 3:1 duty must print its values beside or on the mark (valuesPrinted)')
        if row:
            table.setdefault(row, {})[s] = cell
    report['table'] = table

    # --- F. Rule 05.3
    precedence_words = {1: 'an error', 2: 'the ask', 3: "the headline's point"}
    for p, t in toks.items():
        if L.resolved_type(p, toks) != 'color':
            continue
        h = hex_of(p)
        e = X[p]
        s = L.surface_of(p, t)
        if not is_red(h):
            continue
        if s == 'prussian' or p.endswith('onPrussian') or (e.get('ground') and ref_hex(e['ground'], p) == PRUSSIAN):
            fails.append(f'{p}: Rule 05.3, red never sits on Prussian')
        if e.get('kind') in ('text', 'largeText'):
            fails.append(f'{p}: Rule 05.3 and T-6, red never sets text')
        if 'hingeDivider' in p:
            fails.append(f'{p}: Rule 05.3, the hinge divider\'s ampersand takes its surface\'s ink, never red')
        if tier_of[p] == 'semantic':
            role = e.get('redRole')
            if role not in ('signature', 'working') or (role == 'working' and e.get('precedence') not in (1, 2, 3)):
                fails.append(f'{p}: Rule 05.3, a red token names its claim: signature, or working red at rank 1 to 3')
            if role == 'signature' and e.get('kind') != 'logotype':
                fails.append(f'{p}: signature red belongs to identity marks (kind logotype)')
            if role == 'working' and s == 'newsprint' and not e.get('repeats'):
                kl = e.get('keyline')
                kh = ref_hex(kl, p) if kl else None
                if not kh or L.ratio(kh, L.LOCKED['newsprint']) < 3.0:
                    fails.append(f'{p}: Rule 05.3, working red on Newsprint (2.96:1) takes its 1 px Charcoal keyline')
            if role == 'working':
                expected = {'state.error': 1, 'action.ask': 2, 'data.emphasisRed': 3}
                for k, rank in expected.items():
                    if f'.{k}.' in p and e.get('precedence') != rank:
                        fails.append(f'{p}: Rule 05.3 ranks {precedence_words[rank]} at {rank}; this token says {e.get("precedence")}')
        if p.startswith('oa.color.tint.') or p.startswith('oa.color.derived.'):
            fails.append(f'{p}: T-6, no derived red')
    # signature red only through the palette color; no derived red ink anywhere
    red_l, red_c, red_h = L.oklch(RED)
    for p in toks:
        h = hex_of(p)
        if not h or is_red(h) or p.startswith('oa.color.palette.'):
            continue
        Lh, Ch, Hh = L.oklch(h)
        if Ch >= 0.08 and L.hue_gap(Hh, red_h) <= 30:
            fails.append(f'{p}: {h} is a second red (chroma {Ch:.3f}, hue {Hh:.0f}°); T-6 allows no derived red')
    # the rule's wording
    rule_text = meta.get('redRule')
    want_rule = ledger_rule()
    if meta.get('redRuleId') != 'Rule 05.3':
        fails.append('root: redRuleId must be Rule 05.3')
    if want_rule is None:
        fails.append('Rule 05.3: could not read D2-01 and DR-66 from work/ledger/*_Decision-Log.md')
    elif rule_text != want_rule:
        fails.append('Rule 05.3: the stored wording differs from D2-01 as amended by DR-66')
    # red reaching Prussian through the stylesheet
    if css_path:
        sheet = L.parse_css(pathlib.Path(css_path).read_text(encoding='utf-8'))
        root = dict(next((d for sel, d in sheet['blocks'] if sel == ':root'), []) or [])
        for sel, decls in sheet['blocks']:
            if sel != '.oa-surface-prussian':
                continue
            for name, value in decls or []:
                if value in (None, 'initial'):
                    continue
                try:
                    v = L.resolve_css(value, root)
                except (KeyError, ValueError):
                    continue
                if v.strip().upper() == RED:
                    fails.append(f'.oa-surface-prussian: {name} resolves to Pillar Red; Rule 05.3, red never sits on Prussian')

    # --- G. chart rules
    party = [p for p in toks if '.party.' in p or X[p].get('partyMark')]
    if not party:
        fails.append('chart: no party token; DR-48 needs one neutral ink for party marks')
    by_surface = {}
    for p in party:
        h = hex_of(p)
        if h and h.upper() in (RED, PRUSSIAN):
            fails.append(f'{p}: a party mark resolves to {"Pillar Red" if is_red(h) else "Prussian"}; DR-48 and DR-58 forbid it')
        if h:
            by_surface.setdefault(L.surface_of(p, toks[p]), set()).add(h.upper())
    for s, hs in by_surface.items():
        if len(hs) > 1:
            fails.append(f'chart: party marks on {s} take {len(hs)} different inks ({", ".join(sorted(hs))}); DR-58 allows no party color pair')
    for p in toks:
        if p.startswith('oa.chart.') and is_red(hex_of(p)):
            ranks = [X[c].get('precedence') for c in L.chain(p, toks) if X[c].get('redRole') == 'working']
            if 3 not in ranks:
                fails.append(f'{p}: chart red comes only through data.emphasisRed at rank 3 (Rule 05.3)')
    scales = {}
    for p, e in X.items():
        if e.get('scale') and isinstance(e.get('step'), int):
            scales.setdefault((e['scale'], L.surface_of(p, toks[p])), {})[e['step']] = p
    for (scale, s), st in scales.items():
        ordered = [st[i] for i in sorted(st)]
        if sorted(st) != list(range(1, len(st) + 1)):
            fails.append(f'chart: {scale} scale on {s} has steps {sorted(st)}, not 1 to {len(st)}')
        hexes = [hex_of(p) for p in ordered]
        if not all(hexes):
            continue
        if scale == 'diverging':
            for p, h in zip(ordered, hexes):
                Lh, Ch, Hh = L.oklch(h)
                if is_red(h) or (Ch >= 0.02 and L.hue_gap(Hh, red_h) <= 45):
                    fails.append(f'{p}: a diverging step is red ({h}); no diverging scale pairs red with blue (Master Brief V2 section 13)')
            if hexes[0].upper() != PRUSSIAN:
                fails.append(f'chart: diverging pair B starts at Prussian (DR-54); step 1 on {s} is {hexes[0]}')
            mid = hexes[len(hexes) // 2]
            if L.oklch(mid)[1] >= 0.02:
                fails.append(f'chart: the diverging midpoint on {s} ({mid}) is not neutral')
            if L.hue_gap(L.oklch(hexes[-1])[2], L.oklch(L.LOCKED['verdigris'])[2]) > 30:
                fails.append(f'chart: diverging pair B ends at Verdigris (DR-54); step {len(hexes)} on {s} is {hexes[-1]}')
            ls = [L.oklab(h)[0] for h in hexes]
            half = len(ls) // 2
            if not (all(a < b for a, b in zip(ls[:half], ls[1:half + 1])) and all(a > b for a, b in zip(ls[half:], ls[half + 1:]))):
                fails.append(f'chart: diverging pair B on {s} must lighten toward the midpoint from both ends')
        else:
            ls = [L.oklab(h)[0] for h in hexes]
            steps_ = [b - a for a, b in zip(ls, ls[1:])]
            want_up = L.LOCKED[s] == L.LOCKED['charcoal'] if s in L.LOCKED else False
            ok = all(d > 0 for d in steps_) if want_up else all(d < 0 for d in steps_)
            if not ok:
                fails.append(f'chart: the {scale} scale on {s} loses its order; the most must read strongest')
            elif min(abs(d) for d in steps_) < 0.05:
                fails.append(f'chart: two {scale} steps on {s} sit {min(abs(d) for d in steps_):.3f} apart in OKLab lightness, under 0.05')

    # --- H. type
    if meta.get('fontSizeExceptions'):
        fails.append('root: T-9 allows no screen exceptions to the 13 px floor')
    for p, t in toks.items():
        if t.get('$type') == 'typography' and isinstance(t['$value'], dict):
            v, e = t['$value'], X[p]
            for label, sz in (('size', v['fontSize']), ('minimum size', e.get('minFontSize'))):
                if not sz:
                    fails.append(f'{p}: no minFontSize record')
                    continue
                if sz['unit'] != 'rem':
                    fails.append(f'{p}: {label} is in {sz["unit"]}; screen type sizes are in rem (T-9)')
                px = sz['value'] * 16 if sz['unit'] == 'rem' else sz['value']
                if px < FLOOR_PX - 1e-9:
                    fails.append(f'{p}: {label} {px:g} px is under the 13 px floor')
        if t.get('$type') == 'dimension' and X[p].get('role') == 'fontSize' and isinstance(t['$value'], dict):
            v = t['$value']
            px = v['value'] * (16 if v['unit'] == 'rem' else 1)
            if px < FLOOR_PX - 1e-9:
                fails.append(f'{p}: chart type at {px:g} px is under the 13 px floor')
    lab = toks.get('oa.type.label')
    if lab:
        v, e = lab['$value'], X['oa.type.label']
        if v['fontSize'] != {'value': 0.8125, 'unit': 'rem'} or e.get('trackingEm') != 0.06 or e.get('textTransform') != 'uppercase':
            fails.append('oa.type.label: T-9 sets labels at 13 px (0.8125 rem) in capitals with 6% tracking')
    else:
        fails.append('oa.type.label: missing')
    for p in ('oa.type.ask',):
        if p not in resolvable:
            fails.append(f'{p}: missing')
    for p, t in toks.items():
        if p.startswith('oa.layout.measure.') and isinstance(t['$value'], dict) and t['$value'].get('unit') != 'rem':
            fails.append(f'{p}: measures are in rem (T-9)')

    # --- I. opacity, transparency, motion
    op = [p for p in toks if p.startswith('oa.opacity.')]
    if len(op) != 2:
        fails.append(f'opacity: T-10 gives opacity two decorative jobs; found {len(op)} tokens')
    for p in op:
        t, e = toks[p], X[p]
        if 'Decoration only' not in t.get('$description', ''):
            fails.append(f'{p}: opacity tokens are decoration only and must say so')
        comp = e.get('composite') or {}
        ink, ground = comp.get('ink'), comp.get('ground')
        if ink and ground and isinstance(t['$value'], (int, float)):
            ih, gh = ref_hex(ink, p), ref_hex(ground, p)
            if ih and gh:
                a = t['$value']
                mixed = '#' + ''.join(f'{round((x * a + y * (1 - a)) * 255):02X}' for x, y in zip(L.rgb(ih), L.rgb(gh)))
                c = L.ratio(mixed, gh)
                if mixed != (comp.get('hex') or '').upper() or not close(comp.get('contrastWithGround'), c):
                    fails.append(f'{p}: stored composite is stale; measured {mixed} at {c:.2f}:1')
                if c >= 1.5:
                    fails.append(f'{p}: a watermark at {c:.2f}:1 could carry meaning; keep it under 1.5:1')
        else:
            fails.append(f'{p}: an opacity token records the composite it makes')
    for name, want in V5_DURATIONS.items():
        t = toks.get(f'oa.motion.duration.{name}')
        if not t or t['$value'] != {'value': want, 'unit': 'ms'}:
            fails.append(f'oa.motion.duration.{name}: V5 sets {want} ms (T-10)')
    for p, t in toks.items():
        if t.get('$type') == 'duration' and X[p].get('reducedMotionValue') != {'value': 0, 'unit': 'ms'}:
            fails.append(f'{p}: under prefers-reduced-motion every duration resolves to 0 ms')
    for p in toks:
        if p.startswith('oa.color.state.loading.mark.') and X[p].get('motion') != 'none':
            fails.append(f'{p}: the loading state is still (T-10)')

    # --- J. icons and tiles
    small = toks.get('oa.size.icon.small')
    if not small or small['$value'] != {'value': 16, 'unit': 'px'} or X['oa.size.icon.small'].get('oneColor') is not True:
        fails.append('oa.size.icon.small: R10 sets 16 px icons in one color')
    for p in toks:
        if p.startswith('oa.component.icon.accent.'):
            ms = X[p].get('minSize')
            a = L.alias_target(ms or '')
            v = resolvable.get(a, (None, None))[1] if a else None
            if not v or v.get('unit') != 'px' or v.get('value', 0) < 24:
                fails.append(f'{p}: R10, a red accent appears only at 24 px and up (minSize)')
    for p in ('oa.component.appIcon.tile', 'oa.component.avatar.tile'):
        if hex_of(p) != L.LOCKED['charcoal']:
            fails.append(f'{p}: R13 makes Charcoal the default tile')

    # --- K. version
    ver = meta.get('tokenSetVersion', '')
    m = SEMVER.match(ver)
    if not m or (int(m.group(1)), int(m.group(2)), int(m.group(3))) < (6, 0, 0):
        fails.append(f'root: tokenSetVersion {ver!r} is not SemVer from 6.0.0 (T-11)')
    elif m.group(4) and meta.get('status') != 'pre-release':
        fails.append(f'root: version {ver} is a pre-release, so status must say pre-release')

    # --- L. themes (DR-204)
    theme = meta.get('theme') or {}
    report['themes'] = {}
    if not theme:
        fails.append('root: no theme record; DR-204 asks for a light and a dark theme')
    notes = meta.get('changeNotes') or []
    if not notes or notes[0].get('version') != meta.get('tokenSetVersion') or not notes[0].get('change') or not notes[0].get('reason'):
        fails.append(f'root: version {meta.get("tokenSetVersion")} has no change note (version, change, reason) at the head of changeNotes (section 7, step 6)')
    if theme and css_path:
        sheet = L.parse_css(pathlib.Path(css_path).read_text(encoding='utf-8'))
        root = dict(next((d for sel, d in sheet['blocks'] if sel == ':root'), []) or [])
        a = theme.get('attribute', 'data-oa-theme')
        want_sel = {'light': f':root:not([{a}="dark"]), [{a}="light"]', 'dark': f'[{a}="dark"]'}
        by_css = {L.css_name(q): q for q in toks}
        norm_sel = lambda x: ', '.join(y.strip() for y in ' '.join(x.split()).split(','))
        for which, sel_want in want_sel.items():
            surf = (theme.get(which) or {}).get('surface')
            block = next((d for sel, d in sheet['blocks'] if norm_sel(sel) == sel_want), None)
            if surf not in L.LOCKED or block is None:
                fails.append(f'{which} theme: no block {sel_want} on a known surface')
                continue
            ground = L.LOCKED[surf]
            decls = dict(block)
            measured = 0
            ink = decls.get('color')
            try:
                ih = L.resolve_css(ink, root).strip().upper() if ink else None
            except (KeyError, ValueError):
                ih = None
            if not ih or L.ratio(ih, ground) < 4.5:
                fails.append(f'{which} theme: its ink {ink} does not pass 4.5:1 on {surf}')
            for name, value in block:
                if not name.startswith('--oa-') or value == 'initial' or name == theme.get('shortSurface'):
                    continue
                m = re.fullmatch(r'var\((--oa-[a-z0-9-]+)\)', value or '')
                q = by_css.get(m.group(1)) if m else None
                if not q:
                    fails.append(f'{which} theme: {name} reads {value}, which names no token')
                    continue
                if L.surface_of(q, toks[q]) != surf:
                    fails.append(f'{which} theme: {name} points at {q}, a token for another surface than {surf}')
                    continue
                # the role's kind and ground come from the first semantic token in its alias chain
                sem = next((c for c in L.chain(q, toks) if X[c].get('tier') == 'semantic'), q)
                e = X[sem]
                kind = e.get('kind')
                h = hex_of(q)
                if not h:
                    continue
                if kind == 'background':
                    for ref in e.get('textOnIt') or []:
                        th = ref_hex(ref, sem)
                        if th and L.ratio(th, h) < 4.5:
                            fails.append(f'{which} theme: {name}, text {ref} on it measures {L.ratio(th, h):.2f}:1, under 4.5:1')
                    measured += 1
                elif kind in THRESH:
                    g = ref_hex(e['ground'], sem) if e.get('ground') else ground
                    c = L.ratio(h, g)
                    if c < THRESH[kind] and not (kind == 'graphic' and e.get('repeats')):
                        kl = e.get('keyline')
                        kc = L.ratio(ref_hex(kl, sem), ground) if kl and kind == 'graphic' else 0
                        if kc < 3.0:
                            fails.append(f'{which} theme: {name} ({kind}) measures {c:.2f}:1 on {surf}, under {THRESH[kind]}:1')
                    measured += 1
            report['themes'][which] = {'surface': surf, 'shortNamesMeasured': measured}
    elif theme:
        fails.append('themes: the rule test needs tokens.css to measure the theme blocks')

    report['tokens'] = len(toks)
    return fails, report


def ledger_rule():
    logs = sorted(L.ROOT.glob('work/ledger/*_Decision-Log.md'))
    if not logs:
        return None
    text = logs[0].read_text(encoding='utf-8')
    d201 = next((ln for ln in text.splitlines() if ln.startswith('| D2-01 |')), None)
    dr66 = next((ln for ln in text.splitlines() if ln.startswith('| DR-66 |')), None)
    if not d201 or not dr66:
        return None
    m1 = re.search(r'word for word: "(.*?)" \|', d201)
    m2 = re.search(r'sentence reads "(.*?)" \|', dr66)
    old = 'In a row or a menu, icons go one color and only the current one keeps its red.'
    if not m1 or not m2 or old not in m1.group(1):
        return None
    return m1.group(1).replace(old, m2.group(1))


NAMES = {**{v.upper(): k[0].upper() + k[1:] for k, v in L.LOCKED.items()}, '#4E535B': 'Deep Stone', '#A3A19C': 'Dim Newsprint',
         '#E1C9C1': 'Error Band'}
NAMES['#E63946'] = 'Pillar Red'


def table_md(table, toks=None):
    lines = ['| Role | Newsprint | White | Charcoal | Prussian |', '|---|---|---|---|---|']
    for row, cells in table.items():
        out = []
        for s in L.SURFACES:
            c = cells.get(s)
            if not c:
                out.append('none')
                continue
            name = NAMES.get(c['hex'].upper(), c['hex'])
            r = f"{c['ratio']:.2f}" if c.get('ratio') is not None else ''
            extra = f", keyline {c['keyline']:.2f}" if c.get('keyline') else ''
            mark = '' if c.get('threshold') is None else f" (needs {c['threshold']:g})"
            out.append(f'{name} {r}{extra}{mark}'.strip())
        lines.append(f'| {row.replace("oa.", "", 1)} | ' + ' | '.join(out) + ' |')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', default=str(L.TOKENS_DIR / 'tokens.json'))
    ap.add_argument('--css', default=str(L.TOKENS_DIR / 'tokens.css'))
    ap.add_argument('--quiet', action='store_true')
    ap.add_argument('--table', action='store_true', help='print the role table by surface')
    a = ap.parse_args()
    fails, report = check(a.json, a.css)
    print(f'rules: {report.get("tokens")} tokens, {report.get("derived")} derived colors and tints, '
          f'{sum(len(v) for v in report.get("table", {}).values())} semantic color cells measured, {len(fails)} failures')
    for f in fails if not a.quiet else fails[:30]:
        print('  FAIL', f)
    if a.table:
        print(table_md(report['table']))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
