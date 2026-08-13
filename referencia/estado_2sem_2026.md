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

## Ajustes manuais na Proposta 3 (08/2026, a pedido do usuário)

Editados **diretamente na planilha já gerada** (não passaram pelo
solver, não entraram na skill nem no `gerar_calendario.py` — exceto o
limite de data da série 9/11, ver abaixo) — se a Proposta 3 for
regenerada do zero, esses ajustes se perdem e precisam ser reaplicados
manualmente. Estado **final**, já com as correções de espaçamento da
2ª rodada incorporadas:

1. **10C1/10C2**: Química movida para a 1ª ocorrência de LP/LIT/RED
   (24/08); LP/LIT/RED movida para 31/08 (semana 5, não para a semana 7
   que a Química deixou — a semana 7 já tinha Matemática, o que violava
   o grupo 1, e ficava a só 2 semanas da 2ª ocorrência de LP/LIT/RED,
   28/09, violando o piso de 4). A 2ª ocorrência de cada uma (LP/LIT/RED
   28/09, Química 09/11) não mudou.
2. **9C1/9C2**: Português (Jana), 1ª ocorrência, movida de 26/08 para
   02/09; 2ª ocorrência movida de 23/09 para 21/10 (restaura os 7
   semanas de espaçamento).
3. **11C1/11C2**: Matemática movida de 27/08 para 21/09 (semana 8) —
   as duas datas sugeridas pelo usuário (28/08 e 04/09) tinham
   problema (28/08 continua na semana do simulado S3-11; 04/09 já
   estava no teto de 3 provas/semana), por isso a semana 8 foi usada
   no lugar.
4. **12C1/12C2**: ciclo de 4 provas — LP/LIT/RED 25/08→01/09, GL
   27/08→25/08, Física 15/09→27/08, Biologia (1ª ocorrência) 01/09→15/09
   (a vaga que a Física deixou). Biologia, 2ª ocorrência, movida de
   06/10 para 03/11 (restaura os 7 semanas de espaçamento com a 1ª).
5. **12C1/12C2**: Filosofia (LAn) movida de 11/11 para 30/09.
6. **9C1/9C2**: Física movida de 16/11 para 23/11 (semana 17, segunda).
7. **11C1/11C2**: Química, 2ª ocorrência, movida de 17/11 para 24/11
   (semana 17, terça). Os itens 6 e 7 atendem o pedido de a semana 17
   ter pelo menos 1 prova até quarta-feira (ver skill) — exigiu também
   estender o limite de data da série 9/11 no código (item abaixo).

**Regra conscientemente quebrada** por causa do item 1 (usuário pediu
para não se preocupar): duas disciplinas do grupo 1 na mesma semana em
9C1/9C2 (semana 5: Port + Ing, aceitável pela exceção "uma delas é
Inglês").

### 3ª rodada de ajustes (mesmo dia, 08/2026)

8. **10C1/10C2**: Matemática ↔ Física, troca completa — não deu pra
   trocar só a 1ª ocorrência de cada (o pedido original): a semana 5 já
   tinha LP/LIT/RED + Inglês (2 disciplinas do grupo 1, no limite da
   exceção "uma delas é Inglês"), então colocar a Matemática lá criaria
   3 disciplinas do grupo 1 na mesma semana, que a regra nunca permite
   (mesmo com Inglês no meio). Resultado: **Física** vai para as semanas
   7 e 12 (onde a Matemática estava); **Matemática** vai para as semanas
   10 e 15 (a 15 é nova — a semana 12 sozinha ficava a só 3 semanas da
   semana 15... na verdade a semana 12 ficou livre pra Física porque a
   Matemática saiu de lá; a nova 2ª ocorrência da Matemática foi para a
   semana 15 pra manter as 4 semanas mínimas da 1ª, que ficou na semana
   10). Ambas as trocas mantêm o piso de 4 semanas (ambas com gap de 5).
9. **10C1/10C2**: LP/LIT/RED, 2ª ocorrência, movida da semana 9 para a
   **semana 13** — confirmado pelo usuário que o conselho de classe
   relevante para a 10C é o conselho final (17/11, marcação "CC 10,12"),
   não o do meio do semestre (semana 11); a regra de 10 dias antes do
   conselho, portanto, não bloqueia a semana 13 nessa turma (07/11, data
   limite pelos 10 dias, é bem depois do fim da semana 13). **Corrigido
   no código** (mesmo dia): `LIMITE_LPLITRED_CONSELHO` deixou de ser um
   número único e virou um limite por grupo de turma, calculado a partir
   da marcação "CC <séries>" do modelo — usa o maior entre o limite do
   conselho do meio do semestre e o do conselho final do grupo. Resultado
   nesta rodada: `10_12` → semana 14; `9_11` → semana 17.
   `verificar_calendario.py` não acusa mais nada para a semana 13.
10. **9C1/9C2**: Biologia, Química e Física (1 única ocorrência cada,
    já que são de prova única nessas turmas) movidas para as semanas
    12-14 — Biologia p/ semana 13 (segunda), Química p/ semana 13
    (sexta), Física p/ semana 14 (quinta).
11. **9C1/9C2**: Redação, 2ª ocorrência, movida de 19/11 para 23/11
    (semana 17, segunda) — repõe a prova que a semana 17 perdeu quando a
    Física saiu de lá para o item 10 (mantém "semana 17 precisa de prova
    até quarta"). Usa os tempos 3-4 dessa segunda-feira, não 1-2: o 2º
    tempo de segunda é a única aula semanal de Física na grade da 9C2 e
    não pode ceder (regra 2).
12. **12C1/12C2**: Sociologia movida de 23/09 para 07/10 (pedido
    específico do usuário, dentro do espírito do item "disciplina de 1
    único tempo" acima).

Todos os efeitos colaterais de grupo 1 e distância mínima dessa rodada
foram corrigidos nos próprios itens acima, e o item 9 deixou de ser um
falso positivo depois da correção no código — `verificar_calendario.py`
fecha sem nenhum PROBLEMA nesta versão da Proposta 3.

## Limite de data da série 9/11 estendido (08/2026)

`LIMITE_DIA["9_11"]` (`gerar_calendario.py`) e `LIMITE["9_11"]`
(`verificar_calendario.py`) foram estendidos de quinta da semana 16
(19/11) para **quinta da semana 17 (26/11)** — pedido do usuário: as
aulas normais da série 9/11 seguem até 27/11 (sexta da semana 17,
mesma data da 2ª chamada "2CH 9,11"), então a semana 17 é letiva e
precisa poder receber provas. Essa é uma mudança **de código** (não só
manual na Proposta 3 atual) — vale para qualquer regeneração futura.

## Datas concretas das regras novas (08/2026)

- **Véspera de 2ª chamada, turmas 9C** (ver skill): a 2ª chamada da
  série 9/11 está marcada (`"2CH 9,11"`) em **27/11/2026** (sexta,
  semana 17) — a véspera protegida é **26/11/2026** (quinta).
- **12C — 6 dias do último conselho de classe** (ver skill): a marcação
  `"CC 10,12"` no modelo está em **17/11/2026** (terça, semana 16) —
  6 dias antes é **11/11/2026**; provas da 12C1/12C2 não deveriam
  passar dessa data.

## Regra de presença do professor — prioridade 1 (08/2026)

Pedido do usuário: revisão manual encontrou provas de professor comum
entre turmas irmãs (GL, Física, Redação) aplicadas em blocos onde
**nenhum** dos professores citados tinha aula própria (nem na turma, nem
na turma irmã) — o professor não estaria fisicamente presente para
acompanhar a prova. Regra nova, marcada como **prioridade 1** (nunca
relaxa) na skill: todo professor citado precisa de pelo menos 1 tempo
próprio no bloco (turma OU turma irmã); quando há mais de um professor
citado, basta 1 deles satisfazer a regra.

**Causa raiz**: os 3 casos vieram de **edições manuais** feitas em rodadas
anteriores desta mesma conversa (não do algoritmo do gerador) — ao mover
GL e Física da 12C1/12C2 e a Redação da 9C1/9C2 para novos dias/tempos a
pedido do usuário, os tempos escolhidos não foram reconferidos contra a
grade-base para o novo dia. Verificado que o caminho de resolução do
gerador (`_tentar_par`, usado quando há professor comum entre turmas
irmãs) **já garantia** essa propriedade estruturalmente antes mesmo
desta correção — smoke test rodando `_tentar_par` para os 4 pares de
turmas irmãs com a Proposta 3 (semente `SEED_PROPOSTA_3`) deu **zero**
violações da regra nos exames comuns gerados. Ainda assim, o filtro foi
reescrito para checar o professor citado explicitamente (função nova
`professor_presente_no_bloco`), em vez de depender implicitamente da
premissa "1 professor por disciplina por turma nesse caminho" — ver
skill para detalhes.

**6 violações encontradas e corrigidas na Proposta 3** (todas dentro da
mesma semana/dia, só mudando o(s) tempo(s); confirmado com `G.GRADES`
antes de aplicar):

| Turma(s) | Disciplina | Semana/dia | Tempos (antes) | Tempos (depois) | Motivo do novo tempo |
|---|---|---|---|---|---|
| 12C1/12C2 | GL (CBu-EFr-Eth) | sem4, terça (25/08) | 9º-10º | **5º-6º** | GL próprio no 6º; 5º é 'apr' (doador seguro, 4x/semana) |
| 12C1/12C2 | Física (Cadu) | sem4, quinta (27/08) | 1º-2º | **2º-3º** | 12C2 tem fis próprio no 3º (resolve via turma irmã); 2º é 'art' (doador seguro, 2x/semana) |
| 9C1/9C2 | Redação (Raf) | sem17, segunda (23/11) | 3º-4º | **6º-7º** | 9C1 tem pred próprio no 7º (resolve via turma irmã); 6º é GL (doador seguro, 3x/semana) |

Depois da correção: `verificar_calendario.py` (novo item "0." do
checklist) e os dois scripts de revisão ad hoc (`revisar_presenca_
professor.py`/`2.py`, no scratchpad, não commitados) confirmam **zero**
violações. Os 42 AVISOs pré-existentes (regras 1/3/4/5 de cessão já
documentadas como relaxamento conhecido) não mudaram.
`Relatorio_Tempos_Cedidos_Proposta_3.xlsx` e `Tabela_Provas_por_Turma_
Proposta_3.xlsx` foram regenerados depois do ajuste.

## Extração do horário-base (progresso)

Já extraído e conferido (sem ambiguidade de siglas, todas batem com
`siglas_profs_aux_etc.xlsx`):

- **9C1** (segunda a sexta, tempos 1-15): ver print da grade — disciplinas
  com grupos paralelos em Espanhol... corrigido para Educação Física
  ("esp"), Alemão (DaF), GL, ingT (inglês optativo).

Faltam extrair (imagens já renderizadas em alta resolução, prontas para
leitura visual): 9C2, 10C1, 10C2, 11C1, 11C2, 12C1, 12C2.

## 7ª rodada de ajustes manuais na Proposta 3 (08/2026, a pedido do usuário)

Todos os alvos foram conferidos contra `G.GRADES` (presença do professor,
cruzamento de intervalo, conflitos de dia/semana, grupo 1, distância
mínima e regra 4 de cessão) antes de aplicar, com `verificar_calendario.py`
fechando em 0 PROBLEMA ao final de cada etapa.

1. **12C1/12C2**: permuta entre LP/LIT/RED (01/09, sem5) e GL (25/08,
   sem4) — mesmo dia (terça) e mesmos tempos de cada uma, só trocaram de
   semana.
2. **12C1/12C2**: Soc e Fil movidas para a janela semana 12-14 pedida
   (Fil → sem12, quarta, 10º tempo; Soc → sem13, quarta, 2º tempo).
   Não precisou "subir" nenhuma outra prova (sem12/sem13 tinham espaço).
   Um detalhe corrigido no meio do caminho: a 1ª tentativa (Fil→sem13,
   Soc→sem12, ambas nos tempos originais) criava cessão de Fis/Cadu e
   Hist/Wag exatamente na véspera/semana da prova própria deles — trocado
   o bloco de tempo do Fil (10º em vez de 4º) e invertidas as semanas
   para eliminar os dois casos.
3. **11C1/11C2**: LP/LIT/RED (2ª ocorrência) sem9 → sem14, em bloco NOVO
   (quinta, 9º ao 11º tempos, doadores Inglês/Bea e Ed.Física) em vez de
   manter o bloco antigo (terça, 8º-10º, doador Biologia) — Bio tem
   prova própria na semana 15, doar na semana 14 violaria a regra 4.
   Matemática (2ª) sem14 → sem16, mesmo dia/tempo (quarta, 2º-3º tempos).
   Efeito colateral aceito: Ed.Física/- passa de 2 para 4 cessões no
   semestre (12,5%, acima da meta de 11%) — foi o único bloco sem cruzar
   o intervalo do recreio nem violar a véspera da prova de Biologia
   (checados todos os blocos válidos, um por um, antes de escolher).
4. **10C2**: Inglês (2ª ocorrência) sem15 (quarta) → sem12 (terça),
   tempo próprio de Inglês nessa turma.
5. **10C1/10C2**: Matemática (2ª ocorrência) tirada da véspera da 2ª
   chamada (quinta, 12/11, sem15) → mesma semana 15, mas terça (10/11),
   10º-11º tempos — dentro do limite de 6 dias do conselho final (17/11)
   e longe da véspera. **Nova regra na skill**: turmas 10 não devem ter
   prova na véspera da 2ª chamada (marcação `"2CH 10,12"`), flexibilizável
   se não houver outra forma de fechar o horário — ainda não implementada
   no gerador, só documentada e aplicada manualmente aqui.
6. **9C1/9C2**: Inglês (2ª ocorrência) sem12 (23/10) → sem10 (09/10),
   mesmo dia (sexta) e mesmo tempo. Hist e Port não precisaram de ajuste
   — já estavam a 7-8 semanas de distância entre as duas ocorrências
   (dentro do ideal).
7. **9C1/9C2**: Biologia (única ocorrência) sem13 → sem15 (09/11);
   Redação (2ª ocorrência) sem17 → sem16 (16/11) — consolida as duas na
   semana 16 (antes vazia) em vez de manter cada uma isolada. Efeito: a
   semana 17 da 9C ficou sem nenhuma prova regular (só a marcação de 2ª
   chamada) — aceito conscientemente, ver a nova regra de "consolidação
   de semanas" na skill, que passa a ter prioridade sobre a regra antiga
   de "semana 17 sempre com 1 prova" quando as duas entrarem em conflito.
   Um detalhe corrigido no meio do caminho: o bloco original de Biologia
   (segunda, 1º tempo) doava de Redação/Raf na 9C2 — como a própria
   Redação passou a cair na semana seguinte (16), isso violaria a regra
   4 (véspera). Trocado o bloco de Biologia para terça/1º tempo (doador
   Português/Jana) para eliminar o conflito.

**Nova regra na skill (consolidação de semanas)**: quando houver a opção
de encaixar 2 provas numa semana já usada por outra, em vez de gastar uma
semana a mais só para mantê-las separadas, isso é preferível — é uma
checagem de revisão pós-horário-fechado (não faz parte do algoritmo de
busca), motivada pela 9C ter a semana 16 inteira livre enquanto a Redação
e a 2ª chamada empurravam a semana 17 para o limite.

Relatórios regenerados ao final: `Relatorio_Tempos_Cedidos_Proposta_3.xlsx`,
`Tabela_Provas_por_Turma_Proposta_3.xlsx`, `Relatorio_trocas_de_tempo.md`
e `.xlsx`. `verificar_calendario.py` fecha em 0 PROBLEMA, 45 AVISOs (todos
de regras já documentadas como relaxamento conhecido).

## 8ª rodada de ajustes manuais na Proposta 3 (08/2026, a pedido do usuário)

- **12C1/12C2**: simulado S4-12 movido de 16-17/09 (semana7, quarta+quinta)
  para 23-24/09 (semana8, quarta+quinta) — mesmos dias da semana, só
  trocou de semana. Semana8 estava totalmente livre para as duas turmas
  (0 provas), sem conflito de dia nem de limite de 3 avaliações.
  **Implementado no código**: `SIMULADOS["12C1"]`/`SIMULADOS["12C2"]`
  em `gerar_calendario.py` atualizados para `(8, 3, ...)`/`(8, 4, ...)`
  — necessário porque `verificar_calendario.py` (item 8 do checklist)
  compara as datas gravadas na planilha contra `G.SIMULADOS` e acusaria
  PROBLEMA se só a planilha fosse editada sem atualizar essa constante.

`verificar_calendario.py` fecha em 0 PROBLEMA, mesma contagem de AVISOs
de antes (45). Os 4 relatórios foram regenerados.

## 9ª rodada de ajustes manuais na Proposta 3 (08/2026, a pedido do usuário)

- **12C1/12C2**: LP/LIT/RED (2ª ocorrência) movida de 02/10 (semana9,
  sexta) para 09/10 (semana10, sexta) — mesmo dia da semana e mesmo
  bloco de tempos (1º ao 3º), só trocou de semana. Semana10 já tinha
  só GL (quinta) para as duas turmas, sem conflito de dia nem de limite
  de 3 avaliações. Efeito colateral positivo: a distância até a 1ª
  ocorrência (semana4) sobe de 5 para 6 semanas, mais perto do ideal de 7.

`verificar_calendario.py` fecha em 0 PROBLEMA, mesma contagem de AVISOs
de antes (45). Os 4 relatórios foram regenerados.

## 10ª rodada de ajustes manuais na Proposta 3 (08/2026, a pedido do usuário)

- **12C2**: Inglês (2ª ocorrência) movida de 28/09 (semana9, segunda)
  para 05/10 (semana10, segunda) — mesmo dia da semana e mesmo bloco de
  tempos (4º-5º), só trocou de semana. (12C1 não tinha prova em 28/09 —
  o pedido "turmas 12C" só se aplicava à 12C2 nesse caso, já que o
  Inglês da 12C1 tem professor diferente e datas próprias.) Semana10 já
  cria a combinação Inglês + LP/LIT/RED (grupo 1) na mesma semana, que é
  a exceção permitida (uma delas é Inglês).
- **12C1/12C2**: GL movida de 08/10 (semana10, quinta) para 01/10
  (semana9, quinta) — mesmo dia da semana e mesmo bloco de tempos
  (9º-10º), só trocou de semana.

`verificar_calendario.py` fecha em 0 PROBLEMA, mesma contagem de AVISOs
de antes (45). Os 4 relatórios foram regenerados.

## 5º relatório: Provas por Professor (08/2026, a pedido do usuário)

Formalizados na skill os 4 relatórios já entregues até aqui (trocas de
tempo, tabela-resumo por turma, tempos cedidos) como a rotina obrigatória
de 5 scripts após qualquer edição manual (o 4º já era `verificar_
calendario.py`), e adicionado um **5º relatório novo**: `Provas_por_
Professor_Proposta_3.xlsx`, gerado por `exportar_provas_por_professor.py`.

- Tabela única (não uma aba por turma), organizada por professor: cada
  linha é uma prova que aquele professor precisa acompanhar, com data,
  dia da semana, tempos e turma(s).
- Quando a mesma prova é professor comum entre turmas irmãs (mesma
  data/tempos, aplicada simultaneamente), vira 1 linha só com as turmas
  juntas na coluna "Turma(s)" — não duplica.
- Não inclui simulados/AG (não têm 1 professor responsável específico).
- Reaproveita `carregar_siglas` de `exportar_tabelas_turma.py` para
  nome completo dos professores.

`verificar_calendario.py` continua em 0 PROBLEMA (o relatório novo é só
leitura da planilha final, não muda o calendário). Todos os 5 relatórios
regenerados.

## Definição geral de turma irmã (08/2026, a pedido do usuário)

`PARES_IRMAS` (e `IRMA`, derivado dele) deixou de ser uma lista fixa
mantida à mão (`[("9C1","9C2"), ("10C1","10C2"), ("11C1","11C2"),
("12C1","12C2")]`) e passou a ser **calculado a partir do nome de cada
turma**: duas turmas são irmãs quando têm a mesma série e a mesma letra,
diferindo só no número final (ex.: "11C1"/"11C2"; **não** "11C1"/"11R1",
mesmo com a mesma série 11). Motivo: a escola pode ter turmas de outra
letra além de "C" no futuro (o usuário deu o exemplo de uma turma "R"),
e a regra precisa valer automaticamente para elas sem precisar editar
`gerar_calendario.py` cada vez.

- Nova função `calcular_pares_irmas(turmas)` em `gerar_calendario.py`,
  chamada com `GRADES.keys()`. Só pareia prefixos (série+letra) com
  exatamente 2 turmas.
- Conferido que reproduz **exatamente** os 4 pares antigos (mesmo
  conjunto, mesma ordem — via ordenação por série numérica, não por
  texto, para não inverter "10C" antes de "9C").
- `verificar_calendario.py` fecha em 0 PROBLEMA, mesma contagem de
  AVISOs. Os 5 relatórios regenerados saíram **byte a byte idênticos**
  aos anteriores (confirma que a mudança é 100% transparente para a
  Proposta 3 atual, só muda como o código descobre os pares, não o
  resultado).
- Regra documentada na skill, na seção "Regras de distribuição das
  provas", como base tanto da regra de presença do professor (prioridade
  1) quanto da regra de professor comum entre turmas irmãs.

## Isonomia História/Geografia — 11C1/11C2 (08/2026, a pedido do usuário/Profa. Verena)

Origem: a Profa. Verena (História) reclamou que a 1ª prova de História
(01/09, 11º-12º tempos) usava sempre a aula dupla própria da 11C2 (nunca
a da 11C1) como âncora — checado contra a grade, a queixa procedia, e o
mesmo padrão se repetia na 2ª prova (20/10). O pedido literal dela (mover
para os tempos 2º-3º, aula dupla da 11C1) esbarrava em Química cedendo na
véspera da própria prova (11C2). Depois de várias rodadas de análise
(mover só a Geografia, tentar datas específicas como 16/11), a solução
final, sem perder nenhuma aula de Química, foi:

1. **Geografia (2ª ocorrência)**: 05/10 → **16/11** (semana 10 → semana
   16), mesmo dia/tempos (segunda, 6º-7º). Motivo: espaçar as 2 provas de
   Geografia para o ideal de pelo menos 7 semanas (antes eram só 5).
2. **História (2ª ocorrência)**: 20/10, terça 9º-10º → **20/10, quarta,
   1º-2º tempos** (mesma semana 12, só muda o dia/bloco). Bloco 50/50: a
   11C1 cede 1 tempo próprio de História, a 11C2 também — nenhuma cede
   os 2 tempos inteiros como antes.
3. **Geografia (1ª ocorrência)**: 31/08 → **05/10** (semana 5 → semana
   10), mesmo dia/tempos (segunda, 2º-3º). Só foi possível **depois** do
   item 1 abrir espaço: com a 2ª ocorrência da Geografia lá na semana 16,
   a 1ª pôde se mover livremente dentro do piso de 4 semanas.
4. **História (1ª ocorrência)**: 01/09, terça 11º-12º → **01/09, quarta,
   1º-2º tempos** (mesma semana 5, só muda o dia/bloco). Só ficou
   possível **depois** do item 3 tirar a Geografia da semana 5 — sem
   isso, o bloco de quarta doaria Geografia bem na semana da prova
   própria dela.

Efeito colateral corrigido no meio do caminho: a 1ª tentativa de mover a
Geografia (1ª ocorrência) usou a semana 9, que ficou colada na véspera de
uma cessão de Matemática que já existia há tempos (prova de Matemática
da semana 8 sempre cedeu um tempo de Geografia dentro do próprio bloco
dela) — trocado para a semana 10, que não tem nenhum vizinho assim.

`verificar_calendario.py` fecha em 0 PROBLEMA, 43 AVISOs (menos que os
45 anteriores — a mudança até resolveu 2 avisos pré-existentes). Os 5
relatórios regenerados.

## Sociologia removida das turmas 11C (08/2026, a pedido do usuário)

"Nas turmas 11C não haverá prova de sociologia" — removida a prova de
Sociologia (semana 12, sexta, 4º tempo) da 11C1/11C2. A aula normal de
Sociologia continua na grade dessas turmas (pode seguir sendo doadora de
tempo); só a avaliação saiu. Sociologia continua com prova normalmente
nas demais séries (ex.: 12C).

**Implementado no código** (não só a planilha): novo dict
`SEM_PROVA_POR_TURMA` em `gerar_calendario.py`, consultado por
`montar_exames()` além do `SEM_PROVA` global — permite exceções de
"sem prova" por turma específica, sem afetar as demais turmas que têm
a mesma disciplina examinada. Hoje só tem `{"11C1": {"soc"}, "11C2":
{"soc"}}`, mas o mecanismo serve para qualquer exceção futura do tipo.

`verificar_calendario.py` fecha em 0 PROBLEMA, mesma contagem de AVISOs
(43). Os 5 relatórios regenerados. O slot vago (semana 12, sexta) ficou
livre, sem nada alocado nele por enquanto.

## Inglês (12C1/12C2): 2ª prova removida (08/2026, a pedido do usuário)

"Pode retirar a segunda prova de inglês do calendário tanto da turma
12c1 quanto da turma 12c2." Removida a 2ª ocorrência de Inglês da
12C1 (semana 14, quinta) e da 12C2 (semana 10, segunda). A 1ª ocorrência
de cada turma permanece (12C1: semana 5, quinta; 12C2: semana 4,
segunda/24-08). Cada turma tem professor diferente (PaH/12C1, Isb/12C2,
não é professor comum), então a mudança é independente entre as duas.

**Implementado no código**: novo dict `UMA_PROVA_POR_TURMA` em
`gerar_calendario.py`, consultado por `montar_exames()` — quando a
disciplina está em `DOIS_TEMPOS` mas a turma tem exceção registrada
aqui, só a 1ª ocorrência é gerada. `verificar_calendario.py` (item 5,
número de provas por disciplina) também consulta esse dict, para não
acusar falsamente "Ing tem 1 prova, esperado 2" nas turmas com a
exceção. Mesmo princípio do `SEM_PROVA_POR_TURMA` (Sociologia/11C) --
fato concreto deste semestre, não regra geral da escola, então **não**
documentado como regra na skill.

`verificar_calendario.py` fecha em 0 PROBLEMA, mesma contagem de AVISOs
(43). Os 5 relatórios regenerados.

**Atualização**: usuário confirmou seguir com os tempos 5º-6º, mantendo
a data real 24/08 (a 25/08 mencionada originalmente não tem aula de
Inglês na 12C2 -- confirmado como engano). Aplicado: 12C2, 1ª prova de
Inglês, 24/08, tempos 4º-5º → **5º-6º** (célula destacada por cruzar o
intervalo do recreio -- é o único bloco que cobre os 2 tempos próprios
de Inglês nesse dia; o bloco anterior, 4º-5º, emprestava 1 tempo de
Alemão). Efeito colateral positivo: elimina a cessão de Alemão que
existia nesse bloco. `verificar_calendario.py` fecha em 0 PROBLEMA,
mesma contagem de AVISOs (43). Confirmado a pedido do usuário: **este
fato (e a remoção da 2ª prova, acima) não entra na skill como regra**
-- é um pedido específico deste semestre, registrado só aqui.

## GL (9C1/9C2): 1 tempo por prova + repositionamento (08/2026, a pedido do usuário)

### Parte 1: Correção de número de tempos

"A prova de GL das turmas 9C1 e 9C2 são aplicadas em apenas um tempo de
aula" — a disciplina GL nunca tem aula dupla nessas turmas (só tempos
únicos: segunda t6, quarta t6, sexta t5), diferente de outras turmas
onde GL é 2 tempos. As provas de GL estavam erroneamente lançadas como
2 tempos (4º e 5º tempos) em ambas as ocorrências.

**Implementado no código**: novo dict `UM_TEMPO_POR_TURMA` em
`gerar_calendario.py`, mecanismo separado do `UMA_PROVA_POR_TURMA`
(aquele muda o Nº de provas, este muda o Nº de tempos por prova).
Consultado por `montar_exames()` — quando a disciplina está em
`DOIS_TEMPOS` mas a turma tem exceção registrada em `UM_TEMPO_POR_TURMA`,
o valor de `n_tempos` é reduzido de 2 para 1, mantendo as 2 ocorrências
normais do semestre (1 por período), só o número de tempos muda.

**Skill**: adicionada documentação completa em "Passo 0", item 7, como
uma regra geral estrutural (não apenas exceção deste semestre). Texto
documenta o motivo (aulas nessas turmas são só tempos únicos) e a
implementação técnica.

### Parte 2: Repositionamento das duas ocorrências

Após a documentação acima, usuário pediu:
1. "Modifique a segunda prova de GL das turmas 9C coloque no dia 13/11"
   — 2ª ocorrência de GL de semana 8 (25/09) para semana 15 (13/11).
2. "Troque a primeira prova de GL das turmas 9C para o dia 18/09"
   — 1ª ocorrência de GL de semana 4 (28/08) para semana 7 (18/09).

**Aplicado ao calendário**:
- 9C1/9C2 — GL **1ª prova**: semana 4 (28/08) → **semana 7 (18/09, sexta)** —
  última sexta de P1.
- 9C1/9C2 — GL **2ª prova**: semana 8 (25/09) → **semana 15 (13/11, sexta)** —
  fim de P2.

Todas as células foram corrigidas com 1 tempo (5º tempo, sexta).
Distância entre as 2 ocorrências: semana 7 → semana 15 = **8 semanas**
(satisfaz DISTANCIA_MIN_MESMA_DISC=4 e ≥7 desejável).

Nenhuma outra disciplina foi alterada. Os slots de semana 4 e semana 8
(sexta) ficaram vazios; semana 7 e semana 15 (sexta) receberam as provas
de GL.

`verificar_calendario.py` fecha em 0 PROBLEMA, 45 AVISOs (2 AVISOs novos
de GL cedendo em week 6 antes da prova de week 7 — soft relaxations
esperadas, não falhas de regra). Os 5 relatórios regenerados com as
mudanças.

## Próximos passos

1. Confirmar a pendência de tempos (Física/Geo/Química fora do 9º ano).
2. Extrair horário-base das 7 turmas restantes via visão computacional.
3. Copiar a semana-grade (linhas de data) da aba `10C2` para as outras 7
   abas de turma no arquivo de modelo do 2º semestre, se ainda não feito.
4. Gerar as 3 propostas de calendário (3 arquivos xlsx, 8 abas cada).
5. Gerar relatório de trocas de tempo entre professores.
6. Rodar o checklist final da skill antes de entregar.
