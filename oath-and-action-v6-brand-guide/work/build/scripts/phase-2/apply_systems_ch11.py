"""Chapter 11, Status and utility icons (systems designer). Trackers from the apply pass, November 7, 2026; stage B
round 2, November 10, 2026, adds records requests and agency rules, the utility icons, the error, success and warning
marks and five live specimens (apply_systems_ch11_ui.py).

Usage:
    python3 -I work/build/scripts/phase-2/apply_systems_ch11.py

Writes:
    work/build/guide/chapters/11-icons.json                 the chapter in the content contract (Stage A brief)
    work/build/guide/specimens/s-11-*.html                  one fragment per specimen
    work/build/guide/specimens/manifest-systems.json        the s-11-* entries, merged; the 05 to 07 entries are kept
    work/handoffs/phase-2/20261110_Stage-B-Round-2-Ch11-Figures.json   every figure the chapter prints, and how. The
                                                            apply pass's 20261107 figures file stays as its record.

Round 2 (20261110_Stage-B-Round-2-Brief.md, "Chapter 11"): invented state bills renumbered from H.99001 and S.99002 up
(DR-151); Nebraska's step 5 under the slash with "Nebraska has one chamber" (DR-150); Rule 11.7's 44 px for trackers
and every control that carries a utility icon (DR-153); records requests and agency rules on the tracker's marks
(DR-140, D2-526 to D2-529); every mark tagged data-icon and data-icon-family="status" (D2-517), on a group whose box is
the circle's own size, so guide check B-3 reads 24 to 30 px; and the mark widths in MARK_CSS read the mark tokens
(engineer's request, 20261109_Stage-B-Engineer-Notes.md).

Decisions it carries: DR-108 and DR-128 (six steps, step 6 named for whoever signs), DR-109 (numbered steps in lists and
on story cards, the same marks as a vertical timeline on a bill's own page), DR-110 (the lockmark codes nothing),
DR-97 (one Illustrative label at the head of each invented piece), D2-254 (fixed artboards on the type scale), D2-308
(failure band), D2-324 (the tracker rules open chapter 11), and the creative director's two open items on Board 6:
step 5's hearing, with the take-part mark shown on step 5, and a stopped bill drawn in a list.

The mark geometry follows Board 6's Option B and Option D (work/build/scripts/phase-2/board6_tracker_build.py, read and
never edited), set here in tokens: circle sizes, line weights, the slash, the square and the take-part badge. Two
changes from the board: the badge's Charcoal keyline sits inside its 11 px disc, as Rule 05.5 draws a keyline, with
1.5 px of the surface cut around it so it parts from the ring; and every type size is one the scale names (D2-254).

Contrast figures are computed from tokens.json with the systems designer's helpers (stage_a_systems_core.py). The
specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color, no px
font size, and every class prefixed sx- so no name meets a shell class.
"""
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent


def _load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


B = _load('stage_a_systems_build')
UI = _load('apply_systems_ch11_ui')
C = sys.modules['stage_a_systems_core']
ROOT = C.ROOT
OUT_CH = ROOT / 'work/build/guide/chapters/11-icons.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-systems.json'
FIG_OUT = ROOT / 'work/handoffs/phase-2/20261110_Stage-B-Round-2-Ch11-Figures.json'
CH = '11'
ILLUS = B.ILLUS
RED_W = 'data-red="working" data-red-job="take part now"'
ARROW = '<span aria-hidden="true"> →</span>'

# ------------------------------------------------------------------------------------------------ the six steps
STEPS = [
    ('Filed', 'A legislator files the bill, and it goes to a committee.'),
    ('Hearing', 'The committee holds a hearing and takes testimony on the bill. Many state legislatures take '
                'testimony from the public there. In Congress, the committee hears the witnesses it invites. A bill’s own '
                'page says how to take part.'),
    ('Committee vote', 'The committee votes on whether to send the bill to the full House or Senate.'),
    ('First chamber', 'The full House or Senate, wherever the bill was filed, votes on it.'),
    ('Second chamber', 'The other chamber takes the bill up. Its own committee can hold a hearing first, and then '
                       'the full chamber votes and both chambers agree on one text. Nebraska has one chamber, so a '
                       'Nebraska bill keeps this step under a slash.'),
    ('Governor', 'The governor signs or vetoes the bill, and lawmakers can vote to override a veto.'),
]
SIGNER = {'state': 'Governor', 'federal': 'President', 'nebraska': 'Governor'}
NEBRASKA = 'Nebraska has one chamber.'          # DR-150: on every Nebraska card, beside step 5's slash

# DR-140: a federal records request and a federal agency rule, each in six steps on the tracker's marks, from the research
# lead's section 7 (5 U.S.C. 552 and FOIA.gov; 5 U.S.C. 553, 801 and RegInfo.gov). D2-526: a request's step 6, Appeal, takes
# the slash when no appeal is filed; D2-527: a rule's step 1, Early notice, takes the slash when the agency skipped it.
REQUEST_STEPS = [
    ('Requested', 'The request reaches the agency’s records office in writing and describes the records. The agency’s 20 '
                  'working days to decide start.'),
    ('Acknowledged', 'The agency confirms it has the request and gives it a tracking number.'),
    ('Searching', 'The agency looks for the records.'),
    ('Reviewing', 'The agency decides what it can release, and blacks out what an exemption in the law protects.'),
    ('Answered', 'The agency sends its decision and the records it releases.'),
    ('Appeal', 'Only when the requester appeals. A higher office in the agency reviews the answer and decides. A request '
               'that is never appealed keeps this step under a slash once the time to appeal has passed.'),
]
RULE_STEPS = [
    ('Early notice', 'Optional. The agency asks whether or how to write a rule before it proposes one. A rule with no '
                     'early notice keeps this step under a slash.'),
    ('Proposed', 'The agency publishes the proposed rule in the Federal Register.'),
    ('Comments open', 'Anyone may send the agency written comments until the date the notice sets.'),
    ('Comments closed', 'The comment period has ended, and the agency weighs what it received.'),
    ('Final rule', 'The agency publishes the final rule with its answer to the comments and the date it takes effect, and '
                   'sends it to Congress.'),
    ('In effect', 'The rule takes effect, usually 30 days or more after the final rule is published, and 60 days or '
                  'more for a major rule.'),
]
# Round 5 (DR-231, DR-274, DR-275, R5-7): a state ballot measure (a citizen initiative) and a federal civil court case, each
# in six steps on the bill tracker's marks. Step names, what happens and the law behind each step are the research lead's
# "Facts for owners", item 1 (20261114_Round-5-Research-Notes.md, every source read November 14, 2026); each row is
# (name, what happens, where the law sets it). The extras after Rules 11.10 and 11.11 print these rows as tables.
BALLOT_STEPS = [
    ('Filed', 'The sponsors file the measure’s full text with the attorney general.',
     'Massachusetts Constitution, Amendment Article XLVIII, The Initiative, II, Section 3; California Elections Code 9001'),
    ('Title and summary', 'The attorney general clears the measure and writes the title and summary that petitions and '
                          'ballots carry.',
     'Massachusetts, Article XLVIII, The Initiative, II, Section 3; California Elections Code 9004 and 9014'),
    ('Signatures', 'The sponsors gather signatures, and election officials count and check them.',
     'Massachusetts, Article XLVIII, The Initiative, II, Section 3; California Elections Code 9030 and 9031'),
    ('Legislature', 'The Legislature votes on the measure first, where the state’s initiative is indirect; under a slash '
                    'where it goes straight to the ballot.',
     'Massachusetts, Amendment Article LXXXI, Section 2; Ohio Constitution, Article II, Section 1b; Michigan '
     'Constitution, Article II, Section 9'),
    ('On the ballot', 'The state’s election officer certifies the measure for the ballot.',
     'California Elections Code 9033; Massachusetts, Amendment Article LXXXI, Section 2'),
    ('Vote', 'The voters decide, and the state certifies the result.',
     'California Constitution, Article II, Section 10(a); Massachusetts, Amendment Article LXXXI, Section 2; Ohio, '
     'Article II, Section 1b; Michigan, Article II, Section 9'),
]
COURT_STEPS = [
    ('Filed', 'One side sues the other in a federal district court, the trial court.',
     'Federal Rules of Civil Procedure, Rule 3; 28 U.S.C. 1331'),
    ('Trial court ruling', 'The trial court decides, with or without a trial, unless the case settles or is dismissed.',
     'Federal Rules of Civil Procedure, Rules 41, 56 and 58'),
    ('Appeal', 'The side that lost asks a court of appeals to review the ruling.',
     '28 U.S.C. 1291 and 2107; Federal Rules of Appellate Procedure, Rule 4'),
    ('Appeals court ruling', 'Three judges of the court of appeals decide.',
     '28 U.S.C. 2106; Federal Rules of Appellate Procedure, Rules 40 and 41'),
    ('Supreme Court petition', 'The side that lost asks the Supreme Court to hear the case, and the Court agrees or '
                               'declines.',
     'Rules of the Supreme Court, Rules 10, 13 and 16; 28 U.S.C. 1254 and 2101'),
    ('Supreme Court ruling', 'The Supreme Court decides.',
     '28 U.S.C. 2106; Rules of the Supreme Court, Rule 16'),
]
# A higher court that affirms: the data lead's ED5-3 keeps the docket's own word, "Affirmed", explained once in Rule
# 11.11's text, since "Upheld" can read as if a law struck down below had survived.
AFFIRMED = 'Affirmed'
ROUTE_NAMES = {'request': [n for n, _ in REQUEST_STEPS], 'rule': [n for n, _ in RULE_STEPS],
               'ballot': [s[0] for s in BALLOT_STEPS], 'court': [s[0] for s in COURT_STEPS]}
STEP6_BOTH = ('The governor signs a state bill and the President signs a federal one. Either can veto it, and lawmakers '
              'can vote to override a veto.')
CLERK = ['Introduced', 'Referred', 'Reported', 'Engrossed', 'Enrolled', 'Presented']


def names(kind='state'):
    if kind in ROUTE_NAMES:
        return ROUTE_NAMES[kind]
    return [n for n, _ in STEPS[:5]] + [SIGNER[kind]]


STATE_WORD = {'done': 'Done', 'now': 'Now', 'take': 'You can take part now', 'notyet': 'Not yet',
              'skipped': 'Never happened', 'stopped': 'Stopped'}
STATE_MEANS = {
    'done': 'The step happened.',
    'now': 'The bill is at this step, and the words beside the tracker name it.',
    'take': 'The bill is at this step, and the public can act before a date. The red disc, its place on the ring and '
            'the words carry it together.',
    'notyet': 'The bill has not reached this step.',
    'skipped': 'The bill moved past this step without it, as when a committee votes without holding a hearing. It keeps '
               'its number, so the count still runs to six.',
    'stopped': 'The bill ended here, as when a committee votes it down or a veto stands. The line ends at this step.',
}
STATE_ORDER = ['done', 'now', 'take', 'notyet', 'skipped', 'stopped']

# Invented state bills on the neutral topics the guide uses (Illustrative, one label at the head of each piece)
LIST_BILLS = [
    dict(id='H.99001', title='Public meeting notice', states=['done', 'take', 'notyet', 'notyet', 'notyet', 'notyet'],
         line='Testimony is open until March 3.', take='Send written testimony or sign up to speak by March 3.',
         cta='How to send testimony'),
    dict(id='S.99002', title='School bus contracts', states=['done', 'done', 'done', 'now', 'notyet', 'notyet'],
         line='The committee sent it on, and the Senate votes next.'),
    dict(id='H.99003', title='Library hours', states=['done', 'done', 'done', 'done', 'done', 'now'],
         line='Both chambers passed it, and it waits for the governor to sign or veto it.'),
    dict(id='H.99004', title='Records request fees', states=['done', 'skipped', 'done', 'now', 'notyet', 'notyet'],
         line='Step 2 never happened, because the committee voted without holding a hearing. The House votes next.'),
    dict(id='S.99005', title='Parking meter fees', states=['done', 'done', 'done', 'done', 'done', 'stopped'],
         line='The governor vetoed it on February 9, and the Senate’s vote to override fell short on February 23.'),
]
LAW_BILL = dict(id='H.99003', title='Library hours', states=['done'] * 6, law='April 2', line='It takes effect July 1.')
OVERRIDE_BILL = dict(id='S.99006', title='Snow route parking', states=['done'] * 6, law='March 18',
                     how='over the governor’s veto', line='It takes effect June 1.')
STOP_BILL = LIST_BILLS[4]
CARD_BILL = dict(id='S.99007', title='Town audit deadlines', states=['done', 'done', 'done', 'done', 'take', 'notyet'],
                 line='The Senate passed it on February 24, and a House committee holds its hearing on March 10.',
                 take='Send written testimony or sign up to speak by March 10.', cta='How to send testimony')
FED_BILL = dict(id='H.R. 99012', title='Passport wait times', kind='federal',
                states=['done', 'done', 'done', 'done', 'done', 'now'],
                line='Both chambers passed it, and it waits for the President to sign or veto it.')
# DR-150: Nebraska keeps all six steps; step 5 takes the slash, and the card says why beside it. LB is Nebraska's prefix
# for a Legislative Bill; the number follows DR-151's range.
NE_BILL = dict(id='LB 99008', title='Rural clinic grants', kind='nebraska',
               states=['done', 'done', 'done', 'done', 'skipped', 'now'],
               line=NEBRASKA + ' The Legislature passed the bill on Final Reading on April 14, and it waits for the '
                               'governor to sign or veto it.')

# Invented records requests and agency rules (Illustrative), numbered from 99001 up with no agency named, so a cropped
# plate cannot put our words on a real request or a real rule. Round 3 (BE-S3): every request's subject is one a federal
# agency holds, since the steps, the 20 working days and the end words follow the federal Freedom of Information Act.
REQUESTS = [
    dict(id='99001', noun='Request', kind='request', title='Bridge inspection reports',
         states=['done', 'done', 'done', 'now', 'notyet', 'notyet'],
         line='The agency is deciding what it can release.'),
    dict(id='99003', noun='Request', kind='request', title='Food safety inspection records',
         states=['done', 'done', 'done', 'done', 'done', 'skipped'], end='Partly granted on March 3.',
         line='The agency released 212 of 340 pages and withheld the rest under two exemptions. No appeal was filed by '
              'the June 1 deadline.'),
    dict(id='99005', noun='Request', kind='request', title='Park ranger staffing records',
         states=['done', 'done', 'stopped', 'notyet', 'notyet', 'notyet'], end='Withdrawn by the requester on April 9.',
         line='The requester stopped the request while the agency searched.'),
]
RULES = [
    dict(id='99002', noun='Rule', kind='rule', title='Rail crossing signals',
         states=['skipped', 'done', 'take', 'notyet', 'notyet', 'notyet'],
         line='The agency proposed the rule on April 11 with no early notice, and comments are open until May 12.',
         take='Send the agency a written comment by May 12.', cta='How to send a comment'),
    dict(id='99004', noun='Rule', kind='rule', title='Grain dust limits',
         states=['skipped', 'skipped', 'skipped', 'skipped', 'done', 'done'], end='In effect since August 1.',
         line='Issued without advance comment. The agency takes comments until September 30 and may change the rule '
              'after it reads them.'),
    dict(id='99006', noun='Rule', kind='rule', title='Ferry life vest checks',
         states=['done', 'done', 'done', 'stopped', 'notyet', 'notyet'], end='Withdrawn by the agency on February 20.',
         line='The agency published a notice withdrawing its proposed rule after comments closed.'),
]
WAIT_REQUEST = dict(id='99007', noun='Request', kind='request', title='Weather station repair records',
                    states=['done', 'done', 'now', 'notyet', 'notyet', 'notyet'],
                    line='The agency is looking for the records.',
                    wait='Waiting on you: on April 2 the agency asked which years you need. Its 20 working days stop '
                         'until you answer.',
                    checked='Checked April 20. The agency may have acted since.')

# Round 5 (DR-275): invented ballot measures and court cases, labeled Illustrative, each plate's three in different states:
# one at its step now, one ended in words, one stopped on a square. They continue the records counter past 99009 and skip
# 99012, which H.R. 99012 holds; no state, court or party is named, so a cropped plate cannot put our words on a real one.
# The dates sit on one calendar: the November 3, 2026 election, Massachusetts's "first Wednesday of May" (May 6, 2026) and
# its 30 days to take effect (December 3), a Monday order list for the Supreme Court (January 11, 2027).
BALLOTS = [
    dict(id='99010', noun='Measure', kind='ballot', title='State park entry fees',
         states=['done', 'done', 'done', 'skipped', 'done', 'now'],
         line='Step 4 never happened: a direct initiative goes to the ballot with no vote in the Legislature. The polls '
              'closed on November 3. The count is unofficial until the state certifies it, set for November 25.'),
    dict(id='99011', noun='Measure', kind='ballot', title='Library district funding', states=['done'] * 6,
         end='Approved by voters on November 3, certified on November 24.',
         line='The Legislature did not pass it by May 5, so a second round of signatures sent it to the voters. It takes '
              'effect December 3.'),
    dict(id='99013', noun='Measure', kind='ballot', title='Lake shoreline setbacks',
         states=['done', 'done', 'stopped', 'notyet', 'notyet', 'notyet'],
         end='Too few valid signatures to qualify.',
         line='On July 14, a random sample of the signatures showed fewer valid ones than the law requires.'),
]
COURTS = [
    dict(id='99014', noun='Case', kind='court', title='Bakery name trademark',
         states=['done', 'done', 'done', 'now', 'notyet', 'notyet'],
         line='A panel of three judges heard argument on May 6 and has not ruled.'),
    dict(id='99015', noun='Case', kind='court', title='Ferry route contract', states=['done'] * 6,
         end='Reversed and sent back by the Supreme Court on June 2.',
         line='The appeals court takes the case up again.'),
    dict(id='99016', noun='Case', kind='court', title='Highway noise walls',
         states=['done', 'done', 'done', 'done', 'stopped', 'notyet'], end='Petition denied by the Supreme Court on January 11.',
         line='The appeals court’s ruling stands.'),
]

PAGE_BILL = dict(id='H.99001', title='Public meeting notice', states=LIST_BILLS[0]['states'],
                 dek='The bill would require towns to post notice of a public meeting online two days ahead.')
PAGE_NOTES = [
    'Filed January 16 and sent to the Committee on Local Government.',
    'The committee holds its public hearing on March 3, and testimony is open until then.',
    'The committee votes on whether to send the bill to the full House.',
    'The full House votes on the bill.',
    'The Senate takes it up. Its committee often holds a hearing of its own before both chambers agree on one text.',
    'The governor signs or vetoes the bill. Once it is signed, this page gives the date it became law and the date it '
    'takes effect.',
]


MONTH_DAY = re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December) (\d)')


def nb(text):
    """Keep a month with its day, a number with its unit and a step with its number on one line."""
    text = MONTH_DAY.sub('\\1' + C.NBSP + '\\2', text)
    text = re.sub(r'(\d) (px|pt)\b', '\\1' + C.NBSP + '\\2', text)
    return re.sub(r'\b([Ss]tep) (\d)', '\\1' + C.NBSP + '\\2', text)


def status_words(b, nm=None):
    """The bold status line: the end in words where the record has ended (a law, a request's answer, a rule's end),
    otherwise the step it is at, counted against its own number of steps."""
    nm = nm or names(b.get('kind', 'state'))
    n = len(b['states'])
    if b.get('law'):
        return f'Became law on {b["law"]}' + (f', {b["how"]}.' if b.get('how') else '.')
    if b.get('end'):
        return b['end']
    st = b['states']
    if 'stopped' in st:
        i = st.index('stopped')
        return f'Stopped at step {i + 1} of {n}: {nm[i]}.'
    i = next(k for k, s in enumerate(st) if s in ('now', 'take'))
    return f'Step {i + 1} of {n}: {nm[i]}.'


# ------------------------------------------------------------------------------------------------ marks
# Colors come from the surface through custom properties set once per specimen (see mark_vars()). Every width a mark
# token sets is read here from tokens.css by the mark's own class (engineer's request, D2-402, D2-578): the attribute
# values in the markup stay as the fallback and as the check's hook (guide_check.js, markTokens). A failure plate that
# draws a fault at another width carries none of these classes, so it keeps its own width.
MARK_TOKENS = {
    'rn': ('stroke-width', 'var(--oa-component-mark-ring-now)'),
    'ra': ('stroke-width', 'var(--oa-component-mark-ring-ahead)'),
    'sl': ('stroke-width', 'var(--oa-component-mark-slash)'),
    'lr': ('height', 'var(--oa-component-mark-line-reached)'),
    'la': ('height', 'var(--oa-component-mark-line-ahead)'),
    'td': ('r', 'calc(var(--oa-component-mark-take-part-disc) / 2)'),
    'tk': ('stroke-width', 'var(--oa-component-mark-take-part-keyline)'),
    'tc': ('r', 'calc(var(--oa-component-mark-take-part-disc) / 2 + var(--oa-component-mark-take-part-cut))'),
}
MARK_CSS = ('.mk{display:block;overflow:visible;flex:none}'
            '.mk .fi{fill:var(--ink)}.mk .fs{fill:var(--sub)}.mk .fb{fill:var(--bg)}.mk .ft{fill:var(--txt2)}'
            '.mk .fr{fill:var(--red)}.mk .si{stroke:var(--ink)}.mk .ss{stroke:var(--sub)}.mk .sk{stroke:var(--key)}'
            '.mk line,.mk .nf{fill:none}'
            '.mk text{font-family:var(--oa-font-family-reading);font-weight:700;font-variant-numeric:tabular-nums;'
            'text-anchor:middle}.mk text:not([font-size]){font-size:0.8125rem}'
            '.mk text.tl{font-weight:600}'
            '.mk text.halo{paint-order:stroke;stroke:var(--bg);stroke-width:var(--oa-component-mark-halo);'
            'stroke-linejoin:round}'
            + ''.join(f'.mk .{k}{{{prop}:{val}}}' for k, (prop, val) in MARK_TOKENS.items())
            + '.mk .tk{r:calc(var(--oa-component-mark-take-part-disc) / 2 - var(--oa-component-mark-take-part-keyline) / 2)}')
# D2-517: every mark carries data-icon and data-icon-family="status"; the id names the state
STATE_ICON = {'done': 'S-done', 'now': 'S-now', 'take': 'S-take-part', 'notyet': 'S-not-yet', 'skipped': 'S-never-happened',
              'stopped': 'S-stopped'}


def mark_vars(ctx, surf, follow=False):
    """The colors a mark needs on one surface, read from the surface's tokens. follow=True (round 5, chapter 11's own
    pieces) takes the surface color from the stage's role, --oa-color-surface, like every other color here, so a piece
    drawn for Newsprint keeps its numbers and ring fills on a Charcoal stage too; on a Newsprint stage the role is
    Newsprint, so nothing on the page moves. Chapter 01's card (guide_editor_ch01.py) keeps the default."""
    on = {'n': 'onNewsprint', 'c': 'onCharcoal'}[surf]
    v = ctx.v
    for k in ('graphic.essential', 'graphic.subtle', 'text.primary', 'text.secondary', 'border.hairline', 'border.strong'):
        v(f'oa.color.{k}.{on}')       # the long names the short ones point at on this surface, for the figures record
    # The stage carries the surface's class, which points the short role names at that surface's values (shell notes,
    # section 5), so a piece on Charcoal draws in Charcoal's tokens with the same declarations.
    return (f'--ink:{v("oa.color.graphic.essential")};--sub:{v("oa.color.graphic.subtle")};'
            f'--bg:{v("oa.color.surface" if follow and surf == "n" else "oa.color.surface." + ("newsprint" if surf == "n" else "charcoal"))};'
            f'--txt:{v("oa.color.text.primary")};--txt2:{v("oa.color.text.secondary")};'
            f'--hair:{v("oa.color.border.hairline")};--strong:{v("oa.color.border.strong")};'
            f'--red:{v("oa.color.palette.pillarRed")};--key:{v("oa.component.button.ask.keyline.onNewsprint")}')


def svg(w, h, body, scale=1, cls='mk', extra=''):
    return (f'<svg class="{cls}" width="{w * scale:g}" height="{h * scale:g}" viewBox="0 0 {w:g} {h:g}" '
            f'aria-hidden="true" focusable="false"{extra}>{body}</svg>')


def badge(cx, cy, r=5.5, red=True):
    """The take-part mark: an 11 px red disc with a 1 px Charcoal keyline inside its edge (Rule 05.5), cut from the
    ring by 1.5 px of the surface. red=False draws the same disc in the surface ink: a failure plate, or the yielding
    take-part mark of Rule 11.18, which keeps its shape and its words when an error holds the view's red."""
    tok = abs(r - 5.5) < 1e-9
    gap = f'<circle cx="{cx:g}" cy="{cy:g}" r="{r + 1.5:g}" class="fb{" tc" if tok else ""}"/>'
    if not red:
        return gap + f'<circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="fi{" td" if tok else ""}"/>'
    return (gap + f'<g {RED_W}><circle cx="{cx:g}" cy="{cy:g}" r="{r:g}" class="fr{" td" if tok else ""}"/>'
            f'<circle cx="{cx:g}" cy="{cy:g}" r="{r - 0.5:g}" class="sk nf{" tk" if tok else ""}" stroke-width="1"/></g>')


def node(cx, cy, d, st, num=None, fs=None, red=True, tag=True):
    """One numbered step (Board 6, Option B): filled when done, a heavy ring now, a fine ring ahead, the fine ring
    under a slash when the step never happened, a filled square where the record stopped.

    The mark sits in a group tagged data-icon and data-icon-family="status" (D2-517), with a clear square of the circle's
    own size first, so the group's box is the circle's: guide check B-3 reads 24, 26, 28 or 30 px. The take-part disc
    sits outside that box, after the group. red=False draws the disc in ink (Rule 11.18); tag=False leaves a fault's
    drawing in a failure plate untagged."""
    R = d / 2
    fs = fs or (14 if d >= 28 else 13)
    fsa = '' if fs == 13 else f' font-size="{fs}"'    # 13 px comes from the marks' CSS (0.8125rem)
    ty = cy + 0.36 * fs
    t = ''
    after = ''
    if st == 'done':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R:g}" class="fi"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fb"{fsa}>{num}</text>'
    elif st in ('now', 'take'):
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 1.5:g}" class="fb si rn" stroke-width="3"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fi"{fsa}>{num}</text>'
        if st == 'take':
            after = badge(cx + R * 0.72, cy - R * 0.72, 5.5 if d >= 24 else 4.5, red=red)
    elif st == 'notyet':
        s = f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" class="fb ss ra" stroke-width="1.5"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="ft tl"{fsa}>{num}</text>'
    elif st == 'skipped':
        k = (R + 2) * 0.7071
        s = (f'<circle cx="{cx:g}" cy="{cy:g}" r="{R - 0.75:g}" class="fb ss ra" stroke-width="1.5"/>'
             f'<line x1="{cx - k:.2f}" y1="{cy + k:.2f}" x2="{cx + k:.2f}" y2="{cy - k:.2f}" class="si sl" stroke-width="2"/>')
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="ft tl halo"{fsa}>{num}</text>'
    elif st == 'stopped':
        s = f'<rect x="{cx - R + 1:g}" y="{cy - R + 1:g}" width="{d - 2:g}" height="{d - 2:g}" class="fi"/>'
        if num:
            t = f'<text x="{cx:g}" y="{ty:.2f}" class="fb"{fsa}>{num}</text>'
    else:
        raise ValueError(st)
    if not tag:
        return f'<g>{s}{t}</g>{after}'
    box = f'<rect x="{cx - R:g}" y="{cy - R:g}" width="{d:g}" height="{d:g}" fill="none"/>'
    return (f'<g data-icon="{STATE_ICON[st]}" data-icon-family="status">{box}{s}{t}</g>{after}')


def line_segments(states, xs, cy, red=False):
    """2 px in the surface ink as far as the record has come, 1 px Stone ahead, nothing after a stop."""
    out = []
    stop = states.index('stopped') if 'stopped' in states else None
    for i in range(len(xs) - 1):
        if stop is not None and i >= stop:
            break
        if states[i + 1] != 'notyet':
            cls = 'fr' if red else 'fi'
            out.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="2" class="{cls} lr"/>')
        else:
            out.append(f'<rect x="{xs[i]:g}" y="{cy - 1:g}" width="{xs[i + 1] - xs[i]:g}" height="1" class="fs la"/>')
    return out


def steps_svg(states, W, d, red_progress=False, fs=None, hang=False, red=True, tag=True):
    """Numbered steps across a row W px wide. Centered: an equal share of the row to each step, so names fit under the
    circles. hang=True: the first circle starts on the text edge and the last ends on the far edge, for rows whose names
    sit in a key. red_progress draws the line and the done steps in Pillar Red, for the failure plate of Rule 11.4 only.
    Six steps for every route; a failure plate may pass seven."""
    n = len(states)
    if hang:
        c = (W - d) // (n - 1)
        xs = [d / 2 + c * i for i in range(n)]
    else:
        c = W // n
        xs = [c * i + c // 2 for i in range(n)]
    R = d / 2
    cy = 6 + R
    H = int(cy + R + 2)
    segs = line_segments(states, xs, cy, red=red_progress)
    body = [f'<g data-red="working" data-red-job="progress">{x}</g>' if 'class="fr' in x else x for x in segs]
    for i, (x, s) in enumerate(zip(xs, states)):
        if red_progress and s == 'done':
            body.append(f'<g data-red="working" data-red-job="progress"><circle cx="{x:g}" cy="{cy:g}" r="{R:g}" class="fr"/>'
                        f'<text x="{x:g}" y="{cy + 0.36 * 13:.2f}" class="fi" font-size="13">{i + 1}</text></g>')
        else:
            body.append(node(x, cy, d, s, i + 1, fs, red=red, tag=tag))
    return svg(W, H, ''.join(body))


def dots_svg(states, W):
    """Board 6's Option A, for the failure plate of Rule 11.5: unnumbered dots on a line."""
    c = W // 6
    xs = [c * i + c // 2 for i in range(6)]
    cy = 11
    body = line_segments(states, xs, cy)
    for x, s in zip(xs, states):
        if s == 'done':
            body.append(f'<circle cx="{x}" cy="{cy}" r="5" class="fi"/>')
        elif s in ('now', 'take'):
            body.append(f'<circle cx="{x}" cy="{cy}" r="8" class="fb si" stroke-width="2"/>')
            if s == 'take':
                body.append(f'<g {RED_W}><circle cx="{x}" cy="{cy}" r="4" class="fr"/>'
                            f'<circle cx="{x}" cy="{cy}" r="3.5" class="sk nf" stroke-width="1"/></g>')
        else:
            body.append(f'<circle cx="{x}" cy="{cy}" r="4" class="fb ss" stroke-width="1.5"/>')
    return svg(W, 22, ''.join(body))


def sample(st, d=26, scale=1, num=4, tag=True):
    """One step centered in a square 14 px wider than the circle, which leaves room for the badge. tag=False for an
    enlarged copy, which shows the mark for inspection and is no use of it (guide check B-3 reads the true-size one)."""
    W = d + 14
    return svg(W, W, node(W / 2, W / 2, d, st, num, tag=tag), scale, cls='mk mk-s')


def uicon(name, px=24, transform=None, cls=None):
    """A utility icon from the sprite (D2-589; promotion, the engineer's pattern in guide_build.py): oa-sym-u-<name>-<px>px,
    hidden beside its word (A-1) and tagged for the checks (D2-517). transform turns or mirrors it, as the utility
    manifest gives for each state; it draws in the word's ink through currentColor and never in red (DR-161)."""
    t = f' transform="{transform}"' if transform else ''
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" focusable="false" '
            f'data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"{t}/></svg>')


def labels(nm, states, W):
    """Step names under the circles, in the wide form: the current step in bold, a skipped one says so."""
    lis = []
    for i, s in enumerate(states):
        cls = ' class="cur"' if s in ('now', 'take', 'stopped') else ''
        extra = '<span class="lx">never happened</span>' if s == 'skipped' else ''
        lis.append(f'<li{cls}>{nm[i]}{extra}</li>')
    n = len(states)
    return (f'<ol class="lbls" style="width:{W}px;grid-template-columns:repeat({n},{W // n}px)">{"".join(lis)}</ol>')


# ------------------------------------------------------------------------------------------------ pieces
def piece_css(ctx, surf, size, sizing='floor'):
    """Styles every tracker piece shares, for a surface ('n', 'c') and a width ('s' 360 px, 'l' 600 px)."""
    T = ctx.ty
    h3 = T('h3', 'ceil' if sizing == 'ceil' else 'floor')
    return (f':scope{{{mark_vars(ctx, surf, follow=True)}}}' + MARK_CSS +
            f'.pc{{padding:20px 16px 24px;color:var(--txt)}}'
            + ('.pc{padding:24px 24px 28px}' if size == 'l' else '') +
            f':where(.pc p){{margin:0}}'
            f'.hd{{margin:0 0 16px;{h3};text-wrap:balance}}'
            f'.rows{{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}}'
            f'.row{{padding:16px 0 18px;border-bottom:1px solid var(--hair)}}'
            f'.bill{{margin:0 0 12px;{T("body")};line-height:1.35}}.bill b{{font-weight:700}}'
            f'.mkw{{display:flex;justify-content:center}}'
            f'.st{{margin-top:8px;{T("bodySmall")};line-height:1.5;text-wrap:pretty}}.st b{{font-weight:700}}'
            f'.tp{{display:flex;gap:8px;align-items:flex-start;margin-top:8px;{T("bodySmall")};line-height:1.5}}.tp > span{{text-wrap:pretty}}'
            f'.tp .mk{{margin-top:-6px}}.tp b{{font-weight:700}}'
            f'.cta{{display:inline-flex;align-items:center;min-height:{ctx.v("oa.size.target.touch")};{T("ui")};'
            f'text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}}'
            f'.ctaw{{margin:2px 0 -6px}}'
            f'.lbls{{list-style:none;margin:6px 0 0;padding:0;display:grid;{T("dataLabel")};color:var(--txt2);text-align:center}}'
            f'.lbls li{{padding:0 4px}}.lbls li.cur{{color:var(--txt);font-weight:700}}.lbls .lx{{display:block}}'
            f'.key{{margin-top:20px;{T("caption")};color:var(--txt2)}}'
            f'.kh{{{T("label")};color:var(--txt);margin:12px 0 6px}}.kh:first-child{{margin-top:0}}'
            f'.ks{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:2px 14px}}.ks b{{color:var(--txt)}}'
            f'.km{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 18px}}'
            f'.km li{{display:inline-flex;align-items:center;gap:6px}}'
            + ('.mkw{justify-content:flex-start}' if size == 'l' else ''))


def records_css(ctx):
    """What a records request or agency rule adds to a piece: the wait in words and the dated check under the warning
    mark (Rule 11.12), drawn in the text's ink."""
    T = ctx.ty
    return (f'.wt{{margin-top:6px;{T("bodySmall")};line-height:1.5;text-wrap:pretty}}'
            f'.wn{{display:flex;gap:8px;align-items:flex-start;margin-top:12px;'
            f'padding:{ctx.v("oa.space.100")} {ctx.v("oa.space.150")};'
            f'border-left:{ctx.v("oa.border.width.bar")} solid {ctx.v("oa.color.state.warning.mark.onNewsprint")};'
            f'{T("bodySmall")};line-height:1.5;color:{ctx.v("oa.color.state.warning.text.onNewsprint")}}}'
            f'.wn svg{{flex:none;display:block;margin-top:-1px}}'
            f'.wn b{{font-weight:700}}')


def key(nm, show=('done', 'now', 'notyet', 'skipped', 'stopped', 'take'), steps=True, red=True):
    k = ''
    if steps:
        k = (f'<p class="kh">The {C.num(len(nm))} steps</p><ol class="ks">'
             + ''.join(f'<li><b>{i + 1}</b> {n}</li>' for i, n in enumerate(nm)) + '</ol>')
    lis = ''.join(f'<li>{svg(38, 38, node(19, 19, 24, s, 4, red=red), cls="mk mk-s")}<span>{STATE_WORD[s]}</span></li>'
                  for s in show)
    return f'<div class="key">{k}<p class="kh">What the marks mean</p><ul class="km">{lis}</ul></div>'


def take_part(b, size='s', red=True):
    if 'take' not in b['states']:
        return ''
    n = b['states'].index('take') + 1
    mark = svg(38, 38, node(19, 19, 24, 'take', n, red=red), cls='mk mk-s')
    return (f'<p class="tp">{mark}<span><b>You can take part now.</b> {b["take"]}</span></p>'
            f'<p class="ctaw"><span class="cta">{b["cta"]}{ARROW}</span></p>')


def row(b, size, nm=None, red_progress=False, step_word=None, kind_label=None, red=True):
    nm = nm or names(b.get('kind', 'state'))
    W, d = (328, 26) if size == 's' else (552, 30)
    if size == 'card':
        W, d = 328, 24
    head = (f'<span class="kd">{kind_label}</span> ' if kind_label else '')
    bill = f'<p class="bill">{head}<span><b>{b.get("noun", "Bill")} {b["id"]}</b>, {b["title"]}</span></p>'
    marks = f'<div class="mkw">{steps_svg(b["states"], W, d, red_progress, hang=(size != "l"), red=red)}</div>'
    lab = labels(nm, b['states'], W) if size == 'l' else ''
    sw = step_word or status_words(b, nm)
    st = f'<p class="st"><b>{sw}</b> {b["line"]}</p>'
    wait = f'<p class="wt">{b["wait"]}</p>' if b.get('wait') else ''
    chk = f'<p class="wn">{uicon("warning")}<span><b>Warning:</b> {b["checked"]}</span></p>' if b.get('checked') else ''
    core = f'{marks}{lab}{st}{wait}{take_part(b, size, red=red)}{chk}'
    return f'<li class="row">{bill}{core}</li>'


def bill_list(ctx, sid_surf, size, bills, title, nm=None, extra_key=None):
    nm = nm or names()
    show = [s for s in ('done', 'now', 'notyet', 'skipped', 'stopped', 'take')
            if any(s in b['states'] for b in bills) or s in ('done', 'now', 'notyet')]
    rows = ''.join(row(b, size, nm) for b in bills)
    k = key(nm, show, steps=(size == 's'))
    return f'<div class="pc"><p>{ILLUS}</p><p class="hd">{title}</p><ul class="rows">{rows}</ul>{k}</div>'


# ------------------------------------------------------------------------------------------------ specimens
SURF_NAME = {'n': 'newsprint', 'c': 'charcoal'}


NBHY = '\u2011'


def nb_html(html, fixed=False):
    """nb() on the text of a fragment, outside tags and styles. fixed=True also turns every hyphen between two letters
    or figures into a non-breaking hyphen (U+2011), so a hyphenated compound or an ID never splits at a line end in a
    plate of fixed width (CA-S4, D2-950)."""
    parts = re.split(r'(<style[^>]*>.*?</style>|<script[^>]*>.*?</script>|<[^>]+>)', html, flags=re.S)
    fix = (lambda t: re.sub(r'(?<=\w)-(?=\w)', NBHY, t)) if fixed else (lambda t: t)
    return ''.join(x if x.startswith('<') else fix(nb(x)) for x in parts)


def _css_rules(css):
    """Split CSS into top-level pieces: (prelude, body) for a rule or an at-rule block."""
    out, i, depth, start = [], 0, 0, 0
    head = None
    while i < len(css):
        ch = css[i]
        if ch == '{':
            if depth == 0:
                head = css[start:i]
                body_start = i + 1
            depth += 1
        elif ch == '}':
            depth -= 1
            if depth == 0:
                out.append((head.strip(), css[body_start:i]))
                start = i + 1
        i += 1
    return out


def prune_css(css, classes):
    """Keep only the rules whose selectors can meet this piece's markup: a selector that names a class the markup
    never carries is dropped, and an at-rule keeps what is left inside it. The pieces share one set of styles
    (piece_css, ui_css), and each specimen carries only what it draws, which keeps chapter 11 inside its weight."""
    out = []
    for head, body in _css_rules(css):
        if head.startswith('@'):
            inner = prune_css(body, classes)
            if inner:
                out.append(f'{head}{{{inner}}}')
            continue
        sels = [x for x in head.split(',') if all(c in classes for c in re.findall(r'\.([A-Za-z][\w-]*)', x))]
        if sels:
            out.append(f'{",".join(sels)}{{{body}}}')
    return ''.join(out)


def prune_styles(html):
    classes = set()
    for m in re.finditer(r'class="([^"]*)"', re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.S)):
        classes.update(m.group(1).split())
    classes.add('illus')
    return re.sub(r'(<style[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + prune_css(m.group(2), classes) + m.group(3),
                  html, flags=re.S)


def spec(ctx, sid, html, rule, alt, **kw):
    if re.search(r'Stage \d+ of 9|Signal Grid', re.sub(r'<[^>]+>', '', html)):
        raise ValueError(f'{sid}: a retired tracker phrase in a specimen')
    if (kw.get('width') or 0) > 600:
        # CA-M1: the chapter column holds a 606 px stage from a 768 px window up, so no plate is wider than 600 px
        raise ValueError(f'{sid}: wider than 600 px, so it would scroll inside the chapter column at true size')
    html = prune_styles(html)
    # font: resets font-variant-numeric, so a type style's own "normal" after it adds nothing
    html = re.sub(r';font-variant-numeric:var\(--oa-type-(?:title|section|quote|intro|body|body-small|ui|caption|label|ask)'
                  r'-font-variant-numeric\)', '', html)
    # letter-spacing 0em and text-transform none for the reading styles: the stage inherits those values, and no piece
    # here sets one of these styles inside a label, whose capitals and tracking it would otherwise have to undo
    html = re.sub(r';(?:letter-spacing|text-transform):var\(--oa-type-(?:intro|body|body-small|ui|caption|ask)'
                  r'-(?:letter-spacing|text-transform)\)', '', html)
    if not (kw.get('readable') or kw.get('interactive')):
        # a picture's marks need no measuring frame: guide check B-3 reads marks only outside pictures
        html = re.sub(r'<rect x="[^"]*" y="[^"]*" width="[^"]*" height="[^"]*" fill="none"/>', '', html)
    out = ctx.spec(sid, nb_html(html, fixed=bool(kw.get('width'))), CH, rule, alt, **kw)
    if kw.get('width'):
        # D2-442 offers Fit to window only where fitting keeps every text at 13 px or more; every fixed plate here sets
        # 13 px step names or numbers, so no fit can be offered, and the switch's markup stays out of the page
        ctx.specs[sid]['meta']['fit_switch'] = False
    return out


def alt_list(bills, nm=None):
    out = []
    for b in bills:
        nm2 = nm or names(b.get('kind', 'state'))
        st = '; '.join(f'{i + 1} {nm2[i]} {STATE_WORD[s].lower()}' for i, s in enumerate(b['states']))
        tp = f' You can take part now: {b["take"]}' if 'take' in b['states'] else ''
        out.append(f'Bill {b["id"]}, {b["title"]}: {status_words(b, nm2)} {b["line"]} Steps: {st}.{tp}')
    return ' '.join(out)


def s_steps(ctx):
    rows = ''.join(f'<tr><th scope="row"><span class="n">{i + 1}</span> {n if i < 5 else "Governor or President"}</th>'
                   f'<td>{m if i < 5 else STEP6_BOTH}</td></tr>' for i, (n, m) in enumerate(STEPS))
    T = ctx.ty
    css = (f'table{{width:100%;border-collapse:collapse;{T("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px 16px 12px 0;border-bottom:1px solid '
           f'{ctx.v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{T("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")};border-bottom:2px solid '
           f'{ctx.v("oa.color.border.strong.onNewsprint")}}}'
           f'tbody th{{{T("ui")};width:13rem}}th .n{{display:inline-block;min-width:1.4em;{T("h4")};'
           f'font-variant-numeric:tabular-nums}}td{{max-width:34rem}}'
           f'@container (max-width:30rem){{tbody th{{width:6.5rem;padding-right:12px}}th .n{{display:block}}}}.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr"><table><thead><tr><th scope="col">Step</th>'
            f'<th scope="col">What happens</th></tr></thead><tbody>{rows}</tbody></table></div>')
    alt = ('The six steps, with what happens at each. ' + ' '.join(
        f'{i + 1}, {n if i < 5 else "Governor or President"}: {m if i < 5 else STEP6_BOTH}' for i, (n, m) in enumerate(STEPS)))
    return spec(ctx, 's-11-steps', html, None, alt, readable=True,
                notes='A readable table (D2-255). Step 6 is named for whoever signs (DR-128).')


def mark_rows():
    """PP-M1: each mark's geometry at every circle size, read from node() and line_segments() so the words and the
    drawing cannot drift apart. Sizes are the four of Rule 11.7."""
    ds = (24, 26, 28, 30)
    px = lambda xs: ', '.join(f'{x:g}' for x in xs[:-1]) + f' and {xs[-1]:g} px'
    off = px([round(0.72 * d / 2, 2) for d in ds])       # node(): the badge sits at (cx + 0.72 R, cy - 0.72 R)
    slash = px([d + 4 for d in ds])                       # node(): k = (R + 2) cos 45, so the slash runs d + 4 long
    square = px([d - 2 for d in ds])                      # node(): the stopped square is d - 2 wide
    ink, sub = '--oa-color-graphic-essential-on-&lt;surface&gt;', '--oa-color-graphic-subtle-on-&lt;surface&gt;'
    t2, bg = '--oa-color-text-secondary-on-&lt;surface&gt;', '--oa-color-surface-&lt;surface&gt;'
    return [
        ('Done', 'A filled circle as wide as the step, its number in the surface color.', '', f'{ink}; number {bg}'),
        ('Now', 'A ring as wide as the step, its 3 px line drawn inside the edge, filled with the surface. Its number '
                'in Inter 700, in ink.', '--oa-component-mark-ring-now', ink),
        ('You can take part now', 'The Now ring with an 11 px disc. The disc’s center sits 0.72 of the circle’s radius '
                                  f'right of and above the circle’s center, at 45 degrees: {off}. '
                                  'A 1 px Charcoal keyline sits inside the disc’s edge, and 1.5 px of the surface is cut '
                                  'around it.',
         '--oa-component-mark-take-part-disc, --oa-component-mark-take-part-keyline and '
         '--oa-component-mark-take-part-cut',
         '--oa-color-palette-pillar-red; keyline --oa-component-button-ask-keyline-on-newsprint'),
        ('Not yet', 'A ring as wide as the step, its 1.5 px line drawn inside the edge, filled with the surface. Its '
                    'number in Inter 600, in the secondary text color.', '--oa-component-mark-ring-ahead',
         f'{sub}; number {t2}'),
        ('Never happened', 'The Not yet ring under a 2 px slash in ink at 45 degrees, from lower left to upper right '
                           f'through the center. The slash is 4 px longer than the circle is wide, {slash}, so it runs '
                           '2 px past the ring at each end.', '--oa-component-mark-slash', f'slash {ink}; ring {sub}'),
        ('Halo', 'On a step that never happened, a 4 px stroke in the surface color painted under the number, which '
                 'shows 2 px around each figure and parts it from the slash.', '--oa-component-mark-halo', bg),
        ('Stopped', f'A filled square 2 px narrower than the circle, {square}, centered where the circle would be. Its '
                    'number in the surface color. The line ends here.', '', ink),
        ('Line reached', 'A 2 px bar centered on the circles, from step to step as far as the record has come. It runs '
                         'into a step that never happened, the last step included, since the record moved past it.',
         '--oa-component-mark-line-reached', ink),
        ('Line ahead', 'A 1 px bar from the current step to the next one and on. After a stopped step, no line.',
         '--oa-component-mark-line-ahead', sub),
        ('Numbers', 'Inter at 13 px in circles of 24 and 26 px and 14 px from 28 px, tabular figures, centered, with the '
                    'baseline 0.36 of the type size below the circle’s center.', '', ''),
    ]


def s_marks_table(ctx):
    """PP-M1: one table a developer can build every mark from, after Rule 11.2."""
    T = ctx.ty
    def code(t):
        """Each token name in its own code span, its "--oa-" prefix and first word held together, so a name only
        breaks after a later hyphen."""
        return re.sub(r'--oa-([a-z]+)-(\S+?)(?=[;,]\s|\s|$)', r'<code><span class="nw">--oa-\1-</span>\2</code>', t)
    rows = ''.join(f'<tr><th scope="row">{m}</th><td>{how}</td><td>{code(w) if w else "No token"}</td>'
                   f'<td>{code(c) if c else "Given in each mark’s row"}</td></tr>'
                   for m, how, w, c in mark_rows())
    css = (f'table{{width:100%;border-collapse:collapse;{T("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px 16px 12px 0;border-bottom:1px solid '
           f'{ctx.v("oa.color.border.hairline.onNewsprint")}}}'
           f'thead th{{{T("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")};border-bottom:2px solid '
           f'{ctx.v("oa.color.border.strong.onNewsprint")}}}'
           f'tbody th{{{T("ui")};font-weight:700;width:8.5rem}}.nw{{white-space:nowrap}}td code{{{T("dataLabel")};letter-spacing:0;'
           f'text-transform:none;font-variant-numeric:normal}}'
           f'td:nth-child(3),td:nth-child(4){{width:10rem}}'
           f'@container (max-width:40rem){{thead{{display:none}}tr{{display:block;padding:12px 0;border-bottom:1px solid '
           f'{ctx.v("oa.color.border.hairline.onNewsprint")}}}th,td,td:nth-child(3),td:nth-child(4){{display:block;width:auto;'
           f'padding:0 0 6px;border:0}}'
           f'td:nth-child(3)::before{{content:"Line or size: "}}td:nth-child(4)::before{{content:"Color: "}}}}'
           f'.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr"><table><thead><tr><th scope="col">Mark</th><th scope="col">How to draw '
            f'it at 24, 26, 28 and 30 px</th><th scope="col">Line or size token</th><th scope="col">Color token</th>'
            f'</tr></thead><tbody>{rows}</tbody></table></div>')
    plain = lambda t: re.sub(r'<[^>]+>', '', t).replace('&lt;', '<').replace('&gt;', '>')
    alt = ('Drawing the marks: a table of each mark, how to draw it at the four circle sizes, its line or size token and '
           'its color token. ' + ' '.join(f'{m}: {plain(how)}' for m, how, _, _ in mark_rows()))
    return spec(ctx, 's-11-marks-drawn', html, None, alt, readable=True,
                notes='A readable table (D2-255) for PP-M1. Every figure is computed from node() and line_segments().')


def s_11_1(ctx):
    """CA-M1: the forms of step 6 sit one above the other in a 360 px piece, so every name shows at true size in every
    chapter column and on a phone. Each bill keeps its own key. Round 2 adds a Nebraska bill (DR-150): six steps, step 5
    under the slash, "Nebraska has one chamber" beside the marks."""
    T = ctx.ty
    css = piece_css(ctx, 'n', 's') + (f'.kd{{display:block;margin:0 0 4px;{T("label")};color:var(--txt2)}}'
                                      f'.sig{{padding:16px 0 20px;border-bottom:1px solid var(--hair)}}'
                                      f'.sig:first-of-type{{border-top:1px solid var(--hair)}}.sig:last-of-type{{border-bottom:0;padding-bottom:0}}.sig .key{{margin-top:14px}}'
                                      f'.sig .rows{{border:0}}.sig .row{{padding:0;border:0}}')
    blocks = ''
    for b, label, show in ((dict(LIST_BILLS[2], kind='state'), 'A state bill', ('done', 'now')),
                           (FED_BILL, 'A federal bill', ('done', 'now')),
                           (NE_BILL, 'A Nebraska bill', ('done', 'skipped', 'now'))):
        nm = names(b.get('kind', 'state'))
        blocks += (f'<div class="sig"><p class="kd">{label}</p><ul class="rows">{row(b, "s", nm)}</ul>'
                   f'{key(nm, show)}</div>')
    html = (f'<style>{css}</style><div class="pc"><p>{ILLUS}</p><p class="hd">Three bills that wait for a signature</p>'
            f'{blocks}</div>')
    alt = ('Three Illustrative bills at 360 px on Newsprint, one above the other, each drawn as six numbered steps with '
           'its own key. A state bill, H.99003, Library hours, has steps 1 to 5 done and stands now at step 6: “Step 6 of 6: '
           'Governor. Both chambers passed it, and it waits for the governor to sign or veto it.” Its key reads 1 Filed, '
           '2 Hearing, 3 Committee vote, 4 First chamber, 5 Second chamber, 6 Governor. A federal bill, H.R. 99012, '
           'Passport wait times, has steps 1 to 5 done and stands now at the same place: “Step 6 of 6: President. Both chambers passed it, and it waits '
           'for the President to sign or veto it.” Its key ends 6 President. A Nebraska bill, LB 99008, Rural clinic '
           'grants, has steps 1 to 4 done; step 5 never happened, and the bill stands now at step 6: “Step 6 of '
           '6: Governor. Nebraska has one chamber. The Legislature passed the bill on Final Reading on April 14, and it '
           'waits for the governor to sign or veto it.” Its key adds the mark for a step that never happened.')
    spec(ctx, 's-11-1-correct', html, '11.1', alt, width=360, illustrative=True)
    fcss, band = ctx.fail_band(flush=True)
    css2 = piece_css(ctx, 'n', 's') + fcss
    b = dict(LIST_BILLS[2])
    r = row(b, 's', nm=CLERK, step_word='Step 6 of 6: Presented.')
    r = r.replace('Both chambers passed it, and it waits for the governor to sign or veto it.',
                  'The enrolled bill went to the executive on February 12.')
    html2 = (f'<style>{css2}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where the library hours bill stands</p>'
             f'<ul class="rows">{r}</ul>{key(CLERK, ("done", "now"))}</div>')
    alt2 = ('Failure case: do not publish. An Illustrative tracker for bill H.99003, Library hours, at 360 px, '
            'whose key gives the six steps the clerk’s names: Introduced, Referred, Reported, Engrossed, Enrolled and '
            'Presented. It reads “Step 6 of 6: Presented. The enrolled bill went to the executive on February 12.”')
    spec(ctx, 's-11-1-failure', html2, '11.1', alt2, width=360, illustrative=True)

def s_11_2(ctx):
    T = ctx.ty
    css = (f':scope{{{mark_vars(ctx, "n", follow=True)}}}' + MARK_CSS +
           f'.sk-l{{list-style:none;margin:0;padding:0;display:grid;gap:12px;'
           f'grid-template-columns:repeat(auto-fill,minmax(min(100%,13.5rem),1fr))}}'
           f'.sk-c{{border:1px solid var(--hair);padding:14px 14px 16px}}'
           f'.sk-m{{display:flex;align-items:center;gap:16px;min-height:40px}}'
           f'.sk-n{{margin:8px 0 2px;{T("ui")};font-weight:700}}.sk-t{{margin:0;{T("caption")};color:var(--txt2)}}'
           f'.sk-h{{margin:0 0 12px;{T("caption")};color:var(--txt2)}}')
    cards = ''.join(f'<li class="sk-c"><div class="sk-m" aria-hidden="true">{sample(s, 26)}</div>'
                    f'<p class="sk-n">{STATE_WORD[s]}</p><p class="sk-t">{STATE_MEANS[s]}</p></li>' for s in STATE_ORDER)
    html = (f'<style>{css}</style><p class="sk-h">Each mark is drawn on step 4, at true size in a 26 px circle.</p>'
            f'<ul class="sk-l">{cards}</ul>')
    alt = ('The six states of a step, each drawn on step 4 at true size in a 26 px circle, with its name and meaning. '
           + ' '.join(f'{STATE_WORD[s]}: {STATE_MEANS[s]}' for s in STATE_ORDER)
           + ' Done is a filled circle; Now is a heavy ring; You can take part now is the heavy ring with a small red '
             'disc at its upper right; Not yet is a fine ring; Never happened is the fine ring under a slash; Stopped is '
             'a filled square.')
    spec(ctx, 's-11-2-correct', html, '11.2', alt, readable=True,
         notes='A readable list (D2-255); the marks are hidden from assistive technology and every state is in words.')

    fcss, band = ctx.fail_band(flush=True)
    hue = {'done': 'oa.color.palette.verdigris', 'now': 'oa.color.palette.prussian', 'notyet': 'oa.color.palette.stone'}
    st = ['done', 'done', 'done', 'now', 'notyet', 'notyet']
    c = 324 // 6
    xs = [c * i + c // 2 for i in range(6)]
    body = [f'<rect x="{xs[0]}" y="15" width="{xs[-1] - xs[0]}" height="2" style="fill:{ctx.v("oa.color.palette.stone")}"/>']
    for i, (x, s) in enumerate(zip(xs, st)):
        body.append(f'<circle cx="{x}" cy="16" r="13" style="fill:{ctx.v(hue[s])}"/>'
                    f'<text x="{x}" y="20.68" font-size="13" style="fill:{ctx.v("oa.color.palette.white")}">{i + 1}</text>')
    mk = svg(324, 32, ''.join(body))
    css2 = (MARK_CSS + fcss + f'.pr{{display:grid;gap:20px}}.k{{margin:0 0 8px;{T("label")};color:{ctx.v("oa.color.text.secondary.onNewsprint")}}}'
            f'.g .mk{{filter:grayscale(1)}}.wr{{padding:16px 16px 20px}}')
    html2 = (f'<style>{css2}</style>{band}<div class="wr"><p style="margin:0 0 16px">{ILLUS}</p><div class="pr">'
             f'<div><p class="k">In color</p>{mk}</div><div class="g"><p class="k">In grayscale</p>{mk}</div></div></div>')
    gv, gs, gp = (C.css_gray(ctx.hx(hue[k])) for k in ('done', 'notyet', 'now'))
    rr = ctx.ratio(gv, gs, 'contrast of Verdigris and Stone in grayscale')
    rh = ctx.ratio('oa.color.palette.verdigris', 'oa.color.palette.stone', 'contrast of Verdigris and Stone')
    ctx.fig('grayscale of Verdigris, Stone and Prussian', f'{gv}, {gs}, {gp}',
            'CSS grayscale(1): 0.2126 R + 0.7152 G + 0.0722 B on the encoded token values')
    alt2 = ('Failure case: do not publish. An Illustrative row of six identical numbered circles that tell their '
            'states by hue alone: Verdigris for the three done steps, Prussian for step 4, where the bill is now, and '
            f'Stone for steps 5 and 6 ahead, with no word for any state. Below it, the same row in grayscale, where the '
            f'Verdigris and Stone circles print as grays {rr} to 1 apart.')
    spec(ctx, 's-11-2-failure', html2, '11.2', alt2, width=360, illustrative=True,
         notes=f'Verdigris against Stone {rh} to 1 in color; grays {gv} and {gs} measure {rr} to 1.')
    return rr, rh


def s_11_3(ctx):
    css = piece_css(ctx, 'n', 's')
    rows = row(LAW_BILL, 's') + row(OVERRIDE_BILL, 's') + row(STOP_BILL, 's')
    html = (f'<style>{css}</style><div class="pc"><p>{ILLUS}</p><p class="hd">How three state bills ended</p>'
            f'<ul class="rows">{rows}</ul>{key(names(), ("done", "stopped"))}</div>')
    alt = ('Three Illustrative bills at 360 px on Newsprint. Bill H.99003, Library hours: its six numbered steps, '
           'steps 1 to 6, are all done, and the words say “Became law on April 2. It takes effect July 1.” Bill S.99006, Snow route parking: '
           'steps 1 to 6 are done, and the words say “Became law on March 18, over the governor’s veto. It takes effect '
           'June 1.” Bill S.99005, Parking meter fees: steps 1 to 5 are done, and the bill stopped at step 6, where the '
           'line ends. The words say “Stopped at step 6 of 6: Governor. The governor vetoed it on February 9, and the '
           'Senate’s vote to override fell short on February 23.” A key gives the six step names and the Done and Stopped '
           'marks.')
    spec(ctx, 's-11-3-correct', html, '11.3', alt, width=360, illustrative=True)
    fcss, band = ctx.fail_band(flush=True)
    css2 = piece_css(ctx, 'n', 's') + fcss
    nm = names()[:5] + ['Law']
    r = row(LIST_BILLS[2], 's', nm=nm)
    html2 = (f'<style>{css2}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where the library hours bill stands</p>'
             f'<ul class="rows">{r}</ul>{key(nm, ("done", "now", "notyet"))}</div>')
    alt2 = ('Failure case: do not publish. An Illustrative tracker for bill H.99003, Library hours, whose sixth step '
            'is named Law. Steps 1 to 5 are done and the bill stands now at step 6, so the words read “Step 6 of 6: Law. '
            'Both chambers passed it, and it waits for the governor to sign or veto it.”')
    spec(ctx, 's-11-3-failure', html2, '11.3', alt2, width=360, illustrative=True)


def card(ctx, red_progress=False):
    T = ctx.ty
    css = piece_css(ctx, 'n', 's') + (f'.cd{{border-top:2px solid var(--strong);padding:16px 0 0}}'
                                      f'.ky{{margin:0;{T("label")};color:var(--txt2)}}'
                                      f'.ch{{margin:8px 0 8px;{T("h4", "floor")};text-wrap:balance}}'
                                      f'.dk{{margin:0 0 16px;{T("body")};text-wrap:pretty}}'
                                      f'.cd .rows{{border:0}}.cd .row{{padding:0;border:0}}')
    b = CARD_BILL
    r = row(b, 'card', red_progress=red_progress)
    html = (f'<div class="pc"><p style="margin-bottom:12px">{ILLUS}</p><div class="cd"><p class="ky">Tracker · State bills</p>'
            f'<p class="ch">The House hears the town audit bill on March 10</p>'
            f'<p class="dk">The bill would move each town’s deadline for its yearly audit from June 30 to September 30.</p>'
            f'<ul class="rows">{r}</ul>{key(names(), ("done", "take", "notyet"))}</div></div>')
    return css, html


def s_11_4(ctx):
    css, html = card(ctx)
    alt = ('An Illustrative story card at 360 px on Newsprint with the kicker Tracker, State bills, the headline “The '
           'House hears the town audit bill on March 10”, and a line on what the bill would do. Under it, bill S.99007, '
           'Town audit deadlines, as six numbered steps: steps 1 to 4 done, step 5 where you can take part now, marked by '
           'the small red disc on its ring, and step 6 not yet. The words say “Step 5 of 6: Second chamber. The Senate passed it on '
           'February 24, and a House committee holds its hearing on March 10.” Beside the same red disc, “You can take '
           'part now. Send written testimony or sign up to speak by March 10.”, then the link How to send testimony.')
    spec(ctx, 's-11-4-correct', f'<style>{css}</style>{html}', '11.4', alt, width=360, illustrative=True)
    fcss, band = ctx.fail_band(flush=True)
    css2, html2 = card(ctx, red_progress=True)
    alt2 = ('Failure case: do not publish. The same Illustrative story card, with the line and the four done '
            'steps drawn in Pillar Red, so red marks how far the bill has come as well as the red disc on step 5 that '
            'says you can take part now.')
    spec(ctx, 's-11-4-failure', f'<style>{css2}{fcss}</style>{band}{html2}', '11.4', alt2, width=360, illustrative=True,
         exempt=['red', 'contrast'],
         notes='Labeled failure: red spent on progress as well as the take-part mark (two red jobs), and numbers on red '
               'fills that pass only as large text.')


def s_11_5(ctx):
    sids = {}
    # Round 2 (weight, chapter 11's 0.55 MB budget): one extra shows the wide form and the Charcoal surface together,
    # with two of the five bills, the take-part step and the veto, which carry the form's red and its square.
    three = [LIST_BILLS[0], LIST_BILLS[4]]
    for surf, size in (('n', 's'), ('c', 'l')):
        if True:
            css = piece_css(ctx, surf, size)
            bills = LIST_BILLS if (surf, size) == ('n', 's') else three
            n = C.num(len(bills))
            html = f'<style>{css}</style>' + bill_list(ctx, surf, size, bills, f'Where {n} state bills stand this week')
            w = 360 if size == 's' else 600
            ground = 'Newsprint' if surf == 'n' else 'Charcoal'
            sid = 's-11-5-correct' if (surf, size) == ('n', 's') else f's-11-list-{w}-{SURF_NAME[surf]}'
            where = ('with the step names in a key after the list' if size == 's'
                     else 'with each step’s name under its circle and the bill’s name above its steps')
            alt = (f'An Illustrative list of {n} state bills at {w:,} px on {ground}, each drawn as six numbered steps on a '
                   f'line, {where}. ' + alt_list(bills))
            spec(ctx, sid, html, '11.5' if sid == 's-11-5-correct' else None, alt, width=w, illustrative=True,
                 surface=SURF_NAME[surf])
            sids[(surf, size)] = sid
    fcss, band = ctx.fail_band(flush=True)
    css = piece_css(ctx, 'n', 's') + fcss + '.mkw{padding:4px 0}'
    rows = ''
    for b in LIST_BILLS[:2]:
        rows += (f'<li class="row"><p class="bill"><b>Bill {b["id"]}</b>, {b["title"]}</p>'
                 f'<div class="mkw">{dots_svg(b["states"], 324)}</div>'
                 f'<p class="st"><b>{status_words(b)}</b> {b["line"]}</p></li>')
    html = (f'<style>{css}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where two state bills stand this week</p>'
            f'<ul class="rows">{rows}</ul></div>')
    alt = ('Failure case: do not publish. Two Illustrative bills at 360 px on Newsprint, each drawn as six small '
           'dots on a line with no numbers or names. H.99001’s second dot is a ring with a red center, and S.99002’s fourth '
           'dot is a ring, so a reader counts dots to find the step. The status words sit under each line.')
    spec(ctx, 's-11-5-failure', html, '11.5', alt, width=360, illustrative=True)
    return sids


def timeline(b, d, notes, surf, page=True, generic=False):
    lis = []
    nm = names()
    st = b['states']
    for i, s in enumerate(st):
        seg = 'seg-end' if i == 5 else ('seg-on' if st[i + 1] != 'notyet' else 'seg-off')
        cur = ' cur' if s in ('now', 'take') else ''
        word = 'Now: you can take part' if s == 'take' else STATE_WORD[s]
        box = ''
        if s == 'take' and page:
            box = (f'<div class="tbox"><p class="tp">{sample("take", 24, num=i + 1)}<span><b>You can take part now.</b> '
                   f'Send written testimony or sign up to speak by March 3.</span></p>'
                   f'<p class="askw" {RED_W}><span class="ask">Send testimony</span></p></div>')
        if generic:
            mark = generic_mark(s)
        else:
            mark = sample(s, d, num=i + 1)
        lis.append(f'<li class="{seg}{cur}">{mark}<span class="vt-t"><span class="vt-n">{nm[i]}</span>'
                   + ('' if generic else f'<span class="vt-s">{word}</span>')
                   + (f'<span class="vt-note">{notes[i]}</span>' if notes else '') + f'{box}</span></li>')
    return f'<ol class="vt" style="--d:{d}px">{"".join(lis)}</ol>'


def generic_mark(s):
    """A stock stepper's marks, for the failure plate of Rule 11.6: a check, a dot or an empty box, with no number."""
    if s == 'done':
        body = ('<rect x="7" y="7" width="28" height="28" class="fi"/>'
                '<path d="M14 21.5l5 5 9-10" class="nf" style="stroke:var(--bg)" stroke-width="2.5"/>')
    elif s in ('now', 'take'):
        body = ('<rect x="8" y="8" width="26" height="26" class="fb si" stroke-width="2"/>'
                '<circle cx="21" cy="21" r="5" class="fi"/>')
    else:
        body = '<rect x="8.5" y="8.5" width="25" height="25" class="fb ss" stroke-width="1"/>'
    return svg(42, 42, body, cls='mk mk-s')


def page_css(ctx, surf, size):
    T = ctx.ty
    on = {'n': 'onNewsprint', 'c': 'onCharcoal'}[surf]
    keyline = (f';box-sizing:border-box;border:{ctx.v("oa.border.width.hairline")} solid '
               f'{ctx.v("oa.component.button.ask.keyline.onNewsprint")}' if surf == 'n' else '')
    return (piece_css(ctx, surf, size) +
            f'.chip{{display:inline-flex;{T("dataLabel")};border:1px solid var(--strong);vertical-align:middle}}'
            f'.chip span{{padding:4px 6px}}.chip span:first-child{{background:var(--ink);color:var(--bg)}}'
            f'.ky{{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;margin:12px 0 12px;{T("label")};color:var(--txt2)}}'
            f'.hd{{margin:0 0 8px}}'
            f'.dk{{margin:0 0 12px;{T("body")};text-wrap:pretty}}'
            f'.pg > .st{{margin:0 0 20px;padding-bottom:16px;border-bottom:1px solid var(--hair)}}'
            f'.vt{{list-style:none;margin:0;padding:0}}'
            f'.vt li{{position:relative;display:grid;grid-template-columns:calc(var(--d) + 14px) minmax(0,1fr);column-gap:6px;'
            f'padding-bottom:14px;min-height:calc(var(--d) + 14px)}}'
            f'.vt li::after{{content:"";position:absolute;left:calc(var(--d) / 2 + 6px);width:2px;top:calc(var(--d) + 7px);'
            f'bottom:-7px;background:var(--ink)}}'
            f'.vt li.seg-off::after{{width:1px;left:calc(var(--d) / 2 + 6.5px);background:var(--sub)}}'
            f'.vt li.seg-end::after{{display:none}}'
            f'.vt-t{{padding-top:calc(var(--d) / 2 - 5px);display:flex;flex-direction:column;min-width:0}}'
            f'.vt-n{{{T("body")};font-weight:600;line-height:1.35}}.vt li.cur .vt-n{{font-weight:700}}'
            f'.vt-s{{{T("label")};color:var(--txt2)}}.vt li.cur .vt-s{{color:var(--txt)}}'
            f'.vt-note{{{T("bodySmall")};line-height:1.5;margin-top:2px;text-wrap:pretty}}'
            f'.tbox{{margin:12px 0 4px;padding:14px;border:2px solid var(--strong)}}.tbox .tp{{margin:0 0 12px}}'
            f'.askw{{margin:0}}'
            f'.ask{{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;'
            f'background:{ctx.v("oa.component.button.ask.fill." + on)};color:{ctx.v("oa.component.button.ask.label." + on)};'
            f'{T("ask")}{keyline}}}'
            f'.aside{{{T("caption")};border-top:2px solid var(--strong);padding-top:12px;margin-top:12px}}'
            f'.aside ol{{margin:0;padding:0;list-style:none}}.aside li{{margin:0 0 8px}}.aside b{{font-weight:700}}')


def bill_page(ctx, surf, size, generic=False):
    b = PAGE_BILL
    tl = timeline(b, 28, PAGE_NOTES if not generic else None, surf, page=not generic, generic=generic)
    head = (f'<p>{ILLUS}</p><p class="ky"><span>Tracker · State bills</span>'
            f'<span class="chip"><span>Bill</span><span>H.99001</span></span></p>'
            f'<p class="hd">Public meeting notice</p><p class="dk">{b["dek"]}</p>'
            + ('' if generic else f'<p class="st"><b>{status_words(b)}</b> Testimony is open until March 3.</p>'))
    if size == 'l':
        aside = ('<div class="aside"><p class="kh">What the six steps mean</p><ol>'
                 + ''.join(f'<li><b>{i + 1} {n}.</b> {m}</li>' for i, (n, m) in enumerate(STEPS)) + '</ol></div>')
        body = f'{tl}{aside}'
    else:
        body = tl
    return f'<div class="pc pg">{head}{body}</div>'


def s_11_6(ctx):
    sids = {}
    # Round 2 (weight): the phone page on Charcoal and the wide page leave the chapter. The Charcoal list after Rule 11.5
    # shows the surface, and the wide page's key of meanings is the table of the six steps after Rule 11.1.
    for surf, size in (('n', 's'),):
        w = 360 if size == 's' else 600
        ground = 'Newsprint' if surf == 'n' else 'Charcoal'
        html = f'<style>{page_css(ctx, surf, size)}</style>{bill_page(ctx, surf, size)}'
        sid = 's-11-6-correct' if (surf, size) == ('n', 's') else f's-11-page-{w}-{SURF_NAME[surf]}'
        aside = (' After the steps, a key says what each of the six steps means.' if size == 'l' else '')
        alt = (f'An Illustrative page for one bill at {w:,} px on {ground}: the kicker Tracker, State bills, the ID Bill '
               f'H.99001, the title Public meeting notice and a line on what the bill would do, then “Step 2 of 6: Hearing. '
               f'Testimony is open until March 3.” The six numbered steps run down the page on a line, each with its name, '
               f'its state in words and a note: 1 Filed, done, filed January 16 and sent to the Committee on Local '
               f'Government; 2 Hearing, now, you can take part, with a red disc on its ring and a box holding “You can take '
               f'part now. Send written testimony or sign up to speak by March 3.” and a red Send testimony button; 3 '
               f'Committee vote, 4 First chamber, 5 Second chamber and 6 Governor, each not yet, with a note on what '
               f'happens there. Step 5’s note says the Senate’s committee often holds a hearing of its own.' + aside)
        spec(ctx, sid, html, '11.6' if sid == 's-11-6-correct' else None, alt, width=w, illustrative=True,
             surface=SURF_NAME[surf])
        sids[(surf, size)] = sid
    fcss, band = ctx.fail_band(flush=True)
    html = f'<style>{page_css(ctx, "n", "s")}{fcss}</style>{band}{bill_page(ctx, "n", "s", generic=True)}'
    alt = ('Failure case: do not publish. The same Illustrative page for bill H.99001, Public meeting notice, with '
           'a generic stepper from a component library in place of the numbered steps: a filled box with a check for step 1, a box with a dot for '
           'step 2 and empty boxes for steps 3 to 6, with no numbers, no state in words and no way to take part.')
    spec(ctx, 's-11-6-failure', html, '11.6', alt, width=360, illustrative=True)
    return sids


def s_11_7(ctx):
    T = ctx.ty
    css = (f':scope{{{mark_vars(ctx, "n", follow=True)}}}' + MARK_CSS +
           f'.sz{{list-style:none;margin:0;padding:0;border-top:1px solid var(--hair)}}'
           f'.sz li{{display:grid;grid-template-columns:minmax(0,12rem) minmax(0,1fr);gap:8px 24px;align-items:center;'
           f'padding:12px 0;border-bottom:1px solid var(--hair)}}'
           f'.sz-m{{display:flex;align-items:center;gap:4px}}'
           f'.sz-n{{margin:0;{T("ui")}}}.sz-t{{margin:2px 0 0;{T("caption")};color:var(--txt2)}}'
           f'.tg{{display:flex;flex-wrap:wrap;gap:24px 40px;margin-top:24px;align-items:flex-end}}'
           f'.tgi{{display:flex;align-items:stretch;gap:10px}}'
           f'.dim{{position:relative;width:12px;border-top:1px solid var(--ink);border-bottom:1px solid var(--ink)}}'
           f'.dim::before{{content:"";position:absolute;left:5px;top:0;bottom:0;border-left:1px solid var(--ink)}}'
           f'.dv{{display:flex;flex-direction:column;justify-content:center;{T("dataLabel")}}}'
           f'.cta{{display:inline-flex;align-items:center;min-height:{ctx.v("oa.size.target.touch")};{T("ui")};'
           f'text-decoration:underline;text-underline-offset:3px;outline:1px dashed var(--sub);outline-offset:0}}'
           f'.ask{{display:inline-flex;align-items:center;min-height:48px;padding:0 20px;'
           f'background:{ctx.v("oa.component.button.ask.fill.onNewsprint")};color:{ctx.v("oa.component.button.ask.label.onNewsprint")};'
           f'{T("ask")};box-sizing:border-box;border:{ctx.v("oa.border.width.hairline")} solid '
           f'{ctx.v("oa.component.button.ask.keyline.onNewsprint")}}}'
           f'@container (max-width:30rem){{.sz li{{grid-template-columns:1fr}}}}.wr{{container-type:inline-size}}')
    sizes = [(24, 13, 'On a story card', '24 px circles, numbers at 13 px'),
             (26, 13, 'In a list at 360 px', '26 px circles, numbers at 13 px'),
             (28, 14, 'On a bill’s own page', '28 px circles, numbers at 14 px'),
             (30, 14, 'In a wide list', '30 px circles, numbers at 14 px')]
    lis = ''
    for d, fs, where, what in sizes:
        marks = ''.join(svg(d + 14, d + 14, node((d + 14) / 2, (d + 14) / 2, d, s, n, fs), cls='mk mk-s')
                        for s, n in (('done', 1), ('take', 2), ('notyet', 3)))
        lis += (f'<li><div class="sz-m" aria-hidden="true">{marks}</div><div><p class="sz-n">{where}</p>'
                f'<p class="sz-t">{what}</p></div></li>')
    tg = (f'<div class="tg"><div class="tgi"><span class="dim" aria-hidden="true"></span><div><span class="cta">How to send '
          f'testimony{ARROW}</span></div><span class="dv">44 px tall</span></div>'
          f'<div class="tgi"><span class="dim" aria-hidden="true"></span><div {RED_W}><span class="ask">Send testimony</span></div>'
          f'<span class="dv">48 px tall</span></div></div>')
    html = f'<style>{css}</style><div class="wr"><ul class="sz">{lis}</ul>{tg}</div>'
    alt = ('The tracker’s four sizes at true size, each drawn as a done step, a step where you can take part and a step '
           'ahead: 24 px circles with 13 px numbers on a story card, 26 px with 13 px numbers in a list at 360 px, 28 px '
           'with 14 px numbers on a bill’s own page and 30 px with 14 px numbers in a wide list. Below them, the '
           'link How to send testimony with a bracket marking it 44 px tall, and the red Send testimony button marked '
           '48 px tall.')
    spec(ctx, 's-11-7-correct', html, '11.7', alt, readable=True,
         notes='A readable list (D2-255). Circle sizes and number sizes are the ones every tracker plate in this chapter draws.')
    fcss, band = ctx.fail_band(flush=True)
    b = LIST_BILLS[0]
    small = steps_svg(b['states'], 324, 16, fs=9)
    css2 = (piece_css(ctx, 'n', 's') + fcss +
            '.tiny{display:inline-block;font-size:0.6875rem;line-height:20px;text-decoration:underline;outline:1px dashed var(--sub)}')
    html2 = (f'<style>{css2}</style>{band}<div class="pc"><p>{ILLUS}</p><ul class="rows"><li class="row">'
             f'<p class="bill"><b>Bill {b["id"]}</b>, {b["title"]}</p><div class="mkw">{small}</div>'
             f'<p class="st"><b>{status_words(b)}</b> {b["line"]}</p>'
             f'<p class="tp"><span class="tiny">Send testimony</span></p></li></ul></div>')
    alt2 = ('Failure case: do not publish. An Illustrative tracker for bill H.99001 drawn with 16 px circles and '
            'numbers 9 px tall, and a Send testimony link 20 px tall in 11 px type, marked with a dashed outline.')
    spec(ctx, 's-11-7-failure', html2, '11.7', alt2, width=360, illustrative=True, exempt=['size', 'scale'],
         notes='Labeled failure: numbers at 9 px and a link at 11 px, off the scale on purpose and under the 13 px floor.')


# ------------------------------------------------------------------------------------------------ records requests and agency rules
REQ_KEY = ('done', 'now', 'notyet', 'skipped', 'stopped')
RULE_KEY = ('done', 'take', 'notyet', 'skipped', 'stopped')


def alt_rows(items, nm):
    """One sentence per record for an alt: its number, title, status words, line, wait and check, and each step's state."""
    out = []
    for b in items:
        st = '; '.join(f'{i + 1} {nm[i]} {STATE_WORD[s].lower()}' for i, s in enumerate(b['states']))
        tp = f' You can take part now: {b["take"]}' if 'take' in b['states'] else ''
        wt = f' {b["wait"]}' if b.get('wait') else ''
        ck = f' Beside the warning mark and a 4 px bar in ink: Warning: {b["checked"]}' if b.get('checked') else ''
        out.append(f'{b.get("noun", "Bill")} {b["id"]}, {b["title"]}: {status_words(b, nm)} {b["line"]}{wt} Steps: {st}.{tp}{ck}')
    return ' '.join(out)


def records_piece(ctx, title, items, nm, show, band=''):
    css = piece_css(ctx, 'n', 's') + records_css(ctx)
    fcss = ''
    if band:
        fcss, band = ctx.fail_band(flush=True)
    rows = ''.join(row(b, 's', nm) for b in items)
    return (f'<style>{css}{fcss}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">{title}</p>'
            f'<ul class="rows">{rows}</ul>{key(nm, show)}</div>')


def s_11_8(ctx):
    nm = names('request')
    html = records_piece(ctx, 'Where three records requests stand', REQUESTS, nm, REQ_KEY)
    alt = ('Three Illustrative records requests at 360 px on Newsprint, each drawn as six numbered steps with the bill '
           'tracker’s marks, and a key of the six steps, Requested, Acknowledged, Searching, Reviewing, Answered and '
           'Appeal, and of the marks. ' + alt_rows(REQUESTS, nm))
    spec(ctx, 's-11-8-correct', html, '11.8', alt, width=360, illustrative=True)
    bad = dict(REQUESTS[2], end='Full denial for reasons other than exemptions.',
               line='The agency closed the request on April 9.')
    html2 = records_piece(ctx, 'Where the park ranger records request stands', [bad], nm, ('done', 'stopped'), band=True)
    alt2 = ('Failure case: do not publish. An Illustrative records request, 99005, Park ranger staffing records, at '
            '360 px: steps 1 and 2 done, and the request stopped at step 3, Searching, where the line ends. The words read “Full '
            'denial for reasons other than exemptions. The agency closed the request on April 9.” The requester withdrew '
            'it, and nothing on the card says so.')
    spec(ctx, 's-11-8-failure', html2, '11.8', alt2, width=360, illustrative=True)


def s_11_9(ctx):
    nm = names('rule')
    html = records_piece(ctx, 'Where three agency rules stand', RULES, nm, RULE_KEY)
    alt = ('Three Illustrative federal agency rules at 360 px on Newsprint, each drawn as six numbered steps with the bill '
           'tracker’s marks, and a key of the six steps, Early notice, Proposed, Comments open, Comments closed, Final '
           'rule and In effect, and of the marks. ' + alt_rows(RULES, nm))
    spec(ctx, 's-11-9-correct', html, '11.9', alt, width=360, illustrative=True)
    bad = dict(RULES[1], states=['skipped', 'done', 'done', 'done', 'done', 'done'],
               line='The agency published the final rule on August 1.')
    html2 = records_piece(ctx, 'Where the grain dust rule stands', [bad], nm, ('done', 'skipped'), band=True)
    alt2 = ('Failure case: do not publish. An Illustrative agency rule, 99004, Grain dust limits, at 360 px: step '
            '1 never happened and steps 2 to 6 are drawn as done, so Proposed, Comments open and Comments closed all '
            'read as steps that happened. The '
            'words read “In effect since August 1. The agency published the final rule on August 1.” The agency issued it '
            'without asking for comment first, and nothing on the card says so.')
    spec(ctx, 's-11-9-failure', html2, '11.9', alt2, width=360, illustrative=True)


TRACK_KEY = ('done', 'now', 'notyet', 'skipped', 'stopped')


def used_marks(items):
    """The key holds every mark the list uses and no other (Rule 11.5's spec), in the key's own order."""
    return tuple(s for s in TRACK_KEY if any(s in b['states'] for b in items))
# Group 2's title and line: the editor's words (20261114_Round-5-Editor-Notes.md, "Words for the tracker designer")
GROUP2_TITLE = 'Records requests, agency rules, ballot measures and court cases'
GROUP2_LINE = ('A records request, a federal agency’s rule, a state ballot measure and a federal court case each move through '
               'six steps '
               'of their own, drawn with the bill tracker’s marks. Each ends in words that say how it came out, with the '
               'date.')


def s_11_10(ctx):
    """Rule 11.10, the ballot measure (DR-231, R5-7): three measures in three states, and the fault a tracker most often
    makes on election night, a count read as a result."""
    nm = names('ballot')
    html = records_piece(ctx, 'Where three ballot measures stand', BALLOTS, nm, used_marks(BALLOTS))
    alt = ('Three Illustrative state ballot measures at 360 px on Newsprint, each drawn as six numbered steps with the bill '
           'tracker’s marks, and a key of the six steps, Filed, Title and summary, Signatures, Legislature, On the ballot '
           'and Vote, and of the marks. ' + alt_rows(BALLOTS, nm))
    spec(ctx, 's-11-10-correct', html, '11.10', alt, width=360, illustrative=True)
    bad = dict(BALLOTS[0], states=['done', 'done', 'done', 'skipped', 'done', 'done'], end='Approved by voters.',
               line='Yes leads with 52 percent of the votes counted on election night, November 3.')
    html2 = records_piece(ctx, 'Where the park entry fee measure stands', [bad], nm, ('done', 'skipped'), band=True)
    alt2 = ('Failure case: do not publish. An Illustrative ballot measure, 99010, State park entry fees, at 360 px: steps '
            '1 to 3 done, step 4 never happened, and steps 5 and 6 drawn as done, so the vote reads as finished. The words '
            'read “Approved by voters. Yes leads with 52 percent of the votes counted on election night, November 3.” '
            'The count is '
            'unofficial, the state has not certified it, and nothing on the card says so.')
    spec(ctx, 's-11-10-failure', html2, '11.10', alt2, width=360, illustrative=True)


def s_11_11(ctx):
    """Rule 11.11, the court case (DR-231, R5-7): three federal civil cases in three states, and the fault of reading a
    denied petition as a Supreme Court ruling."""
    nm = names('court')
    html = records_piece(ctx, 'Where three court cases stand', COURTS, nm, used_marks(COURTS))
    alt = ('Three Illustrative federal civil cases at 360 px on Newsprint, each drawn as six numbered steps with the bill '
           'tracker’s marks, and a key of the six steps, Filed, Trial court ruling, Appeal, Appeals court ruling, Supreme '
           'Court petition and Supreme Court ruling, and of the marks. ' + alt_rows(COURTS, nm))
    spec(ctx, 's-11-11-correct', html, '11.11', alt, width=360, illustrative=True)
    bad = dict(COURTS[2], states=['done'] * 6, end=f'{AFFIRMED} by the Supreme Court on January 11.',
               line='The Supreme Court left the appeals court’s ruling in place.')
    html2 = records_piece(ctx, 'Where the highway noise walls case stands', [bad], nm, ('done',), band=True)
    alt2 = ('Failure case: do not publish. An Illustrative federal civil case, 99016, Highway noise walls, at 360 px, with '
            f'all six steps drawn as done, Supreme Court ruling among them. The words read “{AFFIRMED} by the Supreme Court '
            'on January 11. The Supreme Court left the appeals court’s ruling in place.” The Court denied the petition and '
            'never heard the case, and nothing on the card says so.')
    spec(ctx, 's-11-11-failure', html2, '11.11', alt2, width=360, illustrative=True)


def s_route_steps(ctx, sid, steps, what, alt_head):
    """A readable table of a tracker's six steps (R4-3: a reference set in live text): each step's number and name, then
    what happens and, under it, the law that sets it. Two columns, as the bill's table after Rule 11.1 sets them; under
    30rem of plate width each step stacks, its number and name over its words, so the words keep the column's width."""
    T = ctx.ty
    hair = ctx.v('oa.color.border.hairline.onNewsprint')
    t2 = ctx.v('oa.color.text.secondary.onNewsprint')
    rows = ''.join(f'<tr><th scope="row"><span class="n">{i + 1}</span> {n}</th><td><p class="wh">{m}</p>'
                   f'<p class="lw">Law: {law}</p></td></tr>' for i, (n, m, law) in enumerate(steps))
    css = (f'table{{width:100%;border-collapse:collapse;{T("bodySmall")}}}'
           f'th,td{{text-align:left;vertical-align:top;padding:12px 16px 12px 0;border-bottom:1px solid {hair}}}'
           f'td{{padding-right:0}}'
           f'thead th{{{T("label")};color:{t2};border-bottom:2px solid {ctx.v("oa.color.border.strong.onNewsprint")}}}'
           f'tbody th{{{T("ui")};font-weight:700;width:11rem;text-wrap:balance}}th .n{{display:inline-block;min-width:1.4em;'
           f'{T("h4")};font-variant-numeric:tabular-nums}}'
           f'.wh,.lw{{margin:0;text-wrap:pretty}}.lw{{margin-top:6px;{T("caption")};color:{t2}}}'
           f'@container (max-width:30rem){{thead{{display:none}}tr{{display:block;padding:12px 0;border-bottom:1px solid '
           f'{hair}}}tbody th,td{{display:block;width:auto;padding:0;border:0}}tbody th{{padding-bottom:4px}}}}'
           f'.wr{{container-type:inline-size}}')
    html = (f'<style>{css}</style><div class="wr"><table><thead><tr><th scope="col">Step</th><th scope="col">What happens, '
            f'and the law that sets it</th></tr></thead><tbody>{rows}</tbody></table></div>')
    alt = (alt_head + ' ' + ' '.join(f'{i + 1}, {n}: {m} Law: {law}.' for i, (n, m, law) in enumerate(steps)))
    return spec(ctx, sid, html, None, alt, readable=True,
                notes=f'A readable table (D2-255, R4-3) of {what}, from the research lead’s round 5 facts.')


def s_11_12(ctx):
    nm = names('request')
    later = dict(id='99009', noun='Request', kind='request', title='Prison inspection reports', states=['done'] * 6,
                 end='Upheld on appeal on July 8.',
                 line='The appeal office kept the agency’s answer. The requester took the request to federal court on '
                      'August 3.')
    items = [WAIT_REQUEST, later]
    html = records_piece(ctx, 'Two records requests, one paused and one past the agency', items, nm, ('done', 'now', 'notyet'))
    alt = ('Two Illustrative records requests at 360 px on Newsprint, with a key of the six steps and the marks. '
           + alt_rows(items, nm))
    spec(ctx, 's-11-12-correct', html, '11.12', alt, width=360, illustrative=True)
    nm7 = nm[:3] + ['Fee estimate'] + nm[3:]
    bad = dict(WAIT_REQUEST, states=['done', 'done', 'done', 'now', 'notyet', 'notyet', 'notyet'],
               line='The agency sent a fee estimate on April 2.', wait=None, checked=None)
    css = piece_css(ctx, 'n', 's') + records_css(ctx)
    fcss, band = ctx.fail_band(flush=True)
    html2 = (f'<style>{css}{fcss}</style>{band}<div class="pc"><p>{ILLUS}</p><p class="hd">Where the weather station records '
             f'request stands</p><ul class="rows">{row(bad, "s", nm7)}</ul>{key(nm7, ("done", "now", "notyet"))}</div>')
    alt2 = ('Failure case: do not publish. An Illustrative records request, 99007, Weather station repair records, at 360 '
            'px, drawn as seven numbered steps: the fee estimate has become step 4, between Searching and Reviewing. The '
            'words read “Step 4 of 7: Fee estimate. The agency sent a fee estimate on April 2.”, and the key lists seven '
            'steps.')
    spec(ctx, 's-11-12-failure', html2, '11.12', alt2, width=360, illustrative=True)


def s_opener(ctx):
    """Chapter 11's opener (Gate 2 fix pass, call 3, CD-S1): the six steps every bill follows, drawn with the tracker's
    marks at true size, each with its name and its state in words. A state bill at its hearing, step 2, where the
    public can take part, so the take-part disc is the opener's one working red, and step 6 is Governor, who signs a
    state bill (Rule 11.1). Across the column from 36rem, with
    each name under its step; upright below, as a bill's own page turns them (Rule 11.6). A picture with an alt."""
    st = ['done', 'take', 'notyet', 'notyet', 'notyet', 'notyet']
    nm = names('state')
    lis = []
    for i, s_ in enumerate(st):
        seg = 'end' if i == 5 else ('on' if st[i + 1] != 'notyet' else 'off')
        cur = ' cur' if s_ in ('now', 'take') else ''
        lis.append(f'<li class="{seg}{cur}">{sample(s_, 26, num=i + 1)}<span class="t"><span class="n">{nm[i]}</span>'
                   f'<span class="s">{STATE_WORD[s_]}</span></span></li>')
    T = ctx.ty
    css = (f':scope{{{mark_vars(ctx, "n", follow=True)}}}' + MARK_CSS +
           '.op{container-type:inline-size;color:var(--txt)}:where(.op p){margin:0}'
           '.ot{list-style:none;margin:0;padding:0}'
           '.ot li{position:relative;display:grid;grid-template-columns:40px minmax(0,1fr);column-gap:8px;'
           'padding-bottom:12px;min-height:52px}'
           '.ot li::after{content:"";position:absolute;left:19px;width:2px;top:33px;bottom:-7px;background:var(--ink)}'
           '.ot li.off::after{left:19.5px;width:1px;background:var(--sub)}.ot li.end::after{display:none}'
           '.t{display:flex;flex-direction:column;padding-top:9px;min-width:0}'
           f'.n{{{T("ui")};font-weight:600}}.cur .n{{font-weight:700}}'
           f'.s{{{T("label")};color:var(--txt2)}}.cur .s{{color:var(--txt)}}'
           f'.ln{{margin-top:12px;{T("caption")};color:var(--txt2)}}'
           '@container (min-width:36rem){.ot{display:grid;grid-template-columns:repeat(6,minmax(0,1fr))}'
           '.ot li{display:flex;flex-direction:column;align-items:center;padding:0 4px;min-height:0;text-align:center}'
           '.ot li::after{left:calc(50% + 13px);width:calc(100% - 26px);top:19px;bottom:auto;height:2px}'
           '.ot li.off::after{left:calc(50% + 13px);width:calc(100% - 26px);top:19.5px;height:1px}'
           '.t{align-items:center;padding-top:4px}.ln{margin-top:20px}}')
    html = (f'<style>{css}</style><div class="op"><ol class="ot">{"".join(lis)}</ol>'
            '<p class="ln">A tracker follows every bill through the same six steps. Here a state bill is at its hearing, '
            'where the public can take part.</p></div>')
    alt = ('The six steps a tracker follows every bill through, drawn as a tracker draws them, each with its name and its '
           'state in words, for a state bill: 1 Filed, done, a filled circle; 2 Hearing, a heavy ring with a small red '
           'disc at its upper right, which says you can take part now; 3 Committee vote, 4 First chamber, 5 Second '
           'chamber and 6 Governor, not yet, fine rings. A line joins them, heavy as far as the bill has come and fine '
           'ahead. A line under it says a tracker follows every bill through the same six steps, and this state bill is '
           'at its hearing, where the public can take part.')
    return spec(ctx, 's-11-opener', html, None, alt,
                notes='Chapter 11’s opener (Gate 2 fix pass, call 3, CD-S1): Rules 11.1 and 11.2’s marks at true size '
                      'in one tracker, flowing with the column. The take-part disc is its one working red.')


# ------------------------------------------------------------------------------------------------ chapter
def build(ctx):
    s_opener(ctx)
    s_steps(ctx)
    s_marks_table(ctx)
    s_11_1(ctx)
    rr, rh = s_11_2(ctx)
    s_11_3(ctx)
    s_11_4(ctx)
    lists = s_11_5(ctx)
    pages = s_11_6(ctx)
    s_11_7(ctx)
    s_11_8(ctx)
    s_11_9(ctx)
    s_11_10(ctx)
    s_11_11(ctx)
    s_route_steps(ctx, 's-11-ballot-steps', BALLOT_STEPS, 'a ballot measure’s six steps',
                  'The six steps of a state ballot measure, a citizen initiative, with what happens at each and where the '
                  'law sets it in the four states we read.')
    s_route_steps(ctx, 's-11-court-steps', COURT_STEPS, 'a federal civil case’s six steps',
                  'The six steps of a federal civil case, with what happens at each and where the law sets it.')
    s_11_12(ctx)

    r = ctx.ratio
    ink_n = r('oa.color.graphic.essential.onNewsprint', 'oa.color.surface.newsprint')
    sub_n = r('oa.color.graphic.subtle.onNewsprint', 'oa.color.surface.newsprint')
    ink_c = r('oa.color.graphic.essential.onCharcoal', 'oa.color.surface.charcoal')
    sub_c = r('oa.color.graphic.subtle.onCharcoal', 'oa.color.surface.charcoal')
    t2_n = r('oa.color.text.secondary.onNewsprint', 'oa.color.surface.newsprint')
    t2_c = r('oa.color.text.secondary.onCharcoal', 'oa.color.surface.charcoal')
    red_n = r('oa.color.palette.pillarRed', 'oa.color.surface.newsprint')
    red_c = r('oa.color.palette.pillarRed', 'oa.color.surface.charcoal')
    key_n = r('oa.component.button.ask.keyline.onNewsprint', 'oa.color.surface.newsprint')
    ask = r('oa.component.button.ask.label.onNewsprint', 'oa.component.button.ask.fill.onNewsprint')
    touch = int(ctx.T.px('oa.size.target.touch'))
    minimum = int(ctx.T.px('oa.size.target.minimum'))
    ctx.fig('target sizes', f'{touch} and {minimum} px', 'oa.size.target.touch and oa.size.target.minimum in tokens.json')

    rules = [
        {
            'id': '11.1', 'title': 'Follow every bill through six numbered steps with plain names.',
            'rule': ['A tracker follows a bill through six steps, numbered 1 to 6: Filed, Hearing, Committee vote, First '
                     'chamber, Second chamber, and a sixth named for whoever signs the bill, Governor on a state bill and '
                     'President on a federal one. A chamber is one house of a legislature, such as the House or the Senate, '
                     'and the first chamber is the one where the bill was filed. Every tracker prints the number and the name '
                     'together, as in “Step 2 of 6: Hearing”, for the step the bill is at now.',
                     'Six steps fold some procedure together, such as a second reading or a conference committee, where '
                     'members of both chambers settle one text. A bill’s own page gives those dates in the note under the '
                     'step they belong to. Every state keeps all six steps. Nebraska’s Legislature has one chamber, so a '
                     'Nebraska bill keeps step 5 under a slash, and its card says “Nebraska has one chamber” beside the '
                     'marks.'],
            'tokens': ['oa.type.dataLabel', 'oa.type.bodySmall'],
            'why': {'text': ['A number gives a reader words to say, “step 2 of 6”, with no key to learn, and it reads the '
                             'same on a phone and in gray print. Plain names let a newcomer say what happens at each step. '
                             'The hearing keeps a step of its own because it is where a committee takes testimony on the '
                             'bill, from the public in many state legislatures and from the witnesses it invites in '
                             'Congress. Naming step 6 for the person who signs keeps a bill that waits for a signature from '
                             'reading as law.'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-1-correct',
                        'caption': 'Three bills at 360 px, each at step 6 with its own key. The state bill’s sixth step is '
                                   'Governor and the federal bill’s is President. The Nebraska bill keeps all six steps, '
                                   'with step 5 under a slash and the reason beside it.'},
            'failure': {'specimen': 's-11-1-failure',
                        'caption': '<strong>Fails Rule 11.1.</strong> The steps take the clerk’s names. A newcomer cannot '
                                   'say what Engrossed or Enrolled means, so the tracker needs a glossary before it tells '
                                   'anyone where the bill stands.'},
            'specs': [
                {'label': 'Steps', 'value': '1 Filed, 2 Hearing, 3 Committee vote, 4 First chamber, 5 Second chamber, 6 '
                                            'the signer'},
                {'label': 'Step 6', 'value': 'Governor on a state bill; President on a federal bill'},
                {'label': 'Nebraska', 'value': 'Six steps; step 5 under a slash, with “Nebraska has one chamber” beside '
                                               'the marks'},
                {'label': 'Status words', 'value': '“Step 2 of 6: Hearing.”, in bold, for the step the bill is at now, '
                                                   'then one plain sentence', 'token': 'oa.type.bodySmall'},
                {'label': 'Step names under the circles', 'value': 'In a list column 552 px wide or more, Inter 600 '
                                                                   'at 13 px, the current step in bold',
                 'token': 'oa.type.dataLabel'},
            ],
            'related': ['01', '18'],
            'builders': ['Write the status words from the data, never from the drawing: the step number, its name for '
                         'this bill’s route and one sentence on what happens next. Store step 6 as the signer, so a state '
                         'bill prints Governor and a federal bill prints President.',
                         'Number an invented bill past the numbers legislatures assign: a federal bill from H.R. 99001 up, '
                         'state bills from one count that starts at H.99001 and S.99002, and a Nebraska bill with '
                         'Nebraska’s LB, for '
                         'Legislative Bill, from LB 99008 up. Label each one Illustrative. A cropped plate then cannot put '
                         'our status words on a real bill.'],
        },
        {
            'id': '11.2', 'title': 'Draw each step’s state as a shape, and say it in words.',
            'rule': ['Each step shows its state by its shape, and the words beside the tracker say the same thing. Done '
                     'steps fill in, the step a bill is at now takes a heavy ring, and steps ahead keep a fine one. A step '
                     'that never happened, such as a hearing the committee skipped, keeps its number under a slash, so the '
                     'count still runs to six. When a bill stops, its line ends on a filled square at that step.'],
            'tokens': ['oa.color.graphic.essential.onNewsprint', 'oa.color.graphic.subtle.onNewsprint',
                       'oa.color.text.secondary.onNewsprint', 'oa.color.graphic.essential.onCharcoal',
                       'oa.color.graphic.subtle.onCharcoal'],
            'why': {'text': ['A shape holds up in gray print, in bright sun and for the many readers who cannot tell red '
                             'from green. The words carry the state to a screen reader and to anyone unsure of a mark. '
                             'Every mark a bill has reached draws in the surface’s ink, Charcoal on Newsprint and '
                             'Newsprint on Charcoal, as do the slash and the line up to the current step. The rings '
                             'ahead, the ring under a slash and the line after the current step draw lighter, in Stone '
                             'on Newsprint and Dim Newsprint on Charcoal, so the steps still to come stand back. Only '
                             'the take-part disc is red.'],
                    'basis': 'WCAG 2.2 SC 1.4.1 and 1.4.11; design judgment'},
            'correct': {'specimen': 's-11-2-correct',
                        'caption': 'The six states, each drawn on step 4 at true size. Each one changes the '
                                   'shape, so the set reads in grayscale.'},
            'failure': {'specimen': 's-11-2-failure',
                        'caption': f'<strong>Fails Rule 11.2.</strong> Six identical circles tell their states by hue alone. '
                                   f'In grayscale, the done steps in Verdigris and the steps ahead in Stone print as grays '
                                   f'{rr} to 1 apart, and no word says where the bill stands.'},
            'specs': [
                {'label': 'Done', 'value': 'A filled circle, its number in the surface color'},
                {'label': 'Now', 'value': 'A ring with a 3 px line, its number in bold', 'token': 'oa.component.mark.ring.now'},
                {'label': 'Not yet', 'value': 'A ring with a 1.5 px line in Stone, its number in Inter 600 in the secondary text color',
                 'token': 'oa.component.mark.ring.ahead'},
                {'label': 'Never happened', 'value': 'The Not yet ring under a 2 px slash in ink, 4 px longer than the '
                                                     'circle is wide', 'token': 'oa.component.mark.slash'},
                {'label': 'Halo', 'value': 'A 4 px stroke in the surface color under the number of a step that never '
                                           'happened, which shows 2 px around it', 'token': 'oa.component.mark.halo'},
                {'label': 'Stopped', 'value': 'A filled square 2 px narrower than the circle, in its place; the line ends there'},
                {'label': 'Marks on Newsprint', 'value': f'Charcoal {ink_n} to 1, Stone {sub_n} to 1',
                 'token': 'oa.color.graphic.subtle.onNewsprint'},
                {'label': 'Marks on Charcoal', 'value': f'Newsprint {ink_c} to 1, Dim Newsprint {sub_c} to 1',
                 'token': 'oa.color.graphic.subtle.onCharcoal'},
                {'label': 'Numbers ahead', 'value': f'Deep Stone {t2_n} to 1 on Newsprint, Dim Newsprint {t2_c} to 1 on '
                                                    f'Charcoal', 'token': 'oa.color.text.secondary.onNewsprint'},
            ],
            'related': ['05', '17'],
            'builders': ['Draw each tracker as one SVG with <code>aria-hidden="true"</code>, and give screen readers an '
                         'ordered list of the six steps beside it, each with its state in words, such as “Step 2, '
                         'Hearing: never happened.” Hide that list visually and keep it in the reading order.',
                         'Tag each mark <code>data-icon="S-now"</code> (or <code>S-done</code>, <code>S-take-part</code>, '
                         '<code>S-not-yet</code>, <code>S-never-happened</code>, <code>S-stopped</code>) with '
                         '<code>data-icon-family="status"</code>, so the shared checks find it.',
                         'A hearing on the bill’s subject held before the bill was filed does not fill step 2; the step’s '
                         'note names it.',
                         'Draw each mark from the table after this rule, Drawing the marks, which gives its size at every '
                         'circle size, its line, its color token and where its parts sit.'],
        },
        {
            'id': '11.3', 'title': 'Say in words when a bill becomes law or stops.',
            'rule': ['Step 6 keeps the signer’s name while a bill waits, so a bill there reads “Step 6 of 6: Governor”. '
                     'Once it becomes law, all six steps fill and the words say “Became law on” with the date, then when it '
                     'takes effect, as in “Became law on April 2. It takes effect July 1.” A bill can become law by '
                     'signature, by a vote to override a veto, or without a signature where the constitution allows it. '
                     'When it was not signed, the words say how, as in “Became law on March 18, over the governor’s veto.”',
                     'A bill that stops ends its line on a square at the step where it stopped, and the words give the '
                     'date and the reason. A veto that stands stops a bill at step 6.'],
            'why': {'text': ['A reader who sees the last step filled can take the bill for law, so only the words can '
                             'say when the signature came and when the law applies. The date it takes effect is the one '
                             'most readers act on.'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-3-correct',
                        'caption': 'Three ends at 360 px. H.99003 became law when it was signed, and S.99006 over a veto; '
                                   'the words of each say how and when. S.99005 stopped at step 6 when a veto stood, and its '
                                   'line ends on the square.'},
            'failure': {'specimen': 's-11-3-failure',
                        'caption': '<strong>Fails Rule 11.3.</strong> The sixth step is named Law, so a bill that still '
                                   'waits for the governor reads “Step 6 of 6: Law.” A reader may stop following it '
                                   'before a veto.'},
            'specs': [
                {'label': 'Waiting to be signed', 'value': '“Step 6 of 6: Governor.” or “Step 6 of 6: President.”'},
                {'label': 'Signed', 'value': 'All six steps filled; “Became law on April 2. It takes effect July 1.”'},
                {'label': 'Over a veto', 'value': 'All six steps filled; “Became law on March 18, over the governor’s veto.”'},
                {'label': 'Without a signature', 'value': 'All six steps filled; “Became law on May 4, without the governor’s '
                                                          'signature.”, where the constitution allows it'},
                {'label': 'Stopped', 'value': 'A square at the last step reached; “Stopped at step 3 of 6: Committee '
                                              'vote.” with the date and the reason'},
                {'label': 'A veto that stands', 'value': 'Stopped at step 6'},
            ],
            'related': ['02', '13'],
            'builders': ['Keep two dates in a bill’s record once it is signed: the day it was signed and the day it takes '
                         'effect, written in the past tense once that day has passed. Print “Became law on” '
                         'only from the signed date.'],
        },
        {
            'id': '11.4', 'title': 'Mark the one way to take part in red, on its own shape.',
            'rule': ['When the public can act on a bill before a date, the step it is at takes the take-part mark: a '
                     'small red disc at the upper right of its ring, with a 1 px Charcoal keyline inside the disc’s edge. '
                     'The words “You can take part now” sit beside it, with the deadline and the way to act. It is the '
                     'view’s one working red (Rule 05.3), and it can sit on any step where the public can take part, '
                     'such as a hearing in the second chamber at step 5. Every other state stays in the surface’s ink.'],
            'tokens': ['oa.color.palette.pillarRed', 'oa.component.button.ask.keyline.onNewsprint',
                       'oa.component.mark.takePart.keyline', 'oa.component.mark.takePart.cut'],
            'why': {'text': ['Red catches the eye first, so it goes to the one thing a reader can do. The disc changes '
                             'the ring’s outline, so the mark still reads in gray print, and the words say what to do for '
                             f'anyone who cannot see red. On Newsprint, Pillar Red measures {red_n} to 1, under the 3 to 1 a '
                             f'mark needs, and the keyline gives it an edge at {key_n} to 1.'],
                    'basis': 'Rule 05.3; WCAG 2.2 SC 1.4.1 and 1.4.11'},
            'correct': {'specimen': 's-11-4-correct',
                        'caption': 'A story card at 360 px. The House committee holds its own hearing at step 5, so the '
                                   'take-part mark sits there, beside its words and the link to act.'},
            'failure': {'specimen': 's-11-4-failure',
                        'caption': '<strong>Fails Rules 11.4 and 05.3.</strong> Red also fills the steps the bill has '
                                   'passed, so it does two jobs and the one way to take part no longer stands out.'},
            'specs': [
                {'label': 'Take-part mark', 'value': 'An 11 px Pillar Red disc at the upper right of the Now ring, a '
                                                     '1 px Charcoal keyline inside its edge, 1.5 px of the surface around it',
                 'token': 'oa.component.mark.takePart.disc'},
                {'label': 'Contrast', 'value': f'Pillar Red {red_n} to 1 on Newsprint with the keyline at {key_n}; '
                                               f'{red_c} to 1 on Charcoal', 'token': 'oa.component.button.ask.keyline.onNewsprint'},
                {'label': 'Words', 'value': '“You can take part now.” in bold, then the deadline and how to act'},
                {'label': 'In a list, or on a card with this mark', 'value': 'A text link at least 44 px tall; the red '
                                                                            'button waits for the bill’s own page',
                 'token': 'oa.size.target.touch'},
                {'label': 'On a card without this mark', 'value': 'The card may end on the red ask, as the pillar cards in '
                                                                  'chapter 01 do'},
                {'label': 'Red jobs in a view', 'value': 'One: take part now. Every take-part mark and the ask button '
                                                         'share it. An error in the same view takes the red first (Rule 11.18)'},
            ],
            'related': ['05', '18'],
            'builders': ['Mark the disc and the ask button with <code>data-red="working"</code> and '
                         '<code>data-red-job="take part now"</code>, so the shared check counts one red job. The words '
                         'carry the meaning, so the disc stays hidden from screen readers.'],
        },
        {
            'id': '11.5', 'title': 'Use numbered steps in lists and on story cards.',
            'rule': ['In a list of bills and on a story card, the tracker runs across the page: six numbered circles on '
                     'one line, solid as far as the bill has come and fine after it. The bill’s number and name lead each '
                     'row, and its status words follow the marks. In a column narrower than 552 px, as on a phone, the '
                     'first circle starts on the text edge and the step names move into a key after the list. In a wider '
                     'column, each step takes a sixth of the row and its name sits under its circle.'],
            'tokens': ['oa.component.mark.line.reached', 'oa.component.mark.line.ahead', 'oa.type.dataLabel'],
            'why': {'text': ['A list asks a reader to compare bills at a glance, and six numbered steps fit across a '
                             '360 px phone with room for the words. The numbers also keep the tracker apart from the '
                             'lockmark, the small grid of lines and nodes that marks our pages and codes nothing '
                             '(chapter 08).'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-5-correct',
                        'caption': 'Five bills at 360 px on Newsprint, among them one where you can take part, one waiting for the '
                                   'governor, one whose hearing never happened and one stopped by a veto.'},
            'failure': {'specimen': 's-11-5-failure',
                        'caption': '<strong>Fails Rule 11.5.</strong> Dots on a line carry no numbers or names, so a reader '
                                   'counts dots to find the step, and a row of nodes on a line comes close to the '
                                   'lockmark’s drawing.'},
            'specs': [
                {'label': 'Circles', 'value': '26 px in a phone list, 30 px in a wide list, 24 px on a story card'},
                {'label': 'Line', 'value': '2 px in the surface’s ink as far as the record has come, through any step that '
                                           'never happened; 1 px in Stone after the current step',
                 'token': 'oa.component.mark.line.reached'},
                {'label': 'Spacing', 'value': 'Phone list and card: the first circle on the text edge and each next one '
                                              '60 px on, center to center, so six fit a 328 px row. Wide list: one '
                                              'sixth of a 552 px row to each step, 92 px'},
                {'label': 'Step names', 'value': 'Under the circles in a column 552 px wide or more; in the key below '
                                                 'that',
                 'token': 'oa.type.dataLabel'},
                {'label': 'Key', 'value': 'After the last bill: the six steps on phones, and every mark the list uses'},
            ],
            'related': ['07', '08'],
            'builders': ['Mark up the list as a <code>&lt;ul&gt;</code> of bills, each holding its hidden step list from '
                         'Rule 11.2. Switch to the wide form with a container query on the list’s own width, '
                         '<code>@container (min-width: 34.5rem)</code>, so a list in a narrow column keeps its key at any '
                         'window size. When a tracker updates in place, announce the new status words in a status line, '
                         'as chapter 18 sets out.'],
        },
        {
            'id': '11.6', 'title': 'Turn the same steps upright on a bill’s own page.',
            'rule': ['A bill’s own page runs the six steps down the page, with the marks a list uses. Each step gives its '
                     'name, its state in words and a note with its dates. Under the step where the public can act, a box '
                     'holds the deadline and the page’s one red button, the ask. Where the page has room, a key after '
                     'the steps says what each one means.'],
            'tokens': ['oa.component.button.ask.fill.onNewsprint', 'oa.component.button.ask.label.onNewsprint', 'oa.type.ask'],
            'why': {'text': ['A bill’s page has room for the dates and notes a list leaves out, and a reader who knows the '
                             'marks from a list knows them here. The ask sits under the step it belongs to, where the '
                             'reader learns why the date matters.'],
                    'basis': 'Design judgment, approved by our founder and editor in November 2026'},
            'correct': {'specimen': 's-11-6-correct',
                        'caption': 'H.99001’s page at 360 px. Step 2 holds the way to take part, and step 5’s note says the '
                                   'Senate’s committee often holds a hearing of its own.'},
            'failure': {'specimen': 's-11-6-failure',
                        'caption': '<strong>Fails Rule 11.6.</strong> A generic stepper from a component library draws checks and boxes with no '
                                   'numbers, so a reader who learned the steps in a list has to learn a second set.'},
            'specs': [
                {'label': 'Circles', 'value': '28 px with 14 px numbers'},
                {'label': 'Line', 'value': '2 px down the page as far as the bill has come, 1 px after it'},
                {'label': 'Each step', 'value': 'Name in Inter 600 at 17 px, the state in label type, a note at 15 px'},
                {'label': 'Ask button', 'value': f'Inter 700 at 19 px, White on Pillar Red at {ask} to 1, 48 px tall',
                 'token': 'oa.type.ask'},
                {'label': 'Key of meanings', 'value': 'After the steps, in a column 600 px wide or more'},
            ],
            'related': ['18', '20'],
            'builders': ['Mark up the steps as an <code>&lt;ol&gt;</code>, one item for each step, with the state in its '
                         'text. Make the ask a link to the way to take part, styled as the ask button.'],
        },
        {
            'id': '11.7', 'title': 'Size the marks for reading, and the targets for a thumb.',
            'rule': ['Draw the circles at 24 px on a story card, 26 px in a phone list, 28 px on a bill’s page and '
                     '30 px in a wide list. Numbers sit at 13 px in circles under 28 px and at 14 px from 28 px.',
                     f'Every link and button in a tracker, and every control that carries a utility icon, stands at least '
                     f'{touch} px tall, and the ask button 48 px. A plain list of text links, such as a list of contents, may '
                     f'stand shorter, as long as each link keeps the {minimum} px that WCAG asks for through its spacing.'],
            'tokens': ['oa.size.target.touch', 'oa.size.target.minimum'],
            'why': {'text': ['Numbers at 13 px keep the type floor of Rule 06.3 inside the mark. A target 44 px tall '
                             f'clears the {minimum} px minimum in WCAG 2.2 with room for a thumb, and matches our touch '
                             'target token.'],
                    'basis': 'WCAG 2.2 SC 2.5.8; Rule 06.3'},
            'correct': {'specimen': 's-11-7-correct',
                        'caption': 'The four circle sizes at true size, and the two targets with their heights marked.'},
            'failure': {'specimen': 's-11-7-failure',
                        'caption': '<strong>Fails Rules 11.7 and 06.3.</strong> Circles at 16 px force numbers down to 9 px, '
                                   'and the link stands 20 px tall, under the 24 px minimum.'},
            'specs': [
                {'label': 'Circles', 'value': '24, 26, 28 and 30 px, by place'},
                {'label': 'Numbers', 'value': 'Inter 700 at 13 px, or 14 px in circles of 28 px and up; Inter 600 on a step '
                                              'not yet reached or never happened; tabular figures'},
                {'label': 'Links and buttons in a tracker, and controls with a utility icon', 'value': f'At least {touch} px '
                                                                                                     f'tall',
                 'token': 'oa.size.target.touch'},
                {'label': 'A plain list of text links', 'value': f'{minimum} by {minimum} px, through spacing',
                 'token': 'oa.size.target.minimum'},
                {'label': 'Ask button', 'value': '48 px tall'},
            ],
            'related': ['06', '19'],
            'builders': [f'Set <code>min-height: var(--oa-size-target-touch)</code> on every link in a tracker, and give a '
                         f'link that sits inline at least {minimum} px of space around it.'],
        },
    ]


    # ---------------- group 2: records requests and agency rules (DR-140, D2-526 to D2-529)
    rules += [
        {
            'id': '11.8', 'title': 'Follow a records request through six steps, and end it in plain words.',
            'rule': ['A records request asks a government agency to release documents it holds. These steps and end '
                     'words follow the federal Freedom of Information Act and the Justice Department’s categories; a '
                     'request to a state or local agency follows that state’s law. The tracker uses the bill '
                     'tracker’s marks for six steps of its own: Requested, Acknowledged, Searching, Reviewing, Answered and '
                     'Appeal. Step 6 counts only when the requester appeals, so a request that was never appealed keeps '
                     'step 6 under a slash once the time to appeal has passed.',
                     'The words say how the agency answered, with the date: Granted, Partly granted, Denied, or Closed with '
                     'no records released. A request the requester stopped reads “Withdrawn by the requester”, and its line '
                     'ends on a square at the step where it stopped. An appeal ends in words too: Upheld, Partly reversed, '
                     'Reversed and sent back, or Closed for other reasons.'],
            'why': {'text': ['A requester can wait weeks for an answer, and the steps tell them where the request sits. '
                             'The marks are the bill tracker’s, so a reader learns them once. The end words follow the '
                             'Justice Department’s own categories in plain words, with one change: the department counts '
                             'a withdrawn request among its denials, and a reader who saw “denied” would think the agency '
                             'had refused.'],
                    'basis': '5 U.S.C. 552 and FOIA.gov; design judgment'},
            'correct': {'specimen': 's-11-8-correct',
                        'caption': 'Three requests at 360 px. One is under review, one was partly granted and never '
                                   'appealed, so step 6 keeps its slash, and one was withdrawn at step 3.'},
            'failure': {'specimen': 's-11-8-failure',
                        'caption': '<strong>Fails Rule 11.8.</strong> The tracker prints the government’s category for a '
                                   'request the requester withdrew, so “Full denial” tells a reader the agency refused.'},
            'specs': [
                {'label': 'Steps', 'value': '1 Requested, 2 Acknowledged, 3 Searching, 4 Reviewing, 5 Answered, 6 Appeal'},
                {'label': 'Step 6', 'value': 'A fine ring while an appeal can still be filed; under a slash once the time '
                                             'has passed with none', 'token': 'oa.component.mark.slash'},
                {'label': 'The answer, in words', 'value': 'Granted; Partly granted; Denied; Closed, no records released; '
                                                           'Withdrawn by the requester'},
                {'label': 'An appeal, in words', 'value': 'Upheld; Partly reversed; Reversed and sent back; Closed for '
                                                          'other reasons'},
                {'label': 'Marks and sizes', 'value': 'The bill tracker’s, from Rules 11.2 and 11.7'},
            ],
            'related': ['13', '18'],
            'builders': ['Store each request’s step and its end words as data, and print the end words with their date: '
                         '“Partly granted on March 3.” A state’s records law sets its own deadlines, so check that state’s '
                         'statute before you print one. Number an invented request from 99001 up, name no agency, and '
                         'label it Illustrative.'],
        },
        {
            'id': '11.9', 'title': 'Follow an agency rule through six steps.',
            'rule': ['A federal agency writes a rule in six steps: Early notice, Proposed, Comments open, Comments closed, '
                     'Final rule and In effect. Step 1 is optional, so a rule that had no early notice keeps step 1 under a '
                     'slash. While comments are open, step 3 takes the take-part mark from Rule 11.4, with the deadline and '
                     'how to send a comment.',
                     'A rule the agency issued without asking for comment first keeps steps 2 to 4 under slashes, and its '
                     'words say so: “Issued without advance comment.” An interim final rule is one such rule, and it '
                     'takes comments only after it takes effect. A rule that ends early '
                     'says how in words, with the date: Withdrawn by the agency, Struck by Congress, or Set aside by a '
                     'court. Once a rule takes effect, all six steps fill, as a bill’s do once it becomes law.'],
            'tokens': ['oa.component.mark.takePart.disc'],
            'why': {'text': ['Sending a comment is the main way the law gives the public to take part in a federal rule, '
                             'so the open '
                             'comment period carries the view’s working red, as a hearing does on a bill. The slashes keep '
                             'a rule that skipped comment from reading as one the public had a say in before it took '
                             'effect.'],
                    'basis': '5 U.S.C. 553 and RegInfo.gov; Rule 11.4'},
            'correct': {'specimen': 's-11-9-correct',
                        'caption': 'Three agency rules at 360 px. Comments are open on one, so step 3 takes the take-part '
                                   'mark; one took effect without advance comment, with slashes on steps 1 to 4; and one '
                                   'was withdrawn after comments closed.'},
            'failure': {'specimen': 's-11-9-failure',
                        'caption': '<strong>Fails Rule 11.9.</strong> Steps 2 to 4 are filled for a rule issued without '
                                   'advance comment, so the tracker tells a reader the public had its say before the rule '
                                   'took effect.'},
            'specs': [
                {'label': 'Steps', 'value': '1 Early notice, 2 Proposed, 3 Comments open, 4 Comments closed, 5 Final '
                                            'rule, 6 In effect'},
                {'label': 'Step 1', 'value': 'Optional; under a slash when the agency gave no early notice'},
                {'label': 'Take part', 'value': 'On step 3 while comments are open: the take-part mark, the deadline and '
                                                '“How to send a comment”', 'token': 'oa.component.mark.takePart.disc'},
                {'label': 'Without advance comment', 'value': 'Steps 2 to 4 under slashes, and “Issued without advance '
                                                              'comment.”'},
                {'label': 'The end, in words', 'value': 'In effect since; Withdrawn by the agency; Struck by Congress; '
                                                        'Set aside by a court, with the part it set aside'},
                {'label': 'Takes effect', 'value': 'Usually 30 days or more after the final rule is published, and 60 days '
                                                   'or more for a major rule'},
            ],
            'related': ['13', '18'],
            'builders': ['Store the comment deadline with the rule, and take the take-part mark off the day comments close. '
                         'Number an invented rule from 99001 up, name no agency, and label it Illustrative.'],
        },
        # Round 5 (DR-231, DR-274, DR-275, R5-7): the research lead's facts, item 1; the editor's words pass follows
        {
            'id': '11.10', 'title': 'Follow a ballot measure through six steps, and wait for the certified count.',
            'rule': ['A ballot measure here is a citizen initiative: voters propose a law or an amendment to their state’s '
                     'constitution by petition, and the voters decide it. These steps follow the constitutions of '
                     'Massachusetts, California, Ohio and Michigan and California’s election office; each state sets its '
                     'own deadlines and counts. The tracker uses the bill tracker’s marks for six steps of its own: Filed, '
                     'Title and summary, Signatures, Legislature, On the ballot and Vote. Step 4 counts only where the '
                     'Legislature votes on the measure first, so a measure that goes straight to the ballot keeps step 4 '
                     'under a slash.',
                     'Until the state certifies the count, a measure at step 6 stays current, and its words say so: '
                     '“Step 6 of 6: Vote. The count is unofficial until the state certifies it, set for November 25.” Once '
                     'the count is certified, the words say Approved by voters or Rejected by voters, with the date of the '
                     'vote and the date it was certified, then when an approved measure takes effect. A measure that ends '
                     'before step 6 ends its line on a square at the last step it reached, with its words and the date: '
                     'Not certified by the attorney general, Withdrawn by its sponsors, Too few valid signatures to '
                     'qualify, or Removed from the ballot by a court. A measure the Legislature passes keeps steps 5 and 6 '
                     'under slashes, and its words give the date: “Passed by the Legislature on May 2.”'],
            'tokens': ['oa.component.mark.slash'],
            'why': {'text': ['A count on election night is unofficial and keeps moving as ballots are counted, and a '
                             'measure becomes law only on the certified result. Words that wait for certification keep a '
                             'reader from treating a lead as law. The slash on step 4 keeps every measure counting to six '
                             'and still says that no legislature voted on a direct initiative.'],
                    'basis': 'Massachusetts Constitution, Amendment Articles XLVIII and LXXXI; California Constitution, '
                             'Article II, and Elections Code; Ohio and Michigan Constitutions, Article II'},
            'correct': {'specimen': 's-11-10-correct',
                        'caption': 'Three measures at 360 px. One went straight to the ballot, so step 4 keeps its slash, '
                                   'and its count is not yet certified; voters approved one, and the state certified it; '
                                   'and one stopped at step 3 with too few valid signatures.'},
            'failure': {'specimen': 's-11-10-failure',
                        'caption': '<strong>Fails Rule 11.10.</strong> The tracker fills step 6 and prints “Approved by '
                                   'voters” on '
                                   'election night, while the count is unofficial, so a reader takes the measure for law '
                                   'before the state certifies the result.'},
            'specs': [
                {'label': 'Steps', 'value': '1 Filed, 2 Title and summary, 3 Signatures, 4 Legislature, 5 On the ballot, '
                                            '6 Vote'},
                {'label': 'Step 4', 'value': 'The Legislature’s vote where the initiative is indirect, with a second round '
                                             'of signatures in words under it; under a slash where it is direct',
                 'token': 'oa.component.mark.slash'},
                {'label': 'Before the count is certified', 'value': '“Step 6 of 6: Vote.” with the date the state has '
                                                                    'set to certify; never Approved or Rejected'},
                {'label': 'The end, in words', 'value': 'Approved by voters or Rejected by voters, with the date of the '
                                                        'vote and the date it was certified, then when it takes effect; '
                                                        'Not approved by voters where most said yes but a second test '
                                                        'failed, with a sentence that names it'},
                {'label': 'Ended before step 6', 'value': 'A square at the last step reached, with its words: Not '
                                                          'certified by the attorney general; Withdrawn by its sponsors; '
                                                          'Too few valid signatures to qualify; Removed from the ballot by '
                                                          'a court'},
                {'label': 'Passed by the Legislature', 'value': 'Steps 5 and 6 under slashes, and “Passed by the '
                                                                'Legislature on” with its date',
                 'token': 'oa.component.mark.slash'},
                {'label': 'Sent to the voters by the Legislature', 'value': 'Steps 1 to 3 under slashes, and step 4 done, '
                                                                            'with those words and the date'},
                {'label': 'Marks and sizes', 'value': 'The bill tracker’s, from Rules 11.2 and 11.7'},
            ],
            'related': ['13', '15'],
            'builders': ['Store each measure’s steps, whether its initiative is direct or indirect, and the dates its state '
                         'publishes, and print Approved or Rejected only from the certified result. Number an invented '
                         'measure '
                         'from 99001 up, name no state, and label it Illustrative.'],
        },
        {
            'id': '11.11', 'title': 'Follow a court case through six steps, and end a denied petition at step 5.',
            'rule': ['A court case here is a federal civil case: one side, the plaintiff, sues another, the defendant, '
                     'under federal law, and the case can climb from the trial court through a court of appeals to the '
                     'Supreme Court. These steps follow '
                     'Title 28 of the U.S. Code, the federal rules of civil and appellate procedure and the Supreme '
                     'Court’s own rules; a criminal case, or a case in a state’s courts, runs on other rules. The tracker '
                     'uses the bill tracker’s marks for six steps of its own: Filed, Trial court ruling, Appeal, Appeals '
                     'court ruling, Supreme Court petition and Supreme Court ruling. A step the law gives this case no '
                     'room for keeps its number under a slash, as when a district court of three judges grants or denies '
                     'an injunction and the law sends the appeal straight to the Supreme Court.',
                     'The words say how each court ruled, with the court and the date. A trial court’s judgment reads '
                     'Decided for the plaintiff or Decided for the defendant, with “without a trial” where the court '
                     'decided on the record alone. A higher court’s ruling reads as the court enters it: ' + AFFIRMED + ', '
                     'which leaves the ruling below in place; Reversed; Vacated, which cancels the ruling below; or '
                     'Modified; joined to “and sent back” when the court returns the case. The marks never move backward, '
                     'so a case sent back says so in a sentence '
                     'after the end words. A case that ends before step 6 ends its line on a square at the last step it '
                     'reached, with its words: Settled by the parties, Withdrawn by the plaintiff, Dismissed by the court, '
                     'Appeal withdrawn, or Petition denied by the Supreme Court, which ends it at step 5 and leaves the '
                     'appeals court’s ruling standing.'],
            'tokens': ['oa.component.mark.slash'],
            'why': {'text': ['In the Supreme Court’s own words, review is “not a matter of right, but of judicial '
                             'discretion”, so a denied petition says only that the Court chose not to hear the case. A '
                             'tracker that filled step 6 would tell a reader the Court had ruled on a case it never '
                             'heard. Naming each court’s ruling as its own step, and the court in the end words, keeps '
                             'clear which court spoke last.'],
                    'basis': '28 U.S.C. 1253, 1291, 2101, 2106 and 2107; Rules of the Supreme Court, Rules 10, 13 and '
                             '16; Neil v. Biggers (1972)'},
            'correct': {'specimen': 's-11-11-correct',
                        'caption': 'Three cases at 360 px. One waits on the appeals court; the Supreme Court reversed one '
                                   'and sent it back, said in words while all six steps stay filled; and the Court denied '
                                   'one petition, so that line ends on a square at step 5.'},
            'failure': {'specimen': 's-11-11-failure',
                        'caption': '<strong>Fails Rule 11.11.</strong> The Supreme Court denied the petition, and the '
                                   'tracker fills step 6 and prints “' + AFFIRMED + '”, so a reader takes a refusal to hear the '
                                   'case for a ruling on it.'},
            'specs': [
                {'label': 'Steps', 'value': '1 Filed, 2 Trial court ruling, 3 Appeal, 4 Appeals court ruling, 5 Supreme '
                                            'Court petition, 6 Supreme Court ruling'},
                {'label': 'A trial court’s ruling', 'value': 'Decided for the plaintiff; Decided for the defendant; with '
                                                            '“without a trial” where it applies'},
                {'label': 'A higher court’s ruling', 'value': AFFIRMED + '; Reversed; Vacated; Modified; each with the '
                                                              'court, as in “' + AFFIRMED + ' by the appeals court”, and '
                                                              '“and sent back” where the court returns the case'},
                {'label': 'Ended before step 6', 'value': 'A square at the last step reached, with its words: Settled by '
                                                          'the parties; Withdrawn by the plaintiff; Dismissed by the court; '
                                                          'Appeal withdrawn; Appeal dismissed by the court; Petition '
                                                          'denied by the Supreme Court, on step 5'},
                {'label': 'Never appealed', 'value': 'A square on step 2, with “No appeal was filed in the 30 days the law '
                                                     'allows.”, or 60 days where the United States is a party'},
                {'label': 'A tie in the Supreme Court', 'value': AFFIRMED + ' by an equally divided Court, which is a tie '
                                                                 'vote, and “The lower court’s ruling stands.”'},
                {'label': 'Straight to the Supreme Court', 'value': 'Steps 3 and 4 under slashes, where a district court '
                                                                    'of three judges grants or denies an injunction and the '
                                                                    'law sends the appeal straight there',
                 'token': 'oa.component.mark.slash'},
                {'label': 'Inside a step, in words', 'value': 'An order on an injunction and its appeal, under step 2; a '
                                                              'rehearing by the full appeals court, under step 4'},
                {'label': 'Marks and sizes', 'value': 'The bill tracker’s, from Rules 11.2 and 11.7'},
            ],
            'related': ['13', '15'],
            'builders': ['Store each court’s ruling as data, with its date and the verb the court used, and print that '
                         'verb. Number an invented case from 99001 up, name no party or court, and label it '
                         'Illustrative.'],
        },
        {
            'id': '11.12', 'title': 'Say a wait or a later step in words, and keep the count at six.',
            'rule': ['A wait inside a step shows as words under the step it falls in and never adds a mark, so every '
                     'tracker in this group still counts to six. A records request may wait on the requester’s answer, a '
                     'fee estimate or an extension of up to 10 working days, and a draft agency rule may wait on review '
                     'at the White House. A ballot measure may need a second round of signatures after the Legislature '
                     'declines to act, and a court case may pause while a court of appeals hears an appeal of an order '
                     'on an injunction. Anything after the end words, such as a lawsuit over a request or a rule, a case '
                     'sent back to the trial court, or a legislature’s repeal of a measure the voters approved, follows '
                     'them as a sentence with its date.',
                     'A status taken from the deciding body’s own record needs no mark: an agency’s tracking service, the '
                     'Federal Register for a rule, the state election office’s notice for a ballot measure, or the '
                     'court’s docket for a case. A status we piece together ourselves, such as a wait we learn of from an '
                     'agency’s letter, carries a warning with the date we checked it, drawn as Rule 11.17 draws every '
                     'warning: “Warning: Checked April 20. The agency may have acted since.”'],
            'tokens': ['oa.color.state.warning.mark.onNewsprint'],
            'why': {'text': ['The law lets an agency stop its 20 working days while it waits on the requester, once for '
                             'more information and again to settle fees, and add up to 10 working days in unusual '
                             'circumstances, so each wait belongs inside the step it falls in. A count that changed from '
                             'one item to the next would stop readers from comparing them. The check date tells a reader '
                             'how old the status is before they rely on it.'],
                    'basis': '5 U.S.C. 552(a)(6); Executive Order 12866; 28 U.S.C. 1292(a)(1); design judgment'},
            'correct': {'specimen': 's-11-12-correct',
                        'caption': 'Two requests at 360 px. One waits on the requester at step 3, in words, with the date '
                                   'we last checked it beside the warning mark. The other was upheld on appeal and then '
                                   'taken to court, said in a sentence after its end words.'},
            'failure': {'specimen': 's-11-12-failure',
                        'caption': '<strong>Fails Rule 11.12.</strong> The fee estimate becomes a seventh step, so this '
                                   'request reads “Step 4 of 7” while every other request counts to six.'},
            'specs': [
                {'label': 'Waits, in words', 'value': '“Waiting on you”, a fee estimate or an extension on a request; a '
                                                      'second round of signatures on a ballot measure; an appeal of an '
                                                      'injunction on a court case; each under the step it falls in, with '
                                                      'its date'},
                {'label': 'A proposed rule that sits', 'value': '“No action since” and the date, under its step'},
                {'label': 'After the end', 'value': 'Mediation, a lawsuit, a case sent back or a repeal, in a sentence '
                                                    'after the end words'},
                {'label': 'Check date', 'value': 'For a status we piece together ourselves: the warning mark at 24 px, in '
                                                 'ink, then “Warning: Checked” and the date, beside a 4 px bar in ink',
                 'token': 'oa.color.state.warning.mark.onNewsprint'},
                {'label': 'Marks', 'value': 'Six, always'},
            ],
            'related': ['13', '17'],
            'builders': ['Keep a wait as a field on its step, with the dates it began and ended, so the words can say how '
                         'long the count of working days stopped. Store where each status came from, so a status we '
                         'piece together ourselves prints its check date.'],
        },
    ]

    # ---------------- groups 3 and 4: utility icons and the three marks (apply_systems_ch11_ui.py)
    group_titles = [('Trackers', [(r['id'], r['title']) for r in rules[:7]]),
                    (GROUP2_TITLE, [(r['id'], r['title']) for r in rules[7:12]]),
                    ('Utility icons', [('11.13', None), ('11.14', None), ('11.15', None), ('11.16', None)]),
                    ('Error, success and warning', [('11.17', None), ('11.18', None)])]
    ui_rules, ui_extras, ui_groups = UI.build_ui(ctx, sys.modules[__name__], [])
    ui_titles = {r['id']: r['title'] for r in ui_rules}
    group_titles = [(g, [(i, t or ui_titles[i]) for i, t in ids]) for g, ids in group_titles]
    ctx.specs.pop('s-11-menu')
    UI.s_menu(ctx, sys.modules[__name__], group_titles)
    rules += ui_rules

    ch = {
        'number': CH, 'anchor': 'icons', 'title': 'Status and utility icons', 'part': 'Symbols and graphics',
        'instruction': 'Give each record state or interface action a glyph and a word that read without color.',
        'opener': 's-11-opener',
        'intro': [
            'A glyph here is a small drawn mark, and each one carries its meaning twice, in its shape and in the word '
            'beside it. A reader who sees no color, or prints the page in gray, gets the same meaning as everyone else.',
            'Trackers come first: they show how far a bill has come in six numbered steps, and the same marks then '
            'follow a records request, an agency rule, a ballot measure and a court case. After them come the utility '
            'icons, which sit beside the word for '
            'an action on a page, and the three marks that give an error, a success or a warning its shape.',
        ],
        'groups': [{'before_rule': '11.1', 'number': 1, 'title': 'Trackers',
                    'line': 'A tracker shows where a bill stands in six numbered steps, with each step’s state drawn as a '
                            'shape and said in words.'},
                   {'before_rule': '11.8', 'number': 2, 'title': GROUP2_TITLE, 'line': GROUP2_LINE}] + ui_groups,
        'rules': rules,
        'extras': [
            {'after_rule': '11.1', 'specimen': 's-11-steps', 'label': 'The six steps',
             'caption': 'What happens at each step. Step 6 takes the name of whoever signs the bill.'},
            {'after_rule': '11.2', 'specimen': 's-11-marks-drawn', 'label': 'Drawing the marks',
             'caption': 'Each mark at every circle size, with its line, its color token and where its parts sit. Read '
                        '&lt;surface&gt; as “newsprint” or “charcoal”, the ground the tracker sits on.'},
            {'after_rule': '11.5', 'specimen': lists[('c', 'l')], 'label': 'Numbered steps in a 600 px column on Charcoal',
             'caption': 'The wide form, as on a tablet or in a desktop article column, on Charcoal, with two of the bills. '
                        'Each step’s name sits under its circle, the current step’s name is bold, and the marks turn to '
                        'Newsprint and Dim Newsprint while the take-part disc keeps its red.'},
            # Round 5: each new tracker's six steps as a reference set in live text (R4-3), after its rule
            {'after_rule': '11.10', 'specimen': 's-11-ballot-steps', 'label': 'The six steps of a ballot measure',
             'caption': 'What happens at each step of a citizen initiative, and where the law sets it in the four states '
                        'we read. Each state sets its own deadlines and signature counts.'},
            {'after_rule': '11.11', 'specimen': 's-11-court-steps', 'label': 'The six steps of a court case',
             'caption': 'What happens at each step of a federal civil case, and where the law sets it.'},
        ] + ui_extras,
        'related_chapters': [
            {'chapter': '05', 'reason': 'One working red in each view, and states that read without color.'},
            {'chapter': '06', 'reason': 'The 13 px floor and tabular figures.'},
            {'chapter': '08', 'reason': 'The lockmark, which keeps its fixed places and codes nothing.'},
            {'chapter': '17', 'reason': 'Loading, empty and error states for a live tracker.'},
            {'chapter': '18', 'reason': 'How a live tracker announces a change.'},
            {'chapter': '19', 'reason': 'Checking a tracker against WCAG 2.2 AA.'},
            {'chapter': '10', 'reason': 'Topic and atlas symbols, which name subjects and never stand for an action.'},
        ],
        'sources': [
            # BE-S8: a period for every source, "as in force on" after a statute and "no page date" after an undated page
            'Source: Nebraska Legislature, “Lawmaking in Nebraska”, via nebraskalegislature.gov, no page date, retrieved '
            'November 9, 2026. Nebraska’s one-chamber route and its steps, behind Rule 11.1.',
            # BE-S4, CD-S8: the research lead's line (20261109_Stage-B-Research-Notes.md, section 4), with BE-S8's page
            # dates and its closing clause recast without the "examples, not a count" turn (chapter 02, W09)
            'Sources: Nebraska Legislature, “Tips on Testifying at a Committee Hearing”, no page date; Washington State '
            'Legislature, “How to Testify in Committee”, 2023; Minnesota Legislature, “May I testify at a committee '
            'hearing?”, reviewed February 20, 2026; Utah Legislature, “How to Testify In A Committee”, no page date; '
            'Texas Legislature Online, FAQ 27, no page date; five states, all retrieved November 9, 2026. Each '
            'legislature sets its own rules on sign-up, time limits and which bills get a hearing, and we read these '
            'five as examples and made no national count. Testimony from the public at a state committee hearing, '
            'behind Rule 11.1.',
            'Sources: the Freedom of Information Act, 5 U.S.C. 552, via the Legal Information Institute, Cornell Law '
            'School, as in force on November 9, 2026; and FOIA.gov, “Frequently Asked Questions”, run by the Justice '
            'Department’s Office of Information Policy, no page date; both retrieved November 9, 2026. The steps, the '
            '20 working days and the waits in them, behind Rules 11.8 and 11.12.',
            # BE-S1: the sections that hold the categories, and the report's own coverage; ED 4e's form for "retrieved"
            'Source: Office of Information Policy, U.S. Department of Justice, “Fiscal Year 2024 Annual Freedom of '
            'Information Act Report”, March 6, 2025, sections V.B.(1) and VI.B, fiscal year 2024, the Justice '
            'Department and its components, retrieved November 9, 2026. The categories behind the end words in Rule '
            '11.8.',
            'Sources: rulemaking, 5 U.S.C. 553, Congressional review, 5 U.S.C. 801, and judicial review, 5 U.S.C. 706, via '
            'the Legal Information Institute, Cornell Law School, as in force on November 9, 2026; and RegInfo.gov, '
            '“Frequently Asked Questions”, the Office of Information and Regulatory Affairs, no page date; all retrieved '
            'November 9, 2026. The steps of a federal rule, its comment period, when it takes effect and how it can '
            'end, behind Rule 11.9.',
            # Round 5: the research lead's facts, item 1 (20261114_Round-5-Research-Notes.md), each source read on
            # November 14, 2026; the full quotes are in the workflow sources file, "Round 5"
            'Sources: the Massachusetts Constitution, Amendment Articles XLVIII and LXXXI, via malegislature.gov; the Ohio '
            'Constitution, Article II, Section 1b, and Article XVI, Section 1, via codes.ohio.gov; the Michigan '
            'Constitution of 1963, Article II, Section 9, via legislature.mi.gov; each as in force on November 14, 2026; '
            'and California Secretary of State, “Statewide Initiative Guide”, revised January 2026; all retrieved '
            'November 14, 2026. We read these four states as examples of a citizen initiative, and each state sets its '
            'own steps, deadlines and signature counts. The steps of a ballot measure and how one can end, behind Rule '
            '11.10.',
            # the data lead's three source points (batch 1, 02:27), settled by the research lead (02:30, its line):
            # 1253 and 2284 for the three-judge court, Neil v. Biggers for the tie, every section the step table cites
            'Sources: 28 U.S.C. 1253, 1254, 1291, 1292, 1331, 2101, 2106, 2107 and 2284, via govinfo.gov, the 2024 '
            'edition of the U.S. Code; the Federal Rules of Civil Procedure, as amended to December 1, 2025, and the '
            'Federal Rules of Appellate Procedure, as amended to December 1, 2024, via uscourts.gov; the Rules of the '
            'Supreme Court of the United States, adopted February 17, 2026, effective March 16, 2026, via '
            'supremecourt.gov; and Neil v. Biggers, 409 U.S. 188 (1972), on a tie in the Supreme Court, via '
            'govinfo.gov; all retrieved November 14, 2026. The steps of a federal civil case, the time to appeal, the '
            'courts’ rulings and a tie in the Supreme Court, behind Rule 11.11, and the appeal of an injunction, behind '
            'Rule 11.12.',
            # Rule 11.12's draft rule at the White House (the editor's words, D3-1879), from the workflow sources file
            'Source: Executive Order 12866 of September 30, 1993, section 6(b)(2), the National Archives’ copy, '
            'retrieved November 12, 2026; later orders amended parts of it, and we did not trace them. The review of a '
            'draft rule at the White House, behind Rule 11.12.',
        ],
    }
    return ch


def nb_walk(o, key=None):
    if isinstance(o, str):
        return o if key in ('specimen', 'token', 'id', 'anchor', 'number', 'before_rule', 'chapter', 'after_rule', 'opener') else nb(o)
    if isinstance(o, list):
        return [nb_walk(x, key) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in ('tokens', 'related') else nb_walk(v, k)) for k, v in o.items()}
    return o


def main():
    T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
    ctx = B.Ctx(T, {}, 'final')
    ch = nb_walk(build(ctx))
    B.check_chapter(ch)
    used = set()
    for r in ch['rules']:
        for k in ('correct', 'failure'):
            used.add(r[k]['specimen'])
    used |= {x['specimen'] for x in ch['extras']}
    if ch.get('opener'):
        used.add(ch['opener'])
    missing, unused = used - set(ctx.specs), set(ctx.specs) - used
    if missing or unused:
        raise SystemExit(f'specimens missing {sorted(missing)} unused {sorted(unused)}')
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for old in OUT_SP.glob('s-11-*.html'):
        if old.stem not in ctx.specs:
            old.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    man = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    man = {k: v for k, v in man.items() if str(v.get('chapter')) != CH}
    man.update({sid: s['meta'] for sid, s in ctx.specs.items()})
    MANIFEST.write_text(json.dumps(dict(sorted(man.items())), indent=1, ensure_ascii=False) + '\n')
    FIG_OUT.write_text(json.dumps({
        'about': 'Every figure chapter 11 prints, with how it was measured. Contrast is WCAG 2.x relative luminance on '
                 'the token values in tokens.json.',
        'built': '2026-11-07',
        'token_set_version': T.data.get('$extensions', {}).get('org.oathandaction', {}).get('tokenSetVersion'),
        'figures': dict(sorted(ctx.figures.items())),
        'tokens_cited': sorted(T.used),
    }, indent=1, ensure_ascii=False) + '\n')
    print(f'chapter 11: {len(ch["rules"])} rules, {len(ctx.specs)} specimens, {len(ctx.figures)} figures')


if __name__ == '__main__':
    main()
