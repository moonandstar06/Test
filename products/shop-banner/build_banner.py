# -*- coding: utf-8 -*-
"""Builds an Etsy shop banner for Bramble & Brain Co., showcasing the flagship
plus the 3 new printable products in a staggered carousel/fan layout.

Output: 1600x400 (4:1), the commonly recommended Etsy shop banner ratio.
Etsy's upload dialog lets you reposition/crop after upload if needed.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from _brand_kit import (
    pil_font, center_text, brand_tag,
    PIL_F_BOLD, PIL_F_SEMI, PIL_N_REG, PIL_N_SEMI, PIL_N_BOLD,
    P_CREAM, P_CREAM_DEEP, P_TERRACOTTA, P_TERRACOTTA_DARK, P_TERRACOTTA_TINT,
    P_SAGE, P_SAGE_DARK, P_SAGE_TINT, P_MARIGOLD, P_MARIGOLD_TINT,
    P_INK, P_INK_MUTED, P_WHITE,
)

OUT_PATH = os.path.join(os.path.dirname(__file__), "shop_banner.jpg")

SCALE = 2  # supersample for crisp text/edges, then downscale
W, H = 1600 * SCALE, 400 * SCALE

DOT_OFFSETS = [
    (-0.45, -0.50, 0.11), (0.50, -0.55, 0.09), (0.70, 0.10, 0.13),
    (0.40, 0.65, 0.10), (-0.52, 0.50, 0.08), (-0.65, -0.05, 0.12),
]


def draw_mark(d, cx, cy, r, ring_bg=P_TERRACOTTA, dot_color=P_CREAM, focus_color=P_MARIGOLD):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ring_bg)
    for dx, dy, rr in DOT_OFFSETS:
        rad = rr * r
        px, py = cx + dx * r, cy + dy * r
        d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=dot_color)
    fr = 0.42 * r
    d.ellipse([cx - fr, cy - fr, cx + fr, cy + fr], fill=focus_color)


def rounded_card_with_shadow(base, img, cx, cy, target_w, angle, shadow_opacity=90):
    r = target_w / img.width
    img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    pad = 14 * SCALE
    card = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card.width, card.height], radius=16 * SCALE, fill=P_WHITE + (255,))
    card.paste(img, (pad, pad))

    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([0, 0, card.width, card.height], radius=16 * SCALE, fill=(20, 14, 10, shadow_opacity))
    shadow = shadow.rotate(angle, resample=Image.BICUBIC, expand=True)
    shadow = shadow.filter(ImageFilter.GaussianBlur(10 * SCALE))
    rotated = card.rotate(angle, resample=Image.BICUBIC, expand=True)

    sx = int(cx - shadow.width / 2) + 6 * SCALE
    sy = int(cy - shadow.height / 2) + 10 * SCALE
    base.paste(shadow, (sx, sy), shadow)
    rx = int(cx - rotated.width / 2)
    ry = int(cy - rotated.height / 2)
    base.paste(rotated, (rx, ry), rotated)


def load_page(path, target_w=None):
    im = Image.open(path).convert("RGB")
    if target_w:
        r = target_w / im.width
        im = im.resize((target_w, int(im.height * r)), Image.LANCZOS)
    return im


def build():
    im = Image.new("RGB", (W, H), P_CREAM)
    d = ImageDraw.Draw(im)

    # right-side tinted panel behind the carousel
    panel_x = int(W * 0.36)
    d.rectangle([panel_x, 0, W, H], fill=P_TERRACOTTA_TINT)
    # soft diagonal blend strip
    for i in range(60):
        x = panel_x - 60 * SCALE + i * SCALE
        t = i / 60
        col = tuple(int(P_CREAM[j] * (1 - t) + P_TERRACOTTA_TINT[j] * t) for j in range(3))
        d.line([(x, 0), (x, H)], fill=col)

    # ---- left brand block ----
    mark_cx, mark_cy, mark_r = int(W * 0.15), int(H * 0.36), 46 * SCALE
    draw_mark(d, mark_cx, mark_cy, mark_r)

    center_text(d, W * 0.18, H * 0.56, "BRAMBLE & BRAIN CO.", pil_font(PIL_N_BOLD, 30 * SCALE), P_TERRACOTTA_DARK)
    tagline_lines = ["ADHD-friendly printable", "planning systems"]
    ty = H * 0.68
    for line in tagline_lines:
        center_text(d, W * 0.18, ty, line, pil_font(PIL_F_SEMI, 26 * SCALE), P_INK_MUTED)
        ty += 34 * SCALE

    # ---- right: staggered carousel of product covers ----
    products = [
        (os.path.join(os.path.dirname(__file__), "..", "listing_images", "page_1.png"), -7),
        (os.path.join(os.path.dirname(__file__), "..", "time-blindness-timeline", "listing_images", "page_1.png"), 4),
        (os.path.join(os.path.dirname(__file__), "..", "dopamine-menu-tracker", "listing_images", "page_1.png"), -4),
        (os.path.join(os.path.dirname(__file__), "..", "low-spoons-checklist", "listing_images", "page_1.png"), 7),
    ]
    n = len(products)
    carousel_left = panel_x + 40 * SCALE
    carousel_right = W - 30 * SCALE
    span = carousel_right - carousel_left
    card_w = int(span / n * 0.92)
    for i, (path, angle) in enumerate(products):
        cx = carousel_left + span * (i + 0.5) / n
        cy = H * 0.53
        img = load_page(os.path.abspath(path), target_w=card_w)
        rounded_card_with_shadow(im, img, cx, cy, card_w, angle)

    im = im.resize((1600, 400), Image.LANCZOS)
    im.save(OUT_PATH, quality=94)
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
