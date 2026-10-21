"""Phase 1 research lead: read-only metadata check for source/brand-mockups/*.webp.

Lists RIFF chunks (VP8, VP8L, VP8X, EXIF, XMP, ICCP), canvas size, SHA-256,
and any printable provenance strings (C2PA, OpenAI, digitalSourceType).
Run: python3 -I work/build/scripts/phase-1/mockup_metadata.py FILE [FILE ...]
"""
import hashlib, re, struct, sys

def chunks(raw):
    pos = 12
    while pos + 8 <= len(raw):
        fourcc = raw[pos:pos + 4].decode("latin-1")
        size = struct.unpack("<I", raw[pos + 4:pos + 8])[0]
        yield fourcc, raw[pos + 8:pos + 8 + size]
        pos += 8 + size + (size & 1)

def size_of(fourcc, data):
    if fourcc == "VP8X":
        w = 1 + int.from_bytes(data[4:7], "little"); h = 1 + int.from_bytes(data[7:10], "little"); return w, h
    if fourcc == "VP8 ":
        w, h = struct.unpack("<HH", data[6:10]); return w & 0x3FFF, h & 0x3FFF
    if fourcc == "VP8L":
        b = int.from_bytes(data[1:5], "little"); return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    return None

for path in sys.argv[1:]:
    raw = open(path, "rb").read()
    print(path.split("/")[-1], len(raw), hashlib.sha256(raw).hexdigest()[:16])
    for fourcc, data in chunks(raw):
        s = size_of(fourcc, data)
        print("  chunk", repr(fourcc), len(data), s if s else "")
        if fourcc in ("EXIF", "XMP ", "C2PA") or fourcc.startswith("c2p"):
            for m in re.finditer(rb"[\x20-\x7e]{6,}", data):
                t = m.group(0).decode()
                if re.search(r"OpenAI|ChatGPT|GPT|c2pa|SourceType|trained|Software|Creator|Date|Adobe|Google", t, re.I):
                    print("    ", t[:160])
    hits = set(re.findall(rb"(OpenAI|ChatGPT|c2pa|trainedAlgorithmicMedia|jumb)", raw))
    print("  provenance strings anywhere:", sorted(h.decode() for h in hits) or "none")
