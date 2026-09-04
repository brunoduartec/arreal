from pathlib import Path

from pypdf import PdfReader, PdfWriter

from build_bookmark_pdf import FRONT, ROOT, TEMPLATE, build_overlay, prepare_image


OUTPUT = ROOT / "output/pdf/Arreal_Marcador_5x18cm_Somente_Frente.pdf"
TMP = ROOT / "tmp/pdfs/marcador-somente-frente"


def main() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    template = PdfReader(str(TEMPLATE))
    if len(template.pages) < 1:
        raise ValueError("O template não contém a página da frente.")

    template_front = template.pages[0]
    page_width = float(template_front.mediabox.width)
    page_height = float(template_front.mediabox.height)
    width_px = round(page_width / 72 * 300)
    height_px = round(page_height / 72 * 300)

    front_print = TMP / "frente_cmyk_300dpi.jpg"
    prepare_image(FRONT, front_print, width_px, height_px)
    overlay = build_overlay(page_width, page_height, [front_print])

    writer = PdfWriter()
    writer.clone_document_from_reader(template)
    while len(writer.pages) > 1:
        writer.remove_page(len(writer.pages) - 1)
    writer.pages[0].merge_page(overlay.pages[0], over=True)

    writer.add_metadata(
        {
            "/Title": "Arreal - Marcador de página 5x18 cm - Somente frente",
            "/Author": "Bruno Duarte Corrêa",
            "/Subject": "Arquivo de impressão com somente a frente, baseado no template da Fábrica do Livro",
        }
    )
    with OUTPUT.open("wb") as stream:
        writer.write(stream)

    check = PdfReader(str(OUTPUT))
    if len(check.pages) != 1:
        raise ValueError("O PDF final deve conter exatamente uma página.")
    page = check.pages[0]
    if float(page.mediabox.width) != page_width or float(page.mediabox.height) != page_height:
        raise ValueError("As dimensões do PDF final diferem do template.")

    print(OUTPUT)
    print(f"pages={len(check.pages)}")
    print(f"page_size_pt={page_width:.3f}x{page_height:.3f}")
    print(f"raster_size_px={width_px}x{height_px}")


if __name__ == "__main__":
    main()
