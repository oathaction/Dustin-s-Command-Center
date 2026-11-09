"""Stage B Civic Line new topic drawings: Testify and Contact an official
(DR-141, DR-147), three options each, in Civic Line's hand.

Signs these drawings must not borrow (research notes, section 1, note 4, and
the accessibility audit, 1.4 and 1.5): two speech bubbles (R-12, CL-008),
person + arrow + envelope (CL-061), official at a desk with a red tie
(CL-026), two people level across a table (CL-016), speaker at a lectern with
listeners (CL-005, CL-002), gavel and scales (R-11, CL-027, R-16), a raised
right hand, a megaphone or placard, a hand pressing a button (CL-022).
"""
import math

import civic_line_stage_b_common as C

P = C.Pen


# ------------------------------------------------------------------ shared parts

def official_at_desk(pen, x, y, k=0.8, half=34, depth=30, plate=False):
    """An official seated behind a desk, seen from the front, with no tie.
    (x, y) is the desk top's center. The desk front is a box under an
    overhanging top. A nameplate, if asked, stands on the desk top."""
    els = C.person(pen, x, y - 3, k=k, h=24)
    els += [pen.line(x - half - 5, y, x + half + 5, y),
            pen.poly([(x - half, y), (x - half, y + depth), (x + half, y + depth), (x + half, y)])]
    if plate:
        els.append(pen.poly([(x - 13, y), (x - 10, y - 8), (x + 10, y - 8), (x + 13, y)]))
    return els


def speech_mark(pen, x, y, w=34, h=24, tail="left"):
    """One speech mark: a rounded box with a short tail at a bottom corner.
    (x, y) is the box's center."""
    r = 6
    x0, y0, x1, y1 = x - w / 2, y - h / 2, x + w / 2, y + h / 2
    cmds = [("M", x0 + r, y0), ("L", x1 - r, y0), ("A", r, 0, 1, x1, y0 + r), ("L", x1, y1 - r), ("A", r, 0, 1, x1 - r, y1)]
    if tail == "right":
        cmds += [("L", x1 - 3, y1 + 9), ("L", x1 - 14, y1), ("L", x0 + r, y1)]
    else:
        cmds += [("L", x0 + 14, y1), ("L", x0 + 3, y1 + 9), ("L", x0 + r, y1)]
    cmds += [("A", r, 0, 1, x0, y1 - r), ("L", x0, y0 + r), ("A", r, 0, 1, x0 + r, y0), ("Z",)]
    return pen.path(cmds)


def desk_phone(pen, x, y, s=1.0):
    """A very simple telephone: a low body with a round dial, and the handset
    resting across it. (x, y) is the body's bottom center."""
    q = pen.sub(x, y, s)
    body = q.path([("M", -26, 0), ("L", -19, -22), ("L", 19, -22), ("L", 26, 0), ("Z",)])
    dial = q.circle(0, -10, 5.0)
    handset = q.path([("M", -34, -27), ("L", -34, -33), ("Q", -34, -43, -22, -43), ("L", 22, -43),
                      ("Q", 34, -43, 34, -33), ("L", 34, -27)])
    cups = [q.line(-41, -27, -27, -27), q.line(27, -27, 41, -27)]
    return [body, dial, handset] + cups


def microphone(pen, x, y, s=1.0):
    """The common microphone: an upright capsule in a U-shaped holder on a
    stem and a base. (x, y) is the base's center."""
    q = pen.sub(x, y, s)
    return [q.rect(-6.5, -46, 13, 24, rx=6.5),
            q.path([("M", -12, -32), ("L", -12, -29), ("A", 12, 0, 0, 12, -29), ("L", 12, -32)]),
            q.line(0, -17, 0, 0), q.line(-10, 0, 10, 0)]


def bench(pen, n=3, half=74, rise=12, k=0.62):
    """A raised, curved dais seen from the witness's side, with n officials
    seated behind it. The dais front is a band between two arcs that bow up
    at the middle, as a curve around the witness looks from in front of it.
    Origin at the dais top's middle."""
    els = []
    xs = [(-half + 26) + i * ((2 * half - 52) / (n - 1)) for i in range(n)] if n > 1 else [0]
    for x in xs:
        yb = rise * (x / half) ** 2
        els += C.person(pen, x, yb - 2, k=k, h=22)
    top = [("M", -half, rise), ("Q", 0, -rise, half, rise)]
    bot = [("M", -half, rise + 22), ("Q", 0, -rise + 22, half, rise + 22)]
    els += [pen.path(top), pen.path(bot), pen.line(-half, rise, -half, rise + 22), pen.line(half, rise, half, rise + 22)]
    return els


# ------------------------------------------------------------------ Testify

def testify_a():
    """DR-147's option: the hearing from behind the witness. A raised,
    curved dais with three officials above; below, the witness at the table
    with a microphone, red, leaning in."""
    p = P(120, 40)
    top = bench(p)
    w = C.person(p, -10, 128, k=0.9, h=26)
    table = [p.line(-58, 128, 58, 128)]
    mic = microphone(p, 30, 128, s=0.85)
    return [("base", top + w + table), ("accent", mic)]


def testify_b():
    """The hearing from the side: the witness at a low table with the red
    microphone, facing a tall bench where three officials sit above. The
    officials' bench stands on a step, so it is higher than the witness."""
    p = P()
    w = C.person(p, 40, 120, k=0.9, h=26)
    table = [p.line(14, 120, 92, 120), p.line(84, 120, 84, 150)]
    mic = microphone(p, 72, 120, s=0.8)
    officials = []
    for x in (128, 164, 200):
        officials += C.person(p, x, 76, k=0.62, h=22)
    benchf = [p.line(106, 76, 222, 76), p.poly([(112, 76), (112, 136), (216, 136), (216, 76)]),
              p.line(104, 150, 224, 150), p.poly([(104, 150), (104, 136), (224, 136), (224, 150)])]
    return [("base", w + table + officials + benchf), ("accent", mic)]


def testify_c():
    """The reader's own seat: the raised, curved dais with three officials,
    and in front of it the red microphone on the witness table. No witness
    figure; the reader is the witness."""
    p = P(120, 40)
    top = bench(p)
    table = [p.line(-50, 132, 50, 132)]
    mic = microphone(p, 0, 132, s=1.25)
    return [("base", top + table), ("accent", mic)]


# ------------------------------------------------------------------ Contact an official

def contact_a():
    """DR-147's option: a person and an official's desk joined by one line
    that carries one red speech mark from the person to the official."""
    p = P()
    person = C.person(p, 36, 124, k=1.0)
    off = official_at_desk(p, 190, 96, k=0.8, plate=True)
    link = [p.line(66, 96, 94, 96), p.line(130, 96, 150, 96)]
    mark = [speech_mark(p, 112, 92, tail="left")]
    return [("base", person + off + link), ("accent", mark)]


def contact_b():
    """Dustin's very simple phone, with the one part that names the
    official: its cord runs to an official at a desk. The cord is the red, the
    one line that carries the call; rays over the phone read as an alarm bell
    and a red handset as hanging up, so neither is used."""
    p = P()
    phone = desk_phone(p, 46, 124)
    cord = [p.path([("M", 72, 118), ("Q", 96, 134, 112, 116), ("Q", 126, 100, 150, 108)])]
    off = official_at_desk(p, 190, 96, k=0.8, plate=True)
    return [("base", phone + off), ("accent", cord)]


def contact_c():
    """The message alone: an official at a desk with a nameplate, and one red
    speech mark arriving from the reader's side, its tail pointing back out
    of the picture to whoever speaks."""
    p = P()
    off = official_at_desk(p, 130, 104, k=0.86, half=40, plate=True)
    mark = [speech_mark(p, 52, 56, w=44, h=32, tail="left")]
    return [("base", off), ("accent", mark)]


REGISTRY = [
    ("Testify", "Testify", "A", "new", testify_a, None,
     "A raised, curved dais with three officials above the witness, who sits at a table with a red microphone."),
    ("Testify", "Testify", "B", "new", testify_b, None,
     "Seen from the side: the witness at a low table with a red microphone, facing three officials at a tall bench on a step."),
    ("Testify", "Testify", "C", "new", testify_c, None,
     "The raised, curved dais with three officials, and the red microphone on the witness table; the reader is the witness."),
    ("Contact-An-Official", "Contact-An-Official", "A", "new", contact_a, None,
     "A person and an official at a desk, joined by one line that carries a red speech mark."),
    ("Contact-An-Official", "Contact-An-Official", "B", "new", contact_b, None,
     "A very simple phone whose red cord runs to an official at a desk."),
    ("Contact-An-Official", "Contact-An-Official", "C", "new", contact_c, None,
     "An official at a desk with a nameplate, and one red speech mark arriving from the reader's side."),
]
