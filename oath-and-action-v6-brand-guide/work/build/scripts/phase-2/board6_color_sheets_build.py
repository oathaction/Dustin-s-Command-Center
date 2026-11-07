"""Build Board 6, section 4 (November 7, 2026): six identity sheets in six color schemes, and today's palette.

Usage:
    python3 -I work/build/scripts/phase-2/board6_color_sheets_build.py
    node work/build/scripts/phase-2/board6_color_sheets_render.js     (captures and the painted-color check)
    python3 -I work/build/scripts/phase-2/board6_color_sheets_build.py (again, to print the render results on the board)

Dustin's direction is DR-107: six one-page identity sheets, each led by a color other than red, on Newsprint with
Charcoal text, after the research lead's memo (work/handoffs/phase-2/20261107_Color-And-Aesthetic-Research.md).
Every sheet uses one layout and one set of content, so only the color changes. A seventh sheet shows today's palette.

Writes:
    work/boards/phase-2/board-6/color-sheets/20261107_Board-6-Color-Sheets.html
    work/boards/phase-2/board-6/color-sheets/20261107_Board-6-Color-Sheets-Pairs.json   every color pair the page prints

Reads (read and place only, never edited):
    work/build/tokens/tokens.css                                   inlined; faces, type sizes and neutrals come from it
    work/build/assets/identity/{wordmark,ampersand,lockmark}/...   the approved masters; B and the lever are recolored
                                                                   only through their fill variables (--amp, --lever)
    work/build/assets/civic-line/{red-black,red-newsprint,black}/  CL-019 to CL-022 and CL-031; only the red parts
                                                                   (#E63946) are recolored
    .../color-sheets/20261107_Board-6-Color-Sheets-Render-Results.json   when present, from the render script

Contrast: every ratio printed on the page is computed here from the WCAG 2.2 formula, and the build stops if a pair
falls under its threshold (4.5 to 1 for text, 3 to 1 for large text, marks, control edges and focus rings). Today's
sheet prints Pillar Red's own values, and the three pairs under 3 to 1 that today's guide accepts are marked as such.

Red: every Pillar Red paint sits under data-red. Red shown as a sample of today's system or of the error state is
data-red="specimen", as on Board 3; the wordmark's ampersand, the lever and icon accents on today's sheet are
data-red="signature". The script stops on an em dash or an en dash in its own copy.
"""
import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DATE = '20261107'
OUT_DIR = ROOT / 'work/boards/phase-2/board-6/color-sheets'
OUT = OUT_DIR / f'{DATE}_Board-6-Color-Sheets.html'
PAIRS_OUT = OUT_DIR / f'{DATE}_Board-6-Color-Sheets-Pairs.json'
RENDER = OUT_DIR / f'{DATE}_Board-6-Color-Sheets-Render-Results.json'
CHECK = OUT_DIR / f'{DATE}_Board-6-Color-Sheets-Check-Results.json'
TOKENS = ROOT / 'work/build/tokens/tokens.css'
ID = ROOT / 'work/build/assets/identity'
CL = ROOT / 'work/build/assets/civic-line'
FONTS = ('https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800'
         '&family=Inter:wght@400;500;600;700&family=Lora:ital,wght@1,400;1,500&display=swap')
TAGLINE = 'A country that answers to its people.'
FLAGGED = ['genuinely', 'really', 'truly', 'actually', 'simply', 'just', 'leverage', 'underscore', 'underscores',
           'reflect', 'reflects', 'stunning', 'robust', 'seamless', 'seamlessly', 'vibrant', 'bold choice']


# ------------------------------------------------------------------------------------------------ color math
def _lin(v):
    v /= 255
    return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4


def _rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i + 2], 16) for i in (0, 2, 4)]


def lum_hex(h):
    r, g, b = _rgb(h)
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def mix(a, b, t):
    ca, cb = _rgb(a), _rgb(b)
    return '#' + ''.join(f'{round(x * (1 - t) + y * t):02X}' for x, y in zip(ca, cb))


HEX = {
    # neutrals and today's palette, as tokens.css sets them
    'Newsprint': '#DCD9D2', 'Charcoal': '#121212', 'White': '#FFFFFF', 'Stone': '#5D636D', 'Deep Stone': '#4E535B',
    'Dim Newsprint': '#A3A19C', 'Error Band': '#E1C9C1', 'Pillar Red': '#E63946', 'Prussian': '#1F2D5A',
    'Verdigris': '#4A7C74',
    # the research lead's directions, values as the memo gives them
    'Patina': '#1F6E6A', 'Brass': '#8A6A2A', 'Sea Glass': '#7FB8AE',
    'Civic Yellow': '#FFD23F', 'Sky': '#9DB7E0',
    'Signal Orange': '#C2500E', 'Ember': '#8F3A0A', 'Apricot': '#F4B183',
    'Ochre': '#946616', 'Sepia': '#5B4630', 'Parchment': '#CDB98A',
    'Highlighter': '#D4F25A', 'Moss': '#45611A', 'Lilac': '#CBBDEB',
    'Ballot Violet': '#7552B3', 'Deep Violet': '#4B2E83', 'Suffrage Gold': '#E0B13A', 'Lavender': '#B39DDB',
}
# The one color this board adds: a hover fill for Patina, which the memo gives no deep partner. Patina with 30 percent
# Charcoal, the way the token file builds its tints.
HEX['Deep Patina'] = mix(HEX['Patina'], HEX['Charcoal'], 0.30)


def ratio(a, b):
    x, y = lum_hex(HEX.get(a, a)), lum_hex(HEX.get(b, b))
    return (max(x, y) + 0.05) / (min(x, y) + 0.05)


def rs(a, b):
    """A ratio as the page prints it."""
    return f'{ratio(a, b):.2f}:1'


def verdict(a, ground):
    if a == ground:
        return 'ground'
    v = ratio(a, ground)
    return 'text' if v >= 4.5 else 'mark' if v >= 3 else 'fill only'


NEED = {'text': 4.5, 'large': 3.0, 'mark': 3.0}


# ------------------------------------------------------------------------------------------------ text helpers
def copy(s):
    s = str(s)
    s = re.sub(r'"([^"<>]*)"', '“\\1”', s)
    s = re.sub(r"(?<=\w)'(?=\w)|(?<=s)'(?=[\s.,;:)])", '’', s)
    return s


def E(s):
    return html.escape(copy(s), quote=False)


def A(s):
    return html.escape(str(s), quote=True)


LINT = []


def lint_text(s, where):
    if '—' in s:
        sys.exit(f'em dash in {where}: {s[:80]}')
    if '–' in s:
        sys.exit(f'en dash in {where}: {s[:80]}')
    for w in FLAGGED:
        if re.search(rf'\b{w}\b', s, flags=re.I):
            LINT.append(f'{where}: "{w}"')


# ------------------------------------------------------------------------------------------------ schemes
NEUTRALS = [('Newsprint', 'Ground for every view'), ('Charcoal', 'Text, lines and the dark tile'),
            ('Deep Stone', 'Secondary text, disabled'), ('Stone', 'Chart context, hairlines')]

SCHEMES = [
    dict(key='patina', n=1, name='Patina', feel='Civic calm', status='Exploration', kind='band',
         lead='Patina', hero_ink='White', amp_n='Patina', amp_c='Patina', lever_n='Patina', lever_c='Patina',
         acc_n='Patina', acc_c='Patina', hinge='Patina', hinge_band=None,
         ask_fill='Patina', ask_label='White', ask_edge=None, hov_fill='Deep Patina', hov_label='White',
         ring='Charcoal', foc_fill=None, foc_label=None, c_ask_fill='Patina', c_ask_label='White',
         emph='Patina', emph_edge=None, emph_band=None, ctx='Stone', ink2='Prussian', tint='Sea Glass',
         palette=[('Patina', 'Lead: B, lever, ask, the named bar'), ('Prussian', 'Labels and links, a second series'),
                  ('Brass', 'The warm end of the diverging scale'), ('Sea Glass', 'Tint fill; text on Charcoal'),
                  ('Deep Patina', 'Hover fill only')],
         kind_line='A band lead. One hex passes 3 to 1 on Newsprint and on Charcoal.',
         jobs=['Ampersand B and the lockmark\'s lever on both grounds, with no keyline',
               'The ask button, under a White label at 6.01:1',
               'The one bar a chart\'s title names',
               'The accents of Civic Line icons'],
         limit='Patina sets text only from 24 px, or 18.66 px bold, since it measures 4.26:1 on Newsprint. Labels take Prussian.',
         party_level='Low', party=('No party claims teal in the sources the research lead checked. Green reads as the Green '
                                   'Party and as ecology, and teal leans toward blue.'),
         refs=['WGSN and Coloro named Transformative Teal the Colour of the Year 2026, in a trend report.',
               'GOV.UK\'s 2025 refresh keeps teal #158187 as an accent.',
               'The Financial Times sets teal #0D7680 on its paper ground.'],
         focus_note='Charcoal, 2 px with a 2 px gap, at 13.29:1. Verdigris leaves the ring, since it sits one step from Patina in the same hue.',
         error_note='Pillar Red stays as the error state only, with its glyph and the word Error.',
         div=('Prussian', 'Brass', 'Prussian to Brass, so the lead never stands for a data value. Verdigris leaves the scale.'),
         chart_note='Patina and Stone match in grayscale and for a reader with deuteranopia, so the bold label carries the emphasis.',
         print_note='Needs a process build and a press proof on the real stock.',
         change='Focus ring to Charcoal; diverging scale to Prussian and Brass'),
    dict(key='federal-ink', n=2, name='Federal Ink', feel='Official record', status='Exploration', kind='ink',
         lead='Prussian', hero_ink='White', amp_n='Prussian', amp_c='Sky', lever_n='Prussian', lever_c='Sky',
         acc_n='Prussian', acc_c='Sky', hinge='Prussian', hinge_band=None,
         ask_fill='Prussian', ask_label='White', ask_edge=None, hov_fill='Charcoal', hov_label='White',
         ring='Charcoal', foc_fill='Civic Yellow', foc_label='Charcoal', c_ask_fill='Sky', c_ask_label='Charcoal',
         emph='Prussian', emph_edge=None, emph_band=None, ctx='Stone', ink2='Prussian', tint='Civic Yellow',
         palette=[('Prussian', 'Lead: B, lever, ask, labels'), ('Civic Yellow', 'Focus fill and highlight, under Charcoal'),
                  ('Sky', 'The lead\'s partner on Charcoal'), ('Verdigris', 'A second mark')],
         kind_line='An ink lead. It passes 4.5 to 1 for text on Newsprint and fails on Charcoal, where Sky takes its place.',
         jobs=['Ampersand B, the lever and icon accents on Newsprint, at 9.42:1',
               'The ask button, under a White label at 13.28:1',
               'Labels and links at any size',
               'On Charcoal, Sky takes each of these jobs at 9.17:1'],
         limit='Prussian sits 1.41:1 from Charcoal, so a two-color icon reads as two inks only up close.',
         party_level='Moderate', party=('Navy is still blue, and blue reads Democratic on election maps; this week\'s headlines '
                                        'called the midterms a "blue wave". That deep navy reads less partisan than bright blue '
                                        'is untested with readers. Civic Yellow, the Libertarian color in Rock the Vote\'s list, '
                                        'stays a fill.'),
         refs=['GOV.UK pairs its brand blue with a yellow focus state under near-black text.',
               'The Guardian pairs navy #052962 with yellow #FFE500 for its asks.',
               'The U.S. Web Design System grades each color from 0 to 100 and sets contrast by the gap.'],
         focus_note='The button turns Civic Yellow under a Charcoal label, at 12.97:1, inside a 2 px Charcoal ring at 13.29:1, as GOV.UK does.',
         error_note='Pillar Red stays as the error state only, with its glyph and the word Error, and red still never sits on Prussian.',
         div=('Verdigris', 'Brass', 'Verdigris to Brass, since Prussian, the scale\'s blue end today, becomes the lead.'),
         chart_note='Prussian is far darker than Stone, so the named bar stands apart in grayscale as well.',
         print_note='Prussian is today\'s ink blue; Sky and Civic Yellow need press proofs on newsprint.',
         change='Sky on Charcoal; Civic Yellow focus; diverging scale to Verdigris and Brass'),
    dict(key='signal-orange', n=3, name='Signal Orange', feel='Editorial urgency', status='Exploration', kind='band',
         lead='Signal Orange', hero_ink='White', amp_n='Signal Orange', amp_c='Signal Orange', lever_n='Signal Orange',
         lever_c='Signal Orange', acc_n='Signal Orange', acc_c='Signal Orange', hinge='Signal Orange', hinge_band=None,
         ask_fill='Signal Orange', ask_label='White', ask_edge=None, hov_fill='Ember', hov_label='White',
         ring='Verdigris', foc_fill=None, foc_label=None, c_ask_fill='Signal Orange', c_ask_label='White',
         emph='Signal Orange', emph_edge=None, emph_band=None, ctx='Stone', ink2='Ember', tint='Apricot',
         palette=[('Signal Orange', 'Lead: B, lever, ask, the named bar'), ('Ember', 'Labels, links and hover'),
                  ('Prussian', 'Dark panels, a second series'), ('Apricot', 'Tint fill under Charcoal')],
         kind_line='A band lead. One hex passes 3 to 1 on Newsprint and on Charcoal.',
         jobs=['Ampersand B and the lever on both grounds, with no keyline',
               'The ask button, under a White label at 4.72:1, which passes even for small text',
               'The one bar a chart\'s title names',
               'The accents of Civic Line icons'],
         limit='Signal Orange sets text only from 24 px, since it measures 3.35:1 on Newsprint. Kickers and links take Ember at 5.36:1.',
         party_level='Low as a party; moderate on firearms pieces',
         party=('Rock the Vote\'s list names no party for orange. Wear Orange uses it for gun safety, so an orange ask on a '
                'piece about firearms law could read as that campaign\'s color.'),
         refs=['The Guardian marks opinion with orange #C74600, 2.4 from Signal Orange, so an orange Act piece could read as opinion.',
               'Pinterest\'s 2026 trend palette names Persimmon, "part orange, part red".',
               'WGSN lists Energy Orange for spring and summer 2027.'],
         focus_note='Verdigris, 2 px with a 2 px gap, at 3.37:1, as today.',
         error_note='Pillar Red stays as the error state only. For a reader with deuteranopia it sits 6.9 from Signal Orange, so the glyph and the word carry it. Warning keeps its own triangle and word, since orange means WARNING on U.S. safety signs.',
         div=('Prussian', 'Verdigris', 'Prussian to Verdigris, as today (DR-54).'),
         chart_note='Signal Orange and Stone sit close in grayscale, so the bold label carries the emphasis there.',
         print_note='Needs a process build and a press proof on the real stock.',
         change='No token changes; Ember for small text'),
    dict(key='archive-ochre', n=4, name='Archive Ochre', feel='Archival warmth', status='Exploration', kind='band',
         lead='Ochre', hero_ink='White', amp_n='Ochre', amp_c='Ochre', lever_n='Ochre', lever_c='Ochre',
         acc_n='Ochre', acc_c='Ochre', hinge='Ochre', hinge_band=None,
         ask_fill='Ochre', ask_label='White', ask_edge=None, hov_fill='Sepia', hov_label='White',
         ring='Verdigris', foc_fill=None, foc_label=None, c_ask_fill='Ochre', c_ask_label='White',
         emph='Ochre', emph_edge=None, emph_band=None, ctx='Stone', ink2='Sepia', tint='Parchment',
         palette=[('Ochre', 'Lead: B, lever, ask, the named bar'), ('Sepia', 'Labels, links and hover'),
                  ('Parchment', 'Tint fill under Charcoal'), ('Prussian', 'Ink blue, a second series')],
         kind_line='A band lead. One hex passes 3 to 1 on Newsprint and on Charcoal.',
         jobs=['Ampersand B and the lever on both grounds, with no keyline',
               'The ask button, under a White label at 5.03:1',
               'The one bar a chart\'s title names',
               'The accents of Civic Line icons'],
         limit='Ochre sets text only from 24 px, at 3.57:1 on Newsprint. Small text takes Sepia at 6.30:1.',
         party_level='Low to moderate',
         party=('No party reading turned up for brown or ochre. Gold and yellow are the Libertarian Party\'s colors and the '
                'Gadsden flag\'s, and a deep ochre sits far darker than either.'),
         refs=['The Guardian\'s culture pages use a brown in the same band, #866D50.',
               'Gold was the one color every U.S. suffrage group shared, the National Park Service records.',
               'WGSN\'s trend report lists Clay for spring and summer 2027.'],
         focus_note='Verdigris, 2 px with a 2 px gap, at 3.37:1, as today.',
         error_note='Pillar Red stays as the error state only. For a reader with deuteranopia it sits 8.9 from Ochre, so the glyph and the word carry the error.',
         div=('Prussian', 'Verdigris', 'Prussian to Verdigris, as today (DR-54).'),
         chart_note='Ochre and Stone sit close in grayscale, so the bold label carries the emphasis there.',
         print_note='Ochre needs three process inks, so it may shift most between print runs.',
         change='No token changes; Sepia for small text'),
    dict(key='highlighter', n=5, name='Highlighter', feel='Modern markup', status='Exploration', kind='fill',
         lead='Highlighter', hero_ink='Charcoal', amp_n='Moss', amp_c='Highlighter', lever_n='Moss', lever_c='Highlighter',
         acc_n='Moss', acc_c='Highlighter', hinge='Charcoal', hinge_band='Highlighter',
         ask_fill='Highlighter', ask_label='Charcoal', ask_edge='Charcoal', hov_fill='Charcoal', hov_label='Highlighter',
         ring='Verdigris', foc_fill=None, foc_label=None, c_ask_fill='Highlighter', c_ask_label='Charcoal',
         emph='Charcoal', emph_edge=None, emph_band='Highlighter', ctx='Stone', ink2='Moss', tint='Lilac',
         palette=[('Highlighter', 'Lead: a fill behind Charcoal type'), ('Moss', 'The lead\'s ink: B, lever, labels'),
                  ('Lilac', 'A second fill, for the selected state')],
         kind_line='A fill lead. It carries Charcoal type at 14.85:1 and cannot draw on Newsprint, where it measures 1.12:1.',
         jobs=['The ask button, under a Charcoal label with a Charcoal keyline',
               'A band behind Charcoal headline words',
               'Ampersand B and the lever on Charcoal, at 14.85:1',
               'A band behind the value a chart\'s title names'],
         limit='On Newsprint, B, the lever and icon accents take Moss at 5.00:1, which changes how the wordmark shows on paper.',
         party_level='Moderate',
         party=('The Harris campaign\'s July 2024 banner used a neon green. Whether readers still tie the color to that '
                'campaign is untested.'),
         refs=['Grist sets a pale chartreuse band behind brown-black type.',
               'USAFacts marks headline words with a mint highlight.',
               'Pinterest\'s 2026 trend palette names Wasabi, "electric chartreuse".'],
         focus_note='Verdigris, 2 px with a 2 px gap, at 3.37:1, as today.',
         error_note='Pillar Red stays as the error state only, with its glyph and the word Error.',
         div=('Prussian', 'Verdigris', 'Prussian to Verdigris, as today (DR-54).'),
         chart_note='The named bar takes Charcoal, and its value sits on a Highlighter band, since a lime bar would vanish on Newsprint.',
         print_note='A pale fill dulls most on newsprint, and a dull highlighter loses its point.',
         change='B, lever and accents in Moss on Newsprint; chart emphasis becomes a band'),
    dict(key='ballot-violet', n=6, name='Ballot Violet', feel='Community heritage', status='Exploration', kind='band',
         lead='Ballot Violet', hero_ink='White', amp_n='Ballot Violet', amp_c='Ballot Violet', lever_n='Ballot Violet',
         lever_c='Ballot Violet', acc_n='Ballot Violet', acc_c='Ballot Violet', hinge='Ballot Violet', hinge_band=None,
         ask_fill='Ballot Violet', ask_label='White', ask_edge=None, hov_fill='Deep Violet', hov_label='White',
         ring='Verdigris', foc_fill=None, foc_label=None, c_ask_fill='Ballot Violet', c_ask_label='White',
         emph='Ballot Violet', emph_edge=None, emph_band=None, ctx='Stone', ink2='Deep Violet', tint='Suffrage Gold',
         palette=[('Ballot Violet', 'Lead: B, lever, ask, the named bar'), ('Deep Violet', 'Labels, links and hover'),
                  ('Suffrage Gold', 'Tint fill under Charcoal'), ('Lavender', 'Text on Charcoal')],
         kind_line='A band lead. One hex passes 3 to 1 on Newsprint and on Charcoal.',
         jobs=['Ampersand B and the lever on both grounds, with no keyline',
               'The ask button, under a White label at 5.81:1',
               'The one bar a chart\'s title names',
               'The accents of Civic Line icons'],
         limit='Ballot Violet sets text only from 24 px, at 4.12:1 on Newsprint. Small text takes Deep Violet at 7.38:1.',
         party_level='Low as a party; moderate as a meaning',
         party=('Purple blends the two party colors, so it can say the brand sits between the parties, a different claim '
                'from one standard of evidence (DR-93). Five civic groups the research lead checked already lead with purple.'),
         refs=['The National Woman\'s Party flew purple, white and gold, the National Park Service records.',
               'Votebeat sets its wordmark tag in purple #824F9D.',
               'Democracy Works moved to deep indigo and violet in February 2026.'],
         focus_note='Verdigris, 2 px with a 2 px gap, at 3.37:1, as today.',
         error_note='Pillar Red stays as the error state only, with its glyph and the word Error.',
         div=('Prussian', 'Verdigris', 'Prussian to Verdigris, as today (DR-54).'),
         chart_note='Ballot Violet and Stone match in grayscale, so the bold label carries the emphasis.',
         print_note='Violet needs a process build and a press proof on the real stock.',
         change='No token changes; Deep Violet for small text'),
    dict(key='today', n=7, name='Pillar Red', feel='Precise punctuation', status='Today, for reference', kind='today',
         lead='Pillar Red', hero_ink='White', amp_n='Pillar Red', amp_c='Pillar Red', lever_n='Pillar Red',
         lever_c='Pillar Red', acc_n='Pillar Red', acc_c='Pillar Red', hinge='Pillar Red', hinge_band=None,
         ask_fill='Pillar Red', ask_label='White', ask_edge='Charcoal', hov_fill='Pillar Red', hov_label='White',
         ring='Verdigris', foc_fill=None, foc_label=None, c_ask_fill='Pillar Red', c_ask_label='White',
         emph='Pillar Red', emph_edge='Charcoal', emph_band=None, ctx='Stone', ink2='Deep Stone', tint='White',
         palette=[('Pillar Red', 'Lead: signature and one working red'), ('Prussian', 'Depth: dark panels'),
                  ('Verdigris', 'Focus ring, success, diverging end'), ('Error Band', 'Ground for an error message')],
         kind_line='Outside the band. Pillar Red measures 2.96:1 on Newsprint and 4.49:1 on Charcoal.',
         jobs=['Signature red: ampersand B, the lever and icon accents',
               'One working red per view: an error, the ask or the one point a headline names (Rule 05.3)',
               'The ask\'s White label measures 4.17:1, which passes because the ask sets 19 px bold'],
         limit='A red mark that carries meaning on Newsprint takes a 1 px Charcoal keyline (Rule 05.5), and red never sits on Prussian.',
         party_level='Documented, and managed by rule',
         party=('Red has marked the Republican side of U.S. election maps since 2000. The guide keeps red off Prussian and '
                'off every party mark (DR-48).'),
         refs=['Chapter 05 of this guide, Rules 05.1 to 05.5.',
               'Newsweek\'s September 2025 redesign with the studio 2x4 used "a confident red-and-paper palette".'],
         focus_note='Verdigris, 2 px with a 2 px gap, at 3.37:1.',
         error_note='Pillar Red, as one of the working red\'s three claims, with its glyph and the word Error.',
         div=('Prussian', 'Verdigris', 'Prussian to Verdigris (DR-54).'),
         chart_note='The named bar takes red with a 1 px Charcoal keyline, since red measures 2.96:1 on Newsprint.',
         print_note='Today\'s print notes stand (chapter 25).',
         change='Today\'s guide'),
]
SCHEME = {s['key']: s for s in SCHEMES}
ORDER = [s['key'] for s in SCHEMES]


# ------------------------------------------------------------------------------------------------ pairs registry
class Pairs:
    """Every color pair a sheet prints, with the threshold it must meet."""

    def __init__(self):
        self.by = {}
        self.cur = None

    def start(self, key):
        self.cur = key
        self.by.setdefault(key, [])

    def add(self, where, fg, bg, kind, prop=None, exempt=None):
        v = ratio(fg, bg)
        rec = dict(where=where, fg=fg, fg_hex=HEX.get(fg, fg), bg=bg, bg_hex=HEX.get(bg, bg), kind=kind,
                   need=NEED[kind], ratio=round(v, 2), exempt=exempt)
        if (where, fg, bg) not in {(r['where'], r['fg'], r['bg']) for r in self.by[self.cur]}:
            self.by[self.cur].append(rec)
        if v + 1e-9 < NEED[kind] and not exempt:
            sys.exit(f'{self.cur}: {where}: {fg} on {bg} measures {v:.2f}:1, under {NEED[kind]}:1 for {kind}')
        if prop is None:
            return ''
        need = 0 if exempt else NEED[kind]
        return f' data-chk="{prop}|{HEX.get(bg, bg)}|{need}|{HEX.get(fg, fg)}"'


P = Pairs()


# ------------------------------------------------------------------------------------------------ masters
def _clean(path):
    s = path.read_text()
    s = re.sub(r'<\?xml[^>]*>\s*', '', s)
    s = re.sub(r'<title>.*?</title>', '', s, flags=re.S)
    s = re.sub(r'<desc>.*?</desc>', '', s, flags=re.S)
    s = re.sub(r'\s(id|data-id)="[^"]*"', '', s)
    return s.strip()


def place(path, w, h=None, cls='', style='', label=None, attrs=''):
    """Place a master at a size. Geometry is untouched; the root element gets size, class and accessibility."""
    s = _clean(path)
    vb = re.search(r'viewBox="([^"]+)"', s).group(1)
    vw, vh = (float(v) for v in vb.split()[2:])
    h = h if h is not None else w * vh / vw
    a11y = f'role="img" aria-label="{A(label)}"' if label else 'aria-hidden="true"'
    st = f' style="{style}"' if style else ''
    s = re.sub(r'<svg\b[^>]*>', f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="{w:.2f}" height="{h:.2f}" '
               f'class="{cls}" {a11y} focusable="false"{st}{attrs}>', s, count=1)
    return s


WM = ID / 'wordmark/20261028_Wordmark-Display-Master.svg'
WM16 = ID / 'wordmark/20261028_Wordmark-16px-Master.svg'
AMP16 = ID / 'ampersand/20261028_Amp-B-16px-Master.svg'
AMPD = ID / 'ampersand/20261028_Amp-B-Display-Master.svg'
LOCKD = ID / 'lockmark/20261028_Lockmark-Master-V5.svg'
LOCK24 = ID / 'lockmark/20261028_Lockmark-24px-Master.svg'
PILLARS = [('CL-019', 'Explain'), ('CL-020', 'Track'), ('CL-021', 'Connect'), ('CL-022', 'Act')]


def cl_file(code, label, edition):
    slug = label.replace(' ', '-')
    suffix = {'red-black': 'Red-Black', 'red-newsprint': 'Red-Newsprint', 'black': 'Black'}[edition]
    return CL / edition / f'20261029_Oath-And-Action-Civic-Line-{code}-{slug}-{suffix}.svg'


def icon(code, label, edition, size, acc=None, chk=''):
    """A Civic Line drawing. Only its red parts change: #E63946 becomes the accent color."""
    s = place(cl_file(code, label, edition), size, size, cls='cl')
    if acc:
        s = s.replace('#E63946', HEX[acc])
        if chk:
            s = s.replace('data-part="accent"', f'data-part="accent"{chk}', 1)
    return s


def red_attr(color, kind, job):
    return f' data-red="{kind}" data-red-job="{job}"' if color == 'Pillar Red' else ''


def wordmark(s, w, n_ground='Newsprint', where='Wordmark B', master=WM):
    amp = s['amp_n']
    exempt = 'logo; today\'s signature red' if amp == 'Pillar Red' else None
    chk = P.add(f'{where} on Newsprint', amp, n_ground, 'mark', prop='fill', exempt=exempt)
    P.add(f'{where.replace(" B", "")} letters on Newsprint', 'Charcoal', n_ground, 'mark')
    svg = place(master, w, cls='wm', label='Oath & Action', style=f'color:{HEX["Charcoal"]};--amp:{HEX[amp]}',
                attrs=red_attr(amp, 'signature', 'signature ampersand'))
    return svg.replace('fill="var(--amp,#E63946)"', f'fill="var(--amp,#E63946)"{chk}', 1)


def lockmark(s, size, ground):
    on_c = ground == 'Charcoal'
    lever = s['lever_c'] if on_c else s['lever_n']
    ink = 'Newsprint' if on_c else 'Charcoal'
    link = 'Newsprint' if on_c else 'Stone'
    exempt = 'logo; today\'s signature red' if (lever == 'Pillar Red' and not on_c) else None
    chk = P.add(f'Lockmark lever on {ground}', lever, ground, 'mark', prop='fill', exempt=exempt)
    P.add(f'Lockmark nodes on {ground}', ink, ground, 'mark')
    P.add(f'Lockmark links on {ground}', link, ground, 'mark')
    svg = place(LOCKD if size >= 48 else LOCK24, size, size, cls='lk',
                style=f'color:{HEX[ink]};--lever:{HEX[lever]};--link:{HEX[link]}',
                attrs=red_attr(lever, 'signature', 'signature lever'))
    if size >= 48:
        return svg.replace('fill="var(--lever,#E63946)"', f'fill="var(--lever,#E63946)"{chk}', 1)
    return svg.replace('<g fill="var(--lever,#E63946)">', f'<g fill="var(--lever,#E63946)"{chk}>', 1)


def hinge_b(color, cap):
    """B in a hinge headline: the 16 px master scaled so its 14 units of capitals match the type's cap height."""
    k = cap / 14
    return place(AMP16, 14 * k, 16 * k, cls='hb-svg', style=f'color:{HEX[color]};vertical-align:{-k:.2f}px')


# ------------------------------------------------------------------------------------------------ sheet parts
def m_h(text, extra=''):
    return f'<p class="m-h"{extra}>{E(text)}</p>'


def sec_head(s):
    wm = wordmark(s, 640)
    amp = s['amp_n']
    if s['key'] == 'highlighter':
        cap = (f'Wordmark, display master. On Newsprint, B takes Moss at {rs("Moss", "Newsprint")}, because Highlighter '
               f'measures {rs("Highlighter", "Newsprint")} there.')
    elif amp == 'Pillar Red':
        cap = (f'Wordmark, display master. B in Pillar Red at {rs(amp, "Newsprint")} on Newsprint, accepted today as '
               f'signature red in a logo.')
    else:
        cap = f'Wordmark, display master, with ampersand B in {amp} at {rs(amp, "Newsprint")} on Newsprint.'
    hero_red = red_attr(s['lead'], 'specimen', 'palette swatch')
    P.add('Hero name, feel and hex (large type)', s['hero_ink'], s['lead'], 'large')
    return (f'<div class="m-head">{wm}<p class="cap">{E(cap)}</p></div>'
            f'<div class="m-hero" style="--hero:{HEX[s["lead"]]};--hero-ink:{HEX[s["hero_ink"]]}"{hero_red}>'
            f'<p class="h-n">{E(s["name"])}</p><p class="h-f">{E(s["feel"])}</p>'
            f'<p class="h-x"><span>Lead</span> {HEX[s["lead"]]}</p></div>')


def sec_palette(s):
    rows = []
    names = [p[0] for p in s['palette']] + [n[0] for n in NEUTRALS] + [('White')]
    roles = dict(s['palette'] + NEUTRALS)
    roles['White'] = 'Label on the ask' if s['ask_label'] == 'White' or s['c_ask_label'] == 'White' else 'Available; no job on this sheet'
    for nm in names:
        hx = HEX[nm]
        cells = []
        for g in ('Newsprint', 'Charcoal'):
            v = verdict(nm, g)
            num = '' if v == 'ground' else f'<b>{ratio(nm, g):.2f}</b> '
            cells.append(f'<td data-k="On {g}">{num}<span class="vd">{v}</span></td>')
        red = red_attr(nm, 'specimen', 'palette swatch')
        rows.append(f'<tr><th scope="row"><span class="sw"><span class="chip" style="background:{hx}"{red}></span>'
                    f'<span class="sw-t"><span class="pn">{E(nm)}</span><span class="pr">{E(roles[nm])}</span></span></span></th>'
                    f'<td class="hx" data-k="Hex">{hx}</td>{"".join(cells)}</tr>')
    P.add('Palette table text and chips', 'Charcoal', 'Newsprint', 'text')
    P.add('Palette roles and verdicts', 'Deep Stone', 'Newsprint', 'text')
    return (f'<div class="m-pal">{m_h("Palette")}<table class="pal"><thead><tr><th scope="col">Color</th><th scope="col">Hex</th>'
            f'<th scope="col">On Newsprint</th><th scope="col">On Charcoal</th></tr></thead><tbody>{"".join(rows)}</tbody></table>'
            f'<p class="cap">text, 4.5:1 or more at any size. mark, 3:1 or more: marks, focus rings, control edges and type from '
            f'24 px, or 18.66 px bold. fill only, under 3:1: it sits under type and draws no mark on that ground.</p></div>')


def sec_type(s):
    P.add('Type samples', 'Charcoal', 'Newsprint', 'text')
    P.add('Type labels', s['ink2'], 'Newsprint', 'text')
    return (f'<div class="m-type">{m_h("Type")}'
            f'<div class="ty"><p class="ty-l">Inter Tight 800 · headlines</p><p class="ty-a">A board sets your rate.</p></div>'
            f'<div class="ty"><p class="ty-l">Inter 400 and 600 · reading and interface</p><p class="ty-b">A regulator or a '
            f'board approves your rate, and you can comment before it votes.</p></div>'
            f'<div class="ty"><p class="ty-l">Lora Italic · quoted words</p><p class="ty-c">"{E(TAGLINE)}"</p></div></div>')


def sec_card(s):
    cap_px = 28 * 0.7275
    hc = s['hinge']
    exempt = None
    job = 'the one point the headline names'
    if s['hinge_band']:
        P.add('Hinge headline on its band', 'Charcoal', s['hinge_band'], 'text')
        P.add('Hinge B on its band', hc, s['hinge_band'], 'mark')
        chk = ''
    else:
        exempt = 'today\'s working red as large type' if hc == 'Pillar Red' else None
        # B is set at the headline's cap height (28 px type), so it counts as large type: 3 to 1
        chk = P.add('Hinge B on Newsprint', hc, 'Newsprint', 'mark', prop='color', exempt=exempt)
    b = hinge_b(hc, cap_px)
    bwrap = (f'<span class="hb" role="img" aria-label="and"{chk}{red_attr(hc, "specimen", job)} style="color:{HEX[hc]}">{b}</span>')
    line2 = f'{bwrap}&nbsp;the&nbsp;rent.'
    if s['hinge_band']:
        line2 = f'<span class="band" style="--band:{HEX[s["hinge_band"]]}">{line2}</span>'
    P.add('Card text', 'Charcoal', 'Newsprint', 'text')
    P.add('Card kicker', s['ink2'], 'Newsprint', 'text')
    P.add('Card kicker icon, one color', 'Charcoal', 'Newsprint', 'mark')
    kick_icon = icon('CL-031', 'Local Government', 'black', 24)
    wm16 = wordmark(s, 152, where='Card wordmark B', master=WM16)
    return (f'<div class="m-card">{m_h("Article card")}<div class="card">'
            f'<p class="illus">Illustrative</p>'
            f'<p class="kick">{kick_icon}<span>Explainer · Local government</span></p>'
            f'<p class="hl">The&nbsp;zoning&nbsp;code<br><span class="nw">{line2}</span></p>'
            f'<p class="dek">A county board decides what can be built on each lot, and that limit shapes the rent nearby.</p>'
            f'<div class="cfoot">{wm16}</div></div>'
            f'<p class="cap">{E(card_cap(s))}</p></div>')


def card_cap(s):
    if s['hinge_band']:
        return f'The hinge line sits on a Highlighter band, with B in Charcoal at {rs("Charcoal", "Highlighter")}.'
    if s['hinge'] == 'Pillar Red':
        return f'Hinge B in Pillar Red, today\'s working red, at {rs("Pillar Red", "Newsprint")} as 28 px type.'
    return f'Hinge B in {s["hinge"]} at {rs(s["hinge"], "Newsprint")}, set at the headline\'s cap height.'


def sec_icons(s):
    acc = s['acc_n']
    exempt = 'today\'s signature red beside its word (R11)' if acc == 'Pillar Red' else None
    chk = P.add('Icon accents on Newsprint', acc, 'Newsprint', 'mark', prop='stroke', exempt=exempt)
    P.add('Icon lines on Newsprint', 'Charcoal', 'Newsprint', 'mark')
    red = red_attr(acc, 'signature', 'signature icon accent')
    items = ''.join(f'<li><span class="ic"{red}>{icon(c, l, "red-black", 56, acc=acc, chk=chk)}</span><span>{E(l)}</span></li>'
                    for c, l in PILLARS)
    if acc == 'Moss':
        cap = f'Accents in Moss at {rs("Moss", "Newsprint")}; Highlighter would measure {rs("Highlighter", "Newsprint")}.'
    elif acc == 'Pillar Red':
        cap = f'Accents in Pillar Red at {rs(acc, "Newsprint")}, signature red beside each word, as today.'
    else:
        cap = f'Accents in {acc} at {rs(acc, "Newsprint")}; lines in Charcoal.'
    lever = s['lever_n']
    lk_cap = f'Lever in {lever} at {rs(lever, "Newsprint")}; links in Stone at {rs("Stone", "Newsprint")}.'
    if lever == 'Pillar Red':
        lk_cap = f'Lever in Pillar Red at {rs(lever, "Newsprint")}, signature red, as today; links in Stone.'
    return (f'<div class="m-icons">{m_h("Civic Line, two colors")}<ul class="pillars">{items}</ul>'
            f'<p class="cap">{E(cap)}</p>'
            f'{m_h("Lockmark", " style=\"margin-top:20px\"")}<div class="lkrow">{lockmark(s, 64, "Newsprint")}{lockmark(s, 24, "Newsprint")}</div>'
            f'<p class="cap">{E(lk_cap)}</p></div>')


def ask(s, state, ground='Newsprint', label='Sign up to speak'):
    """One ask button, as a still picture of its state."""
    if ground == 'Charcoal':
        f, l = s['c_ask_fill'], s['c_ask_label']
        kind = 'text' if ratio(l, f) >= 4.5 else 'large'
        lchk = P.add('Ask label on Charcoal', l, f, kind, prop='color')
        P.add('Ask fill against Charcoal', f, 'Charcoal', 'mark')
        red = red_attr(f, 'specimen', 'ask')
        return f'<span class="ask" style="--f:{HEX[f]};--l:{HEX[l]}"{lchk}{red}>{E(label)}</span>'
    f, l, edge = s['ask_fill'], s['ask_label'], s['ask_edge']
    style = f'--f:{HEX[f]};--l:{HEX[l]}'
    cls = 'ask'
    if state == 'default':
        kind = 'text' if ratio(l, f) >= 4.5 else 'large'
        lchk = P.add('Ask label on its fill', l, f, kind, prop='color')
        if edge:
            P.add('Ask keyline on Newsprint', edge, 'Newsprint', 'mark')
            P.add('Ask fill on Newsprint, inside its keyline', f, 'Newsprint', 'mark', exempt='a fill inside a Charcoal keyline')
            style += f';--e:{HEX[edge]}'
            cls += ' edge'
        else:
            P.add('Ask fill on Newsprint', f, 'Newsprint', 'mark')
    elif state == 'hover':
        hf, hl = s['hov_fill'], s['hov_label']
        kind = 'text' if ratio(hl, hf) >= 4.5 else 'large'
        lchk = P.add('Hover label on its fill', hl, hf, kind, prop='color')
        P.add('Hover fill on Newsprint', hf, 'Newsprint', 'mark',
              exempt='a fill inside a Charcoal keyline' if edge and ratio(hf, 'Newsprint') < 3 else None)
        style = f'--f:{HEX[hf]};--l:{HEX[hl]}'
        if edge:
            style += f';--e:{HEX[edge]}'
            cls += ' edge'
        cls += ' hov'
        f = hf
    elif state == 'focus':
        ring = s['ring']
        rchk = P.add('Focus ring on Newsprint', ring, 'Newsprint', 'mark', prop='outline-color')
        if s['foc_fill']:
            ff, fl = s['foc_fill'], s['foc_label']
            lchk = P.add('Focus label on its fill', fl, ff, 'text', prop='color')
            style = f'--f:{HEX[ff]};--l:{HEX[fl]}'
            f = ff
        else:
            kind = 'text' if ratio(l, f) >= 4.5 else 'large'
            lchk = P.add('Ask label on its fill', l, f, kind, prop='color')
        style += f';--r:{HEX[ring]}'
        if edge:
            style += f';--e:{HEX[edge]}'
            cls += ' edge'
        cls += ' foc'
        lchk = lchk + rchk.replace('data-chk', 'data-chk2')
    else:  # disabled
        P.add('Disabled label and dashed edge', 'Deep Stone', 'Newsprint', 'text')
        return f'<span class="ask dis">{E(label)}</span>'
    red = red_attr(f, 'specimen', 'ask')
    return f'<span class="{cls}" style="{style}"{lchk}{red}>{E(label)}</span>'


def sec_dark(s):
    amp = s['amp_c']
    chk = P.add('B on Charcoal', amp, 'Charcoal', 'mark', prop='fill')
    bsvg = place(AMPD, 56 * 93.29 / 102.69, 56, cls='bd', style=f'color:{HEX[amp]}',
                 attrs=red_attr(amp, 'signature', 'signature ampersand'))
    bsvg = bsvg.replace('fill="currentColor"', f'fill="currentColor"{chk}', 1)
    acc = s['acc_c']
    achk = P.add('Icon accent on Charcoal', acc, 'Charcoal', 'mark', prop='stroke')
    P.add('Icon lines on Charcoal', 'Newsprint', 'Charcoal', 'mark')
    ic = f'<span class="ic"{red_attr(acc, "signature", "signature icon accent")}>{icon("CL-022", "Act", "red-newsprint", 56, acc=acc, chk=achk)}</span>'
    P.add('Labels on Charcoal', 'Newsprint', 'Charcoal', 'text')
    P.add('Captions on Charcoal', 'Dim Newsprint', 'Charcoal', 'text')
    f, l = s['c_ask_fill'], s['c_ask_label']
    cap = (f'B, the lever and the accent in {amp} at {rs(amp, "Charcoal")}. The ask: fill at {rs(f, "Charcoal")} '
           f'on Charcoal, {l} label at {rs(l, f)}.')
    return (f'<div class="m-dark">{m_h("On Charcoal, the default tile")}'
            f'<div class="drow"><span class="dcell">{bsvg}<span class="dl">B</span></span>'
            f'<span class="dcell">{lockmark(s, 56, "Charcoal")}<span class="dl">Lockmark</span></span>'
            f'<span class="dcell">{ic}<span class="dl">Act</span></span></div>'
            f'<p class="dask">{ask(s, "default", "Charcoal")}</p>'
            f'<p class="cap">{E(cap)}</p></div>')


def sec_buttons(s):
    def row(name, note, btn, extra=''):
        return (f'<div class="st"><p class="st-l"><b>{E(name)}</b><span>{E(note)}</span></p>'
                f'<p class="st-b">{btn}</p>{extra}</div>')
    f, l = s['ask_fill'], s['ask_label']
    d_note = f'{l} on {f}, {rs(l, f)}' + (f'; Charcoal keyline' if s['ask_edge'] else '')
    if s['hov_fill'] == s['ask_fill']:
        h_note = 'Underlined; the tokens name no hover fill'
    else:
        h_note = f'{s["hov_fill"]}, underlined, {rs(s["hov_label"], s["hov_fill"])}'
    if s['foc_fill']:
        fo_note = f'{s["foc_fill"]} under Charcoal, {s["ring"]} ring {rs(s["ring"], "Newsprint")}'
    else:
        fo_note = f'{s["ring"]} ring, {rs(s["ring"], "Newsprint")}'
    out = (row('Default', d_note, ask(s, 'default')) +
           row('Hover', h_note, ask(s, 'hover')) +
           row('Focus', fo_note, ask(s, 'focus')) +
           row('Disabled', f'Deep Stone, dashed, {rs("Deep Stone", "Newsprint")}', ask(s, 'disabled'),
               '<p class="reason">Choose a meeting date first.</p>'))
    return f'<div class="m-btn">{m_h("The ask button")}{out}</div>'


CHART = [('Jan.', 42), ('Feb.', 57), ('March', 128), ('April', 64), ('May', 38)]
CHART_MAX, CHART_H = 128, 120


def sec_chart(s):
    em, band, edge = s['emph'], s['emph_band'], s['emph_edge']
    exempt = 'a fill inside a Charcoal keyline, today\'s working red (Rule 05.5)' if edge else None
    echk = P.add('Named bar on Newsprint', em, 'Newsprint', 'mark', prop='background-color', exempt=exempt)
    if edge:
        P.add('Named bar keyline on Newsprint', edge, 'Newsprint', 'mark')
    cchk = P.add('Context bars on Newsprint', s['ctx'], 'Newsprint', 'mark', prop='background-color')
    P.add('Chart labels', 'Charcoal', 'Newsprint', 'text')
    P.add('Chart subtitle', 'Deep Stone', 'Newsprint', 'text')
    if band:
        P.add('Named value on its band', 'Charcoal', band, 'text')
    cols, xs = [], []
    for m, v in CHART:
        h = v / CHART_MAX * CHART_H
        is_em = m == 'March'
        val = f'{v}'
        if is_em and band:
            val = f'<span class="vband" style="--band:{HEX[band]}">{v}</span>'
        style = f'height:{h:.3f}px;--c:{HEX[em if is_em else s["ctx"]]}'
        if is_em and edge:
            style += f';--e:{HEX[edge]}'
        cls = 'ch-bar em' + (' edge' if is_em and edge else '') if is_em else 'ch-bar'
        red = red_attr(em, 'specimen', 'the one point the title names') if is_em else ''
        chk = echk if is_em else (cchk if m == 'Jan.' else '')
        cols.append(f'<span class="ch-col{" em" if is_em else ""}"><span class="ch-v">{val}</span>'
                    f'<span class="{cls}" data-mark="bar" data-axis="y" data-value="{v}" data-key="{m}" style="{style}"{chk}{red}></span></span>')
        xs.append(f'<span{" class=\"em\"" if is_em else ""}>{E(m)}</span>')
    cap = f'March in {em}, its value and name in bold; other months in Stone, {rs("Stone", "Newsprint")}. {s["chart_note"]}'
    return (f'<figure class="m-chart ch" data-spec="cs-{s["key"]}">{m_h("Chart")}'
            f'<figcaption><p class="ch-t">Comments on the county budget peaked in March, the month of the hearing.</p>'
            f'<p class="ch-s"><span>Comments received each month</span><span class="illus">Illustrative data</span></p></figcaption>'
            f'<div class="ch-plot" aria-hidden="true">{"".join(cols)}</div><div class="ch-x" aria-hidden="true">{"".join(xs)}</div>'
            f'<p class="sr">Comments received: {", ".join(f"{m} {v}" for m, v in CHART)}.</p>'
            f'<p class="cap">{E(cap)}</p></figure>')


def sec_jobs(s):
    P.add('Text on the tint', 'Charcoal', s['tint'], 'text')
    lis = ''.join(f'<li>{E(j)}</li>' for j in s['jobs'])
    return (f'<div class="m-jobs" style="--tint:{HEX[s["tint"]]}"><p class="m-h">{E(s["lead"])}\'s jobs</p>'
            f'<p class="kl">{E(s["kind_line"])}</p><ul class="jl">{lis}</ul>'
            f'<p class="lim"><b>Limit.</b> {E(s["limit"])}</p>'
            f'<p class="tint-n">On {E(s["tint"])}, {HEX[s["tint"]]}: Charcoal text at {rs("Charcoal", s["tint"])}.</p></div>')


def sec_party(s):
    return (f'<div class="m-party">{m_h("Party reading")}<p class="risk">{E(s["party_level"])}</p>'
            f'<p>{E(s["party"])}</p>'
            f'<p class="rule">No party takes the lead. Party marks print in Charcoal with the party\'s name (DR-48), '
            f'under one standard of evidence (DR-93).</p></div>')


def sec_refs(s):
    # Inter's contextual alternates draw "2x4" as "2×4"; the studio's name keeps its letter x
    lis = ''.join(f'<li>{E(r).replace("2x4", "<span class=\"nc\">2x4</span>")}</li>' for r in s['refs'])
    return f'<div class="m-refs">{m_h("References")}<ol class="refs">{lis}</ol><p class="cap">From the research lead\'s memo of November 7, 2026.</p></div>'


def err_glyph():
    return ('<svg class="eg" width="18" height="18" viewBox="0 0 18 18" aria-hidden="true" focusable="false">'
            f'<circle cx="9" cy="9" r="7.5" fill="{HEX["Pillar Red"]}" stroke="{HEX["Charcoal"]}"/>'
            f'<path d="M6 6l6 6M12 6l-6 6" stroke="{HEX["Newsprint"]}" stroke-width="1.75"/></svg>')


def sec_sys(s):
    P.add('Error text on Error Band', 'Charcoal', 'Error Band', 'text')
    P.add('Error glyph edge on Error Band', 'Charcoal', 'Error Band', 'mark')
    P.add('Error glyph fill inside its Charcoal edge', 'Pillar Red', 'Error Band', 'mark', exempt='a fill inside a Charcoal edge')
    a, b, note = s['div']
    P.add('Diverging end on Newsprint', a, 'Newsprint', 'mark')
    P.add('Diverging end on Newsprint', b, 'Newsprint', 'mark')
    job = 'error' if s['kind'] == 'today' else 'error state'
    errbox = (f'<span class="err"{red_attr("Pillar Red", "specimen", job)}>{err_glyph()}'
              f'<span><b>Error:</b> Enter a ZIP code with five digits.</span></span>')
    chips = (f'<span class="dv"><span class="dvc" style="background:{HEX[a]}"></span><span class="dvc" style="background:{HEX["Newsprint"]}">'
             f'</span><span class="dvc" style="background:{HEX[b]}"></span></span>')
    return (f'<div class="m-sys">{m_h("States and scales" if s["kind"] == "today" else "What else changes")}<div class="sys">'
            f'<dl><dt>Error</dt><dd>{errbox}<span class="dd-n">{E(s["error_note"])}</span></dd>'
            f'<dt>Focus ring</dt><dd>{E(s["focus_note"])}</dd></dl>'
            f'<dl><dt>Diverging scale</dt><dd>{chips}<span class="dd-n">{E(note)}</span></dd>'
            f'<dt>Print</dt><dd>{E(s["print_note"])}</dd></dl></div></div>')


def sheet(s):
    P.start(s['key'])
    P.add('Sheet text', 'Charcoal', 'Newsprint', 'text')
    P.add('Module labels', s['ink2'], 'Newsprint', 'text')
    P.add('Captions', 'Deep Stone', 'Newsprint', 'text')
    parts = [sec_head(s), sec_palette(s), f'<div class="m-side">{sec_type(s)}{sec_refs(s)}</div>', sec_card(s), sec_icons(s),
             sec_dark(s), sec_buttons(s), sec_chart(s), sec_jobs(s), sec_party(s), sec_sys(s)]
    return (f'<article class="cs cs-{s["key"]}" data-sheet="{s["key"]}" style="--ink2:{HEX[s["ink2"]]}">'
            f'<div class="cs-in"><div class="cs-top"><span>Oath &amp; Action identity sheet · {s["n"]} of 7</span>'
            f'<span>{E(s["status"])}</span></div><div class="cs-g">{"".join(parts)}</div></div></article>')


# ------------------------------------------------------------------------------------------------ board sections
def sec_overview(sheets):
    thumbs = []
    for s in SCHEMES:
        thumbs.append(f'<li class="thumb"><a href="#sheet-{s["key"]}"><span class="thumb-box" aria-hidden="true">{sheets[s["key"]]}</span>'
                      f'<span class="thumb-t"><b>{s["n"]} {E(s["name"])}</b><span>{E(s["feel"])}</span>'
                      f'<span class="hx">{HEX[s["lead"]]}</span></span></a></li>')
    rows = []
    for s in SCHEMES:
        L = s['lead']
        lab_on = s['ask_label']
        red = red_attr(L, 'specimen', 'palette swatch')
        rows.append(f'<tr><th scope="row"><span class="sw"><span class="chip" style="background:{HEX[L]}"{red}></span>'
                    f'<span><a href="#sheet-{s["key"]}">{s["n"]} {E(s["name"])}</a></span></span></th>'
                    f'<td data-label="Feel">{E(s["feel"])}</td>'
                    f'<td class="num" data-label="Lead">{HEX[L]}</td>'
                    f'<td class="num" data-label="On Newsprint">{ratio(L, "Newsprint"):.2f} <span class="vd">{verdict(L, "Newsprint")}</span></td>'
                    f'<td class="num" data-label="On Charcoal">{ratio(L, "Charcoal"):.2f} <span class="vd">{verdict(L, "Charcoal")}</span></td>'
                    f'<td class="num" data-label="Ask label">{E(lab_on)} {ratio(lab_on, s["ask_fill"]):.2f}</td>'
                    f'<td data-label="Party reading">{E(s["party_level"])}</td>'
                    f'<td data-label="What else changes">{E(s["change"])}</td></tr>')
    return f'''<section id="all-seven" aria-labelledby="all-seven-h"><p class="secnum">01</p>
<h2 id="all-seven-h">All seven at once</h2>
<div class="lede"><p>Every sheet has the same layout and the same content, so only the color changes. Select a sheet to open it at full size. The small sheets are pictures; their type is too small to read here.</p></div>
<div class="thumbs-w" role="region" aria-label="The seven sheets, side by side"><ol class="thumbs">{"".join(thumbs)}</ol></div>
<h3 class="sub">The seven leads, measured</h3>
<div class="tw"><table class="cmp stk"><thead><tr><th scope="col">Sheet</th><th scope="col">Feel</th><th scope="col">Lead</th>
<th scope="col">On Newsprint</th><th scope="col">On Charcoal</th><th scope="col">Ask label</th><th scope="col">Party reading</th>
<th scope="col">What else changes</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<p class="small">"Ask label" is the label color on the ask button's fill and its ratio. The party readings are the research lead's design judgments from the sources in her memo; no reader was asked.</p>
</section>'''


def sec_sheet(s, num, html_sheet):
    intro = {
        'patina': 'The green that copper roofs and statues weather to, one step deeper than today\'s Verdigris. It reads as calm public authority.',
        'federal-ink': 'Today\'s Prussian, promoted to lead, with a GOV.UK-style yellow focus. It reads as the government document and the court opinion.',
        'signal-orange': 'The bulletin and the deadline. It keeps the energy red gives the brand today in a different hue.',
        'archive-ochre': 'The record room: bound volumes, brass plaques and iron-gall ink.',
        'highlighter': 'The marked-up page, the newsletter and the social card. The lead is a fill behind dark type and never an ink.',
        'ballot-violet': 'The suffrage banner, the polling place and the neighborhood meeting.',
        'today': 'Today\'s palette at the same size, with Pillar Red\'s own measured values, so the six sheets have a fixed point.',
    }[s['key']]
    return (f'<section id="sheet-{s["key"]}" class="sheet-sec" aria-labelledby="sheet-{s["key"]}-h"><p class="secnum">{num:02d}</p>'
            f'<h2 id="sheet-{s["key"]}-h">{s["n"]} {E(s["name"])}<span class="chip-f">{E(s["feel"])}</span></h2>'
            f'<div class="lede"><p>{E(intro)}</p></div>{html_sheet}</section>')


def sec_checks(render):
    det = []
    for s in SCHEMES:
        rows = []
        for r in P.by[s['key']]:
            if r['ratio'] >= r['need']:
                res = 'passes'
            elif r['exempt'] and r['exempt'].startswith('a fill inside'):
                res = 'passes by its Charcoal edge'
            else:
                res = 'accepted today: ' + r['exempt']
            rows.append(f'<tr><td>{E(r["where"])}</td><td>{E(r["fg"])} <span class="hx">{r["fg_hex"]}</span></td>'
                        f'<td>{E(r["bg"])} <span class="hx">{r["bg_hex"]}</span></td><td class="num">{r["ratio"]:.2f}:1</td>'
                        f'<td class="num">{r["need"]:g}:1 {r["kind"]}</td><td>{E(res)}</td></tr>')
        under = [r for r in P.by[s['key']] if r['exempt'] and r['ratio'] < r['need']]
        n_edge = sum(1 for r in under if r['exempt'].startswith('a fill inside'))
        n_today = len(under) - n_edge
        tail = ''.join([f'; {n_edge} {"fill passes" if n_edge == 1 else "fills pass"} by a Charcoal edge' if n_edge else '',
                        f'; {n_today} red marks at 2.96:1 that today\'s guide accepts' if n_today else ''])
        det.append(f'<details class="pairs"><summary>{s["n"]} {E(s["name"])}: {len(P.by[s["key"]])} pairs{tail}</summary>'
                   f'<div class="tw" role="region" aria-label="{A(s["name"])} pairs" tabindex="0"><table class="stk"><thead><tr><th scope="col">Where</th><th scope="col">Color</th>'
                   f'<th scope="col">On</th><th scope="col">Ratio</th><th scope="col">Needs</th><th scope="col">Result</th></tr></thead>'
                   f'<tbody>{"".join(rows)}</tbody></table></div></details>')
    total = sum(len(v) for v in P.by.values())
    rend = ''
    if render:
        rend = (f'<p>The render script read the painted color of {render.get("checked", 0)} marks, labels and rings at 1440 px and '
                f'compared each with its ground: {render.get("failures", 0)} fell under the ratio this page prints for them, and '
                f'{render.get("mismatch", 0)} painted a different color from the one measured here.</p>')
    return f'''<section id="checks" aria-labelledby="checks-h"><p class="secnum">09</p>
<h2 id="checks-h">How the sheets were measured</h2>
<div class="lede"><p>The build computes every ratio on this page from the WCAG 2.2 formula and stops when a pair falls under its threshold: 4.5 to 1 for text, and 3 to 1 for type from 24 px (18.66 px bold), marks, control edges and focus rings. Its values match the research lead's memo to the hundredth. Two kinds of pair sit under 3 to 1 on purpose, and each is named below: a fill inside a Charcoal keyline or edge, where the edge carries the contrast as Rule 05.5 asks, and, on today's sheet only, the red marks the guide accepts as signature red or as large type.</p></div>
<p>The sheets print {total} pairs in all. Open a sheet to see each one.</p>
{rend}
{"".join(det)}
</section>'''


DECISIONS = [
    dict(id='C1', q='Which lead should the studio develop into a full color proposal for chapter 05?',
         opts=['Patina', 'Federal Ink', 'Signal Orange', 'Archive Ochre', 'Highlighter', 'Ballot Violet', 'Keep Pillar Red'],
         rec='a', why='Patina does every job with one hex on Newsprint and on Charcoal, reads civic, and carries the lowest party reading of the six. It costs two token changes, both shown on its sheet.'),
    dict(id='C2', q='If the lead changes, where does red go?',
         opts=['Pillar Red stays as the error state only, with its glyph and the word Error',
               'Error moves to the new lead\'s deep partner, and red leaves the palette'],
         rec='a', why='Readers already know a red error, and the guide keeps state color apart from identity color. The glyph and the word carry the error for every reader.'),
    dict(id='C3', q='How is the pick tested before you approve it?',
         opts=['Add it to the reader check with the party question, and print a press proof on newsprint',
               'Approve it from the screen'],
         rec='a', why='No reader has been asked how any of these colors reads for party, and no lead has been printed on newsprint.'),
]


def sec_decisions():
    cards = []
    for d in DECISIONS:
        ol = ''.join(f'<li><b>{chr(97 + i)}</b> {E(t)}{" <span class=\"chip chip-rec\">Recommended</span>" if chr(97 + i) == d["rec"] else ""}</li>'
                     for i, t in enumerate(d['opts']))
        cards.append(f'<li class="dec"><p class="dec-id">{d["id"]}</p><p class="dec-q">{E(d["q"])}</p>'
                     f'<ol class="dec-o">{ol}</ol><p class="dec-why"><b>Why {d["rec"]}.</b> {E(d["why"])}</p></li>')
    sample = ', '.join(f'{d["id"]} {d["rec"]}' for d in DECISIONS)
    return f'''<section id="answers" aria-labelledby="answers-h"><p class="secnum">10</p>
<h2 id="answers-h">Your answers</h2>
<div class="lede"><p>Three questions, each with the studio's recommendation. Pillar Red stays in force until you approve a change by name, and nothing in the guide changes until you pick (D2-320). A reply of letters is enough, for example "{sample}".</p></div>
<ol class="decs">{"".join(cards)}</ol>
</section>'''


# ------------------------------------------------------------------------------------------------ page
CSS = r"""
/* Board 6, section 4. The Board 5 frame on Newsprint, set from the inlined tokens. Each sheet is a 1,200 px artboard. */
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;font:400 1rem/1.6 var(--oa-font-family-reading);background:var(--oa-color-palette-newsprint);color:var(--oa-color-palette-charcoal)}
a{color:inherit;text-underline-offset:3px}
:focus-visible{outline:3px solid var(--oa-color-palette-charcoal);outline-offset:3px}
.board{max-width:1344px;margin:0 auto;padding:40px 32px 96px}
.mast{display:flex;justify-content:space-between;align-items:baseline;gap:16px;border-bottom:2px solid var(--oa-color-palette-charcoal);padding-bottom:14px}
.mast b{font:800 1.25rem/1 var(--oa-font-family-display);letter-spacing:-.02em;white-space:nowrap}
.mast span{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);text-align:right}
.eyebrow{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);margin:28px 0 0}
h1,h2,h3{font-family:var(--oa-font-family-display);font-weight:800;text-wrap:balance;margin:0}
h1{font-size:var(--oa-type-section-font-size);line-height:var(--oa-type-section-line-height);letter-spacing:var(--oa-type-section-letter-spacing);margin-top:10px;max-width:20ch}
h2{font-size:var(--oa-type-h3-font-size);line-height:var(--oa-type-h3-line-height);letter-spacing:var(--oa-type-h3-letter-spacing);margin:0 0 14px;display:flex;flex-wrap:wrap;align-items:center;gap:8px 14px}
h3.sub{font-size:var(--oa-type-h4-font-size);line-height:var(--oa-type-h4-line-height);letter-spacing:var(--oa-type-h4-letter-spacing);margin:40px 0 12px}
p{margin:0 0 12px;max-width:68ch}
.deck{font:var(--oa-type-intro);max-width:60ch;margin-top:18px}
.lede p{font-size:1.125rem;line-height:1.6;max-width:62ch}
section{border-top:1px solid var(--oa-color-palette-stone);margin-top:64px;padding-top:28px}
.secnum{font:var(--oa-type-label);letter-spacing:.06em;color:var(--oa-color-derived-deep-stone);margin:0 0 6px}
.small{font-size:.9375rem;color:var(--oa-color-derived-deep-stone);margin-top:12px}
.toc{display:flex;flex-wrap:wrap;gap:0 22px;margin:24px 0 0;padding:6px 0;border-top:1px solid var(--oa-color-palette-stone);border-bottom:1px solid var(--oa-color-palette-stone);list-style:none}
.toc a{font:600 .9375rem/1.3 var(--oa-font-family-reading);text-decoration:none;display:inline-flex;align-items:center;min-height:44px}
.toc a:hover{text-decoration:underline}
.recbox{background:var(--oa-color-palette-white);border:1px solid var(--oa-color-palette-charcoal);padding:20px 24px;margin-top:28px;max-width:88ch}
.recbox p{max-width:none}.recbox p:last-child{margin:0}
.key-h{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;margin:0 0 8px}
.chip{display:inline-block;font:700 .8125rem/1 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;padding:5px 7px;border:1px solid currentColor;vertical-align:middle;white-space:nowrap}
.chip-rec{background:var(--oa-color-palette-charcoal);color:var(--oa-color-palette-newsprint);border-color:var(--oa-color-palette-charcoal)}
.chip-f{font:700 .8125rem/1 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;padding:6px 8px;border:1px solid var(--oa-color-palette-charcoal)}
.sr{position:absolute!important;width:1px!important;height:1px!important;overflow:hidden!important;clip:rect(0 0 0 0);clip-path:inset(50%);white-space:nowrap;margin:0!important;padding:0!important}
code{font:500 max(13px,.875em)/1.4 ui-monospace,Menlo,monospace;overflow-wrap:anywhere}
.tw{overflow-x:auto;max-width:100%}
table{border-collapse:collapse;width:100%;font-size:.9375rem}
th,td{text-align:left;vertical-align:top;padding:10px 14px 10px 0;border-bottom:1px solid var(--oa-color-palette-stone)}
thead th{font:var(--oa-type-label);letter-spacing:.06em;text-transform:uppercase;color:var(--oa-color-derived-deep-stone);border-bottom:2px solid var(--oa-color-palette-charcoal);vertical-align:bottom}
tbody th{font-weight:700}
td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.hx{font-variant-numeric:tabular-nums;color:var(--oa-color-derived-deep-stone)}
.vd{font-size:.8125rem;color:var(--oa-color-derived-deep-stone)}
.sw{display:inline-flex;align-items:center;gap:10px}
.chip,.cmp .chip{flex:none}
.cmp .chip{display:inline-block;width:22px;height:22px;padding:0;border:1px solid var(--oa-color-palette-charcoal)}
.cmp a{font-weight:700}

/* the strip of seven */
.thumbs-w{margin-top:16px;overflow-x:auto;max-width:100%}
.thumbs{list-style:none;margin:0;padding:0 0 4px;display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:12px}
.thumb a{display:block;text-decoration:none}
.thumb a:hover .thumb-t b{text-decoration:underline}
.thumb-box{display:block;position:relative;overflow:hidden;width:100%;height:220px;border:1px solid var(--oa-color-palette-charcoal)}
.thumb-box > .cs{position:absolute;left:0;top:0;width:1200px;max-width:none;transform-origin:0 0;transform:scale(.142);border:0;pointer-events:none}
.thumb-t{display:flex;flex-direction:column;margin-top:8px;font-size:.875rem;line-height:1.35}
.thumb-t b{font:800 1rem/1.2 var(--oa-font-family-display)}
.sheet-sec .lede{margin-bottom:18px}

/* checks */
details.pairs{border-top:1px solid var(--oa-color-palette-stone);padding:4px 0}
details.pairs summary{cursor:pointer;font-weight:700;min-height:44px;display:flex;align-items:center}
details.pairs table{font-size:.875rem;margin:4px 0 12px}
details.pairs td,details.pairs th{padding:6px 12px 6px 0}

/* decisions */
.decs{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr))}
.dec{background:var(--oa-color-palette-white);border:1px solid var(--oa-color-palette-stone);padding:20px 24px}
.dec-id{font:800 1.5rem/1 var(--oa-font-family-display);margin:0 0 6px}
.dec-q{font:700 1.125rem/1.4 var(--oa-font-family-reading);margin:0 0 10px}
.dec-o{list-style:none;margin:0 0 10px;padding:0}.dec-o li{margin:0 0 6px}.dec-o b{display:inline-block;min-width:1.4em}
.dec-why{margin:0;font-size:.9375rem}
.foot{margin-top:64px;border-top:2px solid var(--oa-color-palette-charcoal);padding-top:16px;font-size:.875rem;color:var(--oa-color-derived-deep-stone)}

/* ============================================================ the sheet, a 1,200 px artboard */
.cs{container:sheet/inline-size;position:relative;width:100%;max-width:1200px;background:#DCD9D2;color:#121212;border:1px solid #121212;
  font:400 14px/1.45 var(--oa-font-family-reading)}
.cs p{margin:0;max-width:none}
.cs-in{padding:32px 40px 40px}
.cs-top{display:flex;justify-content:space-between;flex-wrap:wrap;gap:4px 16px;padding-bottom:10px;border-bottom:2px solid #121212;
  font:700 13px/1.3 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
.cs-g{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));column-gap:24px;row-gap:26px;margin-top:20px;
  grid-template-areas:"head head head head head head head head hero hero hero hero" "pal pal pal pal pal pal pal side side side side side"
  "card card card card icons icons icons icons dark dark dark dark" "btn btn btn btn chart chart chart chart jobs jobs jobs jobs"
  "party party party party sys sys sys sys sys sys sys sys";grid-template-rows:/*ROWS*/}
.m-head{grid-area:head;align-self:end}.m-hero{grid-area:hero}.m-pal{grid-area:pal}.m-side{grid-area:side}
.m-card{grid-area:card}.m-icons{grid-area:icons}.m-dark{grid-area:dark}
.m-btn{grid-area:btn}.m-chart{grid-area:chart}.m-jobs{grid-area:jobs}
.m-party{grid-area:party}.m-sys{grid-area:sys}
.m-side .m-refs{margin-top:22px}
.cs .m-h{font:700 13px/1.3 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2);
  border-top:2px solid #121212;padding-top:8px;margin:0 0 12px}
.cs .cap{font-size:13px;line-height:1.45;color:#4E535B;margin-top:8px}
.cs svg{display:block;flex:none;overflow:visible}

.m-head .wm{width:100%;max-width:640px;height:auto}
.m-head .cap{margin-top:12px}
.m-hero{background:var(--hero);color:var(--hero-ink);padding:18px 20px 18px;display:flex;flex-direction:column;gap:6px;min-height:156px;justify-content:flex-end}
.m-hero .h-n{font:800 44px/1 var(--oa-font-family-display);letter-spacing:-.025em}
.m-hero .h-f,.m-hero .h-x{font:700 19px/1.25 var(--oa-font-family-reading)}
.m-hero .h-x{font-variant-numeric:tabular-nums}

.pal{width:100%;border-collapse:collapse;font-size:14px}
.pal th,.pal td{padding:4px 10px 4px 0;border-bottom:1px solid #5D636D;vertical-align:middle;text-align:left}
.pal thead th{font:700 13px/1.3 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;color:#4E535B;border-bottom:2px solid #121212;padding-bottom:6px}
.pal tbody th{font-weight:400}
.pal .sw{display:grid;grid-template-columns:28px minmax(0,1fr);column-gap:10px;align-items:center}
.pal .chip{display:block;width:28px;height:28px;padding:0;border:1px solid #121212}
.pal .sw-t{display:flex;flex-direction:column;line-height:1.2}
.pal .pn{font-weight:700}.pal .pr{font-size:13px;color:#4E535B}
.pal .hx{font-variant-numeric:tabular-nums;color:#121212;white-space:nowrap}
.pal td b{font-variant-numeric:tabular-nums}
.pal .vd{font-size:13px;color:#4E535B}

.ty + .ty{margin-top:16px;padding-top:14px;border-top:1px solid #5D636D}
.ty-l{font:700 13px/1.3 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2);margin-bottom:8px!important}
.ty-a{font:800 38px/1.05 var(--oa-font-family-display);letter-spacing:-.01em;text-wrap:balance}
.ty-b{font:400 17px/1.6 var(--oa-font-family-reading)}
.ty-c{font:italic 400 24px/1.3 var(--oa-font-family-quote);letter-spacing:-.02em}

.card{border:1px solid #5D636D;padding:16px 18px 14px;display:flex;flex-direction:column;gap:10px}
.illus{display:inline-block;align-self:flex-start;padding:0 .4em;border:1px solid currentColor;font:700 13px/1.5 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;white-space:nowrap}
.kick{display:flex;align-items:center;gap:10px;font:700 13px/1.3 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
.hl{font:800 28px/1.08 var(--oa-font-family-display);letter-spacing:-.01em}
.hl .nw{white-space:nowrap}
.hl .hb{display:inline-block;line-height:0}
.hl .hb svg{display:inline-block}
.hl .band{background:var(--band);padding:0 .14em;margin-left:-.14em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.dek{font:400 15px/1.5 var(--oa-font-family-reading)}
.cfoot{margin-top:auto;padding-top:10px;border-top:1px solid #5D636D}

.pillars{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.pillars li{display:flex;flex-direction:column;align-items:center;gap:6px;font:600 14px/1.2 var(--oa-font-family-reading)}
.ic{display:block;line-height:0}
.lkrow{display:flex;align-items:flex-end;gap:24px}

.m-dark{background:#121212;color:#DCD9D2;padding:2px 18px 18px;align-self:start}
.m-dark .m-h{color:#DCD9D2;border-top:0;padding-top:14px;border-bottom:1px solid #5D636D;padding-bottom:10px}
.m-dark .cap{color:#A3A19C}
.drow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;align-items:end}
.dcell{display:flex;flex-direction:column;align-items:flex-start;gap:8px}
.dl{font:600 13px/1.3 var(--oa-font-family-reading);color:#DCD9D2}
.dask{margin-top:20px!important}

.st + .st{margin-top:10px}
.st-l{display:flex;flex-wrap:wrap;gap:0 8px;align-items:baseline;font-size:13px;line-height:1.35;margin-bottom:4px!important}
.st-l b{font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:var(--ink2)}
.st-l span{color:#4E535B}
.ask{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:0 20px;background:var(--f);color:var(--l);
  font:var(--oa-type-ask);letter-spacing:var(--oa-type-ask-letter-spacing);white-space:nowrap}
.ask.edge{box-shadow:inset 0 0 0 1px var(--e)}
.ask.hov{text-decoration:underline;text-decoration-thickness:2px;text-underline-offset:.2em}
.ask.foc{outline:2px solid var(--r);outline-offset:2px}
.ask.dis{background:transparent;color:#4E535B;border:1px dashed #4E535B}
.reason{font-size:13px;color:#4E535B;margin-top:4px!important}

.ch{margin:0}
.ch-t{font:700 15px/1.35 var(--oa-font-family-reading);text-wrap:balance}
.ch-s{display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;font-size:13px;color:#4E535B;margin-top:6px!important}
.ch-s .illus{color:#121212}
.ch-plot{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));column-gap:10px;align-items:end;height:144px;margin-top:12px;border-bottom:1px solid #121212}
.ch-col{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%}
.ch-v{font:600 13px/1.2 var(--oa-font-family-reading);font-variant-numeric:tabular-nums;margin-bottom:4px}
.ch-col.em .ch-v{font-weight:800}
.vband{background:var(--band);padding:1px 4px}
.ch-bar{display:block;width:72%;background:var(--c)}
.ch-bar.edge{box-shadow:inset 0 0 0 1px var(--e)}
.ch-x{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));column-gap:10px;margin-top:6px;font-size:13px;text-align:center}
.ch-x .em{font-weight:800}

.m-jobs{background:var(--tint);color:#121212;padding:2px 18px 16px;align-self:start}
.m-jobs .m-h{color:#121212;border-top:0;padding-top:14px;border-bottom:2px solid #121212;padding-bottom:8px}
.kl{font-weight:700}
.jl{margin:8px 0 0;padding-left:1.1em}.jl li{margin:0 0 4px}
.lim{margin-top:10px!important}
.tint-n{margin-top:10px!important;padding-top:8px;border-top:1px solid #121212;font-size:13px}

.risk{font:800 22px/1.15 var(--oa-font-family-display);letter-spacing:-.01em;margin-bottom:8px!important;text-wrap:balance}
.m-party p + p{margin-top:8px}
.m-party .rule{font-size:13px;color:#4E535B}
.refs{margin:0;padding-left:1.25em}.refs li{margin:0 0 8px}
.nc{font-feature-settings:"calt" 0}

.sys{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:24px}
.sys dl{margin:0}
.sys dt{font:700 13px/1.3 var(--oa-font-family-reading);letter-spacing:.06em;text-transform:uppercase;color:var(--ink2);margin-top:8px}
.sys dt:first-child{margin-top:0}
.sys dd + dt{margin-top:14px}
.sys dd{margin:0}
.dd-n{display:block;margin-top:6px}
.err{display:flex;gap:10px;align-items:flex-start;background:#E1C9C1;color:#121212;padding:8px 10px}
.err .eg{margin-top:1px}
.dv{display:inline-flex;gap:0;border:1px solid #121212;vertical-align:middle}
.dvc{display:block;width:34px;height:16px}

/* 1,099 px and narrower: two columns */
@container sheet (max-width: 1099px){
  .cs-in{padding:28px 28px 32px}
  .cs-g{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-areas:none;grid-template-rows:none}
  .cs-g > *{grid-area:auto}
  .m-head,.m-pal,.m-side,.m-sys{grid-column:1/-1}
}
/* 640 px and narrower: one column */
@container sheet (max-width: 640px){
  .cs-in{padding:20px 16px 24px}
  .cs-g{grid-template-columns:minmax(0,1fr);row-gap:26px}
  .m-head,.m-pal,.m-side,.m-sys{grid-column:auto}
  .sys{grid-template-columns:minmax(0,1fr)}.sys dl + dl{margin-top:14px}
  .m-hero .h-n{font-size:36px}
  .ty-a{font-size:30px}
  .pal thead{display:none}
  .pal,.pal tbody,.pal tr,.pal th,.pal td{display:block;width:100%}
  .pal tr{display:grid;grid-template-columns:repeat(3,auto);justify-content:start;column-gap:16px;row-gap:2px;padding:8px 0;border-bottom:1px solid #5D636D}
  .pal th{grid-column:1/-1;border:0;padding:0 0 4px}
  .pal td{border:0;padding:0}
  .pal td[data-k]::before{content:attr(data-k);display:block;font-size:13px;color:#4E535B}
  .lkrow{gap:16px}
  .drow{grid-template-columns:repeat(3,auto);justify-content:start;gap:16px}
}

@media (max-width:1000px){.thumbs{grid-template-columns:repeat(7,150px)}}
@media (max-width:760px){
.board{padding:24px 16px 64px}
.mast{flex-direction:column;gap:6px}.mast span{text-align:left}
.lede p{font-size:1.0625rem}
table.stk,table.stk tbody,table.stk tr,table.stk th,table.stk td{display:block;width:100%}
table.stk thead{display:none}table.stk tr{border-bottom:1px solid var(--oa-color-palette-stone);padding:10px 0}
table.stk th,table.stk td{border:0;padding:2px 0}
table.stk td[data-label]::before{content:attr(data-label) ": ";font-weight:700}
.recbox,.dec{padding:16px}
}
"""

JS = r"""
(function(){
  function fit(){
    document.querySelectorAll('.thumb-box').forEach(function(b){
      var s = b.firstElementChild; if (!s) return;
      var k = b.clientWidth / 1200;
      s.style.transform = 'scale(' + k + ')';
      b.style.height = Math.ceil(s.offsetHeight * k) + 'px';
    });
    document.querySelectorAll('.thumbs-w,.tw').forEach(function(f){
      if (f.scrollWidth > f.clientWidth + 1) { f.tabIndex = 0; f.setAttribute('role','region'); if(!f.getAttribute('aria-label')) f.setAttribute('aria-label','Wide table'); }
      else if (!f.closest('details')) { f.removeAttribute('tabindex'); }
    });
  }
  window.addEventListener('resize', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  fit();
})();
"""


def curl_page(page):
    parts = re.split(r'(<style[^>]*>.*?</style>|<script[^>]*>.*?</script>|<[^>]+>)', page, flags=re.S)
    out = []
    for part in parts:
        if part.startswith('<'):
            out.append(part)
        else:
            t = part.replace('&quot;', '"').replace('&#x27;', "'")
            out.append(copy(t))
    return ''.join(out)


def build():
    render = json.loads(RENDER.read_text()) if RENDER.exists() else None
    tokens = TOKENS.read_text()
    sheets = {s['key']: sheet(s) for s in SCHEMES}
    # the strip's copies carry no ids and no focusable element; the full sheets below are the record
    for k, v in sheets.items():
        if re.search(r'\sid="', v) or re.search(r'<(a|button|input)\b|tabindex', v):
            sys.exit(f'sheet {k} carries an id or a focusable element')
    head_rec = ('<div class="recbox"><p class="key-h">What we recommend</p>'
                '<p>We recommend Patina. It does every job with one hex on Newsprint and on Charcoal, reads as civic, and '
                'carries the lowest party reading of the six. It costs two token changes, shown on its sheet: the focus ring '
                'moves to Charcoal, and the diverging scale\'s green end moves to Brass. If you want to keep the urgency red '
                'gives the brand today, Signal Orange is the second choice, and it changes no token.</p></div>')
    toc = [('all-seven', 'All seven')] + [(f'sheet-{s["key"]}', f'{s["n"]} {s["name"]}') for s in SCHEMES] + \
          [('checks', 'Measurements'), ('answers', 'Your answers')]
    tocs = ''.join(f'<li><a href="#{a}">{E(t)}</a></li>' for a, t in toc)
    body = sec_overview(sheets) + ''.join(sec_sheet(s, i + 2, sheets[s['key']]) for i, s in enumerate(SCHEMES)) + \
        sec_checks(render) + sec_decisions()
    deck = ('You asked which colors could lead if red stepped back from the front. Each sheet keeps Newsprint, Charcoal, '
            'the three faces, the hinge and the approved marks, and changes the lead color and its partners. A seventh '
            'sheet shows today\'s palette at the same size.')
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Color Scheme Sheets</title>
<meta name="description" content="Board 6, section 4: six one-page identity sheets for Oath &amp; Action, each led by a color other than red, beside today's palette.">
<meta name="chart-views" content="overview">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{A(FONTS)}" rel="stylesheet">
<style>
{tokens}
</style>
<style>{CSS}</style>
</head>
<body class="oa-surface-newsprint">
<main class="board" id="overview" data-view-root="overview">
<header>
<div class="mast"><b>Oath &amp; Action</b><span>Board 6, section 4 of 4 · November 7, 2026</span></div>
<p class="eyebrow">Board 6 · Color and identity designer</p>
<h1>Six color schemes for Oath&nbsp;&amp;&nbsp;Action, with today's palette beside them</h1>
<p class="deck">{E(deck)}</p>
{head_rec}
<nav aria-label="On this board"><ul class="toc">{tocs}</ul></nav>
</header>
{body}
<footer class="foot"><p>Built by <code>work/build/scripts/phase-2/board6_color_sheets_build.py</code> on November 7, 2026, from the approved masters, the Civic Line drawings and <code>tokens.css</code>, with only the ampersand's fill, the lever's fill and the icons' red parts recolored. The article card, its county and the chart's figures are invented, and each carries an Illustrative label. Every ratio on the page is computed by the build. Notes: <code>work/handoffs/phase-2/20261107_Board-6-Color-Sheets-Notes.md</code>.</p></footer>
</main>
<script>{JS}</script>
</body>
</html>
'''
    rows = (render or {}).get('rows')
    page = page.replace('grid-template-rows:/*ROWS*/', 'grid-template-rows:' + (' '.join(f'{h}px' for h in rows) if rows else 'auto'))
    head, sep, rest = page.partition('<body')
    page = head + curl_page(sep + rest)
    text = re.sub(r'<(style|script)[^>]*>.*?</\1>', ' ', page, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', text)
    lint_text(html.unescape(text), 'page copy')
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT.write_text(page)
    PAIRS_OUT.write_text(json.dumps({'date': '2026-11-07', 'formula': 'WCAG 2.2 relative luminance',
                                     'colors': HEX, 'sheets': P.by}, indent=1, ensure_ascii=False))
    for w in LINT:
        print('warning', w)
    n = sum(len(v) for v in P.by.values())
    ex = sum(1 for v in P.by.values() for r in v if r['exempt'] and r['ratio'] < r['need'])
    print(f'wrote {OUT.relative_to(ROOT)} ({len(page) / 1024:.0f} KB), {n} pairs, {ex} accepted under threshold'
          f'{", with render results" if render else ""}')


if __name__ == '__main__':
    build()
