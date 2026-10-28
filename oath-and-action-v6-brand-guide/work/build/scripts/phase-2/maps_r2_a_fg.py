"""Direction A, Field Guide: every loop is drawn as one specimen card, at four sizes.

Layout rule a reader can hear in one sentence: the first box sits top left, the line across the top runs forward,
and the closing step comes back underneath (two steps) or up the left side (three and four steps) into the first box.
  two steps    box 1 and box 2 side by side, the return under them
  three steps  box 1 and box 2 over box 3, routed clockwise
  four steps   two over two, a rectangle route clockwise from top left
One function lays out every scale (miniature, double-size lead, card, catalog head) from the same proportions, so the
miniature is the card's drawing at a smaller size. The phone card stacks the boxes and runs the return up the left.

Notation by scale follows the creative director's budget (CD review section 4):
  miniature  M1 texture, hollow line, a sign in a 16 px disc; no record square, ticks, pointers or red
  card       adds the record square, grade words, delay ticks, step names and the 'Higher:' rules; red at one
             reform's targets, on White only
Every data mark carries the round-one data-* attributes, so the verifier reads them back.
"""
import math

import maps_draw as D
import maps_r2_a_text as TX

MINUS = "−"
GLYPH = {"+": "+", "-": MINUS}

SCALES = {
    # box width, box height floor, horizontal gap, vertical gap, return depth, label size, id size, line width, disc r
    "mini": dict(bw=158, bh=48, hg=60, vg=60, depth=34, ls=13, lw=600, ids=0, stroke=2.0, disc=8, glyph=13, pad=9),
    "lead": dict(bw=300, bh=84, hg=150, vg=96, depth=58, ls=18, lw=600, ids=15, stroke=2.5, disc=11, glyph=15, pad=14),
    "card": dict(bw=300, bh=0, hg=220, vg=150, depth=110, ls=16, lw=600, ids=16, stroke=2.5, disc=12, glyph=15, pad=16),
}


def T(x, y, s, size, weight=400, fill=D.INK, anchor=None, family="inter", extra=""):
    cls = {"inter": "mt", "tight": "md", "lora-italic": "mq"}[family]
    if family == "inter" and weight >= 700:
        cls += " mb"
    elif family == "inter" and weight >= 600:
        cls += " ms"
    a = f' text-anchor="{anchor}"' if anchor else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" font-size="{size}" fill="{fill}"{a}{extra}>{D.esc(s)}</text>'


STYLE = ("<style>.mt{font-family:Inter,'Helvetica Neue',Arial,sans-serif}.md{font-family:'Inter Tight',Inter,Arial,sans-serif;font-weight:800}"
         ".ms{font-weight:600}.mb{font-weight:700}.mq{font-family:Lora,Georgia,serif;font-style:italic}</style>")


def svg_doc(w, h, body, label, view, attrs="", bg=None):
    bgr = f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" role="img" '
            f'aria-label="{D.esc(label)}" data-view="{D.esc(view)}"{attrs}><title>{D.esc(label)}</title>{STYLE}{bgr}{body}</svg>')


# ------------------------------------------------------------------ marks

def sign_disc(cx, cy, step, r, size, bg, red=False, record=False, extra=""):
    """The step's sign in a disc on its line, as on Concept 08. On the card a documented step also carries the record
    square (M1) inside a wider capsule. A targeted step's disc takes a Pillar Red outline; the glyph stays Charcoal,
    because 15 px red text on White measures 4.17:1."""
    g = GLYPH.get(step.get("polarity"), "")
    stroke = D.RED if red else D.INK
    doc = record and step.get("evidence") == "documented"
    if doc:
        w = 2 * r + 12
        out = [f'<rect x="{cx - w / 2:.1f}" y="{cy - r:.1f}" width="{w:.1f}" height="{2 * r:.1f}" rx="{r:.1f}" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>',
               f'<rect x="{cx - w / 2 + 6:.1f}" y="{cy - 3.5:.1f}" width="7" height="7" fill="{D.INK}" data-record="1"/>',
               T(cx + 6, cy + size * 0.36, g, size, 700, D.INK, "middle", extra=' data-sign-glyph="1"')]
    else:
        out = [f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/>',
               T(cx, cy + size * 0.36, g, size, 700, D.INK, "middle", extra=' data-sign-glyph="1"')]
    return f'<g class="pill"{extra}>' + "".join(out) + "</g>"


def rounded(points, r):
    """Orthogonal polyline with one corner radius at every bend, sampled densely for textures and ticks."""
    pts = [points[0]]
    for i in range(1, len(points) - 1):
        p0, p1, p2 = points[i - 1], points[i], points[i + 1]
        d1 = D.dist(p0, p1)
        d2 = D.dist(p1, p2)
        rr = min(r, d1 / 2, d2 / 2)
        u1 = ((p1[0] - p0[0]) / d1, (p1[1] - p0[1]) / d1)
        u2 = ((p2[0] - p1[0]) / d2, (p2[1] - p1[1]) / d2)
        a = (p1[0] - u1[0] * rr, p1[1] - u1[1] * rr)
        b = (p1[0] + u2[0] * rr, p1[1] + u2[1] * rr)
        pts.append(a)
        for k in range(1, 8):
            t = k / 8
            pts.append(((1 - t) ** 2 * a[0] + 2 * (1 - t) * t * p1[0] + t * t * b[0],
                        (1 - t) ** 2 * a[1] + 2 * (1 - t) * t * p1[1] + t * t * b[1]))
        pts.append(b)
    pts.append(points[-1])
    dense = [pts[0]]
    for q in pts[1:]:
        p = dense[-1]
        n = max(1, int(D.dist(p, q) // 3))
        for k in range(1, n + 1):
            dense.append((p[0] + (q[0] - p[0]) * k / n, p[1] + (q[1] - p[1]) * k / n))
    return dense


def line(poly, step, width, color, bg, red, ticks, head=8):
    """A step's line: V7 texture (M1), arrowhead, and delay ticks on the card (M4)."""
    if red:
        color = D.RED
    base = D.trim(poly, 0, head - 0.5)
    if step.get("conceptual"):
        body = (f'<path d="{D.path_d(base)}" fill="none" stroke="{color}" stroke-width="{width + 3:.1f}" data-texture="hollow"/>'
                f'<path d="{D.path_d(base)}" fill="none" stroke="{bg}" stroke-width="{max(1.5, width - 0.5):.1f}"/>')
    else:
        dash = D.DASH.get(step["evidence"])
        da = f' stroke-dasharray="{dash}"' if dash else ""
        body = (f'<path d="{D.path_d(base)}" fill="none" stroke="{color}" stroke-width="{width}"{da} data-texture="{dash or "solid"}"'
                + (' data-red="1"' if red else "") + "/>")
    body += D.arrow_at(poly, head, head * 0.5, color)
    if ticks and step.get("delay"):
        body += D.ticks_on(poly, D.TICKS[step["delay"]], start=10, step=5, length=11, color=color)
    return body


# ------------------------------------------------------------------ layout

def box_texts(loop, model, sc, with_rules):
    out = []
    for s in loop["stations"]:
        inner = sc["bw"] - 4 - 2 * sc["pad"]
        lab = TX.balanced_wrap(s["label"], inner, sc["ls"], sc["lw"])
        rule = []
        if with_rules and s["code"]:
            inc = (model["nodes"][s["code"]]["increase_means"] or "").replace("A higher value means ", "Higher: ")
            rule = TX.wrap(inc, inner, 16, 400)
        out.append((lab, rule))
    return out


def box_height(lab, rule, sc, has_id):
    lh = round(sc["ls"] * 1.28)
    h = 2 * sc["pad"] + lh * len(lab) + (sc["ids"] + 6 if has_id else 0) + (8 + 21 * len(rule) if rule else 0)
    return max(sc["bh"], h)


def layout(loop, sc, texts, has_id, x0=0, y0=0):
    """Box rectangles and step routes for one loop at one scale. Boxes in a row share one height."""
    n = loop["n"]
    bw, hg, vg = sc["bw"], sc["hg"], sc["vg"]
    hs = [box_height(l, r, sc, has_id and s["is_variable"]) for (l, r), s in zip(texts, loop["stations"])]
    if n == 2:
        H = max(hs)
        boxes = [(x0, y0, bw, H), (x0 + bw + hg, y0, bw, H)]
    elif n == 3:
        H1 = max(hs[0], hs[1])
        boxes = [(x0, y0, bw, H1), (x0 + bw + hg, y0, bw, H1), (x0 + (bw + hg) / 2, y0 + H1 + vg, bw, hs[2])]
    else:
        H1 = max(hs[0], hs[1])
        H2 = max(hs[2], hs[3])
        boxes = [(x0, y0, bw, H1), (x0 + bw + hg, y0, bw, H1), (x0 + bw + hg, y0 + H1 + vg, bw, H2), (x0, y0 + H1 + vg, bw, H2)]
    cxs = [(b[0] + b[2] / 2, b[1] + b[3] / 2) for b in boxes]
    routes, orient = [], []
    for i in range(n):
        a, b = boxes[i], boxes[(i + 1) % n]
        ca, cb = cxs[i], cxs[(i + 1) % n]
        if n == 2:
            if i == 0:
                y = y0 + min(a[3], b[3]) / 2
                routes.append([(a[0] + a[2], y), (b[0], y)]); orient.append("top")
            else:
                yb = y0 + max(a[3], b[3]) + sc["depth"]
                routes.append([(ca[0], a[1] + a[3]), (ca[0], yb), (cb[0], yb), (cb[0], b[1] + b[3])]); orient.append("under")
        elif n == 3:
            if i == 0:
                y = y0 + a[3] / 2
                routes.append([(a[0] + a[2], y), (b[0], y)]); orient.append("top")
            elif i == 1:
                routes.append([(ca[0], a[1] + a[3]), (ca[0], cb[1]), (b[0] + b[2], cb[1])]); orient.append("right")
            else:
                routes.append([(a[0], ca[1]), (cb[0], ca[1]), (cb[0], b[1] + b[3])]); orient.append("left")
        else:
            if i == 0:
                y = y0 + a[3] / 2
                routes.append([(a[0] + a[2], y), (b[0], y)]); orient.append("top")
            elif i == 1:
                routes.append([(ca[0], a[1] + a[3]), (cb[0], b[1])]); orient.append("right")
            elif i == 2:
                y = b[1] + b[3] / 2
                routes.append([(a[0], y), (b[0] + b[2], y)]); orient.append("bottom")
            else:
                routes.append([(ca[0], a[1]), (cb[0], b[1] + b[3])]); orient.append("left")
    return boxes, routes, orient


def disc_point(route, orient):
    """Where the sign disc sits: the middle of the step's longest straight run."""
    best, bl = None, -1
    for p, q in zip(route, route[1:]):
        L = D.dist(p, q)
        if L > bl:
            best, bl = ((p[0] + q[0]) / 2, (p[1] + q[1]) / 2), L
    return best


# ------------------------------------------------------------------ the drawing

def drawing(loop, model, scale="mini", reform_id=None, bg=D.WHITE, view=None, markers=None, margin=None):
    """One loop as a Field Guide specimen. scale: mini, lead or card. Returns (svg, meta) where meta carries the
    geometry the page needs, such as marker points for the catalog head's callouts."""
    sc = SCALES[scale]
    card = scale == "card"
    has_id = sc["ids"] > 0
    texts = box_texts(loop, model, sc, with_rules=card)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    n = loop["n"]
    # margins: room for step labels on the card
    if margin is None:
        if card:
            margin = {"l": 200 if n >= 3 else 8, "r": 200 if n >= 3 else 8, "t": 150, "b": 116}
        elif scale == "lead":
            margin = {"l": 12, "r": 12, "t": 12, "b": 22}
        else:
            margin = {"l": 9, "r": 9, "t": 6, "b": 14}
    boxes, routes, orient = layout(loop, sc, texts, has_id, margin["l"], margin["t"])
    width = max(b[0] + b[2] for b in boxes) + margin["r"]
    bottom = max(b[1] + b[3] for b in boxes)
    if n == 2:
        bottom = max(bottom, max(p[1] for p in routes[1]))
    height = bottom + margin["b"]
    lines_, discs, boxes_svg, labels, marks = [], [], [], [], {}
    stroke = sc["stroke"]
    for st, rt, orn in zip(loop["steps"], routes, orient):
        red = bool(st["id"] and st["id"] in red_targets)
        poly = rounded(rt, 10 if card else 6)
        lines_.append(f'<g class="step"{D.step_attrs(st)}>' + line(poly, st, stroke, D.INK, bg, red, ticks=card,
                                                                    head=10 if card else 8) + "</g>")
        dx, dy = disc_point(rt, orn)
        discs.append(sign_disc(dx, dy, st, sc["disc"], sc["glyph"], bg, red=red, record=card,
                               extra=f' data-for="{st["id"] or "concept-" + str(st["index"])}"'))
        marks[st["id"] or f"s{st['index']}"] = (dx, dy, orn)
        if card:
            labels.append(step_label(st, rt, orn, sc, loop, boxes, margin, width, red, reform_id))
    for s, (x, y, w, h), (lab, rule) in zip(loop["stations"], boxes, texts):
        red = bool(s["code"] and s["code"] in red_targets)
        if s["is_variable"]:
            g = [f'<g class="var"{D.node_attrs(s["code"], s["label"])}' + (f' data-red="1" data-target="{reform_id}"' if red else "") + ">"]
            g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="2" fill="{D.NEWS}"'
                     + (f' stroke="{D.RED}" stroke-width="3"' if red else "") + "/>")
            g.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="5" height="{h:.1f}" fill="{D.INK}"/>')
            ty = y + sc["pad"]
            if has_id:
                g.append(T(x + 4 + sc["pad"], ty + sc["ids"] * 0.78, s["code"], sc["ids"], 800, D.INK, family="tight"))
                ty += sc["ids"] + 6
            lh = round(sc["ls"] * 1.28)
            if not has_id and not card:
                # center the label block vertically in the miniature box
                ty = y + (h - lh * len(lab)) / 2
            for i, ln in enumerate(lab):
                g.append(T(x + 4 + sc["pad"], ty + lh * i + sc["ls"] * 0.82, ln, sc["ls"], sc["lw"], D.INK))
            if rule:
                ry = ty + lh * len(lab) + 8
                for i, ln in enumerate(rule):
                    g.append(T(x + 4 + sc["pad"], ry + 21 * i + 13, ln, 16, 400, D.DEEP))
            g.append("</g>")
            boxes_svg.append("".join(g))
        else:
            # a sketched station: an open box, the chain label in words
            g = [f'<g class="sketch" data-concept-label="{D.esc(s["label"])}">',
                 f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="3" fill="{bg}" stroke="{D.INK}" stroke-width="1.25" stroke-dasharray="none"/>']
            lh = round(sc["ls"] * 1.28)
            ty = y + (h - lh * len(lab)) / 2
            for i, ln in enumerate(lab):
                g.append(T(x + sc["pad"], ty + lh * i + sc["ls"] * 0.82, ln, sc["ls"], sc["lw"], D.INK))
            g.append("</g>")
            boxes_svg.append("".join(g))
        marks["box:" + (s["code"] or s["label"])] = (x, y, w, h)
    marker_svg = ""
    if markers:
        marker_svg = "".join(markers(marks))
    label = f'Loop {loop["id"]}, Field Guide {scale} drawing. {loop["how_to_read"]}'
    v = view or f"fg-{scale}"
    attrs = f' data-loop="{loop["id"]}" data-direction="field-guide"' + (f' data-reform="{reform_id}"' if reform_id else "")
    svg = svg_doc(width, height, "".join(lines_) + "".join(boxes_svg) + "".join(discs) + "".join(labels) + marker_svg, label, v, attrs,
                  bg=None)
    return svg, {"w": width, "h": height, "marks": marks, "boxes": boxes, "routes": routes, "orient": orient}


def step_label(st, rt, orn, sc, loop, boxes, margin, width, red, reform_id):
    """Card labels: the step's ID with the weakest-step note, its V7 name, then grade and delay in words."""
    gw = D.GRADE_WORD[st["evidence"]] + ("  ·  " + st["type"] if st["type"] != "causal" else "")
    head = st["id"] + ("  ·  least certain step" if st["id"] in loop["weakest"] else "")
    tail = D.DELAY_WORD[st["delay"]] + (f"  ·  {reform_id} acts here" if red else "")
    if orn == "top":
        (x1, y), (x2, _) = rt[0], rt[-1]
        mx = (x1 + x2) / 2
        lines = TX.balanced_wrap(st["name"], (x2 - x1) - 24, 16, 600)
        tails = TX.balanced_wrap(gw + "  ·  " + tail, (x2 - x1) - 24, 13, 400)
        rows = [(head, 13, 700, D.INK)] + [(l, 16, 600, D.INK) for l in lines] + [(t, 13, 400, D.DEEP) for t in tails]
        y_end = y - 26
        blk = []
        for i, (t, s, wgt, col) in enumerate(reversed(rows)):
            blk.append(T(mx, y_end - i * 21, t, s, wgt, col, "middle"))
    elif orn == "under":
        yb = rt[1][1]
        mx = (rt[1][0] + rt[2][0]) / 2
        lines = TX.balanced_wrap(st["name"], 440, 16, 600)
        rows = [(head, 13, 700, D.INK)] + [(l, 16, 600, D.INK) for l in lines] + [(gw + "  ·  " + tail, 13, 400, D.DEEP)]
        blk = [T(mx, yb + 36 + i * 21, t, s, wgt, col, "middle") for i, (t, s, wgt, col) in enumerate(rows)]
    elif orn == "bottom":
        (x1, y), (x2, _) = rt[0], rt[-1]
        mx = (x1 + x2) / 2
        lines = TX.balanced_wrap(st["name"], abs(x1 - x2) - 24, 16, 600)
        rows = [(head, 13, 700, D.INK)] + [(l, 16, 600, D.INK) for l in lines] + [(gw, 13, 400, D.DEEP), (tail, 13, 400, D.DEEP)]
        blk = [T(mx, y + 36 + i * 21, t, s, wgt, col, "middle") for i, (t, s, wgt, col) in enumerate(rows)]
    else:
        # vertical runs: label on the outside of the line, set against the drawing's edge
        xs = [p[0] for p in rt]
        ys = [p[1] for p in rt]
        x_line = xs[0] if orn == "right" else xs[-1]
        ymid = (min(ys) + max(ys)) / 2
        right = orn == "right"
        avail = (width - x_line - 22) if right else (x_line - 22)
        lines = TX.balanced_wrap(st["name"], min(avail, 200), 16, 600)
        rows = [(head, 13, 700, D.INK)] + [(l, 16, 600, D.INK) for l in lines] + [(gw, 13, 400, D.DEEP), (tail, 13, 400, D.DEEP)]
        y_start = ymid - (len(rows) * 21) / 2 + 14
        xx = x_line + 22 if right else x_line - 22
        blk = [T(xx, y_start + i * 21, t, s, wgt, col, "start" if right else "end") for i, (t, s, wgt, col) in enumerate(rows)]
    return f'<g class="steplabel" data-for="{st["id"]}">' + "".join(blk) + "</g>"


# ------------------------------------------------------------------ the phone card: boxes stacked, return up the left

def phone_drawing(loop, model, reform_id=None, bg=D.WHITE, w=326, view="fg-card-phone", markers=None, with_meta=False):
    sc = dict(SCALES["card"])
    left = 40
    bw = w - left
    sc["bw"] = bw
    texts = box_texts(loop, model, sc, with_rules=True)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    gap = 150
    y = 8
    boxes = []
    for (lab, rule), s in zip(texts, loop["stations"]):
        h = box_height(lab, rule, sc, s["is_variable"])
        boxes.append((left, y, bw, h))
        y += h + gap
    total = boxes[-1][1] + boxes[-1][3] + 120
    lines_, discs, boxes_svg, labels = [], [], [], []
    xl = left + 34
    for i, st in enumerate(loop["steps"]):
        a = boxes[i]
        red = bool(st["id"] and st["id"] in red_targets)
        if not st["closing"]:
            b = boxes[i + 1]
            rt = [(xl, a[1] + a[3]), (xl, b[1])]
            dx, dy = xl, (a[1] + a[3] + b[1]) / 2
            lab_x, lab_y0 = xl + 26, a[1] + a[3] + 26
            lines = TX.balanced_wrap(st["name"], w - lab_x - 4, 15, 600)
            rows = [(st["id"] + ("  ·  least certain" if st["id"] in loop["weakest"] else ""), 13, 700, D.INK)] + \
                   [(l, 15, 600, D.INK) for l in lines] + \
                   [(D.GRADE_WORD[st["evidence"]] + "  ·  " + D.DELAY_WORD[st["delay"]], 13, 400, D.DEEP)]
            if red:
                rows.append((f"{reform_id} acts here", 13, 700, D.INK))
            labels.append(f'<g class="steplabel" data-for="{st["id"]}">' + "".join(
                T(lab_x, lab_y0 + 20 * k, t, s, wt, c) for k, (t, s, wt, c) in enumerate(rows)) + "</g>")
        else:
            first = boxes[0]
            ya = a[1] + a[3] / 2
            yb = first[1] + min(first[3] / 2, 40)
            rt = [(left, ya), (10, ya), (10, yb), (left, yb)]
            dx, dy = 10, (ya + yb) / 2
            rows = [(st["id"] + "  ·  the return line" + ("  ·  least certain" if st["id"] in loop["weakest"] else ""), 13, 700, D.INK)] + \
                   [(l, 15, 600, D.INK) for l in TX.balanced_wrap(st["name"], w - left - 4, 15, 600)] + \
                   [(D.GRADE_WORD[st["evidence"]] + "  ·  " + D.DELAY_WORD[st["delay"]], 13, 400, D.DEEP)]
            if red:
                rows.append((f"{reform_id} acts here", 13, 700, D.INK))
            ly = a[1] + a[3] + 28
            labels.append(f'<g class="steplabel" data-for="{st["id"]}">' + "".join(
                T(left, ly + 20 * k, t, s, wt, c) for k, (t, s, wt, c) in enumerate(rows)) + "</g>")
            total = max(total, ly + 20 * len(rows) + 10)
        poly = rounded(rt, 10)
        lines_.append(f'<g class="step"{D.step_attrs(st)}>' + line(poly, st, 2.5, D.INK, bg, red, ticks=True, head=10) + "</g>")
        discs.append(sign_disc(dx, dy, st, 12, 15, bg, red=red, record=True, extra=f' data-for="{st["id"]}"'))
    for s, (x, y, w_, h), (lab, rule) in zip(loop["stations"], boxes, texts):
        red = s["code"] in red_targets
        g = [f'<g class="var"{D.node_attrs(s["code"], s["label"])}' + (f' data-red="1" data-target="{reform_id}"' if red else "") + ">",
             f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h:.1f}" rx="2" fill="{D.NEWS}"'
             + (f' stroke="{D.RED}" stroke-width="3"' if red else "") + "/>",
             f'<rect x="{x:.1f}" y="{y:.1f}" width="5" height="{h:.1f}" fill="{D.INK}"/>',
             T(x + 20, y + 16 + 13, s["code"], 16, 800, D.INK, family="tight")]
        ty = y + 16 + 22
        for i, ln in enumerate(lab):
            g.append(T(x + 20, ty + 20 * i + 13, ln, 16, 600, D.INK))
        ry = ty + 20 * len(lab) + 8
        for i, ln in enumerate(rule):
            g.append(T(x + 20, ry + 20 * i + 12, ln, 15, 400, D.DEEP))
        g.append("</g>")
        boxes_svg.append("".join(g))
    label = f'Loop {loop["id"]}, Field Guide phone drawing. {loop["how_to_read"]}'
    attrs = f' data-loop="{loop["id"]}" data-direction="field-guide"' + (f' data-reform="{reform_id}"' if reform_id else "")
    marker_svg = "".join(markers({"boxes": boxes, "xl": xl, "left": left})) if markers else ""
    svg = svg_doc(w, total, "".join(lines_) + "".join(boxes_svg) + "".join(discs) + "".join(labels) + marker_svg, label, view, attrs)
    return (svg, {"boxes": boxes, "xl": xl, "h": total}) if with_meta else svg


def phone_mini(loop, model, w=326):
    """The catalog miniature on a phone: the phone card's stacked drawing at catalog size, names only."""
    left = 30
    bw = w - left
    gap = 34
    bh = 40
    lab_w = bw - 5 - 2 * 10
    texts = [TX.balanced_wrap(s["label"], lab_w, 13, 600) for s in loop["stations"]]
    y = 4
    boxes = []
    for lab in texts:
        h = max(bh, 16 * len(lab) + 18)
        boxes.append((left, y, bw, h))
        y += h + gap
    total = boxes[-1][1] + boxes[-1][3] + 8
    lines_, discs, boxes_svg = [], [], []
    xl = left + 40
    for i, st in enumerate(loop["steps"]):
        a = boxes[i]
        if not st["closing"]:
            b = boxes[i + 1]
            rt = [(xl, a[1] + a[3]), (xl, b[1])]
            dx, dy = xl, (a[1] + a[3] + b[1]) / 2
        else:
            first = boxes[0]
            ya = a[1] + a[3] / 2
            yb = first[1] + first[3] / 2
            rt = [(left, ya), (8, ya), (8, yb), (left, yb)]
            dx, dy = 8, (ya + yb) / 2
        poly = rounded(rt, 6)
        lines_.append(f'<g class="step"{D.step_attrs(st)}>' + line(poly, st, 2.0, D.INK, D.WHITE, False, ticks=False, head=8) + "</g>")
        discs.append(sign_disc(dx, dy, st, 8, 13, D.WHITE, extra=f' data-for="{st["id"] or "concept-" + str(st["index"])}"'))
    for s, (x, y, w_, h), lab in zip(loop["stations"], boxes, texts):
        if s["is_variable"]:
            g = [f'<g class="var"{D.node_attrs(s["code"], s["label"])}>', f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h:.1f}" rx="2" fill="{D.NEWS}"/>',
                 f'<rect x="{x:.1f}" y="{y:.1f}" width="5" height="{h:.1f}" fill="{D.INK}"/>']
        else:
            g = [f'<g class="sketch" data-concept-label="{D.esc(s["label"])}">', f'<rect x="{x:.1f}" y="{y:.1f}" width="{w_:.1f}" height="{h:.1f}" rx="2" fill="{D.WHITE}" stroke="{D.INK}" stroke-width="1.25"/>']
        ty = y + (h - 16 * len(lab)) / 2
        for i, ln in enumerate(lab):
            g.append(T(x + 15, ty + 16 * i + 11, ln, 13, 600, D.INK))
        g.append("</g>")
        boxes_svg.append("".join(g))
    label = f'Loop {loop["id"]}, Field Guide phone miniature. {loop["how_to_read"]}'
    return svg_doc(w, total, "".join(lines_) + "".join(boxes_svg) + "".join(discs), label, "fg-mini-phone",
                   f' data-loop="{loop["id"]}" data-direction="field-guide"')
