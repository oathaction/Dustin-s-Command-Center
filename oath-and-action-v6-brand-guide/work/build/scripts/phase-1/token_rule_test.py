"""The rule for adding a token (Master Brief V2 section 10), as a test.

Run:  python3 -I work/build/scripts/phase-1/token_rule_test.py [tokens.json]
Default input: work/build/tokens/20261021_Token-Schema-Draft.json

The five conditions of section 10, plus the tier and format rules in
work/ledger/20261021_Token-Architecture.md. Exit code 1 on any failure.
After the real file, it runs seven broken copies and expects each to fail,
so a check that silently passes everything is caught too.

The color math is written out again here on purpose: the test must not
share code with the generator it checks.
"""

import copy
import json
import math
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DEFAULT = ROOT / "work/build/tokens/20261021_Token-Schema-Draft.json"
NS = "org.oathandaction"
LOCKED = {"newsprint": "#DCD9D2", "charcoal": "#121212", "pillarRed": "#E63946", "prussian": "#1F2D5A",
          "stone": "#5D636D", "verdigris": "#4A7C74", "white": "#FFFFFF"}
TOWARD_OK = {"newsprint", "charcoal"}
THRESH = {"text": 4.5, "largeText": 3.0, "graphic": 3.0, "focus": 3.0}
FLOOR_REM = 13 / 16
NAME_BAD = re.compile(r"[{}.]|^\$")


# --- independent color math ---------------------------------------------------
def _rgb(h):
    h = h.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]


def _lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lum(h):
    r, g, b = map(_lin, _rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    x, y = sorted((_lum(a), _lum(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


def _lab(h):
    r, g, b = map(_lin, _rgb(h))
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return [0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s]


def _hex(L, a, b):
    l, m, s = ((L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3,
               (L - 0.0894841775 * a - 1.2914855480 * b) ** 3)
    out = []
    for c in (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
              -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
              -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s):
        c = min(1, max(0, c))
        c = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
        out.append(f"{round(c * 255):02X}")
    return "#" + "".join(out)


def mix(base, toward, t, space):
    p, q = _lab(base), _lab(toward)
    if space == "oklab":
        return _hex(*(x + (y - x) * t for x, y in zip(p, q)))
    # oklch, shorter hue arc, powerless hue below 1e-4 chroma
    def lch(v):
        C = math.hypot(v[1], v[2])
        return v[0], C, (math.degrees(math.atan2(v[2], v[1])) % 360 if C >= 1e-4 else None)
    (L1, C1, H1), (L2, C2, H2) = lch(p), lch(q)
    H1 = H2 if H1 is None else H1
    H2 = H1 if H2 is None else H2
    H1 = H1 or 0
    H2 = H2 or 0
    d = (H2 - H1) % 360
    d = d - 360 if d > 180 else d
    L, C, H = L1 + (L2 - L1) * t, C1 + (C2 - C1) * t, math.radians(H1 + d * t)
    return _hex(L, C * math.cos(H), C * math.sin(H))


# --- token walking --------------------------------------------------------------
def tokens(tree):
    out = {}

    def walk(node, path, inherited):
        typ = node.get("$type", inherited)
        for k, v in node.items():
            if k.startswith("$") or not isinstance(v, dict):
                continue
            p = path + [k]
            if "$value" in v:
                out[".".join(p)] = dict(v, **({"$type": v.get("$type", typ)}))
            else:
                walk(v, p, typ)
    walk(tree, [], None)
    return out


def css_name(path):
    parts = path.split(".")[1:]
    return "--oa-" + "-".join(re.sub(r"([a-z0-9])([A-Z])", r"\1-\2", x).lower() for x in parts)


def resolve(path, toks, seen=()):
    if path in seen:
        raise ValueError("alias cycle: " + " > ".join(seen + (path,)))
    v = toks[path]["$value"]
    if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        target = v[1:-1]
        if target not in toks:
            raise KeyError(f"{path} points to missing {target}")
        return resolve(target, toks, seen + (path,))
    return path, v


def x(t):
    return (t.get("$extensions") or {}).get(NS, {})


# --- the checks -----------------------------------------------------------------
def check(tree):
    fails = []
    toks = tokens(tree)
    meta = x(tree)
    needs = meta.get("needs", {})
    exceptions = meta.get("fontSizeExceptions", [])
    if meta.get("formatVersion") != "2025.10":
        fails.append("root: formatVersion must record the DTCG version (2025.10)")

    names = {}
    for path, t in toks.items():
        for seg in path.split("."):
            if NAME_BAD.search(seg):
                fails.append(f"{path}: name segment '{seg}' breaks the format's naming rules")
        cn = css_name(path)
        if cn in names:
            fails.append(f"{path}: CSS name {cn} collides with {names[cn]}")
        names[cn] = path
        if not t.get("$description"):
            fails.append(f"{path}: no $description (condition 5, usage notes)")
        if not t.get("$type"):
            fails.append(f"{path}: no $type")

    # locked palette, exact
    pal = {p.split(".")[-1]: t for p, t in toks.items() if p.startswith("oa.color.palette.")}
    if set(pal) != set(LOCKED):
        fails.append(f"palette: expected exactly {sorted(LOCKED)}, found {sorted(pal)}")
    for k, t in pal.items():
        if t["$value"].get("hex", "").upper() != LOCKED.get(k, "").upper():
            fails.append(f"oa.color.palette.{k}: {t['$value'].get('hex')} differs from the locked value {LOCKED.get(k)}")

    tier_of = {p: x(t).get("tier") for p, t in toks.items()}
    for path, t in toks.items():
        v = t["$value"]
        tier = tier_of[path]
        is_alias = isinstance(v, str) and v.startswith("{")
        try:
            end, val = resolve(path, toks)
        except (KeyError, ValueError) as e:
            fails.append(str(e))
            continue
        # tier rules
        if is_alias and tier == "component" and tier_of.get(v[1:-1]) != "semantic":
            fails.append(f"{path}: a component token must alias a semantic token, not {v[1:-1]}")
        if is_alias and tier == "semantic" and tier_of.get(v[1:-1]) != "primitive":
            fails.append(f"{path}: a semantic token must alias a primitive, not {v[1:-1]}")
        if tier == "primitive" and is_alias:
            fails.append(f"{path}: a primitive holds a literal value")
        status = x(toks[end]).get("status")
        if is_alias and status in ("held", "rejected"):
            fails.append(f"{path}: uses {end}, which is {status}")

        if t["$type"] == "color" and isinstance(val, dict) and val.get("alpha", 1) < 1:
            fails.append(f"{path}: a color token is never transparent; opacity has named jobs of its own")

        # conditions 1 to 4 for derived colors
        if path.startswith("oa.color.derived."):
            e = x(t)
            if e.get("need") not in needs:
                fails.append(f"{path}: condition 1, no measured need registered (need={e.get('need')})")
            d = e.get("derivation") or {}
            base = (d.get("base") or "")[1:-1].split(".")[-1]
            toward = (d.get("toward") or "")[1:-1].split(".")[-1]
            if d.get("method") != "color-mix" or d.get("space") not in ("oklab", "oklch") or base not in LOCKED \
                    or toward not in TOWARD_OK or not 0 < d.get("amount", 0) < 1:
                fails.append(f"{path}: condition 2, derivation must mix a palette color toward Newsprint or Charcoal")
            else:
                want = mix(LOCKED[base], LOCKED[toward], d["amount"], d["space"])
                if want != val["hex"].upper():
                    fails.append(f"{path}: condition 2, derivation gives {want} but the token says {val['hex']}")
            job = e.get("job", "")
            if not job or ";" in job or len(job) > 120:
                fails.append(f"{path}: condition 3, one named job in one short sentence")
            kind = e.get("kind")
            for s in e.get("surfaces", []):
                if kind in THRESH:
                    c = ratio(val["hex"], LOCKED[s])
                    if c < THRESH[kind]:
                        fails.append(f"{path}: condition 4, {c:.2f}:1 on {s} is under {THRESH[kind]}:1")
                    stored = (e.get("contrast") or {}).get(s)
                    if stored is None or abs(stored - round(c, 2)) > 0.005:
                        fails.append(f"{path}: stored contrast on {s} ({stored}) is stale; measured {c:.2f}")

        # condition 4 for every semantic color on its surface
        e = x(t)
        if tier == "semantic" and t["$type"] == "color" and e.get("surface"):
            kind, s = e.get("kind"), e["surface"]
            hexv = val["hex"]
            if kind == "background":
                ink = LOCKED["charcoal"] if s in ("newsprint", "white") else LOCKED["newsprint"]
                c, need = ratio(ink, hexv), 4.5
            elif kind in THRESH:
                c, need = ratio(hexv, LOCKED[s]), THRESH[kind]
            else:
                continue
            if c < need:
                fails.append(f"{path}: condition 4, {c:.2f}:1 is under {need}:1")
            if e.get("contrast") is not None and abs(e["contrast"] - round(c, 2)) > 0.005:
                fails.append(f"{path}: stored contrast {e['contrast']} is stale; measured {c:.2f}")

        # the 13 px floor
        if t["$type"] == "typography":
            sizes = [val.get("fontSize")] + [e.get("minFontSize")]
            for sz in sizes:
                if not sz:
                    continue
                rem = sz["value"] if sz["unit"] == "rem" else sz["value"] / 16
                if rem < FLOOR_REM - 1e-9 and path not in exceptions:
                    fails.append(f"{path}: {rem * 16:g} px is under the 13 px floor and has no exception record")

        # opacity only for named decorative jobs
        if path.startswith("oa.opacity.") and "Decoration only" not in t.get("$description", ""):
            fails.append(f"{path}: opacity tokens are decoration only and must say so")
    return fails


def mutants(tree):
    m = []
    a = copy.deepcopy(tree)
    a["oa"]["color"]["text"]["secondary"]["onNewsprint"]["$value"] = "{oa.color.palette.stone}"
    a["oa"]["color"]["text"]["secondary"]["onNewsprint"]["$extensions"][NS]["contrast"] = 4.29
    m.append(("Stone as secondary text on Newsprint", a))
    b = copy.deepcopy(tree)
    b["oa"]["color"]["derived"]["deepStone"]["$value"]["hex"] = "#4E535C"
    m.append(("Deep Stone hex that its derivation does not produce", b))
    c = copy.deepcopy(tree)
    c["oa"]["component"]["button"]["disabled"]["label"]["onWhite"]["$value"] = "{oa.color.palette.stone}"
    m.append(("Component token aliasing a primitive", c))
    d = copy.deepcopy(tree)
    d["oa"]["type"]["label"]["$value"]["fontSize"] = {"value": 0.6875, "unit": "rem"}
    m.append(("11 px label with no exception", d))
    e = copy.deepcopy(tree)
    e["oa"]["color"]["palette"]["pillarRed"]["$value"]["hex"] = "#BD2C32"
    m.append(("Locked Pillar Red changed", e))
    f = copy.deepcopy(tree)
    f["oa"]["color"]["derived"]["deepStone"]["$extensions"][NS]["need"] = "N-99"
    m.append(("Derived color with no registered need", f))
    g = copy.deepcopy(tree)
    g["oa"]["color"]["text"]["primary"]["onWhite"]["$value"] = "{oa.color.derived.verdigrisOnDark}"
    m.append(("Semantic token using a held value", g))
    return m


def main():
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    tree = json.loads(path.read_text(encoding="utf-8"))
    n = len(tokens(tree))
    fails = check(tree)
    print(f"{path.name}: {n} tokens, {len(fails)} failures")
    for f in fails:
        print("  FAIL", f)
    caught = 0
    muts = mutants(tree)
    for label, mt in muts:
        got = [f for f in check(mt) if f not in fails]
        ok = len(got) > 0
        caught += ok
        print(f"  mutant {'caught' if ok else 'MISSED'}: {label}" + (f" -> {got[0]}" if ok else ""))
    print(f"mutants caught: {caught} of {len(muts)}")
    sys.exit(0 if not fails and caught == len(muts) else 1)


if __name__ == "__main__":
    main()
