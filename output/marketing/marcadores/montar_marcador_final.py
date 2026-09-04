from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parent
ABSTRACT_SOURCE = Path(
    "/Users/bruno.duartec/.codex/generated_images/"
    "01a0103e-f4e9-71b1-8810-d2ca4984d4cb/"
    "exec-750beb9d-6eb2-4fc9-af75-7c58edb2f75e.png"
)
WIDTH, HEIGHT = 591, 2126  # 5 x 18 cm a 300 dpi
FONT_SANS_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FONT_SANS = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"
FONT_SERIF_ITALIC = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
FONT_SERIF_BOLD_ITALIC = "/System/Library/Fonts/Supplemental/Georgia Bold Italic.ttf"
GOLD = (226, 177, 103, 255)
CREAM = (239, 231, 216, 255)
NAVY = (7, 17, 25, 255)


def tracked_width(draw, text, font, tracking):
    return sum(draw.textlength(char, font=font) for char in text) + tracking * (len(text) - 1)


def draw_tracked(draw, xy, text, font, fill, tracking, anchor="ma"):
    x, y = xy
    if anchor.startswith("m"):
        x -= tracked_width(draw, text, font, tracking) / 2
    for char in text:
        draw.text((x, y), char, font=font, fill=fill, anchor="la")
        x += draw.textlength(char, font=font) + tracking


def make_front():
    front = Image.open(ROOT / "04_marcador_capa.png").convert("RGB")
    front.save(ROOT / "marcador_final_frente.png", dpi=(300, 300))
    return front


def make_back():
    source = Image.open(ABSTRACT_SOURCE).convert("RGB")
    back = ImageOps.fit(
        source,
        (WIDTH, HEIGHT),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    ).convert("RGBA")

    # Escurece a textura para dar prioridade à frase, sem criar figura narrativa.
    back.alpha_composite(Image.new("RGBA", back.size, (3, 12, 20, 92)))
    draw = ImageDraw.Draw(back)

    title_font = ImageFont.truetype(FONT_SANS_BOLD, 82)
    quote_font = ImageFont.truetype(FONT_SERIF_ITALIC, 55)
    emphasis_font = ImageFont.truetype(FONT_SERIF_BOLD_ITALIC, 78)
    author_font = ImageFont.truetype(FONT_SANS, 31)
    social_font = ImageFont.truetype(FONT_SANS, 24)

    draw_tracked(draw, (WIDTH / 2, 112), "ARREAL", title_font, GOLD, 4)

    # Filetes puramente gráficos, dentro da margem segura.
    draw.line((162, 390, 429, 390), fill=(226, 177, 103, 155), width=2)
    draw.line((162, 1530, 429, 1530), fill=(226, 177, 103, 155), width=2)

    lines = [
        ("“Todo ser humano", quote_font, CREAM),
        ("é capaz de", quote_font, CREAM),
        ("muito mais", emphasis_font, GOLD),
        ("do que imagina.”", quote_font, CREAM),
    ]
    ys = [690, 825, 960, 1125]
    for (text, font, color), y in zip(lines, ys):
        draw.text((WIDTH / 2, y), text, font=font, fill=color, anchor="ma", align="center")

    draw_tracked(
        draw,
        (WIDTH / 2, HEIGHT - 160),
        "BRUNO DUARTE CORRÊA",
        author_font,
        GOLD,
        3,
    )
    draw_tracked(
        draw,
        (WIDTH / 2, HEIGHT - 91),
        "@brunoduartec.escreve",
        social_font,
        GOLD,
        1,
    )

    result = back.convert("RGB")
    result.save(ROOT / "marcador_final_verso.png", dpi=(300, 300))
    return result


def add_shadow(canvas, image, xy):
    x, y = xy
    shadow = Image.new("RGBA", (image.width + 42, image.height + 42), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (21, 17, image.width + 21, image.height + 17),
        radius=8,
        fill=(0, 0, 0, 115),
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    canvas.alpha_composite(shadow, (x - 21, y - 17))
    canvas.alpha_composite(image.convert("RGBA"), (x, y))


def make_preview(front, back):
    canvas = Image.new("RGBA", (1040, 1260), (238, 233, 225, 255))
    draw = ImageDraw.Draw(canvas)
    heading = ImageFont.truetype(FONT_SANS_BOLD, 58)
    label = ImageFont.truetype(FONT_SANS_BOLD, 35)
    draw.text((520, 56), "MARCADOR ARREAL · FINAL", font=heading, fill=NAVY, anchor="ma")

    size = (280, 1008)
    front_preview = front.resize(size, Image.Resampling.LANCZOS)
    back_preview = back.resize(size, Image.Resampling.LANCZOS)
    add_shadow(canvas, front_preview, (170, 150))
    add_shadow(canvas, back_preview, (590, 150))
    draw.text((310, 1190), "FRENTE", font=label, fill=NAVY, anchor="ma")
    draw.text((730, 1190), "VERSO", font=label, fill=NAVY, anchor="ma")

    canvas.convert("RGB").save(
        ROOT / "marcador_final_frente_verso.jpg",
        quality=95,
        dpi=(150, 150),
    )


if __name__ == "__main__":
    print("Montando verso...", flush=True)
    final_back = make_back()
    print("Concluído.", flush=True)
