"""Chapter 01 Purpose: content and specimens for stage board A. Imported by guide_editor_build.py.

Fix pass round one, November 6, 2026: the items the stage A fix pass brief lists for the editor. Round two applies
the research lead's checks (H.R. 7008's grade, Rule 01.5's limits, Rules 01.11, 01.13 and 01.16, the Senate vote
line and the photographs in Rules 01.6 and 01.8).

Apply pass round one, November 7, 2026: the one-standard wording (DR-125), the pillar icons and kickers (DR-111,
DR-112) and the H.R. 7008 card on the six steps (DR-108, DR-109, DR-128). Two inputs wait for the research lead and
drop in without rewording: UNEVEN, the 2020 court example after Rule 01.11, and HR7008_STEPS, the card's step states.
"""
from guide_editor_common import (AMP16, AMP24, ARTICLE, BASE, CHART_DATA, HL, HR7008, HR7008_BOTH, HR7008_FIRST, HR7008_TRACKER,
                                 LOCKED, PIECE, PROW, TILE_GRID, WORDMARK24, WORDMARK24_PRUSSIAN, amp_h, cl_icon, dnp,
                                 e, flow, fx, hinge, ill, kicker, load, pillar_row, q)

# ---------------------------------------------------------------------------------------------------------------
# Inputs from the research lead, for round two of the apply pass. Each stays None until the main session routes the
# research lead's report (work/handoffs/phase-2/20261107_Apply-Pass-Research.md); the chapter then builds them in
# without any other wording changing.
# ---------------------------------------------------------------------------------------------------------------
# DR-125: the example of a finding that falls on one side, from atlas issue I155, printed only if the research lead's
# full reading of the court's opinion and the review holds. Shape:
#   dict(grade="Documented", lines=["sentence", ...], source="Source: ...", alt_note="", domain="D02",
#        state="Pennsylvania", region="Northeast", level="Federal")
# `lines` and `source` are printed exactly as the research lead writes them, sized to the grade.
# Round two: the research lead's recommended text and source line, word for word (work/handoffs/phase-2/
# 20261107_Apply-Pass-Research.md, section 1, "Recommendation"), graded Documented. Atlas issue I155 sits in domain D10;
# the court case is Pennsylvania's, and the review covers six states in all four regions.
UNEVEN = dict(
    grade="Documented",
    lines=["After the 2020 election, Donald J. Trump’s presidential campaign asked a federal appeals court to block "
           "Pennsylvania’s certified vote totals from taking effect. The court refused on November 27, 2020, noting that the "
           "campaign “never alleges that any ballot was fraudulent or cast by an illegal voter.” Lost, Not Stolen, a July 2022 "
           "review by eight conservatives, among them two former U.S. senators and three former federal appeals judges, "
           "counted 64 cases that Donald Trump and his supporters brought in six battleground states. It found that they "
           "“failed to produce substantive evidence to make their case,” and it records one case they won, in Pennsylvania, "
           "on far too few votes to change the result."],
    source=("Sources: U.S. Court of Appeals for the Third Circuit, Donald J. Trump for President, Inc. v. Secretary Commonwealth "
            "of Pennsylvania, No. 20-3371, opinion filed November 27, 2020, pages 9 and 21, via govinfo.gov; John Danforth and "
            "seven co-authors, Lost, Not Stolen: The Conservative Case that Trump Lost and Biden Won the 2020 Presidential "
            "Election, July 2022, printed pages 1 and 3, lostnotstolen.org; the 2020 presidential election in Arizona, Georgia, "
            "Michigan, Nevada, Pennsylvania and Wisconsin. Retrieved November 7, 2026. The court issued the opinion as not "
            "precedential. The count of 64 cases is the review’s own, and its authors say each of them “has worked in "
            "Republican politics, been appointed to office by Republicans, or is otherwise associated with the Party.”"),
    alt_note="",
    domain="D10", state="Pennsylvania, with five more states in the review", region="All four regions", level="Federal")

# DR-108, DR-128: the six steps of a federal bill; step 6 is named for whoever signs it.
STEPS_FEDERAL = ["Filed", "Hearing", "Committee vote", "First chamber", "Second chamber", "President"]
# The research lead's mapping of H.R. 7008's record to the six steps: one (state, words) pair per step, in order. The
# state is done, now, take, notyet, skipped or stopped; the words are what a screen reader hears for that step, such
# as its date. HR7008_STATUS is the line after "Step n of 6: Name." and HR7008_AS_OF the date of the newest record.
# Round two: the research lead's mapping (section 2, "The six steps for H.R. 7008"), as of the Congressional Record of
# November 5, 2026. Step 2 is a slash: the committee held no hearing on this bill, and its report cites only a hearing held
# before the bill was filed. Step 5 is current: no action in the record ends the bill, so no stopped square.
HR7008_STEPS = [("done", "January 12, 2026"),
                ("skipped", "no hearing on this bill"),
                ("done", "January 14, 2026, 7 to 4"),
                ("done", "the House passed it July 22, 2026, 232 to 198"),
                ("now", "a Senate vote to end debate on taking it up got 53 votes on September 30, 2026, short of the 60 it needed"),
                ("notyet", "")]
HR7008_STATUS = ("A Senate vote to end debate on taking it up got 53 votes on September 30, 2026, short of the 60 it needed, "
                 "and the bill has stayed on the Senate’s calendar since.")
HR7008_EARLIER = ("Step 2 never happened, because the committee held no hearing on this bill. Its report cites only a hearing "
                  "held November 19, 2025, before the bill was filed. The committee voted 7 to 4 on January 14, 2026, on a "
                  "version without the photo ID section, and the House passed both provisions 232 to 198 on July 22, 2026.")
HR7008_AS_OF = "November 5, 2026"
STATE_WORDS = {"done": "done", "now": "the bill is here now", "take": "the bill is here now, and you can take part",
               "notyet": "not yet", "skipped": "never happened", "stopped": "stopped here"}

# DR-125: the one-standard wording from board A's card A13, approved as written. The build checks each string verbatim.
NONPARTISAN = ("Nonpartisan, for us, means one standard of evidence and one way of describing sources, actors and parties, "
               "applied to everyone. We report each finding as the record shows it. When the record shows one party or official "
               "doing more of something, we say so, name who acted and size the claim to its evidence grade. No piece adds, "
               "softens or drops a finding to make the sides look even.")
# The hinge paragraph opens the hinge figure, so chapter 01's opening keeps the contract's two paragraphs (who we are,
# and what nonpartisan means, DR-125).
HINGE_LEAD = ("The ampersand in our name is the hinge, the joint a door swings on. It joins a promise to the action that keeps it, "
              "so every piece explains and tracks a decision, then turns to the people who make it and the step a reader can take. "
              "Chapter 04 draws the hinge and sets its rules.")
RULE_11_ADDED = ("When the record shows one party using a mechanism more, report it that way, with the counts, as Rule 01.13 "
                 "asks, and add no case to even the count.")
RULE_11_WHY = ("Where both parties use a mechanism, a case from each, told the same way, puts the mechanism in front of the "
               "reader. Where the record shows one side doing more, the finding stands as the record shows it.")

ATLAS = "Oath & Action’s systems atlas, Who Do They Answer To?"

SRC_STOCK_SURVEY = ("Source: Program for Public Consultation, University of Maryland, survey of 2,625 registered voters, "
                    "fielded May 19 to 30, 2023, United States, as recorded in " + ATLAS + ", snapshot of October 15, 2026. "
                    "The survey asked about a ban in general and names no bill.")
SRC_STOCK_VOTES = ("Sources: Library of Congress, bill status for H.R. 7008, 119th Congress, updated October 1, 2026, via "
                   "govinfo.gov; U.S. House of Representatives, Committee on House Administration, H. Rept. 119-479, February 3, "
                   "2026, page 5; Office of the Clerk, Roll Call 280, passage of H.R. 7008, July 22, 2026; Congressional Record, "
                   "Senate, August 6, 2026, page S4494, and Vote 253, cloture on the motion to proceed to H.R. 7008, September "
                   "30, 2026, page S5199; United States. Retrieved November 7, 2026. The Congressional Record shows no later "
                   "action through November 5, 2026. Ending debate needs three-fifths of the Senate, 60 votes.")
SRC_INITIATIVE = ("Source: Ballotpedia, a secondary source, States with initiative or referendum, statewide citizen-initiated "
                  "measures as described on November 6, 2026, 50 states and DC. Retrieved November 6, 2026. Mississippi’s "
                  "process cannot be used after a May 14, 2021 state supreme court ruling. Florida’s citizens may propose only "
                  "constitutional amendments, which need 60 percent of the vote. Illinois’s citizens may propose only "
                  "amendments on the legislature’s structure and procedure.")
SRC_FEC = ("Source: Federal Election Commission, Official 2024 Presidential General Election Results, compiled from state "
           "election offices, November 2024, 50 states and DC. Retrieved November 6, 2026.")
SRC_R4A = ("Sources: Texas Legislature, H.B. 4, 89th Legislature, second called session, bill history, August 2025; "
           "California Secretary of State, Statement of Vote, Proposition 50, November 4, 2025; Tangipa v. Newsom, U.S. "
           "District Court for the Central District of California, order of January 14, 2026; Texas and California. "
           "Retrieved November 6, 2026. The five-seat aims are each side’s stated goals; these lines do not measure the "
           "seats either map produced.")
SRC_PAY = ("Sources: Anna M. Stansbury and Lawrence H. Summers, Harvard University, “Productivity and Pay: Is the Link "
           "Broken?”, National Bureau of Economic Research Working Paper 24165, December 2017, 1973 to 2016, United States; "
           "Economic Policy Institute, “The Productivity-Pay Gap”, 1979 to 2026, United States. Retrieved November 6, 2026. "
           "The two differ in the price index they use and in how they count benefits; our systems atlas grades the "
           "connection plausible and contested.")
SRC_MINWAGE = ("Source: U.S. Department of Labor, Wage and Hour Division, State Minimum Wage Laws, updated July 1, 2026, "
               "Ohio and Pennsylvania, as recorded in " + ATLAS + ", snapshot of October 15, 2026. Ohio’s yearly rate "
               "applies to employers with annual gross receipts of $405,000 or more.")
SRC_CLOTURE = "Source: " + ATLAS + ", glossary entry “Cloture”."
PHOTO_PARKS = "work/build/assets/photography/20261106_Photo-Rule-01-6-Rosa-Parks-Lying-In-Honor-Capitol-Rotunda-2005.jpg"
PHOTO_ZIANNO = "work/build/assets/photography/20261106_Photo-Rule-01-8-Corps-Of-Engineers-Public-Meeting-Lake-Isabella-2014-Zianno.jpg"
CAP_PARKS = ("Members of the public file past the casket of Rosa Parks, the civil rights pioneer, as she lies in honor in the "
             "Rotunda of the U.S. Capitol, Washington, D.C., October 2005. Photograph: Architect of the Capitol.")
CAP_ZIANNO = ("Paul Zianno, chief of civil works acquisition and management for the U.S. Army Corps of Engineers Sacramento "
              "District, explains the Isabella Lake Dam safety project’s land purchases to residents at a public meeting in "
              "Lake Isabella, California, March 27, 2014. Photograph: John Prettyman, U.S. Army.")
SRC_ELECTRIC = "From " + ATLAS + ", the everyday answer to “Why is my electric bill going up?”"


# ---------------------------------------------------------------------------------------------------------------
# Pieces, one per pillar, at the width of a phone's text column (340 px, phone floor)
# ---------------------------------------------------------------------------------------------------------------
def piece_explain():
    return f'''<div class="pc">
{kicker("Explainer", "Utility rates")}
<p class="hl">Why is my electric bill going up?</p>
<p class="dek">A regulator or a board approves your rate.</p>
<div class="blk"><p class="lab">Who decides</p><p>For an investor-owned utility, your state’s public utility commission sets rates in a rate case, its formal review of the utility’s request. For public power and cooperatives, a city council, a utility board or a co-op board does.</p></div>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Find your utility’s name on your bill, then look up its open rate case on your state commission’s site for the dates to comment.</p>
<span class="ask" data-red="working" data-red-job="ask">Find your rate case</span>
<p class="by">{e(SRC_ELECTRIC)}</p>
</div>'''


HR7008_VOTES = ("The House passed it 232 to 198 on July 22, 2026. On September 30, 2026, a Senate vote to end debate on "
                "taking it up got 53 votes, short of the 60 it needed.")


def ch11():
    """Chapter 11's tracker module, apply_systems_ch11.py, read as it stands: its marks, step names and status words draw
    this card, so the card matches Rules 11.2 to 11.7 (24 px circles on a story card) with no marks of its own."""
    import importlib.util
    import sys
    from pathlib import Path
    if "apply_systems_ch11" not in sys.modules:
        here = Path(__file__).resolve().parent
        spec = importlib.util.spec_from_file_location("apply_systems_ch11", here / "apply_systems_ch11.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["apply_systems_ch11"] = mod
        spec.loader.exec_module(mod)
    return sys.modules["apply_systems_ch11"]


# Rule 11.5 gives each step one sixth of the row. A 288 px row (48 px a step) fits the card's narrowest column, 296 px at a
# 360 px screen, so the marks never scale and the numbers stay at 13 px (Rule 11.7).
STEPS_ROW = 288


def track_css():
    """The marks' colors for Newsprint and chapter 11's mark classes, as its story card sets them."""
    m = ch11()
    T = m.C.Tokens(m.C.TOKENS_JSON, m.C.TOKENS_CSS)
    ctx = m.B.Ctx(T, {}, "final")
    return ".ed .trk{" + m.mark_vars(ctx, "n") + "}" + m.MARK_CSS


def track_steps():
    """The six numbered steps of H.R. 7008's tracker, drawn by chapter 11's steps_svg() at its story card size, with a
    list a screen reader hears, a key of the six names and chapter 11's status words. Empty until HR7008_STEPS is set."""
    if not HR7008_STEPS:
        return ""
    m = ch11()
    if len(HR7008_STEPS) != 6:
        raise SystemExit("HR7008_STEPS needs one entry per step, six in all")
    states = [st for st, _ in HR7008_STEPS]
    if m.names("federal") != STEPS_FEDERAL:
        raise SystemExit("chapter 11's federal step names differ from this chapter's")
    sr = "".join(f"<li>Step {i + 1}, {STEPS_FEDERAL[i]}: {STATE_WORDS[st]}{', ' + e(w) if w else ''}.</li>"
                 for i, (st, w) in enumerate(HR7008_STEPS))
    key = " ".join(f'<span><b class="num">{i + 1}</b> {e(n)}</span>' for i, n in enumerate(STEPS_FEDERAL))
    status = m.status_words(dict(states=states, kind="federal"))
    earlier = f'<p class="st">{e(HR7008_EARLIER)}</p>' if HR7008_EARLIER else ""
    return (f'<div class="trk"><div class="mkw">{m.steps_svg(states, STEPS_ROW, 24)}</div><ol class="vh">{sr}</ol>'
            f'<p class="skey" aria-hidden="true">{key}</p></div>'
            f'<p class="st"><b>{e(status)}</b> {e(HR7008_STATUS or HR7008_VOTES)}</p>{earlier}')


def piece_track():
    """The Track piece: H.R. 7008's tracker as a story card, named whole with both provisions at first mention (DR-98).
    The card's words hold now; the numbered steps arrive with the research lead's mapping (round two)."""
    votes = "" if HR7008_STEPS else f'<p class="st">{e(HR7008_VOTES)}</p>'
    return f'''<div class="pc">
{kicker("Tracker", "Congress")}
<p class="hl">{e(HR7008_TRACKER)}</p>
<p class="dek">{e(HR7008_FIRST)}. As of {e(HR7008_AS_OF)}.</p>
{track_steps()}{votes}
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Get an email the day the Senate schedules its next vote on the bill.</p>
<span class="ask" data-red="working" data-red-job="ask">Follow this bill</span>
<p class="by">{e(SRC_STOCK_VOTES)}</p>
</div>'''


def piece_connect():
    return f'''<div class="pc">
{kicker("Guide", "Field Notes", illus=True)}
<p class="hl">Who answers for the repair on your street?</p>
<p class="dek">Alder County’s public works department schedules street repairs, and the Board of Supervisors sets its road budget each spring.</p>
<div class="blk"><p class="lab">What to say in 90 seconds</p><p>Give the street and the date you reported the damage. Then ask the board when the repair is scheduled and what it will cost.</p></div>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Speak at the board’s public comment period, 6 p.m. Tuesday, April 13, 2027.</p>
<span class="ask" data-red="working" data-red-job="ask">Find your supervisor</span>
</div>'''


def piece_act():
    return f'''<div class="pc">
{kicker("Act · How to take part", illus=True)}
<p class="hl">Alder County votes on backyard cottages March 9. Send a comment by March 3 or speak at the meeting.</p>
<div class="blk"><p class="lab">Who decides</p><p>Five county supervisors decide, and three votes pass the change.</p></div>
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Send a written comment by 5 p.m. Wednesday, March 3, 2027.</p>
<span class="ask" data-red="working" data-red-job="ask">Send a comment</span>
</div>'''


STAGES = f"""
.ed .trk{{margin:4px 0 0}}
.ed .mkw{{display:flex;justify-content:center}}
.ed .mk{{max-width:100%;height:auto}}
.ed .skey{{display:flex;flex-wrap:wrap;gap:2px 12px;margin:8px 0 0;{fx('caption')};color:var(--oa-color-text-secondary)}}
.ed .pc .st{{margin:10px 0 0}}
.ed .vh{{position:absolute;width:1px;height:1px;margin:0;padding:0;overflow:hidden;clip-path:inset(50%);white-space:nowrap}}
.sp-flow{{padding-left:0;padding-right:0}}
.ed .grid4{{display:flex;flex-wrap:wrap;gap:40px 24px;align-items:flex-start}}
.ed .grid4>div{{width:340px;max-width:100%}}
.ed .grid4 .pl{{{fx('h4')};margin:0 0 6px}}
"""


# ---------------------------------------------------------------------------------------------------------------
# The two Act kinds as phone pages, 360 px wide (phone floor)
# ---------------------------------------------------------------------------------------------------------------
def process_piece(fail=False):
    ask = "Tell the supervisors to vote yes" if fail else "Send a comment"
    sides = ('<div class="sec"><p class="lab">Why it matters</p><p>More homes would ease rents across the county, and the '
             'change costs taxpayers nothing.</p></div>') if fail else (
        '<div class="sec"><p class="lab">What each side has said</p><div class="two">'
        '<p><b>Supporters</b> said more homes would ease rents.</p>'
        '<p><b>Opponents</b> said sewers were sized for fewer homes.</p></div></div>')
    step2 = "" if fail else '<p class="step">Or speak for two minutes at 6 p.m. Tuesday, March 9, 2027.</p>'
    track = "" if fail else '<p class="foot">Follow the vote on the Backyard Cottages Tracker.</p>'
    return f'''<div class="art">
{kicker("Act · How to take part", illus=True)}
<p class="hl">Alder County votes on backyard cottages March 9. Send a comment by March 3 or speak at the meeting.</p>
<p class="dek">The Board of Supervisors will decide whether homeowners may build one small cottage behind a house, which the zoning code calls an accessory dwelling unit.</p>
<div class="sec"><p class="lab">Who decides</p><p>Five county supervisors decide, and three votes pass the change.</p></div>
{sides}
{hinge()}
<p class="wycd">What you can do</p>
<p class="step">Send a written comment by 5 p.m. Wednesday, March 3, 2027.</p>
{step2}
<span class="ask" data-red="working" data-red-job="ask">{e(ask)}</span>
{track}
</div>'''


def position_piece(fail=False):
    kick = kicker("Act", illus=True) if fail else kicker("Our position", "Committee votes", illus=True)
    against = "" if fail else (
        '<div class="sec"><p class="lab">The strongest case against</p><p>Committee chairs in both parties say posting every '
        'procedural vote would discourage early compromise and need new clerk staff. Sources: committee testimony, February '
        '2027; the clerk’s estimate.</p></div>'
        '<div class="sec"><p class="lab">What we don’t know</p><p>Whether faster posting changes how members vote.</p></div>')
    disc = "" if fail else ('<div class="disc"><p class="lab">Who decided</p><p>Our editorial board decided this position on '
                            'February 26, 2027. No funder has a stake in S. 214 or saw this piece before it ran. '
                            '<span class="bio">Read the bios of the board members who decided.</span></p></div>')
    foot = ('<p class="foot"><span class="pos">Our position</span> Decided by the editorial board.</p>' if fail else
            '<p class="foot">Our explainer on S. 214 sets out the main arguments on each side. Every position we take is listed in our position log.</p>')
    return f'''<div class="art">
{kick}
<p class="hl">State senate committees should post every vote within two days.</p>
<p class="dek">We support S. 214, which would require it.</p>
<div class="sec"><p class="lab">What the record shows</p><p>Documented: 14 of 20 committees posted no roll calls last session. Source: the senate clerk’s journal, 2026.</p></div>
{against}
{hinge()}
{disc}
<span class="ask" data-red="working" data-red-job="ask">Ask your senator to vote yes</span>
{foot}
</div>'''


# ---------------------------------------------------------------------------------------------------------------
# Charts and maps
# ---------------------------------------------------------------------------------------------------------------
CHART = f"""
.ed.vote{{max-width:600px}}
.ed .ct{{{fx('h4')};margin:0 0 4px;max-width:34ch;text-wrap:balance}}
.ed .cm{{{fx('caption')};color:var(--oa-color-text-secondary);margin:0 0 12px}}
.ed .bchart{{display:grid;gap:10px;margin:0}}
.ed .bar{{display:grid;grid-template-columns:7.5rem minmax(0,1fr);gap:10px;align-items:center}}
.ed .bar .nm{{{fx('body-small')}}}
.ed .bar .tr{{position:relative;height:28px}}
.ed .bar .f{{display:flex;align-items:center;justify-content:flex-end;height:28px;padding-right:8px;{fx('body-small', weight='700')};font-variant-numeric:tabular-nums}}
.ed .f.ink{{background:var(--oa-chart-color-party-mark);color:var(--oa-color-surface-newsprint)}}
.ed .f.red{{background:var(--oa-color-palette-pillar-red);color:var(--oa-color-palette-charcoal)}}
.ed .f.blue{{background:var(--oa-color-palette-prussian);color:var(--oa-color-palette-white)}}
.ed .key{{display:flex;flex-wrap:wrap;gap:6px 18px;margin:0 0 10px;{fx('body-small')}}}
.ed .sw{{display:inline-block;width:14px;height:14px;vertical-align:-2px;margin-right:6px}}
.ed .sw.red{{background:var(--oa-color-palette-pillar-red)}}.ed .sw.blue{{background:var(--oa-color-palette-prussian)}}
"""


def bars(rows, title, measure, src, names=True, key=None, head="", fail=False, after=""):
    out = [f'<div class="ed vote">{dnp() if fail else ""}{head}<p class="ct">{e(title)}</p><p class="cm">{e(measure)}</p>']
    if key:
        out.append('<p class="key">' + "".join(f'<span><span class="sw {c}"></span>{e(t)}</span>' for c, t in key) + "</p>")
    out.append('<div class="bchart">')
    for name, val, cls, vmax in rows:
        lab = e(name) if names else '<span aria-hidden="true"></span>'
        red = ' data-red="failure"' if cls == "red" else ""
        out.append(f'<div class="bar"><span class="nm">{lab}</span><span class="tr"><span class="f {cls}" style="width:{val / vmax * 100:.1f}%"'
                   f'{red}>{e(val)}{"%" if vmax == 100 else ""}</span></span></div>')
    out.append("</div>" + after + (f'<p class="src">{e(src)}</p>' if src else "") + "</div>")
    return "".join(out)


def tile_map(mode):
    """mode 'rule': states with a working citizen initiative; mode 'winner': the failure, colored by 2024 winner."""
    tiles = load(TILE_GRID)
    data = load(CHART_DATA)["datasets"]
    init = {r["code"]: r for r in data["initiative-states"]["rows"]}
    pres = {r["code"]: r for r in data["presidential-shift-by-state"]["rows"]}
    S, G = 24, 2  # 312 px across, so the map stays at true size inside a 360 px phone's frame
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
        halo = ' stroke="var(--oa-color-surface-newsprint)" stroke-width="4" paint-order="stroke"' if fill == "url(#hatch)" else ""
        cells.append(f'<g><rect x="{x}" y="{y}" width="{S}" height="{S}" fill="{fill}" stroke="var(--oa-color-border-strong)" '
                     f'stroke-width="1"{red}/><text x="{x + S / 2}" y="{y + S / 2 + 4.5}" text-anchor="middle" fill="{ink}" '
                     f'font-size="13" font-weight="700" font-family="var(--oa-font-family-reading)"{halo}>{c}</text></g>')
    defs = ('<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
            '<rect width="6" height="6" fill="var(--oa-color-surface-newsprint)"/><line x1="0" y1="0" x2="0" y2="6" '
            'stroke="var(--oa-color-data-emphasis)" stroke-width="2.5"/></pattern></defs>')
    svg = (f'<svg viewBox="-1 -1 {w + 2} {h + 2}" width="{w + 2}" height="{h + 2}" aria-hidden="true" focusable="false">'
           f'{defs}{"".join(cells)}</svg>')
    return svg, counts


MAP = f"""
@media (max-width:47.99em){{.sp{{padding-left:8px;padding-right:8px}}}}.ed .mapk{{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:6px;{fx('body-small')};max-width:360px}}
.ed .mapk li{{display:grid;grid-template-columns:22px minmax(0,1fr);gap:8px;align-items:start}}
.ed .mapk svg{{margin-top:3px}}
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
                y1, y2 = (28, 12) if up else (12, 28)
                head = (f'<polyline points="22,{17 if up else 23} 28,{y2} 34,{17 if up else 23}" fill="none" stroke="{ink}" '
                        f'stroke-width="2.5" stroke-linejoin="miter"/>')
                arrow = f'<line x1="28" y1="{y1}" x2="28" y2="{y2}" stroke="{ink}" stroke-width="2.5"/>{head}'
                if kind in ("down2", "up2"):
                    arrow = arrow.replace('x1="28"', 'x1="24"', 1).replace('x2="28"', 'x2="24"', 1)
                    arrow += f'<line x1="32" y1="{y1}" x2="32" y2="{y2}" stroke="{ink}" stroke-width="2.5"/>'
            sw = (f'<svg width="56" height="40" viewBox="0 0 56 40" aria-hidden="true" focusable="false"><rect x=".5" y=".5" width="55" '
                  f'height="39" fill="{fill}" stroke="var(--oa-color-border-strong)"/><rect x="14" y="6" width="28" height="28" '
                  f'fill="none" stroke="{ink}" stroke-width="1.5"/>{arrow}</svg>')
        out.append(f'<li>{sw}<span>{e(word)}</span></li>')
    return out


DIV = f"""
.ed .dk{{max-width:600px;list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:0}}
.ed .dk li{{display:grid;justify-items:start;gap:6px;width:112px;{fx('body-small')};padding-right:8px}}
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
NAMED_STATES = ("Texas", "California", "Ohio", "Pennsylvania")
EXAMPLES = [
    # (example, domain, state, region, level, coalition, illustrative, where)
    ("Who sets your electric rate", "D09", "Every state", "Every region", "State", "No reform shown", False, "Explain piece; Rule 01.13"),
    ("A ban on stock trading by members of Congress, May 2023 survey", "D03", "National", "National", "Federal",
     "Survey majorities of both parties’ voters, for a ban in general", False, "Rules 01.2, 01.20"),
    ("H.R. 7008, the Stop Insider Trading Act", "D03", "National", "National", "Federal",
     "House passage: 218 Republicans, 13 Democrats and one independent; Senate vote to end debate: 53 Republicans", False,
     "Track piece; Rules 01.6, 01.10, 01.21, 01.24"),
    ("A county road budget", "D04", "Alder County (invented)", "None, invented", "County or city", "No reform shown", True, "Connect piece"),
    ("Backyard cottages", "D09", "Alder County (invented)", "None, invented", "County or city", "Invented", True, "Act piece; Rules 01.8, 01.21, 01.22"),
    ("Posting committee votes, S. 214", "D01", "Unnamed state (invented)", "None, invented", "State", "Invented", True, "Rules 01.1, 01.4, 01.21, 01.23"),
    ("Mid-decade map redraws", "D02", "Texas and California", "South and West", "State", "No reform shown", False, "Rule 01.11"),
    ("Citizen initiatives", "D02", "50 states and DC", "Every region", "State", "No reform shown", False, "Rule 01.5"),
    ("Minimum wage floors", "D07", "Ohio and Pennsylvania", "Midwest and Northeast", "State", "No reform shown", False, "Rules 01.10, 01.12"),
    ("Productivity and pay", "D07", "National", "National", "Federal", "No reform shown", False, "Rule 01.16"),
    ("The cloture rule", "D04", "National", "National", "Federal", "No reform shown", False, "Rule 01.17"),
    ("A state overtime rule", "D07", "Unnamed state (invented)", "None, invented", "State", "Invented", True, "Rule 01.15"),
    ("A school bell schedule", "D09", "Unnamed district (invented)", "None, invented", "School district", "Invented", True, "Rule 01.10"),
    ("How property tax rates are set", "D08", "Every state", "Every region", "County or city", "No reform shown", False, "Rule 01.14"),
    ("A bus route hearing", "D04", "Unnamed city (invented)", "None, invented", "County or city", "No reform shown", True, "Rule 01.19"),
    ("Rosa Parks lying in honor at the Capitol", "D10", "Washington, D.C.", "National", "Federal", "No reform shown", False, "Rule 01.6"),
    ("A public meeting on a federal dam project", "D04", "California", "West", "Federal", "No reform shown", False, "Rule 01.8"),
]


def all_examples():
    """The chapter's examples, with the 2020 court example once the research lead's check lets it print (DR-125)."""
    if not UNEVEN:
        return EXAMPLES
    return EXAMPLES + [("Claims of outcome-changing fraud after the 2020 election, in court", UNEVEN["domain"], UNEVEN["state"],
                        UNEVEN["region"], UNEVEN["level"], "No reform shown", False, "After Rule 01.11")]


def tally():
    from collections import Counter
    ex = all_examples()
    n = len(ex)
    dom = Counter(x[1] for x in ex)
    named_states = Counter()
    for x in ex:
        for s in NAMED_STATES:
            if s in x[2]:
                named_states[s] += 1
    return n, dom, named_states


def words(s):
    import re
    return len(re.findall(r"[\w’'.,-]+", s))


SPELL = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


# ---------------------------------------------------------------------------------------------------------------
def build(book):
    """Write chapter 01's specimens into the book and return the chapter dictionary."""
    A = lambda sid, body, **kw: book.add(sid, body, chapter="01", **kw)
    rules = []

    # --- extras before Rule 01.1 -----------------------------------------------------------------------------
    words_key = [
        ("Locked lines", "Our four brand lines whose wording never changes: the tagline, the mission, the reader promise and "
                         "the editorial commitment.", "#rule-02-23", "Rule 02.23"),
        ("Pillars", "Explain, Track, Connect and Act, the four jobs our work does, always in that order. Each pillar has an "
                    "icon, set with its word beside it.", None, None),
        ("The seven colors", "Newsprint, a warm off-white, is our page, and Charcoal carries the words. Pillar Red marks one "
                             "thing in each view. Prussian, our dark blue, Stone, a mid gray, Verdigris, a muted green, and "
                             "White support the rest.", "#color", "Chapter 05"),
        ("View", "One screen, card, slide or printed page.", "#rule-04-2", "Rule 04.2"),
        ("Working red", "The one red a view may spend, on an error the reader must fix, the step they can take now or the "
                        "point the headline names, in that order.", "#rule-05-3", "Rule 05.3"),
        ("Signature red", "The red inside our marks and icons, such as the wordmark’s ampersand and the lockmark’s lever. It "
                          "never counts as a view’s working red.", "#rule-05-3", "Rule 05.3"),
        ("Token", "A named color, size or type setting in our code, such as --oa-color-text-primary-on-newsprint. Builders "
                  "use the name, and writers can skip the Tokens lines.", None, None),
        ("Kicker", "The short line above a headline that says what kind of piece it is.", "#rule-01-21", "Rule 01.21"),
        ("Deck", "The line under a headline that says what the piece covers.", None, None),
        ("Hinge headline", "A headline that joins a rule to what it produces with our ampersand, as in “The zoning code "
                           "& the rent.”", "#rule-02-27", "Rule 02.27"),
        ("Hinge divider", "A hairline broken by our ampersand, set where a piece turns from how a decision is made to what "
                          "you can do.", "#rule-04-4", "Rule 04.4"),
        ("Lockup", "Our name and marks set together in one fixed arrangement.", "#identity", "Chapter 03"),
        ("Our systems atlas", "Who Do They Answer To?, our map of who makes public decisions and what shapes them. A loop "
                              "in it is a chain of causes that returns to where it started, and its ten domains sort "
                              "every issue by subject, such as elections and representation.", None, None),
        ("Evidence grade", "How sure a claim is: documented, well supported, plausible, contested or hypothesis.",
         "#s-02-22-correct--h08", "House rule H08"),
        ("Illustrative", "Our label for anything invented for an example, such as a person, a quote, a place or a figure.",
         "#s-02-22-correct--h03", "House rule H03"),
    ]
    WCSS = (f".ed .wk{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,19rem),1fr));gap:0 32px;margin:0}}"
            f".ed .wk div{{border-top:1px solid var(--oa-color-border-hairline);padding:10px 0 12px}}"
            f".ed .wk dt{{{fx('body', weight='700')}}}.ed .wk dd{{margin:2px 0 0;{fx('body-small')}}}"
            f".ed .wk code{{font-size:inherit;overflow-wrap:anywhere}}.ed .wk a{{color:inherit;text-underline-offset:3px}}")
    wk = "".join(f'<div><dt>{e(t)}</dt><dd>{e(d).replace("--oa-color-text-primary-on-newsprint", "<code>--oa-color-text-primary-on-newsprint</code>")}'
                 + (f' <a href="{h}">{e(lk)}</a>' if h else "") + "</dd></div>" for t, d, h, lk in words_key)
    A("s-01-words", f'<div class="ed"><dl class="wk">{wk}</dl></div>', css=(BASE, WCSS), rule=None, readable=True,
      label="Words this guide uses",
      alt="A list of the words this guide uses, each with its meaning and the rule or chapter that sets it: "
          + " ".join(f"{t}: {d}" for t, d, _, _ in words_key),
      notes="CP-M2, RP-S7: the guide's vocabulary before chapter 01 uses it. Token is defined here for the first time. "
            "The atlas glossary's own wording for a feedback loop: a chain of causes that returns to its starting variable.")

    rows = [("Mission", LOCKED["mission"], ("understand", "improve"), "understand", "improve"),
            ("Reader promise", LOCKED["promise"], ("We explain how a decision is made", "give you a practical way to take part."),
             "we explain the decision", "you get a way to take part"),
            ("Editorial commitment", LOCKED["commitment"], ("Clarity is our duty.", "Action is our promise."), "clarity, our duty", "action, our promise"),
            ("Pillars", "Explain → Track → Connect → Act", ("Explain → Track", "Connect → Act"), "Explain, Track", "Connect, Act")]

    def split_line(line, halves):
        a, b = halves
        i, j = line.index(a), line.index(b)
        return e(line[:i]) + f'<b class="cm1">{e(a)}</b>' + e(line[i + len(a):j]) + f'<span class="ac1">{e(b)}</span>' + e(line[j + len(b):])

    trs = "".join(f'<tr><th scope="row">{e(r)}<br><span class="ll">{"“" if r != "Pillars" else ""}{split_line(l, h)}{"”" if r != "Pillars" else ""}</span></th>'
                  f'<td data-k="Commitment">{e(c)}</td><td data-k="Action">{e(a)}</td></tr>' for r, l, h, c, a in rows)
    trs += (f'<tr><th scope="row">Tagline<br><span class="ll">{e(q(LOCKED["tagline"]))}</span></th>'
            f'<td colspan="2">It names the result when the hinge has turned and the loop closes: officials who answer to the people they serve.</td></tr>')
    A("s-01-hinge-lines", f'<div class="ed hl"><p class="hlead">{e(HINGE_LEAD)}</p><table class="stack"><thead><tr><th scope="col">Locked line, exact</th><th scope="col">The commitment</th>'
      f'<th scope="col">The action</th></tr></thead><tbody>{trs}</tbody></table></div>',
      rule=None, readable=True, label="The hinge in the locked lines",
      css=(BASE, f".ed.hl .cm1{{font-weight:700}}.ed.hl .ac1{{text-decoration:underline solid 2px var(--oa-color-graphic-essential);text-underline-offset:4px}}"
                 f".ed.hl th[scope=row]{{min-width:18rem;{fx('body-small', weight='700')}}}.ed.hl .ll{{display:block;{fx('body')};margin-top:4px}}"
                 f".ed.hl .hlead{{{fx('body')};max-width:64ch;margin:0 0 20px}}"),
      alt=HINGE_LEAD + " Then a table of the locked lines, each shown whole with its commitment in bold and its action underlined. Mission: understand, then improve. "
          "Reader promise: we explain the decision, then you get a way to take part. Editorial commitment: clarity, our duty, then "
          "action, our promise. Pillars: Explain and Track, then Connect and Act. The tagline names the result.",
      notes="From the brand strategy, section 1, approved at Gate 1 (S1). The hinge drawing is chapter 04's. The lead paragraph was the "
            "opening's second paragraph until the apply pass; it moved here so the opening keeps the content contract's two paragraphs "
            "once A13's paragraph on what nonpartisan means joined it (DR-125).")

    pillars = [
        ("01", "Explain", "Make the rules and their effects understandable.",
         ["Explainers, in the Reform 101 and The Oath series", "The atlas’s 16 question-first pathways, such as “Why did my rent go up?”",
          "Reports", "The weekly briefing newsletter", "Glossaries and primers"]),
        ("02", "Track", "Follow the decision and keep its record within reach.",
         ["Trackers, each named for its subject and dated “as of”", "Two series, Dispatch and The Public Record",
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
    PCSS = (f".ed .pills{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,290px),1fr));gap:28px 28px;margin:28px 0 0}}"
            f".ed .pcol{{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}}"
            f".ed .pn{{{fx('label')};font-variant-numeric:tabular-nums;color:var(--oa-color-text-secondary);margin:0 0 6px}}"
            + flow(".ed .pname", "h3") + f".ed .pname{{margin:0 0 10px}}"
            f".ed .pjob{{{fx('body')};margin:0 0 14px}}"
            f".ed .pcol ul{{margin:0;padding-left:1.1em;{fx('body-small')}}}.ed .pcol li{{margin:0 0 6px}}"
            f".ed .prow-box+.prow-box,.ed .pills+.prow-box{{margin-top:32px}}.ed .prow-box .lab{{margin:0 0 12px}}"
            f".ed .prow-box{{border-top:1px solid var(--oa-color-border-hairline);padding-top:12px}}")
    A("s-01-pillars", f'<div class="ed"><div class="prow-box"><p class="lab">The pillar row</p>{pillar_row(48)}</div>'
                      f'<div class="pills">{cards}</div>'
                      f'<div class="prow-box"><p class="lab">The compact row, on a page that serves Track</p>'
                      f'{pillar_row(24, current="Track", label="The four pillars, in order, with Track as the current pillar")}</div></div>',
      css=(BASE, PCSS, PROW),
      rule=None, readable=True, label="The four pillars, always in this order",
      alt="The pillar row: the four pillar icons at 48 px, each with its word beside it, joined by arrows in order: Explain, an open "
          "book; Track, a route to a magnifier; Connect, two overlapping rings; Act, a finger pressing a round control. "
          "Then each pillar's job and products. 01 Explain: make the rules and their effects understandable. "
          "Explainers in the Reform 101 and The Oath series, the atlas's 16 question-first pathways, reports, the weekly briefing "
          "newsletter, glossaries and primers. 02 Track: follow the decision and keep its record within reach. Trackers, two series, Dispatch and "
          "The Public Record, the atlas Register. 03 Connect: help people reach the office that decides and the evidence it "
          "decides on. Guides and call scripts, the Field Notes series, the atlas's view of who can act. 04 Act: give the reader a "
          "useful next step. Act pieces in two kinds, case studies in the Proof It Works series, and the closing step on every piece. "
          "Last, the compact row at 24 px on a page that serves Track: every icon in one color, and the word Track set bold and underlined.",
      notes="DR-111: the four pillar icons are Civic Line CL-019 Explain, CL-020 Track, CL-021 Connect and CL-022 Act, inlined from the "
            "black masters with their geometry untouched and their ink taken through currentColor; each word sits beside its icon, "
            "and the current pillar's word is underlined at every size, bold under 48 px. Red as a second sign on the current icon "
            "starts at 48 px, so the 24 px row stays one color. The 48 px row stacks in one column under 48em, with downward arrows, "
            "after the creative director's Board 6 review found the phone row dropping its arrow. Products named as the brand's set, "
            "with no launch dates or status (DR-91). Product placement follows the brand architecture table (strategy section 3, S2); "
            "each series' pillar follows Rule 02.26's series list, and series routes retire (DR-110). Connect's job line is new, "
            "since the V5 census cut its line at 50 characters (DR-123). CP-S8: the series is Dispatch, as Rule 02.26 spells it.")

    A("s-01-pieces", f'''<div class="ed"><div class="grid4">
<div><p class="pl">Explain</p>{piece_explain()}</div>
<div><p class="pl">Track</p>{piece_track()}</div>
<div><p class="pl">Connect</p>{piece_connect()}</div>
<div><p class="pl">Act</p>{piece_act()}</div></div></div>''', css=(BASE, PIECE, STAGES, track_css()),
      rule=None, label="One piece from each pillar, at true size",
      alt="Four pieces at a phone's text width, one per pillar, each opening with its kicker, turning at the hinge divider to What "
          "you can do and ending on one red ask button. Explain: Explainer, utility rates. Why is my electric bill going up? A "
          "regulator or a board approves your rate; who decides; then find your rate case. Track: Tracker, Congress. "
          f"{HR7008_TRACKER}. {HR7008_FIRST}. As of {HR7008_AS_OF}. "
          + (f"Six numbered steps, Filed, Hearing, Committee vote, First chamber, Second chamber and President: "
             + "; ".join(f"step {i + 1}, {STEPS_FEDERAL[i]}, {STATE_WORDS[s]}" for i, (s, _) in enumerate(HR7008_STEPS or [])) + ". "
             if HR7008_STEPS else "")
          + (ch11().status_words(dict(states=[st for st, _ in HR7008_STEPS], kind="federal")) + " " if HR7008_STEPS else "")
          + f"{HR7008_STATUS or HR7008_VOTES} {HR7008_EARLIER if HR7008_STEPS else ''} Then follow this bill. Connect, "
          "labeled Illustrative: Guide, Field Notes. Who answers for the repair on your street in Alder County, what to say in 90 "
          "seconds, then find your supervisor. Act, labeled Illustrative: Act, how to take part. Alder County votes on backyard "
          "cottages March 9; send a comment by March 3.",
      notes="Explain and Track use real atlas copy and records; Connect and Act are invented, each with one Illustrative label at "
            "its head (DR-97). Each card is 340 px wide, the text column of a phone; the plate flows so the cards stack on a "
            "phone, and the caption carries the width (C-S6). H.R. 7008 named and described whole at its first mention (DR-98). "
            "The Track card is a tracker story card, so it takes numbered steps (DR-109) on the six steps with step 6 named "
            "President for a federal bill (DR-128); its step states come from the research lead's mapping in round two, and until "
            "then it prints the two documented votes. Its kicker stays in words: the Civic Line's Congress icon, CL-025, draws a capitol "
            "dome with columns, which Rule 01.6 keeps out of icons.")

    # --- Group 1: color and party -----------------------------------------------------------------------------
    vote_rows = lambda fail: [("Yes", 6, "ink", 9), ("No", 3, "red" if fail else "ink", 9)]
    vt = "The Government Operations Committee sent S. 214 to the full senate, 6 to 3."
    vm = "Committee vote on S. 214, Tuesday, March 2, 2027."
    vbody = lambda fail: bars(vote_rows(fail), vt, vm, "", head=kicker("Report", "State senate", illus=True), fail=fail,
                              after=f'{hinge()}<span class="ask" data-red="working" data-red-job="ask">Follow S. 214</span>')
    rules.append({
        "id": "01.1", "title": "Keep red off every party, side and person.",
        "rule": ["Pillar Red never stands for a party, one side of a debate or a named person, in a chart, a map, a label or a headline. "
                 "Each view gives its one working red to the job Rule 05.3 names, and none of those jobs is a side."],
        "tokens": ["oa.chart.color.party.mark.onNewsprint", "oa.color.action.ask.fill.onNewsprint"],
        "why": {"text": ["Election-night maps have taught readers to see red as one party. A red mark on a side tells a reader on the other "
                         "side that the piece is against them before they read a word, and they stop trusting the record we keep for everyone."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-1-correct", vbody(False), css=(BASE, CHART), rule="01.1", illustrative=True, width=360,
                                  alt="An illustrative card, kicker Report, state senate. The Government Operations Committee sent S. 214 to the full senate, 6 to 3. "
                                      "Both bars, yes and no, are Charcoal, each with its name and count. After the hinge divider, one red button: Follow S. 214."),
                    "caption": "Both sides of the vote take the same Charcoal, with their names and counts printed. The view’s one working red goes to the step a reader can take now, the button that follows the bill."},
        "failure": {"specimen": A("s-01-1-failure", vbody(True), css=(BASE, CHART), rule="01.1", illustrative=True, width=360, exempt=["red", "contrast"],
                                  alt="Failure case: do not publish. The same card with the no bar drawn in Pillar Red, so the card has two reds, one on a side of the vote."),
                    "caption": "Red on the no votes casts those three senators as the problem. A reader who agrees with them sees an attack, and the count stops reading as a record."},
        "specs": [{"label": "Working red", "value": "One job per view, in the order Rule 05.3 sets", "token": "oa.color.action.ask.fill.onNewsprint"},
                  {"label": "Sides of a vote", "value": "One neutral ink, names and counts printed", "token": "oa.chart.color.party.mark.onNewsprint"}],
        "related": ["05", "14"],
        "builders": "Search the piece for Pillar Red and name each red mark’s job. If a mark stands for a party, a side or a person, redraw it in the party mark ink with its name printed.",
    })

    st = load(CHART_DATA)["datasets"]["stock-trading-ban"]["rows"]
    sv = {r["key"]: r["value"] for r in st}
    t2 = "In May 2023, most Democrats and most Republicans favored a ban on stock trading by members of Congress."
    m2 = "Percent of registered voters who favored a ban, May 2023. Parties in alphabetical order."
    rules.append({
        "id": "01.2", "title": "Draw every party in one neutral ink, with its name on the mark.",
        "rule": ["When a chart, map or table shows parties, draw every party’s mark in the same neutral ink, Charcoal on Newsprint, and "
                 "print the party’s name on or beside its mark. Where two sides must be told apart at a glance, draw one solid and one in "
                 "outline, in that same ink. Red never stands against blue or Verdigris."],
        "tokens": ["oa.chart.color.party.mark.onNewsprint"],
        "why": {"text": ["Red against blue reads as an election before it reads as data, and red against Verdigris stages the same contest in "
                         "other hues. One ink gives every party the same weight, and a printed name lets a reader see who is who without "
                         "learning a color code, in color or in grayscale."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-2-correct", bars([("Democrats", sv["support-democrats"], "ink", 100), ("Republicans", sv["support-republicans"], "ink", 100)], t2, m2, SRC_STOCK_SURVEY),
                                  css=(BASE, CHART), rule="01.2",
                                  alt=f"Bar chart: {t2} Democrats 88 percent and Republicans 87 percent, both bars in the same Charcoal, each named beside its bar. {SRC_STOCK_SURVEY}"),
                    "caption": "Both parties take the same Charcoal, with each party’s name beside its bar, so a finding of agreement reads as agreement."},
        "failure": {"specimen": A("s-01-2-failure", bars([("Democrats", sv["support-democrats"], "blue", 100), ("Republicans", sv["support-republicans"], "red", 100)], t2, m2, SRC_STOCK_SURVEY, names=False,
                                                         key=[("blue", "Democrats"), ("red", "Republicans")], fail=True),
                                  css=(BASE, CHART), rule="01.2", exempt=["red", "contrast"],
                                  alt="Failure case: do not publish. The same chart with the Democrats' bar in Prussian blue and the Republicans' bar in Pillar Red, unlabeled, with a color key above."),
                    "caption": "Red and blue turn a finding of agreement into a contest, and the color key makes a reader match swatches to find each party, which fails in grayscale."},
        "specs": [{"label": "Party marks", "value": "Charcoal, one ink for every party", "token": "oa.chart.color.party.mark.onNewsprint"},
                  {"label": "Two sides at a glance", "value": "One solid and one in outline, in the same ink"},
                  {"label": "Names", "value": "Printed on or beside each mark, in the text ink"},
                  {"label": "Order", "value": "Alphabetical, unless the data sets another order"}],
        "related": ["05", "14"],
        "builders": "Use the party mark token for every party, never a palette color by name, and set each party’s name as a direct label.",
    })

    dk_ok = "".join(diverging_key(False))
    dk_bad = "".join(diverging_key(True))
    dtitle = '<p class="ct">Change since the last count, in percentage points</p><p class="cm">A key with no data behind it, shown for its colors and arrows.</p>'
    rules.append({
        "id": "01.3", "title": "Run a two-way scale from Prussian through the page color to Verdigris.",
        "rule": ["A scale that shows change in two directions runs from Prussian through Newsprint to Verdigris. A boxed arrow and a word "
                 "name each step’s direction, because the two hues lose their order in grayscale. Red and blue never form a two-way pair."],
        "tokens": [f"oa.chart.color.diverging.fill.step{i}.onNewsprint" for i in range(1, 6)],
        "why": {"text": ["Neither end of the pair belongs to a party, so a fall and a rise carry the same weight. The arrow and the word carry "
                         "the direction for a reader who sees no color at all."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-3-correct", f'<div class="ed">{dtitle}<ul class="dk">{dk_ok}</ul></div>', css=(BASE, CHART, DIV), rule="01.3",
                                  alt="A five-step key for change in two directions, from Prussian through Newsprint to Verdigris. Each step has a boxed arrow and a word: down 2 points or more, down less than 2, no change, up less than 2, up 2 points or more."),
                    "caption": "Each step carries a boxed arrow and a word, so the key reads the same in grayscale."},
        "failure": {"specimen": A("s-01-3-failure", f'<div class="ed">{dnp()}{dtitle}<ul class="dk">{dk_bad}</ul></div>', css=(BASE, CHART, DIV), rule="01.3", exempt=["red", "contrast"],
                                  alt="Failure case: do not publish. The same key running from Pillar Red through Newsprint to Prussian blue, with no arrows."),
                    "caption": "A red-to-blue scale reads as one party’s gain against the other’s, whatever it measures, and with no arrows its direction disappears in grayscale."},
        "specs": [{"label": "Steps", "value": "Five, step 1 the strongest fall, step 3 the page color", "token": "oa.chart.color.diverging.fill.step3.onNewsprint"},
                  {"label": "Direction", "value": "A boxed arrow in each step’s label ink, and a word"}],
        "related": ["05", "14"],
        "builders": "Use the five diverging steps in order and draw each arrow in the matching diverging label token, which the chart palette pairs with its fill.",
    })

    pr_bar = ('<div class="pbar"><p class="pt">Committees that posted every roll call last session</p>'
              '<div class="pb"><span style="width:30%"></span></div><p class="pv num">6 of 20</p></div>')
    PRCSS = (f".ed.prus{{padding:0}}"
             f".ed .pbar{{margin-top:22px}}.ed .pt{{{fx('body')};margin:0 0 8px}}"
             f".ed .pb{{height:16px;border:1px solid var(--oa-color-data-emphasis)}}.ed .pb span{{display:block;height:100%;background:var(--oa-color-data-emphasis)}}"
             f".ed .pv{{{fx('body', weight='700')};margin-top:6px}}"
             f".ed .wmk{{display:block;height:24px;width:auto;color:var(--oa-color-text-primary)}}"
             f".ed .wmk.redamp{{--amp:var(--oa-color-palette-pillar-red)}}")
    rules.append({
        "id": "01.4", "title": "On Prussian, turn identity marks White and data marks Newsprint.",
        "rule": ["On a Prussian ground, set every identity mark in one color, White, the ampersand included. Draw data graphics on Prussian "
                 "in Newsprint. Red never sits on Prussian."],
        "tokens": ["oa.color.identity.signature.onPrussian", "oa.color.data.emphasis.onPrussian"],
        "why": {"text": ["Pillar Red measures 3.19 to 1 against Prussian, which passes the 3 to 1 WCAG asks of marks until the size drops. "
                         "At 16 px, where smoothing thins the strokes, the red ampersand measures 2.27 to 1 and a White one 8.27 to 1. "
                         "Red on our dark blue also pairs the two colors election maps give the parties."],
                "basis": "Design judgment, measured against WCAG 2.2 SC 1.4.11 at rendered sizes"},
        "correct": {"specimen": A("s-01-4-correct", f'<div class="ed prus">{kicker("Report", "State legislatures", illus=True)}<img data-inline src="{WORDMARK24_PRUSSIAN}" alt="Oath & Action" class="wmk" height="24">{pr_bar}</div>',
                                  css=(BASE, PRCSS), rule="01.4", surface="prussian", illustrative=True, width=360,
                                  alt="A Prussian panel with the wordmark in White, ampersand included, at its 24 px master, and an illustrative bar in Newsprint: committees that posted every roll call last session, 6 of 20."),
                    "caption": "The wordmark and its ampersand turn White, and the bar turns Newsprint. The panel carries no red."},
        "failure": {"specimen": A("s-01-4-failure", f'<div class="ed prus">{kicker("Report", "State legislatures", illus=True)}<img data-inline src="{WORDMARK24}" alt="Oath & Action" class="wmk redamp" height="24" data-red="failure">{pr_bar}</div>',
                                  css=(BASE, PRCSS), rule="01.4", surface="prussian", illustrative=True, width=360, exempt=["contrast", "red"],
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
        "id": "01.5", "title": "Color a map by the rule or measure the story covers.",
        "rule": ["Color a map by the rule, count or measure the story is about, never by which party won each place. Use the neutral palette "
                 "or a pattern, and set the key beside the map."],
        "tokens": ["oa.color.data.emphasis.onNewsprint", "oa.color.border.strong.onNewsprint"],
        "why": {"text": ["A map colored by winner splits the country into two camps and gives large, thinly settled states the most ink. "
                         "What a reader wants to know is whether a rule reaches the place where they live."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-5-correct", f'<div class="ed"><p class="ct">{e(t5)}</p><p class="cm">Statewide citizen-initiated measures, by state, as read November 6, 2026</p>'
                                                    f'{svg_rule}{key_rule}<p class="src">{e(SRC_INITIATIVE)}</p></div>',
                                  css=(BASE, CHART, MAP), rule="01.5",
                                  alt=f"Tile map of the 50 states and DC. {t5} Those tiles are solid Charcoal; Mississippi is hatched; the other {cnt['none']} states are open. Key below the map. {SRC_INITIATIVE}",
                                  notes="Round two: the research lead checks the 23-state count and each state's limits (Mississippi, Illinois, Florida), and the source line takes them (DR-99, BE-S3)."),
                    "caption": "Solid, hatched and open tiles show the rule, with the key next to the map and the source below it."},
        "failure": {"specimen": A("s-01-5-failure", f'<div class="ed">{dnp()}<p class="ct">The 2024 presidential vote, by state</p><p class="cm">Winner of each state</p>'
                                                    f'{svg_win}{key_win}<p class="src">{e(SRC_FEC)}</p></div>',
                                  css=(BASE, CHART, MAP), rule="01.5", exempt=["red", "contrast"],
                                  alt=f"Failure case: do not publish. The same tile map colored by the 2024 presidential winner, {cw['rep']} tiles in Pillar Red and {cw['dem']} in Prussian blue. {SRC_FEC}"),
                    "caption": "Colored by winner, the map splits the country into two camps and says nothing about the rule a story covers."},
        "specs": [{"label": "Tile grid", "value": "12 columns by 8 rows, one square per state and DC"},
                  {"label": "Fills", "value": "Charcoal, a Charcoal hatch and open, keyed in words", "token": "oa.color.data.emphasis.onNewsprint"}],
        "files": [TILE_GRID],
        "related": ["14", "05"],
        "builders": "Start from our shared tile grid and join the story’s own measure to it by state code. A map of election results follows chapter 14’s rules, with party names printed.",
    })

    # --- Group 2: pictures --------------------------------------------------------------------------------------
    PH = (f".ed .phw{{max-width:600px}}.ed .ph{{display:block;width:100%;height:auto;object-fit:cover;background:var(--oa-color-surface-white)}}"
          f".ed .ph.r53{{aspect-ratio:5/3;object-position:50% 0%}}.ed .ph.r32{{aspect-ratio:3/2;object-position:50% 50%}}"
          f".ed .phc{{{fx('caption')};margin-top:8px;max-width:34rem;text-wrap:pretty}}"
          f".ed .card{{border-top:4px solid var(--oa-color-border-strong);padding-top:14px;position:relative;overflow:hidden}}"
          f".ed .card .hl{{{fx('h3')};margin:0 0 10px;position:relative;max-width:16ch}}"
          f".ed .card .dek{{position:relative;max-width:40ch}}"
          f".ed .dome{{position:absolute;right:-16px;top:36px;width:200px;height:auto;color:var(--oa-color-graphic-subtle)}}")
    ph = lambda src, crop, alt, cap: (f'<div class="phw"><img src="{src}" alt="{e(alt)}" class="ph {crop}" width="1920" height="1152" loading="lazy">'
                                      f'<p class="phc">{cap}</p></div>')
    dome = ('<svg class="dome" viewBox="0 0 260 200" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="3">'
            '<path d="M70 120 A60 60 0 0 1 190 120"/><path d="M60 120h140M55 132h150"/><path d="M130 60v-26M122 34h16"/>'
            '<path d="M80 132v52M100 132v52M120 132v52M140 132v52M160 132v52M180 132v52M40 186h180"/></svg>')
    rules.append({
        "id": "01.6", "title": "Show domes, columns and flags only in a captioned photograph of that place.",
        "rule": ["Show a capitol dome, columns or a flag only inside a documentary photograph of that place or event, with a caption that "
                 "names it. Keep them out of icons, backgrounds and textures."],
        "why": {"text": ["Campaigns in both parties use the dome and the flag as shorthand for government. As decoration they stand for no rule, "
                         "office or event, so they give the reader nothing to check or act on."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-6-correct", '<div class="ed">' + ph(PHOTO_PARKS, "r53", "Mourners file past a casket ringed by velvet ropes in the Capitol Rotunda, under its paintings and statues.", e(CAP_PARKS)) + "</div>",
                                  css=(BASE, PH), rule="01.6",
                                  alt="A documentary photograph of the U.S. Capitol Rotunda, its pilasters, framed paintings and statues above a line of people "
                                      "filing past a casket inside velvet ropes, with Capitol Police officers among them. Caption: " + CAP_PARKS,
                                  notes="DR-101, round two: the research lead's recommended photograph (pho-01 in the rights ledger), a public-domain work of the "
                                        "Architect of the Capitol, from Wikimedia's 1,920 px rendition. Cropped by CSS to 5:3 from the top, so the agency's mark at "
                                        "lower right falls outside the frame. No public-domain photograph of the H.R. 7008 vote day was found, so the caption names this event."),
                    "caption": "The Capitol Rotunda appears only as the place where a named public event happened, and the caption says what, where and when, with the credit. The crop keeps the walls and the public and leaves out the agency’s mark."},
        "failure": {"specimen": A("s-01-6-failure", f'<div class="ed"><div class="card">{dome}{kicker("Explainer", "Congress")}'
                                                    '<p class="hl">What the Senate vote on the Stop Insider Trading Act means for you</p><p class="dek">One vote, 53 to 47, and what comes next.</p></div></div>',
                                  css=(BASE, PH), rule="01.6", width=360,
                                  alt="An explainer card with a line drawing of a capitol dome and columns behind the headline, What the Senate vote on the Stop Insider Trading Act means for you."),
                    "caption": "The dome behind the headline decorates a story about one vote and borrows the look of campaign mail, and the card names no office."},
        "specs": [{"label": "Photograph", "value": "Documentary, of the place where a named public event happened"},
                  {"label": "Crop", "value": "Keep the building as the setting and the people in it; crop any agency mark"},
                  {"label": "Caption", "value": "What happened, where and when, then the credit"}],
        "files": [PHOTO_PARKS],
        "related": ["16", "12"],
        "builders": "Build cards from type and the brand’s own devices. A dome, a column or a flag enters only with a documentary photograph, its caption and its credit, logged in the rights ledger.",
    })

    ballot = lambda fail: (f'<div class="ed"><div class="card">{kicker("Explainer", "Ballot measures", illus=True)}'
                           '<p class="hl">What a yes vote and a no vote on Measure B would do</p>'
                           '<p class="dek">Alder County’s bond for road repairs, on the March 2027 ballot.</p>'
                           + ('<div class="gear"><span class="cbtn">YES<br>ON B</span><span class="plac">STOP THE TAX</span></div>' if fail else
                              '<div class="docref"><p class="lab">Document</p><p>Alder County, Measure B, ballot text and the county counsel’s summary, March 2027.</p></div>')
                           + "</div></div>")
    BCSS = (f".ed .gear{{display:flex;gap:16px;align-items:center;margin-top:12px}}"
            f".ed .cbtn{{display:flex;align-items:center;justify-content:center;text-align:center;width:104px;height:104px;border-radius:50%;border:4px solid var(--oa-color-border-strong);background:var(--oa-color-surface-white);{fx('h4')}}}"
            f".ed .plac{{display:inline-block;padding:18px 16px;border:4px solid var(--oa-color-border-strong);background:var(--oa-color-surface-white);{fx('h4')}}}"
            f".ed .docref{{border:1px solid var(--oa-color-border-strong);background:var(--oa-color-surface-white);padding:12px 14px;margin-top:12px}}")
    rules.append({
        "id": "01.7", "title": "Keep party symbols, candidate photos, campaign gear and protest slogans out of brand graphics.",
        "rule": ["Keep party symbols, candidate photographs, campaign merchandise and legible protest slogans out of brand graphics, since each "
                 "takes a side the piece never argued. A party’s logo may appear as evidence, inside a sourced document the piece reproduces."],
        "why": {"text": ["A reader takes any symbol on our page as ours. A campaign button or a slogan placard reads as an endorsement, even when the story beside it is neutral."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-7-correct", ballot(False), css=(BASE, PH, BCSS), rule="01.7", illustrative=True, width=360,
                                  alt="An illustrative explainer card: What a yes vote and a no vote on Measure B would do. Below it, a document reference to the measure's ballot text and the county counsel's summary."),
                    "caption": "The card explains both votes and points to the ballot text as its document."},
        "failure": {"specimen": A("s-01-7-failure", ballot(True), css=(BASE, PH, BCSS), rule="01.7", illustrative=True, width=360,
                                  alt="The same card with a campaign button reading YES ON B and a protest placard reading STOP THE TAX."),
                    "caption": "The button and the placard take sides on a measure the card set out to explain, so a reader on either side stops at the picture."},
        "related": ["16", "23"],
        "builders": "When a story needs a party’s logo or a campaign’s material, place the whole document as a sourced image with its credit, never the symbol by itself.",
    })

    rules.append({
        "id": "01.8", "title": "Photograph people doing public work, and caption who, what, where and when.",
        "rule": ["Choose photographs of people of different ages, places and roles doing public work, officials among them. Every caption "
                 "names who is shown, what they are doing, where and when."],
        "why": {"text": ["A reader trusts a picture of a real hearing more than a picture of the idea of one, and a full caption lets them check it."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-8-correct", '<div class="ed">' + ph(PHOTO_ZIANNO, "r32", "An official points to a project map while two residents, seen from behind, listen.", e(CAP_ZIANNO)) + "</div>",
                                  css=(BASE, PH), rule="01.8",
                                  alt="A documentary photograph of a public meeting: a federal official facing the camera points to a large map of Lake Isabella while two "
                                      "residents, seen from behind, listen; a board at left reads Steps in the real estate process. Caption: " + CAP_ZIANNO,
                                  notes="DR-101, round two: the research lead's recommended photograph (pho-04), a public-domain work of the U.S. Army Corps of Engineers, from "
                                        "Wikimedia's 1,920 px rendition, cropped by CSS to 3:2. Chosen over the Menniti frame from the same meeting because the named "
                                        "official faces the camera, so the caption's who is the person a reader sees, and the residents, who are not named, face away."),
                    "caption": "The caption names the official and his job, what he is doing, where and when, then the credit. The residents face away and stay unnamed."},
        "failure": {"specimen": A("s-01-8-failure", '<div class="ed">' + ph(PHOTO_ZIANNO, "r32", "The same photograph of the public meeting.", "Democracy in action. " + ill()) + "</div>",
                                  css=(BASE, PH), rule="01.8",
                                  alt="The same photograph of the public meeting, captioned only Democracy in action, a caption invented for this example and labeled Illustrative."),
                    "caption": "The caption names no person, act, place or date, so a reader cannot check the picture and learns nothing from it."},
        "specs": [{"label": "Caption", "value": "Who is shown, what they are doing, where and when, then the credit"},
                  {"label": "People", "value": "Name officials by their role; leave residents unnamed unless the record names them"},
                  {"label": "Crop", "value": "3:2, keeping the official, the people they serve and what the meeting is about"}],
        "files": [PHOTO_ZIANNO],
        "related": ["16"],
        "builders": "Write the caption’s four parts before a photograph goes in: who, what, where and when. Take them from the agency’s own caption and log the photograph in the rights ledger.",
    })

    # --- Group 3: choosing examples -----------------------------------------------------------------------------
    n, dom, states = tally()
    TCSS = (".ed.tal td.c{white-space:nowrap;font-variant-numeric:tabular-nums}.ed.tal th[scope=row]{font-weight:400}.ed .log th[scope=row]{font-weight:700}"
            "@media (max-width:79.99em){.ed table.log,.ed table.log tbody,.ed table.log tr,.ed table.log th,.ed table.log td{display:block;width:100%}"
            ".ed table.log thead{display:none}.ed table.log tr{border-bottom:1px solid var(--oa-color-border-strong);padding:10px 0}"
            ".ed table.log th,.ed table.log td{border:0;padding:3px 0}.ed table.log td[data-k]::before{content:attr(data-k) \": \";font-weight:700}}"
            ".ed.tal .bar1{display:inline-block;height:10px;background:var(--oa-color-data-emphasis);vertical-align:0}"
            ".ed .vh{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}")
    top = max(dom.values())
    trs = "".join(f'<tr><th scope="row">{e(DOMAINS[d])}</th><td class="c">{dom[d]} of {n}</td></tr>'
                  for d in sorted(dom, key=lambda k: (-dom[k], k)))
    limit = n / 4
    st_names = [s for s in NAMED_STATES if states[s]]
    many = [x for x in st_names if states[x] > 1]
    ones = [x for x in st_names if states[x] == 1]
    def joined(xs):
        return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]
    parts = []
    for cnt in sorted({states[x] for x in many}, reverse=True):
        grp = [x for x in many if states[x] == cnt]
        parts.append(f"{joined(grp)} supplies {SPELL[cnt]} examples" if len(grp) == 1
                     else f"{joined(grp)} supply {SPELL[cnt]} examples each")
    st_line = (", ".join(parts) + (", and " if many else "")
               + joined(ones) + (" one each" if many else " supply one example each"))
    st_max = max(states.values())
    import math
    tal_ok = (f'<div class="ed tal"><p class="ct">This chapter’s {n} examples by atlas domain</p><p class="cm">One in four of {n} is {limit:g}, so no domain may supply {SPELL[math.floor(limit) + 1]}. '
              f'{st_line}.</p><table><thead><tr><th scope="col">Domain</th><th scope="col">Examples</th></tr></thead><tbody>{trs}</tbody></table></div>')
    bad = [("Elections and representation", 3), ("Money, lobbying and influence", 1), ("Taxes, wealth and economic security", 1)]
    tal_bad = (f'<div class="ed tal"><p class="ct">A draft chapter’s five examples by domain and state</p><p class="cm">Three of five come from one domain, and three of five from Massachusetts.</p><table class="stack"><thead><tr><th scope="col">Domain</th><th scope="col">Examples</th><th scope="col">From Massachusetts</th></tr></thead><tbody>'
               + "".join(f'<tr><th scope="row">{e(a)}</th><td class="c" data-k="Examples">{b} of 5</td><td class="c" data-k="From Massachusetts">{["3", "0", "0"][i]}</td></tr>' for i, (a, b) in enumerate(bad)) + "</tbody></table></div>")
    rules.append({
        "id": "01.9", "title": "Draw no more than one example in four from one atlas domain, or one in five from one state.",
        "rule": ["Count examples within one unit: a chapter of this guide, a report, or a month of newsletter issues. Draw no more than one "
                 "in four from any one of our systems atlas’s ten domains, and no more than one in five from any one state."],
        "why": {"text": ["A run of examples from one subject or one state tells readers whose problems we care about. Rotation keeps a reader in "
                         "Texas and a reader in Maine in view of the same chapter."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-9-correct", tal_ok, css=(BASE, CHART, TCSS), rule="01.9", readable=True,
                                  alt=f"A table of this chapter's {n} examples by atlas domain. The largest count is {top} of {n}, under the one-in-four limit. " +
                                      "; ".join(f"{DOMAINS[d]}: {dom[d]}" for d in sorted(dom)) + f". {st_line}."),
                    "caption": f"This chapter checked against its own rule: no domain supplies more than {SPELL[top]} of its {n} examples, under one in four, and no named state supplies more than {SPELL[st_max]}, under one in five."},
        "failure": {"specimen": A("s-01-9-failure", tal_bad, css=(BASE, CHART, TCSS), rule="01.9", illustrative=True, readable=True,
                                  alt="An illustrative tally of a draft chapter's five examples: three from elections and representation, and three from Massachusetts."),
                    "caption": "Three election examples from one state would tell readers elsewhere that the chapter was written for someone else."},
        "related": ["13"],
        "builders": "Count from the rotation log before a chapter, report or month of issues runs, using the atlas’s ten domains by their full names.",
    })

    LCSS = (f".ed .lv{{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,150px),1fr));gap:16px}}"
            f".ed .lv>div{{border-top:2px solid var(--oa-color-border-strong);padding-top:8px}}.ed .lv .lab{{margin-bottom:4px}}"
            f".ed .lv ul{{list-style:none;margin:0;padding:0}}.ed .lv li{{{fx('body-small')};margin-top:8px}}"
            f".ed .lv .rg{{display:block;{fx('caption')};color:var(--oa-color-text-secondary)}}")
    lv = lambda items: "<ul>" + "".join(f'<li>{t}<span class="rg">{e(r)}</span></li>' for t, r in items) + "</ul>"
    lv_ok = ('<div class="ed"><div class="lv">'
             f'<div><p class="lab">Federal</p>{lv([("The Stop Insider Trading Act in Congress", "National"), ("The Senate’s cloture rule", "National"), ("Rosa Parks lying in honor at the Capitol", "National"), ("A public meeting on a federal dam project in California", "West")] + ([("Court cases after the 2020 presidential election", "Six states, in all four regions")] if UNEVEN else []))}</div>'
             f'<div><p class="lab">State</p>{lv([("Map redraws in Texas and California", "South and West"), ("Minimum wage floors: Ohio’s rises each year by formula, and Pennsylvania’s stays at the federal $7.25", "Midwest and Northeast"), ("Posting committee votes " + ill(), "No region")])}</div>'
             f'<div><p class="lab">County or city</p>{lv([("Backyard cottages in Alder County " + ill(), "No region"), ("Property tax rates", "Every region")])}</div>'
             f'<div><p class="lab">School district</p>{lv([("A bell schedule vote " + ill(), "No region")])}</div></div>'
             f'<p class="src">{e(SRC_MINWAGE)}</p></div>')
    lv_bad = ('<div class="ed"><div class="lv">'
              f'<div><p class="lab">Federal</p>{lv([("The cloture rule", "National"), ("The Stop Insider Trading Act", "National"), ("The debt limit", "National"), ("Medicare drug prices", "National")])}</div>'
              f'<div><p class="lab">State</p>{lv([("None", "")])}</div><div><p class="lab">County or city</p>{lv([("None", "")])}</div><div><p class="lab">School district</p>{lv([("None", "")])}</div></div></div>')
    rules.append({
        "id": "01.10", "title": "Rotate examples across levels of government and regions.",
        "rule": ["Draw examples from federal, state, county or city, and school district decisions, and from every region of the country: "
                 "the Northeast, the Midwest, the South and the West."],
        "why": {"text": ["Most of the rules that reach a household are written below the federal level. A reader who only ever sees Congress learns that the decisions nearest to them are not worth following."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-10-correct", lv_ok, css=(BASE, LCSS), rule="01.10", readable=True,
                                  alt="This chapter's examples sorted by level, each with its region. Federal: the Stop Insider Trading Act in Congress, the Senate's cloture rule and Rosa Parks lying in honor at the Capitol, national; a public meeting on a federal dam project in California, West" + ("; court cases after the 2020 presidential election, six states in all four regions. " if UNEVEN else ". ") +
                                      "State: map redraws in Texas and California, South and West; minimum wage floors, Ohio's rising each year by formula and Pennsylvania's at the federal $7.25, Midwest and Northeast; posting committee votes, illustrative. "
                                      "County or city: backyard cottages in Alder County, illustrative; property tax rates, every region. School district: a bell schedule vote, illustrative. " + SRC_MINWAGE),
                    "caption": "This chapter’s examples reach all four levels, and its real cases come from all four regions: Texas in the South, California in the West, Ohio in the Midwest and Pennsylvania in the Northeast."},
        "failure": {"specimen": A("s-01-10-failure", lv_bad, css=(BASE, LCSS), rule="01.10", readable=True,
                                  alt="A draft chapter with four federal examples and none at the state, county or city, or school district level."),
                    "caption": "Four federal examples in a row leave out the councils, boards and districts where a reader can most easily be heard."},
        "related": ["13", "21"],
        "builders": "Tag each row of the rotation log with its level and region, and look for an empty one before the piece runs.",
    })

    CASES = (f".ed .cases{{max-width:720px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px 28px}}"
             f".ed .cases div{{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}}"
             f".ed .cases .st{{{fx('h4')};margin:0 0 6px}}")
    tx = "In August 2025, Texas’s Republican-led legislature passed a congressional map aimed at five more Republican seats, and Governor Greg Abbott signed it."
    ca = "In August 2025, California’s Democratic-led legislature passed a congressional map aimed at five more Democratic seats, and voters approved it in November."
    if words(tx) != words(ca):
        raise SystemExit(f"Rule 01.11: the two cases differ in length ({words(tx)} and {words(ca)} words)")
    lead11 = '<p class="ct">Loop R4a, the map-drawing loop: majorities draw maps that help them keep control.</p>'
    rules.append({
        "id": "01.11", "title": "Show a case from each party that uses a mechanism, and report the counts as the record gives them.",
        "rule": ["When majorities of both parties use the same mechanism, show a documented case from each, described in the same form and "
                 "at the same length. The test case is Loop R4a, the map-drawing loop, which our systems atlas titles “Majorities draw "
                 "maps that help them keep control.”",
                 RULE_11_ADDED],
        "why": {"text": [RULE_11_WHY],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-11-correct", f'<div class="ed">{lead11}<div class="cases"><div><p class="st">Texas</p><p>{e(tx)}</p></div>'
                                                     f'<div><p class="st">California</p><p>{e(ca)}</p></div></div><p class="src">{e(SRC_R4A)}</p></div>',
                                  css=(BASE, CHART, CASES), rule="01.11",
                                  alt=f"Loop R4a, the map-drawing loop. Two cases in the same form and at the same length. Texas: {tx} California: {ca} {SRC_R4A}",
                                  notes="BE-S1, CP-M5: both cases in one form, as the research lead's fix pass report sets them (task 3), with its source line. Both aims are each side's stated goal: Texas's stay application, and the California three-judge court's finding."),
                    "caption": f"Each case names the month, the majority that acted and the seats its map aimed at, then the last step its state required, in {words(tx)} words. Texas’s map became law with the governor’s signature; California’s needed a constitutional amendment only voters could approve."},
        "failure": {"specimen": A("s-01-11-failure", f'<div class="ed">{lead11}<div class="cases"><div><p class="st">Texas</p><p>{e(tx)}</p></div></div><p class="src">{e(SRC_R4A)}</p></div>',
                                  css=(BASE, CHART, CASES), rule="01.11",
                                  alt=f"The same loop with only the Texas case: {tx}"),
                    "caption": "The record holds a case from each party, so a piece that shows Texas alone drops a finding, and the loop reads as a charge against one party."},
        "related": ["15", "13"],
        "builders": ("Before a piece runs a mechanism, count the atlas’s case records for that loop by the party of the majority, and print "
                     "the counts with their source when one party leads. Pick one case from each party that uses the mechanism, and "
                     "write the cases in the same form."),
    })
    if UNEVEN:
        # DR-125: the research lead's sentences and source line, printed exactly as written, with the grade they are sized to.
        UCSS = (f".ed .unv{{max-width:640px;border-top:2px solid var(--oa-color-border-strong);padding-top:12px}}"
                f".ed .unv .lab{{margin:0 0 8px}}.ed .unv .ln{{{fx('body')};margin:0 0 8px}}")
        ulines = "".join(f'<p class="ln">{e(x)}</p>' for x in UNEVEN["lines"])
        extras_uneven = [{"after_rule": "01.11", "label": "A finding that falls on one side",
                          "specimen": A("s-01-uneven", f'<div class="ed"><div class="unv"><p class="lab">{e(UNEVEN["grade"])}</p>{ulines}'
                                                       f'<p class="src">{e(UNEVEN["source"])}</p></div></div>',
                                        css=(BASE, UCSS), rule=None, readable=True, label="A finding that falls on one side",
                                        alt=f"A finding graded {UNEVEN['grade'].lower()}, reported as the record shows it. "
                                            + " ".join(UNEVEN["lines"]) + " " + UNEVEN["source"] + (" " + UNEVEN["alt_note"] if UNEVEN.get("alt_note") else ""),
                                        notes="DR-125 and atlas issue I155: the research lead's sentences and source line, printed as written "
                                              "(work/handoffs/phase-2/20261107_Apply-Pass-Research.md, section 1)."),
                          "caption": ("The lines name who acted and what the record shows, in words sized to the grade, and they add no "
                                      "case from another party to even the count, as Rule 01.11 asks.")}]
    else:
        extras_uneven = []

    LOGH = ('<table class="stack log"><thead><tr><th scope="col">Example</th><th scope="col">Domain</th><th scope="col">State</th>'
            '<th scope="col">Region</th><th scope="col">Level</th><th scope="col">Coalition behind any reform shown</th></tr></thead><tbody>')
    log_rows = [x for x in EXAMPLES if x[0] in ("Minimum wage floors", "Mid-decade map redraws", "Citizen initiatives", "Backyard cottages", "Posting committee votes, S. 214")]
    log_ok = (f'<div class="ed tal"><p class="ct">Rotation log, chapter 01, five of its {n} rows</p>' + LOGH
              + "".join(f'<tr><th scope="row">{e(a)}{" " + ill() if il else ""}</th><td data-k="Domain">{e(DOMAINS[d])}</td><td data-k="State">{e(s)}</td><td data-k="Region">{e(rg)}</td>'
                        f'<td data-k="Level">{e(l)}</td><td data-k="Coalition">{e(c)}</td></tr>' for a, d, s, rg, l, c, il, _ in log_rows)
              + "</tbody></table></div>")
    log_bad = (f'<div class="ed tal"><p class="ct">Rotation log, a draft row</p>' + LOGH
               + '<tr><th scope="row">Town library hours</th><td data-k="Domain">(blank)</td><td data-k="State">Massachusetts</td><td data-k="Region">(blank)</td><td data-k="Level">(blank)</td><td data-k="Coalition">(blank)</td></tr></tbody></table></div>')
    rules.append({
        "id": "01.12", "title": "Log each example’s domain, state, region, level and backing coalition.",
        "rule": ["Log every example with its atlas domain, its state and region, its level of government and, for any reform shown, the coalition "
                 "that usually backs it. Our editors review the log before each chapter, report or series runs."],
        "why": {"text": ["A chapter can lean toward one topic or one side without anyone noticing. A log turns the spread of examples into counts anyone can check, including a reader who suspects a lean."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-12-correct", log_ok, css=(BASE, CHART, TCSS), rule="01.12", readable=True,
                                  alt="A rotation log table with five of this chapter's rows, each with example, domain, state, region, level and the coalition behind any reform shown."),
                    "caption": "Every field is filled, and an invented example says so in the state, region and coalition columns."},
        "failure": {"specimen": A("s-01-12-failure", log_bad, css=(BASE, CHART, TCSS), rule="01.12", illustrative=True, readable=True,
                                  alt="An illustrative log row for town library hours in Massachusetts with the domain, region, level and coalition left blank."),
                    "caption": "A row with blank fields cannot be counted, so whoever checks the log cannot see a run of one topic or one side’s reforms."},
        "related": ["13", "28"],
        "builders": "Keep one log row per example in the piece’s notes and count domains, states and regions from it before it runs.",
    })

    # --- Group 4: words -------------------------------------------------------------------------------------------
    LINES = (f".ed .lnbox{{max-width:640px;border-top:2px solid var(--oa-color-border-strong);padding-top:12px}}"
             f".ed .ln{{{fx('intro')};margin:0}}.ed .ln.h{{{fx('h3')}}}"
             f".ed .ln+.src{{margin-top:10px}}")
    line = lambda t, src="", illus=False, head=False, kick="": (f'<div class="ed"><div class="lnbox">{kick}<p class="ln{" h" if head else ""}">{e(t)}{" " + ill() if illus else ""}</p>'
                                                                + (f'<p class="src">{e(src)}</p>' if src else "") + "</div></div>")
    t13 = "For an investor-owned utility, the state public utility commission sets your rate in a rate case, its formal review of the utility’s request."
    rules.append({
        "id": "01.13", "title": "Name the office that decides, and name a party only when party is part of the finding.",
        "rule": ["Say which office or body makes the decision. Name a party only when party is part of the finding, such as a party-line "
                 "vote or a record that shows one party doing more of something, and give the count and its source."],
        "why": {"text": ["A reader can call an office or testify before it, and at the next election they can vote out its members or the official who appointed them. A party’s name in place of an office gives them a team to blame and nobody to call."],
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
        "why": {"text": ["A question that assumes the reader is angry tells half our readers the piece is for someone else. Who decided, and when the rule could change, are things a reader on either side of it wants to know."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-14-correct", line("Who sets your property tax rate, and when could it change?", head=True), css=(BASE, LINES), rule="01.14",
                                  alt="A headline question: Who sets your property tax rate, and when could it change?"),
                    "caption": "A homeowner who likes today’s rate and one who wants it lower would both click this question."},
        "failure": {"specimen": A("s-01-14-failure", line("Who wrote the rule you are angry about?", "Our brand guide, fifth edition, chapter 13 In use", head=True), css=(BASE, LINES), rule="01.14",
                                  alt="A headline question quoted from our brand guide's fifth edition, chapter 13: Who wrote the rule you are angry about?"),
                    "caption": "The question assumes the reader is angry and that someone wronged them, so a reader who likes the rule has no reason to read on."},
        "related": ["02", "23"],
        "builders": "Search a draft for the words this rule lists, and read each question as someone who likes the current rule would.",
    })

    rules.append({
        "id": "01.15", "title": "Use plain verbs in place of war and sports metaphors.",
        "rule": ["Describe a public decision in the words for what happens, such as propose, debate, vote and pass. Leave out war and sports "
                 "metaphors such as fight, battle, front and game plan."],
        "why": {"text": ["A war or a game needs an enemy or a loser, and the people on the other side of a vote are our readers too. The verbs for what happens also tell a reader where the decision stands."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-15-correct", line("The state senate votes on the overtime rule Thursday.", illus=True, head=True, kick=kicker("Report", "Dispatch")),
                                  css=(BASE, LINES), rule="01.15",
                                  alt="A kicker, Report, Dispatch, over an illustrative headline: The state senate votes on the overtime rule Thursday."),
                    "caption": "The series name is Dispatch, and the headline names the vote and its day. Only the headline is invented, so the label sits beside it."},
        "failure": {"specimen": A("s-01-15-failure", line("The battle over overtime heads to the senate floor.", illus=True, head=True, kick=kicker("Report", "Dispatch from the Front")),
                                  css=(BASE, LINES), rule="01.15",
                                  alt="Our fifth edition's series name, Dispatch from the Front, in the kicker over an illustrative headline: The battle over overtime heads to the senate floor."),
                    "caption": "“From the Front”, our fifth edition’s series name, and “battle” cast the vote as a war with an enemy, and the headline never says when the vote happens."},
        "related": ["02"],
        "builders": "Search a draft for fight, battle, front, war and game plan, and name the step in the process in its place.",
    })

    ra = "Economists at Harvard University find that faster productivity growth has still brought faster pay growth for typical and average workers, in the authors’ estimates."
    rb = "Economists at the Economic Policy Institute find that typical workers’ pay has grown far more slowly than productivity since 1979, in the authors’ measures."
    if words(ra) != words(rb):
        raise SystemExit(f"Rule 01.16: the two readings differ in length ({words(ra)} and {words(rb)} words)")
    RCSS = (f".ed .rd{{max-width:720px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px 28px}}"
            f".ed .rd div{{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}}"
            f".ed .rd .small{{{fx('caption')};color:var(--oa-color-text-secondary);border-top-width:1px}}")
    lead16 = '<p class="ct">Does pay rise with productivity?</p><p class="cm">Credible studies disagree. Two readings, at the same length.</p>'
    rules.append({
        "id": "01.16", "title": "Show both readings of a contested claim at the same length.",
        "rule": ["When credible studies disagree, which is what the grade contested means, give the two readings equal length, the same verbs "
                 "and the same type, and name who holds each one in the same form. A claim with any other grade takes one reading, at the "
                 "strength its grade allows, and no piece adds a second reading to even the score."],
        "why": {"text": ["Equal space is how a reader sees that the disagreement is real. A long reading beside a short dismissal, or a credential on one side and a tag on the other, tells them which side we prefer before they weigh either. "
                         "A second reading added to a claim no credible study disputes would invent a disagreement."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-16-correct", f'<div class="ed">{lead16}<div class="rd"><div><p class="lab">One reading</p><p>{e(ra)}</p></div><div><p class="lab">The other reading</p><p>{e(rb)}</p></div></div><p class="src">{e(SRC_PAY)}</p></div>',
                                  css=(BASE, CHART, RCSS), rule="01.16",
                                  alt=f"Does pay rise with productivity? Two readings at the same length, {words(ra)} words each, in the same type. One: {ra} The other: {rb} {SRC_PAY}",
                                  notes="BE-M2, CP-S6: both holders by role and affiliation in one form, as the research lead's report sets them (task 5). The first reading follows the paper's abstract, which covers median and average pay."),
                    "caption": f"Each reading runs {words(ra)} words, uses the verb “find” and names who holds it by role and affiliation."},
        "failure": {"specimen": A("s-01-16-failure", f'<div class="ed">{lead16}<div class="rd"><div><p class="lab">What the research shows</p><p>{e(ra)}</p></div><div class="small"><p>Some critics disagree.</p></div></div></div>',
                                  css=(BASE, CHART, RCSS), rule="01.16",
                                  alt="The first reading set in full under the label What the research shows, and the second cut to three words in small gray type: Some critics disagree."),
                    "caption": "One reading becomes “the research” and the other three small words, so the layout settles a question the evidence leaves open."},
        "related": ["13", "14"],
        "builders": ("Look up the claim’s grade in our systems atlas first, and use this block only when the grade is contested. Set both "
                     "readings in one two-column block with matching labels, describe both holders in the same words, and count the words "
                     "of each before you publish."),
    })

    t17 = "The filibuster lets senators keep debating a bill until 60 of them vote to end debate, a vote called cloture."
    rules.append({
        "id": "01.17", "title": "Describe a rule so its supporters would accept the description.",
        "rule": ["Read your description of a rule as someone who supports it would. If they would object to the words, rewrite the description "
                 "until they would accept it, and save the argument for a labeled position piece."],
        "why": {"text": ["Readers who back a rule are among the people we serve, and many are the officials we ask readers to contact, so the description has to hold for them as well."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-17-correct", line(t17, SRC_CLOTURE), css=(BASE, LINES), rule="01.17",
                                  alt=f"{t17} {SRC_CLOTURE}"),
                    "caption": "A senator who values the 60-vote rule and one who wants it gone would both sign off on this sentence about the same rule."},
        "failure": {"specimen": A("s-01-17-failure", line("The filibuster lets a minority of senators hold the country hostage.", illus=True), css=(BASE, LINES), rule="01.17", illustrative=True,
                                  alt="An illustrative line: The filibuster lets a minority of senators hold the country hostage."),
                    "caption": "“Hold the country hostage” is an opponent’s charge, so a senator who values the rule would reject the sentence before reaching the facts."},
        "related": ["13", "02"],
        "builders": "Before the piece runs, read the description in the place of someone who supports the rule, and mark every word they would change.",
    })

    # --- Group 5: hinge headlines ---------------------------------------------------------------------------------
    hh = lambda a, b, fail=False: (f'<div class="ed"><p class="hh">{e(a)} {amp_h()} '
                                   + (f'<span style="color:var(--oa-color-palette-pillar-red)" data-red="failure">{e(b)}</span>' if fail else e(b)) + "</p></div>")
    rules.append({
        "id": "01.18", "title": "Set both halves of a hinge headline in one color and weight, and give the red to the ampersand.",
        "rule": ["Set both noun phrases of a hinge headline in the same ink, face and weight. The ampersand takes the view’s working red, unless "
                 "an error or a step on the same view already holds it; then the ampersand takes the headline’s ink, as Rule 04.3 sets out."],
        "tokens": ["oa.font.family.display", "oa.color.palette.pillarRed"],
        "why": {"text": ["When one half is red or heavier, the headline takes a side between a rule and its result. Equal halves leave the joining to the ampersand."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-18-correct", hh("The overtime rule", "the paycheck."), css=(BASE, HL), rule="01.18",
                                  alt="A hinge headline: The overtime rule and the paycheck. Both halves in Charcoal Inter Tight ExtraBold; only ampersand B is red."),
                    "caption": "Both halves share Charcoal and ExtraBold, and ampersand B carries the red."},
        "failure": {"specimen": A("s-01-18-failure", hh("The overtime rule", "the paycheck.", True), css=(BASE, HL), rule="01.18", exempt=["red", "contrast"],
                                  alt="The same headline with the second half, the paycheck, also set in red."),
                    "caption": "The red second half reads as the alarm and the first half as its cause, and the ampersand no longer stands out as the join."},
        "files": [AMP16, AMP24],
        "related": ["04", "02"],
        "builders": "Set the headline in Inter Tight ExtraBold and place ampersand B at the cap height in place of the font’s ampersand, from the master Rule 04.3 names for the size.",
    })

    PP = ".ed.pp{display:grid;gap:28px}.ed.pp .lab{margin:0 0 6px}"
    rules.append({
        "id": "01.19", "title": "Join people through a rule or place they share, and rotate their order.",
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
        "builders": "Log the order of each pair of people, and swap it the next time a piece joins the same two groups.",
    })

    dek20 = (f"In a May 2023 survey, {sv['support-democrats']} percent of Democrats and {sv['support-republicans']} percent of Republicans "
             f"favored a ban on stock trading by members of Congress.")
    rules.append({
        "id": "01.20", "title": "Name parties, the left or the right in a hinge headline only to report sourced agreement.",
        "rule": ["Use “left”, “right” or a party’s name in a hinge headline only to report a point where the sides agree, such as a bill with "
                 "sponsors from both parties. Join the two through what they agree on, as Rule 01.19 asks of every pair of people, and "
                 "source the agreement in the deck."],
        "why": {"text": ["A red ampersand between two sides would mark the sides themselves, against Rule 01.1. Reporting agreement is the one case where naming the sides in a hinge headline helps a reader."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-20-correct", f'<div class="ed"><p class="hh">Democratic voters {amp_h()} Republican voters on a stock trading ban.</p><p class="dk2">{e(dek20)}</p><p class="src">{e(SRC_STOCK_SURVEY)}</p></div>',
                                  css=(BASE, HL, f".ed .dk2{{{fx('intro')};margin-top:12px}}"), rule="01.20",
                                  alt=f"A hinge headline: Democratic voters and Republican voters on a stock trading ban. Deck: {dek20} {SRC_STOCK_SURVEY}"),
                    "caption": "The headline joins both parties’ voters through the ban they agree on, and the deck gives the figures and their source."},
        "failure": {"specimen": A("s-01-20-failure", f'<div class="ed"><p class="hh">The left {amp_h()} the right.</p></div>', css=(BASE, HL), rule="01.20",
                                  alt="A hinge headline: The left and the right."),
                    "caption": "The red ampersand sits between two sides with no shared fact, so it marks the divide and reports nothing."},
        "related": ["04", "02"],
        "builders": "When a headline names the sides, link the deck’s source line to the vote, the sponsor list or the survey that shows the agreement.",
    })

    # --- Group 6: labels, Act pieces and names ------------------------------------------------------------------------
    KCSS2 = (f".ed .kl{{display:grid;gap:12px;max-width:600px}}.ed .kl>div{{border-top:1px solid var(--oa-color-border-hairline);padding-top:10px}}"
             f".ed .kl .kick{{margin:0 0 4px}}.ed .kl .kt{{{fx('body')}}}.ed .kl .kw{{{fx('caption')};color:var(--oa-color-text-secondary);margin-top:4px}}")
    kl = [("Explainer", "Utility rates", "Why is my electric bill going up?", False, None),
          ("Tracker", "Congress", HR7008_TRACKER, False, None),
          ("Analysis", "Productivity", "Does pay rise with productivity?", False, "CL-055"),
          ("Report", "State legislatures", "Oath & Action Report 3: How state committees record their votes", True, None),
          ("Guide", "Field Notes", "Who answers for the repair on your street?", True, None),
          ("Act · How to take part", None, "Alder County votes on backyard cottages March 9.", True, None),
          ("Our position", "Committee votes", "State senate committees should post every vote within two days.", True, None)]
    kl_ok = '<div class="ed"><div class="kl">' + "".join(
        f'<div>{kicker(a, b, icon=ic)}<p class="kt">{e(h)}{" " + ill() if il else ""}</p></div>' for a, b, h, il, ic in kl) + "</div></div>"
    kl_bad = ('<div class="ed"><div class="kl">'
              f'<div><p class="kick"><span class="lb">Explain</span></p><p class="kt">Why is my electric bill going up?</p><p class="kw">A pillar name alone</p></div>'
              f'<div><p class="kick"><span class="lb">Must read</span><span class="dot" aria-hidden="true">·</span><span class="sx">Breaking</span></p><p class="kt">State senate committees should post every vote within two days. {ill()}</p><p class="kw">Push words, and no label to say the piece argues a position</p></div>'
              f'<div><p class="kick"><span class="lb">Field Notes</span><span class="dot" aria-hidden="true">·</span><span class="sx">Guide</span><span class="dot" aria-hidden="true">·</span><span class="sx">Street repairs</span></p><p class="kt">Who answers for the repair on your street? {ill()}</p><p class="kw">The series first, the label second, and three parts</p></div>'
              f'<div><p class="kick">{cl_icon("CL-019", 24, cls="ki")}<span class="lb">Analysis</span><span class="dot" aria-hidden="true">·</span><span class="sx">Productivity</span></p><p class="kt">Does pay rise with productivity?</p><p class="kw">A pillar icon, Explain’s, beside a label that names no pillar</p></div>'
              '</div></div>')
    rules.append({
        "id": "01.21", "title": "Open every kicker with one content label.",
        "rule": ["Open the kicker, the short line above a headline, with one of the seven content labels in this rule’s specifications. At most "
                 "one more part follows, after a middle dot: the series name if the piece belongs to a series, otherwise its topic, as in "
                 "“Explainer · Local schools”. A newsletter issue carries no label in its header, and each story inside it carries its own.",
                 "Set the kicker in words. The one picture it may hold is a topic icon from the Civic Line, our set of symbols in chapter 10, "
                 "placed directly before the topic’s own word. Pillar icons belong to the pillar row, section openers and tiles, and never enter a kicker."],
        "tokens": ["oa.color.action.primary.fill.onNewsprint", "oa.size.icon.medium"],
        "why": {"text": ["The label tells a reader what kind of claim the piece makes before they read it, and whether we are reporting or arguing. "
                         "A topic icon beside its own word shows the subject a second way. A pillar icon in a kicker would sit beside a label such as "
                         "Report or Guide, which names no pillar, and leave the reader to decode the drawing."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-21-correct", kl_ok, css=(BASE, KCSS2), rule="01.21",
                                  alt="Seven kickers, one per content label, each over a headline. Explainer, utility rates: Why is my electric bill going up? "
                                      f"Tracker, Congress: {HR7008_TRACKER}. Analysis, productivity, with the Productivity topic icon, a worker at a desk beside a clock, directly before the word Productivity: Does pay rise with productivity? Report, state legislatures, "
                                      "illustrative. Guide, Field Notes, illustrative. Act, how to take part, illustrative. Our position, committee votes, "
                                      "in a Charcoal label, illustrative. The four invented headlines carry the Illustrative label."),
                    "caption": ("Each kicker opens with its label and adds at most a series or a topic. The Analysis kicker holds the one picture a "
                                "kicker may carry, the Productivity icon beside its own word. Only “Our position” takes the Charcoal fill, and the "
                                "first three headlines are real, so the label sits beside each invented one.")},
        "failure": {"specimen": A("s-01-21-failure", kl_bad, css=(BASE, KCSS2), rule="01.21",
                                  alt="Four kickers that break the rule. Explain, a pillar name alone. Must read and Breaking above an illustrative position headline, with no label. "
                                      "Field Notes, then Guide, then Street repairs: the series first, the label second and three parts. The same Analysis kicker "
                                      "with the Explain pillar icon before its label, in place of the Productivity icon."),
                    "caption": ("“Explain” is a pillar and says nothing about the claim, and “Must read” and “Breaking” push the reader while hiding "
                                "that the piece argues. The third kicker reaches its label only after the series. In the last, the Explain icon "
                                "codes a pillar that the label Analysis never names.")},
        "specs": [{"label": "Explainer", "value": "How a rule or a decision works"},
                  {"label": "Tracker", "value": "Where a decision stands, dated “as of”"},
                  {"label": "Analysis", "value": "What the evidence shows on a contested question"},
                  {"label": "Report", "value": "What the record shows about a decision, from a story in a series such as Dispatch to a numbered study"},
                  {"label": "Guide", "value": "How to reach the office that decides, for a Connect piece"},
                  {"label": "Act · How to take part", "value": "One step with its date and place; one label, with nothing after it"},
                  {"label": "Our position", "value": "An argument for or against a named measure, in the Charcoal label (Rule 01.23)", "token": "oa.color.action.primary.fill.onNewsprint"},
                  {"label": "Never a kicker", "value": "A pillar name alone, and a chart’s “Finding” line, which sits above the chart’s title as its evidence line"},
                  {"label": "Type", "value": "The label style, Inter 700 capitals at 13 px; the second part in the secondary text ink"},
                  {"label": "Topic icon", "value": "Optional: a Civic Line icon at 24 px in one color, 8 px before the topic’s own word, only when the second part is a topic", "token": "oa.size.icon.medium"},
                  {"label": "Never inside a kicker", "value": "A pillar icon, the lockmark, or an icon beside a label or a series name"}],
        "related": ["10", "13"],
        "builders": ("Pick the label from the seven in this rule. If a piece fits none of them, ask the editor before it runs. Add a topic "
                     "icon only when the kicker’s second part is the word that icon names, and keep pillar icons and the lockmark out of kickers."),
    })

    rules.append({
        "id": "01.22", "title": "In a process piece, name the step and leave the side to the reader.",
        "rule": ["An Act piece labeled “Act · How to take part” gives one step with its date and place, sets out what supporters and opponents "
                 "have said at the same length, and takes no side. Its ask is the view’s one working red."],
        "tokens": ["oa.color.action.ask.fill.onNewsprint", "oa.color.action.ask.label.onNewsprint", "oa.component.button.ask.keyline.onNewsprint"],
        "why": {"text": ["A reader of any view can use a process piece, because it tells them how to be heard and leaves what to say to them."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-22-correct", f'<div class="ed">{process_piece(False)}</div>', css=(BASE, ARTICLE), rule="01.22", illustrative=True, width=360,
                                  alt="An illustrative process piece. Kicker: Act, how to take part. Headline: Alder County votes on backyard cottages March 9. Send a comment by March 3 or speak at the meeting. Who decides: five county supervisors, and three votes pass the change. What each side has said: supporters said more homes would ease rents; opponents said sewers were sized for fewer homes. After the hinge divider, What you can do: send a written comment by 5 p.m. Wednesday, March 3, 2027, or speak for two minutes at 6 p.m. Tuesday, March 9, 2027. One red button: Send a comment. A line pointing to the Backyard Cottages Tracker."),
                    "caption": "The piece names who decides, gives both sides one sentence each, then turns at the hinge divider to two dated ways to take part. The red sits on the ask alone."},
        "failure": {"specimen": A("s-01-22-failure", f'<div class="ed">{process_piece(True)}</div>', css=(BASE, ARTICLE), rule="01.22", illustrative=True, width=360,
                                  alt="The same piece with only the supporters' case, under the label Why it matters, and a red button reading Tell the supervisors to vote yes."),
                    "caption": "The piece keeps the process label and then argues one side, so a reader who opposes the change meets a position they were told was not there."},
        "specs": [{"label": "Kicker", "value": "Act · How to take part, the label alone"},
                  {"label": "Ask", "value": "Pillar Red fill, White label at 19 px bold, Charcoal keyline on Newsprint", "token": "oa.color.action.ask.fill.onNewsprint"},
                  {"label": "Before the ask", "value": "The hinge divider, its ampersand in the surface’s ink", "token": "oa.color.identity.hingeDivider.onNewsprint"},
                  {"label": "Width", "value": "Shown as a phone page, 360 px wide, with the phone sizes of the type scale; on a wider screen the column grows to the reading measure"}],
        "related": ["13", "12", "18"],
        "builders": "Build the ending from the hinge divider, the “What you can do” line and one ask button. Link the neutral tracker, never a campaign page.",
    })

    kit = [("Label first", "“Our position” opens the kicker, before the headline, and a shared card keeps it top left."),
           ("The strongest case against", "The opposing case as its supporters would put it, sourced, at least a third of the argument’s length."),
           ("Grades kept", "Every claim keeps its evidence grade, and its verb matches the grade."),
           ("Opponents by role", "Name opponents by office or role, and cast no party as a villain."),
           ("What we don’t know", "The open questions, named."),
           ("Process facts", "Who decides, when and how, word for word as the neutral tracker gives them."),
           ("Disclosure", "Who decided the position and when, any funder’s interest in the measure, and links to the bios of those who decided, above the ask."),
           ("Kept out of the record", "Positions stay out of the atlas, the trackers and the data.")]
    rules.append({
        "id": "01.23", "title": "Put a position piece’s label before the headline and its fairness kit before the ask.",
        "rule": ["A piece that asks readers to support or oppose a named measure opens its kicker with the label “Our position”, before the "
                 "headline. Before the ask it carries the fairness kit, the eight parts in this rule’s specifications, among them the "
                 "strongest case against the position, what we don’t know and who decided."],
        "tokens": ["oa.color.action.primary.fill.onNewsprint", "oa.color.action.ask.fill.onNewsprint"],
        "why": {"text": ["A reader who disagrees with us can still trust the rest of our coverage when each argument carries its label, its strongest opposing case and the names of the people who decided it."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-23-correct", f'<div class="ed">{position_piece(False)}</div>', css=(BASE, ARTICLE), rule="01.23", illustrative=True, width=360,
                                  alt="An illustrative position piece. The kicker opens with a Charcoal label, Our position, then the topic, committee votes. Headline: State senate committees should post every vote within two days. We support S. 214, which would require it. What the record shows: 14 of 20 committees posted no roll calls last session. The strongest case against: chairs in both parties say posting every procedural vote would discourage early compromise and need new clerk staff. What we don't know: whether faster posting changes how members vote. After the hinge divider, who decided: our editorial board, February 26, 2027; no funder has a stake in S. 214 or saw the piece before it ran; a link to the bios of the board members who decided. One red button: Ask your senator to vote yes. A footer pointing to our explainer on S. 214 and to the position log."),
                    "caption": "The label comes first, the case against comes before the ask, and the disclosure of who decided, when and with what funder interest sits directly above the button."},
        "failure": {"specimen": A("s-01-23-failure", f'<div class="ed">{position_piece(True)}</div>', css=(BASE, ARTICLE), rule="01.23", illustrative=True, width=360,
                                  alt="The same piece with the Our position label moved to the footer, a pillar name alone in the kicker, and no case against, no open questions and no disclosure above the ask."),
                    "caption": "With the label at the bottom and no case against, a reader learns the piece was an argument only after the ask, which reads as a trick."},
        "specs": [{"label": n, "value": v} for n, v in kit],
        "related": ["13", "18"],
        "builders": "Use the position label component, never a plain kicker, and check the eight parts of the kit in this rule’s specifications before the piece goes to the editor.",
    })

    PN = (f".ed .pnl{{list-style:none;margin:0;padding:0;display:grid;gap:10px}}"
          f".ed .pnl li{{border-top:1px solid var(--oa-color-border-hairline);padding-top:8px;{fx('body', weight='700')}}}"
          f".ed .pnl .pd{{display:block;{fx('caption')};color:var(--oa-color-text-secondary)}}")
    pn_ok = [("Oath & Action, the weekly briefing", "The newsletter", False),
             ("Who Do They Answer To? The Oath & Action Systems Atlas", "The atlas, the one product named as a question", False),
             (HR7008_TRACKER, "A tracker, named for the bill it follows", False),
             ("Reform 101 / Cloture", "An explainer: series, slash, topic", False),
             ("Oath & Action Report 3: How state committees record their votes, March 2027", "A report, numbered and dated", True)]
    pn_bad = [("Rent & Reform Tracker", "An ampersand in a product name", True), ("The Senator Scorecard", "A product that grades officials", True),
              ("Dispatch from the Front", "Our fifth edition’s series name, a war metaphor", False)]
    pnl = lambda items: '<div class="ed"><ul class="pnl">' + "".join(f'<li>{e(a)}{" " + ill() if il else ""}<span class="pd">{e(b)}</span></li>' for a, b, il in items) + "</ul></div>"
    rules.append({
        "id": "01.24", "title": "Name each product for what it does, and keep the ampersand for Oath & Action.",
        "rule": ["Give each product a plain name that says what it does, signed by Oath & Action. The atlas is the only product named as a "
                 "question, and no product name holds an ampersand. When we type a partner’s name in our own copy, its ampersand becomes "
                 "“and”, and the partner’s logo stays as the partner draws it."],
        "why": {"text": ["Every product carries one name, Oath & Action, so a reader who trusts the newsletter can trust the tracker it links to. A plain name tells them what they will get before they open it."],
                "basis": "Design judgment"},
        "correct": {"specimen": A("s-01-24-correct", pnl(pn_ok), css=(BASE, PN), rule="01.24", readable=True,
                                  alt=f"Five product names, each with what it is: Oath & Action, the weekly briefing, the newsletter. Who Do They Answer To? The Oath & Action Systems Atlas, the one product named as a question. {HR7008_TRACKER}, named for the bill it follows. Reform 101 / Cloture, an explainer. Oath & Action Report 3: How state committees record their votes, March 2027, numbered and dated, labeled Illustrative."),
                    "caption": "Each name says what the product does, and the only ampersand belongs to Oath & Action."},
        "failure": {"specimen": A("s-01-24-failure", pnl(pn_bad), css=(BASE, PN), rule="01.24", readable=True,
                                  alt="Three names that break the rule. Rent & Reform Tracker, labeled Illustrative, with an ampersand. The Senator Scorecard, labeled Illustrative, which grades officials. Dispatch from the Front, our fifth edition's series name, a war metaphor."),
                    "caption": "A second ampersand competes with ours, a scorecard grades the officials we ask readers to contact, and “the Front” turns a series into a war."},
        "related": ["03", "22"],
        "builders": ("Name a new product as its subject plus its kind, such as “Child Care Rules Tracker”, and check the name against this rule "
                     "and Rule 01.15 before it ships. A piece made with a partner goes to Dustin Cathcart, our founder and editor, or an "
                     "editor he names, before it prints or posts, and the host’s name leads. Chapter 03 sets the partnership lockup."),
    })

    FL = f".ed .fl{{border-top:2px solid var(--oa-color-border-strong);padding-top:14px}}.ed .fl .big{{{fx('quote')};margin:6px 0 12px}}"
    extras_after = [{"after_rule": "01.24", "specimen": A("s-01-founding-line",
        '<div class="ed"><div class="fl"><p class="lab">Our founding line, kept as a record</p><p class="big">“From spectators to stewards.”</p>'
        '<p>The line Oath &amp; Action started with. Our brand guide’s fourth edition lists it as the historical tagline, “Retired from current applications.” '
        'It has no role as a brand line today, because it competes with the tagline for the same place and casts a newcomer as a spectator.</p></div></div>',
        css=(BASE, FL), rule=None, label="Our founding line", readable=True,
        alt="A record card. Our founding line, kept as a record: From spectators to stewards. Our fourth edition lists it as the historical tagline, retired from current applications. It has no role as a brand line today."),
        "label": "Our founding line", "caption": "Chapter 02’s table of brand lines lists it with no role."}]

    extras = [{"specimen": "s-01-words", "label": "Words this guide uses",
               "caption": "We define each word once here and keep it the same through the guide. The link beside it opens the rule or chapter that sets it."},
              {"specimen": "s-01-hinge-lines", "label": "The hinge in the locked lines",
               "caption": "Each locked line splits at the hinge, a commitment first and the action after it. The pillars split the same way, between Track and Connect, where a reader stops learning about a decision and starts taking part in it."},
              {"specimen": "s-01-pillars", "label": "The four pillars, always in this order",
               "caption": ("Each pillar’s icon sits beside its word, and a page that serves one pillar underlines that word; from 48 px its "
                           "icon also shows its red part as a second sign. The icons belong to the Civic Line, our set of symbols, and "
                           "chapter 09 sets their sizes. "
                           "Every product carries the Oath & Action name. The atlas, the trackers and the data never take a position; "
                           "positions appear only in labeled Act pieces.")},
              {"specimen": "s-01-pieces", "label": "One piece from each pillar, at true size",
               "caption": "Each piece is 340 px wide, the text column of a phone, and opens with its kicker, turns at the hinge divider to “What you can do” and ends on one step, the view’s one working red. Explain and Track quote real records. Connect and Act are invented, and each carries the Illustrative label at its head."}] + extras_uneven + extras_after

    groups = [
        {"before_rule": "01.1", "number": 1, "title": "Color and party",
         "line": "Give no party, side or person a color of its own, and print every name on its mark."},
        {"before_rule": "01.6", "number": 2, "title": "Pictures",
         "line": "Show real places and people doing public work, with a caption a reader can check."},
        {"before_rule": "01.9", "number": 3, "title": "Choosing examples",
         "line": "Spread examples across subjects, states, regions and levels of government, and log each one so anyone can count them."},
        {"before_rule": "01.13", "number": 4, "title": "Words",
         "line": "Name the office that decides, and describe every rule in words its supporters would accept."},
        {"before_rule": "01.18", "number": 5, "title": "Hinge headlines",
         "line": "Keep both halves equal and join people only through something they share; Rule 02.27 sets how to write a hinge headline and Rule 04.3 how to draw one."},
        {"before_rule": "01.21", "number": 6, "title": "Labels, Act pieces and names",
         "line": "Tell a reader what kind of piece they are reading, and name each product for what it does."},
    ]

    sources = [SRC_STOCK_SURVEY, SRC_STOCK_VOTES, SRC_INITIATIVE, SRC_FEC, SRC_R4A, SRC_MINWAGE, SRC_PAY, SRC_CLOTURE, SRC_ELECTRIC,
               "Our brand guide, fifth edition, chapter 13 In use: “Who wrote the rule you are angry about?”"]

    data = {
        "number": "01", "anchor": "purpose", "title": "Purpose", "part": "Foundations",
        "instruction": "Learn what Oath & Action does, and how its pillars and nonpartisan rules shape every piece.",
        "intro": [f"Oath & Action is a nonpartisan publication and a set of tools for people in every state who live under public rules they "
                  f"rarely get to read. Our mission is {q(LOCKED['mission'])}",
                  NONPARTISAN],
        "groups": groups,
        "rules": rules, "extras": extras, "sources": sources,
        "related_chapters": [{"chapter": "02", "reason": "The lines that state the purpose."}, {"chapter": "04", "reason": "The hinge in full."},
                             {"chapter": "05", "reason": "Rule 05.3, the red rule these rules cite."}, {"chapter": "09", "reason": "The pillar icons and their sizes."},
                             {"chapter": "13", "reason": "Evidence grades and the labels beside each item."}, {"chapter": "21", "reason": "The atlas as the purpose at work."}],
    }
    return data
