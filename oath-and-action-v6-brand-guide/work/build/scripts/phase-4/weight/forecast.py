"""1b's forecast (DR-331, Phase 4 board 1 item 3): chapters 22 to 25, 27 and 28 estimated from units measured on the page the
build has just made, low, mid and high, and the projection with each in place of the allocations.

guide_build.py calls it after the weight gates and prints one note beside the projection; the record goes to the build report
under weight.forecast. The method is chat 12b's (work/handoffs/phase-4/20261124_Chat-12b-Engineer-Weight-Notes.md, "option 1b"):
chat 10's counts of what each chapter draws (work/handoffs/phase-4/20261121_Phase-4-Allocations.md, section 3), priced at units
measured on chapters 16, 20 and 21 as built, and at chat 10's prices for parts no built chapter draws yet. Low takes the
cheapest measured unit, mid the measured mean, high the dearest, with the swaps chat 12 named for a page-like view.

  python3 work/build/scripts/phase-4/weight/forecast.py PAGE.html   prints the units and the six chapters for a built page
"""
import json
import re
import sys
from pathlib import Path

# The chapters the units come from (Phase 4's chapters as built and approved, DR-329) and their anchors
UNIT_CHAPTERS = {"16": "photography", "20": "web", "21": "atlas"}
WEB_PAGES = {"A06": "home", "A07": "article", "A08": "Act page"}   # chapter 20's full-length pages
# Chat 10's prices for parts no built chapter draws yet (Phase-4-Allocations, sections 1 and 2)
CHAT_10 = {"rule": 6_726, "artboard": 8_039, "twin": 3_657, "print": 11_355, "chart": 11_570, "chart_in_post": 12_570,
           "reader": 69_902, "controls": 10_000, "slides": 35_687}
NO_SAMPLE = {"low": 150_000, "mid": 200_000, "high": 400_000}   # chapters 27 and 28: chapters 19 and 17 bracket them
FORECAST = ("22", "23", "24", "25", "27", "28")
CASES = ("low", "mid", "high")
size = lambda x: len(x.encode())


def element_at(text, start, tag):
    depth = 0
    for m in re.finditer(rf"<{tag}\b|</{tag}>", text[start:]):
        depth += 1 if m.group(0) != f"</{tag}>" else -1
        if depth == 0:
            return text[start:start + m.end()]
    return text[start:]


def spans(page):
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'<section class="(?:chapter|part|contents|appendix|cover|start)[^"]*" id="([^"]+)"', page)]
    end = page.rfind("</main>")
    return {a: (s, n) for (s, a), (n, _) in zip(marks, marks[1:] + [(end, None)])}


def plates(sec):
    out, i = [], 0
    for m in re.finditer(r'<figure class="plate\b[^"]*"', sec):
        if m.start() < i:
            continue
        f = element_at(sec, m.start(), "figure")
        out.append((m.group(0), f))
        i = m.start() + len(f)
    return out


CROP_KEY = re.compile(r"^\d+-(?:light|dark)(?:-open)?-(?!screen$)[a-z0-9]+$")


def units(page):
    """The measured units, each with the measures behind it. None when chapters 16, 20 and 21 are not all on the page."""
    sp = spans(page)
    if not all(a in sp for a in UNIT_CHAPTERS.values()):
        return None
    rule, fail, detail = {}, {}, []
    for n, a in UNIT_CHAPTERS.items():
        s, e = sp[a]
        sec = page[s:e]
        pl = plates(sec)
        rules = len(re.findall(r'<div class="rule"', sec))
        rule[n] = round((size(sec) - sum(size(f) for _, f in pl)) / rules)
        fl = [size(f) for c, f in pl if "plate--failure" in c]
        fail[n] = round(sum(fl) / len(fl))
        if n == "21":
            for c, f in pl:
                keys = [k.split(" ", 1)[1] for k in re.findall(r'data-oa-page-frame="([^"]+)"', f)]
                if keys and all(CROP_KEY.match(k) for k in keys):
                    sid = re.search(r'data-specimen="([^"]+)"', f)
                    detail.append((sid.group(1) if sid else "?", size(f)))
    s, e = sp[UNIT_CHAPTERS["20"]]
    sec = page[s:e]
    web = {}
    for m in re.finditer(r'<div class="oa-app-frame"[^>]*data-oa-page-frame="(A\d+) ([^"]+)"', sec):
        if m.group(1) in WEB_PAGES and not m.group(2).endswith("-screen"):
            web.setdefault(WEB_PAGES[m.group(1)], []).append(size(element_at(sec, m.start(), "div")))
    web = {k: round(sum(v) / len(v)) for k, v in web.items()}
    head = page[:page.find("<body")]
    style = {m.group(1): size(m.group(0)) for m in re.finditer(r'<style data-oa-app-kit="([^"]+)">.*?</style>', head, re.S)}
    mean = lambda d: round(sum(d) / len(d))
    det = [b for _, b in detail]
    return {
        "rule": {"low": min(CHAT_10["rule"], *rule.values()), "mid": mean(list(rule.values())), "high": max(rule.values()), "measured": rule},
        "failure": {"low": min(fail.values()), "mid": mean(list(fail.values())), "high": max(fail.values()), "measured": fail},
        "web_frame": {"low": min(web.values()), "mid": mean(list(web.values())), "high": max(web.values()), "measured": web},
        "style": {"low": min(style.values()), "mid": mean(list(style.values())), "high": max(style.values()), "measured": style},
        "detail": {"low": min(det), "mid": mean(det), "high": max(det), "measured": dict(detail)},
    }


def chapters(u):
    """Each chapter's lines and its low, mid and high, from the units (chat 12b's lines, chat 10's counts)."""
    U = lambda k, c: u[k][c]
    A, T, P = CHAT_10["artboard"], CHAT_10["twin"], CHAT_10["print"]
    plan = {
        "22": [("10 rules' words and frames", lambda c: 10 * U("rule", c)),
               ("Substack's 8 parts (artboards; high: page frames)", lambda c: 8 * (U("web_frame", "high") if c == "high" else A)),
               ("one chart in a post", lambda c: CHAT_10["chart_in_post"]),
               ("the working email at 600 and 375 px and images off (3 page frames; high: both themes, 6)",
                lambda c: (6 if c == "high" else 3) * U("web_frame", c)),
               ("its renderer's style, once", lambda c: U("style", c)),
               ("share preview", lambda c: A),
               ("10 failure plates", lambda c: 10 * U("failure", c)),
               ("4 detail plates", lambda c: 4 * U("detail", c))],
        "23": [("20 rules' words and frames", lambda c: 20 * U("rule", c)),
               ("36 posts and 4 video frames (artboards)", lambda c: 40 * A),
               ("12 profiles as a reader meets them (low: artboards; mid: the cheapest page frame; high: the mean)",
                lambda c: 12 * {"low": A, "mid": U("web_frame", "low"), "high": U("web_frame", "mid")}[c]),
               ("smallest-size twins (8; high: every post with its feed twin, 36)", lambda c: (36 if c == "high" else 8) * T),
               ("its renderer's style, once", lambda c: U("style", c)),
               ("20 failure plates", lambda c: 20 * U("failure", c)),
               ("4 detail plates", lambda c: 4 * U("detail", c))],
        "24": [("13 rules' words and frames", lambda c: 13 * U("rule", c)),
               ("the reader with all 12 pages (high: each at the full print unit)", lambda c: 12 * P if c == "high" else CHAT_10["reader"]),
               ("2 charts", lambda c: 2 * CHAT_10["chart"]),
               ("the reader's controls (assumed 10,000; high: as heavy as the largest renderer style)",
                lambda c: U("style", "high") if c == "high" else CHAT_10["controls"]),
               ("13 failure pages", lambda c: 13 * U("failure", c)),
               ("2 detail plates", lambda c: 2 * U("detail", c))],
        "25": [("9 rules' words and frames", lambda c: 9 * U("rule", c)),
               ("explainer, letterhead, poster and table sign (high: half again heavier)", lambda c: round(4 * P * (1.5 if c == "high" else 1))),
               ("slide cover, content and data with its chart (high: half again heavier)", lambda c: round(CHAT_10["slides"] * (1.5 if c == "high" else 1))),
               ("9 failure plates", lambda c: 9 * U("failure", c)),
               ("2 detail plates", lambda c: 2 * U("detail", c))],
    }
    out = {}
    for n, lines in plan.items():
        rows = [{"line": w, **{c: round(f(c)) for c in CASES}} for w, f in lines]
        out[n] = {**{c: sum(r[c] for r in rows) for c in CASES}, "lines": rows}
    for n in ("27", "28"):
        out[n] = {**NO_SAMPLE, "lines": [{"line": "no sample; chapters 19 and 17 bracket it", **NO_SAMPLE}]}
    return out


def beside(page, weights, projection, allocation, in_progress):
    """The forecast and the projection with it, for the build's note. allocation and in_progress are guide_charts'."""
    u = units(page)
    if not u:
        return None
    est = chapters(u)
    ch = {n: v["bytes"] for n, v in weights["chapters"].items()}
    proj = projection["projected_bytes"]
    with_forecast, counted = {}, {}
    for c in CASES:
        delta = 0
        for n in FORECAST:
            if n in ch and n not in in_progress:
                continue   # built and finished: the page carries it at its bytes
            have = ch.get(n, 0)
            delta += max(0, est[n][c] - have) - max(0, round(allocation[n]) - have)
        with_forecast[c] = proj + delta
    for n in FORECAST:
        counted[n] = round(allocation[n])
    return {"units": u, "chapters": est, "allocated": sum(counted.values()), "allocations": counted,
            "totals": {c: sum(est[n][c] for n in FORECAST) for c in CASES},
            "projection": proj, "projection_with_forecast": with_forecast}


def line(rec, limit=16_000_000):
    t, p, u = rec["totals"], rec["projection_with_forecast"], rec["units"]
    room = lambda x: (f"{limit - x:,} under 16 MB" if x <= limit else f"{x - limit:,} past 16 MB")
    return ("page weight: 1b's forecast beside the projection (DR-331): chapters 22 to 25, 27 and 28 from units measured on this page "
            f"come to low {t['low']:,}, mid {t['mid']:,} and high {t['high']:,} bytes against {rec['allocated']:,} allocated; with them in "
            f"place of the allocations the page projects to low {p['low']:,} ({room(p['low'])}), mid {p['mid']:,} ({room(p['mid'])}) and "
            f"high {p['high']:,} ({room(p['high'])}), beside the build's {rec['projection']:,}. Mid by chapter: "
            + "; ".join(f"{n} {rec['chapters'][n]['mid']:,}" for n in FORECAST)
            + f". Units (low / mid / high): a rule's words and frames {u['rule']['low']:,} / {u['rule']['mid']:,} / {u['rule']['high']:,}; "
            f"a failure plate {u['failure']['low']:,} / {u['failure']['mid']:,} / {u['failure']['high']:,}; a web page frame "
            f"{u['web_frame']['low']:,} / {u['web_frame']['mid']:,} / {u['web_frame']['high']:,}; a renderer's style {u['style']['low']:,} / "
            f"{u['style']['mid']:,} / {u['style']['high']:,}; a detail plate {u['detail']['low']:,} / {u['detail']['mid']:,} / {u['detail']['high']:,}")


if __name__ == "__main__":
    page = Path(sys.argv[1]).read_text(encoding="utf-8")
    u = units(page)
    print(json.dumps(u, indent=1))
    est = chapters(u)
    for n in FORECAST:
        print(n, {c: est[n][c] for c in CASES})
    print("all", {c: sum(est[n][c] for n in FORECAST) for c in CASES})
