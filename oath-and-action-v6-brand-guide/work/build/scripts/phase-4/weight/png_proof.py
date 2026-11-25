"""3b's proof (DR-331): every PNG the page shows, decoded from the page built with C1 off and from the page built with C1 on, in
page order; the same size and the same RGBA value at every pixel, image by image.

  python3 -I png_proof.py OFF.html ON.html
"""
import base64
import hashlib
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from c1 import SHOWN_PNG, rgba  # noqa: E402


def main():
    a = [base64.b64decode(m.group(2)) for m in SHOWN_PNG.finditer(Path(sys.argv[1]).read_text(encoding="utf-8"))]
    b = [base64.b64decode(m.group(2)) for m in SHOWN_PNG.finditer(Path(sys.argv[2]).read_text(encoding="utf-8"))]
    if len(a) != len(b):
        print(f"FAIL: {len(a)} PNGs with C1 off, {len(b)} with C1 on")
        sys.exit(1)
    same, changed, seen = 0, 0, set()
    for x, y in zip(a, b):
        key = hashlib.sha256(x).hexdigest()
        sx, px, _ = rgba(x)
        sy, py, _ = rgba(y)
        ok = sx == sy and px == py
        same += ok
        changed += x != y
        if key not in seen:
            seen.add(key)
            print(f"{'same' if ok else 'DIFFERENT'} {key[:16]} {sx[0]}x{sx[1]}: {len(x):,} -> {len(y):,} bytes")
    print(f"{same} of {len(a)} PNGs decode to the same pixels ({len(seen)} distinct; {changed} re-encoded)")
    sys.exit(0 if same == len(a) else 1)


if __name__ == "__main__":
    main()
