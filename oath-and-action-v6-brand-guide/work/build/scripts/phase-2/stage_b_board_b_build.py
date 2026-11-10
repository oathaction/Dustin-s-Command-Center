"""Build board B, the decisions board (November 10, 2026): the two decisions Dustin answers by name, the creative
director's scores, the calls the studio made that he may overrule, what he answered this chat, what is carried, and the
reader check's invitation (DR-193, brief: work/handoffs/phase-2/20261110_Board-B-Brief.md).

Usage:
    python3 -I work/build/scripts/phase-2/stage_b_board_b_build.py [--strict] [--reader-check-url URL]
        [--publish DIR] [--guide PAGE] [--out PATH] [--scratch DIR]

Reads, on every run (the facts on the board come from these files; the script holds only the board's own words):
    work/build/tokens/tokens.css                                   the colors behind every contrast figure
    work/build/guide/chapters/*.json                               rule text the board quotes, and every rule it links
    work/build/assets/utility/svg-24/20261110_Utility-Error-24px.svg   the error mark, drawn inline in currentColor
    work/build/assets/civic-line-v6/ (inventory, black SVGs) and work/build/assets/civic-line/tiles/   the drawings
    work/build/guide/specimens/s-proofs-social.html                the social card's "Left out" line
    work/handoffs/phase-2/20261110_Stage-B-Round-3-CD-Scores.json  round 3 scores, and the rescore block once it lands
    work/handoffs/phase-2/20261110_Stage-B-Ch10-Labels.json        the drawings' names
    work/handoffs/phase-2/20261110_Reader-Check-2-Questions.md     the editor's invitation, section "The invitation"
    work/ledger/*_Decision-Log.md                                  every DR and D2 code the board prints must exist
Writes:
    work/boards/phase-2/stage-b/board-b/20261110_Board-B.html           the board, images by relative path in img/
    work/boards/phase-2/stage-b/board-b/20261110_Board-B-Content.json   every string and figure the board prints
    work/boards/phase-2/stage-b/board-b/img/                            the Civic Line files the board shows
    <scratch>/board-b/check-copy/                                       a copy for dataviz_check.js with captures
    <publish>/20261110_Board-B.html, <publish>/img/, <publish>/files.json   the publish copy, no document skeleton

--strict exits 1 on any warning: a quoted sentence the chapters no longer hold, a contrast figure that differs from
Rule 11.15's text, a decision code missing from the log, a studio code in the reader's way, a flagged word, an en dash,
a rule link with no rule behind it, or a rescore block the script cannot read. An em dash stops the build. A missing
rescore and a placeholder reader check address are notes, not warnings: rerun when either arrives.
"""
import argparse
import datetime
import hashlib
import html
import json
import pathlib
import re
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261110'
BOARD_DIR = ROOT / 'work/boards/phase-2/stage-b/board-b'
SCRATCH = pathlib.Path('/tmp/claude-0/-home-user-Dustin-s-Command-Center/c9dc3e94-c343-5611-8fc3-849f48a2fa49/scratchpad')
HANDOFFS = ROOT / 'work/handoffs/phase-2'
ASSETS = ROOT / 'work/build/assets'
CHAPTERS = ROOT / 'work/build/guide/chapters'
TOKENS = ROOT / 'work/build/tokens/tokens.css'
SRC = {
    'scores': HANDOFFS / f'{DATE}_Stage-B-Round-3-CD-Scores.json',
    'labels': HANDOFFS / f'{DATE}_Stage-B-Ch10-Labels.json',
    'reader': HANDOFFS / f'{DATE}_Reader-Check-2-Questions.md',
    'inventory': ASSETS / 'civic-line-v6/20261110_Civic-Line-V6-Inventory.json',
    'black': ASSETS / 'civic-line-v6/black',
    'tiles_v6': ASSETS / 'civic-line-v6',
    'error_svg': ASSETS / 'utility/svg-24/20261110_Utility-Error-24px.svg',
    'social': ROOT / 'work/build/guide/specimens/s-proofs-social.html',
    'form': ROOT / 'work/build/guide/specimens/s-11-15-correct.html',
}
DEF_OUT = BOARD_DIR / f'{DATE}_Board-B.html'
DEF_PUBLISH = SCRATCH / 'publish-board-b'
DEF_SCRATCH = SCRATCH / 'board-b'
CHAPTERS_URL = 'https://claude.ai/artifact/9pWY47rkVa8N2SFwAPExTF'
CHAPTERS_VERSION = 5
PLACEHOLDER = 'READER-CHECK-PENDING'
TITLE = 'Board B Decisions'
TAGLINE = 'A country that answers to its people.'
LIMIT = 16_000_000
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'leverages', 'leveraged', 'underscore',
           'underscores', 'reflect', 'reflects', 'reflected', 'stunning', 'robust', 'seamless', 'perhaps', 'somewhat']
CRITERIA = [('craft', 'Craft'), ('clarity', 'Clarity'), ('brand_fidelity', 'Brand fidelity'), ('usefulness', 'Usefulness'),
            ('evidence_honesty', 'Evidence honesty'), ('accessibility', 'Accessibility')]
TILE_SUBJECT = 'CL-005'                       # Public meeting: off the list of 41, among the 94 that read at 32 px
LOOKALIKES = ['CL-023', 'CL-028', 'R-08', 'R-27', 'R-45']   # Rule 10.9, D2-971
ENLARGE = 4                                   # the error mark's enlargement, named on the board
WARN, NOTES = [], []
# Copy edits to strings the board takes from other owners' files (the scores' reasons): exact text, replacement.
# Each must match at least once, or the build warns.
OVERRIDES = [
    ['`s-05-3-corrective` draws the error as a white cross in a red disc, the sign for Close, against DR-173 (already D2-881).',
     'Rule 05.3’s corrective plate draws the error as a white cross in a red disc, the sign for Close, where you approved a circle holding an exclamation mark.', 0],
    ["s-05-3-corrective now draws the approved error mark, a circle holding an exclamation mark, in the text's ink with the 4 px Pillar Red bar, as Rule 11.15 does (D2-881, D2-959).",
     'Rule 05.3’s corrective plate now draws the approved error mark, a circle holding an exclamation mark, in the text’s ink with the 4 px Pillar Red bar, as Rule 11.15 does.', 0],
]

# ------------------------------------------------------------------------------------------------ the board's words
# Every word the studio writes for this board. Facts the board quotes or measures are read from the sources at build
# time and filled in where a {name} stands. Codes in "codes" fields print in small type beside a card, for the record.
W = {
    'kicker': 'Edition 06 · Stage B · Board B',
    'for_line': 'For Dustin Cathcart · {built_date}',
    'title': 'Two decisions are yours',
    'deck': [
        'Board B closes stage B, in which the studio built chapters 09 to 12 and fixed, in one pass, what three red teams and the creative director found in them.',
        'This page holds the two questions you answer by name, with the creative director’s scores and the calls the studio made that you may overrule.',
    ],
    'pages_h': 'The three pages of board B',
    'pages': [
        ('The chapters page', 'chapters', 'version {chapters_version}, with chapters 01 to 12 and the identity proofs as the fix pass left them. Each rule number on this board opens it at that rule.'),
        ('The reader check', 'reader', 'a test of about 15 minutes on a phone, for five to eight people who have never seen the brand. Its invitation waits at the end of this board, ready to paste.'),
        ('This board', None, 'your two decisions, the scores, the calls you may overrule and what stays open after board B.'),
    ],
    'reply_h': 'A reply can be this short',
    'sample_reply': 'All as recommended. I approve option A for the error mark by name, and keep the one-color tile exception in Rule 10.5.',
    'copy_reply': 'Copy the reply',
    'toc_h': 'On this board',
    'd1': {
        'label': 'Decision 1 of 2',
        'title': 'The error mark',
        'codes': 'D2-880 · D2-859 · DR-173',
        'lede': [
            'Rule 11.15 draws the error mark, a circle holding an exclamation mark, in the text’s ink, and gives the error’s red to a 4 px Pillar Red bar at the left of the field and of the message. You approved the drawing on November 10. Its color comes to you by name because our red token’s description names the mark and its bar, and Gate 2 confirms the tokens.',
        ],
        'a_h': 'Option A, as built',
        'a_text': 'The mark in the text’s ink, Charcoal, with the 4 px Pillar Red bar at the left of the field and of the message.',
        'b_h': 'Option B',
        'b_text': 'The same mark drawn in Pillar Red, with the same bar.',
        'row_form': 'In the form, at actual size',
        'row_form_cap': 'A sign-up field after a wrong entry, as a phone shows it, at most 360 px wide. The mark stands at 24 px.',
        'row_alone': 'The mark alone, 24 px, at actual size',
        'row_enl': 'Enlarged {enlarge_words} times',
        'row_enl_cap': 'The 24 px master drawn at {enlarged_px} px, so its 2 px line stands {enlarged_line} px wide.',
        'on_np': 'On Newsprint',
        'on_band': 'On the Error Band',
        'contrast_h': 'Contrast against the ground',
        'contrast_note': 'A mark that carries meaning needs 3 to 1 against its ground (Rule 05.5, and WCAG 2.2 success criterion 1.4.11). This board’s build works out each figure from the colors in our tokens.',
        'field_label': 'Email',
        'field_value': 'name.example.com',
        'rec': [
            'Option A. In Pillar Red the mark measures {b_band} to 1 on the Error Band and {b_np} to 1 on Newsprint, so a reader with low vision can lose it on either ground, and a 2 px line leaves no room for the Charcoal keyline Rule 05.5 gives red on Newsprint. In ink it measures {a_band} to 1 on the band, and the bar still gives the error the view’s red.',
            'If you approve option A, the engineer rewords the red token’s description at Gate 2 so it names the bar alone. Option B changes one color in one drawing, and setting that color back undoes it.',
        ],
        'approve': 'Option A for the error mark, as Rule 11.15 draws it.',
    },
    'd2': {
        'label': 'Decision 2 of 2',
        'title': 'Tiles under the 48 px floor',
        'codes': 'D2-976 · DR-136',
        'lede': [
            'On November 8 you set 48 px as the smallest size for a topic or atlas symbol, with 24 px allowed only for the 41 that read there. A tile, the square, rounded square or circle that holds a drawing as an app icon or an avatar, draws its symbol at about two thirds of its own size. So a one-color tile from 48 px draws its symbol at 32 to 34 px, under that floor.',
            'The tile sizes came from the October review, which read every drawing at 32 px before you set the floor. Rule 10.5 now names the small one-color tiles as the one exception:',
        ],
        'fig_cap': '{subject}, a topic symbol off the list of 41, at actual size on Newsprint. The tile is Charcoal, the default for app icons and avatars.',
        'tile_cap': 'One-color tile, {px} px, its drawing about {inner} px',
        'alone48_cap': 'The drawing alone, 48 px, the floor',
        'alone32_cap': 'The drawing alone, 32 px',
        'other_h': 'The other answer',
        'other_cap': 'The smallest one-color tile, {px} px, its drawing about {inner} px',
        'rec': [
            'Keep the exception. Avatars and small app tiles show at 32 to 48 px, and on a tile the drawing sits on a solid ground of its own.',
            'The other answer gives all {n_all} drawings one-color tiles from {sq} px square, {rd} px rounded and {ci} px round, which keeps the 48 px floor with no exception and rules out small avatars.',
        ],
        'approve': 'Keep the one-color tile exception in Rule 10.5.',
    },
    'rec_h': 'Recommendation',
    'approve_h': 'What you approve by name',
    'scores': {
        'title': 'The creative director’s scores',
        'intro': [
            'The creative director scored chapters 09 to 12, and the parts of chapters 01, 03, 04, 05 and 08 that changed, on the six criteria of our rubric, from 1 to 5. An item is ready at 4 or more on every one.',
        ],
        'r3_caption': 'Round 3, {r3_date}: the page as the red teams read it, before the fix pass. A boxed score is under 4.',
        'rescore_caption': 'The rescore after the fix pass{rs_date}. A boxed score is under 4, and “was” gives the round 3 score where it moved.',
        'waiting': 'The creative director rescores after the fix pass, and the studio then rebuilds this board with the rescore set apart from round 3.',
        'low_h': 'What stood under 4 at round 3',
        'moved_h': 'What moved in the rescore',
        'ready_h': 'Ready',
        'item_h': 'Chapter or part',
    },
    'calls': {
        'title': 'Calls the studio made that you may overrule',
        'intro': 'The studio made these four calls inside the plan you approved. Each stands unless you say otherwise.',
        'row': {
            'h': 'Where the pillar row goes',
            'codes': 'D2-962',
            'text': 'No rule said where the row of four pillar icons belongs, which stopped the simulated designer in the production test. Rule 09.1 now says:',
            'social': 'The social card in the identity proofs now names what it leaves out:',
        },
        'five': {
            'h': 'Five symbols that look alike at 24 px',
            'codes': 'D2-971 · DR-136',
            'text': 'At 24 px these five drawings from the list of 41 draw as one shape, a page under a magnifier. The 41 stay as you approved them, and Rule 10.9 adds this line:',
            'cap': 'At actual size, 24 px, one color on Newsprint. They share a view here only to show the likeness.',
        },
        'reforms': {
            'h': 'Examples moved off the reforms tied to your work',
            'codes': 'D2-958 · DR-100 · DR-195',
            'text': [
                'Our atlas marks two reforms as tied to your own work: all-party primaries with ranked general elections (R-01) and ranked-choice voting (R-02). The guide no longer prints a disclosure, so the studio moved two examples it had chosen.',
                'Rule 10.8 used to show only R-01 and R-02. It now draws all 10 reforms the atlas aims at the six variables of its elections domain, so no two stand out.',
                'Rule 11.16’s invented bill, once on all-party primaries, is now a local news grants bill, and its figure marks reform R-32, public and philanthropic funding for local news, which carries no flag.',
                'Nothing else moved off them. Rule 12.5’s marker and the reader check stay on loop R10, on safe seats, and reform R-01, as you answered on November 10. That answer moved only chapter 11’s loop stepper, Rule 11.14, to loop R1, in which wealth and political influence reinforce each other.',
            ],
        },
        'tokens': {
            'h': 'The tokens download',
            'codes': 'D2-964 · DR-192',
            'text': 'On the published chapters page, the tokens.css button saves {zip}, a zip file holding tokens.css, because the host refuses to save a file that ends in .css and accepts a zip. A saved copy of the page, with no host behind it, still saves tokens.css itself.',
            'link': 'The download in the chapters page’s colophon',
        },
        'open': 'Open {what} in the chapters page',
    },
    'answered': {
        'title': 'What you answered this chat',
        'intro': 'You answered these on November 10, each as the studio recommended.',
        'lines': [
            ('DR-190', 'Round 3 ran three red teams side by side: brand, evidence and nonpartisanship; craft and accessibility; and plain language with a production test, in which a simulated designer and a simulated developer each tried a real task with the guide.'),
            ('DR-191', 'An item still under 4 after the fix pass gets a short second pass on that item alone when the fix is craft or wording, and only an item that needs your call comes to this board.'),
            ('DR-192', 'The chapters page asks the host for its download permission, so its tokens.css button saves the file for anyone viewing it.'),
            ('DR-193', 'Board B is three pages: the chapters page at its address as version 5, this decisions board and the reader check on its own private page.'),
            ('DR-194', 'The studio deletes the first reader check page once you have sent the new link and confirmed the delete.'),
            ('DR-195', 'Chapter 11’s loop stepper runs our atlas’s loop R1, in which wealth and political influence reinforce each other.'),
            ('DR-196', 'A subject that no topic drawing names, such as Housing, takes its word alone, and a Housing drawing joins the next drawings board for your approval by name.'),
            ('DR-197', 'The 16 px Pause and Filter files get 5 px bars and a 5 px spout, so each opening keeps a whole open pixel on 1x screens, and they come to you beside the approved files at stage C.'),
            ('DR-198', 'Pixel fits for the 37 drawings that may be set at 24 px, drawn by one hand, come to a board at stage C or Phase 3. Rule 10.4’s words stand until then.'),
        ],
    },
    'carried': {
        'title': 'Carried forward',
        'intro': 'These stay open after board B, apart from the last, which closes when you answer decision 2.',
        'lines': [
            ('D2-838', 'Missouri’s certified result. Counties file by November 17, the state board then has two weeks, and Rule 01.11’s words follow what it certifies.'),
            ('', 'Virginia’s 2025 House of Delegates party count, which still rests on our atlas until a primary source confirms it.'),
            ('D2-968', 'Tangipa v. Newsom’s January 14, 2026 order and the Ohio Redistricting Commission’s minutes, which the brand team could not open, so both stay unchecked.'),
            ('D2-715 · D2-965 · DR-196 · DR-197 · DR-198', 'Stage C: the shell’s last pass, with the creative director’s chapter 08 items and an opening figure for chapters 09 and 10; the 16 px Pause and Filter redraws; the 24 px fits, at stage C or Phase 3; and the Housing drawing.'),
            ('DR-194', 'The first reader check page, deleted once you have sent the new link and confirmed.'),
            ('D2-976', 'The tile question, decision 2 on this board. Rule 10.5 states the one-color tile exception until you answer.'),
        ],
    },
    'reader': {
        'title': 'The reader check',
        'text': [
            'The invitation goes to five to eight people who have never seen the brand, with a mix of ages and political leanings. Each takes the check once, on a phone, in about 15 minutes.',
            'The editor wrote these two lines for you to paste, with the check’s address already in place.',
        ],
        'address_h': 'Its address',
        'invite_h': 'The invitation',
        'copy': 'Copy the invitation',
        'pending': 'The address fills in when the main session publishes the reader check.',
    },
    'foot': 'Built {built_date} at {built_time} UTC from the chapter files, the tokens, the creative director’s scores, the editor’s reader check file and the decision log.',
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


def ov(s):
    if not isinstance(s, str):
        return s
    for o in OVERRIDES:
        if o[0] in s:
            o[2] += s.count(o[0])
            s = s.replace(o[0], o[1])
    return s


def copy(s):
    """Curly quotes and apostrophes, the true minus before a figure (H07), and plain hyphens in IDs (D2-975)."""
    s = str(s).replace('‑', '-')
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    s = re.sub(r'(\d) (px|percent)\b', '\\1\u00a0\\2', s)
    return re.sub(r'(?<![\w.\-/])-(?=\d)', '−', s)


def attr(s):
    return html.escape(str(s), quote=True)


RULES = {}          # '11.15' -> rule dict
CH_ANCHORS = set()  # chapter anchors
GUIDE_IDS = None    # ids in a built guide page, when --guide is given
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
                    out += f'<a href="{attr(rule_href(p))}">{word} {p}</a>'
                    first = False
                else:
                    out += f'<a href="{attr(rule_href(p))}" aria-label="Rule {p}">{p}</a>'
            else:
                out += p
        return out
    return re.sub(r'\b(Rules?) ((?:\d{2}\.\d{1,2})(?:(?:, | and | to |, and )\d{2}\.\d{1,2})*)', one, t)


ZIPS = set()


def ids_nowrap(t):
    for z in ZIPS:
        t = t.replace(z, f'<span class="nw">{z}</span>')
    return re.sub(r'\b((?:CL|R|DR|D2)-\d+)\b', r'<span class="nw">\1</span>', t)


def md(s):
    """Escaped text with **bold**, rule links and IDs kept whole at line ends."""
    t = html.escape(copy(s), quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = link_rules(t)
    return ids_nowrap(t)


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


NUM_WORDS = {1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six', 7: 'seven', 8: 'eight', 9: 'nine'}


def num_words(n):
    return NUM_WORDS.get(n, str(n))


def codes(s):
    return f'<p class="codes"><span class="vh">For the record: </span>{ids_nowrap(esc(s))}</p>' if s else ''


# ------------------------------------------------------------------------------------------------ sources
def read_tokens():
    t = TOKENS.read_text()
    v = dict(re.findall(r'(--oa-[\w-]+):\s*([^;]+);', t))

    def res(n, depth=0):
        need(n in v and depth < 20, f'tokens.css: {n} is missing')
        x = v[n].strip()
        m = re.fullmatch(r'var\((--[\w-]+)\)', x)
        return res(m.group(1), depth + 1) if m else x
    names = {
        'newsprint': '--oa-color-surface-newsprint', 'band': '--oa-color-state-error-band-on-newsprint',
        'red': '--oa-color-state-error-mark-on-newsprint', 'ink': '--oa-color-state-error-text-on-newsprint',
        'pillar_red': '--oa-color-palette-pillar-red', 'charcoal': '--oa-color-palette-charcoal',
    }
    out = {k: res(n).upper() for k, n in names.items()}
    for k, h in out.items():
        need(re.fullmatch(r'#[0-9A-F]{6}', h), f'tokens.css: {names[k]} resolves to {h}, not a hex color')
    need(out['red'] == out['pillar_red'], 'the error mark token no longer resolves to Pillar Red')
    return out, names


def contrast(a, b):
    def lum(h):
        c = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        c = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
        return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
    x, y = lum(a), lum(b)
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def fmt_ratio(r):
    return f'{r:.2f}'


def read_chapters():
    anchors = {}
    for p in sorted(CHAPTERS.glob('*.json')):
        d = load_json(p, 'a chapter file')
        if isinstance(d, dict) and d.get('anchor'):
            anchors[d['anchor']] = d.get('title')
        for r in (d.get('rules') or []) if isinstance(d, dict) else []:
            if isinstance(r, dict) and r.get('id'):
                RULES[str(r['id'])] = r
    CH_ANCHORS.update(anchors)
    need(len(RULES) > 100, f'only {len(RULES)} rules found in the chapter files')


def rule_paras(rid):
    r = RULES.get(rid)
    need(r is not None, f'Rule {rid} is missing from the chapter files')
    x = r.get('rule')
    return [x] if isinstance(x, str) else list(x or [])


def sentences(p):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+(?=[A-Z“])', p) if s.strip()]


def quote_09_1():
    """Rule 09.1's places sentences (D2-962): the sentences that place the rows and keep them off a card."""
    found = [s for p in rule_paras('09.1') for s in sentences(p) if re.search(r'\brow runs\b|carry no row|carries no row', s)]
    if not found:
        warn('Rule 09.1 no longer holds a sentence that places the pillar row; the card prints the whole rule')
        return ' '.join(rule_paras('09.1'))
    return ' '.join(found)


def quote_social():
    t = SRC['social'].read_text()
    txt = html.unescape(re.sub(r'<[^>]+>', '\x00', t))
    m = re.search(r'Left out\x00+([^\x00]+)', txt)
    if not m:
        warn('the social card no longer prints a "Left out" line')
        return None
    return m.group(1).strip()


def quote_10_9():
    paras_ = rule_paras('10.9')
    p = next((x for x in paras_ if 'magnifier' in x), None)
    s = next((x for q in paras_ for x in sentences(q) if x.startswith('Never set two')), None)
    if not p or not s:
        warn('Rule 10.9 no longer holds the look-alike paragraph or its "Never set two" sentence')
    return p, s


def quote_10_5():
    p = next((x for x in rule_paras('10.5') if 'floor' in x and '32' in x), None)
    if not p:
        warn('Rule 10.5 no longer holds the paragraph that names the tile exception')
    return p


def check_11_15(figs):
    """Rule 11.15's why prints the contrast figures; the board computes them, and the two must agree."""
    why = RULES['11.15'].get('why') or {}
    text = ' '.join(why.get('text') if isinstance(why.get('text'), list) else [str(why.get('text', ''))])
    for k in ('b_band', 'b_np', 'a_band'):
        if figs[k] not in text:
            warn(f'Rule 11.15 does not print {figs[k]} to 1, the board\'s figure for {k}')
    return text


def check_11_16():
    r = RULES['11.16']
    cap = (r.get('correct') or {}).get('caption', '')
    if 'R-32' not in cap.replace('‑', '-'):
        warn('Rule 11.16\'s caption no longer names reform R-32')


def check_10_8():
    r = RULES['10.8']
    cap = (r.get('correct') or {}).get('caption', '')
    if not re.search(r'\ball 10 reforms\b|\ball ten reforms\b', cap):
        warn('Rule 10.8\'s caption no longer says it draws all 10 reforms')


def read_invitation(url):
    t = SRC['reader'].read_text()
    m = re.search(r'^## The invitation\s*$(.*?)(?=^## |\Z)', t, flags=re.S | re.M)
    need(m, 'the reader check file has no "## The invitation" section')
    quoted = [ln[1:].strip() for ln in m.group(1).splitlines() if ln.startswith('>')]
    lines, cur = [], []
    for q in quoted:
        if q:
            cur.append(q)
        elif cur:
            lines.append(' '.join(cur))
            cur = []
    if cur:
        lines.append(' '.join(cur))
    need(len(lines) == 2, f'the invitation has {len(lines)} paragraphs, not two')
    need(sum('[link]' in x for x in lines) == 1, 'the invitation should hold [link] once')
    return lines, [x.replace('[link]', url) for x in lines]


def read_log():
    logs = sorted((ROOT / 'work/ledger').glob('*_Decision-Log.md'))
    need(logs, 'no decision log in work/ledger/')
    t = logs[0].read_text()
    rows = {}
    for ln in t.splitlines():
        m = re.match(r'\|\s*((?:DR|D2)-\d+)\s*\|(.*)', ln)
        if m:
            rows[m.group(1)] = m.group(2)
    return rows


def read_labels():
    d = load_json(SRC['labels'], 'the chapter 10 labels')
    return {r['id']: r for r in d['rows']}


def read_inventory():
    d = load_json(SRC['inventory'], 'the Civic Line inventory in use')
    icons = {x['id']: x for x in d['icons']}
    return d, icons


def svg_file(icons, iid, kind):
    """kind 'black' for the drawing alone, 'tile' for the one-color Charcoal square tile."""
    x = icons[iid]
    if kind == 'black':
        f = SRC['black'] / x['exports']['svg_black']
    else:
        rel_ = next((t for t in x['tiles'] if 'square-charcoal' in t and t.endswith('One-Color.svg')), None)
        need(rel_, f'{iid}: no one-color Charcoal square tile in the inventory')
        f = (SRC['tiles_v6'] / rel_).resolve()
    need(f.exists(), f'{iid}: {f} is missing')
    return f


def read_form_message():
    """The email field's error message as Rule 11.15's live form writes it, so the board shows the same words."""
    t = SRC['form'].read_text()
    m = re.search(r"email:'((?:[^'\\]|\\.)*)'", t)
    need(m, 's-11-15-correct no longer holds the email field\'s message')
    return json.loads('"' + m.group(1).replace('"', '\\"') + '"')


def read_error_svg():
    t = SRC['error_svg'].read_text()
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    inner = re.search(r'<svg\b[^>]*>(.*)</svg>', t, flags=re.S)
    need(inner, 'the error mark file holds no <svg>')
    need('currentColor' in t, 'the error mark no longer draws in currentColor')
    attrs = re.search(r'<svg\b([^>]*)>', t).group(1)
    sw = re.search(r'stroke-width="([\d.]+)"', attrs)
    return re.sub(r'\s+', ' ', inner.group(1)).strip(), float(sw.group(1)) if sw else 2.0


# ------------------------------------------------------------------------------------------------ scores
def read_scores(S):
    need(isinstance(S.get('items'), list) and S['items'], 'the scores file has no items')
    for it in S['items']:
        need(isinstance(it.get('scores'), dict), f'scores: item {it.get("key")} has no scores')
        for k, _ in CRITERIA:
            need(isinstance(it['scores'].get(k), (int, float)), f'scores: item {it.get("key")} has no {k} score')
    R = S.get('rescore')
    if not R:
        note('the scores file has no rescore block yet; the board says the rescore is coming. Rerun when it lands.')
        return None, None
    meta, items = {}, None
    if isinstance(R, dict):
        meta = {k: R[k] for k in ('date', 'author', 'basis', 'summary', 'note') if isinstance(R.get(k), str)}
        if isinstance(R.get('items'), list):
            items = {i.get('key'): i for i in R['items'] if isinstance(i, dict)}
        elif isinstance(R.get('items'), dict):
            items = R['items']
        else:
            keys = {i['key'] for i in S['items']}
            items = {k: v for k, v in R.items() if k in keys and isinstance(v, dict)} or None
    elif isinstance(R, list):
        items = {i.get('key'): i for i in R if isinstance(i, dict)}
    if not items:
        warn('the rescore block holds no items this script can read; the board shows round 3 alone')
        return meta, None
    known = {i['key'] for i in S['items']}
    for k, v in items.items():
        if k not in known:
            warn(f'rescore item {k} matches no round 3 item')
        sc = v.get('scores') if isinstance(v.get('scores'), dict) else {c: v.get(c) for c, _ in CRITERIA}
        if not all(isinstance(sc.get(c), (int, float)) for c, _ in CRITERIA):
            warn(f'rescore item {k} lacks a score on one or more of the six criteria')
        v['_scores'] = sc
    return meta, items


def moved_reason(r, crit):
    for key in ('moved', 'changes', 'reasons', 'why', 'reason'):
        x = r.get(key)
        if isinstance(x, dict) and isinstance(x.get(crit), str):
            return ov(x[crit])
        if isinstance(x, str) and key in ('why', 'reason', 'changes', 'moved'):
            return ov(x)
    return None


def score_cell(v, was=None):
    low = isinstance(v, (int, float)) and v < 4
    sr = ' <span class="vh">(under 4)</span>' if low else ''
    w = f'<span class="was">was {was}</span>' if was is not None and was != v else ''
    val = '–' if v is None else str(v).rstrip('0').rstrip('.') if isinstance(v, float) else str(v)
    return f'<td class="sc{" low" if low else ""}"><span class="v">{val}</span>{sr}{w}</td>'


def item_name(it):
    nm = ov(it.get('name', it.get('key')))
    a = it.get('anchor')
    if a:
        return f'<a href="{attr(anchor_href(a))}">{esc(nm)}</a>'
    return esc(nm)


def scores_table(S, values, caption, cid, was=None, ready=None):
    head = ''.join(f'<th scope="col">{esc(n)}</th>' for _, n in CRITERIA)
    rows = ''
    for it in S['items']:
        k = it['key']
        vals = values.get(k)
        if vals is None:
            cells = f'<td colspan="{len(CRITERIA)}" class="nr">Not rescored; round 3 stands.</td>'
            rd = ''
        else:
            cells = ''.join(score_cell(vals.get(c), (was or {}).get(k, {}).get(c) if was else None) for c, _ in CRITERIA)
            r = (ready or {}).get(k)
            rd = 'Yes' if r is True else 'Not yet' if r is False else ''
        rows += f'<tr><th scope="row">{item_name(it)}</th>{cells}<td class="rd">{rd}</td></tr>'
    return (f'<div class="tw" role="region" tabindex="0" aria-labelledby="{cid}"><table class="sc-t">'
            f'<caption id="{cid}">{md(caption)}</caption><thead><tr><th scope="col">{esc(W["scores"]["item_h"])}</th>{head}'
            f'<th scope="col">{esc(W["scores"]["ready_h"])}</th></tr></thead><tbody>{rows}</tbody></table></div>')


def scores_section(S, meta, rs):
    WS = W['scores']
    r3 = {it['key']: it['scores'] for it in S['items']}
    r3_ready = {it['key']: it.get('ready') for it in S['items']}
    d = S.get('date', '')
    try:
        r3_date = words_date(datetime.date.fromisoformat(d))
    except ValueError:
        r3_date = d
    FILL['r3_date'] = r3_date
    body = paras(WS['intro'])
    body += scores_table(S, r3, fill(WS['r3_caption']), 'r3-cap', ready=r3_ready)
    lows = []
    for it in S['items']:
        for c, n in CRITERIA:
            v = it['scores'][c]
            if v < 4:
                reason = ov((it.get('reasons') or {}).get(c, ''))
                lows.append({'item': ov(it['name']), 'criterion': n, 'score': v, 'reason': reason})
    content = {'round_3': {'date': d, 'scores': r3, 'ready': r3_ready, 'under_4': lows}}
    if lows:
        body += f'<h3 class="sub4">{esc(WS["low_h"])}</h3><ul class="lines">'
        for x in lows:
            body += f'<li><b>{esc(x["item"])}, {esc(x["criterion"])} {x["score"]}.</b> {md(x["reason"])}</li>'
        body += '</ul>'
    if rs is None:
        body += f'<p class="waiting">{md(WS["waiting"])}</p>'
        content['rescore'] = None
    else:
        vals = {k: v['_scores'] for k, v in rs.items()}
        rd = {k: v.get('ready') for k, v in rs.items()}
        rs_date = ''
        if meta.get('date'):
            try:
                rs_date = ', ' + words_date(datetime.date.fromisoformat(meta['date'][:10]))
            except ValueError:
                rs_date = ', ' + meta['date']
        FILL['rs_date'] = rs_date
        body += scores_table(S, vals, fill(WS['rescore_caption']), 'rs-cap', was=r3, ready=rd)
        moved = []
        for it in S['items']:
            k = it['key']
            if k not in rs:
                continue
            for c, n in CRITERIA:
                a, b = r3[k][c], vals[k].get(c)
                if b is not None and a != b:
                    why = moved_reason(rs[k], c)
                    if not why:
                        warn(f'rescore: {k} {c} moved from {a} to {b} with no reason this script can find')
                    moved.append({'item': ov(it['name']), 'criterion': n, 'from': a, 'to': b, 'reason': why or ''})
        if moved:
            body += f'<h3 class="sub4">{esc(WS["moved_h"])}</h3><ul class="lines">'
            for x in moved:
                body += f'<li><b>{esc(x["item"])}, {esc(x["criterion"])}: {x["from"]} to {x["to"]}.</b> {md(x["reason"])}</li>'
            body += '</ul>'
        content['rescore'] = {'meta': meta, 'scores': vals, 'ready': rd, 'moved': moved}
    return (f'<section class="sec sec--minor" id="scores" aria-labelledby="scores-h"><h2 class="sec-h2" id="scores-h">{esc(WS["title"])}</h2>'
            f'{body}</section>'), content


# ------------------------------------------------------------------------------------------------ drawing helpers
ASSET_REFS = {}     # published name -> source path


def img(p, w, h, alt, cls=''):
    p = pathlib.Path(p)
    name = p.name
    need(name not in ASSET_REFS or ASSET_REFS[name] == p, f'two files share the name {name}')
    ASSET_REFS[name] = p
    c = f' class="snap {cls}"' if cls else ' class="snap"'
    return f'<img src="img/{attr(name)}" width="{w}" height="{h}" alt="{attr(copy(alt))}"{c} decoding="sync">'


ERR_INNER, ERR_SW = '', 2.0


def err_svg(size, cls):
    return (f'<svg class="mk snap {cls}" viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="{ERR_SW:g}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{ERR_INNER}</svg>')


def form_specimen(opt):
    """The field and message as Rule 11.15 builds them (s-11-15-correct's error state), with the mark in ink (A) or red (B)."""
    D = W['d1']
    cls = 'mk--ink' if opt == 'a' else 'mk--red'
    return (f'<div class="fx" data-red="working" data-red-job="error">'
            f'<p class="fx-l">{esc(D["field_label"])} <span class="chip chip--ill">Illustrative</span></p>'
            f'<div class="fx-in">{esc(D["field_value"])}</div>'
            f'<div class="fx-er">{err_svg(24, cls)}<span><b>Error:</b> {esc(FILL["message"])}</span></div></div>')


def mark_tile(opt, ground, size):
    cls = 'mk--ink' if opt == 'a' else 'mk--red'
    g = 'gr--np' if ground == 'np' else 'gr--band'
    red = ' data-red="working" data-red-job="error"' if opt == 'b' else ''
    return f'<span class="mt {g}"{red}>{err_svg(size, cls)}</span>'


def ratio_line(v):
    under = float(v) < 3
    return (f'<span class="ratio{" ratio--under" if under else ""}">{v} to 1</span>'
            + (' <span class="under">under 3 to 1</span>' if under else ''))


# ------------------------------------------------------------------------------------------------ sections
def link_out(text, href):
    return f'<a href="{attr(href)}">{esc(text)}</a>'


def cover(reader_url, pending):
    pg = ''
    for name, key, text in W['pages']:
        if key == 'chapters':
            h = link_out(name, CHAPTERS_URL)
        elif key == 'reader':
            h = esc(name) if pending else link_out(name, reader_url)
        else:
            h = esc(name)
        pg += f'<li><b>{h}</b>, {md(fill(text))}</li>'
    toc = [('d1', W['d1']['title']), ('d2', W['d2']['title']), ('scores', W['scores']['title']),
           ('calls', W['calls']['title']), ('answered', W['answered']['title']), ('carried', W['carried']['title']),
           ('reader', W['reader']['title'])]
    toc_html = ''.join(f'<li><a href="#{k}">{esc(t)}</a></li>' for k, t in toc)
    return f'''<header class="cover">
<p class="mast"><b>Oath &amp; Action</b><span class="label">{esc(W["kicker"])}</span></p>
<p class="label for">{esc(fill(W["for_line"]))}</p>
<h1>{esc(W["title"])}</h1>
<div class="cover-grid"><div class="deck">{paras(W["deck"], "intro")}
<h2 class="sub4">{esc(W["pages_h"])}</h2><ul class="pages">{pg}</ul></div>
<aside class="ask" aria-labelledby="ask-h"><h2 id="ask-h" class="sub4">{esc(W["reply_h"])}</h2>
<p class="q" id="sample-reply">{md(W["sample_reply"])}</p>
<div class="copy-row"><button type="button" class="btn-copy" data-copy="sample-reply" data-status="reply-status">{esc(W["copy_reply"])}</button>
<span class="status" id="reply-status" role="status" aria-live="polite"></span></div></aside></div>
<nav class="toc" aria-labelledby="toc-h"><h2 class="label" id="toc-h">{esc(W["toc_h"])}</h2><ol>{toc_html}</ol></nav>
</header>'''


def rec_block(D, extra_fill=None):
    return (f'<div class="decide"><div class="rec"><h3 class="label">{esc(W["rec_h"])}</h3>{paras(D["rec"])}</div>'
            f'<div class="approve"><h3 class="label">{esc(W["approve_h"])}</h3><p class="q">{md(D["approve"])}</p></div></div>')


def decision_1(figs):
    D = W['d1']
    FILL.update({'enlarge_words': num_words(ENLARGE), 'enlarged_px': 24 * ENLARGE, 'enlarged_line': f'{ERR_SW * ENLARGE:g}'})
    head = (f'<div class="sec-top"><p class="label">{esc(D["label"])}</p>{codes(D["codes"])}</div>'
            f'<h2 class="sec-h" id="d1-h">{esc(D["title"])}</h2>{paras(D["lede"], "intro")}')

    def opt_head(o):
        return (f'<div class="oh"><h3 class="oh-h">{esc(D[o + "_h"])}</h3><p>{md(D[o + "_text"])}</p></div>')
    rows = f'<div class="cmp-row cmp-row--h"><div class="cmp-lab" aria-hidden="true"></div>{opt_head("a")}{opt_head("b")}</div>'

    def row(label, cells, cap=''):
        c = ''.join(f'<div class="cmp-cell"><p class="cmp-o">{esc(D[o + "_h"])}</p>{x}</div>' for o, x in zip(('a', 'b'), cells))
        cp = f'<p class="caption">{md(fill(cap))}</p>' if cap else ''
        return f'<div class="cmp-row"><div class="cmp-lab"><h4 class="rl">{esc(fill(label))}</h4>{cp}</div>{c}</div>'
    forms = [f'<div class="stage stage--np stage--phone">{form_specimen(o)}</div>' for o in ('a', 'b')]
    rows += row(D['row_form'], forms, D['row_form_cap'])

    def alone(o, size):
        np_v = figs['a_np'] if o == 'a' else figs['b_np']
        band_v = figs['a_band'] if o == 'a' else figs['b_band']
        return ('<div class="alone">'
                f'<figure class="al">{mark_tile(o, "np", size)}<figcaption><span class="al-g">{esc(D["on_np"])}</span>{ratio_line(np_v)}</figcaption></figure>'
                f'<figure class="al">{mark_tile(o, "band", size)}<figcaption><span class="al-g">{esc(D["on_band"])}</span>{ratio_line(band_v)}</figcaption></figure>'
                '</div>')
    rows += row(D['row_alone'], [alone('a', 24), alone('b', 24)])
    rows += row(D['row_enl'], [alone('a', 24 * ENLARGE), alone('b', 24 * ENLARGE)], D['row_enl_cap'])
    note_ = f'<p class="cnote">{md(D["contrast_note"])}</p>'
    body = f'<div class="card"><div class="cmp">{rows}</div>{note_}{rec_block(D)}</div>'
    return f'<section class="sec" id="d1" aria-labelledby="d1-h">{head}{body}</section>'


def decision_2(inv, icons, labels):
    D = W['d2']
    x = icons[TILE_SUBJECT]
    name = labels.get(TILE_SUBJECT, {}).get('label') or x['label']
    sq = x['tile_scale']['square']
    one, two = x['tile_min_px']['one-color'], x['tile_min_px']['two-color']
    need(one['square'] == 48, f'{TILE_SUBJECT} no longer takes a 48 px one-color tile')
    n94 = sum(1 for i in inv['icons'] if i['tile_min_px']['one-color']['square'] == 48)
    n_all = len(inv['icons'])
    p105 = quote_10_5()
    if p105 and (str(n94) not in p105):
        warn(f'Rule 10.5\'s exception names no {n94}, the count of drawings whose one-color tile starts at 48 px')
    other = {k: two[k] for k in ('square', 'rounded', 'circle')}
    FILL.update({'subject': name, 'n_all': n_all, 'sq': other['square'], 'rd': other['rounded'], 'ci': other['circle']})
    tile_f, black_f = svg_file(icons, TILE_SUBJECT, 'tile'), svg_file(icons, TILE_SUBJECT, 'black')
    inner48, inner72 = round(48 * sq), round(other['square'] * sq)

    def fig(inner, cap, box):
        return f'<figure class="tf"><span class="tbox" style="--tb:{box}px">{inner}</span><figcaption>{md(cap)}</figcaption></figure>'
    t48 = fig(img(tile_f, 48, 48, f'{name} on a Charcoal tile, 48 px'), D['tile_cap'].format(px=48, inner=inner48), 48)
    a48 = fig(img(black_f, 48, 48, f'{name}, the drawing alone at 48 px'), D['alone48_cap'], 48)
    a32 = fig(img(black_f, 32, 32, f'{name}, the drawing alone at 32 px'), D['alone32_cap'], 48)
    t72 = fig(img(tile_f, other['square'], other['square'], f'{name} on a Charcoal tile, {other["square"]} px'),
              D['other_cap'].format(px=other['square'], inner=inner72), other['square'])
    head = (f'<div class="sec-top"><p class="label">{esc(D["label"])}</p>{codes(D["codes"])}</div>'
            f'<h2 class="sec-h" id="d2-h">{esc(D["title"])}</h2>{paras(D["lede"], "intro")}')
    ordinal = ['first', 'second', 'third', 'fourth', 'fifth'][rule_paras('10.5').index(p105)] if p105 else ''
    quote = f'<blockquote class="rq"><p>{md(p105)}</p><footer>{md(f"Rule 10.5, {ordinal} paragraph")}</footer></blockquote>' if p105 else ''
    stage = (f'<div class="tiles-fig"><div class="stage stage--np tiles"><div class="tset" style="--n:3">{t48}{a48}{a32}</div></div>'
             f'<div class="stage stage--np tiles tiles--other"><p class="t-oh">{esc(D["other_h"])}</p><div class="tset" style="--n:1;--w:11.5rem">{t72}</div></div></div>'
             f'<p class="caption fig-cap">{md(fill(D["fig_cap"]))}</p>')
    body = f'<div class="card">{quote}{stage}{rec_block(D)}</div>'
    content = {'subject': {'id': TILE_SUBJECT, 'name': name}, 'tile_scale_square': sq, 'one_color_min': one,
               'two_color_min': two, 'drawing_in_48_tile_px': 48 * sq, 'drawing_in_72_tile_px': other['square'] * sq,
               'n_one_color_from_48': n94, 'n_drawings': n_all, 'rule_10_5_quote': p105,
               'files': [str(tile_f.relative_to(ROOT)), str(black_f.relative_to(ROOT))]}
    return f'<section class="sec" id="d2" aria-labelledby="d2-h">{head}{body}</section>', content


def calls_section(labels, log):
    C = W['calls']
    cards = []
    # the pillar row
    R = C['row']
    q91 = quote_09_1()
    soc = quote_social()
    soc_html = (f'<p>{md(R["social"])}</p><blockquote class="rq"><p><b>Left out.</b> {md(soc)}</p>'
                f'<footer>{link_out("The social card, in the identity proofs", anchor_href("proofs-social-card"))}</footer></blockquote>') if soc else ''
    cards.append(('row', R['h'], R['codes'],
                  f'<p>{md(R["text"])}</p><blockquote class="rq"><p>{md(q91)}</p><footer>{md("Rule 09.1")}</footer></blockquote>{soc_html}'))
    # the five look-alikes
    F = C['five']
    p109, s109 = quote_10_9()
    figs = ''
    for i in LOOKALIKES:
        lab = labels.get(i, {}).get('label') or i
        f = SRC['black'] / next((p.name for p in SRC['black'].glob(f'*Civic-Line-{i}-*-Black.svg')), 'missing')
        need(f.exists(), f'{i}: no Black file in civic-line-v6/black')
        figs += f'<figure class="la">{img(f, 24, 24, f"{lab}, at 24 px")}<figcaption>{esc(lab)} <span class="nw id">{esc(i)}</span></figcaption></figure>'
    cards.append(('five', F['h'], F['codes'],
                  f'<p>{md(F["text"])}</p><blockquote class="rq"><p>{md(s109 or "")}</p><footer>{md("Rule 10.9")}</footer></blockquote>'
                  f'<div class="stage stage--np la-row">{figs}</div><p class="caption">{md(F["cap"])}</p>'))
    # the reforms
    Rf = C['reforms']
    check_10_8()
    check_11_16()
    cards.append(('reforms', Rf['h'], Rf['codes'], paras(Rf['text'])))
    # the tokens download
    T = C['tokens']
    row = log.get('D2-964', '')
    m = re.search(r'`(\d{8}_[\w-]+\.zip)`', row)
    need(m, 'D2-964 in the decision log names no zip file')
    FILL['zip'] = m.group(1)
    ZIPS.add(m.group(1))
    cards.append(('tokens', T['h'], T['codes'],
                  f'<p>{md(fill(T["text"]))}</p><p>{link_out(T["link"], anchor_href("colophon"))}</p>'))
    lis = ''.join(f'<li class="call" id="call-{k}"><article aria-labelledby="call-{k}-h"><div class="call-top">'
                  f'<h3 class="call-h" id="call-{k}-h">{esc(h)}</h3>{codes(c)}</div>{b}</article></li>' for k, h, c, b in cards)
    html_ = (f'<section class="sec sec--minor" id="calls" aria-labelledby="calls-h"><h2 class="sec-h2" id="calls-h">{esc(C["title"])}</h2>'
             f'<p class="intro">{md(C["intro"])}</p><ul class="calls">{lis}</ul></section>')
    content = {'rule_09_1_quote': q91, 'social_left_out': soc, 'rule_10_9_paragraph': p109, 'rule_10_9_line': s109,
               'lookalikes': [{'id': i, 'label': labels.get(i, {}).get('label')} for i in LOOKALIKES], 'zip': FILL['zip']}
    return html_, content


def list_section(key, sid):
    A = W[key]
    lis = ''.join(f'<li><p>{md(t)}</p>{codes(c)}</li>' for c, t in A['lines'])
    return (f'<section class="sec sec--minor" id="{sid}" aria-labelledby="{sid}-h"><h2 class="sec-h2" id="{sid}-h">{esc(A["title"])}</h2>'
            f'<p class="intro">{md(A["intro"])}</p><ul class="log">{lis}</ul></section>')


def reader_section(url, pending, invite_filled):
    Rd = W['reader']
    shown = esc(url) if pending else f'<a href="{attr(url)}">{esc(url)}</a>'
    addr = (f'<p class="addr"><span class="mono" id="reader-url">{shown}</span></p>'
            + (f'<p class="pend">{md(Rd["pending"])}</p>' if pending else ''))
    inv = ''.join(f'<p>{esc(x)}</p>' for x in invite_filled)
    plain = '\n\n'.join(copy(x) for x in invite_filled)
    return f'''<section class="sec" id="reader" aria-labelledby="reader-h"><h2 class="sec-h" id="reader-h">{esc(Rd["title"])}</h2>
<div class="panel">{paras(Rd["text"])}
<h3 class="label">{esc(Rd["address_h"])}</h3>{addr}
<h3 class="label">{esc(Rd["invite_h"])}</h3><div class="invite" id="invite">{inv}</div>
<div class="copy-row"><button type="button" class="btn-copy" data-copy="invite" data-text="{attr(plain)}" data-status="invite-status">{esc(Rd["copy"])}</button>
<span class="status" id="invite-status" role="status" aria-live="polite"></span></div></div></section>'''


# ------------------------------------------------------------------------------------------------ page
CSS = r'''
/* Board B, the decisions board. The brand's shell on Newsprint: tokens.css grid margins, title, section, H3 and H4 styles,
   hairlines in Stone, White cards for words, Newsprint stages that hold specimens at actual size, one Prussian panel for
   the reader check. The board has no red of its own: Pillar Red appears only inside the error specimens. One light look
   by design, on the brand's own surfaces, with every color set explicitly. */
:root{--m:max(var(--oa-layout-grid-phone-small-margin),env(safe-area-inset-left,0px));--mr:max(var(--oa-layout-grid-phone-small-margin),env(safe-area-inset-right,0px));--max:78rem;
--ink:var(--oa-color-text-primary-on-newsprint);--ink-2:var(--oa-color-text-secondary-on-newsprint);
--hair:var(--oa-color-border-hairline-on-newsprint);--strong:var(--oa-color-border-strong-on-newsprint);
--white:var(--oa-color-surface-white);--np:var(--oa-color-surface-newsprint);--wink-2:var(--oa-color-text-secondary-on-white);
--band:var(--oa-color-state-error-band-on-newsprint);--mono:ui-monospace,"SFMono-Regular",Menlo,Consolas,monospace;color-scheme:light}
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
.card :focus-visible,.call :focus-visible,.ask :focus-visible,.tw:focus-visible{outline-color:var(--oa-color-focus-ring-on-white)}
.panel :focus-visible{outline-color:var(--oa-color-focus-ring-on-prussian)}
p{margin:0 0 var(--oa-space-200);max-width:var(--oa-layout-measure-body-max);text-wrap:pretty}
.vh{position:absolute!important;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
[hidden]{display:none!important}
.nw,a[href*="#rule-"]{white-space:nowrap}
.board{max-width:calc(var(--max) + var(--m) + var(--mr));margin:0 auto;padding-left:var(--m);padding-right:var(--mr);padding-block:0 var(--oa-space-1300)}
.label{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0}
.caption{font:var(--oa-type-caption);color:var(--ink-2)}
.intro{font:var(--oa-type-intro);max-width:var(--oa-layout-measure-intro-max)}
.sub4{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:var(--oa-space-500) 0 var(--oa-space-200);text-wrap:balance}
.codes{font:var(--oa-type-caption);color:var(--ink-2);margin:0;font-variant-numeric:tabular-nums}
.card .codes,.call .codes{color:var(--wink-2)}
.chip{display:inline-block;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;border:var(--oa-border-width-hairline) solid var(--strong);padding:0 6px;white-space:nowrap;vertical-align:.1em;font-size:.8125rem}
/* cover */
.mast{max-width:none;display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-100) var(--oa-space-300);
  padding:var(--oa-space-300) 0 var(--oa-space-200);margin:0;border-bottom:var(--oa-border-width-rule) solid var(--strong)}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.01em;white-space:nowrap}
.for{margin-top:var(--oa-space-800)}
h1{font:var(--oa-type-title);letter-spacing:var(--oa-type-title-letter-spacing);margin:var(--oa-space-200) 0 var(--oa-space-500);max-width:12ch;text-wrap:balance}
.cover-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-500) var(--oa-space-800);align-items:start}
@media (min-width:64em){.cover-grid{grid-template-columns:minmax(0,7fr) minmax(0,4fr)}}
.deck .sub4{margin-top:var(--oa-space-400)}
.pages{list-style:none;margin:0;padding:0;max-width:var(--oa-layout-measure-intro-max);border-top:var(--oa-border-width-hairline) solid var(--hair)}
.pages li{padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair);max-width:var(--oa-layout-measure-intro-max)}
.ask{background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-300)}
.ask .sub4{margin-top:0}
.q{font:italic 400 1.25rem/1.45 var(--oa-font-family-quote);margin:0 0 var(--oa-space-200)}
.copy-row{display:flex;flex-wrap:wrap;align-items:center;gap:var(--oa-space-150) var(--oa-space-200)}
.btn-copy{font:var(--oa-type-ui);min-height:var(--oa-size-target-touch);padding:0 var(--oa-space-300);border:0;border-radius:0;cursor:pointer;
  background:var(--oa-color-action-primary-fill-on-white);color:var(--oa-color-action-primary-label-on-white)}
.btn-copy:hover{background:var(--oa-color-action-primary-fill-hover-on-white)}
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
.sec > .intro + .card,.sec > .intro + .calls,.sec > .intro + .log,.sec > .intro + .panel{margin-top:var(--oa-space-400)}
.card{background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-300) var(--oa-space-200);min-width:0}
@media (min-width:48em){.card{padding:var(--oa-space-400) var(--oa-space-500)}}
.card .caption,.card .label{color:var(--wink-2)}
/* stages that hold specimens at actual size */
.stage{background:var(--np);color:var(--ink);min-width:0}
.stage .caption,.stage figcaption{color:var(--ink-2)}
img{display:block;max-width:none}
/* decision 1: the comparison, row by row */
.cmp{display:grid;gap:0}
.cmp-row{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-200) var(--oa-space-400);padding:var(--oa-space-300) 0;border-top:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white)}
.cmp-row--h{border-top:0;padding-top:0}
.cmp-row--h .cmp-lab{display:none}
@media (min-width:72em){.cmp-row{grid-template-columns:15rem minmax(0,1fr) minmax(0,1fr)}.cmp-row--h .cmp-lab{display:block}.cmp-o{display:none}}
@media (max-width:71.99em){.cmp-row--h{grid-template-columns:repeat(auto-fit,minmax(15rem,1fr))}}
.oh{border-top:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding-top:var(--oa-space-150)}
.oh-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0 0 var(--oa-space-100)}
.oh p{font:var(--oa-type-body-small);margin:0}
.rl{font:var(--oa-type-ui);font-weight:700;margin:0 0 var(--oa-space-100)}
.cmp-lab .caption{margin:0}
.cmp-cell{min-width:0}
.cmp-o{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);margin:0 0 var(--oa-space-100)}
.stage--phone{width:100%;max-width:360px;padding:20px 16px 24px}
.fx{font:var(--oa-type-body)}
.fx-l{font:var(--oa-type-ui);font-weight:600;margin:0;display:flex;flex-wrap:wrap;align-items:baseline;gap:var(--oa-space-100)}
.fx-in{display:flex;align-items:center;min-height:48px;margin-top:6px;padding:0 12px 0 9px;border:1px solid var(--oa-color-border-strong-on-newsprint);
  border-left:4px solid var(--oa-color-state-error-mark-on-newsprint);background:var(--white);color:var(--ink);font:var(--oa-type-body);overflow-wrap:anywhere}
.fx-er{display:grid;grid-template-columns:24px minmax(0,1fr);gap:8px;margin-top:8px;padding:10px 12px;background:var(--band);
  color:var(--oa-color-state-error-text-on-newsprint);border-left:4px solid var(--oa-color-state-error-mark-on-newsprint);font:var(--oa-type-body-small)}
.fx-er .mk{display:block;margin-top:-1px}
.fx-er b{font-weight:700}
.mk--ink{color:var(--oa-color-state-error-text-on-newsprint)}
.mk--red{color:var(--oa-color-state-error-mark-on-newsprint)}
.alone{display:flex;flex-wrap:wrap;gap:var(--oa-space-200) var(--oa-space-300);align-items:flex-start}
.al{margin:0;display:grid;gap:var(--oa-space-100);justify-items:start}
.mt{display:inline-flex;align-items:center;justify-content:center;padding:16px}
.gr--np{background:var(--np)}.gr--band{background:var(--band)}
.mt .mk{display:block}
.al figcaption{font:var(--oa-type-caption);color:var(--wink-2);display:grid}
.al-g{font-weight:600;color:var(--oa-color-text-primary-on-white)}
.ratio{font-variant-numeric:tabular-nums;color:var(--oa-color-text-primary-on-white)}
.ratio--under{border:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);padding:0 4px;font-weight:700;justify-self:start}
.under{font-weight:600}
.cnote{font:var(--oa-type-body-small);color:var(--wink-2);margin:var(--oa-space-200) 0 0;max-width:var(--oa-layout-measure-intro-max)}
/* recommendation and approval */
.decide{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300) var(--oa-space-600);margin-top:var(--oa-space-400);border-top:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);padding-top:var(--oa-space-300)}
@media (min-width:64em){.decide{grid-template-columns:minmax(0,3fr) minmax(0,2fr)}}
.decide .label{margin-bottom:var(--oa-space-100)}
.rec p{max-width:var(--oa-layout-measure-intro-max)}
.approve .q{font-size:1.375rem}
/* decision 2: tiles */
.rq{margin:0 0 var(--oa-space-300);padding:var(--oa-space-050) 0 var(--oa-space-050) var(--oa-space-200);border-left:var(--oa-border-width-rule) solid var(--oa-color-border-strong-on-white);max-width:var(--oa-layout-measure-intro-max)}
.rq p{margin:0 0 var(--oa-space-100)}
.rq footer{font:var(--oa-type-caption);color:var(--wink-2)}
.tiles-fig{display:flex;flex-wrap:wrap;align-items:flex-start;gap:var(--oa-space-200)}
.tiles{padding:var(--oa-space-200) var(--oa-space-200) var(--oa-space-150)}
@media (min-width:48em){.tiles{padding:var(--oa-space-300) var(--oa-space-300) var(--oa-space-200)}}
.tset{display:grid;grid-template-columns:repeat(var(--n),minmax(0,var(--w,8.5rem)));align-items:start;gap:var(--oa-space-200)}
@media (min-width:48em){.tset{gap:var(--oa-space-300) var(--oa-space-400)}}
.tf{margin:0;display:grid;gap:var(--oa-space-100);justify-items:start;align-content:start;min-width:0}
.tbox{display:flex;align-items:flex-end;height:var(--tb)}
.tf figcaption{font:var(--oa-type-caption);color:var(--ink-2)}
.tiles--other{border-left:var(--oa-border-width-rule) solid var(--strong)}
.t-oh{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--ink-2);margin:0 0 var(--oa-space-150)}
.fig-cap{margin:var(--oa-space-150) 0 0}
/* scores */
.tw{position:relative;overflow-x:auto;background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);margin:var(--oa-space-300) 0 0}
table{border-collapse:collapse;width:100%;font:var(--oa-type-body-small)}
table.sc-t{min-width:46rem}
caption{caption-side:top;text-align:left;padding:var(--oa-space-150) var(--oa-space-200);font:var(--oa-type-body-small);color:var(--wink-2);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white)}
th,td{text-align:left;vertical-align:top;padding:var(--oa-space-100) var(--oa-space-150);border-bottom:var(--oa-border-width-hairline) solid var(--oa-color-tint-stone-n88)}
thead th{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:var(--wink-2);background:var(--oa-color-tint-white-n55);vertical-align:bottom}
tbody th{font-weight:600;min-width:12rem}
td.sc,td.rd{text-align:center;font-variant-numeric:tabular-nums}
td.sc .v{display:inline-block;min-width:1.9em;font-weight:600}
td.low .v{box-shadow:inset 0 0 0 var(--oa-border-width-rule) var(--oa-color-border-strong-on-white);font-weight:800}
td.sc .was{display:block;font:var(--oa-type-caption);color:var(--wink-2)}
td.nr{color:var(--wink-2)}
.lines{margin:0;padding:0 0 0 1.1em;max-width:var(--oa-layout-measure-intro-max)}
.lines li{margin:0 0 var(--oa-space-150)}
.waiting{margin-top:var(--oa-space-300);font:var(--oa-type-ui);font-weight:600;border-left:var(--oa-border-width-bar) solid var(--oa-color-palette-charcoal);padding:var(--oa-space-100) var(--oa-space-200);max-width:var(--oa-layout-measure-intro-max)}
/* calls */
.calls{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-300)}
@media (min-width:64em){.calls{grid-template-columns:repeat(2,minmax(0,1fr))}}
.call{background:var(--white);border:var(--oa-border-width-hairline) solid var(--oa-color-border-hairline-on-white);padding:var(--oa-space-300) var(--oa-space-200);min-width:0}
@media (min-width:48em){.call{padding:var(--oa-space-300) var(--oa-space-400)}}
.call-top{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:var(--oa-space-050) var(--oa-space-200);margin-bottom:var(--oa-space-150)}
.call-h{font:var(--oa-type-h4);letter-spacing:var(--oa-type-h4-letter-spacing);margin:0;text-wrap:balance}
.call p{font:var(--oa-type-body-small)}
.call .rq p{font:var(--oa-type-body-small)}
.call .caption{font:var(--oa-type-caption);color:var(--wink-2)}
.la-row{display:grid;grid-template-columns:repeat(auto-fill,minmax(7.5rem,1fr));align-items:start;gap:var(--oa-space-200) var(--oa-space-200);padding:var(--oa-space-200);margin-bottom:var(--oa-space-100)}
.la{margin:0;display:grid;gap:var(--oa-space-100);justify-items:start;align-content:start}
.la figcaption{font:var(--oa-type-caption);color:var(--ink-2)}
.la .id{display:block;font-variant-numeric:tabular-nums}
/* answered and carried */
.log{list-style:none;margin:0;padding:0;border-top:var(--oa-border-width-hairline) solid var(--hair);max-width:56rem}
.log li{display:grid;grid-template-columns:minmax(0,1fr);gap:var(--oa-space-050) var(--oa-space-400);padding:var(--oa-space-150) 0;border-bottom:var(--oa-border-width-hairline) solid var(--hair)}
@media (min-width:48em){.log li{grid-template-columns:minmax(0,1fr) 12rem}.log .codes{text-align:right}}
.log p{margin:0}
/* the reader check */
.panel{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);padding:var(--oa-space-400) var(--oa-space-200)}
@media (min-width:48em){.panel{padding:var(--oa-space-500)}}
.panel p{color:var(--oa-color-text-primary-on-prussian);max-width:var(--oa-layout-measure-intro-max)}
.panel .label{color:var(--oa-color-text-secondary-on-prussian);margin:var(--oa-space-400) 0 var(--oa-space-100)}
.addr{margin:0}.mono{font:500 1rem/1.5 var(--mono);overflow-wrap:anywhere;user-select:all}
.pend{font:var(--oa-type-body-small);margin:var(--oa-space-100) 0 0}
.invite{background:var(--np);color:var(--ink);padding:var(--oa-space-300);max-width:44rem;margin-bottom:var(--oa-space-200)}
.invite p{color:var(--ink);font:italic 400 1.1875rem/1.5 var(--oa-font-family-quote);margin:0 0 var(--oa-space-200);overflow-wrap:anywhere}
.invite p:last-child{margin:0}
.panel .btn-copy{background:var(--oa-color-action-primary-fill-on-prussian);color:var(--oa-color-action-primary-label-on-prussian)}
.panel .btn-copy:hover{background:var(--oa-color-action-primary-fill-hover-on-prussian)}
.panel .status{color:var(--oa-color-text-primary-on-prussian)}
.foot{margin-top:var(--oa-space-1000);padding-top:var(--oa-space-200);border-top:var(--oa-border-width-hairline) solid var(--hair)}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto!important}}
'''

JS = r'''
(function () {
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  // Each mark and drawing sits on whole CSS pixels, so a 1x screen draws it as its master is drawn (D2-565).
  function snap() {
    $$('.snap').forEach(function (el) { el.style.transform = ''; });
    $$('.snap').forEach(function (el) {
      var r = el.getBoundingClientRect(); if (!r.width) return;
      var dx = Math.round(r.left) - r.left, dy = Math.round(r.top + window.scrollY) - (r.top + window.scrollY);
      if (Math.abs(dx) > 0.001 || Math.abs(dy) > 0.001) el.style.transform = 'translate(' + dx.toFixed(3) + 'px,' + dy.toFixed(3) + 'px)';
    });
  }
  var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(snap, 120); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(snap);
  window.addEventListener('load', snap);
  snap();
  // Copy: the host's clipboard when it allows it, else the browser's own copy of the selected text, else a prompt to copy.
  function selectNode(el) {
    try { var r = document.createRange(); r.selectNodeContents(el); var s = window.getSelection(); s.removeAllRanges(); s.addRange(r); return true; } catch (e) { return false; }
  }
  $$('.btn-copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var src = document.getElementById(b.getAttribute('data-copy'));
      var st = document.getElementById(b.getAttribute('data-status'));
      var text = b.getAttribute('data-text') || (src ? src.innerText.trim() : '');
      var done = function () { st.textContent = 'Copied.'; };
      var fall = function () {
        var ok = false;
        if (src && selectNode(src)) { try { ok = document.execCommand('copy'); } catch (e) { ok = false; } }
        st.textContent = ok ? 'Copied.' : 'The text is selected. Press Ctrl or Command and C to copy it.';
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


def build_page(sections, built):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{TITLE}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="chart-views" content="overview">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800&family=Inter:wght@400;500;600;700&family=Lora:ital@1&display=swap" rel="stylesheet">
<style>{strip_css(TOKENS.read_text())}
{strip_css(CSS)}</style></head>
<body><main class="board" data-view-root="overview">
{sections}
<p class="foot caption">{esc(fill(W["foot"]))}</p>
</main>
<script>{JS}</script></body></html>'''


def visible_text(page):
    t = re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S)
    return html.unescape(re.sub(r'<[^>]+>', ' ', t))


def checks(page):
    text = visible_text(page)
    need('—' not in text, 'an em dash on the board: ' + text[max(0, text.find('—') - 60):text.find('—') + 20])
    if '–' in text.replace('<span class="v">–', ''):
        i = text.find('–')
        warn('an en dash on the board: ' + text[max(0, i - 40):i + 20])
    flagged = sorted({w for w in FLAGGED if re.search(rf'\b{w}\b', text, flags=re.I)})
    if flagged:
        warn('flagged words on the board: ' + ', '.join(flagged))
    if 'answers to its people' in text and TAGLINE not in text.replace('’', "'"):
        raise BoardError('the tagline is quoted inexactly (H01)')
    # studio codes stay in the small "codes" lines
    no_codes = re.sub(r'<p class="codes">.*?</p>', ' ', re.sub(r'<(script|style)\b.*?</\1>', '', page, flags=re.S), flags=re.S)
    stray = sorted(set(re.findall(r'\b(?:DR|D2)-\d+\b', html.unescape(re.sub(r'<[^>]+>', ' ', no_codes)))))
    if stray:
        warn('decision codes in the reader\'s way: ' + ', '.join(stray))
    for pat in (r'/home/', r'/tmp/', r'file:', r'\bwork/', r'scratchpad', r'@anthropic', r'\.local\b'):
        if re.search(pat, page):
            warn(f'a private path or address on the board ({pat})')
    hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', page))
    extra = hosts - {'fonts.googleapis.com', 'fonts.gstatic.com', 'claude.ai'}
    if extra:
        warn('links or loads to hosts other than claude.ai and Google Fonts: ' + ', '.join(sorted(extra)))
    return text


def main():
    global GUIDE_IDS, ERR_INNER, ERR_SW
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--strict', action='store_true')
    ap.add_argument('--reader-check-url', default=f'https://claude.ai/artifact/{PLACEHOLDER}')
    ap.add_argument('--publish', type=pathlib.Path, default=DEF_PUBLISH)
    ap.add_argument('--scratch', type=pathlib.Path, default=DEF_SCRATCH)
    ap.add_argument('--out', type=pathlib.Path, default=DEF_OUT)
    ap.add_argument('--guide', type=pathlib.Path, help='a built chapters page; every anchor the board links must be on it')
    ap.add_argument('--scores', type=pathlib.Path, default=SRC['scores'], help='the scores file (default: the round 3 file)')
    a = ap.parse_args()
    url = a.reader_check_url.strip()
    need(re.fullmatch(r'https://claude\.ai/(?:code/)?artifact/[\w-]+', url), f'--reader-check-url {url} is not a claude.ai artifact address')
    pending = PLACEHOLDER in url
    if pending:
        note('the reader check address is the placeholder; the main session reruns with the real address at publish')
    if a.guide:
        need(a.guide.exists(), f'--guide {a.guide} does not exist')
        GUIDE_IDS = set(re.findall(r'\bid="([^"]+)"', a.guide.read_text()))
    need('—' not in json.dumps(W, ensure_ascii=False), 'the board\'s words hold an em dash (W21)')
    read_chapters()
    tok, tok_names = read_tokens()
    figs = {
        'a_band': fmt_ratio(contrast(tok['ink'], tok['band'])), 'a_np': fmt_ratio(contrast(tok['ink'], tok['newsprint'])),
        'b_band': fmt_ratio(contrast(tok['red'], tok['band'])), 'b_np': fmt_ratio(contrast(tok['red'], tok['newsprint'])),
    }
    check_11_15(figs)
    FILL.update(figs)
    ERR_INNER, ERR_SW = read_error_svg()
    FILL['message'] = read_form_message()
    S = load_json(a.scores, 'the creative director\'s scores')
    meta, rs = read_scores(S)
    labels = read_labels()
    inv, icons = read_inventory()
    for i in LOOKALIKES + [TILE_SUBJECT]:
        need(i in icons, f'{i} is not in the inventory in use')
    log = read_log()
    built = datetime.datetime.now(datetime.timezone.utc)
    FILL.update({'built_date': words_date(built), 'built_time': words_time(built), 'chapters_version': CHAPTERS_VERSION})
    invite_raw, invite = read_invitation(url)

    # every code the board prints is in the decision log
    printed = set()
    for s in json.dumps(W, ensure_ascii=False).split('"'):
        printed |= set(re.findall(r'\b(?:DR|D2)-\d+\b', s))
    for c in sorted(printed):
        if c not in log:
            warn(f'{c} is printed on the board and missing from the decision log')
    for c, _ in W['answered']['lines']:
        if c in log and 'Dustin' not in log[c]:
            warn(f'{c} is listed as answered this chat, and its log row names no answer from Dustin')

    s_cover = cover(url, pending)
    s_d1 = decision_1(figs)
    s_d2, d2_content = decision_2(inv, icons, labels)
    s_scores, sc_content = scores_section(S, meta or {}, rs)
    s_calls, calls_content = calls_section(labels, log)
    s_ans = list_section('answered', 'answered')
    s_car = list_section('carried', 'carried')
    s_rd = reader_section(url, pending, invite)
    page = build_page('\n'.join([s_cover, s_d1, s_d2, s_scores, s_calls, s_ans, s_car, s_rd]), built)
    for o in OVERRIDES:
        if not o[2]:
            warn(f'a copy edit matches nothing in the scores file: "{o[0][:70]}"')
    text = checks(page)

    # the repository copy and its images
    out_dir = a.out.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    idir = out_dir / 'img'
    if idir.exists():
        shutil.rmtree(idir)
    idir.mkdir()
    for name, p in sorted(ASSET_REFS.items()):
        shutil.copy2(p, idir / name)
    a.out.write_text(page)
    img_bytes = sum(p.stat().st_size for p in ASSET_REFS.values())
    total = len(page.encode()) + img_bytes
    need(total < LIMIT, f'the board and its files come to {total / 1e6:.1f} MB, over 16 MB')
    # a check copy for dataviz_check.js with captures, in the scratchpad
    chk = a.scratch / 'check-copy'
    if chk.exists():
        shutil.rmtree(chk)
    (chk / 'img').mkdir(parents=True)
    for name, p in ASSET_REFS.items():
        shutil.copy2(p, chk / 'img' / name)
    (chk / a.out.name).write_text(page)
    # the publish copy: no document skeleton (D2-317), files under img/
    head, body = re.split(r'</head>\s*<body>', page, maxsplit=1)
    head = head.split('<head>', 1)[1]
    head = head.replace('<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n', '')
    head = head.replace(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n', '')
    body = re.sub(r'</body>\s*</html>\s*$', '', body)
    a.publish.mkdir(parents=True, exist_ok=True)
    pdir = a.publish / 'img'
    if pdir.exists():
        shutil.rmtree(pdir)
    pdir.mkdir()
    files = {}
    for name, p in sorted(ASSET_REFS.items()):
        shutil.copy2(p, pdir / name)
        files[f'img/{name}'] = str(pdir / name)
    pub_html = a.publish / a.out.name
    pub_html.write_text(f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
                        + head + '<script>document.documentElement.lang="en";</script>' + body)
    (a.publish / 'files.json').write_text(json.dumps(files, indent=1))
    # the content record: every string and figure the board prints, and where each fact came from
    content = {
        'built': built.isoformat(), 'board': show(a.out),
        'chapters_page': {'url': CHAPTERS_URL, 'version': CHAPTERS_VERSION},
        'reader_check': {'url': url, 'placeholder': pending, 'invitation_source': invite_raw, 'invitation': invite},
        'words': W, 'filled': {k: v for k, v in FILL.items()},
        'decision_1': {'contrast': figs, 'colors': tok, 'tokens': tok_names, 'enlargement': ENLARGE,
                       'rule_11_15_why': ' '.join(RULES['11.15']['why']['text']) if isinstance(RULES['11.15']['why'].get('text'), list) else RULES['11.15']['why'].get('text'),
                       'mark_file': str(SRC['error_svg'].relative_to(ROOT))},
        'decision_2': d2_content, 'scores': sc_content, 'calls': calls_content,
        'rule_anchors_linked': sorted(LINKED), 'images': {k: str(v.relative_to(ROOT)) for k, v in sorted(ASSET_REFS.items())},
        'notes': NOTES, 'warnings': WARN, 'visible_text_sha1': hashlib.sha1(text.encode()).hexdigest(),
    }
    cpath = out_dir / f'{DATE}_Board-B-Content.json'
    cpath.write_text(json.dumps(content, indent=1, ensure_ascii=False, default=str))
    print(f'wrote {show(a.out)} ({len(page.encode()) / 1e3:.0f} kB) with {len(ASSET_REFS)} files ({img_bytes / 1e3:.1f} kB)')
    print(f'wrote {show(cpath)}')
    print(f'wrote the check copy {chk / a.out.name}')
    print(f'wrote the publish copy {pub_html} with {len(files)} files; map in {a.publish / "files.json"}')
    print(f'{len(LINKED)} chapters page anchors linked; {len(NOTES)} notes; {len(WARN)} warnings')
    if WARN and a.strict:
        sys.exit(1)


if __name__ == '__main__':
    try:
        main()
    except BoardError as e:
        print('error:', e)
        sys.exit(2)
