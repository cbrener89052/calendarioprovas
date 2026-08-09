# Inventário — calendarioprovas

> Gerado pelo Scout (Reversa) em 2026-08-09

## Visão geral

Sistema **Python CLI** para montar calendários de provas da Escola Alemã Corcovado.
Processa planilhas Excel e PDFs de horários; **não possui banco de dados, API web
nem interface gráfica** no estado atual. Evolução planejada: plataforma multi-coordenador
com PostgreSQL (ver `.reversa/context/user-requirements.md`).

## Estrutura de pastas

```
calendarioprovas/
├── gerar_calendario.py          # Core: gera propostas de calendário
├── verificar_calendario.py      # Valida planilhas geradas
├── exportar_tabelas_turma.py    # Tabela-resumo por turma
├── exportar_tempos_cedidos.py   # Relatório de cessões
├── exportar_regras_pdf.py       # Exporta regras para PDF
├── analisar_*.py, comparar_*.py # Análise de semestres anteriores
├── extrair_grade_*.py           # Extração de grades de PDF
├── horarios2025/                # Grades extraídas 2025
├── horarios_1semestre/          # Horários 1º sem 2026
├── horarios turmas/             # PDF horário-base Untis
├── Horario modelo/              # Modelo xlsx + referência 1º sem
├── Horario desenvolvido/        # Saídas geradas (propostas, relatórios)
├── siglas/                      # Planilha sigla → professor
├── SIMULADOS/                   # PDF calendário simulados
├── referencia/                  # Decisões e estado da rodada
├── provas2sem_2025/             # Calendário 2025 referência
├── .claude/skills/calendario-provas/  # Regras de negócio (skill)
├── *.bat                        # Sync GitHub (Windows)
└── Klausurplan_2026_2SEM.xlsx   # Modelo ativo 2º sem 2026
```

## Linguagens (contagem de arquivos)

| Linguagem | Extensão | Arquivos (código) |
|---|---|---|
| Python | `.py` | 16 |
| Markdown | `.md` | ~10 (projeto) |
| Batch | `.bat` | 4 |
| Excel | `.xlsx` | ~12 |
| PDF | `.pdf` | ~5 |

**Linguagem principal:** Python 3

## Módulos funcionais identificados

| Módulo | Scripts | Responsabilidade |
|---|---|---|
| **geracao-calendario** | `gerar_calendario.py` | Aloca provas, escreve xlsx, relatório trocas |
| **verificacao** | `verificar_calendario.py` | Checklist automático pós-geração |
| **exportacao-relatorios** | `exportar_tabelas_turma.py`, `exportar_tempos_cedidos.py`, `exportar_regras_pdf.py` | Relatórios derivados |
| **extracao-grade** | `extrair_grade_*.py`, `esqueleto_grade_2025.py`, `limpar_grade_2025.py`, `horarios2025/*.py` | PDF → estrutura de grade |
| **analise-historica** | `analisar_*.py`, `comparar_semestres.py`, `contar_2sem_2025.py` | Análise semestres passados |
| **regras-negocio** | `.claude/skills/calendario-provas/SKILL.md` | Regras formais de distribuição |
| **sincronizacao** | `commit_github.bat`, `atualizar_do_github.bat`, etc. | Git sync Windows |

## Pontos de entrada (CLI)

| Script | Comando | Papel |
|---|---|---|
| `gerar_calendario.py` | `python gerar_calendario.py` | **Entry point principal** |
| `verificar_calendario.py` | `python verificar_calendario.py` | Validação |
| `exportar_tabelas_turma.py` | `python exportar_tabelas_turma.py` | Export tabelas |
| `exportar_tempos_cedidos.py` | `python exportar_tempos_cedidos.py` | Export cessões |

Demais scripts são utilitários pontuais (extração, análise histórica).

## Configuração e infraestrutura

| Item | Status |
|---|---|
| `requirements.txt` | **Ausente** |
| `.env` / config | **Ausente** (constantes no código) |
| Banco de dados | **Ausente** |
| Docker | **Ausente** |
| CI/CD | **Ausente** |
| Testes automatizados | **Ausente** |

## Dados de entrada/saída

**Entradas:**
- `Klausurplan_2026_2SEM.xlsx` — modelo com datas
- `horarios turmas/*.pdf` — grade Untis
- `siglas/siglas_profs_aux_etc.xlsx`
- `SIMULADOS/*.pdf`

**Saídas:**
- `Horario desenvolvido/Proposta_*_Calendario_*.xlsx`
- `Horario desenvolvido/Relatorio_trocas_de_tempo.md`
- `Horario desenvolvido/Tabela_*.xlsx`, `Relatorio_Tempos_Cedidos_*.xlsx`

## Integrações externas

Nenhuma API externa. Dependência de bibliotecas Python locais (openpyxl, pymupdf).
