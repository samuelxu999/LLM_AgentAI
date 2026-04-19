# Skill: Generate RDMC Workshop Speaker Poster

Generate a one-page PDF speaker poster in research workshop, following the established template and rules below.

---

## Folder Structure

```
speaker_design/
├── Abstract/          # Source files: talk title + abstract text only
├── logo/
│   ├── nsf_logo.png   # NSF logo (left corner of header)
│   └── mtu_logo.png   # Michigan Tech logo (right corner of header)
├── Speaker_poster/    # Output folder for generated posters
│   └── rdmce_{Author Name}.pdf
├── make_poster.py     # Poster generation script
└── skill.md           # Skill file to support poster generation task.
```

---

## Step-by-Step Workflow

### 1. Read the abstract file
- Open the speaker's `.docx` file from the `Speaker_Abstract/` folder.
- Extract **Title** and **Abstract** text only.
- Do **not** use any bio or affiliation text from this file.

### 2. Fetch speaker photo
- Extract **Website** from speaker's `.docx` file to search for official faculty/personal webpage.
- Download their headshot/profile photo and save it to `Speaker_poster/profile_photo/{author_name}_photo.jpg`.

### 3. Fetch speaker bio
- Fetch the speaker's official faculty/personal webpage.
- Extract an accurate, current bio paragraph (position, lab, research focus, publications, awards, memberships).
- Do **not** use bio text from the Abstract folder file.

### 4. Generate the poster via `make_poster.py`
Update the data section at the bottom of `make_poster.py` with the new speaker's information, then run:
```bash
python make_poster.py
```

---

## Poster Layout Rules

### Header (gold background `#F2A900`)
- **Left corner**: `logo/nsf_logo.png`
- **Center**: Talk title (bold, 16pt Times) + Speaker name (12pt Times)
- **Right corner**: `logo/mtu_logo.png`
- No "Civil Engineering Seminar" label — title only.

### Bio Section
- Section heading: **Bio** (bold, centered)
- Speaker photo on the left, scaled to max width 1.65 in, preserving original aspect ratio — no stretching or cropping.
- Bio paragraph text on the right (justified, 10.5pt Times).
- No affiliation/title lines below the bio text.

### Abstract Section
- Section heading: **Abstract** (bold, centered)
- Full abstract text (justified, 10.5pt Times).
- Separate paragraphs with `<br/><br/>` tags in the text string.

---

## Output

- Save poster to: `Speaker_poster/rdmce_{Author Name}.pdf`
  - Example: `Speaker_poster/rdmce_Samuel Xu.pdf`

---

## Key Rules Summary

| Rule | Detail |
|------|--------|
| Bio source | Official website only — never Abstract folder |
| Photo display | Original aspect ratio, max width 1.65 in, no crop/stretch |
| Affiliation lines | Not shown (removed from layout) |
| Header label | Talk title + speaker name only (no "Civil Engineering Seminar") |
| Logos | NSF left, Michigan Tech right, loaded from `logo/` folder |
| Output filename | `rdmce_{Author Name}.pdf` in `Speaker_poster/` folder |

---

## Dependencies

```bash
pip install reportlab Pillow python-docx
```

---

## `make_poster()` Function Signature

```python
make_poster(
    output_path,    # full path to output PDF
    photo_path,     # full path to speaker photo
    title,          # talk title string
    speaker_name,   # e.g. "Ronghua Xu, Ph.D."
    bio_text,       # bio paragraph (HTML entities OK, use <br/> for breaks)
    abstract_text,  # abstract text (use <br/><br/> between paragraphs)
)
```
