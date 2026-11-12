"""Write chapter 14's rules for every chart (14.1 to 14.14), their plates, and the chapter's own words.

Oath & Action Edition 06, Phase 3, round 1. Editor (oa-editor), November 12, 2026, under
work/handoffs/phase-3/20261112_Phase-3-Round-1-Brief.md (R1, R2, C7) and the plan file
work/handoffs/phase-3/20261112_Chapter-14-Plan.json, which fixes every number and subject.

Usage:
    python3 -I work/build/scripts/phase-3/phase3_ch14_rules_build.py [--check-only]

Reads every value it prints, by script, from work/build/data/*.csv, *.json and their sidecars (contract C1).
Writes:
    work/build/guide/entries/14-001.json to 14-014.json   one entry file per rule (R2), with chapter 13's plate shape
    work/build/guide/entries/14-chapter.json               the opener, introduction, group lines and sources
    work/build/guide/specimens/s-14-<n>-correct.html, s-14-<n>-failure.html and s-14-opener.html
    work/build/guide/specimens/s-14-<n>-*.chart.json       contract C7's specs, drawn by the kit in the guide

Each plate's manifest fields (alt, illustrative, readable, notes) travel inside its entry's correct or failure
object, and each rule's examples for Rule 01.12's log travel in its "examples" list, for the engineer's chapter
14 generator to read.

Then runs the editor's checks and stops on any failure: the plan's numbers and subjects, no em dash or U+2011, no
listed filler or corporate word, no studio word or decision code in reader text, titles of about twelve words,
every failure caption led by "Fails Rule 14.N.", every failure plate with the do-not-publish band and an alt that
opens "Failure case: do not publish.", no literal color, every token named in tokens.json, every rule cited in the
chapter or plan, every figure in a title checked against its data, the opener under 16 KB, and the rules with the
opener under 0.20 MB.
"""
import csv
import html
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
DATA = ROOT / "work/build/data"
ENTRIES = ROOT / "work/build/guide/entries"
SPECIMENS = ROOT / "work/build/guide/specimens"
PLAN = json.loads((ROOT / "work/handoffs/phase-3/20261112_Chapter-14-Plan.json").read_text())
TOKENS = ROOT / "work/build/tokens/tokens.json"
WRITTEN = "November 12, 2026"
MINUS = "−"
BASIS = "Design judgment, from the chart system our founder and editor approved in November 2026"
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
          "November", "December"]


def need(cond, msg):
    if not cond:
        raise SystemExit(f"phase3_ch14_rules_build: {msg}")


def e(s):
    return html.escape(str(s), quote=True)


def sidecar(name):
    return json.loads((DATA / f"{name}.meta.json").read_text())


def rows(name):
    p = DATA / f"{name}.csv"
    if p.exists():
        with open(p, newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    return json.loads((DATA / f"{name}.json").read_text())["rows"]


def comma(n):
    return f"{int(round(n)):,}"


def fmt1(x):
    s = f"{x:.1f}"
    return s.replace("-", MINUS)


def words_date(iso):
    y, m, d = iso.split("-")
    return f"{MONTHS[int(m) - 1]} {int(d)}, {y}"


# ---------------------------------------------------------------------------------------------------------------
# Styles. Each plate carries only the rules its own markup uses (D2-1732). Sizes from type or chart tokens, colors from
# the short chart names the stage's surface class sets, so a plate follows Newsprint and Charcoal alike.
# ---------------------------------------------------------------------------------------------------------------
LBL = ("font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);"
       "text-transform:var(--oa-type-label-text-transform)")
CAP = "font:var(--oa-type-caption)"
SMALL = "font:var(--oa-type-body-small)"
BASE = (":scope{color:var(--oa-color-text-primary)}"
        ".p{box-sizing:border-box;padding:16px;font:var(--oa-type-body);max-width:100%}"
        ".p *{box-sizing:border-box}:where(.p) :where(p){margin:0}@media (min-width:48em){.p{padding:24px}}")
CSS = {
    "dnp": f".dnp{{display:flex;align-items:center;gap:8px;margin:0 0 16px;padding:6px 10px;background:var(--oa-color-surface-charcoal);"
           f"color:var(--oa-color-text-primary-on-charcoal);{LBL}}}",
    "evr": ".evr{display:flex;flex-wrap:wrap;align-items:center;gap:6px 12px;margin:0 0 10px}",
    "ev": f".ev{{display:inline-flex;align-items:center;min-height:24px;padding:3px 8px;background:var(--oa-chart-color-chip-fill);"
          f"color:var(--oa-chart-color-chip-label);{LBL}}}",
    "gr": f".gr{{{CAP};color:var(--oa-color-text-secondary)}}",
    "illus": f".illus{{display:inline-block;padding:2px 6px;border:1px solid var(--oa-color-border-strong);{LBL}}}",
    "ct": (".ct{font:var(--oa-font-weight-extrabold) var(--oa-chart-type-title-phone-size)/var(--oa-chart-type-title-phone-leading) "
           "var(--oa-font-family-display);letter-spacing:-0.01em;margin:0 0 6px;max-width:34em;text-wrap:balance}"
           "@media (min-width:48em){.ct{font-size:var(--oa-chart-type-title-size);line-height:var(--oa-chart-type-title-leading)}}"),
    "gd": ".gd{font:var(--oa-type-body-small);margin:6px 0 0;max-width:40em}",
    "ms": (".ms{font:400 var(--oa-chart-type-measure-size)/var(--oa-chart-type-measure-leading) var(--oa-font-family-reading);"
           "color:var(--oa-color-text-secondary);margin-top:6px;max-width:40em}"),
    "art": ".art{margin-top:20px}",
    "nt": f".nt{{{CAP};margin-top:12px;max-width:40em}}",
    "src": f".src{{{CAP};color:var(--oa-color-text-secondary);margin-top:12px;padding-top:8px;border-top:1px solid var(--oa-color-border-hairline);max-width:44em}}",
    "eq": (f".eq{{margin-top:10px}}.eq>summary{{cursor:pointer;font:var(--oa-font-weight-semibold) var(--oa-type-body-small-font-size)/1.5 var(--oa-font-family-reading)}}"
           f".eq table{{border-collapse:collapse;margin-top:8px;{SMALL}}}.eq caption{{{CAP};text-align:left;color:var(--oa-color-text-secondary);padding-bottom:4px}}"
           f".eq th,.eq td{{text-align:left;padding:4px 16px 4px 0;border-bottom:1px solid var(--oa-color-border-hairline)}}"
           f".eq thead th{{{LBL};color:var(--oa-color-text-secondary)}}.eq tbody th{{font-weight:var(--oa-font-weight-regular)}}"
           f".eq td.n{{text-align:right;font-variant-numeric:tabular-nums}}"),
    # HTML bars: a name, a track and a value per row, so the words stay at their size at any width
    "hb": (f".hb{{list-style:none;margin:0;padding:0;display:grid;gap:6px;{SMALL}}}"
           ".hb li{display:grid;grid-template-columns:minmax(0,9.5rem) minmax(0,1fr) 3.4rem;align-items:center;gap:10px}"
           ".hb .bt{position:relative;height:var(--oa-chart-bar-phone-height)}.hb .b{position:absolute;left:0;top:0;bottom:0;background:var(--oa-chart-color-context)}"
           ".hb .b.s{background:var(--oa-chart-color-subject)}.hb .b.pt{background:var(--oa-chart-color-point);box-shadow:inset 0 0 0 1px var(--oa-chart-color-point-keyline)}"
           ".hb .v{text-align:right;font-variant-numeric:tabular-nums}.hb .nm.s,.hb .v.s{font-weight:var(--oa-font-weight-bold)}"
           ".hb .bt::before{content:'';position:absolute;left:0;top:-3px;bottom:-3px;border-left:var(--oa-chart-line-baseline) solid var(--oa-chart-color-baseline)}"),
    "rk": (f".rk{{list-style:none;margin:0;padding:0;{SMALL}}}.rk li{{display:grid;grid-template-columns:2.2rem minmax(0,1fr) 4rem;gap:8px;padding:5px 0;"
           f"border-bottom:1px solid var(--oa-color-border-hairline)}}.rk .r{{font-weight:var(--oa-font-weight-bold)}}.rk .v{{text-align:right;font-variant-numeric:tabular-nums}}"),
    # a dot with its interval per row, positioned in percent of the track
    "di": (f".di{{list-style:none;margin:0;padding:0;display:grid;gap:4px;{SMALL}}}"
           ".di li{display:grid;grid-template-columns:minmax(0,7.5rem) minmax(0,1fr) 4.2rem;align-items:center;gap:10px;min-height:26px}"
           ".di .tk{position:relative;height:22px}.di .iv{position:absolute;top:10px;height:2px;background:var(--oa-chart-color-context)}"
           ".di .dt{position:absolute;top:4px;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:var(--oa-chart-color-subject);border:2px solid var(--oa-chart-color-subject)}"
           ".di .dt.o{background:var(--oa-color-surface)}"
           ".di .ref{position:absolute;top:-6px;bottom:-6px;border-left:var(--oa-chart-line-baseline) dashed var(--oa-chart-color-baseline)}"
           ".di .v{text-align:right;font-variant-numeric:tabular-nums}.di li.hd{min-height:0}.di li.hd .tk{height:auto;"
           f"{CAP};color:var(--oa-color-text-secondary)}}"),
    "ky": f".ky{{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 12px;{CAP}}}.ky span{{display:inline-flex;align-items:center;gap:6px}}",
    "kd": (".kd{display:inline-block;width:14px;height:14px;border-radius:50%;border:2px solid var(--oa-chart-color-subject);background:var(--oa-chart-color-subject)}"
           ".kd.o{background:var(--oa-color-surface)}"),
    "sv": (".sv{display:block;max-width:100%;height:auto;overflow:visible}.sv text{font-family:var(--oa-font-family-reading);"
           "font-size:var(--oa-chart-type-label);fill:var(--oa-chart-color-label)}.sv .tk{font-size:var(--oa-chart-type-tick);fill:var(--oa-color-text-secondary)}"
           ".sv .b{font-weight:var(--oa-font-weight-bold)}.sv .ax{stroke:var(--oa-chart-color-baseline);stroke-width:var(--oa-chart-line-baseline)}"
           ".sv .gl{stroke:var(--oa-chart-color-gridline);stroke-width:1}.sv .ln{fill:none;stroke:var(--oa-chart-color-subject);stroke-width:var(--oa-chart-line-subject);stroke-linejoin:round}"
           ".sv .lc{fill:none;stroke:var(--oa-chart-color-context);stroke-width:var(--oa-chart-line-context)}"
           ".sv .s{fill:var(--oa-chart-color-subject)}.sv .c{fill:var(--oa-chart-color-context)}.sv .o{fill:var(--oa-color-surface);stroke:var(--oa-chart-color-subject);stroke-width:2}"
           ".sv .ld{stroke:var(--oa-chart-color-leader);stroke-width:1}"),
    "g1": ".sv .g1{stroke:var(--oa-chart-color-categorical-fill-group1)}.sv .g2{stroke:var(--oa-chart-color-categorical-fill-group2)}"
          ".sv .g3{stroke:var(--oa-chart-color-categorical-fill-group3)}.sv .g4{stroke:var(--oa-chart-color-categorical-fill-group4)}"
          ".sv .g5{stroke:var(--oa-chart-color-sequential-fill-step3)}.sv .kl{stroke-width:3}",
    "band": ".sv .bd{fill:var(--oa-chart-color-band)}",
    "rb": ".sv .rd{fill:var(--oa-color-palette-pillar-red)}.sv .bl{fill:var(--oa-color-palette-prussian)}",
    "kc": ".sv .kc{fill:var(--oa-chart-color-subject)}",
    "pal": (f".pal{{display:grid;gap:14px}}.pal .row{{display:grid;grid-template-columns:minmax(0,1fr);gap:6px;padding-bottom:12px;border-bottom:1px solid var(--oa-color-border-hairline)}}"
            f"@media (min-width:48em){{.pal .row{{grid-template-columns:12rem minmax(0,15rem) minmax(0,1fr);gap:16px;align-items:center}}}}"
            f".pal .nm{{font-weight:var(--oa-font-weight-bold)}}.pal .sw{{display:flex;gap:3px}}.pal .sw i{{flex:1 1 0;height:28px;min-width:20px}}"
            f".pal .jb{{{SMALL}}}.pal .q{{{CAP};color:var(--oa-color-text-secondary)}}"
            ".pal .hx{background-image:repeating-linear-gradient(135deg,transparent 0 4px,var(--oa-color-surface) 4px 6px)}"),
    "sw": ("i.s1{background:var(--oa-chart-color-sequential-fill-step1)}i.s2{background:var(--oa-chart-color-sequential-fill-step2)}"
           "i.s3{background:var(--oa-chart-color-sequential-fill-step3)}i.s4{background:var(--oa-chart-color-sequential-fill-step4)}"
           "i.s5{background:var(--oa-chart-color-sequential-fill-step5)}"
           "i.d1{background:var(--oa-chart-color-diverging-fill-step1)}i.d2{background:var(--oa-chart-color-diverging-fill-step2)}"
           "i.d3{background:var(--oa-chart-color-diverging-fill-step3);box-shadow:inset 0 0 0 1px var(--oa-chart-color-sequential-outline)}"
           "i.d4{background:var(--oa-chart-color-diverging-fill-step4)}i.d5{background:var(--oa-chart-color-diverging-fill-step5)}"
           "i.c1{background:var(--oa-chart-color-categorical-fill-group1)}i.c2{background:var(--oa-chart-color-categorical-fill-group2)}"
           "i.c3{background:var(--oa-chart-color-categorical-fill-group3)}i.c4{background:var(--oa-chart-color-categorical-fill-group4)}"
           "i.m1{background:var(--oa-chart-color-magnitude-fill-step1)}i.m2{background:var(--oa-chart-color-magnitude-fill-step2)}"
           "i.m3{background:var(--oa-chart-color-magnitude-fill-step3)}i.m4{background:var(--oa-chart-color-magnitude-fill-step4)}"),
    "sb": (f".sb{{list-style:none;margin:0;padding:0;display:grid;gap:6px;{SMALL}}}.sb li{{display:grid;grid-template-columns:minmax(0,9rem) minmax(0,1fr) 3rem;gap:10px;align-items:center}}"
           ".sb .bt{height:var(--oa-chart-bar-phone-height)}.sb .v{text-align:right;font-variant-numeric:tabular-nums}"
           ".sb i{display:block;height:100%}"),
    "two": ".two{display:grid;grid-template-columns:minmax(0,1fr);gap:28px}@media (min-width:60em){.two{grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);align-items:start}}",
    "fr": (f".fr{{border:1px solid var(--oa-color-border-strong);padding:14px}}.fr .fh{{{LBL};color:var(--oa-color-text-secondary);margin:0 0 10px}}"
           ".fr.ph{max-width:358px}"),
    "cl": (".cl{display:flex;align-items:flex-end;gap:6px;height:180px;border-bottom:var(--oa-chart-line-baseline) solid var(--oa-chart-color-baseline);margin-top:8px}"
           ".cl .c{flex:1 1 0;display:flex;flex-direction:column;justify-content:flex-end;align-items:stretch;height:100%;min-width:0}"
           ".cl .c i{display:block;background:var(--oa-chart-color-context)}.cl .c.s i{background:var(--oa-chart-color-subject)}"
           f".cl .c b{{display:block;text-align:center;font-variant-numeric:tabular-nums;{CAP};margin-bottom:4px}}"
           f".cn{{display:flex;gap:6px;{CAP}}}.cn span{{flex:1 1 0;min-width:0;text-align:center;overflow-wrap:anywhere;padding-top:6px}}"),
    "files": (f".files{{list-style:none;margin:0;padding:0;{SMALL}}}.files li{{display:grid;grid-template-columns:minmax(0,1fr);gap:2px;padding:10px 0;border-bottom:1px solid var(--oa-color-border-hairline)}}"
              f"@media (min-width:48em){{.files li{{grid-template-columns:minmax(0,1fr) 5rem minmax(0,16rem);gap:16px;align-items:baseline}}}}"
              ".files .fn{font-weight:var(--oa-font-weight-semibold);overflow-wrap:anywhere}.files .ty{font-weight:var(--oa-font-weight-semibold)}"
              f".files .what{{{CAP};color:var(--oa-color-text-secondary)}}"),
    "cmd": (f".cmd{{margin:0 0 14px;padding:10px 12px;background:var(--oa-color-surface-white);border:1px solid var(--oa-color-border-hairline);"
            f"font:var(--oa-type-body-small);overflow-wrap:anywhere}}"),
    "hov": (f".hov{{{CAP};color:var(--oa-color-text-secondary);margin-top:8px}}"),
    "k": f".k{{{LBL};color:var(--oa-color-text-secondary)}}",
    "tip": (f".tip{{display:inline-block;margin-top:10px;padding:6px 10px;background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);{SMALL}}}"),
    "opq": (".opq{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0}"
            "@media (min-width:48em){.opq{grid-template-columns:repeat(2,minmax(0,1fr));column-gap:32px}}"
            ".opq li{display:grid;grid-template-columns:2.4rem minmax(0,1fr);gap:4px 10px;padding:10px 0;border-top:1px solid var(--oa-color-border-hairline)}"
            f".opq .n{{{LBL};color:var(--oa-color-text-secondary);padding-top:4px}}"
            ".opq .qq{font:var(--oa-font-weight-bold) var(--oa-type-h4-font-size)/var(--oa-type-h4-line-height) var(--oa-font-family-display);letter-spacing:-0.01em}"
            f".opq .fm{{{CAP};color:var(--oa-color-text-secondary);grid-column:2}}"),
    "olp": (f".olp{{margin:16px 0 0;padding:0;list-style:none;counter-reset:pt;display:grid;gap:4px;{SMALL}}}"
            ".olp li{counter-increment:pt;display:grid;grid-template-columns:28px minmax(0,1fr);gap:8px;align-items:center}"
            f".olp li::before,.anat .mk::before{{content:counter(pt);display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border-radius:50%;"
            f"background:var(--oa-chart-color-chip-fill);color:var(--oa-chart-color-chip-label);{LBL};letter-spacing:0}}"),
}


def styled(body, extra=""):
    used = set()
    for cls in re.findall(r'class="([^"]+)"', body):
        used.update(cls.split())
    rules = [BASE] + [css for k, css in CSS.items() if k in used] + ([extra] if extra else [])
    return "<style>" + "".join(rules) + "</style>"


def dnp():
    return '<p class="dnp"><span aria-hidden="true">×</span>Failure case: do not publish</p>'


def ill(words="Illustrative data"):
    return f'<span class="illus">{e(words)}</span>'


def head(label, grade, title, guide=None, measure=None, illus=None):
    out = [f'<div class="evr"><span class="ev">{e(label)}</span>' + (f'<span class="gr">{e(grade)}</span>' if grade else "")
           + (ill(illus) if illus else "") + "</div>", f'<p class="ct">{e(title)}</p>']
    if guide:
        out.append(f'<p class="gd">{e(guide)}</p>')
    if measure:
        out.append(f'<p class="ms">{e(measure)}</p>')
    return "".join(out)


def tl(title):
    """A failure plate's title alone: the caption names the fault, so the plate carries only what shows it."""
    return f'<p class="ct">{e(title)}</p>'


def foot(notes=(), source=None):
    out = [f'<p class="nt">{e(n)}</p>' for n in notes]
    if source:
        out.append(f'<p class="src">{e(source)}</p>')
    return "".join(out)


def table(caption, cols, data):
    """The table equivalent, live text, folded under the source line as the kit folds it (Rule 14.13)."""
    th = "".join(f'<th scope="col">{e(c)}</th>' for c in cols)
    body = "".join("<tr>" + "".join((f'<th scope="row">{e(v)}</th>' if i == 0 else f'<td class="n">{e(v)}</td>') for i, v in enumerate(r)) + "</tr>"
                   for r in data)
    return (f'<details class="eq"><summary>The table and notes</summary><table><caption>{e(caption)}</caption>'
            f"<thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></details>")


def chart(cid):
    return f'<div class="art" data-oa-chart="{cid}"></div>'


# ---------------------------------------------------------------------------------------------------------------
# Static drawings, written by this script from the data: lines in an SVG drawn at a phone's width (so no word falls
# under 13 px at 390 px), bars and dots in HTML so their words keep their size at any width.
# ---------------------------------------------------------------------------------------------------------------
def scale(d0, d1, r0, r1):
    return lambda v: r0 + (v - d0) * (r1 - r0) / (d1 - d0)


def path(pts):
    return "M" + "L".join(f"{x:.0f} {y:.0f}" for x, y in pts)


def svg(w, h, inner, cls="sv"):
    return (f'<svg class="{cls}" viewBox="0 0 {w} {h}" width="{w}" height="{h}" aria-hidden="true" focusable="false">'
            f"{inner}</svg>")


def axis_y(ys, ticks, x0, x1, fmt):
    out = []
    for t in ticks:
        y = ys(t)
        out.append(f'<line class="gl" x1="{x0}" x2="{x1}" y1="{y:.1f}" y2="{y:.1f}"/>'
                   f'<text class="tk" x="{x0}" y="{y - 4:.1f}">{e(fmt(t))}</text>')
    return "".join(out)


def axis_x(xs, ticks, y, fmt):
    return "".join(f'<text class="tk" x="{xs(t):.1f}" y="{y}" text-anchor="middle">{e(fmt(t))}</text>' for t in ticks)


def hbars(data, vmax, fmt, subject=(), point=(), red=()):
    """Bars in HTML: data is [(name, value)]; subject names are set in ink, point names take the view's red."""
    out = []
    for name, v in data:
        cls = "pt" if name in point else ("s" if name in subject else "")
        red_attr = ' data-red="failure"' if name in red else ""
        out.append(f'<li><span class="nm{" s" if cls else ""}">{e(name)}</span><span class="bt"><span class="b {cls}"{red_attr} '
                   f'style="width:{100 * v / vmax:.2f}%"></span></span><span class="v{" s" if cls else ""}">{e(fmt(v))}</span></li>')
    return '<ul class="hb">' + "".join(out) + "</ul>"


# ---------------------------------------------------------------------------------------------------------------
# The book of plates and specs
# ---------------------------------------------------------------------------------------------------------------
class Book:
    def __init__(self):
        self.files, self.specs, self.plates = {}, {}, {}

    def add(self, sid, body, *, alt, illustrative=False, readable=False, notes="", extra_css=""):
        need(sid not in self.files, f"duplicate specimen {sid}")
        body = re.sub(r">\s+<", "><", body.strip())
        self.files[sid] = (f"<!-- {sid}: Oath & Action guide, Edition 06, chapter 14. Editor, {WRITTEN}. Written by "
                           f"work/build/scripts/phase-3/phase3_ch14_rules_build.py. -->\n" + styled(body, extra_css)
                           + f'\n<div class="p">{body}</div>\n')
        charts = re.findall(r'data-oa-chart="([^"]+)"', body)
        for c in charts:
            need(c in self.specs, f"{sid} places chart {c}, which has no spec")
        m = {"alt": " ".join(alt.split()), "illustrative": bool(illustrative), "notes": notes}
        if readable:
            m["readable"] = True
        if charts:
            m["charts"] = charts
        self.plates[sid] = m
        return sid

    def plate(self, sid, caption):
        need(sid in self.plates, f"no plate {sid}")
        return dict({"specimen": sid, "caption": caption}, **self.plates[sid])

    def spec(self, cid, **kw):
        """A kit spec under contract C2, its id the chart's (C7)."""
        need(cid not in self.specs, f"duplicate chart {cid}")
        s = {"kit": 1, "id": cid}
        s.update(kw)
        s.setdefault("illustrative", False)
        s.setdefault("phone", "same")
        self.specs[cid] = s
        return cid


def src(name):
    return sidecar(name)["printed_source_line"]


def variant(name, key):
    v = (sidecar(name).get("source_line_variants") or {}).get(key)
    need(v, f"{name} has no source line variant {key}")
    return v


def ex(example, domain, states=(), level="federal", where=""):
    """One example for Rule 01.12's log (Rule 01.9 counts it); a rule's two plates on one data are one example."""
    return {"example": example, "domain": domain, "states": list(states), "level": level, "where": where}


def entry(rid, title, rule, why, specs, related, builders, correct, failure, examples, tokens=(), basis=BASIS):
    return {"id": rid, "title": title, "rule": rule, "use_when": None, "use_instead": [], "why": {"text": why, "basis": basis},
            "specimen": None, "tier": None, "tokens": list(tokens), "related": related, "builders": builders,
            "specs": [dict(zip(("label", "value", "token"), s)) if len(s) == 3 else dict(zip(("label", "value"), s)) for s in specs],
            "correct": correct, "failure": failure, "examples": examples}


FC = "Failure case: do not publish. "


def fails(n, text):
    return f"<strong>Fails Rule {n}.</strong> {text}"


# ===============================================================================================================
# 14.1 Start from the reader's question, then choose the form
# ===============================================================================================================
def rule_14_1(B):
    ds = "census-bfs-business-applications-by-state"
    us = [(int(r["year"]), int(r["business_applications"])) for r in rows(ds) if r["code"] == "US"]
    us.sort()
    need(us[0][0] == 2005 and us[-1][0] == 2025 and len(us) == 21, "the business applications series no longer runs 2005 to 2025")
    first, last = us[0][1], us[-1][1]
    need(2 < last / first < 2.5 and round(last / 1e6, 1) == 5.7 and round(first / 1e6, 1) == 2.5, "the 2005 and 2025 totals moved")
    by_size = sorted(us, key=lambda t: -t[1])
    need(by_size[0][0] == 2025 and by_size[-1][0] == 2009, "the largest and smallest years moved")
    y2019, y2021 = dict(us)[2019], dict(us)[2021]
    title = "Americans filed 5.7 million applications to start a business in 2025, more than twice the 2.5 million of 2005"
    common = dict(form=None, family="change-over-time", tier="core", dataset=ds, where={"code": "US"},
                  reader_question="How has the number of applications to start a business changed since 2005?",
                  evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau count of applications for a tax ID",
                  title=title,
                  measure_line="Applications for a federal tax ID that signal a new business, each year from 2005, the first full year the "
                               "Census Bureau publishes, to 2025, United States",
                  source_line=variant(ds, "all_years"),
                  notes=["Many applications never become a business that hires anyone, so the count measures plans to start one."],
                  alt=f"A line of business applications each year from 2005 to 2025 in the United States: about {fmt1(first / 1e6)} million a year "
                      f"through 2013, rising to {fmt1(y2019 / 1e6)} million in 2019, {fmt1(y2021 / 1e6)} million in 2021 and {fmt1(last / 1e6)} million in 2025.",
                  table={"caption": "Business applications each year, United States",
                         "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                                     {"field": "business_applications", "label": "Applications", "format": "integer"}]},
                  domain="D06", states=[])
    B.spec("s-14-1-line", **dict(common, form="line-event-notes",
                                  encode={"x": "year", "y": "business_applications"},
                                  annotations=[{"at": {"x": 2005}, "text": "2.5 million", "place": "above"},
                                               {"at": {"x": 2025}, "text": "5.7 million", "place": "above"}],
                                  notes_internal="Rule 14.1's correct plate. Figures checked by script: 2005 and 2025 from the US rows."))
    B.spec("s-14-1-sorted", **dict(common, form="ranked-bar", family="comparison", sort=[{"field": "business_applications", "order": "desc"}],
                                    encode={"category": "year", "value": "business_applications"},
                                    reading_guide=None,
                                    failure={"rule": "14.1", "caption_lead": "Fails Rule 14.1."},
                                    alt="The same 21 years of business applications as bars sorted by size, from 2025 at the top to 2009 at the bottom, "
                                        "so the years run out of order.",
                                    notes_internal="Rule 14.1's failure plate: the right data in a form that answers another question."))
    for k in ("s-14-1-sorted",):
        B.specs[k].pop("reading_guide", None)
    B.add("s-14-1-correct", chart("s-14-1-line"),
          alt=f"A line chart answers how business applications changed: {title}. The line climbs slowly to 2019 and jumps to 2021.",
          notes="A line answers a question about change over time; the kit draws it from the US rows of the business formation file.")
    B.add("s-14-1-failure", dnp() + chart("s-14-1-sorted"),
          alt=FC + "The same applications drawn as bars sorted by size, 2025 first and 2009 last, so the years fall out of order.")
    return entry(
        "14.1", "Start from the reader’s question, then choose the form.",
        ["Write down the question a reader brings to the numbers, in the words a reader would use, before choosing a form. The question names "
         "the comparison: which is bigger, what moved, how it changed, what it is made of, where it happens, or how sure a figure is. Each "
         "group of this chapter opens with one of those questions, and each entry in the group says when its form fits the data at hand.",
         "When one figure answers the question, a sentence carries it (Rule 14.134). When a reader needs to look values up, a table does "
         "(Rule 14.133)."],
        ["Each form answers one kind of question well. Bars sorted by size show which year was largest and hide the order of the years, so "
         "a reader who asked how something changed cannot see the change."],
        [("First step", "The reader’s question, in a reader’s words, written into the chart’s spec before any drawing"),
         ("Question to form", "The question that opens each group of this chapter, then the entry whose use names the data at hand"),
         ("One figure", "A sentence, Rule 14.134"), ("Values to look up", "A table, Rule 14.133")],
        ["14.29", "14.15", "14.133", "14.134"],
        "Write reader_question in the spec first, then pick the form from the group whose question matches; the kit draws it with "
        "node work/build/chart-kit/oa-chart.mjs build <spec>.",
        B.plate("s-14-1-correct", "The question asks how applications changed, so the years run left to right on one line, and the jump "
                                  f"after 2019 shows at once: from {fmt1(y2019 / 1e6)} million to {fmt1(y2021 / 1e6)} million in two years."),
        B.plate("s-14-1-failure", fails("14.1", "The reader asked how applications changed, and bars sorted by size put 2025 first and "
                                                "2009 last, so the years fall out of order and the jump after 2019 cannot be seen.")),
        [ex("Business applications, United States, 2005 to 2025", "D06", where="14.1")])


# ===============================================================================================================
# 14.2 Build every chart in one anatomy
# ===============================================================================================================
PARTS = ["Evidence label and grade line", "Title", "Reading guide", "Measure line", "Chart", "Notes", "Source line", "Table"]


def rule_14_2(B):
    ds = "census-cbp-civic-organizations"
    r = {int(x["year"]): int(x["employees"]) for x in rows(ds)}
    need(min(r) == 1998 and max(r) == 2023, "the civic organizations series moved")
    drop = r[1998] - r[2023]
    need(round(drop, -2) == 113300, "the civic organizations figures moved")
    title = f"Civic and social organizations employed {comma(r[2023])} people in March 2023, about {comma(round(drop, -2))} fewer than in 1998"
    base = dict(form="line-event-notes", family="change-over-time", tier="core", dataset=ds,
                reader_question="How many people work for civic and social organizations, and how has that changed?",
                evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau count of employers",
                title=title,
                reading_guide="Each point is one year’s count of paid employees, taken in the pay period that includes March 12.",
                measure_line="Paid employees of civic and social organizations, such as service clubs and neighborhood associations, each year "
                             "from 1998, the first year counted under today’s industry codes, to 2023, United States",
                notes=["Groups run only by volunteers have no paid employees and do not appear in the count."],
                source_line=src(ds),
                alt=f"A line of paid employees at civic and social organizations from 1998 to 2023: {comma(r[1998])} in 1998, about 330,000 in "
                    f"2007, {comma(r[2009])} in 2009 and {comma(r[2023])} in 2023.",
                table={"caption": "Paid employees of civic and social organizations, mid-March of each year",
                       "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                                   {"field": "employees", "label": "Employees", "format": "integer"}]},
                encode={"x": "year", "y": "employees"}, domain="D10", states=[])
    B.spec("s-14-2-full", **dict(base, notes_internal="Rule 14.2's correct plate: every part of the anatomy, numbered by the plate's style."))
    B.spec("s-14-2-bare", **dict(base, title="Civic and social organizations, 1998 to 2023", show=["title", "chart"],
                                 failure={"rule": "14.2", "caption_lead": "Fails Rule 14.2."},
                                 notes_internal="Rule 14.2's failure plate: a topic for a title, and only the chart under it."))
    # the numerals sit in the left margin at desktop and before each part on a phone, in the order of PARTS
    sel = [".oac-ev", ".oac-title", ".oac-guide", ".oac-measure", ".oac-art", ".oac-notes", ".oac-src", ".oac-eq"]
    marks = "".join(f".anat {s}::before{{content:'{i + 1}'}}" for i, s in enumerate(sel))
    extra = (".anat{counter-reset:none}.anat .oac-fig>*{position:relative}"
             + ",".join(f".anat {s}::before" for s in sel)
             + "{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;margin:0 8px 4px 0;border-radius:50%;"
               "background:var(--oa-chart-color-chip-fill);color:var(--oa-chart-color-chip-label);" + LBL + ";letter-spacing:0;vertical-align:middle}"
             "@media (min-width:48em){.anat{padding-left:36px}" + ",".join(f".anat {s}::before" for s in sel)
             + "{position:absolute;left:-36px;top:0;margin:0}}" + marks)
    lst = "".join(f"<li>{e(p)}</li>" for p in PARTS)
    B.add("s-14-2-correct", f'<div class="anat">{chart("s-14-2-full")}</div><ol class="olp" aria-label="The parts in order">{lst}</ol>',
          alt=f"A finished chart with each of its eight parts numbered in reading order: {', '.join(PARTS)}. Its title: {title}.",
          notes="The numerals are drawn by the plate's style on the kit's own parts, so they follow the figure as the kit prints it.",
          extra_css=extra)
    B.add("s-14-2-failure", dnp() + chart("s-14-2-bare"),
          alt=FC + "The same line under a title that names only the topic, with no label, measure line, notes or source line.")
    return entry(
        "14.2", "Build every chart in one anatomy, from evidence label to table.",
        ["Every chart prints the same eight parts in the same order, so a reader always knows where to look: the evidence label and grade "
         "line (Rules 13.1 and 13.2), the title, the reading guide, the measure line (Rule 13.7), the chart, its notes, the source line "
         "(Rule 13.6) and the table (Rule 14.13).",
         "The title is one full sentence, and house rule H08 sizes its claim. The reading guide says in a sentence or two how to read the "
         "drawing. Notes carry what the drawing cannot. A part with nothing to say is left out, and the rest keep their order."],
        ["Readers learn where things are after a few charts. When every chart puts its source in the same place, a reader can check any "
         "figure in seconds, and a chart that lacks a part shows the gap."],
        [("Order", "Evidence label and grade line, title, reading guide, measure line, chart, notes, source line, table"),
         ("Evidence label", "On the chip fill, in the label style", "oa.chart.color.chip.fill.onNewsprint"),
         ("Title", "One full sentence in Inter Tight at the chart title size; its claim follows H08 and its verb Rule 13.2"),
         ("Reading guide", "One or two sentences, in the body style, only when the drawing needs one"),
         ("Measure line", "What is counted, the unit, the period and the place, under the title"),
         ("Table", "Every row the chart draws, folded under the source line as “The table and notes”")],
        ["13.1", "13.2", "13.6", "13.7", "14.13"],
        "Fill every word field of the spec under contract C2; the kit prints the parts in this order and leaves out an empty one.",
        B.plate("s-14-2-correct", "The eight parts in order, each numbered where the kit prints it. The table sits folded under the source line."),
        B.plate("s-14-2-failure", fails("14.2", "The title names a topic and states no finding, and the chart drops its label, measure line, "
                                                "notes and source line, so a reader cannot tell what was counted or who counted it.")),
        [ex("Civic and social organizations, employees, 1998 to 2023", "D10", where="14.2")],
        tokens=["oa.chart.color.chip.fill.onNewsprint"])


# ===============================================================================================================
# 14.3 Label the data directly
# ===============================================================================================================
AGES = [("18_to_24", "18 to 24"), ("25_to_44", "25 to 44"), ("45_to_64", "45 to 64"), ("65_and_over", "65 and over")]


def voting_by_age():
    out = {}
    for r in rows("census-cps-reported-voting"):
        if r["election_type"] == "presidential" and r["base"] == "citizen_voting_age_population" and r["age_group"] in dict(AGES):
            out.setdefault(r["age_group"], {})[int(r["year"])] = float(r["voted_pct"])
    return out


def rule_14_3(B):
    ds = "census-cps-reported-voting"
    v = voting_by_age()
    years = sorted(v["18_to_24"])
    need(years == [2004, 2008, 2012, 2016, 2020, 2024], f"the age series' years moved: {years}")
    for y in years:
        need(all(v["18_to_24"][y] + 10 < v[a][y] for a, _ in AGES[1:]), f"18 to 24 is not clearly lowest in {y}")
    title = "Citizens 18 to 24 reported voting at the lowest rate of four age groups in every presidential year from 2004 to 2024"
    B.spec("s-14-3-lines", form="line-event-notes", family="change-over-time", tier="core", dataset=ds,
           where={"election_type": "presidential", "base": "citizen_voting_age_population", "age_group": [a for a, _ in AGES]},
           reader_question="Which age groups report voting most and least?",
           evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau survey",
           title=title,
           measure_line="Share of citizens who reported voting, by age, in presidential years from 2004, the first with these age groups, "
                        "to 2024, United States",
           notes=["In every year the youngest group trails the next, citizens 25 to 44, by 11 to 16 points."],
           source_line=variant(ds, "source_line_citizen_only"),
           alt="Four lines of reported voting by age in presidential years from 2004 to 2024, each named at its end: 65 and over highest, "
               f"near 71 to 75 percent; 45 to 64 next; 25 to 44 below; and 18 to 24 lowest, from {fmt1(v['18_to_24'][2004])} percent in 2004 "
               f"to {fmt1(v['18_to_24'][2024])} percent in 2024.",
           table={"caption": "Share of citizens who reported voting, by age, percent",
                  "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                              {"field": "age_group", "label": "Age", "format": "text", "words": dict(AGES)},
                              {"field": "voted_pct", "label": "Reported voting", "format": "percent:1"}]},
           encode={"x": "year", "y": "voted_pct", "series": "age_group"},
           labels={"subject": "18_to_24", "series": dict(AGES),
                   "series_place": {"65_and_over": {"dy": -9}, "45_to_64": {"dy": 9}}},
           domain="D10", states=[], notes_internal="Rule 14.3's correct plate. Checked by script: 18 to 24 more than 10 points below every other "
                                                   "group in each year (gaps 11.2 to 16.1).")
    # the failure: the same four lines in the four group inks, with a key under the chart and no names on the lines
    W, H, L, R, T, Bt = 320, 236, 30, 312, 14, 170
    xs = scale(2004, 2024, L, R)
    ys = scale(40, 80, Bt, T)
    lines = "".join(f'<path class="ln g{i + 1} kl" d="{path([(xs(y), ys(v[a][y])) for y in years])}"/>' for i, (a, _) in enumerate(AGES))
    key = "".join(f'<line class="g{i + 1} kl" x1="{L + (i % 2) * 150}" x2="{L + (i % 2) * 150 + 22}" y1="{204 + (i // 2) * 22}" '
                  f'y2="{204 + (i // 2) * 22}"/><text x="{L + (i % 2) * 150 + 30}" y="{209 + (i // 2) * 22}">{e(n)}</text>'
                  for i, (_, n) in enumerate(AGES))
    inner = (axis_y(ys, [40, 60, 80], L, R, lambda t: f"{t}%") + axis_x(xs, [2004, 2014, 2024], Bt + 18, str) + lines + key)
    B.add("s-14-3-correct", chart("s-14-3-lines"),
          alt=f"Four lines of reported voting by age, each named at its last point. {title}.")
    B.add("s-14-3-failure", dnp() + tl(title)
          + f'<div class="art">{svg(W, H, inner, "sv g1")}</div>',
          alt=FC + "The same four lines in four inks with no names on them, and a key under the chart that the reader must match.")
    return entry(
        "14.3", "Label the data directly, and use a key only when labels cannot fit.",
        ["Rule 12.6 sets where a label sits. In a chart, each line takes its name at its last point, each bar its value at its end, and each "
         "group its name on or beside its marks, in the ink of the text. Units go once in the measure line, so the labels carry numbers alone.",
         "A key earns its place only when a mark codes something a label cannot carry on every mark, such as an evidence grade, a pattern or a "
         "run of shades. Then it sits under the measure line, in the order the marks run, as Rule 12.6 sets."],
        ["A reader matching inks between a key and the lines looks away from the data at every step, and close inks are hard to match at "
         "all in grayscale or with a color vision deficiency. A name at the end of each line is read in place."],
        [("A line", "Its name at its last point, in the label ink", "oa.chart.color.label.onNewsprint"),
         ("A bar", "Its value at its end, its name beside it"),
         ("Units", "Once, in the measure line"),
         ("A key", "Only for a code no label can carry, under the measure line, in the order the marks run (Rule 12.6)")],
        ["12.6", "13.7"],
        "Name each series in the spec's labels.series; the kit sets the names at the line ends and warns when one cannot fit.",
        B.plate("s-14-3-correct", "Each line carries its own name where it ends, so a reader reads the age group in place and the youngest "
                                  "group, which the title names, stands out in ink."),
        B.plate("s-14-3-failure", fails("14.3", "Four lines in four inks send the reader down to a key and back for every line, where a name "
                                                "at each line’s end would be read in place.")),
        [ex("Reported voting by age, presidential years 2004 to 2024", "D10", where="14.3")],
        tokens=["oa.chart.color.label.onNewsprint"])


# ===============================================================================================================
# 14.4 Zero, one scale, area
# ===============================================================================================================
def rule_14_4(B):
    ds = "census-cps-reported-voting"
    pres = {int(r["year"]): float(r["voted_pct"]) for r in rows(ds)
            if r["election_type"] == "presidential" and r["base"] == "citizen_voting_age_population" and r["age_group"] == "all"}
    years = sorted(pres)
    lo, hi = min(pres.values()), max(pres.values())
    y_lo, y_hi = min(pres, key=pres.get), max(pres, key=pres.get)
    title = (f"In every presidential year from {years[0]} to {years[-1]}, between {math.floor(lo)} and {math.ceil(hi)} percent of "
             f"citizens 18 and over reported voting")
    B.spec("s-14-4-cols", form="column", family="comparison", tier="core", dataset=ds,
           where={"election_type": "presidential", "base": "citizen_voting_age_population", "age_group": "all"},
           sort=[{"field": "year", "order": "asc"}],
           reader_question="How many citizens report voting in presidential years?",
           evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau survey",
           title=title,
           measure_line=f"Share of citizens 18 and over who reported voting, presidential years from {years[0]}, the first the survey counted "
                        f"citizens alone, to {years[-1]}, United States",
           source_line=variant(ds, "source_line_citizen_only"),
           alt=f"Columns from zero for each presidential year from {years[0]} to {years[-1]}, all of similar height, from {fmt1(lo)} percent in "
               f"{y_lo} to {fmt1(hi)} percent in {y_hi}.",
           table={"caption": "Share of citizens who reported voting, presidential years, percent",
                  "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                              {"field": "voted_pct", "label": "Reported voting", "format": "percent:1"}]},
           encode={"x": "year", "y": "voted_pct"}, formats={"value": "percent:0"},
           domain="D10", states=[], notes_internal=f"Rule 14.4's correct plate. Checked by script: lowest {lo} ({y_lo}), highest {hi} ({y_hi}).")
    # the failure: the same columns on an axis cut at 55, drawn here so the cut is the plate's own (the kit draws every bar from zero)
    cut = 55
    need(lo > cut + 2, "the cut axis no longer sits under every value")
    ratio = (hi - cut) / (lo - cut)
    W, H, L, R, T, Bt = 320, 210, 28, 314, 18, 178
    n = len(years)
    step = (R - L) / n
    ys = scale(cut, 70, Bt, T)
    bars = "".join(f'<rect class="{"s" if y == y_hi else "c"}" x="{L + i * step + 3:.1f}" y="{ys(pres[y]):.1f}" width="{step - 6:.1f}" '
                   f'height="{Bt - ys(pres[y]):.1f}"/>' for i, y in enumerate(years))
    lab = "".join(f'<text class="tk" x="{L + i * step + step / 2:.1f}" y="{Bt + 16}" text-anchor="middle">{"’" + str(y)[2:]}</text>'
                  for i, y in enumerate(years) if i % 2 == 0 or y == years[-1])
    inner = axis_y(ys, [55, 60, 65, 70], L, R, lambda t: f"{t}%") + bars + lab + f'<line class="ax" x1="{L}" x2="{R}" y1="{Bt}" y2="{Bt}"/>'
    B.add("s-14-4-correct", chart("s-14-4-cols"), alt=f"Columns from a zero line. {title}.")
    B.add("s-14-4-failure", dnp() + tl(title) + f'<div class="art">{svg(W, H, inner)}</div>',
          alt=FC + f"The same columns on an axis that starts at {cut} percent, so {y_hi}’s column stands {ratio:.1f} times as tall as {y_lo}’s.")
    return entry(
        "14.4", "Start bars and columns at zero, keep one scale per axis, and size circles by area.",
        ["Draw an amount at its true size. Bars and columns start at zero, because a reader compares their lengths. A line may start above "
         "zero when the change is the point, with the axis labeled where it starts.",
         "Each axis keeps one scale, so two measures take two panels side by side rather than a second axis on the right. A circle that "
         "stands for an amount takes its area from the value, so its radius grows with the square root of the value."],
        [f"Readers judge a bar by its length before they read its number. Cut the axis at {cut} percent and {y_hi}’s {fmt1(hi)} percent "
         f"stands {ratio:.1f} times as tall as {y_lo}’s {fmt1(lo)}, for a gap of {fmt1(hi - lo)} points."],
        [("Bars and columns", "From a zero line drawn at the baseline weight", "oa.chart.line.baseline"),
         ("A line", "May start above zero, with the axis labeled at its start"),
         ("Two measures", "Two panels on two scales, side by side"),
         ("Circles", "Area in proportion to the value, so the radius follows its square root")],
        ["14.23", "14.29"],
        "The kit draws every bar and column from zero and fails a circle not sized by area; scale may set a line’s range, never a bar’s.",
        B.plate("s-14-4-correct", "From zero, the columns stand close in height, as the shares do: a few points apart in every presidential year."),
        B.plate("s-14-4-failure", fails("14.4", f"The axis starts at {cut} percent, so {y_hi}’s column stands {ratio:.1f} times as tall as "
                                                f"{y_lo}’s for a gap of {fmt1(hi - lo)} points.")),
        [ex("Reported voting, citizens 18 and over, presidential years", "D10", where="14.4")],
        tokens=["oa.chart.line.baseline"])


# ===============================================================================================================
# 14.5 Each color one job
# ===============================================================================================================
def rule_14_5(B):
    pal = [("Sequential", "s1 s2 s3 s4 s5", "One measure from low to high, in five steps of Verdigris", "How high is the rate in each place?"),
           ("Diverging, pair B", "d1 d2 d3 d4 d5", "Above and below a midpoint, from Prussian through the page color to Verdigris, with an arrow "
                                                   "and a word for the direction (Rule 01.3)", "Which way did each value move, and how far?"),
           ("Groups", "c1 c2 c3 c4 hx", "Up to four named groups, in this order: Charcoal, Verdigris, Prussian, then Stone with its hatch",
            "How do these named groups compare?"),
           ("Magnitude", "m1 m2 m3 m4", "Size with no direction, in four steps of Stone", "How large is each amount?")]
    rws = []
    for name, sw, job, q in pal:
        cells = "".join(f'<i class="{c}{" hx c4" if c == "hx" else ""}"></i>' if c != "hx" else "" for c in sw.split())
        if "hx" in sw:
            cells = cells.replace('<i class="c4"></i>', '<i class="c4 hx"></i>')
        rws.append(f'<div class="row"><p class="nm">{e(name)}</p><div class="sw" aria-hidden="true">{cells}</div>'
                   f'<div><p class="jb">{e(job)}</p><p class="q">{e(q)}</p></div></div>')
    B.add("s-14-5-correct", f'<div class="pal">{"".join(rws)}</div>',
          alt="The four data palettes, each with its swatches, its one job and the question it answers: sequential Verdigris for one measure "
              "from low to high; diverging pair B from Prussian through the page color to Verdigris for values above and below a midpoint; "
              "four group inks, Charcoal, Verdigris, Prussian and hatched Stone, for named groups; and Stone steps for size with no direction.",
          readable=True, notes="Swatches drawn from the chart tokens the stage's surface class sets, so the strip follows Newsprint and Charcoal.")
    # the failure: four channels with no order, in four steps of one hue, with a key that reads as a scale (invented values)
    chans = [("Phone", 4120), ("Email", 3310), ("At the counter", 1880), ("Online form", 2540)]
    items = "".join(f'<li><span>{e(n)}</span><span class="bt"><i class="s{i + 2}" style="width:{100 * v / 4120:.1f}%"></i></span>'
                    f'<span class="v">{comma(v)}</span></li>' for i, (n, v) in enumerate(chans))
    keyw = "".join(f'<span><i class="kd s{i + 2}" style="border:0;border-radius:0"></i>{e(n)}</span>' for i, (n, _) in enumerate(chans))
    B.add("s-14-5-failure", dnp() + head("Illustration", None, "Phone calls were the most common way residents reached Alder County in 2026",
                                         illus="Illustrative data")
          + f'<div class="art sw"><p class="ky">{keyw}</p><ul class="sb">{items}</ul></div>',
          alt=FC + "An illustrative bar chart of four ways residents reached Alder County, each bar in a darker step of one green, with a key "
                   "that reads from light to dark as if the channels ran from less to more.",
          illustrative=True)
    return entry(
        "14.5", "Give each color in a chart one job from the four data palettes.",
        ["Each palette does one job, and a chart uses one palette for each thing its colors encode. Sequential Verdigris runs one measure "
         "from low to high. Diverging pair B runs above and below a midpoint, as Rule 01.3 sets. The four group inks name up to four groups, "
         "always in the order Charcoal, Verdigris, Prussian, then Stone, which carries its hatch. The Stone magnitude steps show size with "
         "no direction.",
         "Steps of one hue promise an order, so named groups take the group inks and a measure takes a scale. Rule 05.7 sets the subject, the "
         "context and the one red point inside any of them."],
        ["A reader takes a color’s meaning from the first chart and carries it to the next. When each palette keeps its one job across our "
         "work, a reader who has learned that a darker green means more can trust it on every page."],
        [("Sequential", "Five steps of Verdigris, light to dark for low to high", "oa.chart.color.sequential.fill.step1.onNewsprint"),
         ("Diverging, pair B", "Five steps, Prussian through the page color to Verdigris (Rule 01.3)", "oa.chart.color.diverging.fill.step1.onNewsprint"),
         ("Groups", "Charcoal, Verdigris, Prussian, Stone with its hatch, in that order; four at most (Rule 14.8)",
          "oa.chart.color.categorical.fill.group1.onNewsprint"),
         ("Magnitude", "Four steps of Stone", "oa.chart.color.magnitude.fill.step1.onNewsprint"),
         ("One chart", "One palette for each thing its colors encode")],
        ["01.3", "05.7", "14.8"],
        "Name a color role in the form (seq-1 to seq-5, div-1 to div-5, cat-1 to cat-4, mag-1 to mag-4); a spec never names a color.",
        B.plate("s-14-5-correct", "The four palettes, each beside its one job and the question it answers. The fourth group ink always "
                                  "carries its hatch, so it reads apart from the third in grayscale."),
        B.plate("s-14-5-failure", fails("14.5", "Four ways to reach the county take four steps of one green, so the key reads as a scale from "
                                                "less to more, though the channels have no order.")),
        [ex("Ways residents reached a county office, invented", "D04", level="county", where="14.5")],
        tokens=["oa.chart.color.sequential.fill.step1.onNewsprint", "oa.chart.color.diverging.fill.step1.onNewsprint",
                "oa.chart.color.categorical.fill.group1.onNewsprint", "oa.chart.color.magnitude.fill.step1.onNewsprint"])


# ===============================================================================================================
# 14.6 The view's one red on the point the title names
# ===============================================================================================================
def circuits():
    c = Counter(r["court_name"] for r in rows("fjc-article-iii-judges") if r["court_type"] == "U.S. Court of Appeals")
    short = lambda n: n.replace("U.S. Court of Appeals for the ", "").replace("District of Columbia Circuit", "D.C. Circuit")
    return sorted(((short(k), v) for k, v in c.items()), key=lambda t: (-t[1], t[0]))


def rule_14_6(B):
    ds = "fjc-article-iii-judges"
    data = circuits()
    need(len(data) == 13 and data[0] == ("Ninth Circuit", 29) and data[1][1] < 29, f"the circuit counts moved: {data[:2]}")
    total = sum(v for _, v in data)
    title = "The Ninth Circuit has 29 judges in active service, the most of the 13 federal courts of appeals"
    g = "Documented: the Federal Judicial Center’s directory of judges"
    measure = f"Judges in active service on each federal court of appeals, as of {words_date('2026-11-11')}"
    note = "Counts by court made by Oath & Action from the directory’s list; seats left empty are not counted."
    tab = table("Judges in active service, by court of appeals", ["Court", "Judges"], [(n, v) for n, v in data])
    B.add("s-14-6-correct", head("Finding", g, title, measure=measure)
          + f'<div class="art">{hbars(data, 30, str, point=("Ninth Circuit",))}</div>' + foot([note], src(ds)) + tab,
          alt=f"Bars of active judges on the 13 federal courts of appeals, the Ninth Circuit’s in red with a dark edge and the rest in gray: "
              f"{', '.join(f'{n} {v}' for n, v in data)}.",
          notes="Drawn here from the directory's rows, counted by script, until the kit takes a red point by name (request ED-E1).")
    reds = ("Ninth Circuit", "Fifth Circuit", "Sixth Circuit")
    B.add("s-14-6-failure", dnp() + tl(title)
          + f'<div class="art">{hbars(data, 30, str, point=reds, red=reds)}</div>',
          alt=FC + "The same bars with three courts in red, the Ninth, Fifth and Sixth Circuits, under a title that names one.")
    return entry(
        "14.6", "Spend the view’s one red on the point the title names.",
        ["Rule 05.3 gives each view one working red and says which job claims it first. In a chart, the red goes to the one point, bar or "
         "line the title names, inside the 1 px Charcoal keyline of Rule 05.5, and that mark carries its own label. Every other mark keeps "
         "the subject and context inks of Rule 05.7.",
         "When an error or a step the reader can take already holds the view’s red, the named point gives it up and takes Charcoal at the "
         "subject weight, with its label. Red never codes a series, a group or a step on a scale."],
        ["One red mark tells a reader where to look first, and the title tells them why. A second red mark splits their attention, and red "
         "that codes a group reads as a warning about that group."],
        [("The point", "Pillar Red with a 1 px Charcoal keyline", "oa.chart.color.point.onNewsprint"),
         ("Its label", "Beside the mark, in the text ink"),
         ("When red is taken", "Charcoal at the subject weight, with the label", "oa.chart.color.subject.onNewsprint"),
         ("Red never", "Codes a series, a group or a step on a scale")],
        ["05.3", "05.5", "05.7", "01.1"],
        "Name the one point in the spec (labels.named for the subject ink); the kit counts working reds and fails a view with two.",
        B.plate("s-14-6-correct", "The title names the Ninth Circuit, and its bar alone takes the view’s red, inside its keyline, with every "
                                  "other court in gray."),
        B.plate("s-14-6-failure", fails("14.6", "Red falls on three courts while the title names one, so a reader cannot tell which bar the "
                                                "title means.")),
        [ex("Active judges by federal court of appeals, November 11, 2026", "D05", where="14.6")],
        tokens=["oa.chart.color.point.onNewsprint", "oa.chart.color.subject.onNewsprint"])


# ===============================================================================================================
# 14.7 Parties by name, position and shape
# ===============================================================================================================
def rule_14_7(B):
    ds = "clerk-house-current-party-breakdown"
    d = {r["party"]: int(r["seats"]) for r in rows(ds)}
    need(d == {"Republicans": 218, "Democrats": 214, "Independents": 1, "Vacancies": 2}, f"the House breakdown moved: {d}")
    title = "Republicans held 218 House seats and Democrats 214 on November 11, 2026, with one independent and two seats empty"
    B.spec("s-14-7-seats", form="ranked-bar", family="comparison", tier="core", dataset=ds,
           reader_question="How many House seats does each party hold?",
           evidence="finding", evidence_label="Finding", grade_line="Documented: the House Clerk’s record",
           title=title, measure_line="Seats in the U.S. House of Representatives, by party, as of November 11, 2026",
           source_line=src(ds),
           alt="Four bars in one dark ink, each named: Republicans 218, Democrats 214, Independents 1, Vacancies 2.",
           table={"caption": "House seats by party, November 11, 2026",
                  "columns": [{"field": "party", "label": "Party", "format": "text", "row_header": True},
                              {"field": "seats", "label": "Seats", "format": "integer"}]},
           encode={"category": "party", "value": "seats"}, domain="D02", states=[],
           notes_internal="Rule 14.7's correct plate: every party in the subject ink, named on its bar (Rule 01.2).")
    # the failure: red and blue, the names moved to a key
    W, H = 320, 150
    xs = scale(0, 230, 40, 300)
    inner = (f'<rect class="rd" data-red="failure" x="40" y="14" width="{xs(218) - 40:.1f}" height="26"/>'
             f'<rect class="bl" x="40" y="50" width="{xs(214) - 40:.1f}" height="26"/>'
             f'<text x="34" y="32" text-anchor="end">R</text><text x="34" y="68" text-anchor="end">D</text>'
             f'<text x="{xs(218) + 6:.1f}" y="32">218</text><text x="{xs(214) + 6:.1f}" y="68">214</text>'
             f'<rect class="rd" data-red="failure" x="40" y="104" width="14" height="14"/><text x="60" y="116">R</text>'
             f'<rect class="bl" x="100" y="104" width="14" height="14"/><text x="120" y="116">D</text>'
             f'<line class="ax" x1="40" x2="40" y1="8" y2="84"/>')
    B.add("s-14-7-correct", chart("s-14-7-seats"), alt=f"Bars in one ink with each party named on its bar. {title}.")
    B.add("s-14-7-failure", dnp() + tl(title)
          + f'<div class="art">{svg(W, H, inner, "sv rb")}</div>',
          alt=FC + "Two bars, a red one marked R at 218 and a blue one marked D at 214, with a key of a red square for R and a blue square for D.")
    return entry(
        "14.7", "Tell parties apart by name, place and shape, with no red and blue.",
        ["Rule 01.2 draws every party in one neutral ink with its name on the mark, and Rule 01.1 keeps red off every party. A chart then "
         "tells parties apart by what a reader can read without color: the name on or beside each mark, the mark’s place in the order, a "
         "solid and an open mark where two sides sit side by side, and a word or sign for direction, as in “Republican +2.2”.",
         "No election graphic pairs red with blue, social cards included, and Prussian never stands for a party."],
        ["Red and blue turn a chart of results into team colors, and a reader decides which side the chart is on before reading a number. "
         "A name on each mark gives readers on both sides the same facts, in color or in grayscale."],
        [("Party marks", "One neutral ink for every party, Charcoal on Newsprint", "oa.chart.color.party.mark.onNewsprint"),
         ("Two sides at a glance", "One solid and one open mark, in the same ink (Rule 01.2)"),
         ("Direction", "An arrow, the mark’s place or a printed lead, such as “Republican +2.2”"),
         ("Never", "Red against blue, or Prussian for a party")],
        ["01.1", "01.2", "05.7"],
        "Party data takes the party role in any form; the kit fails a party mark in Pillar Red or Prussian.",
        B.plate("s-14-7-correct", "Every party takes the same ink and its name, so the bars compare seats and nothing else."),
        B.plate("s-14-7-failure", fails("14.7", "Red and blue stand for the parties and a key holds their initials, so the chart reads as one "
                                                "team against another and loses the parties in grayscale.")),
        [ex("House seats by party, November 11, 2026", "D02", where="14.7")],
        tokens=["oa.chart.color.party.mark.onNewsprint"])


# ===============================================================================================================
# 14.8 Past four groups
# ===============================================================================================================
OWN_AGES = ["Less than 35 years", "35 to 44 years", "45 to 54 years", "55 to 64 years", "65 years and over"]
OWN_NAMES = {"Less than 35 years": "Under 35", "35 to 44 years": "35 to 44", "45 to 54 years": "45 to 54",
             "55 to 64 years": "55 to 64", "65 years and over": "65 and over"}


def ownership():
    out = {}
    for r in rows("census-hvs-homeownership-by-age"):
        if r["grouping"] == "summary" and not r["series_variant"] and r["age_group"] in OWN_AGES:
            out.setdefault(r["age_group"], {})[int(r["year"])] = float(r["rate_pct"])
    return out


def rule_14_8(B):
    ds = "census-hvs-homeownership-by-age"
    o = ownership()
    years = sorted(set.intersection(*(set(v) for v in o.values())))
    y0, y1 = years[0], years[-1]
    need(all(o["Less than 35 years"][y] + 15 < o[a][y] for y in years for a in OWN_AGES[1:]), "under 35 is not clearly lowest every year")
    title = f"Householders under 35 were the least likely to own their homes in every year from {y0} to {y1}"
    B.spec("s-14-8-panels", form="multi-line-highlight", family="change-over-time", tier="core", dataset=ds,
           where={"grouping": "summary", "age_group": OWN_AGES, "series_variant": {"not": ["revised_1990_census", "revised_2000_census"]}},
           reader_question="How does homeownership differ by age, and has that changed?",
           evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau survey",
           title=title,
           reading_guide="Each panel draws one age group in ink over the other four in gray, on one shared scale.",
           measure_line=f"Share of households that own their home, by the householder’s age, each year from {y0} to {y1}, United States",
           source_line=src(ds),
           alt=f"Five small panels of homeownership by age from {y0} to {y1}, one group in ink in each: under 35 lowest, near "
               f"{round(o['Less than 35 years'][y1])} percent in {y1}; 65 and over highest, near {round(o['65 years and over'][y1])} percent.",
           table={"caption": "Share of households that own their home, by age of householder, percent",
                  "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                              {"field": "age_group", "label": "Age", "format": "text", "words": OWN_NAMES},
                              {"field": "rate_pct", "label": "Own their home", "format": "percent:1"}]},
           encode={"x": "year", "y": "rate_pct", "series": "age_group"},
           labels={"panels": [{"value": a, "label": OWN_NAMES[a]} for a in OWN_AGES], "columns": 5},
           domain="D09", states=[], notes_internal="Rule 14.8's correct plate. Checked by script: under 35 lowest by more than 15 points every year.")
    # the failure: five lines in five inks with a key, one ink borrowed from the sequential scale
    W, H, L, R, T, Bt = 320, 250, 30, 312, 14, 170
    xs = scale(y0, y1, L, R)
    ys = scale(20, 90, Bt, T)
    lines = "".join(f'<path class="ln g{i + 1}" d="{path([(xs(y), ys(o[a][y])) for y in years])}"/>' for i, a in enumerate(OWN_AGES))
    key = "".join(f'<line class="g{i + 1} kl" x1="{L + (i % 3) * 96}" x2="{L + (i % 3) * 96 + 18}" y1="{204 + (i // 3) * 22}" '
                  f'y2="{204 + (i // 3) * 22}"/><text x="{L + (i % 3) * 96 + 24}" y="{209 + (i // 3) * 22}">{e(OWN_NAMES[a])}</text>'
                  for i, a in enumerate(OWN_AGES))
    inner = axis_y(ys, [20, 50, 80], L, R, lambda t: f"{t}%") + axis_x(xs, [y0, y1], Bt + 18, str) + lines + key
    B.add("s-14-8-correct", chart("s-14-8-panels"), alt=f"Five small panels, one age group in ink in each over the rest in gray. {title}.")
    B.add("s-14-8-failure", dnp() + tl(title)
          + f'<div class="art">{svg(W, H, inner, "sv g1")}</div>',
          alt=FC + "The same five age groups as five lines in five inks on one plot, the fifth ink borrowed from a scale, with a key of five "
                   "short lines under the chart.")
    return entry(
        "14.8", "Past four groups, split into small multiples or set one group in ink against gray.",
        ["The four group inks of Rule 14.5 are as many as a reader can tell apart and hold in mind. With five or more groups, draw one small "
         "panel for each on a shared scale, or draw the group the title names in ink and the others in gray. Either way, every group carries "
         "its name on the chart.",
         "Rule 14.23 shows small multiples of bars, Rule 14.30 small multiples of lines, and Rule 14.31 one line in ink over a field of gray."],
        ["Past four, the inks start to look alike and the key grows longer than a reader will hold. Small panels on one scale let a reader "
         "take each group’s shape and level one at a time, and still compare them."],
        [("Groups in color", "Four at most, in Rule 14.5’s order"),
         ("Five or more", "Small multiples on one shared scale, or one group in ink and the rest in gray",
          "oa.chart.color.context.onNewsprint"),
         ("Names", "Every group named on the chart, in its panel or at its line’s end")],
        ["14.5", "14.23", "14.30", "14.31"],
        "Use multi-line-highlight or small-multiple-bars for five or more groups; the kit fails a key of more than four inks.",
        B.plate("s-14-8-correct", "Each panel sets one age group in ink against the other four in gray, on one scale, so a reader compares "
                                  "five groups without a key."),
        B.plate("s-14-8-failure", fails("14.8", "Five groups take five inks, the fifth borrowed from a scale, and the key under the plot asks "
                                                "the reader to match each one.")),
        [ex("Homeownership by age of householder", "D09", where="14.8")],
        tokens=["oa.chart.color.context.onNewsprint"])


# ===============================================================================================================
# 14.9 Uncertainty, and ranks only past the margin of error
# ===============================================================================================================
def turnout10():
    rs = [r for r in rows("census-cps-2024-turnout-by-state") if r["year"] == "2024"]
    nat = [r for r in rs if r["code"] == "US"][0]
    st = sorted([r for r in rs if r["code"] != "US"], key=lambda r: -int(r["citizen_vap_thousands"]))[:10]
    n, nm = float(nat["voted_pct"]), float(nat["moe_pct"])
    out = []
    for r in st:
        v, m = float(r["voted_pct"]), float(r["moe_pct"])
        gm = math.sqrt(m * m + nm * nm)
        out.append({"code": r["code"], "name": r["name"], "v": v, "m": m, "gap": v - n, "gm": gm, "past": abs(v - n) > gm})
    return n, nm, out


def rule_14_9(B):
    ds = "census-cps-2024-turnout-by-state"
    n, nm, st = turnout10()
    past = [s for s in st if s["past"]]
    need(len(past) == 5 and n == 65.3, f"the turnout comparison moved: {len(past)} past, nation {n}")
    by = sorted(st, key=lambda s: -s["v"])
    mi, pa, ny, tx = by[0], by[1], by[-2], by[-1]
    need((mi["code"], pa["code"], ny["code"], tx["code"]) == ("MI", "PA", "NY", "TX"), "the ranked ends moved")
    gm_top = math.sqrt(mi["m"] ** 2 + pa["m"] ** 2)
    gm_bot = math.sqrt(ny["m"] ** 2 + tx["m"] ** 2)
    need(mi["v"] - pa["v"] < gm_top and ny["v"] - tx["v"] < gm_bot, "the ranked ends now pass their margins")
    title = "Five of the ten states with the most voting-age citizens differed from the nation’s 65.3 percent turnout by more than the margin of error"
    g = "Documented: a Census Bureau survey"
    measure = "Share of citizens 18 and over who reported voting, November 2024, the ten states with the most voting-age citizens"
    lo, hi = 50, 80
    pos = lambda v: 100 * (v - lo) / (hi - lo)
    li = ['<li class="hd"><span></span><span class="tk">' + f'<span class="ref" style="left:{pos(n):.2f}%"></span>'
          + f'<span style="position:relative;left:{pos(n):.2f}%;margin-left:4px">Nation 65.3%</span></span><span></span></li>']
    for s in by:
        li.append(f'<li><span>{e(s["name"])}</span><span class="tk"><span class="ref" style="left:{pos(n):.2f}%"></span>'
                  f'<span class="iv" style="left:{pos(s["v"] - s["m"]):.2f}%;width:{pos(s["v"] + s["m"]) - pos(s["v"] - s["m"]):.2f}%"></span>'
                  f'<span class="dt{"" if s["past"] else " o"}" style="left:{pos(s["v"]):.2f}%"></span></span>'
                  f'<span class="v">{fmt1(s["v"])}%</span></li>')
    keyw = ('<p class="ky"><span><i class="kd"></i>Differs from the nation by more than the margin</span>'
            '<span><i class="kd o"></i>Within the margin of error</span></p>')
    notes = ["Each line spans a state’s margin of error at 90 percent confidence. A gap counts only past the margin of the gap itself, "
             "the square root of the sum of the two squared margins."]
    tab = table("Reported voting, November 2024, percent", ["State", "Reported voting", "Margin of error", "Gap from the nation"],
                [(s["name"], fmt1(s["v"]), "±" + fmt1(s["m"]), (fmt1(s["gap"]) if s["gap"] < 0 else "+" + fmt1(s["gap"]))
                  + (" past" if s["past"] else " within")) for s in by])
    B.add("s-14-9-correct", head("Finding", g, title, measure=measure) + f'<div class="art">{keyw}<ul class="di">{"".join(li)}</ul></div>'
          + foot(notes, variant(ds, "source_line_2024_only")) + tab,
          alt=f"Dots with margin of error lines for ten states’ reported turnout in 2024, against a dashed line at the nation’s 65.3 percent. "
              f"Filled dots, past the margin: {', '.join(s['name'] for s in by if s['past'])}. Open dots, within it: "
              f"{', '.join(s['name'] for s in by if not s['past'])}.",
          notes="Drawn here from the turnout file with each gap's margin computed by script, until the kit's interval form lands (round 2).")
    rk = "".join(f'<li><span class="r">{i + 1}</span><span>{e(s["name"])}</span><span class="v">{fmt1(s["v"])}%</span></li>'
                 for i, s in enumerate(by))
    B.add("s-14-9-failure", dnp() + tl("Michigan led the ten largest states in reported turnout in 2024, and Texas came last") + f'<div class="art"><ol class="rk">{rk}</ol></div>',
          alt=FC + "The ten states ranked 1 to 10 by reported turnout, Michigan first at 72.3 percent and Texas tenth at 57.9 percent, with no "
                   "margins of error.")
    return entry(
        "14.9", "Show the publisher’s uncertainty, and rank only where a gap passes the margin of error.",
        ["Rule 13.5 draws a survey figure’s margin of error as an interval. A chart that ranks survey figures, or singles one out as higher or "
         "lower than another, does so only where the gap between them passes the gap’s own margin of error at the publisher’s stated "
         "confidence, and a note says so. Figures whose gaps sit inside it are drawn and described as alike: an open dot, a shared place, or "
         "the words “within the margin of error”.",
         "A count of every case, such as votes cast or seats held, has no sampling margin and ranks as it stands."],
        ["A survey measures a sample, so each figure could sit anywhere in its interval. Two states three points apart, each with a margin "
         "near three points, may stand in either order across the whole population, and a ranking that puts one first tells a reader "
         "something the survey cannot know."],
        [("Interval", "The publisher’s margin of error at its stated confidence, a line through the dot", "oa.chart.color.context.onNewsprint"),
         ("A gap’s margin", "For two independent survey figures, the square root of the sum of their squared margins"),
         ("Within the margin", "An open dot and the words “within the margin of error”"),
         ("Counts", "No sampling margin; they rank as they stand")],
        ["13.5", "13.1"],
        "Carry each figure’s margin in its own column of the data; a form draws the interval from it and the note names the confidence.",
        B.plate("s-14-9-correct", "Each state’s line shows its margin of error. Five states sit past the margin from the nation and take a "
                                  "filled dot; the five within it take an open one, and the chart ranks none of them."),
        B.plate("s-14-9-failure", fails("14.9", f"The ranks put Michigan first and Texas last, but Michigan’s lead over Pennsylvania, "
                                                f"{fmt1(mi['v'] - pa['v'])} points, and Texas’s gap below New York, {fmt1(ny['v'] - tx['v'])} points, "
                                                f"both sit inside the margin of error, so the survey cannot order them.")),
        [ex("Reported turnout, ten states with the most voting-age citizens, 2024", "D10", states=[s["code"] for s in st], level="state",
            where="14.9")],
        tokens=["oa.chart.color.context.onNewsprint"])


# ===============================================================================================================
# 14.10 The window and the inauguration
# ===============================================================================================================
TERMS = [(2001, "Bush"), (2009, "Obama"), (2017, "Trump"), (2021, "Biden")]


def rule_14_10(B):
    ds = "census-cbp-newspaper-publishers"
    r = {int(x["year"]): int(x["establishments"]) for x in rows(ds)}
    need(min(r) == 1998 and max(r) == 2023, "the newspaper series moved")
    ends = [t for t, _ in TERMS] + [2023]
    need(all(r[a] > r[b] for a, b in zip(ends, ends[1:])), "newspaper establishments did not fall across every term")
    title = f"Newspaper publishers ran {comma(r[2023])} establishments in 2023, down from {comma(r[1998])} in 1998"
    B.spec("s-14-10-line", form="line-event-notes", family="change-over-time", tier="core", dataset=ds,
           reader_question="How many newspaper publishers are left, and how has that changed?",
           evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau count of employers",
           title=title,
           measure_line="Newspaper publishers’ establishments with paid employees, each year from 1998, the first year the Census Bureau "
                        "counted them under today’s industry codes, to 2023, the latest it has published, United States",
           source_line=src(ds),
           alt=f"An unbroken line of newspaper publishers’ establishments from 1998 to 2023, falling from {comma(r[1998])} to {comma(r[2023])}.",
           table={"caption": "Newspaper publishers’ establishments with paid employees",
                  "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                              {"field": "establishments", "label": "Establishments", "format": "integer"}]},
           encode={"x": "year", "y": "establishments"}, domain="D01", states=[],
           notes_internal="Rule 14.10's correct plate: the window's reason in the measure line, one unbroken line.")
    # the failure: bands at each inauguration, named for each president
    W, H, L, R, T, Bt = 320, 210, 34, 312, 30, 178
    xs = scale(1998, 2023, L, R)
    ys = scale(0, 10000, Bt, T)
    bands = "".join(f'<rect class="bd" x="{xs(a):.1f}" y="{T - 18}" width="{xs(b) - xs(a):.1f}" height="{Bt - T + 18}"/>'
                    for i, ((a, _), b) in enumerate(zip(TERMS, [t for t, _ in TERMS[1:]] + [2023])) if i % 2 == 0)
    names = "".join(f'<text class="tk" x="{xs(a) + 3:.1f}" y="{T - 6}">{e(nm)}</text>' for a, nm in TERMS)
    pts = sorted(r.items())
    line = "".join(f'<path class="ln" d="{path([(xs(y), ys(v)) for y, v in pts if a <= y <= b])}"/>'
                   for a, b in zip([1998] + [t for t, _ in TERMS], [t for t, _ in TERMS] + [2023]))
    inner = (bands + axis_y(ys, [0, 5000, 10000], L, R, comma) + axis_x(xs, [1998, 2023], Bt + 18, str) + names + line
             + f'<line class="ax" x1="{L}" x2="{R}" y1="{Bt}" y2="{Bt}"/>')
    B.add("s-14-10-correct", chart("s-14-10-line"), alt=f"An unbroken line with its window’s reason in the measure line. {title}.")
    B.add("s-14-10-failure", dnp() + tl(title)
          + f'<div class="art">{svg(W, H, inner, "sv band")}</div>',
          alt=FC + "The same line cut into four presidential terms by shaded bands at each inauguration, each band named for a president.")
    return entry(
        "14.10", "Choose the window from the question, and draw an inauguration only as a dated note.",
        ["Choose the window, the first and last period a chart shows, from the reader’s question, and print its reason in the measure line: "
         "the first year a series exists, the first year a method holds, or the span the question names. Rule 13.7 gives charts shown "
         "together one window.",
         "An inauguration or an election may appear inside the window as a dated note on an unbroken line. The line keeps one ink and one "
         "weight across the date, and no band, color or break divides the period into one officeholder’s years and another’s (house rule H09)."],
        ["A window that starts where a line looks best can make a long fall look like a rise, and a reader cannot see what was left out. "
         "Bands at each inauguration ask the reader to credit or blame each officeholder for whatever the line does inside them, which the "
         "chart cannot show."],
        [("Window", "From the question, its reason printed in the measure line"),
         ("Charts shown together", "One window, printed once (Rule 13.7)"),
         ("An event", "A dated note with a leader, on an unbroken line", "oa.chart.color.leader.onNewsprint"),
         ("An inauguration", "No band, color change or break at the date (H09)")],
        ["13.7", "14.29"],
        "Put the window's reason in measure_line and any event in annotations; the kit draws one line with no band.",
        B.plate("s-14-10-correct", "The window runs from the first year these industry codes allow to the latest count, and the measure line "
                                   "says so. The line runs unbroken across every inauguration in it."),
        B.plate("s-14-10-failure", fails("14.10", "Bands at each inauguration cut a 25-year fall into four presidencies, so the drawing invites "
                                                  "a reader to credit or blame each president for a decline that runs through all four terms.")),
        [ex("Newspaper publishers’ establishments, 1998 to 2023", "D01", where="14.10")],
        tokens=["oa.chart.color.leader.onNewsprint"])


# ===============================================================================================================
# 14.11 Gaps, breaks and preliminary values
# ===============================================================================================================
def rule_14_11(B):
    ds = "census-cps-median-household-income"
    rs = rows(ds)
    m = sidecar(ds)
    seg_key = lambda r: (0 if int(r["year"]) < 2013 or (r["year"] == "2013" and "7" in r["footnotes"].split()) else
                         1 if int(r["year"]) < 2017 or (r["year"] == "2017" and not r["footnotes"].strip()) else 2)
    segs = [sorted(((int(r["year"]), int(r["median_income"])) for r in rs if seg_key(r) == k)) for k in range(3)]
    need(segs[0][-1] == (2013, 69470) and segs[1][0] == (2013, 71670) and segs[1][-1] == (2017, 78900) and segs[2][0] == (2017, 78600),
         "the two breaks moved")
    last = segs[2][-1]
    need(last == (2025, 87460), f"the 2025 median moved: {last}")
    moe = [int(r["median_moe"]) for r in rs if r["year"] == "2025"][0]
    title = f"Median household income stood at ${comma(last[1])} in 2025, in 2025 dollars"
    g = "Documented: a Census Bureau survey"
    measure = "Median household income in 2025 dollars, each year from 1967, the first in the Census Bureau’s series, to 2025, United States"
    W, H, L, R, T, Bt = 320, 220, 46, 312, 16, 184
    xs = scale(1967, 2025, L, R)
    ys = scale(50000, 90000, Bt, T)
    lines = "".join(f'<path class="ln" d="{path([(xs(y), ys(v)) for y, v in s])}"/>' for s in segs)
    dots = "".join(f'<circle class="{c}" cx="{xs(y):.1f}" cy="{ys(v):.1f}" r="3.5"/>'
                   for (y, v), c in [(segs[0][-1], "o"), (segs[1][0], "s"), (segs[1][-1], "o"), (segs[2][0], "s")])
    notes_svg = (f'<line class="ld" x1="{xs(2013):.1f}" x2="{xs(2013):.1f}" y1="{ys(71670) - 6:.1f}" y2="{T + 46}"/>'
                 f'<text x="{xs(2013) - 4:.1f}" y="{T + 30}" text-anchor="end">2013: new</text>'
                 f'<text x="{xs(2013) - 4:.1f}" y="{T + 44}" text-anchor="end">questions</text>')
    inner = (axis_y(ys, [50000, 70000, 90000], L, R, lambda t: f"${t // 1000},000") + axis_x(xs, [1967, 1995, 2025], Bt + 18, str)
             + lines + dots + notes_svg)
    notes = ["The line breaks twice where the survey changed. In 2013 it asked new income questions, and in 2017 it moved to a new "
             "processing system; each year prints both its estimates, the old method’s as an open dot and the new one’s filled.",
             f"The 2025 figure carries a margin of error of ±${comma(moe)} at 90 percent confidence."]
    tab = table("Median household income, 2025 dollars, the years with two estimates", ["Year and method", "Median income"],
                [("2013, earlier questions", f"${comma(69470)}"), ("2013, new questions", f"${comma(71670)}"),
                 ("2017, earlier processing", f"${comma(78900)}"), ("2017, new processing", f"${comma(78600)}"),
                 ("2025", f"${comma(last[1])}")])
    B.add("s-14-11-correct", head("Finding", g, title, measure=measure) + f'<div class="art">{svg(W, H, inner)}</div>'
          + foot(notes, src(ds)) + tab,
          alt=f"A line of median household income from 1967 to 2025 in 2025 dollars, broken at 2013 and 2017 where the survey changed, with "
              f"both estimates printed in each of those years; it ends at ${comma(last[1])} in 2025.",
          notes="Drawn here from the Census Bureau's table, segments split by its footnotes 6 and 7 (2013) and 5 (2017).")
    allpts = sorted(((int(r["year"]), int(r["median_income"]), seg_key(r)) for r in rs), key=lambda t: (t[0], t[2]))
    bad = f'<path class="ln" d="{path([(xs(y), ys(v)) for y, v, _ in allpts])}"/>'
    inner2 = axis_y(ys, [50000, 70000, 90000], L, R, lambda t: f"${t // 1000},000") + axis_x(xs, [1967, 1995, 2025], Bt + 18, str) + bad
    B.add("s-14-11-failure", dnp() + tl(title) + f'<div class="art">{svg(W, H, inner2)}</div>',
          alt=FC + "The same income series as one line run through both estimates for 2013 and both for 2017, so each change in the survey "
                   "draws as a sudden step in income.")
    return entry(
        "14.11", "Mark a gap, a break in a series or a preliminary value in the drawing.",
        ["Draw what the data lacks or changes where it happens. A month or year with no figure leaves a gap in the line, and the line never "
         "bridges it. Where a publisher changes its method, the line breaks, the year prints both estimates, and a note says what changed. "
         "A preliminary value takes an open mark and the word preliminary beside it, and the qualification names it (Rule 13.7)."],
        ["A line drawn through a missing month invents a value, and a line run across a change of method shows the change as a jump in "
         "what was measured. Marking each one where it falls lets a reader see what the data can and cannot say."],
        [("No figure", "A gap in the line, with a note that says why"),
         ("A change of method", "A break, both estimates printed, a note that names the change", "oa.chart.color.leader.onNewsprint"),
         ("Preliminary", "An open mark and the word preliminary; the qualification names it (Rule 13.7)")],
        ["13.7", "14.37", "14.32"],
        "Mark breaks in the data's break column and preliminary rows in its status column; the kit leaves the gap and opens the mark.",
        B.plate("s-14-11-correct", "The line breaks where the survey changed, and each of those years prints both its estimates, so a "
                                   "change of method never reads as a change in income."),
        B.plate("s-14-11-failure", fails("14.11", "One line runs through both of 2013’s estimates and both of 2017’s, so a change in the "
                                                  "survey’s questions draws as a jump in income.")),
        [ex("Median household income, 1967 to 2025", "D08", where="14.11")],
        tokens=["oa.chart.color.leader.onNewsprint"])


# ===============================================================================================================
# 14.12 The phone drawing
# ===============================================================================================================
SOURCE_NAMES = {"Individual Income Taxes": "Individual income taxes", "Employment and General Retirement": "Payroll taxes for Social Security and Medicare",
                "Corporation Income Taxes": "Corporate income taxes", "Customs Duties": "Customs duties", "Excise Taxes": "Excise taxes",
                "Unemployment Insurance": "Unemployment insurance", "Miscellaneous Receipts": "Other receipts", "Estate and Gift Taxes": "Estate and gift taxes",
                "Other Retirement": "Other retirement"}


def receipts():
    rs = [r for r in rows("treasury-mts-receipts-by-source") if r["fiscal_year"] == "2026"]
    tot = [float(r["receipts_dollars"]) for r in rs if r["source"] == "Total"][0]
    parts = sorted(((SOURCE_NAMES[r["source"]], float(r["receipts_dollars"]) / 1e9) for r in rs if r["source"] != "Total"), key=lambda t: -t[1])
    need(abs(sum(v for _, v in parts) - tot / 1e9) < 1, "the receipts no longer add up to the total")
    return parts, tot / 1e9


def rule_14_12(B):
    ds = "treasury-mts-receipts-by-source"
    parts, tot = receipts()
    need(parts[0][0] == "Individual income taxes" and round(parts[0][1] / 1000, 2) == 2.85 and round(tot / 1000, 2) == 5.40, "the receipts moved")
    title = "Individual income taxes brought in $2.85 trillion of the $5.40 trillion the federal government collected in fiscal year 2026"
    g = "Documented: the Treasury’s monthly statement"
    measure = "Federal receipts by source, billions of dollars, fiscal year 2026, October 1, 2025 to September 30, 2026"
    vmax = parts[0][1]
    cols = "".join(f'<div class="c{" s" if i == 0 else ""}"><b>{comma(v)}</b><i style="height:{max(1.0, 100 * v / vmax * 0.82):.1f}%"></i></div>'
                   for i, (_, v) in enumerate(parts))
    names = "".join(f"<span>{e(n)}</span>" for n, _ in parts)
    desk = f'<div class="fr"><p class="fh">At full width</p><div class="cl">{cols}</div><div class="cn">{names}</div></div>'
    phone = (f'<div class="fr ph"><p class="fh">On a phone, 358 px</p>'
             + hbars([(n, v) for n, v in parts], vmax * 1.02, comma, subject=("Individual income taxes",)) + "</div>")
    tab = table("Federal receipts by source, fiscal year 2026, billions of dollars", ["Source", "Billions of dollars"],
                [(n, comma(v)) for n, v in parts] + [("Total", comma(tot))])
    B.add("s-14-12-correct", head("Finding", g, title, measure=measure) + f'<div class="art two">{desk}{phone}</div>' + foot([], src(ds)) + tab,
          alt=f"The same nine sources of federal receipts drawn twice: as columns at full width, with names under each column, and as bars on a "
              f"phone, with each name beside its bar. Both show individual income taxes largest at {comma(parts[0][1])} billion dollars of "
              f"{comma(tot)} billion.",
          notes="The two drawings side by side, drawn here from the Treasury file, so the plate shows both widths at once.")
    top3 = parts[:3]
    B.add("s-14-12-failure", dnp() + f'<div class="fr ph"><p class="fh">On a phone, 358 px</p>'
          + head("Finding", g, "Income and payroll taxes pay for the federal government", measure=measure)
          + f'<div class="art">{hbars(top3, vmax * 1.02, comma, subject=("Individual income taxes",))}</div></div>',
          alt=FC + "A phone version of the receipts chart that keeps three of nine sources and gives them a new title, “Income and payroll taxes "
                   "pay for the federal government”.")
    return entry(
        "14.12", "Redraw for a phone only when the form must change, and keep the data and finding.",
        ["Draw a chart once for every width when its form still reads at 358 px. Change the form for a phone only when it must: when labels "
         "would fall under 13 px (Rule 06.3), when columns grow too narrow to carry their names, or when arrows grow too short to read. "
         "Columns then become bars, and a map of arrows becomes a list.",
         "The phone drawing keeps every row, the title, the finding and the source line, and a note under the drawing carries any words that "
         "leave the plot."],
        ["Many readers meet our charts on a phone first. A drawing redrawn for no reason gives them a second picture to learn, and one that "
         "drops rows or changes its title gives phone readers a different finding from everyone else."],
        [("Phone width", "358 px, the narrowest drawing the kit checks above 296 px", "oa.chart.artboard.phone"),
         ("Same form", "When every label and mark reads at that width"),
         ("A new form", "Columns as bars, arrows as a list, when the first form cannot carry its words"),
         ("Kept", "Every row, the title, the finding and the source line")],
        ["06.3", "14.16", "14.25"],
        "Set phone to differs and write phone_note in the spec when the form changes; the kit draws both and checks each at 358 px.",
        B.plate("s-14-12-correct", "At full width the nine sources stand as columns. On a phone their names would not fit under them, so they "
                                   "become bars, with the same rows, title and finding."),
        B.plate("s-14-12-failure", fails("14.12", "The phone drawing keeps three of the nine sources and takes a new title, so a reader on a "
                                                  "phone meets a different finding from a reader at a desk.")),
        [ex("Federal receipts by source, fiscal year 2026", "D08", where="14.12")],
        tokens=["oa.chart.artboard.phone"])


# ===============================================================================================================
# 14.13 The table, and the still image first
# ===============================================================================================================
NEWS_YEARS = [1998, 2003, 2008, 2013, 2018, 2023]


def rule_14_13(B):
    ds = "census-cbp-newspaper-publishers"
    r = {int(x["year"]): int(x["employees"]) for x in rows(ds)}
    need(r[2023] / r[1998] < 0.25 and r[2023] == 91350 and r[1998] == 401373, "the newspaper employment figures moved")
    title = f"Newspaper publishers employed {comma(r[2023])} people in March 2023, under a quarter of the {comma(r[1998])} of 1998"
    measure = "Paid employees of newspaper publishers in mid-March, every fifth year from 1998 to 2023, United States"
    B.spec("s-14-13-cols", form="column", family="comparison", tier="core", dataset=ds, where={"year": NEWS_YEARS},
           reader_question="How many people do newspaper publishers employ, and how has that changed?",
           evidence="finding", evidence_label="Finding", grade_line="Documented: a Census Bureau count of employers",
           title=title, measure_line=measure, source_line=src(ds),
           alt=f"Six columns of newspaper publishers’ employees, every fifth year: {', '.join(f'{y} {comma(r[y])}' for y in NEWS_YEARS)}.",
           table={"caption": "Paid employees of newspaper publishers, mid-March",
                  "columns": [{"field": "year", "label": "Year", "format": "year", "row_header": True},
                              {"field": "employees", "label": "Employees", "format": "integer"}]},
           encode={"x": "year", "y": "employees"}, labels={"named": 2023}, domain="D01", states=[],
           notes_internal="Rule 14.13's correct plate: a still chart with every value printed and its table as live text.")
    W, H, L, R, T, Bt = 320, 190, 10, 310, 12, 160
    step = (R - L) / len(NEWS_YEARS)
    ys = scale(0, 420000, Bt, T)
    bars = "".join(f'<rect class="{"s" if y == 2023 else "c"}" x="{L + i * step + 6:.1f}" y="{ys(r[y]):.1f}" width="{step - 12:.1f}" '
                   f'height="{Bt - ys(r[y]):.1f}"/><text class="tk" x="{L + i * step + step / 2:.1f}" y="{Bt + 18}" text-anchor="middle">{y}</text>'
                   for i, y in enumerate(NEWS_YEARS))
    inner = bars + f'<line class="ax" x1="{L}" x2="{R}" y1="{Bt}" y2="{Bt}"/>'
    B.add("s-14-13-correct", chart("s-14-13-cols"),
          alt=f"Columns with every value printed and the table open beneath them. {title}.")
    B.add("s-14-13-failure", dnp() + tl(title)
          + f'<div class="art">{svg(W, H, inner)}<p class="tip">2023: 91,350</p><p class="hov">Hover over a column to see its value.</p></div>',
          alt=FC + "The same columns with no values printed, a tooltip over the 2023 column, a line asking the reader to hover over a column, "
                   "and no table or source line.")
    return entry(
        "14.13", "Carry every chart’s table as live text, and publish the still image first.",
        ["Every chart carries its table: the rows it draws, as live text that a screen reader, a search and a copy can reach, folded under the "
         "source line as “The table and notes”. Rule 18.10 sets the table’s markup. With scripts off, the table stands open and the "
         "chart’s description takes the drawing’s place.",
         "Design the still image first, for a newsletter, an email or a social card, where nothing moves and nothing answers a pointer. A value "
         "a reader needs prints on the chart or in its notes. An interactive layer on the website adds filters or a switch to the still chart "
         "and takes nothing away from it."],
        ["Many readers meet a chart as a still picture in an inbox, where hovering does nothing. A table in live text gives every reader the "
         "numbers, whether they listen to the page, search it or copy a figure into their own notes."],
        [("Table", "Every row the chart draws, live text, folded under the source line"),
         ("Scripts off", "The table open and the description in the drawing’s place"),
         ("Still image", "Designed first; every value a reader needs printed"),
         ("Interactive layer", "Adds to the still chart on the website, and drops nothing from it")],
        ["18.10", "19.2", "14.130"],
        "Fill the spec's table under contract C2; the kit writes the table, and its check fails one whose rows differ from the data.",
        B.plate("s-14-13-correct", "Each column prints its value, so the still image needs no pointer, and the table under the source line "
                                   "gives the same rows as live text."),
        B.plate("s-14-13-failure", fails("14.13", "The values show only in a tooltip, which a newsletter, an email and a screen reader never "
                                                  "reach, and the chart carries no table.")),
        [ex("Newspaper publishers’ employees, every fifth year, 1998 to 2023", "D01", where="14.13")],
        basis="WCAG 2.2, success criterion 1.1.1, Non-text Content, and design judgment, from the chart system our founder and editor approved in November 2026")


# ===============================================================================================================
# 14.14 Exports from the kit
# ===============================================================================================================
def rule_14_14(B):
    stem = "20261112_S14-Columns-With-Moving-Average"
    files = [(f"{stem}-Newsprint-1440.svg", "SVG", "The drawing with its title and description inside, colors read from the tokens, fonts named"),
             (f"{stem}-Newsprint-1440.png", "PNG", "The still image at twice size, on the ground’s own color, for a newsletter or a social card"),
             (f"{stem}.csv", "CSV", "Exactly the rows the chart draws, every column of the data file, which the kit checks against the table")]
    li = "".join(f'<li><span class="fn">{e(f)}</span><span class="ty">{t}</span><span class="what">{e(w)}</span></li>' for f, t, w in files)
    B.add("s-14-14-correct", '<p class="k" style="margin:0 0 6px">One command</p>'
          '<p class="cmd">node work/build/chart-kit/oa-chart.mjs build s14</p><ul class="files">' + li + "</ul>",
          alt="One kit command, node work/build/chart-kit/oa-chart.mjs build s14, and the three files it writes for the payroll chart: an SVG, a "
              "PNG and a CSV, each with a dated name that says what the chart is, its ground and its width.",
          readable=True, notes="File names as the kit writes them for S14 on November 12, 2026 (contract C3).")
    bad = [("chart final v2.png", "PNG", "A screenshot, cropped above the source line"),
           ("payrolls numbers.xlsx", "Spreadsheet", "The values typed in again and rounded to the thousand"),
           ("chart.svg", "SVG", "Redrawn by hand, with its title edited after the page went live")]
    li2 = "".join(f'<li><span class="fn">{e(f)}</span><span class="ty">{t}</span><span class="what">{e(w)}</span></li>' for f, t, w in bad)
    B.add("s-14-14-failure", dnp() + '<ul class="files">' + li2 + "</ul>",
          alt=FC + "Three files made by hand for the payroll chart: a screenshot cropped above its source line, a spreadsheet of retyped and "
                   "rounded values, and a redrawn SVG whose title no longer matches the page.")
    return entry(
        "14.14", "Export every chart from the kit, so its files match the page.",
        ["Make every file of a chart with the chart kit’s one command, from the same spec and data file the page draws. The kit writes three "
         "files for each ground and width: an SVG with the chart’s title and description inside it, a PNG at twice size, and a CSV of exactly "
         "the rows the chart draws. Each name carries the date, what the chart is, its ground and its width, as Rule 18.14 asks of a download.",
         "To change a chart, change its spec or its data and run the command again; every file and the page then change together."],
        ["A file made by hand drifts from the page the first time someone fixes one and forgets the other. One command from one spec keeps "
         "the drawing, the still image and the numbers in step, and the kit checks the CSV against the table each time it runs."],
        [("Command", "node work/build/chart-kit/oa-chart.mjs build <spec>"),
         ("Files", "SVG, PNG at twice size, CSV of the drawn rows"),
         ("Names", "Date, chart and form, ground and width, as the kit writes them (Rule 18.14)")],
        ["18.14", "14.13"],
        "Run node work/build/chart-kit/oa-chart.mjs build <spec> --out <folder>; never edit an exported file, edit the spec and run it again.",
        B.plate("s-14-14-correct", "One command writes the three files from the spec the page uses, each named for its date, chart, ground "
                                   "and width."),
        B.plate("s-14-14-failure", fails("14.14", "Each file was made by hand: the screenshot drops the source line, the retyped numbers "
                                                  "round away the table’s values, and the redrawn picture no longer matches the page.")),
        [])


# ===============================================================================================================
# The opener and the chapter's own words
# ===============================================================================================================
def opener(B):
    lis = []
    for gp in PLAN["groups"][1:]:
        fam, q = gp["title"].split(": ", 1)
        lis.append(f'<li><span class="n">{gp["group"]}</span><span class="qq">{e(q[0].upper() + q[1:])}</span>'
                   f'<span class="fm">{e(fam)}</span></li>')
    body = ('<p class="k" style="margin:0 0 12px">Every chart answers one question</p><ol class="opq">' + "".join(lis) + "</ol>")
    B.add("s-14-opener", body, readable=True,
          alt="The sixteen questions chapter 14’s groups answer, each with its family and rules: "
              + "; ".join(g["title"] for g in PLAN["groups"][1:]) + ".",
          notes="The chapter's opener: the reader's questions that open groups 2 to 17, read from the plan file.")
    return {"specimen": "s-14-opener", "caption": "Each group of this chapter opens with the question a reader brings, and its forms answer it.",
            **{k: v for k, v in B.plates["s-14-opener"].items()}}


GROUP_LINES = {
    1: "Fourteen rules hold for every chart, from the question it answers to the files it ships as.",
    2: "Bars, dots and slopes set values side by side on one scale, so a reader sees which is bigger and by how much.",
    3: "Arrows, lollipops and diverging bars show which way each value moved and how far, with the direction in a word as well as a mark.",
    4: "Time runs from left to right in lines, columns and timelines, with each gap, break and preliminary value marked where it falls.",
    5: "Split bars, unit charts and treemaps show the parts of a whole and print the whole they add up to.",
    6: "Histograms, strip plots and box plots show how values spread, where they bunch and how far they run.",
    7: "Scatter plots and their relatives show whether two measures move together, and an association’s note says what the pattern cannot show about cause.",
    8: "How sure a figure is shows as a range, a band or a fan, as its publisher states it.",
    9: "Icon arrays, proportional symbols and overlap diagrams make a share countable and show where groups overlap.",
    10: "Big numbers, bullet graphs and progress bars show where one measure stands now against a target or a range.",
    11: "People move through a process in funnels, cohort charts and survival curves, which show where they leave it.",
    12: "Process diagrams, decision trees and who-decides diagrams show who decides and how a decision moves.",
    13: "Networks, matrices and arc diagrams show who is connected to whom, and how strongly.",
    14: "Sankeys, alluvial charts and flow maps show where money or people go, with every flow accounted for.",
    15: "A map appears when the place answers the question, and it names its places in words as well as color.",
    16: "A table lets a reader look a value up, and one sentence answers when a single figure is the whole story.",
    17: "Process explainers, number panels and comparison cards show how something works in one view.",
}


def chapter(B, sources):
    groups = []
    for gp in PLAN["groups"]:
        first = gp["rules"].split(" to ")[0]
        groups.append({"number": gp["group"], "before_rule": first, "title": gp["title"], "rules": gp["rules"], "line": GROUP_LINES[gp["group"]]})
    return {
        "number": "14", "anchor": "data-visualization", "title": "Data visualization", "part": "Evidence and media",
        "instruction": "Start from the reader's question to choose a chart, then title it with the evidence it shows.",
        "opener": opener(B),
        "intro": [
            "This chapter sets how Oath & Action shows numbers. Fourteen rules come first and hold for every chart. Each form a chart can take "
            "then has its own entry, grouped by the question it answers, with when to use it, what to use instead, and a finished example "
            "drawn from real data or labeled as illustrative.",
            "Chapter 13 sets the evidence every chart carries: its label, its grade, its source line and its dates. The rules here cite those "
            "rules by number and add what a drawing needs, from its scale and colors to its labels, its phone drawing and its files.",
            "The entries’ charts are drawn by our chart kit from frozen data files, the same way a chart in a story will be, and each one "
            "carries its table as live text."],
        "groups": groups,
        "related_chapters": [
            {"chapter": "01", "reason": "Rules 01.1 to 01.3 on parties and two-way scales, and Rule 01.9’s limits on examples."},
            {"chapter": "05", "reason": "Rules 05.3, 05.5 and 05.7: the one working red, marks at 3 to 1 and the chart palette."},
            {"chapter": "06", "reason": "Rules 06.3 and 06.5: no text under 13 px, and figures and minus signs in tables."},
            {"chapter": "12", "reason": "Rule 12.6, where labels and keys sit."},
            {"chapter": "13", "reason": "The evidence every chart carries: its label and grade, its source line, its period and Illustrative labels."},
            {"chapter": "15", "reason": "Systems drawings of the atlas, held to the same evidence rules."},
            {"chapter": "18", "reason": "Rules 18.10 and 18.14: tables and named downloads, and the components interactive charts use."}],
        "sources": sources,
    }


# ===============================================================================================================
# Checks
# ===============================================================================================================
FILLERS = ["genuinely", "really", "truly", "actually", "simply", "just", "leverage", "underscore", "underscores", "reflect", "reflects"]
STUDIO = r"Master Brief|\bPhase \d|\bGates?\b|\b[Bb]oards? \d|stage board|the studio|\bV5\b|\bV4\.2\b|Atlas V7|\bV7\b|\bDR-\d|\bD[123]-\d|\bG[12]-\d|\bT-\d"
LIMIT_BYTES = 200_000
OPENER_LIMIT = 16_000


def known_rules():
    ids = set()
    for f in (ROOT / "work/build/guide/chapters").glob("*.json"):
        try:
            d = json.loads(f.read_text())
        except Exception:
            continue
        if isinstance(d, dict):
            ids.update(r["id"] for r in d.get("rules", []))
    ids.update(r["rule"] for r in PLAN["chapter_rules"])
    ids.update(f["rule"] for f in PLAN["forms"])
    return ids


def token_names():
    out = set()

    def walk(o, p):
        if isinstance(o, dict):
            if "$value" in o:
                out.add(".".join(p))
                return
            for k, v in o.items():
                walk(v, p + [k])
    walk(json.loads(TOKENS.read_text()), [])
    return out


def reader_strings(entry_or_chapter):
    skip = {"notes", "builders", "specimen", "charts", "examples", "token", "tokens", "related", "id", "illustrative", "readable"}

    def walk(o, k=None):
        if isinstance(o, str):
            if k not in skip:
                yield k, o
        elif isinstance(o, dict):
            for kk, v in o.items():
                if kk not in skip:
                    yield from walk(v, kk)
        elif isinstance(o, list):
            for v in o:
                yield from walk(v, k)
    return list(walk(entry_or_chapter))


def visible(fragment):
    t = re.sub(r"<style\b.*?</style>|<!--.*?-->", " ", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def check(entries, chap, B):
    fails = []
    css_vars = set(re.findall(r"--oa-[a-z0-9-]+(?=\s*:)", (ROOT / "work/build/tokens/tokens.css").read_text()))
    toks, rules_known = token_names(), known_rules()
    plan = {r["rule"]: r["subject"] for r in PLAN["chapter_rules"]}
    for en in entries:
        need(en["id"] in plan, f"{en['id']} is not a chapter-wide rule in the plan")
        n_words = len(en["title"].split())
        if n_words > 16:
            fails.append(f"{en['id']} title runs {n_words} words")
        for t in en["tokens"] + [s["token"] for s in en["specs"] if s.get("token")]:
            if t not in toks:
                fails.append(f"{en['id']} names token {t}, which tokens.json lacks")
        for rr in en["related"]:
            if rr not in rules_known:
                fails.append(f"{en['id']} relates to {rr}, which no chapter or plan holds")
        f = en["failure"]
        if not f["caption"].startswith(f"<strong>Fails Rule {en['id']}.</strong>"):
            fails.append(f"{en['id']} failure caption does not lead with its rule")
        if not f["alt"].startswith(FC.strip()):
            fails.append(f"{en['id']} failure alt does not open with the band's words")
        if 'class="dnp"' not in B.files[f["specimen"]]:
            fails.append(f"{en['id']} failure plate lacks the do-not-publish band")
    texts = [(f"{en['id']} {k}", s) for en in entries for k, s in reader_strings(en)]
    texts += [(f"chapter {k}", s) for k, s in reader_strings(chap)]
    texts += [(f"{sid} visible", visible(t)) for sid, t in B.files.items()]
    texts += [(f"{cid} {k}", s) for cid, sp in B.specs.items() for k, s in reader_strings(sp) if k not in ("notes_internal", "failure")]
    for where, s in texts:
        if "—" in s or "‑" in s:
            fails.append(f"an em dash or U+2011 in {where}")
        for w in FILLERS:
            if re.search(rf"\b{w}\b", s, re.I):
                fails.append(f"listed word {w!r} in {where}")
        if re.search(STUDIO, s):
            fails.append(f"a studio word or decision code in {where}: {re.search(STUDIO, s).group(0)}")
        for m in re.finditer(r"\bRules? (\d\d\.\d+)", s):
            if m.group(1) not in rules_known:
                fails.append(f"{where} cites Rule {m.group(1)}, which no chapter or plan holds")
        if re.search(r"(?<![\w’])'|\"", re.sub(r"<[^>]+>", "", s)) and "visible" not in where:
            fails.append(f"a straight quote mark in {where}: {s[:60]}")
    for sid, t in B.files.items():
        bare = re.sub(r"var\([^)]*\)", "", t)
        if re.search(r"#[0-9a-fA-F]{3,6}\b|\brgba?\(", bare):
            fails.append(f"{sid}: a literal color")
        for v in re.findall(r"var\((--oa-[a-z0-9-]+)", t):
            if v not in css_vars:
                fails.append(f"{sid}: {v} is not in tokens.css")
        if re.search(r"<h[1-6]\b", t):
            fails.append(f"{sid}: a heading element")
    op = len(B.files["s-14-opener"].encode())
    if op > OPENER_LIMIT:
        fails.append(f"the opener weighs {op} bytes, over {OPENER_LIMIT}")
    return fails


# ===============================================================================================================
# Writing
# ===============================================================================================================
MINE = re.compile(r"^s-14-(opener|(\d+)-[a-z0-9-]+)\.(html|chart\.json)$")


def write(entries, chap, B):
    ENTRIES.mkdir(parents=True, exist_ok=True)
    for en in entries:
        n = int(en["id"].split(".")[1])
        (ENTRIES / f"14-{n:03d}.json").write_text(json.dumps(en, indent=1, ensure_ascii=False) + "\n")
    (ENTRIES / "14-chapter.json").write_text(json.dumps(chap, indent=1, ensure_ascii=False) + "\n")
    keep = {f"{sid}.html" for sid in B.files} | {f"{cid}.chart.json" for cid in B.specs}
    for p in SPECIMENS.glob("s-14-*"):
        m = MINE.match(p.name)
        if m and (m.group(1) == "opener" or (m.group(2) and int(m.group(2)) <= 14)) and p.name not in keep:
            p.unlink()
    for sid, t in B.files.items():
        (SPECIMENS / f"{sid}.html").write_text(t)
    for cid, s in B.specs.items():
        (SPECIMENS / f"{cid}.chart.json").write_text(json.dumps(s, indent=1, ensure_ascii=False) + "\n")


def main():
    only_check = "--check-only" in sys.argv
    B = Book()
    entries = [f(B) for f in (rule_14_1, rule_14_2, rule_14_3, rule_14_4, rule_14_5, rule_14_6, rule_14_7, rule_14_8, rule_14_9,
                              rule_14_10, rule_14_11, rule_14_12, rule_14_13, rule_14_14)]
    sources = []
    for s in [sp.get("source_line") for sp in B.specs.values()] + re.findall(r'<p class="src">(.*?)</p>', "".join(B.files.values())):
        s = html.unescape(s) if s else s
        if s and s not in sources:
            sources.append(s)
    chap = chapter(B, sources)
    fails = check(entries, chap, B)
    weight = sum(len(t.encode()) for t in B.files.values()) + sum(len(json.dumps(s, ensure_ascii=False).encode()) for s in B.specs.values())
    print(f"14 rules, {len(B.files)} plates, {len(B.specs)} kit specs; fragments and specs {weight:,} bytes before the kit draws; "
          f"opener {len(B.files['s-14-opener'].encode()):,} bytes")
    doms = Counter(x["domain"] for en in entries for x in en["examples"])
    print("examples by domain:", dict(sorted(doms.items())))
    if fails:
        for f in fails:
            print("FAIL:", f)
        raise SystemExit(f"{len(fails)} check(s) failed; nothing written")
    if weight > LIMIT_BYTES:
        raise SystemExit(f"the plates weigh {weight:,} bytes before drawing, over {LIMIT_BYTES:,}")
    if not only_check:
        write(entries, chap, B)
        print("wrote 14-001.json to 14-014.json, 14-chapter.json and the plates")


if __name__ == "__main__":
    main()
