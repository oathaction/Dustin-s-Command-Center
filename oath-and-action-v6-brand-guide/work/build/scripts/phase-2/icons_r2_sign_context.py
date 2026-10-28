"""Concept 3, Public sign, stage 2: render the two context pieces that need web fonts to PNG.

Run after icons_r2_sign_assets.py: python3 -I icons_r2_sign_context.py
Writes in work/boards/phase-2/icons-r2/public-sign/context/:
  20261028_Public-Sign-Social-Card-1080x1350.png   one icon large in the square sign panel and one
                                                   working red elsewhere (a rule over the headline)
  20261028_Public-Sign-Article-Header-1440.png     an article header at 1440 px with a 64 px
                                                   feature icon beside the headline
All copy on both is illustrative. The HTML sources go to the scratch folder.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import icons_r2_sign_common as C  # noqa: E402
from icons_r2_sign_common import CHAR, NEWS, RED  # noqa: E402

FONTS = ('<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;800'
         '&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">')


def page(body, w, h, css):
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>'
            f'html,body{{margin:0;padding:0}}body{{width:{w}px;height:{h}px;overflow:hidden;background:{NEWS};color:{CHAR};'
            f'font-family:Inter,Arial,sans-serif}}{css}</style></head><body>{body}</body></html>')


def social_card():
    tile, *_ = C.tile_svg("testify", "Sign-Panel", "Charcoal", 600)
    css = ('.wrap{position:absolute;inset:0;padding:96px 90px}'
           '.eye{font:700 28px/1.2 Inter;letter-spacing:.08em;text-transform:uppercase}'
           '.tile{margin-top:64px}.tile svg{display:block}'
           '.rule{width:140px;height:14px;background:' + RED + ';margin-top:70px}'
           'h1{font:800 76px/1.04 "Inter Tight";letter-spacing:-.02em;margin:28px 0 0;max-width:880px}'
           '.ft{position:absolute;left:90px;bottom:90px;font:400 30px/1.3 Inter}')
    body = (f'<div class="wrap"><div class="eye">How to testify</div><div class="tile">{tile}</div>'
            '<div class="rule"></div><h1>Two minutes at the microphone, planned in five steps</h1>'
            '<div class="ft">Swipe for the steps</div></div>')
    return page(body, 1080, 1350, css)


def article_header():
    css = ('.bar{height:64px;border-bottom:1px solid #5D636D;display:flex;align-items:center;padding:0 120px;'
           'font:600 16px/1 Inter;gap:36px}.bar span:first-child{font:800 20px/1 "Inter Tight";margin-right:auto}'
           '.hd{display:grid;grid-template-columns:64px 1fr;gap:28px;align-items:start;padding:72px 120px 0;max-width:1200px}'
           '.hd svg{display:block}.eye{font:700 14px/1.2 Inter;letter-spacing:.08em;text-transform:uppercase;margin:0 0 14px}'
           'h1{font:800 56px/1.06 "Inter Tight";letter-spacing:-.02em;margin:0;max-width:900px}'
           '.dek{font:400 22px/1.5 Inter;margin:20px 0 0;max-width:760px;color:#45494F}'
           '.by{font:600 15px/1.4 Inter;margin:26px 0 0}')
    icon = C.svg("testify", "Display", "Charcoal-Red", px=64)
    body = ('<div class="bar"><span>Publication name</span><span>Explain</span><span>Track</span><span>Connect</span><span>Act</span></div>'
            f'<div class="hd">{icon}<div><p class="eye">Testify</p><h1>How to sign up, speak and follow up at a city council hearing</h1>'
            '<p class="dek">A guide to the two minutes you get at the microphone, and what happens to your words afterward.</p>'
            '<p class="by">By the newsroom · 8 minute read</p></div></div>')
    return page(body, 1440, 520, css)


def render(html, name, w, h):
    C.SCRATCH.mkdir(parents=True, exist_ok=True)
    src = C.SCRATCH / f"{name}.html"
    src.write_text(html)
    out = C.CONTEXT / f"{C.DATE}_Public-Sign-{name}.png"
    subprocess.run(["node", str(C.SHOT_JS), str(src), str(out), str(w), "1"], check=True)
    from PIL import Image
    im = Image.open(out)
    if im.size[1] != h:        # the capture is at least the 900 px viewport tall; trim to the page
        im.crop((0, 0, w, h)).save(out)
    return out


def main():
    a = render(social_card(), "Social-Card-1080x1350", 1080, 1350)
    b = render(article_header(), "Article-Header-1440", 1440, 520)
    print(a.name, b.name)


if __name__ == "__main__":
    main()
