# -*- coding: utf-8 -*-
"""Shared Bramble & Brain Co. brand system for reportlab (PDF) + PIL (listing images).

Font note: the brand spec (04_BRAND.md) calls for Fredoka (display) + Nunito
(body). Those exact families weren't fetchable in this environment, so this
kit substitutes Outfit (display) + Work Sans (body) — both free/OFL, rounded
and friendly in the same spirit, ADHD/dyslexia-readable.
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "/mnt/skills/examples/canvas-design/canvas-fonts/"

_registered = False


def register_fonts():
    global _registered
    if _registered:
        return
    pdfmetrics.registerFont(TTFont("Display-Reg", FONT_DIR + "Outfit-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("Display-Bold", FONT_DIR + "Outfit-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Reg", FONT_DIR + "WorkSans-Regular.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Semi", FONT_DIR + "WorkSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont("Body-Bold", FONT_DIR + "WorkSans-Bold.ttf"))
    _registered = True


# Reportlab font aliases matching the original script's naming
F_MED = "Display-Reg"
F_SEMI = "Display-Bold"
F_BOLD = "Display-Bold"
N_REG = "Body-Reg"
N_SEMI = "Body-Semi"
N_BOLD = "Body-Bold"

# PIL font filenames (relative to FONT_DIR)
PIL_F_BOLD = "Outfit-Bold.ttf"
PIL_F_SEMI = "Outfit-Bold.ttf"
PIL_N_REG = "WorkSans-Regular.ttf"
PIL_N_SEMI = "WorkSans-Bold.ttf"
PIL_N_BOLD = "WorkSans-Bold.ttf"

CREAM = HexColor("#FAF3E9")
CREAM_DEEP = HexColor("#F1E4D0")
TERRACOTTA = HexColor("#C06544")
TERRACOTTA_DARK = HexColor("#8F4930")
TERRACOTTA_TINT = HexColor("#F0DCCF")
SAGE = HexColor("#8C9B7C")
SAGE_DARK = HexColor("#5F6B54")
SAGE_TINT = HexColor("#E4E8DC")
MARIGOLD = HexColor("#E8A94A")
MARIGOLD_TINT = HexColor("#FBECD2")
INK = HexColor("#4A3B32")
INK_MUTED = HexColor("#6E5A4E")
LINE = HexColor("#D9C9B4")
WHITE = HexColor("#FFFFFF")

# PIL RGB tuples (same palette)
P_CREAM = (250, 243, 233)
P_CREAM_DEEP = (241, 228, 208)
P_TERRACOTTA = (192, 101, 68)
P_TERRACOTTA_DARK = (143, 73, 48)
P_TERRACOTTA_TINT = (240, 220, 207)
P_SAGE = (140, 155, 124)
P_SAGE_DARK = (95, 107, 84)
P_SAGE_TINT = (228, 232, 220)
P_MARIGOLD = (232, 169, 74)
P_MARIGOLD_TINT = (251, 236, 210)
P_INK = (74, 59, 50)
P_INK_MUTED = (110, 90, 78)
P_WHITE = (255, 255, 255)

PAGE_W, PAGE_H = letter
MARGIN = 42
CONTENT_W = PAGE_W - 2 * MARGIN
LEFT = MARGIN
RIGHT = PAGE_W - MARGIN

DOT_OFFSETS = [
    (-0.45, -0.50, 0.11),
    (0.50, -0.55, 0.09),
    (0.70, 0.10, 0.13),
    (0.40, 0.65, 0.10),
    (-0.52, 0.50, 0.08),
    (-0.65, -0.05, 0.12),
]


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(test, font, size) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_paragraph(c, text, x, y, max_width, font=N_REG, size=10.5, leading=14, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(text, font, size, max_width)
    for line in lines:
        if align == "center":
            c.drawCentredString(x + max_width / 2, y, line)
        else:
            c.drawString(x, y, line)
        y -= leading
    return y


def draw_mark(c, cx, cy, r, ring_bg=TERRACOTTA, dot_color=CREAM, focus_color=MARIGOLD, draw_ring=True):
    c.saveState()
    if draw_ring:
        c.setFillColor(ring_bg)
        c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(dot_color)
    for dx, dy, rr in DOT_OFFSETS:
        c.circle(cx + dx * r, cy + dy * r, rr * r, fill=1, stroke=0)
    c.setFillColor(focus_color)
    c.circle(cx, cy, 0.42 * r, fill=1, stroke=0)
    c.restoreState()


def header_band(c, title, subtitle=None, band_color=TERRACOTTA, band_h=70, brand_line="B R A M B L E   &   B R A I N   C O ."):
    c.saveState()
    c.setFillColor(band_color)
    c.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont(N_BOLD, 8.5)
    c.drawString(LEFT, PAGE_H - 18, brand_line)
    c.setFont(F_BOLD, 25)
    c.drawString(LEFT, PAGE_H - band_h + 16, title)
    if subtitle:
        c.setFont(N_SEMI, 10.5)
        tw = pdfmetrics.stringWidth(title, F_BOLD, 25)
        c.drawString(LEFT + tw + 14, PAGE_H - band_h + 20, subtitle)
    c.restoreState()


def footer(c, page_num, total_pages, product_name):
    c.saveState()
    c.setFillColor(INK_MUTED)
    c.setFont(N_REG, 8)
    c.drawCentredString(PAGE_W / 2, 24, "Bramble & Brain Co.   ·   %s   ·   page %d of %d" % (product_name, page_num, total_pages))
    c.restoreState()


def box(c, x, y, w, h, stroke=LINE, fill=None, radius=8, lw=1.1):
    c.saveState()
    c.setLineWidth(lw)
    c.setStrokeColor(stroke)
    if fill is not None:
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, radius, fill=0, stroke=1)
    c.restoreState()


def checkbox(c, x, y, size=11, color=TERRACOTTA):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(1.3)
    c.roundRect(x, y, size, size, 2.5, fill=0, stroke=1)
    c.restoreState()


def numbered_dot(c, cx, cy, r, num, bg=TERRACOTTA, text_color=CREAM):
    c.saveState()
    c.setFillColor(bg)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont(N_BOLD, r * 1.05)
    c.drawCentredString(cx, cy - r * 0.35, str(num))
    c.restoreState()


# ---------------------------------------------------------------- PIL (listing images) helpers
from PIL import Image, ImageDraw, ImageFont, ImageFilter

IMG_W = IMG_H = 2000


def pil_font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def new_canvas(bg=P_CREAM):
    return Image.new("RGB", (IMG_W, IMG_H), bg)


def center_text(draw, cx, y, text, f, fill):
    bbox = draw.textbbox((0, 0), text, font=f)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return bbox[3] - bbox[1]


def pil_wrap_text(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        test = (cur + " " + wd).strip()
        bbox = draw.textbbox((0, 0), test, font=f)
        if bbox[2] - bbox[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def paste_with_shadow(base, img, x, y, shadow_offset=18, shadow_blur=30, shadow_opacity=70):
    shadow = Image.new("RGBA", (img.width + 120, img.height + 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([60, 60, 60 + img.width, 60 + img.height], radius=18, fill=(20, 14, 10, shadow_opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(shadow_blur))
    base.paste(shadow, (x - 60 + shadow_offset, y - 60 + shadow_offset), shadow)
    base.paste(img, (x, y))


def brand_tag(draw, y=1940):
    center_text(draw, IMG_W / 2, y, "B R A M B L E   &   B R A I N   C O .", pil_font(PIL_N_BOLD, 26), P_TERRACOTTA)


def render_pdf_pages(pdf_path, out_dir, dpi=200):
    """Render every page of pdf_path to out_dir/page_N.png using pymupdf."""
    import fitz
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=mat)
        pix.save(os.path.join(out_dir, f"page_{i}.png"))
    doc.close()
