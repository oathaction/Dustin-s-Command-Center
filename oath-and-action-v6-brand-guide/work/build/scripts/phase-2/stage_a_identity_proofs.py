"""Identity proofs (D2-328): the identity in use at true size on the site masthead, a social avatar, a link-preview card
and a letterhead, at today's width with ampersand B (DR-115), and L2 beside S1 at the same cap height at 48 px, 96 px and
display size, the record of DR-113. Also writes the letterhead print proof (US Letter, one page) and proofs.json.

Apply pass, November 7, 2026: the width pairs, the condensed minimums and the email pair leave (DR-115, D2-328). The
avatar shows ampersand B alone on the Charcoal tile (DR-116). The social card's sign-off is the lockmark at 48 px from
its display master (D2-327). The stage A letterhead proof (20261106_Letterhead-Proof.pdf, both widths) stays in the
proofs folder as the record of what board A showed; this pass writes a new one-page proof beside it.

Q1 to Q4 pass, November 8, 2026 (DR-131): the site masthead places L3's masthead master, the lockmark at 48 px from its
48 px master, and the social card's sign-off draws the 48 px master and prints the feed test's figures from
stage_a_identity_q_measure.py. The letterhead draws neither place, so it is unchanged.

Earlier rulings that still bind: each width-free proof is one specimen at actual size; kickers follow Rule 01.21
(D2-250); the social card breaks at the hinge and carries its specifications; the letterhead's town is invented
(Wrenfield) and its letter opens on the request; no decision codes or production words reach the page (D2-253)."""
import base64
import json
import subprocess

import stage_a_identity_lib as LIB
from stage_a_identity_lib import (E, ROOT, WM, L2, LOCK, AMP, S1, S1_BOX, mark, lockmark, illus, ink, ink2, hair, pal, tv, ty,
                                  CHAP_DIR, HERE, curl_html, figures)
from stage_a_identity_s03 import rec as _rec, l3_small
from stage_a_identity_s04 import headline

S = []
PROOF_DIR = ROOT / "work/boards/phase-2/stage-a/proofs"
PDF = PROOF_DIR / "20261107_Letterhead-Proof.pdf"
TAGLINE = "A country that answers to its people."


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "proofs")
    return _rec(*a, **k)


PROOF_CSS = (".oai .oai-pl{font:var(--oa-type-label);letter-spacing:var(--oa-type-label-letter-spacing);text-transform:uppercase;margin:0 0 8px}"
             ".oai-pl-x{text-transform:none;letter-spacing:0;font-weight:400;color:var(--oa-color-text-secondary-on-newsprint)}"
             ".oai-stackpair{display:flex;flex-direction:column;gap:28px;align-items:flex-start}")


def plabel(text, extra=""):
    tail = f' <span class="oai-pl-x">{E(extra)}</span>' if extra else ""
    return f'<p class="oai-pl">{E(text)}{tail}</p>'


def l3(surface="newsprint"):
    """L3 at the masthead's size, from its masthead master: the 24 px wordmark master, 13 px and the lockmark at 48 px
    from its 48 px master, 282 by 48 px on whole pixels (DR-131)."""
    return l3_small(24, surface=surface, label="Oath & Action")


def _burger(surface="newsprint"):
    return (f'<span aria-hidden="true" style="width:44px;height:44px;display:flex;flex-direction:column;justify-content:center;gap:5px;align-items:center">'
            + "".join(f'<span style="width:20px;height:2px;background:{ink(surface)}"></span>' for _ in range(3)) + '</span>')


# ------------------------------------------------------------------------------------------- masthead
def _desk_bar():
    nav = "".join(f'<span style="{ty("ui", 1440)}">{t}</span>' for t in ("Explain", "Track", "Connect", "Act", "About"))
    return (f'<div class="oai-s-newsprint" style="width:1440px;height:80px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 64px;border:1px solid {hair("newsprint")}">{l3()}<div style="display:flex;gap:32px">{nav}</div></div>')


def _phone_bar():
    return (f'<div class="oai-s-newsprint" style="width:390px;height:56px;display:flex;align-items:center;justify-content:space-between;'
            f'padding:0 8px 0 20px;border:1px solid {hair("newsprint")}">{mark(WM[24], h=24, label="Oath & Action")}{_burger()}</div>')


@spec
def s_proofs_masthead():
    body = ('<div class="oai-pad"><div class="oai-stackpair">'
            f'<div>{plabel("Site", "1440 px, L3")}{_desk_bar()}</div>'
            f'<div>{plabel("Phone", "390 px, L1 from the 24 px master")}{_phone_bar()}</div>'
            '</div></div>')
    alt = ("The site masthead at true size: a 1440 pixel Newsprint bar with OATH & ACTION and the lockmark at left and five "
           "navigation words at right. Below it, on the same left edge, the 390 pixel phone bar with the wordmark and a menu button.")
    return rec("s-proofs-masthead", "proofs", 1488, alt, body, css=PROOF_CSS, fit_switch=True,
               notes="Today's width (DR-115). L3 from its masthead master: the 24 px wordmark master (221 px), 13 px and the lockmark "
                     "at 48 px from its 48 px master (DR-131); phone bar with the 24 px master (Rule 03.6). The width pair it replaces "
                     "stays on board A as the record.")


# ------------------------------------------------------------------------------------------- avatar
def _b_tile(size, shape="circle"):
    b = 0.58 * size
    key = AMP["display"] if b >= 48 else (AMP[24] if b >= 24 else AMP[16])
    rad = "50%" if shape == "circle" else ("0" if shape == "full" else f"{0.2237 * size:.1f}px")
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;border-radius:{rad};'
            f'background:{tv("component-avatar-tile")};flex:none">{mark(key, h=b, surface="charcoal", decorative=True)}</span>')


def _upload():
    """The 400 px square a producer uploads, with the circle a platform cuts drawn as a hairline guide."""
    return (f'<span style="position:relative;display:inline-block;width:400px;height:400px;line-height:0">{_b_tile(400, "full")}'
            f'<span aria-hidden="true" style="position:absolute;inset:0;border-radius:50%;box-shadow:inset 0 0 0 1px {pal("stone")}"></span></span>')


def _feed_row(size):
    return (f'<div class="oai-s-white" style="width:288px;padding:12px;display:flex;gap:12px;align-items:center;border:1px solid {hair("white")}">'
            f'{_b_tile(size)}<div><p style="{ty("ui")};font-weight:600">Oath &amp; Action</p>'
            f'<p style="{ty("caption")};color:{ink2("white")}">Posted a link</p></div></div>')


@spec
def s_proofs_avatar():
    up = _upload()
    body = ('<div class="oai-pad"><div class="oai-row top" style="gap:24px">'
            f'<div style="width:400px">{plabel("Upload", "400 px square; the circle shows where a platform cuts it")}{up}</div>'
            f'<div class="oai-stack" style="gap:16px;width:288px">{plabel("In a feed")}{_feed_row(48)}{_feed_row(32)}'
            f'{plabel("App icon", "180 px")}{_b_tile(180, "square")}</div></div></div>')
    alt = ("Ampersand B alone, red on Charcoal, at true size: a 400 pixel square upload with a thin circle showing where a "
           "platform cuts it; the same avatar in a white feed at 48 and 32 pixels beside the name Oath & Action and the words "
           "Posted a link; and a 180 pixel Charcoal app icon with rounded corners.")
    return rec("s-proofs-avatar", "proofs", 760, alt, body, css=PROOF_CSS,
               notes="DR-116: B alone on the Charcoal tile, at 58 percent of the tile (Rule 04.7). The 400 px upload is Master Brief "
                     "section 18's starting size; platform circles are drawn as a guide, not read from a platform's help page.")


# ------------------------------------------------------------------------------------------- social card
SOCIAL_SPECS = [
    ("Size", "1200 by 630 px, the link-preview size"),
    ("Margin", "72 px on every side"),
    ("Kicker", "The H4 style at 24 px in Deep Stone: the content label, then the topic (Rule 01.21)"),
    ("Headline", "The title style at 110 px, broken at the hinge; B from its display master in the card's working red"),
    ("Wordmark", "The display master, 44 px tall, bottom left"),
    ("Lockmark", "48 px from its 48 px master, bottom right, inside the margin (Rule 08.2)"),
    ("Feed test", None),
    ("Left out", "A deck, so the headline keeps the title size, and a web address until ours is settled"),
]


def _social():
    return (f'<div class="oai-s-newsprint" style="position:relative;width:1200px;height:630px;padding:72px;border:1px solid {hair("newsprint")}">'
            f'<p style="{ty("h4", 1200)};color:{ink2("newsprint")}">Explainer · Zoning</p>'
            f'{headline("The zoning code", "the rent.", "title", board=1200, extra_style="margin-top:24px")}'
            f'<div style="position:absolute;left:72px;bottom:72px">{mark(WM["display"], h=44, label="Oath & Action")}</div>'
            f'<div style="position:absolute;right:72px;bottom:72px;line-height:0">{lockmark(48, label="Lockmark")}</div></div>')


def feed_line():
    """Rule 08.2's feed test on this card, as stage_a_identity_q_measure.py measured it on the built page."""
    f = figures("feed") or {}
    a, b = f.get("at_500"), f.get("at_360")
    if not (a and b and a.get("passes") and b.get("passes")):
        return "[run stage_a_identity_q_measure.py feed after the build, then build again]"
    return (f"Passes Rule 08.2's test. Reduced to 500 px wide, the lockmark keeps {a['dark_nodes_kept']} of 8 nodes and "
            f"{a['lever_red_px']} red pixels; at 360 px, {b['dark_nodes_kept']} of 8 nodes and {b['lever_red_px']} red pixels")


@spec
def s_proofs_social():
    specs = "".join(f'<div class="oai-sp"><dt>{E(a)}</dt><dd>{E(b if b is not None else feed_line())}</dd></div>' for a, b in SOCIAL_SPECS)
    css = PROOF_CSS + (".oai-spl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0 32px;margin:8px 0 0;max-width:1200px}"
                       ".oai-sp{display:grid;grid-template-columns:96px minmax(0,1fr);gap:12px;padding:8px 0;border-top:1px solid var(--oa-color-border-hairline-on-newsprint);font-size:14px;line-height:1.5}"
                       ".oai-sp dt{font-weight:700}.oai-sp dd{margin:0}")
    body = ('<div class="oai-pad"><div class="oai-stackpair">'
            f'<div>{plabel("Link-preview card", "1200 by 630 px")}{_social()}</div>'
            f'<div style="width:1200px"><p class="oai-pl">Specifications</p><dl class="oai-spl">{specs}</dl></div>'
            '</div></div>')
    alt = ("A social card at actual size, 1200 by 630 pixels, on Newsprint: the kicker Explainer · Zoning, the hinge headline "
           "The zoning code & the rent. broken before a red ampersand B, the wordmark 44 pixels tall at bottom left and the "
           "lockmark at 48 pixels at bottom right, inside the 72 pixel margin. No web address. Under it, the card's "
           "specifications. The headline and kicker are invented.")
    return rec("s-proofs-social", "proofs", 1248, alt, body, css=css, illustrative=True, fit_switch=True,
               notes="1200 by 630, the link-preview size, type at the desktop ceiling (D2-254). The headline is chapter 02's hinge example. "
                     "Sign-off from the lockmark's 48 px master at 48 px (DR-131), and the feed test's figures measured on this card "
                     "in the built page (work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json, key feed). No web address "
                     "until the site is settled (DR-55).")


# ------------------------------------------------------------------------------------------- letterhead
LETTER = [
    "Please send us the approved minutes of the Planning Board's October 14 meeting, and any written comments the board received before that date on the bylaw for backyard cottages, which the zoning code calls accessory dwelling units.",
    "We publish a plain account of how the board reached each decision on the bylaw, and we link readers to the official record. Your office's copy is the record we want to cite.",
    "An electronic copy is fine. If the request carries a fee, please tell us the amount before you begin, and we will pay it the same week.",
]
LETTER_SLUG = "The address, recipient and letter are invented."


def _letter():
    """One US Letter sheet at 96 px to the inch, type in points (D2-205). A line in the top margin says what is invented,
    so the sheet carries its label wherever it travels."""
    w = mark(WM["display"], h=26, label="Oath & Action")
    paras = "".join(f'<p style="margin-top:11pt">{E(t)}</p>' for t in LETTER)
    sec = ink2("white")
    return (f'<div class="oai-s-white oai-letter" style="position:relative;width:816px;height:1056px;padding:72px 84px;border:1px solid {hair("white")};font-size:11pt;line-height:1.55">'
            f'<div class="oai-slug" style="position:absolute;left:84px;right:84px;top:26px;display:flex;flex-wrap:wrap;align-items:center;gap:4px 10px;font-size:10pt;line-height:1.3;color:{sec}">'
            f'{illus()}<span>{E(LETTER_SLUG)}</span></div>'
            f'<div style="display:flex;justify-content:space-between;align-items:flex-start">{w}'
            f'<p style="font-size:10pt;line-height:1.5;text-align:right;color:{sec}">Oath &amp; Action<br>PO Box 214<br>Wrenfield, MA 01000</p></div>'
            f'<div style="margin-top:72px"><p>November 7, 2026</p>'
            f'<p style="margin-top:15pt">Jordan Lee<br>Town Clerk, Town of Wrenfield</p>'
            f'<p style="margin-top:15pt">Dear Jordan Lee,</p>{paras}'
            f'<p style="margin-top:15pt">Thank you,</p><p style="margin-top:21pt">Dustin Cathcart<br>Founder and Editor</p></div>'
            f'<div style="position:absolute;left:84px;right:84px;bottom:56px;display:flex;gap:12px;align-items:center;'
            f'border-top:1px solid {hair("white")};padding-top:14px">'
            f'{lockmark(24, surface="white", label="Lockmark")}<p style="font-size:10pt;color:{sec}">{E(TAGLINE)}</p></div></div>')


def _pdf_link():
    if not PDF.exists():
        return ""
    data = base64.b64encode(PDF.read_bytes()).decode()
    return (f'<p style="margin-top:16px"><a download="{PDF.name}" href="data:application/pdf;base64,{data}" '
            f'style="{ty("ui")};color:var(--oa-color-text-primary-on-newsprint)">Download the print proof, US Letter, one page (PDF)</a></p>')


@spec
def s_proofs_letterhead():
    body = f'<div class="oai-pad">{plabel("US Letter", "8.5 by 11 in at 96 px to the inch")}{_letter()}{_pdf_link()}</div>'
    alt = ("A US Letter letterhead at true size on screen, 8.5 by 11 inches: a line in the top margin saying the address, "
           "recipient and letter are invented; the wordmark at top left; a return address at top right; a records request to "
           "the town clerk of Wrenfield signed by Dustin Cathcart, Founder and Editor; and a footer with the lockmark at 24 "
           "pixels followed by the tagline. A link downloads the one-page print proof.")
    return rec("s-proofs-letterhead", "proofs", 864, alt, body, illustrative=True, css=PROOF_CSS, interactive=True, fit_switch=True,
               check_exempt=["scale"],
               notes="A print piece set in points (D2-205): 11 pt body, 10 pt address, slug and footer, so check_exempt scale. "
                     "96 CSS px to the inch, so the sheet is 816 by 1056 px. Display master at 26 px tall, as a print piece places it. "
                     "Footer: the lockmark at 24 px, 12 px, then the tagline, at the footer's left edge, the footer place as Rule 08.2 now draws it (CA-S10). interactive: the stage holds the PDF link.")


def write_letterhead(pdf=False):
    """A standalone one-page US Letter page, masters inlined, printed to PDF by Chromium at its CSS page size."""
    PROOF_DIR.mkdir(parents=True, exist_ok=True)
    LIB.INLINE_ALL[0] = True
    try:
        pages = f'<section class="pg">{curl_html(_letter())}</section>'
    finally:
        LIB.INLINE_ALL[0] = False
    tokens = (ROOT / "work/build/tokens/tokens.css").read_text()
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Letterhead proof</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Inter+Tight:wght@800&display=swap" rel="stylesheet">'
            f'<style>{tokens}</style><style>{LIB.CSS}'
            '@page{size:8.5in 11in;margin:0}html,body{margin:0;padding:0}body{font-family:var(--oa-font-family-reading)}'
            '.pg{width:8.5in;height:11in;overflow:hidden}'
            '.oai-letter{border:0!important}.oai-svg{display:block}p{margin:0}'
            '.illus{display:inline-block;padding:0 .4em;border:1px solid currentColor;font:700 10pt/1.5 var(--oa-font-family-reading);'
            'letter-spacing:.06em;text-transform:uppercase}</style></head>'
            f'<body class="oai">{pages}</body></html>')
    html_path = PROOF_DIR / "20261107_Letterhead-Proof.html"
    html_path.write_text(page)
    if pdf:
        subprocess.run(["node", str(HERE / "p2_print_pdf.js"), str(html_path.resolve()), str(PDF.resolve())], check=True)


# ------------------------------------------------------------------------------------------- L2 beside S1
# The record of DR-113 (D2-328): both lockups at one cap height. L2 has a display master only, so it is drawn from it at
# every size; S1 takes the master whose range holds the cap height (its 24 px master at 22 px capitals).
L2_BOX = (638.32, 217.96, 100.0)
PAIR_SIZES = [("48 px", 22.0), ("96 px", 44.0), ("Display size", 100.0)]


def _l2(caps):
    w, h, c = L2_BOX
    return mark(L2["today"], h=h * caps / c, label="L2, the stacked lockup S1 replaced")


def _s1(caps):
    key = 16 if caps < 18 else (24 if caps < 37 else "display")
    w, h, c = S1_BOX[key]
    return mark(S1[key], h=h * caps / c, label="S1, the stacked lockup in use")


@spec
def s_proofs_stacked():
    rows = []
    for name, caps in PAIR_SIZES:
        l2h = L2_BOX[1] * caps / 100
        rows.append(f'<div>{plabel(name, f"capitals {caps:g} px; L2 {l2h:.0f} px tall")}'
                    f'<div class="oai-row" style="gap:48px;flex-wrap:nowrap;align-items:flex-end">'
                    f'<div class="oai-cell">{_l2(caps)}<span class="oai-tag">L2, kept for the record</span></div>'
                    f'<div class="oai-cell">{_s1(caps)}<span class="oai-tag">S1, in use</span></div></div></div>')
    body = f'<div class="oai-pad"><div class="oai-stackpair" style="gap:36px">{"".join(rows)}</div></div>'
    alt = ("The two stacked lockups side by side at true size, at the same cap height, three times: capitals 22 pixels, so "
           "each stands about 48 pixels tall; capitals 44 pixels, about 96 tall; and the display masters at 100 pixel "
           "capitals. At left in each pair, L2: OATH over ACTION with a large ampersand at the right of the second line. At "
           "right, S1: OATH & over ACTION on two flush-left lines, the ampersand at the size of the capitals. S1 runs about a "
           "fifth narrower than L2 at every size.")
    return rec("s-proofs-stacked", "proofs", 1248, alt, body, css=PROOF_CSS, fit_switch=True,
               notes="The record of DR-113, Dustin's named approval of S1 in place of L2 (gate rule 4). Same cap height in each pair. "
                     "L2 from its display master at every size (it has no small masters); S1 from its 24 px master at 22 px capitals "
                     "and its display master at 44 and 100 px. Widths: L2 6.38x, S1 5.09x.")


# ------------------------------------------------------------------------------------------- proofs.json
PROOFS = {
    "title": "Identity proofs",
    "instruction": "Check the identity at true size on four pieces we publish, and see the stacked lockup that replaced L2.",
    "intro": [
        "These proofs set the wordmark, ampersand B and the lockmark at true size on four pieces we publish: the site's masthead, a social avatar, a link-preview card and a letterhead. Each follows the rules in chapters 03, 04 and 08.",
        "The last proof is a record. On November 7, 2026, Dustin Cathcart, our founder and editor, approved S1, the stacked lockup that sets OATH & over ACTION, in place of L2. The two stand side by side at the same cap height at three sizes, so anyone can check the change at true size.",
    ],
    "groups": [
        {"label": "Masthead on the site", "text": ["L3 in the 1440 px site bar and L1 in the 390 px phone bar, on one left edge (Rule 03.6)."],
         "items": [{"specimen": "s-proofs-masthead", "label": "Site and phone", "caption": "Use Fit to window to see the site bar whole on a smaller screen."}]},
        {"label": "Avatar", "text": ["Ampersand B alone on the Charcoal tile, as Rule 04.7 sets it for social avatars and the app icon. The platform prints our name beside the avatar, so the mark can be B alone."],
         "items": [{"specimen": "s-proofs-avatar", "label": "Upload, feed and app icon", "caption": "At 32 px in a feed, B still reads, where any lettered mark would set its capitals under the 14 px floor."}]},
        {"label": "Social card", "text": ["The 1200 by 630 link-preview card, with its specifications under it. Its sign-off passes Rule 08.2's feed test at 500 and 360 px wide."],
         "items": [{"specimen": "s-proofs-social", "label": "Link-preview card", "caption": "Until chapter 23 sets social cards, build one from these specifications."}]},
        {"label": "Letterhead", "text": ["US Letter, 8.5 by 11 inches, at true size on screen, 96 px to the inch. Check the print proof's scale with a ruler before you judge it on paper."],
         "items": [{"specimen": "s-proofs-letterhead", "label": "US Letter", "caption": "The address, recipient and letter are invented, and the letter is signed with Dustin's name and title."}]},
        {"label": "L2 beside S1", "text": ["The record of the change to the stacked lockup: L2 at left and S1 at right in each pair, at the same cap height."],
         "items": [{"specimen": "s-proofs-stacked", "label": "Three sizes", "caption": "S1 reads in the name's order with B at the size of the capitals, and it runs about a fifth narrower than L2 at every size."}]},
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
