#!/usr/bin/env python3
"""Create the deterministic 4:5 physical-book announcement for Arreal."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
BACKGROUND = ROOT / "output" / "marketing" / "livro_fisico_em_breve" / "fundo_editorial.png"
COVER = ROOT / "output" / "kdp" / "Arreal_Capa_Kindle_1600x2560.jpg"
OUTPUT = (
    ROOT
    / "output"
    / "marketing"
    / "livro_fisico_em_breve"
    / "Arreal_Em_Breve_Livro_Fisico_1080x1350.png"
)

W, H = 1080, 1350
GOLD = (232, 184, 112)
IVORY = (245, 241, 232)
MUTED = (205, 207, 210)
ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
ARIAL_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")
ARIAL_NARROW_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf")


def crop_fill(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def draw_tracked_centered(
    draw: ImageDraw.ImageDraw,
    text: str,
    y: int,
    chosen_font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
    tracking: int,
) -> None:
    widths = [draw.textlength(char, font=chosen_font) for char in text]
    total = sum(widths) + tracking * max(0, len(text) - 1)
    x = (W - total) / 2
    for char, width in zip(text, widths):
        draw.text((x, y), char, font=chosen_font, fill=fill)
        x += width + tracking


def make_book_mockup() -> Image.Image:
    front_w, front_h = 424, 678
    cover = crop_fill(Image.open(COVER).convert("RGB"), front_w, front_h)

    book = Image.new("RGBA", (500, 750), (0, 0, 0, 0))
    draw = ImageDraw.Draw(book)

    # Page block and a restrained spine create a physical object without
    # altering any narrative element of the approved cover.
    draw.polygon(
        [(57, 35), (467, 55), (467, 718), (57, 698)],
        fill=(223, 215, 196, 255),
    )
    draw.polygon(
        [(28, 57), (57, 35), (57, 698), (28, 722)],
        fill=(17, 26, 38, 255),
    )
    draw.polygon(
        [(57, 698), (467, 718), (438, 739), (28, 722)],
        fill=(190, 181, 161, 255),
    )
    book.paste(cover, (57, 35))

    gloss = Image.new("RGBA", book.size, (0, 0, 0, 0))
    gloss_draw = ImageDraw.Draw(gloss)
    gloss_draw.polygon(
        [(57, 35), (175, 41), (92, 698), (57, 698)],
        fill=(255, 255, 255, 13),
    )
    book = Image.alpha_composite(book, gloss)
    return book.rotate(-3.2, resample=Image.Resampling.BICUBIC, expand=True)


def main() -> None:
    background = crop_fill(Image.open(BACKGROUND).convert("RGB"), W, H)
    background = ImageEnhance.Brightness(background).enhance(0.82)

    # Darken the upper copy zone while retaining the generated paper texture.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shade_draw = ImageDraw.Draw(shade)
    for y in range(0, 500):
        alpha = round(155 * (1 - y / 500))
        shade_draw.line((0, y, W, y), fill=(0, 0, 0, alpha))
    composition = Image.alpha_composite(background.convert("RGBA"), shade)

    draw = ImageDraw.Draw(composition)
    draw_tracked_centered(draw, "EM BREVE", 62, font(ARIAL_BOLD, 30), GOLD, 10)
    draw_tracked_centered(draw, "ARREAL", 116, font(ARIAL_NARROW_BOLD, 112), IVORY, 4)
    draw_tracked_centered(
        draw,
        "EM LIVRO FÍSICO",
        239,
        font(ARIAL_NARROW_BOLD, 58),
        GOLD,
        3,
    )
    draw.line((305, 329, 775, 329), fill=GOLD + (180,), width=2)

    book = make_book_mockup()
    shadow = Image.new("RGBA", book.size, (0, 0, 0, 0))
    shadow.putalpha(book.getchannel("A").filter(ImageFilter.GaussianBlur(24)))
    shadow = Image.new("RGBA", book.size, (0, 0, 0, 150))
    shadow.putalpha(book.getchannel("A").filter(ImageFilter.GaussianBlur(24)))

    bx = (W - book.width) // 2
    by = 360
    composition.alpha_composite(shadow, (bx + 22, by + 32))
    composition.alpha_composite(book, (bx, by))

    draw = ImageDraw.Draw(composition)
    footer = "A EDIÇÃO IMPRESSA ESTÁ CHEGANDO"
    footer_font = font(ARIAL_BOLD, 29)
    footer_box = draw.textbbox((0, 0), footer, font=footer_font)
    footer_w = footer_box[2] - footer_box[0]
    pill = (W - footer_w) / 2 - 30, 1190, (W + footer_w) / 2 + 30, 1252
    draw.rounded_rectangle(pill, radius=30, fill=(6, 13, 23, 220), outline=GOLD + (160,), width=2)
    draw.text(((W - footer_w) / 2, 1206), footer, font=footer_font, fill=IVORY)

    draw_tracked_centered(
        draw,
        "ACOMPANHE AS NOVIDADES",
        1281,
        font(ARIAL, 21),
        MUTED,
        5,
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    composition.convert("RGB").save(OUTPUT, format="PNG", dpi=(300, 300), optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
