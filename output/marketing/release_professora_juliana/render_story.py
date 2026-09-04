from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parent
BACKGROUND = Path(
    "/Users/bruno.duartec/.codex/generated_images/"
    "01a034fe-e556-7cc0-a568-af34159fbdcf/"
    "exec-58993d91-14ee-43f3-a9d4-247e511d1586.png"
)
OUTPUT = ROOT / "arreal_release_story.png"
COVER = Path(
    "/Users/bruno.duartec/Library/CloudStorage/OneDrive-Personal/"
    "Área de Trabalho/Arreal/LaTex/output/kdp/Arreal_Capa_Kindle_1600x2560.jpg"
)
OUTPUT_WITH_COVER = ROOT / "arreal_release_story_com_capa.png"

W, H = 1080, 1920
GOLD = "#E8AD5B"
OFF_WHITE = "#F4F1EA"
MUTED = "#C9C5BC"
NAVY = "#07121D"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_NARROW = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def centered(draw: ImageDraw.ImageDraw, text: str, y: int, face, fill, spacing=4):
    box = draw.multiline_textbbox((0, 0), text, font=face, spacing=spacing, align="center")
    width = box[2] - box[0]
    draw.multiline_text(((W - width) / 2, y), text, font=face, fill=fill,
                        spacing=spacing, align="center")


background = Image.open(BACKGROUND).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
background = background.filter(ImageFilter.GaussianBlur(0.35))

# Preserve the textured background while ensuring strong mobile readability.
veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil)
vd.rectangle((0, 0, W, H), fill=(3, 10, 18, 48))
vd.rounded_rectangle((74, 205, 1006, 1655), radius=38, fill=(3, 11, 20, 188),
                     outline=(232, 173, 91, 95), width=2)
background = Image.alpha_composite(background.convert("RGBA"), veil)

draw = ImageDraw.Draw(background)

centered(draw, "FANTASIA URBANA BRASILEIRA", 282, font(FONT_BOLD, 30), GOLD)

centered(draw, "CONHEÇA", 405, font(FONT_REGULAR, 38), MUTED)
centered(draw, "ARREAL", 480, font(FONT_NARROW, 172), OFF_WHITE)

draw.rounded_rectangle((336, 695, 744, 701), radius=3, fill=GOLD)

hook = "E SE TUDO O QUE\nPARECE FANTASIA\nFOSSE VERDADE?"
centered(draw, hook, 805, font(FONT_BOLD, 58), OFF_WHITE, spacing=19)

centered(draw, "Poderes extraordinários.\nEscolhas profundamente humanas.",
         1115, font(FONT_REGULAR, 38), MUTED, spacing=12)

centered(draw, "BRUNO DUARTE CORRÊA", 1395, font(FONT_BOLD, 31), GOLD)

draw.rounded_rectangle((175, 1510, 905, 1610), radius=50,
                       fill=(7, 18, 29, 230), outline=GOLD, width=3)
centered(draw, "@brunoduartec.escreve", 1543, font(FONT_BOLD, 31), OFF_WHITE)

centered(draw, "DESCUBRA ARREAL", 1742, font(FONT_BOLD, 25), MUTED)

background.convert("RGB").save(OUTPUT, quality=95)
print(OUTPUT)


# Variant for third-party sharing: the official cover is shown unchanged as a
# clearly framed product image, rather than blended into a new narrative scene.
story = Image.open(BACKGROUND).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
story = story.filter(ImageFilter.GaussianBlur(0.35)).convert("RGBA")

veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil)
vd.rectangle((0, 0, W, H), fill=(3, 10, 18, 70))
vd.rounded_rectangle((65, 165, 1015, 1745), radius=38, fill=(3, 11, 20, 178),
                     outline=(232, 173, 91, 90), width=2)
story = Image.alpha_composite(story, veil)
draw = ImageDraw.Draw(story)

centered(draw, "FANTASIA URBANA BRASILEIRA", 220, font(FONT_BOLD, 29), GOLD)
centered(draw, "CONHEÇA", 317, font(FONT_REGULAR, 32), MUTED)
centered(draw, "ARREAL", 365, font(FONT_NARROW, 104), OFF_WHITE)

cover = Image.open(COVER).convert("RGB")
cover_w, cover_h = 420, 672
cover = cover.resize((cover_w, cover_h), Image.Resampling.LANCZOS).convert("RGBA")

shadow = Image.new("RGBA", (cover_w + 70, cover_h + 70), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.rounded_rectangle((35, 25, 35 + cover_w, 25 + cover_h), radius=8,
                     fill=(0, 0, 0, 215))
shadow = shadow.filter(ImageFilter.GaussianBlur(20))
cover_x = (W - cover_w) // 2
cover_y = 515
story.alpha_composite(shadow, (cover_x - 35, cover_y - 25))

border = Image.new("RGBA", (cover_w + 8, cover_h + 8), (0, 0, 0, 0))
bd = ImageDraw.Draw(border)
bd.rounded_rectangle((0, 0, cover_w + 7, cover_h + 7), radius=6,
                     fill=GOLD)
story.alpha_composite(border, (cover_x - 4, cover_y - 4))
story.alpha_composite(cover, (cover_x, cover_y))

centered(draw, "E SE TUDO O QUE PARECE FANTASIA\nFOSSE VERDADE?",
         1260, font(FONT_BOLD, 43), OFF_WHITE, spacing=10)
centered(draw, "BRUNO DUARTE CORRÊA", 1435, font(FONT_BOLD, 29), GOLD)

draw.rounded_rectangle((175, 1535, 905, 1637), radius=51,
                       fill=(7, 18, 29, 235), outline=GOLD, width=3)
centered(draw, "@brunoduartec.escreve", 1569, font(FONT_BOLD, 31), OFF_WHITE)
centered(draw, "DESCUBRA ARREAL", 1780, font(FONT_BOLD, 25), MUTED)

story.convert("RGB").save(OUTPUT_WITH_COVER, quality=95)
print(OUTPUT_WITH_COVER)
