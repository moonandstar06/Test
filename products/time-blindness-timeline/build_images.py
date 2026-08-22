# -*- coding: utf-8 -*-
"""Builds Etsy listing photo set for 'Time-Blindness Daily Timeline Sheet'."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _brand_kit import P_TERRACOTTA_TINT, P_SAGE_TINT, P_TERRACOTTA_DARK, P_SAGE_DARK
from _listing_kit import build_hero, build_collage, build_callout, build_checklist, build_faq

HERE = os.path.dirname(__file__)
IMG_DIR = os.path.join(HERE, "listing_images")


def main():
    build_hero(
        IMG_DIR, os.path.join(IMG_DIR, "listing_1_hero.jpg"),
        title="Time-Blindness", subtitle="Daily Timeline",
        badge_text="2-PAGE PDF  ·  INSTANT DOWNLOAD", cover_page=1, title_size=88,
    )
    build_collage(
        IMG_DIR, os.path.join(IMG_DIR, "listing_2_whats_inside.jpg"),
        title="What's Inside", subtitle="2 pages built around one question: what time is it, actually?",
        items=[(1, "Daily Timeline"), (2, "Week at a Glance")],
    )
    build_callout(
        IMG_DIR, os.path.join(IMG_DIR, "listing_3_daily.jpg"),
        page_num=1, headline_lines=["Time blindness", "gets a real", "visual timeline."],
        body_text="Not just an hour-by-hour list — six color-coded windows from early morning to "
                   "night, plus a brain dump, so the day has a shape you can actually feel.",
        accent_bg=P_TERRACOTTA_TINT, headline_color=P_TERRACOTTA_DARK,
    )
    build_callout(
        IMG_DIR, os.path.join(IMG_DIR, "listing_4_week.jpg"),
        page_num=2, headline_lines=["See your", "whole week", "at once."],
        body_text="A mini timeline for every day of the week, side by side — plan ahead without "
                   "holding seven schedules in your head at the same time.",
        accent_bg=P_SAGE_TINT, headline_color=P_SAGE_DARK,
    )
    build_checklist(
        os.path.join(IMG_DIR, "listing_5_whats_included.jpg"),
        title="What You Get", subtitle="One 2-page PDF, ready to print at home",
        items=[
            "Daily Timeline (6 color-coded time windows)",
            "Brain Dump space on every daily page",
            "Week at a Glance (all 7 days, mini timelines)",
            "Fill-in-pencil friendly — plans can change",
        ],
        footer_lines=["Instant PDF download  ·  US Letter (8.5″ × 11″)", "Print at home, as many times as you like  ·  Personal use"],
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
