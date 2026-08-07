#!/bin/zsh
set -euo pipefail

root_dir="$(cd "$(dirname "$0")/../../.." && pwd)"
carousel_dir="$root_dir/output/marketing/carrossel-leia-no-app-kindle"
source_dir="$carousel_dir/fontes"
cover_path="$root_dir/images/capa_kdp_refinada.png"
temp_cover="$source_dir/capa-compacta.png"

sips -Z 420 "$cover_path" --out "$temp_cover" >/dev/null
cover_data="$(base64 -b 0 -i "$temp_cover")"

for source_svg in "$source_dir/01-capa-final.svg" "$source_dir/02-voce-nao-precisa-do-aparelho.svg" "$source_dir/03-baixe-o-app.svg" "$source_dir/04-entre-e-comece-a-ler.svg" "$source_dir/05-pronto.svg"; do
  filename="${source_svg:t:r}"
  if [[ "$filename" == "01-capa-final" ]]; then
    filename="01-nao-tem-kindle"
  fi
  embedded_svg="$source_dir/${filename}-embutido.svg"
  output_png="$carousel_dir/${filename}.png"
  sed "s|BOOK_COVER_DATA_URI|data:image/png;base64,$cover_data|g" "$source_svg" > "$embedded_svg"
  sips -s format png "$embedded_svg" --out "$output_png" >/dev/null
  rm "$embedded_svg"
done
