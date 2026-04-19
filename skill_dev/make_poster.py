from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from PIL import Image as PILImage
import os

GOLD = colors.HexColor('#F2A900')
DARK_TEXT = colors.HexColor('#1a1a1a')
PAGE_W, PAGE_H = letter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_DIR = os.path.join(BASE_DIR, 'logo')


def make_logo(filename, w, h):
    path = os.path.join(LOGO_DIR, filename)
    if os.path.exists(path):
        return Image(path, width=w, height=h)
    return Spacer(w, h)


def make_poster(output_path, photo_path, title, speaker_name,
                bio_text, abstract_text):

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=0.6*inch,
        rightMargin=0.6*inch,
        topMargin=0,
        bottomMargin=0.5*inch,
    )

    style_seminar = ParagraphStyle(
        'Seminar', fontSize=11, leading=15, alignment=TA_CENTER,
        textColor=DARK_TEXT, fontName='Times-Bold',
    )
    style_title = ParagraphStyle(
        'Title', fontSize=16, leading=21, alignment=TA_CENTER,
        textColor=DARK_TEXT, fontName='Times-Bold',
    )
    style_speaker = ParagraphStyle(
        'Speaker', fontSize=12, leading=16, alignment=TA_CENTER,
        textColor=DARK_TEXT, fontName='Times-Roman',
    )
    style_section = ParagraphStyle(
        'Section', fontSize=13, leading=17, alignment=TA_CENTER,
        textColor=DARK_TEXT, fontName='Times-Bold',
    )
    style_body = ParagraphStyle(
        'Body', fontSize=10.5, leading=15, alignment=TA_JUSTIFY,
        textColor=DARK_TEXT, fontName='Times-Roman', spaceAfter=4,
    )
    style_affil = ParagraphStyle(
        'Affil', fontSize=10, leading=13, alignment=TA_LEFT,
        textColor=DARK_TEXT, fontName='Times-Roman',
    )

    story = []

    # ---- Header ----
    header_content = [
        Paragraph(title, style_title),
        Spacer(1, 4),
        Paragraph(speaker_name, style_speaker),
    ]

    # NSF (left, square) — 396x490 original kept proportional
    logo_h = 0.70 * inch
    nsf_logo  = make_logo('nsf_logo.png', logo_h, logo_h)          # square
    mtu_logo  = make_logo('mtu_logo.png', 0.57*inch, logo_h)       # 396/490 ratio

    left_w  = 0.85 * inch
    right_w = 0.85 * inch
    mid_w   = PAGE_W - 1.2*inch - left_w - right_w

    header_table = Table(
        [[nsf_logo, header_content, mtu_logo]],
        colWidths=[left_w, mid_w, right_w],
    )
    header_table.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), GOLD),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN',         (0, 0),  (0, 0),  'CENTER'),
        ('ALIGN',        (-1, 0), (-1, 0),  'CENTER'),
        ('TOPPADDING',    (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING',   (0, 0),  (0, 0),   8),
        ('RIGHTPADDING', (-1, 0), (-1, 0),   8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.25*inch))

    # ---- Bio ----
    story.append(Paragraph("Bio", style_section))
    story.append(Spacer(1, 6))

    max_photo_w = 1.65 * inch
    if os.path.exists(photo_path):
        pil = PILImage.open(photo_path)
        pw, ph = pil.size
        # Scale to fit max width while preserving original aspect ratio
        photo_w = max_photo_w
        photo_h = photo_w * (ph / pw)
        photo_img = Image(photo_path, width=photo_w, height=photo_h)
    else:
        photo_w, photo_h = max_photo_w, max_photo_w
        photo_img = Spacer(photo_w, photo_h)

    bio_col = [Paragraph(bio_text, style_body)]

    bio_table = Table(
        [[photo_img, bio_col]],
        colWidths=[photo_w + 0.15*inch, PAGE_W - 1.2*inch - photo_w - 0.15*inch],
    )
    bio_table.setStyle(TableStyle([
        ('VALIGN',        (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING',   (0, 0),  (0, 0),   0),
        ('RIGHTPADDING',  (0, 0),  (0, 0),  10),
        ('LEFTPADDING',   (1, 0),  (1, 0),   4),
        ('TOPPADDING',    (0, 0), (-1, -1),  0),
        ('BOTTOMPADDING', (0, 0), (-1, -1),  0),
    ]))
    story.append(bio_table)
    story.append(Spacer(1, 0.2*inch))

    # ---- Abstract ----
    story.append(Paragraph("Abstract", style_section))
    story.append(Spacer(1, 6))
    story.append(Paragraph(abstract_text, style_body))

    doc.build(story)
    print(f"Saved: {output_path}")


# ---- Ronghua Xu data ----
title = (
    "Blockchain Applications in RDMC"
)
speaker_name = "Ronghua Xu, Ph.D."
bio_text = (
    "Dr. Ronghua (Sam) Xu is an Assistant Professor in Applied Computing at Michigan Technological "
    "University and a member of the ICC Center for Cybersecurity. He earned his M.S. (2018) and Ph.D. "
    "(2023) in Electrical and Computer Engineering from Binghamton University. His research focuses on "
    "network security, IoT security, machine learning, edge computing, and multimedia forensics. He "
    "teaches courses in digital forensics, blockchain applications, and Internet of Medical Things. "
    "Prior to his academic career, he worked at Siemens on software development and test automation "
    "(2010&#8211;2016). His work bridges cybersecurity and applied computing, with particular emphasis "
    "on blockchain-enabled trust frameworks, decentralized data management, and security for "
    "cyber-physical systems in construction and engineering contexts."
)
abstract_text = (
    "Blockchain technology offers transformative potential for research and construction data management "
    "(RCDM) by providing decentralized, tamper-resistant ledgers that enhance data provenance, "
    "integrity, and trustworthiness across distributed stakeholders. This talk explores practical "
    "blockchain applications in the construction engineering ecosystem, where data flows across "
    "contractors, owners, regulators, and researchers over long project lifecycles."
    "<br/><br/>"
    "The presentation examines how blockchain-based architectures can address key RCDM challenges "
    "including immutable audit trails for construction records, smart contract-driven access control "
    "for sensitive datasets, and decentralized identity management for multi-party data sharing. "
    "Drawing on experience with Web3 systems and IoT security, the talk discusses design principles "
    "for integrating blockchain into construction data pipelines without sacrificing performance or "
    "usability. Attendees will gain insight into current limitations, emerging standards, and "
    "open research questions at the intersection of blockchain, cybersecurity, and construction "
    "data management."
)

make_poster(
    output_path=os.path.join(BASE_DIR, "Speaker_poster", "rdmce_Ronghua Xu.pdf"),
    photo_path=os.path.join(BASE_DIR, "Speaker_poster", "profile_photo", "ronghua_xu_photo.jpg"),
    title=title,
    speaker_name=speaker_name,
    bio_text=bio_text,
    abstract_text=abstract_text,
)

