from pathlib import Path
import math
import random
import textwrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[4]
OUT_DIR = ROOT / "output/marketing/posts_planejados/post_04_qual_poder"
COVER_PATH = ROOT / "images/capa_kdp_refinada.png"

WIDTH, HEIGHT = 1080, 1350
INK = (5, 10, 17)
WHITE = (245, 245, 241)
GOLD = (222, 163, 82)
PALE_GOLD = (242, 205, 151)
BLUE = (91, 170, 227)
ORANGE = (241, 124, 52)
VIOLET = (159, 123, 225)

FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def fit_font(text: str, max_width: int, start_size: int, min_size: int = 44):
    for size in range(start_size, min_size - 1, -2):
        font = ImageFont.truetype(FONT_BOLD, size)
        if ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(text, font=font) <= max_width:
            return font
    return ImageFont.truetype(FONT_BOLD, min_size)


def centered_lines(draw, text, top, font, fill, spacing=12, max_width=850):
    words = text.split()
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and draw.textlength(candidate, font=font) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)

    heights = []
    for line in lines:
        box = draw.textbbox((0, 0), line, font=font)
        heights.append(box[3] - box[1])
    total = sum(heights) + spacing * (len(lines) - 1)
    y = top
    for line, height in zip(lines, heights):
        box = draw.textbbox((0, 0), line, font=font)
        x = (WIDTH - (box[2] - box[0])) // 2
        draw.text((x, y), line, font=font, fill=fill)
        y += height + spacing
    return y, total


def base_canvas(cover, accent, seed):
    random.seed(seed)
    bg = cover_crop(cover, (WIDTH, HEIGHT)).filter(ImageFilter.GaussianBlur(30))
    bg = ImageEnhance.Brightness(bg).enhance(0.20)
    bg = ImageEnhance.Color(bg).enhance(0.55).convert("RGBA")
    shade = Image.new("RGBA", (WIDTH, HEIGHT), (2, 7, 13, 168))
    canvas = Image.alpha_composite(bg, shade)

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    for radius in range(430, 30, -18):
        alpha = max(0, int(1.5 * (430 - radius)))
        alpha = min(alpha, 12)
        glow_draw.ellipse(
            (WIDTH // 2 - radius, 675 - radius, WIDTH // 2 + radius, 675 + radius),
            fill=(*accent, alpha),
        )
    glow = glow.filter(ImageFilter.GaussianBlur(48))
    canvas = Image.alpha_composite(canvas, glow)

    particles = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    pd = ImageDraw.Draw(particles)
    for _ in range(120):
        x = random.randint(45, WIDTH - 45)
        y = random.randint(170, HEIGHT - 100)
        r = random.choice([1, 1, 2, 2, 3])
        pd.ellipse((x-r, y-r, x+r, y+r), fill=(*accent, random.randint(30, 115)))
    particles = particles.filter(ImageFilter.GaussianBlur(0.35))
    return Image.alpha_composite(canvas, particles)


def draw_brand(draw, index, accent):
    brand = ImageFont.truetype(FONT_BOLD, 34)
    small = ImageFont.truetype(FONT_REGULAR, 26)
    draw.text((72, 54), "ARREAL", font=brand, fill=PALE_GOLD)
    marker = f"{index}/6"
    w = draw.textlength(marker, font=small)
    draw.text((WIDTH - 72 - w, 59), marker, font=small, fill=(*accent, 230))
    draw.line((72, 108, WIDTH - 72, 108), fill=(*accent, 95), width=2)


def draw_symbol(canvas, kind, accent):
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = WIDTH // 2, 565
    if kind == "question":
        font = ImageFont.truetype(FONT_BOLD, 300)
        text = "?"
        box = d.textbbox((0, 0), text, font=font)
        d.text((cx - (box[2]-box[0])//2, cy - 180), text, font=font, fill=(*accent, 115))
    elif kind == "invisibility":
        for i in range(7):
            offset = i * 13
            alpha = 100 - i * 11
            d.ellipse((cx-132+offset, cy-180, cx+132+offset, cy+84), outline=(*accent, alpha), width=5)
            d.rounded_rectangle((cx-180+offset, cy+62, cx+180+offset, cy+320), radius=105, outline=(*accent, alpha), width=5)
    elif kind == "strength":
        for radius in (72, 125, 182):
            d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=(*accent, 110), width=5)
        d.line((cx, cy-245, cx, cy+245), fill=(*accent, 165), width=12)
        d.line((cx-245, cy, cx+245, cy), fill=(*accent, 165), width=12)
    elif kind == "fire":
        pts = [(cx, cy-235), (cx+78, cy-86), (cx+42, cy-42), (cx+130, cy+65),
               (cx+52, cy+235), (cx, cy+270), (cx-62, cy+220), (cx-126, cy+70),
               (cx-52, cy-40), (cx-82, cy-100)]
        d.polygon(pts, fill=(*accent, 105), outline=(*accent, 205))
        d.polygon([(cx, cy-75), (cx+42, cy+30), (cx+17, cy+165), (cx-45, cy+65)], fill=(*PALE_GOLD, 130))
    elif kind == "flight":
        d.arc((cx-330, cy-210, cx+20, cy+245), 205, 335, fill=(*accent, 185), width=12)
        d.arc((cx-20, cy-210, cx+330, cy+245), 205, 335, fill=(*accent, 185), width=12)
        d.ellipse((cx-28, cy-70, cx+28, cy-14), fill=(*accent, 210))
        d.line((cx, cy-12, cx, cy+155), fill=(*accent, 210), width=11)
        d.line((cx, cy+45, cx-80, cy+110), fill=(*accent, 210), width=10)
        d.line((cx, cy+45, cx+80, cy+110), fill=(*accent, 210), width=10)
    elif kind == "choice":
        for angle in (0, math.pi/2, math.pi, 3*math.pi/2):
            x2 = cx + int(math.cos(angle) * 225)
            y2 = cy + int(math.sin(angle) * 225)
            d.line((cx, cy, x2, y2), fill=(*accent, 175), width=8)
            d.ellipse((x2-22, y2-22, x2+22, y2+22), fill=(*accent, 205))
        d.ellipse((cx-34, cy-34, cx+34, cy+34), fill=(*PALE_GOLD, 230))
    return Image.alpha_composite(canvas, layer.filter(ImageFilter.GaussianBlur(0.25)))


slides = [
    {
        "accent": GOLD,
        "symbol": "question",
        "eyebrow": "UMA PERGUNTA PARA VOCÊ",
        "title": "SE UMA EMOÇÃO SUA PUDESSE DESPERTAR UM PODER…",
        "answer": "QUAL SERIA?",
    },
    {
        "accent": BLUE,
        "symbol": "invisibility",
        "eyebrow": "1  •  DESEJO DE DESAPARECER",
        "title": "INVISIBILIDADE",
        "answer": "SUMIR QUANDO O MUNDO PESA DEMAIS.",
    },
    {
        "accent": GOLD,
        "symbol": "strength",
        "eyebrow": "2  •  PRECISAR PROTEGER ALGUÉM",
        "title": "FORÇA",
        "answer": "MOVER O IMPOSSÍVEL QUANDO ALGUÉM PRECISA DE VOCÊ.",
    },
    {
        "accent": ORANGE,
        "symbol": "fire",
        "eyebrow": "3  •  RAIVA QUE NÃO CABE MAIS",
        "title": "FOGO",
        "answer": "TRANSFORMAR EM CHAMA AQUILO QUE VOCÊ NÃO CONSEGUE DIZER.",
    },
    {
        "accent": VIOLET,
        "symbol": "flight",
        "eyebrow": "4  •  VONTADE DE ESCAPAR DE TUDO",
        "title": "VOO",
        "answer": "IR PARA LONGE ANTES QUE ALGO POSSA PRENDER VOCÊ.",
    },
    {
        "accent": GOLD,
        "symbol": "choice",
        "eyebrow": "AGORA É COM VOCÊ",
        "title": "QUAL PODER DESPERTARIA EM VOCÊ?",
        "answer": "COMENTE 1, 2, 3 OU 4 — E O PORQUÊ.",
    },
]


OUT_DIR.mkdir(parents=True, exist_ok=True)
cover = Image.open(COVER_PATH).convert("RGB")
preview_thumbs = []

for index, spec in enumerate(slides, start=1):
    accent = spec["accent"]
    canvas = base_canvas(cover, accent, 100 + index)
    canvas = draw_symbol(canvas, spec["symbol"], accent)
    draw = ImageDraw.Draw(canvas)
    draw_brand(draw, index, accent)

    eyebrow_font = fit_font(spec["eyebrow"], 820, 35, 28)
    eyebrow_w = draw.textlength(spec["eyebrow"], font=eyebrow_font)
    draw.text(((WIDTH-eyebrow_w)/2, 170), spec["eyebrow"], font=eyebrow_font, fill=(*accent, 245))

    title_font = ImageFont.truetype(FONT_BOLD, 76 if index not in (1, 6) else 68)
    centered_lines(draw, spec["title"], 880, title_font, WHITE, spacing=6, max_width=860)

    answer_font = ImageFont.truetype(FONT_REGULAR, 38 if index not in (1, 6) else 42)
    centered_lines(draw, spec["answer"], 1102, answer_font, PALE_GOLD, spacing=7, max_width=810)

    draw.line((200, 1270, WIDTH-200, 1270), fill=(*accent, 110), width=2)
    footer = "FANTASIA BRASILEIRA  •  DISPONÍVEL NO KINDLE"
    footer_font = ImageFont.truetype(FONT_REGULAR, 24)
    footer_w = draw.textlength(footer, font=footer_font)
    draw.text(((WIDTH-footer_w)/2, 1292), footer, font=footer_font, fill=(218, 220, 221, 190))

    out = OUT_DIR / f"{index:02d}.png"
    canvas.convert("RGB").save(out, quality=96, subsampling=0)
    preview_thumbs.append(canvas.convert("RGB").resize((270, 338), Image.Resampling.LANCZOS))

preview = Image.new("RGB", (3*270 + 4*28, 2*338 + 3*28), INK)
for i, thumb in enumerate(preview_thumbs):
    col, row = i % 3, i // 3
    preview.paste(thumb, (28 + col*(270+28), 28 + row*(338+28)))
preview.save(OUT_DIR / "preview.jpg", quality=92, subsampling=0)

