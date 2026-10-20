#!/usr/bin/env python3
"""Phase 0 atlas reconciliation, step 2: write the reconciliation table.

Inputs (written by the other two phase-0 scripts):
  work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json
  work/handoffs/phase-0/20261020_Brief-V7-Values-Check.json
The rows below were written by hand after reading each flagged item in context.
Output: work/handoffs/phase-0/20261020_Atlas-Reconciliation-Table.md

Run with:  python3 -I build_reconciliation_table.py
"""
import collections
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
H = os.path.join(ROOT, "work", "handoffs", "phase-0")
DATA = json.load(open(os.path.join(H, "20261020_Atlas-Reconciliation-Data.json"), encoding="utf-8"))
BRIEF = json.load(open(os.path.join(H, "20261020_Brief-V7-Values-Check.json"), encoding="utf-8"))
OUT = os.path.join(H, "20261020_Atlas-Reconciliation-Table.md")

V5C = "work/extract/v5-polished/chapters/"
V5I = "work/extract/v5-polished/images/"
AVC = "work/extract/atlas-visual-system/chapters/"
AVI = "work/extract/atlas-visual-system/images/"
CV2 = "source/20261019_Oath-And-Action-Atlas-Design-Concepts_V2.html"

# File | Location | Item | Value shown | V7 value | Type | Resolution proposed
ROWS = [
    # ---------------- ID
    (V5I + "cc6e26ddee.svg (also " + AVC + "03-connections.html)", "V5P ch. 16 fig. 1; AVS ch. 03 figure",
     "Connection ID", "\"L## · delay S\", \"L## · delay M\"", "No connection L##. Real examples: L01 (delay S), L24 (delay M)",
     "ID", "Use real typed IDs in the grammar specimen, for example \"Connection L01 · S\", so a reader can look the example up."),
    (V5C + "15-standards.html and " + V5C + "16-atlas-system.html", "V5P Standards rules list and checklist; Atlas System captions",
     "R1 to R9", "Rules R1 to R9 (\"cite R5 instead of describing it\"); loops R1 and R16 in ch. 16, with R16 bare in two captions",
     "Loops R1 to R18 exist (R5 is \"Financial strain narrows who takes part in policy decisions\")", "ID",
     "Renumber the Standards rules with an unused prefix, for example \"Std-05\" (V7 uses no G, Std or QA prefix). Type every atlas chip: \"Loop R16\"."),
    (AVC + "04-loops.html; " + AVI + "9638b1d4fd.svg", "AVS ch. 04 captions and dark R1 figure", "R1",
     "\"the same R1 graph\" and \"R1 and R-01 are also distinct\" with bare R1 four times", "Loop R1; reform R-01 is a different record",
     "ID", "Apply the chapter's own rule in its captions: write \"Loop R1\" and \"Reform R-01\"."),
    (CV2, "Concept 08 Field Guide, every specimen", "Ring chips and loop ID",
     "Variable chips and the loop ID set in one row: \"D5 C3 C5 B4\" (B4 is the loop), \"B4 B6 R3\" (B4 is a variable), \"B4 C3 D2 R11\", \"A4 B5 E1 R5\"; \"B2, B3, R9\" listed as loops on the plate that rings variable B2 in R16",
     "Variable B4 \"Hostility toward the other political party\"; loop B4 \"Electoral consequences can improve public performance\"; loops B2, B3 conceptual",
     "ID", "Give loop IDs their own typed chip (\"Loop B4\") set apart from the ring; prefix ring chips or show names on the ring."),
    (CV2, "Concept 06 Ledger, domain table", "B2 to B5, D1 to D5, loop IDs",
     "Variable chips B2, B3, B4, B5 and D1 to D5 in the same table as domain codes D01 to D10 and bare loop IDs in \"Main loop\" (R1, R1b, R2, R3, R6, R8, R10)",
     "B2 to B5 are both variables and loops; D1 to D7 are variables, D01 to D10 domains", "ID",
     "Typed chips in every column: \"Var B4\", \"Loop R3\", \"Domain D02\"."),
    (CV2, "Concept 11 Register sheets 03 (D02), 04 (D03), 05 (D04), 11 (D10)", "B4, B5",
     "Variable B4 or B5 in the From column and on variable cards, and loop B4 or B5 in \"Closed loops that pass through\", on the same sheet; only the neighbouring name tells them apart",
     "Variables B4, B5 and loops B4, B5", "ID", "Typed chips; set loop chips in the loop style used in the loop list."),
    (CV2, "Concept 11 Register, all 12 data sheets", "D1 to D7 beside D01 to D10",
     "\"D1 Congress's capacity D04\": a variable chip and a domain tag in one row", "Variable D1; domain D04", "ID",
     "Write domain tags as \"Domain D04\" or use the domain short title, so a bare D-number never appears."),
    (CV2, "Concepts 01 Transit (R8), 02 Orbit (R10, R4a beside \"LEVER R-01\"), 04 Broadsheet (R10), 05 Iceberg (R10 beside R-01 to R-50)",
     "Loop and reform R-numbers", "Bare loop IDs on pages that also show reform IDs", "Loops R4a, R8, R10; reforms R-01 to R-50", "ID",
     "Typed chips (\"Loop R10\", \"Reform R-01\") on every page where both appear."),
    (CV2, "Concept 11 Register sheet 04 (D03); Concept 08 Field Guide", "B1 beside B1a",
     "Variable B1 and loop B1a on the same page", "Variable B1 \"Money spent to influence politics\"; loop B1a \"Independent oversight can limit policy favoritism\"",
     "ID", "Typed chips; never shorten B1a to B1."),
    # ---------------- delay
    (V5I + "4722932495.svg, e44e256497.svg, 0164ea8408.svg; " + AVI + "bcdfadeec2.svg, 8dd0d7807c.svg", "V5P ch. 16 figs. 2 to 4; AVS chs. 04 to 07 figures",
     "Delay letters", "\"S · well-supported\", \"M · plausible\", \"L · well-supported\"",
     "Delay codes S, M, L; effect codes +S, +M, +L use the same letters for size", "delay",
     "Spell delays out on public views (\"under 2 years\"), as Concepts V2 does, or set the letter inside a delay chip with its own key; never print a bare S, M or L near an effect code."),
    # ---------------- encoding: evidence lines
    (V5C + "16-atlas-system.html; " + AVC + "09-production.html; " + AVC + "03-connections.html", "Working rules table, \"Evidence\" row; connections table",
     "Hypothesis line", "\"Hypotheses use 8/7 dashes ... All other evidence distinctions remain textual\"",
     "Methods: a hypothesis \"is drawn as a dotted line\"; V7 renderer: hypothesis dotted (2 4), plausible dashed (9 4), contested dash-dot (9 3 2 3), documented and well-supported solid",
     "encoding", "Adopt V7's line code with a written grade on every link: dotted hypothesis, dashed plausible, dash-dot contested, solid documented and well-supported."),
    (V5I + "e44e256497.svg; " + AVI + "e44e256497.svg", "V5P ch. 16 fig. 3; AVS ch. 05", "T01",
     "Return step drawn with 8/7 dashes", "T01 hypothesis; V7 draws it dotted", "encoding", "Redraw T01 dotted and keep the \"Hypothesis\" label."),
    (V5I + "4722932495.svg; " + AVI + "4722932495.svg, 9638b1d4fd.svg", "V5P ch. 16 fig. 2; AVS ch. 04, light and dark", "L02",
     "Drawn solid, the same line as L01 and L03", "L02 plausible; V7 dashes plausible links", "encoding",
     "Dash L02 so the least certain step shows in the drawing as well as the label (brief worked example 1)."),
    (AVI + "8dd0d7807c.svg", "AVS ch. 07 household figure", "LE26", "Drawn solid", "LE26 plausible; V7 dashes plausible links",
     "encoding", "Dash LE26."),
    (V5I + "cc6e26ddee.svg; " + AVI + "cc6e26ddee.svg", "V5P ch. 16 fig. 1; AVS ch. 03", "Association line",
     "\"ASSOCIATION / REGISTER ONLY: a dotted, undirected line\"",
     "V7 uses the dotted line for hypotheses and keeps associations \"in the register and left off the map\"", "encoding",
     "Remove the dotted association line from the map grammar; show associations only in tables."),
    (CV2, "Concept 03 Field Manual, Figure 1-1", "Cross-layer lines", "The 31 connections that cross layers drawn as dotted plumb lines (dash 2 3)",
     "Dotted means hypothesis in V7 and \"Untested\" in the Concepts V2 shared language; none of these 31 is a hypothesis (15 documented, 5 well-supported, 7 plausible, 4 plausible_contested)", "encoding",
     "Draw cross-layer lines with the grade texture of each connection, or as thin solid plumb lines with a key."),
    (CV2 + " against V5P and AVS", "Concepts 00 to 11 keys (\"dashes mark some evidence\") against V5P/AVS rules", "Dashed line",
     "Dashed means plausible in Concepts V2 and hypothesis in V5P and AVS", "Dashed means plausible (V7 renderer)", "encoding",
     "Keep the Concepts V2 meaning, which matches V7, and retire the V5P/AVS dash rule."),
    (CV2, "Concept 00 key; Concept 06 Ledger evidence bars; Concept 09 texture key; Concept 11 index and sheet evidence bars", "Grade order and shade",
     "\"Strong evidence\" first and darkest (black), \"On the record\" second (dark gray)",
     "V7 grade meter ranks documented 4, well-supported 3, plausible 2, contested 2, hypothesis 1", "encoding",
     "Order keys as V7 does, or give documented its own pattern; avoid a single lightness ramp that reads as strength."),
    # ---------------- encoding: signs and types
    (CV2, "Concept 00 shared language and every Concepts V2 board", "Sign", "Plus and minus moved off the map; arrowhead \"raises\", bar \"lowers\"; signs kept only in the evidence view",
     "V7 diagrams label each step with its connection code and sign; the sign is the model's record", "sign",
     "Keep the end shape and print the sign in the connection chip (\"L25 −\") on public views, with the reading rule beside it."),
    (V5I + "cc6e26ddee.svg and " + AVC + "03-connections.html against " + CV2, "V5P/AVS authority row; Concepts V2 \"Decides\"",
     "Authority mark", "V5P/AVS: open arrowhead plus a verb (sets, funds, appoints). Concepts V2: open diamond, \"decides, no direction\"",
     "Authority: 7 connections, no polarity, never in a loop; V7's diagram legend draws a teal line labeled \"auth\" with no sign", "encoding",
     "Choose one mark. Proposal: the open diamond plus a verb label, so it cannot be read as a causal arrowhead."),
    (V5I + "4722932495.svg, e44e256497.svg; " + AVI + "8dd0d7807c.svg; " + CV2 + " Concepts 09 and 11",
     "All connection drawings", "Connection type", "Money (L01, L02, L03, LE16) and information (L26) links drawn as ordinary causal links with no type word",
     "Types: causal 80, money 17, information 9, authority 7, ownership 5", "encoding",
     "Add the V7 type as a word in the connection chip (\"L01 · money\"); never as a weight, ribbon or color."),
    (V5I + "cc6e26ddee.svg", "V5P ch. 16 fig. 1, \"MEMBERSHIP / CONTAINMENT\"", "Ownership",
     "A frame or bracket with \"no causal arrowhead or polarity\"",
     "Ownership links are signed connections (\"one quantity is held inside another\"): LE09 +, LE25 +, LT02 +, LT08 +, T12 −", "structure",
     "Use frames only for layout groups. Draw ownership as a signed connection tagged \"ownership\"."),
    (V5I + "cc6e26ddee.svg; " + AVC + "03-connections.html", "\"Six relationship conventions\"", "Grammar structure",
     "Same direction, opposite direction, hypothesized, authority, membership, association",
     "Five connection types plus separate polarity, grade and delay fields", "structure",
     "Rebuild the grammar on V7 fields: type, sign, grade and delay as four separate encodings."),
    (CV2, "Concept 00 key (\"Bigger dot, more connections\"); Concept 11 index matrix (\"Dot size counts connections\")",
     "Node and dot size", "Area scaled to a count with no size key", "Count of connections per variable or per pair of sheets",
     "encoding", "Add a size key with reference values, or print the count."),
    (CV2 + "; " + AVC + "01-language.html; " + V5C + "11-data.html; work/extract/v5-polished/chapters/07-grid.html",
     "Color roles", "Verdigris", "Economy layer (Concepts V2); \"record status, labeled\" (AVS); trackers and live status (V5 Grid); fourth series and \"In progress\" (V5 Data)",
     "V7 field nodes[].layer (core, economy, technology)", "encoding",
     "Give Verdigris one job and code layer by position and label first; Stone and Verdigris measure 1.28:1 in grayscale."),
    # ---------------- encoding: ordinal effects, routes
    (CV2, "Concept 10 Who Can Act, reform-to-outcome strands", "Effect size",
     "Strand width 1.3, 2.6 and 3.9 for small, moderate and large", "Ordinal codes +S, +M, +L; \"codes for different families are never added together\"",
     "encoding", "Brief tension 13: replace width with labeled ordinal marks (words or one to three pips with a key), or keep width with a key that says \"ordinal categories with no measured size\"; drop the Sankey bundling."),
    (CV2, "Concept 10 Who Can Act", "Costs", "Strands drawn only for expected gains; costs appear in the side text",
     "DQ: 2 gains carry a possible cost; EP: 4 reforms carry a possible small cost and no gain", "structure",
     "Draw costs with their own mark so the tradeoff stays on the graphic."),
    (CV2, "Concept 10 Who Can Act, route strands", "Feasibility", "Two classes: dark for high or medium, light for low or very low",
     "Four levels: high, medium, low, very low", "encoding", "Show all four levels with labels."),
    (CV2, "Concept 11 Register effect cells (all sheets); Concept 10 strands", "Effect qualifiers",
     "Plain codes shown as cell fills of one third, two thirds and full; qualifiers dropped",
     "38 of 200 effect values carry a qualifier or range (25 live reforms), for example R-25 DQ \"+S hypothesis\", R-24 EP \"+S contested long run\", R-12 DQ \"+M / -M risk\", R-29 EQ \"+M at scale; 0 at $1,000\"",
     "label", "Show the full V7 string beside the mark or behind a marked footnote; use ordinal pips rather than partial fills."),
    # ---------------- label
    (V5I + "*.svg; " + AVI + "*.svg; " + CV2, "All three demonstrations", "Grade words",
     "V5P/AVS print V7 codes (\"well-supported\", \"plausible\"); Concepts V2 prints \"Strong evidence\", \"On the record\", \"Some evidence\", \"Disputed\", \"Untested\"",
     "V7 display labels: Documented, Well supported, Plausible, Contested, Hypothesis (plus Mixed and Not yet tested)", "label",
     "One display vocabulary with a mapping table (brief tension 8). Decide whether \"Disputed\" or V7's \"Contested\" names plausible_contested."),
    (CV2, "Concepts 00 to 11 (\"Short variable names were written for these boards\")", "Variable short names",
     "About 45 board-only names, for example A1 \"Wealth at the top\", B4 \"Hostility to the other party\", C3 \"Risk of losing office\"",
     "V7 titles; V7 loop chain_labels give a different short set (A1 \"Wealth concentration\", B4 \"Affective polarization\", C3 \"Electoral pressure\")",
     "label", "Approve one short-label list, starting from V7 chain_labels; show the full V7 title at first use on every page."),
    (CV2, "Concepts 00, 01, 02, 04, 05 against 07, 08, 09, 11", "C2", "\"Primary decides the winner\" and \"Seats settled in the primary\"",
     "\"How often the primary decides the winner\"", "label", "Use one short name everywhere."),
    (CV2, "Concepts 08 Field Guide, 09 Circuit, 11 Register From column", "D4, TC5", "D4 \"Watchdogs and enforcement\"; TC5 \"Government digital teams\"",
     "D4 \"Ability to investigate and enforce the rules\"; TC5 \"Government's ability to build and run digital services\"", "label",
     "Name the capacity, as the AVS element rule requires (\"Keep actors distinct from the variables that describe their capacity\")."),
    (CV2, "Concepts 01, 02, 04, 08, 09, 11", "C5", "\"Incumbents defeated\"", "\"Incumbents defeated or pushed into retirement\"", "label",
     "Keep the retirement half: \"Incumbents defeated or retired\"."),
    (CV2, "Concept 06 Ledger, \"Main loop\" column", "Loop short names", "R3 \"Hostile content\", R1b \"Money and courts\", R2 \"Outside expertise\", R6 \"Bargaining and wealth\"",
     "V7 loop titles, for example R3 \"Political hostility and hostile content may reinforce each other\"", "label",
     "Use V7 titles or an approved short-title list."),
    (CV2, "Concept 08 Field Guide intro", "Closure", "\"20 loops close fully in V7\"",
     "18 \"closed: every step is a numbered connection\"; 2 \"closed with a hypothesized step\" (R2, R16); 3 conceptual", "label",
     "Use V7's closure terms; the plate's own \"2 close with an untested step\" can stay."),
    (CV2, "Concept 09 Circuit intro", "Return line", "\"3 connections along the bottom carry policy back into the economy\"",
     "The 3 return connections (L03, L31, L37) run from area E to area A, Economic structure; the economy layer is a separate part of the model",
     "label", "Say \"back to area A, Economic structure\"."),
    (CV2, "Concept 04 Broadsheet, proposal panel", "R-01 status", "\"The atlas takes no position on Massachusetts Question 3.\"",
     "\"The Atlas takes no position on Question 3 or Ballot Measure 2.\"", "label", "Name both measures, as Concept 07 does."),
    (CV2, "Concept 05 Iceberg, depth gauge", "Reform bands", "\"Numbers\", \"Power over the rules\", \"Goals and mindsets\"",
     "parameter, power to change the rules, goals", "label", "Use V7 band names, or print the mapping on the gauge."),
    (AVI + "bcdfadeec2.svg", "AVS ch. 04, B4 figure, \"KEEP THE QUALIFICATION\"", "L54", "\"L54 is the weakest transfer to U.S. services\"",
     "All three B4 links well-supported; V7 names no weakest step. L54 qualification: the main study concerns Brazilian mayors and \"U.S. service quality was not studied\"",
     "grade", "Quote the V7 qualification and drop \"weakest\", which reads as a lower grade."),
    (V5I + "0164ea8408.svg; " + AVI + "0164ea8408.svg", "V5P ch. 16 fig. 4; AVS ch. 06", "R-28 route",
     "\"Congress and a federal tax-law route through reconciliation\"", "Route FS (Federal statute), who \"Reconciliation\", feasibility low, no check date",
     "label", "Show the route code and feasibility: \"FS · low, 2026 to 2030\"."),
    # ---------------- structure
    (CV2, "Concept 06 Ledger, rows D03 and D04", "Reforms per domain", "D03: 10; D04: 14",
     "9 and 13 live reforms target these domains; the counts include the rejected R-35 (targets L18, L19)", "structure",
     "Exclude R-35, or count it with a \"rejected option\" label as the Register does."),
    (CV2, "Concept 06 Ledger against Concept 11 Register", "Counting rule", "D02 links: 27 (Ledger) and 19 (Register); D01: 13 and 9",
     "Both reproduce from V7: the Ledger counts links that touch a domain's variables, the Register counts links filed under the variable they move",
     "structure", "Print the counting rule in each column header."),
    (CV2, "Concept 11 index, \"The whole atlas\"", "Issues", "194", "194 records, 193 active, 1 retired (V7's home page says 193 issue records)",
     "structure", "Show \"193 active\" and footnote the retired record."),
    (V5I + "4722932495.svg, e44e256497.svg, 0164ea8408.svg; " + AVI + "b9cc0e3aa0.svg, bcdfadeec2.svg, 8dd0d7807c.svg", "V5P and AVS variable cards",
     "Variable type and meaning", "Cards show ID and title only", "Every variable has a type (stock, flow, auxiliary, driver) and increase_means",
     "structure", "Add the type word and the \"A higher value means\" line, as the Register and the Loop Card do."),
]

TYPES = ["ID", "sign", "grade", "delay", "label", "structure", "encoding"]


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


s = DATA["summary"]
cr = s["checks_run"]
reg_rows = len(DATA["register_rows"])
tags = sum(1 for r in DATA["register_rows"] if r["from_sheet_shown"])
also = sum(1 for v in DATA["register_vars"] if "Also under" in v["kind"])
link_attr = sum(1 for o in DATA["occurrences"] if "connection" in o["kinds"] and o["shown"])
COMP = [
    ("Concepts V2 Register connection rows: from and to, sign glyph, line texture, grade word, delay, name, filing sheet, plus %d from-sheet tags" % tags,
     reg_rows * 7 + tags, 0),
    ("Concepts V2 Register variable cards: title, type, loops, higher-means text, plus %d secondary domains" % also,
     cr["Register variable cards"] * 4 + also, 0),
    ("Concepts V2 Register reform rows: title and route list", cr["Register reform rows"] * 2, 0),
    ("Concepts V2 Register effect cells: ordinal value and cost bar", cr["Register effect cells"], 0),
    ("Concepts V2 Register sheet figures (12 sheets x 7) and index table (12 rows x 5, 4 busiest crossings)", 82 + 64, 0),
    ("Concepts V2 Field Guide specimens: type, turn time, title, ring order, weakest step, state, textures, end marks", cr["Field Guide specimens"] * 8, 0),
    ("Concepts V2 Who Can Act: route counts, feasibility counts, route names, family tallies, group sizes, reform titles",
     cr["Who Can Act route rows"] * 3 + cr["Who Can Act outcome rows"] + cr["Who Can Act group rows"] + cr["Who Can Act reform titles"], 0),
    ("Concepts V2 Ledger rows: variables, links, loops, reforms", cr["Ledger rows"] * 4, 2),
    ("Concepts V2 Circuit: tally, area cards, pass-on examples, 13 drawn bundle counts", 5 + 4 + cr["Circuit pass-on examples"] + 13, 0),
    ("Other numeric claims (layers, loops, closure, live reforms, cross-layer links, Iceberg bands)", cr["numeric and structural claims"], 0),
    ("Direction-and-sign sentences (\"A1 to B1 through L01 positive\")", cr["from-to-sign statements"] * 2, 0),
    ("AVS production table rows: from and to, sign, delay, grade", cr["table rows (link, from-to, sign, delay, grade)"] * 4, 0),
    ("Connection names shown without an ID, with their grade and delay", cr["link names shown without their ID"], 0),
    ("Connection IDs with a grade, delay or glyph shown beside them (all sources)", link_attr, 0),
    ("Reform effect words (Concepts V2 and AVS outcome figure)", cr["reform effect words"] + cr["AVS outcome cells"], 0),
    ("AVS domain titles and layer rows", cr["AVS domain rows"] + cr["AVS layer rows"], 0),
]
total_comp = sum(c[1] for c in COMP)
total_conf = sum(c[2] for c in COMP)
type_n = collections.Counter(r[5] for r in ROWS)

L = []
w = L.append
w("# Atlas reconciliation table, Phase 0")
w("")
w("Prepared by the data visualization and systems lead for Gate 0, October 20, 2026. Review only: nothing in `source/`, `work/extract/` or the V7 model was changed. "
  "Scripts: `work/build/scripts/phase-0/atlas_reconcile_extract.py` (extraction and comparison), `verify_brief_v7_values.py` (brief values) and "
  "`build_reconciliation_table.py` (this file). Machine-readable results: `work/handoffs/phase-0/20261020_Atlas-Reconciliation-Data.json` and "
  "`20261020_Brief-V7-Values-Check.json`.")
w("")
w("## Summary")
w("")
w("**Sources scanned.** V5 Polished chapters 11 (Data Visualization) and 16 (Atlas System), the text inside the four Atlas System SVG figures, and chapter 15 (Standards) for its rule numbers. "
  "All 11 Atlas Visual System chapters and all 78 of its images, including its 9 diagram SVGs. All 25 sections of Concepts V2, parsed from the source HTML with the text of its inline SVGs, "
  "and the 118 Register link glyphs decoded into sign and texture. %d documents in all." % s["documents_scanned"])
w("")
w("**Identifiers checked.** %s occurrences of %d distinct atlas identifiers: %d in V5 Polished (18 of them Standards rule numbers), %d in the Atlas Visual System and %s in Concepts V2, plus %d route-code chips. "
  "Every identifier resolves to a V7 record except the placeholder \"L##\" (4 occurrences, one image used in both V5 Polished and the Atlas Visual System). "
  "No issue, claim, source, repair-log or delivery-log ID appears in any of the three files." % (
      format(s["identifier_occurrences"], ","), s["unique_identifiers"], s["occurrences_by_source"]["V5 Polished"],
      s["occurrences_by_source"]["Atlas Visual System"], format(s["occurrences_by_source"]["Concepts V2"], ","),
      s["route_code_occurrences"]))
w("")
w("**Matches.** %s attribute comparisons against V7 (sign, grade, delay, from and to, names, counts, routes and effect codes); %s match and %d conflict. "
  "No file shows a wrong sign, grade, delay, from-and-to pair or connection name. The two value conflicts are the Ledger's reform counts for D03 and D04. "
  "The generic context scan raised 8 further flags; I read each in context and all 8 are false positives (listed at the end)." % (
      format(total_comp, ","), format(total_comp - total_conf, ","), total_conf))
w("")
w("| Comparison family | Comparisons | Conflicts |")
w("|---|---|---|")
for name, n, c in COMP:
    w("| %s | %d | %d |" % (esc(name), n, c))
w("| **Total** | **%s** | **%d** |" % (format(total_comp, ","), total_conf))
w("")
w("**Conflicts and ambiguities in the table: %d rows.** " % len(ROWS) +
  ", ".join("%s %d" % (t, type_n.get(t, 0)) for t in TYPES) + ". "
  "Most rows concern how the demonstrations encode V7 (line patterns, sign marks, widths, colors) and how they name things. "
  "The ID rows record every page where colliding identifiers (variable B2 to B5 against loop B2 to B5; loop R-numbers against reform R-numbers and the Standards rules R1 to R9; "
  "variable D1 to D7 against domain D01 to D10; variable B1 against loop B1a) sit on the same page without a type word. "
  "Pages that type their chips (\"VARIABLE B2\" on the V5 Polished R16 figure, \"Loop B4\" and \"Variable B4\" in the AVS loops chapter) are not listed.")
w("")
w("## Reconciliation table")
w("")
w("V5P is V5 Polished, AVS the Atlas Visual System. Concept numbers follow Concepts V2 (Concept 00 is the shared language; the Register's data sheets are sections 13 to 24 of the file).")
w("")
w("| # | File | Location | Item | Value shown | V7 value | Type | Resolution proposed |")
w("|---|---|---|---|---|---|---|---|")
for i, r in enumerate(ROWS, 1):
    w("| %d | %s |" % (i, " | ".join(esc(x) for x in r)))
w("")
w("## Master Brief values checked against V7")
w("")
w("Every V7 value quoted in sections 8 (items 7 and 8), 13 and 14, read from `atlas-v7-data.json`, plus the section 2 counts. "
  "%d claims: %d confirmed, %d corrected or not confirmed." % (
      len(BRIEF), sum(1 for b in BRIEF if b["status"] == "confirmed"), sum(1 for b in BRIEF if b["status"] != "confirmed")))
w("")
w("| Section | Claim in the brief | V7 reading | Status | Note |")
w("|---|---|---|---|---|")
for b in BRIEF:
    st = b["status"]
    if b["claim"].startswith("V7 draws drivers"):
        st = "not confirmed"
    v = b["v7"]
    if isinstance(v, (dict, list)):
        v = json.dumps(v, ensure_ascii=False)
    w("| %s | %s | %s | %s | %s |" % (b["section"], esc(b["claim"]), esc(str(v))[:260], st, esc(b["note"])))
w("")
w("## V7 inconsistencies to log for Dustin")
w("")
w("I changed nothing in V7. These belong in `work/ledger/*_Open-Questions.md` when the studio lead starts it.")
w("")
for x in [
    "Grade vocabulary (brief tension 8, confirmed and extended). Connections use `well-supported` and `plausible_contested`; issues use `well_supported` and `retired`; claims use `well-supported` and `contested`; "
    "reform remedy evidence uses `plausible_contested` twice and `contested` once; loop `evidence` is free text that mixes grades by step. The methods text and the renderer define `Mixed` and the renderer adds `Not yet tested`, "
    "and no record carries either as a grade. The renderer maps `plausible_contested` and `contested` to one display label, \"Contested\".",
    "D6 \"State and local testing of reforms\" is typed `flow`, and its `kind_plain` text begins \"Stock (an amount built up over time)\".",
    "`meta.counts.sources` is 1,099 while the source register holds 1,140 IDs (`sources_total_ids`). The brief quotes 1,099, which matches `meta`.",
    "38 of the 200 reform effect values extend the seven codes with qualifiers or ranges, for example \"+M sector\", \"0 to -S\" and \"+M / -M risk\".",
    "13 of 126 reform-route entries carry a `checked` date; the other 113 are null. For R-01, SS and FS have no date.",
    "194 issue records include 1 retired record; the V7 home page counts 193.",
    "V7's own interface palette (paper #F3F2EA, red #BD2C32, navy #223458, teal #3F6C64) differs from the locked brand palette. V7 stays the authority for content only.",
]:
    w("- " + x)
w("")
w("## What I checked and what I could not")
w("")
w("Checked:")
w("")
for x in [
    "Every identifier in the three files against V7 by script, and every flagged item by reading it in context.",
    "All 118 Register connection rows, 51 variable cards, 86 reform rows and 344 effect cells, field by field.",
    "All 20 Field Guide specimens: titles, types, turn times, ring order against the V7 chain, weakest steps, states, and the arc textures and end marks drawn in each SVG.",
    "Every count printed in Concepts V2 that V7 can reproduce: Register sheets and index, busiest crossings, Ledger rows, Circuit tallies and the 13 drawn bundle counts, Who Can Act routes, families and groups, layer and loop totals.",
    "The line patterns in the V5 Polished and AVS figure SVGs against V7's renderer CSS (`work/extract/atlas-v7/styles.css`) and methods text.",
    "The 1440 px screenshots of V5 Polished chapters 11 and 16, V7's home page, and Concepts V2 tiles 03, 07, 08, 09, 10 and 11.",
]:
    w("- " + x)
w("")
w("Not checked:")
w("")
for x in [
    "Station order on the Concept 01 Transit lines, the hairline count on the Concept 02 Orbit dial, the plumb lines on the Concept 03 Field Manual and the wire routing on the Concept 09 Circuit. These are drawn as SVG paths with no labels, so a check needs geometry matching.",
    "Strand-by-strand routing on Concept 10. I checked the totals by stroke width (small, moderate and large strands match V7's tallies) but not which reform each strand reaches.",
    "Tick counts for delay on the Concepts V2 arrows.",
    "Whether V7's rendered map draws drivers as rounded pills; I read the extracted renderer and two screenshots, and no screenshot shows the map.",
    "The Atlas Visual System and Concepts V2 at 390 px, in grayscale and with assistive technology.",
]:
    w("- " + x)
w("")
w("## Automatic flags reviewed and dismissed")
w("")
w("| File | Item | Flag | Why it is not a conflict |")
w("|---|---|---|---|")
for f in DATA["reviewed_false_positives"]:
    w("| %s | %s | %s shown, V7 %s | %s |" % (esc(f["file"].split("/")[-1] + ", " + f["location"].split(";")[0]), f["item"], f["shown"], f["v7"], esc(f["why"])))
w("")
open(OUT, "w", encoding="utf-8").write("\n".join(L) + "\n")
print("rows", len(ROWS), dict(type_n), "comparisons", total_comp, "conflicts", total_conf)
