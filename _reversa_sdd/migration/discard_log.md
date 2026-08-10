---
schemaVersion: 1
generatedAt: 2026-08-10T02:00:00Z
reversa:
  version: "1.2.58"
kind: discard_log
producedBy: curator
---

# Discard Log

> Regras e comportamentos do legado descartados na migração, com justificativa e rastreabilidade.

## Resumo

- Total descartados: 6
- Vinculados a paradigma: 5
- Por escopo excluído: 1

## BR-DESCARTAR-001 — Saída CLI stdout

- **Origem**: `architecture.md` — execução batch via terminal
- **Descrição**: Coordenador executa scripts Python manualmente; progresso via print.
- **Motivo**: Artefato procedural; plataforma usa API REST + polling de jobs.
- **Vinculado a paradigma**: sim
- **Substituído por**: POST `/semestres/{id}/gerar`, GET `/jobs/{id}`

## BR-DESCARTAR-002 — Scripts `.bat` git sync

- **Origem**: `inventory.md`, gaps G-K02
- **Descrição**: `git-sync.bat`, `commit.bat` para workflow Windows local.
- **Motivo**: Escopo excluído no brief; CI/CD substitui.
- **Vinculado a paradigma**: sim

## BR-DESCARTAR-003 — Módulo análise histórica

- **Origem**: `analise-historica/requirements.md`
- **Descrição**: Comparação entre semestres anteriores.
- **Motivo**: Brief exclui v1 ("analise-historica v2").
- **Vinculado a paradigma**: não

## BR-DESCARTAR-004 — Arquivos locais no cwd

- **Origem**: `gerar_calendario.py`, `data-dictionary.md`
- **Descrição**: Grade, modelo, siglas e saídas em pastas fixas do repositório.
- **Motivo**: Multi-tenant exige blob storage + metadados PostgreSQL.
- **Vinculado a paradigma**: sim
- **Substituído por**: `ARQUIVO_ENTRADA`, S3/volume local

## BR-DESCARTAR-005 — Hardcode grupos de viagem

- **Origem**: `gerar_calendario.py` constantes `10_12`, `9_11`
- **Descrição**: Períodos de semestre e conselho embutidos no código.
- **Motivo**: ADR-006 — entidade GRUPO configurável absorve a regra de negócio.
- **Vinculado a paradigma**: sim (localização da config mudou, regra permanece como BR-MIGRAR-004)

## BR-DESCARTAR-006 — Fluxo operacional manual único-usuário

- **Origem**: `user-requirements.md` legado
- **Descrição**: Um coordenador local executa pipeline completo na máquina.
- **Motivo**: 5 coordenadores isolados + admin requer plataforma web.
- **Vinculado a paradigma**: sim

## Utilitários não descartados (referência)

| Script | Decisão | Nota |
|--------|---------|------|
| `limpar_grade_2025.py` | Não migrar v1 | G-K01; opcional |
| `contar_2sem_2025.py` | Não migrar v1 | G-K01; opcional |
| `exportar_regras_pdf.py` | Absorvido | RF-06 catálogo BD |
