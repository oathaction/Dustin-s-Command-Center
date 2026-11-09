"""Stage B Civic Line drawings: shared drawing and export helpers.

Every drawing is authored in Civic Line's source space, where the line is
5.5 source px (the set's W), and baked into the 128-unit box with the family's
own code (cl_svg.parse_source and cl_svg.emit) and the capped fit of DR-08:
s = min(116 / extent, 1.25 * 0.487395), centered on the ink box. So a new
drawing carries the same line, caps, joins, colors and file layout as the
122 masters.

A drawing is a list of groups, each (role, [element]), painted in order.
An element is (tag, attrs) where attrs holds geometry plus optional id and
class ('butt', 'fill', 'fill-stroke', 'miter').

The Pen maps local coordinates by offset and uniform scale, so one sign can
be drawn once and placed in several drawings. Only geometry scales; the line
weight is the family's in every placement.
"""
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CL_SCRIPTS = os.path.join(ROOT, "work", "build", "scripts", "civic-line")
sys.path.insert(0, CL_SCRIPTS)
import cl_svg  # noqa: E402

W = 5.5                      # Civic Line line, source px
S_SHARED = 0.487395          # shared scale, units per source px
CAP = 1.25                   # DR-08
FILL = 116.0
S_CAP = CAP * S_SHARED       # 0.60924375
CHARCOAL = "#121212"
RED = "#E63946"
NEWSPRINT = "#DCD9D2"
DATE = "20261109"


def f(v):
    s = f"{v:.3f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


class Pen:
    """Map local (x, y) to source space: (ox + k x, oy + k y)."""

    def __init__(self, ox=0.0, oy=0.0, k=1.0, mirror=False):
        self.ox, self.oy, self.k, self.mirror = ox, oy, k, mirror

    def p(self, x, y):
        if self.mirror:
            x = -x
        return (self.ox + self.k * x, self.oy + self.k * y)

    def sub(self, ox, oy, k=1.0):
        X, Y = self.p(ox, oy)
        return Pen(X, Y, self.k * k, self.mirror)

    # elements -------------------------------------------------------------
    def line(self, x1, y1, x2, y2, **kw):
        a, b = self.p(x1, y1), self.p(x2, y2)
        return ("line", dict(x1=a[0], y1=a[1], x2=b[0], y2=b[1], **kw))

    def poly(self, pts, closed=False, **kw):
        q = " ".join(f"{f(X)},{f(Y)}" for X, Y in (self.p(x, y) for x, y in pts))
        return ("polygon" if closed else "polyline", dict(points=q, **kw))

    def circle(self, cx, cy, r, **kw):
        c = self.p(cx, cy)
        return ("circle", dict(cx=c[0], cy=c[1], r=r * self.k, **kw))

    def ellipse(self, cx, cy, rx, ry, **kw):
        c = self.p(cx, cy)
        return ("ellipse", dict(cx=c[0], cy=c[1], rx=rx * self.k, ry=ry * self.k, **kw))

    def rect(self, x, y, w, h, rx=None, **kw):
        if self.mirror:
            x = -(x + w)
            a = (self.ox + self.k * x, self.oy + self.k * y)
        else:
            a = self.p(x, y)
        d = dict(x=a[0], y=a[1], width=w * self.k, height=h * self.k, **kw)
        if rx:
            d["rx"] = rx * self.k
        return ("rect", d)

    def path(self, cmds, **kw):
        """cmds: list of tuples in local coordinates, absolute only:
        ('M', x, y) ('L', x, y) ('A', r, large, sweep, x, y) ('E', rx, ry, rot, large, sweep, x, y)
        ('Q', cx, cy, x, y) ('C', x1, y1, x2, y2, x, y) ('Z',)."""
        out = []
        for c in cmds:
            t = c[0]
            if t in ("M", "L"):
                X, Y = self.p(c[1], c[2])
                out.append(f"{t}{f(X)} {f(Y)}")
            elif t == "A":
                r, large, sweep, x, y = c[1:]
                if self.mirror:
                    sweep = 1 - sweep
                X, Y = self.p(x, y)
                R = r * self.k
                out.append(f"A{f(R)} {f(R)} 0 {large} {sweep} {f(X)} {f(Y)}")
            elif t == "E":
                rx, ry, rot, large, sweep, x, y = c[1:]
                if self.mirror:
                    sweep = 1 - sweep
                    rot = -rot
                X, Y = self.p(x, y)
                out.append(f"A{f(rx * self.k)} {f(ry * self.k)} {f(rot)} {large} {sweep} {f(X)} {f(Y)}")
            elif t == "Q":
                A, B = self.p(c[1], c[2]), self.p(c[3], c[4])
                out.append(f"Q{f(A[0])} {f(A[1])} {f(B[0])} {f(B[1])}")
            elif t == "C":
                A, B, D = self.p(c[1], c[2]), self.p(c[3], c[4]), self.p(c[5], c[6])
                out.append(f"C{f(A[0])} {f(A[1])} {f(B[0])} {f(B[1])} {f(D[0])} {f(D[1])}")
            elif t == "Z":
                out.append("Z")
            else:
                raise ValueError(t)
        return ("path", dict(d=" ".join(out), **kw))


def person(pen, x, y, k=1.0, h=26.5):
    """A Civic Line person, CL-005's listener: a hollow head (r 10.1) over
    open, round-cornered shoulders (43 wide, corner r 15.75), 8 apart on
    their center lines. (x, y) is the shoulders' foot at the center; k
    scales the figure, never the line. h is the shoulders' height at k 1."""
    q = pen.sub(x, y, k)
    w, rc, gap, hr = 43.0, 15.75, 8.0, 10.1
    top = -h
    shoulder = [("M", -w / 2, 0), ("L", -w / 2, top + rc), ("A", rc, 0, 1, -w / 2 + rc, top),
                ("L", w / 2 - rc, top), ("A", rc, 0, 1, w / 2, top + rc), ("L", w / 2, 0)]
    return [q.circle(0, top - gap - hr, hr), q.path(shoulder)]


def person_top(k=1.0, h=26.5):
    """Height from the shoulders' foot to the top of the head's line."""
    return k * (h + 8.0 + 2 * 10.1)


def source_svg(icon_id, groups, vb=(0, 0, 260, 220), masks=None):
    """The source file text in the masters' format."""
    lines = [f'<svg xmlns="http://www.w3.org/2000/svg" data-id="{icon_id}" viewBox="{f(vb[0])} {f(vb[1])} {f(vb[2])} {f(vb[3])}">']
    if masks:
        lines.append("  <defs>")
        for mid, els in masks.items():
            lines.append(f'    <mask id="{mid}">')
            for tag, a in els:
                lines.append("      <" + tag + " " + " ".join(f'{k.replace("_", "-")}="{f(v) if isinstance(v, (int, float)) else v}"' for k, v in a.items()) + "/>")
            lines.append("    </mask>")
        lines.append("  </defs>")
    for g in groups:
        role, els = g[0], g[1]
        extra = f' mask="url(#{g[2]})"' if len(g) > 2 and g[2] else ""
        lines.append(f'  <g data-role="{role}"{extra}>')
        for tag, a in els:
            attrs = " ".join(f'{"class" if k == "cls" else k.replace("_", "-")}="{f(v) if isinstance(v, (int, float)) else v}"'
                             for k, v in a.items())
            lines.append(f"    <{tag} {attrs}/>")
        lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def parse(icon_id, text):
    import xml.etree.ElementTree as ET
    vb = ET.fromstring(text).attrib["viewBox"].split()
    return cl_svg.parse_source(text, icon_id, vb[2], vb[3], {"id": icon_id, "corrections": []})


def ink_box(src):
    crop = cl_svg.emit(src, cl_svg.Mapping(), W, {"base": CHARCOAL, "accent": RED}, 10, 10,
                       f"0 0 {src.vb_w} {src.vb_h}", data_id=False, mask_prefix="m-")
    box, _ = cl_svg.drawn_bounds(crop)
    return box


def bake(src, cap=True):
    """DR-08 capped fit. Returns mapping dict with s, cx, cy, extent, stroke."""
    x0, y0, x1, y1 = ink_box(src)
    ext = max(x1 - x0, y1 - y0)
    s = min(FILL / ext, S_CAP) if cap else FILL / ext
    return {"s": s, "cx": (x0 + x1) / 2, "cy": (y0 + y1) / 2, "extent_px": ext,
            "w_px": x1 - x0, "h_px": y1 - y0, "stroke_units": W * s, "extent_units": ext * s,
            "at_cap": s >= S_CAP - 1e-9}


def export(src, mapping, root_stem, title, desc):
    """Red-black and black 128-unit strings, the black a color swap of the red-black."""
    M = cl_svg.Mapping(mapping["s"], mapping["cx"], mapping["cy"], 64.0, 64.0)
    rid = root_stem + "-red-black"
    rb = cl_svg.emit(src, M, W, {"base": CHARCOAL, "accent": RED}, 128, 128, "0 0 128 128",
                     root_id=rid, title=title, desc=desc, mask_prefix=rid + "-", group_prefix=rid + "-")
    rb = '<?xml version="1.0" encoding="UTF-8"?>\n' + rb
    bk = rb.replace(RED, CHARCOAL).replace(rid, root_stem + "-black")
    return rb, bk


def render(jobs, tmp):
    """jobs: [{svg, w, h, bg, out}] rendered by the masters' Chromium renderer."""
    os.makedirs(tmp, exist_ok=True)
    jf = os.path.join(tmp, "render-jobs.json")
    with open(jf, "w", encoding="utf-8") as fh:
        json.dump(jobs, fh)
    subprocess.run(["node", os.path.join(CL_SCRIPTS, "render_svgs.js"), jf], check=True)


def sized(svg_text, px):
    """The same SVG drawn at px by px."""
    body = svg_text.split("?>", 1)[-1].strip()
    return body.replace('width="128" height="128"', f'width="{px}" height="{px}"', 1)
