"""Phase 1 research lead: inventory source/pics_i_like.pdf without modifying it.

Reads the PDF metadata and per-page image list with pypdf, hashes the rendered
page PNGs in work/extract/references/pics-i-like/, and groups identical pages.
Writes JSON to work/handoffs/phase-1/20261021_Pics-I-Like-Inventory.json.
Run: python3 -I work/build/scripts/phase-1/pics_pdf_inventory.py <ROOT>
"""
import hashlib, json, os, sys
from pypdf import PdfReader

root = sys.argv[1]
pdf_path = os.path.join(root, "source", "pics_i_like.pdf")
png_dir = os.path.join(root, "work", "extract", "references", "pics-i-like")
out = os.path.join(root, "work", "handoffs", "phase-1", "20261021_Pics-I-Like-Inventory.json")

r = PdfReader(pdf_path)
meta = {k: str(v) for k, v in (r.metadata or {}).items()}
pages = []
for i, p in enumerate(r.pages, 1):
    imgs = []
    try:
        res = p.get("/Resources") or {}
        xo = res.get("/XObject") or {}
        for name in xo:
            o = xo[name].get_object()
            if o.get("/Subtype") == "/Image":
                data = o.get_data() if False else b""
                imgs.append({"name": str(name), "w": int(o.get("/Width", 0)), "h": int(o.get("/Height", 0)),
                             "filter": str(o.get("/Filter")), "bpc": int(o.get("/BitsPerComponent", 0) or 0)})
    except Exception as e:
        imgs.append({"error": repr(e)})
    text = ""
    try:
        text = (p.extract_text() or "").strip()[:200]
    except Exception:
        pass
    png = os.path.join(png_dir, f"page-{i:02d}.png")
    h = hashlib.sha256(open(png, "rb").read()).hexdigest() if os.path.exists(png) else None
    mb = [float(x) for x in p.mediabox]
    pages.append({"page": i, "mediabox": mb, "images": imgs, "text": text, "png_sha256": h})

groups = {}
for pg in pages:
    groups.setdefault(pg["png_sha256"], []).append(pg["page"])
dups = [v for v in groups.values() if len(v) > 1]
res = {"file": "source/pics_i_like.pdf", "size_bytes": os.path.getsize(pdf_path),
       "sha256": hashlib.sha256(open(pdf_path, "rb").read()).hexdigest(),
       "page_count": len(r.pages), "metadata": meta, "duplicate_page_groups": dups,
       "unique_pages": len(groups), "pages": pages}
json.dump(res, open(out, "w"), indent=1)
print(json.dumps({k: res[k] for k in ("size_bytes", "sha256", "page_count", "metadata", "duplicate_page_groups", "unique_pages")}, indent=1))
for pg in pages:
    print(pg["page"], [ (x.get("w"), x.get("h")) for x in pg["images"]], repr(pg["text"][:60]))
