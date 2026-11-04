"""Build the Insight Global healthcare AI case-study deck (python-pptx).

Usage:
    python3 deck/extract_assets.py <PowerPoint_Template.pdf>   # once, creates deck/assets/
    python3 deck/build_deck.py                                  # writes deck/IG_Healthcare_AI_Case_Studies.pptx
"""
import math
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

import content as C

HERE = Path(__file__).resolve().parent
ASSETS = HERE / "assets"
OUT = HERE / "IG_Healthcare_AI_Case_Studies.pptx"

# Brand (from the Insight Global template user guide)
FONT = "Trenda IG Text"
FONT_LIGHT = "Trenda IG Text Light"
BLACK = RGBColor(0x00, 0x00, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
YELLOW = RGBColor(0xFF, 0xD2, 0x00)
CYAN = RGBColor(0x00, 0xD3, 0xF2)
MAGENTA = RGBColor(0xFF, 0x0A, 0x6C)
NAVY = RGBColor(0x0D, 0x22, 0x35)
PURPLE = RGBColor(0x5B, 0x2A, 0xA0)
GREEN = RGBColor(0x5B, 0xE4, 0x4A)
ORANGE = RGBColor(0xFF, 0x8A, 0x33)
LIGHT = RGBColor(0xF2, 0xF2, 0xF2)
MID = RGBColor(0xE6, 0xE6, 0xE6)
GRAY = RGBColor(0x5F, 0x5F, 0x5F)
SOFT = RGBColor(0xBF, 0xBF, 0xBF)
ACCENTS = {"cyan": CYAN, "magenta": MAGENTA, "yellow": YELLOW}

W, H = 13.333, 7.5
ML = 0.6  # left margin (in)


# ----------------------------------------------------------------------------- helpers
def est_lines(text, size, width_in):
    cpl = max(1.0, width_in * 72 / (size * 0.48) * 0.93)
    return max(1, math.ceil(len(text) / cpl))


def text_h(text, size, width_in, spacing=1.18):
    return est_lines(text, size, width_in) * size * spacing / 72


def tb(slide, x, y, w, h, text, size=14, color=BLACK, bold=False, light=False, italic=False,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, tracking=None, line=1.08):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    lines = text if isinstance(text, list) else [text]
    for i, t in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line
        r = p.add_run()
        r.text = t
        f = r.font
        f.name = FONT_LIGHT if light else FONT
        f.size = Pt(size)
        f.bold = bold
        f.italic = italic
        f.color.rgb = color
        if tracking:
            r._r.get_or_add_rPr().set("spc", str(int(tracking * 100)))
    return box


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
    style = s._element.find(qn("p:style"))
    if style is not None:
        s._element.remove(style)
    return s


def oval(slide, x, y, d, fill=None, line=None, line_w=1.25):
    return rect(slide, x, y, d, d, fill=fill, line=line, line_w=line_w, shape=MSO_SHAPE.OVAL)


def hline(slide, x1, y, x2, color, width=1.0, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y), Inches(x2), Inches(y))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = 3  # round dot
    return c


def vline(slide, x, y1, y2, color, width=1.0, dash=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x), Inches(y1), Inches(x), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    if dash:
        c.line.dash_style = 3
    return c


def pill(slide, x, y, text, color, size=11, h=0.32, fill=None, text_color=None):
    w = len(text) * size * 0.56 / 72 + 0.36
    rect(slide, x, y, w, h, fill=fill, line=color, line_w=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.5)
    tb(slide, x, y, w, h, text, size=size, color=text_color or color, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return x + w + 0.12


def bullets(slide, x, y, w, items, size=14, color=BLACK, dot=MAGENTA, gap=0.14):
    for it in items:
        oval(slide, x, y + size * 0.42 / 72 - 0.045, 0.09, fill=dot)
        h = text_h(it, size, w - 0.25)
        tb(slide, x + 0.25, y, w - 0.25, h, it, size=size, color=color)
        y += h + gap
    return y


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
        tb(s, ML, 0.3, 8, 0.25, label, size=8, bold=True, color=col, tracking=2.2)
        # ●●●IG footer mark
        for i in range(3):
            oval(s, ML + i * 0.135, 7.12, 0.105, fill=col)
        tb(s, ML + 0.42, 7.065, 0.4, 0.22, "IG", size=10, bold=True, color=col)
        nd = dark if num_dark is None else num_dark
        tb(s, W - 1.1, 7.07, 0.5, 0.22, str(self.n), size=9, color=WHITE if nd else BLACK, align=PP_ALIGN.RIGHT)

    @staticmethod
    def notes(s, text):
        s.notes_slide.notes_text_frame.text = text


# ----------------------------------------------------------------------------- slides
def title_slide(d):
    s = d.slide(bg="bg_title.png")
    tb(s, 1, 2.55, W - 2, 1.6, ["HEALTHCARE AI &", "AGENTIC SOLUTIONS"], size=42, light=True, color=WHITE,
       align=PP_ALIGN.CENTER, tracking=6, line=1.0)
    tb(s, 1, 4.35, W - 2, 0.5, "Ideation case studies across the healthcare value chain", size=18, color=WHITE,
       align=PP_ALIGN.CENTER)
    tb(s, 1, 6.55, W - 2, 0.3, f"IGH PRESIDENT BRIEFING  ·  {C.DECK_DATE}", size=11, color=WHITE,
       align=PP_ALIGN.CENTER, tracking=4)
    d.notes(s, "Purpose: show the president what our core team can do in healthcare, and give account managers and sales "
               "a library of case studies they can use to start conversations.\n\nAll case studies are at ideation stage: "
               "problem, solution, high-level architecture and value. Figures marked 'Pilot target' are agreed with each client; "
               "sourced figures are public evidence.")


def agenda_slide(d):
    s = d.slide(bg="bg_dark_magenta.jpg")
    d.chrome(s)
    tb(s, ML, 0.75, 6, 0.8, "Agenda", size=40, bold=True, color=WHITE)
    items = ["Who we are", "Our approach"] + [sec["title"] for sec in C.SECTIONS] + ["How we engage"]
    for i, it in enumerate(items):
        col, row = divmod(i, 4)
        x, y = ML + col * 6.3, 2.0 + row * 1.0
        oval(s, x, y, 0.5, line=WHITE, line_w=1.5)
        tb(s, x, y, 0.5, 0.5, str(i + 1), size=15, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        tb(s, x + 0.72, y, 5.2, 0.5, it, size=24, light=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, "Five healthcare domains, two case studies each, each told in three slides: problem and solution, "
               "high-level architecture, value. We close with how we engage and a cheat sheet for sales.")


def who_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "A core team built for any healthcare requirement", size=32, bold=True)
    tb(s, ML, 1.45, 12, 0.4, "From strategy to production across AI, data, Salesforce and cloud, with healthcare compliance built in.",
       size=16, color=GRAY)
    cols = [CYAN, YELLOW, MAGENTA, CYAN, YELLOW, MAGENTA]
    tw, th, gx, gy = 3.93, 1.84, 0.17, 0.12
    for i, (t, desc) in enumerate(C.CAPABILITIES):
        c, r = i % 3, i // 3
        x, y = ML + c * (tw + gx), 2.1 + r * (th + gy)
        rect(s, x, y, tw, th, fill=LIGHT)
        oval(s, x + 0.25, y + 0.25, 0.3, fill=cols[i])
        tb(s, x + 0.25, y + 0.66, tw - 0.5, 0.5, t, size=16, bold=True, line=1.0, anchor=MSO_ANCHOR.BOTTOM)
        tb(s, x + 0.25, y + 1.24, tw - 0.5, 0.6, desc, size=11.5, color=GRAY)
    rect(s, ML, 6.15, W - 2 * ML, 0.68, fill=BLACK)
    tb(s, ML + 0.25, 6.15, 1.5, 0.68, "PROOF POINT", size=10, bold=True, color=YELLOW, tracking=2, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, ML + 1.75, 6.15, W - 2 * ML - 2.0, 0.68, C.PROOF_POINT.replace("Proof point: ", ""), size=12.5, color=WHITE,
       anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, "Key message: one core team covers every layer a healthcare AI program needs, so we can take any requirement "
               "from idea to production.\n\nThe proof point is our current delivery for a large US health system "
               "(client name withheld; use it verbally only if cleared).")


def team_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "Our core team", size=32, bold=True)
    roles = ["Engagement lead", "AI / agentic architect", "Knowledge graph & data lead",
             "Salesforce Health Cloud architect", "Marketing & Data Cloud lead", "Cloud & platform engineer",
             "Healthcare compliance lead", "Clinical / domain SME", "Delivery manager"]
    for i, role in enumerate(roles):
        c, r = i % 3, i // 3
        x, y = ML + c * 4.1, 1.85 + r * 1.55
        oval(s, x, y, 1.05, fill=MID)
        tb(s, x + 1.3, y + 0.2, 2.7, 0.35, "[Name]", size=18, bold=True)
        tb(s, x + 1.3, y + 0.58, 2.7, 0.35, role, size=14)
    d.notes(s, "Fill in names and photos before presenting (circle placeholders). Roles are suggested; adjust to the real team.")


def approach_slide(d):
    s = d.slide(bg="bg_dark_glow.jpg")
    d.chrome(s)
    tb(s, ML, 0.7, 12, 0.7, "One reusable pattern, applied to every domain", size=32, bold=True, color=WHITE)
    tb(s, ML, 1.45, 12, 0.4, "Every case study: problem  →  solution  →  architecture  →  value", size=16, color=SOFT)
    cols = [CYAN, YELLOW, MAGENTA, PURPLE, WHITE]
    bw, gap, y = 2.25, 0.22, 2.3
    for i, (t, desc) in enumerate(C.APPROACH_COLUMNS):
        x = ML + i * (bw + gap)
        rect(s, x, y, bw, 2.45, line=cols[i], line_w=1.5, shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08)
        oval(s, x + 0.22, y + 0.25, 0.42, fill=cols[i])
        tb(s, x + 0.22, y + 0.25, 0.42, 0.42, str(i + 1), size=14, bold=True, color=BLACK, align=PP_ALIGN.CENTER,
           anchor=MSO_ANCHOR.MIDDLE)
        tb(s, x + 0.22, y + 0.8, bw - 0.4, 0.55, t, size=17, bold=True, color=WHITE, line=1.0, anchor=MSO_ANCHOR.BOTTOM)
        tb(s, x + 0.22, y + 1.42, bw - 0.4, 0.9, desc, size=12.5, color=SOFT)
        if i < 4:
            tb(s, x + bw, y + 0.95, gap, 0.4, "›", size=24, color=WHITE, align=PP_ALIGN.CENTER)
    rect(s, ML, 5.0, W - 2 * ML, 0.62, fill=MAGENTA)
    tb(s, ML + 0.25, 5.0, W - 2 * ML - 0.5, 0.62, C.APPROACH_GOVERNANCE, size=13, bold=True, color=WHITE,
       anchor=MSO_ANCHOR.MIDDLE)
    tb(s, ML, 5.98, 1.6, 0.32, "Runs on any cloud", size=12, color=SOFT, anchor=MSO_ANCHOR.MIDDLE)
    x = ML + 1.65
    for c in C.CLOUDS:
        x = pill(s, x, 5.98, c, WHITE, size=11)
    d.notes(s, "This is the engine behind every case study. Same five layers, same governance, different data and agents per domain. "
               "That reuse is why we can stand up a new domain quickly. It is cloud-agnostic: GCP, AWS or Azure, with Salesforce as "
               "the engagement layer where clients already use it.")


def map_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "Where we play across the healthcare value chain", size=32, bold=True)
    cw, gap = 2.3, 0.155
    for i, sec in enumerate(C.SECTIONS):
        x = ML + i * (cw + gap)
        acc = ACCENTS[sec["accent"]]
        rect(s, x, 1.75, cw, 0.08, fill=acc)
        tb(s, x, 1.98, cw, 0.25, sec["stage"].upper(), size=8.5, bold=True, color=GRAY, tracking=1.2)
        tb(s, x, 2.3, cw, 0.5, sec["num"], size=30, light=True, color=BLACK)
        tb(s, x, 2.9, cw, 0.6, sec["title"], size=17, bold=True)
        for j, case in enumerate(sec["cases"]):
            y = 3.65 + j * 1.05
            rect(s, x, y, cw, 0.92, fill=LIGHT)
            tb(s, x + 0.15, y + 0.12, 0.3, 0.3, "AB"[j], size=12, bold=True, color=acc if acc != YELLOW else ORANGE)
            tb(s, x + 0.45, y + 0.12, cw - 0.6, 0.72, case["short"], size=12.5)
        tb(s, x, 5.9, cw, 0.8, "Buyers: " + sec["buyers"], size=10.5, color=GRAY)
    d.notes(s, "Five domains that cover the full value chain, from developing and making medicines to engaging patients and delivering care. "
               "Each has two case studies. Pick the domain that matches the client in front of you.")


def divider(d, sec):
    s = d.slide(bg=sec["bg"])
    d.chrome(s)
    acc = ACCENTS[sec["accent"]]
    tb(s, ML + 0.4, 2.15, 4, 1.0, sec["num"], size=60, light=True, color=acc)
    tsize = 40 if len(sec["title"]) <= 22 else 32
    tb(s, ML + 0.4, 3.2, 12, 0.8, sec["title"].upper(), size=tsize, light=True, color=WHITE, tracking=5)
    for j, case in enumerate(sec["cases"]):
        tb(s, ML + 0.4, 4.3 + j * 0.48, 11, 0.4, f"{'AB'[j]}  ·  {case['title']}", size=18, color=WHITE)
    tb(s, ML + 0.4, 5.65, 11, 0.35, "Who buys: " + sec["buyers"], size=13, color=SOFT)
    d.notes(s, f"Section {sec['num']}: {sec['title']}.\nListen for: {sec['trigger']}.\nWho to talk to: {sec['who']}.")


def problem_slide(d, sec, case, j):
    s = d.slide(fill=WHITE)
    rect(s, W / 2, 0, W / 2, H, fill=BLACK)
    d.chrome(s, label=f"{sec['num']} · {sec['title'].upper()} · CASE STUDY {'AB'[j]}", dark=False, num_dark=True)
    lw = W / 2 - ML - 0.45
    th = text_h(case["title"], 24, lw, 1.1)
    tb(s, ML, 0.7, lw, th, case["title"], size=24, bold=True, line=1.0)
    y = 0.7 + th + 0.3
    tb(s, ML, y, lw, 0.25, "THE PROBLEM", size=10, bold=True, color=MAGENTA, tracking=2.2)
    y += 0.35
    h = text_h(case["problem"], 14.5, lw)
    tb(s, ML, y, lw, h, case["problem"], size=14.5)
    y += h + 0.2
    who = "Who feels it: " + case["who"]
    h = text_h(who, 12, lw)
    tb(s, ML, y, lw, h, who, size=12, italic=True, color=GRAY)
    y += h + 0.25
    y = bullets(s, ML, y, lw, case["pains"], size=13.5, dot=MAGENTA, gap=0.1)
    big, txt, src = case["facts"][0]
    fy = max(y + 0.2, 5.55)
    hline(s, ML, fy, ML + lw, BLACK, 0.75, dash=True)
    bw = max(1.2, len(big) * 30 * 0.6 / 72 + 0.2)
    tb(s, ML, fy + 0.15, bw, 0.6, big, size=30, light=True, color=MAGENTA)
    tb(s, ML + bw + 0.15, fy + 0.15, lw - bw - 0.15, 0.6, txt, size=11.5)
    tb(s, ML + bw + 0.15, fy + 0.15 + text_h(txt, 11.5, lw - bw - 0.15) + 0.05, lw - bw - 0.15, 0.25,
       "Source: " + src, size=9.5, italic=True, color=GRAY)

    rx, rw = W / 2 + 0.55, W / 2 - 1.15
    tb(s, rx, 0.7, rw, 0.3, "OUR SOLUTION", size=10, bold=True, color=CYAN, tracking=2.2)
    tb(s, rx, 1.05, rw, 0.5, "Specialist AI agents, grounded in trusted data, with people in control", size=17,
       bold=True, color=WHITE)
    bullets(s, rx, 2.05, rw, case["solution"], size=15, color=WHITE, dot=CYAN, gap=0.22)
    tb(s, rx, 5.75, rw, 0.25, "BUILT ON", size=9, bold=True, color=SOFT, tracking=2)
    x, yy = rx, 6.08
    for b in case["built_on"]:
        wpill = len(b) * 11 * 0.56 / 72 + 0.36
        if x + wpill > rx + rw:
            x, yy = rx, yy + 0.42
        x = pill(s, x, yy, b, WHITE, size=11)
    note = case["notes"]
    d.notes(s, ("PRESIDENT CUT: present this case.\n\n" if note["cut"] else "Backup / sales library case.\n\n")
            + "Talk track: " + note["talk"])


HLD_COLS = [("DATA SOURCES", "sources", CYAN, BLACK), ("INGEST & GOVERN", "ingest", YELLOW, BLACK),
            ("KNOWLEDGE", "knowledge", MAGENTA, WHITE), ("AI AGENTS", "agents", PURPLE, WHITE),
            ("EXPERIENCE", "experience", BLACK, WHITE)]


def hld_slide(d, sec, case, j):
    s = d.slide(fill=WHITE)
    d.chrome(s, label=f"{sec['num']} · {sec['title'].upper()} · CASE STUDY {'AB'[j]}", dark=False)
    tb(s, ML, 0.62, 8, 0.25, "HIGH-LEVEL ARCHITECTURE", size=10, bold=True, color=MAGENTA, tracking=2.2)
    tb(s, ML, 0.9, 12, 0.6, "How it works: " + case["short"], size=26, bold=True)
    cw, gap, top = 2.3, 0.16, 1.75
    body_h = 3.55
    for i, (label, key, col, tcol) in enumerate(HLD_COLS):
        x = ML + i * (cw + gap)
        rect(s, x, top, cw, 0.42, fill=col)
        tb(s, x + 0.15, top, cw - 0.3, 0.42, f"{i + 1}  {label}", size=11.5, bold=True, color=tcol,
           anchor=MSO_ANCHOR.MIDDLE, tracking=0.3)
        rect(s, x, top + 0.42, cw, body_h, fill=LIGHT)
        items = case["hld"][key]
        y = top + 0.6
        for it in items:
            ih = max(0.46, text_h(it, 11, cw - 0.4, 1.12) + 0.2)
            words = set(it.lower().replace("-", " ").split())
            border = YELLOW if words & {"gate", "approval", "approver", "handoff", "reviewer"} else None
            rect(s, x + 0.12, y, cw - 0.24, ih, fill=WHITE, line=border, line_w=1.5,
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.12)
            tb(s, x + 0.2, y, cw - 0.4, ih, it, size=11, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
            y += ih + 0.08
        if i < 4:
            tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(x + cw + 0.025), Inches(top + 0.42 + body_h / 2 - 0.08),
                                     Inches(0.11), Inches(0.16))
            tri.rotation = 90
            tri.fill.solid()
            tri.fill.fore_color.rgb = BLACK
            tri.line.fill.background()
            st = tri._element.find(qn("p:style"))
            if st is not None:
                tri._element.remove(st)
    gy = top + 0.42 + body_h + 0.18
    rect(s, ML, gy, W - 2 * ML, 0.52, fill=BLACK)
    tb(s, ML + 0.2, gy, 1.6, 0.52, "GOVERNANCE", size=10, bold=True, color=YELLOW, tracking=2, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, ML + 1.8, gy, W - 2 * ML - 2.0, 0.52,
       "Guardrails in & out  ·  PHI masking & minimum-data access  ·  Human approval gates  ·  Evaluation set  ·  Audit trail",
       size=12, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    cy = gy + 0.68
    tb(s, ML, cy, 1.7, 0.3, "Runs on any cloud:", size=11, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    x = ML + 1.6
    for c in C.CLOUDS:
        x = pill(s, x, cy, c, GRAY, size=10, h=0.3)
    oval(s, W - ML - 2.65, cy + 0.08, 0.15, fill=WHITE, line=YELLOW, line_w=1.5)
    tb(s, W - ML - 2.42, cy, 2.45, 0.3, "Yellow outline = human in the loop", size=10, color=GRAY, anchor=MSO_ANCHOR.MIDDLE)
    d.notes(s, "Walk left to right: where the data comes from, how it is cleaned and protected, the knowledge layer "
               "(graph + vector search) that keeps answers grounded, the agents, and where users see the result. "
               "Governance runs underneath everything. Boxes outlined in yellow are where a person approves. "
               "The same design runs on Google Cloud, AWS or Azure.")


def value_slide(d, sec, case, j):
    s = d.slide(fill=BLACK)
    d.chrome(s, label=f"{sec['num']} · {sec['title'].upper()} · CASE STUDY {'AB'[j]}")
    tb(s, ML, 0.62, 8, 0.25, "VALUE & BENEFITS", size=10, bold=True, color=CYAN, tracking=2.2)
    tb(s, ML, 0.92, W - 2 * ML, 1.0, case["value_headline"], size=28, light=True, color=WHITE, line=1.05)
    cw, gap = 2.88, 0.2
    for i, (big, label, src) in enumerate(case["stats"]):
        x = ML + i * (cw + gap)
        size = 54 if len(big) <= 5 else 40
        tb(s, x, 2.15, cw, 0.9, big, size=size, light=True, color=CYAN)
        lh = text_h(label, 14, cw - 0.1) * 1.15
        tb(s, x, 3.15, cw - 0.1, lh, label, size=14, color=WHITE)
        cap = src if src.startswith(("Pilot", "Design")) else "Source: " + src
        tb(s, x, 3.15 + lh + 0.08, cw - 0.1, 0.4, cap, size=10, italic=True, color=SOFT)
    hline(s, ML, 4.85, W - ML, WHITE, 0.75, dash=True)
    dots = [CYAN, YELLOW, MAGENTA, GREEN]
    for i, (k, v) in enumerate(case["benefits"].items()):
        x = ML + i * (cw + gap)
        oval(s, x, 5.17, 0.13, fill=dots[i])
        tb(s, x + 0.25, 5.08, cw - 0.3, 0.3, k, size=14, bold=True, color=WHITE)
        tb(s, x, 5.5, cw - 0.1, 1.0, v, size=13, color=SOFT)
    q = "\n".join(f"  {n + 1}. {qq}" for n, qq in enumerate(case["notes"]["questions"]))
    d.notes(s, "Value: arrows are pilot targets we agree with the client in the ideation workshop; numbers with a source are public evidence.\n\n"
               "Discovery questions for account managers:\n" + q)


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
        top = ly - 1.55 if i % 2 == 0 else ly + 0.2
        if i % 2 == 0:
            vline(s, x, ly - 1.55, ly - 0.15, WHITE, 1.25, dash=True)
        else:
            vline(s, x, ly + 0.15, ly + 1.55, WHITE, 1.25, dash=True)
        tb(s, x + 0.2, top, 2.85, 0.3, name, size=15, bold=True, color=WHITE)
        tb(s, x + 0.2, top + 0.32, 2.85, 0.28, dur.upper(), size=10, bold=True, color=CYAN, tracking=1.5)
        tb(s, x + 0.2, top + 0.65, 2.85, 0.85, desc, size=12.5, color=SOFT)
    tb(s, ML, 6.0, W - 2 * ML, 0.4, "Next step: pick one case study and run a 2-week ideation workshop with the client.",
       size=16, color=WHITE)
    d.notes(s, "The ask for account managers: when you hear one of these needs, bring us in for a 2-week ideation workshop. "
               "We leave the client with a chosen use case, an HLD and agreed KPIs, and a proof-of-concept plan.")


def cheatsheet_slide(d):
    s = d.slide(fill=WHITE)
    d.chrome(s, dark=False)
    tb(s, ML, 0.7, 12, 0.7, "Sales cheat sheet: opportunity triggers", size=32, bold=True)
    widths = [2.25, 4.45, 2.95, 2.48]
    heads = ["Domain", "Listen for…", "Who to talk to", "Case studies to bring"]
    y = 1.65
    x = ML
    for wdt, h in zip(widths, heads):
        tb(s, x + 0.1, y, wdt - 0.2, 0.4, h, size=14, bold=True)
        x += wdt
    y += 0.45
    hline(s, ML, y, W - ML, BLACK, 1.5)
    rh = 0.92
    for r, sec in enumerate(C.SECTIONS):
        if r % 2 == 0:
            rect(s, ML, y, W - 2 * ML, rh, fill=LIGHT)
        cells = [sec["title"], sec["trigger"], sec["who"], " · ".join(c["short"] for c in sec["cases"])]
        x = ML
        for k, (wdt, cell) in enumerate(zip(widths, cells)):
            tb(s, x + 0.1, y, wdt - 0.2, rh, cell, size=13 if k == 0 else 12, bold=(k == 0),
               anchor=MSO_ANCHOR.MIDDLE)
            x += wdt
        y += rh
        hline(s, ML, y, W - ML, BLACK, 0.75, dash=True)
    d.notes(s, "Leave-behind for account managers. If a client mentions anything in 'Listen for', note who said it and bring us in.")


def thankyou_slide(d):
    s = d.slide(bg="bg_thankyou.png")
    d.notes(s, "Thank you. Next step: agree which client and case study to take into an ideation workshop first.")


def build():
    d = Deck()
    title_slide(d)
    agenda_slide(d)
    who_slide(d)
    team_slide(d)
    approach_slide(d)
    map_slide(d)
    for sec in C.SECTIONS:
        divider(d, sec)
        for j, case in enumerate(sec["cases"]):
            problem_slide(d, sec, case, j)
            hld_slide(d, sec, case, j)
            value_slide(d, sec, case, j)
    engage_slide(d)
    cheatsheet_slide(d)
    thankyou_slide(d)
    d.prs.save(OUT)
    print(f"wrote {OUT} ({d.n} slides)")


if __name__ == "__main__":
    build()
