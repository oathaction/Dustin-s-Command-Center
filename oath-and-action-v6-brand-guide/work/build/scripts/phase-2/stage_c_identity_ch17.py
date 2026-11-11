"""Chapter 17, Rule 17.6: the hinge and the lever, the identity's own motions (stage C round 1, November 11, 2026).

Under work/handoffs/phase-2/20261111_Stage-C-Round-1-Brief.md and the main session's round 1 task for the identity
designer. Chapter 17 belongs to the systems designer (stage_c_ch17_build.py), which reads these specimens from
manifest-identity.json: s-17-hinge-correct fills Rule 17.6's correct plate, s-17-hinge-failure its failure plate, and
s-17-lever-correct follows the rule as an extra plate, each with the caption (and the extra's label) this file writes.

The motions (timing from tokens.json, read at build time and again by the script at the moment of a press):
  hinge   OATH and ACTION slide toward each other over the slow duration with the standard easing; the gap holds;
          ampersand B lands from 112 percent to its true size over the standard duration with the enter easing, so
          it comes to rest at the hinge duration, 680 ms (B starts at hinge minus standard).
  lever   The six links draw from the top left over the standard duration with the enter easing; one stagger later the
          eight nodes land together; the lever lands last and comes to rest at the lever duration, 560 ms (it starts at
          lever minus standard). Built from Rule 17.5's draw and land; a land starts at 112 percent (chapter 17's
          figure, our fifth edition's 1.4 over 1.25).

Each player draws three layers in one place: the moving layer, which is the master's own elements inlined (the
wordmark's one letter path split by position into OATH and ACTION, every other element as the file draws it) with
data-part names the script animates; and the end layer, the master placed by reference, which the guide build inlines
unchanged. Each player rests on the end layer, the master itself (stage C round 2, CD-M1, call 5: data-frame="end"
and data-oa-rest="master" on load). Play steps to the first frame and runs the moving layer; at its end the player
shows the end layer again, so the last frame is the master. Reset returns to the master, and at rest it is unavailable
with the line "The mark is at rest on its master. Reset works once you press Play." (D2-1666, the editor's I1). Under
reduced motion every duration token is 0 ms and Play shows the
end layer at once (Rule 17.4). Nothing moves on load and nothing loops (Rule 17.3). A state or mechanism player in
chapter 17 still rests on its first frame. The player follows the engineer's
contract (data-oa-motion on the root, data-oa-play and data-oa-pause on one button, data-oa-reset) and chapter 17's
player in its parts and words: one Play and Pause button, Reset, Slow motion, a status line and a still view.

No master is written. Every drawing is placed from its file.
"""
import json
import re
from pathlib import Path

import stage_a_identity_lib as LIB
from stage_a_identity_lib import E, ROOT, ID_DIR, WM, LOCK, mark, tv, ink, dnp, raster_png
from stage_a_identity_s03 import rec as _rec

S = []
TOKENS = json.loads((ROOT / "work/build/tokens/tokens.json").read_text())
CH17_FIGS = ROOT / "work/handoffs/phase-2/20261111_Stage-C-Round-1-Ch17-Figures.json"


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "17")
    return _rec(*a, **k)


def ms(name):
    return int(TOKENS["oa"]["motion"]["duration"][name]["$value"]["value"])


FAST, STD, SLOW, STAG, HINGE, LEVER = (ms(n) for n in ("fast", "standard", "slow", "stagger", "hinge", "lever"))


def _land_from():
    """Rule 17.5's land starts at this share of the mark's size: chapter 17's figure, read from its figures file."""
    try:
        v = json.loads(CH17_FIGS.read_text())["figures"]["land from"]["value"]
        return int(re.match(r"(\d+)", v).group(1)) / 100
    except Exception:
        return 1.12


LAND_FROM = _land_from()
NB = " "


def msw(n):
    return f"{n:,}{NB}ms"


def var(name):
    return f"--oa-motion-duration-{name}"


def ease(name):
    return f"--oa-motion-easing-{name}"


# The two timelines, each ending on its own token (asserted)
HINGE_B_AT = HINGE - STD            # 480: B starts so that it comes to rest at the hinge duration
LEVER_NODES_AT = STD + STAG         # 240
LEVER_AT = LEVER - STD              # 360
assert SLOW < HINGE_B_AT and HINGE_B_AT + STD == HINGE, "the hinge's slide must end before B lands, and B rest at 680 ms"
assert LEVER_NODES_AT < LEVER_AT and LEVER_NODES_AT + STD <= LEVER and LEVER_AT + STD == LEVER, "the lever must land last, at 560 ms"


# ------------------------------------------------------------------------------------------------ masters, split
def _inline(rel, h, surface, mode="color"):
    """A master inlined as the guide build would place it: hooks on the root, title out, aria-hidden."""
    LIB.INLINE_ALL[0] = True
    try:
        return mark(rel, h=h, surface=surface, mode=mode, decorative=True)
    finally:
        LIB.INLINE_ALL[0] = False


NUM = re.compile(r"-?\d*\.?\d+(?:e-?\d+)?")


def _subpath_xrange(sub):
    """The x range of one absolute subpath (M, L, H, V, Q, C, Z only), from its points; control points included."""
    xs = []
    for cmd, args in re.findall(r"([MLHVQCZ])([^MLHVQCZ]*)", sub):
        nums = [float(n) for n in NUM.findall(args)]
        if cmd == "H":
            xs += nums
        elif cmd in "MLQC":
            xs += nums[0::2]
    return min(xs), max(xs)


def _split_wordmark(svg):
    """The wordmark's letter path split into OATH and ACTION by each subpath's place left or right of B. The subpaths
    keep their order and their bytes; only the path element they sit in changes."""
    letters = re.search(r'<path fill="currentColor" d="([^"]+)"/>', svg)
    amp = re.search(r'<path fill="(var\(--amp[^"]*\))" d="([^"]+)"/>', svg)
    assert letters and amp, "the wordmark master is not the file this step was written for"
    bx0, bx1 = _subpath_xrange(amp.group(2))
    subs = re.findall(r"M[^M]*", letters.group(1))
    assert "".join(subs) == letters.group(1)
    left, right = [], []
    for sp in subs:
        x0, x1 = _subpath_xrange(sp)
        if x1 <= bx0:
            left.append(sp)
        elif x0 >= bx1:
            right.append(sp)
        else:
            raise AssertionError("a letter's subpath overlaps B")
    assert len(left) == 6 and len(right) == 8, (len(left), len(right))      # O A T H: 6 subpaths; A C T I O N: 8
    return letters, amp, "".join(left), "".join(right)


def hinge_layer(rel, h, surface, sfx, still=None):
    """The wordmark master inlined with its parts named for the script: oath, action and amp, suffixed by size. still:
    a frame drawn as a picture for the still view (its parts take inline styles and no data-part)."""
    svg = _inline(rel, h, surface)
    letters, amp, oath, action = _split_wordmark(svg)
    attr = "data-still-part" if still is not None else "data-part"
    st = still or {}

    def style(part):
        return f' style="{st[part]}"' if part in st else ""
    new = (f'<path fill="currentColor" {attr}="oath-{sfx}"{style("oath")} d="{oath}"/>'
           f'<path fill="currentColor" {attr}="action-{sfx}"{style("action")} d="{action}"/>'
           f'<path fill="{amp.group(1)}" {attr}="amp-{sfx}"{style("amp")} d="{amp.group(2)}"/>')
    out = svg.replace(letters.group(0) + amp.group(0), new, 1)
    assert out != svg, "the wordmark's two paths are not where this step expects them"
    return out


def lever_layer(rel, h, surface, sfx, still=None):
    """A lockmark master inlined with its parts named: hlinks and vlinks (each link by its direction), nodes and lever.
    Works on the 48 px master (rects and paths) and the display master (lines and circles)."""
    svg = _inline(rel, h, surface)
    attr = "data-still-part" if still is not None else "data-part"
    st = still or {}

    def tag(part):
        return f' {attr}="{part}-{sfx}"' + (f' style="{st[part]}"' if part in st else "")

    def link(m):
        el = m.group(0)
        if el.startswith("<rect"):
            w, hh = (float(re.search(rf'\s{k}="([\d.]+)"', el).group(1)) for k in ("width", "height"))
            part = "hlinks" if w > hh else "vlinks"
        else:
            x1, x2 = (re.search(rf'\s{k}="([\d.]+)"', el).group(1) for k in ("x1", "x2"))
            part = "vlinks" if x1 == x2 else "hlinks"
        return el.replace(" ", tag(part) + " ", 1)
    svg = re.sub(r"<rect [^>]*/>|<line [^>]*/>", link, svg)
    # nodes: the 48 px master's eight paths in the currentColor group; the display master's circles of radius 3.8
    svg = re.sub(r'(<g fill="currentColor">)(.*?)(</g>)',
                 lambda m: m.group(1) + m.group(2).replace("<path ", "<path" + tag("nodes") + " ") + m.group(3), svg, count=1, flags=re.S)
    svg = re.sub(r'<circle ([^>]*r="3\.8"[^>]*)/>', lambda m: "<circle" + tag("nodes") + " " + m.group(1) + "/>", svg)
    # the lever: the 48 px master's red path, or the display master's circle of radius 4.75
    svg = re.sub(r'<path fill="var\(--lever', "<path" + tag("lever") + ' fill="var(--lever', svg, count=1)
    svg = re.sub(r'<circle ([^>]*r="4\.75"[^>]*)/>', lambda m: "<circle" + tag("lever") + " " + m.group(1) + "/>", svg)
    n = {p: svg.count(f'{attr}="{p}-{sfx}"') for p in ("hlinks", "vlinks", "nodes", "lever")}
    assert n == {"hlinks": 3, "vlinks": 3, "nodes": 8, "lever": 1}, n
    return svg


# ------------------------------------------------------------------------------------------------ sizes
HINGE_SIZES = [  # suffix, master, height px, slide each way in px (whole pixels), the label
    ("24", WM[24], 24, 12, "24 px master at 24 px"),
    ("64", WM["display"], 64, 32, "Display master at 64 px tall"),
]
LEVER_SIZES = [
    ("48", LOCK[48], 48, "48 px master at 48 px"),
    ("120", LOCK["display"], 120, "Display master at 120 px"),
]


def _vb(rel):
    s = (ID_DIR / rel).read_text()
    return [float(v) for v in re.search(r'viewBox="([^"]+)"', s).group(1).split()]


def _units(rel, h, px):
    """px on screen as the master's user units at a height h (an SVG element's CSS transform reads user units)."""
    return px * _vb(rel)[3] / h


def hinge_frames():
    """The motion as tracks for the script and the first frame as CSS, from one list."""
    tracks, start_css = [], []
    for sfx, rel, h, d, _ in HINGE_SIZES:
        u = round(_units(rel, h, d), 4)
        tracks += [
            {"part": f"oath-{sfx}", "frames": [{"transform": f"translateX({-u:g}px)"}, {"transform": "translateX(0px)"}],
             "dur": var("slow"), "ease": ease("standard"), "at": []},
            {"part": f"action-{sfx}", "frames": [{"transform": f"translateX({u:g}px)"}, {"transform": "translateX(0px)"}],
             "dur": var("slow"), "ease": ease("standard"), "at": []},
            {"part": f"amp-{sfx}", "frames": [{"transform": f"scale({LAND_FROM:g})", "visibility": "visible"},
                                               {"transform": "scale(1)", "visibility": "visible"}],
             "dur": var("standard"), "ease": ease("enter"), "at": [["+", var("hinge")], ["-", var("standard")]], "fill": "forwards"},
        ]
        start_css += [f'.oai-mv[data-frame="start"] [data-part="oath-{sfx}"]{{transform:translateX({-u:g}px)}}',
                      f'.oai-mv[data-frame="start"] [data-part="action-{sfx}"]{{transform:translateX({u:g}px)}}',
                      f'.oai-mv:not([data-frame="end"]) [data-part="amp-{sfx}"]{{visibility:hidden}}']
    return tracks, "".join(start_css)


def lever_frames():
    tracks, start_css = [], []
    for sfx, rel, h, _ in LEVER_SIZES:
        tracks += [
            {"part": f"hlinks-{sfx}", "frames": [{"transform": "scaleX(0)"}, {"transform": "scaleX(1)"}],
             "dur": var("standard"), "ease": ease("enter"), "at": []},
            {"part": f"vlinks-{sfx}", "frames": [{"transform": "scaleY(0)"}, {"transform": "scaleY(1)"}],
             "dur": var("standard"), "ease": ease("enter"), "at": []},
            {"part": f"nodes-{sfx}", "frames": [{"transform": f"scale({LAND_FROM:g})", "visibility": "visible"},
                                                 {"transform": "scale(1)", "visibility": "visible"}],
             "dur": var("standard"), "ease": ease("enter"), "at": [["+", var("standard")], ["+", var("stagger")]], "fill": "forwards"},
            {"part": f"lever-{sfx}", "frames": [{"transform": f"scale({LAND_FROM:g})", "visibility": "visible"},
                                                 {"transform": "scale(1)", "visibility": "visible"}],
             "dur": var("standard"), "ease": ease("enter"), "at": [["+", var("lever")], ["-", var("standard")]], "fill": "forwards"},
        ]
        start_css += [f'.oai-mv[data-frame="start"] [data-part="hlinks-{sfx}"]{{transform:scaleX(0)}}',
                      f'.oai-mv[data-frame="start"] [data-part="vlinks-{sfx}"]{{transform:scaleY(0)}}',
                      f'.oai-mv:not([data-frame="end"]) [data-part="nodes-{sfx}"],'
                      f'.oai-mv:not([data-frame="end"]) [data-part="lever-{sfx}"]{{visibility:hidden}}']
    return tracks, "".join(start_css)


# The hinge's display master shows where its ground's content box is at least BIG_REM wide. The first frame's slides
# run into the ground's padding (HINGE_CSS), so the box needs only the master's own width (round 2: was 41rem, which
# held the slides as well).
_WM_W64 = 64 * _vb(WM["display"])[2] / _vb(WM["display"])[3]
BIG_REM = "37"
assert _WM_W64 <= int(BIG_REM) * 16, (_WM_W64, BIG_REM)


# ------------------------------------------------------------------------------------------------ the player
def tyv(name, size=None):
    k = f"--oa-type-{name}"
    out = f"font:var({k});letter-spacing:var({k}-letter-spacing);text-transform:var({k}-text-transform)"
    return out + (f";font-size:{size}" if size else "")


def uicon(name):
    return (f'<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false" data-icon="U-{name}" '
            f'data-icon-family="utility"><use href="#oa-sym-u-{name}-24px"/></svg>')


PLAYER_CSS = (
    ".oai-mv{display:grid;gap:12px}"
    ".oai-mv p{margin:0}"
    ".oai-mv-ti{" + tyv("h4", "1.25rem") + ";text-wrap:balance}"
    ".oai-mv-k{" + tyv("label") + ";color:var(--oa-color-text-secondary)}"
    ".oai-mv-grounds{display:grid;gap:12px}"
    ".oai-mv-ground{container-type:inline-size;padding:24px}"
    ".oai-mv-ground.oai-s-newsprint{border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-newsprint)}"
    ".oai-mv-gl{" + tyv("caption") + ";margin:0 0 12px}"
    ".oai-s-newsprint .oai-mv-gl,.oai-s-newsprint .oai-mv-tag{color:var(--oa-color-text-secondary-on-newsprint)}"
    ".oai-s-charcoal .oai-mv-gl,.oai-s-charcoal .oai-mv-tag{color:var(--oa-color-text-secondary-on-charcoal)}"
    ".oai-mv-row{display:flex;flex-wrap:wrap;gap:24px 40px;align-items:flex-end}"
    ".oai-mv-cell{display:grid;gap:8px;justify-items:start}"
    ".oai-mv-tag{" + tyv("caption") + "}"
    ".oai-mv-box{display:block;position:relative;line-height:0;overflow:visible}"
    ".oai-mv-box svg{display:block;overflow:visible}"
    ".oai-mv-big{display:none}"
    "@container (min-width:" + BIG_REM + "rem){.oai-mv-big{display:grid}}"
    # layers: the moving master until the end, then the master itself
    '.oai-mv [data-layer="end"]{display:none}'
    '.oai-mv[data-frame="end"] [data-layer="end"]{display:block}'
    '.oai-mv[data-frame="end"] [data-layer="run"]{display:none}'
    "[data-part],[data-still-part]{transform-box:fill-box;transform-origin:center}"
    '[data-part^="hlinks"],[data-still-part^="hlinks"]{transform-origin:0 50%}'
    '[data-part^="vlinks"],[data-still-part^="vlinks"]{transform-origin:50% 0}'
    ".oai-mv-out{min-height:3em;" + tyv("body-small") + "}"
    ".oai-mv-cl{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,9.5rem),1fr));gap:8px;max-width:22rem}"
    ".oai-mv-b{display:inline-flex;align-items:center;gap:8px;min-height:var(--oa-size-target-touch);margin:0;"
    "padding:0 14px 0 10px;border:var(--oa-border-width-hairline) solid var(--oa-color-border-strong);border-radius:0;"
    "background:var(--oa-color-surface);color:var(--oa-color-text-primary);" + tyv("ui") + ";text-align:left;cursor:pointer}"
    ".oai-mv-b svg{flex:none;display:block}.oai-mv-b svg[hidden]{display:none}"
    ".oai-mv-b:hover{border-width:var(--oa-border-width-rule);padding:0 13px 0 9px}"
    '.oai-mv-b[aria-disabled="true"]{color:var(--oa-component-button-disabled-label);border-style:dashed;'
    "border-color:var(--oa-component-button-disabled-edge);cursor:not-allowed}"
    '.oai-mv-b[aria-disabled="true"]:hover{border-width:var(--oa-border-width-hairline);padding:0 14px 0 10px}'
    ".oai-mv-sl{display:flex;align-items:center;gap:10px;min-height:var(--oa-size-target-touch);" + tyv("ui") + ";cursor:pointer;"
    "width:max-content;max-width:100%}"
    ".oai-mv-sl input{flex:none;width:24px;height:24px;margin:0}"
    ".oai-mv-sl[data-off]{color:var(--oa-color-state-disabled-text);cursor:not-allowed}"
    ".oai-mv-why{" + tyv("caption") + ";color:var(--oa-color-text-secondary)}"
    ".oai-mv-why:empty{display:none}"
    ".oai-mv-sv{display:grid;gap:10px;padding-top:12px;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline)}"
    ".oai-mv-fr{list-style:none;margin:0;padding:0;display:grid;gap:16px 24px;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr))}"
    ".oai-mv-fr li{display:grid;gap:8px;align-content:start;justify-items:start}"
    ".oai-mv-fh{" + tyv("caption") + "}.oai-mv-fh b{font-weight:700}"
    ".oai-mv-fw{" + tyv("caption") + "}"
    ".oai-mv-empty{display:block;border:var(--oa-border-width-hairline) dashed var(--oa-color-state-empty-edge)}"
    ".oai-mv-tl{margin:0;padding-left:1.25em;" + tyv("caption") + "}"
    ".oai-mv-tl li+li{margin-top:4px}"
)

# The player's script, one copy per specimen; it wires every player inside its own specimen. Same contract and words as
# chapter 17's player (stage_c_ch17_build.PLAYER_JS), with two additions: a track's start may subtract a token (a mark
# that comes to rest at its motion's own duration), and a part names every element that carries it.
PLAYER_JS = r"""(function(){var S=document.currentScript.closest("[data-specimen]");if(!S)return;
var RM=window.matchMedia?window.matchMedia("(prefers-reduced-motion: reduce)"):null;
function tok(el,n){var v=getComputedStyle(el).getPropertyValue(n).trim(),x=parseFloat(v);if(isNaN(x))return 0;return /ms$/.test(v)?x:(/s$/.test(v)?x*1000:x);}
function ez(el,n){return getComputedStyle(el).getPropertyValue(n).trim()||"linear";}
S.querySelectorAll("[data-oa-motion]").forEach(function(P){
var M=JSON.parse(P.querySelector("script[data-motion]").textContent),B=P.querySelector("[data-oa-play]"),R=P.querySelector("[data-oa-reset]"),
L=P.querySelector("input[data-slow]"),W=P.querySelector("[data-why]"),O=P.querySelector("[data-out]"),I=B.querySelectorAll("svg"),
Y=B.querySelector("[data-word]"),A=[],run=0,st="rest";
function at(t){return (t.at||[]).reduce(function(s,a){return s+(a[0]==="-"?-1:1)*tok(P,a[1]);},0);}
function total(){return M.tracks.reduce(function(s,t){return Math.max(s,at(t)+tok(P,t.dur));},0);}
function off(el,y){if(!el)return;var lab=el.closest("label");if(y){el.setAttribute("aria-disabled","true");el.setAttribute("aria-describedby",W.id);if(lab)lab.setAttribute("data-off","");}
else{el.removeAttribute("aria-disabled");el.removeAttribute("aria-describedby");if(lab)lab.removeAttribute("data-off");}}
function show(){var z=total()===0,why=[];I[0].toggleAttribute("hidden",st==="running");I[1].toggleAttribute("hidden",st!=="running");
Y.textContent=st==="running"?"Pause":(st==="end"?"Play again":"Play");var still=st==="rest"||st==="end";off(R,still);if(still)why.push(M.why.rest);
if(L){off(L,z);if(z)why.push(M.why.slowDevice);}W.textContent=why.join(" ");}
function frame(f){P.setAttribute("data-frame",f);}
function stop(){run++;A.forEach(function(a){a.cancel();});A=[];}
function end(){stop();frame("end");st="end";O.textContent=M.words.end;show();}
function reset(){stop();frame("end");st="rest";O.textContent=M.words.rest;show();}
function play(){if(st==="paused"){A.forEach(function(a){a.play();});st="running";O.textContent=M.words.run;show();return;}
stop();frame("start");if(total()===0){end();return;}
frame("run");st="running";var my=++run,rate=L&&L.checked?0.1:1;A=[];
M.tracks.forEach(function(t){P.querySelectorAll('[data-part="'+t.part+'"]').forEach(function(el){
var a=el.animate(t.frames,{duration:tok(P,t.dur),easing:ez(P,t.ease),delay:at(t),fill:t.fill||"both"});a.playbackRate=rate;A.push(a);});});
O.textContent=M.words.run;Promise.all(A.map(function(a){return a.finished;})).then(function(){if(my===run)end();},function(){});show();}
function pause(){A.forEach(function(a){a.pause();});st="paused";O.textContent=M.words.pause;show();}
B.addEventListener("click",function(){if(st==="running")pause();else play();});
R.addEventListener("click",function(){if(R.getAttribute("aria-disabled")!=="true")reset();});
if(L){L.addEventListener("click",function(e){if(L.getAttribute("aria-disabled")==="true")e.preventDefault();});
L.addEventListener("change",function(){var k=L.checked?0.1:1;A.forEach(function(a){a.updatePlaybackRate(k);});});}
if(RM&&RM.addEventListener)RM.addEventListener("change",function(){if(total()===0&&(st==="running"||st==="paused"))end();else show();});
show();});})();"""

WHY = {"rest": "The mark is at rest on its master. Reset works once you press Play.",
       "slowDevice": "Your device asks for reduced motion, so Play shows the last frame at once and Slow motion has nothing to slow."}


def player(pid, *, title, kicker, grounds, words, frames, timeline, tracks, group, start_css):
    wid = f"{pid}-why"
    icons = uicon("play") + uicon("pause").replace("<svg ", "<svg hidden ", 1)
    ctl = (f'<div class="oai-mv-cl" role="group" aria-label="{E(group)}">'
           f'<button type="button" class="oai-mv-b" data-oa-play="" data-oa-pause="">{icons}<span data-word="">Play</span></button>'
           f'<button type="button" class="oai-mv-b" data-oa-reset="" aria-disabled="true" aria-describedby="{wid}">'
           f'{uicon("reset")}<span>Reset</span></button></div>')
    sl = '<label class="oai-mv-sl"><input type="checkbox" data-slow=""><span>Slow motion, one tenth speed</span></label>'
    whyp = f'<p class="oai-mv-why" id="{wid}" data-why="">{E(WHY["rest"])}</p>'
    out = f'<p class="oai-mv-out" role="status" data-out="">{E(words["rest"])}</p>'
    fl = "".join(f'<li><p class="oai-mv-fh"><b>{E(t)}</b>, {msw(tm)}</p>{svg}<p class="oai-mv-fw">{E(w)}</p></li>' for t, tm, svg, w in frames)
    tl = "".join(f"<li>{E(x)}</li>" for x in timeline)
    sv = (f'<div class="oai-mv-sv"><p class="oai-mv-k">Still view</p><ol class="oai-mv-fr">{fl}</ol>'
          f'<ol class="oai-mv-tl">{tl}</ol></div>')
    data = json.dumps({"tracks": tracks, "words": words, "why": WHY}, ensure_ascii=False)
    head = f'<div><p class="oai-mv-k">{E(kicker)}</p><p class="oai-mv-ti">{E(title)}</p></div>'
    return (f'<div class="oai-mv" data-oa-motion="" data-oa-rest="master" data-frame="end">{head}'
            f'<div class="oai-mv-grounds">{grounds}</div>{out}{ctl}{sl}{whyp}{sv}'
            f'<script type="application/json" data-motion="">{data}</script></div>')


def ground(surface, cells):
    name = {"newsprint": "On Newsprint", "charcoal": "On Charcoal"}[surface]
    return (f'<div class="oai-mv-ground oai-s-{surface}"><p class="oai-mv-gl">{name}</p>'
            f'<div class="oai-mv-row">{cells}</div></div>')


def cell(run_svg, end_mark, label, big=False):
    """One size of a mark: the moving master and the master itself in one place, with the master's left edge on its
    label's (CD-S4). A first frame that slides outward runs into the ground's padding (HINGE_CSS)."""
    return (f'<div class="oai-mv-cell{" oai-mv-big" if big else ""}"><div class="oai-mv-box">'
            f'<div data-layer="run">{run_svg}</div><div data-layer="end">{end_mark}</div></div>'
            f'<span class="oai-mv-tag">{E(label)}</span></div>')


# ------------------------------------------------------------------------------------------------ 17.6: the hinge
HINGE_WORDS = {"rest": "At rest: the wordmark, OATH & ACTION, as its master draws it.",
               "start": "First frame: OATH and ACTION stand apart, with no ampersand between them.",
               "end": "Last frame: the wordmark, OATH & ACTION, as its master draws it.",
               "run": "Playing.", "pause": "Paused."}
# The master rests on its label's left edge (CD-S4), so the first frame's slide runs outward into the ground's padding:
# 40 px (oa.space.500) each side holds the largest slide with 8 px to spare. The display master's cell starts its own
# row, so no slide meets the next cell's.
HINGE_PAD = 40
assert max(d for _, _, _, d, _ in HINGE_SIZES) + 8 <= HINGE_PAD
HINGE_CSS = (".oai-mv-ground{padding:var(--oa-space-300) var(--oa-space-500)}"
             ".oai-mv-big{flex-basis:100%}")


def _hinge_still(sfx, rel, h, d, state):
    u = round(_units(rel, h, d), 4)
    st = {"first": {"oath": f"transform:translateX({-u:g}px)", "action": f"transform:translateX({u:g}px)", "amp": "visibility:hidden"},
          "middle": {"amp": "visibility:hidden"}}[state]
    return f'<div class="oai-mv-box" style="padding:0 {d}px">{hinge_layer(rel, h, "newsprint", sfx, still=st)}</div>'


@spec
def s_17_hinge_correct():
    tracks, css = hinge_frames()
    cells = {}
    for s in ("newsprint", "charcoal"):
        cells[s] = "".join(cell(hinge_layer(rel, h, s, sfx), mark(rel, h=h, surface=s, decorative=True), lab, big=sfx != "24")
                           for sfx, rel, h, d, lab in HINGE_SIZES)
    grounds = ground("newsprint", cells["newsprint"]) + ground("charcoal", cells["charcoal"])
    sfx, rel, h, d, _ = HINGE_SIZES[0]
    frames = [("First frame", 0, _hinge_still(sfx, rel, h, d, "first"), HINGE_WORDS["start"][len("First frame: "):]),
              ("OATH and ACTION in place", SLOW, _hinge_still(sfx, rel, h, d, "middle"),
               "Both words rest in their places, with the gap where the ampersand goes."),
              ("Last frame", HINGE, f'<div class="oai-mv-box" style="padding:0 {d}px">{mark(rel, h=h, decorative=True)}</div>',
               "The wordmark’s 24 px master, unchanged.")]
    timeline = [
        f"0{NB}ms: OATH and ACTION slide toward each other, {HINGE_SIZES[0][3]}{NB}px each at 24{NB}px and "
        f"{HINGE_SIZES[1][3]}{NB}px each at 64{NB}px, over the slow {msw(SLOW)} with the standard easing.",
        f"{msw(SLOW)}: both rest in their places, and the gap holds.",
        f"{msw(HINGE_B_AT)}: the ampersand lands in the gap, from {round(LAND_FROM * 100)} percent of its size to its true "
        f"size, over the standard {msw(STD)} with the enter easing.",
        f"{msw(HINGE)}, the hinge duration: at rest on the master."]
    body = player("oai-hinge", title="The hinge", kicker=f"The wordmark, {HINGE} ms", grounds=grounds, words=HINGE_WORDS, frames=frames,
                  timeline=timeline, tracks=tracks, group="Play the hinge", start_css=css)
    alt = (f"A live player for the hinge, the wordmark's own motion, on Newsprint and on Charcoal. At rest it shows the "
           f"wordmark's master, OATH & ACTION with its red ampersand, from its 24 pixel master at 24 pixels, and on a "
           f"wide screen from its display master at 64 pixels tall as well. Play steps to the first frame, where OATH and "
           f"ACTION stand apart with no ampersand between them, then slides them toward each other over {SLOW} ms; the "
           f"gap holds, then the ampersand lands in it, from {round(LAND_FROM * 100)} percent of its size to its true "
           f"size, and comes to rest at {HINGE} ms on the master. One button plays and pauses, Reset returns to the "
           f"master, Slow motion plays at one tenth speed, and a status line says each frame in words. The still view "
           f"draws the first frame, the words in place and the last frame, and lists each step with its time.")
    return rec("s-17-hinge-correct", "17.6", None, alt, PLAYER_JS_WRAP(body), css=PLAYER_CSS + HINGE_CSS + css, interactive=True,
               caption=(f"Live, at rest on the wordmark’s master. Press Play, and OATH and ACTION start apart, settle into "
                        f"place over {msw(SLOW)}, then the ampersand lands between them and comes to rest at "
                        f"{msw(HINGE)}, on the master again. The master stands at 24 px and, on a wide screen, at 64 px."),
               notes=(f"Rule 17.6, the hinge (oa.motion.duration.hinge, {HINGE} ms). The moving layer is each master's own "
                      "elements, inlined: the letter path split by position into OATH (six subpaths) and ACTION (eight), "
                      "each subpath's bytes unchanged, and B's path as the file draws it. The end layer is the master "
                      "placed by reference, so the last frame is the master itself. Timing read from tokens.css at the "
                      f"press: slide {SLOW} ms, standard easing; B lands at hinge minus standard, {HINGE_B_AT} ms, over "
                      f"{STD} ms with the enter easing, from {round(LAND_FROM * 100)} percent (chapter 17's land). The "
                      "first frame's slides are whole pixels on screen. Round 2 fix pass (CD-M1, CD-S4, call 5): the "
                      "player rests on the master (data-frame end, data-oa-rest master), Play steps to the first frame "
                      "and runs to the master, Reset returns to the master and is unavailable at rest; each master's left "
                      f"edge sits on its label's, and the first frame slides outward into the ground's {HINGE_PAD} px "
                      "padding. Written by stage_c_identity_ch17.py."))


def PLAYER_JS_WRAP(body):
    return f"{body}<script>{PLAYER_JS}</script>"


# ------------------------------------------------------------------------------------------------ 17.6: the lever
LEVER_WORDS = {"rest": "At rest: the lockmark as its master draws it, nine nodes joined by their links, with the red "
                       "lever at bottom right.",
               "start": "First frame: the field is empty.",
               "end": "Last frame: the lockmark as its master draws it, nine nodes joined by their links, with the red "
                      "lever at bottom right.",
               "run": "Playing.", "pause": "Paused."}


def _lever_still(state):
    sfx, rel, h, _ = LEVER_SIZES[0]
    if state == "first":
        return f'<span class="oai-mv-empty" style="width:{h}px;height:{h}px" aria-hidden="true"></span>'
    st = {"links": {"nodes": "visibility:hidden", "lever": "visibility:hidden"}}[state]
    return f'<div class="oai-mv-box">{lever_layer(rel, h, "newsprint", sfx, still=st)}</div>'


@spec
def s_17_lever_correct():
    tracks, css = lever_frames()
    cells = {}
    for s in ("newsprint", "charcoal"):
        cells[s] = "".join(cell(lever_layer(rel, h, s, sfx), mark(rel, h=h, surface=s, decorative=True), lab)
                           for sfx, rel, h, lab in LEVER_SIZES)
    grounds = ground("newsprint", cells["newsprint"]) + ground("charcoal", cells["charcoal"])
    sfx, rel, h, _ = LEVER_SIZES[0]
    frames = [("First frame", 0, _lever_still("first"), "The field is empty; the dashed square marks its place and is no part of the lockmark."),
              ("Links drawn", STD, _lever_still("links"), "The six links, drawn from the top left, with no node yet."),
              ("Last frame", LEVER, f'<div class="oai-mv-box">{mark(rel, h=h, decorative=True)}</div>',
               "The lockmark’s 48 px master, unchanged.")]
    timeline = [
        f"0{NB}ms: the six links draw from the top left, over the standard {msw(STD)} with the enter easing.",
        f"{msw(LEVER_NODES_AT)}, one stagger after the links: the eight nodes land together, from "
        f"{round(LAND_FROM * 100)} percent of their size to their true size, over {msw(STD)} with the enter easing.",
        f"{msw(LEVER_AT)}: the lever lands last, the same way, over {msw(STD)}.",
        f"{msw(LEVER)}, the lever duration: at rest on the master."]
    body = player("oai-lever", title="The lever landing", kicker=f"{LEVER} ms, on request", grounds=grounds, words=LEVER_WORDS,
                  frames=frames, timeline=timeline, tracks=tracks, group="Play the lever landing", start_css=css)
    alt = (f"A live player for the lever landing, the lockmark's own motion, on Newsprint and on Charcoal, at 48 pixels "
           f"from the 48 pixel master and at 120 pixels from the display master. At rest it shows the lockmark's masters. "
           f"Play steps to the first frame, an empty field, then draws the six links from the top left over {STD} ms; one "
           f"stagger later the eight nodes land together from {round(LAND_FROM * 100)} percent of their size; the red "
           f"lever lands last, at bottom right, and comes to rest at {LEVER} ms on the master. One button plays and "
           f"pauses, Reset returns to the master, Slow motion plays at one tenth speed, and a status line says each frame "
           f"in words. The still view draws the empty field, the links drawn and the last frame, and lists each step with "
           f"its time.")
    return rec("s-17-lever-correct", "17.6", None, alt, PLAYER_JS_WRAP(body), css=PLAYER_CSS + css, interactive=True,
               label="The lockmark’s motion",
               caption=(f"Live, at rest on the lockmark’s masters, the 48 px master at 48 px and the display master at "
                        f"120 px. Press Play, and the field empties, then the links draw from the top left, the eight nodes "
                        f"land together and the lever lands last, coming to rest on the master again at {msw(LEVER)}."),
               notes=(f"Rule 17.6, the lever landing (oa.motion.duration.lever, {LEVER} ms). The moving layer is each "
                      "master's own elements, inlined and named by part: three horizontal and three vertical links, "
                      "eight nodes and the lever. The end layer is the master placed by reference. Timing read from "
                      f"tokens.css at the press: links draw over {STD} ms from 0; nodes land at standard plus stagger, "
                      f"{LEVER_NODES_AT} ms; the lever lands at lever minus standard, {LEVER_AT} ms; each land {STD} ms "
                      f"with the enter easing from {round(LAND_FROM * 100)} percent. Round 2 fix pass (CD-M1, call 5): "
                      "the player rests on the master, Play steps to the empty first frame and runs to the master, Reset "
                      "returns to the master and is unavailable at rest, and the dashed squares that marked the empty "
                      "first frame in the live player are gone; the still view keeps its first frame. Written by "
                      "stage_c_identity_ch17.py."))


# ------------------------------------------------------------------------------------------------ 17.6: the failure
FAIL_CSS = (".oai-mf{display:grid;gap:16px;max-width:42rem}"
            ".oai-mf-grid{display:grid;gap:12px}"
            ".oai-mf-row{display:flex;flex-wrap:wrap;gap:12px 40px;align-items:flex-end}"
            ".oai-mf-cell{display:grid;gap:8px;justify-items:start}"
            ".oai-mf-h{" + tyv("label") + ";color:var(--oa-color-text-secondary-on-newsprint);margin:8px 0 0}"
            ".oai-mf-tag{" + tyv("caption") + ";color:var(--oa-color-text-secondary-on-newsprint)}"
            ".oai-mf-px{display:block;max-width:100%;height:auto;image-rendering:pixelated;image-rendering:crisp-edges}"
            ".oai-mf-pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr));gap:16px 24px}"
            ".oai-mf-one{grid-template-columns:minmax(0,1fr)}"
            ".oai-mf-nt{" + tyv("body-small") + ";max-width:62ch}")
FAIL_OFF = 0.5                   # half a pixel: the player centers each mark with translate(-50%, -50%) in a box one
                                 # pixel taller than the mark; a transform is not snapped to whole pixels, as padding is
FAIL_ZOOM = 6


def _fail_raster(rel, h, w_px, low, name, crop_w=None):
    """Chromium's 1x render of one master on Newsprint, at rest on the pixel grid or half a pixel low, as a PNG data URI
    and its size. crop_w keeps the left part only (a wordmark's first letters)."""
    LIB.INLINE_ALL[0] = True
    try:
        raw = mark(rel, h=h, decorative=True)
    finally:
        LIB.INLINE_ALL[0] = False
    w = (crop_w or w_px) + 4
    hh = h + 4
    tf = f'transform:translateY({FAIL_OFF}px);' if low else ''
    html = (f'<div style="width:{w}px;height:{hh}px;overflow:hidden;background:var(--oa-color-surface-newsprint);'
            f'padding:2px 0 0 2px;box-sizing:border-box;line-height:0"><div style="{tf}line-height:0">{raw}</div></div>')
    return raster_png(html, w, hh, name, scale=1), w, hh


@spec
def s_17_hinge_failure():
    """Rule 17.6's failure, for the hinge and the lever alike: last frames half a pixel below their masters."""
    marks = [("wordmark", WM[24], 24, 221, "The hinge, 24 px"), ("lockmark", LOCK[48], 48, 48, "The lever landing, 48 px")]

    def at(rel, h, low):
        m = mark(rel, h=h, decorative=True)
        return f'<div style="transform:translateY({FAIL_OFF}px);line-height:0">{m}</div>' if low else m
    def row(low):
        return ('<div class="oai-mf-row">'
                + "".join(f'<div class="oai-mf-cell">{at(rel, h, low)}<span class="oai-mf-tag">{E(lab)}</span></div>' for _, rel, h, _, lab in marks)
                + "</div>")
    true_size = ('<div class="oai-mf-grid"><p class="oai-mf-h">Last frames, half a pixel low</p>' + row(True)
                 + '<p class="oai-mf-h">The masters</p>' + row(False) + "</div>")
    # enlarged from a 1x screen: the lockmark whole, and the wordmark's first letters
    big = []
    for key, rel, h, w_px, crop in (("lockmark", LOCK[48], 48, 48, None), ("wordmark", WM[24], 24, 221, 104)):
        cells = []
        for low, lab in ((True, "Half a pixel low"), (False, "The master")):
            uri, w, hh = _fail_raster(rel, h, w_px, low, f"s17-fail-{key}-{'low' if low else 'master'}", crop)
            cells.append(f'<div class="oai-mf-cell"><img class="oai-mf-px" src="{uri}" width="{w * FAIL_ZOOM}" '
                         f'height="{hh * FAIL_ZOOM}" alt=""><span class="oai-mf-tag">{E(lab)}</span></div>')
        big.append(f'<div class="oai-mf-pair{" oai-mf-one" if crop else ""}">{"".join(cells)}</div>')
    body = (f'<div class="oai-mf">{dnp()}<div class="oai-panel oai-s-newsprint">{true_size}</div>'
            f'<p class="oai-mf-h" style="margin:0">Enlarged {FAIL_ZOOM} times from a 1x screen</p>{"".join(big)}'
            f'<p class="oai-mf-nt">The player centers each mark with <code>translate(-50%, -50%)</code> in a box one pixel '
            f'taller than the mark, so the motion comes to '
            f'rest half a pixel below the pixel grid. On a 1x screen each 1{NB}px link of the lockmark spreads into two rows of '
            f'gray, every node blurs, and the wordmark’s top and bottom edges go soft. A 2x screen hides the fault, so check '
            f'the last frame on a 1x screen.</p></div>')
    alt = ("Failure case: do not publish. The last frames of the hinge and the lever landing, half a pixel below their "
           "masters, beside the masters at true size: the wordmark at 24 pixels and the lockmark at 48 pixels. Below, "
           "enlarged six times from a 1x screen: the lockmark half a pixel low, whose one pixel links have each spread into "
           "two rows of gray and whose nodes have blurred, beside its crisp master; then the first letters of the wordmark, "
           "whose top and bottom edges have gone gray, beside the master.")
    return rec("s-17-hinge-failure", "17.6", None, alt, body, css=FAIL_CSS, check_exempt=["scale"],
               caption=("Last frames that come to rest half a pixel low, because the player centers each mark with a "
                        "transform in a box one pixel taller than the mark. On a 1x screen the lockmark’s links turn into "
                        "gray bands and the wordmark goes soft, so each last frame is a second version of its mark."),
               notes=("Failure for Rule 17.6, for the hinge and the lever: a last frame off its master by half a pixel. The "
                      "true-size marks are moved down with transform: translateY(0.5px), since Chromium snaps an svg's "
                      "box to whole pixels but not a transform; the enlargements are Chromium's 1x renders of the same "
                      "masters, embedded as PNG and drawn with pixelated scaling, since a 2x screen hides the fault. The "
                      "wordmark's enlargement keeps its first 104 px. check_exempt scale: the enlargements show pixels on "
                      "purpose. Written by stage_c_identity_ch17.py."))
