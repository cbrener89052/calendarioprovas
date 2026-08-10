---
schemaVersion: 1
generatedAt: 2026-08-10T02:10:00Z
reversa:
  version: "1.2.58"
kind: data_migration_plan
producedBy: designer
---

# Data Migration Plan

> Legado: arquivos locais + constantes Python  
> Alvo: PostgreSQL + blob storage

## Escopo

| Dado | Migrar? | Estratégia |
|------|---------|------------|
| Grade-base xlsx | Sim | Upload manual ou script import |
| Modelo calendário | Sim | Upload por semestre |
| Siglas professores | Sim | Upload ou seed CSV |
| Simulados | Sim | Params GRUPO + arquivo |
| Constantes feriados | Sim | regra_config.params ou seed |
| Histórico semestres anteriores | Opcional v2 | Fora escopo v1 |
| Catálogo regras | Sim | Seed from skill + sync job |

## Fase 1 — Seed estrutural

1. Criar `instituicao` (Escola Alemã Corcovado)
2. Criar Brener (`admin_instituicao`) + 5 coordenadores
3. Criar 5 segmentos 1:1
4. Seed `regra_catalogo` (~30 regras mapeadas em code-spec-matrix)
5. Criar GRUPOs default por segmento (espelhar `10_12`, `9_11` legado)

**Script sugerido**: `scripts/seed_catalogo_regras.py` (lê skill hashes)

## Fase 2 — Import entradas semestre ativo

| Passo | Ação |
|-------|------|
| 1 | Identificar arquivos legado em `legacy/data/` ou cwd |
| 2 | Upload para blob com path `{segmento}/{semestre}/{tipo}/{filename}` |
| 3 | Inserir `arquivo_entrada` com checksum sha256 |
| 4 | Validar integridade (re-download + compare) |

## Fase 3 — Params solver

| Constante legado | Destino alvo |
|------------------|--------------|
| GRUPO datas | tabela `grupo` |
| Feriados | `regra_config.params` ou tabela feriados |
| SEED_PROPOSTA_3 | env worker ou regra_config |
| LIMITE_LPLITRED_CONSELHO | regra_config (implementada_solver=true pós PR #18) |
| folga_extra por turma | params GRUPO/turma jsonb |

## Fase 4 — Validação

- Parallel Run: mesmas entradas → diff xlsx
- Verificador plataforma == verificador CLI
- Checksum blobs antes/after

## Rollback dados

- Snapshots PostgreSQL pré-cutover
- Blobs versionados (não sobrescrever sem version suffix)
- CLI legado continua lendo arquivos locais originais

## Não migrar (v1)

- `analise-historica` datasets
- Logs stdout históricos
- Scripts utilitários (`limpar_grade`, `contar`)

## Cronograma lógico

```
Seed BD → Import blobs semestre piloto → Config GRUPOS → Parallel Run → Cutover
```

## Owner

- Seed catálogo: Brener + dev
- Import blobs: coordenador por segmento
- Validação: dev (automação parity_tests)
