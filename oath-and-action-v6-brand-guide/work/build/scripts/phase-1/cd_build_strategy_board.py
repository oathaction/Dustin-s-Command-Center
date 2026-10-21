"""Creative director, Phase 1: build the Strategy and Direction board.

Reads the template in work/boards/phase-1/strategy/, inlines V5 Polished vector
masters from work/extract/v5-polished/sprite/ (read only), inlines the identity
board's V2 hinge diagram from work/boards/phase-1/identity/07-hinge/ once
work/handoffs/phase-1/20261021_Hinge-V2-Ready.md exists (a marked placeholder
otherwise), draws the Loop R9 sketch with hollow conceptual lines, and writes
work/boards/20261021_Strategy-And-Direction-Board.html.

Run: python3 -I work/build/scripts/phase-1/cd_build_strategy_board.py <project root>
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SPRITE = ROOT / "work/extract/v5-polished/sprite"
TEMPLATE = ROOT / "work/boards/phase-1/strategy/strategy-board.template.html"
CHECKS = ROOT / "work/boards/phase-1/strategy/20261021_Board-Check-Results.json"
OUT = ROOT / "work/boards/20261021_Strategy-And-Direction-Board.html"

CHARCOAL, RED, MUTED = "#121212", "#E63946", "#45494F"


def read_svg(name):
    return (SPRITE / f"{name}.svg").read_text(encoding="utf-8")


def path_d(name):
    m = re.search(r'<path fill="currentColor" d="([^"]+)"', read_svg(name))
    return m.group(1)


def viewbox(name):
    return re.search(r'viewBox="([^"]+)"', read_svg(name)).group(1)


def amp_inner():
    svg = read_svg("amp")
    return re.search(r"<g fill=\"currentColor\">(.*?)</g>", svg, re.S).group(1)


AMP_VIEWBOX = "-3 -3 95.62 106.61"  # padded so the loop top and tail are not clipped (Phase 0 finding)


def wordmark():
    svg = read_svg("wordmark")
    svg = re.sub(r"<title>.*?</title>", "", svg)
    svg = svg.replace(' xmlns:xlink="http://www.w3.org/1999/xlink"', "")
    svg = svg.replace(' style="color:#121212"', ' class="wm" role="img" aria-label="Oath &amp; Action wordmark, V5 Polished master"')
    return svg


def amp_small():
    return (f'<svg viewBox="{AMP_VIEWBOX}" aria-hidden="true" focusable="false">'
            f'<g fill="currentColor">{amp_inner()}</g></svg>')


HINGE_DIR = ROOT / "work/boards/phase-1/identity/07-hinge"
HINGE_READY = ROOT / "work/handoffs/phase-1/20261021_Hinge-V2-Ready.md"
HINGE_LABEL = ("Hinge diagram V2: OATH{u} and ACTION{i}, joined by a line through a circle around the red ampersand. "
               "A solid arc runs clockwise over the top from OATH to ACTION, and a second solid arc returns under the bottom.")


def hinge_inline(name, cls, label):
    svg = (HINGE_DIR / name).read_text(encoding="utf-8")
    svg = re.sub(r"<title>.*?</title>", "", svg, flags=re.S)
    return svg.replace("<svg ", f'<svg class="{cls}" role="img" aria-label="{label}" ', 1)


def hinge_amp_head():
    """Hinge headline ampersand: the V5 master glyph, colored by CSS (the view's working red)."""
    return (f'<svg class="hamp" viewBox="{AMP_VIEWBOX}" role="img" aria-label="and" focusable="false">'
            f'<g fill="currentColor">{amp_inner()}</g></svg>')


def loop_figure():
    disp, comp = "20261021_Hinge-Display-Master_V2.svg", "20261021_Hinge-Compact-Master_V2.svg"
    if HINGE_READY.exists() and (HINGE_DIR / disp).exists() and (HINGE_DIR / comp).exists():
        body = (hinge_inline(disp, "display", HINGE_LABEL.format(u=" with UNDERSTAND below", i=" with IMPACT below"))
                + hinge_inline(comp, "compact", HINGE_LABEL.format(u="", i="")))
        cap = ('<span class="tag">Option</span> The identity board\'s V2 hinge diagram: solid arcs, clockwise, '
               'UNDERSTAND and IMPACT below. Under 600 px its compact master drops the labels.')
        return f'<figure class="white hingev2">{body}<figcaption>{cap}</figcaption></figure>'
    return ('<figure class="placeholder hingev2"><p><span class="tag defect">Placeholder</span></p>'
            '<p>The identity board\'s V2 hinge diagram goes here, from '
            '<code>work/handoffs/phase-1/20261021_Hinge-V2-Ready.md</code>, which did not exist when this board was built.</p></figure>')


def r9_svg():
    """Loop R9 sketch. Conceptual steps take the systems board's hollow line: two hairlines around an empty core."""
    def node(x, y, l1, l2):
        return (f'<rect x="{x}" y="{y}" width="150" height="56" fill="#FFFFFF" stroke="{CHARCOAL}" stroke-width="1.5"/>'
                f'<text x="{x + 75}" y="{y + 24}" text-anchor="middle">{l1}</text>'
                f'<text x="{x + 75}" y="{y + 44}" text-anchor="middle">{l2}</text>')

    def hollow(x1, y1, x2, y2):
        import math
        L = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / L, (y2 - y1) / L
        ex, ey = x2 - ux * 9, y2 - uy * 9  # stop the line where the arrowhead starts
        px, py = -uy * 5, ux * 5
        head = f"M{x2:.1f} {y2:.1f} L{ex + px:.1f} {ey + py:.1f} L{ex - px:.1f} {ey - py:.1f}Z"
        return (f'<path d="M{x1} {y1} L{ex:.1f} {ey:.1f}" stroke="{CHARCOAL}" stroke-width="5" fill="none"/>'
                f'<path d="M{x1} {y1} L{ex:.1f} {ey:.1f}" stroke="#FFFFFF" stroke-width="2.2" fill="none"/>'
                f'<path d="{head}" fill="{CHARCOAL}"/>')

    return "".join([
        '<svg viewBox="0 0 360 236" role="img" aria-label="Loop R9 sketch, graded Hypothesis: effective participation raises accountable delivery, '
        'which raises warranted trust, which raises effective participation. Every step is positive and drawn as a hollow line, for a conceptual step.">',
        f'<g font-family="Inter, Helvetica Neue, Arial, sans-serif" font-size="15" fill="{CHARCOAL}">',
        node(0, 8, "Effective", "participation"), node(210, 8, "Accountable", "delivery"), node(105, 172, "Warranted", "trust"),
        hollow(154, 36, 206, 36), hollow(296, 68, 236, 166), hollow(124, 166, 64, 68),
        '<g font-weight="700" font-size="17"><text x="179" y="27" text-anchor="middle">+</text>'
        '<text x="284" y="124" text-anchor="middle">+</text><text x="76" y="124" text-anchor="middle">+</text></g>',
        f'<rect x="138" y="82" width="84" height="26" fill="#FFFFFF" stroke="{CHARCOAL}" stroke-width="1.5"/>'
        '<text x="180" y="100" text-anchor="middle" font-weight="700">Loop R9</text>'
        '<text x="180" y="130" text-anchor="middle">Hypothesis</text>',
        "</g></svg>",
    ])


def li(items):
    return "".join(f"<li>{i}</li>" for i in items)


def main():
    html = TEMPLATE.read_text(encoding="utf-8")
    checks = json.loads(CHECKS.read_text(encoding="utf-8")) if CHECKS.exists() else {}
    fill = {
        "{{WORDMARK}}": wordmark(),
        "{{LOOP_FIGURE}}": loop_figure(),
        "{{AMP_HEAD}}": hinge_amp_head(),
        "{{R9_SVG}}": r9_svg(),
        "{{AMP_SMALL}}": amp_small(),
        "{{A11Y_SCORE}}": checks.get("a11y_score", "Pending"),
        "{{A11Y_REASON}}": checks.get("a11y_reason", "Board checks not yet run."),
        "{{CHECKED}}": li(checks.get("checked", ["Board checks not yet run."])),
        "{{NOT_CHECKED}}": li(checks.get("not_checked", ["Board checks not yet run."])),
    }
    for k, v in fill.items():
        html = html.replace(k, v)
    left = re.findall(r"\{\{[A-Z0-9_]+\}\}", html)
    if left:
        raise SystemExit(f"Unfilled placeholders: {left}")
    OUT.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
