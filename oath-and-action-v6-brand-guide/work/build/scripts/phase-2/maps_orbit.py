"""Direction 1, Orbit: a loop is a closed figure, and a slow step bows outward.

Geometry: n stations on a base circle, clockwise from the top. Each step is a circular arc from one station to the
next, bowing outward by its delay class (under 2 years 0.14, 2 to 10 years 0.27, over 10 years 0.42 of the chord).
A sketched loop with no numbered steps sits on the plain base circle in the hollow line. The miniature and the card
call the same geometry at two radii; only marks keep their absolute size.
"""
import math

import maps_draw as D

BOW = {"S": 0.14, "M": 0.27, "L": 0.42}


def stations_xy(n, cx, cy, r0):
    return [(cx + r0 * math.cos(-math.pi / 2 + i * 2 * math.pi / n), cy + r0 * math.sin(-math.pi / 2 + i * 2 * math.pi / n))
            for i in range(n)]


def step_arcs(loop, cx, cy, r0):
    n = loop["n"]
    P = stations_xy(n, cx, cy, r0)
    arcs = []
    for i, st in enumerate(loop["steps"]):
        a, b = P[i], P[(i + 1) % n]
        c = D.dist(a, b)
        if st["conceptual"]:
            # sit on the base circle: sagitta of the circle's own arc between the two stations
            half = math.pi / n
            sag = r0 * (1 - math.cos(half)) if n > 2 else r0
        else:
            sag = BOW[st["delay"]] * c
        arcs.append(D.arc_through(a, b, sag, 96))
    return P, arcs


def _outward(cx, cy, x, y):
    vx, vy = x - cx, y - cy
    d = math.hypot(vx, vy) or 1
    return vx / d, vy / d


def _clamp_text(x, anchor, text, size, weight, w, pad=4):
    tw = D.text_w(text, size, weight)
    if anchor == "start":
        x = min(x, w - pad - tw)
    elif anchor == "end":
        x = max(x, pad + tw)
    else:
        x = min(max(x, pad + tw / 2), w - pad - tw / 2)
    return x


def mini(loop, w=236, h=206, r0=None, red_targets=None, bg=D.NEWS, only_reform=None, weakest_style="word"):
    """Catalog miniature. Ink only on the catalog: a reform target is an ink pointer, since the catalog names
    no single reform and so carries no working red (Rule 05.3). red_targets draws one reform's targets in red."""
    n = loop["n"]
    r0 = r0 or {2: 58, 3: 60, 4: 62}[n]
    cx, cy = w / 2 + 6, h / 2 + (6 if n == 3 else 2)
    P, arcs = step_arcs(loop, cx, cy, r0)
    rn = 13
    red_targets = red_targets or set()
    if only_reform:
        # a reform view marks that reform's targets only
        loop = dict(loop, targets={k: [only_reform] for k, v in loop["targets"].items() if only_reform in v}
                    | {k: [only_reform] for k in red_targets})
    body, pills, nodes, notes, ptr = [], [], [], [], []
    for st, arc in zip(loop["steps"], arcs):
        rnf = 13 if loop["stations"][st["index"] - 1]["is_variable"] else 6
        rnt = 13 if loop["stations"][st["index"] % n]["is_variable"] else 6
        tg = loop["targets"].get(st["id"]) if st["id"] else None
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(arc, st, start_gap=rnf + 3, end_gap=rnt + 3, red=red, bg=bg) + "</g>")
        (mx, my), _ = D.mid(arc)
        weak_pill = weakest_style == "pill" and st["id"] in loop["weakest"]
        p, pw = D.sign_pill(mx, my, st, bg=D.INK if weak_pill else bg, ink=bg if weak_pill else D.INK,
                            extra=f' data-for="{st["id"] or "concept-" + str(st["index"])}"' + (f' data-weakest="{st["id"]}"' if weak_pill else ""))
        pills.append(p)
        ux, uy = _outward(cx, cy, mx, my)
        reach = pw / 2 * abs(ux) + 10 * abs(uy) + 3
        if tg:
            ptr.append(D.pointer(mx + ux * reach, my + uy * reach, ux, uy, red=red, ids=tg, at=st["id"]))
            reach += 13
        if st["id"] in loop["weakest"] and weakest_style == "word":
            tx, ty = mx + ux * (reach + 6), my + uy * (reach + 6)
            anchor = "start" if ux > 0.35 else ("end" if ux < -0.35 else "middle")
            ty = ty + 4.5 + (8 if uy > 0.6 else (-4 if uy < -0.6 else 0))
            if ty > h - 5 or ty < 14:
                # no room above or below: set the word beside the label pill instead
                side = 1 if mx <= w - 80 else -1
                tx, ty = mx + side * (pw / 2 + 6), my + 4.5
                anchor = "start" if side > 0 else "end"
            tx2 = _clamp_text(tx, anchor, "weakest", 13, 400, w)
            if abs(tx2 - tx) > 3:
                # pushed against the edge: set it under the label pill instead
                tx2, ty, anchor = mx, my + 25, "middle"
                tx2 = _clamp_text(tx2, anchor, "weakest", 13, 400, w)
            notes.append(D.T(tx2, ty, "weakest", 13, 400, D.DEEP, anchor, italic=True,
                             extra=f' data-weakest="{st["id"]}" stroke="{bg}" stroke-width="4" paint-order="stroke" stroke-linejoin="round"'))
    for s, (x, y) in zip(loop["stations"], P):
        if s["is_variable"]:
            tg = loop["targets"].get(s["code"])
            red = s["code"] in red_targets
            if tg:
                ux, uy = _outward(cx, cy, x, y)
                ptr.append(D.pointer(x + ux * (rn + 3), y + uy * (rn + 3), ux, uy, red=red, ids=tg, at=s["code"]))
            nodes.append(f'<g class="var"{D.node_attrs(s["code"], s["label"])}><circle cx="{x:.1f}" cy="{y:.1f}" r="{rn}" fill="{D.INK}"/>'
                         + D.T(x, y + 4.6, s["code"], 13, 700, bg, "middle") + "</g>")
        else:
            nodes.append(f'<g class="sketch" data-concept-label="{D.esc(s["label"])}"><circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{bg}" stroke="{D.INK}" stroke-width="1.5"/></g>')
    km = ""
    label = f'Loop {loop["id"]}, orbit miniature. {loop["kind_word"]} loop. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(body) + "".join(nodes) + "".join(pills) + "".join(ptr) + "".join(notes) + km, label,
                     "orbit-mini", f' data-loop="{loop["id"]}" data-direction="orbit"', bg=None if bg == D.NEWS else bg)


def card_figure(loop, model, reform_id=None, w=760, h=660, r0=178, bg=D.WHITE, label_w=196):
    """The loop card's drawing: the miniature's geometry at a larger radius, with full labels outside each arc.
    Red on White marks the targets of one reform, the point the card's headline names (Rule 05.3)."""
    n = loop["n"]
    cx, cy = w / 2, h / 2 + 4
    P, arcs = step_arcs(loop, cx, cy, r0)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    rn = 27
    body, pills, nodes, labels = [], [], [], []
    for st, arc in zip(loop["steps"], arcs):
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(arc, st, start_gap=rn + 4, end_gap=rn + 4, red=red, bg=bg, width=2.5) + "</g>")
        (mx, my), _ = D.mid(arc)
        p, pw = D.sign_pill(mx, my, st, size=14, bg=bg, extra=f' data-for="{st["id"]}"')
        pills.append(p)
        ux, uy = _outward(cx, cy, mx, my)
        reach = pw / 2 * abs(ux) + 10 * abs(uy) + 4
        if red:
            pills.append(D.pointer(mx + ux * reach, my + uy * reach, ux, uy, red=True, ids=[reform_id], size=10, at=st["id"]))
            reach += 22
        lx, ly = mx + ux * (reach + 8), my + uy * (reach + 8)
        anchor = "start" if ux > 0.3 else ("end" if ux < -0.3 else "middle")
        lines = D.wrap(st["name"], label_w, 15, 600) if st["name"] else []
        head = st["id"] + ("  ·  weakest step" if st["id"] in loop["weakest"] else "")
        gw = D.GRADE_WORD[st["evidence"]] + ("  ·  " + st["type"] if st["type"] != "causal" else "")
        blk_lines = [(head, 13, 700, D.INK)] + [(ln, 15, 600, D.INK) for ln in lines] + [(gw, 13, 400, D.INK), (D.DELAY_WORD[st["delay"]], 13, 400, D.DEEP)]
        total = 18 * len(blk_lines)
        if anchor == "middle":
            y = ly + 14 if uy > 0 else ly - total + 8
        else:
            y = ly - total / 2 + 12
        blk = []
        for text, size, wt, col in blk_lines:
            blk.append(D.T(_clamp_text(lx, anchor, text, size, wt, w, 6), y, text, size, wt, col, anchor))
            y += 18
        labels.append(f'<g class="steplabel" data-for="{st["id"]}">' + "".join(blk) + "</g>")
    for s, (x, y) in zip(loop["stations"], P):
        red = s["code"] in red_targets
        g = [f'<g class="var"{D.node_attrs(s["code"], s["label"])}' + (f' data-target="{reform_id}" data-red="1"' if red else "") + ">"]
        if red:
            g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rn + 7}" fill="none" stroke="{D.RED}" stroke-width="3.5"/>')
        g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rn}" fill="{D.INK}"/>' + D.T(x, y + 6.2, s["code"], 18, 800, bg, "middle", display=True))
        ux, uy = _outward(cx, cy, x, y)
        if abs(uy) > abs(ux):
            ty = y - rn - 18 if uy < 0 else y + rn + 28
            lines = D.wrap(s["label"], 260, 16, 700)
            for i, ln in enumerate(lines[:2]):
                yy = ty - 20 * (len(lines[:2]) - 1 - i) if uy < 0 else ty + 20 * i
                g.append(D.T(_clamp_text(x, "middle", ln, 16, 700, w), yy, ln, 16, 700, D.INK, "middle"))
        else:
            anchor = "start" if ux > 0 else "end"
            tx = x + (rn + 12) * (1 if ux > 0 else -1)
            lines = D.wrap(s["label"], 150, 16, 700)
            for i, ln in enumerate(lines[:3]):
                g.append(D.T(_clamp_text(tx, anchor, ln, 16, 700, w), y + 6 + 20 * (i - (len(lines[:3]) - 1) / 2), ln, 16, 700, D.INK, anchor))
        g.append("</g>")
        nodes.append("".join(g))
    km = D.kind_mark(cx, cy - 12, loop["type"], r=17)
    kw = D.T(cx, cy + 30, loop["kind_gloss"], 15, 700, D.INK, "middle")
    label = f'Loop {loop["id"]}, orbit card drawing. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(body) + km + kw + "".join(nodes) + "".join(pills) + "".join(labels), label,
                     "orbit-card", f' data-loop="{loop["id"]}" data-direction="orbit"' + (f' data-reform="{reform_id}"' if reform_id else ""), bg=bg)


# ------------------------------------------------------------------ whole system: the turning ring

RING_ORDER = ["X", "A", "B", "C", "D", "E", "TC", "EC"]


def ring_positions(model, cx, cy, r):
    """Rule: every variable sits on one ring, grouped by area, clockwise in the order effects mostly travel
    (A, B, C, D, E), with technology and the economy closing the circle back to A and the outside drivers at the top."""
    N = model["nodes"]
    slots = []
    for a in RING_ORDER:
        ks = [k for k in model["order"] if N[k]["area"] == a]
        slots.extend(ks)
        slots.append(None)
        slots.append(None)
    step = 2 * math.pi / len(slots)
    ang, XY = {}, {}
    off = -math.pi / 2 - step * 2.5
    for i, k in enumerate(slots):
        if k:
            ang[k] = off + i * step
            XY[k] = (cx + r * math.cos(ang[k]), cy + r * math.sin(ang[k]))
    return XY, ang


def whole_map(model, w=1216, h=1216, highlight_reform=None, bg=None, focus_loop=None):
    """The whole system on one turning ring. Each connection bends to its left, more when it is slower (the orbit
    rule at system scale), so links that run forward, clockwise, hug the rim and the steps that come back cross the
    middle. Loop connections in Charcoal, the rest in Stone; texture keeps the V7 grade."""
    N, L = model["nodes"], model["links"]
    surface = bg or D.NEWS
    cx, cy = w / 2, h / 2
    R = 326
    XY, ang = ring_positions(model, cx, cy, R)
    red_targets = set(model["reforms"][highlight_reform]["targets"]) if highlight_reform else set()
    focus = set(model["loops"][focus_loop]["steps"][i]["id"] for i in range(model["loops"][focus_loop]["n"])) if focus_loop else None
    in_loop = {k for k, l in L.items() if l["loops"]}
    ctx, emph, reds = [], [], []
    for k, l in L.items():
        a, b = XY[l["from"]], XY[l["to"]]
        c = D.dist(a, b)
        sag = min(0.5 * BOW[l["delay"]] * c, 44)
        poly = D.arc_through(a, b, sag, 72)
        red = k in red_targets
        strong = (k in focus) if focus is not None else (k in in_loop or red)
        g = (f'<g class="link"{D.link_attrs(l)}' + (f' data-target="{highlight_reform}" data-red="1"' if red else "") + ">"
             + D.connection(poly, l, start_gap=12, end_gap=12, width=2 if strong else 1.25,
                            color=D.INK if strong else D.STONE, red=red, bg=surface, ticks=False) + "</g>")
        (reds if red else emph if strong else ctx).append(g)
    nodes, labs = [], []
    for k in model["order"]:
        x, y = XY[k]
        n = N[k]
        red = k in red_targets
        filled = n["layer"] == "core" and n["area"] != "X"
        ring = f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="none" stroke="{D.RED}" stroke-width="3"/>' if red else ""
        disc = (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="10" fill="{D.INK}"/>' if filled else
                f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{surface}" stroke="{D.INK}" stroke-width="1.75"/>')
        nodes.append(f'<g class="var"{D.node_attrs(k)}' + (f' data-target="{highlight_reform}" data-red="1"' if red else "") + f">{ring}{disc}</g>")
        ca, sa = math.cos(ang[k]), math.sin(ang[k])
        deg = math.degrees(ang[k])
        flip = ca < 0
        lx, ly = cx + (R + 34) * ca, cy + (R + 34) * sa
        rot = deg + 180 if flip else deg
        anchor = "end" if flip else "start"
        name = n["short"] or n["title"]
        if len(name) > 34:
            name = D.wrap(name, 210, 13, 400)[0].rstrip(",") + "\u2026"
        tr = f' transform="rotate({rot:.2f} {lx:.1f} {ly:.1f})"'
        blk = [f'<text x="{lx:.1f}" y="{ly + 4.5:.1f}" class="mt" font-size="13" fill="{D.INK}" text-anchor="{anchor}"{tr}>'
               + (f'<tspan class="mb">{k}</tspan> {D.esc(name)}' if not flip else f'{D.esc(name)} <tspan class="mb">{k}</tspan>') + "</text>"]
        labs.append("".join(blk))
    caps = []
    for a in RING_ORDER:
        ks = [k for k in model["order"] if N[k]["area"] == a]
        am = math.atan2(sum(math.sin(ang[k]) for k in ks), sum(math.cos(ang[k]) for k in ks))
        rr = R - 46
        x, y = cx + rr * math.cos(am), cy + rr * math.sin(am)
        caps.append(D.T(x, y + 7, a, 20, 800, D.DEEP, "middle", display=True))
    ax, ay = 40, h - 92
    arrow = D.arc_through((ax, ay + 40), (ax + 120, ay + 40), 22, 40)
    note = (f'<path d="{D.path_d(D.trim(arrow, 0, 8))}" fill="none" stroke="{D.DEEP}" stroke-width="1.5"/>' + D.arrow_at(arrow, 8, 4, D.DEEP)
            + D.T(ax + 140, ay + 30, "Effects mostly travel clockwise, A to E.", 14, 600, D.DEEP)
            + D.T(ax + 140, ay + 48, "The steps that come back cross the middle.", 14, 600, D.DEEP))
    body = "".join(ctx) + "".join(emph) + "".join(reds) + note + "".join(caps) + "".join(nodes) + "".join(labs)
    label = ("Whole system, orbit ring: 51 variables and 118 connections on one ring, grouped by area in the order effects "
             "mostly travel. Each connection bends to its left, more when it is slower.")
    return D.svg_doc(w, h, body, label, "orbit-map", ' data-direction="orbit"' + (f' data-reform="{highlight_reform}"' if highlight_reform else ""), bg=bg)
