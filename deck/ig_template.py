"""Build an Insight Global slide master with named IG layouts (python-pptx + XML).

Backgrounds, the ●●●IG footer mark and the slide number live on the layouts, so on every slide
they are fixed (not selectable or deletable shapes), and PowerPoint's New Slide gallery offers the
IG layouts: gradient, black and white, matching the IG PowerPoint template.
"""
import re
from pathlib import Path

from lxml import etree
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls, qn
from pptx.util import Emu, Inches

ASSETS = Path(__file__).resolve().parent / "assets"
FONT = "Trenda IG Text"
W_IN, H_IN = 13.333, 7.5

# name, background ("img:<file>" or "solid:<hex>"), footer mark (None/"white"/"black"),
# title box (x, y, w, h in inches) or None, title size (pt), title colour
LAYOUTS = [
    ("IG Title", "img:bg_title.png", None, (1.0, 2.55, 11.33, 1.6), 42, "FFFFFF"),
    ("IG Agenda – Gradient", "img:bg_dark_magenta.jpg", "white", (0.6, 0.75, 8.0, 0.8), 40, "FFFFFF"),
    ("IG Section – Navy", "img:bg_section_navy.png", "white", (2.2, 2.48, 10.0, 1.0), 54, "FFFFFF"),
    ("IG Section – Magenta", "img:bg_section_magenta.png", "white", (2.2, 2.48, 10.0, 1.0), 54, "FFFFFF"),
    ("IG Section – Gold", "img:bg_section_gold.png", "white", (2.2, 2.48, 10.0, 1.0), 54, "FFFFFF"),
    ("IG Content – Black", "solid:000000", "white", (0.6, 0.7, 12.13, 0.7), 32, "FFFFFF"),
    ("IG Content – White", "solid:FFFFFF", "black", (0.6, 0.7, 12.13, 0.7), 32, "000000"),
    ("IG Thank You", "img:bg_thankyou.png", None, None, 32, "FFFFFF"),
]

# IG palette in the theme colour slots (dk1, lt1, dk2, lt2, accent1-6, hlink, folHlink)
THEME_COLORS = {"dk1": "000000", "lt1": "FFFFFF", "dk2": "0D2235", "lt2": "F2F2F2",
                "accent1": "00D3F2", "accent2": "FF0A6C", "accent3": "FFD200", "accent4": "5B2AA0",
                "accent5": "5BE44A", "accent6": "FF8A33", "hlink": "00D3F2", "folHlink": "FF0A6C"}

_ID = [5000]


def _next_id():
    _ID[0] += 1
    return _ID[0]


def _set_name(layout, name):
    layout._element.cSld.set("name", name)


def _set_background(part_owner, spec):
    """Background on a layout (or master) cSld: image stretched to the slide, or a solid colour."""
    cSld = part_owner._element.cSld
    old = cSld.find(qn("p:bg"))
    if old is not None:
        cSld.remove(old)
    kind, val = spec.split(":", 1)
    if kind == "img":
        _, rId = part_owner.part.get_or_add_image_part(str(ASSETS / val))
        fill = (f'<a:blipFill dpi="0" rotWithShape="1"><a:blip r:embed="{rId}"/><a:srcRect/>'
                f'<a:stretch><a:fillRect/></a:stretch></a:blipFill>')
    else:
        fill = f'<a:solidFill><a:srgbClr val="{val}"/></a:solidFill>'
    bg = parse_xml(f'<p:bg {nsdecls("p", "a", "r")}><p:bgPr>{fill}<a:effectLst/></p:bgPr></p:bg>')
    cSld.insert(0, bg)


def _add_picture(owner, path, x, y, w, h, name):
    _, rId = owner.part.get_or_add_image_part(str(path))
    pic = parse_xml(
        f'<p:pic {nsdecls("p", "a", "r")}><p:nvPicPr><p:cNvPr id="{_next_id()}" name="{name}"/>'
        f'<p:cNvPicPr><a:picLocks noGrp="1" noChangeAspect="1"/></p:cNvPicPr><p:nvPr userDrawn="1"/></p:nvPicPr>'
        f'<p:blipFill><a:blip r:embed="{rId}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
        f'<p:spPr><a:xfrm><a:off x="{Inches(x)}" y="{Inches(y)}"/><a:ext cx="{Inches(w)}" cy="{Inches(h)}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')
    owner._element.cSld.spTree.append(pic)


def _add_slide_number(owner, color):
    """Slide-number field at the template position (bottom right); numbers itself on every slide."""
    sp = parse_xml(
        f'<p:sp {nsdecls("p", "a")}><p:nvSpPr><p:cNvPr id="{_next_id()}" name="IG Slide Number"/>'
        f'<p:cNvSpPr txBox="1"><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr userDrawn="1"/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{Inches(W_IN - 1.6)}" y="{Inches(7.0)}"/><a:ext cx="{Inches(1.0)}" cy="{Inches(0.25)}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="none" lIns="0" tIns="0" rIns="0" bIns="0" anchor="ctr"/><a:lstStyle/>'
        f'<a:p><a:pPr algn="r"/><a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="slidenum">'
        f'<a:rPr lang="en-US" sz="900"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="{FONT}"/></a:rPr><a:t>‹#›</a:t></a:fld></a:p></p:txBody></p:sp>')
    owner._element.cSld.spTree.append(sp)


def _strip_placeholders(owner, keep_title):
    """Remove all placeholders except (optionally) the title."""
    spTree = owner._element.cSld.spTree
    for sp in list(spTree):
        ph = sp.find(".//" + qn("p:ph"))
        if ph is None:
            continue
        if keep_title and ph.get("type") in ("title", "ctrTitle"):
            ph.set("type", "title")
            continue
        spTree.remove(sp)


def _style_title(owner, box, size, color):
    for sp in owner._element.cSld.spTree.iter(qn("p:sp")):
        ph = sp.find(".//" + qn("p:ph"))
        if ph is None or ph.get("type") != "title":
            continue
        x, y, w, h = box
        spPr = sp.find(qn("p:spPr"))
        for child in list(spPr):
            spPr.remove(child)
        spPr.append(parse_xml(f'<a:xfrm {nsdecls("a")}><a:off x="{Inches(x)}" y="{Inches(y)}"/>'
                              f'<a:ext cx="{Inches(w)}" cy="{Inches(h)}"/></a:xfrm>'))
        txBody = sp.find(qn("p:txBody"))
        if txBody is not None:
            sp.remove(txBody)
        sp.append(parse_xml(
            f'<p:txBody {nsdecls("p", "a")}><a:bodyPr lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:normAutofit/></a:bodyPr>'
            f'<a:lstStyle><a:lvl1pPr algn="l"><a:lnSpc><a:spcPct val="100000"/></a:lnSpc>'
            f'<a:defRPr sz="{size * 100}" b="1"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
            f'<a:latin typeface="{FONT}"/></a:defRPr></a:lvl1pPr></a:lstStyle>'
            f'<a:p><a:r><a:rPr lang="en-US"/><a:t>Click to add title</a:t></a:r></a:p></p:txBody>'))


def _theme(prs):
    """IG fonts and colours in the theme, so new text boxes default to the IG look."""
    master = prs.slide_masters[0]
    theme = master.part.part_related_by(RT.THEME)
    xml = theme.blob.decode("utf-8")
    xml = re.sub(r'(<a:majorFont>\s*<a:latin typeface=")[^"]*', r"\g<1>" + FONT, xml)
    xml = re.sub(r'(<a:minorFont>\s*<a:latin typeface=")[^"]*', r"\g<1>" + FONT, xml)
    for slot, val in THEME_COLORS.items():
        xml = re.sub(rf"(<a:{slot}>)\s*<a:(?:srgbClr|sysClr)[^>]*?(?:/>|>.*?</a:(?:srgbClr|sysClr)>)",
                     rf'\g<1><a:srgbClr val="{val}"/>', xml, flags=re.S)
    xml = xml.replace('name="Office Theme"', 'name="Insight Global"', 1)
    theme._blob = xml.encode("utf-8")


def build_presentation():
    """Return a 16:9 Presentation whose master and layouts are the IG template."""
    prs = Presentation()
    prs.slide_width = Inches(W_IN)
    prs.slide_height = Inches(H_IN)
    master = prs.slide_masters[0]
    master._element.cSld.set("name", "Insight Global")
    _set_background(master, "solid:000000")
    # master keeps its title/body placeholders (for the master view); date/footer/number go
    spTree = master._element.cSld.spTree
    for sp in list(spTree):
        ph = sp.find(".//" + qn("p:ph"))
        if ph is not None and ph.get("type") in ("dt", "ftr", "sldNum"):
            spTree.remove(sp)
    _theme(prs)

    # reuse the default layouts that have a title placeholder (skip "Blank"), in order
    layouts = [l for l in prs.slide_layouts if l.name != "Blank"] + [l for l in prs.slide_layouts if l.name == "Blank"]
    for layout, (name, bg, mark, box, size, color) in zip(layouts, LAYOUTS):
        _set_name(layout, name)
        _strip_placeholders(layout, keep_title=box is not None)
        if box is not None:
            _style_title(layout, box, size, color)
        _set_background(layout, bg)
        if mark:
            _add_picture(layout, ASSETS / f"ig_mark_{mark}.png", 0.553, 7.05, 0.537, 0.108, "IG Footer Mark")
            _add_slide_number(layout, "FFFFFF" if mark == "white" else "000000")
    for layout in layouts[len(LAYOUTS):]:
        prs.slide_layouts.remove(layout)
    return prs


def layout(prs, name):
    return prs.slide_layouts.get_by_name(name)
