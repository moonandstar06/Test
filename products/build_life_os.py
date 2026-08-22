\
# -*- coding: utf-8 -*-
"""Builds 'The ADHD Life OS — Printable Edition' PDF for Bramble & Brain Co."""
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_DIR = "/tmp/claude-0/fonts/"
pdfmetrics.registerFont(TTFont("Fredoka-Medium", FONT_DIR + "Fredoka-Medium.ttf"))
pdfmetrics.registerFont(TTFont("Fredoka-SemiBold", FONT_DIR + "Fredoka-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Fredoka-Bold", FONT_DIR + "Fredoka-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Nunito-Regular", FONT_DIR + "Nunito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Nunito-SemiBold", FONT_DIR + "Nunito-SemiBold.ttf"))
pdfmetrics.registerFont(TTFont("Nunito-Bold", FONT_DIR + "Nunito-Bold.ttf"))

CREAM = HexColor("#FAF3E9")
CREAM_DEEP = HexColor("#F1E4D0")
TERRACOTTA = HexColor("#C06544")
TERRACOTTA_DARK = HexColor("#8F4930")
TERRACOTTA_TINT = HexColor("#F0DCCF")
SAGE = HexColor("#8C9B7C")
SAGE_DARK = HexColor("#5F6B54")
SAGE_TINT = HexColor("#E4E8DC")
MARIGOLD = HexColor("#E8A94A")
MARIGOLD_TINT = HexColor("#FBECD2")
INK = HexColor("#4A3B32")
INK_MUTED = HexColor("#6E5A4E")
LINE = HexColor("#D9C9B4")
WHITE = HexColor("#FFFFFF")

PAGE_W, PAGE_H = letter
MARGIN = 42
CONTENT_W = PAGE_W - 2 * MARGIN
LEFT = MARGIN
RIGHT = PAGE_W - MARGIN

OUT_PATH = "/tmp/claude-0/-home-user-dgroup-booking/6e18ded9-e301-5997-b108-de22bc28193a/scratchpad/etsy-co/products/ADHD-Life-OS-Printable-Edition.pdf"

TOTAL_PAGES = 8


def wrap_text(text, font, size, max_width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if pdfmetrics.stringWidth(test, font, size) <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_paragraph(c, text, x, y, max_width, font="Nunito-Regular", size=10.5, leading=14, color=INK, align="left"):
    c.setFillColor(color)
    c.setFont(font, size)
    lines = wrap_text(text, font, size, max_width)
    for line in lines:
        if align == "center":
            c.drawCentredString(x + max_width / 2, y, line)
        else:
            c.drawString(x, y, line)
        y -= leading
    return y


DOT_OFFSETS = [
    (-0.45, -0.50, 0.11),
    (0.50, -0.55, 0.09),
    (0.70, 0.10, 0.13),
    (0.40, 0.65, 0.10),
    (-0.52, 0.50, 0.08),
    (-0.65, -0.05, 0.12),
]


def draw_mark(c, cx, cy, r, ring_bg=TERRACOTTA, dot_color=CREAM, focus_color=MARIGOLD, draw_ring=True):
    c.saveState()
    if draw_ring:
        c.setFillColor(ring_bg)
        c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(dot_color)
    for dx, dy, rr in DOT_OFFSETS:
        c.circle(cx + dx * r, cy + dy * r, rr * r, fill=1, stroke=0)
    c.setFillColor(focus_color)
    c.circle(cx, cy, 0.42 * r, fill=1, stroke=0)
    c.restoreState()


def header_band(c, title, subtitle=None, band_color=TERRACOTTA, band_h=70):
    c.saveState()
    c.setFillColor(band_color)
    c.rect(0, PAGE_H - band_h, PAGE_W, band_h, fill=1, stroke=0)
    c.setFillColor(CREAM)
    c.setFont("Nunito-Bold", 8.5)
    c.drawString(LEFT, PAGE_H - 18, "B R A M B L E   &   B R A I N   C O .")
    c.setFont("Fredoka-Bold", 25)
    c.drawString(LEFT, PAGE_H - band_h + 16, title)
    if subtitle:
        c.setFont("Nunito-SemiBold", 10.5)
        tw = pdfmetrics.stringWidth(title, "Fredoka-Bold", 25)
        c.drawString(LEFT + tw + 14, PAGE_H - band_h + 20, subtitle)
    c.restoreState()


def footer(c, page_num):
    c.saveState()
    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-Regular", 8)
    c.drawCentredString(PAGE_W / 2, 24, "Bramble & Brain Co.   ·   The ADHD Life OS   ·   page %d of %d" % (page_num, TOTAL_PAGES))
    c.restoreState()


def box(c, x, y, w, h, stroke=LINE, fill=None, radius=8, lw=1.1):
    c.saveState()
    c.setLineWidth(lw)
    c.setStrokeColor(stroke)
    if fill is not None:
        c.setFillColor(fill)
        c.roundRect(x, y, w, h, radius, fill=1, stroke=1)
    else:
        c.roundRect(x, y, w, h, radius, fill=0, stroke=1)
    c.restoreState()


def checkbox(c, x, y, size=11, color=TERRACOTTA):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(1.3)
    c.roundRect(x, y, size, size, 2.5, fill=0, stroke=1)
    c.restoreState()


def numbered_dot(c, cx, cy, r, num, bg=TERRACOTTA, text_color=CREAM):
    c.saveState()
    c.setFillColor(bg)
    c.circle(cx, cy, r, fill=1, stroke=0)
    c.setFillColor(text_color)
    c.setFont("Nunito-Bold", r * 1.05)
    c.drawCentredString(cx, cy - r * 0.35, str(num))
    c.restoreState()


def priority_row(c, x, y, w, h, num, label=""):
    box(c, x, y, w, h, stroke=LINE)
    numbered_dot(c, x + 18, y + h / 2, 10, num)
    if label:
        c.setFillColor(INK_MUTED)
        c.setFont("Nunito-Regular", 9)
        c.drawString(x + 36, y + h / 2 - 3, label)


# ---------------------------------------------------------------- PAGE 1
def page_cover(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    draw_mark(c, PAGE_W / 2, 598, 96)

    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-Bold", 40)
    c.drawCentredString(PAGE_W / 2, 452, "The ADHD Life OS")

    c.setFillColor(SAGE_DARK)
    c.setFont("Fredoka-SemiBold", 18)
    c.drawCentredString(PAGE_W / 2, 418, "Printable Edition")

    c.setStrokeColor(LINE)
    c.setLineWidth(1.2)
    c.line(PAGE_W / 2 - 34, 394, PAGE_W / 2 + 34, 394)

    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-SemiBold", 12.5)
    c.drawCentredString(PAGE_W / 2, 368, "Digital planning systems for brains that work differently")

    c.setFont("Nunito-Regular", 10.5)
    c.drawCentredString(PAGE_W / 2, 344, "An 8-page printable system — US Letter, print at home")

    c.setStrokeColor(LINE)
    c.line(PAGE_W / 2 - 90, 76, PAGE_W / 2 + 90, 76)
    c.setFillColor(TERRACOTTA)
    c.setFont("Nunito-Bold", 10)
    c.drawCentredString(PAGE_W / 2, 56, "B R A M B L E   &   B R A I N   C O .")


# ---------------------------------------------------------------- PAGE 2
def page_how_to(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "How This Works")

    y = PAGE_H - 70 - 34
    y = draw_paragraph(
        c,
        "This isn’t a planner you have to earn your way into using correctly. "
        "There’s no wrong way to start — here’s the short version.",
        LEFT, y, CONTENT_W, font="Nunito-Regular", size=11.5, leading=16, color=INK,
    )
    y -= 16

    tips = [
        ("Start with the Weekly page", "Pick 3 priorities, max. More than that isn’t a plan — it’s a wish list."),
        ("Fill out a Daily page each day", "Whenever your day actually starts. There’s no rule that it has to be morning."),
        ("Having a hard day? Flip to Low-Spoons Mode", "That’s not giving up — that’s the system doing exactly what it’s for."),
        ("Actually use the Dopamine Menu", "It’s not decoration. Reward the effort, not just the finished result."),
        ("Missed a day on the Habit Tracker?", "Leave the square blank and move on. There are no shame boxes in this system."),
    ]
    for i, (head, body) in enumerate(tips, start=1):
        numbered_dot(c, LEFT + 12, y - 7, 12, i)
        c.setFillColor(INK)
        c.setFont("Nunito-Bold", 13)
        c.drawString(LEFT + 34, y, head)
        y -= 18
        y = draw_paragraph(c, body, LEFT + 34, y, CONTENT_W - 34, font="Nunito-Regular", size=11, leading=15, color=INK_MUTED)
        y -= 24

    y -= 6
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 13.5)
    c.drawString(LEFT, y, "Quick Legend")
    y -= 24
    legend = [
        ("circle", "A pick-one scale, like energy check-ins — circle the number that fits."),
        ("checkbox", "A small, doable action — check it off when it's done, however small."),
        ("line", "Open space — write whatever's actually true, not what sounds impressive."),
    ]
    lx = LEFT
    for kind, desc in legend:
        if kind == "circle":
            c.setStrokeColor(TERRACOTTA)
            c.setLineWidth(1.3)
            c.circle(lx + 7, y + 4, 8, fill=0, stroke=1)
        elif kind == "checkbox":
            checkbox(c, lx, y - 4, size=14, color=TERRACOTTA)
        else:
            c.setStrokeColor(LINE)
            c.setLineWidth(1)
            c.line(lx, y, lx + 15, y)
        y2 = draw_paragraph(c, desc, lx + 28, y + 4, CONTENT_W - 28, font="Nunito-Regular", size=10, leading=13, color=INK_MUTED)
        y = y2 - 6

    box(c, LEFT, 90, CONTENT_W, 50, stroke=LINE, fill=CREAM_DEEP, radius=10)
    draw_paragraph(
        c, "Print single-sided or double-sided — US Letter (8.5″ × 11″), fits any standard home printer.",
        LEFT + 18, 118, CONTENT_W - 36, font="Nunito-Regular", size=10, leading=13, color=INK_MUTED,
    )
    footer(c, 2)


# ---------------------------------------------------------------- PAGE 3
def page_weekly(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Weekly Overview", subtitle="Week of ______________________")

    y = PAGE_H - 70 - 30
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 13.5)
    c.drawString(LEFT, y, "Top 3 Priorities This Week")
    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-Regular", 9)
    c.drawRightString(RIGHT, y + 2, "Only 3. That’s the whole point.")

    y -= 18
    row_h = 34
    for i in range(1, 4):
        priority_row(c, LEFT, y - row_h, CONTENT_W, row_h, i)
        y -= row_h + 8

    y -= 10
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 13.5)
    c.drawString(LEFT, y, "This Week, Day by Day")
    y -= 18

    days = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
    col_gap = 6
    col_w = (CONTENT_W - col_gap * 6) / 7
    grid_top = y
    grid_h = 340
    for i, d in enumerate(days):
        x = LEFT + i * (col_w + col_gap)
        c.setFillColor(SAGE_TINT)
        c.roundRect(x, grid_top - 22, col_w, 22, 5, fill=1, stroke=0)
        c.setFillColor(SAGE_DARK)
        c.setFont("Fredoka-SemiBold", 9.5)
        c.drawCentredString(x + col_w / 2, grid_top - 15, d)
        box(c, x, grid_top - grid_h, col_w, grid_h - 22, stroke=LINE)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        for j in range(1, 7):
            ly = grid_top - 30 - j * ((grid_h - 34) / 7)
            c.line(x + 6, ly, x + col_w - 6, ly)

    band_y = grid_top - grid_h - 30
    box(c, LEFT, band_y - 44, CONTENT_W, 44, stroke=LINE, fill=MARIGOLD_TINT, radius=10)
    c.setFillColor(INK)
    c.setFont("Nunito-SemiBold", 9.5)
    c.drawString(LEFT + 16, band_y - 18, "This week’s fuel: check the Dopamine Menu (page 5) before you need it.")
    c.setFont("Nunito-SemiBold", 9.5)
    c.drawString(LEFT + 16, band_y - 34, "Energy for the week ahead:")
    startx = LEFT + 210
    for i in range(1, 6):
        checkbox(c, startx + (i - 1) * 22, band_y - 40, size=13, color=TERRACOTTA)
        c.setFont("Nunito-Regular", 8)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(startx + (i - 1) * 22 + 6.5, band_y - 51, str(i))
    footer(c, 3)


# ---------------------------------------------------------------- PAGE 4
def page_daily(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Today", subtitle="Date: ______________________")

    y = PAGE_H - 70 - 30
    c.setFillColor(INK)
    c.setFont("Nunito-SemiBold", 10.5)
    c.drawString(LEFT, y, "Energy check-in:")
    for i in range(1, 6):
        cx = LEFT + 100 + (i - 1) * 24
        checkbox(c, cx, y - 8, size=14, color=SAGE_DARK)
        c.setFont("Nunito-Regular", 8)
        c.setFillColor(INK_MUTED)
        c.drawCentredString(cx + 7, y - 20, str(i))
    c.setFont("Nunito-Regular", 8.5)
    c.drawString(LEFT + 235, y - 3, "(1 = running on empty — 5 = genuinely good)")

    y -= 44
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 13.5)
    c.drawString(LEFT, y, "Today, Visually")
    y -= 16

    blocks = [
        ("MORNING", TERRACOTTA_TINT, TERRACOTTA_DARK),
        ("MIDDAY", MARIGOLD_TINT, TERRACOTTA_DARK),
        ("AFTERNOON", SAGE_TINT, SAGE_DARK),
        ("EVENING", CREAM_DEEP, INK_MUTED),
    ]
    bh = 46
    gap = 6
    for label, tint, txt_color in blocks:
        c.setFillColor(tint)
        c.roundRect(LEFT, y - bh, CONTENT_W, bh, 8, fill=1, stroke=0)
        c.setFillColor(txt_color)
        c.setFont("Fredoka-SemiBold", 10.5)
        c.drawString(LEFT + 14, y - bh / 2 - 4, label)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        lx = LEFT + 120
        for k in range(2):
            ly = y - 15 - k * 16
            c.line(lx, ly, RIGHT - 14, ly)
        y -= bh + gap

    y -= 14
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 13.5)
    c.drawString(LEFT, y, "Top 3 Priorities Today")
    y -= 16
    row_h = 26
    for i in range(1, 4):
        priority_row(c, LEFT, y - row_h, CONTENT_W, row_h, i)
        y -= row_h + 6

    y -= 12
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 12.5)
    c.drawString(LEFT, y, "Brain Dump")
    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-Regular", 9)
    c.drawRightString(RIGHT, y + 1, "Get it out of your head and onto the page")
    y -= 12
    dump_h = 90
    box(c, LEFT, y - dump_h, CONTENT_W, dump_h, stroke=LINE)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.6)
    for j in range(1, 5):
        ly = y - j * (dump_h / 5)
        c.line(LEFT + 10, ly, RIGHT - 10, ly)
    y -= dump_h + 20

    c.setFillColor(INK)
    c.setFont("Nunito-SemiBold", 10)
    c.drawString(LEFT, y, "One kind thing I’ll do for myself today:")
    c.setStrokeColor(LINE)
    c.line(LEFT + 232, y - 3, RIGHT, y - 3)
    footer(c, 4)


# ---------------------------------------------------------------- PAGE 5
def page_dopamine(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Dopamine Menu", subtitle="Fuel, not an afterthought.")

    y = PAGE_H - 70 - 32
    y = draw_paragraph(
        c,
        "Motivation isn’t a personality trait — it’s fuel. Pick a reward before you start, "
        "not after you’re already burnt out.",
        LEFT, y, CONTENT_W, font="Nunito-Regular", size=11, leading=15, color=INK,
    )
    y -= 20

    cols = [
        ("SMALL", "2 minutes", "favorite song · stretch · text a friend", TERRACOTTA_TINT, TERRACOTTA_DARK),
        ("MEDIUM", "15–30 minutes", "an episode · walk outside · a snack you actually like", MARIGOLD_TINT, TERRACOTTA_DARK),
        ("BIG", "save for real wins", "that thing you’ve been eyeing · a lazy afternoon · dinner out", SAGE_TINT, SAGE_DARK),
    ]
    col_gap = 12
    col_w = (CONTENT_W - col_gap * 2) / 3
    col_top = y
    col_h = 340
    for i, (label, sub, examples, tint, txt) in enumerate(cols):
        x = LEFT + i * (col_w + col_gap)
        c.setFillColor(tint)
        c.roundRect(x, col_top - col_h, col_w, col_h, 10, fill=1, stroke=0)
        c.setFillColor(txt)
        c.setFont("Fredoka-SemiBold", 13)
        c.drawCentredString(x + col_w / 2, col_top - 24, label)
        c.setFont("Nunito-Regular", 8.5)
        c.drawCentredString(x + col_w / 2, col_top - 38, sub)
        draw_paragraph(c, examples, x + 12, col_top - 58, col_w - 24, font="Nunito-Regular", size=8, leading=10.5, color=INK_MUTED, align="left")
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        for j in range(8):
            ly = col_top - 100 - j * 26
            c.line(x + 12, ly, x + col_w - 12, ly)

    y2 = col_top - col_h - 30
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 12.5)
    c.drawString(LEFT, y2, "Reward Tracker — 4 Weeks")
    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-Regular", 9)
    c.drawRightString(RIGHT, y2 + 1, "Mark a box each day you followed through — no matter how small")
    y2 -= 26
    n = 14
    box_w = CONTENT_W / n
    for row in range(2):
        for i in range(n):
            x = LEFT + i * box_w
            d = row * n + i + 1
            checkbox(c, x + box_w / 2 - 7, y2 - 14, size=14, color=MARIGOLD)
            c.setFont("Nunito-Regular", 7.5)
            c.setFillColor(INK_MUTED)
            c.drawCentredString(x + box_w / 2, y2 - 28, "D%d" % d)
        y2 -= 44
    footer(c, 5)


# ---------------------------------------------------------------- PAGE 6
def page_habits(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Habit Tracker")

    y = PAGE_H - 70 - 26
    y = draw_paragraph(
        c,
        "Pick 3–5 habits, max. This isn’t about a perfect streak — it’s about noticing your own patterns.",
        LEFT, y, CONTENT_W, font="Nunito-Regular", size=10.5, leading=14, color=INK,
    )
    y -= 20

    name_w = 116
    days = 31
    grid_w = CONTENT_W - name_w
    cell_w = grid_w / days
    row_h = 80
    header_y = y

    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-Regular", 6.3)
    for d in range(1, days + 1):
        if d == 1 or d % 5 == 0:
            cx = LEFT + name_w + (d - 1) * cell_w + cell_w / 2
            c.drawCentredString(cx, header_y, str(d))

    top = header_y - 10
    n_rows = 5
    for r in range(n_rows):
        ry = top - r * row_h
        c.setStrokeColor(LINE)
        c.setLineWidth(0.7)
        c.line(LEFT, ry - row_h, RIGHT, ry - row_h)
        c.line(LEFT, ry, LEFT, ry - row_h)
        c.line(LEFT + name_w, ry, LEFT + name_w, ry - row_h)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.6)
        c.line(LEFT + 10, ry - row_h + 16, LEFT + name_w - 10, ry - row_h + 16)
        for d in range(days):
            cx = LEFT + name_w + d * cell_w + cell_w / 2
            cy = ry - row_h / 2
            c.setStrokeColor(LINE)
            c.setLineWidth(0.9)
            c.circle(cx, cy, min(cell_w, row_h) * 0.30, fill=0, stroke=1)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.7)
    c.line(RIGHT, top, RIGHT, top - n_rows * row_h)
    c.line(LEFT, top, RIGHT, top)

    note_y = top - n_rows * row_h - 40
    box(c, LEFT, note_y, CONTENT_W, 30, stroke=LINE, fill=CREAM_DEEP, radius=8)
    draw_paragraph(c, "A blank circle isn’t a failure — it’s just a blank circle. Fill in what you did, skip what you didn’t.",
                    LEFT + 14, note_y + 10, CONTENT_W - 28, font="Nunito-Regular", size=9, leading=11, color=INK_MUTED)
    footer(c, 6)


# ---------------------------------------------------------------- PAGE 7
def page_low_spoons(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Low-Spoons Mode", subtitle="For the days that are just… a lot.", band_color=SAGE_DARK)

    y = PAGE_H - 70 - 40
    c.setFillColor(SAGE_DARK)
    c.setFont("Fredoka-SemiBold", 15)
    c.drawCentredString(PAGE_W / 2, y, "You don’t need the whole system today. Just this page.")
    y -= 42

    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 13)
    c.drawString(LEFT, y, "The ONLY things that matter today")
    c.setFillColor(INK_MUTED)
    c.setFont("Nunito-Regular", 9)
    c.drawRightString(RIGHT, y + 1, "Three, at most")
    y -= 22
    row_h = 68
    for i in range(1, 4):
        box(c, LEFT, y - row_h, CONTENT_W, row_h, stroke=SAGE, fill=SAGE_TINT, radius=12)
        numbered_dot(c, LEFT + 26, y - row_h / 2, 14, i, bg=SAGE_DARK)
        c.setStrokeColor(WHITE)
        c.setLineWidth(1)
        c.line(LEFT + 52, y - row_h / 2, RIGHT - 20, y - row_h / 2)
        y -= row_h + 14

    y -= 10
    c.setFillColor(TERRACOTTA_DARK)
    c.setFont("Fredoka-SemiBold", 14)
    c.drawString(LEFT, y, "Bare-Minimum Self-Care")
    y -= 30
    items = ["Water", "One real meal", "Meds, if that’s part of your day", "Rest or lie down for a bit", "One message to someone, if you need it"]
    for item in items:
        checkbox(c, LEFT, y - 11, size=16, color=SAGE_DARK)
        c.setFillColor(INK)
        c.setFont("Nunito-Regular", 12)
        c.drawString(LEFT + 26, y - 10, item)
        y -= 32

    y -= 22
    box(c, LEFT, y - 78, CONTENT_W, 78, stroke=SAGE, fill=CREAM_DEEP, radius=12)
    c.setFillColor(SAGE_DARK)
    c.setFont("Fredoka-SemiBold", 15)
    c.drawCentredString(PAGE_W / 2, y - 32, "Rest is not falling behind.")
    c.setFont("Nunito-Regular", 11.5)
    c.setFillColor(INK_MUTED)
    c.drawCentredString(PAGE_W / 2, y - 55, "Tomorrow’s system will still be here when you’re ready for it.")
    footer(c, 7)


# ---------------------------------------------------------------- PAGE 8
def page_med_tracker(c):
    c.setFillColor(CREAM)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    header_band(c, "Medication & Symptom Tracker")

    y = PAGE_H - 70 - 30
    y = draw_paragraph(
        c,
        "This is for your own pattern-spotting — not for anyone to grade you on.",
        LEFT, y, CONTENT_W, font="Nunito-Regular", size=10.5, leading=14, color=INK,
    )
    y -= 24

    cols = [("DAY", 62), ("AM", 44), ("PM", 44), ("SLEEP (HRS)", 66), ("ENERGY 1–5", 66), ("MOOD 1–5", 66), ("NOTES", 0)]
    fixed_w = sum(w for _, w in cols if w)
    notes_w = CONTENT_W - fixed_w
    header_h = 26
    c.setFillColor(TERRACOTTA)
    c.roundRect(LEFT, y - header_h, CONTENT_W, header_h, 6, fill=1, stroke=0)
    x = LEFT
    c.setFillColor(CREAM)
    c.setFont("Nunito-Bold", 8)
    for label, w in cols:
        cw = w if w else notes_w
        c.drawCentredString(x + cw / 2, y - header_h / 2 - 3, label)
        x += cw
    y -= header_h

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    row_h = 66
    for d in days:
        x = LEFT
        c.setStrokeColor(LINE)
        c.setLineWidth(0.8)
        c.rect(LEFT, y - row_h, CONTENT_W, row_h, fill=0, stroke=1)
        col_x = LEFT
        for label, w in cols:
            cw = w if w else notes_w
            if col_x != LEFT:
                c.line(col_x, y, col_x, y - row_h)
            col_x += cw
        c.setFillColor(INK)
        c.setFont("Nunito-SemiBold", 9)
        c.drawString(LEFT + 8, y - row_h / 2 - 3, d)
        cx = LEFT + cols[0][1]
        checkbox(c, cx + cols[1][1] / 2 - 6, y - row_h / 2 - 6, size=13)
        cx += cols[1][1]
        checkbox(c, cx + cols[2][1] / 2 - 6, y - row_h / 2 - 6, size=13)
        y -= row_h

    footer(c, 8)


def build():
    c = canvas.Canvas(OUT_PATH, pagesize=letter)
    c.setTitle("The ADHD Life OS — Printable Edition")
    c.setAuthor("Bramble & Brain Co.")
    c.setSubject("ADHD-friendly digital planning system, printable PDF edition")

    for page_fn in [page_cover, page_how_to, page_weekly, page_daily, page_dopamine, page_habits, page_low_spoons, page_med_tracker]:
        page_fn(c)
        c.showPage()
    c.save()
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    build()
