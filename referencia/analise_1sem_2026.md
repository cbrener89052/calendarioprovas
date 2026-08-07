# Análise das aulas cedidas no 1º semestre de 2026

Contagem do que **de fato ocorreu** no 1º semestre, para comparar com as
propostas do 2º. Gerada por `extrair_grade_1semestre.py` (grade de aulas,
lida do PDF do Untis) e `analisar_1semestre.py` (provas aplicadas +
contagem), e confrontada com a Proposta 3 por `comparar_semestres.py`.

## Dados de entrada

- `Horario modelo/Klausurplan_2026_1SEM.xlsx` — calendário de provas
  executado. Preenchimento manual e **muito irregular**: os tempos
  aparecem ora na linha do título, ora na da sala, com "º", com "o", por
  extenso ("primeiro e segundo"), como fração ("4.5") ou como intervalo
  ("1-7"), e códigos de sala (E301) se misturam aos números dos tempos.
- `horarios_1semestre/EM C Horarios Turmas 20260130.pdf` — grade de aulas
  do 1º semestre (8 páginas, uma por turma). **Diferente da do 2º
  semestre.** Não numera os tempos, mas cada célula traz a hora de início.

## Correspondência hora → tempo (confirmada pela escola)

| Tempo | Início | Tempo | Início |
|---|---|---|---|
| 1 | 7h15 | 7 | 12h45 |
| 2 | 8h05 | 8 | 13h30 |
| 3 | 8h55 | 9 | 14h15 |
| 4 | 10h00 | 10 | 15h10 |
| 5 | 10h50 | 11 | 15h55 |
| 6 | 11h55 | | |

Intervalos: após o 3º tempo (9h40–10h) e entre o 5º e o 6º (11h35–11h55).

## Período letivo (confirmado pela escola)

**04/02/2026 a 10/07/2026.** Os dias sem aula (feriados e recessos) vêm
das marcações `unterrichtsfrei` do próprio calendário de provas — semana
de carnaval inteira, Páscoa, Tiradentes, 1º de maio e Corpus Christi.

## Resultado

165 das 168 células de prova lidas. Cessões por turma:

| Turma | Cedidas | Aulas no semestre | % | Mais afetado |
|---|---|---|---|---|
| 9C1 | 21 | 728 | 2,9% | Mat/BrSa — 6 (5,8%) |
| 9C2 | 15 | 728 | 2,1% | Fís/VSi — 3 (14,3%) |
| 10C1 | 24 | 725 | 3,3% | Fís/VSi — 5 (12,5%) |
| 10C2 | 16 | 725 | 2,2% | Ing/Vir — 8 (9,4%) |
| 11C1 | 19 | 748 | 2,5% | Mat/ClaMe — 5 (11,6%) |
| 11C2 | 25 | 748 | 3,3% | Fís/Cadu — 5 (8,2%) |
| 12C1 | 29 | 807 | 3,6% | **Quí/CAl — 8 (19,0%)** |
| 12C2 | 24 | 750 | 3,2% | Quí/CAl — 6 (9,8%) |

**Acima do teto de 11%: 4 casos no 1º semestre, nenhum na Proposta 3.**

Ao comparar os semestres, use o **percentual**, nunca a contagem: o 1º
semestre tem 23 semanas letivas e o 2º tem 15 (turmas 10/12) ou 17 (9/11).
Como o número de provas é praticamente o mesmo, elas se espalham por menos
aulas no 2º semestre, o que sozinho empurra o percentual para cima — a
comparação já é desfavorável à Proposta 3 por construção.

## Pendências em aberto

### Células que não deu para ler (2)

| Turma | Quando | Conteúdo | Problema |
|---|---|---|---|
| 10C1 | sem. 14, terça | `p[[+` | Digitação acidental: sem disciplina e sem tempo |
| 10C1 | sem. 15, quarta | `Geografia \| Rios \| 06+` | Tempo ambíguo — seria 6º e 7º? |

Onde a disciplina faltava mas a turma irmã tinha prova no **mesmo dia e
nos mesmos tempos**, ela foi recuperada de lá (10 casos na 12C1) — é
comprovadamente a mesma prova, de professor comum. As correções que a
escola confirmou a mão ficam em `CORRECOES`, em `analisar_1semestre.py`.

## Decisões de interpretação — confirmadas pela escola

Todas as cinco foram validadas; ficam registradas porque não são óbvias
pelo código e voltarão a valer em rodadas futuras.

1. **O código `p` da grade** conta como Português. Ele aparece 1×/semana
   (`p`/Jana nas 9C, `p`/SMo nas 10C, `p`/Raf nas 11C), e na grade do 2º
   semestre esses mesmos professores aparecem como `gram` nas 10C e 11C —
   ainda assim, tratar como Português é o correto para esta contagem.
2. **A prova "Port (SMo/MFo/BPad)" das 10C** conta como prova de
   Português, e não como a combinada LP/LIT/RED — o tempo da Redação
   nela conta como cessão.
3. **`ingT` conta como o Inglês** das turmas 9, que não têm `ing` na
   grade.
4. **Simulados e AGs não contam como cessão** (23 dias no semestre):
   bloco fixo, fora da lógica de empréstimo, mesmo critério do 2º
   semestre.
5. **Células com grupos paralelos** (18): fica a disciplina **regular**,
   descartando a trilha de apoio/aprofundamento.

### Confirmação avulsa

- 12C1, semana 16, quarta, 3º tempo: **Sociologia**. A célula trazia só o
  tempo, e não dava para inferir da 12C2 (lá a Sociologia caiu no 6º).
  Caiu no próprio tempo de Sociologia da 12C1 (quarta, 3º, prof. Kle),
  então não gerou cessão nenhuma — e serve de conferência cruzada da
  grade extraída do PDF.
