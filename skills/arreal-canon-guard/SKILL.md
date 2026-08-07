---
name: arreal-canon-guard
description: Garantir fidelidade estrita ao cânone de Arreal em imagens, vídeos, animações, legendas, anúncios, sinopses comerciais e qualquer divulgação do livro. Usar sempre que Codex criar, editar, revisar, aprovar, agendar ou publicar material promocional de Arreal; exigir fonte no manuscrito, ficha de cena e auditoria antes da entrega ou publicação.
---

# Arreal Canon Guard

Impedir que uma peça promocional mostre ou afirme acontecimentos, poderes,
relações, lugares ou objetos que não existam no livro.

## Autoridade das fontes

Usar esta ordem:

1. `chapters/*.tex`: única prova suficiente de que uma cena acontece.
2. `chapters/nota_autor.tex`: prova apenas de experiências e intenções do autor,
   nunca de acontecimentos narrativos.
3. `chapters/sinopse.tex`: apoio de posicionamento, nunca prova visual de cena.
4. Guias editoriais e resumos: ferramentas de localização; confirmar tudo no
   capítulo antes de usar.
5. Capa e artes de marketing: referências de identidade visual; nunca tratar
   como prova de cânone.

## Fluxo obrigatório

1. Localizar no manuscrito a cena ou afirmação que sustentará a peça.
2. Ler a cena completa, não apenas um resultado de busca isolado.
3. Criar uma ficha de cena conforme
   [references/acceptance-checklist.md](references/acceptance-checklist.md).
4. Gerar ou selecionar a imagem somente a partir dessa ficha.
5. Inspecionar a imagem final e comparar cada elemento narrativamente relevante
   com a ficha.
6. Registrar `PASSA` ou `REPROVA` em `auditoria-canonica.md` junto ao material.
7. Entregar, agendar ou publicar somente imagens marcadas `PASSA`.

## Restrições absolutas

- Não compor personagens, poderes, objetos ou lugares de cenas diferentes numa
  única imagem, salvo quando o manuscrito os reúna naquela cena exata.
- Não converter metáforas em acontecimentos literais.
- Não inventar demonstrações de poderes para explicar um tema.
- Não acrescentar multidões, confrontos, romances, símbolos, marcos urbanos,
  figurinos ou consequências não descritos.
- Não usar uma arte existente sem auditá-la; nome de arquivo e aparência
  plausível não comprovam fidelidade.
- Não aceitar “inspirado no tema” como equivalente a “acontece no livro”.
- Se a fonte for ambígua, pausar e pedir decisão ao autor em vez de preencher a
  lacuna criativamente.

Elementos puramente gráficos — tipografia, molduras, gradientes e textura — são
permitidos quando não sugerirem um acontecimento, poder ou relação inexistente.
Detalhes ambientais incidentais podem ser inferidos apenas quando forem neutros,
necessários à ilustração e não contradisserem o texto.

## Prompt de imagem

Incluir no prompt:

- capítulo e trecho-fonte;
- local, momento, personagens e ação exatos;
- poderes realmente ativos na cena;
- aparência, roupas e objetos confirmados;
- lista explícita do que não adicionar;
- `Representar somente este acontecimento literal. Não criar montagem,
  simbolismo narrativo ou antecipação de eventos posteriores.`

## Critério de aceite

Reprovar ao primeiro detalhe narrativamente relevante sem apoio no trecho.
Beleza, impacto e coerência temática não compensam falta de fidelidade.

Antes de publicar, exigir simultaneamente:

- fonte canônica identificada;
- ficha preenchida;
- imagem inspecionada em resolução final;
- nenhum elemento importante fora da ficha;
- copy sem promessa além do livro;
- status `PASSA` registrado.

Se qualquer item faltar, não publicar, mesmo que o usuário tenha autorizado uma
postagem imediata.

