"""Direction C, Loop Lines: every drawing, from one network geometry (maps_r2_c_geom.py).

Views: the poster on Prussian; the working map on Newsprint with one line lit; the reform view on White; the
poster band for the catalog head; each loop's own line lifted from the map (the catalog miniature); the loop card
at full size with its locator inset.

Every data mark carries data-* attributes that maps_r2_c_verify.py reads back and checks against raw V7: one group
per drawn step (data-link, from, to, sign, grade, delay, type), the line path with its texture, the sign glyph,
one group per station, the loop bullets, and data-red on each red mark.
"""
import html
import math

import maps_r2_c_geom as G

esc = html.escape
M, LOOPS = G.M, G.LOOPS

# locked palette (Master Brief section 3)
CHARCOAL, NEWS, WHITE, RED, PRUSSIAN, STONE = "#121212", "#DCD9D2", "#FFFFFF", "#E63946", "#1F2D5A", "#5D636D"
DEEP = "#4E535B"           # derived secondary text on Newsprint and White (round one, maps_draw.py)
MINUS = "−"
FONT_UI = "Inter, 'Helvetica Neue', Arial, sans-serif"
FONT_DISPLAY = "'Inter Tight', Inter, 'Helvetica Neue', Arial, sans-serif"
FONT_QUOTE = "Lora, Georgia, serif"
STYLE = (f"<style>.t{{font-family:{FONT_UI}}}.d{{font-family:{FONT_DISPLAY};font-weight:800;letter-spacing:-0.01em}}"
         f".q{{font-family:{FONT_QUOTE};font-style:italic}}.b{{font-weight:700}}.s{{font-weight:600}}</style>")

# Gate 1 mark M1, V7's line code. Dash lengths scale with line weight (code written for a 2 px line).
M1 = {"documented": "solid", "well-supported": "solid", "plausible": "9 4", "plausible_contested": "9 3 2 3",
      "hypothesis": "2 4"}
GRADE_WORD = {"documented": "Documented", "well-supported": "Well supported", "plausible": "Plausible",
              "plausible_contested": "Contested", "hypothesis": "Hypothesis"}
GRADE_GLOSS = MM_GLOSS = G.MM.GRADE_GLOSS
DELAY_WORD = G.MM.DELAY_WORD
TICKS = {"S": 1, "M": 2, "L": 3}


def dash_for(grade, weight):
    code = M1[grade]
    if code == "solid":
        return None, "solid"
    k = weight / 2.0
    return " ".join(f"{float(x) * k:g}" for x in code.split()), code


def sign_glyph(p):
    return "+" if p == "+" else (MINUS if p == "-" else "")


def text_w(s, size=15, weight=600, display=False):
    """Approximate advance width of Inter, for layout. The browser check measures the real widths."""
    narrow = sum(1 for ch in s if ch in "il.,:;'|()![] fjtI1")
    wide = sum(1 for ch in s if ch in "MWmw")
    caps = sum(1 for ch in s if ch.isupper() and ch not in "IMW")
    per = 0.55 if weight < 600 else 0.58
    if display:
        per = 0.56
    return size * (per * (len(s) - narrow - wide - caps) + 0.29 * narrow + 0.86 * wide + 0.68 * caps)


def wrap2(s, size=15, weight=600):
    """Split a name into two balanced lines."""
    words = s.split()
    if len(words) < 2:
        return [s]
    best, bw = None, 1e9
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        w = max(text_w(a, size, weight), text_w(b, size, weight))
        if w < bw:
            best, bw = [a, b], w
    return best


def wrap_to(s, width, size=13, weight=400):
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


def T(x, y, s, size=15, weight=600, fill=WHITE, anchor="start", cls="t", extra=""):
    w = " b" if weight >= 700 and cls == "t" else (" s" if weight >= 600 and cls == "t" else "")
    a = f' text-anchor="{anchor}"' if anchor != "start" else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}{w}" font-size="{size}" fill="{fill}"{a}{extra}>{esc(s)}</text>'


def svg_doc(w, h, body, label, view, bg, extra="", desc=None):
    d = f"<desc>{esc(desc)}</desc>" if desc else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" viewBox="0 0 {w:.0f} {h:.0f}" '
            f'role="img" aria-label="{esc(label)}" data-view="{esc(view)}"{extra}><title>{esc(label)}</title>{d}{STYLE}'
            f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>{body}</svg>')


# ------------------------------------------------------------------ the two kind glyphs (shared with Direction B)

def kind_glyph(cx, cy, kind, size=16, ink=NEWS, width=2.0):
    """Reinforcing: one turn of a spiral that ends one lap further out. Balancing: a ring that closes on itself.
    Ink only, never red; the words "feeds itself" and "pushes back" print beside it in every key."""
    r = size / 2 - width
    if kind == "B":
        return (f'<g class="kind" data-kind="B"><circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r * 0.78:.2f}" fill="none" '
                f'stroke="{ink}" stroke-width="{width}"/></g>')
    pts = []
    for i in range(61):
        t = i / 60
        a = -math.pi / 2 + 2 * math.pi * t
        rr = r * (0.42 + 0.58 * t)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d = "M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts)
    return f'<g class="kind" data-kind="R"><path d="{d}" fill="none" stroke="{ink}" stroke-width="{width}" stroke-linecap="round"/></g>'


# ------------------------------------------------------------------ typed chip (Gate 1 mark M3)

def chip(x, y, kind_word, code, ink, ground, h=26, extra="", glyph=None):
    """Two-part chip: the type word in an ink cell, the code in an outlined cell, 13 and 14 px. Returns (svg, width)."""
    w1 = text_w(kind_word, 13, 600) + 14
    w2 = text_w(code, 14, 700) + 14 + (20 if glyph else 0)
    out = [f'<rect x="{x:.1f}" y="{y:.1f}" width="{w1:.1f}" height="{h}" fill="{ink}"/>',
           T(x + w1 / 2, y + h / 2 + 4.6, kind_word, 13, 600, ground, "middle"),
           f'<rect x="{x + w1:.1f}" y="{y + 0.75:.1f}" width="{w2 - 0.75:.1f}" height="{h - 1.5}" fill="{ground}" stroke="{ink}" stroke-width="1.5"/>',
           T(x + w1 + 7 + text_w(code, 14, 700) / 2, y + h / 2 + 5, code, 14, 700, ink, "middle")]
    if glyph:
        out.append(kind_glyph(x + w1 + w2 - 15, y + h / 2, glyph, 15, ink, 1.8))
    return f'<g class="chip"{extra}>' + "".join(out) + "</g>", w1 + w2


# ------------------------------------------------------------------ the network drawing

class Theme:
    def __init__(self, name):
        self.name = name
        if name == "prussian":
            self.bg, self.line, self.ring, self.fill, self.id, self.label, self.tag, self.tagtext = PRUSSIAN, NEWS, WHITE, PRUSSIAN, WHITE, WHITE, NEWS, PRUSSIAN
            self.dim = None
        elif name == "newsprint":
            self.bg, self.line, self.ring, self.fill, self.id, self.label, self.tag, self.tagtext = NEWS, STONE, STONE, NEWS, CHARCOAL, CHARCOAL, STONE, WHITE
            self.dim = True
        elif name == "white":
            self.bg, self.line, self.ring, self.fill, self.id, self.label, self.tag, self.tagtext = WHITE, CHARCOAL, CHARCOAL, WHITE, CHARCOAL, CHARCOAL, CHARCOAL, WHITE
            self.dim = None
        elif name == "white-card":
            self.bg, self.line, self.ring, self.fill, self.id, self.label, self.tag, self.tagtext = WHITE, CHARCOAL, CHARCOAL, WHITE, CHARCOAL, CHARCOAL, CHARCOAL, WHITE
            self.dim = None


LINE_W = 4.0
RING_R = 12.0
CAP_W = 42.0


def step_attrs(link_id):
    l = M["links"][link_id]
    a = {"data-link": link_id, "data-from": l["from"], "data-to": l["to"], "data-sign": l["polarity"] or "none",
         "data-grade": l["evidence"], "data-delay": l["delay"], "data-type": l["type"]}
    return "".join(f' {k}="{esc(v)}"' for k, v in a.items())


def station_shape(L, sid, theme, red=False, lit=True, scale=1.0, inside_name=True, show_id=True, filled=False):
    """One station: an open ring for a variable on one loop, an open capsule for a variable several loops share.
    A station on five or more loops holds its name inside the capsule."""
    x, y = L.station_px(sid)
    loops = G.station_loops(sid)
    ring = theme.ring if lit else STONE
    idc = theme.id if lit else (DEEP if theme.name in ("newsprint", "white") else theme.id)
    fill = theme.fill
    sw = 2.5
    if filled:
        # a station on a lit loop: Charcoal filled, its ID in Newsprint
        ring, fill, idc = CHARCOAL, CHARCOAL, NEWS
    out = []
    kind = "ring" if len(loops) == 1 else "capsule"
    named = inside_name and len(loops) >= 5
    if red:
        ring = RED
        sw = 3.5
    if named:
        name = M["nodes"][sid]["short"]
        lines = wrap2(name, 15, 600)
        w = max(text_w(l, 15, 600) for l in lines) + 26
        h = 22 + 19 * len(lines) + 8
        out.append(f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="16" fill="{fill}" stroke="{ring}" stroke-width="{sw}"/>')
        out.append(T(x, y - h / 2 + 22, sid, 13, 700, (NEWS if (filled or theme.name == "prussian") else idc), "middle"))
        for i, ln in enumerate(lines):
            out.append(T(x, y - h / 2 + 22 + 19 * (i + 1), ln, 15, 600, (NEWS if filled else (theme.label if lit else idc)), "middle"))
        kind = "hub"
        box = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    elif kind == "ring":
        r = RING_R * scale
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{ring}" stroke-width="{sw}"/>')
        if show_id:
            out.append(T(x, y + 4.6, sid, 13, 700, idc, "middle"))
        box = (x - r, y - r, x + r, y + r)
    else:
        w, h = CAP_W * scale, 2 * RING_R * scale
        out.append(f'<rect x="{x - w / 2:.1f}" y="{y - h / 2:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{h / 2:.1f}" fill="{fill}" stroke="{ring}" stroke-width="{sw}"/>')
        if show_id:
            out.append(T(x, y + 4.6, sid, 13, 700, idc, "middle"))
        box = (x - w / 2, y - h / 2, x + w / 2, y + h / 2)
    lab = M["nodes"][sid]["short"]
    red_attr = ' data-red="1"' if red else ""
    g = (f'<g class="var" data-node="{sid}" data-label="{esc(lab)}" data-kind="{kind}" data-loops="{" ".join(loops)}"{red_attr}>'
         + "".join(out) + "</g>")
    return g, box


def station_label(L, sid, theme, box, lit=True, size=15):
    """The station's everyday V7 name beside its marker, on the side the station table names."""
    t = L.table[sid]
    side = t["label"]
    if side == "inside":
        return "", None
    name = M["nodes"][sid]["short"]
    lines = wrap2(name, size, 600) if t["wrap"] else [name]
    x, y = L.station_px(sid)
    x0, y0, x1, y1 = box
    gap = 7
    lh = size * 1.22
    hgt = lh * len(lines)
    wid = max(text_w(l, size, 600) for l in lines)
    dx, dy = t["dx"], t["dy"]
    if side == "e":
        ax, anchor, ty = x1 + gap, "start", y - hgt / 2 + size * 0.8
    elif side == "w":
        ax, anchor, ty = x0 - gap, "end", y - hgt / 2 + size * 0.8
    elif side == "n":
        ax, anchor, ty = x, "middle", y0 - gap - hgt + size * 0.8
    elif side == "s":
        ax, anchor, ty = x, "middle", y1 + gap + size * 0.8
    elif side == "ne":
        ax, anchor, ty = x1 - 2, "start", y0 - gap - hgt + size * 0.8
    elif side == "nw":
        ax, anchor, ty = x0 + 2, "end", y0 - gap - hgt + size * 0.8
    elif side == "se":
        ax, anchor, ty = x1 - 2, "start", y1 + gap + size * 0.8
    else:  # sw
        ax, anchor, ty = x0 + 2, "end", y1 + gap + size * 0.8
    ax += dx
    ty += dy
    fill = theme.label if lit else (DEEP if theme.name in ("newsprint", "white") else theme.label)
    out = "".join(T(ax, ty + i * lh, ln, size, 600, fill, anchor) for i, ln in enumerate(lines))
    if anchor == "start":
        bx = (ax, ty - size * 0.8, ax + wid, ty - size * 0.8 + hgt)
    elif anchor == "end":
        bx = (ax - wid, ty - size * 0.8, ax, ty - size * 0.8 + hgt)
    else:
        bx = (ax - wid / 2, ty - size * 0.8, ax + wid / 2, ty - size * 0.8 + hgt)
    return f'<g class="label" data-for="{sid}">{out}</g>', bx


def sign_tag(p, u, sign, theme, bundle_w=0.0, lit=True, extra="", strong=False):
    """The sign of one connection, at the middle of its run, in a tag that points the way the step runs."""
    hw = max(7.0, bundle_w / 2 + 4)
    L0, L1 = 9.0, 5.5
    nx, ny = -u[1], u[0]
    cx, cy = p
    back = (cx - u[0] * L0, cy - u[1] * L0)
    front = (cx + u[0] * L0, cy + u[1] * L0)
    tip = (cx + u[0] * (L0 + L1), cy + u[1] * (L0 + L1))
    pts = [(back[0] + nx * hw, back[1] + ny * hw), (front[0] + nx * hw, front[1] + ny * hw), tip,
           (front[0] - nx * hw, front[1] - ny * hw), (back[0] - nx * hw, back[1] - ny * hw)]
    fill = theme.tag if lit else STONE
    tc = theme.tagtext if lit else WHITE
    if strong:
        fill, tc = CHARCOAL, NEWS
    poly = " ".join(f"{a:.1f},{b:.1f}" for a, b in pts)
    g = sign_glyph(sign)
    return (f'<g class="sign"{extra}><polygon points="{poly}" fill="{fill}" stroke="{fill}" stroke-width="2" stroke-linejoin="round"/>'
            f'{T(cx, cy + 4.6, g, 13, 700, tc, "middle", extra=" data-sign-glyph=\"1\"")}</g>')


LIT_W, DIM_W = 6.0, 2.0


def network(L, theme, lit_loop=None, reform=None, show_labels=True, show_signs=True, show_bullets=True,
            bullets=None, line_w=LINE_W, show_ids=True, ghost=False, station_scale=1.0, hub_names=True,
            glyph_bullets=False, lit_w=None, dim_w=None, avoid=(), tag_shift=None):
    """Draw every numbered loop line, its stations and signs. Returns (svg, boxes) where boxes lists label and
    station boxes for the collision check."""
    reform_targets = set(M["reforms"][reform]["targets"]) if reform else set()
    lit = None if lit_loop is None else ({lit_loop} if isinstance(lit_loop, str) else set(lit_loop))
    # a lit view: lit loops at 6 px Charcoal (red where the named reform acts), every other loop at 2 px Stone
    lit_w = LIT_W * line_w / LINE_W if lit_w is None else lit_w
    dim_w = DIM_W * line_w / LINE_W if dim_w is None else dim_w
    lines, tags, stations, labels, boxes, bullet_svgs, tag_boxes = [], [], [], [], [], [], []
    for (a, b), trs in L.tracks.items():
        base = L.corridor_px(a, b)
        n = len(trs)
        bundle_w = (n - 1) * L.pitch + line_w
        by_link = {}
        for t in trs:
            by_link.setdefault(t["link"], []).append(t)
        links_here = list(by_link)
        for li, (link, group) in enumerate(by_link.items()):
            l = M["links"][link]
            for t in group:
                pts = G.offset_poly(base, t["offset"])
                if l["from"] != a:
                    pts = list(reversed(pts))
                    off = -t["offset"]
                else:
                    off = t["offset"]
                d, _ = G.rounded_path(pts, L.radius, off)
                on = (lit is None) or (t["loop"] in lit)
                red = link in reform_targets
                w = line_w if lit is None else (lit_w if on else dim_w)
                dash, code = dash_for(l["evidence"], w)
                col = RED if red else (theme.line if on else STONE)
                if lit is not None and on and not red:
                    col = CHARCOAL
                da = f' stroke-dasharray="{dash}"' if dash else ""
                ra = ' data-red="1"' if red else ""
                lit_attr = (' data-lit="1"' if on else ' data-lit="0"') if lit is not None else ""
                lines.append((0 if not on else (2 if red else 1),
                              f'<g class="step" data-loop="{t["loop"]}"{step_attrs(link)}{lit_attr}><path d="{d}" fill="none" stroke="{col}" '
                              f'stroke-width="{w}"{da} data-texture="{code}" data-weight="{w}"{ra}/></g>'))
            if show_signs:
                # one sign per connection: across its bundle when several loops ride it
                pts = base if l["from"] == a else list(reversed(base))
                Lp = G.plen(pts)
                runs = G.straight_runs(pts)
                longest = max(runs, key=lambda r: r[2])
                s0 = sum(r[2] for r in runs[:runs.index(longest)])
                mid_s = s0 + longest[2] / 2
                if len(links_here) == 2:
                    # the two directions of a two-step loop: tags 48 px apart about the middle, each on its own track
                    shift = 24.0 if li == 0 else -24.0
                    if l["from"] != a:
                        shift = -shift
                    sp = mid_s + shift
                else:
                    sp = mid_s
                # a tag slides along its run where the layout gives it a shift, to leave its loop's bullet room
                sp += (tag_shift or {}).get(link, 0.0)
                p, u = G.point_at(pts, sp)
                offs = [t["offset"] if l["from"] == a else -t["offset"] for t in group]
                mo = sum(offs) / len(offs)
                nx, ny = -u[1], u[0]
                p = (p[0] + nx * mo, p[1] + ny * mo)
                on = (lit is None) or any(t["loop"] in lit for t in group)
                bw = (len(group) - 1) * L.pitch + (line_w if lit is None else (lit_w if on else dim_w))
                tags.append((1 if on else 0, sign_tag(p, u, l["polarity"], theme, bw, lit=on, strong=(lit is not None and on),
                                                     extra=f' data-for="{link}" data-sign="{l["polarity"]}"')))
                hw = max(7.0, bw / 2 + 4) + 2
                ext = 16
                tag_boxes.append((p[0] - ext, p[1] - ext, p[0] + ext, p[1] + ext) if abs(u[0]) > 0.3 and abs(u[1]) > 0.3 else
                                 (p[0] - (ext if abs(u[0]) > 0.5 else hw), p[1] - (ext if abs(u[1]) > 0.5 else hw),
                                  p[0] + (ext if abs(u[0]) > 0.5 else hw), p[1] + (ext if abs(u[1]) > 0.5 else hw)))
    for sid in G.STATIONS:
        on = (lit is None) or bool(lit & set(G.station_loops(sid)))
        red = sid in reform_targets
        g, box = station_shape(L, sid, theme, red=red, lit=on, show_id=show_ids, scale=station_scale, inside_name=hub_names,
                               filled=(lit is not None and on))
        stations.append((1 if on else 0, g))
        boxes.append(("station", sid, box))
        if show_labels:
            lg, lb = station_label(L, sid, theme, box, lit=on)
            if lg:
                labels.append(lg)
                boxes.append(("label", sid, lb))
    if show_bullets:
        placed = place_bullets(L, boxes, tag_boxes, glyph=glyph_bullets, avoid=avoid)
        for lid in G.NUMBERED:
            (cx, cy), score, corr, leader = placed[lid]
            on = (lit is None) or (lid in lit)
            ink = theme.line if on else STONE
            if lit is not None and on:
                ink = CHARCOAL
            first = LOOPS[lid]["stations"][0]["code"]
            bullet_svgs.append((1 if on else 0, bullet_svg(cx, cy, lid, ink, theme.bg, glyph=glyph_bullets, leader=leader,
                                                           extra=f' data-first="{first}" data-on="{corr}" data-score="{score:.0f}"',
                                                           text_ink=(DEEP if not on else None))))
            w, h = bullet_size(lid, glyph_bullets)
            boxes.append(("bullet", lid, (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)))
    body = ("".join(s for _, s in sorted(lines, key=lambda x: x[0]))
            + "".join(s for _, s in sorted(tags, key=lambda x: x[0]))
            + "".join(s for _, s in sorted(stations, key=lambda x: x[0]))
            + "".join(labels) + "".join(s for _, s in sorted(bullet_svgs, key=lambda x: x[0])))
    for b in tag_boxes:
        boxes.append(("sign", "", b))
    return body, boxes


BULLET_H = 22.0
GLYPH_CELL = 20.0     # the ink cell that carries the kind glyph on the print poster: about 12 px drawn, 29 px printed


def bullet_size(lid, glyph=False):
    return (GLYPH_CELL if glyph else 0) + text_w(lid, 14, 700) + 14, BULLET_H


def bullet_svg(cx, cy, lid, ink, ground, extra="", text_ink=None, glyph=False, leader=None):
    """The loop's line bullet, set on its own track: the typed chip (M3) in its bullet form. On screen it is the
    outlined code cell alone, because the kind glyph would draw at about 12 px and read as a numeral; the ID's R or B
    carries the kind. Where the bullet prints at 24 px or more (the poster PDF), the ink cell carries the kind glyph.
    Where no stretch of its own track has room, the bullet sits beside it on a 1 px leader."""
    w, h = bullet_size(lid, glyph)
    x, y = cx - w / 2, cy - h / 2
    kind = LOOPS[lid]["type"]
    out = []
    if leader:
        (x0, y0), (x1, y1) = leader
        out.append(f'<path class="leader" d="M{x0:.1f} {y0:.1f} L{x1:.1f} {y1:.1f}" stroke="{ink}" stroke-width="1" fill="none"/>')
        extra += f' data-leader="{x0:.1f} {y0:.1f} {x1:.1f} {y1:.1f}"'
    g0 = 0
    if glyph:
        out += [f'<rect x="{x:.1f}" y="{y:.1f}" width="{GLYPH_CELL:.0f}" height="{h}" fill="{ink}"/>',
                kind_glyph(x + GLYPH_CELL / 2, y + h / 2, kind, 16, ground, 1.8)]
        g0 = GLYPH_CELL
    out += [f'<rect x="{x + g0 + 0.75:.1f}" y="{y + 0.75:.1f}" width="{w - g0 - 1.5:.1f}" height="{h - 1.5}" fill="{ground}" stroke="{ink}" stroke-width="1.5"/>',
            T(x + g0 + (w - g0) / 2, y + h / 2 + 5, lid, 14, 700, text_ink or ink, "middle")]
    return (f'<g class="bullet" data-bullet="{lid}" data-kind="{kind}" data-cx="{cx:.1f}" data-cy="{cy:.1f}"{extra}>'
            + "".join(out) + "</g>")


def own_corridors(L, lid):
    """The corridors only this loop rides (every track in them is the loop's)."""
    return [(a, b) for (a, b), trs in L.tracks.items() if all(t["loop"] == lid for t in trs)]


def _box_entry(q0, c, box):
    """Where the segment from q0 (outside the box) to c (its centre) enters the box."""
    t_in = 0.0
    for k in (0, 1):
        d = c[k] - q0[k]
        if abs(d) < 1e-9:
            continue
        lo, hi = (box[0], box[2]) if k == 0 else (box[1], box[3])
        t1, t2 = (lo - q0[k]) / d, (hi - q0[k]) / d
        t_in = max(t_in, min(t1, t2))
    return (q0[0] + (c[0] - q0[0]) * t_in, q0[1] + (c[1] - q0[1]) * t_in)


def bullet_candidates(L, lid, glyph=False):
    """Places for a loop's bullet, as (centre, preference, corridor, leader). First choice: on a corridor only this
    loop rides, centred on its track or tracks, on the straight part of a run, nearest the loop's first station.
    Second choice: beside such a corridor, joined to its track by a 1 px leader."""
    first = LOOPS[lid]["stations"][0]["code"]
    w, h = bullet_size(lid, glyph)
    out = []
    for (a, b) in own_corridors(L, lid):
        base = L.corridor_px(a, b)
        if first == b:
            base = list(reversed(base))
        touches = first in (a, b)
        trs = L.tracks[(a, b)]
        hw_c = ((len(trs) - 1) * L.pitch + LINE_W) / 2
        acc = 0.0
        for (p0, p1, ln) in G.straight_runs(base):
            for f in (0.2, 0.25, 0.28, 0.32, 0.36, 0.38, 0.4, 0.6, 0.62, 0.64, 0.68, 0.72, 0.75, 0.8, 0.5, 0.44, 0.56):
                s_ = acc + ln * f
                p, u = G.point_at(base, s_)
                # on the track: the bullet must sit on the straight part of the run, clear of the corner arcs
                ext = abs(u[0]) * w / 2 + abs(u[1]) * h / 2
                if min(f, 1 - f) * ln >= ext + 6:
                    out.append((p, (0 if touches else 40) + s_ / 40, f"{a}-{b}", None))
                # beside the track on a leader: square to the run, or level or plumb from a diagonal run
                n = (-u[1], u[0])
                dirs = [n, (-n[0], -n[1])]
                if abs(u[0]) > 0.3 and abs(u[1]) > 0.3:
                    dirs += [(1, 0), (-1, 0), (0, 1), (0, -1)]
                for dvec in dirs:
                    # distance along dvec from the centreline to the outer edge of the bundle
                    cross = abs(dvec[0] * n[0] + dvec[1] * n[1])
                    edge = hw_c / max(cross, 0.3)
                    ext_d = abs(dvec[0]) * w / 2 + abs(dvec[1]) * h / 2
                    for gap in (9, 16, 26, 38):
                        q0 = (p[0] + dvec[0] * edge, p[1] + dvec[1] * edge)
                        c = (p[0] + dvec[0] * (edge + gap + ext_d), p[1] + dvec[1] * (edge + gap + ext_d))
                        box = (c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2)
                        q1 = _box_entry(q0, c, box)
                        bend = 0 if dvec in (n, (-n[0], -n[1])) else 15
                        out.append((c, 150 + gap + bend + (0 if touches else 20) + s_ / 40, f"{a}-{b}", (q0, q1)))
            acc += ln
    return out


def _seg_hits_box(p, q, bx, pad=2.0):
    n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 2))
    for i in range(n + 1):
        t = i / n
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if bx[0] - pad <= x <= bx[2] + pad and bx[1] - pad <= y <= bx[3] + pad:
            return True
    return False


def _seg_near_seg(p, q, a, b, d):
    n = max(2, int(math.hypot(q[0] - p[0], q[1] - p[1]) / 2))
    for i in range(1, n + 1):
        t = i / n
        x, y = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        dx, dy = b[0] - a[0], b[1] - a[1]
        L2 = dx * dx + dy * dy
        tt = max(0, min(1, ((x - a[0]) * dx + (y - a[1]) * dy) / L2)) if L2 else 0
        if math.hypot(x - a[0] - tt * dx, y - a[1] - tt * dy) < d:
            return True
    return False


def place_bullets(L, boxes, tag_boxes, glyph=False, avoid=()):
    """Choose each bullet's place by a collision score against stations, names, sign tags, other corridors, the
    view's fixed text and the bullets already placed. Returns {loop: (centre, score, corridor, leader)}."""
    chosen = {}
    stations_first = [b for k, _, b in boxes if k == "station"]
    n_station = len(stations_first)
    n_label = n_station + len([1 for k, _, b in boxes if k != "station"])
    n_tag = n_label + len(tag_boxes)
    occupied = stations_first + [b for k, _, b in boxes if k != "station"] + list(tag_boxes) + list(avoid)
    segs = []
    for (a, c), trs in L.tracks.items():
        hw = ((len(trs) - 1) * L.pitch + LINE_W) / 2 + 3
        pts = L.corridor_px(a, c)
        for i in range(len(pts) - 1):
            segs.append((f"{a}-{c}", pts[i], pts[i + 1], hw))
    for lid in G.NUMBERED:
        w, h = bullet_size(lid, glyph)
        best = None
        for (cx, cy), pref, corr, leader in bullet_candidates(L, lid, glyph):
            bx = (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)
            score = pref
            for (name, p, q, hw) in segs:
                if name == corr and leader is None:
                    continue
                if _seg_box(p, q, (bx[0] - hw, bx[1] - hw, bx[2] + hw, bx[3] + hw)):
                    score += 1000
                if leader is not None and name != corr and _seg_near_seg(leader[0], leader[1], p, q, hw):
                    score += 1000
            for i_ob, ob in enumerate(occupied):
                # stations get a wider berth, so a bullet never reads as a name; sign tags a little more than text
                m = 7 if i_ob < n_station else (5 if n_label <= i_ob < n_tag else 3)
                if bx[0] < ob[2] + m and ob[0] < bx[2] + m and bx[1] < ob[3] + m and ob[1] < bx[3] + m:
                    score += 1000
                if leader is not None and _seg_hits_box(leader[0], leader[1], ob):
                    score += 1000
            if best is None or score < best[1]:
                best = ((cx, cy), score, corr, leader)
        chosen[lid] = best
        occupied.append((best[0][0] - w / 2, best[0][1] - h / 2, best[0][0] + w / 2, best[0][1] + h / 2))
    return chosen


def _inside(pt, poly):
    x, y = pt
    c = False
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


def overlaps(boxes, pad=2):
    """Label, station and bullet boxes that touch each other (for the 2x review)."""
    bad = []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            (k1, n1, a), (k2, n2, b) = boxes[i], boxes[j]
            if {k1, k2} <= {"station", "sign"}:
                continue
            if n1 == n2 and {k1, k2} == {"station", "label"}:
                continue
            if a[0] < b[2] + pad and b[0] < a[2] + pad and a[1] < b[3] + pad and b[1] < a[3] + pad:
                bad.append((k1, n1, k2, n2))
    return bad


def box_hits_lines(L, boxes, pad=3):
    """Label and bullet boxes that sit on a corridor (approximate: the corridor centerline widened by its bundle)."""
    bad = []
    for kind, name, b in boxes:
        if kind not in ("label", "bullet"):
            continue
        for (a, c), trs in L.tracks.items():
            hw = ((len(trs) - 1) * L.pitch + LINE_W) / 2 + pad
            pts = L.corridor_px(a, c)
            for i in range(len(pts) - 1):
                if _seg_box(pts[i], pts[i + 1], (b[0] - hw, b[1] - hw, b[2] + hw, b[3] + hw)):
                    if kind == "bullet" and name in [t["loop"] for t in trs]:
                        continue
                    bad.append((kind, name, f"{a}-{c}"))
                    break
    return bad


def _seg_box(p, q, b):
    # Liang-Barsky clip test
    x0, y0, x1, y1 = b
    dx, dy = q[0] - p[0], q[1] - p[1]
    t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, p[0] - x0), (dx, x1 - p[0]), (-dy, p[1] - y0), (dy, y1 - p[1])):
        if pp == 0:
            if qq < 0:
                return False
        else:
            t = qq / pp
            if pp < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
            if t0 > t1:
                return False
    return True
