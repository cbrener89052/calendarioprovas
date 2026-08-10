---
schemaVersion: 1
generatedAt: 2026-08-10T02:00:00Z
reversa:
  version: "1.2.58"
kind: target_business_rules
producedBy: curator
---

# Target Business Rules

> Catálogo das regras de negócio do legado com decisão de migração: MIGRAR, DESCARTAR ou DECISÃO HUMANA.

## Resumo

- Total de regras analisadas: 42
- MIGRAR: 34
- DESCARTAR: 6 (detalhe em `discard_log.md`)
- DECISÃO HUMANA: 2 (resolvidas em auto — ver `ambiguity_log.md`)

## Regras MIGRAR

### BR-MIGRAR-001 — Máx. 3 avaliações/semana
- **Origem**: `geracao-calendario/requirements.md` RN-01
- **Confiança original**: 🟢
- **Descrição**: No máximo 3 avaliações por semana por turma; simulado de 2 dias conta como 1.
- **Justificativa**: Regra core Proposta 3; solver preservado.
- **Compatibilidade**: Expressa via `RuleContext` + constantes externalizadas.

### BR-MIGRAR-002 — Uma prova por dia
- **Origem**: `geracao-calendario/requirements.md` RN-02 | 🟢
- **Descrição**: Uma prova por dia por turma.

### BR-MIGRAR-003 — Distância 4 semanas entre provas
- **Origem**: `geracao-calendario/requirements.md` RN-03 | 🟢

### BR-MIGRAR-004 — Período por GRUPO configurável
- **Origem**: `geracao-calendario/requirements.md` RN-04 | 🟢
- **Descrição**: Provas dentro do período do GRUPO, excluindo feriados e semana vetada de conselho.
- **Nota**: Substitui hardcode `10_12`/`9_11`; params vêm de PostgreSQL.

### BR-MIGRAR-005 — Cessão Proposta 3 (regras 1–5)
- **Origem**: `geracao-calendario/requirements.md` RN-05, RN-06 | 🟢
- **Descrição**: Regras 1, 2, 5 duras; 3 e 4 relaxáveis na escada; regra 4 só depois da prova.

### BR-MIGRAR-006 — Bloco LP/LIT/RED 3 tempos
- **Origem**: `geracao-calendario/requirements.md` RN-07 | 🟢

### BR-MIGRAR-007 — LP/LIT/RED ≥10 dias antes conselho
- **Origem**: `geracao-calendario/requirements.md` RN-08 | 🟢
- **Nota**: PR #18 implementado (`LIMITE_LPLITRED_CONSELHO=9`).

### BR-MIGRAR-008 — Relatório regras relaxadas
- **Origem**: `geracao-calendario/requirements.md` RN-09 | 🟢

### BR-MIGRAR-009 — Verificador pós-geração
- **Origem**: `verificacao-calendario/requirements.md` | 🟢
- **Descrição**: Checks 1–5 + 5a-bis; bloqueia publish se erro crítico.

### BR-MIGRAR-010 — Exportação 8 abas + relatórios
- **Origem**: `exportacao-relatorios/requirements.md` | 🟢
- **Descrição**: Paridade xlsx, tabela-resumo, cessões, trocas.

### BR-MIGRAR-011 — Extração grade PDF/xlsx
- **Origem**: `extracao-grade/requirements.md` | 🟡
- **Nota**: Validar no agente de codificação; upload na plataforma.

### BR-MIGRAR-012 — SKILL fonte viva de regras
- **Origem**: `regras-negocio/requirements.md` RN-01 | 🟢

### BR-MIGRAR-013 — Catálogo REGRA_CATALOGO + toggles
- **Origem**: `regras-negocio/requirements.md` RN-03, RF-02, RF-03 | 🟢

### BR-MIGRAR-014 — Customização IA (verificador + relatório)
- **Origem**: `regras-negocio/requirements.md` RN-05 | 🟢
- **Decisão Brener 2026-08-09**: não altera solver determinístico.

### BR-MIGRAR-015 — RuleContext para solver
- **Origem**: `regras-negocio/requirements.md` RF-08 | 🟡
- **Nota**: Spec pronta; implementação na codificação.

### BR-MIGRAR-016 — Isolamento tenant por segmento
- **Origem**: `plataforma-multi-coordenador/requirements.md` RN-01 | 🟢

### BR-MIGRAR-017 — GRUPO customizável (datas, conselho, 2CH)
- **Origem**: `plataforma-multi-coordenador/requirements.md` RN-02, RN-03 | 🟢

### BR-MIGRAR-018 — RBAC admin_instituicao + coordenadores
- **Origem**: `permissions.md`, resposta Brener | 🟢
- **Descrição**: Brener admin global; coords só no próprio segmento.

### BR-MIGRAR-019 — Job assíncrono gerar calendário
- **Origem**: `plataforma-multi-coordenador/requirements.md` RF-06 | 🟢

### BR-MIGRAR-020 — Upload entradas → blob + metadados
- **Origem**: `plataforma-multi-coordenador/requirements.md` RF-05 | 🟢

### BR-MIGRAR-021 — Sync skill ↔ catálogo BD
- **Origem**: `regras-negocio/requirements.md` RF-07 | 🟡

### BR-MIGRAR-022 — folga_extra por turma (cessão localizada)
- **Origem**: PR #18 / `addenda/sync-skill-2026-08-10.md` | 🟢

### BR-MIGRAR-023 — SEED_PROPOSTA_3 = 3
- **Origem**: PR #18 | 🟢

### BR-MIGRAR-024 — Simulados fixos por série
- **Origem**: `domain.md`, skill | 🟢

### BR-MIGRAR-025 — Turmas irmãs coordenadas
- **Origem**: `geracao-calendario/requirements.md` RF-02 | 🟢

### BR-MIGRAR-026 — Grupos paralelos prova simultânea
- **Origem**: skill calendario-provas | 🟢

### BR-MIGRAR-027 — Disciplinas 1 prova/semestre por série
- **Origem**: skill | 🟢

### BR-MIGRAR-028 — Preferência primeiros tempos
- **Origem**: skill | 🟢

### BR-MIGRAR-029 — Deploy híbrido nuvem + Docker on-prem
- **Origem**: `plataforma-multi-coordenador/requirements.md` RN-05 | 🟢

### BR-MIGRAR-030 — Frontend React Vite + Tailwind
- **Origem**: ADR-007 | 🟢

### BR-MIGRAR-031 — Validação ARGB cores (Should)
- **Origem**: gaps G-M03 | 🟡
- **Nota**: Skill pede; verificador legado só texto — implementar na plataforma.

### BR-MIGRAR-032 — Audit log toggles/customizações (Should)
- **Origem**: gaps ADR-006 | 🟡

### BR-MIGRAR-033 — Publicar calendário com gate verificação
- **Origem**: `plataforma-multi-coordenador/requirements.md` RF-11 | 🟢

### BR-MIGRAR-034 — Export PDF regras a partir catálogo
- **Origem**: `regras-negocio/requirements.md` RF-06 | 🟢

## Regras DESCARTAR (resumo)

| ID | Origem | Motivo curto | Vínculo a paradigma? |
|---|---|---|---|
| BR-DESCARTAR-001 | CLI stdout | Substituído por API JSON + jobs | sim |
| BR-DESCARTAR-002 | Scripts `.bat` git sync | Escopo excluído (CI) | sim |
| BR-DESCARTAR-003 | `analise-historica` | Escopo v2 no brief | não |
| BR-DESCARTAR-004 | Paths cwd locais | Blob storage + BD | sim |
| BR-DESCARTAR-005 | Hardcode grupo viagem | GRUPO configurável absorve | sim |
| BR-DESCARTAR-006 | Execução manual coordenador CLI | UI web + worker | sim |

> Detalhe completo em `discard_log.md`.

## Regras DECISÃO HUMANA

### BR-HUMANA-001 — Context vs Redux
- **Origem**: ADR-007, `plataforma-multi-coordenador/design.md`
- **Tipo**: dependência de stakeholder
- **Descrição**: Escolha de biblioteca de estado global no frontend.
- **Opções**: (1) React Context, (2) Redux Toolkit
- **Recomendação do Curator**: Context para MVP (menos boilerplate); Redux se toggles/jobs complexos.
- **Status**: RESOLVIDA — **REFERIDA À CODIFICAÇÃO** (auto-decidido: implementador escolhe na T-13)

### BR-HUMANA-002 — Validação ARGB no verificador
- **Origem**: gaps G-M03
- **Tipo**: 🔴 GAP parcial
- **Opções**: (1) Implementar check ARGB na plataforma, (2) Manter só textual
- **Recomendação**: Implementar na plataforma (Should).
- **Status**: RESOLVIDA — MIGRAR como BR-MIGRAR-031 (auto-decidido)

## Notas

- Feature `analise-historica` fora do escopo v1 conforme `migration_brief.md`.
- PR #14/18 resolvido: LP/LIT/RED e folga_extra migrados.
- Itens auto-decididos registrados em `ambiguity_log.md` (modo `--auto`).
