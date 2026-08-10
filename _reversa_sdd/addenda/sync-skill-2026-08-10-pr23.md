# Sync Reversa — PR #23 (2026-08-10)

> Merge base `claude/skill-calendar-install-b2oqrs` @ 5f1e3f4 into `cursor/reversa-reconstruct-b8d6`

## Commits incorporados (outra IA)

| SHA | Conteúdo |
|-----|----------|
| 9082179 | Mat/Fis 10C; Química/Física/Bio 9C semanas 12–14; Soc 12C; skill escada 7→4 sem |
| 5f1e3f4 | `LIMITE_LPLITRED_CONSELHO` por grupo via marcação CC (gerador + verificador) |

## Alterações de código

| Arquivo | Mudança |
|---------|---------|
| `gerar_calendario.py` | `LIMITE_LPLITRED_CONSELHO_BASE` + dict por grupo; `carregar_ocupadas()` lê CC |
| `verificar_calendario.py` | Mesma lógica LP/LIT/RED por grupo |
| `SKILL.md` | Escada distância 7→4; regra 9C sem 12–14; CC 10,12 vs conselho meio |
| `referencia/estado_2sem_2026.md` | Ajustes manuais Proposta 3 |
| xlsx Proposta 3 | Regenerados |

## Impacto plataforma / Reversa

- **GRUPO** futuro: `conselho_inicio/fim` + marcações CC no modelo → params solver
- **Seed catálogo**: novas regras `distancia_escada_7_4`, `quimica_fis_bio_9c_semanas_12_14`, `lp_lit_red_por_grupo_cc`
- G-M03 ARGB: inalterado

## Hashes

Ver `.reversa/context/sources.json` — `last_sync_pr`: 23.
