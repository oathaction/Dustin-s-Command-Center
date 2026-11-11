"""Chapter content for 03 Identity, 04 The Ampersand and the hinge, and 08 The lockmark.

Apply pass, November 7, 2026: S1 replaces L2 (DR-113); today's width is the one in force (DR-115); avatars show B alone
(DR-116); the crop takes the surface's ink (DR-117); B alone ends an article and the badge keeps sizes from 48 px (DR-118);
chapter 08 becomes The lockmark, with four places and no codes (DR-110, D2-325 to D2-327).

Q1 to Q4 pass, November 8, 2026: L6 without its pillar dots (DR-129); the end mark at the text's cap height, with Rule
03.4's exception line and measured figures (DR-130, CD-N8); the lockmark's 48 px master in the masthead and the sign-off,
L3's masthead master and Rule 08.2's feed test (DR-131, CA-S1, CA-S2). Measured figures come from
work/handoffs/phase-2/20261108_Q1-To-Q4-Identity-Figures.json, written by stage_a_identity_q_measure.py.

Promotion, November 10, 2026: the end mark's pixel masters on a 1x screen in 17 and 15 px text (DR-180), the rebuilt 24
and 48 px lockmark masters (DR-181) and L6 centered (DR-182). The end mark's fit figures and the feed test's figures
with the rebuilt master come from work/handoffs/phase-2/20261110_Promotion-Identity-Figures.json (promotion_identity.py).

Stage C, round 0, November 10, 2026: Rule 08.2's feed test gains its version for a dark card (CD-N12, D2-715), with
floors measured on the proofs' card drawn on Charcoal and Prussian; figures from
work/handoffs/phase-2/20261110_Stage-C-Identity-Figures.json, key feed_dark (stage_c_identity_round0.py). Chapter
09 names its opener figure, s-09-opener (D2-1134).

Promotion C, November 11, 2026: the print L3 serves print and every width but the 282 px masthead (DR-210), in Rules
03.2, 03.6 and 08.2; social cards sign off at 96 px, the 48 px master at exactly twice its size, and covers, posters and
the masthead keep 48 px (DR-211), in Rules 03.4, 08.1 and 08.2. Rule 08.2's feed figures, on all four grounds, and the
thumbnail figures come from work/handoffs/phase-2/20261111_Promotion-C-Identity-Figures.json (promotion_c_identity.py).

Every word follows chapter 02's writing section (DR-73). Typographic quotes and apostrophes are set by smart() on the
prose fields, so the source stays easy to edit."""
import re

from stage_a_identity_lib import figures, LOCK, L3, AMP_END, SIGN_OFF

_END = (figures("endmark") or {}).get("measured_at_8x", {})
_FEED = figures("feed") or {}            # since promotion C, the card with its 96 px sign-off (DR-211), promotion_c_identity.py
_FIT = figures("endmark_fit") or {}      # the end mark's pixel masters (DR-180), promotion_identity.py
_FEED_DARK = figures("feed_dark") or {}  # the feed test on every ground (stage C, CD-N12), since promotion C on the 96 px card
_THUMB = figures("feed_thumbnail") or {}  # the thumbnail path at 48 and 96 px (DR-211), promotion_c_identity.py


def _end(text_px):
    m = _END.get(str(text_px))
    if not m:
        return f"[run stage_a_identity_q_measure.py endmark for {text_px} px]"
    return (f"capitals {m['capitals_px']:.1f} px; B {m['b_px']:.1f} px tall, its top {m['top_over_cap_line_px']:.1f} px over the "
            f"cap line and its tail {m['tail_under_baseline_px']:.1f} px under the baseline")


def _feed():
    """Rule 08.2's test on the proofs' card as the built page draws it, with its 96 px sign-off (DR-211), from
    promotion_c_identity.py's figures."""
    a, b = _FEED.get("at_500"), _FEED.get("at_360")
    if not (a and b and a.get("passes") and b.get("passes")) or _FEED.get("sign_off_px") != SIGN_OFF["social"]:
        return "[run promotion_c_identity.py feed after the build, then build again]"
    return (f"The link-preview card in the identity proofs, on Newsprint, passes with its {SIGN_OFF['social']} px sign-off. At 500 px wide, its "
            f"lockmark keeps {a['dark_nodes_kept']} of 8 nodes and {a['lever_red_px']} red pixels; at 360 px, "
            f"{b['dark_nodes_kept']} of 8 nodes and {b['lever_red_px']} red pixels")


def _thumb():
    """Why a social card signs off at 96 px (DR-211): the thumbnail path, measured on our card at 360 px with the sign-off
    at 48 and at 96 px (promotion_c_identity.py, key feed_thumbnail)."""
    t = _THUMB.get("newsprint", {})
    try:
        r48, r96 = t["48"]["at_360"]["lever_red_px"], t["96"]["at_360"]["lever_red_px"]
    except (KeyError, TypeError):
        return "[run promotion_c_identity.py feed, then build again]"
    return (f"On a social card the sign-off stands at {SIGN_OFF['social']} px. A feed shrinks the card to 500 px wide or less, "
            "and some services then save the small copy as a JPEG that keeps color in blocks of 2 by 2 pixels. On our card at "
            f"360 px, that leaves the lever {_n(r48, 'red pixel')} at 48 px and {_n(r96, 'red pixel')} at {SIGN_OFF['social']} px.")


def _n(k, word):
    return f"no {word}s" if k == 0 else f"{k} {word}" + ("" if k == 1 else "s")


def _feed_dark(part):
    """Rule 08.2's feed test on a dark card (stage C, CD-N12): the floors ("rule") or the proofs' card drawn on White,
    Charcoal and Prussian ("card"). Since promotion C, measured on the card with its 96 px sign-off (DR-211) by
    promotion_c_identity.py feed; stage_c_identity_round0.py's figures, on the 48 px card, stay as the record."""
    f = _FEED_DARK
    try:
        fl, c, p = f["floors"], f["charcoal"], f["prussian"]
        ok = all(c[w]["passes"] and p[w]["passes"] for w in ("at_500", "at_360"))
    except (KeyError, TypeError):
        ok = False
    if not ok:
        return "[run promotion_c_identity.py feed, then build again]"
    if part == "rule":
        if f.get("dark_unit") != "block of 2 by 2 pixels":
            return "[run promotion_c_identity.py feed, then build again]"
        # stage C round 2 (CD-S16): the block's four pixels each clear the floor, the block sits anywhere in the node's
        # square plus 1 px, and the card is reduced with Lanczos, as promotion_c_identity.counts runs it
        return (f"On Charcoal, each of the eight light nodes keeps at least one block of 2 by 2 pixels, anywhere in the "
                f"node's square plus 1 px on every side, whose four pixels each have every color channel over "
                f"{fl['charcoal']}. Judge each pixel on its own, since an average of the four can pass a block whose dimmest "
                f"pixel fails. The lever keeps at least four red pixels, counted as on a light ground. On Prussian, where "
                f"the lever is White as well, each of the nine nodes keeps such a block, its four pixels each with every "
                f"channel over {fl['prussian']}. Reduce the card with Lanczos resampling, as on a light ground. On a dark "
                f"ground the links take the nodes' own color. In a {SIGN_OFF['social']} px "
                "sign-off they run 2 px wide, so a single bright pixel can come from a link, and the test counts blocks because "
                "a link the feed shrinks under 1 px wide cannot fill one. Each floor sits halfway between the brightest block "
                "the links alone leave in a node's square and the dimmest node's brightest block, measured on our card at both "
                "widths, then rounded down to a multiple of 5")
    if f.get("sign_off_px") != SIGN_OFF["social"] or not all(f["white"][w]["passes"] for w in ("at_500", "at_360")):
        return "[run promotion_c_identity.py feed, then build again]"
    def fig(g):
        x, y = f[g]["at_500"], f[g]["at_360"]
        return (x["nodes_kept"], x["lever_red_px"], y["nodes_kept"], y["lever_red_px"])

    def said(n5, r5, n3, r3):
        return f"{n5} of 8 nodes and {r5} red pixels at 500 px, and {n3} of 8 nodes and {r3} red pixels at 360 px"
    p5, p3 = p["at_500"]["nodes_kept"], p["at_360"]["nodes_kept"]
    pr = ("On Prussian, with the White lever counted as a ninth node, it keeps "
          + (f"{p5} of 9 nodes at both widths" if p5 == p3 else f"{p5} of 9 nodes at 500 px and {p3} of 9 at 360 px"))
    if fig("white") == fig("charcoal"):          # one sentence when the two grounds give the same figures
        return f"Drawn on White or on Charcoal, the same card keeps {said(*fig('white'))}. " + pr
    return (f"Drawn on White, the same card keeps {said(*fig('white'))}. On Charcoal it keeps {said(*fig('charcoal'))}. " + pr)


_B17 = _END.get("17", {})


def _fit(text_px):
    """The pixel master's height and width in px at a text size, as the promotion's figures give them."""
    m = _FIT.get(str(text_px))
    if not m:
        return None
    return round(m["b_px"]), round(m["b_width_px"])


_F17, _F15 = _fit(17) or (0, 0), _fit(15) or (0, 0)

A = "work/build/assets/identity/"


def smart(t):
    if not isinstance(t, str):
        return t
    t = re.sub(r"(\d) (px|pt|in|mm)\b", "\\1\u00a0\\2", t)      # CA-N4: a number keeps its unit on its line
    parts = re.split(r"(<code>.*?</code>|<[^>]+>)", t)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p)
            continue
        p = re.sub(r'(^|[\s(\[])"', "\\1\u201c", p)
        p = p.replace('"', "\u201d")
        p = re.sub(r"(\w)'(\w)", "\\1\u2019\\2", p)
        p = re.sub(r"(\w)'(\s|$|[.,;:])", "\\1\u2019\\2", p)
        p = re.sub(r"(^|\s)'(\w)", "\\1\u2018\\2", p)
        out.append(p)
    return "".join(out)


def S(label, value, token=None):
    d = {"label": label, "value": value}
    if token:
        d["token"] = token
    return d


def fails(id_, caption):
    """Gate 2's fix pass (CD-S2): a failure caption leads with the rule it breaks, in bold, as stage C's captions do."""
    lead = f"<strong>Fails Rule {id_}.</strong> "
    return caption if caption.startswith("<strong>Fails Rule") else lead + caption


def R(id_, title, rule, why, basis, correct, failure, *, tokens=(), specs=(), files=(), related=(), builders="", corrective=None):
    r = {"id": id_, "title": title, "rule": rule, "tokens": list(tokens), "why": {"text": why, "basis": basis},
         "correct": {"specimen": f"s-{id_.replace('.', '-')}-correct", "caption": correct},
         "failure": {"specimen": f"s-{id_.replace('.', '-')}-failure", "caption": fails(id_, failure)},
         "specs": list(specs), "files": list(files), "related": list(related), "builders": builders}
    if corrective:
        r["corrective"] = {"specimen": f"s-{id_.replace('.', '-')}-corrective", "caption": corrective}
    return r


DJ = "Design judgment"

# =========================================================================================== 03 Identity
CH03 = {
    "number": "03", "anchor": "identity", "title": "Identity", "part": "Foundations",
    "instruction": "Pick the lockup that fits the surface and size, and give it room on every side.",
    # Gate 2's fix pass (CD-S1): the opener, a plate of the chapter's subject under the intro
    "opener": {"specimen": "s-03-opener", "caption": "Seven of the eight lockups at true size, from the masters Rule 03.2's plate draws. L5 needs 388 px, so it shows on screens 48em wide and up, and L6, at 884 px, has its own plate under Rule 03.2."},
    "intro": [
        "The wordmark is our name drawn as one piece of artwork: OATH and ACTION in heavy capitals, joined by ampersand B, the red ampersand we drew for Oath & Action. A lockup is a fixed arrangement of the wordmark with another part, such as the tagline or the lockmark, the three by three grid of nodes that chapter 08 explains.",
        "Every mark here is a vector master drawn for a range of sizes. You place the master, color it with tokens and leave room around it. In this chapter x means the height of the wordmark's capitals. The wordmark keeps the width our fifth edition drew, with ampersand B as refined for this edition, and the identity proofs at the end of the guide show it in use.",
    ],
    "rules": [
        R("03.1", "Place the wordmark from its master file.",
          "Use the master drawn for the height you need and set its color with tokens. The masters hold the wordmark's one width, the width our fifth edition drew, with ampersand B as refined for this edition. Never type the name in a font, Inter Tight included, though we cut the capitals from it.",
          "The masters set every gap between letters by eye and give the ampersand the same white on each side, 0.203x, so the name keeps one shape from a 16 px email footer to a printed banner. Ampersand B exists only as drawn artwork. A typed name takes the font's ampersand and the font's spacing, and a reader who meets two slightly different names starts to wonder which one is ours.",
          DJ,
          "The display master at 440 px wide on Newsprint, with its construction drawn in: the cap line and baseline, x, one cap height of clear space and the white on each side of the ampersand.",
          "The name typed in Inter Tight 800 for a slide. The font's own ampersand stands in for B, the gaps come out wide and uneven, and the result no longer matches the masthead the reader saw a minute earlier.",
          tokens=["oa.color.text.primary.onNewsprint", "oa.color.identity.signature.onNewsprint"],
          specs=[S("Width", "One width, 9.78x at every size: the width our fifth edition drew, with ampersand B as refined"),
                 S("Display master", "From 40 px tall; 978.31 by 108 units, capitals 100 units"),
                 S("24 px master", "From 20 to 39 px tall; 221 by 24 px, capitals 22 px"),
                 S("16 px master", "From 16 to 19 px tall; 152 by 16 px, capitals 14 px"),
                 S("White beside the ampersand", "0.203x on each side, measured as area"),
                 S("Overshoot", "The O and the ampersand run 1.34 units past the cap line and the baseline"),
                 S("Letters", "Charcoal on light surfaces, Newsprint on Charcoal", "oa.color.text.primary.onNewsprint"),
                 S("Ampersand", "Signature red on Newsprint, White and Charcoal; White on Prussian", "oa.color.identity.signature.onNewsprint")],
          files=[A + "wordmark/20261028_Wordmark-Display-Master.svg", A + "wordmark/20261028_Wordmark-24px-Master.svg", A + "wordmark/20261028_Wordmark-16px-Master.svg"],
          related=["04", "05", "27"],
          builders="Pick the file by the height you will draw it, from the files this rule lists. Set <code>color</code> to the surface's primary text token and <code>--amp</code> to its signature token; the file reads both. On Prussian, place the file from <code>prussian/</code>, which carries White in the drawing."),
        R("03.2", "Choose the lockup by the space and the surface.",
          "Eight lockups cover every use, and each has one job. Start from the width you have: L1, the wordmark alone, for most uses; L3, the wordmark with the lockmark, for the site and email masthead; S1, the stacked lockup, OATH & over ACTION, for square formats and posters; and L8, the monogram, for small squares where the name must show. The sheet after this rule shows all eight at true size, and the specifications give each one's minimum.",
          "A fixed set means a reader meets the same arrangement in the same place, and a producer never has to invent one. Each lockup's job comes from the space it fills, so the choice turns on two facts you can measure: the width you have and the surface under it.",
          DJ,
          "A 120 px tile in a partner directory carries L8 at 74 px wide, so its capitals stand 25 px tall.",
          "The same tile with the full wordmark squeezed in at 100 px wide. Its capitals drop to 10 px, under the 14 px floor, and the white around the ampersand fills in.",
          specs=[S("L1 Wordmark", "Most uses: page heads, documents, slides and signs. Minimum 16 px tall, 152 px wide; 1.20 in"),
                 S("S1 Stacked", "OATH & over ACTION, flush left, for square formats and posters. Minimum 79 px wide; 0.65 in"),
                 S("L3 Horizontal with the lockmark", "The site and email masthead, where it is 282 px wide with the lockmark at 48 px. Minimum 196 px wide; 1.55 in"),
                 S("L4 Monogram and tagline", "Document footers and small print. Minimum 304 px wide; 2.30 in"),
                 S("L5 Wordmark and tagline", "Covers, banners and partner placements where the tagline travels with the mark. Minimum 388 px wide; 2.90 in"),
                 S("L6 Editorial signature", "The strip that closes a report or a long page: the wordmark over the tagline, centered on the strip's height, and the lockmark at right. Minimum 884 px wide; 6.60 in. A narrower page closes with the footer place (Rule 08.2)"),
                 S("L7 Section masthead", "Names the pillar a piece serves. Minimum 250 px wide with the longest pillar word; 1.90 in"),
                 S("L8 Monogram", "Small squares where the name must show, such as a tile in a partner's directory; never an avatar or a favicon. Minimum 48 px wide; 0.50 in")],
          files=[A + "lockups/20261107_S1-Stacked-Master.svg", A + "lockups/20261107_S1-Stacked-Master-24px.svg", A + "lockups/20261107_S1-Stacked-Master-16px.svg",
                 A + L3["masthead"], A + L3["print"], A + "lockups/20261028_L8-Monogram-Master.svg"],
          related=["04", "07", "27"],
          # stage C round 2 (PP-S12): one short line per lockup, and the record sentence dropped; the L3 lines keep DR-217
          builders=["Every lockup: check its minimum before you place it, and under that minimum switch to the lockup Rule 03.4's table names.",
                    "L1: place the wordmark master drawn for its height (Rule 03.1).",
                    "S1: place its master for the size. Its files come in a Charcoal edition with its colors written in, for light grounds, and a White edition in <code>prussian/</code>. S1 replaced the stacked L2 in November 2026, so retire L2 from your templates.",
                    "L3 in the masthead: place L3's masthead master, which serves the 282 px masthead on screen.",
                    "L3 elsewhere on screen, with the wordmark under 40 px tall: build it from the masters drawn on the pixel grid, the wordmark's 16 or 24 px master beside the lockmark's master for its size, as the 196 px minimum does.",
                    "L3 in print, and on screen with the wordmark 40 px tall or more: place L3's print master, which sets the lockmark at 2.18 cap heights, the masthead's proportion.",
                    "L4, L5 and L7: none has a master file yet, so build each from the wordmark, monogram and tagline masters on the layouts from our brand guide's fifth edition, as the sheet shows, or ask the editor for a file.",
                    "L6: build it the same way, and leave out the four dots our fifth edition drew under its tagline. Move the wordmark and tagline down 14.7 of L6's 300 units, 9.3 px at 884 px, so the span from the wordmark's cap line to the tagline's baseline sits centered on the strip, as the lockmark does.",
                    "L8: place its master from 48 px wide, in the colors Rule 03.5 sets for the surface."]),
        R("03.3", "Keep one cap height of clear space on every side.",
          "Leave 1.0x of open space around the lockup's outer edge, with its tagline and lockmark inside that edge. Text, rules, image edges and other logos all stay outside it. In a partnership lockup the hairline and the partner's logo belong to the lockup, so the clear space runs around all three (Rule 03.8). Over a photograph, set the lockup on a solid Newsprint or Charcoal panel with the same space inside the panel.",
          "Open space lets the eye find the name before it reads anything else, and it keeps a headline or a partner's logo from reading as part of our mark. A measure of one cap height grows with the mark, so the rule holds at every size.",
          DJ,
          "A page head at true size: L1 at 32 px tall, its clear space drawn in, and the headline set below that space.",
          "The same page head with the headline moved up to 9 px under the wordmark, 0.3x. The headline's first words read as part of the name.",
          tokens=["oa.space.400"],
          specs=[S("Clear space", "1.0x on every side, from the outer edge of the lockup"),
                 S("At 32 px capitals", "32 px, the 400 step of the spacing scale", "oa.space.400"),
                 S("Taglines in L4, L5 and L6", "Part of the lockup; clear space starts outside them"),
                 S("Partnership lockup", "The hairline and the partner's logo are part of the lockup; clear space starts outside the partner's logo"),
                 S("Over a photograph", "A solid Newsprint or Charcoal panel, with 1.0x inside it")],
          related=["07", "12"],
          builders="Round the clear space up to the next step of the spacing scale, so a page built on the 8 px rhythm keeps it."),
        R("03.4", "Keep every mark at or above its minimum size.",
          "On screen, no identity mark draws its capitals under 14 px, and no tagline inside a lockup sets under 13 px. In print, no capitals under 3 mm and no tagline under 7 pt. Under a lockup's minimum, switch to the lockup the table names. Only the end mark, ampersand B at the close of an article, may stand under B's 16 px minimum, at the text's cap height, because it follows a word and names nothing on its own (Rule 04.6).",
          "We drew and checked each master at its smallest size, where the wordmark keeps its six enclosed counters, the holes inside letters such as O and A, and the ampersand keeps its two. Our fifth edition scaled one drawing to every size, and at its own 120 px minimum a notch in the ampersand closed into a seventh enclosed shape.",
          "Our measurements, October 2026",
          "Every mark at its screen minimum, at true size. These are graphics drawn at their smallest allowed size, so the 13 px floor for text does not apply to the letters inside them.",
          "The display master scaled to 12 px tall for an email footer. Its capitals fall to 11 px, the white around the ampersand fills in and the name blurs. The 16 px master, 152 px wide, fits the same footer.",
          specs=[S("L1", "16 px tall, 152 px wide; 1.20 in in print"),
                 S("S1", "79 px wide, capitals 14 px; 0.65 in"),
                 S("L3", "196 px wide; 1.55 in"),
                 S("L8", "48 px wide; 0.50 in; never a favicon"),
                 S("Ampersand B and the lockmark", "16 px; 0.25 in"),
                 S("End mark", f"Ampersand B at the text's cap height, under 16 px in body text. On a 1x screen it is its pixel fit, a copy redrawn on whole pixels, {_F17[0]} px tall in 17 px text and {_F15[0]} px in 15 px text. Every denser screen, 1.25x and 1.5x included, takes the 16 px master, since there the pixel fit's edges fall between device pixels and soften (Rule 04.6)"),
                 S("Hinge-circle badge", "48 px; 0.50 in (Rule 04.6)"),
                 S("L4 to L7", "Their minimums are in Rule 03.2's specifications"),
                 S("Favicon", "Ampersand B's 16 px master at 16 px")],
          files=[A + "20261028_Identity-Minimum-Sizes.json"],
          related=["06", "19", "27"],
          builders="Read the height you will draw, then pick the master whose range holds it. For the wordmark, the 16 px master runs from 16 to 19 px tall, the 24 px master from 20 to 39 px and the display master from 40 px. For ampersand B, the 16 px master runs from 16 to 23 px, the 24 px master from 24 to 47 px and the display master from 48 px (Rule 04.1). The lockmark's 16 and 24 px masters take B's ranges. Its 48 px master serves 48 px, and exactly twice that, 96 px, in a social card's sign-off; its display master serves every other size from 49 px (Rule 08.1). S1's masters follow its capitals: the 16 px master for capitals 14 to 17 px, the 24 px master for 18 to 36 px and the display master from 37 px. The badge starts at 48 px, from its display master. In print, set the width in inches from the table."),
        R("03.5", "Set the marks in their colors on the four approved surfaces.",
          "Newsprint, White and Charcoal carry the wordmark with its red ampersand. On Prussian every mark goes White, ampersand and lever included, because red never sits on Prussian (Rule 05.3). One-color versions in Charcoal or White serve one-color print, embossing and watermarks.",
          "Each surface has one ink that reads on it: Charcoal on Newsprint at 13.29 to 1, Newsprint on Charcoal at 13.29 to 1, White on Prussian at 13.28 to 1. Pillar Red measures 3.19 to 1 on Prussian, a little over the 3 to 1 a graphic needs, but once drawn small it falls short: our fifth edition's red ampersand measured 2.27 to 1 there at 16 px. Red on our dark blue also reads as a pair of party colors, which Rule 01.1 keeps off every page.",
          "Design judgment, measured against WCAG 2.2 SC 1.4.11 at rendered sizes; Rule 05.3 for red",
          "L1, S1 and L8 on six grounds at true size: Newsprint, White and Charcoal with the red ampersand, Prussian in White, and the one-color versions.",
          "The Newsprint file dropped onto a Charcoal slide. The Charcoal letters vanish into the ground and only the red ampersand shows.",
          tokens=["oa.color.text.primary.onCharcoal", "oa.color.identity.signature.onCharcoal", "oa.color.identity.signature.onPrussian"],
          specs=[S("Newsprint and White", "Charcoal letters, red ampersand, Stone links in the lockmark"),
                 S("Charcoal", "Newsprint letters and links, red ampersand and lever at 4.49 to 1", "oa.color.identity.signature.onCharcoal"),
                 S("Prussian", "Every part White, from the files in prussian/", "oa.color.identity.signature.onPrussian"),
                 S("One color", "Charcoal on light grounds, White on dark ones")],
          files=[A + "prussian/20261028_Wordmark-Display-Master-Prussian-White.svg", A + "prussian/20261107_S1-Stacked-Master-Prussian-White.svg",
                 A + "prussian/20261028_L8-Monogram-Master-Prussian-White.svg"],
          related=["05", "12", "27"],
          builders="Pick the surface first. On Prussian, place the file whose name ends in Prussian-White; it needs no CSS."),
        R("03.6", "Use L3 for the masthead, and drop the lockmark when the bar gets narrow.",
          "The masthead is the bar across the top of every page and email. From 48em wide, 768 px at the default text size, it sets L3 from its masthead master: the wordmark at left and, to its right, the lockmark's 48 px master at 48 px. Under 48em, it sets L1 from the 24 px master beside the menu button. Email takes L3 as an image.",
          "The masthead is the one place every reader sees the mark, so it carries the fullest lockup the width allows. The lockmark needs about 34 px to show its nine nodes and its lever, and on a phone that room goes to the menu button.",
          DJ,
          "Three mastheads at true size: the site at 1440 px, the site on a 390 px phone and a 600 px email header, each from the master drawn for its height.",
          "L3 squeezed to 150 px across a phone bar, under its 196 px minimum. Its capitals fall to 12 px, under the 14 px floor, and the lockmark to 26 px.",
          specs=[S("Site, from 48em", "L3 from its masthead master: the 24 px wordmark master, 13 px of space and the lockmark at 48 px from its 48 px master, 282 by 48 px on whole pixels; bar 80 px tall"),
                 S("Site, under 48em", "L1 from the 24 px master, 221 px wide; bar 56 px; menu button 44 px", "oa.size.target.touch"),
                 S("Email header", "L3 at 282 px in a 600 px header, sent as a PNG at twice size"),
                 S("In print", "L3's print master, with the lockmark at 2.18 cap heights, the masthead's proportion (Rule 03.2)"),
                 S("Section masthead", "L7: L1, a hairline and the pillar's name in Inter 600 capitals, in the surface's ink")],
          files=[A + L3["masthead"], A + "wordmark/20261028_Wordmark-24px-Master.svg", A + LOCK[48], A + L3["print"]],
          related=["07", "20", "22"],
          builders="Write the switch as a media query in em, <code>@media (min-width: 48em)</code>, so it follows the reader's text size (Rule 07.5). In email, export the masthead as a PNG at twice its size with the alt text \"Oath & Action\". Most email clients drop web fonts, and several show no inline SVG. In a short email whose footer shows in the same view as its header, set L1 at the top and keep the lockmark in the footer (Rule 08.2)."),
        R("03.7", "Use L8 as the one monogram, and retire the spaced \"O & A\".",
          "L8 sets O and A with ampersand B between them, cut from the same masters as the wordmark. It serves squares where the name must show, such as a tile in a partner's directory, from 48 px wide. Social avatars and the app icon show ampersand B alone on the Charcoal tile (Rule 04.7). The compact signature from our brand guide's fourth edition, \"O & A\" typed with word spaces, retires, along with any other typed monogram.",
          "Two monograms split what readers learn to recognize. L8 keeps the wordmark's own white beside the ampersand, so it reads as the name in brief. Typed with spaces, the three characters read as separate letters, and the font's ampersand replaces B.",
          DJ,
          "L8 at its 48 px minimum and at 120 px, on Newsprint and on Charcoal.",
          "Our fourth edition's compact signature, typed in Inter Tight with word spaces and the font's own ampersand.",
          specs=[S("Display master", "299.67 by 108 units"), S("Minimum", "48 px wide, capitals 16 px; 0.50 in"),
                 S("Below the minimum", "Ampersand B's 16 px master"), S("Avatars and the app icon", "Never L8; ampersand B alone on the Charcoal tile (Rule 04.7)"),
                 S("Favicon", "Never L8; ampersand B's 16 px master")],
          files=[A + "lockups/20261028_L8-Monogram-Master.svg"],
          related=["04", "23"],
          builders="L8 belongs where the name has to show and the square has room for 16 px capitals. For an app tile or an avatar, the platform prints the name, so use ampersand B alone on the Charcoal tile (Rule 04.7)."),
        R("03.8", "Join a partner with a hairline, and keep our ampersand inside our name.",
          "In a partnership lockup the host's name leads: on a piece we host, L1 sits at left; on a piece the partner hosts, the partner's logo sits at left and L1 follows. A 1 px vertical hairline stands between them with 0.6x of space on each side, and the partner's logo stands no taller than our capitals. For a square, set L8 beside the partner's logo the same way. Our ampersand stays inside the wordmark, and a second ampersand or a plus sign never joins the two names.",
          "The ampersand is our hinge between an oath and the action that keeps it. Used to join two organizations, it turns our mark into a conjunction anyone can borrow, and the reader sees one organization with a long name. A hairline marks a partnership and gives each name its own field, and the host leads because a reader first wants to know who is holding the event.",
          "Design judgment, approved by our founder and editor in November 2026",
          "Two partnership lockups at true size, each led by the host: our name on a piece we host, the partner's on a piece it hosts. The partner is invented.",
          "An event flyer that joins the names with a second ampersand, so it reads as one organization called \"Oath & Action & Merrimack Valley Civic Lab\".",
          tokens=["oa.color.border.hairline.onNewsprint"],
          specs=[S("Order", "The host's name leads, at left"),
                 S("Hairline", "1 px on screen, 0.5 pt in print; 1.2x tall, centered on our capitals", "oa.color.border.hairline.onNewsprint"),
                 S("Space", "0.6x on each side of the hairline"),
                 S("Partner", "Its logo as the partner draws it, or its name in Inter 600, no taller than 1.0x"),
                 S("Square formats", "L8 beside the partner's logo, with the same hairline and space"),
                 S("Clear space", "1.0x around the whole lockup, partner included (Rule 03.3)"),
                 S("Approval", "Dustin Cathcart, or an editor he names, sees each co-branded piece before it prints or posts")],
          related=["01", "25"],
          builders="Ask the partner for its logo file and its own clear-space rule, and give each mark the larger of the two. Place the partner's logo as the partner draws it, ampersand and all; write \"and\" for a partner's ampersand only in copy we type (Rule 01.24). Send the finished piece to the editor before it prints or posts."),
    ],
    "extras": [
        {"after_rule": "03.2", "specimen": "s-03-lockups", "label": "The eight lockups", "caption": "Seven of the eight lockups at true size, each with its job and its minimum on screen and in print; L6 follows in its own plate. L1, S1, L3 and L8 are masters; L4, L5 and L7 are built from the approved masters on our fifth edition's layouts."},
        {"after_rule": "03.2", "specimen": "s-03-l6", "label": "L6 at its minimum", "caption": "L6 at its 884 px minimum, wider than this column, so it scrolls on smaller screens. The wordmark and tagline sit centered on the strip, as the lockmark does. A page narrower than 884 px closes with the footer place (Rule 08.2). L6 leaves out a web address until ours is settled."},
        {"after_rule": "03.4", "specimen": "s-03-minimums", "label": "Minimum sizes", "caption": "The smallest size for every mark on screen and in print, and the mark to use below it."},
        {"after_rule": "03.8", "specimen": "s-03-misuse", "label": "Three more failures", "caption": "<strong>Fails Rules 03.1 and 03.5.</strong> Three more failures that slide and design apps make easy: a stretched mark, a drop shadow and a recolored ampersand."},
    ],
    "sources": [],
}

# =========================================================================================== 04 The Ampersand and the hinge
CH04 = {
    "number": "04", "anchor": "ampersand", "title": "The Ampersand and the hinge", "part": "Foundations",
    "instruction": "Use the ampersand once per composition to join a commitment to what it produces.",
    "opener": {"specimen": "s-04-opener", "caption": "Ampersand B at display size, and a hinge headline in its own frame, since a composition carries one ampersand moment (Rule 04.2). On a phone the headline sets in H3, so each phrase stays whole on its line."},
    "intro": [
        "The ampersand is the hinge of the brand. It joins an oath, the commitment a person or an office makes, to the action that keeps it, and in our headlines it joins a rule to its result. Ampersand B is our own drawing: one pen path that crosses itself at the waist, with a beak at the top right and a tail that lands on the baseline.",
        "This chapter covers B drawn alone and the places the hinge appears: the hinge headline, the hinge divider, the hinge diagram, the end mark that closes an article and the hinge-circle badge. It ends with the tiles for avatars and the app icon, and the large crop for covers.",
    ],
    "rules": [
        R("04.1", "Draw the ampersand from B's master for its size.",
          "B has three masters: the 16 px master for 16 to 23 px tall, the 24 px master for 24 to 47 px, and the display master from 48 px. Place the one whose range holds your height.",
          "B's strokes swell and thin at 1.74 to 1, so the glyph keeps its color beside the heavy capitals, and its waist crossing sits on the center line that the hinge diagram draws through its nodes. The small masters sit on the pixel grid: at 16 px, 66 percent of B's ink pixels are solid, where the glyph in our brand guide's fifth edition reached 48 percent.",
          "Our measurements, October 2026",
          "B at true size on one baseline: the display master at 160 and 48 px, the 24 px master and the 16 px master. Below, enlarged four times, the 16 px master as the browser draws it in pixels, and its outline on the pixel grid.",
          "Our fifth edition's ampersand, placed from an old file. It is Lora Bold's glyph, which anyone with Lora can type, and it has no beak.",
          tokens=["oa.color.identity.signature.onNewsprint"],
          specs=[S("Stroke contrast", "1.74 to 1, thickest over thinnest"), S("Weight", "Thick strokes at 0.91 of the wordmark's stem"),
                 S("Waist crossing", "On the glyph's vertical ink center"), S("Overshoot", "1.34 wordmark units above the cap line and below the baseline"),
                 S("Clear space, drawn alone", "1.0x of B's own cap height"), S("Color", "Signature red; White on Prussian", "oa.color.identity.signature.onNewsprint")],
          files=[A + "ampersand/20261028_Amp-B-Display-Master.svg", A + "ampersand/20261028_Amp-B-24px-Master.svg", A + "ampersand/20261028_Amp-B-16px-Master.svg"],
          related=["03", "17", "27"],
          builders="The ampersand files draw in <code>currentColor</code>, so set <code>color</code> to the surface's signature token. Our fifth edition's <code>OA_Amp_Master.svg</code> holds the Lora glyph; retire it from your templates."),
        R("04.2", "Give each composition one ampersand moment.",
          "A composition is one view: a screen, a card, a slide or a printed page. It carries one ampersand moment, a hinge headline, a freestanding B or a cropped B. The wordmark's own ampersand, the hinge divider and the end mark that closes an article do not count.",
          "The ampersand carries the brand's idea, and a reader takes in one hinge at a time. With two or three on a card, each says less and the eye has no place to land.",
          DJ,
          "A link card at 358 by 188 px, the size a phone feed shows it, with one hinge headline and the wordmark at its foot.",
          "The same card with a cropped B in the corner and a second B beside the wordmark. Three ampersands compete for one glance.",
          specs=[S("Moments", "A hinge headline, a freestanding B or a cropped B"), S("Not counted", "The wordmark's ampersand, the hinge divider and the end mark (Rule 04.6)")],
          related=["02", "05"],
          builders="When a template already holds a hinge headline, leave its ampersand slot out of every other layer."),
        R("04.3", "Join a rule to its result with a hinge headline.",
          "A hinge headline joins two noun phrases with B, as in \"The zoning code & the rent.\", and B takes the view's working red, the one red each view may spend, unless an error or a step the reader can take now already holds it. Then B takes the headline's ink. Rule 02.27 sets how to write one, and Rules 01.18 to 01.20 set when to use one.",
          "The headline names a mechanism in five or six words, and the red ampersand marks the joint. Rule 05.3 ranks an error first and the step a reader can take now second, so on an Act piece with a red button the step keeps the red.",
          "Rule 05.3, the red rule",
          "Three hinge headlines from Rule 02.27 at three sizes of the type scale, at true size: the title style at 56 px, the section style at 44 and H3 at 26. Each B comes from the master whose range holds that cap height.",
          "An Act card with a red ampersand in its headline and a red button below it, two working reds in one view.",
          corrective="The same card with B in Charcoal. The button keeps the red, so the step to take is the one red mark.",
          tokens=["oa.color.identity.signature.onNewsprint", "oa.color.action.ask.fill.onNewsprint"],
          specs=[S("Face", "Inter Tight 800, the headline's tracking"), S("B's height", "The type's cap height, 0.7275 of the font size"),
                 S("B's position", "Its baseline on the text's baseline, a word space on each side"),
                 S("Line break", "At the hinge, so B leads the second line and each phrase stays whole"),
                 S("Master", "16 px master for capitals 16 to 23 px tall, 24 px master from 24 to 47 px, display master from 48 px")],
          related=["02", "05", "06"],
          builders="Set B as an inline image of its master, joined to the second phrase with no-break spaces, so a line break falls at the hinge."),
        R("04.4", "Set a hinge divider before the step a reader can take.",
          "Set the divider between how a decision is made and what you can do about it. It centers B's 24 px master on a 1 px line as wide as the text it divides, with 12 px of clear line on each side of B. Line and B take the surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. It is never red.",
          "The divider marks the turn from how a decision is made to the step a reader can take, the same turn the ampersand makes in our name. In ink it stays quiet, and the view's one working red stays free for the step itself.",
          "Rule 05.3, the red rule; design judgment",
          "A divider at true size in an article, between how a bill leaves committee and what a reader can do, and below it the divider on all four surfaces.",
          "Our fifth edition's divider, with a red ampersand, above a red button. The divider spends the view's red, and two red marks compete for the step.",
          tokens=["oa.color.identity.hingeDivider.onNewsprint", "oa.color.identity.hingeDivider.onCharcoal", "oa.color.identity.hingeDivider.onPrussian"],
          specs=[S("Ampersand", "B's 24 px master at 24 px, at the center of the line"),
                 S("Line", "1 px, as wide as the text block it divides, in the same ink as B", "oa.color.identity.hingeDivider.onNewsprint"),
                 S("Space", "12 px of clear line on each side of B", "oa.space.150"),
                 S("Above and below", "24 px or more", "oa.space.300")],
          files=[A + "ampersand/20261028_Amp-B-24px-Master.svg"],
          related=["12", "02"],
          builders="Draw the line as two flexible halves with B between them, so B stays centered at any width. This guide draws the same divider between each rule and its correct use."),
        R("04.5", "Show the hinge diagram on its own, to explain the idea.",
          "The hinge diagram draws OATH and ACTION on a line with four nodes, B in a ring between them, two solid arcs running clockwise, and UNDERSTAND and IMPACT beneath. Draw its lines solid, give it words alone, and keep it out of any view that holds the wordmark, the badge or a figure with a key. Where a page needs a break, use the divider.",
          "The diagram teaches the brand's idea in one picture: a promise becomes action, and the result shapes the next promise. Its arcs are solid because our systems atlas draws a hypothesis as a dotted line and a connection graded plausible as a dashed one. It carries words alone, with no ID, sign, grade, delay or count, so no reader takes it for one of the atlas's loops.",
          DJ,
          "The display master at 600 px on Newsprint, and the compact master at 280 px on Newsprint and on Charcoal.",
          "The diagram with dashed arcs and a dashed ring, as an early mockup drew it. In the atlas's key a dashed line marks a connection graded plausible, so the brand's own idea reads as unproven.",
          tokens=["oa.color.identity.signature.onNewsprint", "oa.color.graphic.subtle.onNewsprint"],
          specs=[S("Display master", "From 533 px wide, labels at 13 px; 4.00 in in print"), S("Compact master", "From 245 px wide, no labels"),
                 S("Lines", "Solid; 3.5 units, arcs 2.8 units on the display master"), S("B", "In the ring, 1.25 cap heights, signature red"),
                 S("Below 245 px", "A hinge headline")],
          files=[A + "hinge/20261028_Hinge-Diagram-V2-Display-Master.svg", A + "hinge/20261028_Hinge-Diagram-V2-Compact-Master.svg"],
          related=["15", "05", "17"],
          builders="The diagram's lines read <code>--line</code>; leave it at Stone on light grounds and Newsprint on Charcoal. On Prussian, place the White file."),
        R("04.6", "End an article with B alone, and keep the badge for back covers and events.",
          "An article ends with ampersand B alone, half an em after its last word, in the text's ink. B stands at the text's cap height. On a 1x screen, which gives each CSS pixel one device pixel, B comes from its pixel fit for the text size, a copy redrawn on whole pixels, and sits on the baseline: in 17 px body text it is " + f"{_F17[0]} px tall" + ", with its top on the capitals' top row. On other screens, such as the 2x screens of phones and many laptops, and at other text sizes, B comes from its 16 px master, and only the curves at its top and foot run past the capitals: in 17 px text it is " + f"{_B17.get('b_px', 0):.1f} px tall beside capitals {_B17.get('capitals_px', 0):.1f} px tall" + ". The end mark is the one use of B that may stand under its 16 px minimum (Rule 03.4). The hinge-circle badge, B inside the hinge diagram's ring, keeps sizes from 48 px, on back covers and event materials. Keep the badge off anything about a candidate or a ballot measure, where a seal-like mark could read as an endorsement, and add no words or dates to it.",
          "At 16 px after a period, the badge's ring closes in on B and the mark reads as the registered trademark sign, which tells a reader something false about our mark. B alone stays legible at text size and spends no red, and it keeps the hinge at the end of every piece. Set at the capitals' height, it sits within the line it closes. On a 1x screen the smooth drawing blurred, with at most 45 percent of its ink pixels at full color, and it moved a row up or down with the line's position. The pixel fits draw every ink pixel at full color and keep B on the capitals' rows wherever the line falls. The pillar icons keep their fits on every screen under 2x instead (Rule 09.3), because a pillar master's thin line fills in there, while B's 16 px master keeps its shape on every screen above 1x. From 48 px the ring reads as a ring, and with no words on it the badge claims nothing more. Our fifth edition gave the reason: \"Seals imply an authority we do not claim.\"",
          "Design judgment and our measurements, approved by our founder and editor in November 2026",
          "The last lines of an article at true size, body text at 17 px on Newsprint and on Charcoal, then 15 px text on Newsprint: each paragraph ends on B at the text's cap height, in the text's ink, half an em after the period. Below, the badge at 96 px on the back of a 4 by 6 in event card.",
          "The badge at 16 px after an article's last word. Beside the registered trademark sign at the same size, its ring reads as the same mark.",
          tokens=["oa.color.text.primary.onNewsprint", "oa.color.identity.signature.onCharcoal"],
          specs=[S("End mark", "Ampersand B alone, half an em after the last word, held to it so B never starts a line"),
                 S("Ink", "The text's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian; never red", "oa.color.text.primary.onNewsprint"),
                 S("Size", "B at the text's cap height. On a 1x screen in 17 or 15 px text, B's pixel fit for that size, set on the baseline. On other screens and at other text sizes, B's band, its height less the overshoot above and below, on the text's capitals, so B stands 16/14 of the cap height tall, from the 16 px master until B reaches 24 px. In body text that puts B under its 16 px minimum, the end mark's exception (Rule 03.4)"),
                 S("At 17 px text", f"The body size. On a 1x screen, the 14 px pixel fit, {_F17[1]} by {_F17[0]} px: its top on the capitals' top row and its last row on theirs. On other screens: " + _end(17) + ", measured in Chromium"),
                 S("At 15 px text", f"On a 1x screen, the 12 px pixel fit, {_F15[1]} by {_F15[0]} px, on exactly the capitals' rows. On other screens: " + _end(15) + ", measured in Chromium"),
                 S("At 19 px text", _end(19)[:1].upper() + _end(19)[1:] + ", measured in Chromium. A screen may move B 1 px up or down as it rounds to whole pixels; its height stays the same"),
                 S("Badge", "From 48 px, its display master; 0.50 in in print. Back covers and event materials"),
                 S("Badge color", "Signature red, ring and B alike; White on Prussian", "oa.color.identity.signature.onCharcoal"),
                 S("Badge, never", "On an avatar or a favicon, or in a view with the wordmark or the hinge diagram"),
                 S("Print finishes", "A blind emboss on uncoated stock, matte red foil on Charcoal, or one color; chapter 25 sets the details")],
          files=[A + AMP_END[17][0], A + AMP_END[15][0], A + "ampersand/20261028_Amp-B-16px-Master.svg", A + "ampersand/20261028_Amp-B-24px-Master.svg",
                 A + "badge/20261028_Hinge-Badge-Display-Master.svg"],
          related=["12", "24", "25"],
          builders="Wrap the last word and B in one span that does not break, with <code>margin-left: 0.5em</code> on B, so B never starts a line alone. In 17 and 15 px text, put two drawings of B in that span and let a media query show one: the pixel fit for the text size, at its own size with <code>vertical-align: 0</code>, under <code>@media (resolution: 1dppx)</code>, and the 16 px master on every other screen, 1.25x and 1.5x screens included, where the fit's pixels fall between device pixels and its edges soften. At other text sizes, draw the 16 px master alone. Draw the 16 px master at 16/14 of the text's cap height, with the master's lowest row under the baseline. In Inter that is <code>height: 0.831em</code> and <code>vertical-align: -0.052em</code>, and those values hold for text up to 27 px. Both drawings use <code>currentColor</code>, so B takes the paragraph's ink. Place the badge from its display master only."),
        R("04.7", "Put B on a Charcoal tile for avatars and the app icon.",
          "Social avatars and the app icon show B alone on a Charcoal tile, a circle for avatars and a square for the app icon. The platform prints the account name beside an avatar, so the mark can be the ampersand alone. L8, the monogram, serves squares where the name must show, such as a tile in a partner's directory (Rule 03.7). Favicons use B's 16 px master with no tile.",
          "A feed often draws an avatar at 32 to 48 px. B's 24 px master still reads there, where any lettered mark would set its capitals under the 14 px floor. Charcoal is the default tile because it holds Pillar Red at 4.49 to 1, the strongest red of any approved surface, and stays visible on light and dark app themes.",
          "WCAG 2.2 SC 1.4.11; design judgment for the feed sizes",
          "Avatars and the app icon at true size: B on a Charcoal circle at 180, 64 and 32 px and on a Charcoal square at 180 and 64 px; the Newsprint, Prussian and one-color tiles; and the favicon on a light and a dark browser tab.",
          "A Newsprint circle in a white feed with no keyline. Its edge measures 1.41 to 1 against the page, so the tile fades and B floats.",
          tokens=["oa.component.avatar.tile", "oa.component.avatar.accent", "oa.component.appIcon.tile"],
          specs=[S("B's height", "58 percent of the tile"), S("Default tile", "Charcoal, for avatars and the app icon", "oa.component.avatar.tile"),
                 S("Light tile", "Newsprint with a 1 px Charcoal keyline, for dark app themes"), S("Prussian tile", "B in White"),
                 S("Upload", "A full-bleed square at 1080 px; platforms cut their own circle or corner"), S("Favicon", "B's 16 px master at 16 px, no tile")],
          files=[A + "ampersand/20261028_Amp-B-Display-Master.svg", A + "ampersand/20261028_Amp-B-16px-Master.svg"],
          related=["23", "03", "27"],
          builders="Export one 1080 px square and let each platform reduce it; check it at 48 and 32 px before you upload."),
        R("04.8", "Crop a large B off the bottom-right corner only.",
          "On a cover or a section opener, a large B may run off the bottom-right corner with 25 to 40 percent of its ink outside the frame. What stays inside reads as one letter, with no stroke cut off alone at the edge. It takes the surface's ink, never red, and stays clear of the text and out of the top-left corner, where reading starts.",
          "Readers start at the top left, so a crop there sits in the way of the title. At the bottom right it frames the page and points to the turn. Rule 05.3 gives red no job for a crop, so it takes the surface's ink, as the divider does.",
          "Design judgment; Rule 05.3",
          "A half-letter report cover at true size, 5.5 by 8.5 in, with B cropped off the bottom-right corner.",
          "The crop moved up behind the title. The title's letters cross B's strokes and lose their edge.",
          tokens=["oa.color.text.primary.onNewsprint"],
          specs=[S("Corner", "Bottom right"), S("Outside the frame", "25 to 40 percent of the glyph's ink"),
                 S("Inside the frame", "One piece: no stroke or fragment cut off from the letter at the trim"),
                 S("Color", "The surface's ink, never red: Charcoal on Newsprint, Newsprint on Charcoal, White on Prussian", "oa.color.text.primary.onNewsprint"),
                 S("Text", "Clear of B's strokes by at least the body text's line height")],
          files=[A + "ampersand/20261028_Amp-B-Display-Master.svg"],
          related=["12", "24", "25"],
          builders="Place the display master in a frame with its overflow hidden, and move it until 25 to 40 percent of its ink sits outside and every part left inside the trim joins the rest of the letter, with no fragment alone at the edge."),
    ],
    "extras": [],
    "sources": ["Oath & Action Brand Guide, fifth edition, chapter 04 The Ampersand, \"Seal and emboss\". Quoted in Rule 04.6."],
}

# =========================================================================================== 08 The lockmark
# DR-110 and D2-325 to D2-327: the lockmark keeps four fixed places and codes nothing. Rules renumber from 08.1; the old
# 08.3 to 08.9, the codes table, the stages sheet and the composer leave the chapter.
CH08 = {
    "number": "08", "anchor": "lockmark", "title": "The lockmark", "part": "Foundations",
    "instruction": "Draw the lockmark from its master, and place it only in its four fixed places.",
    "opener": {"specimen": "s-08-opener", "caption": "The lockmark in its four places at true size, each cropped to the part that holds it. Rule 08.2 sets the size for each place."},
    "intro": [
        "Democracy has a structure. The lockmark draws it as nine nodes joined by links, with the lever, a larger red node at bottom right, at the place where one change moves the rest. It signs our work in four fixed places: the masthead, the page header, the footer and the sign-off.",
        "Its drawing never changes, and it codes nothing. Chapter 11 sets how a tracker shows a bill's steps, and words name a series or a pillar.",
    ],
    "rules": [
        R("08.1", "Draw the lockmark from its master for its size, and keep its drawing fixed.",
          "The lockmark is a three by three grid of nodes joined around its edge and through its center, with the lever in signature red at bottom right. It has four masters. Place the 16 px master from 16 to 23 px and the 24 px master from 24 to 47 px. The 48 px master serves 48 px in the masthead and on covers and posters, and exactly twice that, 96 px, in a social card's sign-off. The display master, drawn for our brand guide's fifth edition, serves every other size from 49 px. Each master keeps the nine nodes in the same order, their links and the lever at bottom right. The 16, 24 and 48 px masters sit on the pixel grid and draw the nodes and the lever heavier than the display master, so the drawing holds at the sizes each one serves.",
          "At small sizes our fifth edition's single master lost its shape: at 24 px only 5 percent of its ink was solid, and at 16 px the lever became one pink pixel. The small masters set every node and link on whole pixels and draw the lever one size up, so it still reads as the place where one change moves the rest. At 48 px the display master covers 15 percent of its field with ink, against 42 percent for the 24 px master at 24 px, so the masthead and the sign-off take a 48 px master drawn the same way, which covers 22 percent. In the 24 and 48 px masters each node and the lever is one outline on the pixel grid, so between their sizes the nodes stay whole. The 48 px master serves 48 px and exactly twice that, 96 px, where each of its pixels becomes a block of 2 by 2. At any other size its edges fall between pixels and soften.",
          "Our measurements, October and November 2026; the 48 px master, the rebuilt 24 and 48 px files and the 96 px sign-off on social cards approved by our founder and editor in November 2026",
          "The lockmark's construction at 240 px, then its four masters at true size: the display master at 120 px beside the 48 px master drawn at 96 px for a social card's sign-off, then the 48, 24 and 16 px masters at their own sizes. Last, the 48 px master on Charcoal and on Prussian.",
          "Our fifth edition's master scaled to 16 px beside the 16 px master. Its nodes shrink to the width of a link and the lever turns into a single pink pixel.",
          tokens=["oa.color.identity.signature.onNewsprint", "oa.color.palette.stone"],
          specs=[S("Field", "123.5 units square"), S("Node centers", "11.75, 61.75 and 111.75 units on each axis"),
                 S("Nodes", "Radius 3.8 units"), S("Lever", "Radius 4.75 units, bottom right, signature red", "oa.color.identity.signature.onNewsprint"),
                 S("Links", "1 px Stone around the edge and through the center", "oa.color.palette.stone"),
                 S("16 px master", "Centers at 2.5, 7.5 and 12.5 px; 3 px nodes; 5 px lever"),
                 S("24 px master", "Centers at 3.5, 11.5 and 19.5 px; 5 px nodes; 7 px lever"),
                 S("48 px master", "Centers at 4.5, 23.5 and 42.5 px; 7 px nodes; 9 px lever; at 48 px, and at exactly 96 px in a social card's sign-off"),
                 S("Display master", "The field and node sizes above, at every size from 49 px except a social card's 96 px sign-off; its links stay 1 px wide at every size"), S("Print", "0.25 in at the smallest")],
          files=[A + LOCK["display"], A + LOCK[48], A + LOCK[24], A + LOCK[16]],
          related=["03", "05"],
          builders="The lockmark files read <code>--link</code> for the links and <code>--lever</code> for the lever. Leave the lever on the signature token; on Prussian, place the White file from <code>prussian/</code>. Place the 48 px master on whole pixels at exactly 48 px, the size its pixel grid was drawn for, or at exactly 96 px in a social card's sign-off. The 24 and 48 px files this rule lists draw each node and the lever as one outline; the earlier files, one rect per pixel row, stay in the folder only as the record. The display master keeps our fifth edition's drawing, with its links held at 1 px at every size."),
        R("08.2", "Place the lockmark only in its four places, once in a view.",
          "The lockmark signs four places: the masthead, the page header, the footer and the sign-off. Each place sets the lockmark's size, as this rule's specifications list them, and draws the master made for that size. A social card draws the 48 px master at exactly twice its size, so its nodes, links and lever still land on whole pixels. A view shows the lockmark once, so when a masthead and a footer share a view, the footer keeps it.",
          "A signature works by turning up in the same place at the same size, so a reader finds it without looking. Because each place draws a master on whole pixels, at the size it was made for or at exactly twice that, the four places read as one mark at the size each one sets. " + _thumb() + " Used as a bullet or scattered as decoration, the lockmark stops signing the page.",
          "Design judgment, approved by our founder and editor in November 2026",
          "The four places at true size, each with the size it sets: the masthead, a report's page header, two footers and the corner of a social card.",
          "The lockmark used as list bullets on a flyer, three lockmarks in one view, each one decoration.",
          tokens=["oa.color.identity.signature.onNewsprint"],
          specs=[S("Masthead", "L3 on screens from 48em, 768 px at the default text size, and in the email header, from its masthead master: the 24 px wordmark master, 13 px of space and the lockmark at 48 px from its 48 px master (Rule 03.6). In print, L3's print master, with the lockmark at the same 2.18 cap heights (Rule 03.2)"),
                 S("Page header", "24 px beside the section label on report and slide pages; 0.25 in in print"),
                 S("Footer", "24 px, then 12 px of space and the tagline, on one line at the footer's left edge, at the foot of a page, an email or a letter; 16 px at the right end of a chart's source line. L6, the strip that closes a report, carries it at L6's own proportion (Rule 03.2), and a page narrower than L6's 884 px closes with this footer"),
                 S("Sign-off", "Bottom right, inside the margin. On a social card, 96 px: the 48 px master drawn at exactly twice its size, so every node, every link and the lever land on whole pixels. On a cover or poster, 48 px from the 48 px master. In print, 0.50 in from the display master, since the 48 px master is drawn for a screen's pixel grid"),
                 S("Feed test", "A 1200 by 630 px card, reduced to 500 and 360 px wide, as a feed shows it, must keep a visible lockmark. On a light ground, such as Newsprint or White, each of its eight dark nodes keeps at least one near-black pixel (every color channel under 70), and the lever keeps at least four red pixels (red over 170, green and blue under 120). Reduce the card with Lanczos resampling, a common filter for shrinking images, and count each node's square plus 1 px on every side"),
                 S("Feed test, dark card", _feed_dark("rule")),
                 S("Feed test, our card", _feed() + ". " + _feed_dark("card")),
                 S("Once in a view", "When a masthead and a footer share one view, the footer keeps the lockmark and the masthead sets the wordmark alone"),
                 S("Favicon", "Never the lockmark: favicons use ampersand B's 16 px master (Rule 03.4)")],
          files=[A + L3["masthead"], A + L3["print"], A + LOCK[48], A + LOCK[24], A + LOCK[16], A + LOCK["display"]],
          related=["03", "07", "14", "23"],
          builders="Pick the master by the size each place sets in the specifications, and set it on whole pixels. On screen the masthead places L3's masthead master, which holds the lockmark already, and in print L3's print master. Run the feed test on every new template for a social card, on the file you will upload, before it ships. We run the test on the card in the identity proofs with a script of our own, and the asset package will carry a copy of that script that takes any card. Until then, ask the editor to run it on yours."),
        R("08.3", "Let the lockmark code nothing.",
          "Draw the lockmark the same in every place, with no node lit, dimmed, moved or added. It never shows how far a bill has moved, which series a piece belongs to or which pillar a piece serves. Each of those jobs has its own sign: chapter 11 numbers a bill's steps, the kicker names a series in words (Rule 01.21), and a pillar takes its icon with its word beside it.",
          "One drawing with one job is easy to learn. Our fifth edition used the same nine nodes to code a bill's stage, a series, a pillar and a kind of content, and a reader could not tell which code a grid carried, or whether the mark in the masthead meant anything at all. Numbers and words do those jobs better, because a reader can say \"step 4 of 6\" out loud and words survive gray print.",
          "Design judgment, approved by our founder and editor in November 2026",
          "A bill in a tracker list as Rule 11.5 draws it, at true size on a 358 px phone column: six numbered steps, the fourth marked as the step the bill is at, with the step in words beside them. No lockmark sits in the row.",
          "The same bill drawn on the lockmark's nine nodes, four of them filled to show progress. Nine nodes cannot count six steps, a reader has to decode the filled ones, and the mark that signs our pages changes from bill to bill.",
          specs=[S("Drawing", "The same in every place and from each of the four masters: nine nodes in the same three by three order, their links around the edge and through the center, and the red lever at bottom right. The 16, 24 and 48 px masters draw the nodes and the lever heavier than the display master, so only the weight changes (Rule 08.1)"),
                 S("A bill's progress", "Numbered steps with the step in words; Rule 11.5"),
                 S("A series", "Its name in words in the kicker; Rule 01.21"),
                 S("A pillar", "Its icon with its word beside it; chapter 09"),
                 S("Patterns", "None; the lockmark always appears whole")],
          related=["11", "01", "09"],
          builders="Take the grid out of any template that used it for a tracker, a series, a pillar or a state, and take each job from the chapter that now holds it. Chapter 11 sets the tracker's steps, their sizes and their words, and Rule 11.5 sets them in lists."),
    ],
    "extras": [],
    "sources": ["\"Democracy has a structure.\" is the lockmark's explanatory line, approved by Dustin Cathcart in October 2026."],
}

CHAPTERS = [CH03, CH04, CH08]

_PROSE = ("instruction", "title", "rule", "caption", "builders", "label", "value", "text", "basis")


def _smarten(o, key=None):
    if isinstance(o, dict):
        return {k: (_smarten(v, k) if k not in ("specimen", "token", "id", "files", "tokens", "related", "anchor", "number", "part", "after_rule") else v) for k, v in o.items()}
    if isinstance(o, list):
        return [_smarten(v, key) for v in o]
    if isinstance(o, str) and key in _PROSE + ("intro", "sources"):
        return smart(o)
    return o


CHAPTERS = [_smarten(c) for c in CHAPTERS]


def specimens_used(ch):
    out = []
    for r in ch["rules"]:
        for k in ("correct", "failure", "corrective"):
            if r.get(k):
                out.append(r[k]["specimen"])
    out += [x["specimen"] for x in ch.get("extras", [])]
    op = ch.get("opener")                 # stage C: a chapter's opener figure (D2-1134); from Gate 2's fix pass a
    if op:                                # specimen id or {"specimen", "caption"}
        out.append(op if isinstance(op, str) else op["specimen"])
    return out
