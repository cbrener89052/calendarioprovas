---
schemaVersion: 1
generatedAt: 2026-08-10T02:20:00Z
reversa:
  version: "1.2.58"
kind: parity_specs
producedBy: inspector
---

# Parity Specs

> Equivalência CLI legado ↔ plataforma web. Paradigma: híbrido (procedural solver preservado).

## Estratégia geral

- [x] Characterization tests (comportamento legado como oráculo)
- [x] Contract tests (OpenAPI FastAPI)
- [x] Data parity (checksum xlsx + relatórios)
- [ ] Shadow mode (opcional pós-MVP)
- [x] Contract test de tela (modo modernizado)

## Critérios de paridade aceita

- **Métrica primária**: 0 divergências críticas em xlsx e verificador entre CLI e plataforma para mesmo semestre piloto
- **Janela**: Parallel Run completo (≥2 segmentos ou 8 turmas C)
- **Bloqueio cutover**: Qualquer falha check 5a-bis (LP/LIT/RED), cessão dura, ou max 3/semana

## Cobertura adaptada ao paradigma

### Procedural → camadas + solver wrap

- **Equivalência funcional**: mesmas entradas (grade, modelo, GRUPO params, RuleContext) → mesmo xlsx (normalização metadata)
- **Invariantes**: backtracking produz mesma alocação com SEED_PROPOSTA_3=3
- **Side effects**: stdout legado ↔ job status + blobs plataforma
- **Validação**: verificador plataforma aplica mesmos checks que `verificar_calendario.py`

### Dimensões adicionais

| Dimensão | Critério |
|----------|----------|
| Idempotência job | Re-enqueue mesmo semestre não corrompe estado (versionamento calendario) |
| Tenant isolation | Coord A não vê job de B |
| Toggle regras | RuleContext off = comportamento sem restrição |

## Tipos de teste

| Tipo | Ferramenta sugerida |
|------|---------------------|
| Funcional solver | pytest + diff openpyxl |
| API contract | schemathesis / pytest + OpenAPI |
| E2E UI | Playwright (fluxo SCR-07) |
| Performance | job duration ≤ 2× CLI |

## Paridade de telas (modernizado)

- Hierarquia componentes conforme `target_screens.md`
- 4 estados por tela
- Textos de erro verificador alinhados ao legado

## Exceções

(nenhuma — screen_deviation_log vazio)

## Saídas

- `parity_tests/01-geracao-proposta3.feature`
- `parity_tests/02-verificacao-calendario.feature`
- `parity_tests/03-isolamento-tenant.feature`
- `parity_tests/04-toggles-regras.feature`
- `parity_tests/05-export-relatorios.feature`

## Reuso characterization_specs

Não existem specs prévias; suíte derivada de `code-analysis.md` e requirements features.
