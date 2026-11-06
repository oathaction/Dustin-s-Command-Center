"""Chapter 01 Purpose: content and specimens for stage board A. Imported by guide_editor_build.py."""
from guide_editor_common import (AMP_DISPLAY, ARTICLE, BASE, CHART_DATA, HL, LOCKED, PIECE, TILE_GRID, WORDMARK24,
                                 WORDMARK24_PRUSSIAN, amp_h, e, hinge, ill, load, q)

ATLAS = "Oath & Action’s systems atlas, Who Do They Answer To?"

SRC_STOCK_SURVEY = ("Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, "
                    "fielded May 19 to 30, 2023, United States, as recorded in " + ATLAS + ", snapshot of October 15, 2026. "
                    "The survey came three years before the House and Senate votes.")
SRC_STOCK_VOTES = ("Source: U.S. House of Representatives, Roll Call 280, passage of H.R. 7008, July 22, 2026, and U.S. Senate, "
                   "Vote 253, cloture on the motion to proceed, September 30, 2026, United States, as recorded in " + ATLAS +
                   ", snapshot of October 15, 2026. The studio could not open the Senate’s own page for the vote.")
SRC_INITIATIVE = ("Source: Ballotpedia, States with initiative or referendum, 50 states and DC. Retrieved November 6, 2026. "
                  "Mississippi’s process exists on paper but cannot be used after a 2021 state supreme court ruling.")
SRC_FEC = ("Source: Federal Election Commission, Official 2024 Presidential General Election Results, compiled from state "
           "election offices, November 2024, 50 states and DC. Retrieved November 6, 2026.")
SRC_R4A = ("Source: " + ATLAS + ", Loop R4a, the map-drawing loop, case record, August 2025 to November 2025, Texas and "
           "California, snapshot of October 15, 2026. These events show maps being drawn; they do not measure how long "
           "either majority’s hold lasts.")
SRC_PAY = ("Sources: Anna Stansbury and Lawrence H. Summers, “Productivity and Pay: Is the Link Broken?”, NBER Working "
           "Paper 24165, December 2017, United States; Economic Policy Institute, “The Productivity-Pay Gap”, 1979 to 2026, "
           "United States; both as recorded in " + ATLAS + ", the connection from productivity to household income, "
           "snapshot of October 15, 2026. The two differ in the price index they use and in how they count benefits. "
           "The atlas grades the connection plausible and contested.")
SRC_CLOTURE = "Source: " + ATLAS + ", glossary entry “Cloture”."
SRC_ELECTRIC = "From " + ATLAS + ", the everyday answer to “Why is my electric bill going up?”"


def kick(*parts, illus=False):
    s = "".join(f'<span class="{c}">{e(t)}</span>' for c, t in parts)
    return f'<p class="kick">{s}{ill() if illus else ""}</p>'


# ---------------------------------------------------------------------------------------------------------------
# Pieces, one per pillar, at the phone width they ship at (360 px)
# ---------------------------------------------------------------------------------------------------------------
def piece_explain():
    return f'''<article class="pc" aria-label="Explain piece">
{kick(("chip solid", "Explainer"), ("k", "Explain"))}
<p class="hl">Why is my electric bill going up?</p>
<p class="dek">A regulator or a board approves your rate.</p>
<div class="blk"><p class="lab">Who decides</p><p>For an investor-owned utility, your state’s public utility commission sets rates in a rate case, its formal review of the utility’s request. For public power and cooperatives, a city council, a utility board or a co-op board does.</p></div>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Find your utility’s name on your bill, then look up its open rate case on your state commission’s site for the dates to comment.</p>
<span class="ask" data-red="working">Find your rate case</span>
<p class="by">{e(SRC_ELECTRIC)}</p>
</article>'''


def piece_track():
    return f'''<article class="pc" aria-label="Track piece">
{kick(("chip solid", "Tracker"), ("k", "Track"))}
<p class="hl">Stock Trading Ban Tracker</p>
<p class="dek">H.R. 7008 would bar members of Congress from trading individual stocks. As of October 15, 2026.</p>
<ol class="stages">
<li class="done"><span class="sn">1</span><span><b>Passed the House, 232 to 198</b><br>July 22, 2026</span></li>
<li class="now"><span class="sn">2</span><span><b>Senate vote to take it up failed, 53 to 47</b><br>September 30, 2026. It needed 60.</span></li>
<li class="next"><span class="sn">3</span><span><b>Next: a Senate vote to take it up</b><br>It needs 60 votes to go forward.</span></li>
</ol>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Get an email the day the Senate schedules its next vote on the bill.</p>
<span class="ask" data-red="working">Follow this bill</span>
<p class="by">{e(SRC_STOCK_VOTES)}</p>
</article>'''


def piece_connect():
    return f'''<article class="pc" aria-label="Connect piece">
{kick(("chip solid", "Explainer"), ("k", "Field Notes"), illus=True)}
<p class="hl">Who answers for the repair on your street?</p>
<p class="dek">Alder County’s public works department schedules street repairs, and the Board of Supervisors sets its road budget each spring. {ill()}</p>
<div class="blk"><p class="lab">What to say in 90 seconds</p><p>Give the street and the date you reported the damage. Then ask the board when the repair is scheduled and what it will cost.</p></div>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Speak at the board’s public comment period, 6 p.m. Tuesday, April 13, 2027. {ill()}</p>
<span class="ask" data-red="working">Find your supervisor</span>
</article>'''


def piece_act():
    return f'''<article class="pc" aria-label="Act piece">
{kick(("chip", "Act · How to take part"), illus=True)}
<p class="hl">Alder County votes on backyard cottages March 9. Send a comment by March 3 or speak at the meeting.</p>
<div class="blk"><p class="lab">Who decides</p><p>Five county supervisors decide, and three votes pass the change. {ill()}</p></div>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Send a written comment by 5 p.m. Wednesday, March 3, 2027. {ill()}</p>
<span class="ask" data-red="working">Send a comment</span>
</article>'''


STAGES = """
.ed .stages{list-style:none;margin:12px 0 0;padding:0;border-top:1px solid var(--oa-color-border-hairline)}
.ed .stages li{display:grid;grid-template-columns:2rem minmax(0,1fr);gap:8px;padding:10px 0 10px 10px;border-bottom:1px solid var(--oa-color-border-hairline);line-height:1.45}
.ed .stages li.now{border-left:4px solid var(--oa-color-border-strong);padding-left:6px}
.ed .stages li.next{color:var(--oa-color-text-secondary)}
.ed .stages .sn{font:800 1.125rem/1.3 var(--oa-font-family-display)}
.ed .grid4{display:flex;flex-wrap:wrap;gap:40px 48px;align-items:flex-start}
.ed .grid4>div{width:360px;max-width:100%}
.ed .grid4 .pl{font:800 1.125rem/1.2 var(--oa-font-family-display);margin:0 0 6px}
"""


# ---------------------------------------------------------------------------------------------------------------
# The two Act kinds at the site's reading width
# ---------------------------------------------------------------------------------------------------------------
def process_piece(fail=False):
    ask = "Tell the supervisors to vote yes" if fail else "Send a comment"
    sides = ('<div class="sec"><p class="lab">Why it matters</p><p>More homes would ease rents across the county, and the '
             'change costs taxpayers nothing. ' + ill() + '</p></div>') if fail else (
        '<div class="sec"><p class="lab">What each side has said</p><div class="two">'
        '<p><b>Supporters</b> said more homes would ease rents. ' + ill() + '</p>'
        '<p><b>Opponents</b> said sewers were sized for fewer homes. ' + ill() + '</p></div></div>')
    step2 = "" if fail else f'<p class="step">Or speak for two minutes at 6 p.m. Tuesday, March 9, 2027. {ill()}</p>'
    track = "" if fail else f'<p class="foot">Follow the vote on the Accessory Homes Tracker. {ill()}</p>'
    return f'''<article class="art" aria-label="Process piece">
{kick(("chip", "Act · How to take part"), illus=True)}
<p class="hl">Alder County votes on backyard cottages March 9. Send a comment by March 3 or speak at the meeting.</p>
<p class="dek">The Board of Supervisors will decide whether homeowners may build one small cottage behind a house. {ill()}</p>
<div class="sec"><p class="lab">Who decides</p><p>Five county supervisors decide, and three votes pass the change. {ill()}</p></div>
{sides}
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Send a written comment by 5 p.m. Wednesday, March 3, 2027. {ill()}</p>
{step2}
<span class="ask" data-red="working">{e(ask)}</span>
{track}
</article>'''


def position_piece(fail=False):
    label_top = "" if fail else '<span class="chip solid">Our position</span><span class="k">Act</span>'
    kickh = f'<p class="kick">{label_top}{ill()}</p>' if not fail else f'<p class="kick"><span class="k">Act</span>{ill()}</p>'
    against = "" if fail else (
        '<div class="sec"><p class="lab">The strongest case against</p><p>Committee chairs in both parties say posting every '
        'procedural vote would discourage early compromise and need new clerk staff. Sources: committee testimony, February '
        '2027; the clerk’s estimate. ' + ill() + '</p></div>'
        '<div class="sec"><p class="lab">What we don’t know</p><p>Whether faster posting changes how members vote. ' + ill() + '</p></div>')
    disc = "" if fail else ('<p class="disc">Oath &amp; Action supports S. 214. Read our explainer on it, which sets out the main '
                            'arguments, before you decide.</p>')
    foot = (f'<p class="foot"><span class="chip solid">Our position</span> Decided by the editorial board.</p>' if fail else
            f'<p class="foot">Decided by the editorial board, February 26, 2027. No funder reviewed this piece. All our positions are in the position log. {ill()}</p>')
    return f'''<article class="art" aria-label="Position piece">
{kickh}
<p class="hl">State senate committees should post every vote within two days.</p>
<p class="dek">We support S. 214, which would require it. {ill()}</p>
<div class="sec"><p class="lab">What the record shows</p><p>Documented: 14 of 20 committees posted no roll calls last session. Source: the senate clerk’s journal, 2026. {ill()}</p></div>
{against}
{hinge()}
{disc}
<span class="ask" data-red="working">Ask your senator to vote yes</span>
{foot}
</article>'''


# ---------------------------------------------------------------------------------------------------------------
# Charts and maps
# ---------------------------------------------------------------------------------------------------------------
CHART = """
.ed .ct{font:800 1.25rem/1.2 var(--oa-font-family-display);letter-spacing:-.01em;margin:0 0 4px;max-width:34ch;text-wrap:balance}
.ed .cm{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin:0 0 12px}
.ed .bars{display:grid;gap:10px;margin:0;max-width:520px}
.ed .bar{display:grid;grid-template-columns:7.5rem minmax(0,1fr);gap:10px;align-items:center}
.ed .bar .n{font:var(--oa-type-data-label);font-size:.9375rem}
.ed .bar .t{position:relative;height:28px}
.ed .bar .f{display:flex;align-items:center;justify-content:flex-end;height:28px;padding-right:8px;font:700 .9375rem/1 var(--oa-font-family-reading);font-variant-numeric:tabular-nums}
.ed .f.ink{background:var(--oa-color-data-emphasis);color:var(--oa-color-surface-newsprint)}
.ed .f.ctx{background:var(--oa-color-data-context);color:var(--oa-color-surface-white)}
.ed .f.red{background:var(--oa-color-palette-pillar-red);color:var(--oa-color-palette-charcoal)}
.ed .f.blue{background:var(--oa-color-palette-prussian);color:var(--oa-color-palette-white)}
.ed .key{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 10px;font-size:.9375rem}
.ed .sw{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:6px}
.ed .sw.red{background:var(--oa-color-palette-pillar-red)}.ed .sw.blue{background:var(--oa-color-palette-prussian)}
.ed .vote{max-width:520px}
"""


def bars(rows, title, measure, src, names=True, key=None):
    out = [f'<div class="ed vote"><p class="ct">{e(title)}</p><p class="cm">{e(measure)}</p>']
    if key:
        out.append('<p class="key">' + "".join(f'<span><span class="sw {c}"></span>{e(t)}</span>' for c, t in key) + "</p>")
    out.append('<div class="bars">')
    for name, val, cls, vmax in rows:
        lab = e(name) if names else '<span aria-hidden="true"></span>'
        out.append(f'<div class="bar"><span class="n">{lab}</span><span class="t"><span class="f {cls}" style="width:{val / vmax * 100:.1f}%"'
                   f'{" data-red=\"failure\"" if cls == "red" else ""}>{e(val)}{"%" if vmax == 100 else ""}</span></span></div>')
    out.append(f'</div><p class="src">{e(src)}</p></div>')
    return "".join(out)


def tile_map(mode):
    """mode 'rule': states with a working citizen initiative; mode 'winner': the failure, colored by 2024 winner."""
    tiles = load(TILE_GRID)
    data = load(CHART_DATA)["datasets"]
    init = {r["code"]: r for r in data["initiative-states"]["rows"]}
    pres = {r["code"]: r for r in data["presidential-shift-by-state"]["rows"]}
    S, G = 27, 3
    w, h = 12 * S + 11 * G, 8 * S + 7 * G
    cells = []
    counts = {"work": 0, "paper": 0, "none": 0, "rep": 0, "dem": 0}
    for t in tiles:
        x, y = t["col"] * (S + G), t["row"] * (S + G)
        c = t["code"]
        if mode == "rule":
            r = init[c]
            if r.get("citizen_initiative") == 1.0 and (r.get("initiative_usable") == 1.0 or c == "DC"):
                kind, fill, ink = "work", "var(--oa-color-data-emphasis)", "var(--oa-color-surface-newsprint)"
            elif r.get("citizen_initiative") == 1.0:
                kind, fill, ink = "paper", "url(#hatch)", "var(--oa-color-text-primary)"
            else:
                kind, fill, ink = "none", "var(--oa-color-surface-newsprint)", "var(--oa-color-text-primary)"
            if c != "DC":
                counts[kind] += 1
            red = ""
        else:
            rep = pres[c]["margin_2024"] > 0
            kind = "rep" if rep else "dem"
            counts[kind] += 1
            fill = "var(--oa-color-palette-pillar-red)" if rep else "var(--oa-color-palette-prussian)"
            ink = "var(--oa-color-palette-charcoal)" if rep else "var(--oa-color-palette-white)"
            red = ' data-red="failure"' if rep else ""
        cells.append(f'<g><rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{fill}" stroke="var(--oa-color-border-strong)" '
                     f'stroke-width="1"{red}/><text x="{x + S / 2}" y="{y + S / 2 + 4.5}" text-anchor="middle" fill="{ink}" '
                     f'font-size="13" font-weight="700" font-family="var(--oa-font-family-reading)">{c}</text></g>')
    defs = ('<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="6" height="6" fill="var(--oa-color-surface-newsprint)"/><line x1="0" y1="0" x2="0" y2="6" '
            'stroke="var(--oa-color-data-emphasis)" stroke-width="2.5"/></pattern></defs>')
    svg = (f'<svg viewBox="-1 -1 {w + 2} {h + 2}" width="{w + 2}" height="{h + 2}" aria-hidden="true" focusable="false">'
           f'{defs}{"".join(cells)}</svg>')
    return svg, counts


MAP = """
.ed .mapk{list-style:none;margin:12px 0 0;padding:0;display:grid;gap:6px;font-size:.9375rem;max-width:360px}
.ed .mapk li{display:grid;grid-template-columns:22px minmax(0,1fr);gap:8px;align-items:start}
.ed .mapk svg{margin-top:3px}
.ed .mapw{display:flex;flex-wrap:wrap;gap:16px 28px;align-items:flex-start}
"""


def key_swatch(fill, red=False):
    r = ' data-red="failure"' if red else ""
    defs = ('<defs><pattern id="hk" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" '
            'height="6" fill="var(--oa-color-surface-newsprint)"/><line x1="0" y1="0" x2="0" y2="6" stroke="var(--oa-color-data-emphasis)" '
            'stroke-width="2.5"/></pattern></defs>') if "#hk" in fill else ""
    return (f'<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true" focusable="false">{defs}<rect x=".5" y=".5" '
            f'width="15" height="15" fill="{fill}" stroke="var(--oa-color-border-strong)"{r}/></svg>')


def diverging_key(fail=False):
    steps = [("Down 2 points or more", "down2"), ("Down less than 2", "down1"), ("No change", "flat"),
             ("Up less than 2", "up1"), ("Up 2 points or more", "up2")]
    out = []
    for i, (word, kind) in enumerate(steps, 1):
        if fail:
            fill = ["var(--oa-color-palette-pillar-red)", "var(--oa-color-palette-pillar-red)", "var(--oa-color-surface-newsprint)",
                    "var(--oa-color-palette-prussian)", "var(--oa-color-palette-prussian)"][i - 1]
            red = ' data-red="failure"' if i <= 2 else ""
            sw = (f'<svg width="56" height="40" viewBox="0 0 56 40" aria-hidden="true" focusable="false"><rect x=".5" y=".5" width="55" '
                  f'height="39" fill="{fill}" stroke="var(--oa-color-border-strong)"{red}/></svg>')
            if i in (2, 4):
                sw = sw.replace(f'fill="{fill}"', f'fill="{fill}" fill-opacity="0.55"')
        else:
            fill = f"var(--oa-chart-color-diverging-fill-step{i})"
            ink = f"var(--oa-chart-color-diverging-label-step{i})"
            if kind == "flat":
                arrow = f'<line x1="20" y1="20" x2="36" y2="20" stroke="{ink}" stroke-width="2.5"/>'
            else:
                up = kind.startswith("up")
                y1, y2, tip = (28, 12, "12") if up else (12, 28, "28")
                head = (f'<polyline points="22,{17 if up else 23} 28,{y2} 34,{17 if up else 23}" fill="none" stroke="{ink}" '
                        f'stroke-width="2.5" stroke-linejoin="miter"/>')
                arrow = f'<line x1="28" y1="{y1}" x2="28" y2="{y2}" stroke="{ink}" stroke-width="2.5"/>{head}'
                if kind in ("down2", "up2"):
                    arrow = arrow.replace('x1="28"', 'x1="24"', 1).replace('x2="28"', 'x2="24"', 1)
                    arrow += (f'<line x1="32" y1="{y1}" x2="32" y2="{y2}" stroke="{ink}" stroke-width="2.5"/>')
            sw = (f'<svg width="56" height="40" viewBox="0 0 56 40" aria-hidden="true" focusable="false"><rect x=".5" y=".5" width="55" '
                  f'height="39" fill="{fill}" stroke="var(--oa-color-border-strong)"/><rect x="14" y="6" width="28" height="28" '
                  f'fill="none" stroke="{ink}" stroke-width="1.5"/>{arrow}</svg>')
        out.append(f'<li>{sw}<span>{e(word)}</span></li>')
    return out


DIV = """
.ed .dk{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:0}
.ed .dk li{display:grid;justify-items:start;gap:6px;width:112px;font-size:.9375rem;line-height:1.3;padding-right:8px}
.ed .dkw{max-width:600px}
"""


# ---------------------------------------------------------------------------------------------------------------
# The chapter's own examples, for the rotation tally and log (Rules 01.9, 01.10, 01.12)
# ---------------------------------------------------------------------------------------------------------------
DOMAINS = {
    "D01": "News, records and public information", "D02": "Elections and representation",
    "D03": "Money, lobbying and influence", "D04": "Congress, agencies and public services",
    "D05": "Checks on power and equal justice", "D06": "Competition and market power",
    "D07": "Work, pay and bargaining power", "D08": "Taxes, wealth and economic security",
    "D09": "Housing, health care and getting ahead", "D10": "Taking part, trust and shared norms",
}
EXAMPLES = [
    # (example, domain, state, level, coalition, illustrative, where)
    ("Who sets your electric rate", "D09", "Every state", "State", "No reform shown", False, "Explain piece; Rule 01.13"),
    ("The stock trading ban", "D03", "National", "Federal", "Survey majorities of both parties’ voters", False, "Track piece; Rules 01.2, 01.6, 01.20, 01.24"),
    ("A county road budget", "D04", "Alder County (invented)", "County or city", "No reform shown", True, "Connect piece"),
    ("Backyard cottages", "D09", "Alder County (invented)", "County or city", "Invented", True, "Act piece; Rules 01.8, 01.22"),
    ("Posting committee votes, S. 214", "D01", "Unnamed state (invented)", "State", "Invented", True, "Rules 01.1, 01.4, 01.23"),
    ("Mid-decade map redraws", "D02", "Texas and California", "State", "No reform shown", False, "Rule 01.11"),
    ("Citizen initiatives", "D02", "50 states and DC", "State", "No reform shown", False, "Rule 01.5"),
    ("Productivity and pay", "D07", "National", "Federal", "No reform shown", False, "Rule 01.16"),
    ("The cloture rule", "D04", "National", "Federal", "No reform shown", False, "Rule 01.17"),
    ("A state overtime rule", "D07", "Unnamed state (invented)", "State", "Invented", True, "Rule 01.15"),
    ("A school bell schedule", "D09", "Unnamed district (invented)", "School district", "Invented", True, "Rule 01.10"),
    ("How property tax rates are set", "D08", "Every state", "County or city", "No reform shown", False, "Rule 01.14"),
    ("A bus route hearing", "D04", "Unnamed city (invented)", "County or city", "No reform shown", True, "Rule 01.19"),
]


def tally():
    from collections import Counter
    n = len(EXAMPLES)
    dom = Counter(x[1] for x in EXAMPLES)
    named_states = Counter()
    for x in EXAMPLES:
        for s in ("Texas", "California"):
            if s in x[2]:
                named_states[s] += 1
    return n, dom, named_states


# ---------------------------------------------------------------------------------------------------------------
def build(book):
    """Write chapter 01's specimens into the book and return the chapter dictionary."""
    A = lambda sid, body, **kw: book.add(sid, body, chapter="01", **kw)
    rules = []

    # --- extras before Rule 01.1 -----------------------------------------------------------------------------
    rows = [("Mission", LOCKED["mission"], "understand", "improve"),
            ("Reader promise", LOCKED["promise"], "explain how a decision is made", "give you a practical way to take part"),
            ("Editorial commitment", LOCKED["commitment"], "clarity, our duty", "action, our promise"),
            ("Pillars", "Explain → Track → Connect → Act", "Explain, Track", "Connect, Act")]
    trs = "".join(f'<tr><th scope="row">{e(r)}<br><span class="lk">{e(q(l) if r != "Pillars" else l)}</span></th>'
                  f'<td>{e(c)}</td><td>{e(a)}</td></tr>' for r, l, c, a in rows)
    trs += (f'<tr><th scope="row">Tagline<br><span class="lk">{e(q(LOCKED["tagline"]))}</span></th>'
            f'<td colspan="2">It names the result when the hinge has turned and the loop closes: officials who answer to the people they serve.</td></tr>')
    A("s-01-hinge-lines", f'<div class="ed"><table><thead><tr><th scope="col">Locked line, exact</th><th scope="col">The commitment</th>'
      f'<th scope="col">The action</th></tr></thead><tbody>{trs}</tbody></table></div>',
      rule=None, interactive=True, label="The hinge in the locked lines",
      alt="A table of the locked lines. Each one splits at the hinge into a commitment and an action. Mission: understand, then improve. "
          "Reader promise: explain how a decision is made, then give you a practical way to take part. Editorial commitment: clarity, "
          "our duty, then action, our promise. Pillars: Explain and Track, then Connect and Act. The tagline names the result.",
      notes="From the brand strategy, section 1, approved at Gate 1 (S1). The hinge drawing is chapter 04's.")

    pillars = [
        ("01", "Explain", "Make the rules and their effects understandable.",
         ["Explainers, in the Reform 101 and The Oath series", "The atlas’s 16 question-first pathways, such as “Why did my rent go up?”",
          "Reports", "The weekly briefing newsletter", "Glossaries and primers"]),
        ("02", "Track", "Follow the decision and keep its record within reach.",
         ["Trackers, each named for its subject and dated “as of”", "The Dispatch and The Public Record series",
          "The atlas Register, the record-by-record view of each claim"]),
        ("03", "Connect", "Help people reach the office that decides and the evidence it decides on.",
         ["Guides and call scripts", "The Field Notes series", "The atlas’s view of who can act on each issue"]),
        ("04", "Act", "Give the reader a useful next step.",
         ["Act pieces, in two kinds: How to take part, and Our position", "Case studies, in the Proof It Works series",
          "The closing step on every explainer, tracker, report and newsletter issue"]),
    ]
    cards = "".join(f'<div class="pcol"><p class="pn">{n}</p><p class="pname">{e(p)}</p><p class="pjob">{e(j)}</p>'
                    f'<p class="lab">Products</p><ul>{"".join(f"<li>{e(x)}</li>" for x in prods)}</ul></div>'
                    for n, p, j, prods in pillars)
    PCSS = """
.ed .pills{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:24px 28px}
.ed .pcol{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}
.ed .pn{font:700 .9375rem/1 var(--oa-font-family-reading);font-variant-numeric:tabular-nums;color:var(--oa-color-text-secondary);margin:0 0 6px}
.ed .pname{font:800 2rem/1 var(--oa-font-family-display);letter-spacing:-.03em;margin:0 0 10px}
.ed .pjob{font-size:1.0625rem;line-height:1.45;margin:0 0 14px}
.ed .pcol ul{margin:0;padding-left:1.1em;font-size:.9375rem;line-height:1.45}.ed .pcol li{margin:0 0 6px}
"""
    A("s-01-pillars", f'<div class="ed"><div class="pills">{cards}</div></div>', css=(BASE, PCSS),
      rule=None, interactive=True, label="The four pillars, always in this order",
      alt="The four pillars in order with each pillar's job and products. 01 Explain: make the rules and their effects understandable. "
          "Explainers in the Reform 101 and The Oath series, the atlas's 16 question-first pathways, reports, the weekly briefing "
          "newsletter, glossaries and primers. 02 Track: follow the decision and keep its record within reach. Trackers, the Dispatch and "
          "The Public Record series, the atlas Register. 03 Connect: help people reach the office that decides and the evidence it "
          "decides on. Guides and call scripts, the Field Notes series, the atlas's view of who can act. 04 Act: give the reader a "
          "useful next step. Act pieces in two kinds, case studies in the Proof It Works series, and the closing step on every piece.",
      notes="Products named as the brand's set, with no launch dates or status (DR-91). Product placement follows the brand "
            "architecture table (strategy section 3, S2); series pillars follow V5's series routes. Connect's job line is new, since "
            "the V5 census cut its line at 50 characters.")

    A("s-01-pieces", f'''<div class="ed"><div class="grid4">
<div><p class="pl">Explain</p>{piece_explain()}</div>
<div><p class="pl">Track</p>{piece_track()}</div>
<div><p class="pl">Connect</p>{piece_connect()}</div>
<div><p class="pl">Act</p>{piece_act()}</div></div></div>''', css=(BASE, PIECE, STAGES),
      rule=None, illustrative=True, label="One piece from each pillar, at true size",
      alt="Four pieces at phone width, one per pillar, each turning at the hinge divider to What you can do and ending on one red "
          "ask button. Explain: an explainer, Why is my electric bill going up? A regulator or a board approves your rate; who decides; "
          "then find your rate case. Track: the Stock Trading Ban Tracker, as of October 15, 2026: passed the House 232 to 198 on "
          "July 22, 2026; the Senate vote to take it up failed 53 to 47 on September 30, 2026, short of 60; then follow this bill. "
          "Connect, illustrative: who answers for the repair on your street in Alder County, what to say in 90 seconds, then find "
          "your supervisor. Act, illustrative: Alder County votes on backyard cottages March 9; send a comment by March 3.",
      notes="Explain and Track use real atlas copy and records; Connect and Act are invented and labeled beside each invented item. "
            "Each card is 360 px wide, the phone width it ships at.")

    # --- Rules 01.1 to 01.20: the nonpartisan rule set (Gate 1, S7) -----------------------------------------
    vote_rows = lambda fail: [("Yes", 6, "ink", 9), ("No", 3, "red" if fail else "ctx", 9)]
    vt = "The Government Operations Committee sent S. 214 to the full senate, 6 to 3."
    vm = "Committee vote on S. 214, Tuesday, March 2, 2027."
    vbody = lambda fail: (bars(vote_rows(fail), vt, vm, "Illustrative committee and bill, invented for the specimen.")
                          .replace('<div class="ed vote">', '<div class="ed vote"><p class="kick"><span class="chip solid">Tracker</span>' + ill() + '</p>', 1)
                          .replace('</div><p class="src">', f'</div>{hinge()}<span class="ask" data-red="working">Follow S. 214</span><p class="src">', 1))
    KCSS = ".ed .kick{display:flex;gap:8px;align-items:center;margin:0 0 10px}"
    rules.append({
        "id": "01.1", "title": "Red never marks a party, a side or a person.",
        "rule": ["Pillar Red never stands for a party, one side of a debate or a named person, in a chart, a map, a label or a headline. "
                 "Each view gives its one working red to the job Rule 05.3 names, and none of those jobs is a side."],
        "tokens": ["oa.color.data.emphasis.onNewsprint", "oa.color.data.context.onNewsprint", "oa.color.action.ask.fill.onNewsprint"],
        "why": {"text": ["Election-night maps have taught readers to see red as one party. A red mark on a side tells a reader on the other "
                         "side that the piece is against them before they read a word, and they stop trusting the record we keep for everyone."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-1-correct", vbody(False), css=(BASE, CHART, KCSS), rule="01.1", illustrative=True,
                                  alt="An illustrative tracker card. The Government Operations Committee sent S. 214 to the full senate, 6 to 3. "
                                      "The yes bar is Charcoal and the no bar Stone, each with its count. After the hinge divider, one red button: Follow S. 214."),
                    "caption": "The votes sit in Charcoal and Stone with their counts printed. The view’s one working red goes to the step a reader can take now, the button that follows the bill."},
        "failure": {"specimen": A("s-01-1-failure", vbody(True), css=(BASE, CHART, KCSS), rule="01.1", illustrative=True, exempt=["red"],
                                  alt="The same tracker card with the no bar drawn in Pillar Red, so the card has two reds, one on a side of the vote."),
                    "caption": "Red on the no votes casts those three senators as the problem. A reader who agrees with them sees an attack, and the count stops reading as a record."},
        "specs": [{"label": "Working red", "value": "One job per view, in the order Rule 05.3 sets", "token": "oa.color.action.ask.fill.onNewsprint"},
                  {"label": "Sides of a vote", "value": "Charcoal and Stone, counts printed", "token": "oa.color.data.context.onNewsprint"}],
        "related": ["05", "14"],
        "builders": "Search the piece for Pillar Red and name each red mark’s job. If a mark stands for a party, a side or a person, redraw it in Charcoal or Stone.",
    })

    st = load(CHART_DATA)["datasets"]["stock-trading-ban"]["rows"]
    sv = {r["key"]: r["value"] for r in st}
    t2 = "Most Republicans and most Democrats favor a ban on stock trading by members of Congress."
    m2 = "Percent of registered voters who favor a ban, May 2023. Parties in alphabetical order."
    rules.append({
        "id": "01.2", "title": "Two sides take Charcoal and Stone, with their names printed.",
        "rule": ["When a chart or table compares two parties or two sides, draw one in Charcoal and the other in Stone, or one solid and "
                 "one in outline, and print each side’s name on its mark. Red never stands against blue or Verdigris."],
        "tokens": ["oa.color.data.emphasis.onNewsprint", "oa.color.data.context.onNewsprint"],
        "why": {"text": ["Red against blue reads as an election before it reads as data, and red against Verdigris stages the same contest in "
                         "other hues. Neutral inks with printed names let a reader see who is who without learning a color code, and they hold in grayscale."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-2-correct", bars([("Democrats", sv["support-democrats"], "ink", 100), ("Republicans", sv["support-republicans"], "ctx", 100)], t2, m2, SRC_STOCK_SURVEY),
                                  css=(BASE, CHART), rule="01.2",
                                  alt=f"Bar chart: {t2} Democrats 88 percent in Charcoal, Republicans 87 percent in Stone, each named beside its bar. {SRC_STOCK_SURVEY}"),
                    "caption": "Charcoal and Stone, with each party’s name beside its bar, show a finding of agreement as agreement."},
        "failure": {"specimen": A("s-01-2-failure", bars([("Democrats", sv["support-democrats"], "blue", 100), ("Republicans", sv["support-republicans"], "red", 100)], t2, m2, SRC_STOCK_SURVEY, names=False,
                                                         key=[("blue", "Democrats"), ("red", "Republicans")]),
                                  css=(BASE, CHART), rule="01.2", exempt=["red"],
                                  alt="The same chart with the Democrats' bar in Prussian blue and the Republicans' bar in Pillar Red, unlabeled, with a color key above."),
                    "caption": "Red and blue turn a finding of agreement into a contest, and the color key makes a reader match swatches to find each party, which fails in grayscale."},
        "specs": [{"label": "First side", "value": "Charcoal, solid", "token": "oa.color.data.emphasis.onNewsprint"},
                  {"label": "Second side", "value": "Stone, solid, or a Charcoal outline", "token": "oa.color.data.context.onNewsprint"},
                  {"label": "Names", "value": "Printed on or beside each mark, in the text ink"}],
        "related": ["05", "14"],
        "builders": "Pick the data emphasis and data context tokens for the two sides, never a palette color by name, and set each side’s name as a direct label.",
    })

    dk_ok = "".join(diverging_key(False))
    dk_bad = "".join(diverging_key(True))
    dtitle = '<p class="ct">Change since the last count, in percentage points</p><p class="cm">A key with no data behind it, shown for its colors and arrows.</p>'
    rules.append({
        "id": "01.3", "title": "A diverging scale runs from Prussian through the page color to Verdigris.",
        "rule": ["A scale that shows change in two directions runs from Prussian through Newsprint to Verdigris. A boxed arrow and a word "
                 "name each step’s direction, because the two hues lose their order in grayscale. Red and blue never form a diverging pair."],
        "tokens": [f"oa.chart.color.diverging.fill.step{i}.onNewsprint" for i in range(1, 6)],
        "why": {"text": ["Neither end of the pair belongs to a party, so a fall and a rise carry the same weight. The arrow and the word carry "
                         "the direction for a reader who sees no color at all."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-3-correct", f'<div class="ed dkw">{dtitle}<ul class="dk">{dk_ok}</ul></div>', css=(BASE, CHART, DIV), rule="01.3",
                                  alt="A five-step diverging key from Prussian through Newsprint to Verdigris. Each step has a boxed arrow and a word: down 2 points or more, down less than 2, no change, up less than 2, up 2 points or more."),
                    "caption": "Each step carries a boxed arrow and a word, so the key reads the same in grayscale."},
        "failure": {"specimen": A("s-01-3-failure", f'<div class="ed dkw">{dtitle}<ul class="dk">{dk_bad}</ul></div>', css=(BASE, CHART, DIV), rule="01.3", exempt=["red"],
                                  alt="The same key running from Pillar Red through Newsprint to Prussian blue, with no arrows."),
                    "caption": "A red-to-blue scale reads as one party’s gain against the other’s whatever it measures, and with no arrows its direction disappears in grayscale."},
        "specs": [{"label": "Steps", "value": "Five, step 1 the strongest fall, step 3 the page color", "token": "oa.chart.color.diverging.fill.step3.onNewsprint"},
                  {"label": "Direction", "value": "A boxed arrow in each step’s label ink, and a word"}],
        "related": ["05", "14"],
        "builders": "Use the five diverging steps in order and draw each arrow in the matching diverging label token, which the chart palette pairs with its fill.",
    })

    pr_bar = ('<div class="pbar"><p class="pt">Committees that posted every roll call last session ' + ill() + '</p>'
              '<div class="pb"><span style="width:30%"></span></div><p class="pv">6 of 20</p></div>')
    PRCSS = """
.ed.prus{padding:24px;max-width:520px}
.ed .pbar{margin-top:22px}.ed .pt{font-size:1rem;margin:0 0 8px}
.ed .pb{height:16px;border:1px solid var(--oa-color-data-emphasis)}.ed .pb span{display:block;height:100%;background:var(--oa-color-data-emphasis)}
.ed .pv{font:700 1rem/1.4 var(--oa-font-family-reading);font-variant-numeric:tabular-nums;margin-top:6px}
.ed .wm{display:block;height:24px;width:auto;color:var(--oa-color-text-primary)}
.ed .wm.redamp{--amp:var(--oa-color-palette-pillar-red)}
"""
    rules.append({
        "id": "01.4", "title": "On Prussian, identity marks turn White and data marks turn Newsprint.",
        "rule": ["On a Prussian ground, set every identity mark in one color, White, the ampersand included. Draw data graphics on Prussian "
                 "in Newsprint. Red never sits on Prussian."],
        "tokens": ["oa.color.identity.signature.onPrussian", "oa.color.data.emphasis.onPrussian"],
        "why": {"text": ["Pillar Red measures 3.19 to 1 against Prussian. At 16 px, where smoothing thins the strokes, the red ampersand measures "
                         "2.27 to 1 and a White one 8.27 to 1, so only White stays legible."],
                "basis": "WCAG 2.2 SC 1.4.11 Non-text Contrast"},
        "correct": {"specimen": A("s-01-4-correct", f'<div class="ed prus"><img data-inline src="{WORDMARK24_PRUSSIAN}" alt="Oath and Action" class="wm" height="24">{pr_bar}</div>',
                                  css=(BASE, PRCSS), rule="01.4", surface="prussian", illustrative=True,
                                  alt="A Prussian panel with the wordmark in White, ampersand included, at its 24 px master, and an illustrative bar in Newsprint: committees that posted every roll call last session, 6 of 20."),
                    "caption": "The wordmark and its ampersand turn White, and the bar turns Newsprint. The panel carries no red."},
        "failure": {"specimen": A("s-01-4-failure", f'<div class="ed prus"><img data-inline src="{WORDMARK24}" alt="Oath and Action" class="wm redamp" height="24" data-red="failure">{pr_bar}</div>',
                                  css=(BASE, PRCSS), rule="01.4", surface="prussian", illustrative=True, exempt=["contrast", "red"],
                                  alt="The same panel with the wordmark's ampersand in Pillar Red on Prussian."),
                    "caption": "The red ampersand sinks into the Prussian ground at 3.19 to 1, and at small sizes a reader loses the mark’s center."},
        "specs": [{"label": "Identity marks", "value": "White, one color", "token": "oa.color.identity.signature.onPrussian"},
                  {"label": "Data marks", "value": "Newsprint", "token": "oa.color.data.emphasis.onPrussian"}],
        "files": [WORDMARK24_PRUSSIAN],
        "related": ["03", "05"],
        "builders": "Inside a Prussian surface class, the identity signature token resolves to White and the data emphasis token to Newsprint. Never name the palette red there.",
    })

    svg_rule, cnt = tile_map("rule")
    key_rule = ('<ul class="mapk">'
                f'<li>{key_swatch("var(--oa-color-data-emphasis)")}<span>A working citizen initiative: {cnt["work"]} states and DC</span></li>'
                f'<li>{key_swatch("url(#hk)")}<span>In the constitution, unusable since a 2021 court ruling: Mississippi</span></li>'
                f'<li>{key_swatch("var(--oa-color-surface-newsprint)")}<span>No citizen initiative: {cnt["none"]} states</span></li></ul>')
    t5 = f"Citizens in {cnt['work']} states and DC have a working way to petition a proposed law or amendment onto the ballot."
    svg_win, cw = tile_map("winner")
    key_win = ('<ul class="mapk">'
               f'<li>{key_swatch("var(--oa-color-palette-pillar-red)", red=True)}<span>Won by the Republican nominee</span></li>'
               f'<li>{key_swatch("var(--oa-color-palette-prussian)")}<span>Won by the Democratic nominee</span></li></ul>')
    rules.append({
        "id": "01.5", "title": "Maps show a rule or a measure, never which party won a place.",
        "rule": ["Color a map by the rule, count or measure the story is about, never by which party won each place. Use the neutral palette "
                 "or a pattern, and set the key beside the map."],
        "tokens": ["oa.color.data.emphasis.onNewsprint", "oa.color.border.strong.onNewsprint"],
        "why": {"text": ["A map colored by winner splits the country into two camps and gives large, thinly settled states the most ink. A map of a "
                         "rule shows a reader whether the rule reaches the place where they live."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-5-correct", f'<div class="ed"><p class="ct">{e(t5)}</p><p class="cm">Statewide citizen-initiated measures, by state, as read November 6, 2026</p>'
                                                    f'<div class="mapw">{svg_rule}{key_rule}</div><p class="src">{e(SRC_INITIATIVE)}</p></div>',
                                  css=(BASE, CHART, MAP), rule="01.5", width=None,
                                  alt=f"Tile map of the 50 states and DC. {t5} Those tiles are solid Charcoal; Mississippi is hatched; the other {cnt['none']} states are open. Key beside the map. {SRC_INITIATIVE}"),
                    "caption": "Solid, hatched and open tiles show the rule, with the key beside the map and the source below it."},
        "failure": {"specimen": A("s-01-5-failure", f'<div class="ed"><p class="ct">The 2024 presidential vote, by state</p><p class="cm">Winner of each state</p>'
                                                    f'<div class="mapw">{svg_win}{key_win}</div><p class="src">{e(SRC_FEC)}</p></div>',
                                  css=(BASE, CHART, MAP), rule="01.5", exempt=["red"],
                                  alt=f"The same tile map colored by the 2024 presidential winner, {cw['rep']} tiles in Pillar Red and {cw['dem']} in Prussian blue. {SRC_FEC}"),
                    "caption": "Colored by winner, the map splits the country into two camps and says nothing about the rule a story covers."},
        "specs": [{"label": "Tile grid", "value": "12 columns by 8 rows, one square per state and DC"},
                  {"label": "Fills", "value": "Charcoal, a Charcoal hatch and open, keyed in words", "token": "oa.color.data.emphasis.onNewsprint"}],
        "files": [TILE_GRID],
        "related": ["14", "05"],
        "builders": "Start from the studio’s shared tile grid and join the story’s own measure to it by state code. A map of election results follows chapter 14’s rules, with party names printed.",
    })

    PH = """
.ed .ph{position:relative;aspect-ratio:3/2;width:100%;max-width:520px;border:1px solid var(--oa-color-border-strong);
background:repeating-linear-gradient(135deg,var(--oa-color-surface-newsprint) 0 10px,var(--oa-color-surface-white) 10px 20px);display:flex;align-items:flex-end}
.ed .ph .phl{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;background:var(--oa-color-surface-white);border-top:1px solid var(--oa-color-border-strong);border-right:1px solid var(--oa-color-border-strong);padding:6px 10px}
.ed .phc{font:var(--oa-type-caption);margin-top:8px;max-width:520px}
.ed .card{max-width:520px;border-top:4px solid var(--oa-color-border-strong);padding-top:14px;position:relative;overflow:hidden}
.ed .card .hl{font:800 1.75rem/1.1 var(--oa-font-family-display);letter-spacing:-.02em;margin:0 0 10px;position:relative;max-width:16ch}
.ed .card .dek{position:relative;max-width:40ch}
.ed .dome{position:absolute;right:-10px;top:10px;width:260px;height:auto;color:var(--oa-color-graphic-subtle)}
.ed .kick{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 10px}
"""
    ph = lambda cap: f'<div class="ph"><span class="phl">Photograph placeholder</span></div><p class="phc">{cap}</p>'
    dome = ('<svg class="dome" viewBox="0 0 260 200" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="3">'
            '<path d="M70 120 A60 60 0 0 1 190 120"/><path d="M60 120h140M55 132h150"/><path d="M130 60v-26M122 34h16"/>'
            '<path d="M80 132v52M100 132v52M120 132v52M140 132v52M160 132v52M180 132v52M40 186h180"/></svg>')
    rules.append({
        "id": "01.6", "title": "Domes, columns and flags appear only in a captioned photograph of that place.",
        "rule": ["Show a capitol dome, columns or a flag only inside a documentary photograph of that place or event, with a caption that "
                 "names it. Keep them out of icons, backgrounds and textures."],
        "why": {"text": ["Campaigns in both parties use the dome and the flag as shorthand for government. As decoration they stand for no rule, "
                         "office or event, so they give the reader nothing to check or act on."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-6-correct", '<div class="ed">' + ph("The doors of the U.S. Senate chamber on September 30, 2026, the day of the vote on the stock trading ban. Placeholder: photograph and credit to come.") + "</div>",
                                  css=(BASE, PH), rule="01.6",
                                  alt="A labeled photograph placeholder with its caption: the doors of the U.S. Senate chamber on September 30, 2026, the day of the vote on the stock trading ban. Photograph and credit to come."),
                    "caption": "The building appears only as the place where the vote happened, named in a caption, in a photograph still to be made."},
        "failure": {"specimen": A("s-01-6-failure", f'<div class="ed"><div class="card">{dome}<p class="kick"><span class="chip solid">Explainer</span></p>'
                                                    '<p class="hl">What the Senate vote on stock trading means for you</p><p class="dek">One vote, 53 to 47, and what comes next.</p></div></div>',
                                  css=(BASE, PH), rule="01.6",
                                  alt="An explainer card with a line drawing of a capitol dome and columns behind the headline, What the Senate vote on stock trading means for you."),
                    "caption": "The dome behind the headline decorates a story about one vote, names no office and borrows the look of campaign mail."},
        "related": ["16", "12"],
        "builders": "Build cards from type and the brand’s own devices. A dome, a column or a flag enters only with a documentary photograph, its caption and its credit.",
    })

    ballot = lambda fail: (f'<div class="ed"><div class="card"><p class="kick"><span class="chip solid">Explainer</span>{ill()}</p>'
                           '<p class="hl">What a yes vote and a no vote on Measure B would do</p>'
                           '<p class="dek">Alder County’s bond for road repairs, on the March 2027 ballot.</p>'
                           + ('<svg class="btn" viewBox="0 0 120 120" aria-hidden="true" focusable="false"><circle cx="60" cy="60" r="56" fill="var(--oa-color-surface-white)" stroke="currentColor" stroke-width="4"/>'
                              '<text x="60" y="56" text-anchor="middle" font-size="22" font-weight="800" font-family="var(--oa-font-family-display)" fill="currentColor">YES</text>'
                              '<text x="60" y="80" text-anchor="middle" font-size="16" font-weight="800" font-family="var(--oa-font-family-display)" fill="currentColor">ON B</text></svg>'
                              '<svg class="plac" viewBox="0 0 150 120" aria-hidden="true" focusable="false"><rect x="4" y="4" width="142" height="70" fill="var(--oa-color-surface-white)" stroke="currentColor" stroke-width="4"/>'
                              '<text x="75" y="48" text-anchor="middle" font-size="20" font-weight="800" font-family="var(--oa-font-family-display)" fill="currentColor">STOP THE TAX</text>'
                              '<path d="M75 74v44" stroke="currentColor" stroke-width="6"/></svg>' if fail else
                              '<div class="docref"><p class="lab">Document</p><p>Alder County, Measure B, ballot text and the county counsel’s summary, March 2027. ' + ill() + '</p></div>')
                           + "</div></div>")
    BCSS = """
.ed .btn{width:96px;height:96px;margin:8px 12px 0 0}.ed .plac{width:130px;height:104px;margin-top:8px}
.ed .docref{border:1px solid var(--oa-color-border-strong);background:var(--oa-color-surface-white);padding:12px 14px;margin-top:12px;max-width:44ch}
"""
    rules.append({
        "id": "01.7", "title": "Brand graphics carry no party symbols, candidate photos, campaign gear or protest slogans.",
        "rule": ["Keep party symbols, candidate photographs, campaign merchandise and legible protest slogans out of brand graphics, since each "
                 "takes a side the piece never argued. A party’s logo may appear as evidence, inside a sourced document the piece reproduces."],
        "why": {"text": ["A reader takes any symbol on our page as ours. A campaign button or a slogan placard reads as an endorsement, even when the story beside it is neutral."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-7-correct", ballot(False), css=(BASE, PH, BCSS), rule="01.7", illustrative=True,
                                  alt="An illustrative explainer card: What a yes vote and a no vote on Measure B would do. Below it, a document reference to the measure's ballot text and the county counsel's summary."),
                    "caption": "The card explains both votes and points to the ballot text as its document."},
        "failure": {"specimen": A("s-01-7-failure", ballot(True), css=(BASE, PH, BCSS), rule="01.7", illustrative=True,
                                  alt="The same card with a campaign button reading YES ON B and a protest placard reading STOP THE TAX."),
                    "caption": "The button and the placard take sides on a measure the card set out to explain, so a reader on either side stops at the picture."},
        "related": ["16", "23"],
        "builders": "When a story needs a party’s logo or a campaign’s material, place the whole document as a sourced image with its credit, never the symbol by itself.",
    })

    rules.append({
        "id": "01.8", "title": "Photographs show people doing public work, with who, what, where and when in the caption.",
        "rule": ["Choose photographs of people of different ages, places and roles doing public work, officials among them. Every caption "
                 "names who is shown, what they are doing, where and when."],
        "why": {"text": ["A reader trusts a picture of a real hearing more than a picture of the idea of one, and a full caption lets them check it."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-8-correct", '<div class="ed">' + ph("A county planner answers residents’ questions about backyard cottages before the Alder County Board of Supervisors votes, 6 p.m. Tuesday, March 9, 2027. " + ill()) + "</div>",
                                  css=(BASE, PH), rule="01.8", illustrative=True,
                                  alt="A labeled photograph placeholder with an illustrative caption naming who, what, where and when: a county planner answers residents' questions about backyard cottages before the Alder County Board of Supervisors votes, 6 p.m. Tuesday, March 9, 2027."),
                    "caption": "The caption names the person by role, the act, the place and the time."},
        "failure": {"specimen": A("s-01-8-failure", '<div class="ed">' + ph("Democracy in action. " + ill()) + "</div>",
                                  css=(BASE, PH), rule="01.8", illustrative=True,
                                  alt="The same placeholder captioned only Democracy in action."),
                    "caption": "The caption names no person, act, place or date, so a reader cannot check the picture and learns nothing from it."},
        "related": ["16"],
        "builders": "Write the caption’s four parts before a photograph goes in: who, what, where and when. Until the photography direction is settled, use a labeled placeholder.",
    })

    n, dom, states = tally()
    TCSS = ".ed .tal{max-width:640px}.ed .tal td.c{font-variant-numeric:tabular-nums;white-space:nowrap}.ed .tal .bar1{display:inline-block;height:10px;background:var(--oa-color-data-emphasis);vertical-align:0}"
    trs = "".join(f'<tr><td>{e(DOMAINS[d])}</td><td class="c">{dom[d]} of {n}</td><td class="c"><span class="bar1" style="width:{dom[d] * 14}px"></span></td></tr>'
                  for d in sorted(dom, key=lambda k: (-dom[k], k)))
    limit = n / 4
    tal_ok = (f'<div class="ed tal"><p class="ct">This chapter’s {n} examples by atlas domain</p><p class="cm">The limit is one in four, {limit:g} of {n}. '
              f'The only named states, Texas and California, supply one example each.</p><table><thead><tr><th scope="col">Domain</th><th scope="col">Examples</th><th scope="col"><span class="vh">Bar</span></th></tr></thead><tbody>{trs}</tbody></table></div>')
    bad = [("Elections and representation", 3), ("Money, lobbying and influence", 1), ("Taxes, wealth and economic security", 1)]
    tal_bad = ('<div class="ed tal"><p class="ct">A draft chapter’s five examples by domain and state ' + ill() + '</p><p class="cm">Three of five come from one domain, and three of five from Massachusetts.</p><table><thead><tr><th scope="col">Domain</th><th scope="col">Examples</th><th scope="col">From Massachusetts</th></tr></thead><tbody>'
               + "".join(f'<tr><td>{e(a)}</td><td class="c">{b} of 5</td><td class="c">{["3", "0", "0"][i]}</td></tr>' for i, (a, b) in enumerate(bad)) + "</tbody></table></div>")
    rules.append({
        "id": "01.9", "title": "No atlas domain supplies more than one example in four, and no state more than one in five.",
        "rule": ["Within a chapter, draw no more than one example in four from any one of the atlas’s ten domains, and no more than one in five "
                 "from any one state. Massachusetts examples may appear on the same terms as any other state’s."],
        "why": {"text": ["A run of examples from one subject or one state tells readers whose problems we care about. Rotation keeps a reader in "
                         "Texas and a reader in Maine in view of the same chapter."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-9-correct", tal_ok, css=(BASE, CHART, TCSS + ".ed .vh{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}"), rule="01.9",
                                  alt=f"A table of this chapter's {n} examples by atlas domain. The largest counts are 3 of {n}, under the one-in-four limit. " +
                                      "; ".join(f"{DOMAINS[d]}: {dom[d]}" for d in sorted(dom))),
                    "caption": f"This chapter checked against its own rule: no domain passes {limit:g} of {n} examples, and no state supplies more than one."},
        "failure": {"specimen": A("s-01-9-failure", tal_bad, css=(BASE, CHART, TCSS), rule="01.9", illustrative=True,
                                  alt="An illustrative tally of a draft chapter's five examples: three from elections and representation, and three from Massachusetts."),
                    "caption": "Three election examples from one state would tell readers elsewhere that the chapter was written for someone else."},
        "related": ["13"],
        "builders": "Count from the rotation log before a chapter goes to review, using the atlas’s ten domains by their full names.",
    })

    LCSS = ".ed .lv{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:16px;max-width:720px}.ed .lv div{border-top:2px solid var(--oa-color-border-strong);padding-top:8px}.ed .lv .lab{margin-bottom:4px}.ed .lv p+p{font-size:.9375rem;margin-top:4px}"
    lv_ok = ('<div class="ed"><div class="lv">'
             '<div><p class="lab">Federal</p><p>The stock trading ban in Congress</p><p>The cloture rule</p></div>'
             '<div><p class="lab">State</p><p>Map redraws in Texas and California</p><p>Posting committee votes ' + ill() + '</p></div>'
             '<div><p class="lab">County or city</p><p>Backyard cottages in Alder County ' + ill() + '</p><p>Property tax rates</p></div>'
             '<div><p class="lab">School district</p><p>A bell schedule vote ' + ill() + '</p></div></div></div>')
    lv_bad = ('<div class="ed"><div class="lv">'
              '<div><p class="lab">Federal</p><p>The cloture rule</p><p>The stock trading ban</p><p>The debt limit</p><p>Medicare drug prices</p></div>'
              '<div><p class="lab">State</p><p>None</p></div><div><p class="lab">County or city</p><p>None</p></div><div><p class="lab">School district</p><p>None</p></div></div></div>')
    rules.append({
        "id": "01.10", "title": "Examples rotate across levels of government and regions.",
        "rule": ["Draw examples from federal, state, county or city, and school district decisions, and from every region of the country."],
        "why": {"text": ["Most of the rules that reach a household are written below the federal level. A reader who only ever sees Congress learns that the decisions nearest to them are not worth following."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-10-correct", lv_ok, css=(BASE, LCSS), rule="01.10",
                                  alt="This chapter's examples sorted by level. Federal: the stock trading ban, the cloture rule. State: map redraws in Texas and California, posting committee votes (illustrative). County or city: backyard cottages in Alder County (illustrative), property tax rates. School district: a bell schedule vote (illustrative)."),
                    "caption": "This chapter’s examples reach all four levels, with real cases from Texas, California and Congress beside the invented county."},
        "failure": {"specimen": A("s-01-10-failure", lv_bad, css=(BASE, LCSS), rule="01.10",
                                  alt="A draft chapter with four federal examples and none at the state, county or city, or school district level."),
                    "caption": "Four federal examples in a row leave out the councils, boards and districts where a reader can most easily be heard."},
        "related": ["13", "21"],
        "builders": "Tag each row of the rotation log with its level, and look for an empty level before review.",
    })

    CASES = """
.ed .cases{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px 28px;max-width:720px}
.ed .cases div{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}
.ed .cases .st{font:800 1.25rem/1.2 var(--oa-font-family-display);margin:0 0 6px}
"""
    tx = "In August 2025, the Republican-led legislature redrew the congressional map, aiming at five more Republican seats."
    ca = "In November 2025, voters approved Proposition 50, which put in place a congressional map drawn to favor Democrats."
    lead11 = '<p class="ct">Loop R4a, the map-drawing loop: majorities draw maps that help them keep control.</p>'
    rules.append({
        "id": "01.11", "title": "When majorities of both parties use a mechanism, show a case from each.",
        "rule": ["When majorities of either party use the same mechanism, show a documented case from each, at the same length. The test case is "
                 "Loop R4a, the map-drawing loop, which the atlas titles “Majorities draw maps that help them keep control.”"],
        "why": {"text": ["A mechanism shown through one party’s case reads as a charge against that party. A case from each side shows the mechanism itself, which is what a reader can change."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-11-correct", f'<div class="ed">{lead11}<div class="cases"><div><p class="st">Texas</p><p>{e(tx)}</p></div>'
                                                     f'<div><p class="st">California</p><p>{e(ca)}</p></div></div><p class="src">{e(SRC_R4A)}</p></div>',
                                  css=(BASE, CHART, CASES), rule="01.11",
                                  alt=f"Loop R4a, the map-drawing loop. Two cases at the same length. Texas: {tx} California: {ca} {SRC_R4A}"),
                    "caption": "One case from a Republican majority and one from a Democratic majority, at the same length, show the loop as a mechanism both sides use."},
        "failure": {"specimen": A("s-01-11-failure", f'<div class="ed">{lead11}<div class="cases"><div><p class="st">Texas</p><p>{e(tx)}</p></div></div><p class="src">{e(SRC_R4A)}</p></div>',
                                  css=(BASE, CHART, CASES), rule="01.11",
                                  alt=f"The same loop with only the Texas case: {tx}"),
                    "caption": "With one party’s case alone, the loop reads as a charge against that party, and a reader who votes for it stops at the first line."},
        "related": ["15", "13"],
        "builders": "Before a piece runs a mechanism, list the party of the majority in each of the atlas’s case records for that loop, and pick one case from each.",
    })

    log_rows = [x for x in EXAMPLES if x[0] in ("The stock trading ban", "Posting committee votes, S. 214", "Mid-decade map redraws", "Citizen initiatives", "Backyard cottages")]
    log_ok = ('<div class="ed tal"><p class="ct">Rotation log, chapter 01, five of its 13 rows</p><table><thead><tr><th scope="col">Example</th><th scope="col">Domain</th>'
              '<th scope="col">State</th><th scope="col">Level</th><th scope="col">Coalition behind any reform shown</th></tr></thead><tbody>'
              + "".join(f'<tr><td>{e(a)}</td><td>{e(DOMAINS[d])}</td><td>{e(s)}</td><td>{e(l)}</td><td>{e(c)}</td></tr>' for a, d, s, l, c, _, _ in log_rows)
              + "</tbody></table></div>")
    log_bad = ('<div class="ed tal"><p class="ct">Rotation log, a draft row ' + ill() + '</p><table><thead><tr><th scope="col">Example</th><th scope="col">Domain</th>'
               '<th scope="col">State</th><th scope="col">Level</th><th scope="col">Coalition behind any reform shown</th></tr></thead><tbody>'
               '<tr><td>Open primaries</td><td>(blank)</td><td>Massachusetts</td><td>(blank)</td><td>(blank)</td></tr></tbody></table></div>')
    rules.append({
        "id": "01.12", "title": "A rotation log records each example’s domain, state, level and backing coalition.",
        "rule": ["Log every example with its atlas domain, its state, its level of government and, for any reform shown, the coalition that "
                 "usually backs it. The studio reviews the log at each gate."],
        "why": {"text": ["Balance across a chapter is easy to feel and hard to see. A log turns it into counts anyone can check, including a reader who suspects a lean."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-12-correct", log_ok, css=(BASE, CHART, TCSS), rule="01.12", interactive=True,
                                  alt="A rotation log table with five of this chapter's rows, each with example, domain, state, level and the coalition behind any reform shown."),
                    "caption": "Every field is filled, and an invented example says so in the coalition column."},
        "failure": {"specimen": A("s-01-12-failure", log_bad, css=(BASE, CHART, TCSS), rule="01.12", illustrative=True,
                                  alt="An illustrative log row for open primaries in Massachusetts with the domain, level and coalition left blank."),
                    "caption": "A row with blank fields cannot be counted, so the gate review cannot see a run of one topic or one side’s reforms."},
        "related": ["13", "28"],
        "builders": "Keep one log row per example in the chapter’s notes and count domains and states from it before review.",
    })

    LINES = """
.ed .ln{font:600 clamp(1.25rem,1.1rem + .6vw,1.5rem)/1.35 var(--oa-font-family-reading);max-width:34ch;margin:0}
.ed .ln+.src{margin-top:10px}
.ed .lnbox{max-width:620px;border-top:2px solid var(--oa-color-border-strong);padding-top:12px}
"""
    line = lambda t, src="", illus=False: (f'<div class="ed"><div class="lnbox"><p class="ln">{e(t)}{" " + ill() if illus else ""}</p>'
                                           + (f'<p class="src">{e(src)}</p>' if src else "") + "</div></div>")
    t13 = "For an investor-owned utility, the state public utility commission sets your rate in a rate case, its formal review of the utility’s request."
    rules.append({
        "id": "01.13", "title": "Name the office that decides, and name a party only when party is the mechanism.",
        "rule": ["Say which office or body makes the decision. Name a party only when party is part of how the decision works, such as a party-line "
                 "vote, and give the count and its source."],
        "why": {"text": ["A reader can call an office, testify before it or vote its members out. A party’s name in place of an office gives them a team to blame and nobody to call."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-13-correct", line(t13, SRC_ELECTRIC), css=(BASE, LINES), rule="01.13", alt=f"{t13} {SRC_ELECTRIC}"),
                    "caption": "The sentence names the commission and the hearing where it decides, so a reader knows where to look."},
        "failure": {"specimen": A("s-01-13-failure", line("Politicians raised your electric bill again.", illus=True), css=(BASE, LINES), rule="01.13", illustrative=True,
                                  alt="An illustrative line: Politicians raised your electric bill again."),
                    "caption": "“Politicians” names no office, so the reader has no one to call, and “again” supplies a grievance the record does not show."},
        "related": ["02", "13"],
        "builders": "Search a draft for “politicians”, “Washington”, “lawmakers” and party names, and replace each with the office that holds the decision.",
    })

    rules.append({
        "id": "01.14", "title": "Ask questions a supporter of the current rule could ask too.",
        "rule": ["Leave grievance words out of headlines, questions and calls to act, such as “rigged”, “broken”, “crisis” and “the rule you are "
                 "angry about”. Write each question so a person who supports the current rule could ask it too."],
        "why": {"text": ["A question that assumes the reader is angry tells half our readers the piece is not for them. A plain question about who decided, and when it could change, works for every reader."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-14-correct", line("Who sets your property tax rate, and when could it change?"), css=(BASE, LINES), rule="01.14",
                                  alt="A headline question: Who sets your property tax rate, and when could it change?"),
                    "caption": "A homeowner who likes today’s rate and one who wants it lower would both click this question."},
        "failure": {"specimen": A("s-01-14-failure", line("Who wrote the rule you are angry about?", "Our brand guide, fifth edition, chapter 13 In use"), css=(BASE, LINES), rule="01.14",
                                  alt="A headline question quoted from our brand guide's fifth edition, chapter 13: Who wrote the rule you are angry about?"),
                    "caption": "The question assumes the reader is angry and that someone wronged them, so a reader who likes the rule has no reason to read on."},
        "related": ["02", "23"],
        "builders": "Search a draft for the words this rule lists, and read each question as someone who likes the current rule would.",
    })

    KK = ".ed .kk{display:flex;flex-wrap:wrap;gap:6px;align-items:center;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;margin:0 0 10px}.ed .kk .sl{color:var(--oa-color-text-secondary)}"
    disp = lambda series, head: (f'<div class="ed"><div class="lnbox"><p class="kk"><b>{e(series)}</b><span class="sl">/</span><span>State overtime rule</span>{ill()}</p>'
                                 f'<p class="ln">{e(head)}</p></div></div>')
    rules.append({
        "id": "01.15", "title": "Use plain verbs in place of war and sports metaphors.",
        "rule": ["Describe a public decision in the words for what happens, such as propose, debate, vote and pass. Leave out war and sports "
                 "metaphors such as fight, battle, front and game plan."],
        "why": {"text": ["A war or a game needs an enemy or a loser, and the people on the other side of a vote are our readers too. The verbs for what happens also tell a reader where the decision stands."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-15-correct", disp("Dispatch", "The state senate votes on the overtime rule Thursday."), css=(BASE, LINES, KK), rule="01.15", illustrative=True,
                                  alt="A Dispatch kicker and an illustrative headline: The state senate votes on the overtime rule Thursday."),
                    "caption": "The series name is Dispatch, and the headline names the vote and its day."},
        "failure": {"specimen": A("s-01-15-failure", disp("Dispatch from the Front", "The battle over overtime heads to the senate floor."), css=(BASE, LINES, KK), rule="01.15", illustrative=True,
                                  alt="The fifth edition's series name, Dispatch from the Front, over an illustrative headline: The battle over overtime heads to the senate floor."),
                    "caption": "“From the Front” and “battle” cast the vote as a war with an enemy, and the headline never says when the vote happens."},
        "related": ["02"],
        "builders": "Search a draft for fight, battle, front, war and game plan, and name the step in the process in its place.",
    })

    ra = "Economists Anna Stansbury and Lawrence Summers find that average pay still rises with productivity, by most or all of each gain, in their estimates."
    rb = "The Economic Policy Institute, an advocacy group, finds that typical workers’ pay has risen far more slowly than productivity since 1979, in its measures."
    RCSS = """
.ed .rd{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px 28px;max-width:720px}
.ed .rd div{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}
.ed .rd .small{font-size:.875rem;color:var(--oa-color-text-secondary);border-top-width:1px}
"""
    lead16 = '<p class="ct">Does pay rise with productivity?</p><p class="cm">Credible studies disagree. Two readings, at the same length.</p>'
    rules.append({
        "id": "01.16", "title": "Show both readings of a contested claim at the same length.",
        "rule": ["When credible studies disagree, give each reading the same length, the same verb and the same type, and name who holds it."],
        "why": {"text": ["Equal space is how a reader sees that the disagreement is real. A long reading beside a short dismissal tells them which side we prefer before they weigh either."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-16-correct", f'<div class="ed">{lead16}<div class="rd"><div><p class="lab">One reading</p><p>{e(ra)}</p></div><div><p class="lab">The other reading</p><p>{e(rb)}</p></div></div><p class="src">{e(SRC_PAY)}</p></div>',
                                  css=(BASE, CHART, RCSS), rule="01.16",
                                  alt=f"Does pay rise with productivity? Two readings at the same length, 24 words each, in the same type. One: {ra} The other: {rb} {SRC_PAY}"),
                    "caption": "Each reading runs 24 words, uses the verb “finds” and names who holds it."},
        "failure": {"specimen": A("s-01-16-failure", f'<div class="ed">{lead16}<div class="rd"><div><p class="lab">What the research shows</p><p>{e(ra)}</p></div><div class="small"><p>Some critics disagree.</p></div></div></div>',
                                  css=(BASE, CHART, RCSS), rule="01.16",
                                  alt=f"The first reading set in full under the label What the research shows, and the second cut to three words in small gray type: Some critics disagree."),
                    "caption": "One reading becomes “the research” and the other three small words, so the layout settles a question the evidence leaves open."},
        "related": ["13", "14"],
        "builders": "Set both readings in one two-column block with matching labels and count their words before you publish.",
    })

    rules.append({
        "id": "01.17", "title": "Describe a rule so its supporters would accept the description.",
        "rule": ["Read your description of a rule as someone who supports it would. If they would object to the words, rewrite the description "
                 "until they would accept it, and save the argument for a labeled position piece."],
        "why": {"text": ["Readers who back a rule are among the people we serve, and many are the officials a reader is asked to contact. A description both sides accept is one both sides can use."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-17-correct", line("Cloture, a Senate vote to end debate, takes 60 votes for most legislation.", SRC_CLOTURE), css=(BASE, LINES), rule="01.17",
                                  alt=f"Cloture, a Senate vote to end debate, takes 60 votes for most legislation. {SRC_CLOTURE}"),
                    "caption": "A senator who values the 60-vote rule and one who wants it gone would both sign off on this sentence."},
        "failure": {"specimen": A("s-01-17-failure", line("The filibuster lets a minority of senators hold the country hostage.", illus=True), css=(BASE, LINES), rule="01.17", illustrative=True,
                                  alt="An illustrative line: The filibuster lets a minority of senators hold the country hostage."),
                    "caption": "“Hold the country hostage” is an opponent’s charge, so a senator who values the rule would reject the sentence before reaching the facts."},
        "related": ["13", "02"],
        "builders": "Before review, read the description in the place of someone who supports the rule, and mark every word they would change.",
    })

    hh = lambda a, b, fail=False: (f'<div class="ed"><p class="hh">{e(a)} {amp_h()} '
                                   + (f'<span style="color:var(--oa-color-palette-pillar-red)" data-red="failure">{e(b)}</span>' if fail else e(b)) + "</p></div>")
    rules.append({
        "id": "01.18", "title": "Both halves of a hinge pair share one color and weight, and only the ampersand is red.",
        "rule": ["Set both noun phrases of a hinge headline in the same ink, face and weight. Only the ampersand takes red, as the view’s working red."],
        "tokens": ["oa.font.family.display", "oa.color.palette.pillarRed"],
        "why": {"text": ["When one half is red or heavier, the headline takes a side between a rule and its result. Equal halves leave the joining to the ampersand."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-18-correct", hh("The overtime rule", "the paycheck."), css=(BASE, HL), rule="01.18",
                                  alt="A hinge headline: The overtime rule and the paycheck. Both halves in Charcoal Inter Tight ExtraBold; only ampersand B is red."),
                    "caption": "Both halves share Charcoal and ExtraBold, and ampersand B carries the red."},
        "failure": {"specimen": A("s-01-18-failure", hh("The overtime rule", "the paycheck.", True), css=(BASE, HL), rule="01.18", exempt=["red"],
                                  alt="The same headline with the second half, the paycheck, also set in red."),
                    "caption": "The red second half reads as the alarm and the first half as its cause, and the ampersand no longer stands out as the join."},
        "files": [AMP_DISPLAY],
        "related": ["04", "02"],
        "builders": "Set the headline in Inter Tight ExtraBold and place ampersand B’s display master at the cap height in place of the font’s ampersand. Chapter 04 gives the sizes.",
    })

    PP = ".ed .pp{display:grid;gap:18px}.ed .pp .lab{margin:0}"
    rules.append({
        "id": "01.19", "title": "People pairs join people through a shared rule or place, and their order rotates.",
        "rule": ["When a hinge headline joins two people or groups, join them through a rule or a place they share. Swap their order from one "
                 "piece to the next, so neither always comes first."],
        "why": {"text": ["The ampersand stands for common ground, and people stand on it through something they share. A fixed order would rank one group above the other."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-19-correct", f'<div class="ed pp"><div><p class="lab">One piece</p><p class="hh">The bus rider {amp_h()} the driver on one route.</p></div>'
                                                     f'<div><p class="lab">The next piece</p><p class="hh">The driver {amp_h()} the bus rider at one hearing.</p></div></div>',
                                  css=(BASE, HL, PP), rule="01.19",
                                  alt="Two hinge headlines from two pieces. One: The bus rider and the driver on one route. The next: The driver and the bus rider at one hearing. The order swaps, and each pair shares a route or a hearing."),
                    "caption": "The rider and the driver share a route, then a hearing, and the next piece puts the driver first."},
        "failure": {"specimen": A("s-01-19-failure", f'<div class="ed"><p class="hh">Us {amp_h()} them.</p></div>', css=(BASE, HL), rule="01.19",
                                  alt="A hinge headline: Us and them."),
                    "caption": "“Us” and “them” name two sides with nothing shared between them, so the ampersand marks a divide."},
        "related": ["04", "02"],
        "builders": "Log the order of each people pair, and swap it the next time a piece joins the same two groups.",
    })

    dek20 = f"In a May 2023 survey, {sv['support-republicans']} percent of Republicans and {sv['support-democrats']} percent of Democrats favored a ban on stock trading by members of Congress."
    rules.append({
        "id": "01.20", "title": "Party names, “left” and “right” enter a hinge headline only to report sourced agreement.",
        "rule": ["Use “left”, “right” or a party’s name in a hinge headline only to report a point where the sides agree, such as a bill with "
                 "sponsors from both parties, and source the agreement in the deck."],
        "why": {"text": ["A red ampersand between two sides would mark the sides themselves, against Rule 01.1. Reporting agreement is the one case where naming the sides helps a reader."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-20-correct", f'<div class="ed"><p class="hh">Both parties’ voters {amp_h()} the stock trading ban.</p><p class="dk2">{e(dek20)}</p><p class="src">{e(SRC_STOCK_SURVEY)}</p></div>',
                                  css=(BASE, HL, ".ed .dk2{font-size:1.125rem;max-width:44ch;margin-top:10px}"), rule="01.20",
                                  alt=f"A hinge headline: Both parties' voters and the stock trading ban. Deck: {dek20} {SRC_STOCK_SURVEY}"),
                    "caption": "The headline names both parties’ voters to report a point of agreement, and the deck gives the figures and their source."},
        "failure": {"specimen": A("s-01-20-failure", f'<div class="ed"><p class="hh">The left {amp_h()} the right.</p></div>', css=(BASE, HL), rule="01.20",
                                  alt="A hinge headline: The left and the right."),
                    "caption": "The red ampersand sits between two sides with no shared fact, so it marks the divide and reports nothing."},
        "related": ["04", "02"],
        "builders": "When a headline names the sides, link the deck’s source line to the vote, the sponsor list or the survey that shows the agreement.",
    })

    # --- Rules 01.21 to 01.24: content labels, the two Act kinds, product names ------------------------------
    KCSS2 = ".ed .kl{display:grid;gap:12px;max-width:520px}.ed .kl p{display:flex;flex-wrap:wrap;gap:8px;align-items:center;border-top:1px solid var(--oa-color-border-hairline);padding-top:10px}.ed .kl .t{font-size:1rem}"
    kl = [("chip solid", "Explainer", "Why is my electric bill going up?"), ("chip solid", "Tracker", "Stock Trading Ban Tracker"),
          ("chip solid", "Analysis", "Does pay rise with productivity?"), ("chip solid", "Report", "How state committees record their votes"),
          ("chip", "Act · How to take part", "Alder County votes on backyard cottages March 9."),
          ("chip solid", "Our position", "State senate committees should post every vote within two days.")]
    kl_ok = '<div class="ed"><div class="kl">' + "".join(
        f'<p><span class="{c}">{e(t)}</span>{"<span class=\"k\">Act</span>" if t == "Our position" else ""}<span class="t">{e(h)}</span>'
        f'{" " + ill() if i >= 3 else ""}</p>' for i, (c, t, h) in enumerate(kl)) + "</div></div>"
    kl_bad = ('<div class="ed"><div class="kl"><p><span class="chip solid">Must read</span><span class="chip">Breaking</span><span class="t">State senate committees should post every vote within two days.</span> '
              + ill() + '</p></div></div>')
    rules.append({
        "id": "01.21", "title": "Every piece carries one content label in its kicker.",
        "rule": ["Open the kicker, the short line above a headline, with one content label: Explainer, Tracker, Analysis, Report, Act · How to "
                 "take part, or Our position. A series name may follow the label."],
        "tokens": ["oa.color.action.primary.fill.onNewsprint"],
        "why": {"text": ["The label tells a reader what kind of claim the piece makes before they read it, and whether we are reporting or arguing."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-21-correct", kl_ok, css=(BASE, KCSS2), rule="01.21", illustrative=True,
                                  alt="Six kickers, one per content label, each with a headline: Explainer, Tracker, Analysis, Report, Act · How to take part, and Our position followed by Act. The last three headlines are illustrative."),
                    "caption": "Each kicker opens with its one label. A position piece’s label comes first and fills with Charcoal."},
        "failure": {"specimen": A("s-01-21-failure", kl_bad, css=(BASE, KCSS2), rule="01.21", illustrative=True,
                                  alt="An illustrative kicker reading Must read and Breaking above a position headline, with no content label."),
                    "caption": "“Must read” and “Breaking” push the reader and never say that the headline argues a position."},
        "related": ["13", "09"],
        "builders": "Pick the label from the six in this rule. A piece that fits none of them needs a ruling before it runs.",
    })

    rules.append({
        "id": "01.22", "title": "A process piece names the step and leaves the side to the reader.",
        "rule": ["An Act piece labeled “Act · How to take part” gives one step with its date and place, sets out what supporters and opponents "
                 "have said at the same length, and takes no side. Its ask is the view’s one working red."],
        "tokens": ["oa.color.action.ask.fill.onNewsprint", "oa.color.action.ask.label.onNewsprint", "oa.component.button.ask.keyline.onNewsprint"],
        "why": {"text": ["A reader of any view can use a process piece, because it tells them how to be heard and leaves what to say to them."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-22-correct", f'<div class="ed">{process_piece(False)}</div>', css=(BASE, ARTICLE), rule="01.22", illustrative=True,
                                  alt="An illustrative process piece at the site's reading width. Kicker: Act · How to take part. Headline: Alder County votes on backyard cottages March 9. Send a comment by March 3 or speak at the meeting. Who decides: five county supervisors, and three votes pass the change. What each side has said: supporters said more homes would ease rents; opponents said sewers were sized for fewer homes. After the hinge divider, What you can do: send a written comment by 5 p.m. Wednesday, March 3, 2027, or speak for two minutes at 6 p.m. Tuesday, March 9, 2027. One red button: Send a comment. A link to the Accessory Homes Tracker."),
                    "caption": "The piece names who decides, gives both sides one sentence each, then turns at the hinge divider to two dated ways to take part. The red sits on the ask alone."},
        "failure": {"specimen": A("s-01-22-failure", f'<div class="ed">{process_piece(True)}</div>', css=(BASE, ARTICLE), rule="01.22", illustrative=True,
                                  alt="The same piece with only the supporters' case, under the label Why it matters, and a red button reading Tell the supervisors to vote yes."),
                    "caption": "The piece keeps the process label and then argues one side, so a reader who opposes the change meets a position they were told was not there."},
        "specs": [{"label": "Kicker", "value": "Act · How to take part, in plain type"},
                  {"label": "Ask", "value": "Pillar Red fill, White label at 19 px bold, Charcoal keyline on Newsprint", "token": "oa.color.action.ask.fill.onNewsprint"},
                  {"label": "Before the ask", "value": "The hinge divider, its ampersand in the surface’s ink", "token": "oa.color.identity.hingeDivider.onNewsprint"},
                  {"label": "Width", "value": "640 px reading column, reflowing to a phone"}],
        "related": ["13", "12", "18"],
        "builders": "Build the ending from the hinge divider, the “What you can do” heading and one ask button. Link the neutral tracker, never a campaign page.",
    })

    kit = [("Label first", "“Our position” opens the kicker, before the headline, and a shared card keeps it top left."),
           ("The strongest case against", "The opposing case as its supporters would put it, sourced, at least a third of the argument’s length."),
           ("Grades kept", "Every claim keeps its evidence grade, and its verb matches the grade."),
           ("Opponents by role", "Opponents are named by office or role, never by party as a villain."),
           ("What we don’t know", "The open questions, named."),
           ("Process facts", "Who decides, when and how, word for word as the neutral tracker gives them."),
           ("Disclosure", "Who decided the position, the date and any funder interest, above the ask, with the public position log."),
           ("Never in the record", "Positions never appear in the atlas, the trackers or the data.")]
    rules.append({
        "id": "01.23", "title": "A position piece wears its label before the headline and its fairness kit before the ask.",
        "rule": ["A piece that asks readers to support or oppose a named measure opens its kicker with the label “Our position”, before the "
                 "headline. Before the ask it gives the strongest case against the position, what we don’t know and a disclosure of who decided."],
        "tokens": ["oa.color.action.primary.fill.onNewsprint", "oa.color.action.ask.fill.onNewsprint"],
        "why": {"text": ["A reader who disagrees with us can still trust the rest of our coverage when every argument is labeled, answered by its strongest opposing case and logged."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-23-correct", f'<div class="ed">{position_piece(False)}</div>', css=(BASE, ARTICLE), rule="01.23", illustrative=True,
                                  alt="An illustrative position piece. The kicker opens with a Charcoal label, Our position, then Act. Headline: State senate committees should post every vote within two days. We support S. 214, which would require it. What the record shows: 14 of 20 committees posted no roll calls last session. The strongest case against: chairs in both parties say posting every procedural vote would discourage early compromise and need new clerk staff. What we don't know: whether faster posting changes how members vote. After the hinge divider, the disclosure: Oath & Action supports S. 214; read our explainer first. One red button: Ask your senator to vote yes. Footer: decided by the editorial board, February 26, 2027; no funder reviewed this piece; all positions are in the position log."),
                    "caption": "The label comes first, the case against comes before the ask, and the disclosure sits directly above the button."},
        "failure": {"specimen": A("s-01-23-failure", f'<div class="ed">{position_piece(True)}</div>', css=(BASE, ARTICLE), rule="01.23", illustrative=True,
                                  alt="The same piece with the Our position label moved to the footer, and with no case against, no open questions and no disclosure above the ask."),
                    "caption": "With the label at the bottom and no case against, a reader learns the piece was an argument only after the ask, which reads as a trick."},
        "specs": [{"label": n, "value": v} for n, v in kit],
        "related": ["13", "18"],
        "builders": "Use the position label component, never a plain kicker, and check the eight kit items in this rule’s specifications before the piece goes to the editor.",
    })

    PN = ".ed .pnl{list-style:none;margin:0;padding:0;display:grid;gap:10px;max-width:560px}.ed .pnl li{border-top:1px solid var(--oa-color-border-hairline);padding-top:8px;font:700 1.0625rem/1.4 var(--oa-font-family-reading)}.ed .pnl li span{display:block;font:var(--oa-type-caption);color:var(--oa-color-text-secondary)}"
    pn_ok = [("Oath & Action, the weekly briefing", "The newsletter"), ("Who Do They Answer To? The Oath & Action Systems Atlas", "The atlas, the one product named as a question"),
             ("Stock Trading Ban Tracker", "A tracker, named for its subject"), ("Reform 101 / Cloture", "An explainer: series, slash, topic"),
             ("Oath & Action Report 3: How state committees record their votes", "A report, numbered and dated")]
    pn_bad = [("Rent & Reform Tracker", "An ampersand in a product name"), ("The Senator Scorecard", "A product that grades officials"),
              ("Dispatch from the Front", "A war metaphor in a series name")]
    rules.append({
        "id": "01.24", "title": "Name each product for what it does, and keep the ampersand for Oath & Action.",
        "rule": ["Give each product a plain name that says what it does, signed by Oath & Action. The atlas is the only product named as a "
                 "question, and no product name holds an ampersand; a partner’s ampersand is written as “and”."],
        "why": {"text": ["One masterbrand means one trust mark, so a reader who trusts the newsletter can trust the tracker it links to. A plain name tells them what they will get before they open it."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-24-correct", '<div class="ed"><ul class="pnl">' + "".join(f'<li>{e(a)}{" " + ill() if a.startswith("Oath & Action Report") else ""}<span>{e(b)}</span></li>' for a, b in pn_ok) + "</ul></div>",
                                  css=(BASE, PN), rule="01.24",
                                  alt="Five product names: Oath & Action, the weekly briefing. Who Do They Answer To? The Oath & Action Systems Atlas. Stock Trading Ban Tracker. Reform 101 / Cloture. Oath & Action Report 3: How state committees record their votes (illustrative)."),
                    "caption": "Each name says what the product does, and the only ampersand belongs to Oath & Action."},
        "failure": {"specimen": A("s-01-24-failure", '<div class="ed"><ul class="pnl">' + "".join(f'<li>{e(a)} {ill()}<span>{e(b)}</span></li>' if i < 2 else f'<li>{e(a)}<span>{e(b)}</span></li>' for i, (a, b) in enumerate(pn_bad)) + "</ul></div>",
                                  css=(BASE, PN), rule="01.24",
                                  alt="Three names that break the rule: Rent & Reform Tracker, with an ampersand; The Senator Scorecard, which grades officials; and Dispatch from the Front, the fifth edition's series name, a war metaphor."),
                    "caption": "A second ampersand competes with ours, a scorecard grades the officials a reader is asked to contact, and “the Front” turns a series into a war."},
        "related": ["03", "22"],
        "builders": "Name a new product as its subject plus its kind, such as “Child Care Rules Tracker”, and run the name past this rule and Rule 01.15 before it ships.",
    })

    FL = ".ed .fl{max-width:620px;border-top:2px solid var(--oa-color-border-strong);padding-top:14px}.ed .fl .big{font:italic 400 clamp(1.5rem,1.3rem + .8vw,2rem)/1.3 var(--oa-font-family-quote);margin:6px 0 12px}"
    extras_after = [{"after_rule": "01.24", "specimen": A("s-01-founding-line",
        '<div class="ed"><div class="fl"><p class="lab">Our founding line, kept as a record</p><p class="big">“From spectators to stewards.”</p>'
        '<p>The line Oath &amp; Action started with. Our brand guide’s edition 4.2 lists it as the historical tagline, “Retired from current applications.” '
        'It has no role as a brand line today, because it competes with the tagline for the same place and casts a newcomer as a spectator.</p></div></div>',
        css=(BASE, FL), rule=None, label="Our founding line",
        alt="A record card. Our founding line, kept as a record: From spectators to stewards. Edition 4.2 lists it as the historical tagline, retired from current applications. It has no role as a brand line today."),
        "caption": "The founding line stays in our history, out of every lockup and headline."}]

    # extras that sit before Rule 01.1 carry no after_rule
    extras = [{"specimen": "s-01-hinge-lines", "label": "The hinge in the locked lines",
               "caption": "Each locked line splits at the hinge, a commitment first and the action after it. The pillars split the same way, between Track and Connect, where a reader stops learning about a decision and starts taking part in it."},
              {"specimen": "s-01-pillars", "label": "The four pillars, always in this order",
               "caption": "Every product carries the Oath & Action name. The atlas, the trackers and the data never take a position; positions appear only in labeled Act pieces. Chapter 09 draws the pillar marks."},
              {"specimen": "s-01-pieces", "label": "One piece from each pillar, at true size",
               "caption": "Each piece names its pillar in the kicker, turns at the hinge divider to “What you can do” and ends on one step, the view’s one working red. Explain and Track quote real records; Connect and Act are invented and labeled."}] + extras_after

    sources = [SRC_STOCK_SURVEY, SRC_STOCK_VOTES, SRC_INITIATIVE, SRC_FEC, SRC_R4A, SRC_PAY, SRC_CLOTURE, SRC_ELECTRIC,
               "Our brand guide, fifth edition, chapter 13 In use: “Who wrote the rule you are angry about?”"]

    data = {
        "number": "01", "anchor": "purpose", "title": "Purpose", "part": "Foundations",
        "instruction": "Learn what Oath & Action does, and how its pillars and nonpartisan rules shape every piece.",
        "intro": [f"Oath & Action is a nonpartisan publication and a set of tools for people in every state who live under public rules they "
                  f"rarely get to read. Our mission is {q(LOCKED['mission'])}",
                  "The ampersand in our name is the hinge, the joint a door swings on. It joins a promise to the action that keeps it, so "
                  "every piece explains and tracks a decision, then turns to the people who make it and the step a reader can take. "
                  "Chapter 04 draws the hinge and sets its rules."],
        "rules": rules, "extras": extras, "sources": sources,
        "related_chapters": [{"chapter": "02", "reason": "The lines that state the purpose."}, {"chapter": "04", "reason": "The hinge in full."},
                             {"chapter": "05", "reason": "Rule 05.3, the red rule these rules cite."}, {"chapter": "09", "reason": "The pillar marks."},
                             {"chapter": "13", "reason": "Evidence grades and the labels beside each item."}, {"chapter": "21", "reason": "The atlas as the purpose at work."}],
    }
    return data
