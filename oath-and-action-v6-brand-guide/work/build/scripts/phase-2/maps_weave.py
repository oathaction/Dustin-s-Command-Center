"""Direction 3, Weave: a loop is a stitch in the fabric of the system.

Geometry (after BioFabric, Longabaugh 2012): every variable is a horizontal thread in V7's system order, and every
connection is a vertical thread from its source row (a dot) to its target row (an arrowhead). Nothing crosses at an
angle, so the whole system never becomes a hairball. A loop is a run of vertical threads that leaves a row and comes
back to it. The miniature keeps the loop's own rows in system order, with a wider gap where it crosses into another
area; the card adds the loop's other threads to the rest of the system in Stone.
"""
import maps_draw as D

AREA_GAP = 16


def rows_for(loop, model, pitch, gap=AREA_GAP):
    """Row y positions for the loop's stations, in system order, with a gap at each change of area."""
    order = model["order"]
    codes = [s["code"] for s in loop["stations"] if s["code"]]
    if loop["conceptual"]:
        keys = [s["code"] or ("~" + s["label"]) for s in loop["stations"]]
        return {k: i * pitch for i, k in enumerate(keys)}, keys
    keys = sorted(set(codes), key=order.index)
    y, prev, Y = 0, None, {}
    for k in keys:
        a = model["nodes"][k]["area"]
        if prev is not None:
            y += pitch + (gap if a != prev else 0)
        Y[k] = y
        prev = a
    return Y, keys


def key_of(s):
    return s["code"] or ("~" + s["label"])


def mini(loop, model, w=300, h=236, pitch=44, col=60, red_targets=None, bg=D.NEWS):
    """Catalog miniature: the loop's own rows in system order, a wider gap where it crosses into another area,
    and one vertical thread per step in chain order. Labels sit beside each thread so its texture stays visible."""
    Y, keys = rows_for(loop, model, pitch, gap=18)
    height = max(Y.values())
    y0 = (h - height) / 2 - 6
    x_label = 40
    n = loop["n"]
    x0 = (w - (n - 1) * col) / 2 + 4
    red_targets = red_targets or set()
    body, rows, pills, notes, ptr = [], [], [], [], []
    xl = x0 + (n - 1) * col + 38
    for k in keys:
        y = y0 + Y[k]
        rows.append(f'<line x1="{x_label + 6}" y1="{y:.1f}" x2="{xl:.1f}" y2="{y:.1f}" stroke="{D.STONE}" stroke-width="1"/>')
        if not k.startswith("~"):
            tg = loop["targets"].get(k)
            red = k in red_targets
            lab = next(s["label"] for s in loop["stations"] if s["code"] == k)
            rows.append(f'<g class="var"{D.node_attrs(k, lab)}><rect x="{x_label - 26:.1f}" y="{y - 11:.1f}" width="30" height="22" rx="4" fill="{D.INK}"/>'
                        + D.T(x_label - 11, y + 4.6, k, 13, 700, bg, "middle") + "</g>")
            if tg:
                ptr.append(D.pointer(x_label - 29, y, -1, 0, red=red, ids=tg, at=k))
        else:
            rows.append(f'<g class="sketch" data-concept-label="{D.esc(k[1:])}"><rect x="{x_label - 18:.1f}" y="{y - 7:.1f}" width="14" height="14" rx="3" fill="{bg}" stroke="{D.INK}" stroke-width="1.5"/></g>')
    for i, st in enumerate(loop["steps"]):
        x = x0 + i * col
        a = loop["stations"][i]
        b = loop["stations"][(i + 1) % n]
        ya, yb = y0 + Y[key_of(a)], y0 + Y[key_of(b)]
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}><circle cx="{x:.1f}" cy="{ya:.1f}" r="3.5" fill="{D.INK}"/>'
                    + D.connection([(x, ya), (x, yb)], st, start_gap=4, end_gap=1, red=red, bg=bg) + "</g>")
        my = (ya + yb) / 2
        p, pw = D.sign_pill(x + 4 + 10, my, st, bg=bg, extra=f' data-for="{st["id"] or "concept-" + str(st["index"])}"')
        # the pill sits just right of its thread
        p = p.replace('<g class="pill"', f'<g class="pill" transform="translate({pw / 2 - 10:.1f} 0)"', 1)
        pills.append(p)
        tg = loop["targets"].get(st["id"]) if st["id"] else None
        if tg:
            ptr.append(D.pointer(x + 4 + pw + 3, my, 1, 0, red=red, ids=tg, at=st["id"]))
        if st["id"] in loop["weakest"]:
            notes.append(f'<line x1="{x:.1f}" y1="{y0 + height + 14:.1f}" x2="{x:.1f}" y2="{y0 + height + 22:.1f}" stroke="{D.DEEP}" stroke-width="1.5" data-weakest="{st["id"]}"/>')
    if loop["weakest"]:
        xs = [x0 + i * col for i, st in enumerate(loop["steps"]) if st["id"] in loop["weakest"]]
        notes.append(D.T(sum(xs) / len(xs), y0 + height + 38, "weakest", 13, 400, D.DEEP, "middle", italic=True))
    label = f'Loop {loop["id"]}, weave miniature. {loop["kind_word"]} loop. {loop["how_to_read"]}'
    return D.svg_doc(w, h, "".join(rows) + "".join(body) + "".join(pills) + "".join(ptr) + "".join(notes), label,
                     "weave-mini", f' data-loop="{loop["id"]}" data-direction="weave"')


def card_figure(loop, model, reform_id=None, w=1180, bg=D.WHITE, pitch=86, col=150):
    """Card drawing: the loop's rows with V7 names, its stitch at full size, and every other connection that
    leaves or enters those rows, drawn in Stone to the right, so the card shows where the loop touches the rest."""
    Y, keys = rows_for(loop, model, pitch, gap=34)
    L = model["links"]
    height = max(Y.values())
    y0 = 104
    x_label = 300
    x0 = x_label + 70
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    loop_links = {s["id"] for s in loop["steps"]}
    codes = [k for k in keys if not k.startswith("~")]
    others = [l for l in L.values() if (l["from"] in codes or l["to"] in codes) and l["id"] not in loop_links]
    others.sort(key=lambda l: (keys.index(l["from"]) if l["from"] in codes else keys.index(l["to"]), l["id"]))
    xc0 = x0 + (loop["n"] - 1) * col + 120
    ccol = min(56, (w - 60 - xc0) / max(1, len(others)))
    xl = xc0 + max(0, len(others) - 1) * ccol + 30
    body, rows, pills, labels, ctx = [], [], [], [], []
    for k in keys:
        y = y0 + Y[k]
        rows.append(f'<line x1="{x_label - 6}" y1="{y:.1f}" x2="{xl:.1f}" y2="{y:.1f}" stroke="{D.INK}" stroke-width="1.25"/>')
        if k.startswith("~"):
            rows.append(D.T(x_label - 14, y + 5, k[1:], 16, 700, D.INK, "end"))
            continue
        n = model["nodes"][k]
        red = k in red_targets
        lab = next(s["label"] for s in loop["stations"] if s["code"] == k)
        g = [f'<g class="var"{D.node_attrs(k, lab)}' + (f' data-target="{reform_id}" data-red="1"' if red else "") + ">"]
        if red:
            # red outline around a Charcoal tile: White on Pillar Red would fall under 4.5:1 for 16 px text
            g.append(f'<rect x="{x_label - 50:.1f}" y="{y - 19:.1f}" width="50" height="38" rx="7" fill="none" stroke="{D.RED}" stroke-width="3"/>')
        g.append(f'<rect x="{x_label - 46:.1f}" y="{y - 15:.1f}" width="42" height="30" rx="5" fill="{D.INK}"/>')
        g.append(D.T(x_label - 25, y + 6, k, 16, 800, D.WHITE, "middle", display=True))
        g.append(D.T(x_label - 58, y + 1, lab, 16, 700, D.INK, "end"))
        inc = (n["increase_means"] or "").replace("A higher value means ", "Higher: ")
        for i, ln in enumerate(D.wrap(inc, 250, 13, 400)[:3]):
            g.append(D.T(x_label - 58, y + 19 + 15 * i, ln, 13, 400, D.DEEP, "end"))
        g.append("</g>")
        rows.append("".join(g))
    for i, st in enumerate(loop["steps"]):
        x = x0 + i * col
        a = loop["stations"][i]
        b = loop["stations"][(i + 1) % loop["n"]]
        ya, yb = y0 + Y[key_of(a)], y0 + Y[key_of(b)]
        red = bool(st["id"] and st["id"] in red_targets)
        body.append(f'<g class="step"{D.step_attrs(st)}><circle cx="{x:.1f}" cy="{ya:.1f}" r="5" fill="{D.RED if red else D.INK}"/>'
                    + D.connection([(x, ya), (x, yb)], st, start_gap=6, end_gap=1, red=red, bg=bg, width=2.5) + "</g>")
        my = (ya + yb) / 2
        p, pw = D.sign_pill(x, my, st, size=14, bg=bg, extra=f' data-for="{st["id"]}"')
        pills.append(p)
        if red:
            pills.append(D.pointer(x - pw / 2 - 2, my, -1, 0, red=True, ids=[reform_id], at=st["id"]))
        # label in a band under the rows, one block per thread
        lines = D.wrap(st["name"], col - 24, 14, 600)
        lx = x
        ly = y0 + height + 70
        blk = [D.T(lx, ly, st["id"] + ("  weakest" if st["id"] in loop["weakest"] else ""), 13, 700, D.INK, "middle")]
        for j, ln in enumerate(lines[:3]):
            blk.append(D.T(lx, ly + 18 * (j + 1), ln, 14, 600, D.INK, "middle"))
        k = min(3, len(lines))
        blk.append(D.T(lx, ly + 18 * (k + 1) + 2, D.GRADE_WORD[st["evidence"]], 13, 400, D.INK, "middle"))
        blk.append(D.T(lx, ly + 18 * (k + 2) + 2, D.DELAY_WORD[st["delay"]], 13, 400, D.DEEP, "middle"))
        labels.append(f'<g class="steplabel" data-for="{st["id"]}">' + "".join(blk) + "</g>")
    # context threads: each other connection that touches the loop's rows, to a stub naming the far variable
    stub_y_top = y0 - 52
    stub_y_bot = y0 + height + 52
    for j, l in enumerate(others):
        x = xc0 + j * ccol
        red = l["id"] in red_targets
        if l["from"] in codes and l["to"] in codes:
            ya, yb = y0 + Y[l["from"]], y0 + Y[l["to"]]
            far = None
        elif l["from"] in codes:
            ya = y0 + Y[l["from"]]
            yb = stub_y_bot if Y[l["from"]] >= height / 2 else stub_y_top
            far = l["to"]
        else:
            yb = y0 + Y[l["to"]]
            ya = stub_y_bot if Y[l["to"]] >= height / 2 else stub_y_top
            far = l["from"]
        col_ = D.RED if red else D.STONE
        dot = f'<circle cx="{x:.1f}" cy="{ya:.1f}" r="3.5" fill="{col_}"/>'
        g = f'<g class="link ctx"{D.link_attrs(l)}' + (f' data-target="{reform_id}"' if red else "") + f'>{dot}' + D.connection([(x, ya), (x, yb)], l, start_gap=4, end_gap=1, color=D.STONE if not red else D.INK, red=red, bg=bg, width=1.5)
        if far:
            end_y = yb if l["from"] in codes else ya
            ty = end_y + 18 if end_y > y0 + height / 2 else end_y - 8
            g += D.T(x, ty, far, 13, 700, D.INK, "middle")
        g += "</g>"
        ctx.append(g)
    head = (D.T(x0 - 10, y0 - 62, "This loop", 13, 700, D.INK) +
            (D.T(xc0 - 10, y0 - 74, "Its other connections to the rest of the system", 13, 700, D.DEEP) if others else ""))
    km = D.kind_mark(x0 + (loop["n"] - 1) * col + 64, y0 + height / 2 - 12, loop["type"], r=14)
    kw = D.T(x0 + (loop["n"] - 1) * col + 64, y0 + height / 2 + 22, loop["kind_gloss"], 14, 700, D.INK, "middle")
    h = y0 + height + 70 + 18 * 6 + 24
    label = f'Loop {loop["id"]}, weave card drawing. {loop["how_to_read"]}'
    return D.svg_doc(w, h, head + "".join(rows) + "".join(ctx) + "".join(body) + km + kw + "".join(pills) + "".join(labels), label,
                     "weave-card", f' data-loop="{loop["id"]}" data-direction="weave"' + (f' data-reform="{reform_id}"' if reform_id else ""), bg=bg)


# ------------------------------------------------------------------ whole system: the fabric

def fabric_columns(model):
    """Column order: one band per numbered loop in V7's order, each holding that loop's steps in chain order
    (a connection on two or three loops is woven into each, and the copies are marked), then the connections
    on no loop, by layer and by source row."""
    L = model["links"]
    order = model["order"]
    bands, seen = [], set()
    for lid in model["loop_order"]:
        lp = model["loops"][lid]
        if lp["conceptual"]:
            continue
        cols = []
        for st in lp["steps"]:
            cols.append({"link": st["id"], "repeat": st["id"] in seen, "loop": lid})
            seen.add(st["id"])
        bands.append({"id": lid, "label": lid, "cols": cols, "kind": "loop"})
    for layer, title in (("core", "Core, on no loop"), ("economy", "Economy layer"), ("technology", "Technology layer")):
        ks = sorted([k for k, l in L.items() if not l["loops"] and l["layer"] == layer],
                    key=lambda k: (order.index(L[k]["from"]), order.index(L[k]["to"])))
        bands.append({"id": layer, "label": title, "cols": [{"link": k, "repeat": False, "loop": None} for k in ks], "kind": "rest"})
    return bands


def whole_map(model, w=1216, highlight_reform=None, bg=None, focus_loop=None, pitch=6.5, bgap=7, row=19):
    N, L = model["nodes"], model["links"]
    surface = bg or D.NEWS
    bands = fabric_columns(model)
    label_w = 252
    y0 = 118
    Y, y, prev = {}, y0, None
    area_rows = []
    for k in model["order"]:
        a = N[k]["area"]
        if prev is not None:
            y += row + (10 if a != prev else 0)
        if a != prev:
            area_rows.append((a, y))
        Y[k] = y
        prev = a
    y_end = y
    red_targets = set(model["reforms"][highlight_reform]["targets"]) if highlight_reform else set()
    ncols = sum(len(b["cols"]) for b in bands)
    pitch = min(pitch, (w - label_w - 12 - 16 - bgap * (len(bands) - 1)) / (ncols - 1))
    x = label_w + 12
    threads, heads, rows = [], [], []
    xr = x
    for b in bands:
        b["x0"] = x
        for c in b["cols"]:
            l = L[c["link"]]
            ya, yb = Y[l["from"]], Y[l["to"]]
            red = l["id"] in red_targets
            strong = (b["kind"] == "loop") if focus_loop is None else (b["id"] == focus_loop)
            col = D.INK if strong or red else D.STONE
            poly = [(x, ya), (x, yb)]
            body = (f'<circle cx="{x:.1f}" cy="{ya:.1f}" r="2.4" fill="{D.RED if red else col}"/>'
                    + D.connection(poly, l, start_gap=2.5, end_gap=0.5, width=1.4 if strong else 1.1, color=col, red=red, bg=surface,
                                   ticks=False, head=False))
            # compact arrowhead for the fabric's narrow columns
            body += D.arrow_at(D.trim(poly, 0, 0.5), 6, 2.6, D.RED if red else col)
            threads.append(f'<g class="link"{D.link_attrs(l)}' + (' data-repeat="1"' if c["repeat"] else "")
                           + (f' data-loopband="{b["id"]}"' if b["kind"] == "loop" else "")
                           + (f' data-target="{highlight_reform}" data-red="1"' if red else "") + f">{body}</g>")
            x += pitch
        b["x1"] = x - pitch
        x += bgap
    xr = x - bgap + 8
    for k in model["order"]:
        yy = Y[k]
        n = N[k]
        red = k in red_targets
        name = n["short"] or n["title"]
        if D.text_w(name, 13, 400) > label_w - 40:
            name = D.wrap(name, label_w - 52, 13, 400)[0].rstrip(",") + "…"
        rows.append(f'<g class="var"{D.node_attrs(k)}' + (f' data-target="{highlight_reform}" data-red="1"' if red else "") + ">"
                    + f'<line x1="{label_w + 4}" y1="{yy:.1f}" x2="{xr:.1f}" y2="{yy:.1f}" stroke="{D.RED if red else D.STONE}" stroke-width="{2 if red else 0.75}"/>'
                    + D.T(label_w - 2, yy + 4.5, name, 13, 400, D.INK, "end")
                    + D.T(4, yy + 4.5, k, 13, 700, D.INK) + "</g>")
    area_caps = []
    for a, ya in area_rows:
        area_caps.append(f'<line x1="0" y1="{ya - 12:.1f}" x2="{label_w:.1f}" y2="{ya - 12:.1f}" stroke="{D.INK}" stroke-width="1"/>')
    band_labels = []
    for i, b in enumerate(bands):
        xm = (b["x0"] + b["x1"]) / 2
        if b["kind"] == "loop":
            band_labels.append(f'<text x="{xm + 4.5:.1f}" y="{y0 - 22:.1f}" class="mt mb" font-size="13" fill="{D.INK}" transform="rotate(-90 {xm + 4.5:.1f} {y0 - 22:.1f})">{b["label"]}</text>')
            band_labels.append(f'<line x1="{b["x0"] - 1:.1f}" y1="{y0 - 14:.1f}" x2="{b["x1"] + 1:.1f}" y2="{y0 - 14:.1f}" stroke="{D.INK}" stroke-width="2"/>')
        else:
            lab = b["label"] if D.text_w(b["label"], 13, 700) <= b["x1"] - b["x0"] + 4 else b["label"].split(" layer")[0].split(",")[0]
            band_labels.append(D.T(b["x0"], y0 - 22, lab, 13, 700, D.DEEP))
            band_labels.append(f'<line x1="{b["x0"] - 1:.1f}" y1="{y0 - 14:.1f}" x2="{b["x1"] + 1:.1f}" y2="{y0 - 14:.1f}" stroke="{D.STONE}" stroke-width="2"/>')
    head = (D.T(4, 24, "Each row is a variable. Each vertical thread is one connection: it leaves its row at a dot and", 13, 600, D.INK)
            + D.T(4, 42, "lands on another row at an arrowhead. Loops sit side by side on the left, one band each.", 13, 600, D.INK))
    h = y_end + 30
    body = head + "".join(area_caps) + "".join(rows) + "".join(threads) + "".join(band_labels)
    label = ("Whole system as a fabric: 51 variables as rows and 118 connections as vertical threads, grouped into one band per "
             "numbered loop and then the connections on no loop. Seven loop connections are woven into more than one band.")
    return D.svg_doc(w, h, body, label, "weave-map", ' data-direction="weave"' + (f' data-reform="{highlight_reform}"' if highlight_reform else ""), bg=bg)
