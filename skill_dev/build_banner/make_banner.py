#!/usr/bin/env python3
"""Generate NSF Workshop 2026 banner as banner.pdf, matching demo.jpg design."""

import os
from reportlab.lib.pagesizes import inch
from reportlab.lib.colors import HexColor, white
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE = os.path.join(os.path.dirname(__file__), 'images')
OUT  = os.path.join(os.path.dirname(__file__), 'banner.pdf')

# ── Dimensions ─────────────────────────────────────────────────────────────────
W = 5.5 * inch
H = 14.0 * inch

# ── Brand colours ──────────────────────────────────────────────────────────────
GOLD   = HexColor('#F0B11D')
BLACK  = HexColor('#1A1A1A')
DGRAY  = HexColor('#4A4A4A')
LGRAY  = HexColor('#F0F0F0')

# ── Section heights ────────────────────────────────────────────────────────────
FOOTER_H = 0.42 * inch
PHOTO_H  = 3.60 * inch
LOGO_H   = 1.70 * inch
RULE_PX  = 3            # gold rule under logo strip (pts)

# Derived Y positions (reportlab: Y=0 at bottom)
Y_PHOTO_BOT = FOOTER_H
Y_PHOTO_TOP = FOOTER_H + PHOTO_H
Y_LOGO_BOT  = H - LOGO_H
Y_LOGO_TOP  = H
Y_CONT_BOT  = Y_PHOTO_TOP
Y_CONT_TOP  = Y_LOGO_BOT
CX = W / 2


# ── Drawing helpers ─────────────────────────────────────────────────────────────

def load_img(fname):
    return ImageReader(os.path.join(BASE, fname))

def logo_draw_size(fname, max_h, max_w):
    """Return (w, h) respecting aspect ratio within max_h / max_w."""
    pil = Image.open(os.path.join(BASE, fname))
    iw, ih = pil.size
    ratio = iw / ih
    w = min(max_h * ratio, max_w)
    h = w / ratio
    return w, h


def draw_icon_calendar(c, cx, cy, size):
    """Simple calendar icon."""
    s = size
    c.setFillColor(GOLD)
    c.roundRect(cx - s/2, cy - s*0.45, s, s*0.9, s*0.1, fill=1, stroke=0)
    c.setFillColor(white)
    # header bar
    c.rect(cx - s/2, cy + s*0.18, s, s*0.27, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(cx - s/2, cy + s*0.18, s, s*0.04, fill=1, stroke=0)
    # grid dots
    for col in [-0.25, 0, 0.25]:
        for row in [-0.05, -0.22]:
            c.setFillColor(white)
            c.circle(cx + col*s, cy + row*s, s*0.07, fill=1, stroke=0)


def draw_icon_pin(c, cx, cy, size):
    """Simple location-pin icon."""
    s = size
    c.setFillColor(GOLD)
    # circle top
    c.circle(cx, cy + s*0.15, s*0.38, fill=1, stroke=0)
    # triangle tail
    from reportlab.graphics.shapes import Path
    p = c.beginPath()
    p.moveTo(cx - s*0.18, cy + s*0.05)
    p.lineTo(cx + s*0.18, cy + s*0.05)
    p.lineTo(cx,           cy - s*0.5)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # inner white circle
    c.setFillColor(white)
    c.circle(cx, cy + s*0.15, s*0.16, fill=1, stroke=0)


def draw_icon_building(c, cx, cy, size):
    """Simple building / temple icon."""
    s = size
    c.setFillColor(GOLD)
    # roof bar
    c.rect(cx - s*0.48, cy + s*0.30, s*0.96, s*0.12, fill=1, stroke=0)
    # top cap
    c.rect(cx - s*0.38, cy + s*0.42, s*0.76, s*0.10, fill=1, stroke=0)
    # columns
    for xo in [-0.30, -0.10, 0.10, 0.30]:
        c.rect(cx + xo*s - s*0.055, cy - s*0.35, s*0.11, s*0.65, fill=1, stroke=0)
    # base
    c.rect(cx - s*0.50, cy - s*0.47, s, s*0.12, fill=1, stroke=0)


def draw_icon_globe(c, cx, cy, size):
    """Simple globe icon."""
    s = size
    c.setFillColor(GOLD)
    c.setLineWidth(s * 0.10)
    c.setStrokeColor(GOLD)
    c.circle(cx, cy, s*0.44, fill=0, stroke=1)
    c.setLineWidth(s * 0.07)
    # vertical ellipse (longitude)
    c.ellipse(cx - s*0.15, cy - s*0.44, cx + s*0.15, cy + s*0.44, fill=0, stroke=1)
    # horizontal line (equator)
    c.line(cx - s*0.44, cy, cx + s*0.44, cy)
    c.setLineWidth(1)


# ── Section renderers ──────────────────────────────────────────────────────────

def draw_footer(c):
    c.setFillColor(BLACK)
    c.rect(0, 0, W, FOOTER_H, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(0, FOOTER_H - RULE_PX, W, RULE_PX, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont('Helvetica', 10)
    c.drawCentredString(CX, FOOTER_H / 2 - 4,
                        'Supported by NSF CI PAOS Program  |  Award No. 2541825')


def draw_photo(c):
    img = load_img('mtu-mub.jpg')
    c.drawImage(img, 0, Y_PHOTO_BOT, W, PHOTO_H,
                preserveAspectRatio=False, anchor='c')
    # subtle dark gradient overlay at top of photo so text above reads cleanly
    # thin gold cap at top of photo
    c.setFillColor(GOLD)
    c.rect(0, Y_PHOTO_TOP - RULE_PX, W, RULE_PX, fill=1, stroke=0)


def draw_logo_strip(c):
    # White background
    c.setFillColor(white)
    c.rect(0, Y_LOGO_BOT, W, LOGO_H, fill=1, stroke=0)

    # Logo definitions: (filename, max_h_fraction_of_LOGO_H)
    logos = [
        ('nsf.png',       0.88),
        ('mtu.png',       0.88),
        ('mtu-icc.png',   0.88),
        ('MTTI-logo.png', 0.88),
    ]

    n = len(logos)
    slot_w = W / n
    pad = 0.03 * inch

    for i, (fname, h_frac) in enumerate(logos):
        max_h = LOGO_H * h_frac
        max_w = slot_w - 2 * pad
        lw, lh = logo_draw_size(fname, max_h, max_w)
        x = i * slot_w + (slot_w - lw) / 2
        y = Y_LOGO_BOT + RULE_PX + (LOGO_H - RULE_PX - lh) / 2
        c.drawImage(load_img(fname), x, y, lw, lh,
                    preserveAspectRatio=True, mask='auto')



def draw_content(c):
    # White background
    c.setFillColor(white)
    c.rect(0, Y_CONT_BOT, W, Y_CONT_TOP - Y_CONT_BOT, fill=1, stroke=0)

    LM          = 0.40 * inch
    ICON_SIZE   = 0.50 * inch
    ICON_GAP    = 0.14 * inch          # space between icon right edge and text
    ICON_X      = LM + ICON_SIZE / 2
    TEXT_X      = LM + ICON_SIZE + ICON_GAP
    LINE_H_1    = 0.75 * inch
    LINE_H_2    = 1.00 * inch
    DETAIL_FONT = 'Helvetica-Bold'
    DETAIL_SIZE = 16
    URL_ROW_H   = 0.78 * inch

    # ── Even vertical distribution ─────────────────────────────────────────────
    SEP_ABOVE   = 0.25 * inch                             # gap from 2026 baseline to separator
    SEP_BELOW   = 0.72 * inch                             # gap from separator to NSF Workshop baseline (0.72-0.47cap≈0.25 visual gap, matching above)
    # Height of title block (sum of internal y-steps + tagline cap height)
    TITLE_STEPS = (SEP_ABOVE + SEP_BELOW + 0.68 + 0.38 + 0.36) * inch
    TITLE_H     = TITLE_STEPS + (19 / 72) * inch
    # Height of detail block
    DETAIL_H    = LINE_H_1 + LINE_H_2 + LINE_H_1 + URL_ROW_H
    # Fixed gap below logo strip, then three equal pads between content blocks
    HEADER_GAP = 0.45 * inch
    CONT_H = Y_CONT_TOP - Y_CONT_BOT
    PAD    = max((CONT_H - HEADER_GAP - TITLE_H - DETAIL_H) / 3, 0.30 * inch)

    # ── Year — with flanking gold rules aligned to NSF Workshop text edges ────
    YEAR_SZ  = 62
    TITLE_SZ = 47
    y = Y_CONT_TOP - HEADER_GAP - PAD

    # Pre-compute bounds of both texts for alignment
    year_w  = c.stringWidth('2026',         'Helvetica-Bold', YEAR_SZ)
    title_w = c.stringWidth('NSF Workshop', 'Helvetica-Bold', TITLE_SZ)
    year_x  = CX - year_w  / 2
    title_x = CX - title_w / 2

    # Gold lines: outer edges flush with NSF Workshop, inner edges gap from 2026
    line_y = y + YEAR_SZ * 0.35          # mid cap-height of 2026
    gap    = 8
    c.setFillColor(GOLD)
    c.rect(title_x,                   line_y, year_x - title_x - gap,                          3.5, fill=1, stroke=0)
    c.rect(year_x + year_w + gap,     line_y, (title_x + title_w) - (year_x + year_w + gap),   3.5, fill=1, stroke=0)

    # Draw 2026 text on top of lines
    c.setFillColor(GOLD)
    c.setFont('Helvetica-Bold', YEAR_SZ)
    c.drawCentredString(CX, y, '2026')

    # ── Gold separator between 2026 and NSF Workshop (35% of banner width) ───
    sep_w = W * 0.35
    sep_y = y - SEP_ABOVE
    c.setFillColor(GOLD)
    c.rect(CX - sep_w / 2, sep_y, sep_w, 3.5, fill=1, stroke=0)

    # ── Title ─────────────────────────────────────────────────────────────────
    c.setFillColor(BLACK)
    c.setFont('Helvetica-Bold', TITLE_SZ)
    y -= SEP_ABOVE + SEP_BELOW
    c.drawCentredString(CX, y, 'NSF Workshop')

    # ── Subtitle ──────────────────────────────────────────────────────────────
    y -= 0.68 * inch   # absorbs the old 0.22 rule gap + 0.46 subtitle gap
    c.setFillColor(BLACK)
    c.setFont('Helvetica-Bold', 25)
    c.drawCentredString(CX, y, 'Research Data Management')
    y -= 0.38 * inch
    c.drawCentredString(CX, y, 'in Construction Engineering')

    # ── Tagline ───────────────────────────────────────────────────────────────
    y -= 0.36 * inch
    c.setFillColor(DGRAY)
    c.setFont('Helvetica-Oblique', 19)
    c.drawCentredString(CX, y, 'Challenges and Opportunities')

    # ── Gap between title section and detail section ─────────────────────────
    y -= PAD + 0.22 * inch

    def detail_row(y_top, draw_icon_fn, bold_line, plain_line=None):
        row_h      = LINE_H_2 if plain_line else LINE_H_1
        row_center = y_top - row_h / 2          # vertical midpoint of the row
        cap_half   = DETAIL_SIZE * 0.35         # half cap-height in pts

        # Icon centred on row midpoint
        draw_icon_fn(c, ICON_X, row_center, ICON_SIZE)

        c.setFillColor(BLACK)
        c.setFont(DETAIL_FONT, DETAIL_SIZE)
        if plain_line:
            # Two lines: space them symmetrically around row_center
            line_gap  = DETAIL_SIZE * 1.35      # baseline-to-baseline spacing (pts)
            bold_y    = row_center + line_gap / 2
            plain_y   = row_center - line_gap / 2
            c.drawString(TEXT_X, bold_y, bold_line)
            c.setFillColor(DGRAY)
            c.setFont(DETAIL_FONT, DETAIL_SIZE)
            c.drawString(TEXT_X, plain_y, plain_line)
        else:
            # Single line: baseline at row_center + half cap-height
            c.drawString(TEXT_X, row_center + cap_half, bold_line)
        return y_top - row_h

    y_detail_top = y
    y = detail_row(y, draw_icon_calendar, 'May 07–08, 2026')
    y = detail_row(y, draw_icon_pin,
                   'Michigan Technological University',
                   'Houghton, Michigan')
    y = detail_row(y, draw_icon_building, 'Memorial Union Building (MUB)')
    y_detail_bot = y

    # Vertical gold bar — spans only the three detail rows
    c.setFillColor(GOLD)
    c.rect(LM - 0.22 * inch, y_detail_bot, 2.5, y_detail_top - y_detail_bot, fill=1, stroke=0)

    # ── URL row ───────────────────────────────────────────────────────────────
    y -= 0.42 * inch
    url_cy   = y - URL_ROW_H / 2
    url_text = 'rdmce.icc.mtu.edu'
    c.setFont(DETAIL_FONT, DETAIL_SIZE)
    url_w    = c.stringWidth(url_text, DETAIL_FONT, DETAIL_SIZE)

    # Centre the [globe  gap  text] group at CX
    GLOB_GAP    = 0.14 * inch          # space between globe and text
    group_w     = ICON_SIZE + GLOB_GAP + url_w
    group_left  = CX - group_w / 2
    globe_cx    = group_left + ICON_SIZE / 2
    url_x       = group_left + ICON_SIZE + GLOB_GAP

    draw_icon_globe(c, globe_cx, url_cy + 0.03 * inch, ICON_SIZE)

    # Gold rules flanking the group
    line_y  = url_cy + 0.07 * inch
    line_h  = 2
    margin  = 0.30 * inch
    c.setFillColor(GOLD)
    c.rect(LM, line_y, group_left - LM - 8, line_h, fill=1, stroke=0)
    c.rect(group_left + group_w + 8, line_y, W - margin - (group_left + group_w + 8), line_h, fill=1, stroke=0)

    c.setFillColor(BLACK)
    c.drawString(url_x, url_cy, url_text)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    c = canvas.Canvas(OUT, pagesize=(W, H))
    # Draw back-to-front
    draw_footer(c)
    draw_photo(c)
    draw_content(c)
    draw_logo_strip(c)
    c.save()
    print(f'Banner saved: {OUT}')


if __name__ == '__main__':
    main()
