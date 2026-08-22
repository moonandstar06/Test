# -*- coding: utf-8 -*-
"""Builds 'Low-Spoons Mode — Simplified Daily Checklist' PDF for Bramble & Brain Co."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from _brand_kit import *

register_fonts()

OUT_PATH = os.path.join(os.path.dirname(__file__), "Low-Spoons-Mode-Checklist.pdf")
TOTAL_PAGES = 2
PRODUCT_NAME = "Low-Spoons Mode Checklist"


def page_low_spoons(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Low-Spoons Mode", subtitle="For the days that are just… a lot.", band_color=SAGE_DARK)

    y = PAGE_H - 70 - 38
    c.setFillColor(SAGE_DARK)
    c.setFont(F_SEMI, 15)
    c.drawCentredString(PAGE_W / 2, y, "You don't need the whole system today. Just this page.")
    y -= 40

    c.setFillColor(TERRACOTTA_DARK)
    c.setFont(F_SEMI, 13)
    c.drawString(LEFT, y, "The ONLY things that matter today")
    c.setFillColor(INK_MUTED)
    c.setFont(N_REG, 9)
    c.drawRightString(RIGHT, y + 1, "Three, at most")
    y -= 22
    row_h = 62
    for i in range(1, 4):
        box(c, LEFT, y - row_h, CONTENT_W, row_h, stroke=SAGE, fill=SAGE_TINT, radius=12)
        numbered_dot(c, LEFT + 26, y - row_h / 2, 14, i, bg=SAGE_DARK)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        c.line(LEFT + 52, y - row_h / 2, RIGHT - 20, y - row_h / 2)
        y -= row_h + 12

    y -= 8
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont(F_SEMI, 14)
    c.drawString(LEFT, y, "Bare-Minimum Self-Care")
    y -= 28
    items = ["Water", "One real meal", "Meds, if that's part of your day", "Rest or lie down for a bit", "One message to someone, if you need it"]
    for item in items:
        checkbox(c, LEFT, y - 10, size=15, color=SAGE_DARK)
        c.setFillColor(INK)
        c.setFont(N_REG, 11.5)
        c.drawString(LEFT + 24, y - 9, item)
        y -= 28

    y -= 18
    box(c, LEFT, y - 66, CONTENT_W, 66, stroke=SAGE, fill=CREAM_DEEP, radius=12)
    c.setFillColor(SAGE_DARK)
    c.setFont(F_SEMI, 13.5)
    c.drawCentredString(PAGE_W / 2, y - 28, "Rest is not falling behind.")
    c.setFont(N_REG, 10.5)
    c.setFillColor(INK_MUTED)
    c.drawCentredString(PAGE_W / 2, y - 48, "Tomorrow's system will still be here when you're ready for it.")
    footer(c, 1, TOTAL_PAGES, PRODUCT_NAME)


def page_spoon_budget(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Spoon Budget", subtitle="Spend them on purpose.", band_color=SAGE_DARK)

    y = PAGE_H - 70 - 30
    y = draw_paragraph(
        c,
        "Spoon theory, in one line: you start the day with a limited number of “spoons” "
        "(units of energy), and everything you do — even small things — costs one. Budget them "
        "instead of spending blind.",
        LEFT, y, CONTENT_W, font=N_REG, size=10.5, leading=14, color=INK,
    )
    y -= 22

    c.setFillColor(TERRACOTTA_DARK)
    c.setFont(F_SEMI, 12.5)
    c.drawString(LEFT, y, "Today I'm starting with:")
    n_spoons = 12
    sx = LEFT + 190
    for i in range(n_spoons):
        cx = sx + i * 24
        c.setStrokeColor(MARIGOLD)
        c.setLineWidth(1.3)
        c.ellipse(cx, y - 10, cx + 16, y + 6, fill=0, stroke=1)
    y -= 20
    c.setFillColor(INK_MUTED)
    c.setFont(N_REG, 8.5)
    c.drawString(LEFT, y, "Circle how many feel true this morning — no wrong number.")
    y -= 34

    c.setFillColor(TERRACOTTA_DARK)
    c.setFont(F_SEMI, 12.5)
    c.drawString(LEFT, y, "Where they're going")
    c.setFillColor(INK_MUTED)
    c.setFont(N_REG, 9)
    c.drawRightString(RIGHT, y + 1, "List the task, mark the cost")
    y -= 20

    rows = 8
    row_h = 34
    col_task_w = CONTENT_W - 180
    for r in range(rows):
        ry = y - r * row_h
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(LEFT, ry - row_h + 8, RIGHT, ry - row_h + 8)
        c.setFont(N_REG, 8.5)
        c.setFillColor(INK_MUTED)
        for i in range(3):
            cx = LEFT + col_task_w + 14 + i * 44
            c.setStrokeColor(SAGE)
            c.setLineWidth(1.2)
            c.ellipse(cx, ry - row_h + 14, cx + 15, ry - row_h + 29, fill=0, stroke=1)

    y2 = y - rows * row_h - 20
    box(c, LEFT, y2 - 50, CONTENT_W, 50, stroke=SAGE, fill=SAGE_TINT, radius=10)
    draw_paragraph(
        c, "Ran out early? That's data, not a failure — it tells you what to protect tomorrow. "
           "Left some over? Bank them for something you actually want to do.",
        LEFT + 16, y2 - 22, CONTENT_W - 32, font=N_REG, size=9.5, leading=13, color=SAGE_DARK,
    )
    footer(c, 2, TOTAL_PAGES, PRODUCT_NAME)


def build():
    c = canvas.Canvas(OUT_PATH, pagesize=letter)
    c.setTitle(PRODUCT_NAME)
    c.setAuthor("Bramble & Brain Co.")
    c.setSubject("ADHD-friendly low-spoons day checklist and spoon budget, printable PDF")
    for page_fn in [page_low_spoons, page_spoon_budget]:
        page_fn(c)
        c.showPage()
    c.save()
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
