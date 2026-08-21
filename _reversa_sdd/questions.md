# Perguntas para Validação — calendarioprovas

> Gerado pelo Revisor em 2026-08-21  
> **Status:** defaults 🟡 aplicados em 2026-08-21 — Brener respondeu `continuar` sem escolher opções explícitas.

---

## Pergunta 1 — L-01 R-2CH (prova antes da 2ª chamada do período)

**Contexto:** Skill `calendario-provas` (sync 2026-08-20) exige R-2CH; `gerar_calendario.py` e `verificar_calendario.py` não implementam.

**Spec afetada:** `_reversa_sdd/regras-negocio/requirements.md`, `_reversa_sdd/geracao-calendario/`

**Pergunta:** O que fazer com R-2CH no ciclo forward?

| Opção | Descrição |
|-------|-----------|
| **a** | Won't — manter só na skill/checklist manual |
| **b** | **Must implementar** no solver + verificador antes da plataforma |
| **c** | Should — implementar só no verificador primeiro |

**Impacto:** Define prioridade T-12+ em `geracao-calendario/tasks.md` e checklist item 2CH.

**Resposta (default 🟡):** **b** — Must implementar no solver e verificador; regra inegociável conforme skill; datas de 2CH informadas via `CalendarBlockPicker` / modelo (marcação `"2CH <séries>"`).

✅ Respondida (default inferido)

---

## Pergunta 2 — L-02 ENEM / véspera 2CH série 9

**Contexto:** Skill documenta restrições ENEM (semanas com disciplinas limitadas) e véspera 2CH para 9C; código ausente.

**Spec afetada:** `_reversa_sdd/regras-negocio/requirements.md`, `_reversa_sdd/geracao-calendario/`

**Pergunta:** Escopo das regras ENEM e véspera 2CH?

| Opção | Descrição |
|-------|-----------|
| **a** | **Must** — mesma prioridade que R-2CH; perguntar datas ENEM na UI |
| **b** | Should — verificador primeiro, solver depois |
| **c** | Could — só documentar até coordenação validar datas 2026 |

**Impacto:** Telas de entrada (datas ENEM) + constraints no solver.

**Resposta (default 🟡):** **a** — Must; véspera 2CH série 9 é **primeira regra a flexibilizar** (skill); ENEM exige duas datas (domingos) na rodada.

✅ Respondida (default inferido)

---

## Pergunta 3 — L-03 Parser grade 2º sem 2026

**Contexto:** Rodada ativa usa `GRADE_TXT` hardcoded; extractors existem para 2025 OCR e 1º sem 2026.

**Spec afetada:** `_reversa_sdd/extracao-grade/`

**Pergunta:** Estratégia para grade do 2º semestre?

| Opção | Descrição |
|-------|-----------|
| **a** | Manter `GRADE_TXT` manual no legado indefinidamente |
| **b** | **Plataforma: upload PDF Must**; legado mantém hardcode até parser 2sem existir |
| **c** | Criar `extrair_grade_2semestre.py` no legado antes da plataforma |

**Impacto:** `GradeParserService` e T-05 plataforma.

**Resposta (default 🟡):** **b** — plataforma Must aceita upload PDF Untis (reutilizar pipeline 1º sem onde couber); legado continua `GRADE_TXT` até T-parser-2sem no forward.

✅ Respondida (default inferido)

---

## Pergunta 4 — L-04 Auth / RBAC 5 coordenadores

**Contexto:** Requisito usuário: login individual, 5 coordenadores, isolamento de dados.

**Spec afetada:** `_reversa_sdd/plataforma-multi-coordenador/`, `_reversa_sdd/permissions.md`

**Pergunta:** Modelo de autenticação e isolamento?

| Opção | Descrição |
|-------|-----------|
| **a** | **E-mail + senha** (JWT), row-level por `coordenador_id`; templates institucionais read-only compartilhados |
| **b** | SSO escola (SAML/OIDC) — aguardar TI |
| **c** | Conta única compartilhada + PIN por coordenador |

**Impacto:** T-02 plataforma, ERD `usuario`, middleware FastAPI.

**Resposta (default 🟡):** **a** — e-mail + senha com JWT (refresh token); isolamento estrito por coordenador; papel `admin_instituicao` para SMTP/usuários; sem portal professor na v1.

✅ Respondida (default inferido)

---

## Pergunta 5 — L-05 `exportar_regras_pdf` / fpdf

**Contexto:** Script legado falhou no cloud agent por dependência `fpdf` ausente.

**Spec afetada:** `_reversa_sdd/exportacao-relatorios/`

**Pergunta:** Destino do export PDF de regras?

| Opção | Descrição |
|-------|-----------|
| **a** | Remover RF-05 — regras só na plataforma/skill |
| **b** | **Could v1** — adicionar `fpdf` ao legado; plataforma gera HTML/PDF na v1.1 |
| **c** | Must — PDF institucional na v1 da plataforma |

**Impacto:** `requirements.txt`, `ReportExporter`.

**Resposta (default 🟡):** **b** — RF-05 permanece Could; forward adiciona `fpdf` ao legado; plataforma v1 exporta regras como HTML/Markdown indexável (PDF na v1.1).

✅ Respondida (default inferido)
