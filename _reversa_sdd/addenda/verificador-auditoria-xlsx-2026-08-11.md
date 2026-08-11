# Addenda — Verificador como auditoria xlsx (2026-08-11)

> Esclarecimento de Brener via `/reversa` sobre o papel de `verificar_calendario.py`

## Princípio

O verificador **não confia na memória do gerador**. É auditoria do artefato **já gravado**:

- Arquivo: `Horario desenvolvido/Proposta_3_Calendario_Provas_2026_2SEM.xlsx`
- Método: relê **célula por célula** (colunas E–I, semanas 1–20)
- Escopo: **8 turmas** (8 abas)

## Saída

| Grupo | Severidade API | Bloqueia entrega |
|-------|----------------|------------------|
| PROBLEMA | `erro` | Sim |
| AVISO | `aviso` | Não (relaxamento documentado) |

## Artefatos atualizados

- ADR-010
- `verificacao-calendario/requirements.md`, `design.md`
- `.reversa/context/user-requirements.md` (seção verificação)

## Impacto reconstrução

- **T5/T6:** `packages/verifier` ou submódulo; worker chama verificador **após** write xlsx
- **T10/SCR-08:** UI separa erros críticos de avisos relaxados
- **Parity tests:** comparar listas PROBLEMA/AVISO CLI vs plataforma
