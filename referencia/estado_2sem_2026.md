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

## Redação (2ª prova, 9C1/9C2): 19/10 → 22/10, tempos 1-2 → 4-5 (08/2026)

"Coloque a redação das turmas 9C que está no dia 19.10 para 22.10 (4º e
5º tempos)". 2ª ocorrência de Redação movida de semana 12 segunda (19/10,
1º e 2º tempos) para semana 12 quinta (22/10, 4º e 5º tempos). Mesma
semana, dia diferente. `verificar_calendario.py` fechou em 0 PROBLEMA.

## GL, Matemática, Biologia e DSD1 (9C1/9C2) — rodada de 08/2026

### 1. GL: semana 13 sexta (30/10) → semana 15 sexta (13/11)

Mesmo dia da semana e mesmo tempo (5º tempo) — só a semana mudou, sem
risco de violar presença do professor.

### 2. Matemática: semana 14 quarta (04/11) → semana 16 quarta (18/11)

2ª ocorrência de Mat/BrSa. Mesmo dia da semana e mesmos tempos (4º e 5º)
— só a semana mudou. Distância da 1ª ocorrência (semana 6, 08/09):
semana 16 − semana 6 = 10 semanas, cumpre o piso.

### 3. Biologia (9C1/9C2): correção de 1 para 2 tempos + nova prova em P1

Usuário corrigiu a documentação anterior: "a prova de biologia das
turmas 9C são dois tempos de aplicação" — Biologia **não** pertence mais
à exceção de "1 tempo, 1 prova no semestre" que ainda vale para Química
e Física no 9º ano. Passa a seguir o tratamento normal de `DOIS_TEMPOS`:
2 tempos por prova, 2 ocorrências no semestre (1 por período) — mesmo
sem aula dupla nessas turmas (Bio só tem tempos únicos: 9C1 segunda 1º e
quarta 3º; 9C2 terça 1º e 8º), a prova toma emprestado o tempo vizinho,
igual a outras provas sem aula dupla nessas turmas (Redação, GL antes).

**Implementado no código**: `bio` removida de `NOVE_UM_TEMPO` em
`gerar_calendario.py` (que agora só vale para `fis`/`qui` no 9º ano).
Também corrigidas 2 referências hard-coded em `verificar_calendario.py`
que ainda tratavam Bio como exceção de 1 tempo/1 prova nas turmas 9C
(linhas do cálculo de `esperado` e do check "disciplinas de 1 tempo
usam 1 tempo") — sem essa correção o checklist reprovava com falsos
PROBLEMA. Skill atualizada (Passo 0 item 7 e checklist final).

**Proposta aplicada ao calendário** (sem alterar nenhuma outra prova):
- Prova existente (2ª ocorrência): semana 16 terça (17/11) — 1º tempo →
  **1º e 2º tempos**.
- Prova nova (1ª ocorrência, período 1): **semana 7 terça (15/09), 1º e
  2º tempos** — dia escolhido porque é a terça livre mais próxima dentro
  de P1 (semanas 4-7) coincidindo com o tempo próprio do professor Ale
  em 9C2 (terça 1º tempo); em 9C1 a presença do professor fica coberta
  pela coordenação entre turmas irmãs (mesmo professor). Distância entre
  as 2 ocorrências: semana 7 → semana 16 = 9 semanas (cumpre o piso
  desejável de 7).

`verificar_calendario.py` fechou em 0 PROBLEMA após as correções acima.

### 4. DSD1 (Deutsches Sprachdiplom) — avaliação externa, NÃO é regra

"Colocar nos dias 19 de agosto (parte escrita) e 31 de agosto e 01 de
setembro (parte oral) DSD1, não colocar na regra" — usuário confirmou
que se aplica a 9C1 e 9C2. Por pedido explícito, **não** foi adicionado
a `SIMULADOS` em `gerar_calendario.py` nem à skill — é um evento pontual
deste semestre, não uma regra recorrente de geração de calendário.

**Escrito diretamente na planilha** (mesmo padrão visual dos simulados,
preenchimento amarelo, bloco "2º ao 7º tempos"):
- 19/08 (semana 3, quarta): "DSD1 — Parte escrita".
- 31/08 (semana 5, segunda) e 01/09 (semana 5, terça): "DSD1 — Parte
  oral" (2 dias).

**Ajuste mínimo em `verificar_calendario.py`** (só classificação, não
regra de geração): `SIM_COD` passou a reconhecer o prefixo `DSD` para
não contar DSD1 como se fosse uma disciplina normal (evita falso
PROBLEMA de "Nº de provas" e de tempo único). Criado `SIM_COD_OFICIAL`
(sem DSD) para o check separado que compara os simulados encontrados
contra a lista oficial `G.SIMULADOS` — assim DSD1 não precisa constar
nessa lista oficial, respeitando o pedido de não virar regra.

`exportar_tempos_cedidos.py` já ignora graciosamente códigos não
reconhecidos (mensagem informativa, sem erro), então DSD1 não afeta a
contagem de cedências de nenhum professor.

## DSD2 (12C1/12C2) — avaliação externa, NÃO é regra (08/2026)

"Colocar nas turmas 12C: nos dias 18 de agosto (parte escrita) e 3 de
setembro (parte oral) serão realizados os exames DSD2" — aplicado às
duas turmas (12C1 e 12C2), mesmo padrão do DSD1 (9C): escrito
diretamente na planilha, **não** entrou em `SIMULADOS` nem na skill.

**Conflito identificado e resolvido**: em 12C1, 03/09 já tinha a
(única) prova de Inglês/PaH (4º e 5º tempos) — `UMA_PROVA_POR_TURMA`
faz Inglês ter só 1 ocorrência no semestre nessa turma, então não dava
para simplesmente apagar. Usuário confirmou: "nesse dia não terá outra
prova a não ser DSD2". A prova de Inglês foi **remanejada para 24/08
(semana 4, segunda, 1º e 2º tempos)** — dia em que o prof. PaH já tem
aula dupla de Inglês na grade normal de 12C1, sem necessidade de doação
de tempo de outra disciplina. Em 12C2 não havia conflito (a prova única
de Inglês já está em 24/08).

**Escrito diretamente na planilha** (mesmo padrão visual dos simulados):
- 18/08 (semana 3, terça): "DSD2 — Parte escrita".
- 03/09 (semana 5, quinta): "DSD2 — Parte oral" (dia exclusivo, sem
  nenhuma outra prova).

`SIM_COD` em `verificar_calendario.py` já usava o padrão genérico
`DSD\d+` (criado para o DSD1), então reconheceu "DSD2" automaticamente,
sem precisar de nova alteração no código de verificação.

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças.

## Reposicionamento coordenado Mat/Port/Redação — semanas 4 a 7 (08/2026)

Usuário pediu avaliação antes de executar: "avalie a possibilidade
necessária de nas turmas 9C colocar a primeira prova de matemática no
dia 16.09, ou no dia 15.09 trocando biologia, ou um dia melhor na
sétima semana. [...] mude a prova de língua portuguesa que está no
02.09 para outro dia nessa semana ou na semana seguinte e para isso a
redação ocorra uma semana antes ou na mesma semana que a prova de
língua portuguesa."

**Avaliação apresentada e aprovada pelo usuário** ("continue, pode
aplicar"):

1. **Matemática (1ª prova)**: rejeitada a opção de trocar com Biologia
   em 15/09 (nenhuma das duas tem aula dupla nesse dia/tempo, não traria
   vantagem). Escolhido **16/09 (semana 7, quarta), 4º e 5º tempos** —
   dia real de aula dupla do prof. BrSa em 9C1 às quartas, sem cessão de
   tempo de nenhuma disciplina; 9C2 coberta por coordenação entre turmas
   irmãs. Slot antigo (semana 6 terça, 08/09) liberado.

2. **Português (1ª prova)**: avaliados todos os dias da semana 5 antes
   de decidir mudar de semana — segunda/terça tomadas pelo DSD1 (dia
   inteiro), quinta sem aula de Português da profa. Jana em nenhuma das
   duas turmas (violaria presença do professor), sexta já tem prova de
   Inglês. Nenhum dia da própria semana 5 é viável. Movido para
   **semana 6, terça (08/09), 1º e 2º tempos** — slot liberado pela
   saída da Matemática; tempo próprio da profa. Jana em 9C1 às terças
   (9C2 coberta por coordenação entre turmas irmãs).

3. **Redação (1ª prova)**: como o Português saiu da semana 5 para a
   semana 6, a Redação (que estava na semana 4) ficaria 2 semanas antes
   do Português, violando a regra "1 semana antes ou mesma semana".
   Movida de **semana 4 quinta (27/08) para semana 5 quinta (03/09)**,
   mesmo bloco de 4º e 5º tempos já usado — dia real de aula do prof.
   Raf nas duas turmas (tempo6 em 9C1, tempo5 em 9C2). Fica exatamente
   1 semana antes da nova data do Português (semana 6) — cumpre a regra.
   A 2ª ocorrência (semana 12 quinta, 22/10) já cumpria a regra por estar
   na mesma semana que o Português (semana 12 quarta, 21/10) — não foi
   alterada.

**Resultado (semanas 4 a 7)**:
- Semana 4: só Hist (terça, 25/08) — Redação saiu de lá.
- Semana 5: DSD1 (seg+ter), Redação (qui, 03/09), Ing (sex, 04/09) —
  quarta (02/09) ficou livre.
- Semana 6: Português (ter, 08/09), Geo (qua, 09/09).
- Semana 7: Bio (ter, 15/09, já da rodada anterior), Mat (qua, 16/09).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças.

## Geografia (2ª prova, 12C1/12C2): 23/10 → 09/11 (08/2026)

Usuário pediu avaliação: "avaliar a possibilidade de colocar a segunda
prova de geografia das turmas 12C no dia 09.11 ou 13.11 pela manhã".

**Avaliação apresentada e aprovada** ("sim"):

- **13/11 descartado**: esse dia (semana 15, sexta) já tem a marcação
  fixa "2CH 10,12" (2ª chamada da série 10/12) — não é slot livre para
  prova regular. Mesmo se estivesse livre, ficaria a só 4 dias do CC
  10,12 (17/11), violando o mínimo de 6 dias exigido para turmas
  10C/12C.
- **09/11 escolhido**: semana 15, segunda — livre nas duas turmas.
  12C1 tem aula dupla real de Geografia com o prof. Mar às segundas,
  5º e 6º tempos (ainda manhã, já que o 7º tempo é o primeiro da
  tarde) — sem cessão de tempo de nenhuma disciplina; 12C2 coberta por
  coordenação entre turmas irmãs. Distância da 1ª prova (semana 5,
  31/08): 10 semanas. Distância do CC 10,12 (17/11): 8 dias — cumpre
  o mínimo de 6.

**Aplicado**: Geo (2ª prova) de semana 12 sexta (23/10) → semana 15
segunda (09/11), 5º-6º tempos, nas duas turmas.

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

## Inglês (10C1 apenas): 02/09 → 03/09 e 19/10 → 05/11 (08/2026)

Usuário pediu para verificar (só em 10C1, não mexer em 10C2): "colocar a
prova de inglês de 02/09 para 04/09 e a segunda prova que está 19/10
colocar em 05/11".

**04/09 (sexta) testado e rejeitado**: o prof. APa não dá nenhuma aula
de Inglês na sexta-feira em 10C1, em nenhum tempo — verificado com
`G.professor_presente_no_bloco('10C1', 'ing', 'APa', 5, t, n)` para
todos os tempos, todos `False`. Diferente de outras trocas nesta
rodada, aqui não existe cobertura por turma irmã: o Inglês de 10C2 é
com outra professora (Vir), datas e horários totalmente diferentes.
Usuário corrigiu: a intenção era **quinta-feira, 03/09** (não 04/09).

**Aplicado**:
- **1ª prova**: semana 5 quarta (02/09) → semana 5 **quinta (03/09)**,
  2º-3º tempos — aula dupla real do prof. APa em 10C1 às quintas
  (verificado `True`), sem cessão de tempo de nenhuma disciplina.
- **2ª prova**: semana 12 segunda (19/10) → semana 14 **quinta
  (05/11)**, mesmo bloco 2º-3º tempos — mesma aula dupla real.
  Distância entre as 2 ocorrências: semana 14 − semana 5 = 9 semanas,
  acima do piso desejável de 7.

Mudança feita **apenas em 10C1** (10C2 não foi tocada).
`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças.

## História (11C1/11C2): quarta → terça, 01/09 e 03/11 (08/2026)

Usuário pediu para verificar a possibilidade de colocar História (11C)
em "01/09/2026, 2º e 3º tempos" e "03/11/2026, 2º e 3º tempos".

**Verificado com `G.professor_presente_no_bloco()` e aprovado**: terça,
2º e 3º tempos, é a **aula dupla real** do prof. Ver de História em
11C1 (11C2 coberta por coordenação entre turmas irmãs, mesmo
professor). Melhor que a posição anterior (quarta, 1º-2º tempos, que
usava 1 tempo emprestado em cada turma, não era aula dupla real em
nenhuma delas).

**Aplicado**:
- 1ª prova: semana 5 quarta (02/09) → semana 5 **terça (01/09)**,
  2º-3º tempos.
- 2ª prova: semana 12 quarta (21/10) → semana 14 **terça (03/11)**,
  2º-3º tempos.

Distância entre as 2 ocorrências: semana 14 − semana 5 = 9 semanas
(antes era 7, exatamente no piso desejável).

`verificar_calendario.py` fechou em 0 PROBLEMA. Novos AVISOs leves
surgiram em 11C2 (Mat/JJ e Qui/CAl cedendo tempo, já que 11C2 não tem
aula própria de História nesse horário — só 11C1 tem a aula dupla
real) — são cessões esperadas do mecanismo de coordenação entre
turmas irmãs, não falhas de regra. Os 5 relatórios regenerados.

**Por que essa solução não apareceu antes**: os reposicionamentos
anteriores desta rodada (Mat/Port/Redação, Geografia, Inglês) foram
todos motivados por pedidos específicos do usuário sobre datas
exatas — nenhum deles pediu para revisar a posição de História. O
processo de geração original (`montar_exames()`) resolve o
posicionamento buscando viabilidade e distância mínima entre as duas
provas da mesma disciplina, mas **não otimiza qual bloco de tempos usar
dentro do dia escolhido** — ele aceita o primeiro bloco viável
(incluindo bloco com 1 tempo emprestado) sem comparar contra outras
combinações de dia/tempo que eliminariam a cessão por completo. Ou
seja, a "quarta, 1º-2º tempos" passou no checklist (0 PROBLEMA) porque
cumpre todas as regras obrigatórias — só não é o **ótimo** entre todas
as opções viáveis. Encontrar a alternativa sem nenhuma cessão (terça,
aula dupla real) exige comparar explicitamente os dias da semana em
que o professor dá aula dupla de fato, o que só acontece quando
alguém pede essa avaliação pontual — como nesta rodada.

## 9C: permuta Hist/Bio + Inglês reposicionado; 10C: Sociologia bloqueada (08/2026)

Usuário pediu 4 mudanças em uma única rodada; 3 aplicadas, 1 bloqueada
por conflito estrutural (ver abaixo).

### Aplicado: 9C1/9C2 — permuta das 2ªs provas de Hist e Bio

"Permutar as segundas provas de HIST e Bio, ou seja, Biologia vai para
10/11 e história vai para 17/11" — troca direta das datas mantendo os
blocos de tempo de cada disciplina:
- Bio (2ª prova): semana 16 terça (17/11) → semana 15 terça (10/11),
  1º-2º tempos.
- Hist (2ª prova): semana 15 terça (10/11) → semana 16 terça (17/11),
  4º-5º tempos.

### Aplicado: 9C1/9C2 — Inglês de 09/10 para 06/11

Semana 10 sexta (09/10) → semana 14 sexta (06/11), mesmo bloco 2º-3º
tempos (mesmo dia da semana, só a semana mudou).

### Bloqueado: 10C1/10C2 — Sociologia (Soc/Kle)

"Nas turmas 10c1 leve a prova de Soc de 2/10 para 23/10 e na turma
10c2 leve a prova de Soc de 02/10 para uma data possível posterior a
semana 11 considerando que essa prova seja aplicada no tempo do
professor da disciplina."

**Testado e revertido**: `verificar_calendario.py` acusou PROBLEMA —
"Soc tem professor comum mas as provas não coincidem" — Sociologia é
lecionada pelo mesmo prof. Kle em 10C1 (quarta, 5º tempo) e 10C2
(sexta, 5º tempo), e o checklist **exige que provas de professor comum
entre turmas irmãs caiam exatamente no mesmo dia e tempo nas duas
turmas** (regra 11 do verificador) — não é permitido dar datas
diferentes a cada turma quando o professor é o mesmo.

Além disso, ao tentar uma data única na sexta-feira (tempo próprio do
prof. Kle em 10C2, conforme pedido), **todas as sextas-feiras
disponíveis depois da semana 11 esbarraram em outro limite**: o
máximo de 3 avaliações por semana por turma. Levantamento semana a
semana (10C1 / 10C2, contagem antes de somar Soc):
- Semana 12 (23/10): 2 / **3** (10C2 já no teto)
- Semana 13 (30/10): **3** / **3** (as duas já no teto)
- Semana 14 (06/11): **3** / 2 (10C1 já no teto, por causa do Inglês
  de 10C1 que já tinha sido movido para cá numa rodada anterior)
- Semana 15 (13/11): sexta bloqueada nas duas turmas pela marcação fixa
  "2CH 10,12"
- Semana 16 (20/11): sexta é "unterrichtsfrei" (sem aula) nas duas
  turmas
- Semana 17 (27/11): livre em 10C1, mas bloqueada em 10C2 pela
  marcação "2CH 9,11"

Ou seja, **não existe nenhuma sexta-feira depois da semana 11** que
sirva simultaneamente para as duas turmas sem violar o teto semanal ou
cair em dia bloqueado. **Sociologia foi revertida para a posição
original (semana 9, sexta, 02/10)** nas duas turmas, aguardando decisão
do usuário: (a) aceitar um dia que não seja sexta-feira, com 10C2
coberta por coordenação entre turmas irmãs em vez de tempo próprio
(ex.: semana 16 quarta, 18/11, ambas as turmas com 0 avaliações antes
de somar Soc); (b) aceitar estourar o teto de 3/semana em alguma das
turmas como exceção pontual; ou (c) manter a data atual (02/10).

`verificar_calendario.py` fechou em 0 PROBLEMA (com Soc revertida). Os
5 relatórios regenerados com as 3 mudanças aplicadas (Hist/Bio/Ing).

## Sociologia (10C1/10C2): exceção à coordenação entre turmas irmãs (08/2026)

Depois do bloqueio documentado na seção anterior, usuário esclareceu:
"no caso de sociologia o professor excepcionalmente fora da regra
decidiu usar o seu tempo de aula em cada turma para aplicar a sua
prova. Faça a mudança."

**Implementada a exceção**: novo dict `COORDENACAO_EXCECAO` em
`verificar_calendario.py`, consultado pela regra 11 do checklist
(provas de professor comum entre turmas irmãs precisam coincidir em
dia/tempo) — `{("10C1", "10C2", "Soc")}` fica de fora dessa exigência.
Documentado também na skill (Passo 0, seção de professor comum entre
turmas irmãs).

**Aplicado, cada turma no tempo real do prof. Kle nela** (sem cessão de
tempo de nenhuma disciplina em nenhuma das duas):
- 10C1: semana 9 sexta (02/10) → semana 15 **quarta (11/11)**, 5º tempo
  (tempo próprio do Kle em 10C1).
- 10C2: semana 9 sexta (02/10) → semana 14 **sexta (06/11)**, 5º tempo
  (tempo próprio do Kle em 10C2).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

### Pesquisa à parte: Filosofia usa tempo de outro professor?

Usuário perguntou, em todas as turmas, se o professor de Filosofia
(LAn) usa horário de outro professor. Resposta levantada na grade
(`GRADE_TXT`) e nas provas atuais:

Filosofia é lecionada pelo mesmo prof. LAn em todas as 6 turmas
(10C1/10C2/11C1/11C2/12C1/12C2), sempre às quartas-feiras, mas em
**tempos diferentes por turma**: 10C1 tempo1, 10C2 tempo7, 11C1
tempo9, 11C2 tempo11, 12C1 tempo10, 12C2 tempo4. As provas hoje seguem
o padrão normal de coordenação entre pares de turmas irmãs (regra 11,
sem exceção como a de Sociologia): em cada par, a prova cai no tempo
próprio de UMA das turmas, e a outra usa esse mesmo tempo **emprestado
de outra disciplina**, já que não é o tempo real do LAn lá:
- 10C1-10C2: prova no 1º tempo (tempo próprio de 10C1); em 10C2 esse
  horário é normalmente de Geografia/Mlo — é ela quem cede.
- 11C1-11C2: prova no 9º tempo (tempo próprio de 11C1); em 11C2 esse
  horário é normalmente de Física/Cadu — é ela quem cede.
- 12C1-12C2: prova no 10º tempo (tempo próprio de 12C1); em 12C2 esse
  horário é normalmente de Português/Deb — é ela quem cede.

Ou seja: **sim, em metade das turmas (10C2, 11C2, 12C2) a prova de
Filosofia usa o tempo de outra disciplina**, não o tempo real do LAn
lá — diferente do que passou a valer para Sociologia (exceção pontual
pedida pelo usuário). Nenhuma mudança foi feita a partir dessa
pesquisa; é só informativo.

## Filosofia e Sociologia: exceção de coordenação estendida a todas as turmas (08/2026)

Depois da pesquisa sobre Filosofia (seção anterior), usuário pediu:
"verifique se as provas de sociologia [e filosofia] podem ser
executadas na própria aula do professor [de cada disciplina], esse
pedido contraria o pedido sobre turmas irmãs, porém para FILOSOFIA e
SOCIOLOGIA abriremos essa exceção."

**Estendida a exceção `COORDENACAO_EXCECAO`** (já criada para
Sociologia 10C1-10C2) para mais 4 pares: Sociologia 12C1-12C2,
Filosofia 10C1-10C2, Filosofia 11C1-11C2, Filosofia 12C1-12C2.

**Aplicado — sem mudar nenhuma outra prova do calendário.** Em todos
os 4 casos a disciplina já caía no mesmo dia da semana em todas as
turmas (Filosofia sempre quarta; Sociologia 12C sempre quarta) — só o
**tempo** mudou, na mesma célula (mesma semana, mesmo dia), para
refletir o tempo real do professor em cada turma:
- **Filosofia/LAn 10C2**: 1º tempo → **7º tempo** (semana 13, quarta).
- **Filosofia/LAn 11C2**: 9º tempo → **11º tempo** (semana 8, quarta).
- **Filosofia/LAn 12C2**: 10º tempo → **4º tempo** (semana 12, quarta).
- **Sociologia/Kle 12C2**: 2º tempo → **6º tempo** (semana 13, quarta).

(10C1, 11C1, 12C1 já usavam o tempo próprio do professor — não
precisaram de ajuste.)

Efeito colateral positivo: as cessões de tempo que essas 3 provas de
Filosofia exigiam de Geografia/Mlo (10C2), Física/Cadu (11C2) e
Português/Deb (12C2) — por estarem usando o tempo de 10C1/11C1/12C1 em
vez do próprio — deixaram de existir, já que agora cada prova usa
exclusivamente o tempo do próprio professor da disciplina.

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças. Skill atualizada (Passo 0, professor
comum entre turmas irmãs).

## 12C: Química e Biologia divididas entre semanas 12 e 15 (08/2026)

Usuário pediu: "nas turmas 12c analise a possibilidade de colocar
química ou biologia nas semana 15, uma delas entra na semana 15 e
outra entra na semana 12 mesmo que para isso a filosofia passe para a
semana 14 (utilize essa possibilidade)."

Antes da mudança, Química (2ª prova) e Biologia (2ª prova) estavam as
duas na semana 14 (06/11 e 03/11), e Filosofia estava na semana 12
(21/10).

**Aplicado**:
1. **Filosofia**: semana 12 quarta (21/10) → semana 14 **quarta
   (04/11)**, mantendo o tempo próprio de cada turma (10º em 12C1, 4º
   em 12C2 — já não precisa coincidir, é regra fixa desde a rodada
   anterior).
2. **Química (2ª prova)**: semana 14 sexta (06/11) → semana 12
   **quarta (21/10)**, 1º tempo (tempo próprio de 12C2; 12C1 coberta
   por coordenação entre turmas irmãs — Química não tem a exceção de
   Fil/Soc, então as duas turmas precisam coincidir no mesmo tempo).
3. **Biologia (2ª prova)**: semana 14 terça (03/11) → semana 15
   **quinta (12/11)**, 5º-6º tempos.

**2 problemas encontrados e corrigidos antes de fechar**:
- Tentativa inicial colocou Química em tempos diferentes por turma
  (6º em 12C1, 1º em 12C2) — `verificar_calendario.py` acusou "provas
  não coincidem", porque Química não está na exceção
  `COORDENACAO_EXCECAO` (só Filosofia/Sociologia têm essa liberdade).
  Corrigido para 1º tempo nas duas turmas.
- Tentativa inicial colocou Biologia na quarta-feira da semana 15,
  tempos 1º-2º — o 2º tempo doaria a única aula semanal de Sociologia
  em 12C1 (Sociologia não pode doar, é disciplina de 1 aula/semana).
  Corrigido para quinta-feira, tempos 5º-6º (doadores: Português e
  Matemática/JJ, nenhum de aula única).

Distância entre as 2 provas de cada disciplina depois da mudança:
Química 1ª(semana6)→2ª(semana12) = 6 semanas (abaixo do piso desejável
de 7, mas acima do mínimo rígido de 4); Biologia 1ª(semana7)→2ª(semana15)
= 8 semanas (acima do piso desejável).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças.

## 12C: Geografia e DaF reposicionadas + correção de feriado faltante (08/2026)

Usuário pediu para avaliar mover a 2ª prova de Geografia (12C) de
09/11 para a semana 14 ou 13. Na análise, sugeri **semana 14, segunda
(02/11)**, mesmo tempo (5º-6º) já usado hoje — mas o usuário corrigiu:
**02/11 é feriado de Finados**, e a proposta caía justamente nesse dia.

**Bug encontrado e corrigido**: `gerar_calendario.py` já bloqueava
02/11 corretamente via `BLOQUEIOS = {(14, 1), ...}` (usado na geração),
mas `verificar_calendario.py` só cruza contra seu próprio `FERIADOS`
(por data), que tinha só 07/09 e 20/11 — **02/11 estava faltando**. Ou
seja, se a proposta de semana 14 tivesse sido aplicada, o checklist
não teria pego o erro. Corrigido: `FERIADOS` agora inclui
`datetime.date(2026, 11, 2)`.

**Aplicado, seguindo a instrução do usuário** ("mova a prova de
geografia das 12c para 26/10 e a prova de DAF para 23/10"):
- **DaF (2ª prova)**: semana 13 sexta (30/10) → semana 12 **sexta
  (23/10)**, mesmo bloco 6º-7º tempos (aula dupla real do grupo DaF
  nas duas turmas — só a semana mudou, slot ficou livre).
- **Geografia (2ª prova)**: semana 15 segunda (09/11) → semana 13
  **segunda (26/10)**, mesmo bloco 5º-6º tempos (aula dupla real do
  prof. Mar em 12C1 — slot liberado pela saída do DaF daquela semana).

Resultado: semana 12 ganhou DaF (2 → 3 avaliações, no teto); semana 13
trocou DaF por Geo (permanece com 3, no teto); semana 15 perdeu Geo
(3 → 2 avaliações).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças.

## 9C: prova de Química faltando — encontrada e adicionada (08/2026)

Usuário pediu para verificar: "verifique que no calendario das turmas
9C a prova de quimica não consta". Confirmado — busca em todas as 17
semanas das duas turmas não encontrou nenhuma célula de Química.

**Causa raiz**: Química é lecionada nas duas turmas (`qui/Fab`, 1 aula
semanal cada) e segue a mesma regra de Física para o 9º ano
(`NOVE_UM_TEMPO`: 1 tempo, 1 prova no semestre inteiro) — Física está
corretamente no calendário (05/11, 7º tempo), mas Química nunca foi
inserida.

**Bug de checklist encontrado**: `verificar_calendario.py` não acusou
nada (nem PROBLEMA nem AVISO). A regra 5 ("número de provas por
disciplina") só itera sobre disciplinas que **já aparecem** no
calendário — se uma disciplina tem zero provas, ela nunca entra na
contagem, então nunca é comparada com o esperado (1). Mesma categoria
do bug do feriado de Finados (checklist detecta "número errado", não
"disciplina inteira faltando") — **ainda não corrigido**, fica como
pendência.

**Aplicado** (pedido do usuário: "seguindo o padrão de Física (1 tempo,
tempo próprio do prof. Fab) — e tentando ter uma única prova para as
duas turmas"): adicionada Química em **semana 14, quarta-feira (04/11),
2º tempo** — tempo próprio da profa. Fab em 9C2 às quartas (9C1 coberta
por coordenação entre turmas irmãs, já que o tempo real dela em 9C1 é
sexta 7º tempo). Mesma semana que Física, dentro da faixa esperada
(semanas 12 a 14) documentada na skill para Química/Física do 9º ano.
Célula estava vazia antes — nenhuma outra prova foi alterada, movida
ou removida (confirmado célula a célula).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

### Resolvido: Química (12C) corrigida para 2 tempos, movida para 09/11

Usuário identificou que a 2ª prova de Química das turmas 12C (semana
12, quarta, 21/10) estava com **apenas 1 tempo** — bug introduzido na
rodada anterior (quando a Química foi movida para a semana 12, usei
`n_tempos=1` por engano; deveria seguir o padrão normal de
`DOIS_TEMPOS`, igual à 1ª prova de Química, que já está correta com 2
tempos em 11/09).

**Avaliação apresentada** (pedido pelo usuário, sem executar):
testadas todas as combinações de 2 tempos possíveis na quarta-feira
(posição atual) — 1º-2º tempos doaria a única aula semanal de
Sociologia em 12C1 (não pode doar); 5º-6º tempos cruza o intervalo do
recreio; 6º-7º tempos é bloco inválido (7º tempo não existe na grade
de quarta-feira). Nenhuma opção cabe na quarta-feira. Proposta inicial:
segunda-feira da própria semana 12 (19/10), 6º-7º tempos — tempo
próprio da profa. Fab em 12C1 (12C2 coberta por coordenação entre
turmas irmãs).

**Aplicado, com a data ajustada pelo usuário** ("coloque a prova de
quimica das turmas 12c no dia 09/11 no 6 e 7 tempos"): 2ª prova de
Química movida de semana 12 quarta (21/10, 1 tempo, com bug) para
**semana 15 segunda (09/11), 6º-7º tempos** — mesmo bloco da proposta,
só a semana mudou (09/11 já estava livre nas duas turmas, pois a
Geografia tinha saído de lá para a semana 13 numa rodada anterior).

`verificar_calendario.py` fechou em 0 PROBLEMA. Novos AVISOs leves
(Geo/Mar e Ing/Isb cedendo 1 aula a mais que a meta, por causa do
bloco 6º-7º) — soft, esperados, não são falhas do checklist. Os 5
relatórios regenerados.

## 10C2: Inglês (2ª prova) movida de 20/10 para 11/11 (08/2026)

Usuário pediu para avaliar mover a 2ª prova de Inglês de 10C2 (20/10)
para novembro. Avaliação: bloco atual (terça, 4º-5º tempos) usa o 5º
tempo próprio da profa. Vir + o 4º emprestado de Artes; a aula dupla
real dela nessa turma é **quarta-feira, 4º-5º tempos** (sem cessão).
Novembro só tem uma quarta-feira livre dentro do limite de 6 dias
antes do CC final (17/11): **11/11 (semana 15)** — as quartas de
18/11 e 25/11 já ficam depois do limite.

**Aplicado, conforme aprovado pelo usuário**: 2ª prova de Inglês
(10C2) movida de semana 12 terça (20/10) para semana 15 **quarta
(11/11)**, 4º-5º tempos — zero cessão de tempo (bloco 100% próprio da
Vir). Distância da 1ª prova (semana 5): 10 semanas.

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

## 10C1/10C2: cadeia de 5 reposicionamentos (08/2026)

Usuário pediu uma cadeia de trocas encadeadas, cada uma liberando o
slot da próxima, com dois passos exclusivos por turma. Todas mantêm o
mesmo dia da semana e bloco de tempos — só a semana muda:

1. **LP/LIT/RED** (10C1+10C2): semana 13 segunda (26/10) → semana 12
   segunda (19/10), 1º ao 3º tempos.
2. **Química** (10C1+10C2): semana 15 segunda (09/11) → semana 13
   segunda (26/10), 4º-5º tempos — ocupa o slot liberado pela
   Língua Portuguesa.
3. **GL** (10C1+10C2): semana 12 quarta (21/10) → semana 10 quarta
   (07/10), 2º-3º tempos.
4. **Sociologia (10C1 apenas)**: semana 15 quarta (11/11) → semana 12
   quarta (21/10), 5º tempo — ocupa o slot liberado pelo GL.
5. **Sociologia (10C2 apenas)**: semana 14 sexta (06/11) → semana 12
   sexta (23/10), 5º tempo.

Os passos 4 e 5 usam a exceção `COORDENACAO_EXCECAO` (Sociologia não
precisa coincidir entre 10C1/10C2), por isso puderam ir para dias
diferentes (quarta em 10C1, sexta em 10C2) sem violar regra.

Verificação de teto semanal antes de aplicar (nenhuma semana passou de
3 avaliações): semana 10 (2→3), semana 12 (2→3 nas duas, trocando GL
por LP+Soc), semana 13 (3→3, trocando LP por Química), semana 14
(3→2 em 10C2), semana 15 (3→1 em 10C1, 3→2 em 10C2).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com as mudanças. Nenhuma outra prova foi tocada, conforme
pedido pelo usuário.

## 12C1/12C2: Biologia (2ª prova) movida de 12/11 para 22/10 (08/2026)

Usuário pediu: "mude a prova de biologia de 12/11 dsa turmas 12c para
22/10". 2ª prova de Biologia movida de semana 15 quinta (12/11) para
semana 12 **quinta (22/10)**, mesmo bloco 5º-6º tempos — mesmo dia da
semana, só a semana mudou (slot já estava livre, sem cessão adicional).

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

## 10C1/10C2: Química (1ª prova) — mudança de dia, mesma semana (08/2026)

Pedido repassado do professor de Química: "é possível mudar o dia, não
a semana, da prova 1 das turmas 10C1 e 10C2, do dia 24/08, segunda-
feira, para o dia 28/08, sexta-feira, desta mesma semana?"

**Verificado e confirmado possível**: testados todos os blocos de 2
tempos na sexta-feira (posição real da profa. CAl nas duas turmas —
10C1 tem Química só na terça e sexta; 10C2 só na segunda e sexta).
Blocos 1º-2º e 2º-3º não têm presença da professora em nenhuma das
turmas; 4º-5º e 5º-6º ficam inválidos em 10C2 porque o 5º tempo é
Sociologia, que só tem 1 aula semanal e não pode doar. **Único bloco
válido para as duas turmas: 3º-4º tempos** — tempo próprio da profa.
CAl em 10C2 (4º tempo); 10C1 coberta por coordenação entre turmas
irmãs.

**Aplicado**: 1ª prova de Química movida de semana 4 segunda (24/08)
para semana 4 **sexta (28/08)**, tempos 3º-4º — mesma semana, só o dia
mudou. Sexta-feira estava livre; a semana continua com 3 avaliações
(Qui, Bio, GL), sem estourar o teto.

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

## 9C2: Matemática (2ª prova) movida para reduzir cessão de Português (08/2026)

Usuário perguntou por que Português/Jana aparecia cedendo 12,5%
(4 de 32 aulas) no relatório de tempos cedidos, mesmo estando acima do
teto de 11%. Investigação: em **9C1**, vem de Geografia (2 cessões) +
Biologia (2 cessões); em **9C2**, vem inteiramente de Matemática
(2 ocorrências × 2 tempos, quarta-feira 4º-5º tempos).

**Pedido para achar alternativa sem mexer em Geografia.** Busca
exaustiva de todos os blocos de 2 tempos válidos (presença de
professor, disciplinas de aula única que não podem doar, sem cruzar o
recreio):
- **Biologia (9C1)**: só existe **1 combinação válida no calendário
  inteiro** — a atual (terça, 1º-2º tempos, doador Português). Todas as
  outras esbarram em Física ou Química (aula única no 9º ano, não
  podem doar). **Estruturalmente inevitável, não dá pra evitar.**
- **Matemática (9C2)**: encontradas 3 alternativas sem Português.
  Primeira proposta (terça, 4º-5º tempos) foi **rejeitada pelo
  usuário**: colidiria com a prova de Biologia na semana 7 e,
  coincidentemente, com a própria prova de História na semana 16 (mesmo
  bloco de tempos). Segunda proposta, aceita: **quinta-feira, 4º-5º
  tempos** (doadores: Artes nas duas turmas + Redação em 9C2 — nenhum
  dos dois com prova nas semanas 7 ou 16).

**Aplicado, só na semana 16** (usuário pediu para deixar a semana 7
como está): 2ª prova de Matemática (9C1/9C2) movida de quarta (18/11)
para **quinta (19/11)**, mesmo bloco 4º-5º tempos. Semana 7 permanece
inalterada.

**Resultado**: Português/Jana em 9C2 caiu de 4 para **2 cessões
(6,25%)**, dentro da meta. Em 9C1 permanece em 4 (12,5%), pela
combinação Geografia+Biologia, fora do escopo desta mudança. Novo
AVISO leve: Artes cedeu 3 (meta 2) nas duas turmas — tradeoff aceito.

`verificar_calendario.py` fechou em 0 PROBLEMA. Os 5 relatórios
regenerados com a mudança.

## 12C1/12C2: LP/LIT/RED movida de 09/10 para 06/10 (08/2026)

Usuário pediu para avaliar mover LP/LIT/RED de 09/10 para 07/10.
**07/10 (quarta) rejeitado**: bloco de 3 tempos (1º ao 3º) inválido em
12C1 — o 2º tempo é Sociologia, que só tem 1 aula semanal e não pode
doar. Busca exaustiva de todos os blocos de 3 tempos válidos na
semana 10 (vazia, sem risco de teto semanal) encontrou:
- Quinta 1º-3º (doadores Artes+Física, manhã) — recomendada
  inicialmente.
- **Terça 9º-11º** (doadores Apoio+História) — válida, mas no período
  da tarde.

Usuário perguntou sobre a opção de terça 9º-11º e, depois de
confirmada a viabilidade, escolheu essa.

**Aplicado**: LP/LIT/RED (12C1/12C2) movida de semana 10 sexta (09/10)
para semana 10 **terça (06/10)**, tempos 9º-11º.

`verificar_calendario.py` fechou em 0 PROBLEMA (com o AVISO esperado
de "tempos 7-11", já que a prova ficou no período da tarde por escolha
do usuário). Os 5 relatórios regenerados com a mudança.

## Próximos passos

1. Confirmar a pendência de tempos (Física/Geo/Química fora do 9º ano).
2. Extrair horário-base das 7 turmas restantes via visão computacional.
3. Copiar a semana-grade (linhas de data) da aba `10C2` para as outras 7
   abas de turma no arquivo de modelo do 2º semestre, se ainda não feito.
4. Gerar as 3 propostas de calendário (3 arquivos xlsx, 8 abas cada).
5. Gerar relatório de trocas de tempo entre professores.
6. Rodar o checklist final da skill antes de entregar.
