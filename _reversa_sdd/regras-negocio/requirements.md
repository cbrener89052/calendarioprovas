# Requirements: Regras de Negócio

> Identificador: `006-regras-negocio`
> Data: `2026-08-21`
> Fonte viva: `.claude/skills/calendario-provas/SKILL.md` (1051 linhas, hash em `sources.json`)

## 1. Resumo executivo

Feature **regras-negocio** formaliza o catálogo de regras da escola — hoje na
**skill** + constantes Python + checklist verificador. Na plataforma: catálogo
BD, **Telas 1–2** de seleção/flexibilização, `RuleSetSnapshot` por rodada, sync
com `sources.json`.

## 2. Contexto

| Fonte | Confiança |
|-------|-----------|
| Skill `calendario-provas` | 🟢 |
| `_reversa_sdd/adrs/005-skill-fonte-viva-regras.md` | 🟢 |
| `.reversa/context/sync-regras.md` | 🟢 |
| `_reversa_sdd/addenda/skill-github-sync-2026-08-20.md` | 🟢 |

## 3. Regras de negócio (meta)

1. **RN-01:** Skill Git = fonte humana principal; código implementa subconjunto. 🟢
2. **RN-02:** Regras inegociáveis (R-P1, simulados fixos) sempre ativas; flex bloqueada. 🟢
3. **RN-03:** Coordenador marca **Aplicar** / **Pode flexibilizar** antes da fatoração. 🟢
4. **RN-04:** Regras novas (Tela 2) podem ser `fixa` ou `sessao`. 🟡
5. **RN-05:** Regra **2ª chamada por período** documentada na skill (08/2026) — 🔴 não implementada no gerador. 🟢 skill / 🔴 código
6. **RN-06:** Regras ENEM / véspera 2CH documentadas — 🔴 não implementadas. 🟡
7. **RN-07:** `FERIADOS` vs `BLOQUEIOS` Must unificar via `CalendarConstraints` (ADR-012). 🟡

## 4. Catálogo (amostra — skill)

| ID | Nome | Inegociável | Flexível |
|----|------|-------------|----------|
| R-P1 | Professor presente | sim | não |
| R-FIX | Simulados/datas forçadas | sim | não |
| R-C1..C5 | Cessão Proposta 3 | não | sim (escada) |
| R-SEM | Limite provas/semana | não | sim |
| R-G1 | Grupo 1 | não | sim |
| R-2CH | Prova antes 2ª chamada do período | sim 🟡 | não |

## 5. Requisitos Funcionais — plataforma

| ID | Requisito | Must |
|----|-----------|------|
| RF-01 | `RulesCatalogService` espelha seções da skill | Must |
| RF-02 | `RulesSelectionWizard` Tela 1 — catálogo existente | Must |
| RF-03 | Tela 2 — regras adicionais opcionais | Should |
| RF-04 | Persistir `RuleSetSnapshot` por calendário/rodada | Must |
| RF-05 | Solver/verificador recebem snapshot — regras desmarcadas ignoradas | Must |
| RF-06 | Sync hash skill → alerta defasagem specs | Should |
| RF-07 | Export PDF regras (`exportar_regras_pdf.py`) | Could |

## 6. Critérios de Aceitação

```gherkin
Cenário: Seleção de regras antes da fatoração
  Dado coordenador na Tela 1 com R-C4 desmarcada "aplicar"
  Quando dispara fatoração
  Então solver não aplica limite C4 nesta rodada

Cenário: Skill atualizada no GitHub
  Dado hash em sources.json diverge da skill local
  Quando sistema detecta sync
  Então alerta coordenador para re-validar catálogo
```

## 7. Lacunas

- 🔴 Implementar R-2CH no gerador e verificador
- 🔴 ENEM / véspera 2CH
- 🟡 Parser automático skill → catálogo BD

## 8. Histórico

| Data | Alteração |
|------|-----------|
| 2026-08-21 | Versão inicial + regras 2CH pós-sync GitHub |
