"""The wordmark width proofs (DR-71, DR-89): masthead, email, avatar, social card and letterhead at today's wordmark width
and the condensed width, each with ampersand B, at actual size. Also writes the letterhead print proof (US Letter, two
pages) and proofs.json, the appendix's groups and captions.

Fix pass, November 6, 2026 (D2-251, C-M6): each pair is one comparison specimen at actual size. Mastheads and social
cards stack on one left edge; emails, avatars and letterheads sit side by side, so both wordmarks show in one view. Each
width is labeled inside the stage. The PDF prints its width and its Illustrative line on each page (BE-M4). The condensed
minimums move here from chapter 03 (BE-S11). Kickers follow Rule 01.21 (D2-250); the social card breaks at the hinge
(C-S14) and carries its specifications (RP-S4); the email deck opens on the step (BE-S12, RP-S1); the letterhead's town
is renamed so it cannot be joined to Alder County (CP-S17), and its letter opens on the request (CP-S10). No decision
codes or production words reach the page (D2-253)."""
import base64
import json
import re
import subprocess

import stage_a_identity_lib as LIB
from stage_a_identity_lib import (E, ROOT, ID_DIR, WM, WMC, L2, L8, LOCK, AMP, mark, lockmark, illus, head_label, ink, ink2,
                                  hair, pal, tv, ty, CHAP_DIR, HERE, curl_html)
from stage_a_identity_s03 import rec as _rec, MINIMUM_ROWS, _mark_name, _no_condensed
from stage_a_identity_s04 import headline

S = []
PROOF_DIR = ROOT / "work/boards/phase-2/stage-a/proofs"
PDF = PROOF_DIR / "20261106_Letterhead-Proof.pdf"
NAME = {"today": "Today's width", "condensed": "Condensed width, proposed"}
WIDTHS = ("today", "condensed")


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "proofs")
    return _rec(*a, **k)


def plabel(width, extra=""):
    """The label that names a width inside a comparison stage."""
    tail = f' <span class="oai-pl-x">{E(extra)}</span>' if extra else ""
    return f'<p class="oai-pl">{E(NAME[width])}{tail}</p>'


PAIR_CSS = (".oai .oai-pl{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;margin:0 0 8px}"
            ".oai-pl-x{text-transform:none;letter-spacing:0;font-weight:400;color:var(--oa-color-text-secondary-on-newsprint)}"
            ".oai-stackpair{display:flex;flex-direction:column;gap:28px;align-items:flex-start}"
            ".oai-sidepair{display:flex;gap:32px;align-items:flex-start;flex-wrap:nowrap}")


def l3(width, surface="newsprint"):
    """L3 at the masthead's size: the 24 px wordmark master, 13 px, the lockmark at 52 px."""
    files = WM if width == "today" else WMC
    return (f'<span role="img" aria-label="Oath &amp; Action" style="display:inline-flex;align-items:flex-start;gap:13px;padding:14px 0">'
            f'{mark(files[24], h=24, surface=surface, decorative=True)}<span style="display:block;line-height:0;margin:-14px 0">{mark(LOCK["display"], h=52, surface=surface, decorative=True)}</span></span>')


def _burger(surface="newsprint"):
    return (f'<span aria-hidden="true" style="width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:center">'
            + "".join(f'<span style="width:20px;height:2px;background:{ink(surface)}"></span>' for _ in range(3)) + '</span>')


# ------------------------------------------------------------------------------------------- at a glance
@spec
def s_proofs_glance():
    def col(width):
        files, l8 = (WM, L8["today"]) if width == "today" else (WMC, L8["condensed"])
        w16, w24, wd = (152, 221, 978.31) if width == "today" else (120, 181, 770.07)
        rows = [
            ("16 px master", mark(files[16], h=16, label=f"Wordmark, {NAME[width]}, 16 px master"), f"{w16} by 16 px"),
            ("24 px master", mark(files[24], h=24, label=f"Wordmark, {NAME[width]}, 24 px master"), f"{w24} by 24 px"),
            ("Display master, 48 px tall", mark(files["display"], h=48, label=f"Wordmark, {NAME[width]}, display"), f"{wd * 48 / 108:.0f} by 48 px"),
            ("L2 stacked, 72 px tall", mark(L2[width], h=72, label=f"L2, {NAME[width]}"), ""),
            ("L8 monogram, 48 px tall", mark(l8, h=48, label=f"L8, {NAME[width]}"), ""),
        ]
        cells = "".join(f'<div class="oai-cell" style="gap:6px">{m}<span class="oai-tag">{E(a)}{(" · " + E(b)) if b else ""}</span></div>' for a, m, b in rows)
        return (f'<div class="oai-stack" style="gap:28px;padding:24px 28px;border:1px solid {hair("newsprint")};flex:1">'
                f'{plabel(width)}{cells}</div>')
    body = f'<div class="oai-pad"><div class="oai-row top" style="gap:16px;flex-wrap:nowrap">{col("today")}{col("condensed")}</div></div>'
    alt = ("The wordmark at both widths side by side at true size, today's width at left and the condensed width at right, "
           "each at the same height so the difference shows as width: from the 16 pixel masters, 152 against 120 pixels "
           "wide; from the 24 pixel masters, 221 against 181; from the display masters at 48 pixels tall, 435 against 342. "
           "Below them, the stacked lockup and the O & A monogram at both widths.")
    return rec("s-proofs-glance", "proofs", 960, alt, body, css=PAIR_CSS,
               notes="Same height for both widths, so the difference shows as width. Today's width is in force; the condensed width is the proposal for Gate 2 (DR-71).")


# ------------------------------------------------------------------------------------------- mastheads
def _desk_bar(width):
    nav = "".join(f'<span style="{ty("ui", 1440)}">{t}</span>' for t in ("Explain", "Track", "Connect", "Act", "About"))
    return (f'<div class="oai-s-newsprint" style="width:1440px;height:80px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 64px;border:1px solid {hair("newsprint")}">{l3(width)}<div style="display:flex;gap:32px">{nav}</div></div>')


def _phone_bar(width):
    files = WM if width == "today" else WMC
    return (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}">{mark(files[24], h=24, label="Oath & Action")}{_burger()}</div>')


@spec
def s_proofs_masthead():
    body = ('<div class="oai-pad"><div class="oai-stackpair">'
            + "".join(f'<div>{plabel(w, "site, 1440 px")}{_desk_bar(w)}</div>' for w in WIDTHS)
            + "".join(f'<div>{plabel(w, "phone, 390 px")}{_phone_bar(w)}</div>' for w in WIDTHS)
            + '</div></div>')
    alt = ("The site masthead at both widths, at true size, one above the other on one left edge: two 1440 pixel Newsprint "
           "bars, each with OATH & ACTION and the lockmark at left and five navigation words at right. Today's wordmark runs "
           "221 pixels and the condensed one 181, so the condensed lockmark sits 40 pixels further left. Below them, the two "
           "390 pixel phone bars with the wordmark and a menu button, also on one left edge.")
    return rec("s-proofs-masthead", "proofs", 1488, alt, body, css=PAIR_CSS, fit_switch=True,
               notes="L3 from the 24 px master (221 or 181 px) with a 52 px lockmark; phone bars with the 24 px master. Stacked on one left edge (D2-251).")


# ------------------------------------------------------------------------------------------- email
def _email(width):
    sans = "font-family:var(--oa-font-family-email-sans)"
    return (f'<div class="oai-s-white" style="width:600px;border:1px solid {hair("white")}">'
            f'<div style="height:96px;display:flex;align-items:center;padding:0 24px;border-bottom:1px solid {hair("white")}">{l3(width, "white")}</div>'
            f'<div style="padding:24px;{sans}">{head_label()}'
            f'<p style="{sans};font-weight:700;font-size:13px;line-height:1.4;letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;color:{ink2("white")}">Explainer · Local budgets</p>'
            f'<p style="{sans};font-weight:700;font-size:24px;line-height:1.2;margin-top:8px">Your county board votes on the budget Tuesday at 7 p.m.</p>'
            f'<p style="{sans};margin-top:10px;font-size:17px;line-height:1.5">Sign up with the board clerk by noon Monday to speak before the vote.</p></div></div>')


@spec
def s_proofs_email():
    body = ('<div class="oai-pad"><div class="oai-sidepair">'
            + "".join(f'<div>{plabel(w)}{_email(w)}</div>' for w in WIDTHS) + '</div></div>')
    alt = ("Two 600 pixel emails side by side at true size, today's width at left and the condensed width at right. Each opens "
           "with the L3 masthead in a white header, then an invented story: the kicker Explainer · Local budgets, the headline "
           "Your county board votes on the budget Tuesday at 7 p.m., and the line Sign up with the board clerk by noon Monday "
           "to speak before the vote. The story is Illustrative.")
    return rec("s-proofs-email", "proofs", 1280, alt, body, illustrative=True, css=PAIR_CSS, fit_switch=True,
               notes="Drawn live; in email the masthead ships as a PNG at twice size. Body in the email stack. The pair is 1,280 px, so its "
                     "type takes sizes common to both sets: 24 px headline, 17 px body, 13 px kicker (D2-254). Deck opens on the step (BE-S12).")


# ------------------------------------------------------------------------------------------- avatar
def _av(width, size, shape):
    m = mark(L8[width], w=0.62 * size, surface="charcoal", decorative=True)
    rad = "50%" if shape == "circle" else f"{0.2237 * size:.1f}px"
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;border-radius:{rad};'
            f'background:{tv("component-avatar-tile")};flex:none">{m}</span>')


def _avatars(width):
    vbw = 299.67 if width == "today" else 246.15

    def cap(size):
        return 0.62 * size * 100 / vbw

    def it(lbl, inner):
        return f'<div class="oai-cell" style="max-width:200px">{inner}<span class="oai-tag">{E(lbl)}</span></div>'
    row1 = it(f"Circle, 200 px · capitals {cap(200):.0f} px", _av(width, 200, "circle")) + it("Square, 200 px", _av(width, 200, "square"))
    row2 = (it(f"96 px · capitals {cap(96):.0f} px", _av(width, 96, "circle"))
            + it(f"48 px, feed size · capitals {cap(48):.0f} px, under the 14 px floor", _av(width, 48, "circle")))
    return (f'<div style="width:440px">{plabel(width)}<div class="oai-stack" style="gap:24px">'
            f'<div class="oai-row">{row1}</div><div class="oai-row">{row2}</div></div></div>')


@spec
def s_proofs_avatar():
    body = f'<div class="oai-pad"><div class="oai-sidepair">{_avatars("today")}{_avatars("condensed")}</div></div>'
    alt = ("Avatars on Charcoal at both widths side by side, at true size, today's width at left and the condensed width at "
           "right: the O & A monogram in Newsprint with a red ampersand fills 62 percent of a 200 pixel circle and a 200 pixel "
           "rounded square, then a 96 and a 48 pixel circle. Today's capitals stand 41, 20 and 10 pixels tall; the condensed "
           "capitals stand 50, 24 and 12, and its narrow O reads close to a zero. At 48 pixels both fall under the 14 pixel floor.")
    return rec("s-proofs-avatar", "proofs", 960, alt, body, css=PAIR_CSS,
               notes="L8 fills 62 percent of the tile's width at both widths, as a designer fits a tile. Charcoal tile (R13, DR-67).")


# ------------------------------------------------------------------------------------------- social card
SOCIAL_SPECS = [
    ("Size", "1200 by 630 px, the link-preview size"),
    ("Margin", "72 px on every side"),
    ("Kicker", "The H4 style at 24 px in Deep Stone: the content label, then the topic (Rule 01.21)"),
    ("Headline", "The title style at 110 px, broken at the hinge; B from its display master in the card's working red"),
    ("Wordmark", "The display master, 44 px tall, bottom left"),
    ("Lockmark", "40 px, bottom right, inside the margin (Rule 08.2)"),
    ("Left out", "A deck, so the headline keeps the title size, and a web address until ours is settled"),
]


def _social(width):
    files = WM if width == "today" else WMC
    return (f'<div class="oai-s-newsprint" style="position:relative;width:1200px;height:630px;padding:72px;border:1px solid {hair("newsprint")}">'
            f'<p style="{ty("h4", 1200)};color:{ink2("newsprint")}">Explainer · Zoning</p>'
            f'{headline("The zoning code", "the rent.", "title", board=1200, extra_style="margin-top:24px")}'
            f'<div style="position:absolute;left:72px;bottom:72px">{mark(files["display"], h=44, label="Oath & Action")}</div>'
            f'<div style="position:absolute;right:72px;bottom:72px">{lockmark(40, label="Lockmark")}</div></div>')


@spec
def s_proofs_social():
    specs = "".join(f'<div class="oai-sp"><dt>{E(a)}</dt><dd>{E(b)}</dd></div>' for a, b in SOCIAL_SPECS)
    css = PAIR_CSS + (".oai-spl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px;margin:8px 0 0;max-width:1200px}"
                      ".oai-sp{display:grid;grid-template-columns:96px minmax(0,1fr);gap:12px;padding:8px 0;border-top:1px solid var(--oa-color-border-hairline-on-newsprint);font-size:14px;line-height:1.5}"
                      ".oai-sp dt{font-weight:700}.oai-sp dd{margin:0}")
    body = ('<div class="oai-pad"><div class="oai-stackpair">'
            + "".join(f'<div>{plabel(w)}{_social(w)}</div>' for w in WIDTHS)
            + f'<div style="width:1200px"><p class="oai-pl">Specifications, both widths</p><dl class="oai-spl">{specs}</dl></div>'
            + '</div></div>')
    alt = ("Two social cards at actual size, 1200 by 630 pixels, one above the other on one left edge, today's width above "
           "the condensed width. Each card on Newsprint carries the kicker Explainer · Zoning, the hinge headline The zoning "
           "code & the rent. broken before a red ampersand B, the wordmark 44 pixels tall at bottom left and the lockmark at "
           "bottom right. No web address. Under them, the card's specifications: 72 pixel margins, the kicker in the H4 style "
           "at 24 pixels, the headline in the title style at 110, the wordmark's display master at 44 pixels tall and the "
           "lockmark at 40. The headline and kicker are invented.")
    return rec("s-proofs-social", "proofs", 1248, alt, body, css=css, illustrative=True, fit_switch=True,
               notes="1200 by 630, the link-preview size, type at the desktop ceiling (D2-254). The headline is chapter 02's hinge example. "
                     "No web address until the site is settled (DR-55). Stacked on one left edge (D2-251).")


# ------------------------------------------------------------------------------------------- letterhead
LETTER = [
    "Please send us the approved minutes of the Planning Board's October 14 meeting, and any written comments the board received before that date on the bylaw for backyard cottages, which the zoning code calls accessory dwelling units.",
    "We publish a plain account of how the board reached each decision on the bylaw, and we link readers to the official record. Your office's copy is the record we want to cite.",
    "An electronic copy is fine. If the request carries a fee, please tell us the amount before you begin, and we will pay it the same week.",
]
LETTER_SLUG = "The address, recipient and letter are invented."


def _letter(width):
    """One US Letter sheet at 96 px to the inch, type in points (D2-205). A slug line in the top margin names the width
    and what is invented, so the sheet carries its labels wherever it travels (BE-M4)."""
    files = WM if width == "today" else WMC
    w = mark(files["display"], h=26, label="Oath & Action")
    paras = "".join(f'<p style="margin-top:11pt">{E(t)}</p>' for t in LETTER)
    sec = ink2("white")
    return (f'<div class="oai-s-white oai-letter" style="position:relative;width:816px;height:1056px;padding:72px 84px;border:1px solid {hair("white")};font-size:11pt;line-height:1.55">'
            f'<div class="oai-slug" style="position:absolute;left:84px;right:84px;top:26px;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;font-size:10pt;line-height:1.3;color:{sec}">'
            f'<span style="font-weight:700;color:{ink("white")}">{E(NAME[width])}</span>{illus()}<span>{E(LETTER_SLUG)}</span></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{w}'
            f'<p style="font-size:10pt;line-height:1.5;text-align:right;color:{sec}">Oath &amp; Action<br>PO Box 214<br>Wrenfield, MA 01000</p></div>'
            f'<div style="margin-top:72px"><p>November 6, 2026</p>'
            f'<p style="margin-top:15pt">Jordan Lee<br>Town Clerk, Town of Wrenfield</p>'
            f'<p style="margin-top:15pt">Dear Jordan Lee,</p>{paras}'
            f'<p style="margin-top:15pt">Thank you,</p><p style="margin-top:21pt">Dustin Cathcart<br>Founder and Editor</p></div>'
            f'<div style="position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;align-items:center;'
            f'border-top:1px solid {hair("white")};padding-top:14px">'
            f'<p style="font-size:10pt;color:{sec}">A country that answers to its people.</p>{lockmark(24, surface="white", label="Lockmark")}</div></div>')


def _pdf_link():
    if not PDF.exists():
        return ""
    data = base64.b64encode(PDF.read_bytes()).decode()
    return (f'<p style="margin-top:16px"><a download="20261106_Letterhead-Proof.pdf" href="data:application/pdf;base64,{data}" '
            f'style="{ty("ui")};color:var(--oa-color-text-primary-on-newsprint)">Download the print proof, US Letter, two pages, one per width (PDF)</a></p>')


@spec
def s_proofs_letterhead():
    body = ('<div class="oai-pad"><div class="oai-sidepair">'
            + "".join(f'<div>{plabel(w)}{_letter(w)}</div>' for w in WIDTHS)
            + f'</div>{_pdf_link()}</div>')
    alt = ("Two US Letter letterheads side by side at true size on screen, 8.5 by 11 inches each, today's width at left and "
           "the condensed width at right. Each has a proof line in its top margin naming its width and saying the address, "
           "recipient and letter are invented; the wordmark at top left at the same height; a return address at top right; "
           "a records request to the town clerk of Wrenfield signed by Dustin Cathcart, Founder and Editor; and a footer with "
           "the tagline and the lockmark. A link downloads the two-page print proof.")
    return rec("s-proofs-letterhead", "proofs", 1712, alt, body, illustrative=True, css=PAIR_CSS, interactive=True, fit_switch=True,
               check_exempt=["scale"],
               notes="A print piece set in points (D2-205): 11 pt body, 10 pt address, slug and footer, so check_exempt scale. "
                     "96 CSS px to the inch, so each sheet is 816 by 1056 px. Display master at 26 px tall, as a print piece places it. "
                     "Side by side, so both wordmarks sit on one line 72 px from the top: stacked, they would sit 1,128 px apart, "
                     "more than a 900 px window. interactive: the stage holds the PDF link.")


def write_letterhead(pdf=False):
    """A standalone two-page US Letter page, masters inlined, printed to PDF by Chromium at its CSS page size."""
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    LIB.INLINE_ALL[0] = True
    try:
        pages = "".join(f'<section class="pg">{curl_html(_letter(w))}</section>' for w in WIDTHS)
    finally:
        LIB.INLINE_ALL[0] = False
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Letterhead proof, both wordmark widths</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>{LIB.CSS}'
            '@page{size:8.5in 11in;margin:0}html,body{margin:0;padding:0}body{font-family:var(--oa-font-family-reading)}'
            '.pg{width:8.5in;height:11in;overflow:hidden;break-after:page}.pg:last-child{break-after:auto}'
            '.oai-letter{border:0!important}.oai-svg{display:block}p{margin:0}'
            '.illus{display:inline-block;padding:0 .4em;border:1px solid currentColor;font:700 10pt/1.5 var(--oa-font-family-reading);'
            'letter-spacing:.06em;text-transform:uppercase}</style></head>'
            f'<body class="oai">{pages}</body></html>')
    html_path = PROOF_DIR / "20261106_Letterhead-Proof.html"
    html_path.write_text(page)
    if pdf:
        subprocess.run(["node", str(HERE / "p2_print_pdf.js"), str(html_path.resolve()), str(PDF.resolve())], check=True)


# ------------------------------------------------------------------------------------------- minimums at both widths
# Each mark whose minimum changes with the width, as the identity masters' table gives it (20261028_Identity-Minimum-Sizes.json).
MIN_BOTH = [
    ("L1 Wordmark", "16 px tall, 152 px wide; 1.20 in in print", "16 px tall, 120 px wide; 0.95 in in print"),
    ("L2 Stacked", "90 px wide; 0.80 in in print", "72 px wide; 0.65 in in print"),
    ("L3 Horizontal with the lockmark", "196 px wide; 1.55 in in print", "164 px wide; 1.30 in in print"),
    ("L8 Monogram", "48 px wide, capitals 16 px; 0.50 in in print", "48 px wide, capitals 19.5 px; 0.50 in in print"),
    ("Hinge diagram, display master", "533 px wide; 4.00 in in print", "463 px wide"),
    ("Hinge diagram, compact master", "245 px wide", "213 px wide"),
]


def _check_min_both():
    """Every condensed figure above must appear in the masters' table, so the proof never drifts from it."""
    text = json.dumps(MINIMUM_ROWS)
    for _, _, c in MIN_BOTH:
        for n in re.findall(r"[\d.]+ (?:px|in)", c):
            assert n.split()[0] in text, f"{n} not in the identity masters' table"


@spec
def s_proofs_minimums():
    _check_min_both()
    rows = "".join(f'<tr><th scope="row">{E(m)}</th><td data-k="{E(NAME["today"])}">{E(t)}</td><td data-k="{E(NAME["condensed"])}">{E(c)}</td></tr>'
                   for m, t, c in MIN_BOTH)
    table = (f'<table class="stack"><thead><tr><th scope="col">Mark</th><th scope="col">{E(NAME["today"])}</th>'
             f'<th scope="col">{E(NAME["condensed"])}</th></tr></thead><tbody>{rows}</tbody></table>')
    body = f'<div class="oai-panel oai-s-newsprint">{table}</div>'
    alt = "Minimum sizes of the marks whose size changes with the wordmark's width, at today's width and at the condensed width."
    return rec("s-proofs-minimums", "proofs", None, alt, body, readable=True,
               notes="The condensed figures from the identity masters' table (I8), moved here from chapter 03 (BE-S11), each checked against the table at build time. readable: a static table.")


# ------------------------------------------------------------------------------------------- proofs.json
PROOFS = {
    "title": "Wordmark width proofs",
    "instruction": "Compare each piece at both wordmark widths at actual size, so Dustin can choose one.",
    "intro": [
        "Dustin Cathcart, our founder and editor, chooses the wordmark's width from these proofs. Each proof shows one piece at actual size at today's width and at the condensed width, both with ampersand B, set on one edge or one line so the wordmark is the one thing that changes. Today's width stays in use until he chooses.",
        "We recommend today's width. At the same height the condensed drawing only runs narrower, and its heavy capitals sit close to the lettering of campaign signs. Its monogram also reads as 0&A.",
    ],
    "groups": [
        {"label": "The marks at a glance", "text": ["The wordmark from each of its masters, the stacked lockup and the monogram, both widths at the same height."],
         "items": [{"specimen": "s-proofs-glance", "label": "Both widths", "caption": "At the same height the condensed wordmark runs about a fifth narrower: 152 against 120 px from the 16 px masters, 221 against 181 from the 24 px masters, and 435 against 342 from the display masters at 48 px tall."}]},
        {"label": "Masthead on the site", "text": ["L3 in the 1440 px site bar and L1 in the 390 px phone bar, today's width above the condensed width on one left edge."],
         "items": [{"specimen": "s-proofs-masthead", "label": "Both widths, stacked", "caption": "At the same height the condensed wordmark runs 40 px shorter, so the lockmark moves 40 px to the left. Use Fit to window to see each bar whole."}]},
        {"label": "Masthead in email", "text": ["L3 at the head of a 600 px email, the two widths side by side. A sent email carries the masthead as a PNG at twice size, with the alt text “Oath & Action”."],
         "items": [{"specimen": "s-proofs-email", "label": "Both widths, side by side", "caption": "The story under each masthead is invented."}]},
        {"label": "Avatar", "text": ["The monogram, L8, on the Charcoal tile that Rule 04.7 sets as the default, in a circle and a square. A feed draws an avatar at about 32 to 48 px, where L8 at either width sets its capitals under the 14 px floor. Rule 04.7's avatar, ampersand B alone, reads at that size and is the same at both widths, so we recommend it whichever width Dustin chooses."],
         "items": [{"specimen": "s-proofs-avatar", "label": "Both widths, side by side", "caption": "L8 fills 62 percent of the tile's width at both widths, so the condensed capitals stand taller, and its narrow O reads close to a zero."}]},
        {"label": "Social card", "text": ["The 1200 by 630 link-preview card, today's width above the condensed width on one left edge, with its specifications under them."],
         "items": [{"specimen": "s-proofs-social", "label": "Both widths, stacked", "caption": "Until chapter 23 sets social cards, build one from these specifications at today's width."}]},
        {"label": "Letterhead", "text": ["US Letter, 8.5 by 11 inches, at true size on screen, 96 px to the inch, the two widths side by side. The print proof holds both widths, one per page, each labeled; check its scale with a ruler before you judge it on paper."],
         "items": [{"specimen": "s-proofs-letterhead", "label": "Both widths, side by side", "caption": "The address, recipient and letter are invented, and the letter is signed with Dustin's name and title."}]},
        {"label": "Minimum sizes at both widths", "text": ["The smallest size of each mark whose size changes with the width. Chapter 03 lists today's width alone."],
         "items": [{"specimen": "s-proofs-minimums", "label": "Both widths", "caption": "From the identity masters' table. Every other mark keeps its minimum at either width."}]},
    ],
}


def write_proofs_json():
    from stage_a_identity_lib import curl

    def sm(o):
        if isinstance(o, dict):
            return {k: (v if k == "specimen" else sm(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [sm(v) for v in o]
        return curl(o)
    (CHAP_DIR / "proofs.json").write_text(json.dumps(sm(PROOFS), indent=1, ensure_ascii=False) + "\n")
