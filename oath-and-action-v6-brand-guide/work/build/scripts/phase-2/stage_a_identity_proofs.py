"""The Gate 2 proofs panel (DR-71, DR-89): masthead, avatar, social card and letterhead at today's wordmark width and the
condensed width, each with ampersand B, at actual size. Also writes the letterhead print proof (US Letter, two pages) and
proofs.json, the appendix's groups and captions."""
import base64
import json
import subprocess
from pathlib import Path

import stage_a_identity_lib as LIB
from stage_a_identity_lib import (E, ROOT, ID_DIR, WM, WMC, L2, L3, L8, LOCK, AMP, mark, lockmark, illus, ink, ink2, hair, pal,
                                  tv, sig, ground, CHAP_DIR, HERE)
from stage_a_identity_s03 import rec as _rec
from stage_a_identity_s04 import headline

S = []
PROOF_DIR = ROOT / "work/boards/phase-2/stage-a/proofs"
PDF = PROOF_DIR / "20261106_Letterhead-Proof.pdf"
NAME = {"today": "Today's width", "condensed": "Condensed width, for Gate 2"}


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "proofs")
    return _rec(*a, **k)


def wm(width, h, surface="newsprint", label="Oath & Action", print_=False):
    """The wordmark at a box height from the master for that height, at either width. print_ places the display master
    at any height, as a print piece would."""
    files = WM if width == "today" else WMC
    key = "display" if (print_ or h >= 40) else (24 if h >= 20 else 16)
    return mark(files[key], h=h, surface=surface, label=label)


def l3(width, surface="newsprint"):
    """L3 as I8 composes it at the masthead's size: the 24 px wordmark master, 13 px, the lockmark at 52 px."""
    files = WM if width == "today" else WMC
    return (f'<span role="img" aria-label="Oath &amp; Action" style="display:inline-flex;align-items:flex-start;gap:13px;padding:14px 0">'
            f'{mark(files[24], h=24, surface=surface, decorative=True)}<span style="margin-top:-14px">{mark(LOCK["display"], h=52, surface=surface, decorative=True)}</span></span>')


def _burger(surface="newsprint"):
    return (f'<span aria-hidden="true" style="width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:center">'
            + "".join(f'<span style="width:20px;height:2px;background:{ink(surface)}"></span>' for _ in range(3)) + '</span>')


# ------------------------------------------------------------------------------------------- at a glance
@spec
def s_proofs_glance():
    def col(width):
        files, l8 = (WM, L8["today"]) if width == "today" else (WMC, L8["condensed"])
        w16 = 152 if width == "today" else 120
        rows = [
            ("16 px master", mark(files[16], h=16, label=f"Wordmark, {NAME[width]}, 16 px master"), f"{w16} by 16 px"),
            ("24 px master", mark(files[24], h=24, label=f"Wordmark, {NAME[width]}, 24 px master"), f"{221 if width == 'today' else 181} by 24 px"),
            ("Display master, 48 px tall", mark(files["display"], h=48, label=f"Wordmark, {NAME[width]}, display"), f"{(978.31 if width == 'today' else 770.07) * 48 / 108:.0f} by 48 px"),
            ("L2 stacked, 72 px tall", mark(L2[width], h=72, label=f"L2, {NAME[width]}"), ""),
            ("L8 monogram, 48 px tall", mark(l8, h=48, label=f"L8, {NAME[width]}"), ""),
        ]
        cells = "".join(f'<div class="oai-cell" style="gap:6px">{m}<span class="oai-tag">{E(a)}{(" · " + E(b)) if b else ""}</span></div>' for a, m, b in rows)
        return (f'<div class="oai-stack" style="gap:28px;padding:24px 28px;border:1px solid {hair("newsprint")};flex:1">'
                f'<p class="oai-label">{E(NAME[width])}</p>{cells}</div>')
    body = f'<div class="oai-pad"><div class="oai-row top" style="gap:16px;flex-wrap:nowrap">{col("today")}{col("condensed")}</div></div>'
    alt = ("The wordmark at both widths side by side at true size: today's width at left and the condensed width at right, "
           "each from its 16 px master, its 24 px master and its display master at 48 pixels tall, then the stacked lockup "
           "and the O & A monogram. At the same height the condensed drawing runs about a fifth narrower.")
    return rec("s-proofs-glance", "proofs", 960, alt, body,
               notes="Same height for both widths, so the difference shows as width. Today's width is in force; the condensed width is a proposal for Gate 2.")


# ------------------------------------------------------------------------------------------- mastheads
def _masthead(width):
    nav = "".join(f'<span style="font:600 15px/1 var(--oa-font-family-reading)">{t}</span>' for t in ("Explain", "Track", "Connect", "Act", "About"))
    desk = (f'<div class="oai-s-newsprint" style="width:1440px;height:80px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 64px;border-bottom:1px solid {hair("newsprint")}">{l3(width)}<div style="display:flex;gap:32px">{nav}</div></div>')
    files = WM if width == "today" else WMC
    phone = (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
             f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}">{mark(files[24], h=24, label="Oath & Action")}{_burger()}</div>')
    return (f'<div class="oai-stack" style="gap:20px">{desk}<div class="oai-cell" style="padding-left:64px">{phone}'
            f'<span class="oai-tag">The same masthead on a 390 px phone</span></div></div>')


@spec
def s_proofs_masthead_today():
    alt = ("The site masthead at today's width, at true size: a 1440 pixel Newsprint bar with OATH & ACTION and the lockmark at "
           "left and five navigation words at right, and below it the phone bar at 390 pixels with the wordmark and a menu button.")
    return rec("s-proofs-masthead-today", "proofs", 1440, alt, _masthead("today"),
               notes="L3 from the 24 px wordmark master (221 px) with a 52 px lockmark; phone bar with the 24 px master.")


@spec
def s_proofs_masthead_condensed():
    alt = ("The same site masthead with the condensed wordmark, at true size: the wordmark runs 181 pixels wide at the same "
           "height, so the lockmark sits 40 pixels further left; the phone bar below it.")
    return rec("s-proofs-masthead-condensed", "proofs", 1440, alt, _masthead("condensed"),
               notes="The condensed 24 px master (181 px) at the same height as today's.")


def _email(width):
    return (f'<div class="oai-s-white" style="width:600px;border:1px solid {hair("white")}">'
            f'<div style="height:96px;display:flex;align-items:center;padding:0 24px;border-bottom:1px solid {hair("white")}">{l3(width, "white")}</div>'
            f'<div style="padding:24px;font-family:var(--oa-font-family-email-sans, Arial, sans-serif)">'
            f'<p style="font-weight:700;font-size:24px;line-height:1.2">Your county board votes on the budget Tuesday</p>'
            f'<p style="margin-top:10px;font-size:16px;line-height:1.5">Here is who wrote it, what changed since the draft, and how to speak before the vote.</p>'
            f'<p style="margin-top:12px">{illus()}</p></div></div>')


@spec
def s_proofs_email_today():
    alt = "An email at true size, 600 pixels wide: the L3 masthead at today's width in a white header, then an invented headline and first line in Arial. Illustrative."
    return rec("s-proofs-email-today", "proofs", 600, alt, _email("today"), illustrative=True,
               notes="Drawn live here; in email the masthead ships as a PNG at twice size. Body text uses the email stack (V5's system fonts).")


@spec
def s_proofs_email_condensed():
    alt = "The same email with the condensed wordmark in the masthead, at true size. Illustrative."
    return rec("s-proofs-email-condensed", "proofs", 600, alt, _email("condensed"), illustrative=True)


# ------------------------------------------------------------------------------------------- avatar
def _av(width, size, shape):
    l8 = L8[width]
    w = 0.62 * size
    m = mark(l8, w=w, surface="charcoal", decorative=True)
    rad = "50%" if shape == "circle" else f"{0.2237 * size:.1f}px"
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;border-radius:{rad};'
            f'background:{tv("component-avatar-tile")};flex:none">{m}</span>')


def _avatars(width):
    vbw = 299.67 if width == "today" else 246.15
    def cap(size):
        return 0.62 * size * 100 / vbw
    def it(lbl, inner):
        return f'<div class="oai-cell">{inner}<span class="oai-tag">{lbl}</span></div>'
    row1 = (it(f"Circle, 200 px · capitals {cap(200):.0f} px", _av(width, 200, "circle"))
            + it(f"Square, 200 px", _av(width, 200, "square")))
    row2 = (it(f"96 px · capitals {cap(96):.0f} px", _av(width, 96, "circle"))
            + it(f"48 px, feed size · capitals {cap(48):.0f} px, under the 14 px floor", _av(width, 48, "circle"))
            + it("48 px with ampersand B", f'<span style="display:inline-flex;align-items:center;justify-content:center;width:48px;height:48px;border-radius:50%;background:{tv("component-avatar-tile")}">{mark(AMP[24], h=28, surface="charcoal", decorative=True)}</span>'))
    return (f'<div class="oai-pad"><p class="oai-label" style="margin-bottom:16px">{E(NAME[width])}</p>'
            f'<div class="oai-stack" style="gap:24px"><div class="oai-row">{row1}</div><div class="oai-row">{row2}</div></div></div>')


@spec
def s_proofs_avatar_today():
    alt = ("Avatars on Charcoal at today's width, at true size: the O & A monogram in Newsprint with a red ampersand, filling "
           "a 200 pixel circle and a 200 pixel rounded square, then the circle at 96 and at 48 pixels, where its capitals fall "
           "to 10 pixels, and ampersand B alone in a 48 pixel circle.")
    return rec("s-proofs-avatar-today", "proofs", 480, alt, _avatars("today"),
               notes="L8 fills 62 percent of the tile's width (same width for both drawings, as a designer fits a tile). Charcoal tile by R13.")


@spec
def s_proofs_avatar_condensed():
    alt = ("The same avatars with the condensed monogram, at true size: at the same width its capitals stand taller, 50 pixels "
           "in the 200 pixel circle, and its narrow O reads close to a zero; at 48 pixels its capitals reach 12 pixels, still "
           "under the floor, beside ampersand B alone.")
    return rec("s-proofs-avatar-condensed", "proofs", 480, alt, _avatars("condensed"))


# ------------------------------------------------------------------------------------------- social card
def _social(width):
    files = WM if width == "today" else WMC
    card = (f'<div class="oai-s-newsprint" style="position:relative;width:1200px;height:630px;padding:72px 80px;border:1px solid {hair("newsprint")}">'
            f'<p class="oai-label" style="font-size:20px;color:{ink2("newsprint")}">Explain</p>'
            f'{headline("The zoning code", "the rent.", 104, extra_style="margin-top:20px;max-width:12ch")}'
            f'<p style="margin-top:28px;font-size:32px;line-height:1.3;max-width:28ch">Who decides what can be built near you, and when they vote next.</p>'
            f'<div style="position:absolute;left:80px;bottom:64px">{mark(files["display"], h=44, label="Oath & Action")}</div>'
            f'<div style="position:absolute;right:64px;bottom:64px">{lockmark(40, label="Lockmark")}</div></div>')
    return f'<div>{card}<p style="margin-top:12px">{illus()} <span class="oai-tag" style="margin-left:8px">{E(NAME[width])}</span></p></div>'


@spec
def s_proofs_social_today():
    alt = ("A social card at actual size, 1200 by 630 pixels, on Newsprint: the pillar word Explain, the hinge headline The "
           "zoning code & the rent. with a red ampersand B, a line under it, the wordmark at today's width at bottom left and "
           "the lockmark at bottom right. No web address. Illustrative.")
    return rec("s-proofs-social-today", "proofs", 1200, alt, _social("today"), illustrative=True,
               notes="1200 by 630, the link-preview size. The headline is chapter 02's W10 example (DR-75). No web address until the site is settled (DR-55).")


@spec
def s_proofs_social_condensed():
    alt = "The same social card at actual size with the condensed wordmark at bottom left, at the same height. Illustrative."
    return rec("s-proofs-social-condensed", "proofs", 1200, alt, _social("condensed"), illustrative=True)


# ------------------------------------------------------------------------------------------- letterhead
LETTER = [
    "We are writing to ask for the approved minutes of the Planning Board's October 14 meeting, and for any written comments the board received on the accessory dwelling bylaw before that date.",
    "We publish a plain account of how each decision on the bylaw was made, and we link readers to the official record. Your office's copy is the record we want to cite.",
    "An electronic copy is fine. If the request needs a fee, please tell us the amount before you begin, and we will pay it the same week.",
]


def _letter(width, for_print=False):
    files = WM if width == "today" else WMC
    w = mark(files["display"], h=26, label="Oath & Action")
    tag_line = "A country that answers to its people."
    lab = '' if for_print else f' {illus()}'
    paras = "".join(f'<p style="margin-top:14px">{E(t)}</p>' for t in LETTER)
    return (f'<div class="oai-s-white oai-letter" style="position:relative;width:816px;height:1056px;padding:72px 84px;border:1px solid {hair("white")};font-size:14.67px;line-height:1.55">'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{w}'
            f'<p style="font-size:13.33px;line-height:1.5;text-align:right;color:{ink2("white")}">Oath &amp; Action<br>PO Box 214<br>Alder, MA 01000{lab}</p></div>'
            f'<div style="margin-top:72px"><p>November 6, 2026</p>'
            f'<p style="margin-top:20px">Jordan Lee<br>Town Clerk, Town of Alder{lab}</p>'
            f'<p style="margin-top:20px">Dear Jordan Lee,</p>{paras}'
            f'<p style="margin-top:20px">Thank you,</p><p style="margin-top:28px">Dustin Cathcart<br>Founder and Editor</p></div>'
            f'<div style="position:absolute;left:84px;right:84px;bottom:56px;display:flex;justify-content:space-between;align-items:center;'
            f'border-top:1px solid {hair("white")};padding-top:14px">'
            f'<p style="font-size:13.33px;color:{ink2("white")}">{tag_line}</p>{lockmark(24, surface="white", label="Lockmark")}</div></div>')


def _pdf_link():
    if not PDF.exists():
        return ""
    data = base64.b64encode(PDF.read_bytes()).decode()
    return (f'<p style="margin-top:12px"><a download="20261106_Letterhead-Proof.pdf" href="data:application/pdf;base64,{data}" '
            f'style="font-weight:600;color:var(--oa-color-text-primary-on-newsprint)">Download the print proof, US Letter, two pages (PDF)</a></p>')


@spec
def s_proofs_letterhead_today():
    body = f'<div>{_letter("today")}<p style="margin-top:12px"><span class="oai-tag">{E(NAME["today"])}</span></p>{_pdf_link()}</div>'
    alt = ("A US Letter letterhead at true size on screen, 8.5 by 11 inches: the wordmark at today's width at top left, a "
           "return address at top right, a short records request to a town clerk signed by Dustin Cathcart, Founder and Editor, "
           "and a footer with the tagline and the lockmark. The address, recipient and letter are Illustrative. A link "
           "downloads the two-page print proof.")
    r = rec("s-proofs-letterhead-today", "proofs", 816, alt, body, illustrative=True,
            notes="96 CSS px to the inch, so the sheet is 816 by 1056 px. The display master at 26 px tall, as a print piece places it. Every line of text is 10 pt or larger.")
    r["interactive"] = True
    return r


@spec
def s_proofs_letterhead_condensed():
    body = f'<div>{_letter("condensed")}<p style="margin-top:12px"><span class="oai-tag">{E(NAME["condensed"])}</span></p></div>'
    alt = "The same letterhead with the condensed wordmark at the same height, at true size. Illustrative address, recipient and letter."
    return rec("s-proofs-letterhead-condensed", "proofs", 816, alt, body, illustrative=True)


def write_letterhead(pdf=False):
    """A standalone two-page US Letter page, masters inlined, printed to PDF by Chromium at its CSS page size."""
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    LIB.INLINE_ALL[0] = True
    try:
        pages = "".join(f'<section class="pg">{_letter(w, for_print=True)}</section>' for w in ("today", "condensed"))
    finally:
        LIB.INLINE_ALL[0] = False
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Letterhead proof, both wordmark widths</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>{LIB.CSS}'
            '@page{size:8.5in 11in;margin:0}html,body{margin:0;padding:0}body{font-family:var(--oa-font-family-reading)}'
            '.pg{width:8.5in;height:11in;overflow:hidden;break-after:page}.pg:last-child{break-after:auto}'
            '.oai-letter{border:0!important}.oai-svg{display:block}p{margin:0}</style></head>'
            f'<body class="oai">{pages}</body></html>')
    html_path = PROOF_DIR / "20261106_Letterhead-Proof.html"
    html_path.write_text(page)
    if pdf:
        subprocess.run(["node", str(HERE / "p2_print_pdf.js"), str(html_path), str(PDF)], check=True)


# ------------------------------------------------------------------------------------------- proofs.json
PROOFS = {
    "intro": [
        "Gate 2 settles the wordmark's width and ampersand B as refined (DR-71). Each piece below appears twice at actual size, first at today's width and then at the condensed width, both carrying ampersand B. Today's width stays in force until you choose.",
        "The studio recommends today's width and B as refined (D2-30). At the same height the condensed drawing only runs narrower, and its heavy capitals sit close to the lettering of campaign signs. Its monogram also reads as 0&A.",
    ],
    "groups": [
        {"label": "The marks at a glance", "text": ["The wordmark from each of its masters, the stacked lockup and the monogram, at the same height in both widths."],
         "items": [{"specimen": "s-proofs-glance", "label": "Both widths", "caption": "Same height, so the difference shows as width: 152 against 120 px from the 16 px masters."}]},
        {"label": "Masthead on the site", "text": ["L3 in the 1440 px bar, with the phone bar under it. Both widths sit at the same height, so the condensed bar is shorter by 40 px."],
         "items": [{"specimen": "s-proofs-masthead-today", "label": NAME["today"], "caption": "L3 from the 24 px master, 221 px wide, and a 52 px lockmark."},
                   {"specimen": "s-proofs-masthead-condensed", "label": NAME["condensed"], "caption": "L3 from the condensed 24 px master, 181 px wide, and the same lockmark."}]},
        {"label": "Masthead in email", "text": ["L3 at the head of a 600 px email. In a sent email it is a PNG at twice size with the alt text Oath & Action."],
         "items": [{"specimen": "s-proofs-email-today", "label": NAME["today"], "caption": "Invented headline and first line."},
                   {"specimen": "s-proofs-email-condensed", "label": NAME["condensed"], "caption": "Invented headline and first line."}]},
        {"label": "Avatar", "text": ["The monogram, L8, on the Charcoal tile that R13 sets as the default, in a circle and a square. Feeds draw an avatar at about 32 to 48 px, where L8 at either width sets its capitals under the 14 px floor; ampersand B alone reads there and is the same at both widths, so the studio recommends B for avatars whichever width you choose."],
         "items": [{"specimen": "s-proofs-avatar-today", "label": NAME["today"], "caption": "L8 fills 62 percent of the tile's width."},
                   {"specimen": "s-proofs-avatar-condensed", "label": NAME["condensed"], "caption": "Same width, so the condensed capitals stand taller; its narrow O reads close to a zero."}]},
        {"label": "Social card", "text": ["The 1200 by 630 link-preview card, with a hinge headline whose ampersand takes the card's working red. No web address until the site is settled (DR-55)."],
         "items": [{"specimen": "s-proofs-social-today", "label": NAME["today"], "caption": "Invented headline and line."},
                   {"specimen": "s-proofs-social-condensed", "label": NAME["condensed"], "caption": "Invented headline and line."}]},
        {"label": "Letterhead", "text": ["US Letter, 8.5 by 11 inches, at true size on screen (96 px to the inch). The print proof holds both widths, one per page; check its scale with a ruler before you judge it on paper."],
         "items": [{"specimen": "s-proofs-letterhead-today", "label": NAME["today"], "caption": "Invented address, recipient and letter, signed with Dustin's name and title."},
                   {"specimen": "s-proofs-letterhead-condensed", "label": NAME["condensed"], "caption": "Invented address, recipient and letter."}]},
    ],
}


def write_proofs_json():
    from stage_a_identity_chapters import smart

    def sm(o):
        if isinstance(o, dict):
            return {k: (v if k == "specimen" else sm(v)) for k, v in o.items()}
        if isinstance(o, list):
            return [sm(v) for v in o]
        return smart(o)
    (CHAP_DIR / "proofs.json").write_text(json.dumps(sm(PROOFS), indent=1, ensure_ascii=False) + "\n")
