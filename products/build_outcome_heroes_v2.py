# -*- coding: utf-8 -*-
"""Builds outcome-focused hero images (#1) for the 3 new printables, same
treatment as the flagship's redo."""
import os
from _outcome_hero_kit import build_outcome_hero
from _brand_kit import P_TERRACOTTA, P_CREAM, P_MARIGOLD, P_TERRACOTTA_DARK, P_SAGE_DARK

BASE = os.path.dirname(__file__)

build_outcome_hero(
    img_dir=os.path.join(BASE, "dopamine-menu-tracker", "listing_images"),
    page_num=1,
    title="DOPAMINE MENU",
    subtitle="Reward yourself before you burn out, not after.",
    pills=[
        ("BUILD YOUR OWN MENU", P_TERRACOTTA, P_CREAM),
        ("4-WEEK TRACKER", P_MARIGOLD, P_TERRACOTTA_DARK),
        ("NO STREAK SHAMING", P_SAGE_DARK, P_CREAM),
    ],
    out_path=os.path.join(BASE, "dopamine-menu-tracker", "listing_images", "listing_1_hero_v2.jpg"),
    title_size=84,
)

build_outcome_hero(
    img_dir=os.path.join(BASE, "time-blindness-timeline", "listing_images"),
    page_num=1,
    title="TIME-BLINDNESS TIMELINE",
    subtitle="See your day in color, not just numbers.",
    pills=[
        ("6 COLOR-CODED BLOCKS", P_TERRACOTTA, P_CREAM),
        ("BRAIN DUMP SPACE", P_MARIGOLD, P_TERRACOTTA_DARK),
        ("WEEK AT A GLANCE", P_SAGE_DARK, P_CREAM),
    ],
    out_path=os.path.join(BASE, "time-blindness-timeline", "listing_images", "listing_1_hero_v2.jpg"),
    title_size=64,
)

build_outcome_hero(
    img_dir=os.path.join(BASE, "low-spoons-checklist", "listing_images"),
    page_num=1,
    title="LOW-SPOONS MODE",
    subtitle="For the days that are just... a lot.",
    pills=[
        ("3 MUST-DOS, MAX", P_SAGE_DARK, P_CREAM),
        ("SPOON BUDGET TRACKER", P_MARIGOLD, P_TERRACOTTA_DARK),
        ("REST IS NOT FAILURE", P_TERRACOTTA, P_CREAM),
    ],
    out_path=os.path.join(BASE, "low-spoons-checklist", "listing_images", "listing_1_hero_v2.jpg"),
    title_size=80,
)

print("all done")
