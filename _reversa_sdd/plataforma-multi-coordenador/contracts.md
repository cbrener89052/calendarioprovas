# Contratos — Plataforma Multi-Coordenador

> OpenAPI resumido. Especificação completa: `_reversa_sdd/openapi/calendarioprovas.yaml`

## Autenticação

- **Tipo:** Bearer JWT
- **Header:** `Authorization: Bearer <token>`
- **Claims:** `sub` (coordenador_id), `segmento_id`

## Endpoints

### Auth

| Método | Path | Body | Response |
|--------|------|------|----------|
| POST | `/api/v1/auth/login` | `{ email, password }` | `200 { access_token, token_type }` |
| POST | `/api/v1/auth/logout` | — | `204` |

### Segmento

| Método | Path | Response |
|--------|------|----------|
| GET | `/api/v1/segmento/me` | `Segmento` |
| PATCH | `/api/v1/segmento/me` | `Segmento` |

### GRUPOS

| Método | Path | Body | Response |
|--------|------|------|----------|
| GET | `/api/v1/grupos` | — | `Grupo[]` |
| POST | `/api/v1/grupos` | `GrupoCreate` | `201 Grupo` |
| GET | `/api/v1/grupos/{id}` | — | `Grupo` |
| PATCH | `/api/v1/grupos/{id}` | `GrupoUpdate` | `Grupo` |
| DELETE | `/api/v1/grupos/{id}` | — | `204` |

**GrupoCreate:**
```json
{
  "nome": "Turmas que viajam cedo",
  "data_inicio_semestre": "2026-08-04",
  "data_fim_semestre": "2026-11-28",
  "datas_segunda_chamada": ["2026-11-10"],
  "conselho_inicio": "2026-11-24",
  "conselho_fim": "2026-11-28"
}
```

### Semestres

| Método | Path | Response |
|--------|------|----------|
| GET | `/api/v1/semestres` | `Semestre[]` |
| POST | `/api/v1/semestres` | `201 Semestre` |
| GET | `/api/v1/semestres/{id}` | `Semestre` |

### Upload entradas

| Método | Path | Content-Type | Response |
|--------|------|--------------|----------|
| POST | `/api/v1/semestres/{id}/upload/grade` | multipart | `{ arquivo_id }` |
| POST | `/api/v1/semestres/{id}/upload/modelo` | multipart | `{ arquivo_id }` |
| POST | `/api/v1/semestres/{id}/upload/siglas` | multipart | `{ arquivo_id }` |

### Geração

| Método | Path | Body | Response |
|--------|------|------|----------|
| POST | `/api/v1/semestres/{id}/gerar` | `{ proposta: 3, seed?: 7 }` | `202 { job_id }` |
| GET | `/api/v1/jobs/{job_id}` | — | `JobStatus` |

**JobStatus:**
```json
{
  "id": "uuid",
  "status": "pending|running|completed|failed",
  "calendario_id": "uuid|null",
  "erros": ["string"]|null
}
```

### Regras (toggles)

| Método | Path | Body | Response |
|--------|------|------|----------|
| GET | `/api/v1/semestres/{id}/regras` | — | `RegraConfig[]` |
| PATCH | `/api/v1/semestres/{id}/regras/{codigo}` | `{ ativo, params? }` | `RegraConfig` |

### Customizações IA

| Método | Path | Response |
|--------|------|----------|
| GET | `/api/v1/customizacoes-ia` | `CustomizacaoIA[]` |
| POST | `/api/v1/customizacoes-ia` | `201 CustomizacaoIA` |
| DELETE | `/api/v1/customizacoes-ia/{id}` | `204` |

### Saídas

| Método | Path | Response |
|--------|------|----------|
| GET | `/api/v1/calendarios/{id}/download` | xlsx stream |
| GET | `/api/v1/calendarios/{id}/relatorios/tabela-resumo` | xlsx |
| GET | `/api/v1/calendarios/{id}/relatorios/tempos-cedidos` | xlsx |
| POST | `/api/v1/calendarios/{id}/verificar` | `{ ok, problemas[] }` |
| POST | `/api/v1/calendarios/{id}/publicar` | `{ publicado_at }` |

### Histórico de calendários (ADR-009)

| Método | Path | Response |
|--------|------|----------|
| GET | `/api/v1/calendarios/consulta` | `PeriodoCalendariosConsulta[]` — períodos do segmento + resumo versões |
| GET | `/api/v1/semestres/{id}/calendarios` | `CalendarioVersao[]` (exclui `deleted_at` preenchido) |
| GET | `/api/v1/calendarios/{id}` | `CalendarioVersao` + metadados verificação |
| DELETE | `/api/v1/calendarios/{id}` | `204` — soft-delete + purge blob (confirmação no body `{ confirm: true }`) |
| POST | `/api/v1/calendarios/{id}/restaurar-referencia` | `{ referencia_ativa: true }` |

**Query params `GET /calendarios/consulta`:** `ano` (int), `periodo` (1|2), `ordenar` (`desc`|`asc`), `limit` (default 20)

**PeriodoCalendariosConsulta:**
```json
{
  "semestre": {
    "id": "uuid",
    "ano": 2026,
    "periodo": 2,
    "inicio": "2026-08-04",
    "fim": "2026-11-28"
  },
  "total_versoes": 3,
  "referencia_ativa": {
    "id": "uuid",
    "versao": 3,
    "rotulo": "Proposta 3 — 11/08/2026",
    "gerado_em": "2026-08-11T09:15:00Z"
  },
  "ultima_geracao_em": "2026-08-11T09:15:00Z"
}
```

**CalendarioVersao:**
```json
{
  "id": "uuid",
  "semestre_id": "uuid",
  "job_id": "uuid",
  "versao": 3,
  "rotulo": "Proposta 3 — 11/08/2026 09:15",
  "status": "verified|published|failed",
  "referencia_ativa": true,
  "gerado_em": "2026-08-11T09:15:00Z",
  "publicado_em": null,
  "verificacao_ok": true
}
```

## Códigos de erro

| Status | Uso |
|--------|-----|
| 400 | Validação body |
| 401 | Não autenticado |
| 403 | Fora do segmento |
| 404 | Recurso inexistente |
| 422 | Verificação calendário falhou |
| 500 | Erro worker |

## Confiança

🟡 — Contrato inferido de user-requirements + ADRs; não há API implementada ainda.
