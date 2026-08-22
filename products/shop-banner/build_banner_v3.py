# -*- coding: utf-8 -*-
"""Shop banner variation 3: bold color-block poster — full-bleed alternating
brand-color panels, one per product, with name labels. 1600x400."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from _brand_kit import (
    pil_font, center_text,
    PIL_F_BOLD, PIL_N_SEMI, PIL_N_BOLD,
    P_CREAM, P_TERRACOTTA, P_TERRACOTTA_DARK, P_TERRACOTTA_TINT,
    P_SAGE, P_SAGE_DARK, P_SAGE_TINT, P_MARIGOLD, P_MARIGOLD_TINT,
    P_INK, P_WHITE,
)

OUT_PATH = os.path.join(os.path.dirname(__file__), "shop_banner_v3_color_blocks.jpg")
SCALE = 2
W, H = 1600 * SCALE, 400 * SCALE

DOT_OFFSETS = [
    (-0.45, -0.50, 0.11), (0.50, -0.55, 0.09), (0.70, 0.10, 0.13),
    (0.40, 0.65, 0.10), (-0.52, 0.50, 0.08), (-0.65, -0.05, 0.12),
]


def draw_mark(d, cx, cy, r, ring_bg, dot_color, focus_color=P_MARIGOLD):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=ring_bg)
    for dx, dy, rr in DOT_OFFSETS:
        rad = rr * r
        px, py = cx + dx * r, cy + dy * r
        d.ellipse([px - rad, py - rad, px + rad, py + rad], fill=dot_color)
    fr = 0.42 * r
    d.ellipse([cx - fr, cy - fr, cx + fr, cy + fr], fill=focus_color)


def card_with_shadow(base, img, cx, cy, target_w, shadow_opacity=70):
    r = target_w / img.width
    img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    pad = 8 * SCALE
    card = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card.width, card.height], radius=10 * SCALE, fill=P_WHITE + (255,))
    card.paste(img, (pad, pad))

    shadow = Image.new("RGBA", (card.width + 40 * SCALE, card.height + 40 * SCALE), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([20 * SCALE, 22 * SCALE, 20 * SCALE + card.width, 22 * SCALE + card.height],
                          radius=10 * SCALE, fill=(20, 14, 10, shadow_opacity))
    shadow = shadow.filter(ImageFilter.GaussianBlur(7 * SCALE))
    x, y = int(cx - card.width / 2), int(cy - card.height / 2)
    base.paste(shadow, (x - 20 * SCALE, y - 18 * SCALE), shadow)
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

    base_dir = os.path.join(os.path.dirname(__file__), "..")
    brand_w = int(W * 0.185)

    # brand block (solid terracotta)
    d.rectangle([0, 0, brand_w, H], fill=P_TERRACOTTA)
    draw_mark(d, brand_w / 2, H * 0.34, 42 * SCALE, ring_bg=P_TERRACOTTA_DARK, dot_color=P_CREAM)
    center_text(d, brand_w / 2, H * 0.52, "BRAMBLE", pil_font(PIL_F_BOLD, 30 * SCALE), P_CREAM)
    center_text(d, brand_w / 2, H * 0.59, "& BRAIN CO.", pil_font(PIL_F_BOLD, 30 * SCALE), P_CREAM)
    center_text(d, brand_w / 2, H * 0.70, "ADHD-friendly", pil_font(PIL_N_SEMI, 17 * SCALE), P_MARIGOLD)
    center_text(d, brand_w / 2, H * 0.755, "printables", pil_font(PIL_N_SEMI, 17 * SCALE), P_MARIGOLD)

    panels = [
        (os.path.join(base_dir, "listing_images", "page_1.png"), P_TERRACOTTA_TINT, "ADHD LIFE OS", P_TERRACOTTA_DARK),
        (os.path.join(base_dir, "time-blindness-timeline", "listing_images", "page_1.png"), P_CREAM, "TIME-BLINDNESS", P_TERRACOTTA_DARK),
        (os.path.join(base_dir, "dopamine-menu-tracker", "listing_images", "page_1.png"), P_MARIGOLD_TINT, "DOPAMINE MENU", P_TERRACOTTA_DARK),
        (os.path.join(base_dir, "low-spoons-checklist", "listing_images", "page_1.png"), P_SAGE_TINT, "LOW-SPOONS", P_SAGE_DARK),
    ]
    n = len(panels)
    panel_w = (W - brand_w) / n
    for i, (path, bg, label, label_color) in enumerate(panels):
        x0 = brand_w + i * panel_w
        d.rectangle([x0, 0, x0 + panel_w, H], fill=bg)
        if i > 0:
            d.line([(x0, 0), (x0, H)], fill=P_WHITE, width=2 * SCALE)

        card_w = int(panel_w * 0.62)
        cx = x0 + panel_w / 2
        cy = H * 0.44
        img = load_page(os.path.abspath(path), target_w=card_w)
        max_h = H * 0.72
        if img.height > max_h:
            r2 = max_h / img.height
            img = img.resize((int(img.width * r2), int(img.height * r2)), Image.LANCZOS)
        card_with_shadow(im, img, cx, cy, img.width)

        center_text(d, cx, H * 0.87, label, pil_font(PIL_N_BOLD, 15 * SCALE), label_color)

    im = im.resize((1600, 400), Image.LANCZOS)
    im.save(OUT_PATH, quality=94)
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
