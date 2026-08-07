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
- `qualidade`: 576 x 1024, 33 quadros, 30 etapas. Recomendado para publicar.
- `maxima`: 704 x 1280, 33 quadros, 40 etapas. Resolucao nativa do Wan 2.2;
  pode levar dezenas de minutos e deixar o Mac praticamente indisponivel.
- `maxima_3s`: 768 x 1152, 73 quadros, 40 etapas. Produz 3,04 segundos, usa a
  mesma proporcao 2:3 das artes originais e e o teto recomendado para o M4 Pro
  com 24 GB. Pode levar cerca de uma hora, dependendo da temperatura do Mac.

O modelo produz 24 quadros por segundo. Os clipes curtos devem ser unidos no
CapCut ou outro editor para formar o video promocional completo.

## Regras para preservar os personagens

- Use uma unica imagem de referencia por clipe.
- Descreva movimentos pequenos e objetivos. Para maior fidelidade, anime somente
  elementos que ja aparecem na imagem; nao peca ao modelo para criar fogo ou
  objetos novos.
- Evite transformacoes, dialogos, rotacoes corporais completas e contato fisico
  complexo entre personagens.
- Gere cada personagem ou habilidade em um clipe separado.
- Use `teste` apenas para validar se o pipeline funciona; sua resolucao e seu
  numero de etapas sao baixos demais para avaliar a qualidade visual.
- Para evitar que o modelo invente conteudo nas bordas, prefira camera travada e
  movimento no personagem. Evite zoom, pan e mudanca de enquadramento.

## Atualizar o codigo

O repositorio original esta em `local-video/mlx-video`. Para atualizar no futuro:

```bash
git -C local-video/mlx-video pull --ff-only
local-video/.venv/bin/python -m pip install -e local-video/mlx-video
```

O ambiente virtual, o modelo e os videos locais nao precisam ser enviados para
um repositorio Git.
