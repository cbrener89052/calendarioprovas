# Adendo — sincronização skill calendario-provas

**Data:** 2026-08-09  
**Cenário:** legado  
**Fonte:** `.claude/skills/calendario-provas/SKILL.md` (655 linhas)

## Vigência

Vigente desde 2026-08-09.

## Resumo

Re-sincronização pedida pelo usuário após atualização da skill no Claude Code. Artefatos `_reversa_sdd/code-analysis.md` e `modules.json` atualizados para refletir regras refinadas já presentes na skill e no código.

## Impacto por artefato da extração

| Artefato | Seção | Tipo | Delta |
|---|---|---|---|
| `_reversa_sdd/code-analysis.md` | geracao-calendario | regra-alterada | Regra 4 refinada: afrouxamento só libera cessão **depois** da prova, nunca antes/no dia |
| `_reversa_sdd/code-analysis.md` | geracao-calendario | regra-nova | `FORCAR_DATA` protegida **antes** de `resolver_par`; datas fixas inegociáveis |
| `_reversa_sdd/code-analysis.md` | geracao-calendario | regra-alterada | Escada de afrouxamento: regra4 → regra3 → tetos (por turma, não global) |
| `_reversa_sdd/code-analysis.md` | geracao-calendario | componente-novo | `detectar_regras_relaxadas()` + seção "Regras relaxadas" no relatório MD |
| `_reversa_sdd/code-analysis.md` | verificacao-calendario | regra-alterada | Checklist expandido (cores FF, amarelo simulados, mesclagem, regra 4 relaxada) |
| `_reversa_sdd/code-analysis.md` | regras-negocio | regra-alterada | Skill é fonte viva; PDF (`exportar_regras_pdf.py`) é resumo — skill tem mais detalhe |
| `.reversa/context/modules.json` | business_rules | regra-alterada | Regras de cessão e entregáveis alinhados à skill |

## Regras-chave sincronizadas (skill ↔ código)

1. **Regra 4 (cessão véspera):** estrita = sem cessão na semana da prova nem na anterior; relaxada = **só** libera cessão após o dia da prova (`Cessoes.pode_ceder_bloco`, `gerar_calendario.py:~853`)
2. **FORCAR_DATA:** reserva semanas antes das provas coordenadas (`resolver_par`, ~1303)
3. **Relatório:** seção obrigatória "Regras relaxadas" por turma+disciplina (`relatorio()`, `detectar_regras_relaxadas`)
4. **Verificação:** regra 4 relaxada → aviso, não falha; cessão antes da prova → sempre falha (`verificar_calendario.py`)
5. **Cores:** ARGB `FF` + RGB; amarelo exclusivo simulados; laranja intervalo

## Fontes

- `.claude/skills/calendario-provas/SKILL.md`
- `gerar_calendario.py`
- `verificar_calendario.py`
- `.reversa/context/sources.json`
