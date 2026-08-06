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
  mais o relatório de trocas de tempo entre professores.
- **`verificar_calendario.py`** — relê as planilhas geradas (sem confiar na
  memória do gerador) e confere o checklist: limite de 3 avaliações por
  semana, disciplinas do grupo 1 sem coincidir, feriados, semana vetada,
  datas-limite por grupo de turma, simulados nas datas oficiais, número de
  provas por disciplina.

```bash
pip install openpyxl
python gerar_calendario.py
python verificar_calendario.py
```

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
- **Tempos emprestados**: quando a prova precisa de mais de um tempo
  seguido, o tempo extra vem de outra disciplina daquele dia — antes ou
  depois do tempo da própria disciplina. Todas as trocas ficam registradas
  em `Horario desenvolvido/Relatorio_trocas_de_tempo.md`.

## Enviar para o GitHub

Dois cliques em `commit_github.bat`. Na primeira vez o Git pede o login;
use um Personal Access Token no lugar da senha.
