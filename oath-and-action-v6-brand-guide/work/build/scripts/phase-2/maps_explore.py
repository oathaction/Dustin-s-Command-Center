"""Quick explorations: seven form families drawn on real V7 loops before choosing three directions.

Each thumbnail draws Loop R8 (two steps, both well supported, slow) and Loop R10 (four steps, mixed grades), and
where the family suggests one, the whole-system idea. These are sketches at sketch fidelity, drawn from V7 data.
"""
import math

import maps_draw as D
import maps_line
import maps_orbit
import maps_weave

W, H = 560, 300


def _frame(body, label, fam):
    return D.svg_doc(W, H, body, label, "explore", f' data-family="{fam}"')


def _embed(svg, x, y, scale=1.0):
    inner = svg[svg.index(">", svg.index("<svg")) + 1: svg.rindex("</svg>")]
    inner = inner.split("</title>", 1)[1] if "</title>" in inner else inner
    return f'<g transform="translate({x} {y}) scale({scale})">{inner}</g>'


def orbit(model):
    L = model["loops"]
    body = _embed(maps_orbit.mini(L["R8"]), 0, 40) + _embed(maps_orbit.mini(L["R10"]), 170, 40) + _embed(maps_orbit.mini(L["R3"]), 340, 40)
    body += D.T(12, 26, "R8, R10, R3: slow steps bow out, so each loop takes its own shape", 13, 600, D.INK)
    return _frame(body, "Exploration: orbits and rings, drawn on loops R8, R10 and R3", "orbit")


def transit(model):
    L = model["loops"]
    body = _embed(maps_line.mini(L["R8"]), -10, 40) + _embed(maps_line.mini(L["R10"]), 250, 40)
    body += _embed(maps_line.mini(L["B4"]), 120, 150)
    body += D.T(12, 26, "R8, R10, B4: stations on a line, the closing step on a return line", 13, 600, D.INK)
    return _frame(body, "Exploration: transit strip maps, drawn on loops R8, R10 and B4", "transit")


def weave(model):
    L = model["loops"]
    body = _embed(maps_weave.mini(L["R8"], model, w=270), 0, 40) + _embed(maps_weave.mini(L["R10"], model, w=270), 280, 34)
    body += D.T(12, 26, "R8, R10: rows are variables, threads are connections", 13, 600, D.INK)
    return _frame(body, "Exploration: a woven field, drawn on loops R8 and R10", "weave")


def field(model):
    """Every loop on one fixed map: core areas as columns, variables stacked, the loop's route lit."""
    N = model["nodes"]
    cols = ["A", "B", "C", "D", "E"]
    pos = {}
    for ci, a in enumerate(cols):
        ks = [k for k in model["order"] if N[k]["area"] == a]
        for ri, k in enumerate(ks):
            pos[k] = (ci, ri)

    def panel(lid, ox, oy, cw=48, rh=26):
        lp = model["loops"][lid]
        out = []
        for k, (c, r) in pos.items():
            out.append(f'<circle cx="{ox + c * cw:.1f}" cy="{oy + r * rh:.1f}" r="3.5" fill="{D.STONE}"/>')
        for st in lp["steps"]:
            a = pos[st["from"]]
            b = pos[st["to"]]
            pa = (ox + a[0] * cw, oy + a[1] * rh)
            pb = (ox + b[0] * cw, oy + b[1] * rh)
            poly = D.arc_through(pa, pb, 8, 24)
            out.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(poly, st, start_gap=7, end_gap=7, ticks=False) + "</g>")
        for s in lp["stations"]:
            c, r = pos[s["code"]]
            out.append(f'<g class="var"{D.node_attrs(s["code"])}><circle cx="{ox + c * cw:.1f}" cy="{oy + r * rh:.1f}" r="6" fill="{D.INK}"/></g>')
        for ci, a in enumerate(cols):
            out.append(D.T(ox + ci * cw, oy - 14, a, 13, 700, D.DEEP, "middle"))
        out.append(D.T(ox - 10, oy + 7 * rh + 8, lid, 13, 700, D.INK))
        return "".join(out)
    body = panel("R8", 40, 70) + panel("R10", 310, 70)
    body += D.T(12, 26, "R8, R10: the same map every time, with one loop lit", 13, 600, D.INK)
    return _frame(body, "Exploration: one fixed field with the loop lit, drawn on loops R8 and R10", "field")


def mechanical(model):
    """A loop as a belt over pulleys: each variable a pulley, the belt the chain of steps."""
    def belt(lid, cx, cy, r0, rp=18):
        lp = model["loops"][lid]
        n = lp["n"]
        P = [(cx + r0 * math.cos(-math.pi / 2 + i * 2 * math.pi / n), cy + r0 * math.sin(-math.pi / 2 + i * 2 * math.pi / n)) for i in range(n)]
        out = []
        for i, st in enumerate(lp["steps"]):
            a, b = P[i], P[(i + 1) % n]
            # outer tangent between two equal pulleys
            dx, dy = b[0] - a[0], b[1] - a[1]
            d = math.hypot(dx, dy)
            nx, ny = dy / d, -dx / d
            pa = (a[0] + nx * rp, a[1] + ny * rp)
            pb = (b[0] + nx * rp, b[1] + ny * rp)
            out.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection([pa, pb], st, start_gap=2, end_gap=2, ticks=False) + "</g>")
        for s, (x, y) in zip(lp["stations"], P):
            out.append(f'<g class="var"{D.node_attrs(s["code"])}><circle cx="{x:.1f}" cy="{y:.1f}" r="{rp}" fill="none" stroke="{D.INK}" stroke-width="1.5"/>'
                       f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="{D.INK}"/>' + D.T(x, y + rp + 18, s["code"], 13, 700, D.INK, "middle") + "</g>")
        return "".join(out)
    body = belt("R8", 140, 160, 62) + belt("R10", 400, 160, 78)
    body += D.T(12, 26, "R8, R10: a belt over pulleys, turning as one machine", 13, 600, D.INK)
    return _frame(body, "Exploration: a mechanical belt and pulleys, drawn on loops R8 and R10", "mechanical")


def typographic(model):
    """The loop as its own sentence, set in type, with the sign words in the line."""
    out = [D.T(12, 26, "R8, R10: the read-aloud sentence, set as the diagram", 13, 600, D.INK)]
    y = 70
    for lid in ("R8", "R10"):
        lp = model["loops"][lid]
        parts = []
        for s, st in zip(lp["stations"], lp["steps"]):
            parts.append((s["label"], True))
            parts.append(("raises" if st["polarity"] == "+" else "lowers", False))
        parts.append((lp["stations"][0]["label"], True))
        x = 16
        out.append(D.T(16, y - 20, lid, 13, 700, D.DEEP))
        line_y = y
        for text, is_var in parts:
            size = 17 if is_var else 13
            wgt = 800 if is_var else 400
            tw = D.text_w(text, size, wgt, display=is_var) + 10
            if x + tw > W - 12:
                x = 16
                line_y += 30
            out.append(D.T(x, line_y, text, size, wgt, D.INK if is_var else D.DEEP, display=is_var, italic=not is_var))
            x += tw
        y = line_y + 64
    return _frame("".join(out), "Exploration: a typographic sentence diagram, set from loops R8 and R10", "typographic")


def terrain(model):
    """Stability landscape: a reinforcing loop as a ball on a crest, a balancing loop as a ball in a valley."""
    def prof(ox, oy, up, label):
        pts = [(ox + t * 2.2, oy + (-1 if up else 1) * 46 * math.exp(-((t - 50) / 22) ** 2)) for t in range(0, 101, 2)]
        ball_y = oy + (-46 - 10 if up else 46 - 10)
        return (f'<path d="{D.path_d(pts)}" fill="none" stroke="{D.INK}" stroke-width="2"/>'
                f'<circle cx="{ox + 110:.1f}" cy="{ball_y:.1f}" r="9" fill="{D.INK}"/>' + D.T(ox + 110, oy + 80, label, 13, 600, D.INK, "middle"))
    body = prof(30, 170, True, "Loop R8, reinforcing: any push grows") + prof(300, 130, False, "Loop B4, balancing: a push comes back")
    body += D.T(12, 26, "R8, B4: the loop's kind as a landscape", 13, 600, D.INK)
    return _frame(body, "Exploration: terrain, the loop kind as a stability landscape, for loops R8 and B4", "terrain")


FAMILIES = [
    ("orbit", "Orbits and rings", orbit, "kept",
     "A loop already reads as a ring. Letting each step's delay bend its arc makes every loop its own shape, so the catalog becomes 23 different drawings. Kept as Direction 1."),
    ("transit", "Transit and circuit lines", transit, "kept",
     "The strip map above a train door: stations in order, a return line home. It reads left to right like the sentence V7 writes for each loop, and it is the R8 card Dustin likes. Kept as Direction 2."),
    ("weave", "Woven field", weave, "kept",
     "Rows for variables and vertical threads for connections, after BioFabric. Nothing crosses at an angle, so the whole system never tangles. Kept as Direction 3."),
    ("field", "Fixed field, loop lit", field, "dropped",
     "Strong for 'where does this loop live', and the research ranks fixed positions highly. At catalog size, steps inside one area shrink to a few pixels, so grades and signs cannot be read. Its fixed-position rule moves into the whole-system maps."),
    ("mechanical", "Mechanical belt", mechanical, "dropped",
     "Vivid, and wrong in two ways: a belt turns at one speed, which hides the different delays, and a machine promises a precision V7 does not estimate (research pitfall 6)."),
    ("typographic", "Typographic sentence", typographic, "dropped",
     "The clearest reading device in the earlier concepts. It cannot shrink to a miniature without falling under 13 px, and it has no whole-system form. Its sentence stays on every card as the read-aloud line."),
    ("terrain", "Terrain", terrain, "dropped",
     "A good picture of reinforcing and balancing, and a poor map: height and slope imply measured quantities the model does not have. It is not used as a mark, because a ball on a crest reads as a person at small sizes."),
]
