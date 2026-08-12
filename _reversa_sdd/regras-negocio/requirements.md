# Requirements: Regras de Negócio

> Identificador: `006-regras-negocio`  
> Data: `2026-08-09`

## 1. Resumo executivo

Centraliza o catálogo vivo de regras de calendário de provas: fonte primária na skill `calendario-provas`, espelhada em PDF estático, sincronizada com Reversa e, na plataforma, materializada em `REGRA_CATALOGO` com toggles por segmento/semestre. Garante rastreabilidade skill → código → verificador.

## 2. Contexto

| Fonte | Trecho | Conf. |
|-------|--------|-------|
| `.claude/skills/calendario-provas/SKILL.md` | Fonte viva | 🟢 |
| `_reversa_sdd/adrs/004-skill-fonte-viva-regras.md` | Hierarquia de fontes | 🟢 |
| `_reversa_sdd/adrs/006-segmento-regras-configuraveis-ia.md` | Toggles + IA | 🟢 |
| `.reversa/context/sync-regras.md` | Sync skill ↔ Reversa | 🟢 |
| `exportar_regras_pdf.py` | PDF resumo | 🟢 |

## 3. Personas

| Persona | Objetivo | Cenário |
|---------|----------|---------|
| Coordenador | Consultar regras vigentes | Lê skill/PDF ou UI catálogo |
| Admin instituição | Manter catálogo template | Publica regras no BD |
| Coordenador | Ativar/desativar regra codificada | Toggle no menu semestre |
| Coordenador | Registrar exceção contextual | Customização IA (texto) |
| Dev/IA | Sincronizar skill após PR | Fluxo sync-regras.md |

## 4. Regras de negócio

1. **RN-01:** SKILL.md em **GitHub `main`** é fonte de verdade para regras de domínio 🟢 (ver ADR-004, addenda github-fonte-verdade-2026-08-12)
2. **RN-02:** PDF é snapshot; não substitui skill 🟢
3. **RN-03:** Regra codificada = implementada no solver; toggle on/off 🟢
4. **RN-04:** Regra só na skill sem código = lacuna documentada (ex. PR #14) 🔴
5. **RN-05:** Customização IA não altera código; interpretada na camada assistida 🟢
6. **RN-06:** Sync Reversa: hashes em `sources.json` detectam drift 🟢
7. **RN-07:** Grupo 1 (Mat/DaF/Port/Ing) ≠ entidade GRUPO customizável 🟢

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério | Conf. |
|----|-----------|------------|----------|-------|
| RF-01 | Catálogo de regras com código, descrição, skill_ref | Must | Lista ≥30 regras mapeadas | 🟢 |
| RF-02 | Flag `implementada_solver` por regra | Must | LP/LIT/RED 10d = false hoje | 🟢 |
| RF-03 | Toggle `ativo` por segmento/semestre | Must | Desligar regra 3 impede relaxamento | 🟢 |
| RF-04 | Params JSON opcionais por regra (ex. tetos) | Should | Override sem redeploy | 🟡 |
| RF-05 | CRUD customização IA (texto + metadados) | Should | Persiste por segmento | 🟢 |
| RF-06 | Export PDF a partir do catálogo/skill | Should | Paridade exportar_regras_pdf | 🟢 |
| RF-07 | Sync skill → catálogo BD (job/CLI) | Should | Novas regras skill viram entrada catálogo | 🟡 |
| RF-08 | Montar `RuleContext` para solver | Must | Só regras ativas + params | 🟡 |

## 6. RNFs

| Tipo | Requisito | Evidência | Conf. |
|------|-----------|-----------|-------|
| Rastreabilidade | skill_ref em cada regra catálogo | ADR-004 | 🟢 |
| Versionamento | Git para skill; semver catálogo BD | sync-regras | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Toggle desativa regra codificada
  Dado regra "max_3_avaliacoes_semana" ativa no catálogo
  Quando coordenador desativa toggle no semestre 2026-2
  Então RuleContext enviado ao solver não inclui essa restrição

Cenário: Lacuna PR #14 documentada
  Dado regra "lp_lit_red_10_dias_conselho" no catálogo
  Quando consulto implementada_solver
  Então valor false e link skill_ref PR #14

Cenário: Customização IA registrada
  Dado coordenador registra "preferir provas Geo às sextas"
  Quando gera calendário com camada IA
  Então preferência aparece no relatório auxiliar (não no solver determinístico)
```

## 8. MoSCoW

| Item | MoSCoW |
|------|--------|
| RF-01, RF-02, RF-03, RF-08 | Must |
| RF-05, RF-06 | Should |
| RF-07 | Should |
| RF-04 | Could |

## 10. Lacunas

- 🟢 PR #14/#18: skill + código implementados
- 🟢 Customização IA: verificador + relatório auxiliar (Brener 2026-08-09)
- 🟢 Admin: Brener admin_instituicao; coords isolados

## 11. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial Fase 4 | reversa-writer |
