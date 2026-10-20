"""Split the large supplied HTML files into reviewable parts.

Usage: python3 -I extract_sources.py <project-root>

Reads only from source/. Writes only to work/extract/. Never edits a source file.
"""
import base64
import hashlib
import html
import json
import os
import re
import sys
import zipfile

ROOT = os.path.abspath(sys.argv[1])
SRC = os.path.join(ROOT, "source")
OUT = os.path.join(ROOT, "work", "extract")

DATA_URI = re.compile(r"data:([a-z0-9.+/-]+);base64,([A-Za-z0-9+/=]+)", re.I)
EXT = {"font/woff2": "woff2", "font/woff": "woff", "application/font-woff2": "woff2",
       "application/font-woff": "woff", "font/ttf": "ttf", "font/otf": "otf",
       "image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/svg+xml": "svg",
       "image/gif": "gif"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def write(path, text, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as f:
        f.write(text)


def strip_data_uris(text, store):
    """Replace base64 data URIs with a short reference and save the payload."""
    def repl(m):
        mime, payload = m.group(1).lower(), m.group(2)
        digest = hashlib.sha1(payload.encode()).hexdigest()[:10]
        name = f"{digest}.{EXT.get(mime, 'bin')}"
        store.setdefault(name, (mime, payload))
        return f"[[data-uri:{name}]]"
    return DATA_URI.sub(repl, text)


def to_text(fragment):
    fragment = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<svg[^>]*>.*?</svg>", " [svg] ", fragment, flags=re.S | re.I)
    fragment = re.sub(r"<br\s*/?>|</(p|h[1-6]|li|tr|figcaption|div|dt|dd|caption)>", "\n", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", " ", fragment)
    fragment = html.unescape(fragment)
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in fragment.splitlines()]
    out, blank = [], False
    for ln in lines:
        if ln:
            out.append(ln)
            blank = False
        elif not blank:
            out.append("")
            blank = True
    return "\n".join(out).strip() + "\n"


def sections(h):
    """Top-level <section> blocks with their ids, in document order."""
    found = []
    for m in re.finditer(r"<section\b[^>]*>", h, re.I):
        start = m.start()
        depth, i = 0, start
        tag = re.compile(r"<(/?)section\b[^>]*>", re.I)
        for t in tag.finditer(h, start):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                i = t.end()
                break
        if any(s <= start < e for s, e, _ in found):
            continue
        sid = re.search(r'id="([^"]+)"', m.group(0))
        found.append((start, i, sid.group(1) if sid else f"section-{len(found)}"))
    return found


def extract_html(name, slug, full):
    path = os.path.join(SRC, name)
    h = read(path)
    out = os.path.join(OUT, slug)
    store = {}
    inv = {"file": name, "chars": len(h)}

    styles = re.findall(r"<style[^>]*>(.*?)</style>", h, re.S | re.I)
    scripts = re.findall(r"<script(?![^>]*application/json)[^>]*>(.*?)</script>", h, re.S | re.I)
    json_blocks = re.findall(r'<script[^>]*type="application/json"[^>]*id="([^"]+)"[^>]*>(.*?)</script>', h, re.S | re.I)
    inv["style_blocks"] = len(styles)
    inv["script_blocks"] = len(scripts)
    inv["json_blocks"] = [b[0] for b in json_blocks]

    css = "\n\n".join(styles)
    fonts = re.findall(r"@font-face\s*{([^}]*)}", css)
    font_meta = []
    for f in fonts:
        fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", f)
        wt = re.search(r"font-weight:\s*([^;]+)", f)
        st = re.search(r"font-style:\s*([^;]+)", f)
        uri = DATA_URI.search(f)
        entry = {"family": fam.group(1).strip() if fam else None,
                 "weight": wt.group(1).strip() if wt else None,
                 "style": st.group(1).strip() if st else "normal"}
        if uri and full:
            mime = uri.group(1).lower()
            ext = EXT.get(mime, "bin")
            fname = f"{(entry['family'] or 'font').replace(' ', '-')}-{(entry['weight'] or '').replace(' ', '-')}-{entry['style']}.{ext}"
            raw = base64.b64decode(uri.group(2))
            write(os.path.join(out, "fonts", fname), raw, "wb")
            entry["file"] = fname
            entry["bytes"] = len(raw)
        font_meta.append(entry)
    inv["fonts"] = font_meta

    write(os.path.join(out, "styles.css"), strip_data_uris(css, store))
    if scripts:
        write(os.path.join(out, "script.js"), strip_data_uris("\n\n/* ---- */\n\n".join(scripts), store))
    for bid, body in json_blocks:
        write(os.path.join(out, f"{bid}.json"), body)

    sprite = re.search(r'<svg[^>]*id="sprite"[^>]*>(.*?)</svg>\s*(?=<)', h, re.S)
    symbols = re.findall(r'(<symbol\b[^>]*id="([^"]+)"[^>]*>.*?</symbol>)', h, re.S)
    inv["symbols"] = [s[1] for s in symbols]
    if symbols and full:
        defs = "".join(s[0] for s in symbols)
        for raw, sid in symbols:
            vb = re.search(r'viewBox="([^"]+)"', raw)
            inner = re.sub(r"^<symbol[^>]*>|</symbol>$", "", raw.strip(), flags=re.S)
            doc = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                   f'viewBox="{vb.group(1) if vb else "0 0 24 24"}" style="color:#121212">'
                   f'<title>{sid}</title>'
                   + (f"<defs>{defs}</defs>" if "<use" in inner else "")
                   + inner + "</svg>\n")
            write(os.path.join(out, "sprite", f"{sid}.svg"), doc)

    secs = sections(h)
    inv["sections"] = []
    for n, (s, e, sid) in enumerate(secs):
        frag = h[s:e]
        heading = re.search(r"<h[12][^>]*>(.*?)</h[12]>", frag, re.S)
        title = to_text(heading.group(1)).strip() if heading else ""
        base = f"{n:02d}-{sid}"
        if full:
            write(os.path.join(out, "chapters", base + ".html"), strip_data_uris(frag, store))
        write(os.path.join(out, "chapters-text", base + ".txt"), to_text(strip_data_uris(frag, store)))
        inv["sections"].append({"n": n, "id": sid, "title": title, "chars": e - s,
                                "figures": frag.count("<figure"), "tables": frag.count("<table"),
                                "inline_svg": frag.count("<svg"), "uses": frag.count("<use")})
    if not secs:
        body = re.search(r"<body[^>]*>(.*)</body>", h, re.S | re.I)
        write(os.path.join(out, "page-text.txt"), to_text(strip_data_uris(body.group(1) if body else h, store)))

    inv["data_uris"] = {}
    for fname, (mime, payload) in store.items():
        inv["data_uris"][fname] = mime
        if full and not mime.startswith("font"):
            write(os.path.join(out, "images", fname), base64.b64decode(payload), "wb")
    inv["buttons"] = len(re.findall(r"<button\b", h))
    inv["dialogs"] = len(re.findall(r"<dialog\b", h))
    inv["download_names"] = sorted(set(re.findall(r"[A-Za-z0-9_-]+\.(?:svg|png|css|json|zip|pdf|txt)\b", "\n".join(scripts))))
    write(os.path.join(out, "inventory.json"), json.dumps(inv, indent=1))
    return inv


def unzip(name, slug):
    dest = os.path.join(OUT, "references", slug)
    count = 0
    with zipfile.ZipFile(os.path.join(SRC, name)) as z:
        for info in z.infolist():
            if info.is_dir():
                continue
            target = os.path.normpath(os.path.join(dest, info.filename))
            if not target.startswith(os.path.abspath(dest) + os.sep):
                raise SystemExit(f"unsafe path in {name}: {info.filename}")
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(info) as src, open(target, "wb") as dst:
                dst.write(src.read())
            count += 1
    return count


def manifest():
    rows = []
    for dirpath, _, files in os.walk(SRC):
        for f in sorted(files):
            p = os.path.join(dirpath, f)
            with open(p, "rb") as fh:
                data = fh.read()
            rows.append((os.path.relpath(p, SRC), len(data), hashlib.sha256(data).hexdigest()))
    return sorted(rows)


if __name__ == "__main__":
    report = {"manifest": manifest()}
    jobs = [
        ("20261018_Oath-And-Action-Brand-Guide_V5-Polished.html", "v5-polished", True),
        ("20261018_Oath-And-Action-Brand-Guide_V5.html", "v5", False),
        ("20261018_Oath-And-Action-Brand-Guide_V4.2.html", "v4-2", False),
        ("20261018_Oath-And-Action-Atlas-Visual-System.html", "atlas-visual-system", True),
        ("20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html", "concepts-v2", False),
        ("20261019_Oath-And-Action-Atlas-Design-Concepts_V1.html", "concepts-v1", False),
        ("20261015_Who-Do-They-Answer-To-Systems-Atlas_V7.html", "atlas-v7", False),
    ]
    report["html"] = {slug: extract_html(name, slug, full) for name, slug, full in jobs}
    v7 = os.path.join(OUT, "atlas-v7", "atlas-data.json")
    if os.path.exists(v7):
        data = json.loads(read(v7))
        write(os.path.join(OUT, "atlas-v7-data.json"), json.dumps(data, indent=1, ensure_ascii=False))
    report["references"] = {"data-viz": unzip("data_viz.zip", "data-viz"),
                            "design-i-like": unzip("Design_I_like.zip", "design-i-like")}
    write(os.path.join(OUT, "extract-report.json"), json.dumps(report, indent=1))
    print(json.dumps({k: (v if k != "html" else {s: {"sections": len(i["sections"]), "symbols": len(i["symbols"]),
                                                    "fonts": len(i["fonts"]), "scripts": i["script_blocks"],
                                                    "json": i["json_blocks"]} for s, i in v.items()})
                      for k, v in report.items() if k != "manifest"}, indent=1))
