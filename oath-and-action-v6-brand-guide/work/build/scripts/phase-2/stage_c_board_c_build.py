"""Build board C (November 11, 2026): the one decision round 2 raised, a standing rule on examples (D2-1555), the
creative director's scores before and after the fix pass, what round 2 found and fixed, the calls Dustin may overrule,
what he answered this chat and what comes next (DR-220, D2-1691, brief: work/handoffs/phase-2/20261111_Board-C-Brief.md).

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_board_c_build.py [--strict] [--answered "<Dustin's words>"]
        [--answered-on "November 12, 2026"] [--publish DIR] [--guide PAGE] [--out PATH] [--scratch DIR]

Reads, on every run (every score, figure, quoted sentence and code on the board comes from these files; the script
holds only the board's own words):
    work/build/guide/chapters/*.json                         rule text the board quotes, and every rule it links
    the frozen chapters page, read from git at the commit D2-1531 names, checked against its SHA-256
    work/build/tokens/tokens.css and tokens.json             contrast figures, the release, its count and names
    work/extract/atlas-v7-data.json                          reform and loop titles, flags and grades
    work/build/guide/code/c-18-loop-stepper.html             Loop R1's grade line
    work/build/scripts/phase-2/guide_build.py                the closing token block's words
    work/handoffs/phase-2/20261111_Stage-C-Round-2-*.md and *.json, 20261111_WCAG22-Criteria-Text.json
                                                             the reports, fix notes, scores and rescore
    work/ledger/*_Decision-Log.md, *_Open-Questions.md      every code the board prints must exist
Writes:
    work/boards/phase-2/stage-c/board-c/20261111_Board-C.html            the board, one file
    work/boards/phase-2/stage-c/board-c/20261111_Board-C-Content.json    every string, figure and quote, with its source
    <scratch>/board-c/check-copy/20261111_Board-C.html                    a copy for dataviz_check.js with captures
    <publish>/20261111_Board-C.html, <publish>/files.json                 the publish copy, no document skeleton

--answered prints the decision as answered, with Dustin's words and the date (--answered-on, default the build date).
--strict exits 1 on any warning: a quoted sentence the files no longer hold, a code missing from the log, a studio code
in a sentence, a bare reform code, a flagged word, an en dash, or a rule link with no rule behind it. An em dash stops
the build.
"""
import argparse
import datetime
import difflib
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261111'
BOARD_DIR = ROOT / 'work/boards/phase-2/stage-c/board-c'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/49b1040f-34e8-55e0-97c3-93e08c6dbc2c/scratchpad')
HANDOFFS = ROOT / 'work/handoffs/phase-2'
CHAPTERS = ROOT / 'work/build/guide/chapters'
FROZEN_PATH = 'work/boards/phase-2/stage-a/20261106_Stage-A-Chapters.html'
SRC = {
    'scores': HANDOFFS / f'{DATE}_Stage-C-Round-2-CD-Scores.json',
    'rescores': HANDOFFS / f'{DATE}_Stage-C-Round-2-CD-Rescores.json',
    'be': HANDOFFS / f'{DATE}_Stage-C-Round-2-Red-Team-Brand-Evidence.md',
    'pp': HANDOFFS / f'{DATE}_Stage-C-Round-2-Red-Team-Plain-Production.md',
    'ca': HANDOFFS / f'{DATE}_Stage-C-Round-2-Red-Team-Craft-Access.md',
    'eng': HANDOFFS / f'{DATE}_Stage-C-Round-2-Engineer-Fix-Notes.md',
    'comp': HANDOFFS / f'{DATE}_Stage-C-Round-2-Components-Fix-Notes.md',
    'a11y': HANDOFFS / f'{DATE}_Stage-C-Round-2-Accessibility-Fix-Notes.md',
    'wcag': HANDOFFS / f'{DATE}_WCAG22-Criteria-Text.json',
    'tokens_css': ROOT / 'work/build/tokens/tokens.css',
    'tokens_json': ROOT / 'work/build/tokens/tokens.json',
    'atlas': ROOT / 'work/extract/atlas-v7-data.json',
    'loop_set': ROOT / 'work/build/guide/code/c-18-loop-stepper.html',
    'guide_build': ROOT / 'work/build/scripts/phase-2/guide_build.py',
}
DEF_OUT = BOARD_DIR / f'{DATE}_Board-C.html'
DEF_PUBLISH = SCRATCH / 'publish-board-c'
DEF_SCRATCH = SCRATCH / 'board-c'
DEF_GUIDE = SCRATCH / 'final/guide.html'
CHAPTERS_URL = 'https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF'
CHAPTERS_VERSION = 7
TITLE = 'Board C Decision'
TAGLINE = 'A country that answers to its people.'
LIMIT = 16_000_000
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat',
           'basically', 'very', 'incredibly', 'utilize', 'utilizes']
CRITERIA = [('craft', 'Craft'), ('clarity', 'Clarity'), ('brand_fidelity', 'Brand fidelity'), ('usefulness', 'Usefulness'),
            ('evidence_honesty', 'Evidence honesty'), ('accessibility', 'Accessibility')]
WARN, NOTES, QUOTES = [], [], {}
# Copy edits to strings the board takes from other owners' files (the creative director's names and reasons): exact
# text, replacement, and a check that the replacement's claim is on file. Each must match once, or the build warns.
OVERRIDES = [
    {'find': 'Chapter 12, Rule 12.4 as wired (DR-216)', 'put': 'Chapter 12, Rule 12.4 as rewritten', 'evidence': None},
    {'find': "; 19.5's chart is still a bare line sketch (R2).",
     'put': "; the short second pass then gave 19.5's chart its title, its lines' names, its years and a source line.",
     'evidence': ('a11y', r'\*\*R2, `s-19-5-correct` and `s-19-5-failure`\.\*\* The chart now has a title')},
    {'find': ' The broken-out stage reaches left while its label rule stays in the column (R1).',
     'put': ' The short second pass then carried the plate’s label row and rule out with the stage.',
     'evidence': ('eng', r'\*\*R1, the token table\'s head\.\*\* From 80em, when the table breaks out over the rail, its label row and rule go out with it')},
]
for o in OVERRIDES:
    o['n'] = 0

# ------------------------------------------------------------------------------------------------ the board's words
# Every word the studio writes for this board. Facts the board quotes or measures are read from the sources at build
# time and filled in where a {name} stands. Codes in "codes" fields print in small type beside an item, for the record.
W = {
    'kicker': 'Edition 06 · Stage C · Board C',
    'for_line': 'For Dustin Cathcart · {built_date}',
    'title': 'One decision is yours',
    'title_answered': 'You answered the one decision',
    'deck': [
        'Board C closes round 2 of stage C, in which three red teams and the creative director read chapters 17, 18, 19 and 26 and the parts of 01 to 11 that changed, and the studio fixed what they found.',
        'Round 2 raised one question that is yours, a standing rule on examples, and this page sets it beside the scores, what changed and the calls you may overrule.',
    ],
    'deck_answered_2': 'Round 2 raised one question that was yours, a standing rule on examples, and this page records your answer beside the scores, what changed and the calls you may overrule.',
    'pages_h': 'The two pages of board C',
    'pages': [
        ('The chapters page', 'chapters', 'version {chapters_version}, with chapters {chapter_list} and the identity proofs as the fix pass left them. Each rule number on this board opens it at that rule.'),
        ('This board', None, 'the one decision, the scores, what round 2 found and fixed, the calls you may overrule and what comes next.'),
    ],
    'reply_h': 'A reply can be this short',
    'sample_reply': 'Yes to the standing rule on examples.',
    'copy_reply': 'Copy the reply',
    'answer_h': 'Your answer, {answered_on}',
    'toc_h': 'On this board',
    'decision': {
        'label': 'The one decision',
        'label_answered': 'The one decision, answered',
        'title': 'A standing rule on examples',
        'codes': 'D2-1555 · D2-1546 · D2-958 · D2-278 · DR-99 · DR-100',
        'lede': [
            'Our systems atlas flags two of its {n_reforms} reforms as tied to your own work: Reform R-01, “{r01}”, and Reform R-02, “{r02}”. The guide prints no disclosure, so the studio keeps its examples off both.',
            'Round 2 found chapter 18’s examples back on Reform R-01 and on the safe-seat and primary mechanism it targets, across {n_plates} plates. The studio has now moved examples off that subject three times, one case at a time: chapter 01’s failure row in Rule 01.12, then Rules 10.8 and 11.16 at stage B, and now chapter 18, whose samples moved to the housing loop and Reform R-30. The brand and evidence team asks for one rule that holds everywhere.',
        ],
        'rule_cap': 'The standing rule, as the brand and evidence team wrote it',
        'drift_h': 'Where it drifted: the example in Rule 18.24',
        'before_h': 'Before, version {frozen_version}',
        'after_h': 'After, version {chapters_version}',
        'before_src': 'Rule 18.24 on the frozen page the reviewers read',
        'after_src': 'Rule 18.24 in chapter 18 as the fix pass left it',
        'before_cap': 'Loop R10 is “{r10}”, and Reform R-01, a flagged reform, sits on that loop.',
        'after_cap': 'Loop R1 is “{r1}”, and Reform R-04 is “{r04}”. Neither reform sits on Loop R1, and Reform R-04 carries no flag.',
        'marks_note': 'Struck words show what the fix pass took out, and bold words show what it put in their place.',
        'rec_h': 'Recommendation',
        'rec': ['Yes. With one standing rule, a maker checks each new example against the atlas’s flag before drawing it, so the next chapter needs no round of moves.'],
        'cost_h': 'What it costs',
        'cost': ['Nothing on the page changes today, since the fix pass already moved chapter 18’s samples. From now on, makers check every new example, sample and failure plate against the atlas’s flag. The filter bar and the search keep Reforms R-01 to R-12 in the atlas’s own order, since a list in that order is no example, and real atlas content keeps its grade and source.'],
        'approve_h': 'What you approve by name',
        'approve': 'The standing rule on examples.',
        'answered_h': 'Your answer, {answered_on}',
    },
    'scores': {
        'title': 'The creative director’s scores',
        'intro_ready': 'The creative director scored chapters 17, 18, 19 and 26, the changed parts of chapters 01 to 11 and Rule 12.4 as rewritten, on the six criteria of our rubric, from 1 to 5. An item is ready at 4 or more on every one, and after the fix pass every item is.',
        'intro_not_ready': 'The creative director scored chapters 17, 18, 19 and 26, the changed parts of chapters 01 to 11 and Rule 12.4 as rewritten, on the six criteria of our rubric, from 1 to 5. An item is ready at 4 or more on every one.',
        'caption': 'Scores from 1 to 5, round 2 and after the fix pass',
        'legend': 'In each cell, round 2’s score in small type, then the rescore after the fix pass, both on {score_dates}. A box marks a score under 4.',
        'scroll_hint': 'The table scrolls sideways, with each item’s name held at the left.',
        'item_h': 'Chapter or part',
        'ready_h': 'Ready',
        'new_item': 'First scored after the fix pass',
        'moved_h': 'What moved, with the creative director’s reason',
    },
    'found': {
        'title': 'What round 2 found and fixed',
        'intro': 'The reviewers read the frozen page you saw as version {frozen_version}. These are the faults a reader or a builder would notice, each with its fix, now in version {chapters_version}.',
        'groups': [
            ('What a reader sees', [
                ('Red stays off Prussian', None,
                 'In the dark theme a form field sat on Prussian, so an error’s red bar touched it, the red and blue pair Rule 05.3 rules out. A field on Charcoal now takes Charcoal inside its light edge, where the bar measures {red_on_charcoal} to 1. The guide check now fails any red pixel beside Prussian, in both themes, after it presses Send in every form.'),
                ('Our marks rest whole', None,
                 'The players for the wordmark and the lockmark rested on their first frames, so a reader who never pressed Play met split words and empty squares. Each now rests on its master (Rule 17.3).'),
                ('Rule 12.4, rewritten', None,
                 'As you approved on November 11, the hinge arcs retire. An open area stays plain, or carries the large crop of our ampersand or a watermark.'),
            ]),
            ('What a builder uses', [
                ('A production test', 'Simulated',
                 'One reviewer played a panel of three in turn. As its developer, they built an event sign-up card from chapters 18 and 26 and tokens.css alone, then switched it to dark mode, and the guide failed them twice. The chapters said to put a surface class on the body, and that class keeps one ground in both themes, so the card stayed light. The token block each chapter offered as a second route missed {n_missing} properties its code reads, so the form drew in a fallback font with a send button under {target_px} px. Rules 26.3 and 26.6 now leave the body with no surface class, and tokens.css is the one route. {pp_label}'),
                ('A token table you can scan', None,
                 'Its {n_groups} groups stay closed until a reader opens one, so the table stands {h_after} px tall at 1440 px, where it ran {h_before} px. From a plate width of 40rem each group is a real table (Rule 26.7).'),
                ('Code panels break their lines', None,
                 'Each declaration and each long attribute takes its own line, so the longest line fell from {line_before} characters to {line_after}, and a panel shows about {panel_lines} lines before it scrolls.'),
                ('Token release {version}', None,
                 'The error bar’s token takes the name {bar_name}, and the old name works until {alias_leaves}. Every description a reader sees, across all {n_tokens} tokens, is in plain words.'),
            ]),
            ('What the evidence says', [
                ('W3C’s words in W3C’s order', None,
                 'Four criteria printed their parts out of order, so success criterion 3.3.7 read as if filling in a field for the reader were an exception. All {n_criteria} now print from a stored copy of the Recommendation fetched from w3.org, and the build stops if the page differs from it (Rule 19.1).'),
                ('Met means a rule says so', None,
                 'A criterion now reads Met only where a rule states what it asks. Met fell from {met_before} to {met_after}; {inpart_after} are met in part, {gaps_after} are gaps and {unused_after} cover things no product does yet.'),
                ('Loop R1 states its grade', None,
                 'The guide’s main example of a loop about money in politics read as a finding. Its heading now names the loop in quotation marks, with a line under it (Rule 18.22): “{grade_line}”'),
                ('Examples left the subject of your work', None,
                 'Chapter 18’s samples now come from the housing loop, Loop R8, and Reform R-30, with their real grades and a dated source. The decision above asks whether this becomes a standing rule.'),
            ]),
        ],
    },
    'calls': {
        'title': 'Calls the studio made that you may overrule',
        'intro': 'The studio made these five calls inside the plan you approved. Each stands unless you say otherwise.',
        'items': [
            ('Fields on Charcoal take Charcoal', 'D2-1544 · D2-1469 · D2-1562',
             'An earlier call let an error’s red bar touch a Prussian field in the dark theme, because the pair measures {red_on_prussian} to 1, over the 3 to 1 a mark needs. The fix pass withdrew that call, since Rule 05.3 gives this reason: “{q_05_3}” The field’s ground moved to Charcoal, so a field shows by its light edge (Rule 18.17). The selected band on Charcoal stays Prussian, and the guide check keeps red away from it.'),
            ('The ask stands on its own row', 'D2-1545 · D2-1592',
             'A primary button’s hover turns Prussian, and in Rule 18.1’s plate it sat {hover_gap} px from the red ask. The hover stays as our token plan sets it, and the ask now has a row of its own. Rule 18.1 says: “{q_18_1}”'),
            ('A mark’s player rests on the mark', 'D2-1548 · D2-1563',
             'Rule 17.3 now says: “{q_17_3}” A player of a state or a mechanism still rests on its first frame, where the change starts.'),
            ('tokens.css is the one route', 'D2-1549 · D2-1639 · D2-266',
             'The engineer chose one route over a complete copy of each chapter’s tokens. A copy with both themes would hold most of tokens.css, and one without them would teach a product with no dark mode. Each chapter’s block stays for reading, and the words above it say: “{q_block}” Rule 26.5 starts every page from tokens.css.'),
            ('Closed groups for the token table', 'D2-1557 · D2-1641',
             'Each of the {n_groups} groups stays closed until a reader opens it or a search finds a match in it, and a list of the groups heads the table. Under a plate width of 40rem, as on a phone, the rows stay cards (Rule 26.7). An open table with the rail out of the way would still run roughly {open_px} px, as the craft team measured.'),
        ],
    },
    'answered': {
        'title': 'What you answered this chat',
        'intro': 'You gave these answers on November 11, each as the studio proposed.',
        'lines': [
            ('DR-219', 'Round 2’s production test had a simulated developer build an event sign-up card from chapters 18 and 26 and tokens.css alone, then switch it to dark mode.'),
            ('DR-220', 'The chapters page comes back at its address as version {chapters_version} with a note on what changed, and a decisions board follows only when round 2 raises a call that is yours. It raised one, so this board exists.'),
            ('DR-221', 'At Gate 2 the creative director reads all 16 chapters together and scores each one, to catch drift between chapters built at different stages.'),
            ('DR-222', 'From this container census.gov, fec.gov, api.congress.gov and data.gov answer, while bls.gov and Missouri’s secretary of state turn automated visitors away. The Phase 3 proposal plans on downloading public data.'),
        ],
    },
    'next': {
        'title': 'What comes next',
        'lines': [
            ('DR-221', 'The Gate 2 preview, in a new chat. It holds the whole guide as one file with its fonts embedded and the creative director’s read of all 16 chapters together, then the Gate 2 report with the proposal for Phase 3.'),
        ],
        'carried_h': 'Still open',
        'carried': [
            ('D2-1532 · D2-1118', 'Missouri’s certified count. The studio reads it when the preview is built; if the state has not certified by then, the plate keeps “unofficial” and the read moves to Phase 5’s assembly.'),
            ('Q-04', 'Whether a photography commission or licensed documentary images come before launch. Until then the guide uses placeholders and its full photography rules.'),
            ('Q-12', 'Whether a trademark attorney clears OATH & ACTION, the monogram and a standalone ampersand before launch. The guide flags the need and assumes no filing.'),
        ],
    },
    'foot': 'Built {built_date} at {built_time} UTC from the chapter files, the frozen page, the tokens, the atlas, round 2’s reports and fix notes, the creative director’s scores and the decision log.',
}


# ------------------------------------------------------------------------------------------------ helpers
class BoardError(Exception):
    pass


def warn(msg):
    WARN.append(msg)
    print('warning', msg)


def note(msg):
    NOTES.append(msg)
    print('note', msg)


def need(cond, msg):
    if not cond:
        raise BoardError(msg)


def show(p):
    p = pathlib.Path(p).resolve()
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def load_json(p, what):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except (OSError, ValueError) as e:
        raise BoardError(f'{what} ({p}): {e}')


def read(key):
    p = SRC[key]
    need(p.exists(), f'{show(p)} is missing')
    return p.read_text()


def find(key, pattern, what, flags=0, text=None):
    """One regex match in a source file; a miss is a warning, since the board then lacks a fact it prints."""
    t = text if text is not None else read(key)
    m = re.search(pattern, t, flags)
    if not m:
        warn(f'{what}: no longer found in {show(SRC[key]) if key in SRC else key}')
    return m


def quote(key, s, where):
    """Record a sentence the board quotes, so the page check can find it word for word."""
    QUOTES[key] = {'text': s, 'source': where}
    return s


def squash(s):
    return re.sub(r'\s+', ' ', s).strip()


def norm(s):
    return squash(str(s).replace('\u00a0', ' ').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"'))


def ov(s):
    if not isinstance(s, str):
        return s
    for o in OVERRIDES:
        if o['find'] in s:
            o['n'] += s.count(o['find'])
            s = s.replace(o['find'], o['put'])
    return s


def copy(s):
    """Curly quotes and apostrophes, and no-break spaces before units (H07 and the guide's own setting)."""
    s = str(s).replace('‑', '-')
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    return re.sub(r'(\d) (px|percent)\b', '\\1\u00a0\\2', s)


def attr(s):
    return html.escape(str(s), quote=True)


RULES = {}          # '18.24' -> rule dict
GUIDE_IDS = None    # ids on a built chapters page, when one is given
LINKED = set()


def rule_href(rid):
    anchor = 'rule-' + rid.replace('.', '-')
    if rid not in RULES:
        warn(f'a link to Rule {rid}, which no chapter file holds')
    if GUIDE_IDS is not None and anchor not in GUIDE_IDS:
        warn(f'Rule {rid}: #{anchor} is not on the built page given with --guide')
    LINKED.add(anchor)
    return f'{CHAPTERS_URL}#{anchor}'


def anchor_href(anchor):
    a = anchor.lstrip('#')
    if GUIDE_IDS is not None and a not in GUIDE_IDS:
        warn(f'#{a} is not on the built page given with --guide')
    LINKED.add(a)
    return f'{CHAPTERS_URL}#{a}'


def link_rules(t):
    """Every rule number in escaped text links to the chapters page; the link text or its name says which rule."""
    def one(m):
        word, nums = m.group(1), m.group(2)
        parts = re.split(r'(\d{2}\.\d{1,2})', nums)
        out, first = '', True
        for p in parts:
            if re.fullmatch(r'\d{2}\.\d{1,2}', p):
                if first:
                    out += f'<a href="{attr(rule_href(p))}">{word}\u00a0{p}</a>'
                    first = False
                else:
                    out += f'<a href="{attr(rule_href(p))}" aria-label="Rule {p}">{p}</a>'
            else:
                out += p
        return out
    return re.sub(r'\b(Rules?)[ \u00a0]((?:\d{2}\.\d{1,2})(?:(?:, | and | to |, and )\d{2}\.\d{1,2})*)', one, t)


def ids_nowrap(t):
    t = re.sub(r'\b((?:Loop|Reforms?|Rules?)) ((?:R-?\d+[a-z]?|\d{2}\.\d{1,2}))\b', '\\1\u00a0\\2', t)
    return re.sub(r'(?<![\w-])((?:CL|R|DR|D2|Q)-\d+)\b', r'<span class="nw">\1</span>', t)


def md(s):
    """Escaped text with **bold**, rule links and IDs kept whole at line ends."""
    t = html.escape(copy(s), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = ids_nowrap(t)
    return link_rules(t)


def esc(s):
    return html.escape(copy(s), quote=False)


FILL = {}


def fill(s):
    try:
        return str(s).format_map(FILL)
    except (KeyError, IndexError, ValueError) as e:
        raise BoardError(f'the board\'s words name an unknown value {e}: {str(s)[:80]}')


def paras(x, cls=''):
    items = x if isinstance(x, list) else [x] if x else []
    c = f' class="{cls}"' if cls else ''
    return ''.join(f'<p{c}>{md(fill(p))}</p>' for p in items)


def words_date(d):
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def words_time(d):
    h = d.hour % 12 or 12
    return f'{h}:{d.minute:02d} {"a.m." if d.hour < 12 else "p.m."}'


def iso_words(s):
    try:
        return words_date(datetime.date.fromisoformat(str(s)[:10]))
    except ValueError:
        return str(s)


def codes(s):
    return f'<p class="codes"><span class="vh">For the record: </span>{esc(s)}</p>' if s else ''


def sentences(p):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z“])', p) if s.strip()]


def strip_tags(t):
    return html.unescape(re.sub(r'<[^>]+>', '', t))


# ------------------------------------------------------------------------------------------------ sources
def read_log():
    logs = sorted((ROOT / 'work/ledger').glob('*_Decision-Log.md'))
    need(logs, 'no decision log in work/ledger/')
    rows = {}
    for ln in logs[0].read_text().splitlines():
        m = re.match(r'\|\s*((?:DR|D2)-\d+)\s*\|(.*)', ln)
        if m:
            rows[m.group(1)] = m.group(2)
    qs = sorted((ROOT / 'work/ledger').glob('*_Open-Questions.md'))
    need(qs, 'no open questions file in work/ledger/')
    for ln in qs[0].read_text().splitlines():
        m = re.match(r'\|\s*(Q-\d+)\s*\|(.*)', ln)
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


def read_chapters():
    nums = []
    for p in sorted(CHAPTERS.glob('*.json')):
        d = load_json(p, 'a chapter file')
        if isinstance(d, dict) and str(d.get('number', '')).isdigit():
            nums.append(int(d['number']))
        for r in (d.get('rules') or []) if isinstance(d, dict) else []:
            if isinstance(r, dict) and r.get('id'):
                RULES[str(r['id'])] = r
    need(len(RULES) > 100, f'only {len(RULES)} rules found in the chapter files')
    return sorted(nums)


def chapter_list(nums):
    """'01 to 12, 17, 18, 19 and 26' from the chapter numbers: runs of four or more collapse to 'a to b'."""
    runs, cur = [], [nums[0]]
    for n in nums[1:]:
        if n == cur[-1] + 1:
            cur.append(n)
        else:
            runs.append(cur)
            cur = [n]
    runs.append(cur)
    parts = []
    for r in runs:
        if len(r) >= 4:
            parts.append(f'{r[0]:02d} to {r[-1]:02d}')
        else:
            parts += [f'{n:02d}' for n in r]
    return ', '.join(parts[:-1]) + ' and ' + parts[-1] if len(parts) > 1 else parts[0]


def rule_text(rid):
    r = RULES.get(rid)
    need(r is not None, f'Rule {rid} is missing from the chapter files')
    x = r.get('rule')
    return [x] if isinstance(x, str) else list(x or [])


def rule_sentence(rid, start, field='rule'):
    paras_ = rule_text(rid) if field == 'rule' else (RULES[rid].get('why') or {}).get('text') or []
    paras_ = [paras_] if isinstance(paras_, str) else paras_
    for p in paras_:
        for s in sentences(strip_tags(p)):
            if s.startswith(start):
                return s
    warn(f'Rule {rid} no longer holds a sentence starting "{start}"')
    return None


def frozen_page(log):
    """The page the reviewers read, from git at the commit D2-1531 names, checked against the SHA-256 the log records."""
    row = log.get('D2-1531', '')
    m = re.search(r'at commit ([0-9a-f]{7,40})', row)
    h = re.search(r'SHA-256 ([0-9a-f]{8,64})', row)
    v = re.search(r'published as version (\d+)', row)
    need(m and h and v, 'D2-1531 no longer names the frozen page\'s commit, SHA-256 and version')
    try:
        raw = subprocess.run(['git', '-C', str(ROOT), 'show', f'{m.group(1)}:./{FROZEN_PATH}'],
                             capture_output=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as e:
        raise BoardError(f'git could not read the frozen page at {m.group(1)}: {e}')
    sha = hashlib.sha256(raw).hexdigest()
    need(sha.startswith(h.group(1)), f'the frozen page at {m.group(1)} has SHA-256 {sha[:16]}, not {h.group(1)} as D2-1531 records')
    return raw.decode('utf-8'), {'commit': m.group(1), 'sha256': sha, 'version': int(v.group(1)), 'path': FROZEN_PATH}


def frozen_rule_paras(page, rid):
    anchor = f'id="rule-{rid.replace(".", "-")}"'
    i = page.find(anchor)
    need(i >= 0, f'the frozen page has no {anchor}')
    j = page.find('id="rule-', i + len(anchor))
    chunk = page[i:j if j > 0 else i + 40000]
    return [squash(strip_tags(x)) for x in re.findall(r'<p class="rule-text">(.*?)</p>', chunk, flags=re.S)]


def counts_19(text):
    m = re.search(r'Today a rule meets (\d+) criteria and (\w+) more in part\. (\w+) are gaps.*?and (\w+) govern things', text)
    if not m:
        return None
    return {'met': m.group(1), 'in_part': m.group(2).lower(), 'gaps': m.group(3).lower(), 'unused': m.group(4).lower()}


def read_tokens():
    t = SRC['tokens_css'].read_text()
    v = dict(re.findall(r'(--oa-[\w-]+):\s*([^;]+);', t))

    def res(n, depth=0):
        need(n in v and depth < 20, f'tokens.css: {n} is missing')
        x = v[n].strip()
        mm = re.fullmatch(r'var\((--[\w-]+)\)', x)
        return res(mm.group(1), depth + 1) if mm else x.upper()
    c = {k: res(n) for k, n in {'red': '--oa-color-palette-pillar-red', 'charcoal': '--oa-color-palette-charcoal',
                                 'prussian': '--oa-color-palette-prussian',
                                 'field_on_charcoal': '--oa-color-field-ground-on-charcoal'}.items()}
    if c['field_on_charcoal'] != c['charcoal']:
        warn(f'tokens.css: the field ground on Charcoal resolves to {c["field_on_charcoal"]}, not Charcoal')
    j = load_json(SRC['tokens_json'], 'tokens.json')
    ext = j['$extensions']['org.oathandaction']

    def walk(o, path=()):
        if isinstance(o, dict):
            if '$value' in o:
                yield path, o
                return
            for k, x in o.items():
                if not k.startswith('$'):
                    yield from walk(x, path + (k,))
    toks = list(walk(j))
    names = {'.'.join(p) for p, _ in toks}
    bar = 'oa.color.state.error.bar'
    if not any(n.startswith(bar + '.') for n in names):
        warn(f'tokens.json holds no {bar} token')
    dep = next((o.get('$deprecated') for p, o in toks if '.'.join(p).startswith('oa.color.state.error.mark') and o.get('$deprecated')), None)
    leaves = re.search(r'leaves with (\d+\.\d+\.\d+)', dep or '')
    if not leaves:
        warn('tokens.json: the old error mark name carries no "leaves with" release')
    return c, {'version': ext['version'], 'count': len(toks), 'bar': bar,
               'alias_leaves': leaves.group(1) if leaves else '6.1.0', 'tokens_json': j}


def contrast(a, b):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def read_atlas():
    a = load_json(SRC['atlas'], 'the atlas')
    loops = a['loops'] if isinstance(a['loops'], list) else list(a['loops'].values())
    reforms = a['reforms'] if isinstance(a['reforms'], list) else list(a['reforms'].values())
    L = {x['id']: x for x in loops}
    R = {x['id']: x for x in reforms}
    flagged = sorted(r['id'] for r in reforms if r.get('interest_note'))
    need(flagged == ['R-01', 'R-02'], f'the atlas flags {flagged}, not R-01 and R-02; the board\'s words name those two')
    for k in ('R1', 'R8', 'R10'):
        need(k in L, f'the atlas has no Loop {k}')
    for k in ('R-01', 'R-02', 'R-04', 'R-30'):
        need(k in R, f'the atlas has no Reform {k}')
    if L['R1'].get('evidence') != 'plausible':
        warn(f'the atlas grades Loop R1 {L["R1"].get("evidence")}, where the board says plausible')
    if 'R10' not in (R['R-01'].get('loops') or []):
        warn('Reform R-01 no longer sits on Loop R10, as the before caption says')
    if any('R1' in (R[f].get('loops') or []) for f in flagged) or R['R-04'].get('interest_note'):
        warn('a flagged reform sits on Loop R1, or Reform R-04 carries a flag; the after caption says neither')
    if 'R8' not in (R['R-30'].get('loops') or []) or R['R-30'].get('interest_note'):
        warn('Reform R-30 no longer sits on the housing loop R8 unflagged')
    return {'n_reforms': len(reforms), 'r01': R['R-01']['title'], 'r02': R['R-02']['title'], 'r04': R['R-04']['title'],
            'r30': R['R-30']['title'], 'r1': L['R1']['title'], 'r8': L['R8']['title'], 'r10': L['R10']['title'],
            'r1_grade': L['R1'].get('evidence'), 'snapshot': a['meta'].get('snapshot')}


def word_diff(a, b):
    """Two sentences with what changed marked: struck in the first, bold in the second (chapter 02's marks)."""
    tok = lambda s: re.findall(r'\w[\w-]*|\s+|[^\w\s]', s)
    x, y = tok(a), tok(b)
    sm = difflib.SequenceMatcher(a=x, b=y, autojunk=False)
    pa, pb = '', ''
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        ta, tb = ''.join(x[i1:i2]), ''.join(y[j1:j2])
        if op == 'equal':
            pa += esc(ta)
            pb += esc(tb)
            continue
        if ta:
            pa += f'<del><span class="vh">taken out: </span>{esc(ta)}</del>'
        if tb:
            pb += f'<ins><span class="vh">put in: </span>{esc(tb)}</ins>'
    return pa, pb, sum(1 for o in sm.get_opcodes() if o[0] != 'equal')


# ------------------------------------------------------------------------------------------------ facts
def gather(log, frozen, tok, tokx, atlas, nums):
    F = {'chapters_version': CHAPTERS_VERSION, 'frozen_version': frozen['meta']['version'], 'chapter_list': chapter_list(nums)}
    F.update({k: atlas[k] for k in ('n_reforms', 'r01', 'r02', 'r04', 'r1', 'r10')})
    # contrast, from the palette
    F['red_on_charcoal'] = f'{contrast(tok["red"], tok["charcoal"]):.2f}'
    F['red_on_prussian'] = f'{contrast(tok["red"], tok["prussian"]):.2f}'
    note_ = json.dumps(tokx['tokens_json'], ensure_ascii=False)
    if f'{F["red_on_charcoal"]} to 1' not in note_:
        warn(f'tokens.json\'s change note does not print {F["red_on_charcoal"]} to 1 for red on Charcoal')
    q053 = rule_sentence('05.3', 'Red never sits on Prussian, where', field='why')
    if q053 and f'{F["red_on_prussian"]} to 1' not in q053:
        warn(f'Rule 05.3 does not print {F["red_on_prussian"]} to 1, the board\'s figure for red on Prussian')
    F['q_05_3'] = quote('q_05_3', q053 or '', 'chapter 05, Rule 05.3, why') if q053 else ''
    F['q_18_1'] = quote('q_18_1', rule_sentence('18.1', 'The ask stands') or '', 'chapter 18, Rule 18.1')
    F['q_17_3'] = quote('q_17_3', rule_sentence('17.3', 'For the wordmark or the lockmark') or '', 'chapter 17, Rule 17.3')
    # the closing block's words, from the build that prints them
    gb = read('guide_build')
    m = find('guide_build', r'(It holds no themes and no surface classes, so it cannot stand in for tokens\.css\.)', 'the closing block\'s words', text=gb)
    F['q_block'] = quote('q_block', m.group(1) if m else '', 'work/build/scripts/phase-2/guide_build.py, the For builders block')
    # tokens
    F.update({'version': tokx['version'], 'n_tokens': f'{tokx["count"]:,}', 'bar_name': tokx['bar'], 'alias_leaves': tokx['alias_leaves']})
    # Loop R1's grade line, from the code set a builder copies
    ls = squash(read('loop_set'))
    m = find('loop_set', r'(Our atlas grades this loop plausible:[^<]*?\.)\s*<', 'Loop R1\'s grade line', text=ls)
    F['grade_line'] = quote('grade_line', m.group(1) if m else '', 'work/build/guide/code/c-18-loop-stepper.html')
    # the log's figures
    m = re.search(r'missed (\d+) properties.*?targets under (\d+) px', log.get('D2-1549', ''))
    need(m, 'D2-1549 no longer gives the properties the block missed and the target size')
    F['n_missing'], F['target_px'] = m.group(1), m.group(2)
    m = re.search(r'sat (\d+) px from the red ask', log.get('D2-1545', ''))
    need(m, 'D2-1545 no longer gives the hover\'s distance from the ask')
    F['hover_gap'] = m.group(1)
    if not re.search(r'Rule 18\.24\'s examples become Loop R1 and Reform R-04', log.get('D2-1546', '')):
        warn('D2-1546 no longer sets Rule 18.24\'s examples to Loop R1 and Reform R-04')
    # the reports
    pp = read('pp')
    m = find('pp', r'\*\*(The panel is simulated and untested with real people\.)\*\*', 'the production test\'s label', text=pp)
    F['pp_label'] = quote('pp_label', m.group(1) if m else '', 'the plain language and production report')
    be = read('be')
    m = find('be', r'approve one standing rule: (.+?)\n', 'the standing rule\'s words', text=be)
    F['rule_text'] = quote('rule_text', m.group(1).strip() if m else '', 'the brand and evidence report, question 2')
    m = find('be', r'Chapter 18 brings it back across (\w+) plates', 'how many plates drifted', text=be)
    F['n_plates'] = m.group(1) if m else 'several'
    find('be', r'four criteria are not printed in W3C\'s order', 'the four criteria out of order', text=be)
    find('be', r'a builder reads auto-population as an exception', 'what 3.3.7 read as', text=be)
    ca = read('ca')
    m = find('ca', r'still leaves a table of roughly ([\d,]+) px', 'the open table\'s height', text=ca)
    F['open_px'] = m.group(1) if m else ''
    eng = read('eng')
    m = find('eng', r'Measured: ([\d,]+) px tall closed at 1440 px \(it was ([\d,]+)\)', 'the token table\'s heights', text=eng)
    F['h_after'], F['h_before'] = (m.group(1), m.group(2)) if m else ('', '')
    m = find('eng', r'Each of the (\d+) categories is a disclosure', 'the token table\'s groups', text=eng)
    F['n_groups'] = m.group(1) if m else ''
    m = find('eng', r'A code panel shows (\d+) lines', 'a panel\'s height in lines', text=eng)
    F['panel_lines'] = m.group(1) if m else ''
    find('eng', r'tokens\.css is the one route', 'the engineer\'s call on the route', text=eng)
    comp = read('comp')
    m = find('comp', r'the longest ([\d,]+) \(the masthead\'s wordmark\), became [\d,]+ lines with \d+ over 100, the longest (\d+)',
             'the code panels\' line lengths', text=comp)
    F['line_before'], F['line_after'] = (m.group(1), m.group(2)) if m else ('', '')
    if F['n_groups'] and F['n_groups'] not in ' '.join(rule_text('26.7')):
        warn(f'Rule 26.7 no longer says the table has {F["n_groups"]} groups')
    # WCAG and chapter 19's counts, before (the frozen page) and after (the chapter file)
    wc = load_json(SRC['wcag'], 'the stored WCAG text')
    F['n_criteria'] = wc['count']['all']
    before = counts_19(' '.join(frozen_rule_paras(frozen['page'], '19.1')))
    after = counts_19(' '.join(strip_tags(p) for p in rule_text('19.1')))
    need(before and after, 'Rule 19.1 no longer gives its counts in the words the board reads')
    F.update({'met_before': before['met'], 'met_after': after['met'], 'inpart_after': after['in_part'],
              'gaps_after': after['gaps'], 'unused_after': after['unused']})
    F['_counts'] = {'before': before, 'after': after}
    return F


def rule_18_24(frozen):
    fz = frozen_rule_paras(frozen['page'], '18.24')
    b = next((s for p in fz for s in sentences(p) if s.startswith('A typed ID')), None)
    a = rule_sentence('18.24', 'A typed ID')
    need(b and a, 'Rule 18.24\'s example sentence is missing from the frozen page or the chapter file')
    b, a = b.replace('\u00a0', ' '), squash(a).replace('\u00a0', ' ')
    for w, s in (('Loop R10', b), ('Reform R-01', b), ('Loop R1', a), ('Reform R-04', a)):
        if w not in s:
            warn(f'Rule 18.24\'s {"before" if s is b else "after"} sentence no longer names {w}')
    quote('r1824_before', b, f'the frozen page, Rule 18.24 (commit {frozen["meta"]["commit"]})')
    quote('r1824_after', a, 'work/build/guide/chapters/18-components.json, Rule 18.24')
    return b, a


# ------------------------------------------------------------------------------------------------ sections
def cover(answer):
    pg = ''
    for name, key, text in W['pages']:
        h = f'<a href="{attr(CHAPTERS_URL)}">{esc(name)}</a>' if key == 'chapters' else esc(name)
        pg += f'<li><b>{h}</b>, {md(fill(text))}</li>'
    deck = list(W['deck'])
    if answer:
        deck[1] = W['deck_answered_2']
        box = (f'<aside class="ask ask--answered" aria-labelledby="ask-h"><h2 id="ask-h" class="sub4">{esc(fill(W["answer_h"]))}</h2>'
               f'<blockquote class="q q--answer"><p>{esc(answer)}</p></blockquote></aside>')
    else:
        box = (f'<aside class="ask" aria-labelledby="ask-h"><h2 id="ask-h" class="sub4">{esc(W["reply_h"])}</h2>'
               f'<p class="q" id="sample-reply">{md(W["sample_reply"])}</p>'
               f'<div class="copy-row"><button type="button" class="btn-copy" data-copy="sample-reply" data-status="reply-status">{esc(W["copy_reply"])}</button>'
               f'<span class="status" id="reply-status" role="status" aria-live="polite"></span></div></aside>')
    toc = [('decision', W['decision']['title']), ('scores', W['scores']['title']), ('found', W['found']['title']),
           ('calls', W['calls']['title']), ('answered', W['answered']['title']), ('next', W['next']['title'])]
    toc_html = ''.join(f'<li><a href="#{k}">{esc(t)}</a></li>' for k, t in toc)
    return f'''<header class="cover">
<p class="mast"><b>Oath &amp; Action</b><span class="label">{esc(W["kicker"])}</span></p>
<p class="label for">{esc(fill(W["for_line"]))}</p>
<h1>{esc(W["title_answered"] if answer else W["title"])}</h1>
<div class="cover-grid"><div class="deck">{paras(deck, "intro")}</div>
{box}
<div class="pages-w"><h2 class="sub4">{esc(W["pages_h"])}</h2><ul class="pages">{pg}</ul></div></div>
<nav class="toc" aria-labelledby="toc-h"><h2 class="label" id="toc-h">{esc(W["toc_h"])}</h2><ol>{toc_html}</ol></nav>
</header>'''


def decision(frozen, answer):
    D = W['decision']
    before, after = rule_18_24(frozen)
    pb, pa, nchg = word_diff(before, after)
    need(nchg >= 1, 'Rule 18.24\'s example did not change between the frozen page and the chapter file')
    label = D['label_answered'] if answer else D['label']
    head = (f'<div class="sec-top"><p class="label">{esc(label)}</p>{codes(D["codes"])}</div>'
            f'<h2 class="sec-h" id="decision-h">{esc(D["title"])}</h2>{paras(D["lede"][:1], "intro")}{paras(D["lede"][1:])}')
    rule_q = (f'<figure class="rule-q"><blockquote><p>{esc(FILL["rule_text"])}</p></blockquote>'
              f'<figcaption>{esc(D["rule_cap"])}</figcaption></figure>')
    link = f'<a href="{attr(rule_href("18.24"))}">Rule\u00a018.24</a>'

    def side(h, src, sent, cap, cls):
        return (f'<figure class="pair-side {cls}"><p class="label">{esc(fill(h))}</p><blockquote><p>{sent}</p></blockquote>'
                f'<figcaption><span class="src">{esc(src).replace("Rule 18.24", link)}</span> {md(fill(cap))}</figcaption></figure>')
    pair = (f'<h3 class="sub4" id="drift-h">{md(D["drift_h"])}</h3><div class="pair" role="group" aria-labelledby="drift-h">'
            + side(D['before_h'], D['before_src'], pb, D['before_cap'], 'pair--before')
            + side(D['after_h'], D['after_src'], pa, D['after_cap'], 'pair--after')
            + f'</div><p class="caption marks">{esc(D["marks_note"])}</p>')
    if answer:
        last = (f'<div class="approve approve--answered"><h3 class="label">{esc(fill(D["answered_h"]))}</h3>'
                f'<blockquote class="q q--answer"><p>{esc(answer)}</p></blockquote></div>')
    else:
        last = (f'<div class="approve"><h3 class="label">{esc(D["approve_h"])}</h3><p class="q">{md(D["approve"])}</p></div>')
    decide = (f'<div class="decide"><div class="rec"><h3 class="label">{esc(D["rec_h"])}</h3>{paras(D["rec"])}</div>'
              f'<div class="cost"><h3 class="label">{esc(D["cost_h"])}</h3>{paras(D["cost"])}</div>{last}</div>')
    body = f'<div class="card">{rule_q}{pair}{decide}</div>'
    return f'<section class="sec sec--lead" id="decision" aria-labelledby="decision-h">{head}{body}</section>'


def read_scores():
    S = load_json(SRC['scores'], 'the creative director\'s round 2 scores')
    R = load_json(SRC['rescores'], 'the creative director\'s rescore')
    for d, what in ((S, 'scores'), (R, 'rescore')):
        need(isinstance(d.get('items'), list) and d['items'], f'the {what} file has no items')
        for it in d['items']:
            for k, _ in CRITERIA:
                need(isinstance((it.get('scores') or {}).get(k), (int, float)), f'{what}: item {it.get("key")} has no {k} score')
    r2 = {it['key']: it for it in S['items']}
    for it in R['items']:
        if it['key'] not in r2 and it.get('was') is not None:
            warn(f'rescore item {it["key"]} has a "was" block but no round 2 item')
        if it['key'] in r2:
            for c, _ in CRITERIA:
                a, b = r2[it['key']]['scores'][c], it['scores'][c]
                was = (it.get('was') or {}).get(c)
                if a != b and was != a:
                    warn(f'rescore: {it["key"]} {c} moved from {a} to {b}, and its "was" reads {was}')
    return S, R, r2


def cell(a, b):
    def fig(v, cls, lab):
        low = isinstance(v, (int, float)) and v < 4
        return (f'<span class="{cls}{" lo" if low else ""}"><span class="vh">{lab} </span>{v}'
                f'{"<span class=vh> (under 4)</span>" if low else ""}</span>')
    r2 = fig(a, 'r2', 'Round 2:') if a is not None else '<span class="r2 r2--none"><span class="vh">Round 2: not scored.</span></span>'
    moved = a is not None and a != b
    return f'<td class="sc{" mv" if moved else ""}">{r2}{fig(b, "r3", "After the fix pass:")}</td>'


def scores_section(S, R, r2):
    WS = W['scores']
    dates = sorted({iso_words(S.get('date', '')), iso_words(R.get('date', ''))})
    FILL['score_dates'] = ' and '.join(dates)
    all_ready = all(it.get('ready') is True for it in R['items']) and all(min(it['scores'].values()) >= 4 for it in R['items'])
    head = ''.join(f'<th scope="col">{esc(n)}</th>' for _, n in CRITERIA)
    rows, moved, content_rows = '', [], []
    for it in R['items']:
        k = it['key']
        old = r2.get(k)
        name = ov(it.get('name', k))
        a = it.get('anchor')
        shown = esc(name).replace('Rule ', 'Rule\u00a0')
        nm = f'<a class="item" href="{attr(anchor_href(a))}">{shown}</a>' if a else shown
        if old is None:
            nm += f'<span class="sub">{esc(WS["new_item"])}</span>'
        cells = ''.join(cell(old['scores'][c] if old else None, it['scores'][c]) for c, _ in CRITERIA)
        rd_old = (old or {}).get('ready')
        rd = ('<span class="r2">' + ('<span class="vh">Round 2: </span>' + ('Yes' if rd_old else 'No') if old else '') + '</span>'
              + '<span class="r3"><span class="vh">After the fix pass: </span>' + ('Yes' if it.get('ready') else 'Not yet') + '</span>')
        rows += f'<tr><th scope="row">{nm}</th>{cells}<td class="sc rd">{rd}</td></tr>'
        content_rows.append({'key': k, 'name': name, 'round_2': (old or {}).get('scores'), 'after': it['scores'],
                             'ready_round_2': rd_old, 'ready_after': it.get('ready')})
        if old:
            for c, n in CRITERIA:
                if old['scores'][c] != it['scores'][c]:
                    why = ov((it.get('reasons') or {}).get(c, ''))
                    if not why:
                        warn(f'rescore: {k} {c} moved with no reason on file')
                    moved.append({'item': name, 'criterion': n, 'from': old['scores'][c], 'to': it['scores'][c], 'reason': why})
    table = (f'<p class="legend caption">{md(fill(WS["legend"]))} <span class="scroll-hint" aria-hidden="true">{esc(WS["scroll_hint"])}</span></p>'
             f'<div class="tw" role="region" tabindex="0" aria-labelledby="sc-cap"><table class="sc-t">'
             f'<caption id="sc-cap" class="vh">{esc(WS["caption"])}</caption><thead><tr><th scope="col">{esc(WS["item_h"])}</th>{head}'
             f'<th scope="col">{esc(WS["ready_h"])}</th></tr></thead><tbody>{rows}</tbody></table></div>')
    # One line of reason for each item that moved: of the reasons the creative director gave for the criteria that moved,
    # the shortest, word for word. The content JSON keeps every reason.
    mv, lines = '', []
    for name in dict.fromkeys(x['item'] for x in moved):
        xs = [x for x in moved if x['item'] == name]
        pick = min(xs, key=lambda x: len(x['reason']))
        what = ' · '.join(f'{x["criterion"]} {x["from"]} to {x["to"]}' for x in xs)
        lines.append({'item': name, 'moves': what, 'reason_of': pick['criterion'], 'reason': pick['reason']})
    if lines:
        mv = f'<h3 class="sub4">{esc(WS["moved_h"])}</h3><ul class="moves">'
        for x in lines:
            mv += (f'<li><p class="mv-h"><b>{esc(x["item"])}</b><span class="mv-c">{esc(x["moves"])}</span></p>'
                   f'<p>{md(x["reason"])}</p></li>')
        mv += '</ul>'
    intro = WS['intro_ready'] if all_ready else WS['intro_not_ready']
    if not all_ready:
        warn('an item in the rescore is not ready or scores under 4; the board says so without the "every item is" clause')
    html_ = (f'<section class="sec sec--minor" id="scores" aria-labelledby="scores-h"><h2 class="sec-h2" id="scores-h">{esc(WS["title"])}</h2>'
             f'<p class="intro">{md(intro)}</p>{table}{mv}</section>')
    return html_, {'rows': content_rows, 'moved': moved, 'printed_lines': lines, 'all_ready': all_ready,
                   'files': [show(SRC['scores']), show(SRC['rescores'])]}


def found_section():
    Fd = W['found']
    cols = ''
    for gi, (gh, items) in enumerate(Fd['groups']):
        lis = ''
        for h, chip, t in items:
            ch = f' <span class="chip">{esc(chip)}</span>' if chip else ''
            lis += f'<li><h4 class="f-h">{md(fill(h))}{ch}</h4><p>{md(fill(t))}</p></li>'
        cols += f'<section class="f-col" aria-labelledby="fg-{gi}"><h3 class="label f-g" id="fg-{gi}">{esc(gh)}</h3><ul class="f-list">{lis}</ul></section>'
    return (f'<section class="sec" id="found" aria-labelledby="found-h"><h2 class="sec-h2" id="found-h">{esc(Fd["title"])}</h2>'
            f'<p class="intro">{md(fill(Fd["intro"]))}</p><div class="found">{cols}</div></section>')


def calls_section():
    C = W['calls']
    lis = ''
    for i, (h, c, t) in enumerate(C['items']):
        lis += (f'<li class="call"><div class="call-l"><h3 class="call-h" id="call-{i}">{md(fill(h))}</h3>{codes(c)}</div>'
                f'<div class="call-r"><p>{md(fill(t))}</p></div></li>')
    return (f'<section class="sec sec--minor" id="calls" aria-labelledby="calls-h"><h2 class="sec-h2" id="calls-h">{esc(C["title"])}</h2>'
            f'<p class="intro">{md(C["intro"])}</p><ul class="calls">{lis}</ul></section>')


def log_list(lines):
    return '<ul class="log">' + ''.join(f'<li><p>{md(fill(t))}</p>{codes(c)}</li>' for c, t in lines) + '</ul>'


def answered_section():
    A = W['answered']
    return (f'<section class="sec sec--minor" id="answered" aria-labelledby="answered-h"><h2 class="sec-h2" id="answered-h">{esc(A["title"])}</h2>'
            f'<p class="intro">{md(A["intro"])}</p>{log_list(A["lines"])}</section>')


def next_section():
    N = W['next']
    return (f'<section class="sec sec--minor" id="next" aria-labelledby="next-h"><h2 class="sec-h2" id="next-h">{esc(N["title"])}</h2>'
            f'{log_list(N["lines"])}<h3 class="sub4">{esc(N["carried_h"])}</h3>{log_list(N["carried"])}</section>')


# ------------------------------------------------------------------------------------------------ page
CSS = r'''
/* Board C. The brand's shell on Newsprint, as board B set it: tokens.css grid margins, title, section, H3 and H4 styles,
   hairlines in Stone, White cards for words. The board has no red of its own and no Prussian: its one job is to read.
   One light look by design, on the brand's own surfaces, with every color set explicitly. */
:root{--m:max(var(--oa-layout-grid-phone-small-margin),env(safe-area-inset-left,0px));--mr:max(var(--oa-layout-grid-phone-small-margin),env(safe-area-inset-right,0px));--max:78rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--np:var(--oa-color-surface-newsprint);--wink:var(--oa-color-text-primary-on-white);--wink-2:var(--oa-color-text-secondary-on-white);
--whair:var(--oa-color-border-hairline-on-white);--wstrong:var(--oa-color-border-strong-on-white);color-scheme:light}
@media (min-width:24.375em){:root{--m:max(var(--oa-layout-grid-phone-margin),env(safe-area-inset-left,0px));--mr:max(var(--oa-layout-grid-phone-margin),env(safe-area-inset-right,0px))}}
@media (min-width:48em){:root{--m:var(--oa-layout-grid-tablet-margin);--mr:var(--oa-layout-grid-tablet-margin)}}
@media (min-width:64em){:root{--m:var(--oa-layout-grid-desktop-margin);--mr:var(--oa-layout-grid-desktop-margin)}}
@media (min-width:90em){:root{--m:var(--oa-layout-grid-wide-margin);--mr:var(--oa-layout-grid-wide-margin)}}
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;background:var(--np);scroll-padding-top:var(--oa-space-300)}
body{margin:0;background:var(--np);color:var(--ink);font:var(--oa-type-body);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration-thickness:var(--oa-border-width-underline);text-underline-offset:.2em}
a:hover{text-decoration-thickness:var(--oa-border-width-underline-hover)}
:focus-visible{outline:var(--oa-border-width-focus-ring) solid var(--oa-color-focus-ring-on-newsprint);outline-offset:var(--oa-border-focus-offset)}
.card :focus-visible,.ask :focus-visible,.tw:focus-visible,.call :focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
p{margin:0 0 var(--oa-space-200);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.nw,a[href*="#rule-"]{white-space:nowrap}
.board{max-width:calc(var(--max) + var(--m) + var(--mr));margin:0 auto;padding-left:var(--m);padding-right:var(--mr);padding-block:0 var(--oa-space-1300)}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0}
.caption{font:var(--oa-type-caption);color:var(--ink-2)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.sub4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-500) 0 var(--oa-space-200);text-wrap:balance}
.codes{font:var(--oa-type-caption);color:var(--ink-2);margin:0;font-variant-numeric:tabular-nums}
.card .codes,.call .codes{color:var(--wink-2)}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--strong);
  padding:0 6px;white-space:nowrap;vertical-align:.2em;font-size:.8125rem;line-height:1.5;margin-left:var(--oa-space-050)}
/* cover */
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);margin:0;border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.for{margin-top:var(--oa-space-800)}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-500);max-width:12ch;text-wrap:balance}
.cover-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-400) var(--oa-space-800);align-items:start}
.deck p:last-child{margin-bottom:0}
@media (min-width:64em){.cover-grid{grid-template-columns:minmax(0,7fr) minmax(0,4fr);grid-template-areas:"deck ask" "pages ask"}
  .deck{grid-area:deck}.ask{grid-area:ask}.pages-w{grid-area:pages}}
.pages-w .sub4{margin-top:0}
.pages{list-style:none;margin:0;padding:0;max-width:var(--oa-layout-measure-intro-max);border-top:var(--oa-border-width-hairline) solid var(--hair)}
.pages li{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.ask{background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300)}
.ask .sub4{margin-top:0}
.ask--answered{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal)}
.q{font:italic 400 1.25rem/1.45 var(--oa-font-family-quote);margin:0 0 var(--oa-space-200)}
blockquote.q{margin:0}blockquote.q p{font:inherit;margin:0}
.copy-row{display:flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-150) var(--oa-space-200)}
.btn-copy{font:var(--oa-type-ui);min-height:var(--oa-size-target-touch);padding:0 var(--oa-space-300);border:0;border-radius:0;cursor:pointer;
  background:var(--oa-color-action-primary-fill-on-white);color:var(--oa-color-action-primary-label-on-white)}
.btn-copy:hover{background:var(--oa-color-palette-charcoal);text-decoration:underline;text-underline-offset:.2em}
.status{font:var(--oa-type-body-small)}
.toc{margin:var(--oa-space-600) 0 0;border-top:var(--oa-border-width-hairline) solid var(--hair);border-bottom:var(--oa-border-width-hairline) solid var(--hair);padding:var(--oa-space-150) 0}
.toc .label{margin-bottom:var(--oa-space-050)}
.toc ol{margin:0;padding:0 0 0 1.4em;columns:1;column-gap:var(--oa-space-600)}
@media (min-width:48em){.toc ol{columns:2}}@media (min-width:80em){.toc ol{columns:3}}
.toc li{break-inside:avoid;font:var(--oa-type-body-small);font-variant-numeric:tabular-nums}
.toc a{display:inline-flex;align-items:center;min-height:2.25rem}
/* sections */
.sec{margin-top:var(--oa-space-1300);border-top:var(--oa-border-width-rule) solid var(--strong);padding-top:var(--oa-space-300)}
.sec--minor{margin-top:var(--oa-space-1000)}
.sec-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300)}
.sec-h{font:var(--oa-type-section);letter-spacing:var(--oa-type-section-letter-spacing);margin:var(--oa-space-150) 0 var(--oa-space-300);text-wrap:balance;max-width:16ch}
.sec-h2{font:var(--oa-type-h3);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0 0 var(--oa-space-200);text-wrap:balance}
.sec > .intro{margin-bottom:var(--oa-space-200)}
.card{background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300) var(--oa-space-200);min-width:0;margin-top:var(--oa-space-400)}
@media (min-width:48em){.card{padding:var(--oa-space-500) var(--oa-space-500)}}
.card .caption,.card .label{color:var(--wink-2)}
/* the decision */
.rule-q{margin:0;padding:0 0 var(--oa-space-400);border-bottom:var(--oa-border-width-hairline) solid var(--whair)}
.rule-q blockquote{margin:0;max-width:44rem}
.rule-q blockquote p{font:var(--oa-type-quote);font-size:clamp(1.375rem,1.2rem + .6vw,1.75rem);line-height:1.4;margin:0 0 var(--oa-space-150);max-width:none}
.rule-q blockquote p::first-letter{text-transform:uppercase}
.rule-q figcaption{font:var(--oa-type-caption);color:var(--wink-2)}
.card .sub4{margin-top:var(--oa-space-400)}
.pair{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300)}
@media (min-width:56em){.pair{grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--oa-space-500)}}
.pair-side{margin:0;border-top:var(--oa-border-width-bar) solid var(--wstrong);padding-top:var(--oa-space-150);min-width:0}
.pair--before{border-top-color:var(--oa-color-tint-stone-n88)}
.pair-side .label{margin-bottom:var(--oa-space-100)}
.pair-side blockquote{margin:0 0 var(--oa-space-150)}
.pair-side blockquote p{font:var(--oa-type-body);margin:0;max-width:none}
.pair-side figcaption{font:var(--oa-type-body-small);color:var(--wink-2);max-width:36rem}
.pair-side .src{display:block;font:var(--oa-type-caption);color:var(--wink-2);margin-bottom:var(--oa-space-050)}
del{text-decoration-thickness:2px;text-decoration-color:currentColor;color:var(--wink-2)}
ins{text-decoration:none;font-weight:700;background:var(--oa-color-tint-stone-n88);padding:0 .15em;margin:0 .05em}
.marks{margin:var(--oa-space-150) 0 0}
.decide{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-500);margin-top:var(--oa-space-500);border-top:var(--oa-border-width-rule) solid var(--wstrong);padding-top:var(--oa-space-300)}
@media (min-width:64em){.decide{grid-template-columns:minmax(0,4fr) minmax(0,5fr) minmax(0,3fr)}}
.decide .label{margin-bottom:var(--oa-space-100)}
.decide p{font:var(--oa-type-body-small)}
.decide .q,.approve .q p{font:italic 400 1.375rem/1.4 var(--oa-font-family-quote)}
.approve{border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-left:var(--oa-space-200)}
/* scores */
.legend{margin:var(--oa-space-300) 0 var(--oa-space-100);max-width:var(--oa-layout-measure-intro-max)}
@media (min-width:56em){.scroll-hint{display:none}}
.tw{position:relative;overflow-x:auto;background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);margin:var(--oa-space-300) 0 0}
.legend + .tw{margin-top:0}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
table.sc-t{min-width:48rem}
caption{caption-side:top;text-align:left;padding:var(--oa-space-150) var(--oa-space-200);font:var(--oa-type-body-small);color:var(--wink-2);border-bottom:var(--oa-border-width-hairline) solid var(--whair)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-150) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--oa-color-tint-white-n55);vertical-align:bottom}
thead th:not(:first-child){text-align:center}
tbody th{font-weight:600;width:9.5rem;min-width:9.5rem;max-width:9.5rem;position:sticky;left:0;z-index:1;background:var(--white);box-shadow:inset -1px 0 0 var(--oa-color-tint-stone-n88)}
thead th:first-child{position:sticky;left:0;z-index:2}
@media (min-width:56em){tbody th{width:auto;min-width:13rem;max-width:none;box-shadow:none}}
tbody th a.item{white-space:normal}
tbody th .sub{display:block;font:var(--oa-type-caption);color:var(--wink-2);font-weight:400}
td.sc{text-align:center;font-variant-numeric:tabular-nums;white-space:nowrap}
td.sc .r2{display:inline-block;min-width:1.4em;font:var(--oa-type-caption);color:var(--wink-2);margin-right:.35em;padding:0 .2em}
td.sc .r3{display:inline-block;min-width:1.7em;font-weight:700;font-size:1.0625rem;padding:0 .2em}
td.sc .lo{box-shadow:inset 0 0 0 var(--oa-border-width-hairline) var(--wstrong)}
td.sc .r3.lo{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--wstrong)}
td.mv .r3{background:var(--oa-color-tint-stone-n88)}
td.rd .r3{font-size:inherit;font-weight:600}
.moves{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:0 var(--oa-space-500);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:64em){.moves{grid-template-columns:repeat(2,minmax(0,1fr))}}
.moves li{padding:var(--oa-space-150) 0 var(--oa-space-100);border-bottom:var(--oa-border-width-hairline) solid var(--hair);min-width:0}
.moves p{font:var(--oa-type-body-small);margin:0 0 var(--oa-space-050)}
.mv-h{display:flex;flex-wrap:wrap;justify-content:space-between;gap:0 var(--oa-space-200)}
.mv-c{color:var(--ink-2);font-variant-numeric:tabular-nums}
/* found and fixed */
.found{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-400) var(--oa-space-500);margin-top:var(--oa-space-400)}
@media (min-width:64em){.found{grid-template-columns:repeat(3,minmax(0,1fr))}}
.f-col{min-width:0;border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-150)}
.f-g{margin-bottom:var(--oa-space-100)}
.f-list{list-style:none;margin:0;padding:0}
.f-list li{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
.f-list li:last-child{border-bottom:0}
.f-h{font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-050);text-wrap:balance}
.f-list p{font:var(--oa-type-body-small);margin:0}
/* calls */
.calls{list-style:none;margin:var(--oa-space-400) 0 0;padding:0;display:grid;gap:var(--oa-space-200)}
.call{background:var(--white);color:var(--wink);border:var(--oa-border-width-hairline) solid var(--whair);padding:var(--oa-space-300) var(--oa-space-200);
  display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-100) var(--oa-space-500)}
@media (min-width:48em){.call{padding:var(--oa-space-300) var(--oa-space-400)}}
@media (min-width:64em){.call{grid-template-columns:minmax(0,1fr) minmax(0,2fr)}}
.call-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-100);text-wrap:balance}
.call-r p{font:var(--oa-type-body-small);margin:0;max-width:var(--oa-layout-measure-intro-max)}
/* answered and next */
.log{list-style:none;margin:var(--oa-space-300) 0 0;padding:0;border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:58rem}
.sub4 + .log{margin-top:0}
.log li{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-050) var(--oa-space-400);padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.log li{grid-template-columns:minmax(0,1fr) 11rem}.log .codes{text-align:right}}
.log p{margin:0}
.foot{max-width:none;margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media print{.btn-copy,.copy-row,.toc{display:none}.sec{break-inside:auto}.call,.f-list li,.moves li{break-inside:avoid}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''

JS = r'''
(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  // Copy: the host's clipboard when it allows it, else the browser's own copy of the selected text, else a prompt to copy.
  function selectNode(el) {
    try { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); return true; } catch (e) { return false; }
  }
  $$('.btn-copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var src = document.getElementById(b.getAttribute('data-copy'));
      var st = document.getElementById(b.getAttribute('data-status'));
      var text = src ? src.innerText.trim() : '';
      var done = function () { st.textContent = 'Copied.'; };
      var fall = function () {
        var ok = false;
        if (src && selectNode(src)) { try { ok = document.execCommand('copy'); } catch (e) { ok = false; } }
        st.textContent = ok ? 'Copied.' : 'The reply is selected. Press Ctrl or Command and C to copy it.';
      };
      try {
        if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, fall);
        else fall();
      } catch (e) { fall(); }
    });
  });
})();
'''


def strip_css(t):
    """CSS without its comments, which carry build notes and repository paths."""
    return re.sub(r'\n\s*\n+', '\n', re.sub(r'/\*.*?\*/', '', t, flags=re.S)).strip()


def build_page(sections):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="chart-views" content="overview">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{strip_css(SRC["tokens_css"].read_text())}
{strip_css(CSS)}</style></head>
<body><main class="board" data-view-root="overview">
{sections}
<p class="foot caption">{esc(fill(W["foot"]))}</p>
</main>
<script>{JS}</script></body></html>'''


def visible_text(page):
    """The words a sighted reader sees: inline tags drop out without a space, block ends become one."""
    t = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    t = re.sub(r'<span class="vh">[^<]*</span>', '', t)
    t = re.sub(r'</?(?:p|li|ul|ol|h\d|td|th|tr|div|figure|figcaption|caption|blockquote|section|header|nav|aside|main|table|thead|tbody|button)\b[^>]*>|<br\s*/?>',
               ' ', t)
    return html.unescape(re.sub(r'<[^>]+>', '', t))


def checks(page, answer):
    text = visible_text(page)
    i = text.find('—')
    need(i < 0, 'an em dash on the board: ' + text[max(0, i - 60):i + 20])
    if '–' in text:
        i = text.find('–')
        warn('an en dash on the board: ' + text[max(0, i - 40):i + 20])
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text.replace(answer or '\x00', ' '), flags=re.I)})
    if flagged:
        warn('flagged words on the board: ' + ', '.join(flagged))
    if 'answers to its people' in text and TAGLINE not in text:
        raise BoardError('the tagline is quoted inexactly (H01)')
    # studio codes stay in the small "codes" lines
    no_codes = visible_text(re.sub(r'<p class="codes">.*?</p>', ' ', page, flags=re.S))
    stray = set(re.findall(r'\b(?:DR|D2|G1|Q)-\d+\b|\b(?:CD|BE|PP|CA)-[MS]\d+\b|\b[MS]\d{1,2}\b|\((?:R|S|M)\d\)', no_codes))
    stray |= {m for m in re.findall(r'(?<!Loop )(?<!Loop\u00a0)\bR\d+[a-z]?\b', no_codes)}
    if stray:
        warn('studio codes in the reader\'s way: ' + ', '.join(sorted(stray)))
    bare = re.sub(r'Reforms?[ \u00a0]R-\d+(?:[ \u00a0]to[ \u00a0]R-\d+)?', ' ', no_codes)
    bare_hits = sorted(set(re.findall(r'\bR-\d+\b', bare)))
    if bare_hits:
        warn('reform codes without their type word (H11): ' + ', '.join(bare_hits))
    for pat in (r'/home/', r'/tmp/', r'file:', r'\bwork/', r'scratchpad', r'@anthropic', r'\.local\b'):
        if re.search(pat, page):
            warn(f'a private path or address on the board ({pat})')
    hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', page))
    extra = hosts - {'fonts.googleapis.com', 'fonts.gstatic.com', 'claude.ai'}
    if extra:
        warn('links or loads to hosts other than claude.ai and Google Fonts: ' + ', '.join(sorted(extra)))
    # every quoted sentence is on the page word for word
    nt = norm(text)
    for k, q in QUOTES.items():
        if not q['text']:
            warn(f'quote {k} is empty: its source no longer holds it')
        elif norm(q['text']) not in nt:
            warn(f'quote {k} is not on the page word for word: "{q["text"][:70]}"')
    small = re.findall(r'font-size:\s*(\d*\.?\d+)(px|rem)', strip_css(CSS))
    for v, u in small:
        px = float(v) * (16 if u == 'rem' else 1)
        if px < 13:
            warn(f'a font size of {v}{u} in the board\'s CSS, under 13 px')
    return text


def main():
    global GUIDE_IDS
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--answered', help='Dustin\'s words, quoted exactly, once he answers the decision')
    ap.add_argument('--answered-on', help='the date of his answer in words, such as "November 12, 2026" (default: the build date)')
    ap.add_argument('--publish', type=pathlib.Path, default=DEF_PUBLISH)
    ap.add_argument('--scratch', type=pathlib.Path, default=DEF_SCRATCH)
    ap.add_argument('--out', type=pathlib.Path, default=DEF_OUT)
    ap.add_argument('--guide', type=pathlib.Path, default=DEF_GUIDE if DEF_GUIDE.exists() else None,
                    help='a built chapters page; every anchor the board links must be on it (default: the final build, if present)')
    a = ap.parse_args()
    answer = squash(a.answered) if a.answered else None
    if a.answered is not None:
        need(answer, '--answered is empty')
        need('—' not in answer, 'Dustin\'s words hold an em dash; the board quotes them exactly and prints no em dash, so ask the main session how to set them')
    if a.guide:
        need(a.guide.exists(), f'--guide {a.guide} does not exist')
        GUIDE_IDS = set(re.findall(r'\bid="([^"]+)"', a.guide.read_text()))
    else:
        note('no built chapters page to check the board\'s anchors against; pass --guide')
    need('—' not in json.dumps(W, ensure_ascii=False), 'the board\'s words hold an em dash (W21)')

    log = read_log()
    nums = read_chapters()
    page_raw, meta = frozen_page(log)
    frozen = {'page': page_raw, 'meta': meta}
    tok, tokx = read_tokens()
    atlas = read_atlas()
    FILL.update(gather(log, frozen, tok, tokx, atlas, nums))
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL.update({'built_date': words_date(built), 'built_time': words_time(built)})
    FILL['answered_on'] = squash(a.answered_on) if a.answered_on else words_date(built)
    if answer:
        need(re.fullmatch(r'[A-Z][a-z]+ \d{1,2}, \d{4}', FILL['answered_on']), f'--answered-on "{FILL["answered_on"]}" is not a date in words')
    for o in OVERRIDES:
        if o['evidence']:
            k, pat = o['evidence']
            if not re.search(pat, read(k)):
                warn(f'a copy edit\'s claim is not on file in {show(SRC[k])}: "{o["put"][:60]}"')
                o['put'] = o['find']

    # every code the board prints is in the decision log or the open questions
    printed = set()
    for s in json.dumps(W, ensure_ascii=False).split('"'):
        printed |= set(re.findall(r'\b(?:DR|D2|Q)-\d+\b', s))
    for c in sorted(printed):
        if c not in log:
            warn(f'{c} is printed on the board and missing from the decision log and open questions')
    for c, _ in W['answered']['lines']:
        if c in log and 'Dustin' not in log[c]:
            warn(f'{c} is listed as answered this chat, and its log row names no answer from Dustin')

    S, R, r2 = read_scores()
    s_cover = cover(answer)
    s_dec = decision(frozen, answer)
    s_scores, sc_content = scores_section(S, R, r2)
    s_found = found_section()
    s_calls = calls_section()
    s_ans = answered_section()
    s_next = next_section()
    page = build_page('\n'.join([s_cover, s_dec, s_scores, s_found, s_calls, s_ans, s_next]))
    for o in OVERRIDES:
        if o['n'] != 1:
            warn(f'a copy edit matched {o["n"]} times in the scores, not once: "{o["find"][:60]}"')
    text = checks(page, answer)
    need(len(page.encode()) < LIMIT, 'the board is over 16 MB')

    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(page)
    chk = a.scratch / 'check-copy'
    chk.mkdir(parents=True, exist_ok=True)
    (chk / a.out.name).write_text(page)
    # the publish copy: no document skeleton (D2-317)
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n', '')
    head = head.replace(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    body = re.sub(r'</body>\s*</html>\s*$', '', body)
    a.publish.mkdir(parents=True, exist_ok=True)
    pub_html = a.publish / a.out.name
    pub_html.write_text(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
                        + head + '<script>document.documentElement.lang="en";</script>' + body)
    (a.publish / 'files.json').write_text('{}\n')
    content = {
        'built': built.isoformat(), 'board': show(a.out), 'title': TITLE,
        'chapters_page': {'url': CHAPTERS_URL, 'version': CHAPTERS_VERSION},
        'frozen_page': meta, 'answered': {'words': answer, 'on': FILL['answered_on']} if answer else None,
        'words': W, 'filled': {k: v for k, v in FILL.items() if not k.startswith('_')},
        'chapter_19_counts': FILL['_counts'], 'quotes': QUOTES, 'atlas': atlas,
        'tokens': {'version': tokx['version'], 'count': tokx['count'], 'colors': tok},
        'scores': sc_content, 'overrides': [{k: o[k] for k in ('find', 'put', 'n')} for o in OVERRIDES],
        'rule_anchors_linked': sorted(LINKED), 'guide_checked': show(a.guide) if a.guide else None,
        'sources': {k: show(v) for k, v in SRC.items()},
        'notes': NOTES, 'warnings': WARN, 'visible_text_sha1': hashlib.sha1(text.encode()).hexdigest(),
    }
    cpath = a.out.parent / f'{DATE}_Board-C-Content.json'
    cpath.write_text(json.dumps(content, indent=1, ensure_ascii=False, default=str))
    print(f'wrote {show(a.out)} ({len(page.encode()) / 1e3:.0f} kB){" as answered" if answer else ""}')
    print(f'wrote {show(cpath)}')
    print(f'wrote the check copy {chk / a.out.name}')
    print(f'wrote the publish copy {pub_html}')
    print(f'{len(LINKED)} chapters page anchors linked; {len(QUOTES)} quotes; {len(NOTES)} notes; {len(WARN)} warnings')
    if WARN and a.strict:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
