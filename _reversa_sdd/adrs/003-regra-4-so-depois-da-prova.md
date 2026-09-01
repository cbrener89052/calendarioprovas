# ADR-003 — Regra 4 refinada: afrouxamento só depois da prova

**Status:** Aceito  
**Data:** 2026-08-08 (PRs #10, #11)  
**Confiança:** 🟢

## Contexto

Afrouxar regra 4 liberava cessão na semana **anterior** à prova, eliminando a aula de revisão.

## Decisão

Com `sem_regra4` por turma: cessão permitida apenas **após** o dia da prova. Semana anterior e dia da prova permanecem protegidos.

## Consequências

- `Cessoes.pode_ceder_bloco` distingue dia `d` vs semana `w`
- Verificador: violação antes = falha; depois relaxada = aviso
- Skill documenta exemplo (prova terça → ceder a partir quarta)
