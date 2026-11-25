"""C1 (DR-331, Phase 4 board 1 item 3): four build steps that take bytes off the guide page and change nothing a reader sees.

guide_build.py runs them on the assembled page after the Phase 3 weight pass and before the weight gates measure it, and records
each step in the build report under weight.c1. `guide_build.py --no-c1` builds the same tree without them, so one tree builds
both ways and the proof (run.sh --proof, in this folder) compares the two pages.

  3a  plate styles drawn once. A plate's <style> is wrapped as `@scope ([data-specimen="ID"]){...}`; where the same body repeats,
      the first block carries a scope list of every specimen that uses it and the later ones go. A block stays where it is when
      moving it would change the order of the scoped rules that reach its specimen (the cascade check, below).
  3b  the page's PNGs re-encoded without loss, from the committed cache work/build/cache/png/, keyed by the SHA-256 of the PNG
      as the page carries it; the build needs no tool, and it uses an entry only when the entry decodes to the same pixels.
      `c1.py --fill-cache PAGE --lib DIR` fills the cache with oxipng (zopfli), from Python bindings installed in DIR.
  3c  chapter 20's repeated drawings in its frames (the charts S10 and S86 on the home and article pages, the Act page's chart,
      and the favicon in the tab frames) drawn once and placed again by <use>; the tracker marks stay inline.
  3d  `&quot;`, `&gt;` and `&#x27;` (or `&#39;`) written as the characters themselves wherever the parser reads the same thing
      (text, and quoted attribute values that are not quoted by that character), outside script, style, comments and raw text.

The cascade check (3a). Two scoped rules of equal specificity that reach the same element are ordered by scope proximity, then
by order of appearance; a rule with no scope loses to a scoped one at any position. So for each specimen the check lists the
scoped blocks whose root is the specimen itself (its own blocks, any merged block that names it, and a chapter's
`@scope (#chapter [data-specimen])` block in the same section), in page order, before and after; where the two lists differ,
that specimen keeps its own blocks in place.

  python3 work/build/scripts/phase-4/weight/c1.py PAGE.html [--steps 3a,3b,3c,3d] [--out SMALLER.html]   measure on a page
  python3 work/build/scripts/phase-4/weight/c1.py --fill-cache PAGE.html --lib DIR                        fill 3b's cache
  python3 work/build/scripts/phase-4/weight/c1.py --self-test
"""
import base64
import datetime
import hashlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CACHE = ROOT / "work/build/cache/png"
STEPS = ("3a", "3b", "3c", "3d")
CHAPTER_20 = "web"   # chapter 20's anchor (guide_build.CHAPTERS)


# --------------------------------------------------------------------------------------------------------------------
# A tokenizer for the page as the build writes it: text, comments, declarations, CDATA, start and end tags, and the raw
# contents of the elements the parser reads without markup (script, style and the rest). Start tags carry their
# attributes' value spans and quotes.
# --------------------------------------------------------------------------------------------------------------------
RAW = ("script", "style", "xmp", "iframe", "noembed", "noframes", "noscript", "textarea", "title", "plaintext")
TAG_NAME = re.compile(r"[A-Za-z][^\s/>]*")
ATTR_NAME = re.compile(r"[^\s/>=][^\s/>=]*")
WS = re.compile(r"[\s/]*")


def tokens(page):
    """Yield (kind, start, end, extra). kind: text, comment, cdata, decl, end, start, raw. A start token's extra is
    (name, [(name, value_start, value_end, quote)]); a raw token's extra is the element's name."""
    i, n = 0, len(page)
    low = None
    while i < n:
        j = page.find("<", i)
        if j < 0:
            yield ("text", i, n, None)
            return
        if j > i:
            yield ("text", i, j, None)
        if page.startswith("<!--", j):
            k = page.find("-->", j + 4)
            k = n if k < 0 else k + 3
            yield ("comment", j, k, None)
            i = k
            continue
        if page.startswith("<![CDATA[", j):
            k = page.find("]]>", j + 9)
            k = n if k < 0 else k + 3
            yield ("cdata", j, k, None)
            i = k
            continue
        if page.startswith("<!", j) or page.startswith("<?", j):
            k = page.find(">", j)
            k = n if k < 0 else k + 1
            yield ("decl", j, k, None)
            i = k
            continue
        if page.startswith("</", j) and j + 2 < n and page[j + 2].isalpha():
            k = page.find(">", j)
            k = n if k < 0 else k + 1
            yield ("end", j, k, None)
            i = k
            continue
        m = TAG_NAME.match(page, j + 1)
        if not m:
            yield ("text", j, j + 1, None)
            i = j + 1
            continue
        name = m.group(0).lower()
        k, attrs = m.end(), []
        while k < n:
            k = WS.match(page, k).end()
            if k >= n or page[k] == ">":
                break
            a = ATTR_NAME.match(page, k)
            if not a:
                k += 1
                continue
            aname, k = a.group(0).lower(), a.end()
            k2 = re.compile(r"\s*").match(page, k).end()
            if k2 < n and page[k2] == "=":
                k = re.compile(r"\s*").match(page, k2 + 1).end()
                q = page[k] if k < n else ""
                if q in "\"'":
                    e = page.find(q, k + 1)
                    attrs.append((aname, k + 1, e, q))
                    k = e + 1
                else:
                    e = re.compile(r"[^\s>]*").match(page, k).end()
                    attrs.append((aname, k, e, ""))
                    k = e
            else:
                attrs.append((aname, k, k, None))
        k = min(n, k + 1)
        yield ("start", j, k, (name, attrs))
        i = k
        if name in RAW:
            if low is None:
                low = page.lower()
            e = low.find("</" + name, k)
            while e >= 0 and e + 2 + len(name) < n and page[e + 2 + len(name)] not in " \t\n\f\r/>":
                e = low.find("</" + name, e + 1)
            e = n if e < 0 else e
            if e > k:
                yield ("raw", k, e, name)
            i = e


# --------------------------------------------------------------------------------------------------------------------
# 3a: plate styles drawn once
# --------------------------------------------------------------------------------------------------------------------
ONE_SCOPE = re.compile(r'@scope \(\[data-specimen="([^"]+)"\]\)\{(.*)\}\Z', re.S)
SECTION_SCOPE = re.compile(r"@scope \(#([A-Za-z][\w-]*) \[data-specimen\]\)")
GLOBAL_AT = re.compile(r"@(keyframes|font-face|property|counter-style|layer|import|namespace|page|font-feature-values|font-palette-values)\b")
SECTION = re.compile(r'<section class="(?:chapter|part|contents|appendix|cover|start)[^"]*" id="([^"]+)"')


def style_blocks(page):
    """Every <style> element outside scripts: (tag start, end after </style>, its attribute text, its body)."""
    out, it = [], tokens(page)
    pending = None
    for kind, s, e, x in it:
        if kind == "start" and x[0] == "style":
            pending = (s, e)
        elif pending and kind == "raw" and x == "style":
            close = page.find(">", e) + 1
            out.append((pending[0], close, page[pending[0] + 6:pending[1] - 1], page[s:e]))
            pending = None
        elif pending and kind == "end":
            out.append((pending[0], e, page[pending[0] + 6:pending[1] - 1], ""))
            pending = None
    return out


def sections(page):
    marks = [(m.start(), m.group(1)) for m in SECTION.finditer(page)]
    return marks


def section_at(marks, pos):
    lo, hi, best = 0, len(marks) - 1, None
    while lo <= hi:
        mid = (lo + hi) // 2
        if marks[mid][0] <= pos:
            best, lo = marks[mid][1], mid + 1
        else:
            hi = mid - 1
    return best


def step_3a(page):
    blocks = style_blocks(page)
    marks = sections(page)
    plate = []        # (index, start, end, sid, body)
    shared = []       # a chapter's @scope (#chapter [data-specimen]) block: (index, start, section)
    for k, (s, e, attrs, body) in enumerate(blocks):
        m = ONE_SCOPE.match(body)
        if m and not attrs.strip():
            plate.append((k, s, e, m.group(1), m.group(2)))
        elif SECTION_SCOPE.match(body):
            shared.append((k, s, section_at(marks, s)))
    home = {}
    for k, s, e, sid, body in plate:
        home.setdefault(sid, section_at(marks, s))
    groups = {}
    for b in plate:
        groups.setdefault(b[4], []).append(b)

    def reach(plan):
        """For each specimen: the bodies of the scoped blocks rooted at it, in page order, under a plan that maps a block's
        index to the scope list it carries (an empty list: the block goes)."""
        seq = {}
        rows = [(s, sids, body) for k, s, e, sid, body in plate for sids in [plan.get(k, [sid])] if sids]
        rows += [(s, ("@section", sec), None) for k, s, sec in shared]
        rows.sort(key=lambda r: r[0])
        by_sec = {}
        for sid, sec in home.items():
            by_sec.setdefault(sec, []).append(sid)
        for s, sids, body in rows:
            if isinstance(sids, tuple):
                for sid in by_sec.get(sids[1], []):
                    seq.setdefault(sid, []).append(("@section", s))
            else:
                for sid in sids:
                    seq.setdefault(sid, []).append(body)
        return seq

    before = reach({})
    plan, kept_whole, skipped_global = {}, set(), 0
    for body, bl in groups.items():
        if len(bl) < 2:
            continue
        if GLOBAL_AT.search(body):
            skipped_global += 1
            continue
        first = bl[0]
        sids = []
        for b in bl:
            if b[3] not in sids:
                sids.append(b[3])
        plan[first[0]] = sids
        for b in bl[1:]:
            plan[b[0]] = []
    after = reach(plan)
    bad = sorted(sid for sid in before if before[sid] != after.get(sid))
    if bad:
        # each specimen whose scoped rules would come in another order keeps its own blocks where they are
        for sid in bad:
            kept_whole.add(sid)
        for body, bl in groups.items():
            if len(bl) < 2 or bl[0][0] not in plan:
                continue
            first = bl[0]
            for b in bl[1:]:
                if b[3] in kept_whole:
                    plan[b[0]] = [b[3]]
            listed = [first[3]] + [b[3] for b in bl[1:] if not plan[b[0]] and b[3] != first[3]]
            plan[first[0]] = list(dict.fromkeys(listed))
        after = reach(plan)
        still = sorted(sid for sid in before if before[sid] != after.get(sid))
        if still:
            raise AssertionError(f"C1 3a: the cascade check still fails for {len(still)} specimen(s), first {still[0]}")
    # write the page
    out, last = [], 0
    dropped, merged_firsts, touched = 0, 0, set()
    for k, s, e, sid, body in plate:
        if k not in plan:
            continue
        sids = plan[k]
        out.append(page[last:s])
        if not sids:
            dropped += 1
            touched.add(sid)
        elif sids == [sid]:
            out.append(page[s:e])
        else:
            merged_firsts += 1
            touched.update(sids)
            out.append("<style>@scope (" + ",".join(f'[data-specimen="{x}"]' for x in sids) + "){" + body + "}</style>")
        last = e
    out.append(page[last:])
    new = "".join(out)
    rec = {"blocks": len(plate), "repeated_bodies": sum(1 for bl in groups.values() if len(bl) > 1),
           "blocks_dropped": dropped, "blocks_carrying_a_list": merged_firsts, "specimens_touched": len(touched),
           "specimens_kept_whole_by_the_cascade_check": sorted(kept_whole), "groups_left_for_a_global_rule": skipped_global,
           "touched": sorted(touched)}
    return new, rec


# --------------------------------------------------------------------------------------------------------------------
# 3b: the page's PNGs from the lossless cache
# --------------------------------------------------------------------------------------------------------------------
SHOWN_PNG = re.compile(r'(<(?:img|image)\b[^>]*?\s(?:src|href|xlink:href)=")data:image/png;base64,([A-Za-z0-9+/=]+)(")')


def rgba(b):
    from PIL import Image
    im = Image.open(io.BytesIO(b))
    im.load()
    return im.size, im.convert("RGBA").tobytes(), im.mode


def same_pixels(a, b):
    """Decoded to RGBA, the same size and the same value at every pixel. A 16-bit image must stay 16-bit, since RGBA reads
    only its top 8 bits."""
    sa, pa, ma = rgba(a)
    sb, pb, mb = rgba(b)
    if sa != sb or pa != pb:
        return False
    deep = lambda m: m.startswith("I") or m in ("RGB;16", "RGBA;16")
    if deep(ma) or deep(mb):
        from PIL import Image
        ia, ib = Image.open(io.BytesIO(a)), Image.open(io.BytesIO(b))
        return ia.mode == ib.mode and ia.tobytes() == ib.tobytes()
    return True


def step_3b(page, cache=CACHE):
    found, used, missing, refused, saved = {}, 0, [], [], 0

    def one(m):
        nonlocal used, saved
        b64 = m.group(2)
        if b64 not in found:
            raw = base64.b64decode(b64)
            sha = hashlib.sha256(raw).hexdigest()
            f = Path(cache) / f"{sha}.png"
            new = b64
            if f.is_file():
                small = f.read_bytes()
                if len(small) < len(raw) and same_pixels(raw, small):
                    new = base64.b64encode(small).decode()
                else:
                    refused.append(sha)
            else:
                missing.append(sha)
            found[b64] = new
        new = found[b64]
        if new != b64:
            used += 1
            saved += len(b64) - len(new)
        return m.group(1) + "data:image/png;base64," + new + m.group(3)

    page = SHOWN_PNG.sub(one, page)
    return page, {"shown_pngs": len(found), "images_replaced": used, "bytes_saved": saved,
                  "not_in_cache": missing, "refused": refused}


def fill_cache(page, lib, cache=CACHE):
    """Re-encode every PNG the page shows with oxipng (zopfli) and keep each smaller file with the same pixels, named by the
    SHA-256 of the PNG as the page carries it, with a manifest beside it."""
    sys.path.insert(0, str(Path(lib).resolve()))
    import oxipng
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    man_path = cache / "manifest.json"
    man = json.loads(man_path.read_text()) if man_path.exists() else {}
    seen = {}
    for m in SHOWN_PNG.finditer(page):
        raw = base64.b64decode(m.group(2))
        sha = hashlib.sha256(raw).hexdigest()
        if sha in seen:
            continue
        small = oxipng.optimize_from_memory(raw, level=6, strip=oxipng.StripChunks.none(), deflate=oxipng.Deflaters.zopfli(15))
        ok = len(small) < len(raw) and same_pixels(raw, small)
        seen[sha] = ok
        if ok:
            (cache / f"{sha}.png").write_bytes(small)
            man[sha] = {"bytes_before": len(raw), "bytes_after": len(small), "tool": "oxipng 9.1.1 (pyoxipng), level 6, zopfli 15 iterations, no chunk stripped",
                        "same_pixels": True, "made": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
    man_path.write_text(json.dumps(man, indent=1, sort_keys=True) + "\n")
    return seen


# --------------------------------------------------------------------------------------------------------------------
# 3c: chapter 20's repeated drawings by <use>
# --------------------------------------------------------------------------------------------------------------------
ID_ATTR = re.compile(r'\sid="([^"]+)"')


def svg_spans(text):
    st, out = [], []
    for m in re.finditer(r"<svg\b|</svg>", text):
        if m.group(0) == "<svg":
            st.append(m.start())
        elif st:
            out.append((st.pop(), m.end()))
    return sorted(out)


def step_3c(page, anchor=CHAPTER_20):
    m = re.search(r'<section class="chapter[^"]*" id="' + re.escape(anchor) + '"', page)
    if not m:
        return page, {"groups": 0, "copies_by_use": 0, "bytes_saved": 0, "note": f"no section #{anchor}"}
    a = m.start()
    nx = SECTION.search(page, m.end())
    b = nx.start() if nx else len(page)
    sec = page[a:b]
    cands = []
    for s, e in svg_spans(sec):
        t = sec[s:e]
        gt = t.find(">") + 1
        tag = t[:gt]
        fr = sec.rfind('data-oa-page-frame="', 0, s)
        if fr < 0:
            continue
        frame = sec[fr + 20:sec.find('"', fr + 20)]
        # the drawing sits inside a frame's picture (inert, hidden from assistive technology)
        pic = sec.rfind('data-oa-picture', fr, s)
        if pic < 0:
            continue
        cls = re.search(r'\sclass="([^"]*)"', tag)
        cls = cls.group(1).split() if cls else []
        chart = "oac-svg" in cls
        tab = frame.startswith("A10 tab-") and 'viewBox="0 0 16 16"' in tag
        if not (chart or tab) or "mk" in cls:
            continue
        cands.append((s, e, gt, frame))
    # each drawing's markup with the ids nothing on the page names put aside, so the copies of one drawing read the same
    count_cache = {}

    def named(x):
        if x not in count_cache:
            count_cache[x] = page.count(x)
        return count_cache[x] > 1

    groups = {}
    for s, e, gt, frame in cands:
        inner = sec[s + gt:e - 6]
        if "<svg" in inner:
            continue
        key, k = inner, 0
        for x in ID_ATTR.findall(inner):
            if not named(x):
                key = key.replace(f' id="{x}"', f' id="\0{k}"', 1)
                k += 1
        groups.setdefault(key, []).append((s, e, gt, frame))
    edits, n_groups, n_copies, sprite = [], 0, 0, 0
    for key, bl in groups.items():
        if len(bl) < 2:
            continue
        n_groups += 1
        sym = "oa-c1-" + hashlib.sha256(key.encode()).hexdigest()[:10]
        s, e, gt, frame = bl[0]
        inner = sec[s + gt:e - 6]
        if sym in page:
            raise AssertionError(f"C1 3c: the id {sym} is already on the page")
        edits.append((s + gt, e - 6, f'<g id="{sym}">{inner}</g>'))
        sprite += len(inner.encode())
        for s2, e2, gt2, fr2 in bl[1:]:
            edits.append((s2 + gt2, e2 - 6, f'<use href="#{sym}"/>'))
            n_copies += 1
    edits.sort()
    out, last = [], 0
    for s, e, t in edits:
        out.append(sec[last:s])
        out.append(t)
        last = e
    out.append(sec[last:])
    new_sec = "".join(out)
    rec = {"groups": n_groups, "copies_by_use": n_copies, "drawn_once_bytes": sprite, "candidates": len(cands),
           "bytes_saved": len(sec.encode()) - len(new_sec.encode()),
           "plates": sorted({sec[sec.rfind('data-specimen="', 0, s) + 15:sec.find('"', sec.rfind('data-specimen="', 0, s) + 15)]
                             for key, bl in groups.items() if len(bl) > 1 for s, *_ in bl})}
    return page[:a] + new_sec + page[b:], rec


# --------------------------------------------------------------------------------------------------------------------
# 3d: three characters written as themselves
# --------------------------------------------------------------------------------------------------------------------
TEXT_REF = re.compile(r"&(?:quot|gt|#x27|#39);")
TEXT_CHAR = {"&quot;": '"', "&gt;": ">", "&#x27;": "'", "&#39;": "'"}
DQ_REF = re.compile(r"&(?:gt|#x27|#39);")      # inside "...": a double quote stays a reference
SQ_REF = re.compile(r"&(?:gt|quot);")          # inside '...': a single quote stays a reference


def step_3d(page):
    out, last, saved_text, saved_attr = [], 0, 0, 0
    sub = lambda rx, s: rx.sub(lambda m: TEXT_CHAR[m.group(0)], s)
    for kind, s, e, x in tokens(page):
        if kind == "text":
            seg = page[s:e]
            if "&" in seg:
                new = sub(TEXT_REF, seg)
                if new != seg:
                    out.append(page[last:s])
                    out.append(new)
                    saved_text += len(seg) - len(new)
                    last = e
        elif kind == "start":
            for aname, vs, ve, q in x[1]:
                if not q:
                    continue
                seg = page[vs:ve]
                if "&" not in seg:
                    continue
                new = sub(DQ_REF if q == '"' else SQ_REF, seg)
                if new != seg:
                    out.append(page[last:vs])
                    out.append(new)
                    saved_attr += len(seg) - len(new)
                    last = ve
    out.append(page[last:])
    return "".join(out), {"bytes_saved": saved_text + saved_attr, "text": saved_text, "attribute_values": saved_attr}


# --------------------------------------------------------------------------------------------------------------------
def run(page, steps=STEPS, cache=CACHE, anchor=CHAPTER_20):
    """Returns the smaller page and each step's record."""
    rec = {"before": len(page.encode()), "steps": list(steps)}
    for st in steps:
        b0 = len(page.encode())
        if st == "3a":
            page, r = step_3a(page)
        elif st == "3b":
            page, r = step_3b(page, cache)
        elif st == "3c":
            page, r = step_3c(page, anchor)
        elif st == "3d":
            page, r = step_3d(page)
        else:
            raise ValueError(f"C1: no step {st}")
        r["bytes_saved"] = b0 - len(page.encode())
        rec[st] = r
    rec["after"] = len(page.encode())
    rec["bytes_saved"] = rec["before"] - rec["after"]
    return page, rec


def self_test():
    bad = 0

    def check(name, ok):
        nonlocal bad
        print(f"{'pass' if ok else 'FAIL'} {name}")
        bad += not ok

    # 3d: text and quoted attribute values; script, style, comments and the other quote stay
    src = ('<p title="a &gt; b &quot;c&quot; &#x27;d&#39;" data-x=\'&quot;q&quot; &#x27;\'>x &gt; y &quot;z&quot; it&#x27;s &amp;gt;</p>'
           '<script>var s="&quot;&gt;";</script><style>a::after{content:"&gt;"}</style><!-- &quot; --><textarea>&gt;</textarea>')
    want = ('<p title="a > b &quot;c&quot; \'d\'" data-x=\'"q" &#x27;\'>x > y "z" it\'s &amp;gt;</p>'
            '<script>var s="&quot;&gt;";</script><style>a::after{content:"&gt;"}</style><!-- &quot; --><textarea>&gt;</textarea>')
    got, r = step_3d(src)
    check("3d: text and quoted values lose the three references; the value's own quote, script, style, comments and textarea keep theirs", got == want)
    # 3a: a repeated body goes, the first carries the list; a specimen whose order would change keeps its block
    S = lambda sid, body: f'<style>@scope ([data-specimen="{sid}"]){{{body}}}</style>'
    pg = ('<section class="chapter" id="c1"><div data-specimen="a">' + S("a", ".x{color:red}") + '</div>'
          '<div data-specimen="b">' + S("b", ".y{color:blue}") + S("b", ".x{color:red}") + '</div>'
          '<div data-specimen="c">' + S("c", ".x{color:red}") + '</div></section>')
    got, r = step_3a(pg)
    check("3a: b's repeated block stays (its own .y block would then follow it), c's goes into a's list",
          r["blocks_dropped"] == 1 and '[data-specimen="a"],[data-specimen="c"]' in got and S("b", ".x{color:red}") in got
          and S("c", ".x{color:red}") not in got and r["specimens_kept_whole_by_the_cascade_check"] == ["b"])
    pg2 = ('<section class="chapter" id="c1">' + S("a", ".x{color:red}") + S("b", ".x{color:red}") + '</section>'
           '<section class="chapter" id="c2"><style data-plate-css>@scope (#c2 [data-specimen]){.x{color:green}}</style>'
           + S("d", ".x{color:red}") + '</section>')
    got, r = step_3a(pg2)
    check("3a: a specimen after its chapter's shared scoped block keeps its own; one before it merges",
          '[data-specimen="a"],[data-specimen="b"]' in got and S("d", ".x{color:red}") in got and r["blocks_dropped"] == 1)
    got, r = step_3a('<script>var t=\'<style>@scope ([data-specimen="a"]){.x{y:1}}</style>\';</script>' + S("a", ".x{y:1}") + S("b", ".x{y:1}"))
    check("3a: a style inside a script's text is no style", r["blocks"] == 2 and r["blocks_dropped"] == 1 and got.startswith("<script>var t='<style>@scope"))
    # 3c: two copies of a chart in frames' pictures, an id nothing names put aside; a tracker mark stays
    fr = lambda f, body: f'<div data-oa-page-frame="{f}"><div data-oa-picture>{body}</div></div>'
    ch = lambda i: f'<svg class="oac-svg" viewBox="0 0 10 10"><title>T</title><pattern id="p-{i}"></pattern><path d="M0 0"/></svg>'
    mk = '<svg class="mk" viewBox="0 0 1 1"><path d="M1 1"/></svg>'
    pg3 = '<section class="chapter" id="web">' + fr("A07 1440-light", ch(1) + mk) + fr("A07 1440-dark", ch(2) + mk) + '</section>'
    got, r = step_3c(pg3)
    check("3c: the second chart becomes a <use> of the first; the tracker marks stay inline",
          r["groups"] == 1 and r["copies_by_use"] == 1 and got.count("<use href=\"#oa-c1-") == 1 and got.count(mk) == 2 and 'id="p-1"' in got and 'id="p-2"' not in got)
    # 3b: a cache entry with other pixels is refused; one with the same pixels is used
    from PIL import Image
    import tempfile
    im = Image.new("RGB", (8, 8), (10, 20, 30))
    b1 = io.BytesIO(); im.save(b1, "PNG", compress_level=0); raw = b1.getvalue()
    b2 = io.BytesIO(); im.save(b2, "PNG", optimize=True); small = b2.getvalue()
    im.putpixel((1, 1), (0, 0, 0))
    b3 = io.BytesIO(); im.save(b3, "PNG", optimize=True); wrong = b3.getvalue()
    sha = hashlib.sha256(raw).hexdigest()
    pg4 = f'<img src="data:image/png;base64,{base64.b64encode(raw).decode()}"><a download href="data:image/png;base64,{base64.b64encode(raw).decode()}">x</a>'
    with tempfile.TemporaryDirectory() as d:
        (Path(d) / f"{sha}.png").write_bytes(small)
        got, r = step_3b(pg4, d)
        ok1 = r["images_replaced"] == 1 and base64.b64encode(small).decode() in got and base64.b64encode(raw).decode() in got
        (Path(d) / f"{sha}.png").write_bytes(wrong)
        got, r = step_3b(pg4, d)
        ok2 = r["images_replaced"] == 0 and r["refused"] == [sha]
    check("3b: a cached file with the same pixels replaces the shown PNG (the download stays); one with a pixel changed is refused", ok1 and ok2)
    print("c1 self-test: " + ("every case passes" if not bad else f"{bad} failed"))
    return 1 if bad else 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--self-test" in args:
        sys.exit(self_test())
    if "--fill-cache" in args:
        page = Path(args[args.index("--fill-cache") + 1]).read_text(encoding="utf-8")
        lib = args[args.index("--lib") + 1]
        print(json.dumps(fill_cache(page, lib), indent=1))
        sys.exit(0)
    page = Path(args[0]).read_text(encoding="utf-8")
    steps = tuple(args[args.index("--steps") + 1].split(",")) if "--steps" in args else STEPS
    for st in steps:
        _, r = run(page, (st,))
        print(st, json.dumps({k: v for k, v in r[st].items() if k != "touched"}))
    out, rec = run(page, steps)
    print("all", rec["before"], "->", rec["after"], "saved", rec["bytes_saved"])
    if "--out" in args:
        Path(args[args.index("--out") + 1]).write_text(out, encoding="utf-8")
