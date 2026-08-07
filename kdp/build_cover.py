#!/usr/bin/env python3
"""Generate the full KDP paperback cover from the approved front artwork."""

from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "images" / "capa_kdp_sem_texto_v2.png"
OUTPUT_DIR = ROOT / "output" / "kdp"

ISBN13 = "9786502276570"
ISBN_DISPLAY = "978-65-02-27657-0"
PAGE_COUNT = 310
TRIM_W_IN = 5.5
TRIM_H_IN = 8.5
BLEED_IN = 0.125
SPINE_IN = PAGE_COUNT * 0.0025  # KDP black-and-white interior on cream paper.
FULL_W_IN = (2 * TRIM_W_IN) + SPINE_IN + (2 * BLEED_IN)
FULL_H_IN = TRIM_H_IN + (2 * BLEED_IN)
PPI = 300

PNG_OUT = OUTPUT_DIR / "Arreal_Capa_Impressa_55x85_310p.png"
JPG_OUT = OUTPUT_DIR / "Arreal_Capa_Impressa_55x85_310p.jpg"
PDF_OUT = OUTPUT_DIR / "Arreal_Capa_Impressa_55x85_310p.pdf"
BARCODE_OUT = OUTPUT_DIR / "Arreal_ISBN_978-65-02-27657-0_EAN13.png"

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

EAN_L = {
    "0": "0001101", "1": "0011001", "2": "0010011", "3": "0111101",
    "4": "0100011", "5": "0110001", "6": "0101111", "7": "0111011",
    "8": "0110111", "9": "0001011",
}
EAN_G = {
    "0": "0100111", "1": "0110011", "2": "0011011", "3": "0100001",
    "4": "0011101", "5": "0111001", "6": "0000101", "7": "0010001",
    "8": "0001001", "9": "0010111",
}
EAN_R = {
    "0": "1110010", "1": "1100110", "2": "1101100", "3": "1000010",
    "4": "1011100", "5": "1001110", "6": "1010000", "7": "1000100",
    "8": "1001000", "9": "1110100",
}
EAN_PARITY = {
    "0": "LLLLLL", "1": "LLGLGG", "2": "LLGGLG", "3": "LLGGGL",
    "4": "LGLLGG", "5": "LGGLLG", "6": "LGGGLL", "7": "LGLGLG",
    "8": "LGLGGL", "9": "LGGLGL",
}


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
        raise ValueError(f"{label} fora da zona segura: {bounds}; zona segura: {safe_box}")


def isbn13_check_digit(first_twelve: str) -> str:
    if len(first_twelve) != 12 or not first_twelve.isdigit():
        raise ValueError("O ISBN deve fornecer exatamente os 12 primeiros dígitos.")
    weighted_sum = sum(
        int(digit) * (1 if index % 2 == 0 else 3)
        for index, digit in enumerate(first_twelve)
    )
    return str((10 - weighted_sum % 10) % 10)


def ean13_modules(value: str) -> str:
    if len(value) != 13 or not value.isdigit():
        raise ValueError("EAN-13 deve conter exatamente 13 dígitos.")
    expected = isbn13_check_digit(value[:12])
    if value[-1] != expected:
        raise ValueError(f"Dígito verificador inválido: esperado {expected}, recebido {value[-1]}.")

    parity = EAN_PARITY[value[0]]
    left = "".join(
        (EAN_L if encoding == "L" else EAN_G)[digit]
        for digit, encoding in zip(value[1:7], parity)
    )
    right = "".join(EAN_R[digit] for digit in value[7:])
    modules = f"101{left}01010{right}101"
    if len(modules) != 95:
        raise AssertionError(f"EAN-13 deveria ter 95 módulos, mas tem {len(modules)}.")
    return modules


def build_barcode() -> Image.Image:
    """Render a press-ready Bookland EAN-13 block at 300 ppi."""
    canvas_w = round(2.15 * PPI)
    canvas_h = round(1.35 * PPI)
    module_w = 5
    quiet_left = 12
    quiet_right = 10
    modules = ean13_modules(ISBN13)
    symbol_w = (quiet_left + len(modules) + quiet_right) * module_w
    symbol_x = (canvas_w - symbol_w) // 2 + quiet_left * module_w

    barcode = Image.new("RGB", (canvas_w, canvas_h), "white")
    barcode_draw = ImageDraw.Draw(barcode)
    label_font = font(ARIAL, 9)
    digits_font = font(ARIAL, 10)

    label = f"ISBN {ISBN_DISPLAY}"
    label_box = barcode_draw.textbbox((0, 0), label, font=label_font)
    barcode_draw.text(
        ((canvas_w - (label_box[2] - label_box[0])) / 2, round(0.08 * PPI)),
        label,
        font=label_font,
        fill="black",
    )

    bar_top = round(0.31 * PPI)
    bar_bottom = round(1.03 * PPI)
    guard_bottom = round(1.09 * PPI)
    guard_ranges = ((0, 3), (45, 50), (92, 95))
    for index, bit in enumerate(modules):
        if bit != "1":
            continue
        is_guard = any(start <= index < end for start, end in guard_ranges)
        barcode_draw.rectangle(
            (
                symbol_x + index * module_w,
                bar_top,
                symbol_x + (index + 1) * module_w - 1,
                guard_bottom if is_guard else bar_bottom,
            ),
            fill="black",
        )

    digit_y = round(1.075 * PPI)
    first_width = barcode_draw.textlength(ISBN13[0], font=digits_font)
    barcode_draw.text(
        (symbol_x - 7 * module_w - first_width / 2, digit_y),
        ISBN13[0],
        font=digits_font,
        fill="black",
    )
    for offset, digit in enumerate(ISBN13[1:7]):
        center = symbol_x + (3 + offset * 7 + 3.5) * module_w
        digit_width = barcode_draw.textlength(digit, font=digits_font)
        barcode_draw.text((center - digit_width / 2, digit_y), digit, font=digits_font, fill="black")
    for offset, digit in enumerate(ISBN13[7:]):
        center = symbol_x + (50 + offset * 7 + 3.5) * module_w
        digit_width = barcode_draw.textlength(digit, font=digits_font)
        barcode_draw.text((center - digit_width / 2, digit_y), digit, font=digits_font, fill="black")

    barcode.save(BARCODE_OUT, format="PNG", dpi=(PPI, PPI), optimize=True)
    return barcode


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

    # Draw the front-cover typography as separate, measurable elements. KDP asks
    # for at least 0.375 in from every trim edge; 0.5 in provides extra tolerance
    # for cutting variance and automated quality checks.
    front_trim_left = front_x
    front_trim_right = width - bleed
    front_trim_top = bleed
    front_trim_bottom = height - bleed
    front_safe_inset = round(0.5 * PPI)
    front_safe = (
        front_trim_left + front_safe_inset,
        front_trim_top + front_safe_inset,
        front_trim_right - front_safe_inset,
        front_trim_bottom - front_safe_inset,
    )
    front_center_x = (front_trim_left + front_trim_right) / 2

    front_title = "ARREAL"
    front_title_font = font(ARIAL_NARROW_BOLD, 88)
    front_title_tracking = round(0.06 * PPI)
    title_reference = draw.textbbox((0, 0), front_title, font=front_title_font)
    title_y = front_safe[1] - title_reference[1]
    title_bounds = draw_centered_tracking(
        draw,
        front_center_x,
        title_y,
        front_title,
        front_title_font,
        warm,
        front_title_tracking,
    )
    assert_inside("Título da frente", title_bounds, front_safe)

    front_author = "BRUNO DUARTE CORRÊA"
    front_author_font = font(ARIAL, 15)
    front_author_tracking = round(0.045 * PPI)
    author_reference = draw.textbbox((0, 0), front_author, font=front_author_font)
    author_y = front_safe[3] - author_reference[3]
    author_bounds = draw_centered_tracking(
        draw,
        front_center_x,
        author_y,
        front_author,
        front_author_font,
        warm,
        front_author_tracking,
    )
    assert_inside("Autor da frente", author_bounds, front_safe)

    # Place our assigned ISBN as a Bookland EAN-13 barcode. Supplying it in the
    # cover prevents KDP from adding a second barcode to the reserved area.
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
    barcode = build_barcode()
    if barcode.size != (barcode_w, barcode_h):
        raise AssertionError(f"Tamanho inesperado do código de barras: {barcode.size}")
    cover.paste(barcode, (barcode_box[0], barcode_box[1]))

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
    print(f"Front safe zone: 0.500 in from trim edges")
    print(f"Front title bounds: {title_bounds}")
    print(f"Front author bounds: {author_bounds}")
    print(f"ISBN: {ISBN_DISPLAY} (EAN-13 válido)")
    print(BARCODE_OUT)
    print(PDF_OUT)


if __name__ == "__main__":
    build()
