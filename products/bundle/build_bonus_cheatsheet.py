# -*- coding: utf-8 -*-
"""Builds the 1-page bonus 'Quick-Start Cheat Sheet' — exclusive to the
Founding Bundle, never sold separately."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from _brand_kit import *

register_fonts()

OUT_PATH = os.path.join(os.path.dirname(__file__), "Quick-Start-Cheat-Sheet-BONUS.pdf")
PRODUCT_NAME = "Quick-Start Cheat Sheet (Bonus)"


def page_cheatsheet(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Quick-Start Cheat Sheet", subtitle="Bonus — Founding Bundle exclusive", band_color=MARIGOLD)

    y = PAGE_H - 70 - 30
    y = draw_paragraph(
        c,
        "Four systems, one page. Don't know where to start? Start here.",
        LEFT, y, CONTENT_W, font=N_REG, size=12, leading=16, color=INK,
    )
    y -= 26

    items = [
        ("1. Pick ONE system for this week", "Not all four at once. Start with whichever page solves today's specific problem.", TERRACOTTA_TINT, TERRACOTTA_DARK),
        ("Losing track of time?", "Start with the Time-Blindness Timeline. Fill it in each morning.", CREAM_DEEP, TERRACOTTA_DARK),
        ("Can't get motivated to start?", "Start with the Dopamine Menu. Pick your reward before the task, not after.", MARIGOLD_TINT, TERRACOTTA_DARK),
        ("Today is just too much?", "Start with Low-Spoons Mode. Three things, max. That's the whole system today.", SAGE_TINT, SAGE_DARK),
        ("Want the full daily/weekly structure?", "Start with The ADHD Life OS — it's the complete system the other three are drawn from.", TERRACOTTA_TINT, TERRACOTTA_DARK),
    ]
    row_h = 76
    for head, body, tint, txt in items:
        box(c, LEFT, y - row_h, CONTENT_W, row_h, stroke=LINE, fill=tint, radius=12)
        c.setFillColor(txt)
        c.setFont(F_SEMI, 13.5)
        c.drawString(LEFT + 18, y - 28, head)
        draw_paragraph(c, body, LEFT + 18, y - 50, CONTENT_W - 36, font=N_REG, size=10.5, leading=14, color=INK_MUTED)
        y -= row_h + 14

    y -= 10
    box(c, LEFT, y - 56, CONTENT_W, 56, stroke=LINE, fill=CREAM_DEEP, radius=10)
    draw_paragraph(
        c, "2. Give it 3 days before judging it. 3. Message us anytime — we reply fast and we mean it.",
        LEFT + 16, y - 24, CONTENT_W - 32, font=N_REG, size=10, leading=14, color=INK_MUTED,
    )
    footer(c, 1, 1, PRODUCT_NAME)


def build():
    c = canvas.Canvas(OUT_PATH, pagesize=letter)
    c.setTitle(PRODUCT_NAME)
    c.setAuthor("Bramble & Brain Co.")
    page_cheatsheet(c)
    c.showPage()
    c.save()
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
