"""The drawing-method pilot (Phase 3, round 0): S01 to S16 placed in a pilot chapter 14 of a real guide build, built once by
each drawing method, measured, and projected to chapter 14's 97 finished specimens against its stop (DR-227; 2,803,941
bytes since DR-238, read from guide_charts.CEILING).

Usage:
    python3 -I work/build/scripts/phase-3/chart_pilot.py --out DIR [--methods lean,load,load-trim]

Writes into DIR (scratch, outside the repository):
  pilot/chapters/14-data-visualization.json   a pilot chapter: one rule, then S01 to S16 as plates
  pilot/specimens/s-14-sNN.html, .chart.json  each plate's fragment (one chart placeholder) and its spec
  20261111_Pilot-<method>.html and its build report, one page per method
  20261111_Pilot-Results.json                 every measurement and the projection
Specs come from work/build/chart-kit/specs/sNN.json (the Explainer maker's); a specimen with no spec there yet takes the
engineer's fixture or test spec named with --fallback DIR, and the results say which.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(Path(__file__).resolve().parent))
import guide_charts  # noqa: E402   the stop and the page budget live there
KIT = ROOT / "work/build/chart-kit"
MB = 1_000_000
IDS = [f"s{n:02d}" for n in range(1, 17)]
# The proposal's other parts of chapter 14 (section 3), held as allocated
OTHER = {"rules, plates, selection guide and palette specification": 0.30 * MB,
         "three complex examples": 0.09 * MB,
         "shared map geometry": 0.25 * MB}
SKETCHES, AVOID = 22, 8
SKETCH_EACH, AVOID_EACH = 4 * 1024, 2 * 1024
FINISHED = 97                  # core and extended specimens
FORMS_TOTAL = 97               # forms with a drawing module (one per core and extended form, at most)
STOP = guide_charts.CEILING[guide_charts.HARD_STOP]     # 2,803,941 bytes (DR-238); 1.75 MB until board 1


def write_pilot(base, fallback):
    pil = base / "pilot"
    if pil.exists():
        shutil.rmtree(pil)
    (pil / "chapters").mkdir(parents=True)
    (pil / "specimens").mkdir(parents=True)
    manifest, extras, used = {}, [], {}
    for sid in IDS:
        src = KIT / "specs" / f"{sid}.json"
        origin = "Explainer maker's spec"
        if not src.exists():
            alt = [Path(d) / f"{sid}.json" for d in fallback] + [KIT / "fixtures/specs" / f"{sid}.json"]
            src = next((p for p in alt if p.exists()), None)
            origin = f"engineer's stand-in ({src.parent.name}/{src.name})" if src else "missing"
        if not src:
            continue
        spec = json.loads(src.read_text())
        # a spec still on its sidecar's Phase 2 wording of the atlas takes the reader wording for the pilot (request X9)
        ds = spec.get("dataset")
        first = (ds[0] if isinstance(ds, list) else ds) if ds else None
        mp = ROOT / "work/build/data" / f"{first}.meta.json" if first else None
        if mp and mp.exists():
            meta = json.loads(mp.read_text())
            if spec.get("source_line") == (meta.get("source_line_variants") or {}).get("phase_2_wording"):
                spec["source_line"] = meta["printed_source_line"]
                origin += ", source line moved to the reader wording"
        pid = f"s-14-{sid}"
        (pil / "specimens" / f"{pid}.chart.json").write_text(json.dumps(spec, ensure_ascii=False))
        (pil / "specimens" / f"{pid}.html").write_text(f'<div data-oa-chart="{pid}"></div>\n')
        manifest[pid] = {"chapter": "14", "rule": None, "width_px": None, "alt": spec.get("alt") or spec["id"], "illustrative": bool(spec.get("illustrative"))}
        extras.append({"after_rule": "14.1", "specimen": pid, "label": f"{spec['id']}, {spec.get('form')}", "caption": spec.get("reader_question", "")})
        used[sid] = {"spec": str(src.relative_to(ROOT)) if ROOT in src.parents else str(src), "origin": origin, "form": spec.get("form"), "tier": spec.get("tier")}
    (pil / "specimens" / "manifest-pilot.json").write_text(json.dumps(manifest, indent=1, ensure_ascii=False))
    ch = {
        "number": "14", "anchor": "data-visualization", "title": "Data visualization", "part": "evidence",
        "instruction": "Start from the reader's question to choose a chart, then title it with the evidence it shows.",
        "intro": ["A pilot of the drawing method, built for measurement only: sixteen finished charts, drawn by the chart kit."],
        "rules": [{"id": "14.1", "title": "Draw every chart with the chart kit from its data file.",
                   "rule": ["A pilot rule that carries the plates below; the real chapter is built from round 1."],
                   "why": {"text": ["One renderer draws the guide, the exports and the boards, so they cannot drift."], "basis": "Pilot"}}],
        "extras": extras, "related_chapters": [], "sources": [],
    }
    (pil / "chapters" / "14-data-visualization.json").write_text(json.dumps(ch, indent=1, ensure_ascii=False))
    return pil, used


def build(base, pil, method):
    out = base / f"20261111_Pilot-{method}.html"
    r = subprocess.run([sys.executable, "-I", str(ROOT / "work/build/scripts/phase-2/guide_build.py"), "--pilot", str(pil),
                        "--chart-method", method, "--out", str(out), "--quiet"], capture_output=True, text=True)
    rep = json.loads(out.with_name(out.stem + "-Build-Report.json").read_text())
    return out, rep, r.returncode


def kit_parts():
    """The kit as the page carries it (comments and indentation stripped): core script, style, map geometry and forms."""
    js = ("import('" + str(KIT / "oa-chart.mjs") + "').then(k => { const p = k.kit_parts(); const K = globalThis.OAChart;"
          " console.log(JSON.stringify({ core: Buffer.byteLength(p.core), css: Buffer.byteLength(p.css), geo: Buffer.byteLength(p.geo),"
          " files: Object.values(p.forms).map(x => Buffer.byteLength(x)), forms: Object.keys(K.forms).length, words: Buffer.byteLength(JSON.stringify(K.words)) })); })")
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd=str(ROOT))
    return json.loads(r.stdout.strip().splitlines()[-1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--methods", default="lean,load,load-trim,load-table")
    ap.add_argument("--fallback", action="append", default=[])
    a = ap.parse_args()
    base = Path(a.out).resolve()
    base.mkdir(parents=True, exist_ok=True)
    pil, used = write_pilot(base, a.fallback)
    kp = kit_parts()
    form_avg = sum(kp["files"]) / kp["forms"]          # bytes per registered form (19 forms in 17 files today)
    core = kp["core"] + kp["css"] + kp["words"] + 400  # the script and style elements' own tags
    results = {"specs": used, "methods": {}, "kit": dict(kp, form_avg_bytes=round(form_avg), core_with_css=core,
               note="Map geometry (geo.js) is counted under the proposal's shared map geometry, not the renderer")}
    for m in a.methods.split(","):
        page, rep, code = build(base, pil, m)
        w = rep["weight"]
        ch14 = w["chapters"].get("14", {}).get("bytes", 0)
        kit = w["parts"].get("chart kit", 0)
        charts = w.get("charts") or {}
        # chapter 14's plates only: chapter 13's own charts (the editor's plates) weigh in chapter 13
        per = {k: v["bytes"] for k, v in sorted(charts.items()) if k.startswith("s-14-")}
        n = len(per)
        avg = sum(per.values()) / n if n else 0
        frame = (ch14 - sum(per.values())) / max(1, n)       # the plate frame, caption and chapter text per specimen
        # projection: 97 finished specimens at this method's measured average (figure plus its plate frame), the sketches and
        # avoid entries, the other parts as allocated, and the renderer grown to every form (kit core + forms x form average + geometry)
        renderer_now = kit
        renderer_full = (core + FORMS_TOTAL * form_avg) if m != "lean" else kp["css"]
        spec_part = FINISHED * (avg + frame)
        sketches = SKETCHES * SKETCH_EACH + AVOID * AVOID_EACH
        proj = spec_part + sketches + sum(OTHER.values()) + renderer_full
        results["methods"][m] = {
            "page": str(page), "build_exit": code, "page_bytes": rep["bytes"], "chapter_14_bytes": ch14, "chart_kit_bytes": kit,
            "chapter_14_with_kit": ch14 + kit, "specimens": n, "specimen_bytes": per, "specimen_avg": round(avg), "frame_avg": round(frame),
            "warnings": [x for x in rep["warnings"]][:60], "warning_count": len(rep["warnings"]),
            "projection": {"specimens": round(spec_part), "sketches_and_avoid": sketches, "other_parts": round(sum(OTHER.values())),
                           "renderer": round(renderer_full), "renderer_now": renderer_now, "chapter_14": round(proj), "stop": STOP,
                           "under_stop": proj <= STOP, "margin": round(STOP - proj)},
        }
        print(f"{m:10s} ch14 {ch14:>9,} + kit {kit:>7,} = {ch14 + kit:>9,} | {n} specimens avg {avg:>8,.0f} + frame {frame:>6,.0f} | "
              f"projected chapter 14: {proj / MB:.3f} MB ({'under' if proj <= STOP else 'OVER'} its {STOP:,.0f} byte stop) | warnings {len(rep['warnings'])}")
    (base / "20261111_Pilot-Results.json").write_text(json.dumps(results, indent=1))
    print(f"results: {base / '20261111_Pilot-Results.json'}")


if __name__ == "__main__":
    main()
