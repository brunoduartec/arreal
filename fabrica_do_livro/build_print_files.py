#!/usr/bin/env python3
"""Build press-ready Arreal files for Fabrica do Livro's 14 x 21 cm format."""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageCms, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
TMP_DIR = ROOT / "tmp" / "pdfs" / "fabrica_do_livro"

SOURCE_INTERIOR = ROOT / "output" / "kdp" / "Arreal_Miolo_Impresso_55x85_310p.pdf"
SOURCE_ART = ROOT / "images" / "capa_kdp_sem_texto_v2.png"
SOURCE_BARCODE = ROOT / "output" / "kdp" / "Arreal_ISBN_978-65-02-27657-0_EAN13.png"

INTERIOR_OUT = OUTPUT_DIR / "Arreal_Miolo_FabricaDoLivro_14x21_310p.pdf"
COVER_OUT = OUTPUT_DIR / "Arreal_Capa_FabricaDoLivro_14x21_310p_Polen80.pdf"
COVER_PNG_OUT = TMP_DIR / "Arreal_Capa_FabricaDoLivro_14x21_310p_Polen80.png"
COVER_CMYK_JPG = TMP_DIR / "Arreal_Capa_FabricaDoLivro_14x21_310p_Polen80_CMYK.jpg"

PAGE_COUNT = 310
TRIM_W_MM = 140.0
TRIM_H_MM = 210.0
BLEED_MM = 2.5
SPINE_MM = 16.74
INTERIOR_W_MM = TRIM_W_MM + 2 * BLEED_MM
INTERIOR_H_MM = TRIM_H_MM + 2 * BLEED_MM
COVER_W_MM = 2 * TRIM_W_MM + SPINE_MM + 2 * BLEED_MM
COVER_H_MM = TRIM_H_MM + 2 * BLEED_MM
PPI = 300

MM_TO_PT = 72 / 25.4

ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
ARIAL_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ARIAL_NARROW_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf")
GEORGIA = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")
SRGB_PROFILE = Path("/System/Library/ColorSync/Profiles/sRGB Profile.icc")
CMYK_PROFILE = Path("/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc")

HOOK_LINES = ("ELE DORMIU CRIANÇA.", "ACORDOU ESTRANHO.")
BLURB = (
    "Depois de cinco anos em coma, um garoto acorda com memórias de um mundo "
    "que não deveria existir. Enquanto tenta retomar a vida, descobre que "
    "crenças, sentimentos e traumas podem se transformar em habilidades "
    "sobrenaturais.\n\n"
    "Em Arreal, o risco não está apenas em ganhar poder, mas em decidir o que "
    "fazer com ele. Quando essa descoberta começa a se espalhar, o que era "
    "segredo vira disputa, e cada escolha cobra um preço.\n\n"
    "Arreal é uma fantasia urbana brasileira sobre poder, identidade e "
    "responsabilidade. Uma história sobre pessoas comuns diante do extraordinário "
    "e sobre o que acontece quando o impossível deixa de ser exceção."
)


def mm_to_px(value: float) -> int:
    return round(value / 25.4 * PPI)


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
    lines: list[str] = []
    current = ""
    for word in paragraph.split():
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
) -> tuple[float, float, float, float]:
    widths = [draw.textlength(char, font=chosen_font) for char in text]
    total = sum(widths) + tracking * max(0, len(text) - 1)
    x = center_x - total / 2
    bounds: list[tuple[float, float, float, float]] = []
    for char, width in zip(text, widths):
        bounds.append(draw.textbbox((x, y), char, font=chosen_font))
        draw.text((x, y), char, font=chosen_font, fill=fill)
        x += width + tracking
    return (
        min(box[0] for box in bounds),
        min(box[1] for box in bounds),
        max(box[2] for box in bounds),
        max(box[3] for box in bounds),
    )


def assert_inside(
    label: str,
    bounds: tuple[float, float, float, float],
    safe_box: tuple[float, float, float, float],
) -> None:
    left, top, right, bottom = bounds
    safe_left, safe_top, safe_right, safe_bottom = safe_box
    if left < safe_left or top < safe_top or right > safe_right or bottom > safe_bottom:
        raise ValueError(f"{label} fora da zona segura: {bounds}; zona: {safe_box}")


def build_interior() -> None:
    reader = PdfReader(SOURCE_INTERIOR)
    if len(reader.pages) != PAGE_COUNT:
        raise ValueError(f"Miolo deveria ter {PAGE_COUNT} páginas; tem {len(reader.pages)}")

    target_w = INTERIOR_W_MM * MM_TO_PT
    target_h = INTERIOR_H_MM * MM_TO_PT
    trim_w = TRIM_W_MM * MM_TO_PT
    trim_h = TRIM_H_MM * MM_TO_PT
    bleed = BLEED_MM * MM_TO_PT

    writer = PdfWriter()
    for page in reader.pages:
        source_w = float(page.mediabox.width)
        source_h = float(page.mediabox.height)
        scale = min(trim_w / source_w, trim_h / source_h)
        placed_w = source_w * scale
        placed_h = source_h * scale
        tx = bleed + (trim_w - placed_w) / 2
        ty = bleed + (trim_h - placed_h) / 2

        output_page = writer.add_blank_page(width=target_w, height=target_h)
        transform = Transformation((scale, 0, 0, scale, tx, ty))
        output_page.merge_transformed_page(page, transform, over=True)

    writer.add_metadata(
        {
            "/Title": "Arreal - Miolo 14x21 cm - Fabrica do Livro",
            "/Author": "Bruno Duarte Corrêa",
            "/Subject": "Miolo preto e branco, 310 páginas, formato 14x21 cm",
        }
    )
    with INTERIOR_OUT.open("wb") as stream:
        writer.write(stream)


def build_cover() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    width = mm_to_px(COVER_W_MM)
    height = mm_to_px(COVER_H_MM)
    bleed_left = mm_to_px(BLEED_MM)
    back_end = mm_to_px(BLEED_MM + TRIM_W_MM)
    spine_end = mm_to_px(BLEED_MM + TRIM_W_MM + SPINE_MM)
    front_end = mm_to_px(BLEED_MM + TRIM_W_MM + SPINE_MM + TRIM_W_MM)

    source = Image.open(SOURCE_ART).convert("RGB")
    backdrop_crop = source.crop((0, round(source.height * 0.18), source.width, source.height))
    backdrop = crop_fill(backdrop_crop, width, height).filter(ImageFilter.GaussianBlur(28))
    backdrop = ImageEnhance.Color(backdrop).enhance(0.45)
    backdrop = ImageEnhance.Brightness(backdrop).enhance(0.30)
    cover = Image.blend(Image.new("RGB", (width, height), (5, 13, 24)), backdrop, 0.58)

    front_art = crop_fill(source, width - spine_end, height)
    cover.paste(front_art, (spine_end, 0))

    overlay = Image.new("RGBA", cover.size, (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rectangle((0, 0, back_end, height), fill=(2, 8, 17, 150))
    cover = Image.alpha_composite(cover.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(cover)

    warm = (231, 188, 126)
    ivory = (242, 239, 230)

    # Existing design already uses margins wider than the printer's 5 mm safe area.
    back_safe_outer = bleed_left + mm_to_px(14)
    back_safe_spine = back_end - mm_to_px(14)
    text_width = back_safe_spine - back_safe_outer

    hook_font = font(ARIAL_NARROW_BOLD, 15.5)
    body_font = font(GEORGIA, 10.5)
    hook_y = mm_to_px(15.5)
    for hook_line in HOOK_LINES:
        draw_centered_tracking(
            draw,
            (back_safe_outer + back_safe_spine) / 2,
            hook_y,
            hook_line,
            hook_font,
            warm,
            round(0.45 * PPI / 12),
        )
        hook_y += mm_to_px(8.5)
    draw.line(
        (back_safe_outer + mm_to_px(10), mm_to_px(36), back_safe_spine - mm_to_px(10), mm_to_px(36)),
        fill=warm,
        width=max(2, round(PPI / 150)),
    )

    y = mm_to_px(43)
    line_height = round(15.4 * PPI / 72)
    paragraph_gap = round(8 * PPI / 72)
    for paragraph in BLURB.split("\n\n"):
        for line in fit_wrapped_lines(draw, paragraph, body_font, text_width):
            draw.text((back_safe_outer, y), line, font=body_font, fill=ivory)
            y += line_height
        y += paragraph_gap

    front_trim_left = spine_end
    front_trim_right = front_end
    front_trim_top = bleed_left
    front_trim_bottom = height - mm_to_px(BLEED_MM)
    safe_inset = mm_to_px(12.7)
    front_safe = (
        front_trim_left + safe_inset,
        front_trim_top + safe_inset,
        front_trim_right - safe_inset,
        front_trim_bottom - safe_inset,
    )
    front_center_x = (front_trim_left + front_trim_right) / 2

    title_font = font(ARIAL_NARROW_BOLD, 88)
    title_tracking = round(0.06 * PPI)
    title_reference = draw.textbbox((0, 0), "ARREAL", font=title_font)
    title_y = front_safe[1] - title_reference[1]
    title_bounds = draw_centered_tracking(
        draw, front_center_x, title_y, "ARREAL", title_font, warm, title_tracking
    )
    assert_inside("Título", title_bounds, front_safe)

    author_font = font(ARIAL, 15)
    author_tracking = round(0.045 * PPI)
    author = "BRUNO DUARTE CORRÊA"
    author_reference = draw.textbbox((0, 0), author, font=author_font)
    author_y = front_safe[3] - author_reference[3]
    author_bounds = draw_centered_tracking(
        draw, front_center_x, author_y, author, author_font, warm, author_tracking
    )
    assert_inside("Autor", author_bounds, front_safe)

    barcode = Image.open(SOURCE_BARCODE).convert("RGB")
    barcode_w = mm_to_px(54.6)
    barcode_h = mm_to_px(34.3)
    barcode = barcode.resize((barcode_w, barcode_h), Image.Resampling.LANCZOS)
    barcode_right = back_end - mm_to_px(6.4)
    barcode_bottom = height - mm_to_px(6.4)
    cover.paste(barcode, (barcode_right - barcode_w, barcode_bottom - barcode_h))

    spine_center_x = (back_end + spine_end) / 2
    spine_w = spine_end - back_end
    spine_layer = Image.new("RGBA", (height, spine_w), (0, 0, 0, 0))
    spine_draw = ImageDraw.Draw(spine_layer)
    spine_font = font(ARIAL_NARROW_BOLD, 13.5)
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

    cover.save(COVER_PNG_OUT, format="PNG", dpi=(PPI, PPI), optimize=True)
    # Use ColorSync's CMYK profile instead of Pillow's naive conversion. The
    # latter leaves K at zero and lifts dark blue-black areas to gray in print.
    cmyk_cover = ImageCms.profileToProfile(
        cover,
        str(SRGB_PROFILE),
        str(CMYK_PROFILE),
        outputMode="CMYK",
        renderingIntent=0,
    )
    cmyk_cover.save(
        COVER_CMYK_JPG,
        format="JPEG",
        quality=96,
        subsampling=0,
        dpi=(PPI, PPI),
        icc_profile=CMYK_PROFILE.read_bytes(),
    )

    pdf = canvas.Canvas(
        str(COVER_OUT),
        pagesize=(COVER_W_MM * MM_TO_PT, COVER_H_MM * MM_TO_PT),
        pageCompression=1,
        pdfVersion=(1, 3),
    )
    pdf.setTitle("Arreal - Capa 14x21 cm - Fabrica do Livro")
    pdf.setAuthor("Bruno Duarte Corrêa")
    pdf.setSubject("Capa completa com lombada de 16,74 mm e sangria de 2,5 mm")
    pdf.drawImage(
        ImageReader(COVER_CMYK_JPG),
        0,
        0,
        width=COVER_W_MM * MM_TO_PT,
        height=COVER_H_MM * MM_TO_PT,
        preserveAspectRatio=False,
        mask="auto",
    )
    pdf.showPage()
    pdf.save()


def verify() -> None:
    interior = PdfReader(INTERIOR_OUT)
    if len(interior.pages) != PAGE_COUNT:
        raise AssertionError("A paginação do miolo mudou.")
    expected_interior = (INTERIOR_W_MM * MM_TO_PT, INTERIOR_H_MM * MM_TO_PT)
    for index, page in enumerate(interior.pages, start=1):
        actual = (float(page.mediabox.width), float(page.mediabox.height))
        if any(abs(a - e) > 0.02 for a, e in zip(actual, expected_interior)):
            raise AssertionError(f"Página {index} com tamanho inesperado: {actual}")

    cover = PdfReader(COVER_OUT)
    if len(cover.pages) != 1:
        raise AssertionError("A capa deve ter uma página.")
    actual_cover = (
        float(cover.pages[0].mediabox.width),
        float(cover.pages[0].mediabox.height),
    )
    expected_cover = (COVER_W_MM * MM_TO_PT, COVER_H_MM * MM_TO_PT)
    if any(abs(a - e) > 0.02 for a, e in zip(actual_cover, expected_cover)):
        raise AssertionError(f"Capa com tamanho inesperado: {actual_cover}")

    print(f"Miolo: {len(interior.pages)} páginas, {INTERIOR_W_MM:.2f} x {INTERIOR_H_MM:.2f} mm")
    print(f"Capa: {COVER_W_MM:.2f} x {COVER_H_MM:.2f} mm")
    print(f"Lombada: {SPINE_MM:.2f} mm")
    print(INTERIOR_OUT)
    print(COVER_OUT)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    build_interior()
    build_cover()
    verify()


if __name__ == "__main__":
    main()
