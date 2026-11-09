"""Stage B Civic Line drawings, authored in source space (line 5.5 px).

Every function returns groups for civic_line_stage_b_common.source_svg:
a list of (role, [element]) painted in order. Kept parts of an original
master use that master's own source coordinates (work/build/assets/
civic-line/src/<ID>.svg), so an option marked "Within DR-135" can be
checked part by part against its original.
"""
import math

import civic_line_stage_b_common as C

P = C.Pen


# ------------------------------------------------------------------ shared parts

def ellarc(pen, cx, cy, rx, ry, t0, t1):
    """Arc of the ellipse (cx, cy, rx, ry) from angle t0 to t1 in degrees
    (0 at the right end, 90 at the bottom), as one path."""
    def pt(t):
        r = math.radians(t)
        return (cx + rx * math.cos(r), cy + ry * math.sin(r))
    a, b = pt(t0), pt(t1)
    large = 1 if abs(t1 - t0) > 180 else 0
    sweep = 1 if t1 > t0 else 0
    return pen.path([("M", *a), ("E", rx, ry, 0, large, sweep, *b)])


def seat_rows(pen, cy, rxs, rys, nseg, gap=9.0):
    """Rows of members' desks seen from the gallery: the lower halves of
    ellipses around the rostrum, each split into seat sections by aisles
    that line up toward the rostrum. An odd count keeps a section, never an
    aisle, on the center line, so no row splits into two sides."""
    els = []
    for rx, ry, n in zip(rxs, rys, nseg):
        span = 180.0 / n
        for i in range(n):
            els.append(ellarc(pen, 0, cy, rx, ry, i * span + gap / 2, (i + 1) * span - gap / 2))
    return els


def rostrum(pen, tiers=((34, 14), (22, 14))):
    """The rostrum from the gallery: desk fronts stacked in tiers, each open
    at its foot. Returns (elements, top y)."""
    els, y = [], 0.0
    for half, h in tiers:
        els.append(pen.poly([(-half, y), (-half, y - h), (half, y - h), (half, y)]))
        y -= h
    return els, y


HOUSE_ROWS = dict(cy=-2, rxs=[46, 68, 90], rys=[30, 46, 62], nseg=[5, 5, 5], gap=9)


def chamber_b(pen, tiers=((34, 14), (22, 14))):
    """Set B's Congress sign: the House chamber from the gallery, seats in
    three rows of five sections curving around the rostrum. Origin at the
    rostrum's foot. Returns (rows, rostrum)."""
    rows = seat_rows(pen, **HOUSE_ROWS)
    ros, _ = rostrum(pen, tiers)
    return rows, ros


def chamber_unit(pen, senate=False):
    """One chamber of set C: two rows and a one-tier rostrum. The House has
    three and five sections, the Senate three and three. Origin at the
    rostrum's foot."""
    rows = seat_rows(pen, -2, [44, 66], [38, 58], [3, 3] if senate else [3, 5], gap=10)
    ros, _ = rostrum(pen, ((30, 16),))
    return rows, ros


def chambers_c(pen, k=1.0):
    """Set C's Congress sign: the House (left, larger) and the Senate (right,
    smaller) side by side, both seen from the gallery. Origin between them
    on the rostrums' line. Returns (rows, rostrums)."""
    h_rows, h_ros = chamber_unit(pen.sub(-60 * k, 0, 0.86 * k))
    s_rows, s_ros = chamber_unit(pen.sub(70 * k, 4 * k, 0.64 * k), senate=True)
    return h_rows + s_rows, h_ros + s_ros


def a_block(pen, door=True, windows=True, attic_h=14.7):
    """Set A's Congress sign: CL-025's central block without its dome or
    columns. Origin at the base's center. The dome becomes a flat attic of
    the old dome base's width; the colonnade becomes a plain band between two
    walls at the outer supports; the four facade columns become two windows
    and a center door. Proportions are CL-025's own (axis x 90.7, base
    y 138.56). Returns (black parts, door)."""
    base = [
        pen.poly([(-29.26, -67.86), (-29.26, -67.86 - attic_h), (29.26, -67.86 - attic_h), (29.26, -67.86)]),
        pen.line(-38.25, -67.86, 38.25, -67.86),
        pen.line(-33.69, -67.86, -33.69, -47.56),
        pen.line(33.69, -67.86, 33.69, -47.56),
        pen.poly([(-43.85, 0), (-43.85, -47.56), (43.85, -47.56), (43.85, 0)]),
        pen.line(-47.93, 0, 47.93, 0),
    ]
    if windows:
        base += [pen.rect(-25.44 - 5.5, -31.0, 11, 15), pen.rect(25.44 - 5.5, -31.0, 11, 15)]
    d = [pen.poly([(-8.5, 0), (-8.5, -24.5), (8.5, -24.5), (8.5, 0)])] if door else []
    return base, d


def crate(pen, s=1.0):
    """The family's crate for imports, as CL-064 and CL-036 draw it: a box in
    a three-quarter view with a lid seam. Origin at the front face's
    bottom-left corner; s scales it."""
    q = pen.sub(0, 0, s)
    w, h, d = 34, 30, 12
    return [
        q.poly([(0, 0), (0, -h), (w, -h), (w, 0)], closed=True),
        q.poly([(0, -h), (d, -h - d * 0.8), (w + d, -h - d * 0.8), (w + d, -d * 0.8), (w, 0)]),
        q.line(w, -h, w + d, -h - d * 0.8),
        q.line(w / 2, -h, w / 2 + d, -h - d * 0.8),
        q.line(w / 2, -h, w / 2, -h + 9),
    ]


# ------------------------------------------------------------------ CL-025 Congress

def cl025_a():
    """Within DR-135. Kept at their source coordinates: the upper cornice,
    the facade, both wings and the base. Redrawn: dome, cupola and finial
    become a flat attic on the old dome base's width; the five upper supports
    become the band's two end walls; the four facade columns become two
    windows and a center door, which takes the red from the column; each
    wing's two supports become an end wall and a window."""
    p = P(90.7, 138.56)
    blk, door = a_block(p)
    wings = [
        P().line(10.57, 102.05, 46.85, 102.05), P().line(134.55, 102.05, 170.83, 102.05),
        P().line(15.52, 102.05, 15.52, 138.1), P().line(165.88, 102.05, 165.88, 138.1),
        P().rect(31.17 - 5.5, 113.0, 11, 15), P().rect(150.23 - 5.5, 113.0, 11, 15),
    ]
    return [("base", blk + wings), ("accent", door)]


def cl025_b():
    """Outside DR-135. The House chamber from the gallery: three rows of
    seats in five sections curving around the rostrum, red on the rostrum."""
    rows, ros = chamber_b(P(100, 60))
    return [("base", rows), ("accent", ros)]


def cl025_c():
    """Outside DR-135. The two chambers, the House larger and the Senate
    smaller, each seen from the gallery, red on both rostrums: one job, the
    place each chamber is led from."""
    rows, ros = chambers_c(P(140, 60))
    return [("base", rows), ("accent", ros)]


# ------------------------------------------------------------------ CL-014 Entrenched Power

def cl014_fence(lower_break=True, front=True):
    """CL-014's fence at its source coordinates (axis x 100.85). front=False
    leaves out the inner two pairs of front pickets, which would cross a low
    chamber's rows."""
    p = P()
    els = [
        p.poly([(10.75, 124.93), (10.75, 85.5), (12.06, 81.66)]),
        p.poly([(190.95, 124.93), (190.95, 85.5), (189.64, 81.66)]),
        p.path([("M", 12.53, 88.4), ("E", 88.32, 21.14, 0, 0, 1, 54.74, 70.37)]),
        p.path([("M", 146.96, 70.37), ("E", 88.32, 21.14, 0, 0, 1, 189.17, 88.4)]),
    ]
    if lower_break:
        els += [p.path([("M", 15.18, 93.5), ("E", 85.9, 23.66, 0, 0, 0, 77.99, 114.58)]),
                p.path([("M", 123.71, 114.58), ("E", 85.9, 23.66, 0, 0, 0, 186.52, 93.5)])]
    else:
        els += [p.path([("M", 15.18, 93.5), ("E", 85.9, 23.66, 0, 0, 0, 186.52, 93.5)])]
    pickets = [(27.85, 71.8, 87.56), (45.36, 65.9, 93.06), (26.17, 97.0, 134.07), (43.69, 101.94, 139.81)]
    if front:
        pickets += [(62.04, 106.0, 143.2), (77.99, 100.5, 143.37)]
    for x1, y1, y2 in pickets:
        x2 = 201.7 - x1
        els += [p.line(x1, y1, x1, y2), p.line(x2, y1, x2, y2)]
    return els


def cl014_a():
    """Within DR-135. Kept at their source coordinates: the fence, its posts
    and pickets, the cornice band, the facade and the red door. Redrawn: the
    spire, cupola and dome become set A's flat attic; the six columns become
    the band's two end walls at the outer pair."""
    p = P()
    attic = p.poly([(73.16, 54.25), (73.16, 40.5), (128.54, 40.5), (128.54, 54.25)])
    building = [
        attic,
        p.path([("M", 68.25, 63.8), ("L", 68.25, 58), ("A", 3.75, 0, 1, 72, 54.25), ("L", 129.7, 54.25),
                ("A", 3.75, 0, 1, 133.45, 58), ("L", 133.45, 63.8)]),
        p.line(66.35, 63.8, 135.35, 63.8),
        p.line(70.25, 63.8, 70.25, 83.88), p.line(131.45, 63.8, 131.45, 83.88),
        p.path([("M", 58.52, 112.36), ("L", 58.52, 83.88), ("L", 143.18, 83.88), ("L", 143.18, 112.36)]),
    ]
    door = [p.rect(90.9, 100.44, 19.9, 41.68, rx=3.8)]
    return [("base", building + cl014_fence()), ("accent", door)]


def cl014_chamber(kind):
    """Outside DR-135. The chamber of the set, without its Congress-only
    feature, standing inside CL-014's whole fence where the building stood;
    red on the rostrum. The chamber sits high enough that the front pickets
    start below its last row, and the front rail runs whole now that the
    door is gone."""
    if kind == "b":
        p = P(100.85, 55, 0.62)
        rows = seat_rows(p, **HOUSE_ROWS)
        ros, _ = rostrum(p, ((34, 14),))
    else:
        p = P(100.85, 52, 0.74)
        rows, ros = chamber_unit(p)
    return [("base", rows + cl014_fence(lower_break=False, front=True)), ("accent", ros)]


def cl014_b():
    return cl014_chamber("b")


def cl014_c():
    return cl014_chamber("c")


# ------------------------------------------------------------------ R-13 Congressional Capacity

def r13_staff_orig():
    p = P()
    return [p.circle(23.79, 89.09, 6.19),
            p.path([("M", 10.85, 115.05), ("L", 10.85, 108.45), ("A", 12.35, 0, 1, 35.55, 108.45), ("L", 35.55, 115.05)]),
            p.circle(56.6, 83.59, 7.85),
            p.path([("M", 44.49, 115.05), ("L", 44.49, 108.45), ("A", 12.35, 0, 1, 69.19, 108.45), ("L", 69.19, 115.05)])]


def r13_book_orig():
    p = P()
    base = [p.path([("M", 164.42, 105.9), ("L", 164.42, 69.55), ("L", 170, 69.55), ("Q", 181.25, 69.55, 194.25, 78),
                    ("Q", 207.25, 69.55, 218.5, 69.55), ("L", 224.08, 69.55), ("L", 224.08, 105.9)]),
            p.line(194.25, 78, 194.25, 103.6),
            p.path([("M", 156.46, 79.75), ("L", 156.46, 115), ("L", 174, 115), ("Q", 182.65, 115, 194.25, 122.1),
                    ("Q", 205.85, 115, 214.5, 115), ("L", 232.04, 115), ("L", 232.04, 79.75)])]
    edge = [p.path([("M", 164.42, 105.9), ("L", 172, 105.9), ("Q", 183.1, 105.9, 194.25, 112.8), ("Q", 205.4, 105.9, 216.5, 105.9),
                    ("L", 224.08, 105.9)])]
    return base, edge


def r13_a():
    """Within DR-135. Kept at their source coordinates: both staff, the
    building's drum walls with their stepped joints, the entablature, the
    walls, the base, and the open book with its red page edge. Redrawn: the
    dome arcs and finial go, so the drum's top line becomes a flat attic (set
    A's sign); the three drum columns go; the three lower columns become
    windows."""
    p = P()
    building = [
        p.line(92.25, 43.92, 137.25, 43.92),
        p.poly([(92.25, 43.92), (92.25, 49.5), (87.33, 49.5), (87.33, 69.58)]),
        p.poly([(137.25, 43.92), (137.25, 49.5), (142.17, 49.5), (142.17, 69.58)]),
        p.line(77.44, 69.58, 152.06, 69.58),
        p.line(81.65, 69.58, 81.65, 103.1), p.line(147.85, 69.58, 147.85, 103.1),
        p.line(81.31, 115.05, 148.19, 115.05),
    ] + [p.rect(x - 5.25, 84.5, 10.5, 14) for x in (97.75, 114.75, 131.75)]
    book, edge = r13_book_orig()
    return [("base", r13_staff_orig() + building + book), ("accent", edge)]


def report(pen):
    """An analyst's report: a page with two lines of text and a rising chart
    line. Origin at the page's bottom-left corner. Returns (page, chart)."""
    w, h = 40, 50
    page = [pen.poly([(0, 0), (0, -h), (w, -h), (w, 0)], closed=True),
            pen.line(8, -h + 10, w - 8, -h + 10), pen.line(8, -h + 19, w - 14, -h + 19)]
    chart = [pen.poly([(8, -9), (16, -18), (23, -13), (32, -26)])]
    return page, chart


def r13_new(sign):
    """Outside DR-135: the set's Congress sign in place of the domed
    building, between two staff figures and an analyst's report, which
    takes the red on its chart line (the book was CL-019 Explain's sign)."""
    p = P()
    staff = C.person(p, 20, 120, k=0.58) + C.person(p, 50, 120, k=0.66)
    if sign == "b":
        rows, ros = chamber_b(p.sub(130, 86, 0.56))
    else:
        rows, ros = chambers_c(p.sub(137, 92, 0.5))
    page, chart = report(p.sub(194, 120))
    return [("base", staff + rows + ros + page), ("accent", chart)]


def r13_b():
    return r13_new("b")


def r13_c():
    return r13_new("c")


# ------------------------------------------------------------------ R-42 Congressional Tariff Votes

def r42_a():
    """Within DR-135. Kept at their source coordinates: the drum, cornice and
    base line of the upper building, the annex with its slot, the ground, the
    ballot box with its red ballot, the L-shaped line, the ribbed box and the
    red arrow. Redrawn: finial, lantern and dome go, so the drum becomes a
    flat attic (set A's sign); the two upper columns become a band under the
    cornice; the three short pillars go; the two lower pillars become
    windows."""
    p = P()
    base = [
        p.line(44.45, 41.08, 91.25, 41.08),
        p.line(45.73, 41.08, 45.73, 50.54), p.line(89.97, 41.08, 89.97, 50.54),
        p.line(37.73, 50.54, 97.97, 50.54),
        p.poly([(42.72, 50.54), (42.72, 60.3), (92.98, 60.3), (92.98, 50.54)]),
        p.line(35.4, 68.16, 98.8, 68.16),
        p.poly([(11.87, 76.73), (37.56, 76.73), (37.56, 113.17)]),
        p.line(13.67, 76.73, 13.67, 113.17),
        p.line(25.6, 88.63, 25.6, 101.25),
        p.rect(52.76 - 5, 84.5, 10, 14), p.rect(67.72 - 5, 84.5, 10, 14),
        p.line(10.5, 113.17, 76.75, 113.17),
        p.path([("M", 92.84, 77.2), ("L", 86.23, 89.19), ("L", 86.23, 120.3), ("A", 3.5, 0, 0, 89.73, 123.8),
                ("L", 132.4, 123.8), ("A", 3.5, 0, 0, 135.9, 120.3), ("L", 135.9, 89.19), ("L", 129.29, 77.2)]),
        p.line(86.23, 89.19, 135.9, 89.19),
        p.poly([(162.94, 103.25), (162.94, 58.5), (213, 58.5)]),
        p.line(147.5, 94.56, 167.87, 94.56),
        p.rect(177.93, 78.47, 59.19, 37.53),
    ] + [p.line(x, 78.47, x, 116) for x in (189.77, 201.61, 213.44, 225.28)] + [p.line(207.7, 70, 207.7, 78.47)]
    acc = [p.poly([(101.78, 79.8), (117.5, 61.06), (126.31, 68.45), (116.79, 79.8)], closed=True),
           p.line(211.12, 58.5, 237.4, 58.5, cls="butt"),
           p.poly([(228.6, 49.7), (237.4, 58.5), (228.6, 67.3)])]
    return [("base", base), ("accent", acc)]


def parcel(pen):
    """CL-064's parcel, at its proportions: front face, top, side and tape.
    Origin at the front face's bottom-left corner."""
    return [pen.rect(0, -53.13, 57.37, 53.13),
            pen.poly([(0, -53.13), (15.89, -68.13), (73.26, -68.13), (57.37, -53.13)]),
            pen.poly([(73.26, -68.13), (73.26, -15.0), (57.37, 0)]),
            pen.poly([(44.72, -68.13), (28.83, -53.13), (28.83, -35.18)])]


def vote_card(pen):
    """A recorded vote: a card with a yes mark over a no mark. Origin at the
    card's bottom-left corner."""
    w, h = 36, 52
    return [pen.rect(0, -h, w, h, rx=3)], [
        pen.poly([(9, -38), (15, -32), (27, -44)]),
        pen.line(11, -20, 25, -6), pen.line(25, -20, 11, -6)]


def r42_new(sign):
    """Outside DR-135: the set's Congress sign, a card holding a recorded
    yes and no in place of the ballot box (a ballot box means a public
    election), and CL-064's parcel for imports with a tag for the tax. The
    red moves from the ballot to the vote card."""
    p = P()
    if sign == "b":
        rows, ros = chamber_b(p.sub(60, 74, 0.56))
    else:
        rows, ros = chambers_c(p.sub(66, 82, 0.5))
    card, marks = vote_card(p.sub(122, 112))
    q = p.sub(172, 112, 0.62)
    goods = parcel(q)
    tag = [q.path([("M", 73.26, -50), ("L", 84, -50), ("L", 92, -42), ("L", 84, -34), ("L", 73.26, -34)]),
           q.circle(83.5, -42, 1.2)]
    return [("base", rows + ros + marks + goods + tag), ("accent", card)]


def r42_b():
    return r42_new("b")


def r42_c():
    return r42_new("c")
