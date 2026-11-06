"""Build the identity designer's stage board A content: chapters 03, 04 and 08 and the Gate 2 proofs panel.

Writes
  work/build/guide/specimens/<id>.html            one self-contained fragment per specimen
  work/build/guide/specimens/manifest-identity.json
  work/build/guide/chapters/03-identity.json, 04-ampersand.json, 08-signal-grid.json
  work/boards/phase-2/stage-a/proofs/20261106_Letterhead-Proof.html and .pdf (with --pdf)
  <scratch>/preview-identity.html                 a local preview of every specimen with tokens.css (with --preview DIR)

Run from anywhere: python3 work/build/scripts/phase-2/stage_a_identity_build.py [--pdf] [--preview DIR]
It reads the identity masters and Civic Line files and writes none of them.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stage_a_identity_lib as L  # noqa: E402
import stage_a_identity_s03 as S03  # noqa: E402
import stage_a_identity_s04 as S04  # noqa: E402
import stage_a_identity_s08 as S08  # noqa: E402
import stage_a_identity_proofs as SP  # noqa: E402
import stage_a_identity_chapters as CH  # noqa: E402


# manifest fields the shell reads beyond the brief's (Guide Shell Notes section 5)
EXTRA = {
    "s-03-1-failure": {"check_exempt": ["contrast"]},  # the typed name's red ampersand, 2.96:1, is the failure shown
    "s-03-7-failure": {"check_exempt": ["contrast"]},
    "s-04-3-failure": {"check_exempt": ["red"]},      # the failure is two working reds in one view
    "s-04-4-failure": {"check_exempt": ["red"]},
    "s-08-composer": {"interactive": True},
}


def build(preview_dir=None, pdf=False):
    L.SPEC_DIR.mkdir(parents=True, exist_ok=True)
    L.CHAP_DIR.mkdir(parents=True, exist_ok=True)
    SP.write_letterhead(pdf=pdf)          # first, so the letterhead specimen can carry the PDF
    records = []
    for mod in (S03, S04, S08, SP):
        for fn in mod.S:
            r = fn()
            records.append(r)
    ids = [r["id"] for r in records]
    assert len(ids) == len(set(ids)), "duplicate specimen id"
    manifest = {}
    for r in records:
        (L.SPEC_DIR / f'{r["id"]}.html').write_text(r["html"])
        m = {k: r[k] for k in ("chapter", "rule", "width_px", "alt", "illustrative", "notes")}
        m.update({k: v for k, v in EXTRA.get(r["id"], {}).items()})
        if r.get("interactive"):
            m["interactive"] = True
        manifest[r["id"]] = m
    (L.SPEC_DIR / "manifest-identity.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    for ch in CH.CHAPTERS:
        f = L.CHAP_DIR / f'{ch["number"]}-{ch["anchor"]}.json'
        f.write_text(json.dumps(ch, indent=1, ensure_ascii=False) + "\n")
        used = CH.specimens_used(ch)
        missing = [u for u in used if u not in manifest]
        assert not missing, f"{f.name} names specimens that do not exist: {missing}"
    SP.write_proofs_json()
    if preview_dir:
        write_preview(Path(preview_dir), records)
    print(f"{len(records)} specimens, {len(CH.CHAPTERS)} chapters")
    for ch in CH.CHAPTERS:
        print(f'  {ch["number"]} {ch["title"]}: {len(ch["rules"])} rules, {len(ch.get("extras", []))} extras')
    return records


def write_preview(d, records):
    """A plain page that shows every specimen with its rule and caption, for the maker's own looking."""
    d.mkdir(parents=True, exist_ok=True)
    tokens = (L.ROOT / "work/build/tokens/tokens.css").resolve()
    caps = {}
    for ch in CH.CHAPTERS:
        for r in ch["rules"]:
            for k in ("correct", "failure", "corrective"):
                if r.get(k):
                    caps[r[k]["specimen"]] = f'Rule {r["id"]} {r["title"]} / {k}: {r[k]["caption"]}'
        for x in ch.get("extras", []):
            caps[x["specimen"]] = f'After {x["after_rule"]}: {x["caption"]}'
    parts = []
    for r in records:
        parts.append(f'<section style="margin:0 0 56px"><p style="font:600 13px/1.4 Inter;color:#4E535B;margin:0 0 8px">{L.E(r["id"])} · {L.E(caps.get(r["id"], r["notes"]))}</p>'
                     f'<figure style="margin:0">{r["html"]}</figure></section>')
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Identity specimens preview</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&family=Lora:ital,wght@1,400&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="file://{tokens}">'
            '<style>body{margin:0;padding:32px 16px;background:var(--oa-color-surface-newsprint);font-family:Inter}main{max-width:1000px;margin:0 auto}</style>'
            f'</head><body><main>{"".join(parts)}</main></body></html>')
    (d / "preview-identity.html").write_text(page)


if __name__ == "__main__":
    pv = None
    if "--preview" in sys.argv:
        pv = sys.argv[sys.argv.index("--preview") + 1]
    build(pv, pdf="--pdf" in sys.argv)
