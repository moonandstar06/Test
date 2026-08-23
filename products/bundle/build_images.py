# -*- coding: utf-8 -*-
"""Builds listing images for 'The Founding Bundle' — all 4 printables + bonus."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from PIL import Image, ImageDraw, ImageFilter
from _brand_kit import (
    pil_font, new_canvas, center_text, pil_wrap_text, brand_tag,
    PIL_F_BOLD, PIL_F_SEMI, PIL_N_REG, PIL_N_SEMI, PIL_N_BOLD,
    P_CREAM, P_CREAM_DEEP, P_TERRACOTTA, P_TERRACOTTA_DARK, P_TERRACOTTA_TINT,
    P_SAGE, P_SAGE_DARK, P_SAGE_TINT, P_MARIGOLD, P_MARIGOLD_TINT,
    P_INK, P_INK_MUTED, P_WHITE, IMG_W, IMG_H,
)

HERE = os.path.dirname(__file__)
IMG_DIR = os.path.join(HERE, "listing_images")
BASE = os.path.join(HERE, "..")


def pill(d, cx, cy, text, bg, text_color, pad_x=26, h=60, font_size=26):
    f = pil_font(PIL_N_BOLD, font_size)
    bbox = d.textbbox((0, 0), text, font=f)
    w = (bbox[2] - bbox[0]) + pad_x * 2
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=bg)
    center_text(d, cx, y0 + (h - (bbox[3] - bbox[1])) / 2 - bbox[1], text, f, text_color)
    return w


def pill_row(d, cy, items, gap=20):
    f = pil_font(PIL_N_BOLD, 26)
    widths = []
    for text, bg, tc in items:
        bbox = d.textbbox((0, 0), text, font=f)
        widths.append(bbox[2] - bbox[0] + 26 * 2)
    total_w = sum(widths) + gap * (len(items) - 1)
    cx = (IMG_W - total_w) / 2
    for (text, bg, tc), w in zip(items, widths):
        pill(d, cx + w / 2, cy, text, bg, tc)
        cx += w + gap


def rounded_card_with_shadow(base, img, cx, cy, target_w, angle, shadow_opacity=90):
    r = target_w / img.width
    img = img.resize((int(img.width * r), int(img.height * r)), Image.LANCZOS)
    pad = 12
    card = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    cd.rounded_rectangle([0, 0, card.width, card.height], radius=14, fill=P_WHITE + (255,))
    card.paste(img, (pad, pad))

    shadow = Image.new("RGBA", card.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([0, 0, card.width, card.height], radius=14, fill=(20, 14, 10, shadow_opacity))
    shadow = shadow.rotate(angle, resample=Image.BICUBIC, expand=True)
    shadow = shadow.filter(ImageFilter.GaussianBlur(9))
    rotated = card.rotate(angle, resample=Image.BICUBIC, expand=True)

    sx = int(cx - shadow.width / 2) + 5
    sy = int(cy - shadow.height / 2) + 8
    base.paste(shadow, (sx, sy), shadow)
    rx = int(cx - rotated.width / 2)
    ry = int(cy - rotated.height / 2)
    base.paste(rotated, (rx, ry), rotated)


def load_cover(path, target_w):
    im = Image.open(path).convert("RGB")
    r = target_w / im.width
    return im.resize((target_w, int(im.height * r)), Image.LANCZOS)


# ---------------------------------------------------------------- IMAGE 1: HERO
def img_hero():
    im = new_canvas()
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 60, "THE FOUNDING BUNDLE", pil_font(PIL_F_BOLD, 88), P_TERRACOTTA_DARK)
    for i, line in enumerate(["All 4 ADHD Life OS printables", "+ a bonus — one price."]):
        center_text(d, IMG_W / 2, 172 + i * 56, line, pil_font(PIL_F_SEMI, 42), P_SAGE_DARK)

    covers = [
        (os.path.join(BASE, "listing_images", "page_1.png"), -8),
        (os.path.join(BASE, "time-blindness-timeline", "listing_images", "page_1.png"), -3),
        (os.path.join(BASE, "dopamine-menu-tracker", "listing_images", "page_1.png"), 3),
        (os.path.join(BASE, "low-spoons-checklist", "listing_images", "page_1.png"), 8),
    ]
    card_w = 420
    cy = 900
    span = IMG_W - 160
    left = 80
    for i, (path, angle) in enumerate(covers):
        cx = left + span * (i + 0.5) / len(covers)
        img = load_cover(os.path.abspath(path), card_w)
        rounded_card_with_shadow(im, img, cx, cy, card_w, angle)

    py = 1560
    pill_row(d, py, [
        ("$49 VALUE", P_CREAM_DEEP, P_INK_MUTED),
        ("→", P_CREAM, P_INK_MUTED),
        ("$19 LAUNCH PRICE", P_TERRACOTTA, P_CREAM),
    ], gap=14)
    pill_row(d, py + 84, [
        ("+ BONUS QUICK-START CHEAT SHEET", P_MARIGOLD, P_TERRACOTTA_DARK),
    ])
    center_text(d, IMG_W / 2, py + 160, "B R A M B L E   &   B R A I N   C O .", pil_font(PIL_N_BOLD, 24), P_TERRACOTTA)
    im.save(os.path.join(IMG_DIR, "listing_1_hero.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 2: WHAT'S INCLUDED (value stack)
def img_value_stack():
    im = new_canvas(bg=P_TERRACOTTA_DARK)
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 100, "What's Included", pil_font(PIL_F_BOLD, 84), P_CREAM)
    center_text(d, IMG_W / 2, 210, "5 PDFs, one download, instant delivery", pil_font(PIL_N_SEMI, 32), P_MARIGOLD)

    rows = [
        ("The ADHD Life OS (8 pages)", "$22"),
        ("Time-Blindness Daily Timeline", "$9"),
        ("Dopamine Menu + Reward Tracker", "$9"),
        ("Low-Spoons Mode Checklist", "$9"),
        ("Quick-Start Cheat Sheet", "BONUS"),
    ]
    y = 380
    for label, price in rows:
        d.rounded_rectangle([90, y, IMG_W - 90, y + 130], radius=16, fill=P_TERRACOTTA)
        d.text((130, y + 45), label, font=pil_font(PIL_N_SEMI, 34), fill=P_CREAM)
        f = pil_font(PIL_N_BOLD, 34)
        bbox = d.textbbox((0, 0), price, font=f)
        d.text((IMG_W - 130 - (bbox[2] - bbox[0]), y + 45), price, font=f, fill=P_MARIGOLD)
        y += 150

    y += 20
    d.rounded_rectangle([90, y, IMG_W - 90, y + 150], radius=16, fill=P_MARIGOLD)
    center_text(d, IMG_W / 2, y + 24, "TOTAL VALUE: $49", pil_font(PIL_N_BOLD, 30), P_TERRACOTTA_DARK)
    center_text(d, IMG_W / 2, y + 72, "YOUR PRICE: $19", pil_font(PIL_F_BOLD, 42), P_TERRACOTTA_DARK)
    brand_tag(d, y=1940)
    im.save(os.path.join(IMG_DIR, "listing_2_value_stack.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 3: GUARANTEE
def img_guarantee():
    im = new_canvas(bg=P_SAGE_TINT)
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 140, "Our Promise", pil_font(PIL_F_BOLD, 96), P_SAGE_DARK)

    box_y = 340
    box_h = 1500
    d.rounded_rectangle([120, box_y, IMG_W - 120, box_y + box_h], radius=28, fill=P_WHITE, outline=P_CREAM_DEEP, width=3)

    # big quote mark accent
    center_text(d, IMG_W / 2, box_y + 60, "“", pil_font(PIL_F_BOLD, 160), P_SAGE_TINT)

    lines = [
        "If it's not helping within 7 days,",
        "message us and we'll make it right —",
        "no hoops, no hard feelings.",
    ]
    ty = box_y + 340
    for line in lines:
        center_text(d, IMG_W / 2, ty, line, pil_font(PIL_F_SEMI, 58), P_TERRACOTTA_DARK)
        ty += 84
    ty += 60
    for line in pil_wrap_text(d, "We built this because generic planners failed us too.", pil_font(PIL_N_REG, 38), 1400):
        center_text(d, IMG_W / 2, ty, line, pil_font(PIL_N_REG, 38), P_INK_MUTED)
        ty += 52
    for line in pil_wrap_text(d, "We want it to actually work for you.", pil_font(PIL_N_REG, 38), 1400):
        center_text(d, IMG_W / 2, ty, line, pil_font(PIL_N_REG, 38), P_INK_MUTED)
        ty += 52

    ty += 60
    pill(d, IMG_W / 2, ty + 30, "7-DAY MAKE-IT-RIGHT PROMISE", P_SAGE_DARK, P_CREAM, pad_x=34, h=76, font_size=32)

    brand_tag(d, y=1940)
    im.save(os.path.join(IMG_DIR, "listing_3_guarantee.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 4: FAQ
def img_faq():
    im = new_canvas(bg=P_CREAM_DEEP)
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 130, "Good to Know", pil_font(PIL_F_BOLD, 92), P_TERRACOTTA_DARK)

    rows = [
        ("Format", "5 PDF files, delivered instantly after purchase — no waiting, no shipping."),
        ("Size", "US Letter (8.5″ × 11″). Print at home or at any copy shop."),
        ("Devices", "Opens on anything that reads a PDF — phone, tablet, or computer."),
        ("Price", "$19 launch price for a limited time, then back to $49 separately."),
        ("Support", "Questions or issues? Message the shop — we reply fast."),
    ]
    y = 300
    for label, desc in rows:
        d.rounded_rectangle([90, y, IMG_W - 90, y + 240], radius=20, fill=P_WHITE, outline=P_CREAM_DEEP, width=2)
        d.text((130, y + 30), label.upper(), font=pil_font(PIL_N_BOLD, 30), fill=P_TERRACOTTA)
        ty = y + 90
        for line in pil_wrap_text(d, desc, pil_font(PIL_N_REG, 34), IMG_W - 260):
            d.text((130, ty), line, font=pil_font(PIL_N_REG, 34), fill=P_INK)
            ty += 44
        y += 270
    brand_tag(d, y=1940)
    im.save(os.path.join(IMG_DIR, "listing_4_faq.jpg"), quality=92)


if __name__ == "__main__":
    img_hero()
    img_value_stack()
    img_guarantee()
    img_faq()
    print("done")
