#!/usr/bin/env python3
"""Build a clean EPUB 3 edition of Arreal from the canonical LaTeX chapters."""

from __future__ import annotations

import html
import re
import shutil
import uuid
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "tmp" / "epub-build"
OEBPS = BUILD / "OEBPS"
OUTPUT = ROOT / "output" / "kdp" / "Arreal_Kindle.epub"

CHAPTERS = [
    "0", "1", "2-3", "4-5", "6", "7", "8", "8-1", "9", "10", "11",
    "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22",
    "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33",
    "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45",
]

TITLE = "Arreal"
AUTHOR = "Bruno Duarte Corrêa"
LANG = "pt-BR"
BOOK_ID = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'arreal-bruno-duarte-correa-2026')}"


def strip_conditionals(text: str) -> str:
    pattern = re.compile(
        r"\\ifdefined\\useChapters\s*(.*?)\s*\\else\s*.*?\s*\\fi",
        re.DOTALL,
    )
    return pattern.sub(lambda match: match.group(1), text)


def inline_tex(text: str) -> str:
    text = html.escape(text.strip(), quote=False)
    text = text.replace("$\\ast$~$\\ast$~$\\ast$", "* * *")
    text = text.replace("$\\ast$", "*")
    text = text.replace("~", " ")
    text = text.replace("\\noindent", "")

    macros = (("emph", "em"), ("textit", "em"), ("textbf", "strong"))
    for _ in range(6):
        previous = text
        for macro, tag in macros:
            text = re.sub(
                rf"\\{macro}\{{([^{{}}]*)\}}",
                rf"<{tag}>\1</{tag}>",
                text,
            )
        if text == previous:
            break

    text = text.replace("\\\\", "<br />")
    text = re.sub(r"\\(?:color|pagecolor)\{[^{}]*\}", "", text)
    text = re.sub(r"\\[A-Za-z@]+\*?", "", text)
    text = text.replace("{", "").replace("}", "")
    return re.sub(r"\s+", " ", text).strip()


def render_center(content: str) -> str:
    pieces = []
    for paragraph in re.split(r"\n\s*\n", content.strip()):
        value = inline_tex(" ".join(line.strip() for line in paragraph.splitlines()))
        if value:
            pieces.append(value)
    return '<div class="scene">' + "<br />".join(pieces) + "</div>"


def render_quote(content: str) -> str:
    value = inline_tex(" ".join(line.strip() for line in content.splitlines()))
    return f"<blockquote>{value}</blockquote>" if value else ""


def render_itemize(content: str) -> str:
    items = re.split(r"\\item\s*", content)
    values = [inline_tex(" ".join(item.splitlines())) for item in items[1:]]
    values = [value for value in values if value]
    return "<ul>" + "".join(f"<li>{value}</li>" for value in values) + "</ul>"


def extract_environment(text: str, name: str, renderer, stored: dict[str, str]) -> str:
    pattern = re.compile(
        rf"\\begin\{{{name}\}}(.*?)\\end\{{{name}\}}",
        re.DOTALL,
    )

    def replace(match: re.Match[str]) -> str:
        key = f"@@BLOCK{len(stored)}@@"
        stored[key] = renderer(match.group(1))
        return f"\n\n{key}\n\n"

    return pattern.sub(replace, text)


def latex_to_body(source: str) -> tuple[str, str]:
    text = source.replace("\r\n", "\n")
    text = re.sub(r"(?m)^\s*%.*$", "", text)
    text = strip_conditionals(text)

    # Preserve the final sentence positioned through TikZ in the print edition.
    text = re.sub(
        r"\\begin\{tikzpicture\}.*?\\node.*?\{([^{}]+)\};.*?\\end\{tikzpicture\}",
        r"\n\n\1\n\n",
        text,
        flags=re.DOTALL,
    )

    title_match = re.search(r"\\chapter\*?\{([^{}]+)\}", text)
    title = inline_tex(title_match.group(1)) if title_match else ""
    text = re.sub(r"\\chapter\*?\{[^{}]*\}", "", text)
    text = re.sub(r"\\addcontentsline\{[^{}]*\}\{[^{}]*\}\{[^{}]*\}", "", text)
    text = text.replace("\\newpage", "")

    stored: dict[str, str] = {}
    text = extract_environment(text, "center", render_center, stored)
    text = extract_environment(text, "quote", render_quote, stored)
    text = extract_environment(text, "itemize", render_itemize, stored)

    def heading(level: int, match: re.Match[str]) -> str:
        key = f"@@BLOCK{len(stored)}@@"
        stored[key] = f"<h{level}>{inline_tex(match.group(1))}</h{level}>"
        return f"\n\n{key}\n\n"

    text = re.sub(r"\\section\*?\{([^{}]+)\}", lambda m: heading(2, m), text)
    text = re.sub(r"\\subsection\*?\{([^{}]+)\}", lambda m: heading(3, m), text)
    text = re.sub(r"\\(?:medskip|bigskip)", "\n\n@@SPACE@@\n\n", text)
    text = re.sub(r"\\(?:begin|end)\{[^{}]+\}", "", text)

    blocks: list[str] = []
    last_space = False
    for raw in re.split(r"\n\s*\n", text):
        raw = raw.strip()
        if not raw:
            continue
        if raw in stored:
            value = stored[raw]
            if value:
                blocks.append(value)
            last_space = False
            continue
        if raw == "@@SPACE@@":
            if not last_space:
                blocks.append('<div class="breath" aria-hidden="true"></div>')
            last_space = True
            continue

        value = inline_tex(" ".join(line.strip() for line in raw.splitlines()))
        if value:
            if value == "* * *":
                blocks.append('<div class="scene">* * *</div>')
            else:
                blocks.append(f"<p>{value}</p>")
            last_space = False

    return title, "\n".join(blocks)


def xhtml_document(title: str, body: str, body_class: str = "chapter") -> str:
    return f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{LANG}" xml:lang="{LANG}">
<head>
  <meta charset="utf-8" />
  <title>{html.escape(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles.css" />
</head>
<body class="{body_class}">
{body}
</body>
</html>
'''


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def dedication_text() -> str:
    source = (ROOT / "chapters" / "dedicatoria.tex").read_text(encoding="utf-8")
    match = re.search(
        r"\\itshape\s*(.*?)\s*\\end\{flushleft\}",
        source,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError("Não foi possível extrair a dedicatória de chapters/dedicatoria.tex")
    return inline_tex(match.group(1))


def build() -> None:
    if BUILD.exists():
        shutil.rmtree(BUILD)
    OEBPS.mkdir(parents=True)
    (BUILD / "META-INF").mkdir(parents=True)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    write_text(BUILD / "mimetype", "application/epub+zip")
    write_text(
        BUILD / "META-INF" / "container.xml",
        '''<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
''',
    )

    styles = '''
html { -webkit-text-size-adjust: 100%; }
body { font-family: serif; line-height: 1.45; margin: 5%; text-align: justify; }
p { margin: 0; text-indent: 1.2em; }
h1 { font-style: italic; font-weight: normal; text-align: left; margin: 22% 0 3em; page-break-before: always; break-before: page; }
h2 { font-style: italic; font-weight: normal; margin: 1.6em 0 0.6em; }
h3 { font-style: italic; font-weight: normal; margin: 1.2em 0 0.4em; }
.title-page { text-align: center; padding-top: 30%; }
.title-page h1 { font-family: sans-serif; font-style: normal; font-weight: bold; margin: 0 0 2em; letter-spacing: 0.12em; }
.title-page p, .copyright p { text-indent: 0; text-align: center; margin: 0.8em 0; }
.copyright { padding-top: 28%; }
.dedication { padding-top: 65%; text-align: left; font-style: italic; }
.dedication p { text-indent: 0; }
.scene { text-align: center; text-indent: 0; margin: 1.6em 0; font-style: italic; }
.breath { height: 1.2em; }
blockquote { margin: 1.2em 8%; font-style: italic; }
ul { margin: 1em 0 1em 1.2em; padding: 0; }
li { margin: 0.7em 0; }
'''.strip()
    write_text(OEBPS / "styles.css", styles)

    title_body = f'''<div class="title-page" epub:type="titlepage">
  <h1>{TITLE.upper()}</h1>
  <p>{AUTHOR}</p>
</div>'''
    write_text(OEBPS / "title.xhtml", xhtml_document(TITLE, title_body, "title-page"))

    copyright_body = '''<div class="copyright">
  <p>Copyright © 2026 Bruno Duarte Corrêa</p>
  <p>Todos os direitos reservados.</p>
  <p>Primeira edição, 2026.<br />Brasil.</p>
</div>'''
    write_text(OEBPS / "copyright.xhtml", xhtml_document("Direitos autorais", copyright_body, "copyright"))

    dedication_body = f'''<div class="dedication" epub:type="dedication">
  <p>{dedication_text()}</p>
</div>'''
    write_text(
        OEBPS / "dedication.xhtml",
        xhtml_document("Dedicatória", dedication_body, "dedication"),
    )

    entries: list[tuple[str, str, str]] = []
    for index, chapter in enumerate(CHAPTERS, start=1):
        source = (ROOT / "chapters" / f"chapter{chapter}.tex").read_text(encoding="utf-8")
        chapter_title, body = latex_to_body(source)
        filename = f"chapter-{index:02d}.xhtml"
        content = f"<h1>{chapter_title}</h1>\n{body}"
        write_text(OEBPS / filename, xhtml_document(chapter_title, content))
        entries.append((f"chapter{index:02d}", filename, chapter_title))

    for item_id, filename, path in (
        ("appendix", "appendix.xhtml", ROOT / "chapters" / "habilidades.tex"),
        ("authornote", "author-note.xhtml", ROOT / "chapters" / "nota_autor.tex"),
    ):
        section_title, body = latex_to_body(path.read_text(encoding="utf-8"))
        write_text(
            OEBPS / filename,
            xhtml_document(section_title, f"<h1>{section_title}</h1>\n{body}"),
        )
        entries.append((item_id, filename, section_title))

    nav_items = "\n".join(
        f'      <li><a href="{filename}">{html.escape(label)}</a></li>'
        for _, filename, label in entries
    )
    nav = f'''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{LANG}" xml:lang="{LANG}">
<head><meta charset="utf-8" /><title>Sumário</title><link rel="stylesheet" type="text/css" href="styles.css" /></head>
<body>
  <nav epub:type="toc" id="toc"><h1>Sumário</h1><ol>
{nav_items}
  </ol></nav>
  <nav epub:type="landmarks" hidden="hidden"><ol>
    <li><a epub:type="titlepage" href="title.xhtml">Folha de rosto</a></li>
    <li><a epub:type="bodymatter" href="chapter-01.xhtml">Início</a></li>
  </ol></nav>
</body>
</html>
'''
    write_text(OEBPS / "nav.xhtml", nav)

    manifest_entries = [
        '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
        '<item id="css" href="styles.css" media-type="text/css" />',
        '<item id="title" href="title.xhtml" media-type="application/xhtml+xml" />',
        '<item id="copyright" href="copyright.xhtml" media-type="application/xhtml+xml" />',
        '<item id="dedication" href="dedication.xhtml" media-type="application/xhtml+xml" />',
    ]
    manifest_entries.extend(
        f'<item id="{item_id}" href="{filename}" media-type="application/xhtml+xml" />'
        for item_id, filename, _ in entries
    )
    spine_entries = [
        '<itemref idref="title" />',
        '<itemref idref="copyright" />',
        '<itemref idref="dedication" />',
    ]
    spine_entries.extend(f'<itemref idref="{item_id}" />' for item_id, _, _ in entries)

    opf = f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{LANG}">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">{BOOK_ID}</dc:identifier>
    <dc:title>{TITLE}</dc:title>
    <dc:creator id="creator">{AUTHOR}</dc:creator>
    <meta refines="#creator" property="role" scheme="marc:relators">aut</meta>
    <dc:language>{LANG}</dc:language>
    <dc:rights>Copyright © 2026 Bruno Duarte Corrêa. Todos os direitos reservados.</dc:rights>
    <meta property="dcterms:modified">2026-07-25T12:00:00Z</meta>
  </metadata>
  <manifest>
    {chr(10).join(manifest_entries)}
  </manifest>
  <spine>
    {chr(10).join(spine_entries)}
  </spine>
</package>
'''
    write_text(OEBPS / "content.opf", opf)

    if OUTPUT.exists():
        OUTPUT.unlink()
    with zipfile.ZipFile(OUTPUT, "w") as archive:
        archive.write(BUILD / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(BUILD.rglob("*")):
            if path.is_file() and path.name != "mimetype":
                archive.write(path, path.relative_to(BUILD), compress_type=zipfile.ZIP_DEFLATED)

    print(f"Generated {OUTPUT}")
    print(f"Chapters: {len(CHAPTERS)}; additional sections: 2")


if __name__ == "__main__":
    build()
