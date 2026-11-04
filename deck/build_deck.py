"""Build the Insight Global "Healthcare AI Solution Blueprints" deck (python-pptx).

Usage:
    python3 deck/extract_assets.py <PowerPoint_Template.pdf>   # once, creates deck/assets/
    python3 deck/build_deck.py [--icons <lucide-static/icons dir>]

Icons are Lucide SVGs rendered to PNG by deck/make_icons.js. Rendered icons live in
deck/assets/icons/. If any icon is missing and --icons is given, they are rendered and
the deck is rebuilt automatically.
"""
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

import content as C

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
ICONS = ASSETS / "icons"
LOGOS = ASSETS / "logos"
OUT = HERE / "IG_Healthcare_AI_Solution_Blueprints.pptx"

# Brand (from the Insight Global template user guide)
FONT = "Trenda IG Text"
FONT_LIGHT = "Trenda IG Text Light"
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
YELLOW = RGBColor(0xFF, 0xD2, 0x00)
CYAN = RGBColor(0x00, 0xD3, 0xF2)
MAGENTA = RGBColor(0xFF, 0x0A, 0x6C)
PURPLE = RGBColor(0x5B, 0x2A, 0xA0)
GREEN = RGBColor(0x5B, 0xE4, 0x4A)
ORANGE = RGBColor(0xFF, 0x8A, 0x33)
LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
MID = RGBColor(0xE2, 0xE2, 0xE2)
GRAY = RGBColor(0x5F, 0x5F, 0x5F)
SOFT = RGBColor(0xBF, 0xBF, 0xBF)
ACCENTS = {"cyan": CYAN, "magenta": MAGENTA, "yellow": YELLOW, "purple": PURPLE, "green": GREEN, "orange": ORANGE}
# Darker tints for icons / text on white backgrounds (contrast)
ON_WHITE = {CYAN: "00A3C4", YELLOW: "C99A00", GREEN: "23A41A", MAGENTA: "FF0A6C", PURPLE: "5B2AA0",
            ORANGE: "E86A12", BLACK: "000000", GRAY: "5F5F5F"}
SPOKE_COLORS = [CYAN, MAGENTA, YELLOW, PURPLE, GREEN, ORANGE, CYAN, MAGENTA]

W, H = 13.333, 7.5
ML = 0.6  # left margin (in)

MISSING_ICONS = set()


def hexof(c):
    return str(c)


def on_white(c):
    return ON_WHITE.get(c, hexof(c))


def ink_on(c):
    """Icon/text color to put on top of a filled accent."""
    return BLACK if c in (CYAN, YELLOW, GREEN, ORANGE) else WHITE


# ----------------------------------------------------------------------------- helpers
def est_lines(text, size, width_in):
    cpl = max(1.0, width_in * 72 / (size * 0.48) * 0.93)
    return max(1, math.ceil(len(text) / cpl))


def text_h(text, size, width_in, spacing=1.18):
    return est_lines(text, size, width_in) * size * spacing / 72


def _font(r, size, color, bold=False, light=False, italic=False, tracking=None):
    f = r.font
    f.name = FONT_LIGHT if light else FONT
    f.size = Pt(size)
    f.bold = bold
    f.italic = italic
    f.color.rgb = _rgb(color)
    if tracking:
        r._r.get_or_add_rPr().set("spc", str(int(tracking * 100)))


def _rgb(c):
    return RGBColor.from_string(c) if isinstance(c, str) else c


def _box(slide, x, y, w, h, anchor):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    return box, tf


def tb(slide, x, y, w, h, text, size=14, color=BLACK, bold=False, light=False, italic=False,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, tracking=None, line=1.08):
    box, tf = _box(slide, x, y, w, h, anchor)
    lines = text if isinstance(text, list) else [text]
    for i, t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line
        r = p.add_run()
        r.text = t
        _font(r, size, color, bold, light, italic, tracking)
    return box


def rich(slide, x, y, w, h, runs, size=14, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, line=1.08):
    """runs: list of (text, color, bold)."""
    box, tf = _box(slide, x, y, w, h, anchor)
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line
    for text, color, bold in runs:
        r = p.add_run()
        r.text = text
        _font(r, size, color, bold)
    return box


def _nostyle(shape):
    style = shape._element.find(qn("p:style"))
    if style is not None:
        shape._element.remove(style)


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(line_w)
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    s.shadow.inherit = False
    _nostyle(s)
    return s


def rbox(slide, x, y, w, h, fill=WHITE, line=MID, line_w=1.0, radius=0.12):
    return rect(slide, x, y, w, h, fill=fill, line=line, line_w=line_w, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=radius)


def oval(slide, x, y, d, fill=None, line=None, line_w=1.25):
    return rect(slide, x, y, d, d, fill=fill, line=line, line_w=line_w, shape=MSO_SHAPE.OVAL)


def connector(slide, x1, y1, x2, y2, color, width=1.0, dash=False, arrow=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = 3  # round dot
    if arrow:
        ln = c.line._get_or_add_ln()
        tail = etree.SubElement(ln, qn("a:tailEnd"))
        tail.set("type", "triangle")
        tail.set("w", "med")
        tail.set("h", "med")
    return c


def hline(slide, x1, y, x2, color, width=1.0, dash=False):
    return connector(slide, x1, y, x2, y, color, width, dash)


def vline(slide, x, y1, y2, color, width=1.0, dash=False):
    return connector(slide, x, y1, x, y2, color, width, dash)


def tri_right(slide, x, y, color=GRAY, w=0.12, h=0.18):
    t = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    t.rotation = 90
    t.fill.solid()
    t.fill.fore_color.rgb = color
    t.line.fill.background()
    _nostyle(t)


def pill(slide, x, y, text, color, size=11, h=0.32, fill=None, text_color=None):
    w = len(text) * size * 0.56 / 72 + 0.36
    rect(slide, x, y, w, h, fill=fill, line=color, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tb(slide, x, y, w, h, text, size=size, color=text_color or color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return x + w + 0.12


def icon(slide, name, color, x, y, size):
    """Place a Lucide icon PNG. color: RGBColor or hex string."""
    hx = color if isinstance(color, str) else hexof(color)
    path = ICONS / f"{name}-{hx}.png"
    if not path.exists():
        MISSING_ICONS.add((name, hx))
        return None
    return slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(size), Inches(size))


SF_PRODUCTS = ("Cloud", "Agentforce", "Tableau", "MuleSoft", "Salesforce")


def logo(slide, key, x, y, h):
    """Place a vendor logo (deck/assets/logos/<key>.png) at height h; returns its width."""
    from PIL import Image
    path = LOGOS / f"{key}.png"
    w_px, h_px = Image.open(path).size
    w = h * w_px / h_px
    slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    return w


def is_salesforce(label):
    return any(k in label for k in SF_PRODUCTS) and "Any cloud" not in label


def logo_pill(slide, x, y, text, color, size=11, h=0.32, key="salesforce"):
    """Pill with a vendor logo on the left."""
    lh = h - 0.1
    from PIL import Image
    w_px, h_px = Image.open(LOGOS / f"{key}.png").size
    lw = lh * w_px / h_px
    w = len(text) * size * 0.56 / 72 + 0.36 + lw + 0.08
    rect(slide, x, y, w, h, line=color, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    logo(slide, key, x + 0.14, y + 0.05, lh)
    tb(slide, x + 0.14 + lw + 0.06, y, w - lw - 0.3, h, text, size=size, color=color, anchor=MSO_ANCHOR.MIDDLE)
    return x + w + 0.12


class Deck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(W)
        self.prs.slide_height = Inches(H)
        self.n = 0

    def slide(self, bg=None, fill=None):
        s = self.prs.slides.add_slide(self.prs.slide_layouts[6])
        self.n += 1
        if bg:
            s.shapes.add_picture(str(ASSETS / bg), 0, 0, Inches(W), Inches(H))
        elif fill is not None:
            rect(s, 0, 0, W, H, fill=fill)
        return s

    def chrome(self, s, label=C.DECK_LABEL, dark=True, num_dark=None):
        col = WHITE if dark else BLACK
        tb(s, ML, 0.3, 12, 0.25, label, size=8, bold=True, color=col, tracking=2.2)
        # the template's real ●●●IG footer mark (extracted from the template PDF)
        mark = ASSETS / ("ig_mark_white.png" if dark else "ig_mark_black.png")
        s.shapes.add_picture(str(mark), Inches(0.553), Inches(7.05), Inches(0.537), Inches(0.108))
        nd = dark if num_dark is None else num_dark
        tb(s, W - 1.1, 7.07, 0.5, 0.22, str(self.n), size=9, color=WHITE if nd else BLACK, align=PP_ALIGN.RIGHT)

    @staticmethod
    def notes(s, text):
        s.notes_slide.notes_text_frame.text = text


def bnum(p):
    return f"{C.PLATFORMS.index(p) + 1:02d}"


def plabel(p):
    return f"BLUEPRINT {bnum(p)} · {p['name'].upper()} · {p['domain'].upper()}"


# ----------------------------------------------------------------------------- front slides
def title_slide(d):
    s = d.slide(bg="bg_title.png")
    tb(s, 1, 2.55, W - 2, 1.6, ["HEALTHCARE AI", "SOLUTION BLUEPRINTS"], size=42, light=True, color=WHITE,
       align=PP_ALIGN.CENTER, tracking=6, line=1.0)
    tb(s, 1, 4.35, W - 2, 0.5, "Six knowledge-graph blueprints across healthcare and enterprise governance", size=18, color=WHITE,
       align=PP_ALIGN.CENTER)
    tb(s, 1, 6.55, W - 2, 0.3, f"IGH PRESIDENT BRIEFING  ·  {C.DECK_DATE}", size=11, color=WHITE,
       align=PP_ALIGN.CENTER, tracking=4)
    d.notes(s, "Purpose: show what our core team can do in healthcare, and give account managers and sales six clear "
               "solution blueprints (CareGraph, TherapyGraph, RxGraph, DeviceGraph, ChainGraph, ShieldGraph) to start conversations.\n\n"
               "Blueprints, not case studies: all six are proposed solutions at ideation stage: problem, solution, architecture and value. Figures marked 'Pilot target' are agreed "
               "with each client; sourced figures are public evidence.")


def agenda_slide(d):
    s = d.slide(bg="bg_dark_magenta.jpg")
    d.chrome(s)
    tb(s, ML, 0.75, 6, 0.8, "Agenda", size=40, bold=True, color=WHITE)
    items = [("Who we are", None), ("Universal architecture", None)] + \
            [(p["name"], p["domain"]) for p in C.PLATFORMS] + [("How we engage", None)]
    for i, (it, sub) in enumerate(items):
        col, row = divmod(i, 5)
        x, y = ML + col * 6.3, 1.85 + row * 0.92
        oval(s, x, y, 0.5, line=WHITE, line_w=1.5)
        tb(s, x, y, 0.5, 0.5, str(i + 1), size=15, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        if sub:
            rich(s, x + 0.72, y, 5.5, 0.5, [(it, WHITE, True), ("  ·  " + sub, SOFT, False)], size=18,
                 anchor=MSO_ANCHOR.MIDDLE)
        else:
            tb(s, x + 0.72, y, 5.5, 0.5, it, size=22, light=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, "One universal architecture, then six solution blueprints, one per domain, each in three slides: problem and solution, "
               "the blueprint on the universal architecture, value. "
               "We close with how we engage and a cheat sheet for sales.")


def who_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "A core team built for any healthcare requirement", size=32, bold=True)
    tb(s, ML, 1.45, 12, 0.4, "From strategy to production across AI, data, Salesforce and cloud, with healthcare compliance built in.",
       size=16, color=GRAY)
    cols = [CYAN, YELLOW, MAGENTA, PURPLE, GREEN, ORANGE]
    icons = ["bot", "network", "cloud", "server", "shield-check", "workflow"]
    tw, th, gx, gy = 3.93, 1.84, 0.17, 0.12
    for i, (t, desc) in enumerate(C.CAPABILITIES):
        c, r = i % 3, i // 3
        x, y = ML + c * (tw + gx), 2.1 + r * (th + gy)
        rect(s, x, y, tw, th, fill=LIGHT)
        oval(s, x + 0.25, y + 0.2, 0.5, fill=cols[i])
        icon(s, icons[i], ink_on(cols[i]), x + 0.36, y + 0.31, 0.28)
        tb(s, x + 0.25, y + 0.72, tw - 0.5, 0.5, t, size=16, bold=True, line=1.0, anchor=MSO_ANCHOR.BOTTOM)
        tb(s, x + 0.25, y + 1.28, tw - 0.5, 0.55, desc, size=11.5, color=GRAY)
        if i == 2:
            logo(s, "salesforce", x + tw - 0.25 - 0.62, y + 0.2, 0.44)
        if i == 3:
            lx_ = x + tw - 0.25
            for key, hh in (("azure", 0.38), ("aws", 0.3), ("googlecloud", 0.38)):
                from PIL import Image
                wpx, hpx = Image.open(LOGOS / f"{key}.png").size
                lx_ -= hh * wpx / hpx
                logo(s, key, lx_, y + 0.22 + (0.38 - hh) / 2, hh)
                lx_ -= 0.15
    rect(s, ML, 6.15, W - 2 * ML, 0.68, fill=BLACK)
    tb(s, ML + 0.25, 6.15, 1.5, 0.68, "PROOF POINT", size=10, bold=True, color=YELLOW, tracking=2, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, ML + 1.75, 6.15, W - 2 * ML - 2.0, 0.68, C.PROOF_POINT, size=12.5, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, "Key message: one core team covers every layer a healthcare AI program needs, so we can take any requirement "
               "from idea to production.\n\nThe proof point is our current delivery for a large US health system "
               "(client name withheld; use it verbally only if cleared).")


def five_graphs_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "Six blueprints, one architecture", size=32, bold=True)
    tb(s, ML, 1.42, 12, 0.4, "Each blueprint is built around one central entity and solves the whole set of problems in its domain.",
       size=15, color=GRAY)
    gap = 0.12
    cw = (W - 2 * ML - gap * (len(C.PLATFORMS) - 1)) / len(C.PLATFORMS)
    for i, p in enumerate(C.PLATFORMS):
        x = ML + i * (cw + gap)
        acc = ACCENTS[p["accent"]]
        rect(s, x, 2.1, cw, 4.65, fill=LIGHT)
        rect(s, x, 2.1, cw, 0.07, fill=acc)
        oval(s, x + 0.18, 2.4, 0.78, fill=acc)
        icon(s, p["icon"], ink_on(acc), x + 0.37, 2.59, 0.4)
        tb(s, x + 1.06, 2.58, cw - 1.1, 0.5, f"BLUEPRINT\n{bnum(p)}".split("\n"), size=8, bold=True, color=GRAY, tracking=1.0, line=1.0)
        tb(s, x + 0.18, 3.35, cw - 0.25, 0.4, p["name"], size=18, bold=True)
        dh = text_h(p["domain"].upper(), 8, cw - 0.25, 1.1) + 0.05
        tb(s, x + 0.18, 3.74, cw - 0.25, dh, p["domain"].upper(), size=8, bold=True, color=GRAY, tracking=1.0, line=1.0)
        rich(s, x + 0.18, 4.22, cw - 0.25, 0.3, [("Center: ", GRAY, False), (p["center"][0], BLACK, True)], size=10.5)
        y = 4.62
        for title, _ in p["modules"]:
            icon(s, "circle-check", on_white(acc), x + 0.18, y + 0.02, 0.16)
            h = text_h(title, 10, cw - 0.58)
            tb(s, x + 0.41, y, cw - 0.5, h, title, size=10)
            y += h + 0.06
    d.notes(s, "The six blueprints at a glance. Pick the blueprint that matches the client in front of you: provider or payer → CareGraph; "
               "pharma commercial or clinical → TherapyGraph; pharmacy, PBM or patient hub → RxGraph; MedTech or virtual care → DeviceGraph; "
               "manufacturing, CDMO or distribution → ChainGraph; any organization facing SOX / HIPAA audits or access sprawl → ShieldGraph.")


# ----------------------------------------------------------------------------- blueprint slides
def problem_slide(d, p):
    s = d.slide(fill=WHITE)
    rect(s, W / 2, 0, W / 2, H, fill=BLACK)
    d.chrome(s, label=plabel(p), dark=False, num_dark=True)
    acc = ACCENTS[p["accent"]]
    lw = W / 2 - ML - 0.45
    tb(s, ML, 0.7, lw, 0.25, "THE PROBLEM", size=10, bold=True, color=MAGENTA, tracking=2.2)
    th = text_h(p["headline"], 21, lw, 1.1)
    tb(s, ML, 0.98, lw, th, p["headline"], size=21, bold=True, line=1.0)
    y = 0.98 + th + 0.15
    h = text_h(p["problem"], 12.5, lw)
    tb(s, ML, y, lw, h, p["problem"], size=12.5)
    y += h + 0.08
    who = "Who feels it: " + p["who"]
    h = text_h(who, 10.5, lw)
    tb(s, ML, y, lw, h, who, size=10.5, italic=True, color=GRAY)
    y += h + 0.22
    tb(s, ML, y, lw, 0.25, "PROBLEMS IT SOLVES", size=10, bold=True, color=MAGENTA, tracking=2.2)
    y += 0.34
    cw = (lw - 0.2) / 2
    pitch = 0.74
    for i, (ic, title, desc) in enumerate(p["problems"]):
        c, r = i % 2, i // 2
        x, yy = ML + c * (cw + 0.2), y + r * pitch
        oval(s, x, yy, 0.42, fill=LIGHT)
        icon(s, ic, on_white(MAGENTA), x + 0.09, yy + 0.09, 0.24)
        t_h = text_h(title, 11.5, cw - 0.55, 1.1)
        tb(s, x + 0.52, yy - 0.01, cw - 0.55, t_h, title, size=11.5, bold=True, line=1.0)
        tb(s, x + 0.52, yy + t_h + 0.01, cw - 0.55, 0.4, desc, size=10, color=GRAY, line=1.0)
    # evidence callout: published research or another organization's reported result
    big, txt, src = p["evidence"]
    fy = y + 3 * pitch + 0.08
    hline(s, ML, fy, ML + lw, BLACK, 0.75, dash=True)
    tb(s, ML, fy + 0.08, 2, 0.22, "EVIDENCE FROM THE FIELD", size=8, bold=True, color=GRAY, tracking=1.5)
    bw = max(0.6, len(big) * 26 * 0.55 / 72 + 0.25)
    tb(s, ML, fy + 0.3, bw, 0.5, big, size=26, light=True, color=MAGENTA)
    th_ = text_h(txt, 11, lw - bw - 0.1) * 1.12
    tb(s, ML + bw + 0.1, fy + 0.32, lw - bw - 0.1, th_, txt, size=11)
    tb(s, ML + bw + 0.1, fy + 0.34 + th_, lw - bw - 0.1, 0.22, "Source: " + src, size=9, italic=True, color=GRAY)

    rx, rw = W / 2 + 0.55, W / 2 - 1.15
    tb(s, rx, 0.7, rw, 0.3, "OUR SOLUTION", size=10, bold=True, color=CYAN, tracking=2.2)
    rect(s, rx, 1.02, 0.62, 0.62, fill=acc, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    icon(s, p["icon"], ink_on(acc), rx + 0.13, 1.15, 0.36)
    tb(s, rx + 0.8, 0.98, rw - 0.8, 0.5, p["name"], size=30, bold=True, color=WHITE)
    tb(s, rx + 0.8, 1.48, rw - 0.8, 0.3, p["promise"], size=12, color=SOFT)
    h = text_h(p["definition"], 14, rw)
    tb(s, rx, 1.95, rw, h, p["definition"], size=14, color=WHITE)
    y = 1.95 + h + 0.28
    for title, desc in p["modules"]:
        oval(s, rx, y + 0.07, 0.11, fill=acc if acc != PURPLE else MAGENTA)
        txt = title + "  " + desc
        hh = text_h(txt, 12.5, rw - 0.3) * 1.05
        rich(s, rx + 0.3, y, rw - 0.3, hh, [(title, WHITE, True), ("  " + desc, SOFT, False)], size=12.5)
        y += hh + 0.13
    by = max(y + 0.12, 5.85)
    tb(s, rx, by, rw, 0.25, "BUILT ON", size=9, bold=True, color=SOFT, tracking=2)
    x, yy = rx, by + 0.3
    for b in p["built_on"]:
        sf = is_salesforce(b)
        wpill = len(b) * 11 * 0.56 / 72 + 0.36 + (0.4 if sf else 0)
        if x + wpill > rx + rw:
            x, yy = rx, yy + 0.4
        x = logo_pill(s, x, yy, b, WHITE, size=11) if sf else pill(s, x, yy, b, WHITE, size=11)
    d.notes(s, "PRESIDENT CUT: present this blueprint.\n\nTalk track: " + p["talk"])


def panel(s, x, y, w, h, title, sub, ic, acc):
    rbox(s, x, y, w, h, fill=WHITE, line=SOFT, line_w=1.0, radius=0.04)
    rect(s, x + 0.02, y + 0.02, w - 0.04, 0.58, fill=LIGHT)
    icon(s, ic, on_white(acc), x + 0.14, y + 0.17, 0.28)
    tb(s, x + 0.5, y + 0.08, w - 0.56, 0.24, title, size=10, bold=True, tracking=0.6)
    tb(s, x + 0.5, y + 0.33, w - 0.56, 0.22, sub, size=8.5, color=GRAY)


ARCH_LAYERS = [("DATA FOUNDATION", "Sources we connect", "database"),
               ("DATA READINESS", "Matching, masking, codes", "shield-check"),
               ("INTELLIGENCE CORE", "The {model} model", "network"),
               ("AGENTIC WORKFLOWS", "Agents + where users see it", "bot")]
ARCH_TOP, ARCH_PH, ARCH_GAP = 1.55, 4.38, 0.16
ARCH_WIDTHS = [2.45, 2.07, 3.83, 3.3]


def hub(s, cx, cy, center_label, center_icon, spokes, acc, rx_=1.38, ry_=1.08, sd=0.84, cd=1.08):
    """Hub-and-spoke graph. spokes: list of (label or [lines], icon, color)."""
    n = len(spokes)
    pos = []
    for k in range(n):
        a = math.radians(-90 + k * 360 / n)
        pos.append((cx + rx_ * math.cos(a), cy + ry_ * math.sin(a)))
    for px, py in pos:
        connector(s, cx, cy, px, py, SOFT, 1.25)
    oval(s, cx - cd / 2, cy - cd / 2, cd, fill=acc)
    icon(s, center_icon, ink_on(acc), cx - 0.19, cy - 0.38, 0.38)
    tb(s, cx - cd / 2 + 0.05, cy + 0.02, cd - 0.1, 0.4, center_label, size=10, bold=True, color=ink_on(acc),
       align=PP_ALIGN.CENTER, line=0.95)
    for (lab, ic, col), (px, py) in zip(spokes, pos):
        oval(s, px - sd / 2, py - sd / 2, sd, fill=WHITE, line=col, line_w=2.0)
        icon(s, ic, on_white(col), px - 0.13, py - 0.33, 0.26)
        tb(s, px - sd / 2 + 0.04, py - 0.04, sd - 0.08, 0.38, lab, size=7.5, bold=True, align=PP_ALIGN.CENTER, line=0.95)


def arch_body(s, acc, model, sources, prepare, standards, center, spokes, crew_title, crew_sub, crew, outputs,
              strip_label, strip_items):
    """The four business layers + bottom strip, shared by the universal and the blueprint architecture slides."""
    acc_w = on_white(acc)
    top, ph, gap, widths = ARCH_TOP, ARCH_PH, ARCH_GAP, ARCH_WIDTHS
    xs = [ML]
    for wdt in widths[:-1]:
        xs.append(xs[-1] + wdt + gap)
    for i, ((t, sub, ic), x, wdt) in enumerate(zip(ARCH_LAYERS, xs, widths)):
        panel(s, x, top, wdt, ph, t, sub.format(model=model), ic, acc)
        if i < 3:
            tri_right(s, x + wdt + 0.035, top + ph / 2 - 0.09, GRAY)

    # data foundation
    x, wdt = xs[0], widths[0]
    y = top + 0.72
    for k, src in enumerate(sources):
        name, desc, ic = src[:3]
        key = src[3] if len(src) > 3 else None
        rbox(s, x + 0.12, y, wdt - 0.24, 0.55)
        if key:
            from PIL import Image
            wpx, hpx = Image.open(LOGOS / f"{key}.png").size
            lh_ = min(0.29, 0.34 * hpx / wpx)
            logo(s, key, x + 0.2, y + 0.275 - lh_ / 2, lh_)
        else:
            icon(s, ic, on_white(SPOKE_COLORS[k % 6]), x + 0.22, y + 0.13, 0.29)
        tb(s, x + 0.62, y + 0.05, wdt - 0.8, 0.24, name, size=9.5, bold=True)
        tb(s, x + 0.62, y + 0.27, wdt - 0.8, 0.28, desc, size=8.5, color=GRAY, line=1.0)
        y += 0.6

    # data readiness
    x, wdt = xs[1], widths[1]
    y = top + 0.74
    for k, (ic, step) in enumerate(prepare):
        rbox(s, x + 0.12, y, wdt - 0.24, 0.8)
        icon(s, ic, on_white(SPOKE_COLORS[k]), x + wdt / 2 - 0.14, y + 0.08, 0.28)
        tb(s, x + 0.16, y + 0.4, wdt - 0.32, 0.38, step, size=9, bold=True, align=PP_ALIGN.CENTER, line=1.0)
        y += 0.9

    # intelligence core
    x, wdt = xs[2], widths[2]
    chips_w = sum(len(st) * 8.5 * 0.56 / 72 + 0.36 for st in standards) + 0.06 * len(standards)
    if chips_w <= wdt - 0.95 - 0.12:
        tb(s, x + 0.14, top + 0.72, 0.85, 0.3, "Standards", size=8.5, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
        cxp = x + 0.95
    else:
        cxp = x + 0.14
    for st in standards:
        cxp = pill(s, cxp, top + 0.72, st, _rgb(acc_w), size=8.5, h=0.28) - 0.06
    hub(s, x + wdt / 2, top + 1.12 + (ph - 1.12) / 2, center[0], center[1], spokes, acc)

    # agentic workflows
    x, wdt = xs[3], widths[3]
    lx, lwid = x + 0.12, 1.74
    ox, owid = x + wdt - 0.12 - 1.18, 1.18
    y0 = top + 0.72
    rbox(s, lx, y0, lwid, 0.62)
    icon(s, "lock", acc_w, lx + 0.1, y0 + 0.16, 0.28)
    tb(s, lx + 0.46, y0 + 0.07, lwid - 0.5, 0.26, "Secure access", size=10, bold=True)
    tb(s, lx + 0.46, y0 + 0.32, lwid - 0.5, 0.26, "APIs · MCP tools", size=8.5, color=GRAY)
    ay, ah = y0 + 0.74, 2.05
    rbox(s, lx, ay, lwid, ah, line=acc, line_w=1.5)
    icon(s, "bot", acc_w, lx + 0.1, ay + 0.12, 0.3)
    tb(s, lx + 0.46, ay + 0.08, lwid - 0.5, 0.26, crew_title, size=10, bold=True)
    tb(s, lx + 0.46, ay + 0.32, lwid - 0.5, 0.26, crew_sub, size=8.5, color=GRAY)
    yy = ay + 0.68
    for ag in crew:
        oval(s, lx + 0.16, yy + 0.07, 0.07, fill=acc if acc != YELLOW else ORANGE)
        tb(s, lx + 0.32, yy, lwid - 0.38, 0.26, ag, size=9)
        yy += 0.26
    gy = ay + ah + 0.1
    rbox(s, lx, gy, lwid, 0.66, line=YELLOW, line_w=1.5)
    icon(s, "shield-check", on_white(YELLOW), lx + 0.1, gy + 0.18, 0.28)
    tb(s, lx + 0.45, gy + 0.05, lwid - 0.5, 0.2, "Trust layer", size=8.5, bold=True)
    tb(s, lx + 0.45, gy + 0.24, lwid - 0.5, 0.4, C.GOVERNANCE_LINE, size=7.5, color=GRAY, line=1.0)
    oh, og = 0.98, 0.26
    oy = y0 + 0.2
    for k, (lab, ic) in enumerate(outputs):
        by = oy + k * (oh + og)
        rbox(s, ox, by, owid, oh)
        if is_salesforce(lab):
            logo(s, "salesforce", ox + owid / 2 - 0.23, by + 0.1, 0.32)
        else:
            icon(s, ic, on_white(SPOKE_COLORS[k]), ox + owid / 2 - 0.16, by + 0.1, 0.32)
        tb(s, ox + 0.06, by + 0.48, owid - 0.12, 0.46, lab, size=9, bold=True, align=PP_ALIGN.CENTER, line=1.0)
        connector(s, lx + lwid, ay + 0.45 + k * 0.6, ox, by + oh / 2, GRAY, 1.0, arrow=True)

    # bottom strip
    cy0 = top + ph + 0.15
    rect(s, ML, cy0, W - 2 * ML, 0.66, fill=LIGHT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.18)
    rect(s, ML + 0.08, cy0 + 0.08, 1.3, 0.5, fill=BLACK, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.3)
    tb(s, ML + 0.08, cy0 + 0.08, 1.3, 0.5, strip_label, size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
       anchor=MSO_ANCHOR.MIDDLE)
    iw = (W - 2 * ML - 1.55) / len(strip_items)
    for k, item in enumerate(strip_items):
        lab, ic = item[0], item[1]
        key = item[2] if len(item) > 2 else None
        ix = ML + 1.55 + k * iw
        if key:
            lw_ = logo(s, key, ix, cy0 + 0.15, 0.36 if key != "aws" else 0.3)
        else:
            icon(s, ic, on_white(SPOKE_COLORS[k % 6]), ix, cy0 + 0.18, 0.3)
            lw_ = 0.3
        tb(s, ix + lw_ + 0.1, cy0 + 0.06, iw - lw_ - 0.15, 0.54, lab, size=9.5, bold=True, anchor=MSO_ANCHOR.MIDDLE, line=1.0)


def arch_header(s, title, promise, tile_fill, tile_icon, promise_color):
    rect(s, ML, 0.6, 0.62, 0.62, fill=tile_fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.2)
    icon(s, tile_icon, ink_on(tile_fill), ML + 0.13, 0.73, 0.36)
    name_w = len(title) * 28 * 0.6 / 72 + 0.25
    tb(s, ML + 0.8, 0.55, name_w, 0.5, title, size=28, bold=True)
    tb(s, ML + 0.8 + name_w, 0.66, 12.0 - name_w, 0.4, promise, size=18, light=True, color=promise_color)


def universal_arch_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, label=C.DECK_LABEL + " · UNIVERSAL ARCHITECTURE", dark=False)
    U = C.UNIVERSAL
    arch_header(s, "Universal architecture", U["promise"], BLACK, "network", on_white(MAGENTA))
    tb(s, ML + 0.8, 1.08, 11.8, 0.3, U["subtitle"], size=12, color=GRAY)
    spokes = [([p["center"][0], p["name"]], p["center"][1], ACCENTS[p["accent"]]) for p in C.PLATFORMS]
    arch_body(s, MAGENTA, "domain", U["sources"], U["prepare"], U["standards"], ("Central entity", "network"), spokes,
              "AI agent crew", "model-agnostic", U["agent_skills"], U["outputs"], "Runs on", U["runs_on"])
    d.notes(s, "This is the one architecture behind every blueprint. Four layers: data foundation (what we connect), data readiness "
               "(match identities, map to standard codes, mask PHI, make documents searchable), intelligence core (a domain model with "
               "one central entity: Patient, Therapy, Medication, Device or Product lot), and agentic workflows (an agent crew that plans, "
               "retrieves, drafts, checks and hands off to a person, delivering into Salesforce, dashboards and plain-English questions). "
               "The trust layer covers everything. Because the architecture is shared, a new blueprint reuses about 80% of the build; "
               "only the data, the central entity and the agents change. It runs on Google Cloud, AWS or Azure, with any LLM.")


def arch_slide(d, p):
    s = d.slide(fill=WHITE)
    d.chrome(s, label=plabel(p) + " · ON THE UNIVERSAL ARCHITECTURE", dark=False)
    acc = ACCENTS[p["accent"]]
    arch_header(s, p["name"], p["promise"], acc, p["icon"], on_white(acc))
    # layer ribbon: ties this slide back to the universal architecture
    tb(s, ML + 0.8, 1.06, 2.3, 0.3, "On the universal architecture:", size=10.5, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    x = ML + 3.0
    for i, (t, _, _) in enumerate(ARCH_LAYERS):
        x = pill(s, x, 1.07, t.title().replace("Ai", "AI"), BLACK, size=9, h=0.28)
        if i < 3:
            tb(s, x - 0.1, 1.06, 0.2, 0.3, "›", size=12, color=GRAY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            x += 0.1
    spokes = [(lab, ic, SPOKE_COLORS[k]) for k, (lab, ic) in enumerate(p["spokes"])]
    outputs = [(f"Ask {p['name']}" if lab == "Ask the graph" else lab, ic) for lab, ic in p["outputs"]]
    arch_body(s, acc, p["name"], p["sources"], p["prepare"], p["standards"], p["center"], spokes,
              "AI agent crew", "model-agnostic", p["agents"], outputs, "Outcomes", p["outcomes"])
    d.notes(s, f"This is {p['name']} on the universal architecture: same four layers, filled with {p['domain'].lower()} content. "
               f"Data foundation: the sources on the left. Data readiness: matching, standard codes, PHI masking and search. "
               f"Intelligence core: the {p['name']} model puts {p['center'][0]} at the center and connects every related entity, so "
               f"answers are grounded and cited. Agentic workflows: the agent crew works through secure access and delivers into "
               f"Salesforce, dashboards and plain-English questions. A person approves anything that matters. "
               f"The outcomes strip is what the client gets.")


def value_slide(d, p):
    s = d.slide(fill=BLACK)
    d.chrome(s, label=plabel(p) + " · VALUE")
    tb(s, ML, 0.62, 8, 0.25, "VALUE & BENEFITS", size=10, bold=True, color=CYAN, tracking=2.2)
    tb(s, ML, 0.92, W - 2 * ML, 1.0, p["value_headline"], size=28, light=True, color=WHITE, line=1.05)
    cw, gap = 2.88, 0.2
    for i, (big, label, src) in enumerate(p["value_stats"]):
        x = ML + i * (cw + gap)
        size = 54 if len(big) <= 5 else (46 if len(big) <= 6 else 40)
        tb(s, x, 2.15, cw, 0.9, big, size=size, light=True, color=CYAN)
        lh = text_h(label, 14, cw - 0.1) * 1.15
        tb(s, x, 3.15, cw - 0.1, lh, label, size=14, color=WHITE)
        cap = "Pilot target (validated in pilot)" if src == "Pilot target" else (src if src.startswith("Design") else "Source: " + src)
        tb(s, x, 3.15 + lh + 0.08, cw - 0.1, 0.4, cap, size=10, italic=True, color=SOFT)
    hline(s, ML, 4.85, W - ML, WHITE, 0.75, dash=True)
    dots = [CYAN, YELLOW, MAGENTA, GREEN]
    for i, (k, v) in enumerate(p["benefits"].items()):
        x = ML + i * (cw + gap)
        oval(s, x, 5.17, 0.13, fill=dots[i])
        tb(s, x + 0.25, 5.08, cw - 0.3, 0.3, k, size=14, bold=True, color=WHITE)
        tb(s, x, 5.5, cw - 0.1, 1.0, v, size=13, color=SOFT)
    q = "\n".join(f"  {n + 1}. {qq}" for n, qq in enumerate(p["questions"]))
    d.notes(s, "Value: ranges marked Pilot target are targets we agree with the client in the ideation workshop and measure in the pilot; numbers with a source are public evidence.\n\n"
               "Discovery questions for account managers:\n" + q)


# ----------------------------------------------------------------------------- close
def engage_slide(d):
    s = d.slide(bg="bg_dark_glow.jpg")
    d.chrome(s)
    tb(s, ML, 0.7, 12, 0.7, "How we engage: from idea to production", size=32, bold=True, color=WHITE)
    ly = 4.0
    hline(s, ML, ly, W - ML, WHITE, 3)
    oval(s, ML - 0.09, ly - 0.09, 0.18, fill=WHITE)
    oval(s, W - ML - 0.09, ly - 0.09, 0.18, fill=WHITE)
    xs = [0.85, 3.85, 6.85, 9.85]
    for i, (t, desc) in enumerate(C.ENGAGEMENT_STEPS):
        x = xs[i]
        name, dur = t.split(" · ")
        top = ly - 1.8 if i % 2 == 0 else ly + 0.2
        if i % 2 == 0:
            vline(s, x, ly - 1.8, ly - 0.15, WHITE, 1.25, dash=True)
        else:
            vline(s, x, ly + 0.15, ly + 1.55, WHITE, 1.25, dash=True)
        tb(s, x + 0.2, top, 2.85, 0.3, name, size=15, bold=True, color=WHITE)
        tb(s, x + 0.2, top + 0.32, 2.85, 0.28, dur.upper(), size=10, bold=True, color=CYAN, tracking=1.5)
        tb(s, x + 0.2, top + 0.65, 2.85, 0.85, desc, size=12.5, color=SOFT)
    tb(s, ML, 6.0, W - 2 * ML, 0.4, "Next step: pick one blueprint and run a 2-week ideation workshop with the client.",
       size=16, color=WHITE)
    d.notes(s, "The ask for account managers: when you hear one of these needs, bring us in for a 2-week ideation workshop. "
               "We leave the client with a chosen blueprint and first modules, an architecture, agreed KPIs and a proof-of-concept plan.")


def cheatsheet_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "Sales cheat sheet: which blueprint to bring", size=32, bold=True)
    widths = [3.0, 5.4, 3.73]
    heads = ["Bring", "Listen for…", "Who to talk to"]
    y = 1.65
    x = ML
    for wdt, h in zip(widths, heads):
        tb(s, x + 0.1, y, wdt - 0.2, 0.4, h, size=14, bold=True)
        x += wdt
    y += 0.45
    hline(s, ML, y, W - ML, BLACK, 1.5)
    rh = 0.76
    for r, p in enumerate(C.PLATFORMS):
        if r % 2 == 0:
            rect(s, ML, y, W - 2 * ML, rh, fill=LIGHT)
        acc = ACCENTS[p["accent"]]
        oval(s, ML + 0.1, y + rh / 2 - 0.22, 0.44, fill=acc)
        icon(s, p["icon"], ink_on(acc), ML + 0.2, y + rh / 2 - 0.12, 0.24)
        tb(s, ML + 0.65, y + 0.14, widths[0] - 0.7, 0.3, p["name"], size=14, bold=True)
        tb(s, ML + 0.65, y + 0.45, widths[0] - 0.7, 0.3, p["domain"], size=10.5, color=GRAY)
        x = ML + widths[0]
        for wdt, cell in zip(widths[1:], [p["trigger"], p["who_to_talk"]]):
            tb(s, x + 0.1, y, wdt - 0.2, rh, cell, size=12, anchor=MSO_ANCHOR.MIDDLE)
            x += wdt
        y += rh
        hline(s, ML, y, W - ML, BLACK, 0.75, dash=True)
    d.notes(s, "Leave-behind for account managers. If a client mentions anything in 'Listen for', note who said it and bring us in "
               "with the matching blueprint.")


def thankyou_slide(d):
    s = d.slide(bg="bg_thankyou.png")
    d.notes(s, "Thank you. Next step: agree which client and which blueprint to take into an ideation workshop first.")


def build(out=OUT, only=None):
    """only: a blueprint name -> preview build with just the universal architecture and that blueprint's 3 slides."""
    MISSING_ICONS.clear()
    d = Deck()
    platforms = [p for p in C.PLATFORMS if only is None or p["name"].lower() == only.lower()]
    if only is None:
        title_slide(d)
        agenda_slide(d)
        who_slide(d)
    universal_arch_slide(d)
    if only is None:
        five_graphs_slide(d)
    for p in platforms:
        problem_slide(d, p)
        arch_slide(d, p)
        value_slide(d, p)
    if only is None:
        engage_slide(d)
        cheatsheet_slide(d)
        thankyou_slide(d)
    d.prs.save(out)
    return d.n


def render_icons(icon_dir):
    ICONS.mkdir(parents=True, exist_ok=True)
    jobs = [{"name": n, "color": c, "out": str(ICONS / f"{n}-{c}.png")} for n, c in sorted(MISSING_ICONS)]
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(jobs, f)
    subprocess.run(["node", str(HERE / "make_icons.js"), f.name, icon_dir], check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--icons", help="path to lucide-static/icons (renders any missing icons)")
    ap.add_argument("--only", help="preview: build only one blueprint (e.g. CareGraph) plus the universal architecture")
    ap.add_argument("--out", default=str(OUT), help="output .pptx path")
    args = ap.parse_args()
    n = build(args.out, args.only)
    if MISSING_ICONS:
        if not args.icons:
            raise SystemExit(f"{len(MISSING_ICONS)} icons missing; rerun with --icons <lucide-static/icons>")
        render_icons(args.icons)
        n = build(args.out, args.only)
        assert not MISSING_ICONS, MISSING_ICONS
    print(f"wrote {args.out} ({n} slides)")
