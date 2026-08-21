# Regras de Negócio — Design Técnico

## Arquitetura dois trilhos (ADR-006)

```
SKILL.md ──sync──► REGRA_CATALOGO (institucional)
                         │
                         ▼
              REGRA_CONFIG (toggle + params)
                         │
                         ▼
                   RuleContext ──► Solver (geracao-calendario)

CUSTOMIZACAO_IA (texto) ──► Camada IA ──► Relatório / pós-processamento
```

## Interface — Catálogo (legado + futuro)

| Componente | Legado | Plataforma |
|------------|--------|------------|
| Fonte viva | `.claude/skills/calendario-provas/SKILL.md` | Sync job |
| Snapshot | `exportar_regras_pdf.py` → PDF | GET `/regras/pdf` |
| Sync Reversa | `.reversa/context/sources.json` | Webhook/manual |

## Entidades (ERD)

- **REGRA_CATALOGO:** codigo, descricao, implementada_solver, skill_ref
- **REGRA_CONFIG:** segmento_id, semestre_id, regra_id, ativo, params (jsonb)
- **CUSTOMIZACAO_IA:** segmento_id, texto, created_at

## RuleContext (contrato solver) 🟡

```python
@dataclass
class RuleContext:
    regras_ativas: set[str]  # códigos catálogo
    params: dict[str, dict]  # overrides por código
    grupos: list[GrupoConfig]  # datas semestre, conselho, 2CH
    customizacoes_ia: list[str]  # textos para camada IA
```

## Fluxo sync skill → Reversa

1. Ler hashes em `sources.json` 🟢
2. Fetch skill/código GitHub 🟢
3. Diff → adendo `_reversa_sdd/addenda/` se mudou 🟢
4. Atualizar catálogo BD (futuro) 🟡

## Regras mapeadas (amostra)

| Código | Solver | Toggle default |
|--------|--------|----------------|
| max_3_avaliacoes_semana | ✅ | on |
| cessao_regra_4_pos_prova | ✅ | on |
| lp_lit_red_10_dias_conselho | 🔴 | on (quando impl.) |
| grupo_1_semana_unica | ✅ | on |

## Dependências

- SKILL.md, sync-regras.md, gerar_calendario (implementação)
- plataforma-multi-coordenador (persistência)

## Riscos

- 🔴 Divergência skill/código sem sync regular
- 🟡 IA não determinística — não substituir toggles críticos
- 🟡 Params JSON sem schema — validar com JSON Schema
