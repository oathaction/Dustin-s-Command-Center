"""Chapter 18's anatomy plates, s-18-01-anatomy to s-18-24-anatomy (stage C round 1, systems designer, November 11, 2026).

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py           write the plates and their manifest
    python3 -I work/build/scripts/phase-2/stage_c_ch18_anatomy_build.py --check   build in memory and report sizes only

Writes:
    work/build/guide/specimens/s-18-NN-anatomy.html         one fragment per rule 18.1 to 18.24
    work/build/guide/specimens/manifest-anatomy.json        their entries: chapter "18", rule "18.N", alt, notes

Reads, never edits:
    work/build/guide/code/c-18-<name>.html and .css         the component engineer's code sets (DR-203)
    work/build/guide/chapters/18-components.json            each rule's anatomy caption, which names the parts to label

How a plate is drawn. Each plate is the component's own markup, cut to the parts its caption names, with its own CSS,
cut to the rules those parts use. It is a picture, not a live control (AX-S8, the round 1 brief): every button, link,
field, label, summary, dialog and landmark becomes a span or a div, ids and names go, and a state a reader would set by
hand (focus, hover, checked) is set as an attribute the rewritten CSS reads, so the code's own focus ring, hover and
checked look draw. The code's class names are shortened inside the plate to keep chapter 18 inside its weight (D2-1366);
the drawing is the code's. Numbered callouts sit on the parts, a bracket marks the target's height, and a key in words
follows, in one style across the 24 plates. The stage's alt names every callout.
"""
import argparse
import html
import html.parser
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent


def _load(name, path=None):
    spec = importlib.util.spec_from_file_location(name, path or HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


B = _load('stage_a_systems_build')
C = sys.modules['stage_a_systems_core']
ROOT = C.ROOT
CODE = ROOT / 'work/build/guide/code'
CH18 = ROOT / 'work/build/guide/chapters/18-components.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-anatomy.json'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'source', 'track', 'wbr'}
# What each live element becomes in a picture (AX-S8: no landmark; no control a reader could reach)
TAGMAP = {'a': 'span', 'button': 'span', 'input': 'span', 'select': 'span', 'textarea': 'span', 'label': 'span',
          'output': 'span', 'summary': 'div', 'details': 'div', 'dialog': 'div', 'fieldset': 'div', 'legend': 'div',
          'form': 'div', 'nav': 'div', 'header': 'div', 'footer': 'div', 'main': 'div', 'aside': 'div', 'section': 'div',
          'article': 'div', 'search': 'div', 'h1': 'p', 'h2': 'p', 'h3': 'p', 'h4': 'p', 'h5': 'p', 'h6': 'p'}
SVG_CASE = {'viewbox': 'viewBox', 'preserveaspectratio': 'preserveAspectRatio'}


# ------------------------------------------------------------------------------------------------ a small tree
class El:
    def __init__(self, tag, attrs=None):
        self.tag, self.a, self.k, self.up = tag, dict(attrs or {}), [], None

    def cls(self):
        return self.a.get('class', '').split()

    def add_cls(self, c):
        self.a['class'] = ' '.join(self.cls() + [c])


class _P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.root = El('#')
        self.cur = self.root

    def _el(self, t, attrs):
        e = El(t, [(SVG_CASE.get(k, k), v) for k, v in attrs])
        e.up = self.cur
        self.cur.k.append(e)
        return e

    def handle_starttag(self, t, attrs):
        e = self._el(t, attrs)
        if t not in VOID:
            self.cur = e

    def handle_startendtag(self, t, attrs):
        self._el(t, attrs)

    def handle_endtag(self, t):
        n = self.cur
        while n is not self.root and n.tag != t:
            n = n.up
        if n is not self.root:
            self.cur = n.up

    def handle_data(self, d):
        self.cur.k.append(d)

    def handle_entityref(self, name):
        self.cur.k.append(f'&{name};')

    def handle_charref(self, name):
        self.cur.k.append(f'&#{name};')


def parse(text):
    p = _P()
    p.feed(re.sub(r'<!--.*?-->', '', text, flags=re.S))
    return p.root


def ser(e):
    if isinstance(e, str):
        return e
    inner = ''.join(ser(k) for k in e.k)
    if e.tag == '#':
        return inner
    at = ''.join(f' {k}' if v is None else f' {k}="{html.escape(v, quote=True)}"' for k, v in e.a.items())
    if e.tag in VOID:
        return f'<{e.tag}{at}>'
    return f'<{e.tag}{at}>{inner}</{e.tag}>'


def walk(e):
    for k in e.k:
        if isinstance(k, El):
            yield k
            yield from walk(k)


def qa(root, cls):
    return [e for e in walk(root) if cls in e.cls()]


def q(root, cls, i=0):
    found = qa(root, cls)
    if len(found) <= i:
        raise SystemExit(f'anatomy: no element {i} with class {cls}')
    return found[i]


def drop(*els):
    for e in els:
        e.up.k.remove(e)


def only(root, *keep):
    """Keep these elements with their whole subtrees and their ancestors; drop everything else, text included."""
    inside, path = set(), set()
    for e in keep:
        inside.update(id(x) for x in walk(e))
        inside.add(id(e))
        n = e
        while n is not None:
            path.add(id(n))
            n = n.up

    def prune(n):
        out = []
        for k in n.k:
            if isinstance(k, El):
                if id(k) in inside:
                    out.append(k)
                elif id(k) in path:
                    prune(k)
                    out.append(k)
            elif id(n) in inside:
                out.append(k)
        n.k = out
    prune(root)
    return root


def say(e, text):
    """Set an element's words, as the component's script would at that moment."""
    e.k = [html.escape(text, quote=False)]


def pin(e, n, at='tl'):
    """A numbered callout on a part. A block of words takes it in the margin before its first line, so no word is
    covered; a control takes it on a corner."""
    if at == 'tl' and e.tag in ('p', 'legend', 'caption', 'label', 'li'):
        at = 'l'
    e.add_cls('ax-p')
    b = El('span', {'class': 'ax-n' if at == 'tl' else f'ax-n ax-{at}'})
    b.k = [str(n)]
    b.up = e
    e.k.append(b)


def at_word(e, n, at, glue=False):
    """A callout on the first word of a run of words, held in a span that does not wrap, for a link that wraps and so
    has no single corner. glue=True joins the next word with a no-break space, for words inside a flex box, where a
    plain space between two runs collapses."""
    for i, k in enumerate(e.k):
        if isinstance(k, str) and k.strip():
            lead = len(k) - len(k.lstrip())
            word, rest = (k[lead:].split(' ', 1) + [''])[:2]
            w = El('span', {'class': 'ax-nw'})
            w.k = [word]
            w.up = e
            e.k[i:i + 1] = ([k[:lead]] if lead else []) + [w] + ([('\u00a0' if glue else ' ') + rest] if rest else [])
            pin(w, n, at)
            return
    pin(e, n, at)


def bracket(e, n, up=False):
    """A bracket down the target's left edge, with its callout: the height a finger or pointer can hit. up=True sets the
    callout above the bracket, where words sit close before the target."""
    e.add_cls('ax-p')
    t = El('span', {'class': 'ax-t ax-tup' if up else 'ax-t'})
    b = El('span', {'class': 'ax-n'})
    b.k = [str(n)]
    t.k = [b]
    t.up = e
    e.k.append(t)


# ------------------------------------------------------------------------------------------------ picture conversion
def to_picture(root, css_attrs):
    """Every control and landmark becomes a span or div with a class for its old tag; ids, names and links go; a state
    attribute the CSS reads becomes data-ax-*, every other aria and data attribute goes."""
    for e in list(walk(root)):
        t = e.tag
        if t in ('template', 'script'):
            drop(e)
            continue
        a = {}
        for k, v in e.a.items():
            if k == 'class':
                a[k] = v
            elif k in ('hidden',):
                a[k] = v
            elif k in ('checked', 'disabled', 'open'):
                a[f'data-ax-{k}'] = None
            elif k == 'role' or k.startswith('aria-'):
                if k != 'aria-hidden' and k in css_attrs:
                    a[f'data-ax-{k}'] = v
            elif k.startswith('data-ax-'):
                a[k] = v
            elif k.startswith('data-oa-') or k.startswith('data-red'):
                if k in css_attrs:
                    a[k] = v
            elif k in ('data-icon', 'data-icon-family'):
                a[k] = v
            elif t in ('svg', 'path', 'circle', 'rect', 'line', 'polyline', 'polygon', 'g', 'use', 'ellipse'):
                if k not in ('focusable', 'aria-hidden', 'id', 'role'):
                    a[k] = v
            elif t in ('td', 'th', 'col', 'colgroup') and k in ('colspan', 'rowspan'):
                a[k] = v
        icon = e.a.get('data-icon', '') if t == 'svg' else ''
        if icon.startswith('U-'):
            # a utility icon draws from the sprite, as the build asks of every specimen from chapter 09 on; a mirror or a
            # turn on the code's path moves to the <use>
            size = (e.a.get('viewBox') or '0 0 24 24').split()[-1]
            # one <use> for each way the code draws the icon: a turn or mirror, and a class the CSS shows or hides by
            # state (a table heading's up and down arrows)
            ways = []
            for k in walk(e):
                way = (k.a.get('class'), k.a.get('transform'))
                if way not in ways:
                    ways.append(way)
            uses = []
            for cls, move in ways:
                use = El('use', {'href': f'#oa-sym-u-{icon[2:].lower()}-{size}px'})
                if cls:
                    use.a['class'] = cls
                if move:
                    use.a['transform'] = move
                use.up = e
                uses.append(use)
            e.k = uses
            e.a = {k: v for k, v in a.items() if k in ('class', 'viewBox', 'width', 'height', 'hidden', 'data-icon')}
            e.a['data-icon-family'] = 'utility'
            continue
        for stroke, kls in ((UTIL_STROKE, 'ax-u'), (dict(UTIL_STROKE, **{'stroke-width': '1.5'}), 'ax-u16')):
            if t == 'svg' and all(a.get(k) == v for k, v in stroke.items()):
                for k in stroke:
                    a.pop(k)
                a.pop('data-icon-family', None)
                a['class'] = (a.get('class', '') + f' {kls}').strip()
        e.a = a
        if t in TAGMAP:
            e.tag = TAGMAP[t]
            e.add_cls(f'ax-{t}')
    return root


UTIL_STROKE = {'fill': 'none', 'stroke': 'currentColor', 'stroke-width': '2', 'stroke-linecap': 'round',
               'stroke-linejoin': 'round'}
STR = re.compile(r'"[^"]*"|\'[^\']*\'')
PSEUDO = [(':focus-visible', '[data-ax-focus]'), (':focus-within', '[data-ax-within]'), (':focus', '[data-ax-focus]'),
          (':hover', '[data-ax-hover]'), (':checked', '[data-ax-checked]'), (':disabled', '[data-ax-disabled]')]
TAGSEL = re.compile(r'(?<![\w\-.#\[:])(' + '|'.join(sorted(TAGMAP, key=len, reverse=True)) + r')(?![\w-])')


def rewrite_selector(sel):
    keep = []
    sel = STR.sub(lambda m: keep.append(m.group(0)) or f'\x00{len(keep) - 1}\x00', sel)
    if re.search(r'::(-webkit-|backdrop|marker|-moz-)', sel):
        return None
    for a, b in PSEUDO:
        sel = sel.replace(a, b)
    sel = sel.replace('[aria-', '[data-ax-aria-').replace('[role', '[data-ax-role').replace('[open]', '[data-ax-open]')
    sel = TAGSEL.sub(lambda m: f'.ax-{m.group(1)}', sel)
    return re.sub(r'\x00(\d+)\x00', lambda m: keep[int(m.group(1))], sel)


def css_blocks(css):
    """Top-level rules as (prelude, body); an at-rule's body holds its own rules."""
    css = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    out, i = [], 0
    while True:
        j = css.find('{', i)
        if j < 0:
            break
        depth, k = 1, j + 1
        while depth:
            if css[k] == '{':
                depth += 1
            elif css[k] == '}':
                depth -= 1
            k += 1
        out.append((css[i:j].strip(), css[j + 1:k - 1].strip()))
        i = k
    return out


def css_attrs_of(css):
    names = set(re.findall(r'\[([a-z][\w-]*)', re.sub(r'/\*.*?\*/', '', css, flags=re.S)))
    return names | {'aria-' + x[len('aria-'):] for x in names if x.startswith('aria-')}


def attr_ok(sel, markup):
    """A selector's attribute tests, outside :not(), each met somewhere in the plate's markup."""
    bare = re.sub(r':not\((?:[^()]|\([^()]*\))*\)', '', sel)
    for name, val in re.findall(r'\[([\w-]+)(?:="([^"]*)")?\]', bare):
        if val:
            if f'{name}="{val}"' not in markup:
                return False
        elif not re.search(rf'\s{re.escape(name)}(?:=|[\s>])', markup):
            return False
    return True


def split_selectors(pre):
    """A selector list split at its top-level commas only, so :is(a, b) stays whole."""
    out, depth, cur, quote = [], 0, '', None
    for ch in pre:
        if quote:
            quote = None if ch == quote else quote
        elif ch in '"\'':
            quote = ch
        elif ch in '([':
            depth += 1
        elif ch in ')]':
            depth -= 1
        elif ch == ',' and depth == 0:
            out.append(cur)
            cur = ''
            continue
        cur += ch
    return out + [cur]


def prune_css(css, classes, markup=''):
    out = []
    for pre, body in css_blocks(css):
        if pre.startswith('@'):
            if re.search(r'forced-colors|prefers-reduced-motion', pre):
                continue
            inner = prune_css(body, classes, markup)
            if inner:
                out.append(f'{pre}{{{inner}}}')
            continue
        sels = []
        for s in split_selectors(pre):
            s = rewrite_selector(s.strip())
            if s and all(c in classes for c in re.findall(r'\.([A-Za-z][\w-]*)', s)) and (not markup or attr_ok(s, markup)):
                sels.append(s)
        if sels:
            body = re.sub(r'(?:^|;)\s*(?:transition|cursor|user-select|-webkit-tap-highlight-color|will-change)\s*:[^;]*', '', body)
            body = body.strip().strip(';')
            if body:
                out.append(f'{",".join(sels)}{{{body}}}')
    return ''.join(out)


def alias_vars(css):
    """A token read twice or more in one plate is read once, through a short property set on the plate (D2-1366)."""
    counts = {}
    for v in re.findall(r'var\((--oa-[\w-]+)\)', css):
        counts[v] = counts.get(v, 0) + 1
    names = sorted((v for v, n in counts.items() if n > 1), key=lambda v: (-counts[v], v))
    if not names:
        return css
    short = {v: f'--x{i}' for i, v in enumerate(names)}
    css = re.sub(r'var\((--oa-[\w-]+)\)', lambda m: f'var({short[m.group(1)]})' if m.group(1) in short else m.group(0), css)
    return '.ax{' + ';'.join(f'{s}:var({v})' for v, s in short.items()) + '}' + css


def minify(css):
    css = re.sub(r'\s+', ' ', css)
    css = re.sub(r'\s*([{};,>])\s*', r'\1', css)
    css = re.sub(r':\s+', ':', css)
    css = re.sub(r';}', '}', css)
    return css.strip()


# One look for every plate: the stage, the numbered callout, the target bracket and the key (D2-xxx in the notes)
AX_CSS = minify("""
.ax{container-type:inline-size}
.ax-st{position:relative;padding:28px 24px 28px 44px;border:1px solid var(--oa-color-border-hairline);background:var(--oa-color-surface);color:var(--oa-color-text-primary);overflow-wrap:anywhere}
@container (max-width:24rem){.ax-st{padding:24px 14px 24px 40px}}
.ax-p{position:relative}
.ax-n{position:absolute;z-index:3;top:-24px;left:-2px;display:flex;align-items:center;justify-content:center;width:20px;height:20px;border-radius:50%;background:var(--oa-color-text-primary);color:var(--oa-color-surface);box-shadow:0 0 0 2px var(--oa-color-surface);font:700 .8125rem/1 var(--oa-font-family-reading);letter-spacing:0;text-transform:none;text-decoration:none}
.ax-tr{left:auto;right:-2px}.ax-bl{top:auto;bottom:-24px}.ax-br{top:auto;bottom:-24px;left:auto;right:-2px}
.ax-lm{top:50%;margin-top:-10px;left:-28px}.ax-rm{top:50%;margin-top:-10px;left:auto;right:-28px}
.ax-il{margin:0 0 20px}
.ax-t{position:absolute;top:0;bottom:0;left:-14px;width:5px;border:2px solid var(--oa-color-text-primary);border-right:0}
.ax-t .ax-n{top:50%;left:-27px;margin-top:-10px}.ax-tup .ax-n{top:-24px;left:-14px;margin-top:0}
.ax-upl{top:-30px;left:0}.ax-dnl{top:auto;bottom:-30px;left:0}.ax-dnrl{top:auto;bottom:-30px;left:auto;right:-2px}
.ax-upl::after,.ax-dnl::after,.ax-dnrl::after{content:"";position:absolute;left:9px;height:8px;border-left:1px solid var(--oa-color-text-primary)}
.ax-upl::after{top:22px}.ax-dnl::after,.ax-dnrl::after{bottom:22px}
.ax-tlm{left:14px}
.ax-blx{top:auto;bottom:-24px}.ax-brx{top:auto;bottom:-24px;left:auto;right:-2px}.ax-trx{left:auto;right:-2px}
.ax-rmx{top:50%;margin-top:-10px;left:auto;right:-28px}
@container (max-width:24rem){.ax-blx{top:50%;bottom:auto;margin-top:-10px;left:-28px}
.ax-brx,.ax-trx{top:50%;bottom:auto;margin-top:-10px;right:-28px}.ax-rmx{top:-24px;margin-top:0;right:-2px}}
.ax-try{left:auto;right:-2px}
@container (max-width:36rem){.ax-try{top:50%;margin-top:-10px;right:-28px}}
.ax-trb{left:auto;right:-2px}
@container (max-width:24rem){.ax-trb{top:auto;bottom:-24px}}
.ax-in{top:6px;left:6px}.ax-inr{top:6px;left:auto;right:6px}.ax-l{top:2px;left:-28px}.ax-up{top:-24px;left:0}.ax-dn{top:auto;bottom:-24px;left:0}
.ax-st .ax-input{display:flex;align-items:center}.ax-nw{white-space:nowrap}.ax-lup{top:2px;left:-28px}
@container (min-width:34rem){.ax-lup{top:-22px;left:0}}
.ax-k{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:8px 24px}
@container (min-width:34rem){.ax-k{grid-template-columns:1fr 1fr}}
.ax-k li{position:relative;min-height:22px;padding-left:30px;font:var(--oa-type-body-small);color:var(--oa-color-text-primary)}
.ax-k .ax-n{top:1px;left:0;box-shadow:none}.ax-k b{font-weight:700}
.ax-u,.ax-u16{fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}.ax-u16{stroke-width:1.5}
""")


def render(sets, root, key, extra_css='', illus=False):
    """The plate's markup: the stage with the cut component and its callouts, then the key. An invented piece takes the
    shell's Illustrative chip at the plate's head, in place of any label the code set draws (CD-S7, CA-S7, D2-1551)."""
    if illus:
        drop(*[e for e in walk(root) if any('illus' in c for c in e.cls())])
    code_css, markup, classes = draw(sets, root, extra_css)
    lis = ''.join(f'<li><span class="ax-n">{n}</span><b>{html.escape(term)}.</b> {html.escape(words)}</li>'
                  for n, term, words in key)
    ax_classes = classes | {'ax', 'ax-st', 'ax-k', 'ax-n'} | ({'ax-il'} if illus else set())
    ax_css = prune_css(AX_CSS, ax_classes)
    css = alias_vars(minify(ax_css + code_css))
    head = '<p class="ax-il"><span class="illus">Illustrative</span></p>' if illus else ''
    return f'<style>{css}</style><div class="ax"><div class="ax-st">{head}{markup}</div><ol class="ax-k">{lis}</ol></div>'


def draw(sets, root, extra_css=''):
    """The cut component as a picture: its markup and its own CSS, cut to the rules it uses, class names shortened."""
    css_all = ''.join((CODE / f'c-18-{s}.css').read_text() for s in sets)
    root = to_picture(root, css_attrs_of(css_all))
    markup = ser(root)
    classes = set(re.findall(r'class="([^"]*)"', markup))
    classes = {c for group in classes for c in group.split()}
    code_css = minify(prune_css(css_all, classes, markup) + extra_css)
    # shorten the code's class names inside the plate (D2-1366); a class holding "illus" keeps its name, so the shell
    # still finds the piece's Illustrative label
    used = sorted({c for c in classes if c.startswith('oa-') and 'illus' not in c}, key=lambda c: (-len(c), c))
    # letters only: the specimen build leaves a class unprefixed after a digit, so .c9.c1 would lose its second class
    def letters(i):
        out = ''
        while True:
            out = 'abcdefghijklmnopqrstuvwxyz'[i % 26] + out
            i = i // 26 - 1
            if i < 0:
                return 'k' + out
    short = {c: letters(i) for i, c in enumerate(used)}

    markup = re.sub(r'class="([^"]*)"', lambda m: 'class="' + ' '.join(short.get(c, c) for c in m.group(1).split()) + '"',
                    markup)
    code_css = re.sub(r'\.(oa-[\w-]+)', lambda m: '.' + short.get(m.group(1), m.group(1)), code_css)
    return code_css, markup, classes


def opener():
    """Chapter 18's opener (the round 2 fix brief's call 8, CD-S18, D2-1550): a button, a chip and a choice in one row,
    each drawn from its own code set at true size, as a picture. The row wraps where the column is narrow."""
    b = D('button')
    only(b, q(qa(b, 'oa-button-row')[0], 'oa-button--primary'))
    t = D('toggle')
    only(t, qa(q(t, 'oa-toggle-chips'), 'oa-toggle--chip')[0])
    c = D('choice')
    row = q(c, 'oa-choice-row')
    only(c, row)
    drop(*qa(row, 'oa-choice-item')[2:])
    root = El('#')
    for tree in (b, t, c):
        for k in tree.k:
            if isinstance(k, El):
                k.up = root
                root.k.append(k)
    code_css, markup, _ = draw(['button', 'toggle', 'choice'], root)
    css = alias_vars(minify('.ax-op{display:flex;flex-wrap:wrap;align-items:center;gap:16px 24px}' + code_css))
    alt = ('Three controls from this chapter, drawn from their code: a primary button, Save to your list, filled in '
           'Charcoal; a chip that is on, Housing, with the selected check, its word in bold and a 2 px edge; and a '
           'choice of two, Summary and Full text, with Summary checked the same way.')
    return f'<style>{css}</style><div class="ax ax-op">{markup}</div>', alt


def D(name):
    return parse((CODE / f'c-18-{name}.html').read_text())


def focus(e):
    e.a['data-ax-focus'] = None


def hover(e):
    e.a['data-ax-hover'] = None


# ------------------------------------------------------------------------------------------------ the 24 plates
# Each returns (sets, root, key, what, notes, illustrative, extra_css). The key's numbers follow reading order, and every
# number in the key sits on the plate.
def p01():
    r = D('button')
    rows = qa(r, 'oa-button-row')

    def label_of(row):
        sib = [x for x in row.up.k if isinstance(x, El)]
        return sib[sib.index(row) - 1]
    save, read = q(rows[0], 'oa-button--primary'), q(rows[0], 'oa-button--quiet')
    start = q(r, 'oa-button--icon-start')
    # the unavailable button is the one its reason line describes; the ask now stands on a row of its own (CD-M2)
    send = next(e for e in qa(r, 'oa-button') if e.a.get('aria-describedby') == 'oa-button-why')
    why = next(e for e in qa(r, 'oa-button-note') if e.a.get('id') == 'oa-button-why')
    only(r, label_of(rows[0]), rows[0], label_of(start.up), start.up, label_of(send.up), send.up, why)
    for e in qa(r, 'oa-button--ask') + qa(r, 'oa-button--icon-end'):
        drop(e)
    say(label_of(rows[0]), 'Primary and quiet')
    focus(save)
    pin(save, 1, 'lm')
    pin(save, 2, 'tr')
    pin(read, 3, 'rm')
    bracket(start, 4)
    pin(start, 5, 'rmx')
    pin(send, 6, 'rmx')
    pin(why, 7)
    key = [(1, 'Word', 'What the button does, in a word or a few; the button’s name starts with it'),
           (2, 'Focus ring', 'The code’s own 2 px ring at a 2 px gap, drawn at once'),
           (3, 'Fill or edge', 'A primary button is filled; a quiet one draws a 1 px edge in the strong border color'),
           (4, 'Height', 'At least 44 px tall and 44 px wide'),
           (5, 'Utility icon', '24 px, before or after the word, in the word’s ink'),
           (6, 'Unavailable', 'A dashed edge and the disabled label color; it keeps its focus'),
           (7, 'Reason line', 'Says what makes the button available, and the button points to it')]
    return ['button'], r, key, 'a button', '', False, '.oa-button-k{margin-bottom:28px}'


def p02():
    r = D('toggle')
    chips = q(r, 'oa-toggle-chips')
    k = qa(r, 'oa-toggle-k')[1]
    hs, hc, el = qa(chips, 'oa-toggle--chip')[:3]
    only(r, k, chips)
    drop(*qa(chips, 'oa-toggle--chip')[2:])
    bracket(hs, 1)
    pin(hs, 2)
    pin(hs, 3, 'tr')
    pin(hc, 4, 'lm')
    pin(hc, 5, 'rm')
    key = [(1, 'Height', '44 px tall and at least 44 px wide'),
           (2, 'On: check and bold word', 'The selected check, 24 px, before the word, and the word in bold'),
           (3, 'On: 2 px edge', 'In the strong border color; the fill stays the ground'),
           (4, 'Off: word', 'The same word at 600, the weight every control’s word takes, with no check'),
           (5, 'Off: 1 px edge', 'The chip’s edge when it is off')]
    return ['toggle'], r, key, 'a chip, on and off', 'The chip that is on stands above one that is off.', True, (
        '.oa-toggle-k{margin-bottom:28px}.oa-toggle-chips{display:flex;flex-direction:column;align-items:flex-start;gap:16px}')


def p03():
    r = D('choice')
    items = qa(r, 'oa-choice-item')
    legend, why = q(r, 'oa-choice-legend'), q(r, 'oa-choice-why')
    focus(q(items[0], 'oa-choice-input'))
    pin(legend, 1)
    bracket(items[0], 2)
    pin(q(items[0], 'oa-choice-face'), 3)
    pin(q(items[0], 'oa-choice-face'), 4, 'tr')
    pin(q(items[1], 'oa-choice-face'), 5, 'try')
    pin(q(items[2], 'oa-choice-face'), 6, 'tr')
    pin(why, 7)
    key = [(1, 'Legend', 'Names the group, and a screen reader says it on entering'),
           (2, 'Height', 'Each segment 44 px tall, and all of it is the label'),
           (3, 'Checked', 'The selected check before the word, the word in bold and a 2 px edge'),
           (4, 'Focus ring', 'Around the whole segment of the radio button in focus'),
           (5, 'Segment', 'A choice not taken: its word inside a 1 px edge'),
           (6, 'Waiting', 'A choice that cannot be taken yet: a dashed edge and the disabled color'),
           (7, 'Reason line', 'Says why that choice waits')]
    return ['choice'], r, key, 'a choice of one of a few', '', False, (
        '.oa-choice-legend{margin-bottom:28px}'
        '@container (max-width:36rem){.oa-choice-row{display:flex;flex-direction:column;align-items:flex-start}}')


def p04():
    m = D('masthead')
    head = q(m, 'oa-masthead-dialog-head')
    only(m, head)
    t = D('theme-switch')
    fs = q(t, 'oa-theme')
    items = qa(fs, 'oa-theme-item')
    only(t, fs)
    root = El('#')
    for part in (m, t):
        for k in part.k:
            if isinstance(k, El):
                k.up = root
                root.k.append(k)
    pin(q(head, 'oa-masthead-dialog-name'), 1)
    pin(q(fs, 'oa-theme-legend'), 2, 'up')
    bracket(items[0], 3)
    pin(q(items[0], 'oa-theme-face'), 4)
    pin(q(items[2], 'oa-theme-face'), 5, 'rm')
    key = [(1, 'Its place', 'At the top of the phone menu, under its title, or in the masthead, in the same place on '
                            'every page'),
           (2, 'Legend', 'The word Theme names the group of three'),
           (3, 'Height', 'Each segment 44 px tall'),
           (4, 'A choice', 'Light, Dark and Match my device, each its word inside a 1 px edge'),
           (5, 'Checked', 'Match my device, checked at first: the selected check, the word in bold and a 2 px edge')]
    return ['masthead', 'theme-switch'], root, key, 'the theme switch', '', False, ('.oa-masthead-dialog{overflow:visible;height:auto}'
                                                                                 '.oa-theme-legend{margin-bottom:28px}')


def p05():
    r = D('link')
    skip, text = q(r, 'oa-link-skip'), qa(r, 'oa-link-text')[0]
    ks = qa(r, 'oa-link-k')
    only(r, skip, ks[0], text)
    links = qa(text, 'oa-link')
    focus(skip)
    hover(links[0])
    pin(skip, 1, 'lm')
    at_word(links[0], 2, 'upl')
    at_word(links[0], 3, 'dnl')
    at_word(links[1], 4, 'upl')
    pin(q(text, 'oa-link-last'), 5, 'dnrl')
    key = [(1, 'Skip link', 'Hidden until the Tab key reaches it first on a page, then shown at the top'),
           (2, 'Words', 'Say where the link goes, and make sense read on their own'),
           (3, 'Underline', '1 px at rest, 2 px under a pointer, as here'),
           (4, 'Link to another site', 'Its name ends with the hidden words “(another site)” for a screen reader'),
           (5, 'Mark', 'The 16 px mark for another site, after the last word, which it never leaves')]
    return ['link'], r, key, 'links', ('The skip link is drawn in place above the text, and the lines are spaced apart to '
                                       'leave room for the callouts.'), False, ('.oa-link-skip{position:relative;display:inline-block;margin:0 0 20px}'
                                       '.oa-link-text{line-height:3.25}')


def p06():
    r = D('masthead')
    head = q(r, 'oa-masthead')
    bar = q(r, 'oa-masthead-bar')
    dlg = q(r, 'oa-masthead-dialog')
    only(r, head)
    for e in qa(dlg, 'oa-masthead-row') + qa(dlg, 'oa-masthead-sub'):
        drop(e)
    dlg.a.pop('open', None)
    # a second bar, as it draws with 40rem of room or more, beside the phone bar the container shows by default
    nav = q(bar, 'oa-masthead-nav')
    drop(nav, q(bar, 'oa-masthead-wm--24'))
    nav.add_cls('ax-wide')
    nav.up = head
    head.k.insert(head.k.index(bar) + 1, nav)
    pin(q(bar, 'oa-masthead-home'), 1)
    menu = q(bar, 'oa-masthead-menu')
    bracket(menu, 2)
    pin(menu, 3, 'trx')
    pin(nav, 4, 'l')
    pin(q(nav, 'oa-masthead-part'), 5, 'upl')
    pin(q(dlg, 'oa-masthead-dialog-name'), 6, 'l')
    pin(q(dlg, 'oa-masthead-close'), 7, 'tr')
    rows = qa(dlg, 'oa-masthead-row-link')
    pin(rows[0], 8, 'rm')
    pin(rows[1], 9, 'rm')
    key = [(1, 'Home link', 'The product’s name, from the wordmark’s master, links to the front page'),
           (2, 'Height', 'Each link and Menu at least 44 px tall; Close the menu 44 by 44 px'),
           (3, 'Menu', 'Under 40rem: three bars and the word, which opens the menu over the page'),
           (4, 'Navigation', 'Named Parts of the site; with 40rem of room it sits in the bar in place of Menu'),
           (5, 'Current part', 'Bold, with a 2 px underline'),
           (6, 'Open menu', 'Its title, in a dialog that holds focus until it closes'),
           (7, 'Close the menu', 'The cross and its words; Escape closes it too, and focus returns to Menu'),
           (8, 'Current row', 'The selected band, a 4 px bar and bold words'),
           (9, 'Row', 'Each part again, 44 px tall')]
    extra = ('.ax-wide.oa-masthead-nav{display:block;margin:24px 0 0;padding:16px 16px 0;border-top:1px dashed var(--oa-color-border-hairline)}'
             '.oa-masthead-wm--16{display:block}.oa-masthead-bar .oa-masthead-menu{display:inline-flex}'
             '.oa-masthead-dialog{display:block;height:auto;margin-top:16px;border:1px solid var(--oa-color-border-strong);overflow:visible}'
             '.oa-masthead-dialog-head{position:static}.oa-masthead-dialog .oa-masthead-row-link{margin-right:36px}')
    return ['masthead'], r, key, 'a masthead and its phone menu', '', False, extra


def p07():
    r = D('location')
    crumbs, rail = q(r, 'oa-location-crumbs'), q(r, 'oa-location-rail')
    ks = qa(r, 'oa-location-k')
    only(r, ks[0], crumbs, ks[1], rail)
    items = qa(rail, 'oa-location-item')
    at_word(q(crumbs, 'oa-location-link', 2), 1, 'dnl', glue=True)      # under its first word, wherever the trail wraps
    pin(ks[1], 2)
    pin(items[0], 3, 'rm')
    bracket(items[1], 4)
    pin(items[1], 5, 'rm')
    key = [(1, 'Breadcrumb’s current page', 'The last step, in bold and not underlined; its link says it is the page'),
           (2, 'Label', 'Names the list, as the navigation’s own name does'),
           (3, 'Link', 'A place to go, with its words'),
           (4, 'Height', 'Rows 44 px tall in a list a thumb uses'),
           (5, 'Current place', 'The selected band, a 4 px bar drawn as a border, and bold words')]
    return ['location'], r, key, 'location lists', '', False, ('.oa-location-k{margin-bottom:28px}'
                                                                 '.oa-location-crumbs{margin-bottom:40px}'
                                                                 '.oa-location-rail{margin-right:36px}')


def p08():
    r = D('disclosure')
    stack = qa(r, 'oa-disclosure-stack')[0]
    ds = qa(stack, 'oa-disclosure')
    only(r, stack)
    drop(q(ds[1], 'oa-disclosure-body'))
    s0, s1 = q(ds[0], 'oa-disclosure-summary'), q(ds[1], 'oa-disclosure-summary')
    focus(s1)
    pin(q(s0, 'oa-disclosure-label'), 1, 'l')
    pin(s0, 2, 'tr')
    pin(q(ds[0], 'oa-disclosure-body'), 3, 'l')
    bracket(s1, 4)
    pin(s1, 5, 'bl')
    pin(s1, 6, 'br')
    key = [(1, 'Words', 'Name the part that opens'),
           (2, 'Chevron up', 'While the part is open'),
           (3, 'The part that opens', 'Shown in place, under its row'),
           (4, 'Height', 'The row at least 44 px tall across its width'),
           (5, 'Focus ring', 'Around the row in focus'),
           (6, 'Chevron down', 'While the part is closed')]
    return ['disclosure'], r, key, 'a disclosure, open and closed', '', False, ''


def p09():
    r = D('tabs')
    lst, why = q(r, 'oa-tabs-list'), q(r, 'oa-tabs-why')
    tabs = qa(lst, 'oa-tabs-tab')
    panel = q(r, 'oa-tabs-panel')
    only(r, q(r, 'oa-tabs-k'), lst, why, panel)
    focus(tabs[0])
    pin(lst, 1, 'br')
    bracket(tabs[0], 2)
    pin(tabs[0], 3)
    pin(tabs[0], 4, 'tr')
    pin(tabs[1], 5, 'tr')
    pin(tabs[3], 6, 'rm')
    pin(panel, 7, 'l')
    key = [(1, 'Tab list', 'Named Views of the bill; the Tab key enters at the selected tab, and the arrow keys move'),
           (2, 'Height', 'Each tab 44 px tall'),
           (3, 'Selected tab', 'A 4 px bar and bold words; its panel shows at once'),
           (4, 'Focus ring', 'Inside the tab in focus, with its 2 px gap, since the tabs stand close (Rule 18.11)'),
           (5, 'Tab', 'A view’s name in a word or two'),
           (6, 'Unavailable tab', 'Dashed, with the reason under the list'),
           (7, 'Panel', 'The selected tab’s view, named by its tab')]
    return ['tabs'], r, key, 'tabs', '', True, '.oa-tabs-k{margin-bottom:28px}.oa-tabs-list{row-gap:28px}'


def p10():
    r = D('table')
    rows = qa(r, 'oa-table-row')
    only(r, q(r, 'oa-table-grid'))
    for row in rows[3:]:
        drop(row)
    for row in rows[:3]:
        cells = [e for e in row.k if isinstance(e, El)]
        drop(cells[-1])
    th = qa(r, 'oa-table-th')
    sort = q(th[0], 'oa-table-sort')
    pin(q(r, 'oa-table-caption'), 1, 'l')
    bracket(q(th[0], 'oa-table-sort'), 2)
    pin(q(th[0], 'oa-table-word'), 3, 'up')
    pin(q(th[1], 'oa-table-word'), 4, 'up')
    pin(q(r, 'oa-table-grid').up, 5, 'bl')      # on the table's wrapper: a span inside a table would leave it
    key = [(1, 'Caption', 'Names the table, as table markup’s own caption'),
           (2, 'Height', 'Each sort button at least 44 px tall, across its words and arrow'),
           (3, 'Sorted heading', 'The arrow turned to the order, and the heading says it in aria-sort'),
           (4, 'Column heading', 'Each heading holds a sort button with its words and a 16 px arrow'),
           (5, 'Row rule', 'A hairline between rows, drawn as a border')]
    return ['table'], r, key, 'a sortable table', 'The status line under the table is written by its script when a reader sorts; the plate shows the table at rest.', True, '.oa-table-caption{padding-bottom:24px}'


def p11():
    r = D('scroll-region')
    hint, frame = q(r, 'oa-scroll-hint'), q(r, 'oa-scroll-frame')
    # the ring sits inside the frame where the code sets a negative offset (D2-1475), around it otherwise
    ring = re.search(r'\.oa-scroll-frame:focus-visible\s*\{[^}]*outline-offset:\s*([^;}]+)',
                     (CODE / 'c-18-scroll-region.css').read_text())
    inside = bool(ring) and ring.group(1).strip().startswith(('-', 'calc(-1', 'calc(0px -', 'calc(-'))
    hint.a.pop('hidden', None)
    focus(frame)
    pin(q(r, 'oa-scroll-k'), 1)
    pin(hint, 2)
    # on the region around the frame, since the frame cuts anything past its edge
    pin(q(r, 'oa-scroll'), 3, 'tr')
    pin(q(r, 'oa-scroll'), 4, 'bl')
    pin(q(r, 'oa-scroll'), 5, 'br')
    key = [(1, 'Name', 'Names the frame, and the frame takes it'),
           (2, 'Hint', 'Shown only while the content is wider than the frame'),
           (3, 'Wide content', 'Its own width, cut by the frame’s edge'),
           (4, 'Frame', 'A hairline edge; the content scrolls inside it, so the page never does'),
           (5, 'Focus ring', ('Drawn inside the frame’s edge' if inside else 'Drawn around the frame')
            + '; the frame is a Tab stop only while it scrolls, and the arrow keys move it')]
    return ['scroll-region'], r, key, 'a scroll region', '', False, '.oa-scroll-frame{overflow:hidden}.oa-scroll-hint{margin-bottom:28px}'


def p12():
    r = D('code-block')
    panel = q(r, 'oa-code-panel')
    st = q(r, 'oa-code-status')
    only(r, q(r, 'oa-code-name'), panel, st)
    err = parse(ser(st)).k[0]
    for mark in qa(st, 'oa-code-mark--error'):
        mark.a['hidden'] = None
    for mark in qa(st, 'oa-code-mark--ok'):
        mark.a.pop('hidden', None)
    say(q(st, 'oa-code-words'), 'Copied the HTML, 2 lines, to the clipboard.')
    err.a['data-oa-state'] = 'error'
    words = q(err, 'oa-code-words')
    words.k = ['<b>Error:</b> The browser blocked copying. The code is selected above: press Control and C, or Command and C.']
    for mark in qa(err, 'oa-code-mark--ok'):
        mark.a['hidden'] = None
    for mark in qa(err, 'oa-code-mark--error'):
        mark.a.pop('hidden', None)
    err.up = st.up
    st.up.k.insert(st.up.k.index(st) + 1, err)
    copy = q(panel, 'oa-code-copy')
    pin(q(panel, 'oa-code-lang'), 1, 'l')
    bracket(copy, 2)
    pin(copy, 3, 'tr')
    pin(panel, 4, 'bl')
    pin(st, 5)
    pin(err, 6)
    key = [(1, 'Panel label', 'The file’s kind, HTML, CSS or Script'),
           (2, 'Height', 'Each Copy button 44 px tall'),
           (3, 'Copy button', 'Named for what it copies, Copy the HTML, and described by the block’s name'),
           (4, 'Code', 'At 14 px in the code face, scrolling inside its panel'),
           (5, 'Status line', 'The success mark and what was copied, in words'),
           (6, 'Copy refused', 'The error mark, “Error:”, the Error Band and the 4 px bar, with the code selected')]
    # a picture holds no scrolling region (axe's scrollable-region-focusable); the code is cut at the panel's edge, as
    # the panel draws it at rest
    return ['code-block'], r, key, 'a code block', 'The code is cut at the panel’s edge, as it draws before a reader scrolls it.', False, '.oa-code-status{margin-top:28px}.oa-code-pre{overflow:hidden}'


def p13():
    r = D('copy')
    row = q(r, 'oa-copy-row', 0)
    st = q(r, 'oa-copy-status')
    only(r, row, st)
    say(q(st, 'oa-copy-words'), 'Copied --oa-color-text-primary.')
    for mark in qa(st, 'oa-copy-mark--error'):
        mark.a['hidden'] = None
    for mark in qa(st, 'oa-copy-mark--ok'):
        mark.a.pop('hidden', None)
    btn = q(row, 'oa-copy-button')
    pin(q(row, 'oa-copy-value'), 1, 'lup')
    bracket(btn, 2)
    pin(btn, 3, 'br')
    pin(st, 4)
    key = [(1, 'Value', 'The value to copy, in the code face, beside what it is'),
           (2, 'Size', 'At least 44 by 44 px, even beside a short value'),
           (3, 'Copy button', 'The two-sheet icon and the word Copy; hidden words finish its name with what it '
                              'copies'),
           (4, 'Status line', 'The success mark and what was copied, in words; the icon never turns into a check')]
    return ['copy'], r, key, 'a copy control', '', False, '.oa-copy-status{margin-top:28px}'


def p14():
    r = D('download')
    ds = qa(r, 'oa-download')
    ks = qa(r, 'oa-download-k')
    why = q(r, 'oa-download-why')
    bracket(ds[0], 1)
    pin(ds[0], 2)
    pin(ds[0], 3, 'br')
    pin(ds[1], 4, 'tr')
    pin(why, 5)
    key = [(1, 'Height', '44 px tall'),
           (2, 'Icon', 'The download arrow into a tray, 24 px, before the word'),
           (3, 'Words', 'From “Download” to the file, its type and its size'),
           (4, 'Not ready', 'A dashed edge and the disabled color; it keeps its focus'),
           (5, 'Reason line', 'Says why the file is not ready and when to try again')]
    return ['download'], r, key, 'a download', '', True, '.oa-download-k{margin-bottom:28px}'


def p15():
    r = D('search')
    box, st = q(r, 'oa-search-box'), q(r, 'oa-search-status')
    only(r, q(r, 'oa-search-label'), box, st)
    q(box, 'oa-search-clear').a.pop('hidden', None)
    say(q(box, 'oa-search-input'), 'lottery')
    say(st, '0 of 12 reforms. No reform matches. Clear the search to see all 12.')
    field = q(box, 'oa-search-input')
    pin(q(r, 'oa-search-label'), 1)
    bracket(box, 2)
    pin(box, 3)
    pin(q(box, 'oa-search-clear'), 4, 'tr')
    pin(st, 5)
    key = [(1, 'Label', 'Above the field, always shown; a placeholder never stands in for it'),
           (2, 'Height', 'The field 44 px tall; Clear the search 44 by 44 px'),
           (3, 'Field', 'Its edge on the field ground, with the magnifier before the text'),
           (4, 'Clear the search', 'The cross, once there is text; Escape clears it too'),
           (5, 'Status line', 'The count, and when nothing matches, the advice in the same line')]
    return ['search'], r, key, 'a search', '', False, '.oa-search-label{display:block;margin-bottom:28px}'


def p16():
    r = D('filter-bar')
    bar, sheet, st = q(r, 'oa-filters-bar'), q(r, 'oa-filters-sheet'), q(r, 'oa-filters-status')
    first = qa(sheet, 'oa-filters-chip')[0].a.get('data-oa-filter')
    results = qa(r, 'oa-filters-result')
    n_on = sum(1 for x in results if x.a.get('data-oa-area') == first)
    only(r, bar, sheet, st)
    tog, clear = q(bar, 'oa-filters-toggle'), q(bar, 'oa-filters-clear')
    tog.a['aria-expanded'] = 'true'
    clear.a.pop('hidden', None)
    sheet.a.pop('hidden', None)
    say(q(tog, 'oa-filters-count'), 'Filters, 1 on')
    chips = qa(sheet, 'oa-filters-chip')
    chips[0].a['aria-pressed'] = 'true'
    for g in qa(sheet, 'oa-filters-chips')[1:]:
        drop(g)
    drop(qa(sheet, 'oa-filters-k')[1])
    say(st, f'{n_on} of {len(results)} reforms')
    bracket(tog, 1)
    pin(tog, 2)
    pin(tog, 3, 'br')
    pin(clear, 4, 'rm')
    for c in chips[2:]:
        drop(c)
    pin(chips[0], 5)
    pin(chips[1], 6, 'rmx')
    pin(st, 7)
    key = [(1, 'Height', '44 px tall for Filters, each chip and Clear filters'),
           (2, 'Filters', 'The funnel, the word and a chevron that points up while the filters are open'),
           (3, 'Count', 'How many filters are on, in the button’s own name'),
           (4, 'Clear filters', 'Shown only while a filter is on; focus moves to Filters after it'),
           (5, 'Chip on', 'The selected check, the word in bold and a 2 px edge'),
           (6, 'Chip off', 'Its word inside a 1 px edge'),
           (7, 'Status line', 'The count the filters leave, shared with the search')]
    return ['filter-bar'], r, key, 'a filter bar', 'Two chips of the area group, one on and one off, one above the other.', True, (
        '.oa-filters-k{margin-bottom:28px}.oa-filters-chips{display:flex;flex-direction:column;align-items:flex-start}'
        '@container (max-width:24rem){.oa-filters-clear{margin-top:28px}}')


def p17():
    r = D('form')
    fields = qa(r, 'oa-form-field')
    send = q(r, 'oa-form-send')
    st = q(r, 'oa-form-status')
    only(r, fields[0], fields[1], send, st)
    em = q(fields[0], 'oa-form-input')
    em.a['aria-invalid'] = 'true'
    say(em, 'name@example')
    err = q(fields[0], 'oa-form-error')
    err.a.pop('hidden', None)
    send.a['data-oa-yield'] = ''
    drop(q(fields[1], 'oa-form-error'))
    tpl = parse((CODE / 'c-18-form.html').read_text())
    done = q(tpl, 'oa-form-say-done')
    st.k = done.k
    for k in st.k:
        if isinstance(k, El):
            k.up = st
    pin(q(fields[0], 'oa-form-label'), 1)
    pin(em, 2, 'tr')
    pin(err, 3)
    pin(err, 4, 'tr')
    pin(q(fields[1], 'oa-form-hint'), 5)
    bracket(q(fields[1], 'oa-form-input'), 6)
    pin(send, 7, 'rmx')
    pin(st, 8)
    key = [(1, 'Label', 'Above its field, always shown'),
           (2, 'Field in error', 'The 4 px red bar on its edge, drawn as a border, and it points to its message'),
           (3, 'Error mark and “Error:”', 'The mark in the text’s ink, then “Error:”'),
           (4, 'The fix', 'On the Error Band with its own 4 px bar, in plain words'),
           (5, 'Hint', 'Under the label, read with the field'),
           (6, 'Height', 'Fields and the send button at least 44 px tall'),
           (7, 'Send', 'While an error holds the red, the ask steps down to the primary button'),
           (8, 'Success line', 'After a send that works: the success mark and what happens next')]
    return ['form'], r, key, 'a form field, in error and after a send', '', True, (
        '.oa-form-field .oa-form-error{margin-top:28px}.oa-form-send{margin-top:28px}')


def p18():
    r = D('messages')
    msgs = qa(r, 'oa-msg')
    only(r, *msgs)
    pin(msgs[0], 1, 'tlm')
    pin(q(msgs[0], 'oa-msg-words'), 2)
    pin(msgs[0], 3, 'lm')
    pin(msgs[0], 4, 'rm')
    pin(msgs[1], 5, 'rm')
    pin(msgs[2], 6, 'lm')
    key = [(1, 'Mark', '24 px: the error mark in the text’s ink'),
           (2, 'First word', '“Error:”, “Warning:” or what happened, in bold'),
           (3, 'Bar', '4 px, drawn as a border: Pillar Red for an error'),
           (4, 'Error Band', 'Behind an error on Newsprint; none on Charcoal'),
           (5, 'Warning', 'The warning mark and a 4 px bar, both in the text’s ink'),
           (6, 'Success', 'The success mark in Verdigris, with no bar')]
    return ['messages'], r, key, 'messages', '', False, '.oa-msg{margin-right:36px}.oa-msg + .oa-msg{margin-top:20px}'


def p19():
    r = D('loading-empty')
    ld, em = q(r, 'oa-wait-loading'), q(r, 'oa-wait-empty')
    pin(q(ld, 'oa-wait-still'), 1, 'lm')
    pin(ld, 2, 'rmx')
    pin(em, 3, 'tr')
    pin(em, 4, 'bl')
    key = [(1, 'Still drawing', 'An outline that never pulses or turns'),
           (2, 'Loading words', 'Say what is loading, in a status line'),
           (3, 'Empty region', 'A dashed edge around the words'),
           (4, 'What to do next', 'What is missing, then what to do to fill it')]
    return ['loading-empty'], r, key, 'loading and empty', ('The code set’s empty state names its next step in words '
                                                            'and holds no control yet; the caption’s control waits on the set.'), False, '.oa-wait-loading{width:fit-content}'


def p20():
    r = D('tracker')
    card = q(r, 'oa-tracker-card')
    only(r, card)
    for c in ('oa-tracker-take', 'oa-tracker-alert', 'oa-tracker-next', 'oa-tracker-why', 'oa-tracker-news'):
        for e in qa(card, c):
            drop(e)
    steps = qa(card, 'oa-tracker-step')
    pin(q(card, 'oa-tracker-bill'), 1)
    pin(q(steps[0], 'oa-tracker-mark'), 2, 'upl')
    pin(q(steps[1], 'oa-tracker-mark'), 3, 'upl')
    pin(q(steps[2], 'oa-tracker-mark'), 4, 'upl')
    pin(q(card, 'oa-tracker-status'), 5)
    pin(q(card, 'oa-tracker-check'), 6)
    key = [(1, 'Bill', 'Its number and title'),
           (2, 'Done', 'A filled step with its number and state word, Filed'),
           (3, 'Now', 'The step under way, its ring and its word; here a reader can take part'),
           (4, 'Not yet', 'A fine ring and its word'),
           (5, 'Status line', 'Says each change once, politely, in words'),
           (6, 'Check date', 'The warning mark, “Warning:” and when we last checked, beside a 4 px bar in ink')]
    return ['tracker'], r, key, 'a live tracker', '', True, '.oa-tracker-steps{margin-top:40px}'


def p21():
    r = D('report-reader')
    view, st, turn, why, size = (q(r, 'oa-reader-view'), q(r, 'oa-reader-status'), q(r, 'oa-reader-turn'),
                                 q(r, 'oa-reader-why'), q(r, 'oa-reader-size'))
    only(r, q(r, 'oa-reader-head'), view, st, turn, why, size)
    for pg in qa(view, 'oa-reader-page')[1:]:
        drop(pg)
    prev, nxt = q(turn, 'oa-reader-prev'), q(turn, 'oa-reader-next')
    pin(view, 1, 'lm')
    pin(st, 2)
    bracket(prev, 3)
    pin(prev, 4, 'tr')
    pin(nxt, 5, 'trb')
    pin(why, 6)
    pin(q(size, 'oa-reader-size-face'), 7, 'tr')
    key = [(1, 'Page view', 'The page as readable text, fitted to the width'),
           (2, 'Status line', 'The page number and title, said once on each turn'),
           (3, 'Height', '44 px tall'),
           (4, 'Unavailable', 'Previous page on the first page: a dashed edge, and it keeps its focus'),
           (5, 'Next page', 'Its word and the arrow after it'),
           (6, 'Reason line', 'Says why Previous page waits'),
           (7, 'Page size', 'Fit width or Full size, a choice of one, the checked one with its check')]
    return ['report-reader'], r, key, 'a report reader', '', True, ('.oa-reader-view{overflow:visible}'
                                                                     '.oa-reader-turn{margin-top:28px}'
                                                                     '@container (max-width:24rem){.oa-reader-why{margin-top:28px}}')


def p22():
    r = D('loop-stepper')
    steps = qa(r, 'oa-stepper-step')
    st, ctl, why = q(r, 'oa-stepper-status'), q(r, 'oa-stepper-controls'), q(r, 'oa-stepper-why')
    last = steps[-1]
    last.a['aria-current'] = 'step'
    line, more = q(last, 'oa-stepper-line'), q(last, 'oa-stepper-more')
    say(st, f'Step {len(steps)} of {len(steps)}: ' + re.sub(r'<[^>]+>', '', ser(line)) + ' ' + re.sub(r'<[^>]+>', '', ser(more)))
    play, reset, prev, nxt = (q(ctl, 'oa-stepper-play'), q(ctl, 'oa-stepper-reset'), q(ctl, 'oa-stepper-prev'),
                              q(ctl, 'oa-stepper-next'))
    for b in (reset, prev):
        b.a.pop('aria-disabled', None)
    nxt.a['aria-disabled'] = 'true'
    say(q(play, 'oa-stepper-word'), 'Play again')
    say(why, 'At the last step. Reset the loop to start again.')
    pin(st, 1)
    pin(last, 2)
    bracket(play, 3)
    pin(play, 4, 'tr')
    pin(reset, 5, 'tr')
    pin(prev, 6, 'br')
    pin(nxt, 7, 'br')
    pin(why, 8)
    key = [(1, 'Status line', 'Each step, said once, politely'),
           (2, 'Current step', 'A 4 px bar drawn as a border, in the step list'),
           (3, 'Height', '44 px tall'),
           (4, 'Play', 'Its icon and word; Pause while it runs, Play again at the end'),
           (5, 'Reset the loop', 'The open circle with one arrowhead, and its words'),
           (6, 'Previous step', 'The arrow mirrored, before the words'),
           (7, 'Next step, unavailable', 'At the last step: a dashed edge, and it keeps its focus'),
           (8, 'Reason line', 'Says why Next step waits and what to do')]
    return ['loop-stepper'], r, key, 'a loop stepper', ('Drawn at the last step, the state the stepper script writes '
                                                        'there, with its four buttons two by two, and one a row in a '
                                                        'column of 24rem or less, where two would cut their words, as the '
                                                        'code set stacks them.'), False, (
        '.oa-stepper-controls{grid-template-columns:repeat(2,minmax(0,1fr));margin-top:28px}.oa-stepper-why{margin-top:28px}'
        '@container (max-width:24rem){.oa-stepper-controls{grid-template-columns:minmax(0,1fr);row-gap:28px}}')


def p23():
    r = D('diagram-controls')
    drawing, panel, words = q(r, 'oa-diagram-drawing'), q(r, 'oa-diagram-panel'), q(r, 'oa-diagram-words')
    readout = q(r, 'oa-diagram-readout')
    only(r, q(r, 'oa-diagram-k'), q(r, 'oa-diagram-title'), drawing, readout, panel, words)
    items = qa(drawing, 'oa-diagram-item')
    drawing.a['data-oa-chosen'] = ''
    items[1].a['aria-pressed'] = 'true'
    focus(items[0])
    say(readout, 'Concentration of household wealth. How much of the nation’s wealth the top tenth of households '
                 'hold.')
    panel.a.pop('hidden', None)
    say(q(panel, 'oa-diagram-panel-name'), 'Money spent to influence politics')
    say(q(panel, 'oa-diagram-panel-text'), 'The money spent to influence elections and policy: campaign gifts, outside '
                                           'groups and lobbying.')
    bracket(items[0], 1)
    pin(items[0], 2, 'rmx')
    pin(items[1], 3, 'rmx')
    pin(items[2], 4, 'rmx')
    pin(readout, 5)
    pin(q(panel, 'oa-diagram-panel-name'), 6)
    pin(q(words, 'oa-diagram-summary'), 7, 'lm')
    key = [(1, 'Height', 'Each item at least 44 px tall on a phone'),
           (2, 'Item in focus', 'Its heavier mark and underlined label; the arrow keys move between items'),
           (3, 'Selected item', 'The selected check, bold words and a 2 px edge'),
           (4, 'Muted item', 'While another is selected: the muted edge and words'),
           (5, 'Readout line', 'The item in focus in words, as focus moves'),
           (6, 'Panel', 'Its title takes focus; Escape closes it and focus returns to the item'),
           (7, 'The lines in words', 'A disclosure that gives the drawing as sentences')]
    return ['diagram-controls'], r, key, 'diagram controls', ('The code set holds the disclosure for the lines in '
                                                              'words; a disclosure that shows the drawing as a table waits on the set.'), False, '.oa-diagram-title{margin-bottom:28px}'


def p24():
    r = D('id-chip')
    rows = qa(r, 'oa-chip-row')
    ks = qa(r, 'oa-chip-k')
    only(r, ks[0], rows[0], ks[1], rows[1])
    plain = q(rows[0], 'oa-chip')
    link = q(rows[1], 'oa-chip--link')
    hover(link)
    pin(plain, 1, 'up')
    pin(q(plain, 'oa-chip-id'), 2, 'up')
    pin(plain, 3, 'lm')
    bracket(link, 4)
    pin(link, 5, 'tr')
    key = [(1, 'Type word', 'Loop, Variable, Reform or Domain, before the code'),
           (2, 'Code', 'The atlas ID, in tabular figures'),
           (3, 'Edge', 'A hairline in the strong border color'),
           (4, 'Target', 'As a link, at least 24 px tall'),
           (5, 'As a link', 'It opens the record; its words keep a 1 px underline, 2 px under a pointer, as here')]
    return ['id-chip'], r, key, 'typed ID chips', '', False, '.oa-chip-row{padding:20px 0 24px}'


PLATES = [p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12, p13, p14, p15, p16, p17, p18, p19, p20, p21,
          p22, p23, p24]


def build(write=True):
    T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
    ctx = B.Ctx(T, {}, 'final')
    ch = json.loads(CH18.read_text()) if CH18.exists() else {'rules': []}
    caps = {r['id']: (r.get('correct') or {}).get('caption', '') for r in ch.get('rules', [])}
    sizes = {}
    for i, fn in enumerate(PLATES, 1):
        sets, root, key, what, note, illus, extra = fn()
        nums = [n for n, _, _ in key]
        if nums != list(range(1, len(key) + 1)):
            raise SystemExit(f'18.{i}: the key runs {nums}')
        body = render(sets, root, key, extra, illus)
        placed = sorted(int(x) for x in re.findall(r'class="ax-n[^"]*">(\d+)<', body))
        if placed != sorted(nums * 2):
            raise SystemExit(f'18.{i}: callouts on the plate {placed} do not match the key {nums}')
        sid = f's-18-{i:02d}-anatomy'
        alt = (f'Anatomy of {what}, drawn from its code to copy on Newsprint, with {C.num(len(key))} numbered callouts '
               'and a key. ' + ' '.join(f'{n}, {t}: {w}.' for n, t, w in key))
        alt = alt.replace('“', '').replace('”', '')
        notes = ('Drawn from ' + ', '.join(f'work/build/guide/code/c-18-{s}.html and .css' for s in sets)
                 + ' by stage_c_ch18_anatomy_build.py: the parts the caption names, as a picture (AX-S8), with the code’s '
                   'own states set by attribute and its class names shortened (D2-1366).' + (f' {note}' if note else ''))
        ctx.spec(sid, body, '18', f'18.{i}', alt, illustrative=illus, notes=notes)
        sizes[sid] = len(ctx.specs[sid]['html'].encode()) + len(alt.encode())
        if caps.get(f'18.{i}') is None and CH18.exists():
            print(f'  note: Rule 18.{i} has no anatomy caption in 18-components.json')
    body, alt = opener()
    ctx.spec('s-18-opener', body, '18', None, alt,
             notes='Chapter 18’s opener (call 8 of the round 2 fix brief, D2-1134, D2-1550): a primary button, a chip '
                   'that is on and a choice of two, drawn from c-18-button, c-18-toggle and c-18-choice by '
                   'stage_c_ch18_anatomy_build.py; it flows with the column and wraps on a phone.')
    sizes['s-18-opener'] = len(ctx.specs['s-18-opener']['html'].encode()) + len(alt.encode())
    if write:
        for sid, s in ctx.specs.items():
            (OUT_SP / f'{sid}.html').write_text(s['html'])
        MANIFEST.write_text(json.dumps({k: v['meta'] for k, v in sorted(ctx.specs.items())}, indent=1,
                                       ensure_ascii=False) + '\n')
    return sizes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build in memory and report sizes; write nothing')
    a = ap.parse_args()
    sizes = build(write=not a.check)
    total = sum(sizes.values())
    for sid, n in sizes.items():
        print(f'  {sid}: {n:,} bytes with its alt')
    print(f'anatomy: {len(sizes)} plates, {total:,} bytes, {total / len(sizes):,.0f} a plate')


if __name__ == '__main__':
    main()
