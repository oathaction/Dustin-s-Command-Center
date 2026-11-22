"""Chapter 21, The atlas (design director), Phase 4, chat 11c, November 22, 2026.

Usage:
    python3 -I work/build/scripts/phase-4/phase4_ch21_build.py                  write the chapter, specimens and manifest
    python3 -I work/build/scripts/phase-4/phase4_ch21_build.py --check          build everything in memory and report
    python3 -I work/build/scripts/phase-4/phase4_ch21_build.py --page-words A14 print one atlas page's words as JSON
                                                                                 (A11 to A17, or "all"); writes nothing

Writes:
    work/build/guide/chapters/21-atlas.json          the chapter, in the content contract chapters 16 and 20 follow
    work/build/guide/specimens/s-21-*.html           one fragment per specimen this generator owns
    work/build/guide/specimens/manifest-atlas.json   this chapter's manifest, written whole

Reads, never writes: the atlas model (work/extract/atlas-v7-data.json), the application kit's plates and its atlas test's
report once the kit has drawn them (work/build/app-kit/plates/), the exports manifest, and tokens.json and tokens.css
(through the stage A helpers).

The plan is work/handoffs/phase-4/20261121_Chapter-21-Plan.md (sixteen rules in five groups, one extra and an opener), and
the layout of every atlas page is work/handoffs/phase-4/20261122_Atlas-View-Specs.md. The pages are drawn by the
application kit's atlas-page renderer (the engineer's contract C9): a correct plate holds only its words around a
placeholder, <div data-oa-app="A14" data-oa-app-views="...">, and the guide build sets the kit's frames in its place
(D4-134). No specimen copies kit markup. Failure plates are small drawings this file makes from the tokens and the model,
each showing one fault.

Words. Every word a reader sees sits in the WORDS section near the top of this file, so the editor writes them there and
nothing else changes (brief section 6.1, job 6; the design director's notes, "Words for the editor"):
    W            the chapter's title, instruction, intro, group lines, opener caption and alt, related chapters, sources
    PARTS        the eight parts' plain names and questions (Dustin's words, DR-35 and DR-41)
    ATLAS        the words every atlas page shares: the title bar, the views, the breadcrumb, the locator
    PAGES        each atlas page's words, A11 to A17: its title's first part, its current view, its breadcrumb and the
                 template's own words (headings, labels, glosses, status lines and templates the kit fills)
    R['21.1'] to R['21.16']   each rule's title, rule, why, basis, specs, builders, captions and alts, then the words
                 drawn inside its failure plate
    EXTRA_HOW    the extra after Rule 21.14, How to read
The kit reads ATLAS and PAGES by running this file with --page-words (chapter 20's pattern, D4-155), so a page's words
are written once, here. The site's masthead and footer words stay chapter 20's (phase4_ch20_build.py --page-words).
The atlas's own stored text (titles, summaries, cases, citations, the subtitle and the snapshot) is read from the model by
the kit, never typed here (DR-37). Counts this file prints in the chapter's own words are read from the model at build
time through {placeholders}, never typed.

Specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color, no px
font size; every class is prefixed sx-.
"""
import argparse
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
P2 = HERE.parent / 'phase-2'


def _load(name, folder):
    spec = importlib.util.spec_from_file_location(name, folder / f'{name}.py')
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


B = _load('stage_a_systems_build', P2)
C = sys.modules['stage_a_systems_core']
ROOT = C.ROOT
OUT_CH = ROOT / 'work/build/guide/chapters/21-atlas.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-atlas.json'
KIT_PLATES = ROOT / 'work/build/app-kit/plates'
EXPORTS = ROOT / 'work/build/exports/phase-4'
MODEL_FILE = ROOT / 'work/extract/atlas-v7-data.json'
CH = '21'
ILLUS = B.ILLUS
NB = C.NBSP
T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
ctx = B.Ctx(T, {}, 'final')


# ================================================================================================ FACTS, read from the model
MODEL_BYTES = MODEL_FILE.read_bytes()
MODEL_SHA = hashlib.sha256(MODEL_BYTES).hexdigest()
M = json.loads(MODEL_BYTES)
META = M['meta']
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November',
          'December']


def date_words(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return f'{MONTHS[m - 1]} {d}, {y}'


# the counts the chapter's own words print, by the data lead's methods (R2), read at build time
NUMBERED = [k for k, v in M['loops'].items() if not str(v.get('closure', '')).startswith('conceptual')]
RETIRED = sorted(k for k, v in M['issues'].items() if v.get('retired'))
FACT = {
    'variables': len(M['nodes']),
    'connections': len(M['links']),
    'loops': len(M['loops']),
    'loops_numbered': len(NUMBERED),
    'reforms': len(M['reforms']),
    'issues': len(M['issues']),
    'retired': len(RETIRED),
    'retired_ids': RETIRED,
    'questions': len(M['pathways']),
    'hubs': len(M['hubs']),
    'snapshot': date_words(META['snapshot']),
    'double': 2 * len(M['links']),                                   # Rule 21.9's failure: each connection filed twice
    'answer_sources': len(set(next(p for p in M['pathways'] if p['id'] == 'PW06')['source_ids'])),
}
assert FACT['variables'] == META['counts']['variables'] and FACT['connections'] == META['counts']['connections'], \
    'the model’s own counts disagree with its records'


# ================================================================================================ WORDS
# Everything a reader sees. The editor's fields. A {name} in braces is a fact the build fills from the model; keep it.

W = {
    'title': 'The atlas',
    'instruction': 'Apply the system to the atlas, with typed IDs and evidence a step from every claim.',
    'intro': [
        'Our systems atlas, Who Do They Answer To?, lives inside our website, under the site’s masthead, with a '
        'title bar of its own. This chapter shows its four kinds of page: the home page, which draws the whole system '
        'and starts from an everyday question; a page for each reform; the Register, which files each of the atlas’s '
        '{connections} connections once with its evidence; and a page for each loop, which a reader can step through.',
        'Chapter 15 sets how each mechanism is drawn, and these pages use its rules as they stand. What this chapter '
        'adds is the page around the drawing. Every ID sits in a typed chip, every claim links to the record that grades '
        'it, and every page passes the atlas test before it ships.'],
    'groups': [
        ('21.1', 'The atlas in our website',
         'The atlas sits under the site’s masthead with a title bar of its own, and its home page draws the whole '
         'system and starts from a reader’s question.'),
        ('21.4', 'A page for each record',
         'A reform’s page reads its own record in the order a reader asks, and every ID on it opens the record it '
         'names.'),
        ('21.8', 'The Register',
         'The Register files each of the atlas’s connections once, with its sign, its grade and its source, and keeps '
         'what the atlas rejected in view.'),
        ('21.12', 'Loop pages',
         'A loop page reads the loop’s signs aloud, names its weakest step and lets a reader step through it at a '
         'pace they can follow.'),
        ('21.15', 'The dark mode and the atlas test',
         'The atlas reads the same on Charcoal, and every page passes one test against the model before it ships.'),
    ],
    'opener_caption': 'The home page of our systems atlas inside our website, on Newsprint and in the dark mode at 1440 and '
                      '390 pixels. A reader has pressed the question “Why can the same care produce different '
                      'bills?”, and the drawing lights the three parts of the system it reaches.',
    'opener_alt': 'The atlas home page four times: on a desktop at 1440 px and a phone at 390 px, each on Newsprint and in '
                  'the dark mode. Each shows the site’s masthead, the atlas’s title bar, the drawing of the '
                  'eight parts with a count on every flow, and the everyday questions, one of them pressed.',
    'related_chapters': [
        ('05', 'One working red a view, the screens of Rule 05.1 and the marks that keep 3 to 1.'),
        ('10', 'Rule 10.8: the atlas’s parts named in words, and the encoding glyphs.'),
        ('12', 'The red target (Rule 12.5) and the atlas locator (Rule 12.7).'),
        ('13', 'Grade words, the line code, delays, typed chips, dates and source lines.'),
        ('15', 'Every mechanism these pages draw.'),
        ('17', 'The pressed, muted and current looks, and the stepper’s motion.'),
        ('18', 'The chip, stepper, chooser, filters, toggle, disclosure and table.'),
        ('19', 'The WCAG map these pages add to.'),
        ('20', 'The masthead, menu, footer and theme switch the atlas sits in.'),
        ('28', 'The atlas test’s lines in the standards checklist.'),
    ],
    'sources': [
        'Source: our systems atlas, Who Do They Answer To?, Atlas V7, snapshot of {snapshot}, as extracted to the '
        'studio’s model file and read by this chapter’s build.',
        'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, '
        'as our accessibility lead read and quoted it on November 21, 2026.',
        'Source: the atlas concepts Field Manual, The Circuit, Who Can Act and Register, October 21, 2026, and the atlas '
        'editorial systems of November 5, 2026, cited as earlier drawings and never as evidence (Rule 15.25).',
    ],
}

# Dustin's plain names and questions for the eight parts (DR-35, DR-41), in the order effects travel; the model's own
# titles print beneath them, read by the kit. Outside forces has no question of its own (DR-35 gives none).
PARTS = {
    'X': ['Outside forces', None],
    'A': ['Wealth', 'Who holds the cards?'],
    'B': ['Voice', 'Who pays for influence?'],
    'C': ['Elections', 'Who picks them?'],
    'D': ['Checks', 'Who checks their work?'],
    'E': ['Policy', 'Whose side are the rules on?'],
    'EC': ['Your household', 'Who lives with the results?'],
    'TC': ['Technology', 'Who controls the machines?'],
}

# The words every atlas page shares (specs sections 2 and 3; the engineer's C9, plus views_button, DD11C-C3)
ATLAS = {
    'views_label': 'Atlas views',
    'views_button': 'Views',             # at most 46 px in oa.type.ui (specs 2.4); "Views" measures 44.3 px
    'views': [['Home', '/atlas'], ['Loops', '/atlas/loops'], ['Reforms', '/atlas/reforms'],
              ['The Register', '/atlas/register'], ['How to read', '/atlas/how-to-read']],
    'snapshot': 'Snapshot of {date}',
    'breadcrumb_label': 'Breadcrumb',
    'locator_alt': 'Where this page sits in our atlas: {part}. Atlas home',
    'title_end': 'Oath & Action',        # the title's third part (AL-01); its second is the model's own title
    'parts': PARTS,
    # the display words for a stored grade (Rule 13.3), and the glosses beside them
    'grades': {'documented': 'Documented', 'well-supported': 'Well supported', 'well_supported': 'Well supported',
               'plausible': 'Plausible', 'plausible_contested': 'Contested', 'contested': 'Contested',
               'hypothesis': 'Hypothesis'},
    'signs': {'+': 'raises', '-': 'lowers', 'none': 'decides'},
    'delays': {'S': 'under 2 years', 'M': '2 to 10 years', 'L': 'over 10 years'},
    'kinds': {'R': 'Reinforcing', 'B': 'Balancing'},
    'kind_words': {'variable': 'Variable', 'connection': 'Connection', 'loop': 'Loop', 'reform': 'Reform',
                   'issue': 'Issue', 'claim': 'Claim', 'domain': 'Domain', 'route': 'Route',
                   'rule-change': 'Rule change', 'delivery-case': 'Delivery case'},
    'not_checked': 'Not checked',
    'checked': 'Checked {date}',
    'as_of': 'As of {date}',
}

# The words of each page. "view" is the first part of the page's title (AL-01); "current_view" one of ATLAS['views'];
# "crumbs" the places above the page, from Home (None on the home page); the page's own crumb is the kit's typed chip
# or, on a page with no record, its current view. "page" holds the template's own words.
PAGES = {
    'A11': {
        'view': 'Atlas home',
        'current_view': 'Home',
        'crumbs': None,
        'page': {
            'h1': 'Who do they answer to?',
            'intro': 'Our atlas maps how power and money move through American government and the economy, and who can '
                     'change the rules. It holds {variables} variables, {connections} connections between them, {loops} '
                     'loops, {reforms} reforms and {issues} issue records, each graded by its evidence.',
            'switch': 'Show every variable',
            'key_main': 'The main circuit, part to part',
            'key_other': 'Other flows',
            'inside': '{n} connections inside',
            'inside_none': 'None inside',
            'variables': '{n} variables',
            'flow_line': '{n} to {part}',
            'questions_heading': 'Start from a question',
            'lit': 'This question reaches here',
            'status': 'This question reaches {parts}.',
            'answer_label': 'The short answer',
            'drawing_label': 'The parts of the system and the connections between them',
        },
    },
    'A12': {
        'view': 'Reform R-23, a minimum wage that rises with an index',
        'current_view': 'Reforms',
        'crumbs': [['Home', '/atlas'], ['Reforms', '/atlas/reforms']],
        'page': {
            'status_label': 'Where it stands',
            'problem': 'The problem',
            'remedy': 'The remedy',
            'where_heading': 'Where it acts',
            'where_note': 'Reform {reform} aims at {targets}.',
            'touches': 'It touches {loop}, whose chain holds neither target.',
            'aims_here': 'aims here',
            'grades_heading': 'How sure our atlas is',
            'source_link': 'Its source',
            'effects_heading': 'What it would change',
            'effects_confidence': 'Our atlas’s confidence: “{text}”',
            'routes_heading': 'How it could pass',
            'routes_head': ['Route', 'Who acts', 'How likely', 'Note', 'Checked'],
            'complements_heading': 'Works alongside',
            'sources_summary': 'Sources for this page',
        },
    },
    'A13': {
        'view': 'The Register: Congress, agencies and public services',
        'current_view': 'The Register',
        'crumbs': [['Home', '/atlas']],
        'page': {
            'h1': 'The Register',
            'intro': 'Every connection in our atlas, filed once on the sheet of the condition it moves, with its sign, '
                     'its grade and the atlas’s citation.',
            'index_heading': 'The sheets',
            'index_head': ['Sheet', 'Variables', 'Connections', 'Loops', 'Reforms', 'Issue records'],
            'none_filed': 'none filed',
            'whole': 'The whole atlas',
            'whole_issues': '{n}, one retired',
            'whole_note': 'The last row counts each loop and reform once, though many reach several sheets.',
            'sheet_question_label': 'Its everyday question',
            'variables_heading': 'Its variables',
            'connections_heading': 'Its connections',
            'conn_head': ['Connection', 'From, to', 'Sign', 'Type', 'Delay', 'Grade', 'The atlas’s citation'],
            'rejected_heading': 'Rejected option',
            'rejected_grade': 'Here the grade measures confidence in a finding of harm',
            'reviewed_heading': 'Reviewed and not drawn',
            'records_heading': 'Its issue records',
            'filters': 'Filters',
            'filters_on': 'Filters, {n} on',
            'showing': '{n} of {total} issue records',
        },
    },
    'A14': {
        'view': 'Loop R18, weakening watchdogs',
        'current_view': 'Loops',
        'crumbs': [['Home', '/atlas'], ['Loops', '/atlas/loops']],
        'page': {
            'kind': '{kind} loop',
            'grade_line': '{grade} for {from} to {to}',
            'facts_label': 'This loop',
            'facts': {'kind': 'Kind', 'steps': 'Steps', 'minus': 'Minus signs', 'closure': 'Closure', 'delay': 'Delay',
                      'weakest': 'Weakest step'},
            'minus_even': '{n}, an even count',
            'minus_odd': '{n}, an odd count',
            'stepper_heading': 'Step through the loop',
            'read_label': 'Read aloud',
            'arithmetic': 'Built from the signs: start with more, flip at each minus.',
            'parity_even': '{n} minus signs, an even count: the loop feeds itself.',
            'parity_odd': '{n} minus signs, an odd count: the loop holds itself in check.',
            'weakest_label': 'Weakest step',
            'weakest_line': 'The loop holds only as firmly as this link.',
            'also_aim': '{chips} also aim here',
            # the stepper's status lines; the kit prefixes "Step n of m: " and the hold counts every word read (AL-24)
            'steps': [
                {'line': 'Presidential action without new legislation lowers the ability to investigate and enforce the '
                         'rules. Firing inspectors general and commissioners, leaving boards without a quorum and cutting '
                         'staff all reduce what watchdogs can investigate and enforce.'},
                {'line': 'The ability to investigate and enforce the rules can lower presidential action without new '
                         'legislation, where the loop began. Audits, lawsuits and enforcement raise the cost of acting '
                         'without a law, provided the enforcer does not answer to the official being checked. Our atlas '
                         'grades this step plausible, the least certain in the loop.'},
            ],
            'step_prefix': 'Step {n} of {m}:',
            'chooser_legend': 'Reforms that aim at this loop',
            'effects_heading': 'Its effects',
            'routes_heading': 'How it could pass',
            'record_heading': 'The loop in our atlas’s words',
            'record_labels': {'summary': 'Summary', 'case': 'The case', 'qualification': 'What it depends on',
                              'adaptation': 'How it adapts'},
            'evidence_heading': 'Evidence for each step',
            'step_word': 'Step {n}',
            'on_sheet': 'Its line on sheet {sheet} of the Register',
            'records_line': 'Issue records on this loop: {n}',
        },
    },
    'A15': {
        'view': 'Loops',
        'current_view': 'Loops',
        'crumbs': [['Home', '/atlas']],
        'page': {
            'h1': 'Loops',
            'intro': 'Every loop in our atlas, the ones that feed themselves and then the ones that hold themselves in '
                     'check, each in the order the atlas lists it.',
            'reinforcing': 'Reinforcing',
            'balancing': 'Balancing',
            'head': ['Loop', 'Title', 'Steps', 'Minus signs', 'How it closes', 'Grade'],
            'no_chain': 'no numbered chain',
            # DR-321: the note under the index
            'titles_note': 'The atlas’s next version reviews the titles that state an effect.',
        },
    },
    'A16': {
        'view': 'How to read',
        'current_view': 'How to read',
        'crumbs': [['Home', '/atlas']],
        'page': {
            'h1': 'How to read our atlas',
            'intro': 'Every mark our atlas’s pages use, with its words and the rule that sets it.',
        },
    },
}


def _holds():
    """AL-24: 250 ms a word of everything the status line reads, "Step 1 of 2:" included, never under 6,000 ms."""
    pw = PAGES['A14']['page']
    m = len(pw['steps'])
    for i, s in enumerate(pw['steps'], 1):
        said = pw['step_prefix'].format(n=i, m=m) + ' ' + s['line']
        s['words'] = len(said.split())
        s['hold'] = max(6000, 250 * s['words'])


_holds()


R = {}
# ---- Group 1, the atlas in our website
R['21.1'] = {
    'title': 'Set every atlas page under the site’s masthead, with the atlas’s title bar beneath.',
    'rule': ['Our systems atlas is one part of our website, so every atlas page opens with the site’s masthead, with '
             'Who Do They Answer To? marked as the part the reader is in. Directly under it, the atlas’s title bar '
             'names the atlas, gives the date of its snapshot and lists its views: Home, Loops, Reforms, The Register '
             'and How to read. Pages below the home add a breadcrumb, and on wide screens a small locator that shows '
             'where the page sits in the whole system. Each page’s title names the view first, then the atlas, then '
             'Oath & Action.'],
    'why': 'A reader who reaches the atlas from a search or a shared link still sees whose site they are on and can '
           'reach every other part of it. The title bar keeps the atlas’s own views one step away without a second '
           'masthead.',
    'basis': 'DR-307; the accessibility lead’s AL-01, AL-09 and AL-17; ED-F8 and D2-65; chapter 20 as built (D4-189); '
             'design judgment for the title bar, from measured word widths',
    'specs': [('Order', 'Skip link, the site’s masthead, the atlas’s title bar, the breadcrumb, main, the site’s footer'),
              ('Title bar', 'A Charcoal band 56 px tall from edge to edge, in both themes: the atlas’s name in the label '
                            'style, then its subtitle and snapshot date in the caption style; the five views at the right'),
              ('Views', 'From 64em, in the masthead parts’ style and gap, ending at the parts’ right edge; the current '
                        'view in bold with a 2 px underline'),
              ('Under 64em', 'The name and the snapshot at the left, and a Views button that opens the five views as rows '
                             'in place; the subtitle shows from 48em'),
              ('Breadcrumb', 'A navigation named Breadcrumb, 8 px under the band; the current page last, bold and not '
                             'underlined; on a record’s page, the record’s chip'),
              ('Locator', '88 by 41 px at the breadcrumb row’s right end from 48em, the parts as boxes and the page’s '
                          'own filled in ink; hidden under 48em'),
              ('Page title', '[view] | Who Do They Answer To? | Oath & Action'),
              ('Landmarks', 'One banner, the site’s; navigations for the parts, the atlas’s views and the breadcrumb; '
                            'one main; one contentinfo')],
    'builders': ['Draw the masthead and footer from the website’s own renderer, add the atlas’s title bar as a '
                 'navigation of its own, and build each page title from the view’s own words.'],
    'correct_caption': 'The top of a loop page at 1440 px, and at 390 px with the views open: the site’s masthead with '
                       'the atlas as the current part, the atlas’s title bar, the breadcrumb and, on the desktop, the '
                       'locator.',
    'correct_alt': 'Two crops of a loop page’s top. On the desktop, the masthead with Who Do They Answer To? underlined, '
                   'a dark title bar naming the atlas with five views, a breadcrumb ending on the chip Loop R18 and a '
                   'small map of eight boxes with one filled. On the phone, the masthead, the dark title bar open to five '
                   'rows with Loops marked, and the breadcrumb.',
    'failure_caption': '<strong>Fails Rule 21.1.</strong> The atlas brings a masthead of its own, so a reader sees two sets '
                       'of links and cannot tell which site they are on, and the tab’s title names no page.',
    'failure_alt': 'The top of an atlas page with two mastheads: the site’s, with no part marked, and under it a second '
                   'banner with its own wordmark and its own copy of the site’s parts. The tab reads Oath & Action.',
    'fail_tab': 'Oath & Action',
    'fail_label': 'The top of the page at 1440 px, and its tab',
}
R['21.2'] = {
    'title': 'Open the atlas home on the whole system, with a count on every flow.',
    'rule': ['Start the atlas’s home page with the whole system on the first screen: one box for each part, each with '
             'its name, its question and the count of connections inside it, and one arrow for each pair of parts that '
             'connect, with the count of connections it carries. Draw the main circuit in full ink and the other flows '
             'in a lighter ink, all at one width. A switch opens every box in place to show its variables, and closes '
             'them again. Draw the system once on the page.'],
    'why': 'A newcomer sees how the parts fit together before reading any one of them, and every number on the drawing is '
           'a count a reader can check in the Register. One drawing that opens in place keeps the first screen short.',
    'basis': 'Concept 09, The Circuit; System 1’s overview; ED-F3, ED-F9 and ED-F10; DR-35; Rule 15.1; the data '
             'lead’s rulings R2, R6 and R7',
    'specs': [('Parts', 'Eight boxes in the order effects travel: Outside forces, Wealth, Voice, Elections, Checks, '
                        'Policy, Your household, Technology, each with its plain name, its question and the model’s '
                        'title beneath'),
              ('Boxes and pills', 'A part takes a box with square corners; a variable takes a pill (Rule 15.2)'),
              ('Counts', 'Inside each box and on each arrow, in the data label style with tabular figures, read at build '
                         'time; the build stops when a count and the model disagree'),
              ('Ink', 'The main circuit in the essential ink and its counts in bold; the other flows in the subtle ink; one '
                      'width, 2 px; one arrow for each direction of a pair'),
              ('Switch', 'A toggle button with its words and aria-pressed'),
              ('At 390 px', 'A stacked list of the eight parts, each with its counts and a “5 to Voice” line for '
                            'each flow it sends')],
    'builders': ['Count every number on the drawing from the model at build time, and stop the build when a count and the '
                 'model disagree.'],
    'correct_caption': 'The atlas home’s drawing with the switch pressed: every part open to its variables, at 1440 px '
                       'on Newsprint.',
    'correct_alt': 'The eight parts of the atlas as boxes, each open to its variables as rounded pills, with arrows '
                   'between the parts and a count on each arrow.',
    'failure_caption': '<strong>Fails Rule 21.2.</strong> The arrows widen with their counts and nothing on the drawing '
                       'says what a width measures, so the eye reads weight where the page prints a number.',
    'failure_alt': 'The five core parts in a row with arrows between them of different widths, the widest from Your '
                   'household to Wealth, and no key.',
    'fail_label': 'The core row at 1440 px, arrows by count',
}
R['21.3'] = {
    'title': 'Light the parts an everyday question reaches, and say which they are in words.',
    'rule': ['Offer the atlas’s everyday questions under their hubs, each as a button. When a reader presses one, mark it '
             'pressed with a check, bold words and a heavier edge, keep the parts its variables sit in at full strength '
             'with the words This question reaches here, and mute the rest. A status line names the parts in words, and '
             'the answer opens below with each figure linked to its evidence.'],
    'why': 'A reader who arrives with a bill in hand sees at once which parts of the system decide it. Words carry the '
           'result, so a reader who cannot see the shading, or who prints the page in gray, gets the same answer.',
    'basis': 'ED-F5; UX-4 and the accessibility lead’s AL-21; D2-1152; the pathway’s own variables; the data lead’s R6',
    'specs': [('Question', 'A toggle button, aria-pressed true when pressed; one pressed at a time'),
              ('Pressed look', 'The selected check before the words, bold words and a 2 px edge in the strong border '
                               'color, where an unpressed question keeps 1 px (Rule 17.10)'),
              ('Lit parts', 'The parts that hold the question’s own variables, at full strength with the words This '
                            'question reaches here; the rest muted'),
              ('Status line', 'Names the parts in words, once per press, never on load'),
              ('Hubs', 'Named in words, with no chip (Rule 10.8)')],
    'builders': ['Light a part only when the question’s own record names a variable in it, and write the same list in '
                 'the status line.'],
    'correct_caption': 'The question “Why can the same care produce different bills?” pressed beside unpressed '
                       'questions, and the three parts it reaches lit, at 1440 and 390 px on Newsprint and on Charcoal.',
    'correct_alt': 'Four crops of the atlas home: a list of questions with one marked by a check, bold words and a heavy '
                   'edge, and the drawing with Wealth, Checks and Your household in full ink, each labeled This question '
                   'reaches here, and the other parts muted.',
    'failure_caption': '<strong>Fails Rule 21.3.</strong> Only the weight of its words shows which question is pressed, and '
                       'only a tint shows which parts it reaches, so the answer is lost in gray print and to a reader who '
                       'cannot see the tint.',
    'failure_alt': 'Three questions, one in bold with no check and no heavier edge, and three part boxes, two tinted with '
                   'no words.',
    'fail_label': 'The questions and three parts at 390 px',
}

# ---- Group 2, a page for each record
R['21.4'] = {
    'title': 'Build a reform’s page from its own record, in the order a reader asks.',
    'rule': ['Give each reform a page that answers a reader’s questions in order: what it is and its status, with its '
             'date; where it acts, drawn at its targets; how sure our atlas is that the problem exists and that the '
             'remedy works, as two grades; what it would change in each of the four outcome families, one to a row; how '
             'it could pass, route by route, each with its check date or Not checked; and where its evidence comes from. '
             'When the atlas grades a remedy contested, print both readings at the same length.'],
    'why': 'A reader who asks whether a reform would work gets the evidence for that answer before the routes, and a '
           'contested remedy shows both sides of the dispute, as our atlas records it.',
    'basis': 'Rules 15.11, 15.12, 15.16, 15.20 and 15.24, applied as one page; house rule H08; Concept 10, Who Can Act, '
             'without its strand widths; Concept 03’s Detail A',
    'specs': [('Order', 'Head and status; where it acts; the two grades; the four effects; routes; complements; sources'),
              ('Contested remedy', 'Two readings side by side at 1440 px and one after the other at 390 px, within a '
                                   'line’s length of each other, each with its source a step away'),
              ('Effects', 'Rule 15.16’s rows, codes whole with qualifiers and a true minus; Quality of democracy for DQ'),
              ('Routes', 'Rule 15.24’s rows, with Not checked where the record holds no date'),
              ('Status', '“As of” and the date in words')],
    'builders': ['Read every field from the reform’s own record, and set a contested remedy’s two readings as one '
                 'pair.'],
    'correct_caption': 'Reform R-23’s page at 1440 and 390 px, on Newsprint and in the dark mode.',
    'correct_alt': 'A reform page four times: its head with a status panel, a drawing of its two targets in red, its two '
                   'grades with the contested remedy’s two readings side by side, four effect rows and four routes.',
    'failure_caption': '<strong>Fails Rule 21.4.</strong> The panel keeps the finding of little job loss, drops the budget '
                       'office’s estimate and grades the remedy well supported. Our atlas grades it contested and '
                       'records both.',
    'failure_alt': 'A remedy panel headed Well supported with one reading of little job loss and no second reading.',
    'fail_label': 'The remedy panel at 1440 px',
    'fail_grade': 'Well supported',
}
R['21.5'] = {
    'title': 'Tag reforms that share a target in ink, and keep the red for this one.',
    'rule': ['On a reform’s page, the reform’s own targets turn red. Where other reforms in our atlas aim at the same '
             'variable or connection, tag that mark with each one’s chip and the words aims here, in the text’s '
             'ink. On a loop page, where a reader chooses one reform, the others that aim at the loop take the same ink '
             'tags.'],
    'why': 'A reader learns that several reforms compete for the same lever, and the one red still shows which reform the '
           'page is about (Rule 05.3).',
    'basis': 'ED-F6, from System 4; Rules 05.3 and 12.5; the reforms’ own target lists; the data lead’s R10',
    'specs': [('Tag', 'The reform’s typed chip and “aims here”, in the data label style, in the text’s ink, '
                      '6 px from the mark'),
              ('Several tags', 'Stacked under one leader line; past four, “and [n] more” with a link to the list'),
              ('Red', 'The page’s own reform only; the tags never take red, an outline or a fill')],
    'builders': ['Find every reform that names the same target in its own record, and draw its tag in ink.'],
    'correct_caption': 'Reform R-23’s two targets in red, with the four other reforms that aim at one of them tagged in '
                       'ink, at 1440 and 390 px on Newsprint.',
    'correct_alt': 'Two variables joined by one connection, both outlined in red, and beside the second four ink tags, '
                   'each a reform chip with the words aims here.',
    'failure_caption': '<strong>Fails Rule 21.5.</strong> Five reforms share the red, so the page has five working reds and '
                       'no longer shows which reform it is about.',
    'failure_alt': 'The same two variables with all five reform tags drawn in red.',
    'fail_label': 'The targets at 390 px',
}
R['21.6'] = {
    'title': 'Name every record in its typed chip, and let the chip open the record’s page.',
    'rule': ['Every ID on an atlas page sits in its typed chip, the kind of record in words and its code, such as Loop R18 '
             'or Reform R-23. A chip that names a record with a page of its own links to that page, and the first time a '
             'page names a record, its name follows the chip.'],
    'why': 'Our atlas uses B4 for a variable and for a loop, and R1 sits one hyphen from R-01. The word in the chip says '
           'which record a reader is looking at, and the link takes them to it.',
    'basis': 'Rules 13.9 and 18.24; house rule H11; V7.1 item 12; the model’s IDs',
    'specs': [('Kinds', 'Rule 13.9’s ten words'),
              ('Chip', 'Rule 18.24’s, plain or as a link with a target at least 24 px tall'),
              ('Link', 'To the record’s own page, or for a connection to its Register line; the record’s name as the '
                       'link’s description where the words around it do not name it'),
              ('Check', 'Every chip’s ID exists under its kind in the model (Rule 21.16)')],
    'builders': ['Take each chip’s kind word from where its ID lives in the model, never from its letters.'],
    'correct_caption': 'One chip for each of the ten kinds of record, plain and as a link, then the four pairs of codes our '
                       'atlas repeats, on Newsprint and on Charcoal.',
    'correct_alt': 'Ten typed chips in two rows, plain and underlined, each followed by its record’s name, then four '
                   'pairs such as Variable B4 and Loop B4, on a light ground and on a dark one.',
    'failure_caption': '<strong>Fails Rule 21.6.</strong> Bare codes let a loop pass for a variable: B4 and R1 here are '
                       'loops, filed under Variables.',
    'failure_alt': 'A list headed Variables with three bare codes and names, two of them loops.',
    'fail_label': 'A list of bare codes',
    'fail_head': 'Variables',
    'chips_plain': 'Plain',
    'chips_link': 'As a link',
    'chips_pairs': 'Codes our atlas repeats',
    'on_newsprint': 'On Newsprint',
    'on_charcoal': 'On Charcoal',
}
R['21.7'] = {
    'title': 'Put the evidence one step from every claim.',
    'rule': ['Every claim an atlas page makes links to its evidence in one step. A figure links to the atlas’s claim '
             'record, which gives the claim, its grade, the people and place it covers, its period, its limit and its '
             'source. A connection’s chip links to its line in the Register, with its grade and citation. A '
             'reform’s sources sit in a disclosure on its own page.'],
    'why': 'A reader who doubts a number or a step can check it without leaving the page they are reading, and we never '
           'ask them to trust a claim we cannot show.',
    'basis': 'The architecture map’s instruction for chapter 21; Rules 13.6 and 13.12; the model’s claim and source '
             'records; the data lead’s R5',
    'specs': [('Figure', 'Its claim’s chip right after it, linked; the claim’s record in a disclosure'),
              ('Connection', 'Its chip links to its line on its sheet of the Register'),
              ('Reform', 'Its sources in a disclosure, closed on load, open on paper (Rule 18.8)'),
              ('Steps', 'One link or one disclosure, never a search'),
              ('Source lines', 'Rule 13.6’s six parts as the source record holds them')],
    'builders': ['Give every figure and every connection on a page a link to its own record, and fail the build when one '
                 'has none.'],
    'correct_caption': 'Two one-step paths at 1440 px: the home answer’s figure with its claim record open, and a loop '
                       'step’s chip beside its line in the Register.',
    'correct_alt': 'A short answer with a figure and the chip Claim CL1340, its record open beneath with grade, people, '
                   'place, period and limitation; and the chip Connection L14 beside its row on sheet D04.',
    'failure_caption': '<strong>Fails Rule 21.7.</strong> The figure points to a list of {answer_sources} sources at the foot of the '
                       'page, and a reader cannot tell which one holds it.',
    'failure_alt': 'A short answer with a figure and no chip, and a long numbered list of sources at the foot.',
    'fail_label': 'The answer and its sources at 1440 px',
    'fail_sources': 'Sources',
}

# ---- Group 3, the Register
R['21.8'] = {
    'title': 'Index the Register by sheet, and count each grade in words.',
    'rule': ['Open the Register with one row for each of its twelve sheets, one for each domain and one for each of the two '
             'lower layers, giving the sheet’s variables, connections, loops, reforms and issue records, and then how '
             'many of its connections carry each grade. A last row counts the whole atlas, each loop and reform once.'],
    'why': 'A reader sees where the atlas’s evidence is strong and where it is thin, sheet by sheet, in numbers they can '
           'check line by line.',
    'basis': 'Concept 11, Register; Rule 15.25’s row on Concept 11’s evidence bars; Rule 13.5; the data lead’s '
             'count methods (R2)',
    'specs': [('Rows', 'Domains D01 to D10 with their chips, then the two layers in words (Rule 10.8), then the whole atlas'),
              ('Grade columns', 'Rule 13.3’s five words in its order, each head with its 40 px line sample (Rule 13.4); '
                                'never a shade, width or bar'),
              ('Issue records', '“none filed” for the two layers; the whole row says one is retired'),
              ('Table', 'Rule 18.10’s markup with tabular figures; at 390 px a card per sheet')],
    'builders': ['Count every column from the model by one written method, and print it with the table.'],
    'correct_caption': 'The Register at 1440 and 390 px, on Newsprint and in the dark mode, with its index and sheet D04 open.',
    'correct_alt': 'The Register four times: an index table of twelve sheets with counts and five grade columns, then sheet '
                   'D04 with its three variables, ten connection rows, its rejected option and its filtered issue records.',
    'failure_caption': '<strong>Fails Rule 21.8.</strong> Shading ranks the grades and hides the counts, so a reader cannot '
                       'tell how many connections on a sheet are a hypothesis.',
    'failure_alt': 'An index with one bar for each sheet, shaded from dark to light, and no numbers.',
    'fail_label': 'The index’s grade column, as Concept 11 drew it',
}
R['21.9'] = {
    'title': 'File each connection once, on the sheet of the variable it moves.',
    'rule': ['On each sheet, list every connection that moves one of the sheet’s variables, once, with its chip, the '
             'variables it joins, its sign as a tag and a word, its type, its delay, its grade as a line and a word, and the '
             'atlas’s citation. Give each line an address of its own, so a chip anywhere in the atlas can link to it.'],
    'why': 'Filed once, every connection has one home a reader can find, and the sheets add up to the atlas’s '
           '{connections}.',
    'basis': 'Concept 11; Rules 13.4, 13.5, 15.3 to 15.5; the filing method (the data lead’s R2)',
    'specs': [('Filing', 'By the variable the connection moves; a variable in the economy or technology layer files on that '
                         'layer’s sheet; a variable with two domains files on the first'),
              ('Columns', 'Chip; from and to by title with chips; sign tag and raises or lowers; type in words; delay ticks '
                          'and words; grade line and word; citation as stored'),
              ('Authority', 'Decides and the open diamond, no sign (Rule 15.5)'),
              ('Address', 'Each line’s id, register- and the connection’s ID')],
    'builders': ['File each connection by its variable’s sheet and stop the build when the sheets do not sum to the '
                 'model’s count.'],
    'correct_caption': 'Sheet D10, taking part, trust and shared norms: its connections at 1440 px on Newsprint, two of them '
                       'contested.',
    'correct_alt': 'A table of connection rows, each with its chip, its two variables, a sign tag, type, delay ticks, a '
                   'grade line and word and a citation; two rows carry the dash and dot of Contested.',
    'failure_caption': '<strong>Fails Rule 21.9.</strong> Every connection appears on two sheets, so the Register counts '
                       '{double} where our atlas holds {connections}.',
    'failure_alt': 'The whole-atlas row of the index reading twice the atlas’s count of connections.',
    'fail_label': 'The whole-atlas row, filed twice',
}
R['21.10'] = {
    'title': 'Keep the rejected option and the connections left off the map on their sheets.',
    'rule': ['Where our atlas rejects a reform, keep it on the sheets its targets file on, under the label Rejected option, '
             'with its grade read as the atlas reads it: for a rejected option, a strong grade measures confidence in harm. '
             'Where the atlas reviewed a connection and did not draw it, list it on its sheet under Reviewed and not drawn, '
             'with its two variables and the atlas’s reason, and draw no line.'],
    'why': 'What the atlas decided against is evidence too, and a reader who meets a popular idea there sees the finding '
           'behind the decision.',
    'basis': 'Rule 15.10; the model’s rejected flag and its reviewed connections; Concept 11, which keeps the rejected '
             'option in the evidence view',
    'specs': [('Label', '“Rejected option” as the block’s heading, the reform’s title as stored'),
              ('Grade', 'The atlas’s words quoted under the grade word'),
              ('Reviewed and not drawn', 'Rule 15.10’s form, from and to with chips, the reason quoted, no line in any '
                                         'pattern'),
              ('Counts', 'Rejected reforms stay out of the index’s reforms column')],
    'builders': ['Read the rejected flag and the reviewed connections from the model, and file each on its targets’ '
                 'sheets.'],
    'correct_caption': 'Sheet D04’s rejected option and sheet D10’s connections reviewed and not drawn, at 390 px on '
                       'Newsprint.',
    'correct_alt': 'A block headed Rejected option with Reform R-35, its two effects and a quoted line on what its grade '
                   'measures; then a block headed Reviewed and not drawn with two connections and their reasons, and no '
                   'lines.',
    'failure_caption': '<strong>Fails Rule 21.10.</strong> Term limits read as a well supported remedy, though our atlas '
                       'rejects them on strong evidence of harm.',
    'failure_alt': 'A list of reforms in which Reform R-35 sits with no label and the words Well supported.',
    'fail_label': 'Sheet D04’s reforms at 390 px',
}
R['21.11'] = {
    'title': 'Filter a sheet’s issue records by variable, and say how many show.',
    'rule': ['Under each sheet’s connections, list its issue records with their grades. Let a reader narrow the list to the '
             'records that name one of the sheet’s variables, with one Filters button that says how many filters are '
             'on, and a line that says how many records show out of how many.'],
    'why': 'A sheet can hold twenty or more records, and a reader who cares about one variable finds its records without '
           'reading all of them.',
    'basis': 'ED-F4; Rule 18.16; the issue records’ own variable lists',
    'specs': [('Control', 'Rule 18.16’s Filters button with the count of filters on, and one check box per variable, '
                          'each with its chip and its count of records'),
              ('Count line', 'A status line on each change, never on load (Rule 18.15)'),
              ('Each record', 'Chip, title as stored, grade word'),
              ('No variable', 'Records that name none of the sheet’s variables show only with every filter off')],
    'builders': ['Build the filters from the variables on the sheet and count each from the records’ own variable lists.'],
    'correct_caption': 'Sheet D04’s issue records with one filter on, at 390 px on Newsprint and in the dark mode.',
    'correct_alt': 'A Filters button reading one on, a line giving how many of the sheet’s records show, and the records '
                   'as rows, each with its chip, title and grade word.',
    'failure_caption': '<strong>Fails Rule 21.11.</strong> Color alone shows which filter is on, nothing says how many records '
                       'are hidden, and the grades are gone.',
    'failure_alt': 'Three tabs, one filled, over a list of record titles with no count and no grades.',
    'fail_label': 'The filtered list at 390 px',
}

# ---- Group 4, loop pages
R['21.12'] = {
    'title': 'Head a loop page with its grade line and the arithmetic of its signs.',
    'rule': ['Open a loop page with the loop’s chip, its kind and its title from our atlas in quotation marks, and under '
             'the title the grade of each step from the atlas’s own words. Read the loop aloud in one sentence that '
             'starts with more of its first variable and turns at each minus sign, and say beside it that an even count '
             'of minus signs makes a loop that feeds itself. On the drawing, name the weakest step and say that the loop '
             'holds only as firmly as that step.'],
    'why': 'The arithmetic lets a reader check the loop’s kind from its signs, and naming the weakest step keeps the '
           'loop’s title from claiming more than its least certain link.',
    'basis': 'ED-F4 and ED-F6, from Systems 3 and 4; Rules 15.6, 15.7, 15.13 and 18.22; the model’s loop record; the '
             'data lead’s R4 and R8',
    'specs': [('Head', 'Chip, kind word, title in quotation marks as the h1, grade line in display words with chips'),
              ('Read aloud', 'One sentence from the signs, built by chapter 15’s read-aloud; the arithmetic line beside it'),
              ('Weakest step', 'Weakest step under its words where the atlas’s evidence summary names it (Rule 15.13), '
                               'with the line on how firmly the loop holds'),
              ('Closure and delay', 'In the atlas’s words (Rule 15.7)')],
    'builders': ['Build the read-aloud line from the signs, and stop the build when the loop’s kind and its count of '
                 'minus signs disagree.'],
    'correct_caption': 'Loop R18’s page at 1440 and 390 px, on Newsprint and in the dark mode, with Reform R-11 chosen.',
    'correct_alt': 'A loop page four times: its head with a facts panel, the loop read aloud beside its two-step drawing '
                   'with the weakest step named, the stepper, the reform chooser and the chosen reform’s effects and '
                   'routes.',
    'failure_caption': '<strong>Fails Rule 21.12.</strong> The head grades Loop R18 documented, the grade of its first step. '
                       'Our atlas grades the return step plausible, and the loop holds only as firmly as that step.',
    'failure_alt': 'A loop page’s head with the word Documented beside the title and no reading of its signs.',
    'fail_label': 'The head at 1440 px',
}
R['21.13'] = {
    'title': 'Run the atlas’s stepper in the guide’s order and at the guide’s pace.',
    'rule': ['Every loop page steps through its loop with the guide’s loop stepper: Play, Reset the loop, Previous step '
             'and Next step, in that order, on every screen. Play holds each step about a quarter of a second for every '
             'word the status line reads, and never less than six seconds. Nothing plays until a reader presses Play.'],
    'why': 'A reader who learns the stepper anywhere in our work finds the same buttons in the same place here, and the '
           'pace lets a reader, or a screen reader, finish each step before the next.',
    'basis': 'Rule 18.22; D2-1154; the accessibility lead’s AL-22 and AL-24; registers F-8 and F-15',
    'specs': [('Order and names', 'Play, Reset the loop, Previous step, Next step'),
              ('Phone', 'A two-by-two grid: Play and Reset the loop, then Previous step and Next step'),
              ('Hold', '250 ms a word of everything the status line reads, the step’s number included, never under '
                       '6,000 ms, with reduced motion too; computed by script from the status lines'),
              ('Code', 'Chapter 18’s loop stepper, read from its files')],
    'builders': ['Read the stepper from chapter 18’s files, and time each hold from its status line’s words.'],
    'correct_caption': 'Loop R18’s stepper on step 2, at 390 px on Newsprint in a two-by-two grid and at 1440 px in the '
                       'dark mode in one row.',
    'correct_alt': 'Two steppers, each with a status line on step 2 of 2 and four buttons: Play, Reset the loop, Previous '
                   'step and Next step, in a grid on the phone and in a row on the desktop.',
    'failure_caption': '<strong>Fails Rule 21.13.</strong> The buttons run in another order than the rest of our work, and '
                       'each step moves on after about three seconds, before a reader can finish it.',
    'failure_alt': 'A stepper with Play, Previous step, Next step and Reset, and a note of 3,200 ms a step.',
    'fail_label': 'The stepper as the atlas runs it today',
    'fail_buttons': ['Play', 'Previous step', 'Next step', 'Reset'],
    'fail_hold': '3,200 ms a step',
}
R['21.14'] = {
    'title': 'List every loop on one index, by kind, closure and grade.',
    'rule': ['Give the atlas one index of its loops: the reinforcing ones and then the balancing ones, each with its chip, '
             'its title, its number of steps, its count of minus signs, how it closes in the atlas’s words and its '
             'grade in the atlas’s words. Order each group as the atlas lists it. Leave out any score or rank of '
             'strength.'],
    'why': 'A reader can find a loop by its kind and see at a glance which loops rest on a hypothesis or close only in '
           'concept.',
    'basis': 'ED-F4, System 3’s loop index; Rules 15.6, 15.7, 15.18, 15.21; the model’s loops; DR-321',
    'specs': [('Groups', 'Reinforcing, then Balancing, each in the atlas’s order'),
              ('Row', 'Chip, title as stored, steps, minus signs, closure and grade as stored, each a link to the '
                      'loop’s page'),
              ('Conceptual loops', '“no numbered chain” with their grade (Rule 15.18)'),
              ('Titles', 'As the atlas stores them, with a note that its next version reviews titles that state an effect '
                         '(DR-321)'),
              ('Never', 'A strength, a score, or a size for a loop (Rule 15.21)')],
    'builders': ['Read every row from the loop’s own record, in the atlas’s order.'],
    'correct_caption': 'The index of all {loops} loops, at 1440 and 390 px on Newsprint.',
    'correct_alt': 'A table of loops in two groups, reinforcing and balancing, each row with its chip, title, steps, minus '
                   'signs, closure and grade.',
    'failure_caption': '<strong>Fails Rule 21.14.</strong> A bar ranks each loop by a strength our atlas does not measure.',
    'failure_alt': 'A list of loops each with a horizontal bar of a different length.',
    'fail_label': 'A ranked index',
}

# ---- Group 5, the dark mode and the atlas test
R['21.15'] = {
    'title': 'Draw the atlas’s dark mode from the Charcoal tokens, and measure every mark.',
    'rule': ['In the dark mode, every atlas page draws on Charcoal from the tokens set for Charcoal: text in Newsprint, '
             'quieter words and muted marks in Dim Newsprint, the selected bar in Newsprint and the red target in Pillar '
             'Red. Line patterns, sign tags, ticks and chips keep their shapes. Measure every mark on the page’s own '
             'pixels before it ships.'],
    'why': 'A reader who sets their device to dark reads the same atlas with the same marks, and every mark keeps the '
           'contrast it needs on Charcoal.',
    'basis': 'DR-36 and DR-204; ED-F2; register F-14 and the accessibility lead’s AL-23; ratios measured on the '
             'plate’s pixels by the kit',
    'specs': [('Ground', 'Charcoal'),
              ('Text', 'Newsprint; secondary words in Dim Newsprint'),
              ('Marks', 'Essential in Newsprint; muted in Dim Newsprint, never Stone'),
              ('Selected bar', 'Newsprint, never White'),
              ('Red target', 'Pillar Red on Charcoal, with no edge'),
              ('Hairlines that carry no meaning', 'Stone'),
              ('Every color', 'From a token, never a hex in the renderer; checked on the frame’s pixels'),
              ('Switch', 'The site’s, remembered across a reload')],
    'builders': ['Name a token for every color in a dark view, and check each frame’s pixels with the contrast script.'],
    'correct_caption': 'Loop R18’s drawing with Reform R-11’s targets in red and the chooser beside it, at 1440 px in '
                       'the dark mode, with the ratios measured on the plate’s pixels.',
    'correct_alt': 'A dark loop drawing with one connection and one variable outlined in red, a chooser of three reforms, '
                   'and a table of measured contrast ratios.',
    'failure_caption': '<strong>Fails Rule 21.15.</strong> Muted marks in Stone clear 3 to 1 by a tenth, and the selection '
                       'draws in White, a color no token sets on Charcoal.',
    'failure_alt': 'A dark drawing with gray muted marks and a white selection bar.',
    'fail_label': 'The drawing in the colors of today’s dark kit',
    'ratio_head': ['Mark', 'Token', 'Measured'],
    'ratio_rows': {'text': 'Text', 'secondary': 'Secondary words and muted marks', 'red': 'The red target',
                   'hairline': 'A hairline that carries no meaning'},
    'ratio_value': '{r} to 1',
}
R['21.16'] = {
    'title': 'Test every atlas page against the model before it ships.',
    'rule': ['Before any atlas page ships, run the atlas test. It reads the page and the model together and checks every '
             'ID, sign, type, delay, grade, count and date the page prints against the model, every red mark against the '
             'chosen reform’s targets, every effect against its family, every link from a claim to its evidence, and '
             'the stepper’s order and pace. A single failure stops the page.'],
    'why': 'The atlas changes as its evidence changes, and a page that copies a value can drift from the record without '
           'anyone seeing. The test reads the record each time.',
    'basis': 'Master Brief section 14 and the architecture map; chapter 15’s generator checks, extended to pages',
    'specs': [('Checks', 'Sixteen, one line a check and page, each with its pass condition'),
              ('Output', 'PASS or FAIL, with the page, the record and both values'),
              ('Stop', 'Any FAIL stops the kit’s build and the strict guide build'),
              ('Self-test', 'Planted faults, one a check, each caught by its own check')],
    'builders': ['Run the atlas test on every build, and treat a failure as a stop.'],
    'correct_caption': 'The atlas test’s report for the four views, one line a check, from the build’s own run.',
    'correct_alt': 'A list of check lines, each beginning PASS, with the check, the page and what it read.',
    'failure_caption': '<strong>Fails Rule 21.16.</strong> The page grades Connection L15 documented. Our atlas grades it '
                       'plausible, and the test stops the page.',
    'failure_alt': 'A loop step labeled Documented beside a test line beginning FAIL that names the page, the connection, '
                   'the printed grade and the model’s grade.',
    'fail_label': 'The page and the test’s line',
    'fail_line': 'FAIL T2 A14 1440-light Connection L15: printed {printed}, model {model}',
    'report_label': 'The atlas test, from the build’s last run',
}

EXTRA_HOW = {
    'label': 'How to read our atlas',
    'caption': 'Our atlas’s How to read page, which lists every mark its pages use with the rule that sets it, at 1440 '
               'px on Newsprint and at 390 px in the dark mode.',
    'alt': 'A page listing the atlas’s marks, each with a small drawing, its words and the rule that sets it: sign '
           'tags, type words, the open diamond, five grade lines, delay ticks, the record square, the hollow line, the red '
           'target, the typed chip and the pressed question.',
}

# the line above each row of frames: the width, the theme and the state each frame shows, composed from a view's key
# (the engineer's C9: <width>-<theme>, then "screen", "open" or a part's name); joined by commas, rows by middle dots
VIEW_WORDS = {
    'px': '{w} px', 'light': 'light', 'dark': 'dark', 'screen': 'first screen', 'open': 'views open',
    'parts': {'top': 'the top of the page', 'drawing': 'the drawing', 'questions': 'the questions', 'answer': 'the answer',
              'targets': 'where it acts', 'grades': 'the two grades', 'effects': 'the effects', 'routes': 'the routes',
              'index': 'the index', 'sheet': 'the open sheet', 'records': 'the issue records',
              'rejected': 'the rejected option', 'stepper': 'the stepper', 'chooser': 'the chooser',
              'read': 'the loop read aloud', 'evidence': 'the evidence', 'claim': 'the claim’s record'},
}

WCAG = {
    '21.1': ['1.3.1', '2.4.1', '2.4.2', '2.4.3', '3.2.3', '3.2.6', '4.1.2'],
    '21.2': ['1.1.1', '1.3.1', '1.4.10', '1.4.11', '4.1.2'],
    '21.3': ['1.4.1', '4.1.2', '4.1.3'],
    '21.4': ['1.3.1', '1.4.1', '2.4.6'],
    '21.5': ['1.4.1', '2.4.4'],
    '21.6': ['1.3.1', '2.4.4', '2.5.8'],
    '21.7': ['2.4.4', '1.3.1'],
    '21.8': ['1.3.1', '1.4.1', '1.4.10'],
    '21.9': ['1.3.1', '1.4.1'],
    '21.10': ['1.3.1'],
    '21.11': ['1.3.1', '2.1.1', '4.1.2', '4.1.3'],
    '21.12': ['1.1.1', '1.3.1', '2.4.6'],
    '21.13': ['2.1.1', '2.2.2', '2.4.3', '3.2.4', '4.1.3', '2.3.3 (AAA, the guide’s own pace)'],
    '21.14': ['1.3.1'],
    '21.15': ['1.4.3', '1.4.11'],
}
TOKENS = {
    '21.1': ['oa.type.label', 'oa.type.caption', 'oa.type.ui', 'oa.type.bodySmall', 'oa.color.surface.charcoal',
             'oa.border.width.rule', 'oa.color.border.hairline.onNewsprint', 'oa.size.target.touch'],
    '21.2': ['oa.color.graphic.essential.onNewsprint', 'oa.color.graphic.subtle.onNewsprint', 'oa.type.dataLabel',
             'oa.type.label', 'oa.border.width.hairline'],
    '21.3': ['oa.color.border.strong.onNewsprint', 'oa.border.width.rule', 'oa.size.icon.medium',
             'oa.color.state.muted.mark.onNewsprint', 'oa.color.state.muted.text.onNewsprint'],
    '21.4': ['oa.color.data.emphasisRed.onNewsprint', 'oa.color.graphic.essential.onNewsprint', 'oa.type.dataLabel',
             'oa.type.section'],
    '21.5': ['oa.type.dataLabel', 'oa.color.text.primary.onNewsprint', 'oa.color.data.emphasisRed.onNewsprint'],
    '21.6': ['oa.type.dataLabel', 'oa.color.border.strong.onNewsprint', 'oa.size.target.minimum'],
    '21.7': ['oa.type.caption', 'oa.type.dataLabel', 'oa.border.width.underline'],
    '21.8': ['oa.type.dataLabel', 'oa.chart.grade.documented', 'oa.chart.grade.plausible', 'oa.chart.grade.contested',
             'oa.chart.grade.hypothesis'],
    '21.9': ['oa.type.dataLabel', 'oa.color.graphic.essential.onNewsprint'],
    '21.10': ['oa.type.label', 'oa.type.bodySmall', 'oa.color.border.hairline.onNewsprint'],
    '21.11': ['oa.size.target.touch', 'oa.type.ui', 'oa.type.dataLabel'],
    '21.12': ['oa.type.section', 'oa.type.intro', 'oa.chart.grade.documented', 'oa.chart.grade.plausible'],
    '21.13': ['oa.size.target.touch', 'oa.size.icon.medium', 'oa.color.state.selected.bar.onNewsprint',
              'oa.border.width.bar'],
    '21.14': ['oa.type.dataLabel', 'oa.type.bodySmall'],
    '21.15': ['oa.color.surface.charcoal', 'oa.color.text.primary.onCharcoal', 'oa.color.text.secondary.onCharcoal',
              'oa.color.state.muted.mark.onCharcoal', 'oa.color.state.selected.bar.onCharcoal',
              'oa.color.data.emphasisRed.onCharcoal'],
    '21.16': ['oa.type.dataLabel', 'oa.type.bodySmall'],
}
RELATED = {
    '21.1': (['12', '17', '18', '20'], ['12.7', '17.10', '18.5', '18.6', '18.7', '18.8', '20.1', '20.3']),
    '21.2': (['07', '12', '15', '18'], ['07.2', '12.7', '15.1', '15.2', '15.9', '18.2']),
    '21.3': (['05', '17', '18'], ['05.4', '17.8', '17.10', '18.2', '21.7']),
    '21.4': (['13', '15', '18'], ['13.3', '13.5', '13.10', '15.11', '15.12', '15.16', '15.20', '15.24', '18.8']),
    '21.5': (['05', '12', '15'], ['05.3', '12.5', '12.6', '15.11', '15.20']),
    '21.6': (['13', '18'], ['13.9', '18.5', '18.24']),
    '21.7': (['13', '14', '18'], ['13.6', '13.9', '14.13', '18.5', '18.8', '21.9']),
    '21.8': (['10', '13', '14', '18'], ['10.8', '13.3', '13.4', '13.5', '14.13', '18.10']),
    '21.9': (['13', '15', '18'], ['13.4', '13.5', '15.3', '15.4', '15.5', '18.10', '21.7']),
    '21.10': (['13', '15'], ['13.3', '15.10', '15.12']),
    '21.11': (['18'], ['18.15', '18.16', '18.19']),
    '21.12': (['13', '15', '18'], ['13.2', '15.3', '15.6', '15.7', '15.13', '18.22']),
    '21.13': (['11', '15', '17', '18'], ['11.16', '15.19', '17.3', '17.4', '18.22']),
    '21.14': (['15', '18'], ['15.6', '15.7', '15.18', '15.21', '18.10']),
    '21.15': (['05', '17', '18'], ['05.2', '05.5', '17.10', '18.4']),
    '21.16': (['13', '15', '19', '28'], ['13.9', '15.6', '15.11', '15.16', '19.7', '19.8']),
}


# ================================================================================================ WORDS FOR THE KIT
APPS = ('A11', 'A12', 'A13', 'A14', 'A15', 'A16')


def _fill(s):
    return s.format(**{k: (f'{v:,}' if isinstance(v, int) else v) for k, v in FACT.items() if not isinstance(v, list)})


def page_words(aid):
    """One atlas page's words for the kit (the engineer's C9 handshake): its whole title, the shared words, its current
    view, its breadcrumb and its template's own words. Templates in braces stay for the kit to fill from the model, except
    the chapter's own counts in an intro, which this file fills."""
    if aid == 'all':
        return {k: page_words(k) for k in APPS}
    if aid not in PAGES:
        raise SystemExit(f'no atlas page {aid}; use {", ".join(APPS)} or all')
    p = PAGES[aid]
    page = dict(p['page'])
    if 'intro' in page:
        page['intro'] = _fill(page['intro'])
    if aid == 'A14':
        page['steps'] = [{'line': s['line'], 'hold': s['hold']} for s in page['steps']]
    return {
        'title': f'{p["view"]} | {META["title"]} | {ATLAS["title_end"]}',
        'atlas': {k: v for k, v in ATLAS.items() if k != 'title_end'},
        'current_view': p['current_view'],
        'crumbs': p['crumbs'],
        'page': page,
    }


def check_words():
    """Every word the pages print passes chapter 02's mechanical checks, as the specimens' words do."""
    def walk(x, where):
        if isinstance(x, str):
            if not x.startswith(('/', 'http', '--oa-')):
                C.check_copy(x, where)
        elif isinstance(x, dict):
            for k, v in x.items():
                walk(v, f'{where}.{k}')
        elif isinstance(x, (list, tuple)):
            for i, v in enumerate(x):
                walk(v, f'{where}[{i}]')
    walk(ATLAS, 'ATLAS')
    walk(PAGES, 'PAGES')
    views = [v for v, _ in ATLAS['views']]
    for aid, p in PAGES.items():
        if p['current_view'] not in views:
            raise SystemExit(f'{aid}: current view {p["current_view"]!r} is not one of the atlas’s views')


# ================================================================================================ LAYOUT
def ty(name):
    return ctx.ty(name)


class Waiting(Exception):
    """A plate that needs the kit's drawing or report before it can be written."""


# The plates come with hand-over 4 (specs section 11); until then the chapter waits.
PLATES = []


def spec(sid, html, rule, alt, **kw):
    kw.setdefault('readable', True)
    ctx.spec(sid, html, CH, rule, alt, **kw)
    return sid


def app(aid, views=None):
    """The kit's placeholder (contract C4). The guide build sets the kit's frames in its place."""
    v = f' data-oa-app-views="{views}"' if views else ''
    return f'<div data-oa-app="{aid}"{v}></div>'


# ------------------------------------------------------------------------------------------------ the chapter
def build_chapter():
    waiting = []
    for f in PLATES:
        try:
            f()
        except Waiting as e:
            waiting.append(str(e))
    if not PLATES:
        waiting.append('the plates (specs section 11, hand-over 4)')
    rules = []
    for rid in sorted(R, key=lambda k: int(k.split('.')[1])):
        r = R[rid]
        n = rid.split('.')[1]
        correct = {'21.4': 's-21-reform', '21.6': 's-21-chips', '21.8': 's-21-register', '21.12': 's-21-loop'}.get(
            rid, f's-21-{n}-correct')
        specs = [{'label': a, 'value': _fill(b)} for a, b in r['specs']]
        if WCAG.get(rid):
            specs.append({'label': 'WCAG 2.2', 'value': ', '.join(WCAG[rid])})
        rel, rr = RELATED[rid]
        rules.append({
            'id': rid, 'title': r['title'], 'rule': [_fill(x) for x in r['rule']], 'tokens': TOKENS[rid],
            'why': {'text': [_fill(r['why'])], 'basis': r['basis']},
            'correct': {'specimen': correct, 'caption': _fill(r['correct_caption'])},
            'failure': {'specimen': f's-21-{n}-failure', 'caption': _fill(r['failure_caption'])},
            'specs': specs, 'related': rel, 'related_rules': rr, 'builders': r['builders'],
        })
    ch = {
        'number': CH, 'anchor': 'atlas', 'title': W['title'], 'part': 'applications', 'opener': 's-21-home',
        'instruction': W['instruction'], 'intro': [_fill(x) for x in W['intro']],
        'groups': [{'before_rule': b, 'number': i, 'title': t, 'line': l} for i, (b, t, l) in enumerate(W['groups'], 1)],
        'rules': rules,
        'extras': [{'after_rule': '21.14', 'specimen': 's-21-how-to-read', 'label': EXTRA_HOW['label'],
                    'caption': EXTRA_HOW['caption']}],
        'related_chapters': [{'chapter': c, 'reason': t} for c, t in W['related_chapters']],
        'sources': [_fill(s) for s in W['sources']],
    }
    return ch, waiting


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build in memory and report; write nothing')
    ap.add_argument('--page-words', metavar='ID', help='print one atlas page’s words as JSON (A11 to A16, or all)')
    a = ap.parse_args()
    if a.page_words:
        check_words()
        print(json.dumps(page_words(a.page_words), ensure_ascii=False, indent=1))
        return
    check_words()
    ch, waiting = build_chapter()
    B.check_chapter(ch)
    for w in waiting:
        print(f'  waiting: {w}')
    total = sum(len(s['html'].encode()) for s in ctx.specs.values())
    print(f'chapter 21: {len(ch["rules"])} rules, {len(ctx.specs)} specimens ({total:,} bytes before the kit’s frames); '
          f'model {MODEL_SHA[:16]}')
    if a.check:
        return
    if waiting:
        raise SystemExit('not written: plates wait for the kit or for hand-over 4')


if __name__ == '__main__':
    main()
