from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "fontes"
WIDTH, HEIGHT = 591, 2126  # 5 x 18 cm at 300 dpi (trim-size preview)
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"


def tracked_width(draw, text, font, tracking):
    return sum(draw.textlength(char, font=font) for char in text) + tracking * (len(text) - 1)


def draw_tracked(draw, xy, text, font, fill, tracking, anchor="la", stroke_width=0, stroke_fill=None):
    x, y = xy
    if anchor.startswith("m"):
        x -= tracked_width(draw, text, font, tracking) / 2
    for char in text:
        draw.text(
            (x, y),
            char,
            font=font,
            fill=fill,
            anchor="la",
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        x += draw.textlength(char, font=font) + tracking


def vertical_gradient(size, top_alpha, bottom_alpha, color=(3, 10, 16)):
    w, h = size
    alpha = Image.new("L", (1, h))
    px = alpha.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        if t < 0.28:
            a = int(top_alpha * (1 - t / 0.28))
        elif t > 0.72:
            a = int(bottom_alpha * ((t - 0.72) / 0.28))
        else:
            a = 0
        px[0, y] = a
    alpha = alpha.resize((w, h))
    overlay = Image.new("RGBA", size, color + (255,))
    overlay.putalpha(alpha)
    return overlay


def make_bookmark(
    source_name,
    output_name,
    title_color,
    author_color,
    top_alpha,
    bottom_alpha,
    centering=(0.5, 0.5),
):
    source = Image.open(SOURCE / source_name).convert("RGB")
    image = ImageOps.fit(
        source,
        (WIDTH, HEIGHT),
        method=Image.Resampling.LANCZOS,
        centering=centering,
    )
    image = image.convert("RGBA")
    image.alpha_composite(vertical_gradient(image.size, top_alpha, bottom_alpha))

    draw = ImageDraw.Draw(image)
    title_font = ImageFont.truetype(FONT_BOLD, 118)
    author_font = ImageFont.truetype(FONT_REGULAR, 32)
    social_font = ImageFont.truetype(FONT_REGULAR, 24)

    draw_tracked(
        draw,
        (WIDTH / 2, 92),
        "ARREAL",
        title_font,
        title_color,
        5,
        anchor="ma",
        stroke_width=1,
        stroke_fill=(0, 0, 0, 110),
    )
    draw_tracked(
        draw,
        (WIDTH / 2, HEIGHT - 160),
        "BRUNO DUARTE CORRÊA",
        author_font,
        author_color,
        3,
        anchor="ma",
        stroke_width=1,
        stroke_fill=(0, 0, 0, 125),
    )
    draw_tracked(
        draw,
        (WIDTH / 2, HEIGHT - 91),
        "@brunoduartec.escreve",
        social_font,
        author_color,
        1,
        anchor="ma",
        stroke_width=1,
        stroke_fill=(0, 0, 0, 125),
    )

    rgb = image.convert("RGB")
    rgb.save(ROOT / output_name, quality=96, dpi=(300, 300))
    return rgb


def add_shadow(canvas, bookmark, xy):
    x, y = xy
    shadow = Image.new("RGBA", (bookmark.width + 36, bookmark.height + 36), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (18, 14, bookmark.width + 18, bookmark.height + 14),
        radius=7,
        fill=(0, 0, 0, 115),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas.alpha_composite(shadow, (x - 18, y - 14))
    canvas.alpha_composite(bookmark.convert("RGBA"), (x, y))


def make_contact_sheet(items):
    canvas = Image.new("RGBA", (1660, 1160), (238, 233, 225, 255))
    draw = ImageDraw.Draw(canvas)
    heading = ImageFont.truetype(FONT_BOLD, 58)
    label = ImageFont.truetype(FONT_BOLD, 34)
    sublabel = ImageFont.truetype(FONT_REGULAR, 25)
    draw.text((830, 52), "ARREAL · PROPOSTAS DE MARCADOR", font=heading, fill=(12, 25, 35), anchor="ma")

    preview_size = (230, 828)
    xs = [95, 505, 915, 1325]
    labels = [
        ("01 · A MOEDA", "abertura · baixo spoiler"),
        ("02 · A PORTA", "mistério · baixo spoiler"),
        ("03 · GRÁFICO", "identidade · zero spoiler"),
        ("04 · CAPA", "arte oficial · conceitual"),
    ]
    for x, item, texts in zip(xs, items, labels):
        preview = item.resize(preview_size, Image.Resampling.LANCZOS)
        add_shadow(canvas, preview, (x, 145))
        draw.text((x + preview_size[0] / 2, 1010), texts[0], font=label, fill=(12, 25, 35), anchor="ma")
        draw.text((x + preview_size[0] / 2, 1054), texts[1], font=sublabel, fill=(75, 78, 80), anchor="ma")

    canvas.convert("RGB").save(ROOT / "00_prancha_comparativa.jpg", quality=95, dpi=(150, 150))


if __name__ == "__main__":
    moeda = make_bookmark(
        "moeda.png",
        "01_marcador_a_moeda.png",
        title_color=(9, 24, 36, 255),
        author_color=(239, 225, 198, 255),
        top_alpha=12,
        bottom_alpha=145,
    )
    porta = make_bookmark(
        "porta.png",
        "02_marcador_a_porta.png",
        title_color=(225, 177, 105, 255),
        author_color=(225, 177, 105, 255),
        top_alpha=105,
        bottom_alpha=175,
    )
    grafico = make_bookmark(
        "grafico.png",
        "03_marcador_grafico.png",
        title_color=(225, 177, 105, 255),
        author_color=(225, 177, 105, 255),
        top_alpha=70,
        bottom_alpha=105,
    )
    capa = make_bookmark(
        "capa.png",
        "04_marcador_capa.png",
        title_color=(225, 177, 105, 255),
        author_color=(225, 177, 105, 255),
        top_alpha=115,
        bottom_alpha=155,
        centering=(0.55, 0.5),
    )
    make_contact_sheet([moeda, porta, grafico, capa])
