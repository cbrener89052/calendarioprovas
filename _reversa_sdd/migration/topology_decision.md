# Topology Decision — calendarioprovas

> Produzido por: Designer (Fase 1) | 2026-08-10  
> **Decisão:** modernizar (aprovada implicitamente via ADR-007 + respostas Brener)

## Opções consideradas

| Opção | Descrição | Veredito |
|-------|-----------|----------|
| Preservar | Mesma árvore de scripts Python | Rejeitada — não escala multi-coord |
| **Modernizar** | Monorepo API + worker + web | **Escolhida** |
| Híbrido legado | CLI + API sidecar | Rejeitada — duplicação de manutenção |

## Árvore alvo (esboço)

```
calendarioprovas/
├── apps/
│   ├── api/                 # FastAPI — auth, CRUD, jobs, uploads
│   ├── worker/              # Job solver + verificador + exportadores
│   └── web/                 # React Vite + Tailwind
├── packages/
│   └── solver/              # gerar_calendario + verificar + export (refatorado)
├── infra/
│   └── docker-compose.yml   # api, worker, postgres, web, minio
└── legacy/                  # scripts CLI originais (referência/paridade)
```

## Fronteiras de módulo

| Módulo | Responsabilidade | Comunicação |
|--------|------------------|-------------|
| api | HTTP, auth, tenant | → postgres, blob, fila jobs |
| worker | Solver pipeline | ← jobs, → blob, postgres |
| web | UI coordenador/admin | → api REST |
| solver | Lógica combinatória pura | chamada in-process pelo worker |

## Honra à topologia

- Nenhum script `.py` na raiz em produção — apenas `legacy/` ou removidos após paridade
- OpenAPI em `apps/api` é contrato web ↔ api
