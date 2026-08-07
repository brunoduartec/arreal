# Diretrizes de Revisão Técnica (LaTeX)

Este documento estabelece as regras de engajamento e revisão técnica do material LaTeX.

## 1. Estrutura e Préâmbulo
*   **Verificação:** Inspecione o preâmbulo (`\documentclass{...}` até a declaração do `\begin{document}`). Confirme se todos os pacotes necessários (pacotes de imagens, bibliografia, matemática) estão corretamente carregados.
*   **Revisão Crucial:** Revise o uso de *packages* e comandos específicos do LaTeX que podem ter sido adicionados ad hoc no passado, garantindo a consistência global.

## 2. Gestão de Conteúdo (Seções e Capítulos)
*   **Sistema de Referências:** Certifique-se de que todo `\chapter{}` está corretamente balanceado com o número de capítulos esperado para a publicação final.
*   **Metadados:** Os dados estruturais do livro (nome, autor, data, etc.) devem ser centralizados e gerenciáveis (por exemplo, em um único bloco ou pacote).

## 3. Estilo e Padronização
*   **Formatação de Código/Diagramas:** Se o livro incluir blocos de código ou diagramas, use sempre a sintaxe LaTeX apropriada (`lstlisting` para código, `tikzpicture` para gráficos) e padronize o estilo visual (cores, fontes).
*   **Citações e Bibliografia:** Verifique se todas as citações no texto correspondem a entradas na bibliografia. Se for usado BibTeX, garanta que o arquivo `.bib` referenciado é completo e atualizado.

## 4. Workflow de Análise Iterativa (Snowflake-to-LaTeX)
*   **Ciclo:** Para cada seção importante do capítulo, mapeie: *Qual conceito está sendo discutido?* -> *De qual artefato `snowflake/` ele deriva?* -> *Qual é o refinamento mais recente associado a este tópico?*

