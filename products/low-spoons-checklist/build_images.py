# -*- coding: utf-8 -*-
"""Builds Etsy listing photo set for 'Low-Spoons Mode — Simplified Daily Checklist'."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _brand_kit import P_SAGE_TINT, P_MARIGOLD_TINT, P_SAGE_DARK, P_TERRACOTTA_DARK
from _listing_kit import build_hero, build_collage, build_callout, build_checklist, build_faq

HERE = os.path.dirname(__file__)
IMG_DIR = os.path.join(HERE, "listing_images")


def main():
    build_hero(
        IMG_DIR, os.path.join(IMG_DIR, "listing_1_hero.jpg"),
        title="Low-Spoons Mode", subtitle="Simplified Checklist",
        badge_text="2-PAGE PDF  ·  INSTANT DOWNLOAD", cover_page=1, title_size=84,
    )
    build_collage(
        IMG_DIR, os.path.join(IMG_DIR, "listing_2_whats_inside.jpg"),
        title="What's Inside", subtitle="2 pages for the days that are just... a lot",
        items=[(1, "Daily Checklist"), (2, "Spoon Budget")],
    )
    build_callout(
        IMG_DIR, os.path.join(IMG_DIR, "listing_3_checklist.jpg"),
        page_num=1, headline_lines=["For the days", "that are just", "…a lot."],
        body_text="A stripped-down page: three must-dos at most, bare-minimum self-care, and a "
                   "reminder that rest is not falling behind.",
        accent_bg=P_SAGE_TINT, headline_color=P_SAGE_DARK,
    )
    build_callout(
        IMG_DIR, os.path.join(IMG_DIR, "listing_4_budget.jpg"),
        page_num=2, headline_lines=["Spend your", "spoons", "on purpose."],
        body_text="A visual spoon-theory budget — start the day with a number that feels true, "
                   "then track where each one actually goes.",
        accent_bg=P_MARIGOLD_TINT, headline_color=P_TERRACOTTA_DARK,
    )
    build_checklist(
        os.path.join(IMG_DIR, "listing_5_whats_included.jpg"),
        title="What You Get", subtitle="One 2-page PDF, ready to print at home",
        items=[
            "Low-Spoons Daily Page (3 must-dos, max)",
            "Bare-Minimum Self-Care checklist",
            "Spoon Budget tracker (12-spoon visual)",
            "Task-by-task spoon-cost log",
        ],
        footer_lines=["Instant PDF download  ·  US Letter (8.5″ × 11″)", "Print at home, as many times as you like  ·  Personal use"],
        bg=P_SAGE_DARK,
    )
    build_faq(
        os.path.join(IMG_DIR, "listing_6_faq.jpg"),
        title="Good to Know",
        rows=[
            ("Format", "One PDF file, delivered instantly after purchase — no waiting, no shipping."),
            ("Size", "US Letter (8.5″ × 11″). Print at home or at any copy shop."),
            ("Devices", "Opens on anything that reads a PDF — phone, tablet, or computer."),
            ("Use", "For personal use. Print it as many times as you need for yourself."),
            ("Support", "File trouble or questions? Message the shop — we reply fast."),
        ],
    )
    print("done")


if __name__ == "__main__":
    main()
