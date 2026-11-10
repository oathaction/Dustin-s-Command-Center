"""Chapter 01's three pillar specimens drawn from the sprite (stage B round 2, D2-719).

s-01-pillars, s-01-21-correct and s-01-21-failure are written by the editor's build (guide_editor_build.py), which
inlines each Civic Line master. Their drawings move to the identity designer this round, and their words stay the
editor's. This step rewrites only the drawings, in place:

  pillar icons     each inline master becomes chapter 09's glyph (stage_b_identity_ch09.glyph): the master from the
                   sprite at 48 px, the 24 px pattern (the pixel fit under 2x, the master from 2x, DR-179, D2-783), with
                   data-icon-family="pillar" (D2-517); the current pillar's 48 px icon keeps its red through the
                   accent token; margins pulled in to the ink (D2-439), whole pixels at 24 px
  the kicker icon  s-01-21-correct's CL-055 Productivity, which is not among the 41 that read at 24 px (DR-136, D2-373),
                   becomes CL-057 from the sprite, data-icon-family="topic", with the word the editor gave it, "Workers'
                   share of income" (editor's round 2 notes, section 4; DR-185)
  the phone column under 48em, the 48 px row keeps each icon's whole box, so its four words share one left edge, and
                   each downward arrow stands centered under its icon between rows, as chapter 09's row does (round 3,
                   CD-S1, CA-S6)

It touches only inline masters (an <svg> with an xmlns attribute and a Civic Line data-icon) and the one kicker word, so
it can run again after any rebuild of the editor's chapters, and a second run changes nothing.

Run: python3 -I work/build/scripts/phase-2/stage_b_identity_ch01.py
"""
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
STACK_CSS = ("@media (max-width:47.99em){.ed .prow-48{row-gap:" + str(C9.STACK_GAP) + "px}.ed .prow-48 .cl{margin:0!important}"
             ".ed .prow-48 .pi{position:relative}.ed .prow-48 .pi:not(:last-child)::after{position:absolute;left:24px;"
             "top:calc(100% + " + str(C9.STACK_GAP // 2) + "px);transform:translate(-50%,-50%);margin:0;line-height:1}}")
OLD_STACK_CSS = ("@media (max-width:47.99em){.ed .prow-48 .cl{margin:0!important}}",)      # round 2's, replaced in place


def _attr(tag, name):
    m = re.search(rf'\s{name}="([^"]*)"', tag)
    return m.group(1) if m else None


def topic(cid, size, cls):
    return (f'<svg viewBox="0 0 128 128" width="{size}" height="{size}" class="{cls}" aria-hidden="true" focusable="false" '
            f'data-icon="{cid}" data-icon-family="topic" style="color:var(--oa-component-icon-ink-on-newsprint)">'
            f'<use href="#oa-sym-{cid.lower()}"/></svg>')


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
    return report


if __name__ == "__main__":
    for k, v in run().items():
        print(k + ":", "; ".join(v))
