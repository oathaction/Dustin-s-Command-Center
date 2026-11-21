"""Chapter 20, Web (design director), Phase 4, chat 11, November 21, 2026.

Usage:
    python3 -I work/build/scripts/phase-4/phase4_ch20_build.py                  write the chapter, specimens and manifest
    python3 -I work/build/scripts/phase-4/phase4_ch20_build.py --check          build everything in memory and report
    python3 -I work/build/scripts/phase-4/phase4_ch20_build.py --page-words A06 print one application's words as JSON
                                                                                 (A04 to A10, or "all"); writes nothing

Writes:
    work/build/guide/chapters/20-web.json            the chapter, in the content contract chapter 16 follows
    work/build/guide/specimens/s-20-*.html           one fragment per specimen this generator owns
    work/build/guide/specimens/manifest-web.json     this chapter's manifest, written whole

Reads, never writes: the Act page's docket file (work/research/20261121_Act-Page-Docket.md), the data files and sidecars
behind the facts the pages print (work/build/data/), the atlas model (work/extract/atlas-v7-data.json), the application
kit's plates and exports manifest once the kit has drawn them, and tokens.json and tokens.css (through the stage A helpers).

The plan is work/handoffs/phase-4/20261121_Chapter-20-Plan.md (eleven rules in three groups, one extra and an opener), and
the layout of every page is work/handoffs/phase-4/20261121_Web-Page-Specs.md. The pages themselves are drawn by the
application kit (contracts C3 and C4 in the engineer's notes): a correct plate holds only its words around a placeholder,
<div data-oa-app="A06" data-oa-app-views="...">, and the guide build sets the kit's frames in its place. No specimen copies
kit markup. Failure plates are small drawings this file makes from the tokens, each showing one fault.

Words. Every word a reader sees sits in the WORDS section near the top of this file, so the editor writes them there and
nothing else changes (brief section 9a; contract DD-3 in the design director's notes):
    W            the chapter's title, instruction, intro, group lines, opener caption and alt, related chapters, sources
    SITE         the masthead, menu and footer every page shares (applications A04 and A05, and A06 to A08)
    PAGES        each page's words: A06 home, A07 article, A08 Act page, A09 share preview, A10 favicons
    R['20.1'] to R['20.11']   each rule's title, rule, why, basis, specs, builders, captions and alts, then the words drawn
                 inside its failure plate under the keys that follow
    EXTRA_FILES  the extra after Rule 20.9
The kit reads SITE and PAGES by running this file with --page-words, so a page's words are written once, here. Facts the
pages print (counts, votes, dates, the docket, the agency's summary, the atlas's questions, source lines) are read from
their files below and checked, never typed twice; a fact that moves stops the build.

Specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color, no px
font size; every class is prefixed sx-.
"""
import argparse
import csv
import html as _html
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
OUT_CH = ROOT / 'work/build/guide/chapters/20-web.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-web.json'
KIT_PLATES = ROOT / 'work/build/app-kit/plates'
EXPORTS = ROOT / 'work/build/exports/phase-4'
CH = '20'
ILLUS = B.ILLUS
NB = C.NBSP
T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
ctx = B.Ctx(T, {}, 'final')


# ================================================================================================ FACTS, read from files
def _read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def _meta(name):
    return json.loads(_read(f'work/build/data/{name}.meta.json'))


def _need(text, *needles, where=''):
    for n in needles:
        if n not in text:
            raise SystemExit(f'{where}: “{n}” is no longer in the file; reread the Act page and Rule 20.8')


# The Act page's docket (DR-309). Every fact below must stand in the docket file word for word.
DOCKET_FILE = 'work/research/20261121_Act-Page-Docket.md'
_DK = _read(DOCKET_FILE)
DOCKET = {
    'docket': 'FDA-2025-N-2699',
    'rin': '0910-AI91',
    'citation': '91 FR 73717 (21 CFR Part 190)',
    'citation_short': '91 FR 73717',
    'published': 'November 17, 2026',
    'closes': 'January 19, 2027',
    'agency': 'Food and Drug Administration (FDA), Department of Health and Human Services',
    'comment_url': 'https://www.regulations.gov/commenton/FDA-2025-N-2699-0001',
    'rule_url': 'https://www.federalregister.gov/documents/2026/11/17/2026-23351/rulemaking-to-provide-that-n-acetyl-l-cysteine-is-not-excluded-from-the-dietary-supplement',
    'pdf_url': 'https://www.govinfo.gov/content/pkg/FR-2026-11-17/pdf/2026-23351.pdf',
    'mail': 'Dockets Management Staff (HFA-305), Food and Drug Administration, 5630 Fishers Lane, Rm. 1061, Rockville, MD 20852',
    'phone': '240-402-7500',
    'checked': 'November 21, 2026',
}
_need(_DK, *[v for k, v in DOCKET.items() if k not in ('agency', 'checked', 'citation_short')], where=DOCKET_FILE)
_need(_DK, '11:59 p.m. Eastern Time', 'Food and Drug Administration (FDA), Department of Health and Human Services',
      'between 9 a.m. and 4 p.m., Monday through Friday', 'THIS DOCUMENT CONTAINS CONFIDENTIAL INFORMATION',
      'medical information, your or anyone else’s Social Security number, or confidential business information',
      'read on November 21, 2026', where=DOCKET_FILE)
# The record's own words on each side and on the steps before the proposal (the main session's addendum, 20:17 to 20:19
# UTC, read from govinfo's PDF page by page and H.R. 7008's bill status file); each must stand in the file word for word
REC = {
    'petitions': 'In 2021, we received two citizen petitions requesting that we conclude that NAC is not excluded from the '
                 'definition of dietary supplement under section 201(ff)(3)(B) of the FD&C Act',
    'incentives': 'to protect the incentives for new drug development',
    'no_concern': 'To date, we have not received any comments expressing concern or providing data to demonstrate that '
                  'allowing the sale of NAC in or as a dietary supplement would impact drug development or identifying any '
                  'other concerns',
    'question': 'whether the sale of NAC-containing products labeled as dietary supplements in the United States has '
                'negatively impacted NAC drug development or is anticipated to in the future',
}
# The rule's step 1, Early notice (Rule 11.9): the FDA's Federal Register notice of April 22, 2022, in which it said it was
# likely to propose this rule (the rule, page 73723; D4-110). The page prints its date, so the date stands in the file.
EARLY_NOTICE = {'date': 'April 22, 2022', 'citation': '87 FR 24170'}
_need(_DK, *REC.values(), '(page 73720)', '(page 73721)', '(page 73723)', '2001, 2010 and July 2020',
      EARLY_NOTICE['date'], EARLY_NOTICE['citation'], 'was likely to propose', 'January 14, 2026',
      'yeas and nays, 7 to 4', 'lists no committee hearing', where=DOCKET_FILE)
_m = re.search(r'\*\*The agency.s summary, quoted\.\*\* "(.+?)"\n', _DK)
if not _m:
    raise SystemExit(f'{DOCKET_FILE}: the agency’s summary is no longer where Rule 20.8 reads it')
SUMMARY = _m.group(1)

# H.R. 7008's votes (DR-98), from the roll call file the guide's charts already use
HR = {(r['chamber'], r['party']): r for r in csv.DictReader(open(ROOT / 'work/build/data/congress-hr7008-roll-calls.csv'))}
SEN_YES = sum(int(r['yea']) for (ch, _), r in HR.items() if ch == 'Senate')
if (SEN_YES, 60 - SEN_YES) != (53, 7):
    raise SystemExit('H.R. 7008’s Senate vote has changed in its data file; reread the Track card')
HR_META = _meta('congress-hr7008-roll-calls')
HR_SOURCE = HR_META['printed_source_line']
HR_ASOF = 'November 11, 2026'
if HR_META['date_retrieved'] != '2026-11-11':
    raise SystemExit('H.R. 7008’s data was retrieved again; set the Track card’s “As of” date from it')

# Special districts (S86's data)
COG = {r['government_type']: int(r['governments']) for r in csv.DictReader(open(ROOT / 'work/build/data/census-cog-2022-governments-by-type.csv'))}
SD, ALL_GOV = COG['Special district governments'], sum(COG.values())
if (SD, ALL_GOV) != (39555, 90888):
    raise SystemExit('the Census of Governments counts have changed; reread the article')
COG_SOURCE = _meta('census-cog-2022-governments-by-type')['printed_source_line']

# The electric bill's eight bodies (S68's data, our systems atlas)
EL = json.loads(_read('work/build/data/v7-pathway-electric-decision-makers.json'))['rows']
EL_CAN = sum(1 for r in EL if r.get('can_change_rule'))
if (len(EL), EL_CAN) != (8, 6):
    raise SystemExit('the atlas’s electric bill record has changed; reread the Connect card')
EL_SOURCE = _meta('v7-pathway-electric-decision-makers')['printed_source_line']

# The atlas's everyday questions, one from each of its five hubs, in the atlas's own words
ATLAS = json.loads(_read('work/extract/atlas-v7-data.json'))
_PW = {p['id']: p for p in ATLAS['pathways']}
QUESTIONS = [(_PW[i]['question'], '/atlas/' + _PW[i]['slug']) for i in ('PW03', 'PW06', 'PW11', 'PW12', 'PW15')]
N_ANSWERS = len(ATLAS['pathways'])
if N_ANSWERS != 16 or len({_PW[i]['hub'] for i in ('PW03', 'PW06', 'PW11', 'PW12', 'PW15')}) != 5:
    raise SystemExit('the atlas’s everyday answers have changed; reread the home page’s atlas section')

# The Census Bureau's report on each state's governments, read at 19:03 UTC (design director's notes)
ISD = {'title': 'Individual State Descriptions: 2022 Census of Governments',
       'url': 'https://www.census.gov/library/publications/2024/econ/2022isd.html',
       'report': 'G22-CG-ISD', 'date': 'April 30, 2024'}

TAGLINE = 'A country that answers to its people.'
ADDRESS = 'oathandaction.org'


# ================================================================================================ WORDS
# Everything a reader sees. The editor's fields.
W = {
    'title': 'Web',
    'instruction': 'Build each web page from the system, opening on the reader’s question.',
    'intro': [
        'This chapter sets how our website looks and works. It covers the masthead, the menu and the footer every page '
        'shares; the home page, an article and an Act page; the preview a link shows when someone shares it; and the '
        'icon in a browser tab. Every page is built from the tokens and the components in chapter 18, in the '
        'light and the dark theme, at the four widths we test.',
        # DR-98: the bill named whole, with both provisions, at its first mention in the chapter
        'The pages here are real. The home page leads with one piece for each pillar: our explainer on special '
        'districts; our tracker for H.R.' + NB + '7008, the Stop Insider Trading Act, a bill that would limit stock '
        'purchases by members of Congress and require photo ID to vote in federal elections; a guide to who sets an '
        'electric bill; and a rule open for comment. The Act page walks through commenting on that rule, checked '
        'November 21, 2026. Only the web address is a stand-in, labeled Illustrative until our founder and editor '
        'settles it.'],
    'groups': [
        ('20.1', 'The frame every page shares',
         'Every page opens with the same masthead, closes with the same footer, names itself in its title and offers '
         'the theme switch in one place.'),
        ('20.6', 'Three pages',
         'The home page, an article and an Act page, each at four widths and in the dark theme, built from one set of '
         'parts.'),
        ('20.10', 'Beyond the page',
         'The preview a shared link shows, and the icons a browser and a phone draw for the site.'),
    ],
    'opener_alt': 'The home page’s first screen twice: on a desktop at 1440 px in the light theme, and on a phone at 390 px '
                  'in the dark theme. Each shows the masthead, the pillar row and the first pieces under it.',
    'opener_caption': 'The home page’s first screen on a desktop in the light theme and on a phone in the dark theme. On '
                      'the desktop the pillar row heads one piece for each pillar, the last of them a step a reader can '
                      'take now; on the phone each pillar heads its own section.',
    'related_chapters': [
        ('01', 'Content labels, process pieces and the spread of examples across issues and places.'),
        ('02', 'The writing rules, among them Rules 02.8 and 02.19, which retire the two lines the failure plates show.'),
        ('03', 'L3 and L1 in the masthead (Rule 03.6).'),
        ('04', 'The end mark, the favicon and the app icon (Rules 04.6 and 04.7).'),
        ('05', 'One dark panel a section and one working red a view (Rules 05.1 and 05.3).'),
        ('07', 'The grid at each width (Rules 07.2 and 07.3).'),
        ('08', 'The lockmark’s places: the footer and the sign-off (Rule 08.2).'),
        ('09', 'The pillar rows (Rule 09.1).'),
        ('11', 'The step trackers and the mark for a link to another site.'),
        ('14', 'The charts the pages carry, whole.'),
        ('18', 'The masthead, menu, theme switch, links and disclosure these pages reuse.'),
        ('19', 'The WCAG map this chapter completes.'),
        ('21', 'The atlas’s pages inside the site.'),
        ('26', 'The head script that applies a stored theme.'),
    ],
    'sources': [
        'Source: W3C, “Understanding Success Criterion 2.4.2: Page Titled”, “3.1.1: Language of Page”, “3.1.2: Language '
        'of Parts” and “3.2.6: Consistent Help”, and Technique G88, retrieved November 21, 2026. Behind Rules 20.3 and '
        '20.4.',
        'Source: Federal Register, document 2026-23351, “Rulemaking To Provide That N-acetyl-L-cysteine Is Not Excluded '
        'From the Dietary Supplement Definition”, ' + DOCKET['citation_short'] + ', ' + DOCKET['published'] + ', docket '
        + DOCKET['docket'] + ', and its PDF on govinfo.gov, retrieved November 21, 2026. Behind the Act page.',
        'Source: U.S. Census Bureau, ' + ISD['title'] + ', report ' + ISD['report'] + ', ' + ISD['date'] + ', and the '
        'Census of Governments glossary, retrieved November 21, 2026. Behind the article.',
        COG_SOURCE + ' The article’s counts.',
        HR_SOURCE + ' The home page’s tracker.',
        EL_SOURCE + ' The home page’s guide.',
        'Source: the platform rows for our website in our platform specifications, checked November 21, 2026: the share '
        'preview at 1200 by 630 px, the favicons and the app icons. Behind Rules 20.10 and 20.11.',
    ],
}

SITE = {
    'skip': 'Skip to the content',
    'home_name': 'Oath & Action, home',
    'nav_label': 'Parts of the site',
    'parts': [['Explain', '/explain'], ['Track', '/track'], ['Connect', '/connect'], ['Act', '/act'],
              ['Who Do They Answer To?', '/atlas'], ['About', '/about'], ['Subscribe', '/subscribe']],
    'menu': {'button': 'Menu', 'title': 'Menu', 'close': 'Close the menu', 'nav_label': 'Parts of the site, in the menu'},
    'footer': {
        'nav_label': 'Site map',
        'groups': [['Our work', [['Explain', '/explain'], ['Track', '/track'], ['Connect', '/connect'], ['Act', '/act']]],
                   ['The atlas', [['Who Do They Answer To?', '/atlas']]],
                   ['Oath & Action', [['About', '/about'], ['Subscribe', '/subscribe']]],
                   ['Help', [['Contact us', '/contact']]]],
        'tagline': TAGLINE,
        'address': ADDRESS,
        'illustrative': 'Illustrative',
    },
}

INTRO_SD = ('A special district is a local government that state law sets up to do one job or a few, such as supplying '
            'water or fighting fires. It keeps enough control over its own work and money to count as a government of '
            'its own, apart from the county, city or town around it.')

PAGES = {
    'A06': {
        'title': 'Oath & Action | ' + TAGLINE,
        'pillars': [
            {'pillar': 'explain', 'word': 'Explain', 'icon': 'cl-019',
             'kicker': ['Explainer', 'Local government'], 'symbol': 'cl-031',
             'headline': 'What a special district does', 'href': '/explain/special-districts',
             'dek': INTRO_SD.split('. ')[0] + '.', 'tracker': None, 'status': None,
             'dateline': 'November 21, 2026', 'source': None, 'link': None},
            {'pillar': 'track', 'word': 'Track', 'icon': 'cl-020',
             'kicker': ['Tracker', 'Congress'], 'symbol': None,
             'headline': 'H.R.' + NB + '7008, the Stop Insider Trading Act', 'href': '/track/hr-7008',
             'dek': 'The bill would limit stock purchases by members of Congress and require photo ID to vote in federal '
                    'elections.',
             'tracker': {'kind': 'bill', 'steps': [
                 {'n': 1, 'name': 'Filed', 'state': 'done'}, {'n': 2, 'name': 'Hearing', 'state': 'never'},
                 {'n': 3, 'name': 'Committee vote', 'state': 'done'}, {'n': 4, 'name': 'First chamber', 'state': 'done'},
                 {'n': 5, 'name': 'Second chamber', 'state': 'now'}, {'n': 6, 'name': 'President', 'state': 'ahead'}],
                 'pending': []},
             'status': [['Step 5 of 6: Second chamber.', True],
                        [f'On September 30, 2026, a Senate vote to take it up got {SEN_YES} votes, seven short of the 60 '
                         'it needed.', False]],
             'dateline': 'As of November 21, 2026',
             'source': HR_SOURCE + ' Steps from the bill’s status file on govinfo.gov, retrieved November 21, 2026.',
             'link': None},
            {'pillar': 'connect', 'word': 'Connect', 'icon': 'cl-021',
             'kicker': ['Guide', 'Electric bills'], 'symbol': None,
             'headline': 'Who sets your electric bill', 'href': '/connect/electric-bills',
             'dek': 'A regulator or a board approves your rate. Our systems atlas lists eight bodies behind an electric '
                    'bill, and six of them can change the rules that set it.',
             'tracker': None, 'status': None, 'dateline': None, 'source': EL_SOURCE, 'link': None},
            {'pillar': 'act', 'word': 'Act', 'icon': 'cl-022',
             'kicker': ['Act · How to take part', None], 'symbol': None,
             'headline': 'Comment on the FDA’s proposed rule on NAC', 'href': '/act/fda-nac-rule',
             'dek': 'The Food and Drug Administration proposes to let products containing N-acetyl-L-cysteine (NAC) be '
                    'sold as dietary supplements.',
             'tracker': {'kind': 'rule', 'steps': [
                 {'n': 1, 'name': 'Early notice', 'state': 'done'}, {'n': 2, 'name': 'Proposed', 'state': 'done'},
                 {'n': 3, 'name': 'Comments open', 'state': 'now', 'take_part': True},
                 {'n': 4, 'name': 'Comments closed', 'state': 'ahead'}, {'n': 5, 'name': 'Final rule', 'state': 'ahead'},
                 {'n': 6, 'name': 'In effect', 'state': 'ahead'}],
                 'pending': []},
             'status': [['Step 3 of 6: Comments open.', True], ['You can take part now.', True],
                        ['Comments close ' + DOCKET['closes'] + '.', False]],
             'dateline': None, 'source': None, 'link': ['How to send a comment', '/act/fda-nac-rule#comment']},
        ],
        'atlas': {
            'label': 'Our systems atlas',
            'heading': 'Who Do They Answer To?',
            'intro': f'Our systems atlas answers {N_ANSWERS} everyday questions with who decides, what the evidence shows '
                     'and who can change the rules.',
            'panel_label': 'Questions the atlas answers',
            'questions': [[q, h] for q, h in QUESTIONS],
            'open': ['Open the atlas', '/atlas'],
            'chart': 's10',
        },
    },
    'A07': {
        'title': 'What a special district does | Oath & Action',
        'current': 'Explain',
        'kicker': ['Explainer', 'Local government'], 'symbol': 'cl-031',
        'headline': 'What a special district does',
        'intro': INTRO_SD,
        'byline': ['Dustin Cathcart, Founder and Editor', 'November 21, 2026', '2026-11-21'],
        'count': {'figure': f'{SD:,}', 'line1': 'special districts in 2022, the most common kind of government',
                  'line2': f'of the {ALL_GOV:,} governments the Census Bureau counted', 'source': COG_SOURCE},
        'sections': [
            {'key': 'Count', 'heading': 'How the Census Bureau counts them', 'blocks': [
                {'p': f'The Census Bureau’s 2022 Census of Governments found {ALL_GOV:,} governments in the country: the '
                      f'federal government, the 50 states and {ALL_GOV - 51:,} local governments. Special districts made '
                      f'up {SD:,} of the local ones, more than four in ten.'},
                {'chart': 's86'},
                {'p': 'A district can go by many names, such as authority, board or commission. The state law that '
                      'creates it names the jobs it may do, from running a library to building a transit line.'}]},
            # the report explains how each state organizes its governments, in one summary a state, so the step is to
            # read your state's summary (the report's page, read by the design director at 19:03 UTC)
            {'key': 'Step', 'heading': 'See which districts your state has', 'blocks': [
                {'p': 'Each state’s laws decide which kinds of special district it allows and what they may do.'},
                {'p': 'Read your state’s summary in the Census Bureau’s report {link}. It covers each state and the '
                      'District of Columbia, arranged by kind of government.',
                 'link': [ISD['title'], ISD['url']], 'link_kind': 'another-site', 'end_mark': True}]},
        ],
        'count_fact': {'figure': '5', 'line1': 'years between censuses of governments',
                       'line2': 'Federal law requires the Census Bureau to take one every five years (Title 13, U.S. Code, '
                                'Section 161).',
                       'source': 'Source: U.S. Census Bureau, ' + ISD['title'] + ', report ' + ISD['report'] + ', '
                                 'introduction, ' + ISD['date'] + ', United States. Retrieved November 21, 2026.'},
        'def_source': 'Source for the definition and the report: U.S. Census Bureau, Census of Governments glossary, '
                      '“Special district governments” and its function entries, and ' + ISD['title'] + ' (report '
                      + ISD['report'] + ', ' + ISD['date'] + '), United States. Retrieved November 21, 2026. The counts '
                      'are the chart’s.',
    },
    'A08': {
        'title': 'How to comment on the FDA’s proposed rule on NAC | Oath & Action',
        'current': 'Act',
        'kicker': 'Act · How to take part',
        'headline': 'How to comment on the FDA’s proposed rule on NAC',
        'intro': 'The Food and Drug Administration proposes to let products containing N-acetyl-L-cysteine (NAC) be sold '
                 'as dietary supplements. Anyone may comment until ' + DOCKET['closes'] + ', and the agency then decides '
                 'whether to make the rule final.',
        'checked': 'Checked ' + DOCKET['checked'],
        'byline': ['Dustin Cathcart, Founder and Editor', 'November 21, 2026', '2026-11-21'],
        'status': {
            'label': 'Where the rule stands',
            'state_words': {'done': 'Done', 'now': 'Now', 'ahead': 'Not yet'},
            'steps': [{'n': 1, 'name': 'Early notice', 'state': 'done',
                       'note': EARLY_NOTICE['date'] + ': the FDA said it was likely to propose this rule'},
                      {'n': 2, 'name': 'Proposed', 'state': 'done', 'note': 'Published ' + DOCKET['published']},
                      {'n': 3, 'name': 'Comments open', 'state': 'now', 'note': 'Until ' + DOCKET['closes'],
                       'take_part': True},
                      {'n': 4, 'name': 'Comments closed', 'state': 'ahead', 'note': ''},
                      {'n': 5, 'name': 'Final rule', 'state': 'ahead', 'note': ''},
                      {'n': 6, 'name': 'In effect', 'state': 'ahead', 'note': ''}],
            'pending': [],
            'box': [['You can take part now.', True],
                    ['Comments close ' + DOCKET['closes'] + ', at 11:59 p.m. Eastern Time.', False]],
        },
        'ask': {'words': 'Comment at Regulations.gov', 'href': DOCKET['comment_url'],
                'hidden': '(another site)', 'address': DOCKET['comment_url']},
        'proposal': {
            'heading': 'What the FDA proposes',
            'doc_label': 'The proposed rule',
            'doc_parts': ['Food and Drug Administration', 'Docket ' + DOCKET['docket'], DOCKET['citation_short'],
                          'Published ' + DOCKET['published']],
            'quote': SUMMARY,
            'cite': 'The Food and Drug Administration’s summary of its proposed rule, ' + DOCKET['citation_short'] + ', '
                    + DOCKET['published'],
            'cite_href': DOCKET['rule_url'],
            # Rule 01.22's two sides, as the record holds them (DR-93; D4-108): the request, the law's concern with the
            # FDA's earlier position, the rule's statement that no comment has raised a concern, and the FDA's question
            'sides': {'heading': 'What the record shows',
                      'paragraphs': [
                          'The request. The rule says: “' + REC['petitions'] + '” (page 73720).',
                          'The concern in the law. In 2001, 2010 and 2020, the FDA said products containing NAC are '
                          'excluded from the dietary supplement definition (pages 73719 to 73720). That exclusion exists in '
                          'part “' + REC['incentives'] + '” (page 73721). The rule says: “' + REC['no_concern'] + '” (page '
                          '73723), and it asks commenters “' + REC['question'] + '” (page 73723).']},
            'decides_heading': 'Who decides',
            'decides': 'The FDA decides whether to make the rule final. Once it does, Congress and the President can '
                       'strike the rule down, and a court can set it aside.',
            'chart': 's66',
        },
        'comment': {
            'heading': 'How to send a comment',
            'steps': ['Open the docket’s comment page on Regulations.gov, the website most federal agencies use for '
                      'comments.',
                      'Write your comment, and include the docket number, ' + DOCKET['docket'] + '.',
                      'Leave out medical information, Social Security numbers and confidential business information. '
                      'Regulations.gov posts each comment unchanged, with any name or contact details in it.',
                      'Send it by 11:59 p.m. Eastern Time on ' + DOCKET['closes'] + '.'],
            'mail': 'You can also mail a comment, or have it delivered, to arrive by ' + DOCKET['closes'] + ': '
                    + DOCKET['mail'] + '. Confidential information goes this way only, in two copies, one marked '
                    '“THIS DOCUMENT CONTAINS CONFIDENTIAL INFORMATION” and one with that information blacked out.',
            'panel_label': 'Docket ' + DOCKET['docket'],
            'deadline': 'Comments close ' + DOCKET['closes'] + ', at 11:59 p.m. Eastern Time.',
            'others_heading': 'Read other comments',
            'others': 'You can read the comments the FDA receives on Regulations.gov, or in person at the Dockets '
                      'Management Staff from 9 a.m. to 4 p.m., Monday through Friday (' + DOCKET['phone'] + ').',
            'glance_heading': 'The rule at a glance',
            'glance': [['Agency', 'Food and Drug Administration, Department of Health and Human Services'],
                       ['Docket', DOCKET['docket']], ['Regulation Identifier Number', DOCKET['rin']],
                       ['Citation', DOCKET['citation']],
                       ['Published', DOCKET['published']],
                       ['Comments close', DOCKET['closes'] + ', 11:59 p.m. Eastern Time']],
            'checked': 'Checked ' + DOCKET['checked'] + '.',
            'links': [['The rule on the Federal Register', DOCKET['rule_url']],
                      ['The rule as a PDF on govinfo.gov', DOCKET['pdf_url']]],
        },
    },
    'A09': {
        'kicker': ['Explainer', 'Local government'],
        'headline': ['What a special', 'district does'],
        'alt': 'Explainer, Local government: What a special district does. Oath & Action.',
    },
    'A10': {'favicon_ink': '--oa-color-identity-signature'},
}

R = {}

# ---- Group 1, the frame every page shares
R['20.1'] = {
    'title': 'Open every page with the same masthead, and move its parts behind Menu once they no longer fit in the bar.',
    'rule': ['Every page opens with the same masthead. From 64em, 1,024 px at the default text size, the bar holds L3, the '
             'wordmark with the lockmark, at the left and the seven parts of the site at the right, in this order: '
             'Explain, Track, Connect, Act, Who Do They Answer To?, About and Subscribe. The theme switch sits on a row '
             'beneath them, at the right edge.',
             'Between 48em and 64em the bar keeps L3 and moves the parts and the switch behind Menu, and under 48em the '
             'bar sets L1, the wordmark alone, with Menu beside it. The part the reader is in shows in bold with a 2 px '
             'underline. Every part stays in the masthead’s ink, Subscribe included, so the view’s one red stays free '
             'for the step a reader can take. On an atlas page, the atlas’s own title bar sits under the masthead.'],
    'why': 'A reader finds the parts in the same place on every page, and a screen reader reaches them as one named set '
           'of links. The parts come in the order of the pillars and then the rest, so the list itself says what we do. '
           'Once the seven no longer fit beside L3, a Menu button keeps them one press away and leaves the wordmark its '
           'room.',
    'basis': 'Rules 03.6, 08.2 and 18.6; the parts approved by our founder and editor on November 21, 2026; design '
             'judgment for the breakpoints, from measured word widths',
    'specs': [('Bar, from 64em', '80 px tall: L3 from its masthead master, 282 by 48 px on whole pixels, at the left '
                                 'margin; the seven parts at the right, each a 44 px box in the interface style, 32 px '
                                 'apart from 90em and 16 px apart below it'),
              ('Switch row, from 64em', 'The theme switch, 44 px tall, at the right edge under the parts, with 16 px '
                                        'under it and then the 1 px hairline'),
              ('48em to 64em', 'An 80 px bar with L3 and Menu'),
              ('Under 48em', 'A 56 px bar: L1 from the 24 px master, 221 by 24 px, and Menu; under 24.375em, L1 from '
                             'the 16 px master, 152 by 16 px'),
              ('Measured', 'The seven parts take 484 px in the interface style, 580 px with their gaps at 1,024 px; with '
                           'L3 and 32 px of space they fill 894 of the 944 px inside the margins'),
              ('Divider', 'A 1 px hairline, 20 px tall, in the gap before Who Do They Answer To?, so the four pillars '
                          'read as a set'),
              ('Current part', 'Bold, with a 2 px underline at 0.3 em, and aria-current'),
              ('Red', 'None of its own: the wordmark’s ampersand and the lockmark’s lever are signature red'),
              ('Sticking', 'Never; the masthead scrolls away, so its lockmark and the footer’s never share a screen'),
              ('Landmarks', 'One header; the parts in a navigation named “Parts of the site”')],
    'builders': ['Write the parts once and let the bar or the menu show them. Test the bar at 1,024 px with the longest '
                 'current part in bold before you add an eighth part.'],
    'correct_caption': 'The masthead at 1440, 1024, 390 and 360 px in the light theme, and at 1440 and 390 px in the dark '
                       'theme, drawn on the article page, where Explain is the current part.',
    'correct_alt': 'Six mastheads stacked, from a 1440 px desktop to a 360 px phone and two in the dark theme. On the '
                   'desktop, L3 at the left and seven parts at the right with Explain underlined, and the theme switch '
                   'on a row beneath. On the phones, the wordmark and a Menu button.',
    'failure_caption': '<strong>Fails Rule 20.1.</strong> Subscribe takes a red fill in the masthead, so every page '
                       'spends its one red on a sign-up, and on the Act page the ask becomes the second red in the first '
                       'screen.',
    'failure_alt': 'The right end of a desktop masthead: Explain, Track, Connect, Act, Who Do They Answer To? and About in '
                   'ink, and Subscribe as a red button.',
    'fail_label': 'The right end of the bar at 1440 px',
}
R['20.2'] = {
    'title': 'Under 64em, open the parts in a menu that holds focus, with the theme switch at its top.',
    'rule': ['Menu opens the parts of the site in a dialog that covers the page. Its title, Menu, and Close the menu sit '
             'at the top, then the theme switch, then the seven parts as rows, with the current part on the selected '
             'band.',
             'Focus moves to the current part, or to Close the menu on a page with no current part. Tab and Shift+Tab '
             'keep focus inside the menu. Escape or Close the menu closes it and returns focus to Menu, and a part opens '
             'its page. If the window widens past 64em while the menu is open, it closes and focus moves to the current '
             'part in the bar, or to the home link on a page with none.'],
    'why': 'A dialog makes the page behind it unreachable, so a keyboard or screen reader user never walks into links '
           'the menu covers. The switch at the top keeps the theme one press away on a phone, where the bar has no room '
           'for it.',
    'basis': 'Rule 18.6 and the Dialog (Modal) pattern in the W3C’s ARIA Authoring Practices Guide; design judgment for '
             'the order inside',
    'specs': [('Dialog', 'The whole window, on the surface of the theme it opens in, with the page’s own side margins'),
              ('Head', '56 px: the title Menu in bold at the left; Close the menu, 44 px tall with its icon and words, at '
                       'the right; a 1 px strong line under it'),
              ('Switch', '24 px under the head: its legend, Theme, on its own line, then the three choices; at 360 px '
                         'Match my device wraps to its own line, and at 320 px each choice takes a line'),
              ('Parts', '24 px under the switch: rows at least 44 px tall with a hairline under each, and a strong line '
                        'after Act'),
              ('Current part', 'The selected band, the 4 px bar at its left edge, bold words and aria-current'),
              ('Opening', 'Focus to the current part’s link, or to Close the menu where no part is current'),
              ('Closing', 'Escape or Close the menu, with focus back to Menu and aria-expanded back to false; a part opens '
                          'its page'),
              ('Navigation name', '“Parts of the site, in the menu”')],
    'builders': ['Open the menu with <code>showModal()</code> and test it with the keyboard alone: Menu, Tab to the end, '
                 'Shift+Tab back, Escape.'],
    'correct_caption': 'The menu open over the article page at 390 and 360 px in the light theme and at 390 px in the '
                       'dark theme, with Explain on the selected band.',
    'correct_alt': 'Three phone screens with the menu open: Menu and Close the menu at the top, the theme switch under '
                   'them, and seven rows from Explain to Subscribe, Explain on a white band with a dark bar at its left. '
                   'The third screen is in the dark theme.',
    'failure_caption': '<strong>Fails Rule 20.2.</strong> The menu leaves the theme switch out, so on a phone a reader '
                       'cannot change the theme from any page.',
    'failure_alt': 'A phone menu with Menu and Close the menu at the top and seven rows under them, and no theme switch.',
}
R['20.3'] = {
    'title': 'Close every page with the same footer: the parts, help in one place, and the lockmark with the tagline.',
    'rule': ['Every page ends with the same footer. Four lists name the site again: our work by pillar, the atlas, Oath & '
             'Action, and Help, whose one link, Contact us, opens our contact page. Help keeps its place in that order on every '
             'page, the atlas’s pages included.',
             'Under the lists, a Charcoal strip closes the page with the lockmark at 24 px and the tagline on one line, '
             'and the web address after them.'],
    'why': 'A reader who gets stuck finds help where they found it last time, which matters most on the page where they '
           'are trying to take part. The lockmark closes the page in the footer, and since the masthead scrolls away, '
           'its lockmark and the footer’s never share a screen (Rule 08.2).',
    'basis': 'Rule 08.2; WCAG 2.2 SC 3.2.6, as the W3C’s page “Understanding Success Criterion 3.2.6: Consistent Help”, '
             'retrieved November 21, 2026, sets it; the web address shown as a stand-in, approved by our founder and '
             'editor on November 21, 2026',
    'specs': [('Ground', 'The lists on the page’s own ground, under a 2 px strong line; then the closing strip, Charcoal '
                         'in both themes and the footer’s one dark panel, with a 1 px hairline edge in the dark theme'),
              ('Space', '104 px above the footer and 48 px between its line and the lists; the strip 48 px under the '
                        'lists, with 56 px of padding above and below from 48em and 40 px on phones'),
              ('Lists', 'Four groups, each a heading in the label style and links in the small body style on 44 px rows; '
                        'four across from 48em, two by two on phones'),
              ('Help', 'The fourth group, with Contact us its first link, on every page'),
              ('Lockmark row', 'In the strip: the lockmark’s 24 px master, 12 px, and the tagline, on one line at the '
                               'left'),
              ('Web address', 'At the row’s right end from 48em, and on its own line under the row on phones, in the '
                              'caption style, with the Illustrative label until our address is settled'),
              ('Navigation name', '“Site map”, which differs from the masthead’s')],
    'builders': ['Draw the footer from one source for every page, and never move or rename the help link for one page.'],
    'correct_caption': 'The footer at 1440, 1024, 390 and 360 px in the light theme, and at 1440 px in the dark theme, '
                       'where a hairline edges its Charcoal strip.',
    'correct_alt': 'Five footers. Each shows four link groups, Our work, The atlas, Oath & Action and Help, then a '
                   'Charcoal strip with the lockmark, the tagline and the web address with its Illustrative label. On '
                   'the phones the groups sit two by two.',
    'failure_caption': '<strong>Fails Rule 20.3.</strong> Help moves and changes its words from one page to the next, so '
                       'a reader has to hunt for it on the page where they need it most.',
    'failure_alt': 'Two footers side by side. The home page’s ends its lists with Help and Contact us; the Act page’s has '
                   'no Help group and ends its Oath & Action list with Get in touch.',
    'fail_pages': ['Home page', 'Act page'],
    'fail_other': 'Get in touch',
}
R['20.4'] = {
    'title': 'Name every page in its title, and set its language in the markup.',
    'rule': ['Give every page a title that starts with its own words and ends with our name, as in “What a special '
             'district does | Oath & Action”. The home page leads with our name and the tagline. Set the language of '
             'every page on its root, as <code>lang="en"</code>.',
             'When a passage or phrase is in another language, mark the smallest element that holds it with its own '
             'language, and leave names and terms that English uses as they are, such as Regulations.gov or '
             'N-acetyl-L-cysteine.'],
    'why': 'A title is the first thing a screen reader says and the name a tab, a bookmark and a search result show, so a '
           'reader with ten tabs open can find this one. The language tells a screen reader how to pronounce the words '
           'and tells a browser which characters to draw.',
    'basis': 'WCAG 2.2 SC 2.4.2, 3.1.1 and 3.1.2, and Technique G88, as the W3C’s pages set them, retrieved November 21, '
             '2026',
    'specs': [('Title', 'The page’s headline, or a shorter form of it past about 60 characters, then a spaced vertical '
                        'bar and Oath & Action'),
              ('Home page', '“Oath & Action | A country that answers to its people.”'),
              ('Atlas pages', 'The view, then Who Do They Answer To?, then Oath & Action, each after a spaced vertical bar'),
              ('Language', '<code>lang="en"</code> on the root of every page'),
              ('Another language', 'Its own <code>lang</code> code on the smallest element that holds the passage; on a '
                                   'link or a button when the passage is its whole name; <code>hreflang</code> on a '
                                   'link to a page in another language'),
              ('Head, in order', 'Character set, viewport, title, color scheme, the head script that applies a stored '
                                 'theme, the stylesheet, the icons, the preview tags')],
    'builders': ['Write the title when you write the headline, and check it in a tab beside two other pages.'],
    'correct_caption': 'Three tabs a reader can tell apart, the head every page carries, and a phrase in another '
                       'language marked with its own.',
    'correct_alt': 'A browser’s tab strip with three titles: Oath & Action with the tagline, What a special district '
                   'does, and How to comment on the FDA’s proposed rule on NAC, each ending with Oath & Action. Under '
                   'it, the head of a page in code, and a sentence that marks the Latin motto E pluribus unum.',
    'tabs_label': 'Three pages in a browser',
    'head_label': 'The head of the article page',
    'lang_label': 'A phrase in another language',
    'lang_sentence': 'The motto on the Great Seal of the United States, {phrase}, is Latin for “out of many, one.”',
    'lang_phrase': 'E pluribus unum',
    'failure_caption': '<strong>Fails Rule 20.4.</strong> Every tab says Oath & Action, so a reader cannot tell the '
                       'explainer from the Act page without opening each one.',
    'failure_alt': 'A browser’s tab strip with three tabs that each read Oath & Action, and a page root with no language.',
}
R['20.5'] = {
    'title': 'Draw every page in the dark theme from the same markup, and keep each panel’s edge.',
    'rule': ['Every page follows the reader’s device at first and changes theme from the switch, with no second page and '
             'no second set of words. The dark theme sets Charcoal for the page and the matching value for every part.',
             'A dark panel keeps its Charcoal and draws a 1 px edge, so it still reads as a panel on a Charcoal page. '
             'Charts take the chart kit’s Charcoal drawing, and the identity marks take their paint for Charcoal.'],
    'why': 'One page in two themes keeps the words, links and order the same for every reader. Without an edge, a '
           'Charcoal panel on a Charcoal page disappears, and the section loses the signal that told the reader it had '
           'turned.',
    'basis': 'One dark theme for every screen product, with a visible switch that remembers the reader’s choice, approved '
             'by our founder and editor on November 10, 2026; Rules 18.4 and 26.6; design judgment for the edge',
    'specs': [('Themes', 'Light, dark, or the device’s, set on the page’s root and kept under the key '
                         '<code>oa-theme</code> (Rule 18.4)'),
              ('Panel edge', 'A 1 px hairline for Charcoal around each dark panel, the footer’s strip included; along '
                             'the top and foot only on the pillar row’s cells, which meet as one band at 1440 px'),
              ('Contrast', 'The edge, Stone on Charcoal, measures 3.10 to 1, past the 3 to 1 a boundary needs'),
              ('Charts', 'The chart kit’s Charcoal drawing in every dark frame'),
              ('Marks', 'L3, L1 and the lockmark take their paint for Charcoal, with signature red kept'),
              ('The switch', 'In the masthead from 64em, at the top of the menu under it')],
    'builders': ['Build the light page with the theme’s own token names only, then switch the theme and look for any '
                 'panel or mark that disappeared.'],
    'correct_caption': 'The home page’s first screen at 390 px in the light and the dark theme, from the same markup. On '
                       'the dark page each head cell of the pillar row keeps a 1 px edge along its top and foot.',
    'correct_alt': 'Two phone screens of the home page side by side, light and dark. Each shows the wordmark and Menu, '
                   'then the Explain cell on Charcoal and the explainer under it; on the dark screen thin lines above '
                   'and below set off the Charcoal cell.',
    'failure_caption': '<strong>Fails Rule 20.5.</strong> With no edge, the pillar cell melts into the dark page, and '
                       'only its icon and word show where the section begins.',
    'failure_alt': 'A phone screen in the dark theme where the Explain cell has no edge, so its icon and word float on '
                   'the page with nothing to show the cell.',
}

# ---- Group 2, three pages
R['20.6'] = {
    'title': 'Open the home page on one piece for each pillar, with the step a reader can take now.',
    'rule': ['The home page opens on the pillar row, with one piece under each pillar: an explainer, a tracker, a guide '
             'and a step a reader can take now. Each piece is a card with its kicker, headline, a few lines and its '
             'date. The Act card carries the take-part mark on its step and the view’s one red.',
             'Below them, the atlas’s section opens on its title bar, then lists the everyday questions it answers '
             'beside a chart and its source line.'],
    'why': 'A first-time reader sees in one screen what each pillar does and one thing they can do now. The pillar row is '
           'the order of our work, so it can order the page without a word of explanation.',
    'basis': 'Rules 01.21, 09.1, 09.4, 11.4, 11.5 and 11.9; design judgment for the layout',
    'specs': [('Pillar row', 'Each pillar section opens with its cell: Charcoal, the 48 px pillar icon in one color, its '
                             'word in the intro style, bold, and an arrow to the next; at 1440 px the four cells meet as '
                             'one band, at 1,024 px two to a line, and on phones one at the top of each section'),
              ('Cards', '309 px wide at 1440, 460 at 1,024, 350 at 390 and 328 at 360: kicker, headline in the H3 style, '
                        'a few lines in the small body style, and the date or “As of” line'),
              ('Trackers', 'Six circles at 24 px, 60 px apart, 57 px on the 309 px card; steps drawn only from the record'),
              ('The step', 'The take-part mark on step 3 of the rule, “You can take part now.” in bold, the deadline and '
                           'a text link at least 44 px tall'),
              ('The atlas', 'Its title bar on Charcoal, the section’s one dark panel; its questions on Newsprint, first '
                            'at every width; and chart S10, the atlas’s claims by evidence grade, whole with its source '
                            'line'),
              ('Title', '“Oath & Action | A country that answers to its people.”')],
    'builders': ['Choose the four pieces by pillar, then check that the Act card’s step is still open on the day the page '
                 'goes up.'],
    'correct_caption': 'The home page at 1440, 1024, 390 and 360 px in the light theme, and at 1440 and 390 px in the dark '
                       'theme. At 1,024 px the pillar row breaks after Track, two pillars to a line, as Rule 09.1 sets '
                       'it.',
    'correct_alt': 'The home page at six sizes. Under the masthead, the pillar row on Charcoal, Explain, Track, Connect '
                   'and Act, with a card under each: an explainer on special districts, a tracker for H.R. 7008, a guide '
                   'to who sets an electric bill, and a step to comment on the FDA’s proposed rule on NAC, its step '
                   'marked in red. Below, the atlas’s title bar on Charcoal, its questions beside a chart, then the '
                   'footer.',
    'failure_caption': '<strong>Fails Rule 20.6.</strong> The first screen opens on a slogan, so a reader learns nothing '
                       'they can use and finds no step to take.',
    'failure_alt': 'A desktop first screen with a Charcoal panel that reads Make your voice heard! and a Subscribe button, '
                   'and nothing else.',
    'fail_slogan': 'Make your voice heard!',
    'fail_button': 'Subscribe',
    'fail_note': 'Our fifth edition’s line, which Rule 02.19 retires',
}
R['20.7'] = {
    'title': 'Build an article from its question to its step, with the chart whole in its column.',
    'rule': ['An article opens with the compact pillar row, its kicker and a headline that answers the reader’s question, '
             'then an intro of two or three sentences and the byline. Its body runs at the reading measure, and a chart '
             'keeps all its parts, its source line and its table in the body’s column.',
             'The last section ends on a step the reader can take, and the last word carries ampersand B.'],
    'why': 'A reader who came with a question gets the answer in the headline and the evidence in the column they are '
           'already reading. Ending on a step tells them what to do with what they learned.',
    'basis': 'Rules 01.21, 02.8, 04.6, 07.3, 09.1 and 14.2; the counts from the Census Bureau’s 2022 Census of '
             'Governments',
    'specs': [('Pillar row', 'The 24 px row in the piece’s header, Explain bold and underlined, every icon in one color'),
              ('Headline', 'The title style, balanced: 110 px at 1440, 88.6 at 1,024 and 56 on phones'),
              ('Count panel', 'Charcoal, beside the intro from 64em and after it on phones: the figure in the figure '
                              'style, two lines on what it counts and the counts’ source line'),
              ('Body', 'Five of 12 columns at 1440 and seven at 1,024 (Rule 07.3)'),
              ('Fact box', 'Charcoal, beside the Count section’s first paragraph from 64em and after it on phones, its '
                           'source line under it on Newsprint'),
              ('Chart', 'S86, the count of governments by type, whole, six of 12 columns at 1440, each frame carrying '
                        'only the drawing its width shows'),
              ('Ending', 'The step on a Charcoal box, across the content width from 64em with its words in the body’s '
                         'columns: a link to another site with its mark, and B after the last word'),
              ('Title', '“What a special district does | Oath & Action”')],
    'builders': ['Write the step before you write the headline, then check that the last section still ends on it.'],
    'correct_caption': 'The article at 1440, 1024, 390 and 360 px in the light theme, and at 1440 and 390 px in the dark '
                       'theme. The count panel is the first screen’s one dark panel.',
    'correct_alt': 'The article What a special district does at six sizes: the compact pillar row with Explain '
                   'underlined, the kicker, the headline, the intro beside a Charcoal panel reading 39,555, the byline, '
                   'a section with a Charcoal fact box and chart S86, and a closing section whose step, on a Charcoal '
                   'box, points to the Census Bureau’s report on each state and ends on ampersand B.',
    'failure_caption': '<strong>Fails Rule 20.7.</strong> The article ends on a slogan, so a reader who wants to see '
                       'which districts their state has finishes with nowhere to go.',
    'failure_alt': 'The last lines of the article, ending on the line Put the promise to work. and ampersand B.',
    'fail_slogan': 'Put the promise to work.',
    'fail_note': 'Our fifth edition’s closing headline, which Rule 02.8 retires',
}
R['20.8'] = {
    'title': 'Build an Act page as a process piece that names who decides and by when, with one way to take part in red.',
    'rule': ['An Act page opens on the step and its date: what the agency proposes, who decides and when comments close, '
             'with the rule’s steps beside the opening and the ask under the step that is open. It quotes the agency’s '
             'own summary, sets out what the record shows from those who asked for the change and on the concern the law '
             'guards, at the length the record holds, and takes no side.',
             'After the hinge divider it lists how to comment, online and by mail, what becomes public and how to read '
             'other comments, and gives the ask again. The ask is a red link to the comment page that names the action '
             'and the place, with the docket number beside it, and the page says the day we checked its facts.'],
    'why': 'A reader of any view can use the page, because it tells them how to be heard and leaves what to say to them. '
           'Naming the place in the link tells a reader they are leaving our site before they press it.',
    'basis': 'Rules 01.22, 04.4, 11.4, 11.6, 11.9 and 11.15; the docket as the Federal Register and govinfo.gov printed '
             'it, retrieved November 21, 2026; the page’s subject approved by our founder and editor on November 21, '
             '2026',
    'specs': [('Opening', 'The 24 px pillar row with Act current, the kicker “Act · How to take part” alone, the headline '
                          'in the section style, the intro and “Checked November 21, 2026”'),
              ('Status panel', 'Charcoal, beside the opening from 64em: the rule’s six steps down the panel, 28 px '
                               'circles, step 3 with the take-part mark, and under it the deadline and the ask'),
              ('Document strip', 'Charcoal, across the content width from 64em, the section’s one dark panel: the '
                                 'agency, the docket, the citation and the date of the proposed rule'),
              ('Summary', 'On Newsprint under the strip: the agency’s summary word for word in the quotation style, a '
                          '2 px line at its left and its citation under it'),
              ('Who decides', 'One paragraph and chart S66, the steps of federal rule making, whole with its source '
                              'line'),
              ('Hinge divider', 'Before the steps to comment (Rule 04.4)'),
              ('The ask', 'A link that names the action and the place, “Comment at Regulations.gov”, on one line where '
                          'its panel gives it 304 px and in two phrases where it does not, as on phones, White '
                          'on Pillar Red in the ask style, 48 px tall at least, with the mark for another site and '
                          '“(another site)” for screen readers; on Charcoal, so it needs no keyline; the docket number '
                          'in the panel’s label above it'),
              ('The address', 'Printed in full under each ask, so a reader can copy it or read it on paper'),
              ('Red', 'One job, the step: the take-part mark and each ask; the two asks never share a screen'),
              ('Title', '“How to comment on the FDA’s proposed rule on NAC | Oath & Action”')],
    'builders': ['Check the docket on the day the page goes up and again the week it closes, and take the red away the '
                 'day comments close.'],
    'correct_caption': 'The Act page at 1440, 1024, 390 and 360 px in the light theme, and at 1440 and 390 px in the dark '
                       'theme. Its red does one job, the step: the take-part mark with the ask under it, and the ask '
                       'again after the instructions.',
    'correct_alt': 'The Act page at six sizes: the compact pillar row with Act underlined, the kicker Act, How to take '
                   'part, the headline How to comment on the FDA’s proposed rule on NAC, and a Charcoal panel of six '
                   'steps with step 3, Comments open, marked in red and a red link under it; then a Charcoal strip '
                   'naming the proposed rule with the FDA’s summary under it, chart S66, the hinge divider, the steps '
                   'to comment, a Charcoal panel with the deadline and the red link again, and the rule’s facts.',
    'failure_caption': '<strong>Fails Rule 20.8.</strong> “Take action” names no place, so a reader cannot tell where '
                       'the link leads or that it leaves our site.',
    'failure_alt': 'A Charcoal panel with the docket number and the deadline, and a red button that reads Take action.',
    'fail_ask': 'Take action',
}
R['20.9'] = {
    'title': 'Give each section one dark panel in its opening screen, and let running text stay Newsprint.',
    'rule': ['Measure a long page one screen at a time. The first screen and each section’s opening screen hold 60 to 85 '
             'percent Newsprint and at most one dark panel, and Pillar Red stays within 5 percent.',
             'Put each section’s dark panel where its opening screen needs it, and let the screens of running text '
             'between them hold more Newsprint.'],
    'why': 'A reader judges a page one screen at a time. A dark panel at the turn of each section tells them something new '
           'begins, and long stretches of reading stay calm on Newsprint.',
    'basis': 'Rule 05.1, with its sentence for long pages approved by our founder and editor on November 21, 2026; the '
             'application kit’s measure of each screen',
    'specs': [('Screens', '1440 by 900, 1024 by 768, 390 by 844 and 360 by 780 px'),
              ('Each first and opening screen', 'Newsprint 60 to 85 percent; one dark panel at most; Pillar Red within 5 '
                                                'percent, signature red included'),
              ('Sections', 'Marked in the markup, the footer its own'),
              ('A pixel', 'Counts as a color within 3 levels on each channel, or 24 for red'),
              ('Panels', 'Charcoal or Prussian, counted in the section where the panel’s top falls'),
              ('Dark frames', 'Shares printed for the record; only the red limit is judged')],
    'builders': ['Run the measure on every light frame before a page goes up, and move a panel before you add one.'],
    'correct_caption': 'Every first and opening screen of the three pages at 1440 px in the light theme, measured on the '
                       'application kit’s captures.',
    'correct_alt': 'Small boxes, one for each first and opening screen of the home page, the article and the Act page at '
                   '1440 px, each with its Charcoal panel drawn in place and its measured Newsprint, dark and red shares '
                   'beside it.',
    'failure_caption': '<strong>Fails Rule 20.9.</strong> With no panel in its first screen, our studio sample of this '
                       'article measured 88.2 percent Newsprint, past the 85 a screen allows.',
    'failure_alt': 'One screen drawn as a box, nearly all Newsprint, with the measure beside it: 88.2 percent Newsprint and '
                   'no dark panel.',
    'screen_words': {'first': 'first screen', 'news': 'Newsprint', 'dark': 'dark', 'red': 'red', 'panel': 'panel',
                     'panels': 'panels', 'none': 'no panel', 'pct': 'percent'},
    # each page and section named as a reader meets it, for the boxes in the correct plate
    'page_words': {'A06': 'Home page', 'A07': 'Article', 'A08': 'Act page'},
    'section_words': {'Explain': 'Explain', 'Track': 'Track', 'Connect': 'Connect', 'Act': 'Act',
                      'Atlas': 'Who Do They Answer To?', 'Count': 'How the Census Bureau counts them',
                      'Step': 'See which districts your state has', 'Proposal': 'What the FDA proposes',
                      'Comment': 'How to send a comment', 'Footer': 'footer'},
    'fail_value': '88.2',
    'fail_label': 'Studio sample article, 1440 px, first screen',
}

# ---- Group 3, beyond the page
R['20.10'] = {
    'title': 'Share every page as a 1200 by 630 card, its headline over a Charcoal foot that holds the sign-off.',
    'rule': ['Each page shares as a 1200 by 630 card on Newsprint: the page’s kicker in the H3 style, its headline at the '
             'title size, and a Charcoal foot that holds the wordmark at the left and the lockmark’s 96 px sign-off at '
             'the right.',
             'The card carries no web address until ours is settled, no deck and no icon, and its words go into the '
             'image’s alt text too.'],
    'why': 'A feed shows the card at about 500 px wide, so only the headline and the marks survive, and the sign-off at '
           '96 px keeps its lever red at that size. The foot puts the card in Rule 05.1’s range and gives every shared '
           'page the same signature in the same place.',
    'basis': 'Rule 08.2 and its feed test; the link-preview card in the identity proofs; the platform rows retrieved '
             'November 21, 2026; design judgment for the foot',
    'specs': [('Size', '1200 by 630 px, PNG'),
              ('Margin', '72 px'),
              ('Kicker', 'The H3 style at 32 px: the label in Charcoal, the topic in Deep Stone'),
              ('Headline', 'The title style at 110 px, two lines at most, balanced'),
              ('Foot', 'Charcoal, full width, 186 px tall: the wordmark’s display master, 44 px tall, at the left; the '
                       'lockmark’s 48 px master at twice its size, bottom right inside the margin'),
              ('Feed test', 'Rule 08.2’s test for a dark card, at 500 and 360 px wide'),
              ('Tags', 'og:image with its width, height and alt; twitter:card summary_large_image with its alt')],
    'builders': ['Write the headline for the card first: if it runs to three lines at 110 px, the editor shortens it for '
                 'the card alone.'],
    'correct_caption': 'The article’s share preview at full size and at the two widths a feed shows it.',
    'correct_alt': 'A Newsprint card reading Explainer, Local government, and the headline What a special district does, '
                   'with a Charcoal foot holding the wordmark and the lockmark, shown at full size and at two feed sizes.',
    'failure_caption': '<strong>Fails Rule 20.10.</strong> At 48 px the sign-off loses its lever’s red once a feed '
                       'shrinks the card to 360 px; Rule 08.2 counted no red pixel left on our card.',
    'failure_alt': 'The same card with a small lockmark in its foot, half the size of the sign-off.',
}
R['20.11'] = {
    'title': 'Draw the favicon from ampersand B’s 16 px master, and the app icons from B on the Charcoal tile.',
    'rule': ['The browser tab shows ampersand B from its 16 px master, with no tile, in signature red. The home screen and '
             'app icons show B on the Charcoal square at 58 percent of the tile.',
             'Never use the lockmark or the wordmark as a favicon.'],
    'why': 'At 16 px, B holds its shape and reads as ours on a light or a dark tab. The lockmark’s nine nodes run together '
           'at that size.',
    'basis': 'Rules 04.7 and 08.2; ampersand B alone on the Charcoal tile for avatars and the app icon, approved by our '
             'founder and editor on November 7, 2026; the platform rows retrieved November 21, 2026',
    'specs': [('SVG favicon', 'B’s 16 px master in a 16 by 16 view, no tile, declared for every size'),
              ('favicon.ico', '16, 32 and 48 px in one file'),
              ('Apple touch icon', '180 by 180 px, B on the Charcoal square'),
              ('Manifest icons', '192 and 512 px; the 512 px icon maskable, with B inside the circle of 40 percent of its '
                                 'width'),
              ('Head', 'One link for each, and a manifest that names the two manifest icons')],
    'builders': ['Look at the favicon at 16 px on a dark tab before you ship it.'],
    'correct_caption': 'The favicon on a light and a dark tab, and each icon file at its own size.',
    'correct_alt': 'Ampersand B in red at 16 px on a light and a dark browser tab, then the favicon file at 16, 32 and 48 '
                   'px, and B on a Charcoal square at 180, 192 and 512 px.',
    'failure_caption': '<strong>Fails Rule 20.11.</strong> The lockmark at 16 px shrinks to a cluster of dots in the tab, '
                       'too small to read as our mark.',
    'failure_alt': 'A browser tab with the lockmark at 16 px as its icon, a small cluster of dots, before the page title.',
}
EXTRA_FILES = {
    'label': 'The pages and their files',
    'caption': 'Each page, preview and icon this chapter shows, as a file in our exports, with its size.',
    'head': ['Application', 'File', 'Size'],
    'alt': 'A table of the chapter’s export files: each application, its file name and its pixel size.',
    'apps': {'A04': 'Masthead and menu', 'A05': 'Footer', 'A06': 'Home page', 'A07': 'Article page', 'A08': 'Act page',
             'A09': 'Share preview', 'A10': 'Favicon set'},
    'size_words': {'px': '{w} by {h} px', 'ico': '{sizes} px', 'svg': 'Any size', 'html': 'A working page'},
}

# the line above each row of frames: the width, the theme and the state each frame shows
VIEW_WORDS = {'1440-light': '1440 px, light', '1024-light': '1024 px, light', '390-light': '390 px, light',
              '360-light': '360 px, light', '1440-dark': '1440 px, dark', '390-dark': '390 px, dark',
              '390-light-open': '390 px, light, menu open', '360-light-open': '360 px, light, menu open',
              '390-dark-open': '390 px, dark, menu open', '1440-light-screen': '1440 px, light, first screen',
              '390-light-screen': '390 px, light, first screen', '390-dark-screen': '390 px, dark, first screen'}

WCAG = {
    '20.1': ['1.3.1', '2.4.1', '2.4.3', '3.2.3', '3.2.4', '4.1.2'],
    '20.2': ['2.1.1', '2.1.2', '2.4.3', '2.4.7', '2.4.11', '2.5.3', '2.5.8', '4.1.2'],
    '20.3': ['3.2.6', '3.2.3', '3.2.4', '2.5.8'],
    '20.4': ['2.4.2', '3.1.1', '3.1.2 (the markup)'],
    '20.5': ['1.4.3', '1.4.11', '3.2.2', '3.2.3', '4.1.2'],
    '20.6': ['1.3.1', '1.4.1', '1.4.10', '2.4.6'],
    '20.7': ['1.1.1', '1.3.1', '1.4.1', '1.4.4', '1.4.10', '1.4.12', '2.4.6'],
    '20.8': ['1.4.1', '1.4.3', '2.4.4', '2.5.8', '3.2.5'],
}
TOKENS = {
    '20.1': ['oa.type.ui', 'oa.color.surface', 'oa.color.text.primary', 'oa.color.border.hairline', 'oa.border.width.rule',
             'oa.size.target.touch'],
    '20.2': ['oa.color.surface', 'oa.color.border.strong', 'oa.color.state.selected.band', 'oa.color.state.selected.bar',
             'oa.border.width.bar', 'oa.size.target.touch'],
    '20.3': ['oa.color.surface.charcoal', 'oa.color.text.primary.onCharcoal', 'oa.color.text.secondary.onCharcoal',
             'oa.color.border.hairline.onCharcoal', 'oa.color.identity.signature.onCharcoal', 'oa.type.label',
             'oa.type.bodySmall', 'oa.type.caption'],
    '20.4': ['oa.type.bodySmall', 'oa.type.caption'],
    '20.5': ['oa.color.surface', 'oa.color.border.hairline.onCharcoal', 'oa.color.text.primary.onCharcoal',
             'oa.color.identity.signature.onCharcoal'],
    '20.6': ['oa.type.intro', 'oa.type.h3', 'oa.type.bodySmall', 'oa.type.label', 'oa.type.caption', 'oa.type.section',
             'oa.size.icon.large', 'oa.color.surface.charcoal'],
    '20.7': ['oa.type.title', 'oa.type.intro', 'oa.type.h3', 'oa.type.body', 'oa.type.figure', 'oa.type.caption',
             'oa.layout.measure.bodyIdeal'],
    '20.8': ['oa.type.section', 'oa.type.intro', 'oa.type.quote', 'oa.type.ask', 'oa.color.action.ask.fill.onCharcoal',
             'oa.color.action.ask.label.onCharcoal', 'oa.color.identity.hingeDivider'],
    '20.9': ['oa.color.surface.newsprint', 'oa.color.surface.charcoal', 'oa.color.palette.pillarRed'],
    '20.10': ['oa.type.title', 'oa.type.h3', 'oa.color.surface.newsprint', 'oa.color.surface.charcoal',
              'oa.color.identity.signature.onCharcoal'],
    '20.11': ['oa.component.appIcon.tile', 'oa.color.identity.signature'],
}
RELATED = {
    '20.1': (['03', '08', '18'], ['03.6', '08.2', '18.4', '18.6', '18.7', '20.2', '20.5']),
    '20.2': (['18'], ['18.4', '18.6', '18.7', '18.8', '20.1']),
    '20.3': (['08', '13', '18'], ['08.1', '08.2', '13.8', '18.5', '20.1']),
    '20.4': (['02', '18', '19', '26'], ['18.12', '20.10', '20.11', '26.6']),
    '20.5': (['05', '18', '26'], ['05.1', '18.4', '20.1', '20.2', '26.6']),
    '20.6': (['01', '05', '09', '11', '14'], ['01.21', '05.1', '05.3', '09.1', '09.4', '11.4', '11.5', '11.9', '20.9']),
    '20.7': (['01', '04', '07', '09', '14'], ['01.21', '04.6', '07.3', '09.1', '14.2', '14.13', '20.9']),
    '20.8': (['01', '04', '11', '18'], ['01.22', '04.4', '11.4', '11.6', '11.9', '11.15', '18.5', '20.6']),
    '20.9': (['05'], ['05.1', '05.3', '20.6', '20.7', '20.8']),
    '20.10': (['01', '05', '08'], ['01.21', '05.1', '08.2', '16.3', '16.4']),
    '20.11': (['03', '04', '08'], ['03.4', '04.1', '04.7', '08.2', '20.4']),
}


# ================================================================================================ LAYOUT
def ty(name):
    return ctx.ty(name)


BASE = (
    f'.w{{{ty("body")};color:var(--oa-color-text-primary);max-width:100%}}.w p{{margin:0}}.w *{{box-sizing:border-box}}'
    f'.lab{{{ty("label")};margin:0 0 12px}}.sec{{color:var(--oa-color-text-secondary)}}'
    f'.sm{{{ty("bodySmall")}}}.cap{{{ty("caption")};color:var(--oa-color-text-secondary)}}'
    '.mt8{margin-top:8px}.mt16{margin-top:16px}.mt24{margin-top:24px}.mt32{margin-top:32px}'
    '.row{display:flex;flex-wrap:wrap;gap:24px 32px;align-items:flex-start}'
    '.dk{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal)}'
    '.dk .sec,.dk .cap{color:var(--oa-color-text-secondary-on-charcoal)}'
    '.ui{display:block;flex:none;fill:none;stroke:currentColor;stroke-width:var(--oa-component-icon-utility-line-medium);'
    'stroke-linecap:round;stroke-linejoin:round}'
    '.mk{display:inline-block;line-height:0;flex:none}'
)


def css(extra=''):
    return f'<style>{BASE}{extra}</style>'


# style pruning, as chapters 16 and 17 do: a specimen carries only the rules its classes use
def _split_top(sel):
    parts, depth, cur = [], 0, ''
    for c in sel:
        depth += {'(': 1, '[': 1, ')': -1, ']': -1}.get(c, 0)
        if c == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += c
    return parts + [cur]


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
            keep = [p for p in _split_top(sel) if all(c in used for c in re.findall(r'\.([A-Za-z][\w-]*)', p))]
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


def uicon(name, px=24):
    return (f'<svg class="ui" viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" focusable="false" '
            f'data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"/></svg>')


def master(path, w, h, style, red='signature', alt=''):
    """An identity master the build inlines from its file (the identity proofs' pattern), its paint set by token. A mark
    in the text's ink (the end mark) carries no data-red."""
    dr = f' data-red="{red}"' if red else ''
    return (f'<span class="mk"{dr}><img data-inline src="{path}" alt="{alt}" width="{w}" height="{h}" '
            f'style="{style}"></span>')


AMP16 = 'work/build/assets/identity/ampersand/20261028_Amp-B-16px-Master.svg'
AMP_DISPLAY = 'work/build/assets/identity/ampersand/20261028_Amp-B-Display-Master.svg'
LOCK16 = 'work/build/assets/identity/lockmark/20261028_Lockmark-16px-Master.svg'
LOCK48 = 'work/build/assets/identity/lockmark/20261109_Lockmark-48px-Master-Outline.svg'
WM_DISPLAY = 'work/build/assets/identity/wordmark/20261028_Wordmark-Display-Master.svg'
INK_NEWS = ('color:var(--oa-color-text-primary-on-newsprint);--amp:var(--oa-color-identity-signature-on-newsprint);'
            '--lever:var(--oa-color-identity-signature-on-newsprint);--link:var(--oa-color-palette-stone);'
            '--line:var(--oa-color-palette-stone)')
INK_CHAR = ('color:var(--oa-color-text-primary-on-charcoal);--amp:var(--oa-color-identity-signature-on-charcoal);'
            '--lever:var(--oa-color-identity-signature-on-charcoal);--link:var(--oa-color-text-primary-on-charcoal);'
            '--line:var(--oa-color-text-primary-on-charcoal)')


def spec(sid, html, rule, alt, **kw):
    kw.setdefault('readable', True)
    ctx.spec(sid, prune(html), CH, rule, alt, **kw)
    return sid


def app(aid, views=None):
    """The kit's placeholder (contract C4). The guide build sets the kit's frames in its place."""
    v = f' data-oa-app-views="{views}"' if views else ''
    return f'<div data-oa-app="{aid}"{v}></div>'


# Frames named in one placeholder share one row at one scale (the engineer's C4), so each plate sets its rows: a wide
# page alone in its row, the phones side by side
PAGE_ROWS = [['1440-light'], ['1024-light'], ['390-light', '360-light', '390-dark'], ['1440-dark']]
BAR_ROWS = [['1440-light'], ['1440-dark'], ['1024-light'], ['390-light', '360-light', '390-dark']]
FOOT_ROWS = [['1440-light'], ['1440-dark'], ['1024-light'], ['390-light', '360-light']]
ROWS_CSS = '.rw2+.rw2{margin-top:32px}'


def rows(aid, layout):
    """One placeholder a row, each under a line naming its views."""
    return ''.join(f'<div class="rw2"><p class="lab sec">{" · ".join(VIEW_WORDS[v] for v in r)}</p>{app(aid, " ".join(r))}</div>'
                   for r in layout)


# ------------------------------------------------------------------------------------------------ the plates
def s_opener():
    html = css(ROWS_CSS) + f'<div class="w">{rows("A06", [["1440-light-screen"], ["390-dark-screen"]])}</div>'
    return spec('s-20-opener', html, None, W['opener_alt'],
                notes='Drawn by the application kit (A06, the home page): its first screen at 1440 px light and 390 px '
                      'dark, one window tall each.')


# 20.1
def s20_1_correct():
    r = R['20.1']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A04", BAR_ROWS)}</div>'
    return spec('s-20-1-correct', html, '20.1', r['correct_alt'],
                notes='Drawn by the application kit (A04): the masthead closed at six views, on the article page.')


FAIL_BAR = (f'.bar{{display:flex;flex-wrap:wrap;align-items:center;justify-content:flex-end;gap:8px 16px;padding:18px 24px;'
            f'background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);'
            f'border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint);{ty("ui")}}}'
            '.bar span{display:inline-flex;align-items:center;min-height:44px}'
            '.bar .dv{width:1px;height:20px;min-height:0;background:var(--oa-color-border-hairline-on-newsprint)}'
            f'.bar .redb{{padding:8px 16px;background:var(--oa-color-action-ask-fill-on-newsprint);'
            f'color:var(--oa-color-action-ask-label-on-newsprint);{ty("ask")};box-shadow:inset 0 0 0 1px '
            'var(--oa-color-palette-charcoal)}')


def s20_1_failure():
    r = R['20.1']
    parts = [p for p, _ in SITE['parts']]
    items = ''.join(f'<span>{p}</span>' for p in parts[:4]) + '<span class="dv" aria-hidden="true"></span>' + ''.join(
        f'<span>{p}</span>' for p in parts[4:6])
    html = (css(FAIL_BAR) + f'<div class="w"><p class="lab sec">{r["fail_label"]}</p><div class="bar">{items}'
            f'<span class="redb" data-red="working">{parts[6]}</span></div></div>')
    return spec('s-20-1-failure', html, '20.1', r['failure_alt'],
                notes='A drawing of a fault: Subscribe as a red button, with the ask’s fill and label tokens.')


# 20.2
def s20_2_correct():
    r = R['20.2']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A04", [["390-light-open", "360-light-open", "390-dark-open"]])}</div>'
    return spec('s-20-2-correct', html, '20.2', r['correct_alt'],
                notes='Drawn by the application kit (A04): the menu open, one window tall, at three views.')


FAIL_MENU = ('.menu{width:390px;max-width:100%;padding:0 20px 24px;background:var(--oa-color-surface-newsprint);'
             'color:var(--oa-color-text-primary-on-newsprint);border:1px solid var(--oa-color-border-hairline-on-newsprint)}'
             '.mh{display:flex;align-items:center;justify-content:space-between;min-height:56px;'
             'border-bottom:1px solid var(--oa-color-border-strong-on-newsprint)}'
             f'.mt{{{ty("ui")};font-weight:var(--oa-font-weight-bold)}}'
             f'.cl{{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 17px 8px 13px;'
             f'border:1px solid var(--oa-color-border-strong-on-newsprint);{ty("ui")}}}'
             f'.rw{{display:flex;align-items:center;min-height:44px;padding:8px 12px;{ty("ui")};'
             'border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}'
             '.rw.cur{padding-left:8px;background:var(--oa-color-state-selected-band-on-newsprint);'
             'border-left:4px solid var(--oa-color-state-selected-bar-on-newsprint);font-weight:var(--oa-font-weight-bold)}'
             '.rw.grp{border-bottom-color:var(--oa-color-border-strong-on-newsprint)}'
             '.list{margin-top:24px}')


def s20_2_failure():
    r = R['20.2']
    m = SITE['menu']
    rows = ''.join(f'<div class="rw{" cur" if i == 0 else ""}{" grp" if i == 3 else ""}">{p}</div>'
                   for i, (p, _) in enumerate(SITE['parts']))
    html = (css(FAIL_MENU) + f'<div class="w"><div class="menu"><div class="mh"><span class="mt">{m["title"]}</span>'
            f'<span class="cl">{uicon("close")}<span>{m["close"]}</span></span></div><div class="list">{rows}</div></div></div>')
    return spec('s-20-2-failure', html, '20.2', r['failure_alt'], width=390,
                notes='A drawing of a fault: chapter 18’s menu rows with the theme switch left out.')


# 20.3
def s20_3_correct():
    r = R['20.3']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A05", FOOT_ROWS)}</div>'
    return spec('s-20-3-correct', html, '20.3', r['correct_alt'],
                notes='Drawn by the application kit (A05): the footer at five views.')


FAIL_FOOT = ('.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,16rem),1fr));gap:24px}'
             '.ft{padding:24px 20px 20px}.ft .g{margin-top:16px}'
             f'.ft .gh{{{ty("label")};color:var(--oa-color-text-secondary-on-charcoal)}}'
             f'.ft .ln{{{ty("bodySmall")};padding-top:6px}}.ft .ln.hit{{font-weight:var(--oa-font-weight-bold)}}')


def s20_3_failure():
    r = R['20.3']
    g = SITE['footer']['groups']

    def foot(groups):
        return '<div class="ft dk">' + ''.join(
            f'<div class="g"><p class="gh">{h}</p>' + ''.join(
                f'<p class="ln{" hit" if w in ("Contact us", r["fail_other"]) else ""}">{w}</p>' for w, _ in links)
            + '</div>' for h, links in groups) + '</div>'
    act = [g[0], g[1], [g[2][0], g[2][1] + [[r['fail_other'], '/contact']]]]
    html = (css(FAIL_FOOT) + '<div class="w"><div class="pair">'
            f'<div><p class="lab sec">{r["fail_pages"][0]}</p>{foot(g)}</div>'
            f'<div><p class="lab sec">{r["fail_pages"][1]}</p>{foot(act)}</div></div></div>')
    return spec('s-20-3-failure', html, '20.3', r['failure_alt'],
                notes='A drawing of a fault: two footers whose help link moves and changes its words; the help links are '
                      'set in bold here only so the fault can be found.')


# 20.4
TABS = ('.tabs{display:flex;flex-wrap:wrap;gap:0;background:var(--oa-color-surface-white);'
        'border:1px solid var(--oa-color-border-hairline-on-white);padding:8px 8px 0}'
        f'.tab{{display:flex;align-items:center;gap:8px;min-width:0;max-width:16rem;padding:8px 12px;{ty("caption")};'
        'color:var(--oa-color-text-primary-on-white);border:1px solid var(--oa-color-border-hairline-on-white);'
        'border-bottom:0;margin-right:4px;background:var(--oa-color-surface-white)}'
        '.tab .t{overflow:hidden;white-space:nowrap;text-overflow:ellipsis}'
        '.code{margin:0;padding:16px;white-space:pre-wrap;overflow-wrap:anywhere;'
        f'{ty("caption")};font-variant-numeric:tabular-nums;border:1px solid var(--oa-color-border-strong);'
        'background:var(--oa-color-field-ground)}'
        '.block{margin-top:32px}')


def tab(title, icon_path=AMP16, w=14, h=16):
    style = 'color:var(--oa-color-palette-pillar-red)' if icon_path == AMP16 else INK_NEWS.replace('-on-newsprint', '-on-white')
    return f'<span class="tab">{master(icon_path, w, h, style)}<span class="t">{_html.escape(title, quote=False)}</span></span>'


def head_code():
    a = PAGES['A07']
    lines = ['<!doctype html>', '<html lang="en">', '<head>', '  <meta charset="utf-8">',
             '  <meta name="viewport" content="width=device-width, initial-scale=1">',
             f'  <title>{a["title"]}</title>', '  <meta name="color-scheme" content="light dark">',
             '  <script>/* applies a stored theme before the first paint (Rule 26.6) */</script>',
             '  <link rel="stylesheet" href="/site.css">',
             '  <link rel="icon" href="/favicon.svg" type="image/svg+xml">',
             '  <link rel="icon" href="/favicon.ico" sizes="16x16 32x32 48x48">',
             '  <link rel="apple-touch-icon" href="/apple-touch-icon.png">',
             '  <link rel="manifest" href="/site.webmanifest">',
             f'  <meta property="og:title" content="{a["headline"]}">',
             '  <meta property="og:image" content="/share/special-districts.png">',
             '  <meta property="og:image:width" content="1200">', '  <meta property="og:image:height" content="630">',
             f'  <meta property="og:image:alt" content="{PAGES["A09"]["alt"]}">',
             '  <meta name="twitter:card" content="summary_large_image">', '</head>']
    return '\n'.join(x.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
                     for x in lines)


def s20_4_correct():
    r = R['20.4']
    titles = [PAGES['A06']['title'], PAGES['A07']['title'], PAGES['A08']['title']]
    phrase = r['lang_phrase']
    sentence = r['lang_sentence'].replace('{phrase}', f'<i lang="la">{phrase}</i>')
    code_line = ('&lt;p&gt;' + r['lang_sentence'].replace('{phrase}', f'&lt;i lang=&quot;la&quot;&gt;{phrase}&lt;/i&gt;')
                 + '&lt;/p&gt;')
    html = (css(TABS) + f'<div class="w"><p class="lab sec">{r["tabs_label"]}</p><div class="tabs">'
            + ''.join(tab(t) for t in titles) + '</div>'
            f'<div class="block"><p class="lab sec">{r["head_label"]}</p><pre class="code">{head_code()}</pre></div>'
            f'<div class="block"><p class="lab sec">{r["lang_label"]}</p><p>{sentence}</p>'
            f'<pre class="code mt16">{code_line}</pre></div></div>')
    return spec('s-20-4-correct', html, '20.4', r['correct_alt'],
                notes='The titles are the pages’ own, from this generator’s PAGES words, which the kit prints in each '
                      'page’s head. The Latin motto is marked with lang="la" in this plate’s own markup too.')


def s20_4_failure():
    r = R['20.4']
    code = '&lt;html&gt;\n&lt;head&gt;\n  &lt;title&gt;Oath &amp;amp; Action&lt;/title&gt;'
    html = (css(TABS) + f'<div class="w"><div class="tabs">' + ''.join(tab('Oath & Action') for _ in range(3))
            + f'</div><pre class="code mt16">{code}</pre></div>')
    return spec('s-20-4-failure', html, '20.4', r['failure_alt'], notes='A drawing of a fault: three identical titles.')


# 20.5
def s20_5_correct():
    r = R['20.5']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A06", [["390-light-screen", "390-dark-screen"]])}</div>'
    return spec('s-20-5-correct', html, '20.5', r['correct_alt'],
                notes='Drawn by the application kit (A06): the home page’s first screen at 390 px in both themes.')


FAIL_DARK = ('.ph{width:390px;max-width:100%;padding:0 20px 32px}'
             '.top{display:flex;align-items:center;justify-content:space-between;min-height:56px;'
             'border-bottom:1px solid var(--oa-color-border-hairline-on-charcoal);margin:0 -20px;padding:0 20px}'
             f'.mn{{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:8px 17px 8px 13px;'
             f'border:1px solid var(--oa-color-border-strong-on-charcoal);{ty("ui")}}}'
             '.cell{display:flex;align-items:center;gap:12px;margin-top:32px;padding:20px;'
             'background:var(--oa-color-surface-charcoal)}'
             f'.cell .wd{{{ty("intro")};font-weight:var(--oa-font-weight-bold)}}'
             '.pil{width:48px;height:48px;color:var(--oa-color-text-primary-on-charcoal)}'
             f'.kk{{{ty("label")};margin-top:24px}}.hl{{{ty("h3")};margin-top:16px;text-wrap:balance}}'
             f'.dek{{{ty("bodySmall")};margin-top:12px;color:var(--oa-color-text-primary-on-charcoal)}}')


def s20_5_failure():
    r = R['20.5']
    p = PAGES['A06']['pillars'][0]
    wm = master('work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg', 221, 24, INK_CHAR)
    pil = (f'<svg class="pil" viewBox="0 0 48 48" width="48" height="48" aria-hidden="true" focusable="false" '
           f'data-icon="CL-019" data-icon-family="pillar"><use href="#oa-sym-{p["icon"]}"/></svg>')
    html = (css(FAIL_DARK) + f'<div class="w"><div class="ph dk"><div class="top">{wm}<span class="mn">{uicon("menu")}'
            f'<span>{SITE["menu"]["button"]}</span></span></div><div class="cell">{pil}<span class="wd">{p["word"]}</span></div>'
            f'<p class="kk">{p["kicker"][0]} <span class="sec">· {p["kicker"][1]}</span></p><p class="hl">{p["headline"]}</p>'
            f'<p class="dek">{p["dek"]}</p></div></div>')
    return spec('s-20-5-failure', html, '20.5', r['failure_alt'], width=390, surface='charcoal',
                notes='A drawing of a fault: the dark home page’s first screen with the cell’s edge left off.')


# 20.6 to 20.8, the three pages
def s20_6_correct():
    r = R['20.6']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A06", PAGE_ROWS)}</div>'
    return spec('s-20-6-correct', html, '20.6', r['correct_alt'], notes='Drawn by the application kit (A06): six views.')


FAIL_HERO = ('.scr{max-width:720px;border:1px solid var(--oa-color-border-hairline-on-newsprint);'
             'background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint)}'
             '.mh{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;'
             'border-bottom:1px solid var(--oa-color-border-hairline-on-newsprint)}'
             '.hero{margin:24px 20px 32px;padding:48px 32px}'
             f'.sl{{{ty("section")};text-wrap:balance}}'
             f'.btn{{display:inline-flex;align-items:center;min-height:44px;margin-top:32px;padding:8px 20px;'
             f'background:var(--oa-color-action-primary-fill-on-charcoal);color:var(--oa-color-action-primary-label-on-charcoal);{ty("ui")}}}')


def s20_6_failure():
    r = R['20.6']
    wm = master('work/build/assets/identity/wordmark/20261028_Wordmark-24px-Master.svg', 221, 24, INK_NEWS)
    html = (css(FAIL_HERO) + f'<div class="w"><div class="scr"><div class="mh">{wm}</div><div class="hero dk">'
            f'<p class="sl">{r["fail_slogan"]}</p><span class="btn">{r["fail_button"]}</span></div></div>'
            f'<p class="cap mt8">{r["fail_note"]}</p></div>')
    return spec('s-20-6-failure', html, '20.6', r['failure_alt'],
                notes='A drawing of a fault: a first screen that opens on a slogan with no piece and no step.')


def s20_7_correct():
    r = R['20.7']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A07", PAGE_ROWS)}</div>'
    return spec('s-20-7-correct', html, '20.7', r['correct_alt'], notes='Drawn by the application kit (A07): six views.')


FAIL_END = (f'.end{{max-width:34rem}}.end p{{{ty("body")}}}.end p+p{{margin-top:16px}}'
            '.em{white-space:nowrap}.em .mk{margin-left:.5em;vertical-align:-.052em}')


def s20_7_failure():
    r = R['20.7']
    body = PAGES['A07']['sections'][0]['blocks'][2]['p']
    b = master(AMP16, 14, 16, 'color:currentColor;height:.831em;width:auto', red=None)
    html = (css(FAIL_END) + f'<div class="w"><div class="end"><p>{body}</p>'
            f'<p><span class="em">{r["fail_slogan"]}{b}</span></p></div><p class="cap mt8">{r["fail_note"]}</p></div>')
    return spec('s-20-7-failure', html, '20.7', r['failure_alt'],
                notes='A drawing of a fault: the article’s last paragraph, then a slogan in place of the step.')


def s20_8_correct():
    r = R['20.8']
    html = css(ROWS_CSS) + f'<div class="w">{rows("A08", PAGE_ROWS)}</div>'
    return spec('s-20-8-correct', html, '20.8', r['correct_alt'], notes='Drawn by the application kit (A08): six views.')


FAIL_ASK = ('.pn{max-width:40rem;padding:32px}'
            f'.pn .pl{{{ty("label")};color:var(--oa-color-text-secondary-on-charcoal)}}'
            f'.pn .dl{{{ty("h4")};margin-top:8px}}'
            f'.ask{{display:inline-flex;align-items:center;min-height:48px;margin-top:24px;padding:12px 20px;'
            f'background:var(--oa-color-action-ask-fill-on-charcoal);color:var(--oa-color-action-ask-label-on-charcoal);'
            f'{ty("ask")}}}')


def s20_8_failure():
    r = R['20.8']
    c = PAGES['A08']['comment']
    html = (css(FAIL_ASK) + f'<div class="w"><div class="pn dk"><p class="pl">{c["panel_label"]}</p>'
            f'<p class="dl">{c["deadline"]}</p><span class="ask" data-red="working">{r["fail_ask"]}</span></div></div>')
    return spec('s-20-8-failure', html, '20.8', r['failure_alt'],
                notes='A drawing of a fault: the comment panel with an ask that names no docket and no place.')


# 20.9, color screen by screen: drawn from the kit's own measure (contract C5)
SCR = ('.strips{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,13rem),1fr));gap:24px 32px}'
       '.scb{display:flex;flex-direction:column;gap:8px}'
       '.box{position:relative;aspect-ratio:1440/900;border:1px solid var(--oa-color-border-strong);'
       'background:var(--oa-color-surface-newsprint);overflow:hidden}'
       '.box .pnl{position:absolute;background:var(--oa-color-surface-charcoal)}'
       f'.fig{{{ty("h4")};font-variant-numeric:tabular-nums}}.sub{{{ty("caption")};color:var(--oa-color-text-secondary)}}')


def screens():
    """Each first and opening screen of A06 to A08 at 1440 px light, from the plates the kit writes (C5's measure)."""
    out = []
    for aid in ('A06', 'A07', 'A08'):
        f = KIT_PLATES / f'{aid.lower()}.json'
        if not f.exists():
            return None
        plate = json.loads(f.read_text())
        view = next((v for v in plate.get('views', []) if v.get('key') == '1440-light'), None)
        if not view or not view.get('screens'):
            return None
        out.append((aid, view['screens']))
    return out


def s20_9_correct():
    r = R['20.9']
    sw = r['screen_words']
    data = screens()
    if data is None:
        raise Waiting('Rule 20.9’s correct plate needs the kit’s screen shares (C5) in plates/a06.json to a08.json')
    def nm(names):
        return ', '.join(r['section_words'].get(x.strip(), x.strip()) for x in names.split(','))
    cells = []
    for aid, scr0 in data:
        # sections that open on the same screen (the home page's four pillars at 1440 px) share one box
        scr = []
        for s in scr0:
            if scr and (scr[-1]['newsprint'], scr[-1]['dark'], scr[-1]['red']) == (s['newsprint'], s['dark'], s['red']) \
                    and s['name'] != 'first' and scr[-1]['name'] != 'first':
                scr[-1] = {**scr[-1], 'name': scr[-1]['name'] + ', ' + s['name'],
                           'panels': scr[-1].get('panels', 0) + s.get('panels', 0),
                           'panels_box': scr[-1].get('panels_box', []) + s.get('panels_box', [])}
            else:
                scr.append(s)
        for s in scr:
            pn = ''.join(f'<span class="pnl" style="left:{p["x"]:.2f}%;top:{p["y"]:.2f}%;width:{p["w"]:.2f}%;'
                         f'height:{p["h"]:.2f}%"></span>' for p in s.get('panels_box', []))
            n = s.get('panels', 0)
            cells.append(f'<div class="scb"><div class="box" aria-hidden="true">{pn}</div>'
                         f'<p class="sub">{r["page_words"][aid]}, {sw["first"] if s["name"] == "first" else nm(s["name"])}</p>'
                         f'<p class="fig">{s["newsprint"]:.1f} {sw["pct"]} {sw["news"]}</p>'
                         f'<p class="sub">{s["dark"]:.1f} {sw["dark"]}, {s["red"]:.1f} {sw["red"]}; '
                         f'{sw["none"] if n == 0 else (str(n) + " " + (sw["panel"] if n == 1 else sw["panels"]))}</p></div>')
    html = css(SCR) + f'<div class="w"><div class="strips">{"".join(cells)}</div></div>'
    return spec('s-20-9-correct', html, '20.9', r['correct_alt'],
                notes='Each screen’s shares and panels are read from the kit’s plates, measured on its captures (C5).')


def s20_9_failure():
    r = R['20.9']
    sw = r['screen_words']
    html = (css(SCR) + f'<div class="w"><div class="scb" style="max-width:20rem"><div class="box" aria-hidden="true"></div>'
            f'<p class="sub">{r["fail_label"]}</p><p class="fig">{r["fail_value"]} {sw["pct"]} {sw["news"]}</p>'
            f'<p class="sub">{sw["none"]}</p></div></div>')
    return spec('s-20-9-failure', html, '20.9', r['failure_alt'],
                notes='The figure is the chat 10 sample’s measure (D4-11), the first screen alone.')


# The extra: the pages and their files, from the kit's exports manifest
FILES = (f'.tb{{border-collapse:collapse;width:100%;{ty("bodySmall")}}}'
         f'.tb th{{{ty("label")};color:var(--oa-color-text-secondary);text-align:left;padding:0 12px 8px 0;'
         'border-bottom:2px solid var(--oa-color-border-strong)}'
         '.tb td{text-align:left;vertical-align:top;padding:8px 12px 8px 0;border-bottom:1px solid var(--oa-color-border-hairline);'
         'overflow-wrap:anywhere}.tb td.n{font-variant-numeric:tabular-nums;white-space:nowrap}'
         '@media (max-width:47.99em){.tb,.tb tbody,.tb tr,.tb td{display:block;width:100%}.tb thead{display:none}'
         '.tb tr{padding:10px 0;border-bottom:1px solid var(--oa-color-border-strong)}.tb td{border:0;padding:2px 0}'
         '.tb td[data-k]::before{content:attr(data-k) ": ";font-weight:700}}')


def _size_words(f):
    """A file's size in words, read from the file itself (EXTRA_FILES['size_words'] holds the words)."""
    sw = EXTRA_FILES['size_words']
    p = EXPORTS / f
    if f.endswith('.png'):
        from PIL import Image
        with Image.open(p) as im:
            w, h = im.size
        return sw['px'].format(w=f'{w:,}', h=f'{h:,}')
    if f.endswith('.ico'):
        b = p.read_bytes()
        n = int.from_bytes(b[4:6], 'little')
        sizes = sorted({(b[6 + 16 * i] or 256) for i in range(n)})
        return sw['ico'].format(sizes=', '.join(str(s) for s in sizes[:-1]) + ' and ' + str(sizes[-1]))
    if f.endswith('.svg'):
        return sw['svg']
    if f.endswith('.html'):
        return sw['html']
    return ''


def s20_files():
    man = sorted(EXPORTS.glob('*_Phase-4-Exports-Manifest.json'))
    if not man:
        raise Waiting('the extra needs the kit’s exports manifest')
    files = [f for f in json.loads(man[-1].read_text()).get('files', []) if f.get('spec') in EXTRA_FILES['apps']]
    if not files:
        raise Waiting('the exports manifest lists no chapter 20 file yet')
    files.sort(key=lambda f: (f['spec'], not f['file'].endswith('.html'), f['file']))
    h = EXTRA_FILES['head']
    rows = ''.join(f'<tr><td data-k="{h[0]}">{EXTRA_FILES["apps"][f["spec"]]}</td><td data-k="{h[1]}">{f["file"]}</td>'
                   f'<td class="n" data-k="{h[2]}">{_size_words(f["file"])}</td></tr>' for f in files)
    html = (css(FILES) + '<div class="w"><table class="tb"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in h)
            + f'</tr></thead><tbody>{rows}</tbody></table></div>')
    return spec('s-20-files', html, None, EXTRA_FILES['alt'],
                notes='Read from the kit’s exports manifest; each size read from its file.')


# 20.10 and 20.11
def s20_10_correct():
    r = R['20.10']
    html = css() + f'<div class="w">{app("A09")}</div>'
    return spec('s-20-10-correct', html, '20.10', r['correct_alt'], notes='Drawn by the application kit (A09).')


CARD = ('.card{position:relative;container-type:inline-size;max-width:600px;aspect-ratio:1200/630;'
        'background:var(--oa-color-surface-newsprint);color:var(--oa-color-text-primary-on-newsprint);'
        'border:1px solid var(--oa-color-border-hairline-on-newsprint);overflow:hidden}'
        '.card .kk{position:absolute;left:6cqi;top:6cqi;font-family:var(--oa-type-h3-font-family);'
        'font-weight:var(--oa-type-h3-font-weight);font-size:2.667cqi;line-height:var(--oa-type-h3-line-height)}'
        '.card .kk span{color:var(--oa-color-text-secondary-on-newsprint)}'
        '.card .hl{position:absolute;left:6cqi;top:10.9cqi;width:88cqi;font-family:var(--oa-type-title-font-family);'
        'font-weight:var(--oa-type-title-font-weight);font-size:9.167cqi;line-height:var(--oa-type-title-line-height);'
        'letter-spacing:var(--oa-type-title-letter-spacing)}'
        '.card .ft{position:absolute;left:0;right:0;bottom:0;height:15.5cqi}'
        '.card .wm{position:absolute;left:6cqi;top:5.17cqi;width:33.2cqi}.card .wm img{width:100%;height:auto}'
        '.card .lm{position:absolute;right:10cqi;top:7.17cqi;width:4cqi}.card .lm img{width:100%;height:auto}')


def s20_10_failure():
    r = R['20.10']
    a = PAGES['A09']
    html = (css(CARD) + f'<div class="w"><div class="card"><p class="kk">{a["kicker"][0]}<span> · {a["kicker"][1]}</span></p>'
            f'<p class="hl">{"<br>".join(a["headline"])}</p><div class="ft dk">'
            f'<span class="wm">{master(WM_DISPLAY, 398.57, 44, INK_CHAR)}</span>'
            f'<span class="lm">{master(LOCK48, 48, 48, INK_CHAR)}</span></div></div></div>')
    return spec('s-20-10-failure', html, '20.10', r['failure_alt'],
                notes='A drawing of a fault: the sign-off at 48 px in place of 96. Rule 08.2 counts the red pixels.')


def s20_11_correct():
    r = R['20.11']
    html = css() + f'<div class="w">{app("A10")}</div>'
    return spec('s-20-11-correct', html, '20.11', r['correct_alt'], notes='Drawn by the application kit (A10).')


def s20_11_failure():
    r = R['20.11']
    html = css(TABS) + f'<div class="w"><div class="tabs">{tab(PAGES["A07"]["title"], LOCK16, 16, 16)}</div></div>'
    return spec('s-20-11-failure', html, '20.11', r['failure_alt'],
                notes='A drawing of a fault: the lockmark’s 16 px master as a favicon (Rule 08.2’s row says never).')


class Waiting(Exception):
    """A plate whose facts come from the kit's output, which does not exist yet."""


PLATES = [s_opener, s20_1_correct, s20_1_failure, s20_2_correct, s20_2_failure, s20_3_correct, s20_3_failure,
          s20_4_correct, s20_4_failure, s20_5_correct, s20_5_failure, s20_6_correct, s20_6_failure, s20_7_correct,
          s20_7_failure, s20_8_correct, s20_8_failure, s20_9_correct, s20_9_failure, s20_files, s20_10_correct,
          s20_10_failure, s20_11_correct, s20_11_failure]


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
        sid = 's-20-' + rid.split('.')[1]
        specs = [{'label': a, 'value': b} for a, b in r['specs']]
        if WCAG.get(rid):
            specs.append({'label': 'WCAG 2.2', 'value': ', '.join(WCAG[rid])})
        rel, rr = RELATED[rid]
        rules.append({
            'id': rid, 'title': r['title'], 'rule': r['rule'], 'tokens': TOKENS[rid],
            'why': {'text': [r['why']], 'basis': r['basis']},
            'correct': {'specimen': sid + '-correct', 'caption': r['correct_caption']},
            'failure': {'specimen': sid + '-failure', 'caption': r['failure_caption']},
            'specs': specs, 'related': rel, 'related_rules': rr, 'builders': r['builders'],
        })
    ch = {
        'number': CH, 'anchor': 'web', 'title': W['title'], 'part': 'applications', 'opener': 's-20-opener',
        'instruction': W['instruction'], 'intro': W['intro'],
        'groups': [{'before_rule': b, 'number': i, 'title': t, 'line': l} for i, (b, t, l) in enumerate(W['groups'], 1)],
        'rules': rules,
        'extras': [{'after_rule': '20.9', 'specimen': 's-20-files', 'label': EXTRA_FILES['label'],
                    'caption': EXTRA_FILES['caption']}],
        'related_chapters': [{'chapter': c, 'reason': t} for c, t in W['related_chapters']],
        'sources': W['sources'],
    }
    return ch, waiting


def page_words(aid):
    if aid == 'all':
        return {k: page_words(k) for k in ('A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10')}
    if aid in ('A04', 'A05'):
        return {'site': SITE, 'article': PAGES['A07']}
    if aid in ('A06', 'A07', 'A08'):
        return {'site': SITE, **PAGES[aid]}
    if aid in PAGES:
        return PAGES[aid]
    raise SystemExit(f'no application {aid}; use A04 to A10 or all')


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
    walk(SITE, 'SITE')
    walk(PAGES, 'PAGES')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build in memory and report; write nothing')
    ap.add_argument('--page-words', metavar='ID', help='print one application’s words as JSON (A04 to A10, or all)')
    a = ap.parse_args()
    if a.page_words:
        print(json.dumps(page_words(a.page_words), ensure_ascii=False, indent=1))
        return
    check_words()
    ch, waiting = build_chapter()
    B.check_chapter(ch)
    for w in waiting:
        print(f'  waiting: {w}')
    used = {ch['opener']} | {x['specimen'] for x in ch['extras']}
    for rr in ch['rules']:
        used |= {rr['correct']['specimen'], rr['failure']['specimen']}
    ours = set(ctx.specs)
    total = sum(len(s['html'].encode()) for s in ctx.specs.values())
    print(f'chapter 20: {len(ch["rules"])} rules, {len(ctx.specs)} specimens ({total:,} bytes before the kit’s frames)')
    if used - ours or ours - used:
        msg = f'specimens missing {sorted(used - ours)} unused {sorted(ours - used)}'
        if a.check:
            print('  ' + msg)
            return
        raise SystemExit(msg)
    if a.check:
        return
    if waiting:
        raise SystemExit('not written: plates wait for the kit')
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for p in OUT_SP.glob('s-20-*.html'):
        if p.stem not in ours:
            p.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    MANIFEST.write_text(json.dumps(dict(sorted((k, v['meta']) for k, v in ctx.specs.items())), indent=1,
                                   ensure_ascii=False) + '\n')
    print(f'wrote {OUT_CH.relative_to(ROOT)}, {len(ctx.specs)} specimens, {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
