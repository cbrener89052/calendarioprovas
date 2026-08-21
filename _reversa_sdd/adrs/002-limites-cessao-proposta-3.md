# ADR-002 — Limites de cessão de aula (Proposta 3)

**Status:** Aceito  
**Data:** 2026-08-07 (PR #4)  
**Confiança:** 🟢

## Contexto

Professores cediam tempos para provas de colegas sem controle — risco de sobrecarga (caso Profa. Luiza/Biologia).

## Decisão

Implementar classe `Cessoes` com 5 regras (tetos numéricos + percentual 11% + sem contato + vésperas). Escada de afrouxamento por turma se insolúvel.

## Consequências

- Backtracking ~100× mais lento (`MAX_NOS`, pré-computação de slots)
- Relatório de tempos cedidos tornou-se entregável obrigatório
- Verificador checa regras 1–5 separando problemas vs avisos
