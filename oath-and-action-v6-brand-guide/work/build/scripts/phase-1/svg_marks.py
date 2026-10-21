"""Drawing helpers for the Systems Marks Board. Every mark is drawn at 1 SVG unit = 1 CSS pixel.

Colour comes from the enclosing surface cell: currentColor is the ink, the class .bgf fills with var(--cell),
and .ink2 uses var(--ink2). Nothing here reads V7; callers pass values read by systems_marks_data.py.
"""
import html
import math

esc = html.escape

DASH = {"documented": None, "well-supported": None, "plausible": "9 4", "plausible_contested": "9 3 2 3",
        "contested": "9 3 2 3", "hypothesis": "2 4"}
GRADE_WORD = {"documented": "Documented", "well-supported": "Well supported", "well_supported": "Well supported",
              "plausible": "Plausible", "plausible_contested": "Contested", "contested": "Contested",
              "hypothesis": "Hypothesis", "mixed": "Mixed", "not yet tested": "Not yet tested"}
DELAY_WORD = {"S": "under 2 years", "M": "2 to 10 years", "L": "over 10 years"}
DELAY_TICKS = {"S": 1, "M": 2, "L": 3}
MINUS = "−"


def sign_glyph(p):
    return "+" if p == "+" else (MINUS if p == "-" else "")


def text_w(s, size=13, weight=400):
    """Rough advance width of Inter at a size, used only for layout and wrapping."""
    per = 0.565 if weight < 600 else 0.6
    narrow = sum(1 for ch in s if ch in "il.,:;'| ")
    return size * (per * (len(s) - narrow) + 0.3 * narrow)


def wrap(s, width, size=13, weight=400):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_w(t, size, weight) <= width or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def T(x, y, s, cls="", anchor=None, size=None):
    a = f' text-anchor="{anchor}"' if anchor else ""
    sz = f' font-size="{size}"' if size else ""
    c = f' class="{cls}"' if cls else ""
    return f'<text x="{x:.1f}" y="{y:.1f}"{c}{a}{sz}>{esc(s)}</text>'


def svg(w, h, body, label, cls="mk"):
    return (f'<svg class="{cls}" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
            f'aria-label="{esc(label)}">{body}</svg>')


# ------------------------------------------------------------------ lines, heads, ticks

def _unit(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n


def arrow_head(p_prev, p_end, length=9, half=4.5):
    ux, uy = _unit(p_prev, p_end)
    bx, by = p_end[0] - ux * length, p_end[1] - uy * length
    px, py = -uy, ux
    pts = f"{p_end[0]:.1f},{p_end[1]:.1f} {bx + px * half:.1f},{by + py * half:.1f} {bx - px * half:.1f},{by - py * half:.1f}"
    return (bx, by), f'<polygon points="{pts}" fill="currentColor"/>'


def diamond_head(p_prev, p_end, length=12, half=4.5):
    ux, uy = _unit(p_prev, p_end)
    mx, my = p_end[0] - ux * length / 2, p_end[1] - uy * length / 2
    bx, by = p_end[0] - ux * length, p_end[1] - uy * length
    px, py = -uy, ux
    pts = (f"{p_end[0]:.1f},{p_end[1]:.1f} {mx + px * half:.1f},{my + py * half:.1f} "
           f"{bx:.1f},{by:.1f} {mx - px * half:.1f},{my - py * half:.1f}")
    return (bx, by), f'<polygon points="{pts}" class="bgf" stroke="currentColor" stroke-width="1.5" stroke-linejoin="miter"/>'


def ticks(p0, p1, n, start=7, step=5, length=10):
    if not n:
        return ""
    ux, uy = _unit(p0, p1)
    px, py = -uy, ux
    out = []
    for i in range(n):
        cx, cy = p0[0] + ux * (start + i * step), p0[1] + uy * (start + i * step)
        out.append(f'<line x1="{cx + px * length / 2:.1f}" y1="{cy + py * length / 2:.1f}" '
                   f'x2="{cx - px * length / 2:.1f}" y2="{cy - py * length / 2:.1f}" stroke="currentColor" stroke-width="1.5"/>')
    return "".join(out)


def path_d(points):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in points)


def connection(points, grade, delay=None, kind="causal", width=2, head=True, conceptual=False, dash_override=None):
    """A connection drawn on a polyline. The line stops at the base of its end mark so dashes never poke through."""
    pts = list(points)
    end = ""
    if head and kind == "authority":
        base, end = diamond_head(pts[-2], pts[-1])
        pts[-1] = base
    elif head:
        base, end = arrow_head(pts[-2], pts[-1])
        pts[-1] = base
    dash = dash_override if dash_override is not None else DASH.get(grade)
    if conceptual:
        line = (f'<path d="{path_d(pts)}" fill="none" stroke="currentColor" stroke-width="5"/>'
                f'<path d="{path_d(pts)}" fill="none" class="bgs" stroke-width="2"/>')
    else:
        da = f' stroke-dasharray="{dash}"' if dash else ""
        line = f'<path d="{path_d(pts)}" fill="none" stroke="currentColor" stroke-width="{width}"{da}/>'
    return line + end + ticks(points[0], points[1], DELAY_TICKS.get(delay, 0) if delay else 0)


def pill(x, y, text, record=False, h=22):
    w = 16 + text_w(text, 13, 600) + (12 if record else 0)
    sq = f'<rect x="{x + 9:.1f}" y="{y + h / 2 - 3.5:.1f}" width="7" height="7" fill="currentColor"/>' if record else ""
    tx = x + 8 + (12 if record else 0)
    return w, (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="{h / 2}" class="bgf" stroke="currentColor" stroke-width="1"/>'
               f'{sq}<text x="{tx:.1f}" y="{y + 15.5:.1f}" class="sb">{esc(text)}</text>')


def conn_label(link, show_type=True):
    s = f'{link["id"]} {sign_glyph(link["polarity"])}'.strip()
    if link["type"] == "authority":
        s = f'{link["id"]} no sign'
    if show_type and link["type"] not in ("causal", "authority"):
        s += f' · {link["type"]}'
    return s


def vbox(x, y, w, h, code, label):
    lines = wrap(label, w - 16 - text_w(code, 13, 700) - 6, 13, 400)
    first_x = x + 8 + text_w(code, 13, 700) + 6
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" class="bgf" stroke="currentColor" stroke-width="1.5"/>',
           T(x + 8, y + 18, code, "b")]
    for i, ln in enumerate(lines[:2]):
        out.append(T(first_x if i == 0 else first_x, y + 18 + i * 16, ln))
    return "".join(out)


def ring(cx, cy, r=6):
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="#121212" stroke-width="4.5"/>'
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="#E63946" stroke-width="2.5"/>')


# ------------------------------------------------------------------ vertical loop

def vloop(nodes, steps, ret, W=320, record_mark=True, rings=None, label="", grade_words=True):
    """nodes: [(code, label)], steps: link dicts from node i to node i+1, ret: link dict from last node to first.
    rings: {"links": [ids], "nodes": [codes]} for a reform's targets."""
    rings = rings or {"links": [], "nodes": []}
    bx, bw, bh, gap, y0 = 30, 178, 42, 84, 6
    ax = bx + 60
    ys = [y0 + i * (bh + gap) for i in range(len(nodes))]
    out = []
    for i, st in enumerate(steps):
        y_a, y_b = ys[i] + bh, ys[i + 1]
        out.append(connection([(ax, y_a), (ax, y_b)], st["evidence"], st["delay"], st["type"]))
        px = ax + 14
        py = y_a + 10
        _, p = pill(px, py, conn_label(st), record=record_mark and st["evidence"] == "documented")
        out.append(p)
        if grade_words:
            out.append(T(px, py + 38, GRADE_WORD[st["evidence"]], "sb"))
            out.append(T(px, py + 54, DELAY_WORD[st["delay"]], "ink2"))
        if st["id"] in rings["links"]:
            out.append(ring(ax, (y_a + y_b) / 2 + 6))
    yl = ys[-1] + bh
    rp = [(ax, yl), (ax, yl + 26), (12, yl + 26), (12, ys[0] + bh / 2), (bx, ys[0] + bh / 2)]
    out.append(connection(rp, ret["evidence"], ret["delay"], ret["type"]))
    if ret["id"] in rings["links"]:
        out.append(ring(12, (yl + 26 + ys[0]) / 2))
    py = yl + 36
    pw, p = pill(24, py, conn_label(ret), record=record_mark and ret["evidence"] == "documented")
    out.append(p)
    if grade_words:
        out.append(T(24 + pw + 8, py + 15.5, GRADE_WORD[ret["evidence"]], "sb"))
        out.append(T(24 + pw + 8, py + 31.5, DELAY_WORD[ret["delay"]], "ink2"))
    for (code, lab), y in zip(nodes, ys):
        out.append(vbox(bx, y, bw, bh, code, lab))
        if code in rings["nodes"]:
            out.append(ring(bx + bw, y))
    H = py + 40
    return svg(W, H, "".join(out), label)


# ------------------------------------------------------------------ small specimens

def line_specimen(grade, w=104, delay=None, kind="causal", conceptual=False, dash=None, width=2, opacity=None):
    body = connection([(4, 9), (w - 4, 9)], grade, delay, kind, width=width, conceptual=conceptual, dash_override=dash)
    if opacity is not None:
        body = f'<g opacity="{opacity}">{body}</g>'
    return svg(w, 18, body, f"{grade} line")


def grade_sample(grade, w=40):
    return svg(w, 12, f'<path d="M2 6 L{w - 2} 6" stroke="currentColor" stroke-width="2" fill="none"'
                      + (f' stroke-dasharray="{DASH[grade]}"' if DASH.get(grade) else "") + "/>", f"{grade} texture", "mk inl")


def pips(parsed, w=150, h=22):
    """Diverging ordinal pips: costs left of the zero line, gains right. Filled = a code V7 states;
    ring = the far end of a range V7 states. Sign glyphs sit at the outer end of each run."""
    cx = w / 2
    r, pitch = 4.5, 12
    out = [f'<line x1="{cx}" y1="2" x2="{cx}" y2="{h - 2}" stroke="currentColor" stroke-width="1"/>']
    g, go = parsed["gain"], parsed["gain_open"]
    c, co = parsed["cost"], parsed["cost_open"]
    for i in range(max(g, go)):
        x = cx + 11 + i * pitch
        if i < g:
            out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="{r}" fill="currentColor"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="{r - 0.75}" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    if max(g, go):
        out.append(T(cx + 11 + max(g, go) * pitch - 3, h / 2 + 4.5, "+", "b"))
    for i in range(max(c, co)):
        x = cx - 11 - i * pitch
        if i < c:
            out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="{r}" fill="currentColor"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{h / 2}" r="{r - 0.75}" fill="none" stroke="currentColor" stroke-width="1.5"/>')
    if max(c, co):
        out.append(T(cx - 11 - max(c, co) * pitch - 4, h / 2 + 4.5, MINUS, "b", anchor="end"))
    if parsed["zero"] and not (g or c):
        out.append(f'<rect x="{cx - 2:.1f}" y="{h / 2 - 7:.1f}" width="4" height="14" fill="currentColor"/>')
    elif parsed["zero"]:
        out.append(f'<rect x="{cx - 2:.1f}" y="{h / 2 - 7:.1f}" width="4" height="14" fill="currentColor"/>')
    if parsed["uncertain"]:
        out.append(f'<circle cx="{cx}" cy="{h / 2}" r="8" class="bgf" stroke="currentColor" stroke-width="1.5"/>'
                   + T(cx, h / 2 + 4.5, "?", "b", anchor="middle"))
    return svg(w, h, "".join(out), "ordinal effect mark", "mk inl")


def width_strand(code, w=120):
    wid = {"+S": 1.3, "+M": 2.6, "+L": 3.9}.get(code, 0)
    if not wid:
        return svg(w, 14, "", "no strand", "mk inl")
    return svg(w, 14, f'<line x1="4" y1="7" x2="{w - 4}" y2="7" stroke="currentColor" stroke-width="{wid}"/>', "strand", "mk inl")


# ------------------------------------------------------------------ events

def ev_glyph(family, cx, cy, pending=False):
    dash = ' stroke-dasharray="2 1.5"' if pending else ""
    fill = 'fill="none"' if pending else 'fill="currentColor"'
    stroke = f'stroke="currentColor" stroke-width="1.5"{dash}' if pending else ""
    if family == "Ballot measure":
        return f'<rect x="{cx - 4:.1f}" y="{cy - 4:.1f}" width="8" height="8" {fill} {stroke}/>'
    if family == "Statute or local law":
        return f'<rect x="{cx - 6:.1f}" y="{cy - 3:.1f}" width="12" height="6" {fill} {stroke}/>'
    if family == "Court ruling":
        return f'<rect x="{cx - 3:.1f}" y="{cy - 6:.1f}" width="6" height="12" {fill} {stroke}/>'
    # executive or agency action: outline square with a centre dot
    return (f'<rect x="{cx - 3.75:.1f}" y="{cy - 3.75:.1f}" width="7.5" height="7.5" fill="none" stroke="currentColor" stroke-width="1.5"{dash}/>'
            f'<rect x="{cx - 1.5:.1f}" y="{cy - 1.5:.1f}" width="3" height="3" fill="currentColor"/>')


def glyph_svg(family, pending=False):
    return svg(16, 16, ev_glyph(family, 8, 8, pending), family + (" pending" if pending else ""), "mk inl")


def year_frac(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return y + (m - 1) / 12 + (d - 1) / 365


DIR_ORDER = ["toward voters", "voters kept existing rules", "mixed", "pending", "away from voters"]
DIR_LABEL = {"toward voters": "Toward voters", "voters kept existing rules": "Voters kept existing rules",
             "mixed": "Mixed direction", "pending": "Pending", "away from voters": "Away from voters"}


def timeline(events, y0, y1, W, label_w, tick_step, title):
    """Rows by direction, glyph shape by instrument family, same-time events stacked upward in their row."""
    plot_x0, plot_x1 = label_w + 6, W - 10
    sx = lambda t: plot_x0 + (t - y0) / (y1 - y0) * (plot_x1 - plot_x0)
    pitch, mw = 13, 13
    out, y = [], 6
    for dirn in DIR_ORDER:
        evs = sorted((e for e in events if e["direction"] == dirn), key=lambda e: e["date"])
        levels = []
        placed = []
        for e in evs:
            x = sx(year_frac(e["date"]))
            lv = 0
            while lv < len(levels) and levels[lv] > x - mw:
                lv += 1
            if lv == len(levels):
                levels.append(x)
            else:
                levels[lv] = x
            placed.append((x, lv, e))
        n = max(1, len(levels))
        row_h = max(30, n * pitch + 12)
        base = y + row_h - 8
        lab = wrap(DIR_LABEL[dirn], label_w - 4, 13, 600)
        for i, ln in enumerate(lab):
            out.append(T(2, y + 15 + i * 15, ln, "sb"))
        out.append(f'<line x1="{plot_x0}" y1="{base + 4}" x2="{plot_x1}" y2="{base + 4}" stroke="currentColor" stroke-width="1"/>')
        if not evs:
            out.append(T(plot_x0 + 4, base - 2, "none in this selection", "ink2"))
        for x, lv, e in placed:
            out.append(f'<g><title>{esc(e["id"] + " · " + e["date"] + " · " + e["jurisdiction"] + " · " + e["instrument"] + " · " + DIR_LABEL[dirn])}</title>'
                       + ev_glyph(e["family"], x, base - 4 - lv * pitch, pending=(dirn == "pending")) + "</g>")
        y += row_h + 4
    # axis
    for yr in range(int(math.ceil(y0)), int(y1) + 1):
        if (yr - int(math.ceil(y0))) % tick_step == 0:
            x = sx(yr)
            out.append(f'<line x1="{x:.1f}" y1="{y - 2}" x2="{x:.1f}" y2="{y + 4}" stroke="currentColor" stroke-width="1"/>')
            out.append(T(x, y + 19, str(yr), "", anchor="middle"))
    out.append(f'<line x1="{plot_x0}" y1="{y - 2}" x2="{plot_x1}" y2="{y - 2}" stroke="currentColor" stroke-width="1"/>')
    return svg(W, y + 26, "".join(out), title)


def spans(rows, y0, y1, W, label_w, tick_step, snapshot, title, stacked=False, grade_col=0):
    plot_x0, plot_x1 = label_w + 6, W - 8 - grade_col
    sx = lambda t: plot_x0 + (t - y0) / (y1 - y0) * (plot_x1 - plot_x0)
    out, y = [], 4
    snap_x = sx(year_frac(snapshot))
    for r in rows:
        p = r["period"]
        word = GRADE_WORD.get(r["grade"], r["grade"])
        if stacked:
            out.append(f'<text x="2" y="{y + 14:.1f}"><tspan class="b">{esc(r["id"])}</tspan> {esc(r["date"])} · {esc(word)}</text>')
            by = y + 22
            row_h = 36
        else:
            out.append(f'<text x="2" y="{y + 14:.1f}"><tspan class="b">{esc(r["id"])}</tspan> {esc(r["date"])}</text>')
            if grade_col:
                out.append(T(W - grade_col, y + 14, word, "ink2"))
            by = y + 6
            row_h = 21
        x_a = sx(year_frac(p["start"]))
        if p["kind"].startswith("point"):
            out.append(f'<rect x="{x_a - 4:.1f}" y="{by:.1f}" width="8" height="8" class="bgf" stroke="currentColor" stroke-width="1.5"/>')
        else:
            x_b = sx(year_frac(p["end"])) if p["end"] else snap_x
            wdt = max(3, x_b - x_a)
            out.append(f'<rect x="{x_a:.1f}" y="{by:.1f}" width="{wdt:.1f}" height="8" fill="currentColor"/>')
            if p["kind"] == "open span":
                out.append(f'<rect x="{x_a + wdt - 1:.1f}" y="{by - 3:.1f}" width="2" height="14" class="bgf"/>')
        if p.get("extra_point"):
            xe = sx(year_frac(p["extra_point"]["date"]))
            out.append(f'<rect x="{xe - 4:.1f}" y="{by:.1f}" width="8" height="8" class="bgf" stroke="currentColor" stroke-width="1.5"/>')
        y += row_h
    for yr in range(y0, y1 + 1):
        if (yr - y0) % tick_step == 0:
            x = sx(yr)
            out.append(f'<line x1="{x:.1f}" y1="{y + 2}" x2="{x:.1f}" y2="{y + 7}" stroke="currentColor" stroke-width="1"/>')
            out.append(T(x, y + 22, str(yr), "", anchor="middle"))
    out.append(f'<line x1="{plot_x0}" y1="{y + 2}" x2="{plot_x1}" y2="{y + 2}" stroke="currentColor" stroke-width="1"/>')
    out.append(f'<line x1="{snap_x:.1f}" y1="0" x2="{snap_x:.1f}" y2="{y + 2}" stroke="currentColor" stroke-width="0.75"/>')
    return svg(W, y + 28, "".join(out), title)
