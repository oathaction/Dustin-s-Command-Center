#!/usr/bin/env python3
"""Writes work/handoffs/phase-3/20261120_Board-3-Decisions.json (the data lead's decision file for board 3).

Run from oath-and-action-v6-brand-guide/ with python3 -I. Every count comes from board_3_data_lead_counts.py (beside this
file) or from the build report named by --report; the words are the data lead's first draft, which the editor owns once
written (board 3 brief, "The decision file"). Once the editor has worked on the file, rerun only with --counts-only,
which replaces the "counts" key and the time and leaves every word alone.
"""
import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path.cwd()
OUT = ROOT / "work/handoffs/phase-3/20261120_Board-3-Decisions.json"
spec = importlib.util.spec_from_file_location("counts", HERE / "board_3_data_lead_counts.py")
counts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(counts)

PAGES = {"v9": "work/boards/phase-3/round-3/20261113_Guide-Preview-V9.html",
         "v10": "work/boards/phase-3/round-4/20261113_Guide-Preview-V10.html",
         "v11": "work/boards/phase-3/round-5/20261114_Guide-Preview-V11.html",
         "v12": "work/boards/phase-3/review-4-5/20261116_Guide-Preview-V12.html",
         "final": "the chat 8 strict build after the second pass, version 13 (the main session names its path)"}
REG = "work/ledger/20261116_Deferred-Fixes-Register.md"
SCRIPT = "work/build/scripts/phase-3/board_3_data_lead_counts.py"
HOME = "work/build/scripts/phase-3/board_3_data_lead_counts.py"


def G(el, w, label, role="after", page="final", row=None, ground="newsprint", fold=False, setup=None, spec=None):
    p = {"kind": "guide", "page": page, "element": el, "width": w, "ground": ground, "path": None, "label": label, "role": role}
    if spec:
        p["spec"] = spec
    if row:
        p["row"] = row
    if fold:
        p["fold"] = True
    if setup:
        p["setup"] = setup
    return p


def MAKE(label, owner, how, row=None, w=1440):
    p = {"kind": "to-make", "path": None, "width": w, "label": label, "role": "view", "owner": owner, "how": how}
    if row:
        p["row"] = row
    return p


def reg(code, section="Held for Dustin (board 3)"):
    return {"file": REG, "section": section, "code": code}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--report", required=True, help="the strict build report the Phase 4 figures come from")
    ap.add_argument("--state", default="draft")
    ap.add_argument("--counts-only", action="store_true", help="replace only the counts key of the file on disk")
    a = ap.parse_args()
    atlas = json.loads(counts.ATLAS.read_text())
    r9, log = counts.rule_01_9(atlas)
    dr = counts.dr_229(log)
    ch = counts.changed_found()
    held = counts.held_found()
    who = counts.routes_who(atlas)
    rep = json.loads(Path(a.report).read_text())
    p4 = rep["weight"]["projection"]["phase_4"]
    pics = rep["pictures"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    held_by_code = {h["code"]: h for h in held["rows"]}
    for h in held["rows"]:
        h.pop("section", None)

    ballot = [{"n": i + 1, "name": s[0], "what_happens": s[1], "law": s[2]} for i, s in enumerate(counts_steps("BALLOT_STEPS"))]
    court = [{"n": i + 1, "name": s[0], "what_happens": s[1], "law": s[2]} for i, s in enumerate(counts_steps("COURT_STEPS"))]

    # ------------------------------------------------------------------------------------------------ panel 1: trackers
    trackers = {
        "id": "trackers", "title": "The two new trackers’ step names",
        "lede": ("Rules 11.10 and 11.11 track a state ballot measure and a federal court case in six steps each, on the bill "
                 "tracker’s marks. Their twelve step names come from the law, each with its source, and they wait for your "
                 "word as the bill’s six did (DR-108)."),
        "approval": "each",
        "items": [
            {"id": "11.10", "rule": "11.10", "title": "Rule 11.10, a state ballot measure, in six steps",
             "answer": ("The six names are Filed, Title and summary, Signatures, Legislature, On the ballot and Vote. Step 4 "
                        "holds only where a state’s initiative goes to the Legislature first; a measure that goes straight to "
                        "the ballot keeps step 4 under a slash, as the bill tracker marks a step that never happened."),
             "what_changed": ("New in round 5 (C-118). The plate draws three invented measures, each labeled Illustrative: one "
                              "counted but not yet certified, one approved by voters and certified, and one that failed to "
                              "qualify, which ends on a square at step 3. A table after the rule gives each step, what happens "
                              "at it and where the law of Massachusetts, California, Ohio and Michigan sets it. The review’s "
                              "fixes changed words only (C-123), and the second pass gave the plate’s alt its title and key, so "
                              "a screen reader hears it once (RS-1)."),
             "why": ("DR-108 approved the bill’s six names by name, and DR-231 puts these trackers under the same rule, so "
                     "their names need the same word from you."),
             "recommendation": "Approve the six names as the plate prints them.",
             "refs": ["DR-108", "DR-150", "DR-231", "DR-274", "DR-275", "D3-2011", "C-118", "C-123"],
             "question_for_dustin": True,
             "steps": ballot,
             "marks": ["Done", "Now", "Not yet", "Never happened", "Stopped"],
             "facts": [{"label": "Invented items", "value": "Measures 99010, 99011 and 99013, labeled Illustrative (DR-275)"},
                       {"label": "States read for the law", "value": "Massachusetts, California, Ohio and Michigan"}],
             "pictures": [G("fig-s-11-10-correct", 1440, "The plate at a 1,440 px window", row="1440"),
                          G("fig-s-11-10-correct", 390, "The plate on a 390 px phone", row="390"),
                          G("fig-s-11-ballot-steps", 1440, "The step table after Rule 11.10, with the law for each step"),
                          G("fig-s-11-10-failure", 1440, "The failure plate: a count read as a result", fold=True)]},
            {"id": "11.11", "rule": "11.11", "title": "Rule 11.11, a federal court case, in six steps",
             "answer": ("The six names are Filed, Trial court ruling, Appeal, Appeals court ruling, Supreme Court petition and "
                        "Supreme Court ruling. A petition the Supreme Court denies ends on a square at step 5, and the "
                        "appeals court’s ruling stands."),
             "what_changed": ("New in round 5 (C-118). The plate draws three invented federal civil cases, each labeled "
                              "Illustrative: one argued and waiting on the appeals court, one reversed and sent back by the "
                              "Supreme Court, and one whose petition the Court denied. A table after the rule gives each step "
                              "and the rule or statute behind it. The review’s fixes changed words only, among them a ruling no "
                              "one appeals, which keeps the steps after it under slashes (C-123, calls 4 and 5); the second "
                              "pass gave the plate’s alt its title and key (RS-1)."),
             "why": "As for Rule 11.10: DR-231 puts the court case tracker under DR-108, which approved the bill’s names by name.",
             "recommendation": "Approve the six names as the plate prints them.",
             "refs": ["DR-108", "DR-231", "DR-274", "DR-275", "D3-2011", "C-118", "C-123"],
             "question_for_dustin": True,
             "steps": court,
             "marks": ["Done", "Now", "Not yet", "Stopped"],
             "facts": [{"label": "Invented items", "value": "Cases 99014, 99015 and 99016, labeled Illustrative (DR-275)"},
                       {"label": "The docket’s word", "value": "“Affirmed”, explained once in the rule’s text (ED5-3)"}],
             "pictures": [G("fig-s-11-11-correct", 1440, "The plate at a 1,440 px window", row="1440"),
                          G("fig-s-11-11-correct", 390, "The plate on a 390 px phone", row="390"),
                          G("fig-s-11-court-steps", 1440, "The step table after Rule 11.11, with the rule or statute for each step"),
                          G("fig-s-11-11-failure", 1440, "The failure plate: a denied petition read as a ruling", fold=True),
                          G("fig-s-11-marks", 1440, "The tracker marks, as Rule 11.2 draws them for every tracker", fold=True)]},
        ],
    }

    # ---------------------------------------------------------------------------------------- panel 2: changed approved work
    changed_items = [
        {"id": "board-1-maps", "title": "S12, S16, S78 and S07: the maps at a desk and on a phone",
         "specs": ["S12", "S16", "S78", "S07"],
         "answer": ("S12 now draws the stacked tile you chose on board 2, and on a phone S12, S16 and S78 print a code in every "
                    "one of the 51 tiles. S07’s phone tiles move 1 px."),
         "what_changed": ("At a desk S12 draws its stacked tile from a 618 px drawing (DR-261). At the 326 px phone drawing, S12, "
                          "S16 and S78 code all 51 states: S16 in a code column under 358 px, S12 and S78 on a 2 px tile gap, "
                          "the token release 6.0.0-gate3.3 (2.5 px before), which also moves S07’s phone tiles 1 px. S12’s "
                          "phone tiles now take their edge in the context ink, and its phone key prints “United States 5.9”."),
         "why": "Board 2 noted three states with no code on S12’s phone drawing; the tile gap is a chart token, which Gate 3 decides.",
         "recommendation": "Approve them as drawn.",
         "refs": ["DR-261", "D3-1553", "D3-1556", "D3-1710", "C-108", "C-112", "C-125"],
         "ledger": ["C-108", "C-112", "C-125"], "approved_at": "board 1 (S07, S12, S16) and board 2 (S78, DR-263; S12’s stacked tile, DR-261)",
         "shows": True, "question_for_dustin": False,
         "pictures": [G("oac-s-14-s12", 1440, "S12 at a 1,440 px window, the stacked tile", spec="S12", row="s12-desk"),
                      {"kind": "board-pictures", "spec": "s12", "width": 1440, "ground": "newsprint",
                       "path": "work/handoffs/phase-3/board-2-pictures/20261113_S12-Stacked-Tile-1440-Drawing-Newsprint.png",
                       "label": "Board 2’s picture of the stacked tile, as you chose it", "role": "before", "row": "s12-desk"},
                      G("oac-s-14-s12", 390, "S12 on a phone before round 4", role="before", page="v9", spec="S12", row="s12-phone"),
                      G("oac-s-14-s12", 390, "S12 on a phone now", spec="S12", row="s12-phone"),
                      G("oac-s-14-s16", 390, "S16 on a phone before round 4", role="before", page="v9", spec="S16", row="s16-phone"),
                      G("oac-s-14-s16", 390, "S16 on a phone now", spec="S16", row="s16-phone"),
                      G("oac-s-14-s78", 390, "S78 on a phone before round 4", role="before", page="v9", spec="S78", row="s78-phone"),
                      G("oac-s-14-s78", 390, "S78 on a phone now", spec="S78", row="s78-phone"),
                      G("oac-s-14-s07", 390, "S07 on a phone before round 4", role="before", page="v9", spec="S07", row="s07-phone", fold=True),
                      G("oac-s-14-s07", 390, "S07 on a phone now, its tiles 1 px apart from the gap token", spec="S07", row="s07-phone", fold=True)]},
        {"id": "S37", "spec": "S37", "rule": "14.129", "title": "S37, the heat table: curled apostrophes",
         "answer": "S37’s drawn labels and its table print curled apostrophes.",
         "what_changed": ("Straight apostrophes in S37’s drawn labels and table became curled ones. Board 2’s pass held S37 because two "
                          "drawn labels change, so it carried to round 4 with its drawing shown here (D3-1556). No figure or mark moves."),
         "why": "Printed words take curled apostrophes; data and exports keep them as stored (D3-1556).",
         "recommendation": "Approve it as drawn.", "refs": ["D3-1556", "C-108"], "ledger": ["C-108"],
         "approved_at": "board 2", "shows": True, "question_for_dustin": False,
         "pictures": [G("oac-s-14-s37", 1440, "Before round 4", role="before", page="v9", spec="S37", row="s37", fold=True),
                      G("oac-s-14-s37", 1440, "Now", spec="S37", row="s37", fold=True)]},
        {"id": "S14", "spec": "S14", "rule": "14.32", "title": "S14, monthly jobs: its source line and its two label keys",
         "answer": ("S14’s source line names the September 2026 release, as S96 does, and two label keys move its latest label "
                    "clear of a gridline and dash its average over the preliminary months."),
         "what_changed": ("The source line names the payroll release (D3-2144). Two opt-in keys in S14’s spec, "
                          "`labels.latest_clear` and `labels.average_dash`, move the latest label clear of its gridline and "
                          "dash the average where it includes a preliminary month (D3-2143). The data, the scale and the title "
                          "are as board 1 approved."),
         "why": "One series prints one release line, and a label crossed by a gridline is hard to read (call 18).",
         "recommendation": "Approve the three changes as drawn.",
         "refs": ["D3-2143", "D3-2144", "C-124", "C-130"], "ledger": ["C-124", "C-130"], "approved_at": "board 1",
         "shows": True, "question_for_dustin": False,
         "pictures": [G("oac-s-14-s14", 1440, "Before the fix pass", role="before", page="v11", spec="S14", row="1440"),
                      G("oac-s-14-s14", 1440, "Now", spec="S14", row="1440"),
                      G("oac-s-14-s14", 390, "Before the fix pass, on a phone", role="before", page="v11", spec="S14", row="390"),
                      G("oac-s-14-s14", 390, "Now, on a phone", spec="S14", row="390")]},
        {"id": "S40", "spec": "S40", "rule": "14.132", "title": "S40, the tracker list: committee vote dates in words",
         "answer": "S40 prints its committee vote dates in words through a new table format, `date-lead`.",
         "what_changed": ("Four cells such as “2025-12-17, 50 to 1” now read “December 17, 2025, 50 to 1” (C-130). No row, "
                          "mark or value changes."),
         "why": "Chapter 02’s house rule H05 writes the month as a word; S40’s were the only figure dates in chapters 11, 13, 14 and 15 (DF-16).",
         "recommendation": "Approve it as drawn.", "refs": ["C-130"], "ledger": ["C-130"], "approved_at": "board 2",
         "shows": True, "question_for_dustin": False,
         "pictures": [G("oac-s-14-s40", 1440, "Before the fix pass", role="before", page="v11", spec="S40", row="1440"),
                      G("oac-s-14-s40", 1440, "Now", spec="S40", row="1440")]},
        {"id": "rules-14-1-to-14-14", "title": "Rules 14.1 to 14.14: words",
         "answer": ("The fourteen chart rules shown at board 2 changed in words only: each prints its own Basis line, the role "
                    "inks are defined where first used, and Rule 14.1 links “Choose a chart”."),
         "what_changed": ("Rules 14.1 to 14.12 and 14.14 each print their own Basis line; Rules 14.5 and 14.6 define the three "
                          "role inks at first use, and Rule 14.6’s light fill covers every other bar only where the title names "
                          "one bar; Rule 14.3’s spec says “the text’s ink”; Rule 14.1 names and links “Choose a chart”; the "
                          "chapter’s introduction says “a fixed copy of its source’s data”; group 17’s line names all seven of "
                          "its forms; group 18’s line says the three reforms’ “records name one housing loop”."),
         "why": "The review found the rules leaning on terms they had not defined (DF-12, DF-13, CD-S8, NB-M1; call 3).",
         "recommendation": "Approve the words as printed.", "refs": ["C-128"], "ledger": ["C-128"], "approved_at": "board 2",
         "shows": True, "question_for_dustin": False,
         "pictures": [G("rule-14-6", 1440, "Rule 14.6 before the fix pass", role="before", page="v11", row="14.6"),
                      G("rule-14-6", 1440, "Rule 14.6 now", row="14.6"),
                      G("rule-14-1", 1440, "Rule 14.1 before the fix pass", role="before", page="v11", row="14.1", fold=True),
                      G("rule-14-1", 1440, "Rule 14.1 now", row="14.1", fold=True)]},
        {"id": "14.144-pips", "rule": "14.144", "title": "Rule 14.144: pips beside each effect code, and the phone line-up",
         "answer": ("Each reform card draws Rule 13.5’s pips beside each whole effect code, and on a phone each code’s pips stay "
                    "on its line. The cards still print no total."),
         "what_changed": ("Ruling (d) had printed the effects as words with no pips (D3-1973). Call 2 replaced that: Rule 13.5, "
                          "which you approved with chapter 13, governs the effect mark, so each code draws its pips (D3-2127). "
                          "The phone line-up sets each family’s effects one reform a row (CR-S3), and the second pass keeps "
                          "every reform’s pips on its code’s line at every width (CR-S23). The atlas’s sentence that codes "
                          "are never added stays, and the failure plate’s total stays its fault."),
         "why": "One effect mark across the guide; Rules 15.16 and 15.20 already draw the pips (DR-237).",
         "recommendation": "Approve the pips as drawn.",
         "refs": ["D3-1973", "D3-2127", "DR-237", "C-124", "CR-S23"], "ledger": ["C-124"],
         "approved_at": "ruling (d), inside the round 5 plan (DR-276)", "shows": True, "question_for_dustin": False,
         "pictures": [G("fig-s-14-144-correct", 1440, "Before the fix pass: no pips", role="before", page="v11", row="1440"),
                      G("fig-s-14-144-correct", 1440, "Now: pips beside each code", row="1440"),
                      G("fig-s-14-144-correct", 390, "Before the fix pass, on a phone", role="before", page="v11", row="390"),
                      G("fig-s-14-144-correct", 390, "Now, on a phone: the line-up", row="390")]},
        {"id": "15.20-chooser", "rule": "15.20", "title": "Rule 15.20: the chooser’s list form",
         "answer": ("The two reforms now sit in one list at one width, and the failure plate takes the same list form. "
                    "The keyline these plates draw inside the red ring is a separate question below, since it touches a "
                    "settled mark."),
         "what_changed": ("Call 15 changed the shared chooser once, on Rules 15.20 and 14.144: one width for the choices, through "
                          "Rule 18.3’s opt-in list form (`oa-choice-row--list`, D3-2243), and a keyline inside a chosen pill’s "
                          "red ring (D3-2140; see the keyline item under “Held for you”). The second pass gave "
                          "the failure plate the same list form, so its options stop splitting into columns; its fault, both "
                          "reforms lit at once with a combined score, stays as captioned (CR-S1’s remainder)."),
         "why": "Five readers named the same faults in one shared component (DD-R2, DD-R5, AX-S5, CR-S1, CD-S5).",
         "recommendation": "Approve the chooser’s list form, on both plates.",
         "refs": ["D3-2140", "D3-2243", "C-129", "C-132", "CR-S1"], "ledger": ["C-129", "C-132"],
         "approved_at": "built in round 4 under the approved plan (DR-270); D3-2140 has board 3 show it changed", "shows": True, "question_for_dustin": False,
         "pictures": [G("fig-s-15-20-correct", 1440, "Before the fix pass", role="before", page="v11", row="1440"),
                      G("fig-s-15-20-correct", 1440, "Now", row="1440"),
                      G("fig-s-15-20-correct", 390, "Before the fix pass, on a phone", role="before", page="v11", row="390"),
                      G("fig-s-15-20-correct", 390, "Now, on a phone", row="390"),
                      G("fig-s-15-20-failure", 1440, "The failure plate before the second pass", role="before", page="v12", row="fail", fold=True),
                      G("fig-s-15-20-failure", 1440, "The failure plate now", row="fail", fold=True)]},
        {"id": "chapter-15-approved", "title": "Rules 15.1, 15.6, 15.11, 15.12, 15.15 and 15.16: words and chips",
         "answer": ("Six chapter 15 rules you approved at board 2 changed in small ways: three read-aloud lines say “fewer”, "
                    "three plates’ chips drop the wide hyphen, and Rule 15.16 explains “outcome family”."),
         "what_changed": ("The read-aloud lines on Rules 15.1, 15.6 and 15.15 say “fewer” where a count falls; Rule 15.16 glosses "
                          "“outcome family”; chip IDs drop tabular figures on 37 plates, among them Rules 15.11, 15.12 and "
                          "15.16, so “R-04” no longer reads “R - 04”. No mark or loop drawing moves."),
         "why": "The review’s word and craft readers (C-129).",
         "recommendation": "Approve them as printed.", "refs": ["C-129"], "ledger": ["C-129"], "approved_at": "board 2",
         "shows": True, "question_for_dustin": False,
         "pictures": [G("fig-s-15-16-correct", 1440, "Rule 15.16 before the fix pass", role="before", page="v11", row="15.16"),
                      G("fig-s-15-16-correct", 1440, "Rule 15.16 now", row="15.16"),
                      G("fig-s-15-11-correct", 1440, "Rule 15.11 before", role="before", page="v11", row="15.11", fold=True),
                      G("fig-s-15-11-correct", 1440, "Rule 15.11 now", row="15.11", fold=True)]},
        {"id": "chapter-11", "title": "Chapter 11: the bill’s step table and the new numbers",
         "answer": ("The bill’s step table sets each step’s number over its name, like the two new tables, and Rules 11.10 to "
                    "11.16 became 11.12 to 11.18 to make room for the new trackers."),
         "what_changed": ("`s-11-steps` changes layout only: number over name (C-118). The old Rules 11.10 to 11.16 are now 11.12 "
                          "to 11.18, with every link and citation fixed in one pass (DR-274); past boards and the decision log "
                          "keep the numbers they printed. In the second pass the alt of Rule 11.12’s two plates, records "
                          "requests, gained its title and key (RS-1), which hides the picture from a screen reader and changes "
                          "nothing a reader sees."),
         "why": "DR-274 placed the new trackers in group 2 and renumbered the rules after them.",
         "recommendation": "Approve the table as drawn.", "refs": ["DR-274", "C-118", "RS-1"], "ledger": ["C-118"],
         "approved_at": "Gate 2", "shows": True, "question_for_dustin": False,
         "pictures": [G("fig-s-11-steps", 1440, "Before round 5", role="before", page="v10", row="1440"),
                      G("fig-s-11-steps", 1440, "Now", row="1440")]},
        {"id": "image-stages", "title": "The words inside image stages: heard once",
         "answer": (f"A screen reader now hears {pics['hidden']} image stages by their alt alone, once, where it heard them "
                    "twice; nothing changes on the screen."),
         "what_changed": (f"`plate()` hides an image stage’s picture from a screen reader where its alt carries every word the "
                          f"picture holds (D3-2153): 95 of 416 at the fix pass, {pics['hidden']} after the second pass gave six "
                          f"tracker alts their missing words (RS-1). The other {pics['open']} keep their words open, since their "
                          "alts lack a word, and wait in the deferred fixes register. Two alts that hid the Illustrative label "
                          "now lead with it."),
         "why": "Words heard twice were a carried item that reaches approved work in 19 chapters and the proofs (DR-278 (b)).",
         "recommendation": "Approve the change.", "refs": ["DR-278", "D3-2153", "C-131", "RS-1"], "ledger": ["C-131"],
         "approved_at": "19 chapters and the proofs, Gate 2 on", "shows": False,
         "shows_note": "Nothing changes on the screen; the change is in what a screen reader hears.",
         "facts": [{"label": "Hidden", "value": f"{pics['hidden']} of {pics['hidden'] + pics['open']} image stages"},
                   {"label": "Open", "value": f"{pics['open']}, listed for the register"}],
         "question_for_dustin": False, "pictures": []},
        {"id": "masthead", "title": "The masthead’s measured room and focus offsets",
         "answer": "A focused link no longer hides under the masthead at 360 to 372 px, at 1,024 to 1,362 px or with large text.",
         "what_changed": ("The shell measures the masthead’s real height and sets the scroll and focus offsets from it, with "
                          "floors for a page with scripts off (call 10)."),
         "why": "At 1,024 to 1,360 px a focused link in the chapter rail could sit wholly under the masthead (AX-M1; WCAG 2.4.11).",
         "recommendation": "Approve the change.", "refs": ["DR-278", "D3-2135", "C-132"], "ledger": ["C-132"],
         "approved_at": "Gate 2 (the shell)", "shows": True, "question_for_dustin": False,
         "pictures": [G("header.masthead", 1024, "Before the fix pass: a focused rail link under the masthead", role="before",
                        page="v11", row="1024", setup={"focus": "the first chapter rail link past the masthead's height", "scroll": "to the focused link"}),
                      G("header.masthead", 1024, "Now: the same link clear of it", row="1024",
                        setup={"focus": "the first chapter rail link past the masthead's height", "scroll": "to the focused link"})]},
        {"id": "where-to-start", "title": "“Where to start” at 320 px with 200 percent text",
         "answer": "The page no longer scrolls sideways at 320 px with text at 200 percent; it scrolled 33 px.",
         "what_changed": "The “Where to start” lines, narrow code plates and closing related lists now wrap (call 12).",
         "why": "A page that scrolls sideways at 320 px fails reflow (AX-S7; WCAG 1.4.10); a carried item (DR-278 (c)).",
         "recommendation": "Approve the change.", "refs": ["DR-278", "D3-2137", "C-132"], "ledger": ["C-132"],
         "approved_at": "Gate 2 (the start page)", "shows": True, "question_for_dustin": False,
         "pictures": [G("start", 320, "Before the fix pass", role="before", page="v11", row="320", setup={"text_scale": 2}),
                      G("start", 320, "Now", row="320", setup={"text_scale": 2})]},
        {"id": "chapter-26-selector", "title": "Chapter 26’s token table script",
         "answer": "The token table’s script now looks only inside its own plate.",
         "what_changed": "It selected across the whole page; it now selects inside its plate (call 13).",
         "why": "A page-wide selector could catch another plate’s parts (DR-278 (d)).",
         "recommendation": "Approve the change.", "refs": ["DR-278", "C-131"], "ledger": ["C-131"], "approved_at": "Gate 2",
         "shows": False, "shows_note": "Nothing changes on the screen; the table works as before.",
         "question_for_dustin": False, "pictures": []},
        {"id": "chapter-18-and-shell", "title": "Chapter 18’s code and the shell",
         "answer": ("Fixes that keep approved rules true: the stepper script, printing with every disclosure open, Rule 18.14’s "
                    "file size, the 18.22 plate’s buttons on a phone, the chooser’s list form and the form script’s reach."),
         "what_changed": ("Rule 18.22’s stepper script writes `data-oa-live` and `data-oa-at`, and its step list keeps "
                          "`role=\"list\"`; the shell opens every closed disclosure at print (Rule 18.8’s promise) and holds "
                          "15.20’s status line; Rule 18.14’s example names tokens.css at 105 KB, where it said 95; the 18.22 "
                          "anatomy plate’s buttons no longer break mid-word at 320 to 390 px; Rule 18.3’s chooser gains an "
                          "opt-in list form, `oa-choice-row--list`; chapter 18’s form script selects `form[data-oa-form]` "
                          "only; the shell holds `.tok-v`, unused until a plate asks for it."),
         "why": "Defects in approved rules, and round 4’s interaction (D3-1701, D3-1705, D3-1712; calls 10, 12 and 15).",
         "recommendation": "Approve the changes.", "refs": ["D3-1701", "D3-1705", "D3-1712", "C-113", "C-132"],
         "ledger": ["C-113", "C-132"], "approved_at": "Gate 2 (chapter 18 and the shell)", "shows": True,
         "question_for_dustin": False,
         "pictures": [G("fig-s-18-22-anatomy", 390, "Rule 18.22’s plate on a phone before round 4", role="before", page="v9", row="390"),
                      G("fig-s-18-22-anatomy", 390, "Now", row="390"),
                      G("fig-s-18-14-anatomy", 1440, "Rule 18.14 now: 105 KB", fold=True)]},
        {"id": "source-line-wrap", "title": "Source lines wrap more evenly",
         "answer": "Every HTML source line sets `text-wrap: pretty`, so a line’s last word stops sitting alone.",
         "what_changed": "Line breaks move in 4 of 107 source lines at 1,440 px and 20 at 390 px; no word or drawing moves (D3-1711).",
         "why": "A single word on a source line’s last row reads as a stray.",
         "recommendation": "Approve the change.", "refs": ["D3-1711"], "ledger": [],
         "approved_at": "board 1 and board 2 charts", "shows": False,
         "shows_note": "Shows only as where 4 of 107 source lines break at 1,440 px and 20 at 390 px.",
         "question_for_dustin": False, "pictures": []},
        {"id": "related-chapters", "title": "Second pass: chapter 15 joins three rules’ related chapters",
         "answer": "Rules 14.88 and 14.96, shown at board 2, and Rule 14.135 now list “15 Systems graphics” under Related chapters.",
         "what_changed": ("The second pass gave five entries the related rules the reader panel asked for (RS-5). The page prints "
                          "a rule’s related items as chapters only, so the one visible change is chapter 15 under Related "
                          "chapters on 14.88, 14.96 and 14.135. Printing the rules themselves is held for you below (D3-2278)."),
         "why": "RP-3’s reader, who picks a form and never meets the chapter that maps its process.",
         "recommendation": "Approve the change.", "refs": ["RS-5", "D3-2278"], "ledger": [],
         "approved_at": "board 2 (14.88, 14.96)", "shows": True, "question_for_dustin": False,
         "pictures": [G("rule-14-88", 1440, "Rule 14.88 before the second pass", role="before", page="v12", row="1440", fold=True),
                      G("rule-14-88", 1440, "Rule 14.88 now", row="1440", fold=True)]},
    ]
    changed = {"id": "changed-approved", "title": "Changed approved work",
               "lede": (f"{len(changed_items)} changes reach work you approved at board 1, board 2 or Gate 2, or work a decision "
                        "sent to this board. A script found "
                        f"{len(ch['found'])} change ledger rows that list them for this board, and the decision log and the "
                        "second pass add the rest. Each shows the page before the change beside today’s at true size, or "
                        "says in one line that it does not show."),
               "approval": "one", "items": changed_items}

    # ------------------------------------------------------------------------------------------- panel 3: held for Dustin
    def H(code, **kw):
        row = held_by_code.get(code)
        sec = "Held for Dustin (board 3)"
        if code in ("AX-S3, chapter 11's three step tables and its marks plate", "CR-S4, Rule 15.19's order and a sticky drawing"):
            sec = "Not fixed in the fix pass"
        d = {"register": reg(code, sec), "question_for_dustin": True}
        d.update(kw)
        if row is None and not kw.get("question") and not kw.get("decision"):
            raise SystemExit(f"held row not found by script: {code}")
        return d

    held_items = [
        H("CE-S22", id="CE-S22-words", title="Three pairs of the selection guide’s questions overlap",
          answer="Keep the sixteen family questions as you approved them in the coverage plan.",
          what_changed=("Nothing yet. The civic education reader found three pairs of questions that ask nearly the same thing "
                        "in a newcomer’s words: Shift and swing with Change over time, Composition with Proportion and overlap, "
                        "and Structure with Infographics."),
          why="The questions are the coverage plan’s words (DR-62), which your settled list holds.",
          recommendation=("Keep the questions. Take the next item’s example lines instead, which leave the questions as "
                          "approved."),
          settled={"touches": ["DR-62, the coverage plan"], "respects": "The recommendation changes no question."},
          refs=["DR-62", "CE-S22"],
          pictures=[G("fig-s-14-selection-guide", 1440, "The selection guide today", fold=True)]),
        H("CE-S22, one reader's example under each question", id="CE-S22-examples",
          title="One reader’s example under each of the sixteen questions",
          answer="Add a short example under each question, in a reader’s words, in the finishing pass.",
          what_changed=("Nothing yet. Under each question, before its skip link, one line such as “How did turnout change between "
                        "2020 and 2024?” under Shift and swing, set in the tier words’ type; the editor writes all sixteen, "
                        "and any figure in them is labeled Illustrative."),
          why="Call 6 allowed the lines only if the craft reader agreed, and the craft report does not speak to them.",
          recommendation=("Add the sixteen lines in the finishing pass: about 100 bytes each, no new keyboard stop, and the "
                          "approved questions unchanged."),
          settled={"touches": [], "respects": "The questions stay the coverage plan’s words (DR-62)."},
          refs=["CE-S22", "D3-2131"],
          pictures=[MAKE("Two questions with an example line under each, at 1,440 and 390 px", "editor and board builder",
                         "the editor’s two example lines set under their questions in a scratch copy of the plate")]),
        H("NB-S4", id="NB-S4", title="The lockmark at the end of a chart’s source line",
          answer=("Draw the 16 px lockmark at the right end of the source line on a chart exported alone, and keep the guide’s "
                  "plates as they are."),
          what_changed=("Nothing yet. Rule 08.2’s footer row puts the lockmark “16 px at the right end of a chart’s source line”; "
                        "no kit chart or export carries it, only the credit “Chart: Oath & Action” in words (D3-593)."),
          why="Every chart approved at boards 1 and 2 carries no lockmark, so a change to them all is yours to make.",
          recommendation=("The kit’s exports, the PNG and SVG a partner or a story takes away, draw the 16 px lockmark at the "
                          "source line’s right end; the on-page plates stay as approved, since a view shows the lockmark once "
                          "(Rule 08.2); Rule 08.2’s row adds “on a chart exported alone”."),
          settled={"touches": ["Rule 08.2 (Gate 2)", "the charts approved at boards 1 and 2"],
                   "respects": "No chart on the page changes; the chart system’s plates are as approved (DR-52)."},
          refs=["NB-S4", "D3-593", "DR-211"],
          pictures=[MAKE("A kit export with the 16 px lockmark at its source line’s end, beside today’s export", "engineer",
                         "one spec built with and without the mark in a scratch kit")]),
        H("S14 line in chapters 02 and 13", id="S14-line-02-13", title="S14’s source line where chapters 02 and 13 print it",
          answer="Print S14’s new source line in the two places chapters 02 and 13 quote it.",
          what_changed=("S14’s own source line now names the September 2026 release (D3-2144); Rules 02.22 and 13.6 print the "
                        "older line as their example."),
          why="Chapters 02 and 13 are approved.",
          recommendation="Update both copies to S14’s line as it prints today; the editor’s words are ready.",
          settled={"touches": ["chapter 02’s plate 02.22 (an example line, not a writing rule)", "chapter 13 (DR-237)"],
                   "respects": "Chapter 02’s writing rules do not change."},
          refs=["D3-2144"],
          pictures=[G("fig-s-02-22-correct", 1440, "Rule 02.22’s example today, the older line", row="a"),
                    G("fig-s-13-6-correct", 1440, "Rule 13.6’s example today, the older line", row="a"),
                    G("oac-s-14-s14", 1440, "S14’s own line today", spec="S14", fold=True)]),
        H("RP-14 and R5-G (the creative director's accessibility reason)", id="RP-14-headings",
          title="Headings in the selection guide and chapter 14’s group heads",
          answer=("Make “Choose a chart” a level 3 heading and each question a level 4 heading, and give chapter 14’s 18 group "
                  "heads heading levels in the same pass."),
          what_changed=("Nothing yet. A reader who moves by headings passes the selection guide’s links without meeting a "
                        "heading, as they pass chapter 14’s group heads; a reader who moves by lists meets 16 lists, each named "
                        "by its question."),
          why="The main session declined it in the fix pass (call 17, D3-2142), since a plate holds no heading; the maker put it to you as a choice.",
          recommendation=("Yes. The selection guide sits in the chapter’s head with no frame, so its questions work as the "
                          "chapter’s own headings; the guide check allows headings in that one plate."),
          settled={"touches": [], "respects": "No settled element changes; the words stay the coverage plan’s."},
          refs=["RP-14", "R5-G", "D3-2142", "D3-2074"], pictures=[]),
        H("S59's \"4.1\" label against its line (the craft reader's question 1)", id="S59-label", spec="S59", rule="14.77",
          title="S59’s “4.1” label against its line",
          answer="Move S59’s “4.1” label clear of its line by a spec key, as S14’s was moved.",
          what_changed="Nothing yet. At 390 and 558 px the label sits against a line of the fan chart.",
          why="S59 is approved (DR-263); the fix pass moved only S14’s label (call 18).",
          recommendation=("Move it, by a spec key alone. Turn the kit’s edge guard on for every form only after a sweep lists "
                          "each approved chart the guard would move, for you to see first."),
          settled={"touches": ["S59 (DR-263)"], "respects": "The data, scale and words of S59 stay; only the label’s place moves."},
          refs=["DR-263", "D3-2143", "DD-E7"],
          pictures=[G("oac-s-14-s59", 390, "Today, on a 390 px phone", spec="S59", row="390"),
                    MAKE("With the label moved, on a 390 px phone", "engineer", "S59 built with the spec key in a scratch kit", row="390", w=390),
                    G("oac-s-14-s59", 1024, "Today, in the 558 px column of a 1,024 px window", spec="S59", row="1024", fold=True)]),
        H("AX question 1, the masthead at 360 to 372 px", id="masthead-360", title="The masthead at 360 to 375 px",
          answer="Move the 16 px wordmark master’s switch to 376 px, after the design director has looked at it there.",
          what_changed=("Nothing yet. At 360 to 372 px the 24 px wordmark returns and the menu button drops to a second line, "
                        "so the masthead takes 132 to 133 px, about a fifth of a 640 px phone screen."),
          why="It changes where Rule 03.6’s two approved masters meet; a change to identity needs your named approval (gate rule 4).",
          recommendation="Yes, with the design director’s look at 360 to 375 px first; the accessibility lead recommends it.",
          settled={"touches": ["Rule 03.6’s wordmark masters (Gate 2)"],
                   "respects": "Neither master’s drawing changes; only the width where one gives way to the other."},
          refs=["AX question 1", "D3-2135"],
          pictures=[G("header.masthead", 360, "Today at 360 px", row="360"),
                    MAKE("At 360 px with the 16 px master", "design director", "the shell with the switch at 23.5em in scratch", row="360", w=360),
                    G("header.masthead", 375, "Today at 375 px", row="375"),
                    MAKE("At 375 px with the 16 px master", "design director", "as above", row="375", w=375)]),
        H("Call 15's keyline on the approved red targets (CR-S1's last part)", id="red-target-keyline",
          title="The keyline inside the red target: two settled rules disagree",
          answer=("Two things you settled point different ways, so only you can choose. Rule 05.5 says a red mark that "
                  "carries meaning on Newsprint takes a 1 px Charcoal keyline, since Pillar Red measures 2.96 to 1 there. "
                  "The atlas visual system (DR-36) draws its red target with no keyline. Rules 15.20 and 14.144 now draw the "
                  "keyline; Rules 15.11, 15.12 and 15.16 do not."),
          what_changed=("Call 15 (D3-2140) gave the chooser plates, Rules 15.20 and 14.144, a 1 px keyline inside a chosen "
                        "pill’s red ring and a 1 px ink edge on the red arrowhead. Rules 15.11, 15.12 and 15.16, approved at "
                        "board 2, keep the atlas’s red target with no keyline, so on Newsprint their red stands at about "
                        "2.95 to 1, under the 3 to 1 that Rule 05.5 and WCAG 2.2’s 1.4.11 ask of a mark a reader needs. "
                        "Today one red target has two looks."),
          why=("Rule 05.5 (chapter 05, approved) and the atlas visual system’s red target (DR-36) are both on your settled "
               "list, and on these five plates they cannot both hold."),
          recommendation=("Keep the atlas’s red target as you settled it (DR-36): the keyline and the ink edge come off "
                          "Rules 15.20 and 14.144, so one red target has one look again. The cost: on Newsprint the red ring "
                          "stands at about 2.95 to 1 on all five plates, under the 3 to 1 that Rule 05.5 and WCAG 2.2’s "
                          "1.4.11 ask (the accessibility reader’s AX-S5). The keyline everywhere would meet Rule 05.5 and "
                          "keep the red, the ring and the pill as the atlas draws them, but it changes a settled mark, so it "
                          "takes your own word: reply “Keyline everywhere”."),
          settled={"touches": ["Rule 05.5’s keyline on a red mark on Newsprint (chapter 05, approved)",
                               "Rule 12.5’s red target, a mark of the atlas visual system (DR-36)",
                               "Rules 15.11, 15.12 and 15.16 (board 2)"],
                   "respects": ("The recommendation changes nothing you settled: it returns Rules 15.20 and 14.144 to the "
                                "atlas’s drawing. The keyline everywhere happens only on your named reply.")},
          refs=["D3-2140", "CR-S1"],
          pictures=[G("fig-s-15-11-correct", 1440, "Rule 15.11 today", row="a"),
                    G("fig-s-15-20-correct", 1440, "Rule 15.20 today, with the keyline", row="a"),
                    MAKE("Rule 15.11 with the keyline", "systems designer", "the `keyline` flag set in a scratch run of the chapter 15 build"),
                    G("fig-s-15-12-correct", 1440, "Rule 15.12 today", fold=True),
                    G("fig-s-15-16-correct", 1440, "Rule 15.16 today", fold=True)]),
        H("CR-S17, chapter 13's chips and Rule 18.24's code chip", id="CR-S17-chips",
          title="Chapter 13’s chips and Rule 18.24’s code chip",
          answer="Drop tabular figures from the chip ID in chapter 13 and in Rule 18.24, as chapter 15’s chips already do.",
          what_changed=("Nothing yet. Tabular figures set Inter’s hyphen at a figure’s width, so “R-04” reads “R - 04”, the "
                        "hyphen 8.42 px wide against 6.06."),
          why="Both are approved work outside this pass’s rows.",
          recommendation="Yes, with the anatomy key’s words changed to match.",
          settled={"touches": ["chapter 13 (DR-237)", "Rule 18.24 (Gate 2)"], "respects": "The chip’s drawing stays."},
          refs=["CR-S17", "D3-2152"],
          pictures=[G("fig-s-13-5-correct", 1440, "Rule 13.5 today", row="a"), G("fig-s-18-24-anatomy", 1440, "Rule 18.24 today", row="a")]),
        H("DF-10, S71's \"read\"", id="S71-retrieved", spec="S71", rule="14.101", title="S71 says “read” where every other date says “retrieved”",
          answer="Print “retrieved” on S71’s route pages, as chapter 15’s plates do.",
          what_changed="Nothing yet. S71 prints “read” for the date a source was taken; chapters 11, 14 and 15 say “retrieved” (ruling R7).",
          why="S71 is approved at board 2.", recommendation="Yes.",
          settled={"touches": ["S71 (board 2)"], "respects": "One word in the source dates; no figure moves."},
          refs=["DF-10", "R7", "Rule 13.6"],
          pictures=[G("oac-s-14-s71", 1440, "S71 today", spec="S71")]),
        H("Rule 14.6's color word", id="14.6-ink", rule="14.6", title="Rule 14.6 names a color that changes with the ground",
          answer="Say “the text’s ink at the subject weight” in Rule 14.6, where it says “Charcoal at the subject weight”.",
          what_changed="Nothing yet. On a Charcoal ground the text’s ink is light, so “Charcoal” names the wrong color there.",
          why="Rules 14.1 to 14.14 changed only for DF-12 and DF-13 in the fix pass.", recommendation="Yes.",
          settled={"touches": ["Rule 14.6 (board 2)"], "respects": "Words only."}, refs=["DF-5"], pictures=[]),
        H("Pillar Red's ratio, two figures for one measure", id="pillar-red-ratio",
          title="Pillar Red’s contrast printed two ways",
          answer="Keep chapter 05 as approved, and let the palette plate name its rounding beside each figure.",
          what_changed=("Nothing yet. The palette plate prints 2.95 and 4.16 to 1, rounded down (call 9); chapter 05 prints 2.96 "
                        "and 4.17, rounded to the nearest, from the same measured 2.9568."),
          why="Chapter 05 is approved, and each figure is true to two places.",
          recommendation=("The palette plate names its rounding beside the figure, as its method line already says; chapter 05 "
                          "stays as you approved it."),
          settled={"touches": ["chapter 05 (Gate 2)"], "respects": "Chapter 05 does not change."},
          refs=["D3-1929"],
          pictures=[G("fig-s-14-palette-spec", 1440, "The palette plate today", fold=True), G("fig-s-05-3-correct", 1440, "Rule 05.3 today", fold=True)]),
        H("Rule 15.15's read-aloud line", id="15.15-read-aloud", rule="15.15", title="Rule 15.15’s read-aloud line",
          answer="Read the loop as “The quality of public services rises ...”, which keeps the variable’s own title.",
          what_changed="Nothing yet. The line reads “More quality of public services ... and back to less quality of public services”.",
          why=("Rule 15.15 is approved, and “more” and “less” before a quality noun is the read-aloud function’s rule for every "
               "loop, so a change reaches every read-aloud line of that kind."),
          recommendation=("Yes, the “The quality of ... rises” form, which keeps each variable’s own title as DR-265 asks; the "
                          "editor lists every read-aloud line it changes before the build."),
          settled={"touches": ["Rule 15.15 (board 2)", "DR-265"], "respects": "The variable keeps its own title."},
          refs=["DR-265"], pictures=[]),
        H("CR-S19, the evidence chip's layout", id="CR-S19-chip", title="The evidence chip when its grade line wraps",
          answer=("Set the grade line beside the chip on S89, S91 and S94, which are not yet approved, and keep today’s layout "
                  "on every approved chart."),
          what_changed=("The layout landed opt-in as `\"evidence_layout\": \"beside\"`; no spec sets it. Where a grade line does not "
                        "fit beside the chip it drops under the chip alone, so the heads of S89, S91 and S94 read in a second layout."),
          why="As the kit’s default it moves every signed-off chart whose grade line wraps at some width, which no browser has measured.",
          recommendation=("Take the opt-in on S89, S91 and S94 in the finishing pass; leave the default, so no approved chart "
                          "moves, unless a sweep at every width lists the charts it would move for you to see."),
          settled={"touches": ["the chart system’s header (DR-52)"], "respects": "No approved chart moves."},
          refs=["CR-S19"],
          pictures=[G("oac-s-14-s91", 390, "S91 today on a phone", spec="S91", row="390"),
                    MAKE("S91 with the grade line beside the chip", "engineer", "S91 built with the opt-in in a scratch kit", row="390", w=390)]),
        H("Rule 15.22's sunset and repeal examples (the creative director's risk)", id="15.22-examples", rule="15.22",
          title="Why Rule 15.22 shows these two laws",
          answer="State the rule that chose each law in the plate’s note.",
          what_changed=("Nothing yet. The sunset example is Public Law 115-97, section 11022, and the later change is Public Law "
                        "119-21, section 70104; the plate names each law but not the rule that chose it."),
          why="Raised by the creative director as a risk for you to weigh (RP-11).",
          recommendation=("State the rule in the note, for example the most recent sunset and the most recent repeal the research "
                          "lead found, with the date searched. The laws stay as the rule finds them; none is swapped to even the sides (DR-93)."),
          settled={"touches": [], "respects": "One standard of evidence (DR-93); every line read from both sides (DR-124)."},
          refs=["RP-11", "DR-93", "DR-124"],
          pictures=[G("fig-s-15-22-correct", 1440, "Rule 15.22 today", fold=True)]),
        H("Q-PR1, Phase 4's weight", id="Q-PR1", title="Room on the page for Phase 4",
          answer="Size each Phase 4 chapter from its nearest built chapter before Phase 4 starts, and decide then what ships as a download; cut nothing now.",
          what_changed=(f"Nothing. The projection gives Phase 4’s seven chapters {p4['assumed_each']:,} bytes each, against "
                        f"{p4['break_even_each_16mb']:,} each to stay under 16 MB and {p4['break_even_each_15_5mb']:,} under the "
                        f"15.5 MB warning; today’s {p4['built_chapters_counted']} built chapters other than 14 weigh "
                        f"{p4['built_chapters_median']:,} at the median and {p4['built_chapters_mean']:,} on average."),
          why="The production reader put it to you; DR-271 keeps the page’s 16 MB as the one fixed limit.",
          recommendation="As suggested: the engineer sizes each chapter first; nothing is cut now (DR-271).",
          settled={"touches": [], "respects": "DR-271"},
          facts=[{"label": "Projected page", "value": f"{rep['weight']['projection']['projected_bytes']:,} bytes"},
                 {"label": "Page today", "value": f"{rep['bytes']:,} bytes"}],
          refs=["Q-PR1", "DR-271", "ST-S10"], pictures=[]),
        H("AX-S3, chapter 11's three step tables and its marks plate", id="AX-S3-tables",
          title="Chapter 11’s step tables and marks plate: an alt that repeats the table",
          answer=("Shorten the alts of the bill’s step table and the marks plate to their head sentence, and give each table a "
                  "caption with the same sentence."),
          what_changed=("Nothing yet. Each table’s alt repeats every step’s words and law (1,509 characters against a 1,373-"
                        "character table), and no table has a caption, so a list of tables names each one only “table”."),
          why="`s-11-steps` and `s-11-marks-drawn` are approved at Gate 2; the two new tables are not.",
          recommendation="Yes, with the caption visually hidden or set as the plate’s label, so nothing on the screen changes.",
          settled={"touches": ["chapter 11 (Gate 2)"], "respects": "Nothing changes on the screen."},
          refs=["AX-S3"], pictures=[]),
        H("CR-S4, Rule 15.19's order and a sticky drawing", id="CR-S4-sticky", rule="15.19",
          title="A drawing that stays in view while a reader steps through Rule 15.19",
          answer="Leave the drawing as it is for now; the second pass fixed the order, and the sticky frame waits for the shell.",
          what_changed=("The second pass set Rule 15.19’s parts in Rule 14.143’s order (RS-7). At a desk the drawing still ends "
                        "about 340 px above Play, so its column stands empty while a reader steps through the list."),
          why="Every plate frame scrolls sideways today, so a sticky part sticks to its frame; changing that reaches every frame’s clipping and keyboard scrolling.",
          recommendation="Hold the sticky frame for the shell’s next pass, when every frame can be measured at once.",
          settled={"touches": [], "respects": "No approved plate changes."}, refs=["CR-S4", "RS-7"],
          pictures=[G("fig-s-15-19-correct", 1440, "Rule 15.19 today")]),
        {"id": "related-rules", "title": "Print each chapter 14 rule’s related rules as links",
         "decision": {"code": "D3-2278", "file": "work/ledger/20261020_Decision-Log.md"},
         "answer": "Print a “Related rules” line of links beside Related chapters on chapter 14’s entries.",
         "what_changed": ("The second pass gave entries 14.32, 14.74, 14.88, 14.96 and 14.135 the related rules the reader panel "
                          "asked for (RS-5), but the page prints a rule’s related items only as chapters, so no rule number reaches "
                          "a reader."),
         "why": "It changes the foot of every approved chapter 14 entry that carries related rules.",
         "recommendation": ("Yes. The data is in every entry already, so it is one build change; the engineer measures the bytes "
                            "before it is built."),
         "facts": [{"label": "Rules that would print the line", "value": "138 of chapter 14’s 144"},
                   {"label": "Links", "value": "363: 284 inside chapter 14, 79 to chapters 01, 05, 06, 11, 12, 13, 15, 18 and 19"},
                   {"label": "Rules with a Related chapters line today", "value": "38"},
                   {"label": "Estimated weight", "value": "About 37,000 bytes, by one link per related rule in the page’s link form; an estimate, not measured"}],
         "settled": {"touches": ["chapter 14’s entries (board 2)"], "respects": "No rule’s words change."},
         "refs": ["D3-2278", "RS-5", "RP-3"], "question_for_dustin": True,
         "pictures": [G("rule-14-32", 1440, "Rule 14.32’s foot today", row="a"),
                      MAKE("Rule 14.32’s foot with a Related rules line", "engineer", "a scratch build that prints related_rules", row="a")]},
        {"id": "Q-12", "title": "Trademark clearance for the name, the monogram and the ampersand",
         "question": "Q-12",
         "answer": "Have a trademark attorney run clearance on OATH & ACTION, the monogram and the standalone ampersand before launch.",
         "what_changed": "Nothing. The question has stood since Gate 1; the guide flags the need and assumes no filing.",
         "why": held["q_12"]["why"] if held["q_12"] else "",
         "recommendation": "Yes, before Phase 5’s release; the guide keeps its flag until the attorney reports. The research lead adds the facts.",
         "settled": {"touches": [], "respects": "No design changes."},
         "refs": ["Q-12"], "question_for_dustin": True, "pictures": [],
         "source": "work/handoffs/phase-3/20261120_Board-3-Research-Notes.md"},
    ]
    held_panel = {"id": "held", "title": "Held for you",
                  "lede": (f"{held['rows_in_section']} rows of the deferred fixes register stand under “Held for Dustin (board 3)”, "
                           f"and {len(held['held_elsewhere'])} more rows elsewhere in it name board 3. With RS-5’s visible half "
                           "from the second pass and Q-12, each is a choice only you can make."),
                  "approval": "each", "items": held_items}

    # ------------------------------------------------------------------------------------------------ panel 4: V7.1 row
    v71 = {"id": "atlas-v7-1", "title": "The proposed atlas V7.1 row",
           "lede": "One finding from round 4 for the atlas editor’s list, which needs your word to join it (D3-1861).",
           "approval": "one",
           "items": [{"id": "routes-who", "title": "Each reform route’s “who” field holds three kinds of thing",
                      "answer": "Add a row to the V7.1 list: keep `who` for who acts, and move an instrument or an action to the route’s note or a new field.",
                      "what_changed": (f"Nothing in the atlas. Of its {who['entries']} route entries ({who['distinct']} values), many "
                                       "name an actor (“Congress” 12, “Voters” 9, “Legislatures” 8), others an instrument (“Statute” 5, "
                                       f"“Amendment” 3), and {len(who['verb_led'])} an action that opens with a verb, such as R-03’s "
                                       "federal statute route, “Repeal the single-member mandate (2 U.S.C. 2c) and require ranked "
                                       "multi-winner counting”. Rule 15.20’s correct plate prints that line on R-03’s route card."),
                      "why": "A new row on the V7.1 list needs your word (D3-1861); the guide never changes the V7 model.",
                      "recommendation": "Add the row, as board 2’s items were added (DR-264).",
                      "new_to_v7_1_list": True,
                      "counts": [{"label": "Route entries", "value": who["entries"], "from": "atlas-v7-data.json, reforms[].routes[]"},
                                 {"label": "Distinct values", "value": who["distinct"], "from": "the same"},
                                 {"label": "Values that open with a verb", "value": len(who["verb_led"]), "from": "the same"}],
                      "verb_led": who["verb_led"],
                      "top": who["top"],
                      "source": "work/handoffs/phase-3/20261113_Round-4-Research-Notes.md#v71-items-raised-in-round-4",
                      "refs": ["D3-1861", "DR-264"], "question_for_dustin": True,
                      "pictures": [G("fig-s-15-20-correct", 1440, "Rule 15.20 today: R-03’s federal statute route prints an action where it means who acts", fold=True)]}]}

    panels = [trackers, changed, held_panel, v71]
    replies, n = [], 0
    for it in trackers["items"]:
        n += 1
        it["reply_number"] = n
        replies.append({"n": n, "panel": "trackers", "id": it["id"], "line": f"{it['title']}: approve the six names.",
                        "recommendation": it["recommendation"], "item": it["id"]})
    n += 1
    changed["reply_number"] = n
    replies.append({"n": n, "panel": "changed-approved", "id": None,
                    "line": f"The {len(changed_items)} changes to approved work, as listed.", "recommendation": "Approve them as listed.",
                    "item": "changed-approved"})
    for it in held_items:
        n += 1
        it["reply_number"] = n
        replies.append({"n": n, "panel": "held", "id": it["id"], "line": it["title"] + ".", "recommendation": it["recommendation"],
                        "item": it["id"]})
    n += 1
    v71["reply_number"] = n
    replies.append({"n": n, "panel": "atlas-v7-1", "id": "routes-who", "line": v71["items"][0]["title"] + ".",
                    "recommendation": v71["items"][0]["recommendation"], "item": "routes-who"})

    r9_out = {k: v for k, v in r9.items()}
    r9_out["rows"] = [{k: x[k] for k in ("where", "rule", "kind", "domain", "states", "round")} for x in r9["rows"]]
    r9_out["note"] = (f"Chapter 14 as finished holds {r9['total_examples']} examples: {r9['make_up']['rule_plates']} on rule "
                      f"plates, {r9['make_up']['kit_charts']} kit charts and {r9['make_up']['charts_in_full']} in the three "
                      f"charts in full; its {r9['make_up']['sketches_not_counted']} sketches draw invented data and count none. "
                      f"The largest domain, {r9['by_domain'][0]['title']}, supplies {r9['by_domain'][0]['count']} against a "
                      f"limit of {r9['limit_domain']}, and no state supplies more than {r9['by_state'][0]['count']} against "
                      f"{r9['limit_state']}. The recount agrees with the generator’s log row for row.")
    r9_out["caption"] = f"Chapter 14’s examples by topic and by state, of {r9['total_examples']}, rounds 0 to 5."
    dr_out = dict(dr)
    dr_out["note"] = (f"{dr['count']} of the {r9['total_examples']} examples draw election or voting data: {dr['election_domain']} "
                      f"in elections and representation and {dr['voting_under_taking_part']} on reported voting. Every new form "
                      f"that keeps election data passes D3-689’s test ({dr['new_forms_pass']} pass, {dr['new_forms_fail']} fail). "
                      "Since board 2 one example joined: Loop R10 on Rule 14.143, one of Gate 2’s three named complex examples.")
    dr_out["caption"] = f"Examples that draw election or voting data, of the {r9['total_examples']} in chapter 14."
    doc = {
        "schema": "board-3-decisions/1",
        "state": a.state,
        "updated_utc": now,
        "written_by": "data lead",
        "words_owner": "editor",
        "reply_line": "To answer, reply “As recommended”, or name the item and your change.",
        "pages": PAGES,
        "panels": panels,
        "changed_found": {"script": SCRIPT, "requested_home": HOME, "run_utc": now,
                          **{k: v for k, v in ch.items()},
                          "second_pass": ["RS-1 (Rule 11.12’s alts)", "RS-5 (related chapters on 14.88 and 14.96)",
                                          "CR-S1’s remainder (Rule 15.20’s failure plate)", "CR-S23 (Rule 14.144’s phone line-up)"],
                          "also_from_decision_log": ["D3-1711", "D3-2127", "D3-2140", "D3-2143", "D3-2144"]},
        "held_found": {k: v for k, v in held.items()},
        "counts": {"script": SCRIPT, "requested_home": HOME, "made_by": "make_board_3_decisions.py, beside the script", "run_utc": now,
                   "rule_01_9": r9_out, "dr_229": dr_out},
        "replies": replies,
    }
    if a.state == "signed off":
        doc["signed_off_utc"] = now
        doc["signed_off_note"] = ("Signed off by the data lead: every count read by script (board_3_data_lead_counts.py) from the "
                                  "repository and from the strict build report named in `build_report`; every picture's element "
                                  "found in the page it names; the words are a first draft, which the editor owns from here.")
        doc["build_report"] = {"file": a.report, "bytes": rep["bytes"], "warnings": len(rep["warnings"]),
                               "pictures_hidden": pics["hidden"], "pictures_open": pics["open"]}
    if a.counts_only:
        old = json.loads(OUT.read_text())
        for k in ("rule_01_9", "dr_229"):   # a note and a caption are the editor's words; a counts run keeps them
            for w in ("note", "caption"):
                if old.get("counts", {}).get(k, {}).get(w):
                    doc["counts"][k][w] = old["counts"][k][w]
        old["counts"], old["updated_utc"] = doc["counts"], now
        doc = old
    s = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    if "—" in s:
        raise SystemExit("an em dash in the decision file")
    OUT.write_text(s)
    print(f"wrote {OUT.relative_to(ROOT)}: {len(s.encode()):,} bytes; panels {[p['id'] for p in panels]}; "
          f"items {[len(p['items']) for p in panels]}; replies {len(replies)}")


def counts_steps(name):
    import ast
    src = (ROOT / "work/build/scripts/phase-2/apply_systems_ch11.py").read_text()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == name for t in node.targets):
            return ast.literal_eval(node.value)
    raise SystemExit(f"{name} not found")


if __name__ == "__main__":
    main()
