# ADR-006 — Filosofia e Sociologia: exceção fixa de coordenação

**Status:** Aceito (retroativo)  
**Data:** 2026-08 (PR #42, `e7b2202`, `0a8e3a3`)  
**Confiança:** 🟢

## Contexto

Professores comuns entre turmas irmãs normalmente aplicam prova **simultaneamente**. Filosofia e Sociologia aplicam no **tempo próprio de cada turma** — pedido explícito da coordenação.

## Decisão

- Tratar Fil/Soc como caso "professores diferentes" para coordenação entre irmãs
- Codificar em `COORDENACAO_EXCECAO` no verificador
- Skill: regra **fixa da escola**, não exceção pontual por semestre — adicionar automaticamente pares Fil/Soc ao configurar novo semestre

## Consequências

- ✅ Reflete prática pedagógica real
- ⚠️ Lista manual de pares em `verificar_calendario.py` (não no gerador)
- ✅ Commits de reposicionamento Soc em 10C ilustram uso

## Evidência Git

- `7dc521c`, `0a8e3a3`, `e7b2202`
