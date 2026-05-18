# Skill Dev — PDF Generation Tools for Workshop Materials

A collection of Python scripts for generating print-ready PDF materials (event banners and speaker posters) for the NSF RDMCE Workshop. Each sub-project includes a skill markdown file documenting its layout rules and customization points for use with AI-assisted workflows.

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) (recommended) or `pip`

## Project Structure

```
skill_dev/
├── build_banner/               # Vertical event banner generator
│   ├── make_banner.py          # Banner generation script → banner.pdf
│   ├── make_banner_skill.md    # Skill file (layout rules & tuning guide)
│   └── images/
│       ├── nsf.png             # NSF logo
│       ├── mtu.png             # MTU logo
│       ├── mtu-icc.png         # ICC logo
│       ├── MTTI-logo.png       # MTTI logo
│       ├── mtu-mub.jpg         # Venue photo
│       └── demo.jpg            # Reference design
└── build_poster/               # Speaker poster generator
    ├── make_poster.py          # Poster generation script → Speaker_poster/*.pdf
    ├── speaker_poster_skill.md # Skill file (workflow & layout rules)
    └── logo/
        ├── nsf_logo.png        # NSF logo
        └── mtu_logo.png        # MTU logo
```

## build_banner

Generates a **5.5" × 14.0" vertical banner** as `banner.pdf` for the NSF Workshop 2026, matching the `images/demo.jpg` reference design.

### Banner Structure (top → bottom)

| Section | Height | Content |
|---------|--------|---------|
| Logo header | 1.70" | NSF · MTU · ICC · MTTI logos |
| Content area | computed | Year · Title · Subtitle · Tagline · Event details |
| Venue photo | 3.60" | `mtu-mub.jpg`, full width |
| Footer | 0.42" | NSF award acknowledgment |

### Install dependencies

```bash
pip install reportlab Pillow
```

### Run

```bash
cd build_banner
python make_banner.py
# → banner.pdf
```

To preview as PNG (requires PyMuPDF):
```bash
python -c "import fitz; pix=fitz.open('banner.pdf')[0].get_pixmap(matrix=fitz.Matrix(2.5,2.5),alpha=False); pix.save('preview.png')"
```

---

## build_poster

Generates a **letter-size (8.5" × 11") speaker poster** as a PDF for RDMCE Workshop speakers, combining a gold-header title block, speaker bio with photo, and talk abstract.

### Poster Layout

| Section | Content |
|---------|---------|
| Header (gold `#F2A900`) | NSF logo · Talk title + speaker name · MTU logo |
| Bio | Speaker photo (left) + bio paragraph (right) |
| Abstract | Full abstract text, justified |

### Install dependencies

```bash
pip install reportlab Pillow python-docx
```

### Run

Update the data section at the bottom of `make_poster.py` with the speaker's information, then:

```bash
cd build_poster
python make_poster.py
# → Speaker_poster/rdmce_{Author Name}.pdf
```

See `speaker_poster_skill.md` for the full step-by-step workflow (fetching bio, photo, and abstract from source documents).
