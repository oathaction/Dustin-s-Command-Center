"""Chapter content for 03 Identity, 04 The Ampersand and the hinge, and 08 The lockmark.

Apply pass, November 7, 2026: S1 replaces L2 (DR-113); today's width is the one in force (DR-115); avatars show B alone
(DR-116); the crop takes the surface's ink (DR-117); B alone ends an article and the badge keeps sizes from 48 px (DR-118);
chapter 08 becomes The lockmark, with four places and no codes (DR-110, D2-325 to D2-327).

Every word follows chapter 02's writing section (DR-73). Typographic quotes and apostrophes are set by smart() on the
prose fields, so the source stays easy to edit."""
import re

A = "work/build/assets/identity/"


def smart(t):
    if not isinstance(t, str):
        return t
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


def R(id_, title, rule, why, basis, correct, failure, *, tokens=(), specs=(), files=(), related=(), builders="", corrective=None):
    r = {"id": id_, "title": title, "rule": rule, "tokens": list(tokens), "why": {"text": why, "basis": basis},
         "correct": {"specimen": f"s-{id_.replace('.', '-')}-correct", "caption": correct},
         "failure": {"specimen": f"s-{id_.replace('.', '-')}-failure", "caption": failure},
         "specs": list(specs), "files": list(files), "related": list(related), "builders": builders}
    if corrective:
        r["corrective"] = {"specimen": f"s-{id_.replace('.', '-')}-corrective", "caption": corrective}
    return r


DJ = "Design judgment"

# =========================================================================================== 03 Identity
CH03 = {
    "number": "03", "anchor": "identity", "title": "Identity", "part": "Foundations",
    "instruction": "Pick the lockup that fits the surface and size, and give it room on every side.",
    "intro": [
        "The wordmark is our name drawn as one piece of artwork: OATH and ACTION in heavy capitals, joined by ampersand B, the red ampersand we drew for Oath & Action. A lockup is a fixed arrangement of the wordmark with another part, such as the tagline or the lockmark, the 3 by 3 grid of nodes that chapter 08 explains.",
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
                 S("L3 Horizontal with the lockmark", "The site and email masthead. Minimum 196 px wide; 1.55 in"),
                 S("L4 Monogram and tagline", "Document footers and small print. Minimum 304 px wide; 2.30 in"),
                 S("L5 Wordmark and tagline", "Covers, banners and partner placements where the tagline travels with the mark. Minimum 388 px wide; 2.90 in"),
                 S("L6 Editorial signature", "The strip that closes a report or a long page, with the tagline and the lockmark. Minimum 884 px wide; 6.60 in"),
                 S("L7 Section masthead", "Names the pillar a piece serves. Minimum 250 px wide with the longest pillar word; 1.90 in"),
                 S("L8 Monogram", "Small squares where the name must show, such as a tile in a partner's directory; never an avatar or a favicon. Minimum 48 px wide; 0.50 in")],
          files=[A + "lockups/20261107_S1-Stacked-Master.svg", A + "lockups/20261107_S1-Stacked-Master-24px.svg", A + "lockups/20261107_S1-Stacked-Master-16px.svg",
                 A + "lockups/20261028_L3-Horizontal-Master.svg", A + "lockups/20261028_L8-Monogram-Master.svg"],
          related=["04", "07", "27"],
          builders="Check the lockup's minimum before you place it. When the space falls under that minimum, switch to the lockup Rule 03.4's table names. S1 replaced the earlier stacked lockup, L2, in November 2026, so retire L2 from your templates; S1's files come in a Charcoal edition with its colors written in, for light grounds, and a White edition in <code>prussian/</code>. L4 to L7 have no master files of their own yet: build them from the wordmark, monogram and tagline masters on the layouts from our brand guide's fifth edition, as the sheet shows, or ask the editor for a file."),
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
          "On screen, no identity mark draws its capitals under 14 px, and no tagline inside a lockup sets under 13 px. In print, no capitals under 3 mm and no tagline under 7 pt. Under a lockup's minimum, switch to the lockup the table names.",
          "We drew and checked each master at its smallest size, where the wordmark keeps its six enclosed counters, the holes inside letters such as O and A, and the ampersand keeps its two. Our fifth edition scaled one drawing to every size, and at its own 120 px minimum a notch in the ampersand closed into a seventh enclosed shape.",
          "Our measurements, October 2026",
          "Every mark at its screen minimum, at true size. These are graphics drawn at their smallest allowed size, so the 13 px floor for text does not apply to the letters inside them.",
          "The display master scaled to 12 px tall for an email footer. Its capitals fall to 11 px, the white around the ampersand fills in and the name blurs. The 16 px master, 152 px wide, fits the same footer.",
          specs=[S("L1", "16 px tall, 152 px wide; 1.20 in in print"),
                 S("S1", "79 px wide, capitals 14 px; 0.65 in"),
                 S("L3", "196 px wide; 1.55 in"),
                 S("L8", "48 px wide; 0.50 in; never a favicon"),
                 S("Ampersand B and the lockmark", "16 px; 0.25 in"),
                 S("Hinge-circle badge", "48 px; 0.50 in (Rule 04.6)"),
                 S("L4 to L7", "Their minimums are in Rule 03.2's specifications"),
                 S("Favicon", "Ampersand B's 16 px master at 16 px")],
          files=[A + "20261028_Identity-Minimum-Sizes.json"],
          related=["06", "19", "27"],
          builders="Read the height you will draw, then pick the master whose range holds it. For the wordmark, the 16 px master runs from 16 to 19 px tall, the 24 px master from 20 to 39 px and the display master from 40 px. For ampersand B and the lockmark, the 16 px master runs from 16 to 23 px, the 24 px master from 24 to 47 px and the display master from 48 px (Rule 04.1). S1's masters follow its capitals: the 16 px master for capitals 14 to 17 px, the 24 px master for 18 to 36 px and the display master from 37 px. The badge starts at 48 px, from its display master. In print, set the width in inches from the table."),
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
          "The masthead is the bar across the top of every page and email. From 48em wide, 768 px at the default text size, it sets L3: the wordmark at left and the lockmark at its right, 2.4 cap heights tall. Under 48em, it sets L1 from the 24 px master beside the menu button. Email takes L3 as an image.",
          "The masthead is the one place every reader sees the mark, so it carries the fullest lockup the width allows. The lockmark needs about 34 px to show its nine nodes and its lever, and on a phone that room goes to the menu button.",
          DJ,
          "Three mastheads at true size: the site at 1440 px, the site on a 390 px phone and a 600 px email header, each from the master drawn for its height.",
          "L3 squeezed to 150 px across a phone bar. Its capitals fall to 12 px and the lockmark's nodes and links run together at 28 px.",
          specs=[S("Site, from 48em", "L3: the 24 px wordmark master, 13 px of space, the lockmark at 52 px; bar 80 px tall"),
                 S("Site, under 48em", "L1 from the 24 px master, 221 px wide; bar 56 px; menu button 44 px", "oa.size.target.touch"),
                 S("Email header", "L3 at 287 px in a 600 px header, sent as a PNG at twice size"),
                 S("Section masthead", "L7: L1, a hairline and the pillar's name in Inter 600 capitals, in the surface's ink")],
          files=[A + "lockups/20261028_L3-Horizontal-Master.svg", A + "wordmark/20261028_Wordmark-24px-Master.svg", A + "lockmark/20261028_Lockmark-24px-Master.svg"],
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
          "Design judgment; Dustin Cathcart's ruling on partners, November 6, 2026",
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
        {"after_rule": "03.2", "specimen": "s-03-l6", "label": "L6 at its minimum", "caption": "L6 at its 884 px minimum, wider than this column, so it scrolls on smaller screens. It leaves out a web address until ours is settled."},
        {"after_rule": "03.4", "specimen": "s-03-minimums", "label": "Minimum sizes", "caption": "The smallest size for every mark on screen and in print, and the mark to use below it."},
        {"after_rule": "03.8", "specimen": "s-03-misuse", "label": "Three more failures", "caption": "Three more failures that slide and design apps make easy: a stretched mark, a drop shadow and a recolored ampersand."},
    ],
    "sources": [],
}

# =========================================================================================== 04 The Ampersand and the hinge
CH04 = {
    "number": "04", "anchor": "ampersand", "title": "The Ampersand and the hinge", "part": "Foundations",
    "instruction": "Use the ampersand once per composition to join a commitment to what it produces.",
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
        R("04.3", "Join a rule to its result with a hinge headline, and give its ampersand the view's working red.",
          "A hinge headline joins two noun phrases with B, as in \"The zoning code & the rent.\" B takes the view's working red, the one red each view may spend, unless an error or a step the reader can take now already holds it. Then B takes the headline's ink. Rule 02.27 sets how to write one, and Rules 01.18 to 01.20 set when to use one.",
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
        R("04.4", "Set a hinge divider between how a decision is made and what you can do about it.",
          "The hinge divider centers B's 24 px master on a 1 px line as wide as the text it divides, with 12 px of clear line on each side of B. Line and B take the surface's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian. It is never red.",
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
          "The diagram teaches the brand's idea in one picture: a promise becomes action, and the result shapes the next promise. Its arcs are solid because our systems atlas draws a hypothesis as a dotted line and a plausible link as a dashed one. It carries words alone, with no ID, sign, grade, delay or count, so no reader takes it for one of the atlas's loops.",
          DJ,
          "The display master at 600 px on Newsprint, and the compact master at 280 px on Newsprint and on Charcoal.",
          "The diagram with dashed arcs and a dashed ring, as an early mockup drew it. In the atlas's key a dashed line means a plausible link, so the brand's own idea reads as unproven.",
          tokens=["oa.color.identity.signature.onNewsprint", "oa.color.graphic.subtle.onNewsprint"],
          specs=[S("Display master", "From 533 px wide, labels at 13 px; 4.00 in in print"), S("Compact master", "From 245 px wide, no labels"),
                 S("Lines", "Solid; 3.5 units, arcs 2.8 units on the display master"), S("B", "In the ring, 1.25 cap heights, signature red"),
                 S("Below 245 px", "A hinge headline")],
          files=[A + "hinge/20261028_Hinge-Diagram-V2-Display-Master.svg", A + "hinge/20261028_Hinge-Diagram-V2-Compact-Master.svg"],
          related=["15", "05", "17"],
          builders="The diagram's lines read <code>--line</code>; leave it at Stone on light grounds and Newsprint on Charcoal. On Prussian, place the White file."),
        R("04.6", "End an article with B alone, and keep the badge for back covers and events.",
          "An article ends with ampersand B alone after its last word, in the text's ink, as tall as the text's capitals, or 14 px tall where they are shorter. The hinge-circle badge, B inside the hinge diagram's ring, keeps sizes from 48 px, on back covers and event materials. Keep the badge off anything about a candidate or a ballot measure, where a seal-like mark could read as an endorsement, and add no words or dates to it.",
          "At 16 px after a period, the badge's ring closes in on B and the mark reads as the registered trademark sign, which tells a reader something false about our mark. B alone stays legible at text size and spends no red, and it keeps the hinge at the end of every piece. From 48 px the ring reads as a ring, and with no words on it the badge claims nothing more. Our fifth edition gave the reason: \"Seals imply an authority we do not claim.\"",
          "Design judgment, approved by our founder and editor in November 2026",
          "The last lines of an article at true size, body text at 17 px: the paragraph ends on B in Charcoal, the text's ink, from its 16 px master. Below, the badge at 96 px on the back of a 4 by 6 in event card.",
          "The badge at 16 px after an article's last word. Beside the registered trademark sign at the same size, its ring reads as the same mark.",
          tokens=["oa.color.text.primary.onNewsprint", "oa.color.identity.signature.onCharcoal"],
          specs=[S("End mark", "Ampersand B alone, after the last word with a no-break space before it"),
                 S("Ink", "The text's ink: Charcoal on Newsprint and White, Newsprint on Charcoal, White on Prussian; never red", "oa.color.text.primary.onNewsprint"),
                 S("Size", "As tall as the text's capitals, 0.7275 of the font size, from the master whose range holds that height; 14 px at the least (Rule 03.4)"),
                 S("At body size", "17 px text has capitals 12.4 px tall, under B's 14 px floor, so B takes its 16 px master at 16 px, its tail 1 px under the baseline"),
                 S("Badge", "From 48 px, its display master; 0.50 in in print. Back covers and event materials"),
                 S("Badge color", "Signature red, ring and B alike; White on Prussian", "oa.color.identity.signature.onCharcoal"),
                 S("Badge, never", "On an avatar or a favicon, or in a view with the wordmark or the hinge diagram"),
                 S("Print finishes", "A blind emboss on uncoated stock, matte red foil on Charcoal, or one color; chapter 25 sets the details")],
          files=[A + "ampersand/20261028_Amp-B-16px-Master.svg", A + "ampersand/20261028_Amp-B-24px-Master.svg", A + "badge/20261028_Hinge-Badge-Display-Master.svg"],
          related=["12", "24", "25"],
          builders="Set B inline after the last word with a no-break space before it, so it never starts a line alone. Draw it in <code>currentColor</code>, so it takes the paragraph's ink, from the master whose range holds the text's cap height, and set it 1 px under the baseline at the 16 px master, where its tail lands. Place the badge from its display master only."),
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
    "intro": [
        "Democracy has a structure. The lockmark draws it as nine nodes joined by links, with the lever, a larger red node at bottom right, at the place where one change moves the rest. It signs our work in four fixed places: the masthead, the page header, the footer and the sign-off.",
        "Its drawing never changes, and it codes nothing. Chapter 11 sets how a tracker shows a bill's steps, and words name a series or a pillar.",
    ],
    "rules": [
        R("08.1", "Draw the lockmark from its master for its size, and keep its drawing fixed.",
          "The lockmark is a three by three grid of nodes joined around its edge and through its center, with the lever in signature red at bottom right. Place the 16 px master from 16 to 23 px, the 24 px master from 24 to 47 px and the display master, drawn for our brand guide's fifth edition, from 48 px.",
          "At small sizes our fifth edition's single master lost its shape: at 24 px only 5 percent of its ink was solid, and at 16 px the lever became one pink pixel. The small masters set every node and link on whole pixels and draw the lever one size up, so it still reads as the place where one change moves the rest.",
          "Our measurements, October 2026",
          "The lockmark's construction at 240 px, then at true size at 96, 48, 24 and 16 px, and at 48 px on Charcoal and on Prussian.",
          "Our fifth edition's master scaled to 16 px beside the 16 px master. Its nodes shrink to the width of a link and the lever turns into a single pink pixel.",
          tokens=["oa.color.identity.signature.onNewsprint", "oa.color.palette.stone"],
          specs=[S("Field", "123.5 units square"), S("Node centers", "11.75, 61.75 and 111.75 units on each axis"),
                 S("Nodes", "Radius 3.8 units"), S("Lever", "Radius 4.75 units, bottom right, signature red", "oa.color.identity.signature.onNewsprint"),
                 S("Links", "1 px Stone around the edge and through the center", "oa.color.palette.stone"),
                 S("16 px master", "Centers at 2.5, 7.5 and 12.5 px; 3 px nodes; 5 px lever"),
                 S("24 px master", "Centers at 3.5, 11.5 and 19.5 px; 5 px nodes; 7 px lever"), S("Print", "0.25 in at the smallest")],
          files=[A + "lockmark/20261028_Lockmark-24px-Master.svg", A + "lockmark/20261028_Lockmark-16px-Master.svg"],
          related=["03", "05"],
          builders="The lockmark files read <code>--link</code> for the links and <code>--lever</code> for the lever. Leave the lever on the signature token; on Prussian, place the White file. Ask the editor for the display master, which keeps our fifth edition's drawing."),
        R("08.2", "Place the lockmark only in its four places, once in a view.",
          "The lockmark signs four places, at the size each one sets: the masthead, where L3 sets it beside the wordmark (Rule 03.6); the page header of a report or slide page, 24 px beside the section label; the footer, 24 px beside the tagline or 16 px beside a chart's source line; and the sign-off, 48 px from the display master at the bottom right of a social card, cover or poster. A view shows it once, so when a masthead and a footer share a view, the footer keeps it.",
          "A signature works by turning up in the same place at the same size, so a reader finds it without looking. Each size keeps the drawing crisp: the 24 and 16 px masters sit on whole pixels, and the sign-off takes the display master because the 24 px master turns soft when enlarged to 40 px. Used as a bullet or scattered as decoration, the lockmark stops signing the page.",
          "Design judgment, approved by our founder and editor in November 2026",
          "The four places at true size: a 768 px site masthead with L3; a report page header with the lockmark at 24 px beside the section label; a footer with the lockmark at 24 px beside the tagline, and a chart's footer with it at 16 px beside the source line; and the bottom-right corner of a 1080 px social card with the lockmark at 48 px inside the 72 px margin.",
          "The lockmark used as list bullets on a flyer, three lockmarks in one view, each one decoration.",
          tokens=["oa.color.identity.signature.onNewsprint"],
          specs=[S("Masthead", "L3 on screens from 48em, 768 px at the default text size, and in the email header: the 24 px wordmark master with the lockmark at 52 px from its display master (Rule 03.6)"),
                 S("Page header", "24 px beside the section label on report and slide pages; 0.25 in in print"),
                 S("Footer", "24 px beside the tagline at the foot of a page or an email; 16 px beside the source line in a chart's footer. L6, the strip that closes a report, carries it at L6's own proportion (Rule 03.2)"),
                 S("Sign-off", "48 px from the display master, bottom right of social cards, covers and posters, inside the margin; 0.50 in in print"),
                 S("Once in a view", "When a masthead and a footer share one view, the footer keeps the lockmark and the masthead sets the wordmark alone"),
                 S("Favicon", "Never the lockmark: favicons use ampersand B's 16 px master (Rule 03.4)")],
          files=[A + "lockmark/20261028_Lockmark-24px-Master.svg", A + "lockmark/20261028_Lockmark-16px-Master.svg"],
          related=["03", "07", "14", "23"],
          builders="Pick the master by the size the place sets: the 24 px master in page headers and footers, the 16 px master in a chart's footer, and the display master for the sign-off and inside L3. Ask the editor for the display master's file."),
        R("08.3", "Let the lockmark code nothing.",
          "Draw the lockmark the same in every place, with no node lit, dimmed, moved or added. It never shows how far a bill has moved, which series a piece belongs to or which pillar a piece serves. Each of those jobs has its own sign: chapter 11 numbers a bill's steps, the kicker names a series in words (Rule 01.21), and a pillar takes its icon with its word beside it.",
          "One drawing with one job is easy to learn. Our fifth edition used the same nine nodes to code a bill's stage, a series, a pillar and a kind of content, and a reader could not tell which code a grid carried, or whether the mark in the masthead meant anything at all. Numbers and words do those jobs better, because a reader can say \"step 4 of 6\" out loud and words survive gray print.",
          "Design judgment, approved by our founder and editor in November 2026",
          "A bill in a tracker list as Rule 11.5 draws it, at true size on a 358 px phone column: six numbered steps, the fourth marked as the step the bill is at, with the step in words beside them. No lockmark sits in the row.",
          "The same bill drawn on the lockmark's nine nodes, four of them filled to show progress. Nine nodes cannot count six steps, a reader has to decode the filled ones, and the mark that signs our pages changes from bill to bill.",
          specs=[S("Drawing", "The same in every place: nine nodes, their links and the red lever"),
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
    return out
