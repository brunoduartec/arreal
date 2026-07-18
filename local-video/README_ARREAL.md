# Geracao local de videos de Arreal

Esta pasta usa `Blaizzy/mlx-video` com o modelo Wan 2.2 TI2V 5B convertido para
MLX. O gerador foi configurado para aceitar referencias somente destas pastas:

- `images/`
- `output/marketing/`

Qualquer imagem localizada fora delas e recusada antes da geracao. Os videos sao
salvos em `output/marketing/videos_locais/`.

## Gerar o primeiro teste

No Terminal, entre na pasta raiz do projeto e execute:

```bash
local-video/.venv/bin/python local-video/generate_arreal.py \
  --imagem "images/larissa.png" \
  --prompt "Larissa remains still while restrained flames flicker gently around her hands; a very slow cinematic camera push-in; tense psychological fantasy atmosphere" \
  --preset teste \
  --saida "teste_larissa.mp4" \
  --executar
```

Retire `--executar` para apenas validar a imagem, o modelo e os parametros sem
processar o video.

## Presets

- `teste`: 320 x 576, 17 quadros, 6 etapas. Sempre use primeiro.
- `curto`: 384 x 672, 33 quadros, 12 etapas.
- `social`: 576 x 1024, 49 quadros, 20 etapas. Exige mais memoria e tempo.

O modelo produz 24 quadros por segundo. Os clipes curtos devem ser unidos no
CapCut ou outro editor para formar o video promocional completo.

## Regras para preservar os personagens

- Use uma unica imagem de referencia por clipe.
- Descreva movimentos pequenos e objetivos.
- Evite transformacoes, dialogos, rotacoes corporais completas e contato fisico
  complexo entre personagens.
- Gere cada personagem ou habilidade em um clipe separado.
- Use sempre `teste` antes de aumentar a resolucao.

## Atualizar o codigo

O repositorio original esta em `local-video/mlx-video`. Para atualizar no futuro:

```bash
git -C local-video/mlx-video pull --ff-only
local-video/.venv/bin/python -m pip install -e local-video/mlx-video
```

O ambiente virtual, o modelo e os videos locais nao precisam ser enviados para
um repositorio Git.
