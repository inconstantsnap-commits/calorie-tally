#!/usr/bin/env python3
"""Generate simple launcher icon PNGs for Calorie Tally.

Draws the letters "CT" in white on the app's purple, using a tiny 5x7
bitmap font, and writes a valid PNG with only the Python standard library.
Usage: make_icon.py <size_px> <output_png>
"""
import struct
import sys
import zlib

FONT = {
    "C": [
        "01110",
        "10001",
        "10000",
        "10000",
        "10000",
        "10001",
        "01110",
    ],
    "T": [
        "11111",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
        "00100",
    ],
}
TEXT = "CT"
BG = (108, 52, 131)   # #6c3483, the app accent
FG = (255, 255, 255)


def render(size):
    rows = 7
    cols = len(TEXT) * 5 + (len(TEXT) - 1) * 1
    # Fit the letter block into ~72% of the icon width.
    cell = max(1, int(size * 0.72 / cols))
    block_w = cell * cols
    block_h = cell * rows
    ox = (size - block_w) // 2
    oy = (size - block_h) // 2
    pixels = [[BG] * size for _ in range(size)]
    for li, ch in enumerate(TEXT):
        glyph = FONT[ch]
        gx = ox + li * 6 * cell
        for y in range(rows):
            for x in range(5):
                if glyph[y][x] == "1":
                    for dy in range(cell):
                        for dx in range(cell):
                            pixels[oy + y * cell + dy][gx + x * cell + dx] = FG
    return pixels


def write_png(pixels, path):
    h = len(pixels)
    w = len(pixels[0])
    raw = b""
    for row in pixels:
        raw += b"\x00" + b"".join(bytes(px) for px in row)

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        c += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return c

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    size = int(sys.argv[1])
    write_png(render(size), sys.argv[2])
