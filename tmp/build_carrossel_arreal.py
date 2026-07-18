from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "marketing" / "carrossel_primeiro_post"
SOURCES = OUT / "fontes"
SCENES = ROOT / "output" / "marketing" / "cenas"
IMAGES = ROOT / "images"

W, H = 1080, 1350
GOLD = (222, 163, 91)
PALE_GOLD = (242, 203, 148)
WHITE = (245, 243, 237)
MUTED = (190, 199, 207)
INK = (5, 13, 21)

FONT_HEAD = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT_BODY = "/System/Library/Fonts/Avenir Next.ttc"
FONT_BODY_BOLD = "/System/Library/Fonts/Avenir Next.ttc"


def font(path: str, size: int, index: int = 0) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size, index=index)


def crop_fill(path: Path, focus=(0.5, 0.5)) -> Image.Image:
    image = Image.open(path).convert("RGB")
    scale = max(W / image.width, H / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    image = image.resize(size, Image.Resampling.LANCZOS)
    extra_x = max(0, image.width - W)
    extra_y = max(0, image.height - H)
    left = round(extra_x * focus[0])
    top = round(extra_y * focus[1])
    return image.crop((left, top, left + W, top + H))


def vertical_gradient(size, top_alpha=210, middle_alpha=15, bottom_alpha=145):
    gradient = Image.new("L", size)
    pixels = gradient.load()
    h = size[1]
    for y in range(h):
        p = y / max(1, h - 1)
        if p < 0.48:
            t = p / 0.48
            alpha = round(top_alpha * (1 - t) + middle_alpha * t)
        else:
            t = (p - 0.48) / 0.52
            alpha = round(middle_alpha * (1 - t) + bottom_alpha * t)
        for x in range(size[0]):
            pixels[x, y] = alpha
    layer = Image.new("RGBA", size, (*INK, 0))
    layer.putalpha(gradient)
    return layer


def add_overlay(base: Image.Image, uniform=35, top=210, middle=20, bottom=145):
    canvas = base.convert("RGBA")
    if uniform:
        canvas = Image.alpha_composite(canvas, Image.new("RGBA", canvas.size, (*INK, uniform)))
    canvas = Image.alpha_composite(
        canvas, vertical_gradient(canvas.size, top, middle, bottom)
    )
    return canvas


def text_size(draw, text, face, spacing=4, stroke_width=0):
    box = draw.multiline_textbbox(
        (0, 0), text, font=face, spacing=spacing, stroke_width=stroke_width
    )
    return box[2] - box[0], box[3] - box[1]


def fit_font(draw, text, path, max_size, min_size, max_width, spacing=4, index=0):
    for size in range(max_size, min_size - 1, -2):
        face = font(path, size, index=index)
        width, _ = text_size(draw, text, face, spacing=spacing)
        if width <= max_width:
            return face
    return font(path, min_size, index=index)


def draw_center(draw, text, y, face, fill, spacing=4, stroke=0, stroke_fill=INK):
    width, height = text_size(draw, text, face, spacing=spacing, stroke_width=stroke)
    x = (W - width) / 2
    draw.multiline_text(
        (x, y),
        text,
        font=face,
        fill=fill,
        spacing=spacing,
        align="center",
        stroke_width=stroke,
        stroke_fill=stroke_fill,
    )
    return y + height


def draw_brand(draw, number, light=False):
    color = WHITE if light else MUTED
    small = font(FONT_BODY, 22)
    draw.text((62, 46), "ARREAL  •  BRUNO DUARTE CORRÊA", font=small, fill=color)
    page = f"{number}/7"
    box = draw.textbbox((0, 0), page, font=small)
    draw.text((W - 62 - (box[2] - box[0]), 46), page, font=small, fill=color)
    draw.rounded_rectangle((62, 84, 184, 89), radius=3, fill=GOLD)


def save_slide(image, name):
    path = OUT / name
    image.convert("RGB").save(path, quality=95, optimize=True)
    return path


def save_preview(slides):
    thumb_w, thumb_h = 324, 405
    preview = Image.new("RGB", (thumb_w * 4, thumb_h * 2), (16, 24, 32))
    for index, slide in enumerate(slides):
        image = Image.open(slide).convert("RGB").resize(
            (thumb_w, thumb_h), Image.Resampling.LANCZOS
        )
        preview.paste(image, ((index % 4) * thumb_w, (index // 4) * thumb_h))
    preview.save(OUT / "preview_carrossel.jpg", quality=92, optimize=True)


def slide_1():
    base = crop_fill(SOURCES / "00_arte_base_abertura.png", focus=(0.5, 0.5))
    canvas = add_overlay(base, uniform=20, top=205, middle=8, bottom=150)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 1)

    pre = font(FONT_BODY, 44)
    draw_center(draw, "E SE VOCÊ JÁ TIVESSE", 132, pre, WHITE)
    power = fit_font(draw, "PODERES...", FONT_HEAD, 132, 104, 920)
    draw_center(draw, "PODERES...", 188, power, GOLD, spacing=0, stroke=1)
    final = fit_font(draw, "MAS TIVESSE ESQUECIDO?", FONT_HEAD, 82, 62, 930)
    draw_center(draw, "MAS TIVESSE ESQUECIDO?", 320, final, WHITE, spacing=0)

    swipe = font(FONT_BODY, 26)
    draw.rounded_rectangle((728, 1244, 1018, 1302), radius=29, fill=(8, 18, 27, 210), outline=GOLD, width=2)
    draw.text((782, 1255), "DESLIZE  →", font=swipe, fill=WHITE)
    return save_slide(canvas, "01_e_se_voce_tivesse_poderes.png")


def slide_2():
    base = crop_fill(SCENES / "07_despertar_no_hospital.png", focus=(0.5, 0.43))
    canvas = add_overlay(base, uniform=40, top=225, middle=15, bottom=170)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 2)

    headline = font(FONT_HEAD, 116)
    draw.multiline_text((62, 145), "CINCO ANOS\nEM COMA.", font=headline, fill=GOLD, spacing=-8)
    body = font(FONT_BODY, 42)
    draw.multiline_text(
        (64, 420),
        "Quando acordou,\nele não lembrava\nquem era.",
        font=body,
        fill=WHITE,
        spacing=12,
    )
    return save_slide(canvas, "02_cinco_anos_em_coma.png")


def slide_3():
    base = crop_fill(SCENES / "05_garoto_empire_state_moeda.png", focus=(0.58, 0.46))
    canvas = add_overlay(base, uniform=32, top=225, middle=5, bottom=175)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 3)

    first = font(FONT_HEAD, 76)
    draw.multiline_text(
        (62, 140), "MAS O IMPOSSÍVEL\nCOMEÇOU A", font=first, fill=WHITE, spacing=-2
    )
    last = fit_font(draw, "RECONHECÊ-LO.", FONT_HEAD, 112, 82, 950)
    draw.text((62, 304), "RECONHECÊ-LO.", font=last, fill=GOLD)

    body = font(FONT_BODY, 35)
    draw.text((64, 1228), "E aquilo que parecia perdido começou a voltar.", font=body, fill=WHITE)
    return save_slide(canvas, "03_o_impossivel_o_reconheceu.png")


def slide_4():
    base = crop_fill(SCENES / "01_confronto_no_patio.png", focus=(0.5, 0.45))
    canvas = add_overlay(base, uniform=30, top=220, middle=5, bottom=180)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 4)

    headline = fit_font(draw, "ELE NÃO ERA O ÚNICO.", FONT_HEAD, 112, 82, 950)
    draw.text((62, 142), "ELE NÃO ERA O ÚNICO.", font=headline, fill=GOLD)
    body = font(FONT_BODY, 44)
    draw.text((64, 270), "Outros também estavam despertando.", font=body, fill=WHITE)
    return save_slide(canvas, "04_ele_nao_era_o_unico.png")


def slide_5():
    base = crop_fill(SCENES / "20_realidades_fragmentadas.png", focus=(0.5, 0.47))
    canvas = add_overlay(base, uniform=48, top=225, middle=0, bottom=210)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 5)

    headline = font(FONT_HEAD, 91)
    draw.multiline_text(
        (62, 142), "QUANTO MAIS ELE\nDESCOBRE...", font=headline, fill=GOLD, spacing=-2
    )
    panel = Image.new("RGBA", (W - 96, 206), (5, 13, 21, 205))
    canvas.alpha_composite(panel, (48, 1086))
    draw = ImageDraw.Draw(canvas)
    body = font(FONT_BODY, 44)
    draw.multiline_text(
        (74, 1120),
        "menos pode confiar\nna própria memória.",
        font=body,
        fill=WHITE,
        spacing=7,
    )
    return save_slide(canvas, "05_a_propria_memoria.png")


def slide_6():
    base = crop_fill(SOURCES / "00_arte_base_memorias.png", focus=(0.5, 0.5))
    canvas = add_overlay(base, uniform=18, top=225, middle=0, bottom=190)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 6)

    first = font(FONT_HEAD, 85)
    draw.multiline_text(
        (62, 140), "E SE VOCÊ TAMBÉM\nFOI O GAROTO...", font=first, fill=WHITE, spacing=-2
    )
    question = fit_font(draw, "E SÓ NÃO SE LEMBRA?", FONT_HEAD, 86, 68, 930)
    draw_center(draw, "E SÓ NÃO SE LEMBRA?", 1164, question, PALE_GOLD)
    return save_slide(canvas, "06_e_se_voce_foi_o_garoto.png")


def slide_7():
    background = crop_fill(SOURCES / "00_arte_base_abertura.png", focus=(0.5, 0.5))
    background = background.filter(ImageFilter.GaussianBlur(18)).convert("RGBA")
    canvas = Image.alpha_composite(background, Image.new("RGBA", (W, H), (*INK, 205)))
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, 7, light=True)

    title = fit_font(draw, "ARREAL", FONT_HEAD, 124, 96, 440)
    draw.text((62, 154), "ARREAL", font=title, fill=GOLD)
    body = font(FONT_BODY, 34)
    draw.multiline_text(
        (64, 290),
        "Uma história sobre poder,\nidentidade e tudo o que\nescolhemos esquecer.",
        font=body,
        fill=WHITE,
        spacing=12,
    )

    cover = Image.open(IMAGES / "capa_kdp_refinada.png").convert("RGB")
    cover.thumbnail((440, 850), Image.Resampling.LANCZOS)
    shadow = Image.new("RGBA", (cover.width + 70, cover.height + 70), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (35, 35, 35 + cover.width, 35 + cover.height), radius=8, fill=(0, 0, 0, 205)
    )
    shadow = shadow.filter(ImageFilter.GaussianBlur(24))
    cover_x, cover_y = 578, 220
    canvas.alpha_composite(shadow, (cover_x - 35, cover_y - 35))
    canvas.paste(cover, (cover_x, cover_y))

    draw = ImageDraw.Draw(canvas)
    badge = (62, 708, 514, 790)
    draw.rounded_rectangle(badge, radius=15, fill=GOLD)
    badge_font = font(FONT_HEAD, 49)
    draw.text((102, 719), "EM BREVE NO KINDLE", font=badge_font, fill=INK)
    cta = font(FONT_BODY, 33)
    draw.multiline_text(
        (64, 842),
        "Salve este post e acompanhe\no lançamento.",
        font=cta,
        fill=WHITE,
        spacing=10,
    )
    author = font(FONT_BODY, 27)
    draw.text((64, 1232), "BRUNO DUARTE CORRÊA", font=author, fill=PALE_GOLD)
    return save_slide(canvas, "07_arreal_em_breve_no_kindle.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    SOURCES.mkdir(parents=True, exist_ok=True)
    slides = [slide_1(), slide_2(), slide_3(), slide_4(), slide_5(), slide_6(), slide_7()]
    save_preview(slides)
    for slide in slides:
        print(slide)


if __name__ == "__main__":
    main()
