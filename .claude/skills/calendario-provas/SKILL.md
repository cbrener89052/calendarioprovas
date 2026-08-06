---
name: "calendario-provas"
description: "Monta calendário de provas para turmas da escola: distribuição entre disciplinas, limite semanal de avaliações, períodos por turma/grupo (turmas que viajam terminam mais cedo), feriados e semanas vetadas, preferência por provas nos primeiros tempos do dia, datas de simulados por série, provas combinadas no mesmo dia (Português+Redação+Gramática em 3 tempos), disciplinas com só 1 prova no semestre conforme a série, grupos paralelos com prova simultânea, e uso de tempos de outros professores quando a prova precisa de tempos seguidos. Lê o horário-base (planilha, PDF ou imagem) e gera as propostas de calendário, o relatório de trocas de tempo entre professores e a tabela-resumo por turma (disciplina, professor, dia e tempos, nº de tempos). Usar sempre que o usuário pedir para montar, gerar, revisar, ajustar ou exportar um calendário/plano de provas."
---

# Calendário de Provas

## Objetivo

Montar um calendário de provas a partir de:
1. Um arquivo-base com o horário semanal de cada turma (disciplina abreviada
   + sigla do professor + sala, por tempo/dia) — em planilha, PDF ou imagem.
2. Um arquivo-modelo com o layout esperado da planilha de saída (formato de
   célula, abas, datas do período).
3. (Opcional, mas recomendado) O calendário de provas já executado no
   semestre anterior, como referência do que costuma ter prova, quantos
   tempos cada disciplina usa, e quais exceções existem por turma/série.
4. (Se houver) A tabela oficial de simulados / avaliações globais.
5. A planilha de siglas de professores (sigla → nome completo).

O resultado final são as **propostas de calendário** (quantidade combinada
com o usuário), um **relatório de trocas de tempo entre professores** e uma
**tabela-resumo por turma**.

## Passo 0 — Perguntas obrigatórias antes de começar

Nunca comece a montar o calendário sem antes:

1. **Perguntar os períodos de provas POR TURMA ou grupo de turmas** — não
   assumir um único período para o semestre todo. Grupos de turmas
   diferentes podem ter datas de término diferentes (ex.: turmas que viajam
   ao exterior terminam o ano letivo mais cedo). Perguntar explicitamente
   quais turmas pertencem a cada grupo e a data-limite de cada um.
2. **Perguntar os dias que NÃO podem ser usados**: feriados nacionais,
   semanas inteiras vetadas (ex.: semana de conselho de classe), dias
   letivos especiais. Depois de receber a lista, **conferir também o
   calendário civil**: o usuário pode esquecer algum feriado nacional.
   Listar para ele os feriados que você encontrou no período antes de gerar.
3. **Perguntar até que tempo do dia as provas podem ser aplicadas.** Nesta
   escola a preferência é evitar ao máximo os **tempos 7 a 11** (o 7º tempo
   começa 12h45). Não é proibição: algumas disciplinas só têm aula nesses
   horários. Ver a regra completa abaixo.
4. **Perguntar as datas dos simulados por série**, pois contam como prova.
   O usuário pode preferir subir um arquivo (PDF/planilha) com a tabela.
   Perguntar também **em quais tempos o simulado ocupa o dia** (ex.: do 2º
   ao 7º tempo). Códigos usados nesta escola: **AG9** (9º ano), **AG10**
   (10º ano), **S1-11 a S4-11** (11º ano), **S1-12 a S4-12** (12º ano) e
   extras no formato **EX-TURMA-NÚMERO** (ex.: "EX11-1").
   Ao receber a tabela, confirmar com o usuário eventuais correções
   (datas remarcadas) e erros de digitação (ex.: ano errado numa célula).
5. **Perguntar quais disciplinas fazem prova combinada no mesmo dia.**
   Nesta escola, nas turmas 10, 11 e 12, Português (plit), Redação (pred)
   e Gramática (p) fazem **uma única prova de 3 tempos consecutivos**, no
   mesmo dia, com os três professores. Nas turmas 9, Redação e Português
   são **provas separadas de 2 tempos cada**. Sempre confirmar esse tipo de
   agrupamento — ele muda a contagem de avaliações da semana.
6. **Perguntar quantos tempos cada prova usa** e quais usam apenas 1 tempo.
   Não inferir da carga horária semanal. Se houver calendário do semestre
   anterior, use-o como ponto de partida, mas confirme quando os dados
   forem inconsistentes entre turmas.
7. **Perguntar sobre exceções de "1 prova só no semestre" por série**:
   ex.: nesta escola, Biologia, Química e Física têm apenas 1 prova no
   semestre inteiro (1 tempo cada) nas turmas do 9º ano, mas 1 prova por
   período nas demais séries. Filosofia e Sociologia têm 1 tempo semanal na
   grade e por isso 1 prova no semestre, de 1 tempo.
8. **Confirmar quais disciplinas NÃO têm prova.** Nesta escola: Educação
   Física ("esp"/"Spo"), Artes/Música/Teatro, Técnicas, Finanças,
   Socioemocional, aulas de apoio/aprofundamento ("ap...", "apr..."),
   eletivas e Projeto Vestibular. Confirmar sempre.
9. **Confirmar a estrutura de saída** (quantos arquivos/abas, layout de
   célula) olhando o arquivo-modelo mais recente. Perguntar quantas
   propostas o usuário quer.
10. **Confirmar a leitura do horário-base** em caso de ambiguidade. Cuidado
    com siglas parecidas entre escolas: aqui "esp"/"Spo" = Esportes/Educação
    Física, NÃO Espanhol.
11. **Perguntar como tratar grupos paralelos** (turma se divide, cada
    professor com seu grupo no mesmo tempo — ex.: Alemão/DaF). Regra
    confirmada nesta escola: **1 prova só, aplicada simultaneamente**, cada
    professor com o seu grupo; conta como 1 avaliação da turma.
12. **Perguntar se há sala padrão de provas.** Nesta escola **não há** —
    o campo de sala fica em branco.

## Regras de distribuição das provas

- **Máximo de 3 avaliações por semana** por turma. Simulados/AG contam para
  esse limite; um simulado de 2 dias conta como **1** avaliação.
- **Uma prova por dia** por turma (a célula do modelo comporta uma só).
- **Grupo 1** — Matemática, Alemão (DaF), Português (ou a prova combinada
  LP/LIT/RED) e Inglês: não devem ter prova na mesma semana entre si. Só
  permitir sobreposição se não houver nenhuma outra forma de fechar o
  calendário — e avisar o usuário quando isso acontecer.
  **GL não pertence ao grupo 1** (é disciplina própria, com prova).
- **Evitar os tempos 7 a 11** (a partir das 12h45). Trate como preferência
  forte, não proibição: há disciplinas cujo único horário na grade é à
  tarde (ex.: Biologia numa turma que só tem Bio no 7º, 7º e 11º tempos;
  Filosofia no 9º tempo). O algoritmo deve **minimizar** o número de provas
  nesses tempos — buscar primeiro uma solução com zero, depois com uma, e
  assim por diante — e priorizar a redução dessas provas **antes** de
  aceitar sobreposição do grupo 1. Ao final, listar para o usuário quais
  provas ficaram à tarde e por quê.
- **Disciplinas com 1 prova no semestre** (1 tempo semanal na grade, ou
  exceção de série confirmada): alocar em apenas um dos períodos.
- **Simulados/AG**: entram nas datas informadas, são fixos, não podem ser
  movidos para encaixar outras provas.
- **Tempo de aplicação**: preferencialmente no(s) tempo(s) da própria
  disciplina.
- **Tempos emprestados**: os professores raramente têm dois tempos seguidos
  da própria disciplina. Quando a prova precisa de 2 ou 3 tempos seguidos,
  o(s) tempo(s) extra(s) vêm de outra disciplina da grade naquele dia.
  - **O tempo emprestado pode vir tanto DEPOIS quanto ANTES** do tempo da
    disciplina — considerar as duas direções. Isso é essencial: uma
    disciplina que só tem aula no último tempo do dia não teria nenhuma
    opção se apenas o tempo seguinte fosse considerado.
  - **Disciplinas com apenas 1 tempo de aula por semana NÃO podem doar**
    (Filosofia, Sociologia e qualquer outra com uma única aula semanal na
    grade daquela turma). Ceder esse tempo significaria perder a aula
    inteira da semana. Calcule essa lista por turma, contando as ocorrências
    de cada disciplina na grade — não use uma lista fixa de nomes.
  - Preferir os arranjos que emprestam menos tempos de terceiros.
  - Evitar tomar um tempo que também seja parte do tempo duplo da
    disciplina doadora.
- **Não preencher**: células de dia sem aula; células já preenchidas com
  qualquer outra informação.

## Leitura do arquivo-base

- Disciplina abreviada, sigla do professor e sala aparecem juntas em cada
  tempo/dia (ex.: "plit MFo E306").
- Leia por extração de planilha quando possível; use **visão computacional**
  quando o horário estiver em PDF ou imagem. Grades tipo Untis: a extração
  de texto plano **perde o mapeamento dia/tempo** — renderize a página em
  imagem (ex.: `pdftoppm -png -r 200 -f N -l N`) e leia visualmente.
- **Registre na grade TODAS as aulas, inclusive as que não têm prova**
  (Educação Física, artes, eletivas, apoio). Elas não geram avaliação, mas
  seus tempos podem ser emprestados. Omiti-las faz disciplinas legítimas
  ficarem sem nenhum slot possível.
- Grupos paralelos numa mesma célula não são erro de leitura — é a
  estrutura real da grade.
- Em caso de dúvida sobre uma abreviação, **pare e pergunte**. Valide as
  siglas de professor contra a planilha de siglas.
- Ao usar o calendário do semestre anterior como referência, trate os dados
  extraídos como candidatos a confirmar — a posição das linhas (sala x
  tempo) varia entre abas.

## Escrita na planilha de saída

- **Edite o arquivo-modelo existente** (copiando-o), não gere a planilha do
  zero: o modelo já traz grade de semanas, datas, cores e células mescladas.
- As células de data costumam ser **fórmulas** (`=A3+1`). Ao reler o arquivo
  com `data_only=True` elas voltam vazias — calcule as datas a partir da
  primeira semana em vez de lê-las célula a célula.
- Células mescladas: escreva sempre na célula âncora (canto superior
  esquerdo) — escrever nas demais gera erro.
- **Cuidado ao copiar uma aba de turma como template para as outras**: ela
  carrega marcações específicas daquela turma/série (simulados, "2CH 10,12",
  "CC 9,11"). Apague as que não pertencem à série da aba de destino, senão
  elas bloqueiam dias silenciosamente e provas somem sem aviso.
- O algoritmo de alocação deve conhecer as células já ocupadas no modelo,
  senão aloca provas em dias que serão descartados na escrita.

Formato de célula confirmado nesta escola (3 linhas):

```
Disciplina - Sigla(s) do professor
[sala — deixar em branco quando não houver sala padrão]
Tempo(s)
```

Exemplo real:
```
LP/LIT/RED - BPad/MFo/SMo

1º ao 3º tempos
```

## Entregáveis finais

1. **As propostas de calendário**, na estrutura combinada com o usuário
   (ex.: um arquivo xlsx por proposta, com uma aba por turma).
2. **Relatório de trocas de tempo entre professores**, em tabela, uma linha
   por troca:

   | Turma | Disciplina/Prof. solicitante | Tempo necessário | Prof. doador | Disciplina do tempo doado | Ação |
   |---|---|---|---|---|---|

   Claro o suficiente para ser usado direto na comunicação com os
   professores.
3. **Tabela-resumo por turma** (uma aba por turma, um arquivo por proposta),
   em formato de lista ordenada por data — é a visão que a coordenação usa
   para conferir e divulgar. Colunas:

   | Disciplina | Professor(es) | Dia e tempos da prova | Nº de tempos |
   |---|---|---|---|

   - **Professor(es)**: sigla **e** nome completo, buscados na planilha de
     siglas (ex.: "BPad (Beatriz de Matos Ferreira Padrão)"). Quando a prova
     tem vários professores (grupos paralelos, prova combinada), listar
     todos separados por vírgula. As siglas na planilha de saída vêm
     separadas por `/` ou `-` — quebrar por ambos.
   - **Dia e tempos**: dia da semana por extenso + data + tempos
     (ex.: "Quinta, 27/08/2026 — 1º ao 3º tempos").
   - **Nº de tempos**: contar a faixa inteira (do primeiro ao último tempo),
     não a quantidade de números escritos no rótulo.
   - Simulados de 2 dias devem aparecer em **uma linha só**, com as duas
     datas.
   - Incluir os simulados/AG na tabela: eles são avaliações.
   - Gerar essa tabela a partir das planilhas de calendário já gravadas,
     em script separado — assim ela reflete o que foi realmente escrito, e
     não o que o gerador acha que escreveu.

## Verificação obrigatória antes de entregar

Escreva um **script de verificação separado** que releia os arquivos .xlsx
gravados (sem confiar na memória do gerador) e cheque cada item abaixo.
Erros silenciosos são o risco principal aqui: prova descartada por célula
ocupada, marcação herdada de outra turma, disciplina sem slot possível.

- [ ] Nenhuma turma ultrapassa 3 avaliações na mesma semana (simulado de 2
      dias conta 1)
- [ ] Nenhum dia com mais de uma prova
- [ ] Disciplinas do grupo 1 não coincidem na mesma semana
- [ ] Cada disciplina tem exatamente o número de provas esperado (2, ou 1
      para as de prova única) — se aparecer 1 onde deveria haver 2, alguma
      prova foi descartada silenciosamente na escrita
- [ ] Provas combinadas (LP/LIT/RED) usam o número certo de tempos e não
      aparecem como disciplinas separadas
- [ ] Disciplinas de prova única usam apenas 1 tempo
- [ ] Nenhuma prova para disciplinas sem avaliação
- [ ] Toda prova nos tempos 7 a 11 é inevitável — a disciplina não tem
      nenhum slot possível pela manhã
- [ ] Nenhuma prova usa tempo de disciplina que tem só 1 aula na semana
- [ ] Todos os simulados nas datas oficiais e nos tempos corretos
- [ ] Nenhuma prova em feriado, na semana vetada, antes do início do
      período ou depois da data-limite do grupo daquela turma
- [ ] Todo tempo emprestado de outro professor está no relatório de trocas
- [ ] A tabela-resumo tem o mesmo número de linhas que o calendário tem de
      avaliações, e todas as siglas foram traduzidas em nomes
- [ ] A estrutura de saída está conforme combinado

