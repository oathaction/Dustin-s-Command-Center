"""Concept 3, Public sign: the ten display masters (design director, Phase 2 round two).

Oath & Action's subjects drawn in the tradition of public information symbols. People and objects
are built from one bar (3 units, round ends) on the shared 24-unit grid, with lines at 0, 45 and
90 degrees and curves taken from circles. Charcoal names the thing. One red stroke at bar width,
the accent, shows what happens: the verb.

Family rules, as drawn:
  bar      3 units, round ends, round joins (outer corner radius 1.5, inner corner sharp)
  head     a disc 4.5 across, 1.5 above the body; figures carry no hands, feet, faces or gender cues
  node     a disc 4.5 across on the horizontal center line in the four pillar marks
  gap      1.5 units, the family's one gap: head to body, part to part, ink to red
  red      one stroke or arrowhead at bar width; it floats one gap off the ink, so removing it
           leaves the drawing whole. Two exceptions, each because the verb is a contact: Connect's
           bridge lands on both halves, and Ballot's check sits on the paper, where red on
           Charcoal measures 4.49:1
  never    red on a figure (Rule 01.1); red plus shapes; domes, columns, flags, scales, seals, stars

Each drawing returns {"ink": path, "accent": path}. Coordinates are in grid units; straight bar
centerlines sit on half units so 3 px bars land on whole pixels at 24 px.
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from icons_r2_sign_geom import (BAR, GAP, HEAD, NODE, arc, arrowhead, bar, box, chevron, circle, disc,  # noqa: E402,F401
                                empty, intersect, minus, on_arc, path, rect, rot, solid, union)

ICONS = ["explain", "track", "connect", "act", "ballot", "bill", "testify", "housing", "money", "loop"]
LABELS = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
          "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign money",
          "loop": "Feedback loop"}
FILE_NAME = {"explain": "Explain", "track": "Track", "connect": "Connect", "act": "Act", "ballot": "Ballot",
             "bill": "Bill", "testify": "Testify", "housing": "Housing", "money": "Campaign-Money",
             "loop": "Feedback-Loop"}
CLASS = {"explain": "Pillar mark", "track": "Pillar mark", "connect": "Pillar mark", "act": "Pillar mark",
         "ballot": "Topic symbol", "bill": "Topic symbol", "testify": "Topic symbol", "housing": "Topic symbol",
         "money": "Topic symbol", "loop": "Atlas symbol"}
# The one-line reason for each icon's red: the verb it shows.
VERB = {
    "explain": "The corner swinging open, so you can see the node inside.",
    "track": "The arrow up the stair: the decision moves to the next stage.",
    "connect": "The bridge across the gap, the ground both halves stand on.",
    "act": "The door's swing, the quarter circle a floor plan draws for a door's path.",
    "ballot": "The check, the stroke a voter makes before the paper goes in.",
    "bill": "The signature line, where a bill becomes law.",
    "testify": "The sound leaving the speaker.",
    "housing": "The door, the way in.",
    "money": "The coin's motion as it leaves the hand.",
    "loop": "The arrowhead that closes the loop.",
}


def explain():
    """A square broken open, its top-right quarter lifted away. The node sits inside on the center
    line. The red arc is the corner's swing, concentric with the node, where the quarter went."""
    cx, cy, h = 11.0, 12.0, 7.5
    body = bar((cx, cy - h), (cx - h, cy - h), (cx - h, cy + h), (cx + h, cy + h), (cx + h, cy))
    node = disc(cx, cy, NODE)
    acc = arc(cx, cy, 9.5, -59, -31)
    return {"ink": union(body, node), "accent": acc}

def track():
    """Three stages on a rising stair, closed by the stair's back. The node is the stage reached, a
    station on the middle nosing at the center line. Red: the arrow up the stair, a public-sign
    arrowhead set in the open corner above the steps."""
    st = bar((3.5, 20.5), (3.5, 17.0), (8.5, 17.0), (8.5, 12.0), (14.0, 12.0), (14.0, 7.0), (20.5, 7.0), (20.5, 20.5))
    node = disc(14.0, 12.0, NODE)
    acc = arrowhead((10.25, 3.0), -45, 4.25, 3.0)
    return {"ink": union(st, node), "accent": acc}

def connect():
    """One circle in two halves held apart. The node is the meeting point; the red bridge spans the
    gap and lands on both halves, under the node."""
    c = circle(12, 12, 10.25)
    gap = 4.5
    L = intersect(c, rect(0, 0, 12 - gap, 24))
    R = intersect(c, rect(12 + gap, 0, 12, 24))
    node = disc(12, 12, NODE)
    acc = minus(rect(12 - gap, 12 - BAR / 2, 2 * gap, BAR), node)
    return {"ink": union(L, R, node), "accent": acc}


def act():
    """A door swung open: lintel and jamb, and the leaf hinged on the left, its top at 45 degrees as
    it turns away. The node is the latch, a station on the jamb at the center line where the door
    meets its frame. Red: the swing, the quarter circle a floor plan draws around a door's hinge."""
    frame = bar((4.5, 3.5), (19.5, 3.5), (19.5, 20.5))
    leaf = solid([(2.0, 6.5), (8.0, 12.5), (8.0, 22.0), (2.0, 22.0)])
    node = disc(19.5, 12.0, NODE)
    acc = arc(2.0, 22.0, 11.5, -33, -15)
    return {"ink": union(frame, leaf, node), "accent": acc}

def ballot():
    """A box with a slot and a marked paper going in. The paper is solid, so the red check sits on
    Charcoal at 4.49:1. Red: the check, the stroke a voter makes."""
    bx = minus(box(3.5, 16.0, 17.0, 5.5), rect(6.5, 14.5, 11.0, 3.0))
    paper = minus(box(7.5, 2.5, 9.0, 14.0, 1.5), rect(0, 16.0, 24, 10))
    acc = bar((10.25, 9.75), (11.0, 10.5), (13.25, 8.25))
    return {"ink": union(bx, paper), "accent": acc}

def bill():
    """A page with a folded corner and lines of text. Red: the signature line, set apart below the
    text where a bill is signed into law."""
    page = bar((12.5, 3.5), (6.5, 3.5), (6.5, 20.5), (17.5, 20.5), (17.5, 8.5), (12.5, 3.5), closed=True)
    lines = union(bar((10.5, 9.5), (11.0, 9.5)), bar((10.5, 13.0), (13.5, 13.0)))
    acc = bar((12.0, 16.75), (13.5, 16.75))
    return {"ink": union(page, lines), "accent": acc}

def testify():
    """A witness seated at a hearing table, speaking into a desk microphone whose stem bends toward
    the face. The person is never red. Red: the sound leaving the speaker, an arc between the face
    and the microphone."""
    head = disc(6.0, 6.25, HEAD)
    body = bar((6.0, 11.5), (6.0, 16.0), (10.5, 16.0), (10.5, 20.5))
    table = bar((10.5, 14.0), (20.5, 14.0), (20.5, 20.5))
    mic = bar((15.0, 14.0), (15.0, 9.0), (13.5, 7.5))
    acc = arc(6.0, 6.25, 5.25, -13, 15)
    return {"ink": union(head, body, table, mic), "accent": acc}

def housing():
    """A house: a pitched roof with a chimney, set one gap above two walls, and a door. Red: the
    door, the way in."""
    roof = bar((3.5, 12.5), (12.0, 4.0), (20.5, 12.5))
    chimney = bar((16.5, 8.0), (16.5, 3.5))
    walls = union(bar((6.5, 14.0), (6.5, 20.5)), bar((17.5, 14.0), (17.5, 20.5)))
    acc = bar((12.0, 18.25), (12.0, 20.5))
    return {"ink": union(roof, chimney, walls), "accent": acc}

def money():
    """A hand and a coin: a cuff, a palm held up with curled fingertips, the thumb set one gap off
    the palm, and a coin tossed up and away. Red: the coin's motion, an arc trailing it on the side
    it came from."""
    cuff = bar((3.5, 13.0), (3.5, 20.5))
    palm = path([("M", 7.0, 20.5), ("L", 14.0, 20.5), ("A", 14.0, 17.0, 3.5, 90, 0)])
    thumb = bar((8.0, 16.5), (10.5, 14.0))
    coin = minus(disc(16.25, 7.0, 9.5), disc(16.25, 7.0, 3.0))
    acc = arc(16.25, 7.0, 7.75, 144, 166)
    return {"ink": union(cuff, palm, thumb, coin), "accent": acc}

def loop():
    """Two nodes joined by two arrowed arcs into a loop, clockwise like the hinge diagram's arcs.
    The nodes are the subject, two bars across, so they sit on the arcs' circle; each arc leaves
    one node a gap clear and its arrowhead stops a gap short of the next. Red: the arrowhead that
    closes the loop."""
    r, nd, hl, hh = 7.25, 6.0, 4.5, 3.1
    a = disc(12 - r, 12, nd)
    b = disc(12 + r, 12, nd)
    start = math.degrees((nd / 2 + GAP + BAR / 2) / r)     # arc's round end a gap clear of the node
    tip = math.degrees((nd / 2 + GAP) / r)                  # arrowhead tip a gap short of the node
    into = math.degrees(hl * 0.7 / r)                       # the arc runs into the arrowhead's base

    def head(theta):
        return arrowhead(on_arc(12, 12, r, theta), theta + 90 + 9, hl, hh)
    top = arc(12, 12, r, 180 + start, 360 - tip - into)
    bot = arc(12, 12, r, start, 180 - tip - into)
    return {"ink": union(a, b, top, bot, head(360 - tip)), "accent": head(180 - tip)}

DRAW = {n: globals()[n] for n in ICONS}


def display(name):
    """The display master for 48 px and up: the 24-unit drawing, unhinted."""
    return DRAW[name]()
