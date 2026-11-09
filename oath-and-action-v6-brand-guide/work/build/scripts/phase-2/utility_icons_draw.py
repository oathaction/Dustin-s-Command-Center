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


def reset_A(s):
    # One open circle, about three quarters round, travelling anticlockwise from 9 o'clock under and over to 12,
    # the head at the top pointing left into the gap.
    if s == 24:
        cx, cy, r, arm = 12, 12.5, 8, 3.5
    else:
        cx, cy, r, arm = 8, 8.25, 5.25, 2.5
    d = arc_d(cx, cy, r, 270, 360, clockwise=False)
    tip = clock(cx, cy, r, 0)
    return [path(d), lines(head(tip, (-1, 0), arm))]


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


ICONS = [
    # (key, file word, action label, audit rank, the drawing the audit asks for, options)
    ('close', 'Close', 'Close', '1', 'A cross', {
        'A': ('A bare cross', {
            24: [lines([(6, 6), (18, 18)], [(18, 6), (6, 18)])],
            16: [lines([(4, 4), (12, 12)], [(12, 4), (4, 12)])]}),
        'B': ('The cross in a circle', {
            24: [circle(12, 12, 9), lines([(9, 9), (15, 15)], [(15, 9), (9, 15)])],
            16: [circle(8, 8, 6.25), lines([(6, 6), (10, 10)], [(10, 6), (6, 10)])]}),
        'C': ('The cross in a square, the window sign', {
            24: [rrect(4, 4, 20, 20, R24), lines([(9, 9), (15, 15)], [(15, 9), (9, 15)])],
            16: [rrect(1.75, 1.75, 14.25, 14.25, R16), lines([(6, 6), (10, 10)], [(10, 6), (6, 10)])]}),
    }),
    ('menu', 'Menu', 'Open the menu', '2', 'Three bars', {
        'A': ('Three even bars, wide', {
            24: [path('M4 6H20 M4 12H20 M4 18H20')],
            16: [path('M2.5 3.75H13.5 M2.5 7.75H13.5 M2.5 11.75H13.5')]}),
        'B': ('Three even bars, narrow and closer', {
            24: [path('M6 7H18 M6 12H18 M6 17H18')],
            16: [path('M4 4.25H12 M4 7.75H12 M4 11.25H12')]}),
        'C': ('Three bars, the last one short', {
            24: [path('M4 6H20 M4 12H20 M4 18H13')],
            16: [path('M2.5 3.75H13.5 M2.5 7.75H13.5 M2.5 11.75H8.5')]}),
    }),
    ('arrow', 'Arrow', 'Next and Previous (mirrored), and the sort order in use (turned)', '3, 4, 16',
     'An arrow with a shaft, pointing right', {
        'A': ('An arrow with a shaft and a square-cut head', {
            24: [lines([(5, 12), (19, 12)], [(12, 5), (19, 12), (12, 19)])],
            16: [lines([(3, 7.75), (13, 7.75)], [(8.5, 3.25), (13, 7.75), (8.5, 12.25)])]}),
        'B': ('The arrow in a circle', {
            24: [circle(12, 12, 9), lines([(8, 12), (16, 12)], [(12, 8), (16, 12), (12, 16)])],
            16: [circle(8, 7.75, 6.25), lines([(5.25, 7.75), (10.75, 7.75)], [(8, 5), (10.75, 7.75), (8, 10.5)])]}),
        'C': ('A long shaft with a small head', {
            24: [lines([(3, 12), (21, 12)], [(16, 7), (21, 12), (16, 17)])],
            16: [lines([(1.75, 7.75), (14.25, 7.75)], [(11, 4.5), (14.25, 7.75), (11, 11)])]}),
    }),
    ('chevron', 'Chevron', 'Expand and collapse (down when closed, up when open)', '5', 'A chevron', {
        'A': ('A chevron, 12 units wide', {
            24: [lines([(6, 9), (12, 15), (18, 9)])],
            16: [lines([(4, 6), (8, 10), (12, 6)])]}),
        'B': ('The chevron in a circle', {
            24: [circle(12, 12, 9), lines([(8, 10.5), (12, 14.5), (16, 10.5)])],
            16: [circle(8, 8, 6.25), lines([(5.5, 7), (8, 9.5), (10.5, 7)])]}),
        'C': ('A small chevron, 8 units wide', {
            24: [lines([(8, 10), (12, 14), (16, 10)])],
            16: [lines([(5.25, 6.5), (8, 9.25), (10.75, 6.5)])]}),
    }),
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
        'C': ('An arrow down in a circle', {
            24: [circle(12, 12, 9), lines([(12, 7), (12, 16)], [(8, 12), (12, 16), (16, 12)])],
            16: [circle(7.75, 8, 6.25), lines([(7.75, 4.75), (7.75, 10.75)], [(5.25, 8.25), (7.75, 10.75), (10.25, 8.25)])]}),
    }),
    ('another-site', 'Another-Site', 'Go to another site', '7', 'Its own drawing', {
        'A': ('An arrow leaving a box by its top right corner', {
            24: [rpoly([(11, 7), (4, 7), (4, 20), (17, 20), (17, 13)], R24, closed=False),
                 lines([(14, 4), (20, 4), (20, 10)], [(10, 14), (20, 4)])],
            16: [rpoly([(7.25, 4.75), (2.75, 4.75), (2.75, 13.25), (11.25, 13.25), (11.25, 8.75)], R16, closed=False),
                 lines([(9.25, 2.75), (13.25, 2.75), (13.25, 6.75)], [(6.75, 9.25), (13.25, 2.75)])]}),
        'B': ('A bare arrow up and to the right', {
            24: [lines([(7, 6), (18, 6), (18, 17)], [(6, 18), (18, 6)])],
            16: [lines([(4.75, 4.25), (11.75, 4.25), (11.75, 11.25)], [(4.25, 11.75), (11.75, 4.25)])]}),
        'C': ('An arrow leaving a ring by its upper right', {
            24: [path(arc_d(11, 13, 8, 100, 355, clockwise=True)),
                 lines([(14, 4), (20, 4), (20, 10)], [(11, 13), (20, 4)])],
            16: [path(arc_d(6.75, 9.25, 5, 100, 355, clockwise=True)),
                 lines([(9.75, 2.25), (13.75, 2.25), (13.75, 6.25)], [(6.75, 9.25), (13.75, 2.25)])]}),
    }),
    ('search', 'Search', 'Search', '8', 'Its own drawing', {
        'A': ('A magnifier: round lens, handle to the lower right', {
            24: [circle(10.5, 10.5, 7), lines([(15.5, 15.5), (20.5, 20.5)])],
            16: [circle(7, 7, 4.75), lines([(10.5, 10.5), (13.75, 13.75)])]}),
        'B': ('The magnifier with a glint in the lens', {
            24: [circle(10.5, 10.5, 7), lines([(15.5, 15.5), (20.5, 20.5)]), path('M7 10.5 A3.5 3.5 0 0 1 10.5 7')],
            16: [circle(7, 7, 4.75), lines([(10.5, 10.5), (13.75, 13.75)]), path('M5 7 A2 2 0 0 1 7 5')]}),
        'C': ('A larger lens on a short handle', {
            24: [circle(11, 11, 8), lines([(16.66, 16.66), (20.5, 20.5)])],
            16: [circle(7.25, 7.25, 5.5), lines([(11.15, 11.15), (13.75, 13.75)])]}),
    }),
    ('filter', 'Filter', 'Filter', '9', 'A funnel, not sliders', {
        'A': ('A funnel with a slanted spout', {
            24: [rpoly([(4, 4), (20, 4), (14, 11.5), (14, 18.5), (10, 20.5), (10, 11.5)], R24)],
            16: [rpoly([(2.75, 2.75), (13.25, 2.75), (9.25, 7.75), (9.25, 12.25), (6.75, 13.5), (6.75, 7.75)], R16)]}),
        'B': ('A funnel with a square spout', {
            24: [rpoly([(4, 4), (20, 4), (14, 11.5), (14, 20), (10, 20), (10, 11.5)], R24)],
            16: [rpoly([(2.75, 2.75), (13.25, 2.75), (9.25, 7.75), (9.25, 13.25), (6.75, 13.25), (6.75, 7.75)], R16)]}),
        'C': ('A wide funnel with a short spout', {
            24: [rpoly([(3, 5), (21, 5), (14, 13), (14, 19), (10, 19), (10, 13)], R24)],
            16: [rpoly([(1.75, 3.25), (14.25, 3.25), (9.25, 8.75), (9.25, 12.75), (6.75, 12.75), (6.75, 8.75)], R16)]}),
    }),
    ('copy', 'Copy', 'Copy', '10', 'Two sheets', {
        'A': ('Two square sheets, the back one up and to the left', {
            24: [rrect(9, 9, 20, 20, R24), rpoly([(5, 15), (4, 15), (4, 4), (15, 4), (15, 5)], R24, closed=False)],
            16: [rrect(5.75, 5.75, 14.25, 14.25, R16),
                 rpoly([(3.25, 10.25), (1.75, 10.25), (1.75, 1.75), (10.25, 1.75), (10.25, 3.25)], R16, closed=False)]}),
        'B': ('Two tall sheets, the back one shown as a corner below and to the left', {
            24: [rrect(9, 3, 19, 16, R24), rpoly([(5, 8), (5, 20), (15, 20)], R24, closed=False)],
            16: [rrect(5.75, 1.75, 12.75, 10.75, R16), rpoly([(3.25, 5.25), (3.25, 13.25), (9.75, 13.25)], R16, closed=False)]}),
        'C': ('Two sheets, the front one with two lines of text', {
            24: [rrect(9, 9, 20, 20, R24), rpoly([(5, 15), (4, 15), (4, 4), (15, 4), (15, 5)], R24, closed=False),
                 path('M12 13H17 M12 16H15')],
            16: [rrect(5.75, 5.75, 14.25, 14.25, R16),
                 rpoly([(3.25, 10.25), (1.75, 10.25), (1.75, 1.75), (10.25, 1.75), (10.25, 3.25)], R16, closed=False),
                 path('M8.5 9.25H11.5')]}),
    }),
    ('play', 'Play', 'Play (one button with Pause)', '11', 'A triangle', {
        'A': ('A triangle pointing right', {
            24: [rpoly([(7, 4), (19.5, 12), (7, 20)], R24)],
            16: [rpoly([(4.75, 2.75), (13, 8), (4.75, 13.25)], R16)]}),
        'B': ('The triangle in a circle', {
            24: [circle(12, 12, 9), rpoly([(10, 8), (16.5, 12), (10, 16)], R24)],
            16: [circle(8, 8, 6.25), rpoly([(6.75, 5.25), (11, 8), (6.75, 10.75)], R16)]}),
        'C': ('The triangle on a screen', {
            24: [rrect(3, 5, 21, 19, R24), rpoly([(10, 8.5), (15.5, 12), (10, 15.5)], R24)],
            16: [rrect(1.75, 2.75, 14.25, 13.25, R16), rpoly([(6.25, 5.25), (11, 8), (6.25, 10.75)], R16)]}),
    }),
    ('pause', 'Pause', 'Pause (one button with Play)', '11', 'Two bars', {
        'A': ('Two upright bars', {
            24: [rrect(6, 4, 10, 20, R24), rrect(14, 4, 18, 20, R24)],
            16: [rrect(3.75, 2.75, 6.25, 13.25, R16), rrect(9.75, 2.75, 12.25, 13.25, R16)]}),
        'B': ('Two bars in a circle', {
            24: [circle(12, 12, 9), path('M10 9V15 M14 9V15')],
            16: [circle(8, 8, 6.25), path('M6.25 5.75V10.25 M9.75 5.75V10.25')]}),
        'C': ('Two bars on a screen', {
            24: [rrect(3, 5, 21, 19, R24), path('M10 9.5V14.5 M14 9.5V14.5')],
            16: [rrect(1.75, 2.75, 14.25, 13.25, R16), path('M6.25 6.25V9.75 M9.75 6.25V9.75')]}),
    }),
    ('reset', 'Reset', 'Reset, start over', '12', 'One open circle with one arrowhead, anticlockwise, no nodes', {
        'A': ('Three quarters of a circle, the head at the top pointing left', {24: reset_A(24), 16: reset_A(16)}),
        'B': ('Three quarters of a circle, an upright corner head at the upper left', {24: reset_B(24), 16: reset_B(16)}),
        'C': ('Three quarters of a circle, the head at the left pointing down', {24: reset_C(24), 16: reset_C(16)}),
    }),
    ('error', 'Error', 'Error mark', '13', 'A circle holding an exclamation mark, never a cross', {
        'A': ('An exclamation mark in a circle', {
            24: [circle(12, 12, 9)] + excl24(7, 13, 17),
            16: [circle(7.75, 7.75, 6.25)] + excl16(4.5, 8.5, 11.25)}),
        'B': ('An exclamation mark in an octagon, the stop sign', {
            24: [rpoly(octagon(12, 12, 8), R24)] + excl24(7, 13, 17),
            16: [rpoly(octagon(7.75, 7.75, 6), R16)] + excl16(4.5, 8.5, 11.25)}),
        'C': ('An exclamation mark in a square', {
            24: [rrect(4, 4, 20, 20, R24)] + excl24(7.5, 12.5, 16.5),
            16: [rrect(1.75, 1.75, 13.75, 13.75, R16)] + excl16(4.5, 8.5, 11.25)}),
    }),
    ('success', 'Success', 'Success mark', '14', 'The check in its enclosure', {
        'A': ('A check in a circle', {
            24: [circle(12, 12, 9), lines([(7.5, 12), (10.5, 15), (16.5, 9)])],
            16: [circle(8, 8, 6.25), lines([(5, 8), (7, 10), (11, 6)])]}),
        'B': ('A check leaving an open circle', {24: success_B(24), 16: success_B(16)}),
        'C': ('A check in a square', {
            24: [rrect(4, 4, 20, 20, R24), lines([(8, 12), (11, 15), (16, 9)])],
            16: [rrect(1.75, 1.75, 14.25, 14.25, R16), lines([(5, 8), (7, 10), (11, 6)])]}),
    }),
    ('check', 'Selected-Check', 'Selected check (a chip or list choice that is on)', '14', 'The bare check', {
        'A': ('A check, long arm at 45 degrees', {
            24: [lines([(4, 12.5), (9, 17.5), (20, 6.5)])],
            16: [lines([(3.5, 8.5), (6.5, 11.5), (13.5, 4.5)])]}),
        'B': ('A tick, the long arm steeper', {
            24: [lines([(5, 13.5), (9.5, 18), (19, 5.5)])],
            16: [lines([(3.25, 9), (6.25, 12), (12.75, 3.75)])]}),
        'C': ('A compact check', {
            24: [lines([(7, 12.5), (10.5, 16), (17, 9.5)])],
            16: [lines([(4.5, 8.25), (7, 10.75), (11.5, 6.25)])]}),
    }),
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
            16: [lines([(1.75, 5.25), (1.75, 1.75), (5.25, 1.75)], [(10.75, 1.75), (14.25, 1.75), (14.25, 5.25)],
                       [(14.25, 10.75), (14.25, 14.25), (10.75, 14.25)], [(5.25, 14.25), (1.75, 14.25), (1.75, 10.75)],
                       [(1.75, 1.75), (6.25, 6.25)], [(14.25, 1.75), (9.75, 6.25)],
                       [(14.25, 14.25), (9.75, 9.75)], [(1.75, 14.25), (6.25, 9.75)])]}),
        'C': ('Two arrows out to opposite corners', {
            24: [lines([(14, 4), (20, 4), (20, 10)], [(20, 4), (14, 10)], [(10, 20), (4, 20), (4, 14)], [(4, 20), (10, 14)])],
            16: [lines([(10.25, 1.75), (14.25, 1.75), (14.25, 5.75)], [(14.25, 1.75), (9.75, 6.25)],
                       [(5.75, 14.25), (1.75, 14.25), (1.75, 10.25)], [(1.75, 14.25), (6.25, 9.75)])]}),
    }),
    ('sort', 'Sort', 'Sort a column (can sort)', '16', 'Two small arrows, up and down', {
        'A': ('An up arrow and a down arrow side by side', {
            24: [lines([(8, 20), (8, 4)], [(4, 8), (8, 4), (12, 8)], [(16, 4), (16, 20)], [(12, 16), (16, 20), (20, 16)])],
            16: [lines([(5.25, 13.25), (5.25, 2.75)], [(2.75, 5.25), (5.25, 2.75), (7.75, 5.25)],
                       [(10.75, 2.75), (10.75, 13.25)], [(8.25, 10.75), (10.75, 13.25), (13.25, 10.75)])]}),
        'B': ('Two chevrons, one up and one down', {
            24: [lines([(8, 9), (12, 5), (16, 9)], [(8, 15), (12, 19), (16, 15)])],
            16: [lines([(5, 6.25), (8, 3.25), (11, 6.25)], [(5, 9.75), (8, 12.75), (11, 9.75)])]}),
        'C': ('One upright arrow with a head at each end', {
            24: [lines([(12, 4), (12, 20)], [(8, 8), (12, 4), (16, 8)], [(8, 16), (12, 20), (16, 16)])],
            16: [lines([(7.75, 2.75), (7.75, 13.25)], [(5, 5.5), (7.75, 2.75), (10.5, 5.5)],
                       [(5, 10.5), (7.75, 13.25), (10.5, 10.5)])]}),
    }),
    ('warning', 'Warning', 'Warning mark', '17', 'A triangle holding an exclamation mark', {
        'A': ('An exclamation mark in a wide triangle', {
            24: [rpoly([(12, 2.5), (22, 20), (2, 20)], R24)] + excl24(9.5, 13.5, 17),
            16: [rpoly([(7.75, 0.75), (15.25, 14.25), (0.25, 14.25)], R16)] + excl16(6.25, 8.5, 11.25)}),
        'B': ('An exclamation mark in a diamond, the road sign', {
            24: [rpoly([(12, 2), (22, 12), (12, 22), (2, 12)], R24)] + excl24(7.5, 13, 16.5),
            16: [rpoly([(7.75, 1), (14.5, 7.75), (7.75, 14.5), (1, 7.75)], R16)] + excl16(4.75, 7.75, 10.25)}),
        'C': ('An exclamation mark in a narrower triangle', {
            24: [rpoly([(12, 3.5), (21, 20), (3, 20)], R24)] + excl24(10, 13.5, 17),
            16: [rpoly([(7.75, 1.5), (14.25, 14.25), (1.25, 14.25)], R16)] + excl16(7.5, 9, 11.75)}),
    }),
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


def main():
    out = OUT
    if '--out' in sys.argv:
        out = os.path.abspath(sys.argv[sys.argv.index('--out') + 1])
    for sub in ('svg-24', 'svg-16'):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    manifest = []
    for key, word, label, rank, asked, options in ICONS:
        entry = {'key': key, 'word': word, 'label': label, 'rank': rank, 'asked': asked, 'options': []}
        for opt in ('A', 'B', 'C'):
            desc, sizes = options[opt]
            files = {}
            for size in (24, 16):
                name = '%s_Utility-%s-Option-%s-%dpx.svg' % (DATE, word, opt, size)
                rel = os.path.join('svg-%d' % size, name)
                with open(os.path.join(out, rel), 'w') as fh:
                    fh.write(svg_text(key, word, opt, desc, size, sizes[size]))
                files[str(size)] = rel
            entry['options'].append({'option': opt, 'shows': desc, 'files': files})
        manifest.append(entry)
    with open(os.path.join(out, '%s_Utility-Icons-Manifest.json' % DATE), 'w') as fh:
        json.dump(manifest, fh, indent=1)
    n = sum(len(e['options']) for e in manifest)
    print('wrote %d drawings, %d options, %d SVG files to %s' % (len(manifest), n, n * 2, out))


if __name__ == '__main__':
    main()
