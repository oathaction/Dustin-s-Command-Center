"""Civic Line source format: parse, validate, bake and emit.

A source file `src/<ID>.svg` draws one icon in crop pixel coordinates so it
overlays the reference crop. The build bakes the uniform affine
X = s * (x - cx) + 64, Y = s * (y - cy) + 64 into every coordinate and emits
the 128-unit exports. See the tracer guide for the format in prose.
"""
import math
import re
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr

import cl_common as C

SVG_NS = "http://www.w3.org/2000/svg"
NS = "{" + SVG_NS + "}"

GEOM_ATTRS = {
    "path": {"d"},
    "line": {"x1", "y1", "x2", "y2"},
    "polyline": {"points"},
    "polygon": {"points"},
    "circle": {"cx", "cy", "r"},
    "ellipse": {"cx", "cy", "rx", "ry"},
    "rect": {"x", "y", "width", "height", "rx", "ry"},
}
REQUIRED = {
    "path": {"d"}, "line": {"x1", "y1", "x2", "y2"}, "polyline": {"points"}, "polygon": {"points"},
    "circle": {"cx", "cy", "r"}, "ellipse": {"cx", "cy", "rx", "ry"}, "rect": {"x", "y", "width", "height"},
}
COMMON_ATTRS = {"class", "id", "data-w", "data-note", "mask"}
FILL_RULE_OK = {"path", "polygon"}
CLASSES = {"fill", "fill-stroke", "miter", "butt"}
ROLES = {"base", "accent"}
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
URL_RE = re.compile(r"^url\(#([A-Za-z][A-Za-z0-9_-]*)\)$")
NUM_RE = re.compile(r"[+-]?(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?")
CMD_ARGS = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


class SourceError(Exception):
    pass


# ------------------------------------------------------------------ numbers

def fmt(v, nd=4):
    """Compact number: nd decimals (4 by default), no trailing zeros, no '-0'."""
    s = f"{v:.{nd}f}".rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s


def parse_number(s, what):
    try:
        v = float(s)
    except (TypeError, ValueError):
        raise SourceError(f"{what}: '{s}' is not a number")
    if not math.isfinite(v):
        raise SourceError(f"{what}: '{s}' is not finite")
    return v


def parse_points(s, what):
    nums = NUM_RE.findall(s or "")
    rest = NUM_RE.sub(" ", s or "").replace(",", " ").strip()
    if rest:
        raise SourceError(f"{what}: stray characters '{rest}' in points")
    if len(nums) < 4 or len(nums) % 2:
        raise SourceError(f"{what}: points needs an even count of at least 4 numbers, got {len(nums)}")
    v = [float(n) for n in nums]
    return list(zip(v[0::2], v[1::2]))


# ------------------------------------------------------------------ path data

def tokenize_path(d, what):
    """Split path data into commands with numeric argument lists. Arc flags may
    be written without separators (a5 5 0 011 1)."""
    i, n = 0, len(d)
    out = []
    cmd = None
    args = []

    def skip():
        nonlocal i
        while i < n and (d[i].isspace() or d[i] == ","):
            i += 1

    def flush():
        if cmd is None:
            return
        k = CMD_ARGS[cmd.upper()]
        if k == 0:
            if args:
                raise SourceError(f"{what}: '{cmd}' takes no arguments")
            out.append((cmd, []))
            return
        if not args or len(args) % k:
            raise SourceError(f"{what}: '{cmd}' needs a multiple of {k} numbers, got {len(args)}")
        for j in range(0, len(args), k):
            c = cmd
            if j > 0 and cmd in "Mm":
                c = "L" if cmd == "M" else "l"  # implicit lineto after moveto
            out.append((c, args[j:j + k]))

    while True:
        skip()
        if i >= n:
            break
        ch = d[i]
        if ch.isalpha():
            if ch.upper() not in CMD_ARGS:
                raise SourceError(f"{what}: unknown path command '{ch}'")
            flush()
            cmd, args = ch, []
            i += 1
            continue
        if cmd is None:
            raise SourceError(f"{what}: path data must start with a command")
        k = CMD_ARGS[cmd.upper()]
        if k == 0:
            raise SourceError(f"{what}: number after '{cmd}'")
        pos = len(args) % k
        if cmd.upper() == "A" and pos in (3, 4):
            if d[i] not in "01":
                raise SourceError(f"{what}: arc flag must be 0 or 1, got '{d[i]}'")
            args.append(float(d[i]))
            i += 1
            continue
        m = NUM_RE.match(d, i)
        if not m:
            raise SourceError(f"{what}: cannot read '{d[i:i + 12]}'")
        args.append(float(m.group(0)))
        i = m.end()
    flush()
    if not out:
        raise SourceError(f"{what}: empty path")
    if out[0][0] not in "Mm":
        raise SourceError(f"{what}: path must start with M or m")
    return out


ND = 4      # decimals for exported coordinates and lengths (0.0001 unit = 0.0002 source px)
ND_R = 6    # decimals for arc radii


def _half_chord(p0, p1, rx, ry, phi):
    """Half the chord from p0 to p1 in the frame where the ellipse is a circle of radius rx."""
    c, s = math.cos(math.radians(phi)), math.sin(math.radians(phi))
    dx, dy = (p1[0] - p0[0]) / 2.0, (p1[1] - p0[1]) / 2.0
    x1, y1 = c * dx + s * dy, -s * dx + c * dy
    return math.hypot(x1, y1 * rx / ry)


def arc_radii(p0, p1, rx, ry, phi, S, q0, q1):
    """Output radii for an arc whose source runs p0 -> p1 and whose output, as a
    renderer reads the rounded numbers, runs q0 -> q1.

    An arc's centre sits off its chord by d = sqrt(r^2 - h^2), which is very
    sensitive to rounding when h is close to r: a half circle whose rounded
    chord comes out a hair shorter than its diameter gets its centre pushed
    off the chord, and the arc shifts by up to a pixel. So the exporter keeps
    the centre, not the radius: it measures d in the source and writes
    r = sqrt(h_out^2 + (s d)^2) for the rounded chord. A source half circle
    (d = 0, including radii a renderer would scale up) gets r rounded down to
    at most half its chord, so renderers draw an exact half circle."""
    rx, ry = abs(rx), abs(ry)
    if rx == 0 or ry == 0:
        return round(rx * S, ND_R), round(ry * S, ND_R)
    h = _half_chord(p0, p1, rx, ry, phi)
    if h == 0:
        return round(rx * S, ND_R), round(ry * S, ND_R)
    ho = _half_chord(q0, q1, rx, ry, phi)
    if h >= rx * (1 - 1e-12):
        r = math.floor(ho * 10 ** ND_R) / 10 ** ND_R
    else:
        d = math.sqrt(rx * rx - h * h) * S
        r = round(math.sqrt(ho * ho + d * d), ND_R)
    return r, round(r * ry / rx, ND_R)


def transform_path(segs, X, Y, S):
    """Bake the affine into path segments and round the output.

    Absolute coordinates go through X/Y, relative ones are scaled by S. A
    leading 'm' is absolute by the SVG rules. The function tracks the current
    point twice: in the source, and in the output as a renderer accumulates
    the rounded numbers, so arc radii can be fitted to the chord the renderer
    will actually see (see arc_radii). Arc rotation and flags stay."""
    q = lambda v: round(v, ND)  # noqa: E731
    out = []
    sx = sy = ox = oy = 0.0           # current point: source, output
    ssx = ssy = osx = osy = 0.0       # subpath start: source, output
    for idx, (c, a) in enumerate(segs):
        u = c.upper()
        rel = c.islower() and not (idx == 0 and c == "m")
        if u == "Z":
            out.append((c, []))
            sx, sy, ox, oy = ssx, ssy, osx, osy
            continue
        if u in "HV":
            if rel:
                v = q(a[0] * S)
                ns, no = (sx + a[0], ox + v) if u == "H" else (sy + a[0], oy + v)
            else:
                v = q(X(a[0]) if u == "H" else Y(a[0]))
                ns, no = a[0], v
            if u == "H":
                sx, ox = ns, no
            else:
                sy, oy = ns, no
            out.append((c, [v]))
            continue
        if u == "A":
            rx, ry, rot, la, sw, x, y = a
            if rel:
                ex, ey = q(x * S), q(y * S)
                tsx, tsy, tox, toy = sx + x, sy + y, ox + ex, oy + ey
            else:
                ex, ey = q(X(x)), q(Y(y))
                tsx, tsy, tox, toy = x, y, ex, ey
            rxo, ryo = arc_radii((sx, sy), (tsx, tsy), rx, ry, rot, S, (ox, oy), (tox, toy))
            out.append((c, [rxo, ryo, rot, la, sw, ex, ey]))
            sx, sy, ox, oy = tsx, tsy, tox, toy
            continue
        b = []
        for j in range(0, len(a), 2):
            if rel:
                b += [q(a[j] * S), q(a[j + 1] * S)]
            else:
                b += [q(X(a[j])), q(Y(a[j + 1]))]
        if rel:
            sx, sy, ox, oy = sx + a[-2], sy + a[-1], ox + b[-2], oy + b[-1]
        else:
            sx, sy, ox, oy = a[-2], a[-1], b[-2], b[-1]
        if u == "M":
            ssx, ssy, osx, osy = sx, sy, ox, oy
        out.append((c, b))
    return out


def path_string(segs):
    parts = []
    for c, a in segs:
        if c.upper() == "A":
            rx, ry, rot, la, sw, x, y = a
            parts.append(f"{c}{fmt(rx, ND_R)} {fmt(ry, ND_R)} {fmt(rot)} {int(la)} {int(sw)} {fmt(x)} {fmt(y)}")
        elif a:
            parts.append(c + " ".join(fmt(v) for v in a))
        else:
            parts.append(c)
    return " ".join(parts)


def flatten_path(segs, steps=24):
    """Absolute polylines (one per subpath) approximating the path, for bounds."""
    polys = []
    cur = []
    x = y = sx = sy = 0.0
    lc = None  # last control point for S/T
    prev = None
    for c, a in segs:
        u = c.upper()
        rel = c.islower()
        ox, oy = (x, y) if rel else (0.0, 0.0)
        if u == "M":
            if cur:
                polys.append(cur)
            x, y = a[0] + ox, a[1] + oy
            sx, sy = x, y
            cur = [(x, y)]
            lc = None
        elif u == "L":
            x, y = a[0] + ox, a[1] + oy
            cur.append((x, y))
            lc = None
        elif u == "H":
            x = a[0] + (x if rel else 0.0)
            cur.append((x, y))
            lc = None
        elif u == "V":
            y = a[0] + (y if rel else 0.0)
            cur.append((x, y))
            lc = None
        elif u in "CS":
            if u == "C":
                x1, y1, x2, y2, ex, ey = a[0] + ox, a[1] + oy, a[2] + ox, a[3] + oy, a[4] + ox, a[5] + oy
            else:
                if prev in "CS" and lc:
                    x1, y1 = 2 * x - lc[0], 2 * y - lc[1]
                else:
                    x1, y1 = x, y
                x2, y2, ex, ey = a[0] + ox, a[1] + oy, a[2] + ox, a[3] + oy
            for k in range(1, steps + 1):
                t = k / steps
                mt = 1 - t
                cur.append((mt ** 3 * x + 3 * mt * mt * t * x1 + 3 * mt * t * t * x2 + t ** 3 * ex,
                            mt ** 3 * y + 3 * mt * mt * t * y1 + 3 * mt * t * t * y2 + t ** 3 * ey))
            lc = (x2, y2)
            x, y = ex, ey
        elif u in "QT":
            if u == "Q":
                x1, y1, ex, ey = a[0] + ox, a[1] + oy, a[2] + ox, a[3] + oy
            else:
                if prev in "QT" and lc:
                    x1, y1 = 2 * x - lc[0], 2 * y - lc[1]
                else:
                    x1, y1 = x, y
                ex, ey = a[0] + ox, a[1] + oy
            for k in range(1, steps + 1):
                t = k / steps
                mt = 1 - t
                cur.append((mt * mt * x + 2 * mt * t * x1 + t * t * ex, mt * mt * y + 2 * mt * t * y1 + t * t * ey))
            lc = (x1, y1)
            x, y = ex, ey
        elif u == "A":
            rx, ry, rot, la, sw, ex, ey = a
            ex, ey = ex + ox, ey + oy
            cur += arc_points(x, y, rx, ry, rot, la, sw, ex, ey, steps)
            x, y = ex, ey
            lc = None
        elif u == "Z":
            cur.append((sx, sy))
            polys.append(cur)
            cur = [(sx, sy)]
            x, y = sx, sy
            lc = None
        prev = u
    if len(cur) > 1:
        polys.append(cur)
    return polys


def arc_points(x1, y1, rx, ry, phi_deg, fa, fs, x2, y2, steps):
    """Sample an SVG elliptical arc (endpoint parameterisation, SVG 1.1 F.6)."""
    if rx == 0 or ry == 0 or (x1 == x2 and y1 == y2):
        return [(x2, y2)]
    rx, ry = abs(rx), abs(ry)
    phi = math.radians(phi_deg)
    cp, sp = math.cos(phi), math.sin(phi)
    dx, dy = (x1 - x2) / 2, (y1 - y2) / 2
    x1p, y1p = cp * dx + sp * dy, -sp * dx + cp * dy
    lam = (x1p / rx) ** 2 + (y1p / ry) ** 2
    if lam > 1:
        rx, ry = rx * math.sqrt(lam), ry * math.sqrt(lam)
    num = rx * rx * ry * ry - rx * rx * y1p * y1p - ry * ry * x1p * x1p
    den = rx * rx * y1p * y1p + ry * ry * x1p * x1p
    coef = math.sqrt(max(0.0, num / den)) if den else 0.0
    if bool(fa) == bool(fs):
        coef = -coef
    cxp, cyp = coef * rx * y1p / ry, -coef * ry * x1p / rx
    cx = cp * cxp - sp * cyp + (x1 + x2) / 2
    cy = sp * cxp + cp * cyp + (y1 + y2) / 2

    def ang(ux, uy, vx, vy):
        a = math.atan2(ux * vy - uy * vx, ux * vx + uy * vy)
        return a

    t1 = ang(1, 0, (x1p - cxp) / rx, (y1p - cyp) / ry)
    dt = ang((x1p - cxp) / rx, (y1p - cyp) / ry, (-x1p - cxp) / rx, (-y1p - cyp) / ry)
    if not fs and dt > 0:
        dt -= 2 * math.pi
    elif fs and dt < 0:
        dt += 2 * math.pi
    pts = []
    for k in range(1, steps + 1):
        t = t1 + dt * k / steps
        pts.append((cx + rx * math.cos(t) * cp - ry * math.sin(t) * sp, cy + rx * math.cos(t) * sp + ry * math.sin(t) * cp))
    return pts


# ------------------------------------------------------------------ model

class Elem:
    def __init__(self, tag, geom, classes, w_override, eid, fill_rule, mask, note, keep=False, raw_segs=None):
        self.tag = tag
        self.geom = geom          # dict of parsed geometry
        self.classes = classes
        self.w = w_override       # source px or None
        self.id = eid
        self.fill_rule = fill_rule
        self.mask = mask
        self.note = note
        self.keep = keep          # inside a mask: paint white instead of black
        self.segs = raw_segs

    @property
    def kind(self):
        if "fill" in self.classes:
            return "fill"
        if "fill-stroke" in self.classes:
            return "fill-stroke"
        return "stroke"


class Group:
    def __init__(self, role, mask, elems):
        self.role = role
        self.mask = mask
        self.elems = elems


class Source:
    def __init__(self, icon_id, vb_w, vb_h, groups, masks, corrections):
        self.id = icon_id
        self.vb_w = vb_w
        self.vb_h = vb_h
        self.groups = groups
        self.masks = masks        # id -> [Elem]
        self.corrections = corrections


def _strip(tag):
    return tag[len(NS):] if tag.startswith(NS) else tag


def parse_element(el, where, errors, in_mask=False):
    tag = _strip(el.tag)
    if tag not in GEOM_ATTRS:
        errors.append(f"{where}: <{tag}> is not allowed (allowed: {', '.join(sorted(GEOM_ATTRS))})")
        return None
    allowed = GEOM_ATTRS[tag] | COMMON_ATTRS | ({"fill-rule"} if tag in FILL_RULE_OK else set()) | ({"data-mask"} if in_mask else set())
    for k in el.attrib:
        if k not in allowed:
            hint = ""
            if k in ("transform",):
                hint = " (transforms are not supported; write the final coordinates)"
            elif k in ("fill", "stroke", "stroke-width", "style", "color", "opacity", "fill-opacity", "stroke-opacity",
                       "stroke-linecap", "stroke-linejoin"):
                hint = " (colors and stroke style come from the group role and the class; use class or data-w)"
            errors.append(f"{where}: attribute '{k}' is not allowed on <{tag}>{hint}")
    missing = REQUIRED[tag] - set(el.attrib)
    if missing:
        errors.append(f"{where}: <{tag}> is missing {', '.join(sorted(missing))}")
        return None
    if len(el):
        errors.append(f"{where}: <{tag}> must not have child elements")
    if (el.text or "").strip():
        errors.append(f"{where}: <{tag}> must not contain text")
    eid = el.attrib.get("id")
    if eid is not None and not ID_RE.match(eid):
        errors.append(f"{where}: id '{eid}' must start with a letter and use letters, digits, '-' or '_'")
    w = f"{where} <{tag}{' id=' + eid if eid else ''}>"
    classes = set((el.attrib.get("class") or "").split())
    bad = classes - CLASSES
    if bad:
        errors.append(f"{w}: unknown class {', '.join(sorted(bad))} (allowed: {', '.join(sorted(CLASSES))})")
    if "fill" in classes and "fill-stroke" in classes:
        errors.append(f"{w}: use either 'fill' or 'fill-stroke', not both")
    if "fill" in classes and (classes & {"miter", "butt"}):
        errors.append(f"{w}: 'miter' and 'butt' describe a stroke; a 'fill' element has none")
    fill_rule = el.attrib.get("fill-rule")
    if fill_rule is not None:
        if fill_rule not in ("evenodd", "nonzero"):
            errors.append(f"{w}: fill-rule must be evenodd or nonzero")
        if not (classes & {"fill", "fill-stroke"}):
            errors.append(f"{w}: fill-rule only applies to a 'fill' or 'fill-stroke' element")
    wv = None
    if "data-w" in el.attrib:
        try:
            wv = parse_number(el.attrib["data-w"], f"{w} data-w")
            if wv <= 0:
                errors.append(f"{w}: data-w must be positive")
        except SourceError as e:
            errors.append(str(e))
        if "fill" in classes:
            errors.append(f"{w}: data-w sets a stroke width; a 'fill' element has no stroke")
        if not eid:
            errors.append(f"{w}: an element with data-w needs an id so the corrections log can name it")
    mask = None
    if "mask" in el.attrib:
        m = URL_RE.match(el.attrib["mask"])
        if not m:
            errors.append(f"{w}: mask must be url(#id)")
        else:
            mask = m.group(1)
        if in_mask:
            errors.append(f"{w}: elements inside a mask cannot carry their own mask")
    keep = False
    if in_mask and "data-mask" in el.attrib:
        if el.attrib["data-mask"] not in ("cut", "keep"):
            errors.append(f"{w}: data-mask must be cut or keep")
        keep = el.attrib["data-mask"] == "keep"
    geom = {}
    segs = None
    try:
        if tag == "path":
            segs = tokenize_path(el.attrib["d"], w)
        elif tag in ("polyline", "polygon"):
            geom["points"] = parse_points(el.attrib["points"], w)
        else:
            for k in GEOM_ATTRS[tag]:
                if k in el.attrib:
                    geom[k] = parse_number(el.attrib[k], f"{w} {k}")
            for k in ("r", "rx", "ry", "width", "height"):
                if k in geom and geom[k] < 0:
                    errors.append(f"{w}: {k} must not be negative")
            if tag == "circle" and geom.get("r", 1) == 0:
                errors.append(f"{w}: r is zero")
            if tag == "rect" and (geom.get("width", 1) == 0 or geom.get("height", 1) == 0):
                errors.append(f"{w}: zero-size rect")
    except SourceError as e:
        errors.append(str(e))
        return None
    return Elem(tag, geom, classes, wv, eid, fill_rule, mask, el.attrib.get("data-note"), keep, segs)


def parse_source(svg_text, icon_id, crop_w, crop_h, corrections):
    errors = []
    try:
        root = ET.fromstring(svg_text)
    except ET.ParseError as e:
        raise SourceError(f"{icon_id}: XML parse error: {e}")
    if root.tag != NS + "svg":
        raise SourceError(f"{icon_id}: root must be <svg xmlns=\"{SVG_NS}\">, got {root.tag}")
    allowed_root = {"viewBox", "data-id", "width", "height"}
    for k in root.attrib:
        if k not in allowed_root:
            errors.append(f"root: attribute '{k}' is not allowed (allowed: viewBox, data-id)")
    if root.attrib.get("data-id") != icon_id:
        errors.append(f"root: data-id must be '{icon_id}', got '{root.attrib.get('data-id')}'")
    vb = root.attrib.get("viewBox", "")
    want = f"0 0 {crop_w} {crop_h}"
    if " ".join(vb.replace(",", " ").split()) != want:
        errors.append(f"root: viewBox must be '{want}' (the crop size), got '{vb}'")
    for k in ("width", "height"):
        if k in root.attrib:
            exp = crop_w if k == "width" else crop_h
            if root.attrib[k] != str(exp):
                errors.append(f"root: {k} may be omitted or set to {exp}")
    groups = []
    masks = {}
    seen_ids = set()
    for i, child in enumerate(root):
        tag = _strip(child.tag)
        where = f"root child {i + 1} <{tag}>"
        if tag in ("title", "desc"):
            continue
        if tag == "defs":
            if groups:
                errors.append(f"{where}: <defs> must come before the groups")
            for j, m in enumerate(child):
                mt = _strip(m.tag)
                if mt != "mask":
                    errors.append(f"{where} child {j + 1}: only <mask> is allowed in <defs>, got <{mt}>")
                    continue
                mid = m.attrib.get("id")
                extra = set(m.attrib) - {"id"}
                if extra:
                    errors.append(f"mask '{mid}': attributes {', '.join(sorted(extra))} are not allowed; the build sets the mask region")
                if not mid or not ID_RE.match(mid):
                    errors.append(f"{where} child {j + 1}: <mask> needs a valid id")
                    continue
                if mid in masks or mid in seen_ids:
                    errors.append(f"mask id '{mid}' is used twice")
                elems = []
                for k, e in enumerate(m):
                    pe = parse_element(e, f"mask '{mid}' child {k + 1}", errors, in_mask=True)
                    if pe:
                        elems.append(pe)
                if not elems:
                    errors.append(f"mask '{mid}' is empty")
                masks[mid] = elems
                seen_ids.add(mid)
            continue
        if tag != "g":
            errors.append(f"{where}: only <defs>, <title>, <desc> and <g data-role> are allowed at the top level")
            continue
        role = child.attrib.get("data-role")
        if role not in ROLES:
            errors.append(f"{where}: data-role must be 'base' or 'accent', got '{role}'")
            continue
        extra = set(child.attrib) - {"data-role", "mask", "data-note"}
        if extra:
            errors.append(f"{where}: attributes {', '.join(sorted(extra))} are not allowed on a group")
        gmask = None
        if "mask" in child.attrib:
            m = URL_RE.match(child.attrib["mask"])
            if not m:
                errors.append(f"{where}: mask must be url(#id)")
            else:
                gmask = m.group(1)
        elems = []
        for k, e in enumerate(child):
            if _strip(e.tag) == "g":
                errors.append(f"{where} child {k + 1}: groups cannot nest; start a new top-level group instead")
                continue
            pe = parse_element(e, f"{where} ({role}) child {k + 1}", errors)
            if pe:
                if pe.id:
                    if pe.id in seen_ids:
                        errors.append(f"id '{pe.id}' is used twice")
                    seen_ids.add(pe.id)
                elems.append(pe)
        if not elems:
            errors.append(f"{where}: empty group")
        groups.append(Group(role, gmask, elems))
    if not groups:
        errors.append("no <g data-role> groups")
    used = {g.mask for g in groups if g.mask} | {e.mask for g in groups for e in g.elems if e.mask}
    for u in sorted(used):
        if u not in masks:
            errors.append(f"mask '#{u}' is referenced but not defined in <defs>")
    for mid in masks:
        if mid not in used:
            errors.append(f"mask '{mid}' is defined but never used")
    # corrections log
    if corrections is None:
        errors.append(f"corrections log src/{icon_id}.json is missing")
        corrections = {"corrections": []}
    else:
        if corrections.get("id") != icon_id:
            errors.append(f"src/{icon_id}.json: 'id' must be '{icon_id}'")
        cl = corrections.get("corrections")
        if not isinstance(cl, list):
            errors.append(f"src/{icon_id}.json: 'corrections' must be a list")
            cl = []
        for n, c in enumerate(cl):
            if not isinstance(c, dict) or not isinstance(c.get("what"), str) or not isinstance(c.get("why"), str) \
                    or not c["what"].strip() or not c["why"].strip():
                errors.append(f"src/{icon_id}.json: correction {n + 1} needs non-empty 'what' and 'why' strings")
        named = {c.get("element") for c in cl if isinstance(c, dict)}
        for g in groups:
            for e in g.elems:
                if e.w is not None and e.id and e.id not in named:
                    errors.append(f"element '{e.id}' sets data-w but src/{icon_id}.json has no correction with \"element\": \"{e.id}\"")
        for elems in masks.values():
            for e in elems:
                if e.w is not None and e.id and e.id not in named:
                    errors.append(f"mask element '{e.id}' sets data-w but has no correction entry naming it")
    if errors:
        raise SourceError(f"{icon_id}: {len(errors)} problem(s)\n  - " + "\n  - ".join(errors))
    return Source(icon_id, crop_w, crop_h, groups, masks, corrections)


# ------------------------------------------------------------------ emit

class Mapping:
    """Coordinate mapping used when emitting: identity (crop space) or the bake."""

    def __init__(self, s=1.0, cx=0.0, cy=0.0, ox=0.0, oy=0.0):
        self.s, self.cx, self.cy, self.ox, self.oy = s, cx, cy, ox, oy

    @classmethod
    def bake(cls, t):
        return cls(t["s"], t["cx"], t["cy"], 64.0, 64.0)

    def X(self, x):
        return self.s * (x - self.cx) + self.ox

    def Y(self, y):
        return self.s * (y - self.cy) + self.oy


def elem_geometry(e, M):
    """Mapped geometry attributes for one element, as (name, value) pairs."""
    X, Y, S = M.X, M.Y, M.s
    g = e.geom
    if e.tag == "path":
        return [("d", path_string(transform_path(e.segs, X, Y, S)))]
    if e.tag in ("polyline", "polygon"):
        return [("points", " ".join(f"{fmt(X(x))},{fmt(Y(y))}" for x, y in g["points"]))]
    if e.tag == "line":
        return [("x1", fmt(X(g["x1"]))), ("y1", fmt(Y(g["y1"]))), ("x2", fmt(X(g["x2"]))), ("y2", fmt(Y(g["y2"])))]
    if e.tag == "circle":
        return [("cx", fmt(X(g["cx"]))), ("cy", fmt(Y(g["cy"]))), ("r", fmt(g["r"] * S))]
    if e.tag == "ellipse":
        return [("cx", fmt(X(g["cx"]))), ("cy", fmt(Y(g["cy"]))), ("rx", fmt(g["rx"] * S)), ("ry", fmt(g["ry"] * S))]
    if e.tag == "rect":
        out = [("x", fmt(X(g["x"]))), ("y", fmt(Y(g["y"]))), ("width", fmt(g["width"] * S)), ("height", fmt(g["height"] * S))]
        if "rx" in g:
            out.append(("rx", fmt(g["rx"] * S)))
        if "ry" in g:
            out.append(("ry", fmt(g["ry"] * S)))
        return out
    raise AssertionError(e.tag)


def elem_paint(e, color, width):
    k = e.kind
    out = []
    if k == "fill":
        out.append(("fill", color))
    elif k == "fill-stroke":
        out += [("fill", color), ("stroke", color), ("stroke-width", fmt4(width))]
    else:
        out += [("fill", "none"), ("stroke", color), ("stroke-width", fmt4(width))]
    if k != "fill":
        out.append(("stroke-linecap", "butt" if "butt" in e.classes else "round"))
        out.append(("stroke-linejoin", "miter" if "miter" in e.classes else "round"))
    if e.fill_rule:
        out.append(("fill-rule", e.fill_rule))
    return out


def fmt4(v):
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return s or "0"


def emit(src, M, W, colors, width_px, height_px, viewbox, root_id=None, title=None, desc=None,
         data_id=True, mask_prefix=""):
    """Serialise the source with mapping M. colors = {'base': hex, 'accent': hex}.
    W is the stroke width in source px; it is scaled by M.s."""
    lines = []
    attrs = [("xmlns", SVG_NS)]
    if root_id:
        attrs.append(("id", root_id))
    if data_id:
        attrs.append(("data-id", src.id))
    attrs += [("width", fmt(width_px)), ("height", fmt(height_px)), ("viewBox", viewbox)]
    lines.append("<svg " + " ".join(f"{k}={quoteattr(v)}" for k, v in attrs) + ">")
    if title:
        lines.append(f"  <title>{escape(title)}</title>")
    if desc:
        lines.append(f"  <desc>{escape(desc)}</desc>")
    vb = [float(v) for v in viewbox.split()]
    mids = {}
    if src.masks:
        lines.append("  <defs>")
        for mid, elems in src.masks.items():
            out_id = f"{mask_prefix}{mid}"
            mids[mid] = out_id
            # The mask region is the whole canvas in user space, so thin or
            # zero-height elements are never clipped by a bounding-box region.
            region = [("x", fmt(vb[0])), ("y", fmt(vb[1])), ("width", fmt(vb[2])), ("height", fmt(vb[3]))]
            lines.append(f"    <mask id={quoteattr(out_id)} maskUnits=\"userSpaceOnUse\" "
                         + " ".join(f"{k}={quoteattr(v)}" for k, v in region) + ">")
            lines.append("      <rect " + " ".join(f"{k}={quoteattr(v)}" for k, v in region) + " fill=\"#FFFFFF\"/>")
            for e in elems:
                col = "#FFFFFF" if e.keep else "#000000"
                w = (e.w if e.w is not None else W) * M.s
                a = elem_geometry(e, M) + elem_paint(e, col, w)
                lines.append(f"      <{e.tag} " + " ".join(f"{k}={quoteattr(v)}" for k, v in a) + "/>")
            lines.append("    </mask>")
        lines.append("  </defs>")
    counts = {r: sum(1 for g in src.groups if g.role == r) for r in ROLES}
    seen = {r: 0 for r in ROLES}
    for g in src.groups:
        seen[g.role] += 1
        gid = g.role if counts[g.role] == 1 else f"{g.role}-{seen[g.role]}"
        ga = [("id", gid)]
        if g.mask:
            ga.append(("mask", f"url(#{mids[g.mask]})"))
        lines.append("  <g " + " ".join(f"{k}={quoteattr(v)}" for k, v in ga) + ">")
        for e in g.elems:
            w = (e.w if e.w is not None else W) * M.s
            a = elem_geometry(e, M) + elem_paint(e, colors[g.role], w)
            if e.mask:
                a.append(("mask", f"url(#{mids[e.mask]})"))
            lines.append(f"    <{e.tag} " + " ".join(f"{k}={quoteattr(v)}" for k, v in a) + "/>")
        lines.append("  </g>")
    lines.append("</svg>")
    return "\n".join(lines) + "\n"


def export_pair(src, inv_row, W):
    """Red-black and black export strings from one in-memory serialisation.
    The black string is the red-black string with Pillar Red swapped for
    Charcoal, so the pair is identical byte for byte after the swap."""
    M = Mapping.bake(inv_row["transform"])
    title = inv_row["label"]
    desc = (f"Oath & Action Civic Line {src.id} {inv_row['label']}. Traced vector reconstruction from the Civic Line "
            f"reference sheet {inv_row['sheet']}, row {inv_row['row']}, column {inv_row['column']}. "
            f"Group 'base' is the main drawing; group 'accent' holds the accent parts named in the catalogue.")
    rid = "oa-civic-line-" + src.id.lower()
    rb = emit(src, M, W, {"base": C.CHARCOAL, "accent": C.PILLAR_RED}, 128, 128, "0 0 128 128",
              root_id=rid, title=title, desc=desc, mask_prefix=src.id.lower() + "-")
    rb = '<?xml version="1.0" encoding="UTF-8"?>\n' + rb
    bk = rb.replace(C.PILLAR_RED, C.CHARCOAL)
    return rb, bk


def crop_space_svg(src, W, colors, z=1):
    """Render-ready SVG in crop coordinates at z times the crop size."""
    return emit(src, Mapping(), W, colors, src.vb_w * z, src.vb_h * z, f"0 0 {src.vb_w} {src.vb_h}",
                data_id=False, mask_prefix="m-")


def export_at_crop_scale(export_svg, inv_row, z=1):
    """Re-frame a baked export so its viewBox covers the crop again: the bake check."""
    t = inv_row["transform"]
    s = t["s"]
    x0 = 64 - s * t["cx"]
    y0 = 64 - s * t["cy"]
    w, h = inv_row["crop"]["w"], inv_row["crop"]["h"]
    body = export_svg.split("?>", 1)[-1] if export_svg.startswith("<?xml") else export_svg
    body = re.sub(r'width="128" height="128" viewBox="0 0 128 128"',
                  f'width="{w * z}" height="{h * z}" viewBox="{x0:.6f} {y0:.6f} {w * s:.6f} {h * s:.6f}"', body, count=1)
    return body


# ------------------------------------------------------------------ bounds of an emitted file

def _shape_polys(tag, a):
    """Absolute polylines for an emitted element's attributes; closed flags."""
    f = lambda k, d=0.0: float(a.get(k, d))  # noqa: E731
    if tag == "path":
        segs = tokenize_path(a["d"], "export")
        polys = flatten_path(segs)
        closed = [len(p) > 2 and p[0] == p[-1] for p in polys]
        return polys, closed
    if tag in ("polyline", "polygon"):
        pts = parse_points(a["points"], "export")
        if tag == "polygon":
            pts = pts + [pts[0]]
        return [pts], [tag == "polygon"]
    if tag == "line":
        return [[(f("x1"), f("y1")), (f("x2"), f("y2"))]], [False]
    if tag in ("circle", "ellipse"):
        cx, cy = f("cx"), f("cy")
        rx = f("r") if tag == "circle" else f("rx")
        ry = f("r") if tag == "circle" else f("ry")
        pts = [(cx + rx * math.cos(2 * math.pi * k / 96), cy + ry * math.sin(2 * math.pi * k / 96)) for k in range(97)]
        return [pts], [True]
    if tag == "rect":
        x, y, w, h = f("x"), f("y"), f("width"), f("height")
        return [[(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]], [True]
    return [], []


def _miter_tips(poly, closed, h, limit=4.0):
    tips = []
    pts = poly[:-1] if closed else poly
    n = len(pts)
    if n < 3 and not closed:
        return tips
    rng = range(n) if closed else range(1, n - 1)
    for i in rng:
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        ax, ay = p0[0] - p1[0], p0[1] - p1[1]
        bx, by = p2[0] - p1[0], p2[1] - p1[1]
        la, lb = math.hypot(ax, ay), math.hypot(bx, by)
        if la < 1e-9 or lb < 1e-9:
            continue
        ax, ay, bx, by = ax / la, ay / la, bx / lb, by / lb
        cosang = max(-1.0, min(1.0, ax * bx + ay * by))
        theta = math.acos(cosang)
        if theta < 1e-6 or abs(theta - math.pi) < 1e-6:
            continue
        ml = 1.0 / math.sin(theta / 2)
        if ml > limit:
            continue
        dx, dy = -(ax + bx), -(ay + by)
        dl = math.hypot(dx, dy)
        if dl < 1e-12:
            continue
        tips.append((p1[0] + dx / dl * h * ml, p1[1] + dy / dl * h * ml))
    return tips


def drawn_bounds(svg_text):
    """Bounds of everything an emitted SVG paints outside <defs>: geometry plus
    half the stroke, with miter tips where joins are miters. Returns
    (x0, y0, x1, y1) or None, plus a list of per-element boxes."""
    root = ET.fromstring(svg_text.encode("utf-8") if isinstance(svg_text, str) else svg_text)
    boxes = []

    def walk(node, in_defs=False):
        for ch in node:
            t = _strip(ch.tag)
            if t == "defs":
                continue
            if t == "g":
                walk(ch)
                continue
            if t not in GEOM_ATTRS:
                continue
            a = ch.attrib
            stroked = a.get("stroke", "none") != "none"
            h = float(a.get("stroke-width", "1")) / 2 if stroked else 0.0
            polys, closed = _shape_polys(t, a)
            xs, ys = [], []
            for p, c in zip(polys, closed):
                for x, y in p:
                    xs += [x - h, x + h]
                    ys += [y - h, y + h]
                if stroked and a.get("stroke-linejoin") == "miter":
                    for x, y in _miter_tips(p, c, h):
                        xs.append(x)
                        ys.append(y)
            if xs:
                boxes.append((t, a.get("id"), min(xs), min(ys), max(xs), max(ys)))

    walk(root)
    if not boxes:
        return None, []
    return (min(b[2] for b in boxes), min(b[3] for b in boxes), max(b[4] for b in boxes), max(b[5] for b in boxes)), boxes
