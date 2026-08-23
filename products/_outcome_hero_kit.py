# -*- coding: utf-8 -*-
"""Generic outcome-focused hero/thumbnail builder (image #1), same design
language as the flagship's redone hero: headline states the outcome, a real
strong planner page shown large, 3 proof-point pills underneath."""
import os
from PIL import Image, ImageDraw, ImageFilter
from _brand_kit import (
    pil_font, new_canvas, center_text,
    PIL_F_BOLD, PIL_F_SEMI, PIL_N_BOLD,
    P_CREAM, P_TERRACOTTA, P_TERRACOTTA_DARK,
    P_SAGE_DARK, P_MARIGOLD, P_WHITE, IMG_W,
)


def pill(d, cx, cy, text, bg, text_color, pad_x=28, h=64, font_size=28):
    f = pil_font(PIL_N_BOLD, font_size)
    bbox = d.textbbox((0, 0), text, font=f)
    w = (bbox[2] - bbox[0]) + pad_x * 2
    x0, y0 = cx - w / 2, cy - h / 2
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], radius=h / 2, fill=bg)
    center_text(d, cx, y0 + (h - (bbox[3] - bbox[1])) / 2 - bbox[1], text, f, text_color)
    return w


def build_outcome_hero(img_dir, page_num, title, subtitle, pills, out_path, title_size=92):
    im = new_canvas()
    d = ImageDraw.Draw(im)

    center_text(d, IMG_W / 2, 56, title, pil_font(PIL_F_BOLD, title_size), P_TERRACOTTA_DARK)
    center_text(d, IMG_W / 2, 56 + title_size + 24, subtitle, pil_font(PIL_F_SEMI, 46), P_SAGE_DARK)

    raw = Image.open(os.path.join(img_dir, f"page_{page_num}.png")).convert("RGB")
    target_h = 1440
    r = target_h / raw.height
    page = raw.resize((int(raw.width * r), target_h), Image.LANCZOS)

    frame_pad = 14
    fx = (IMG_W - page.width) // 2
    fy = 56 + title_size + 24 + 46 + 46

    shadow = Image.new("RGBA", (page.width + frame_pad * 2 + 60, page.height + frame_pad * 2 + 60), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle([30, 34, 30 + page.width + frame_pad * 2, 34 + page.height + frame_pad * 2],
                          radius=20, fill=(20, 14, 10, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(22))
    im.paste(shadow, (fx - frame_pad - 30, fy - frame_pad - 30), shadow)

    d.rounded_rectangle([fx - frame_pad, fy - frame_pad, fx + page.width + frame_pad, fy + page.height + frame_pad],
                         radius=20, fill=P_WHITE)
    im.paste(page, (fx, fy))

    py = fy + page.height + frame_pad + 56
    gap = 24
    widths = []
    f = pil_font(PIL_N_BOLD, 28)
    for text, bg, tc in pills:
        bbox = d.textbbox((0, 0), text, font=f)
        widths.append(bbox[2] - bbox[0] + 28 * 2)
    total_w = sum(widths) + gap * (len(pills) - 1)
    cx = (IMG_W - total_w) / 2
    for (text, bg, tc), w in zip(pills, widths):
        pill(d, cx + w / 2, py, text, bg, tc)
        cx += w + gap

    center_text(d, IMG_W / 2, py + 46, "B R A M B L E   &   B R A I N   C O .", pil_font(PIL_N_BOLD, 24), P_TERRACOTTA)

    im.save(out_path, quality=92)
    print("wrote", out_path)
