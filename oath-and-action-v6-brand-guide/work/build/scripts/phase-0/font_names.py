"""Phase 0 rights inventory: read font name tables and embedding flags.

Read-only. Reads
  1. the TTF files already extracted to work/extract/v5-polished/fonts/
  2. every font data URI inside each source HTML (decoded in memory only;
     nothing is written to source/ or work/extract/)
and writes work/handoffs/phase-0/20261020_Rights-Font-Name-Tables.json.

For each font it records: sha256, format, name IDs 0-6, 8-14, 16, 17,
OS/2 fsType (embedding permission bits), OS/2 vendor ID, head fontRevision,
glyph count and whether the font is variable (fvar).

Usage: python3 -I font_names.py <ROOT>
"""
import base64
import hashlib
import io
import json
import re
import site
import sys
from pathlib import Path

# -I drops user site-packages; fontTools was installed with --user.
sys.path.append(site.getusersitepackages())
from fontTools.ttLib import TTFont  # noqa: E402

ROOT = Path(sys.argv[1]).resolve()
OUT = ROOT / "work/handoffs/phase-0/20261020_Rights-Font-Name-Tables.json"
NAME_IDS = {
    0: "copyright", 1: "family", 2: "subfamily", 3: "unique_id",
    4: "full_name", 5: "version", 6: "postscript_name", 7: "trademark",
    8: "manufacturer", 9: "designer", 10: "description", 11: "vendor_url",
    12: "designer_url", 13: "license_description", 14: "license_url",
    16: "typographic_family", 17: "typographic_subfamily",
}
FSTYPE_BITS = {
    0x0002: "Restricted License embedding",
    0x0004: "Preview & Print embedding",
    0x0008: "Editable embedding",
    0x0100: "No subsetting",
    0x0200: "Bitmap embedding only",
}
DATA_URI = re.compile(
    rb"url\(\s*['\"]?data:(font/[a-z0-9]+|application/(?:x-)?font-[a-z0-9]+|application/octet-stream)"
    rb"(?:;[a-z0-9=+-]+)*;base64,([A-Za-z0-9+/=\s]+)['\"]?\s*\)",
    re.I,
)
FAMILY_NEAR = re.compile(rb"font-family\s*:\s*['\"]?([^;'\"]+)['\"]?", re.I)


def describe(raw, label):
    rec = {"label": label, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}
    try:
        font = TTFont(io.BytesIO(raw), lazy=True)
    except Exception as exc:
        rec["error"] = repr(exc)
        return rec
    rec["flavor"] = font.flavor or "ttf/otf"
    names = {}
    for nid, key in NAME_IDS.items():
        rec_name = font["name"].getName(nid, 3, 1, 0x409) or font["name"].getName(nid, 1, 0, 0)
        if rec_name is not None:
            names[key] = str(rec_name)
    rec["names"] = names
    os2 = font["OS/2"] if "OS/2" in font else None
    if os2 is not None:
        fs = os2.fsType
        rec["fsType"] = fs
        if fs == 0:
            rec["fsType_meaning"] = "0: Installable embedding (no restriction)"
        else:
            rec["fsType_meaning"] = ", ".join(v for b, v in FSTYPE_BITS.items() if fs & b)
        rec["vendor_id"] = os2.achVendID
        rec["weight_class"] = os2.usWeightClass
    rec["head_fontRevision"] = round(font["head"].fontRevision, 3)
    rec["glyphs"] = font["maxp"].numGlyphs
    rec["variable"] = "fvar" in font
    if rec["variable"]:
        rec["axes"] = [(a.axisTag, a.minValue, a.defaultValue, a.maxValue) for a in font["fvar"].axes]
    return rec


def main():
    result = {"v5_polished_extracted": [], "sources": {}}
    for ttf in sorted((ROOT / "work/extract/v5-polished/fonts").glob("*.ttf")):
        rec = describe(ttf.read_bytes(), ttf.name)
        rec["file"] = str(ttf.relative_to(ROOT))
        result["v5_polished_extracted"].append(rec)
    for html in sorted((ROOT / "source").glob("*.html")):
        raw = html.read_bytes()
        fonts = []
        for m in DATA_URI.finditer(raw):
            start = raw.rfind(b"@font-face", 0, m.start())
            block = raw[start:m.start()] if start >= 0 else b""
            fam = FAMILY_NEAR.search(block)
            data = base64.b64decode(re.sub(rb"\s+", b"", m.group(2)))
            rec = describe(data, "data-uri")
            rec["mime"] = m.group(1).decode()
            rec["css_family"] = fam.group(1).decode("utf-8", "replace").strip() if fam else None
            end = raw.find(b"}", m.end())
            face = block + raw[m.end():end if end >= 0 else m.end()]
            wt = re.search(rb"font-weight\s*:\s*([0-9a-z]+)", face, re.I)
            st = re.search(rb"font-style\s*:\s*([a-z]+)", face, re.I)
            rec["css_weight"] = wt.group(1).decode() if wt else None
            rec["css_style"] = st.group(1).decode() if st else None
            fonts.append(rec)
        result["sources"][html.name] = fonts
    OUT.write_text(json.dumps(result, indent=1))
    print("wrote", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
