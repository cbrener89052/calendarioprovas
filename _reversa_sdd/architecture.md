# Arquitetura — calendarioprovas

> Gerado pelo Arquiteto (Reversa), doc_level=completo.

---

## Visão geral

Sistema **batch/CLI** para coordenação escolar: lê horário-base + modelo xlsx, resolve alocação combinatória de provas, grava planilhas e relatórios. **Sem runtime persistente** no legado.

Evolução planejada: **API FastAPI + PostgreSQL + blob storage**, 5 coordenadores.

---

## Legado (as-is)

```
┌─────────────────────────────────────────────────────────┐
│  Coordenador (Windows)                                   │
│  Claude Code / Cursor / terminal                         │
└────────────┬────────────────────────────────────────────┘
             │ CLI
             ▼
┌─────────────────────────────────────────────────────────┐
│  Scripts Python                                          │
│  gerar → verificar → exportar                           │
└────────────┬────────────────────────────────────────────┘
             │ read/write
             ▼
┌─────────────────────────────────────────────────────────┐
│  Arquivos locais + Git                                   │
│  xlsx, pdf, md, skill, Horario desenvolvido/            │
└─────────────────────────────────────────────────────────┘
```

---

## Futuro (to-be) — resumo

```
Browser → Frontend → FastAPI → PostgreSQL
                          ↘ Blob (S3/local)
                          ↘ Worker (solver Python)
```

Detalhes: `c4-*.md`, `erd-complete.md`, ADR-005.

---

## Componentes lógicos (features)

| Feature | Responsabilidade | Script principal |
|---|---|---|
| geracao-calendario | Solver + escrita xlsx | `gerar_calendario.py` |
| verificacao-calendario | Checklist pós-geração | `verificar_calendario.py` |
| exportacao-relatorios | Derivados Excel | `exportar_*.py` |
| extracao-grade | PDF → grade Python | `extrair_grade_*.py` |
| analise-historica | Benchmark semestres | `analisar_*.py` |
| regras-negocio | Documentação | SKILL.md |

Organização specs: **feature-folder** (`_reversa_sdd/<feature>/` na fase Redator).

---

## Integrações externas

| Sistema | Tipo | Uso |
|---|---|---|
| Excel (.xlsx) | Arquivo | Entrada/saída principal |
| PDF Untis | Arquivo | Horário-base |
| Tesseract OCR | CLI | Grade 2025 sem texto |
| GitHub | Git | **Fonte da verdade** — skill, código, specs (`main` / `producao`) |
| PostgreSQL | 🔴 futuro | Metadados multi-coord |
| S3 / filesystem | 🔴 futuro | Blobs |

---

## Dívidas técnicas

| Item | Severidade |
|---|---|
| Constantes hardcoded (grades, simulados, feriados) | Alta |
| Sem `requirements.txt` | Média |
| Sem testes automatizados | Alta |
| Acoplamento verificador ↔ gerador (`import gerar_calendario`) | Média |
| Skill à frente do código (PR #14) | Média |
| Cores: verificador não valida ARGB | Baixa |

---

## Referências

- `_reversa_sdd/domain.md`
- `_reversa_sdd/c4-context.md`
- `_reversa_sdd/erd-complete.md`
- `_reversa_sdd/traceability/spec-impact-matrix.md`
