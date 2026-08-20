# ADR-003 — Presença do professor na aplicação (prioridade 1)

**Status:** Aceito (retroativo)  
**Data:** 2026-08-08 (`677cec0`, PR #24)  
**Confiança:** 🟢

## Contexto

Revisão manual encontrou provas (GL, Física, Redação) em blocos sem nenhum professor citado presente — efeito de edições manuais, não do gerador ideal.

## Decisão

- Regra **PRIORIDADE 1**: todo professor citado deve ter aula da família da disciplina no bloco (turma ou irmã)
- Implementar `professor_presente_no_bloco()` central
- Checklist item **0** no verificador (antes de todos)
- **Nunca relaxar** no solver — acima de intervalo, tarde e grupo 1

## Consequências

- ✅ Alinhamento pedagógico (professor acompanha prova)
- ⚠️ Reduz espaço de solução; mais edições manuais possíveis
- ✅ Detecta regressões pós-refração

## Evidência Git

- PR #24, `677cec0`, skill seção PRIORIDADE 1
