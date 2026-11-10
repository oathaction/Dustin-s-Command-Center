#!/usr/bin/env python3
"""Promote the 18 approved utility icons to finals in work/build/assets/utility/ (promotion brief, November 10, 2026).

Written by the icon designer, utility hand, November 10, 2026, under 20261110_Promotion-Brief.md.

Dustin approved every card on the stage B drawings board by name (DR-161 to DR-178). Each final is its approved
option's file with three changes only: the file name, the root attributes (no data-option; the brief's data-icon
name) and the comment. Every drawing element is copied byte for byte. The option files stay where they are, as the
record (D2-718).

Usage:
  python3 -I work/build/scripts/phase-2/utility_icons_promote.py [--report DIR] [--review DIR]

  (no flags)    write svg-24/, svg-16/, the manifest and png/ (1x and 2x previews, Charcoal on a clear ground, drawn
                the way utility_icons_render.js drew the options' previews), then compare every final with its
                approved option file and every preview with the option's preview; exits 1 on any difference
  --report DIR  also write the comparison as JSON to DIR (a scratch folder, outside work/build)
  --review DIR  also draw review sheets to DIR: every final at true size on Newsprint and Charcoal at device scale 1
                and 2, the turned and mirrored states beside them, and nearest-neighbour enlargements of each sheet;
                and write the turned and mirrored copies there as SVGs for the checks

The PNG previews and review sheets need Chromium, which this environment has for Node only, so the script runs a
short Node program (below) through Playwright, as icon_pixel_fit_check.py does.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

DATE = '20261110'
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
SRC = os.path.join(ROOT, 'work', 'build', 'assets', 'utility-icons')
OUT = os.path.join(ROOT, 'work', 'build', 'assets', 'utility')
INK = '#121212'
NEWSPRINT = '#DCD9D2'
LINE = {24: '2', 16: '1.5'}

# The 18 approved picks, in the audit's order (section 1.1). Name is the file name's title case; the data-icon is
# U- and the name in lower case (brief, "Folder and naming conventions"). Words, uses, states and targets are the
# accessibility audit's, section 1.2, cut to what a builder needs beside the file.
PICKS = [
    {
        'name': 'Close', 'option': 'A', 'dr': 'DR-162', 'rank': '1', 'action': 'Close',
        'drawing': 'A bare cross',
        'word': 'Close, extended when two things could close: "Close the menu", "Close full size", "Close the report reader"',
        'word_rule': 'The word always shows, except for the clear control inside a search field, which is named "Clear the search" and takes its context from the field label',
        'uses': ["The guide's phone menu", 'The atlas detail panel', 'The atlas full-size view ("Close full size")',
                 'The report reader', 'Every dialog', 'The clear control in a search field'],
        'states': 'None. Escape does the same wherever the control closes a dialog',
        'target': '44 by 44 px',
    },
    {
        'name': 'Menu', 'option': 'A', 'dr': 'DR-163', 'rank': '2', 'action': 'Open the menu',
        'drawing': 'Three even bars',
        'word': 'Menu',
        'word_rule': 'The word always shows',
        'uses': ["The guide's masthead under 64em (the engineer swaps the shell's glyph for this one)",
                 "The site's phone masthead", "The report reader's phone masthead"],
        'states': 'Closed and open, carried by aria-expanded. The bars stay bars when the menu opens; the open menu has its own Close',
        'target': '44 px tall',
    },
    {
        'name': 'Arrow', 'option': 'A', 'dr': 'DR-164', 'rank': '3, 4, 16',
        'action': 'Next; Previous (mirrored); the sort order in use (turned)',
        'drawing': 'An arrow with a shaft and an open head, pointing right',
        'word': 'Next or Previous with its object ("Next page", "Previous step", "Next chapter, 02 Voice"); in a sorted column, the heading\'s word',
        'word_rule': 'The word always shows',
        'uses': ["The guide's chapter foot (\"Next 02 Voice\")", "The report reader's page controls",
                 'The atlas stepper ("Previous step", "Next step")', 'Any carousel',
                 'The column in use in a sortable table: the chapter 27 asset table, the tracker\'s list of bills, the atlas reform list, a table view of the symbol library'],
        'states': 'Available, and unavailable at either end: the control keeps focus with aria-disabled="true", takes the subtle ink and a dashed outline, and says why in words ("This is the first page")',
        'target': '44 by 44 px; in a column heading, the heading button, 44 px tall',
    },
    {
        'name': 'Chevron', 'option': 'A', 'dr': 'DR-165', 'rank': '5', 'action': 'Expand and collapse',
        'drawing': 'A chevron pointing down',
        'word': "The row's own words; the atlas panel keeps \"More\" and \"Less\"",
        'word_rule': 'The row\'s words always show. The state comes from aria-expanded or a native details element, so "expand" never enters the name',
        'uses': ['The atlas: 47 disclosures on one page, and the detail panel\'s More and Less',
                 "The symbol library's family groups", 'Report source notes', 'The phone filter sheet',
                 "Chapter 18's disclosures"],
        'states': 'Closed (pointing down, as drawn) and open (turned half round, pointing up)',
        'target': 'The whole row, 44 px tall',
    },
    {
        'name': 'Download', 'option': 'A', 'dr': 'DR-166', 'rank': '6', 'action': 'Download',
        'drawing': 'An arrow down into an open tray',
        'word': '"Download", then the file, type and size, as in "Download tokens.css, CSS, 41 KB"; the type and size are visible text',
        'word_rule': 'The word always shows',
        'uses': ['The guide\'s links to tokens.css (9 today)', 'Chapter 27, every file by size and surface',
                 'Each color matrix cell', 'The report PDF', 'Any atlas data file'],
        'states': 'Available, and unavailable: the control keeps focus with aria-disabled="true" and shows its reason',
        'target': '44 px tall',
    },
    {
        'name': 'Another-Site', 'option': 'A', 'dr': 'DR-167', 'rank': '7', 'action': 'Go to another site',
        'drawing': 'An arrow leaving a box by its top right corner',
        'word': 'The link\'s own words, with visually hidden words added to its name: " (another site)", or " (opens in a new tab)" for a link that does open a new tab',
        'word_rule': 'The glyph follows the last word and never wraps onto a line of its own. These links open in the same tab',
        'uses': ['Source links in the atlas', 'Report source notes', 'Chapters 13 and 15',
                 'The official sources behind the tracker workflows (congress.gov and the rest)'],
        'states': 'None',
        'target': 'Inside running text, the line box, at least 24 px tall (the inline exception of WCAG 2.2 SC 2.5.8); in a list of sources, 44 px tall',
    },
    {
        'name': 'Search', 'option': 'A', 'dr': 'DR-168', 'rank': '8', 'action': 'Search',
        'drawing': 'A magnifier with its handle to the lower right',
        'word': 'The field\'s visible label, such as "Search the symbols", or "Search" on a masthead button. Placeholder text is never the label',
        'word_rule': 'The glyph inside the field is hidden',
        'uses': ['The chapter 10 symbol library (124 drawings)', 'The site',
                 'The atlas (51 variables, 50 reforms and 23 loops)', 'Any later search across the guide'],
        'states': 'Empty; holding text, when the clear control appears; results, announced in a polite live region ("3 of 124 symbols"); and no match, in words with a next step',
        'target': 'Field and button 44 px tall',
    },
    {
        'name': 'Filter', 'option': 'A', 'dr': 'DR-169', 'rank': '9', 'action': 'Filter',
        'drawing': 'A funnel with a slanted spout',
        'word': '"Filters" with the count of active ones, in visible text: "Filters, 2 on"',
        'word_rule': 'The word always shows',
        'uses': ['The chapter 10 library filter bar (family, size, surface)', "Chapter 11's filter bar specimen",
                 'The atlas lists (problems by area, reforms by route)', 'The tracker (bills by step and state)',
                 'The chapter 27 asset table', 'On a phone, the one button that opens the filter sheet'],
        'states': 'The sheet closed and open (aria-expanded); the count; each chip on or off (aria-pressed), with the Selected check shown when on',
        'target': '44 px tall, chips included',
    },
    {
        'name': 'Copy', 'option': 'A', 'dr': 'DR-170', 'rank': '10', 'action': 'Copy',
        'drawing': 'Two square sheets, the back one up and to the left',
        'word': '"Copy" and what, as in "Copy #121212, Charcoal"',
        'word_rule': 'The word always shows',
        'uses': ['The guide\'s "Copy this chapter\'s CSS" buttons (9 today)',
                 'Hex values and token names in chapters 05 and 06', 'Code blocks', 'File paths in chapter 27',
                 '"Copy link to this rule", if the shell adds it'],
        'states': 'Idle. The result goes to the status line in words, with the Success mark or the Error mark. The glyph never flips to a check',
        'target': '44 px tall',
    },
    {
        'name': 'Play', 'option': 'A', 'dr': 'DR-171', 'rank': '11', 'action': 'Play (one button with Pause)',
        'drawing': 'A triangle pointing right',
        'word': '"Play", or "Play again" when the run has ended; the word changes with the glyph',
        'word_rule': 'The word always shows. The button does not also use aria-pressed, since its name changes',
        'uses': ['The atlas stepper (Play, Pause, Play again)',
                 "Chapter 17's reader-controlled motion (the hinge, the lever landing)", 'Video in chapters 16 and 23'],
        'states': 'Stopped, playing, ended. Playback starts only on a press, with or without reduced motion',
        'target': '44 by 44 px',
        'pair': 'U-pause',
    },
    {
        'name': 'Pause', 'option': 'A', 'dr': 'DR-171', 'rank': '11', 'action': 'Pause (one button with Play)',
        'drawing': 'Two upright bars',
        'word': '"Pause"; the word changes with the glyph',
        'word_rule': 'The word always shows. The button does not also use aria-pressed, since its name changes',
        'uses': ['The atlas stepper (Play, Pause, Play again)',
                 "Chapter 17's reader-controlled motion (the hinge, the lever landing)", 'Video in chapters 16 and 23'],
        'states': 'Shown while playing; the same button shows Play when stopped or ended',
        'target': '44 by 44 px',
        'pair': 'U-play',
    },
    {
        'name': 'Reset', 'option': 'B', 'dr': 'DR-172', 'rank': '12', 'action': 'Reset, start over',
        'drawing': 'Three quarters of a circle with an upright corner head at the upper left',
        'word': '"Reset" or "Start over", plus the object where needed ("Reset the loop", "Reset to the default")',
        'word_rule': 'The word always shows. Clearing filters is a different action and stays a word, "Clear filters"',
        'uses': ["The atlas stepper's row (Play, Previous step, Next step, Reset)", "Chapter 17's motion demos",
                 'The tracker\'s settings ("Reset to the default")'],
        'states': 'Available, and unavailable at the start, with aria-disabled="true" and the reason ("Already at the start")',
        'target': '44 by 44 px',
    },
    {
        'name': 'Error', 'option': 'A', 'dr': 'DR-173', 'rank': '13', 'action': 'Error mark',
        'drawing': 'An exclamation mark in a circle',
        'word': 'The message beside it, which names the field and the fix ("Enter a ZIP code with five digits.")',
        'word_rule': 'The words always show. The mark is hidden; the field carries aria-invalid="true" and aria-describedby to the message',
        'uses': ['Form errors: the newsletter sign-up, the tracker\'s settings, the chapter 11 and chapter 18 form specimens',
                 "The guide's copy failure line (the shell's is-error)", 'A page that cannot load its data'],
        'states': 'None. An error is the view\'s first red job under Rule 05.3; the file draws in currentColor and the page sets its ink',
        'target': 'Not a target',
    },
    {
        'name': 'Success', 'option': 'B', 'dr': 'DR-174', 'rank': '14', 'action': 'Success mark',
        'drawing': 'A check leaving an open circle',
        'word': 'The status text beside it, which says what happened ("Copied 12 lines to the clipboard.", "You\'re signed up.")',
        'word_rule': 'The words always show. The mark is hidden',
        'uses': ['The copy result line', 'A sent form', 'Saved tracker settings',
                 'A finished download, where the page reports it'],
        'states': 'None',
        'target': 'Not a target',
    },
    {
        'name': 'Selected-Check', 'option': 'A', 'dr': 'DR-175', 'rank': '14',
        'action': 'Selected check (a chip or list choice that is on)',
        'drawing': 'A check',
        'word': "The chip's or the choice's own word",
        'word_rule': 'The word always shows. The check is hidden; the state comes from aria-pressed="true"',
        'uses': ['A filter chip that is on', 'A list choice that is on'],
        'states': 'Shown when on, so the selected state does not rest on color (WCAG 2.2 SC 1.4.1)',
        'target': 'Not a target; a chip is 44 px tall',
    },
    {
        'name': 'View-Full-Size', 'option': 'A', 'dr': 'DR-176', 'rank': '15', 'action': 'View full size',
        'drawing': 'Four corners',
        'word': 'The visible words, as built: "View the map full size", "View the drawing full size", "View the loop full size"',
        'word_rule': 'The words always show. Leaving full size uses Close and the words "Close full size"',
        'uses': ['The atlas, on phones (the map, a drawing, a loop)', "The report reader's full-size choice"],
        'states': 'Closed and open; open is a modal dialog that returns focus to this button',
        'target': '44 px tall',
    },
    {
        'name': 'Sort', 'option': 'A', 'dr': 'DR-177', 'rank': '16', 'action': 'Sort a column (can sort)',
        'drawing': 'An up arrow and a down arrow side by side',
        'word': "The column heading's word, on a button inside the th",
        'word_rule': 'The heading\'s word always shows. The order comes from aria-sort on the th, and a polite status line says it in words ("Sorted by date, newest first")',
        'uses': ['The chapter 27 asset table', "The tracker's list of bills", 'The atlas reform list',
                 'A table view of the symbol library'],
        'states': 'Can sort (this mark). The column in use shows the Arrow turned up or down instead',
        'target': 'The heading button, 44 px tall',
    },
    {
        'name': 'Warning', 'option': 'A', 'dr': 'DR-178', 'rank': '17', 'action': 'Warning mark',
        'drawing': 'An exclamation mark in a triangle, in ink',
        'word': 'The notice beside it ("This record was checked October 15, 2026. The agency may have acted since.")',
        'word_rule': 'The words always show. The mark is hidden',
        'uses': ['A record last checked before its latest action', 'Data the page could not refresh',
                 'A browser feature the page needs and lacks'],
        'states': 'None. Drawn in ink, never red. It never marks an evidence grade, a contested link or an Illustrative label, which have their own encodings (chapters 13 and 15)',
        'target': 'Not a target',
    },
]

# Turns and mirrors (D2-652, D2-653, D2-556). Each transform goes on a <g> around the drawing, or as a CSS transform
# about the box's centre. Every one keeps the straight lines on the grid: at 16 px the turned-down arrow is a
# mirror across the diagonal, so its shaft sits on x = 7.75 like the turned-up one (D2-649), where a quarter turn
# about the centre would put it on x = 8.25.
TURNS = {
    'Arrow': [
        {'use': 'Next', 'how': 'As drawn, pointing right', 'transform': {'24': None, '16': None}, 'variant': None},
        {'use': 'Previous', 'how': 'Mirrored left to right about the centre', 'variant': 'Previous',
         'transform': {'24': 'matrix(-1 0 0 1 24 0)', '16': 'matrix(-1 0 0 1 16 0)'}},
        {'use': 'Sort order in use, pointing up', 'how': 'Turned a quarter round anticlockwise', 'variant': 'Up',
         'transform': {'24': 'rotate(-90 12 12)', '16': 'rotate(-90 8 8)'}},
        {'use': 'Sort order in use, pointing down', 'how': 'Turned a quarter round clockwise; at 16 px, mirrored across the diagonal so the shaft stays on x = 7.75',
         'variant': 'Down', 'transform': {'24': 'rotate(90 12 12)', '16': 'matrix(0 1 1 0 0 0)'}},
    ],
    'Chevron': [
        {'use': 'Closed', 'how': 'As drawn, pointing down', 'transform': {'24': None, '16': None}, 'variant': None},
        {'use': 'Open', 'how': 'Turned half round, pointing up. The swap is immediate under reduced motion, and otherwise a turn of no more than 200 ms (--oa-motion-duration-standard)',
         'variant': 'Open', 'transform': {'24': 'rotate(180 12 12)', '16': 'rotate(180 8 8)'}},
    ],
}
TURN_DECISIONS = {'Arrow': ['D2-652', 'D2-555'], 'Chevron': ['D2-653', 'D2-556']}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rel(p):
    return os.path.relpath(p, ROOT)


def src_name(p, size):
    return '20261109_Utility-%s-Option-%s-%dpx.svg' % (p['name'], p['option'], size)


def final_name(p, size):
    return '%s_Utility-%s-%dpx.svg' % (DATE, p['name'], size)


def icon_id(p):
    return 'U-' + p['name'].lower()


def comment(p, size):
    return ('<!-- Oath & Action utility icon: %s, %d px master, final. %s. %d-unit grid, %s px line, round caps and '
            'joins, currentColor, no red. The final approved on the stage B drawings board: Dustin approved option %s '
            'by name on November 10, 2026 (%s). Its drawing is the approved option file, %s, unchanged. -->'
            % (p['name'].replace('-', ' '), size, p['drawing'], size, LINE[size], p['option'], p['dr'],
               src_name(p, size)))


def split(text):
    """Root tag, comment line and the drawing (every byte after the comment) of a utility SVG."""
    m = re.match(r'(<svg\b[^>]*>)\n(  <!--[^\n]*-->)\n(.*)\Z', text, re.S)
    if not m:
        raise SystemExit('unexpected layout: the file does not open with its root tag and one comment line')
    return m.group(1), m.group(2), m.group(3)


def final_root(src_root, p):
    root = re.sub(r' data-option="[A-C]"', '', src_root, count=1)
    root = re.sub(r'data-icon="U-[a-z-]+"', 'data-icon="%s"' % icon_id(p), root, count=1)
    return root


def attrs(tag):
    return dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))


def elements(text):
    """Every element under the root, in order, as (tag, attributes), and the root's attributes."""
    root = ET.fromstring(text)
    return root.attrib, [(e.tag, dict(sorted(e.attrib.items()))) for e in root.iter() if e is not root]


def promote():
    results = []
    for sub in ('svg-24', 'svg-16', 'png'):
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    for p in PICKS:
        for size in (24, 16):
            sp = os.path.join(SRC, 'svg-%d' % size, src_name(p, size))
            fp = os.path.join(OUT, 'svg-%d' % size, final_name(p, size))
            sb = open(sp, 'rb').read()
            s_root, s_comment, s_body = split(sb.decode('utf-8'))
            out = final_root(s_root, p) + '\n  ' + comment(p, size) + '\n' + s_body
            with open(fp, 'w', newline='') as fh:
                fh.write(out)
            results.append((p, size, sp, fp))
    return results


def compare(results):
    rows, bad = [], 0
    for p, size, sp, fp in results:
        sb, fb = open(sp, 'rb').read(), open(fp, 'rb').read()
        s_root, _, s_body = split(sb.decode('utf-8'))
        f_root, f_comment, f_body = split(fb.decode('utf-8'))
        s_attr, s_el = elements(sb.decode('utf-8'))
        f_attr, f_el = elements(fb.decode('utf-8'))
        changed = {k: [s_attr.get(k), f_attr.get(k)] for k in sorted(set(s_attr) | set(f_attr))
                   if s_attr.get(k) != f_attr.get(k)}
        expect = {'data-option': [p['option'], None]}
        if s_attr.get('data-icon') != icon_id(p):
            expect['data-icon'] = [s_attr.get('data-icon'), icon_id(p)]
        n_d = sum(1 for t, a in s_el if 'd' in a)
        n_shape = sum(1 for t, a in s_el if t.endswith('circle'))
        row = {
            'icon': icon_id(p), 'size': size, 'source': rel(sp), 'final': rel(fp),
            'source_sha256': sha(sb), 'final_sha256': sha(fb),
            'drawing_sha256_source': sha(s_body.encode()), 'drawing_sha256_final': sha(f_body.encode()),
            'drawing_bytes_equal': s_body == f_body,
            'elements_equal': s_el == f_el, 'elements': len(s_el), 'paths_with_d': n_d, 'circles': n_shape,
            'root_attributes_changed': changed, 'root_changes_as_planned': changed == expect,
            'root_tag_rest_equal': final_root(s_root, p) == f_root,
            'ids_in_file': len(re.findall(r'\sid="', fb.decode())),
            'comment_names_dr': p['dr'] in f_comment and 'drawings board' in f_comment,
        }
        ok = (row['drawing_bytes_equal'] and row['elements_equal'] and row['root_changes_as_planned']
              and row['root_tag_rest_equal'] and row['comment_names_dr'] and '\u2014' not in fb.decode())
        row['pass'] = ok
        bad += 0 if ok else 1
        rows.append(row)
    return rows, bad


# ---------------------------------------------------------------------------------------------- Chromium (Node)
NODE_PROGRAM = r"""
'use strict';
const fs = require('fs');
const { chromium } = require('playwright');
const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const strip = (t) => t.replace(/<!--[\s\S]*?-->/g, '');
(async () => {
  const browser = await chromium.launch();
  try {
    for (const scale of [1, 2]) {
      const ctx = await browser.newContext({ deviceScaleFactor: scale, viewport: { width: 200, height: 200 } });
      const page = await ctx.newPage();
      for (const j of jobs.previews.filter((x) => x.scale === scale)) {
        await page.setContent(`<!doctype html><html><head><style>html,body{margin:0;background:transparent}
          #b{position:absolute;left:0;top:0;width:${j.size}px;height:${j.size}px;color:${jobs.ink}}
          #b svg{display:block}</style></head><body><div id="b">${strip(fs.readFileSync(j.svg, 'utf8'))}</div></body></html>`);
        await page.locator('#b').screenshot({ path: j.out, omitBackground: true });
      }
      await ctx.close();
    }
    for (const s of jobs.sheets || []) {
      const ctx = await browser.newContext({ deviceScaleFactor: s.scale, viewport: { width: s.width, height: 200 } });
      const page = await ctx.newPage();
      await page.setContent(s.html);
      const h = await page.evaluate(() => document.body.scrollHeight);
      await page.setViewportSize({ width: s.width, height: h });
      const off = await page.evaluate(() => [...document.querySelectorAll('svg')].filter((g) => {
        const r = g.getBoundingClientRect();
        return [r.left, r.top, r.width, r.height].some((v) => Math.abs(v - Math.round(v)) > 0.001);
      }).length);
      await page.screenshot({ path: s.out, fullPage: true });
      console.log(`sheet ${s.out}: ${off} glyphs off whole CSS pixels`);
      await ctx.close();
    }
  } finally { await browser.close(); }
})();
"""


def run_node(jobs, workdir):
    os.makedirs(workdir, exist_ok=True)
    prog = os.path.join(workdir, 'utility_promote_chromium.js')
    jpath = os.path.join(workdir, 'utility_promote_jobs.json')
    with open(prog, 'w') as fh:
        fh.write(NODE_PROGRAM)
    with open(jpath, 'w') as fh:
        json.dump(jobs, fh)
    env = dict(os.environ)
    paths = [x for x in (env.get('NODE_PATH', ''), '/opt/node-tools/node_modules') if x]
    env['NODE_PATH'] = os.pathsep.join(paths)
    r = subprocess.run(['node', prog, jpath], cwd=ROOT, env=env, capture_output=True, text=True, timeout=600)
    if r.returncode:
        raise SystemExit('Chromium run failed: ' + (r.stderr or r.stdout)[-800:])
    return r.stdout


def png_name(svg_path, scale):
    base = os.path.basename(svg_path)[:-4]
    return base + ('-2x' if scale == 2 else '') + '.png'


def previews(results, workdir):
    jobs = {'ink': INK, 'previews': []}
    for p, size, sp, fp in results:
        for scale in (1, 2):
            jobs['previews'].append({'svg': fp, 'size': size, 'scale': scale,
                                     'out': os.path.join(OUT, 'png', png_name(fp, scale))})
    run_node(jobs, workdir)
    # Compare each preview's pixels with the approved option's preview (utility-icons/png/), drawn the same way.
    from PIL import Image  # noqa: E402  (Pillow is only needed here)
    rows, bad = [], 0
    for j in jobs['previews']:
        p = next(x for x in results if x[3] == j['svg'])[0]
        size = j['size']
        op = os.path.join(SRC, 'png', png_name(src_name(p, size), j['scale']))
        a, b = Image.open(op).convert('RGBA'), Image.open(j['out']).convert('RGBA')
        same = a.size == b.size and a.tobytes() == b.tobytes()
        bad += 0 if same else 1
        rows.append({'final_png': rel(j['out']), 'option_png': rel(op), 'size_px': list(b.size),
                     'pixels_equal': same, 'bytes_equal': open(op, 'rb').read() == open(j['out'], 'rb').read()})
    return rows, bad


# ---------------------------------------------------------------------------------------------- manifest
def manifest(results, cmp_rows):
    by = {(r['icon'], r['size']): r for r in cmp_rows}
    icons = []
    for p in PICKS:
        sizes = {}
        for size in (24, 16):
            r = by[(icon_id(p), size)]
            fp = os.path.join(OUT, 'svg-%d' % size, final_name(p, size))
            sizes[str(size)] = {
                'svg': rel(fp),
                'png_1x': rel(os.path.join(OUT, 'png', png_name(fp, 1))),
                'png_2x': rel(os.path.join(OUT, 'png', png_name(fp, 2))),
                'line_px': float(LINE[size]),
                'sprite_symbol_id': 'oa-sym-%s-%dpx' % (icon_id(p).lower(), size),
                'source': r['source'],
                'source_sha256': r['source_sha256'],
                'sha256': r['final_sha256'],
                'drawing_sha256': r['drawing_sha256_final'],
            }
        entry = {
            'id': icon_id(p),
            'name': p['name'],
            'drawing': p['drawing'],
            'approved': {'option': p['option'], 'dr': p['dr'], 'family_dr': 'DR-161',
                         'board': 'Stage B drawings board, card by card, approved by name',
                         'date': '2026-11-10'},
            'audit_rank': p['rank'],
            'action': p['action'],
            'word': p['word'],
            'word_rule': p['word_rule'],
            'uses': p['uses'],
            'states': p['states'],
            'target': p['target'],
            'turns_and_mirrors': [],
            'sizes': sizes,
        }
        if 'pair' in p:
            entry['one_button_with'] = p['pair']
        if p['name'] in TURNS:
            entry['turns_and_mirrors'] = [{k: v for k, v in t.items() if k != 'variant'} for t in TURNS[p['name']]]
            entry['turn_decisions'] = TURN_DECISIONS[p['name']]
        icons.append(entry)
    doc = {
        'title': 'Oath & Action utility icons: the finals in use',
        'edition': 'Edition 06',
        'date': '2026-11-10',
        'made_by': 'The icon designer, utility hand, promoting the options Dustin approved on the stage B drawings '
                   'board (DR-161 to DR-178) under 20261110_Promotion-Brief.md. Each drawing is its approved option '
                   'file\'s, byte for byte; the options stay in work/build/assets/utility-icons/ as the record (D2-718).',
        'family': {'dr': 'DR-161', 'rule': 'Every action drawn bare, with Error, Success and Warning in their own '
                                           'shapes; no rings or frames on actions'},
        'construction': {
            'grid': '24-unit grid at 24 px; its own master on a 16-unit grid at 16 px (D2-648)',
            'lines': 'At 24 px every straight centerline on a whole unit; at 16 px on a quarter, with x = 7.75 as the '
                     'axis of a glyph built on one upright line (D2-649)',
            'finish': 'Round caps and joins; a frame\'s corner rounds by half the line on the centerline (D2-650); a '
                      'dot as wide as the line (D2-651)',
            'color': 'One ink through currentColor, no red, no ids or masks',
            'root_attributes': 'aria-hidden="true" focusable="false" data-icon="U-<name>" '
                               'data-icon-family="utility" data-size="24" or "16"; no data-option',
        },
        'sizes': [
            {'size_px': 24, 'line_px': 2.0, 'token': '--oa-component-icon-utility-line-medium',
             'folder': 'work/build/assets/utility/svg-24/', 'use': "Beside a control's word (audit B-3)"},
            {'size_px': 16, 'line_px': 1.5, 'token': None,
             'token_note': 'No 16 px utility line token yet; the token source adds it with the first 16 px utility '
                           'icon on a page (D2-661)',
             'folder': 'work/build/assets/utility/svg-16/',
             'use': 'Inline in running text or in a table heading (audit B-3). A 16 px glyph always comes from its '
                    '16 px master (D2-648)'},
        ],
        'previews': 'png/: each SVG drawn by Chromium at its own size, Charcoal (#121212) on a clear ground, at '
                    'device scale 1 (1x) and 2 (-2x), as the options\' previews were (D2-658)',
        'icons': icons,
    }
    path = os.path.join(OUT, '%s_Utility-Icons-Manifest.json' % DATE)
    with open(path, 'w') as fh:
        json.dump(doc, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    return path


# ---------------------------------------------------------------------------------------------- review sheets
def turned_svg(text, transform):
    root, _, body = split(text)
    inner = body.rsplit('</svg>', 1)[0].rstrip('\n')
    return root + '\n  <g transform="%s">\n%s\n  </g>\n</svg>\n' % (transform, inner)


def review(results, outdir):
    os.makedirs(outdir, exist_ok=True)
    tdir = os.path.join(outdir, 'turned')
    os.makedirs(tdir, exist_ok=True)
    finals = {(p['name'], size): fp for p, size, sp, fp in results}
    turned = []
    for name, ts in TURNS.items():
        for t in ts:
            if not t['variant']:
                continue
            for size in (24, 16):
                text = open(finals[(name, size)]).read()
                out = os.path.join(tdir, '%s_Utility-%s-Variant-%s-%dpx.svg' % (DATE, name, t['variant'], size))
                with open(out, 'w') as fh:
                    fh.write(turned_svg(text, t['transform'][str(size)]))
                turned.append((name + ' ' + t['variant'], size, out))

    def strip(path):
        return re.sub(r'<!--.*?-->', '', open(path).read(), flags=re.S)

    rows = []
    for p in PICKS:
        rows.append((p['name'].replace('-', ' '), finals[(p['name'], 24)], finals[(p['name'], 16)]))
    for label in sorted({t[0] for t in turned}):
        f24 = next(t[2] for t in turned if t[0] == label and t[1] == 24)
        f16 = next(t[2] for t in turned if t[0] == label and t[1] == 16)
        rows.append((label, f24, f16))
    cells = ''.join(
        '<div class="row"><div class="name">%s</div>'
        '<div class="sw np"><span class="g24">%s</span><span class="g16">%s</span></div>'
        '<div class="sw ch"><span class="g24">%s</span><span class="g16">%s</span></div></div>'
        % (lab, strip(a), strip(b), strip(a), strip(b)) for lab, a, b in rows)
    html = ('<!doctype html><html><head><style>body{margin:0;background:#fff;font:11px/1 sans-serif;color:%s}'
            '.row{display:flex;align-items:center;height:36px}.name{width:120px;padding-left:8px}'
            '.sw{display:flex;align-items:center;gap:8px;padding:6px 8px;height:24px;margin-right:8px}'
            '.np{background:%s;color:%s}.ch{background:%s;color:%s}'
            '.g24,.g16{display:block;line-height:0}.g24 svg{width:24px;height:24px;display:block}'
            '.g16 svg{width:16px;height:16px;display:block}</style></head><body>%s</body></html>'
            % (INK, NEWSPRINT, INK, INK, NEWSPRINT, cells))
    sheets = [{'scale': s, 'width': 320, 'html': html,
               'out': os.path.join(outdir, 'utility-finals-sheet-%dx.png' % s)} for s in (1, 2)]
    log = run_node({'ink': INK, 'previews': [], 'sheets': sheets}, os.path.join(outdir, 'node'))
    from PIL import Image
    for s in sheets:
        im = Image.open(s['out'])
        k = 6 if s['scale'] == 1 else 3
        im.resize((im.width * k, im.height * k), Image.NEAREST).save(s['out'].replace('.png', '-enlarged.png'))
    return turned, log


def main():
    report = sys.argv[sys.argv.index('--report') + 1] if '--report' in sys.argv else None
    rev = sys.argv[sys.argv.index('--review') + 1] if '--review' in sys.argv else None
    work = report or rev or tempfile.mkdtemp(prefix='utility-promote-')
    results = promote()
    cmp_rows, cmp_bad = compare(results)
    png_rows, png_bad = previews(results, os.path.join(work, 'node'))
    mpath = manifest(results, cmp_rows)
    print('wrote %d SVG finals, %d PNG previews and %s' % (len(results), len(png_rows), rel(mpath)))
    print('drawing comparison: %d of %d finals match their approved option file (drawing bytes, elements, root '
          'attributes as planned)' % (len(cmp_rows) - cmp_bad, len(cmp_rows)))
    print('preview comparison: %d of %d previews draw the same pixels as the option\'s preview (%d byte for byte)'
          % (len(png_rows) - png_bad, len(png_rows), sum(r['bytes_equal'] for r in png_rows)))
    for r in cmp_rows:
        if not r['pass']:
            print('  DIFFERS:', r['final'], json.dumps(r['root_attributes_changed']))
    for r in png_rows:
        if not r['pixels_equal']:
            print('  PREVIEW DIFFERS:', r['final_png'])
    if report:
        os.makedirs(report, exist_ok=True)
        with open(os.path.join(report, 'utility-promote-comparison.json'), 'w') as fh:
            json.dump({'svg': cmp_rows, 'png': png_rows}, fh, indent=1)
        print('comparison written to', os.path.join(report, 'utility-promote-comparison.json'))
    if rev:
        turned, log = review(results, rev)
        print('review: %d turned and mirrored copies in %s' % (len(turned), os.path.join(rev, 'turned')))
        print(log.strip())
    sys.exit(1 if cmp_bad or png_bad else 0)


if __name__ == '__main__':
    main()
