"""Direction 1, Orbit: a loop is a closed figure, and a slow step bows outward.

Geometry: n stations on a base circle, clockwise from the top. Each step is a circular arc from one station to the
next, bowing outward by its delay class (under 2 years 0.08, 2 to 10 years 0.22, over 10 years 0.38 of the chord).
A sketched loop with no numbered steps sits on the plain base circle in the hollow line. The miniature and the card
call the same geometry at two radii; only marks keep their absolute size.
"""
import math

import maps_draw as D

BOW = {"S": 0.08, "M": 0.22, "L": 0.38}


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


def mini(loop, w=236, h=206, r0=None, red_targets=None, show_weakest=True):
    """Catalog miniature. Ink only; reform targets as ink rings (no working red on the catalog)."""
    n = loop["n"]
    r0 = r0 or {2: 56, 3: 58, 4: 60}[n]
    cx, cy = w / 2, h / 2 + (4 if n == 3 else 0)
    P, arcs = step_arcs(loop, cx, cy, r0)
    rn = 13 if not loop["conceptual"] else 6
    body, pills, nodes, notes = [], [], [], []
    red_targets = red_targets or set()
    for st, arc in zip(loop["steps"], arcs):
        rnf = 13 if (loop["stations"][st["index"] - 1]["is_variable"]) else 7
        rnt = 13 if (loop["stations"][st["index"] % n]["is_variable"]) else 7
        tg = loop["targets"].get(st["id"]) if st["id"] else None
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(arc, st, start_gap=rnf + 3, end_gap=rnt + 3, red=red) + "</g>")
        (mx, my), _ = D.mid(arc)
        p, pw = D.sign_pill(mx, my, st, ring=tg, ring_red=red, extra=f' data-for="{st["id"] or "concept-" + str(st["index"])}"')
        pills.append(p)
        if show_weakest and st["id"] in loop["weakest"]:
            vx, vy = mx - cx, my - cy
            d = math.hypot(vx, vy) or 1
            ux, uy = vx / d, vy / d
            tx, ty = mx + ux * 26, my + uy * 22
            anchor = "start" if ux > 0.35 else ("end" if ux < -0.35 else "middle")
            notes.append(D.T(tx, ty + 4, "weakest", 13, 400, D.DEEP, anchor, italic=True, extra=f' data-weakest="{st["id"]}"'))
    for s, (x, y) in zip(loop["stations"], P):
        if s["is_variable"]:
            tg = loop["targets"].get(s["code"])
            red = s["code"] in red_targets
            ring = D.target_ring_circle(x, y, rn + 5, red=red, ids=tg) if tg else ""
            nodes.append(f'<g class="var"{D.node_attrs(s["code"], s["label"])}>{ring}<circle cx="{x:.1f}" cy="{y:.1f}" r="{rn}" fill="{D.INK}"/>'
                         + D.T(x, y + 4.6, s["code"], 13, 700, D.NEWS, "middle") + "</g>")
        else:
            nodes.append(f'<g class="sketch" data-concept-label="{D.esc(s["label"])}"><circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{D.NEWS}" stroke="{D.INK}" stroke-width="1.5"/></g>')
    km = D.kind_mark(cx, cy, loop["type"], r=9)
    label = f'Loop {loop["id"]}, orbit miniature. {loop["kind_word"]} loop. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(body) + km + "".join(nodes) + "".join(pills) + "".join(notes), label,
                     "orbit-mini", f' data-loop="{loop["id"]}" data-direction="orbit"')


def card_figure(loop, model, reform_id=None, w=720, h=600, r0=170, compact=False):
    """The loop card's drawing. Same geometry as the miniature at a larger radius, with full labels outside each arc.
    Red marks the targets of one reform (Rule 05.3: the point the headline names)."""
    n = loop["n"]
    cx, cy = w / 2, h / 2 + 6
    P, arcs = step_arcs(loop, cx, cy, r0)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    rn = 26
    body, pills, nodes, labels = [], [], [], []
    for st, arc in zip(loop["steps"], arcs):
        red = bool(st["id"] and st["id"] in red_targets)
        tg = loop["targets"].get(st["id"]) if st["id"] else None
        body.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(arc, st, start_gap=rn + 4, end_gap=rn + 4, red=red) + "</g>")
        (mx, my), _ = D.mid(arc)
        p, pw = D.sign_pill(mx, my, st, ring=tg if red else None, ring_red=red, extra=f' data-for="{st["id"]}"')
        pills.append(p)
        # label block outside the apex
        vx, vy = mx - cx, my - cy
        d = math.hypot(vx, vy) or 1
        ux, uy = vx / d, vy / d
        lx, ly = mx + ux * 30, my + uy * 30
        anchor = "start" if ux > 0.3 else ("end" if ux < -0.3 else "middle")
        if anchor == "middle":
            ly += 14 if uy > 0 else -40
        else:
            ly -= 18
        width = 190
        lines = D.wrap(st["name"], width, 14, 600) if st["name"] else []
        y = ly
        blk = [D.T(lx, y, st["id"] + ("  weakest step" if st["id"] in loop["weakest"] else ""), 13, 700, D.INK, anchor)]
        for ln in lines:
            y += 18
            blk.append(D.T(lx, y, ln, 14, 600, D.INK, anchor))
        y += 18
        gw = D.GRADE_WORD[st["evidence"]] + (" · " + st["type"] if st["type"] not in ("causal",) else "")
        blk.append(D.T(lx, y, gw, 13, 400, D.INK, anchor))
        y += 17
        blk.append(D.T(lx, y, D.DELAY_WORD[st["delay"]], 13, 400, D.DEEP, anchor))
        labels.append(f'<g class="steplabel" data-for="{st["id"]}">' + "".join(blk) + "</g>")
    for s, (x, y) in zip(loop["stations"], P):
        red = s["code"] in red_targets
        tg = loop["targets"].get(s["code"])
        ring = D.target_ring_circle(x, y, rn + 7, red=True, ids=tg) if red else ""
        nodes.append(f'<g class="var"{D.node_attrs(s["code"], s["label"])}>{ring}<circle cx="{x:.1f}" cy="{y:.1f}" r="{rn}" fill="{D.INK}"/>'
                     + D.T(x, y + 6, s["code"], 17, 800, D.NEWS, "middle", display=True) + "</g>")
        # station name beside the disc, away from the centre
        vx, vy = x - cx, y - cy
        if abs(vy) > abs(vx):
            ty = y - rn - 14 if vy < 0 else y + rn + 24
            nodes.append(D.T(x, ty, s["label"], 15, 700, D.INK, "middle"))
        else:
            tx = x + rn + 10 if vx > 0 else x - rn - 10
            nodes.append(D.T(tx, y + 5, s["label"], 15, 700, D.INK, "start" if vx > 0 else "end"))
    km = D.kind_mark(cx, cy - 8, loop["type"], r=16)
    kw = D.T(cx, cy + 28, loop["kind_gloss"], 14, 600, D.INK, "middle")
    label = f'Loop {loop["id"]}, orbit card drawing. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(body) + km + kw + "".join(nodes) + "".join(pills) + "".join(labels), label,
                     "orbit-card", f' data-loop="{loop["id"]}" data-direction="orbit"' + (f' data-reform="{reform_id}"' if reform_id else ""))


# ------------------------------------------------------------------ whole system: the layered dial

def whole_map(model, w=1216, h=1160, highlight_reform=None):
    """Core variables on an inner ring by area; outside drivers, economy and technology on an outer ring placed
    near what they touch. Loop connections in Charcoal, the rest in Stone; every connection keeps its texture."""
    N, L = model["nodes"], model["links"]
    cx, cy = w / 2, h / 2 + 10
    Rc, Ro = 285, 470
    core = [k for k in model["order"] if N[k]["layer"] == "core" and N[k]["area"] != "X"]
    outer = [k for k in model["order"] if k not in core]
    # inner angles with gaps between areas
    slots, prev = [], None
    for k in core:
        a = N[k]["area"]
        if prev is not None and a != prev:
            slots.append(None)
        slots.append(k)
        prev = a
    slots.append(None)
    step = 2 * math.pi / len(slots)
    ang = {}
    for i, k in enumerate(slots):
        if k:
            ang[k] = -math.pi / 2 + (i + 0.5) * step
    # outer angles: circular mean of core neighbours, then spread to a minimum separation
    def neighbours(k):
        out = []
        for l in L.values():
            if l["from"] == k and l["to"] in ang:
                out.append(ang[l["to"]])
            if l["to"] == k and l["from"] in ang:
                out.append(ang[l["from"]])
        return out
    pref = {}
    for k in outer:
        nb = neighbours(k)
        if nb:
            pref[k] = math.atan2(sum(math.sin(a) for a in nb), sum(math.cos(a) for a in nb))
    # layer-only nodes: place next to their own layer's mean
    for _ in range(3):
        for k in outer:
            if k in pref:
                continue
            nb = []
            for l in L.values():
                o = l["to"] if l["from"] == k else (l["from"] if l["to"] == k else None)
                if o in pref:
                    nb.append(pref[o])
            if nb:
                pref[k] = math.atan2(sum(math.sin(a) for a in nb), sum(math.cos(a) for a in nb))
    for k in outer:
        pref.setdefault(k, 0)
    order_o = sorted(outer, key=lambda k: (pref[k] + math.pi / 2) % (2 * math.pi))
    sep = 2 * math.pi / (len(outer) + 2)
    pos = [(pref[k] + math.pi / 2) % (2 * math.pi) for k in order_o]
    for _ in range(200):
        moved = False
        for i in range(len(pos) - 1):
            if pos[i + 1] - pos[i] < sep:
                m = (pos[i] + pos[i + 1]) / 2
                pos[i], pos[i + 1] = m - sep / 2, m + sep / 2
                moved = True
        if not moved:
            break
    for k, p in zip(order_o, pos):
        ang[k] = p - math.pi / 2
    R = {k: (Rc if k in core else Ro) for k in N}
    XY = {k: (cx + R[k] * math.cos(ang[k]), cy + R[k] * math.sin(ang[k])) for k in N}
    red_targets = set(model["reforms"][highlight_reform]["targets"]) if highlight_reform else set()
    in_loop = {k for k, l in L.items() if l["loops"]}
    ctx, emph, reds = [], [], []
    for k, l in L.items():
        a, b = XY[l["from"]], XY[l["to"]]
        ra, rb = R[l["from"]], R[l["to"]]
        if ra == Rc and rb == Rc:
            da = abs((ang[l["to"]] - ang[l["from"]] + math.pi) % (2 * math.pi) - math.pi)
            beta = max(0.08, 1 - da / math.pi * 1.05)
            mxp, myp = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            c = (cx + (mxp - cx) * beta, cy + (myp - cy) * beta)
            poly = D.quad(a, c, b, 64)
        elif ra == Ro and rb == Ro:
            da = (ang[l["to"]] - ang[l["from"]] + math.pi) % (2 * math.pi) - math.pi
            am = ang[l["from"]] + da / 2
            rr = Ro + 40 + abs(da) * 60
            c = (cx + rr * math.cos(am), cy + rr * math.sin(am))
            poly = D.quad(a, c, b, 64)
        else:
            am = ang[l["from"]] + ((ang[l["to"]] - ang[l["from"]] + math.pi) % (2 * math.pi) - math.pi) / 2
            rr = (Rc + Ro) / 2
            c = (cx + rr * math.cos(am), cy + rr * math.sin(am))
            poly = D.quad(a, c, b, 64)
        red = k in red_targets
        g = f'<g class="link"{D.link_attrs(l)}>' + D.connection(poly, l, start_gap=11, end_gap=12, width=1.75 if k in in_loop or red else 1.25,
                                                               color=D.INK if (k in in_loop or red) else D.STONE, red=red, ticks=False) + "</g>"
        (reds if red else emph if k in in_loop else ctx).append(g)
    nodes = []
    for k in model["order"]:
        x, y = XY[k]
        a = ang[k]
        n = N[k]
        red = k in red_targets
        ring = D.target_ring_circle(x, y, 17, red=True, ids=[highlight_reform]) if red else ""
        fill = D.INK if k in core else D.NEWS
        tf = D.NEWS if k in core else D.INK
        nodes.append(f'<g class="var"{D.node_attrs(k)}>{ring}<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{fill}" stroke="{D.INK}" stroke-width="1.5"/></g>')
        # label outside the node, radial direction
        ca, sa = math.cos(a), math.sin(a)
        off = 18
        lx, ly = x + ca * off, y + sa * off
        anchor = "start" if ca > 0.2 else ("end" if ca < -0.2 else "middle")
        txt = k if k not in core else f"{k} {n['short'] or n['title']}"
        if k in core:
            lines = D.wrap(n["short"] or n["title"], 120, 13, 400)
            blk = [D.T(lx, ly + 4, k, 13, 700, D.INK, anchor)]
            for i, ln in enumerate(lines[:2]):
                blk.append(D.T(lx, ly + 4 + 15 * (i + 1), ln, 13, 400, D.INK, anchor))
            if sa < -0.5:
                blk = [b.replace(f'y="{ly + 4:.1f}"', f'y="{ly + 4 - 15 * len(lines[:2]):.1f}"', 1) if i == 0 else b for i, b in enumerate(blk)]
                # place name lines above the ID when the node sits at the top
                blk = [D.T(lx, ly + 4 - 15 * (len(lines[:2]) - i), ln, 13, 400, D.INK, anchor) for i, ln in enumerate(lines[:2])] + [D.T(lx, ly + 4, k, 13, 700, D.INK, anchor)]
            nodes.append("".join(blk))
        else:
            nodes.append(D.T(lx, ly + 4, txt, 13, 700, D.INK, anchor))
    # area captions on the inner ring
    caps = []
    for a in model["areas"]:
        ks = [k for k in a["nodes"] if k in core]
        if not ks:
            continue
        am = math.atan2(sum(math.sin(ang[k]) for k in ks), sum(math.cos(ang[k]) for k in ks))
        rr = Rc - 46
        x, y = cx + rr * math.cos(am), cy + rr * math.sin(am)
        caps.append(D.T(x, y + 5, a["id"], 22, 800, D.DEEP, "middle", display=True))
    body = (f'<circle cx="{cx}" cy="{cy}" r="{Rc}" fill="none" stroke="{D.STONE}" stroke-width="0.75"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{Ro}" fill="none" stroke="{D.STONE}" stroke-width="0.75" stroke-opacity="0.6"/>'
            + "".join(ctx) + "".join(emph) + "".join(reds) + "".join(caps) + "".join(nodes))
    label = "Whole system, orbit dial: 51 variables and 118 connections. Core variables sit on the inner ring by area; outside drivers, economy and technology on the outer ring."
    return D.svg_doc(w, h, body, label, "orbit-map", ' data-direction="orbit"' + (f' data-reform="{highlight_reform}"' if highlight_reform else ""))
