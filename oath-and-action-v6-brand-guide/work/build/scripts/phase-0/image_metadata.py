"""Phase 0 rights inventory: collect metadata for every reference image.

Read-only. Reads the contact-sheet index and the icon studies, and writes
work/handoffs/phase-0/20261020_Rights-Image-Metadata.json with, for each file:
size, sha256, format, dimensions, EXIF and XMP fields of interest,
PNG text chunks, and byte markers for C2PA / JUMBF / IPTC provenance.

Run from anywhere with: python3 -I <this file> <ROOT>
"""
import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image, ExifTags

ROOT = Path(sys.argv[1]).resolve()
INDEX = ROOT / "work/boards/screens/references/index.json"
OUT = ROOT / "work/handoffs/phase-0/20261020_Rights-Image-Metadata.json"

MARKERS = {
    "c2pa": b"c2pa",
    "jumbf": b"jumb",
    "caBX_chunk": b"caBX",
    "openai": b"OpenAI",
    "chatgpt": b"ChatGPT",
    "dall-e": b"DALL",
    "gemini": b"Gemini",
    "google_ai": b"Google AI",
    "imagen": b"Imagen",
    "midjourney": b"Midjourney",
    "firefly": b"Firefly",
    "adobe_stock": b"Adobe Stock",
    "stock.adobe": b"stock.adobe",
    "istock": b"iStock",
    "getty": b"Getty",
    "shutterstock": b"Shutterstock",
    "alamy": b"Alamy",
    "freepik": b"Freepik",
    "trainedAlgorithmicMedia": b"trainedAlgorithmicMedia",
    "compositeWithTrained": b"compositeWithTrainedAlgorithmicMedia",
    "ai_generated": b"AI generated",
    "stable_diffusion": b"Stable Diffusion",
    "parameters_chunk": b"parameters",
    "photoshop": b"Photoshop",
    "canva": b"Canva",
    "figma": b"Figma",
    "snipping": b"Snipping",
    "screenshot": b"Screenshot",
    "iptc_8bim": b"8BIM",
    "xmp": b"<x:xmpmeta",
}

XMP_KEYS = [
    "dc:creator", "dc:rights", "photoshop:Credit", "photoshop:Source",
    "xmpRights:WebStatement", "xmpRights:UsageTerms", "Iptc4xmpCore",
    "plus:Licensor", "xmp:CreatorTool", "DigitalSourceType",
    "photoshop:AuthorsPosition", "dc:title", "dc:description",
]


def exif_fields(img):
    out = {}
    try:
        exif = img.getexif()
    except Exception:
        return out
    for tag_id, val in exif.items():
        name = ExifTags.TAGS.get(tag_id, str(tag_id))
        if name in ("Artist", "Copyright", "Software", "ImageDescription",
                    "Make", "Model", "DateTime", "XPAuthor", "XPComment",
                    "UserComment", "HostComputer"):
            if isinstance(val, bytes):
                val = val.decode("utf-16-le" if name.startswith("XP") else "latin-1", "replace").strip("\x00")
            out[name] = str(val)[:300]
    return out


def xmp_fields(raw):
    out = {}
    m = re.search(rb"<x:xmpmeta.*?</x:xmpmeta>", raw, re.S)
    if not m:
        return out
    xmp = m.group(0).decode("utf-8", "replace")
    for key in XMP_KEYS:
        pattern = re.escape(key) + r'(?:="([^"]*)"|[^>]*>(.*?)</' + re.escape(key) + ">)"
        for mm in re.finditer(pattern, xmp, re.S):
            val = (mm.group(1) or mm.group(2) or "").strip()
            val = re.sub(r"<[^>]+>", " ", val)
            val = re.sub(r"\s+", " ", val).strip()
            if val:
                out.setdefault(key, []).append(val[:300])
    return out


def one(path):
    raw = path.read_bytes()
    rec = {
        "file": str(path.relative_to(ROOT)),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
    }
    try:
        with Image.open(path) as img:
            rec["format"] = img.format
            rec["width"], rec["height"] = img.size
            rec["mode"] = img.mode
            rec["exif"] = exif_fields(img)
            info = {}
            for k, v in (img.info or {}).items():
                if k in ("icc_profile", "exif", "xmp", "photoshop"):
                    info[k] = f"<{len(v)} bytes>" if isinstance(v, (bytes, bytearray)) else str(v)[:80]
                else:
                    info[k] = str(v)[:400]
            rec["info"] = info
    except Exception as exc:  # pragma: no cover
        rec["error"] = repr(exc)
    rec["markers"] = sorted(k for k, b in MARKERS.items() if b in raw)
    rec["xmp"] = xmp_fields(raw)
    return rec


def main():
    index = json.loads(INDEX.read_text())
    records = {}
    for set_name, files in index.items():
        if not isinstance(files, list):
            continue
        records[set_name] = []
        for n, rel in enumerate(files, 1):
            rec = one(ROOT / rel)
            rec["sheet_number"] = n
            records[set_name].append(rec)
    OUT.write_text(json.dumps(records, indent=1))
    for set_name, recs in records.items():
        print(set_name, len(recs))


if __name__ == "__main__":
    main()
