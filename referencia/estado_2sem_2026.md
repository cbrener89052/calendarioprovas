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

Todas as turmas: **Período 1 = 24/08/2026 a 18/09/2026** (semanas 4 a 7).

**Alteração pontual (08/2026)**: o período 1 mudou de 17/08-11/09 (semanas
3-6) para 24/08-18/09 (semanas 4-7), a pedido do usuário. A **primeira
segunda chamada passa para 19/09/2026** (sábado seguinte à sexta 18/09) —
data administrativa, fora da janela de segunda a sexta usada pelo gerador,
não exige mudança de código, só o registro aqui. Isto é um dado concreto
desta rodada, não uma regra genérica — não foi incorporado à skill.

**Segundo ajuste (mesma rodada)**: o AG10 (10C1/10C2) **não** ficou no
último dia de P1 como se pensava inicialmente — a escola reagendou para
**25/09/2026** (sexta da semana 8), já dentro do pool de P2. A janela de
P1 (24/08 a 18/09) em si não mudou de novo com esse ajuste.

Período 2 varia por grupo (turmas que viajam à Alemanha terminam antes):

- **10C1, 10C2, 12C1, 12C2**: Período 2 = 14/09/2026 a 12/11/2026.
- **9C1, 9C2, 11C1, 11C2**: Período 2 = 14/09/2026 a 26/11/2026.

(A semana 7 agora é comum aos pools de P1 e P2 — já era assim na prática,
porque o pool de P2 sempre incluiu as semanas de P1 como fallback; a
mecânica de busca não muda.)

## Fim das aulas normais (para o relatório de tempos cedidos)

Data da última prova de 2ª chamada do semestre, confirmada pelo usuário —
usada para contar quantas semanas letivas ativas cada turma tem no
semestre (ver skill, item "Relatório de tempos cedidos"):

- **10C1, 10C2, 12C1, 12C2**: até **13/11/2026** (sexta da semana 15).
- **9C1, 9C2, 11C1, 11C2**: até **27/11/2026** (sexta da semana 17).

A semana vetada (12 a 16/10, conselho de classe) foi tratada como **zero
aula normal** — **confirmado pelo usuário**: não tem aula nenhuma nessa
semana.

## Limites de cessão de aula (Proposta 3)

Pedido da coordenação, aplicado só na Proposta 3 (as Propostas 1 e 2 ficam
sem eles, para comparação). Ver a mecânica na skill:

1. 2 ou 3 aulas semanais: no máximo 2 cessões no semestre — **3 para
   História, Geografia e GL** (exceção confirmada pelo usuário).
2. 1 aula semanal: não cede.
3. Nunca duas semanas seguidas sem contato com a turma.
4. Não ceder na semana da própria prova nem na anterior.
5. Teto de 11% das aulas programadas no semestre (alvo 10%).

**Resultado original desta rodada** (antes da regra de LP/LIT/RED ≥10 dias
do conselho, ver abaixo): fechou com **as cinco regras integrais, sem
nenhuma exceção**. Pior caso de cessão: 10,7% (contra 23,1% na Proposta 1).

**Atualização (08/2026, regra do LP/LIT/RED ≥10 dias do conselho)**: essa
nova exigência de data (ver skill) apertou demais a 10C1 especificamente —
sem nenhum limite de cessão ela fecha na hora, mas com os cinco limites
estritos não fecha de jeito nenhum, mesmo relaxando a regra 4 sozinha.
A **10C1 passou a precisar de um afrouxamento localizado**: regra 4 e
regra 3 relaxadas nela, mais o teto de cessão elevado em +1 (só nela —
as outras sete turmas continuam cumprindo as cinco regras integrais).
Pior caso de cessão na 10C1 com o afrouxamento: 14,3% (GL) — acima do
teto de 11% pedido pela escola, mas é o preço da nova exigência de data
combinada com os limites de cessão; sem a folga localizada a 10C1 não
fecha. `verificar_calendario.py` já trata isso como aviso esperado, não
como falha do checklist (mesmo tratamento que já dava à regra 4).

A semente da busca importa: com restrições tão apertadas, ela decide se há
ou não solução dentro do orçamento de nós. A semente 20261107 deixava a
11C1 sem solução (obrigando a relaxar a regra 4 nela). A semente 7 (usada
até esta atualização) fechava as oito turmas integralmente sob as regras
antigas, mas com a nova regra do LP/LIT/RED ela não fecha a 10C1 nem com
tudo relaxado — a **semente 3** fecha, com o afrouxamento localizado
descrito acima. Está fixada em `SEED_PROPOSTA_3`.

O afrouxamento do teto de cessão passou a ser **por turma**
(`folga_extra` em `montar_proposta`/`main()`), não mais global: antes,
subir o teto para fechar uma turma difícil estourava a folga de todas as
outras também, mesmo as que já fechavam com as regras integrais.

## Datas de simulados/AG (fixas, contam como avaliação, não podem ser movidas)

| Código | Turmas | Data(s) | Período |
|---|---|---|---|
| AG9 | 9C1, 9C2 | 02/10/2026 | P2 |
| AG10 | 10C1, 10C2 | **25/09/2026** (era 11/09, passou por 18/09 antes de fechar em 25/09) | P2 |
| S3-11 | 11C1, 11C2 | 25/08 e 26/08/2026 | P1 |
| S4-11 | 11C1, 11C2 | 26/10 e 27/10/2026 | P2 |
| S4-12 | 12C1, 12C2 | 16/09 e 17/09/2026 | P2 |

Fonte: `Calendário de simulados e avaliação global 2026_v2.pdf` (versão
revisada, upload de 08/2026) + correção verbal do usuário sobre o AG10
(a planilha-modelo local, conferida pelo usuário, mostrava o AG10 destacado
em amarelo na semana 8 — 25/09 — e não na semana 7 como o PDF sugeria).
AG9, S3-11 e S4-11 conferidos contra o PDF, vieram idênticos ao valor
anterior. O S4-12 do PDF novo veio com o ano grafado "2025" ("16.09.2025" /
"17.09.2025") — tratado como erro de digitação e mantido em 2026, pois
bate exatamente com a data já confirmada anteriormente e um 2025 seria
passado em relação a este planejamento; **sinalizar ao usuário**, não foi
uma confirmação explícita.

Simulados extras (EX-TURMA-N): **ainda não definidos** pelo usuário —
perguntar antes de fechar o calendário final, ou deixar espaço reservado.

**Reconferência (08/2026)**: novo upload do PDF oficial (`Calendário de
simulados e avaliação global 2026.pdf`, "Proposta de Calendário das
Avaliações Globais e Simulados de 2025" no título — nome do arquivo tem
"2025" mas as datas são de 2026) confirmou os 5 valores acima item a
item, inclusive o AG10 em 25.09.2026 — bate exatamente com o valor já
corrigido nesta rodada. Nenhuma mudança adicional necessária. O S4-12
segue com o mesmo ano grafado "2025" nesse PDF novo também — mesma
suposição de erro de digitação mantida.

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
