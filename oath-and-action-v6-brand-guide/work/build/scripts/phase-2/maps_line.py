"""Direction 2, Line: a loop is a line you ride out and back.

Geometry: the stations sit on one line in V7's chain order, left to right, at a fixed pitch, so a longer strip means
more steps and nothing else. Every step but the last runs along the line. The closing step drops below the line and
returns to the first station: the return line. The card is Concept 08's R8 layout rebuilt on V7 and the Gate 1 marks;
the miniature is the same strip at a smaller pitch.
"""
import maps_draw as D


def strip_geom(loop, x0, y0, pitch, depth, sw, sh, corner=10):
    n = loop["n"]
    X = [x0 + sw / 2 + i * pitch for i in range(n)]
    paths = []
    for i, st in enumerate(loop["steps"]):
        if i < n - 1:
            paths.append([(X[i] + sw / 2, y0), (X[i + 1] - sw / 2, y0)])
        else:
            yb = y0 + sh / 2 + depth
            xa, xb = X[-1], X[0]
            c = corner
            pts = [(xa, y0 + sh / 2), (xa, yb - c)]
            pts += [(xa - c + c * __import__("math").cos(t / 8 * 1.5708), yb - c + c * __import__("math").sin(t / 8 * 1.5708)) for t in range(1, 9)]
            pts += [(xb + c, yb)]
            pts += [(xb + c - c * __import__("math").sin(t / 8 * 1.5708), yb - c + c * __import__("math").cos(t / 8 * 1.5708)) for t in range(1, 9)]
            pts += [(xb, y0 + sh / 2)]
            paths.append(pts)
    return X, paths


def mini(loop, w=300, h=158, pitch=82, red_targets=None):
    n = loop["n"]
    sw, sh = 30, 22
    span = (n - 1) * pitch + sw
    x0 = (w - span) / 2
    y0 = 52
    depth = 40
    X, paths = strip_geom(loop, x0, y0, pitch, depth, sw, sh)
    red_targets = red_targets or set()
    body, pills, nodes, notes, ptr = [], [], [], [], []
    for st, poly in zip(loop["steps"], paths):
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(poly, st, start_gap=1, end_gap=1, red=red) + "</g>")
        if not st["closing"]:
            (mx, my), _ = D.mid(poly)
            py = y0 - 24
        else:
            mx, py = (X[0] + X[-1]) / 2, y0 + sh / 2 + depth
        p, pw = D.sign_pill(mx, py, st, extra=f' data-for="{st["id"] or "concept-" + str(st["index"])}"')
        pills.append(p)
        tg = loop["targets"].get(st["id"]) if st["id"] else None
        if tg:
            ptr.append(D.pointer(mx, py - 12, 0, -1, red=red, ids=tg, at=st["id"]))
        if st["id"] in loop["weakest"]:
            wy = (y0 + 19) if not st["closing"] else (py + 26)
            wx = mx if not st["closing"] else mx
            notes.append(D.T(wx, wy, "weakest", 13, 400, D.DEEP, "middle", italic=True, extra=f' data-weakest="{st["id"]}"'))
    for s, x in zip(loop["stations"], X):
        if s["is_variable"]:
            tg = loop["targets"].get(s["code"])
            red = s["code"] in red_targets
            if tg:
                ptr.append(D.pointer(x, y0 - sh / 2 - 2, 0, -1, red=red, ids=tg, at=s["code"]))
            nodes.append(f'<g class="var"{D.node_attrs(s["code"], s["label"])}><rect x="{x - sw / 2:.1f}" y="{y0 - sh / 2:.1f}" width="{sw}" height="{sh}" rx="4" fill="{D.INK}"/>'
                         + D.T(x, y0 + 4.6, s["code"], 13, 700, D.NEWS, "middle") + "</g>")
        else:
            nodes.append(f'<g class="sketch" data-concept-label="{D.esc(s["label"])}"><rect x="{x - 7:.1f}" y="{y0 - 7:.1f}" width="14" height="14" rx="3" fill="{D.NEWS}" stroke="{D.INK}" stroke-width="1.5"/></g>')
    # kind mark inside the return loop, at the right end of the strip for clarity
    km = ""
    label = f'Loop {loop["id"]}, line miniature. {loop["kind_word"]} loop. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(body) + "".join(nodes) + "".join(pills) + "".join(ptr) + "".join(notes) + km, label,
                     "line-mini", f' data-loop="{loop["id"]}" data-direction="line"')


def card_figure(loop, model, reform_id=None, w=1180, pitch=None, bg=D.WHITE):
    """Card drawing: station boxes with V7's chain label and its reading rule, steps named above the line, the
    return line underneath with its label below it. Red on White marks one reform's targets (Rule 05.3)."""
    n = loop["n"]
    sw = 236 if n <= 3 else 214
    pitch = pitch or (sw + (360 if n == 2 else 150 if n == 3 else 86))
    # box height from the longest station text
    texts = []
    for s in loop["stations"]:
        inc = (model["nodes"][s["code"]]["increase_means"] or "").replace("A higher value means ", "Higher: ") if s["code"] else ""
        texts.append((D.wrap(s["label"], sw - 72, 16, 700)[:2], D.wrap(inc, sw - 30, 13, 400)))
    sh = max(30 + 20 * len(t[0]) + 16 * len(t[1]) for t in texts) + 8
    span = (n - 1) * pitch + sw
    x0 = (w - span - 90) / 2
    top = 112
    y0 = top + sh / 2
    depth = 96
    X, paths = strip_geom(loop, x0, y0, pitch, depth, sw, sh, corner=16)
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    body, pills, nodes, labels = [], [], [], []
    for st, poly in zip(loop["steps"], paths):
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}>' + D.connection(poly, st, start_gap=1, end_gap=1, red=red, bg=bg, width=2.5) + "</g>")
        gw = D.GRADE_WORD[st["evidence"]] + ("  \u00b7  " + st["type"] if st["type"] != "causal" else "") + "  \u00b7  " + D.DELAY_WORD[st["delay"]]
        head = st["id"] + ("  \u00b7  weakest step" if st["id"] in loop["weakest"] else "")
        if not st["closing"]:
            (mx, my), _ = D.mid(poly)
            py = y0
            lines = D.wrap(st["name"], pitch - 40, 15, 600)
            blk = [D.T(mx, top - 18 - 18 * (len(lines) - 1) - 20, head, 13, 700, D.INK, "middle")]
            blk += [D.T(mx, top - 18 - 18 * (len(lines) - 1 - i), ln, 15, 600, D.INK, "middle") for i, ln in enumerate(lines)]
            gap = pitch - sw
            if gap >= 220:
                blk.append(D.T(mx, y0 + 34, gw, 13, 400, D.DEEP, "middle"))
            else:
                blk.append(D.T(mx, top - 4, gw, 13, 400, D.DEEP, "middle"))
        else:
            mx, py = (X[0] + X[-1]) / 2, y0 + sh / 2 + depth
            lines = D.wrap(st["name"], 460, 15, 600)
            yy = py + 34
            blk = [D.T(mx, yy, head, 13, 700, D.INK, "middle")]
            blk += [D.T(mx, yy + 19 * (i + 1), ln, 15, 600, D.INK, "middle") for i, ln in enumerate(lines)]
            blk.append(D.T(mx, yy + 19 * (len(lines) + 1) + 2, gw, 13, 400, D.DEEP, "middle"))
        p, pw = D.sign_pill(mx, py, st, size=14, bg=bg, extra=f' data-for="{st["id"]}"')
        pills.append(p)
        if red:
            pills.append(D.pointer(mx, py - 13, 0, -1, red=True, ids=[reform_id], size=10, at=st["id"]))
        labels.append(f'<g class="steplabel" data-for="{st["id"]}">' + "".join(blk) + "</g>")
    for (s, x), (lab_lines, inc_lines) in zip(zip(loop["stations"], X), texts):
        red = s["code"] in red_targets
        stroke = f'stroke="{D.RED}" stroke-width="3"' if red else f'stroke="{D.INK}" stroke-width="1.5"'
        g = [f'<g class="var"{D.node_attrs(s["code"], s["label"])}' + (f' data-target="{reform_id}" data-red="1"' if red else "") + ">",
             f'<rect x="{x - sw / 2:.1f}" y="{y0 - sh / 2:.1f}" width="{sw}" height="{sh:.1f}" rx="6" fill="{bg}" {stroke}/>',
             f'<rect x="{x - sw / 2:.1f}" y="{y0 - sh / 2:.1f}" width="6" height="{sh:.1f}" fill="{D.INK}"/>',
             D.T(x - sw / 2 + 18, y0 - sh / 2 + 26, s["code"], 16, 800, D.INK, display=True)]
        for i, ln in enumerate(lab_lines):
            g.append(D.T(x - sw / 2 + 56, y0 - sh / 2 + 26 + 20 * i, ln, 16, 700, D.INK))
        base = y0 - sh / 2 + 26 + 20 * len(lab_lines) + 4
        for i, ln in enumerate(inc_lines):
            g.append(D.T(x - sw / 2 + 18, base + 16 * i, ln, 13, 400, D.DEEP))
        if red:
            g.append(D.pointer(x, y0 - sh / 2 - 3, 0, -1, red=True, ids=[reform_id], size=10, at=s["code"]))
        g.append("</g>")
        nodes.append("".join(g))
    kx = X[-1] + sw / 2 + 52
    km = D.kind_mark(kx, y0 - 10, loop["type"], r=16)
    kw = D.T(kx, y0 + 26, loop["kind_gloss"], 14, 700, D.INK, "middle")
    h = y0 + sh / 2 + depth + 34 + 19 * (len(D.wrap(loop["steps"][-1]["name"] or "", 460, 15, 600)) + 1) + 30
    label = f'Loop {loop["id"]}, line card drawing. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(body) + km + kw + "".join(nodes) + "".join(pills) + "".join(labels), label,
                     "line-card", f' data-loop="{loop["id"]}" data-direction="line"' + (f' data-reform="{reform_id}"' if reform_id else ""), bg=bg)


# ------------------------------------------------------------------ whole system: the line with returns underneath

LINE_ORDER = ["X", "TC", "EC", "A", "B", "C", "D", "E"]


def whole_map(model, w=1216, highlight_reform=None, bg=None, focus_loop=None):
    """All 51 variables on one line: outside drivers and the two lower layers on the left, then the core areas A to
    E in the order effects mostly travel. A connection that runs right arcs over the line; one that runs back to
    the left arcs under it, so the steps that close loops sit below. Loop connections in Charcoal, the rest in Stone."""
    N, L = model["nodes"], model["links"]
    surface = bg or D.NEWS
    keys = []
    gaps = 0
    for a in LINE_ORDER:
        ks = [k for k in model["order"] if N[k]["area"] == a]
        keys.append((a, ks))
    n_nodes = sum(len(ks) for _, ks in keys)
    margin, agap = 24, 14
    pitch = (w - 2 * margin - agap * (len(keys) - 1)) / (n_nodes - 1)
    X, x = {}, margin
    spans = []
    for i, (a, ks) in enumerate(keys):
        x0 = x
        for k in ks:
            X[k] = x
            x += pitch
        spans.append((a, x0, x - pitch))
        x += agap - pitch + pitch
    top_h, band, lab_h, bot_h = 300, 58, 34, 300
    y_top = 60 + top_h
    y_bot = y_top + band
    red_targets = set(model["reforms"][highlight_reform]["targets"]) if highlight_reform else set()
    focus = set(s["id"] for s in model["loops"][focus_loop]["steps"]) if focus_loop else None
    in_loop = {k for k, l in L.items() if l["loops"]}
    ctx, emph, reds = [], [], []
    order_draw = sorted(L.values(), key=lambda l: -abs(X[l["to"]] - X[l["from"]]))
    for l in order_draw:
        xa, xb = X[l["from"]], X[l["to"]]
        span = abs(xb - xa)
        hgt = min(top_h - 14, 18 + span * 0.36)
        if xb > xa:   # forward: over the line
            ya, yb = y_top, y_top
            poly = D.cubic((xa, ya), (xa, ya - hgt * 1.33), (xb, yb - hgt * 1.33), (xb, yb), 80)
        else:         # back: under the line, below the area labels
            ya, yb = y_bot + lab_h, y_bot + lab_h
            poly = D.cubic((xa, ya), (xa, ya + hgt * 1.33), (xb, yb + hgt * 1.33), (xb, yb), 80)
        red = l["id"] in red_targets
        strong = (l["id"] in focus) if focus is not None else (l["id"] in in_loop or red)
        g = (f'<g class="link"{D.link_attrs(l)}' + (f' data-target="{highlight_reform}" data-red="1"' if red else "") + ">"
             + D.connection(poly, l, start_gap=0, end_gap=0, width=1.9 if strong else 1.15, color=D.INK if strong else D.STONE,
                            red=red, bg=surface, ticks=False) + "</g>")
        (reds if red else emph if strong else ctx).append(g)
    # band of stations
    band_svg = [f'<line x1="{margin - 8}" y1="{y_top}" x2="{w - margin + 8}" y2="{y_top}" stroke="{D.INK}" stroke-width="1.5"/>',
                f'<line x1="{margin - 8}" y1="{y_bot}" x2="{w - margin + 8}" y2="{y_bot}" stroke="{D.INK}" stroke-width="1.5"/>']
    for k, x in X.items():
        n = N[k]
        red = k in red_targets
        filled = n["layer"] == "core" and n["area"] != "X"
        tf = D.NEWS if filled else D.INK
        fill = D.INK if filled else surface
        band_svg.append(f'<g class="var"{D.node_attrs(k)}' + (f' data-target="{highlight_reform}" data-red="1"' if red else "") + ">"
                        + f'<rect x="{x - 9:.1f}" y="{y_top + 3:.1f}" width="18" height="{band - 6}" rx="3" fill="{fill}" stroke="{D.RED if red else D.INK}" stroke-width="{3 if red else 1.25}"/>'
                        + f'<text x="{x + 4.6:.1f}" y="{y_bot - 8:.1f}" class="mt mb" font-size="13" fill="{tf}" transform="rotate(-90 {x + 4.6:.1f} {y_bot - 8:.1f})">{k}</text></g>')
        # stubs to the arc ends below the label row
        band_svg.append(f'<line x1="{x:.1f}" y1="{y_bot}" x2="{x:.1f}" y2="{y_bot + lab_h}" stroke="{D.STONE}" stroke-width="0.75"/>')
    for a, x0, x1 in spans:
        title = model["region_titles"].get(a, a)
        short = {"X": "Drivers", "TC": "Technology", "EC": "Economy"}.get(a, title)
        band_svg.append(f'<line x1="{x0 - 8:.1f}" y1="{y_bot + lab_h - 8}" x2="{x1 + 8:.1f}" y2="{y_bot + lab_h - 8}" stroke="{D.INK}" stroke-width="3"/>')
        tw = D.text_w(short, 13, 700)
        lab = short if tw < (x1 - x0 + 16) else a
        band_svg.append(D.T((x0 + x1) / 2, y_bot + 18, lab, 13, 700, D.INK, "middle"))
    over = D.T(margin, 34, "Runs forward, to the right: over the line", 14, 700, D.INK)
    under_y = y_bot + lab_h + bot_h + 12
    under = D.T(margin, under_y, "Runs back, to the left: under the line. Most steps that close a loop sit here.", 14, 700, D.INK)
    h = under_y + 24
    body = over + "".join(ctx) + "".join(emph) + "".join(reds) + "".join(band_svg) + under
    label = ("Whole system on one line: 51 variables and 118 connections. Connections that run to the right arc over the line; "
             "connections that run back arc under it.")
    return D.svg_doc(w, h, body, label, "line-map", ' data-direction="line"' + (f' data-reform="{highlight_reform}"' if highlight_reform else ""), bg=bg)
