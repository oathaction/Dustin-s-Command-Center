"""Build Board 6, section 1 (November 7, 2026): the grid keeps one job, and a simpler bill tracker.

Usage:
    python3 -I work/build/scripts/phase-2/board6_tracker_build.py

Dustin's direction is DR-104: the grid keeps one job, the lockmark in fixed places, and the bill tracker becomes "like a
line with dots or a 1, 2, 3, 4, 5, 6 step process". The page leads with six plain steps, compares four tracker options
in one view, then sets each option in full in the four-bill list at 360 and 1024 px on Newsprint and Charcoal, then
shows where the lockmark stays and what retires, then the checks and the decisions.

Writes:
    work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker.html

Reads (read and place only, never edited):
    work/build/tokens/tokens.css                          inlined; every color, face and size comes from it
    work/build/assets/identity/lockmark/*.svg             the 24 px master and the display master
    work/build/assets/identity/lockups/20261028_L3-Horizontal-Master.svg
    work/build/assets/civic-line/{black,newsprint}/...CL-005-Public-Meeting...svg
    work/boards/phase-2/board-6/tracker/20261107_Board-6-Tracker-Measurements.json   when present, written by
        board6_tracker_measure.js, so the board prints measured target sizes (run build, measure, build)

Red: every Pillar Red mark sits under data-red. Working red has one job on the page, "take part now" (Rule 05.3);
the lockmark's lever and the wordmark's ampersand are signature red. Nothing red sits on Prussian, and the page uses
no Prussian. Text is 13 px or larger everywhere. The script fails on an em dash or an en dash in its own copy.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261107'
OUT_DIR = ROOT / 'work/boards/phase-2/board-6/tracker'
OUT = OUT_DIR / f'{DATE}_Board-6-Tracker.html'
MEAS = OUT_DIR / f'{DATE}_Board-6-Tracker-Measurements.json'
TOKENS = ROOT / 'work/build/tokens/tokens.css'
ID = ROOT / 'work/build/assets/identity'
CL = ROOT / 'work/build/assets/civic-line'
FONTS = ('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800'
         '&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400;1,500&display=swap')
TAGLINE = 'A country that answers to its people.'
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'underscore', 'underscores',
           'reflect', 'reflects', 'stunning', 'robust', 'seamless', 'seamlessly']

# ------------------------------------------------------------------------------------------------ colors
HEX = {'Newsprint': '#DCD9D2', 'Charcoal': '#121212', 'Pillar Red': '#E63946', 'Stone': '#5D636D',
       'Deep Stone': '#4E535B', 'Dim Newsprint': '#A3A19C', 'White': '#FFFFFF'}


def _lin(v):
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def lum(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def ratio(a, b):
    x, y = lum(HEX[a]), lum(HEX[b])
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


# ------------------------------------------------------------------------------------------------ text helpers
def copy(s):
    """Curly quotes and apostrophes."""
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    return s


def E(s):
    return html.escape(copy(s), quote=False)


def A(s):
    return html.escape(str(s), quote=True)


LINT = []


def lint_text(s, where):
    if '—' in s:
        sys.exit(f'em dash in {where}: {s[:80]}')
    if '–' in s:
        sys.exit(f'en dash in {where}: {s[:80]}')
    for w in FLAGGED:
        if re.search(rf'\b{w}\b', s, flags=re.I):
            LINT.append(f'{where}: "{w}"')


# ------------------------------------------------------------------------------------------------ content
# Six steps. "covers" lists today's nine stages each step takes in (Rule 08.5, chapter 08 as built November 6).
STAGES = [
    dict(n=1, name='Filed', means='A legislator files the bill, and it goes to a committee.',
         covers=['1 Filed', '2 Sent to committee']),
    dict(n=2, name='Hearing', means='The committee holds a public hearing, where anyone can speak or send written testimony.',
         covers=['3 Hearing']),
    dict(n=3, name='Committee vote', means='The committee votes on whether to send the bill to the full House or Senate.',
         covers=['4 Out of committee']),
    dict(n=4, name='First chamber', means='The full House or Senate, wherever the bill was filed, votes on it.',
         covers=['5 Passed one chamber']),
    dict(n=5, name='Second chamber', means='The other chamber votes, and both agree on one text.',
         covers=['6 Passed both chambers', '7 Final text agreed']),
    dict(n=6, name='Governor', means='The governor signs or vetoes the bill, and lawmakers can override a veto. Once all six steps are done, the tracker says "Became law on" with the date, and the bill\'s page adds the date it takes effect.',
         covers=['8 Signed', '9 In effect']),
]
NAMES = [s['name'] for s in STAGES]

STATES = {
    'done': ('Done', 'The step happened.'),
    'now': ('Now', 'The bill is at this step. The words beside the tracker name it.'),
    'take': ('You can take part now', 'The bill is at this step, and the public can act before a date. Red, a shape of its own and the words carry it together.'),
    'notyet': ('Not yet', 'The bill has not reached this step.'),
    'skipped': ('Never happened', 'The bill moved past this step without it, as when a committee votes with no public hearing. It keeps its number, so the count still runs to six.'),
    'stopped': ('Stopped', 'The bill ended here, as when a committee votes it down or a veto stands. The line ends at this step, and the words give the date and the reason.'),
}
STATE_ORDER = ['done', 'now', 'take', 'notyet', 'skipped', 'stopped']
LEGEND_ORDER = ['done', 'now', 'notyet', 'skipped', 'take']

# Dustin's four-bill list (the invented bills of V5, Q-01, on the neutral topics of D2-203), on the six steps.
BILLS = [
    dict(id='H.4212', title='Public meeting notice', step=2,
         states=['done', 'take', 'notyet', 'notyet', 'notyet', 'notyet'],
         line='Testimony is open until March 3.',
         take='Send written testimony or sign up to speak by March 3.', cta='How to send testimony',
         notes={2: 'Testimony is open until March 3.'},
         today='Stage 3 of 9: Hearing, under way. Testimony is open until March 3'),
    dict(id='S.0876', title='School bus contracts', step=4,
         states=['done', 'done', 'done', 'now', 'notyet', 'notyet'],
         line='The committee sent it on, and the Senate votes next.',
         notes={4: 'The Senate votes next.'},
         today='Stage 4 of 9: Out of committee'),
    dict(id='H.1180', title='Library hours', step=6,
         states=['done', 'done', 'done', 'done', 'done', 'now'],
         line='Both chambers passed it, and it waits for the governor to sign or veto it.',
         notes={6: 'It waits for the governor to sign or veto it.'},
         today='Stage 6 of 9: Passed both chambers'),
    dict(id='H.3301', title='Records request fees', step=4,
         states=['done', 'skipped', 'done', 'now', 'notyet', 'notyet'],
         line='Step 2 never happened: the committee voted without a public hearing. The House votes next.',
         notes={2: 'Never happened: no public hearing.', 4: 'The House votes next.'}, short='Step 2 never happened.',
         today='Stage 4 of 9: Out of committee. No hearing was held'),
]


# H.1180 once the governor signs it: all six steps done. Invented dates, Illustrative.
LAW_BILL = dict(id='H.1180', title='Library hours', step=6, law='April 2', effect='July 1',
                states=['done'] * 6, line='It takes effect July 1.', short='It takes effect July 1.',
                notes={6: 'Signed April 2. It takes effect July 1.'})


def status_words(b):
    if b.get('law'):
        return f'Became law on {b["law"]}.'
    return f'Step {b["step"]} of 6: {NAMES[b["step"] - 1]}.'


# ------------------------------------------------------------------------------------------------ marks
RED_W = 'data-red="working" data-red-job="take part now"'


def svg(w, h, body, scale=1, cls='mk'):
    return (f'<svg class="{cls}" width="{w * scale:g}" height="{h * scale:g}" viewBox="0 0 {w:g} {h:g}" '
            f'aria-hidden="true" focusable="false" data-view="tracker">{body}</svg>')


def badge(cx, cy, r=5.5):
    """The take-part mark's red disc with a Charcoal keyline, which carries its edge on Newsprint (2.96 to 1 alone)."""
    return f'<g {RED_W}><circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="fr sk" stroke-width="1.5"/></g>'


# Option A: a line with dots ------------------------------------------------------------------------------
def a_node(cx, cy, st):
    if st == 'done':
        return f'<circle cx="{cx:g}" cy="{cy:g}" r="5" class="fi"/>'
    if st in ('now', 'take'):
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="8" class="fb si" stroke-width="2"/>'
        if st == 'take':
            s += f'<g {RED_W}><circle cx="{cx:g}" cy="{cy:g}" r="4" class="fr sk" stroke-width="1"/></g>'
        return s
    if st == 'notyet':
        return f'<circle cx="{cx:g}" cy="{cy:g}" r="4" class="fb ss" stroke-width="1.5"/>'
    if st == 'skipped':
        return (f'<circle cx="{cx:g}" cy="{cy:g}" r="5" class="fb ss" stroke-width="1.5"/>'
                f'<line x1="{cx - 7:g}" y1="{cy + 7:g}" x2="{cx + 7:g}" y2="{cy - 7:g}" class="si" stroke-width="2" stroke-linecap="butt"/>')
    if st == 'stopped':
        return f'<rect x="{cx - 5.5:g}" y="{cy - 5.5:g}" width="11" height="11" class="fi"/>'
    raise ValueError(st)


def line_segments(states, xs, cy):
    """Solid 2 px where the bill has come, fine 1 px ahead; nothing after a stop."""
    out = []
    stop = states.index('stopped') if 'stopped' in states else None
    for i in range(len(xs) - 1):
        if stop is not None and i >= stop:
            break
        if states[i + 1] != 'notyet':
            out.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="2" class="fi"/>')
        else:
            out.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="1" class="fs"/>')
    return out


def mk_dots(states, W, scale=1):
    c = W // 6
    xs = [c * i + c // 2 for i in range(6)]
    cy = 11
    body = line_segments(states, xs, cy) + [a_node(x, cy, s) for x, s in zip(xs, states)]
    return svg(W, 22, ''.join(body), scale)


def a_sample(st, scale=1):
    return svg(22, 22, a_node(11, 11, st), scale, cls='mk mk-s')


# Option B: numbered steps --------------------------------------------------------------------------------
def b_node(cx, cy, d, st, num=None):
    R = d / 2
    fs = 14 if d >= 28 else 13
    ty = cy + 0.36 * fs
    t = ''
    if st == 'done':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R:g}" class="fi"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fb tn" font-size="{fs}">{num}</text>'
    elif st in ('now', 'take'):
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 1.5:g}" class="fb si" stroke-width="3"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fi tn tb" font-size="{fs}">{num}</text>'
        if st == 'take':
            t += badge(cx + R * 0.72, cy - R * 0.72, 5.5 if d >= 24 else 4.5)
    elif st == 'notyet':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" class="fb ss" stroke-width="1.5"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="ft tn tl" font-size="{fs}">{num}</text>'
    elif st == 'skipped':
        k = (R + 2) * 0.7071
        s = (f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" class="fb ss" stroke-width="1.5"/>'
             f'<line x1="{cx - k:.2f}" y1="{cy + k:.2f}" x2="{cx + k:.2f}" y2="{cy - k:.2f}" class="si" stroke-width="2"/>')
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="ft tn tl halo" font-size="{fs}">{num}</text>'
    elif st == 'stopped':
        s = f'<rect x="{cx - R + 1:g}" y="{cy - R + 1:g}" width="{d - 2:g}" height="{d - 2:g}" class="fi"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fb tn" font-size="{fs}">{num}</text>'
    else:
        raise ValueError(st)
    return f'<g>{s}{t}</g>'


def mk_steps(states, W, d, scale=1):
    c = W // 6
    xs = [c * i + c // 2 for i in range(6)]
    R = d / 2
    cy = 6 + R
    H = int(cy + R + 2)
    body = line_segments(states, xs, cy) + [b_node(x, cy, d, s, i + 1) for i, (x, s) in enumerate(zip(xs, states))]
    return svg(W, H, ''.join(body), scale)


def b_sample(st, d=24, scale=1, num=None):
    """One numbered step centered in a square 14 px wider than the circle, which leaves room for the badge."""
    W = d + 14
    return svg(W, W, b_node(W / 2, W / 2, d, st, num), scale, cls='mk mk-s')


# Option C: a segmented bar with the stage word -----------------------------------------------------------
def c_seg(x, y0, sw, h, st):
    if st == 'done':
        return f'<rect x="{x:g}" y="{y0:g}" width="{sw:g}" height="{h:g}" class="fi"/>'
    if st in ('now', 'take'):
        s = (f'<rect x="{x + 1:g}" y="{y0 + 1:g}" width="{sw - 2:g}" height="{h - 2:g}" class="fb si" stroke-width="2"/>'
             f'<rect x="{x:g}" y="{y0:g}" width="{sw // 2:g}" height="{h:g}" class="fi"/>')
        if st == 'take':
            s += badge(x + sw * 0.75, y0 - 7)
        return s
    if st == 'notyet':
        return f'<rect x="{x + 0.5:g}" y="{y0 + 0.5:g}" width="{sw - 1:g}" height="{h - 1:g}" class="fb ss" stroke-width="1"/>'
    if st == 'skipped':
        return (f'<rect x="{x + 0.5:g}" y="{y0 + 0.5:g}" width="{sw - 1:g}" height="{h - 1:g}" class="fb ss" stroke-width="1"/>'
                f'<line x1="{x + 3:g}" y1="{y0 + h - 1:g}" x2="{x + sw - 3:g}" y2="{y0 + 1:g}" class="si" stroke-width="2"/>')
    if st == 'stopped':
        return (f'<rect x="{x:g}" y="{y0:g}" width="{sw:g}" height="{h:g}" class="fi"/>'
                f'<rect x="{x + sw - 3:g}" y="{y0 - 5:g}" width="3" height="{h + 10:g}" class="fi"/>')
    raise ValueError(st)


def mk_bar(states, W, h, scale=1):
    gap = 4
    sw = (W - 5 * gap) // 6
    W = sw * 6 + gap * 5
    y0 = 14
    body = [c_seg(i * (sw + gap), y0, sw, h, s) for i, s in enumerate(states)]
    return svg(W, y0 + h + 6, ''.join(body), scale)


def c_sample(st, h=12, scale=1):
    sw = 28
    return svg(sw + 4, 14 + h + 6, c_seg(2, 14, sw, h, st), scale, cls='mk mk-s')


# ------------------------------------------------------------------------------------------------ identity masters
def master(path, w, h=None, cls='idm', red=None, strip_ids=False):
    s = path.read_text()
    s = re.sub(r'<\?xml[^>]*>\s*', '', s)
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    s = re.sub(r'<desc>.*?</desc>', '', s, flags=re.S)
    if strip_ids:
        s = re.sub(r'\s(id|data-id|data-part)="[^"]*"', '', s)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    vw, vh = (float(v) for v in vb.split()[2:])
    h = h if h is not None else w * vh / vw
    extra = f' data-red="{red}"' if red else ''
    s = re.sub(r'<svg\b[^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w:g}" height="{h:g}" '
               f'class="{cls}" aria-hidden="true" focusable="false"{extra}>', s, count=1)
    return s.strip()


LOCK24 = ID / 'lockmark/20261028_Lockmark-24px-Master.svg'
LOCK_DISPLAY = ID / 'lockmark/20261028_Lockmark-Master-V5.svg'
L3 = ID / 'lockups/20261028_L3-Horizontal-Master.svg'
CL005 = {'n': CL / 'black/20261029_Oath-And-Action-Civic-Line-CL-005-Public-Meeting-Black.svg',
         'c': CL / 'newsprint/20261029_Oath-And-Action-Civic-Line-CL-005-Public-Meeting-Newsprint.svg'}


def lockmark(size, surface='n'):
    path = LOCK24 if size < 48 else LOCK_DISPLAY
    return master(path, size, size, cls=f'idm lk lk-{surface}', red='signature')


def icon(surface='n', size=24):
    return master(CL005[surface], size, size, cls='idm cl', strip_ids=True)


# Today's Signal Grid drawings, from chapter 08's specifications (Rules 08.5 to 08.8), for the before ---------------
def lattice(size, nodes, route=None):
    cs = [3.5, 19.5, 35.5] if size == 40 else [3.5, 11.5, 19.5]
    a, b = cs[0], cs[2]
    body = []
    for v in cs:
        body.append(f'<rect x="{a:g}" y="{v - 0.5:g}" width="{b - a:g}" height="1" class="fs"/>')
        body.append(f'<rect x="{v - 0.5:g}" y="{a:g}" width="1" height="{b - a:g}" class="fs"/>')
    pos = [(cs[i % 3], cs[i // 3]) for i in range(9)]
    if route:
        w = 3 if size == 40 else 2
        for p, q in zip(route, route[1:]):
            (x1, y1), (x2, y2) = pos[p], pos[q]
            x, y = min(x1, x2) - w / 2, min(y1, y2) - w / 2
            body.append(f'<rect x="{x:g}" y="{y:g}" width="{abs(x2 - x1) + w:g}" height="{abs(y2 - y1) + w:g}" class="fi"/>')
    big = 3.5 if size == 40 else 3
    for i, (x, y) in enumerate(pos):
        k = nodes.get(i, 'small')
        if k == 'done' or k == 'end':
            body.append(f'<circle cx="{x}" cy="{y}" r="{big}" class="fi"/>')
        elif k == 'ring':
            body.append(f'<circle cx="{x}" cy="{y}" r="3" class="fb si" stroke-width="1"/>')
        elif k == 'route':
            body.append(f'<circle cx="{x}" cy="{y}" r="2.5" class="fi"/>')
        elif k == 'small':
            body.append(f'<circle cx="{x}" cy="{y}" r="1.5" class="fs"/>')
    return svg(size, size, ''.join(body), cls='mk')


# ------------------------------------------------------------------------------------------------ list rows
def steps_sr(states):
    items = ''.join(f'<li>Step {i + 1}, {NAMES[i]}: {STATES[s][0].lower() if s != "take" else "now, and you can take part"}</li>'
                    for i, s in enumerate(states))
    return f'<ol class="sr">{items}</ol>'


def labels(states, W):
    lis = []
    for i, s in enumerate(states):
        cls = ' class="cur"' if s in ('now', 'take') else (' class="skp"' if s == 'skipped' else '')
        extra = '<span class="lbl-x">never happened</span>' if s == 'skipped' else ''
        lis.append(f'<li{cls}>{E(NAMES[i])}{extra}</li>')
    return f'<ol class="lbls" aria-hidden="true" style="width:{W}px;grid-template-columns:repeat(6,{W // 6}px)">{"".join(lis)}</ol>'


def take_part(b, mark, compact=False):
    if 'take' not in b:
        return ''
    if compact:
        return f'<p class="tp">{mark}<span><b>You can take part now</b>, until March 3.</span></p>'
    return (f'<p class="tp">{mark}<span><b>You can take part now.</b> {E(b["take"])}</span></p>'
            f'<p class="ctaw"><span class="cta">{E(b["cta"])}<span aria-hidden="true"> →</span></span></p>')


def legend_mark(opt, st):
    if opt == 'A':
        return a_sample(st)
    if opt in ('B', 'D'):
        return b_sample(st, 24)
    return c_sample(st, 10)


def mark_for(opt, b, ctx):
    st = b['states']
    if opt == 'A':
        return mk_dots(st, {'s': 324, 'l': 636, 'm': 240}[ctx])
    if opt == 'B':
        return mk_steps(st, {'s': 324, 'l': 636, 'm': 240}[ctx], {'s': 26, 'l': 30, 'm': 24}[ctx])
    if opt == 'C':
        return mk_bar(st, {'s': 326, 'l': 620, 'm': 236}[ctx], {'s': 12, 'l': 14, 'm': 12}[ctx])
    raise ValueError(opt)


def vt_list(b, d, notes=True, cls='vt'):
    """Option D: the six steps down the page. Each row: a numbered mark, the step's name, and a note where one belongs."""
    lis = []
    st = b['states']
    stop = st.index('stopped') if 'stopped' in st else None
    for i, s in enumerate(st):
        if i == 5:
            seg = 'seg-end'
        elif stop is not None and i >= stop:
            seg = 'seg-none'
        else:
            seg = 'seg-on' if st[i + 1] != 'notyet' else 'seg-off'
        cur = ' cur' if s in ('now', 'take') else ''
        note = ''
        if notes and (i + 1) in b.get('notes', {}):
            note = f'<span class="vt-note">{E(b["notes"][i + 1])}</span>'
        word = ''
        if s == 'skipped' and not notes:
            word = '<span class="vt-note">Never happened</span>'
        srw = '' if word else f'<span class="sr">: {E(STATES[s][0].lower())}</span>'
        lis.append(f'<li class="{seg}{cur}">{b_sample(s, d, num=i + 1)}<span class="vt-t"><span class="vt-n">{E(NAMES[i])}</span>'
                   f'{srw}{note}{word}</span></li>')
    return f'<ol class="{cls}" style="--d:{d}px">{"".join(lis)}</ol>'


def row(opt, b, ctx):
    """One bill in the list, for an option at 's' (360 px), 'l' (1024 px) or 'm' (a comparison cell)."""
    bill = f'<p class="bill"><b>Bill {E(b["id"])}</b>, {E(b["title"])}</p>'
    tmark = legend_mark(opt, 'take')
    if opt == 'D':
        d = {'s': 24, 'l': 24, 'm': 22}[ctx]
        body = vt_list(b, d, notes=(ctx != 'm'))
        tp = take_part(b, tmark, compact=(ctx == 'm'))
        if ctx == 'm':
            return f'{body}<p class="st">{E(status_words(b))}{" " + E(b["short"]) if b.get("law") else ""}</p>{tp}'
        return f'<li class="row">{bill}{body}{tp}</li>'
    mark = mark_for(opt, b, ctx)
    if opt == 'C':
        word = (f'<p class="cw"><span class="cw-w">{E("Became law" if b.get("law") else NAMES[b["step"] - 1])}</span> '
                f'<span class="cw-n">{E(b["law"] if b.get("law") else "Step " + str(b["step"]) + " of 6")}</span></p>')
        st_line = (f'<p class="st">{E(b["line"])}</p>' if ctx != 'm'
                   else (f'<p class="st">{E(b["short"])}</p>' if b.get('short') else ''))
        core = f'{word}<div class="mkw">{mark}</div>{steps_sr(b["states"])}{st_line}'
    else:
        lab = labels(b['states'], {'l': 636}.get(ctx, 0)) if ctx == 'l' else ''
        st_line = (f'<p class="st"><b>{E(status_words(b))}</b> {E(b["line"])}</p>' if ctx != 'm'
                   else f'<p class="st"><b>{E(status_words(b))}</b>{" " + E(b["short"]) if b.get("short") else ""}</p>')
        core = f'<div class="mkw">{mark}</div>{lab}{steps_sr(b["states"])}{st_line}'
    tp = take_part(b, tmark, compact=(ctx == 'm'))
    if ctx == 'm':
        return f'{core}{tp}'
    if ctx == 'l':
        return f'<li class="row">{bill}<div class="mkc">{core}{tp}</div></li>'
    return f'<li class="row">{bill}{core}{tp}</li>'


def legend(opt, steps_key=True):
    k = ''
    if steps_key:
        k = ('<p class="key-h">The six steps</p><ol class="key-steps">'
             + ''.join(f'<li><b>{i + 1}</b> {E(n)}</li>' for i, n in enumerate(NAMES)) + '</ol>')
    lis = ''.join(f'<li>{legend_mark(opt, s)}<span>{E(STATES[s][0])}</span></li>' for s in LEGEND_ORDER)
    return f'<div class="key">{k}<p class="key-h">What the marks mean</p><ul class="key-states">{lis}</ul></div>'


def panel(opt, size, surface):
    sc = 'oa-surface-newsprint' if surface == 'n' else 'oa-surface-charcoal'
    rows = ''.join(row(opt, b, size) for b in BILLS)
    ul_cls = 'rows vt4' if (opt == 'D' and size == 'l') else 'rows'
    steps_key = not (size == 'l' and opt in ('A', 'B')) and opt != 'D'
    return (f'<div class="tkp tkp--{size} {sc}">'
            f'<p class="ill">Illustrative</p>'
            f'<p class="tk-h">Where four state bills stand this week</p>'
            f'<ul class="{ul_cls}">{rows}</ul>{legend(opt, steps_key)}</div>')


def frame(inner, label, cap, width):
    return (f'<figure class="spec" style="--w:{width}px"><figcaption class="spec-cap"><b>{E(cap)}</b>'
            f'<span class="hint">Wider than this screen. Scroll the frame sideways.</span></figcaption>'
            f'<div class="frame" role="region" aria-label="{A(label)}">{inner}</div></figure>')


# ------------------------------------------------------------------------------------------------ option D bill page
PAGE_NOTES = {
    1: ('Done', 'Filed January 16 and sent to the Committee on Local Government.'),
    2: ('Now', 'The committee holds its public hearing on March 3, and testimony is open until then.'),
    3: ('Not yet', 'The committee votes on whether to send the bill to the full House.'),
    4: ('Not yet', 'The full House votes on the bill.'),
    5: ('Not yet', 'The Senate votes, and both chambers agree on one text.'),
    6: ('Not yet', 'The governor signs or vetoes the bill. Once it is signed, this page gives the date it became law and the date it takes effect.'),
}


def bill_page(size, surface):
    sc = 'oa-surface-newsprint' if surface == 'n' else 'oa-surface-charcoal'
    b = BILLS[0]
    lis = []
    for i, s in enumerate(b['states']):
        seg = 'seg-end' if i == 5 else ('seg-on' if b['states'][i + 1] != 'notyet' else 'seg-off')
        cur = ' cur' if s in ('now', 'take') else ''
        word, note = PAGE_NOTES[i + 1]
        box = ''
        if s == 'take':
            box = (f'<div class="tbox"><p class="tp">{legend_mark("D", "take")}<span><b>You can take part now.</b> '
                   f'Send written testimony or sign up to speak by March 3.</span></p>'
                   f'<p class="askw" {RED_W}><span class="ask">Send testimony</span></p></div>')
        lis.append(f'<li class="{seg}{cur}">{b_sample(s, 28, num=i + 1)}<span class="vt-t">'
                   f'<span class="vt-n">{E(NAMES[i])}</span><span class="vt-s">{E(word if s != "take" else "Now: you can take part")}</span>'
                   f'<span class="vt-note">{E(note)}</span>{box}</span></li>')
    tl = f'<ol class="vt vt-page" style="--d:28px">{"".join(lis)}</ol>'
    aside = ('<aside class="bp-aside"><p class="key-h">What the six steps mean</p><ol class="bp-key">'
             + ''.join(f'<li><b>{s["n"]} {E(s["name"])}.</b> {E(s["means"])}</li>' for s in STAGES)
             + '</ol></aside>')
    head = (f'<p class="ill">Illustrative</p><p class="kick">{icon(surface)}<span class="kick-l">Tracker</span>'
            f'<span class="chip-id"><span>Bill</span><span>H.4212</span></span></p>'
            f'<p class="bp-h">Public meeting notice</p>'
            f'<p class="bp-dek">The bill would require towns to post notice of a public meeting online two days ahead.</p>'
            f'<p class="st"><b>{E(status_words(b))}</b> Testimony is open until March 3.</p>')
    body = f'<div class="bp-cols"><div class="bp-main">{tl}</div>{aside}</div>' if size == 'l' else tl
    return f'<div class="tkp tkp--{size} {sc} bp">{head}{body}</div>'


# ------------------------------------------------------------------------------------------------ options
OPTIONS = [
    dict(k='A', name='A line with dots', short='Line with dots',
         what='Six dots sit on one line. The line is solid as far as the bill has come and fine after it, so the line works as a progress bar. Where the page has room, step names sit under the dots; on a phone, the words beside the line name the step.',
         best='It is the calmest of the four. A reader still needs the words to know which dot is which, and a row of nodes on a line comes close to the lockmark\'s own drawing.',
         specs=[('Line', '2 px Charcoal as far as the bill has come; 1 px Stone after it'),
                ('Done', '10 px disc'), ('Now', '18 px ring, 2 px line'), ('Not yet', '9.5 px ring, 1.5 px Stone'),
                ('Never happened', '11.5 px Stone ring crossed by a 2 px Charcoal slash'),
                ('Stopped', '11 px square; the line ends there'),
                ('You can take part now', 'The 18 px ring with an 8 px red center and a 1 px Charcoal keyline'),
                ('Spacing', '54 px between dots at 360 px, 106 px at 1024 px')]),
    dict(k='B', name='Numbered steps, 1 to 6', short='Numbered steps',
         what='Each step is a numbered circle on the line, filled once the bill has passed it. The step a bill is at now carries a heavy ring, and the steps ahead stay fine. The number lets a reader say where a bill stands, "step 2 of 6", before reading anything else.',
         best='We recommend it for lists and story cards, since it reads without a key and six numbered steps fit a phone. Its numbers also set it apart from the lockmark.',
         specs=[('Circles', '26 px at 360 px, 30 px at 1024 px, 24 px on a card; numbers in Inter 700 at 13 or 14 px'),
                ('Line', '2 px Charcoal as far as the bill has come; 1 px Stone after it'),
                ('Done', 'Filled Charcoal circle, Newsprint number'), ('Now', 'Ring with a 3 px line, Charcoal number'),
                ('Not yet', 'Ring with a 1.5 px Stone line, Deep Stone number'),
                ('Never happened', 'The Not yet ring crossed by a 2 px Charcoal slash, with the number kept clear of it'),
                ('Stopped', 'A filled square in place of the circle; the line ends there'),
                ('You can take part now', 'The Now ring with an 11 px red badge at its upper right, keylined in Charcoal')]),
    dict(k='C', name='A segmented bar with the stage word', short='Segmented bar',
         what='The step\'s name leads in large type, with "Step 2 of 6" beside it, and a bar of six segments fills as the bill moves. It takes the least height of the four, so it suits long lists and the top of a story.',
         best='It is compact, and the stage word reads first. The segments carry no names, so a reader who wants the whole path needs the key, and a slashed segment is small at 12 px.',
         specs=[('Stage word', 'Inter Tight 800, 20 px at 360 px and 24 px at 1024 px, with "Step 2 of 6" at 15 px'),
                ('Bar', 'Six segments with 4 px gaps, 12 px tall at 360 px and 14 px at 1024 px'),
                ('Done', 'Filled segment'), ('Now', 'Outlined with a 2 px line, left half filled'),
                ('Not yet', 'Outlined with a 1 px Stone line'), ('Never happened', 'The Not yet segment crossed by a 2 px slash'),
                ('Stopped', 'Filled, with a 3 px bar standing 5 px above and below its right end'),
                ('You can take part now', 'The Now segment with an 11 px red badge above it, keylined in Charcoal')]),
    dict(k='D', name='A vertical timeline for a bill\'s own page', short='Vertical timeline',
         what='The six steps run down the page, each with its name, its date and a line on what happened. Under the current step there is room for the date to act and the way to do it, so it suits a bill\'s own page. In a list it runs tall.',
         best='We recommend it for a bill\'s own page, where Option B\'s numbered steps turn upright so the two read as one system. In a list of many bills it runs too tall.',
         specs=[('Steps', 'Option B\'s numbered circles at 24 px in a list and 28 px on a bill\'s page'),
                ('Line', 'A 2 px Charcoal line down the page as far as the bill has come; 1 px Stone after it'),
                ('Row', 'Step name in Inter 600 at 16 px, the state in words, then a note at 15 px'),
                ('You can take part now', 'The badge on the step, the words, and a box under the step with the date and the red ask button'),
                ('Ask button', 'Inter 700 at 19 px, White on Pillar Red, 48 px tall')]),
]
OPT = {o['k']: o for o in OPTIONS}


def state_key(opt):
    cards = []
    for s in STATE_ORDER:
        if opt == 'A':
            one, two = a_sample(s), a_sample(s, 2)
        elif opt in ('B', 'D'):
            one, two = b_sample(s, 26, num=4), b_sample(s, 26, 2, num=4)
        else:
            one, two = c_sample(s, 12), c_sample(s, 12, 2)
        cards.append(f'<li class="sk-card"><div class="sk-marks"><span class="sk-1">{one}</span><span class="sk-2">{two}</span></div>'
                     f'<p class="sk-name">{E(STATES[s][0])}</p><p class="sk-mean">{E(STATES[s][1])}</p></li>')
    note = ' Each mark is drawn on step 4, at true size and at twice size.' if opt in ('B', 'D') else ' Each mark is drawn at true size and at twice size.'
    return (f'<p class="small">Six states, each named in words wherever it appears.{E(note)}</p>'
            f'<ul class="skey">{"".join(cards)}</ul>')


def option_section(o, num):
    k = o['k']
    rec = '<span class="chip chip-rec">Recommended</span>' if k in ('B', 'D') else ''
    specs = ''.join(f'<div><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in o['specs'])
    n360 = frame(panel(k, 's', 'n'), f'Option {k} at 360 px on Newsprint, true size', '360 px, Newsprint', 360)
    c360 = frame(panel(k, 's', 'c'), f'Option {k} at 360 px on Charcoal, true size', '360 px, Charcoal', 360)
    n1024 = frame(panel(k, 'l', 'n'), f'Option {k} at 1024 px on Newsprint, true size', '1024 px, Newsprint', 1024)
    c1024 = frame(panel(k, 'l', 'c'), f'Option {k} at 1024 px on Charcoal, true size', '1024 px, Charcoal', 1024)
    extra = ''
    if k == 'D':
        extra = ('<h3 class="sub">On a bill\'s own page</h3><p>H.4212\'s page sets the same six steps with a note on each and the dates known so far. '
                 'The box under step 2 holds the date to act and the page\'s one red ask, the button that opens the way to send testimony.</p>'
                 '<div class="pair">'
                 + frame(bill_page('s', 'n'), 'Option D, a bill\'s page at 360 px on Newsprint, true size', 'Bill page, 360 px, Newsprint', 360)
                 + frame(bill_page('s', 'c'), 'Option D, a bill\'s page at 360 px on Charcoal, true size', 'Bill page, 360 px, Charcoal', 360)
                 + '</div>'
                 + frame(bill_page('l', 'n'), 'Option D, a bill\'s page at 1024 px on Newsprint, true size', 'Bill page, 1024 px, Newsprint', 1024)
                 + frame(bill_page('l', 'c'), 'Option D, a bill\'s page at 1024 px on Charcoal, true size', 'Bill page, 1024 px, Charcoal', 1024))
    return (f'<section id="option-{k.lower()}" aria-labelledby="option-{k.lower()}-h">'
            f'<p class="secnum">{num:02d}</p><h2 id="option-{k.lower()}-h">Option {k}: {E(o["name"])} {rec}</h2>'
            f'<div class="lede"><p>{E(o["what"])}</p><p class="verdict"><b>Our read.</b> {E(o["best"])}</p></div>'
            f'<h3 class="sub">How each state shows</h3>{state_key(k)}'
            f'<h3 class="sub">In the four-bill list</h3>'
            f'<p class="small">Each list is drawn at true size. On a phone, a frame wider than the screen scrolls sideways.</p>'
            f'<div class="pair">{n360}{c360}</div>{n1024}{c1024}{extra}'
            f'<h3 class="sub">Sizes</h3><dl class="specs">{specs}</dl></section>')


# ------------------------------------------------------------------------------------------------ sections
def sec_steps():
    rows = ''.join(f'<tr><td class="n">{s["n"]}</td><th scope="row">{E(s["name"])}</th><td>{E(s["means"])}</td>'
                   f'<td>{E(", ".join(s["covers"]))}</td></tr>' for s in STAGES)
    states = ''.join(f'<div><dt>{E(STATES[s][0])}</dt><dd>{E(STATES[s][1])}</dd></div>' for s in STATE_ORDER)
    m = ''.join(f'<tr><th scope="row">Bill {E(b["id"])}, {E(b["title"])}</th><td>{E(b["today"])}</td>'
                f'<td><b>{E(status_words(b))}</b> {E(b["line"])}{" You can take part now." if "take" in b else ""}</td></tr>'
                for b in BILLS)
    law = ''.join(f'<li><p class="key-h">Option {o["k"]}, {E(o["short"])}</p>{row(o["k"], LAW_BILL, "m")}</li>' for o in OPTIONS)
    return f'''<section id="six-steps" aria-labelledby="six-steps-h"><p class="secnum">01</p>
<h2 id="six-steps-h">Six steps a newcomer reads at once</h2>
<div class="lede"><p>Today's tracker counts nine stages on a 3 by 3 grid, and a reader has to learn the grid's reading order and five shapes before it tells them anything. Six steps cover the same path. Each has a plain name, and every tracker prints the name with its number, as in "Step 2 of 6: Hearing."</p>
<p>A chamber is one half of the legislature, the House or the Senate. A bill numbered H. starts in the House, and one numbered S. starts in the Senate, so the words beside each tracker name the real chamber.</p></div>
<div class="tw"><table class="stk tbl-steps"><caption class="sr">The six steps of a state bill, what happens at each, and the stages of today's tracker each one covers</caption>
<thead><tr><th scope="col">Step</th><th scope="col">Name</th><th scope="col">What happens</th><th scope="col">Today's stages it covers</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="small">These steps follow a state bill. Chapter 15 sets the steps for other routes, such as a ballot measure or an agency rule, in the same form.</p>
<h3 class="sub">How a state shows, in words</h3>
<p>Each option below draws these six states its own way, and every one of them prints the state in words beside the mark.</p>
<dl class="states">{states}</dl>
<h3 class="sub">When a bill becomes law</h3>
<p>Step 6 is the governor, who signs or vetoes the bill. A bill at step 6 reads "Step 6 of 6: Governor", which says it is waiting. Once the governor signs, all six steps are done, and the words say "Became law on" with the date. The bill's page adds the date it takes effect. A veto that stands ends the line at step 6 as Stopped.</p>
<p class="small"><span class="chip chip-ill">Illustrative</span> Bill H.1180, Library hours, after the governor signs it, in each option at the width of a story card.</p>
<ul class="lawx">{law}</ul>
<h3 class="sub">Your four bills, today and on six steps</h3>
<p>Today's list names the last stage a bill finished. The six steps name the step a bill is at now, which is the one a reader can act on.</p>
<div class="tw"><table class="stk tbl-bills"><caption class="sr">The four bills in your list, as today's tracker reads them and as the six steps read them</caption>
<thead><tr><th scope="col">Bill <span class="chip chip-ill">Illustrative</span></th><th scope="col">Today, nine stages</th><th scope="col">Proposed, six steps</th></tr></thead>
<tbody>{m}</tbody></table></div>
</section>'''


COMPARE = [
    ('Says where a bill stands without the key', ['Only with the words beside it', 'Yes: the number and the name', 'Yes: the stage word leads', 'Yes: every step is named']),
    ('On a 360 px phone', ['The dots fit; names move to the key', 'Six numbered steps fit; names move to the key', 'One line of words and a thin bar', 'About 330 px tall for each bill, and more with a way to take part']),
    ('A step that never happened', ['A slashed ring', 'A slashed ring with its number kept', 'A slashed segment, small at 12 px', 'The step\'s own line says so']),
    ('You can take part now', ['A red center in the ring, with the words', 'A red badge on the step, with the words', 'A red badge over the segment, with the words', 'A box under the step, with the date and the ask']),
    ('A list of 20 bills', ['Works', 'Works', 'The most compact', 'Too tall']),
    ('Next to the lockmark', ['Close to it: nodes on a line', 'Set apart by its numbers', 'Unlike it', 'Unlike it']),
    ('Our read', ['Calm, and it needs its words', 'Use in lists and on cards', 'A good second for dense lists', 'Use on a bill\'s own page']),
]


def sec_compare():
    head = ''.join(f'<th scope="col" role="columnheader">Option {o["k"]}<span class="mx-o">{E(o["short"])}</span>'
                   f'{"<span class=\"chip chip-rec\">Recommended</span>" if o["k"] in ("B", "D") else ""}</th>' for o in OPTIONS)
    trs = []
    for b in BILLS:
        tds = ''.join(f'<td role="cell" data-label="Option {o["k"]}, {A(o["short"])}">{row(o["k"], b, "m")}</td>' for o in OPTIONS)
        trs.append(f'<tr role="row"><th scope="row" role="rowheader"><b>Bill {E(b["id"])}</b><span>{E(b["title"])}</span></th>{tds}</tr>')
    crit = ''.join(f'<tr role="row"><th scope="row" role="rowheader">{E(c)}</th>'
                   + ''.join(f'<td role="cell" data-label="Option {o["k"]}">{E(v)}</td>' for o, v in zip(OPTIONS, vals)) + '</tr>'
                   for c, vals in COMPARE)
    chead = ''.join(f'<th scope="col" role="columnheader">Option {o["k"]}<span class="mx-o">{E(o["short"])}</span></th>' for o in OPTIONS)
    return f'''<section id="compare" aria-labelledby="compare-h"><p class="secnum">02</p>
<h2 id="compare-h">The four options side by side</h2>
<div class="lede"><p>Each column draws your four bills with one option, at the width of a story card. Read across a row to see how the four options show the same bill.</p></div>
<div class="mxw" role="region" aria-label="The four options for the four bills"><table class="mx" role="table"><caption class="sr">Each of the four bills drawn with each of the four tracker options</caption>
<thead><tr role="row"><th scope="col" role="columnheader"><span class="chip chip-ill">Illustrative</span></th>{head}</tr></thead>
<tbody>{"".join(trs)}</tbody></table></div>
<h3 class="sub">How they compare</h3>
<div class="mxw" role="region" aria-label="How the four options compare"><table class="mx mx-c" role="table"><caption class="sr">The four options compared on seven questions</caption>
<thead><tr role="row"><th scope="col" role="columnheader">Question</th>{chead}</tr></thead><tbody>{crit}</tbody></table></div>
<div class="recbox"><p class="key-h">Recommendation</p>
<p>Use Option B in lists and on story cards, and Option D on a bill's own page. They share the six steps and the same numbered marks, so a reader who learns one has learned the other. A number gives a reader words to say, "step 2 of 6", and it survives a phone screen, gray print and color blindness. A bill's page has the room the timeline needs for dates, notes and the way to take part.</p>
<p>Option C is the strongest second choice, for a dense list such as a weekly roundup of 20 bills. The dots of Option A are the lightest mark here, though they need their words more than any other option does.</p></div>
</section>'''


def sec_grid():
    before = [
        (lattice(40, {0: 'done', 1: 'done', 2: 'ring'}), 'Tracker progress', 'Stage 3 of 9: Hearing, under way', 'Rule 08.5'),
        (lattice(40, {3: 'route', 4: 'route', 5: 'route', 2: 'end'}, route=[3, 4, 5, 2]), 'Series route', 'Dispatch, a Track series', 'Rule 08.6'),
        (lattice(24, {6: 'end'}), 'Pillar corner', 'Connect', 'Rule 08.7'),
        (f'<span class="kick kick-old">{lattice(24, {3: "route", 4: "route", 5: "route", 2: "end"}, route=[3, 4, 5, 2])}{icon("n")}<span class="kick-l">Report · Dispatch</span></span>',
         'The grid in the kicker', '', 'Rule 08.8'),
        (lattice(40, {i: 'none' for i in range(9)}), 'Coded states', 'Loading tracker', 'Rule 08.9'),
    ]
    bl = ''.join(f'<li><div class="ba-mark">{m}</div><div><p class="ba-t">{E(t)}</p>'
                 f'{f"<p class=\"ba-k\">{E(k)}</p>" if k else ""}<p class="ba-r">{E(r)}, retires</p></div></li>' for m, t, k, r in before)
    masthead = (f'<div class="am am-mast oa-surface-newsprint">{master(L3, 264, cls="idm l3", red="signature")}</div>')
    header = (f'<div class="am am-head oa-surface-white">{lockmark(24)}<span class="kick-l">03 · Who writes the budget</span>'
              f'<span class="pg">7</span></div>')
    footer = (f'<div class="am am-foot oa-surface-charcoal">{lockmark(24, "c")}<span class="ft-t"><b>Oath &amp; Action</b>'
              f'<span class="tag">{E(TAGLINE)}</span></span></div>')
    signoff = (f'<div class="am am-sign oa-surface-newsprint"><span class="sg-l">Bottom-right corner of a 1080 px social card</span>'
               f'{lockmark(40)}<span class="sg-m">72 px margin</span></div>')
    after = [
        (masthead, 'Masthead', 'L3, the wordmark with the lockmark, on screens 768 px and wider'),
        (header, 'Page header', 'Report and slide pages: 24 px, beside the section label. The section title is invented, so the piece is Illustrative'),
        (footer, 'Footer', 'Site, email and chart footers: 24 px, beside the tagline; 16 px in a chart footer'),
        (signoff, 'Sign-off', 'Bottom right of social cards, covers and posters: 40 px, inside the margin'),
    ]
    al = ''.join(f'<li><div class="ba-app" role="region" aria-label="{A(t)}, true size">{m}</div><p class="ba-t">{E(t)}</p><p class="ba-k">{E(k)}</p></li>' for m, t, k in after)
    kicker_after = (f'<div class="am am-kick oa-surface-newsprint"><span class="kick">{icon("n")}<span class="kick-l">Report · Dispatch</span>'
                    f'<span class="chip-id"><span>Bill</span><span>H.4212</span></span></span>'
                    f'<p class="kick-hl">The House takes up the meeting notice bill on Thursday</p></div>')
    ret = [
        ('Tracker progress on the grid', 'Rule 08.5', 'The six numbered steps on this board'),
        ('Series routes', 'Rule 08.6', 'The series named in words in the kicker (Rule 01.21)'),
        ('Pillar corners', 'Rule 08.7', 'The pillar icon with its word, on Board 6, section 2'),
        ('The grid in the kicker', 'Rule 08.8', 'An icon and the label, as drawn here'),
        ('Coded grids, their key, the order of codes and the composer', 'Rules 08.3 and 08.4', 'Nothing left to code'),
        ('Grid states: empty, loading, ready, under way and final', 'Rule 08.9', 'The tracker\'s own states, in words'),
        ('The lattice as a background pattern', 'Rule 08.2, builders note for chapter 12', 'No pattern; the lockmark appears whole or not at all'),
    ]
    rt = ''.join(f'<tr><th scope="row">{E(a)}</th><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in ret)
    return f'''<section id="grid" aria-labelledby="grid-h"><p class="secnum">07</p>
<h2 id="grid-h">The grid keeps one job</h2>
<div class="lede"><p>The lockmark keeps its drawing and signs four fixed places, once in a view. Every use of the grid that codes something retires, and words or other marks take over each job. Rule 08.1 stays as it is, and Rule 08.2 names the four places below.</p></div>
<div class="ba">
<div class="ba-col"><p class="key-h">Today: the grid codes five things</p><ul class="ba-list ba-before">{bl}</ul></div>
<div class="ba-col"><p class="key-h">Proposed: the lockmark signs four places</p><ul class="ba-list ba-after">{al}</ul></div>
</div>
<h3 class="sub">The kicker without the grid</h3>
<p>The kicker, the short line above a title, keeps its icon and its words. The series that the route used to code is named in the words, as Rule 01.21 already asks.</p>
<div class="frame frame-fit" role="region" aria-label="A story kicker without the grid, true size">{kicker_after}</div>
<p class="small"><span class="chip chip-ill">Illustrative</span> The top of a story card at true size, with the public meeting icon at 24 px and the words "Report · Dispatch".</p>
<h3 class="sub">What retires, and what takes each job</h3>
<div class="tw"><table class="stk tbl-ret"><caption class="sr">Each use of the grid that retires, the rule it comes from, and what takes over its job</caption>
<thead><tr><th scope="col">Retires</th><th scope="col">From</th><th scope="col">What takes the job</th></tr></thead><tbody>{rt}</tbody></table></div>
<p class="small">A page that shows its masthead and its footer in one view, such as a short email, keeps the lockmark in the footer and sets the wordmark alone at the top, so the lockmark still appears once.</p>
</section>'''


def sec_checks(meas):
    pairs = [
        ('Newsprint', 'Done marks, the 2 px line, ring lines and numbers', 'Charcoal', 'Newsprint', 3),
        ('Newsprint', 'Not yet marks and the 1 px line', 'Stone', 'Newsprint', 3),
        ('Newsprint', 'Notes, keys and Not yet numbers', 'Deep Stone', 'Newsprint', 4.5),
        ('Newsprint', 'Numbers on a done step', 'Newsprint', 'Charcoal', 4.5),
        ('Newsprint', 'The red take-part mark alone', 'Pillar Red', 'Newsprint', 3),
        ('Newsprint', 'The red mark\'s Charcoal keyline, which carries its edge', 'Charcoal', 'Newsprint', 3),
        ('Newsprint', 'Ask button label, 19 px bold', 'White', 'Pillar Red', 3),
        ('Charcoal', 'Done marks, lines and numbers', 'Newsprint', 'Charcoal', 3),
        ('Charcoal', 'Not yet marks, notes and keys', 'Dim Newsprint', 'Charcoal', 4.5),
        ('Charcoal', 'The red take-part mark', 'Pillar Red', 'Charcoal', 3),
    ]
    trs = []
    for surf, what, fg, bg, need in pairs:
        r = ratio(fg, bg)
        ok = r >= need - 0.005
        note = 'passes' if ok else ('fails alone; the keyline carries it' if fg == 'Pillar Red' else 'fails')
        trs.append(f'<tr><td>{surf}</td><td>{E(what)}</td><td>{fg} on {bg}</td><td class="num">{r:.2f}:1</td>'
                   f'<td class="num">{need:g}:1</td><td>{note}</td></tr>')
    tgt = ''
    if meas and meas.get('targets'):
        t = meas['targets']
        tgt = (f'<li>Take-part links in the lists: {t["cta"]["count"]} measured, the smallest {t["cta"]["minW"]:.0f} by {t["cta"]["minH"]:.0f} px. '
               f'The 2.5.8 floor is 24 by 24 px, and 44 px tall clears the touch size in our tokens.</li>'
               f'<li>Ask buttons on the bill pages: {t["ask"]["count"]} measured, the smallest {t["ask"]["minW"]:.0f} by {t["ask"]["minH"]:.0f} px.</li>')
        if meas.get('marks'):
            m = meas['marks']
            tgt += (f'<li>Smallest drawn mark that carries a state: {m["minMark"]:.1f} px across, the Not yet ring of Option A. '
                    f'The smallest red mark is {m.get("minRed", 0):.0f} px across, with its own Charcoal keyline. Smallest text on the page: {m["minText"]:.0f} px.</li>')
        w = meas.get('widths', {}).get('1440', {})
        if w.get('contrast'):
            by = {(c['surface'], c['role']): c['ratio'] for c in w['contrast']}
            g = lambda s, r: f'{by.get((s, r), 0):.2f}'
            tgt += (f'<li>Rendered contrast in Option B\'s lists, read from the page: done marks {g("Newsprint", "Done mark")} to 1 on Newsprint '
                    f'and {g("Charcoal", "Done mark")} to 1 on Charcoal; Not yet rings {g("Newsprint", "Not yet ring")} and {g("Charcoal", "Not yet ring")} to 1; '
                    f'the red badge {g("Newsprint", "Red badge")} to 1 on Newsprint inside a keyline of {g("Newsprint", "Red badge keyline")} to 1, and {g("Charcoal", "Red badge")} to 1 on Charcoal; '
                    f'key text {g("Newsprint", "Key text")} and {g("Charcoal", "Key text")} to 1. The values match the table above.</li>')
        if w.get('focus'):
            f390 = meas['widths'].get('390', {}).get('focus', {})
            tgt += (f'<li>Keyboard: {w["focus"]["stops"]} Tab stops at 1440 px and {f390.get("stops", 0)} at 390 px, where more frames scroll; '
                    f'{len(w["focus"]["withoutRing"]) + len(f390.get("withoutRing", []))} without a visible ring.</li>')
        tgt += f'<li>Measured {E(meas.get("measured", ""))} by <code>board6_tracker_measure.js</code> at 1440 and 390 px.</li>'
    else:
        tgt = '<li>Targets are set at 44 px tall in the lists and 48 px on the bill pages. Run the measure script to print measured sizes here.</li>'
    return f'''<section id="checks" aria-labelledby="checks-h"><p class="secnum">08</p>
<h2 id="checks-h">Accessibility: what was measured</h2>
<div class="lede"><p>Each state has a name in words. The legend under every list names all of them, and the line beside each tracker names the step a bill is at, any step that never happened and the chance to take part. A screen reader hears every step's name and state from a list the eye does not see.</p><p>Shape alone tells each state apart in grayscale, and color never works alone: the one red mark always comes with its own shape and the words "You can take part now".</p></div>
<h3 class="sub">Contrast, from the token values</h3>
<div class="tw"><table class="stk tbl-con"><caption class="sr">Contrast of every mark and text pair the trackers use</caption>
<thead><tr><th scope="col">Surface</th><th scope="col">What</th><th scope="col">Pair</th><th scope="col">Ratio</th><th scope="col">Needs</th><th scope="col">Result</th></tr></thead>
<tbody>{"".join(trs)}</tbody></table></div>
<p class="small">Graphics need 3 to 1 against their surface (WCAG 2.2, 1.4.11), and text needs 4.5 to 1, or 3 to 1 at 19 px bold and larger (1.4.3).</p>
<h3 class="sub">Targets and sizes, measured on the rendered page</h3><ul class="facts">{tgt}</ul>
</section>'''


DECISIONS = [
    dict(id='T1', q='Do the nine tracker stages become these six steps?',
         opts=['Six steps, as drawn: Filed, Hearing, Committee vote, First chamber, Second chamber, Governor', 'Keep the nine stages'],
         rec='a', why='Six steps cover the same path in words a newcomer knows. Each one joins stages a reader seldom needs apart, such as Signed and In effect, whose dates the bill\'s page still gives. The hearing keeps a step of its own, since it is the step where the public is invited to speak, and a missing hearing is news a reader should see.'),
    dict(id='T2', q='Which tracker do we use?',
         opts=['Option A, a line with dots', 'Option B in lists and on cards, and Option D on a bill\'s own page', 'Option C, the segmented bar', 'Option D everywhere'],
         rec='b', why='Numbers read without a key and hold up on a phone and in gray print. The timeline gives a bill\'s page room for dates and the way to take part. Before trackers ship, the six steps and the take-part mark go into the next reader check.'),
    dict(id='T3', q='Does the lockmark keep these four places, with Rules 08.3 to 08.9 retiring?',
         opts=['Yes: masthead, page header, footer and sign-off, and every coded grid retires', 'Yes, and keep the 16 px legend mark inside charts as a fifth place'],
         rec='a', why='You asked for one use. A chart footer already holds the lockmark under the footer place, so a separate legend mark adds a fifth spot without a new job.'),
]


def sec_decisions():
    cards = []
    for d in DECISIONS:
        ol = ''.join(f'<li><b>{chr(97 + i)}</b> {E(t)}{" <span class=\"chip chip-rec\">Recommended</span>" if chr(97 + i) == d["rec"] else ""}</li>'
                     for i, t in enumerate(d['opts']))
        cards.append(f'<li class="dec" id="{d["id"].lower()}"><p class="dec-id">{d["id"]}</p><p class="dec-q">{E(d["q"])}</p>'
                     f'<ol class="dec-o">{ol}</ol><p class="dec-why"><b>Why {d["rec"]}.</b> {E(d["why"])}</p></li>')
    sample = ', '.join(f'{d["id"]} {d["rec"]}' for d in DECISIONS)
    return f'''<section id="answers" aria-labelledby="answers-h"><p class="secnum">09</p>
<h2 id="answers-h">Your answers</h2>
<div class="lede"><p>Three questions, each with the studio's recommendation. Nothing in the guide changes until you pick (D2-320). A reply of letters is enough, for example "{sample}".</p></div>
<ol class="decs">{"".join(cards)}</ol>
</section>'''


# ------------------------------------------------------------------------------------------------ page
CSS = r"""
/* Board 6, section 1. The Board 5 frame on Newsprint, set from the inlined tokens. Specimens sit in frames at true size. */
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:400 1rem/1.6 var(--oa-font-family-reading)}
a{color:inherit;text-underline-offset:3px}
:focus-visible{outline:3px solid var(--oa-color-palette-charcoal);outline-offset:3px}
.oa-surface-charcoal :focus-visible{outline-color:var(--oa-color-palette-newsprint)}
.board{max-width:1344px;margin:0 auto;padding:40px 32px 96px}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--oa-color-palette-charcoal);padding-bottom:14px}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.02em;white-space:nowrap}
.mast span{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);text-align:right}
.eyebrow{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);margin:28px 0 0}
h1,h2,h3{font-family:var(--oa-font-family-display);font-weight:800;text-wrap:balance;margin:0}
h1{font-size:var(--oa-type-section-font-size);line-height:var(--oa-type-section-line-height);letter-spacing:var(--oa-type-section-letter-spacing);margin-top:10px;max-width:18ch}
h2{font-size:var(--oa-type-h3-font-size);line-height:var(--oa-type-h3-line-height);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0 0 14px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px}
h3.sub{font-size:var(--oa-type-h4-font-size);line-height:var(--oa-type-h4-line-height);letter-spacing:var(--oa-type-h4-letter-spacing);margin:40px 0 12px}
p{margin:0 0 12px;max-width:68ch}
.deck{font:var(--oa-type-intro);max-width:58ch;margin-top:18px}
.lede p{font-size:1.125rem;line-height:1.6;max-width:62ch}
section{border-top:1px solid var(--oa-color-palette-stone);margin-top:64px;padding-top:28px}
.secnum{font:var(--oa-type-label);letter-spacing:.06em;color:var(--oa-color-derived-deep-stone);margin:0 0 6px}
.small{font-size:.9375rem;color:var(--oa-color-derived-deep-stone)}
.verdict{border-left:4px solid var(--oa-color-palette-charcoal);padding-left:14px}
.toc{display:flex;flex-wrap:wrap;gap:0 22px;margin:24px 0 0;padding:6px 0;border-top:1px solid var(--oa-color-palette-stone);border-bottom:1px solid var(--oa-color-palette-stone);list-style:none}
.toc a{font:600 .9375rem/1.3 var(--oa-font-family-reading);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}
.toc a:hover{text-decoration:underline}
.recbox{background:var(--oa-color-palette-white);border:1px solid var(--oa-color-palette-charcoal);padding:20px 24px;margin-top:28px;max-width:84ch}
.recbox p{max-width:none}.recbox p:last-child{margin:0}
.key-h{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;margin:0 0 8px}
.chip{display:inline-block;font:700 .8125rem/1 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;padding:5px 7px;border:1px solid currentColor;vertical-align:middle;white-space:nowrap}
.chip-rec{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint);border-color:var(--oa-color-palette-charcoal);font-family:var(--oa-font-family-reading)}
.chip-ill{border-style:solid}
.sr{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;margin:0!important;padding:0!important}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.tw{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.9375rem}
th,td{text-align:left;vertical-align:top;padding:12px 14px 12px 0;border-bottom:1px solid var(--oa-color-palette-stone)}
thead th{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);border-bottom:2px solid var(--oa-color-palette-charcoal)}
tbody th{font-weight:700}
td.n{font:800 1.5rem/1 var(--oa-font-family-display);width:3rem}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
dl.states{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr));gap:16px 32px;margin:12px 0 0}
dl.states dt{font-weight:700}dl.states dd{margin:2px 0 0;font-size:.9375rem}
dl.specs{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr));gap:12px 32px;margin:0}
dl.specs dt{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone)}dl.specs dd{margin:2px 0 0;font-size:.9375rem}
ul.facts{margin:0;padding-left:1.1em}ul.facts li{margin:0 0 8px;max-width:76ch}

/* state keys */
.skey{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,190px),1fr));gap:12px}
.sk-card{background:var(--oa-color-palette-newsprint);border:1px solid var(--oa-color-palette-stone);padding:14px}
.sk-marks{display:flex;align-items:center;gap:18px;min-height:76px}
.sk-name{font-weight:700;margin:8px 0 2px}.sk-mean{font-size:.875rem;margin:0;color:var(--oa-color-derived-deep-stone)}

/* specimen frames */
.spec{margin:16px 0 0;min-width:0}
.spec-cap{font:600 .875rem/1.4 var(--oa-font-family-reading);margin:0 0 8px;display:flex;flex-wrap:wrap;gap:4px 12px}
.spec-cap .hint{display:none;color:var(--oa-color-derived-deep-stone);font-weight:400}
.spec:has(.frame.is-wide) .hint{display:inline}
.frame{overflow-x:auto;max-width:100%;width:max-content}
.frame.is-wide{width:auto}
.pair{display:flex;flex-wrap:wrap;gap:8px 32px;align-items:flex-start}
.pair .spec{max-width:100%}
.frame-fit{margin:8px 0 10px}

/* marks */
.mk{display:block;overflow:visible;flex:none}
.mk .fi{fill:var(--tk-ink)}.mk .fs{fill:var(--tk-sub)}.mk .fb{fill:var(--tk-bg)}.mk .ft{fill:var(--tk-text2)}
.mk .fr{fill:var(--oa-color-palette-pillar-red)}
.mk .si{stroke:var(--tk-ink)}.mk .ss{stroke:var(--tk-sub)}.mk .sk{stroke:var(--oa-color-palette-charcoal)}
.mk line{fill:none}
.mk text{font-family:var(--oa-font-family-reading);font-weight:700;font-variant-numeric:tabular-nums;text-anchor:middle}
.mk text.tb{font-weight:800}.mk text.tl{font-weight:600}
.mk text.halo{paint-order:stroke;stroke:var(--tk-bg);stroke-width:4px;stroke-linejoin:round}
.oa-surface-newsprint{--tk-bg:var(--oa-color-surface-newsprint)}
.oa-surface-charcoal{--tk-bg:var(--oa-color-surface-charcoal)}
.oa-surface-white{--tk-bg:var(--oa-color-surface-white)}
.oa-surface-newsprint,.oa-surface-charcoal,.oa-surface-white{--tk-ink:var(--oa-color-graphic-essential);--tk-sub:var(--oa-color-graphic-subtle);--tk-text2:var(--oa-color-text-secondary)}

/* tracker panels, the specimens */
.tkp{font-family:var(--oa-font-family-reading);font-size:15px;line-height:1.5;padding:20px 16px 24px;color:var(--oa-color-text-primary)}
.tkp--s{width:360px}.tkp--l{width:1024px;padding:32px 40px 36px}
.tkp p{margin:0;max-width:none}
.tkp .ill{display:inline-block;font:700 13px/1 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;padding:5px 7px;border:1px solid var(--oa-color-border-strong);margin:0 0 12px}
.tkp .tk-h{font:800 26px/1.08 var(--oa-font-family-display);letter-spacing:-.01em;margin:0 0 16px;text-wrap:balance}
.tkp--l .tk-h{font-size:32px}
.tkp .rows{list-style:none;margin:0;padding:0;border-top:1px solid var(--oa-color-border-hairline)}
.tkp .row{padding:16px 0 18px;border-bottom:1px solid var(--oa-color-border-hairline)}
.tkp .bill{font-size:17px;line-height:1.35;margin:0 0 12px}
.tkp .bill b{font-weight:700}
.tkp .mkw{display:flex;justify-content:center}
.tkp--l .mkw{justify-content:flex-start}
.tkp .st{margin-top:8px}
.tkp .tp{display:flex;gap:8px;align-items:flex-start;margin-top:8px}
.tkp .tp .mk{margin-top:1px}
.tkp .ctaw{margin:2px 0 -6px}
.tkp .cta{display:inline-flex;align-items:center;min-height:44px;font-weight:600;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
.tkp--l .row{display:grid;grid-template-columns:272px 640px;column-gap:32px}
.tkp--l .row .bill{margin:4px 0 0}
.tkp .lbls{list-style:none;margin:6px 0 0;padding:0;display:grid;font-size:13px;line-height:1.3;color:var(--oa-color-text-secondary);text-align:center}
.tkp .lbls li{padding:0 4px}
.tkp .lbls li.cur{color:var(--oa-color-text-primary);font-weight:700}
.tkp .lbls .lbl-x{display:block}
.tkp .cw{display:flex;align-items:baseline;flex-wrap:wrap;gap:2px 10px;margin:0 0 2px}
.tkp .cw-w{font:800 20px/1.15 var(--oa-font-family-display);letter-spacing:-.005em}
.tkp--l .cw-w{font-size:24px}
.tkp .cw-n{font-size:15px;color:var(--oa-color-text-secondary);font-variant-numeric:tabular-nums}
.tkp .key{margin-top:18px;font-size:14px;line-height:1.45;color:var(--oa-color-text-secondary)}
.tkp .key .key-h{color:var(--oa-color-text-primary);margin:12px 0 6px}
.tkp .key .key-h:first-child{margin-top:0}
.tkp .key-steps{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:2px 14px}
.tkp .key-steps b{color:var(--oa-color-text-primary)}
.tkp .key-states{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:6px 18px}
.tkp .key-states li{display:inline-flex;align-items:center;gap:7px}

/* option D */
.vt{list-style:none;margin:0;padding:0}
.vt li{position:relative;display:grid;grid-template-columns:calc(var(--d) + 14px) minmax(0,1fr);column-gap:6px;padding-bottom:4px;min-height:calc(var(--d) + 14px)}
.vt li::after{content:"";position:absolute;left:calc(var(--d) / 2 + 6px);width:2px;top:calc(var(--d) + 7px);bottom:-7px;background:var(--tk-ink)}
.vt li.seg-off::after{width:1px;left:calc(var(--d) / 2 + 6.5px);background:var(--tk-sub)}
.vt li.seg-end::after,.vt li.seg-none::after{display:none}
.vt .vt-t{padding-top:calc(var(--d) / 2 - 3px);display:flex;flex-direction:column}
.vt .vt-n{font-weight:600;font-size:15px;line-height:1.3}
.vt li.cur .vt-n{font-weight:800}
.vt .vt-note{font-size:14px;line-height:1.4;color:var(--oa-color-text-secondary)}
.vt li.cur .vt-note{color:var(--oa-color-text-primary)}
.tkp .rows.vt4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));column-gap:24px;border-top:0}
.tkp .rows.vt4 .row{display:block;border-top:2px solid var(--oa-color-border-strong);border-bottom:0}
.mx .vt li{min-height:calc(var(--d) + 14px);padding-bottom:0}
.mx .vt .vt-n{font-size:13px}
.vt-page li{padding-bottom:14px}
.vt-page .vt-n{font-size:16px}.vt-page .vt-s{font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-text-secondary)}
.vt-page .vt-note{font-size:15px;line-height:1.5;margin-top:2px;color:var(--oa-color-text-primary)}
.tbox{margin:12px 0 4px;padding:14px;border:2px solid var(--oa-color-border-strong)}
.tbox .tp{margin:0 0 12px}
.askw{margin:0}
.ask{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;background:var(--oa-color-palette-pillar-red);color:var(--oa-color-palette-white);font:var(--oa-type-ask);border:1.5px solid var(--oa-color-palette-charcoal)}
.bp .kick{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:0 0 12px}
.bp-h{font:800 26px/1.08 var(--oa-font-family-display);letter-spacing:-.01em;margin:0 0 8px}
.tkp--l .bp-h{font-size:32px}
.bp-dek{font-size:17px;line-height:1.5;margin:0 0 12px}
.bp > .st{margin:0 0 20px;padding-bottom:16px;border-bottom:1px solid var(--oa-color-border-hairline)}
.bp-cols{display:grid;grid-template-columns:600px 1fr;column-gap:48px}
.bp-aside{font-size:14px;line-height:1.45;border-top:2px solid var(--oa-color-border-strong);padding-top:12px}
.bp-key{margin:0;padding-left:0;list-style:none}.bp-key li{margin:0 0 8px}

/* kicker, identity applications */
.kick{display:inline-flex;align-items:center;gap:12px;flex-wrap:wrap}
.kick-l{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase}
.chip-id{display:inline-flex;font:600 13px/1 var(--oa-font-family-reading);border:1px solid var(--oa-color-border-strong, #121212)}
.chip-id span{padding:5px 6px}.chip-id span:first-child{background:var(--tk-ink);color:var(--tk-bg)}
.idm{display:block;flex:none}
.lk-c{color:var(--oa-color-palette-newsprint)}
.am{padding:18px 20px}
.am-mast{width:660px;border-bottom:2px solid var(--oa-color-palette-charcoal);color:var(--oa-color-palette-charcoal)}
.am-head{width:520px;display:flex;align-items:center;gap:12px;border-bottom:1px solid var(--oa-color-palette-stone);color:var(--oa-color-palette-charcoal)}
.am-head .pg{margin-left:auto;font:600 13px/1 var(--oa-font-family-reading);font-variant-numeric:tabular-nums}
.am-foot{width:560px;display:flex;align-items:center;gap:14px}
.ft-t{display:flex;flex-direction:column;gap:2px;font-size:14px}
.ft-t .tag{font:italic 400 15px/1.4 var(--oa-font-family-quote)}
.am-sign{width:320px;height:200px;position:relative;border:1px solid var(--oa-color-palette-stone);padding:0}
.am-sign .sg-l{position:absolute;left:16px;top:14px;font-size:13px;color:var(--oa-color-derived-deep-stone);max-width:200px;line-height:1.35}
.am-sign .idm{position:absolute;right:72px;bottom:72px}
.am-sign::after{content:"";position:absolute;left:0;top:0;right:72px;bottom:72px;border-right:1px dashed var(--oa-color-palette-stone);border-bottom:1px dashed var(--oa-color-palette-stone);pointer-events:none}
.am-sign .sg-m{position:absolute;right:8px;bottom:8px;font-size:13px;color:var(--oa-color-derived-deep-stone)}
.am-kick{width:560px;border:1px solid var(--oa-color-palette-stone)}
.kick-hl{font:800 24px/1.12 var(--oa-font-family-display);letter-spacing:-.01em;margin:12px 0 0;max-width:none}
.ba{display:grid;grid-template-columns:minmax(0,5fr) minmax(0,7fr);gap:24px 48px;margin-top:20px}
.ba-col{min-width:0}
.ba-list{list-style:none;margin:0;padding:0}
.ba-before li{display:grid;grid-template-columns:auto minmax(0,1fr);gap:16px;align-items:center;padding:14px 0;border-top:1px solid var(--oa-color-palette-stone)}
.ba-mark{display:flex;align-items:center;min-width:40px}
.ba-t{font-weight:700;margin:0}.ba-k{font-size:.9375rem;margin:0}.ba-r{font-size:.875rem;color:var(--oa-color-derived-deep-stone);margin:0}
.ba-after li{padding:14px 0 16px;border-top:1px solid var(--oa-color-palette-stone)}
.ba-app{overflow-x:auto;max-width:100%;margin-bottom:8px}
.kick-old .mk{display:block}

/* comparison */
.mxw{overflow-x:auto;margin-top:16px}
.mx{table-layout:fixed;min-width:1180px;border-top:2px solid var(--oa-color-palette-charcoal)}
.mx th,.mx td{padding:14px 12px 16px 0}
.mx thead th{vertical-align:bottom}
.mx thead th:first-child,.mx tbody th{width:150px}
.mx .mx-o{display:block;font:800 1.0625rem/1.2 var(--oa-font-family-display);letter-spacing:-.005em;text-transform:none;color:var(--oa-color-palette-charcoal);margin:4px 0 6px}
.mx tbody th span{display:block;font-weight:400}
.mx td{font-size:14px;line-height:1.45}
.mx td p{margin:0;max-width:none}
.mx td .st{margin-top:6px}.mx td .tp{display:flex;gap:6px;align-items:flex-start;margin-top:4px}
.mx td .cw{display:flex;align-items:baseline;gap:8px;margin:0 0 2px}
.mx td .cw-w{font:800 17px/1.2 var(--oa-font-family-display)}
.mx td .cw-n{font-size:13px;color:var(--oa-color-derived-deep-stone)}
.mx-c td{font-size:.9375rem}
.lawx{list-style:none;margin:12px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:20px 24px}
.lawx > li{font-size:14px;line-height:1.45;border-top:2px solid var(--oa-color-palette-charcoal);padding-top:10px}
.lawx p{margin:0;max-width:none}.lawx .st{margin-top:6px}
.lawx .cw{display:flex;align-items:baseline;gap:8px;margin:0 0 2px}.lawx .cw-w{font:800 17px/1.2 var(--oa-font-family-display)}
.lawx .cw-n{font-size:13px;color:var(--oa-color-derived-deep-stone)}
.lawx .vt li{min-height:calc(var(--d) + 14px);padding-bottom:0}.lawx .vt .vt-n{font-size:13px}

/* decisions */
.decs{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr))}
.dec{background:var(--oa-color-palette-white);border:1px solid var(--oa-color-palette-stone);padding:20px 24px}
.dec-id{font:800 1.5rem/1 var(--oa-font-family-display);margin:0 0 6px}
.dec-q{font:700 1.125rem/1.4 var(--oa-font-family-reading);margin:0 0 10px}
.dec-o{list-style:none;margin:0 0 10px;padding:0}.dec-o li{margin:0 0 6px}.dec-o b{display:inline-block;min-width:1.4em}
.dec-why{margin:0;font-size:.9375rem}
.foot{margin-top:64px;border-top:2px solid var(--oa-color-palette-charcoal);padding-top:16px;font-size:.875rem;color:var(--oa-color-derived-deep-stone)}

@media (forced-colors: active){
.mk .fi{fill:CanvasText}.mk .fs{fill:GrayText}.mk .fb{fill:Canvas}.mk .ft{fill:CanvasText}.mk .fr{fill:Highlight}
.mk .si,.mk .sk{stroke:CanvasText}.mk .ss{stroke:GrayText}.mk text.halo{stroke:Canvas}
.vt li::after{background:CanvasText}.vt li.seg-off::after{background:GrayText}
.chip-id span:first-child{forced-color-adjust:none;background:CanvasText;color:Canvas}
}
@media (max-width:1000px){.ba{grid-template-columns:minmax(0,1fr)}.bp-cols{grid-template-columns:600px 280px}}
@media (max-width:760px){
.board{padding:24px 16px 64px}
.mast{flex-direction:column;gap:6px}.mast span{text-align:left}
.lede p{font-size:1.0625rem}
table.stk,table.stk tbody,table.stk tr,table.stk th,table.stk td{display:block;width:100%}
table.stk thead{display:none}table.stk tr{border-bottom:1px solid var(--oa-color-palette-stone);padding:10px 0}
table.stk th,table.stk td{border:0;padding:2px 0}
td.n{width:auto}
.mx{min-width:0;table-layout:auto;border-top:0}
.mx,.mx tbody,.mx tr,.mx th,.mx td{display:block;width:100%}
.mx thead{display:none}
.mx tr{border-top:2px solid var(--oa-color-palette-charcoal);padding:12px 0 4px;margin-bottom:12px}
.mx tbody th,.mx td{width:auto;border:0;padding:6px 0 12px}
.mx td::before{content:attr(data-label);display:block;font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);margin-bottom:6px}
.recbox,.dec{padding:16px}
.am-mast,.am-head,.am-foot,.am-kick{width:auto;min-width:0}
.am-mast .idm{width:200px;height:auto}
.am-head{flex-wrap:wrap}.am-foot{align-items:flex-start}
}
"""

JS = r"""
(function(){
  function upd(){
    document.querySelectorAll('.frame,.mxw,.ba-app').forEach(function(f){
      if (f.scrollWidth > f.clientWidth + 1) { f.tabIndex = 0; f.classList.add('is-wide'); }
      else { f.removeAttribute('tabindex'); f.classList.remove('is-wide'); }
    });
  }
  window.addEventListener('resize', upd);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(upd);
  upd();
})();
"""


def curl_page(page):
    """Typographic quotes and apostrophes in every text node, outside tags, styles and scripts."""
    parts = re.split(r'(<style[^>]*>.*?</style>|<script[^>]*>.*?</script>|<[^>]+>)', page, flags=re.S)
    out = []
    for part in parts:
        if part.startswith('<'):
            out.append(part)
        else:
            t = part.replace('&quot;', '"').replace('&#x27;', "'")
            out.append(copy(t))
    return ''.join(out)


def build():
    meas = json.loads(MEAS.read_text()) if MEAS.exists() else None
    tokens = TOKENS.read_text()
    head_rec = ('<div class="recbox"><p class="key-h">What we recommend</p>'
                '<p>We recommend six plain steps in place of the nine stages. Option B, numbered steps, fits lists and story cards, '
                'and Option D sets the same steps as a timeline on a bill\'s own page. The lockmark keeps four fixed places, '
                'the masthead, page headers, footers and the sign-off, while every grid that codes something retires.</p></div>')
    toc = [('six-steps', 'Six steps'), ('compare', 'Compare the four'), ('option-a', 'Option A'), ('option-b', 'Option B'),
           ('option-c', 'Option C'), ('option-d', 'Option D'), ('grid', 'The grid\'s one job'), ('checks', 'Checks'),
           ('answers', 'Your answers')]
    tocs = ''.join(f'<li><a href="#{a}">{E(t)}</a></li>' for a, t in toc)
    body = ''.join([
        sec_steps(), sec_compare(),
        option_section(OPT['A'], 3), option_section(OPT['B'], 4), option_section(OPT['C'], 5), option_section(OPT['D'], 6),
        sec_grid(), sec_checks(meas), sec_decisions(),
    ])
    deck = ('You asked for a bill tracker a newcomer can read at once, "like a line with dots or a 1, 2, 3, 4, 5, 6 step process", '
            'and for the grid to keep one job. This section proposes six plain steps and draws four trackers with them in your '
            'four-bill list. It ends with where the lockmark stays.')
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bill Tracker Options</title>
<meta name="description" content="Board 6, section 1: six plain steps for the bill tracker, four tracker options, and the lockmark's four fixed places.">
<meta name="chart-views" content="overview">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{A(FONTS)}" rel="stylesheet">
<style>
{tokens}
</style>
<style>{CSS}</style>
</head>
<body class="oa-surface-newsprint">
<main class="board" id="overview" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Board 6, section 1 of 4 · November 7, 2026</span></div>
<p class="eyebrow">Board 6 · Systems designer</p>
<h1>Six plain steps for the bill tracker, and one job for the grid</h1>
<p class="deck">{E(deck)}</p>
{head_rec}
<nav aria-label="On this board"><ul class="toc">{tocs}</ul></nav>
</header>
{body}
<footer class="foot"><p>Built by <code>work/build/scripts/phase-2/board6_tracker_build.py</code> on November 7, 2026, from the approved masters and <code>tokens.css</code>. Every bill, date, committee and section title in the specimens is invented, and each piece carries one Illustrative label at its head (DR-97). Notes: <code>work/handoffs/phase-2/20261107_Board-6-Tracker-Notes.md</code>.</p></footer>
</main>
<script>{JS}</script>
</body>
</html>
'''
    head, sep, rest = page.partition('<body')
    page = head + curl_page(sep + rest)
    # lint the copy: strip tags, styles and scripts first
    text = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', page, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    lint_text(html.unescape(text), 'page copy')
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    for w in LINT:
        print('warning', w)
    print(f'wrote {OUT.relative_to(ROOT)} ({len(page) / 1024:.0f} KB){" with measurements" if meas else ""}')


if __name__ == '__main__':
    build()
