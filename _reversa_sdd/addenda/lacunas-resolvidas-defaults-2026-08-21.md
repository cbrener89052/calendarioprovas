# Addenda — Resolução de lacunas (defaults)

> Registrado em 2026-08-21 após Brener responder `continuar` sem opções explícitas.  
> Decisões 🟡 **INFERIDAS** — alinhadas à skill e a `user-requirements.md`. Corrigível a qualquer momento.

## Vigência

- **Superado** pela re-extração de 2026-08-28 (ADR-015 confirmado Brener).
- Histórico apenas — não usar defaults deste adendo.

## Decisões (obsoletas)

| ID | Decisão default | Forward |
|----|-----------------|---------|
| L-01 | R-2CH **Must** no solver + verificador | `geracao-calendario` T-12, `verificacao-calendario` |
| L-02 | ENEM + véspera 2CH **Must**; véspera 9 flexível primeiro | UI datas ENEM + constraints |
| L-03 | Plataforma upload PDF Must; legado `GRADE_TXT` até parser 2sem | `extracao-grade` T-parser-2sem |
| L-04 | Auth e-mail/senha + JWT; RLS por coordenador | `plataforma` T-02 |
| L-05 | `fpdf` Could legado; plataforma HTML regras v1, PDF v1.1 | `exportacao-relatorios` |

## Specs atualizadas

- `_reversa_sdd/questions.md`
- `_reversa_sdd/gaps.md`
- `_reversa_sdd/confidence-report.md`
- `_reversa_sdd/adrs/014-decisoes-lacunas-revisao.md`
- Units: `regras-negocio`, `geracao-calendario`, `extracao-grade`, `plataforma-multi-coordenador`, `exportacao-relatorios`
- `.reversa/context/user-requirements.md` (seção lacunas críticas)

## Reclassificação

Lacunas L-01–L-05: 🔴 → 🟡 (decisão registrada; implementação pendente no forward).
