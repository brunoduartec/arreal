from __future__ import annotations

from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BACKGROUND = Path(__file__).with_name("fundo-abstrato-imagegen.png")
W, H = 1080, 1350

INK = "#061321"
PAPER = "#F1EEE7"
GOLD = "#E7AA45"
GOLD_SOFT = "#F0C47E"
TEAL = "#39B6B3"
MUTED = "#B8C3C8"

FONT_DISPLAY = "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf"
FONT_BODY = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"
FONT_BODY_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"


SLIDES = [
    {
        "title": ["POR QUE ALGUNS", "PERSONAGENS PARECEM", "TÃO FAMILIARES?"],
        "accent": 2,
        "body": "A resposta pode estar nos arquétipos.",
        "note": "DESLIZE PARA DESCOBRIR",
        "icon": "rings",
        "art": "capa-impacto-imagegen.png",
        "footer": "ARQUÉTIPOS · 01  →",
    },
    {
        "title": ["ARQUÉTIPOS NÃO SÃO", "PERSONAGENS PRONTOS."],
        "accent": 0,
        "body": "São padrões recorrentes de desejo, medo e função narrativa.",
        "note": "Eles ajudam a reconhecer forças que atravessam histórias diferentes.",
        "icon": "pattern",
    },
    {
        "title": ["O HERÓI"],
        "accent": 0,
        "body": "Cruza um limite, enfrenta o desconhecido e é transformado pela jornada.",
        "note": "Não precisa ser perfeito. Precisa aceitar o movimento.",
        "icon": "hero",
        "art": "personagem-heroi-imagegen.png",
    },
    {
        "title": ["O MENTOR"],
        "accent": 0,
        "body": "Oferece direção, conhecimento ou o impulso que faltava para seguir.",
        "note": "Às vezes guia. Às vezes testa.",
        "icon": "mentor",
        "art": "personagem-mentor-imagegen.png",
    },
    {
        "title": ["A SOMBRA"],
        "accent": 0,
        "body": "Dá forma ao que o protagonista teme, rejeita ou ainda não reconhece em si.",
        "note": "Nem sempre é o vilão.",
        "icon": "shadow",
        "art": "personagem-sombra-imagegen.png",
    },
    {
        "title": ["MAS ELES NÃO SÃO", "CAIXAS."],
        "accent": 1,
        "body": "Um personagem pode reunir vários arquétipos — e mudar de função ao longo da história.",
        "note": "Arquétipo é uma lente, não uma sentença.",
        "icon": "overlap",
    },
    {
        "title": ["QUAL ARQUÉTIPO", "MAIS PRENDE VOCÊ", "NUMA HISTÓRIA?"],
        "accent": 2,
        "body": "Herói, mentor, sombra… ou outro?",
        "note": "Nos próximos posts, vou mostrar como alguns aparecem em ARREAL — sem spoilers.",
        "icon": "question",
        "footer": "CONTE NOS COMENTÁRIOS  ↓",
    },
]


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def fit_background() -> Image.Image:
    bg = Image.open(BACKGROUND).convert("RGB")
    scale = max(W / bg.width, H / bg.height)
    bg = bg.resize((round(bg.width * scale), round(bg.height * scale)), Image.Resampling.LANCZOS)
    left = (bg.width - W) // 2
    top = (bg.height - H) // 2
    bg = bg.crop((left, top, left + W, top + H))
    bg = ImageEnhance.Brightness(bg).enhance(0.78)
    bg = ImageEnhance.Contrast(bg).enhance(1.08)
    return bg


def fit_character_art(filename: str) -> Image.Image:
    art = Image.open(Path(__file__).with_name(filename)).convert("RGB")
    scale = max(W / art.width, H / art.height)
    art = art.resize((round(art.width * scale), round(art.height * scale)), Image.Resampling.LANCZOS)
    left = (art.width - W) // 2
    top = (art.height - H) // 2
    art = art.crop((left, top, left + W, top + H))
    art = ImageEnhance.Brightness(art).enhance(0.78)
    art = ImageEnhance.Contrast(art).enhance(1.07).convert("RGBA")

    # Preserve the figure while protecting the left and lower text fields.
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pixels = shade.load()
    for y in range(H):
        for x in range(W):
            left_alpha = int(195 * max(0.0, min(1.0, (700 - x) / 520)))
            bottom_alpha = int(150 * max(0.0, min(1.0, (y - 760) / 360)))
            pixels[x, y] = (2, 12, 22, max(left_alpha, bottom_alpha))
    return Image.alpha_composite(art, shade).convert("RGB")


def draw_header(draw: ImageDraw.ImageDraw, index: int) -> None:
    draw.rounded_rectangle((58, 62, 178, 69), radius=3, fill=GOLD)
    draw.text((58, 88), "BRUNO DUARTE CORRÊA", font=font(FONT_BODY_BOLD, 25), fill=PAPER)
    count = f"{index}/7"
    f = font(FONT_BODY_BOLD, 25)
    box = draw.textbbox((0, 0), count, font=f)
    draw.text((W - 58 - (box[2] - box[0]), 88), count, font=f, fill=GOLD)


def multiline(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], size: int,
              fill: str, width: int, spacing: int = 12, bold: bool = False) -> int:
    f = font(FONT_BODY_BOLD if bold else FONT_BODY, size)
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if draw.textbbox((0, 0), candidate, font=f)[2] <= width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    x, y = xy
    step = size + spacing
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += step
    return y


def icon(draw: ImageDraw.ImageDraw, kind: str, cx: int = 820, cy: int = 610) -> None:
    gold = GOLD_SOFT
    teal = TEAL
    if kind == "rings":
        for r, color, width in [(154, gold, 5), (112, teal, 4), (70, gold, 4)]:
            draw.arc((cx-r, cy-r, cx+r, cy+r), 208, 512, fill=color, width=width)
        draw.ellipse((cx-11, cy-11, cx+11, cy+11), fill=PAPER)
    elif kind == "pattern":
        for dx, dy, color in [(-64, -64, gold), (64, -64, teal), (-64, 64, teal), (64, 64, gold)]:
            draw.rounded_rectangle((cx+dx-58, cy+dy-58, cx+dx+58, cy+dy+58), 18, outline=color, width=4)
        draw.ellipse((cx-15, cy-15, cx+15, cy+15), fill=PAPER)
    elif kind == "hero":
        draw.ellipse((cx-128, cy-128, cx+128, cy+128), outline=gold, width=5)
        draw.line((cx, cy+82, cx, cy-62), fill=teal, width=7)
        draw.line((cx, cy-62, cx-42, cy-18), fill=teal, width=7)
        draw.line((cx, cy-62, cx+42, cy-18), fill=teal, width=7)
        draw.arc((cx-152, cy-152, cx+152, cy+152), 220, 310, fill=PAPER, width=3)
    elif kind == "mentor":
        draw.ellipse((cx-130, cy-130, cx+130, cy+130), outline=gold, width=4)
        for radius, color in [(100, teal), (46, PAPER)]:
            pts = [(cx, cy-radius), (cx+radius//3, cy-radius//3), (cx+radius, cy),
                   (cx+radius//3, cy+radius//3), (cx, cy+radius),
                   (cx-radius//3, cy+radius//3), (cx-radius, cy),
                   (cx-radius//3, cy-radius//3)]
            draw.polygon(pts, outline=color)
        draw.ellipse((cx-10, cy-10, cx+10, cy+10), fill=gold)
    elif kind == "shadow":
        box = (cx-128, cy-128, cx+128, cy+128)
        draw.pieslice(box, 90, 270, fill="#102837")
        draw.pieslice(box, 270, 90, fill=GOLD)
        draw.ellipse(box, outline=PAPER, width=4)
        draw.line((cx, cy-128, cx, cy+128), fill=TEAL, width=4)
    elif kind == "overlap":
        for dx, dy, color in [(-62, -28, gold), (62, -28, teal), (0, 64, PAPER)]:
            draw.ellipse((cx+dx-92, cy+dy-92, cx+dx+92, cy+dy+92), outline=color, width=5)
        draw.ellipse((cx-15, cy-15, cx+15, cy+15), fill=GOLD)
    elif kind == "question":
        f = font(FONT_DISPLAY, 310)
        bbox = draw.textbbox((0, 0), "?", font=f)
        draw.text((cx-(bbox[2]-bbox[0])//2, cy-(bbox[3]-bbox[1])//2-45), "?", font=f, fill=GOLD)
        draw.arc((cx-155, cy-155, cx+155, cy+155), 195, 515, fill=TEAL, width=4)


def render_slide(index: int, data: dict) -> None:
    if data.get("art"):
        img = fit_character_art(data["art"]).convert("RGBA")
    else:
        img = fit_background().convert("RGBA")
    veil = Image.new("RGBA", (W, H), (2, 12, 22, 45))
    img = Image.alpha_composite(img, veil)
    draw = ImageDraw.Draw(img)
    draw_header(draw, index)

    if not data.get("art"):
        icon(draw, data["icon"])

    is_cover = index == 1
    title_y = 752 if is_cover else 190
    title_size = 82 if is_cover else (94 if len(data["title"]) < 3 else 78)
    title_font = font(FONT_DISPLAY, title_size)
    for line_no, line in enumerate(data["title"]):
        fill = GOLD if line_no == data["accent"] else PAPER
        draw.text((58, title_y), line, font=title_font, fill=fill)
        title_y += 82 if is_cover else (92 if len(data["title"]) < 3 else 78)

    body_y = 1040 if is_cover else 875
    body_width = 860 if is_cover else (650 if data.get("art") else 820)
    body_size = 39 if is_cover else 48
    body_y = multiline(draw, data["body"], (58, body_y), body_size, PAPER, body_width, spacing=12, bold=True)
    draw.rounded_rectangle((58, body_y + 26, 122, body_y + 32), radius=3, fill=TEAL)
    multiline(draw, data["note"], (58, body_y + 55), 33, MUTED, 870, spacing=10)

    footer = data.get("footer", "ARQUÉTIPOS · UMA SÉRIE SOBRE PERSONAGENS")
    draw.text((58, 1284), footer, font=font(FONT_BODY_BOLD, 24), fill=GOLD_SOFT)

    out = ROOT / f"{index:02d}-arquetipos.png"
    img.convert("RGB").save(out, quality=96, optimize=True)


if __name__ == "__main__":
    ROOT.mkdir(parents=True, exist_ok=True)
    for idx, slide in enumerate(SLIDES, start=1):
        render_slide(idx, slide)
    print(f"Carrossel salvo em {ROOT}")
