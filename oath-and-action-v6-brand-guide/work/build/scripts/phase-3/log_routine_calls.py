"""Number an owner's routine calls into the decision log.

Usage, from the project folder:
  python3 -I work/build/scripts/phase-3/log_routine_calls.py <notes.md> "<log heading>" ["<section name>"]

Reads the notes file's section "## <section name>" (default "Routine calls") up to the next "## " heading, takes every
line of the form "- D3-xxx | decision | reason", and appends them to work/ledger/20261020_Decision-Log.md under
"### <log heading>", numbered on from the log's highest D3 number. It slices by heading, never by a text search, so a
section is never logged twice by accident (V13, section 3). Check the log for repeated D3 numbers afterwards:
  grep -o "^| D3-[0-9]*" work/ledger/20261020_Decision-Log.md | sort | uniq -d
"""
import re
import sys

LOG = 'work/ledger/20261020_Decision-Log.md'


def main():
    src, heading = sys.argv[1], sys.argv[2]
    section = sys.argv[3] if len(sys.argv) > 3 else 'Routine calls'
    text = open(src, encoding='utf-8').read()
    m = re.search(r'^## ' + re.escape(section) + r'[^\n]*\n', text, re.M)
    if not m:
        sys.exit(f'no "## {section}" section in {src}')
    sec = text[m.end():]
    nxt = re.search(r'^## ', sec, re.M)
    sec = sec[:nxt.start()] if nxt else sec
    lines = [l for l in sec.splitlines() if re.match(r'^\s*[-*]?\s*\|?\s*D3-xxx\s*\|', l)]
    log = open(LOG, encoding='utf-8').read()
    last = max(int(n) for n in re.findall(r'^\| D3-(\d+) ', log, re.M))
    out = ['', f'### {heading}', '', '| # | Decision | Reason |', '|---|---|---|']
    n = last
    for l in lines:
        n += 1
        body = re.sub(r'^\s*[-*]?\s*\|?\s*D3-xxx\s*\|\s*', '', l).rstrip().rstrip('|').rstrip()
        out.append(f'| D3-{n} | {body} |')
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write('\n'.join(out) + '\n')
    print(f'{len(lines)} calls: D3-{last + 1} to D3-{n}' if lines else 'no calls found')


if __name__ == '__main__':
    main()
