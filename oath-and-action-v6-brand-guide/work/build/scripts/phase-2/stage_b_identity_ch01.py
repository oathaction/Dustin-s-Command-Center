"""Chapter 01's three pillar specimens drawn from the sprite (stage B round 2, D2-719).

s-01-pillars, s-01-21-correct and s-01-21-failure are written by the editor's build (guide_editor_build.py), which
inlines each Civic Line master. Their drawings move to the identity designer this round, and their words stay the
editor's. This step rewrites only the drawings, in place:

  pillar icons     each inline master becomes chapter 09's glyph (stage_b_identity_ch09.glyph): the master from the
                   sprite at 48 px, the 24 px pattern (the pixel fit under 2x, the master from 2x, DR-179, D2-783), with
                   data-icon-family="pillar" (D2-517); the current pillar's 48 px icon keeps its red through the
                   accent token; margins pulled in to the ink (D2-439), whole pixels at 24 px
  the kicker icon  s-01-21-correct's CL-055 Productivity, which is not among the 41 that read at 24 px (DR-136, D2-373),
                   becomes CL-057 from the sprite, data-icon-family="atlas" (Variable EC3, as chapter 10 files it; round 3),
                   with the word the editor gave it, "Workers' share of income" (editor's round 2 notes, section 4; DR-185)
  the phone column under 48em, the 48 px row keeps each icon's whole box, so its four words share one left edge, and
                   each downward arrow stands centered under its icon between rows, as chapter 09's row does (round 3,
                   CD-S1, CA-S6)
  the 24 px switch promotion C (DR-209, D2-1265): a 24 px drawing of the 37 topic and atlas drawings on the list of 41
                   draws its pixel fit on 1x screens and its master from 2x, as the pillar icons do (DR-179), in one
                   <svg viewBox="0 0 24 24"> with <use class="oa-at-1x" href="#oa-sym-<id>-24px"/> and
                   <use class="oa-at-2x" href="#oa-sym-<id>"/>. In chapter 01 that is s-01-21-correct's kicker icon,
                   CL-057. No word changes. A drawing placed before as the master alone is upgraded in place.

It touches only inline masters (an <svg> with an xmlns attribute and a Civic Line data-icon) and the one kicker word, so
it can run again after any rebuild of the editor's chapters, and a second run changes nothing.

Gate 2's fix pass (CD-S1, November 11, 2026): chapter 01's opener, s-01-opener, a light version of the editor's four
pillar pieces (s-01-pieces) read from that file: each piece keeps its pillar, kicker, headline, Track's "as of" date,
the hinge divider, "What you can do", its step and its one red button, with the words, classes and drawings the editor's
plate has; the blocks, the tracker and the source lines stay on the full plate after the rule index, and so does every
dek but Track's, which names H.R. 7008 whole with both its provisions, as DR-98 asks at a bill's first mention in a
chapter (the editor's second pass, row 14). The step
keeps only the styles those parts use, so the opener stays under 16 KB. It writes s-01-opener.html, its manifest entry
in manifest-identity-ch01.json, and the "opener" key in 01-purpose.json.

Run: python3 -I work/build/scripts/phase-2/stage_b_identity_ch01.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import stage_b_identity_ch09 as C9  # noqa: E402

SPEC = HERE.parents[1] / "guide/specimens"
FILES = ("s-01-pillars", "s-01-21-correct", "s-01-21-failure")
INLINE = re.compile(r'<svg\b[^>]*\sxmlns="http://www\.w3\.org/2000/svg"[^>]*\sdata-icon="(CL-\d{3})"[^>]*>.*?</svg>', re.S)
PILLAR = {"CL-019", "CL-020", "CL-021", "CL-022"}
KICKER_OLD, KICKER_NEW = ("CL-055", "Productivity"), ("CL-057", "Workers’ share of income")
# Each Civic Line drawing's family where chapter 10 files it under atlas (D2-517): CL-057 is Variable EC3, an atlas
# symbol, as Rule 01.21 and its alt now call it (round 3, the editor's BE-S7 follow-on). Any other drawing is a topic.
FAMILY = {"CL-057": "atlas"}
# The 37 topic and atlas drawings on the list of 41 (work/handoffs/phase-2/20261110_Stage-B-Ch10-Construction.md,
# section 10; D2-587). Each takes the 24 px switch since DR-209; their fits live in civic-line-v6/fit-24/ (D2-1265).
FIT_24 = frozenset(("CL-001 CL-004 CL-006 CL-010 CL-013 CL-023 CL-024 CL-028 CL-031 CL-032 CL-039 CL-040 CL-047 CL-048 CL-050 "
                    "CL-051 CL-054 CL-057 CL-060 CL-061 CL-067 CL-068 CL-070 CL-071 CL-072 R-05 R-06 R-08 R-09 R-14 R-15 R-17 "
                    "R-19 R-23 R-27 R-37 R-45").split())
assert len(FIT_24) == 37
# a 24 px drawing of one of the 37 that an earlier run placed as the master alone
MASTER_24 = re.compile(r'<svg viewBox="0 0 128 128" width="24" height="24" ([^>]*\bdata-icon="((?:CL|R)-\d+)"[^>]*)>'
                       r'<use href="#oa-sym-([a-z0-9-]+)"/></svg>')
STACK_CSS = ("@media (max-width:47.99em){.ed .prow-48{row-gap:" + str(C9.STACK_GAP) + "px}.ed .prow-48 .cl{margin:0!important}"
             ".ed .prow-48 .pi{position:relative}.ed .prow-48 .pi:not(:last-child)::after{position:absolute;left:24px;"
             "top:calc(100% + " + str(C9.STACK_GAP // 2) + "px);transform:translate(-50%,-50%);margin:0;line-height:1}}")
OLD_STACK_CSS = ("@media (max-width:47.99em){.ed .prow-48 .cl{margin:0!important}}",)      # round 2's, replaced in place


def _attr(tag, name):
    m = re.search(rf'\s{name}="([^"]*)"', tag)
    return m.group(1) if m else None


def topic(cid, size, cls):
    fam = FAMILY.get(cid, "topic")
    sid = cid.lower()
    if size == 24 and cid in FIT_24:          # the fit on 1x screens, the master from 2x (DR-209)
        vb, uses = "0 0 24 24", f'<use class="oa-at-1x" href="#oa-sym-{sid}-24px"/><use class="oa-at-2x" href="#oa-sym-{sid}"/>'
    else:
        vb, uses = "0 0 128 128", f'<use href="#oa-sym-{sid}"/>'
    return (f'<svg viewBox="{vb}" width="{size}" height="{size}" class="{cls}" aria-hidden="true" focusable="false" '
            f'data-icon="{cid}" data-icon-family="{fam}" style="color:var(--oa-component-icon-ink-on-newsprint)">{uses}</svg>')


def upgrade_24(text, log):
    """A 24 px drawing of one of the 37 placed as the master alone takes the switch, its attributes kept."""
    def swap(m):
        attrs, cid, ref = m.group(1), m.group(2), m.group(3)
        if cid not in FIT_24 or ref != cid.lower():
            return m.group(0)
        log.append(f"{cid} at 24 px takes the 1x and 2x switch")
        return (f'<svg viewBox="0 0 24 24" width="24" height="24" {attrs}><use class="oa-at-1x" href="#oa-sym-{ref}-24px"/>'
                f'<use class="oa-at-2x" href="#oa-sym-{ref}"/></svg>')
    return MASTER_24.sub(swap, text)


def rewrite(text, sid):
    log = []

    def swap(m):
        tag = re.match(r"<svg\b[^>]*>", m.group(0)).group(0)
        cid, size, cls = m.group(1), int(float(_attr(tag, "width"))), _attr(tag, "class") or "cl"
        red = _attr(tag, "data-red") == "signature"
        trimmed = (_attr(tag, "style") or "").startswith("margin")
        if cid in PILLAR:
            log.append(f"{cid} at {size} px{' with its red' if red else ''}")
            return C9.glyph(cid, size, "newsprint", red=red and size >= 48, trim=trimmed, cls=cls)
        if cid == KICKER_OLD[0] and sid == "s-01-21-correct":
            log.append(f"{cid} at {size} px became {KICKER_NEW[0]}")
            return topic(KICKER_NEW[0], size, cls)
        log.append(f"{cid} at {size} px, topic")
        return topic(cid, size, cls)

    out = INLINE.sub(swap, text)
    out = upgrade_24(out, log)
    for cid, fam in FAMILY.items():          # a drawing this step placed before with the topic family
        old = f'data-icon="{cid}" data-icon-family="topic"'
        if old in out:
            out = out.replace(old, f'data-icon="{cid}" data-icon-family="{fam}"')
            log.append(f"{cid} filed as {fam}")
    if sid == "s-01-21-correct":
        old = f'data-icon="{KICKER_NEW[0]}"'
        i = out.find(old)
        j = out.find(f'<span class="sx">{KICKER_OLD[1]}</span>', i)
        if i >= 0 and j >= 0:
            out = out[:j] + f'<span class="sx">{KICKER_NEW[1]}</span>' + out[j + len(f'<span class="sx">{KICKER_OLD[1]}</span>'):]
            log.append(f"kicker word {KICKER_OLD[1]} became {KICKER_NEW[1]}")
    if sid == "s-01-pillars" and STACK_CSS not in out:
        old = next((o for o in OLD_STACK_CSS if o in out), None)
        out = out.replace(old, STACK_CSS, 1) if old else out.replace("</style>", STACK_CSS + "</style>", 1)
        log.append("stacked column keeps whole boxes, arrows under the icons")
    return out, log


# ============================================================================================ the opener (CD-S1)
CHAP = HERE.parents[1] / "guide/chapters/01-purpose.json"
OPENER_ID = "s-01-opener"
OPENER_MANIFEST = SPEC / "manifest-identity-ch01.json"
OPENER_CAPTION = ("One piece for each pillar at true size, from its kicker to the one red step after the hinge divider. "
                  "Explain and Track quote real records, and the four pieces stand whole, with their sources, after the rule index.")
DROP_P = ("dek", "by")                   # the full plate's parts the opener leaves out; Track keeps its dek (DR-98)
KEEP_DEK = "Track"
HR7008_WHOLE = ("H.R. 7008, the Stop Insider Trading Act", "buying individual stocks", "photo ID to vote in federal elections")
DROP_DIV = ("blk", "trk")
KEEP_CLASSES = {"ed", "sp", "sp-flow", "grid4", "pl", "pc", "kick", "lb", "dot", "sx", "hl", "dek", "lab", "asof", "hg", "hamp",
                "wycd", "step", "ask", "illus"}


def _drop_div(html, cls):
    """Remove each <div class="cls"> with everything inside it, nested divs included."""
    while True:
        i = html.find(f'<div class="{cls}"')
        if i < 0:
            return html
        depth, j = 0, i
        for m in re.finditer(r"<div\b|</div>", html[i:]):
            depth += 1 if m.group(0) == "<div" else -1
            if depth == 0:
                j = i + m.end()
                break
        html = html[:i] + html[j:]


def _css_keep(css):
    """The rules of a style sheet whose selectors name only kept classes; @media blocks keep their kept rules."""
    out, i = [], 0
    while i < len(css):
        k = css.find("{", i)
        if k < 0:
            break
        head = css[i:k].strip()
        depth, j = 0, k
        while j < len(css):
            depth += {"{": 1, "}": -1}.get(css[j], 0)
            j += 1
            if depth == 0:
                break
        block = css[k + 1:j - 1]
        if head.startswith("@media"):
            inner = _css_keep(block)
            if inner:
                out.append(f"{head}{{{inner}}}")
        elif head and set(re.findall(r"\.([A-Za-z][\w-]*)", head)) <= KEEP_CLASSES:
            out.append(f"{head}{{{block}}}")
        i = j
    return "\n".join(out)


def _text(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).replace(" ·", " ·").strip()


def opener():
    src = (SPEC / "s-01-pieces.html").read_text()
    m = re.search(r"<style>(.*?)</style>(.*)$", src, re.S)
    css, body = m.group(1), m.group(2).strip()
    for c in DROP_DIV:
        body = _drop_div(body, c)
    head = '<div><p class="pl">'
    chunks = body.split(head)                # one chunk per piece after the first
    for i in range(1, len(chunks)):
        for c in DROP_P:
            if not (c == "dek" and chunks[i].startswith(KEEP_DEK + "</p>")):
                chunks[i] = re.sub(rf'<p class="{c}">.*?</p>', "", chunks[i], flags=re.S)
    body = head.join(chunks)
    body = re.sub(r"\n+", "\n", body)
    pieces = re.findall(r'<div><p class="pl">(.*?)</p><div class="pc">(.*?)</div></div>', body, re.S)
    assert len(pieces) == 4, f"s-01-pieces holds {len(pieces)} pieces, not four"
    assert body.count('class="ask"') == 4 and body.count('class="hg"') == 4, "each piece keeps its hinge and its one ask"
    track = next(inner for pillar, inner in pieces if pillar == KEEP_DEK)
    assert all(w in _text(track) for w in HR7008_WHOLE), "the Track piece must name H.R. 7008 whole with both provisions (DR-98)"
    assert body.count('class="dek"') == 1, "only Track keeps its dek"
    parts = []
    for pillar, inner in pieces:
        hl = _text(re.search(r'<p class="hl">(.*?)</p>', inner, re.S).group(1))
        ask = _text(re.search(r'<span class="ask"[^>]*>(.*?)</span>', inner, re.S).group(1))
        asof = re.search(r'<p class="lab asof">(.*?)</p>', inner, re.S)
        lab = ", Illustrative" if 'class="illus"' in inner else ""
        t = _text(asof.group(1)) if asof else ""
        when = f", {t[:1].lower()}{t[1:]}" if asof else ""        # "as of November 5, 2026": the month keeps its capital
        dek = re.search(r'<p class="dek">(.*?)</p>', inner, re.S)
        deck = f" {_text(dek.group(1))}" if dek else ""
        parts.append(f"{pillar}{lab}: {hl}{when}.{deck} It ends on {ask}.")
    alt = ("Four pieces at a phone's text width, one per pillar, each from its kicker and headline to the hinge divider, "
           "What you can do, one step and one red button. " + " ".join(parts))
    alt = alt.replace("..", ".").replace("?.", "?")
    html = (f"<!-- {OPENER_ID}: Oath & Action guide, Edition 06, chapter 01's opener. Identity designer, Gate 2's fix pass, "
            f"November 11, 2026, from the editor's s-01-pieces. -->\n<style>\n{_css_keep(css)}\n</style>\n{body}\n")
    (SPEC / f"{OPENER_ID}.html").write_text(html)
    entry = {OPENER_ID: {"chapter": "01", "rule": None, "alt": alt, "illustrative": False,
                         "notes": "Gate 2's fix pass, CD-S1: chapter 01's opener, a light version of s-01-pieces read from the "
                                  "editor's file by stage_b_identity_ch01.py. Each piece keeps its pillar, kicker, headline, "
                                  "Track's as-of date, the hinge divider, What you can do, its step and its red button; the "
                                  "dek, blocks, tracker and source lines stay on the full plate. It flows, as that plate does."}}
    OPENER_MANIFEST.write_text(json.dumps(entry, indent=1, ensure_ascii=False) + "\n")
    ch = json.loads(CHAP.read_text())
    want = {"specimen": OPENER_ID, "caption": OPENER_CAPTION.replace("'", "\u2019")}
    if ch.get("opener") != want:
        ch["opener"] = want
        CHAP.write_text(json.dumps(ch, indent=1, ensure_ascii=False) + "\n")
    return [f"{OPENER_ID}: {len(html.encode()):,} bytes before the build inlines B, four pieces"]


def run():
    report = {}
    for sid in FILES:
        f = SPEC / f"{sid}.html"
        text = f.read_text()
        new, log = rewrite(text, sid)
        assert not INLINE.search(new), f"{sid}: an inline Civic Line master is left"
        if new != text:
            f.write_text(new)
        report[sid] = log or ["unchanged"]
    report[OPENER_ID] = opener()
    return report


if __name__ == "__main__":
    for k, v in run().items():
        print(k + ":", "; ".join(v))
