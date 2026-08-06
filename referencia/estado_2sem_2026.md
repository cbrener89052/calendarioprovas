# Estado do trabalho — Calendário de Provas 2º semestre 2026

Este arquivo guarda os fatos e decisões já confirmados com o usuário para
esta rodada específica (2º semestre de 2026), para retomar o trabalho em
qualquer ambiente (Cowork ou Claude Code) sem perder contexto. As regras
genéricas e reutilizáveis já estão na skill `calendario-provas`; aqui só
ficam os dados concretos deste semestre.

## Arquivos de entrada (na pasta CALENDARIODEPROVAS)

- `Horario modelo/Klausurplan_2026_1SEM.xlsx` — calendário do 1º semestre já
  executado (referência de disciplinas/tempos, com inconsistências) + aba
  `Planungshilfe 2.Sem` com a grade em branco (datas) do 2º semestre.
- `Klausurplan_2026_2SEM.xlsx` (raiz da pasta) — modelo do 2º semestre;
  a aba `10C2` já tem as datas certas preenchidas (semanas 1 a 20, de
  03/08/2026 a 18/12/2026). As demais abas de turma ainda têm datas do 1º
  semestre e precisam ser atualizadas com essas mesmas semanas antes de
  preencher.
- `horarios turmas/turmas9a12_2osemestre2026.pdf` — horário-base (grade
  Untis) de todas as turmas, 16 páginas. Só as 8 páginas das turmas C
  interessam: 9C1 (pág 16), 9C2 (pág 15), 10C1 (pág 12), 10C2 (pág 11),
  11C1 (pág 8), 11C2 (pág 7), 12C1 (pág 4), 12C2 (pág 3). Extração de texto
  simples perde o mapeamento dia/tempo — usar visão computacional
  (renderizar a página em imagem, ex. `pdftoppm -png -r 200`).
- `siglas/siglas_profs_aux_etc.xlsx` — sigla → nome do professor.
- `Calendário de simulados e avaliação global 2026_v2.pdf` (em uploads,
  cópia dos dados abaixo) — datas oficiais dos simulados/AG.

## Estrutura de saída combinada

**3 arquivos xlsx separados** (um por proposta), cada um com **8 abas**
(uma por turma: 9C1, 9C2, 10C1, 10C2, 11C1, 11C2, 12C1, 12C2), no mesmo
layout do `Horario modelo` (grade semanal, células de prova em 3 linhas:
disciplina-professor / sala / tempo). Salvar na pasta `Horario desenvolvido`.

## Períodos de provas (por grupo de turma)

Todas as turmas: **Período 1 = 17/08/2026 a 11/09/2026**.

Período 2 varia por grupo (turmas que viajam à Alemanha terminam antes):

- **10C1, 10C2, 12C1, 12C2**: Período 2 = 14/09/2026 a 12/11/2026.
- **9C1, 9C2, 11C1, 11C2**: Período 2 = 14/09/2026 a 26/11/2026.

## Datas de simulados/AG (fixas, contam como avaliação, não podem ser movidas)

| Código | Turmas | Data(s) | Período |
|---|---|---|---|
| AG9 | 9C1, 9C2 | 02/10/2026 | P2 |
| AG10 | 10C1, 10C2 | 11/09/2026 | P1 |
| S3-11 | 11C1, 11C2 | 25/08 e 26/08/2026 | P1 |
| S4-11 | 11C1, 11C2 | 26/10 e 27/10/2026 | P2 |
| S4-12 | 12C1, 12C2 | 16/09 e 17/09/2026 | P2 |

Simulados extras (EX-TURMA-N): **ainda não definidos** pelo usuário —
perguntar antes de fechar o calendário final, ou deixar espaço reservado.

## Regras específicas confirmadas para esta escola/rodada

- "esp"/"Spo" no horário-base = **Educação Física**, não Espanhol. Não tem
  prova.
- Grupos paralelos (línguas eletivas, ex. Alemão/DaF com vários
  professores no mesmo tempo): **1 prova só, aplicada simultaneamente**,
  cada professor aplica pro seu grupo; conta como 1 avaliação da turma.
- "Pred" (visto no calendário do 1º sem) = prova de **Redação**.
- "AR" = sinalização de atendimento a responsáveis, **não é prova**.
- "SIP" = Semana de Informação Profissional, **não ocorre no 2º semestre**.
- Nas turmas **9C1 e 9C2**: Biologia, Química e Física têm **apenas 1 prova
  no semestre inteiro** (não 1 por período), usando **1 tempo cada**.
  Nas demais séries essas disciplinas seguem a regra normal (1 prova por
  período, tempos a confirmar/observar no modelo do 1º sem — ver seção
  abaixo).
- Filosofia e Sociologia: 1 tempo semanal na grade → 1 prova no semestre
  inteiro, 1 tempo.

## Tempos por disciplina observados no 1º semestre (a confirmar/padronizar)

Do calendário do 1º semestre (`Horario modelo`), padrão observado (ver
skill para a ressalva de que a extração automática pode vir desalinhada):

- Matemática: 2 tempos
- Português (LP/LIT/RED): 3 tempos
- Inglês: 2 tempos
- Alemão (DaF/GL): 2 tempos, grupos paralelos
- Biologia: 2 tempos (exceto 9C: 1 tempo, 1x/semestre)
- História: 2 tempos
- Redação (Pred): 2 tempos
- Física: inconsistente entre turmas no 1º sem (1 ou 2 tempos) — decidir
  2 tempos como padrão para turmas que não são 9C (usuário ainda não
  confirmou explicitamente esse padrão, só confirmou a exceção do 9C).
- Geografia: inconsistente (1 ou 2 tempos) — mesma pendência acima.
- Química: célula de tempo veio vazia/ilegível na extração — mesma
  pendência acima (exceto 9C: 1 tempo, 1x/semestre).

**Pendência em aberto**: confirmar com o usuário se Física, Geografia e
Química (fora do 9º ano) usam 2 tempos padronizados, ou se variam por
turma.

## Extração do horário-base (progresso)

Já extraído e conferido (sem ambiguidade de siglas, todas batem com
`siglas_profs_aux_etc.xlsx`):

- **9C1** (segunda a sexta, tempos 1-15): ver print da grade — disciplinas
  com grupos paralelos em Espanhol... corrigido para Educação Física
  ("esp"), Alemão (DaF), GL, ingT (inglês optativo).

Faltam extrair (imagens já renderizadas em alta resolução, prontas para
leitura visual): 9C2, 10C1, 10C2, 11C1, 11C2, 12C1, 12C2.

## Próximos passos

1. Confirmar a pendência de tempos (Física/Geo/Química fora do 9º ano).
2. Extrair horário-base das 7 turmas restantes via visão computacional.
3. Copiar a semana-grade (linhas de data) da aba `10C2` para as outras 7
   abas de turma no arquivo de modelo do 2º semestre, se ainda não feito.
4. Gerar as 3 propostas de calendário (3 arquivos xlsx, 8 abas cada).
5. Gerar relatório de trocas de tempo entre professores.
6. Rodar o checklist final da skill antes de entregar.
