# Plataforma Multi-Coordenador — Design Técnico

## Containers (C4)

```
Browser → Frontend React (Vite) + Tailwind + Lucide 🟢
              ↓ HTTPS
         FastAPI (API)
         ├── Auth (JWT)
         ├── CRUD Segmento/GRUPO/Semestre
         ├── Upload → Blob Store
         └── Jobs → Queue/DB
              ↓
         Worker (Python)
         ├── extracao-grade (opcional)
         ├── gerar_calendario (RuleContext)
         ├── verificar_calendario
         └── exportadores
              ↓
         PostgreSQL + Blob (S3/local)
```

## Interface API (resumo)

Ver `contracts.md` para OpenAPI detalhado.

| Área | Endpoints principais |
|------|---------------------|
| Auth | POST `/auth/login`, POST `/auth/logout` |
| Segmento | GET/PATCH `/segmento/me` |
| GRUPOS | CRUD `/segmento/grupos` |
| Semestres | CRUD `/semestres` |
| Entradas | POST `/semestres/{id}/upload/{tipo}` |
| Geração | POST `/semestres/{id}/gerar`, GET `/jobs/{id}` |
| Regras | GET/PATCH `/semestres/{id}/regras` |
| IA | CRUD `/segmento/customizacoes-ia` |
| Saídas | GET `/calendarios/{id}/download`, `/relatorios/*` |

## Modelo GRUPO 🟢

| Campo | Tipo | Uso no solver |
|-------|------|---------------|
| nome | string | UI |
| data_inicio_semestre | date | Janela provas |
| data_fim_semestre | date | Janela provas |
| datas_segunda_chamada | date[] | Restrições 2CH |
| conselho_inicio | date | Semana vetada início |
| conselho_fim | date | Semana vetada fim |

Substitui hardcode `10_12` / `9_11` legado.

## Fluxo Principal

1. Login → JWT com `coordenador_id`, `segmento_id` 🟢
2. Configurar GRUPOS e turmas 🟢
3. Criar semestre; upload entradas → blob + `arquivo_entrada` 🟢
4. Configurar toggles regras + customizações IA 🟢
5. POST gerar → job worker 🟢
6. Worker: monta RuleContext → `montar_proposta` → xlsx 🟢
7. Verificador automático 🟡
8. Persistir `calendario_gerado` + blobs relatórios 🟢
9. Coordenador publica ou baixa 🟡

## Dependências

- PostgreSQL, FastAPI, openpyxl, solver legado
- regras-negocio (RuleContext)
- Blob storage (S3 ou local path)

## Deploy híbrido 🟢

**Nuvem:** API managed + Neon Postgres + S3  
**On-prem:** `docker-compose.yml` — api, postgres, worker, **frontend** (Vite build), volume blobs

## Frontend (ADR-007) 🟢

| Item | Escolha |
|------|---------|
| Build | Vite + React + TypeScript |
| UI | Tailwind CSS |
| Ícones | lucide-react |
| Estado | Context ou Redux — stores: `regras` (toggles), `solverJob`, `segmento` |
| API | Client OpenAPI/fetch → FastAPI |

Telas MVP: login, segmento/GRUPOS, upload entradas, toggles regras, customizações IA, gerar (progress), verificação, downloads.

## Decisões

| Decisão | ADR | Conf. |
|---------|-----|-------|
| FastAPI + Postgres | 005 | 🟢 |
| Segmento + toggles + IA | 006 | 🟢 |
| React Vite + Tailwind | 007 | 🟢 |
| Brener = admin_instituicao | permissions 2026-08-09 | 🟢 |
| Manter Python solver | user-requirements | 🟢 |

## Riscos

- 🟡 Refactor constantes hardcoded — blocker para multi-segmento
- 🟡 Escolha Context vs Redux — decidir na implementação T-13
- 🟡 Context vs Redux (decisão implementação)
