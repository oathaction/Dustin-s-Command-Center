"""Turn a studio page (a full HTML document) into the form the private-page host expects: no doctype, html, head
or body tags of its own, the title first, and an explicit page ground, since the host wraps the page in its own
document skeleton.

Usage:
    python3 -I work/build/scripts/phase-2/to_artifact_page.py <in.html> <out.html> --title "Name" --ground "#FFFFFF" [--ink "#121212"]

The studio file stays the record; the output is a publish copy only.
"""
import re
import sys


def main():
    args = sys.argv[1:]
    src, out = args[0], args[1]
    opts = dict(zip(args[2::2], args[3::2]))
    page = open(src, encoding='utf-8').read()
    page = re.sub(r'<!doctype[^>]*>\s*', '', page, flags=re.I)
    page = re.sub(r'</?html[^>]*>\s*', '', page, flags=re.I)
    page = re.sub(r'</?head>\s*', '', page, flags=re.I)
    page = re.sub(r'<body([^>]*)>', r'<div\1>', page, count=1, flags=re.I) if opts.get('--keep-body-attrs') else re.sub(r'<body[^>]*>\s*', '', page, count=1, flags=re.I)
    page = re.sub(r'\s*</body>\s*', '\n', page, flags=re.I)
    page = re.sub(r'<meta\s+charset=[^>]*>\s*', '', page, flags=re.I)
    page = re.sub(r'<meta\s+name="viewport"[^>]*>\s*', '', page, flags=re.I)
    page = re.sub(r'<title>.*?</title>\s*', '', page, flags=re.S | re.I)
    title = opts.get('--title', 'Untitled page')
    ground = opts.get('--ground', '#FFFFFF')
    ink = opts.get('--ink', '#121212')
    head = f'<title>{title}</title>\n<style>:root{{color-scheme:light}} body{{background:{ground};color:{ink}}}</style>\n'
    open(out, 'w', encoding='utf-8').write(head + page.strip() + '\n')
    print('wrote', out, f'{len(page) / 1e3:.0f} kB')


if __name__ == '__main__':
    main()
