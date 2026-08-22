# -*- coding: utf-8 -*-
"""Builds the new outcome-focused hero/thumbnail (image #1) for the flagship
'ADHD Life OS — Printable Edition' listing.

Design brief: lead with the outcome, show a real strong planner page large
(not a small cover mockup in beige space), add 3 proof-point pills, keep it
legible as a small square thumbnail (Etsy's #1 image is what drives clicks).
"""
import os
from PIL import Image, ImageDraw
from _brand_kit import (
    pil_font, new_canvas, center_text, pil_wrap_text,
    PIL_F_BOLD, PIL_F_SEMI, PIL_N_REG, PIL_N_SEMI, PIL_N_BOLD,
    P_CREAM, P_CREAM_DEEP, P_TERRACOTTA, P_TERRACOTTA_DARK, P_TERRACOTTA_TINT,
    P_SAGE, P_SAGE_DARK, P_SAGE_TINT, P_MARIGOLD, P_MARIGOLD_TINT,
    P_INK, P_INK_MUTED, P_WHITE, IMG_W, IMG_H,
)

HERE = os.path.dirname(__file__)
IMG_DIR = os.path.join(HERE, "listing_images")
OUT_PATH = os.path.join(IMG_DIR, "listing_1_hero_v2.jpg")


def load_page(n, target_w=None):
    im = Image.open(os.path.join(IMG_DIR, f"page_{n}.png")).convert("RGB")
    if target_w:
        r = target_w / im.width
        im = im.resize((target_w, int(im.height * r)), Image.LANCZOS)
    return im


def pill(d, cx, cy, text, bg, text_color, pad_x=28, h=64, font_size=28):
    f = pil_font(PIL_N_BOLD, font_size)
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    w = tw + pad_x * 2
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=bg)
    center_text(d, cx, y0 + (h - (bbox[3] - bbox[1])) / 2 - bbox[1], text, f, text_color)
    return w


def build():
    im = new_canvas()
    d = ImageDraw.Draw(im)

    # ---- headline block ----
    center_text(d, IMG_W / 2, 56, "THE ADHD LIFE OS", pil_font(PIL_F_BOLD, 92), P_TERRACOTTA_DARK)
    center_text(d, IMG_W / 2, 172, "Plan your day without fighting your brain.", pil_font(PIL_F_SEMI, 46), P_SAGE_DARK)

    # ---- large, prominent real planner page (the "Today" / daily page) ----
    raw = Image.open(os.path.join(IMG_DIR, "page_4.png")).convert("RGB")
    target_h = 1440
    r = target_h / raw.height
    page = raw.resize((int(raw.width * r), target_h), Image.LANCZOS)

    frame_pad = 14
    fx = (IMG_W - page.width) // 2
    fy = 250
    # soft shadow
    shadow = Image.new("RGBA", (page.width + frame_pad * 2 + 60, page.height + frame_pad * 2 + 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([30, 34, 30 + page.width + frame_pad * 2, 34 + page.height + frame_pad * 2],
                          radius=20, fill=(20, 14, 10, 70))
    from PIL import ImageFilter
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    im.paste(shadow, (fx - frame_pad - 30, fy - frame_pad - 30), shadow)

    d.rounded_rectangle([fx - frame_pad, fy - frame_pad, fx + page.width + frame_pad, fy + page.height + frame_pad],
                         radius=20, fill=P_WHITE)
    im.paste(page, (fx, fy))

    # ---- proof point pills ----
    py = fy + page.height + frame_pad + 56
    items = [
        ("VISUAL TIME BLOCKS", P_TERRACOTTA, P_CREAM),
        ("DOPAMINE MENU", P_MARIGOLD, P_TERRACOTTA_DARK),
        ("LOW-SPOONS MODE", P_SAGE_DARK, P_CREAM),
    ]
    gap = 24
    widths = []
    f = pil_font(PIL_N_BOLD, 28)
    for text, bg, tc in items:
        bbox = d.textbbox((0, 0), text, font=f)
        widths.append(bbox[2] - bbox[0] + 28 * 2)
    total_w = sum(widths) + gap * (len(items) - 1)
    cx = (IMG_W - total_w) / 2
    for (text, bg, tc), w in zip(items, widths):
        cx_pill = cx + w / 2
        pill(d, cx_pill, py, text, bg, tc)
        cx += w + gap

    center_text(d, IMG_W / 2, py + 46, "B R A M B L E   &   B R A I N   C O .", pil_font(PIL_N_BOLD, 24), P_TERRACOTTA)

    im.save(OUT_PATH, quality=92)
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
