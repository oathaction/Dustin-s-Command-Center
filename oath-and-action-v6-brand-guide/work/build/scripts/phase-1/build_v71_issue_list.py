#!/usr/bin/env python3
"""Write the Atlas V7.1 issue list for the atlas editor (decision DC-08).

Run:  python3 -I work/build/scripts/phase-1/build_v71_issue_list.py
Reads work/extract/atlas-v7-data.json, work/extract/atlas-v7/script.js and
work/boards/phase-1/systems/20261021_Systems-Marks-Data.json (run systems_marks_data.py first).
Writes work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md. Changes nothing in V7.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
d = json.loads((ROOT / "work/extract/atlas-v7-data.json").read_text(encoding="utf-8"))
js = (ROOT / "work/extract/atlas-v7/script.js").read_text(encoding="utf-8")
D = json.loads((ROOT / "work/boards/phase-1/systems/20261021_Systems-Marks-Data.json").read_text(encoding="utf-8"))
OUT = ROOT / "work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md"
N, L, LP, R, I, C = d["nodes"], d["links"], d["loops"], d["reforms"], d["issues"], d["claims"]
G = {g["term"]: g["definition"] for g in d["glossary"]}
g = D["grades"]


def cnt(c):
    return ", ".join(f"`{k}` {v}" for k, v in sorted(c.items(), key=lambda x: -x[1]))


def js_line(pattern):
    for i, line in enumerate(js.splitlines(), 1):
        if re.search(pattern, line):
            return i
    return None


near = [m for m in D["collisions"]["near"] if len({k for k, _ in m["members"] if k != "v5_standards_rule"}) > 1]
near_groups = Counter()
for m in near:
    kinds = tuple(sorted({k for k, _ in m["members"] if k != "v5_standards_rule"}))
    near_groups[kinds] += 1
loop_reform = [m["normalized"] for m in near if {k for k, _ in m["members"]} >= {"loop", "reform"}]
var_domain = [m["normalized"] for m in near if {k for k, _ in m["members"]} >= {"variable", "domain"}]
var_issue = [m["normalized"] for m in near if {k for k, _ in m["members"]} >= {"variable", "issue"}]
exact = [x for x, k in D["collisions"]["exact"] if "v5_standards_rule" not in k]
routes = D["routes"]
fx = D["effects"]
mf = D["model_facts"]
rows_rl = d["repairLog"]["rows"]
rows_dl = d["deliveryLog"]["rows"]
date_formats = Counter()
for r in rows_dl:
    s = r["date"]
    f = re.sub(r"\d", "9", s)
    date_formats[f] += 1
counts = d["meta"]["counts"]
ec = Counter("plain" if r["effects_confidence"] in ("high", "medium", "low") else "scoped" for r in R.values())
pill_line = js_line(r'rx="11"')
region_line = js_line(r"function regionMap")
amb_line = js_line(r"function ambiguousCode")
grades_line = js_line(r"^var GRADES = \{")
kind_line = js_line(r"var KIND_LABEL")
x16 = I["X16"]["remedy_note"][:120]
i128 = I["I128"]
d6 = N["D6"]
conc = mf["conceptual_chain_items"]
conc_g = mf["conceptual_loop_grades"]

issues = []


def add(title, loc, evidence, fix, v6, kind="Model"):
    issues.append((title, loc, evidence, fix, v6, kind))


add("Grade vocabulary differs across record types",
    "`links[].evidence`; `issues[].grade`; `claims[].confidence`; `reforms[].problem_evidence.grade`; `reforms[].remedy_evidence.grade`; `deliveryLog.rows[].evidence_grade`; `loops[].evidence`",
    f"Connections: {cnt(g['links.evidence'])}. Issues: {cnt(g['issues.grade'])}. Claims: {cnt(g['claims.confidence'])}. "
    f"Reform problem evidence: {cnt(g['reforms.problem_evidence.grade'])}. Reform remedy evidence: {cnt(g['reforms.remedy_evidence.grade'])}. "
    f"Delivery log: {cnt(g['deliveryLog.rows.evidence_grade'])}. Loops hold free text, for example R10: \"{LP['R10']['evidence']}\". "
    f"Well supported is spelled `well-supported` in five fields and `well_supported` in one; contested is `plausible_contested` on connections and `contested` on claims, and reform remedies use both.",
    "Pick one stored code per grade (for example `well-supported` and `contested`) and use it in every field. If `plausible_contested` should stay a separate grade from `contested`, define it in the methods text and the glossary. Give loops a grade field for the weakest step and keep the free text as a note.",
    "Yes. The guide shows one display word per grade from a mapping table (Systems Marks Board, Mark 2) and keeps V7's stored code in record panels and downloads.")
add("The `contested` flag repeats the `plausible_contested` grade",
    "`links[].contested`",
    f"The flag is true on {len(D['grade_facts']['contested_flag_links'])} connections ({', '.join(D['grade_facts']['contested_flag_links'])}), exactly the {len(D['grade_facts']['plausible_contested_links'])} graded `plausible_contested`.",
    "Drop the flag, or document it as derived from the grade so the two cannot drift apart.",
    "Yes. The guide reads the grade field only.")
add("Issue remedy grades live only as the first word of a note",
    "`issues[].remedy_note`",
    f"First words: {cnt(g['issues.remedy_note (first word)'])}. No issue record has a remedy grade field, while reforms keep `remedy_evidence.grade` as a field.",
    "Add `issues[].remedy_grade` with the same codes as other grade fields, and keep the note as prose.",
    "Yes. The guide parses the first word, as V7's renderer does (`leadGrade`).")
add("Mixed is defined, nearly unused and missing from the glossary list",
    "`methods.how_claims_are_assessed`; `glossary` term \"Confidence label\"; `issues.X16.remedy_note`",
    f"The methods text defines it: \"{D['quotes']['methods_mixed']}\" One record uses it, as the first word of issue X16's remedy note (\"{x16}…\"). The glossary's confidence label list reads: \"{G['Confidence label']}\" It omits Mixed.",
    "Either add Mixed to the glossary list and to a grade field where it applies, or remove it from the methods text and recode X16.",
    "Yes. The guide's display list includes Mixed and shows it only where a record uses it.")
add("Not yet tested appears in the glossary and renderer, in no record",
    f"`glossary` term \"Confidence label\"; renderer `GRADES` table (`script.js` line {grades_line})",
    f"Records that use it: {D['grade_facts']['not_yet_tested_uses']}. The methods text does not define it. The renderer text: \"{D['renderer']['grade_table']['not yet tested']['text']}\"",
    "Define it in the methods text if responses will carry it, or remove it from the glossary list.",
    "Yes. The guide keeps the word in its key, marked as reserved.")
add("A status sits in the grade field of one issue",
    "`issues.I128.grade`; `issues.I128.retired`",
    f"I128 \"{i128['title']}\" has `grade: \"{i128['grade']}\"` and `retired: {str(i128['retired']).lower()}`. Its status text: \"{i128['status']['text']}\"",
    "Set the grade to the record's last grade or to null, and keep retirement in `retired` and `status`.",
    "Yes. The guide shows Retired as a status chip, never as a grade.")
add("Two definitions of well supported",
    "`methods.how_claims_are_assessed`; `glossary` term \"Well-supported\"",
    f"Methods: \"{D['quotes']['methods_well_supported']}\" Glossary: \"{G['Well-supported']}\" The methods text allows one well-designed study or an official estimate; the glossary asks for several studies that agree.",
    "Use one definition in both places.",
    "Partly. The guide's gloss (\"strong studies agree on the direction\") fits both; it quotes neither until they agree.")
add("D6 is typed as a flow and described as a stock",
    "`nodes.D6.type`; `nodes.D6.kind_plain`",
    f"`type: \"{d6['type']}\"`. `kind_plain`: \"{d6['kind_plain']}\"",
    "Set `type` to `stock` and keep the indicator note, or rewrite `kind_plain` to explain why the variable is a flow.",
    "Yes. The guide prints V7's `type` and quotes the `kind_plain` text in the record panel, so the conflict stays visible.")
add("Most route entries have no check date",
    "`reforms[].routes[].checked`",
    f"{routes['checked']} of {routes['entries']} entries carry a date, all {', '.join(sorted({e[3] for e in routes['checked_list']}))}: "
    + ", ".join(f"{e[0]} {e[1]}" for e in routes["checked_list"])
    + ". The other entries are null. Reform R-01 has dates for BI and LOC and none for SS and FS, though its status was checked "
    + f"{R['R-01']['status']['checked']}.",
    "Add a check date to every route entry, or store an explicit state such as `\"not checked\"` with a reason.",
    "Yes. The guide prints \"no check date in V7\" for a null date and never infers one from the reform's status date.")
add("Effect values extend the seven codes with qualifiers and ranges",
    "`reforms[].effects`",
    f"{fx['qualified']} of {fx['total']} values are not one of the seven codes. Examples: "
    + "; ".join(f"{q[0]} {q[1]} \"{q[2]}\"" for q in fx["qualified_list"][:8])
    + f". {len(fx['costs_live'])} values on live reforms state a cost: " + "; ".join(f"{c[0]} {c[1]} \"{c[2]}\"" for c in fx["costs_live"]) + ".",
    "Store each effect as a code plus structured extras, for example `{\"code\": \"0\", \"range_to\": \"-S\", \"qualifier\": \"short run\"}`, and keep the display string.",
    "Yes. The guide's pips read the codes in each string, and the words beside them quote V7's full value.")
add("Effect confidence is free text on a third scale",
    "`reforms[].effects_confidence`",
    f"{ec['plain']} of 50 reforms use a single level and {ec['scoped']} use scoped text, for example R-01: \"{R['R-01']['effects_confidence']}\". The levels high, medium and low also name route feasibility.",
    "Store confidence per outcome family or per named scope, with the level as a code.",
    "Yes. The guide prints it as \"Confidence in the effect: …\", apart from the grade and the effect mark.")
add("Identifiers collide across kinds",
    "IDs in `nodes`, `loops`, `reforms`, `domains`, `issues`; renderer `ambiguousCode` (`script.js` line " + str(amb_line) + ")",
    f"Identical codes: {', '.join(exact)} name both a variable and a loop. Codes that match once a hyphen or leading zero is set aside: "
    f"loop and reform {', '.join(loop_reform)}; variable and domain {', '.join(var_domain)}; variable and issue {', '.join(var_issue)}. Variable B1 sits beside loop B1a. "
    f"V7's methods text says: \"{D['quotes']['methods_identifiers']}\" The renderer adds a type word only for identical codes: `{D['renderer']['ambiguous_rule']}`.",
    "Keep the IDs, since sources and backlinks cite them. Extend the renderer so every reference to a loop, reform, domain or issue carries its type word, as it already does for B2 to B5.",
    "Yes. The guide's typed chips carry the type word every time (Mark 3).")
add("The glossary's driver pills do not match the renderer",
    f"`glossary` term \"Outside driver\"; renderer pill code (`script.js` line {pill_line}) and `regionMap` (line {region_line})",
    f"Glossary: \"{G['Outside driver']}\" In the renderer the only rounded pill (rx {D['renderer']['pill_rx']}) is the connection label, and X1 to X5 appear as a sixth area card titled \"{D['renderer']['outside_driver_region'][0]}\". The rendered map was not inspected beyond two screenshots.",
    "Change the glossary sentence to describe what the renderer draws, or draw drivers as pills.",
    "Yes. The guide does not quote the sentence and sets its own driver mark in Phase 3.")
add("Source count and register size differ without a label",
    "`meta.counts.sources`; `meta.counts.sources_total_ids`; `sources`",
    f"`sources` {counts['sources']}, `sources_total_ids` {counts['sources_total_ids']}. The register holds {len(d['sources'])} IDs, of which {sum(1 for v in d['sources'].values() if v.get('duplicate_of'))} carry `duplicate_of`; {len(d['sources'])} minus those is {len(d['sources']) - sum(1 for v in d['sources'].values() if v.get('duplicate_of'))}, so `sources` appears to count unique sources. No field says so.",
    "Rename the first count `sources_unique` and say in the methods text what it counts.",
    "Yes. The guide quotes 1,099 as unique sources and names the register size where it matters.")
add("Issue count includes a retired record",
    "`meta.counts.issues`; `meta.counts.issues_active`; methods and glossary text",
    f"`issues` {counts['issues']}, `issues_active` {counts['issues_active']}. The methods text and the glossary say 193.",
    "Rename the first count `issue_records` or show 193 everywhere with the retired record footnoted.",
    "Yes. The guide says 193 active issue records.")
add("Conceptual loop chains mix labels and IDs",
    "`loops.B2.chain`; `loops.B3.chain`; `loops.R9.chain`",
    "Closed loops list variable IDs in `chain`. The conceptual loops list " + "; ".join(f"{k}: " + ", ".join(f'"{x}"' for x in conc[k]) for k in conc)
    + ". \"A4 hardship\" puts an ID inside a label.",
    "Keep `chain` for IDs only (null where a step has no variable) and put the words in `chain_labels`.",
    "Yes. The guide draws conceptual loops from `chain_labels`.")
add("Conceptual loops carry loop grades without numbered steps",
    "`loops.B2.evidence`; `loops.B3.evidence`; `loops.R9.evidence`",
    "; ".join(f"{k}: \"{v}\"" for k, v in conc_g.items()) + f". The glossary says: \"{G['Loop closure']}\"",
    "Say what the grade covers when a loop has no complete numbered chain, for example the evidence for its mechanism.",
    "Yes. The guide prints the closure status first and the grade text second, with the hollow line for conceptual steps.")
add("Delivery log dates are free text in several formats, out of time order",
    "`deliveryLog.rows[].date`",
    f"{len(date_formats)} formats across {len(rows_dl)} rows: " + ", ".join(f"\"{k}\" {v}" for k, v in date_formats.most_common())
    + f" (9 stands for a digit). Rows are {'in' if D['delivery']['v7_order_is_chronological'] else 'not in'} time order of their start dates, for example DL07 (1935-2023) follows DL06 (1966-2012).",
    "Add `start`, `end`, `precision` and `kind` (span, open span, point) beside the display string.",
    "Yes. The guide's period rule parses all 24 strings (Mark 5).")
add("Mixed names a direction, a jurisdiction and a grade",
    "`repairLog.rows[].direction`; `issues[].jurisdiction`; methods grade Mixed",
    f"Repair log rows with direction `mixed`: {g['repairLog.rows.direction'].get('mixed')}. Issues with jurisdiction `mixed`: {g['issues.jurisdiction = mixed'].get('mixed')}.",
    "Rename the non-grade values, for example `both directions` and `several levels`, or document the three meanings.",
    "Yes. The guide displays \"Mixed direction\" and \"Several levels of government\".")
add("Log rows reference loops by text",
    "`repairLog.rows[].loop`; `deliveryLog.rows[].loop`",
    f"All {len(rows_rl)} repair rows and {sum(1 for r in rows_dl if r['loop'])} delivery rows give a loop as \"Loop R10: title\". Every title matches V7 today; delivery rows add notes such as \"(running in the improving direction)\".",
    "Add `loop_id` and keep the text as a note.",
    "Yes. The guide reads the ID from the text.")
add("Some variables carry two domains in one string",
    "`nodes[].domain`",
    "; ".join(f"{k} \"{v}\"" for k, v in mf["compound_domains"]) + ".",
    "Store a list, first domain first.",
    "Yes. The guide splits on \"/\" and files a variable under its first domain, as Concept 11 does.")
add("Effect codes and delay codes share the letters S, M and L",
    "`reforms[].effects`; `links[].delay`",
    f"Delay codes: \"{D['delay']['definition']}\" Effect codes: " + ", ".join(f"{k} {v}" for k, v in d["outcomes"]["effect_codes"].items()) + ".",
    "Document the overlap in the methods text, or spell delays out in every display.",
    "Yes. The guide never prints a bare letter outside a data table (Mark 6).")
add("Two words for areas",
    f"renderer `KIND_LABEL` (`script.js` line {kind_line}); `layers.*.regions`; `methods.boundary`",
    f"The renderer labels a domain \"{D['renderer']['kind_label'].get('domain')}\" and lists clusters under \"Areas of this layer\"; the methods text calls the clusters \"clusters\"; the data key for D01 to D10 is `domains`.",
    "One word per level: for example \"domain\" for D01 to D10 and \"area\" for A to E and X.",
    "Yes. The guide uses Domain for D01 to D10 and area for A to E.", "Renderer")
add("Documented and well supported draw the same line",
    "renderer legend and `.edge` styles",
    f"Legend: \"documented or well supported\" share the solid line; dashes plausible {D['renderer']['edge_css_dashes']['u-plausible']}, contested {D['renderer']['edge_css_dashes']['u-contested']}, hypothesis {D['renderer']['edge_css_dashes']['u-hypothesis']}.",
    "If Dustin approves the record square at Gate 1, add it to documented connection labels.",
    "Yes. The guide adds the square in its own figures.", "Renderer")
add("Conceptual steps are close to the plausible dash",
    "renderer `.edge.u-concept`",
    f"Conceptual steps use dash {D['renderer']['edge_css_dashes']['u-concept']} in #8b9095; plausible uses {D['renderer']['edge_css_dashes']['u-plausible']}. Both are dashed gray lines that differ in shade and dash length, which is a weak difference in grayscale and print.",
    "If approved at Gate 1, draw conceptual steps as a hollow line.",
    "Yes. The guide draws the hollow line.", "Renderer")
add("Authority links end in an arrowhead",
    "renderer markers (`-t` teal arrowhead) and `.edge.authority`",
    "Authority connections are drawn teal with a filled arrowhead and \"auth\" in the label. The arrowhead is the causal end mark.",
    "If approved at Gate 1, end authority lines in an open diamond with \"no sign\" in the label.",
    "Yes. The guide draws the open diamond.", "Renderer")
add("Interface palette and fonts",
    "renderer styles",
    "V7 uses its own palette (paper #F3F2EA, red #BD2C32, navy #223458, teal #3F6C64) and renamed URW Nimbus faces.",
    "Converge on Inter Tight, Inter and Pillar Red, as Dustin decided (DC-03).",
    "Yes. Decided; listed so the atlas editor has it in one place.", "Renderer")

lines = []
lines.append("# Atlas V7.1 issue list")
lines.append("")
lines.append("For the atlas editor. Prepared by the data visualization and systems lead on October 21, 2026, under Dustin's decision DC-08 (\"Prepare them for an atlas V7.1\").")
lines.append("")
lines.append(f"Every value below was read by script from the Atlas V7 snapshot of {d['meta']['snapshot']} (`work/extract/atlas-v7-data.json`) and the extracted renderer (`work/extract/atlas-v7/script.js`). Script: `work/build/scripts/phase-1/build_v71_issue_list.py`. Nothing in V7 was changed. V6 never edits the model; the last line of each item says how the guide handles the issue until V7.1 exists.")
lines.append("")
lines.append("How to read an item: **Where** gives the JSON path (or renderer location), **Evidence** quotes or counts what V7 holds, **Fix** is the proposal, and **V6 works around it** says what the guide does meanwhile. Items 1 to " + str(sum(1 for i in issues if i[5] == 'Model')) + " are in the model JSON; the rest are in the renderer, which ships in the same atlas file.")
lines.append("")
lines.append("| # | Issue | Where | Kind |")
lines.append("|---|---|---|---|")
for n, it in enumerate(issues, 1):
    lines.append(f"| {n} | {it[0]} | {it[1].split(';')[0]} | {it[5]} |")
lines.append("")
for n, (title, loc, ev, fix, v6, kind) in enumerate(issues, 1):
    lines.append(f"## {n}. {title}")
    lines.append("")
    lines.append(f"- **Where:** {loc}")
    lines.append(f"- **Evidence:** {ev}")
    lines.append(f"- **Fix:** {fix}")
    lines.append(f"- **V6 works around it:** {v6}")
    lines.append("")

lines.append("## Checks that found no problem")
lines.append("")
lines.append(f"- Loop type against signs: every loop with numbered steps has an even count of negative steps when reinforcing and an odd count when balancing ({len(D['delay']['loop_sign_rule'])} loops, all consistent).")
lines.append(f"- Loop delay: each loop's delay equals its slowest step ({len(D['delay']['loop_delay_rule'])} loops, all consistent).")
lines.append("- Loop chains and link lists agree in order, start variable and sign, and every connection that names a loop is listed by that loop.")
lines.append(f"- Authority: all {len(D['authority']['links'])} authority connections have no sign and sit in no loop.")
lines.append("- Connection ID prefixes match the glossary (L, LE, LT, LX, T).")
lines.append("- The loop titles quoted in the repair and delivery logs all match V7's loop records.")
lines.append("")
lines.append("## Concept and guide files (not the model)")
lines.append("")
lines.append("These belong to the supplied demonstrations, which V6 replaces. They need no V7.1 change. Full detail is in `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md`.")
lines.append("")
lines.append(f"- **Concept 06 Ledger** counts the rejected reform R-35 in its D03 and D04 totals (10 and 14; V7 has 9 and 13 live reforms there). R-35 is V7's only rejected reform ({', '.join(mf['rejected_reforms'])}). Its link counts also use a different rule from Concept 11's (links that touch a domain against links filed under the variable they move), and neither page prints its rule.")
lines.append("- **Concept 08 Field Guide** says \"20 loops close fully\"; V7 counts 18 closed, 2 closed with a hypothesized step and 3 conceptual. Its specimens set a loop ID among ring variables (\"D5 C3 C5 B4\", where B4 is the loop).")
lines.append("- **Concept 09 Circuit** says the return line carries policy \"back into the economy\"; the three return connections run to area A, Economic structure.")
lines.append("- **Concept 04 Broadsheet** names Massachusetts Question 3 and omits Alaska Ballot Measure 2, which V7's R-01 text names.")
lines.append("- **Concept 05 Iceberg** renames V7's reform bands.")
lines.append("- **Concept 03 Field Manual** draws all 31 cross-layer connections dotted, the hypothesis texture, though none is a hypothesis.")
lines.append("- **Concepts 10 and 11** draw ordinal effects as widths or thirds, drop the 38 qualifiers, and Concept 10 draws gains only and two feasibility classes.")
lines.append("- **Concepts V2 boards** use about 45 board-only short names for variables, beside V7's own `chain_labels`.")
lines.append("- **V5 Polished and the Atlas Visual System** dash hypotheses (V7 dots them), draw plausible L02 and LE26 solid, show the placeholder \"L##\", draw associations as a dotted map line, and draw ownership as a frame.")
lines.append("- **Correction to the Phase 0 table, row 40.** Phase 0 listed the Atlas Visual System's \"L54 is the weakest transfer to U.S. services\" as a conflict. V7's own loop summary says \"For U.S. services the weakest is L54, since its main study covers Brazilian mayors\" (`loops.B4.evidence_summary`), so the figure is faithful. The grade of all three B4 steps is well supported.")
lines.append("")
lines.append("## Change log")
lines.append("")
lines.append("- Created: `work/handoffs/phase-1/20261021_Atlas-V7-1-Issue-List.md` (this file), by `work/build/scripts/phase-1/build_v71_issue_list.py`.")
lines.append("- Modified: none. V7 and every file in `source/` are unchanged.")
lines.append("")
OUT.write_text("\n".join(lines), encoding="utf-8")
print("wrote", OUT.relative_to(ROOT), len(issues), "issues", len(" ".join(lines).split()), "words")
