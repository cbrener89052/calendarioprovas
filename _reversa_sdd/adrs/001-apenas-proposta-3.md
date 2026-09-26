# ADR-001 — Apenas Proposta 3 em desenvolvimento

**Status:** Aceito  
**Data:** 2026-08 (commit `60da625`)  
**Confiança:** 🟢

## Contexto

O sistema gerava múltiplas propostas (1, 2, 3) com estratégias diferentes. A coordenação escolheu focar na **Proposta 3** (limites de cessão de aula).

## Decisão

Manter só Proposta 3 nos scripts (`gerar_calendario.py`, exportadores, verificador). Propostas 1 e 2 removidas do fluxo ativo.

## Consequências

- Código e skill simplificados
- Verificador e exportadores iteram só `proposta=3`
- Histórico git preserva evolução das propostas anteriores
