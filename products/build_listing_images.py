# -*- coding: utf-8 -*-
"""Builds Etsy listing photo set for 'The ADHD Life OS — Printable Edition'."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

BASE = "/tmp/claude-0/-home-user-dgroup-booking/6e18ded9-e301-5997-b108-de22bc28193a/scratchpad/etsy-co/products"
IMG_DIR = os.path.join(BASE, "listing_images")
FONT_DIR = "/tmp/claude-0/fonts/"

CREAM = (250, 243, 233)
CREAM_DEEP = (241, 228, 208)
TERRACOTTA = (192, 101, 68)
TERRACOTTA_DARK = (143, 73, 48)
TERRACOTTA_TINT = (240, 220, 207)
SAGE = (140, 155, 124)
SAGE_DARK = (95, 107, 84)
SAGE_TINT = (228, 232, 220)
MARIGOLD = (232, 169, 74)
MARIGOLD_TINT = (251, 236, 210)
INK = (74, 59, 50)
INK_MUTED = (110, 90, 78)
WHITE = (255, 255, 255)

W = H = 2000


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_BOLD = "Fredoka-Bold.ttf"
F_SEMI = "Fredoka-SemiBold.ttf"
N_REG = "Nunito-Regular.ttf"
N_SEMI = "Nunito-SemiBold.ttf"
N_BOLD = "Nunito-Bold.ttf"


def new_canvas(bg=CREAM):
    return Image.new("RGB", (W, H), bg)


def center_text(draw, cx, y, text, f, fill):
    bbox = draw.textbbox((0, 0), text, font=f)
    w = bbox[2] - bbox[0]
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return bbox[3] - bbox[1]


def wrap_text(draw, text, f, max_w):
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


def rounded_border(draw, box, radius=18, outline=CREAM_DEEP, width=3):
    draw.rounded_rectangle(box, radius=radius, outline=outline, width=width)


def brand_tag(draw, y=1940):
    center_text(draw, W / 2, y, "B R A M B L E   &   B R A I N   C O .", font(N_BOLD, 26), TERRACOTTA)


def load_page(n, target_w=None):
    im = Image.open(os.path.join(IMG_DIR, f"page_{n}.png")).convert("RGB")
    if target_w:
        r = target_w / im.width
        im = im.resize((target_w, int(im.height * r)), Image.LANCZOS)
    return im


# ---------------------------------------------------------------- IMAGE 1: HERO
def img_hero():
    im = new_canvas()
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 90, "The ADHD Life OS", font(F_BOLD, 118), TERRACOTTA_DARK)
    center_text(d, W / 2, 232, "Printable Planner System", font(F_SEMI, 54), SAGE_DARK)

    cover = load_page(1, target_w=1140)
    paste_with_shadow(im, cover, int((W - cover.width) / 2), 350)

    badge_w, badge_h = 640, 90
    bx, by = int((W - badge_w) / 2), 1870 - badge_h - 30
    d.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=45, fill=MARIGOLD)
    center_text(d, W / 2, by + 24, "8-PAGE PDF  ·  INSTANT DOWNLOAD", font(N_BOLD, 30), TERRACOTTA_DARK)
    brand_tag(d)
    im.save(os.path.join(IMG_DIR, "listing_1_hero.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 2: WHAT'S INSIDE COLLAGE
def img_collage():
    im = new_canvas()
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 80, "What's Inside", font(F_BOLD, 96), TERRACOTTA_DARK)
    center_text(d, W / 2, 200, "8 pages, designed around how ADHD brains actually work", font(N_SEMI, 34), INK_MUTED)

    items = [(3, "Weekly Overview"), (4, "Daily Page"), (5, "Dopamine Menu"), (7, "Low-Spoons Mode")]
    cell_w, cell_h = 880, 760
    gap = 40
    grid_w = cell_w * 2 + gap
    start_x = int((W - grid_w) / 2)
    start_y = 300
    for i, (pnum, label) in enumerate(items):
        col, row = i % 2, i // 2
        x = start_x + col * (cell_w + gap)
        y = start_y + row * (cell_h + gap)
        d.rounded_rectangle([x, y, x + cell_w, y + cell_h], radius=24, fill=WHITE, outline=CREAM_DEEP, width=3)
        page_im = load_page(pnum, target_w=cell_w - 80)
        max_h = cell_h - 140
        if page_im.height > max_h:
            r = max_h / page_im.height
            page_im = page_im.resize((int(page_im.width * r), max_h), Image.LANCZOS)
        px = x + int((cell_w - page_im.width) / 2)
        py = y + 30
        im.paste(page_im, (px, py))
        center_text(d, x + cell_w / 2, y + cell_h - 78, label, font(N_BOLD, 34), TERRACOTTA_DARK)
    brand_tag(d)
    im.save(os.path.join(IMG_DIR, "listing_2_whats_inside.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 3: TIMELINE CALLOUT
def img_timeline_callout():
    im = new_canvas(bg=TERRACOTTA_TINT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 780, H], fill=CREAM)

    tx = 90
    y = 260
    for line in ["Time blindness", "gets a real", "visual timeline."]:
        d.text((tx, y), line, font=font(F_BOLD, 78), fill=TERRACOTTA_DARK)
        y += 96
    y += 40
    for line in wrap_text(d, "Not just an hour-by-hour list — color-coded blocks for morning, midday, afternoon, and evening, so “what time is it, actually” stops being the hard part.", font(N_REG, 34), 600):
        d.text((tx, y), line, font=font(N_REG, 34), fill=INK_MUTED)
        y += 46

    page_im = load_page(4, target_w=1180)
    max_h = H - 240
    if page_im.height > max_h:
        r = max_h / page_im.height
        page_im = page_im.resize((int(page_im.width * r), max_h), Image.LANCZOS)
    paste_with_shadow(im, page_im, 900, int((H - page_im.height) / 2))
    brand_tag(d)
    im.save(os.path.join(IMG_DIR, "listing_3_timeline.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 4: LOW-SPOONS CALLOUT
def img_low_spoons_callout():
    im = new_canvas(bg=SAGE_TINT)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 780, H], fill=CREAM)

    tx = 90
    y = 260
    for line in ["For the days", "that are just", "… a lot."]:
        d.text((tx, y), line, font=font(F_BOLD, 78), fill=SAGE_DARK)
        y += 96
    y += 40
    for line in wrap_text(d, "A stripped-down page for hard days: 1-3 must-dos, bare-minimum self-care, and a reminder that rest is not falling behind.", font(N_REG, 34), 600):
        d.text((tx, y), line, font=font(N_REG, 34), fill=INK_MUTED)
        y += 46

    page_im = load_page(7, target_w=1180)
    max_h = H - 240
    if page_im.height > max_h:
        r = max_h / page_im.height
        page_im = page_im.resize((int(page_im.width * r), max_h), Image.LANCZOS)
    paste_with_shadow(im, page_im, 900, int((H - page_im.height) / 2))
    brand_tag(d)
    im.save(os.path.join(IMG_DIR, "listing_4_low_spoons.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 5: WHAT'S INCLUDED LIST
def img_checklist():
    im = new_canvas(bg=TERRACOTTA_DARK)
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 130, "What You Get", font(F_BOLD, 92), CREAM)
    center_text(d, W / 2, 250, "One 8-page PDF, ready to print at home", font(N_SEMI, 36), MARIGOLD)

    pages = [
        "Cover + How This Works",
        "Weekly Overview (top 3 priorities, day-by-day)",
        "Daily Page (visual timeline + brain dump)",
        "Dopamine Menu + 4-Week Reward Tracker",
        "Habit Tracker (up to 5 habits, 31 days)",
        "Low-Spoons Mode (for the hard days)",
        "Medication & Symptom Tracker",
    ]
    y = 420
    for p in pages:
        d.ellipse([90, y + 14, 106, y + 30], fill=MARIGOLD)
        d.text((140, y), p, font=font(N_SEMI, 38), fill=CREAM)
        y += 92

    d.rounded_rectangle([90, y + 30, W - 90, y + 170], radius=20, fill=TERRACOTTA)
    for i, line in enumerate(["Instant PDF download  ·  US Letter (8.5″ × 11″)", "Print at home, as many times as you like  ·  Personal use"]):
        center_text(d, W / 2, y + 60 + i * 50, line, font(N_SEMI, 30), CREAM)
    brand_tag(d, y=1940)
    im.save(os.path.join(IMG_DIR, "listing_5_whats_included.jpg"), quality=92)


# ---------------------------------------------------------------- IMAGE 6: FAQ / GOOD TO KNOW
def img_faq():
    im = new_canvas(bg=CREAM_DEEP)
    d = ImageDraw.Draw(im)
    center_text(d, W / 2, 130, "Good to Know", font(F_BOLD, 92), TERRACOTTA_DARK)

    rows = [
        ("Format", "One PDF file, delivered instantly after purchase — no waiting, no shipping."),
        ("Size", "US Letter (8.5″ × 11″). Print at home or at any copy shop."),
        ("Devices", "Opens on anything that reads a PDF — phone, tablet, or computer."),
        ("Use", "For personal use. Print it as many times as you need for yourself."),
        ("Support", "File trouble or questions? Message the shop — we reply fast."),
    ]
    y = 300
    for label, desc in rows:
        d.rounded_rectangle([90, y, W - 90, y + 240], radius=20, fill=WHITE, outline=CREAM_DEEP, width=2)
        d.text((130, y + 30), label.upper(), font=font(N_BOLD, 30), fill=TERRACOTTA)
        ty = y + 90
        for line in wrap_text(d, desc, font(N_REG, 34), W - 260):
            d.text((130, ty), line, font=font(N_REG, 34), fill=INK)
            ty += 44
        y += 270
    brand_tag(d, y=1940)
    im.save(os.path.join(IMG_DIR, "listing_6_faq.jpg"), quality=92)


if __name__ == "__main__":
    img_hero()
    img_collage()
    img_timeline_callout()
    img_low_spoons_callout()
    img_checklist()
    img_faq()
    print("done")
