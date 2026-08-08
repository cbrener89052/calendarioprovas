# Calendário de Provas — Escola Alemã Corcovado

Estrutura, dados e scripts para montar o calendário de provas das turmas C
a cada semestre.

## Pastas

| Pasta | Conteúdo |
|---|---|
| `Horario modelo/` | Modelo da planilha de saída e o calendário do semestre anterior (referência) |
| `horarios turmas/` | Horário-base das turmas (grade semanal, PDF do Untis) |
| `siglas/` | Planilha de siglas dos professores |
| `SIMULADOS/` | Calendário oficial de simulados e avaliações globais |
| `Horario desenvolvido/` | Propostas geradas + relatório de trocas de tempo |
| `referencia/` | Decisões e regras confirmadas para a rodada em andamento |
| `.claude/skills/calendario-provas/` | Skill do Claude com as regras de montagem |

## Scripts

- **`gerar_calendario.py`** — monta as propostas de calendário. Lê o modelo
  `Klausurplan_2026_2SEM.xlsx`, aplica as regras de distribuição e grava um
  arquivo por proposta em `Horario desenvolvido/`, com uma aba por turma,
  mais o relatório de trocas de tempo entre professores. As Propostas 1 e 2
  seguem as regras gerais; a **Proposta 3** aplica, além delas, os limites
  de cessão de aula (ver abaixo).
- **`verificar_calendario.py`** — relê as planilhas geradas (sem confiar na
  memória do gerador) e confere o checklist: limite de 3 avaliações por
  semana, disciplinas do grupo 1 sem coincidir, feriados, semana vetada,
  datas-limite por grupo de turma, simulados nas datas oficiais, número de
  provas por disciplina, provas à tarde só quando inevitáveis, e nenhum
  tempo cedido por disciplina de uma aula semanal.
- **`exportar_tabelas_turma.py`** — gera a tabela-resumo por turma a partir
  das propostas já gravadas: disciplina, professores (sigla + nome completo),
  dia e tempos da prova, e número de tempos. Uma aba por turma.
- **`exportar_tempos_cedidos.py`** — gera o relatório de tempos cedidos por
  turma a partir das propostas já gravadas, cruzando com a grade-base: para
  cada disciplina/professor, número de aulas semanais e número de aulas
  cedidas no semestre para provas de outras disciplinas. Uma aba por turma.

## Como rodar (em qualquer máquina)

```bash
git clone https://github.com/cbrener89052/calendarioprovas.git
cd calendarioprovas
pip install openpyxl

python gerar_calendario.py        # gera as 2 propostas + relatório de trocas
python verificar_calendario.py    # confere tudo; deve terminar com "OK"
python exportar_tabelas_turma.py  # gera as tabelas-resumo por turma
python exportar_tempos_cedidos.py # gera os relatórios de tempos cedidos
```

A skill fica em `.claude/skills/calendario-provas/` e é carregada
automaticamente pelo Claude Code ao abrir esta pasta.

## Regras aplicadas (2º semestre de 2026)

- **Períodos**: P1 de 17/08 a 11/09 para todas as turmas. P2 até 12/11 para
  as turmas 10 e 12 (viagem à Alemanha) e até 21/11 para as turmas 9 e 11.
- **Bloqueios**: feriados de 07/09, 02/11 e 20/11; semana inteira de 12/10 a
  16/10 (o feriado de 12/10 cai nela).
- **Máximo de 3 avaliações por semana** por turma; simulado de 2 dias conta
  como 1 avaliação.
- **Grupo 1** (Matemática, Alemão, Português/LP-LIT-RED e Inglês) não
  coincide na mesma semana.
- **LP/LIT/RED**: nas turmas 10, 11 e 12, Português, Redação e Gramática são
  uma prova única de 3 tempos seguidos, no mesmo dia, com os três
  professores. Nas turmas 9, Redação e Português são separadas, 2 tempos
  cada.
- **Prova única no semestre**: Filosofia e Sociologia (1 tempo); e também
  Biologia, Química e Física nas turmas do 9º ano (1 tempo cada).
- **Sem prova**: Educação Física, Artes/Música/Teatro, Técnicas, Finanças,
  Socioemocional, apoio/aprofundamento, eletivas e Projeto Vestibular.
- **Simulados**: do 2º ao 7º tempo, nas datas oficiais (AG9 02/10; AG10
  11/09; S3-11 25 e 26/08; S4-11 26 e 27/10; S4-12 16 e 17/09).
- **Horário do dia**: evita ao máximo os tempos 7 a 11 (a partir das
  12h45). As poucas provas que sobram nesses tempos são inevitáveis — a
  disciplina não tem nenhuma aula pela manhã na grade da turma.
- **Tempos emprestados**: quando a prova precisa de mais de um tempo
  seguido, o tempo extra vem de outra disciplina daquele dia — antes ou
  depois do tempo da própria disciplina. **Disciplinas com uma única aula
  na semana (Filosofia, Sociologia e afins) não podem ceder tempo**, pois
  perderiam a aula inteira. Todas as trocas ficam registradas em
  `Horario desenvolvido/Relatorio_trocas_de_tempo.md`.

## Limites de cessão de aula (só na Proposta 3)

A Proposta 3 mantém todas as regras acima e acrescenta tetos para proteger
a carga horária de quem cede tempo. Os tetos valem por
**(disciplina, professor) dentro de cada turma**:

1. Disciplina com **2 ou 3 aulas semanais**: no máximo **2 cessões** no
   semestre — **3** para História, Geografia e GL.
2. Disciplina com **1 aula semanal**: **não cede** nada.
3. Nenhuma disciplina fica **duas semanas seguidas sem contato com a
   turma** por causa das cessões. A semana de conselho de classe
   (12–16/10, sem aula) conta como semana sem contato, então ceder todas
   as aulas na semana anterior ou posterior a ela também viola a regra.
4. Nenhuma disciplina cede aula **na semana da própria prova ou na
   semana anterior** — é a aula de revisão.
5. Nenhuma disciplina cede mais de **11%** das aulas programadas dela no
   semestre (alvo 10%; a folga até 11% é o que permite as 3 cessões das
   disciplinas de 2 aulas semanais da regra 1).

Quando a regra 1 e a regra 5 discordam, vale a mais restritiva. Datas de
prova exigidas pela coordenação são inegociáveis: nenhuma cessão ocorre na
semana delas nem na anterior.

Se os limites estritos não fecharem, o gerador afrouxa nesta ordem —
tetos +1, depois regra 4, depois regra 3 — e avisa no terminal o que foi
relaxado. **As regras 1, 2 e 5 nunca são relaxadas.** O
`verificar_calendario.py` separa **falhas** (regras que valiam) de
**avisos** (regras relaxadas de propósito).

Resultado desta rodada: a Proposta 3 fechou com **as cinco regras
integrais, sem nenhuma exceção**. O pior caso de cessão caiu de 23,1%
(Proposta 1) para 10,7%.

## Sincronizar com o GitHub

Repositório remoto: https://github.com/cbrener89052/calendarioprovas

### Pasta local já existente (Windows)

Se os arquivos já estão em uma pasta (por exemplo
`C:\Users\cbrener\Downloads\CALENDARIODEPROVAS\calendarioprovas`) e você
quer ligá-la ao GitHub **sem apagar nada**:

1. Copie para essa pasta os arquivos `.bat` deste repositório (ou clone
   o repo em outro lugar e copie o conteúdo para lá).
2. Dê dois cliques em **`configurar_pasta_local.bat`** — ele cria o
   `.git`, conecta o remoto, une com a `main` do GitHub e configura o
   acompanhamento (`push` / `pull`).
3. Na primeira vez o Git pede login; use um
   [Personal Access Token](https://github.com/settings/tokens) no lugar
   da senha.

Depois disso:

| Ação | Arquivo |
|---|---|
| Enviar alterações locais → GitHub | `commit_github.bat` |
| Baixar alterações do GitHub → pasta | `atualizar_do_github.bat` |

### Pasta nova (qualquer sistema)

```bash
git clone https://github.com/cbrener89052/calendarioprovas.git
cd calendarioprovas
```

No Windows, após editar arquivos, use `commit_github.bat` para enviar.
