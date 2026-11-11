"""Chapter 17, Motion and states (systems designer), stage C round 1, November 11, 2026.

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_ch17_build.py           write the chapter, specimens and manifest
    python3 -I work/build/scripts/phase-2/stage_c_ch17_build.py --check   build everything in memory and report, write nothing

Writes:
    work/build/guide/chapters/17-motion-and-states.json      the chapter, in chapter 11's content contract
    work/build/guide/specimens/s-17-*.html                   one fragment per specimen this generator owns
    work/build/guide/specimens/manifest-motion.json          this chapter's manifest (D2-1267); written whole
    work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json   every figure the chapter prints, and how

Reads, never writes: work/build/tokens/tokens.json and tokens.css (the nine motion tokens, the state roles and the two
themes), and work/build/guide/specimens/manifest-identity.json for the identity designer's Rule 17.6 specimens.

Rule numbers 17.1 to 17.10 are fixed by the round 1 brief; 17.11 (disabled) and 17.12 (empty) are this generator's.

Rule 17.6 belongs to the identity designer's motion. Its specimens are named s-17-hinge-* and s-17-lever-* and sit in
manifest-identity.json, made by that designer's own generator. On every run this script looks for them there:
    s-17-hinge-correct     the rule's correct plate (else s-17-lever-correct)
    s-17-hinge-failure     the rule's failure plate (else s-17-lever-failure)
    any other s-17-hinge-* or s-17-lever-*   an extra plate after Rule 17.6, in name order
Each takes its caption from the manifest entry's "caption" (and an extra its "label"), so the identity designer writes
those words. Until a slot is filled, it shows this generator's pending marker (s-17-6-pending, s-17-6-pending-failure),
an ordinary specimen that says what is coming, so the build stays clean. Rerun this script after the identity designer
lands; the pending markers then leave the manifest.

Motion specimens (D2-xxx in the notes): every player root carries data-oa-motion and data-frame; one button carries
Play and Pause (data-oa-play data-oa-pause), as the utility icons' rule sets one button for both; Reset carries
data-oa-reset. Nothing moves until a press. Durations and easings are read from tokens.css by name at the moment of
the press, so under prefers-reduced-motion every duration is 0 ms and Play draws the last frame at once. Motion runs
through the Web Animations API, so no @keyframes sits inside the build's @scope.

Specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color, no
px font size; every class is prefixed sx- so no name meets a shell class. Colors in theme cells read only role names
that data-oa-theme points at Newsprint or Charcoal (D2-1159).
"""
import argparse
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
OUT_CH = ROOT / 'work/build/guide/chapters/17-motion-and-states.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-motion.json'
ID_MANIFEST = OUT_SP / 'manifest-identity.json'
FIG_OUT = ROOT / 'work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json'
INVENTORY = ROOT / 'work/build/assets/civic-line-v6/20261110_Civic-Line-V6-Inventory.json'
N_LIB = len(json.loads(INVENTORY.read_text())['icons'])     # the symbol library's count, as chapter 11 reads it
CH = '17'
ILLUS = B.ILLUS
RED_ERR = 'data-red="working" data-red-job="error"'
NB = C.NBSP

T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
ctx = B.Ctx(T, {}, 'final')


# ------------------------------------------------------------------------------------------------ tokens and figures
def ms(name):
    val, unit = T.dim(f'oa.motion.duration.{name}')
    return int(val * 1000) if unit == 's' else int(val)


def bez(name):
    return T.value(f'oa.motion.easing.{name}')


FAST, STD, SLOW, STAG, HINGE, LEVER = (ms(n) for n in ('fast', 'standard', 'slow', 'stagger', 'hinge', 'lever'))
LAND_FROM = 1.12          # D2-xxx: a land starts at 112 percent, our fifth edition's lever step, 1.4 / 1.25
assert abs(1.4 / 1.25 - LAND_FROM) < 1e-9


def tokcss(name):
    """A CSS custom property name, checked against tokens.css."""
    if name not in T.css_names:
        raise KeyError(f'{name} is not in tokens.css')
    return name


def r(fg, bg, key=None):
    return ctx.ratio(fg, bg, key)


def bz(name):
    return 'cubic-bezier(' + ', '.join(f'{x:g}' for x in bez(name)) + ')'


ctx.fig('motion durations', {n: ms(n) for n in ('fast', 'standard', 'slow', 'stagger', 'hinge', 'lever')},
        'tokens.json oa.motion.duration, read by this generator')
ctx.fig('motion easings', {n: bz(n) for n in ('standard', 'enter', 'exit')}, 'tokens.json oa.motion.easing')
ctx.fig('land from', '112 percent', 'our fifth edition’s lever landed at 1.4 times a node and settled at 1.25 (Phase 0 '
        'text census, V5 chapter 12); 1.4 / 1.25 = 1.12')

# The figures the chapter prints, each computed from tokens.json (WCAG 2.x relative luminance)
F = {
    'dis_n': r('oa.color.state.disabled.text.onNewsprint', 'oa.color.surface.newsprint'),
    'dis_c': r('oa.color.state.disabled.text.onCharcoal', 'oa.color.surface.charcoal'),
    'ring_n': r('oa.color.focus.ring.onNewsprint', 'oa.color.surface.newsprint'),
    'ring_w': r('oa.color.focus.ring.onWhite', 'oa.color.surface.white'),
    'ring_c': r('oa.color.focus.ring.onCharcoal', 'oa.color.surface.charcoal'),
    'ring_p': r('oa.color.focus.ring.onPrussian', 'oa.color.surface.prussian'),
    'ring_on_fill_c': r('oa.color.focus.ring.onCharcoal', 'oa.color.action.primary.fill.onCharcoal',
                        'focus ring on Charcoal against the Newsprint primary fill'),
    'hover_n': r('oa.color.action.primary.fill.onNewsprint', 'oa.color.action.primary.fillHover.onNewsprint',
                 'primary fill against its hover fill on Newsprint'),
    'hover_c': r('oa.color.action.primary.fill.onCharcoal', 'oa.color.action.primary.fillHover.onCharcoal',
                 'primary fill against its hover fill on Charcoal'),
    'err_c': r('oa.color.state.error.bar.onCharcoal', 'oa.color.surface.charcoal'),
    'err_n': r('oa.color.state.error.bar.onNewsprint', 'oa.color.surface.newsprint'),
    'err_band': r('oa.color.state.error.bar.onNewsprint', 'oa.color.state.error.band.onNewsprint'),
    'err_text_band': r('oa.color.state.error.text.onNewsprint', 'oa.color.state.error.band.onNewsprint'),
    'load_n': r('oa.color.state.loading.mark.onNewsprint', 'oa.color.surface.newsprint'),
    'load_c': r('oa.color.state.loading.mark.onCharcoal', 'oa.color.surface.charcoal'),
    'load_t_n': r('oa.color.state.loading.text.onNewsprint', 'oa.color.surface.newsprint'),
    'empty_n': r('oa.color.state.empty.edge.onNewsprint', 'oa.color.surface.newsprint'),
    'empty_c': r('oa.color.state.empty.edge.onCharcoal', 'oa.color.surface.charcoal'),
    'ok_n': r('oa.color.state.success.mark.onNewsprint', 'oa.color.surface.newsprint'),
    'ok_c': r('oa.color.state.success.mark.onCharcoal', 'oa.color.surface.charcoal'),
    'muted_mark_n': r('oa.color.state.muted.mark.onNewsprint', 'oa.color.surface.newsprint'),
    'muted_mark_c': r('oa.color.state.muted.mark.onCharcoal', 'oa.color.surface.charcoal'),
    'warn_n': r('oa.color.state.warning.mark.onNewsprint', 'oa.color.surface.newsprint'),
    'warn_c': r('oa.color.state.warning.mark.onCharcoal', 'oa.color.surface.charcoal'),
    'band_n': r('oa.color.state.selected.band.onNewsprint', 'oa.color.surface.newsprint'),
    'band_c': r('oa.color.state.selected.band.onCharcoal', 'oa.color.surface.charcoal'),
    'edge_n': r('oa.color.border.strong.onNewsprint', 'oa.color.surface.newsprint'),
    'edge_c': r('oa.color.border.strong.onCharcoal', 'oa.color.surface.charcoal'),
    'red_text_n': r('oa.color.palette.pillarRed', 'oa.color.surface.newsprint', 'Pillar Red words on Newsprint'),
    'verd_text_n': r('oa.color.palette.verdigris', 'oa.color.surface.newsprint', 'Verdigris words on Newsprint'),
}
FADED = C.composite(T.hex('oa.color.palette.charcoal'), T.hex('oa.color.palette.newsprint'), 0.4)
F['faded_n'] = r(FADED, 'oa.color.surface.newsprint', 'Charcoal at 40 percent opacity over Newsprint')
F['faded_w'] = r(C.composite(T.hex('oa.color.palette.charcoal'), T.hex('oa.color.palette.white'), 0.4),
                 'oa.color.surface.white', 'Charcoal at 40 percent opacity over White')

# The failure easing of Rule 17.2: a curve that overshoots its place and comes back
BOUNCE = (0.34, 1.56, 0.64, 1)


def bezier_y_max(x1, y1, x2, y2, n=2000):
    best = 0
    for i in range(n + 1):
        t = i / n
        y = 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3
        best = max(best, y)
    return best


OVER = round((bezier_y_max(*BOUNCE) - 1) * 100)
ctx.fig('overshoot of cubic-bezier(0.34, 1.56, 0.64, 1)', f'{OVER} percent past its place',
        'sampled at 2,001 points of the curve’s progress')


def bezier_y_at(x1, y1, x2, y2, x):
    """Progress of a CSS cubic-bezier easing at time fraction x, by bisection on the curve's own parameter."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        t = (lo + hi) / 2
        xt = 3 * (1 - t) ** 2 * t * x1 + 3 * (1 - t) * t ** 2 * x2 + t ** 3
        lo, hi = (t, hi) if xt < x else (lo, t)
    t = (lo + hi) / 2
    return 3 * (1 - t) ** 2 * t * y1 + 3 * (1 - t) * t ** 2 * y2 + t ** 3


# CD-S2: the failure of Rule 17.4 times a 400 ms draw with the browser's "ease-out", cubic-bezier(0, 0, 0.58, 1); at
# 200 ms, halfway in time, the line is this far along
EASE_OUT_HALF = bezier_y_at(0, 0, 0.58, 1, 0.5)
ctx.fig('ease-out at half its time', f'{round(EASE_OUT_HALF * 100)} percent of the way',
        'cubic-bezier(0, 0, 0.58, 1), the CSS keyword ease-out, solved for progress at time 0.5 by bisection')


# ------------------------------------------------------------------------------------------------ small parts
def ty(name):
    return ctx.ty(name)


def uicon(name, px=24, cls=None, transform=None):
    """A utility icon from the sprite, hidden beside its word and tagged for the checks (D2-517)."""
    c = f' class="{cls}"' if cls else ''
    t = f' transform="{transform}"' if transform else ''
    return (f'<svg{c} viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" focusable="false" '
            f'data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"{t}/></svg>')


def fail_band():
    css, html = ctx.fail_band()
    return css, html


# ------------------------------------------------------------------------------------------------ tracker marks
# Chapter 11's numbered steps (Board 6, Option B), drawn here with the same classes and token reads so the guide's
# mark checks (markTokens, B-3, A-5) measure them as they measure chapter 11's. The 26 px circle of chapter 11's
# 360 px list. Colors through --ink, --sub, --bg and --txt2, set on the stage from the role names.
DIA = 26
RAD = DIA / 2
MARK_CSS = ('.mk{display:block;overflow:visible;flex:none;max-width:100%;height:auto}'
            '.mk .fi{fill:var(--ink)}.mk .fs{fill:var(--sub)}.mk .fb{fill:var(--bg)}.mk .ft{fill:var(--txt2)}'
            '.mk .si{stroke:var(--ink)}.mk .ss{stroke:var(--sub)}.mk .nf{fill:none}'
            '.mk text{font-family:var(--oa-font-family-reading);font-weight:700;font-variant-numeric:tabular-nums;'
            'text-anchor:middle;font-size:0.8125rem;letter-spacing:0;text-transform:none}.mk text.tl{font-weight:600}'
            '.mk .rn{stroke-width:var(--oa-component-mark-ring-now)}.mk .ra{stroke-width:var(--oa-component-mark-ring-ahead)}'
            '.mk .lr{height:var(--oa-component-mark-line-reached)}.mk .la{height:var(--oa-component-mark-line-ahead)}')
MARK_VARS = ('--ink:var(--oa-color-graphic-essential);--sub:var(--oa-color-graphic-subtle);--bg:var(--oa-color-surface);'
             '--txt2:var(--oa-color-text-secondary)')
STATE_ICON = {'done': 'S-done', 'now': 'S-now', 'notyet': 'S-not-yet'}


def when(w):
    return f' data-when="{w}"' if w else ''


def step(cx, cy, st, num, w=None):
    ty_ = f'{cy + 0.36 * 13:.2f}'
    if st == 'done':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{RAD:g}" class="fi"/><text x="{cx:g}" y="{ty_}" class="fb">{num}</text>'
    elif st == 'now':
        s = (f'<circle cx="{cx:g}" cy="{cy:g}" r="{RAD - 1.5:g}" class="fb si rn" stroke-width="3"/>'
             f'<text x="{cx:g}" y="{ty_}" class="fi">{num}</text>')
    else:
        s = (f'<circle cx="{cx:g}" cy="{cy:g}" r="{RAD - 0.75:g}" class="fb ss ra" stroke-width="1.5"/>'
             f'<text x="{cx:g}" y="{ty_}" class="ft tl">{num}</text>')
    box = f'<rect x="{cx - RAD:g}" y="{cy - RAD:g}" width="{DIA}" height="{DIA}" fill="none"/>'
    return f'<g data-icon="{STATE_ICON[st]}" data-icon-family="status"{when(w)}>{box}{s}</g>'


def seg(x1, x2, cy, reached, w=None, part=None):
    p = f' data-part="{part}"' if part else ''
    if reached:
        return f'<rect x="{x1:g}" y="{cy - 1:g}" width="{x2 - x1:g}" height="2" class="fi lr"{when(w)}{p}/>'
    return f'<rect x="{x1:g}" y="{cy - 1:g}" width="{x2 - x1:g}" height="1" class="fs la"{when(w)}{p}/>'


TW = 264          # six 44 px steps: the content width of a fluid plate at 360 px (frame, stage and inset each pad 16 px)
TXS = [TW // 6 * i + TW // 12 for i in range(6)]
TCY = 6 + RAD
TH = int(TCY + RAD + 2)


def tracker_svg(states):
    """A still tracker: six numbered steps in one state each."""
    body = [seg(TXS[i], TXS[i + 1], TCY, states[i + 1] != 'notyet') for i in range(5)]
    body += [step(x, TCY, s, i + 1) for i, (x, s) in enumerate(zip(TXS, states))]
    return f'<svg class="mk" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}" aria-hidden="true" focusable="false">{"".join(body)}</svg>'


START = ['done', 'done', 'now', 'notyet', 'notyet', 'notyet']
END = ['done', 'done', 'done', 'now', 'notyet', 'notyet']


def tracker_motion_svg():
    """The live tracker: the parts that stay, the start and end versions of the parts that change, and the layers that
    move only while the motion runs (untagged, since they are the motion, not a mark)."""
    x3, x4 = TXS[2], TXS[3]
    body = []
    for i in range(5):
        if i == 2:
            body.append(seg(TXS[i], TXS[i + 1], TCY, False, 'start'))
            body.append(seg(TXS[i], TXS[i + 1], TCY, True, 'end'))
            body.append(seg(TXS[i], TXS[i + 1], TCY, True, 'run', 'grow'))
        else:
            body.append(seg(TXS[i], TXS[i + 1], TCY, START[i + 1] != 'notyet'))
    for i, x in enumerate(TXS):
        if START[i] == END[i]:
            body.append(step(x, TCY, START[i], i + 1))
        else:
            body.append(step(x, TCY, START[i], i + 1, 'start'))
            body.append(step(x, TCY, END[i], i + 1, 'end'))
    ty_ = f'{TCY + 0.36 * 13:.2f}'
    body.append(f'<g data-part="land" data-when="run"><circle cx="{x3:g}" cy="{TCY:g}" r="{RAD:g}" class="fi"/>'
                f'<text x="{x3:g}" y="{ty_}" class="fb">3</text></g>')
    body.append(f'<g data-part="slide" data-when="run"><circle cx="{x3:g}" cy="{TCY:g}" r="{RAD - 1.5:g}" '
                f'class="si nf rn" stroke-width="3"/></g>')
    return (f'<svg class="mk" width="{TW}" height="{TH}" viewBox="0 0 {TW} {TH}" aria-hidden="true" focusable="false">'
            f'{"".join(body)}</svg>'), x4 - x3


# ------------------------------------------------------------------------------------------------ the mechanism link
# Loop R1's first link from our systems atlas, as chapter 11's stepper words it (DR-195): "Wealth concentration raises
# money in politics." Two nodes and the link between them. Plain nodes, untagged: they are a diagram, not status marks.
#
# CD-S3 and CA-S5: each node's name sits centered under its node, on one baseline with the other. The drawing therefore
# flows with its column up to 26rem: the nodes stand at fixed shares of its width, 28 and 78.5 percent, the centers of
# the two name columns under it (0 to 56 percent and 57 to 100 percent), so both names
# fit on one line at 14 px from about 290 px, and each wraps to two lines, still centered, below that. The nodes, the line and the arrowhead keep their true sizes at every width; only the
# link's length changes. The line runs from center to center under a halo of the ground around each node, 4 px wide,
# so it shows from 4 px past the first node to the arrowhead's point, 4 px short of the second, as before.
MH = 40
MCY = 20
MR = 8
HALO = MR + 4
MA_P, MB_P = 28, 78.5                  # percent of the drawing's width
NAME_COLS = '56fr 1fr 43fr'            # name columns centered on 28 and 78.5 percent
MECH_MAX = '26rem'
TIP = f'M-{HALO + 7} {MCY - 7}L-{HALO} {MCY}L-{HALO + 7} {MCY + 7}'   # drawn at the second node, its point 4 px short


def _line(extra=''):
    return f'<line x1="{MA_P}%" y1="{MCY}" x2="{MB_P}%" y2="{MCY}" class="ln"{extra}/>'


def _tip(inner_attrs=''):
    return f'<svg x="{MB_P}%" y="0" overflow="visible"><g{inner_attrs}><path d="{TIP}" class="ln"/></g></svg>'


def _node(pct, cls, r=MR, attrs=''):
    return f'<circle cx="{pct}%" cy="{MCY}" r="{r:g}" class="{cls}"{attrs}/>'


def _halos():
    return ''.join(f'<circle cx="{x}%" cy="{MCY}" r="{HALO}" class="hal"/>' for x in (MA_P, MB_P))


def _svg(body):
    return (f'<svg class="dg dgl" width="100%" height="{MH}" aria-hidden="true" focusable="false" overflow="visible">'
            f'{body}</svg>')


def mech_svg(state, frac=None):
    """A still frame of the link: 'start' (the cause alone) or 'end' (the link drawn, the effect reached). With frac,
    a 'start' frame draws that share of the link's line, as a frame part way through a draw does (CD-S2)."""
    a = _node(MA_P, 'nd-on')
    if state == 'start':
        ln = _line(f' pathLength="1" stroke-dasharray="{frac:.3f} 1"') if frac else ''
        return _svg(ln + _halos() + a + _node(MB_P, 'nd-off', MR - 0.75))
    return _svg(_line() + _halos() + _tip() + a + _node(MB_P, 'nd-on'))


def mech_motion_svg():
    body = [
        _line(' data-when="end"'),
        _line(' pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" data-when="run" data-part="draw"'),
        _halos(),
        _tip().replace('<g>', '<g data-when="end">'),
        _tip(' data-when="run" data-part="tip" data-wait=""'),
        _node(MA_P, 'nd-on'),
        _node(MB_P, 'nd-off', MR - 0.75, ' data-when="start"'),
        _node(MB_P, 'nd-on', MR, ' data-when="end"'),
        f'<g data-when="run" data-part="land" data-wait="">{_node(MB_P, "nd-on")}</g>',
    ]
    return _svg(''.join(body))


MECH_NAMES = '<p class="nn"><span>Wealth concentration</span><span>Money in politics</span></p>'
MECH_CSS = ('.lk{max-width:' + MECH_MAX + '}.dgl{width:100%;max-width:' + MECH_MAX + ';height:' + str(MH) + 'px}'
            '.dg .hal{fill:var(--oa-color-surface)}'
            '.nn{display:grid;grid-template-columns:' + NAME_COLS + ';align-items:start;margin-top:6px;' + ty('caption') + '}'
            # 6 px inside each column keeps the two names at least 12 px apart; a name that cannot keep it wraps under its node
            '.nn span{padding:0 6px;text-align:center;text-wrap:balance}.nn span + span{grid-column:3}')


def mech_stage(svg):
    """The drawing with its two node names centered under their nodes (CD-S3, CA-S5)."""
    return f'<div class="lk">{svg}{MECH_NAMES}</div>'


# ------------------------------------------------------------------------------------------------ the three behaviors
SW, SH = 150, 48


def mini_svg(kind, state, live=False):
    """Slide, draw and land on their own, each 150 px wide: plain nodes and one moving part."""
    n = []
    if kind == 'slide':
        a, b, cy = 14, 136, 24
        n.append(f'<rect x="{a}" y="{cy - 0.5:g}" width="{b - a}" height="1" class="hl"/>')
        n.append(f'<circle cx="{a}" cy="{cy}" r="4" class="dot"/><circle cx="{b}" cy="{cy}" r="4" class="dot"/>')
        ring = f'<circle cx="{{x}}" cy="{cy}" r="10.5" class="rg"/>'
        if live:
            n.append(f'<g data-when="first">{ring.format(x=a)}</g><g data-when="end">{ring.format(x=b)}</g>')
            n.append(f'<g data-when="run" data-part="slide">{ring.format(x=a)}</g>')
        else:
            n.append(ring.format(x=a if state == 'start' else b))
    elif kind == 'draw':
        d = 'M22 12H96V36H128'
        n.append('<circle cx="14" cy="12" r="6" class="nd-on"/>')
        if live:
            n.append(f'<path d="{d}" class="ln" data-when="end"/>')
            n.append(f'<path d="{d}" class="ln" pathLength="1" stroke-dasharray="1 1" stroke-dashoffset="1" data-when="run" data-part="draw"/>')
        elif state == 'end':
            n.append(f'<path d="{d}" class="ln"/>')
        n.append('<circle cx="136" cy="36" r="5.25" class="nd-off"/>')
    else:
        cx, cy = 75, 24
        n.append(f'<circle cx="{cx}" cy="{cy}" r="11.25" class="nd-off"/>')
        disc = f'<circle cx="{cx}" cy="{cy}" r="12" class="nd-on"/>'
        if live:
            n.append(f'<g data-when="end">{disc}</g><g data-when="run" data-part="land">{disc}</g>')
        elif state == 'end':
            n.append(disc)
    return (f'<svg class="dg" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}" aria-hidden="true" focusable="false">'
            f'{"".join(n)}</svg>')


# ------------------------------------------------------------------------------------------------ the player
DUR = {'fast': '--oa-motion-duration-fast', 'standard': '--oa-motion-duration-standard', 'slow': '--oa-motion-duration-slow',
       'stagger': '--oa-motion-duration-stagger'}
EASE = {'standard': '--oa-motion-easing-standard', 'enter': '--oa-motion-easing-enter', 'exit': '--oa-motion-easing-exit'}
for _v in list(DUR.values()) + list(EASE.values()):
    tokcss(_v)
REDUCED_VARS = ';'.join(f'{tokcss("--oa-motion-duration-" + n)}:0ms' for n in ('fast', 'standard', 'slow', 'stagger', 'hinge', 'lever'))

PLAYER_CSS = (
    ':scope{' + MARK_VARS + '}'
    + MARK_CSS +
    '.pl{display:grid;grid-template-columns:minmax(0,1fr);gap:12px;max-width:40rem}'
    ':where(.pl p){margin:0}'
    '.k{' + ty('label') + ';color:var(--oa-color-text-secondary)}'
    '.ti{' + ty('h4') + ';text-wrap:balance}'
    '.stg{padding:16px 0 4px}'
    '.out{min-height:3em;' + ty('bodySmall') + '}'
    '.cl{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,8.5rem),1fr));gap:8px;max-width:22rem}'
    '.b{display:inline-flex;align-items:center;gap:8px;min-height:var(--oa-size-target-touch);margin:0;'
    'padding:0 14px 0 10px;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);border-radius:0;'
    'background:var(--oa-color-surface);color:var(--oa-color-text-primary);' + ty('ui') + ';text-align:left;cursor:pointer}'
    '.b svg{flex:none;display:block}.b svg[hidden]{display:none}'
    '.b:hover{border-width:var(--oa-border-width-rule);padding:0 13px 0 9px}'
    '.b[aria-disabled="true"]{color:var(--oa-component-button-disabled-label);border-style:dashed;'
    'border-color:var(--oa-component-button-disabled-edge);cursor:not-allowed}'
    '.b[aria-disabled="true"]:hover{border-width:var(--oa-border-width-hairline);padding:0 14px 0 10px}'
    '.sl{display:flex;align-items:center;gap:10px;min-height:var(--oa-size-target-touch);' + ty('ui') + ';cursor:pointer;'
    'justify-self:start;min-width:0}'
    '.sl input{flex:none;width:24px;height:24px;margin:0;accent-color:var(--oa-color-graphic-essential)}'
    '.sl[data-off]{color:var(--oa-color-state-disabled-text);cursor:not-allowed}'
    '.why,.dv{' + ty('caption') + ';color:var(--oa-color-text-secondary)}'
    '.why:empty{display:none}'
    '.sv{display:grid;gap:10px;padding-top:12px;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
    '.fr{list-style:none;margin:0;padding:0;display:grid;gap:12px 24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,var(--fw,19rem)),1fr))}'
    '.fr li{display:grid;gap:8px;align-content:start}'
    '.fh{' + ty('caption') + '}.fh b{font-weight:700}'
    '.fw{' + ty('caption') + '}'
    '.tl{margin:0;padding:0;list-style:none;display:grid;gap:2px;' + ty('caption') + '}.tl b{font-weight:700}'
    '.dg{display:block;overflow:visible;max-width:100%;height:auto}'
    '.dg .nd-on{fill:var(--oa-color-graphic-essential)}'
    '.dg .nd-off{fill:var(--oa-color-surface);stroke:var(--oa-color-graphic-subtle);stroke-width:1.5}'
    '.dg .ln{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:2;stroke-linejoin:round;stroke-linecap:butt}'
    '.dg .hl{fill:var(--oa-color-border-hairline)}'
    '.dg .dot{fill:var(--oa-color-graphic-subtle)}'
    '.dg .rg{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:3}'
    + MECH_CSS +
    '.gd{' + ty('bodySmall') + ';max-width:36rem;margin-top:4px}'
    '.cn{position:relative}.cn > .nb{position:absolute;top:-12px;left:-12px;'
    'box-shadow:0 0 0 2px var(--oa-color-surface)}'
    '.an.row2{gap:20px 28px}'
    # frames: the data-when layers show by the player's data-frame (start, run or end)
    '[data-oa-motion]:not([data-frame="end"]) [data-when="end"]{display:none}'
    '[data-oa-motion][data-frame="end"] [data-when="start"]{display:none}'
    '[data-oa-motion]:not([data-frame="run"]) [data-when="run"]{display:none}'
    '[data-oa-motion]:not([data-frame="start"]) [data-when="first"]{display:none}'
    '[data-wait]{visibility:hidden}'
    '[data-part]{transform-box:fill-box;transform-origin:center}'
    '[data-part="grow"]{transform-origin:0 50%}'
    '[data-oa-motion][data-preview="reduced"]{' + REDUCED_VARS + '}'
    '.nb{display:inline-grid;place-items:center;flex:none;width:24px;height:24px;border-radius:50%;'
    'background:var(--oa-color-graphic-essential);color:var(--oa-color-surface);' + ty('label') + ';letter-spacing:0}'
    '.ax{display:grid;grid-template-columns:24px minmax(0,1fr);gap:10px;align-items:start}'
    '.row2{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center}.row2 .b{min-width:min(100%,8.5rem)}'
    '.pair{display:inline-flex;gap:10px;align-items:center;max-width:100%}'
)

# The player's script: one copy per motion specimen. It finds every player inside its own specimen and wires each.
PLAYER_JS = r"""(function(){var S=document.currentScript.closest("[data-specimen]");if(!S)return;
var RM=window.matchMedia?window.matchMedia("(prefers-reduced-motion: reduce)"):null;
function tok(el,n){var v=getComputedStyle(el).getPropertyValue(n).trim(),x=parseFloat(v);if(isNaN(x))return 0;return /ms$/.test(v)?x:(/s$/.test(v)?x*1000:x);}
function ez(el,n){return getComputedStyle(el).getPropertyValue(n).trim()||"linear";}
S.querySelectorAll("[data-oa-motion]").forEach(function(P){
var M=JSON.parse(P.querySelector("script[data-motion]").textContent),B=P.querySelector("[data-oa-play]"),R=P.querySelector("[data-oa-reset]"),
L=P.querySelector("input[data-slow]"),V=P.querySelector("input[data-preview]"),W=P.querySelector("[data-why]"),O=P.querySelector("[data-out]"),
D=P.querySelector("[data-device]"),I=B.querySelectorAll("svg"),Y=B.querySelector("[data-word]"),A=[],run=0,st="start";
function total(){return M.tracks.reduce(function(s,t){return s+tok(P,t.dur);},0);}
function dev(){return !!(RM&&RM.matches);}
function off(el,y){if(!el)return;var lab=el.closest("label");if(y){el.setAttribute("aria-disabled","true");el.setAttribute("aria-describedby",W.id);if(lab)lab.setAttribute("data-off","");}
else{el.removeAttribute("aria-disabled");el.removeAttribute("aria-describedby");if(lab)lab.removeAttribute("data-off");}}
function show(){var z=total()===0,why=[];I[0].toggleAttribute("hidden",st==="running");I[1].toggleAttribute("hidden",st!=="running");
Y.textContent=st==="running"?"Pause":(st==="end"?"Play again":"Play");
off(R,st==="start");if(st==="start")why.push(M.why.start);
if(L){off(L,z);if(z)why.push(dev()?M.why.slowDevice:M.why.slowPreview);}
if(V){if(dev()){V.checked=true;off(V,true);why.push(M.why.previewDevice);}else off(V,false);}
if(D)D.textContent=dev()?M.device.reduce:M.device.full;W.textContent=why.join(" ");}
function frame(f){P.setAttribute("data-frame",f);}
function end(){run++;A.forEach(function(a){a.cancel();});A=[];frame("end");st="end";O.textContent=M.words.end;show();}
function reset(quiet){run++;A.forEach(function(a){a.cancel();});A=[];frame("start");st="start";if(!quiet)O.textContent=M.words.start;show();}
function play(){if(st==="paused"){A.forEach(function(a){if(a.oaHeld){a.oaHeld=false;a.play();}});st="running";O.textContent=M.words.run;show();return;}
if(st==="end")reset(true);if(total()===0){end();return;}
frame("run");st="running";var my=++run,rate=L&&L.checked?0.1:1;
A=M.tracks.map(function(t){var el=P.querySelector('[data-part="'+t.part+'"]'),d=(t.at||[]).reduce(function(s,n){return s+tok(P,n);},0);
var a=el.animate(t.frames,{duration:tok(P,t.dur),easing:ez(P,t.ease),delay:d,fill:t.fill||"both"});a.playbackRate=rate;return a;});
O.textContent=M.words.run;Promise.all(A.map(function(a){return a.finished;})).then(function(){if(my===run)end();},function(){});show();}
function pause(){A.forEach(function(a){if(a.playState==="running"){a.oaHeld=true;a.pause();}});st="paused";O.textContent=M.words.pause;show();}
B.addEventListener("click",function(){if(st==="running")pause();else play();});
R.addEventListener("click",function(){if(R.getAttribute("aria-disabled")!=="true")reset(false);});
[L,V].forEach(function(c){if(c)c.addEventListener("click",function(e){if(c.getAttribute("aria-disabled")==="true")e.preventDefault();});});
if(L)L.addEventListener("change",function(){var k=L.checked?0.1:1;A.forEach(function(a){a.updatePlaybackRate(k);});});
if(V)V.addEventListener("change",function(){if(V.checked)P.setAttribute("data-preview","reduced");else P.removeAttribute("data-preview");if(total()===0&&(st==="running"||st==="paused"))end();else show();});
if(RM&&RM.addEventListener)RM.addEventListener("change",function(){if(total()===0&&(st==="running"||st==="paused"))end();else show();});
show();});})();"""


def player(pid, *, kicker, title, drawing, below='', words, frames, timeline, motion, why, slow=True, preview=False,
           group, static=False, fw=None, sub=None):
    """One motion player. static=True draws the same parts as a picture (no controls, no script, no data-oa-motion),
    with numbered badges for the anatomy plate of Rule 17.3, numbered top to bottom (CD-S1). sub is a line under the
    title, such as a loop's evidence grade."""
    wid = f'{pid}-why'
    play_icons = uicon('play') + uicon('pause').replace('<svg ', '<svg hidden ', 1)

    def badge(n):
        return f'<span class="nb" aria-hidden="true">{n}</span>' if static else ''

    def row(n, inner):
        return f'<div class="ax">{badge(n)}<div>{inner}</div></div>' if static else inner

    head = ''
    if kicker or title:
        k = f'<p class="k">{kicker}</p>' if kicker else ''
        t = f'<p class="ti">{title}</p>' if title else ''
        g = f'<p class="gd">{sub}</p>' if sub else ''
        head = f'<div>{k}{t}{g}</div>'
    stage = f'<div class="stg">{drawing}{below}</div>'
    out = f'<p class="out"{"" if static else " role=\"status\" data-out=\"\""}>{words["start"]}</p>'
    if static:
        # Play takes its number in the margin, as every other part does; Reset's sits off its top left corner (CD-S1)
        ctl = row(3, f'<div class="row2 an"><span class="b">{play_icons}<span>Play</span></span>'
                     f'<span class="b cn" aria-disabled="true">{badge(4)}{uicon("reset")}<span>Reset</span></span></div>')
        sl = (f'<p class="sl"><span class="cb" aria-hidden="true"></span>Slow motion, one tenth speed</p>' if slow else '')
        whyp = f'<p class="why">{why["start"]}</p>'
    else:
        ctl = (f'<div class="cl" role="group" aria-label="{group}">'
               f'<button type="button" class="b" data-oa-play="" data-oa-pause="">{play_icons}<span data-word="">Play</span></button>'
               f'<button type="button" class="b" data-oa-reset="" aria-disabled="true" aria-describedby="{wid}">'
               f'{uicon("reset")}<span>Reset</span></button></div>')
        sl = ''
        if slow:
            sl += f'<label class="sl"><input type="checkbox" data-slow=""><span>Slow motion, one tenth speed</span></label>'
        if preview:
            sl += f'<label class="sl"><input type="checkbox" data-preview=""><span>Preview reduced motion</span></label>'
            sl += '<p class="dv" data-device="">Your device sets no motion preference, so Play runs each motion.</p>'
        whyp = f'<p class="why" id="{wid}" data-why="">{why["start"]}</p>'
    fl = ''.join(f'<li><p class="fh"><b>{t}</b>, {tm}{NB}ms</p>{svg}{extra}<p class="fw">{w}</p></li>'
                 for t, tm, svg, w, extra in frames)
    tl = ''.join('<li>' + re.sub(r'^([^:]+):', r'<b>\1:</b>', x, count=1) + '</li>' for x in timeline)
    sv = (f'<div class="sv"><p class="k">Still view</p><ol class="fr"{f" style=\"--fw:{fw}\"" if fw else ""}>{fl}</ol>'
          + (f'<ol class="tl">{tl}</ol>' if tl else '') + '</div>')
    data = ''
    if not static:
        m = dict(motion, words=words, why=why,
                 device={'reduce': 'Your device asks for reduced motion, so every player here shows its last frame at once.',
                         'full': 'Your device sets no motion preference, so Play runs each motion.'})
        data = f'<script type="application/json" data-motion="">{json.dumps(m, ensure_ascii=False)}</script>'
    attrs = '' if static else ' data-oa-motion="" data-frame="start"'
    parts = [head, row(1, stage), row(2, out), ctl]
    if static:
        parts += [row(5, sl), row(6, whyp)]
    else:
        parts += [sl, whyp]
    parts.append(row(7, sv))
    return f'<div class="pl"{attrs}>{"".join(parts)}{data}</div>'


def track(part, frames, dur, ease, at=(), fill=None):
    t = {'part': part, 'frames': frames, 'dur': DUR[dur], 'ease': EASE[ease], 'at': [DUR[a] for a in at]}
    if fill:
        t['fill'] = fill
    return t


LAND = [{'transform': f'scale({LAND_FROM:g})'}, {'transform': 'scale(1)'}]
LAND_SHOW = [{'transform': f'scale({LAND_FROM:g})', 'visibility': 'visible'}, {'transform': 'scale(1)', 'visibility': 'visible'}]
WHY_START = 'Reset works once you press Play.'
WHY = {'start': WHY_START,
       'slowDevice': 'Your device asks for reduced motion, so Play shows the last frame at once and Slow motion has nothing to slow.',
       'slowPreview': 'Preview reduced motion is on, so Play shows the last frame at once and Slow motion has nothing to slow.',
       'previewDevice': 'Your device asks for reduced motion, so the preview is already on.'}


def ms_words(n):
    return f'{n:,}{NB}ms'


# ------------------------------------------------------------------------------------------------ specimens
SPECS = {}


def _split_top(sel):
    parts, depth, cur = [], 0, ''
    for ch_ in sel:
        depth += {'(': 1, '[': 1, ')': -1, ']': -1}.get(ch_, 0)
        if ch_ == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch_
    return parts + [cur]


def prune_css(css, used):
    """Keep only the rules whose classes all appear in the fragment, so shared style sets cost a specimen only what
    it draws (the chapter's weight budget, 0.5 MB, has to leave room for Rule 17.6's identity specimens)."""
    out, i = [], 0
    while i < len(css):
        j = css.find('{', i)
        if j < 0:
            out.append(css[i:])
            break
        sel = css[i:j].strip()
        depth, k = 0, j
        while True:
            if css[k] == '{':
                depth += 1
            elif css[k] == '}':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        body = css[j + 1:k]
        if sel.startswith(('@media', '@container', '@supports')):
            inner = prune_css(body, used)
            if inner.strip():
                out.append(f'{sel}{{{inner}}}')
        elif sel.startswith('@'):
            out.append(f'{sel}{{{body}}}')
        else:
            keep = [p for p in _split_top(sel) if all(c in used for c in re.findall(r'\.([A-Za-z][\w-]*)', p))]
            if keep:
                out.append(','.join(keep) + '{' + body + '}')
        i = k + 1
    return ''.join(out)


def prune(html):
    bare = re.sub(r'<style\b[^>]*>.*?</style>|<script\b.*?</script>', '', html, flags=re.S)
    used = {c for v in re.findall(r'class="([^"]*)"', bare) for c in v.split()}
    return re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + prune_css(m.group(2), used) + m.group(3),
                  html, flags=re.S)


def spec(sid, html, rule, alt, **kw):
    ctx.spec(sid, prune(html), CH, rule, alt, **kw)
    SPECS[sid] = rule
    return sid


def player_specimen(css_extra, body):
    return f'<style>{PLAYER_CSS}{css_extra}</style>{body}<script>{PLAYER_JS}</script>'


# ---- 17.1 correct: a bill moves on (live)
TRACK_WORDS = {
    'start': 'Step 3 of 6: Committee vote. Steps 1 and 2 done, step 3 now, steps 4 to 6 not yet.',
    'end': 'Step 4 of 6: First chamber. Steps 1 to 3 done, step 4 now, steps 5 and 6 not yet.',
    'run': 'Playing.', 'pause': 'Paused.'}
T_SLIDE_AT = STD + STAG
T_END = T_SLIDE_AT + SLOW


def s17_1_correct():
    svg, dx = tracker_motion_svg()
    motion = {'tracks': [
        track('land', LAND, 'standard', 'enter'),
        track('slide', [{'transform': 'translateX(0px)'}, {'transform': f'translateX({dx}px)'}], 'slow', 'standard',
              ('standard', 'stagger')),
        track('grow', [{'transform': 'scaleX(0)'}, {'transform': 'scaleX(1)'}], 'slow', 'standard', ('standard', 'stagger')),
    ]}
    frames = [('First frame', 0, tracker_svg(START), TRACK_WORDS['start'], ''),
              ('Last frame', T_END, tracker_svg(END), TRACK_WORDS['end'], '')]
    timeline = [
        f'0{NB}ms: step 3 lands as done, over the standard {ms_words(STD)} with the enter easing.',
        f'{ms_words(T_SLIDE_AT)}: the ring slides from step 3 to step 4 and draws the line behind it, over the slow '
        f'{ms_words(SLOW)} with the standard easing.',
        f'{ms_words(T_END)}: at rest on step 4.']
    body = player('p1', kicker=ILLUS, title='Bill S.99002, School bus contracts', drawing=svg, words=TRACK_WORDS,
                  frames=frames, timeline=timeline, motion=motion, why=WHY, group='Play the bill’s move')
    alt = ('A live player for an Illustrative bill, S.99002, School bus contracts, drawn as a tracker of six numbered '
           'steps. At the first frame steps 1 and 2 done, step 3 now, steps 4 to 6 not yet, and the words say “Step 3 of '
           '6: Committee vote.” Play moves the bill on: step 3 lands as done, then the ring that marks the step the bill '
           f'is at now slides to step 4 and draws the line behind it, {T_END} ms in all. The last frame reads steps 1 to '
           '3 done, step 4 now, steps 5 and 6 not yet, “Step 4 of 6: First chamber.” One button plays and pauses, Reset '
           'returns to the first frame and is unavailable there with its reason, and Slow motion plays at one tenth '
           'speed. Under the player, the still view draws the first and last frames with their times and words.')
    return spec('s-17-1-correct', player_specimen('', body), '17.1', alt, interactive=True, illustrative=True,
                notes='Live motion player (data-oa-motion). Land, then slide with its draw, one stagger apart, timed '
                      'from the tokens at the press. Chapter 11’s marks and words for S.99002, which chapter 11 '
                      'shows at step 4.')


# ---- filmstrip: still frames of a failure, never animated (D2-xxx)
STRIP_CSS = ('.st{display:grid;gap:12px}:where(.st p){margin:0}'
             '.fs3{list-style:none;margin:0;padding:0;display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(min(100%,8.5rem),1fr))}'
             '.fs3 li{display:grid;gap:6px;align-content:start;padding:12px;border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
             '.fs3 svg{max-width:100%;height:auto}'
             '.tm{' + ty('caption') + ';font-weight:700}'
             '.big{' + ty('h4') + ';font-variant-numeric:tabular-nums}'
             '.nt{' + ty('caption') + '}'
             '.k{' + ty('label') + ';color:var(--oa-color-text-secondary)}'
             '.ti{' + ty('bodySmall') + ';font-weight:700}'
             '.code{margin:0;padding:10px 12px;background:var(--oa-color-field-ground);'
             'border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline);'
             'font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.875rem;line-height:1.5;overflow-wrap:anywhere}')


def s17_1_failure():
    css, band = fail_band()
    frames = [('0 ms', '0'), ('400 ms', '412'), ('1,200 ms', '1,284')]
    lis = ''.join(f'<li><p class="tm">{t.replace(" ", NB)}</p><p class="big">{n}</p><p class="nt">comments on the rule</p></li>'
                  for t, n in frames)
    html = (f'<style>{css}{STRIP_CSS}</style><div class="st">{band}<p>{ILLUS}</p>'
            f'<p class="k">Starts as the page opens</p><ol class="fs3">{lis}</ol>'
            '<p class="nt">The number was known before the page drew. The count makes the reader wait 1.2 seconds to read it.</p></div>')
    alt = ('Failure case: do not publish. Three still frames of a count that rises as the page opens, labeled '
           'Illustrative: 0 at 0 ms, 412 at 400 ms and 1,284 comments on the rule at 1,200 ms. A line under them says the '
           'number was known before the page drew and the count makes the reader wait 1.2 seconds to read it.')
    return spec('s-17-1-failure', html, '17.1', alt, illustrative=True,
                notes='Picture of a fault in still frames: a motion with no state change behind it. Failures are never '
                      'animated in the guide (D2-xxx).')


# ---- 17.2: the timing sheet
def curve_svg(x1, y1, x2, y2, ymax=1.0, ymin=0.0, size=112, dashed_top=False):
    pad = 8
    W = H = size
    s = W - 2 * pad
    span = ymax - ymin

    def X(v):
        return pad + v * s

    def Yv(v):
        return pad + (ymax - v) / span * (H - 2 * pad)
    path = (f'M{X(0):.2f} {Yv(0):.2f}C{X(x1):.2f} {Yv(y1):.2f} {X(x2):.2f} {Yv(y2):.2f} {X(1):.2f} {Yv(1):.2f}')
    frame = (f'<rect x="{pad - 0.5}" y="{Yv(1) - 0.5:.2f}" width="{s + 1}" height="{Yv(0) - Yv(1) + 1:.2f}" class="fr1"/>')
    top = ''
    if dashed_top:
        top = f'<path d="M{X(0):.2f} {Yv(1):.2f}H{X(1):.2f}" class="dsh"/>'
    return (f'<svg class="cv" width="{W}" height="{H}" viewBox="0 0 {W} {H}" aria-hidden="true" focusable="false">'
            f'{frame}{top}<path d="{path}" class="cvl"/></svg>')


SHEET_CSS = (':where(.ts p){margin:0}.ts{display:grid;gap:20px;max-width:44rem}'
             '.k{' + ty('label') + ';color:var(--oa-color-text-secondary)}'
             '.rows{list-style:none;margin:0;padding:0;display:grid;gap:14px}'
             '.nm{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;' + ty('bodySmall') + '}'
             '.nm b{font-weight:700;font-variant-numeric:tabular-nums}'
             '.nm code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.875rem;overflow-wrap:anywhere}'
             # CD-S5: a token name stays on one line wherever its row holds it, and breaks only where it cannot fit
             '.ts .tk{white-space:nowrap;font-size:0.8125rem}.rows > li{container:tr / inline-size}.ez > li{container:te / inline-size}'
             '@container tr (max-width:14.25rem){.ts .tk{white-space:normal}}@container te (max-width:13.25rem){.ts .tk{white-space:normal}}'
             '.jb{' + ty('caption') + ';color:var(--oa-color-text-secondary)}'
             '.trk{position:relative;height:10px;margin-top:6px;background:var(--oa-color-surface);'
             'border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
             '.bar{display:block;height:10px;width:calc(var(--v) / ' + str(HINGE) + ' * 100%);background:var(--oa-color-graphic-essential)}'
             '.rl{position:relative;height:2.5em;' + ty('caption') + ';font-variant-numeric:tabular-nums;'
             'border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
             '.rl span{position:absolute;top:0;left:calc(var(--v) / ' + str(HINGE) + ' * 100%);transform:translateX(-50%);'
             'padding-top:8px;white-space:nowrap;border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
             '.rl span:first-child{transform:none}'
             '.rl span{border-left:0}.rl span::before{content:"";position:absolute;top:0;left:50%;height:5px;'
             'border-left:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
             '.rl span:first-child::before{left:0}'
             '.ez{list-style:none;margin:0;padding:0;display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,13.5rem),1fr))}'
             '.ez li{display:grid;gap:6px;align-content:start}'
             '.cv{display:block;overflow:visible}.cv .fr1{fill:none;stroke:var(--oa-color-border-hairline);stroke-width:1}'
             '.cv .cvl{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:2}'
             '.cv .dsh{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:1;stroke-dasharray:4 3}'
             '.ax{' + ty('caption') + ';color:var(--oa-color-text-secondary)}'
             '.cd{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.875rem;overflow-wrap:anywhere}'
             '.nt{' + ty('caption') + '}')
DUR_ROWS = [
    ('fast', 'Fast', 'Hover and toggles.'),
    ('standard', 'Standard', 'Reveals, panels, a mark that lands and a line that draws on its own.'),
    ('slow', 'Slow', 'A move across a page or a component, such as the ring that slides to a bill’s next step.'),
    ('stagger', 'Stagger', 'The wait between marks that move one after another.'),
    ('hinge', 'Hinge', 'The hinge, played on request only.'),
    ('lever', 'Lever', 'The lever landing, played on request only.'),
]
EASE_ROWS = [
    ('standard', 'Standard', 'A mark that moves from one place to another.'),
    ('enter', 'Enter', 'A mark that arrives: a panel, a land, a line that draws.'),
    ('exit', 'Exit', 'A mark that leaves, at the fast duration.'),
]


def s17_2_correct():
    rows = ''.join(
        f'<li><p class="nm"><b>{lab}, {ms(n)}{NB}ms</b><code class="tk">{tokcss(DUR[n] if n in DUR else "--oa-motion-duration-" + n)}</code></p>'
        f'<p class="jb">{job}</p><div class="trk"><span class="bar" style="--v:{ms(n)}"></span></div></li>'
        for n, lab, job in DUR_ROWS)
    ticks = ''.join(f'<span style="--v:{t}">{t}{NB}ms</span>' for t in (0, 200, 400, 600))
    ez = ''.join(
        f'<li>{curve_svg(*bez(n))}<p class="nm"><b>{lab}</b></p><p class="cd">{bz(n)}</p>'
        f'<p class="cd tk">{tokcss(EASE[n])}</p><p class="jb">{job}</p></li>' for n, lab, job in EASE_ROWS)
    html = (f'<style>{SHEET_CSS}</style><div class="ts">'
            f'<div><p class="k">Six durations, drawn to one scale</p></div><ul class="rows">{rows}</ul>'
            f'<div class="rl" aria-hidden="true">{ticks}</div>'
            '<p class="nt">Under reduced motion each of the six durations is 0 ms (Rule 17.4).</p>'
            '<p class="k">Three easings, each drawn as its curve</p>'
            '<p class="ax">Time runs left to right and progress runs bottom to top, from where a mark starts to where it rests.</p>'
            f'<ul class="ez">{ez}</ul></div>')
    alt = (f'The nine motion tokens. Six durations as bars on one scale, the hinge’s {HINGE} ms the longest: fast '
           f'{FAST} ms for hover and toggles; standard {STD} ms for reveals, panels, a mark that lands and a line that '
           f'draws on its own; slow {SLOW} ms for a move across a page or a component; stagger {STAG} ms between '
           f'marks that move one after another; hinge {HINGE} ms and lever {LEVER} ms, each played on request only. A line says each is 0 ms under '
           f'reduced motion. Then three easing curves, time across and progress up: standard {bz("standard")}, which '
           f'starts quickly and slows into place; enter {bz("enter")}, which slows all the way into place; exit '
           f'{bz("exit")}, which starts slowly and leaves at speed. Each curve ends at its place without passing it.')
    return spec('s-17-2-correct', html, '17.2', alt, readable=True,
                notes='Values read from tokens.json; bars drawn as calc(value / 680 * 100%) so the scale holds at '
                      'every width.')


def s17_2_failure():
    css, band = fail_band()
    curve = curve_svg(*BOUNCE, ymax=1.2, ymin=-0.05, dashed_top=True)
    html = (f'<style>{css}{SHEET_CSS}</style><div class="ts">{band}'
            f'<div class="ez" style="display:flex;flex-wrap:wrap;gap:16px;align-items:flex-start">{curve}'
            '<div style="flex:1 1 12rem;min-width:0;display:grid;gap:8px">'
            '<p class="cd">transition: transform 250ms cubic-bezier(0.34, 1.56, 0.64, 1)</p>'
            f'<p class="nt">Two numbers of its own: 250 ms is no token, and the curve goes {OVER} percent past the '
            'dashed line, where the mark should rest, before it comes back.</p></div></div></div>')
    alt = (f'Failure case: do not publish. A line of CSS, transition: transform 250ms cubic-bezier(0.34, 1.56, 0.64, '
           f'1), beside the curve it draws, which rises {OVER} percent past the dashed line where '
           'the mark should rest before it falls back. A note says 250 ms is no token and the curve overshoots its place.')
    return spec('s-17-2-failure', html, '17.2', alt, notes='Picture of a fault: literal timing and an overshooting easing.')


# ---- 17.3 correct: the player's parts (a picture), 17.4 correct: the same player live
MECH_WORDS = {
    'start': 'First frame: wealth concentration, where Loop R1 starts.',
    'end': 'Last frame: wealth concentration raises money in politics.',
    'run': 'Playing.', 'pause': 'Paused.'}
M_LAND_AT = STD + STAG
M_END = M_LAND_AT + STD
MECH_TIMELINE = [
    f'0{NB}ms: the link draws from wealth concentration toward money in politics, over the standard {ms_words(STD)} with the enter easing.',
    f'{ms_words(M_LAND_AT)}: the arrowhead and the second node land, over the standard {ms_words(STD)} with the enter easing.',
    f'{ms_words(M_END)}: at rest. Under reduced motion the last frame shows at 0{NB}ms.']
MECH_KICK = 'From our systems atlas, Loop R1'
# BE-M3 and the fix brief's call 4 (D2-1547): V7's title stays as the loop's name, in quotation marks, and the line under
# it gives the loop's grade. The same words sit in chapter 18's two loop sets.
MECH_TITLE = '“Wealth and political influence reinforce each other”'
MECH_GRADE = ('Our atlas grades this loop plausible: its middle step is the least certain, and it runs only on issues '
              'where large donors and middle-income voters want different things.')


def mech_player(static):
    motion = {'tracks': [
        track('draw', [{'strokeDashoffset': 1}, {'strokeDashoffset': 0}], 'standard', 'enter'),
        track('tip', LAND_SHOW, 'standard', 'enter', ('standard', 'stagger'), fill='forwards'),
        track('land', LAND_SHOW, 'standard', 'enter', ('standard', 'stagger'), fill='forwards'),
    ]}
    frames = [('First frame', 0, mech_stage(mech_svg('start')), MECH_WORDS['start'], ''),
              ('Last frame', M_END, mech_stage(mech_svg('end')), MECH_WORDS['end'], '')]
    return player('p4', kicker=MECH_KICK, title=MECH_TITLE, sub=MECH_GRADE,
                  drawing=mech_stage(mech_motion_svg() if not static else mech_svg('start')),
                  words=MECH_WORDS, frames=frames, timeline=MECH_TIMELINE, motion=motion, why=WHY,
                  slow=True, preview=not static, group='Play the link', static=static)


# CD-S1: the key runs top to bottom, in the order the parts stand in the player.
ANATOMY = [
    'The stage. A player of a state or a mechanism, like this one, rests on its first frame until a reader presses '
    'Play. A player of the wordmark or the lockmark rests on its master.',
    'The status line, which says in words what the frame shows. A screen reader hears it when it changes.',
    'Play, one button that turns to Pause while the motion runs and to Play again at its end. Its icon and its word change together.',
    'Reset, which returns the player to where it rests. At rest it is unavailable and keeps focus.',
    'Slow motion, which plays at one tenth speed, so Pause has time to work.',
    'The reason line, which says why a control is unavailable and what makes it available.',
    'The still view: the first and last frames at true size, each with its time and its words, then each step of the motion in order.',
]


def s17_3_correct():
    css = ('.anat{display:grid;grid-template-columns:minmax(0,1fr);gap:20px}.key{margin:0;padding:0;list-style:none;display:grid;gap:8px}'
           '.key li{display:flex;gap:10px;align-items:flex-start;' + ty('bodySmall') + '}'
           '.cb{display:inline-block;flex:none;width:20px;height:20px;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);'
           'background:var(--oa-color-field-ground)}')
    key = ''.join(f'<li><span class="nb" aria-hidden="true">{i + 1}</span><span>{t}</span></li>' for i, t in enumerate(ANATOMY))
    html = (f'<style>{PLAYER_CSS}{css}</style><div class="anat">{mech_player(True)}'
            f'<ol class="key">{key}</ol></div>')
    alt = ('The parts of a motion player, numbered 1 to 7 from top to bottom, drawn from the player for Loop R1’s first '
           f'link in Rule 17.4, under its heading, the loop’s name, {MECH_TITLE}, and the line “{MECH_GRADE}” '
           '1, the stage at its first frame, where a player of a state or a mechanism rests: two nodes, wealth '
           'concentration filled and money in politics empty. A player of the wordmark or the lockmark rests on its '
           'master. 2, the status line, which says what the frame shows. 3, the Play button, which turns to Pause while '
           'the motion runs and to Play again at its end. 4, Reset, unavailable at rest with a dashed edge, its number '
           'set off its top left corner. 5, Slow motion, a check box that plays at one tenth speed. 6, the reason line: '
           '“Reset works once you press Play.” 7, the still view: the first and last frames with their times and words, '
           'and the steps of the motion in order. A numbered key under the player says the same.')
    return spec('s-17-3-correct', html, '17.3', alt, notes='A picture of the player, with no controls and no script: the '
                'live player is s-17-4-correct.')


def s17_3_failure():
    css, band = fail_band()
    extra = ('.fp{display:grid;gap:10px;max-width:22rem}.ib{display:inline-grid;place-items:center;width:44px;height:44px;'
             'border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong)}'
             '.lp{display:flex;gap:8px;align-items:center;' + ty('caption') + '}'
             '.fs3{grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}'
             '.fs3 li{padding:10px 0 0;border:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}')
    lis = ''.join(f'<li><p class="tm">{t}</p>{tracker_svg(s)}</li>'
                  for t, s in ((f'0{NB}ms, as the page opens', START), (f'{T_END:,}{NB}ms', END),
                               (f'{T_END + 2440:,}{NB}ms, starting again', START)))
    html = (f'<style>{css}{STRIP_CSS}{PLAYER_CSS}{extra}</style><div class="st">{band}<p>{ILLUS}</p>'
            f'<div class="fp"><span class="ib">{uicon("play")}</span>'
            '<p class="nt">One button with a play icon and no word. Pause, Reset and the still view are all missing.</p></div>'
            f'<ol class="fs3">{lis}</ol>'
            '<p class="nt">The motion starts as the page opens and starts again every three seconds, so the bill seems to '
            'move back and forth between two steps.</p></div>')
    alt = ('Failure case: do not publish. An Illustrative bill’s tracker drawn in three still frames: at 0 ms as the '
           f'page opens steps 1 and 2 done, step 3 now, steps 4 to 6 not yet; at {T_END:,} ms steps 1 to 3 done, step 4 '
           f'now, steps 5 and 6 not yet; at {T_END + 2440:,} ms, starting again, steps 1 and 2 done, step 3 now, steps 4 to '
           '6 not yet. Above them, one square button with a play icon and no word, and a note that Pause, Reset and the still view are all '
           'missing. A line says the motion starts as the page opens and every three seconds after.')
    return spec('s-17-3-failure', html, '17.3', alt, illustrative=True,
                notes='Picture of a fault in still frames. The tracker’s marks keep chapter 11’s words in '
                      'the alt, so the drawing says its steps.')


def s17_4_correct():
    body = mech_player(False)
    alt = ('A live player for the first link of Loop R1 from our systems atlas, “Wealth and political influence reinforce '
           f'each other”, with the line “{MECH_GRADE}” '
           'At the first frame the node for wealth concentration is filled and the node for money in '
           f'politics is empty. Play draws the link from the first node to the second over {STD} ms, then the arrowhead '
           f'and the second node land, {M_END} ms in all, and the status line says “Last frame: wealth concentration '
           'raises money in politics.” A check box, Preview reduced motion, sets this player’s motion tokens to 0 '
           'ms, so Play draws the last frame at once, as it does for every player when a device asks for reduced motion. '
           'A line says what this device asks for, and when it asks for reduced motion the preview is checked and '
           'unavailable with its reason. Slow motion plays at one tenth speed. The still view draws the first and last '
           'frames with their words and lists the steps of the motion.')
    return spec('s-17-4-correct', player_specimen('', body), '17.4', alt, interactive=True,
                notes='Live motion player with a reduced-motion preview: data-preview="reduced" sets the six duration '
                      'tokens to 0ms on the player, so the script reads 0 exactly as it does under the media query.')


def s17_4_failure():
    css, band = fail_band()
    pc = round(EASE_OUT_HALF * 100)
    lis = ''.join(f'<li><p class="tm">{t}</p>{mech_svg(s, fr)}<p class="nt">{w}</p></li>' for t, s, fr, w in (
        ('0 ms', 'start', None, 'Not started'), ('200 ms', 'start', EASE_OUT_HALF, f'{pc} percent drawn'),
        ('400 ms', 'end', None, 'Reaches the second node')))
    lis = lis.replace(' ms<', NB + 'ms<')
    css2 = ('.fs3{grid-template-columns:repeat(auto-fit,minmax(min(100%,20rem),1fr))}'
            '.fs3 li{padding:10px 0 0;border:0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}') + ('.dg .nd-on{fill:var(--oa-color-graphic-essential)}'
                                                    '.dg .nd-off{fill:var(--oa-color-surface);stroke:var(--oa-color-graphic-subtle);stroke-width:1.5}'
                                                    '.dg .ln{fill:none;stroke:var(--oa-color-graphic-essential);stroke-width:2;stroke-linejoin:round}'
                                                    '.dg{display:block;overflow:visible}') + MECH_CSS
    html = (f'<style>{css}{STRIP_CSS}{css2}</style><div class="st">{band}'
            '<p class="code">link.animate(frames, { duration: 400, easing: "ease-out" })</p>'
            '<p class="k">With reduced motion on</p>'
            f'<ol class="fs3">{lis}</ol>'
            '<p class="nt">The script carries its own 400 ms and never reads the tokens, so a reader who asked for '
            'reduced motion still watches the link draw for 400 ms.</p></div>')
    alt = ('Failure case: do not publish. A line of script, link.animate(frames, { duration: 400, easing: “ease-out” }), '
           'over three still frames of Loop R1’s first link with reduced motion on: at 0 ms the link has not started, at '
           f'200 ms it is {round(EASE_OUT_HALF * 100)} percent drawn, and only at 400 ms does it reach the second node. '
           'A note says the script carries its own 400 '
           'ms and never reads the tokens.')
    return spec('s-17-4-failure', html, '17.4', alt, notes='Picture of a fault: a script timing that the reduced '
                'motion setting cannot reach.')


# ---- 17.5: the three behaviors, live
MINI = [
    ('slide', 'Slide', 'The ring marks the current place and slides to the next one.',
     {'start': 'First frame: the ring at the first place.', 'end': 'Last frame: the ring at the second place.'},
     [track('slide', [{'transform': 'translateX(0px)'}, {'transform': 'translateX(122px)'}], 'slow', 'standard')],
     SLOW, f'0{NB}ms to {ms_words(SLOW)}: a straight move over the slow {ms_words(SLOW)}, with the standard easing.'),
    ('draw', 'Draw', 'A line draws along its own path, from its first node to its second.',
     {'start': 'First frame: two nodes, not yet joined.', 'end': 'Last frame: a line joins the first node to the second.'},
     [track('draw', [{'strokeDashoffset': 1}, {'strokeDashoffset': 0}], 'standard', 'enter')],
     STD, f'0{NB}ms to {ms_words(STD)}: the line extends from its start over the standard {ms_words(STD)}, with the enter easing.'),
    ('land', 'Land', f'A mark arrives at {round(LAND_FROM * 100)} percent of its size and settles to its true size.',
     {'start': 'First frame: an empty node.', 'end': 'Last frame: the node is filled.'},
     [track('land', LAND, 'standard', 'enter')],
     STD, f'0{NB}ms to {ms_words(STD)}: from {round(LAND_FROM * 100)} percent to true size over the standard {ms_words(STD)}, with the enter easing.'),
]


def s17_5_correct():
    blocks = []
    for i, (kind, name, desc, words, tracks, total, line) in enumerate(MINI):
        w = dict(words, run='Playing.', pause='Paused.')
        frames = [('First frame', 0, mini_svg(kind, 'start'), w['start'], ''),
                  ('Last frame', total, mini_svg(kind, 'end'), w['end'], '')]
        blocks.append(player(f'p5{kind[0]}', kicker=name, title=None,
                             drawing=f'<p class="ds">{desc}</p>' + mini_svg(kind, None, live=True), words=w,
                             frames=frames, timeline=[line], motion={'tracks': tracks}, why=WHY,
                             group=f'Play the {kind}', fw='9.375rem'))
    css = ('.three{display:grid;grid-template-columns:minmax(0,1fr);gap:32px;container-type:inline-size}.three > .pl + .pl{padding-top:24px;'
           'border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}.ds{margin:0 0 12px;' + ty('bodySmall') + '}'
           '.three .stg{padding-top:0}'
           '@container (min-width:38rem){.three .pl{grid-template-columns:minmax(0,1fr) minmax(0,1fr);column-gap:32px;'
           'max-width:none;align-content:start}.three .pl > *{grid-column:1}.three .pl > .sv{grid-column:2;grid-row:1 / span 6;'
           'align-self:start;border-top:0;padding-top:0}}')
    body = f'<div class="three">{"".join(blocks)}</div>'
    alt = (f'Three live players, one for each behavior. Slide: a ring around the first of two small nodes moves along a '
           f'hairline to the second over {SLOW} ms with the standard easing. Draw: a line with one bend extends from a '
           f'filled node to an empty one over {STD} ms with the enter easing. Land: a filled disc arrives over an empty '
           f'node at {round(LAND_FROM * 100)} percent of its size and settles to its true size over {STD} ms with the '
           'enter easing. Each has a Play button that pauses, Reset, Slow motion at one tenth speed, a status line, and '
           'a still view with its first and last frames and its timing in words.')
    return spec('s-17-5-correct', player_specimen(css, body), '17.5', alt, interactive=True,
                notes='Three motion players (data-oa-motion each), plain nodes untagged.')


def s17_5_failure():
    css, band = fail_band()
    # a disc that lands with a bounce: four still frames of its size
    sizes = [('0 ms', 1.0), ('120 ms', 0.82), ('200 ms', 1.08), ('320 ms', 0.97), ('440 ms', 1.0)]

    def disc(sc):
        rr = 12 * sc
        return (f'<svg class="dg" width="64" height="48" viewBox="0 0 64 48" aria-hidden="true" focusable="false">'
                f'<circle cx="32" cy="24" r="11.25" class="nd-off"/><circle cx="32" cy="24" r="{rr:.2f}" class="nd-on"/></svg>')
    lis = ''.join(f'<li><p class="tm">{t.replace(" ", NB)}</p>{disc(s)}<p class="nt">{round(s * 100)} percent</p></li>'
                  for t, s in sizes)
    css2 = ('.dg{display:block}.dg .nd-on{fill:var(--oa-color-graphic-essential)}'
            '.dg .nd-off{fill:var(--oa-color-surface);stroke:var(--oa-color-graphic-subtle);stroke-width:1.5}'
            '.fs3{grid-template-columns:repeat(auto-fit,minmax(min(100%,5.5rem),1fr))}')
    html = (f'<style>{css}{STRIP_CSS}{css2}</style><div class="st">{band}<p class="k">A land with a bounce</p>'
            f'<ol class="fs3">{lis}</ol><p class="nt">The disc shrinks inside its node, swells past it and shrinks again '
            'before it rests, so it sits at four sizes in under half a second.</p></div>')
    alt = ('Failure case: do not publish. Five still frames of a disc landing on a node with a bounce: true size at 0 ms, '
           '82 percent at 120 ms, 108 percent at 200 ms, 97 percent at 320 ms and true size at 440 ms. A note says the '
           'disc sits at four sizes in under half a second.')
    return spec('s-17-5-failure', html, '17.5', alt, notes='Picture of a fault in still frames: bounce easing, which our '
                'fifth edition already left out.')


# ---- 17.6: the identity designer's slots, or this generator's pending markers
PEND_CSS = ('.pd{display:grid;gap:8px;padding:20px;border:var(--oa-border-width-hairline) dashed var(--oa-color-state-empty-edge);'
            'color:var(--oa-color-state-empty-text);' + ty('bodySmall') + '}:where(.pd p){margin:0}'
            '.pd b{font-weight:700;color:var(--oa-color-text-primary)}')


def s17_6_pending():
    html = (f'<style>{PEND_CSS}</style><div class="pd" data-oa-pending="identity"><p><b>Coming later.</b> The hinge and '
            f'the lever, live, each with Play, Pause, Reset and a still view.</p><p>The hinge plays over {HINGE} ms and '
            f'the lever over {LEVER} ms, and each ends on its approved master. Until they are drawn, Rules 04.5 and 08.1 '
            'show both masters at rest.</p></div>')
    alt = (f'A placeholder with a dashed edge that says the hinge and the lever, live, are coming later: the hinge over '
           f'{HINGE} ms and the lever over {LEVER} ms, each ending on its approved master, with Rules 04.5 and 08.1 '
           'showing both masters at rest meanwhile.')
    return spec('s-17-6-pending', html, '17.6', alt, notes='Pending marker for the identity designer’s '
                's-17-hinge-correct and s-17-lever-correct (manifest-identity.json). Leaves the manifest on the first '
                'run after they land.')


def s17_6_pending_failure():
    html = (f'<style>{PEND_CSS}</style><div class="pd" data-oa-pending="identity"><p><b>Coming later.</b> A failure case '
            'drawn with the hinge and the lever: a motion whose last frame misses its master by a pixel, set beside the '
            'master at the same size.</p></div>')
    alt = ('A placeholder with a dashed edge that says a failure case is coming later: a hinge or lever motion whose last '
           'frame misses its master by a pixel, beside the master at the same size.')
    return spec('s-17-6-pending-failure', html, '17.6', alt, notes='Pending marker for the identity designer’s '
                's-17-hinge-failure or s-17-lever-failure.')


# ---- theme cells: one sample on Newsprint and on Charcoal (D2-1159: role names only)
CELL_CSS = (
    '.wr{container-type:inline-size}:where(.wr p){margin:0}'
    '.k{' + ty('label') + ';color:var(--oa-color-text-secondary)}'
    '.pr{display:grid;gap:12px;grid-template-columns:minmax(0,1fr)}'
    '@container (min-width:34rem){.pr{grid-template-columns:repeat(2,minmax(0,1fr))}}'
    '.cell{display:grid;gap:10px;align-content:start;padding:12px 16px 16px;'
    'border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}'
    '.sf{' + ty('label') + ';color:var(--oa-color-text-secondary)}'
    '.row{display:flex;flex-wrap:wrap;gap:12px;align-items:center}'
    '.btn{display:inline-flex;align-items:center;gap:8px;min-height:var(--oa-size-target-touch);padding:0 16px;'
    'border:var(--oa-border-width-hairline) solid transparent;' + ty('ui') + '}'
    '.btn svg{flex:none;display:block}'
    '.pri{background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label)}'
    '.pri.hv{background:var(--oa-color-action-primary-fill-hover);text-decoration:underline;text-underline-offset:0.2em}'
    '.qt{background:var(--oa-color-surface);color:var(--oa-color-text-primary);border-color:var(--oa-color-border-strong)}'
    '.qt.hv{border-width:var(--oa-border-width-rule);padding:0 15px}'
    '.fo{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring);outline-offset:var(--oa-border-focus-offset)}'
    '.lk{color:var(--oa-color-text-primary);text-decoration:underline;text-decoration-thickness:var(--oa-border-width-underline);'
    'text-underline-offset:0.2em;' + ty('bodySmall') + '}'
    '.lk.hv{text-decoration-thickness:var(--oa-border-width-underline-hover)}'
    '.dis{color:var(--oa-component-button-disabled-label);border:var(--oa-border-width-hairline) dashed var(--oa-component-button-disabled-edge)}'
    '.why{' + ty('caption') + ';color:var(--oa-color-text-secondary)}'
    '.chip{display:inline-flex;align-items:center;gap:6px;min-height:var(--oa-size-target-touch);padding:0 14px;'
    'border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);color:var(--oa-color-text-primary);' + ty('ui') + '}'
    '.chip.on{border-width:var(--oa-border-width-rule);font-weight:700;padding:0 13px 0 7px}'
    '.chip svg{flex:none;display:block}'
    '.seg{display:inline-flex;flex-wrap:wrap}.seg .chip + .chip{margin-left:-1px}'
    '.msg{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px;align-items:start;padding:10px 12px;' + ty('bodySmall') + '}'
    '.msg svg{display:block;margin-top:-1px}.msg b{font-weight:700}'
    '.wn{border-left:var(--oa-border-width-bar) solid var(--oa-color-state-warning-mark);color:var(--oa-color-state-warning-text)}'
    '.wn svg{color:var(--oa-color-state-warning-mark)}'
    '.er{border-left:var(--oa-border-width-bar) solid var(--oa-color-state-error-bar);'
    'background-color:var(--oa-color-state-error-band);color:var(--oa-color-state-error-text)}'
    '.ok{padding-left:16px;color:var(--oa-color-state-success-text)}.ok svg{color:var(--oa-color-state-success-mark)}'
    '.em{display:grid;gap:4px;padding:14px 16px;border:var(--oa-border-width-hairline) dashed var(--oa-color-state-empty-edge);'
    'color:var(--oa-color-state-empty-text);' + ty('bodySmall') + '}'
    '.ld{display:grid;gap:8px;color:var(--oa-color-state-loading-text);' + ty('bodySmall') + '}'
    '.ld svg{display:block;max-width:100%}.ld .lm{stroke:var(--oa-color-state-loading-mark);stroke-width:1.5}'
    '.mu{display:grid;gap:8px;' + ty('bodySmall') + '}'
    '.mu p{display:flex;gap:10px;align-items:center}.mu .on{color:var(--oa-color-text-primary);font-weight:600}'
    '.mu .off{color:var(--oa-color-state-muted-text);font-weight:400}'
    '.mu svg{flex:none;display:block}.mu .dk{fill:var(--oa-color-graphic-essential)}'
    '.mu .ol{fill:none;stroke:var(--oa-color-state-muted-mark);stroke-width:1.5}'
    '.cur{display:block;padding:8px 12px;background:var(--oa-color-state-selected-band);'
    'border-left:var(--oa-border-width-bar) solid var(--oa-color-state-selected-bar);color:var(--oa-color-text-primary);' + ty('bodySmall') + ';font-weight:var(--oa-font-weight-bold)}'
    '.nav{list-style:none;margin:0;padding:0;display:grid;gap:2px}'
    '.nav span:not(.cur){display:block;padding:8px 12px 8px 16px;color:var(--oa-color-text-primary);' + ty('bodySmall') + '}'
    '.uc{color:var(--oa-color-text-primary);text-decoration:underline;text-decoration-thickness:var(--oa-border-width-rule);'
    'text-underline-offset:0.25em;' + ty('bodySmall') + ';font-weight:var(--oa-font-weight-bold)}'
    '.fld{display:flex;align-items:center;gap:8px;min-height:var(--oa-size-target-touch);padding:0 12px;'
    'background:var(--oa-color-field-ground);border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);'
    'color:var(--oa-color-text-primary);' + ty('ui') + ';font-weight:400}'
    '.fld svg{flex:none;display:block;color:var(--oa-color-text-secondary)}'
    '.lb{' + ty('ui') + '}'
    '.st-l{display:grid;gap:4px}'
)


def cells(sample, label_n='On Newsprint', label_c='On Charcoal'):
    """The same sample twice, in the light and the dark theme. A sample may be a function of the theme ('n' or 'c')."""
    def one(theme, lab):
        s = sample(theme) if callable(sample) else sample
        return f'<div class="cell" data-oa-theme="{"light" if theme == "n" else "dark"}"><p class="sf">{lab}</p>{s}</div>'
    return f'<div class="pr">{one("n", label_n)}{one("c", label_c)}</div>'


def check():
    return uicon('selected-check')


def tracker_line_svg():
    """Loading: the tracker's line alone, still, where the six steps will sit (D2-200: links alone)."""
    return (f'<svg width="{TW}" height="16" viewBox="0 0 {TW} 16" aria-hidden="true" focusable="false">'
            f'<line x1="{TXS[0]}" y1="8" x2="{TXS[-1]}" y2="8" class="lm"/></svg>')


def state_samples():
    """The ten states of Rule 17.8: (name, cue in words, sample markup)."""
    muted = ('<div class="mu"><p class="on"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
             '<circle cx="8" cy="8" r="6" class="dk"/></svg>Budget hearing, in this view</p>'
             '<p class="off"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
             '<circle cx="8" cy="8" r="5.25" class="ol"/></svg>Zoning hearing, outside this view</p></div>')
    disabled = (f'<div class="st-l"><span class="btn dis">{uicon("download")}Download the files</span>'
                '<p class="why">Choose a size to download.</p></div>')
    hover = '<div class="row"><span class="btn pri hv">Download the files</span></div>'
    focus = '<div class="row" style="padding:4px"><span class="btn pri fo">Download the files</span></div>'
    loading = (f'<div class="ld">{tracker_line_svg()}<p>Loading the tracker for S.99002.</p></div>')
    selected = (f'<div class="row"><span class="chip on">{check()}Housing</span><span class="chip">Schools</span></div>')
    warning = (f'<div class="msg wn">{uicon("warning")}<span><b>Warning:</b> Checked October 15, 2026. The agency may '
               'have acted since.</span></div>')
    error = (f'<div class="msg er" {RED_ERR}>{uicon("error")}<span><b>Error:</b> Enter a ZIP code with five digits.</span></div>')
    empty = (f'<div class="em"><p>0 of {N_LIB} symbols. No symbol matches.</p><p>Clear the search or the filters to see more.</p></div>')
    success = (f'<div class="msg ok">{uicon("success")}<span><b>You’re signed up.</b> We’ll email you on '
               'March 1.</span></div>')
    return [
        ('Muted', 'Secondary words in regular weight, and marks drawn as outlines.', muted),
        ('Disabled', 'A dashed edge, readable words and a line that says what makes it available. It keeps focus.', disabled),
        ('Hover', 'The label underlines, and a filled button steps one shade.', hover),
        ('Focus', 'A 2 px ring with a 2 px gap, shown at once.', focus),
        ('Loading', 'Words that name what is loading, and a still drawing of the line where it will sit.', loading),
        ('Selected', 'A check before the word, the word in bold and a 2 px edge.', selected),
        ('Warning', 'The warning mark, the word “Warning:” and a 4 px bar, all in the text’s ink.', warning),
        ('Error', 'The error mark, the word “Error:”, the fix and a 4 px Pillar Red bar, on the Error Band on Newsprint '
                  'and on the ground itself on Charcoal.', error),
        ('Empty', 'A dashed region that says what is missing and what to do next.', empty),
        ('Success', 'The success mark in Verdigris and words that say what happened.', success),
    ]


def s17_8_correct():
    lis = ''.join(f'<li><p class="nm">{n}</p><p class="cu">{cue}</p>{cells(s)}</li>' for n, cue, s in state_samples())
    css = (CELL_CSS + '.tn{list-style:none;margin:0;padding:0;display:grid;gap:24px}'
           '.tn > li{display:grid;gap:8px}.nm{' + ty('label') + '}.cu{' + ty('bodySmall') + ';max-width:40rem}')
    html = f'<style>{css}</style><div class="wr"><p style="margin:0 0 16px">{ILLUS}</p><ol class="tn">{lis}</ol></div>'
    alt = ('The ten states, each drawn on Newsprint and on Charcoal from the same short names, with its cue in words. '
           'Muted: Zoning hearing, outside this view, in secondary words in regular weight with an outline dot, under Budget hearing in '
           'bold with a filled dot. Disabled: a download button with a dashed edge and readable words, and the line '
           '“Choose a size to download.” Hover: a primary button one shade lighter, its label underlined. Focus: the '
           'primary button with a 2 px ring 2 px outside it, Verdigris on Newsprint and Newsprint on Charcoal. Loading: '
           'a still line where a tracker will sit and “Loading the tracker for S.99002.” Selected: a Housing chip with a '
           'check, bold words and a 2 px edge beside a Schools chip with a 1 px edge. Warning: the warning mark, '
           '“Warning:” and a 4 px bar in the text’s ink. Error: the error mark, “Error: Enter a ZIP code with five '
           'digits.” and a 4 px Pillar Red bar, on the Error Band on Newsprint and on the ground on Charcoal. Empty: a '
           f'dashed region that says “0 of {N_LIB} symbols. No symbol matches. Clear the search or the filters to see more.” '
           'Success: the Verdigris success mark and “You’re signed up. We’ll email you on March 1.”')
    return spec('s-17-8-correct', html, '17.8', alt, illustrative=True, readable=True,
                notes='The canonical ten-states plate (round 1 brief, Rule 17.8): data-oa-theme light and dark cells, role '
                      'names only. Error Band is initial on Charcoal (D2-1160, confirmed here).')


def s17_8_failure():
    css, band = fail_band()
    extra = ('.fl{list-style:none;margin:0;padding:0;display:grid;gap:14px}.fl li{display:grid;gap:6px}'
             '.nm{' + ty('label') + ';color:var(--oa-color-text-secondary)}'
             '.chipx{display:inline-flex;align-items:center;min-height:var(--oa-size-target-touch);padding:0 14px;'
             'border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);' + ty('ui') + '}'
             '.chipx.f{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);'
             'border-color:var(--oa-color-surface-prussian)}'
             '.red{color:var(--oa-color-palette-pillar-red);' + ty('bodySmall') + '}'
             '.grn{color:var(--oa-color-palette-verdigris);' + ty('bodySmall') + '}'
             '.fade{opacity:0.4}')
    html = (f'<style>{css}{CELL_CSS}{extra}</style><div class="st" style="display:grid;gap:14px">{band}<ol class="fl">'
            '<li><p class="nm">Selected, by fill alone</p><div class="row"><span class="chipx f">Housing</span>'
            '<span class="chipx">Schools</span></div></li>'
            f'<li><p class="nm">Error, in red words alone</p><p class="red" {RED_ERR}>Enter a ZIP code with five digits.</p></li>'
            '<li><p class="nm">Success, in Verdigris words alone</p><p class="grn">Signed up.</p></li>'
            f'<li><p class="nm">Disabled, faded to 40 percent</p><div class="row"><span class="btn qt fade">{uicon("download")}'
            'Download the files</span></div></li></ol></div>')
    alt = (f'Failure case: do not publish. Four states drawn by color alone on Newsprint: a selected Housing chip that '
           f'differs from Schools only by its Prussian fill; an error in Pillar Red words, {F["red_text_n"]} to 1, with no '
           f'mark or “Error:”; a success in Verdigris words, {F["verd_text_n"]} to 1, with no mark; and a download button '
           f'faded to 40 percent, {F["faded_n"]} to 1, with no reason.')
    return spec('s-17-8-failure', html, '17.8', alt, exempt=['contrast'],
                notes='Picture of a fault. Red words at 2.96 and Verdigris at 3.37 fail text contrast on purpose; the '
                      'red is the error’s one job.')


# ---- 17.7 loading
def s17_7_correct():
    def sample(theme):
        return (f'<div class="ld"><p class="lb">Bill S.99002, School bus contracts</p>{tracker_line_svg()}'
                '<p>Loading the tracker for S.99002.</p></div>')
    css = CELL_CSS + '.ld .lb{color:var(--oa-color-text-primary)}'
    html = f'<style>{css}</style><div class="wr"><p style="margin:0 0 12px">{ILLUS}</p>{cells(sample)}</div>'
    alt = (f'An Illustrative bill’s tracker while it loads, on Newsprint and on Charcoal: the title “Bill S.99002, '
           f'School bus contracts”, a still line where the six steps will sit, with no steps on it, and the words '
           f'“Loading the tracker for S.99002.” The line measures {F["load_n"]} to 1 on Newsprint and {F["load_c"]} on '
           'Charcoal. Nothing moves.')
    return spec('s-17-7-correct', html, '17.7', alt, illustrative=True,
                notes='D2-200: the links alone, never a node, so no mark reads as a step under way.')


def s17_7_failure():
    css, band = fail_band()
    ops = [('0 ms', 0.2), ('600 ms', 0.5), ('1,200 ms', 0.2)]

    def disc(o):
        return (f'<svg width="48" height="48" viewBox="0 0 48 48" aria-hidden="true" focusable="false">'
                f'<circle cx="24" cy="24" r="12" fill-opacity="{o}" class="pu"/></svg>')
    lis = ''.join(f'<li><p class="tm">{t.replace(" ", NB)}</p>{disc(o)}<p class="nt">{round(o * 100)} percent</p></li>'
                  for t, o in ops)
    extra = '.pu{fill:var(--oa-color-graphic-essential)}'
    html = (f'<style>{css}{STRIP_CSS}{extra}</style><div class="st">{band}<p class="k">A pulse, with no words</p>'
            f'<ol class="fs3">{lis}</ol><p class="nt">The disc fades between 20 and 50 percent strength every 1.2 seconds for as '
            'long as the wait lasts, and nothing says what is loading.</p></div>')
    alt = ('Failure case: do not publish. Three still frames of a loading pulse: a disc at 20 percent strength at 0 ms, '
           '50 percent at 600 ms and 20 percent again at 1,200 ms. A note says it fades every 1.2 seconds for as long as '
           'the wait lasts and nothing says what is loading.')
    return spec('s-17-7-failure', html, '17.7', alt, notes='Picture of a fault in still frames: our fifth edition’s '
                'loading pulse (pulse 1.2s ease-in-out infinite, 20 to 50 percent), drawn in ink for the picture.')


# ---- 17.9 hover and focus
def s17_9_correct():
    def sample(theme):
        rows = []
        for lab, cls in (('At rest', ''), ('Hover', ' hv'), ('Focus', ' fo')):
            rows.append(f'<div class="hfr"><p class="sf">{lab}</p><div class="row">'
                        f'<span class="btn pri{cls}">Save</span><span class="btn qt{cls}">Save</span>'
                        f'<span class="lk{cls}">Sources</span></div></div>')
        return ''.join(rows)
    css = CELL_CSS + '.hfr{display:grid;gap:6px;padding:4px}.hfr + .hfr{margin-top:6px}'
    html = f'<style>{css}</style><div class="wr">{cells(sample)}</div>'
    alt = (f'A primary button, a quiet button and a link, each at rest, on hover and with focus, on Newsprint and on '
           f'Charcoal. On hover the primary button’s fill steps one shade, {F["hover_n"]} to 1 from its rest, and '
           'its label underlines; the quiet button’s edge grows from 1 to 2 px; the link’s underline grows from '
           f'1 to 2 px. With focus each takes a 2 px ring 2 px outside it, Verdigris on Newsprint, {F["ring_n"]} to 1, '
           f'and Newsprint on Charcoal, {F["ring_c"]}. On Charcoal the ring around the Newsprint button is the same '
           'color as its fill, and the 2 px gap of Charcoal between them shows the ring.')
    return spec('s-17-9-correct', html, '17.9', alt, notes='Hover and focus drawn as states (classes), not live, so the '
                'plate shows all three at once on both surfaces.')


def s17_9_failure():
    css, band = fail_band()
    extra = ('.qx{box-shadow:inset 0 0 0 1px var(--oa-color-border-strong)}'
             '.f0{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring);outline-offset:0}')

    def sample(theme):
        return ('<div class="hfr"><p class="sf">Focus with no gap</p><div class="row" style="padding:4px">'
                '<span class="btn pri f0">Save</span></div></div>'
                '<div class="hfr"><p class="sf">Hover drawn as an inset shadow</p><div class="row">'
                '<span class="btn qt qx">Save</span></div></div>')
    html = (f'<style>{css}{CELL_CSS}{extra}.hfr{{display:grid;gap:6px}}.hfr + .hfr{{margin-top:10px}}</style>'
            f'<div class="wr">{band}{cells(sample)}</div>')
    alt = (f'Failure case: do not publish. On Newsprint and on Charcoal, a primary button whose focus ring touches it '
           f'with no gap, and a quiet button whose hover is an inset shadow. On Charcoal the Newsprint ring meets the '
           f'Newsprint fill, {F["ring_on_fill_c"]} to 1, so focus only makes the button 2 px larger; with forced colors on, '
           'the inset shadow disappears and hover shows nothing.')
    return spec('s-17-9-failure', html, '17.9', alt, notes='Picture of a fault on both surfaces.')


# ---- 17.10 pressed, checked and current
def s17_10_correct():
    def sample(theme):
        return ('<div class="hfr"><p class="sf">Toggle buttons, pressed and not</p>'
                f'<div class="row"><span class="chip on">{check()}Housing</span><span class="chip">Schools</span></div></div>'
                '<div class="hfr"><p class="sf">A choice of one, checked</p>'
                f'<div class="seg"><span class="chip on">{check()}Fit width</span><span class="chip">Full size</span></div></div>'
                '<div class="hfr"><p class="sf">The current page in a list</p><ul class="nav">'
                '<li><span>16 Photography, illustration and video</span></li><li><span class="cur">17 Motion and states</span></li>'
                '<li><span>18 Components and interaction</span></li></ul></div>'
                '<div class="hfr"><p class="sf">The current part in a masthead</p><p><span class="uc">Behavior</span></p></div>')
    css = CELL_CSS + '.hfr{display:grid;gap:6px}.hfr + .hfr{margin-top:10px}'
    html = f'<style>{css}</style><div class="wr">{cells(sample)}</div>'
    alt = ('On Newsprint and on Charcoal: a Housing toggle that is pressed, with the selected check before the word, the '
           'word in bold and a 2 px edge, beside Schools with a 1 px edge; Fit width checked the same way beside Full '
           'size; a list of three chapters with 17 Motion and states as the current page, in bold on the selected band '
           f'with a 4 px bar; and Behavior, the current part in a masthead, in bold with a 2 px underline. The band measures {F["band_n"]} '
           f'to 1 against Newsprint and {F["band_c"]} against Charcoal, so the bar and the weight carry it.')
    return spec('s-17-10-correct', html, '17.10', alt)


def s17_10_failure():
    css, band = fail_band()
    extra = ('.x1{background:var(--oa-color-action-primary-fill);color:var(--oa-color-action-primary-label);'
             'text-decoration:underline;border-color:var(--oa-color-action-primary-fill)}'
             '.x2{font-weight:700;text-decoration:underline;border-width:var(--oa-border-width-rule)}'
             '.hfr{display:grid;gap:6px}.hfr + .hfr{margin-top:10px}')
    html = (f'<style>{css}{CELL_CSS}{extra}</style><div class="wr">{band}'
            '<div class="hfr"><p class="sf">Size of this picture</p><div class="seg"><span class="chip x1">Fit to window</span>'
            '<span class="chip">True size</span></div></div>'
            '<div class="hfr"><p class="sf">Page view</p><div class="seg"><span class="chip x2">Full size</span>'
            '<span class="chip">Fit width</span></div></div>'
            f'<div class="hfr"><p class="sf">Filters</p><div class="row"><span class="chip on">{check()}Housing</span>'
            '<span class="chip">Schools</span></div></div></div>')
    alt = ('Failure case: do not publish. Three controls in one view show the chosen option three ways: Fit to window '
           'filled in Charcoal and underlined; Full size in bold, underlined, with a 2 px edge; and a Housing chip with '
           'a check, bold words and a 2 px edge.')
    return spec('s-17-10-failure', html, '17.10', alt)


# ---- 17.11 disabled
def s17_11_correct():
    def sample(theme):
        return ('<div class="hfr"><p class="sf">Before a size is chosen</p>'
                f'<div class="st-l"><span class="btn dis">{uicon("download")}Download the files</span>'
                '<p class="why">Choose a size to download.</p></div></div>'
                '<div class="hfr"><p class="sf">After</p>'
                f'<div class="row"><span class="btn pri">{uicon("download")}Download the files</span></div></div>')
    css = CELL_CSS + '.hfr{display:grid;gap:6px}.hfr + .hfr{margin-top:12px}'
    html = f'<style>{css}</style><div class="wr">{cells(sample)}</div>'
    alt = (f'A download button before and after a size is chosen, on Newsprint and on Charcoal. Before: a dashed edge, '
           f'its words readable at {F["dis_n"]} to 1 on Newsprint and {F["dis_c"]} on Charcoal, and under it “Choose a '
           'size to download.” After: the primary button, filled, with the same words.')
    return spec('s-17-11-correct', html, '17.11', alt)


def s17_11_failure():
    css, band = fail_band()
    html = (f'<style>{css}{CELL_CSS}.fade{{opacity:0.4}}</style><div class="wr">{band}'
            f'<div class="row"><span class="btn qt fade">{uicon("download")}Download the files</span></div></div>')
    alt = (f'Failure case: do not publish. A download button faded to 40 percent on Newsprint, its words at '
           f'{F["faded_n"]} to 1, with no line that says why it is unavailable.')
    return spec('s-17-11-failure', html, '17.11', alt, exempt=['contrast'],
                notes=f'Picture of a fault: opacity, {F["faded_n"]} to 1 on Newsprint, no reason.')


# ---- 17.12 empty
def s17_12_correct():
    def sample(theme):
        return ('<div class="st-l" style="gap:8px"><p class="lb">Search the symbols</p>'
                f'<p class="fld">{uicon("search")}<span>parking meter</span></p>'
                f'<div class="em"><p>0 of {N_LIB} symbols. No symbol matches.</p>'
                '<p>Clear the search or the filters to see more.</p></div></div>')
    html = f'<style>{CELL_CSS}</style><div class="wr"><p style="margin:0 0 12px">{ILLUS}</p>{cells(sample)}</div>'
    alt = ('A symbol search with no match, on Newsprint and on Charcoal: the label “Search the symbols”, a field holding '
           f'“parking meter”, and under it a dashed region whose words say “0 of {N_LIB} symbols. No symbol matches. Clear the '
           'search or the filters to see more.”')
    return spec('s-17-12-correct', html, '17.12', alt, illustrative=True,
                notes='D2-1157: the count and the advice in one status line.')


def s17_12_failure():
    css, band = fail_band()
    html = (f'<style>{css}{CELL_CSS}.blank{{min-height:6rem}}</style><div class="wr">{band}<div class="st-l" style="gap:8px">'
            f'<p class="lb">Search the symbols</p><p class="fld">{uicon("search")}<span>parking meter</span></p>'
            '<p class="why">No results.</p><div class="blank"></div></div></div>')
    alt = ('Failure case: do not publish. The same search with “No results.” in small secondary words and a blank space '
           'under it, with no edge, no count and no step to take.')
    return spec('s-17-12-failure', html, '17.12', alt)


# ---- the chapter's opener (the fix brief's call 8, CD-S18, D2-1550): the ten states strip
def s17_opener():
    """The ten states of Rule 17.8 in the order of its plate, one small sample each at true size, on the page's own
    ground. A picture that flows with the column: five a row from 40rem, two on a phone, one at large text sizes. Every
    color is a short name, so the strip follows the page's theme. Under 6 KB (D2-1550)."""
    def lab(t):
        return f'font:var(--oa-type-{t});letter-spacing:var(--oa-type-{t}-letter-spacing);text-transform:var(--oa-type-{t}-text-transform)'
    css = ('.op{container-type:inline-size}:where(.op p){margin:0}'
           '.g{list-style:none;margin:0;padding:0;display:grid;gap:16px;grid-template-columns:minmax(0,1fr)}'
           '@container (min-width:15rem){.g{grid-template-columns:repeat(2,minmax(0,1fr))}}'
           '@container (min-width:40rem){.g{grid-template-columns:repeat(5,minmax(0,1fr))}}'
           '.g li{display:grid;gap:8px;align-content:start;justify-items:start;min-width:0}'
           '.n{' + lab('label') + ';color:var(--oa-color-text-secondary)}'
           '.s{' + lab('caption') + ';color:var(--oa-color-text-primary)}'
           '.b{display:inline-flex;align-items:center;gap:6px;min-height:var(--oa-size-target-touch);padding:0 14px;'
           'border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);background:var(--oa-color-surface);' + lab('ui') + '}'
           '.b svg,.m svg{flex:none;display:block}'
           '.hv{border-width:var(--oa-border-width-rule);padding:0 13px}'
           '.fo{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring);outline-offset:var(--oa-border-focus-offset)}'
           '.ds{color:var(--oa-component-button-disabled-label);border-style:dashed;border-color:var(--oa-component-button-disabled-edge)}'
           '.on{border-width:var(--oa-border-width-rule);font-weight:700;padding:0 13px 0 7px}'
           '.mu{display:flex;gap:8px;align-items:center;color:var(--oa-color-state-muted-text)}'
           '.mu circle{fill:none;stroke:var(--oa-color-state-muted-mark);stroke-width:1.5}'
           '.ld{display:grid;gap:6px;color:var(--oa-color-state-loading-text)}'
           '.ld line{stroke:var(--oa-color-state-loading-mark);stroke-width:1.5}'
           '.m{display:flex;gap:6px;align-items:flex-start;padding:6px 8px}.m b{font-weight:700}'
           '.wn{border-left:var(--oa-border-width-bar) solid var(--oa-color-state-warning-mark);color:var(--oa-color-state-warning-text)}'
           '.er{border-left:var(--oa-border-width-bar) solid var(--oa-color-state-error-bar);'
           'background-color:var(--oa-color-state-error-band);color:var(--oa-color-state-error-text)}'
           '.ok{color:var(--oa-color-state-success-text)}.ok svg{color:var(--oa-color-state-success-mark)}'
           '.em{padding:8px 12px;border:var(--oa-border-width-hairline) dashed var(--oa-color-state-empty-edge);'
           'color:var(--oa-color-state-empty-text)}')
    cells = [
        ('Muted', '<p class="s mu"><svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">'
                  '<circle cx="8" cy="8" r="5.25"/></svg>Outside this view</p>'),
        ('Disabled', '<span class="b ds">Download</span>'),
        ('Hover', '<span class="b hv">Save</span>'),
        ('Focus', '<span class="b fo">Save</span>'),
        ('Loading', '<p class="s ld"><svg width="96" height="8" viewBox="0 0 96 8" aria-hidden="true" focusable="false">'
                    '<line x1="0" y1="4" x2="96" y2="4"/></svg>Loading the tracker</p>'),
        ('Selected', f'<span class="b on">{check()}Housing</span>'),
        ('Warning', f'<p class="s m wn">{uicon("warning")}<span><b>Warning:</b> Checked in October</span></p>'),
        ('Error', f'<p class="s m er" {RED_ERR}>{uicon("error")}<span><b>Error:</b> Enter a date</span></p>'),
        ('Empty', '<p class="s em">No symbol matches</p>'),
        ('Success', f'<p class="s m ok">{uicon("success")}<span>Saved</span></p>'),
    ]
    lis = ''.join(f'<li><p class="n">{n}</p>{x}</li>' for n, x in cells)
    html = f'<style>{css}</style><div class="op"><ul class="g">{lis}</ul></div>'
    alt = ('The ten states in a strip, each named above a small sample at true size: muted, “Outside this view” in '
           'secondary words with an outline dot; disabled, a Download button with a dashed edge; hover, a Save button '
           'with a 2 px edge; focus, a Save button with a 2 px ring 2 px outside it; loading, a still line and “Loading '
           'the tracker”; selected, a Housing chip with a check, bold words and a 2 px edge; warning, the warning mark '
           'and “Warning: Checked in October” beside a 4 px bar in ink; error, the error mark and “Error: Enter a date” '
           'beside a 4 px Pillar Red bar; empty, “No symbol matches” in a dashed box; success, the success mark and '
           '“Saved”. Rule 17.8 draws each one in full.')
    return spec('s-17-opener', html, None, alt,
                notes='Chapter 17’s opener (call 8 of the round 2 fix brief, D2-1134, D2-1550): the ten states of Rule '
                      '17.8 in its order, flowing with the column; short names only, so it follows the page’s theme. '
                      'The error’s red bar is the strip’s one working red.')


# ------------------------------------------------------------------------------------------------ the identity slots
def identity_slots():
    """The identity designer's Rule 17.6 specimens, if any have landed (see the module docstring)."""
    if not ID_MANIFEST.exists():
        return {}, []
    man = json.loads(ID_MANIFEST.read_text())
    ours = {k: v for k, v in man.items() if re.match(r'^s-17-(hinge|lever)-', k) and (OUT_SP / f'{k}.html').exists()}
    used = set()

    def pick(names):
        for n in names:
            if n in ours and n not in used:
                used.add(n)
                return n
        return None
    slots = {'correct': pick(['s-17-hinge-correct', 's-17-lever-correct']),
             'failure': pick(['s-17-hinge-failure', 's-17-lever-failure'])}
    extras = [k for k in sorted(ours) if k not in used]
    return {k: (v, ours[v]) for k, v in slots.items() if v}, [(k, ours[k]) for k in extras]


# ------------------------------------------------------------------------------------------------ the chapter
def build_chapter():
    slots, id_extras = identity_slots()
    s17_1_correct(); s17_1_failure()
    s17_2_correct(); s17_2_failure()
    s17_3_correct(); s17_3_failure()
    s17_4_correct(); s17_4_failure()
    s17_5_correct(); s17_5_failure()
    if 'correct' not in slots:
        s17_6_pending()
    if 'failure' not in slots:
        s17_6_pending_failure()
    s17_7_correct(); s17_7_failure()
    s17_8_correct(); s17_8_failure()
    s17_9_correct(); s17_9_failure()
    s17_10_correct(); s17_10_failure()
    s17_11_correct(); s17_11_failure()
    s17_12_correct(); s17_12_failure()
    s17_opener()

    def idblock(kind, default_sid, default_cap):
        if kind in slots:
            sid, meta = slots[kind]
            cap = meta.get('caption') or default_cap
            if kind == 'failure' and not cap.startswith('<strong>Fails'):
                cap = '<strong>Fails Rule 17.6.</strong> ' + cap     # every failure caption opens so (chapters 05 to 11)
            return {'specimen': sid, 'caption': cap}
        return {'specimen': default_sid, 'caption': default_cap}

    rules = []

    rules.append({
        'id': '17.1',
        'title': 'Move something only to explain a state or a mechanism.',
        'rule': [
            'Motion has two jobs. It shows a state changing, as when a bill finishes one step and moves to the next, and '
            'it shows a mechanism at work, as when a link draws from a cause to its effect. A mark that would move for '
            'any other reason, to decorate a page or to catch the eye, stays still.',
            f'A reader’s own actions, such as a hover, a toggle or a change of theme, answer at once or within the fast '
            f'duration, {ms_words(FAST)}. The focus ring shows at once, with no motion at all.'],
        'tokens': ['oa.motion.duration.fast', 'oa.motion.duration.standard', 'oa.motion.duration.slow'],
        'why': {'text': [
            'A moving mark draws the eye before the words around it, so a motion with no change behind it takes a reader '
            'away from the sentence they came to read. For some readers motion costs more than attention. The W3C’s '
            'Media Queries Level 5 says the motion a reduced motion setting removes can “trigger '
            'discomfort for those with vestibular motion sensitivity, or distraction for those with attention deficits.” '
            'The vestibular sense is the inner ear’s sense of balance and motion.'],
            'basis': 'Design judgment, with the W3C’s Media Queries Level 5'},
        'correct': {'specimen': 's-17-1-correct', 'caption':
                    'Live. Press Play and bill S.99002 moves from step 3, Committee vote, to step 4, First chamber. Step 3 '
                    'lands as done, then the ring that marks where the bill is now slides to step 4 and draws the line '
                    'behind it. Every part of the motion shows something that changed.'},
        'failure': {'specimen': 's-17-1-failure', 'caption':
                    '<strong>Fails Rule 17.1.</strong> A count rises from 0 to 1,284 as the page opens. Nothing changed '
                    'for the reader: the number was known before the page drew, and the motion makes them wait for it.'},
        'specs': [
            {'label': 'A state changes', 'value': 'A step finishes; a bill moves on; a mark arrives at its new state'},
            {'label': 'A mechanism works', 'value': 'A link draws from cause to effect; the current step of a loop moves on'},
            {'label': 'A reader’s own action', 'value': f'Hover and toggles at once or in {ms_words(FAST)}; the focus ring at once',
             'token': 'oa.motion.duration.fast'},
            {'label': 'Leave out', 'value': 'Autoplaying video, looping animation, parallax, motion tied to scrolling, bounce or '
                                            'elastic easing, animated gradients, confetti, counters that tick up and hover that moves layout'},
        ],
        'related': ['11', '15', '18'],
        'builders': [
            'Before you add a motion, write the sentence it shows, such as “Step 3 is done and the bill is now at step 4.” '
            'If no change gives you that sentence, leave the mark still.',
            'Keep native scrolling. Tie no motion to the scroll position, and take nothing over from the wheel or the '
            'keys that scroll the page.'],
    })

    rules.append({
        'id': '17.2',
        'title': 'Time every motion with the nine motion tokens.',
        'rule': [
            f'Every duration and easing in a motion comes from a token: three durations for most moves, a {STAG}{NB}ms '
            'stagger between marks that move one after another, two durations kept for the hinge and the lever, and three easings. A motion reads '
            'them from tokens.css by name, so a reduced motion setting reaches it (Rule 17.4).',
            f'Hover and toggles take the fast duration, {ms_words(FAST)}. Reveals, panels, a mark that lands and a line '
            f'that draws on its own take the standard {ms_words(STD)}, and a move across a page or a component takes the '
            f'slow {ms_words(SLOW)}. The easing follows where a mark goes: the enter easing for a mark that arrives, the '
            'exit easing at the fast duration for one that leaves, and the standard easing for one that moves from place '
            'to place.'],
        'tokens': ['oa.motion.duration.fast', 'oa.motion.duration.standard', 'oa.motion.duration.slow',
                   'oa.motion.duration.stagger', 'oa.motion.duration.hinge', 'oa.motion.duration.lever',
                   'oa.motion.easing.standard', 'oa.motion.easing.enter', 'oa.motion.easing.exit'],
        'why': {'text': [
            f'These are our fifth edition’s values, kept as they were. Nothing in the set runs longer than '
            f'{ms_words(HINGE)}, so a motion is over before a reader’s eye moves on. The three easings slow down '
            'into place, or speed away from it, and none passes its place and comes back, so a mark rests exactly where '
            'the still view draws it.'],
            'basis': 'Design judgment, kept from our fifth edition'},
        'correct': {'specimen': 's-17-2-correct', 'caption':
                    f'The nine tokens. The six durations share one scale, with the hinge’s {ms_words(HINGE)} across '
                    'its full width, and each easing is drawn as its curve.'},
        'failure': {'specimen': 's-17-2-failure', 'caption':
                    '<strong>Fails Rule 17.2.</strong> A transition written with its own numbers. A reduced motion '
                    f'setting never reaches 250{NB}ms, and the curve goes {OVER} percent past its place before it comes '
                    'back.'},
        'specs': [
            {'label': 'Fast', 'value': f'{ms_words(FAST)}; hover and toggles', 'token': 'oa.motion.duration.fast'},
            {'label': 'Standard', 'value': f'{ms_words(STD)}; reveals, panels, a land, a draw on its own', 'token': 'oa.motion.duration.standard'},
            {'label': 'Slow', 'value': f'{ms_words(SLOW)}; a move across a page or a component', 'token': 'oa.motion.duration.slow'},
            {'label': 'Stagger', 'value': f'{ms_words(STAG)} between marks that move one after another', 'token': 'oa.motion.duration.stagger'},
            {'label': 'Hinge', 'value': f'{ms_words(HINGE)}, on request only (Rule 17.6)', 'token': 'oa.motion.duration.hinge'},
            {'label': 'Lever', 'value': f'{ms_words(LEVER)}, on request only (Rule 17.6)', 'token': 'oa.motion.duration.lever'},
            {'label': 'Standard easing', 'value': f'{bz("standard")}; a move from place to place', 'token': 'oa.motion.easing.standard'},
            {'label': 'Enter easing', 'value': f'{bz("enter")}; a mark that arrives', 'token': 'oa.motion.easing.enter'},
            {'label': 'Exit easing', 'value': f'{bz("exit")}; a mark that leaves, at the fast duration', 'token': 'oa.motion.easing.exit'},
        ],
        'related': ['26'],
        'builders': [
            'Write <code>transition: transform var(--oa-motion-duration-standard) var(--oa-motion-easing-enter)</code>, '
            'never the number. A script reads the same names with <code>getComputedStyle(el).getPropertyValue('
            '\'--oa-motion-duration-slow\')</code>, which gives <code>320ms</code>, or <code>0ms</code> under reduced motion.'],
    })

    rules.append({
        'id': '17.3',
        'title': 'Play a motion only when a reader asks, with Play, Pause, Reset and a still view.',
        'rule': [
            'A motion starts when a reader presses Play, and never as the page opens, as it scrolls into view or on a '
            'timer. It runs once and stops on its last frame. One button carries Play and Pause and '
            'changes its icon and its word together, then reads Play again at the end.',
            'A player of a state or a mechanism rests on its first frame, where the change starts. For the wordmark or '
            'the lockmark, the player rests on the master itself, so a reader who never presses Play still sees the '
            'whole mark; Play then steps to the first frame and runs to the master. Reset returns either kind to where '
            'it rests, and at rest Reset is unavailable and says why.',
            'Beside every player sits its still view: the first and last frames at true size, each with its time and the '
            'words for what it shows, then each step of the motion in order. A status line says the same words when the '
            'frame changes, so every fact the motion shows reaches a reader who prints the page or listens with a screen '
            'reader, and one who never presses Play.'],
        'tokens': ['oa.size.target.touch', 'oa.size.icon.medium'],
        'why': {'text': [
            'WCAG 2.2 success criterion 2.2.2 Pause, Stop, Hide asks for a way to pause anything that starts on its own '
            'and moves for more than five seconds. Our motions last under a second and never start on their own, so none '
            'needs it. Every player has the controls all the same, and a reader decides when each mark moves. Slow '
            'motion stretches a motion to a few seconds, which gives Pause time to work and lets a reader see the easing.'],
            'basis': 'WCAG 2.2 SC 2.2.2; design judgment'},
        'correct': {'specimen': 's-17-3-correct', 'caption':
                    'The parts of a player, numbered from top to bottom, drawn from the live player in Rule 17.4. It shows '
                    'a mechanism, so it rests on its first frame. Each part has its words, and the controls stand 44 px '
                    'tall.'},
        'failure': {'specimen': 's-17-3-failure', 'caption':
                    '<strong>Fails Rule 17.3.</strong> The bill moves as the page opens and again every three seconds, so it '
                    'seems to go back and forth between two steps. Its one button has an icon and no word, and there is '
                    'no Pause, Reset or still view.'},
        'specs': [
            {'label': 'Play and Pause', 'value': 'One button; its icon and word change together: Play, Pause, Play again'},
            {'label': 'At rest', 'value': 'A state or a mechanism: its first frame. The wordmark or the lockmark: its master'},
            {'label': 'Reset', 'value': 'Returns the player to where it rests; unavailable at rest, with its reason'},
            {'label': 'Slow motion', 'value': 'A check box that plays at one tenth speed; unavailable under reduced motion, with its reason'},
            {'label': 'Still view', 'value': 'First and last frames at true size, each with its time and words, then the steps in order'},
            {'label': 'Status line', 'value': 'Polite, so a screen reader waits until it finishes speaking; it says Playing, Paused and the words of the frame the motion stops on'},
            {'label': 'Controls', 'value': '44 px tall, with 24 px icons beside their words', 'token': 'oa.size.target.touch'},
            {'label': 'Runs', 'value': 'Once for each press; never on load, on scroll or on a timer; never loops'},
        ],
        'related': ['11', '18', '19'],
        'builders': [
            'Mark the player’s root <code>data-oa-motion</code>, its one Play and Pause button <code>data-oa-play '
            'data-oa-pause</code> and Reset <code>data-oa-reset</code>; the guide’s own check looks for them. A player '
            'that rests on its master also takes <code>data-oa-rest="master"</code> and loads with '
            '<code>data-frame="end"</code>. Start a motion from a click handler and nowhere else.',
            'Leave the last frame on screen when the motion ends. On load, draw a state or mechanism player at its '
            'first frame, and a player of the wordmark or the lockmark at its master.'],
    })

    rules.append({
        'id': '17.4',
        'title': 'Under reduced motion, show the last frame at once.',
        'rule': [
            'When a reader’s device asks for reduced motion, every motion duration token resolves to 0 ms, and '
            'pressing Play draws the last frame at once. The player keeps its buttons and its words, so the reader still '
            'chooses when the change shows and reads in the status line what changed.',
            'tokens.css does this itself, with the media query <code>prefers-reduced-motion</code>, which every current '
            'browser supports. A motion that reads its timing from the tokens follows the setting with no code of its own.'],
        'tokens': ['oa.motion.duration.standard', 'oa.motion.duration.slow'],
        'why': {'text': [
            'The W3C’s Media Queries Level 5 says the reduce value “Indicates that user has notified the system that '
            'they prefer an interface that removes or replaces the types of motion-based animation that either trigger '
            'discomfort for those with vestibular motion sensitivity, or distraction for those with attention deficits.” '
            'Drawing the last frame keeps every fact the motion shows and removes the movement alone.'],
            'basis': 'Media Queries Level 5, W3C Working Draft, February 19, 2026'},
        'correct': {'specimen': 's-17-4-correct', 'caption':
                    'Live. The first link of Loop R1 from our systems atlas draws from wealth concentration to money in '
                    'politics, and the arrowhead and the second node land. Turn on Preview reduced motion, or set your '
                    'device to reduce motion, and Play draws the last frame at once. The line under the check boxes says '
                    'what your device asks for now.'},
        'failure': {'specimen': 's-17-4-failure', 'caption':
                    '<strong>Fails Rule 17.4.</strong> A script times its own 400 ms. The setting reaches tokens.css, '
                    'which the script never reads, so a reader who asked for reduced motion still watches the link draw.'},
        'specs': [
            {'label': 'Durations', 'value': 'All six resolve to 0 ms: fast, standard, slow, stagger, hinge and lever',
             'token': 'oa.motion.duration.standard'},
            {'label': 'Easings', 'value': 'Unchanged; at 0 ms they have no effect'},
            {'label': 'Media query', 'value': '<code>@media (prefers-reduced-motion: reduce)</code>, already in tokens.css'},
            {'label': 'Controls', 'value': 'Kept: Play draws the last frame and Reset the first; Slow motion is unavailable, with its reason'},
            {'label': 'Browsers', 'value': 'First full support: Chrome 74, Edge 79, Firefox 63, Safari 10.1, Safari on iOS 10.3, '
                                           'by MDN’s compatibility data, checked November 10, 2026'},
        ],
        'related': ['19', '26'],
        'builders': [
            'In a script, read the duration at the moment of the press: <code>parseFloat(getComputedStyle(el)'
            '.getPropertyValue(\'--oa-motion-duration-slow\'))</code> gives 320, or 0 under reduced motion. When every '
            'duration is 0, set the last frame and start no animation.',
            'To check a page, turn on reduced motion in your device settings, or in Chrome’s developer tools under '
            'Rendering, “Emulate CSS media feature prefers-reduced-motion”, and press every Play.'],
    })

    rules.append({
        'id': '17.5',
        'title': 'Build every motion from three behaviors: slide, draw and land.',
        'rule': [
            'A slide moves a mark from one place to another along a straight line, over the slow duration with the '
            'standard easing. A draw extends a line along its own path from its start, over the standard duration with '
            'the enter easing, and a line drawn behind a sliding mark takes the slide’s duration and easing so the '
            f'two keep pace. A land brings a mark to rest: it appears at {round(LAND_FROM * 100)} percent of its size and '
            'settles to its true size over the standard duration with the enter easing.',
            'A motion may join two or three of them in order, one stagger apart, as a bill does when its step lands and '
            'its ring slides on (Rule 17.1). Nothing in a behavior fades, since no state uses opacity, and nothing passes '
            'its place and comes back.'],
        'tokens': ['oa.motion.duration.slow', 'oa.motion.duration.standard', 'oa.motion.easing.standard',
                   'oa.motion.easing.enter', 'oa.motion.duration.stagger'],
        'why': {'text': [
            'Our fifth edition named these three behaviors and timed them, and this edition keeps both. It sets the size '
            f'a land starts from at {round(LAND_FROM * 100)} percent, the step our fifth edition’s lever took when it '
            'landed at 1.4 times a node and settled at 1.25, so every land in our products keeps that one proportion. A '
            'reader who has seen a ring slide to a bill’s next step reads the same slide in a loop on the atlas.'],
            'basis': 'Design judgment, kept and refined from our fifth edition'},
        'correct': {'specimen': 's-17-5-correct', 'caption':
                    'Live. Each behavior on its own: a ring slides from one place to the next, a line draws from its first '
                    'node to its second, and a disc lands on its node. Slow motion plays each at one tenth speed.'},
        'failure': {'specimen': 's-17-5-failure', 'caption':
                    '<strong>Fails Rule 17.5.</strong> A disc lands with a bounce. It shrinks, swells past its node and '
                    'shrinks again, so it sits at four sizes before it rests, and the extra movement says nothing about '
                    'the state.'},
        'specs': [
            {'label': 'Slide', 'value': f'{ms_words(SLOW)}, standard easing; a straight line between two places', 'token': 'oa.motion.duration.slow'},
            {'label': 'Draw', 'value': f'{ms_words(STD)}, enter easing; behind a slide, the slide’s duration and easing',
             'token': 'oa.motion.easing.enter'},
            {'label': 'Land', 'value': f'{ms_words(STD)}, enter easing; from {round(LAND_FROM * 100)} percent to true size',
             'token': 'oa.motion.duration.standard'},
            {'label': 'Together', 'value': f'In order, {ms_words(STAG)} apart', 'token': 'oa.motion.duration.stagger'},
            {'label': 'Leaving', 'value': f'A mark that leaves: the exit easing at {ms_words(FAST)}', 'token': 'oa.motion.easing.exit'},
            {'label': 'What moves', 'value': 'A mark’s place, the length of a drawn line and a mark’s size; never opacity, never layout'},
        ],
        'related': ['11', '15'],
        'builders': [
            'Animate <code>transform</code> and <code>stroke-dashoffset</code> only, so the text around a mark never moves. '
            'Give a drawn line <code>pathLength="1"</code> and <code>stroke-dasharray="1 1"</code>, then move '
            '<code>stroke-dashoffset</code> from 1 to 0 to draw it whole at any length.'],
    })

    hinge_cap = ('Coming later: the hinge, live. Until it is drawn, Rule 04.5 shows the hinge diagram at rest.')
    lever_fail_cap = ('Coming later: a failure case for the hinge and the lever, a last frame that misses its master.')
    rules.append({
        'id': '17.6',
        'title': 'Move the hinge and the lever only as their own motions, ending exactly on their masters.',
        'rule': [
            'The hinge and the lever are the two motions that belong to the identity, and each one plays only on request '
            f'(Rule 17.3). The hinge plays over {ms_words(HINGE)}: OATH and ACTION settle into place, then the ampersand '
            f'lands between them. The lever plays over {ms_words(LEVER)} in the lockmark: its links draw, its nodes land '
            'together and the lever lands last, at bottom right.',
            'Each player rests on the master itself (Rule 17.3). Play steps to the first frame and runs to the master, '
            'and Reset returns to the master; at rest Reset is unavailable, with the line “The mark is at rest on its '
            'master.”',
            'Each is built from slide, draw and land (Rule 17.5), and each ends on a last frame that matches the approved '
            'master for its size, pixel for pixel. The ampersand and the lever keep signature red in every frame, and '
            'signature red never counts as a view’s working red (Rule 05.3).'],
        'tokens': ['oa.motion.duration.hinge', 'oa.motion.duration.lever'],
        'why': {'text': [
            'The hinge and the lever carry our name and our idea of a place where one change moves the rest, so a reader '
            'who sees them move should see them arrive as the same drawings they meet everywhere else. A last frame a '
            'pixel off its master would show a second version of the mark.'],
            'basis': 'Design judgment; Rules 04.1 and 08.1'},
        'correct': idblock('correct', 's-17-6-pending', hinge_cap),
        'failure': idblock('failure', 's-17-6-pending-failure', lever_fail_cap),
        'specs': [
            # the identity designer's draft words (20261111_Stage-C-Round-1-Identity-Notes.md), times from the tokens
            {'label': 'Hinge', 'value': f'{ms_words(HINGE)} in all, on request: OATH and ACTION slide toward each other '
                                        f'over the slow {ms_words(SLOW)}, and the ampersand lands from {ms_words(HINGE - STD)} '
                                        f'and comes to rest at {ms_words(HINGE)}', 'token': 'oa.motion.duration.hinge'},
            {'label': 'Lever', 'value': f'{ms_words(LEVER)} in all, on request: the links draw over {ms_words(STD)}, the '
                                        f'nodes land together from {ms_words(STD + STAG)}, and the lever lands from '
                                        f'{ms_words(LEVER - STD)} and comes to rest at {ms_words(LEVER)}',
             'token': 'oa.motion.duration.lever'},
            {'label': 'Built from', 'value': 'Slide, draw and land, with the enter easing for each arrival'},
            {'label': 'At rest', 'value': 'The master; Reset unavailable, with “The mark is at rest on its master.”'},
            {'label': 'Last frame', 'value': 'The approved master for the size shown, pixel for pixel'},
            {'label': 'Reduced motion', 'value': 'The master at once (Rule 17.4)'},
        ],
        'related': ['04', '08'],
        'builders': [
            'Animate the master itself, never a redrawn copy, and compare the last frame with the master at its size '
            'before it ships.',
            'When the motion ends, show the master file itself, placed as Rules 03.1 and 08.1 place it, so the last '
            'frame is the master. Check the last frame on a 1x screen, since a 2x screen hides a mark that rests half a '
            'pixel off the grid.'],
    })
    rules.append({
        'id': '17.7',
        'title': 'Show loading with words and a still drawing, never a pulse.',
        'rule': [
            'While a region waits for its data, it shows words that name what is loading, such as “Loading the tracker '
            'for S.99002.” <span class="illus">Illustrative</span>, and a still drawing of the lines the data will sit on, with no marks on them yet. The words '
            'sit in a status line, so a screen reader hears them once. Nothing moves while the region waits.',
            'The data replaces the drawing and the words together. When the data fails to arrive, the region shows the '
            'error state with what failed and the fix (Rule 11.15).'],
        'tokens': ['oa.color.state.loading.text.onNewsprint', 'oa.color.state.loading.mark.onNewsprint'],
        'why': {'text': [
            'A pulse repeats for as long as the wait lasts, which puts it under WCAG 2.2 success criterion 2.2.2 Pause, '
            'Stop, Hide once the wait passes five seconds. Our fifth edition’s pulsing lever also fell to 1.27 to 1 '
            'against Newsprint at its faintest, under the 3 to 1 that success criterion 1.4.11 asks of a graphic a '
            'reader needs. Words say what is happening, '
            'and a screen reader can say them too. The drawing leaves out marks, because a step or a node on it would '
            'read as a state the data has not reached.'],
            'basis': 'WCAG 2.2 SC 2.2.2 and 1.4.11; design judgment'},
        'correct': {'specimen': 's-17-7-correct', 'caption':
                    f'A tracker that is loading, on Newsprint and on Charcoal. The line where the six steps will sit '
                    f'measures {F["load_n"]} to 1 on Newsprint and {F["load_c"]} on Charcoal, and the words name the bill.'},
        'failure': {'specimen': 's-17-7-failure', 'caption':
                    '<strong>Fails Rule 17.7.</strong> Our fifth edition’s loading pulse, in still frames. It fades '
                    'between 20 and 50 percent strength for as long as the wait lasts, and nothing says what is loading.'},
        'specs': [
            {'label': 'Words', 'value': 'What is loading, by name, in a status line', 'token': 'oa.color.state.loading.text.onNewsprint'},
            {'label': 'Drawing', 'value': f'The lines the data will sit on, with no marks; {F["load_n"]} to 1 on Newsprint',
             'token': 'oa.color.state.loading.mark.onNewsprint'},
            {'label': 'On Charcoal', 'value': f'Dim Newsprint words and drawing, {F["load_c"]} to 1', 'token': 'oa.color.state.loading.mark.onCharcoal'},
            {'label': 'Motion', 'value': 'None, with or without reduced motion'},
            {'label': 'When it fails', 'value': 'The error state, with what failed and the fix (Rule 11.15)'},
        ],
        'related': ['11', '18'],
        'builders': [
            'Put an empty element with <code>role="status"</code> on the page before the data is asked for, then write '
            'the words into it, so a screen reader hears them.'],
    })

    rules.append({
        'id': '17.8',
        'title': 'Give each of the ten states words or a shape as well as a color, on Newsprint and on Charcoal.',
        'rule': [
            'Ten states cover every control and region: muted, disabled, hover, focus, loading, selected, warning, error, '
            'empty and success. Each changes its words or its shape along with its color, so a reader who sees no color, '
            'prints in gray or reads in a dark theme gets the same state. This plate is the reference for all ten.',
            f'On Charcoal an error takes no band: the 4{NB}px Pillar Red bar measures {F["err_c"]} to 1 there, and the '
            'mark and the word “Error:” in Newsprint carry it. Every other state keeps the same shapes and words on both '
            'surfaces.'],
        'tokens': ['oa.color.state.muted.text.onNewsprint', 'oa.color.state.disabled.edge.onNewsprint',
                   'oa.color.state.loading.mark.onNewsprint', 'oa.color.state.selected.bar.onNewsprint',
                   'oa.color.state.warning.mark.onNewsprint', 'oa.color.state.error.bar.onNewsprint',
                   'oa.color.state.error.band.onNewsprint', 'oa.color.state.empty.edge.onNewsprint',
                   'oa.color.state.success.mark.onNewsprint', 'oa.border.width.bar'],
        'why': {'text': [
            'WCAG 2.2 success criterion 1.4.1 Use of Color asks that color never be the only way a state shows, and 1.4.11 '
            'Non-text Contrast asks 3 to 1 for the edges, marks and rings that show one. Each sample here reads only the '
            'short names, which a theme points at Newsprint’s values or Charcoal’s, so one set of code draws both columns, and a product '
            'that follows a reader’s theme changes its colors and keeps its words and shapes.'],
            'basis': 'WCAG 2.2 SC 1.4.1 and 1.4.11'},
        'correct': {'specimen': 's-17-8-correct', 'caption':
                    'The ten states, each on Newsprint and on Charcoal, with its cue in words. Each cell sets its own theme, '
                    'and every color in it comes from a short name that follows the theme.'},
        'failure': {'specimen': 's-17-8-failure', 'caption':
                    f'<strong>Fails Rule 17.8.</strong> Four states by color alone. The red words measure {F["red_text_n"]} '
                    f'to 1 and the Verdigris words {F["verd_text_n"]}, and a reader who sees neither color gets no state '
                    f'at all; the faded button falls to {F["faded_n"]} and gives no reason.'},
        'specs': [
            {'label': 'Muted', 'value': f'Secondary words in regular weight; outline marks, {F["muted_mark_n"]} to 1 on Newsprint',
             'token': 'oa.color.state.muted.mark.onNewsprint'},
            {'label': 'Disabled', 'value': f'Dashed edge, words at {F["dis_n"]} to 1 on Newsprint and {F["dis_c"]} on Charcoal, a reason line (Rule 17.11)',
             'token': 'oa.color.state.disabled.text.onNewsprint'},
            {'label': 'Hover', 'value': 'Underline or a 2 px edge; a filled button steps one shade (Rule 17.9)',
             'token': 'oa.color.action.primary.fillHover.onNewsprint'},
            {'label': 'Focus', 'value': f'2 px ring, 2 px gap; {F["ring_n"]} to 1 on Newsprint, {F["ring_c"]} on Charcoal (Rule 17.9)',
             'token': 'oa.color.focus.ring.onNewsprint'},
            {'label': 'Loading', 'value': 'Words and a still drawing (Rule 17.7)', 'token': 'oa.color.state.loading.text.onNewsprint'},
            {'label': 'Selected', 'value': 'Check, bold words, 2 px edge; in a list, the band and its 4 px bar (Rule 17.10)',
             'token': 'oa.color.state.selected.bar.onNewsprint'},
            {'label': 'Warning', 'value': f'Warning mark, “Warning:”, 4 px bar in the text’s ink, {F["warn_n"]} to 1',
             'token': 'oa.color.state.warning.mark.onNewsprint'},
            {'label': 'Error', 'value': f'Error mark in ink, “Error:”, the fix, 4 px Pillar Red bar; Error Band on Newsprint '
                                        f'(text {F["err_text_band"]} to 1), none on Charcoal (bar {F["err_c"]} to 1)',
             'token': 'oa.color.state.error.band.onNewsprint'},
            {'label': 'Empty', 'value': 'Dashed region; what is missing and what to do next (Rule 17.12)', 'token': 'oa.color.state.empty.edge.onNewsprint'},
            {'label': 'Success', 'value': f'Success mark in Verdigris, {F["ok_n"]} to 1 on Newsprint and {F["ok_c"]} on Charcoal, and words',
             'token': 'oa.color.state.success.mark.onNewsprint'},
        ],
        'related': ['05', '11', '18', '26'],
        'builders': [
            'Write a state’s colors with the short names, such as <code>var(--oa-color-state-error-bar)</code> for an error’s 4 px bar '
            'and <code>var(--oa-color-surface)</code>, never a name that ends in a surface. The theme and the surface '
            'classes point each short name at the right value, so the same code draws both columns of this plate.',
            'Draw every state bar as a border, <code>border-left: 4px solid</code>. Forced colors, a setting such as the '
            'contrast themes in Windows that repaints a page in a few system colors, removes an inset shadow and keeps a '
            'border.'],
    })

    rules.append({
        'id': '17.9',
        'title': 'Show hover with an underline or a thicker edge, and focus with a 2 px ring and its gap.',
        'rule': [
            'Hover underlines a label, grows a link’s underline from 1 to 2 px, or thickens a quiet control’s 1 px edge '
            'to 2 px. A quiet control is a button drawn as its word in ink inside that edge, on the page’s own ground. A '
            'filled button also steps its fill one shade. Hover never draws an inset shadow, which forced colors removes, '
            'and never moves layout.',
            'Focus draws a 2 px ring 2 px outside the control, at once: Verdigris on Newsprint and White, '
            f'Newsprint on Charcoal and Prussian. On Charcoal the ring around a Newsprint button measures '
            f'{F["ring_on_fill_c"]} to 1 against its fill, so the 2 px gap of Charcoal between them shows the '
            'ring.'],
        'tokens': ['oa.border.width.focusRing', 'oa.border.focusOffset', 'oa.color.focus.ring.onNewsprint',
                   'oa.color.focus.ring.onCharcoal', 'oa.border.width.underlineHover'],
        'why': {'text': [
            'WCAG 2.2 success criterion 2.4.7 Focus Visible asks that keyboard focus always show, and 2.4.11 Focus Not '
            'Obscured (Minimum) asks that content we place never hide it entirely. A ring outside the control, in a color measured '
            'on the surface, shows on every control, filled or not. An underline and an edge are lines in the text’s '
            'own ink, so they stay when forced colors repaints the page.'],
            'basis': 'WCAG 2.2 SC 2.4.7 and 2.4.11'},
        'correct': {'specimen': 's-17-9-correct', 'caption':
                    'A primary button, a quiet button and a link at rest, on hover and with focus, on Newsprint and on '
                    'Charcoal. On Charcoal the ring around the Newsprint button is the same color as the button, and the '
                    'gap shows it.'},
        'failure': {'specimen': 's-17-9-failure', 'caption':
                    '<strong>Fails Rule 17.9.</strong> A ring with no gap merges with a Newsprint button on Charcoal, so '
                    'focus only makes the button 2 px larger. Hover drawn as an inset shadow disappears under forced '
                    'colors.'},
        'specs': [
            {'label': 'Hover, words and links', 'value': 'Underline; a link’s grows from 1 to 2 px', 'token': 'oa.border.width.underlineHover'},
            {'label': 'Hover, filled button', 'value': f'Fill steps one shade, {F["hover_n"]} to 1 on Newsprint and {F["hover_c"]} on Charcoal; label underlines',
             'token': 'oa.color.action.primary.fillHover.onNewsprint'},
            {'label': 'Hover, quiet control', 'value': 'Edge from 1 to 2 px, with no shift in size', 'token': 'oa.border.width.rule'},
            {'label': 'Hover timing', 'value': f'At once, or the fast {ms_words(FAST)}', 'token': 'oa.motion.duration.fast'},
            {'label': 'Focus ring', 'value': '2 px outline, at once', 'token': 'oa.border.width.focusRing'},
            {'label': 'Focus gap', 'value': '2 px; never 0', 'token': 'oa.border.focusOffset'},
            {'label': 'Ring color', 'value': f'Verdigris on Newsprint {F["ring_n"]} to 1 and White {F["ring_w"]}; Newsprint on '
                                             f'Charcoal {F["ring_c"]} and Prussian {F["ring_p"]}', 'token': 'oa.color.focus.ring.onNewsprint'},
        ],
        'related': ['18', '19'],
        'builders': [
            'Draw the ring with <code>:focus-visible</code> and <code>outline</code>: <code>outline: '
            'var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring); outline-offset: '
            'var(--oa-border-focus-offset)</code>. Forced colors keeps an outline and removes a box shadow.',
            'When hover thickens an edge, take the extra pixel from the padding, so the control keeps its size and '
            'nothing beside it moves.'],
    })

    rules.append({
        'id': '17.10',
        'title': 'Draw pressed, checked and current choices one way: a check, bold words and a 2 px edge.',
        'rule': [
            'A toggle that is pressed, a choice that is checked and the current choice in a set all draw one look: the '
            'selected check before the word, the word in bold and a 2 px edge in the strong border color where the '
            'others keep 1 px. The look is the same on Newsprint and Charcoal and stays under forced colors, since '
            'the check, the weight and the edge are shapes.',
            'Links and lists of places keep their own marks for the current place. A link to the page a reader is on '
            'takes bold words, with a 2 px underline in a masthead and none at the end of a breadcrumb, and a rail '
            'or a list takes the selected band, its 4 px bar and bold words.'],
        'tokens': ['oa.border.width.rule', 'oa.color.border.strong.onNewsprint', 'oa.color.state.selected.band.onNewsprint',
                   'oa.color.state.selected.bar.onNewsprint'],
        'why': {'text': [
            'Our pages drew one idea three ways: one switch filled and underlined its choice, one pair turned bold and '
            'thickened its edge, and the filter chips added a check. A reader who learns one look reads every control '
            f'the same way. The check, the weight and the edge carry it without color: the selected band sits only '
            f'{F["band_n"]} to 1 from Newsprint, so the bar beside it does that work in a list.'],
            'basis': 'Design judgment; WCAG 2.2 SC 1.4.1'},
        'correct': {'specimen': 's-17-10-correct', 'caption':
                    'A pressed toggle, a checked choice, the current page in a list and the current part in a masthead, on '
                    'Newsprint and on Charcoal.'},
        'failure': {'specimen': 's-17-10-failure', 'caption':
                    '<strong>Fails Rule 17.10.</strong> Three controls in one view mark their choice three ways: a fill '
                    'with an underline, bold words with an underline and a thick edge, and a check with bold words.'},
        'specs': [
            {'label': 'Check', 'value': 'The selected check, 24 px, before the word, in the word’s ink', 'token': 'oa.size.icon.medium'},
            {'label': 'Word', 'value': 'Bold, 700; 600 when off'},
            {'label': 'Edge', 'value': f'2 px in the strong border color, {F["edge_n"]} to 1 on Newsprint; 1 px when off',
             'token': 'oa.border.width.rule'},
            {'label': 'Fill', 'value': 'The surface’s own ground, on and off'},
            {'label': 'Markup', 'value': '<code>aria-pressed="true"</code> on a toggle; a native radio or check box, <code>:checked</code>'},
            {'label': 'Current place', 'value': 'A link: bold words, with a 2 px underline in a masthead; a rail or list: the selected band, its 4 px bar and bold words',
             'token': 'oa.color.state.selected.bar.onNewsprint'},
        ],
        'related': ['11', '18'],
        'builders': [
            'Tie the look to the state the control already holds, <code>[aria-pressed="true"]</code> or '
            '<code>:checked</code>, so the drawing always agrees with what a screen reader hears.'],
    })

    rules.append({
        'id': '17.11',
        'title': 'Keep an unavailable action in reach and say what makes it available.',
        'rule': [
            'An action that cannot run yet stays in its place with a dashed edge, readable words and a reason line under '
            'it that names the step that makes it available, such as “Choose a size to download.” It keeps focus, so a '
            'keyboard reader reaches it, and its accessible description, the line a screen reader reads after its name, carries the reason. Its words take the disabled '
            f'text token, {F["dis_n"]} to 1 on Newsprint and {F["dis_c"]} on Charcoal, and nothing fades.',
            'Form fields stay editable. A Send button that cannot run yet keeps focus and says why under it.'],
        'tokens': ['oa.color.state.disabled.text.onNewsprint', 'oa.color.state.disabled.edge.onNewsprint',
                   'oa.color.state.disabled.text.onCharcoal'],
        'why': {'text': [
            f'A control faded with opacity falls below the contrast its words need: Charcoal at 40 percent measures '
            f'{F["faded_n"]} to 1 on Newsprint and {F["faded_w"]} on White. A button with the disabled attribute also '
            'leaves the keyboard’s path, so the reader who most needs the reason never meets it. WCAG 2.2 success '
            'criterion 1.4.3 exempts an inactive control’s text from its minimum, and we hold that text to the same 4.5 to 1 as '
            'any other words.'],
            'basis': 'WCAG 2.2 SC 1.4.3; design judgment'},
        'correct': {'specimen': 's-17-11-correct', 'caption':
                    'A download button before and after a reader chooses a size, on Newsprint and on Charcoal. Before, its '
                    'reason sits under it, and the button keeps its place in the Tab order.'},
        'failure': {'specimen': 's-17-11-failure', 'caption':
                    f'<strong>Fails Rule 17.11.</strong> The button is faded to 40 percent, {F["faded_n"]} to 1, and '
                    'nothing says why it will not run.'},
        'specs': [
            {'label': 'Edge', 'value': 'Dashed, 1 px', 'token': 'oa.color.state.disabled.edge.onNewsprint'},
            {'label': 'Words', 'value': f'{F["dis_n"]} to 1 on Newsprint; {F["dis_c"]} on Charcoal', 'token': 'oa.color.state.disabled.text.onNewsprint'},
            {'label': 'Reason line', 'value': 'Under the control in secondary words, and in its accessible description',
             'token': 'oa.color.text.secondary.onNewsprint'},
            {'label': 'Markup', 'value': '<code>aria-disabled="true"</code> with <code>aria-describedby</code> to the reason; '
                                         'never the <code>disabled</code> attribute'},
            {'label': 'Form fields', 'value': 'Always editable'},
            {'label': 'Opacity', 'value': 'None'},
        ],
        'related': ['18', '26'],
        'builders': [
            'Stop the action in the click handler while <code>aria-disabled="true"</code> holds, and leave the button '
            'in the Tab order. Write the reason as the step the reader takes next.'],
    })

    rules.append({
        'id': '17.12',
        'title': 'Say what is missing and what to do next when a region is empty.',
        'rule': [
            'A list, table, search or tracker with nothing to show draws a dashed region in place of its rows, and its '
            'words say what is missing and the step that would fill it. A search writes both into its status line with '
            f'the count, so a screen reader hears them together: “0 of {N_LIB} symbols. No symbol matches. Clear the search or '
            'the filters to see more.”',
            'An empty region names no fault, since nothing failed. When the data fails to arrive, the region shows the '
            'error state instead (Rule 11.15).'],
        'tokens': ['oa.color.state.empty.text.onNewsprint', 'oa.color.state.empty.edge.onNewsprint'],
        'why': {'text': [
            'WCAG 2.2 success criterion 4.1.3 Status Messages asks that a result such as a count reach a screen reader '
            'without moving focus, and a count of 0 alone leaves a reader with nothing to try next. The dashed edge keeps the '
            'region at its size, so the page holds still when results return.'],
            'basis': 'WCAG 2.2 SC 4.1.3; design judgment'},
        'correct': {'specimen': 's-17-12-correct', 'caption':
                    f'A symbol search with no match, on Newsprint and on Charcoal. The dashed edge measures '
                    f'{F["empty_n"]} to 1 on Newsprint and {F["empty_c"]} on Charcoal, and the words in it are the status line.'},
        'failure': {'specimen': 's-17-12-failure', 'caption':
                    '<strong>Fails Rule 17.12.</strong> “No results.” says nothing about what to try, and the blank space '
                    'under it looks like a page still loading.'},
        'specs': [
            {'label': 'Region', 'value': f'Dashed, 1 px; {F["empty_n"]} to 1 on Newsprint', 'token': 'oa.color.state.empty.edge.onNewsprint'},
            {'label': 'Words', 'value': 'What is missing, then the step that fills it', 'token': 'oa.color.state.empty.text.onNewsprint'},
            {'label': 'Status line', 'value': 'The count and the advice in one polite line'},
            {'label': 'On Charcoal', 'value': f'Dim Newsprint edge and words, {F["empty_c"]} to 1', 'token': 'oa.color.state.empty.text.onCharcoal'},
            {'label': 'Size', 'value': 'The region keeps the height its rows would take'},
        ],
        'related': ['11', '18'],
        'builders': [
            'Write the count and the advice into the same status line in one update, so a screen reader reads them as '
            'one message.'],
    })

    extras = []
    for sid, meta in id_extras:
        extras.append({'after_rule': '17.6', 'specimen': sid,
                       'label': meta.get('label') or ('The lever landing' if 'lever' in sid else 'The hinge'),
                       'caption': meta.get('caption') or meta.get('notes') or ''})

    ch = {
        'number': CH,
        'anchor': 'motion-and-states',
        'title': 'Motion and states',
        'part': 'Behavior',
        'opener': 's-17-opener',
        'instruction': 'Keep motion under the reader’s control, and give every state visible text.',
        'intro': [
            'Motion here means a mark that moves on screen to show a change, such as a bill reaching its next step or a '
            'link forming between a cause and its effect. A state is how a control or a region looks while something '
            'about it holds, from a focus ring to an error. This chapter sets how a motion runs and how each state looks, and '
            'chapter 18 says where each component uses them.',
            'A reader starts every motion, and a reader whose device asks for less motion sees the last frame at once. '
            'Every state shows words or a shape as well as a color, on Newsprint and on Charcoal, so it reads in gray '
            'print, in a dark theme and to a reader who sees no color.'],
        'groups': [
            {'before_rule': '17.1', 'number': 1, 'title': 'Motion under the reader’s control',
             'line': 'A motion explains a change, keeps to nine timing tokens and starts only when a reader asks.'},
            {'before_rule': '17.5', 'number': 2, 'title': 'Three behaviors, and the identity’s own',
             'line': 'Slide, draw and land build every motion, and the hinge and the lever keep motions of their own.'},
            {'before_rule': '17.7', 'number': 3, 'title': 'States',
             'line': 'Each state shows words or a shape as well as a color, on Newsprint and on Charcoal.'},
        ],
        'rules': rules,
        'extras': extras,
        'related_chapters': [
            {'chapter': '05', 'reason': 'State colors, kept apart from identity and chart colors.'},
            {'chapter': '11', 'reason': 'The error, success and warning marks, and the tracker these motions move.'},
            {'chapter': '04', 'reason': 'The hinge, whose motion Rule 17.6 frames.'},
            {'chapter': '08', 'reason': 'The lockmark and its lever.'},
            {'chapter': '18', 'reason': 'Where each component uses these states, with code to copy.'},
            {'chapter': '19', 'reason': 'Checking motion and states against WCAG 2.2 AA.'},
            {'chapter': '26', 'reason': 'The motion and state tokens, and how to choose one.'},
        ],
        'sources': [
            'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, '
            'success criteria 1.4.1, 1.4.3, 1.4.11, 2.2.2, 2.4.7, 2.4.11 and 4.1.3, retrieved November 10, 2026. The '
            'criteria behind Rules 17.3 and 17.7 to 17.12.',
            'Source: W3C, “Media Queries Level 5”, W3C Working Draft, February 19, 2026, the prefers-reduced-motion '
            'feature, retrieved November 10, 2026. Its words for the reduce value, behind Rules 17.1 and 17.4.',
            'Source: MDN Web Docs, browser compatibility data, @mdn/browser-compat-data version 8.1.8, built November 2, '
            '2026, retrieved November 10, 2026. The first version of each browser with full support for '
            'prefers-reduced-motion, behind Rule 17.4.',
            'Source: Oath & Action’s systems atlas, Who Do They Answer To?, Loop R1, “Wealth and political influence '
            'reinforce each other”, graded plausible, snapshot of October 15, 2026. Its first link, graded well '
            'supported, and its sentence, behind the players in Rules 17.3 and 17.4.',
        ],
    }
    return ch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build in memory and report; write nothing')
    a = ap.parse_args()
    ch = build_chapter()
    B.check_chapter(ch)
    used = set()
    for rr in ch['rules']:
        for k in ('correct', 'failure'):
            used.add(rr[k]['specimen'])
    for x in ch['extras']:
        used.add(x['specimen'])
    if ch.get('opener'):
        used.add(ch['opener'])
    ours = set(ctx.specs)
    id_used = {s for s in used if re.match(r'^s-17-(hinge|lever)-', s)}
    missing = used - ours - id_used
    unused = ours - used
    if missing or unused:
        raise SystemExit(f'specimens missing {sorted(missing)} unused {sorted(unused)}')
    total = sum(len(s['html'].encode()) for s in ctx.specs.values())
    print(f'chapter 17: {len(ch["rules"])} rules, {len(ctx.specs)} specimens of ours ({total / 1000:.1f} KB), '
          f'identity specimens placed: {sorted(id_used) or "none (pending markers)"}')
    if a.check:
        return
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    # remove our own stale fragments (a pending marker that left, a renamed specimen); never another owner's
    for p in OUT_SP.glob('s-17-*.html'):
        if p.stem not in ours and not re.match(r'^s-17-(hinge|lever)-', p.stem):
            p.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    MANIFEST.write_text(json.dumps(dict(sorted((k, v['meta']) for k, v in ctx.specs.items())), indent=1,
                                   ensure_ascii=False) + '\n')
    FIG_OUT.write_text(json.dumps({
        'about': 'Every figure chapter 17 prints, with the method that produced it. Contrast is WCAG 2.x relative '
                 'luminance on the token hex values in tokens.json; motion values are read from tokens.json.',
        'built': '2026-11-11',
        'token_set_version': (T.data.get('$extensions', {}).get('org.oathandaction', {}).get('tokenSetVersion')
                              or T.data.get('$extensions', {}).get('org.oathandaction', {}).get('version')),
        'figures': dict(sorted(ctx.figures.items())),
        'tokens_cited': sorted(ctx.T.used),
    }, indent=1, ensure_ascii=False) + '\n')
    print(f'wrote {OUT_CH.relative_to(ROOT)}, {len(ctx.specs)} specimens, {MANIFEST.relative_to(ROOT)}, {FIG_OUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
