"""Chapter 18, Components and interaction (accessibility lead), stage C round 1, November 11, 2026.

Usage:
    python3 -I work/build/scripts/phase-2/stage_c_ch18_build.py            write the chapter, its plates and the keys files
    python3 -I work/build/scripts/phase-2/stage_c_ch18_build.py --check    write nothing; exit 1 if any output differs
    python3 -I work/build/scripts/phase-2/stage_c_ch18_build.py --notes    print the anatomy labels and the component
                                                                          engineer's hooks as Markdown, for the notes

Writes:
    work/build/guide/chapters/18-components.json          the chapter in the content contract (round 1 brief)
    work/build/guide/specimens/s-18-NN-failure.html       one failure plate per rule, a picture of the fault
    work/build/guide/specimens/manifest-components.json   the s-18-* entries this script owns (D2-1267)
    work/build/guide/code/c-18-<name>.keys.json           one keyboard path file per code set, format oa-keys/1

Reads tokens.json for every contrast figure the chapter prints, and tokens.css's size for Rule 18.14's example.

Rules 18.1 to 18.24 are the inventory's components 18-01 to 18-24, in order (D2-1146), with the code set names the
main session fixed (D2-1268). Each rule's correct application is the systems designer's anatomy plate, s-18-NN-anatomy
in manifest-anatomy.json, shown pending until it lands; its code to copy is the component engineer's set; its failure
plate is drawn here. Chapter 17's and chapter 26's rules are cited by the numbers the round 1 brief fixes.

Browser support comes from MDN's browser-compat-data, version 8.1.8 (built November 2, 2026; SHA-1 of the package
5604db355f1532106c9e82b81ca8c53798772209, the research lead's copy), read November 11, 2026: the first version with
full support, with no flag, prefix, other name or partial mark (the research lead's D2-1141). The figures sit in BCD
below as read; the script does not fetch them.
"""
import argparse
import html
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parents[4]
GUIDE = ROOT / 'work/build/guide'
OUT_CH = GUIDE / 'chapters/18-components.json'
OUT_SP = GUIDE / 'specimens'
MANIFEST = OUT_SP / 'manifest-components.json'
CODE = GUIDE / 'code'
TOKENS_JSON = ROOT / 'work/build/tokens/tokens.json'
TOKENS_CSS = ROOT / 'work/build/tokens/tokens.css'
CH = '18'
WIDTH = 360          # every failure plate is a phone at 360 px, as chapter 11's are

EM, EN = '—', '–'


# ------------------------------------------------------------------------------------------------- tokens and contrast
def palette():
    """Hex values of the palette, derived and tint colors, from tokens.json."""
    data = json.loads(TOKENS_JSON.read_text())
    flat = {}

    def walk(n, p):
        if isinstance(n, dict):
            if '$value' in n:
                flat['.'.join(p)] = n['$value']
                return
            for k, v in n.items():
                if not k.startswith('$'):
                    walk(v, p + [k])
    walk(data, [])
    out = {}
    for k, v in flat.items():
        m = re.match(r'oa\.color\.(palette|derived|tint)\.(\w+)$', k)
        if m:
            out[m.group(2)] = v['hex'] if isinstance(v, dict) else v
    return out


def lum(hx):
    hx = hx.lstrip('#')
    ch = [int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


P = palette()
FIG = {}


def r2(key, fg, bg):
    """A contrast figure the chapter prints, two decimals, recorded in FIG with its colors."""
    v = ratio(P[fg], P[bg])
    txt = f'{v:.2f}'
    FIG[key] = {'value': txt, 'fg': f'{fg} {P[fg]}', 'bg': f'{bg} {P[bg]}',
                'method': 'WCAG 2.x relative luminance on the hex values in tokens.json'}
    return txt


R_RING_N = r2('focus ring on Newsprint', 'verdigris', 'newsprint')
R_RING_C = r2('focus ring on Charcoal', 'newsprint', 'charcoal')
R_DIS_N = r2('disabled text on Newsprint', 'deepStone', 'newsprint')
R_DIS_C = r2('disabled text on Charcoal', 'dimNewsprint', 'charcoal')
R_BAR_N = r2('error bar on Newsprint', 'pillarRed', 'newsprint')
R_BAR_C = r2('error bar on Charcoal', 'pillarRed', 'charcoal')
R_OK_N = r2('success mark on Newsprint', 'verdigris', 'newsprint')
R_OK_C = r2('success mark on Charcoal', 'verdigris', 'charcoal')
R_ASK = r2('ask label on Pillar Red', 'white', 'pillarRed')
# D2-1722: the guide's own scroll frames sit on the mat, the shell's --mat, which is oa.color.tint.stoneN90
R_RING_MAT = r2('focus ring on the guide’s mat', 'verdigris', 'stoneN90')
R_CHAR_MAT = r2('Charcoal ring on the guide’s mat', 'charcoal', 'stoneN90')
R_F01 = r2('failure 18.1: Dim Newsprint word on Newsprint', 'dimNewsprint', 'newsprint')
R_F05 = r2('failure 18.5: Prussian link beside Charcoal text', 'prussian', 'charcoal')
R_F15 = r2('failure 18.15: Dim Newsprint placeholder on White', 'dimNewsprint', 'white')
TOKENS_KB = f'{max(1, round(len(TOKENS_CSS.read_bytes()) / 1000)):,} KB'


def field_ground(surface):
    """The palette color a field's ground takes on a surface, read from tokens.json (call 1 of round 2's fix brief)."""
    ref = json.loads(TOKENS_JSON.read_text())['oa']['color']['field']['ground'][f'on{surface}']['$value']
    m = re.fullmatch(r'\{oa\.color\.palette\.(\w+)\}', ref)
    if not m:
        raise SystemExit(f'the field ground on {surface} is {ref}, not a palette color')
    return m.group(1)[0].upper() + m.group(1)[1:]


FIELD_N, FIELD_C = field_ground('Newsprint'), field_ground('Charcoal')
if FIELD_C != 'Charcoal':        # Rule 18.15 says the strong edge alone shows a field on Charcoal
    raise SystemExit(f'the field ground on Charcoal is {FIELD_C}; Rule 18.15 says the edge alone shows the field there')
FIELD_WORDS = f'{FIELD_N} on Newsprint and {FIELD_C} on Charcoal'
FIG['field ground'] = {'value': FIELD_WORDS, 'method': 'oa.color.field.ground.onNewsprint and .onCharcoal in tokens.json'}
CL_INVENTORY = ROOT / 'work/build/assets/civic-line-v6/20261110_Civic-Line-V6-Inventory.json'
CL_COUNT = json.loads(CL_INVENTORY.read_text())['count']          # Rule 18.15's example reads the set in use
FIG['Civic Line drawings in use'] = {'value': str(CL_COUNT), 'method': 'count in 20261110_Civic-Line-V6-Inventory.json'}
FIG['tokens.css size'] = {'value': TOKENS_KB, 'method': 'bytes of work/build/tokens/tokens.css over 1,000, rounded (D2-1209)'}


# ------------------------------------------------------------------------------------------------- browser support
# MDN browser-compat-data 8.1.8: Chrome, Edge, Firefox, Safari, Safari on iOS. "all" = every browser MDN lists, from
# versions older than ten years.
BCD = {
    'focus-visible': ('<code>:focus-visible</code>', '86', '86', '85', '15.4', '15.4'),
    'forced-colors': ('<code>forced-colors</code>', '89', '79', '89', '16', '16'),
    'reduced-motion': ('<code>prefers-reduced-motion</code>', '74', '79', '63', '10.1', '10.3'),
    'color-scheme-mq': ('<code>prefers-color-scheme</code>', '76', '79', '67', '12.1', '13'),
    'color-scheme-meta': ('<code>&lt;meta name="color-scheme"&gt;</code>', '81', '81', '96', '12.1', '12.2'),
    'localstorage': ('<code>localStorage</code>', '4', '12', '3.5', '4', '3.2'),
    'mql-change': ('the <code>change</code> event of <code>matchMedia()</code>', '39', '79', '55', '14', '14'),
    'dialog': ('<code>&lt;dialog&gt;</code> and <code>showModal()</code>', '37', '79', '98', '15.4', '15.4'),
    'backdrop': ('<code>::backdrop</code>', '37', '79', '47', '15.4', '15.4'),
    'scroll-padding': ('<code>scroll-padding-top</code>', '69', '79', '68', '14.1', '14.5'),
    'sticky': ('<code>position: sticky</code>', '56', '16', '32', '13', '13'),
    'underline-offset': ('<code>text-underline-offset</code>', '87', '87', '70', '12.1', '12.2'),
    'deco-thickness': ('<code>text-decoration-thickness</code>', '89', '89', '70', '12.1', '12.2'),
    'details': ('<code>&lt;details&gt;</code> and <code>&lt;summary&gt;</code>', '12', '79', '49', '6', '6'),
    'search': ('<code>&lt;search&gt;</code>', '118', '118', '118', '17', '17'),
    'input-search': ('<code>&lt;input type="search"&gt;</code>', '5', '12', '4', '5', '4.2'),
    'download': ('the <code>download</code> attribute', '14', '18', '20', '10.1', '13'),
    'resize-observer': ('<code>ResizeObserver</code>', '64', '79', '69', '13.1', '13.4'),
    'intersection-observer': ('<code>IntersectionObserver</code>', '51', '15', '55', '12.1', '12.2'),
    'write-text': ('<code>navigator.clipboard.writeText()</code>', '66', '79', '63', '13.1', '13.4'),
    'autocomplete': ('the <code>autocomplete</code> attribute', '14', '12', '4', '6', '6'),
    'has': ('<code>:has()</code>', '105', '105', '121', '15.4', '15.4'),
    'aria-pressed-reflect': ('<code>Element.ariaPressed</code>', '81', '81', '119', '12.1', '12.2'),
}


def bs(*keys):
    out = []
    for k in keys:
        name, c, e, f, s, i = BCD[k]
        out.append(f'{name}: Chrome {c}, Edge {e}, Firefox {f}, Safari {s}, Safari on iOS {i}.')
    return ' '.join(out)


ARIA_NOTE = ('ARIA states and roles are read by screen readers, and MDN’s data does not track which screen reader '
             'reads which; chapter 19 lists them as not tested here.')


# ------------------------------------------------------------------------------------------------- the chapter's words
INTRO = [
    'A component is a part of a page that a reader works, such as a button, a menu or a search field. Each rule here '
    'gives one component as code to copy, drawn live in the light theme on Newsprint and in the dark theme on Charcoal, '
    'and a table of its states, its keys, its name, its target size and what a screen reader hears when it changes.',
    'The code reads only tokens.css, the file that holds every color, size and type style as a named value, so one copy '
    'follows either theme. How each state looks and moves comes from chapter 17.',
]

GROUPS = [
    ('18.1', 'Actions and choices', 'Buttons act on the page. Toggles, choices and the theme switch hold a state the reader '
                                    'sets, which a screen reader can name.'),
    ('18.5', 'Moving around', 'Links take a reader somewhere, and the masthead and the location lists show where the '
                              'reader is now.'),
    ('18.8', 'Showing and hiding', 'A disclosure opens a part of the page in place, and tabs switch between views of one '
                                   'thing.'),
    ('18.10', 'Tables, code and files', 'Tables sort where they stand and wide content scrolls inside its own frame. The '
                                        'copy and download controls say in words what they did.'),
    ('18.15', 'Finding and filling in', 'Search, filters and forms tell the reader what they found or what to fix, in a '
                                        'status line or beside the field.'),
    ('18.18', 'Messages and waiting', 'Each message carries its mark and its first word, and a part that waits for data '
                                      'says what is coming or what is missing.'),
    ('18.20', 'Records, readers and drawings', 'The controls our civic records and atlas drawings need: the live tracker, '
                                               'the report reader, the loop stepper, the controls on a drawing and the '
                                               'typed ID chip.'),
]

RELATED = [
    ('17', 'How each state looks and moves, and the one look for pressed, checked and current.'),
    ('26', 'Choosing a token, starting a page from tokens.css and the dark theme.'),
    ('19', 'Checking a finished page against WCAG 2.2 AA.'),
    ('11', 'The utility icons, the marks for error, success and warning, and the tracker’s marks.'),
    ('05', 'Contrast on each surface and the one working red.'),
    ('07', 'Reading at 320 px with nothing lost.'),
    ('20', 'Web pages built from these components.'),
    ('21', 'The atlas, which uses the diagram controls and the typed ID chip.'),
]

SOURCES = [
    'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, retrieved '
    'November 10, 2026. The success criteria each rule’s basis names.',
    'Source: W3C Web Accessibility Initiative, “ARIA Authoring Practices Guide”, the pattern pages each rule names and '
    'the Disclosure Navigation Menu example, no page dates, retrieved November 10, 2026. The Practices show one tested '
    'way to build each control, and WCAG sets what each must meet.',
    'Source: W3C, “Accessible Rich Internet Applications (WAI-ARIA) 1.2”, W3C Recommendation, June 6, 2023, the status '
    'and alert roles and the aria-live property, retrieved November 10, 2026. Behind Rules 18.18 and 18.20.',
    'Source: MDN Web Docs, browser compatibility data, version 8.1.8, built November 2, 2026, retrieved November 11, 2026. '
    'Each figure is the first version of a browser with full support, with no flag, prefix or partial mark. Every '
    '“Browser support” line in this chapter comes from it.',
    'Sources: WHATWG, “HTML Living Standard”, the sections on web storage and on scripts that block rendering, and MDN '
    'Web Docs, “Window: localStorage property” and “Storage quotas and eviction criteria”, retrieved November 10, 2026. '
    'Behind Rule 18.4’s stored choice, its private windows and Safari’s seven days.',
    'Source: Oath & Action’s systems atlas, Who Do They Answer To?, snapshot of October 15, 2026. Behind Loop R1, '
    '“Wealth and political influence reinforce each other”, which the atlas grades plausible, and Loop R8, “Housing '
    'scarcity strengthens owners’ incentive to restrict building”, whose two steps it grades well supported; the '
    'variables Households’ financial security (A4), Housing scarcity (A5), Homeowners’ equity (A6) and Major external '
    'shocks (X5); the first 12 of its 50 reforms, R-01 to R-12, in its own order; and Reform R-30, “More homes allowed '
    'by right near jobs”. Rules 18.7 to 18.9, 18.15, 18.16 and 18.22 to 18.24 show them.',
]

# Specification labels, in the order every table takes (the round 1 brief's list, then the themes and browsers)
L_PAT, L_ST, L_KEY, L_NAME, L_HEAR, L_TGT, L_FC, L_TH, L_BR = (
    'Pattern', 'States', 'Keyboard', 'Accessible name', 'A screen reader hears', 'Target', 'Forced colors',
    'Light and dark', 'Browser support')

RING = (f'the 2 px focus ring at a 2 px gap, in Verdigris on Newsprint ({R_RING_N} to 1) and Newsprint on Charcoal '
        f'({R_RING_C} to 1) (Rule 17.9)')
PRESSED = 'a check before the word, the word in bold and a 2 px edge (Rule 17.10)'


def specs(*rows):
    out = []
    for row in rows:
        lab, val = row[0], row[1]
        d = {'label': lab, 'value': val}
        if len(row) > 2 and row[2]:
            d['token'] = row[2]
        out.append(d)
    return out


# Each rule: number, set, code name, title, rule paragraphs, tokens, why, basis, anatomy caption, failure, code caption,
# code alt (None: the build's default), specs, related, builders. The failure entry: caption, alt, notes, exempt, html.
RULES = []


def rule(**kw):
    RULES.append(kw)


# ---- 18.1 Buttons -----------------------------------------------------------------------------------------------
rule(n=1, set='c-18-button', name='Buttons',
     title='Use a button to act on the page.',
     rule=['A button acts on the page: it sends a form, copies a value or starts a loop. A control that takes the reader to '
           'another page or place is a link (Rule 18.5). A view has one primary button at most, Charcoal on Newsprint and '
           'Newsprint on Charcoal. The ask, the Pillar Red button for the one way to take part, appears only where Rule '
           '05.3 gives the view its working red, the one job red does in a view, which goes to an error when there is one '
           'and otherwise to the step a reader can take now. The ask stands on a row of its own, apart from any primary '
           'button, whose hover turns Prussian on Newsprint, so the ask’s red never meets Prussian (Rule 05.3). Every other '
           'button is quiet: its word in ink inside a 1 px edge. A utility icon sits beside the word (Rule 11.11).',
           'Every component in this chapter hands a screen reader three things: its accessible name, the words a screen '
           'reader says for it; its role, such as button; and its state, such as pressed. When something changes, the code '
           'writes a sentence into a status line, a line on the page that a screen reader reads at its next pause. Each '
           'screen reader words all of this its own way. ARIA, short for Accessible Rich Internet Applications, is W3C’s set '
           'of attributes that gives a role or a state where HTML has none, and each rule names the pattern it follows in '
           'the ARIA Authoring Practices Guide (APG), W3C’s worked examples of each control.',
           'When an action cannot run yet, its button stays in place and keeps its focus. It carries aria-disabled, draws '
           'a dashed edge and points to a line under it that says why and what makes it work, such as “Fill in your email '
           'to send.” While a send runs, its word reads “Sending” and a second press does nothing. While an error on the '
           'page holds the red, the ask steps down to the primary look (Rule 11.16). When an action can no longer run, such '
           'as a sign-up for an event that is full, its button stays in place with its reason and the step the reader can '
           'take instead, such as another date. The form then leaves out the fields a reader could no longer send.'],
     tokens=['--oa-component-button-primary-fill', '--oa-component-button-primary-fill-hover',
             '--oa-component-button-primary-label', '--oa-component-button-ask-fill', '--oa-component-button-ask-label',
             '--oa-component-button-ask-keyline', '--oa-component-button-disabled-label',
             '--oa-component-button-disabled-edge', 'oa.size.target.touch'],
     why=['A native button gives every reader the Tab key, Enter, Space and the role “button” with no script. The disabled '
          'attribute would take the button out of the Tab order and hide its reason with it, so an unavailable button '
          'carries aria-disabled, which keeps both in reach. An underline on hover and a dashed edge when unavailable carry each state in a shape as well as '
          'a color.'],
     basis='WCAG 2.2 SC 1.4.1, 2.1.1, 2.5.8 and 4.1.2; APG Button pattern',
     anatomy='The parts of a button: its word, the 24 px utility icon beside it, its fill or 1 px edge, the 44 px '
             'height, the focus ring at its gap, and the reason line an unavailable button points to.',
     code_caption='Every kind of button, live: primary and quiet, two with a utility icon, the ask on a row of its own, '
                  'one unavailable with its reason, one sending, and the ask stepped down while an error holds the red. Tab '
                  'to “Send your comment” and press it: it keeps focus, and its line says why it waits.',
     specs=specs(
         (L_PAT, 'APG Button, on the native <code><button type="button"></code>.'),
         (L_ST, 'Default. Hover: the primary fill turns Prussian on Newsprint and White on Charcoal, and the word '
                'underlines; a quiet button’s edge thickens from 1 to 2 px. Focus: ' + RING + '. Unavailable: a dashed '
                f'edge, the word in the disabled color ({R_DIS_N} to 1 on Newsprint, {R_DIS_C} on Charcoal) and the reason '
                'line, with focus kept. Sending: the word reads “Sending”. Stepping down: the ask takes the primary look '
                'while an error holds the red, and its hover underlines its word and keeps its fill.'),
         (L_KEY, 'Tab reaches it; Enter or Space presses it. An unavailable button takes focus, and a press does '
                 'nothing.'),
         (L_NAME, 'Its visible word, which starts the name (WCAG 2.2 SC 2.5.3); the icon carries aria-hidden. An '
                  'unavailable button takes its reason as its description through aria-describedby.'),
         (L_HEAR, 'Its word and its role, button. Unavailable: the disabled state that aria-disabled gives, and the '
                  'reason. Sending: the new word, “Sending”, while focus is on it.'),
         (L_TGT, 'At least 44 px tall and 44 px wide (Rule 11.7); a row of two buttons stacks to one column when a word '
                 'would not fit.', 'oa.size.target.touch'),
         (L_FC, 'Fills drop out, so each button draws a 1 px edge in ButtonText around its word in ButtonText. The '
                'unavailable button keeps its dashed edge, in GrayText. The ring takes the system’s color.'),
         (L_TH, f'On Charcoal the primary button turns Newsprint with a Charcoal word, its hover fill turns White, and the '
                f'ask drops its Charcoal keyline; its White word measures {R_ASK} to 1 on Pillar Red in both themes, at '
                '19 px bold.'),
         (L_BR, bs('focus-visible', 'forced-colors')),
     ),
     related=['17', '11', '05'],
     builders=['An unavailable button: <code><button type="button" aria-disabled="true" '
               'aria-describedby="send-why"></code>, and as the first line of its click handler '
               '<code>if (button.getAttribute(\'aria-disabled\') === \'true\') return;</code>, as Rule 18.17’s script does. '
               'A row of two buttons: <code>grid-template-columns: repeat(auto-fit, minmax(min(100%, 10rem), 1fr))</code>, '
               'and no <code>white-space: nowrap</code> on any word.',
               '<code>data-red="working"</code> and <code>data-red-job</code> mark the view’s one working red for Rule 05.3’s '
               'check, which fails a view that marks two. Move both attributes as the red moves, to the error while an '
               'error holds the red and back to the ask once it clears.'],
     failure=dict(
         caption=f'<strong>Fails Rule 18.1.</strong> Send is grayed out with the disabled attribute and no words, so the '
                 f'Tab key skips it and nobody learns that the email is missing. Its word measures {R_F01} to 1 on '
                 'Newsprint.',
         alt=f'Failure case: do not publish. An Illustrative sign-up row at 360 px: a field labeled Email, empty, and '
             f'beside it a Send button grayed out, its word and edge in pale gray at {R_F01} to 1 on Newsprint. Nothing '
             'says why it is gray. A note under it reads “Tab skips Send, and no words say what it waits for.”',
         notes=f'Labeled failure: a pale word at {R_F01} to 1 on purpose, the fault this rule fixes.',
         exempt=['contrast']))

# ---- 18.2 Toggle buttons and chips ------------------------------------------------------------------------------
rule(n=2, set='c-18-toggle', name='Toggle buttons and chips',
     title='Turn a setting on or off with a toggle button.',
     rule=['A toggle button turns one thing on or off and keeps its word in both states, such as “Show sources”. A filter '
           'chip is a toggle that narrows a list, and chips combine, so a reader can turn on several at once. Each carries '
           'aria-pressed, true while it is on.',
           'On looks the same in every product (Rule 17.10): ' + PRESSED.replace(' (Rule 17.10)', '') + '. Off keeps a 1 '
           'px edge and no check. The word stays the same when the state changes, because the check and the pressed '
           'state already say it, and a word that flipped would leave a screen reader saying two things at once.'],
     tokens=['--oa-color-border-strong', '--oa-color-text-primary', 'oa.border.width.rule', 'oa.size.target.touch'],
     why=['A reader learns one look for on and meets it on every chip and toggle. The check and the edge are shapes, so '
          'they hold in gray print and in a contrast theme, where a fill drops out, and aria-pressed lets a screen reader '
          'say on or off.'],
     basis='WCAG 2.2 SC 1.4.1, 1.4.11 and 4.1.2; APG Button pattern, the toggle button',
     anatomy='The parts of a chip, off and on: its word, the 1 px edge, then the check before the word, the bold word '
             'and the 2 px edge, at 44 px tall.',
     code_caption='A toggle button and four filter chips, live, one chip waiting with its reason. Press Space on each: '
                  'the line under it says what changed, and focus stays where it is.',
     specs=specs(
         (L_PAT, 'APG Button, as a toggle button with aria-pressed. A long list of filters inside a form may use '
                 'checkboxes instead (APG Checkbox).'),
         (L_ST, 'Off: a 1 px edge and the word. On: ' + PRESSED + '. Hover: the word underlines. Focus: the ring. '
                'Unavailable: as Rule 18.1, a dashed edge and a reason.'),
         (L_KEY, 'Tab reaches each toggle; Space or Enter turns it on or off; focus stays on it.'),
         (L_NAME, 'Its word, the same in both states; the check carries aria-hidden.'),
         (L_HEAR, 'Its word, its role and “pressed” or “not pressed”; after a press, the new state. A chip that narrows a '
                  'list also changes the list’s status line (Rule 18.16).'),
         (L_TGT, '44 px tall and at least 44 px wide.', 'oa.size.target.touch'),
         (L_FC, 'The check, the bold word and the 2 px edge hold, in ButtonText. No fill carries the state, since a fill '
                'drops out.'),
         (L_TH, 'Charcoal edge, word and check on Newsprint; Newsprint on Charcoal.'),
         (L_BR, 'The script sets aria-pressed with <code>setAttribute</code>, which every browser reads, so it needs '
                'nothing newer than ' + bs('focus-visible') + ' ' + ARIA_NOTE),
     ),
     related=['17', '11'],
     builders=['<code><button type="button" class="oa-toggle oa-toggle--chip" aria-pressed="false"></code>, with the check as an inline '
               'SVG inside it. Draw the on look from <code>[aria-pressed="true"]</code>, so the state and the look cannot '
               'come apart.'],
     failure=dict(
         caption='<strong>Fails Rule 18.2.</strong> The chip that is on differs from the others only by its Prussian fill. '
                 'In a contrast theme the fill drops out, and all three chips look the same.',
         alt='Failure case: do not publish. Three Illustrative filter chips at 360 px: Hearing this week, Comment open and '
             'Became law. Hearing this week is on, shown only by a Prussian fill with White words; it has no check, no '
             'bold words and no heavier edge. A second row, labeled “The same chips in a contrast theme”, shows all three '
             'as identical outlined boxes.',
         notes='Picture of a fault: on shown by a fill alone, which forced colors removes (D2-1152).'))

# ---- 18.3 Choice ------------------------------------------------------------------------------------------------
rule(n=3, set='c-18-choice', name='Choice',
     title='Offer one of a few choices as radio buttons in a named group.',
     rule=['When a reader picks one of two to five choices and only one can hold, such as the size of a page, use native '
           'radio buttons in a fieldset whose legend names the choice. Draw them as a row of segments or as a list, and '
           'make the whole segment the label, so a press anywhere on it chooses.',
           'The checked choice takes the one look for a current choice (Rule 17.10): ' + PRESSED.replace(' (Rule 17.10)', '')
           + '. A choice applies at once, with no Apply button, and focus stays on it. A choice that cannot be made yet '
           'stays in view as a disabled radio, with a line under the row that says why, and the group points to that '
           'line with aria-describedby, so a screen reader hears it on entering the group.'],
     tokens=['--oa-color-border-strong', '--oa-color-text-primary', 'oa.border.width.rule', 'oa.size.target.touch'],
     why=['Radio buttons tell a screen reader that only one choice holds and how many there are, and the arrow keys move '
          'between them with no script. A pair of pressed buttons says neither. The arrow keys pass a disabled radio, so '
          'the line the group points to tells every reader why it waits.'],
     basis='WCAG 2.2 SC 1.3.1, 3.2.2 and 4.1.2; APG Radio Group pattern',
     anatomy='The parts of a choice: the legend, each segment with its word and its edge, the checked segment’s check, '
             'bold word and 2 px edge, the focus ring around the whole segment, and the line under the row that says why a choice '
             'waits.',
     code_caption='A choice of how to show a bill, live. Tab into it and use the arrow keys: each checks the next choice '
                  'and passes the one that waits.',
     specs=specs(
         (L_PAT, 'APG Radio Group, on native <code><input type="radio"></code> in a <code><fieldset></code> with a '
                 '<code><legend></code>.'),
         (L_ST, 'Unchecked: a 1 px edge. Checked: ' + PRESSED + '. Hover: the word underlines. Focus: the ring around the '
                'whole segment. Waiting: a disabled radio with a dashed edge and its reason under the row.'),
         (L_KEY, 'Tab enters the group at the checked choice. The arrow keys move and check, wrapping at the ends and '
                 'passing a choice that waits. Space checks the focused choice when none is checked. Tab leaves the '
                 'group.'),
         (L_NAME, 'The legend names the group; each label names its choice.'),
         (L_HEAR, 'The group’s name on entry, then the choice’s word, “radio button”, “checked” and its place, such as 2 '
                  'of 3; after an arrow key, the next choice the same way.'),
         (L_TGT, 'Each segment 44 px tall, all of it the label.', 'oa.size.target.touch'),
         (L_FC, 'The check, the bold word and the edges hold in ButtonText; a native radio, where it shows, takes the '
                'system’s colors.'),
         (L_TH, 'As Rule 18.2: Charcoal on Newsprint, Newsprint on Charcoal.'),
         (L_BR, 'Radio buttons, fieldsets and legends: every browser MDN lists, from its oldest versions. Draw the checked '
                'look with <code>input:checked + span</code>, which they all read. ' + bs('has') + ' '
                + bs('focus-visible')),
     ),
     related=['17', '11'],
     builders=['Hide the native radio with a visually hidden style that keeps it focusable, since '
               '<code>display: none</code> would take it out of the Tab order, and draw the ring on its segment from '
               '<code>input:focus-visible + span</code>.'],
     failure=dict(
         caption='<strong>Fails Rule 18.3.</strong> Nothing names the choice, and the chosen size differs only by its '
                 'fill. A screen reader hears “Full size” with no group, and a contrast theme loses the fill.',
         alt='Failure case: do not publish. An Illustrative report toolbar at 360 px with two joined segments, Fit width '
             'and Full size, and no words above them to say what they choose. Full size is chosen, shown only by a '
             'Prussian fill. A note under them reads “No group name, and the choice is a fill alone.”',
         notes='Picture of a fault: an unnamed group whose state is a fill alone.'))

# ---- 18.4 Theme switch ------------------------------------------------------------------------------------------
rule(n=4, set='c-18-theme-switch', name='Theme switch',
     title='Let the reader choose Light, Dark or Match my device.',
     rule=['Every screen product follows the reader’s device at first and offers a theme switch in the same place on every '
           'page, in the masthead or at the top of the phone menu. The switch is a choice (Rule 18.3) of three radio '
           'buttons under the legend “Theme”: Light, Dark and Match my device, with Match my device checked until the '
           'reader picks another. Each choice is a word, since a sun or a moon does not say which theme is on.',
           'A choice changes the colors at once, with no motion, and focus stays on it. Light and Dark set '
           '<code>data-oa-theme</code> on the page’s root and store the choice under the key <code>oa-theme</code>; '
           'Match my device removes the key, and the page '
           'follows the device again. The script reads and writes the key inside try and catch, so a browser that refuses '
           'storage still switches for the visit. A short script in the head applies a stored choice before the first '
           'paint (Rule 26.6).'],
     tokens=['--oa-color-surface', '--oa-color-text-primary', '--oa-color-border-strong', 'oa.size.target.touch'],
     why=['Following the device first gives most readers the right theme with no step at all. Three choices keep a way '
          'back to the device, which a two-state switch loses once it is pressed. Radio buttons say which theme is on and '
          'how many there are, and storage that fails costs the reader only the memory of the choice.'],
     basis='WCAG 2.2 SC 3.2.3 and 4.1.2; APG Radio Group pattern; design judgment',
     anatomy='The parts of the theme switch: the legend “Theme”, the three segments Light, Dark and Match my device, the '
             'checked segment’s check, bold word and 2 px edge, and its place in the masthead.',
     code_caption='The theme switch, live. Match my device is checked first, so each stage follows the theme it stands '
                  'in. In this guide a choice changes only its own stage and stores nothing; in a product it changes the '
                  'whole page and remembers the choice.',
     specs=specs(
         (L_PAT, 'APG Radio Group, as Rule 18.3.'),
         (L_ST, 'Checked and unchecked, as Rule 18.3, with Match my device checked first. No unavailable state: every '
                'choice always works.'),
         (L_KEY, 'As Rule 18.3: Tab enters at the checked choice, the arrow keys move and choose, and Tab leaves.'),
         (L_NAME, 'The legend, “Theme”; each choice its word.'),
         (L_HEAR, 'The group “Theme”, then the choice, “radio button”, “checked” and its place, such as Dark, 2 of 3. The '
                  'new colors are not announced, since the checked choice says it.'),
         (L_TGT, 'Each segment 44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'The system’s colors replace both themes, so a choice changes nothing a reader sees there. The switch '
                'still works and still shows which choice holds.'),
         (L_TH, 'Light is Newsprint and Dark is Charcoal. The switch sets <code>data-oa-theme</code> to light, dark or device, and the '
                'theme reaches every role a component reads (Rule 26.6).'),
         ('Stored choice', 'The key <code>oa-theme</code> holds light or dark; Match my device removes it. A private window keeps it '
                           'until the window closes, and Safari with tracking prevention on deletes it once the site goes '
                           'seven days of browsing without a press or a tap.'),
         (L_BR, bs('color-scheme-mq', 'color-scheme-meta', 'localstorage') + ' The page follows the device through the '
                'media query in tokens.css, so no script listens for a change.'),
     ),
     related=['26', '20', '21'],
     builders=['Put <code><meta name="color-scheme" content="light dark"></code> in the head of a themed product, with '
               'the head script of Rule 26.6 before the stylesheet, as the Head script panel below gives it. The switch’s '
               'own script stores only light or dark, and removes the key for Match my device.',
               'The copy names a sample page with <code>data-oa-theme-for</code>, so the guide’s live copy changes '
               'only its own stage. Leave the attribute out in a product, and the switch sets the page’s root and keeps '
               'the reader’s choice.'],
     failure=dict(
         caption='<strong>Fails Rule 18.4.</strong> A moon with no word flips between two themes. Once it is pressed, the '
                 'page never follows the device again, and the drawing does not say which theme is on.',
         alt='Failure case: do not publish. An Illustrative masthead at 360 px with one round button in its corner that '
             'shows a crescent moon and no word. A note under it reads “Two states, no way back to the device, and no '
             'word for the theme that is on.”',
         notes='Picture of a fault: a two-state icon toggle with no words (the main session’s three-choice call).'))

# ---- 18.5 Links -------------------------------------------------------------------------------------------------
rule(n=5, set='c-18-link', name='Links',
     title='Underline every link in text.',
     rule=['A link takes the reader to another page or place, and its words name the place, such as “the committee’s '
           'hearing schedule”. A link in running text keeps a 1 px underline that thickens to 2 px on hover, so its color '
           'is never the only sign. A link to another site opens in the same tab; its 16 px mark follows its last word, '
           'and the words “(another site)” end its name for screen readers (Rule 11.13).',
           'A skip link is the first stop on every page and shows when it takes focus. A link to the page or place the '
           'reader is on carries aria-current and the current look of Rule 18.7. A link to something not built yet stays '
           'plain text in the secondary color, with the words “Coming later.”'],
     tokens=['--oa-color-text-primary', '--oa-color-text-secondary', 'oa.border.width.underline',
             'oa.border.width.underlineHover', 'oa.size.icon.small'],
     why=[f'An underline marks a link in gray print, in a contrast theme and for a reader who cannot tell Prussian from '
          f'Charcoal, which measure {R_F05} to 1 against each other. Words that name the place let a reader choose from a '
          'list of links read out of their sentences, and a skip link lets a keyboard reader pass the masthead in one '
          'press.'],
     basis='WCAG 2.2 SC 1.4.1, 2.4.1, 2.4.4 and 3.2.5; APG Link pattern',
     anatomy='The parts of a link: its words, the 1 px underline and its 2 px hover, the 16 px mark after the last word of '
             'a link to another site, the hidden words “(another site)”, and the skip link shown at the top of a page.',
     code_caption='A skip link, two links in a sentence, one of them to another site, and a list that marks the page '
                  'you are on, live. The mark stays with the last word at every width.',
     specs=specs(
         (L_PAT, 'APG Link, on <code><a href></code>.'),
         (L_ST, 'Default: a 1 px underline. Hover: a 2 px underline. Focus: the ring. Current: aria-current and the look '
                'of Rule 18.7. Not built yet: plain text in the secondary color with “Coming later.”'),
         (L_KEY, 'Tab reaches it; Enter follows it. The skip link is the page’s first Tab stop.'),
         (L_NAME, 'Its words. A link to another site adds the hidden words “(another site)”, or “(opens in a new tab)” '
                  'where it must open one.'),
         (L_HEAR, 'Its words and its role, link, with “visited” once followed and “current page” where aria-current says '
                  'so.'),
         (L_TGT, 'In running text, the line itself, which WCAG 2.2 SC 2.5.8 exempts; in a list, 44 px tall (Rule '
                 '11.13).', 'oa.size.target.minimum'),
         (L_FC, 'Links take LinkText and keep their underline; the mark draws in currentColor.'),
         (L_TH, 'A link takes the text’s ink, Charcoal on Newsprint and Newsprint on Charcoal.'),
         (L_BR, bs('underline-offset', 'deco-thickness') + ' An older browser draws its own underline, which still marks '
                'the link.'),
     ),
     related=['11', '02'],
     builders=['Wrap only the last word and the mark in a span with <code>white-space: nowrap</code>, so the mark never '
               'breaks from its word and the rest of the link still wraps. Put “(another site)” in a visually hidden span '
               'inside the link, and leave out <code>target="_blank"</code>.'],
     failure=dict(
         caption=f'<strong>Fails Rule 18.5.</strong> The links show only as Prussian words beside Charcoal ones, {R_F05} '
                 'to 1 apart, and one of them says “click here”, which names no place.',
         alt=f'Failure case: do not publish. An Illustrative paragraph at 360 px about a county budget hearing. Two of its '
             f'phrases are links, drawn only in Prussian with no underline, {R_F05} to 1 against the Charcoal text around '
             'them. The second link reads “click here”.',
         notes='Picture of a fault: links told apart by color alone, and link words that name no place.'))

# ---- 18.6 Masthead and phone menu -------------------------------------------------------------------------------
rule(n=6, set='c-18-masthead', name='Masthead and phone menu',
     title='Give every page one masthead with its parts in a named navigation.',
     rule=['The masthead holds the product’s name, which links home, and its parts in a navigation landmark, a region a '
           'screen reader can jump to, named for what it holds, such as “Parts of the site”. The link to the part the reader is in carries <code>aria-current="page"</code>, bold words and a 2 px '
           'underline. When the parts no longer fit on one line, they move behind a Menu button, its three bars beside the '
           'word Menu, which opens them in a native modal dialog.',
           'The open menu covers the page and holds focus. Focus moves to the current part’s link, the Tab key reaches '
           'nothing on the page behind it, and Escape or “Close the menu” shuts it and returns focus to Menu. The rows inside open and close as disclosures '
           '(Rule 18.8). A masthead that sticks to the top of the page sets scroll-padding-top to its own height, so no '
           'focused element hides under it.'],
     tokens=['--oa-color-surface', '--oa-color-text-primary', '--oa-color-border-hairline', 'oa.border.width.rule',
             'oa.size.target.touch'],
     why=['One masthead in one place on every page lets a reader find the parts without searching, and a named navigation '
          'lets a screen reader jump straight to it. The native dialog makes the page behind it inert, so neither the Tab '
          'key nor a screen reader’s reading keys reach a link the menu covers.'],
     basis='WCAG 2.2 SC 2.1.2, 2.4.1, 2.4.3, 2.4.11 and 3.2.3; APG Dialog (Modal) pattern and Disclosure Navigation Menu '
           'example',
     anatomy='The parts of a masthead: the product’s name as the home link, the navigation and its label, the current '
             'part’s 2 px underline, the Menu button with its bars and word, and the open menu with its title, Close the '
             'menu and its rows.',
     code_caption='A masthead and its phone menu, live. Open Menu, press Tab to stay inside, and press Escape to return '
                  'to Menu.',
     code_alt='A masthead and its phone menu, drawn live from the HTML, CSS and script below. In this guide the live copy '
              'draws the header and the navigation as named groups, so the guide’s own landmarks stay the only ones on the '
              'page; the code below keeps the real header and nav elements.',
     specs=specs(
         (L_PAT, 'Landmarks, banner and navigation; APG Dialog (Modal) for the phone menu; Disclosure for its rows. A '
                 'dropdown that leaves the page in view follows APG’s Disclosure Navigation Menu example, and no part of '
                 'the masthead takes the menu role.'),
         (L_ST, 'Current part: bold words, a 2 px underline and aria-current. Hover: a 1 px underline. Menu closed or open, with '
                'aria-expanded. Rows closed or open, the chevron down or up. Focus: the ring.'),
         (L_KEY, 'Tab through the home link and the parts. On a phone, Enter or Space on Menu opens the menu with focus on '
                 'the current part’s link; Tab and Shift+Tab move through the menu and never reach the page behind it; Escape '
                 'or Close the menu shuts it, and focus returns to Menu.'),
         (L_NAME, 'The navigation’s label, such as “Parts of the site”; “Menu”, with <code>aria-haspopup="dialog"</code>; the dialog named by its '
                  'title; “Close the menu”.'),
         (L_HEAR, 'The navigation and its name on entry; “current page” on the current part; on Menu, “collapsed” or '
                  '“expanded”, and once it opens, the dialog’s name.'),
         (L_TGT, 'Each link and Menu at least 44 px tall; Close the menu 44 by 44 px.', 'oa.size.target.touch'),
         (L_FC, 'The bars, the chevrons and the underline draw in ButtonText or LinkText, and the current part keeps its '
                'underline. The dialog draws a 1 px edge in CanvasText.'),
         (L_TH, 'The masthead and the dialog paint their ground with --oa-color-surface, so both follow the theme.'),
         (L_BR, bs('dialog', 'backdrop', 'scroll-padding', 'sticky')),
     ),
     related=['20', '21', '07'],
     builders=['Open the menu with <code>dialog.showModal()</code>, which makes the rest of the page inert and gives '
               'Escape. A <code>div</code> with <code>role="dialog"</code> does neither once it is copied into a page.'],
     failure=dict(
         caption='<strong>Fails Rule 18.6.</strong> Menu is three bars with no word in a 32 px square, and its list drops '
                 'over the page without holding focus, so the Tab key walks on into the links it covers.',
         alt='Failure case: do not publish. An Illustrative phone masthead at 360 px with the title “Who Do They Answer '
             'To?” and, at the right, three bars in a 32 px square with no word. Under it, an open list of four parts '
             'drops over the page, and a link of the page shows through below the list. A note reads “No word on Menu, '
             'and Tab moves past the list into the page.”',
         notes='Picture of a fault: an icon-only Menu under 44 px, and a menu that does not hold focus (F-12).'))

# ---- 18.7 Location ----------------------------------------------------------------------------------------------
rule(n=7, set='c-18-location', name='Location list',
     title='Show where the reader is with aria-current and a mark that needs no color.',
     rule=['A list of places in a product, such as a chapter rail, an “In this chapter” list or a breadcrumb, marks the '
           'reader’s place in two ways at once. The link carries aria-current: “page” for the page itself, “location” for '
           'a part of a long page and “step” for a step in a process. A list beside the text marks it with the selected '
           'band, a 4 px bar at its left edge and bold words. A short list in a line, such as a breadcrumb, ends on the '
           'current page as a link in bold words, with aria-current and no underline, after the links to the places '
           'before it.',
           'A list that follows the reader down a long page moves its mark as each part comes into view, and leaves focus '
           'and its own scroll where they are. A breadcrumb sits in a navigation landmark named “Breadcrumb”, with its '
           'places in an ordered list and the current page last.'],
     tokens=['--oa-color-state-selected-band', '--oa-color-state-selected-bar', 'oa.border.width.bar',
             'oa.border.width.rule'],
     why=['aria-current lets a screen reader say where the reader is, and the bar and the bold words say it to everyone '
          'else in shapes that hold in gray print and in a contrast theme. A mark that follows the scroll helps only while '
          'it leaves focus alone.'],
     basis='WCAG 2.2 SC 1.4.1 and 4.1.2; APG Breadcrumb pattern',
     anatomy='The parts of a location list: the list’s label, each link, the current link’s band, 4 px bar and bold '
             'words, and a breadcrumb’s current page in bold.',
     code_caption='A breadcrumb and a list of places, live, each marking where the reader is, with Previous and Next '
                  'after them. The places are the variables our systems atlas files under “Housing, health care and getting '
                  'ahead”.',
     code_alt='A breadcrumb and a list of places, drawn live from the code below. In this guide the live copy '
              'draws the breadcrumb’s navigation as a named group, so the guide’s own landmarks stay the only ones on the '
              'page; the code below keeps the real nav element.',
     specs=specs(
         (L_PAT, 'APG Link; APG Breadcrumb for a trail of places; a navigation landmark for each list that leads around '
                 'the product.'),
         (L_ST, 'Current: the band, the 4 px bar and bold words in a list, or bold words in a breadcrumb, with '
                'aria-current. Hover: an '
                'underline. Focus: the ring.'),
         (L_KEY, 'Tab through the links; Enter follows one.'),
         (L_NAME, 'The list’s label, such as “In this chapter” or “Breadcrumb”; each link its words.'),
         (L_HEAR, '“current page”, “current location” or “current step” on the current link. Nothing when the mark moves '
                  'with the scroll, since moving it changes no focus.'),
         (L_TGT, 'Rows 44 px tall in a list a thumb uses; at least 24 px with spacing in a list of words.',
          'oa.size.target.minimum'),
         (L_FC, 'The band drops out. The 4 px bar, drawn as a border, takes the system’s highlight color, and the bold words '
                'hold.'),
         (L_TH, 'On Newsprint the band is White and the bar Charcoal; on Charcoal the band is Prussian and the bar '
                'Newsprint.'),
         (L_BR, bs('sticky', 'intersection-observer') + ' The second tells a script which part is in view.'),
     ),
     related=['17', '20', '21'],
     builders=['Draw the bar as <code>border-left</code> in <code>--oa-color-state-selected-bar</code> and the band as a '
               'background, so the bar survives a contrast theme. Move <code>aria-current</code> with the mark.'],
     failure=dict(
         caption='<strong>Fails Rule 18.7.</strong> Only the color of “05 Color” marks where the reader is, and no '
                 'aria-current tells a screen reader.',
         alt='Failure case: do not publish. A list of five chapters at 360 px, 03 Identity to 07 Layout and spacing. The '
             'current chapter, 05 Color, differs only by its Prussian words; it has no band, no bar and no bold. A note '
             'reads “The place is a color alone.”',
         notes='Picture of a fault: the current item marked by color alone.'))

# ---- 18.8 Disclosure --------------------------------------------------------------------------------------------
rule(n=8, set='c-18-disclosure', name='Disclosure',
     title='Open a part of the page in place with a disclosure.',
     rule=['A disclosure shows or hides one part of the page in place, such as a drawing’s lines in words or the sources of '
           'a claim. Build it on native details and summary, or on a button with aria-expanded and aria-controls where the '
           'part must sit apart from its control. Its words name what opens, such as “The lines in words”, and its chevron '
           'points down while it is closed and up while it is open.',
           'The chevron turns within 200 ms where motion is allowed, and at once under reduced motion (Rule 17.4). Opening '
           'one disclosure leaves the others as they are, and a printed page opens them all. A stack of disclosures under '
           'headings is an accordion, with each summary inside its heading.'],
     tokens=['oa.motion.duration.standard', 'oa.size.icon.medium', 'oa.size.target.touch'],
     why=['The native element gives Enter, Space, the expanded state and the open part with no script. A chevron that turns '
          'tells a sighted reader what the expanded state tells a screen reader, and words that name the part let a '
          'reader decide before opening it.'],
     basis='WCAG 2.2 SC 1.3.1, 2.1.1 and 4.1.2; APG Disclosure (Show/Hide) and Accordion patterns',
     anatomy='The parts of a disclosure: the summary’s words, the chevron down and up, the 44 px row, the focus ring and '
             'the part that opens.',
     code_caption='Two disclosures built on details and summary and one built on a button, live. Press Enter or Space '
                  'on each to open or close it.',
     specs=specs(
         (L_PAT, 'APG Disclosure (Show/Hide); Accordion for a stack under headings.'),
         (L_ST, 'Closed: the chevron down. Open: the chevron up. Hover: the words underline. Focus: the ring.'),
         (L_KEY, 'Tab reaches the summary; Enter or Space opens or closes it; once open, the links inside join the Tab '
                 'order.'),
         (L_NAME, 'The summary’s words.'),
         (L_HEAR, 'The words, the control’s role and “collapsed” or “expanded”; after a press, the new state.'),
         (L_TGT, 'The summary at least 44 px tall across its row.', 'oa.size.target.touch'),
         (L_FC, 'The chevron draws in currentColor.'),
         (L_TH, 'Words and chevron in the text’s ink on either surface.'),
         ('Motion', 'The chevron turns in 200 ms at most, and in 0 ms under reduced motion.',
          'oa.motion.duration.standard'),
         (L_BR, bs('details', 'reduced-motion')),
     ),
     related=['17', '11'],
     builders=['Hide the browser’s own triangle with <code>list-style: none</code> on the summary and '
               '<code>::-webkit-details-marker { display: none }</code>, then turn the chevron from '
               '<code>details[open]</code>.'],
     failure=dict(
         caption='<strong>Fails Rule 18.8.</strong> The plus stays a plus once the row is open, and the row is a plain box '
                 'that the Tab key passes by.',
         alt='Failure case: do not publish. Two rows at 360 px, “Sources” closed and “The lines in words” open, with the '
             'two lines of our systems atlas’s housing loop under it: scarce homes raise owners’ equity, and owners with '
             'that equity object to new construction. Both rows end in the same plus sign. A note reads “The sign does not '
             'change, and the rows take no focus.”',
         notes='Picture of a fault: a disclosure with no state shape and no button.'))

# ---- 18.9 Tabs --------------------------------------------------------------------------------------------------
rule(n=9, set='c-18-tabs', name='Tabs',
     title='Switch between views of one thing with tabs.',
     rule=['Use tabs only where a reader switches between views of one thing that never need to show at once, such as a '
           'drawing, its lines in words and its table. A process with steps takes a stepper (Rule 18.22), and other pages '
           'take links. The tabs sit in a tab list named for the thing, each tab names its view, and the selected tab '
           'carries aria-selected, a 4 px bar under its word and bold words.',
           'Tab enters the tab list at the selected tab and leaves it for the panel. The arrow keys move between tabs and '
           'show each view as it takes focus, and Home and End reach the first and the last. A panel with nothing '
           'focusable inside takes <code>tabindex="0"</code>, so the Tab key can reach its words.'],
     tokens=['--oa-color-state-selected-bar', 'oa.border.width.bar', 'oa.size.target.touch'],
     why=['One Tab stop for the whole list keeps a keyboard reader from passing every tab to reach the content, and the '
          'roles let a screen reader say which tab holds and how many there are. The bar and the bold words carry the '
          'selection in gray print and in a contrast theme.'],
     basis='WCAG 2.2 SC 1.3.1, 2.1.1, 2.4.3 and 4.1.2; APG Tabs pattern',
     anatomy='The parts of tabs: the tab list and its label, each tab’s words, the selected tab’s 4 px bar and bold words, '
             'the focus ring and the panel.',
     code_caption='Four tabs, live, the last waiting with its reason. Tab to the selected one, then use the arrow keys, '
                  'Home and End.',
     specs=specs(
         (L_PAT, 'APG Tabs, with each view shown as its tab takes focus, since every panel is already in the page.'),
         (L_ST, 'Selected: the 4 px bar as a bottom border and bold words, with <code>aria-selected="true"</code>. Not selected: '
                'words at 600, the weight every control’s word takes, and no bar. Hover: the words underline. Focus: the ring.'),
         (L_KEY, 'Tab enters at the selected tab. Left and Right Arrow move and select, wrapping at the ends. Home and End '
                 'go to the first and the last. Tab moves on to the panel.'),
         (L_NAME, 'The tab list’s label; each tab its words; each panel named by its tab through aria-labelledby.'),
         (L_HEAR, 'The tab list and its name on entry; each tab’s words, “tab”, “selected” and its place, such as 2 of '
                  '4.'),
         (L_TGT, 'Each tab 44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'The bar, a border, and the bold words hold in the system’s colors.'),
         (L_TH, 'The bar in --oa-color-state-selected-bar: Charcoal on Newsprint, Newsprint on Charcoal.'),
         (L_BR, 'Buttons, ARIA roles and a script that moves tabindex itself, with nothing newer than '
                + bs('focus-visible')),
     ),
     related=['17', '15', '14'],
     builders=['Give the selected tab <code>tabindex="0"</code> and every other tab <code>tabindex="-1"</code>, and move '
               'both as the arrow keys move focus. Hide the other panels with the <code>hidden</code> attribute.'],
     failure=dict(
         caption='<strong>Fails Rule 18.9.</strong> The selected view differs only by its fill, every tab is a Tab stop of '
                 'its own, and the arrow keys do nothing.',
         alt='Failure case: do not publish. Three tabs at 360 px, Drawing, In words and Table, over a panel that holds the '
             'first sentence of Loop R1 from our systems atlas: “Households with concentrated wealth can spend more on '
             'campaigns, outside groups and lobbying.” Drawing is selected, shown only by a Prussian fill; there is no bar '
             'and no bold. A note reads “Three Tab stops, no arrow keys, and the selection is a fill alone.”',
         notes='Picture of a fault: tabs with no roles and a fill-only selection.'))

# ---- 18.10 Table ------------------------------------------------------------------------------------------------
rule(n=10, set='c-18-table', name='Sortable table',
     title='Build a table from table markup.',
     rule=['A table has a caption that names it, column headings in th with <code>scope="col"</code>, and row headings where the first '
           'column names each row. A column a reader can sort holds a button in its heading, with the heading’s words and '
           'the 16 px sort arrow after them. The sorted column’s heading carries aria-sort, and the arrow turns up for '
           'ascending and down for descending.',
           'A press sorts the column, a second press reverses it, and focus stays on the button. A status line under the '
           'table says the order in words, such as “Sorted by date, newest first.” The same line says when rows are '
           'loading, what is missing when there are none, and the error with its mark when they fail to load (Rules 18.18 '
           'and 18.19). On a phone a table either scrolls inside a scroll region (Rule 18.11) or reads as one card for each '
           'row, each value under its column’s word. A table drawn as cards states its roles with role attributes, so it '
           'keeps its meaning however CSS displays it.'],
     tokens=['--oa-color-border-hairline', '--oa-color-text-primary', 'oa.size.icon.small', 'oa.size.target.touch'],
     why=['Table markup lets a screen reader name the row and the column of every cell as a reader moves through it. A '
          'button in the heading gives sorting a key and a name, and aria-sort with the status line says the new order to '
          'a reader who cannot see the arrow turn.'],
     basis='WCAG 2.2 SC 1.3.1, 2.1.1, 4.1.2 and 4.1.3; APG Table pattern and its Sortable Table example',
     anatomy='The parts of a sortable table: the caption, the column headings, a sort button with its words and 16 px '
             'arrow, the sorted heading, the row rules and the status line under the table.',
     code_caption='A table of four bills, live, with its loading, empty and error states under it. Sort a column with '
                  'Enter, then press it again to reverse it; the line under the table says the order.',
     specs=specs(
         (L_PAT, 'APG Table, on a native <code><table></code>; the Sortable Table example for aria-sort.'),
         (L_ST, 'Unsorted, sorted ascending, sorted descending. Hover on a sort button: the words underline. Focus: the '
                'ring. Loading, empty and error in the status line under the table.'),
         (L_KEY, 'Tab moves between the sort buttons; Enter or Space sorts. The table has no keys of its own, and a screen '
                 'reader’s table keys move from cell to cell.'),
         (L_NAME, 'The caption names the table; each sort button takes its heading’s words.'),
         (L_HEAR, 'The column heading and “sorted ascending” or “sorted descending” on the sorted column; after a press, '
                  'the status line, such as “Sorted by date, newest first.”'),
         (L_TGT, 'Each sort button at least 44 px tall, as wide as its words and arrow.', 'oa.size.target.touch'),
         (L_FC, 'The arrow draws in currentColor, and the rules between rows hold as borders.'),
         (L_TH, 'Rules in --oa-color-border-hairline and words in the text’s ink on either surface.'),
         (L_BR, 'Tables, captions and th: every browser MDN lists, from its oldest versions. ' + ARIA_NOTE),
     ),
     related=['06', '14', '26'],
     builders=['Set <code>aria-sort</code> only on the sorted column’s th and remove it from the others; a column never '
               'sorted carries none. Keep figures in tabular numerals (Rule 06.5).'],
     failure=dict(
         caption='<strong>Fails Rule 18.10.</strong> The headings are plain cells that only a pointer can sort, and nothing '
                 'says the order changed.',
         alt='Failure case: do not publish. An Illustrative table at 360 px of three bills with the columns Bill, Title and '
             'Last action. The Last action heading shows a small arrow after its word, but the headings are plain text '
             'with no button. A note reads “Only a pointer can sort, and the new order is never said.”',
         notes='Picture of a fault: sorting with no button and no status line.'))

# ---- 18.11 Scroll region ----------------------------------------------------------------------------------------
rule(n=11, set='c-18-scroll-region', name='Scroll region',
     title='Let wide content scroll inside a named frame.',
     rule=['Content wider than its column, such as a wide table or a drawing at true size, scrolls sideways inside its own '
           'frame, so the page itself never scrolls sideways (Rule 07.6). While it overflows, the frame takes '
           '<code>tabindex="0"</code> and the role of a group named for what it holds, and the hint “Wider than this '
           'column. Scroll the frame sideways to see all of it.” shows above it and describes it. Once it fits, the frame '
           'drops all three.',
           'Its focus ring sits inside the frame with its 2 px gap, where the frame’s edge cannot clip it. A control whose '
           'neighbor stands too close for an outside ring, such as a tab or a row in a list, draws the same ring inside its '
           'own edge, with the 2 px gap, offset −4 px. The arrow keys scroll a focused frame, and the page around it stays '
           'where it is. This guide sets its plates and code on a light gray mat, '
           f'where the focus ring’s color measures {R_RING_MAT} to 1, under the 3 to 1 a ring needs, so a frame that '
           f'scrolls on the mat draws the same ring in Charcoal, {R_CHAR_MAT} to 1.'],
     tokens=['--oa-color-border-hairline', '--oa-color-focus-ring', 'oa.border.width.focusRing'],
     why=['A keyboard reader can scroll only what takes focus, and a frame that takes focus while it has nothing to scroll '
          'is a stop that does nothing. The hint tells a sighted reader the frame holds more, and the name tells a screen '
          'reader.'],
     basis='WCAG 2.2 SC 1.4.10, 2.1.1 and 4.1.2',
     anatomy='The parts of a scroll region: the frame and its edge, the wide content inside, the hint above it, and the '
             'focus ring drawn inside the frame.',
     code_caption='A bill’s six steps in a frame, live. Where the frame is narrower than the steps, as on a phone, Tab '
                  'reaches it and the arrow keys scroll it; where it holds them whole, it takes no stop and shows no hint.',
     specs=specs(
         (L_PAT, 'None fits; a group with a name, <code>role="group"</code>, that takes focus while it scrolls.'),
         (L_ST, 'Fits: no Tab stop and no hint. Overflows: the Tab stop, the hint and the name. Focus: the ring inside the '
                'frame.'),
         (L_KEY, 'Tab reaches it while it overflows; Left and Right Arrow scroll it; Tab leaves it.'),
         (L_NAME, 'What it holds, such as “The six steps of a bill”, with the hint as its description.'),
         (L_HEAR, 'The group, its name and the hint when focus enters.'),
         (L_TGT, 'The whole frame.'),
         (L_FC, 'The frame draws a 1 px edge in CanvasText, and the ring takes the system’s color.'),
         (L_TH, 'The edge in --oa-color-border-hairline and the ring in --oa-color-focus-ring, on either surface.'),
         (L_BR, bs('resize-observer') + ' It tells the script when the frame starts or stops overflowing.'),
     ),
     related=['07', '19'],
     builders=['Draw the ring inside the frame with <code>outline-offset: -4px</code>, the ring’s 2 px and its 2 px gap, and set '
               '<code>tabindex</code>, the name and the hint together from one check of '
               '<code>scrollWidth > clientWidth</code>.'],
     failure=dict(
         caption='<strong>Fails Rule 18.11.</strong> The table is cut off at the frame’s edge, and no key or hint lets a '
                 'reader see the columns past it.',
         alt='Failure case: do not publish. An Illustrative table at 360 px of state hearings with four columns, cut off '
             'at the frame’s right edge partway through the third column. The fourth column never shows. A note reads '
             '“Hidden past the edge, with no way to scroll by key.”',
         notes='Picture of a fault: overflow hidden with no scroll and no hint.'))

# ---- 18.12 Code block -------------------------------------------------------------------------------------------
rule(n=12, set='c-18-code-block', name='Code block',
     title='Show code in labeled panels with named Copy buttons.',
     rule=['Code a reader can copy sits in one panel per file, HTML, CSS or Script, each with its label and a Copy button '
           'named for its panel: “Copy the HTML”, “Copy the CSS” and “Copy the script”. One status line under the panels '
           'says what was copied, with the success mark, such as “Copied the CSS, 2 lines, to the clipboard.” The code keeps its own line breaks at 14 px, and a panel that overflows scrolls as Rule 18.11 '
           'sets.',
           'When the browser refuses to copy, the line turns into an error with its mark, “Error:”, the Error Band and the '
           '4 px red bar, and says how to copy by hand. The code is then selected in a field under the line, with focus on '
           'it (Rule 18.13).'],
     tokens=['--oa-color-state-success-mark', '--oa-color-state-error-bar', '--oa-color-state-error-band',
             'oa.border.width.bar', 'oa.size.target.touch'],
     why=['A button for each panel says which file a press takes, and a status line says what happened in words, which a '
          'screen reader hears while focus stays on the button. A browser can refuse the clipboard, so the refusal '
          'leaves the code ready to copy by hand.'],
     basis='WCAG 2.2 SC 2.4.6, 3.3.1 and 4.1.3; APG Button pattern; WAI-ARIA 1.2 status role',
     anatomy='The parts of a code block: each panel’s label, its Copy button, the code at 14 px, the status line with the '
             'success mark, and the error line with its mark, band and bar over the selected code.',
     code_caption='A code block with two panels, live. Press a Copy button and read the line under the panels.',
     specs=specs(
         (L_PAT, 'APG Button for each Copy; a status line with <code>role="status"</code>; Rule 18.11 for a panel that scrolls.'),
         (L_ST, 'Nothing copied yet. Copied: the success mark and the words. Refused: the error mark, “Error:”, the band, '
                'the bar and the selected code. Hover and focus on each Copy button as Rule 18.1.'),
         (L_KEY, 'Tab reaches each Copy button, and each panel while it scrolls. Enter or Space copies. Focus stays on the '
                 'button, or moves to the selected code when the browser refuses.'),
         (L_NAME, '“Copy the HTML”, “Copy the CSS” and “Copy the script”, each described by the component’s name; each '
                  'panel named by its label.'),
         (L_HEAR, 'After a press, the status line at the next pause: what was copied and how many lines. On a refusal, '
                  'the error’s words, then the selected field.'),
         (L_TGT, 'Each Copy button 44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'The 4 px bar is a border and holds; the marks draw in currentColor; the code takes CanvasText.'),
         (L_TH, f'The panel’s ground is --oa-color-surface. On Charcoal the error takes no band, and its bar measures '
                f'{R_BAR_C} to 1.'),
         (L_BR, bs('write-text') + ' It works only on a secure page, served over https, and inside the reader’s press: '
                'Firefox and Safari refuse a call outside one, and Chrome and Edge do from version 107 unless the reader '
                'has granted the permission.'),
     ),
     related=['26', '11'],
     builders=['Call <code>navigator.clipboard.writeText()</code> inside the click handler itself, and catch its refusal. '
               'On a refusal, put the code in a <code><textarea readonly></code>, select it and move focus there.'],
     failure=dict(
         caption='<strong>Fails Rule 18.12.</strong> After a press the copy icon turns into a check, and no words say what '
                 'was copied or whether it worked.',
         alt='Failure case: do not publish. An Illustrative code panel at 360 px holding four lines of CSS, with a lone '
             'icon in its corner that has turned from two sheets into a check after a press. No label names the panel, '
             'and no line says what happened.',
         notes='Picture of a fault: a Copy icon that changes meaning, with no status line (Rule 11.12).'))

# ---- 18.13 Copy a value -----------------------------------------------------------------------------------------
rule(n=13, set='c-18-copy', name='Copy control',
     title='Copy one value with a button that names it.',
     rule=['A value a builder needs, such as a token’s name or a hex color, sits beside a Copy button. Its visible word is '
           '“Copy”, and its name goes on with the value from hidden words, “Copy --oa-color-surface-charcoal”, so every '
           'Copy in a table names its own value. The icon’s two sheets stay as drawn after a press (Rule 11.12), and the '
           'status line says what happened with the success mark: “Copied --oa-color-surface-charcoal.”',
           'When the browser refuses, the line gives the error with its mark and “Error:”, selects the value in a field '
           'and moves focus there, so the reader can copy it by hand with Control and C, or Command and C.'],
     tokens=['--oa-color-state-success-mark', '--oa-color-state-error-bar', 'oa.size.icon.medium',
             'oa.size.target.touch'],
     why=['A reader who hears “Copy” ten times down a table cannot tell the buttons apart, so each name carries its value. '
          'Words in a status line reach a screen reader, where a check that replaces the icon says nothing and looks like '
          'a choice someone made.'],
     basis='WCAG 2.2 SC 2.4.6, 2.5.3 and 4.1.3; Rule 11.12',
     anatomy='The parts of a copy control: the value, the Copy button with its two-sheet icon and word, the hidden words '
             'that finish its name, and the status line with the success mark.',
     code_caption='Two values with their Copy buttons, live. Press one and read the line under them.',
     specs=specs(
         (L_PAT, 'APG Button; a status line with <code>role="status"</code>.'),
         (L_ST, 'Nothing copied yet; copied; refused. Hover and focus as Rule 18.1.'),
         (L_KEY, 'Tab reaches it; Enter or Space copies. Focus stays on it, or moves to the selected value when the '
                 'browser refuses.'),
         (L_NAME, '“Copy” and the value, such as “Copy --oa-color-surface-charcoal”, starting with the visible word.'),
         (L_HEAR, 'After a press, the status line: “Copied --oa-color-surface-charcoal.”'),
         (L_TGT, 'At least 44 by 44 px, even beside a short value.', 'oa.size.target.touch'),
         (L_FC, 'As Rule 18.12: the marks in currentColor and the bar as a border.'),
         (L_TH, 'As Rule 18.12.'),
         (L_BR, bs('write-text') + ' The same limits as Rule 18.12: a secure page and the reader’s own press.'),
     ),
     related=['26', '05', '11'],
     builders=['Put the value in a visually hidden span inside the button, after the word Copy, and write the result to a '
               'status line outside the button, so the name stays the same after a press.'],
     failure=dict(
         caption='<strong>Fails Rule 18.13.</strong> Copy is a 16 px icon with no word, under the 24 px a target needs, '
                 'and every one in the list has the same name.',
         alt='Failure case: do not publish. A list of three Illustrative color values at 360 px, Charcoal, Newsprint and '
             'Prussian, each with its hex value and a 16 px copy icon after it with no word and no frame. A note reads '
             '“Three targets 16 px square, each heard only as Copy.”',
         notes='Picture of a fault: icon-only copy controls under the 24 px minimum target (SC 2.5.8).'))

# ---- 18.14 Download ---------------------------------------------------------------------------------------------
rule(n=14, set='c-18-download', name='Download',
     title='Name each download for its file, type and size.',
     rule=['A download is a link with the download attribute when it fetches a file, and a button when a script builds '
           f'the file. Its words start with “Download” and name the file, its type and its size, in kilobytes of 1,000 '
           f'bytes: “Download tokens.css, CSS, {TOKENS_KB}”. The download icon, an arrow into a tray, sits before the '
           'word (Rule 11.11).',
           'A file that is not ready keeps its control in place and in the Tab order, with aria-disabled, a dashed edge and '
           'a line that says why and when it will be ready. A press does nothing, and focus stays.'],
     tokens=['--oa-color-state-disabled-text', '--oa-color-state-disabled-edge', 'oa.size.icon.medium',
             'oa.size.target.touch'],
     why=['The file’s name, type and size let a reader on a slow or metered connection decide before the download starts, '
          'and a screen reader reading a list of links hears which file each one fetches. A control that hides until its '
          'file is ready leaves a reader wondering whether the file exists.'],
     basis='WCAG 2.2 SC 2.4.4 and 4.1.2; APG Link pattern; design judgment',
     anatomy='The parts of a download: the icon before the word, the words from “Download” to the size, the 44 px height, '
             'and a file not ready with its dashed edge and reason.',
     code_caption='A download that works and one that is not ready, live. Tab to the second and press it: it keeps focus '
                  'and says why.',
     specs=specs(
         (L_PAT, 'APG Link, on <code><a href download></code>; APG Button when a script builds the file. A file not '
                 'ready keeps its control focusable, with aria-disabled.'),
         (L_ST, 'Ready. Not ready: aria-disabled, a dashed edge and the reason, with focus kept. Hover and focus as Rule '
                '18.1.'),
         (L_KEY, 'Tab reaches it; Enter starts the download. A file that is not ready keeps focus, and a press does '
                 'nothing.'),
         (L_NAME, 'Its words, from “Download” to the size.'),
         (L_HEAR, 'The words and the role, link or button; the browser then reports the download in its own way.'),
         (L_TGT, '44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'The edge in ButtonText; a file not ready keeps its dashed edge in GrayText.'),
         (L_TH, 'As Rule 18.1, the quiet button.'),
         (L_BR, bs('download') + ' Chrome from version 65 and Edge from version 79 ignore it for a file on another site, '
                'so serve each file from your own.'),
     ),
     related=['26', '27', '11'],
     builders=['Measure the size when the page is built, in kilobytes of 1,000 bytes, rounded, and write it into the '
               'words.'],
     failure=dict(
         caption='<strong>Fails Rule 18.14.</strong> Three links all read “Download”, with no file, type or size, so a '
                 'screen reader’s list of links hears the same word three times.',
         alt='Failure case: do not publish. An Illustrative list at 360 px of three files, the brand guide, the tokens and '
             'the logo files, each followed by a link that says only “Download”. A note reads “Out of their rows, the '
             'three links sound the same.”',
         notes='Picture of a fault: download links named with one word (SC 2.4.4).'))

# ---- 18.15 Search -----------------------------------------------------------------------------------------------
rule(n=15, set='c-18-search', name='Search',
     title='Search with a labeled field and one status line.',
     rule=['On a product page a search sits in a search landmark, the search element, so a screen reader can jump '
           'straight to it. It has a visible label above its field and a field of type search; a placeholder never '
           'stands in for the label. Results update as the reader types, and focus stays in the field. The status line '
           'under it gives the count and, when nothing matches, the advice in the same line: '
           f'“0 of {CL_COUNT} symbols. No symbol matches. Clear the search or the filters to see more.”',
           'Once the field holds text, a Clear the search control appears at its end, a 44 by 44 px cross (Rule 11.11), '
           'which empties the field and returns focus to it. Escape does the same. Where results come from a server, the '
           'line says “Searching” while they load.'],
     tokens=['--oa-color-field-ground', '--oa-color-border-strong', 'oa.size.icon.medium', 'oa.size.target.touch'],
     why=['A placeholder vanishes at the first letter typed, so the label sits above the field, where it stays in view. A status line lets a screen reader '
          'hear the count while focus stays in the field, and advice in the same line tells a reader who found nothing '
          'what to do next.'],
     basis='WCAG 2.2 SC 1.3.1, 2.4.6, 3.3.2 and 4.1.3; APG Landmarks pattern',
     anatomy='The parts of a search: the label, the field and its edge on the field ground, the Clear the search cross '
             'once text is in, and the status line with the count and the advice.',
     code_caption='A search over a short list, live. Type a word, then press Escape or Clear the search.',
     code_alt='A search over a short list, drawn live from the code below. In this guide the live copy draws the search '
              'landmark as a named group, so the guide’s own landmarks stay the only ones on the page; the code below '
              'keeps the real search element.',
     specs=specs(
         (L_PAT, 'A search landmark, on <code><search></code>; the Combobox pattern only if it ever offers suggestions '
                 'as the reader types.'),
         (L_ST, 'Empty; holding text, with Clear the search showing; results, with the count; no match, with the count and '
                'the advice; searching. Hover. Focus: the ring on the field.'),
         (L_KEY, 'Tab to the field and type. Escape clears it. Tab reaches Clear the search while it shows, and Enter '
                 'clears the field and returns focus to it.'),
         (L_NAME, 'The field: its visible label, such as “Search the symbols”. The clear control: “Clear the search”.'),
         (L_HEAR, 'The search landmark; the label and the field’s role; once typing pauses, the status line, such as “5 '
                  f'of {CL_COUNT} symbols.”'),
         (L_TGT, 'The field 44 px tall; Clear the search 44 by 44 px.', 'oa.size.target.touch'),
         (L_FC, 'The field’s edge and Clear’s cross draw in the system’s colors.'),
         (L_TH, f'The field’s ground is --oa-color-field-ground, {FIELD_N} on Newsprint and {FIELD_C} on Charcoal, with '
                'the strong border as its edge, which alone shows the field on Charcoal.'),
         (L_BR, bs('search', 'input-search') + ' In an older browser the search element is a plain box with no landmark, '
                'and the field still works.'),
     ),
     related=['10', '21'],
     builders=['Write the count and the advice into one status line, in one write, so a screen reader hears them '
               'together. Handle Escape in the script, since browsers differ on what Escape does in a search field.'],
     failure=dict(
         caption=f'<strong>Fails Rule 18.15.</strong> A placeholder is the only label, at {R_F15} to 1, and it disappears '
                 'once the reader types. The count under the field changes without being said.',
         alt=f'Failure case: do not publish. An Illustrative search field at 360 px with no label above it and the '
             f'placeholder “Search symbols…” in pale gray, {R_F15} to 1 on White. Under it, a count in small type reads '
             '“5 results”. A note reads “No label once you type, and the count is never announced.”',
         notes=f'Labeled failure: a placeholder at {R_F15} to 1 on purpose.',
         exempt=['contrast']))

# ---- 18.16 Filter bar -------------------------------------------------------------------------------------------
rule(n=16, set='c-18-filter-bar', name='Filter bar',
     title='Put the filters behind one Filters button that says how many are on.',
     rule=['A filter bar narrows a list. Its Filters button, with the funnel beside its word, opens and closes the filters '
           'as a disclosure (Rule 18.8), and its name counts what is on: “Filters, 2 on”. Inside, each filter is a chip '
           '(Rule 18.2), or a checkbox in a longer form. Every change updates the list at once, and the shared status line '
           'with it, such as “12 of 48 bills.”',
           'Clear filters shows only while a filter is on. A press turns every filter off, hides the control and moves '
           'focus to Filters, since focus cannot stay on a control that has gone.'],
     tokens=['--oa-color-border-strong', 'oa.size.icon.medium', 'oa.size.target.touch'],
     why=['A count in the name tells a reader who closed the filters that the list is still narrowed. Moving focus to '
          'Filters keeps a keyboard reader in place when Clear filters goes, where focus would otherwise fall to the top '
          'of the page.'],
     basis='WCAG 2.2 SC 2.4.3, 4.1.2 and 4.1.3; APG Disclosure and Button patterns',
     anatomy='The parts of a filter bar: the Filters button with its funnel, word, count and chevron, the chips inside, '
             'Clear filters, and the shared status line.',
     code_caption='A filter bar over a short list, live. Open Filters, turn a chip on, then press Clear filters and see '
                  'where focus goes.',
     specs=specs(
         (L_PAT, 'APG Disclosure for Filters and Button for each chip; APG Checkbox for filters inside a form.'),
         (L_ST, 'Filters closed or open, the chevron down or up, the count in its name. Chips on or off, as Rule 18.2. '
                'Clear filters shown or hidden. No match: the shared status line with its advice. Hover. Focus.'),
         (L_KEY, 'Tab to Filters; Enter or Space opens it. Tab through the chips; Space turns each on or off. Tab to Clear '
                 'filters; Enter clears and moves focus to Filters.'),
         (L_NAME, '“Filters” with its count, such as “Filters, 2 on”; each chip its word; “Clear filters”.'),
         (L_HEAR, '“collapsed” or “expanded” on Filters; “pressed” on a chip; the status line’s new count after each '
                  'change.'),
         (L_TGT, '44 px tall for Filters, each chip and Clear filters.', 'oa.size.target.touch'),
         (L_FC, 'As Rule 18.2, with the funnel and the chevron in currentColor.'),
         (L_TH, 'As Rule 18.2.'),
         (L_BR, 'Buttons and ARIA states, with nothing newer than ' + bs('focus-visible')),
     ),
     related=['10', '21'],
     builders=['Keep the count in the button’s own words, such as “Filters” and a visible “2 on”, so its name starts with '
               'what the reader sees. Move focus before you hide Clear filters.'],
     failure=dict(
         caption='<strong>Fails Rule 18.16.</strong> The filters open only while a pointer rests on Filters, and its name '
                 'never says how many are on.',
         alt='Failure case: do not publish. An Illustrative filter bar at 360 px. A pointer rests on the word Filters, and '
             'a list of four kinds of record drops under it; two are on. The word Filters shows no count. A note reads '
             '“Open only on hover, and closed it hides that two filters are on.”',
         notes='Picture of a fault: content that shows only on hover (SC 1.4.13) and a name with no count.'))

# ---- 18.17 Form -------------------------------------------------------------------------------------------------
rule(n=17, set='c-18-form', name='Form',
     title='Give every field a visible label and its own error message.',
     rule=['Each field has a visible label above it and, where it helps, a hint under the label joined by '
           'aria-describedby, such as “Five digits”. A placeholder never stands in for either. Personal fields carry '
           'autocomplete, such as email and postal-code, so the browser can fill them. A field stays open to typing while '
           'its form can still send; a Send button that cannot run yet keeps focus and says why, as Rule 18.1 sets.',
           'On a send with mistakes, each wrong field takes aria-invalid, the 4 px Pillar Red bar at its left edge and a '
           'message under it joined by aria-describedby: the error mark in ink, “Error:” and how to fix it, on the Error '
           'Band on Newsprint and on the ground on Charcoal. Focus moves to the first field to fix, and the ask steps down '
           'to the primary look while the error holds the red (Rule 11.16). A send that works writes its result to a '
           'status line with the success mark.'],
     tokens=['--oa-color-field-ground', '--oa-color-border-strong', '--oa-color-state-error-bar',
             '--oa-color-state-error-band', '--oa-color-state-error-text', '--oa-color-state-success-mark',
             '--oa-color-state-success-text', 'oa.border.width.bar', 'oa.size.target.touch'],
     why=['A label that stays in view helps a reader check what they typed, and autocomplete saves typing for a reader '
          'with limited movement. Moving focus to the first field to fix puts the reader where the work is, and the '
          'field’s description reads the message there, so nothing needs an alert that interrupts.'],
     basis='WCAG 2.2 SC 1.3.5, 3.3.1, 3.3.2, 3.3.3 and 4.1.3; Rule 11.15',
     anatomy='The parts of a form field: the label, the hint, the field and its edge on the field ground, and in error, '
             'the 4 px red bar, the mark, “Error:” and the fix on the band; then the send button and the success line.',
     code_caption='A two-field sign-up form, live. Send it with a field wrong to see focus move to it, then send it right.',
     specs=specs(
         (L_PAT, 'None fits. Native fields in a form with no name of its own, which adds no landmark.'),
         (L_ST, 'Default: a 1 px strong edge on the field ground. Focus: the ring. Error: the 4 px red bar, aria-invalid '
                'and the message with its mark and “Error:”. Sending: the button reads “Sending” and carries '
                'aria-disabled. Success: the status line with the success mark.'),
         (L_KEY, 'Tab through the fields and the send button. Enter in a field sends. After a failed send, focus lands '
                 'on the first field to fix.'),
         (L_NAME, 'Each field its label, with its hint and, after a failed send, its message as its description.'),
         (L_HEAR, 'On landing in the field to fix: its label, its invalid state and the message. After a good send: the '
                  'status line.'),
         (L_TGT, 'Fields and the send button at least 44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'The red bar is a border and holds in CanvasText. The band drops out, and the mark and “Error:” carry '
                'the error.'),
         (L_TH, f'Fields on --oa-color-field-ground. The red bar measures {R_BAR_N} to 1 on Newsprint, so the mark and '
                f'“Error:” carry the error there, and {R_BAR_C} to 1 on Charcoal, where the message takes no band.'),
         (L_BR, bs('autocomplete')),
     ),
     related=['11', '22', '05'],
     builders=['Call <code>preventDefault()</code> on the form’s submit, check every field, then set '
               '<code>aria-invalid</code> and the messages before moving focus, so the field is described when focus '
               'lands.',
               'Give each field <code>aria-invalid="false"</code> from the start, and set it back to '
               '<code>"false"</code> once the reader fixes it. A field without the attribute takes the browser’s own '
               'check, which calls an email address wrong while the reader is still typing it.'],
     failure=dict(
         caption='<strong>Fails Rule 18.17.</strong> The errors sit in a box at the top that names no field, the fields '
                 'have placeholders in place of labels, and focus stays on Send.',
         alt='Failure case: do not publish. An Illustrative sign-up form at 360 px. At its top, a box in ink reads “Please '
             'fix the errors below.” and names no field. Two fields under it carry only the placeholders “Email” and '
             '“ZIP code”, and neither field is marked. A Send button closes the form. A note reads “Focus stays on Send, '
             'and nothing joins an error to its field.”',
         notes='Picture of a fault: errors that point at no field (SC 3.3.1) and placeholder labels (SC 3.3.2).'))

# ---- 18.18 Messages ---------------------------------------------------------------------------------------------
rule(n=18, set='c-18-messages', name='Messages',
     title='Give every message its mark and its first word.',
     rule=['An error, a warning and a success each start with their mark and their words (Rule 11.15). An error starts '
           '“Error:” and says how to fix it, beside a 4 px Pillar Red bar. A warning starts “Warning:” beside a 4 px bar in '
           'ink, and a success says what happened beside the Verdigris mark. Each bar is a left border.',
           'A message that a script writes into the page goes into a status line, which a screen reader reads at its next '
           'pause. Only an error that appears with no field to move focus to uses <code>role="alert"</code>, which interrupts. A '
           'message already in the page when it loads is plain text, since neither role announces it then.'],
     tokens=['--oa-color-state-error-bar', '--oa-color-state-error-band', '--oa-color-state-warning-mark',
             '--oa-color-state-success-mark', 'oa.border.width.bar', 'oa.size.icon.medium'],
     why=['The mark and the first word give each message its kind in a shape and in words, so color never carries it '
          'alone. A status line reaches a screen reader without moving focus or cutting off what it is reading, and '
          'keeping alerts for errors keeps interruptions rare.'],
     basis='WCAG 2.2 SC 1.4.1, 1.4.11 and 4.1.3; WAI-ARIA 1.2 status and alert roles',
     anatomy='The parts of each message: its 24 px mark, its first word, its words, the 4 px bar on an error or a '
             'warning, and the Error Band '
             'behind an error on Newsprint.',
     code_caption='An error, a warning and a success, live in both themes.',
     specs=specs(
         (L_PAT, 'None fits; WAI-ARIA 1.2’s status role, and its alert role for an error with no field.'),
         (L_ST, 'Error, warning and success; inside a line of text, the 16 px marks.'),
         (L_KEY, 'None: a message takes no focus.'),
         (L_NAME, 'None; its words are the message.'),
         (L_HEAR, 'A status line: its new words at the next pause. An alert: its words at once. A message in the page '
                  'when it loads: its words only when the reader reaches them.'),
         (L_TGT, 'No control.'),
         (L_FC, 'The bars, as borders, hold; the marks draw in currentColor; the Error Band drops out.'),
         (L_TH, f'On Charcoal an error takes no band; its red bar measures {R_BAR_C} to 1, and its mark and words turn '
                f'Newsprint. The success mark measures {R_OK_N} to 1 on Newsprint and {R_OK_C} on Charcoal.'),
         (L_BR, ARIA_NOTE + ' Whether a change is heard depends on the browser and the screen reader together.'),
     ),
     related=['11', '05', '17'],
     builders=['Put the status line in the page, empty, when it loads, and write into it later; a status line added '
               'with its words already inside may not be read.'],
     failure=dict(
         caption='<strong>Fails Rule 18.18.</strong> Three messages are told apart only by the color of their boxes, with '
                 'no mark, no first word and no bar.',
         alt='Failure case: do not publish. Three Illustrative messages at 360 px, each a tinted box of words: a pink box '
             'that says the ZIP code needs five digits, a white box that says the record was last checked in March, and '
             'a gray box that says the reader is signed up. None has a mark, a first word such as “Error:” or a bar.',
         notes='Picture of a fault: message kinds in color alone (SC 1.4.1).'))

# ---- 18.19 Loading and empty ------------------------------------------------------------------------------------
rule(n=19, set='c-18-loading-empty', name='Loading and empty states',
     title='Say in words what is loading or missing.',
     rule=['While a part of the page waits for its data, it shows a still drawing and words that name what is coming, such '
           'as “Loading the tracker”, in a status line, with no spinner and no pulse (Rule 17.7). The words sit where the '
           'content will, so nothing jumps when the data lands.',
           'When the data holds nothing, the part says what is missing and what to do next, inside a dashed edge: “No '
           'bills match these filters. Clear the filters to see every bill.” The empty words are plain text, and they '
           'name a step the reader can take on the page, such as a control in the filter bar.'],
     tokens=['--oa-color-state-loading-text', '--oa-color-state-loading-mark', '--oa-color-state-empty-text',
             '--oa-color-state-empty-edge'],
     why=['Words tell every reader what is happening. A spinner shows only that something is happening, and a pulse '
          'moves without end. Saying what to do next turns an empty list into a step.'],
     basis='WCAG 2.2 SC 2.2.2 and 4.1.3; design judgment',
     anatomy='The parts of a loading state, its still drawing and its words, and of an empty state, its dashed edge, '
             'what is missing and what to do next.',
     code_caption='A loading state and an empty state, live in both themes.',
     specs=specs(
         (L_PAT, 'None fits; the status role for the loading words.'),
         (L_ST, 'Loading: the words and a still drawing. Empty: what is missing and what to do, inside a dashed edge. '
                'Loaded: the content in the same place.'),
         (L_KEY, 'None of its own; the control the empty words name takes Tab.'),
         (L_NAME, 'None; the words say it.'),
         (L_HEAR, 'The loading words once, at the next pause, when loading starts; the content when it lands; the empty '
                  'words when the reader reaches them.'),
         (L_TGT, 'Any control the empty words name, wherever the page holds it, at least 44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'The dashed edge and the drawing hold in CanvasText.'),
         (L_TH, f'Loading and empty words in the secondary color, {R_DIS_N} to 1 on Newsprint and {R_DIS_C} on '
                'Charcoal.'),
         ('Motion', 'None: the drawing is still, and nothing moves while the reader waits.'),
         (L_BR, ARIA_NOTE),
     ),
     related=['17', '11'],
     builders=['Swap the loading words for the content in one write, and keep the box the same height while it waits.'],
     failure=dict(
         caption='<strong>Fails Rule 18.19.</strong> A spinning circle with no words stands for loading, and when nothing '
                 'matches, the space is left blank.',
         alt='Failure case: do not publish. Two Illustrative panels at 360 px. The first holds only a circle drawn as an '
             'open ring, meant to spin, with no words. The second, after loading, is an empty box with nothing in it. A '
             'note reads “No words while it loads, and none when the list is empty.”',
         notes='Picture of a fault, drawn still: a wordless spinner and a blank empty state (D2-200).'))

# ---- 18.20 Tracker ----------------------------------------------------------------------------------------------
rule(n=20, set='c-18-tracker', name='Tracker',
     title='Update a live tracker in place.',
     rule=['A tracker built from chapter 11’s marks is a list of steps, each with its name and one state word: Done, Now, '
           'You can take part now, Not yet, Never happened or Stopped (Rules 11.2 and 11.4). When a bill moves, the tracker redraws only the steps that '
           'changed and writes one sentence to its status line that names the new step, and the bill too where the page '
           'follows more than one.',
           'The tracker takes no focus and moves nothing on the page when it updates. While its data loads it says so in '
           'words (Rule 18.19), and when nothing matches it says what to do. When the data fails it gives the error with '
           'its mark and how to try again, and a record that has gone unchecked carries the warning of Rule 11.10.'],
     tokens=['oa.component.mark.ring.now', 'oa.component.mark.ring.ahead', 'oa.size.target.touch'],
     why=['One polite sentence for each change lets a screen reader user hear what moved without losing their place, and '
          'redrawing only the changed steps keeps a sighted reader from losing theirs. The states stay in words, so an '
          'update never rests on a mark changing color.'],
     basis='WCAG 2.2 SC 1.4.1 and 4.1.3; WAI-ARIA 1.2 status role; Rule 11.5',
     anatomy='The parts of a live tracker: the bill’s name, the six steps with their marks and state words, the status '
             'line under the list, and the check date with its warning mark.',
     code_caption='A tracker that updates, live. Each change is said once in the line under it.',
     specs=specs(
         (L_PAT, 'None fits; list markup for the steps and the status role for an update.'),
         (L_ST, 'Done, Now, You can take part now, Not yet, Never happened and Stopped (Rules 11.2 and 11.4); loading; empty; '
                'error; the warning on a record unchecked too long (Rule 11.10).'),
         (L_KEY, 'None of its own; a link inside, such as a bill’s page, takes Tab.'),
         (L_NAME, 'The list’s label names the bill; each step its name and state word.'),
         (L_HEAR, 'The steps read in order; on an update, one sentence from the status line, once.'),
         (L_TGT, '44 px for any control on a tracker (Rule 11.7).', 'oa.size.target.touch'),
         (L_FC, 'Chapter 11’s marks keep their shapes in CanvasText, and the words carry each state.'),
         (L_TH, 'Chapter 11’s marks on Charcoal, in Newsprint and Dim Newsprint, with the take-part disc keeping its '
                'red.'),
         (L_BR, ARIA_NOTE),
     ),
     related=['11', '21', '17'],
     builders=['Write the sentence into a status line that was in the page, empty, from the start, and write only once '
               'for each bill that moves.'],
     failure=dict(
         caption='<strong>Fails Rule 18.20.</strong> An “Updated!” box flashes up for three seconds and does not say which '
                 'bill moved or where.',
         alt='Failure case: do not publish. An Illustrative tracker card at 360 px for a bill on public meeting notices, '
             'with a dark box over its top corner that reads “Updated!”. A note reads “Gone after three seconds, and it '
             'names no bill and no step.”',
         notes='Picture of a fault: a timed toast with no content (SC 2.2.1, 4.1.3) and performed enthusiasm.'))

# ---- 18.21 Report reader ----------------------------------------------------------------------------------------
rule(n=21, set='c-18-report-reader', name='Report reader',
     title='Page through a report with buttons that keep their place.',
     rule=['A report reader shows one page at a time, with Previous page and Next page buttons, each with its arrow beside '
           'its word, and the page’s size as a choice of Fit width or Full size (Rule 18.3). The status line names the '
           'page, the count and the page’s title, such as “Page 2 of 4:” and the title.',
           'On the first page Previous page stays in place with aria-disabled and the line “This is the first page.”, and '
           'on the last Next page does the same; neither button moves focus. At Full size the page scrolls as Rule 18.11 '
           'sets. A page that is loading says so in the status line, and one that fails gives the error and how to try '
           'again. A reader that fills the screen opens in a native modal dialog.'],
     tokens=['--oa-color-state-disabled-edge', '--oa-color-field-ground', 'oa.size.icon.medium', 'oa.size.target.touch'],
     why=['Buttons that keep their place let a keyboard reader press Next page again and again without hunting for it, and '
          'a status line says where the reader is while focus stays put. A radio choice for the size says that only one '
          'size holds.'],
     basis='WCAG 2.2 SC 2.4.3, 4.1.2 and 4.1.3; APG Button and Radio Group patterns; the APG Carousel pattern’s rule '
           'that its buttons do not move focus',
     anatomy='The parts of a report reader: the page view, Previous page and Next page with their arrows, the unavailable '
             'button’s dashed edge and reason, the size choice, and the status line.',
     code_caption='A four-page report, live. Press Next page until the last page: the button keeps focus and says why it '
                  'waits.',
     specs=specs(
         (L_PAT, 'APG Button for each page button, in a named group with no toolbar role; APG Radio Group for the size; '
                 'APG Dialog (Modal) for a reader that fills the screen.'),
         (L_ST, 'First page, a middle page and the last page, each unavailable button with its reason; Fit width or Full '
                'size checked; loading; error. Hover. Focus.'),
         (L_KEY, 'Tab: the page while it scrolls, Previous page, Next page, then the size choice. Enter or Space turns '
                 'the page. The arrow keys change the size.'),
         (L_NAME, '“Previous page” and “Next page”; the size choice’s legend, such as “Page size”; the page by the '
                  'report’s title.'),
         (L_HEAR, 'After a press, the status line: the page, the count and the title. At either end, the disabled state '
                  'and the reason.'),
         (L_TGT, '44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'An unavailable button keeps its dashed edge, and the arrows draw in currentColor.'),
         (L_TH, f'The page sits on --oa-color-field-ground, {FIELD_N} on Newsprint and {FIELD_C} on Charcoal, inside a '
                'hairline edge that parts it from the ground.'),
         (L_BR, bs('dialog') + ' The dialog is needed only for a reader that fills the screen.'),
     ),
     related=['24', '11'],
     builders=['Turn the page by swapping its content inside the same page view, and write the status line after the '
               'swap, so the line never names a page the reader cannot see yet.'],
     failure=dict(
         caption='<strong>Fails Rule 18.21.</strong> On the last page Next page disappears, and focus falls back to the top '
                 'of the page.',
         alt='Failure case: do not publish. An Illustrative report reader at 360 px on page 4 of 4. Only Previous page '
             'shows under the page; where Next page stood there is empty space. A note reads “Next page is gone, and focus '
             'went with it.”',
         notes='Picture of a fault: a control that vanishes at an end and takes focus with it (SC 2.4.3).'))

# ---- 18.22 Loop stepper -----------------------------------------------------------------------------------------
rule(n=22, set='c-18-loop-stepper', name='Loop stepper',
     title='Step through a loop one step at a time.',
     rule=['A loop stepper walks a reader through a loop of connections one step at a time. Its buttons run in one order '
           'in every product, Play, Reset the loop, Previous step and Next step, each with its utility icon beside its '
           'word (Rule 11.14). A loop from our atlas takes its atlas title as its name, in quotation marks, with a line '
           'under it that gives its evidence grade, so the heading claims no more than the evidence holds (chapter 02’s '
           'house rule H08). The status line says each step as it arrives, “Step 2 of 3:” and the step’s '
           'sentence, and the step list marks the current step with <code>aria-current="step"</code> and a 4 px bar.',
           'Nothing plays until the reader presses Play. Play becomes Pause while it plays and Play again at the end, its '
           'icon and its word changing together (Rule 17.3), and it holds each step about 250 ms a word and never under six '
           'seconds, with reduced motion too (Rule 11.14). Next step, Previous step and Reset the loop stop the playback, and no '
           'button moves focus. At the start, Previous step and Reset the loop stay in place with aria-disabled and their '
           'reason; at the end, Next step does.'],
     tokens=['--oa-color-state-selected-bar', 'oa.border.width.bar', 'oa.size.icon.medium', 'oa.size.target.touch'],
     why=['Play on request keeps the page still for a reader who did not ask it to move, and a pace set by the words gives '
          'a slow reader time to finish each step. Buttons that keep focus let a reader press Next step again and again, '
          'and the status line says each step without repeating the rest.'],
     basis='WCAG 2.2 SC 2.2.1, 2.2.2, 4.1.2 and 4.1.3; APG Carousel pattern, its buttons without its slide roles',
     anatomy='The parts of a loop stepper: Play with its icon and word, Reset the loop, Previous step, Next step, an '
             'unavailable button’s reason, the status line, and the step list with its current step’s 4 px bar.',
     code_caption='Loop R1 from our systems atlas, three steps, live, with its grade under its name and its source '
                  'under the steps. Press Next step and listen for the line; press Play and it holds each step long enough '
                  'to read.',
     specs=specs(
         (L_PAT, 'None fits. The Carousel pattern is nearest, and the stepper takes its buttons and its rule that no '
                 'button moves focus, without its slide roles.'),
         (L_ST, 'Ready; step 1, 2 or 3; playing, with Pause; paused; ended, with Play again; unavailable buttons with '
                'their reasons; the current step’s bar.'),
         (L_KEY, 'Tab through the four buttons; Enter or Space presses one; focus stays on the button pressed.'),
         (L_NAME, '“Play”, “Pause” or “Play again”; “Reset the loop”; “Previous step”; “Next step”. Play changes its '
                  'word, so it carries no pressed state.'),
         (L_HEAR, 'Each step once, at the next pause: “Step 1 of 3:” and its sentence. The button’s new word when Play '
                  'becomes Pause, while focus is on it.'),
         (L_TGT, '44 px tall.', 'oa.size.target.touch'),
         (L_FC, 'Icons in currentColor; unavailable buttons keep their dashed edge; the step bar is a border and holds.'),
         (L_TH, 'The bar in --oa-color-state-selected-bar on either surface.'),
         ('Motion', 'Nothing plays on load. Under reduced motion the steps keep their pace, and any drawn runner jumps '
                    'from step to step.'),
         (L_BR, bs('reduced-motion')),
     ),
     related=['17', '15', '11'],
     builders=['Time each step from its own words, at 250 ms a word with a six-second floor, and clear the timer on '
               'every press of Next step, Previous step or Reset the loop.'],
     failure=dict(
         caption='<strong>Fails Rule 18.22.</strong> The loop starts on its own when the page loads, repeats without end '
                 'and offers no button to pause it.',
         alt='Failure case: do not publish. A panel at 360 px for Loop R1 from our systems atlas, showing “Step 1 of 3” and '
             'its sentence, “Wealth concentration raises money in politics.”, with no buttons at all. A note reads “Starts '
             'by itself on load and repeats with no way to stop it.”',
         notes='Picture of a fault: motion that starts by itself with no pause (SC 2.2.2).'))

# ---- 18.23 Diagram controls -------------------------------------------------------------------------------------
rule(n=23, set='c-18-diagram-controls', name='Diagram controls',
     title='Reach a drawing’s items from one Tab stop with the arrow keys.',
     rule=['The items in an atlas drawing, such as its areas, variables and loops, are toggle buttons in one group. The Tab '
           'key reaches the drawing once, at the selected item or the first, and the arrow keys move between items in '
           'reading order, with Home and End for the first and the last. Enter or Space selects an item, which lights its '
           'related items and opens its record in a panel, or a sheet on a phone; Escape closes it and returns focus to '
           'the item.',
           'A readout line under the drawing repeats the name of the item in focus, so a reader who zooms in sees it '
           'without hovering. The readout sits in its own line, covers nothing and keeps its words until focus moves to '
           'another item, and nothing on a drawing shows on hover alone. Each drawing also offers its lines in words behind a disclosure (Rule 18.8), and a drawing '
           'that holds values offers its data as a table the same way. Full size opens it in a native modal dialog. Zoom stays in words, as Zoom in, Zoom '
           'out, Fit and Reset.'],
     tokens=['--oa-color-state-muted-mark', '--oa-color-graphic-essential', 'oa.size.target.touch'],
     why=['One Tab stop for each drawing keeps a keyboard reader from passing every item to leave it, and the arrow keys '
          'still reach each one. The lines in words, with a table where a drawing holds values, give a reader who cannot see the drawing the same connections, '
          'and the readout takes the place of help that would show only on hover.'],
     basis='WCAG 2.2 SC 1.1.1, 1.4.13, 2.1.1, 2.5.1 and 4.1.2; APG Button, Disclosure and Dialog (Modal) patterns',
     anatomy='The parts of the diagram controls: the drawing’s items, the item in focus with its heavier mark and '
             'underlined label, the selected item, the muted items, the readout line, the panel with its title, and the '
             'disclosure for the lines in words.',
     code_caption='A small drawing of Loop R1’s three items, live, with the loop’s grade under its name. Tab to it once, '
                  'move with the arrow keys, select with Enter and close with Escape.',
     specs=specs(
         (L_PAT, 'APG Button, as toggle buttons, for the items; Disclosure for More and Less, the lines in words and the '
                 'table; Dialog (Modal) for Full size.'),
         (L_ST, 'Hover and focus: a heavier mark and an underlined label, the rest muted. Selected: aria-pressed and the '
                'selected look. Muted. The current step of a loop.'),
         (L_KEY, 'Tab reaches the drawing once. The arrow keys move between items, Home and End to the ends. Enter or '
                 'Space selects. Escape closes the panel and returns focus to the item.'),
         (L_NAME, 'Each item a full sentence: its typed ID (Rule 18.24), its name and what a higher value means.'),
         (L_HEAR, 'The item’s sentence, its role and “pressed” or “not pressed”; the panel’s title when it opens.'),
         (L_TGT, 'Each item at least 44 px tall on a phone.', 'oa.size.target.touch'),
         (L_FC, 'Marks keep their shapes in CanvasText, and the selected item keeps its bold label.'),
         (L_TH, 'Muted marks in --oa-color-state-muted-mark on either surface.'),
         (L_BR, bs('dialog', 'focus-visible')),
     ),
     related=['15', '21', '14'],
     builders=['Give one item <code>tabindex="0"</code> and the rest <code>tabindex="-1"</code>, and move both with the '
               'arrow keys. The readout is plain text, never a status line, since it changes with every key.'],
     failure=dict(
         caption='<strong>Fails Rule 18.23.</strong> The drawing answers only to a pointer: the Tab key passes over it, and '
                 'each item’s words show only in a box on hover.',
         alt='Failure case: do not publish. An Illustrative drawing at 360 px of four linked circles. A pointer rests on one '
             'circle, and a small dark box beside it reads “Housing scarcity”. Nothing under the drawing gives its words or '
             'a table. A note reads “Only a pointer reaches the items, and their words show only on hover.”',
         notes='Picture of a fault: hover-only content (SC 1.4.13) and no keyboard path (SC 2.1.1).'))

# ---- 18.24 Typed ID chip ----------------------------------------------------------------------------------------
rule(n=24, set='c-18-id-chip', name='Typed ID chip',
     title='Write a typed ID with its type in words.',
     rule=['A typed ID names a record in the atlas by its type and its code together, such as “Loop R1” or “Reform '
           'R-04”, so a reader never meets a bare code (chapter 02’s house rule H11). The chip sets both in the label '
           'style on a hairline edge, in the text’s ink, and color never codes its type.',
           'A chip that opens its record is a link, underlined as Rule 18.5 sets, 1 px at rest and 2 px on hover, with a '
           'target at least 24 px tall; where '
           'the words around it do not name the record, the link’s description does. A chip that only names a record is plain text, with no role and no '
           'Tab stop.'],
     tokens=['--oa-color-border-hairline', '--oa-color-text-primary', 'oa.size.target.minimum'],
     why=['The type in words tells every reader what the code refers to, where a color would leave a screen reader, or a '
          'reader who cannot see the color, with a bare code. A chip that takes focus only when it goes somewhere keeps '
          'the Tab order to things that act.'],
     basis='WCAG 2.2 SC 1.3.1, 1.4.1 and 2.4.4; chapter 02, house rule H11',
     anatomy='The parts of a typed ID chip: its type word, its code, the hairline edge, and as a link, its underline on '
             'hover and its 24 px target.',
     code_caption='Two chips that name a record and one that opens it, live.',
     specs=specs(
         (L_PAT, 'None fits a label; APG Link when the chip opens its record.'),
         (L_ST, 'Plain. As a link: a 1 px underline, 2 px on hover; focus, the ring.'),
         (L_KEY, 'A linked chip takes Tab, and Enter follows it; a plain chip takes no focus.'),
         (L_NAME, 'Its words, such as “Loop R1”; a link adds the record’s name as its description, such as “Independent '
                  'citizen commissions draw election maps” for Reform R-04.'),
         (L_HEAR, 'As text, its words; as a link, its words and its role.'),
         (L_TGT, 'As a link, at least 24 px tall.', 'oa.size.target.minimum'),
         (L_FC, 'The edge and the words in CanvasText, or LinkText when it links.'),
         (L_TH, 'The edge, a hairline in --oa-color-border-strong, and the words in the text’s ink.'),
         (L_BR, 'Plain links and text, which every browser MDN lists reads.'),
     ),
     related=['02', '21', '10'],
     builders=['Keep the type word and the code in one element, with a no-break space between them, so a line never '
               'splits “Loop” from “R1”.'],
     failure=dict(
         caption='<strong>Fails Rule 18.24.</strong> The chips show bare codes, and only their fills say which is a loop '
                 'and which is a reform.',
         alt='Failure case: do not publish. A sentence at 360 px written from our systems atlas’s records, “R8 runs from '
             'housing scarcity to owners’ equity and back, and R-30 acts on that loop.”, with “R8” in a Prussian fill and '
             '“R-30” in a Verdigris fill and no type word for either. A note reads “A bare code, with its type in color '
             'alone.”',
         notes='Picture of a fault: bare codes (house rule H11) typed by color.'))


# ------------------------------------------------------------------------------------------------- failure plates
BASE_CSS = (':scope{--ink:var(--oa-color-text-primary);--sec:var(--oa-color-text-secondary);'
            '--edge:var(--oa-color-border-strong);--hair:var(--oa-color-border-hairline);--ground:var(--oa-color-surface)}'
            '.f18-fb{display:flex;align-items:center;gap:8px;padding:6px 12px;background:var(--oa-color-surface-charcoal);'
            'color:var(--oa-color-text-primary-on-charcoal);font:var(--oa-type-label);'
            'letter-spacing:var(--oa-type-label-letter-spacing);text-transform:var(--oa-type-label-text-transform)}'
            '.f18-ui{background:var(--ground);color:var(--ink);padding:16px 16px 20px;font:var(--oa-type-body)}'
            ':where(.f18-ui p){margin:0}'
            '.f18-n{margin-top:12px;font:var(--oa-type-caption);color:var(--sec)}'
            '.f18-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}'
            '.f18-btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px;box-sizing:border-box;'
            'border:1px solid var(--edge);font:var(--oa-type-ui)}'
            '.f18-lab{font:var(--oa-type-ui);margin-bottom:4px}'
            '.f18-field{min-height:44px;box-sizing:border-box;border:1px solid var(--edge);'
            'background:var(--oa-color-field-ground);padding:0 12px;display:flex;align-items:center;font:var(--oa-type-body)}'
            '.f18-ill{margin-bottom:12px}'
            '.f18-ico{display:block;flex:none;fill:none;stroke:currentColor}')
BAND = '<div class="f18-fb" aria-hidden="true"><span>×</span> Failure case: do not publish</div>'
ILL = '<p class="f18-ill"><span class="illus">Illustrative</span></p>'


def icon(name, px=24):
    return (f'<svg class="f18-ico" viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" '
            f'focusable="false" data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"/></svg>')


def fplate(css, body, note, illus=True):
    return (f'<style>{BASE_CSS}{css}</style>{BAND}<div class="f18-ui">{ILL if illus else ""}{body}'
            f'<p class="f18-n">{note}</p></div>')


POINTER = ('<svg class="f18-ptr" viewBox="0 0 16 22" width="16" height="22" aria-hidden="true" focusable="false">'
           '<path d="M1 1v17l4.5-4 3 7 3-1.3-3-6.8H14z" fill="var(--oa-color-surface-white)" '
           'stroke="var(--oa-color-text-primary-on-newsprint)" stroke-width="1.5" stroke-linejoin="round"/></svg>')

FAIL_HTML = {
    1: fplate('.f18-dis{color:var(--oa-color-derived-dim-newsprint);border-color:var(--oa-color-derived-dim-newsprint)}'
              '.f18-grow{flex:1 1 160px}',
              '<p class="f18-lab">Email</p><div class="f18-row"><div class="f18-field f18-grow"></div>'
              '<span class="f18-btn f18-dis">Send</span></div>',
              'Tab skips Send, and no words say what it waits for.'),
    2: fplate('.f18-on{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);'
              'border-color:var(--oa-color-surface-prussian)}.f18-k{margin:16px 0 8px;font:var(--oa-type-caption);color:var(--sec)}',
              '<div class="f18-row"><span class="f18-btn f18-on">Hearing this week</span><span class="f18-btn">Comment open'
              '</span><span class="f18-btn">Became law</span></div><p class="f18-k">The same chips in a contrast theme</p>'
              '<div class="f18-row"><span class="f18-btn">Hearing this week</span><span class="f18-btn">Comment open</span>'
              '<span class="f18-btn">Became law</span></div>',
              'In a contrast theme the fill drops out, and nothing marks the chip that is on.'),
    3: fplate('.f18-seg{display:flex}.f18-seg .f18-btn+.f18-btn{border-left:0}'
              '.f18-on{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);'
              'border-color:var(--oa-color-surface-prussian)}',
              '<div class="f18-seg"><span class="f18-btn">Fit width</span><span class="f18-btn f18-on">Full size</span></div>',
              'No group name, and the choice is a fill alone.'),
    4: fplate('.f18-mast{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;'
              'border-bottom:1px solid var(--hair)}.f18-t{font:var(--oa-type-ui)}'
              '.f18-moon{width:44px;height:44px;border:1px solid var(--edge);border-radius:50%;display:flex;'
              'align-items:center;justify-content:center}',
              '<div class="f18-mast"><span class="f18-t">Who Do They Answer To?</span><span class="f18-moon">'
              '<svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true" focusable="false">'
              '<path d="M15 3.5a8.5 8.5 0 1 0 5.5 13.8A7 7 0 0 1 15 3.5z" fill="none" stroke="var(--oa-color-text-primary)" '
              'stroke-width="2" stroke-linejoin="round"/></svg></span></div>',
              'Two states, no way back to the device, and no word for the theme that is on.'),
    5: fplate('.f18-a{color:var(--oa-color-surface-prussian)}',
              '<p>The county board holds <span class="f18-a">its budget hearing</span> on May 12. To send a comment before '
              'the hearing, <span class="f18-a">click here</span>.</p>',
              'The links are a color alone, and “click here” names no place.'),
    6: fplate('.f18-mast{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:6px 0;'
              'border-bottom:1px solid var(--hair)}.f18-t{font:var(--oa-type-ui)}'
              '.f18-bars{width:32px;height:32px;border:1px solid var(--edge);display:flex;align-items:center;'
              'justify-content:center;box-sizing:border-box}'
              '.f18-drop{margin:0 0 0 auto;width:200px;border:1px solid var(--edge);background:var(--oa-color-surface-white)}'
              '.f18-drop p{padding:8px 12px;border-bottom:1px solid var(--hair);font:var(--oa-type-ui)}'
              '.f18-under{margin-top:8px;text-decoration:underline}',
              '<div class="f18-mast"><span class="f18-t">Who Do They Answer To?</span><span class="f18-bars">'
              + icon('menu') + '</span></div>'
              '<div class="f18-drop"><p>Topics</p><p>How it works</p><p>Issue records</p><p>Reforms</p></div>'
              '<p class="f18-under">Read the evidence for each reform</p>',
              'No word on Menu, and Tab moves past the list into the page.'),
    7: fplate('.f18-list p{padding:8px 0;border-bottom:1px solid var(--hair);font:var(--oa-type-ui)}'
              '.f18-cur{color:var(--oa-color-surface-prussian)}',
              '<div class="f18-list"><p>03 Identity</p><p>04 The Ampersand and the hinge</p><p class="f18-cur">05 Color</p>'
              '<p>06 Type</p><p>07 Layout and spacing</p></div>',
              'The place is a color alone.', illus=False),
    8: fplate('.f18-row2{display:flex;justify-content:space-between;align-items:center;min-height:44px;'
              'border-bottom:1px solid var(--hair);font:var(--oa-type-ui)}.f18-plus{font:var(--oa-type-body);font-weight:700}'
              '.f18-open{padding:8px 0 12px;font:var(--oa-type-body-small)}',
              '<div class="f18-row2"><span>Sources</span><span class="f18-plus" aria-hidden="true">+</span></div>'
              '<div class="f18-row2"><span>The lines in words</span><span class="f18-plus" aria-hidden="true">+</span></div>'
              '<p class="f18-open">When homes are scarce, the homes that already exist sell for more, so owners’ equity '
              'grows. Owners whose wealth sits in their home object to new construction nearby, which keeps supply short.</p>',
              'The sign does not change, and the rows take no focus.', illus=False),
    9: fplate('.f18-tabs{display:flex}.f18-tabs .f18-btn+.f18-btn{border-left:0}'
              '.f18-on{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian);'
              'border-color:var(--oa-color-surface-prussian)}'
              '.f18-panel{border:1px solid var(--edge);border-top:0;padding:12px;font:var(--oa-type-body-small)}',
              '<div class="f18-tabs"><span class="f18-btn f18-on">Drawing</span><span class="f18-btn">In words</span>'
              '<span class="f18-btn">Table</span></div><div class="f18-panel">Households with concentrated wealth can spend '
              'more on campaigns, outside groups and lobbying.</div>',
              'Three Tab stops, no arrow keys, and the selection is a fill alone.', illus=False),
    10: fplate('.f18-t{width:100%;border-collapse:collapse;font:var(--oa-type-body-small)}'
               '.f18-t th,.f18-t td{text-align:left;padding:6px 4px;border-bottom:1px solid var(--hair);vertical-align:top}'
               '.f18-t th{font:var(--oa-type-ui)}.f18-ar{white-space:nowrap}',
               '<table class="f18-t"><thead><tr><th>Bill</th><th>Title</th><th><span class="f18-ar">Last action ↓</span></th>'
               '</tr></thead><tbody><tr><td>H.99003</td><td>Library hours</td><td>April 2</td></tr>'
               '<tr><td>S.99002</td><td>School bus contracts</td><td>March 3</td></tr>'
               '<tr><td>H.99001</td><td>Public meeting notice</td><td>January 16</td></tr></tbody></table>',
               'Only a pointer can sort, and the new order is never said.'),
    11: fplate('.f18-cut{overflow:hidden;border:1px solid var(--hair)}'
               '.f18-t{width:560px;border-collapse:collapse;font:var(--oa-type-body-small)}'
               '.f18-t th,.f18-t td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--hair)}'
               '.f18-t th{font:var(--oa-type-ui)}',
               '<div class="f18-cut"><table class="f18-t"><thead><tr><th>State</th><th>Committee</th><th>Hearing</th>'
               '<th>Sign up by</th></tr></thead><tbody><tr><td>Vermont</td><td>Transportation</td><td>April 8</td>'
               '<td>April 6</td></tr><tr><td>Oregon</td><td>Housing</td><td>April 10</td><td>April 9</td></tr></tbody>'
               '</table></div>',
               'Hidden past the edge, with no way to scroll by key.'),
    12: fplate('.f18-code{position:relative;border:1px solid var(--hair);padding:12px 48px 12px 12px;'
               'font:var(--oa-type-caption);font-family:ui-monospace,monospace;white-space:pre;overflow:hidden}'
               '.f18-chk{position:absolute;top:10px;right:10px}',
               '<div class="f18-code">.oa-chip {\n  min-height: 44px;\n  border: 1px solid;\n}<span class="f18-chk">'
               + icon('selected-check') + '</span></div>',
               'The icon turned into a check, and no words say what was copied.'),
    13: fplate('.f18-v{display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--hair);'
               'font:var(--oa-type-body-small)}.f18-v code{font-family:ui-monospace,monospace}.f18-gap{flex:1}',
               ''.join(f'<div class="f18-v"><span>{n}</span><code>&#35;{h}</code><span class="f18-gap"></span>{icon("copy", 16)}'
                       '</div>' for n, h in (('Charcoal', P['charcoal'].lstrip('#')), ('Newsprint', P['newsprint'].lstrip('#')),
                                            ('Prussian', P['prussian'].lstrip('#')))),
               'Three targets 16 px square, each heard only as Copy.'),
    14: fplate('.f18-v{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:8px 0;'
               'border-bottom:1px solid var(--hair);font:var(--oa-type-body-small)}.f18-u{text-decoration:underline}',
               ''.join(f'<div class="f18-v"><span>{n}</span><span class="f18-u">Download</span></div>'
                       for n in ('The brand guide', 'The tokens', 'The logo files')),
               'Out of their rows, the three links sound the same.'),
    15: fplate('.f18-ph{color:var(--oa-color-derived-dim-newsprint)}.f18-c{margin-top:6px;font:var(--oa-type-caption);'
               'color:var(--sec)}',
               '<div class="f18-field f18-ph">Search symbols…</div><p class="f18-c">5 results</p>',
               'No label once you type, and the count is never announced.'),
    16: fplate('.f18-fl{position:relative;display:inline-flex;align-items:center;gap:8px;min-height:44px;'
               'font:var(--oa-type-ui)}.f18-fl .f18-ptr{position:absolute;left:40px;top:26px}'
               '.f18-drop{margin-top:4px;width:220px;border:1px solid var(--edge);background:var(--oa-color-surface-white)}'
               '.f18-drop p{display:flex;gap:8px;align-items:center;padding:6px 12px;font:var(--oa-type-ui)}'
               '.f18-box{width:14px;height:14px;border:1px solid var(--edge);flex:none}'
               '.f18-box.f18-x{background:var(--oa-color-text-primary)}',
               '<div class="f18-fl">' + icon('filter') + '<span>Filters</span>' + POINTER + '</div><div class="f18-drop">'
               + ''.join(f'<p><span class="f18-box{" f18-x" if on else ""}"></span>{w}</p>' for w, on in
                         (('Bills', True), ('Records requests', False), ('Agency rules', True), ('Hearings', False)))
               + '</div>',
               'Open only on hover, and closed it hides that two filters are on.'),
    17: fplate('.f18-box{border:1px solid var(--edge);padding:8px 12px;margin-bottom:12px;font:var(--oa-type-ui)}'
               '.f18-ph{color:var(--sec)}.f18-mb{margin-bottom:12px}',
               '<p class="f18-box">Please fix the errors below.</p><div class="f18-field f18-ph f18-mb">Email</div>'
               '<div class="f18-field f18-ph f18-mb">ZIP code</div><span class="f18-btn">Send</span>',
               'Focus stays on Send, and nothing joins an error to its field.'),
    18: fplate('.f18-m{padding:10px 12px;margin-bottom:8px;font:var(--oa-type-body-small)}'
               '.f18-e{background:var(--oa-color-state-error-band-on-newsprint)}'
               '.f18-w{background:var(--oa-color-surface-white)}.f18-s{background:var(--oa-color-derived-dim-newsprint)}',
               '<p class="f18-m f18-e">The ZIP code needs five digits.</p><p class="f18-m f18-w">This record was last '
               'checked in March.</p><p class="f18-m f18-s">You are signed up for reminders.</p>',
               'Three kinds of message, told apart by color alone.'),
    19: fplate('.f18-p{border:1px solid var(--hair);min-height:72px;display:flex;align-items:center;justify-content:center;'
               'margin-bottom:8px}.f18-k{font:var(--oa-type-caption);color:var(--sec);margin-bottom:4px}',
               '<p class="f18-k">While it loads</p><div class="f18-p"><svg viewBox="0 0 32 32" width="32" height="32" '
               'aria-hidden="true" focusable="false"><path d="M16 4a12 12 0 1 1-12 12" fill="none" '
               'stroke="var(--oa-color-text-primary)" stroke-width="3" stroke-linecap="round"/></svg></div>'
               '<p class="f18-k">With nothing to show</p><div class="f18-p"></div>',
               'No words while it loads, and none when the list is empty.'),
    20: fplate('.f18-card{position:relative;border:1px solid var(--edge);padding:12px;font:var(--oa-type-body-small)}'
               '.f18-card b{font:var(--oa-type-ui)}.f18-toast{position:absolute;top:8px;right:8px;padding:6px 12px;'
               'background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);'
               'font:var(--oa-type-ui)}',
               '<div class="f18-card"><p><b>H.99001</b></p><p>Public meeting notice</p><p>Step 2 of 6, Hearing</p>'
               '<span class="f18-toast">Updated!</span></div>',
               'Gone after three seconds, and it names no bill and no step.'),
    21: fplate('.f18-pg{border:1px solid var(--hair);background:var(--oa-color-surface-white);padding:12px;min-height:96px;'
               'font:var(--oa-type-body-small);margin-bottom:12px}.f18-pg b{font:var(--oa-type-ui)}'
               '.f18-two{display:grid;grid-template-columns:1fr 1fr;gap:8px}',
               '<div class="f18-pg"><p><b>Who decides the list</b></p><p>The county engineer ranks the repairs, and the '
               'board approves the list each spring.</p></div><p class="f18-n">Page 4 of 4</p>'
               '<div class="f18-two"><span class="f18-btn">' + icon('arrow').replace('<svg ', '<svg style="transform:scaleX(-1)" ', 1)
               + 'Previous page</span><span></span></div>',
               'Next page is gone, and focus went with it.'),
    22: fplate('.f18-loop{border:1px solid var(--edge);padding:12px;font:var(--oa-type-body-small)}'
               '.f18-loop b{font:var(--oa-type-ui)}.f18-k{font:var(--oa-type-caption);color:var(--sec);margin-bottom:8px}',
               '<p class="f18-k">From our systems atlas, Loop R1</p><div class="f18-loop"><p><b>Step 1 of 3</b></p>'
               '<p>Wealth concentration raises money in politics.</p></div>',
               'Starts by itself on load and repeats with no way to stop it.', illus=False),
    23: fplate('.f18-dg{position:relative;height:150px}.f18-tip{position:absolute;left:150px;top:28px;padding:4px 8px;'
               'background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);'
               'font:var(--oa-type-caption)}.f18-dg .f18-ptr{position:absolute;left:118px;top:44px}',
               '<div class="f18-dg"><svg viewBox="0 0 328 150" width="328" height="150" aria-hidden="true" focusable="false">'
               '<g fill="none" stroke="var(--oa-color-text-primary)" stroke-width="2"><circle cx="40" cy="40" r="22"/>'
               '<circle cx="110" cy="40" r="22"/><circle cx="110" cy="110" r="22"/><circle cx="40" cy="110" r="22"/>'
               '<path d="M62 40h26M110 62v26M88 110H62M40 88V62"/></g></svg><span class="f18-tip">Housing scarcity</span>'
               + POINTER + '</div>',
               'Only a pointer reaches the items, and their words show only on hover.'),
    24: fplate('.f18-c{display:inline-block;padding:0 8px;font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing)}'
               '.f18-c1{background:var(--oa-color-surface-prussian);color:var(--oa-color-text-primary-on-prussian)}'
               '.f18-c2{background:var(--oa-color-palette-verdigris);color:var(--oa-color-palette-white)}',
               '<p><span class="f18-c f18-c1">R8</span> runs from housing scarcity to owners’ equity and back, and '
               '<span class="f18-c f18-c2">R-30</span> acts on that loop.</p>',
               'A bare code, with its type in color alone.', illus=False),
}


# ------------------------------------------------------------------------------------------------- keyboard paths
_UNSET = object()


def step(key=None, focus=None, states=None, status=_UNSET, status_has=None, type=None, **kw):
    """One step of a path: press key (or type text), then check focus, states and the status line."""
    s = {}
    if key:
        s['key'] = key
    if type is not None:
        s['type'] = type
    if focus is not None:
        s['focus'] = focus
    if states:
        s['states'] = states
    if status is not _UNSET:
        s['status'] = status
    if status_has:
        s['status_has'] = status_has
    s.update(kw)
    return s


def st(el, **kw):
    d = {'el': el}
    d.update(kw)
    return d


def path(name, steps, **kw):
    d = {'name': name}
    d.update(kw)
    d['steps'] = steps
    return d


OUT = 'outside'
B_WHY = '.oa-button[aria-describedby$="oa-button-why"]'
B_SEND = '.oa-button[aria-describedby$="oa-button-sending"]'
T_ONE = '.oa-toggle:not(.oa-toggle--chip)'
T_ONE_LINE = '.oa-toggle:not(.oa-toggle--chip) + .oa-toggle-status'
T_CHIPS_LINE = '.oa-toggle-why + .oa-toggle-status'


def chip(n):
    return f'.oa-toggle-chips > .oa-toggle:nth-child({n})'


def pressed(el, v):
    return st(el, attr='aria-pressed', **{'is': v})


def tab(n):
    return f'.oa-tabs-tab:nth-child({n})'


def sel(n):
    return st(tab(n), attr='aria-selected', **{'is': 'true'})


SORT1, SORT2 = '.oa-table-th:nth-child(1) .oa-table-sort', '.oa-table-th:nth-child(2) .oa-table-sort'
TLINE = '.oa-table-status'
COPY1 = '.oa-copy-row:nth-child(1) .oa-copy-button'
COPY2 = '.oa-copy-row:nth-child(2) .oa-copy-button'
KEYS = {
    1: [path('Tab through every button; the unavailable ones keep focus, and a press does nothing', [
        step('Tab', '.oa-button--primary:not([aria-disabled]):not(.oa-button--icon-end)'),
        step('Tab', '.oa-button--quiet:not(.oa-button--icon-start)'),
        step('Tab', '.oa-button--icon-start'),
        step('Tab', '.oa-button--icon-end'),
        step('Tab', '.oa-button--ask:not([data-oa-yield])'),
        step('Tab', B_WHY, [st(B_WHY, attr='aria-disabled', **{'is': 'true'})]),
        step('Enter', B_WHY, [st(B_WHY, attr='aria-disabled', **{'is': 'true'})]),
        step('Space', B_WHY),
        step('Tab', B_SEND, [st(B_SEND, attr='aria-disabled', **{'is': 'true'})]),
        step('Tab', '.oa-button--ask[data-oa-yield]'),
        step('Tab', OUT)])],
    2: [path('Turn the toggle and the chips on and off; each line says what changed, and focus stays', [
        step('Tab', T_ONE, [pressed(T_ONE, 'false')]),
        step('Space', T_ONE, [pressed(T_ONE, 'true')], status='You follow this bill. We email you when it moves.',
             status_el=T_ONE_LINE),
        step('Enter', T_ONE, [pressed(T_ONE, 'false')], status='You no longer follow this bill.', status_el=T_ONE_LINE),
        step('Tab', chip(1), [pressed(chip(1), 'true')]),
        step('Space', chip(1), [pressed(chip(1), 'false')], status='No topic is on, so every bill shows.',
             status_el=T_CHIPS_LINE),
        step('Tab', chip(2)),
        step('Space', chip(2), [pressed(chip(2), 'true')], status='Showing bills on Health care.', status_el=T_CHIPS_LINE),
        step('Tab', chip(3)),
        step('Enter', chip(3), [pressed(chip(3), 'true')], status='Showing bills on Health care and Elections.',
             status_el=T_CHIPS_LINE),
        step('Tab', chip(4), [st(chip(4), attr='aria-disabled', **{'is': 'true'})]),
        step('Space', chip(4), [pressed(chip(4), 'false')], status='Showing bills on Health care and Elections.',
             status_el=T_CHIPS_LINE),
        step('Tab', OUT)])],
    3: [path('Enter at the checked choice; the arrow keys check each choice and pass the one that waits', [
        step('Tab', '.oa-choice-input[value="summary"]', [st('.oa-choice-input[value="summary"]', prop='checked', **{'is': True})]),
        step('ArrowRight', '.oa-choice-input[value="text"]', [st('.oa-choice-input[value="text"]', prop='checked', **{'is': True}),
                                                              st('.oa-choice-input[value="summary"]', prop='checked', **{'is': False})]),
        step('ArrowRight', '.oa-choice-input[value="summary"]', [st('.oa-choice-input[value="summary"]', prop='checked', **{'is': True}),
                                                                 st('.oa-choice-input[value="changes"]', prop='checked', **{'is': False})]),
        step('ArrowLeft', '.oa-choice-input[value="text"]', [st('.oa-choice-input[value="text"]', prop='checked', **{'is': True})]),
        step('Tab', OUT)])],
    4: [path('Enter at Match my device; choose Dark, Light, then the device again; the guide and its storage stay as they are', [
        step('Tab', '.oa-theme-input[value="device"]', [st('.oa-theme-input[value="device"]', prop='checked', **{'is': True})]),
        step('ArrowLeft', '.oa-theme-input[value="dark"]', [st('.oa-theme-input[value="dark"]', prop='checked', **{'is': True}),
                                                           st('.oa-theme-page', attr='data-oa-theme', **{'is': 'dark'}),
                                                           st(':root', attr='data-oa-theme', **{'is': 'light'}),
                                                           {'storage': 'oa-theme', 'is': None}]),
        step('ArrowLeft', '.oa-theme-input[value="light"]', [st('.oa-theme-page', attr='data-oa-theme', **{'is': 'light'}),
                                                            {'storage': 'oa-theme', 'is': None}]),
        step('ArrowLeft', '.oa-theme-input[value="device"]', [st('.oa-theme-page', attr='data-oa-theme', **{'is': 'device'}),
                                                             st(':root', attr='data-oa-theme', **{'is': 'light'}),
                                                             {'storage': 'oa-theme', 'is': None}]),
        step('Tab', OUT)])],
    5: [path('The skip link shows when it takes focus and moves focus to the main content', [
        step('Tab', '.oa-link-skip', [st('.oa-link-skip', visible=True)]),
        step('Enter', '.oa-link-main')]),
        path('Tab through the links; the one to another site says so in its name; muted text takes no stop', [
            step('Tab', '.oa-link-skip'),
            step('Tab', '.oa-link-text a[href^="#"]'),
            step('Tab', '.oa-link-text a[href^="https:"]', [st('.oa-link-text a[href^="https:"] .oa-link-vh', text='(another site)')]),
            step('Tab', '.oa-link--item[aria-current="page"]'),
            step('Tab', '.oa-link--item:not([aria-current])'),
            step('Tab', OUT)]),
        path('A cross-reference moves focus to the part it names', [
            step('Tab', '.oa-link-skip'),
            step('Tab', '.oa-link-text a[href^="#"]'),
            step('Enter', '[id$="oa-link-steps"]')])],
    6: [path('Wide: Tab through the home link and the parts; the current part says so', [
        step('Tab', '.oa-masthead-home'),
        step('Tab', '.oa-masthead-part[aria-current="page"]', [st('.oa-masthead-menu', visible=False)]),
        step('Tab', '.oa-masthead-part:not([aria-current])'),
        step('Enter', '[id$="oa-masthead-page"]')], widths=[1440]),
        path('Narrow: Menu opens a modal menu at the current part; Tab moves through it; Escape and Close the menu return to Menu', [
            step('Tab', '.oa-masthead-home'),
            step('Tab', '.oa-masthead-menu', [st('.oa-masthead-menu', attr='aria-expanded', **{'is': 'false'}),
                                              st('.oa-masthead-parts', visible=False)]),
            step('Enter', '.oa-masthead-row-link[aria-current="page"]', [st('.oa-masthead-menu', attr='aria-expanded', **{'is': 'true'}),
                                                                        st('.oa-masthead-dialog', prop='open', **{'is': True})]),
            step('Escape', '.oa-masthead-menu', [st('.oa-masthead-menu', attr='aria-expanded', **{'is': 'false'}),
                                                 st('.oa-masthead-dialog', prop='open', **{'is': False})]),
            step('Space', '.oa-masthead-row-link[aria-current="page"]', [st('.oa-masthead-dialog', prop='open', **{'is': True})]),
            step('Shift+Tab', '.oa-masthead-close'),
            step('Tab', '.oa-masthead-row-link[aria-current="page"]'),
            step('Tab', '.oa-masthead-dialog .oa-masthead-row-link:not([aria-current])'),
            step('Tab', '.oa-masthead-dialog .oa-masthead-row-link:not([aria-current])'),
            step('Tab', '.oa-masthead-dialog .oa-masthead-row-link:not([aria-current])'),
            step('Tab', '.oa-masthead-dialog .oa-masthead-row'),
            step('Enter', '.oa-masthead-dialog .oa-masthead-row', [st('.oa-masthead-dialog .oa-masthead-row', attr='aria-expanded', **{'is': 'true'}),
                                                                   st('[id$="oa-masthead-topics"]', visible=True)]),
            step('Tab', '[id$="oa-masthead-topics"] .oa-masthead-row-link'),
            step('Escape', '.oa-masthead-menu', [st('.oa-masthead-dialog', prop='open', **{'is': False})]),
            step('Enter', '.oa-masthead-row-link[aria-current="page"]'),
            step('Shift+Tab', '.oa-masthead-close'),
            step('Enter', '.oa-masthead-menu', [st('.oa-masthead-dialog', prop='open', **{'is': False})])], widths=[390])],
    7: [path('Tab through the breadcrumb, the list and the links before and after; each current place says so', [
        step('Tab', '.oa-location-link:not([aria-current])'),
        step('Tab', '.oa-location-link:not([aria-current])'),
        step('Tab', '.oa-location-link[aria-current="page"]'),
        step('Tab', '.oa-location-item:not([aria-current])'),
        step('Tab', '.oa-location-item[aria-current="page"]'),
        step('Tab', '.oa-location-item:not([aria-current])'),
        step('Tab', '.oa-location-item:not([aria-current])'),
        step('Tab', '.oa-location-step:not(.oa-location-step--next)'),
        step('Tab', '.oa-location-step--next'),
        step('Enter', '[id$="oa-location-page"]')])],
    8: [path('Close and open the details, then the button disclosure; each says its state', [
        step('Tab', '.oa-disclosure:nth-of-type(1) > summary', [st('.oa-disclosure:nth-of-type(1)', prop='open', **{'is': True})]),
        step('Enter', '.oa-disclosure:nth-of-type(1) > summary', [st('.oa-disclosure:nth-of-type(1)', prop='open', **{'is': False})]),
        step('Space', '.oa-disclosure:nth-of-type(1) > summary', [st('.oa-disclosure:nth-of-type(1)', prop='open', **{'is': True})]),
        step('Tab', '.oa-disclosure:nth-of-type(2) > summary', [st('.oa-disclosure:nth-of-type(2)', prop='open', **{'is': False})]),
        step('Enter', '.oa-disclosure:nth-of-type(2) > summary', [st('.oa-disclosure:nth-of-type(2)', prop='open', **{'is': True})]),
        step('Tab', '.oa-disclosure-button', [st('.oa-disclosure-button', attr='aria-expanded', **{'is': 'false'}),
                                              st('[id$="oa-disclosure-lines"]', visible=False)]),
        step('Enter', '.oa-disclosure-button', [st('.oa-disclosure-button', attr='aria-expanded', **{'is': 'true'}),
                                                st('[id$="oa-disclosure-lines"]', visible=True)]),
        step('Space', '.oa-disclosure-button', [st('.oa-disclosure-button', attr='aria-expanded', **{'is': 'false'})]),
        step('Tab', OUT)])],
    9: [path('Enter at the selected tab; the arrow keys, Home and End move and select; the tab that waits takes focus only', [
        step('Tab', tab(1), [sel(1)]),
        step('ArrowRight', tab(2), [sel(2), st(tab(1), attr='aria-selected', **{'is': 'false'}),
                                    st('[id$="oa-tabs-p2"]', visible=True), st('[id$="oa-tabs-p1"]', visible=False)]),
        step('End', tab(4), [st(tab(4), attr='aria-disabled', **{'is': 'true'}), sel(2)]),
        step('ArrowRight', tab(1), [sel(1)]),
        step('ArrowLeft', tab(4), [sel(1)]),
        step('Home', tab(1), [sel(1)]),
        step('Tab', '[role="tabpanel"]:not([hidden])', [st('[id$="oa-tabs-p1"]', visible=True)])])],
    10: [path('Reverse the sorted column, sort another; the line says each order', [
        step('Tab', SORT1, [st('.oa-table-th:nth-child(1)', attr='aria-sort', **{'is': 'ascending'})]),
        step('Enter', SORT1, [st('.oa-table-th:nth-child(1)', attr='aria-sort', **{'is': 'descending'})],
             status='Sorted by bill, highest number first.', status_el=TLINE),
        step('Space', SORT1, [st('.oa-table-th:nth-child(1)', attr='aria-sort', **{'is': 'ascending'})],
             status='Sorted by bill, lowest number first.', status_el=TLINE),
        step('Tab', SORT2),
        step('Enter', SORT2, [st('.oa-table-th:nth-child(2)', attr='aria-sort', **{'is': 'ascending'}),
                              st('.oa-table-th:nth-child(1)', attr='aria-sort', **{'is': None})],
             status='Sorted by title, A to Z.', status_el=TLINE)])],
    11: [path('Where the steps are wider than the frame: reach it, scroll it with the arrow keys, then leave', [
        step('Tab', '.oa-scroll-frame[tabindex="0"][role="group"]', [st('.oa-scroll-hint', visible=True)]),
        step('ArrowRight', '.oa-scroll-frame', [st('.oa-scroll-frame', prop='scrollLeft', above=0)]),
        step('Tab', OUT)], widths=[390]),
        path('Where the frame holds the steps whole: no Tab stop and no hint', [
            step('Tab', OUT, [st('.oa-scroll-hint', visible=False), st('.oa-scroll-frame', attr='tabindex', **{'is': None})])],
            widths=[1440])],
    12: [path('Copy the HTML; the line says what was copied', [
        step('Tab', '.oa-code-panel:nth-of-type(1) .oa-code-copy'),
        step('Enter', '.oa-code-panel:nth-of-type(1) .oa-code-copy', status='Copied the HTML, 2 lines, to the clipboard.')],
        setup={'clipboard': 'allow'}),
        path('A refused copy turns the line into an error and leaves the code selected, with focus on it', [
            step('Tab', '.oa-code-panel:nth-of-type(1) .oa-code-copy'),
            step('Enter', 'textarea.oa-code-fallback', [st('.oa-code-status', attr='data-oa-state', **{'is': 'error'})],
                 status_has='Error: The browser blocked copying.')], setup={'clipboard': 'deny'})],
    13: [path('Copy each value; the line names what was copied', [
        step('Tab', COPY1),
        step('Enter', COPY1, status='Copied --oa-color-text-primary.'),
        step('Tab', COPY2),
        step('Enter', COPY2, status='Copied #121212, Charcoal.')], setup={'clipboard': 'allow'}),
        path('A refused copy selects the value in a field, with focus on it', [
            step('Tab', COPY1),
            step('Enter', 'input.oa-copy-fallback', status_has='Error: The browser blocked copying.')],
            setup={'clipboard': 'deny'})],
    14: [path('Tab past the ready download to the one not ready; it keeps focus and says why', [
        step('Tab', 'a.oa-download[download]'),
        step('Tab', '.oa-download[aria-disabled="true"]', [st('.oa-download[aria-disabled="true"]', attr='aria-describedby', present=True)]),
        step('Enter', '.oa-download[aria-disabled="true"]'),
        step('Tab', OUT)])],
    15: [path('Type, hear the count, then clear with Escape; focus stays in the field', [
        step('Tab', 'input[type="search"]', [st('.oa-search-clear', visible=False)], status='12 of 12 reforms', status_el='.oa-search-status'),
        step(type='voting', focus='input[type="search"]', states=[st('.oa-search-clear', visible=True)], status='1 of 12 reforms',
             status_el='.oa-search-status'),
        step('Escape', 'input[type="search"]', [st('input[type="search"]', prop='value', **{'is': ''}),
                                                st('.oa-search-clear', visible=False)], status='12 of 12 reforms', status_el='.oa-search-status')]),
        path('No match: the count and the advice in one line; Clear the search returns focus to the field', [
            step('Tab', 'input[type="search"]'),
            step(type='zzzz', focus='input[type="search"]',
                 status='0 of 12 reforms. No reform matches. Clear the search to see all 12.', status_el='.oa-search-status'),
            step('Tab', '.oa-search-clear'),
            step('Enter', 'input[type="search"]', [st('input[type="search"]', prop='value', **{'is': ''})],
                 status='12 of 12 reforms', status_el='.oa-search-status')])],
    16: [path('Open Filters, turn a chip on, then Clear filters sends focus to Filters', [
        step('Tab', '.oa-filters-toggle', [st('.oa-filters-toggle', attr='aria-expanded', **{'is': 'false'}),
                                           st('.oa-filters-clear', visible=False)]),
        step('Enter', '.oa-filters-toggle', [st('.oa-filters-toggle', attr='aria-expanded', **{'is': 'true'}),
                                             st('[id$="oa-filters-sheet"]', visible=True)]),
        step('Tab', '.oa-filters-chip[data-oa-filter="elections"]'),
        step('Space', '.oa-filters-chip[data-oa-filter="elections"]',
             [st('.oa-filters-chip[data-oa-filter="elections"]', attr='aria-pressed', **{'is': 'true'}),
              st('.oa-filters-toggle', text='Filters, 1 on'), st('.oa-filters-clear', visible=True)],
             status='6 of 12 reforms', status_el='.oa-filters-status'),
        step('Shift+Tab', '.oa-filters-clear'),
        step('Enter', '.oa-filters-toggle', [st('.oa-filters-clear', visible=False), st('.oa-filters-toggle', text='Filters, 0 on'),
                                             st('.oa-filters-chip[data-oa-filter="elections"]', attr='aria-pressed', **{'is': 'false'})],
             status='12 of 12 reforms', status_el='.oa-filters-status')])],
    17: [path('Send with mistakes: each wrong field says so, and focus moves to the first', [
        step('Tab', 'input[autocomplete="email"]'),
        step(type='name@', focus='input[autocomplete="email"]',
             states=[st('input[autocomplete="email"]', attr='aria-invalid', **{'is': 'false'})]),
        step('Tab', 'input[autocomplete="postal-code"]'),
        step(type='021', focus='input[autocomplete="postal-code"]'),
        step('Tab', '.oa-form-send'),
        step('Enter', 'input[autocomplete="email"]', [st('input[autocomplete="email"]', attr='aria-invalid', **{'is': 'true'}),
                                                      st('input[autocomplete="postal-code"]', attr='aria-invalid', **{'is': 'true'}),
                                                      st('[id$="oa-form-email-error"]', visible=True)])]),
        path('Send right: the line says it is sending, then that it worked', [
            step('Tab', 'input[autocomplete="email"]'),
            step(type='reader@example.org', focus='input[autocomplete="email"]'),
            step('Tab', 'input[autocomplete="postal-code"]'),
            step(type='12345', focus='input[autocomplete="postal-code"]'),
            step('Enter', None, [st('input[autocomplete="email"]', attr='aria-invalid', **{'is': 'false'}),
                                 st('.oa-form-send', text='Sending')],
                 status_has='Sending', status_el='.oa-form-status'),
            step(None, None, [st('.oa-form-send', text='Remind me')], status_has='signed up', status_el='.oa-form-status',
                 wait=1200)])],
    18: [path('Messages take no focus', [step('Tab', OUT)])],
    19: [path('The loading and empty states take no focus of their own', [step('Tab', OUT)])],
    20: [path('Show the next update: the line says it once, and focus stays on the button', [
        step('Tab', '.oa-tracker-link'),
        step('Tab', '.oa-tracker-next'),
        step('Enter', '.oa-tracker-next', status_has='Step 3 of 6: Committee vote.', status_el='.oa-tracker-status'),
        step('Enter', '.oa-tracker-next', [st('.oa-tracker-alert', text_has='Error:')]),
        step('Enter', '.oa-tracker-next', status_has='Stopped at step 3 of 6', status_el='.oa-tracker-status')]),
        path('The link to take part moves focus to how to send testimony', [
            step('Tab', '.oa-tracker-link'),
            step('Enter', '[id$="oa-tracker-how"]')])],
    21: [path('Turn to the last page; each button keeps focus, and the line names each page', [
        step('Tab', '.oa-reader-prev', [st('.oa-reader-prev', attr='aria-disabled', **{'is': 'true'})]),
        step('Enter', '.oa-reader-prev', status='Page 1 of 4: Where the money comes from', status_el='.oa-reader-status'),
        step('Tab', '.oa-reader-next'),
        step('Enter', '.oa-reader-next', [st('.oa-reader-prev', attr='aria-disabled', **{'is': None})],
             status='Page 2 of 4: What a mile of road costs', status_el='.oa-reader-status'),
        step('Enter', '.oa-reader-next', status='Page 3 of 4: Repairs that wait', status_el='.oa-reader-status'),
        step('Enter', '.oa-reader-next', [st('.oa-reader-next', attr='aria-disabled', **{'is': 'true'}),
                                          st('[id$="oa-reader-why"]', text='This is the last page.')],
             status='Page 4 of 4: Who decides the list', status_el='.oa-reader-status'),
        step('Enter', '.oa-reader-next', status='Page 4 of 4: Who decides the list', status_el='.oa-reader-status'),
        step('Tab', '.oa-reader-size-input[value="fit"]', [st('.oa-reader-size-input[value="fit"]', prop='checked', **{'is': True})]),
        step('ArrowRight', '.oa-reader-size-input[value="full"]', [st('.oa-reader-size-input[value="full"]', prop='checked', **{'is': True})])])],
    22: [path('Step by hand; the line says each step, and no button moves focus', [
        step('Tab', '.oa-stepper-play'),
        step('Tab', '.oa-stepper-reset', [st('.oa-stepper-reset', attr='aria-disabled', **{'is': 'true'})]),
        step('Tab', '.oa-stepper-prev', [st('.oa-stepper-prev', attr='aria-disabled', **{'is': 'true'})]),
        step('Tab', '.oa-stepper-next'),
        step('Enter', '.oa-stepper-next', [st('.oa-stepper-step:nth-child(1)', attr='aria-current', **{'is': 'step'})],
             status_has='Step 1 of 3: Wealth concentration raises money in politics.', status_el='.oa-stepper-status'),
        step('Enter', '.oa-stepper-next', [st('.oa-stepper-step:nth-child(2)', attr='aria-current', **{'is': 'step'})],
             status_has='Step 2 of 3:', status_el='.oa-stepper-status'),
        step('Enter', '.oa-stepper-next', [st('.oa-stepper-next', attr='aria-disabled', **{'is': 'true'})],
             status_has='Step 3 of 3:', status_el='.oa-stepper-status'),
        step('Shift+Tab', '.oa-stepper-prev', [st('.oa-stepper-prev', attr='aria-disabled', **{'is': None})]),
        step('Enter', '.oa-stepper-prev', status_has='Step 2 of 3:', status_el='.oa-stepper-status'),
        step('Shift+Tab', '.oa-stepper-reset'),
        step('Enter', '.oa-stepper-reset', [st('.oa-stepper-reset', attr='aria-disabled', **{'is': 'true'})],
             status_has='Ready.', status_el='.oa-stepper-status')]),
        path('Play becomes Pause and back, with focus on it, under reduced motion too', [
            step('Tab', '.oa-stepper-play', [st('.oa-stepper-word', text='Play')]),
            step('Enter', '.oa-stepper-play', [st('.oa-stepper-word', text='Pause')], status_has='Step 1 of 3:', status_el='.oa-stepper-status'),
            step('Enter', '.oa-stepper-play', [st('.oa-stepper-word', text='Play')])], setup={'reducedMotion': True})],
    23: [path('One Tab stop, the arrow keys inside, Enter opens the panel, Escape returns to the part', [
        step('Tab', '.oa-diagram-node:nth-child(1) .oa-diagram-item'),
        step('ArrowRight', '.oa-diagram-node:nth-child(2) .oa-diagram-item', [st('.oa-diagram-readout', text_has='Money in politics')]),
        step('End', '.oa-diagram-node:nth-child(3) .oa-diagram-item'),
        step('Home', '.oa-diagram-node:nth-child(1) .oa-diagram-item'),
        step('Enter', '.oa-diagram-panel-name', [st('.oa-diagram-node:nth-child(1) .oa-diagram-item', attr='aria-pressed', **{'is': 'true'}),
                                                  st('.oa-diagram-panel', visible=True)]),
        step('Escape', '.oa-diagram-node:nth-child(1) .oa-diagram-item', [st('.oa-diagram-panel', visible=False)]),
        step('Tab', '.oa-diagram-summary')]),
        path('Full size opens a modal view; Escape returns focus to its button', [
            step('Tab', '.oa-diagram-item[tabindex="0"]'),
            step('Tab', '.oa-diagram-summary'),
            step('Tab', '.oa-diagram-open'),
            step('Enter', '.oa-diagram-shut', [st('.oa-diagram-dialog', prop='open', **{'is': True})]),
            step('Escape', '.oa-diagram-open', [st('.oa-diagram-dialog', prop='open', **{'is': False})])])],
    24: [path('The linked chip takes Tab and moves focus to its record; the plain chips take none', [
        step('Tab', 'a.oa-chip--link'),
        step('Enter', '[id$="oa-chip-r04"]')]),
        path('Only the linked chip is a stop', [step('Tab', 'a.oa-chip--link'), step('Tab', OUT)])],
}

def keys_doc(r):
    paths = KEYS[r['n']]
    return {
        'format': 'oa-keys/1',
        'set': r['set'],
        'rule': f'18.{r["n"]}',
        'component': r['name'],
        'about': ('The keyboard path of this code set, walked in each live stage by the guide check. Each path starts from '
                  'the component as the page first draws it, with focus on a stand-in control just before the stage. A '
                  'step presses "key" (a KeyboardEvent key; "Space" is the space bar) or types "type"; then "focus" is a '
                  'selector inside the stage that the focused element must match, or "outside"; "states" must hold ("" '
                  'is the stage, ":root" the page root); "status" is the exact words of the stage\'s role="status" line, '
                  'and "status_has" words it must contain. Written by the accessibility lead for chapter 18, Rule '
                  f'18.{r["n"]}.'),
        'paths': paths,
    }


# ------------------------------------------------------------------------------------------------- assembly and checks
BANNED = ('genuinely', 'really', 'truly', 'actually', 'leverage', 'underscore', 'simply', 'reflect')
CODES = re.compile(r'\b(?:DR|D1|D2|G1)-\d+|\bT-\d+\b|\bMaster Brief\b|\bPhase\b|\bGates?\b|\b[Bb]oards?\s+(?:\d+|[A-F])\b'
                   r'|\b[Ss]tages?\s+[A-C]\b|\bthe studio\b|\bV5\b|\bAtlas V7')


def check_words(s, where):
    t = re.sub(r'<code>.*?</code>', '', s, flags=re.S)
    plain = re.sub(r'<[^>]+>', '', t)
    bad = []
    if EM in plain or EN in plain:
        bad.append('em or en dash')
    if re.search(r"(?<![=\w])'(?=[A-Za-z])|(?<=[a-z])'(?=[a-z])", plain):
        bad.append('straight apostrophe')
    if re.search(r'"[A-Za-z]', plain):
        bad.append('straight double quote')
    for w in BANNED:
        if re.search(r'\b' + w + r'\b', plain, re.I):
            bad.append(f'"{w}"')
    m = CODES.search(plain)
    if m:
        bad.append(f'studio code {m.group(0)!r}')
    if re.search(r',\s+not\s+\w+', plain):
        bad.append('a “, not” turn')
    if bad:
        raise SystemExit(f'{where}: {", ".join(bad)} in: {plain[:200]}')


def walk_words(o, where):
    if isinstance(o, str):
        check_words(o, where)
    elif isinstance(o, list):
        for i, x in enumerate(o):
            walk_words(x, f'{where}[{i}]')
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ('specimen', 'token', 'tokens', 'id', 'anchor', 'number', 'related', 'set', 'before_rule', 'chapter'):
                continue
            walk_words(v, f'{where}.{k}')


def build():
    rules, specs_out, manifest = [], {}, {}
    if [r['n'] for r in RULES] != list(range(1, 25)):
        raise SystemExit('rules are not 18.1 to 18.24 in order')
    for r in RULES:
        rid, nn = f'18.{r["n"]}', f'{r["n"]:02d}'
        fid = f's-18-{nn}-failure'
        code = {'set': r['set'], 'name': r['name'], 'caption': r['code_caption']}
        if r.get('code_alt'):
            code['alt'] = r['code_alt']
        rules.append({
            'id': rid,
            'title': r['title'],
            'rule': r['rule'],
            'tokens': r['tokens'],
            'why': {'text': r['why'], 'basis': r['basis']},
            'correct': {'specimen': f's-18-{nn}-anatomy', 'caption': r['anatomy']},
            'failure': {'specimen': fid, 'caption': r['failure']['caption']},
            'code': code,
            'specs': r['specs'],
            'related': r['related'],
            'builders': r['builders'],
        })
        f = r['failure']
        frag = FAIL_HTML[r['n']]
        if re.search(r'<h[1-6]\b|<(nav|article|header|footer|main|aside|section|form|button|a|input)\b', frag, re.I):
            raise SystemExit(f'{fid}: a heading, landmark or control inside a picture')
        bare = re.sub(r'var\((?:[^()]|\([^()]*\))*\)', '', frag)
        bare = re.sub(r'\sd="[^"]*"', '', bare)
        if re.search(r'(?<![\w&])#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b(?![\w-])|\brgba?\(|\bhsla?\(', bare):
            raise SystemExit(f'{fid}: literal color outside var()')
        if re.search(r'font-size:\s*[\d.]+px', frag):
            raise SystemExit(f'{fid}: px font size')
        check_words(re.sub(r'<style>.*?</style>', '', frag, flags=re.S), fid)
        specs_out[fid] = frag + '\n'
        meta = {'chapter': CH, 'rule': rid, 'width_px': WIDTH, 'alt': f['alt'], 'illustrative': '<span class="illus">' in frag,
                'notes': f['notes'], 'fit_switch': False}
        if f.get('exempt'):
            meta['check_exempt'] = f['exempt']
        manifest[fid] = meta
    groups = [{'before_rule': b, 'number': i + 1, 'title': t, 'line': ln} for i, (b, t, ln) in enumerate(GROUPS)]
    ch = {
        'number': CH,
        'anchor': 'components',
        'title': 'Components and interaction',
        'part': 'Behavior',
        'instruction': 'Build controls that work by keyboard and screen reader and announce every change.',
        'opener': 's-18-opener',      # call 8: the systems designer's picture of a button, a chip and a choice (manifest-anatomy.json)
        'intro': INTRO,
        'groups': groups,
        'rules': rules,
        'extras': [],
        'related_chapters': [{'chapter': c, 'reason': why} for c, why in RELATED],
        'sources': SOURCES,
    }
    walk_words(ch, '18')
    for fid, m in manifest.items():
        check_words(m['alt'], f'{fid}.alt')
    keys = {r['set']: keys_doc(r) for r in RULES}
    return ch, specs_out, manifest, keys


def outputs():
    ch, specs_out, manifest, keys = build()
    out = {OUT_CH: json.dumps(ch, indent=2, ensure_ascii=False) + '\n',
           MANIFEST: json.dumps(dict(sorted(manifest.items())), indent=1, ensure_ascii=False) + '\n'}
    for fid, html_ in specs_out.items():
        out[OUT_SP / f'{fid}.html'] = html_
    for sid, doc in keys.items():
        out[CODE / f'{sid}.keys.json'] = json.dumps(doc, indent=1, ensure_ascii=False) + '\n'
    return out, ch


def notes_md():
    lines = ['### Anatomy plates: what each must label', '',
             'Each `s-18-NN-anatomy` goes in `manifest-anatomy.json`, drawn by the systems designer. The caption the chapter '
             'prints under each plate names its parts; each plate labels those parts on the component in the light theme, '
             'on Newsprint, at true size.', '',
             '| Plate | Rule | What it labels |', '|---|---|---|']
    for r in RULES:
        lines.append(f'| `s-18-{r["n"]:02d}-anatomy` | 18.{r["n"]} {r["name"]} | {r["anatomy"]} |')
    lines += ['', '### What each keys file relies on, set by set', '',
              'Every selector and status line the paths name, read from the keys data itself, with the number of paths and '
              'steps.', '', '| Set | Paths, steps | Selectors | Status lines |', '|---|---|---|---|']
    for r in RULES:
        sels, lines_ = [], []
        n_steps = 0
        for pth in KEYS[r['n']]:
            for stp in pth['steps']:
                n_steps += 1
                if stp.get('focus') and stp['focus'] != OUT:
                    sels.append(stp['focus'])
                for c in stp.get('states', []):
                    if c.get('el'):
                        sels.append(c['el'])
                if stp.get('status_el'):
                    lines_.append(stp['status_el'])
        uniq = list(dict.fromkeys(sels))
        lines.append(f'| `{r["set"]}` | {len(KEYS[r["n"]])}, {n_steps} | ' + ', '.join(f'`{x}`' for x in uniq).replace('|', '\\|')
                     + ' | ' + (', '.join(f'`{x}`' for x in dict.fromkeys(lines_)) or 'none') + ' |')
    return '\n'.join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    ap.add_argument('--notes', action='store_true')
    a = ap.parse_args()
    if a.notes:
        print(notes_md())
        return
    out, ch = outputs()
    if a.check:
        stale = [str(p.relative_to(ROOT)) for p, t in out.items() if not p.exists() or p.read_text() != t]
        print('chapter 18: current' if not stale else 'chapter 18: stale ' + ', '.join(stale))
        sys.exit(1 if stale else 0)
    CODE.mkdir(parents=True, exist_ok=True)
    for old in OUT_SP.glob('s-18-*-failure.html'):
        if old not in out:
            old.unlink()
    for p, t in out.items():
        p.write_text(t)
    print(f'chapter 18: {len(ch["rules"])} rules, {len(ch["groups"])} groups, 24 failure plates, 24 keys files; '
          f'{len(FIG)} figures: ' + '; '.join(f'{k} {v["value"]}' for k, v in FIG.items()))


if __name__ == '__main__':
    main()
