"""Editor, Phase 1: extract the visible text of a review board for the editorial pass.

Skips <style>, <script> and <svg> bodies (SVG <title> and <text> are kept and
marked), keeps alt and aria-label text as marked lines, and writes one block per
element with the nearest heading id or text as a locator.

Run: python3 -I work/build/scripts/phase-1/editor_board_text.py <board.html> <out.txt>
"""
import sys
from html.parser import HTMLParser
from pathlib import Path

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "td", "th", "figcaption",
         "caption", "dt", "dd", "blockquote", "div", "section", "summary", "label",
         "button", "a", "span", "small", "strong", "em", "b", "i", "code", "title", "text", "tspan"}


class Extract(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.svg = 0
        self.svg_text = 0
        self.buf = []
        self.out = []
        self.loc = ""
        self.heading = None

    def flush(self, tag=""):
        text = " ".join("".join(self.buf).split())
        if text:
            prefix = "[svg] " if self.svg else ""
            self.out.append(f"{self.loc} | {prefix}{tag}: {text}")
        self.buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("style", "script"):
            self.skip += 1
            return
        if tag == "svg":
            self.svg += 1
        if self.svg and tag in ("title", "text", "desc"):
            self.svg_text += 1
        if a.get("aria-label") and not self.skip:
            self.out.append(f"{self.loc} | aria({tag}): {a['aria-label']}")
        if tag == "img" and a.get("alt") is not None:
            self.out.append(f"{self.loc} | alt: {a.get('alt')}")
        if a.get("id") and tag in ("section", "h1", "h2", "h3", "article", "aside"):
            self.loc = "#" + a["id"]
        if tag in BLOCK or tag == "br":
            self.flush(tag)

    def handle_endtag(self, tag):
        if tag in ("style", "script"):
            self.skip -= 1
            return
        if self.svg and tag in ("title", "text", "desc"):
            self.flush("svg-" + tag)
            self.svg_text -= 1
        if tag == "svg":
            self.svg -= 1
        if tag in BLOCK:
            self.flush(tag)

    def handle_data(self, data):
        if self.skip:
            return
        if self.svg and not self.svg_text:
            return
        self.buf.append(data)


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2])
    p = Extract()
    p.feed(src.read_text(encoding="utf-8"))
    p.flush()
    lines = []
    for i, line in enumerate(p.out, 1):
        lines.append(f"{i:04d} {line}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out, len(lines), "lines", sum(len(l.split()) for l in lines), "words")


if __name__ == "__main__":
    main()
