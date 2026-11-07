"""Chapter 11, Status and utility icons: its first rule group, Trackers (apply pass, systems designer, November 7, 2026).

Usage:
    python3 -I work/build/scripts/phase-2/apply_systems_ch11.py

Writes:
    work/build/guide/chapters/11-icons.json                 the chapter in the content contract (Stage A brief)
    work/build/guide/specimens/s-11-*.html                  one fragment per specimen
    work/build/guide/specimens/manifest-systems.json        the s-11-* entries, merged; the 05 to 07 entries are kept
    work/handoffs/phase-2/20261107_Apply-Pass-Systems-Ch11-Figures.json   every figure the chapter prints, and how

Decisions it carries: DR-108 and DR-128 (six steps, step 6 named for whoever signs), DR-109 (numbered steps in lists and
on story cards, the same marks as a vertical timeline on a bill's own page), DR-110 (the lockmark codes nothing),
DR-97 (one Illustrative label at the head of each invented piece), D2-254 (fixed artboards on the type scale), D2-308
(failure band), D2-324 (the tracker rules open chapter 11), and the creative director's two open items on Board 6:
step 5's hearing, with the take-part mark shown on step 5, and a stopped bill drawn in a list.

The mark geometry follows Board 6's Option B and Option D (work/build/scripts/phase-2/board6_tracker_build.py, read and
never edited), set here in tokens: circle sizes, line weights, the slash, the square and the take-part badge. Two
changes from the board: the badge's Charcoal keyline sits inside its 11 px disc, as Rule 05.5 draws a keyline, with
1.5 px of the surface cut around it so it parts from the ring; and every type size is one the scale names (D2-254).

Contrast figures are computed from tokens.json with the systems designer's helpers (stage_a_systems_core.py). The
specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color, no px
font size, and every class prefixed sx- so no name meets a shell class.
"""
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


B = _load('stage_a_systems_build')
C = sys.modules['stage_a_systems_core']
ROOT = C.ROOT
OUT_CH = ROOT / 'work/build/guide/chapters/11-icons.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-systems.json'
FIG_OUT = ROOT / 'work/handoffs/phase-2/20261107_Apply-Pass-Systems-Ch11-Figures.json'
CH = '11'
ILLUS = B.ILLUS
RED_W = 'data-red="working" data-red-job="take part now"'
ARROW = '<span aria-hidden="true"> →</span>'

# ------------------------------------------------------------------------------------------------ the six steps
STEPS = [
    ('Filed', 'A legislator files the bill, and it goes to a committee.'),
    ('Hearing', 'The committee holds a hearing and takes testimony on the bill. Many state legislatures take '
                'testimony from the public there. In Congress, the committee hears the witnesses it invites. A bill’s own '
                'page says how to take part.'),
    ('Committee vote', 'The committee votes on whether to send the bill to the full House or Senate.'),
    ('First chamber', 'The full House or Senate, wherever the bill was filed, votes on it.'),
    ('Second chamber', 'The other chamber takes the bill up. Its own committee can hold a hearing first, and then '
                       'the full chamber votes and both chambers agree on one text.'),
    ('Governor', 'The governor signs or vetoes the bill, and lawmakers can vote to override a veto.'),
]
SIGNER = {'state': 'Governor', 'federal': 'President'}
STEP6_BOTH = ('The governor signs a state bill and the President signs a federal one. Either can veto it, and lawmakers '
              'can vote to override a veto.')
CLERK = ['Introduced', 'Referred', 'Reported', 'Engrossed', 'Enrolled', 'Presented']


def names(kind='state'):
    return [n for n, _ in STEPS[:5]] + [SIGNER[kind]]


STATE_WORD = {'done': 'Done', 'now': 'Now', 'take': 'You can take part now', 'notyet': 'Not yet',
              'skipped': 'Never happened', 'stopped': 'Stopped'}
STATE_MEANS = {
    'done': 'The step happened.',
    'now': 'The bill is at this step, and the words beside the tracker name it.',
    'take': 'The bill is at this step, and the public can act before a date. The red disc, its place on the ring and '
            'the words carry it together.',
    'notyet': 'The bill has not reached this step.',
    'skipped': 'The bill moved past this step without it, as when a committee votes without holding a hearing. It keeps '
               'its number, so the count still runs to six.',
    'stopped': 'The bill ended here, as when a committee votes it down or a veto stands. The line ends at this step.',
}
STATE_ORDER = ['done', 'now', 'take', 'notyet', 'skipped', 'stopped']

# Invented state bills on the neutral topics the guide uses (Illustrative, one label at the head of each piece)
LIST_BILLS = [
    dict(id='H.4212', title='Public meeting notice', states=['done', 'take', 'notyet', 'notyet', 'notyet', 'notyet'],
         line='Testimony is open until March 3.', take='Send written testimony or sign up to speak by March 3.',
         cta='How to send testimony'),
    dict(id='S.0876', title='School bus contracts', states=['done', 'done', 'done', 'now', 'notyet', 'notyet'],
         line='The committee sent it on, and the Senate votes next.'),
    dict(id='H.1180', title='Library hours', states=['done', 'done', 'done', 'done', 'done', 'now'],
         line='Both chambers passed it, and it waits for the governor to sign or veto it.'),
    dict(id='H.3301', title='Records request fees', states=['done', 'skipped', 'done', 'now', 'notyet', 'notyet'],
         line='Step 2 never happened, because the committee voted without holding a hearing. The House votes next.'),
    dict(id='S.2045', title='Parking meter fees', states=['done', 'done', 'done', 'done', 'done', 'stopped'],
         line='The governor vetoed it on February 9, and the Senate’s vote to override fell short on February 23.'),
]
LAW_BILL = dict(id='H.1180', title='Library hours', states=['done'] * 6, law='April 2', line='It takes effect July 1.')
OVERRIDE_BILL = dict(id='S.1517', title='Snow route parking', states=['done'] * 6, law='March 18',
                     how='over the governor’s veto', line='It takes effect June 1.')
STOP_BILL = LIST_BILLS[4]
CARD_BILL = dict(id='S.0412', title='Town audit deadlines', states=['done', 'done', 'done', 'done', 'take', 'notyet'],
                 line='The Senate passed it on February 24, and a House committee holds its hearing on March 10.',
                 take='Send written testimony or sign up to speak by March 10.', cta='How to send testimony')
FED_BILL = dict(id='H.R. 99012', title='Passport wait times', kind='federal',
                states=['done', 'done', 'done', 'done', 'done', 'now'],
                line='Both chambers passed it, and it waits for the President to sign or veto it.')
PAGE_BILL = dict(id='H.4212', title='Public meeting notice', states=LIST_BILLS[0]['states'],
                 dek='The bill would require towns to post notice of a public meeting online two days ahead.')
PAGE_NOTES = [
    'Filed January 16 and sent to the Committee on Local Government.',
    'The committee holds its public hearing on March 3, and testimony is open until then.',
    'The committee votes on whether to send the bill to the full House.',
    'The full House votes on the bill.',
    'The Senate takes it up. Its committee often holds a hearing of its own before both chambers agree on one text.',
    'The governor signs or vetoes the bill. Once it is signed, this page gives the date it became law and the date it '
    'takes effect.',
]


MONTH_DAY = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d)')


def nb(text):
    """Keep a month with its day, a number with its unit and a step with its number on one line."""
    text = MONTH_DAY.sub('\\1' + C.NBSP + '\\2', text)
    text = re.sub(r'(\d) (px|pt)\b', '\\1' + C.NBSP + '\\2', text)
    return re.sub(r'\b([Ss]tep) (\d)', '\\1' + C.NBSP + '\\2', text)


def status_words(b, nm=None):
    nm = nm or names(b.get('kind', 'state'))
    if b.get('law'):
        return f'Became law on {b["law"]}' + (f', {b["how"]}.' if b.get('how') else '.')
    st = b['states']
    if 'stopped' in st:
        i = st.index('stopped')
        return f'Stopped at step {i + 1} of 6: {nm[i]}.'
    i = next(k for k, s in enumerate(st) if s in ('now', 'take'))
    return f'Step {i + 1} of 6: {nm[i]}.'


# ------------------------------------------------------------------------------------------------ marks
# Colors come from the surface through custom properties set once per specimen (see mark_vars()).
MARK_CSS = ('.mk{display:block;overflow:visible;flex:none}'
            '.mk .fi{fill:var(--ink)}.mk .fs{fill:var(--sub)}.mk .fb{fill:var(--bg)}.mk .ft{fill:var(--txt2)}'
            '.mk .fr{fill:var(--red)}.mk .si{stroke:var(--ink)}.mk .ss{stroke:var(--sub)}.mk .sk{stroke:var(--key)}'
            '.mk line,.mk .nf{fill:none}'
            '.mk text{font-family:var(--oa-font-family-reading);font-weight:700;font-variant-numeric:tabular-nums;'
            'text-anchor:middle}'
            '.mk text.tl{font-weight:600}'
            '.mk text.halo{paint-order:stroke;stroke:var(--bg);stroke-width:4px;stroke-linejoin:round}')


def mark_vars(ctx, surf):
    """The colors a mark needs on one surface, read from the surface's tokens."""
    on = {'n': 'onNewsprint', 'c': 'onCharcoal'}[surf]
    v = ctx.v
    return (f'--ink:{v("oa.color.graphic.essential." + on)};--sub:{v("oa.color.graphic.subtle." + on)};'
            f'--bg:{v("oa.color.surface." + ("newsprint" if surf == "n" else "charcoal"))};'
            f'--txt:{v("oa.color.text.primary." + on)};--txt2:{v("oa.color.text.secondary." + on)};'
            f'--hair:{v("oa.color.border.hairline." + on)};--strong:{v("oa.color.border.strong." + on)};'
            f'--red:{v("oa.color.palette.pillarRed")};--key:{v("oa.component.button.ask.keyline.onNewsprint")}')


def svg(w, h, body, scale=1, cls='mk'):
    return (f'<svg class="{cls}" width="{w * scale:g}" height="{h * scale:g}" viewBox="0 0 {w:g} {h:g}" '
            f'aria-hidden="true" focusable="false">{body}</svg>')


def badge(cx, cy, r=5.5, red=True):
    """The take-part mark: an 11 px red disc with a 1 px Charcoal keyline inside its edge (Rule 05.5), cut from the
    ring by 1.5 px of the surface. red=False draws the same disc in the surface ink, for a failure plate."""
    gap = f'<circle cx="{cx:g}" cy="{cy:g}" r="{r + 1.5:g}" class="fb"/>'
    if not red:
        return gap + f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="fi"/>'
    return (gap + f'<g {RED_W}><circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="fr"/>'
            f'<circle cx="{cx:g}" cy="{cy:g}" r="{r - 0.5:g}" class="sk nf" stroke-width="1"/></g>')


def node(cx, cy, d, st, num=None, fs=None):
    """One numbered step (Board 6, Option B): filled when done, a heavy ring now, a fine ring ahead, the fine ring
    under a slash when the step never happened, a filled square where the bill stopped."""
    R = d / 2
    fs = fs or (14 if d >= 28 else 13)
    ty = cy + 0.36 * fs
    t = ''
    if st == 'done':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R:g}" class="fi"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fb" font-size="{fs}">{num}</text>'
    elif st in ('now', 'take'):
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 1.5:g}" class="fb si" stroke-width="3"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fi" font-size="{fs}">{num}</text>'
        if st == 'take':
            t += badge(cx + R * 0.72, cy - R * 0.72, 5.5 if d >= 24 else 4.5)
    elif st == 'notyet':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" class="fb ss" stroke-width="1.5"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="ft tl" font-size="{fs}">{num}</text>'
    elif st == 'skipped':
        k = (R + 2) * 0.7071
        s = (f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" class="fb ss" stroke-width="1.5"/>'
             f'<line x1="{cx - k:.2f}" y1="{cy + k:.2f}" x2="{cx + k:.2f}" y2="{cy - k:.2f}" class="si" stroke-width="2"/>')
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="ft tl halo" font-size="{fs}">{num}</text>'
    elif st == 'stopped':
        s = f'<rect x="{cx - R + 1:g}" y="{cy - R + 1:g}" width="{d - 2:g}" height="{d - 2:g}" class="fi"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fb" font-size="{fs}">{num}</text>'
    else:
        raise ValueError(st)
    return f'<g>{s}{t}</g>'


def line_segments(states, xs, cy, red=False):
    """2 px in the surface ink as far as the bill has come, 1 px Stone ahead, nothing after a stop."""
    out = []
    stop = states.index('stopped') if 'stopped' in states else None
    for i in range(len(xs) - 1):
        if stop is not None and i >= stop:
            break
        if states[i + 1] != 'notyet':
            cls = 'fr' if red else 'fi'
            out.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="2" class="{cls}"/>')
        else:
            out.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="1" class="fs"/>')
    return out


def steps_svg(states, W, d, red_progress=False, fs=None, hang=False):
    """Numbered steps across a row W px wide. Centered: one sixth of the row to each step, so names fit under the
    circles. hang=True: the first circle starts on the text edge and the last ends on the far edge, for rows whose names
    sit in a key. red_progress draws the line and the done steps in Pillar Red, for the failure plate of Rule 11.4 only."""
    if hang:
        c = (W - d) // 5
        xs = [d / 2 + c * i for i in range(6)]
    else:
        c = W // 6
        xs = [c * i + c // 2 for i in range(6)]
    R = d / 2
    cy = 6 + R
    H = int(cy + R + 2)
    segs = line_segments(states, xs, cy, red=red_progress)
    body = [f'<g data-red="working" data-red-job="progress">{x}</g>' if 'class="fr"' in x else x for x in segs]
    for i, (x, s) in enumerate(zip(xs, states)):
        if red_progress and s == 'done':
            body.append(f'<g data-red="working" data-red-job="progress"><circle cx="{x:g}" cy="{cy:g}" r="{R:g}" class="fr"/>'
                        f'<text x="{x:g}" y="{cy + 0.36 * 13:.2f}" class="fi" font-size="13">{i + 1}</text></g>')
        else:
            body.append(node(x, cy, d, s, i + 1, fs))
    return svg(W, H, ''.join(body))


def dots_svg(states, W):
    """Board 6's Option A, for the failure plate of Rule 11.5: unnumbered dots on a line."""
    c = W // 6
    xs = [c * i + c // 2 for i in range(6)]
    cy = 11
    body = line_segments(states, xs, cy)
    for x, s in zip(xs, states):
        if s == 'done':
            body.append(f'<circle cx="{x}" cy="{cy}" r="5" class="fi"/>')
        elif s in ('now', 'take'):
            body.append(f'<circle cx="{x}" cy="{cy}" r="8" class="fb si" stroke-width="2"/>')
            if s == 'take':
                body.append(f'<g {RED_W}><circle cx="{x}" cy="{cy}" r="4" class="fr"/>'
                            f'<circle cx="{x}" cy="{cy}" r="3.5" class="sk nf" stroke-width="1"/></g>')
        else:
            body.append(f'<circle cx="{x}" cy="{cy}" r="4" class="fb ss" stroke-width="1.5"/>')
    return svg(W, 22, ''.join(body))


def sample(st, d=26, scale=1, num=4):
    """One step centered in a square 14 px wider than the circle, which leaves room for the badge."""
    W = d + 14
    return svg(W, W, node(W / 2, W / 2, d, st, num), scale, cls='mk mk-s')


def labels(nm, states, W):
    """Step names under the circles, in the wide form: the current step in bold, a skipped one says so."""
    lis = []
    for i, s in enumerate(states):
        cls = ' class="cur"' if s in ('now', 'take', 'stopped') else ''
        extra = '<span class="lx">never happened</span>' if s == 'skipped' else ''
        lis.append(f'<li{cls}>{nm[i]}{extra}</li>')
    return (f'<ol class="lbls" style="width:{W}px;grid-template-columns:repeat(6,{W // 6}px)">{"".join(lis)}</ol>')


# ------------------------------------------------------------------------------------------------ pieces
def piece_css(ctx, surf, size, sizing='floor'):
    """Styles every tracker piece shares, for a surface ('n', 'c') and a width ('s' 360 px, 'l' 600 px)."""
    T = ctx.ty
    h3 = T('h3', 'ceil' if sizing == 'ceil' else 'floor')
    return (f':scope{{{mark_vars(ctx, surf)}}}' + MARK_CSS +
            f'.pc{{padding:20px 16px 24px;color:var(--txt)}}'
            + ('.pc{padding:24px 24px 28px}' if size == 'l' else '') +
            f':where(.pc p){{margin:0}}'
            f'.hd{{margin:0 0 16px;{h3};text-wrap:balance}}'
            f'.rows{{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}}'
            f'.row{{padding:16px 0 18px;border-bottom:1px solid var(--hair)}}'
            f'.bill{{margin:0 0 12px;{T("body")};line-height:1.35}}.bill b{{font-weight:700}}'
            f'.mkw{{display:flex;justify-content:center}}'
            f'.st{{margin-top:8px;{T("bodySmall")};line-height:1.5;text-wrap:pretty}}.st b{{font-weight:700}}'
            f'.tp{{display:flex;gap:8px;align-items:flex-start;margin-top:8px;{T("bodySmall")};line-height:1.5}}.tp > span{{text-wrap:pretty}}'
            f'.tp .mk{{margin-top:-6px}}.tp b{{font-weight:700}}'
            f'.cta{{display:inline-flex;align-items:center;min-height:{ctx.v("oa.size.target.touch")};{T("ui")};'
            f'text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}}'
            f'.ctaw{{margin:2px 0 -6px}}'
            f'.lbls{{list-style:none;margin:6px 0 0;padding:0;display:grid;{T("dataLabel")};color:var(--txt2);text-align:center}}'
            f'.lbls li{{padding:0 4px}}.lbls li.cur{{color:var(--txt);font-weight:700}}.lbls .lx{{display:block}}'
            f'.key{{margin-top:20px;{T("caption")};color:var(--txt2)}}'
            f'.kh{{{T("label")};color:var(--txt);margin:12px 0 6px}}.kh:first-child{{margin-top:0}}'
            f'.ks{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:2px 14px}}.ks b{{color:var(--txt)}}'
            f'.km{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 18px}}'
            f'.km li{{display:inline-flex;align-items:center;gap:6px}}'
            + ('.mkw{justify-content:flex-start}' if size == 'l' else ''))


def key(nm, show=('done', 'now', 'notyet', 'skipped', 'stopped', 'take'), steps=True):
    k = ''
    if steps:
        k = ('<p class="kh">The six steps</p><ol class="ks">'
             + ''.join(f'<li><b>{i + 1}</b> {n}</li>' for i, n in enumerate(nm)) + '</ol>')
    lis = ''.join(f'<li>{sample(s, 24, num=4)}<span>{STATE_WORD[s]}</span></li>' for s in show)
    return f'<div class="key">{k}<p class="kh">What the marks mean</p><ul class="km">{lis}</ul></div>'


def take_part(b, size='s'):
    if 'take' not in b['states']:
        return ''
    n = b['states'].index('take') + 1
    return (f'<p class="tp">{sample("take", 24, num=n)}<span><b>You can take part now.</b> {b["take"]}</span></p>'
            f'<p class="ctaw"><span class="cta">{b["cta"]}{ARROW}</span></p>')


def row(b, size, nm=None, red_progress=False, step_word=None, kind_label=None):
    nm = nm or names(b.get('kind', 'state'))
    W, d = (328, 26) if size == 's' else (552, 30)
    if size == 'card':
        W, d = 328, 24
    head = (f'<span class="kd">{kind_label}</span> ' if kind_label else '')
    bill = f'<p class="bill">{head}<span><b>Bill {b["id"]}</b>, {b["title"]}</span></p>'
    marks = f'<div class="mkw">{steps_svg(b["states"], W, d, red_progress, hang=(size != "l"))}</div>'
    lab = labels(nm, b['states'], W) if size == 'l' else ''
    sw = step_word or status_words(b, nm)
    st = f'<p class="st"><b>{sw}</b> {b["line"]}</p>'
    core = f'{marks}{lab}{st}{take_part(b, size)}'
    return f'<li class="row">{bill}{core}</li>'


def bill_list(ctx, sid_surf, size, bills, title, nm=None, extra_key=None):
    nm = nm or names()
    show = [s for s in ('done', 'now', 'notyet', 'skipped', 'stopped', 'take')
            if any(s in b['states'] for b in bills) or s in ('done', 'now', 'notyet')]
    rows = ''.join(row(b, size, nm) for b in bills)
    k = key(nm, show, steps=(size == 's'))
    return f'<div class="pc"><p>{ILLUS}</p><p class="hd">{title}</p><ul class="rows">{rows}</ul>{k}</div>'


# ------------------------------------------------------------------------------------------------ specimens
SURF_NAME = {'n': 'newsprint', 'c': 'charcoal'}


def nb_html(html):
    """nb() on the text of a fragment, outside tags and styles."""
    parts = re.split(r'(<style[^>]*>.*?</style>|<[^>]+>)', html, flags=re.S)
    return ''.join(x if x.startswith('<') else nb(x) for x in parts)


def spec(ctx, sid, html, rule, alt, **kw):
    if re.search(r'Stage \d+ of 9|Signal Grid', re.sub(r'<[^>]+>', '', html)):
        raise ValueError(f'{sid}: a retired tracker phrase in a specimen')
    if (kw.get('width') or 0) > 600:
        # CA-M1: the chapter column holds a 606 px stage from a 768 px window up, so no plate is wider than 600 px
        raise ValueError(f'{sid}: wider than 600 px, so it would scroll inside the chapter column at true size')
    return ctx.spec(sid, nb_html(html), CH, rule, alt, **kw)


def alt_list(bills, nm=None):
    out = []
    for b in bills:
        nm2 = nm or names(b.get('kind', 'state'))
        st = '; '.join(f'{i + 1} {nm2[i]} {STATE_WORD[s].lower()}' for i, s in enumerate(b['states']))
        tp = f' You can take part now: {b["take"]}' if 'take' in b['states'] else ''
        out.append(f'Bill {b["id"]}, {b["title"]}: {status_words(b, nm2)} {b["line"]} Steps: {st}.{tp}')
    return ' '.join(out)


def s_steps(ctx):
    rows = ''.join(f'<tr><th scope="row"><span class="n">{i + 1}</span> {n if i < 5 else "Governor or President"}</th>'
                   f'<td>{m if i < 5 else STEP6_BOTH}</td></tr>' for i, (n, m) in enumerate(STEPS))
    T = ctx.ty
    css = (f'table{{width:100%;border-collapse:collapse;{T("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px 16px 12px 0;border-bottom:1px solid '
           f'{ctx.v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{T("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")};border-bottom:2px solid '
           f'{ctx.v("oa.color.border.strong.onNewsprint")}}}'
           f'tbody th{{{T("ui")};width:13rem}}th .n{{display:inline-block;min-width:1.4em;{T("h4")};'
           f'font-variant-numeric:tabular-nums}}td{{max-width:34rem}}'
           f'@container (max-width:30rem){{tbody th{{width:6.5rem;padding-right:12px}}th .n{{display:block}}}}.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr"><table><thead><tr><th scope="col">Step</th>'
            f'<th scope="col">What happens</th></tr></thead><tbody>{rows}</tbody></table></div>')
    alt = ('The six steps, with what happens at each. ' + ' '.join(
        f'{i + 1}, {n if i < 5 else "Governor or President"}: {m if i < 5 else STEP6_BOTH}' for i, (n, m) in enumerate(STEPS)))
    return spec(ctx, 's-11-steps', html, None, alt, readable=True,
                notes='A readable table (D2-255). Step 6 is named for whoever signs (DR-128).')


def s_11_1(ctx):
    """CA-M1: the two forms of step 6 sit one above the other in a 360 px piece, so both names show at true size in
    every chapter column and on a phone. Each bill keeps its own key."""
    T = ctx.ty
    css = piece_css(ctx, 'n', 's') + (f'.kd{{display:block;margin:0 0 4px;{T("label")};color:var(--txt2)}}'
                                      f'.sig{{padding:16px 0 20px;border-bottom:1px solid var(--hair)}}'
                                      f'.sig:first-of-type{{border-top:1px solid var(--hair)}}.sig .key{{margin-top:14px}}'
                                      f'.sig .rows{{border:0}}.sig .row{{padding:0;border:0}}')
    blocks = ''
    for b, label in ((dict(LIST_BILLS[2], kind='state'), 'A state bill'), (FED_BILL, 'A federal bill')):
        nm = names(b.get('kind', 'state'))
        blocks += (f'<div class="sig"><p class="kd">{label}</p><ul class="rows">{row(b, "s", nm)}</ul>'
                   f'{key(nm, ("done", "now"))}</div>')
    html = (f'<style>{css}</style><div class="pc"><p>{ILLUS}</p><p class="hd">Two bills that wait for a signature</p>'
            f'{blocks}</div>')
    alt = ('Two Illustrative bills at 360 px on Newsprint, one above the other, each drawn as six numbered steps with its '
           'own key. A state bill, H.1180, Library hours, has passed steps 1 to 5 and stands at step 6: “Step 6 of 6: '
           'Governor. Both chambers passed it, and it waits for the governor to sign or veto it.” Its key reads 1 Filed, '
           '2 Hearing, 3 Committee vote, 4 First chamber, 5 Second chamber, 6 Governor. A federal bill, H.R. 99012, '
           'Passport wait times, stands at the same place: “Step 6 of 6: President. Both chambers passed it, and it waits '
           'for the President to sign or veto it.” Its key ends 6 President.')
    spec(ctx, 's-11-1-correct', html, '11.1', alt, width=360, illustrative=True)
    fcss, band = ctx.fail_band()
    css2 = piece_css(ctx, 'n', 'l') + fcss
    b = dict(LIST_BILLS[2])
    r = row(b, 'l', nm=CLERK, step_word='Step 6 of 6: Presented.')
    r = r.replace('Both chambers passed it, and it waits for the governor to sign or veto it.',
                  'The enrolled bill went to the executive on February 12.')
    html2 = (f'<style>{css2}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where the library hours bill stands</p>'
             f'<ul class="rows">{r}</ul></div>')
    alt2 = ('Labeled Failure case: do not publish. An Illustrative tracker for bill H.1180, Library hours, whose six '
            'steps take the clerk’s names: Introduced, Referred, Reported, Engrossed, Enrolled and Presented. It reads '
            '“Step 6 of 6: Presented. The enrolled bill went to the executive on February 12.”')
    spec(ctx, 's-11-1-failure', html2, '11.1', alt2, width=600, illustrative=True)

def s_11_2(ctx):
    T = ctx.ty
    css = (f':scope{{{mark_vars(ctx, "n")}}}' + MARK_CSS +
           f'.sk-l{{list-style:none;margin:0;padding:0;display:grid;gap:12px;'
           f'grid-template-columns:repeat(auto-fill,minmax(min(100%,13.5rem),1fr))}}'
           f'.sk-c{{border:1px solid var(--hair);padding:14px 14px 16px}}'
           f'.sk-m{{display:flex;align-items:center;gap:16px;min-height:84px}}'
           f'.sk-n{{margin:8px 0 2px;{T("ui")};font-weight:700}}.sk-t{{margin:0;{T("caption")};color:var(--txt2)}}'
           f'.sk-h{{margin:0 0 12px;{T("caption")};color:var(--txt2)}}')
    cards = ''.join(f'<li class="sk-c"><div class="sk-m" aria-hidden="true">{sample(s, 26)}{sample(s, 26, 2)}</div>'
                    f'<p class="sk-n">{STATE_WORD[s]}</p><p class="sk-t">{STATE_MEANS[s]}</p></li>' for s in STATE_ORDER)
    html = (f'<style>{css}</style><p class="sk-h">Each mark is drawn on step 4, at true size and at twice size.</p>'
            f'<ul class="sk-l">{cards}</ul>')
    alt = ('The six states of a step, each drawn on step 4 at true size and at twice size, with its name and meaning. '
           + ' '.join(f'{STATE_WORD[s]}: {STATE_MEANS[s]}' for s in STATE_ORDER)
           + ' Done is a filled circle; Now is a heavy ring; You can take part now is the heavy ring with a small red '
             'disc at its upper right; Not yet is a fine ring; Never happened is the fine ring under a slash; Stopped is '
             'a filled square.')
    spec(ctx, 's-11-2-correct', html, '11.2', alt, readable=True,
         notes='A readable list (D2-255); the marks are hidden from assistive technology and every state is in words.')

    fcss, band = ctx.fail_band()
    hue = {'done': 'oa.color.palette.verdigris', 'now': 'oa.color.palette.prussian', 'notyet': 'oa.color.palette.stone'}
    st = ['done', 'done', 'done', 'now', 'notyet', 'notyet']
    c = 324 // 6
    xs = [c * i + c // 2 for i in range(6)]
    body = [f'<rect x="{xs[0]}" y="15" width="{xs[-1] - xs[0]}" height="2" style="fill:{ctx.v("oa.color.palette.stone")}"/>']
    for i, (x, s) in enumerate(zip(xs, st)):
        body.append(f'<circle cx="{x}" cy="16" r="13" style="fill:{ctx.v(hue[s])}"/>'
                    f'<text x="{x}" y="20.68" font-size="13" style="fill:{ctx.v("oa.color.palette.white")}">{i + 1}</text>')
    mk = svg(324, 32, ''.join(body))
    css2 = (MARK_CSS + fcss + f'.pr{{display:grid;gap:20px}}.k{{margin:0 0 8px;{T("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")}}}'
            f'.g .mk{{filter:grayscale(1)}}.wr{{padding:4px 16px 20px}}')
    html2 = (f'<style>{css2}</style>{band}<div class="wr"><p style="margin:0 0 16px">{ILLUS}</p><div class="pr">'
             f'<div><p class="k">In color</p>{mk}</div><div class="g"><p class="k">In grayscale</p>{mk}</div></div></div>')
    gv, gs, gp = (C.css_gray(ctx.hx(hue[k])) for k in ('done', 'notyet', 'now'))
    rr = ctx.ratio(gv, gs, 'contrast of Verdigris and Stone in grayscale')
    rh = ctx.ratio('oa.color.palette.verdigris', 'oa.color.palette.stone', 'contrast of Verdigris and Stone')
    ctx.fig('grayscale of Verdigris, Stone and Prussian', f'{gv}, {gs}, {gp}',
            'CSS grayscale(1): 0.2126 R + 0.7152 G + 0.0722 B on the encoded token values')
    alt2 = ('Labeled Failure case: do not publish. An Illustrative row of six identical numbered circles that tell their '
            'states by hue alone: Verdigris for the three done steps, Prussian for step 4, where the bill is now, and '
            f'Stone for steps 5 and 6 ahead, with no word for any state. Below it, the same row in grayscale, where the '
            f'Verdigris and Stone circles print as grays {rr} to 1 apart.')
    spec(ctx, 's-11-2-failure', html2, '11.2', alt2, width=360, illustrative=True,
         notes=f'Verdigris against Stone {rh} to 1 in color; grays {gv} and {gs} measure {rr} to 1.')
    return rr, rh


def s_11_3(ctx):
    css = piece_css(ctx, 'n', 's')
    rows = row(LAW_BILL, 's') + row(OVERRIDE_BILL, 's') + row(STOP_BILL, 's')
    html = (f'<style>{css}</style><div class="pc"><p>{ILLUS}</p><p class="hd">How three state bills ended</p>'
            f'<ul class="rows">{rows}</ul>{key(names(), ("done", "stopped"))}</div>')
    alt = ('Three Illustrative bills at 360 px on Newsprint. Bill H.1180, Library hours: all six numbered steps are '
           'filled, and the words say “Became law on April 2. It takes effect July 1.” Bill S.1517, Snow route parking: '
           'all six steps are filled, and the words say “Became law on March 18, over the governor’s veto. It takes effect '
           'June 1.” Bill S.2045, Parking meter fees: steps 1 to 5 are filled, and step 6 is a filled square where the '
           'line ends. The words say “Stopped at step 6 of 6: Governor. The governor vetoed it on February 9, and the '
           'Senate’s vote to override fell short on February 23.” A key gives the six step names and the Done and Stopped '
           'marks.')
    spec(ctx, 's-11-3-correct', html, '11.3', alt, width=360, illustrative=True)
    fcss, band = ctx.fail_band()
    css2 = piece_css(ctx, 'n', 's') + fcss
    nm = names()[:5] + ['Law']
    r = row(LIST_BILLS[2], 's', nm=nm)
    html2 = (f'<style>{css2}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where the library hours bill stands</p>'
             f'<ul class="rows">{r}</ul>{key(nm, ("done", "now", "notyet"))}</div>')
    alt2 = ('Labeled Failure case: do not publish. An Illustrative tracker for bill H.1180, Library hours, whose sixth step '
            'is named Law. Steps 1 to 5 are filled and step 6 carries the heavy ring, so the words read “Step 6 of 6: Law. '
            'Both chambers passed it, and it waits for the governor to sign or veto it.”')
    spec(ctx, 's-11-3-failure', html2, '11.3', alt2, width=360, illustrative=True)


def card(ctx, red_progress=False):
    T = ctx.ty
    css = piece_css(ctx, 'n', 's') + (f'.cd{{border-top:2px solid var(--strong);padding:16px 0 0}}'
                                      f'.ky{{margin:0;{T("label")};color:var(--txt2)}}'
                                      f'.ch{{margin:8px 0 8px;{T("h4", "floor")};text-wrap:balance}}'
                                      f'.dk{{margin:0 0 16px;{T("body")};text-wrap:pretty}}'
                                      f'.cd .rows{{border:0}}.cd .row{{padding:0;border:0}}')
    b = CARD_BILL
    r = row(b, 'card', red_progress=red_progress)
    html = (f'<div class="pc"><p style="margin-bottom:12px">{ILLUS}</p><div class="cd"><p class="ky">Tracker · State bills</p>'
            f'<p class="ch">The House hears the town audit bill on March 10</p>'
            f'<p class="dk">The bill would move each town’s deadline for its yearly audit from June 30 to September 30.</p>'
            f'<ul class="rows">{r}</ul>{key(names(), ("done", "take", "notyet"))}</div></div>')
    return css, html


def s_11_4(ctx):
    css, html = card(ctx)
    alt = ('An Illustrative story card at 360 px on Newsprint with the kicker Tracker, State bills, the headline “The '
           'House hears the town audit bill on March 10”, and a line on what the bill would do. Under it, bill S.0412, '
           'Town audit deadlines, as six numbered steps: steps 1 to 4 filled, step 5 a heavy ring with a small red disc '
           'at its upper right, step 6 a fine ring. The words say “Step 5 of 6: Second chamber. The Senate passed it on '
           'February 24, and a House committee holds its hearing on March 10.” Beside the same red disc, “You can take '
           'part now. Send written testimony or sign up to speak by March 10.”, then the link How to send testimony.')
    spec(ctx, 's-11-4-correct', f'<style>{css}</style>{html}', '11.4', alt, width=360, illustrative=True)
    fcss, band = ctx.fail_band()
    css2, html2 = card(ctx, red_progress=True)
    alt2 = ('Labeled Failure case: do not publish. The same Illustrative story card, with the line and the four filled '
            'steps drawn in Pillar Red, so red marks how far the bill has come as well as the red disc on step 5 that '
            'says you can take part now.')
    spec(ctx, 's-11-4-failure', f'<style>{css2}{fcss}</style>{band}{html2}', '11.4', alt2, width=360, illustrative=True,
         exempt=['red', 'contrast'],
         notes='Labeled failure: red spent on progress as well as the take-part mark (two red jobs), and numbers on red '
               'fills that pass only as large text.')


def s_11_5(ctx):
    sids = {}
    for surf in ('n', 'c'):
        for size in ('s', 'l'):
            css = piece_css(ctx, surf, size)
            html = f'<style>{css}</style>' + bill_list(ctx, surf, size, LIST_BILLS, 'Where five state bills stand this week')
            w = 360 if size == 's' else 600
            ground = 'Newsprint' if surf == 'n' else 'Charcoal'
            sid = 's-11-5-correct' if (surf, size) == ('n', 's') else f's-11-list-{w}-{SURF_NAME[surf]}'
            where = ('with the step names in a key after the list' if size == 's'
                     else 'with each step’s name under its circle and the bill’s name above its steps')
            alt = (f'An Illustrative list of five state bills at {w:,} px on {ground}, each drawn as six numbered steps on a '
                   f'line, {where}. ' + alt_list(LIST_BILLS))
            spec(ctx, sid, html, '11.5' if sid == 's-11-5-correct' else None, alt, width=w, illustrative=True,
                 surface=SURF_NAME[surf])
            sids[(surf, size)] = sid
    fcss, band = ctx.fail_band()
    css = piece_css(ctx, 'n', 's') + fcss + '.mkw{padding:4px 0}'
    rows = ''
    for b in LIST_BILLS[:2]:
        rows += (f'<li class="row"><p class="bill"><b>Bill {b["id"]}</b>, {b["title"]}</p>'
                 f'<div class="mkw">{dots_svg(b["states"], 324)}</div>'
                 f'<p class="st"><b>{status_words(b)}</b> {b["line"]}</p></li>')
    html = (f'<style>{css}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where two state bills stand this week</p>'
            f'<ul class="rows">{rows}</ul></div>')
    alt = ('Labeled Failure case: do not publish. Two Illustrative bills at 360 px on Newsprint, each drawn as six small '
           'dots on a line with no numbers or names. H.4212’s second dot is a ring with a red center, and S.0876’s fourth '
           'dot is a ring, so a reader counts dots to find the step. The status words sit under each line.')
    spec(ctx, 's-11-5-failure', html, '11.5', alt, width=360, illustrative=True)
    return sids


def timeline(b, d, notes, surf, page=True, generic=False):
    lis = []
    nm = names()
    st = b['states']
    for i, s in enumerate(st):
        seg = 'seg-end' if i == 5 else ('seg-on' if st[i + 1] != 'notyet' else 'seg-off')
        cur = ' cur' if s in ('now', 'take') else ''
        word = 'Now: you can take part' if s == 'take' else STATE_WORD[s]
        box = ''
        if s == 'take' and page:
            box = (f'<div class="tbox"><p class="tp">{sample("take", 24, num=i + 1)}<span><b>You can take part now.</b> '
                   f'Send written testimony or sign up to speak by March 3.</span></p>'
                   f'<p class="askw" {RED_W}><span class="ask">Send testimony</span></p></div>')
        if generic:
            mark = generic_mark(s)
        else:
            mark = sample(s, d, num=i + 1)
        lis.append(f'<li class="{seg}{cur}">{mark}<span class="vt-t"><span class="vt-n">{nm[i]}</span>'
                   + ('' if generic else f'<span class="vt-s">{word}</span>')
                   + (f'<span class="vt-note">{notes[i]}</span>' if notes else '') + f'{box}</span></li>')
    return f'<ol class="vt" style="--d:{d}px">{"".join(lis)}</ol>'


def generic_mark(s):
    """A stock stepper's marks, for the failure plate of Rule 11.6: a check, a dot or an empty box, with no number."""
    if s == 'done':
        body = ('<rect x="7" y="7" width="28" height="28" class="fi"/>'
                '<path d="M14 21.5l5 5 9-10" class="nf" style="stroke:var(--bg)" stroke-width="2.5"/>')
    elif s in ('now', 'take'):
        body = ('<rect x="8" y="8" width="26" height="26" class="fb si" stroke-width="2"/>'
                '<circle cx="21" cy="21" r="5" class="fi"/>')
    else:
        body = '<rect x="8.5" y="8.5" width="25" height="25" class="fb ss" stroke-width="1"/>'
    return svg(42, 42, body, cls='mk mk-s')


def page_css(ctx, surf, size):
    T = ctx.ty
    on = {'n': 'onNewsprint', 'c': 'onCharcoal'}[surf]
    keyline = (f';box-shadow:inset 0 0 0 1px {ctx.v("oa.component.button.ask.keyline.onNewsprint")}' if surf == 'n' else '')
    return (piece_css(ctx, surf, size) +
            f'.chip{{display:inline-flex;{T("dataLabel")};border:1px solid var(--strong);vertical-align:middle}}'
            f'.chip span{{padding:4px 6px}}.chip span:first-child{{background:var(--ink);color:var(--bg)}}'
            f'.ky{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:12px 0 12px;{T("label")};color:var(--txt2)}}'
            f'.hd{{margin:0 0 8px}}'
            f'.dk{{margin:0 0 12px;{T("body")};text-wrap:pretty}}'
            f'.pg > .st{{margin:0 0 20px;padding-bottom:16px;border-bottom:1px solid var(--hair)}}'
            f'.vt{{list-style:none;margin:0;padding:0}}'
            f'.vt li{{position:relative;display:grid;grid-template-columns:calc(var(--d) + 14px) minmax(0,1fr);column-gap:6px;'
            f'padding-bottom:14px;min-height:calc(var(--d) + 14px)}}'
            f'.vt li::after{{content:"";position:absolute;left:calc(var(--d) / 2 + 6px);width:2px;top:calc(var(--d) + 7px);'
            f'bottom:-7px;background:var(--ink)}}'
            f'.vt li.seg-off::after{{width:1px;left:calc(var(--d) / 2 + 6.5px);background:var(--sub)}}'
            f'.vt li.seg-end::after{{display:none}}'
            f'.vt-t{{padding-top:calc(var(--d) / 2 - 5px);display:flex;flex-direction:column;min-width:0}}'
            f'.vt-n{{{T("body")};font-weight:600;line-height:1.35}}.vt li.cur .vt-n{{font-weight:700}}'
            f'.vt-s{{{T("label")};color:var(--txt2)}}.vt li.cur .vt-s{{color:var(--txt)}}'
            f'.vt-note{{{T("bodySmall")};line-height:1.5;margin-top:2px;text-wrap:pretty}}'
            f'.tbox{{margin:12px 0 4px;padding:14px;border:2px solid var(--strong)}}.tbox .tp{{margin:0 0 12px}}'
            f'.askw{{margin:0}}'
            f'.ask{{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;'
            f'background:{ctx.v("oa.component.button.ask.fill." + on)};color:{ctx.v("oa.component.button.ask.label." + on)};'
            f'{T("ask")}{keyline}}}'
            f'.aside{{{T("caption")};border-top:2px solid var(--strong);padding-top:12px;margin-top:12px}}'
            f'.aside ol{{margin:0;padding:0;list-style:none}}.aside li{{margin:0 0 8px}}.aside b{{font-weight:700}}')


def bill_page(ctx, surf, size, generic=False):
    b = PAGE_BILL
    tl = timeline(b, 28, PAGE_NOTES if not generic else None, surf, page=not generic, generic=generic)
    head = (f'<p>{ILLUS}</p><p class="ky"><span>Tracker · State bills</span>'
            f'<span class="chip"><span>Bill</span><span>H.4212</span></span></p>'
            f'<p class="hd">Public meeting notice</p><p class="dk">{b["dek"]}</p>'
            + ('' if generic else f'<p class="st"><b>{status_words(b)}</b> Testimony is open until March 3.</p>'))
    if size == 'l':
        aside = ('<div class="aside"><p class="kh">What the six steps mean</p><ol>'
                 + ''.join(f'<li><b>{i + 1} {n}.</b> {m}</li>' for i, (n, m) in enumerate(STEPS)) + '</ol></div>')
        body = f'{tl}{aside}'
    else:
        body = tl
    return f'<div class="pc pg">{head}{body}</div>'


def s_11_6(ctx):
    sids = {}
    for surf, size in (('n', 's'), ('n', 'l'), ('c', 's')):
        w = 360 if size == 's' else 600
        ground = 'Newsprint' if surf == 'n' else 'Charcoal'
        html = f'<style>{page_css(ctx, surf, size)}</style>{bill_page(ctx, surf, size)}'
        sid = 's-11-6-correct' if (surf, size) == ('n', 's') else f's-11-page-{w}-{SURF_NAME[surf]}'
        aside = (' After the steps, a key says what each of the six steps means.' if size == 'l' else '')
        alt = (f'An Illustrative page for one bill at {w:,} px on {ground}: the kicker Tracker, State bills, the ID Bill '
               f'H.4212, the title Public meeting notice and a line on what the bill would do, then “Step 2 of 6: Hearing. '
               f'Testimony is open until March 3.” The six numbered steps run down the page on a line, each with its name, '
               f'its state in words and a note: 1 Filed, done, filed January 16 and sent to the Committee on Local '
               f'Government; 2 Hearing, now, you can take part, with a red disc on its ring and a box holding “You can take '
               f'part now. Send written testimony or sign up to speak by March 3.” and a red Send testimony button; 3 '
               f'Committee vote, 4 First chamber, 5 Second chamber and 6 Governor, each not yet, with a note on what '
               f'happens there. Step 5’s note says the Senate’s committee often holds a hearing of its own.' + aside)
        spec(ctx, sid, html, '11.6' if sid == 's-11-6-correct' else None, alt, width=w, illustrative=True,
             surface=SURF_NAME[surf])
        sids[(surf, size)] = sid
    fcss, band = ctx.fail_band()
    html = f'<style>{page_css(ctx, "n", "s")}{fcss}</style>{band}{bill_page(ctx, "n", "s", generic=True)}'
    alt = ('Labeled Failure case: do not publish. The same Illustrative page for bill H.4212, Public meeting notice, with '
           'a stock stepper in place of the numbered steps: a filled box with a check for step 1, a box with a dot for '
           'step 2 and empty boxes for steps 3 to 6, with no numbers, no state in words and no way to take part.')
    spec(ctx, 's-11-6-failure', html, '11.6', alt, width=360, illustrative=True)
    return sids


def s_11_7(ctx):
    T = ctx.ty
    css = (f':scope{{{mark_vars(ctx, "n")}}}' + MARK_CSS +
           f'.sz{{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}}'
           f'.sz li{{display:grid;grid-template-columns:minmax(0,12rem) minmax(0,1fr);gap:8px 24px;align-items:center;'
           f'padding:12px 0;border-bottom:1px solid var(--hair)}}'
           f'.sz-m{{display:flex;align-items:center;gap:4px}}'
           f'.sz-n{{margin:0;{T("ui")}}}.sz-t{{margin:2px 0 0;{T("caption")};color:var(--txt2)}}'
           f'.tg{{display:flex;flex-wrap:wrap;gap:24px 40px;margin-top:24px;align-items:flex-end}}'
           f'.tgi{{display:flex;align-items:stretch;gap:10px}}'
           f'.dim{{position:relative;width:12px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}}'
           f'.dim::before{{content:"";position:absolute;left:5px;top:0;bottom:0;border-left:1px solid var(--ink)}}'
           f'.dv{{display:flex;flex-direction:column;justify-content:center;{T("dataLabel")}}}'
           f'.cta{{display:inline-flex;align-items:center;min-height:{ctx.v("oa.size.target.touch")};{T("ui")};'
           f'text-decoration:underline;text-underline-offset:3px;outline:1px dashed var(--sub);outline-offset:0}}'
           f'.ask{{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;'
           f'background:{ctx.v("oa.component.button.ask.fill.onNewsprint")};color:{ctx.v("oa.component.button.ask.label.onNewsprint")};'
           f'{T("ask")};box-shadow:inset 0 0 0 1px {ctx.v("oa.component.button.ask.keyline.onNewsprint")}}}'
           f'@container (max-width:30rem){{.sz li{{grid-template-columns:1fr}}}}.wr{{container-type:inline-size}}')
    sizes = [(24, 13, 'On a story card', '24 px circles, numbers at 13 px'),
             (26, 13, 'In a list at 360 px', '26 px circles, numbers at 13 px'),
             (28, 14, 'On a bill’s own page', '28 px circles, numbers at 14 px'),
             (30, 14, 'In a wide list', '30 px circles, numbers at 14 px')]
    lis = ''
    for d, fs, where, what in sizes:
        marks = ''.join(svg(d + 14, d + 14, node((d + 14) / 2, (d + 14) / 2, d, s, n, fs), cls='mk mk-s')
                        for s, n in (('done', 1), ('take', 2), ('notyet', 3)))
        lis += (f'<li><div class="sz-m" aria-hidden="true">{marks}</div><div><p class="sz-n">{where}</p>'
                f'<p class="sz-t">{what}</p></div></li>')
    tg = (f'<div class="tg"><div class="tgi"><span class="dim" aria-hidden="true"></span><div><span class="cta">How to send '
          f'testimony{ARROW}</span></div><span class="dv">44 px tall</span></div>'
          f'<div class="tgi"><span class="dim" aria-hidden="true"></span><div {RED_W}><span class="ask">Send testimony</span></div>'
          f'<span class="dv">48 px tall</span></div></div>')
    html = f'<style>{css}</style><div class="wr"><ul class="sz">{lis}</ul>{tg}</div>'
    alt = ('The tracker’s four sizes at true size, each drawn as a done step, a step where you can take part and a step '
           'ahead: 24 px circles with 13 px numbers on a story card, 26 px with 13 px numbers in a list at 360 px, 28 px '
           'with 14 px numbers on a bill’s own page and 30 px with 14 px numbers in a wide list. Below them, the '
           'link How to send testimony with a bracket marking it 44 px tall, and the red Send testimony button marked '
           '48 px tall.')
    spec(ctx, 's-11-7-correct', html, '11.7', alt, readable=True,
         notes='A readable list (D2-255). Circle sizes and number sizes are the ones every tracker plate in this chapter draws.')
    fcss, band = ctx.fail_band()
    b = LIST_BILLS[0]
    small = steps_svg(b['states'], 324, 16, fs=9)
    css2 = (piece_css(ctx, 'n', 's') + fcss +
            '.tiny{display:inline-block;font-size:0.6875rem;line-height:20px;text-decoration:underline;outline:1px dashed var(--sub)}')
    html2 = (f'<style>{css2}</style>{band}<div class="pc"><p>{ILLUS}</p><ul class="rows"><li class="row">'
             f'<p class="bill"><b>Bill {b["id"]}</b>, {b["title"]}</p><div class="mkw">{small}</div>'
             f'<p class="st"><b>{status_words(b)}</b> {b["line"]}</p>'
             f'<p class="tp"><span class="tiny">Send testimony</span></p></li></ul></div>')
    alt2 = ('Labeled Failure case: do not publish. An Illustrative tracker for bill H.4212 drawn with 16 px circles and '
            'numbers 9 px tall, and a Send testimony link 20 px tall in 11 px type, marked with a dashed outline.')
    spec(ctx, 's-11-7-failure', html2, '11.7', alt2, width=360, illustrative=True, exempt=['size', 'scale'],
         notes='Labeled failure: numbers at 9 px and a link at 11 px, off the scale on purpose and under the 13 px floor.')


# ------------------------------------------------------------------------------------------------ chapter
def build(ctx):
    s_steps(ctx)
    s_11_1(ctx)
    rr, rh = s_11_2(ctx)
    s_11_3(ctx)
    s_11_4(ctx)
    lists = s_11_5(ctx)
    pages = s_11_6(ctx)
    s_11_7(ctx)

    r = ctx.ratio
    ink_n = r('oa.color.graphic.essential.onNewsprint', 'oa.color.surface.newsprint')
    sub_n = r('oa.color.graphic.subtle.onNewsprint', 'oa.color.surface.newsprint')
    ink_c = r('oa.color.graphic.essential.onCharcoal', 'oa.color.surface.charcoal')
    sub_c = r('oa.color.graphic.subtle.onCharcoal', 'oa.color.surface.charcoal')
    t2_n = r('oa.color.text.secondary.onNewsprint', 'oa.color.surface.newsprint')
    t2_c = r('oa.color.text.secondary.onCharcoal', 'oa.color.surface.charcoal')
    red_n = r('oa.color.palette.pillarRed', 'oa.color.surface.newsprint')
    red_c = r('oa.color.palette.pillarRed', 'oa.color.surface.charcoal')
    key_n = r('oa.component.button.ask.keyline.onNewsprint', 'oa.color.surface.newsprint')
    ask = r('oa.component.button.ask.label.onNewsprint', 'oa.component.button.ask.fill.onNewsprint')
    touch = int(ctx.T.px('oa.size.target.touch'))
    minimum = int(ctx.T.px('oa.size.target.minimum'))
    ctx.fig('target sizes', f'{touch} and {minimum} px', 'oa.size.target.touch and oa.size.target.minimum in tokens.json')

    rules = [
        {
            'id': '11.1', 'title': 'Follow every bill through six numbered steps with plain names.',
            'rule': ['A tracker follows a bill through six steps, numbered 1 to 6: Filed, Hearing, Committee vote, First '
                     'chamber, Second chamber, and a sixth named for whoever signs the bill, Governor on a state bill and '
                     'President on a federal one. A chamber is one house of a legislature, such as the House or the Senate, '
                     'and the first chamber is the one where the bill was filed. Every tracker prints the number and the name '
                     'together, as in “Step 2 of 6: Hearing”, for the step the bill is at now.',
                     'Six steps fold some procedure together, such as a second reading or a conference committee, where '
                     'members of both chambers settle one text. A bill’s own page gives those dates in the note under the '
                     'step they belong to.'],
            'tokens': ['oa.type.dataLabel', 'oa.type.bodySmall'],
            'why': {'text': ['A number gives a reader words to say, “step 2 of 6”, with no key to learn, and it reads the '
                             'same on a phone and in gray print. Plain names let a newcomer say what happens at each step. '
                             'The hearing keeps a step of its own because it is where a committee takes testimony on the '
                             'bill, from the public in many state legislatures and from the witnesses it invites in '
                             'Congress. Naming step 6 for the person who signs keeps a bill that waits for a signature from '
                             'reading as law.'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-1-correct',
                        'caption': 'Two bills at 360 px, both at step 6, each with its own key. The state bill’s sixth '
                                   'step is Governor, and the federal bill’s is President; the other five names stay the '
                                   'same.'},
            'failure': {'specimen': 's-11-1-failure',
                        'caption': '<strong>Fails Rule 11.1.</strong> The steps take the clerk’s names. A newcomer cannot '
                                   'say what Engrossed or Enrolled means, so the tracker needs a glossary before it tells '
                                   'anyone where the bill stands.'},
            'specs': [
                {'label': 'Steps', 'value': '1 Filed, 2 Hearing, 3 Committee vote, 4 First chamber, 5 Second chamber, 6 '
                                            'the signer'},
                {'label': 'Step 6', 'value': 'Governor on a state bill; President on a federal bill'},
                {'label': 'Status words', 'value': '“Step 2 of 6: Hearing.”, in bold, for the step the bill is at now, '
                                                   'then one plain sentence', 'token': 'oa.type.bodySmall'},
                {'label': 'Step names under the circles', 'value': 'In a list column 552 px wide or more, Inter 600 '
                                                                   'at 13 px, the current step in bold',
                 'token': 'oa.type.dataLabel'},
            ],
            'related': ['01', '18'],
            'builders': ['Write the status words from the data, never from the drawing: the step number, its name for '
                         'this bill’s route and one sentence on what happens next. Store step 6 as the signer, so a state '
                         'bill prints Governor and a federal bill prints President.',
                         'Number an invented federal bill from H.R. 99001 up, far past any number a Congress has used, and '
                         'label it Illustrative. A cropped plate then cannot put our status words on a real bill.'],
        },
        {
            'id': '11.2', 'title': 'Draw each step’s state as a shape, and say it in words.',
            'rule': ['Each step shows its state by its shape, and the words beside the tracker say the same thing. Done '
                     'steps fill in, the step a bill is at now takes a heavy ring, and steps ahead keep a fine one. A step '
                     'that never happened, such as a hearing the committee skipped, keeps its number under a slash, so the '
                     'count still runs to six. When a bill stops, its line ends on a filled square at that step.'],
            'tokens': ['oa.color.graphic.essential.onNewsprint', 'oa.color.graphic.subtle.onNewsprint',
                       'oa.color.text.secondary.onNewsprint', 'oa.color.graphic.essential.onCharcoal',
                       'oa.color.graphic.subtle.onCharcoal'],
            'why': {'text': ['A shape holds up in gray print, in bright sun and for the many readers who cannot tell red '
                             'from green. The words carry the state to a screen reader and to anyone unsure of a mark. '
                             'Each mark but the take-part disc draws in the surface’s ink, Charcoal on Newsprint and '
                             'Newsprint on Charcoal, so a tracker reads the same on either ground.'],
                    'basis': 'WCAG 2.2 SC 1.4.1 and 1.4.11; design judgment'},
            'correct': {'specimen': 's-11-2-correct',
                        'caption': 'The six states, each drawn on step 4 at true size and twice size. Each one changes the '
                                   'shape, so the set reads in grayscale.'},
            'failure': {'specimen': 's-11-2-failure',
                        'caption': f'<strong>Fails 1.4.1.</strong> Six identical circles tell their states by hue alone. '
                                   f'In grayscale, the done steps in Verdigris and the steps ahead in Stone print as grays '
                                   f'{rr} to 1 apart, and no word says where the bill stands.'},
            'specs': [
                {'label': 'Done', 'value': 'A filled circle, its number in the surface color'},
                {'label': 'Now', 'value': 'A ring with a 3 px line, its number in bold'},
                {'label': 'Not yet', 'value': 'A ring with a 1.5 px line, its number in Inter 600 in the secondary text color'},
                {'label': 'Never happened', 'value': 'The Not yet ring under a 2 px slash, its number kept clear by a 2 px '
                                                     'halo in the surface color'},
                {'label': 'Stopped', 'value': 'A filled square in place of the circle; the line ends there'},
                {'label': 'Marks on Newsprint', 'value': f'Charcoal {ink_n} to 1, Stone {sub_n} to 1',
                 'token': 'oa.color.graphic.subtle.onNewsprint'},
                {'label': 'Marks on Charcoal', 'value': f'Newsprint {ink_c} to 1, Dim Newsprint {sub_c} to 1',
                 'token': 'oa.color.graphic.subtle.onCharcoal'},
                {'label': 'Numbers ahead', 'value': f'Deep Stone {t2_n} to 1 on Newsprint, Dim Newsprint {t2_c} to 1 on '
                                                    f'Charcoal', 'token': 'oa.color.text.secondary.onNewsprint'},
            ],
            'related': ['05', '17'],
            'builders': ['Draw each tracker as one SVG with <code>aria-hidden="true"</code>, and give screen readers an '
                         'ordered list of the six steps beside it, each with its state in words, such as “Step 2, '
                         'Hearing: never happened.” Hide that list visually and keep it in the reading order.',
                         'A hearing on the bill’s subject held before the bill was filed does not fill step 2; the step’s '
                         'note names it.'],
        },
        {
            'id': '11.3', 'title': 'Say in words when a bill becomes law or stops.',
            'rule': ['Step 6 keeps the signer’s name while a bill waits, so a bill there reads “Step 6 of 6: Governor”. '
                     'Once it becomes law, all six steps fill and the words say “Became law on” with the date, then when it '
                     'takes effect, as in “Became law on April 2. It takes effect July 1.” A bill can become law by '
                     'signature, by a vote to override a veto, or without a signature where the constitution allows it. '
                     'When it was not signed, the words say how, as in “Became law on March 18, over the governor’s veto.”',
                     'A bill that stops ends its line on a square at the step where it stopped, and the words give the '
                     'date and the reason. A veto that stands stops a bill at step 6.'],
            'why': {'text': ['A reader who sees the last step filled can take the bill for law, so only the words can '
                             'say when the signature came and when the law applies. The date it takes effect is the one '
                             'most readers act on.'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-3-correct',
                        'caption': 'Three ends at 360 px. H.1180 became law when it was signed, and S.1517 over a veto; '
                                   'the words of each say how and when. S.2045 stopped at step 6 when a veto stood, and its '
                                   'line ends on the square.'},
            'failure': {'specimen': 's-11-3-failure',
                        'caption': '<strong>Fails Rule 11.3.</strong> The sixth step is named Law, so a bill that still '
                                   'waits for the governor reads “Step 6 of 6: Law.” A reader may stop following it '
                                   'before a veto.'},
            'specs': [
                {'label': 'Waiting to be signed', 'value': '“Step 6 of 6: Governor.” or “Step 6 of 6: President.”'},
                {'label': 'Signed', 'value': 'All six steps filled; “Became law on April 2. It takes effect July 1.”'},
                {'label': 'Over a veto', 'value': 'All six steps filled; “Became law on March 18, over the governor’s veto.”'},
                {'label': 'Without a signature', 'value': 'All six steps filled; “Became law on May 4, without the governor’s '
                                                          'signature.”, where the constitution allows it'},
                {'label': 'Stopped', 'value': 'A square at the last step reached; “Stopped at step 3 of 6: Committee '
                                              'vote.” with the date and the reason'},
                {'label': 'A veto that stands', 'value': 'Stopped at step 6'},
            ],
            'related': ['02', '13'],
            'builders': ['Keep two dates in a bill’s record once it is signed: the day it was signed and the day it takes '
                         'effect, written in the past tense once that day has passed. Print “Became law on” '
                         'only from the signed date.'],
        },
        {
            'id': '11.4', 'title': 'Mark the one way to take part in red, on its own shape, beside its words.',
            'rule': ['When the public can act on a bill before a date, the step it is at takes the take-part mark: a '
                     'small red disc at the upper right of its ring, with a 1 px Charcoal keyline inside the disc’s edge. '
                     'The words “You can take part now” sit beside it, with the deadline and the way to act. It is the '
                     'view’s one working red (Rule 05.3), and it can sit on any step where the public can take part, '
                     'such as a hearing in the second chamber at step 5. Every other state stays in the surface’s ink.'],
            'tokens': ['oa.color.palette.pillarRed', 'oa.component.button.ask.keyline.onNewsprint'],
            'why': {'text': ['Red catches the eye first, so it goes to the one thing a reader can do. The disc changes '
                             'the ring’s outline, so the mark still reads in gray print, and the words say what to do for '
                             f'anyone who cannot see red. On Newsprint, Pillar Red measures {red_n} to 1, under the 3 to 1 a '
                             f'mark needs, and the keyline gives it an edge at {key_n} to 1.'],
                    'basis': 'Rule 05.3; WCAG 2.2 SC 1.4.1 and 1.4.11'},
            'correct': {'specimen': 's-11-4-correct',
                        'caption': 'A story card at 360 px. The House committee holds its own hearing at step 5, so the '
                                   'take-part mark sits there, beside its words and the link to act.'},
            'failure': {'specimen': 's-11-4-failure',
                        'caption': '<strong>Fails Rules 11.4 and 05.3.</strong> Red also fills the steps the bill has '
                                   'passed, so it does two jobs and the one way to take part no longer stands out.'},
            'specs': [
                {'label': 'Take-part mark', 'value': 'An 11 px Pillar Red disc at the upper right of the Now ring, a '
                                                     '1 px Charcoal keyline inside its edge, 1.5 px of the surface around it',
                 'token': 'oa.color.palette.pillarRed'},
                {'label': 'Contrast', 'value': f'Pillar Red {red_n} to 1 on Newsprint with the keyline at {key_n}; '
                                               f'{red_c} to 1 on Charcoal', 'token': 'oa.component.button.ask.keyline.onNewsprint'},
                {'label': 'Words', 'value': '“You can take part now.” in bold, then the deadline and how to act'},
                {'label': 'In a list, or on a card with this mark', 'value': 'A text link at least 44 px tall; the red '
                                                                            'button waits for the bill’s own page',
                 'token': 'oa.size.target.touch'},
                {'label': 'On a card without this mark', 'value': 'The card may end on the red ask, as the pillar cards in '
                                                                  'chapter 01 do'},
                {'label': 'Red jobs in a view', 'value': 'One: take part now. Every take-part mark and the ask button '
                                                         'share it'},
            ],
            'related': ['05', '18'],
            'builders': ['Mark the disc and the ask button with <code>data-red="working"</code> and '
                         '<code>data-red-job="take part now"</code>, so the shared check counts one red job. The words '
                         'carry the meaning, so the disc stays hidden from screen readers.'],
        },
        {
            'id': '11.5', 'title': 'Use numbered steps in lists and on story cards.',
            'rule': ['In a list of bills and on a story card, the tracker runs across the page: six numbered circles on '
                     'one line, solid as far as the bill has come and fine after it. The bill’s number and name lead each '
                     'row, and its status words follow the marks. In a column narrower than 552 px, as on a phone, the '
                     'first circle starts on the text edge and the step names move into a key after the list. In a wider '
                     'column, each step takes a sixth of the row and its name sits under its circle.'],
            'tokens': ['oa.border.width.rule', 'oa.border.width.hairline', 'oa.type.dataLabel'],
            'why': {'text': ['A list asks a reader to compare bills at a glance, and six numbered steps fit across a '
                             '360 px phone with room for the words. The numbers also keep the tracker apart from the '
                             'lockmark, the small grid of lines and nodes that marks our pages and codes nothing '
                             '(chapter 08).'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-5-correct',
                        'caption': 'Five bills at 360 px on Newsprint, among them one where you can take part, one waiting for the '
                                   'governor, one whose hearing never happened and one stopped by a veto.'},
            'failure': {'specimen': 's-11-5-failure',
                        'caption': '<strong>Fails Rule 11.5.</strong> Dots on a line carry no numbers or names, so a reader '
                                   'counts dots to find the step, and a row of nodes on a line comes close to the '
                                   'lockmark’s drawing.'},
            'specs': [
                {'label': 'Circles', 'value': '26 px in a phone list, 30 px in a wide list, 24 px on a story card'},
                {'label': 'Line', 'value': '2 px in the surface’s ink as far as the bill has come, 1 px after it',
                 'token': 'oa.border.width.rule'},
                {'label': 'Spacing', 'value': 'Phone list and card: first circle on the text edge, last on the far '
                                              'edge, 60 px apart in a 328 px row. Wide list: one sixth of a 552 px row '
                                              'to each step, 92 px'},
                {'label': 'Step names', 'value': 'Under the circles in a column 552 px wide or more; in the key below '
                                                 'that',
                 'token': 'oa.type.dataLabel'},
                {'label': 'Key', 'value': 'After the last bill: the six steps on phones, and every mark the list uses'},
            ],
            'related': ['07', '08'],
            'builders': ['Mark up the list as a <code>&lt;ul&gt;</code> of bills, each holding its hidden step list from '
                         'Rule 11.2. Switch to the wide form with a container query on the list’s own width, '
                         '<code>@container (min-width: 34.5rem)</code>, so a list in a narrow column keeps its key at any '
                         'window size. When a tracker updates in place, announce the new status words through a polite '
                         'live region, as chapter 18 sets out.'],
        },
        {
            'id': '11.6', 'title': 'Turn the same steps upright on a bill’s own page.',
            'rule': ['A bill’s own page runs the six steps down the page, with the marks a list uses. Each step gives its '
                     'name, its state in words and a note with its dates. Under the step where the public can act, a box '
                     'holds the deadline and the page’s one red button, the ask. Where the page has room, a key after '
                     'the steps says what each one means.'],
            'tokens': ['oa.component.button.ask.fill.onNewsprint', 'oa.component.button.ask.label.onNewsprint', 'oa.type.ask'],
            'why': {'text': ['A bill’s page has room for the dates and notes a list leaves out, and a reader who knows the '
                             'marks from a list knows them here. The ask sits under the step it belongs to, where the '
                             'reader learns why the date matters.'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-6-correct',
                        'caption': 'H.4212’s page at 360 px. Step 2 holds the way to take part, and step 5’s note says the '
                                   'Senate’s committee often holds a hearing of its own.'},
            'failure': {'specimen': 's-11-6-failure',
                        'caption': '<strong>Fails Rule 11.6.</strong> A stock stepper draws checks and boxes with no '
                                   'numbers, so a reader who learned the steps in a list has to learn a second set.'},
            'specs': [
                {'label': 'Circles', 'value': '28 px with 14 px numbers'},
                {'label': 'Line', 'value': '2 px down the page as far as the bill has come, 1 px after it'},
                {'label': 'Each step', 'value': 'Name in Inter 600 at 17 px, the state in label type, a note at 15 px'},
                {'label': 'Ask button', 'value': f'Inter 700 at 19 px, White on Pillar Red at {ask} to 1, 48 px tall',
                 'token': 'oa.type.ask'},
                {'label': 'Key of meanings', 'value': 'After the steps, in a column 600 px wide or more'},
            ],
            'related': ['18', '20'],
            'builders': ['Mark up the steps as an <code>&lt;ol&gt;</code>, one item for each step, with the state in its '
                         'text. Make the ask a link to the way to take part, styled as the ask button.'],
        },
        {
            'id': '11.7', 'title': 'Size the marks for reading, and the targets for a thumb.',
            'rule': ['Draw the circles at 24 px on a story card, 26 px in a phone list, 28 px on a bill’s page and '
                     '30 px in a wide list. Numbers sit at 13 px in circles under 28 px and at 14 px from 28 px. '
                     f'Every link and button a reader can press stands at least {touch} px tall, and the ask button 48 px.'],
            'tokens': ['oa.size.target.touch', 'oa.size.target.minimum'],
            'why': {'text': ['Numbers at 13 px keep the type floor of Rule 06.3 inside the mark. A target 44 px tall '
                             f'clears the {minimum} px minimum in WCAG 2.2 with room for a thumb, and matches our touch '
                             'target token.'],
                    'basis': 'WCAG 2.2 SC 2.5.8; Rule 06.3'},
            'correct': {'specimen': 's-11-7-correct',
                        'caption': 'The four circle sizes at true size, and the two targets with their heights marked.'},
            'failure': {'specimen': 's-11-7-failure',
                        'caption': '<strong>Fails Rules 11.7 and 06.3.</strong> Circles at 16 px force numbers down to 9 px, '
                                   'and the link stands 20 px tall, under the 24 px minimum.'},
            'specs': [
                {'label': 'Circles', 'value': '24, 26, 28 and 30 px, by place'},
                {'label': 'Numbers', 'value': 'Inter 700 at 13 px, or 14 px in circles of 28 px and up; tabular figures'},
                {'label': 'Links and buttons', 'value': f'At least {touch} px tall', 'token': 'oa.size.target.touch'},
                {'label': 'Smallest target anywhere', 'value': f'{minimum} by {minimum} px', 'token': 'oa.size.target.minimum'},
                {'label': 'Ask button', 'value': '48 px tall'},
            ],
            'related': ['06', '19'],
            'builders': [f'Set <code>min-height: var(--oa-size-target-touch)</code> on every link in a tracker, and give a '
                         f'link that sits inline at least {minimum} px of space around it.'],
        },
    ]

    ch = {
        'number': CH, 'anchor': 'icons', 'title': 'Status and utility icons', 'part': 'Symbols and graphics',
        'instruction': 'Give each record state or interface action a glyph and a word that read without color.',
        'intro': [
            'A glyph here is a small drawn mark, and each one carries its meaning twice, in its shape and in the word '
            'beside it. A reader who sees no color, or prints the page in gray, gets the same meaning as everyone else.',
            'It opens with trackers, which show how far a bill has come in six numbered steps. Status marks for other '
            'records, such as a records request or an agency rule, join the chapter as rule groups of their own once we '
            'draw them, and so do utility icons for actions such as copy, filter and share.',
        ],
        'groups': [{'before_rule': '11.1', 'number': 1, 'title': 'Trackers',
                    'line': 'A tracker shows where a bill stands in six numbered steps, with each step’s state drawn as a '
                            'shape and said in words.'}],
        'rules': rules,
        'extras': [
            {'after_rule': '11.1', 'specimen': 's-11-steps', 'label': 'The six steps',
             'caption': 'What happens at each step. Step 6 takes the name of whoever signs the bill.'},
            {'after_rule': '11.5', 'specimen': lists[('c', 's')], 'label': 'Numbered steps at 360 px on Charcoal',
             'caption': 'The same five bills on Charcoal. The marks turn to Newsprint and Dim Newsprint, and the take-part disc keeps its red.'},
            {'after_rule': '11.5', 'specimen': lists[('n', 'l')], 'label': 'Numbered steps in a 600 px column on Newsprint',
             'caption': 'The wide form, as on a tablet or in a desktop article column. Each step’s name sits under its '
                        'circle, and the current step’s name is bold.'},
            {'after_rule': '11.5', 'specimen': lists[('c', 'l')], 'label': 'Numbered steps in a 600 px column on Charcoal',
             'caption': 'The same wide list on Charcoal.'},
            {'after_rule': '11.6', 'specimen': pages[('n', 'l')], 'label': 'A bill’s page in a 600 px column on Newsprint',
             'caption': 'The steps run the width of the column, and a key after them says what each step means.'},
            {'after_rule': '11.6', 'specimen': pages[('c', 's')], 'label': 'A bill’s page at 360 px on Charcoal',
             'caption': 'The same page on Charcoal. The ask button keeps its red, which measures '
                        f'{red_c} to 1 on Charcoal and needs no keyline there.'},
        ],
        'related_chapters': [
            {'chapter': '05', 'reason': 'One working red in each view, and states that read without color.'},
            {'chapter': '06', 'reason': 'The 13 px floor and tabular figures.'},
            {'chapter': '08', 'reason': 'The lockmark, which keeps its fixed places and codes nothing.'},
            {'chapter': '17', 'reason': 'Loading, empty and error states for a live tracker.'},
            {'chapter': '18', 'reason': 'How a live tracker announces a change.'},
            {'chapter': '19', 'reason': 'Checking a tracker against WCAG 2.2 AA.'},
        ],
    }
    return ch


def nb_walk(o, key=None):
    if isinstance(o, str):
        return o if key in ('specimen', 'token', 'id', 'anchor', 'number', 'before_rule', 'chapter', 'after_rule') else nb(o)
    if isinstance(o, list):
        return [nb_walk(x, key) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in ('tokens', 'related') else nb_walk(v, k)) for k, v in o.items()}
    return o


def main():
    T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
    ctx = B.Ctx(T, {}, 'final')
    ch = nb_walk(build(ctx))
    B.check_chapter(ch)
    used = set()
    for r in ch['rules']:
        for k in ('correct', 'failure'):
            used.add(r[k]['specimen'])
    used |= {x['specimen'] for x in ch['extras']}
    missing, unused = used - set(ctx.specs), set(ctx.specs) - used
    if missing or unused:
        raise SystemExit(f'specimens missing {sorted(missing)} unused {sorted(unused)}')
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for old in OUT_SP.glob('s-11-*.html'):
        if old.stem not in ctx.specs:
            old.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    man = {k: v for k, v in man.items() if str(v.get('chapter')) != CH}
    man.update({sid: s['meta'] for sid, s in ctx.specs.items()})
    MANIFEST.write_text(json.dumps(dict(sorted(man.items())), indent=1, ensure_ascii=False) + '\n')
    FIG_OUT.write_text(json.dumps({
        'about': 'Every figure chapter 11 prints, with how it was measured. Contrast is WCAG 2.x relative luminance on '
                 'the token values in tokens.json.',
        'built': '2026-11-07',
        'token_set_version': T.data.get('$extensions', {}).get('org.oathandaction', {}).get('tokenSetVersion'),
        'figures': dict(sorted(ctx.figures.items())),
        'tokens_cited': sorted(T.used),
    }, indent=1, ensure_ascii=False) + '\n')
    print(f'chapter 11: {len(ch["rules"])} rules, {len(ctx.specs)} specimens, {len(ctx.figures)} figures')


if __name__ == '__main__':
    main()
