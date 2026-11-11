"""Build the identity designer's content: chapters 03, 04 and 08 (The lockmark) and the identity proofs appendix.

Writes
  work/build/guide/specimens/<id>.html            one self-contained fragment per specimen
  work/build/guide/specimens/manifest-identity.json
  work/build/guide/chapters/03-identity.json, 04-ampersand.json, 08-lockmark.json, proofs.json
  work/boards/phase-2/stage-a/proofs/20261107_Letterhead-Proof.html and .pdf (with --pdf)
  <scratch>/preview-identity.html                 a local preview of every specimen with tokens.css (with --preview DIR)

Run from anywhere: python3 work/build/scripts/phase-2/stage_a_identity_build.py [--pdf] [--preview DIR]
It reads the identity masters and Civic Line files and writes none of them. stage_a_identity_s1.py writes S1's masters
and the minimum sizes table; run it first when either needs writing.
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
import stage_b_identity_ch09 as S09  # noqa: E402  (stage B round 2: chapter 09, Pillar icons)
import stage_b_identity_ch12 as S12  # noqa: E402  (stage B round 2: chapter 12's Rules 12.1 to 12.4, in a shared file)
import stage_c_identity_ch17 as S17  # noqa: E402  (stage C round 1: Rule 17.6's hinge and lever, read by chapter 17's maker)


MINE = ("s-03-", "s-04-", "s-08-", "s-09-", "s-proofs-", "s-17-hinge-", "s-17-lever-") + S12.PREFIXES      # specimen ids this maker owns; in chapter 12
# only its own devices, since the systems designer writes s-12-marker-*, s-12-key-* and the rest (D2-829)
RETIRED_CHAPTER_FILES = ("08-signal-grid.json",)     # this maker's chapter files that no longer exist under that name


def CHAPTERS():
    """Chapters 03, 04 and 08, then chapter 09 from stage B round 2, its prose set by the same quote rules."""
    return CH.CHAPTERS + [CH._smarten(S09.chapter())]


def build(preview_dir=None, pdf=False):
    L.SPEC_DIR.mkdir(parents=True, exist_ok=True)
    L.CHAP_DIR.mkdir(parents=True, exist_ok=True)
    SP.write_letterhead(pdf=pdf)          # first, so the letterhead specimen can carry the PDF
    records = []
    for mod in (S03, S04, S08, S09, S12, SP, S17):     # S17 last: its inlined masters advance the id counter
        for fn in mod.S:
            records.append(fn())
    ids = [r["id"] for r in records]
    assert len(ids) == len(set(ids)), "duplicate specimen id"
    manifest = {}
    for r in records:
        (L.SPEC_DIR / f'{r["id"]}.html').write_text(r["html"])
        m = {"chapter": r["chapter"], "rule": r["rule"]}
        if r["width_px"]:
            m["width_px"] = r["width_px"]      # left out for a sheet or table the shell should flow (C-S6)
        m.update({"alt": r["alt"], "illustrative": r["illustrative"], "notes": r["notes"]})
        m.update(r.get("meta") or {})          # readable, interactive, scale, fit_switch, check_exempt
        manifest[r["id"]] = m
    # specimens this maker wrote before and no longer writes (the proof pairs replaced twelve single plates)
    for f in L.SPEC_DIR.glob("s-*.html"):
        if f.stem.startswith(MINE) and f.stem not in manifest:
            f.unlink()
            print(f"  removed stale {f.name}")
    (L.SPEC_DIR / "manifest-identity.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False) + "\n")
    for old in RETIRED_CHAPTER_FILES:             # chapter 08 moved to 08-lockmark.json (D2-325)
        if (L.CHAP_DIR / old).exists():
            (L.CHAP_DIR / old).unlink()
            print(f"  removed {old}")
    for ch in CHAPTERS():
        f = L.CHAP_DIR / f'{ch["number"]}-{ch["anchor"]}.json'
        f.write_text(json.dumps(ch, indent=1, ensure_ascii=False) + "\n")
        used = CH.specimens_used(ch)
        missing = [u for u in used if u not in manifest]
        assert not missing, f"{f.name} names specimens that do not exist: {missing}"
    S12.write_chapter()                          # merges Rules 12.1 to 12.4 into the shared file (D2-830)
    missing = [u for u in S12.specimens_used() if u not in manifest]
    assert not missing, f"12-graphic-devices.json names specimens that do not exist: {missing}"
    SP.write_proofs_json()
    if preview_dir:
        write_preview(Path(preview_dir), records)
    print(f"{len(records)} specimens, {len(CHAPTERS())} chapters")
    for ch in CHAPTERS():
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
