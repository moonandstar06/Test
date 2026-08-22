# -*- coding: utf-8 -*-
"""Shop banner variation 2: clean flat filmstrip — evenly spaced, no rotation,
minimal/gallery feel. 1600x400."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from _brand_kit import (
    pil_font, center_text,
    PIL_F_SEMI, PIL_N_SEMI, PIL_N_BOLD,
    P_CREAM, P_CREAM_DEEP, P_TERRACOTTA, P_TERRACOTTA_DARK,
    P_MARIGOLD, P_INK_MUTED, P_WHITE,
)

OUT_PATH = os.path.join(os.path.dirname(__file__), "shop_banner_v2_flat_filmstrip.jpg")
SCALE = 2
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


def card_with_shadow(base, img, x, y, target_w, shadow_opacity=60):
    r = target_w / img.width
    img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    pad = 10 * SCALE
    card = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card.width, card.height], radius=12 * SCALE, fill=P_WHITE + (255,))
    card.paste(img, (pad, pad))

    shadow = Image.new("RGBA", (card.width + 40 * SCALE, card.height + 40 * SCALE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([20 * SCALE, 24 * SCALE, 20 * SCALE + card.width, 24 * SCALE + card.height],
                          radius=12 * SCALE, fill=(20, 14, 10, shadow_opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(8 * SCALE))
    base.paste(shadow, (x - 20 * SCALE, y - 20 * SCALE), shadow)
    base.paste(card, (x, y), card)


def load_page(path, target_w=None):
    im = Image.open(path).convert("RGB")
    if target_w:
        r = target_w / im.width
        im = im.resize((target_w, int(im.height * r)), Image.LANCZOS)
    return im


def build():
    im = Image.new("RGB", (W, H), P_CREAM)
    d = ImageDraw.Draw(im)

    # thin brand strip at the very top
    strip_h = 6 * SCALE
    d.rectangle([0, 0, W, strip_h], fill=P_TERRACOTTA)

    mark_cx, mark_cy, mark_r = int(W * 0.085), int(H * 0.30), 34 * SCALE
    draw_mark(d, mark_cx, mark_cy, mark_r)
    center_text(d, W * 0.085, H * 0.46, "BRAMBLE & BRAIN CO.", pil_font(PIL_N_BOLD, 20 * SCALE), P_TERRACOTTA_DARK)
    center_text(d, W * 0.085, H * 0.55, "ADHD-friendly printables", pil_font(PIL_N_SEMI, 16 * SCALE), P_INK_MUTED)

    d.line([(W * 0.16, H * 0.18), (W * 0.16, H * 0.62)], fill=P_CREAM_DEEP, width=2 * SCALE)

    base = os.path.join(os.path.dirname(__file__), "..")
    products = [
        os.path.join(base, "listing_images", "page_1.png"),
        os.path.join(base, "time-blindness-timeline", "listing_images", "page_1.png"),
        os.path.join(base, "dopamine-menu-tracker", "listing_images", "page_1.png"),
        os.path.join(base, "low-spoons-checklist", "listing_images", "page_1.png"),
    ]
    n = len(products)
    strip_left = W * 0.20
    strip_right = W - 30 * SCALE
    span = strip_right - strip_left
    card_w = int(span / n * 0.86)
    card_h_target = int(H * 0.72)
    y = int(H * 0.14)
    for i, path in enumerate(products):
        cx0 = strip_left + span * (i + 0.5) / n
        img = load_page(os.path.abspath(path), target_w=card_w)
        if img.height > card_h_target - 20 * SCALE:
            r2 = (card_h_target - 20 * SCALE) / img.height
            img = img.resize((int(img.width * r2), int(img.height * r2)), Image.LANCZOS)
        x = int(cx0 - img.width / 2)
        card_with_shadow(im, img, x, y, img.width)

    im = im.resize((1600, 400), Image.LANCZOS)
    im.save(OUT_PATH, quality=94)
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
