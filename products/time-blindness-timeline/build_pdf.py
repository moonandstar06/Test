# -*- coding: utf-8 -*-
"""Builds 'Time-Blindness Daily Timeline Sheet' PDF for Bramble & Brain Co."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from _brand_kit import *

register_fonts()

OUT_PATH = os.path.join(os.path.dirname(__file__), "Time-Blindness-Daily-Timeline-Sheet.pdf")
TOTAL_PAGES = 2
PRODUCT_NAME = "Time-Blindness Daily Timeline"


def page_daily_timeline(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Today, Visually", subtitle="Date: ______________________")

    y = PAGE_H - 70 - 28
    y = draw_paragraph(
        c,
        "“What time is it, actually” stops being the hard part. Color-coded blocks instead "
        "of a wall of numbers — write what's happening in each window, roughly.",
        LEFT, y, CONTENT_W, font=N_REG, size=10.5, leading=14, color=INK,
    )
    y -= 20

    blocks = [
        ("EARLY MORNING", "6 - 9 AM", TERRACOTTA_TINT, TERRACOTTA_DARK),
        ("MORNING", "9 - 12 PM", MARIGOLD_TINT, TERRACOTTA_DARK),
        ("MIDDAY", "12 - 2 PM", CREAM_DEEP, INK_MUTED),
        ("AFTERNOON", "2 - 5 PM", SAGE_TINT, SAGE_DARK),
        ("EVENING", "5 - 8 PM", TERRACOTTA_TINT, TERRACOTTA_DARK),
        ("NIGHT", "8 - 10 PM", MARIGOLD_TINT, TERRACOTTA_DARK),
    ]
    bh = 62
    gap = 8
    for label, sub, tint, txt_color in blocks:
        c.setFillColor(tint)
        c.roundRect(LEFT, y - bh, CONTENT_W, bh, 9, fill=1, stroke=0)
        c.setFillColor(txt_color)
        c.setFont(F_SEMI, 11)
        c.drawString(LEFT + 16, y - 22, label)
        c.setFont(N_REG, 8)
        c.drawString(LEFT + 16, y - 36, sub)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        lx = LEFT + 150
        for k in range(2):
            ly = y - 22 - k * 20
            c.line(lx, ly, RIGHT - 14, ly)
        y -= bh + gap

    y -= 14
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont(F_SEMI, 12.5)
    c.drawString(LEFT, y, "Brain Dump")
    c.setFillColor(INK_MUTED)
    c.setFont(N_REG, 9)
    c.drawRightString(RIGHT, y + 1, "Whatever's floating around, out of your head and onto the page")
    y -= 12
    dump_h = 70
    box(c, LEFT, y - dump_h, CONTENT_W, dump_h, stroke=LINE)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    for j in range(1, 4):
        ly = y - j * (dump_h / 4)
        c.line(LEFT + 10, ly, RIGHT - 10, ly)
    footer(c, 1, TOTAL_PAGES, PRODUCT_NAME)


def page_week_glance(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Week at a Glance", subtitle="Week of ______________________")

    y = PAGE_H - 70 - 28
    y = draw_paragraph(
        c,
        "A mini timeline for each day of the week — plan ahead without needing to hold seven "
        "schedules in your head at once.",
        LEFT, y, CONTENT_W, font=N_REG, size=10.5, leading=14, color=INK,
    )
    y -= 20

    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    row_h = 62
    for d in days:
        box(c, LEFT, y - row_h, CONTENT_W, row_h, stroke=LINE, fill=WHITE, radius=8)
        c.setFillColor(TERRACOTTA_DARK)
        c.setFont(F_SEMI, 11)
        c.drawString(LEFT + 14, y - row_h / 2 - 4, d)

        seg_x = LEFT + 74
        seg_w = RIGHT - 14 - seg_x
        n_seg = 4
        seg_labels = ["AM", "MID", "PM", "EVE"]
        tints = [TERRACOTTA_TINT, MARIGOLD_TINT, SAGE_TINT, CREAM_DEEP]
        each_w = seg_w / n_seg
        for i in range(n_seg):
            sx = seg_x + i * each_w
            c.setFillColor(tints[i])
            c.roundRect(sx, y - row_h + 10, each_w - 6, row_h - 20, 6, fill=1, stroke=0)
            c.setFillColor(INK_MUTED)
            c.setFont(N_REG, 7)
            c.drawString(sx + 6, y - row_h + row_h - 22, seg_labels[i])
            c.setStrokeColor(WHITE)
            c.setLineWidth(0.8)
            c.line(sx + 6, y - row_h + 20, sx + each_w - 12, y - row_h + 20)
        y -= row_h + 8

    y -= 26
    box(c, LEFT, y - 44, CONTENT_W, 44, stroke=LINE, fill=MARIGOLD_TINT, radius=10)
    draw_paragraph(
        c, "Tip: fill this in on Sunday night, in pencil — plans change, and that's fine. "
           "The point is having a shape for the week, not a locked-in contract.",
        LEFT + 16, y - 22, CONTENT_W - 32, font=N_REG, size=9.5, leading=13, color=INK_MUTED,
    )
    footer(c, 2, TOTAL_PAGES, PRODUCT_NAME)


def build():
    c = canvas.Canvas(OUT_PATH, pagesize=letter)
    c.setTitle(PRODUCT_NAME)
    c.setAuthor("Bramble & Brain Co.")
    c.setSubject("ADHD-friendly time-blindness visual timeline, printable PDF")
    for page_fn in [page_daily_timeline, page_week_glance]:
        page_fn(c)
        c.showPage()
    c.save()
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
