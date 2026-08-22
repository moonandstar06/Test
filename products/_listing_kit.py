# -*- coding: utf-8 -*-
"""Generic 6-image Etsy listing photo builder for Bramble & Brain Co. printables."""
import os
from PIL import Image, ImageDraw
from _brand_kit import (
    pil_font, new_canvas, center_text, pil_wrap_text, paste_with_shadow, brand_tag,
    PIL_F_BOLD, PIL_F_SEMI, PIL_N_REG, PIL_N_SEMI, PIL_N_BOLD,
    P_CREAM, P_CREAM_DEEP, P_TERRACOTTA, P_TERRACOTTA_DARK, P_TERRACOTTA_TINT,
    P_SAGE, P_SAGE_DARK, P_SAGE_TINT, P_MARIGOLD, P_MARIGOLD_TINT,
    P_INK, P_INK_MUTED, P_WHITE, IMG_W, IMG_H,
)


def load_page(img_dir, n, target_w=None):
    im = Image.open(os.path.join(img_dir, f"page_{n}.png")).convert("RGB")
    if target_w:
        r = target_w / im.width
        im = im.resize((target_w, int(im.height * r)), Image.LANCZOS)
    return im


def build_hero(img_dir, out_path, title, subtitle, badge_text, cover_page=1, title_size=100):
    im = new_canvas()
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 100, title, pil_font(PIL_F_BOLD, title_size), P_TERRACOTTA_DARK)
    center_text(d, IMG_W / 2, 100 + title_size + 24, subtitle, pil_font(PIL_F_SEMI, 48), P_SAGE_DARK)

    cover = load_page(img_dir, cover_page, target_w=1180)
    top = 100 + title_size + 24 + 70
    paste_with_shadow(im, cover, int((IMG_W - cover.width) / 2), top)

    badge_w, badge_h = 700, 90
    bx, by = int((IMG_W - badge_w) / 2), 1870 - badge_h - 30
    d.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=45, fill=P_MARIGOLD)
    center_text(d, IMG_W / 2, by + 24, badge_text, pil_font(PIL_N_BOLD, 30), P_TERRACOTTA_DARK)
    brand_tag(d)
    im.save(out_path, quality=92)


def build_collage(img_dir, out_path, title, subtitle, items):
    """items: list of (page_num, label) — up to 2, shown side by side, large."""
    im = new_canvas()
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 80, title, pil_font(PIL_F_BOLD, 92), P_TERRACOTTA_DARK)
    for line in pil_wrap_text(d, subtitle, pil_font(PIL_N_SEMI, 34), 1700):
        center_text(d, IMG_W / 2, 200, line, pil_font(PIL_N_SEMI, 34), P_INK_MUTED)

    n = len(items)
    cell_w = 880 if n > 1 else 1300
    cell_h = 1460
    gap = 40
    grid_w = cell_w * n + gap * (n - 1)
    start_x = int((IMG_W - grid_w) / 2)
    start_y = 300
    for i, (pnum, label) in enumerate(items):
        x = start_x + i * (cell_w + gap)
        y = start_y
        d.rounded_rectangle([x, y, x + cell_w, y + cell_h], radius=24, fill=P_WHITE, outline=P_CREAM_DEEP, width=3)
        page_im = load_page(img_dir, pnum, target_w=cell_w - 80)
        max_h = cell_h - 140
        if page_im.height > max_h:
            r = max_h / page_im.height
            page_im = page_im.resize((int(page_im.width * r), max_h), Image.LANCZOS)
        px = x + int((cell_w - page_im.width) / 2)
        py = y + 30
        im.paste(page_im, (px, py))
        center_text(d, x + cell_w / 2, y + cell_h - 78, label, pil_font(PIL_N_BOLD, 34), P_TERRACOTTA_DARK)
    brand_tag(d)
    im.save(out_path, quality=92)


def build_callout(img_dir, out_path, page_num, headline_lines, body_text, accent_bg=P_TERRACOTTA_TINT, headline_color=P_TERRACOTTA_DARK):
    im = new_canvas(bg=accent_bg)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 780, IMG_H], fill=P_CREAM)

    tx = 90
    y = 260
    for line in headline_lines:
        d.text((tx, y), line, font=pil_font(PIL_F_BOLD, 74), fill=headline_color)
        y += 92
    y += 40
    for line in pil_wrap_text(d, body_text, pil_font(PIL_N_REG, 32), 600):
        d.text((tx, y), line, font=pil_font(PIL_N_REG, 32), fill=P_INK_MUTED)
        y += 44

    page_im = load_page(img_dir, page_num, target_w=1180)
    max_h = IMG_H - 240
    if page_im.height > max_h:
        r = max_h / page_im.height
        page_im = page_im.resize((int(page_im.width * r), max_h), Image.LANCZOS)
    paste_with_shadow(im, page_im, 900, int((IMG_H - page_im.height) / 2))
    brand_tag(d)
    im.save(out_path, quality=92)


def build_checklist(out_path, title, subtitle, items, footer_lines, bg=P_TERRACOTTA_DARK, accent=P_MARIGOLD, text_color=P_CREAM):
    im = new_canvas(bg=bg)
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 140, title, pil_font(PIL_F_BOLD, 92), text_color)
    center_text(d, IMG_W / 2, 260, subtitle, pil_font(PIL_N_SEMI, 36), accent)

    y = 440
    for p in items:
        d.ellipse([90, y + 14, 106, y + 30], fill=accent)
        d.text((140, y), p, font=pil_font(PIL_N_SEMI, 38), fill=text_color)
        y += 92

    d.rounded_rectangle([90, y + 30, IMG_W - 90, y + 30 + 60 * len(footer_lines) + 60], radius=20, fill=P_TERRACOTTA if bg != P_TERRACOTTA else P_TERRACOTTA_DARK)
    for i, line in enumerate(footer_lines):
        center_text(d, IMG_W / 2, y + 60 + i * 50, line, pil_font(PIL_N_SEMI, 30), text_color)
    brand_tag(d, y=1940)
    im.save(out_path, quality=92)


def build_faq(out_path, title, rows, bg=P_CREAM_DEEP):
    im = new_canvas(bg=bg)
    d = ImageDraw.Draw(im)
    center_text(d, IMG_W / 2, 130, title, pil_font(PIL_F_BOLD, 92), P_TERRACOTTA_DARK)

    row_h = 1900 // len(rows) if len(rows) > 5 else 240
    y = 300
    for label, desc in rows:
        d.rounded_rectangle([90, y, IMG_W - 90, y + row_h - 30], radius=20, fill=P_WHITE, outline=P_CREAM_DEEP, width=2)
        d.text((130, y + 30), label.upper(), font=pil_font(PIL_N_BOLD, 30), fill=P_TERRACOTTA)
        ty = y + 90
        for line in pil_wrap_text(d, desc, pil_font(PIL_N_REG, 34), IMG_W - 260):
            d.text((130, ty), line, font=pil_font(PIL_N_REG, 34), fill=P_INK)
            ty += 44
        y += row_h
    brand_tag(d, y=1940)
    im.save(out_path, quality=92)
