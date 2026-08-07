from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
MARKETING = HERE.parents[1]
OUTPUT_ROOT = HERE.parents[2]
BACKGROUND = HERE / "fundo_arreal_story.png"
PORTRAIT = MARKETING / "perfil" / "bruno_duarte_correa_autor.png"
COVER = OUTPUT_ROOT / "kdp" / "Arreal_Capa_Kindle_1600x2560.jpg"
OUTPUT = HERE.parent / "Arreal_Story_Convite_Perfil_Escritor.png"

W, H = 1080, 1920
FONT_BOLD = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Avenir Next Condensed.ttc"
FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def crop_cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_ratio = size[0] / size[1]
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        width = round(image.height * target_ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / target_ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    return image.resize(size, Image.Resampling.LANCZOS)


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def fit_font(text: str, path: str, max_width: int, start: int, minimum: int = 20):
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    for size in range(start, minimum - 1, -2):
        font = ImageFont.truetype(path, size)
        box = probe.textbbox((0, 0), text, font=font)
        if box[2] - box[0] <= max_width:
            return font
    return ImageFont.truetype(path, minimum)


def main():
    bg = crop_cover(Image.open(BACKGROUND).convert("RGB"), (W, H))
    bg = ImageEnhance.Contrast(bg).enhance(1.04).convert("RGBA")

    # Dark central veil keeps the invitation readable without erasing the Arreal atmosphere.
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    px = veil.load()
    for y in range(H):
        for x in range(W):
            center = abs(x - W / 2) / (W / 2)
            alpha = int(82 + 45 * (1 - center) + 28 * (y / H))
            px[x, y] = (1, 7, 15, min(170, alpha))
    canvas = Image.alpha_composite(bg, veil)

    # Author portrait — preserve the approved image exactly, only crop it to a circle.
    portrait_size = 176
    portrait = crop_cover(Image.open(PORTRAIT).convert("RGB"), (portrait_size, portrait_size)).convert("RGBA")
    circle = Image.new("L", (portrait_size, portrait_size), 0)
    ImageDraw.Draw(circle).ellipse((0, 0, portrait_size - 1, portrait_size - 1), fill=255)
    portrait.putalpha(circle)
    ring = Image.new("RGBA", (portrait_size + 18, portrait_size + 18), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_draw.ellipse((2, 2, portrait_size + 15, portrait_size + 15), fill=(12, 22, 34, 245), outline=(221, 153, 75, 255), width=5)
    canvas.alpha_composite(ring, (72, 86))
    canvas.alpha_composite(portrait, (81, 95))

    draw = ImageDraw.Draw(canvas)
    name_font = ImageFont.truetype(FONT_ARIAL_BOLD, 34)
    role_font = ImageFont.truetype(FONT_REGULAR, 30)
    draw.text((286, 128), "BRUNO DUARTE CORRÊA", font=name_font, fill=(245, 239, 227), anchor="la")
    draw.text((286, 177), "autor de ARREAL", font=role_font, fill=(218, 164, 99), anchor="la")

    # Main message.
    headline_font = ImageFont.truetype(FONT_BOLD, 104)
    headline_y = 340
    for line in ("EU PUBLIQUEI", "MEU PRIMEIRO", "LIVRO."):
        draw.text(
            (78, headline_y),
            line,
            font=headline_font,
            fill=(239, 184, 108) if line == "LIVRO." else (247, 244, 237),
            stroke_width=2,
            stroke_fill=(0, 5, 12),
            anchor="la",
        )
        headline_y += 104

    sub_font = ImageFont.truetype(FONT_REGULAR, 44)
    sub_lines = ("Agora quero dividir essa jornada", "e os bastidores de Arreal com vocês.")
    sub_y = 692
    for line in sub_lines:
        draw.text((80, sub_y), line, font=sub_font, fill=(225, 224, 220), anchor="la")
        sub_y += 54

    # Approved cover as a physical-looking card, without regenerating or changing its typography.
    cover_w, cover_h = 346, 554
    cover = Image.open(COVER).convert("RGB").resize((cover_w, cover_h), Image.Resampling.LANCZOS).convert("RGBA")
    cover_mask = rounded_mask((cover_w, cover_h), 13)
    cover.putalpha(cover_mask)

    shadow = Image.new("RGBA", (cover_w + 90, cover_h + 90), (0, 0, 0, 0))
    shadow_shape = Image.new("L", (cover_w, cover_h), 0)
    ImageDraw.Draw(shadow_shape).rounded_rectangle((0, 0, cover_w, cover_h), radius=13, fill=210)
    shadow_shape = shadow_shape.filter(ImageFilter.GaussianBlur(25))
    shadow.paste((0, 0, 0, 220), (38, 35), shadow_shape)
    canvas.alpha_composite(shadow, (650, 835))
    canvas.alpha_composite(cover, (686, 858))

    # Short premise balances the cover while keeping the Story personal.
    premise_font = ImageFont.truetype(FONT_BOLD, 52)
    premise_y = 940
    for line in ("FANTASIA,", "MEMÓRIA", "E PODERES", "ESQUECIDOS."):
        draw.text((80, premise_y), line, font=premise_font, fill=(241, 237, 228), anchor="la")
        premise_y += 62

    line_y = 1237
    draw.line((82, line_y, 540, line_y), fill=(210, 144, 72, 210), width=3)
    detail_font = ImageFont.truetype(FONT_REGULAR, 34)
    draw.text((80, 1280), "Um novo perfil para contar", font=detail_font, fill=(206, 210, 211), anchor="la")
    draw.text((80, 1323), "como essa história nasceu.", font=detail_font, fill=(206, 210, 211), anchor="la")

    # CTA in the Instagram safe zone. The handle stays whole and highly legible.
    cta_box = (76, 1500, 1004, 1728)
    cta_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cta_draw = ImageDraw.Draw(cta_layer)
    cta_draw.rounded_rectangle(cta_box, radius=35, fill=(6, 16, 28, 232), outline=(219, 151, 74, 235), width=4)
    cta_layer = cta_layer.filter(ImageFilter.GaussianBlur(0.25))
    canvas = Image.alpha_composite(canvas, cta_layer)
    draw = ImageDraw.Draw(canvas)
    cta_label_font = ImageFont.truetype(FONT_REGULAR, 34)
    draw.text((W // 2, 1557), "ME ACOMPANHE NO PERFIL DE ESCRITOR", font=cta_label_font, fill=(218, 213, 203), anchor="ma")
    handle = "@brunoduartec.escreve"
    handle_font = fit_font(handle, FONT_ARIAL_BOLD, 820, 57)
    draw.text((W // 2, 1644), handle, font=handle_font, fill=(239, 176, 94), anchor="mm")

    footer_font = ImageFont.truetype(FONT_REGULAR, 28)
    draw.text((W // 2, 1800), "A história começou. Quero você por perto.", font=footer_font, fill=(186, 191, 192), anchor="ma")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT, "PNG", optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
