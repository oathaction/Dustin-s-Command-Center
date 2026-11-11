"""Token parity evidence for the Gate 2 board (task 6 of the Gate 2 brief, November 11, 2026, guide engineer).

Run from the project folder, after run_token_tests.py:
    python3 -I work/build/tests/tokens/token_parity_evidence.py [PAGE] [--out PATH]

PAGE defaults to the Gate 2 preview, work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html; --out to
work/boards/phase-2/gate-2/evidence/20261111_Token-Parity-Results.json.

It writes one JSON file the board builder reads:
  parity      test_token_parity.py run now, its words and exit code: tokens.json and tokens.css say the same thing,
              both ways, surface classes, themes and reduced motion included
  suite       the step results of the last full run of run_token_tests.py (20261106_Token-Test-Results.json):
              the build check, parity, rules, self-test, Style Dictionary's cross-check and the rendered test
  page        the guide page against the token files: the stylesheet the page inlines (<style id="oa-tokens">) is
              tokens.css byte for byte; the page's tokens.css download and its zip hold tokens.css; its tokens.json
              download and zip hold tokens.json; and the version the page prints is the files' version
"""
import argparse
import base64
import hashlib
import html
import io
import json
import pathlib
import re
import subprocess
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[4]
HERE = pathlib.Path(__file__).resolve().parent
CSS = ROOT / "work/build/tokens/tokens.css"
JSN = ROOT / "work/build/tokens/tokens.json"
SUITE = HERE / "20261106_Token-Test-Results.json"
PAGE = ROOT / "work/boards/phase-2/gate-2/20261111_Gate-2-Preview.html"
OUT = ROOT / "work/boards/phase-2/gate-2/evidence/20261111_Token-Parity-Results.json"

sha = lambda b: hashlib.sha256(b).hexdigest()


def data_uri(href):
    head, _, body = href.partition(",")
    return base64.b64decode(body) if ";base64" in head else html.unescape(body).encode()


def link(page, lid):
    m = re.search(r'<a\b[^>]*\bid="' + lid + r'"[^>]*>', page)
    if not m:
        return None
    tag = m.group(0)
    attr = lambda k: (re.search(k + r'="([^"]*)"', tag) or [None, None])[1]
    return {"href": attr("href"), "zip": attr("data-oa-zip"), "name": attr("download"), "zip_name": attr("data-oa-zip-name")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page", nargs="?", default=str(PAGE))
    ap.add_argument("--out", default=str(OUT))
    a = ap.parse_args()
    page_path = pathlib.Path(a.page).resolve()
    run = subprocess.run([sys.executable, "-I", str(HERE / "test_token_parity.py")], capture_output=True, text=True, cwd=ROOT)
    css_b, json_b = CSS.read_bytes(), JSN.read_bytes()
    version = json.loads(json_b).get("$extensions", {}).get("oa", {}).get("version") or json.loads(json_b).get("version")
    vm = re.search(r"\b(\d+\.\d+\.\d+(?:-[\w.]+)?)\b", css_b.decode()[:2000])
    version = version or (vm.group(1) if vm else None)
    page = page_path.read_text()
    checks = []
    inl = re.search(r'<style id="oa-tokens">\n?(.*?)\n?</style>', page, re.S)
    inl_b = inl.group(1).encode() if inl else b""
    # the build's one-line note above the file says where it came from; the rest is the file
    inl_b = re.sub(rb"\A/\* work/build/tokens/tokens\.css, inlined by guide_build\.py \*/\n", b"", inl_b)
    checks.append({"check": "the page inlines tokens.css byte for byte, under the build's one-line note of where it came from", "pass": inl_b.strip() == css_b.strip(),
                   "detail": f"inlined {len(inl_b):,} bytes and tokens.css {len(css_b):,} bytes, both SHA-256 {sha(css_b.strip())[:16]} with the final newline trimmed" if inl_b.strip() == css_b.strip() else f"inlined {len(inl_b):,} bytes, SHA-256 {sha(inl_b.strip())[:16]}; tokens.css {len(css_b):,} bytes, {sha(css_b.strip())[:16]}"})
    for lid, want, name in (("tokens-download", css_b, "tokens.css"), ("tokens-json-download", json_b, "tokens.json")):
        ln = link(page, lid)
        if not ln:
            checks.append({"check": f"the page carries the {name} download", "pass": False, "detail": f"no <a id=\"{lid}\">"})
            continue
        got = data_uri(ln["href"])
        checks.append({"check": f"the {name} download is {name}", "pass": got == want, "detail": f"{ln['name']}: {len(got):,} bytes, SHA-256 {sha(got)[:16]}"})
        if ln["zip"]:
            z = zipfile.ZipFile(io.BytesIO(base64.b64decode(ln["zip"])))
            names = z.namelist()
            inner = z.read(names[0]) if len(names) == 1 else b""
            checks.append({"check": f"the {name} zip holds {name} alone", "pass": len(names) == 1 and inner == want,
                           "detail": f"{ln['zip_name']}: {names}, {len(inner):,} bytes"})
    if version:
        checks.append({"check": "the page prints the token files' version", "pass": version in page, "detail": version})
    suite = json.loads(SUITE.read_text()) if SUITE.exists() else {}
    out = {
        "about": "Token parity for the Gate 2 board: the token files against each other, and the guide page against the token files. "
                 "Written by work/build/tests/tokens/token_parity_evidence.py.",
        "page": str(page_path.relative_to(ROOT)) if ROOT in page_path.parents else str(page_path),
        "page_sha256": sha(page_path.read_bytes()),
        "token_files": {"tokens.css": {"bytes": len(css_b), "sha256": sha(css_b)}, "tokens.json": {"bytes": len(json_b), "sha256": sha(json_b)}, "version": version},
        "parity": {"command": "python3 -I work/build/tests/tokens/test_token_parity.py", "exit": run.returncode, "pass": run.returncode == 0,
                   "output": (run.stdout + run.stderr).strip().splitlines()},
        "suite": {"file": str(SUITE.relative_to(ROOT)), "run": suite.get("run"), "status": suite.get("status"), "passed": suite.get("passed"),
                  "version": suite.get("tokenSetVersion"), "steps": suite.get("steps"), "counts": suite.get("counts")},
        "page_checks": checks,
    }
    out["pass"] = bool(out["parity"]["pass"] and all(c["pass"] for c in checks))
    p = pathlib.Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    for c in checks:
        print(f"  {'pass' if c['pass'] else 'FAIL'}  {c['check']}: {c['detail']}")
    print(f"{'PASS' if out['pass'] else 'FAIL'} token parity evidence: parity test exit {run.returncode}; {sum(c['pass'] for c in checks)} of {len(checks)} page checks; "
          f"written to {p.relative_to(ROOT) if ROOT in p.parents else p}")
    return 0 if out["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
