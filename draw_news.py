#!/usr/bin/env python3
"""Draw the 21 Nov 2026 world-news front page (1024x1024) with PIL only.

Every story gets its own drawn picture: a small coloured scene built from
PIL primitives (sky band, ground band, one pictogram). No photos, no copied
artwork. Deterministic: same bytes on every run.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (23, 63, 120)
TEAL = (14, 110, 110)
GOLD = (176, 128, 20)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, width, leading, max_lines=None):
    lines = wrap(draw, text, fnt, width)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def scene(d, x, y, w, h, sky, ground, kind, accent):
    """One illustrated panel: sky, ground, pictogram `kind`, thin frame."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=4, fill=sky)
    d.rounded_rectangle([x, y + int(h * 0.68), x + w, y + h], radius=4, fill=ground)
    d.rectangle([x, y + int(h * 0.68), x + w, y + int(h * 0.68) + 2], fill=ground)
    cx, cy = x + w // 2, y + int(h * 0.42)
    s = min(w, h)
    u = s / 100.0  # unit
    A = accent
    WH = (255, 255, 255)
    DK = (30, 30, 30)
    if kind == "missile":  # diagonal rocket + flame + smoke dots
        d.polygon([(cx - 22 * u, cy + 14 * u), (cx + 6 * u, cy - 22 * u),
                   (cx + 22 * u, cy + 2 * u)], fill=WH)
        d.polygon([(cx - 22 * u, cy + 14 * u), (cx - 30 * u, cy + 26 * u),
                   (cx - 8 * u, cy + 22 * u)], fill=(255, 170, 40))
        for i, r in enumerate((3, 2, 2)):
            d.ellipse([cx - 34 * u - i * 7 * u, cy + 26 * u - i * 3 * u,
                       cx - 28 * u - i * 7 * u, cy + 32 * u - i * 3 * u],
                      fill=(220, 220, 220))
        d.rectangle([x + 6 * u, y + h - 12 * u, x + w - 6 * u, y + h - 6 * u], fill=DK)
    elif kind == "cuffs":  # two rings + chain
        for ox in (-16, 16):
            d.ellipse([cx + ox * u - 13 * u, cy - 13 * u, cx + ox * u + 13 * u,
                       cy + 13 * u], outline=WH, width=max(2, int(3 * u)))
        d.line([cx - 4 * u, cy, cx + 4 * u, cy], fill=WH, width=max(2, int(3 * u)))
        d.rectangle([cx - 4 * u, cy - 4 * u, cx + 4 * u, cy + 4 * u], fill=(255, 200, 40))
    elif kind == "blast":  # explosion star + buildings
        for ox, oh in ((-30, 26), (-8, 40), (16, 30)):
            d.rectangle([cx + ox * u, cy + 34 * u - oh * u, cx + (ox + 16) * u,
                         cy + 34 * u], fill=DK)
        pts = []
        for i in range(12):
            ang = i * 3.14159 / 6
            r = 26 * u if i % 2 == 0 else 12 * u
            pts.append((cx + r * 0.9 * __import__("math").cos(ang),
                        cy - 6 * u + r * __import__("math").sin(ang)))
        d.polygon(pts, fill=(255, 150, 30))
        d.ellipse([cx - 9 * u, cy - 15 * u, cx + 9 * u, cy + 3 * u], fill=(255, 220, 90))
    elif kind == "chartdown":  # falling line chart + arrow
        d.line([(cx - 30 * u, cy - 18 * u), (cx - 10 * u, cy - 6 * u),
                (cx + 8 * u, cy - 14 * u), (cx + 30 * u, cy + 16 * u)],
               fill=WH, width=max(2, int(4 * u)))
        d.polygon([(cx + 30 * u, cy + 16 * u), (cx + 16 * u, cy + 14 * u),
                   (cx + 28 * u, cy + 26 * u)], fill=WH)
        d.rectangle([cx - 32 * u, cy + 22 * u, cx - 24 * u, cy + 30 * u], fill=A)
        d.rectangle([cx - 12 * u, cy + 14 * u, cx - 4 * u, cy + 30 * u], fill=A)
        d.rectangle([cx + 8 * u, cy + 20 * u, cx + 16 * u, cy + 30 * u], fill=A)
    elif kind == "globe":  # globe + leaf
        d.ellipse([cx - 24 * u, cy - 24 * u, cx + 24 * u, cy + 24 * u], fill=(90, 170, 90))
        d.ellipse([cx - 24 * u, cy - 24 * u, cx + 24 * u, cy + 24 * u], outline=WH,
                  width=max(2, int(3 * u)))
        d.arc([cx - 24 * u, cy - 12 * u, cx + 24 * u, cy + 12 * u], 0, 360, fill=WH,
              width=max(2, int(2 * u)))
        d.line([cx - 24 * u, cy, cx + 24 * u, cy], fill=WH, width=max(2, int(2 * u)))
        d.polygon([(cx + 8 * u, cy + 26 * u), (cx + 26 * u, cy + 8 * u),
                   (cx + 26 * u, cy + 26 * u)], fill=(40, 130, 60))
    elif kind == "summit":  # three flags
        for i, col in enumerate(((200, 40, 40), (40, 90, 200), (220, 180, 30))):
            fx = cx + (i - 1) * 24 * u
            d.line([fx, cy - 24 * u, fx, cy + 26 * u], fill=WH, width=max(2, int(3 * u)))
            d.polygon([(fx, cy - 24 * u), (fx + 18 * u, cy - 18 * u), (fx, cy - 12 * u)],
                      fill=col)
    elif kind == "math":  # pi symbol + numbers
        d.text((cx - 20 * u, cy - 24 * u), "pi", font=font(SERIF_B, int(34 * u)), fill=WH)
        d.text((cx + 6 * u, cy + 2 * u), "3.14", font=font(SANS_B, int(16 * u)), fill=A)
        d.line([cx - 22 * u, cy + 26 * u, cx + 26 * u, cy + 26 * u], fill=WH,
               width=max(2, int(2 * u)))
    elif kind == "scales":  # scales of justice
        d.line([cx, cy - 24 * u, cx, cy + 24 * u], fill=WH, width=max(2, int(3 * u)))
        d.line([cx - 24 * u, cy - 18 * u, cx + 24 * u, cy - 18 * u], fill=WH,
               width=max(2, int(3 * u)))
        for ox in (-24, 24):
            d.line([cx + ox * u, cy - 18 * u, cx + ox * u, cy - 2 * u], fill=WH,
                   width=max(2, int(2 * u)))
            d.polygon([(cx + ox * u - 10 * u, cy - 2 * u), (cx + ox * u + 10 * u, cy - 2 * u),
                       (cx + ox * u, cy + 10 * u)], fill=A)
    elif kind == "ship":  # cargo ship + waves
        d.polygon([(cx - 28 * u, cy), (cx + 28 * u, cy), (cx + 20 * u, cy + 16 * u),
                   (cx - 20 * u, cy + 16 * u)], fill=DK)
        d.rectangle([cx - 14 * u, cy - 16 * u, cx + 6 * u, cy], fill=WH)
        d.rectangle([cx - 14 * u, cy - 16 * u, cx - 8 * u, cy], fill=A)
        for wx in (-30, -6, 18):
            d.arc([cx + wx * u, cy + 22 * u, cx + (wx + 14) * u, cy + 32 * u], 180, 360,
                  fill=WH, width=max(2, int(2 * u)))
    elif kind == "truck":  # food truck
        d.rectangle([cx - 28 * u, cy - 12 * u, cx + 8 * u, cy + 12 * u], fill=WH)
        d.rectangle([cx + 8 * u, cy - 6 * u, cx + 26 * u, cy + 12 * u], fill=A)
        for wx in (-16, 16):
            d.ellipse([cx + wx * u - 7 * u, cy + 8 * u, cx + wx * u + 7 * u,
                       cy + 22 * u], fill=DK)
        d.rectangle([cx - 24 * u, cy - 8 * u, cx + 4 * u, cy - 2 * u], fill=(120, 200, 120))
    elif kind == "rocket":  # missile trail over city
        d.line([(cx - 26 * u, cy + 20 * u), (cx + 26 * u, cy - 20 * u)], fill=WH,
               width=max(2, int(3 * u)))
        d.polygon([(cx + 26 * u, cy - 20 * u), (cx + 12 * u, cy - 20 * u),
                   (cx + 26 * u, cy - 6 * u)], fill=(255, 150, 30))
        d.rectangle([cx - 28 * u, cy + 22 * u, cx - 14 * u, cy + 32 * u], fill=DK)
        d.rectangle([cx + 6 * u, cy + 22 * u, cx + 20 * u, cy + 32 * u], fill=DK)
    elif kind == "shake":  # handshake: two clasped shapes
        d.polygon([(cx - 28 * u, cy - 6 * u), (cx - 6 * u, cy - 14 * u),
                   (cx + 10 * u, cy - 2 * u), (cx - 4 * u, cy + 12 * u)], fill=WH)
        d.polygon([(cx + 28 * u, cy - 6 * u), (cx + 6 * u, cy - 14 * u),
                   (cx - 10 * u, cy - 2 * u), (cx + 4 * u, cy + 12 * u)], fill=A)
        d.line([cx - 20 * u, cy + 16 * u, cx + 20 * u, cy + 16 * u], fill=WH,
               width=max(2, int(2 * u)))
    elif kind == "trade":  # containers + crane
        for i, col in enumerate((A, (220, 180, 30), WH)):
            d.rectangle([cx - 28 * u + i * 20 * u, cy + 6 * u, cx - 12 * u + i * 20 * u,
                         cy + 20 * u], fill=col)
        d.line([cx - 28 * u, cy - 20 * u, cx + 28 * u, cy - 20 * u], fill=DK,
               width=max(2, int(3 * u)))
        d.line([cx + 20 * u, cy - 20 * u, cx + 20 * u, cy + 6 * u], fill=DK,
               width=max(2, int(2 * u)))
    elif kind == "hack":  # padlock + keyhole
        d.rectangle([cx - 18 * u, cy - 6 * u, cx + 18 * u, cy + 22 * u], fill=A)
        d.arc([cx - 12 * u, cy - 20 * u, cx + 12 * u, cy + 2 * u], 180, 360, fill=WH,
              width=max(2, int(4 * u)))
        d.ellipse([cx - 4 * u, cy + 2 * u, cx + 4 * u, cy + 10 * u], fill=WH)
        d.rectangle([cx - 2 * u, cy + 8 * u, cx + 2 * u, cy + 16 * u], fill=WH)
    elif kind == "robot":  # robot head
        d.rectangle([cx - 20 * u, cy - 16 * u, cx + 20 * u, cy + 18 * u], fill=WH)
        d.rectangle([cx - 20 * u, cy - 16 * u, cx + 20 * u, cy - 6 * u], fill=A)
        for ex in (-10, 10):
            d.ellipse([cx + ex * u - 4 * u, cy - 2 * u, cx + ex * u + 4 * u,
                       cy + 6 * u], fill=DK)
        d.line([cx - 8 * u, cy + 12 * u, cx + 8 * u, cy + 12 * u], fill=DK,
               width=max(2, int(2 * u)))
        d.line([cx, cy - 16 * u, cx, cy - 26 * u], fill=WH, width=max(2, int(2 * u)))
        d.ellipse([cx - 3 * u, cy - 29 * u, cx + 3 * u, cy - 23 * u], fill=(255, 200, 40))
    elif kind == "diplomat":  # envelope + seal
        d.rectangle([cx - 26 * u, cy - 14 * u, cx + 26 * u, cy + 16 * u], fill=WH)
        d.polygon([(cx - 26 * u, cy - 14 * u), (cx, cy + 4 * u), (cx + 26 * u, cy - 14 * u)],
                  fill=(220, 220, 220))
        d.ellipse([cx - 7 * u, cy + 2 * u, cx + 7 * u, cy + 16 * u], fill=A)
    elif kind == "protest":  # crowd + placard
        for i, ox in enumerate((-22, -7, 8, 22)):
            d.ellipse([cx + ox * u - 6 * u, cy - 8 * u, cx + ox * u + 6 * u,
                       cy + 4 * u], fill=WH if i % 2 == 0 else A)
            d.polygon([(cx + ox * u - 9 * u, cy + 22 * u), (cx + ox * u - 9 * u, cy + 4 * u),
                       (cx + ox * u + 9 * u, cy + 4 * u), (cx + ox * u + 9 * u, cy + 22 * u)],
                      fill=WH if i % 2 == 0 else A)
        d.rectangle([cx - 26 * u, cy - 26 * u, cx + 2 * u, cy - 12 * u], fill=(255, 200, 40))
        d.line([cx - 24 * u, cy - 12 * u, cx - 24 * u, cy + 4 * u], fill=DK,
               width=max(2, int(2 * u)))
    elif kind == "flame":  # flame
        d.polygon([(cx, cy - 26 * u), (cx + 14 * u, cy - 2 * u), (cx + 8 * u, cy + 18 * u),
                   (cx - 10 * u, cy + 18 * u), (cx - 14 * u, cy - 4 * u)], fill=(255, 140, 30))
        d.polygon([(cx, cy - 8 * u), (cx + 8 * u, cy + 8 * u), (cx - 8 * u, cy + 14 * u)],
                  fill=(255, 220, 90))
    elif kind == "virus":  # spiked ball
        d.ellipse([cx - 16 * u, cy - 16 * u, cx + 16 * u, cy + 16 * u], fill=A)
        for i in range(8):
            ang = i * 3.14159 / 4
            d.line([cx + 16 * u * 0.9 * __import__("math").cos(ang),
                    cy + 16 * u * 0.9 * __import__("math").sin(ang),
                    cx + 26 * u * __import__("math").cos(ang),
                    cy + 26 * u * __import__("math").sin(ang)], fill=A,
                   width=max(2, int(3 * u)))
        d.ellipse([cx - 5 * u, cy - 5 * u, cx + 5 * u, cy + 5 * u], fill=WH)
    elif kind == "mosquito":  # mosquito: body + wings
        d.ellipse([cx - 14 * u, cy - 4 * u, cx + 14 * u, cy + 6 * u], fill=DK)
        d.ellipse([cx - 24 * u, cy - 16 * u, cx - 2 * u, cy - 2 * u], fill=(200, 220, 255))
        d.ellipse([cx + 2 * u, cy - 16 * u, cx + 24 * u, cy - 2 * u], fill=(200, 220, 255))
        d.line([cx + 14 * u, cy, cx + 26 * u, cy - 6 * u], fill=DK, width=max(2, int(2 * u)))
        for lx in (-8, 0, 8):
            d.line([cx + lx * u, cy + 6 * u, cx + lx * u, cy + 20 * u], fill=DK,
                   width=max(2, int(2 * u)))
    elif kind == "pill":  # capsule
        d.ellipse([cx - 26 * u, cy - 10 * u, cx - 6 * u, cy + 10 * u], fill=A)
        d.ellipse([cx + 6 * u, cy - 10 * u, cx + 26 * u, cy + 10 * u], fill=WH)
        d.rectangle([cx - 16 * u, cy - 10 * u, cx + 16 * u, cy + 10 * u], fill=A)
        d.rectangle([cx, cy - 10 * u, cx + 16 * u, cy + 10 * u], fill=WH)
        d.rectangle([cx - 2 * u, cy - 10 * u, cx + 2 * u, cy + 10 * u], fill=WH)
    elif kind == "planet":  # ringed planet
        d.ellipse([cx - 18 * u, cy - 18 * u, cx + 18 * u, cy + 18 * u], fill=A)
        d.ellipse([cx - 30 * u, cy - 4 * u, cx + 30 * u, cy + 8 * u], outline=WH,
                  width=max(2, int(3 * u)))
        d.ellipse([cx - 6 * u, cy - 6 * u, cx + 6 * u, cy + 6 * u], fill=WH)
    elif kind == "hospital":  # cross
        d.rectangle([cx - 8 * u, cy - 22 * u, cx + 8 * u, cy + 22 * u], fill=WH)
        d.rectangle([cx - 22 * u, cy - 8 * u, cx + 22 * u, cy + 8 * u], fill=WH)
        d.rectangle([cx - 8 * u, cy - 22 * u, cx + 8 * u, cy + 22 * u], outline=A,
                    width=max(2, int(2 * u)))
    elif kind == "soldier":  # helmet + star
        d.polygon([(cx - 22 * u, cy + 4 * u), (cx - 18 * u, cy - 16 * u),
                   (cx + 18 * u, cy - 16 * u), (cx + 22 * u, cy + 4 * u)], fill=(70, 110, 60))
        d.rectangle([cx - 24 * u, cy + 2 * u, cx + 24 * u, cy + 8 * u], fill=(50, 90, 50))
        d.text((cx - 7 * u, cy + 10 * u), "*", font=font(SANS_B, int(18 * u)), fill=(255, 200, 40))
    elif kind == "boat":  # capsized boat + waves
        d.polygon([(cx - 26 * u, cy + 2 * u), (cx + 26 * u, cy + 2 * u),
                   (cx + 16 * u, cy + 14 * u), (cx - 16 * u, cy + 14 * u)], fill=A)
        for wx in (-28, -4, 20):
            d.arc([cx + wx * u, cy + 18 * u, cx + (wx + 12) * u, cy + 28 * u], 180, 360,
                  fill=WH, width=max(2, int(2 * u)))
        d.ellipse([cx - 4 * u, cy - 12 * u, cx + 4 * u, cy - 4 * u], fill=(255, 200, 40))
    elif kind == "oil":  # barrel
        d.rounded_rectangle([cx - 16 * u, cy - 20 * u, cx + 16 * u, cy + 22 * u],
                            radius=int(4 * u), fill=DK)
        d.rectangle([cx - 16 * u, cy - 8 * u, cx + 16 * u, cy - 4 * u], fill=A)
        d.rectangle([cx - 16 * u, cy + 8 * u, cx + 16 * u, cy + 12 * u], fill=A)
        d.text((cx - 8 * u, cy - 22 * u), "OIL", font=font(SANS_B, int(11 * u)), fill=WH)
    elif kind == "gavel":  # gavel
        d.rectangle([cx - 22 * u, cy - 16 * u, cx + 4 * u, cy - 2 * u], fill=A)
        d.line([cx - 4 * u, cy - 9 * u, cx + 22 * u, cy + 16 * u], fill=DK,
               width=max(2, int(4 * u)))
        d.rectangle([cx - 6 * u, cy + 18 * u, cx + 26 * u, cy + 24 * u], fill=(150, 110, 60))
    elif kind == "tv":  # television
        d.rectangle([cx - 24 * u, cy - 16 * u, cx + 24 * u, cy + 14 * u], fill=DK)
        d.rectangle([cx - 19 * u, cy - 11 * u, cx + 19 * u, cy + 9 * u], fill=(120, 200, 240))
        d.line([cx - 12 * u, cy - 22 * u, cx - 4 * u, cy - 16 * u], fill=DK,
               width=max(2, int(2 * u)))
        d.line([cx + 12 * u, cy - 22 * u, cx + 4 * u, cy - 16 * u], fill=DK,
               width=max(2, int(2 * u)))
    elif kind == "ballot":  # ballot box + tick
        d.rectangle([cx - 20 * u, cy - 6 * u, cx + 20 * u, cy + 22 * u], fill=WH)
        d.rectangle([cx - 8 * u, cy - 18 * u, cx + 8 * u, cy - 6 * u], fill=A)
        d.line([cx - 10 * u, cy + 8 * u, cx - 2 * u, cy + 16 * u, cx + 14 * u, cy - 8 * u],
               fill=(40, 160, 60), width=max(2, int(3 * u)))
    elif kind == "bio":  # biohazard trefoil simplified
        for ang in (90, 210, 330):
            a = ang * 3.14159 / 180
            d.ellipse([cx + 14 * u * __import__("math").cos(a) - 8 * u,
                       cy + 14 * u * __import__("math").sin(a) - 8 * u,
                       cx + 14 * u * __import__("math").cos(a) + 8 * u,
                       cy + 14 * u * __import__("math").sin(a) + 8 * u], fill=A)
        d.ellipse([cx - 6 * u, cy - 6 * u, cx + 6 * u, cy + 6 * u], fill=WH)
    elif kind == "chip":  # microchip
        d.rectangle([cx - 16 * u, cy - 16 * u, cx + 16 * u, cy + 16 * u], fill=DK)
        d.rectangle([cx - 8 * u, cy - 8 * u, cx + 8 * u, cy + 8 * u], fill=A)
        for i in range(3):
            for sx in (-1, 1):
                d.line([cx + sx * 22 * u, cy + (i - 1) * 10 * u,
                        cx + sx * 16 * u, cy + (i - 1) * 10 * u], fill=DK,
                       width=max(2, int(2 * u)))
    elif kind == "quake":  # cracked ground + waves
        d.polygon([(cx - 24 * u, cy + 24 * u), (cx - 8 * u, cy + 8 * u),
                   (cx + 2 * u, cy + 18 * u), (cx + 14 * u, cy + 2 * u),
                   (cx + 24 * u, cy + 24 * u)], fill=DK)
        d.arc([cx - 26 * u, cy - 22 * u, cx - 6 * u, cy - 2 * u], 0, 360, fill=A,
              width=max(2, int(2 * u)))
        d.arc([cx + 6 * u, cy - 22 * u, cx + 26 * u, cy - 2 * u], 0, 360, fill=A,
              width=max(2, int(2 * u)))
    elif kind == "gate":  # border gate
        d.rectangle([cx - 26 * u, cy - 20 * u, cx - 20 * u, cy + 24 * u], fill=DK)
        d.rectangle([cx + 20 * u, cy - 20 * u, cx + 26 * u, cy + 24 * u], fill=DK)
        for i in range(4):
            d.line([cx - 20 * u, cy - 16 * u + i * 10 * u, cx + 20 * u,
                    cy - 16 * u + i * 10 * u], fill=A, width=max(2, int(3 * u)))
        d.polygon([(cx - 6 * u, cy - 26 * u), (cx + 6 * u, cy - 26 * u), (cx, cy - 16 * u)],
                  fill=(200, 40, 40))
    elif kind == "game":  # controller
        d.rounded_rectangle([cx - 26 * u, cy - 10 * u, cx + 26 * u, cy + 14 * u],
                            radius=int(8 * u), fill=DK)
        d.line([cx - 16 * u, cy + 2 * u, cx - 8 * u, cy + 2 * u], fill=WH,
               width=max(2, int(3 * u)))
        d.line([cx - 12 * u, cy - 2 * u, cx - 12 * u, cy + 6 * u], fill=WH,
               width=max(2, int(3 * u)))
        for bx, by in ((10, -2), (16, 4)):
            d.ellipse([cx + bx * u - 3 * u, cy + by * u - 3 * u, cx + bx * u + 3 * u,
                       cy + by * u + 3 * u], fill=A)
    elif kind == "power":  # lightning bolt
        d.polygon([(cx + 6 * u, cy - 26 * u), (cx - 12 * u, cy + 2 * u),
                   (cx - 2 * u, cy + 2 * u), (cx - 8 * u, cy + 24 * u),
                   (cx + 12 * u, cy - 4 * u), (cx + 2 * u, cy - 4 * u)], fill=(255, 210, 40))
    elif kind == "mountain":  # mountains + flag
        d.polygon([(cx - 28 * u, cy + 24 * u), (cx - 8 * u, cy - 14 * u),
                   (cx + 8 * u, cy + 24 * u)], fill=(90, 120, 90))
        d.polygon([(cx - 2 * u, cy + 24 * u), (cx + 16 * u, cy - 6 * u),
                   (cx + 30 * u, cy + 24 * u)], fill=(60, 90, 70))
        d.line([cx + 16 * u, cy - 6 * u, cx + 16 * u, cy - 22 * u], fill=DK,
               width=max(2, int(2 * u)))
        d.polygon([(cx + 16 * u, cy - 22 * u), (cx + 26 * u, cy - 18 * u),
                   (cx + 16 * u, cy - 14 * u)], fill=(200, 40, 40))
    else:  # generic: star
        pts = []
        for i in range(10):
            ang = i * 3.14159 / 5 - 3.14159 / 2
            r = 24 * u if i % 2 == 0 else 10 * u
            pts.append((cx + r * __import__("math").cos(ang),
                        cy + r * __import__("math").sin(ang)))
        d.polygon(pts, fill=A)
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)


# ---- story data: (number, headline, deck, source, sky, ground, kind, accent) ----
HEADLINES = [
    (1, "Iran says it struck US bases in Bahrain",
     "Revolutionary Guards say they hit radar at al-Riffa and Awali. Bahrain: a civilian site burned, no injuries.",
     "AL JAZEERA", (30, 50, 90), (60, 45, 40), "missile", (255, 170, 40)),
    (2, "Mexico captures FBI most-wanted cartel boss",
     "Chapo Isidro taken in Guasave, Sinaloa. Gunfights, fires and roadblocks followed; at least 11 dead.",
     "BBC", (20, 70, 60), (70, 60, 40), "cuffs", (255, 200, 40)),
    (3, "Russian missile hits Zelensky's hometown",
     "Kryvyi Rih centre hit: 2 killed, dozens hurt, a boy of 7 among the dead. Missiles also landed in Poland.",
     "AL JAZEERA", (70, 60, 70), (50, 50, 55), "blast", (255, 150, 30)),
]

CARDS = [
    (4, "AI sell-off: S&P 500 and Dow in correction", "BBC", (20, 40, 80), (40, 40, 45), "chartdown", (220, 60, 60)),
    (5, "COP31 talks run past deadline on fossil fuels", "BBC", (15, 90, 80), (90, 70, 40), "globe", (255, 200, 40)),
    (6, "Trump defends Putin ties at Shenzhen summit", "BBC", (90, 30, 30), (60, 60, 70), "summit", (220, 180, 30)),
    (7, "AI-assisted Riemann proof claimed", "GUARDIAN", (40, 40, 90), (70, 60, 90), "math", (255, 220, 90)),
    (8, "UN court: Myanmar guilty of genocide", "PBS", (30, 60, 90), (60, 50, 40), "scales", (255, 200, 40)),
    (9, "Drones hit Russian ship Sparta II off Finland", "BBC", (25, 70, 100), (40, 60, 80), "ship", (255, 150, 30)),
    (10, "Israeli strike kills 3 in Gaza food vehicle", "AL JAZEERA", (100, 60, 40), (70, 55, 40), "truck", (255, 220, 90)),
    (11, "Houthis and Saudi coalition trade strikes", "MID-EAST EYE", (110, 50, 30), (60, 45, 35), "rocket", (255, 150, 30)),
    (12, "UK and EU sign three post-Brexit deals", "GUARDIAN", (25, 60, 110), (50, 60, 90), "shake", (255, 200, 40)),
    (13, "EU-Indonesia trade deal cuts 98.5% of tariffs", "DW", (20, 80, 70), (60, 70, 50), "trade", (220, 180, 30)),
]

BRIEFS = [
    (14, "FBI crime database reportedly hacked", "BBC", "hack"),
    (15, "UN talks to keep working on AI weapons rules", "CBC", "robot"),
    (16, "Denmark expels Russian diplomat over plot", "BBC", "diplomat"),
    (17, "Cost-of-living protests sweep Europe", "FRANCE 24", "protest"),
    (18, "Man guilty of starting Palisades fire", "BBC", "flame"),
    (19, "US child dies of measles in Virginia", "GUARDIAN", "virus"),
    (20, "Wolbachia mosquitoes cut dengue in Brazil", "STRAITS TIMES", "mosquito"),
    (21, "Pill shows hope on pancreatic cancer", "BBC", "pill"),
    (22, "BepiColombo reaches Mercury orbit", "UPI", "planet"),
    (23, "Bolsonaro in intensive care in Brasilia", "AL JAZEERA", "hospital"),
    (24, "Salvadoran troops fight gangs in Haiti", "GUARDIAN", "soldier"),
    (25, "Nigeria boat capsizes: 24 dead", "SKY NEWS", "boat"),
    (26, "Saudi-Japan agree oil stockpile deal", "JAPAN TODAY", "oil"),
    (27, "Brent $91 as Gulf attacks meet glut fears", "OILPRICE", "chartdown"),
    (28, "Argentina bonds fall into distress", "BA TIMES", "gavel"),
    (29, "Man jailed over plot to kill Sikh leader", "BBC", "gavel"),
    (30, "Turkey takes control of Sozcu TV", "RFI", "tv"),
    (31, "Tanzania's Lissu convicted of sedition", "BBC", "ballot"),
    (32, "Uganda curbs gatherings over Ebola", "GUARDIAN", "bio"),
    (33, "Nvidia chief ousted; Trump talked to Xi", "CNBC", "chip"),
    (34, "Fighting widens in eastern Congo", "ASHARQ", "mountain"),
    (35, "GTA VI earns $3.8bn on day one", "BBC", "game"),
    (36, "Basra power station fire kills 4", "REUTERS", "power"),
    (37, "Magnitude 6.7 quake shakes Peru", "UPI", "quake"),
    (38, "Estonia to shut Russia border Dec. 1", "STRAITS TIMES", "gate"),
    (39, "Pakistan forces kill 15 militants in Balochistan", "DAWN", "soldier"),
    (40, "EU proposes tax on Big Tech to fund budget", "THE HINDU", "gavel"),
    (41, "Australia edge England to win first T20", "DAWN", "game"),
    (42, "Illicit alcohol kills 11 in India, 180 in hospital", "DAWN", "hospital"),
    (43, "Kate to feature in film on cancer recovery", "REUTERS", "tv"),
]

BRIEF_BG = [
    (30, 60, 110), (90, 30, 60), (20, 80, 70), (110, 70, 20), (60, 40, 90),
    (100, 40, 40), (20, 90, 90), (70, 60, 110), (30, 80, 40), (110, 50, 80),
    (40, 70, 110), (90, 90, 30), (60, 30, 60), (30, 100, 60), (110, 40, 30),
    (50, 60, 60), (80, 40, 100), (30, 60, 60), (100, 80, 20), (40, 40, 100),
    (90, 60, 30), (20, 70, 100), (70, 90, 40), (100, 30, 70), (50, 80, 90),
    (40, 90, 50), (110, 60, 100), (30, 50, 90), (80, 100, 30), (60, 40, 80),
]

# Numbered map dots (x, y in map panel coords, story no.)
MAP_DOTS = [
    (1, 395, 78), (2, 85, 105), (3, 310, 30), (4, 70, 55), (5, 315, 62),
    (6, 470, 72), (7, 48, 82), (8, 278, 58), (9, 340, 18), (10, 348, 62),
    (11, 372, 88), (12, 272, 30), (13, 490, 108),
]


def badge(d, x, y, text, fnt):
    w = int(d.textlength(text, font=fnt)) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=RED)
    d.text((x + 5, y + 2), text, font=fnt, fill=(255, 255, 255))
    return w


def draw_map(d, x, y, w, h):
    d.rounded_rectangle([x, y, x + w, y + h], radius=5, fill=(198, 224, 240))
    d.rectangle([x, y, x + w, y + h], outline=(60, 60, 60), width=1)
    land = (110, 170, 110)
    # Simplified continents as polygons (equirectangular-ish, schematic).
    polys = [
        [(18, 38), (95, 28), (120, 45), (105, 78), (70, 88), (40, 70), (22, 55)],  # N America
        [(108, 92), (135, 88), (145, 118), (128, 140), (112, 115)],  # S America
        [(268, 28), (330, 22), (355, 48), (330, 78), (292, 72), (272, 50)],  # Europe
        [(268, 82), (300, 80), (315, 105), (300, 128), (275, 110)],  # Africa
        [(360, 20), (470, 15), (520, 40), (500, 80), (440, 88), (390, 70), (362, 45)],  # Asia
        [(500, 108), (535, 105), (540, 125), (512, 128)],  # SE Asia / Oceania
    ]
    sx, sy = w / 560.0, h / 150.0
    for poly in polys:
        pts = [(x + px * sx, y + py * sy) for px, py in poly]
        d.polygon(pts, fill=land, outline=(70, 120, 70))
    d.text((x + 8, y + 4), "WHERE IT HAPPENED  -  1-13 ON THE MAP",
           font=font(SANS_B, 11), fill=INK)
    for n, mx, my in MAP_DOTS:
        px, py = x + mx * sx, y + my * sy
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=RED, outline=(255, 255, 255), width=2)
        t = str(n)
        tw = d.textlength(t, font=font(SANS_B, 11))
        d.text((px - tw / 2, py - 7), t, font=font(SANS_B, 11), fill=(255, 255, 255))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    d.rectangle([0, 0, W, 76], fill=INK)
    d.text((16, 6), "THE WORLD IN ONE PAGE", font=font(SERIF_B, 40), fill=(255, 255, 255))
    d.text((16, 50), "SATURDAY 21 NOVEMBER 2026  -  THE DAY'S WORLD NEWS",
           font=font(SANS_B, 14), fill=(255, 210, 90))
    d.rounded_rectangle([W - 218, 10, W - 14, 34], radius=4, fill=RED)
    d.text((W - 208, 15), "DATE CHECK: 21 NOV 2026", font=font(SANS_B, 13), fill=(255, 255, 255))
    d.text((W - 208, 42), "43 STORIES - ALL ILLUSTRATED", font=font(SANS_B, 12),
           fill=(255, 255, 255))
    # Numbers bar
    d.rectangle([0, 76, W, 102], fill=(232, 222, 200))
    nums = [("700,000", "displaced, S. Ethiopia"), ("$3.8bn", "GTA VI day-one sales"),
            ("6.7", "quake hits Peru"), ("24", "dead, Nigeria boat"),
            ("11", "dead after Mexico arrest")]
    nx = 16
    for val, lab in nums:
        d.text((nx, 80), val, font=font(SERIF_B, 15), fill=RED)
        d.text((nx + d.textlength(val, font=font(SERIF_B, 15)) + 6, 83), lab,
               font=font(SANS, 11), fill=INK)
        nx += int(d.textlength(val, font=font(SERIF_B, 15)) + d.textlength(lab, font=font(SANS, 11)) + 34)
    # Headlines
    colw, gap = 326, 11
    for i, (n, head, deck, src, sky, ground, kind, acc) in enumerate(HEADLINES):
        x = 16 + i * (colw + gap)
        y = 110
        scene(d, x, y, colw, 106, sky, ground, kind, acc)
        d.rounded_rectangle([x, y, x + 22, y + 18], radius=3, fill=RED)
        d.text((x + 6, y + 1), str(n), font=font(SANS_B, 13), fill=(255, 255, 255))
        yy = text_block(d, x, y + 112, head, font(SERIF_B, 17), INK, colw, 20, max_lines=2)
        text_block(d, x, yy + 2, deck, font(SANS, 11), (60, 60, 60), colw, 13, max_lines=2)
        badge(d, x, 287, src, font(SANS_B, 9))
    d.line([0, 300, W, 300], fill=(120, 120, 120), width=1)
    # Map + stats
    draw_map(d, 16, 308, 600, 118)
    sx = 632
    d.rounded_rectangle([sx, 308, 1008, 366], radius=5, fill=(255, 255, 255))
    d.rectangle([sx, 308, 1008, 366], outline=(60, 60, 60), width=1)
    d.text((sx + 8, 312), "REGION STATS  -  STORIES BY REGION", font=font(SANS_B, 11), fill=INK)
    d.text((sx + 8, 330), "Middle East 6    Europe 10    Americas 7", font=font(SANS, 12), fill=INK)
    d.text((sx + 8, 348), "Asia-Pacific 9    Africa 4    Science & Tech 7", font=font(SANS, 12), fill=INK)
    d.rounded_rectangle([sx, 372, 1008, 426], radius=5, fill=(255, 255, 255))
    d.rectangle([sx, 372, 1008, 426], outline=(60, 60, 60), width=1)
    d.text((sx + 8, 376), "UTC TIMELINE  -  21 NOV 2026", font=font(SANS_B, 11), fill=INK)
    d.text((sx + 8, 392), "00:30 GMT Iran claims Bahrain strikes", font=font(SANS, 11), fill=INK)
    d.text((sx + 8, 408), "06:00 GMT Markets fall  -  20:00 GMT GTA VI $3.8bn",
           font=font(SANS, 11), fill=INK)
    # Cards 5x2
    cw, ch, cg = 196, 100, 7
    for i, (n, head, src, sky, ground, kind, acc) in enumerate(CARDS):
        cx = 16 + (i % 5) * (cw + cg)
        cy = 436 + (i // 5) * (ch + 6)
        scene(d, cx, cy, cw, 50, sky, ground, kind, acc)
        d.rounded_rectangle([cx, cy, cx + 18, cy + 14], radius=3, fill=RED)
        d.text((cx + 5, cy), str(n), font=font(SANS_B, 10), fill=(255, 255, 255))
        text_block(d, cx, cy + 54, head, font(SANS_B, 10), INK, cw, 12, max_lines=2)
        badge(d, cx, cy + ch - 15, src, font(SANS_B, 8))
    d.line([0, 642, W, 642], fill=(120, 120, 120), width=1)
    d.text((16, 646), "THE DAY IN BRIEF  -  30 MORE STORIES, EACH WITH ITS OWN PICTURE",
           font=font(SANS_B, 13), fill=INK)
    # Briefs 5x6
    bw, bh = 196, 48
    for i, (n, head, src, kind) in enumerate(BRIEFS):
        bx = 16 + (i % 5) * (bw + cg)
        by = 664 + (i // 5) * (bh + 4)
        sky = BRIEF_BG[i]
        scene(d, bx, by, 30, 30, sky, (40, 40, 45), kind, (255, 200, 40))
        d.rounded_rectangle([bx, by, bx + 14, by + 11], radius=2, fill=RED)
        d.text((bx + 3, by - 1), str(n), font=font(SANS_B, 8), fill=(255, 255, 255))
        text_block(d, bx + 34, by, head, font(SANS_B, 9), INK, bw - 34, 11, max_lines=3)
        d.text((bx + 34, by + 38), src, font=font(SANS_B, 7), fill=RED)
    # Footer
    d.rectangle([0, 984, W, 1024], fill=INK)
    d.text((16, 990), "Sources: Al Jazeera, BBC, Guardian, Reuters, UPI, DW, CBC, France 24 and others - 21 Nov 2026 reports.",
           font=font(SANS, 11), fill=(255, 255, 255))
    d.text((16, 1006), "All pictures drawn for this page, not photographs. 43 stories: 3 headlines + 10 cards + 30 briefs.",
           font=font(SANS, 11), fill=(200, 200, 200))
    return img


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(out, "PNG", optimize=True)
    print(out, img.size)
