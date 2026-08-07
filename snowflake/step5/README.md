# Step 5 — Bíblias e descrições visuais auditáveis

Este diretório foi regenerado a partir do manuscrito em `chapters/*.tex` e das
fichas narrativas do `step3`. O manuscrito é a única autoridade para fatos
visuais. As imagens antigas e as versões anteriores do `step5` foram usadas
somente para localizar divergências.

## Estados usados

- `PENDENTE_DE_AUDITORIA_AUTORAL`: há descrição textual suficiente, mas o autor
  ainda precisa aprovar a ficha.
- `PENDENTE_DE_DEFINICAO_AUTORAL`: o manuscrito deixa traços físicos importantes
  em aberto; não gerar um retrato frontal definitivo antes de preenchê-los.
- `PENDENTE_DE_ESCOLHA_DA_FASE`: existem aparições distintas e é obrigatório
  escolher uma delas.
- `BLOQUEADA_POR_INCONSISTENCIA_CANONICA`: o próprio manuscrito contém descrições
  conflitantes.

## Visão geral

| Personagem | Estado da ficha | Decisão principal |
|---|---|---|
| Lúcia | Pendente de auditoria | 21 anos e pele negra clara aprovados pelo autor; faltam cor/comprimento do cabelo e rosto |
| Larissa | Bloqueada | Resolver cabelo azul versus vermelho |
| Pedro | Pendente de auditoria | Completar pele, cabelo, olhos e rosto |
| Garçom | Pendente de auditoria | Aprovar retrato envelhecido e uniforme gasto |
| Crispim | Escolha da fase | Corpo físico ou projeção mental |
| Ítalo | Definição autoral | Praticamente toda a identidade física |
| Bento | Definição autoral | Fase e identidade física completa |
| Jonas | Definição autoral | Fase e identidade física completa |
| Garoto | Definição autoral | Pele negra clara aprovada pelo autor; faltam nome, idade, rosto, cabelo, olhos e uniforme |
| Joana | Definição autoral | Idade, pele, rosto, cabelo e tipo físico |

## Roteiro de auditoria autoral

Para cada arquivo:

1. Conferir `CHARACTER_SYNOPSIS`.
2. Aprovar ou corrigir `CANONICAL_PHYSICAL_APPEARANCE.confirmed`.
3. Responder aos itens de `OPEN_DECISIONS`.
4. Se uma escolha nova deve ser canônica, inseri-la primeiro no capítulo
   apropriado; depois atualizar a ficha.
5. Selecionar uma única fase e uma única cena antes de escrever prompt de imagem.
6. Não alterar `EXISTING_IMAGE_AUDIT` sem inspecionar a imagem final.

## Ordem sugerida

1. Resolver Larissa, pois há contradição dentro do manuscrito.
2. Aprovar Lúcia, Pedro, Garçom e as duas variantes de Crispim, que já possuem
   marcadores físicos fortes.
3. Definir Ítalo, Bento, Jonas, Garoto e Joana, cujos traços permanecem abertos.

Nenhuma ficha deste diretório autoriza publicação. Uma imagem futura ainda
precisará de ficha de cena e registro `PASSA` na auditoria canônica.

## Referências canon v2 geradas

Em 7 de agosto de 2026 foram geradas versões não destrutivas para os dez
personagens. Os arquivos antigos permanecem preservados; as novas referências
usam o sufixo `-canon-v2.png` em `images/`.

A auditoria está em `images/auditoria-canonica-personagens-v2.md`. Todas as dez
versões receberam `PASSA` exclusivamente como referências visuais internas. O
status não autoriza uso automático em uma peça narrativa ou promocional.
