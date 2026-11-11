"""Fetch the guide's three typefaces from Google Fonts, unmodified, with their licenses, and prove them (Gate 2, D2-1697).

Usage, from the project folder:
  python3 -I work/build/scripts/phase-2/fonts_fetch.py            fetch the files, the three OFL texts and the manifest
  python3 -I work/build/scripts/phase-2/fonts_fetch.py --check    every file on disk matches its manifest row, byte for byte
  python3 -I work/build/scripts/phase-2/fonts_fetch.py --page P   the page P embeds every manifest file once, each data URL
                                                                  decoding to the manifest's bytes, and asks no server for a font

What it fetches. Rule 06.1's one set (Gate 2 fix pass, CD-M1), the link a product loads (Rule 06.10):
  Inter 400, 600 and 700; Inter Tight 800; Lora Italic 400 and 500.
Google serves each family as one variable WOFF2 file per script subset, the same file for every weight of a style. The
script asks for the page's own stylesheet with a current Chrome user agent (the version of the Chromium the guide's
checks run in), keeps the latin and latin-ext subsets (KEEP below, and the engineer's Gate 2 notes for why) and saves each
file exactly as served: no subsetting, no conversion, and no change to the font's names. Each file is stored under the
project's dated file name; the manifest names the URL it came from. Each family's OFL 1.1 text comes from the google/fonts
repository as published.

The manifest, work/build/assets/fonts/20261111_Font-Manifest.json, lists per file: family, style, the weights Google
declares for it, subset, unicode-range, URL, bytes, SHA-256 and the date fetched; per family: authors' copyright line,
license, reserved font name and the OFL text's path, URL, bytes and SHA-256. guide_build.py reads it to embed the fonts.
"""
import argparse
import base64
import datetime
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
FONTS = ROOT / "work/build/assets/fonts"
MANIFEST = FONTS / "20261111_Font-Manifest.json"
# Gate 2 fix pass (CD-M1): Rule 06.1's one weight set, the link a product loads (Rule 06.10). Google serves the same
# variable files for Inter and Lora as for the wider link the page loaded before; for Inter Tight at 800 alone it serves a
# file of that one weight, which replaces the variable file fetched first.
CSS_URL = ("https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800"
           "&family=Lora:ital,wght@1,400;1,500&display=swap")
# Chromium 153 is the browser guide_check.js runs in (Playwright's local build); a desktop Chrome of the same version
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36"
KEEP = ("latin", "latin-ext")
FAMILIES = {
    "Inter": {"dir": "inter", "file": "Inter", "ofl": "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/OFL.txt",
              "authors": "The Inter Project Authors", "reserved_name": None, "rights_id": "T-INTER"},
    "Inter Tight": {"dir": "inter-tight", "file": "Inter-Tight", "ofl": "https://raw.githubusercontent.com/google/fonts/main/ofl/intertight/OFL.txt",
                    "authors": "The Inter Project Authors", "reserved_name": None, "rights_id": "T-INTERTIGHT"},
    "Lora": {"dir": "lora", "file": "Lora", "ofl": "https://raw.githubusercontent.com/google/fonts/main/ofl/lora/OFL.txt",
             "authors": "The Lora Project Authors", "reserved_name": "Lora", "rights_id": "T-LORA"},
}
DATE = "20261111"


def get(url, ua=UA):
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def parse_css(css):
    """Google's stylesheet: one @font-face per family, style, weight and subset, each after a /* subset */ comment."""
    faces = []
    for m in re.finditer(r"/\*\s*([a-z0-9-]+)\s*\*/\s*@font-face\s*\{(.*?)\}", css, re.S):
        sub, body = m.group(1), m.group(2)
        val = lambda k: re.search(k + r":\s*([^;]+);", body).group(1).strip()
        url = re.search(r"src:\s*url\(([^)]+)\)\s*format\('woff2'\)", body).group(1)
        faces.append({"subset": sub, "family": val("font-family").strip("'\""), "style": val("font-style"),
                      "weight": int(val("font-weight")), "display": val("font-display"), "url": url, "unicode_range": val("unicode-range")})
    return faces


def fetch():
    today = datetime.date.today().isoformat()
    css = get(CSS_URL).decode()
    faces = parse_css(css)
    if not faces:
        sys.exit("Google's stylesheet held no @font-face this script can read")
    files = {}
    for f in faces:
        if f["subset"] not in KEEP:
            continue
        key = f["url"]
        if key in files:
            files[key]["weights"].append(f["weight"])
            if files[key]["unicode_range"] != f["unicode_range"]:
                sys.exit(f"one file, two unicode ranges: {key}")
            continue
        fam = FAMILIES[f["family"]]
        style = "Italic" if f["style"] == "italic" else ""
        sub = "-".join(w.capitalize() for w in f["subset"].split("-"))
        name = f"{DATE}_{fam['file']}{'-' + style if style else ''}-{sub}.woff2"
        files[key] = {"file": f"{fam['dir']}/{name}", "family": f["family"], "style": f["style"], "weights": [f["weight"]],
                      "subset": f["subset"], "unicode_range": f["unicode_range"], "display": f["display"], "url": key}
    for key, row in files.items():
        data = get(key)
        if data[:4] != b"wOF2":
            sys.exit(f"{key} is not a WOFF2 file (starts {data[:4]!r})")
        out = FONTS / row["file"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        row.update({"bytes": len(data), "sha256": sha(data), "fetched": today})
        print(f"  {row['file']}  {len(data):,} bytes  {row['family']} {row['style']} {row['weights']} {row['subset']}")
    fams = {}
    for name, fam in FAMILIES.items():
        txt = get(fam["ofl"], ua="oa-guide-build")
        p = FONTS / fam["dir"] / "OFL.txt"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(txt)
        first = txt.decode("utf-8").splitlines()[0].strip()
        if "SIL Open Font License, Version 1.1" not in txt.decode("utf-8"):
            sys.exit(f"{fam['ofl']} does not read as the SIL Open Font License 1.1")
        fams[name] = {"rights_id": fam["rights_id"], "copyright": first, "authors": fam["authors"], "license": "SIL Open Font License 1.1",
                      "reserved_font_name": fam["reserved_name"], "ofl": {"file": f"{fam['dir']}/OFL.txt", "url": fam["ofl"], "bytes": len(txt),
                                                                          "sha256": sha(txt), "fetched": today}}
        print(f"  {fam['dir']}/OFL.txt  {len(txt):,} bytes  {first}")
    skipped = sorted({(f["family"], f["subset"]) for f in faces if f["subset"] not in KEEP})
    manifest = {
        "about": "The guide's three typefaces as Google Fonts serves them, unmodified, with their OFL 1.1 texts (Gate 2, D2-1697). "
                 "Written by work/build/scripts/phase-2/fonts_fetch.py; guide_build.py embeds every file listed here as an @font-face data URL.",
        "stylesheet": CSS_URL, "user_agent": UA, "fetched": today, "subsets_kept": list(KEEP),
        "subsets_left": [f"{a} {b}" for a, b in skipped],
        "families": fams,
        "files": sorted(files.values(), key=lambda r: (r["family"], r["subset"])),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    print(f"wrote {MANIFEST.relative_to(ROOT)}: {len(files)} font files, {sum(r['bytes'] for r in files.values()):,} bytes")
    return 0


def load_manifest():
    return json.loads(MANIFEST.read_text())


def check_files():
    m = load_manifest()
    bad = []
    rows = list(m["files"]) + [dict(f["ofl"], family=k) for k, f in m["families"].items()]
    for r in rows:
        p = FONTS / r["file"]
        if not p.exists():
            bad.append(f"{r['file']}: missing")
            continue
        b = p.read_bytes()
        if len(b) != r["bytes"] or sha(b) != r["sha256"]:
            bad.append(f"{r['file']}: {len(b):,} bytes, SHA-256 {sha(b)[:12]}; the manifest says {r['bytes']:,} and {r['sha256'][:12]}")
    extra = sorted(str(p.relative_to(FONTS)) for p in FONTS.rglob("*") if p.is_file() and p != MANIFEST
                   and str(p.relative_to(FONTS)) not in {r["file"] for r in rows})
    for x in extra:
        bad.append(f"{x}: on disk but not in the manifest")
    for b in bad:
        print("  FAIL " + b)
    print(f"{'PASS' if not bad else 'FAIL'} font files: {len(rows) - len([b for b in bad if 'missing' in b])} of {len(rows)} present, "
          f"{len(bad)} problem(s)")
    return 0 if not bad else 1


FACE = re.compile(r"@font-face\s*\{(.*?)\}", re.S)


def check_page(page_path):
    m = load_manifest()
    page = Path(page_path).read_text()
    bad = []
    seen = {}
    faces = FACE.findall(page)
    for body in faces:
        fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", body)
        fam = fam.group(1) if fam else "?"
        if fam not in m["families"]:
            continue   # a specimen's own face, if one ever carries one, is not the guide's
        for u in re.findall(r"url\(\s*['\"]?([^'\")]+)", body):
            if not u.startswith("data:"):
                bad.append(f"{fam}: an @font-face asks a server for {u[:80]}")
                continue
            mt = re.match(r"data:([^;,]+)(;base64)?,(.*)", u, re.S)
            if not mt or not mt.group(2):
                bad.append(f"{fam}: a data URL that is not base64")
                continue
            data = base64.b64decode(mt.group(3))
            h = sha(data)
            seen[h] = seen.get(h, 0) + 1
            rng = re.search(r"unicode-range:\s*([^;]+);", body)
            row = next((r for r in m["files"] if r["sha256"] == h), None)
            if not row:
                bad.append(f"{fam}: an embedded font of {len(data):,} bytes, SHA-256 {h[:12]}, matches no manifest file")
            elif not rng or rng.group(1).strip() != row["unicode_range"]:
                bad.append(f"{row['file']}: embedded with unicode-range {rng.group(1).strip() if rng else 'none'}, the manifest's is {row['unicode_range']}")
    for r in m["files"]:
        n = seen.get(r["sha256"], 0)
        if n != 1:
            bad.append(f"{r['file']}: embedded {n} time(s); each file goes in once")
    # The page may print a fonts link as code a builder copies; it may not load one: no <link>, no @import, no url() to
    # a font host in markup or a stylesheet
    for pat, what in ((r"<link\b[^>]*fonts\.(?:googleapis|gstatic)\.com", "a <link> to Google Fonts"),
                      (r"@import[^;]*fonts\.(?:googleapis|gstatic)\.com", "an @import of Google Fonts"),
                      (r"url\(\s*['\"]?https?://fonts\.(?:googleapis|gstatic)\.com", "a url() to Google Fonts")):
        n = len(re.findall(pat, page))
        if n:
            bad.append(f"the page holds {n} {what}")
    # Each family's OFL.txt in full, in its disclosure: the words of the file in order, lines of hyphens aside
    import html as _html
    words = lambda t: [w for w in re.sub(r"(?m)^-{3,}$", " ", t).split()]
    for k, f in m["families"].items():
        txt = (FONTS / f["ofl"]["file"]).read_text()
        blk = re.search(r'<div class="lic-body" data-license="' + re.escape(k) + r'">(.*?)</div>', page, re.S)
        if not blk:
            bad.append(f"{k}: no license disclosure holds its OFL text")
            continue
        shown = _html.unescape(re.sub(r"<[^>]+>", " ", blk.group(1)))
        if words(shown) != words(txt):
            a, b = words(shown), words(txt)
            i = next((j for j in range(min(len(a), len(b))) if a[j] != b[j]), min(len(a), len(b)))
            bad.append(f"{k}: the license on the page departs from OFL.txt at word {i + 1} of {len(b)} "
                       f"(page {' '.join(a[i:i + 5])!r}, file {' '.join(b[i:i + 5])!r})")
    for b in bad:
        print("  FAIL " + b)
    n_bytes = sum(r["bytes"] for r in m["files"])
    print(f"{'PASS' if not bad else 'FAIL'} embedded fonts in {Path(page_path).name}: {sum(seen.values())} data URL(s) for "
          f"{len(m['files'])} manifest file(s) of {n_bytes:,} bytes, each matched by SHA-256; {len(bad)} problem(s)")
    return 0 if not bad else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="check the files on disk against the manifest")
    ap.add_argument("--page", help="check a built page's embedded fonts against the manifest")
    a = ap.parse_args()
    if a.page:
        rc = check_files()
        sys.exit(rc | check_page(a.page))
    sys.exit(check_files() if a.check else fetch())


if __name__ == "__main__":
    main()
