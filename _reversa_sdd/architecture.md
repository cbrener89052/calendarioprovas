# Arquitetura — calendarioprovas

> Gerado pelo Arquiteto (Reversa) em 2026-08-15  
> Nível: **completo** | Confiança: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Visão geral

O **calendarioprovas** monta calendários de provas para turmas da Escola Alemã Corcovado. Hoje é um **sistema CLI monolítico** (Python + arquivos locais). A evolução acordada é uma **plataforma web multi-coordenador** (FastAPI + PostgreSQL + blob storage + frontend web).

| Aspecto | Legado 🟢 | Alvo 🟡 |
|---|---|---|
| Interface | Terminal + planilhas Excel | Web app |
| Persistência | Pastas + Git (`main`/`producao`) | PostgreSQL + S3/pasta local |
| Usuários | 1 operador implícito | 5 coordenadores com login |
| Regras | Skill + hardcode Python | Catálogo + solver + **copiloto IA (chat analista)** |
| Comunicação | Relatório manual | E-mail doadores (ação manual) |

Diagramas detalhados: `c4-context.md`, `c4-containers.md`, `c4-components.md`.  
Modelo de dados: `erd-complete.md`.  
Rastreabilidade: `traceability/spec-impact-matrix.md`.

---

## Arquitetura legada (as-is)

```
Coordenador (Windows)
    │
    ├── Python CLI (gerar / verificar / exportar)
    ├── Arquivos locais (xlsx, pdf, md)
    └── Git (main → producao)
```

**Características:**
- Núcleo: `gerar_calendario.py` — solver backtracking + openpyxl
- Validação: `verificar_calendario.py` — checklist 0–11
- Relatórios: scripts que **releem** xlsx gravado (ADR-002)
- Regras: `.claude/skills/calendario-provas/SKILL.md` + constantes em código
- Sem BD, sem API, sem testes automatizados 🟢

---

## Arquitetura alvo (to-be) 🟡

```
Coordenador (browser)
    │
    ▼
Frontend Web ──HTTPS──► API FastAPI (Python)
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
      PostgreSQL      Blob Storage      SMTP / Email
      (metadados)     (xlsx/pdf)        (doadores)
            │
            └── Solver module (extraído de gerar_calendario.py)
            └── ScheduleCopilotService (OpenAI + tool calling 🟢)
            └── RagIndexService (embeddings + busca documentos/xlsx 🟢)
            └── DocumentContextService (ingest corpus RAG)
            └── PythonActionBridge (tools → solver/verifier/patch 🟢)
            └── ProfessorPseudonymService (tokeniza siglas p/ OpenAI 🟢)
```

**Decisões arquiteturais acordadas** (user-requirements 2026-08-09):
- Deploy híbrido: nuvem + Docker Compose on-prem
- Evolução incremental do código Python existente
- Dados por coordenador + templates institucionais compartilhados 🟡

---

## Integrações externas

| Sistema | Legado | Alvo | Protocolo |
|---|---|---|---|
| GitHub | Sync código (`commit_github.bat`) | CI/CD deploy 🟡 | Git/HTTPS |
| Planilhas Excel | Entrada/saída principal | Import/export + blob | openpyxl / API |
| PDF Untis | Horários via PyMuPDF/OCR | Upload blob + parser | File |
| Tesseract | OCR grade 2025 | Opcional batch 🟡 | CLI |
| SMTP | — | E-mail doadores 🔴 | SMTP/API |
| Skill calendario-provas | Fonte regras | Catálogo BD espelhando skill | — |
| Provedor LLM / copiloto | Skill + chat externo (Cursor/Claude Code) | **OpenAI API** + RAG + `ScheduleCopilotService` | HTTPS 🟢 |

---

## Dívidas técnicas

| # | Dívida | Severidade | Confiança |
|---|---|---|---|
| DT-01 | Monolito 2135 linhas (`gerar_calendario.py`) | Alta | 🟢 |
| DT-02 | Regras triplicadas (skill / gerador / verificador) | Alta | 🟢 |
| DT-03 | `BLOQUEIOS` vs `FERIADOS` dessincronizados | Média | 🟢 |
| DT-04 | Grade hardcoded vs extração PDF | Média | 🟢 |
| DT-05 | Sem `requirements.txt` / testes | Alta | 🟢 |
| DT-06 | Regras skill não implementadas (ENEM, véspera 2CH) | Média | 🟢 |
| DT-07 | Lógica parse xlsx duplicada nos exportadores | Média | 🟢 |
| DT-08 | RBAC ausente | Alta (bloqueia multi-coord.) | 🟢 |

---

## Decisão arquitetural: isolamento multi-coordenador 🟡

**Proposta do Arquiteto** (pendente validação usuário):

| Camada | Escopo | Compartilhado? |
|---|---|---|
| `usuario` / `coordenador` | Login, perfil | Por pessoa |
| `semestre_rodada` | Calendário, entradas, saídas | **Por coordenador** |
| `regra_catalogo` | Definições de regras | **Institucional** (read) + override por rodada |
| `professor` / siglas | Nome, e-mail | **Institucional** 🟡 (provável) |
| `template_modelo` | Layout xlsx | **Institucional** |

Row-level security por `coordenador_id` em tabelas operacionais 🟡.

---

## Referências cruzadas

- Domínio: `domain.md`
- ADRs: `adrs/001`–`007`
- Requisitos: `.reversa/context/user-requirements.md`
- Fontes vivas: `.reversa/context/sources.json`
