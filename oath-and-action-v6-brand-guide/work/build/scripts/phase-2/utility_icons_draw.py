#!/usr/bin/env python3
"""Utility icon set, stage B round 1 (DR-134, DR-146): 18 drawings, three options each, at 24 and 16 px.

Written by the icon designer (utility hand, D2-498), November 9, 2026.

Construction, one family:
  24 px: a 24-unit grid, 2 px line (--oa-component-icon-utility-line-medium), every horizontal or vertical
         centerline on a whole unit so both edges of a 2 px line sit on pixel edges. Ink inside 3..21 for squares,
         2..22 for circles (a circle's ring overshoots the square by one unit a side), arrowheads may overshoot.
  16 px: its own master on a 16-unit grid, 1.5 px line, every horizontal or vertical centerline on a quarter
         (n.25 or n.75) so one edge of the 1.5 px line sits on a pixel edge. A glyph with one central vertical
         line takes x = 7.75 as its axis, and its enclosure is centred on that axis.
  Both:  round caps and joins; a frame's corner radius on the centerline is half the line (1 at 24, 0.75 at 16),
         so the outer corner rounds by one line width and the inner corner stays sharp, as in Civic Line; a dot is
         as wide as the line; one color through currentColor; no red.

Usage: python3 -I work/build/scripts/phase-2/utility_icons_draw.py [--out work/build/assets/utility-icons]
Writes svg-24/ and svg-16/ and a manifest JSON beside them.
"""
import json
import math
import os
import sys

DATE = '20261109'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'work', 'build', 'assets', 'utility-icons')


# ---------- number and element helpers ----------
def f(n):
    """Compact number: up to 3 decimals, no trailing zeros."""
    s = ('%.3f' % n).rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def pt(p):
    return f(p[0]) + ' ' + f(p[1])


def path(d):
    return '<path d="%s"/>' % d


def circle(cx, cy, r):
    return '<circle cx="%s" cy="%s" r="%s"/>' % (f(cx), f(cy), f(r))


def dot(cx, cy, r):
    return '<circle cx="%s" cy="%s" r="%s" fill="currentColor" stroke="none"/>' % (f(cx), f(cy), f(r))


def lines(*segs):
    """Open polylines: each seg is a list of points."""
    out = []
    for s in segs:
        out.append('M' + pt(s[0]) + ''.join(' L' + pt(p) for p in s[1:]))
    return path(' '.join(out))


def rpoly_d(pts, r, closed=True):
    """Polygon or polyline with every interior corner rounded to radius r on the centerline."""
    n = len(pts)
    corners = range(n) if closed else range(1, n - 1)
    seg = {}
    for i in corners:
        V = pts[i]
        A = pts[i - 1]
        B = pts[(i + 1) % n]
        u1 = ((A[0] - V[0]), (A[1] - V[1]))
        u2 = ((B[0] - V[0]), (B[1] - V[1]))
        l1 = math.hypot(*u1)
        l2 = math.hypot(*u2)
        u1 = (u1[0] / l1, u1[1] / l1)
        u2 = (u2[0] / l2, u2[1] / l2)
        cosphi = max(-1.0, min(1.0, u1[0] * u2[0] + u1[1] * u2[1]))
        phi = math.acos(cosphi)
        d = r / math.tan(phi / 2) if r > 0 else 0
        d = min(d, l1 / 2, l2 / 2)
        P1 = (V[0] + u1[0] * d, V[1] + u1[1] * d)
        P2 = (V[0] + u2[0] * d, V[1] + u2[1] * d)
        cross = (V[0] - A[0]) * (B[1] - V[1]) - (V[1] - A[1]) * (B[0] - V[0])
        sweep = 1 if cross > 0 else 0
        rr = d * math.tan(phi / 2)
        seg[i] = (P1, P2, rr, sweep)
    if closed:
        P1, P2, rr, sw = seg[0]
        d = 'M' + pt(P2)
        for i in list(range(1, n)) + [0]:
            P1, P2, rr, sw = seg[i]
            d += ' L' + pt(P1) + ' A%s %s 0 0 %d %s' % (f(rr), f(rr), sw, pt(P2))
        return d + ' Z'
    d = 'M' + pt(pts[0])
    for i in range(1, n - 1):
        P1, P2, rr, sw = seg[i]
        d += ' L' + pt(P1) + ' A%s %s 0 0 %d %s' % (f(rr), f(rr), sw, pt(P2))
    return d + ' L' + pt(pts[-1])


def rpoly(pts, r, closed=True):
    return path(rpoly_d(pts, r, closed))


def rrect(x1, y1, x2, y2, r):
    return rpoly([(x1, y1), (x2, y1), (x2, y2), (x1, y2)], r)


def clock(cx, cy, r, theta):
    """Point on a circle at a clock angle (degrees clockwise from 12 o'clock)."""
    t = math.radians(theta)
    return (cx + r * math.sin(t), cy - r * math.cos(t))


def arc_d(cx, cy, r, t0, t1, clockwise):
    """Arc from clock angle t0 to t1, travelling clockwise or anticlockwise."""
    span = (t1 - t0) % 360 if clockwise else (t0 - t1) % 360
    p0 = clock(cx, cy, r, t0)
    p1 = clock(cx, cy, r, t1)
    return 'M%s A%s %s 0 %d %d %s' % (pt(p0), f(r), f(r), 1 if span > 180 else 0, 1 if clockwise else 0, pt(p1))


def head(tip, direction, arm, spread=45):
    """Open arrowhead: two arms running back from the tip at +/- spread degrees to the direction of travel."""
    dx, dy = direction
    L = math.hypot(dx, dy)
    dx, dy = dx / L, dy / L
    bx, by = -dx, -dy
    pts = []
    for s in (spread, -spread):
        a = math.radians(s)
        rx = bx * math.cos(a) - by * math.sin(a)
        ry = bx * math.sin(a) + by * math.cos(a)
        pts.append((tip[0] + rx * arm, tip[1] + ry * arm))
    return [pts[0], tip, pts[1]]


def octagon(cx, cy, half):
    """Regular octagon with flat sides, its flats `half` from the centre on the centerline."""
    c = half * math.tan(math.radians(22.5))
    return [(cx - c, cy - half), (cx + c, cy - half), (cx + half, cy - c), (cx + half, cy + c),
            (cx + c, cy + half), (cx - c, cy + half), (cx - half, cy + c), (cx - half, cy - c)]


# ---------- the drawings ----------
# Each option: {24: [elements], 16: [elements]}. Coordinates are centerlines.
R24, R16 = 1, 0.75          # frame corner radius on the centerline: half the line
DOT24, DOT16 = 1, 0.75      # a dot is as wide as the line


def excl24(top, bottom, dot_y, x=12):
    return [path('M%s %sV%s' % (f(x), f(top), f(bottom))), dot(x, dot_y, DOT24)]


def excl16(top, bottom, dot_y, x=7.75):
    return [path('M%s %sV%s' % (f(x), f(top), f(bottom))), dot(x, dot_y, DOT16)]


def reset_B(s):
    # The arc runs anticlockwise from 7:30 to about 10:40, then a short straight run to the tip; the head is an
    # upright L, so its two arms sit on whole pixels. The gap faces left.
    if s == 24:
        cx, cy, r, t_end, tip, arm = 12, 12, 8, 320, (5, 8), 5
    else:
        cx, cy, r, t_end, tip, arm = 8, 8, 5.25, 320, (3.25, 5.25), 3.25
    d = arc_d(cx, cy, r, 225, t_end, clockwise=False)
    d += ' L' + pt(tip)
    return [path(d), lines([(tip[0], tip[1] - arm), tip, (tip[0] + arm, tip[1])])]


def reset_C(s):
    # Three quarters round, travelling anticlockwise from 6 o'clock up the right side, over the top and down the
    # left to 9 o'clock; the head at 9 points down, and the gap faces the lower left.
    if s == 24:
        cx, cy, r, arm = 12.5, 12, 8, 3.5
    else:
        cx, cy, r, arm = 8.25, 8, 5.25, 2.5
    d = arc_d(cx, cy, r, 180, 270, clockwise=False)
    tip = clock(cx, cy, r, 270)
    return [path(d), lines(head(tip, (0, 1), arm))]


def success_B(s):
    if s == 24:
        cx, cy, r = 12, 12, 9
        d = arc_d(cx, cy, r, 82, 26, clockwise=True)
        return [path(d), lines([(7.5, 11.5), (11, 15), (20.5, 5.5)])]
    cx, cy, r = 8, 8, 6.25
    d = arc_d(cx, cy, r, 82, 26, clockwise=True)
    return [path(d), lines([(4.75, 7.5), (7.25, 10), (13.75, 3.5)])]


def reset_undo(s):
    # Fix round: the undo arc. Half a circle and a little more, travelling anticlockwise from the lower right over
    # the top, then a short run to an upright corner head at the left: the undo sign of word processors, inside the
    # audit's "open circle with one arrowhead".
    if s == 24:
        cx, cy, r, t0, t1, tip, arm = 12.5, 15, 8, 110, 300, (4, 13), 5
    else:
        cx, cy, r, t0, t1, tip, arm = 8.25, 9.75, 5.25, 110, 300, (2.75, 8.75), 3.25
    d = arc_d(cx, cy, r, t0, t1, clockwise=False) + ' L' + pt(tip)
    return [path(d), lines([(tip[0], tip[1] - arm), tip, (tip[0] + arm, tip[1])])]


def cut(key, size, shape, holes, w):
    """A solid shape in currentColor with line-width holes cut by a mask (one color, no second ink)."""
    mid = 'U-%s-%d-cut' % (key, size)
    return ['<defs><mask id="%s" maskUnits="userSpaceOnUse" x="0" y="0" width="%d" height="%d">'
            '<rect width="%d" height="%d" fill="#fff" stroke="none"/>'
            '<g fill="none" stroke="#000" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round">%s</g>'
            '</mask></defs>' % (mid, size, size, size, size, w, ''.join(holes)),
            shape.replace('/>', ' fill="currentColor" stroke="none" mask="url(#%s)"/>' % mid, 1)]


def solid_disc_check(s):
    if s == 24:
        return cut('success-A', 24, circle(12, 12, 10), [lines([(7.5, 12), (10.5, 15), (16.5, 9)])], '2')
    return cut('success-A', 16, circle(8, 8, 6.75), [lines([(5, 8), (7, 10), (11, 6)])], '2')


ICONS = [
    # (key, file word, action label, audit rank, the drawing the audit asks for, options, reason when fewer than three)
    ('close', 'Close', 'Close', '1', 'A cross', {
        'A': ('A bare cross', {
            24: [lines([(6, 6), (18, 18)], [(18, 6), (6, 18)])],
            16: [lines([(4, 4), (12, 12)], [(12, 4), (4, 12)])]}),
    }, 'Readers know one sign for Close, the bare cross. The ring is a choice for the whole set, on the family card.'),
    ('menu', 'Menu', 'Open the menu', '2', 'Three bars', {
        'A': ('Three even bars', {
            24: [path('M4 6H20 M4 12H20 M4 18H20')],
            16: [path('M2.5 3.75H13.5 M2.5 7.75H13.5 M2.5 11.75H13.5')]}),
        'B': ('Two even bars', {
            24: [path('M4 9H20 M4 15H20')],
            16: [path('M2.5 5.75H13.5 M2.5 9.75H13.5')]}),
    }, 'Three dots say More and a grid says apps, so no third form names Menu.'),
    ('arrow', 'Arrow', 'Next and Previous (mirrored), and the sort order in use (turned)', '3, 4, 16',
     'An arrow with a shaft, pointing right', {
        'A': ('An arrow with a shaft and an open head', {
            24: [lines([(5, 12), (19, 12)], [(12, 5), (19, 12), (12, 19)])],
            16: [lines([(3, 7.75), (13, 7.75)], [(8.5, 3.25), (13, 7.75), (8.5, 12.25)])]}),
        'B': ('An arrow with a shaft and a closed triangle head', {
            24: [lines([(4, 12), (14, 12)]), rpoly([(14, 7), (20, 12), (14, 17)], R24)],
            16: [lines([(2.75, 7.75), (9.25, 7.75)]), rpoly([(9.25, 4.25), (13.75, 7.75), (9.25, 11.25)], R16)]}),
    }, 'A longer shaft repeated A, and the ring is a choice for the whole set, on the family card.'),
    ('chevron', 'Chevron', 'Expand and collapse (down when closed, up when open)', '5', 'A chevron', {
        'A': ('A chevron', {
            24: [lines([(6, 9), (12, 15), (18, 9)])],
            16: [lines([(4, 6), (8, 10), (12, 6)])]}),
        'B': ('A disclosure triangle, drawn in line', {
            24: [rpoly([(7, 9), (17, 9), (12, 15)], R24)],
            16: [rpoly([(4.25, 5.75), (11.75, 5.75), (8, 10.25)], R16)]}),
    }, 'A smaller chevron repeated A, and plus and minus are the atlas\'s polarity signs.'),
    ('download', 'Download', 'Download', '6', 'Its own drawing', {
        'A': ('An arrow down into an open tray', {
            24: [lines([(12, 4), (12, 15)], [(7, 10), (12, 15), (17, 10)]),
                 rpoly([(4, 15), (4, 20), (20, 20), (20, 15)], R24, closed=False)],
            16: [lines([(7.75, 2.5), (7.75, 10.25)], [(4.5, 7), (7.75, 10.25), (11, 7)]),
                 rpoly([(2.75, 10.25), (2.75, 13.75), (12.75, 13.75), (12.75, 10.25)], R16, closed=False)]}),
        'B': ('An arrow down onto a line', {
            24: [lines([(12, 4), (12, 16)], [(7, 11), (12, 16), (17, 11)], [(5, 20), (19, 20)])],
            16: [lines([(7.75, 2.25), (7.75, 10.25)], [(4.5, 7), (7.75, 10.25), (11, 7)],
                       [(3.25, 13.75), (12.25, 13.75)])]}),
        'C': ('An arrow down on a page with a folded corner', {
            24: [rpoly([(5, 3), (14, 3), (19, 8), (19, 21), (5, 21)], R24), lines([(14, 3), (14, 8), (19, 8)]),
                 lines([(12, 11), (12, 17)], [(9, 14), (12, 17), (15, 14)])],
            16: [rpoly([(2.75, 1.75), (9.75, 1.75), (13.25, 5.25), (13.25, 14.25), (2.75, 14.25)], R16),
                 lines([(7.75, 6.75), (7.75, 11.25)], [(5.75, 9.25), (7.75, 11.25), (9.75, 9.25)])]}),
    }, None),
    ('another-site', 'Another-Site', 'Go to another site', '7', 'Its own drawing', {
        'A': ('An arrow leaving a box by its top right corner', {
            24: [rpoly([(11, 7), (4, 7), (4, 20), (17, 20), (17, 13)], R24, closed=False),
                 lines([(14, 4), (20, 4), (20, 10)], [(10, 14), (20, 4)])],
            16: [rpoly([(7.25, 4.75), (2.75, 4.75), (2.75, 13.25), (11.25, 13.25), (11.25, 8.75)], R16, closed=False),
                 lines([(9.25, 2.75), (13.25, 2.75), (13.25, 6.75)], [(6.75, 9.25), (13.25, 2.75)])]}),
        'B': ('A bare arrow up and to the right', {
            24: [lines([(7, 6), (18, 6), (18, 17)], [(6, 18), (18, 6)])],
            16: [lines([(4.75, 4.25), (11.75, 4.25), (11.75, 11.25)], [(4.25, 11.75), (11.75, 4.25)])]}),
    }, 'A window would say the link opens a new window, and these links open in the same tab (audit 1.2).'),
    ('search', 'Search', 'Search', '8', 'Its own drawing', {
        'A': ('A magnifier: round lens, handle to the lower right', {
            24: [circle(10.5, 10.5, 7), lines([(15.5, 15.5), (20.5, 20.5)])],
            16: [circle(7, 7, 4.75), lines([(10.5, 10.5), (13.75, 13.75)])]}),
    }, 'Readers know one sign for Search. A glint or a larger lens repeated it, and the ring is on the family card.'),
    ('filter', 'Filter', 'Filter', '9', 'A funnel, not sliders', {
        'A': ('A funnel with a slanted spout', {
            24: [rpoly([(4, 4), (20, 4), (14, 11.5), (14, 18.5), (10, 20.5), (10, 11.5)], R24)],
            16: [rpoly([(2.75, 2.75), (13.25, 2.75), (9.25, 7.75), (9.25, 12.25), (6.75, 13.5), (6.75, 7.75)], R16)]}),
        'B': ('Three lines narrowing downward, the list filter', {
            24: [path('M4 7H20 M7 12H17 M10 17H14')],
            16: [path('M2.5 3.75H13.5 M4.75 7.75H11.25 M7 11.75H9')]}),
    }, 'A square spout and a wider funnel repeated A (0.997 and 0.938).'),
    ('copy', 'Copy', 'Copy', '10', 'Two sheets', {
        'A': ('Two square sheets, the back one up and to the left', {
            24: [rrect(9, 9, 20, 20, R24), rpoly([(5, 15), (4, 15), (4, 4), (15, 4), (15, 5)], R24, closed=False)],
            16: [rrect(5.75, 5.75, 14.25, 14.25, R16),
                 rpoly([(3.25, 10.25), (1.75, 10.25), (1.75, 1.75), (10.25, 1.75), (10.25, 3.25)], R16, closed=False)]}),
        'B': ('Two tall sheets, the back one shown as a corner below and to the left', {
            24: [rrect(9, 3, 19, 16, R24), rpoly([(5, 8), (5, 20), (15, 20)], R24, closed=False)],
            16: [rrect(5.75, 1.75, 12.75, 10.75, R16), rpoly([(3.25, 5.25), (3.25, 13.25), (9.75, 13.25)], R16, closed=False)]}),
        'C': ('Two sheets, the front one with text', {
            24: [rrect(9, 9, 20, 20, R24), rpoly([(5, 15), (4, 15), (4, 4), (15, 4), (15, 5)], R24, closed=False),
                 path('M12 13H17 M12 16H15')],
            16: [rrect(5.25, 5.25, 14.25, 14.25, R16),
                 rpoly([(2.5, 9.75), (1.75, 9.75), (1.75, 1.75), (9.75, 1.75), (9.75, 2.5)], R16, closed=False),
                 path('M8.25 8.75H11.25')]}),
    }, None),
    ('play', 'Play', 'Play (one button with Pause)', '11', 'A triangle', {
        'A': ('A triangle pointing right', {
            24: [rpoly([(7, 4), (19.5, 12), (7, 20)], R24)],
            16: [rpoly([(4.75, 2.75), (13, 8), (4.75, 13.25)], R16)]}),
    }, 'Readers know one sign for Play. The ring is on the family card, and a screen narrows Play to video.'),
    ('pause', 'Pause', 'Pause (one button with Play)', '11', 'Two bars', {
        'A': ('Two upright bars', {
            24: [rrect(6, 4, 10, 20, R24), rrect(14, 4, 18, 20, R24)],
            16: [rrect(3.75, 2.75, 6.25, 13.25, R16), rrect(9.75, 2.75, 12.25, 13.25, R16)]}),
    }, 'Readers know one sign for Pause. The ring is on the family card, and a screen narrows Pause to video.'),
    ('reset', 'Reset', 'Reset, start over', '12', 'One open circle with one arrowhead, anticlockwise, no nodes', {
        'A': ('The undo arc: half a circle over the top, an upright corner head at the left', {24: reset_undo(24), 16: reset_undo(16)}),
        'B': ('Three quarters of a circle, an upright corner head at the upper left', {24: reset_B(24), 16: reset_B(16)}),
        'C': ('Three quarters of a circle, the head at the left pointing down', {24: reset_C(24), 16: reset_C(16)}),
    }, None),
    ('error', 'Error', 'Error mark', '13', 'A circle holding an exclamation mark, never a cross', {
        'A': ('An exclamation mark in a circle', {
            24: [circle(12, 12, 9)] + excl24(7, 13, 17),
            16: [circle(7.75, 7.75, 6.25)] + excl16(4.5, 8.5, 11.25)}),
        'B': ('An exclamation mark in an octagon, the stop sign', {
            24: [rpoly(octagon(12, 12, 8), R24)] + excl24(7, 13, 17),
            16: [rpoly([(5.25, 1.75), (10.25, 1.75), (13.75, 5.25), (13.75, 10.25), (10.25, 13.75), (5.25, 13.75),
                        (1.75, 10.25), (1.75, 5.25)], R16)] + excl16(4.5, 8.5, 11.25)}),
        'C': ('An exclamation mark in a square', {
            24: [rrect(4, 4, 20, 20, R24)] + excl24(7.5, 12.5, 16.5),
            16: [rrect(1.75, 1.75, 13.75, 13.75, R16)] + excl16(4.5, 8.5, 11.25)}),
    }, None),
    ('success', 'Success', 'Success mark', '14', 'The check in its enclosure', {
        'A': ('A check cut out of a solid disc', {24: solid_disc_check(24), 16: solid_disc_check(16)}),
        'B': ('A check leaving an open circle', {24: success_B(24), 16: success_B(16)}),
    }, 'The closed circle repeated B, and the ticked box says selected, so it moves to the Selected check card.'),
    ('check', 'Selected-Check', 'Selected check (a chip or list choice that is on)', '14', 'The bare check', {
        'A': ('A check', {
            24: [lines([(4, 12.5), (9, 17.5), (20, 6.5)])],
            16: [lines([(3.5, 8.5), (6.5, 11.5), (13.5, 4.5)])]}),
        'B': ('A check in a square, the ticked box', {
            24: [rrect(4, 4, 20, 20, R24), lines([(8, 12), (11, 15), (16, 9)])],
            16: [rrect(1.75, 1.75, 14.25, 14.25, R16), lines([(5, 8), (7, 10), (11, 6)])]}),
    }, 'A steeper tick and a compact check repeated A, and the compact one read as the chevron at 16 px.'),
    ('full-size', 'View-Full-Size', 'View full size', '15', 'Four corners pointing out', {
        'A': ('Four corners', {
            24: [rpoly([(4, 9), (4, 4), (9, 4)], R24, closed=False), rpoly([(15, 4), (20, 4), (20, 9)], R24, closed=False),
                 rpoly([(20, 15), (20, 20), (15, 20)], R24, closed=False), rpoly([(9, 20), (4, 20), (4, 15)], R24, closed=False)],
            16: [rpoly([(1.75, 5.25), (1.75, 1.75), (5.25, 1.75)], R16, closed=False),
                 rpoly([(10.75, 1.75), (14.25, 1.75), (14.25, 5.25)], R16, closed=False),
                 rpoly([(14.25, 10.75), (14.25, 14.25), (10.75, 14.25)], R16, closed=False),
                 rpoly([(5.25, 14.25), (1.75, 14.25), (1.75, 10.75)], R16, closed=False)]}),
        'B': ('Four arrows from the middle out to the corners', {
            24: [lines([(4, 9), (4, 4), (9, 4)], [(15, 4), (20, 4), (20, 9)], [(20, 15), (20, 20), (15, 20)],
                       [(9, 20), (4, 20), (4, 15)],
                       [(4, 4), (10, 10)], [(20, 4), (14, 10)], [(20, 20), (14, 14)], [(4, 20), (10, 14)])],
            16: [lines([(1.75, 4.25), (1.75, 1.75), (4.25, 1.75)], [(11.75, 1.75), (14.25, 1.75), (14.25, 4.25)],
                       [(14.25, 11.75), (14.25, 14.25), (11.75, 14.25)], [(4.25, 14.25), (1.75, 14.25), (1.75, 11.75)],
                       [(1.75, 1.75), (5.75, 5.75)], [(14.25, 1.75), (10.25, 5.75)],
                       [(14.25, 14.25), (10.25, 10.25)], [(1.75, 14.25), (5.75, 10.25)])]}),
        'C': ('Two arrows out to opposite corners', {
            24: [lines([(14, 4), (20, 4), (20, 10)], [(20, 4), (14, 10)], [(10, 20), (4, 20), (4, 14)], [(4, 20), (10, 14)])],
            16: [lines([(10.25, 1.75), (14.25, 1.75), (14.25, 5.75)], [(14.25, 1.75), (9.75, 6.25)],
                       [(5.75, 14.25), (1.75, 14.25), (1.75, 10.25)], [(1.75, 14.25), (6.25, 9.75)])]}),
    }, None),
    ('sort', 'Sort', 'Sort a column (can sort)', '16', 'Two small arrows, up and down', {
        'A': ('An up arrow and a down arrow side by side', {
            24: [lines([(8, 20), (8, 4)], [(4, 8), (8, 4), (12, 8)], [(16, 4), (16, 20)], [(12, 16), (16, 20), (20, 16)])],
            16: [lines([(5.25, 13.25), (5.25, 2.75)], [(2.75, 5.25), (5.25, 2.75), (7.75, 5.25)],
                       [(10.75, 2.75), (10.75, 13.25)], [(8.25, 10.75), (10.75, 13.25), (13.25, 10.75)])]}),
        'B': ('Two chevrons, one up and one down', {
            24: [lines([(8, 9), (12, 5), (16, 9)], [(8, 15), (12, 19), (16, 15)])],
            16: [lines([(5, 6.25), (8, 3.25), (11, 6.25)], [(5, 9.75), (8, 12.75), (11, 9.75)])]}),
        'C': ('Bars of falling length beside a down arrow, the sort-lines sign', {
            24: [path('M3 6H12 M3 12H10 M3 18H8'), lines([(17, 5), (17, 19)], [(14, 16), (17, 19), (20, 16)])],
            16: [path('M1.75 3.75H8.25 M1.75 7.75H6.75 M1.75 11.75H5.25'),
                 lines([(11.75, 2.75), (11.75, 13.25)], [(9.5, 11), (11.75, 13.25), (14, 11)])]}),
    }, None),
    ('warning', 'Warning', 'Warning mark', '17', 'A triangle holding an exclamation mark', {
        'A': ('An exclamation mark in a triangle', {
            24: [rpoly([(12, 2.5), (22, 20), (2, 20)], R24)] + excl24(9.5, 13.5, 17),
            16: [rpoly([(7.75, 0.75), (15.25, 14.25), (0.25, 14.25)], R16)] + excl16(6.25, 8.5, 11.25)}),
        'B': ('An exclamation mark in a diamond, the road sign', {
            24: [rpoly([(12, 2), (22, 12), (12, 22), (2, 12)], R24)] + excl24(7.5, 13, 16.5),
            16: [rpoly([(7.75, 1), (14.5, 7.75), (7.75, 14.5), (1, 7.75)], R16)] + excl16(4.75, 7.75, 10.25)}),
    }, 'Readers know two warning shapes, the triangle and the diamond. A narrower triangle repeated A.'),
]


# ---------- the family card (D2-621): the same actions, each set in a ring ----------
# Each action's recommended picture, smaller, inside the ring the old B options used (r 9 at 24 px, 6.25 at 16 px).
def ring(s):
    return circle(12, 12, 9) if s == 24 else circle(8, 8, 6.25)


def reset_ringed(s):
    if s == 24:
        cx, cy, r, tip, arm = 12, 12, 4.5, (8, 11), 3
        d = arc_d(cx, cy, r, 225, 320, clockwise=False) + ' L' + pt(tip)
        return [path(d), lines([(tip[0], tip[1] - arm), tip, (tip[0] + arm, tip[1])])]
    # 16 px: the ring leaves no room for the upright corner head, so the head runs along the arc's tangent.
    cx, cy, r = 8, 8, 3.5
    d = arc_d(cx, cy, r, 225, 320, clockwise=False)
    tip = clock(cx, cy, r, 320)
    t = math.radians(320)
    return [path(d), lines(head(tip, (-math.cos(t), -math.sin(t)), 2))]


RINGED = [
    ('close', 'Close', {24: [lines([(9, 9), (15, 15)], [(15, 9), (9, 15)])],
                        16: [lines([(6, 6), (10, 10)], [(10, 6), (6, 10)])]}),
    ('menu', 'Menu', {24: [path('M8 9H16 M8 12H16 M8 15H16')],
                      16: [path('M5.75 5.25H10.25 M5.75 7.75H10.25 M5.75 10.25H10.25')]}),
    ('arrow', 'Arrow', {24: [lines([(8, 12), (16, 12)], [(12, 8), (16, 12), (12, 16)])],
                        16: [lines([(5.25, 7.75), (10.75, 7.75)], [(8, 5), (10.75, 7.75), (8, 10.5)])]}),
    ('chevron', 'Chevron', {24: [lines([(8, 10.5), (12, 14.5), (16, 10.5)])],
                            16: [lines([(5.5, 7), (8, 9.5), (10.5, 7)])]}),
    ('download', 'Download', {24: [lines([(12, 7), (12, 14)], [(9, 11), (12, 14), (15, 11)], [(9, 17), (15, 17)])],
                              16: [lines([(7.75, 4.5), (7.75, 8.25)], [(6.25, 6.75), (7.75, 8.25), (9.25, 6.75)],
                                         [(6.5, 11.25), (9, 11.25)])]}),
    ('another-site', 'Another-Site', {24: [rpoly([(10, 9), (8, 9), (8, 16), (15, 16), (15, 14)], R24, closed=False),
                                           lines([(13, 8), (16, 8), (16, 11)], [(11.5, 12.5), (16, 8)])],
                                      16: [rpoly([(5.25, 7.5), (5.25, 10.75), (8.5, 10.75)], R16, closed=False),
                                           lines([(8.75, 5.75), (10.25, 5.75), (10.25, 7.25)], [(7.75, 8.25), (10.25, 5.75)])]}),
    ('search', 'Search', {24: [circle(11, 11, 3.5), lines([(13.5, 13.5), (16, 16)])],
                          16: [circle(7.5, 7.5, 2.25), lines([(9.25, 9.25), (10.5, 10.5)])]}),
    ('filter', 'Filter', {24: [rpoly([(8, 8), (16, 8), (13, 12), (13, 16), (11, 17), (11, 12)], R24)],
                          16: [rpoly([(5.25, 5.25), (10.75, 5.25), (9.25, 7.75), (9.25, 10.75), (6.75, 11.25), (6.75, 7.75)], R16)]}),
    ('copy', 'Copy', {24: [rrect(11, 11, 16, 16, R24), rpoly([(9, 13), (8, 13), (8, 8), (13, 8), (13, 9)], R24, closed=False)],
                      16: [rrect(7.25, 7.25, 10.75, 10.75, R16),
                           rpoly([(5.75, 8.75), (5.25, 8.75), (5.25, 5.25), (8.75, 5.25), (8.75, 5.75)], R16, closed=False)]}),
    ('play', 'Play', {24: [rpoly([(10, 8), (16.5, 12), (10, 16)], R24)],
                      16: [rpoly([(6.75, 5.25), (11, 8), (6.75, 10.75)], R16)]}),
    ('pause', 'Pause', {24: [path('M10 9V15 M14 9V15')],
                        16: [path('M6.25 5.75V10.25 M9.75 5.75V10.25')]}),
    ('reset', 'Reset', {24: reset_ringed(24), 16: reset_ringed(16)}),
    ('check', 'Selected-Check', {24: [lines([(8.5, 12.5), (11, 15), (15.5, 9.5)])],
                                 16: [lines([(5.5, 8.25), (7.25, 10), (10.5, 6.25)])]}),
    ('full-size', 'View-Full-Size', {24: [rpoly([(8, 10.5), (8, 8), (10.5, 8)], R24, closed=False),
                                          rpoly([(13.5, 8), (16, 8), (16, 10.5)], R24, closed=False),
                                          rpoly([(16, 13.5), (16, 16), (13.5, 16)], R24, closed=False),
                                          rpoly([(10.5, 16), (8, 16), (8, 13.5)], R24, closed=False)],
                                     16: [path('M5.75 7.25V5.75H7.25 M8.75 5.75H10.25V7.25 M10.25 8.75V10.25H8.75 M7.25 10.25H5.75V8.75')]}),
    ('sort', 'Sort', {24: [lines([(10, 16), (10, 8)], [(8, 10), (10, 8), (12, 10)], [(14, 8), (14, 16)], [(12, 14), (14, 16), (16, 14)])],
                      16: [lines([(5.75, 10.25), (5.75, 5.75)], [(4.5, 7), (5.75, 5.75), (7, 7)],
                                 [(10.25, 5.75), (10.25, 10.25)], [(9, 9), (10.25, 10.25), (11.5, 9)])]}),
]

# Solid partners for Success A, so the three marks could stay one kind if Dustin picks the solid disc.
SOLID = [
    ('error', 'Error', 'An exclamation mark cut out of a solid disc', {
        24: cut('error-solid', 24, circle(12, 12, 10), [path('M12 7V13'), path('M12 17h0')], '2'),
        16: cut('error-solid', 16, circle(8, 8, 6.75), [path('M8 4.5V8.5'), path('M8 11.5h0')], '2')}),
    ('warning', 'Warning', 'An exclamation mark cut out of a solid triangle', {
        24: cut('warning-solid', 24, rpoly([(12, 1.5), (23, 21), (1, 21)], 1.5), [path('M12 9.5V13.5'), path('M12 17h0')], '2'),
        16: cut('warning-solid', 16, rpoly([(8, 0.5), (15.5, 15), (0.5, 15)], 1), [path('M8 6.75V9.25'), path('M8 12.5h0')], '2')}),
]


def svg_text(key, word, opt, desc, size, elems):
    w = '2' if size == 24 else '1.5'
    body = '\n  '.join(elems)
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" fill="none" '
            'stroke="currentColor" stroke-width="%s" stroke-linecap="round" stroke-linejoin="round" '
            'aria-hidden="true" focusable="false" data-icon="U-%s" data-icon-family="utility" data-option="%s" '
            'data-size="%d">\n'
            '  <!-- Oath & Action utility icon: %s, option %s, %d px master. %s. %d-unit grid, %s px line, round caps '
            'and joins, currentColor, no red. Stage B drawings, November 9, 2026 (DR-134, DR-146). -->\n'
            '  %s\n</svg>\n') % (size, size, size, size, w, key, opt, size, word.replace('-', ' '), opt, size, desc,
                                  size, w, body)


def write_set(out, sub, items, tag):
    """Write one SVG per item and size under out/sub; return {size: [relative paths]}. items: (key, word, desc, sizes)."""
    files = {}
    for size in (24, 16):
        os.makedirs(os.path.join(out, sub, 'svg-%d' % size), exist_ok=True)
    for key, word, desc, sizes in items:
        files[key] = {}
        for size in (24, 16):
            name = '%s_Utility-%s-%s-%dpx.svg' % (DATE, word, tag, size)
            rel = os.path.join(sub, 'svg-%d' % size, name) if sub else os.path.join('svg-%d' % size, name)
            with open(os.path.join(out, rel), 'w') as fh:
                fh.write(svg_text(key, word, tag, desc, size, sizes[size]))
            files[key][str(size)] = rel
    return files


def prune(folder, keep):
    """Remove this script's own SVG files that the current set no longer holds (options that left a card)."""
    removed = []
    for fn in sorted(os.listdir(folder)):
        if fn.startswith(DATE + '_Utility-') and fn.endswith('.svg') and fn not in keep:
            os.remove(os.path.join(folder, fn))
            removed.append(fn)
    return removed


def main():
    out = OUT
    if '--out' in sys.argv:
        out = os.path.abspath(sys.argv[sys.argv.index('--out') + 1])
    for sub in ('svg-24', 'svg-16'):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    manifest = []
    keep = {24: set(), 16: set()}
    for key, word, label, rank, asked, options, reason in ICONS:
        entry = {'key': key, 'word': word, 'label': label, 'rank': rank, 'asked': asked, 'options': [],
                 'fewer_reason': reason if len(options) < 3 else None}
        for opt in sorted(options):
            desc, sizes = options[opt]
            files = {}
            for size in (24, 16):
                name = '%s_Utility-%s-Option-%s-%dpx.svg' % (DATE, word, opt, size)
                rel = os.path.join('svg-%d' % size, name)
                with open(os.path.join(out, rel), 'w') as fh:
                    fh.write(svg_text(key, word, opt, desc, size, sizes[size]))
                files[str(size)] = rel
                keep[size].add(name)
            entry['options'].append({'option': opt, 'shows': desc, 'files': files})
        manifest.append(entry)
    removed = prune(os.path.join(out, 'svg-24'), keep[24]) + prune(os.path.join(out, 'svg-16'), keep[16])
    ringed = write_set(out, 'family-ringed', [(k, w, 'The recommended picture set in a ring, for the family card',
                                               {24: [ring(24)] + d[24], 16: [ring(16)] + d[16]})
                                              for k, w, d in RINGED], 'Ringed')
    solid = write_set(out, 'solid-partners', [(k, w, desc, d) for k, w, desc, d in SOLID], 'Solid-Partner')
    doc = {'cards': manifest, 'family_ringed': ringed, 'solid_partners': solid}
    with open(os.path.join(out, '%s_Utility-Icons-Manifest.json' % DATE), 'w') as fh:
        json.dump(doc, fh, indent=1)
    n = sum(len(e['options']) for e in manifest)
    print('wrote %d drawings, %d options, %d option SVGs, %d ringed and %d solid-partner SVGs; removed %d stale files'
          % (len(manifest), n, n * 2, len(ringed) * 2, len(solid) * 2, len(removed)))
    for r in removed:
        print('  removed', r)


if __name__ == '__main__':
    main()
