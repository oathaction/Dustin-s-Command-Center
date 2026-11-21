"""Chapter 16, Photography, illustration and video (design director), Phase 4, chat 10, November 21, 2026.

Usage:
    python3 -I work/build/scripts/phase-4/phase4_ch16_build.py           write the chapter, specimens and manifest
    python3 -I work/build/scripts/phase-4/phase4_ch16_build.py --check   build everything in memory and report, write nothing

Writes:
    work/build/guide/chapters/16-photography.json      the chapter, in the content contract chapter 17 follows
    work/build/guide/specimens/s-16-*.html             one fragment per specimen this generator owns
    work/build/guide/specimens/manifest-photography.json   this chapter's manifest, written whole

Reads, never writes: work/build/tokens/tokens.json and tokens.css (through the stage A helpers), the two photographs'
registry in work/build/scripts/phase-4/guide_photos.py (contract C1, engineer notes), and the photograph files only to
measure Rule 16.4's contrast figure.

The plan is the creative director's, work/handoffs/phase-4/20261121_Chapter-16-Plan.md: thirteen rules in four groups, 28
plates, one extra and an opener.

Words. Every word a reader sees sits in the WORDS section near the top of this file, so the editor writes them there
and nothing else changes: W (the chapter's title, instruction, intro, group lines, the two photographs' captions and
alts, the opener's alt, related chapters and sources), R['16.1'] to R['16.13'] (each rule's title, rule, why, basis,
specs, builders, correct_caption, failure_caption, correct_alt and failure_alt, then the words drawn inside its plates
under the keys that follow) and EXTRA_KINDS (the extra after Rule 16.9). The How lines in R['16.1']['rows'] are the guide's own
direction for each shot, as the plate's caption says (editor, chat 10). The layout code below holds no reader text of its
own, apart from the Illustrative label and the do-not-publish band the stage A helpers add.

Photographs. A plate never embeds a photograph. It asks for one by name with an <img data-oa-photo> and its own alt
(contract C1), cropped in the plate's CSS (object-fit, aspect-ratio, object-position) or with data-oa-crop; the guide
build carries each photograph once for the whole page. Every photograph is shown in black and white (Rule 16.2),
through filter: grayscale(1) on its class, which the build's crop frame takes too.

Specimen checks are stage_a_systems_build.Ctx.spec(): no heading or landmark element, no dash, no literal color, no
px font size; every class is prefixed sx-.
"""
import argparse
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
GP = _load('guide_photos', HERE)
ROOT = C.ROOT
OUT_CH = ROOT / 'work/build/guide/chapters/16-photography.json'
OUT_SP = ROOT / 'work/build/guide/specimens'
MANIFEST = OUT_SP / 'manifest-photography.json'
CH = '16'
ILLUS = B.ILLUS
NB = C.NBSP
T = C.Tokens(C.TOKENS_JSON, C.TOKENS_CSS)
ctx = B.Ctx(T, {}, 'final')


# ------------------------------------------------------------------------------------------------ measured figures
def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rule_16_4_figures():
    """The ground under Rule 16.4's failure headline: Newsprint letters over the photograph in black and white, in the
    box the headline covers (6 to 94 percent across, 54 to 92 percent down the 3:2 crop 24 0 1152 768). CSS grayscale(1)
    mixes the sRGB values 0.2126, 0.7152 and 0.0722; contrast is WCAG 2.x relative luminance, pixel by pixel."""
    from PIL import Image
    p = GP.PHOTOS['lake-isabella-2014']
    im = Image.open(ROOT / p['file']).convert('RGB')
    x0, y0, w, h = 24, 0, 1152, 768
    box = im.crop((round(x0 + 0.06 * w), round(y0 + 0.54 * h), round(x0 + 0.94 * w), round(y0 + 0.92 * h)))
    ln = 0.2126 * _lin(0xDC) + 0.7152 * _lin(0xD9) + 0.0722 * _lin(0xD2)
    lo, n, under = 99.0, 0, 0
    px = box.get_flattened_data() if hasattr(box, 'get_flattened_data') else box.getdata()
    for r, g, b in px:
        y = 0.2126 * r + 0.7152 * g + 0.0722 * b
        lv = _lin(y)
        hi_, lo_ = max(lv, ln), min(lv, ln)
        c = (hi_ + 0.05) / (lo_ + 0.05)
        lo = min(lo, c)
        n += 1
        under += c < 3
    low = f'{lo:.1f}'
    share = round(100 * under / n)
    ctx.fig('16.4 lowest contrast under the headline', low, rule_16_4_figures.__doc__)
    ctx.fig('16.4 share of the ground under 3 to 1', f'{share} percent', rule_16_4_figures.__doc__)
    return low, share


LOW, UNDER3 = rule_16_4_figures()
R_NC = ctx.ratio('oa.color.text.primary.onCharcoal', 'oa.color.surface.charcoal', 'Newsprint on Charcoal')


# ================================================================================================ WORDS
# Everything a reader sees. The editor's fields. Keys name the rule (r1 to r13), the plate, or the chapter part.
# Chart S04's own source line, read from its spec, so the video example's figures carry the line the chart prints
# (house rule H04; editor, chat 10)
S04_SOURCE = json.loads((ROOT / 'work/build/chart-kit/specs/s04.json').read_text())['source_line'].rstrip('.') + '.'
if not S04_SOURCE.startswith('Source: U.S. Census Bureau, Current Population Survey'):
    raise SystemExit('chart S04’s source line has changed; reread Rules 16.10 to 16.13')
S04_FIGURES = 'The figures are chart S04’s, reported voting by age (Rule 14.19). ' + S04_SOURCE

W = {
    'title': 'Photography, illustration and video',
    'instruction': 'Show public life as it happens, and label every placeholder and generated image.',
    'intro': [
        'A photograph in Oath & Action is a record a reader can check. It shows people doing public work, and its caption '
        'says who, what, where and when, then names whoever made it. This chapter covers how we choose, crop, caption and '
        'credit photographs, how a frame holds a photograph’s place until we have one, where the few drawn and generated '
        'pictures may appear, and how we make and publish video.',
        'Two public-domain photographs from federal agencies, the same two chapter 01 shows, teach the photograph rules. '
        'Until we commission photographs of our own, a frame that says Placeholder holds each one’s place, and a '
        'generated picture appears only with its label and never stands for a real event.'],
    'groups': [
        ('16.1', 'Choosing and framing a photograph',
         'A photograph shows people at public work, in black and white unless its color is part of the record, and its '
         'crop and the words around it keep that work in view.'),
        ('16.5', 'The record behind each photograph',
         'Each photograph runs with a caption a reader can check and alt text for each crop, and our rights ledger '
         'records its rights and any consent before it runs.'),
        ('16.8', 'Placeholders and made pictures',
         'A frame that says Placeholder holds the place of a photograph we have yet to make, and a drawn or generated '
         'picture appears only where the table after Rule 16.9 allows, with its label.'),
        ('16.10', 'Video',
         'A video answers one question. Its soundtrack says what the screen shows, a person checks every caption, its '
         'transcript holds every word, and it plays only when a viewer presses Play.'),
    ],
    # the two photographs as chapter 01 captions them, and chapter 01's alts for the wide crops (word for word)
    'cap_lake': 'Paul Zianno, chief of civil works acquisition and management for the U.S. Army Corps of Engineers '
                'Sacramento District, explains the Isabella Lake Dam safety project’s land purchases to residents at a '
                'public meeting in Lake Isabella, California, March 27, 2014. Photograph: John Prettyman, U.S. Army.',
    'cap_rotunda': 'Members of the public file past the casket of Rosa Parks, the civil rights pioneer, as she lies in '
                   'honor in the Rotunda of the U.S. Capitol, Washington, D.C., October 2005. Photograph: Architect of the '
                   'Capitol.',
    'alt_lake': 'An official points to a project map while two residents, seen from behind, listen.',
    'alt_rotunda': 'Mourners file past a casket ringed by velvet ropes in the Capitol Rotunda, under its paintings and '
                   'statues.',
    'opener_alt': 'Two documentary photographs in black and white. A federal official answers residents at a public '
                  'meeting in Lake Isabella, California, in 2014, and members of the public file past the casket of Rosa '
                  'Parks in the Capitol Rotunda in 2005. Each carries its full caption.',
    'related_chapters': [
        ('01', 'Rules 01.6 and 01.8 and the rotation log, which these photographs and settings serve.'),
        ('02', 'Rule 02.9’s rewrite of our fifth edition’s headline, and house rules H03 to H05.'),
        ('03', 'A logo over a photograph, on its panel (Rule 03.3).'),
        ('05', 'The red rule, which black and white keeps clear (Rule 05.3).'),
        ('12', 'L8, the monogram, in a video’s corner, and the exploded view.'),
        ('13', 'The Illustrative label and source lines.'),
        ('14', 'Chart S04 and its table, which the video example reads aloud.'),
        ('17', 'No autoplay, and playback a reader starts.'),
        ('18', 'Buttons and links in the video card.'),
        ('19', 'Alt text, live text and the WCAG map.'),
    ],
    'sources': [
        'Source: W3C, “Web Content Accessibility Guidelines (WCAG) 2.2”, W3C Recommendation, December 12, 2024, success '
        'criteria 1.1.1, 1.2.1 to 1.2.5, 1.3.1, 1.4.1 to 1.4.3, 1.4.5, 2.1.1, 2.2.2 and 4.1.2, and its definitions of '
        'captions and of an alternative for time-based media, retrieved November 21, 2026. Behind Rules 16.2, 16.4, 16.7 '
        'to 16.9 and 16.11 to 16.13.',
        'Source: W3C, “Understanding Success Criterion 1.2.5: Audio Description (Prerecorded)”, retrieved November 21, '
        '2026. Its note on video whose soundtrack already carries what the picture shows, behind Rule 16.12.',
        'Source: Society of Professional Journalists, “SPJ Code of Ethics”, revised October 4, 2026, retrieved November '
        '21, 2026. Behind Rules 16.3, 16.5, 16.6 and 16.9.',
        'Source: Reporters Committee for Freedom of the Press, “Reporter’s Recording Guide”, retrieved November 21, '
        '2026. Its state-by-state guide to recording sound, named in Rule 16.6; this guide gives no legal advice.',
        'Source: YouTube Help, LinkedIn Help, X Help, TikTok’s newsroom and Community Guidelines, and Meta’s newsroom, '
        'on caption files and labels for generated content, retrieved November 21, 2026. Where a page would not open to '
        'us, Rules 16.9 and 16.11 say so and give what a search of that page showed. Platforms change these pages; check '
        'them before a video posts.',
        'Source: Wikimedia Commons file pages for the two photographs, their license boxes retrieved November 21, 2026, '
        'and both photographs’ rows in our rights ledger. Both are public-domain works of federal agencies.',
        S04_SOURCE + ' Chart S04’s line, for the video example in Rules 16.10 to 16.13.',
    ],
}

R = {}

# ---- Group 1
R['16.1'] = {
    'title': 'Photograph public work while it happens.',
    'rule': ['Photograph people while they do public work, such as a resident testifying, a clerk counting ballots or an '
             'official answering questions at a public meeting. Choose the frame where the act and the people it serves '
             'are both in view.',
             'Leave raised fists, megaphones, flag-waving, handshake close-ups, people pointing at laptops, the Capitol '
             'dome at sunset, protest signs used as a motif, glossy stock and crowds of identical smiling people out of '
             'our pictures, because each stands for civic life in general and shows no decision a reader can follow.'],
    'why': 'A picture of a real meeting on a real day gives a reader a place, a date and people they can check against '
           'the record.',
    'basis': 'Design judgment, from our fifth edition’s photography direction',
    'specs': [('Subject', 'People doing public work, officials included'),
              ('Frame', 'The act and the people it serves, both in view'),
              ('Light', 'Available light, at eye level, as our fifth edition set it'),
              ('Staging', 'None; photograph what happens'),
              ('Settings', 'Spread across states, regions and levels of government, logged in chapter 01’s rotation log (Rules 01.9, 01.10 and 01.12)'),
              ('Leave out', 'The list in the rule')],
    'builders': 'Write the subject and the act you need in the shot list’s form before a shoot or a search, then choose '
                'the frame where the act is happening.',
    'correct_caption': 'The shot list, a brief for the photographs we will commission. The first two rows are the '
                       'photographs this guide shows. The other ten take their subjects from our fifth edition, each set at '
                       'a level of government and in a region with our direction for the shot, and a placeholder holds each '
                       'one’s place until it is made.',
    'failure_caption': '<strong>Fails Rule 16.1.</strong> Cropped to its paintings and carved panels, the same photograph '
                       'shows an empty room, so it stands for government in general and records no public act.',
    'correct_alt': 'A table, the shot list, with columns Subject, Where, How and Status. Two rows are photographs in the '
                   'guide, the Capitol Rotunda in 2005 and a public meeting at Lake Isabella in 2014; ten rows are subjects '
                   'to commission, from a planning board meeting in a school cafeteria to a volunteer with a clipboard on a '
                   'sidewalk, each with where it is set and how to shoot it.',
    'failure_alt': 'The upper walls of the Capitol Rotunda in black and white: two large framed paintings between carved '
                   'stone panels and pilasters, and no people.',
    'failure_photo_alt': 'The upper walls of the Capitol Rotunda: two large framed paintings between carved stone panels '
                         'and pilasters.',
    'failure_photo_cap': 'The Rotunda of the U.S. Capitol, Washington, D.C., October 2005. Photograph: Architect of the Capitol.',
    'table_head': ('Subject', 'Where', 'How', 'Status'),
    'status_have_6': 'In the guide (Rule 01.6)',
    'status_have_8': 'In the guide (Rule 01.8)',
    'status_todo': 'To commission; a placeholder holds its place (Rule 16.8)',
    # Subject, Where, How. Rows 3 to 12 take their subjects from our fifth edition's shot list. The How column is the
    # guide's own direction for each shot (editor, chat 10), and the caption says so: three lines keep our fifth edition's
    # words whole (rows 8, 10 and 11), and the rest are written for this guide, so no line passes for a quote of a text
    # the census cut at 50 characters. The plate describes the two photographs it has from the photographs themselves.
    'rows': [
        ('Members of the public file past the casket of Rosa Parks in the Capitol Rotunda',
         'Washington, D.C.; federal; South',
         'From behind the line of people, with the casket and the room in one frame', 'have6'),
        ('A federal official answers residents at a public meeting', 'Lake Isabella, California; federal; West',
         'At eye level, from behind the residents, with the official, two residents and the project map in one frame',
         'have8'),
        ('A planning board meeting in a school cafeteria', 'Town; Northeast',
         'Folding tables and paper agendas, with the board and the residents in one frame.', 'todo'),
        ('A resident testifying at a microphone in a state house hearing room', 'State; Midwest',
         'From the side, at eye level, with the committee’s dais in frame.', 'todo'),
        ('A kitchen table with bills and a laptop at night', 'Household; South',
         'Available light from the lamp, with the hands in frame and the faces out of it.', 'todo'),
        ('A polling place in a gymnasium', 'County; West',
         'Wide, from the door, with the line and the booths in frame. Ask the election official first, and leave out '
         'every marked ballot and every voter at a booth.', 'todo'),
        ('A small business owner at the counter', 'City; West',
         'Mid-task, with the register and the street through the window.', 'todo'),
        ('Neighbors talking on a front porch', 'Neighborhood; South',
         'Late afternoon. Nobody looks at the lens.', 'todo'),
        ('A union hall meeting', 'A union local; Midwest',
         'From the back of the hall, with the rows of folding chairs and the speaker in one frame.', 'todo'),
        ('A library bulletin board with meeting notices', 'Town; Northeast',
         'Flat, overhead or straight on. Pins and paper.', 'todo'),
        ('Veterans and families at a town hall', 'Federal, a member of Congress’s district meeting; South',
         'Seated, listening. Caps and jackets, no ceremony.', 'todo'),
        ('A volunteer with a clipboard on a sidewalk', 'City; West',
         'Walking toward the camera while talking with a neighbor.', 'todo'),
    ],
}

R['16.2'] = {
    'title': 'Show a photograph in black and white, and keep color only where it is part of the record.',
    'rule': ['Show every photograph in black and white, converted from the color original, unless its color is part of '
             'what it records, such as the brown of tap water a resident holds up at a hearing. A photograph kept in color '
             'says in its caption what the color shows.',
             'Change only tone, exposure and contrast, evenly across the frame. Leave off tints, color grades, vignettes '
             'and every other effect, since each changes how the place looked.'],
    'why': 'Black and white keeps a photograph’s own reds and blues off our page. The Rotunda photograph in color holds '
           'red coats and red, white and blue wreaths; in black and white the view’s one working red (Rule 05.3) stays '
           'the only red a reader sees. Black and white also lets photographs from different agencies, cameras and years '
           'sit together as one publication.',
    'basis': 'The photography direction our founder and editor approved on October 28, 2026, black and white with color '
             'where color is evidence; design judgment for the reasons',
    'specs': [('Default', 'Black and white, from the color original'),
              ('On screen', '<code>filter: grayscale(1)</code> on the photograph, and nothing else'),
              ('For print or an export', 'A grayscale conversion made from the original file, never from the 1,200 px copy the page shows'),
              ('Color', 'Only where it is part of the record, named in the caption'),
              ('Adjust', 'Tone, exposure and contrast, evenly across the frame'),
              ('Never', 'A tint, a duotone in a brand color, a color grade, a vignette or any other effect'),
              ('On Charcoal', 'The photograph unchanged; the caption in Charcoal’s text tokens', 'oa.color.text.primary.onCharcoal')],
    'builders': 'On a page, set <code>filter: grayscale(1)</code> on the photograph. For print, convert the original file '
                'and compare it with the screen version at the same size.',
    'correct_caption': 'The Rotunda photograph in black and white, beside a placeholder for the one kind of photograph '
                       'that keeps its color, a picture whose color is the evidence, with a caption that says so.',
    'failure_caption': '<strong>Fails Rule 16.2.</strong> A Prussian tint dresses the people at the meeting in our color, '
                       'as if they belonged to our message, and shows a room that never looked that way.',
    'correct_alt': 'Two panels. The Capitol Rotunda photograph in black and white with its caption, and beside it a '
                   'placeholder frame for a photograph kept in color: a resident holding up a jar of brown tap water at a '
                   'city council hearing, whose caption names the color as the evidence.',
    'failure_alt': 'The Lake Isabella meeting photograph with a Prussian duotone: dark blue shadows and pale highlights '
                   'over the official, the residents and the map.',
    'plh_label': 'Placeholder',
    'plh_kind': 'Photograph to commission',
    'plh_shot': 'A resident holds up a jar of brown tap water at a city council hearing.',
    'plh_note': 'Kept in color, since the water’s color is the evidence, and the caption says so in words.',
}

R['16.3'] = {
    'title': 'Crop to keep the act whole, and change nothing inside the frame.',
    'rule': ['Crop a photograph so the person acting, at least one person they serve and the thing they are working on '
             'stay in view at every ratio it runs at. One photograph can serve all five ratios below. Set each crop by '
             'hand, then check that the caption still describes what the crop shows.',
             'A mark laid on the picture after it was taken, such as an agency’s corner logo, comes out in the crop, and its '
             'credit goes in the caption. A sign, a map or a badge that was in the room stays, since it is part of what '
             'happened. Add, move, remove and retouch nothing inside the frame.'],
    'why': 'A crop decides what a reader believes happened. With the residents cut away, an official seems to lecture an '
           'empty room, and a crop that loses the official leaves the caption naming a man the reader cannot see.',
    'basis': 'Society of Professional Journalists, Code of Ethics, revised October 4, 2026: “Never publish fabricated '
             'content that could be confused with reality.” Design judgment for the ratios',
    'specs': [('3:2', 'Articles, reports and web pages, the default. Lake Isabella 24 0 1152 768; Rotunda 60 0 1080 720'),
              ('16:9', 'A video’s poster frame and thumbnail (chapter 23). Lake Isabella 0 19 1200 675; Rotunda 0 0 1200 675'),
              ('1:1', 'A square post. Lake Isabella 108 0 768 768; Rotunda 300 0 720 720'),
              ('4:5', 'A portrait post. Lake Isabella 205 0 614 768; Rotunda 370 0 576 720'),
              ('1.91:1', 'The share preview (chapter 20). Lake Isabella 0 21 1200 628; Rotunda 0 0 1200 628'),
              ('Rectangles', 'x, y, width and height in the photograph’s own pixels, ready for <code>data-oa-crop</code>. Every Rotunda rectangle ends at row 720 or above, so the agency’s mark at the lower right stays out'),
              ('Keep in every crop', 'The person acting, at least one person they serve, and what they work on where it fits'),
              ('Smallest shown', '240 px wide; below that, faces and hands stop reading'),
              ('Sharpness', 'The crop’s width in photograph pixels at least twice the frame’s width'),
              ('Print', '300 pixels per inch at the printed size, made from the original file')],
    'builders': 'Take a crop from the table, then read the caption against the cropped picture. If a person the caption '
                'names has left the frame, choose another crop.',
    'correct_caption': 'One photograph at four of the five ratios, each crop set by hand. Every crop keeps the official, '
                       'his hand at work and at least one resident, so one caption serves them all.',
    'failure_caption': '<strong>Fails Rule 16.3.</strong> The portrait crop keeps a resident and the map and cuts out the '
                       'official, so the caption names a man the picture no longer shows.',
    'correct_alt': 'The Lake Isabella photograph four times in black and white, each labeled with its ratio and use: 3:2 '
                   'for articles and reports, 16:9 for a video poster, 1:1 for a square post and 4:5 for a portrait post. '
                   'Each keeps the official explaining and at least one resident.',
    'failure_alt': 'A 4:5 crop of the Lake Isabella photograph: one resident seen from behind and the project map, with '
                   'the official cut out, over the caption that names him.',
    'alt_wide': 'An official points to a project map while two residents, seen from behind, listen.',
    'alt_tight': 'An official speaks to two residents, his arm reaching past one of them toward a map.',
    'failure_photo_alt': 'A resident, seen from behind, faces a large project map on an easel.',
    'labels': [('3:2', 'Article and report'), ('16:9', 'Video poster and thumbnail'), ('1:1', 'Square post'), ('4:5', 'Portrait post')],
    # the set's caption is the photograph's own, with its credit, as Rule 16.5 asks of every photograph shown
    'set_caption': W['cap_lake'],
}

R['16.4'] = {
    'title': 'Set words beside a photograph, or on a solid panel over a plain part of it.',
    'rule': ['Set a headline, a label or a logo beside a photograph, or on a solid Charcoal or Newsprint panel laid over a '
             'plain part of it, clear of faces, hands at work and signs. Words never sit straight on the image, with or '
             'without a shadow or a gradient behind them.'],
    'why': 'Over a photograph, the ground under each letter changes from one letter to the next, so parts of a headline '
           'fade for every reader. A solid panel gives the words one ground and a contrast we can measure. Live text also '
           'stays text, so a reader can enlarge it or have it read aloud (Rule 19.4).',
    'basis': 'WCAG 2.2 success criteria 1.4.3 and 1.4.5; our fifth edition’s rule',
    'specs': [('Beside the photograph', 'The default'),
              ('Panel', f'Solid Charcoal or Newsprint, words in that surface’s text tokens; Newsprint on Charcoal measures {R_NC} to 1', 'oa.color.surface.charcoal'),
              ('Where a panel sits', 'On a plain area, clear of faces, hands at work and signs'),
              ('Never', 'Words on the image, a text shadow, or a gradient laid behind the words'),
              ('A logo over a photograph', 'On Rule 03.3’s panel')],
    'builders': 'Set the headline above or beside the photograph first. Use a panel only where the layout has no room '
                'beside it, and check that the panel covers no face, hand at work or sign.',
    'correct_caption': 'An article opener: its kicker and headline set above the photograph as live text, and the caption '
                       'under it.',
    'failure_caption': f'<strong>Fails Rule 16.4.</strong> Set on the picture, the headline crosses dark coats and a pale '
                       f'map. The contrast under parts of it falls to {LOW} to 1, and {UNDER3} percent of the ground under '
                       f'it measures under 3 to 1. It also covers the people the meeting was for.',
    'correct_alt': 'An article opener: the kicker Report, Public lands, then the headline as live text, then the Lake '
                   'Isabella photograph in black and white and its caption.',
    'failure_alt': f'The same headline in pale type set straight across the photograph, over the residents and the map, '
                   f'with a soft shadow; parts of it fade into the map, down to {LOW} to 1.',
    'kicker': ('Report', 'Public lands'),
    # from the agency's record: Zianno "discusses impacted properties and proposed real estate actions with local residents"
    'headline': 'At a public meeting in 2014, the Army Corps discussed the dam project’s proposed land purchases with '
                'Lake Isabella residents.',
}

# ---- Group 2
R['16.5'] = {
    'title': 'Caption who, what, where and when from the record, then credit the maker.',
    'rule': ['Write each caption from the record: the agency’s own caption, our notes from the event or the event’s public '
             'notice. Name who is shown, what they are doing, where and when, in that order, then give the credit.',
             'Give only as much as the record holds, so a record that knows only the month gets a caption that gives only '
             'the month. Claim no feeling, motive or result that the picture and the record do not show.'],
    'why': 'A caption is the part of a photograph a reader can check, and each of its four parts sends them to a record. A '
           'guess in any part gives the reader a fact no record backs.',
    'basis': 'Society of Professional Journalists, Code of Ethics, revised October 4, 2026: “Take responsibility for the '
             'accuracy of their work before releasing it.” and “Never plagiarize. Always attribute.” Rule 01.8',
    'specs': [('Order', 'Who, what, where, when, then the credit'),
              ('Who', 'Officials by name and role, from the record; members of the public unnamed unless the record names them and they agreed (Rule 16.6)'),
              ('What', 'Present tense, the act in view'),
              ('Where', 'The place, the city or town, and the state written out'),
              ('When', 'The date in words (house rule H05), only as exact as the record'),
              ('Credit', '“Photograph: John Prettyman, U.S. Army.” for a named maker; “Photograph: Architect of the Capitol.” when the agency made it; “Photograph: Dustin Cathcart, Oath & Action.” for ours; “Photograph: [name] for Oath & Action.” for a photographer we hire'),
              ('Never', 'The website that hosts the file, such as Wikimedia Commons, in place of the maker; a guess'),
              ('Length', 'One or two sentences', 'oa.type.caption')],
    'builders': 'Copy the record’s facts into the four parts before you write a sentence, then join them in order and add '
                'the credit.',
    'correct_caption': 'Chapter 01’s caption for the Rotunda photograph, with each part keyed in the order this rule sets.',
    'failure_caption': '<strong>Fails Rule 16.5.</strong> The caption claims anger and a seizure that neither the picture '
                       'nor the agency’s record shows. The record says he discussed proposed real estate actions with '
                       'residents.',
    'correct_alt': 'The Rotunda photograph small in black and white, beside its caption with each part underlined and '
                   'keyed: who, what, who, what, where, when and the credit, with a note that the record dates the '
                   'photograph only to two days.',
    'failure_alt': 'The Lake Isabella photograph in black and white over an invented caption: angry homeowners confront '
                   'an Army official over the seizure of their land.',
    'parts': [('Who', 'Members of the public'), ('What', 'file past the casket'), (None, 'of'),
              ('Who', 'Rosa Parks, the civil rights pioneer,'), ('What', 'as she lies in honor'),
              ('Where', 'in the Rotunda of the U.S. Capitol, Washington, D.C.,'), ('When', 'October 2005.'),
              ('Credit', 'Photograph: Architect of the Capitol.')],
    'when_note': 'When: the record places the photograph on October 30 or 31, 2005, the two days she lay in honor, so '
                 'the caption gives the month.',
    'bad_caption': 'Angry Lake Isabella homeowners confront an Army official over the seizure of their land, March 2014. '
                   'Photograph: John Prettyman, U.S. Army.',
}

R['16.6'] = {
    'title': 'Before a photograph runs, record its rights and any consent it needs.',
    'rule': ['The same rules hold for our founder and editor, Dustin Cathcart, photographing on a phone at a public event, '
             'and for any photographer we hire. Check the host’s rules on cameras before the event starts, and photograph from '
             'where the public may stand. A public official doing public work may be shown and named with their role, and '
             'a member of the public may appear in a scene unnamed. Ask a person’s permission, and write down the answer, '
             'before you single them out in a close picture or name them in a caption. A person under 18 may be shown so '
             'they can be recognized only with a parent’s or guardian’s permission. Stop photographing anyone who asks you '
             'to, and leave their picture out.',
             'Before any photograph runs, give it a row in our rights ledger, our record of every picture we use: who made '
             'it, where it came from, the license or permission that covers it, and any consent. Some of this is a matter '
             'of state law that differs from state to state, such as recording a conversation’s sound or using a person’s '
             'likeness, and this guide gives no legal advice.'],
    'why': 'The Society of Professional Journalists’ Code of Ethics says: “Private people have a greater right to control '
           'information about themselves than public figures and others who seek power, influence or attention.” The code '
           'also asks for “heightened sensitivity” with juveniles. A photograph of a private person outlasts the meeting, '
           'so the permission has to be on the record before it runs.',
    'basis': 'Society of Professional Journalists, Code of Ethics, revised October 4, 2026; Reporters Committee for '
             'Freedom of the Press, “Reporter’s Recording Guide”; design judgment for the record’s fields',
    'specs': [('Makers', 'Dustin Cathcart on a phone at public events, and any photographer we hire; one set of rules'),
              ('Before the event', 'The host’s rules on cameras, which differ by body'),
              ('Officials doing public work', 'Shown, and named with their role from the record'),
              ('Members of the public in a scene', 'Shown and unnamed'),
              ('A close picture or a named caption of a private person', 'Their permission, written into the record'),
              ('Under 18', 'Recognizable only with a parent’s or guardian’s permission'),
              ('Asked to stop', 'Stop, and leave the picture out'),
              ('Polling places', 'Ask the election official first; leave out every marked ballot and every voter at a booth'),
              ('Matters of state law', 'Recording a conversation’s sound, a person’s likeness and pictures of minors; the Reporters Committee keeps a state-by-state guide to recording. No legal advice'),
              ('The rights ledger row', 'Maker, source, date, place, license or permission, consent, where the caption came from, the file and its original')],
    'builders': 'Fill the rights ledger row as you take or find the photograph, and leave the photograph out of any draft '
                'until the row is complete.',
    'correct_caption': 'The meeting photograph with two markers and its record. The official is named, with his role, from '
                       'his agency’s caption, and the residents are seen from behind and named nowhere, so no consent was '
                       'needed.',
    'failure_caption': '<strong>Fails Rule 16.6.</strong> The caption names a 14-year-old and her school, and the record '
                       'holds no permission from a parent or guardian.',
    'correct_alt': 'The Lake Isabella photograph in black and white with two numbered markers: 1 beside the official, '
                   '2 on a resident’s back. A key says the official is named with his role and the residents are unnamed. '
                   'Under it, the rights record: maker, agency, date, place, license, consent and rights rows.',
    'failure_alt': 'A placeholder frame for a close portrait of a ninth grader speaking at a school board meeting, with an '
                   'invented caption that names her, her age and her school, and a record line that shows no permission '
                   'from a parent or guardian.',
    'keys': ['Named, with his role. A public official at a public meeting, named in the agency’s own caption.',
             'Unnamed. Members of the public, seen from behind and named nowhere in the record.'],
    'record_head': 'The record',
    'record': [('Maker', 'John Prettyman, U.S. Army'),
               ('Agency', 'U.S. Army Corps of Engineers, Sacramento District'),
               ('Date', 'March 27, 2014'),
               ('Place', 'Lake Isabella, Kern County, California'),
               ('License', 'Public domain in the United States as a work of the federal government (17 U.S.C. 105), read on the Commons file page November 21, 2026'),
               ('Consent', 'None needed: one official at public work, named by his agency; residents unnamed and seen from behind'),
               ('Rights rows', 'pho-04 for the source file and pho-04r for the copy the page shows')],
    'fail_plh': 'Placeholder for this failure: a close portrait of a ninth grader speaking at a school board meeting.',
    # the credit follows Rule 16.5's form for our own photographs, so the plate shows one fault, the missing permission
    'fail_caption_parts': ('Maya Brooks, 14,', 'a ninth grader at', 'Alder County High School,',
                           'asks the school board to keep the late bus, April 2026. Photograph: Dustin Cathcart, Oath & '
                           'Action.'),
    'fail_record': 'Permission from a parent or guardian: none recorded.',
}

R['16.7'] = {
    'title': 'Write alt text for what each crop shows.',
    'rule': ['Write alt text for each use of a photograph, for what that crop shows happening, in one or two sentences. '
             'Leave the names, the place, the date and the credit to the caption, which a screen reader also reads. When '
             'a photograph runs at a new crop, write its alt text again.'],
    'why': 'One photograph can run in five crops, and each shows something different. Alt text written for the wide '
           'frame describes things a tight crop has cut away.',
    'basis': 'WCAG 2.2 success criterion 1.1.1; Rule 19.2',
    'specs': [('Length', 'One or two sentences'),
              ('Says', 'What is happening and who acts, in plain words'),
              ('Leaves to the caption', 'Names, place, date, credit'),
              ('Each use', 'Its own alt text for its own crop'),
              ('Never', 'A file name, “photo of” or “image of”, or the caption repeated'),
              ('A placeholder frame', 'Live text and no alt text (Rule 16.8)'),
              ('A generated image', 'Alt text that begins “Generated image” (Rule 16.9)')],
    'builders': 'Look at the crop as it will run, without the caption, and write what a person who cannot see it needs to '
                'follow the story.',
    'correct_caption': 'Two crops of the Rotunda photograph, each with alt text written for what it shows. The tight crop '
                       'holds the line of mourners, a wreath, a painting and a statue, and no casket.',
    'failure_caption': '<strong>Fails Rule 16.7.</strong> The tight crop reuses the wide crop’s alt text, so a screen '
                       'reader hears of a casket this crop has cut away.',
    'correct_alt': 'Two crops of the Rotunda photograph in black and white, each with its alt text printed under it: the '
                   'wide crop’s mentions the casket, the tight crop’s mentions the line of mourners, a wreath and a painting.',
    'failure_alt': 'The tight crop of the Rotunda photograph, with the wide crop’s alt text printed under it, which names '
                   'a casket the crop does not show.',
    'alt_tight': 'Mourners wait in line along velvet ropes in the Capitol Rotunda, beside a wreath and under a large painting.',
    'alt_head': 'Alt text',
    'labels': ('Wide, 3:2', 'Tight, 4:5'),
    # the photograph's own caption, word for word as chapter 01 prints it
    'shared_caption': W['cap_rotunda'],
}

# ---- Group 3
R['16.8'] = {
    'title': 'Hold a commissioned photograph’s place with a frame that says Placeholder.',
    'rule': ['Until we commission a photograph, a placeholder holds its place: a frame at the photograph’s ratio and size, '
             'with the word Placeholder at its top, the shot it waits for in live text and the caption’s parts still to '
             'write. Here a placeholder means that frame, apart from the hint text in a form field.',
             'A placeholder imitates no photograph, so it takes no gray fill, texture, silhouette or stock picture. A '
             'published piece with no photograph runs without one, and placeholders stay in this guide, in templates and '
             'in drafts.'],
    'why': 'A gray box at a photograph’s size reads as a picture still loading, and our fifth edition’s panels told a '
           'screen reader “Photograph” for pictures that did not exist. Words in the frame tell every reader what is '
           'missing and what will fill it.',
    'basis': 'The direction our founder and editor set for this edition’s pictures, which asks every placeholder to '
             'announce itself; WCAG 2.2 success criterion 1.1.1; our October 2026 audit of the fifth edition’s photographs',
    'specs': [('Frame', 'The photograph’s ratio and display size', 'oa.color.border.strong.onNewsprint'),
              ('Edge', 'A 1 px keyline in the surface’s strong border, no fill, and four corner crop marks: 1 px, 12 px arms, 6 px off each corner'),
              ('Inside', 'Padding of 24 px; 16 px in a frame 320 px wide or narrower', 'oa.space.300'),
              ('Words', '“Placeholder”, what it waits for, the shot, the ratio and the treatment', 'oa.type.label'),
              ('Caption', 'The parts still to write', 'oa.type.caption'),
              ('Markup', 'Live text in a figure, the word Placeholder first; no image role and no alt text'),
              ('Where', 'This guide, templates and drafts; never a published piece'),
              ('Surfaces', 'Newsprint, White and Charcoal, each in its own tokens', 'oa.color.border.strong.onCharcoal'),
              ('Never', 'A dashed edge, which carries evidence grades in chapters 13 and 15, or a cross through the frame')],
    'builders': 'Draw the frame at the size the photograph will run, write the shot from the shot list (Rule 16.1) and '
                'leave the caption’s parts open.',
    'correct_caption': 'Two placeholders: a 3:2 frame on Newsprint for an article, and a 4:5 frame on Charcoal for a '
                       'portrait post in a dark mode. Each says what it waits for in words.',
    'failure_caption': '<strong>Fails Rule 16.8.</strong> Our fifth edition’s panel looks like a picture still loading, and '
                       'a screen reader announced it as a photograph that never existed.',
    'correct_alt': 'Two placeholder frames with corner crop marks and no fill. On Newsprint, a 3:2 frame: Placeholder, '
                   'photograph to commission, a resident testifies at a microphone in a state house hearing room. On '
                   'Charcoal, a 4:5 frame with the same words in Charcoal’s colors.',
    'failure_alt': 'A Stone panel at a photograph’s size with a small caption bar reading A polling place in a gymnasium '
                   'and Natural color 3:2, which our fifth edition announced to screen readers as a photograph.',
    'label': 'Placeholder',
    'kind': 'Photograph to commission',
    'shot': 'A resident testifies at a microphone in a state house hearing room, seen from the side at eye level, with '
            'the committee’s dais in frame.',
    'meta': '3:2 · Black and white · Shot list, row 4 (Rule 16.1)',
    'meta_45': '4:5 · Black and white · Shot list, row 4',
    'cap': 'Caption to write from the record: who, what, where and when, then the credit.',
    # our fifth edition's own words on its panel, kept as it printed them
    'v5_cap': 'A polling place in a gymnasium',
    'v5_meta': 'Natural color / 3:2',
}

R['16.9'] = {
    'title': 'Label a generated image beside it, and never let one stand for a real event.',
    'rule': ['A generated image is a picture an AI tool makes from a written prompt. It may serve only as a labeled '
             'conceptual illustration, or as the setting around our real work in a mockup, a picture that shows our page '
             'where a reader would meet it. Every one carries the words “Generated image” on a solid tab at its top left corner, '
             'its caption says what idea it shows and names the tool and the date, and its alt text begins “Generated '
             'image”.',
             'It never shows a real person or a real place on a real day, or anything a reader could take for a '
             'photograph of an event. Where a platform has its own label, we turn it on too, and we keep the Content '
             'Credentials, the data some tools write into the file to say how it was made. Each generated image gets a '
             'rights row with the tool, the date, the prompt and the tool’s terms.'],
    'why': 'The Society of Professional Journalists asks journalists to “Never publish fabricated content that could be '
           'confused with reality. Clearly label illustrations and reenactments.” The tab stays on the picture when it is '
           'shared without its caption, and the alt text gives the label to a reader who cannot see the picture.',
    'basis': 'The direction our founder and editor set for this edition’s pictures, and his answer of November 21, 2026 '
             'on generated images; Society of Professional Journalists, Code of Ethics, revised October 4, 2026; each '
             'platform’s help or policy page',
    'specs': [('May serve as', 'A conceptual illustration; the setting around our real work in a mockup'),
              ('Label on the picture', '“Generated image” on a solid Charcoal tab, top left', 'oa.color.surface.charcoal'),
              ('Caption', 'The idea it shows, then “Generated image, [tool], [date]”'),
              ('Alt text', 'Begins “Generated image”'),
              ('Never', 'A real person, a real place on a real day, evidence or documentary imagery'),
              ('File and record', '<code>YYYYMMDD_Generated-[Subject].png</code>; a rights row with the tool, the date, the prompt and the tool’s terms as read'),
              ('Content Credentials', 'Kept in the file'),
              ('YouTube', 'In YouTube Studio’s “AI use” setting, answer Yes for any realistic generated or altered content (YouTube Help, read November 21, 2026)'),
              ('TikTok', 'Turn on its label for AI-generated content, which it requires for realistic scenes or people (its Community Guidelines, read November 21, 2026; the label’s wording from a search of TikTok’s help pages, which would not open to us)'),
              ('Instagram, Threads and Facebook', 'Turn on Instagram’s “Label as made with AI” when sharing; Meta shows the label as “AI info” (Meta’s newsroom, read November 21, 2026; Instagram’s help page from a search, since it would not open to us)'),
              ('LinkedIn', 'No label a poster sets; it shows the Content Credentials icon when the file carries that data, so keep it (LinkedIn Help, read November 21, 2026)'),
              ('X', 'We found no label a poster sets; X may add its own “Manipulated media” label, and our tab and caption carry ours (X Help, from a search, since it would not open to us)')],
    'builders': 'Before you make one, check the table after this rule for where a generated picture may appear. Write the '
                'prompt into the rights row, make the image, and set the tab, caption and alt text before it goes anywhere.',
    'correct_caption': 'Where a generated image would sit in a mockup, held by a placeholder: the tab at its corner, the '
                       'prompt, and the caption that labels the scene and keeps our real page’s own credit.',
    'failure_caption': '<strong>Fails Rule 16.9.</strong> A generated picture runs with a news caption and a photograph’s '
                       'credit, so a reader believes a hearing looked this way.',
    'correct_alt': 'A placeholder frame for a generated image, with the Generated image tab at its top left and the '
                   'written prompt inside: a phone on a kitchen table beside a utility bill and a mug. Under it, a caption '
                   'that labels the scene as a generated image, with fields for the tool and the date, and a rights record line.',
    'failure_alt': 'A placeholder frame for a generated picture of a packed hearing room, with no tab, over a news caption '
                   'and a photograph’s credit for an invented hearing.',
    'head': 'Placeholder · Generated image to make',
    'tab': 'Generated image',
    'prompt': 'A phone lying screen up on a kitchen table beside a folded utility bill and a mug, morning light, seen from '
              'above. The screen is blank for our page to be placed on. No people, no logos, no words.',
    'caption': 'Mockup: where a reader meets our explainer. The page on the screen is ours, and the scene around it is a '
               'generated image, [tool], [date].',
    'record': 'Rights row: tool, date, prompt, terms read. File: YYYYMMDD_Generated-Mockup-Kitchen-Table-Phone.png',
    'fail_plh': 'Placeholder for this failure: a generated picture of a packed hearing room.',
    'fail_caption': ('Residents fill the', 'Alder County', 'hearing room before the rezoning vote, March 3, 2026. '
                     'Photograph: Oath & Action.'),
}

EXTRA_KINDS = {
    'label': 'Where each kind of picture may appear',
    'caption': 'Five kinds of picture, where each may appear, how each is labeled and the rule that sets it. We have no '
               'hand-drawn spot illustration yet. The hand-drawn study among our references was probably made by an image '
               'generator, so it cannot ship, and a commissioned drawing will fill that row.',
    'alt': 'A table of five kinds of picture: documentary photograph, placeholder, hand-drawn spot illustration, exploded '
           'view and generated image, with where each may appear, its label, what it never does and its rules.',
    'head': ('Kind', 'Where it may appear', 'Its label', 'Never', 'Rules'),
    'rows': [
        ('Documentary photograph', 'Articles, reports, web pages, social posts, video',
         'Caption: who, what, where, when, then “Photograph: maker”', 'Tinted, cropped to change what happened, or under words',
         'Rules 16.1 to 16.7, 01.6 and 01.8'),
        ('Placeholder', 'This guide, templates, drafts', '“Placeholder” in its frame', 'In a published piece', 'Rule 16.8'),
        ('Hand-drawn spot illustration', 'Article openers, report spreads and event signs, at 96 px and larger, drawn by a '
         'person', '“Illustration: maker”',
         'An icon; red and blue together; a Capitol dome or scales; a generated drawing in its place',
         'None yet; approved by our founder and editor, October 28, 2026'),
        ('Exploded view', 'The atlas’s three layers only', 'Its names, flat beside each plane', 'Anything else', 'Rule 12.8'),
        ('Generated image', 'A conceptual illustration; the setting around our work in a mockup',
         '“Generated image” tab, a caption with the tool and date, alt text that begins “Generated image”',
         'Evidence, a real person, a real place on a real day', 'Rule 16.9'),
    ],
}

# ---- Group 4, the video example: chart S04 (Rule 14.19), every figure from its spec; the video is not made, so each
# plate carries the Illustrative label, and each caption carries the chart's source line
R['16.10'] = {
    'title': 'Make each video answer one question, from its title frame to its step.',
    'rule': ['Each video answers one question a viewer could ask, such as “Which age groups reported voting in 2024?” It '
             'takes one of two forms, Dustin on camera as host or his voice over charts and atlas views, and it may move '
             'between them. The first sentence spoken asks the question or answers it. Every chart on screen carries its '
             'source line for as long as it shows.',
             'The video ends on a step a viewer can take, then the end frame. The first time Dustin appears, his name plate '
             'reads “Dustin Cathcart, Founder and Editor”. L8, the monogram, signs a top corner (Rule 12.3). Chapter 23 '
             'draws the title frame, the end frame, the name plate and each platform’s safe areas.'],
    'why': 'A viewer scrolling a feed decides fast whether to stay, so the question comes first. A video that answers one '
           'question can be captioned, described and summed up in one sentence, which its card needs (Rule 16.13).',
    'basis': 'Design judgment; the two forms are the ones our founder and editor chose on November 21, 2026',
    'specs': [('Question', 'One, in a viewer’s words'),
              ('Forms', 'Dustin on camera as host; his voice over charts and atlas views'),
              ('First sentence', 'Asks or answers the question'),
              ('Charts', 'From the chart kit, each with its source line on screen while it shows (Rule 13.6)'),
              ('Name plate', '“Dustin Cathcart, Founder and Editor”, the first time he appears; chapter 23 places it in the lower third, clear of each platform’s buttons and the captions'),
              ('Signature', 'L8, the monogram, 24 px in from the frame’s top and side edges (Rule 12.3)'),
              ('Ending', 'The step, then the end frame. A process piece names the step and leaves the position to the viewer (Rule 01.22); a position piece shows its label before the ask (Rule 01.23)'),
              ('Title and end frames', 'Chapter 23, at 1920 by 1080 and 1080 by 1920, each with its caption-safe area'),
              ('Music', 'Under the voice, and silent while a figure is read')],
    'builders': 'Write the question first, then the one sentence that answers it, and build the script from that '
                'sentence outward.',
    'correct_caption': 'A storyboard for a one-minute video on chart S04. The question comes in the first two seconds and '
                       'the step at 0:50, and every figure said is the chart’s own. ' + S04_FIGURES,
    'failure_caption': '<strong>Fails Rule 16.10.</strong> The question arrives at 0:21, after an animated logo and a '
                       'greeting, so a viewer who scrolls on never learns what the video answers.',
    'correct_alt': 'A storyboard of six video frames with their times and words: the title frame with the question at 0:00; '
                   'Dustin on camera with his name plate at 0:02; chart S04 with its source line at 0:08; the gap marked at '
                   '0:30; the step at 0:50; the end frame at 1:00.',
    'failure_alt': 'The same storyboard with the logo animating to music at 0:00, a greeting at 0:08 and the question only '
                   'at 0:21.',
    'question': 'Which age groups reported voting in 2024?',
    'slot': 'Drawn in chapter 23',
    'frames': [
        ('0:00', 'title', 'Title frame', ''),
        ('0:02', 'host', 'Placeholder: Dustin Cathcart on camera',
         'Which age groups told the Census Bureau they voted in 2024?'),
        ('0:08', 'chart', 'Chart S04, with its source line',
         'Citizens 18 to 24 reported voting at 47.7 percent, down 3.7 points from 2020. Those 65 and over stayed near 75 '
         'percent.'),
        ('0:30', 'gap', 'The gap, 23 points to 27',
         'So the gap between the youngest and the oldest grew from 23 points to 27. These are answers to a survey, which '
         'run higher than counted ballots.'),
        ('0:50', 'step', 'Check your registration',
         'Your state’s election office can tell you whether you are registered.'),
        ('1:00', 'end', 'End frame', ''),
    ],
    'name_plate': 'Dustin Cathcart, Founder and Editor',
    'step_head': 'The step',
    'fail_frames': [
        ('0:00', 'logo', 'The lockmark animates to music for eight seconds', ''),
        ('0:08', 'host', 'Placeholder: Dustin Cathcart on camera', 'Hey everyone, welcome back.'),
        ('0:21', 'host', 'Placeholder: Dustin Cathcart on camera', 'Today: which age groups reported voting in 2024?'),
    ],
}

R['16.11'] = {
    'title': 'Caption every video, and have a person check every word.',
    'rule': ['Every video carries closed captions, made from the final script and checked word for word against the final '
             'cut by a person before it posts. Captions, in the W3C’s words, are a “synchronized visual and/or text '
             'alternative for both speech and non-speech audio information needed to understand the media content”. '
             'A viewer can turn closed captions on and off in the player. Open captions are burned into the picture '
             'itself.',
             'Upload a caption file, a text file of timed lines, wherever a platform takes one: WebVTT (.vtt) on our own '
             'pages, WebVTT or SubRip (.srt) on YouTube, and SubRip on LinkedIn and X. On TikTok and Instagram, where we '
             'found no way to upload a file, turn on the app’s own captions and correct every word before publishing. '
             'Treat any automatic caption as a first draft. Burn captions in only where a platform offers neither, inside '
             'chapter 23’s caption-safe area, the part of the frame no app button or crop covers, and never on top of '
             'closed captions. Put a sound that matters, such as a gavel, in square brackets, and name a speaker who is '
             'off screen.'],
    'why': 'Automatic captions mishear names and numbers, and a misheard number tells a viewer who cannot hear something '
           'false. YouTube’s own help page says “You should always review automatic captions and edit any parts that '
           'haven’t been properly transcribed.”',
    'basis': 'WCAG 2.2 success criterion 1.2.2; each platform’s help page',
    'specs': [('Closed captions', 'On every video'),
              ('Files', 'WebVTT (<code>.vtt</code>) on our pages; YouTube takes <code>.vtt</code>, <code>.srt</code> and other formats (YouTube Help, read November 21, 2026); LinkedIn takes <code>.srt</code> on desktop (LinkedIn Help, read November 21, 2026); X takes <code>.srt</code> (X Help, from a search, since it would not open to us)'),
              ('TikTok and Instagram', 'The app’s own captions, corrected word for word; we found no caption file upload on either (each from a search of its help pages, November 21, 2026)'),
              ('Automatic captions', 'A first draft only'),
              ('Burned-in captions', 'Only where a platform offers neither, inside chapter 23’s caption-safe area, never doubled'),
              ('Lines', 'Two at most, about 42 characters each, broken at a phrase'),
              ('Type', f'Inter 600 in Newsprint on a Charcoal band, {R_NC} to 1; chapter 23 sets the size for each frame', 'oa.color.surface.charcoal'),
              ('Sounds and speakers', 'Sounds in square brackets when they carry meaning; speakers named when off screen'),
              ('Checked by', 'A person, against the final cut, before posting'),
              ('Live', 'A live stream needs live captions (WCAG 2.2 success criterion 1.2.4); we stream nothing live as of November 2026')],
    'builders': 'Make the caption file from the final script, play the final cut beside it, and correct every line before '
                'it uploads.',
    'correct_caption': 'A vertical frame at a quarter of 1080 by 1920, its captions on a Charcoal band inside the '
                       'caption-safe area, beside the WebVTT lines that make them. ' + S04_FIGURES,
    'failure_caption': '<strong>Fails Rule 16.11.</strong> Nobody checked the automatic caption, so a fall of 3.7 points '
                       'reads as 37.',
    'correct_alt': 'A 9:16 video frame drawn at a quarter size: a placeholder for Dustin’s voice over chart S04, an outlined '
                   'caption-safe area, and inside it two caption lines on a Charcoal band, Citizens 18 to 24 reported voting, '
                   'at 47.7 percent, down 3.7 points. Beside it, the WebVTT file with the same lines and their times.',
    'failure_alt': 'The same frame with an automatic caption that reads down 37 points.',
    'plh': 'Placeholder: Dustin’s voice over chart S04',
    'safe': 'Caption-safe area, set in chapter 23',
    'lines': ('Citizens 18 to 24 reported voting', 'at 47.7 percent, down 3.7 points.'),
    'bad_lines': ('Citizens 18 to 24 reported voting', 'at 47.7 percent, down 37 points.'),
    'file_head': 'The caption file, WebVTT',
    'vtt': 'WEBVTT\n\n00:00:08.000 --> 00:00:11.500\nCitizens 18 to 24 reported voting\nat 47.7 percent, down 3.7 points.',
    'scale_note': 'Drawn at a quarter of 1080 by 1920',
}

R['16.12'] = {
    'title': 'Say aloud what the screen shows, and publish a transcript with every video.',
    'rule': ['Audio description is a spoken account of what the picture shows. Write the script so the soundtrack gives '
             'it as the video runs: read each figure and what it measures, say whose source it is, and name what a gesture '
             'points at. Where the picture shows something there is no time to say, make a described version too, a '
             'second cut that adds the description in the pauses.',
             'Publish a transcript on the video’s page and link it from every post. It holds every word spoken, who speaks, '
             'the sounds that matter and what the screen shows that the words leave out, in order and corrected to the '
             'final cut, and it links each chart to its table.'],
    'why': 'The W3C’s page “Understanding Success Criterion 1.2.5: Audio Description (Prerecorded)”, retrieved November '
           '21, 2026, notes that “if all of the important information in the video track is already conveyed in the audio '
           'track, no additional audio description is necessary.” A voice that reads each chart aloud describes it as it '
           'goes, which serves a viewer who cannot see the screen and one who has the sound on and is looking away.',
    # the W3C's note, quoted in the Why above word for word (the main session's read of the page, 02:21 UTC)
    'why_understanding_quote': '“if all of the important information in the video track is already conveyed in the audio '
                               'track, no additional audio description is necessary.”',
    'basis': 'WCAG 2.2 success criteria 1.2.1, 1.2.3 and 1.2.5, and the W3C’s Understanding page for 1.2.5',
    'specs': [('Script', 'Every figure, its measure and its source said while it shows; gestures named'),
              ('Described version', 'Where the picture outruns the voice'),
              ('Transcript', 'On the video’s page, linked from every post: speakers, sounds that matter and what is shown, in order, corrected to the final cut'),
              ('Charts', 'Linked from the transcript to their tables'),
              ('A clip with sound only', 'A transcript'),
              ('A clip with no sound', 'A transcript or a voice track')],
    'builders': 'Read the script with your eyes closed. Any line that only makes sense while you watch needs the words '
                'for what is on screen.',
    'correct_caption': 'A script that says what the chart shows, with the transcript that follows from it. The transcript '
                       'links the chart to its table in chapter 14. ' + S04_FIGURES,
    'failure_caption': '<strong>Fails Rule 16.12.</strong> The voice points at the chart and reads none of it, so a '
                       'listener hears that something dropped and never learns by how much or in which survey.',
    'correct_alt': 'A two-column script, On screen and Said, three rows that read chart S04’s figures and source aloud, '
                   'then a transcript excerpt with the speaker, the time, the words and a bracketed line for what is on '
                   'screen, and a link to the chart’s table.',
    'failure_alt': 'The same script with one row: the chart on screen, and the voice saying As you can see, young people '
                   'dropped off right here.',
    'head': ('On screen', 'Said'),
    'rows': [('Chart S04: a dot for 2020 and one for 2024 in each age group; citizens 18 to 24 at the left.',
              'Citizens 18 to 24 reported voting at 47.7 percent in 2024, down 3.7 points from 2020, in the Census Bureau’s survey.'),
             ('The gap between the youngest and oldest groups, marked.',
              'The gap between the youngest and the oldest grew from 23 points to 27.'),
             ('S04’s source line.',
              'These are answers to a Census survey, which run higher than counted ballots.')],
    'bad_row': ('Chart S04: a dot for 2020 and one for 2024 in each age group.', 'As you can see, young people dropped off right here.'),
    'transcript_head': 'Transcript, from 0:08',
    'transcript': '[0:08] Dustin Cathcart: Citizens 18 to 24 reported voting at 47.7 percent in 2024, down 3.7 points '
                  'from 2020, in the Census Bureau’s survey. [On screen: a dot chart of reported voting by age group, 2020 '
                  'and 2024, with its source line.]',
    'link': 'The chart’s table, Rule 14.19',
}

R['16.13'] = {
    'title': 'Where a video sits, show its poster, summary and transcript, and play it only when a reader presses Play.',
    'rule': ['On our pages a video sits in a card: its poster frame, its title as live text, its length, one sentence with '
             'what it finds, a Play button, a link to the transcript and a link to watch it on the platform. The '
             'platform’s player loads only when a reader presses Play, and the video never plays by itself, with sound or '
             'without it.',
             'If the player cannot load, because a reader is offline, blocks the platform or runs no scripts, the card '
             'still gives the finding in its summary and the whole video in its transcript.'],
    'why': 'A card that stands on its own serves every reader the player fails, and it keeps the platform’s player off the '
           'page until a reader asks for it. Sound that starts by itself talks over a screen reader.',
    'basis': 'The direction our founder and editor set for this edition’s video; WCAG 2.2 success criteria 1.4.2 and '
             '2.2.2; Rules 17.1 and 17.3',
    'specs': [('Card', 'Poster, title, length, summary, Play, transcript link, platform link'),
              ('Poster', 'A frame from the video, usually its title frame (chapter 23), with alt text that gives its words (Rule 19.4)'),
              ('Player', 'Loads only on Play'),
              ('Playback', 'Never by itself, with sound or without (Rule 17.1)'),
              ('Captions', 'On at the start where the player allows'),
              ('If the player fails', 'The card stays whole'),
              ('Controls', 'The Play button 44 px tall; every control named by its words (Rule 19.3)', 'oa.size.target.touch'),
              ('Email', 'A still and a link, no player (chapter 22)')],
    'builders': 'Build the card first and check it with scripts off. Add the player behind Play only once the card reads '
                'whole on its own.',
    'correct_caption': 'The video card at true size, with its controls drawn: a poster that stands in for chapter 23’s '
                       'title frame, the title, the length, the finding in one sentence, Play and two links. ' + S04_FIGURES,
    'failure_caption': '<strong>Fails Rule 16.13.</strong> The player failed to load and the page offers nothing in its '
                       'place, so a reader gets no finding, no transcript and no link.',
    'correct_alt': 'A video card: a Charcoal poster with the question Which age groups reported voting in 2024? and L8 at '
                   'its corner; under it the title, the length 1:05, a one-sentence finding, a Play button and the links '
                   'Read the transcript and Watch on YouTube.',
    'failure_alt': 'An empty dark box at video size with the words Video unavailable in small gray type, and nothing else.',
    'title_text': 'Which age groups reported voting in 2024?',
    'length': '1:05',
    'summary': 'Citizens 18 to 24 reported voting at 47.7 percent in 2024, down 3.7 points from 2020, in the Census Bureau’s survey.',
    'play': 'Play',
    'links': ('Read the transcript', 'Watch on YouTube'),
    'another_site': '(another site)',
    'unavailable': 'Video unavailable',
}


WCAG = {
    '16.2': ['1.4.1'], '16.4': ['1.4.3', '1.4.5'], '16.7': ['1.1.1'], '16.8': ['1.1.1', '1.3.1'], '16.9': ['1.1.1'],
    '16.11': ['1.2.2'], '16.12': ['1.2.1', '1.2.3', '1.2.5'], '16.13': ['1.4.2', '2.2.2', '2.1.1', '4.1.2'],
}
TOKENS = {
    '16.1': ['oa.type.label', 'oa.type.bodySmall', 'oa.color.border.hairline.onNewsprint'],
    '16.2': ['oa.type.caption', 'oa.color.text.primary.onNewsprint', 'oa.color.text.primary.onCharcoal'],
    '16.3': ['oa.type.label', 'oa.color.text.secondary.onNewsprint'],
    '16.4': ['oa.color.surface.charcoal', 'oa.color.surface.newsprint', 'oa.color.text.primary.onCharcoal', 'oa.type.h3'],
    '16.5': ['oa.type.caption', 'oa.type.label', 'oa.color.graphic.essential.onNewsprint'],
    '16.6': ['oa.color.surface.charcoal', 'oa.color.text.primary.onCharcoal', 'oa.type.label', 'oa.type.bodySmall'],
    '16.7': ['oa.type.label', 'oa.type.bodySmall'],
    '16.8': ['oa.color.border.strong.onNewsprint', 'oa.type.label', 'oa.type.body', 'oa.type.caption', 'oa.space.300'],
    '16.9': ['oa.color.surface.charcoal', 'oa.color.text.primary.onCharcoal', 'oa.type.label', 'oa.type.caption'],
    '16.10': ['oa.color.surface.charcoal', 'oa.color.surface.newsprint', 'oa.type.label', 'oa.type.caption'],
    '16.11': ['oa.color.surface.charcoal', 'oa.color.text.primary.onCharcoal', 'oa.color.border.hairline.onNewsprint', 'oa.type.label'],
    '16.12': ['oa.type.bodySmall', 'oa.type.label', 'oa.color.border.hairline.onNewsprint'],
    '16.13': ['oa.size.target.touch', 'oa.color.surface.charcoal', 'oa.color.text.primary.onCharcoal', 'oa.type.h4', 'oa.type.bodySmall', 'oa.type.label'],
}
RELATED = {
    '16.1': (['01', '02'], ['01.6', '01.8', '01.9', '01.10', '01.12', '02.9']),
    '16.2': (['05', '01', '19'], ['05.3', '01.1', '01.6', '19.1']),
    '16.3': (['01'], ['01.6', '01.8']),
    '16.4': (['03', '19'], ['03.3', '19.4']),
    '16.5': (['01', '13', '02'], ['01.8', '13.6', '13.12', '02.22']),
    '16.6': (['01', '13'], ['01.8', '13.8']),
    '16.7': (['19'], ['19.2', '16.3']),
    '16.8': (['13', '18'], ['16.1', '13.8']),
    '16.9': (['13'], ['13.1', '13.8', '16.8']),
    '16.10': (['12', '13', '14', '01'], ['12.3', '13.6', '01.22', '01.23', '14.19']),
    '16.11': (['19'], ['19.1']),
    '16.12': (['14', '18', '19'], ['14.19', '18.23', '19.2']),
    '16.13': (['17', '18', '19'], ['17.1', '17.3', '19.3', '19.4']),
}

# ================================================================================================ LAYOUT
def ty(name):
    return ctx.ty(name)


V = ctx.v
BASE = (
    f'.w{{{ty("body")};color:var(--oa-color-text-primary);max-width:100%}}.w p{{margin:0}}.w *{{box-sizing:border-box}}'
    '.row{display:flex;flex-wrap:wrap;gap:24px 32px;align-items:flex-start}'
    '.pair{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,17rem),1fr));gap:32px;align-items:start}'
    '.w576{max-width:576px}.w540{max-width:540px}.w480{max-width:480px}.w420{max-width:420px}.w360{max-width:360px}.w320{max-width:320px}.w280{max-width:280px}'
    '.w270{max-width:270px}.w240{max-width:240px}.fig{width:100%}'
    '.ph{display:block;width:100%;height:auto;filter:grayscale(1)}'
    '.c32{aspect-ratio:3/2;object-fit:cover;object-position:50% 50%}'
    '.c169{aspect-ratio:16/9;object-fit:cover;object-position:50% 20%}'
    '.c11{aspect-ratio:1/1;object-fit:cover;object-position:25% 50%}'
    '.c45{aspect-ratio:4/5;object-fit:cover;object-position:35% 50%}'
    f'.cap{{{ty("caption")};color:var(--oa-color-text-secondary);margin-top:12px;max-width:34rem;text-wrap:pretty}}'
    f'.lab{{{ty("label")}}}.sec{{color:var(--oa-color-text-secondary)}}'
    f'.sm{{{ty("bodySmall")}}}.num{{font-variant-numeric:tabular-nums}}'
    '.mt8{margin-top:8px}.mt16{margin-top:16px}.mt24{margin-top:24px}'
    # the placeholder frame (Rule 16.8): keyline, no fill, four corner crop marks 6 px off each corner
    '.plh{position:relative;margin:19px 0;border:1px solid var(--oa-color-border-strong);padding:24px;display:flex;'
    'flex-direction:column;justify-content:space-between;gap:16px}'
    '.plh.tight{padding:16px;gap:12px}.r32{aspect-ratio:3/2}.r45{aspect-ratio:4/5}.r169{aspect-ratio:16/9}'
    '.cm{position:absolute;background:var(--oa-color-border-strong)}'
    '.cmh{width:12px;height:1px}.cmv{width:1px;height:12px}'
    '.tlh{top:-1px;left:-19px}.tlv{top:-19px;left:-1px}.trh{top:-1px;right:-19px}.trv{top:-19px;right:-1px}'
    '.blh{bottom:-1px;left:-19px}.blv{bottom:-19px;left:-1px}.brh{bottom:-1px;right:-19px}.brv{bottom:-19px;right:-1px}'
    '.out{margin:0}'
    # Charcoal panel and its tokens
    '.dk{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);padding:24px}'
    '.dk .plh{border-color:var(--oa-color-border-strong-on-charcoal)}.dk .cm{background:var(--oa-color-border-strong-on-charcoal)}'
    '.dk .sec{color:var(--oa-color-text-secondary-on-charcoal)}'
    # tables that stack into one card per row on phones (Rule 07.6)
    f'.tb{{border-collapse:collapse;width:100%;{ty("bodySmall")}}}'
    f'.tb th{{{ty("label")};color:var(--oa-color-text-secondary);text-align:left;vertical-align:bottom;padding:0 12px 8px 0;'
    'border-bottom:2px solid var(--oa-color-border-strong)}'
    '.tb td{text-align:left;vertical-align:top;padding:8px 12px 8px 0;border-bottom:1px solid var(--oa-color-border-hairline)}'
    '.tb td.k{font-weight:700}'
    '@media (max-width:47.99em){.tb,.tb tbody,.tb tr,.tb td{display:block;width:100%}.tb thead{display:none}'
    '.tb tr{padding:10px 0;border-bottom:1px solid var(--oa-color-border-strong)}.tb td{border:0;padding:2px 0}'
    '.tb td[data-k]::before{content:attr(data-k) ": ";font-weight:700}}'
)


def css(extra=''):
    return f'<style>{BASE}{extra}</style>'


def photo(name, alt, cls, crop=None):
    return GP.photo_img(name, alt, cls=cls, crop=crop)


def cap(text, extra=''):
    return f'<p class="cap{(" " + extra) if extra else ""}">{text}</p>'


def marks():
    return ''.join(f'<span class="cm cm{d[-1]} {d}" aria-hidden="true"></span>'
                   for d in ('tlh', 'tlv', 'trh', 'trv', 'blh', 'blv', 'brh', 'brv'))


def plh(ratio, inner, size='', extra=''):
    """A placeholder frame (Rule 16.8) at a ratio, with its words as live text and its crop marks."""
    return f'<div class="plh {ratio}{(" " + size) if size else ""}"{extra}>{marks()}{inner}</div>'


def uicon(name, px=24):
    return (f'<svg class="ui" viewBox="0 0 {px} {px}" width="{px}" height="{px}" aria-hidden="true" focusable="false" '
            f'data-icon="U-{name}" data-icon-family="utility"><use href="#oa-sym-u-{name}-{px}px"/></svg>')


def spec(sid, html, rule, alt, **kw):
    kw.setdefault('readable', True)
    ctx.spec(sid, prune(html), CH, rule, alt, **kw)
    return sid


# style pruning, as chapter 17's generator does: a specimen carries only the rules its classes use
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
    return re.sub(r'(<style\b[^>]*>)(.*?)(</style>)', lambda m: m.group(1) + prune_css(m.group(2), used) + m.group(3),
                  html, flags=re.S)


# ------------------------------------------------------------------------------------------------ the plates
def s_opener():
    html = (css() + '<div class="w"><div class="pair">'
            f'<div class="fig w576">{photo("lake-isabella-2014", W["alt_lake"], "ph c32")}{cap(W["cap_lake"])}</div>'
            f'<div class="fig w540">{photo("rotunda-2005", W["alt_rotunda"], "ph", (60, 0, 1080, 720))}{cap(W["cap_rotunda"])}</div>'
            '</div></div>')
    return spec('s-16-opener', html, None, W['opener_alt'],
                notes='Both photographs from contract C1, in black and white (Rule 16.2): Lake Isabella by CSS at 3:2, the '
                      'Rotunda by data-oa-crop 60 0 1080 720, which keeps the agency’s corner mark out.')


# 16.1
def s16_1_correct():
    r = R['16.1']
    st = {'have6': r['status_have_6'], 'have8': r['status_have_8'], 'todo': r['status_todo']}
    h = r['table_head']
    rows = ''.join(f'<tr><td class="k" data-k="{h[0]}">{s}</td><td data-k="{h[1]}">{wh}</td><td data-k="{h[2]}">{how}</td>'
                   f'<td data-k="{h[3]}">{st[k]}</td></tr>' for s, wh, how, k in r['rows'])
    html = (css() + '<div class="w"><table class="tb"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in h)
            + f'</tr></thead><tbody>{rows}</tbody></table></div>')
    return spec('s-16-1-correct', html, '16.1', r['correct_alt'],
                notes='Live text. Rows 3 to 12 take their subjects from our fifth edition’s shot list (Phase 0 census, '
                      'photography entries 30 to 49), with a level and a region added; the How lines are the guide’s own direction.')


def s16_1_failure():
    r = R['16.1']
    html = (css() + '<div class="w"><div class="fig w480">'
            f'{photo("rotunda-2005", r["failure_photo_alt"], "ph", (240, 0, 720, 360))}{cap(r["failure_photo_cap"])}</div></div>')
    return spec('s-16-1-failure', html, '16.1', r['failure_alt'], notes='Rotunda, data-oa-crop 240 0 720 360 (2:1).')


# 16.2
def s16_2_correct():
    r = R['16.2']
    inner = (f'<div><p class="lab">{r["plh_label"]}</p><p class="lab sec">{r["plh_kind"]}</p></div>'
             f'<p class="sm">{r["plh_shot"]}</p><p class="sm sec">{r["plh_note"]}</p>')
    html = (css() + '<div class="w"><div class="row">'
            f'<div class="fig w360">{photo("rotunda-2005", W["alt_rotunda"], "ph", (60, 0, 1080, 720))}{cap(W["cap_rotunda"])}</div>'
            f'<div class="fig w320"><div class="out">{plh("r32", inner, "tight")}</div></div>'
            '</div></div>')
    return spec('s-16-2-correct', html, '16.2', r['correct_alt'])


def s16_2_failure():
    r = R['16.2']
    extra = ('.duo{position:relative;max-width:540px}.t1,.t2{position:absolute;inset:0;pointer-events:none}'
             '.t1{background:var(--oa-color-palette-prussian);mix-blend-mode:screen}'
             '.t2{background:var(--oa-color-palette-newsprint);mix-blend-mode:multiply}')
    html = (css(extra) + '<div class="w"><div class="fig w540"><div class="duo">'
            f'{photo("lake-isabella-2014", W["alt_lake"], "ph c32")}<span class="t1" aria-hidden="true"></span>'
            f'<span class="t2" aria-hidden="true"></span></div>{cap(W["cap_lake"])}</div></div>')
    return spec('s-16-2-failure', html, '16.2', r['failure_alt'], exempt=['contrast'],
                notes='Picture of a fault: a Prussian duotone, drawn by two blended layers over the black and white '
                      'photograph (screen in Prussian, then multiply in Newsprint). No red on the plate.')


# 16.3
def s16_3_correct():
    r = R['16.3']
    crops = [('c32', 'w360', r['alt_wide']), ('c169', 'w360', r['alt_wide']), ('c11', 'w240', r['alt_tight']),
             ('c45', 'w240', r['alt_tight'])]
    cells = ''.join(f'<div class="fig {w}">{photo("lake-isabella-2014", a, "ph " + c)}'
                    f'<p class="mt8"><span class="lab num">{lab}</span> <span class="sm sec">{use}</span></p></div>'
                    for (c, w, a), (lab, use) in zip(crops, r['labels']))
    html = (css('.crops{display:grid;gap:24px 32px;grid-template-columns:minmax(0,1fr)}'
                '@media (min-width:48em){.crops{grid-template-columns:repeat(2,max-content);align-items:end}}')
            + f'<div class="w"><div class="crops">{cells}</div>{cap(r["set_caption"])}</div>')
    return spec('s-16-3-correct', html, '16.3', r['correct_alt'],
                notes='CSS crops: 3:2 at 50% 50%, 16:9 at 50% 20%, 1:1 at 25% 50%, 4:5 at 35% 50% (the plan’s rectangles).')


def s16_3_failure():
    r = R['16.3']
    html = (css() + '<div class="w"><div class="fig w240">'
            f'{photo("lake-isabella-2014", r["failure_photo_alt"], "ph", (660, 0, 540, 675))}</div>'
            f'{cap(W["cap_lake"])}</div>')
    return spec('s-16-3-failure', html, '16.3', r['failure_alt'], notes='Lake Isabella, data-oa-crop 660 0 540 675 (4:5).')


# 16.4
def kicker(lab, topic):
    return f'<p class="kick"><span>{lab}</span><span aria-hidden="true">·</span><span class="sec">{topic}</span></p>'


KICK_CSS = f'.kick{{display:flex;flex-wrap:wrap;gap:0 8px;{ty("label")};margin-bottom:12px}}.hl{{{ty("h3")};text-wrap:balance}}'


def s16_4_correct():
    r = R['16.4']
    html = (css(KICK_CSS) + '<div class="w"><div class="w540">' + kicker(*r['kicker'])
            + f'<p class="hl">{r["headline"]}</p><div class="fig mt24">{photo("lake-isabella-2014", W["alt_lake"], "ph c32")}'
            f'{cap(W["cap_lake"])}</div></div></div>')
    return spec('s-16-4-correct', html, '16.4', r['correct_alt'],
                notes='The kicker opens with one content label, Report (Rule 01.21); the headline is live text in the H3 style.')


def s16_4_failure():
    r = R['16.4']
    extra = (KICK_CSS + '.ov{position:relative}.ovt{position:absolute;left:6%;right:6%;bottom:8%;margin:0;'
             'color:var(--oa-color-palette-newsprint);text-shadow:0 1px 6px var(--oa-color-palette-charcoal)}')
    html = (css(extra) + '<div class="w"><div class="w540"><div class="ov">'
            f'{photo("lake-isabella-2014", W["alt_lake"], "ph c32")}<p class="hl ovt">{r["headline"]}</p></div>'
            f'{cap(W["cap_lake"])}</div></div>')
    return spec('s-16-4-failure', html, '16.4', r['failure_alt'], exempt=['contrast'],
                notes=f'Picture of a fault: Newsprint words on the photograph. Measured by this generator: the ground under '
                      f'the headline’s box falls to {LOW} to 1 against Newsprint, and {UNDER3} percent of it is under 3 to 1.')


# 16.5
def s16_5_correct():
    r = R['16.5']
    parts = ''.join((f'<span class="pt"><span class="pk">{k}</span><span class="pw">{t}</span></span>' if k
                     else f'<span class="pt"><span class="pk" aria-hidden="true">{NB}</span><span class="po">{t}</span></span>')
                    for k, t in r['parts'])
    extra = (f'.kc{{display:flex;flex-wrap:wrap;gap:16px 6px;align-items:flex-start;{ty("caption")};max-width:34rem}}'
             '.pt{display:inline-flex;flex-direction:column-reverse;gap:4px}'
             '.pw{border-bottom:2px solid var(--oa-color-graphic-essential);padding-bottom:2px}.po{padding-bottom:4px}'
             f'.pk{{{ty("label")};color:var(--oa-color-text-secondary)}}')
    html = (css(extra) + '<div class="w"><div class="row">'
            f'<div class="fig w240">{photo("rotunda-2005", W["alt_rotunda"], "ph", (60, 0, 1080, 720))}</div>'
            f'<div><p class="kc">{parts}</p><p class="sm sec mt16" style="max-width:34rem">{r["when_note"]}</p></div>'
            '</div></div>')
    return spec('s-16-5-correct', html, '16.5', r['correct_alt'],
                notes='Each part’s key comes first in reading order and shows under its words (column-reverse).')


def s16_5_failure():
    r = R['16.5']
    html = (css() + '<div class="w"><div class="fig w540">'
            f'{photo("lake-isabella-2014", W["alt_lake"], "ph c32")}{cap(r["bad_caption"] + " " + ILLUS)}</div></div>')
    return spec('s-16-5-failure', html, '16.5', r['failure_alt'], illustrative=True)


# 16.6
MK = (f'.mk{{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;'
      f'background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);'
      f'box-shadow:0 0 0 1px var(--oa-color-palette-newsprint);{ty("label")};flex:none}}'
      '.on{position:absolute;margin:-12px 0 0 -12px}.mkw{position:relative}')


def s16_6_correct():
    r = R['16.6']
    extra = (MK + '.keys{display:grid;gap:12px;margin:16px 0 0;padding:0;list-style:none;max-width:34rem}'
             '.keys li{display:flex;gap:12px;align-items:flex-start}'
             f'.rec{{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:4px 16px;margin:16px 0 0;{ty("bodySmall")};max-width:40rem}}'
             '.rec dt{font-weight:700}.rec dd{margin:0}')
    keys = ''.join(f'<li><span class="mk" aria-hidden="true">{i}</span><span class="sm">{t}</span></li>'
                   for i, t in enumerate(r['keys'], 1))
    rec = ''.join(f'<dt>{a}</dt><dd>{b}</dd>' for a, b in r['record'])
    html = (css(extra) + '<div class="w"><div class="fig w540"><div class="mkw">'
            f'{photo("lake-isabella-2014", W["alt_lake"], "ph c32")}'
            '<span class="mk on" style="left:36%;top:12%" aria-hidden="true">1</span>'
            '<span class="mk on" style="left:66%;top:72%" aria-hidden="true">2</span></div>'
            f'{cap(W["cap_lake"])}</div><ol class="keys">{keys}</ol>'
            f'<p class="lab mt24">{r["record_head"]}</p><dl class="rec">{rec}</dl></div>')
    return spec('s-16-6-correct', html, '16.6', r['correct_alt'],
                notes='Markers set in HTML over the frame (contract C1), hidden from a screen reader; the key carries their words.')


def s16_6_failure():
    r = R['16.6']
    a, b, c_, d = r['fail_caption_parts']
    inner = f'<p class="lab">{R["16.8"]["label"]}</p><p class="sm">{r["fail_plh"]}</p>'
    html = (css() + '<div class="w"><div class="w240"><div class="out">' + plh('r45', inner, 'tight') + '</div></div>'
            f'{cap(f"{a} {ILLUS} {b} {c_} {ILLUS} {d}")}<p class="sm mt8">{r["fail_record"]}</p></div>')
    return spec('s-16-6-failure', html, '16.6', r['failure_alt'], illustrative=True)


# 16.7
def s16_7_correct():
    r = R['16.7']
    extra = '.alt{margin-top:8px;max-width:34rem}'
    def one(crop, w, alt, lab):
        return (f'<div class="fig {w}">{photo("rotunda-2005", alt, "ph", crop)}<p class="lab mt8">{lab}</p>'
                f'<p class="alt sm"><span class="lab">{r["alt_head"]}</span> {alt}</p></div>')
    html = (css(extra) + '<div class="w"><div class="row">' + one((60, 0, 1080, 720), 'w360', W['alt_rotunda'], r['labels'][0])
            + one((0, 77, 576, 720), 'w280', r['alt_tight'], r['labels'][1]) + f'</div>{cap(r["shared_caption"])}</div>')
    return spec('s-16-7-correct', html, '16.7', r['correct_alt'],
                notes='Each printed alt text is the same words as its <img> alt.')


def s16_7_failure():
    r = R['16.7']
    html = (css('.alt{margin-top:8px;max-width:34rem}') + '<div class="w"><div class="fig w280">'
            f'{photo("rotunda-2005", W["alt_rotunda"], "ph", (0, 77, 576, 720))}{cap(W["cap_rotunda"])}'  # ED10-4: one fault a plate
            f'<p class="lab mt8">{r["labels"][1]}</p>'
            f'<p class="alt sm"><span class="lab">{r["alt_head"]}</span> {W["alt_rotunda"]}</p></div></div>')
    return spec('s-16-7-failure', html, '16.7', r['failure_alt'])


# 16.8
def plh_words(r, meta):
    return (f'<div><p class="lab">{r["label"]}</p><p class="lab sec">{r["kind"]}</p></div>'
            f'<p class="sm">{r["shot"]}</p><p class="lab sec">{meta}</p>')


def s16_8_correct():
    r = R['16.8']
    html = (css() + '<div class="w"><div class="row">'
            f'<div class="fig w540"><div class="out">{plh("r32", plh_words(r, r["meta"]))}</div>{cap(r["cap"])}</div>'
            f'<div class="dk"><div class="fig w240"><div class="out">{plh("r45", plh_words(r, r["meta_45"]), "tight")}</div>'
            f'<p class="cap sec">{r["cap"]}</p></div></div></div></div>')
    return spec('s-16-8-correct', html, '16.8', r['correct_alt'])


def s16_8_failure():
    r = R['16.8']
    extra = ('.v5{position:relative;aspect-ratio:3/2;background:var(--oa-color-palette-stone)}'
             '.v5b{position:absolute;left:12px;bottom:12px;padding:6px 10px;background:var(--oa-color-palette-newsprint);'
             'color:var(--oa-color-palette-charcoal)}')
    html = (css(extra) + '<div class="w"><div class="w540"><div class="v5">'
            f'<p class="v5b"><span class="lab">{r["v5_meta"]}</span><br><span class="sm">{r["v5_cap"]}</span></p></div></div></div>')
    return spec('s-16-8-failure', html, '16.8', r['failure_alt'], readable=False,
                notes='Our fifth edition’s panel, redrawn as a picture: an image stage, so the guide’s own reader hears its alt.')


# 16.9
TAB = (f'.tab{{position:absolute;top:0;left:0;padding:4px 8px;background:var(--oa-color-surface-charcoal);'
       f'color:var(--oa-color-text-primary-on-charcoal);{ty("label")}}}.pt48{{padding-top:48px}}')


def s16_9_correct():
    r = R['16.9']
    inner = (f'<p class="tab">{r["tab"]}</p><p class="sm">{r["prompt"]}</p>')
    html = (css(TAB) + f'<div class="w"><div class="w540"><p class="lab">{r["head"]}</p><div class="out mt8">'
            + plh('r32', inner, 'pt48') + f'</div>{cap(r["caption"])}<p class="sm sec mt8">{r["record"]}</p></div></div>')
    return spec('s-16-9-correct', html, '16.9', r['correct_alt'],
                notes='No generated image: the studio’s call for chat 10. The tab sits where it sits on a real one.')


def s16_9_failure():
    r = R['16.9']
    a, b, c_ = r['fail_caption']
    inner = f'<p class="lab">{R["16.8"]["label"]}</p><p class="sm">{r["fail_plh"]}</p>'
    html = (css() + '<div class="w"><div class="w540"><div class="out">' + plh('r32', inner) + '</div>'
            f'{cap(f"{a} {b} {ILLUS} {c_}")}</div></div>')
    return spec('s-16-9-failure', html, '16.9', r['failure_alt'], illustrative=True)


def s16_kinds():
    x = EXTRA_KINDS
    h = x['head']
    rows = ''.join('<tr>' + ''.join(f'<td{" class=\"k\"" if i == 0 else ""} data-k="{h[i]}">{v}</td>' for i, v in enumerate(row))
                   + '</tr>' for row in x['rows'])
    html = (css() + '<div class="w"><table class="tb"><thead><tr>' + ''.join(f'<th scope="col">{v}</th>' for v in h)
            + f'</tr></thead><tbody>{rows}</tbody></table></div>')
    return spec('s-16-picture-kinds', html, None, x['alt'])


# 16.10 to 16.13, the video example
VF = (f'.sb{{display:grid;grid-template-columns:minmax(0,1fr);gap:24px 16px;align-items:start;max-width:22rem}}'
      f'@media (min-width:48em){{.sb{{grid-template-columns:repeat(3,minmax(0,200px));gap:24px 32px;max-width:none}}}}'
      f'.vf{{position:relative;aspect-ratio:16/9;border:1px solid var(--oa-color-border-strong);padding:10px;display:flex;'
      f'flex-direction:column;justify-content:space-between;gap:4px;overflow:hidden;{ty("label")};text-transform:none;letter-spacing:0}}'
      '.vf.dkf{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);border-color:var(--oa-color-surface-charcoal)}'
      '.vf .slot{color:var(--oa-color-text-secondary-on-charcoal)}'
      '.np{align-self:flex-start;padding:2px 6px;background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal)}'
      f'.ask{{align-self:flex-start;padding:6px 10px;{ty("ask")};background:var(--oa-color-action-ask-fill-on-newsprint);'  # quick check: the ask's own type, as Rule 18.2's button
      f'color:var(--oa-color-action-ask-label-on-newsprint);box-shadow:inset 0 0 0 1px var(--oa-component-button-ask-keyline-on-newsprint)}}'
      '.said{margin-top:8px}')


def frame(t, kind, label, said, r):
    """One storyboard frame at 16:9: its start time above, its picture in type and tokens, the words said below."""
    if kind == 'title':
        box = f'<div class="vf dkf"><span>{r["question"]}</span><span class="slot">{r["slot"]}</span></div>'
    elif kind == 'end':
        box = f'<div class="vf dkf"><span>{label}</span><span class="slot">{r["slot"]}</span></div>'
    elif kind == 'host':
        box = f'<div class="vf"><span>{label}</span><span class="np">{r["name_plate"]}</span></div>'
    elif kind == 'step':
        box = (f'<div class="vf"><span class="sec">{r["step_head"]}</span>'
               f'<span class="ask" data-red="working" data-red-job="ask">{label}</span></div>')
    elif kind == 'logo':
        box = f'<div class="vf dkf"><span>{label}</span></div>'
    else:
        box = f'<div class="vf"><span>{label}</span></div>'
    words = f'<p class="said sm">{said}</p>' if said else ''
    return f'<div><p class="lab num">{t}</p><div class="mt8">{box}</div>{words}</div>'


def s16_10_correct():
    r = R['16.10']
    cells = ''.join(frame(t, k, lab, s, r) for t, k, lab, s in r['frames'])
    html = css(VF) + f'<div class="w"><p class="mt8" style="margin-bottom:16px">{ILLUS}</p><div class="sb">{cells}</div></div>'
    return spec('s-16-10-correct', html, '16.10', r['correct_alt'], illustrative=True,
                notes='The video is not made, so the plate carries the Illustrative label at its head; every figure is '
                      'chart S04’s (work/build/chart-kit/specs/s04.json). The step frame holds the view’s one working red.')


def s16_10_failure():
    r = R['16.10']
    cells = ''.join(frame(t, k, lab, s, r) for t, k, lab, s in r['fail_frames'])
    html = css(VF) + f'<div class="w"><p style="margin-bottom:16px">{ILLUS}</p><div class="sb">{cells}</div></div>'
    return spec('s-16-10-failure', html, '16.10', r['failure_alt'], illustrative=True)


CAPF = ('.v9{position:relative;width:270px;max-width:100%;aspect-ratio:9/16;border:1px solid var(--oa-color-border-strong);flex:none}'
        '.v9 .in{position:absolute;left:16px;right:16px;top:16px}'
        '.safe{position:absolute;left:4%;right:4%;top:62%;bottom:20%;border:1px solid var(--oa-color-border-hairline);'
        'display:flex;flex-direction:column;justify-content:flex-end;gap:6px;padding:6px}'
        '.safe .lab{color:var(--oa-color-text-secondary);text-transform:none;letter-spacing:0}'
        f'.cb{{background:var(--oa-color-surface-charcoal);color:var(--oa-color-text-primary-on-charcoal);padding:4px;white-space:nowrap;'
        f'{ty("dataLabel")};text-align:center}}'
        f'.code{{margin:0;padding:16px;border:1px solid var(--oa-color-border-hairline);{ty("bodySmall")};white-space:pre;'
        'font-variant-numeric:tabular-nums;overflow-x:auto;max-width:100%}')


def vertical(r, lines, bad=False):
    cap_lines = '<br>'.join(lines)
    ill = f' {ILLUS}' if bad else ''
    return (f'<div><p class="lab">{r["scale_note"]}</p><div class="v9 mt8"><p class="in sm">{r["plh"]}</p>'
            f'<div class="safe"><p class="lab">{r["safe"]}</p><p class="cb">{cap_lines}</p></div></div>'
            + (f'<p class="mt8">{ill.strip()}</p>' if bad else '') + '</div>')


def s16_11_correct():
    r = R['16.11']
    html = (css(CAPF) + '<div class="w"><div class="row">' + vertical(r, r['lines'])
            + f'<div style="min-width:0;max-width:26rem"><p class="lab">{r["file_head"]}</p><pre class="code mt8" tabindex="0" role="region" aria-label="{r["file_head"]}"><code>{r["vtt"]}</code></pre></div>'
            '</div></div>')
    return spec('s-16-11-correct', html, '16.11', r['correct_alt'], illustrative=True,
                notes='Drawn at a quarter of 1080 by 1920, so the caption band’s 13 px words stand for about 52 px on the '
                      'real frame; chapter 23 sets the real size. The video is not made.')


def s16_11_failure():
    r = R['16.11']
    html = css(CAPF) + '<div class="w">' + vertical(r, r['bad_lines'], bad=True) + '</div>'
    return spec('s-16-11-failure', html, '16.11', r['failure_alt'], illustrative=True)


TR = (f'.tx{{margin-top:24px;max-width:40rem}}.tx .lnk{{text-decoration:underline;text-underline-offset:0.2em}}')


def s16_12_correct():
    r = R['16.12']
    h = r['head']
    rows = ''.join(f'<tr><td data-k="{h[0]}">{a}</td><td data-k="{h[1]}">{b}</td></tr>' for a, b in r['rows'])
    html = (css(TR) + f'<div class="w"><p style="margin-bottom:16px">{ILLUS}</p><table class="tb"><thead><tr>'
            + ''.join(f'<th scope="col">{x}</th>' for x in h) + f'</tr></thead><tbody>{rows}</tbody></table>'
            f'<div class="tx"><p class="lab">{r["transcript_head"]}</p><p class="sm mt8">{r["transcript"]}</p>'
            f'<p class="sm mt8"><a class="lnk" href="#rule-14-19">{r["link"]}</a></p></div></div>')
    return spec('s-16-12-correct', html, '16.12', r['correct_alt'], illustrative=True,
                notes='The link goes to chart S04’s rule in chapter 14, where its table opens.')


def s16_12_failure():
    r = R['16.12']
    h = r['head']
    a, b = r['bad_row']
    html = (css() + f'<div class="w"><table class="tb"><thead><tr>' + ''.join(f'<th scope="col">{x}</th>' for x in h)
            + f'</tr></thead><tbody><tr><td data-k="{h[0]}">{a}</td><td data-k="{h[1]}">{b} {ILLUS}</td></tr></tbody></table></div>')
    return spec('s-16-12-failure', html, '16.12', r['failure_alt'], illustrative=True)


CARD = (f'.vc{{max-width:540px}}.pst{{position:relative;aspect-ratio:16/9;background:var(--oa-color-surface-charcoal);'
        f'color:var(--oa-color-text-primary-on-charcoal);padding:24px;display:flex;align-items:flex-end}}'
        f'.pq{{{ty("h3")};max-width:22rem;text-wrap:balance}}'
        '.l8{position:absolute;top:24px;right:24px;line-height:0}'
        f'.vt{{{ty("h4")};margin-top:16px;text-wrap:balance}}'
        '.ctl{display:flex;flex-wrap:wrap;align-items:center;gap:12px 24px;margin-top:16px}'
        f'.btn{{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 16px 0 12px;'
        f'border:1px solid var(--oa-color-border-strong);{ty("ui")}}}'
        '.ui{display:block;flex:none;fill:none;stroke:currentColor;stroke-width:var(--oa-component-icon-utility-line-medium);'
        'stroke-linecap:round;stroke-linejoin:round}'
        f'.lk{{{ty("ui")};text-decoration:underline;text-underline-offset:0.2em;display:inline-flex;align-items:center;gap:4px}}'
        '.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}')


def s16_13_correct():
    r = R['16.13']
    l8 = ('<span class="l8"><img data-inline src="work/build/assets/identity/lockups/20261028_L8-Monogram-Master.svg" '
          'alt="Oath &amp; Action" width="48" height="17.3" data-red="signature" '
          'style="color:var(--oa-color-text-primary-on-charcoal);--amp:var(--oa-color-identity-signature-on-charcoal)"></span>')
    html = (css(CARD) + f'<div class="w"><div class="vc"><div class="pst">{l8}<p class="pq">{r["title_text"]}</p></div>'
            f'<p class="vt">{r["title_text"]} {ILLUS}</p><p class="sm sec num mt8">{r["length"]}</p>'
            f'<p class="sm mt8">{r["summary"]}</p><div class="ctl">'
            f'<span class="btn">{uicon("play")}{r["play"]}</span>'
            f'<span class="lk">{r["links"][0]}</span>'
            f'<span class="lk">{r["links"][1]}{uicon("another-site", 16)}<span class="vh">{r["another_site"]}</span></span>'
            '</div></div></div>')
    return spec('s-16-13-correct', html, '16.13', r['correct_alt'], illustrative=True,
                notes='Controls drawn as text, since nothing can load in the guide; L8 from its master, 48 px wide, 24 px '
                      'in from the poster’s top and right edges (Rule 12.3).')


def s16_13_failure():
    r = R['16.13']
    extra = ('.dead{aspect-ratio:16/9;max-width:540px;background:var(--oa-color-surface-charcoal);display:flex;'
             'align-items:center;justify-content:center}.dead p{color:var(--oa-color-palette-stone)}')
    html = css(extra) + f'<div class="w"><div class="dead"><p class="sm">{r["unavailable"]}</p></div></div>'
    return spec('s-16-13-failure', html, '16.13', r['failure_alt'], exempt=['contrast'],
                notes='Picture of a fault: Stone words on Charcoal, 3.10 to 1, as the empty player it copies.')


PLATES = [s_opener, s16_1_correct, s16_1_failure, s16_2_correct, s16_2_failure, s16_3_correct, s16_3_failure,
          s16_4_correct, s16_4_failure, s16_5_correct, s16_5_failure, s16_6_correct, s16_6_failure, s16_7_correct,
          s16_7_failure, s16_8_correct, s16_8_failure, s16_9_correct, s16_9_failure, s16_kinds, s16_10_correct,
          s16_10_failure, s16_11_correct, s16_11_failure, s16_12_correct, s16_12_failure, s16_13_correct, s16_13_failure]


# ------------------------------------------------------------------------------------------------ the chapter
def build_chapter():
    for f in PLATES:
        f()
    rules = []
    for rid in sorted(R, key=lambda k: int(k.split('.')[1])):
        r = R[rid]
        sid = 's-16-' + rid.split('.')[1]
        specs = []
        for s in r['specs']:
            d = {'label': s[0], 'value': s[1]}
            if len(s) > 2:
                d['token'] = s[2]
            specs.append(d)
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
        'number': CH, 'anchor': 'photography', 'title': W['title'], 'part': 'evidence', 'opener': 's-16-opener',
        'instruction': W['instruction'], 'intro': W['intro'],
        'groups': [{'before_rule': b, 'number': i, 'title': t, 'line': l} for i, (b, t, l) in enumerate(W['groups'], 1)],
        'rules': rules,
        'extras': [{'after_rule': '16.9', 'specimen': 's-16-picture-kinds', 'label': EXTRA_KINDS['label'],
                    'caption': EXTRA_KINDS['caption']}],
        'related_chapters': [{'chapter': c, 'reason': t} for c, t in W['related_chapters']],
        'sources': W['sources'],
    }
    return ch


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build in memory and report; write nothing')
    a = ap.parse_args()
    ch = build_chapter()
    B.check_chapter(ch)
    used = {ch['opener']} | {x['specimen'] for x in ch['extras']}
    for rr in ch['rules']:
        used |= {rr['correct']['specimen'], rr['failure']['specimen']}
    ours = set(ctx.specs)
    if used - ours or ours - used:
        raise SystemExit(f'specimens missing {sorted(used - ours)} unused {sorted(ours - used)}')
    for sid, s in ctx.specs.items():
        bad = GP.placed_by_path(s['html'])
        if bad:
            raise SystemExit(f'{sid} places a photograph by path: {bad}')
    total = sum(len(s['html'].encode()) for s in ctx.specs.values())
    uses = sum(s['html'].count('data-oa-photo=') for s in ctx.specs.values())
    print(f'chapter 16: {len(ch["rules"])} rules, {len(ctx.specs)} specimens ({total:,} bytes), {uses} photograph uses; '
          f'Rule 16.4 ground {LOW} to 1, {UNDER3} percent under 3 to 1')
    if a.check:
        return
    OUT_CH.write_text(json.dumps(ch, indent=2, ensure_ascii=False) + '\n')
    for p in OUT_SP.glob('s-16-*.html'):
        if p.stem not in ours:
            p.unlink()
    for sid, s in ctx.specs.items():
        (OUT_SP / f'{sid}.html').write_text(s['html'])
    MANIFEST.write_text(json.dumps(dict(sorted((k, v['meta']) for k, v in ctx.specs.items())), indent=1,
                                   ensure_ascii=False) + '\n')
    print(f'wrote {OUT_CH.relative_to(ROOT)}, {len(ctx.specs)} specimens, {MANIFEST.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
