---
name: "calendario-provas"
description: "Monta calendário de provas para turmas da escola: distribuição entre disciplinas, limite semanal de avaliações, períodos por turma/grupo (turmas que viajam terminam mais cedo), feriados e semanas vetadas, preferência por provas nos primeiros tempos do dia, datas de simulados por série, provas combinadas no mesmo dia (Português+Redação+Gramática em 3 tempos), disciplinas com só 1 prova no semestre conforme a série, grupos paralelos com prova simultânea, provas coordenadas entre turmas irmãs quando o professor é o mesmo, e uso de tempos de outros professores quando a prova precisa de tempos seguidos. Com limites de cessão de aula: teto de cessões por disciplina no semestre, percentual máximo da carga, proibição de ceder às vésperas da própria prova e de ficar duas semanas sem contato com a turma. Lê o horário-base (planilha, PDF ou imagem) e gera o calendário de provas, o relatório de trocas de tempo entre professores, a tabela-resumo por turma (disciplina, professor, dia e tempos, nº de tempos) e o relatório de tempos cedidos por disciplina/professor (aulas semanais, aulas programadas no semestre, aulas cedidas e percentual). Usar sempre que o usuário pedir para montar, gerar, revisar, ajustar ou exportar um calendário/plano de provas com proteção de carga horária dos professores."
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

O resultado final é o **calendário de provas**, um **relatório de trocas de
tempo entre professores**, uma **tabela-resumo por turma** e um **relatório
de tempos cedidos**.

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
   célula) olhando o arquivo-modelo mais recente.
10. **Confirmar a leitura do horário-base** em caso de ambiguidade. Cuidado
    com siglas parecidas entre escolas: aqui "esp"/"Spo" = Esportes/Educação
    Física, NÃO Espanhol.
11. **Perguntar como tratar grupos paralelos** (turma se divide, cada
    professor com seu grupo no mesmo tempo — ex.: Alemão/DaF). Regra
    confirmada nesta escola: **1 prova só, aplicada simultaneamente**, cada
    professor com o seu grupo; conta como 1 avaliação da turma.
12. **Perguntar se há sala padrão de provas.** Nesta escola **não há** —
    o campo de sala fica em branco.
13. **Checar se há professor comum entre turmas irmãs** (ex.: 10C1 e 10C2
    da mesma série) para cada disciplina, comparando as siglas do professor
    no horário-base — não perguntar ao usuário, isso se verifica direto nos
    dados. Ver regra de aplicação simultânea abaixo.
14. **Se for gerar o relatório de tempos cedidos** (item 4 dos entregáveis):
    perguntar, por grupo de turma, a data da última prova de 2ª chamada do
    semestre — é o que define até quando contar aulas programadas. E
    confirmar se a semana vetada para provas tem alguma aula normal ou é
    zero aula (padrão: zero).

## Regras de distribuição das provas

- **Disciplina com professor comum entre turmas irmãs**: antes de alocar,
  confira nas siglas **e nas posições (dia/tempo)** do horário-base se a
  mesma pessoa leciona aquela disciplina nas duas turmas, e distinga dois
  casos:
  - **Já é aula combinada** (mesmo professor(es) **no mesmo dia e tempo**
    nas duas turmas, hoje, na grade normal — ex.: Alemão/DaF, GL, e o
    Inglês de algumas séries, onde a turma toda se junta e se divide em
    grupos por professor): isso **já é o caso de "grupos paralelos"**, só
    que abrangendo as duas turmas em vez de uma só. Não precisa de nenhuma
    coordenação nova — a prova sai no mesmo slot naturalmente, porque as
    duas turmas só têm essa disciplina nesse único horário. Trate como
    grupos paralelos: 1 prova só, cada professor aplica pro seu grupo,
    conta como 1 avaliação em cada turma.
  - **Mesmo professor, mas em tempos DIFERENTES em cada turma** (ex.:
    Biologia, Física, Geografia, História, Matemática, Português, Redação,
    Química, Sociologia, Filosofia — o professor dá aula de fato em dois
    horários separados, um por turma): é o caso real que precisa de
    coordenação — o professor não pode estar em dois lugares ao mesmo
    tempo, então **priorize aplicar a prova simultaneamente nas duas
    turmas** (mesmo dia, mesmo(s) tempo(s)), escolhido a partir de um
    tempo **próprio da disciplina em pelo menos uma das duas turmas**
    (nunca um horário que não seja tempo próprio em nenhuma das duas). Na
    turma onde esse horário **não** é tempo próprio da disciplina, o(s)
    tempo(s) são cedidos pela disciplina que normalmente ocupa aquele
    horário nela — é uma troca de tempo entre turmas, e entra no
    relatório de trocas do mesmo jeito que uma troca entre disciplinas.
  - **Se forem professores diferentes**: as provas das duas turmas são
    **independentes**. Isso não é uma obrigação de ocorrerem em dias
    diferentes — apenas não há necessidade de coincidirem. Cada uma
    aloca normalmente pelo tempo próprio daquela turma (a prioridade de
    "tempo de aplicação preferencialmente no tempo da própria disciplina",
    já definida abaixo, vale igual aqui).

- **Nunca cruzar o intervalo do recreio**: uma prova de tempos seguidos não
  pode usar o par 3º+4º tempos nem o par 5º+6º tempos, pois isso obrigaria a
  aplicação a avançar para o horário do recreio. É a restrição de **maior
  prioridade** de todas — esgote qualquer outra combinação (inclusive
  aceitar tempos 7 a 11 ou sobreposição do grupo 1) antes de aceitar cruzar
  o intervalo. Se, mesmo assim, não houver nenhuma alternativa: use o par
  que cruza o intervalo, mas (a) destaque a célula da prova na planilha de
  saída com uma cor de preenchimento diferente das demais, e (b) registre o
  caso explicitamente no relatório de trocas de tempo (turma, disciplina,
  par de tempos, motivo).
- **Máximo de 3 avaliações por semana** por turma. Simulados/AG contam para
  esse limite; um simulado de 2 dias conta como **1** avaliação.
- **Uma prova por dia** por turma (a célula do modelo comporta uma só).
- **Grupo 1** — Matemática, Alemão (DaF), Português (ou a prova combinada
  LP/LIT/RED) e Inglês: não devem ter prova na mesma semana entre si. Só
  permitir sobreposição se não houver nenhuma outra forma de fechar o
  calendário — e avisar o usuário quando isso acontecer.
  **GL não pertence ao grupo 1** (é disciplina própria, com prova).
  - **Exceção confirmada nesta escola**: quando não houver saída, é
    aceitável **duas** provas do grupo 1 na mesma semana **desde que uma
    delas seja Inglês**. Isso acontece naturalmente quando as demais
    disciplinas do grupo 1 têm professor comum entre as turmas irmãs (e
    portanto semanas fixadas pela aplicação simultânea) enquanto Inglês
    tem professores diferentes e é alocado por turma. Continua valendo:
    nunca três do grupo 1 na mesma semana, e o par sem Inglês
    (ex.: Mat + LP/LIT/RED) segue proibido.
- **LP/LIT/RED (turmas 10, 11 e 12)**: a prova combinada de Português,
  Redação e Gramática deve cair na **1ª ou 2ª semana de cada rodada de
  provas** (P1 e P2), nunca nas semanas seguintes do período. Vale nas
  duas rodadas do semestre.
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
- **Distância mínima de 4 semanas entre as 2 provas da mesma disciplina/
  professor** no semestre (quando a turma tem 1 prova por período — a
  maioria das disciplinas). Não se aplica às disciplinas de prova única
  (Fil/Soc e as exceções de série), que só têm 1 ocorrência. Checar pela
  **diferença entre os números das semanas** (não pela data corrida) —
  ex.: prova de P1 na semana 6 e prova de P2 na semana 9 tem distância 3,
  viola a regra; semana 6 e semana 10 tem distância 4, ok. Vale tanto
  para as provas resolvidas por turma quanto para as coordenadas entre
  turmas irmãs (mesmo professor, tempos diferentes) — nesse segundo caso
  a distância é conferida **por turma**, comparando as duas ocorrências
  daquela disciplina especificamente naquela turma.
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
  - **Quando a mesma disciplina/professor tiver mais de uma prova de
    tempos duplos no semestre** (ex.: 1 por período) e o tempo próprio dela
    na grade daquela turma for sempre o mesmo tempo fixo, **prefira
    alternar de qual lado vem o tempo emprestado** entre as ocorrências, em
    vez de tomar sempre do mesmo colega — assim nenhum colega perde mais de
    1 aula no semestre por causa da mesma disciplina. É critério de
    desempate: só se aplica entre opções já equivalentes nas outras regras
    (intervalo, tarde, grupo 1, doador válido); nunca piorar essas regras
    só para alternar.
    - Exemplo: Biologia nas turmas 10C1/10C2, professora com aula fixa no
      6º tempo numa turma e no 7º na outra — 1ª prova do semestre usa 5º+6º
      (empresta do 5º), 2ª prova usa 6º+7º (empresta do 7º, ou é tempo
      próprio), em vez de usar o mesmo par nas duas provas.
- **Não preencher**: células de dia sem aula; células já preenchidas com
  qualquer outra informação.

## Limites de cessão de aula

Conjunto de tetos pedido pela coordenação para proteger a carga horária de
quem cede tempo. Sempre aplicados no calendário de provas.

Todos os tetos são por **(disciplina, professor) dentro de uma turma** — é
a mesma chave do relatório de tempos cedidos, então os dois batem
diretamente.

1. **2 ou 3 aulas semanais → no máximo 2 cessões no semestre.**
   *Exceção confirmada nesta escola*: **História, Geografia e GL** podem
   ceder **3**. Perguntar sempre se há disciplinas com exceção — não
   presumir a lista.
2. **1 aula semanal → não cede nada.** (Já valia antes como regra geral;
   aqui vira caso particular do mesmo princípio.)
3. **Nunca ficar duas semanas seguidas sem contato com a turma.** Uma
   semana "sem contato" é aquela em que todas as aulas da disciplina
   naquela semana foram cedidas — e a semana vetada (conselho de classe)
   conta como sem contato para todo mundo, então ceder tudo na semana
   imediatamente anterior ou posterior a ela também viola a regra.
   Avaliar só o que a cessão **causa**: se a disciplina já ficaria sem
   contato por outro motivo (feriado no único dia dela), isso não é
   provocado pela cessão e não conta.
4. **Não ceder às vésperas da própria prova.** Se a disciplina tem prova
   marcada para aquela semana ou para a semana **anterior**, ela não cede
   aula — é justamente a aula de revisão. Vale nos dois sentidos, e o
   algoritmo precisa checar os dois: ao alocar uma cessão (a prova da
   doadora já está marcada para a mesma semana ou para a semana seguinte
   à da cessão?) e ao alocar uma prova (a disciplina já cedeu aula na
   semana da prova ou na anterior?).
   - **Ao afrouxar esta regra** (ver escada de afrouxamento abaixo), **o
     lado ANTES da prova nunca é liberado** — só o lado DEPOIS. Ou seja,
     mesmo numa turma com a regra 4 relaxada, nenhuma disciplina pode
     ceder aula na semana anterior à própria prova, nem em nenhum dia até
     e incluindo o dia da própria prova. O que a relaxação abre é ceder a
     partir do **primeiro dia útil depois da prova** daquela disciplina —
     nunca antes. Exemplo: prova de Português numa terça-feira — relaxada
     a regra, Português pode ceder aula a partir de **quarta-feira** em
     diante; nunca na segunda, na terça, nem em qualquer dia da semana
     anterior. A proteção que importa de verdade é a aula de revisão
     **antes** da prova; depois da prova aplicada, não há mais nada
     naquela ocorrência para proteger.
5. **Teto percentual das aulas do semestre.** O alvo é 10%, e o teto duro
   é **11%** — nenhuma disciplina cede mais que isso das aulas programadas
   dela no semestre (ver o cálculo de "aulas programadas" no relatório de
   tempos cedidos). A folga entre o alvo e o teto é o que viabiliza as 3
   cessões das disciplinas de 2 aulas semanais da exceção acima
   (3 de 28 aulas = 10,7%). Quando o percentual e a regra 1 discordam,
   vale **a mais restritiva**.

Implementação: o teto efetivo de cada disciplina é
`min(regra 1, floor(11% das aulas programadas))`, e 0 para quem tem 1 aula
semanal. As regras 3 e 4 são checadas a cada cessão candidata, durante a
busca — não dá para aplicá-las depois, porque mudam quais slots são
viáveis.

**Datas exigidas pela coordenação são inegociáveis e vêm antes da regra
4.** Se uma prova tem data fixa, nenhuma cessão pode ocorrer na semana
dela nem na anterior — senão a regra 4 tornaria a data impossível. Essa
proteção precisa entrar **na fase que decide as provas coordenadas entre
turmas irmãs**, que roda antes das provas individuais: sem ela, as provas
coordenadas consomem justamente os tempos que a prova de data fixa
precisaria, e o calendário fica insolúvel sem sintoma óbvio.

**Se os limites estritos não fecharem o calendário**, afrouxar nesta
ordem, sempre **avisando o usuário** do que foi relaxado:
1. relaxar a **regra 4** (não ceder às vésperas da própria prova) —
   **só o lado depois da prova**, nunca o lado antes (ver o detalhe da
   regra 4 acima: o afrouxamento nunca reabre a semana anterior nem o
   próprio dia da prova, só os dias posteriores à aplicação);
2. relaxar a **regra 3** (duas semanas sem contato);
3. só por último, subir os tetos de cessão (regra 1/5) de uma unidade
   por vez.

Os tetos (regras 1, 2 e 5) são limites duros que a escola deu em
**número** — relaxá-los primeiro é a troca errada: uma folga vale para
as 8 turmas de uma vez e pode estourar dezenas de tetos só para salvar
a regra 4 em uma única turma. Relaxar a regra 4 (ou a 3) primeiro, e
**por turma** — só nas turmas que não fecham, nunca nas 8 de uma vez —
custa muito menos: normalmente resolve 1 ou 2 turmas sem tocar nas
outras 6 ou 7, que continuam cumprindo tudo. As datas exigidas pela
coordenação **nunca** são relaxadas, em nenhuma etapa. Nunca entregar
em silêncio uma proposta que violou os limites: o script de verificação
deve separar **falhas** (regras que valiam) de **avisos** (regras que
foram explicitamente relaxadas, e em quais turmas).

**No solver de provas coordenadas entre turmas irmãs, evite tomar tempo
de disciplinas cuja prova ainda será alocada depois** (ex.: o Inglês das
turmas 10/11/12, que tem professores diferentes entre as turmas irmãs e
por isso é resolvido individualmente, depois das coordenadas). Sem essa
precaução, a prova coordenada consome justamente os tempos de que a
disciplina pendente vai precisar, e a regra 4 trava essa disciplina sem
nenhuma semana livre mais adiante — sintoma nada óbvio de rastrear. É
critério de desempate entre opções já equivalentes nas regras
anteriores (nunca piora intervalo, tarde ou grupo 1 só para evitar
esse doador).

**A semente da busca importa**: com restrições tão apertadas, qual semente
embaralha a ordem das opções decide se existe ou não solução dentro do
orçamento de nós. Antes de concluir que uma regra é inviável e relaxá-la,
**teste algumas sementes** — nesta rodada, uma turma que parecia exigir
exceção fechou perfeitamente com outra semente. Fixe no código a semente
escolhida, com um comentário dizendo por quê.

**Custo computacional**: estas regras encarecem muito cada nó da busca
(medido: ~600 nós/s contra dezenas de milhares sem elas). Duas
providências são necessárias para o gerador terminar em tempo útil:
pré-computar uma única vez os blocos (dia, tempo) válidos de cada prova —
eles não dependem da semana nem do estado da busca — e usar um orçamento
de nós menor, já que uma solução viável aparece em poucos milhares de nós
e um teto alto só faz os degraus inviáveis custarem minutos.

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
- **Células em branco na grade podem indicar horário de almoço** daquela
  turma (o almoço ocorre entre 11h35 e 14h15, variando por turma). Tratar
  como qualquer outra célula sem aula: nunca usar para prova, e nunca
  considerar um par de tempos "duplo" válido se houver uma célula em branco
  entre eles — isso já quebra o requisito de tempos consecutivos, sem
  necessidade de regra à parte para almoço.
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
- **Datas de 2ª chamada (segunda chamada / Nachschreibtermine)**: sempre
  que o usuário informar (ou corrigir) uma data de 2ª chamada, **marque-a
  no arquivo-modelo**, não só em documentação. Esta escola já tem a
  convenção pronta no modelo: texto `"2CH <séries>"` (ex.: "2CH
  9,10,11,12") com **preenchimento vermelho** (a mesma cor do exemplo na
  legenda "Nachschreibtermine | Segunda Chamada" do modelo), na coluna do
  dia certo — inclusive **sábado**, que tem coluna própria na grade (a
  2ª chamada cai no dia seguinte ao fim de um período, frequentemente um
  sábado, fora da janela de segunda a sexta usada para alocar provas
  normais). Ao mudar uma data de 2ª chamada já marcada, **apague a marca
  antiga** (volte a célula ao estilo vazio de uma célula vizinha do mesmo
  tipo) antes de marcar a nova — senão fica uma marca obsoleta que confunde
  o usuário, do mesmo jeito que aconteceria com uma data de simulado
  movida sem limpar a célula antiga.

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

**Mesclar a célula da prova**: cada dia de semana no modelo ocupa 3 linhas
físicas (a legenda do cabeçalho mostra o porquê: `Fach | Lehrkraft`,
`Raumwunsch`, `U-Stunden` — matéria/professor, sala, horário). Escrever só
na célula-âncora sem mesclar deixa 1 das 3 linhas preenchida e as outras
2 em branco, um efeito visual ruim (o usuário via isso como "só a
primeira de três células preenchida"). Sempre que escrever uma prova ou
simulado, **mescle o bloco de 3 linhas daquele dia** (célula-âncora +
as 2 abaixo) antes ou depois de escrever o texto, e limpe a borda interna
(deixe só a borda externa do bloco visível) — é o mesmo efeito da solução
manual de selecionar as 3 células e mesclar, automatizado. Antes de
mesclar, **confira se aquele bloco já não está mesclado** (algumas
semanas already vêm com bloco mesclado do próprio modelo, ex.: semanas de
feriado/"unterrichtsfrei") para não tentar mesclar em cima de um merge
existente.

**Cor de preenchimento por disciplina**: cada disciplina tem uma cor fixa,
igual em todas as séries/turmas — a mesma disciplina nunca muda de cor
entre 9C, 10C, 11C e 12C. Objetivo: dar para o olhar rápido reconhecer a
disciplina pela cor, sem prejudicar a leitura do texto (por isso paleta
**pastel**, sempre com texto preto por cima — nunca uma cor tão escura
que dificulte a leitura). Regras de prioridade sobre a cor:

1. **Amarelo é EXCLUSIVO dos simulados/AG** (`FFFF00`) — os códigos de
   data fixa (`S1-<turma>` a `S4-<turma>`, `AG9`, `AG10` etc., ver
   SIMULADOS). **Nenhuma outra célula pode usar amarelo**: não é a cor de
   nenhuma disciplina normal, nem serve de destaque para outra coisa —
   reservar essa cor inteira aos simulados é o que deixa eles
   reconhecíveis à primeira vista na planilha. Em qualquer série — não
   depende de cor herdada do modelo por coincidência de posição: **fixe o
   preenchimento explicitamente** toda vez que escrever um simulado.
   (Um bug já aconteceu aqui: o modelo trazia uma célula de exemplo do
   AG10 já amarela numa posição fixa; quando a data mudou de semana, a
   célula nova ficou branca porque o código nunca tinha definido a cor de
   verdade, só herdava por acaso — só apareceu quando o usuário reparou
   que a maioria dos simulados não estava amarela.)
2. **Cruzar o intervalo do recreio** (ver regra acima) é um aviso raro e
   deliberado — quando acontece, o destaque laranja (`FFC000`) tem
   **prioridade sobre a cor da disciplina** naquela célula específica.
3. Fora esses dois casos, use a cor fixa da disciplina.

**Pegadinha do openpyxl com `PatternFill`**: o parâmetro `start_color`/
`end_color` exige uma string ARGB de **8 dígitos hex** (alfa + RGB). Um
código de 6 dígitos (só RGB, ex. `"DDE7C6"`) é aceito sem erro, mas o
Excel entende que o alfa é `00` (totalmente transparente) — a célula fica
gravada como `patternType="solid"` só que **invisível**, sem nenhum aviso
no processo de escrita. Já aconteceu nesta rodada: a implementação
inteira da cor por disciplina (e o destaque de intervalo) foi escrita com
6 dígitos, passou no script de verificação (que só olha o texto, não a
cor) e só o usuário reparou, abrindo o arquivo, que nada estava colorido.
**Sempre prefixar `"FF"`** (ex. `"FFDDE7C6"`) em qualquer cor de
preenchimento — e, se possível, o script de verificação deveria checar
que `cell.fill.fgColor.rgb` começa com `FF` (opaco) em toda célula que
deveria ter cor, não só que o texto está certo.

Paleta usada nesta escola (matiz igualmente espaçado entre 78° e 330°,
saturação 40%, luminosidade 84% — sempre longe da faixa do amarelo,
reservada aos simulados, e da faixa vermelho/laranja, reservada à 2ª
chamada e ao destaque de intervalo):

| Disciplina | Cor |
|---|---|
| Mat | `#DDE7C6` |
| DaF | `#D2E7C6` |
| GL | `#C8E7C6` |
| Ing | `#C6E7CF` |
| Hist | `#C6E7D9` |
| Geo | `#C6E7E4` |
| Bio | `#C6DFE7` |
| Fis | `#C6D4E7` |
| Qui | `#C6CAE7` |
| Fil | `#CDC6E7` |
| Soc | `#D7C6E7` |
| LP/LIT/RED | `#E2C6E7` |
| Port (turma 9, prova separada) | `#E7C6E1` |
| Redação (turma 9, prova separada) | `#E7C6D6` |

Disciplina fora dessa lista: cor cinza-claro neutra (`#E7E6E6`) como
fallback, e sinalizar ao usuário para decidir uma cor definitiva.
Ao montar a paleta para uma escola nova, gere as cores algoritmicamente
(matiz igualmente espaçado, mesma saturação/luminosidade) em vez de
escolher uma a uma — garante que fiquem sempre distintas entre si.

## Entregáveis finais

1. **O calendário de provas**, em arquivo xlsx com uma aba por turma.
2. **Relatório de trocas de tempo entre professores**, em tabela, uma linha
   por troca:

   | Turma | Disciplina/Prof. solicitante | Tempo necessário | Prof. doador | Disciplina do tempo doado | Ação | Observação |
   |---|---|---|---|---|---|---|

   A coluna **Observação** registra casos especiais, como uma prova que
   precisou cruzar o intervalo do recreio por falta de alternativa (ver
   regra em "Regras de distribuição das provas").

   Claro o suficiente para ser usado direto na comunicação com os
   professores.
3. **Tabela-resumo por turma** (uma aba por turma, em arquivo separado),
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
4. **Relatório de tempos cedidos** (uma aba por turma, em arquivo separado),
   para a coordenação enxergar de uma vez quanto cada disciplina/professor
   perdeu de aula própria ao longo do semestre por causa de provas de outras
   disciplinas, em número absoluto e em percentual da carga do semestre.
   Colunas:

   | Disciplina | Professor | Nº de aulas semanais | Nº de aulas programadas no semestre | Nº de aulas cedidas para provas de outras disciplinas | % de aulas cedidas no semestre |
   |---|---|---|---|---|---|

   - Uma linha por combinação (disciplina, professor) que aparece na grade
     da turma — inclusive disciplinas sem prova (Educação Física, Artes,
     eletivas etc.), porque o tempo delas também pode ser tomado como
     doador. Se a mesma disciplina tiver professores diferentes em tempos
     diferentes (ex.: duas turmas de Matemática na mesma turma-C), são
     linhas separadas.
   - **Nº de aulas semanais**: quantas vezes aquela combinação aparece na
     grade-base da turma (contagem simples, não multiplicar por período).
   - **Nº de aulas programadas no semestre**: nº de aulas semanais x nº de
     semanas letivas ativas da turma, contadas dia da semana por dia da
     semana (não um número único para a turma toda), porque um feriado
     específico só derruba as aulas daquele dia da semana:
     - **Perguntar à escola, para cada grupo de turma, a data da última
       prova de 2ª chamada do semestre** — é o fim real do período letivo
       para efeito desta conta (depois disso as turmas que viajam saem de
       aula, e as demais encerram o ciclo de avaliação). Contar da semana 1
       do semestre até a semana dessa data.
     - Descontar a semana inteira vetada para provas (conselho de classe)
       **a não ser que a escola confirme que há aula normal nela** — por
       padrão, tratar como sem nenhuma aula.
     - Descontar, para cada dia da semana, os feriados que caem
       especificamente naquele dia da semana dentro do intervalo.
   - **Nº de aulas cedidas**: some, ao longo do semestre inteiro (P1 + P2),
     cada tempo em que essa disciplina/professor apareceu como doador em
     alguma prova de outra disciplina. Um mesmo par (dia/tempo) doado duas
     vezes no semestre (uma por período) conta 2.
   - **% de aulas cedidas no semestre**: aulas cedidas ÷ aulas programadas
     no semestre. Formatar como percentual (ex.: 18,5%).
   - Gerar a partir das planilhas de calendário já gravadas cruzadas com a
     grade-base, em script separado — mesmo princípio da tabela-resumo:
     não confiar na memória do gerador.
   - Ordenar por número de cedências decrescente, para destacar primeiro
     quem mais perdeu aula — é o uso principal do relatório: apontar
     professores que vêm sendo repetidamente prejudicados pela mesma
     disciplina (ver o caso de referência da Profa. Luiza/Biologia, que deu
     origem à regra de alternância de doador, abaixo).

## Verificação obrigatória antes de entregar

Escreva um **script de verificação separado** que releia os arquivos .xlsx
gravados (sem confiar na memória do gerador) e cheque cada item abaixo.
Erros silenciosos são o risco principal aqui: prova descartada por célula
ocupada, marcação herdada de outra turma, disciplina sem slot possível.

- [ ] Nenhuma turma ultrapassa 3 avaliações na mesma semana (simulado de 2
      dias conta 1)
- [ ] Nenhum dia com mais de uma prova
- [ ] Disciplinas com professor comum entre turmas irmãs foram aplicadas
      simultaneamente (mesmo dia/tempo); as de professores diferentes
      puderam ficar em dias/tempos distintos
- [ ] Nenhuma prova cruza o intervalo (3º/4º ou 5º/6º tempos), salvo os
      casos sinalizados como último recurso (célula destacada + registrado
      no relatório)
- [ ] Quando a mesma disciplina/professor tem mais de uma prova de tempos
      duplos no semestre, o tempo emprestado alterna de lado sempre que as
      outras regras permitirem
- [ ] Disciplinas do grupo 1 não coincidem na mesma semana — salvo o par
      permitido de duas em que uma delas é Inglês (nunca três, nunca um par
      sem Inglês)
- [ ] Cada disciplina tem exatamente o número de provas esperado (2, ou 1
      para as de prova única) — se aparecer 1 onde deveria haver 2, alguma
      prova foi descartada silenciosamente na escrita
- [ ] Nas disciplinas com 2 provas no semestre, a distância entre as
      semanas das duas é de **pelo menos 4**
- [ ] Provas combinadas (LP/LIT/RED) usam o número certo de tempos e não
      aparecem como disciplinas separadas
- [ ] LP/LIT/RED (turmas 10, 11 e 12) caiu na 1ª ou 2ª semana de cada
      rodada (P1 e P2), nas duas turmas irmãs
- [ ] Disciplinas de prova única usam apenas 1 tempo
- [ ] Nenhuma prova para disciplinas sem avaliação
- [ ] Toda prova nos tempos 7 a 11 é inevitável — a disciplina não tem
      nenhum slot possível pela manhã
- [ ] Nenhuma prova usa tempo de disciplina que tem só 1 aula na semana
- [ ] Todos os simulados nas datas oficiais e nos tempos corretos, e **todos
      com preenchimento amarelo** (não herdado por coincidência — checar a
      cor de fato, célula por célula) e **nenhuma outra célula usa amarelo**
- [ ] Cada célula de prova/simulado está **mesclada** (bloco de 3 linhas
      numa célula só, sem linha divisória visível por dentro)
- [ ] A mesma disciplina usa **a mesma cor** em todas as séries/turmas
      (exceto onde o destaque de intervalo ou o amarelo do simulado
      sobrescrevem, de propósito)
- [ ] Toda cor de preenchimento é **opaca** — `cell.fill.fgColor.rgb`
      começa com `FF`, nunca `00` (ver a pegadinha do `PatternFill` de
      6 dígitos, que grava a cor mas fica invisível no Excel)
- [ ] Nenhuma prova em feriado, na semana vetada, antes do início do
      período ou depois da data-limite do grupo daquela turma
- [ ] Todo tempo emprestado de outro professor está no relatório de trocas
- [ ] A tabela-resumo tem o mesmo número de linhas que o calendário tem de
      avaliações, e todas as siglas foram traduzidas em nomes
- [ ] O relatório de tempos cedidos bate com o relatório de trocas de
      tempo: toda cedência de um está refletida no outro
- [ ] Nos **limites de cessão de aula**: nenhuma disciplina de 1 aula
      semanal cedeu; nenhuma de 2-3 aulas semanais passou do teto dela
      (2, ou 3 nas disciplinas com exceção); nenhuma passou do teto
      percentual; nenhuma ficou duas semanas seguidas sem contato com a
      turma por causa de cessão; e nenhuma cedeu na semana da própria
      prova ou na anterior
- [ ] O que o gerador anunciou ter relaxado bate exatamente com o que o
      verificador lista como aviso — se o gerador disse "todos os limites
      estritos", não pode haver nenhum aviso de regra de cessão; se disse
      "regra 4 relaxada em ['11C1']", os avisos de véspera-da-própria-prova
      só podem aparecer nessa turma, nenhuma outra
- [ ] Mesmo nas turmas com a **regra 4 relaxada**, nenhuma cessão aparece
      antes ou no dia da própria prova — só depois. Uma cessão antes da
      prova é sempre falha, nunca é coberta pela relaxação
- [ ] A estrutura de saída está conforme combinado

