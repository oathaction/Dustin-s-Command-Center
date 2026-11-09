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


# ------------------------------------------------------------------ fix round signs (D2-620)

def rostrum_tiers(pen, halves=(32, 22, 12), th=12):
    """The House rostrum from the gallery: desk fronts stacked in tiers, each
    open at its foot. Returns (black lower tiers, red top tier)."""
    els, y = [], 0.0
    for h in halves:
        els.append(pen.poly([(-h, y), (-h, y - th), (h, y - th), (h, y)]))
        y -= th
    return els[:-1], els[-1:]


def chamber_in_session(pen, tiers=3, far=True, member_k=0.44, angles=(46, 68, 90, 112, 134), red_top=True):
    """Set B, reworked (D2-620): the chamber in session from the gallery.
    Five members sit on the near bench, seen from behind as Civic Line heads
    and shoulders; a far bench in five sections curves round the rostrum
    with no center aisle; the rostrum is about a third of the drawing's width,
    stepped in three tiers, the top tier red. tiers=2 leaves out the
    Speaker's tier, the Congress-only feature, for CL-014. Origin at the
    rostrum's foot. Returns (black, red)."""
    halves = (32, 22, 12)[:tiers]
    low, top = rostrum_tiers(pen, halves)
    far_bench = seat_rows(pen, 4, [50], [20], [5], gap=8) if far else []
    near = [ellarc(pen, 0, 4, 86, 62, 0, 180)]
    members = []
    for t in angles:
        a = math.radians(t)
        members += C.person(pen, 86 * math.cos(a), 4 + 62 * math.sin(a), k=member_k, h=24)
    if not red_top:
        return far_bench + near + members + low + top, []
    return far_bench + near + members + low, top


def members_facing(pen):
    """Set C, redrawn (D2-620): the chamber seen from the rostrum. Members
    face the reader from two curved benches, three on the near bench and five
    on the far one, and the presiding desk stands red in the foreground.
    Origin at the benches' center. Returns (black, red)."""
    def row(rx, ry, t0, t1, angles):
        els = [ellarc(pen, 0, 10, rx, ry, t0, t1)]
        for t in angles:
            a = math.radians(t)
            els += C.person(pen, rx * math.cos(a), 10 + ry * math.sin(a), k=0.46, h=24)
        return els
    black = row(46, 16, 200, 340, (238, 270, 302)) + row(88, 56, 195, 345, (215, 242, 270, 298, 325))
    red = [pen.line(-44, 36, 44, 36), pen.poly([(-38, 50), (-38, 36), (38, 36), (38, 50)])]
    return black, red


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
    """Outside DR-135. The chamber in session from the gallery (D2-620):
    members on the near bench seen from behind, a far bench in five
    sections, and the three-tier rostrum with its top tier red."""
    blk, red = chamber_in_session(P(100, 60))
    return [("base", blk), ("accent", red)]


def cl025_c():
    """Outside DR-135. The chamber from the rostrum (D2-620): members face
    the reader from two curved benches, and the presiding desk stands red in
    the foreground. It replaces the two staggered chambers, which read as two
    signals at 48 px."""
    blk, red = members_facing(P(110, 80))
    return [("base", blk), ("accent", red)]


# ------------------------------------------------------------------ CL-014 Entrenched Power

def cl014_fence(lower_break=True, front=True, pen=None, open_=False):
    """CL-014's fence at its source coordinates (axis x 100.85), through pen
    when given. front=False leaves out the inner two pairs of front pickets;
    open_=True keeps only three pickets a side in front and none behind, so a
    chamber inside reads apart from the fence at 48 px (the review's M4)."""
    p = pen or P()
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
    if open_:
        pickets = [(31.0, 98.6, 135.0), (51.0, 104.0, 141.0), (72.0, 107.6, 143.4)]
    else:
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


def cl014_b():
    """Outside DR-135. Set B's chamber in session, without the Speaker's
    tier, inside the fence; the red moves from the door to the rostrum's top
    tier. Opened for 48 px (the review's M4): three front pickets a side and
    none behind, and the far bench left out, so the fence and the chamber
    read as two things."""
    blk, red = chamber_in_session(P(100.85, 50, 0.62), tiers=2, far=False, member_k=0.66, angles=(62, 90, 118))
    return [("base", blk + cl014_fence(lower_break=False, open_=True)), ("accent", red)]


def ballot(pen, x, y):
    """A ballot paper with its vote marked: a sheet and a check. (x, y) is
    the sheet's bottom-left corner."""
    return [pen.rect(x, y - 32, 26, 32, rx=2), pen.poly([(x + 6, y - 16), (x + 11, y - 10), (x + 20, y - 22)])]


def cl014_c():
    """Outside DR-135, replacing the near-duplicate of B (the review's M3):
    the second idea, that an election cannot move the body. A ballot's arrow
    runs at the fenced chamber and stops at the fence on a red bar, as R-48 C
    stops its arrow at the brace. The rostrum stays black."""
    k = 0.8
    fp = P(52.0, 26.0, k)
    blk, _ = chamber_in_session(P(52.0 + k * 100.85, 26.0 + k * 50, k * 0.62), tiers=2, far=False,
                                member_k=0.66, angles=(62, 90, 118), red_top=False)
    fence = cl014_fence(lower_break=False, open_=True, pen=fp)
    p = P()
    post_x = 52.0 + k * 10.75
    ymid = 26.0 + k * 106
    arrow = ballot(p, 4, ymid + 16) + [p.line(36, ymid, post_x - 12, ymid),
                                         p.poly([(post_x - 19, ymid - 7), (post_x - 12, ymid), (post_x - 19, ymid + 7)])]
    stop = [p.line(post_x - 6, ymid - 10, post_x - 6, ymid + 10)]
    return [("base", blk + fence + arrow), ("accent", stop)]


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
    windows and the middle one a door, as in set A's CL-025."""
    p = P()
    building = [
        p.line(92.25, 43.92, 137.25, 43.92),
        p.poly([(92.25, 43.92), (92.25, 49.5), (87.33, 49.5), (87.33, 69.58)]),
        p.poly([(137.25, 43.92), (137.25, 49.5), (142.17, 49.5), (142.17, 69.58)]),
        p.line(77.44, 69.58, 152.06, 69.58),
        p.line(81.65, 69.58, 81.65, 103.1), p.line(147.85, 69.58, 147.85, 103.1),
        p.line(81.31, 115.05, 148.19, 115.05),
    ] + [p.rect(x - 5.25, 84.5, 10.5, 14) for x in (97.75, 131.75)] + [
        p.poly([(108.25, 115.05), (108.25, 92.5), (121.25, 92.5), (121.25, 115.05)])]
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
    """Outside DR-135: the set's Congress sign above, at three quarters of
    CL-025's size so its rows stay open at 48 px, with two staff figures and
    an analyst's report standing in front of it. The report takes the red on
    its chart line; the open book was CL-019 Explain's sign."""
    p = P()
    if sign == "b":
        rows, ros = chamber_in_session(p.sub(100, 40, 0.74))
    else:
        rows, ros = members_facing(p.sub(100, 58, 0.74))
    staff = C.person(p, 38, 150, k=0.7) + C.person(p, 76, 150, k=0.7)
    page, chart = report(p.sub(130, 150, 1.05))
    return [("base", rows + ros + staff + page), ("accent", chart)]


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
    """Outside DR-135: the set's Congress sign above, at three quarters of
    CL-025's size; below it a card holding a recorded yes and no in place of
    the ballot box (a ballot box means a public election), and CL-064's
    parcel for imports with a tag hung from its corner for the tax. The red
    moves from the ballot to the vote card."""
    p = P()
    if sign == "b":
        rows, ros = chamber_in_session(p.sub(100, 40, 0.74))
    else:
        rows, ros = members_facing(p.sub(100, 58, 0.74))
    card, marks = vote_card(p.sub(42, 154))
    q = p.sub(98, 154, 0.66)
    goods = parcel(q)
    t = p.sub(98 + 0.66 * 73.26, 154 - 0.66 * 68.13)
    tag = [t.line(0, 0, 9, 9),
           t.path([("M", 9, 9), ("L", 22, 9), ("L", 30, 17), ("L", 30, 34), ("L", 14, 34), ("L", 9, 26), ("Z",)]),
           t.circle(19.5, 18, 1.2)]
    return [("base", rows + ros + marks + goods + tag), ("accent", card)]


def r42_b():
    return r42_new("b")


def r42_c():
    return r42_new("c")


# ------------------------------------------------------------------ CL-059 Credit Allocation

def cl059_kept():
    """CL-059's home, factory and red branches at their source coordinates."""
    p = P()
    base = [p.poly([(11.31, 156.5), (11.31, 132.65), (35.98, 112.2), (60.65, 132.65), (60.65, 156.5)]),
            p.poly([(30.17, 156.5), (30.17, 142.4), (41.79, 142.4), (41.79, 156.5)]),
            p.poly([(112.42, 134.1), (127.05, 123.9), (127.05, 134.9), (144.88, 123.9), (144.88, 134.9), (162.7, 123.9),
                    (162.7, 134.9), (165.0, 134.9), (171.2, 112.14), (183.07, 112.14), (183.07, 157.28), (112.42, 157.28)],
                   closed=True)]
    red = [p.path([("M", 87.39, 83.0), ("L", 87.39, 90.93), ("A", 2.5, 0, 1, 84.89, 93.43), ("L", 42.76, 93.43),
                   ("A", 2.5, 0, 0, 40.26, 95.93), ("L", 40.26, 104.8)]),
           p.path([("M", 99.61, 83.0), ("L", 99.61, 90.93), ("A", 2.5, 0, 0, 102.11, 93.43), ("L", 144.24, 93.43),
                   ("A", 2.5, 0, 1, 146.74, 95.93), ("L", 146.74, 112.25)])]
    return base, red


def vault_door(pen, cx, cy, r=11.5, hub=0.0, spokes=(), past=0.0):
    """A bank vault's round door. With a hub, spokes join a hub ring to the
    rim at the given angles; past > 0 runs each spoke that far beyond the rim
    as a handle end, so the wheel reads as a vault's wheel at 48 px and not
    as an X in a circle (the review's S2). Spokes in a plus read as a
    first-aid cross and three read as a fan blade."""
    els = [pen.circle(cx, cy, r)]
    if hub:
        els.append(pen.circle(cx, cy, hub))
        for a in spokes:
            t = math.radians(a)
            els.append(pen.line(cx + hub * math.cos(t), cy - hub * math.sin(t),
                                cx + (r + past) * math.cos(t), cy - (r + past) * math.sin(t)))
    return els


def cl059_a():
    """Within DR-135. Kept at their source coordinates: the pediment, the
    bank's base, the home, the factory and the two red branches. Redrawn: the
    four columns become one wall, its sides at the outer columns, holding a
    round vault door."""
    p = P()
    kept, red = cl059_kept()
    bank = [p.poly([(55.8, 34.67), (93.5, 10.3), (131.2, 34.67)], closed=True),
            p.poly([(64.2, 71.86), (64.2, 45.25), (122.8, 45.25), (122.8, 71.86)]),
            p.line(55.15, 71.86, 131.85, 71.86)] + vault_door(p, 93.5, 58.55, r=8.6)
    return [("base", bank + kept), ("accent", red)]


def cl059_b():
    """Outside DR-135. The pediment goes too: the bank is a flat-roofed block
    with a cornice, a large round vault door on its face and a stepped base.
    Home, factory and red branches kept."""
    p = P()
    kept, red = cl059_kept()
    bank = [p.line(55.15, 22.5, 131.85, 22.5),
            p.poly([(62.2, 71.86), (62.2, 22.5), (124.8, 22.5), (124.8, 71.86)]),
            p.line(55.15, 71.86, 131.85, 71.86)] + vault_door(p, 93.5, 47.2, r=15.0, hub=5.5, spokes=(45, 135, 225, 315), past=6.0)
    return [("base", bank + kept), ("accent", red)]


def cl059_c():
    """Outside DR-135, replacing the safe, a near-duplicate of B (the
    review's M7): the lender and the loan. A small flat-roofed building with a
    door stands beside a loan paper marked with a percent sign for its
    interest, and the two red branches carry the new money out to the home
    and the factory. No columns or pediment (D2-623). Home, factory and
    branches kept."""
    p = P()
    kept, red = cl059_kept()
    lender = [p.line(56.0, 30.0, 96.0, 30.0),
              p.poly([(60.0, 71.86), (60.0, 30.0)]), p.poly([(92.0, 30.0), (92.0, 71.86)]),
              p.poly([(70.0, 71.86), (70.0, 52.0), (82.0, 52.0), (82.0, 71.86)])]
    loan = [p.rect(103.0, 16.0, 28.0, 46.0, rx=2),
            p.circle(110.5, 26.5, 3.4), p.circle(123.5, 41.5, 3.4), p.line(125.0, 24.0, 109.0, 44.0),
            p.line(108.0, 53.5, 126.0, 53.5)]
    base = [p.line(52.0, 71.86, 135.0, 71.86)]
    return [("base", lender + loan + base + kept), ("accent", red)]


# ------------------------------------------------------------------ R-48 Agency Independence

def r48_official_lectern():
    p = P()
    return [p.circle(188.4, 27.47, 9.56),
            p.path([("M", 170.75, 56.55), ("L", 170.75, 47.28), ("A", 4, 0, 1, 174.75, 43.28), ("L", 202.05, 43.28),
                    ("A", 4, 0, 1, 206.05, 47.28), ("L", 206.05, 56.55)]),
            p.poly([(159.5, 56.55), (217.3, 56.55), (214.8, 68.11), (162, 68.11)], closed=True),
            p.line(165.4, 68.11, 165.4, 102.25), p.line(211.4, 68.11, 211.4, 102.25)]


def r48_brace():
    p = P()
    return [p.poly([(122.1, 10.31), (132.4, 10.31), (132.4, 104), (122.1, 104)]),
            p.line(132.4, 57.9, 134.95, 57.9),
            p.circle(144.55, 57.85, 3.4, cls="fill")]


def r48_a():
    """Within DR-135. Kept at their source coordinates: the pediment, the
    entablature band, the stepped base, the red brace with its nub and dot,
    and the official at the lectern. Redrawn: the four bays of columns become
    one wall with a center door and two windows."""
    p = P()
    bldg = [p.poly([(19.6, 38.2), (55.9, 10.85), (92.2, 38.2)]),
            p.rect(11, 38.2, 89.8, 11.87, rx=3),
            p.poly([(19.5, 90), (19.5, 50.07), (92.3, 50.07), (92.3, 90)]),
            p.poly([(48.4, 90), (48.4, 68.5), (63.4, 68.5), (63.4, 90)]),
            p.rect(26.5, 60.5, 11, 14), p.rect(74.3, 60.5, 11, 14),
            p.poly([(14.2, 90), (97.7, 90), (101.8, 96), (101.8, 102.44), (10.3, 102.44), (10.3, 96)], closed=True)]
    return [("base", bldg + r48_official_lectern()), ("accent", r48_brace())]


def commission(pen):
    """A commission: three officials seated side by side at one long table.
    Origin at the table's top center."""
    els = []
    for x in (-34, 0, 34):
        els += C.person(pen, x, -1.0, k=0.66, h=24)
    els += [pen.line(-52, 0, 52, 0), pen.line(-44, 0, -44, 34), pen.line(44, 0, 44, 34)]
    return els


def r48_desk_official(dx=0.0):
    """The official who could remove the agency's members, at a desk with no
    tie, and an arrow from the desk that stops short of the brace's nub. The
    arrow runs about 1.9 times its first length, so it reads at 48 px (the
    review's M9), and DR-08's line floor holds."""
    p = P()
    off = C.person(p, 213 + dx, 64, k=0.86, h=24) + [p.line(186 + dx, 64, 237 + dx, 64), p.line(229 + dx, 64, 229 + dx, 104)]
    arrow = [p.line(185 + dx, 40, 142, 40), p.poly([(150, 32), (142, 40), (150, 48)])]
    return off + arrow


def r48_b():
    """Outside DR-135, replacing the commission at a lectern, a near-duplicate
    of C (the review's M8): the agency as a flat-roofed office building with
    no columns or pediment (D2-623), beside the red brace and the official at
    a desk whose arrow stops at it."""
    p = P()
    bldg = [p.line(8.0, 22.0, 104.0, 22.0),
            p.poly([(14.0, 96.0), (14.0, 22.0)]), p.poly([(98.0, 22.0), (98.0, 96.0)]),
            p.line(8.0, 96.0, 104.0, 96.0)]
    for y in (34.0, 56.0):
        for x in (26.0, 50.0, 74.0):
            bldg.append(p.rect(x, y, 12.0, 12.0))
    bldg.append(p.poly([(49.0, 96.0), (49.0, 78.0), (63.0, 78.0), (63.0, 96.0)]))
    return [("base", bldg + r48_desk_official()), ("accent", r48_brace()[:2])]


def r48_c():
    """Outside DR-135. The commission at its table; the official who could
    remove them sits at a desk, not a lectern, and an arrow from that desk
    stops at the red brace, so the protection reads as a power that stops
    short."""
    p = P()
    return [("base", commission(p.sub(58, 70)) + r48_desk_official()), ("accent", r48_brace()[:2])]
