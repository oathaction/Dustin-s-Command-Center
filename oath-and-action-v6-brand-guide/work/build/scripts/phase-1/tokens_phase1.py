"""Phase 1 token architecture: measurements and the schema draft.

Run:  python3 -I work/build/scripts/phase-1/tokens_phase1.py

Reads   work/extract/v5-polished/fonts/*.ttf and chapters-text/*.txt
Writes  work/handoffs/phase-1/20261021_Token-Contrast-Data.json
        work/build/tokens/20261021_Token-Schema-Draft.json
Prints  the Markdown tables used in work/ledger/20261021_Token-Architecture.md

Proposals only. Nothing here ships. Standard library only.
"""

import importlib.util
import json
import pathlib
import struct

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
spec = importlib.util.spec_from_file_location("oa_color", HERE / "oa_color.py")
oc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oc)

P, SURF = oc.PALETTE, oc.SURFACES
FMT = "2025.10"
NS = "org.oathandaction"
OUT_DATA = ROOT / "work/handoffs/phase-1/20261021_Token-Contrast-Data.json"
OUT_DRAFT = ROOT / "work/build/tokens/20261021_Token-Schema-Draft.json"

# WCAG 2.2 thresholds by job kind
THRESH = {"text": 4.5, "largeText": 3.0, "graphic": 3.0, "focus": 3.0, "decorative": None}

# Master Brief V2 section 8, item 9 (to verify)
BRIEF = {
    "charcoal": [13.29, 18.73, None, 1.41], "prussian": [9.42, 13.28, 1.41, None],
    "stone": [4.29, 6.05, 3.10, 2.20], "verdigris": [3.37, 4.74, 3.95, 2.80],
    "pillarRed": [2.96, 4.17, 4.49, 3.19], "newsprint": [None, 1.41, 13.29, 9.42],
}


def r2(x):
    return round(x, 2)


def on_all(h):
    return {s: r2(oc.contrast(h, P[s])) for s in SURF}


def grade(c):
    if c >= 4.5:
        return "text"
    if c >= 3.0:
        return "large text, graphics"
    return "fails 3:1"


# 1. Verify the brief's table -------------------------------------------------
verify = []
for name, row in BRIEF.items():
    for s, want in zip(SURF, row):
        if want is None:
            continue
        got = r2(oc.contrast(P[name], P[s]))
        verify.append({"fg": name, "surface": s, "brief": want, "computed": got, "match": got == want})

# 2. Palette classification per surface ----------------------------------------
classes = {f: {s: {"ratio": r2(oc.contrast(P[f], P[s])), "grade": grade(oc.contrast(P[f], P[s]))}
               for s in SURF if f != s} for f in P}

# 3. Derived candidates ---------------------------------------------------------
def derive(base, toward, amount, space):
    fn = oc.mix_oklch if space == "oklch" else oc.mix_oklab
    hexv, in_gamut = fn(P[base], P[toward], amount)
    return hexv, in_gamut


CANDIDATES = [
    # name, base, toward, amount, space, status, job, kind, surfaces it serves
    ("deepStone", "stone", "charcoal", 0.18, "oklab", "proposed",
     "Secondary text, captions, labels and disabled text on Newsprint and White", "text", ["newsprint", "white"]),
    ("dimNewsprint", "newsprint", "charcoal", 0.25, "oklab", "proposed",
     "Secondary text, captions, labels and disabled text on Charcoal and Prussian", "text", ["charcoal", "prussian"]),
    ("errorBand", "pillarRed", "newsprint", 0.88, "oklab", "proposed",
     "Background of an error message on Newsprint and White", "background", ["newsprint", "white"]),
    ("verdigrisOnDark", "verdigris", "newsprint", 0.10, "oklab", "held",
     "Status marks on Prussian, only if the Phase 2 Signal Grid keeps Verdigris there", "graphic", ["charcoal", "prussian"]),
    ("redInk", "pillarRed", "charcoal", 0.25, "oklab", "rejected",
     "Small red text on Newsprint (not recommended)", "text", ["newsprint", "white"]),
    ("redGraphic", "pillarRed", "charcoal", 0.05, "oklab", "rejected",
     "Red marks on Newsprint without a keyline (not recommended)", "graphic", ["newsprint"]),
]

derived = {}
for name, base, toward, amt, space, status, job, kind, serves in CANDIDATES:
    hexv, ok = derive(base, toward, amt, space)
    alt, _ = derive(base, toward, amt, "oklch")
    d = {
        "hex": hexv, "inGamut": ok, "status": status, "job": job, "kind": kind, "serves": serves,
        "derivation": {"method": "color-mix", "space": space, "base": base, "toward": toward, "amount": amt},
        "oklchEquivalent": alt, "oklchHueDrift": None,
        "contrastOnSurfaces": on_all(hexv),
        "oklch": [round(v, 4) if v is not None else None for v in oc.to_oklch(hexv)],
    }
    h_base, h_alt = oc.to_oklch(P[base])[2], oc.to_oklch(alt)[2]
    if h_base is not None and h_alt is not None:
        dh = abs((h_alt - h_base + 180) % 360 - 180)
        d["oklchHueDrift"] = round(dh, 1)
    if kind == "background":
        d["textOnIt"] = {"charcoal": r2(oc.contrast(P["charcoal"], hexv))}
    derived[name] = d
for d in derived.values():
    if d["kind"] == "background":
        d["textOnIt"]["deepStone"] = r2(oc.contrast(derived["deepStone"]["hex"], d["hex"]))

# The Concepts V2 value
c2 = "#4E535C"
c2_info = {
    "hex": c2, "contrastOnSurfaces": on_all(c2),
    "equalsStoneScaledInSrgb": oc.rgb_to_hex(tuple(c * 0.84 for c in oc.hex_to_rgb(P["stone"]))) == c2,
    "deltaEokToDeepStone": round(oc.delta_e_ok(c2, derived["deepStone"]["hex"]), 4),
    "usesInConceptsV2": 1606,
}
v7_red = "#BD2C32"
red_info = {"v7Red": v7_red, "deltaEokRedInkToV7Red": round(oc.delta_e_ok(derived["redInk"]["hex"], v7_red), 4),
            "v7RedOnNewsprint": r2(oc.contrast(v7_red, P["newsprint"]))}

# Contrast between neighbours that must stay distinct
pairs = {
    "deepStone vs charcoal": r2(oc.contrast(derived["deepStone"]["hex"], P["charcoal"])),
    "dimNewsprint vs newsprint": r2(oc.contrast(derived["dimNewsprint"]["hex"], P["newsprint"])),
    "white vs newsprint (selected swap, light)": r2(oc.contrast(P["white"], P["newsprint"])),
    "prussian vs charcoal (selected swap, dark)": r2(oc.contrast(P["prussian"], P["charcoal"])),
    "errorBand vs newsprint": r2(oc.contrast(derived["errorBand"]["hex"], P["newsprint"])),
    "verdigris vs pillarRed": r2(oc.contrast(P["verdigris"], P["pillarRed"])),
}

# Opacity: what the watermark and an opacity-disabled label actually measure
wm = {
    "charcoal8OnNewsprint": oc.over(P["charcoal"], P["newsprint"], 0.08),
    "newsprint10OnCharcoal": oc.over(P["newsprint"], P["charcoal"], 0.10),
    "newsprint10OnPrussian": oc.over(P["newsprint"], P["prussian"], 0.10),
    "charcoal8OnWhite": oc.over(P["charcoal"], P["white"], 0.08),
}
opacity = {k: {"hex": v, "contrastWithGround": r2(oc.contrast(v, P[{"charcoal8OnNewsprint": "newsprint",
           "newsprint10OnCharcoal": "charcoal", "newsprint10OnPrussian": "prussian",
           "charcoal8OnWhite": "white"}[k]]))} for k, v in wm.items()}
dis40 = oc.over(P["charcoal"], P["white"], 0.40)
opacity["charcoal40OnWhite_disabledByOpacity"] = {"hex": dis40, "contrastWithGround": r2(oc.contrast(dis40, P["white"]))}
lev = oc.over(P["pillarRed"], P["newsprint"], 0.20)
opacity["v5LoadingLever20OnNewsprint"] = {"hex": lev, "contrastWithGround": r2(oc.contrast(lev, P["newsprint"]))}

# 4. Role table: semantic role -> token per surface ------------------------------
DS, DN, EB = derived["deepStone"]["hex"], derived["dimNewsprint"]["hex"], derived["errorBand"]["hex"]
ROLES = [
    # role, kind, {surface: (label, hex)}
    ("text.primary", "text", {"newsprint": ("Charcoal", P["charcoal"]), "white": ("Charcoal", P["charcoal"]),
                              "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("White", P["white"])}),
    ("text.secondary", "text", {"newsprint": ("Deep Stone", DS), "white": ("Deep Stone", DS),
                                "charcoal": ("Dim Newsprint", DN), "prussian": ("Dim Newsprint", DN)}),
    ("identity.signature (wordmark ampersand, lockmark lever)", "logotype", {"newsprint": ("Pillar Red", P["pillarRed"]),
                                "white": ("Pillar Red", P["pillarRed"]), "charcoal": ("Pillar Red", P["pillarRed"]),
                                "prussian": ("White", P["white"])}),
    ("identity.hingeDivider (divider ampersand)", "graphic", {"newsprint": ("Charcoal", P["charcoal"]), "white": ("Charcoal", P["charcoal"]),
                                "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("action.ask fill", "graphic", {"newsprint": ("Pillar Red + 1 px Charcoal keyline", P["pillarRed"]),
                                "white": ("Pillar Red", P["pillarRed"]), "charcoal": ("Pillar Red", P["pillarRed"]),
                                "prussian": ("Newsprint", P["newsprint"])}),
    ("action.ask label (19 px bold)", "largeText", {"newsprint": ("White on Pillar Red", None), "white": ("White on Pillar Red", None),
                                "charcoal": ("White on Pillar Red", None), "prussian": ("Charcoal on Newsprint", None)}),
    ("action.primary fill", "graphic", {"newsprint": ("Charcoal", P["charcoal"]), "white": ("Charcoal", P["charcoal"]),
                                "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("action.primary label", "text", {"newsprint": ("White on Charcoal", None), "white": ("White on Charcoal", None),
                                "charcoal": ("Charcoal on Newsprint", None), "prussian": ("Charcoal on Newsprint", None)}),
    ("graphic.essential", "graphic", {"newsprint": ("Charcoal", P["charcoal"]), "white": ("Charcoal", P["charcoal"]),
                                      "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("graphic.subtle (unlit nodes, context marks)", "graphic", {"newsprint": ("Stone", P["stone"]), "white": ("Stone", P["stone"]),
                                      "charcoal": ("Dim Newsprint", DN), "prussian": ("Dim Newsprint", DN)}),
    ("working.red (one per view)", "graphic", {"newsprint": ("Pillar Red + 1 px Charcoal keyline", P["pillarRed"]),
                                      "white": ("Pillar Red", P["pillarRed"]), "charcoal": ("Pillar Red", P["pillarRed"]),
                                      "prussian": ("None: red never sits on Prussian", None)}),
    ("border.strong (inputs, component edges)", "graphic", {"newsprint": ("Charcoal", P["charcoal"]), "white": ("Charcoal", P["charcoal"]),
                                      "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("border.hairline (decorative)", "decorative", {"newsprint": ("Stone", P["stone"]), "white": ("Stone", P["stone"]),
                                      "charcoal": ("Stone", P["stone"]), "prussian": ("White", P["white"])}),
    ("focus.ring", "focus", {"newsprint": ("Verdigris", P["verdigris"]), "white": ("Verdigris", P["verdigris"]),
                             "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("state.success mark", "graphic", {"newsprint": ("Verdigris", P["verdigris"]), "white": ("Verdigris", P["verdigris"]),
                                       "charcoal": ("Verdigris", P["verdigris"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("state.error mark", "graphic", {"newsprint": ("Pillar Red + keyline", P["pillarRed"]), "white": ("Pillar Red", P["pillarRed"]),
                                     "charcoal": ("Pillar Red", P["pillarRed"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("state.selected band", "background", {"newsprint": ("White", P["white"]), "white": ("Newsprint", P["newsprint"]),
                                           "charcoal": ("Prussian", P["prussian"]), "prussian": ("Charcoal", P["charcoal"])}),
    ("state.error band", "background", {"newsprint": ("Error Band", EB), "white": ("Error Band", EB),
                                        "charcoal": ("none (bar and label only)", None), "prussian": ("none (bar and label only)", None)}),
    ("data.emphasis default", "graphic", {"newsprint": ("Charcoal", P["charcoal"]), "white": ("Charcoal", P["charcoal"]),
                                          "charcoal": ("Newsprint", P["newsprint"]), "prussian": ("Newsprint", P["newsprint"])}),
    ("data.context", "graphic", {"newsprint": ("Stone", P["stone"]), "white": ("Stone", P["stone"]),
                                 "charcoal": ("Dim Newsprint", DN), "prussian": ("Dim Newsprint", DN)}),
]
ON_PAIRS = {"White on Charcoal": (P["white"], P["charcoal"]), "Charcoal on Newsprint": (P["charcoal"], P["newsprint"]),
            "White on Pillar Red": (P["white"], P["pillarRed"])}
role_rows = []
for role, kind, cells in ROLES:
    row = {"role": role, "kind": kind, "cells": {}}
    for s in SURF:
        label, hexv = cells[s]
        if label in ON_PAIRS:
            fg, bg = ON_PAIRS[label]
            c = oc.contrast(fg, bg)
        elif hexv is None:
            c = None
        elif kind == "background":
            c = oc.contrast(P["charcoal"] if s in ("newsprint", "white") else P["newsprint"], hexv)
        else:
            c = oc.contrast(hexv, P[s])
        t = THRESH.get(kind if kind != "background" else "text")
        row["cells"][s] = {"token": label, "hex": hexv, "ratio": r2(c) if c else None,
                           "passes": (c >= t) if (c and t) else None}
        if "keyline" in label:
            k = oc.contrast(P["charcoal"], P[s])
            row["cells"][s].update(keylineRatio=r2(k), passes=k >= 3.0)
    role_rows.append(row)

# 5. Type measures from Inter's own advance widths -------------------------------
def ttf_advances(path):
    data = path.read_bytes()
    num = struct.unpack(">H", data[4:6])[0]
    tables = {}
    for i in range(num):
        tag, _, off, ln = struct.unpack(">4sIII", data[12 + 16 * i: 28 + 16 * i])
        tables[tag.decode()] = (off, ln)
    upm = struct.unpack(">H", data[tables["head"][0] + 18: tables["head"][0] + 20])[0]
    nhm = struct.unpack(">H", data[tables["hhea"][0] + 34: tables["hhea"][0] + 36])[0]
    ho = tables["hmtx"][0]
    adv = [struct.unpack(">H", data[ho + 4 * i: ho + 4 * i + 2])[0] for i in range(nhm)]
    co = tables["cmap"][0]
    n = struct.unpack(">H", data[co + 2: co + 4])[0]
    subs = {}
    for i in range(n):
        pid, eid, off = struct.unpack(">HHI", data[co + 4 + 8 * i: co + 12 + 8 * i])
        subs[(pid, eid)] = co + off
    cmap = {}
    if (3, 10) in subs:
        o = subs[(3, 10)]
        ng = struct.unpack(">I", data[o + 12: o + 16])[0]
        for g in range(ng):
            s, e, gid = struct.unpack(">III", data[o + 16 + 12 * g: o + 28 + 12 * g])
            for cp in range(s, e + 1):
                cmap[cp] = gid + cp - s
    else:
        o = subs[(3, 1)]
        seg = struct.unpack(">H", data[o + 6: o + 8])[0] // 2
        ends = struct.unpack(f">{seg}H", data[o + 14: o + 14 + 2 * seg])
        so = o + 16 + 2 * seg
        starts = struct.unpack(f">{seg}H", data[so: so + 2 * seg])
        deltas = struct.unpack(f">{seg}h", data[so + 2 * seg: so + 4 * seg])
        ro = so + 4 * seg
        ranges = struct.unpack(f">{seg}H", data[ro: ro + 2 * seg])
        for k in range(seg):
            for cp in range(starts[k], ends[k] + 1):
                if cp == 0xFFFF:
                    continue
                if ranges[k] == 0:
                    gid = (cp + deltas[k]) & 0xFFFF
                else:
                    a = ro + 2 * k + ranges[k] + 2 * (cp - starts[k])
                    gid = struct.unpack(">H", data[a: a + 2])[0]
                    gid = (gid + deltas[k]) & 0xFFFF if gid else 0
                cmap[cp] = gid
    def advance(ch):
        gid = cmap.get(ord(ch), 0)
        return adv[min(gid, nhm - 1)] / upm
    return advance


fonts = ROOT / "work/extract/v5-polished/fonts"
corpus = []
for f in sorted((ROOT / "work/extract/v5-polished/chapters-text").glob("*.txt")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if len(line) > 100 and ". " in line and "[svg]" not in line:
            corpus.append(line)
text = " ".join(corpus)
inter = ttf_advances(fonts / "Inter-400-normal.ttf")
mean_em = sum(inter(c) for c in text) / len(text)
zero_em = inter("0")


def measure_rem(chars, px):
    return round(chars * mean_em * px / 16, 2)


measures = {
    "corpusCharacters": len(text), "meanAdvanceEm": round(mean_em, 4), "zeroAdvanceEm": round(zero_em, 4),
    "charsPer1ch": round(zero_em / mean_em, 3),
    "v5Intro65chAt22pxGivesChars": round(65 * zero_em / mean_em, 1),
    "body17": {"min60": measure_rem(60, 17), "ideal68": measure_rem(68, 17), "max75": measure_rem(75, 17)},
    "intro22": {"min55": measure_rem(55, 22), "max65": measure_rem(65, 22)},
    "caption14": {"max75": measure_rem(75, 14)},
    "note": "Advance widths only. Kerning (GPOS) is ignored, which shortens real lines by about 1 to 2 percent.",
}

# 6. Type scale (proposal) --------------------------------------------------------
def fluid(min_px, max_px, vmin=390, vmax=1440):
    slope = (max_px - min_px) / (vmax - vmin)
    icpt = min_px - slope * vmin
    return f"clamp({min_px / 16:g}rem, {icpt / 16:.4f}rem + {slope * 100:.4f}vw, {max_px / 16:g}rem)"


TYPE = [
    # name, family, weight, min px, max px, line height, tracking em, case
    ("title", "display", 800, 56, 110, 0.95, -0.045, "sentence"),
    ("section", "display", 800, 44, 80, 1.03, -0.04, "sentence"),
    ("h3", "display", 800, 26, 32, 1.08, -0.03, "sentence"),
    ("h4", "display", 800, 20, 24, 1.15, -0.02, "sentence"),
    ("quote", "quote", 400, 24, 32, 1.3, -0.02, "sentence"),
    ("intro", "reading", 400, 19, 22, 1.5, 0, "sentence"),
    ("body", "reading", 400, 17, 17, 1.6, 0, "sentence"),
    ("bodySmall", "reading", 400, 15, 15, 1.6, 0, "sentence"),
    ("ui", "reading", 600, 15, 15, 1.4, 0, "sentence"),
    ("caption", "reading", 400, 14, 14, 1.5, 0, "sentence"),
    ("label", "reading", 700, 13, 13, 1.4, 0.06, "uppercase"),
    ("dataLabel", "reading", 600, 13, 13, 1.3, 0, "sentence"),
    ("figure", "display", 800, 48, 104, 1.0, -0.04, "sentence"),
    ("ask", "reading", 700, 19, 19, 1.2, 0, "sentence"),
]
TYPE_JOBS = {
    "title": "Cover and chapter-opening titles", "section": "Chapter headings (h2)", "h3": "Module headings",
    "h4": "Sub-module and card headings", "quote": "Pull quotes and quote cards, Lora Italic",
    "intro": "Chapter introduction paragraph", "body": "Running text", "bodySmall": "Table cells, dense specimen notes",
    "ui": "Buttons, navigation, form controls", "caption": "Figure captions and source lines",
    "label": "Eyebrows, column heads and tags, set in capitals", "dataLabel": "Chart labels, axis values and table figures",
    "figure": "Big numbers in reports and specimens",
    "ask": "Ask button label. White on Pillar Red passes only as large text, so it never sets below 19 px bold",
}
type_rows = []
for name, fam, w, mn, mx, lh, tr, case in TYPE:
    type_rows.append({"name": name, "family": fam, "weight": w, "minPx": mn, "maxPx": mx,
                      "minRem": mn / 16, "maxRem": mx / 16, "lineHeight": lh, "trackingEm": tr, "case": case,
                      "css": fluid(mn, mx) if mn != mx else f"{mn / 16:g}rem",
                      "trackingRemAtMax": round(tr * mx / 16, 5)})
floor_ok = all(t["minPx"] >= 13 for t in type_rows)

# 7. Schema draft (DTCG 2025.10) --------------------------------------------------
def ext(**kw):
    return {NS: kw}


def ctok(hexv, desc, **kw):
    r, g, b = oc.hex_to_rgb(hexv)
    return {"$type": "color",
            "$value": {"colorSpace": "srgb", "components": [round(r, 4), round(g, 4), round(b, 4)], "alpha": 1, "hex": hexv},
            "$description": desc, "$extensions": ext(**kw)}


def atok(typ, ref, desc, **kw):
    return {"$type": typ, "$value": "{" + ref + "}", "$description": desc, "$extensions": ext(**kw)}


def dim(v, unit, desc, **kw):
    t = {"$type": "dimension", "$value": {"value": v, "unit": unit}, "$description": desc}
    if kw:
        t["$extensions"] = ext(**kw)
    return t


def surf_contrast(hexv, surfaces):
    return {s: r2(oc.contrast(hexv, P[s])) for s in surfaces}


JOBS = {
    "newsprint": "Default reading surface", "charcoal": "Primary text on light surfaces; the dark beat",
    "pillarRed": "The ampersand, the lever and one point of emphasis per composition",
    "prussian": "Depth, panels and explainers", "stone": "Hairlines, structure and context marks",
    "verdigris": "Live status, focus on light surfaces", "white": "Reversed text, specimens and neutral production",
}
palette = {k: ctok(v, JOBS[k], tier="primitive", status="locked", job=JOBS[k], lockedIn="Master Brief V2 section 3")
           for k, v in P.items()}
derived_tokens = {}
for name, d in derived.items():
    if d["status"] == "rejected":
        continue
    dd = d["derivation"]
    derived_tokens[name] = ctok(
        d["hex"], d["job"], tier="primitive", status=d["status"], job=d["job"], kind=d["kind"],
        derivation={"method": "color-mix", "space": dd["space"], "base": "{oa.color.palette." + dd["base"] + "}",
                    "toward": "{oa.color.palette." + dd["toward"] + "}", "amount": dd["amount"]},
        surfaces=d["serves"],
        contrast=(surf_contrast(d["hex"], d["serves"]) if d["kind"] != "background" else
                  {"charcoalTextOnIt": d["textOnIt"]["charcoal"], "deepStoneTextOnIt": d["textOnIt"]["deepStone"]}),
        need={"deepStone": "N-01", "dimNewsprint": "N-02", "errorBand": "N-03", "verdigrisOnDark": "N-04"}[name],
        gate="Gate 1")

on = {"newsprint": "onNewsprint", "white": "onWhite", "charcoal": "onCharcoal", "prussian": "onPrussian"}
REF = {"Pillar Red": "oa.color.palette.pillarRed", "Charcoal": "oa.color.palette.charcoal", "Newsprint": "oa.color.palette.newsprint", "White": "oa.color.palette.white",
       "Stone": "oa.color.palette.stone", "Verdigris": "oa.color.palette.verdigris", "Prussian": "oa.color.palette.prussian",
       "Deep Stone": "oa.color.derived.deepStone", "Dim Newsprint": "oa.color.derived.dimNewsprint",
       "Error Band": "oa.color.derived.errorBand"}


def semantic(role_key, desc, kind, red=None, **extra):
    row = next(r for r in role_rows if r["role"].split(" (")[0] == role_key)
    group = {}
    for s in SURF:
        cell = row["cells"][s]
        label = cell["token"].split(" +")[0]
        more = dict(extra)
        if label in ON_PAIRS:
            label, ground = label.split(" on ")
            more["ground"] = "{" + REF[ground] + "}"
        if label not in REF:
            continue
        if "keyline" in cell["token"]:
            more.update(keyline="{oa.color.palette.charcoal}", keylineContrast=cell["keylineRatio"])
        if red and label == "Pillar Red":
            more.update(red)
        group[on[s]] = atok("color", REF[label], desc, tier="semantic", kind=kind, surface=s,
                            contrast=cell["ratio"], threshold=THRESH.get(kind if kind != "background" else "text"), **more)
    return group


draft = {
    "$description": ("Oath & Action V6 token schema DRAFT, 20261021. A sketch of the source format for Gate 1. "
                     "Not for use. Values are proposals; nothing here ships."),
    "$extensions": {NS: {"formatVersion": FMT, "formatReference": "https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/",
                         "tokenSetVersion": "6.0.0-draft.1", "status": "draft", "namespaceNote": "Reverse-domain key from oathandaction.org as written in V5; ownership not confirmed",
                         "needs": {
                             "N-01": "Secondary small text on Newsprint: Stone measures 4.29:1; 49 Stone-on-Newsprint text failures in the V5 census; Concepts V2 already uses #4E535C 1,606 times",
                             "N-02": "Secondary text on Charcoal and Prussian: Stone measures 3.10:1 and 2.20:1; 8 failures in the V5 census",
                             "N-03": "Error message ground that holds 13 px text: Charcoal on Pillar Red is 4.49:1 and White on Pillar Red 4.17:1",
                             "N-04": "Verdigris status marks on Prussian measure 2.80:1; held until the Phase 2 Signal Grid redesign",
                         },
                         "fontSizeExceptions": [],
                         "redRule": ("The wordmark's ampersand and the lockmark's lever are signature red and do not count. Each view (one screen, card, slide or printed page) "
                                     "then carries one working red, in this order of precedence: an error the reader must fix; the step a reader can take now; the one point "
                                     "the headline names, which in a systems figure is where a reform acts. A hinge headline's ampersand uses the view's working red. The hinge "
                                     "divider's ampersand is Charcoal. The Act handle is red only when the Act mark is itself the call to act, as on a social tile. Red never sits on Prussian."),
                         "redRuleSource": "work/handoffs/phase-1/20261021_CD-Review-Of-Phase-1.md, section 2"}},
    "oa": {
        "color": {
            "$description": "Identity, state and data color. Identity marks use palette primitives only.",
            "palette": palette,
            "derived": derived_tokens,
            "text": {
                "primary": semantic("text.primary", "Body text, headings and data values", "text"),
                "secondary": semantic("text.secondary", "Captions, metadata, labels, source lines, disabled text", "text"),
            },
            "border": {
                "strong": semantic("border.strong", "Edges of inputs and controls that a reader must find", "graphic"),
                "hairline": semantic("border.hairline", "Dividers and table rules with no meaning of their own", "decorative"),
            },
            "focus": {"ring": semantic("focus.ring", "Keyboard focus outline", "focus")},
            "state": {
                "selected": {"band": semantic("state.selected band", "Background of a selected row or option; pair with a 4 px bar and a check", "background")},
                "error": {"band": semantic("state.error band", "Background of an error message; pair with the word Error and a mark", "background"),
                          "mark": semantic("state.error mark", "Error glyph and state bar", "graphic",
                                           red={"redRole": "working", "precedence": 1})},
            },
            "identity": {
                "signature": semantic("identity.signature", "Wordmark ampersand and lockmark lever: signature red, which does not count against the view's working red",
                                      "logotype", red={"redRole": "signature"}),
                "hingeDivider": semantic("identity.hingeDivider", "Ampersand in the hinge divider", "graphic"),
            },
            "action": {
                "ask": {
                    "fill": semantic("action.ask fill", "Ask button fill: the step a reader can take now", "graphic",
                                     red={"redRole": "working", "precedence": 2}),
                    "label": semantic("action.ask label", "Ask button label, set in oa.type.ask", "largeText", requiresType="{oa.type.ask}"),
                },
                "primary": {
                    "fill": semantic("action.primary fill", "Primary button fill; also the ask button when an error holds the view's red", "graphic"),
                    "label": semantic("action.primary label", "Primary button label", "text"),
                },
            },
            "data": {
                "$description": "Data color. Reaches Pillar Red only through a future data.emphasisRed, the third claim on the view's working red. Series palettes are decided at Gate 2.",
                "emphasis": semantic("data.emphasis default", "The mark the chart title is about", "graphic"),
                "context": semantic("data.context", "Every other data mark in the same chart", "graphic"),
            },
        },
        "font": {
            "family": {
                "display": {"$type": "fontFamily", "$value": ["Inter Tight", "Arial", "sans-serif"], "$description": "Display"},
                "reading": {"$type": "fontFamily", "$value": ["Inter", "Arial", "sans-serif"], "$description": "Reading and interface"},
                "quote": {"$type": "fontFamily", "$value": ["Lora", "Georgia", "serif"], "$description": "Editorial quotation, italic only",
                          "$extensions": ext(fontStyle="italic")},
                "emailSans": {"$type": "fontFamily", "$value": ["Helvetica", "Arial", "sans-serif"], "$description": "Email display and body"},
                "emailQuote": {"$type": "fontFamily", "$value": ["Georgia", "serif"], "$description": "Email quotation, italic"},
            },
            "weight": {k: {"$type": "fontWeight", "$value": v, "$description": d} for k, v, d in
                       [("regular", 400, "Inter reading text; Lora Italic quotation"), ("medium", 500, "Lora Italic 500 for quote cards"),
                        ("semibold", 600, "Inter interface text and data labels"), ("bold", 700, "Inter labels and strong emphasis"),
                        ("extrabold", 800, "Inter Tight display and the wordmark face")]},
        },
        "type": {},
        "space": {},
        "layout": {"breakpoint": {}},
        "radius": {
            "none": dim(0, "px", "Default for every box, button and input"),
            "full": {"$type": "number", "$value": 0.5, "$description": "Circles: Signal Grid nodes, badges, round container mark",
                     "$extensions": ext(cssValue="50%")},
        },
        "border": {"width": {
            "hairline": dim(1, "px", "Dividers, keylines, chart axes"),
            "rule": dim(2, "px", "Current-page underline, focus ring"),
            "bar": dim(4, "px", "State bar beside selected, error and warning items"),
        }, "focusOffset": dim(2, "px", "Gap between control and focus ring")},
        "opacity": {
            "watermarkOnLight": {"$type": "number", "$value": 0.08, "$description": "Charcoal watermark on Newsprint or White. Decoration only",
                                 "$extensions": ext(measured=opacity["charcoal8OnNewsprint"])},
            "watermarkOnDark": {"$type": "number", "$value": 0.10, "$description": "Newsprint watermark on Charcoal or Prussian. Decoration only",
                                "$extensions": ext(measured=opacity["newsprint10OnCharcoal"])},
        },
        "motion": {
            "duration": {k: {"$type": "duration", "$value": {"value": v, "unit": "ms"}, "$description": d,
                             "$extensions": ext(reducedMotionValue={"value": 0, "unit": "ms"})}
                         for k, v, d in [("fast", 120, "Hover, focus, toggle"), ("standard", 200, "Reveal, panel, node fill"),
                                         ("slow", 320, "Page-level moves, hinge settle, ring slide"), ("stagger", 40, "Between siblings")]},
            "easing": {k: {"$type": "cubicBezier", "$value": v, "$description": d} for k, v, d in
                       [("standard", [0.2, 0, 0, 1], "Most transitions"), ("enter", [0, 0, 0.2, 1], "Arriving: panels, ampersand, lever"),
                        ("exit", [0.4, 0, 1, 1], "Leaving, at the fast duration")]},
        },
        "zIndex": {k: {"$type": "number", "$value": v, "$description": d} for k, v, d in
                   [("base", 0, "Page"), ("raised", 10, "Specimen overlays"), ("sticky", 40, "Sticky navigation"),
                    ("overlay", 90, "Menus and popovers outside the top layer"), ("skip", 100, "Skip link")]},
        "component": {
            "button": {
              "ask": {
                "fill": {on[s]: atok("color", "oa.color.action.ask.fill." + on[s], "Ask button fill", tier="component",
                                     fallback="{oa.component.button.primary.fill." + on[s] + "}",
                                     redRule="Second claim on the view's working red; when an error holds it, use the primary button") for s in SURF},
                "label": {on[s]: atok("color", "oa.color.action.ask.label." + on[s], "Ask button label", tier="component") for s in SURF},
                "keyline": {"onNewsprint": atok("color", "oa.color.border.strong.onNewsprint", "1 px edge that gives the red fill its boundary on Newsprint",
                                                tier="component")},
                "labelType": atok("typography", "oa.type.ask", "Ask button label style", tier="component"),
              },
              "primary": {
                "fill": {on[s]: atok("color", "oa.color.action.primary.fill." + on[s], "Primary button fill", tier="component") for s in SURF},
                "label": {on[s]: atok("color", "oa.color.action.primary.label." + on[s], "Primary button label", tier="component") for s in SURF},
              },
              "disabled": {
                "label": {"onWhite": atok("color", "oa.color.text.secondary.onWhite", "Disabled button label", tier="component")},
                "border": {"onWhite": atok("color", "oa.color.text.secondary.onWhite", "Disabled button edge, drawn dashed", tier="component",
                                           strokeStyle="dashed")},
              },
            },
        },
    },
}
for t in type_rows:
    fam = {"display": "oa.font.family.display", "reading": "oa.font.family.reading", "quote": "oa.font.family.quote"}[t["family"]]
    w = {400: "regular", 600: "semibold", 700: "bold", 800: "extrabold"}[t["weight"]]
    draft["oa"]["type"][t["name"]] = {
        "$type": "typography",
        "$description": TYPE_JOBS[t["name"]],
        "$value": {"fontFamily": "{" + fam + "}", "fontWeight": "{oa.font.weight." + w + "}",
                   "fontSize": {"value": t["maxRem"], "unit": "rem"}, "lineHeight": t["lineHeight"],
                   "letterSpacing": {"value": t["trackingRemAtMax"], "unit": "rem"}},
        "$extensions": ext(tier="semantic", minFontSize={"value": t["minRem"], "unit": "rem"}, cssFontSize=t["css"],
                           trackingEm=t["trackingEm"], textTransform=t["case"],
                           **({"numeric": "tabular-nums", "minusSign": "U+2212"} if t["name"] in ("dataLabel", "figure") else {})),
    }
for step, px in [("0", 0), ("050", 4), ("100", 8), ("150", 12), ("200", 16), ("300", 24), ("400", 32),
                 ("500", 40), ("600", 48), ("800", 64), ("1000", 80), ("1300", 104)]:
    draft["oa"]["space"][step] = dim(px / 16, "rem", f"{px} px")
for name, px, cols, gutter, margin in [("wide", 1440, 12, 24, 64), ("desktop", 1024, 12, 24, 40),
                                       ("tablet", 768, 8, 24, 32), ("phone", 390, 4, 16, 20), ("phoneSmall", 360, 4, 16, 16)]:
    draft["oa"]["layout"]["breakpoint"][name] = dim(px, "px", f"Design and test width {px} px",
                                                    mediaQueryEm=px / 16, columns=cols, gutterPx=gutter, marginPx=margin)
draft["oa"]["layout"]["measure"] = {
    "bodyIdeal": dim(measures["body17"]["ideal68"], "rem", "68 characters of 17 px Inter", chars=68),
    "bodyMax": dim(measures["body17"]["max75"], "rem", "75 characters of 17 px Inter", chars=75),
    "introMax": dim(measures["intro22"]["max65"], "rem", "65 characters of 22 px Inter", chars=65),
}

# 8. Write ------------------------------------------------------------------------
OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
OUT_DRAFT.parent.mkdir(parents=True, exist_ok=True)
data = {"generatedBy": "work/build/scripts/phase-1/tokens_phase1.py", "date": "2026-10-21",
        "formula": "WCAG 2.x relative luminance; OKLab per Ottosson as in CSS Color 4",
        "briefTableCheck": verify, "paletteClasses": classes, "derived": derived, "conceptsV2DarkStone": c2_info,
        "redInkVsV7": red_info, "distinctPairs": pairs, "opacity": opacity, "roles": role_rows,
        "measures": measures, "typeScale": type_rows, "typeFloorHolds": floor_ok}
OUT_DATA.write_text(json.dumps(data, indent=1), encoding="utf-8")
OUT_DRAFT.write_text(json.dumps(draft, indent=2), encoding="utf-8")

# 9. Print tables -----------------------------------------------------------------
print("Brief table check:", sum(v["match"] for v in verify), "of", len(verify), "match")
print("\nDerived")
for k, d in derived.items():
    print(k, d["hex"], d["status"], d["contrastOnSurfaces"], "oklch-equiv", d["oklchEquivalent"], "hue drift", d["oklchHueDrift"],
          d.get("textOnIt", ""))
print("\n4E535C", c2_info)
print("red", red_info)
print("pairs", pairs)
print("opacity", json.dumps(opacity))
print("\nRoles")
for row in role_rows:
    print(f"| {row['role']} | " + " | ".join(
        f"{c['token']} {c['ratio'] if c['ratio'] else ''}{'' if c['passes'] in (None, True) else ' FAIL'}" for c in row["cells"].values()) + " |")
print("\nMeasures", json.dumps(measures))
for t in type_rows:
    print(t["name"], t["css"], t["lineHeight"], t["trackingEm"])
print("floor holds", floor_ok)
print("wrote", OUT_DATA.relative_to(ROOT), "and", OUT_DRAFT.relative_to(ROOT))
