from io import BytesIO
from pathlib import Path

from PIL import Image, ImageCms, ImageOps
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "output/fabrica-do-livro/templates/marcador_de_pagina_5x18cm.pdf"
FRONT = ROOT / "output/marketing/marcadores/04_marcador_capa.png"
BACK = ROOT / "output/marketing/marcadores/final/marcador_arreal_verso.png"
OUTPUT = ROOT / "output/pdf/Arreal_Marcador_5x18cm_Frente_Verso.pdf"
TMP = ROOT / "tmp/pdfs/marcador-final"

SRGB_PROFILE = Path("/System/Library/ColorSync/Profiles/sRGB Profile.icc")
CMYK_PROFILE = Path("/System/Library/ColorSync/Profiles/Generic CMYK Profile.icc")


def prepare_image(source: Path, destination: Path, width_px: int, height_px: int) -> None:
    image = Image.open(source).convert("RGB")
    # O template é horizontal (18 x 5 cm); as artes foram compostas na orientação vertical.
    image = image.rotate(-90, expand=True)
    image = ImageOps.fit(
        image,
        (width_px, height_px),
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    )
    image = ImageCms.profileToProfile(
        image,
        str(SRGB_PROFILE),
        str(CMYK_PROFILE),
        outputMode="CMYK",
    )
    image.save(destination, format="JPEG", quality=97, subsampling=0, dpi=(300, 300))


def build_overlay(page_width: float, page_height: float, images: list[Path]) -> PdfReader:
    stream = BytesIO()
    pdf = canvas.Canvas(stream, pagesize=(page_width, page_height), pageCompression=1)
    for image in images:
        pdf.drawImage(
            ImageReader(str(image)),
            0,
            0,
            width=page_width,
            height=page_height,
            preserveAspectRatio=False,
            mask=None,
        )
        pdf.showPage()
    pdf.save()
    stream.seek(0)
    return PdfReader(stream)


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    template = PdfReader(str(TEMPLATE))
    if len(template.pages) != 2:
        raise ValueError(f"O template deve ter 2 páginas; encontrado: {len(template.pages)}")

    first_page = template.pages[0]
    page_width = float(first_page.mediabox.width)
    page_height = float(first_page.mediabox.height)
    width_px = round(page_width / 72 * 300)
    height_px = round(page_height / 72 * 300)

    front_print = TMP / "frente_cmyk_300dpi.jpg"
    back_print = TMP / "verso_cmyk_300dpi.jpg"
    prepare_image(FRONT, front_print, width_px, height_px)
    prepare_image(BACK, back_print, width_px, height_px)

    overlay = build_overlay(page_width, page_height, [front_print, back_print])

    writer = PdfWriter()
    writer.clone_document_from_reader(template)
    for index in range(2):
        writer.pages[index].merge_page(overlay.pages[index], over=True)

    writer.add_metadata(
        {
            "/Title": "Arreal - Marcador de página 5x18 cm - Frente e verso",
            "/Author": "Bruno Duarte Corrêa",
            "/Subject": "Arquivo de impressão baseado no template da Fábrica do Livro",
        }
    )
    with OUTPUT.open("wb") as stream:
        writer.write(stream)

    # Reabre para detectar qualquer falha estrutural de gravação.
    check = PdfReader(str(OUTPUT))
    if len(check.pages) != 2:
        raise ValueError("O PDF final não contém exatamente duas páginas.")
    for page in check.pages:
        if float(page.mediabox.width) != page_width or float(page.mediabox.height) != page_height:
            raise ValueError("As dimensões do PDF final diferem do template.")

    print(OUTPUT)
    print(f"page_size_pt={page_width:.3f}x{page_height:.3f}")
    print(f"raster_size_px={width_px}x{height_px}")


if __name__ == "__main__":
    main()
