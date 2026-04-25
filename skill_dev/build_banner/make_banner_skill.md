# Banner Design Skill — make_banner.py

## Purpose
Generate a high-resolution vertical event banner as a PDF using Python (`reportlab` + `Pillow`).
The reference design is `images/demo.jpg` (NSF Workshop 2026).

---

## Dependencies
```
reportlab >= 4.0
Pillow >= 10.0
```
Install: `pip install reportlab Pillow`

---

## File & Asset Layout
```
banner_design/
├── make_banner.py          # generator script
├── banner.pdf              # output
└── images/
    ├── nsf.png             # NSF logo  (header slot 1)
    ├── mtu.png             # MTU logo  (header slot 2)
    ├── mtu-icc.png         # ICC logo  (header slot 3)
    ├── MTTI-logo.png       # MTTI logo (header slot 4)
    └── mtu-mub.jpg         # MUB photo (bottom section)
```

---

## Banner Structure (top → bottom)

| Section | Height | Notes |
|---|---|---|
| **Logo header** | 1.70" | 4 logo slots, black dividers between them |
| **Content area** | computed | Year · Title · Subtitle · Tagline · Detail rows |
| **Photo** | 3.60" | `mtu-mub.jpg` stretched full width, gold cap on top |
| **Footer** | 0.42" | Black bg, white text, gold rule on top |

Overall size: **5.5" × 14.0"** (portrait)

---

## Key Constants (easy to tune)

### Global dimensions
```python
W        = 5.5  * inch   # banner width
H        = 14.0 * inch   # banner height
FOOTER_H = 0.42 * inch
PHOTO_H  = 3.60 * inch   # reduce to give more content space
LOGO_H   = 1.70 * inch
```

### Brand colours
```python
GOLD  = HexColor('#F0B11D')   # MTU gold
BLACK = HexColor('#1A1A1A')
DGRAY = HexColor('#4A4A4A')   # sub-label / tagline
```

### Logo strip
```python
pad    = 0.03 * inch   # horizontal padding per slot side (minimal)
h_frac = 0.88          # max logo height as fraction of LOGO_H (same for all)
```
All four logos are **width-bound** (≈ 2 : 1 aspect ratio in a near-square slot).
Reducing `pad` is the only lever to enlarge logos.
Divider lines are auto-sized to match the tallest logo's rendered height.

### Content area — vertical distribution
Three **equal gaps** (PAD) separate:
1. Top of content → "2026" baseline
2. Tagline bottom → first detail row
3. Last URL row → photo top

```python
PAD = max((CONT_H - TITLE_H - DETAIL_H) / 3, 0.30 * inch)
```

### Typography
| Element | Font | Size |
|---|---|---|
| Year "2026" | Helvetica-Bold | 62 pt |
| Title "NSF Workshop" | Helvetica-Bold | 47 pt |
| Subtitle (2 lines) | Helvetica-Bold | 25 pt |
| Tagline | Helvetica-Oblique | 19 pt |
| Detail rows (time / location / venue) | Helvetica-Bold | 16 pt |
| URL | Helvetica-Bold | 16 pt |
| Footer | Helvetica | 10 pt |

### Detail rows — layout
```python
LM        = 0.40 * inch   # unified left margin for all content
ICON_SIZE = 0.50 * inch   # icon diameter
ICON_GAP  = 0.14 * inch   # gap between icon right edge and text
ICON_X    = LM + ICON_SIZE / 2
TEXT_X    = LM + ICON_SIZE + ICON_GAP
LINE_H_1  = 0.96 * inch   # single-line row height
LINE_H_2  = 1.20 * inch   # two-line row height (location)
```

**Vertical centering in each row:**
- Icon: centred on `row_center = y_top - row_h / 2`
- Single-line text: baseline = `row_center + DETAIL_SIZE * 0.35`
- Two-line text: baselines placed symmetrically ± `DETAIL_SIZE * 1.35 / 2` around `row_center`

**Gold vertical accent bar**: positioned at `LM - 0.22 * inch`, spans only the three detail rows (date / location / venue), not the URL row.

---

## "2026" Row — Gold Flanking Lines
Same style as the URL row: two gold bars flank the centred "2026" text.
Outer edges of both bars are **flush with the "NSF Workshop" text edges** (auto-computed).

```python
line_y = y + YEAR_SZ * 0.35          # mid cap-height
gap    = 8                            # pts gap from text
c.rect(title_x, line_y, year_x - title_x - gap, 3.5, ...)
c.rect(year_x + year_w + gap, line_y, title_right - (year_x + year_w + gap), 3.5, ...)
```

---

## URL Row — Globe + Text Group
Globe icon and URL text are centred **together** as a single group at `CX`.
Gold rules flank the full group left and right.

```python
GLOB_GAP   = 0.14 * inch             # globe → text gap
group_w    = ICON_SIZE + GLOB_GAP + url_w
group_left = CX - group_w / 2
```

---

## Draw Order (back to front)
```python
draw_footer(c)      # black strip at bottom
draw_photo(c)       # MUB photo above footer
draw_content(c)     # white content area
draw_logo_strip(c)  # logo header on top
```

---

## Running
```bash
cd banner_design
python make_banner.py
# → banner.pdf
```

To preview without overwriting a locked PDF:
```bash
python -c "import make_banner, os; make_banner.OUT='banner_new.pdf'; make_banner.main()"
```

To render a PNG preview (requires PyMuPDF):
```bash
python -c "import fitz; pix=fitz.open('banner.pdf')[0].get_pixmap(matrix=fitz.Matrix(2.5,2.5),alpha=False); pix.save('preview.png')"
```
