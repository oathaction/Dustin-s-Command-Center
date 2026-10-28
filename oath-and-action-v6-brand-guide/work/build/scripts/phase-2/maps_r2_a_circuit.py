"""Direction A, the Circuit: Concept 09 redrawn as a wiring diagram of the whole system.

Five area cards on a fixed grid, A to E left to right in the order effects mostly travel; the economy and technology
layers in a lower band; the outside drivers as tabs on the top edge. Inside each card, the 25 variables that sit on
a numbered loop are boxes in the Field Guide style. The 46 connections on named loops are individual wires routed
orthogonally with one corner radius:
  - inside one area, a hook in the card's left gutter
  - to the next area, a lane in the channel between the two cards
  - further forward, up over the cards on the top bus
  - further back, down under the cards on the bottom bus, Concept 09's return line
Lanes are shared only where two wires' vertical runs never meet. Ports on a box's two sides sit on offset rows, so no
two stubs share a line. The other 72 connections are counted bundles in Stone, as on Concept 09, with every
connection listed on the bundle that counts it so the verifier can account for all 118.
"""
import collections

import maps_draw as D
import maps_r2_a_fg as FG
import maps_r2_a_text as TX

COLS = ["A", "B", "C", "D", "E"]
LP = 9          # lane pitch
PP = 16         # port pitch on a box side
STUB = 22       # room between a box edge and the first lane, for the sign capsule
LABEL = 13      # station name size on the map
R = 5           # the one corner radius


def _interval_lanes(items, sep=10):
    """Greedy interval colouring: items are (key, lo, hi). Returns {key: lane index}."""
    lanes, ends = {}, []
    for key, lo, hi in sorted(items, key=lambda t: (t[1], t[2])):
        for i, e in enumerate(ends):
            if lo > e + sep:
                lanes[key] = i
                ends[i] = hi
                break
        else:
            lanes[key] = len(ends)
            ends.append(hi)
    return lanes


def build(model, bg=D.NEWS, reform_id=None, lit_loop=None, w_total=1392):
    N, L = model["nodes"], model["links"]
    red_targets = set(model["reforms"][reform_id]["targets"]) if reform_id else set()
    lit = set(s["id"] for s in model["loops"][lit_loop]["steps"]) if lit_loop else None
    loop_links = {k: l for k, l in L.items() if l["loops"]}
    loop_vars = {l["from"] for l in loop_links.values()} | {l["to"] for l in loop_links.values()}
    col = {k: COLS.index(N[k]["area"]) for k in loop_vars}
    card_vars = {c: [k for k in model["order"] if N[k]["area"] == c and k in loop_vars] for c in COLS}
    card_rest = {c: [k for k in model["order"] if N[k]["area"] == c and k not in loop_vars] for c in COLS}

    # ---- classify wires and give each end a side
    wires = []
    for k, l in loop_links.items():
        ca, cb = col[l["from"]], col[l["to"]]
        if ca == cb:
            kind, s_side, d_side = "hook", "L", "L"
        elif cb == ca + 1:
            kind, s_side, d_side = "fwd", "R", "L"
        elif cb == ca - 1:
            kind, s_side, d_side = "back", "L", "R"
        elif cb > ca:
            kind, s_side, d_side = "top", "R", "L"
        else:
            kind, s_side, d_side = "bottom", "L", "R"
        wires.append({"id": k, "l": l, "ca": ca, "cb": cb, "kind": kind, "s_side": s_side, "d_side": d_side})

    # ---- box widths from measured labels, per card
    label_lines, bw = {}, {}
    for c in COLS:
        best = 0
        for k in card_vars[c]:
            name = model["nodes"][k]["label"]
            for w_try in range(118, 220, 2):
                lines = TX.balanced_wrap(name, w_try, LABEL, 600)
                if len(lines) <= 2:
                    break
            label_lines[k] = lines
            best = max(best, max(TX.width(x, LABEL, 600) for x in lines))
        bw[c] = int(best) + 5 + 18 + 2
    # ---- ports per box side, ordered later by the far end's height
    ports = collections.defaultdict(list)
    for wv in wires:
        ports[(wv["l"]["from"], wv["s_side"])].append((wv["id"], "s"))
        ports[(wv["l"]["to"], wv["d_side"])].append((wv["id"], "d"))

    # ---- vertical layout of boxes, on an 18 px rhythm with the two sides offset by 9
    y_cards = 252
    head_h = 76
    box_y, box_h = {}, {}
    col_bottom = {}
    for c in COLS:
        y = y_cards + head_h
        y = PP * (int(y // PP) + 1)
        for k in card_vars[c]:
            n_lines = len(label_lines[k])
            content = 12 + 16 + 4 + 17 * n_lines + 10
            nports = max(len(ports[(k, "R")]), len(ports[(k, "L")]))
            h = max(content, PP * (nports + 1) + PP // 2)
            h = PP * (int((h + PP - 1) // PP))
            box_y[k], box_h[k] = y, h
            y += h + PP
        col_bottom[c] = y + 26 * len(card_rest[c])
    cards_bottom = max(col_bottom.values()) + 64

    # ---- horizontal layout: a hook gutter inside each card, a channel between cards
    def port_y(k, side, i):
        return box_y[k] + PP * (i + 1) + (PP // 2 if side == "L" else 0)

    # order ports on each side by the height of the wire's other end, so neighbouring wires rarely cross
    def other_end_y(wid, end):
        l = L[wid]
        o = l["to"] if end == "s" else l["from"]
        return box_y[o] + box_h[o] / 2
    port_index = {}
    for (k, side), lst in ports.items():
        lst.sort(key=lambda t: other_end_y(*t))
        for i, (wid, end) in enumerate(lst):
            port_index[(wid, end)] = port_y(k, side, i)

    # hooks: interval lanes per card
    hook_lanes = {}
    for c in range(5):
        items = []
        for wv in wires:
            if wv["kind"] == "hook" and wv["ca"] == c:
                y1, y2 = port_index[(wv["id"], "s")], port_index[(wv["id"], "d")]
                items.append((wv["id"], min(y1, y2), max(y1, y2)))
        hook_lanes[c] = _interval_lanes(items)
    n_hook = {c: (max(hook_lanes[c].values()) + 1 if hook_lanes[c] else 0) for c in range(5)}

    # channel lanes: channel k sits between column k-1 and column k
    y_top_bus = y_cards - 16
    y_bot_bus = cards_bottom + 26
    chan_items = collections.defaultdict(list)
    for wv in wires:
        ys, yd = port_index[(wv["id"], "s")], port_index[(wv["id"], "d")]
        if wv["kind"] == "fwd":
            chan_items[wv["cb"]].append(((wv["id"], 0), min(ys, yd), max(ys, yd)))
        elif wv["kind"] == "back":
            chan_items[wv["ca"]].append(((wv["id"], 0), min(ys, yd), max(ys, yd)))
        elif wv["kind"] == "top":
            chan_items[wv["ca"] + 1].append(((wv["id"], 0), y_top_bus, ys))
            chan_items[wv["cb"]].append(((wv["id"], 1), y_top_bus, yd))
        elif wv["kind"] == "bottom":
            chan_items[wv["ca"]].append(((wv["id"], 0), ys, y_bot_bus))
            chan_items[wv["cb"] + 1].append(((wv["id"], 1), yd, y_bot_bus))
    chan_lanes = {k: _interval_lanes(v) for k, v in chan_items.items()}
    n_chan = {k: (max(v.values()) + 1 if v else 0) for k, v in chan_lanes.items()}

    margin = 8
    pad = 12
    x = margin
    card_x, gutter_x, box_x, card_w, chan_x = {}, {}, {}, {}, {}
    for c in range(5):
        if c > 0:
            chan_x[c] = x
            x += STUB + max(0, n_chan.get(c, 0) - 1) * LP + STUB
        card_x[c] = x
        g = pad + (STUB + n_hook[c] * LP if n_hook[c] else 0)
        gutter_x[c] = x + pad
        box_x[COLS[c]] = x + g
        x += g + bw[COLS[c]] + pad
        card_w[c] = x - card_x[c]
    natural_w = x + margin
    spare = max(0, w_total - natural_w)
    # widen the channels evenly to fill the width, keeping lanes centered
    shift = spare / 6 if spare else 0
    for c in range(5):
        card_x[c] += shift * (c + 0.5)
        gutter_x[c] += shift * (c + 0.5)
        box_x[COLS[c]] += shift * (c + 0.5)
    for c in chan_x:
        chan_x[c] += shift * (c - 0.5 + 0.5)
    W = max(w_total, natural_w)

    def chan_lane_x(k, lane):
        left_edge = card_x[k - 1] + card_w[k - 1]
        right_edge = card_x[k]
        n = n_chan.get(k, 1)
        span = (n - 1) * LP
        mid = (left_edge + right_edge) / 2
        return mid - span / 2 + lane * LP

    def hook_lane_x(c, lane):
        # lanes run from the box edge outward, first lane nearest the box
        return box_x[COLS[c]] - STUB - lane * LP

    # bus tracks
    top_items, bot_items = [], []
    for wv in wires:
        if wv["kind"] == "top":
            xa = chan_lane_x(wv["ca"] + 1, chan_lanes[wv["ca"] + 1][(wv["id"], 0)])
            xb = chan_lane_x(wv["cb"], chan_lanes[wv["cb"]][(wv["id"], 1)])
            top_items.append((wv["id"], min(xa, xb), max(xa, xb)))
        if wv["kind"] == "bottom":
            xa = chan_lane_x(wv["ca"], chan_lanes[wv["ca"]][(wv["id"], 0)])
            xb = chan_lane_x(wv["cb"] + 1, chan_lanes[wv["cb"] + 1][(wv["id"], 1)])
            bot_items.append((wv["id"], min(xa, xb), max(xa, xb)))
    top_tr = _interval_lanes(top_items)
    bot_tr = _interval_lanes(bot_items)
    n_top = max(top_tr.values()) + 1 if top_tr else 0
    n_bot = max(bot_tr.values()) + 1 if bot_tr else 0

    def bx_edge(k, side):
        c = COLS.index(N[k]["area"])
        return box_x[N[k]["area"]] + (bw[N[k]["area"]] if side == "R" else 0)

    # ---- route every wire
    paths = {}
    for wv in wires:
        l = wv["l"]
        s, d = l["from"], l["to"]
        ys, yd = port_index[(wv["id"], "s")], port_index[(wv["id"], "d")]
        xs, xd = bx_edge(s, wv["s_side"]), bx_edge(d, wv["d_side"])
        if wv["kind"] == "hook":
            xl = hook_lane_x(wv["ca"], hook_lanes[wv["ca"]][wv["id"]])
            pts = [(xs, ys), (xl, ys), (xl, yd), (xd, yd)]
        elif wv["kind"] in ("fwd", "back"):
            k = wv["cb"] if wv["kind"] == "fwd" else wv["ca"]
            xl = chan_lane_x(k, chan_lanes[k][(wv["id"], 0)])
            pts = [(xs, ys), (xl, ys), (xl, yd), (xd, yd)]
        elif wv["kind"] == "top":
            x1 = chan_lane_x(wv["ca"] + 1, chan_lanes[wv["ca"] + 1][(wv["id"], 0)])
            x2 = chan_lane_x(wv["cb"], chan_lanes[wv["cb"]][(wv["id"], 1)])
            yt = y_top_bus - top_tr[wv["id"]] * LP
            pts = [(xs, ys), (x1, ys), (x1, yt), (x2, yt), (x2, yd), (xd, yd)]
        else:
            x1 = chan_lane_x(wv["ca"], chan_lanes[wv["ca"]][(wv["id"], 0)])
            x2 = chan_lane_x(wv["cb"] + 1, chan_lanes[wv["cb"] + 1][(wv["id"], 1)])
            yb = y_bot_bus + bot_tr[wv["id"]] * LP
            pts = [(xs, ys), (x1, ys), (x1, yb), (x2, yb), (x2, yd), (xd, yd)]
        paths[wv["id"]] = (pts, wv)

    # ---- the lower band and the drivers
    y_bus_bottom = y_bot_bus + max(0, n_bot - 1) * LP
    y_lower_strip = y_bus_bottom + 40
    y_lower = y_lower_strip + 96
    lower = {"EC": (card_x[0], card_x[2] + card_w[2]), "TC": (card_x[3], card_x[4] + card_w[4])}
    rows_ec = [k for k in model["order"] if N[k]["area"] == "EC"]
    rows_tc = [k for k in model["order"] if N[k]["area"] == "TC"]
    y_lower_end = y_lower + 80 + 40 * ((len(rows_ec) + 2) // 3) + 10
    H = y_lower_end + 12

    ink_wire = D.INK
    out_wires, out_red = [], []
    for wid, (pts, wv) in paths.items():
        l = wv["l"]
        red = wid in red_targets
        dim = lit is not None and wid not in lit
        color = D.RED if red else (D.STONE if dim else ink_wire)
        poly = FG.rounded(pts, R)
        base = D.trim(poly, 0, 7.5)
        dash = D.DASH.get(l["evidence"])
        da = f' stroke-dasharray="{dash}"' if dash else ""
        body = (f'<path d="{D.path_d(base)}" fill="none" stroke="{color}" stroke-width="2"{da} data-texture="{dash or "solid"}"'
                + (' data-red="1"' if red else "") + "/>")
        body += D.arrow_at(poly, 8, 3.6, color)
        # the sign: one small glyph on the wire's first stub, in a capsule
        (x0, y0), (x1, _) = pts[0], pts[1]
        gx = x0 + (13 if x1 > x0 else -13)
        g = FG.GLYPH.get(l["polarity"], "")
        cap = (f'<g class="pill" data-for="{wid}"><rect x="{gx - 7.5:.1f}" y="{y0 - 7.5:.1f}" width="15" height="15" rx="7.5" fill="{bg}" stroke="{color}" stroke-width="1.25"/>'
               + FG.T(gx, y0 + 4.6, g, 13, 700, D.INK if not dim else D.STONE, "middle", extra=' data-sign-glyph="1"') + "</g>")
        grp = f'<g class="link"{D.link_attrs(l)}' + (f' data-target="{reform_id}"' if red else "") + f">{body}{cap}</g>"
        (out_red if red else out_wires).append(grp)

    # ---- cards
    cards = []
    for c in range(5):
        a = COLS[c]
        x0, wc = card_x[c], card_w[c]
        y1 = cards_bottom - 14
        edge = f' stroke="{D.STONE}" stroke-width="1"' if bg == D.WHITE else ""
        cards.append(f'<rect x="{x0:.1f}" y="{y_cards:.1f}" width="{wc:.1f}" height="{y1 - y_cards:.1f}" rx="4" fill="{D.WHITE}"{edge}/>')
        cards.append(FG.T(x0 + 14, y_cards + 38, a, 34, 800, D.INK, family="tight"))
        title = model["region_titles"][a]
        tl = TX.balanced_wrap(title, wc - 64, 15, 700)
        for i, t in enumerate(tl):
            cards.append(FG.T(x0 + 50, y_cards + 22 + 18 * i, t, 15, 700, D.INK))
        cards.append(FG.T(x0 + 14, y_cards + 64, f"{len(card_vars[a])} variables on loops", 13, 400, D.DEEP))
        for k in card_vars[a]:
            red = k in red_targets
            dim = lit is not None and not any(L[w]["from"] == k or L[w]["to"] == k for w in lit)
            xb, yb, hb = box_x[a], box_y[k], box_h[k]
            g = [f'<g class="var"{D.node_attrs(k, model["nodes"][k]["label"])}' + (f' data-red="1" data-target="{reform_id}"' if red else "") + ">",
                 f'<rect x="{xb:.1f}" y="{yb:.1f}" width="{bw[a]:.1f}" height="{hb:.1f}" rx="2" fill="{D.NEWS}"' + (f' stroke="{D.RED}" stroke-width="3"' if red else "") + "/>",
                 f'<rect x="{xb:.1f}" y="{yb:.1f}" width="5" height="{hb:.1f}" fill="{D.STONE if dim else D.INK}"/>',
                 FG.T(xb + 14, yb + 22, k, 14, 800, D.INK, family="tight")]
            for i, t in enumerate(label_lines[k]):
                g.append(FG.T(xb + 14, yb + 42 + 17 * i, t, LABEL, 600, D.INK))
            g.append("</g>")
            cards.append("".join(g))
        yr = col_bottom[a] - 26 * len(card_rest[a]) + 8
        for k in card_rest[a]:
            cards.append(f'<g class="var"{D.node_attrs(k)}>' + FG.T(box_x[a], yr + 4, f"{k}  {model['nodes'][k]['title']}", 13, 600, D.INK) + "</g>")
            cards.append(FG.T(box_x[a], yr + 21, "on no loop", 13, 400, D.DEEP))
            yr += 40
    # ---- the other 72: counted bundles
    bundles = collections.defaultdict(list)
    for k, l in L.items():
        if l["loops"]:
            continue
        bundles[(N[l["from"]]["area"], N[l["to"]]["area"])].append(k)
    def area_center(a):
        if a in COLS:
            c = COLS.index(a)
            return card_x[c] + card_w[c] / 2
        lo, hi = lower[a]
        return (lo + hi) / 2
    stone = D.STONE
    bsvg, btxt = [], []

    def capsule(x, y, n):
        s = str(n)
        w_ = max(22, TX.width(s, 13, 700) + 14)
        return (f'<rect x="{x - w_ / 2:.1f}" y="{y - 10:.1f}" width="{w_:.1f}" height="20" rx="10" fill="{bg}" stroke="{stone}" stroke-width="1.5"/>'
                + FG.T(x, y + 4.6, s, 13, 700, D.INK, "middle"))

    def bundle_group(key, links_, inner):
        return (f'<g class="bundle" data-from-area="{key[0]}" data-to-area="{key[1]}" data-count="{len(links_)}" data-links="{" ".join(sorted(links_))}">'
                + inner + "</g>")
    # drivers: tabs on the top edge
    xs_tabs = []
    tab_w = (W - 2 * margin - 4 * 16) / 5
    drivers = [k for k in model["order"] if N[k]["area"] == "X"]
    for i, k in enumerate(drivers):
        xt = margin + i * (tab_w + 16)
        xs_tabs.append(xt)
        title_lines = TX.balanced_wrap(model["nodes"][k]["title"], tab_w - 60, 13, 600)
        bsvg.append(f'<g class="var"{D.node_attrs(k)}><path d="M{xt:.1f} 66 L{xt:.1f} 10 Q{xt:.1f} 4 {xt + 6:.1f} 4 L{xt + tab_w - 6:.1f} 4 Q{xt + tab_w:.1f} 4 {xt + tab_w:.1f} 10 L{xt + tab_w:.1f} 66 Z" fill="{D.INK}"/>'
                    + FG.T(xt + 12, 28, k, 15, 800, D.NEWS, family="tight")
                    + "".join(FG.T(xt + 46, 26 + 17 * j, t, 13, 600, D.NEWS) for j, t in enumerate(title_lines)) + "</g>")
    bsvg.append(f'<rect x="{margin}" y="66" width="{W - 2 * margin:.1f}" height="4" fill="{D.INK}"/>')
    bsvg.append(FG.T(margin, 94, "Outside drivers: conditions the model treats as given", 13, 600, D.DEEP))
    # driver bundles into each card and the layers
    for a in COLS + ["EC", "TC"]:
        ks = bundles.get(("X", a), [])
        if not ks:
            continue
        if a in COLS:
            xc = area_center(a) - 30
            inner = (f'<path d="M{xc:.1f} 70 L{xc:.1f} {y_cards - 8:.1f}" stroke="{stone}" stroke-width="2" fill="none"/>'
                     + D.arrow_at([(xc, 70), (xc, y_cards - 1)], 8, 3.6, stone) + capsule(xc, 120, len(ks)))
            bsvg.append(bundle_group(("X", a), ks, inner))
        else:
            btxt.append((("X", a), ks))
    # core to core bundles above the cards, on their own tracks
    core_pairs = [(p, ks) for p, ks in bundles.items() if p[0] in COLS and p[1] in COLS and p[0] != p[1]]
    core_pairs.sort(key=lambda t: (abs(COLS.index(t[0][0]) - COLS.index(t[0][1])), t[0]))
    track_y = [134, 156, 178]
    slot_used = collections.Counter()
    items = []
    for (a, b), ks in core_pairs:
        xa = area_center(a) + 6 + 14 * slot_used[a]
        slot_used[a] += 1
        xb = area_center(b) + 6 + 14 * slot_used[b]
        slot_used[b] += 1
        items.append((((a, b), tuple(ks)), min(xa, xb), max(xa, xb), xa, xb))
    tracks = _interval_lanes([(it[0], it[1], it[2]) for it in items], sep=26)
    for key, lo, hi, xa, xb in items:
        (a, b), ks = key
        ty = track_y[min(tracks[key], 2)] - 6 * max(0, tracks[key] - 2)
        pts = [(xa, y_cards), (xa, ty), (xb, ty), (xb, y_cards)]
        poly = FG.rounded(pts, R)
        inner = (f'<path d="{D.path_d(D.trim(poly, 0, 7.5))}" stroke="{stone}" stroke-width="2" fill="none"/>' + D.arrow_at(poly, 8, 3.6, stone)
                 + capsule((xa + xb) / 2, ty, len(ks)))
        bsvg.append(bundle_group((a, b), list(ks), inner))
    # within-card counts in the card footers
    for a in COLS:
        ks = bundles.get((a, a), [])
        c = COLS.index(a)
        txt = f"{len(ks)} more connections inside {a}, on no loop" if ks else "No other connections inside"
        fl = TX.wrap(txt, card_w[c] - 28, 13, 400)
        inner = "".join(FG.T(card_x[c] + 14, cards_bottom - 48 + 17 * i, t, 13, 400, D.DEEP) for i, t in enumerate(fl))
        bsvg.append(bundle_group((a, a), ks, inner))
    # core and lower band
    lower_pairs = [(p, ks) for p, ks in bundles.items() if (p[0] in COLS and p[1] in ("EC", "TC")) or (p[0] in ("EC", "TC") and p[1] in COLS)]
    lower_pairs.sort(key=lambda t: (t[0][0], t[0][1]))
    lslot = collections.Counter()
    l_items = []
    for (a, b), ks in lower_pairs:
        core = a if a in COLS else b
        lay = b if a in COLS else a
        c = COLS.index(core)
        xcore = card_x[c] + 22 + 26 * lslot[core]
        lslot[core] += 1
        lo, hi = lower[lay]
        xlay = min(max(xcore, lo + 30), hi - 30)
        l_items.append((((a, b), tuple(ks)), min(xcore, xlay), max(xcore, xlay), xcore, xlay, a in COLS))
    ltr = _interval_lanes([(it[0], it[1], it[2]) for it in l_items], sep=26)
    for key, lo, hi, xcore, xlay, down in l_items:
        (a, b), ks = key
        ty = y_lower_strip + 20 + 22 * ltr[key]
        if down:
            pts = [(xcore, cards_bottom - 14), (xcore, ty), (xlay, ty), (xlay, y_lower)]
        else:
            pts = [(xlay, y_lower), (xlay, ty), (xcore, ty), (xcore, cards_bottom - 14)]
        pts = [p for i, p in enumerate(pts) if i == 0 or p != pts[i - 1]]
        if len(pts) >= 3 and abs(pts[1][0] - pts[2][0]) < 1:
            pts = [pts[0], pts[-1]]
        poly = FG.rounded(pts, R)
        cx_ = xcore if abs(xcore - xlay) < 30 else (xcore + xlay) / 2
        inner = (f'<path d="{D.path_d(D.trim(poly, 0, 7.5))}" stroke="{stone}" stroke-width="2" fill="none"/>' + D.arrow_at(poly, 8, 3.6, stone)
                 + capsule(cx_, ty if abs(xcore - xlay) >= 30 else (cards_bottom + y_lower) / 2, len(ks)))
        bsvg.append(bundle_group((a, b), list(ks), inner))
    # lower band cards
    for lay, rows, title, ncols in (("EC", rows_ec, "Economy layer", 3), ("TC", rows_tc, "Technology layer", 2)):
        lo, hi = lower[lay]
        bsvg.append(f'<rect x="{lo:.1f}" y="{y_lower:.1f}" width="{hi - lo:.1f}" height="{y_lower_end - y_lower:.1f}" rx="4" fill="{D.WHITE}"'
                    + (f' stroke="{D.STONE}" stroke-width="1"' if bg == D.WHITE else "") + "/>")
        bsvg.append(FG.T(lo + 14, y_lower + 30, title, 17, 800, D.INK, family="tight"))
        notes = []
        inside = bundles.get((lay, lay), [])
        other = "TC" if lay == "EC" else "EC"
        between = bundles.get((other, lay), [])
        if inside:
            bsvg.append(bundle_group((lay, lay), inside, ""))
            notes.append(f"{len(inside)} connections inside")
        if between:
            bsvg.append(bundle_group((other, lay), between, ""))
            notes.append(f"{len(between)} from the {'technology' if other == 'TC' else 'economy'} layer")
        for (pair, ks) in btxt:
            if pair[1] == lay:
                bsvg.append(bundle_group(pair, ks, ""))
                notes.append(f"{len(ks)} from outside drivers")
        bsvg.append(FG.T(lo + 14, y_lower + 50, "; ".join(notes) + ". None sits on a named loop.", 13, 400, D.DEEP))
        cw = (hi - lo - 28) / ncols
        for i, k in enumerate(rows):
            cx0 = lo + 14 + (i % ncols) * cw
            cy0 = y_lower + 80 + 40 * (i // ncols)
            name = model["nodes"][k]["title"]
            nl = TX.wrap(name, cw - 52, 13, 400)
            if len(nl) > 1:
                name = nl[0]
            full = model["nodes"][k]["title"]
            bsvg.append(f'<g class="var"{D.node_attrs(k)}>' + FG.T(cx0, cy0, k, 13, 700, D.INK)
                        + "".join(FG.T(cx0 + 44, cy0 + 16 * j, t, 13, 400, D.INK) for j, t in enumerate(TX.balanced_wrap(full, cw - 52, 13, 400))) + "</g>")
        y_lower_end = max(y_lower_end, y_lower + 80 + 40 * ((len(rows) + ncols - 1) // ncols) + 10)
    # TC to EC across the lower band
    # bus labels
    bus = []
    if n_top:
        bus.append(FG.T(card_x[0], y_top_bus - (n_top - 1) * LP - 30, "Over the top: loop steps that skip an area going forward", 13, 600, D.DEEP))
    if n_bot:
        bus.append(FG.T(card_x[0] + card_w[0] + 12, y_bus_bottom + 22, "The return line: loop steps that run back across areas", 13, 600, D.DEEP))
    H = max(H, y_lower_end + 16)
    body = ("".join(cards) + "".join(bsvg) + "".join(out_wires) + "".join(out_red) + "".join(bus))
    label = ("Whole system as a circuit: five area cards, A to E. The 46 connections on named loops are drawn as wires; the other 72 "
             "are counted bundles. The economy and technology layers sit below, the outside drivers above.")
    view = "circuit-map"
    attrs = ' data-direction="field-guide"' + (f' data-reform="{reform_id}"' if reform_id else "") + (f' data-lit="{lit_loop}"' if lit_loop else "")
    stats = {"W": W, "H": H, "natural_w": natural_w, "lanes": n_chan, "hooks": n_hook, "top": n_top, "bottom": n_bot, "bw": bw}
    return FG.svg_doc(W, H, body, label, view, attrs, bg=None), stats
