# Fluxo de revisão do `chapter0.tex` — O despertar

## Objetivo

Revisar o capítulo de abertura sem perder sua função narrativa: apresentar o Garoto, sua necessidade de aceitação, Lúcia como contraponto, o isolamento na escola e o primeiro contato com as habilidades por meio de Ítalo.

O arquivo de trabalho é `chapters/chapter0.tex`. As observações de `REVISAO_PROFISSIONAL.md` são a pauta primária; os demais guias e o material Snowflake funcionam como testes de coerência.

## Fontes e ordem de autoridade

1. `CONTEXT_GUIDES/REVISAO_PROFISSIONAL.md`: problemas percebidos pela leitora profissional.
2. `chapters/chapter0.tex`: voz, cenas e estrutura efetivamente entregues ao leitor.
3. `snowflake/step6/scenelist.json`: função planejada para o capítulo.
4. `CONTEXT_GUIDES/CHARACTER_DEVELOPMENT_GUIDE.md`: consistência dos personagens.
5. Capítulos posteriores: continuidade factual e preparação de eventos.
6. `CONTEXT_GUIDES/ANALYSIS_GUIDELINES.md`: validação técnica do LaTeX.

Em caso de conflito, preservar primeiro a compreensão do leitor e a continuidade do livro; o Snowflake orienta, mas não substitui o texto final.

## Diagnóstico inicial

| ID | Ponto da revisora | Diagnóstico | Decisão recomendada | Critério de aceite |
|---|---|---|---|---|
| R1 | Escrita no topo do Empire State | O cenário tem continuidade com os capítulos 29 e 40, mas o verbo “escrevo” sugere uma ação física sem apoio ou explicação. | Manter o Empire State e converter o enquadramento em relato mental/retrospectivo. Substituir formulações como “não escrevo” e “este relato chegou às suas mãos” por linguagem compatível com uma história contada ao leitor. | O leitor entende onde ele está, o que faz ali e por que começa a narrar, sem imaginá-lo escrevendo em pé. |
| R2 | “Intervalo” antes da aula | A cena ocorre na chegada à escola; “intervalo” indica recreio no meio do turno. | Trocar por “os minutos antes da primeira aula” ou equivalente e manter explícito que os alunos aguardam no pátio. | Não há dúvida sobre o momento do turno escolar. |
| R3 | Biblioteca, cadeiras, perseguição e sinais | A lembrança da agressão anterior se mistura com a perseguição presente. Há ainda dois sinais muito próximos: um na lembrança e outro no presente. | Isolar a lembrança num bloco claramente marcado (“dias antes”), dizer que mesa e cadeiras eram da biblioteca, encerrar o flashback e só então retomar Bento no pátio. No presente, explicar por que os perseguidores continuam correndo apesar do sinal. | Em uma leitura corrida, é possível responder sem hesitação: onde, quando e com quem ocorre cada ação. |
| R4 | Significado de “volitando” | O termo é incomum e Ítalo o usa como distinção conceitual. | Preferir explicação orgânica no diálogo (“volitar é...”). Usar nota de rodapé apenas se o autor quiser uma voz mais editorial. | O significado fica claro sem interromper o primeiro encontro com Ítalo. |
| R5 | Repetição “possibilidade/possível” | Repetição lexical no mesmo período. | Reescrever como “Ali minha mente se abriu para a ideia de que o impossível talvez não existisse”, ou formulação equivalente na voz do Garoto. | Não há repetição e a frase não soa abstrata ou adulta demais para o narrador. |

## Pontos adicionais detectados

### A1 — Explicação da mata

A mata é apresentada como “fundo do pátio” e, logo depois, como uma floresta ampla. Na revisão, explicitar se existe uma cerca, um portão, uma passagem ou um limite aberto entre a escola e a mata. Também deve ficar plausível que a inspetora encontre o Garoto mais tarde.

### A2 — Cronologia depois do desmaio

O texto diz “nos dias seguintes”, depois apresenta a ida à loja e, mais tarde, “depois daquele dia”. Definir se a loja ocorre no mesmo dia do despertar, no dia seguinte ou após várias buscas na mata. Uma marca temporal curta resolve a ambiguidade.

### A3 — Reiteração temática

A expressão “poder pessoal” e a ideia de entregar o controle aos outros aparecem na abertura, no pátio e no encerramento. Essas reiterações fazem parte da intenção temática do autor e devem ser preservadas. Se houver ajuste, ele deve melhorar a transição ou desenvolver a ideia, sem reduzir o conteúdo.

### A4 — Lúcia e o vínculo afetivo

As falas iniciais estabelecem intimidade por meio de provocações, mas a frase sobre ele não ter amigos pode fazer Lúcia parecer apenas cruel. Manter seu ceticismo e rispidez, acrescentando um gesto ou hesitação que sustente sua função de âncora afetiva sem suavizá-la demais.

### A5 — Promessas e informação antecipada

A abertura revela telecinese, volitação e outras habilidades antes do primeiro encontro com Ítalo. Isso é compatível com o plano Snowflake, que pede o Garoto já poderoso no enquadramento, mas a revisão deve verificar se a lista preserva curiosidade suficiente e não antecipa mais do que o necessário.

## Etapas de execução

### Etapa 1 — Revisão estrutural

- Delimitar o enquadramento no Empire State.
- Montar uma linha do tempo simples da manhã na escola.
- Separar visual e verbalmente lembrança e presente.
- Fixar a transição escola → mata → casa → buscas posteriores → loja.

Saída esperada: cenas compreensíveis sem ainda polir cada frase.

### Etapa 2 — Revisão de personagem e voz

- Conferir a tensão do Garoto entre invisibilidade e desejo de reconhecimento.
- Conferir Lúcia como contraponto cético, mas afetivamente implicado.
- Manter Ítalo calmo e associado à promessa de algo maior.
- Reduzir explicações abstratas que não soem naturais na voz do narrador.

Saída esperada: motivações demonstradas por escolhas, reações e diálogos.

### Etapa 3 — Revisão de estilo

- Aplicar R4 e R5.
- Preservar e, quando necessário, desenvolver as passagens sobre aceitação, controle e poder pessoal.
- Revisar repetições de “garoto”, “habilidades”, “acreditar” e “possibilidade”.
- Preservar oralidade dos diálogos sem misturar registros involuntariamente.

Saída esperada: leitura fluida, com reflexão suficiente para caracterizar sem travar a ação.

### Etapa 4 — Validação de continuidade

- Comparar o Empire State com os capítulos 29 e 40.
- Comparar o primeiro contato com Ítalo com as revelações posteriores sobre ele.
- Verificar se nenhuma mudança contradiz a lista de cenas do Step 6.
- Confirmar que todas as promessas do capítulo têm função posterior.

Saída esperada: nenhuma correção local cria contradição global.

### Etapa 5 — Validação técnica

- Compilar `index.tex`.
- Verificar erros, avisos relevantes, caracteres especiais e paginação.
- Ler o PDF renderizado nas páginas do capítulo, com atenção a quebras de parágrafo e eventual nota de rodapé.
- Fazer uma busca final pelos trechos antigos para confirmar que todos os apontamentos foram tratados.

Saída esperada: PDF compilado e checklist encerrado.

## Checklist de aprovação

- [x] R1 — Ação no Empire State está fisicamente clara.
- [x] R2 — Chegada à escola não é chamada de intervalo.
- [x] R3 — Flashback da biblioteca e perseguição presente não se confundem.
- [x] R4 — “Volitar” está explicado.
- [x] R5 — Repetição “possibilidade/possível” foi eliminada.
- [x] A1 — Acesso da escola à mata é plausível.
- [x] A2 — Sequência temporal depois do desmaio está marcada.
- [x] A3 — Tema e extensão das reflexões foram preservados.
- [x] A4 — Lúcia preserva rispidez, afeto e função de âncora.
- [x] A5 — Abertura antecipa sem esvaziar a descoberta.
- [x] Continuidade com capítulos posteriores validada.
- [ ] LaTeX compilado e PDF inspecionado.

> Estado da validação técnica: a verificação estática (`git diff --check` e busca pelos trechos substituídos) foi concluída. A compilação depende do Docker usado pelos executáveis deste projeto; em 13/07/2026, o serviço do Docker não estava em execução.

## Regra de trabalho

Aplicar uma etapa por vez e revisar o diff antes de avançar. Não misturar correção estrutural com polimento fino no mesmo passe: isso torna mais difícil avaliar se uma alteração resolveu o problema original ou apenas mudou sua redação.

Como regra editorial deste projeto, a revisão não deve reduzir o tamanho do texto. Correções de clareza devem preservar o conteúdo existente ou expandi-lo quando for necessário contextualizar uma cena. Qualquer corte precisa de autorização específica do autor.
