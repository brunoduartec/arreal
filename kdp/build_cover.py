#!/usr/bin/env python3
"""Generate the full KDP paperback cover from the approved front artwork."""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "images" / "capa_kdp_refinada.png"
OUTPUT_DIR = ROOT / "output" / "kdp"

PAGE_COUNT = 308
TRIM_W_IN = 5.5
TRIM_H_IN = 8.5
BLEED_IN = 0.125
SPINE_IN = PAGE_COUNT * 0.0025  # KDP black-and-white interior on cream paper.
FULL_W_IN = (2 * TRIM_W_IN) + SPINE_IN + (2 * BLEED_IN)
FULL_H_IN = TRIM_H_IN + (2 * BLEED_IN)
PPI = 300

PNG_OUT = OUTPUT_DIR / "Arreal_Capa_Impressa_55x85_308p.png"
JPG_OUT = OUTPUT_DIR / "Arreal_Capa_Impressa_55x85_308p.jpg"
PDF_OUT = OUTPUT_DIR / "Arreal_Capa_Impressa_55x85_308p.pdf"

ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
ARIAL_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ARIAL_NARROW_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf")
GEORGIA = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")

HOOK_LINES = ("ELE DORMIU CRIANÇA.", "ACORDOU ESTRANHO.")
BLURB = (
    "Depois de cinco anos em coma, um garoto acorda com memórias de um mundo "
    "impossível. Enquanto tenta retomar a vida, pessoas ao seu redor começam a "
    "manifestar habilidades sobrenaturais que nascem de crenças, sentimentos e "
    "traumas profundos - e ele percebe que também mudou.\n\n"
    "Preso entre realidade e fantasia, o Garoto precisa compreender a verdade "
    "sobre o próprio passado antes que o poder humano transforme o futuro em algo "
    "irreconhecível.\n\n"
    "Arreal é uma fantasia psicológica sobre identidade, dor e o poder devastador "
    "das narrativas que contamos a nós mesmos."
)


def font(path: Path, points: float) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), round(points * PPI / 72))


def crop_fill(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def fit_wrapped_lines(
    draw: ImageDraw.ImageDraw,
    paragraph: str,
    chosen_font: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    words = paragraph.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=chosen_font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered_tracking(
    draw: ImageDraw.ImageDraw,
    center_x: float,
    y: float,
    text: str,
    chosen_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    tracking: int,
) -> None:
    widths = [draw.textlength(char, font=chosen_font) for char in text]
    total = sum(widths) + tracking * max(0, len(text) - 1)
    x = center_x - total / 2
    for char, width in zip(text, widths):
        draw.text((x, y), char, font=chosen_font, fill=fill)
        x += width + tracking


def build() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    width = round(FULL_W_IN * PPI)
    height = round(FULL_H_IN * PPI)
    bleed = round(BLEED_IN * PPI)
    back_w = round(TRIM_W_IN * PPI)
    spine_w = round(SPINE_IN * PPI)
    front_x = bleed + back_w + spine_w

    source = Image.open(FRONT).convert("RGB")

    # Create a restrained, continuous background for back cover and spine.
    backdrop_crop = source.crop((0, round(source.height * 0.18), source.width, source.height))
    backdrop = crop_fill(backdrop_crop, width, height).filter(ImageFilter.GaussianBlur(28))
    backdrop = ImageEnhance.Color(backdrop).enhance(0.45)
    backdrop = ImageEnhance.Brightness(backdrop).enhance(0.30)
    cover = Image.blend(Image.new("RGB", (width, height), (5, 13, 24)), backdrop, 0.58)

    # Place the approved front cover across the front trim and outer bleed.
    front_region_w = width - front_x
    front_art = crop_fill(source, front_region_w, height)
    cover.paste(front_art, (front_x, 0))

    draw = ImageDraw.Draw(cover)
    warm = (231, 188, 126)
    ivory = (242, 239, 230)
    muted = (210, 214, 218)

    # Quiet gradient behind back-cover copy for reliable contrast.
    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle((0, 0, bleed + back_w, height), fill=(2, 8, 17, 150))
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(cover)

    safe_left = bleed + round(0.55 * PPI)
    safe_right = bleed + back_w - round(0.55 * PPI)
    text_width = safe_right - safe_left

    hook_font = font(ARIAL_NARROW_BOLD, 15.5)
    body_font = font(GEORGIA, 10.5)
    body_italic = font(GEORGIA, 10.5)

    hook_y = round(0.62 * PPI)
    for hook_line in HOOK_LINES:
        draw_centered_tracking(
            draw,
            (safe_left + safe_right) / 2,
            hook_y,
            hook_line,
            hook_font,
            warm,
            round(0.45 * PPI / 12),
        )
        hook_y += round(0.34 * PPI)
    draw.line(
        (
            safe_left + round(0.4 * PPI),
            round(1.42 * PPI),
            safe_right - round(0.4 * PPI),
            round(1.42 * PPI),
        ),
        fill=warm,
        width=max(2, round(PPI / 150)),
    )

    y = round(1.75 * PPI)
    line_height = round(15.4 * PPI / 72)
    paragraph_gap = round(8 * PPI / 72)
    for paragraph in BLURB.split("\n\n"):
        for line in fit_wrapped_lines(draw, paragraph, body_font, text_width):
            draw.text((safe_left, y), line, font=body_font, fill=ivory)
            y += line_height
        y += paragraph_gap

    # Reserve the lower-right back-cover area for KDP's automatically placed barcode.
    barcode_w = round(2.15 * PPI)
    barcode_h = round(1.35 * PPI)
    barcode_right = bleed + back_w - round(0.25 * PPI)
    barcode_bottom = height - round(0.25 * PPI)
    barcode_box = (
        barcode_right - barcode_w,
        barcode_bottom - barcode_h,
        barcode_right,
        barcode_bottom,
    )
    barcode_overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    barcode_draw = ImageDraw.Draw(barcode_overlay)
    barcode_draw.rounded_rectangle(
        barcode_box,
        radius=round(0.04 * PPI),
        fill=(7, 14, 24, 220),
    )
    cover = Image.alpha_composite(cover.convert("RGBA"), barcode_overlay).convert("RGB")

    # Spine typography, centered and safely inset from fold lines.
    spine_center_x = bleed + back_w + spine_w / 2
    spine_layer = Image.new("RGBA", (height, spine_w), (0, 0, 0, 0))
    spine_draw = ImageDraw.Draw(spine_layer)
    spine_font = font(ARIAL_NARROW_BOLD, 15)
    spine_text = "ARREAL   •   BRUNO DUARTE CORRÊA"
    bbox = spine_draw.textbbox((0, 0), spine_text, font=spine_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    spine_draw.text(
        ((height - tw) / 2, (spine_w - th) / 2 - bbox[1]),
        spine_text,
        font=spine_font,
        fill=warm + (255,),
    )
    rotated = spine_layer.rotate(90, expand=True)
    cover.paste(
        rotated,
        (round(spine_center_x - rotated.width / 2), round((height - rotated.height) / 2)),
        rotated,
    )

    cover.save(PNG_OUT, format="PNG", dpi=(PPI, PPI), optimize=True)
    cover.save(JPG_OUT, format="JPEG", quality=96, subsampling=0, dpi=(PPI, PPI))

    pdf = canvas.Canvas(str(PDF_OUT), pagesize=(FULL_W_IN * 72, FULL_H_IN * 72))
    pdf.setTitle("Arreal - Capa completa KDP")
    pdf.setAuthor("Bruno Duarte Corrêa")
    pdf.drawImage(
        ImageReader(cover),
        0,
        0,
        width=FULL_W_IN * 72,
        height=FULL_H_IN * 72,
        preserveAspectRatio=False,
        mask="auto",
    )
    pdf.showPage()
    pdf.save()

    print(f"Page count: {PAGE_COUNT}")
    print(f"Spine: {SPINE_IN:.3f} in")
    print(f"Full cover: {FULL_W_IN:.3f} x {FULL_H_IN:.3f} in")
    print(PDF_OUT)


if __name__ == "__main__":
    build()
