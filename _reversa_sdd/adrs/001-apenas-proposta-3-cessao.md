# ADR-001 — Apenas Proposta 3 com limites de cessão

**Status:** Aceito (retroativo)  
**Data:** inferido ~2026-07/08 (commits `60da625`, skill)  
**Confiança:** 🟢

## Contexto

O gerador originalmente produzia **3 propostas** com regras crescentes. A coordenação pediu limites de cessão de aula (regras 1–5) para proteger carga horária dos professores.

## Decisão

- Descontinuar geração operacional das Propostas 1 e 2
- **Proposta 3** = única proposta desenvolvida e verificada (`main()` L2066; verificador só lê `prop==3`)
- Implementar classe `Cessoes` com escada de relaxamento por turma

## Consequências

- ✅ Cessões rastreáveis e comparáveis ao relatório histórico
- ✅ Verificador item 10b específico para P3
- ⚠️ Solver muito mais lento (~600 nós/s vs dezenas de milhares)
- ⚠️ Comparações com semestres antigos exigem cautela (Proposta 1 tinha cessões maiores)

## Evidência Git

- `60da625` — skill: mantém só Proposta 3
- Commits de limites de cessão e `folga_extra` por turma
