"""Concept 2, Moving part, stage 2: holders, the 1024 px app tile and the eight contexts.

Run after icons_r2_moving_masters.py: python3 -I icons_r2_moving_assets.py
Writes, in work/boards/phase-2/icons-r2/moving-part/:
  holders/20261028_Moving-Part-Holder-<Shape>-<Color>.svg        the nine empty holders
  holders/20261028_Moving-Part-<Icon>-<Shape>-<Color>-<px>.svg   each icon in each holder at 40 and 96 px
  app-tile/20261028_Moving-Part-App-Tile-1024-Glyph-<pct>.svg    the 1024 px tile at 56, 62 and 66 percent
  app-tile/20261028_Moving-Part-App-Tile-1024.svg                the chosen tile (GLYPH below)
  app-tile/20261028_Moving-Part-App-Tile-Glyph-Test.png          the three scales at 180, 60 and 29 px
  context/20261028_Moving-Part-Context-<N>-<Name>.png            the eight contexts, rendered by Chromium
                                                                  at device scale 1 (the HTML sources go
                                                                  to the scratchpad)
Holder geometry is round one's (icons_common.py, read only): the 24-unit field is 60 percent of the
side and the 20-unit live area half of it. A 40 px holder takes the 24 px master at 1:1; larger
holders take the display master. The rounded square is round one's superellipse, exponent 5.
"""
import html as H
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_common as RC  # noqa: E402  (round one, read only)
import icons_r2_moving_common as C  # noqa: E402
import icons_r2_moving_draw as D  # noqa: E402
from icons_geom import d_of  # noqa: E402

SHAPES = ["Square", "Rounded-Square", "Circle"]
TILE = {"Charcoal": (C.CHAR, "Newsprint-Red"), "Newsprint": (C.NEWS, "Charcoal-Red"), "Prussian": (C.PRUS, "White")}
GLYPHS = [56, 62, 66]
GLYPH = 66            # the app tile's glyph scale, picked by eye on the test sheet (see the notes)
APP_ICON = "act"
AVATAR_ICON = "act"
AVATAR_GLYPH = 56     # the largest live area whose corners stay inside the circle's safe radius (0.40 of the diameter)


def holder_file(shape, color):
    return C.HOLDERS / f"{C.DATE}_Moving-Part-Holder-{shape}-{color}.svg"


def tile_file(name, shape, color, px):
    return C.HOLDERS / f"{C.DATE}_Moving-Part-{D.FILE_NAME[name]}-{shape}-{color}-{px}.svg"


def app_file(pct=None):
    return C.APP / (f"{C.DATE}_Moving-Part-App-Tile-1024-Glyph-{pct}.svg" if pct else f"{C.DATE}_Moving-Part-App-Tile-1024.svg")


def holder_d(shape, size):
    return d_of(RC.holder_path(shape, size))


def tile_svg(name, shape, color, px, open_=False, title=None, glyph=None):
    """One icon in a holder, as an SVG px wide. glyph, when given, sets the live area's share of the
    side (the app tile); otherwise round one's in-product geometry applies."""
    fill, cw = TILE[color]
    size = C.best(px) if px < 48 else "Display"
    if px == 40:
        size = "24px"
    m = C.load(name, size, open_)
    U = C.UNITS[size]
    if glyph:
        sc = px * glyph / 100 / (U * 20 / 24)
        off = px / 2 - U / 2 * sc
    else:
        sc = px * RC.FIELD_FRACTION / U
        off = px * (1 - RC.FIELD_FRACTION) / 2
    t = f"<title>{title}</title>" if title else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{px}" height="{px}" viewBox="0 0 {px} {px}">{t}'
            f'<path id="holder" d="{holder_d(shape, px)}" fill="{fill}"/>{C.inner(m, U, cw, sc, off, off)}</svg>')


def write_holders():
    C.HOLDERS.mkdir(parents=True, exist_ok=True)
    for shape in SHAPES:
        for color, (fill, cw) in TILE.items():
            holder_file(shape, color).write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" width="96" height="96" viewBox="0 0 96 96"><title>{shape.replace("-", " ")} holder, {color}. '
                f'Round one geometry. Concept 2 Moving part, October 28, 2026. Proposal only.</title><path id="holder" d="{holder_d(shape, 96)}" fill="{fill}"/></svg>')
            for name in D.ICONS:
                for px in (40, 96):
                    tile_file(name, shape, color, px).write_text(tile_svg(name, shape, color, px,
                                                                          title=f"{D.LABELS[name]} in a {shape.replace('-', ' ').lower()} holder, {color}, {px} px. Concept 2 Moving part. Proposal only."))


def write_app_tiles():
    C.APP.mkdir(parents=True, exist_ok=True)
    for pct in GLYPHS:
        app_file(pct).write_text(tile_svg(APP_ICON, "Rounded-Square", "Charcoal", 1024, glyph=pct,
                                          title=f"Act as a 1024 px app tile, glyph live area at {pct} percent of the side. Superellipse, exponent 5. Concept 2 Moving part. Proposal only."))
    app_file().write_text(tile_svg(APP_ICON, "Rounded-Square", "Charcoal", 1024, glyph=GLYPH,
                                   title=f"Act as a 1024 px app tile, glyph live area at {GLYPH} percent of the side, chosen by eye. Concept 2 Moving part. Proposal only."))
    # the test sheet: each scale at 180, 60 and 29 px on a light and a dark wallpaper
    rows = []
    for wall, bg, fg in (("light", "linear-gradient(160deg,#EDEAE4,#C9C5BC)", C.CHAR), ("dark", "linear-gradient(160deg,#2B2F36,#0B0C0E)", C.NEWS)):
        cells = []
        for pct in GLYPHS:
            imgs = "".join(f'<img src="file://{app_file(pct)}" width="{s}" height="{s}" style="display:block">' for s in (180, 60, 29))
            cells.append(f'<div class="c"><div class="t">{imgs}</div><div class="l">{pct} percent</div></div>')
        rows.append(f'<div class="w" style="background:{bg};color:{fg}">{"".join(cells)}</div>')
    page = (f'<!doctype html><html><head><meta charset="utf-8"><style>{C.font_css()}html{{background:#DCD9D2}}body{{margin:0;width:1180px;font:600 15px/1.3 Inter,sans-serif}}'
            f'.w{{display:flex;gap:48px;padding:32px 40px}}.c{{display:grid;gap:10px;justify-items:center}}'
            f'.t{{display:flex;gap:28px;align-items:flex-end}}.l{{font-variant-numeric:tabular-nums}}</style></head><body>{"".join(rows)}</body></html>')
    p = C.SCRATCH / "app-test.html"
    p.write_text(page)
    shoot(p, C.APP / f"{C.DATE}_Moving-Part-App-Tile-Glyph-Test.png", 1180)


def shoot(page, out, width, scale=1):
    subprocess.run(["node", str(C.SHOT_JS), str(page), str(out), str(width), str(scale)], check=True)


def img(name, px, cw="Charcoal-Red", open_=False, alt=""):
    size = C.best(px)
    return f'<img src="file://{C.variant_file(name, size, cw, open_)}" width="{px}" height="{px}" alt="{H.escape(alt)}" style="display:block">'


BASE_CSS = """
body{margin:0;background:#DCD9D2;color:#121212;font:400 15px/1.45 Inter,sans-serif}
.rowwrap{padding:20px 24px}
.menu{display:flex;gap:28px;align-items:center;padding:14px 20px}
.menu .it{display:flex;gap:8px;align-items:center;font:500 15px/1 Inter,sans-serif;letter-spacing:-.005em}
.menu .it.cur{font-weight:700}
.menu.dark{background:#121212;color:#DCD9D2}
.menu.pru{background:#1F2D5A;color:#FFFFFF}
.lab{font:700 12px/1 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#45494F;padding:0 20px 6px}
.dark .lab,.pru .lab{color:inherit}
"""


def context_pages():
    pages = {}
    # 1. pillar menu row on Newsprint, Charcoal and Prussian, Track current
    def menu(kind):
        pillars = ["explain", "track", "connect", "act"]
        items = []
        for n in pillars:
            cur = n == "track"
            if kind == "news":
                cw = "Charcoal-Red-Keyline" if cur else "Charcoal"
            elif kind == "dark":
                cw = "Newsprint-Red" if cur else "Newsprint"
            else:
                cw = "White"
            items.append(f'<span class="it{" cur" if cur else ""}">{img(n, 24, cw, open_=cur)}{D.LABELS[n]}</span>')
        cls = {"news": "", "dark": " dark", "pru": " pru"}[kind]
        return f'<div class="menu{cls}">{"".join(items)}</div>'
    pages["1-Menu-Row"] = (f'<div style="width:560px">{menu("news")}{menu("dark")}{menu("pru")}</div>', 560)

    # 2. topic list, all ten at 24 px with labels, Campaign money current
    gloss = {"explain": "How a decision gets made", "track": "Bills on the move this week", "connect": "People and the officials who serve them",
             "act": "Ways to take part", "ballot": "Ranked ballots, step by step", "bill": "Read the text of a bill",
             "testify": "Speak at a public hearing", "housing": "Rent, zoning and building", "money": "Who pays for a campaign",
             "loop": "Loops in the systems atlas"}
    rows = []
    for n in D.ICONS:
        cur = n == "money"
        rows.append(f'<div class="tr{" cur" if cur else ""}">{img(n, 24, "Charcoal-Red-Keyline" if cur else "Charcoal", open_=cur)}'
                    f'<span><b>{D.LABELS[n]}</b><small>{gloss[n]}</small></span></div>')
    pages["2-Topic-List"] = (f'<style>.tl{{width:380px;padding:16px 20px}}.tr{{display:flex;gap:12px;align-items:center;padding:8px 10px;border-bottom:1px solid #B9B5AD}}'
                             f'.tr b{{display:block;font:500 15px/1.25 Inter,sans-serif}}.tr.cur b{{font-weight:700}}.tr small{{display:block;font:400 13px/1.3 Inter,sans-serif;color:#45494F}}'
                             f'.tr.cur{{background:#E6E3DD}}</style><div class="tl">{"".join(rows)}</div>', 420)

    # 3. article header at 1440 px with a 64 px feature icon (Bill, signature red)
    pages["3-Article-Header"] = (
        f'<style>.ah{{width:1440px;box-sizing:border-box;padding:28px 120px 56px;background:#DCD9D2}}'
        f'.nav{{display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #121212;padding-bottom:14px;font:800 22px/1 "Inter Tight",sans-serif;letter-spacing:-.02em}}'
        f'.nav span{{font:500 15px/1 Inter,sans-serif;letter-spacing:0;display:flex;gap:28px}}'
        f'.hd{{display:grid;grid-template-columns:64px 1fr;gap:28px;align-items:start;margin-top:64px;max-width:980px}}'
        f'.eb{{font:700 13px/1 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#45494F;margin:0 0 14px}}'
        f'h1{{font:800 56px/1.04 "Inter Tight",sans-serif;letter-spacing:-.025em;margin:0 0 18px;text-wrap:balance}}'
        f'.dek{{font:400 20px/1.5 Inter,sans-serif;max-width:60ch;margin:0}}.by{{font:500 14px/1.4 Inter,sans-serif;color:#45494F;margin-top:22px}}</style>'
        f'<div class="ah"><div class="nav">Oath &amp; Action<span><span>Explain</span><span>Track</span><span>Connect</span><span>Act</span></span></div>'
        f'<div class="hd">{img("bill", 64, alt="Bill")}<div><p class="eb">Bill &middot; Explainer</p>'
        f'<h1>How a housing bill moves from committee to a floor vote</h1>'
        f'<p class="dek">Each step, who decides it, and where the public can weigh in before the vote.</p>'
        f'<p class="by">Illustrative headline and dek for this board, not a published story</p></div></div></div>', 1440)

    # 4. social avatar, 400 px master, shown at 72 and 40 px
    av400 = tile_svg(AVATAR_ICON, "Circle", "Charcoal", 400, glyph=AVATAR_GLYPH,
                     title="Act as a 400 px social avatar, Charcoal circle, live area at 56 percent of the diameter. Concept 2 Moving part. Proposal only.")
    avf = C.CONTEXT / f"{C.DATE}_Moving-Part-Avatar-400.svg"
    avf.write_text(av400)
    pages["4-Avatar"] = (
        f'<style>.av{{display:flex;gap:40px;align-items:center;padding:24px 28px;width:760px;box-sizing:border-box}}'
        f'.post{{display:flex;gap:12px;align-items:flex-start}}.post b{{font:700 15px/1.3 Inter,sans-serif;display:block}}.post small{{font:400 13px/1.35 Inter,sans-serif;color:#45494F;display:block}}'
        f'.cap{{font:400 13px/1.35 Inter,sans-serif;color:#45494F;margin-top:8px}}</style>'
        f'<div class="av"><div><img src="file://{avf}" width="200" height="200" style="display:block"><div class="cap">400 px master at 200 px</div></div>'
        f'<div style="display:grid;gap:22px"><div class="post"><img src="file://{avf}" width="72" height="72" style="display:block;border-radius:50%">'
        f'<div><b>Oath &amp; Action</b><small>@oathandaction, an illustrative handle &middot; profile header, 72 px</small></div></div>'
        f'<div class="post"><img src="file://{avf}" width="40" height="40" style="display:block;border-radius:50%">'
        f'<div><b>Oath &amp; Action</b><small>In a feed, 40 px</small></div></div></div></div>', 760)

    # 5. social card 1080 by 1350: Ballot large in a Newsprint rounded square on Charcoal, one working red rule
    card_tile = tile_svg("ballot", "Rounded-Square", "Newsprint", 360)
    ctf = C.CONTEXT / f"{C.DATE}_Moving-Part-Card-Ballot-Tile-360.svg"
    ctf.write_text(card_tile)
    pages["5-Social-Card"] = (
        f'<style>.card{{width:1080px;height:1350px;box-sizing:border-box;background:#121212;color:#DCD9D2;padding:96px;display:flex;flex-direction:column}}'
        f'.card .eb{{font:700 26px/1 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin:72px 0 28px}}'
        f'.card .rule{{width:120px;height:12px;background:#E63946;margin-top:64px}}'
        f'.card h2{{font:800 92px/1.0 "Inter Tight",sans-serif;letter-spacing:-.03em;margin:0;text-wrap:balance}}'
        f'.card p{{font:400 34px/1.4 Inter,sans-serif;margin:32px 0 0;max-width:24ch}}'
        f'.card .ft{{margin-top:auto;display:flex;justify-content:space-between;font:800 34px/1 "Inter Tight",sans-serif;letter-spacing:-.02em}}'
        f'.card .ft span{{font:500 24px/1 Inter,sans-serif;letter-spacing:0;color:#C9C5BC}}</style>'
        f'<div class="card"><img src="file://{ctf}" width="360" height="360" style="display:block" alt="Ballot">'
        f'<div class="rule"></div><div class="eb">Ballot &middot; Explainer</div><h2>Ranked ballots, step by step</h2>'
        f'<p>How your second choice counts when your first is out of the race.</p>'
        f'<div class="ft">Oath &amp; Action<span>Illustrative card for this board</span></div></div>', 1080)

    # 6. atlas legend at 16 px beside 13 px text, with Feedback loop
    leg = [("loop", "Feedback loop. An effect comes back to change its cause."), ("bill", "Bill. A proposed law, by its number."),
           ("testify", "Testimony. Who spoke at a hearing."), ("money", "Campaign money. Reported contributions."),
           ("housing", "Housing. Rules on rent, zoning and building.")]
    lrows = "".join(f'<div class="lg">{img(n, 16, "Charcoal")}<span>{t}</span></div>' for n, t in leg)
    lcur = f'<div class="lg">{img("loop", 16, "Charcoal-Red-Keyline", open_=True)}<span><b>Feedback loop</b>, the entry the map now shows.</span></div>'
    pages["6-Atlas-Legend"] = (
        f'<style>.leg{{width:340px;padding:16px 18px;background:#E6E3DD;border:1px solid #5D636D;margin:16px}}'
        f'.leg h4{{font:700 12px/1 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#45494F;margin:0 0 10px}}'
        f'.lg{{display:flex;gap:8px;align-items:center;font:400 13px/1.35 Inter,sans-serif;padding:4px 0}}.lg b{{font-weight:700}}'
        f'.leg hr{{border:0;border-top:1px solid #B9B5AD;margin:8px 0}}</style>'
        f'<div class="leg"><h4>Map key</h4>{lrows}<hr><h4>Selected</h4>{lcur}</div>', 380)

    # 7. tracker table row at 16 px beside status marks
    def mark(kind):
        if kind == "done":
            s = '<circle cx="6" cy="6" r="5" fill="#121212"/>'
        elif kind == "half":
            s = '<circle cx="6" cy="6" r="4.25" fill="none" stroke="#121212" stroke-width="1.5"/><path d="M6 1.75A4.25 4.25 0 0 1 6 10.25Z" fill="#121212"/>'
        else:
            s = '<circle cx="6" cy="6" r="4.25" fill="none" stroke="#121212" stroke-width="1.5"/>'
        return f'<svg width="12" height="12" viewBox="0 0 12 12" style="display:block">{s}</svg>'
    trs = [("bill", "HB 1207, tenant notice", [("done", "Filed"), ("done", "Committee"), ("half", "Floor"), ("todo", "Governor")], "Hearing Nov. 4"),
           ("testify", "Public hearing, HB 1207", [("done", "Notice"), ("half", "Sign-up open"), ("todo", "Hearing")], "Sign up by Nov. 2"),
           ("money", "Ballot committee filing", [("done", "Filed"), ("todo", "Audit")], "Due Dec. 1")]
    body = "".join(
        f'<tr><td class="ic">{img(n, 16, "Charcoal")}</td><td><b>{t}</b></td><td><span class="st">'
        + "".join(f'<span class="mk">{mark(k)}{lbl}</span>' for k, lbl in st) + f'</span></td><td class="n">{nx}</td></tr>'
        for n, t, st, nx in trs)
    pages["7-Tracker-Row"] = (
        f'<style>.tk{{width:860px;margin:16px;border-collapse:collapse;font:400 14px/1.35 Inter,sans-serif}}'
        f'.tk th{{font:700 12px/1 Inter,sans-serif;letter-spacing:.06em;text-transform:uppercase;color:#45494F;text-align:left;padding:8px 10px;border-bottom:2px solid #121212}}'
        f'.tk td{{padding:9px 10px;border-bottom:1px solid #B9B5AD;vertical-align:middle}}.tk td.ic{{width:16px;padding-right:0}}.tk b{{font-weight:600}}'
        f'.st{{display:flex;gap:14px;flex-wrap:wrap}}.mk{{display:inline-flex;gap:5px;align-items:center;font-size:13px}}.n{{font-variant-numeric:tabular-nums;white-space:nowrap}}</style>'
        f'<table class="tk"><thead><tr><th></th><th>Item</th><th>Status</th><th>Next</th></tr></thead><tbody>{body}</tbody></table>'
        f'<p style="font:400 13px/1.4 Inter,sans-serif;color:#45494F;margin:0 16px 16px">Bill numbers, dates and steps are illustrative.</p>', 900)

    # 8. app tile at 180, 120, 60 and 29 px on a light and a dark wallpaper
    walls = []
    for wall, bg, fg in (("Light wallpaper", "linear-gradient(160deg,#EDEAE4 0%,#C9C5BC 100%)", "#121212"),
                         ("Dark wallpaper", "linear-gradient(160deg,#2B2F36 0%,#0B0C0E 100%)", "#F2F0EC")):
        tiles = "".join(f'<div class="ap"><img src="file://{app_file()}" width="{s}" height="{s}" style="display:block"><span style="font-size:{12 if s < 61 else 14}px">{s} px</span></div>'
                        for s in (180, 120, 60, 29))
        walls.append(f'<div class="wp" style="background:{bg};color:{fg}"><div class="wl">{wall}</div><div class="aps">{tiles}</div></div>')
    pages["8-App-Tile"] = (
        f'<style>.wp{{padding:24px 32px 28px}}.wl{{font:700 12px/1 Inter,sans-serif;letter-spacing:.08em;text-transform:uppercase;margin-bottom:16px}}'
        f'.aps{{display:flex;gap:36px;align-items:flex-end}}.ap{{display:grid;gap:8px;justify-items:center;font:500 14px/1 Inter,sans-serif}}</style>{"".join(walls)}', 620)
    return pages


def write_contexts():
    C.CONTEXT.mkdir(parents=True, exist_ok=True)
    out = {}
    for key, (body, width) in context_pages().items():
        page = (f'<!doctype html><html><head><meta charset="utf-8"><style>{C.font_css()}{BASE_CSS}</style></head>'
                f'<body style="width:{width}px">{body}</body></html>')
        p = C.SCRATCH / f"context-{key}.html"
        p.write_text(page)
        png = C.CONTEXT / f"{C.DATE}_Moving-Part-Context-{key}.png"
        shoot(p, png, width)
        out[key] = png
    return out


if __name__ == "__main__":
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    write_holders()
    write_app_tiles()
    for k, v in write_contexts().items():
        print(k, v)
