---
schemaVersion: 1
generatedAt: 2026-08-10T02:10:00Z
reversa:
  version: "1.2.58"
kind: target_data_model
producedBy: designer
---

# Target Data Model

> PostgreSQL 16 — schema `calendario`  
> Diagrama completo: `_reversa_sdd/erd-complete.md`

## Tabelas principais

### instituicao
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| nome | varchar | Escola Alemã Corcovado |

### coordenador
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| instituicao_id | uuid FK | |
| email | varchar UK | |
| nome | varchar | |
| papel | enum | admin_instituicao, coordenador |
| senha_hash | varchar | bcrypt |

### segmento
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| coordenador_id | uuid FK UK | 1:1 |
| nome | varchar | |

### grupo
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| segmento_id | uuid FK | |
| nome | varchar | ex. "10/12" |
| data_inicio_semestre | date | |
| data_fim_semestre | date | |
| datas_segunda_chamada | jsonb | date[] |
| conselho_inicio | date | |
| conselho_fim | date | |

### turma
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| grupo_id | uuid FK | |
| codigo | varchar UK | 10C1, 11C2… |

### semestre
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| segmento_id | uuid FK | |
| ano | int | |
| periodo | int | 1 ou 2 |
| inicio | date | |
| fim | date | |

### regra_catalogo
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| codigo | varchar UK | max_3_avaliacoes_semana |
| descricao | text | |
| implementada_solver | bool | |
| skill_ref | varchar | link seção skill |

### regra_config
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| segmento_id | uuid FK | |
| semestre_id | uuid FK | |
| regra_id | uuid FK | |
| ativo | bool | toggle |
| params | jsonb | overrides |

### customizacao_ia
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| segmento_id | uuid FK | |
| semestre_id | uuid FK | |
| instrucao | text | |
| contexto | text | |
| created_at | timestamptz | |

### arquivo_entrada
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| semestre_id | uuid FK | |
| tipo | enum | grade, modelo, siglas, simulados |
| blob_path | varchar | |
| checksum | varchar | sha256 |
| uploaded_at | timestamptz | |

### job
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| semestre_id | uuid FK | |
| status | enum | queued, running, completed, failed |
| payload | jsonb | RuleContext snapshot |
| started_at | timestamptz | |
| finished_at | timestamptz | |
| error | text | |

### calendario_gerado
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| semestre_id | uuid FK | |
| job_id | uuid FK | |
| status | enum | verified, published, failed |
| xlsx_blob_path | varchar | |
| verificacao_result | jsonb | |
| publicado_em | timestamptz | |

### relatorio
| Coluna | Tipo | Notas |
|--------|------|-------|
| id | uuid PK | |
| calendario_id | uuid FK | |
| tipo | enum | trocas, cessoes, tabela, auxiliar_ia |
| blob_path | varchar | |

## Índices

- `segmento_id` em todas tabelas tenant-scoped
- `(semestre_id, tipo)` unique em arquivo_entrada
- `job(status, created_at)` para worker poll

## Migração desde legado

| Legado | Alvo |
|--------|------|
| Arquivos cwd | arquivo_entrada + blob |
| Constantes inline | grupo + regra_config.params |
| stdout logs | job.error + verificacao_result |

## RLS (recomendado)

Row Level Security por `segmento_id` derivado do JWT — ver `permissions.md`.
