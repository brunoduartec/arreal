from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[4]
COVER_PATH = ROOT / "output/kdp/Arreal_Capa_Kindle_1600x2560.jpg"
OUT_PATH = ROOT / "output/marketing/posts_planejados/post_07_kindle/arte.png"

WIDTH, HEIGHT = 1080, 1350
GOLD = (218, 155, 72)
PALE_GOLD = (238, 198, 139)
WHITE = (244, 244, 242)
INK = (8, 12, 18)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    source_ratio = image.width / image.height
    target_ratio = target_w / target_h
    if source_ratio > target_ratio:
        new_h = target_h
        new_w = round(new_h * source_ratio)
    else:
        new_w = target_w
        new_h = round(new_w / source_ratio)
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill, spacing=8):
    lines = text.split("\n")
    current_y = y
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        x = (WIDTH - (box[2] - box[0])) // 2
        draw.text((x, current_y), line, font=font, fill=fill)
        current_y += (box[3] - box[1]) + spacing
    return current_y


cover = Image.open(COVER_PATH).convert("RGB")

background = cover_crop(cover, (WIDTH, HEIGHT)).filter(ImageFilter.GaussianBlur(24))
background = ImageEnhance.Brightness(background).enhance(0.30)
background = ImageEnhance.Color(background).enhance(0.75).convert("RGBA")

overlay = Image.new("RGBA", (WIDTH, HEIGHT), (3, 8, 14, 120))
canvas = Image.alpha_composite(background, overlay)

# Subtle blue-to-black vertical veil for legibility.
veil = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
veil_draw = ImageDraw.Draw(veil)
for y in range(HEIGHT):
    alpha = int(100 + 70 * abs((y / HEIGHT) - 0.5) * 2)
    veil_draw.line((0, y, WIDTH, y), fill=(2, 8, 16, min(alpha, 175)))
canvas = Image.alpha_composite(canvas, veil)

draw = ImageDraw.Draw(canvas)
font_brand = ImageFont.truetype(FONT_BOLD, 68)
font_headline = ImageFont.truetype(FONT_BOLD, 58)
font_cta = ImageFont.truetype(FONT_BOLD, 62)
font_author = ImageFont.truetype(FONT_REGULAR, 28)

centered_text(draw, 46, "ARREAL", font_brand, PALE_GOLD)
centered_text(draw, 132, "VOCÊ TEM CERTEZA DE QUE\nNUNCA TEVE PODERES?", font_headline, WHITE, spacing=4)

# Cover with a restrained shadow and a fine gold edge.
cover_h = 735
cover_w = round(cover_h * cover.width / cover.height)
cover_small = cover.resize((cover_w, cover_h), Image.Resampling.LANCZOS).convert("RGBA")
cover_x = (WIDTH - cover_w) // 2
cover_y = 295

shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)
shadow_draw.rounded_rectangle(
    (cover_x - 24, cover_y - 14, cover_x + cover_w + 30, cover_y + cover_h + 34),
    radius=18,
    fill=(0, 0, 0, 210),
)
shadow = shadow.filter(ImageFilter.GaussianBlur(22))
canvas = Image.alpha_composite(canvas, shadow)
draw = ImageDraw.Draw(canvas)
draw.rounded_rectangle(
    (cover_x - 4, cover_y - 4, cover_x + cover_w + 4, cover_y + cover_h + 4),
    radius=5,
    outline=GOLD,
    width=3,
)
canvas.alpha_composite(cover_small, (cover_x, cover_y))

draw = ImageDraw.Draw(canvas)
button = (150, 1080, WIDTH - 150, 1198)
draw.rounded_rectangle(button, radius=28, fill=GOLD, outline=PALE_GOLD, width=3)
cta_box = draw.textbbox((0, 0), "LEIA NO KINDLE", font=font_cta)
cta_x = (WIDTH - (cta_box[2] - cta_box[0])) // 2
cta_y = button[1] + (button[3] - button[1] - (cta_box[3] - cta_box[1])) // 2 - 6
draw.text((cta_x, cta_y), "LEIA NO KINDLE", font=font_cta, fill=INK)

centered_text(draw, 1245, "BRUNO DUARTE CORRÊA", font_author, PALE_GOLD)

OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
canvas.convert("RGB").save(OUT_PATH, quality=95, subsampling=0)

# Contact sheet for quick review of the complete scheduled sequence.
preview_items = [
    (ROOT / "output/marketing/posts_planejados/post_03_dossie/arte.png", "20 JUL"),
    (ROOT / "output/marketing/posts_planejados/post_04_pedro/arte.png", "23 JUL"),
    (ROOT / "output/marketing/posts_planejados/post_05_dirigivel/arte.png", "26 JUL"),
    (ROOT / "output/marketing/posts_planejados/post_06_transmissao/arte.png", "29 JUL"),
    (OUT_PATH, "01 AGO"),
]
thumb_w, thumb_h = 324, 405
gap, top = 24, 64
preview_w = gap + len(preview_items) * (thumb_w + gap)
preview_h = top + thumb_h + 36
preview = Image.new("RGB", (preview_w, preview_h), INK)
preview_draw = ImageDraw.Draw(preview)
preview_font = ImageFont.truetype(FONT_BOLD, 30)
for index, (path, label) in enumerate(preview_items):
    x = gap + index * (thumb_w + gap)
    label_box = preview_draw.textbbox((0, 0), label, font=preview_font)
    label_x = x + (thumb_w - (label_box[2] - label_box[0])) // 2
    preview_draw.text((label_x, 16), label, font=preview_font, fill=PALE_GOLD)
    thumb = Image.open(path).convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
    preview.paste(thumb, (x, top))
preview.save(ROOT / "output/marketing/posts_planejados/preview_cinco_posts.jpg", quality=92, subsampling=0)
