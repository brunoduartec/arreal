from pathlib import Path
import random

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


HERE = Path(__file__).resolve().parent
BASE = HERE / "arreal_poster_arte_base.png"
OUTPUT = HERE.parent / "Arreal_Poster_A3_300dpi.png"

# A3 portrait at 300 dpi: 297 x 420 mm.
WIDTH, HEIGHT = 3508, 4961

FONT_TITLE = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT_TEXT = "/System/Library/Fonts/Avenir Next Condensed.ttc"


def crop_to_ratio(image: Image.Image, target_ratio: float) -> Image.Image:
    source_ratio = image.width / image.height
    if source_ratio > target_ratio:
        new_width = round(image.height * target_ratio)
        left = (image.width - new_width) // 2
        return image.crop((left, 0, left + new_width, image.height))

    new_height = round(image.width / target_ratio)
    # Preserve the clean title area while removing most excess height below.
    excess = image.height - new_height
    top = max(0, round(excess * 0.84))
    return image.crop((0, top, image.width, top + new_height))


def spaced_text_mask(
    text: str,
    font: ImageFont.FreeTypeFont,
    spacing: int,
    canvas_width: int,
    canvas_height: int,
) -> Image.Image:
    # Position every glyph on one shared typographic baseline. Measuring and
    # drawing each character from its own top edge makes accents and punctuation
    # float vertically (especially in "NÃO" and at full stops).
    glyph_advances = [font.getlength(char) for char in text]
    total_width = sum(glyph_advances) + spacing * max(0, len(text) - 1)

    mask = Image.new("L", (canvas_width, canvas_height), 0)
    draw = ImageDraw.Draw(mask)
    x = (canvas_width - total_width) // 2
    ascent, _ = font.getmetrics()
    baseline = min(canvas_height - 8, ascent + 8)
    for char, glyph_advance in zip(text, glyph_advances):
        draw.text(
            (round(x), baseline),
            char,
            font=font,
            fill=255,
            anchor="ls",
            stroke_width=0,
        )
        x += glyph_advance + spacing
    return mask


def fit_spaced_font(text: str, font_path: str, max_width: int, start_size: int, spacing: int):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(font_path, size=size)
        widths = [font.getlength(char) for char in text]
        if sum(widths) + spacing * (len(text) - 1) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(font_path, size=size)


def metallic_gold(size: tuple[int, int], seed: int = 91) -> Image.Image:
    width, height = size
    rng = random.Random(seed)
    layer = Image.new("RGBA", size)
    pixels = layer.load()
    for y in range(height):
        t = y / max(1, height - 1)
        # A restrained metallic gradient, warmer through the middle.
        band = 0.5 + 0.5 * abs(2 * t - 1)
        for x in range(width):
            grain = rng.randint(-7, 7)
            r = int(226 - 28 * band + grain)
            g = int(175 - 36 * band + grain)
            b = int(105 - 35 * band + grain // 2)
            pixels[x, y] = (max(0, r), max(0, g), max(0, b), 255)
    return layer.filter(ImageFilter.GaussianBlur(0.28))


def paste_textured_text(base: Image.Image, mask: Image.Image, y: int, glow: int = 0):
    bbox = mask.getbbox()
    if not bbox:
        return
    cropped_mask = mask.crop(bbox)
    x = bbox[0]

    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow_mask = cropped_mask.filter(ImageFilter.GaussianBlur(14))
    shadow_color = Image.new("RGBA", cropped_mask.size, (0, 0, 0, 185))
    shadow.paste(shadow_color, (x + 7, y + 14), shadow_mask)
    base.alpha_composite(shadow)

    if glow:
        glow_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        glow_mask = cropped_mask.filter(ImageFilter.GaussianBlur(glow))
        glow_color = Image.new("RGBA", cropped_mask.size, (211, 147, 63, 70))
        glow_layer.paste(glow_color, (x, y), glow_mask)
        base.alpha_composite(glow_layer)

    texture = metallic_gold(cropped_mask.size)
    base.paste(texture, (x, y), cropped_mask)


def add_vignette(image: Image.Image) -> Image.Image:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    steps = 170
    for i in range(steps):
        alpha = int(1.15 * (steps - i))
        x = round(i * WIDTH * 0.0019)
        y = round(i * HEIGHT * 0.00135)
        draw.rounded_rectangle(
            (x, y, WIDTH - x, HEIGHT - y),
            radius=100,
            outline=(0, 4, 10, max(0, min(80, alpha))),
            width=10,
        )
    return Image.alpha_composite(image, overlay)


def main():
    source = Image.open(BASE).convert("RGB")
    source = crop_to_ratio(source, WIDTH / HEIGHT)
    source = source.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    source = ImageEnhance.Contrast(source).enhance(1.06)
    source = ImageEnhance.Color(source).enhance(0.96)
    source = ImageEnhance.Sharpness(source).enhance(1.15)
    poster = source.convert("RGBA")

    # Quiet the two typography zones while retaining the full-bleed illustration.
    shade = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    shade_pixels = shade.load()
    for y in range(0, 1120):
        alpha = int(120 * max(0.0, 1.0 - y / 1120) ** 0.75)
        for x in range(WIDTH):
            shade_pixels[x, y] = (1, 8, 17, alpha)
    for y in range(4310, HEIGHT):
        alpha = int(145 * ((y - 4310) / (HEIGHT - 4310)) ** 0.85)
        for x in range(WIDTH):
            shade_pixels[x, y] = (0, 4, 9, alpha)
    poster = Image.alpha_composite(poster, shade)
    poster = add_vignette(poster)

    title = "ARREAL"
    title_font = fit_spaced_font(title, FONT_TITLE, int(WIDTH * 0.88), 690, 66)
    title_mask = spaced_text_mask(title, title_font, 66, WIDTH, 760)
    paste_textured_text(poster, title_mask, y=130, glow=18)

    draw = ImageDraw.Draw(poster)
    tagline = "O PODER NÃO DESAPARECE. ELE ESPERA."
    tagline_font = fit_spaced_font(tagline, FONT_TEXT, int(WIDTH * 0.76), 102, 13)
    tagline_mask = spaced_text_mask(tagline, tagline_font, 13, WIDTH, 150)
    tagline_bbox = tagline_mask.getbbox()
    if tagline_bbox:
        tagline_crop = tagline_mask.crop(tagline_bbox)
        tx = tagline_bbox[0]
        tagline_shadow = tagline_crop.filter(ImageFilter.GaussianBlur(5))
        shadow_layer = Image.new("RGBA", poster.size, (0, 0, 0, 0))
        shadow_layer.paste((0, 0, 0, 190), (tx + 3, 850 + 5), tagline_shadow)
        poster.alpha_composite(shadow_layer)
        tagline_layer = Image.new("RGBA", poster.size, (0, 0, 0, 0))
        tagline_layer.paste((218, 204, 180, 235), (tx, 850), tagline_crop)
        poster.alpha_composite(tagline_layer)

    author = "BRUNO DUARTE CORRÊA"
    author_font = fit_spaced_font(author, FONT_TEXT, int(WIDTH * 0.79), 118, 26)
    author_mask = spaced_text_mask(author, author_font, 26, WIDTH, 190)
    author_bbox = author_mask.getbbox()
    if author_bbox:
        author_crop = author_mask.crop(author_bbox)
        ax = author_bbox[0]
        author_shadow = author_crop.filter(ImageFilter.GaussianBlur(6))
        shadow_layer = Image.new("RGBA", poster.size, (0, 0, 0, 0))
        shadow_layer.paste((0, 0, 0, 210), (ax + 4, 4660 + 7), author_shadow)
        poster.alpha_composite(shadow_layer)
        author_layer = Image.new("RGBA", poster.size, (0, 0, 0, 0))
        author_layer.paste((224, 158, 83, 245), (ax, 4660), author_crop)
        poster.alpha_composite(author_layer)

    # Subtle print grain prevents large dark gradients from looking digitally flat.
    rng = random.Random(122)
    grain = Image.new("RGBA", poster.size, (0, 0, 0, 0))
    grain_draw = ImageDraw.Draw(grain)
    for _ in range(28000):
        x = rng.randrange(WIDTH)
        y = rng.randrange(HEIGHT)
        tone = rng.choice((210, 230, 255))
        grain_draw.point((x, y), fill=(tone, tone, tone, rng.randrange(2, 8)))
    poster = Image.alpha_composite(poster, grain)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    poster.convert("RGB").save(OUTPUT, "PNG", dpi=(300, 300), optimize=True)
    print(OUTPUT)


if __name__ == "__main__":
    main()
