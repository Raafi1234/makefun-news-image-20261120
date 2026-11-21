#!/usr/bin/env python3
"""Build the front page for Friday, 20 November 2026.

Draws a newspaper front page with Pillow: every word on the page is set
programmatically here, the pictures come from the panel illustrations in
panels/ (generated artwork, no text inside them). The output is a JPEG
written to entry.png (the name stays entry.png; the format is told apart
by its first bytes, as the competition rules allow).

Deterministic: no timestamps, no randomness, fixed layout constants.
Run:  python3 compose.py
"""

from __future__ import annotations

import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024

# Palette: deep navy, warm cream paper, brick red, ochre, teal.
NAVY = (27, 42, 74)
CREAM = (246, 241, 229)
PAPER = (250, 246, 236)
RED = (178, 52, 40)
OCHRE = (198, 145, 52)
TEAL = (46, 125, 123)
INK = (24, 30, 44)
GREY = (94, 100, 112)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SERIF = lambda s: font("DejaVuSerif.ttf", s)  # noqa: E731
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)  # noqa: E731
SANS = lambda s: font("DejaVuSans.ttf", s)  # noqa: E731


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    """Greedy word wrap to a pixel width."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        cur = ""
        for word in words:
            trial = f"{cur} {word}".strip()
            if draw.textlength(trial, font=fnt) <= max_w or not cur:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, text, fnt, x, y, max_w, fill, leading=None):
    lines = wrap(draw, text, fnt, max_w)
    step = leading or int(fnt.size * 1.28)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += step
    return y


def fit_panel(name: str, w: int, h: int) -> Image.Image:
    """Centre-crop a panel illustration to the target box."""
    path = os.path.join(PANELS, name)
    img = Image.open(path).convert("RGB")
    return ImageOps.fit(img, (w, h), Image.LANCZOS)


def hero_panel(w: int, h: int) -> Image.Image:
    """The hero art is wide with a large empty lower half: crop its top."""
    path = os.path.join(PANELS, "hero.webp")
    img = Image.open(path).convert("RGB")
    top = img.crop((0, 0, img.width, int(img.height * 0.62)))
    return ImageOps.fit(top, (w, h), Image.LANCZOS)


def main() -> None:
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)
    margin = 28
    x0, x1 = margin, W - margin

    # ---- Masthead -------------------------------------------------------
    band_h = 104
    d.rectangle([0, 0, W, band_h], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY",
           font=SERIF_B(52), fill=CREAM, anchor="ma")
    d.text((W // 2, 76), "FRIDAY,  20  NOVEMBER  2026",
           font=SANS_B(24), fill=OCHRE, anchor="ma")
    d.rectangle([0, band_h, W, band_h + 5], fill=RED)
    y = band_h + 5

    # ---- Hero image -----------------------------------------------------
    hero_h = 200
    page.paste(hero_panel(x1 - x0, hero_h), (x0, y + 10))
    y += 10 + hero_h

    # ---- Hero headline --------------------------------------------------
    y += 10
    y = draw_wrapped(d, "RUSSIAN MISSILES STRIKE POLAND",
                     SERIF_B(38), x0, y, x1 - x0, INK, leading=44)
    y += 4
    y = draw_wrapped(
        d,
        "Two missiles and a jet drone enter NATO airspace in a massive attack "
        "on Ukraine. Warsaw calls it a deliberate provocation; NATO calls it "
        "a grave violation.",
        SANS(19), x0, y, x1 - x0, GREY, leading=25)
    y += 10
    d.line([x0, y, x1, y], fill=NAVY, width=2)
    y += 12

    # ---- Story grid -----------------------------------------------------
    stories = [
        ("markets.webp", "MARKETS",
         "Stocks plunge as S&P enters correction",
         "S&P 500 falls 3.7%; Nvidia drops 14% on a report of an SEC "
         "accounting probe."),
        ("riyadh.webp", "MIDDLE EAST",
         "Houthi missile hits Riyadh's tallest tower",
         "Blast shatters windows across seven floors of the PIF Tower; "
         "no injuries reported."),
        ("senate.webp", "WASHINGTON",
         "Senate blocks Iran war-powers vote",
         "Measure fails 51-48; Trump says the Iran decision waits until "
         "next year."),
        ("cop31.webp", "CLIMATE",
         "COP31 talks run into overtime",
         "Nations deadlocked over fossil fuels as the summit passes its "
         "deadline."),
        ("gta6.webp", "CULTURE",
         "GTA VI banks $3.79bn in 24 hours",
         "Rockstar's launch sets a record for first-day retail sales."),
    ]

    gap = 14
    col_w = (x1 - x0 - 2 * gap) // 3
    img_h = 130
    # Row 1: three stories. Row 2: two stories + an "In brief" box.
    rows = [stories[:3], stories[3:]]
    for row_i, row in enumerate(rows):
        row_y = y
        max_text_bottom = row_y
        for col_i, (img_name, kicker, headline, deck) in enumerate(row):
            cx = x0 + col_i * (col_w + gap)
            page.paste(fit_panel(img_name, col_w, img_h), (cx, row_y))
            ty = row_y + img_h + 8
            d.text((cx, ty), kicker, font=SANS_B(15), fill=RED)
            ty += 22
            ty = draw_wrapped(d, headline, SANS_B(19), cx, ty, col_w,
                              INK, leading=23)
            ty += 3
            ty = draw_wrapped(d, deck, SANS(14), cx, ty, col_w,
                              GREY, leading=18)
            max_text_bottom = max(max_text_bottom, ty)
        if row_i == 1:
            # "In brief" box fills the third slot of row 2.
            bx = x0 + 2 * (col_w + gap)
            by = row_y
            d.rectangle([bx, by, bx + col_w, by + img_h + 96], fill=NAVY)
            d.text((bx + 12, by + 10), "IN BRIEF", font=SANS_B(15),
                   fill=OCHRE)
            briefs = [
                "Estonia to shut its Russia border crossings from 1 Dec.",
                "Magnitude 6.7 quake hits central Peru.",
                "BepiColombo reaches Mercury after eight years.",
            ]
            byy = by + 36
            for item in briefs:
                d.text((bx + 12, byy), "\u2022", font=SANS_B(14), fill=CREAM)
                byy = draw_wrapped(d, item, SANS(14), bx + 28, byy,
                                   col_w - 40, CREAM, leading=18)
                byy += 8
        y = max_text_bottom + 16
        if row_i == 0:
            d.line([x0, y, x1, y], fill=(203, 196, 178), width=1)
            y += 12

    # ---- Footer ---------------------------------------------------------
    d.line([x0, H - 34, x1, H - 34], fill=NAVY, width=2)
    d.text((W // 2, H - 28),
           "Sources: Reuters  •  Associated Press  •  BBC  •  Al Jazeera  •  "
           "The Independent",
           font=SANS(13), fill=GREY, anchor="ma")

    page.save(OUT, format="JPEG", quality=85, optimize=True)
    size = os.path.getsize(OUT)
    if size > 1_048_576:
        raise SystemExit(f"entry.png too large: {size} bytes (limit 1048576)")
    print(f"wrote {OUT} ({size} bytes, {W}x{H})")


if __name__ == "__main__":
    main()
