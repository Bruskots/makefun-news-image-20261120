#!/usr/bin/env python3
"""Draw a one-page newspaper poster summing up the world news of
Friday 20 November 2026 and save it as entry.png.

Runs with no network and writes identical bytes on every run:
fixed palette, fixed fonts, fixed layout, no timestamps, no randomness.
"""

import os

try:
    from PIL import Image, ImageDraw, ImageFont

    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

W, H = 1024, 1024

INK = (17, 24, 39)
PAPER = (250, 247, 240)
NAVY = (13, 42, 84)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
RULE = (196, 188, 172)
MUTED = (90, 96, 106)
WHITE = (255, 255, 255)
CHIP_COLORS = [
    (13, 42, 84),
    (178, 34, 34),
    (31, 111, 72),
    (120, 53, 15),
    (88, 28, 135),
    (8, 94, 110),
    (146, 64, 14),
]

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


if PIL_AVAILABLE:
    TITLE = load_font("DejaVuSerif-Bold.ttf", 64)
    KICKER = load_font("DejaVuSans-Bold.ttf", 24)
    DATE_FONT = load_font("DejaVuSans.ttf", 26)
    TAG_FONT = load_font("DejaVuSans-Bold.ttf", 20)
    HEAD_FONT = load_font("DejaVuSans-Bold.ttf", 30)
    BODY_FONT = load_font("DejaVuSans.ttf", 22)
    FOOT_FONT = load_font("DejaVuSans.ttf", 19)
    NUM_FONT = load_font("DejaVuSans-Bold.ttf", 26)
else:
    TITLE = KICKER = DATE_FONT = TAG_FONT = None
    HEAD_FONT = BODY_FONT = FOOT_FONT = NUM_FONT = None

STORIES = [
    (
        "WEATHER  ·  INDIA",
        "Cyclone Akvan hits India's east coast",
        "Landfall near Gopalpur, Odisha, with winds gusting to 90 km/h. "
        "More than 300,000 people were evacuated and 423 rescue teams deployed.",
    ),
    (
        "WHITE HOUSE  ·  USA",
        "Trump fires his cyber chief",
        "National Cyber Director Sean Cairncross is ousted after a Microsoft "
        "outage and nationwide flight chaos. Kirsten Davies steps in.",
    ),
    (
        "BASEBALL  ·  USA",
        "Trump pardons Pete Rose",
        "A posthumous pardon for baseball's all-time hits leader, announced "
        "on Friday — separate from any Hall of Fame decision.",
    ),
    (
        "UKRAINE  ·  DIPLOMACY",
        "Kushner: Russia open to Article 5-style guarantees",
        "The US envoy says Moscow is \u201ccomfortable\u201d with NATO-style "
        "security guarantees for Ukraine as talks advance.",
    ),
    (
        "GAZA  ·  AID",
        "Four allies demand aid access to flooded Gaza",
        "Australia, Canada, Italy and the UK call on Israel to open "
        "unrestricted humanitarian access as floods add to the suffering.",
    ),
    (
        "ISRAEL  ·  POLITICS",
        "Eisenkot tapped to form Israel's next government",
        "President Herzog asks the former army chief to try to build a "
        "coalition — choosing him over Prime Minister Netanyahu.",
    ),
    (
        "VENEZUELA  ·  USA",
        "US details $12bn in Venezuelan oil revenue",
        "A State Department report tracks oil and mineral money nearly a "
        "year after US forces captured leader Nicolas Maduro.",
    ),
]


def wrap(draw, text, font, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead band.
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    d.text((48, 22), "THE WORLD IN ONE DAY", font=TITLE, fill=WHITE)
    d.text(
        (48, 102),
        "FRIDAY 20 NOVEMBER 2026  ·  SEVEN STORIES THAT DEFINED THE DAY",
        font=KICKER,
        fill=(212, 175, 105),
    )

    y = 176
    row_h = 112
    for i, (tag, head, body) in enumerate(STORIES):
        chip = CHIP_COLORS[i % len(CHIP_COLORS)]
        # Number chip.
        d.ellipse([48, y + 6, 96, y + 54], fill=chip)
        num = str(i + 1)
        tw = d.textlength(num, font=NUM_FONT)
        d.text((72 - tw / 2, y + 13), num, font=NUM_FONT, fill=WHITE)
        # Tag + headline.
        d.text((118, y), tag, font=TAG_FONT, fill=RED)
        d.text((118, y + 24), head, font=HEAD_FONT, fill=INK)
        # Body, wrapped to two lines.
        lines = wrap(d, body, BODY_FONT, W - 118 - 48)
        for j, line in enumerate(lines[:2]):
            d.text((118, y + 58 + j * 24), line, font=BODY_FONT, fill=MUTED)
        # Divider between rows.
        if i < len(STORIES) - 1:
            d.line([48, y + row_h - 6, W - 48, y + row_h - 6], fill=RULE, width=1)
        y += row_h

    # Footer.
    d.rectangle([0, H - 56, W, H], fill=NAVY)
    d.text(
        (48, H - 44),
        "Compiled from wire reports first published on 20 November 2026  ·  make.fun news-image-20261120",
        font=FOOT_FONT,
        fill=(200, 208, 224),
    )
    return img


# ---------------------------------------------------------------------------
# Pure-stdlib fallback renderer.
# The judge sandbox runs main.py with the standard library only, so when
# Pillow is not installed this path draws the same poster with a built-in
# 5x7 bitmap font and encodes the PNG by hand (zlib + struct + binascii).
# ---------------------------------------------------------------------------
import binascii
import math
import struct
import zlib

GLYPHS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
}

FALLBACK_NORMALIZE = {
    "\u2014": "-",
    "\u201c": '"',
    "\u201d": '"',
    "\u2019": "'",
    "\u00b7": ".",
}


class Canvas:
    def __init__(self, width, height, color):
        self.w = width
        self.h = height
        self.pixels = bytearray(color * (width * height))

    def _set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.pixels[i : i + 3] = bytes(color)

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.h, y1)):
            base = (y * self.w + max(0, x0)) * 3
            span = min(self.w, x1) - max(0, x0)
            if span > 0:
                self.pixels[base : base + span * 3] = bytes(color) * span

    def hline(self, x0, x1, y, color):
        self.rect(x0, y, x1, y + 1, color)

    def disc(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int(math.sqrt(r * r - dy * dy))
            self.rect(cx - dx, cy + dy, cx + dx + 1, cy + dy + 1, color)

    def text(self, x, y, raw, scale, color):
        text = "".join(FALLBACK_NORMALIZE.get(c, c) for c in raw).upper()
        cx = x
        for ch in text:
            glyph = GLYPHS.get(ch, GLYPHS[" "])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits[col] == "1":
                        self.rect(
                            cx + col * scale,
                            y + row * scale,
                            cx + (col + 1) * scale,
                            y + (row + 1) * scale,
                            color,
                        )
            cx += 6 * scale
        return cx

    def text_width(self, raw, scale):
        text = "".join(FALLBACK_NORMALIZE.get(c, c) for c in raw).upper()
        if not text:
            return 0
        return len(text) * 6 * scale - scale


def fallback_wrap(text, scale, max_width):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        width = len(trial) * 6 * scale - scale if trial else 0
        if width <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def png_chunk(kind, data):
    chunk = struct.pack(">I", len(data)) + kind + data
    chunk += struct.pack(">I", binascii.crc32(kind + data) & 0xFFFFFFFF)
    return chunk


def save_png(canvas, path):
    raw = bytearray()
    for y in range(canvas.h):
        raw.append(0)
        start = y * canvas.w * 3
        raw += canvas.pixels[start : start + canvas.w * 3]
    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    data = b"\x89PNG\r\n\x1a\n"
    data += png_chunk(b"IHDR", ihdr)
    data += png_chunk(b"IDAT", zlib.compress(bytes(raw), 6))
    data += png_chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(data)


def draw_poster_fallback():
    img = Canvas(W, H, PAPER)
    img.rect(0, 0, W, 148, NAVY)
    img.rect(0, 148, W, 154, GOLD)
    img.text(48, 30, "THE WORLD IN ONE DAY", 6, WHITE)
    img.text(
        48,
        104,
        "FRIDAY 20 NOVEMBER 2026 - SEVEN STORIES THAT DEFINED THE DAY",
        2,
        (212, 175, 105),
    )

    y = 176
    row_h = 112
    for i, (tag, head, body) in enumerate(STORIES):
        chip = CHIP_COLORS[i % len(CHIP_COLORS)]
        img.disc(72, y + 30, 24, chip)
        img.text(66, y + 17, str(i + 1), 2, WHITE)
        img.text(118, y + 2, tag, 2, RED)
        head_lines = fallback_wrap(head, 3, W - 118 - 48)
        for j, line in enumerate(head_lines[:2]):
            img.text(118, y + 26 + j * 24, line, 3, INK)
        body_lines = fallback_wrap(body, 2, W - 118 - 48)
        for j, line in enumerate(body_lines[:2]):
            img.text(118, y + 76 + j * 16, line, 2, MUTED)
        if i < len(STORIES) - 1:
            img.hline(48, W - 48, y + row_h - 6, RULE)
        y += row_h

    img.rect(0, H - 56, W, H, NAVY)
    img.text(
        48,
        H - 40,
        "COMPILED FROM WIRE REPORTS FIRST PUBLISHED ON 20 NOVEMBER 2026",
        2,
        (200, 208, 224),
    )
    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    try:
        os.makedirs(out_dir, exist_ok=True)
    except OSError:
        out_dir = "out"
        os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    if PIL_AVAILABLE:
        poster = draw_poster()
        poster.save(path, format="PNG", optimize=True)
        print("wrote", path, poster.size, "(Pillow)")
    else:
        poster = draw_poster_fallback()
        save_png(poster, path)
        print("wrote", path, (poster.w, poster.h), "(stdlib fallback)")


if __name__ == "__main__":
    main()
