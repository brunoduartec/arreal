#!/usr/bin/env python3
"""Gera um clipe local de Arreal usando somente imagens autorizadas."""

from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path


LOCAL_VIDEO_DIR = Path(__file__).resolve().parent
PROJECT_DIR = LOCAL_VIDEO_DIR.parent
PYTHON = LOCAL_VIDEO_DIR / ".venv" / "bin" / "python"
MODEL_DIR = LOCAL_VIDEO_DIR / "models" / "Wan2.2-TI2V-5B-MLX-Q8"
OUTPUT_DIR = PROJECT_DIR / "output" / "marketing" / "videos_locais"
AUTHORIZED_DIRS = (
    (PROJECT_DIR / "images").resolve(),
    (PROJECT_DIR / "output" / "marketing").resolve(),
)

PRESETS = {
    # Primeiro teste: pequeno para confirmar que tudo funciona sem pressionar a memoria.
    "teste": {"width": 320, "height": 576, "frames": 17, "steps": 6},
    # Aproximadamente 1,4 s; bom para experimentar movimento e prompt.
    "curto": {"width": 384, "height": 672, "frames": 33, "steps": 12},
    # Aproximadamente 2 s em 9:16. Use somente depois de aprovar o teste.
    "social": {"width": 576, "height": 1024, "frames": 49, "steps": 20},
}

IDENTITY_GUARD = (
    " Use the supplied image as the exact visual identity and first frame."
    " Preserve the same character, facial structure, hair, clothing, age, body proportions,"
    " painterly illustration style, colors, lighting and environment throughout the entire shot."
    " Only subtle natural motion. No transformation, no gender change, no costume change,"
    " no new people, no duplicate character, no mirrored composition, no reversed reflection,"
    " no text, no logo and no scene replacement."
)


def authorized_image(raw_path: str) -> Path:
    image = Path(raw_path).expanduser()
    if not image.is_absolute():
        image = PROJECT_DIR / image
    image = image.resolve()

    if not image.is_file():
        raise argparse.ArgumentTypeError(f"Imagem nao encontrada: {image}")
    if image.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
        raise argparse.ArgumentTypeError("Use uma imagem PNG, JPG, JPEG ou WEBP.")
    if not any(image.is_relative_to(folder) for folder in AUTHORIZED_DIRS):
        allowed = " ou ".join(str(folder) for folder in AUTHORIZED_DIRS)
        raise argparse.ArgumentTypeError(
            f"Imagem recusada. Ela precisa estar dentro de {allowed}."
        )
    return image


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera video local preservando as referencias visuais de Arreal."
    )
    parser.add_argument("--imagem", required=True, type=authorized_image)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--preset", choices=PRESETS, default="teste")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--saida", help="Nome do MP4; por padrao usa data e nome da imagem.")
    parser.add_argument(
        "--executar",
        action="store_true",
        help="Executa a geracao. Sem esta opcao, apenas mostra e valida o comando.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    preset = PRESETS[args.preset]

    if not PYTHON.is_file():
        sys.exit(f"Ambiente nao encontrado: {PYTHON}")
    required = ("config.json", "model.safetensors", "t5_encoder.safetensors", "vae.safetensors")
    missing = [name for name in required if not (MODEL_DIR / name).is_file()]
    if missing:
        sys.exit("Modelo incompleto. Arquivos ausentes: " + ", ".join(missing))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_name = args.saida or (
        f"{datetime.now():%Y%m%d_%H%M%S}_{args.imagem.stem}_{args.preset}.mp4"
    )
    if not output_name.lower().endswith(".mp4"):
        output_name += ".mp4"
    output = (OUTPUT_DIR / Path(output_name).name).resolve()

    command = [
        str(PYTHON),
        "-m",
        "mlx_video.models.wan_2.generate",
        "--model-dir",
        str(MODEL_DIR),
        "--image",
        str(args.imagem),
        "--prompt",
        args.prompt.strip() + IDENTITY_GUARD,
        "--width",
        str(preset["width"]),
        "--height",
        str(preset["height"]),
        "--num-frames",
        str(preset["frames"]),
        "--steps",
        str(preset["steps"]),
        "--guide-scale",
        "5.0",
        "--seed",
        str(args.seed),
        "--tiling",
        "aggressive",
        "--output-path",
        str(output),
    ]

    print("Imagem autorizada:", args.imagem)
    print("Preset:", args.preset, preset)
    print("Saida:", output)
    if not args.executar:
        print("Validacao concluida. Acrescente --executar para iniciar a geracao.")
        return 0

    print("Iniciando geracao local. O Mac pode ficar lento durante o processamento.")
    subprocess.run(command, cwd=LOCAL_VIDEO_DIR, check=True)
    print("Video criado:", output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
