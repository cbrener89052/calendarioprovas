---
schemaVersion: 1
generatedAt: 2026-08-10T02:15:00Z
reversa:
  version: "1.2.58"
kind: screen_modernization_decision
producedBy: screen_translator
mode: modernizado
---

# Screen Modernization Decision

## Plataforma origem

| Atributo | Valor |
|----------|-------|
| Tipo | CLI Python batch |
| UI detectada | Nenhuma (🟢 CONFIRMADO) |
| Evidência | `architecture.md`, `inventory.md` — scripts sem GUI |

## Plataforma alvo

| Atributo | Valor |
|----------|-------|
| Tipo | Web SPA |
| Stack | React 18 + Vite + TypeScript + Tailwind + Lucide |
| Evidência | ADR-007, `plataforma-multi-coordenador/design.md` |

## Modos considerados

| Modo | Veredito |
|------|----------|
| Literal | N/A — legado sem telas |
| **Modernizado** | **Escolhido** — greenfield UI derivada de specs plataforma |
| Híbrido | N/A |

## Decisão

**Modo: modernizado**

Telas derivadas de `plataforma-multi-coordenador/design.md § Frontend` e user story `fluxo-calendario-semestre.md`. Cada tela declara 4 estados: idle, loading, error, success.

## Trade-offs

- **Prós**: UX adequada multi-coord; tokens Tailwind; sem dívida de terminal
- **Contras**: Sem golden visual legado; paridade é funcional (xlsx), não pixel

## Aprovação

- **Quem**: auto (`--auto`)
- **Quando**: 2026-08-10T02:15:00Z

## Implicações Inspector

- Paridade visual: contract test de tela (hierarquia + eventos + textos)
- Paridade funcional: xlsx + verificador (parity_tests geracao)
