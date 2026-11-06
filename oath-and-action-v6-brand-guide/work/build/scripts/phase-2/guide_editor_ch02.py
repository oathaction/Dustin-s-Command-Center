"""Chapter 02 Voice: content and specimens for stage board A. Imported by guide_editor_build.py.

The writing section (W01 to W21, H01 to H12, the checklist) is read from the approved content file,
work/boards/phase-2/voice/20261106_Voice-Rules-Content.json (Board 5, DR-73 to DR-83), and carried whole. Its words
are not edited here: each W rule becomes Rule 02.n with its W number kept in the title, so Rule 02.5 is W05.
"""
import re

from guide_editor_common import (AMP_DISPLAY, BASE, HL, LOCKED, PAIR, PIECE, VOICE_CONTENT, VOICE_LINE_B, WORDMARK24, added,
                                 amp_h, curl, e, hinge, ill, load, marks, plain, q, removed, say_dash)

VOICE_MD = "work/handoffs/phase-2/20261106_Voice-Writing-Rules.md"

WHY = {
    "W01": "Most readers meet us on a phone, between other things. A sentence they can follow by ear the first time is the one they can act on.",
    "W02": "People can hold an office to account only when they can name it. Putting the actor first gives them the name in the first breath.",
    "W03": "Speech rises and falls. When every sentence runs the same length, a listener starts to hear the beat over the words.",
    "W04": "Words such as because and once carry the logic a listener needs. Without them, the reader has to guess how one short sentence leads to the next.",
    "W05": "A reader decides in the first line whether a piece is worth their time, and a line that only announces what is coming gives them no reason to stay.",
    "W06": "A reveal makes the reader wait for a point we could have given at once, and holding it back sounds like a performance.",
    "W07": "A closing line that restates the point tells the reader we doubt they followed, so we end on the last new fact and trust them with it.",
    "W08": "The last words of a piece are the ones a reader carries away. A dated step gives them something to do with what they read.",
    "W09": "A sentence that starts with what a thing is not makes the reader picture the wrong thing first and then undo it.",
    "W10": "Two matched halves sound like a slogan and leave the reader to supply the link between them, which one plain sentence can state.",
    "W11": "A run of negatives sounds like a list of grievances. One verb and a reason tell the reader what to do and why.",
    "W12": "Three items in a row sound finished, so writers reach for three when the facts hold two or four. A list sized to the facts sounds like advice.",
    "W13": "When sentences in a row open the same way, a listener hears the pattern and stops hearing the content.",
    "W14": "A listener holds each noun in a stack until the last one says what the phrase is about. Pulling the stack apart puts the main noun first.",
    "W15": "A noun made from a verb hides who acts, and turning it back into the verb brings the actor back into the sentence.",
    "W16": "A stack of softeners blurs how sure we are, while one grade verb, taken from the atlas’s scale, tells the reader how far the evidence goes.",
    "W17": "A word added for force signals that the sentence is missing a fact, and the fact, once found, carries the force by itself.",
    "W18": "Memo verbs put distance between the writer and the reader, while the words a resident would use at a council meeting sound like a neighbor talking.",
    "W19": "Excitement on the page asks the reader to feel something we have given them no reason for, and a clear step with its date gives them the reason.",
    "W20": "A word that claims more than the evidence invites a reader to check it and find it wrong, and one wrong word costs the trust the rest of the page earned.",
    "W21": "An em dash lets a writer skip the word that says how two thoughts connect, and a listener needs that word to follow.",
}
FAILCAP = {
    "W01": "“The point of responsibility” names no office a listener could call, and nobody says it out loud.",
    "W02": "The passive verb pushes the actor to the end of the sentence, and in many drafts it drops the actor altogether.",
    "W03": "Three sentences of {lengths} words fall on one beat, and the abbreviation FTC assumes the reader already knows the agency.",
    "W04": "Two commands sit side by side with no word to join them, so a listener cannot tell that one depends on the other, and “the lever” goes undefined.",
    "W05": "“Here is how to weigh in” promises the steps and gives none, so a reader who stops at the headline leaves without the deadline.",
    "W06": "“This is where” and the colon hold the answer back for effect, so a listener waits through the setup to hear who owns what.",
    "W07": "The first and last sentences say one idea twice, and the last lands as a moral the facts did not need.",
    "W08": "“Put the promise to work” sounds like an advertisement and leaves the reader with no step and no date.",
    "W09": "The “not” half is there for rhythm, and a photographer still has to work out what to shoot.",
    "W10": "The second sentence echoes “counts” for rhythm and never says where spoken testimony happens.",
    "W11": "Four “no” phrases in a row give no verb and no reason, so the reader learns what is banned and never why.",
    "W12": "“The rule, the gap, the ask” chants three nouns and gives a first-time speaker no instruction to follow.",
    "W13": "Four sentences open with “We” on one frame, and the run sounds like a pledge read aloud.",
    "W14": "“Report cover kicker” stacks three nouns, so a listener holds all three before learning that the phrase means a kicker.",
    "W15": "“Allocation” and “establishes no claim” turn two actions into nouns, so the sentence names no one who sets money aside.",
    "W16": "“Could perhaps help” and “somewhat in some places” stack four softeners, so a reader cannot tell how strong the evidence is.",
    "W17": "“Really” asks the reader to feel urgency and gives no reason for it.",
    "W18": "“Leverage”, “funds” and “expand broadband access” are memo words, and none of them says who gains.",
    "W19": "The slogan and its exclamation point cheer the reader on and name no one to tell and no time to tell them.",
    "W20": "“Eligible voters” names a wider group than the survey counted, and the ranking ignores the survey’s margin of error.",
    "W21": "The em dash breaks the sentence without saying how the vote relates to the deadline, and a screen reader may skip it.",
}
BUILD = {
    "W01": "Read the draft aloud, or have a screen reader read it to you, and rewrite each line where you stumble or stop to decode.",
    "W02": "Search for “is”, “are”, “was” and “were” before a past participle, and for “by”, and ask who does the action.",
    "W03": "Count the words in each sentence of a paragraph. If every count falls within a few words of the others, join two sentences or split one.",
    "W04": "Look for runs of short sentences with no joining word, and join the ones that depend on each other with because, so, when or once.",
    "W05": "Delete the first sentence of a draft and read it again. If nothing is lost, leave it out.",
    "W06": "Search headlines and openers for colons and for “here’s”, “this is where” and “the answer”, and lead with what follows them.",
    "W07": "Cover the last sentence of each paragraph. If the paragraph still holds every fact, delete the sentence.",
    "W08": "Check that the last line of every piece names a step and its date, or signs off with the locked tagline.",
    "W09": "Search for “, not”, “not only” and “rather than”, and keep the half that says what to do.",
    "W10": "Look for pairs of short sentences that repeat a word or a frame, and write the relation between them in one sentence.",
    "W11": "Search for “no” or “never” opening two or more phrases in a row, and fold them into one list under one verb with its reason.",
    "W12": "Count the items in every list of three. If the facts hold a different number, or the items share one shape, rewrite the list.",
    "W13": "Read the first word of each sentence in a paragraph. When two or more in a row match, combine them or recast one.",
    "W14": "Search for three or more nouns in a row, and rewrite with a preposition or a verb between them.",
    "W15": "Search for words ending in -tion, -ment, -ance and -ity, and ask which verb each one hides and who does it.",
    "W16": "Look up the claim’s grade in the atlas, use the verb the H08 table gives it, and delete every other softener.",
    "W17": "Search for genuinely, really, truly, actually, simply and just, and replace each with a fact or delete it.",
    "W18": "Search for leverage, underscore and reflect, and swap each for use, show or the plain verb you would say.",
    "W19": "Search for exclamation points and delete each one, then check that the sentence names a step.",
    "W20": "Check each adjective and group name against the source’s own definition, and test every ranking against the margin of error.",
    "W21": "Search for the em dash, U+2014, and replace each with a period, or with a comma and a joining word.",
}
REL = {"W01": ["01"], "W02": ["01", "13"], "W05": ["20", "22"], "W06": ["20", "23"], "W07": ["24"], "W08": ["01", "12"],
       "W09": ["16"], "W10": ["04"], "W11": ["03"], "W12": ["23"], "W13": ["01"], "W14": ["06"], "W15": ["13"],
       "W16": ["13", "14"], "W17": ["22"], "W18": ["20"], "W19": ["23"], "W20": ["13", "14"], "W21": ["06"]}

LEGEND = ('<p class="legend"><span><del>Dotted underline</del>: what the rule removes</span><span><ins>Solid underline</ins>: the repair</span>'
          '<span><span class="ill">Illustrative</span> written to show the fault, not quoted</span></p>')
LEG_CSS = ".ed .legend{display:flex;flex-wrap:wrap;gap:6px 24px;font-size:.9375rem;color:var(--oa-color-text-secondary);margin:14px 0 0}"

SRC_SENATE = ("Source: U.S. Senate, Vote 253, cloture on the motion to proceed to H.R. 7008, September 30, 2026, United States, as "
              "recorded in Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. The studio could not "
              "open the Senate’s own page for the vote.")
SRC_INITIATIVE = ("Source: Ballotpedia, States with initiative or referendum, 50 states and DC. Retrieved November 6, 2026. "
                  "Mississippi’s process exists on paper but cannot be used after a 2021 state supreme court ruling.")


def words(s):
    return len(re.findall(r"[\w’'.,-]+", s))


def sentence_lengths(s):
    return [len(x.split()) for x in re.split(r"(?<=[.!?])\s+", s.strip()) if x.strip()]


def pair(r):
    il = ill() if r.get("illustrative") else ""
    note = ""
    if r.get("render_note"):
        note = f'<p class="note">{e(re.sub(r"\s*\(DR-\d+\)", "", r["render_note"]))}</p>'
    src = f'<p class="note">{e(r["source_line"])}</p>' if r.get("source_line") else ""
    return (f'<div class="ed pair"><figure class="ex before"><figcaption class="exh"><span class="chip">Before</span>{il}'
            f'<span class="s">{e(curl(r["before_source"]))}</span></figcaption><p class="q">{marks(r["before"])}</p>{note}</figure>'
            f'{hinge()}<figure class="ex after"><figcaption class="exh"><span class="chip solid">After</span>{il}</figcaption>'
            f'<p class="q">{marks(r["after"])}</p>{src}</figure></div>')


def fault(r):
    """The failure plate: the pattern the rule removes, named in the approved terms line, then the before with only
    its fault in full ink."""
    b = html_fault(r["before"])
    terms = r.get("terms") or ""
    extra = ""
    if r["id"] == "W03":
        L = sentence_lengths(plain(r["before"]))
        bars = "".join(f'<li><span class="lb" style="width:{n * 14}px"></span><span>{n} words</span></li>' for n in L)
        extra = f'<p class="lab">Sentence lengths in the before</p><ul class="lens">{bars}</ul>'
        terms = "A run of sentences the same size: the metronome this rule warns about."
    return (f'<div class="ed flt"><p class="lab">The pattern</p><p class="tm">{e(curl(terms))}</p>{extra}'
            f'<p class="lab">Where it shows in the before{" " + ill() if r.get("illustrative") else ""}</p><p class="q">{b}</p></div>')


def html_fault(s):
    t = marks(re.sub(r"\[\+(.+?)\+\]", r"\1", s))
    parts = re.split(r"(<del>.*?</del>|<span class=\"emrule\"[^>]*></span>)", t)
    return "".join(p if p.startswith("<del>") or p.startswith("<span") else (f'<span class="dim">{p}</span>' if p else "") for p in parts)


FLT_CSS = """
.ed.flt{max-width:760px}
.ed .tm{font-size:1.0625rem;margin:0 0 16px;max-width:64ch}
.ed .flt .q{font:400 clamp(1.1875rem,1.1rem + .4vw,1.375rem)/1.5 var(--oa-font-family-reading);overflow-wrap:anywhere}
.ed .dim{color:var(--oa-color-text-secondary)}
.ed .lens{list-style:none;margin:0 0 16px;padding:0;display:grid;gap:6px}
.ed .lens li{display:flex;align-items:center;gap:10px;font:var(--oa-type-data-label);font-size:.9375rem}
.ed .lb{display:inline-block;height:12px;background:var(--oa-color-data-emphasis)}
"""

GO_CSS = """
.ed.go{max-width:760px;border-top:2px solid var(--oa-color-border-strong);padding-top:16px}
.ed .gwrap{display:grid;grid-template-columns:auto minmax(0,1fr);gap:4px 20px;align-items:start}
.ed .gnum{font:800 clamp(3rem,2.4rem + 2.6vw,4.5rem)/.85 var(--oa-font-family-display);letter-spacing:-.04em;grid-row:1/3}
.ed .gname{font:800 clamp(1.5rem,1.3rem + .8vw,2rem)/1.1 var(--oa-font-family-display);letter-spacing:-.02em}
.ed .gint{font-size:1.0625rem;margin-top:6px;max-width:58ch}
.ed .ghouse{margin-top:14px;border-top:1px solid var(--oa-color-border-hairline);padding-top:10px}
.ed .ghouse ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 24px}
.ed .ghouse a{display:inline-flex;align-items:center;min-height:44px;font-weight:600;color:inherit}
"""


def build(book):
    C = load(VOICE_CONTENT)
    A = lambda sid, body, **kw: book.add(sid, body, chapter="02", **kw)
    groups = C["groups"]
    W = [r for g in groups for r in g["rules"]]
    gi = {r["id"]: i for i, g in enumerate(groups) for r in g["rules"]}
    rid = {r["id"]: f"02.{k + 1}" for k, r in enumerate(W)}
    house = {h["id"]: h for h in C["house_rules"]}
    n_ill = sum(1 for r in W if r.get("illustrative"))
    num_words = {6: "six", 5: "five", 4: "four", 3: "three", 7: "seven"}

    # --- the brand lines, for reference, before the rules ---------------------------------------------------------
    lines = [
        ("Tagline", q(LOCKED["tagline"]), "Principal tagline: the result the loop works toward", "The cover, the home page, the back cover, the newsletter’s sign-off and a video’s last frame"),
        ("Mission", q(LOCKED["mission"]), "Mission: why Oath & Action exists", "The About page, grant and partner material, and a report’s inside cover"),
        ("Reader promise", q(LOCKED["promise"]), "Reader promise: what every piece owes a reader", "Under the home page masthead and in the newsletter welcome"),
        ("Editorial commitment", q(LOCKED["commitment"]), "Editorial commitment: the standard our staff answer to", "The colophon, the method page and the corrections page"),
        ("Pillars", "Explain → Track → Connect → Act", "The pillars: the order of every sequence", "Navigation, the four-dot row and the Signal Grid’s corners"),
        ("Voice line", q(VOICE_LINE_B), "What we do, in our own words, split at the hinge; approved at Gate 1", "The About page, after the mission"),
        ("Supporting line", q("Democracy has a structure."), "The lockmark’s explanatory line, followed by a sentence that names the lever", "Chapter 08 and the About page"),
        ("Founding line", q("From spectators to stewards."), "A record of where we started, with no role as a brand line", "Chapter 01, as a record"),
    ]
    trs = "".join(f'<tr><th scope="row">{e(a)}</th><td><span class="{"lk" if i < 4 or i >= 5 else "pl"}">{e(b)}</span></td><td data-k="Role">{e(c)}</td><td data-k="Where">{e(d)}</td></tr>'
                  for i, (a, b, c, d) in enumerate(lines))
    retired = ["Know the rules. Find the lever.", "Institutions endure when people act.", "The fine print affects the big picture.", "Bring your questions. They belong here."]
    rec = ('<div class="ret"><p class="lab">Retired, kept as a record</p><p>Our fifth edition’s supporting lines '
           + ", ".join(q(x) for x in retired[:-1]) + " and " + q(retired[-1])
           + ' retire with no role. Each fails a writing rule below, and the lines above already do their jobs.</p></div>')
    LCSS = ".ed .lines td:nth-child(2){min-width:14rem;font-size:1.0625rem}@media (max-width:47.99em){.ed .lines td:nth-child(2){min-width:0}}.ed .lines .pl{font-weight:600}.ed .ret{margin-top:16px;border-top:1px solid var(--oa-color-border-hairline);padding-top:10px;font-size:.9375rem;max-width:72ch}"
    A("s-02-lines", f'<div class="ed"><table class="lines stack"><thead><tr><th scope="col">Line</th><th scope="col">Exact wording</th><th scope="col">Role</th>'
      f'<th scope="col">Where it appears</th></tr></thead><tbody>{trs}</tbody></table>{rec}</div>', css=(BASE, LCSS),
      rule=None, interactive=True, label="The brand lines",
      alt="A table of the brand lines with each line's exact wording, role and place. The four locked lines, the pillars, the voice line approved at Gate 1, the supporting line Democracy has a structure, and the founding line From spectators to stewards, with no brand-line role. Below it, a record of four retired lines from the fifth edition.",
      notes="Locked lines from Master Brief section 3. Voice line B (G1-01). Supporting and founding line roles (G1-01, S5). The four retired lines are DR-77's, shown only as a labeled record.")

    # --- the writing section's opening and rule index ---------------------------------------------------------------
    idx = []
    for i, g in enumerate(groups):
        items = "".join(f'<li><a href="#rule-{rid[r["id"]].replace(".", "-")}"><span class="rn">{e(r["id"])}</span><span>{e(r["name"])}</span></a></li>' for r in g["rules"])
        if g.get("house_rules"):
            items += "".join(f'<li><a href="#s-02-22-correct--{h.lower()}"><span class="rn">{e(h)}</span><span>{e(house[h]["name"])}</span></a></li>' for h in g["house_rules"])
        idx.append(f'<div><p class="ig"><span>{i + 1:02d}</span>{e(g["name"])}</p><ol>{items}</ol></div>')
    hr_rest = [h for h in C["house_rules"] if not any(h["id"] in (g.get("house_rules") or []) for g in groups)]
    idx.append('<div><p class="ig"><span>H</span>House rules for every page</p><ol>' + "".join(
        f'<li><a href="#s-02-22-correct--{h["id"].lower()}"><span class="rn">{e(h["id"])}</span><span>{e(h["name"])}</span></a></li>' for h in hr_rest)
        + '<li><a href="#fig-s-02-checklist"><span class="rn">10</span><span>Before you publish: ten questions</span></a></li></ol></div>')
    ICSS = """
.ed.ix{max-width:1040px}
.ed .wt{font:800 clamp(1.75rem,1.4rem + 1.4vw,2.5rem)/1.05 var(--oa-font-family-display);letter-spacing:-.025em;margin:0 0 10px}
.ed .deck{font-size:1.25rem;line-height:1.5;max-width:58ch;margin:0 0 14px}
.ed .nar{font-size:1.0625rem;max-width:64ch;margin:0 0 10px}
.ed .index{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,15rem),1fr));gap:20px 28px;margin-top:20px}
.ed .ig{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;margin:0 0 6px}
.ed .ig span{display:block;font:800 1.75rem/1 var(--oa-font-family-display);letter-spacing:-.02em;margin-bottom:6px;text-transform:none}
.ed .index ol{list-style:none;margin:0;padding:0}.ed .index li{border-top:1px solid var(--oa-color-border-hairline)}
.ed .index a{display:flex;gap:10px;align-items:baseline;min-height:44px;padding:10px 0;color:inherit;text-decoration:none;font-size:.9375rem;line-height:1.35}
.ed .index a:hover span+span,.ed .index a:focus-visible span+span{text-decoration:underline}
.ed .rn{font:700 .8125rem/1 var(--oa-font-family-reading);color:var(--oa-color-text-secondary);font-variant-numeric:tabular-nums;min-width:2.6em}
.ed .fine{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin-top:16px;max-width:76ch}
"""
    A("s-02-index", f'''<div class="ed ix"><p class="wt">{e(C["title"])}</p><p class="deck">{e(C["deck"])}</p>
<p class="nar">{e(C["narrative"][2])}</p><p class="nar">{e(C["rule_index_intro"])} {e(C["scope"])}</p>
<div class="index">{"".join(idx)}</div>{LEGEND}
<p class="fine">{e(C["sources_note"])} Each before is quoted exactly, with its source named, except the {num_words[n_ill]} marked Illustrative, which show the fault in words we wrote for the purpose.</p></div>''',
      css=(BASE, PAIR, ICSS, LEG_CSS), rule=None, interactive=True, label="How Oath & Action writes",
      alt=f"The writing section's opening: {C['deck']} {C['narrative'][2]} A rule index in five groups with links to each of the 21 writing rules, and the 12 house rules. A legend: a dotted underline marks what a rule removes and a solid underline the repair.",
      notes="Title, deck, third narrative paragraph, index intro, scope and sources note verbatim from the approved content file. The count sentence follows Board 5's wording with the number spelled out (H06).")

    def opener(i):
        g = groups[i]
        hh = ""
        if g.get("house_rules"):
            hh = '<div class="ghouse"><p class="lab">House rules in this group</p><ul>' + "".join(
                f'<li><a href="#s-02-22-correct--{h.lower()}">{e(h)} · {e(house[h]["name"])}</a></li>' for h in g["house_rules"]) + "</ul></div>"
        return A(f"s-02-group-{i + 1}", f'<div class="ed go"><div class="gwrap"><p class="gnum" aria-hidden="true">{i + 1:02d}</p><p class="gname">{e(g["name"])}</p>'
                 f'<p class="gint">{e(g["intro"])}</p></div>{hh}{LEGEND}</div>', css=(BASE, PAIR, GO_CSS, LEG_CSS), rule=None,
                 interactive=bool(hh), label=f"Writing rules, group {i + 1} of 5",
                 alt=f"Group {i + 1} of the writing rules: {g['name']}. {g['intro']}" + (" House rules in this group: " + ", ".join(f"{h} {house[h]['name']}" for h in g["house_rules"]) + "." if hh else ""))

    extras = [{"specimen": "s-02-lines", "label": "The brand lines",
               "caption": "The locked lines are quoted word for word everywhere, and H01 keeps their wording even where a writing rule would shape the sentence another way."},
              {"specimen": "s-02-index", "label": "How Oath & Action writes",
               "caption": "The writing section, approved on Board 5: 21 rules in five groups, each with a before and an after, and 12 house rules. Rule 02.1 is W01, and every W rule keeps its number as part of its title."},
              {"specimen": opener(0), "label": "Writing rules, group 1 of 5", "caption": "Each rule below shows a before and its repair, joined by the hinge divider."}]
    for i, after in ((1, "W04"), (2, "W08"), (3, "W13"), (4, "W20")):
        extras.append({"after_rule": rid[after], "specimen": opener(i), "label": f"Writing rules, group {i + 1} of 5",
                       "caption": "H05 to H07 sit with the house rules in Rule 02.22." if i == 4 else ""})
    for x in extras:
        if not x.get("caption"):
            x.pop("caption", None)

    # --- Rules 02.1 to 02.21: the writing rules -----------------------------------------------------------------
    rules = []
    for r in W:
        n = rid[r["id"]]
        k = n.split(".")[1]
        rem = removed(r["before"])
        add = added(r["after"])
        src_before = "Written for the rule, and labeled Illustrative" if r.get("illustrative") and r["before_source"].startswith("We wrote") else curl(r["before_source"])
        pair_alt = (f"Before, {say_dash(curl(r['before_source']))}{', illustrative' if r.get('illustrative') else ''}: {say_dash(plain(r['before']))} "
                    f"The rule removes: {'; '.join(say_dash(x) for x in rem)}. After: {plain(r['after'])} The repair: {'; '.join(add)}."
                    + (f" {r['source_line']}" if r.get("source_line") else ""))
        cap_fail = FAILCAP[r["id"]]
        if "{lengths}" in cap_fail:
            L = sentence_lengths(plain(r["before"]))
            spelled = {8: "eight", 9: "nine", 7: "seven", 6: "six"}
            parts = [spelled.get(x, str(x)) for x in L]
            cap_fail = cap_fail.replace("{lengths}", ", ".join(parts[:-1]) + " and " + parts[-1])
        rule = {
            "id": n, "title": f"{r['id']} {r['name']}.",
            "rule": [r["rule"]] + ([f"Terms. {r['terms']}"] if False else []),
            "why": {"text": [WHY[r["id"]]], "basis": "Editorial judgment"},
            "correct": {"specimen": A(f"s-02-{k}-pair", pair(r), css=(BASE, PAIR), rule=n, illustrative=r.get("illustrative", False), alt=pair_alt,
                                      notes=f"{r['id']} as approved on Board 5. Edit marks from the content file: dotted underline on removed words, solid on the repair."),
                        "caption": "What changed: " + r["why"]},
            "failure": {"specimen": A(f"s-02-{k}-fault", fault(r), css=(BASE, PAIR, FLT_CSS), rule=n, illustrative=r.get("illustrative", False),
                                      alt=f"The pattern: {r.get('terms') or 'a run of sentences the same size'}. In the before, the words the rule removes: {'; '.join(say_dash(x) for x in rem)}.",
                                      notes="The pattern named in the approved terms line, and the before with only its fault in full ink."),
                        "caption": cap_fail},
            "specs": [{"label": "Group", "value": f"{gi[r['id']] + 1}. {groups[gi[r['id']]]['name']}"},
                      {"label": "Before", "value": src_before}],
            "builders": BUILD[r["id"]],
        }
        if REL.get(r["id"]):
            rule["related"] = REL[r["id"]]
        rules.append(rule)

    # --- Rule 02.22: the house rules ----------------------------------------------------------------------------
    def hrow(h):
        grades = ""
        if h.get("grades"):
            grades = '<dl class="grades">' + "".join(f'<dt>{e(x["grade"])}</dt><dd>{e(x["means"])} <b>Title verb:</b> {e(x["title_verb"])}</dd>' for x in h["grades"]) + "</dl>"
        if h.get("example_before"):
            ex = (f'<p class="hb"><span class="chip">Before</span> {marks(h["example_before"])}</p><p class="hsrc">{e(h["example_before_source"])}</p>'
                  f'<p class="hb"><span class="chip solid">After</span> {marks(h["example"])}</p>')
        else:
            exm = e(h["example"])
            if h["id"] == "H03":
                exm = exm.replace(" Illustrative", " " + ill())
            ex = f'<p class="hb">{exm}</p>'
        if h.get("example_source"):
            ex += f'<p class="hsrc">{e(h["example_source"])}</p>'
        return (f'<tr id="{h["id"].lower()}"><th scope="row"><span class="hid">{e(h["id"])}</span> {e(h["name"])}</th>'
                f'<td>{e(h["rule"])}{grades}</td><td class="exq">{ex}</td></tr>')
    HCSS = """
.ed .house th[scope=row]{font-weight:700;min-width:11rem}.ed .hid{display:block;font:700 .8125rem/1.4 var(--oa-font-family-reading);color:var(--oa-color-text-secondary)}
.ed .house td.exq{font-size:1rem;min-width:16rem}.ed .hb{margin:0 0 6px}.ed .hb .chip{margin-right:6px}.ed .hsrc{font:var(--oa-type-caption);color:var(--oa-color-text-secondary);margin:0 0 8px}
.ed .grades{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:4px 12px;margin:10px 0 0;font-size:.875rem}.ed .grades dt{font-weight:700}.ed .grades dd{margin:0}
.ed .house tr:target{outline:3px solid var(--oa-color-focus-ring);outline-offset:-3px}
@media (max-width:47.99em){.ed .house,.ed .house tbody,.ed .house tr,.ed .house th,.ed .house td{display:block;width:100%}.ed .house thead{display:none}.ed .house tr{border-bottom:1px solid var(--oa-color-border-strong);padding:10px 0}.ed .house th,.ed .house td{border:0;padding:4px 0}}
"""
    house_tbl = (f'<div class="ed"><table class="house"><thead><tr><th scope="col">Rule</th><th scope="col">What it asks</th><th scope="col">Example</th></tr></thead>'
                 f'<tbody>{"".join(hrow(h) for h in C["house_rules"])}</tbody></table></div>')
    FCSS = """
.ed.prf{max-width:760px}
.ed .prf .txt{font:400 clamp(1.1875rem,1.1rem + .4vw,1.375rem)/1.7 var(--oa-font-family-reading)}
.ed .bad{text-decoration:underline dotted 2px var(--oa-color-graphic-subtle);text-underline-offset:5px}
.ed sup.f{font:700 .8125rem/1 var(--oa-font-family-reading);border:1px solid var(--oa-color-border-strong);padding:2px 4px;margin-left:3px;vertical-align:.5em}
.ed .fk{list-style:none;margin:14px 0 0;padding:0;display:grid;gap:4px;font-size:.9375rem}.ed .fk b{display:inline-block;min-width:2.8em}
"""
    proof = ('<div class="ed prf"><p class="lab">A draft paragraph ' + ill() + '</p><p class="txt">'
             '<span class="bad">R10</span><sup class="f">H11</sup> is why turnout fell <span class="bad">-2</span><sup class="f">H07</sup> points on '
             '<span class="bad">11/3/2026</span><sup class="f">H05</sup>.<sup class="f">H04</sup> '
             '<span class="bad" style="color:var(--oa-color-palette-pillar-red)" data-red="failure">Republicans</span><sup class="f">H10</sup> gained in '
             '<span class="bad">3</span><sup class="f">H06</sup> states, the <span class="bad">death tax</span> repeal passed and the '
             '<span class="bad">voter suppression bill</span><sup class="f">H12</sup> stalled. A Tucson voter, Jan Ruiz, called it '
             '<span class="bad">“a wake-up call.”</span><sup class="f">H03</sup></p>'
             '<ul class="fk"><li><b>H11</b> A bare ID: say it is Loop R10, the safe-seat loop.</li><li><b>H07</b> A hyphen for a minus sign: write −2.</li>'
             '<li><b>H05</b> A numeric date: write November 3, 2026.</li><li><b>H04</b> A statistic with no source line.</li>'
             '<li><b>H10</b> A party set in red: name it in words, in the text ink.</li><li><b>H06</b> A figure under ten in prose: write three.</li>'
             '<li><b>H12</b> Each side’s term for a contested policy: use the estate tax and the bill’s official name.</li>'
             '<li><b>H03</b> An invented person and quote with no Illustrative label beside them.</li></ul></div>')
    rules.append({
        "id": "02.22", "title": "Follow the 12 house rules on every page.",
        "rule": ["Every page follows the 12 house rules, from quoting the locked lines exactly to calling a contested policy by its neutral name. "
                 "They apply to headings, labels, captions and chart keys as well as to sentences."],
        "why": {"text": ["These are details a reader relies on without noticing, such as a date written in words and a source line they can follow "
                         "back to its table. Each one keeps a page easy to check and fair to every reader."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": A("s-02-22-correct", house_tbl, css=(BASE, PAIR, HCSS), rule="02.22", interactive=True,
                                  alt="The 12 house rules in a table, each with what it asks and an example: H01 to H12, with H08's before and after and its table of evidence grades and title verbs.",
                                  notes="Every rule, example and source line verbatim from the approved content file."),
                    "caption": "The house rules as approved with the writing rules. H05 to H07 also belong to the marks and numbers group."},
        "failure": {"specimen": A("s-02-22-failure", proof, css=(BASE, PAIR, FCSS), rule="02.22", illustrative=True, exempt=["red", "contrast"],
                                  alt="An illustrative draft paragraph that breaks eight house rules, each fault underlined and tagged with the rule it breaks: a bare ID R10, a hyphen used as a minus sign, a numeric date, a statistic with no source, a party name set in red, the figure 3 in prose, one side's terms for two contested policies, and an invented person and quote with no Illustrative label."),
                    "caption": "One short paragraph breaks eight house rules. Each tag names the rule, and the list says how to fix it."},
        "specs": [{"label": "Minus sign", "value": "U+2212, in prose, tables and charts"},
                  {"label": "Dates", "value": "Month in words in prose; numeric dates only in file names and data"},
                  {"label": "Source line order", "value": "Publisher, title or table, observation period, geography, date retrieved, qualification"}],
        "files": ["work/boards/phase-2/voice/20261106_Voice-Rules-Content.json", VOICE_MD],
        "related": ["13", "14", "15"],
        "builders": "Before review, search for numeric dates, a hyphen before a figure, IDs with no name beside them, party names in a color and statistics without a source line.",
    })
    check = "".join(f"<li>{e(x)}</li>" for x in C["checklist"])
    CKCSS = ".ed ol.check{margin:0;padding:0;list-style:none;counter-reset:c;columns:2 22rem;column-gap:40px;max-width:1040px}.ed ol.check li{counter-increment:c;display:grid;grid-template-columns:2.25rem minmax(0,1fr);gap:10px;padding:12px 0;border-bottom:1px solid var(--oa-color-border-strong);font-size:1.0625rem;break-inside:avoid}.ed ol.check li::before{content:counter(c);font:800 1.375rem/1.15 var(--oa-font-family-display)}.ed .ckh{font:800 1.5rem/1.1 var(--oa-font-family-display);margin:0 0 6px}"
    extras.append({"after_rule": "02.22", "specimen": A("s-02-checklist", f'<div class="ed"><p class="ckh">Read it aloud, then ask</p><ol class="check">{check}</ol></div>',
                                                         css=(BASE, CKCSS), rule=None, interactive=True, label="Before you publish",
                                                         alt="Ten questions to ask before you publish, each worded so that yes means pass: " + " ".join(f"{i + 1}. {x}" for i, x in enumerate(C["checklist"]))),
                   "label": "Before you publish", "caption": "The ten questions close the writing section. A yes to each one means the draft passes."})

    # --- Rules 02.23 to 02.27: the brand's lines and words, carried from the fifth edition -------------------------
    PLC = """
.ed .places{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,300px),1fr));gap:24px 32px;max-width:1000px}
.ed .places>div{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}
.ed .places .lab{margin-bottom:10px}
.ed .mh{display:flex;flex-direction:column;gap:10px;background:var(--oa-color-surface-white);padding:16px;border:1px solid var(--oa-color-border-hairline)}
.ed .wm{display:block;height:24px;width:auto;color:var(--oa-color-text-primary)}
.ed .pv{font-size:1.0625rem;line-height:1.45}
.ed .ms{font:600 1.25rem/1.35 var(--oa-font-family-reading)}
.ed .so{font:800 1.5rem/1.15 var(--oa-font-family-display);letter-spacing:-.015em}
.ed .tagslot{display:flex;flex-direction:column;gap:8px;background:var(--oa-color-surface-white);padding:20px;border:1px solid var(--oa-color-border-hairline);max-width:460px}
.ed .tagslot .tg{font:800 1.75rem/1.1 var(--oa-font-family-display);letter-spacing:-.02em}
"""
    wm = f'<img data-inline src="{WORDMARK24}" alt="Oath and Action" class="wm" height="24" data-red="signature">'
    places = (f'<div class="ed"><div class="places">'
              f'<div><p class="lab">Home page, under the masthead</p><div class="mh">{wm}<p class="pv">{e(LOCKED["promise"])}</p></div></div>'
              f'<div><p class="lab">About page</p><div class="mh"><p class="ms">{e(LOCKED["mission"])}</p><p class="pv">{e(VOICE_LINE_B)}</p></div></div>'
              f'<div><p class="lab">Colophon</p><div class="mh"><p class="pv"><span class="lk">{e(q(LOCKED["commitment"]))}</span> Corrections and our method are linked from every page.</p></div></div>'
              f'<div><p class="lab">Newsletter, the sign-off</p><div class="mh"><p class="pv">That’s the briefing for November 6.</p><p class="so">{e(LOCKED["tagline"])}</p></div></div>'
              f'</div></div>')
    bad_slot = (f'<div class="ed"><div class="tagslot">{wm}<p class="tg">From spectators to stewards.</p></div></div>')
    rules.append({
        "id": "02.23", "title": "Set each brand line in its own place, word for word.",
        "rule": ["Each brand line has one job and a set of places where it appears, as the table of brand lines gives them. Quote it exactly there, and "
                 "keep the candidate and founding lines out of the tagline’s slot."],
        "tokens": ["oa.font.family.reading", "oa.font.family.quote"],
        "why": {"text": ["A line that appears in the same place every time becomes something a reader recognizes. Moving a line, or swapping one in, spends that recognition."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": A("s-02-23-correct", places, css=(BASE, PLC), rule="02.23",
                                  alt=f"Four places, each with its line. Home page: the wordmark with the reader promise beneath it. About page: the mission and the voice line. Colophon: the editorial commitment, quoted. Newsletter sign-off: That's the briefing for November 6, then the tagline, {LOCKED['tagline']}"),
                    "caption": "Each line sits where the table puts it, in exact words, and the tagline signs off the newsletter."},
        "failure": {"specimen": A("s-02-23-failure", bad_slot, css=(BASE, PLC), rule="02.23",
                                  alt="The wordmark with From spectators to stewards set beneath it in the tagline's slot."),
                    "caption": "In the tagline’s slot, the founding line competes with “A country that answers to its people.” and casts a newcomer as a spectator."},
        "related": ["01", "03", "08"],
        "builders": "Copy brand lines from the table in this chapter, never retype them, and check them character for character before a piece ships.",
    })
    snd = [("Plain and active.", "The writing rules W01 to W04.", "#rule-02-1"),
           ("Sourced.", "House rule H04, with the source line format; chapter 13 sets the rest.", "#s-02-22-correct--h04"),
           ("Nonpartisan.", "Rules 01.1 to 01.20, with house rules H10 and H12.", "#rule-01-1"),
           ("One next step.", "Rule 02.24, and the two kinds of Act piece in Rules 01.22 and 01.23.", "#rule-02-24")]
    SCSS = ".ed .snd{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr));gap:16px 28px;max-width:1000px}.ed .snd li{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}.ed .snd b{display:block;font:800 1.25rem/1.2 var(--oa-font-family-display);margin-bottom:4px}.ed .snd a{color:inherit;display:inline-block;min-height:24px}"
    extras.append({"after_rule": "02.23", "specimen": A("s-02-sound", '<div class="ed"><ul class="snd">' + "".join(f'<li><b>{e(a)}</b><a href="{h}">{e(b)}</a></li>' for a, b, h in snd) + "</ul></div>",
                                                        css=(BASE, SCSS), rule=None, interactive=True, label="How we sound",
                                                        alt="Our fifth edition's four qualities of voice and where each now lives. Plain and active: writing rules W01 to W04. Sourced: house rule H04 and chapter 13. Nonpartisan: Rules 01.1 to 01.20 with house rules H10 and H12. One next step: Rule 02.24 and Rules 01.22 and 01.23."),
                   "label": "How we sound", "caption": "Our fifth edition named four qualities of the voice. Each one now has rules that teach it."})

    END = ".ed .end{max-width:560px}.ed .end .wycd{font:800 1.5rem/1.15 var(--oa-font-family-display);margin:0 0 10px}.ed .end .step{margin:0 0 12px}.ed .end .asks{display:flex;flex-wrap:wrap;gap:10px}"
    rules.append({
        "id": "02.24", "title": "Close every piece on one next step, with its date.",
        "rule": ["End every piece on the one step a reader is most likely to take, with its date and place and the way to take it. Link other ways to "
                 "take part from the step’s page."],
        "tokens": ["oa.color.action.ask.fill.onNewsprint"],
        "why": {"text": ["Four asks at the end of a piece leave a reader to choose, and most choose none. One dated step is easy to take before the date passes."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": A("s-02-24-correct", f'<div class="ed end">{hinge()}<p class="wycd">What you can do</p><p class="step">Send a written comment to the Alder County Board of Supervisors by 5 p.m. Wednesday, March 3, 2027. {ill()}</p><span class="ask" data-red="working" data-red-job="ask">Send a comment</span></div>',
                                  css=(BASE, END), rule="02.24", illustrative=True,
                                  alt="An illustrative ending. After the hinge divider, What you can do: send a written comment to the Alder County Board of Supervisors by 5 p.m. Wednesday, March 3, 2027. One red button: Send a comment."),
                    "caption": "The ending gives a single dated step at one place, with the button that takes it."},
        "failure": {"specimen": A("s-02-24-failure", f'<div class="ed end">{hinge()}<p class="wycd">What you can do</p><p class="step">Call your supervisor, email the board, share this post and show up! {ill()}</p>'
                                                     '<p class="asks"><span class="ask" data-red="failure">Call</span><span class="ask" data-red="failure">Email</span><span class="ask" data-red="failure">Share</span><span class="ask" data-red="failure">RSVP</span></p></div>',
                                  css=(BASE, END), rule="02.24", illustrative=True, exempt=["red", "contrast"],
                                  alt="The same ending with four asks and four red buttons, Call, Email, Share and RSVP, and no date."),
                    "caption": "Four asks and four red buttons leave out the date and the place, and give a reader no reason to start with any one of them."},
        "related": ["01", "12"],
        "builders": "Give the piece one ask button. Put the other ways to take part on the page the button opens.",
    })

    MCSS = ".ed .mech{max-width:900px}.ed .mech td{font-size:1rem}.ed .mech .lab{margin:0 0 4px}.ed .mech .qq{font-size:1.0625rem}.ed .mech .src{margin-top:6px}"
    mrows = [("A sweeping claim", "Our democracy is broken.", "The specific rule", "In 23 states, citizens can petition a proposed law or constitutional amendment onto the statewide ballot.", SRC_INITIATIVE, False),
             ("A feeling", "People are frustrated with Congress.", "A mechanism", "The committee chair decides which bills get a hearing.", "", False),
             ("A slogan", "Make your voice heard!", "A next step", "The hearing is Tuesday at 10 a.m. in Room 4, and the clerk signs up speakers until 9:45.", "", True),
             ("A side", "One party blocked the bill.", "The structure", "The stock trading ban needed 60 votes to move forward in the Senate, and it got 53.", SRC_SENATE, False)]
    mtr = "".join(f'<tr><td><p class="lab">{e(a)}</p><p class="qq">{e(q(b))}</p></td><td><p class="lab">{e(c)}</p><p class="qq">{e(q(d))}{" " + ill() if il else ""}</p>'
                  + (f'<p class="src">{e(s)}</p>' if s else "") + "</td></tr>" for a, b, c, d, s, il in mrows)
    mech = f'<div class="ed mech"><table class="stack"><thead><tr><th scope="col">What a draft says</th><th scope="col">What we publish</th></tr></thead><tbody>{mtr}</tbody></table></div>'
    mood = (f'<div class="ed"><div class="pc" style="width:360px"><p class="kick"><span class="chip solid">Explainer</span>{ill()}</p><p class="hl">Our democracy is broken.</p>'
            f'<p class="dek">People are frustrated with Congress, and one party blocked the bill again. Make your voice heard!</p></div></div>')
    rules.append({
        "id": "02.25", "title": "Publish the mechanism behind a mood.",
        "rule": ["When a draft states a sweeping claim, a feeling, a slogan or a side, replace it with the mechanism behind it: the rule, the office "
                 "that decides, the step a reader can take or the structure of the vote."],
        "why": {"text": ["A mood asks the reader to agree with us, and the mechanism behind it gives them something to check and an office to call."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": A("s-02-25-correct", mech, css=(BASE, MCSS), rule="02.25", interactive=True,
                                  alt="A table of four rows, what a draft says and what we publish. A sweeping claim, Our democracy is broken, becomes the specific rule: in 23 states, citizens can petition a proposed law or constitutional amendment onto the statewide ballot. A feeling, People are frustrated with Congress, becomes a mechanism: the committee chair decides which bills get a hearing. A slogan, Make your voice heard, becomes an illustrative next step: the hearing is Tuesday at 10 a.m. in Room 4. A side, One party blocked the bill, becomes the structure: the stock trading ban needed 60 votes to move forward in the Senate, and it got 53.",
                                  notes="Fifth-edition table, kept at Gate 0. Its unsourced 23-states line is replaced by a sourced count of working citizen-initiative states; the hearing line carries the Illustrative label; the cloture line now uses the Senate's September 30, 2026 vote."),
                    "caption": "Each mood on the left becomes a rule, an office, a dated step or a vote count a reader can check."},
        "failure": {"specimen": A("s-02-25-failure", mood, css=(BASE, PIECE), rule="02.25", illustrative=True,
                                  alt="An illustrative explainer card whose headline is Our democracy is broken, with the deck: People are frustrated with Congress, and one party blocked the bill again. Make your voice heard!"),
                    "caption": "Every line states a mood, which leaves the reader without a rule to check or an office to call."},
        "related": ["13", "01"],
        "builders": "For each sentence of a draft, ask which rule, office, date or count it rests on. Where the answer is none, the sentence is a mood.",
    })

    VCSS = """
.ed .voc{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,280px),1fr));gap:20px 32px;max-width:1000px}
.ed .voc>div{border-top:2px solid var(--oa-color-border-strong);padding-top:10px}
.ed .voc ul{margin:0;padding-left:1.1em;font-size:.9375rem;line-height:1.5}.ed .voc li{margin:0 0 4px}
.ed .voc dl{display:grid;grid-template-columns:minmax(6rem,42%) minmax(0,1fr);gap:4px 12px;margin:0;font-size:.9375rem}.ed .voc dt{font-weight:700}.ed .voc dd{margin:0}
.ed .out{text-decoration:line-through;text-decoration-thickness:1px}
"""
    use = ["rule", "decision", "record", "hearing", "vote", "office", "deadline", "step"]
    leave = [("genuinely, really, truly, actually, simply, just", "a fact, or nothing"), ("leverage (as a verb)", "use"), ("underscore, reflect", "show"),
             ("unprecedented", "the first time since a named date, sourced"), ("broken, crisis, rigged", "what changed, with its measure"),
             ("stakeholder", "the person or group by name or role"), ("empower", "the step the reader can take"), ("fight, battle, front", "propose, debate, vote, pass")]
    series = [("Reform 101", "Explain"), ("The Oath", "Explain"), ("Dispatch", "Track"), ("The Public Record", "Track"), ("Field Notes", "Connect"), ("Proof It Works", "Act")]
    terms = [("Hinge", "The ampersand’s job: joining a commitment to the action that keeps it. Chapter 04."),
             ("Lockmark", "The three by three grid of nodes beside the wordmark. Chapter 08."),
             ("Lever", "The lockmark’s larger red node, bottom right: the point that moves the structure. Chapter 08."),
             ("Signal Grid", "The lockmark’s grid used to code content, always with a key. Chapter 08."),
             ("Evidence grade", "How sure a claim is: documented, well supported, plausible, contested or hypothesis. Chapter 13.")]
    voc = (f'<div class="ed"><div class="voc"><div><p class="lab">Words we use</p><p>{e(", ".join(use[:-1]) + " and " + use[-1])}</p></div>'
           f'<div><p class="lab">Words we leave out, and what to write</p><dl>' + "".join(f'<dt><span class="out">{e(a)}</span></dt><dd>{e(b)}</dd>' for a, b in leave) + "</dl></div>"
           f'<div><p class="lab">Series names, exactly</p><dl>' + "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in series) + "</dl></div>"
           f'<div><p class="lab">Terms we define at first use</p><dl>' + "".join(f"<dt>{e(a)}</dt><dd>{e(b)}</dd>" for a, b in terms) + "</dl></div></div></div>")
    bad_v = ('<div class="ed"><div class="lnbox" style="max-width:620px;border-top:2px solid var(--oa-color-border-strong);padding-top:12px">'
             '<p style="font:600 1.375rem/1.4 var(--oa-font-family-reading)">Stakeholders must leverage this unprecedented moment to empower communities and fix a broken system. ' + ill() + '</p></div></div>')
    rules.append({
        "id": "02.26", "title": "Use the words a reader would use, and spell series names exactly.",
        "rule": ["Write rule, decision, record, hearing and vote, the words a reader uses for public business. Leave out the words this rule lists, "
                 "define each term of art at first use, and spell the six series names exactly."],
        "why": {"text": ["Every word on the list to leave out has a plainer one that says more. Exact series names let a reader find a series again."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": A("s-02-26-correct", voc, css=(BASE, VCSS), rule="02.26", interactive=True,
                                  alt="A vocabulary sheet in four parts. Words we use: rule, decision, record, hearing, vote, office, deadline and step. Words we leave out, with what to write instead: genuinely, really, truly, actually, simply and just; leverage as a verb; underscore and reflect; unprecedented; broken, crisis and rigged; stakeholder; empower; fight, battle and front. Series names: Reform 101 and The Oath for Explain, Dispatch and The Public Record for Track, Field Notes for Connect, Proof It Works for Act. Terms we define at first use: hinge, lockmark, lever, Signal Grid and evidence grade.",
                                  notes="Fifth-edition vocabulary, with the words W17, W18, Rule 01.14 and Rule 01.15 add. The fifth edition's list of words we use was cut short in the text census, so the last four words are the editor's. Series routes move to chapter 08."),
                    "caption": "The list to leave out pairs each word with what to write in its place."},
        "failure": {"specimen": A("s-02-26-failure", bad_v, css=(BASE,), rule="02.26", illustrative=True,
                                  alt="An illustrative sentence: Stakeholders must leverage this unprecedented moment to empower communities and fix a broken system."),
                    "caption": "Five words from the list fill one sentence, and it leaves the reader without a rule, an office or a step."},
        "related": ["08", "13"],
        "builders": "Search a draft for every word on the list to leave out, and check each series name against the list before a kicker ships.",
    })

    HH = ".ed .hhs{display:grid;gap:14px}"
    pairs_ok = [("The zoning code", "the rent."), ("The filing deadline", "the ballot."), ("The coverage rule", "the copay."), ("The records law", "the answer.")]
    hh_ok = '<div class="ed hhs">' + "".join(f'<p class="hh">{e(a)} {amp_h()} {e(b)}</p>' for a, b in pairs_ok) + "</div>"
    hh_bad = ('<div class="ed hhs"><p class="hh">The hearing ' + amp_h() + ' the vote.</p><p class="src">Our brand guide, fifth edition, chapter 02 Voice</p>'
              '<p class="hh">The problem ' + amp_h() + ' the solution.</p></div>')
    rules.append({
        "id": "02.27", "title": "Write a hinge headline as a rule, then what it produces.",
        "rule": ["A hinge headline joins two noun phrases with the ampersand. The first names a rule, and the second names what the rule produces "
                 "in a reader’s life. Chapter 04 sets how it is drawn."],
        "tokens": ["oa.font.family.display"],
        "why": {"text": ["A reader meets the rule they could change beside the result they already feel, which is the hinge between a commitment and the action that keeps it."],
                "basis": "Editorial judgment"},
        "correct": {"specimen": A("s-02-27-correct", hh_ok, css=(BASE, HL, HH), rule="02.27",
                                  alt="Four hinge headlines, each a rule and then its result: The zoning code and the rent. The filing deadline and the ballot. The coverage rule and the copay. The records law and the answer. Each ampersand is ampersand B in red."),
                    "caption": "Each headline names a rule first and what it produces second, and each works in any state."},
        "failure": {"specimen": A("s-02-27-failure", hh_bad, css=(BASE, HL, HH), rule="02.27",
                                  alt="Two failing hinge headlines. The hearing and the vote, from the fifth edition, names two events. The problem and the solution names no rule."),
                    "caption": "“The hearing & the vote.” puts an event first, and “The problem & the solution.” names no rule at all."},
        "files": [AMP_DISPLAY],
        "related": ["04", "01"],
        "builders": "Test a hinge headline by asking whether its first half is a rule a reader could look up. If not, rewrite it before chapter 04’s drawing rules apply.",
    })

    sources = sorted({r["source_line"] for r in W if r.get("source_line")} | {h["example_source"] for h in C["house_rules"] if h.get("example_source") and h["example_source"].startswith("Source")}
                     | {SRC_INITIATIVE, SRC_SENATE})
    sources.append("Our systems atlas, Who Do They Answer To?, glossary entry “Cloture”, for H02’s example.")

    data = {
        "number": "02", "anchor": "voice", "title": "Voice", "part": "Foundations",
        "instruction": "Write the way you’d explain a rule to a neighbor, and quote the brand lines exactly.",
        "intro": [C["narrative"][0], C["narrative"][1]],
        "rules": rules, "extras": extras, "sources": sources,
        "related_chapters": [{"chapter": "01", "reason": "What the voice serves, and the nonpartisan rules."}, {"chapter": "04", "reason": "How hinge headlines are drawn."},
                             {"chapter": "13", "reason": "Evidence grades, sourcing and the labels beside each item."}, {"chapter": "22", "reason": "The voice in email."}],
    }
    return data
