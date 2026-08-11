# Plataforma web (monorepo)

Estrutura alvo da migração Reversa — ver `_reversa_sdd/migration/handoff.md`.

```
apps/
  api/      FastAPI — auth, CRUD, jobs
  worker/   Pipeline solver + verificador
  web/      React Vite + Tailwind
packages/
  solver/   Lógica Proposta 3 (T5)
  ingest/   Extração grade + check-in (T3c–T3d, ADR-008)
infra/
  docker-compose.yml
legacy/     Referência CLI durante Strangler
```

## Desenvolvimento local

```bash
# Validar compose
docker compose -f infra/docker-compose.yml config

# Subir stack
docker compose -f infra/docker-compose.yml up --build

# Migrations (PostgreSQL rodando)
cd apps/api && ./scripts/migrate.sh upgrade head

# Seed catálogo de regras (após migrate)
python3 scripts/seed_catalogo_regras.py

# Dev: semestre + turmas para testar upload/ingest (T4)
cd apps/api && python3 scripts/seed_dev_semestre.py

# API: http://localhost:8000/health
# Web: http://localhost:8080
```

## CLI legado

Scripts na raiz (`gerar_calendario.py`, etc.) permanecem até paridade confirmada.
