"""Write an ICO file from square PNGs, each kept whole inside it (chat 11, contract C6). A PNG inside an ICO is read by every
browser that reads favicons and by Windows from Vista on; each entry keeps the pixels the kit drew at that size, with no
resampling here.

Usage: python3 -I work/build/app-kit/tools/ico.py OUT.ico IN-16.png IN-32.png IN-48.png
       python3 -I work/build/app-kit/tools/ico.py --read FILE.ico        (prints each entry's size and format)
       python3 -I work/build/app-kit/tools/ico.py --self-test
"""
import io
import struct
import sys
from pathlib import Path


def png_size(data):
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG")
    return struct.unpack(">II", data[16:24])


def write(out, pngs):
    datas = [Path(p).read_bytes() for p in pngs]
    sizes = [png_size(d) for d in datas]
    for (w, h), p in zip(sizes, pngs):
        if w != h or w > 256:
            raise ValueError(f"{p} is {w} by {h}; an ICO entry is square and at most 256 px")
    head = struct.pack("<HHH", 0, 1, len(datas))
    offset = 6 + 16 * len(datas)
    entries, body = b"", b""
    for (w, h), d in zip(sizes, datas):
        entries += struct.pack("<BBBBHHII", w % 256, h % 256, 0, 0, 1, 32, len(d), offset + len(body))
        body += d
    Path(out).write_bytes(head + entries + body)


def read(path):
    data = Path(path).read_bytes()
    reserved, kind, n = struct.unpack("<HHH", data[:6])
    if reserved != 0 or kind != 1:
        raise ValueError("not an icon file")
    out = []
    for i in range(n):
        w, h, _, _, _, bpp, size, off = struct.unpack("<BBBBHHII", data[6 + 16 * i:22 + 16 * i])
        payload = data[off:off + size]
        fmt = "png" if payload[:8] == b"\x89PNG\r\n\x1a\n" else "bmp"
        pw, ph = png_size(payload) if fmt == "png" else (w or 256, h or 256)
        out.append({"width": pw, "height": ph, "dir_width": w or 256, "dir_height": h or 256, "bpp": bpp, "format": fmt, "bytes": size})
    return out


def self_test():
    import tempfile
    from PIL import Image
    bad = 0
    with tempfile.TemporaryDirectory() as t:
        d = Path(t)
        for s in (16, 32, 48):
            Image.new("RGBA", (s, s), (230, 57, 70, 255)).save(d / f"{s}.png")
        write(d / "x.ico", [d / "16.png", d / "32.png", d / "48.png"])
        r = read(d / "x.ico")
        ok = [(e["width"], e["format"]) for e in r] == [(16, "png"), (32, "png"), (48, "png")]
        with Image.open(d / "x.ico") as im:
            ok = ok and sorted(im.info.get("sizes", [])) == [(16, 16), (32, 32), (48, 48)]
        print(f"{'pass' if ok else 'FAIL'} three PNGs make one ICO that the reader and Pillow both read as 16, 32 and 48 px")
        bad += not ok
        Image.new("RGBA", (32, 16)).save(d / "w.png")
        try:
            write(d / "y.ico", [d / "w.png"])
            ok = False
        except ValueError:
            ok = True
        print(f"{'pass' if ok else 'FAIL'} a PNG that is not square is refused")
        bad += not ok
    return bad


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--self-test"]:
        sys.exit(1 if self_test() else 0)
    if a[:1] == ["--read"]:
        for e in read(a[1]):
            print(e)
        sys.exit(0)
    if len(a) < 2:
        print(__doc__)
        sys.exit(2)
    write(a[0], a[1:])
