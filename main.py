#!/usr/bin/env python3
"""news-image-20261117: draw a newspaper front page summing up the world news
of Tuesday 17 November 2026 as a single 1024x1024 PNG.

Standard library only (os, struct, zlib): the grading sandbox installs
nothing and has no network, so the image is drawn pixel by pixel with an
embedded 5x7 bitmap font and a hand-rolled PNG encoder. Fully
deterministic: no randomness, no clock, no I/O besides the output file.
Writes $MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (179, 39, 30)
BLUE = (29, 78, 137)
SEA = (58, 110, 165)
SKY = (205, 225, 240)
SMOKE = (110, 110, 108)
GREY = (96, 96, 94)
WHITE = (255, 255, 255)

# 5x7 bitmap font. Each glyph is 7 rows; bit 4 is the leftmost column.
FONT = {
    "A": (0x0E, 0x11, 0x11, 0x11, 0x1F, 0x11, 0x11),
    "B": (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    "C": (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    "D": (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    "E": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    "F": (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    "G": (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0F),
    "H": (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    "I": (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "J": (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    "K": (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    "L": (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    "M": (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    "N": (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    "O": (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "P": (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    "Q": (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    "R": (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    "S": (0x0F, 0x10, 0x10, 0x0E, 0x01, 0x01, 0x1E),
    "T": (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    "U": (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    "V": (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    "W": (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    "X": (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    "Y": (0x11, 0x11, 0x0A, 0x04, 0x04, 0x04, 0x04),
    "Z": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    "0": (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    "1": (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    "2": (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    "3": (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    "4": (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    "5": (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    "6": (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    "7": (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    "8": (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    "9": (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    " ": (0, 0, 0, 0, 0, 0, 0),
    ".": (0, 0, 0, 0, 0, 0x0C, 0x0C),
    ",": (0, 0, 0, 0, 0x0C, 0x04, 0x08),
    ":": (0, 0x0C, 0x0C, 0, 0x0C, 0x0C, 0),
    ";": (0, 0x0C, 0x0C, 0, 0x0C, 0x04, 0x08),
    "'": (0x04, 0x04, 0x08, 0, 0, 0, 0),
    "!": (0x04, 0x04, 0x04, 0x04, 0x04, 0, 0x04),
    "?": (0x0E, 0x11, 0x01, 0x02, 0x04, 0, 0x04),
    "-": (0, 0, 0, 0x0E, 0, 0, 0),
    "/": (0x01, 0x01, 0x02, 0x04, 0x08, 0x10, 0x10),
    "(": (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ")": (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    "&": (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    "%": (0x19, 0x19, 0x02, 0x04, 0x08, 0x13, 0x13),
    "+": (0, 0x04, 0x04, 0x0E, 0x04, 0x04, 0),
    "=": (0, 0, 0x0E, 0, 0x0E, 0, 0),
    '"': (0x0A, 0x0A, 0x0A, 0, 0, 0, 0),
    "$": (0x04, 0x0F, 0x14, 0x0E, 0x05, 0x1E, 0x04),
}

# The day's news, as reported on 17 November 2026 (BBC, Al Jazeera,
# Reuters, AP, Spaceflight Now). Headlines are one line; summaries wrap
# to two lines at scale 3 inside the 944 px content column.
LEAD = {
    "kicker": "EUROPE / CONFLICT",
    "head": ["KERCH BRIDGE HIT,", "ROAD SPAN COLLAPSES"],
    "body": ("Ukraine struck the bridge linking Russia to occupied Crimea "
             "for the second time in under a day. Russia hit two bridges "
             "over the Dnipro in Kyiv in reply."),
}

ROWS = [
    {
        "kicker": "MIDDLE EAST / SHIPPING",
        "head": "TANKERS HIT BY MINES NEAR HORMUZ",
        "body": ("Two tankers struck mines and caught fire near Hormuz as "
                 "a third US carrier arrived in the region."),
    },
    {
        "kicker": "ASIA / DIPLOMACY",
        "head": "TRUMP LANDS IN ASIA FOR SUMMIT WEEK",
        "body": ("Trump arrived in Manila for ASEAN, then heads to Shenzhen "
                 "for APEC and talks with Xi and Putin."),
    },
    {
        "kicker": "EUROPE / MIGRATION",
        "head": "FIVE EU STATES PLAN RWANDA RETURN HUB",
        "body": ("Germany, Denmark, Austria, Greece and the Netherlands "
                 "plan a joint return facility in Rwanda."),
    },
    {
        "kicker": "BUSINESS / BANKING",
        "head": "JPMORGAN BLAMES BUG FOR BANK OUTAGE",
        "body": ("A bug slowed online banking, branches and Zelle on "
                 "Monday. The bank said it was not a cyberattack."),
    },
    {
        "kicker": "SPACE / LAUNCH",
        "head": "VULCAN ROCKET FAILS; 40 SATELLITES LOST",
        "body": ("A ULA Vulcan rocket failed minutes after launch, "
                 "destroying 40 Amazon internet satellites."),
    },
]

FOOTER = "SOURCES: BBC - AL JAZEERA - REUTERS - AP - SPACEFLIGHT NOW"


class Canvas:
    def __init__(self, w, h, bg):
        self.w = w
        self.h = h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x, y, w, h, color):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, color)

    def hline(self, x, y, w, color, thick=1):
        self.rect(x, y, w, thick, color)

    def circle(self, cx, cy, r, color):
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            for xx in range(cx - dx, cx + dx + 1):
                self.set(xx, cy + dy, color)

    def text_width(self, s, scale):
        return len(s) * 6 * scale - scale

    def text(self, x, y, s, scale, color, align="left"):
        # The embedded font covers capitals only; newspaper style is
        # all-caps, so normalise here instead of in every string.
        s = s.upper()
        if align == "center":
            x -= self.text_width(s, scale) // 2
        cx = x
        for ch in s:
            glyph = FONT.get(ch, FONT["?"])
            for row in range(7):
                bits = glyph[row]
                for col in range(5):
                    if bits >> (4 - col) & 1:
                        self.rect(cx + col * scale, y + row * scale,
                                  scale, scale, color)
            cx += 6 * scale
        return cx

    def wrap(self, s, scale, max_w):
        lines, cur = [], ""
        for word in s.split(" "):
            trial = word if not cur else cur + " " + word
            if self.text_width(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines


def draw_bridge(cv, x, y, w, h):
    """Simple Kerch Bridge scene: sky, sea, deck with a broken span."""
    cv.rect(x, y, w, h, SKY)
    cv.rect(x, y + h - 26, w, 26, SEA)
    # white wave ticks
    for wx in range(x + 12, x + w - 20, 46):
        cv.hline(wx, y + h - 12, 22, WHITE, 2)
    deck_y = y + h - 38
    # towers
    cv.rect(x + 250, y + 6, 8, deck_y - y - 6 + 8, GREY)
    cv.rect(x + 660, y + 6, 8, deck_y - y - 6 + 8, GREY)
    # deck, with a gap where the span fell
    cv.rect(x, deck_y, 430, 8, GREY)
    cv.rect(x + 514, deck_y, w - 514, 8, GREY)
    # fallen span in the water
    cv.rect(x + 448, deck_y + 14, 52, 6, GREY)
    # smoke rising from the gap
    cv.circle(x + 470, y + 16, 9, SMOKE)
    cv.circle(x + 486, y + 8, 12, SMOKE)
    cv.circle(x + 500, y + 20, 7, SMOKE)


def build():
    cv = Canvas(W, H, PAPER)
    mx = 40
    cw = W - 2 * mx  # 944 px content column

    # Masthead
    cv.text(W // 2, 30, "THE WORLD TODAY", 7, INK, align="center")
    cv.hline(mx, 92, cw, INK, 3)
    cv.hline(mx, 98, cw, INK, 1)
    cv.text(W // 2, 110, "TUESDAY, 17 NOVEMBER 2026", 3, INK,
            align="center")
    cv.hline(mx, 142, cw, INK, 2)

    # Lead story
    y = 158
    cv.text(mx, y, LEAD["kicker"], 2, RED)
    y += 22
    for line in LEAD["head"]:
        cv.text(mx, y, line, 5, INK)
        y += 40
    y += 4
    for line in cv.wrap(LEAD["body"], 3, cw):
        cv.text(mx, y, line, 3, INK)
        y += 26

    # Bridge illustration under the lead story
    draw_bridge(cv, mx, 356, cw, 72)
    cv.hline(mx, 444, cw, INK, 2)

    # Five more stories, one full-width row each (pitch 100 px:
    # kicker 14 + headline 28 + two body lines of 21 px).
    y = 462
    for row in ROWS:
        cv.text(mx, y, row["kicker"], 2, RED)
        cv.text(mx, y + 16, row["head"], 4, INK)
        yy = y + 48
        for line in cv.wrap(row["body"], 3, cw):
            cv.text(mx, yy, line, 3, INK)
            yy += 24
        y += 100
        if row is not ROWS[-1]:
            cv.hline(mx, y - 3, cw, (200, 196, 186), 1)

    # Footer
    cv.hline(mx, 962, cw, INK, 2)
    cv.text(W // 2, 974, FOOTER, 2, INK, align="center")
    return cv


def chunk(ctype, data):
    out = struct.pack(">I", len(data)) + ctype + data
    out += struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF)
    return out


def encode_png(cv):
    raw = bytearray()
    stride = cv.w * 3
    for yy in range(cv.h):
        raw.append(0)
        raw += cv.px[yy * stride:(yy + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "entry.png")
    with open(path, "wb") as f:
        f.write(encode_png(build()))
    print("wrote", path)


if __name__ == "__main__":
    main()
