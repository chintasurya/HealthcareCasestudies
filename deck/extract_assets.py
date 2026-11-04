"""Extract Insight Global brand backgrounds and logo from the template PDF.

Usage: python3 deck/extract_assets.py /path/to/PowerPoint_Template.pdf
Writes PNG/JPG assets into deck/assets/.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = HERE / "assets"

# Full-page renders (background + logo already composited, no placeholder text).
PAGE_RENDERS = {
    7: "bg_title.png",       # black with green/cyan + magenta/gold glow, InsightGlobal logo
    9: "bg_section_navy.png",
    10: "bg_section_magenta.png",
    11: "bg_section_gold.png",
    47: "bg_thankyou.png",
}

# Raw background images (no footer / page number baked in).
RAW_BACKGROUNDS = {
    14: "bg_dark_magenta.jpg",
    31: "bg_dark_glow.jpg",
    44: "bg_dark_navy.jpg",
    45: "bg_dark_swirl.jpg",
}


def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)


def render_page(pdf, page, dest):
    with tempfile.TemporaryDirectory() as tmp:
        prefix = Path(tmp) / "p"
        run(["pdftoppm", "-png", "-r", "144", "-f", str(page), "-l", str(page),
             "-singlefile", str(pdf), str(prefix)])
        Image.open(f"{prefix}.png").convert("RGB").resize((1920, 1080)).save(dest)


def largest_image(pdf, page, dest):
    with tempfile.TemporaryDirectory() as tmp:
        run(["pdfimages", "-j", "-f", str(page), "-l", str(page), str(pdf), f"{tmp}/i"])
        jpgs = list(Path(tmp).glob("*.jpg"))
        best = max(jpgs, key=lambda f: Image.open(f).size[0] * Image.open(f).size[1])
        img = Image.open(best).convert("RGB")
        # A same-size non-JPEG file is the soft mask: composite the image over black with it.
        masks = [f for f in Path(tmp).iterdir()
                 if f.suffix != ".jpg" and Image.open(f).size == img.size]
        if masks:
            black = Image.new("RGB", img.size, (0, 0, 0))
            img = Image.composite(img, black, Image.open(masks[0]).convert("L"))
        img.resize((1920, 1080)).save(dest, quality=90)


def logo(pdf, dest):
    """White InsightGlobal logo from page 7 (RGB image + soft mask -> RGBA)."""
    with tempfile.TemporaryDirectory() as tmp:
        run(["pdfimages", "-png", "-f", "7", "-l", "7", str(pdf), f"{tmp}/i"])
        imgs = sorted(Path(tmp).glob("*.png"))
        rgb = next(Image.open(f) for f in imgs if Image.open(f).size == (330, 98) and Image.open(f).mode == "RGB")
        mask = next(Image.open(f) for f in imgs if Image.open(f).size == (330, 98) and Image.open(f).mode == "L")
        out = rgb.convert("RGBA")
        out.putalpha(mask)
        out.save(dest)


def main():
    pdf = Path(sys.argv[1])
    OUT.mkdir(exist_ok=True)
    for page, name in PAGE_RENDERS.items():
        render_page(pdf, page, OUT / name)
    for page, name in RAW_BACKGROUNDS.items():
        largest_image(pdf, page, OUT / name)
    logo(pdf, OUT / "logo_insightglobal_white.png")
    print("assets:", sorted(p.name for p in OUT.iterdir()))


if __name__ == "__main__":
    main()
