"""Chapter 04 The Ampersand and the hinge: specimens."""
from stage_a_identity_lib import (E, ID_DIR, AMP, BADGE, HINGE, LORA, WM, fragment, mark, wordmark, amp, illus, tag,
                                  svg_file, ink, ink2, hair, pal, tv, sig, strong, ground)
from stage_a_identity_s03 import rec as _rec, scroll

S = []


def spec(fn):
    S.append(fn)
    return fn


def rec(*a, **k):
    k.setdefault("chapter", "04")
    return _rec(*a, **k)


CAP = 0.7275   # Inter Tight cap height, in em


def hinge_amp(font_px, surface="newsprint", red=True, job="the one point the headline names"):
    """B set inside a line of Inter Tight 800 at a font size: its cap band on the text's cap band, its baseline on the
    baseline. The 16 and 24 px masters fill their box with 1 px of overshoot top and bottom (14 and 22 px capitals);
    the display master's box runs 1.34 units above the cap line and 1.35 below the baseline (cap height 100)."""
    cap = font_px * CAP
    if cap < 22:
        f, h, below = AMP[16], cap * 16 / 14, cap / 14
    elif cap < 46:
        f, h, below = AMP[24], cap * 24 / 22, cap / 22
    else:
        f, h, below = AMP["display"], cap * 1.0269, cap * 0.0135
    color = (tv("color-palette-pillar-red") if red else ink(surface))
    svg = svg_file(ID_DIR / f, h=h, decorative=True, style=f"color:{color};display:inline-block;vertical-align:{-below:.2f}px")
    if red:
        return f'<span class="oai-red" data-red="working" data-red-job="{E(job)}" style="line-height:0">{svg}</span>'
    return svg


def headline(text_a, text_b, font_px, surface="newsprint", red=True, extra_style="", br=False):
    """A hinge headline: two noun phrases joined by B, set in Inter Tight 800."""
    a = hinge_amp(font_px, surface, red)
    b = E(text_b).replace(" ", "&nbsp;")
    return (f'<p class="oai-disp" style="font-size:{font_px}px;line-height:1.08;letter-spacing:-.035em;text-wrap:balance;{extra_style}">'
            f'{E(text_a)}{"<br>" if br else " "}<span style="white-space:nowrap"><span role="img" aria-label="and" style="display:inline-block">{a}</span>&nbsp;{b}</span></p>')


def divider(surface="newsprint", width=None, red=False):
    """The hinge divider: a 1 px hairline broken by B's 24 px master at 24 px, 12 px of space each side.
    The ampersand takes the surface's ink (Rule 05.3, D1-22); red=True draws V5's red version for a failure case."""
    if red:
        b = f'<span class="oai-red" data-red="working" data-red-job="divider" data-failure="true" style="line-height:0">{svg_file(ID_DIR / AMP[24], h=24, decorative=True, style="color:" + tv("color-palette-pillar-red"))}</span>'
    else:
        b = svg_file(ID_DIR / AMP[24], h=24, decorative=True, style=f"color:{tv('color-identity-hinge-divider-on-' + surface)}")
    line = f'<span aria-hidden="true" style="flex:1;height:1px;background:{tv("color-identity-hinge-divider-on-" + surface) if not red else hair(surface)}"></span>'
    w = f"width:{width}px;" if width else ""
    return (f'<div role="separator" aria-label="Hinge divider" style="display:flex;align-items:center;gap:12px;{w}margin:24px 0">'
            f'{line}{b}{line}</div>')


def ask(label, surface="newsprint", red=True):
    if red:
        kl = f"box-shadow:0 0 0 1px {strong(surface)};" if surface in ("newsprint", "white") else ""
        return (f'<span class="oai-red" data-red="working" data-red-job="the step a reader can take now" style="display:inline-block;line-height:1.2">'
                f'<span style="display:inline-block;padding:12px 20px;background:{tv("color-action-ask-fill-on-" + surface)};color:{tv("color-action-ask-label-on-" + surface)};'
                f'font:700 19px/1.2 var(--oa-font-family-reading);{kl}">{E(label)}</span></span>')
    return (f'<span style="display:inline-block;padding:12px 20px;background:{tv("color-action-primary-fill-on-" + surface)};color:{tv("color-action-primary-label-on-" + surface)};'
            f'font:700 19px/1.2 var(--oa-font-family-reading)">{E(label)}</span>')


# ------------------------------------------------------------------------------------------- 04.1
@spec
def s_04_1_correct():
    def it(lbl, inner):
        return f'<div class="oai-cell">{inner}<span class="oai-tag">{E(lbl)}</span></div>'
    big = mark(AMP["display"], h=160, label="Ampersand B, display master, 160 px tall")
    # the 16 px master enlarged four times over its pixel grid
    grid = "".join(f'<line x1="{i}" x2="{i}" y1="0" y2="16" />' for i in range(15)) + "".join(f'<line x1="0" x2="14" y1="{j}" y2="{j}" />' for j in range(17))
    px = (f'<span style="position:relative;display:inline-block;width:56px;height:64px">'
          f'{mark(AMP[16], h=64, decorative=True)}'
          f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 14 16" width="56" height="64" aria-hidden="true" class="oai-svg" '
          f'style="position:absolute;left:0;top:0" stroke="{pal("stone")}" stroke-width="0.04">{grid}</svg></span>')
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-row">'
            + it("Display master, 160 px", big)
            + it("48 px, display master", mark(AMP["display"], h=48, label="Ampersand B at 48 px"))
            + it("24 px master", mark(AMP[24], h=24, label="Ampersand B, 24 px master"))
            + it("16 px master", mark(AMP[16], h=16, label="Ampersand B, 16 px master"))
            + f'<div class="oai-cell"><span role="img" aria-label="The 16 px master enlarged four times over its pixel grid">{px}</span><span class="oai-tag">16 px master, enlarged four times</span></div>'
            + '</div></div>')
    alt = ("Ampersand B in Pillar Red at true size: the display master 160 pixels tall, then at 48, 24 and 16 pixels, and the "
           "16 pixel master enlarged four times over its pixel grid, with its two open counters.")
    return rec("s-04-1-correct", "04.1", 700, alt, body, notes="The enlarged cell is labeled as enlarged; every other drawing is at true size.")


@spec
def s_04_1_failure():
    lora = mark(LORA, h=160, decorative=True)
    body = (f'<div class="oai-panel oai-s-newsprint"><div class="oai-row"><span role="img" aria-label="Failure case: V5 Lora Bold ampersand">{lora}</span>'
            '<span class="oai-tag">V5\'s ampersand, the Lora Bold glyph, 160 px</span></div></div>')
    alt = "Failure case: V5's ampersand, the unmodified Lora Bold glyph that any Lora user can type, in red at 160 pixels tall. It has no beak, and its strokes are more even than B's."
    return rec("s-04-1-failure", "04.1", 420, alt, body, notes="V5's glyph placed from the re-exported I1 record file, as an old Edition 05 file would place it.")


# ------------------------------------------------------------------------------------------- 04.2
def _card(extra_crop=False, extra_free=False):
    W, H = 480, 252
    crop = ""
    if extra_crop:
        crop = (f'<span aria-hidden="true" style="position:absolute;right:-60px;bottom:-70px">'
                f'{mark(AMP["display"], h=220, mode="ink", decorative=True)}</span>')
    free = ""
    if extra_free:
        free = f'<span style="margin-left:12px">{mark(AMP[16], h=16, decorative=True)}</span>'
    return (f'<div class="oai-s-newsprint" style="position:relative;overflow:hidden;width:{W}px;height:{H}px;padding:28px 32px;'
            f'border:1px solid {hair("newsprint")}">'
            f'{headline("The zoning code", "the rent.", 36, br=True)}'
            f'<p style="margin-top:12px;font-size:16px;max-width:30ch">Who decides what can be built near you, and when they vote next.</p>'
            f'<div style="position:absolute;left:32px;bottom:24px;display:flex;align-items:center">{wordmark(16, label="Oath & Action")}{free}</div>'
            f'{crop}</div>')


@spec
def s_04_2_correct():
    body = f'<div>{scroll(_card(), "Link card at feed size")}<p style="margin-top:8px">{illus()}</p></div>'
    alt = "A link card at 480 by 252 pixels, the size a feed shows it: the hinge headline The zoning code & the rent. with one red ampersand, a line under it, and the wordmark at the foot. Illustrative."
    return rec("s-04-2-correct", "04.2", 490, alt, body, illustrative=True,
               notes="Feed size: a 1200 by 630 file drawn at 480 px wide. The headline is chapter 02's W10 example (DR-75).")


@spec
def s_04_2_failure():
    card = _card(extra_crop=True, extra_free=True)
    body = (f'<div><div role="img" aria-label="Failure case: the same card with three ampersands. Illustrative.">{scroll(card, "Failure case at feed size")}</div>'
            f'<p style="margin-top:8px">{illus()}</p></div>')
    alt = "Failure case: the same card with a large cropped ampersand in the corner and a second small ampersand beside the wordmark, so three ampersands compete with the headline's. Illustrative."
    return rec("s-04-2-failure", "04.2", 490, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 04.3
@spec
def s_04_3_correct():
    body = ('<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:28px">'
            + headline("The rule", "the result.", 64)
            + headline("The budget", "the bill.", 40)
            + headline("The hearing", "the vote.", 24)
            + '<p class="oai-tag">Display, 64 px · Section, 40 px · Caption, 24 px</p></div></div>')
    alt = "Three hinge headlines at true size in heavy type, each joining two noun phrases with a red ampersand B: The rule & the result. at 64 pixels, The budget & the bill. at 40, The hearing & the vote. at 24."
    return rec("s-04-3-correct", "04.3", 700, alt, body,
               notes="V5's three hinge headlines, with B drawn from the master whose range holds each cap height (24 px master at 64 and 40 px type; 16 px master at 24 px).")


def _act_card(red_amp):
    return (f'<div class="oai-s-newsprint" style="width:480px;padding:28px 32px;border:1px solid {hair("newsprint")}">'
            f'<p class="oai-label" style="color:{ink2("newsprint")}">Act</p>'
            f'{headline("The bus map", "the vote.", 34, red=red_amp, extra_style="margin-top:10px")}'
            f'<p style="margin-top:12px;font-size:16px;max-width:34ch">The transit board votes on the new routes March 12. Comments close March 9.</p>'
            f'<div style="margin-top:20px">{ask("Send a comment")}</div></div>')


@spec
def s_04_3_failure():
    body = (f'<div role="img" aria-label="Failure case: an Act card with a red hinge ampersand and a red button. Illustrative.">{scroll(_act_card(True), "Failure case")}</div>'
            f'<p style="margin-top:8px">{illus()}</p>')
    alt = "Failure case: an Act card whose hinge headline The bus map & the vote. has a red ampersand above a red Send a comment button, two working reds in one view. Illustrative."
    return rec("s-04-3-failure", "04.3", 490, alt, body, illustrative=True)


@spec
def s_04_3_corrective():
    body = f'<div>{scroll(_act_card(False), "Corrected card")}<p style="margin-top:8px">{illus()}</p></div>'
    alt = "The same Act card corrected: the headline's ampersand in Charcoal and the Send a comment button in red, so the step to take is the one red mark. Illustrative."
    return rec("s-04-3-corrective", "04.3", 490, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 04.4
@spec
def s_04_4_correct():
    art = (f'<div class="oai-s-newsprint" style="max-width:560px;padding:28px 32px;border:1px solid {hair("newsprint")};font-size:17px;line-height:1.6">'
           f'<p>The committee reports the bill out by a vote of its members. The full House then has 30 days to take it up, or the bill waits for the next session.</p>'
           f'{divider("newsprint")}'
           f'<p><b>What you can do.</b> The committee takes written testimony until March 27. Send it to the committee clerk, and include your town.</p>'
           f'<p style="margin-top:12px">{illus()}</p></div>')
    strips = "".join(
        f'<div class="oai-cell"><div class="oai-s-{s}" style="width:300px;padding:4px 20px">{divider(s)}</div><span class="oai-tag">{n}</span></div>'
        for s, n in (("newsprint", "Charcoal on Newsprint"), ("white", "Charcoal on White"), ("charcoal", "Newsprint on Charcoal"), ("prussian", "White on Prussian")))
    body = f'<div class="oai-stack" style="gap:24px">{art}<div class="oai-row">{strips}</div></div>'
    alt = ("An article passage at true size: a paragraph on how a bill leaves committee, then the hinge divider, a thin line "
           "broken by a small ampersand in Charcoal, then What you can do. with the testimony deadline. Illustrative. Below, "
           "the divider on Newsprint, White, Charcoal and Prussian, its ampersand in each surface's ink.")
    return rec("s-04-4-correct", "04.4", 640, alt, body, illustrative=True,
               notes="Divider: 1 px hairline token, B's 24 px master at 24 px in the hinge-divider token, 12 px gaps, 24 px above and below.")


@spec
def s_04_4_failure():
    art = (f'<div class="oai-s-newsprint" style="width:480px;padding:28px 32px;border:1px solid {hair("newsprint")};font-size:17px;line-height:1.6">'
           f'<p>The committee reports the bill out by a vote of its members.</p>{divider("newsprint", red=True)}'
           f'<p><b>What you can do.</b> Written testimony is open until March 27.</p><div style="margin-top:16px">{ask("Send testimony")}</div></div>')
    body = (f'<div role="img" aria-label="Failure case: a red divider above a red button. Illustrative.">{scroll(art, "Failure case")}</div>'
            f'<p style="margin-top:8px">{illus()}</p>')
    alt = "Failure case: V5's hinge divider with a red ampersand, above a red Send testimony button, so two red marks compete for the step. Illustrative."
    return rec("s-04-4-failure", "04.4", 490, alt, body, illustrative=True)


# ------------------------------------------------------------------------------------------- 04.5
@spec
def s_04_5_correct():
    disp = mark(HINGE["display"], w=600, label="Hinge diagram V2, display master: OATH and ACTION on a line with four nodes, ampersand B in a ring, two solid clockwise arcs, UNDERSTAND and IMPACT beneath")
    comp = mark(HINGE["compact"], w=280, label="Hinge diagram V2, compact master")
    compc = mark(HINGE["compact"], w=280, surface="charcoal", label="Hinge diagram V2, compact master on Charcoal")
    body = ('<div class="oai-stack" style="gap:16px">'
            f'<div class="oai-panel oai-s-newsprint">{scroll(disp, "Hinge diagram, display master at 600 px; scroll sideways on a narrow screen")}<p class="oai-tag" style="margin-top:12px">Display master, 600 px</p></div>'
            f'<div class="oai-row top"><div class="oai-panel oai-s-newsprint">{comp}<p class="oai-tag" style="margin-top:12px">Compact master, 280 px</p></div>'
            f'<div class="oai-panel oai-s-charcoal">{compc}<p class="oai-tag" style="margin-top:12px">Compact master on Charcoal</p></div></div></div>')
    alt = ("The hinge diagram at true size: the display master 600 pixels wide on Newsprint, with OATH and ACTION on a line "
           "through four nodes, a red ampersand B in a ring between them, two solid arcs running clockwise and the words "
           "UNDERSTAND and IMPACT beneath; and the compact master at 280 pixels on Newsprint and on Charcoal.")
    return rec("s-04-5-correct", "04.5", 650, alt, body)


@spec
def s_04_5_failure():
    css = ".oai-dash path[stroke],.oai-dash circle[stroke]{stroke-dasharray:9 5}"
    d = mark(HINGE["display"], w=600, decorative=True, cls="oai-dash")
    body = (f'<div class="oai-panel oai-s-newsprint"><div role="img" aria-label="Failure case: the hinge diagram with dashed arcs">'
            f'{scroll(d, "Failure case at 600 px")}</div></div>')
    alt = "Failure case: the hinge diagram redrawn with dashed arcs and a dashed ring. In the atlas's key a dashed line means a plausible link, so the diagram reads as a guess."
    return rec("s-04-5-failure", "04.5", 650, alt, body, css=css,
               notes="The master is placed unchanged; a dash pattern applied to its strokes at placement shows the failure.")


# ------------------------------------------------------------------------------------------- 04.6
@spec
def s_04_6_correct():
    end = (f'<div class="oai-s-newsprint" style="max-width:520px;padding:24px 32px;border:1px solid {hair("newsprint")};font-size:17px;line-height:1.6">'
           f'<p>The board meets again on April 2, and the agenda posts a week before. We will add the vote to the tracker when the minutes are published.'
           f'&nbsp;<span style="display:inline-block;vertical-align:-3px">{mark(BADGE[16], h=16, label="End mark: the hinge-circle badge")}</span></p>'
           f'<p style="margin-top:12px">{illus()}</p></div>')
    card = (f'<div class="oai-s-charcoal" style="width:384px;height:576px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px">'
            f'{mark(BADGE["display"], h=96, surface="charcoal", label="Hinge-circle badge, 96 px, on the back of an event card")}</div>')
    body = (f'<div class="oai-stack" style="gap:32px">{end}<div class="oai-cell">{scroll(card, "Event card back, 4 by 6 inches at true size")}'
            f'<span class="oai-tag">Back of a 4 by 6 in event card, true size</span></div></div>')
    alt = ("The badge, a red ampersand B inside a thin ring, at true size: at 16 pixels as the end mark after an article's last "
           "sentence, and at 96 pixels centered on the Charcoal back of a 4 by 6 inch event card. Illustrative article text.")
    return rec("s-04-6-correct", "04.6", 560, alt, body, illustrative=True)


@spec
def s_04_6_failure():
    r = 92
    ring = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 240 240" width="240" height="240" aria-hidden="true" class="oai-svg" style="position:absolute;left:0;top:0">'
            f'<defs><path id="oai-seal-arc" d="M120 120m-{r},0a{r},{r} 0 1,1 {2 * r},0a{r},{r} 0 1,1 -{2 * r},0"/></defs>'
            f'<circle cx="120" cy="120" r="116" fill="none" stroke="{ink("newsprint")}" stroke-width="2"/>'
            f'<text font-family="Inter, Arial, sans-serif" font-weight="700" font-size="17" letter-spacing="3" fill="{ink("newsprint")}">'
            f'<textPath href="#oai-seal-arc">OATH &amp; ACTION · OFFICIAL SEAL · OATH &amp; ACTION · OFFICIAL SEAL ·</textPath></text></svg>')
    seal = (f'<span role="img" aria-label="Failure case: the badge inside a ring of words reading Oath and Action, official seal" '
            f'style="position:relative;display:inline-block;width:240px;height:240px">{ring}'
            f'<span style="position:absolute;left:60px;top:60px">{mark(BADGE["display"], h=120, decorative=True)}</span></span>')
    body = f'<div class="oai-panel oai-s-newsprint">{seal}</div>'
    alt = "Failure case: the badge set inside an outer ring of words, OATH & ACTION, OFFICIAL SEAL, repeated around the circle, turning it into a seal."
    return rec("s-04-6-failure", "04.6", 300, alt, body)


# ------------------------------------------------------------------------------------------- 04.7
def _tile(size, shape="circle", surface="charcoal", keyline=False, bg=None):
    b = 0.58 * size
    if surface == "charcoal":
        fill, mk = tv("component-avatar-tile"), mark(AMP["display"] if b >= 48 else (AMP[24] if b >= 24 else AMP[16]), h=b, surface="charcoal", decorative=True)
    elif surface == "prussian":
        fill, mk = ground("prussian"), mark(AMP["display"] if b >= 48 else (AMP[24] if b >= 24 else AMP[16]), h=b, surface="prussian", decorative=True)
    elif surface == "mono":
        fill, mk = ground("white"), mark(AMP["display"] if b >= 48 else (AMP[24] if b >= 24 else AMP[16]), h=b, mode="mono", decorative=True)
    else:
        fill, mk = ground(surface), mark(AMP["display"] if b >= 48 else (AMP[24] if b >= 24 else AMP[16]), h=b, surface=surface, decorative=True)
    rad = "50%" if shape == "circle" else f"{0.2237 * size:.1f}px"
    kl = f"box-shadow:inset 0 0 0 1px {pal('charcoal')};" if keyline else ""
    return (f'<span style="display:inline-flex;align-items:center;justify-content:center;width:{size}px;height:{size}px;border-radius:{rad};'
            f'background:{fill};{kl}flex:none">{mk}</span>')


@spec
def s_04_7_correct():
    def it(lbl, inner):
        return f'<div class="oai-cell">{inner}<span class="oai-tag">{E(lbl)}</span></div>'
    row1 = (it("Avatar, 180 px", f'<span role="img" aria-label="Avatar: ampersand B on a Charcoal circle, 180 px">{_tile(180)}</span>')
            + it("64 px", f'<span role="img" aria-label="Avatar at 64 px">{_tile(64)}</span>')
            + it("32 px", f'<span role="img" aria-label="Avatar at 32 px">{_tile(32)}</span>')
            + it("App icon, 180 px", f'<span role="img" aria-label="App icon: ampersand B on a Charcoal rounded square, 180 px">{_tile(180, "square")}</span>')
            + it("64 px", f'<span role="img" aria-label="App icon at 64 px">{_tile(64, "square")}</span>'))
    fav = (f'<span style="display:inline-flex;gap:8px;align-items:center;padding:8px 12px;background:{ground("white")};border:1px solid {hair("white")}">'
           f'{mark(AMP[16], h=16, surface="white", label="Favicon: ampersand B, 16 px master")}<span style="font-size:14px">Oath &amp; Action</span></span>'
           f'<span style="display:inline-flex;gap:8px;align-items:center;padding:8px 12px;background:{ground("charcoal")};color:{ink("charcoal")}">'
           f'{mark(AMP[16], h=16, surface="charcoal", label="Favicon on a dark browser tab")}<span style="font-size:14px">Oath &amp; Action</span></span>')
    row2 = (it("Newsprint with a 1 px Charcoal keyline, for dark app themes", f'<span role="img" aria-label="Newsprint avatar with keyline">{_tile(64, surface="newsprint", keyline=True)}</span>')
            + it("Prussian, B in White", f'<span role="img" aria-label="Prussian avatar with a White ampersand">{_tile(64, surface="prussian")}</span>')
            + it("Mono, for one-color print", f'<span role="img" aria-label="One-color avatar">{_tile(64, surface="mono", keyline=True)}</span>')
            + it("Favicon, 16 px master, light and dark tabs", f'<div class="oai-row" style="gap:8px">{fav}</div>'))
    body = f'<div class="oai-panel oai-s-newsprint"><div class="oai-stack" style="gap:32px"><div class="oai-row">{row1}</div><div class="oai-row">{row2}</div></div></div>'
    alt = ("Avatars and app icons at true size: ampersand B in red on a Charcoal circle at 180, 64 and 32 pixels and on a "
           "Charcoal rounded square at 180 and 64; then a Newsprint circle with a thin Charcoal keyline, a Prussian circle with "
           "a White ampersand, a one-color circle, and the 16 pixel ampersand as a favicon on a light and a dark browser tab.")
    return rec("s-04-7-correct", "04.7", 700, alt, body,
               notes="B at 58 percent of the tile (V5's container proportion). The rounded square's corner is a placeholder radius; iOS and Android cut their own mask from a full-bleed square upload.")


@spec
def s_04_7_failure():
    feed = (f'<div class="oai-s-white" style="width:420px;padding:16px;display:flex;gap:12px;align-items:center;border:1px solid {hair("white")}">'
            f'{_tile(48, surface="newsprint")}<div><p style="font-weight:700">Oath &amp; Action</p><p style="font-size:14px;color:{ink2("white")}">Posted a link</p></div></div>')
    body = f'<div role="img" aria-label="Failure case: a Newsprint avatar with no keyline on a white feed">{scroll(feed, "Failure case")}</div>'
    alt = "Failure case: a Newsprint circle avatar with no keyline in a white feed. The circle's edge measures 1.41 to 1 against the page and fades, so the ampersand floats without its tile."
    return rec("s-04-7-failure", "04.7", 440, alt, body)


# ------------------------------------------------------------------------------------------- 04.8
def _cover(crop_ok=True):
    W, H = 528, 816
    if crop_ok:
        crop = (f'<span aria-hidden="true" style="position:absolute;right:-120px;bottom:-110px">'
                f'{mark(AMP["display"], h=440, mode="ink", decorative=True)}</span>')
    else:
        crop = (f'<span aria-hidden="true" style="position:absolute;left:-40px;top:70px">'
                f'{mark(AMP["display"], h=480, mode="ink", decorative=True)}</span>')
    return (f'<div class="oai-s-newsprint" style="position:relative;overflow:hidden;width:{W}px;height:{H}px;padding:48px;border:1px solid {hair("newsprint")}">'
            f'{crop}<div style="position:relative">{wordmark(18, label="Oath & Action")}'
            f'<p class="oai-label" style="margin-top:64px;color:{ink2("newsprint")}">Report</p>'
            f'<p class="oai-disp" style="font-size:46px;margin-top:12px;max-width:10ch;line-height:1.02;text-wrap:balance">How a county budget gets written</p>'
            f'<p style="margin-top:16px;font-size:17px;max-width:24ch">Who drafts it, who can change it and when the public can speak.</p></div></div>')


@spec
def s_04_8_correct():
    body = (f'<div class="oai-cell">{scroll(_cover(True), "Report cover at true size, 5.5 by 8.5 inches; scroll on a narrow screen")}'
            f'<p>{illus()}</p></div>')
    alt = ("A half-letter report cover at true size, 5.5 by 8.5 inches, on Newsprint: the wordmark and the title How a county "
           "budget gets written at top left, and a very large Charcoal ampersand B running off the bottom-right corner. Illustrative.")
    return rec("s-04-8-correct", "04.8", 540, alt, body, illustrative=True,
               notes="B display master at 440 px tall in the surface's ink; about 30 percent of it runs past the right and bottom edges.")


@spec
def s_04_8_failure():
    body = (f'<div class="oai-cell"><div role="img" aria-label="Failure case: the cropped ampersand moved up behind the title. Illustrative.">'
            f'{scroll(_cover(False), "Failure case at true size")}</div><p>{illus()}</p></div>')
    alt = "Failure case: the same cover with the large ampersand moved up behind the title, so the title's letters cross its strokes. Illustrative."
    return rec("s-04-8-failure", "04.8", 540, alt, body, illustrative=True)
