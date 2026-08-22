# -*- coding: utf-8 -*-
"""Builds 'Dopamine Menu + Reward Tracker' PDF for Bramble & Brain Co."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from _brand_kit import *

register_fonts()

OUT_PATH = os.path.join(os.path.dirname(__file__), "Dopamine-Menu-Reward-Tracker.pdf")
TOTAL_PAGES = 2
PRODUCT_NAME = "Dopamine Menu + Reward Tracker"


def page_menu(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_mark(c, PAGE_W - 62, PAGE_H - 35, 20)
    header_band(c, "Dopamine Menu", subtitle="Fuel, not an afterthought.")

    y = PAGE_H - 70 - 30
    y = draw_paragraph(
        c,
        "Motivation isn't a personality trait — it's fuel. Build your own menu of rewards "
        "below, then pick one before you start a hard task, not after you're already burnt out.",
        LEFT, y, CONTENT_W, font=N_REG, size=11, leading=15, color=INK,
    )
    y -= 22

    cols = [
        ("SMALL", "2 minutes", "favorite song · stretch · text a friend · a snack you like", TERRACOTTA_TINT, TERRACOTTA_DARK),
        ("MEDIUM", "15-30 minutes", "an episode · walk outside · a hot drink, slowly", MARIGOLD_TINT, TERRACOTTA_DARK),
        ("BIG", "save for real wins", "that thing you've been eyeing · a lazy afternoon · dinner out", SAGE_TINT, SAGE_DARK),
    ]
    col_gap = 12
    col_w = (CONTENT_W - col_gap * 2) / 3
    col_top = y
    col_h = 400
    for i, (label, sub, examples, tint, txt) in enumerate(cols):
        x = LEFT + i * (col_w + col_gap)
        c.setFillColor(tint)
        c.roundRect(x, col_top - col_h, col_w, col_h, 10, fill=1, stroke=0)
        c.setFillColor(txt)
        c.setFont(F_SEMI, 14)
        c.drawCentredString(x + col_w / 2, col_top - 26, label)
        c.setFont(N_REG, 8.5)
        c.drawCentredString(x + col_w / 2, col_top - 41, sub)
        draw_paragraph(c, examples, x + 12, col_top - 62, col_w - 24, font=N_REG, size=8, leading=10.5, color=INK_MUTED, align="left")
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        for j in range(9):
            ly = col_top - 108 - j * 30
            c.line(x + 12, ly, x + col_w - 12, ly)
    y = col_top - col_h - 26

    box(c, LEFT, y - 56, CONTENT_W, 56, stroke=LINE, fill=CREAM_DEEP, radius=10)
    draw_paragraph(
        c, "How to use this: write in rewards that are actually yours — not what a productivity "
           "influencer says should motivate you. If it works, it belongs on this page.",
        LEFT + 16, y - 24, CONTENT_W - 32, font=N_REG, size=9.5, leading=13, color=INK_MUTED,
    )
    footer(c, 1, TOTAL_PAGES, PRODUCT_NAME)


def page_tracker(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Reward Tracker", subtitle="4 weeks — mark a box each day you followed through")

    y = PAGE_H - 70 - 34
    y = draw_paragraph(
        c,
        "No streak-shaming here. A gap in the tracker is just a gap — it doesn't erase the days "
        "you did follow through. This is for noticing your own patterns, not grading yourself.",
        LEFT, y, CONTENT_W, font=N_REG, size=11, leading=15, color=INK,
    )
    y -= 26

    weeks = ["WEEK 1", "WEEK 2", "WEEK 3", "WEEK 4"]
    week_h = 128
    for wi, wk in enumerate(weeks):
        wy = y - wi * (week_h + 14)
        box(c, LEFT, wy - week_h, CONTENT_W, week_h, stroke=LINE, fill=WHITE, radius=10)
        c.setFillColor(TERRACOTTA_DARK)
        c.setFont(F_SEMI, 11.5)
        c.drawString(LEFT + 16, wy - 24, wk)
        c.setFillColor(INK_MUTED)
        c.setFont(N_REG, 8.5)
        c.drawString(LEFT + 16, wy - 40, "This week's reward, chosen in advance:")
        c.setStrokeColor(LINE)
        c.line(LEFT + 210, wy - 43, RIGHT - 16, wy - 43)

        days = ["M", "T", "W", "T", "F", "S", "S"]
        n = 7
        box_w = CONTENT_W / n
        for i, d in enumerate(days):
            cx = LEFT + i * box_w + box_w / 2
            checkbox(c, cx - 8, wy - week_h + 30, size=16, color=MARIGOLD)
            c.setFillColor(INK_MUTED)
            c.setFont(N_REG, 8)
            c.drawCentredString(cx, wy - week_h + 16, d)
    footer(c, 2, TOTAL_PAGES, PRODUCT_NAME)


def build():
    c = canvas.Canvas(OUT_PATH, pagesize=letter)
    c.setTitle(PRODUCT_NAME)
    c.setAuthor("Bramble & Brain Co.")
    c.setSubject("ADHD-friendly dopamine menu and reward tracker, printable PDF")
    for page_fn in [page_menu, page_tracker]:
        page_fn(c)
        c.showPage()
    c.save()
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
