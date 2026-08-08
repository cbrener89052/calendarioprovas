# Plano — Modelo "Semana de Provas" (não implementado ainda)

Este arquivo documenta um pedido do usuário que foi **discutido e decidido em
parte, mas cujo desenvolvimento foi explicitamente adiado**. Serve para
retomar a conversa em outra sessão sem perder o que já foi combinado.

**Status: só planejamento. Nenhum código foi escrito para este modelo.**

## O pedido original (literal)

> "estamos pensando em implementar a semana de provas. a proposta é que
> todos os dias teriamos provas de segunda a sexta feira até completar o
> ciclo de provas da primeira parte do semestre e da segunda parte do
> semestre. faça uma proposta em que não haveria limitação de 3 provas, é
> claro, e seria uma prova por dia. mantenha as outras premissas,
> SOBRETUDO aquela que minimizamos a doação de tempos de aula para outras
> disciplinas aproveitando o tempo da disciplina, e chame esse modelo de
> SEMANA DE PROVAS."

## A ideia, em resumo

Em vez de espalhar as provas de um período (P1 ou P2) por várias semanas
com no máximo 3 avaliações por semana (regra das Propostas 1, 2 e 3), a
Semana de Provas comprime cada período num **bloco de dias corridos,
segunda a sexta, uma prova por dia**, até esgotar todas as provas
daquele período. Dois blocos no semestre: um para P1, um para P2.

## Decisões já confirmadas pelo usuário

O usuário confirmou as opções recomendadas para os 3 primeiros pontos e
respondeu "sim" ao quarto:

1. **Regra do grupo 1** (Mat/DaF/Port-LPLITRED/Ing não coincidir na mesma
   semana): como "mesma semana civil" quase perde o sentido num bloco
   compacto de ~2 semanas, **trocar por uma distância mínima em dias**
   entre duas provas do grupo 1 (ex.: nunca em dias consecutivos — o
   valor exato do mínimo ainda não foi fixado, ver pendências abaixo).
2. **Os 5 limites de cessão da Proposta 3** (máx. 2-3 cessões no
   semestre — 3 para História/Geografia/GL —, 1 aula/semana não cede,
   nunca 2 semanas seguidas sem contato, não ceder na véspera da própria
   prova nem na anterior, teto de 11% da carga do semestre): **continuam
   valendo** na Semana de Provas. A expectativa é que o modelo saia
   ainda melhor que a Proposta 3 nesse quesito, porque ganha liberdade
   extra para escolher o dia que aproveita o tempo próprio da
   disciplina, sem competir por vaga na semana com outras 2 provas.
3. **Simulados/AG de data fixa** (AG9, AG10, S3-11, S4-11, S4-12):
   **entram na sequência diária** — o dia do simulado ocupa o "1
   avaliação por dia" e as provas escritas se organizam ao redor dele,
   igual já acontece nas Propostas 1-3.
4. **Escopo**: é uma **proposta nova e separada** (não substitui nenhuma
   das Propostas 1, 2 ou 3, que continuam como estão). Nome de saída
   sugerido: `Proposta_SemanaDeProvas` (arquivo, abas, relatórios — a
   confirmar o padrão de nomenclatura exato na hora de implementar).

## O que a Semana de Provas MANTÉM das Propostas 1-3

Tudo que não foi listado acima como alterado continua valendo, em
particular:

- **1 prova por dia** por turma (já era regra).
- **Preferência máxima pelo tempo próprio da disciplina**, evitando
  cessão — é a premissa que o usuário destacou como prioridade
  ("SOBRETUDO").
- Provas coordenadas entre turmas irmãs quando há professor comum
  (aplicação simultânea, mesmo dia/tempo).
- Nunca cruzar o intervalo do recreio (3º/4º e 5º/6º tempos) — maior
  prioridade entre as regras de horário do dia.
- Evitar ao máximo os tempos 7-11.
- LP/LIT/RED como prova combinada de 3 tempos nas turmas 10-12.
- Disciplinas de prova única no semestre (Fil, Soc, e Bio/Fis/Qui nas
  turmas 9) alocadas em 1 dos dois períodos.
- Feriados, semana vetada (12-16/10) e datas-limite por grupo de turma
  (10C/12C viajam antes de 9C/11C).
- Alternância de doador quando a mesma disciplina/professor tem mais de
  uma prova de tempos duplos no semestre.

## Números já levantados (para dimensionar o bloco de dias)

Contagem de provas por turma e por período, com as regras atuais
(`montar_exames()` em `gerar_calendario.py`):

| Turma | Provas fixas em P1 | Provas fixas em P2 | Provas "únicas" (Fil/Soc/9C Bio-Fis-Qui, hoje alocadas dinamicamente) |
|---|---|---|---|
| 9C1 | 8 | 8 | 3 |
| 9C2 | 8 | 8 | 3 |
| 10C1 | 10 | 10 | 2 |
| 10C2 | 10 | 10 | 2 |
| 11C1 | 10 | 10 | 2 |
| 11C2 | 10 | 10 | 2 |
| 12C1 | 10 | 10 | 2 |
| 12C2 | 10 | 10 | 2 |

Com 1 prova/dia, cada período vira um bloco de **~8 a ~12 dias úteis
corridos** (pouco menos de 2 a pouco mais de 2 semanas civis), duas
vezes no semestre — bem mais compacto que a distribuição atual (que usa
4 semanas em P1 e 8-9 semanas em P2).

## Pendências a resolver ANTES de implementar

Pontos que ainda não foram fechados com o usuário e precisam de decisão
(ou de uma proposta minha a confirmar) quando o desenvolvimento
retomar:

1. **Valor exato da distância mínima em dias para o grupo 1** (item 1
   acima). "Nunca em dias consecutivos" foi só o exemplo dado na
   pergunta — não foi confirmado como o valor final. Também não ficou
   definido o que fazer quando nem essa distância mínima couber (relaxar
   como as outras regras, com aviso? Até onde relaxar?).
2. **Onde exatamente o bloco de cada período começa.** Hoje P1 começa na
   semana 3 (17/08) e P2 varia por grupo de turma. Confirmar se a Semana
   de Provas de cada turma começa no primeiro dia útil possível dentro
   da janela já definida, ou se há alguma outra regra de início.
3. **Ordem de resolução entre turmas irmãs.** As provas coordenadas
   (professor comum) precisam do mesmo dia nas duas turmas — isso já é
   tratado no motor atual (`resolver_par`) antes de resolver cada turma
   individualmente; a Semana de Provas provavelmente reaproveita essa
   arquitetura, mas com a lógica de "encaixar em um bloco compacto" em
   vez de "escolher entre várias semanas".
4. **Nomenclatura final de saída** (arquivo(s), abas, relatórios
   associados — tempos cedidos, tabela por turma, trocas de tempo) —
   seguir exatamente o padrão das Propostas 1-3 ou ajustar algo
   específico da Semana de Provas.
5. **Desempenho.** As Propostas 1-3 já precisaram de otimizações
   específicas (pré-computar blocos válidos, orçamento de nós menor,
   escolha de semente) para rodar em tempo razoável com os limites de
   cessão ligados. Um bloco compacto de dias muda bastante o espaço de
   busca (menos opções de "para qual semana mandar" cada prova, mas
   mais pressão para encaixar tudo sem furos) — a estratégia de busca
   provavelmente precisa ser repensada, não só reaproveitada.

## Retomando esta conversa

Quando o desenvolvimento for autorizado, o próximo passo é resolver as
5 pendências acima (a maioria pode ser proposta por mim com uma
recomendação, como foi feito para as 4 decisões já tomadas) e então
implementar em `gerar_calendario.py` seguindo o mesmo padrão das
Propostas 1-3: função de resolução dedicada, verificação no
`verificar_calendario.py`, e os relatórios de exportação já existentes
adaptados para incluir a nova proposta.
