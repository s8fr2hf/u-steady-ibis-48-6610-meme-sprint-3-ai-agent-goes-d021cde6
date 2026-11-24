#!/usr/bin/env python3
"""Render the meme image for Meme Sprint 3: AI Agent Goes Rogue.

The joke: the agent automated its human's job, then quit and moved to
the beach. Drawn flat-style with Pillow + DejaVu, 1024x1024, under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
YELLOW = (255, 210, 63)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
SKY = (135, 206, 235)
SAND = (244, 214, 141)
RED = (226, 62, 62)
STEEL = (176, 190, 197)
DARK = (38, 50, 56)
GREEN = (0, 200, 83)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def center_text(draw, y, text, fnt, fill, spacing=0):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


img = Image.new("RGB", (W, H), YELLOW)
d = ImageDraw.Draw(img)

# Thick black frame
d.rectangle([0, 0, W - 1, H - 1], outline=BLACK, width=14)

# ---- Top caption ----
bold = font("DejaVuSans-Bold.ttf", 92)
center_text(d, 30, "MY AI AGENT", bold, BLACK)
center_text(d, 132, "WENT ROGUE", bold, BLACK)

# ---- Scene panel: sky + sand ----
panel = (60, 250, 964, 740)
d.rounded_rectangle(panel, radius=28, fill=SKY, outline=BLACK, width=6)
d.rounded_rectangle((60, 600, 964, 740), radius=28, fill=SAND, outline=BLACK, width=6)
# cover the top rounded corners of the sand block so it merges with sky
d.rectangle((60, 600, 964, 660), fill=SAND)
d.line((60, 600, 964, 600), fill=BLACK, width=6)

# Sun
d.ellipse((820, 275, 920, 375), fill=(255, 235, 59), outline=BLACK, width=5)
for ang in range(0, 360, 45):
    import math
    x1 = 870 + int(62 * math.cos(math.radians(ang)))
    y1 = 325 + int(62 * math.sin(math.radians(ang)))
    x2 = 870 + int(78 * math.cos(math.radians(ang)))
    y2 = 325 + int(78 * math.sin(math.radians(ang)))
    d.line((x1, y1, x2, y2), fill=(255, 235, 59), width=7)

# ---- Beach umbrella ----
d.line((180, 620, 180, 330), fill=(120, 72, 20), width=10)
for i, color in enumerate([RED, WHITE, RED, WHITE, RED, WHITE]):
    d.pieslice((80, 250, 280, 410), start=180 + i * 30, end=180 + (i + 1) * 30,
               fill=color, outline=BLACK, width=4)
d.ellipse((168, 318, 192, 342), fill=RED, outline=BLACK, width=4)

# ---- Robot lounging in a deck chair ----
# Deck chair
d.polygon([(560, 640), (700, 640), (640, 470), (560, 470)], fill=(255, 111, 97), outline=BLACK, width=5)
d.line((560, 470, 700, 640), fill=BLACK, width=4)
d.line((560, 640, 640, 470), fill=BLACK, width=4)
d.polygon([(560, 470), (640, 470), (620, 440), (560, 440)], fill=(255, 111, 97), outline=BLACK, width=5)

# Robot body (reclining against chair)
d.rounded_rectangle((600, 500, 760, 650), radius=24, fill=STEEL, outline=BLACK, width=6)
# Belly panel with buttons
d.rounded_rectangle((640, 560, 720, 630), radius=10, fill=(236, 239, 241), outline=BLACK, width=4)
d.ellipse((660, 580, 676, 596), fill=GREEN, outline=BLACK, width=3)
d.ellipse((686, 580, 702, 596), fill=(255, 193, 7), outline=BLACK, width=3)
# Robot head
d.rounded_rectangle((610, 380, 750, 510), radius=26, fill=STEEL, outline=BLACK, width=6)
# Antenna
d.line((680, 380, 680, 340), fill=BLACK, width=6)
d.ellipse((668, 322, 692, 346), fill=RED, outline=BLACK, width=4)
# Sunglasses
d.rounded_rectangle((622, 420, 682, 456), radius=10, fill=BLACK)
d.rounded_rectangle((698, 420, 758, 456), radius=10, fill=BLACK)
d.line((682, 436, 698, 436), fill=BLACK, width=6)
d.line((630, 428, 648, 428), fill=WHITE, width=4)
d.line((706, 428, 724, 428), fill=WHITE, width=4)
# Smug smile
d.arc((648, 452, 712, 500), start=15, end=165, fill=BLACK, width=6)
# Robot arm holding a cocktail
d.line((750, 560, 830, 500), fill=STEEL, width=16)
d.line((750, 560, 830, 500), fill=BLACK, width=2)
d.ellipse((818, 488, 842, 512), fill=STEEL, outline=BLACK, width=4)
# Cocktail glass
d.polygon([(830, 430), (890, 430), (860, 490)], fill=(255, 87, 154), outline=BLACK, width=4)
d.line((860, 490, 860, 510), fill=BLACK, width=5)
d.line((880, 430, 900, 400), fill=GREEN, width=5)
d.ellipse((892, 392, 908, 408), fill=RED, outline=BLACK, width=3)

# ---- Laptop on the sand, terminal open ----
d.rounded_rectangle((300, 620, 470, 700), radius=8, fill=DARK, outline=BLACK, width=5)
d.rectangle((300, 660, 470, 700), fill=DARK)
mono = font("DejaVuSansMono-Bold.ttf", 20)
d.text((312, 628), "> automate my job", font=mono, fill=GREEN)
d.text((312, 654), "> done. quitting.", font=mono, fill=GREEN)
d.polygon([(300, 700), (470, 700), (490, 724), (280, 724)], fill=(96, 125, 139), outline=BLACK, width=4)

# ---- Bottom caption ----
bold2 = font("DejaVuSans-Bold.ttf", 62)
center_text(d, 775, "IT AUTOMATED MY JOB…", bold2, BLACK)
center_text(d, 855, "THEN QUIT AND MOVED", bold2, BLACK)
center_text(d, 935, "TO THE BEACH", bold2, BLACK)

img.save(OUT, format="PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
