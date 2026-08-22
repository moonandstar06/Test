# -*- coding: utf-8 -*-
"""Builds Etsy listing photo set for 'Dopamine Menu + Reward Tracker'."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from _brand_kit import P_TERRACOTTA_TINT, P_SAGE_TINT, P_TERRACOTTA_DARK, P_SAGE_DARK, P_MARIGOLD, P_SAGE
from _listing_kit import build_hero, build_collage, build_callout, build_checklist, build_faq

HERE = os.path.dirname(__file__)
IMG_DIR = os.path.join(HERE, "listing_images")


def main():
    build_hero(
        IMG_DIR, os.path.join(IMG_DIR, "listing_1_hero.jpg"),
        title="Dopamine Menu", subtitle="+ Reward Tracker",
        badge_text="2-PAGE PDF  ·  INSTANT DOWNLOAD", cover_page=1, title_size=96,
    )
    build_collage(
        IMG_DIR, os.path.join(IMG_DIR, "listing_2_whats_inside.jpg"),
        title="What's Inside", subtitle="2 pages built to make motivation easier to reach for",
        items=[(1, "Dopamine Menu"), (2, "Reward Tracker")],
    )
    build_callout(
        IMG_DIR, os.path.join(IMG_DIR, "listing_3_menu.jpg"),
        page_num=1, headline_lines=["Motivation", "isn't a", "personality trait."],
        body_text="It's fuel. Three tiers of rewards — small, medium, big — so you always have "
                   "something to reach for before a hard task, not just after you're already burnt out.",
        accent_bg=P_TERRACOTTA_TINT, headline_color=P_TERRACOTTA_DARK,
    )
    build_callout(
        IMG_DIR, os.path.join(IMG_DIR, "listing_4_tracker.jpg"),
        page_num=2, headline_lines=["4 weeks of", "proof you", "followed through."],
        body_text="No streak-shaming design — a gap in the tracker is just a gap. This is for noticing "
                   "your own patterns, not grading yourself on them.",
        accent_bg=P_SAGE_TINT, headline_color=P_SAGE_DARK,
    )
    build_checklist(
        os.path.join(IMG_DIR, "listing_5_whats_included.jpg"),
        title="What You Get", subtitle="One 2-page PDF, ready to print at home",
        items=[
            "Dopamine Menu (Small / Medium / Big reward tiers)",
            "Write-your-own reward lines in every tier",
            "4-Week Reward Tracker, day by day",
            "Weekly reward-in-advance planning line",
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
