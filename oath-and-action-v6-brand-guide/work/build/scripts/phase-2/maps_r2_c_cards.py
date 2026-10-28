"""Direction C, Loop Lines: the loop's own line lifted from the map (catalog miniature), the loop card drawing at
full size, the locator inset and the sketched-loop tiles. Every geometry comes from the one station table, so a
loop has the same shape on the poster, in the catalog and on its card."""
import math

import maps_r2_c_draw as D
import maps_r2_c_geom as G

M, LOOPS = G.M, G.LOOPS
T, esc = D.T, D.esc
MINI_SCALE = 0.4       # one shared scale for every miniature: 0.4 of the poster's 36 px grid cell
# miniature name sides that keep a long loop's names inside its own drawing (layout data, like the station table)
MINI_SIDES = {("R4b", "B5"): "se", ("R4b", "C4"): "w", ("R1b", "B1"): "e", ("R1b", "D3"): "nw"}


def loop_corridors(lid):
    """The loop's steps with the corridor each rides, in chain order."""
    out = []
    for st in LOOPS[lid]["steps"]:
        a, b = sorted((st["from"], st["to"]))
        out.append((st, a, b))
    return out


def lifted(L, lid, scale, pitch=None):
    """The loop's tracks as they sit on the map (same route, same offset in each corridor), scaled about the
    loop's own bounding box. Returns tracks [(step, pts)], station points, the scaled transform and the bbox."""
    pitch = pitch if pitch is not None else L.pitch
    tr = []
    for st, a, b in loop_corridors(lid):
        t = next(t for t in L.tracks[(a, b)] if t["link"] == st["id"] and t["loop"] == lid)
        base = L.corridor_px(a, b)
        off = t["offset"] / L.pitch * pitch / scale  # keep the order, set the pitch in the target scale
        pts = G.offset_poly(base, off)
        if st["from"] != a:
            pts = list(reversed(pts))
            off = -off
        tr.append((st, pts, off))
    xs = [p[0] for _, pts, _ in tr for p in pts]
    ys = [p[1] for _, pts, _ in tr for p in pts]
    bb = (min(xs), min(ys), max(xs), max(ys))
    return tr, bb


def _xf(p, bb, scale, ox, oy):
    return (ox + (p[0] - bb[0]) * scale, oy + (p[1] - bb[1]) * scale)


def ghost_stubs(L, lid, scale, bb, ox, oy, length=0.85):
    """Short Stone stubs for the corridors that leave each shared station, so a miniature keeps its context."""
    lp = LOOPS[lid]
    own = {tuple(sorted((st["from"], st["to"]))) for st in lp["steps"]}
    out = []
    for stn in lp["stations"]:
        sid = stn["code"]
        for (a, b) in L.tracks:
            if sid not in (a, b) or (a, b) in own:
                continue
            pts = L.corridor_px(a, b)
            if sid != a:
                pts = list(reversed(pts))
            p0 = pts[0]
            u = G.unit(pts[1][0] - p0[0], pts[1][1] - p0[1])
            p1 = (p0[0] + u[0] * L.cell * length, p0[1] + u[1] * L.cell * length)
            q0, q1 = _xf(p0, bb, scale, ox, oy), _xf(p1, bb, scale, ox, oy)
            links = " ".join(t["link"] for t in L.tracks[(a, b)])
            out.append(f'<path d="M{q0[0]:.1f} {q0[1]:.1f} L{q1[0]:.1f} {q1[1]:.1f}" stroke="{D.STONE}" stroke-width="1.6" '
                       f'stroke-linecap="round" fill="none" data-ghost="{esc(links)}" data-at="{sid}"/>')
    return out


def miniature(L, lid, scale=MINI_SCALE, names=True, pad=None, ink=D.CHARCOAL, ground=D.WHITE, view="c-mini", line_w=3.0,
              max_w=276):
    """Catalog miniature: the loop's own line lifted from the poster at one shared scale, station names in Inter
    13, ghost stubs in Stone. Notation budget for a miniature: texture and the hollow line only. When the names
    would make it wider than its card, the end names move above and below the line."""
    for attempt in range(3):
        svg, W, H = _miniature(L, lid, scale, names, pad, ink, ground, view, line_w, attempt)
        if W <= max_w or not names:
            break
    return svg, W, H


def _miniature(L, lid, scale, names, pad, ink, ground, view, line_w, attempt):
    tr, bb = lifted(L, lid, scale, pitch=5.0)
    lp = LOOPS[lid]
    names_w = {}
    pad = pad or (8, 8, 8, 8)
    # first pass: label boxes, to size the drawing
    stations = [s["code"] for s in lp["stations"]]
    spx = {sid: L.station_px(sid) for sid in stations}
    w0 = (bb[2] - bb[0]) * scale
    h0 = (bb[3] - bb[1]) * scale
    lab_specs = []
    for sid in stations:
        name = M["nodes"][sid]["short"]
        lines = D.wrap_to(name, 112 if attempt < 2 else 92, 13, 600)
        lw = max(D.text_w(x, 13, 600) for x in lines)
        lh = 16 * len(lines)
        side = MINI_SIDES.get((lid, sid)) or mini_side(L, lid, sid)
        if attempt >= 1:
            side = {"e": "ne", "w": "sw", "se": "s", "sw": "s", "ne": "n", "nw": "n"}.get(side, side)
        lab_specs.append((sid, lines, lw, lh, side))
    # place in a provisional frame to measure
    ext = [0, 0, w0, h0]
    placed = []
    for sid, lines, lw, lh, side in lab_specs:
        p = _xf(spx[sid], bb, scale, 0, 0)
        bx = mini_label_box(p, lw, lh, side)
        placed.append((sid, lines, lw, lh, side, bx))
        if names:
            ext = [min(ext[0], bx[0]), min(ext[1], bx[1]), max(ext[2], bx[2]), max(ext[3], bx[3])]
    ox, oy = pad[3] - ext[0], pad[0] - ext[1]
    W = ext[2] - ext[0] + pad[1] + pad[3]
    H = ext[3] - ext[1] + pad[0] + pad[2]
    body = ghost_stubs(L, lid, scale, bb, ox, oy)
    for st, pts, off in tr:
        q = [_xf(p, bb, scale, ox, oy) for p in pts]
        d, _ = G.rounded_path(q, L.radius * scale * 1.4, off * scale)
        dash, code = D.dash_for(st["evidence"], line_w)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        body.append(f'<g class="step" data-loop="{lid}"{D.step_attrs(st["id"])}><path d="{d}" fill="none" stroke="{ink}" '
                    f'stroke-width="{line_w}"{da} data-texture="{code}" data-weight="{line_w}"/></g>')
    for sid in stations:
        p = _xf(spx[sid], bb, scale, ox, oy)
        shared = len(G.station_loops(sid)) > 1
        if shared:
            body.append(f'<g class="var" data-node="{sid}" data-label="{esc(M["nodes"][sid]["short"])}" data-kind="capsule">'
                        f'<rect x="{p[0] - 9:.1f}" y="{p[1] - 6:.1f}" width="18" height="12" rx="6" fill="{ground}" stroke="{ink}" stroke-width="2"/></g>')
        else:
            body.append(f'<g class="var" data-node="{sid}" data-label="{esc(M["nodes"][sid]["short"])}" data-kind="ring">'
                        f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6" fill="{ground}" stroke="{ink}" stroke-width="2"/></g>')
    if names:
        for sid, lines, lw, lh, side, bx in placed:
            x0, y0 = bx[0] + ox, bx[1] + oy
            anchor = "start"
            for i, ln in enumerate(lines):
                body.append(T(x0, y0 + 12 + i * 16, ln, 13, 600, ink, "start", extra=f' data-name-for="{sid}"' if i == 0 else ""))
    label = f"Loop {lid} miniature: {lp['title']}"
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}" role="img" '
           f'aria-label="{esc(label)}" data-view="{view}" data-loop="{lid}" data-scale="{scale}"><title>{esc(label)}</title>{D.STYLE}'
           f'<rect x="0" y="0" width="{W:.0f}" height="{H:.0f}" fill="{ground}"/>' + "".join(body) + "</svg>")
    return svg, W, H


def mini_side(L, lid, sid):
    """Which side a miniature puts a station name on: away from the loop's own steps at that station."""
    p = L.station_px(sid)
    lp = LOOPS[lid]
    dirs = []
    for st in lp["steps"]:
        if sid in (st["from"], st["to"]):
            a, b = sorted((st["from"], st["to"]))
            pts = L.corridor_px(a, b)
            if sid != a:
                pts = list(reversed(pts))
            dirs.append(G.unit(pts[1][0] - pts[0][0], pts[1][1] - pts[0][1]))
    vx = -sum(d[0] for d in dirs)
    vy = -sum(d[1] for d in dirs)
    if abs(vx) < 1e-6 and abs(vy) < 1e-6:
        vx, vy = 0, -1
    ang = math.degrees(math.atan2(vy, vx)) % 360
    for name, a0 in (("e", 0), ("se", 45), ("s", 90), ("sw", 135), ("w", 180), ("nw", 225), ("n", 270), ("ne", 315)):
        if abs((ang - a0 + 180) % 360 - 180) <= 22.5:
            return name
    return "n"


def mini_label_box(p, lw, lh, side, gap=15):
    x, y = p
    if side == "e":
        return (x + gap, y - lh / 2, x + gap + lw, y + lh / 2)
    if side == "w":
        return (x - gap - lw, y - lh / 2, x - gap, y + lh / 2)
    if side == "n":
        return (x - lw / 2, y - gap - lh, x + lw / 2, y - gap)
    if side == "s":
        return (x - lw / 2, y + gap, x + lw / 2, y + gap + lh)
    if side == "ne":
        return (x + gap * 0.6, y - gap * 0.6 - lh, x + gap * 0.6 + lw, y - gap * 0.6)
    if side == "nw":
        return (x - gap * 0.6 - lw, y - gap * 0.6 - lh, x - gap * 0.6, y - gap * 0.6)
    if side == "se":
        return (x + gap * 0.6, y + gap * 0.6, x + gap * 0.6 + lw, y + gap * 0.6 + lh)
    return (x - gap * 0.6 - lw, y + gap * 0.6, x - gap * 0.6, y + gap * 0.6 + lh)


def sketched_tile(lid, ink=D.CHARCOAL, ground=D.WHITE, w=260, h=120):
    """A sketched loop has no numbered chain and no stations on the map. Its tile draws the chain as a closed hollow
    line (Gate 1 mark M1) with V7's chain labels, so it keeps the frame of the other cards."""
    lp = LOOPS[lid]
    labels = [s["label"] for s in lp["stations"]]
    n = len(labels)
    body = []
    cx, cy = w / 2, h / 2 + 4
    if n == 2:
        pts = [(cx - 36, cy), (cx + 36, cy)]
    else:
        pts = [(cx - 70, cy + 22), (cx, cy - 28), (cx + 70, cy + 22)]
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        if n == 2:
            off = -9 if i == 0 else 9
            p = (p[0], p[1] + off)
            q = (q[0], q[1] + off)
            if i == 1:
                p, q = (pts[1][0], pts[1][1] + off), (pts[0][0], pts[0][1] + off)
        st = lp["steps"][i]
        body.append(f'<g class="step" data-concept="1" data-step="{i + 1}" data-sign="{st["polarity"]}" '
                    f'data-from-label="{esc(st["from_label"])}" data-to-label="{esc(st["to_label"])}">'
                    f'<path d="M{p[0]:.1f} {p[1]:.1f} L{q[0]:.1f} {q[1]:.1f}" stroke="{ink}" stroke-width="5" fill="none" data-texture="hollow"/>'
                    f'<path d="M{p[0]:.1f} {p[1]:.1f} L{q[0]:.1f} {q[1]:.1f}" stroke="{ground}" stroke-width="2" fill="none"/></g>')
    for i, p in enumerate(pts):
        body.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6" fill="{ground}" stroke="{ink}" stroke-width="2" stroke-dasharray="none"/>')
    return body, pts, labels


# ------------------------------------------------------------------ the loop card drawing

CARD_LINE = 6.0


def _hit(a, b, pad=6):
    return a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad


def _block_box(ax, ty, anchor, w, h):
    if anchor == "start":
        return (ax, ty, ax + w, ty + h)
    if anchor == "end":
        return (ax - w, ty, ax, ty + h)
    return (ax - w / 2, ty, ax + w / 2, ty + h)


def card_drawing(L, lid, reform=None, width=980, height=440, phone=False, labels=None):
    """Try a few scales and offsets for the drawing and keep the one whose labels collide least."""
    best = None
    tries = [(1.0, 0, 0)]
    if LOOPS[lid]["n"] > 2 and (labels or (labels is None and not phone)):
        tries = [(k, dx, dy) for k in (1.0, 0.9, 0.8, 0.7) for dx in (-240, -160, -80, 0, 80, 160) for dy in (-60, -20, 20, 60)]
    for k, dx, dy in tries:
        sc, svg = _card_drawing(L, lid, reform, width, height, phone, labels, k, dx, dy)
        if best is None or sc < best[0]:
            best = (sc, svg)
    return best[1]


def _card_drawing(L, lid, reform, width, height, phone, labels, k=1.0, dx=0, dy=0):
    """The loop card's drawing: the loop's own line at full size, with the shape it has on the map. A two-step loop
    is a closed shuttle whose line turns around each station; a longer loop keeps the map's polygon. Each step
    carries its ID and V7 name, its sign tag, its grade word (with the record square when documented) and its delay
    ticks; each station carries its name in Inter Tight 700 and V7's reading rule for a higher value. Red marks only
    the targets of the one reform the card names. Labels are placed by a collision score."""
    lp = LOOPS[lid]
    labels = (not phone) if labels is None else labels
    targets = set(M["reforms"][reform]["targets"]) if reform else set()
    stations = [s["code"] for s in lp["stations"]]
    spx = {sid: L.station_px(sid) for sid in stations}
    tr, bb = lifted(L, lid, 1.0, pitch=0.0)
    bw, bh = max(bb[2] - bb[0], 1), max(bb[3] - bb[1], 1)
    ring_r = 22 if not phone else 17
    sep = 34 if not phone else 24
    name_size = 22 if not phone else 18
    rule_size = 15 if not phone else 14
    blk_w = 212 if not phone else 150
    if lp["n"] == 2:
        span = width - (2 * (blk_w / 2 + 16) if labels else 2 * (ring_r + sep + 14))
        scale = span / max(bw, bh)
        ox = (width - max(bw, bh) * scale) / 2
        oy = height / 2 - (bh * scale) / 2
    else:
        mx, my = (230, 150) if labels else (40, 40)
        scale = min((width - 2 * mx) / bw, (height - 2 * my) / bh) * k
        ox = (width - bw * scale) / 2 + dx
        oy = (height - bh * scale) / 2 + dy
    X = lambda p: (ox + (p[0] - bb[0]) * scale, oy + (p[1] - bb[1]) * scale)
    paths, segs, step_info = [], [], []
    if lp["n"] == 2:
        pa, pb = X(spx[stations[0]]), X(spx[stations[1]])
        for i, st in enumerate(lp["steps"]):
            s0, s1 = (pa, pb) if i == 0 else (pb, pa)
            uu = G.unit(s1[0] - s0[0], s1[1] - s0[1])
            nn = (uu[1], -uu[0])  # left of travel: the loop runs clockwise
            p0 = (s0[0] + nn[0] * sep, s0[1] + nn[1] * sep)
            p1 = (s1[0] + nn[0] * sep, s1[1] + nn[1] * sep)
            q = (s1[0] - nn[0] * sep, s1[1] - nn[1] * sep)
            d = f"M{p0[0]:.1f} {p0[1]:.1f} L{p1[0]:.1f} {p1[1]:.1f} A{sep} {sep} 0 0 1 {q[0]:.1f} {q[1]:.1f}"
            step_info.append((st, d, p0, p1, nn))
            segs.append((p0, p1))
    else:
        cxp = sum(X(spx[s])[0] for s in stations) / len(stations)
        cyp = sum(X(spx[s])[1] for s in stations) / len(stations)
        for st, pts, off in tr:
            q = [X(p) for p in pts]
            d, _ = G.rounded_path(q, 30, 0)
            run = max(G.straight_runs(q), key=lambda r: r[2])
            uu = G.unit(run[1][0] - run[0][0], run[1][1] - run[0][1])
            mxp = ((run[0][0] + run[1][0]) / 2, (run[0][1] + run[1][1]) / 2)
            nn = (-uu[1], uu[0])
            if (mxp[0] - cxp) * nn[0] + (mxp[1] - cyp) * nn[1] < 0:
                nn = (-nn[0], -nn[1])
            step_info.append((st, d, run[0], run[1], nn))
            for i in range(len(q) - 1):
                segs.append((q[i], q[i + 1]))
    occupied = []
    total = 0.0
    for sid in stations:
        p = X(spx[sid])
        occupied.append((p[0] - ring_r - 10, p[1] - ring_r, p[0] + ring_r + 10, p[1] + ring_r))
    # step label blocks
    body_steps, body_labels = [], []
    for st, d, p0, p1, nn in step_info:
        link = st["id"]
        name = M["links"][link]["name"]
        lines = D.wrap_to(name, 250 if not phone else 160, 15, 600)
        gw = D.GRADE_WORD[st["evidence"]]
        gtxt = f"{gw}. {D.DELAY_WORD[st['delay']].capitalize()}."
        extra_line = link in set(lp["weakest"])
        h = 18 + 18 * len(lines) + 18 + (18 if extra_line else 0)
        w = max([D.text_w(x, 15, 600) for x in lines] + [D.text_w(gtxt, 13, 400) + 14, 40])
        uu = G.unit(p1[0] - p0[0], p1[1] - p0[1])
        Lr = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
        cands = []
        for f in (0.5, 0.38, 0.62):
            m = (p0[0] + uu[0] * Lr * f, p0[1] + uu[1] * Lr * f)
            for side, pref in ((1, 0), (-1, 40)):
                n2 = (nn[0] * side, nn[1] * side)
                off = 22 + (sep if (lp["n"] == 2 and side < 0) else 0)
                c = (m[0] + n2[0] * off, m[1] + n2[1] * off)
                if abs(n2[0]) < 0.45:
                    anchor, ty = "middle", (c[1] - h if n2[1] < 0 else c[1])
                else:
                    anchor, ty = ("start" if n2[0] > 0 else "end"), c[1] - h / 2
                cands.append((anchor, c[0], ty, pref + abs(f - 0.5) * 60))
        best, bs = None, 1e18
        for anchor, ax, ty, pref in cands:
            bx = _block_box(ax, ty, anchor, w, h)
            sc = pref
            if bx[0] < 4 or bx[2] > width - 4 or bx[1] < 4 or bx[3] > height - 4:
                sc += 5000
            for ob in occupied:
                if _hit(bx, ob):
                    sc += 1000
            for (a, b) in segs:
                if D._seg_box(a, b, (bx[0] - 8, bx[1] - 8, bx[2] + 8, bx[3] + 8)):
                    sc += 1500
            if sc < bs:
                best, bs = (anchor, ax, ty, bx), sc
        anchor, ax, ty, bx = best
        total += bs
        occupied.append(bx)
        lab = [T(ax, ty + 13, link, 13, 700, D.CHARCOAL, anchor)]
        for i, ln in enumerate(lines):
            lab.append(T(ax, ty + 13 + 18 * (i + 1), ln, 15, 600, D.CHARCOAL, anchor))
        yg = ty + 13 + 18 * (len(lines) + 1)
        if st["evidence"] == "documented":
            tw = D.text_w(gtxt, 13, 400) + 12
            rx = ax - tw / 2 if anchor == "middle" else (ax if anchor == "start" else ax - tw)
            lab.append(f'<rect x="{rx:.1f}" y="{yg - 9:.1f}" width="7" height="7" fill="{D.CHARCOAL}" data-record="1"/>')
            lab.append(T(rx + 12, yg, gtxt, 13, 400, D.DEEP, "start"))
        else:
            lab.append(T(ax, yg, gtxt, 13, 400, D.DEEP, anchor))
        if extra_line:
            lab.append(T(ax, yg + 18, "Least certain step", 13, 700, D.CHARCOAL, anchor, extra=f' data-weakest="{link}"'))
        body_steps.append((st, d, p0, p1, nn, '<g class="steplabel" data-for="' + link + '">' + "".join(lab) + "</g>"))
    # station blocks
    for sid in stations:
        p = X(spx[sid])
        nm = M["nodes"][sid]["short"]
        lines = D.wrap_to(nm, blk_w, name_size, 700)
        rule = D.wrap_to(higher_rule(sid), blk_w, rule_size, 400)
        w = max([D.text_w(x, name_size, 700, True) for x in lines] + [D.text_w(x, rule_size, 400) for x in rule])
        h = name_size * 1.15 * len(lines) + (rule_size + 4) * len(rule) + 6
        gap = ring_r + 14
        if lp["n"] == 2:
            gap += sep
        cands = []
        for side, pref in (("s", 0), ("n", 5), ("e", 10), ("w", 10), ("se", 20), ("sw", 20), ("ne", 25), ("nw", 25)):
            ux = {"e": 1, "w": -1, "n": 0, "s": 0, "ne": 0.7, "nw": -0.7, "se": 0.7, "sw": -0.7}[side]
            uy = {"e": 0, "w": 0, "n": -1, "s": 1, "ne": -0.7, "nw": -0.7, "se": 0.7, "sw": 0.7}[side]
            for extra, pe in ((0, 0), (26, 15)):
                cx, cy = p[0] + ux * (gap + extra), p[1] + uy * (gap + extra)
                anchor = "middle" if abs(ux) < 0.1 else ("start" if ux > 0 else "end")
                ty = cy - h if uy < -0.1 else (cy if uy > 0.1 else cy - h / 2)
                cands.append((anchor, cx, ty, pref + pe))
        best, bs = None, 1e18
        for anchor, ax, ty, pref in cands:
            bx = _block_box(ax, ty, anchor, w, h)
            sc = pref
            if bx[0] < 4 or bx[2] > width - 4 or bx[1] < 4 or bx[3] > height - 4:
                sc += 5000
            for ob in occupied:
                if _hit(bx, ob):
                    sc += 1000
            for (a, b) in segs:
                if D._seg_box(a, b, (bx[0] - 8, bx[1] - 8, bx[2] + 8, bx[3] + 8)):
                    sc += 1500
            if sc < bs:
                best, bs = (anchor, ax, ty, bx), sc
        anchor, ax, ty, bx = best
        total += bs
        occupied.append(bx)
        out = []
        for i, ln in enumerate(lines):
            out.append(T(ax, ty + name_size + i * name_size * 1.15, ln, name_size, 700, D.CHARCOAL, anchor, "d"))
        yy = ty + name_size * 1.15 * len(lines) + rule_size + 4
        for i, ln in enumerate(rule):
            out.append(T(ax, yy + i * (rule_size + 4), ln, rule_size, 400, D.DEEP, anchor))
        body_labels.append(f'<g class="stationlabel" data-for="{sid}">' + "".join(out) + "</g>")
    body = []
    for st, d, p0, p1, nn, lab in body_steps:
        body.append(card_step(lid, st, d, p0, p1, targets))
        body_labels.insert(0, lab)
    if not labels:
        body_labels = []
    for sid in stations:
        body.append(card_station(sid, X(spx[sid]), ring_r, sid in targets, phone))
    label = f"Loop {lid} at full size: {lp['title']}"
    extra = f' data-loop="{lid}"' + (f' data-reform="{reform}"' if reform else "")
    return total, D.svg_doc(width, height, "".join(body) + "".join(body_labels), label,
                            "c-card" if not phone else "c-card-phone", D.WHITE, extra=extra)


def card_step(lid, st, d, p0, p1, targets):
    link = st["id"]
    red = link in targets
    col = D.RED if red else D.CHARCOAL
    dash, code = D.dash_for(st["evidence"], CARD_LINE)
    da = f' stroke-dasharray="{dash}"' if dash else ""
    ra = ' data-red="1"' if red else ""
    out = [f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{CARD_LINE}"{da} data-texture="{code}" data-weight="{CARD_LINE}"{ra}/>']
    uu = G.unit(p1[0] - p0[0], p1[1] - p0[1])
    Lr = math.hypot(p1[0] - p0[0], p1[1] - p0[1])
    nt = D.TICKS[st["delay"]]
    tk = []
    n = (-uu[1], uu[0])
    for i in range(nt):
        s = Lr - 52 - i * 7
        c = (p0[0] + uu[0] * s, p0[1] + uu[1] * s)
        tk.append(f'<line x1="{c[0] + n[0] * 8:.1f}" y1="{c[1] + n[1] * 8:.1f}" x2="{c[0] - n[0] * 8:.1f}" y2="{c[1] - n[1] * 8:.1f}" stroke="{col}" stroke-width="2"/>')
    out.append(f'<g class="ticks" data-ticks="{nt}">' + "".join(tk) + "</g>")
    m = (p0[0] + uu[0] * Lr * 0.5, p0[1] + uu[1] * Lr * 0.5)
    out.append(D.sign_tag(m, uu, st["polarity"], D.Theme("white-card"), 6, extra=f' data-for="{link}" data-sign="{st["polarity"]}"'))
    return f'<g class="step" data-loop="{lid}"{D.step_attrs(link)}>' + "".join(out) + "</g>"


def card_station(sid, p, r, red, phone):
    col = D.RED if red else D.CHARCOAL
    sw = 4 if red else 3
    ra = ' data-red="1"' if red else ""
    kind = "capsule" if len(G.station_loops(sid)) > 1 else "ring"
    if kind == "capsule":
        w = r * 2 + 16
        shape = f'<rect x="{p[0] - w / 2:.1f}" y="{p[1] - r:.1f}" width="{w:.1f}" height="{2 * r}" rx="{r}" fill="{D.WHITE}" stroke="{col}" stroke-width="{sw}"/>'
    else:
        shape = f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r}" fill="{D.WHITE}" stroke="{col}" stroke-width="{sw}"/>'
    return (f'<g class="var" data-node="{sid}" data-label="{esc(M["nodes"][sid]["short"])}" data-kind="{kind}"{ra}>{shape}'
            f'{T(p[0], p[1] + 5.5, sid, 15 if not phone else 14, 700, D.CHARCOAL, "middle")}</g>')


def higher_rule(sid):
    s = M["nodes"][sid]["increase_means"]
    s = s.replace("A higher value means ", "")
    return "Higher: " + s


def locator_layout(L, w, h, margin=10):
    """The poster layout scaled to fit an inset of w by h px, same routes."""
    cs = [c for cells in L.routes_cells.values() for c in cells]
    c0, c1 = min(c[0] for c in cs), max(c[0] for c in cs)
    r0, r1 = min(c[1] for c in cs), max(c[1] for c in cs)
    cell = min((w - 2 * margin) / (c1 - c0), (h - 2 * margin) / (r1 - r0))
    ox = (w - (c1 - c0) * cell) / 2 - c0 * cell
    oy = (h - (r1 - r0) * cell) / 2 - r0 * cell
    return L.scaled(cell, ox, oy, pitch=cell * 0.28, radius=cell * 0.6)


def locator(L_small, lid, w, h):
    """The locator inset: the working map on Newsprint, the loop lit in Charcoal and every other line in Stone."""
    th = D.Theme("newsprint")
    net, _ = D.network(L_small, th, lit_loop=lid, show_labels=False, show_signs=False, show_bullets=False,
                       line_w=2.5, show_ids=False, station_scale=0.42, hub_names=False)
    label = f"Locator: Loop {lid} lit on the whole map"
    return D.svg_doc(w, h, net, label, "c-locator", D.NEWS,
                     extra=f' data-loop="{lid}" data-lit="{lid}" data-cell="{L_small.cell}" data-ox="{L_small.ox}" data-oy="{L_small.oy}"')
