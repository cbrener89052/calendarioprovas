# ADR-005 — Evolução para FastAPI + PostgreSQL multi-coordenador

**Status:** Proposto  
**Data:** 2026-08-09  
**Confiança:** 🟡

## Contexto

5 coordenadores precisarão de persistência, login e isolamento — hoje tudo é pasta local + git.

## Decisão (preliminar)

- Backend: FastAPI reutilizando núcleo de `gerar_calendario.py`
- PostgreSQL: metadados, versionamento
- Blob storage: xlsx/pdf de entrada e saída
- Deploy híbrido: nuvem + Docker Compose on-prem

## Alternativas consideradas

| Opção | Prós | Contras |
|---|---|---|
| Reescrita total | Clean slate | Perde solver validado |
| Manter CLI + sync git | Zero infra | Não escala multi-user |
| **Evoluir Python + API** | Reaproveita lógica | Migração gradual |

## Consequências

- ERD dual: legado (arquivos) + plataforma (BD)
- Spec Impact Matrix mapeia migração por feature
- Frontend a definir (provável web app)
