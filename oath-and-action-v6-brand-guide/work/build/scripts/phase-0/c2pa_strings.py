"""Phase 0 rights inventory: print readable provenance strings from C2PA data.

Read-only. For each file given, finds the PNG caBX chunk (C2PA JUMBF store)
or any JUMBF box and prints the printable ASCII runs that carry claim
generator, software agent, digital source type, action and date fields.
No C2PA library is available offline, so this is a string-level read and
does not validate signatures.

Usage: python3 -I c2pa_strings.py FILE [FILE ...]
"""
import re
import struct
import sys
from pathlib import Path

KEEP = re.compile(
    r"(claim_generator|softwareAgent|digitalSourceType|trainedAlgorithmic|"
    r"OpenAI|ChatGPT|GPT|DALL|sora|c2pa\.(created|edited|converted|opened|actions|hash|ingredient)|"
    r"when|20\d\d-\d\d-\d\d|Truepic|issuer|CN=|O=|name|title|format|"
    r"CleanShot|Apple|macOS|Adobe|Google|Microsoft|Gemini)",
    re.I,
)


def png_chunks(raw):
    pos = 8
    while pos + 8 <= len(raw):
        length, ctype = struct.unpack(">I4s", raw[pos:pos + 8])
        data = raw[pos + 8:pos + 8 + length]
        yield ctype.decode("latin-1"), data
        pos += 12 + length


def strings(blob, minlen=4):
    for m in re.finditer(rb"[\x20-\x7e]{%d,}" % minlen, blob):
        yield m.group(0).decode("ascii")


def main():
    for arg in sys.argv[1:]:
        path = Path(arg)
        raw = path.read_bytes()
        print("=" * 70)
        print(path.name)
        stores = []
        if raw[:8] == b"\x89PNG\r\n\x1a\n":
            for ctype, data in png_chunks(raw):
                if ctype == "caBX":
                    stores.append(("caBX", data))
        if not stores:
            i = raw.find(b"jumb")
            if i >= 0:
                stores.append(("jumb@%d" % i, raw[max(0, i - 8): i + 200000]))
            i = raw.find(b"c2pa")
            if i >= 0 and not stores:
                stores.append(("c2pa@%d" % i, raw[max(0, i - 400): i + 400]))
        for label, blob in stores:
            print("--", label, len(blob), "bytes")
            seen = set()
            for s in strings(blob):
                if KEEP.search(s) and s not in seen:
                    seen.add(s)
                    print("   ", s[:200])


if __name__ == "__main__":
    main()
