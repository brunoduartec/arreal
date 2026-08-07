# Guia de Projeto LaTeX - Livro em Desenvolvimento

Este documento serve como um guia de contexto e estrutura, fundamental para manter a coerência narrativa, rastrear a evolução das ideias e garantir que o produto final esteja alinhado com o material fonte.

## 1. Estrutura Geral
O projeto está dividido logicamente entre dois repositórios de informação:
*   **chapters/**: Contém os arquivos `.tex` dos capítulos finais ou quase finais do livro. Estes representam a estrutura narrativa primária e o produto visível ao leitor. Eles devem ser a nossa principal fonte para avaliar a *coerência final*.
*   **snowflake/**: Contém os artefatos gerados pelo método Snowflake (etapas de desenvolvimento, refinamentos). Este material é crucial para rastrear a *evolução da ideia*, mostrando o raciocínio por trás da escrita final nos capítulos.

## 2. Detalhamento dos Conteúdos

### A. Pasta `chapters/`
Esta pasta lista os módulos narrativos principais:
(Liste aqui os arquivos de capítulos, e mencione grupos como 'Capítulos Sequenciais' ou 'Apêndices Estruturais').

**Atenção:** O fluxo principal do livro deve ser rastreado pela ordem crescente dos números dos capítulos (`chapter1.tex` -> `chapter2.tex`, etc.). Os arquivos sem prefixo de capítulo (e.g., `sinopse.tex`, `nota_autor.tex*`) são provavelmente materiais de cabeçalho ou rodapé, e devem ser revisados em conjunto com a estrutura principal do *preâmbulo*.

### B. Pasta `snowflake/`
Esta pasta é o histórico das informações:
(Liste aqui os arquivos encontrados).

**Rastreabilidade:** Os arquivos JSON (`step*.json`) são fundamentais. Eles permitem mapear:
1.  Qual etapa de refinamento (Step N) gerou qual conceito que se manifesta no Capítulo X.
2.  Como a informação foi consolidada (`step0-2_consolidated.md`), servindo como um *briefing* avançado do tópico abordado naquele período.

## 3. Pontos Críticos de Análise (Key Focus Areas)
A análise deve focar na ponte entre o material bruto e o produto final:

1.  **Coerência Narrativa:** Os capítulos fazem uma progressão lógica sem saltos temáticos abruptos? O tom é mantido do início ao fim?
2.  **Fluxo de Informação:** Cada conceito fundamental apresentado nos arquivos `snowflake/` (especialmente os trechos mais consolidados) foi completamente explicado e desenvolvido em um capítulo dedicado?
3.  **Referências Cruzadas:** Deve-se verificar se há menções ou referências internas (em LaTeX, usando comandos como `\ref` ou `\cref`) que conectam conceitos de diferentes capítulos ou até mesmo artigos externos citados no contexto Snowflake.

