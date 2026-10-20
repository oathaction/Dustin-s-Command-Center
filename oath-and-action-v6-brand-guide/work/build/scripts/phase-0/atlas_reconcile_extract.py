#!/usr/bin/env python3
"""Phase 0 atlas reconciliation, step 1: extract and compare.

Reads (never writes) the prepared extracts and the Concepts V2 source file,
finds every Atlas identifier and the signs, grades, delays and labels shown
near it, and compares each against work/extract/atlas-v7-data.json.

Sources scanned
  V5 Polished   chapters/11-data.html, chapters/16-atlas-system.html,
                the four SVG figures of the Atlas System chapter, and
                chapters/15-standards.html (only for the rule numbers R1 to R9)
  Atlas Visual System   every chapters/*.html and every images/*.svg
  Concepts V2   source/20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html,
                split into its 25 sections, HTML text plus inline SVG text,
                with the 118 Register link glyphs decoded (sign and texture)

Output
  work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json

Run with:  python3 -I atlas_reconcile_extract.py
"""
import collections
import html
import json
import os
import re
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
X = os.path.join(ROOT, "work", "extract")
V7_PATH = os.path.join(X, "atlas-v7-data.json")
CV2_SRC = os.path.join(ROOT, "source", "20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html")
OUT = os.path.join(ROOT, "work", "handoffs", "phase-0", "20261020_Atlas-Reconciliation-Data.json")


def rel(p):
    return os.path.relpath(p, ROOT)


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------- V7 model
V7 = json.loads(read(V7_PATH))
NODES, LINKS, LOOPS, REFORMS = V7["nodes"], V7["links"], V7["loops"], V7["reforms"]
ROUTES = {r["code"]: r for r in V7["routes"]["items"]}
ISSUES = V7["issues"]
DOMAINS = {d["id"]: d for d in V7["domains"]}
CLAIMS = V7["claims"]
REPAIR = {r["id"]: r for r in V7["repairLog"]["rows"]}
DELIVERY = {r["id"]: r for r in V7["deliveryLog"]["rows"]}
FAMILIES = V7["outcomes"]["families"]

GRADE_WORDS = [  # order matters: longer, more specific first
    (r"plausible[_ ,]+contested|disputed", "plausible_contested"),
    (r"well[- _]supported|strong evidence", "well-supported"),
    (r"documented|on the record", "documented"),
    (r"hypothes[ie]s|hypothesized|hypothetical|untested", "hypothesis"),
    (r"plausible|some evidence", "plausible"),
    (r"\bcontested\b", "contested"),
]
DELAY_WORDS = [
    (r"under 2 (?:yrs|years)", "S"),
    (r"2 (?:to|–|-) ?10 (?:yrs|years)", "M"),
    (r"over 10 (?:yrs|years)", "L"),
]
DELAY_CODE = [
    (r"(?:^|\s)([SML]) ·", 1),
    (r"delay ([SML])\b", 1),
    (r"[+−-] / ([SML])\b", 1),
]


def norm(s):
    s = html.unescape(s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("−", "-").replace("–", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def grade_of(text):
    """Return the grade named first in the text (earliest position wins)."""
    t = norm(text)
    best = None
    for pat, g in GRADE_WORDS:
        m = re.search(pat, t)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), g)
    return best[1] if best else None


def delay_of(text):
    t = norm(text)
    best = None
    for pat, d in DELAY_WORDS:
        m = re.search(pat, t)
        if m and (best is None or m.start() < best[0]):
            best = (m.start(), d)
    if best:
        return best[1]
    raw = html.unescape(text)
    for pat, grp in DELAY_CODE:
        m = re.search(pat, raw)
        if m:
            return m.group(grp)
    return None


# ------------------------------------------------- identifier classification
LOOP_IDS = set(LOOPS)
NODE_IDS = set(NODES)
LINK_IDS = set(LINKS)
REFORM_IDS = set(REFORMS)
ISSUE_IDS = set(ISSUES)
DOMAIN_IDS = set(DOMAINS)

ID_RE = re.compile(
    r"(?<![A-Za-z0-9\-.])("
    r"R-\d{2}|CL\d{4}|RL\d{2}|DL\d{2}|LTR\d|EC\d{1,2}|TC\d{1,2}|LX\d|LE\d{2}|LT\d{2}|L\d{2}|L##|"
    r"T\d{2}|R\d{1,2}[ab]?|B\d{1,2}a?|[ACE]\d{1,2}|D\d{1,2}|X\d{1,2}|I\d{3}"
    r")(?![A-Za-z0-9])"
)
ROUTE_RE = re.compile(r"(?<![A-Za-z0-9])(LOC|SS|BI|FS|FR|FA|ENF|CRT|AV|IC|CIV)(?![A-Za-z0-9])")
EFFECT_RE = re.compile(r"\b(DQ|GE|EP|EQ)\s*([+\-−]?[LMS]|0|\?)(?![A-Za-z0-9])")


def kinds_of(tok, standards_doc=False):
    k = []
    if tok in NODE_IDS:
        k.append("variable")
    if tok in LINK_IDS:
        k.append("connection")
    if tok in LOOP_IDS:
        k.append("loop")
    if tok in REFORM_IDS:
        k.append("reform")
    if tok in ISSUE_IDS:
        k.append("issue")
    if tok in DOMAIN_IDS:
        k.append("domain")
    if tok in CLAIMS:
        k.append("claim")
    if tok in REPAIR:
        k.append("repair-log row")
    if tok in DELIVERY:
        k.append("delivery-log row")
    if tok in {r["id"] for r in V7["rejectedLinks"]}:
        k.append("rejected connection")
    if standards_doc and re.fullmatch(r"R[1-9]", tok):
        k.append("standards rule")
    if tok == "L##":
        k.append("placeholder")
    return k


# ------------------------------------------------------------ HTML to lines
BLOCK = {"div", "p", "li", "tr", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "figcaption",
         "figure", "section", "header", "footer", "table", "thead", "tbody", "dt", "dd", "caption",
         "br", "text", "title", "desc", "button", "a", "label", "summary", "dl", "ul", "ol", "img"}
HEAD = {"h1", "h2", "h3", "h4", "figcaption", "caption", "title"}


class Lines(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines, self.cur, self.skip = [], [], 0
        self.svg, self.head, self.headlevel = 0, 0, []

    def flush(self):
        t = re.sub(r"\s+", " ", "".join(self.cur)).strip()
        if t:
            self.lines.append({"t": t, "svg": self.svg > 0, "head": self.head > 0})
        self.cur = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("style", "script"):
            self.skip += 1
            return
        if tag == "svg":
            self.svg += 1
        if tag in BLOCK:
            self.flush()
        else:
            self.cur.append(" ")
        if tag in HEAD:
            self.head += 1
        for key in ("alt", "aria-label"):
            if a.get(key) and tag in ("img", "svg", "figure"):
                self.lines.append({"t": "[" + key + "] " + a[key], "svg": False, "head": False})

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in ("style", "script"):
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip = max(0, self.skip - 1)
            return
        if tag in BLOCK:
            self.flush()
        else:
            self.cur.append(" ")
        if tag in HEAD:
            self.head = max(0, self.head - 1)
        if tag == "svg":
            self.svg = max(0, self.svg - 1)

    def handle_data(self, data):
        if not self.skip:
            self.cur.append(data)


def to_lines(fragment):
    fragment = re.sub(r"data:[^\"')\s]+", "[data]", fragment)
    p = Lines()
    p.feed(fragment)
    p.flush()
    return p.lines


# Concepts V2 Register glyphs: 50 x 14 SVGs drawn beside every connection.
def decode_glyph(body):
    if re.search(r'<line x1="46"', body):
        end = "bar (lowers)"
    elif re.search(r"L41\.5 10\.4 L37 7 L41\.5 3\.6 Z", body):
        end = "open diamond (decides)"
    elif re.search(r"L38 10\.6 L38 3\.4 Z", body):
        end = "arrowhead (raises)"
    else:
        end = "unknown"
    dash = re.search(r'stroke-dasharray="([^"]+)"', body)
    tex = {None: "solid", "8 6": "dashed", "0.1 4.4": "dotted", "10 4 2 4": "dash-dot"}.get(
        dash.group(1) if dash else None, "other")
    col = re.search(r'stroke="(#[0-9A-Fa-f]{6})" stroke-width="1.7"', body)
    return end, tex, (col.group(1).upper() if col else None)


def glyph_token(m):
    end, tex, col = decode_glyph(m.group(0))
    return '<div>[[glyph end="%s" texture="%s" color="%s"]]</div>' % (end, tex, col)


# ------------------------------------------------------------- documents
DOCS = []


def add_doc(group, path, location, fragment, standards=False):
    DOCS.append({"group": group, "file": rel(path), "location": location,
                 "lines": to_lines(fragment), "standards": standards})


v5 = os.path.join(X, "v5-polished")
for ch in ("11-data", "16-atlas-system"):
    p = os.path.join(v5, "chapters", ch + ".html")
    add_doc("V5 Polished", p, "chapter " + ch, read(p))
for img, fig in (("cc6e26ddee", "figure 1 (relationship grammar)"), ("4722932495", "figure 2 (loop R1)"),
                 ("e44e256497", "figure 3 (loop R16)"), ("0164ea8408", "figure 4 (reform R-28)")):
    p = os.path.join(v5, "images", img + ".svg")
    add_doc("V5 Polished", p, "chapter 16-atlas-system, " + fig, read(p))
p = os.path.join(v5, "chapters", "15-standards.html")
add_doc("V5 Polished", p, "chapter 15-standards", read(p), standards=True)

avs = os.path.join(X, "atlas-visual-system")
avs_img_chapter = {}
for f in sorted(os.listdir(os.path.join(avs, "chapters"))):
    p = os.path.join(avs, "chapters", f)
    frag = read(p)
    for im in re.findall(r"\[\[data-uri:([^\]]+)\]\]", frag):
        avs_img_chapter.setdefault(im, f[:-5])
    add_doc("Atlas Visual System", p, "chapter " + f[:-5], frag)
for f in sorted(os.listdir(os.path.join(avs, "images"))):
    if f.endswith(".svg"):
        p = os.path.join(avs, "images", f)
        add_doc("Atlas Visual System", p,
                "image in chapter " + avs_img_chapter.get(f, "(sprite or unreferenced)"), read(p))

CV2_HTML = read(CV2_SRC)
CV2_STARTS = [m.start() for m in re.finditer(r'<section class="pg"', CV2_HTML)] + [len(CV2_HTML)]
CV2_SECTIONS = []
for n in range(len(CV2_STARTS) - 1):
    frag = CV2_HTML[CV2_STARTS[n]:CV2_STARTS[n + 1]]
    CV2_SECTIONS.append(frag)
    frag2 = re.sub(r'<svg width="50" height="14"[^>]*>.*?</svg>', glyph_token, frag, flags=re.S)
    title = re.search(r"Atlas concept (\d\d) / ([^<]+)", html.unescape(frag).replace("\xa0", " ").replace("  ", " "))
    loc = "section %02d" % n + (" (Concept %s %s)" % (title.group(1), title.group(2).strip()) if title else
                               " (cover and comparison)")
    add_doc("Concepts V2", CV2_SRC, loc, frag2)

# --------------------------------------------------------- occurrence scan
occ = []
for di, d in enumerate(DOCS):
    sub = ""
    for li, ln in enumerate(d["lines"]):
        t = ln["t"]
        if ln["head"] or re.match(r"^(Sheet \d\d of 13|INTO [A-Z]+\d+|[A-E] [A-Z][a-z]|Atlas concept)", t):
            sub = t[:70]
        for m in ID_RE.finditer(t):
            tok = m.group(1)
            if d["standards"] and not re.fullmatch(r"R[1-9]", tok):
                continue
            k = kinds_of(tok, d["standards"])
            occ.append({"doc": di, "line": li, "id": tok, "kinds": k, "sub": sub,
                        "text": t, "pos": m.start()})
        if not d["standards"]:
            for m in ROUTE_RE.finditer(t):
                if d["group"] == "Concepts V2" or "route" in norm(t):
                    occ.append({"doc": di, "line": li, "id": m.group(1), "kinds": ["route"], "sub": sub,
                                "text": t, "pos": m.start()})
            for m in EFFECT_RE.finditer(t):
                occ.append({"doc": di, "line": li, "id": m.group(0), "kinds": ["effect code"], "sub": sub,
                            "text": t, "pos": m.start()})

FINDINGS = []


def finding(doc, line, item, shown, v7, typ, note, auto=True):
    d = DOCS[doc] if isinstance(doc, int) else doc
    FINDINGS.append({"file": d["file"], "location": d["location"] + (("; " + line) if line else ""),
                     "item": item, "shown": shown, "v7": v7, "type": typ, "note": note})


def window(di, li, n=7, stop_kind=None):
    lines = DOCS[di]["lines"]
    out = [lines[li]["t"]]
    for j in range(li + 1, min(len(lines), li + n)):
        t = lines[j]["t"]
        if stop_kind and any(stop_kind in kinds_of(m.group(1)) for m in ID_RE.finditer(t)):
            break
        out.append(t)
    return out


# ---------------------------------------------- generic per-occurrence checks
checked = collections.Counter()
status = {}  # occurrence index -> "match" | "conflict" | "ambiguous" | "unverified"
for i, o in enumerate(occ):
    tok, k = o["id"], o["kinds"]
    if k == ["route"] or k == ["effect code"]:
        continue
    checked["identifier occurrences"] += 1
    if not k:
        status[i] = "conflict"
        finding(o["doc"], o["sub"], tok, o["text"][:160], "no such identifier in V7", "ID",
                "identifier not found in V7")
        continue
    status.setdefault(i, "match")

# connection attributes in windows
for i, o in enumerate(occ):
    if "connection" not in o["kinds"]:
        continue
    L = LINKS[o["id"]]
    lines = DOCS[o["doc"]]["lines"]
    t = o["text"]
    LEGEND = re.compile(r"^(Signs:|Delays:|DELAYS IN|S under|M 2|L over|\[alt\])")
    if len(t) <= 70 and not LEGEND.match(t):
        parts = [t]  # short label line: attributes may sit before or after the ID
        for j in range(o["line"] + 1, min(len(lines), o["line"] + 7)):
            u = lines[j]["t"]
            if len(u) > 70 or LEGEND.match(u) or any("connection" in kinds_of(m.group(1)) for m in ID_RE.finditer(u)):
                break
            parts.append(u)
    else:
        # prose: only the clause that holds the ID, from the ID onward
        rest = t[o["pos"]:]
        nxt = ID_RE.search(rest, len(o["id"]))
        rest = rest[:nxt.start()] if nxt and "connection" in kinds_of(nxt.group(1)) else rest
        parts = [re.split(r";|\. ", rest)[0]]
    blob = " \n ".join(parts)
    g = grade_of(blob)
    dl = delay_of(blob)
    shown = []
    conflict = []
    if g:
        shown.append("grade " + g)
        if g != L["evidence"] and not (g == "contested" and L["contested"]):
            conflict.append(("grade", g, L["evidence"]))
    if dl:
        shown.append("delay " + dl)
        if dl != L["delay"]:
            conflict.append(("delay", dl, L["delay"]))
    gm = re.search(r'\[\[glyph end="([^"]+)" texture="([^"]+)"', blob)
    if gm:
        sign = {"arrowhead (raises)": "+", "bar (lowers)": "-", "open diamond (decides)": None}.get(gm.group(1))
        shown.append("glyph " + gm.group(1) + ", " + gm.group(2))
        if sign != L["polarity"]:
            conflict.append(("sign", gm.group(1), L["polarity"]))
        tex_expect = {"documented": "solid", "well-supported": "solid", "plausible": "dashed",
                      "plausible_contested": "dash-dot", "hypothesis": "dotted"}[L["evidence"]]
        if gm.group(2) != tex_expect:
            conflict.append(("encoding", gm.group(2), tex_expect + " for " + L["evidence"]))
    o["shown"] = "; ".join(shown)
    for typ, s, v in conflict:
        status[i] = "conflict"
        finding(o["doc"], o["sub"], o["id"], s, str(v), typ, "connection attribute in context: " + blob[:200])

# "A to B through Lnn positive" and "EC7 income to EC8 assets positive through LE24" patterns
VAR = r"\b([A-Z]{1,2}\d{1,2})(?: [a-z][a-z ,']*?)?"
PAIR1 = re.compile(VAR + r" to " + VAR + r" through ([A-Z]{1,2}\d{2}|LX\d) (positive|negative)")
PAIR2 = re.compile(VAR + r" to " + VAR + r" (positive|negative) through ([A-Z]{1,2}\d{2}|LX\d)")
PAIR3 = re.compile(r"^(L\d\d|LE\d\d|LT\d\d|T\d\d|LX\d)$")
for di, d in enumerate(DOCS):
    for li, ln in enumerate(d["lines"]):
        t = html.unescape(ln["t"])
        hits = [(a, b, l, s) for a, b, l, s in PAIR1.findall(t)] + [(a, b, l, s) for a, b, s, l in PAIR2.findall(t)]
        for a, b, l, s in hits:
            if l not in LINKS:
                continue
            L = LINKS[l]
            pol = "+" if s == "positive" else "-"
            checked["from-to-sign statements"] += 1
            if (a, b) != (L["from"], L["to"]):
                finding(di, "", l, "%s to %s" % (a, b), "%s to %s" % (L["from"], L["to"]), "structure",
                        "direction statement: " + t[:160])
            if pol != L["polarity"]:
                finding(di, "", l, s, str(L["polarity"]), "sign", "sign statement: " + t[:160])
        # AVS production table rows: L01 / A1 -> B1 / + / S / well-supported
        if PAIR3.match(t) and li + 3 < len(d["lines"]):
            nx = [d["lines"][li + j]["t"] for j in (1, 2, 3)]
            m = re.match(r"([A-Z]{1,2}\d{1,2}) → ([A-Z]{1,2}\d{1,2})$", nx[0])
            m2 = re.match(r"([+\-−]) / ([SML])$", nx[1])
            if m and m2 and t in LINKS:
                L = LINKS[t]
                checked["table rows (link, from-to, sign, delay, grade)"] += 1
                sgn = "-" if m2.group(1) in "-−" else "+"
                for typ, s, v in (("structure", "%s to %s" % m.groups(), "%s to %s" % (L["from"], L["to"])),
                                  ("sign", sgn, L["polarity"]), ("delay", m2.group(2), L["delay"]),
                                  ("grade", grade_of(nx[2]), L["evidence"])):
                    if s != v:
                        finding(di, "production table", t, s, v, typ, "table row")

# link names shown without IDs, followed by grade and delay
NAME2LINK = collections.defaultdict(list)
for k, L in LINKS.items():
    NAME2LINK[norm(L["name"])].append(k)
name_hits = 0
for di, d in enumerate(DOCS):
    lines = d["lines"]
    for li, ln in enumerate(lines):
        n = norm(re.sub(r"\.$", "", ln["t"]))
        for nm, ks in NAME2LINK.items():
            if n == nm or n.startswith(nm + ",") or n.startswith(nm + " ·") or n.startswith(nm + ", and"):
                L = LINKS[ks[0]]
                nearby = " ".join(x["t"] for x in lines[li:li + 3])
                if any(x in nearby for x in ks):
                    continue  # already covered by the ID check
                g, dl = grade_of(nearby), delay_of(nearby)
                name_hits += 1
                checked["link names shown without their ID"] += 1
                if g and g != L["evidence"]:
                    finding(di, "", ks[0] + " (by name)", g, L["evidence"], "grade", "named link: " + nearby[:160])
                if dl and dl != L["delay"]:
                    finding(di, "", ks[0] + " (by name)", dl, L["delay"], "delay", "named link: " + nearby[:160])

# ---------------------------------------------- variable labels next to IDs
VAR_LABELS = collections.defaultdict(lambda: collections.Counter())
for i, o in enumerate(occ):
    if "variable" not in o["kinds"]:
        continue
    lines = DOCS[o["doc"]]["lines"]
    t = html.unescape(o["text"])
    after = t[o["pos"] + len(o["id"]):].strip(" :·,")
    label = None
    if re.match(r"^(VARIABLE|Variable|OUTSIDE DRIVER|MEASURE OF VARIABLE|INTO)\s", t) and not after:
        label = lines[o["line"] + 1]["t"] if o["line"] + 1 < len(lines) else None
    elif after and not ID_RE.match(after) and len(after) > 3 and not re.match(r"^(to|through|and|income|costs|assets)\b", after):
        label = re.split(r"\s+D\d\d$|\s+(?:EC|TC)$", after)[0]
    elif not after and o["line"] + 1 < len(lines):
        nxt = lines[o["line"] + 1]["t"]
        if not ID_RE.match(nxt) and len(nxt) < 60 and not grade_of(nxt):
            label = nxt
    if label:
        label = re.sub(r"\s+(D\d\d|EC|TC)$", "", label).strip()
        if len(label) < 70 and not label.startswith("[["):
            VAR_LABELS[o["id"]][(label, DOCS[o["doc"]]["group"])] += 1

# ------------------------------------------- ambiguity: colliding identifiers
def meaning(o):
    """Classify a colliding token by its context: variable, loop, reform, rule, or bare."""
    t = html.unescape(o["text"])
    before = t[max(0, o["pos"] - 22):o["pos"]].lower()
    after = norm(t[o["pos"] + len(o["id"]):])
    lines = DOCS[o["doc"]]["lines"]
    nxt = norm(lines[o["line"] + 1]["t"]) if o["line"] + 1 < len(lines) else ""
    prv = norm(lines[o["line"] - 1]["t"]) if o["line"] > 0 else ""
    tok = o["id"]
    if "standards rule" in o["kinds"]:
        return "standards rule"
    if re.search(r"loop\s*$|loops\s*$|loops .*$", before) or prv.endswith(("loop", "loops")):
        return "loop (typed)"
    if re.search(r"variable\s*$|variables .*$", before):
        return "variable (typed)"
    if tok in LOOPS:
        lt = norm(LOOPS[tok]["title"])
        if after.startswith(lt[:25]) or nxt.startswith(lt[:25]) or nxt.startswith(("snowball", "thermostat",
                                                                                     "reinforcing", "balancing")):
            return "loop (by title)"
    if tok in NODES:
        vt = norm(NODES[tok]["title"])
        labels = [norm(l) for (l, g) in VAR_LABELS.get(tok, {})]
        if after.startswith(vt[:18]) or nxt.startswith(vt[:18]) or any(after.startswith(l[:14]) or nxt.startswith(l[:14]) for l in labels if l):
            return "variable (by label)"
    return "bare"


COLLIDE_VL = {"B2", "B3", "B4", "B5"}
page_coll = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
for i, o in enumerate(occ):
    tok = o["id"]
    if tok in COLLIDE_VL:
        page_coll[o["doc"]]["B2-B5"][(tok, meaning(o))] += 1
    if re.fullmatch(r"R\d{1,2}[ab]?", tok) and ("loop" in o["kinds"] or "standards rule" in o["kinds"]):
        page_coll[o["doc"]]["R-number"][(tok, meaning(o))] += 1
    if re.fullmatch(r"R-\d\d", tok):
        page_coll[o["doc"]]["R-number"][(tok, "reform")] += 1
    if re.fullmatch(r"D\d", tok) and "variable" in o["kinds"]:
        page_coll[o["doc"]]["D-number"][(tok, "variable")] += 1
    if re.fullmatch(r"D\d\d", tok):
        page_coll[o["doc"]]["D-number"][(tok, "domain")] += 1
    if re.fullmatch(r"X\d\d", tok):
        page_coll[o["doc"]]["X-number"][(tok, "issue")] += 1
    if re.fullmatch(r"X\d", tok):
        page_coll[o["doc"]]["X-number"][(tok, "variable")] += 1
    if tok in ("B1a", "R1b", "R4a", "R4b"):
        page_coll[o["doc"]]["suffixed loop"][(tok, "loop")] += 1
    if tok in ("B1", "R1", "R4"):
        page_coll[o["doc"]]["suffixed loop"][(tok, "variable" if tok == "B1" else "loop or rule")] += 1

COLLISIONS = []
for di, groups in page_coll.items():
    for g, c in groups.items():
        meanings = collections.Counter()
        for (tok, mn), n in c.items():
            meanings[mn.split(" ")[0]] += n
        bare = sum(n for (tok, mn), n in c.items() if mn == "bare")
        kinds = set(mn.split(" ")[0] for (tok, mn) in c)
        flag = False
        if g == "B2-B5" and (len(kinds) > 1 or bare):
            flag = True
        if g == "R-number" and len(kinds) > 1:
            flag = True
        if g in ("D-number", "X-number") and len(kinds) > 1:
            flag = True
        if g == "suffixed loop" and len(c) > 1 and any(t in ("B1a", "R1b", "R4a", "R4b") for t, _ in c):
            flag = True
        if flag:
            COLLISIONS.append({"file": DOCS[di]["file"], "location": DOCS[di]["location"], "group": g,
                               "tokens": {"%s as %s" % k: v for k, v in sorted(c.items())}, "bare": bare})

# V5 Polished is one document: the Standards rules R1 to R9 and the atlas chapter's loops share it
std_rules = sorted({o["id"] for o in occ if "standards rule" in o["kinds"]})
v5_loops = sorted({o["id"] for o in occ if DOCS[o["doc"]]["group"] == "V5 Polished" and "loop" in o["kinds"]
                   and not DOCS[o["doc"]]["standards"]})

def lead_code(c):
    c = c.replace("−", "-")
    m = re.match(r"^\s*([+\-]?[LMS]|0|\?)", c)
    return m.group(1) if m else c


# ---------------------------------------------- structured: Concepts V2 Register
REG = {"rows": [], "vars": [], "sheets": [], "reforms": []}
SHEET_TITLE = {k: v["title"] for k, v in DOMAINS.items()}
SHEET_TITLE["EC"] = V7["layers"]["economy"]["title"]
SHEET_TITLE["TC"] = V7["layers"]["technology"]["title"]
DOM_SHEET = {}
for k, n in NODES.items():
    DOM_SHEET[k] = n["domain"].split("/")[0] if n["domain"] else n["cluster"]


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


ROW_RE = re.compile(
    r'<div style="display: grid; grid-template-columns: 52px 282px 54px[^"]*"><div[^>]*><span[^>]*>([A-Z]+\d+)</span></div>'
    r'<div[^>]*><span[^>]*><span[^>]*>([A-Z]+\d+)</span></span><span>(.*?)</span></div>'
    r'<div[^>]*><span[^>]*>(<svg.*?</svg>)</span></div><div[^>]*>(.*?)</div><div[^>]*>(.*?)</div><div[^>]*>(.*?)</div></div>',
    re.S)
INTO_RE = re.compile(r'>INTO ([A-Z]+\d+)</span>')
for sn in range(13, 25):
    frag = CV2_SECTIONS[sn]
    sheet = re.search(r"Sheet (\d\d) of 13", frag).group(1)
    code = "?"
    for cm in re.finditer(r'>(D\d\d|EC|TC)</div><div[^>]*>([^<]+)</div>', frag):
        ttl = html.unescape(cm.group(2)).strip()
        if ttl == SHEET_TITLE.get(cm.group(1)):
            code = cm.group(1)
            break
    loc = DOCS[next(i for i, d in enumerate(DOCS) if d["location"].startswith("section %02d" % sn))]["location"]
    intos = [(m.start(), m.group(1)) for m in INTO_RE.finditer(frag)]
    for m in ROW_RE.finditer(frag):
        lid, frm, from_label, svg, name, ev, dl = m.groups()
        into = [v for p, v in intos if p < m.start()]
        into = into[-1] if into else None
        end, tex, col = decode_glyph(svg)
        from_label = strip_tags(from_label)
        dom = re.search(r"\s(D\d\d|EC|TC)$", from_label)
        row = {"sheet": sheet, "code": code, "loc": loc, "id": lid, "from": frm, "to": into,
               "from_label": re.sub(r"\s(D\d\d|EC|TC)$", "", from_label), "from_sheet_shown": dom.group(1) if dom else None,
               "glyph": end, "texture": tex, "color": col, "name": strip_tags(name), "grade": strip_tags(ev),
               "delay": strip_tags(dl)}
        REG["rows"].append(row)
        L = LINKS.get(lid)
        checked["Register connection rows"] += 1
        if not L:
            finding(DOCS[-1] | {"location": loc}, "", lid, "row", "no such connection", "ID", "")
            continue
        exp_sign = {"+": "arrowhead (raises)", "-": "bar (lowers)", None: "open diamond (decides)"}[L["polarity"]]
        exp_tex = {"documented": "solid", "well-supported": "solid", "plausible": "dashed",
                   "plausible_contested": "dash-dot", "hypothesis": "dotted"}[L["evidence"]]
        chk = [("structure", "%s to %s" % (frm, into), "%s to %s" % (L["from"], L["to"])),
               ("sign", end, exp_sign), ("encoding", tex, exp_tex),
               ("grade", grade_of(row["grade"]), L["evidence"]), ("delay", delay_of(row["delay"]), L["delay"]),
               ("label", norm(row["name"]), norm(L["name"]))]
        exp_sheet = DOM_SHEET[L["to"]]
        if code != exp_sheet:
            chk.append(("structure", "filed on sheet " + code, "sheet of moved variable " + exp_sheet))
        fs = DOM_SHEET[frm]
        if row["from_sheet_shown"] and row["from_sheet_shown"] != fs:
            chk.append(("label", "from-variable sheet tag " + row["from_sheet_shown"], fs))
        for typ, s, v in chk:
            if s != v:
                finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s, INTO %s" % (sheet, into), lid, str(s),
                        str(v), typ, "Register row")
    # variable cards
    for m in re.finditer(r'font-variant-numeric:tabular-nums">([A-Z]+\d+)</span>&nbsp;&nbsp;<b[^>]*>(.*?)</b></div>'
                         r'<div[^>]*>(.*?)</div><div[^>]*>(.*?)</div>', frag, re.S):
        vid, title, higher, kind = m.group(1), strip_tags(m.group(2)), strip_tags(m.group(3)), strip_tags(m.group(4))
        if vid not in NODES:
            continue
        N = NODES[vid]
        checked["Register variable cards"] += 1
        REG["vars"].append({"sheet": sheet, "id": vid, "title": title, "higher": higher, "kind": kind})
        if norm(title) != norm(N["title"]):
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s, variable card" % sheet, vid, title,
                    N["title"], "label", "variable card title")
        exp_kind = {"stock": "Stock", "flow": "Flow", "auxiliary": "Condition", "driver": "Outside driver"}[N["type"]]
        if not kind.startswith(exp_kind):
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s, variable card" % sheet, vid, kind.split("·")[0].strip(),
                    N["type"] + " (" + N["kind_plain"][:60] + ")", "label", "variable type label")
        lp = re.search(r"Loops ([A-Za-z0-9, ]+?)(?: ·|$)", kind)
        shown_loops = set(x.strip() for x in lp.group(1).split(",")) if lp else set()
        v7_loops = {k for k, Lp in LOOPS.items() if vid in [c[0] for c in Lp["chain"]] or
                    any(vid in (LINKS[l]["from"], LINKS[l]["to"]) for l in Lp["links"])}
        v7_loops_closed = {k for k in v7_loops if LOOPS[k]["links"]}
        if shown_loops != v7_loops_closed:
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s, variable card" % sheet, vid,
                    ", ".join(sorted(shown_loops)) or "none", ", ".join(sorted(v7_loops_closed)) or "none",
                    "structure", "loops listed on variable card vs closed loops passing through the variable")
        also = re.search(r"Also under (D\d\d)", kind)
        doms = (N["domain"] or "").split("/")
        if also and (len(doms) < 2 or also.group(1) != doms[1]):
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s" % sheet, vid, "also under " + also.group(1),
                    N["domain"], "structure", "secondary domain")
        if norm(higher).replace("higher means", "a higher value means") not in norm(N["increase_means"]) and \
                norm(higher)[12:40] not in norm(N["increase_means"]):
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s, variable card" % sheet, vid, higher,
                    N["increase_means"], "label", "increase_means wording differs")
    # reform rows and their route lists
    for m in re.finditer(r'>(R-\d\d)</span>.*?<div[^>]*>([^<]+)</div>(.*?)<svg', frag[frag.find("Reforms aimed here"):], re.S):
        rid, rtitle, rest = m.group(1), html.unescape(m.group(2)).strip(), m.group(3)
        codes = re.findall(r">(LOC|SS|BI|FS|FR|FA|ENF|CRT|AV|IC|CIV)<", rest)
        if rid not in REFORMS:
            continue
        R = REFORMS[rid]
        checked["Register reform rows"] += 1
        v7codes = [x["route"] for x in R["routes"]]
        REG["reforms"].append({"sheet": sheet, "id": rid, "title": rtitle, "routes": codes})
        if norm(rtitle) != norm(R["title"]):
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s" % sheet, rid, rtitle, R["title"], "label",
                    "reform title")
        cells = re.search(r'<svg width="84" height="17"[^>]*>(.*?)</svg>', frag[frag.find("Reforms aimed here") + m.end() - 4:], re.S)
        if cells:
            body = cells.group(1)
            for fam, x0 in (("DQ", 0.5), ("GE", 21.5), ("EP", 42.5), ("EQ", 63.5)):
                fill = re.search(r'<rect x="%s" y="[\d.]+" width="16" height="([\d.]+)" fill="#' % x0, body)
                dot = re.search(r'<circle cx="%s"' % (x0 + 8), body)
                cost = re.search(r'<line x1="%s" y1="15"' % x0, body)
                shown = {"3.7": "+S", "7.3": "+M", "11": "+L"}.get(fill.group(1) if fill else None, "?" if dot else "0")
                v7c = R["effects"][fam]
                lc = lead_code(v7c)
                has_cost = bool(re.search(r"-[SM]", v7c.replace("−", "-")))
                checked["Register effect cells"] += 1
                if shown != lc or bool(cost) != has_cost:
                    finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s, effect cells" % sheet, rid + " " + fam,
                            shown + (" with cost bar" if cost else ""), v7c, "encoding", "effect cell")
        if codes and codes != v7codes:
            finding({"file": rel(CV2_SRC), "location": loc}, "Sheet %s" % sheet, rid, " ".join(codes),
                    " ".join(v7codes), "structure", "route list")

# sheet statistics
EV_WORD = {"documented": "on the record", "well-supported": "strong evidence", "plausible": "some evidence",
           "plausible_contested": "disputed", "hypothesis": "untested"}
sheet_stats = {}
for sn in range(13, 25):
    d = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section %02d" % sn))
    txt = "\n".join(x["t"] for x in DOCS[d]["lines"])
    ls = txt.split("\n")
    code = next(ls[j] for j in range(len(ls) - 1) if ls[j] in SHEET_TITLE and ls[j + 1] == SHEET_TITLE[ls[j]])
    nums = {}
    for lab, key in (("variables on this sheet", "variables"), ("connections filed here", "connections"),
                     ("closed loops pass through", "loops"), ("reforms aimed here", "reforms"),
                     ("issues tracked", "issues")):
        m = re.search(r"(\d+)\n" + lab, txt)
        nums[key] = int(m.group(1)) if m else None
    ev = re.search(r"Evidence on the connections filed here\n(?:\[\[[^\n]*\n)?([^\n]+)", txt)
    nums["evidence"] = ev.group(1) if ev else None
    leave = re.search(r"(\d+) connections? leaves? this sheet", txt)
    nums["leave"] = int(leave.group(1)) if leave else None
    sheet_stats[code] = (nums, DOCS[d]["location"])

vars_on = collections.defaultdict(list)
for k in NODES:
    vars_on[DOM_SHEET[k]].append(k)
filed = collections.defaultdict(list)
for k, L in LINKS.items():
    filed[DOM_SHEET[L["to"]]].append(k)
SHEET_COMPUTED = {}
for code, (nums, loc) in sheet_stats.items():
    vs = set(vars_on[code])
    lk = filed[code]
    loops_through = {lp for lp, Lp in LOOPS.items() if Lp["links"] and
                     any(LINKS[l]["from"] in vs or LINKS[l]["to"] in vs for l in Lp["links"])}
    reforms_aimed = {r for r, R in REFORMS.items() if not R["rejected"] and
                     any((t in vs) or (t in LINKS and LINKS[t]["to"] in vs) for t in R["targets"])}
    reforms_aimed2 = {r for r, R in REFORMS.items() if not R["rejected"] and
                      any((t in vs) or (t in LINKS and (LINKS[t]["to"] in vs or LINKS[t]["from"] in vs)) for t in R["targets"])}
    issues = len(DOMAINS[code]["issues"]) if code in DOMAINS else None
    evc = collections.Counter(LINKS[l]["evidence"] for l in lk)
    leaving = sum(1 for k, L in LINKS.items() if L["from"] in vs and DOM_SHEET[L["to"]] != code)
    comp = {"variables": len(vs), "connections": len(lk), "loops": len(loops_through),
            "reforms (targets into sheet)": len(reforms_aimed), "reforms (targets touching sheet)": len(reforms_aimed2),
            "issues": issues, "evidence": dict(evc), "leave": leaving,
            "reform_ids": sorted(reforms_aimed2), "loop_ids": sorted(loops_through)}
    SHEET_COMPUTED[code] = comp
    checked["Register sheet statistics"] += 1
    for key in ("variables", "connections", "loops", "issues", "leave"):
        if nums[key] is not None and comp[key] is not None and nums[key] != comp[key]:
            finding({"file": rel(CV2_SRC), "location": loc}, "sheet header", code + " " + key, str(nums[key]),
                    str(comp[key]), "structure", "sheet count")
    if nums["reforms"] not in (comp["reforms (targets into sheet)"], comp["reforms (targets touching sheet)"]):
        finding({"file": rel(CV2_SRC), "location": loc}, "sheet header", code + " reforms", str(nums["reforms"]),
                "%d (targets on the sheet) or %d (targets touching it)" % (comp["reforms (targets into sheet)"],
                                                                         comp["reforms (targets touching sheet)"]),
                "structure", "sheet count")
    if nums["evidence"]:
        shown = {}
        for n, w in re.findall(r"(\d+) ([a-z ]+?)(?: ·|$)", nums["evidence"]):
            shown[w.strip()] = int(n)
        exp = {EV_WORD[g]: n for g, n in evc.items()}
        if shown != exp:
            finding({"file": rel(CV2_SRC), "location": loc}, "evidence summary", code, nums["evidence"],
                    " · ".join("%d %s" % (n, w) for w, n in exp.items()), "grade", "sheet evidence mix")

# ---------------------------------------------- Concepts V2 Index sheet
idx = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 12"))
idx_lines = [x["t"] for x in DOCS[idx]["lines"]]
INDEX_ROWS = {}
for j, t in enumerate(idx_lines):
    if t in SHEET_TITLE and j + 1 < len(idx_lines) and idx_lines[j + 1] == SHEET_TITLE[t]:
        nums = []
        for k in range(j + 1, min(j + 12, len(idx_lines))):
            if re.fullmatch(r"\d+|–", idx_lines[k]):
                nums.append(idx_lines[k])
            if len(nums) == 5:
                break
        if len(nums) == 5 and t not in INDEX_ROWS:
            INDEX_ROWS[t] = nums
for code, nums in INDEX_ROWS.items():
    c = SHEET_COMPUTED.get(code)
    if not c:
        continue
    checked["Index sheet rows"] += 1
    exp = [str(c["variables"]), str(c["connections"]), str(c["loops"]), None, str(c["issues"]) if c["issues"] else "–"]
    labels = ["variables", "connections", "loops", "reforms", "issues"]
    for k in (0, 1, 2, 4):
        if nums[k] != exp[k]:
            finding(idx, "index table", code + " " + labels[k], nums[k], exp[k], "structure", "index count")
    sheet_n = sheet_stats[code][0]["reforms"]
    if nums[3] != str(sheet_n):
        finding(idx, "index table", code + " reforms", nums[3], "sheet says %s" % sheet_n, "structure", "index vs sheet")

# busiest crossings between sheets
cross = collections.Counter()
inside = collections.Counter()
for k, L in LINKS.items():
    a, b = DOM_SHEET[L["from"]], DOM_SHEET[L["to"]]
    if a == b:
        inside[a] += 1
    else:
        cross[(a, b)] += 1
for a, b, n in re.findall(r"(D\d\d|EC|TC) to (D\d\d|EC|TC), (\d+)", " ".join(idx_lines)):
    checked["Index busiest crossings"] += 1
    if cross[(a, b)] != int(n):
        finding(idx, "How the sheets connect", "%s to %s" % (a, b), n, str(cross[(a, b)]), "structure",
                "busiest crossing count")
top_cross = cross.most_common(8)

# ---------------------------------------------- Concepts V2 Field Guide (section 09)
fg = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 09"))
fl = [x["t"] for x in DOCS[fg]["lines"]]
FIELD = []
for j, t in enumerate(fl):
    if t in LOOPS and j + 2 < len(fl) and fl[j + 1] in ("Snowball loop", "Thermostat loop"):
        k = j - 1
        ring = []
        while k >= 0 and fl[k] in NODES:
            ring.insert(0, fl[k])
            k -= 1
        typ = "R" if fl[j + 1].startswith("Snowball") else "B"
        delay = delay_of(fl[j + 2])
        title = fl[j + 3]
        weak = next((x for x in fl[j + 4:j + 8] if x.startswith(("Weakest step", "Every step"))), "")
        now = re.search(r"Now: (.+)$", weak)
        LP = LOOPS[t]
        FIELD.append({"loop": t, "ring": ring, "type": typ, "delay": delay, "title": title, "weak": weak})
        checked["Field Guide specimens"] += 1
        chain = [c[0] for c in LP["chain"]]
        sub = "specimen " + t
        if typ != LP["type"]:
            finding(fg, sub, t, typ, LP["type"], "structure", "loop type")
        if delay != LP["delay"]:
            finding(fg, sub, t, delay, LP["delay"], "delay", "turn time")
        if norm(title) != norm(LP["title"]):
            finding(fg, sub, t, title, LP["title"], "label", "loop title")
        if ring != chain:
            finding(fg, sub, t, " ".join(ring), " ".join(chain), "structure", "ring order vs V7 chain")
        grades = [LINKS[l]["evidence"] for l in LP["links"]]
        rank = ["hypothesis", "plausible_contested", "plausible", "well-supported", "documented"]
        weakest = min(grades, key=lambda g: rank.index(g))
        wshown = grade_of(weak.split("Now:")[0])
        if weak.startswith("Every step"):
            if len(set(grades)) != 1 or grade_of(weak) != grades[0]:
                finding(fg, sub, t, weak.split("Now:")[0].strip(), ", ".join(grades), "grade", "every step claim")
        elif wshown != weakest:
            finding(fg, sub, t, weak.split("Now:")[0].strip(), "weakest graded step: " + weakest +
                    " (" + ", ".join("%s %s" % (l, LINKS[l]["evidence"]) for l in LP["links"]) + ")", "grade",
                    "weakest step")
        dirmap = {"running_up": "running and building", "running_down": "running and wearing down",
                  "running": "working", "unclear": "direction unclear", "dormant": "switched off in practice"}
        if now and dirmap.get(LP["direction"], LP["direction"]) != now.group(1):
            finding(fg, sub, t, now.group(1), LP["direction"], "label", "loop state")
# ring glyph check: count arrowheads and bars per specimen SVG against loop polarities
fg_frag = CV2_SECTIONS[9]
specimen_svgs = re.findall(r'<svg width="1600" height="2000"[^>]*>(.*?)</svg>', fg_frag, re.S)
FIELD_GLYPHS = []
for spec, svg in zip([f for f in FIELD], specimen_svgs):
    LP = LOOPS[spec["loop"]]
    arcs = re.findall(r'<path d="M[\d. ]+A44 44[^"]*" fill="none" stroke="(#[0-9A-F]+)" stroke-width="[\d.]+"'
                      r'(?: stroke-dasharray="([^"]+)")?', svg)
    heads = len(re.findall(r'<path d="M[\d.]+ [\d.]+ L[\d.]+ [\d.]+ L[\d.]+ [\d.]+ Z" fill="#', svg))
    bars = len(re.findall(r'<line [^>]*stroke-width="2\.[0-9]"', svg))
    pos = sum(1 for l in LP["links"] if LINKS[l]["polarity"] == "+")
    neg = sum(1 for l in LP["links"] if LINKS[l]["polarity"] == "-")
    dashes = collections.Counter(a[1] or "solid" for a in arcs)
    tex_name = {"solid": "solid", "8 6": "dashed", "0.1 5.2": "dotted", "0.1 4.4": "dotted", "10 4 2 4": "dash-dot"}
    shown_tex = collections.Counter(tex_name.get(k, k) for k in dashes.elements())
    exp_tex = collections.Counter({"documented": "solid", "well-supported": "solid", "plausible": "dashed",
                                   "plausible_contested": "dash-dot", "hypothesis": "dotted"}[LINKS[l]["evidence"]]
                                  for l in LP["links"])
    checked["Field Guide ring textures and end marks"] += 1
    if shown_tex != exp_tex:
        finding(fg, "specimen " + spec["loop"], spec["loop"], dict(shown_tex), dict(exp_tex), "encoding", "ring textures")
    if heads - 1 != pos or bars != neg:
        finding(fg, "specimen " + spec["loop"], spec["loop"], "%d arrowheads, %d bars" % (heads - 1, bars),
                "%d positive, %d negative" % (pos, neg), "sign", "ring end marks (one triangle belongs to the centre glyph)")
    FIELD_GLYPHS.append({"loop": spec["loop"], "arcs": len(arcs), "arrowheads_or_triangles": heads, "bars": bars,
                         "v7_plus": pos, "v7_minus": neg, "textures": dict(dashes),
                         "red_arcs": sum(1 for a in arcs if a[0] == "#E63946")})

# ---------------------------------------------- Concepts V2 Who Can Act (section 11)
wca = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 11"))
wl = [x["t"] for x in DOCS[wca]["lines"]]
live = {k: R for k, R in REFORMS.items() if not R["rejected"]}
route_n = collections.Counter()
route_hm = collections.Counter()
for k, R in live.items():
    for r in R["routes"]:
        route_n[r["route"]] += 1
        if r["feasibility"] in ("high", "medium"):
            route_hm[r["route"]] += 1
for j, t in enumerate(wl):
    m = re.match(r"^(LOC|SS|BI|FS|FR|FA|ENF|CRT|AV|IC|CIV) (.+?) (\d+)$", t)
    if m:
        code, name, n = m.group(1), m.group(2), int(m.group(3))
        hm = next((x for x in wl[j + 1:j + 4] if "rated high or medium" in x), "")
        mh = re.match(r"(\d+) of (\d+)", hm)
        checked["Who Can Act route rows"] += 1
        if n != route_n[code]:
            finding(wca, "route " + code, code, str(n) + " reforms", "%d live reforms list this route" % route_n[code],
                    "structure", "route count")
        if mh and int(mh.group(1)) != route_hm[code]:
            finding(wca, "route " + code, code, hm, "%d of %d rated high or medium" % (route_hm[code], route_n[code]),
                    "structure", "feasibility count")
        if name != ROUTES[code]["name"]:
            finding(wca, "route " + code, code, name, ROUTES[code]["name"], "label", "route name")


def lead_code(c):
    c = c.replace("−", "-")
    m = re.match(r"^\s*([+\-]?[LMS]|0|\?)", c)
    return m.group(1) if m else c


fam_stats = {}
for f in ("DQ", "GE", "EP", "EQ"):
    cc = collections.Counter(lead_code(R["effects"][f]) for R in live.values())
    cost = sum(1 for R in live.values() if re.search(r"-[SM]", R["effects"][f].replace("−", "-")))
    gain_with_cost = sum(1 for R in live.values() if lead_code(R["effects"][f]).startswith("+") and
                         re.search(r"-[SM]", R["effects"][f].replace("−", "-")))
    cost_no_gain = sum(1 for R in live.values() if not lead_code(R["effects"][f]).startswith("+") and
                       re.search(r"-[SM]", R["effects"][f].replace("−", "-")))
    fam_stats[f] = {"codes": dict(cc), "improve": cc["+L"] + cc["+M"] + cc["+S"], "uncertain": cc["?"],
                    "with cost": cost, "gain with cost": gain_with_cost, "cost without gain": cost_no_gain}
for f, name in (("DQ", "Democratic quality"), ("GE", "Government efficacy"), ("EP", "Economic performance"),
                ("EQ", "Income and wealth equality")):
    j = wl.index(name) if name in wl else None
    if j is None:
        continue
    t = wl[j + 1]
    m = re.match(r"(\d+) reforms expected to improve it: (?:(\d+) large, )?(\d+) moderate, (\d+) small\. (\d+) uncertain", t)
    st = fam_stats[f]
    checked["Who Can Act outcome rows"] += 1
    if m:
        shown = (int(m.group(1)), int(m.group(2) or 0), int(m.group(3)), int(m.group(4)), int(m.group(5)))
        exp = (st["improve"], st["codes"].get("+L", 0), st["codes"].get("+M", 0), st["codes"].get("+S", 0), st["uncertain"])
        if shown != exp:
            finding(wca, "outcome " + f, f, t, "%d improve: %d large, %d moderate, %d small; %d uncertain (leading code of each V7 effect string)" % exp,
                    "structure", "effect tally")
# reform groups
for g in V7["reformGroups"]:
    m = [t for t in wl if re.fullmatch(re.escape(g["title"]) + r" (\d+)", t)]
    if m:
        checked["Who Can Act group rows"] += 1
        n = int(m[0].rsplit(" ", 1)[1])
        if n != len(g["reforms"]):
            finding(wca, "reform groups", g["title"], str(n), str(len(g["reforms"])), "structure", "group size")
for t in wl:
    m = re.match(r"^(R-\d\d) (.+)$", t)
    if m and m.group(1) in REFORMS:
        checked["Who Can Act reform titles"] += 1
        if norm(m.group(2)) != norm(REFORMS[m.group(1)]["title"]):
            finding(wca, "reform list", m.group(1), m.group(2), REFORMS[m.group(1)]["title"], "label", "reform title")

# strand widths in Who Can Act
wca_svg = CV2_SECTIONS[11]
widths = collections.Counter(re.findall(r'stroke-width="([\d.]+)"', wca_svg))
WCA_WIDTHS = widths.most_common(12)

# ---------------------------------------------- Concepts V2 Ledger (section 07)
led = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 07"))
ll = [x["t"] for x in DOCS[led]["lines"]]
LEDGER = {}
for j, t in enumerate(ll):
    if (t in DOMAINS or t in ("EC", "TC")) and j + 2 < len(ll):
        k = j + 1
        while k < len(ll) and not re.fullmatch(r"\d+", ll[k]) and not ll[k].startswith("+"):
            k += 1
        varlist = [x for x in ll[j + 1:k] if x in NODES]
        while k < len(ll) and ll[k].startswith("+"):
            k += 1
        nums = ll[k:k + 3]
        main = ll[k + 3] if k + 3 < len(ll) else ""
        if all(re.fullmatch(r"\d+", x) for x in nums):
            LEDGER[t] = {"vars": varlist, "links": int(nums[0]), "loops": int(nums[1]), "reforms": int(nums[2]),
                         "main": main}
LEDGER_COMPUTED = {}
for code, row in LEDGER.items():
    vs = set(vars_on[code])
    touch = [k for k, L in LINKS.items() if L["from"] in vs or L["to"] in vs]
    vs_any = {k for k, n in NODES.items() if code in (n["domain"] or n["cluster"]).split("/")}
    touch_any = [k for k, L in LINKS.items() if L["from"] in vs_any or L["to"] in vs_any]
    loops_all = {lp for lp, Lp in LOOPS.items() if any(LINKS[l]["from"] in vs or LINKS[l]["to"] in vs for l in Lp["links"])
                 or any(c[0] in vs for c in Lp["chain"])}
    loops_any = {lp for lp, Lp in LOOPS.items() if any(LINKS[l]["from"] in vs_any or LINKS[l]["to"] in vs_any for l in Lp["links"])}
    LEDGER_COMPUTED[code] = {"links touching first-domain vars": len(touch), "links touching any-domain vars": len(touch_any),
                             "loops (first-domain)": len(loops_all), "loops (any domain)": len(loops_any),
                             "reforms touching": SHEET_COMPUTED.get(code, {}).get("reforms (targets touching sheet)")}
    checked["Ledger rows"] += 1

# ---------------------------------------------- Concepts V2 Circuit (section 10)
cir = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 10"))
cl = [x["t"] for x in DOCS[cir]["lines"]]
region_of = {}
for lay in V7["layers"].values():
    for rg in lay["regions"]:
        for n in rg["nodes"]:
            region_of[n] = rg["id"]
core_area = {n: region_of[n] for n in NODES if NODES[n]["layer"] == "core"}


def area(n):
    if NODES[n]["layer"] == "core":
        return core_area[n]
    return NODES[n]["layer"]


inside_area = collections.Counter()
cat = collections.Counter()
for k, L in LINKS.items():
    a, b = area(L["from"]), area(L["to"])
    if a == b:
        inside_area[a] += 1
    elif a == "X":
        cat["from outside drivers"] += 1
    elif a in "ABCDE" and b in "ABCDE":
        cat["between the five areas"] += 1
    else:
        cat["to, from or within the two lower layers"] += 1
CIRCUIT = {"inside": dict(inside_area), "categories": dict(cat), "crossing_total": sum(cat.values())}
cir_txt = " ".join(cl)
checked["Circuit counts"] += 1
m = re.search(r"one of the (\d+) that cross a boundary: (\d+) between the five areas, (\d+) to, from or within the two "
              r"lower layers, and (\d+) from outside drivers\. The (\d+) that stay inside", cir_txt)
if m:
    shown = tuple(int(x) for x in m.groups())
    exp = (sum(cat.values()), cat["between the five areas"], cat["to, from or within the two lower layers"],
           cat["from outside drivers"], sum(inside_area.values()))
    if shown != exp:
        finding(cir, "intro", "connection tally", "81 crossing (38 + 28 + 15), 37 inside",
                "%d crossing (%d + %d + %d), %d inside, computed with V7 regions A to E, X and the two layers" % exp,
                "structure", "Circuit tally")
for a, word in (("A", "6 connections inside this area"), ("B", "5 connections inside this area"),
                ("C", "5 connections inside this area"), ("D", "7 connections inside this area")):
    n = int(word.split()[0])
    if inside_area[a] != n:
        finding(cir, "area " + a, "inside count " + a, str(n), str(inside_area[a]), "structure", "Circuit card")
for m in re.finditer(r"Passes (?:on to|back to) ([A-E]): (.+?) \(([A-Z]+\d+)\)", cir_txt):
    to_area, nm, lid = m.groups()
    L = LINKS.get(lid)
    checked["Circuit pass-on examples"] += 1
    if not L or norm(nm) != norm(L["name"]):
        finding(cir, "pass-on", lid, nm, L["name"] if L else "missing", "label", "pass-on example")
    elif area(L["to"]) != to_area:
        finding(cir, "pass-on", lid, "lands in area " + to_area, "lands in " + area(L["to"]), "structure", "pass-on example")

# ---------------------------------------------- other numeric claims in Concepts V2
CLAIMS_CHECK = []


def claim(doc, where, text, shown, v7, typ="structure"):
    CLAIMS_CHECK.append({"doc": DOCS[doc]["location"], "where": where, "text": text, "shown": shown, "v7": v7,
                         "ok": str(shown) == str(v7)})
    checked["numeric and structural claims"] += 1
    if str(shown) != str(v7):
        finding(doc, where, text, str(shown), str(v7), typ, "claim check")


cross_layer = sum(1 for L in LINKS.values() if NODES[L["from"]]["layer"] != NODES[L["to"]]["layer"])
fm = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 04"))
claim(fm, "Figure 1-1", "connections that cross from one layer to another", 31, cross_layer)
c00 = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 01"))
lay_n = collections.Counter(n["layer"] for n in NODES.values())
claim(c00, "layers key", "Power and accountability variables", 31, lay_n["core"])
claim(c00, "layers key", "How the economy reaches a household variables", 12, lay_n["economy"])
claim(c00, "layers key", "Technology and its effects variables", 8, lay_n["technology"])
claim(c00, "layers key", "Outside drivers among the 31", 5, sum(1 for n in NODES.values() if n["type"] == "driver"))
claim(fg, "intro", "closed loops", 20, sum(1 for Lp in LOOPS.values() if Lp["links"]))
claim(fg, "intro", "snowball (R) closed loops", 17, sum(1 for Lp in LOOPS.values() if Lp["links"] and Lp["type"] == "R"))
claim(fg, "intro", "thermostat (B) closed loops", 3, sum(1 for Lp in LOOPS.values() if Lp["links"] and Lp["type"] == "B"))
claim(fg, "intro", "closed with an untested step", 2, sum(1 for Lp in LOOPS.values() if Lp["closure"].startswith("closed with")))
claim(idx, "intro", "live reforms", 49, len(live))
claim(idx, "whole atlas", "issues", 194, len(ISSUES))
ice = next(i for i, dd in enumerate(DOCS) if dd["location"].startswith("section 06"))
# Iceberg band placement of the elections group
ice_txt = "\n".join(x["t"] for x in DOCS[ice]["lines"])
bands_shown = {}
cur = None
for t in ice_txt.split("\n"):
    if t in ("Numbers", "Feedback", "Information", "Rules", "Power over the rules", "Goals and mindsets"):
        cur = t
    elif cur and re.fullmatch(r"R-\d\d", t):
        bands_shown[t] = cur
band_label = {"parameter": "Numbers", "feedback": "Feedback", "information": "Information", "rules": "Rules",
              "power to change the rules": "Power over the rules", "goals": "Goals and mindsets"}
for r in V7["reformGroups"][0]["reforms"]:
    claim(ice, "depth gauge", r + " leverage band", bands_shown.get(r, "not shown"), band_label[REFORMS[r]["band"]])
# Ledger checks against plausible counting rules
for code, row in LEDGER.items():
    c = LEDGER_COMPUTED[code]
    if row["links"] not in (c["links touching first-domain vars"], c["links touching any-domain vars"]):
        finding(led, "row " + code, code + " links", str(row["links"]),
                "%d (links touching variables first-listed here) or %d (touching any variable listed here)" %
                (c["links touching first-domain vars"], c["links touching any-domain vars"]), "structure",
                "Ledger count; counting rule not stated")
    if row["loops"] not in (c["loops (first-domain)"], c["loops (any domain)"]):
        finding(led, "row " + code, code + " loops", str(row["loops"]),
                "%d or %d" % (c["loops (first-domain)"], c["loops (any domain)"]), "structure", "Ledger count")
    vs_set = set(vars_on[code])

    def touches(R, S=vs_set):
        return any((t in S) or (t in LINKS and (LINKS[t]["from"] in S or LINKS[t]["to"] in S)) for t in R["targets"])
    live_n = sum(1 for R in REFORMS.values() if not R["rejected"] and touches(R))
    all_n = sum(1 for R in REFORMS.values() if touches(R))
    checked["Ledger reform counts"] += 1
    if row["reforms"] != live_n:
        finding(led, "row " + code, code + " reforms", str(row["reforms"]),
                "%d live reforms target this domain; %d if the rejected R-35 is counted" % (live_n, all_n),
                "structure", "Ledger reform count")
    vs = sorted(vars_on[code])
    if row["vars"] and not set(row["vars"]) <= set(vs):
        finding(led, "row " + code, code + " variables", " ".join(row["vars"]), " ".join(vs), "structure", "Ledger variables")

# ---------------------------------------------- effect words for reforms anywhere
EFFECT_WORD = {"+L": "large positive", "+M": "moderate positive", "+S": "small positive", "0": "no expected effect",
               "-S": "small negative", "-M": "moderate negative", "?": "direction uncertain"}
for di, d in enumerate(DOCS):
    lines = [x["t"] for x in d["lines"]]
    for j, t in enumerate(lines):
        if t in ("Democratic quality", "Government efficacy", "Economic performance", "Income and wealth equality",
                 "Income and wealth") and j + 1 < len(lines):
            # find the reform this block belongs to: nearest previous R-xx
            prev = [m.group(1) for x in lines[max(0, j - 40):j] for m in re.finditer(r"(R-\d\d)", x)]
            if not prev:
                continue
            rid = prev[-1]
            fam = {"Democratic quality": "DQ", "Government efficacy": "GE", "Economic performance": "EP",
                   "Income and wealth equality": "EQ", "Income and wealth": "EQ"}[t]
            val = lines[j + 1]
            if val.startswith("[[") and j + 2 < len(lines):
                val = lines[j + 2]
            if val in ("equality",):
                continue
            if not re.match(r"^(large|moderate|small|no expected|direction|none)", val.lower()):
                continue
            code = REFORMS[rid]["effects"][fam]
            checked["reform effect words"] += 1
            if norm(val) != EFFECT_WORD.get(lead_code(code), "?") and not norm(val).startswith(EFFECT_WORD.get(lead_code(code), "?")):
                finding(di, "effects", rid + " " + fam, val, code, "label", "effect word")

# AVS outcomes figure: the three reform columns are read in order from the SVG text
avs_out = next(i for i, dd in enumerate(DOCS) if dd["file"].endswith("924cc52d98.svg"))
ol = [x["t"] for x in DOCS[avs_out]["lines"]]
for rid in ("R-01", "R-06", "R-28"):
    j = ol.index("REFORM " + rid)
    vals, k = [], j + 1
    while len(vals) < 4 and k < len(ol):
        t = ol[k]
        if re.match(r"^(Moderate|Small|Large|No expected|None to)", t):
            if t.startswith("None to") and ol[k + 1] in ("negative",):
                t += " negative"
                k += 1
            if t.endswith("·") and k + 1 < len(ol):
                t += " " + ol[k + 1]
                k += 1
            vals.append(t)
        k += 1
    checked["AVS outcome cells"] += 4
    for fam, v in zip(("DQ", "GE", "EP", "EQ"), vals):
        code = REFORMS[rid]["effects"][fam]
        exp = EFFECT_WORD.get(lead_code(code), code)
        if not norm(v).startswith(exp.split(" ")[0]) and not (code.startswith("0 to -S") and v.startswith("None to small")):
            finding(avs_out, "figure 08", rid + " " + fam, v, code, "label", "effect word")

# ---------------------------------------------- AVS domain table
avs_lay = next(i for i, dd in enumerate(DOCS) if dd["location"] == "chapter 07-layers")
al = [x["t"] for x in DOCS[avs_lay]["lines"]]
for j, t in enumerate(al):
    if t in DOMAINS and j + 1 < len(al):
        checked["AVS domain rows"] += 1
        if norm(al[j + 1]) != norm(DOMAINS[t]["title"]):
            finding(avs_lay, "domain table", t, al[j + 1], DOMAINS[t]["title"], "label", "domain title")
for t in al:
    for lay in V7["layers"].values():
        if t.startswith(lay["title"]):
            checked["AVS layer rows"] += 1

# ---------------------------------------------- loop titles next to loop IDs
for i, o in enumerate(occ):
    if "loop" not in o["kinds"] or "standards rule" in o["kinds"]:
        continue
    t = html.unescape(o["text"])
    after = t[o["pos"] + len(o["id"]):].strip(" :·,")
    lt = LOOPS[o["id"]]["title"]
    if o["id"] in NODES and meaning(o).startswith("variable"):
        continue  # a colliding ID used as a variable; recorded under ID collisions
    if re.match(r"^(Variables?|Links?|Loops?|Reforms?)\b", after):
        continue  # a footer list of IDs, with no title
    if after and len(after) > 25 and not ID_RE.match(after) and re.match(r"^[A-Z][a-z]", after):
        checked["loop titles next to loop IDs"] += 1
        if not norm(after).startswith(norm(lt)) and norm(lt)[:20] not in norm(after):
            finding(o["doc"], o["sub"], o["id"], after[:90], lt, "label", "loop title next to ID")

# ---------------------------------------------- reviewed false positives
REVIEWED_FALSE = []
keep = []
for f in FINDINGS:
    n = f["note"]
    if f["item"] == "L26" and "hypothetical return link" in n:
        REVIEWED_FALSE.append(dict(f, why="the word 'hypothetical' in this clause describes T01, the next link"))
    elif f["item"] == "L03" and "Remedy evidence in V7: plausible" in n:
        REVIEWED_FALSE.append(dict(f, why="'plausible' is the remedy evidence grade of reform R-28, shown on the line below"))
    else:
        keep.append(f)
FINDINGS[:] = keep

# ---------------------------------------------- summary
id_occ = [o for o in occ if o["kinds"] not in (["route"], ["effect code"])]
unique_ids = sorted({o["id"] for o in id_occ})
by_group = collections.Counter(DOCS[o["doc"]]["group"] for o in id_occ)
by_kind = collections.Counter(k for o in id_occ for k in (o["kinds"] or ["unknown"]))
summary = {
    "identifier_occurrences": len(id_occ),
    "unique_identifiers": len(unique_ids),
    "route_code_occurrences": sum(1 for o in occ if o["kinds"] == ["route"]),
    "effect_code_occurrences": sum(1 for o in occ if o["kinds"] == ["effect code"]),
    "occurrences_by_source": dict(by_group),
    "occurrences_by_kind": dict(by_kind),
    "checks_run": dict(checked),
    "auto_findings": len(FINDINGS),
    "reviewed_false_positives": len(REVIEWED_FALSE),
    "auto_findings_by_type": dict(collections.Counter(f["type"] for f in FINDINGS)),
    "documents_scanned": len(DOCS),
}

out = {
    "summary": summary,
    "findings": FINDINGS,
    "reviewed_false_positives": REVIEWED_FALSE,
    "collisions": COLLISIONS,
    "standards_rules_found": std_rules,
    "v5_atlas_loops_found": v5_loops,
    "variable_labels_shown": {k: [{"label": l, "source": g, "n": n} for (l, g), n in v.most_common()]
                              for k, v in sorted(VAR_LABELS.items())},
    "register_rows": REG["rows"],
    "register_vars": REG["vars"],
    "register_reforms": REG["reforms"],
    "sheet_stats_shown": {k: v[0] for k, v in sheet_stats.items()},
    "sheet_stats_computed": SHEET_COMPUTED,
    "index_rows_shown": INDEX_ROWS,
    "busiest_crossings_computed": [["%s to %s" % k, n] for k, n in top_cross],
    "field_guide": FIELD,
    "field_guide_glyphs": FIELD_GLYPHS,
    "who_can_act": {"route_counts": dict(route_n), "route_high_medium": dict(route_hm), "families": fam_stats,
                    "stroke_widths": WCA_WIDTHS},
    "ledger_shown": LEDGER,
    "ledger_computed": LEDGER_COMPUTED,
    "circuit_computed": CIRCUIT,
    "claims": CLAIMS_CHECK,
    "documents": [{"group": d["group"], "file": d["file"], "location": d["location"], "lines": len(d["lines"])}
                  for d in DOCS],
    "occurrences": [{"file": DOCS[o["doc"]]["file"], "location": DOCS[o["doc"]]["location"], "sub": o["sub"],
                     "id": o["id"], "kinds": o["kinds"], "shown": o.get("shown", ""), "text": o["text"][:200]}
                    for o in occ],
}
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, ensure_ascii=False)
print(json.dumps(summary, indent=1))
