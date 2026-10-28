"""Concept 1, Overprint: the eight contexts from the creative director's round-two brief (design
director, Phase 2, round two, October 28, 2026).

Run: python3 -I icons_r2_overprint_contexts.py   (after icons_r2_overprint_assets.py)
Writes standalone HTML compositions and their Chromium captures to
work/boards/phase-2/icons-r2/overprint/context/. The board places the captures and builds the small
contexts (menus, lists, legend, table row) inline at true size.

All copy in the compositions is illustrative and labeled on the board. No real bill, hearing,
person or figure appears.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_overprint_common as C  # noqa: E402
import icons_r2_overprint_draw as O  # noqa: E402

FONT_CSS = "".join(
    f"@font-face{{font-family:'{f}';font-weight:{w};src:url('file://{C.FONTS / fn}')}}"
    for f, w, fn in [("Inter Tight", 800, "Inter-Tight-800-normal.ttf"), ("Inter Tight", 600, "Inter-Tight-600-normal.ttf"),
                     ("Inter", 400, "Inter-400-normal.ttf"), ("Inter", 600, "Inter-600-normal.ttf"), ("Inter", 700, "Inter-700-normal.ttf")])


def wordmark(height, color):
    s = (C.SPRITE / "wordmark.svg").read_text()
    s = s.replace('style="color:#121212"', f'style="color:{color};height:{height}px;width:auto;display:block"', 1)
    return s.replace("<title>wordmark</title>", "<title>Oath &amp; Action</title>")


def page(body, w, h, bg=C.NEWS):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{FONT_CSS}
html,body{{margin:0;padding:0}} body{{width:{w}px;height:{h}px;background:{bg};color:{C.CHAR};font:400 18px/1.5 'Inter',sans-serif;overflow:hidden}}
</style></head><body>{body}</body></html>"""


def article():
    """Context 3: an article header at 1440 px with one feature icon at 64 px beside the headline."""
    icon = C.svg(C.lay("ballot", "Display"), "Display", px=64)
    body = f"""<div style="padding:28px 96px 0;border-bottom:1px solid #5D636D;height:84px;display:flex;align-items:center;justify-content:space-between">
{wordmark(26, C.CHAR)}<div style="display:flex;gap:28px;font:600 15px 'Inter'"><span>Explain</span><span>Track</span><span>Connect</span><span>Act</span></div></div>
<div style="padding:64px 96px 0;display:grid;grid-template-columns:64px 1fr;column-gap:28px;align-items:start;max-width:1040px">
<div style="padding-top:10px">{icon}</div>
<div><div style="font:700 13px 'Inter';letter-spacing:.08em;text-transform:uppercase;color:#45494F">Elections · Explainer</div>
<h1 style="font:800 56px/1.04 'Inter Tight';letter-spacing:-.02em;margin:10px 0 18px">How a question gets onto your ballot</h1>
<p style="font:400 21px/1.5 'Inter';margin:0;max-width:62ch;color:#2B2E33">Who writes the wording, who checks the signatures and how long each step takes, explained for a reader who has never filed a petition.</p>
<p style="font:400 15px 'Inter';color:#45494F;margin-top:22px">By the Oath &amp; Action desk · 8 minute read</p></div></div>"""
    return page(body, 1440, 520)


def social_card():
    """Context 5: a 1080 by 1350 social card with one icon large in a holder and one working red
    elsewhere, the ask button (D1-23: red fill, White bold label, Charcoal keyline on Newsprint)."""
    tile, *_ = C.tile_svg("testify", "Rounded-Square", "Charcoal", 360)
    body = f"""<div style="padding:96px 96px 0">{wordmark(30, C.CHAR)}</div>
<div style="padding:84px 96px 0">{tile}</div>
<div style="padding:64px 96px 0"><div style="font:700 26px 'Inter';letter-spacing:.08em;text-transform:uppercase;color:#45494F">Act · Public hearing</div>
<h1 style="font:800 92px/1.02 'Inter Tight';letter-spacing:-.02em;margin:18px 0 28px">Your three minutes at the microphone</h1>
<p style="font:400 34px/1.45 'Inter';margin:0;color:#2B2E33;max-width:28ch">What to bring, how to sign up and what the committee does with what you say.</p>
<div style="margin-top:56px;display:inline-block;background:{C.RED};color:#fff;font:700 34px 'Inter';padding:26px 44px;border:3px solid {C.CHAR}">Sign up to testify</div></div>"""
    return page(body, 1080, 1350)


def app_wallpapers():
    """Context 8: the app tile at 180, 120, 60 and 29 px on a light and a dark wallpaper."""
    rows = []
    for bg, fg in (("#ECEAE5", C.CHAR), ("#26272B", "#E7E5E0")):
        cells = []
        for s in (180, 120, 60, 29):
            t = C.app_tile_svg(C.APP_SCALE).replace('width="1024" height="1024"', f'width="{s}" height="{s}"')
            cells.append(f'<div style="display:flex;flex-direction:column;align-items:center;gap:10px">{t}'
                         f'<span style="font:600 15px Inter;color:{fg}">{s} px</span></div>')
        rows.append(f'<div style="background:{bg};display:flex;gap:56px;align-items:flex-end;padding:40px 48px">{"".join(cells)}</div>')
    return page("".join(rows), 760, 2 * 300, "#ECEAE5")


def avatar():
    """Context 4: a 400 px social avatar (the circle holder, Charcoal), and the same at 72 and 40 px."""
    big, *_ = C.tile_svg("act", "Circle", "Charcoal", 400)
    return page(f'<div style="padding:20px">{big}</div>', 440, 440)


def write_avatar():
    big, *_ = C.tile_svg("act", "Circle", "Charcoal", 400, title="Oath &amp; Action avatar, Act in the Charcoal circle, 400 px. Proposal only.")
    (C.CONTEXT / f"{C.DATE}_Overprint-Avatar-400.svg").write_text(big + "\n")


def capture(name, html, w, h):
    C.CONTEXT.mkdir(parents=True, exist_ok=True)
    src = C.CONTEXT / f"{C.DATE}_Overprint-Context-{name}.html"
    src.write_text(html)
    png = C.CONTEXT / f"{C.DATE}_Overprint-Context-{name}.png"
    subprocess.run(["node", str(C.SHOT_JS), str(src), str(png), str(w), "1", str(h)], check=True)
    return png


def main():
    capture("Article-Header-1440", article(), 1440, 520)
    capture("Social-Card-1080", social_card(), 1080, 1350)
    capture("App-Tile-Wallpapers", app_wallpapers(), 760, 600)
    capture("Avatar-400", avatar(), 440, 440)
    write_avatar()
    print("contexts written")


if __name__ == "__main__":
    main()
