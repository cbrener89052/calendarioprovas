# ADR-007 — Frontend web React (Vite) + Tailwind

**Status:** Aceito  
**Data:** 2026-08-09  
**Confiança:** 🟢 (declarado por Brener)

## Contexto

Plataforma multi-coordenador exige interface web na v1 (não API-only). Stack backend já definida (FastAPI + PostgreSQL).

## Decisão

| Camada | Escolha |
|--------|---------|
| Framework | **React** com **Vite** |
| Estilo | **Tailwind CSS** |
| Ícones | **Lucide React** |
| Estado global | **React Context** ou **Redux** — regras ativas/toggles e status do job solver |

Frontend consome OpenAPI FastAPI; deploy no Docker Compose junto com API (serviço `web`).

## Alternativas rejeitadas

| Opção | Motivo |
|-------|--------|
| API-only MVP | Brener exige web na v1 |
| Next.js | Preferência explícita por Vite + React SPA |

## Consequências

- `plataforma-multi-coordenador/tasks.md`: T-13 desbloqueado
- Docker Compose: serviço `frontend` (build Vite → nginx ou vite preview prod)
- Redux/Context: stores para `regras`, `jobStatus`, `segmento`
