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
        'Our systems atlas, Who Do They Answer To?, lives inside our website, under the site’s masthead, with a title '
        'bar of its own. Its home page draws the whole system and starts from a question a reader brings. Each proposed '
        'change the atlas weighs, a reform, has a page, and so does each loop, a chain of causes that returns to where it '
        'started. The Register files every one of the atlas’s {connections} connections once, with its evidence. A '
        'connection is an arrow from one variable, a quantity or condition that can rise or fall, to another. An index '
        'lists the loops, and a page called How to read explains every mark. The plates follow four views chosen in '
        'turn across subjects, as chapter 01 rotates examples (Rules 01.9 to 01.12): a question about medical bills, '
        'Reform R-23 on the minimum wage, the Register’s sheet on Congress and the agencies, and Loop R18 on presidential '
        'power over watchdogs, each with a finding from the record that one side of a debate may want to skip.',
        'Chapter 15 sets how each mechanism is drawn, and these pages use its rules as they stand. This chapter covers '
        'what a page adds around the drawing. A page names every ID in a typed chip, the label that gives the kind of '
        'record with its code, and links every claim to the record that grades its evidence, on Rule 13.3’s scale from '
        'documented to hypothesis. Before a page ships, the atlas test checks each value it prints against the atlas’s '
        'own data.'],
    'groups': [
        ('21.1', 'The atlas in our website',
         'Every atlas page sits under the site’s masthead with the atlas’s own title bar, and the home page draws the '
         'whole system and answers a reader’s question.'),
        ('21.4', 'A page for each record',
         'A reform’s page answers a reader’s questions in order from its own record, and every chip and figure on it '
         'opens the record behind it.'),
        ('21.8', 'The Register',
         'The Register files each connection once, with its sign, grade and source, on the sheet for one of the atlas’s '
         'subject areas, and keeps what the atlas rejected in view.'),
        ('21.12', 'Loop pages',
         'A loop page reads the loop’s signs aloud and names its weakest step, and its stepper moves at a pace a reader '
         'can follow.'),
        ('21.15', 'The dark theme and the atlas test',
         'The atlas keeps every mark on Charcoal, and each page passes one test against the atlas’s data before it '
         'ships.'),
    ],
    'opener_caption': 'Our systems atlas’s home page inside our website, at 1440 and 390 px in the light and the dark '
                      'theme. A reader has pressed a question about medical bills, and the drawing keeps the parts it '
                      'reaches at full strength.',
    'opener_alt': 'Four frames of the atlas’s home page, at 1440 px and 390 px, each in the light and the dark theme. '
                  'Under the site’s masthead and the atlas’s Charcoal title bar, the atlas’s eight parts sit as boxes with '
                  'a count on each arrow between them on the desktop, and as a stacked list on the phone. A question '
                  'about medical bills is pressed, and the parts it reaches stay in full ink while the others are muted.',
    'related_chapters': [
        ('05', 'One working red a view, and each section’s opening screen measured as Rule 05.1 sets.'),
        ('10', 'The atlas’s parts named in words, with no icon (Rule 10.8).'),
        ('12', 'The red target and the locator (Rules 12.5 and 12.7).'),
        ('13', 'Grade words and lines, delay ticks, typed chips, dates and source lines.'),
        ('15', 'Every mechanism these pages draw.'),
        ('17', 'The pressed, muted and current looks, and the stepper’s motion.'),
        ('18', 'The chip, stepper, chooser, filters, toggle, disclosure and table.'),
        ('19', 'The accessibility map these pages add to.'),
        ('20', 'The masthead, menu, footer and theme switch the atlas sits in.'),
        ('28', 'The atlas test’s lines on the standards checklist.'),
    ],
    'sources': [
        'Source: Oath & Action, Who Do They Answer To?, our systems atlas, snapshot of {snapshot}, read from its data '
        'file at each build. Behind every value on the atlas’s pages.',
        'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, '
        'retrieved November 21, 2026. Behind Rules 21.1, 21.3, 21.11 and 21.13.',
        'Source: our studio’s earlier drawings of the atlas, October 21 and November 5, 2026, which these pages finish; '
        'they stand as drawings and support no claim (Rule 15.25).',
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
    'locator_alt': 'Atlas home. This page sits in {part}.',
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
    # Rule 15.4's words for a connection's type, for the Register's Type column
    'types': {'causal': 'Causal', 'money': 'Money', 'information': 'Information', 'ownership': 'Ownership',
              'authority': 'Authority'},
    'as_of': 'As of {date}',
    # a route's feasibility in Rule 15.16's form, by the atlas's stored word (batch 1, item 10)
    'feasibility': {'high': 'High feasibility', 'medium': 'Medium feasibility', 'low': 'Low feasibility',
                    'very low': 'Very low feasibility'},
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
            'intro': 'Our systems atlas holds {variables} variables, the quantities and conditions that can rise or fall, '
                     'and {connections} connections between them. It traces {loops} loops, weighs {reforms} reforms and '
                     'files {issues} issue records. Start from the drawing of the whole system, or from a question you '
                     'bring.',
            'switch': 'Show every variable',
            # AX-3: the name of each part's nested list of variables, which the switch opens for every reader
            'variables_list': 'Variables in {part}',
            'key_main': 'The main circuit, part to part.',
            'key_other': 'Other arrows between parts.',
            # editor: the key's third phrase in the specs (12.1); the kit reads it once it draws the home page
            'key_counts': 'Each number counts connections.',
            # the box's two counts print in one line, variables first, so a comma sets them apart (batch 1, item 5)
            'inside': '{n} connections inside',
            'inside_none': 'no connections inside',
            'variables': '{n} variables,',
            'flow_line': '{n} to {part}',
            # R24 (RP4): the label on each box's and card's second line, {title} our atlas's own title for the part,
            # read from the model; the plain name above it stays the part's name
            'part_title': 'In our atlas: {title}',
            'questions_heading': 'Start from a question',
            # the Questions section band's lede (specs 14.1)
            'questions_lede': 'Press a question to see which parts of the system decide it.',
            'lit': 'The question you pressed reaches here',
            'status': 'This question reaches {parts}.',
            'answer_label': 'The short answer',
            # AX-4 and CD-M2: the heading over the pressed question's own short answer, {question} as stored; and the
            # words the answer area shows for a question whose record stores no short answer
            'answer_heading': 'The short answer: {question}',
            'answer_none': 'Our atlas stores no short answer to this question. The parts lit above hold the variables its '
                           'record names.',
            # the claim's disclosure: its summary after the claim's chip, and its record's row labels (R5)
            'claim_summary': 'in full',
            'claim_labels': {'grade': 'Grade', 'population': 'People', 'jurisdiction': 'Place', 'period': 'Period',
                             'limitation': 'Limit', 'sources': 'Sources'},
            'drawing_label': 'The parts of the system and the connections between them',
        },
    },
    'A12': {
        'view': 'Reform R-23, {title}',            # {title}: the kit fills the record's title from the model
        'current_view': 'Reforms',
        'crumbs': [['Home', '/atlas'], ['Reforms', '/atlas/reforms']],
        'page': {
            'status_label': 'Where it stands',
            # Rule 15.12's own labels, in the status panel and over the two grades alike
            'problem': 'Evidence of the problem',
            'remedy': 'Evidence for the remedy',
            'where_heading': 'Where it acts',
            'where_note': '{reform} acts where the marks turn red: on {targets}.',
            # batch 1, item 8: the connection the drawing draws in ink between the targets, with its marks in words;
            # {conn} its linked chip, {name} its stored name, {sign} ATLAS['signs'], {delay} ATLAS['delays'],
            # {grade} the display word (the record square before Documented)
            'conn_note': '{conn} “{name}” joins them: {sign}, {delay}, {grade}. It keeps the drawing’s usual color, since '
                         'the reform does not act on it.',
            'touches': 'Its record names {loop} as a loop it touches. That loop’s steps hold none of the reform’s '
                       'targets, so the drawing leaves it out.',
            'aims_here': 'also aim here',
            'aims_here_one': 'also aims here',
            'grades_heading': 'How sure our atlas is',
            # the Grades section band's lede (specs 14.1)
            'grades_lede': 'Our atlas grades the evidence that the problem exists and the evidence that the remedy '
                           'works, each on its own.',
            'source_link': 'Its source',
            'effects_heading': 'What it would change',
            'effects_confidence': 'Our atlas’s confidence in these effects: “{text}”',
            # R23 (RP1): Rule 01.16’s matching labels over the contested remedy’s two blocks, in the same type
            'reading_one': 'One reading',
            'reading_other': 'The other reading',
            # CE8: a target's sentence on a higher value after its chip; {var} the chip, {means} the stored sentence
            'means_line': '{var}: {means}',
            'routes_heading': 'How it could pass',
            'routes_head': ['Route', 'Who acts', 'Feasibility', 'Note', 'Checked'],
            'complements_heading': 'Works alongside',
            'sources_summary': 'Sources for this page',
        },
    },
    'A13': {
        'view': 'The Register',
        'current_view': 'The Register',
        'crumbs': [['Home', '/atlas']],
        'page': {
            'h1': 'The Register',
            'intro': 'Our atlas lists every connection once, with its sign, its grade and its citation, on the sheet for '
                     'the subject area of the variable it moves. Each sheet counts its records and grades, so a reader can '
                     'check every number here line by line.',
            'index_heading': 'The sheets',
            'index_head': ['Sheet', 'Variables', 'Connections', 'Numbered loops', 'Reforms', 'Issue records'],
            'none_filed': 'none filed',
            'whole': 'The whole atlas',
            # editor: "one" is the count of retired issue records today (Issue I128); the editor's notes ask for a
            # {retired} fill from the model, so the word never goes stale
            'whole_issues': '{n}, one retired',
            # R27 (ST-2): {numbered} atlas:loops-numbered, {loops} atlas:loops, {conceptual} atlas:loops-conceptual in
            # words (house rule H06), each a count span the kit fills from the model; {retired} as before
            'whole_note': 'The whole atlas counts each loop and reform once, though many reach several sheets, and its '
                          'reforms leave out those the atlas rejects. Its loops column counts the {numbered} loops that '
                          'close through numbered connections; the loop index lists all {loops}, since {conceptual} more '
                          'close only in concept, with no chain of connections to file.',
            'sheet_question_label': 'Its everyday question',
            'variables_heading': 'Its variables',
            # CE8 and R22: each variable on the sheet, {var} its chip, {name} its stored title, {means} its stored
            # sentence on a higher value
            'variable_line': '{var} “{name}”: {means}',
            'connections_heading': 'Connections filed here',
            'conn_head': ['Connection', 'From, to', 'Sign', 'Type', 'Delay', 'Grade', 'The atlas’s citation'],
            # editor: the h2 over the rejected option and the connections reviewed and not drawn (specs 10.1)
            'rejected_section': 'What our atlas decided against',
            # the Rejected and Records section bands' ledes (specs 14.1)
            'rejected_lede': 'The atlas keeps what it rejected on the sheet, with the evidence behind each decision.',
            'records_lede': 'Each issue record names the variables it touches. Narrow the list to the records for one '
                            'of them.',
            'rejected_heading': 'Rejected option',
            # our words before the atlas's own sentence, which the kit quotes from the stored text (DR-37)
            'rejected_grade': 'For a rejected option, the grade measures confidence in harm',
            # batch 1, item 16: its targets, each a linked chip to its line; {targets} joined with "and"
            'rejected_targets': 'It would act on {targets}.',
            # the rejected option's two grade rows (Rule 15.12's labels)
            'problem': 'Evidence of the problem',
            'remedy': 'Evidence for the remedy',
            # between a connection's two variables, in the table and in a reviewed connection's line
            'to': 'to',
            # R11: a reviewed connection's words before its variables; {id} is its ID, printed with no chip
            'reviewed_word': 'reviewed connection {id}',
            'reviewed_heading': 'Reviewed and not drawn',
            'records_heading': 'Its issue records',
            'filters': 'Filters',
            'filters_on': 'Filters, {n} on',
            'filters_clear': 'Clear filters',
            # the status line, as chapter 18's script writes it after each change: "{n} of {total} " and the noun
            'showing': '{n} of {total} issue records',
            'records_noun': 'issue records',
            'records_none': 'No issue record matches. Turn a filter off, or clear the filters, to see more.',
        },
    },
    'A14': {
        'view': 'Loop R18, “{title}”',             # in quotation marks, as Rule 18.22 names a loop
        'current_view': 'Loops',
        'crumbs': [['Home', '/atlas'], ['Loops', '/atlas/loops']],
        'page': {
            'kind': '{kind} loop',
            'grade_line': '{grade} for {from} to {to}',
            # R22 item 4: the head's grade of each step by its connection, {conn} the chip and its stored name in
            # quotation marks, joined by the kit with “; ”
            'grade_step': '{grade} for {conn}',
            'facts_label': 'This loop',
            'facts': {'kind': 'Kind', 'steps': 'Steps', 'minus': 'Minus signs', 'closure': 'How it closes',
                      'delay': 'Delay', 'weakest': 'Weakest step'},
            'minus_even': '{n}, an even count',
            'minus_odd': '{n}, an odd count',
            'stepper_heading': 'Step through the loop',
            'read_label': 'Read aloud',
            # the read-aloud line (R4), composed by the kit from these templates: {var} a variable's chip and title,
            # {conn} a connection's chip, {sign} a word from ATLAS['signs'], {dir} a word from 'dirs'
            'read_start': 'Start with {var} rising.',
            'read_step': 'Along {conn}, which {sign}, {var} {dir}.',
            'read_end_same': 'The loop comes back moving the same way it started.',
            'read_end_other': 'The loop comes back moving the other way from how it started.',
            'dirs': {'up': 'rises', 'down': 'falls'},
            'arithmetic': 'This reading starts with a rise and turns at each minus sign.',
            'parity_even': 'An even count of minus signs, {n} here, makes the loop reinforcing, so it feeds itself.',
            'parity_odd': 'An odd count of minus signs, {n} here, makes the loop balancing, so it pushes back on the '
                          'first change.',
            'weakest_label': 'Weakest step',
            'weakest_line': 'The loop holds only as firmly as this step.',
            'also_aim': '{chips} also aim here',
            # editor: the form for one reform alone, for the kit to choose by count (Requests)
            'also_aim_one': '{chips} also aims here',
            # the stepper's status lines (Rule 15.19's step words, in the form chapter 15's stepper uses); the kit
            # prefixes "Step n of m: " and the hold counts every word read (AL-24)
            'steps': [
                {'line': 'Presidential action without new legislation lowers the ability to investigate and enforce the '
                         'rules. Connection L14 “Presidential removals weaken watchdog agencies”: the atlas grades it '
                         'documented, and its effect takes under 2 years.'},
                {'line': 'The ability to investigate and enforce the rules can lower presidential action without new '
                         'legislation. Connection L15 “Independent watchdogs restrain unilateral action”: the atlas '
                         'grades it plausible, the weaker of the loop’s two steps, and its effect takes 2 to 10 years. '
                         'The loop is back where it began, and with a minus sign on both steps it is reinforcing.'},
            ],
            'step_prefix': 'Step {n} of {m}:',
            'stepper_ready': 'Ready. Press Play to step through the loop, or Next step to follow one connection at a '
                             'time.',
            'chooser_legend': 'Reforms that aim at this loop',
            # batch 1, item 18: the note beside the drawing (Rules 12.5 and 15.20), changing with the choice;
            # {reform} its chip, {targets} the targets on the drawing, {off} the targets off it, each a chip
            'chosen_note': '{reform} acts where the marks turn red: on {targets}.',
            'chosen_off': 'Its other targets, {off}, sit off this drawing.',
            'chosen_off_one': 'Its other target, {off}, sits off this drawing.',   # one target off the drawing
            'chosen_none': '{reform} acts on {off}, none of which sits on this drawing, so nothing turns red.',
            'effects_heading': 'What it would change',
            # R21 (ST-1): under each panel's four effect rows, the reform page's line and words; then Rule 15.20's
            # disclosure under the panel, in approved chapter 15's words ({reform} the chip; {grade} the display word in
            # lower case; {text} the stored remedy_evidence.text or tradeoffs, whole)
            'effects_confidence': 'Our atlas’s confidence in these effects: “{text}”',
            'assumptions_summary': 'Our atlas’s qualifications and assumptions for {reform}',
            'assumptions_remedy': 'The evidence for the remedy, {grade}: “{text}”',
            'assumptions_tradeoffs': 'Its tradeoffs: “{text}”',
            'routes_heading': 'How it could pass',
            'record_heading': 'The loop in our atlas’s words',
            # the Record section band's lede (specs 14.1)
            'record_lede': 'Its summary, a case on the record, what it depends on and how it adapts, each as the atlas '
                           'stores it.',
            'record_labels': {'summary': 'Summary', 'case': 'The case', 'qualification': 'What it depends on',
                              'adaptation': 'How it adapts'},
            'evidence_heading': 'Evidence for each step',
            'step_word': 'Step {n}',
            'on_sheet': 'Its line in the Register, on the sheet for {sheet}',
            'records_line': 'Issue records on this loop: {n}',
        },
    },
    'A15': {
        'view': 'Loops',
        'current_view': 'Loops',
        'crumbs': [['Home', '/atlas']],
        'page': {
            'h1': 'Every loop in our atlas',
            'intro': 'A loop is a chain of causes that returns to where it started. The reinforcing loops, which feed '
                     'themselves, come first, then the balancing loops, which push back on a change, each group in the '
                     'order the atlas lists it.',
            'reinforcing': 'Reinforcing',
            'balancing': 'Balancing',
            # the two section bands' ledes (specs 14.1); conceptual loops have no numbered steps to count
            'reinforcing_lede': 'Each of these loops feeds itself; where its steps are numbered, an even count of minus '
                                'signs shows it.',
            'balancing_lede': 'Each of these loops pushes back on a change; where its steps are numbered, an odd count '
                              'of minus signs shows it.',
            'head': ['Loop', 'Title', 'Steps', 'Minus signs', 'How it closes', 'Grade'],
            # batch 1, item 22: a word the Steps and Minus signs columns hold; the closure column says why
            'no_chain': 'None',
            # DR-321: the note under the index
            'titles_note': 'These titles print as our atlas stores them, and its next version reviews the titles that '
                           'state an effect, among them those of Loop R5 and Loop R11.',
        },
    },
    'A16': {
        'view': 'How to read',
        'current_view': 'How to read',
        'crumbs': [['Home', '/atlas']],
        'page': {
            'h1': 'How to read our atlas',
            'intro': 'Each mark below appears on our atlas’s pages, and its row says what the mark means.',
            # editor: the five groups and each mark's name and meaning (specs 11.2; DD-11C-2, no rule numbers on the
            # page); the kit reads them once it draws the page (Requests)
            'groups': {'signs': 'Signs and types', 'grades': 'Grades', 'delay': 'Delay',
                       'loops': 'Loops and reforms', 'every': 'On every page'},
            'marks': {
                'raises': ['Plus sign, raises', 'The two variables tend to move the same way: when one rises, so does '
                                                'the other.'],
                'lowers': ['Minus sign, lowers', 'The two variables tend to move in opposite directions: when one '
                                                 'rises, the other falls.'],
                'type': ['Money, information, ownership', 'A word before the verb says what moves along the '
                                                          'connection. With no such word, the connection is causal: a '
                                                          'change in one variable changes the other.'],
                'authority': ['Open diamond, decides', 'One body holds legal power over something, such as setting a '
                                                       'rate. It carries no sign and never closes a loop.'],
                'documented': ['Documented', 'On the public record. A solid line, with a filled square before the '
                                             'word.'],
                'well-supported': ['Well supported', 'Strong research evidence. A solid line.'],
                'plausible': ['Plausible', 'Some evidence. A dashed line.'],
                'plausible_contested': ['Contested', 'Evidence disputed. A line of dashes and dots.'],
                'hypothesis': ['Hypothesis', 'Not yet tested. A dotted line.'],
                'record_square': ['Record square', 'The public record itself shows this connection.'],
                'S': ['One tick', 'The effect takes under 2 years.'],
                'M': ['Two ticks', 'The effect takes 2 to 10 years.'],
                'L': ['Three ticks', 'The effect takes over 10 years.'],
                'hollow': ['Hollow line', 'A step of a loop with no complete chain of numbered connections, which the '
                                          'atlas describes in words.'],
                'red': ['Red target', 'Where the chosen reform acts: the connections it changes and the outlines of '
                                      'the variables it targets. On the light page a red connection carries a thin dark '
                                      'edge.'],
                'tag': ['Also aim here', 'Other reforms that aim at the same place, in the text’s own color, so the red '
                                         'stays with the reform you chose.'],
                'weakest': ['Weakest step', 'The least certain step in a loop. The loop holds only as firmly as this '
                                            'step.'],
                'chip': ['Typed chip', 'The kind of record and its code together, such as Loop R18. A chip with an '
                                       'underline opens the record.'],
                'pressed': ['Pressed question', 'A check, bold words and a heavier edge mark the question you '
                                                'pressed.'],
            },
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
             'Who Do They Answer To? marked as the part the reader is in. Directly under it, the atlas’s title bar gives '
             'the atlas’s name, the date of its snapshot (Rule 13.10) and its views: Home, Loops, Reforms, The Register '
             'and How to read.',
             'Every page below the home adds a breadcrumb, the trail of links from the home to the page, and on wide '
             'screens a small locator that shows where the page sits in the whole system. Each page’s title names the '
             'view first, then the atlas, then Oath & Action.'],
    'why': 'A reader who reaches the atlas from a search or a shared link still sees whose site they are on and can '
           'reach every other part of it. The title bar keeps the atlas’s own views one step away, and it is the same '
           'Charcoal band that opens the atlas’s section on our home page.',
    'basis': 'The atlas’s place inside our website, under the site’s masthead with a title bar of its own, approved by '
             'our founder and editor on November 21, 2026; WCAG 2.2 SC 2.4.2 and Technique G88; Rules 12.7, 17.10 and '
             '20.1; design judgment for the title bar, from measured word widths',
    'specs': [('Order', 'Skip link, the site’s masthead, the atlas’s title bar, the breadcrumb, the page, the site’s '
                        'footer'),
              ('Title bar', 'A Charcoal band 56 px tall from edge to edge, in both themes: the atlas’s name in the label '
                            'style, then its subtitle and snapshot date in the caption style; the five views at the right, '
                            'in a navigation named Atlas views; on the atlas home, the head band below joins it'),
              ('Views', 'From 64em, in the masthead parts’ style and gap, ending at the parts’ right edge; the current '
                        'view in bold with a 2 px underline (Rule 17.10)'),
              ('Under 64em', 'The name and the snapshot at the left, and a Views button that opens the five views as rows '
                             'in place (Rule 18.8); the subtitle shows from 48em'),
              ('Breadcrumb', 'A navigation named Breadcrumb, 8 px under the band; the current page last, in bold with no '
                             'underline; on a record’s page, the record’s chip'),
              ('Locator', '88 by 41 px at the breadcrumb row’s right end from 48em, the parts as boxes and the page’s '
                          'own filled in ink; a link to the atlas home; hidden under 48em (Rule 12.7)'),
              ('Page title', 'The view, then Who Do They Answer To?, then Oath & Action, joined by vertical bars'),
              ('Landmarks', 'One banner, the site’s; navigations for the site’s parts, the atlas’s views and the '
                            'breadcrumb; one main; one footer')],
    'builders': ['Draw the masthead and footer with the website’s own code, add the title bar as a navigation of its own, '
                 'and build each page title from the view’s own words.'],
    'correct_caption': 'The top of Loop R18’s page at 1440 px, and at 390 px with the views open: the site’s masthead '
                       'with the atlas as the current part, the atlas’s title bar, the breadcrumb and, on the desktop, '
                       'the locator.',
    'correct_alt': 'Two crops of a loop page’s top. On the desktop, the site’s masthead with Who Do They Answer To? '
                   'underlined; a Charcoal title bar with the atlas’s name, its subtitle and snapshot date, and five views '
                   'with Loops underlined; then a breadcrumb ending on the chip Loop R18, and a small map of eight boxes '
                   'with one filled. On the phone, the masthead, then the Charcoal title bar open to five rows with Loops '
                   'marked, then the breadcrumb.',
    'failure_caption': '<strong>Fails Rule 21.1.</strong> The atlas brings a masthead of its own, so a reader sees two sets '
                       'of links and cannot tell whose site they are on, and the tab’s title names no page.',
    'failure_alt': 'The top of an atlas page with two mastheads: the site’s, with no part marked, and under it a second '
                   'banner with its own wordmark and its own copy of the site’s parts. The tab reads Oath & Action alone.',
    'fail_tab': 'Oath & Action',
    'fail_label': 'The top of the page at 1440 px, and its tab',
}
R['21.2'] = {
    'title': 'Open the atlas home on the whole system, with a count on every arrow.',
    'rule': ['Start the atlas’s home page with the whole system on the first screen. Each of its eight parts takes a box '
             'with its name, its question and the count of connections inside it. Where two parts connect, an arrow runs '
             'each way that connections run, with the count it carries.',
             'Draw the main circuit, from Wealth through Voice, Elections, Checks and Policy and back to Wealth, in the '
             'essential ink with its counts in bold, and the other arrows in the subtle ink, every arrow at one width. A '
             'switch, Show every variable, opens each box in place to list its variables and closes them again, so the '
             'page draws the system once.'],
    'why': 'A newcomer sees how the parts fit together before reading any one of them, and every number on the drawing is '
           'a count a reader can check in the Register. One drawing that opens in place keeps the first screen short.',
    'basis': 'The plain names and questions our founder and editor gave the atlas’s parts, with the model’s titles '
             'beneath; Rules 15.1, 15.2 and 15.9; the model’s parts and connections, counted by one written method; '
             'design judgment, from our earlier drawings of the atlas (Rule 15.25)',
    'specs': [('Parts', 'Eight boxes in the order effects travel: Outside forces, Wealth, Voice, Elections, Checks, '
                        'Policy, Your household and Technology, each with its plain name, its question and, on a line '
                        'labeled “In our atlas”, the atlas’s own title for the part'),
              ('Boxes and pills', 'A part takes a box with square corners, and a variable a pill (Rule 15.2)'),
              ('Counts', 'Inside each box and on each arrow, in the data label style with tabular figures, read at build '
                         'time; the build stops when a count and the model disagree'),
              ('Ink', 'The main circuit in the essential ink with its counts in bold; the other arrows in the subtle ink; '
                      'every count in the text’s ink; one width, 2 px; one single-headed arrow for each direction of a '
                      'pair'),
              ('Switch', 'A toggle button, Show every variable, with aria-pressed (Rule 18.2); pressed, it opens each '
                         'part’s list of variables for every reader, in the boxes on wide screens, in the cards on '
                         'phones and in the parts list a screen reader reads'),
              ('At 390 px', 'A stacked list of the eight parts, each with its counts and one line for each part its '
                            'connections reach, such as “5 to Voice”, so each count prints once')],
    'builders': ['Count every number on the drawing from the model at build time, and stop the build when a count and the '
                 'model disagree.'],
    'correct_caption': 'The atlas home’s drawing with Show every variable pressed, each of the eight parts open to its '
                       'variables, at 1440 px in the light theme.',
    'correct_alt': 'The atlas’s eight parts as boxes, each open to list its variables as pills, with arrows between the '
                   'parts, a count on each arrow and the main circuit drawn darker.',
    'failure_caption': '<strong>Fails Rule 21.2.</strong> The arrows widen with their counts and nothing on the drawing '
                       'says what a width measures, so the eye reads weight where the page prints a number.',
    'failure_alt': 'The five core parts and Your household as boxes, with arrows of different widths between them and no '
                   'key; the widest runs from Your household to Wealth.',
    'fail_label': 'The core row at 1440 px, arrows by count',
}
R['21.3'] = {
    'title': 'Light the parts an everyday question reaches, and name them in words.',
    'rule': ['Offer the atlas’s everyday questions under the topics the atlas calls hubs, each question as a button. When '
             'a reader presses one, it takes the pressed look of Rule 17.10: a check before its words, bold words and a '
             '2 px edge.',
             'The parts that hold the question’s variables stay at full strength with the words “The question you '
             'pressed reaches here”, and the others turn muted (Rule 17.8). A status line names the reached parts in '
             'words, and the question’s own short answer opens below, headed by the question, with each figure in it '
             'linked to its evidence. The page loads with no question pressed and every part at full strength.'],
    'why': 'A reader who arrives with a bill in hand sees at once which parts of the system decide it. Words carry the '
           'result too, so a reader who cannot see the shading, or who prints the page in gray, gets the same answer.',
    'basis': 'Rules 17.8 and 17.10; the variables each question’s own record names in the atlas; WCAG 2.2 SC 1.4.1 and '
             '4.1.3',
    'specs': [('Question', 'A toggle button with aria-pressed, one pressed at a time'),
              ('Pressed look', 'The selected check before the words, bold words and a 2 px edge in the strong border '
                               'color, where an unpressed question keeps 1 px (Rule 17.10)'),
              ('Lit parts', 'Each part that holds a variable the question’s own record names, at full strength with the '
                            'words “The question you pressed reaches here”'),
              ('The rest', 'Muted outlines (Rule 17.8), their words still in the text’s ink'),
              ('Status line', 'Names the reached parts in words after each press, and stays silent on load'),
              ('Answer', 'The pressed question’s own short answer, headed by the question and tied to it by '
                         'aria-controls; where its record stores none, words that say so; hidden while no question is '
                         'pressed'),
              ('Hubs', 'Named in words, with no chip (Rule 10.8)')],
    'builders': ['Light a part only where the question’s own record names a variable in it, and write the same parts in '
                 'the status line.'],
    'correct_caption': 'A question about medical bills pressed beside questions left unpressed, and the parts it reaches '
                       'at full strength, at 1440 and 390 px in the light and the dark theme.',
    'correct_alt': 'Crops of the atlas home. The drawing, with the parts the question reaches in full ink, each labeled '
                   '“The question you pressed reaches here”, and the other parts muted; and the questions under their '
                   'hubs, one marked by a check, bold words and a heavier edge, on the desktop and on a light and a dark '
                   'phone.',
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
    'rule': ['Give each reform a page that answers a reader’s questions in order: what it is and its status, with the '
             'date; where it acts, drawn at its targets, the variables and connections it acts on; how sure our atlas is '
             'that the problem exists and that the remedy works, as two grades; what it would change in each outcome '
             'family, the four groups of results the atlas judges reforms by, one to a row; how it could pass, route by '
             'route, each with its check date or Not checked; and where its evidence comes from.',
             'When the atlas grades a remedy contested, set the readings its record holds side by side, in the atlas’s '
             'own words, so a reader meets both before the routes.'],
    'why': 'A reader who asks whether a reform would work gets the evidence for the answer before the routes, and a '
           'contested remedy shows both sides of the dispute as our atlas records them.',
    'basis': 'Rules 15.11, 15.12, 15.16, 15.20 and 15.24, applied as one page; house rule H08 in chapter 02; Reform '
             'R-23’s own record in the atlas',
    'specs': [('Order', 'Head and status; where it acts; the two grades; the four effects; routes; reforms it works '
                        'alongside; sources'),
              ('Status', '“As of” and the date in words, from the record’s own check date (Rule 13.10)'),
              ('Contested remedy', 'The record’s text whole, split at one sentence into its two readings under Rule '
                                   '01.16’s matching labels, One reading and The other reading: side by side '
                                   'from 64em and one after the other below, each with its source a step away, printed '
                                   'as stored; house rule H08 governs our own sentences about the grade'),
              ('Effects', 'Rule 15.16’s rows in the atlas’s order, each code whole with its qualifier and a true minus; '
                          'Quality of democracy names the first family'),
              ('Routes', 'Rule 15.24’s rows, each with its check date or Not checked'),
              ('Sources', 'In a disclosure, closed on load and open on paper (Rule 18.8)')],
    'builders': ['Read every field from the reform’s own record, and set a contested remedy’s readings as one pair.'],
    'correct_caption': 'Reform R-23’s page at 1440 and 390 px, in the light and the dark theme.',
    'correct_alt': 'Reform R-23’s page four times: its head with a Charcoal status panel; a drawing of its two targets '
                   'outlined in red, with the other reforms that aim at one of them listed in ink; its two grades, the '
                   'contested remedy’s two readings side by side under the labels One reading and The other reading; its '
                   'effects, one row a family; its routes, each with its check date or Not checked; and a closed '
                   'disclosure of sources.',
    'failure_caption': '<strong>Fails Rule 21.4.</strong> The panel keeps the finding of little job loss, drops the '
                       'Congressional Budget Office’s estimate and grades the remedy well supported. Our atlas grades it '
                       'contested and records both.',
    'failure_alt': 'A remedy panel headed Well supported with one reading, of little job loss, and no second reading.',
    'fail_label': 'The remedy panel at 1440 px',
    'fail_grade': 'Well supported',
}
R['21.5'] = {
    'title': 'Tag reforms that share a target in ink, and keep the red for this one.',
    'rule': ['On a reform’s page, only that reform’s targets turn red. Where other reforms in our atlas aim at the same '
             'variable or connection, list them beside the drawing under that mark’s chip, each by its own chip and name, '
             'joined by commas and “and”, with the words also aim here, in the text’s ink. On a loop page, where a reader '
             'chooses one reform, the others that aim at the loop take the same tags.'],
    'why': 'A reader learns that several reforms aim at the same place in the system, and the one red still shows which '
           'reform the page is about (Rule 05.3).',
    'basis': 'Rules 05.3 and 12.5; the reforms’ own lists of targets in the atlas; design judgment for the tags',
    'specs': [('Tags', 'A list beside the drawing, one group for each target or step, headed by its chip: the other '
                       'reforms’ chips, each with its name at its first mention on the page, and “also aim here”, in the '
                       'data label style and the text’s ink'),
              ('Long lists', 'Past four reforms at one mark, “and [n] more” with a link to the list'),
              ('Red', 'The page’s own reform only (Rule 12.5); a tag stays in the text’s ink, with no outline or fill')],
    'builders': ['Find every reform whose own record names the same target, and list its chip in ink.'],
    'correct_caption': 'Reform R-23’s two targets in red, with the other reforms that aim at one of them listed in ink, '
                       'at 1440 and 390 px in the light theme.',
    'correct_alt': 'Two variables joined by one connection, both outlined in red, and beside them a list headed by the chip '
                   'Variable A4 and its name, holding the other reforms that aim there, each by its chip and name, and the '
                   'words also aim here.',
    'failure_caption': '<strong>Fails Rule 21.5.</strong> Five reforms share the red, so the page has five working reds and '
                       'no longer shows which reform it is about.',
    'failure_alt': 'The same two variables with every reform’s tag drawn in red, the page’s own among them.',
    'fail_label': 'The targets at 390 px',
}
R['21.6'] = {
    'title': 'Name every record in its typed chip, and let the chip open its page.',
    'rule': ['Every ID on an atlas page sits in its typed chip, the kind of record in words with its code, such as Loop R18 '
             'or Reform R-23. A chip that names a record with a page of its own links to that page, and a connection’s '
             'chip links to its line in the Register. The first time a page names a record, its name follows the chip, and '
             'for a rule change or a delivery case, the sentence the atlas stores for it. A claim has no name, so the '
             'sentence that holds its figure names it.'],
    'why': 'Our atlas uses B4 for a variable and for a loop, and Loop R1 sits one hyphen from Reform R-01. The word in the '
           'chip says which record a reader is looking at, and the link takes them to it.',
    'basis': 'Rules 13.9 and 18.24; house rule H11 in chapter 02; the codes our atlas repeats across kinds of record',
    'specs': [('Kinds', 'Rule 13.9’s ten words: Variable, Connection, Loop, Reform, Issue, Claim, Domain, Route, Rule '
                        'change and Delivery case'),
              ('Chip', 'Rule 18.24’s, plain or as a link with a target at least 24 px tall'),
              ('Link', 'To the record’s own page, or for a connection to its line in the Register, with the record’s name '
                       'as the link’s description where the words around it do not name it'),
              ('First mention', 'The record’s name as the atlas stores it, in quotation marks after the chip, set off by '
                                'commas where the sentence runs on; a list of chips joined by commas and “and”, each '
                                'with its name; later mentions on the page take the chip alone'),
              ('Kind word', 'From where the ID lives in the model, since the same letters name different kinds, as B4 '
                            'does'),
              ('Check', 'Every chip’s ID exists under its kind in the model (Rule 21.16)')],
    'builders': ['Take each chip’s kind word from where its ID lives in the model, since the same letters name different '
                 'kinds, as B4 does.'],
    'correct_caption': 'A chip for each of the ten kinds of record, plain and as a link, each a real record followed by its '
                       'name as the atlas stores it, all but the claim, which a figure’s own sentence names; then the four '
                       'pairs of codes our atlas repeats across kinds, on Newsprint and on Charcoal.',
    'correct_alt': 'Two panels, light and dark. In each, ten chips, plain and underlined, from Variable D4 to Delivery case '
                   'DL05, nine of them followed by the record’s name or stored sentence; then four pairs side by side: '
                   'Variable B4 and Loop B4, Loop R1 and Reform R-01, Variable D4 and Domain D04, and Variable X1 and '
                   'Issue X01.',
    'failure_caption': '<strong>Fails Rule 21.6.</strong> Bare codes let a loop pass for a variable: B4 and R1 here are '
                       'loops, filed under Variables.',
    'failure_alt': 'A list headed Variables with three bare codes and their names, B4, D4 and R1; B4 and R1 are loops.',
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
    'rule': ['Every claim an atlas page makes reaches its evidence in one step. A figure links to the atlas’s claim '
             'record, which gives the claim, its grade, the people and place it covers, its period, its limit and its '
             'source. In the Register, a connection’s line gives its grade and citation, and every chip for that '
             'connection links there. A reform keeps its sources in a disclosure on its own page.'],
    'why': 'A reader who doubts a number or a step can check it from the page they are reading, and every claim we print '
           'shows where it comes from.',
    'basis': 'The instruction for this chapter; Rules 13.6 and 13.9; the atlas’s claim and source records',
    'specs': [('Figure', 'Its claim’s chip right after it, linked to the claim’s record in a disclosure on the same page'),
              ('Connection', 'Its chip links to its line on its sheet of the Register'),
              ('Reform', 'Its sources in a disclosure, closed on load and open on paper (Rule 18.8)'),
              ('One step', 'One link or one disclosure, with no search between'),
              ('Source lines', 'Rule 13.6’s six parts, as far as the source record holds them')],
    'builders': ['Give every figure and every connection on a page a link to its own record, and fail the build when one '
                 'has none.'],
    'correct_caption': 'Two claims one step from their evidence, at 1440 px: the home answer’s figure with its claim '
                       'record open, and Loop R18’s first step beside its line in the Register.',
    'correct_alt': 'A short answer with a figure followed by the chip Claim CL1340, its record open beneath with its grade, '
                   'people, place, period and limit; then the chip Connection L14 in the loop page’s evidence row, beside '
                   'its line on the Register’s sheet for Domain D04.',
    'failure_caption': '<strong>Fails Rule 21.7.</strong> The figure points to a list of {answer_sources} sources at the foot '
                       'of the page, and a reader cannot tell which one holds it.',
    'failure_alt': 'A short answer with a figure and no chip, and a long numbered list of sources at the foot.',
    'fail_label': 'The answer and its sources at 1440 px',
    'fail_sources': 'Sources',
}

# ---- Group 3, the Register
R['21.8'] = {
    'title': 'Index the Register by sheet, and count each grade under its word.',
    'rule': ['Open the Register with one row for each of its sheets: one for each of the atlas’s domains, the subject '
             'areas it files records under, and one each for its economy and technology layers. Each row gives the '
             'sheet’s variables, connections, numbered loops, reforms and issue records, then how many of its '
             'connections carry each grade. An issue record is one of the atlas’s files on a documented problem, case or policy. A last row '
             'counts the whole atlas, each loop and reform once.'],
    'why': 'A reader sees where the atlas’s evidence is strong and where it is thin, sheet by sheet, in numbers they can '
           'check line by line.',
    'basis': 'Rules 13.3, 13.4 and 13.5; the model’s records, counted by one written method',
    'specs': [('Rows', 'Domains D01 to D10 with their chips, then the two layers in words (Rule 10.8), then the whole atlas'),
              ('Counts', 'Each connection on the sheet of the variable it moves; loops with numbered steps through the '
                         'sheet’s variables; reforms the atlas has not rejected, with a target on the sheet'),
              ('Grade columns', 'Rule 13.3’s five words in its order, each head with its 40 px line sample (Rule 13.4), '
                                'and no shade, width or bar'),
              ('Issue records', '“none filed” for the two layers; the whole row says how many are retired'),
              ('Whole atlas', 'Each loop and reform counted once, with a note under the table that says so and gives the '
                              'loop index’s count beside the numbered loops'),
              ('Table', 'Rule 18.10’s markup with tabular figures; at 390 px a card for each sheet, with a grade key '
                        'before the cards')],
    'builders': ['Count every column from the model by one written method, and print the method with the table.'],
    'correct_caption': 'The Register at 1440 and 390 px, in the light and the dark theme: its index of sheets, then the '
                       'sheet for Domain D04 open below it.',
    'correct_alt': 'The Register four times: an index table with a row for each sheet and one for the whole atlas, its '
                   'counts and five grade columns under a Charcoal head row; then the sheet for Domain D04 on a Charcoal '
                   'band, its variables, its connections with their signs, types, delays, grade lines and citations, the '
                   'reform the atlas rejects, and its issue records with one filter on.',
    'failure_caption': '<strong>Fails Rule 21.8.</strong> Shading ranks the grades and hides the counts, so a reader cannot '
                       'tell how many connections on a sheet are a hypothesis.',
    'failure_alt': 'An index with one bar for each sheet, shaded from dark to light, and no numbers.',
    'fail_label': 'The index’s grade column, shaded by grade',
}
R['21.9'] = {
    'title': 'File each connection once, on the sheet of the variable it moves.',
    'rule': ['On each sheet, list every connection that moves one of the sheet’s variables, once, with its chip, the two '
             'variables it joins, its sign as a tag and a word, its type, its delay, its grade as a line and a word, and '
             'the atlas’s citation. Give each line an address of its own, so a chip anywhere in the atlas can link to '
             'it.'],
    'why': 'Filed once, every connection has one home a reader can find, and the sheets add up to the atlas’s '
           '{connections}.',
    'basis': 'Rules 13.4, 13.5 and 15.3 to 15.5; the atlas’s connection records, filed by one written method',
    'specs': [('Filing', 'By the variable the connection moves; a variable in the economy or technology layer files on that '
                         'layer’s sheet, and one with two domains on the first'),
              ('Columns', 'Chip; from and to by title, with chips; sign tag with raises or lowers; type in words (Rule '
                          '15.4); delay ticks and words; grade line and word; the citation as stored'),
              ('Authority', 'Decides and the open diamond, with no sign (Rule 15.5)'),
              ('Address', 'Each line’s own anchor, register- and the connection’s ID')],
    'builders': ['File each connection by its variable’s sheet, and stop the build when the sheets do not add up to the '
                 'model’s count.'],
    'correct_caption': 'The sheet for Domain D10 with its connections at 1440 px in the light theme, its contested lines in '
                       'the dash and dot with the word Contested.',
    'correct_alt': 'A table of connections, each row with its chip, its two variables, a sign tag with raises or lowers, '
                   'its type, delay ticks, a grade line and word, and the atlas’s citation; the contested rows draw dash '
                   'and dot.',
    'failure_caption': '<strong>Fails Rule 21.9.</strong> Every connection appears on two sheets, so the Register counts '
                       '{double} where our atlas holds {connections}.',
    'failure_alt': 'The whole-atlas row of the index reading twice the atlas’s count of connections.',
    'fail_label': 'The whole-atlas row, filed twice',
}
R['21.10'] = {
    'title': 'Keep the rejected option and the connections left off the map on their sheets.',
    'rule': ['Where our atlas rejects a reform, keep it on the sheets its targets file on, as a rejected option, with its '
             'grade read as the atlas reads it: for a rejected option, a strong grade measures confidence in harm. Where '
             'the atlas reviewed a connection and left it off the map, list it on its sheet under Reviewed and not drawn, '
             'with its two variables and the atlas’s reason, and draw no line.'],
    'why': 'What the atlas decided against is evidence too, and a reader who meets a popular idea there sees the finding '
           'behind the decision.',
    'basis': 'Rules 15.10 and 15.12; the atlas’s rejected reform and the connections it reviewed and left off its map',
    'specs': [('Heading', 'The reform’s chip and its title as stored; the label Rejected option above it only when the '
                          'title does not begin with those words'),
              ('Grade', 'The atlas’s own words on what the grade measures, quoted under the grade word'),
              ('Reviewed and not drawn', 'Rule 15.10’s form: from and to with chips, the reason quoted, and no line in any '
                                         'pattern'),
              ('Counts', 'A rejected reform stays out of the index’s reforms column')],
    'builders': ['Read the rejected flag and the reviewed connections from the model, and file each on its targets’ '
                 'sheets.'],
    'correct_caption': 'At 390 px in the light theme: the reform the atlas rejects, on the sheet for Domain D04, and the '
                       'connections reviewed and not drawn on the sheet for Domain D10, each with the atlas’s reason.',
    'correct_alt': 'A block headed by the chip Reform R-35 and its title, which opens with Rejected option, holding its '
                   'effects, its two grades and a quoted line on what its remedy’s grade measures; then a block headed '
                   'Reviewed and not drawn with its connections, their variables and the atlas’s reasons, and no lines.',
    'failure_caption': '<strong>Fails Rule 21.10.</strong> Term limits read as a well supported remedy, though our atlas '
                       'rejects them on strong evidence of harm.',
    'failure_alt': 'A list of reforms in which Reform R-35 sits with no label and the words Well supported.',
    'fail_label': 'The sheet for Domain D04, its reforms, at 390 px',
}
R['21.11'] = {
    'title': 'Filter a sheet’s issue records by variable, and say how many show.',
    'rule': ['Under each sheet’s connections, list its issue records with their grades. Let a reader narrow the list to '
             'the records that name one of the sheet’s variables, with one Filters button that says how many filters are '
             'on, and a line that says how many records show out of how many.'],
    'why': 'A sheet can hold twenty or more records, and a reader who cares about one variable finds its records without '
           'reading all of them.',
    'basis': 'Rules 18.15 and 18.16; the variables each issue record names in the atlas',
    'specs': [('Control', 'Rule 18.16’s Filters button with the count of filters on, such as “Filters, 1 on”, and one '
                          'check box for each variable, each with its chip and its count of records'),
              ('Count line', 'A status line after each change, silent on load: “[n] of [total] issue records.” (Rule '
                             '18.15)'),
              ('Each record', 'Chip, title as stored, grade word'),
              ('No variable', 'Records that name none of the sheet’s variables show only with every filter off')],
    'builders': ['Build the filters from the variables on the sheet, and count each from the records’ own lists of '
                 'variables.'],
    'correct_caption': 'The sheet for Domain D04 with its issue records narrowed to Variable D4, at 390 px in the light '
                       'and the dark theme.',
    'correct_alt': 'A Filters button reading one on, its check boxes open with Variable D4 checked, a line giving how many '
                   'of the sheet’s records show, and the records as rows, each with its chip, title and grade word.',
    'failure_caption': '<strong>Fails Rule 21.11.</strong> Color alone shows which filter is on, nothing says how many records '
                       'are hidden, and the grades are gone.',
    'failure_alt': 'Three tabs, one filled, over a list of record titles with no count and no grades.',
    'fail_label': 'The filtered list at 390 px',
}

# ---- Group 4, loop pages
R['21.12'] = {
    'title': 'Head a loop page with the grade of each step and the arithmetic of its signs.',
    'rule': ['Open a loop page with the loop’s chip, its kind and its title from our atlas in quotation marks. Under the '
             'title, give the grade of each step in the atlas’s words, and name the weakest step, whose grade the whole '
             'loop takes.',
             'Then read the loop aloud, starting with a rise in its first variable and turning at each minus sign, and '
             'say beside it how the count of minus signs sets the kind: an even count makes a reinforcing loop, one that '
             'feeds itself, and an odd count a balancing loop, one that pushes back. Mark the weakest step on the drawing '
             'too, and say that the loop holds only as firmly as that step.'],
    'why': 'The arithmetic lets a reader check the loop’s kind from its signs, and naming the weakest step keeps the '
           'loop’s title from claiming more than its least certain step.',
    'basis': 'Rules 15.6, 15.7, 15.13 and 18.22; the loop’s record and evidence summary in the atlas',
    'specs': [('Head', 'Chip, the loop’s kind (Reinforcing or Balancing) and the title in quotation marks as the h1; under '
                       'it the grade of each step, by its connection’s chip and name; beside it the loop’s facts, the '
                       'weakest step among them'),
              ('Read aloud', 'Each step in turn from a rise in the first variable: the connection, its sign’s word and the '
                             'way the next variable moves; then the count of minus signs and the kind'),
              ('Weakest step', '“Weakest step” where the atlas’s evidence summary names it (Rule 15.13), with the line '
                               '“The loop holds only as firmly as this step.”'),
              ('Closure and delay', 'In the atlas’s words (Rule 15.7), the delay as ticks and words'),
              ('Chosen reform', 'Rule 15.20’s panel, with the atlas’s confidence in its effects quoted once under the four '
                                'rows, as on a reform’s page, and its qualifications and assumptions in a disclosure '
                                'under the panel')],
    'builders': ['Build the read-aloud line from the signs, and stop the build when the loop’s kind and its count of '
                 'minus signs disagree.'],
    'correct_caption': 'Loop R18’s page at 1440 and 390 px, in the light and the dark theme, with Reform R-11 chosen.',
    'correct_alt': 'Loop R18’s page four times: its head with the grade of each step and a Charcoal panel of facts that '
                   'names the weakest step; the loop read aloud beside its two-step drawing, the weakest step marked and '
                   'Reform R-11’s targets in red; the stepper; the reform chooser with the chosen reform’s effects, the '
                   'atlas’s confidence in them, a closed disclosure of its assumptions and its routes; the loop in the '
                   'atlas’s words; and the evidence for each step.',
    'failure_caption': '<strong>Fails Rule 21.12.</strong> The head grades Loop R18 documented, the grade of its first step. '
                       'Our atlas grades the return step plausible, and the loop holds only as firmly as that step.',
    'failure_alt': 'Loop R18’s head with the word Documented beside its title, no reading of its signs and no weakest '
                   'step.',
    'fail_label': 'The head at 1440 px',
}
R['21.13'] = {
    'title': 'Run the atlas’s stepper in the guide’s order and at the guide’s pace.',
    'rule': ['Every loop page steps through its loop with the loop stepper of Rule 18.22, the buttons that walk a reader '
             'through a loop one step at a time: Play, Reset the loop, Previous step and Next step, in that order, on '
             'every screen. Play holds each step 250 ms for every word its status line reads, the step’s count included, '
             'and at least six seconds, with reduced motion too. Nothing plays until a reader presses Play.'],
    'why': 'A reader who learns the stepper anywhere in our work finds the same buttons in the same order here, and the '
           'pace lets a reader, or a screen reader, finish each step before the next.',
    'basis': 'Rules 15.19 and 18.22; WCAG 2.2 SC 2.2.2 and 3.2.4',
    'specs': [('Order and names', 'Play, Reset the loop, Previous step, Next step (Rule 18.22)'),
              ('Phone', 'Under 48em, a two-by-two grid in reading order: Play and Reset the loop, then Previous step and '
                        'Next step'),
              ('Step words', 'The variables’ titles and the sign’s verb, then the connection, its grade and its delay '
                             '(Rule 15.19)'),
              ('Hold', '250 ms a word of everything the status line reads, the step’s count included, and at least '
                       '6,000 ms, with reduced motion too; counted by script from the status lines'),
              ('Code', 'Chapter 18’s loop stepper, read from its files')],
    'builders': ['Read the stepper from chapter 18’s files, and time each hold from its status line’s words.'],
    'correct_caption': 'Loop R18’s stepper on step 2 with its status line, at 390 px in the light theme with its buttons '
                       'two by two, and at 1440 px in the dark theme with its buttons in one row.',
    'correct_alt': 'Two steppers on step 2, each with its status line, Step 2 of 2 and the step’s words, and four buttons, '
                   'Play, Reset the loop, Previous step and Next step: two by two on the phone and in one row on the '
                   'desktop.',
    'failure_caption': '<strong>Fails Rule 21.13.</strong> The buttons run in another order than the rest of our work, and '
                       'each step moves on after about three seconds, before a reader can finish it.',
    'failure_alt': 'A stepper with Play, Previous step, Next step and Reset in one row, and a note reading 3,200 ms a step.',
    'fail_label': 'The stepper as the atlas runs it today',
    'fail_buttons': ['Play', 'Previous step', 'Next step', 'Reset'],
    'fail_hold': '3,200 ms a step',
}
R['21.14'] = {
    'title': 'List every loop on one index, by kind, closure and grade.',
    'rule': ['Give the atlas one index of its loops, the reinforcing ones first and then the balancing ones, each group in '
             'the order the atlas lists it. Each row gives the loop’s chip, its title, its number of steps, its count of '
             'minus signs, how it closes and its grade, the last two in the atlas’s words. Print each title as the atlas '
             'stores it, and leave out any score or rank of strength.'],
    'why': 'A reader can find a loop by its kind and see at a glance which loops rest on a hypothesis or close only in '
           'concept.',
    'basis': 'Rules 15.6, 15.7, 15.18 and 15.21; the atlas’s loop records; every loop title printed as the atlas stores '
             'it, with a note under the index, approved by our founder and editor on November 22, 2026',
    'specs': [('Groups', 'Reinforcing, then Balancing, each with its count, in the atlas’s order'),
              ('Row', 'Chip, title as stored, steps, minus signs, closure and grade as stored, each a link to the loop’s '
                      'page'),
              ('Conceptual loops', '“None” in the steps and minus signs cells, and the atlas’s closure, which says '
                                   'the loop has no numbered chain, with their grade (Rule '
                                   '15.18)'),
              ('Titles', 'As the atlas stores them, with one line under the index: the atlas’s next version reviews the '
                         'titles that state an effect'),
              ('Never', 'A strength, a score or a size for a loop (Rule 15.21)')],
    'builders': ['Read every row from the loop’s own record, in the atlas’s order.'],
    'correct_caption': 'The index of all {loops} loops at 1440 and 390 px in the light theme, with its note on the titles.',
    'correct_alt': 'A table of loops in two groups, reinforcing then balancing, each row with its chip, title, steps, minus '
                   'signs, how it closes and its grade, and a line under it on the titles.',
    'failure_caption': '<strong>Fails Rule 21.14.</strong> A bar ranks each loop by a strength our atlas does not measure.',
    'failure_alt': 'A list of loops, each with a horizontal bar of a different length, labeled Illustrative.',
    'fail_label': 'A ranked index',
}

# ---- Group 5, the dark theme and the atlas test
R['21.15'] = {
    'title': 'Draw the atlas’s dark theme from the Charcoal tokens, and measure every mark.',
    'rule': ['In the dark theme, every atlas page draws on Charcoal from the tokens set for Charcoal: text in Newsprint, '
             'quieter words and muted marks in Dim Newsprint, the selected bar in Newsprint and the red target in Pillar '
             'Red. Line patterns, sign tags, ticks and chips keep their shapes. Measure every mark on the page’s own '
             'pixels before it ships.'],
    'why': 'A reader who sets a device to dark reads the same atlas with the same marks, and every mark keeps the contrast '
           'it needs on Charcoal.',
    'basis': 'One dark theme for every screen product, with a visible switch that remembers the reader’s choice, approved '
             'by our founder and editor on November 10, 2026; Rules 05.2, 05.5 and 17.10; ratios measured on each '
             'frame’s pixels',
    'specs': [('Ground', 'Charcoal'),
              ('Text', 'Newsprint; quieter words in Dim Newsprint'),
              ('Marks', 'Essential in Newsprint; muted in Dim Newsprint'),
              ('Selected bar', 'Newsprint'),
              ('Red target', 'Pillar Red on Charcoal, with no edge; the 1 px Charcoal edge is for Newsprint (Rule 05.5)'),
              ('Hairlines that carry no meaning', 'Stone (Rule 05.5)'),
              ('Every color', 'From a token named in the page’s code; checked on the frame’s pixels'),
              ('Switch', 'The site’s (Rule 18.4), remembered across a reload')],
    'builders': ['Name a token for every color in a dark view, and check each frame’s pixels with the contrast script.'],
    'correct_caption': 'Loop R18’s drawing with Reform R-11’s three targets in red, Variable D4 and Connections L14 and '
                       'L15, and the chooser beside it, at 1440 px in the dark theme, with the ratios measured on the '
                       'plate’s pixels.',
    'correct_alt': 'Loop R18 on Charcoal, with Reform R-11’s three targets in red: the outline of Variable D4 and both of '
                   'the loop’s connections, L14 and L15. Beside it, a chooser of reforms with R-11 chosen, and a table '
                   'of contrast ratios measured on the frame.',
    'failure_caption': '<strong>Fails Rule 21.15.</strong> Muted marks in Stone clear 3 to 1 by a tenth, and the selection '
                       'draws in White, a color no token sets on Charcoal.',
    'failure_alt': 'A dark drawing with gray muted marks and a white selection bar.',
    'fail_label': 'The drawing with muted marks in Stone and a White selection',
    'ratio_head': ['Mark', 'Token', 'Measured'],
    'ratio_rows': {'text': 'Text', 'secondary': 'Quieter words and muted marks', 'red': 'The red target',
                   'hairline': 'A hairline that carries no meaning'},
    'ratio_value': '{r} to 1',
}
R['21.16'] = {
    'title': 'Test every atlas page against the model before it ships.',
    'rule': ['Before any atlas page ships, run the atlas test. It reads the page together with the model, the atlas’s '
             'data, and checks every ID, sign, type, delay, grade, count and date the page prints against the model. It '
             'also checks every red mark against the chosen reform’s targets, every effect against its family, every '
             'link from a claim to its evidence, and the stepper’s order and pace. A single failure stops the page.'],
    'why': 'The atlas changes as its evidence changes, and a page that copies a value can drift from the record without '
           'anyone seeing. The test reads the record on every build.',
    'basis': 'The atlas test this chapter carries for the standards checklist in chapter 28; chapter 15’s checks of its '
             'drawings, extended to pages',
    'specs': [('Checks', 'Sixteen, one line a check and page: typed IDs, connection marks, counts, loops, authority, red, '
                         'effects, routes and dates, evidence a step away, grade words, the stepper, pressed and lit '
                         'parts, colors, type, the site’s frame and retired words'),
              ('Output', 'PASS or FAIL, with the page, the frame, the record, the value printed and the model’s value'),
              ('Stop', 'Any FAIL stops the application kit’s build and the guide’s strict build'),
              ('Self-test', 'One planted fault for each check in a copy of a page, with the model untouched; it passes only '
                            'when each plant is caught by its own check and the clean pages stay quiet')],
    'builders': ['Run the atlas test on every build, and treat a failure as a stop.'],
    'correct_caption': 'The atlas test’s report from the build that drew these plates: each check against the four '
                       'views, with how many of each view’s frames and pages it read.',
    'correct_alt': 'A readable table of the atlas test’s report. Each row is a check, named by its number and what it '
                   'tests; the four columns are the views Home, Reforms, The Register and Loops. Each cell gives the '
                   'result, PASS or FAIL, and how many of that view’s frames and pages the check read.',
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
    'caption': 'Our atlas’s How to read page at 1440 px in the light theme: every mark its pages use, with its meaning. '
               'The table beside it names the rule that sets each mark.',
    'alt': 'A page of the atlas’s marks in five groups, each mark drawn small beside its name and meaning: the sign tags, '
           'the type words and authority’s open diamond; the five grade lines and the record square; the delay ticks; '
           'the hollow line, the red target, the Also aim here tag and the weakest step; the typed chip and the pressed '
           'question. '
           'Beside it, a table names the rule for each mark.',
}

# the line above each row of frames: the width, the theme and the state each frame shows, composed from a view's key
# (the engineer's C9: <width>-<theme>, then "screen", "open" or a part's name); joined by commas, rows by middle dots
VIEW_WORDS = {
    'px': '{w} px', 'light': 'light', 'dark': 'dark', 'screen': 'first screen', 'open': 'views open',
    # CD-S5: where two pages share a part's key in one plate, each page's own words for it
    'page_parts': {'A14': {'rowl14': 'Loop R18’s evidence for its first step, Connection L14'},
                   'A13': {'rowl14': 'Connection L14’s line in the Register',
                           'rejected': 'the rejected option on the sheet for Domain D04'},
                   'A18': {'rejected': 'reviewed and not drawn, on the sheet for Domain D10'}},
    'parts': {'top': 'the top of the page', 'drawing': 'the drawing', 'questions': 'the questions', 'answer': 'the answer',
              'targets': 'where it acts', 'grades': 'the two grades', 'effects': 'the effects', 'routes': 'the routes',
              'index': 'the index', 'sheet': 'the open sheet', 'records': 'the issue records',
              'rejected': 'the rejected option', 'stepper': 'the stepper', 'chooser': 'the chooser',
              'read': 'the loop read aloud', 'evidence': 'the evidence', 'claim': 'the claim’s record',
              'facts': 'the loop’s facts', 'status': 'where it stands', 'rowl14': 'Connection L14’s row'},
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


SPECS_DIR = ROOT / 'work/build/app-kit/specs'
LOOPS_M, REFORMS_M = M['loops'], M['reforms']


def record_of(aid):
    """The record an atlas page is about, read from the kit's content file (the engineer's, read-only)."""
    f = next(iter(sorted(SPECS_DIR.glob(f'{aid.lower()}-*.json'))), None)
    if not f:
        raise SystemExit(f'{aid}: no content file in {SPECS_DIR.relative_to(ROOT)}')
    c = json.loads(f.read_text())
    return c['view'], c.get('record')


def number_words(n):
    return ['none', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'][n] if n <= 10 else f'{n:,}'


def page_words(aid):
    """One atlas page's words for the kit (the engineer's C9 handshake): its whole title, the shared words, its current
    view, its breadcrumb and its template's own words. Templates in braces stay for the kit to fill from the model, counts
    included, so each count it prints carries its data-count mark (T3)."""
    if aid == 'all':
        return {k: page_words(k) for k in APPS}
    if aid not in PAGES:
        raise SystemExit(f'no atlas page {aid}; use {", ".join(APPS)} or all')
    p = PAGES[aid]
    page = dict(p['page'])
    if aid == 'A14':
        page['steps'] = [{'line': s['line'], 'hold': s['hold']} for s in page['steps']]
    view = p['view']
    if '{title}' in view:
        kind, rid = record_of(aid)
        view = view.replace('{title}', {'loop': LOOPS_M, 'reform': REFORMS_M}[kind][rid]['title'])
    return {
        'title': f'{view} | {META["title"]} | {ATLAS["title_end"]}',
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
    check_steps()


def check_steps():
    """The editor's request 10c: each stepper line quotes stored names, so it must still hold, for its own step, the
    connection's typed ID and stored name, its grade word and delay words, and both variables' titles, as the model
    stores them now; a line that drifts stops the build."""
    kind, rid = record_of('A14')
    lids = M['loops'][rid]['links']
    steps = PAGES['A14']['page']['steps']
    if len(steps) != len(lids):
        raise SystemExit(f'A14: {len(steps)} stepper lines for {len(lids)} steps of Loop {rid}')
    for i, (s_, lid) in enumerate(zip(steps, lids), 1):
        l = M['links'][lid]
        line = s_['line'].lower()
        need_ = [f'{ATLAS["kind_words"]["connection"]} {lid}', l['name'], ATLAS['grades'][l['evidence']],
                 ATLAS['delays'][l['delay']], M['nodes'][l['from']]['title'], M['nodes'][l['to']]['title']]
        miss = [x for x in need_ if x.lower() not in line]
        if miss:
            raise SystemExit(f'A14 step {i}: the line no longer holds {", ".join(repr(x) for x in miss)} from the model')


# ================================================================================================ LAYOUT
def ty(name):
    return ctx.ty(name)


class Waiting(Exception):
    """A plate that needs the kit's drawing or report before it can be written."""


# ------------------------------------------------------------------------------------------------ facts the plates draw
def typo(s):
    """DF1 (editor, chat 12): straight apostrophes and single quotes in the atlas's stored text print typographic,
    as approved chapter 15 prints the same stored titles (fix brief section 2); the stored words stay as stored."""
    return re.sub(r"(^|[\s(\[“])'", '\\1\u2018', str(s)).replace("'", '\u2019')


def _esc(s):
    return C.esc(typo(s))


def kw(kind):
    return ATLAS['kind_words'][kind]


NODES, LINKS, LOOPS, REFORMS, ISSUES = M['nodes'], M['links'], M['loops'], M['reforms'], M['issues']
DOMAINS = {d['id']: d for d in M['domains']}
PATHWAYS = {p['id']: p for p in M['pathways']}
LAYER_OF = {}
for _lk, _L in M['layers'].items():
    for _reg in _L.get('regions', []):
        for _n in _reg.get('nodes', []):
            LAYER_OF[_n] = _reg['id'] if _lk == 'core' else ('EC' if _lk == 'economy' else 'TC')


def part_of(v):
    """The data lead's part(): EC or TC for the two layers, else the variable's cluster (R2)."""
    lay = LAYER_OF.get(v)
    return lay if lay in ('EC', 'TC') else (NODES[v].get('cluster') or lay)


def sheet_of(v):
    lay = LAYER_OF.get(v)
    return lay if lay in ('EC', 'TC') else str(NODES[v]['domain']).split('/')[0]


FLOWS, INSIDE = {}, {}
for _k, _l in LINKS.items():
    _a, _b = part_of(_l['from']), part_of(_l['to'])
    if _a == _b:
        INSIDE[_a] = INSIDE.get(_a, 0) + 1
    else:
        FLOWS[(_a, _b)] = FLOWS.get((_a, _b), 0) + 1
assert sum(FLOWS.values()) + sum(INSIDE.values()) == FACT['connections'], 'flows and inside counts miss connections'


def sentences(t):
    return re.split(r'(?<=[.;])\s+(?=[A-Z])', t)


def kit_plate(aid):
    f = KIT_PLATES / f'{aid.lower()}.json'
    if not f.exists():
        raise Waiting(f'the kit has not drawn {aid} yet (work/build/app-kit/plates/{aid.lower()}.json)')
    return json.loads(f.read_text())


# ------------------------------------------------------------------------------------------------ style
BASE = (
    f'.w{{{ty("body")};color:var(--oa-color-text-primary-on-newsprint);max-width:100%}}.w p{{margin:0}}.w *{{box-sizing:border-box}}'
    f'.lab{{{ty("label")};margin:0 0 12px;color:var(--oa-color-text-secondary-on-newsprint)}}'
    f'.sm{{{ty("bodySmall")}}}.cap{{{ty("caption")};color:var(--oa-color-text-secondary-on-newsprint)}}'
    f'.dl{{{ty("dataLabel")}}}.ui{{{ty("ui")}}}'
    '.mt8{margin-top:8px}.mt16{margin-top:16px}.mt24{margin-top:24px}'
    '.pane{padding:16px;background:var(--oa-color-surface-newsprint);border:1px solid var(--oa-color-border-hairline-on-newsprint)}'
    '.dk{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal)}'
    '.dk .lab,.dk .cap{color:var(--oa-color-text-secondary-on-charcoal)}'
    f'.chip{{display:inline-flex;align-items:center;gap:.3em;padding:0 8px;border:1px solid var(--oa-color-border-strong-on-newsprint);{ty("dataLabel")};white-space:nowrap}}'
    '.dk .chip{border-color:var(--oa-color-border-strong-on-charcoal)}'
    '.chip.ln{min-height:24px;text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:.2em}'
    '.row{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center}'
    '.rows>div{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:10px 0;border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}'
    '.svgw{display:block;width:100%;height:auto}'
    '.sv text{fill:var(--oa-color-text-primary-on-newsprint)}'
    f'.sv .t{{{ty("dataLabel")}}}.sv .tb{{{ty("dataLabel")};font-weight:var(--oa-font-weight-bold)}}'
    f'.sv .tn{{{ty("ui")}}}'
)


def css(extra=''):
    return f'<style>{BASE}{extra}</style>'


def prune_css(css_, used):
    out, i = [], 0
    while i < len(css_):
        j = css_.find('{', i)
        if j < 0:
            out.append(css_[i:])
            break
        sel = css_[i:j].strip()
        depth, k = 0, j
        while True:
            if css_[k] == '{':
                depth += 1
            elif css_[k] == '}':
                depth -= 1
                if depth == 0:
                    break
            k += 1
        body = css_[j + 1:k]
        if sel.startswith(('@media', '@container', '@supports')):
            inner = prune_css(body, used)
            if inner.strip():
                out.append(f'{sel}{{{inner}}}')
        elif sel.startswith('@'):
            out.append(f'{sel}{{{body}}}')
        else:
            keep = [p for p in sel.split(',') if all(c in used for c in re.findall(r'\.([A-Za-z][\w-]*)', p))]
            if keep:
                out.append(','.join(keep) + '{' + body + '}')
        i = k + 1
    return ''.join(out)


def prune(html):
    bare = re.sub(r'<style\b[^>]*>.*?</style>', '', html, flags=re.S)
    used = {c for v in re.findall(r'class="([^"]*)"', bare) for c in v.split()}
    out = re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + prune_css(m.group(2), used) + m.group(3),
                 html, flags=re.S)
    return out.replace('<style></style>', '')


def spec(sid, html, rule, alt, **kw_):
    kw_.setdefault('readable', True)
    ctx.spec(sid, prune(html), CH, rule, alt, **kw_)
    return sid


def app(aid, views=None):
    """The kit's placeholder (contract C4), placed only once the kit has drawn the application."""
    kit_plate(aid)
    v = f' data-oa-app-views="{views}"' if views else ''
    return f'<div data-oa-app="{aid}"{v}></div>'


def view_words(key, aid=None):
    bits = key.split('-')
    out = [VIEW_WORDS['px'].format(w=bits[0]), VIEW_WORDS[bits[1]]]
    own = VIEW_WORDS['page_parts'].get(aid, {})                     # CD-S5 (editor, chat 12)
    for b in bits[2:]:
        out.append(VIEW_WORDS.get(b) if b in ('screen', 'open') else own.get(b) or VIEW_WORDS['parts'].get(b, b))
    return ', '.join(out)


ROWS_CSS = '.rw2+.rw2{margin-top:32px}'
PAGE_ROWS = [['1440-light'], ['390-light', '390-dark'], ['1440-dark']]


def rows(aid, layout):
    return ''.join(f'<div class="rw2"><p class="lab">{" · ".join(view_words(v, aid) for v in r)}</p>{app(aid, " ".join(r))}</div>'
                   for r in layout)


def chip(kind, rid, link=False):
    return f'<span class="chip{" ln" if link else ""}">{_esc(kw(kind))} <span>{_esc(rid)}</span></span>'


def gline(grade, w=40, ink='var(--oa-color-graphic-essential-on-newsprint)'):
    """A grade's line sample (R3): solid, dashed, dash and dot, or dots; the record square before documented."""
    t = {'documented': '', 'well-supported': '', 'plausible': ' stroke-dasharray="8 4"',
         'plausible_contested': ' stroke-dasharray="8 3 2 3"', 'contested': ' stroke-dasharray="8 3 2 3"',
         'hypothesis': ' stroke-dasharray="0 5" stroke-linecap="round"'}[grade]
    sq = f'<rect x="0" y="0.5" width="7" height="7" fill="{ink}"/>' if grade == 'documented' else ''
    x0 = 11 if sq else 0
    return (f'<svg class="gl" viewBox="0 0 {w + x0} 8" width="{w + x0}" height="8" aria-hidden="true" focusable="false">{sq}'
            f'<line x1="{x0}" y1="4" x2="{w + x0}" y2="4" stroke="{ink}" stroke-width="2"{t}/></svg>')


def grade_word(g):
    return ATLAS['grades'][g]


# ------------------------------------------------------------------------------------------------ the view plates
def s_opener():
    html = css(ROWS_CSS) + f'<div class="w">{rows("A11", PAGE_ROWS)}</div>'
    return spec('s-21-home', html, None, W['opener_alt'],
                notes='Drawn by the application kit (A11, the atlas home), full length at four views.')


def s_view(sid, aid, rid, what):
    r = R[rid]
    html = css(ROWS_CSS) + f'<div class="w">{rows(aid, PAGE_ROWS)}</div>'
    return spec(sid, html, rid, r['correct_alt'], notes=f'Drawn by the application kit ({aid}, {what}), full length at four views.')


def s21_reform():
    return s_view('s-21-reform', 'A12', '21.4', 'Reform R-23’s page')


def s21_register():
    return s_view('s-21-register', 'A13', '21.8', 'the Register with the sheet for Domain D04 open')


def s21_loop():
    return s_view('s-21-loop', 'A14', '21.12', 'Loop R18’s page')


def s_parts(sid, rid, layout, notes):
    html = css(ROWS_CSS) + '<div class="w">' + ''.join(rows(aid, lay) for aid, lay in layout) + '</div>'
    return spec(sid, html, rid, R[rid]['correct_alt'], notes=notes)


def s21_1_correct():
    return s_parts('s-21-1-correct', '21.1', [('A14', [['1440-light-top'], ['390-light-open-top']])],
                   'Drawn by the application kit (A14): the top of the loop page, and at 390 px with the views open.')


def s21_2_correct():
    return s_parts('s-21-2-correct', '21.2', [('A17', [['1440-light-drawing']])],
                   'Drawn by the application kit (A17, the atlas home with every variable shown).')


def s21_3_correct():
    return s_parts('s-21-3-correct', '21.3', [('A11', [['1440-light-drawing'], ['1440-light-questions'],
                                                      ['390-light-questions', '390-dark-questions']])],
                   'Drawn by the application kit (A11): the pressed question and the lit parts.')


def s21_5_correct():
    return s_parts('s-21-5-correct', '21.5', [('A12', [['1440-light-targets'], ['390-light-targets']])],
                   'Drawn by the application kit (A12): Reform R-23’s targets and the ink tags.')


def s21_7_correct():
    return s_parts('s-21-7-correct', '21.7', [('A20', [['1440-light-answer']]), ('A14', [['1440-light-rowl14']]),
                                             ('A13', [['1440-light-rowl14']])],
                   'Drawn by the application kit (A20, A14 and A13): a figure’s claim record open, and a step’s '
                   'chip beside its Register line.')


def s21_9_correct():
    return s_parts('s-21-9-correct', '21.9', [('A18', [['1440-light-sheet']])],
                   'Drawn by the application kit (A18, the Register with the sheet for Domain D10 open).')


def s21_10_correct():
    return s_parts('s-21-10-correct', '21.10', [('A13', [['390-light-rejected']]), ('A18', [['390-light-rejected']])],
                   'Drawn by the application kit (A13 and A18): the rejected option, and connections reviewed and not drawn.')


def s21_11_correct():
    return s_parts('s-21-11-correct', '21.11', [('A13', [['390-light-records', '390-dark-records']])],
                   'Drawn by the application kit (A13): the filtered issue records.')


def s21_13_correct():
    return s_parts('s-21-13-correct', '21.13', [('A19', [['390-light-stepper'], ['1440-dark-stepper']])],
                   'Drawn by the application kit (A19, Loop R18 on step 2).')


def s21_14_correct():
    return s_parts('s-21-14-correct', '21.14', [('A15', [['1440-light'], ['390-light']])],
                   'Drawn by the application kit (A15, the loop index).')


HOW_RULES = [('Sign tag, raises and lowers', '15.3'), ('Type words', '15.4'), ('Open diamond, decides', '15.5'),
             ('Grade words and glosses', '13.3'), ('Grade lines and the record square', '13.4'), ('Delay ticks', '13.5'),
             ('Hollow line', '15.7'), ('Red target', '12.5'), ('Also aim here', '21.5'), ('Weakest step', '15.13'),
             ('Typed chip', '13.9'), ('Pressed question', '17.10')]


def s21_how():
    table = ''.join(f'<div><span class="sm">{_esc(a)}</span><span class="cap">Rule {b}</span></div>' for a, b in HOW_RULES)
    html = (css(ROWS_CSS + '.rows{max-width:40rem}') + f'<div class="w">{rows("A16", [["1440-light"]])}'
            f'<div class="rows mt24">{table}</div></div>')
    return spec('s-21-how-to-read', html, None, EXTRA_HOW['alt'],
                notes='Drawn by the application kit (A16, How to read), with the rule that sets each mark listed under it '
                      '(DD-11C-2: the public page prints meanings alone).')


def s21_15_correct():
    r = R['21.15']
    plate = kit_plate('A14')
    view = next((v for v in plate.get('views', []) if v.get('key') == '1440-dark'), None)
    ratios = (view or {}).get('contrast')
    if not ratios:
        raise Waiting('Rule 21.15’s ratio table needs the kit’s measured contrast on A14 1440-dark (views[].contrast)')
    body = ''.join(f'<div><span class="sm">{_esc(r["ratio_rows"].get(k, k))}</span><span class="cap">{_esc(v.get("token", ""))}</span>'
                   f'<span class="dl">{_esc(r["ratio_value"].format(r=v.get("ratio")))}</span></div>' for k, v in ratios.items())
    html = (css(ROWS_CSS) + '<div class="w">' + rows('A14', [['1440-dark-drawing'], ['1440-dark-chooser']])
            + f'<p class="lab mt24">{" · ".join(r["ratio_head"])}</p><div class="rows">{body}</div></div>')
    return spec('s-21-15-correct', html, '21.15', r['correct_alt'],
                notes='Drawn by the application kit (A14, dark), with the ratios the kit measured on that frame’s pixels.')


def s21_16_correct():
    """The atlas test's report as the kit's last build wrote it: one row a check, one column a view, each cell the
    check's result and how many of that view's frames and exports it read (the test's own lines, counted)."""
    r = R['21.16']
    f = KIT_PLATES / 'atlas-test.json'
    if not f.exists():
        raise Waiting('Rule 21.16\u2019s plate needs the atlas test\u2019s report (work/build/app-kit/plates/atlas-test.json)')
    rep_ = json.loads(f.read_text())
    cells, names = {}, {}
    for ln in rep_.get('lines') or []:
        m = re.match(r'(PASS|FAIL) (T\d+) (A\d+) \S+ \S+: ([^,]+)', ln if isinstance(ln, str) else ln.get('line', ''))
        if not m:
            continue
        res, t, aid, name = m.groups()
        names[t] = name
        c = cells.setdefault((t, aid), {'PASS': 0, 'FAIL': 0})
        c[res] += 1
    apps = ['A11', 'A12', 'A13', 'A14']
    if not names:
        raise Waiting('the atlas test\u2019s report holds no lines')
    head = '<span class="dl"></span>' + ''.join(f'<span class="dl">{_esc(PAGES[a]["current_view"])}</span>' for a in apps)
    body = ''
    for t in sorted(names, key=lambda k: int(k[1:])):
        row = f'<span class="sm">{t} {_esc(names[t])}</span>'
        for a in apps:
            c = cells.get((t, a), {'PASS': 0, 'FAIL': 0})
            word = 'FAIL' if c['FAIL'] else 'PASS'
            row += f'<span class="dl{" fl" if c["FAIL"] else ""}">{word} {c["FAIL"] or c["PASS"]}</span>'
        body += f'<div class="g5">{row}</div>'
    html = (css('.g5{display:grid;grid-template-columns:2fr repeat(4,1fr);gap:4px 12px;padding:6px 0;'
                'border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint);font-variant-numeric:tabular-nums}'
                '.fl{font-weight:var(--oa-font-weight-bold)}.blk{max-width:54rem}')
            + f'<div class="w blk"><p class="lab">{_esc(r["report_label"])}</p><div class="g5">{head}</div>{body}</div>')
    return spec('s-21-16-correct', html, '21.16', r['correct_alt'],
                notes=f'Read from the atlas test\u2019s report (plates/atlas-test.json, {len(rep_.get("lines") or []):,} lines, '
                      f'self-test {rep_.get("self_test")}), counted by check and view for the four views.')


# ------------------------------------------------------------------------------------------------ the chips plate (21.6)
def _route(code):
    return next(x for x in M['routes']['items'] if x.get('code') == code)


def s21_chips():
    r = R['21.6']
    recs = [('variable', 'D4', NODES['D4']['title']), ('connection', 'L14', LINKS['L14']['name']),
            ('loop', 'R18', LOOPS['R18']['title']), ('reform', 'R-23', REFORMS['R-23']['title']),
            ('issue', 'I164', ISSUES['I164']['title']), ('claim', 'CL1340', None), ('domain', 'D04', DOMAINS['D04']['title']),
            ('route', 'SS', _route('SS')['name']),
            # R22 (CE12): a rule change and a delivery case take their stored sentence as their name; a claim has none
            ('rule-change', 'RL19', next(x for x in M['repairLog']['rows'] if x['id'] == 'RL19')['rule']),
            ('delivery-case', 'DL05', next(x for x in M['deliveryLog']['rows'] if x['id'] == 'DL05')['what_was_done'])]
    pairs = [(('variable', 'B4', NODES['B4']['title']), ('loop', 'B4', LOOPS['B4']['title'])),
             (('loop', 'R1', LOOPS['R1']['title']), ('reform', 'R-01', REFORMS['R-01']['title'])),
             (('variable', 'D4', NODES['D4']['title']), ('domain', 'D04', DOMAINS['D04']['title'])),
             (('variable', 'X1', NODES['X1']['title']), ('issue', 'X01', ISSUES['X01']['title']))]

    def one(dark):
        cls = ' dk' if dark else ''
        kinds = ''.join(f'<div>{chip(k, i)}{chip(k, i, True)}{f"<span class=sm>{_esc(t)}</span>" if t else ""}</div>'
                        for k, i, t in recs)
        prs = ''.join(f'<div><span class="pr">{chip(a[0], a[1])}<span class="sm">{_esc(a[2])}</span></span>'
                      f'<span class="pr">{chip(b[0], b[1])}<span class="sm">{_esc(b[2])}</span></span></div>' for a, b in pairs)
        return (f'<div class="pane{cls}"><p class="lab">{_esc(r["on_charcoal" if dark else "on_newsprint"])}</p>'
                f'<p class="lab">{_esc(r["chips_plain"])} · {_esc(r["chips_link"])}</p><div class="rows ck">{kinds}</div>'
                f'<p class="lab mt24">{_esc(r["chips_pairs"])}</p><div class="rows ck">{prs}</div></div>')
    html = (css('.ck>div{gap:8px 12px;align-items:center}.pr{display:inline-flex;flex-wrap:wrap;gap:4px 12px;align-items:center;flex:1 1 18rem}.dk .rows>div{border-color:var(--oa-color-border-hairline-on-charcoal)}'
                '.two{display:grid;gap:16px}')
            + f'<div class="w two">{one(False)}{one(True)}</div>')
    return spec('s-21-chips', html, '21.6', r['correct_alt'],
                notes='Drawn here from the model: each chip’s kind from where its ID lives, each name as stored, a rule '
                      'change’s and a delivery case’s stored sentence as their name (R22); a claim has no name, so its chip '
                      'stands alone.')


# ------------------------------------------------------------------------------------------------ failure plates
def _site_parts():
    import subprocess
    out = subprocess.run([sys.executable, '-I', str(HERE / 'phase4_ch20_build.py'), '--page-words', 'A04'],
                         capture_output=True, text=True, check=True).stdout
    return [p for p, _ in json.loads(out)['site']['parts']]


def master(path, w, h, style, red='signature'):
    dr = f' data-red="{red}"' if red else ''
    return f'<span class="mk"{dr}><img data-inline src="{path}" alt="" width="{w}" height="{h}" style="{style}"></span>'


WM24 = 'work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg'
INK_NEWS = ('color:var(--oa-color-text-primary-on-newsprint);--amp:var(--oa-color-identity-signature-on-newsprint);'
            '--lever:var(--oa-color-identity-signature-on-newsprint)')


def s21_1_failure():
    r = R['21.1']
    parts = _site_parts()
    items = ''.join(f'<span>{_esc(p)}</span>' for p in parts)
    html = (css('.tab{display:inline-block;padding:6px 16px;border:1px solid var(--oa-color-border-hairline-on-newsprint);'
                'border-bottom:0;background:var(--oa-color-surface-newsprint)}'
                f'.bar{{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:8px 16px;padding:14px 24px;'
                f'border:1px solid var(--oa-color-border-hairline-on-newsprint);{ty("ui")}}}'
                '.bar2{justify-content:space-between;background:var(--oa-color-surface-newsprint)}'
                '.mk{display:inline-block;line-height:0}')
            + f'<div class="w"><p class="lab">{_esc(r["fail_label"])}</p><span class="tab sm">{_esc(r["fail_tab"])}</span>'
            f'<div class="bar">{items}</div><div class="bar bar2">{master(WM24, 221, 24, INK_NEWS)}<span class="row">{items}</span></div></div>')
    return spec('s-21-1-failure', html, '21.1', r['failure_alt'],
                notes='A drawing of a fault: a second banner under the site’s masthead, its parts chapter 20’s words, '
                      'its wordmark inlined from the 24 px master; no part is marked current.')


def s21_2_failure():
    r = R['21.2']
    bw, gap, x0, W2 = 132, 37, 28, 866
    xs = {p: x0 + i * (bw + gap) for i, p in enumerate('ABCDE')}

    def head(x, y, ux, uy, w):
        k = 8 + w
        return (f'<path d="M{x} {y}L{x - k * ux - (k / 2) * uy} {y - k * uy - (k / 2) * ux}'
                f'L{x - k * ux + (k / 2) * uy} {y - k * uy + (k / 2) * ux}Z" fill="var(--ink)"/>')
    out = []
    for p_, x in xs.items():
        out.append(f'<rect x="{x + .5}" y="20.5" width="{bw - 1}" height="79" fill="none" stroke="var(--ink)"/>'
                   f'<text class="tn" x="{x + 12}" y="48">{_esc(PARTS[p_][0])}</text>')
    out.append(f'<rect x="{x0 + .5}" y="180.5" width="{xs["C"] + bw - x0 - 1}" height="49" fill="none" stroke="var(--ink)"/>'
               f'<text class="tn" x="{x0 + 12}" y="210">{_esc(PARTS["EC"][0])}</text>')
    for a_, b_ in (('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')):
        n = FLOWS[(a_, b_)]
        out.append(f'<line x1="{xs[a_] + bw}" y1="60" x2="{xs[b_] - 8 - n}" y2="60" stroke="var(--ink)" stroke-width="{n}"/>'
                   + head(xs[b_], 60, 1, 0, n))
    n = FLOWS[('EC', 'A')]
    xa = xs['A'] + 70
    out.append(f'<line x1="{xa}" y1="180" x2="{xa}" y2="{100 + 8 + n}" stroke="var(--ink)" stroke-width="{n}"/>' + head(xa, 100, 0, -1, n))
    n = FLOWS[('E', 'A')]
    out.append(f'<path d="M{xs["E"] + bw} 86H{W2 - 14}V250H10V86H{xs["A"] - 8 - n}" fill="none" stroke="var(--ink)" stroke-width="{n}"/>'
               + head(xs['A'], 86, 1, 0, n))
    svg = (f'<svg class="sv" viewBox="0 0 {W2} 262" width="{W2}" height="262" style="--ink:var(--oa-color-graphic-essential-on-newsprint);max-width:100%;height:auto" '
           f'aria-hidden="true" focusable="false">{"".join(out)}</svg>')
    html = css() + f'<div class="w"><p class="lab">{_esc(r["fail_label"])}</p>{svg}</div>'
    # D4-299: a drawing of a fault scales below 13 px in a phone's column, so it is a picture whose alt says every word
    # it shows (D4-211, D4-212's pattern), its part names read from PARTS
    names = [PARTS[k][0] for k in ('A', 'B', 'C', 'D', 'E', 'EC')]
    alt = (f'{r["fail_label"]}. Six boxes, {", ".join(names[:-1])} and {names[-1]}, with arrows of different widths between '
           f'them and no key; the widest runs from {names[-1]} to {names[0]}.')
    return spec('s-21-2-failure', html, '21.2', alt, readable=False, exempt=['scale', 'size'],
                notes='A drawing of a fault: each arrow 1 px wide for each connection it carries, read from the model, with '
                      'no key; drawn at 866 px, its true size, so its words scale with the column, and shown as a picture whose alt carries every word (D4-299).')


def s21_3_failure():
    r = R['21.3']
    hub = PATHWAYS['PW06']['hub']
    qs = [p for p in M['pathways'] if p['hub'] == hub][:3]
    btn = ''.join(f'<span class="q{" on" if p["id"] == "PW06" else ""}">{_esc(p["question"])}</span>' for p in qs)
    boxes = ''.join(f'<span class="bx{" tn" if p in ("A", "D") else ""}">{_esc(PARTS[p][0])}</span>' for p in ('A', 'B', 'D'))
    html = (css(f'.q{{display:block;padding:10px 12px;border:1px solid var(--oa-color-border-strong-on-newsprint);{ty("bodySmall")}}}'
                '.q+.q{margin-top:8px}.q.on{font-weight:var(--oa-font-weight-bold)}'
                f'.bx{{display:block;padding:12px 16px;border:1px solid var(--oa-color-graphic-essential-on-newsprint);{ty("ui")}}}'
                '.bx+.bx{margin-top:8px}.bx.tn{background:var(--oa-color-tint-stone-n70)}.qq{max-width:390px}')
            + f'<div class="w qq"><p class="lab">{_esc(r["fail_label"])}</p>{btn}<div class="mt16">{boxes}</div></div>')
    return spec('s-21-3-failure', html, '21.3', r['failure_alt'],
                notes='A drawing of a fault: the pressed question in bold alone, and two parts tinted with no words; the '
                      'questions as the atlas stores them.')


def s21_4_failure():
    r = R['21.4']
    text = REFORMS['R-23']['remedy_evidence']['text']
    first = ' '.join(sentences(text)[:3])
    html = (css('.blk{max-width:54rem;padding-top:16px;border-top:2px solid var(--oa-color-border-strong-on-newsprint)}'
                f'.gw{{{ty("h4")}}}.qt{{padding-left:24px;border-left:2px solid var(--oa-color-border-strong-on-newsprint)}}')
            + f'<div class="w"><p class="lab">{_esc(r["fail_label"])}</p><div class="blk"><p class="lab">'
            f'{_esc(PAGES["A12"]["page"]["remedy"])}</p><p class="gw">{_esc(r["fail_grade"])}</p>'
            f'<p class="qt mt16">{_esc(first)}</p></div></div>')
    return spec('s-21-4-failure', html, '21.4', r['failure_alt'], width=None,
                notes='A drawing of a fault: the first reading of Reform R-23’s stored remedy text alone, under a grade '
                      'the atlas does not give it.')


def s21_5_failure():
    r = R['21.5']
    others = sorted(k for k, v in REFORMS.items() if 'A4' in v['targets'])
    tags = ''.join(f'<span class="tg" data-red="working">{chip("reform", k)} {_esc(PAGES["A12"]["page"]["aims_here"])}</span>' for k in others)
    html = (css(f'.pl{{display:block;padding:10px 16px;border:4px solid var(--oa-color-data-emphasis-red-on-newsprint);box-shadow:0 0 0 1px var(--oa-color-palette-charcoal);border-radius:22px;{ty("bodySmall")}}}'
                '.ln2{width:2px;height:32px;margin-left:40px;background:var(--oa-color-graphic-essential-on-newsprint)}'
                '.tg{display:flex;align-items:center;gap:6px;margin-top:6px;color:var(--oa-color-data-emphasis-red-on-newsprint)}'
                '.tg .chip{border-color:currentColor}.qq{max-width:390px}')
            + f'<div class="w qq"><p class="lab">{_esc(r["fail_label"])}</p><span class="pl" data-red="working">{_esc(NODES["EC7"]["title"])}</span>'
            f'<div class="ln2"></div><span class="pl" data-red="working">{_esc(NODES["A4"]["title"])}</span><div class="mt8">{tags}</div></div>')
    return spec('s-21-5-failure', html, '21.5', r['failure_alt'],
                notes='A drawing of a fault: every reform that names Variable A4 in its own targets tagged in red, so five '
                      'working reds share the view.', exempt=['red', 'contrast'])  # D4-299: its red words are the fault


def s21_6_failure():
    r = R['21.6']
    items = [('B4', LOOPS['B4']['title']), ('D4', NODES['D4']['title']), ('R1', LOOPS['R1']['title'])]
    body = ''.join(f'<div><span class="dl">{c}</span><span class="sm">{_esc(t)}</span></div>' for c, t in items)
    html = css('.qq{max-width:390px}') + (f'<div class="w qq"><p class="lab">{_esc(r["fail_label"])}</p>'
                                         f'<p class="ui">{_esc(r["fail_head"])}</p><div class="rows">{body}</div></div>')
    return spec('s-21-6-failure', html, '21.6', r['failure_alt'],
                notes='A drawing of a fault: bare codes with their stored names; B4 and R1 name loops.')


def s21_7_failure():
    r = R['21.7']
    pw = PATHWAYS['PW06']
    src = M['sources']
    lis = ''.join(f'<li class="cap">{_esc(src[s]["publisher"] if src.get(s) and src[s].get("publisher") not in (None, "None") else "")}'
                  f'{", " if src.get(s, {}).get("publisher") not in (None, "None") else ""}{_esc(src.get(s, {}).get("title", s))}</li>'
                  for s in pw['source_ids'])
    html = (css('.ol{margin:16px 0 0;padding-left:2em;columns:2;column-gap:32px}.blk{max-width:54rem}')
            + f'<div class="w blk"><p class="lab">{_esc(r["fail_label"])}</p><p>{_esc(pw["short_answer"])}</p>'
            f'<p class="lab mt24">{_esc(r["fail_sources"])}</p><ol class="ol">{lis}</ol></div>')
    return spec('s-21-7-failure', html, '21.7', r['failure_alt'],
                notes=f'A drawing of a fault: the pathway’s stored short answer, its figure with no chip, and its '
                      f'{len(pw["source_ids"])} sources listed at the foot, none tied to the figure.')


GRADES5 = ['documented', 'well-supported', 'plausible', 'plausible_contested', 'hypothesis']
SHADES = ['var(--oa-color-palette-charcoal)', 'var(--oa-color-palette-stone)', 'var(--oa-color-derived-dim-newsprint)',
          'var(--oa-color-tint-stone-n70)', 'var(--oa-color-surface-newsprint)']


def s21_8_failure():
    r = R['21.8']
    sheets = [d['id'] for d in M['domains']] + ['EC', 'TC']
    by = {s: [0] * 5 for s in sheets}
    for k, l in LINKS.items():
        by[sheet_of(l['to'])][GRADES5.index(l['evidence'])] += 1
    titles = {**{d['id']: d['title'] for d in M['domains']}, 'EC': M['layers']['economy']['title'],
              'TC': M['layers']['technology']['title']}
    rows_ = ''
    for s in sheets:
        tot = sum(by[s]) or 1
        segs = ''.join(f'<span style="flex:{n};background:{SHADES[i]}"></span>' for i, n in enumerate(by[s]) if n)
        rows_ += f'<div><span class="sm nm">{_esc(titles[s])}</span><span class="bar">{segs}</span></div>'
    html = (css('.rows>div{flex-wrap:nowrap;align-items:center}.nm{flex:0 0 22rem}'
                '.bar{display:flex;flex:1;height:14px;border:1px solid var(--oa-color-graphic-essential-on-newsprint)}.blk{max-width:54rem}')
            + f'<div class="w blk"><p class="lab">{_esc(r["fail_label"])}</p><div class="rows">{rows_}</div></div>')
    return spec('s-21-8-failure', html, '21.8', r['failure_alt'],
                notes='A drawing of a fault: each sheet’s connections by grade as one bar shaded dark to light, its '
                      'shares read from the model, no counts.')


def s21_9_failure():
    r = R['21.9']
    pw = PAGES['A13']['page']
    active = sum(1 for v in REFORMS.values() if not v.get('rejected'))
    vals = [FACT['variables'], FACT['double'], FACT['loops_numbered'], active,
            pw['whole_issues'].format(n=f"{FACT['issues']:,}", retired=number_words(FACT['retired']))]
    head = ''.join(f'<span class="dl">{_esc(h)}</span>' for h in pw['index_head'])
    row = f'<span class="sm b">{_esc(pw["whole"])}</span>' + ''.join(f'<span class="sm b">{_esc(f"{v:,}" if isinstance(v, int) else v)}</span>' for v in vals)
    html = (css('.g6{display:grid;grid-template-columns:2fr repeat(5,1fr);gap:8px 12px;padding:10px 0;border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}'
                '.b{font-weight:var(--oa-font-weight-semibold);font-variant-numeric:tabular-nums}.blk{max-width:54rem}')
            + f'<div class="w blk"><p class="lab">{_esc(r["fail_label"])}</p><div class="g6">{head}</div><div class="g6">{row}</div></div>')
    return spec('s-21-9-failure', html, '21.9', r['failure_alt'],
                notes=f'A drawing of a fault: the whole-atlas row with each connection filed on both its variables’ '
                      f'sheets, {FACT["double"]:,} where the model holds {FACT["connections"]:,}.')


def _d04_reforms():
    vars_ = {k for k in NODES if sheet_of(k) == 'D04'}
    out = []
    for k, v in REFORMS.items():
        hit = any(t in vars_ or (t in LINKS and sheet_of(LINKS[t]['to']) == 'D04') for t in v['targets'])
        if hit:
            out.append(k)
    return out


def s21_10_failure():
    r = R['21.10']
    ks = [k for k in _d04_reforms() if not REFORMS[k].get('rejected')][:3] + ['R-35']
    body = ''.join(f'<div>{chip("reform", k)}<span class="sm">{_esc(REFORMS[k]["title"])}</span>'
                   f'<span class="dl">{_esc(grade_word(REFORMS[k]["remedy_evidence"]["grade"]))}</span></div>' for k in ks)
    html = css('.qq{max-width:390px}') + f'<div class="w qq"><p class="lab">{_esc(r["fail_label"])}</p><div class="rows">{body}</div></div>'
    return spec('s-21-10-failure', html, '21.10', r['failure_alt'],
                notes='A drawing of a fault: Reform R-35 among the sheet’s reforms with no label, its remedy grade read '
                      'as for a remedy that works; titles and grades as stored.')


def s21_11_failure():
    r = R['21.11']
    recs = [k for k in DOMAINS['D04']['issues'] if 'D4' in (ISSUES[k].get('nodes') or [])]
    tabs = ''.join(f'<span class="tb{" on" if v == "D4" else ""}">{_esc(v)}</span>' for v in ('D1', 'D4', 'D5'))
    body = ''.join(f'<div><span class="sm">{_esc(ISSUES[k]["title"])}</span></div>' for k in recs)
    html = (css(f'.tb{{display:inline-block;padding:8px 16px;{ty("ui")};background:var(--oa-color-tint-stone-n70)}}'
                '.tb.on{background:var(--oa-color-palette-prussian);color:var(--oa-color-text-primary-on-charcoal)}.qq{max-width:390px}')
            + f'<div class="w qq"><p class="lab">{_esc(r["fail_label"])}</p><div class="row">{tabs}</div><div class="rows mt8">{body}</div></div>')
    return spec('s-21-11-failure', html, '21.11', r['failure_alt'],
                notes='A drawing of a fault: color alone marks the filter, no count, no grades; the titles as stored.')


def s21_12_failure():
    r = R['21.12']
    html = (css(f'.h{{{ty("h3")}}}.blk{{max-width:54rem}}')
            + f'<div class="w blk"><p class="lab">{_esc(r["fail_label"])}</p><p class="row">{chip("loop", "R18")}'
            f'<span class="lab">{_esc(ATLAS["kinds"][LOOPS["R18"]["type"]])}</span></p>'
            f'<p class="h mt8">“{_esc(LOOPS["R18"]["title"])}”</p><p class="row mt16">{gline("documented")}'
            f'<span class="ui">{_esc(grade_word("documented"))}</span></p></div>')
    return spec('s-21-12-failure', html, '21.12', r['failure_alt'],
                notes='A drawing of a fault: Loop R18’s head with the grade of its first step and no reading of its signs.')


def s21_13_failure():
    r = R['21.13']
    btns = ''.join(f'<span class="bt">{_esc(b)}</span>' for b in r['fail_buttons'])
    html = (css(f'.bt{{display:inline-flex;align-items:center;min-height:44px;padding:8px 16px;border:1px solid var(--oa-color-border-strong-on-newsprint);{ty("ui")}}}'
                '.qq{max-width:390px}')
            + f'<div class="w qq"><p class="lab">{_esc(r["fail_label"])}</p><div class="row">{btns}</div>'
            f'<p class="cap mt8">{_esc(r["fail_hold"])}</p></div>')
    return spec('s-21-13-failure', html, '21.13', r['failure_alt'],
                notes='A drawing of a fault: the stepper’s buttons in the atlas’s own order today and its 3,200 ms pace '
                      '(registers F-8 and F-15).')


def s21_14_failure():
    r = R['21.14']
    ks = [k for k, v in LOOPS.items() if v['type'] == 'R'][:8]
    widths = [92, 80, 74, 66, 58, 47, 35, 22]
    body = ''.join(f'<div>{chip("loop", k)}<span class="sm nm">{_esc(LOOPS[k]["title"])}</span>'
                   f'<span class="bar"><span style="width:{w}%"></span></span></div>' for k, w in zip(ks, widths))
    html = (css('.rows>div{flex-wrap:nowrap;align-items:center}.nm{flex:0 0 26rem}.bar{flex:1;height:12px}'
                '.bar span{display:block;height:100%;background:var(--oa-color-graphic-essential-on-newsprint)}.blk{max-width:58rem}')
            + f'<div class="w blk"><p class="lab">{_esc(r["fail_label"])}</p>{ILLUS}<div class="rows mt8">{body}</div></div>')
    return spec('s-21-14-failure', html, '21.14', r['failure_alt'], illustrative=True,
                notes='A drawing of a fault: bar lengths invented for the drawing, labeled Illustrative; the atlas measures '
                      'no strength. Titles as stored.')


def two_lines(t, x, y):
    """A stored title set whole on two lines, broken at the space nearest its middle."""
    words = t.split()
    best = min(range(1, len(words)), key=lambda i: abs(len(' '.join(words[:i])) - len(' '.join(words[i:])))) if len(words) > 1 else 1
    l1, l2 = ' '.join(words[:best]), ' '.join(words[best:])
    return (f'<text class="tk" x="{x}" y="{y}" text-anchor="middle">{_esc(l1)}</text>'
            f'<text class="tk" x="{x}" y="{y + 17}" text-anchor="middle">{_esc(l2)}</text>')


def s21_15_failure():
    r = R['21.15']
    a_, b_ = typo(NODES['D2']['title']), typo(NODES['D4']['title'])     # DF1: stored text, typographic marks
    st = 'var(--oa-color-palette-stone)'
    svg = (f'<svg class="sv" viewBox="0 0 600 220" width="600" height="220" style="max-width:100%;height:auto" aria-hidden="true" focusable="false">'
           f'<path d="M130 80V30H470V80" fill="none" stroke="{st}" stroke-width="2"/>'
           f'<path d="M470 140V190H130V140" fill="none" stroke="{st}" stroke-width="2" stroke-dasharray="8 4"/>'
           f'<rect x="20" y="82" width="240" height="56" rx="28" fill="none" stroke="{st}" stroke-width="2"/>'
           f'<rect x="340" y="82" width="240" height="56" rx="28" fill="none" stroke="{st}" stroke-width="2"/>'
           f'{two_lines(a_, 140, 108)}{two_lines(b_, 460, 108)}</svg>')
    picks = [k for k, v in REFORMS.items() if 'R18' in (v.get('loops') or [])]
    ch = ''.join(f'<div class="pk{" on" if i == 0 else ""}">{chip("reform", k)}</div>' for i, k in enumerate(picks))
    html = (css('.dkp{padding:16px}.sv .tk{fill:var(--oa-color-text-primary-on-charcoal);font:var(--oa-type-data-label)}'
                '.pk{padding:6px 12px;border-left:4px solid transparent}.pk.on{border-left-color:var(--oa-color-palette-white)}')
            + f'<div class="w"><p class="lab">{_esc(r["fail_label"])}</p><div class="dk dkp">{svg}<div class="mt8">{ch}</div></div></div>')
    # D4-299: a picture whose alt says every word it shows (D4-211, D4-212's pattern), the titles read from the model
    alt = (f'{r["fail_label"]}. On Charcoal, two pills joined in a loop by gray lines, one dashed: \u201c{a_}\u201d and '
           f'\u201c{b_}\u201d. Below them the chips '
           + ', '.join(f'Reform {k}' for k in picks[:-1]) + f' and Reform {picks[-1]}, the first marked by a White bar.')
    return spec('s-21-15-failure', html, '21.15', alt, readable=False, exempt=['scale', 'size'],
                notes='A drawing of a fault: muted marks in Stone on Charcoal and the chosen reform\u2019s bar in White, the '
                      'colors of the dark kit today (register F-14); the reforms are those whose own records name Loop R18; '
                      'shown as a picture whose alt carries every word; its words scale with the column (D4-299).')


def s21_16_failure():
    r = R['21.16']
    line = r['fail_line'].format(printed=LINKS['L15']['evidence'] and 'documented', model=LINKS['L15']['evidence'])
    html = (css('.fl{padding:12px 16px;border-left:4px solid var(--oa-color-graphic-essential-on-newsprint);background:var(--oa-color-surface-newsprint)}.blk{max-width:54rem}')
            + f'<div class="w blk"><p class="lab">{_esc(r["fail_label"])}</p><p class="row">{chip("connection", "L15")}'
            f'{gline("documented")}<span class="ui">{_esc(grade_word("documented"))}</span></p>'
            f'<p class="fl dl mt16">{_esc(line)}</p></div>')
    return spec('s-21-16-failure', html, '21.16', r['failure_alt'],
                notes='A drawing of a fault: Connection L15 printed documented, beside the test’s line with the model’s grade.')


PLATES = [s_opener, s21_1_correct, s21_1_failure, s21_2_correct, s21_2_failure, s21_3_correct, s21_3_failure,
          s21_reform, s21_4_failure, s21_5_correct, s21_5_failure, s21_chips, s21_6_failure, s21_7_correct, s21_7_failure,
          s21_register, s21_8_failure, s21_9_correct, s21_9_failure, s21_10_correct, s21_10_failure, s21_11_correct,
          s21_11_failure, s21_loop, s21_12_failure, s21_13_correct, s21_13_failure, s21_14_correct, s21_14_failure,
          s21_how, s21_15_correct, s21_15_failure, s21_16_correct, s21_16_failure]


# ------------------------------------------------------------------------------------------------ the chapter
def build_chapter():
    waiting = []
    for f in PLATES:
        try:
            f()
        except Waiting as e:
            waiting.append(str(e))
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
        for sid in sorted(ctx.specs, key=lambda k: [int(x) if x.isdigit() else x for x in re.split(r'(\d+)', k)]):
            print(f'  {sid}: {len(ctx.specs[sid]["html"].encode()):,} bytes before the kit\u2019s frames')
        return
    if waiting:
        raise SystemExit('not written: plates wait for the kit')
    used = {ch['opener']} | {x['specimen'] for x in ch['extras']}
    for rr in ch['rules']:
        used |= {rr['correct']['specimen'], rr['failure']['specimen']}
    ours = set(ctx.specs)
    if used - ours or ours - used:
        raise SystemExit(f'specimens missing {sorted(used - ours)} unused {sorted(ours - used)}')
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for f in OUT_SP.glob('s-21-*.html'):
        if f.stem not in ours:
            f.unlink()
    for sid, s_ in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s_['html'])
    MANIFEST.write_text(json.dumps(dict(sorted((k, v['meta']) for k, v in ctx.specs.items())), indent=1,
                                   ensure_ascii=False) + '\n')
    print(f'wrote {OUT_CH.relative_to(ROOT)}, {len(ctx.specs)} specimens, {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
