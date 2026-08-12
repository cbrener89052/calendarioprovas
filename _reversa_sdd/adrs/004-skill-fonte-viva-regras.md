# ADR-004 — Skill como fonte viva de regras (GitHub canônico)

**Status:** Aceito (atualizado 2026-08-12)  
**Data:** 2026-08-09  
**Confiança:** 🟢

## Contexto

Regras evoluem via Claude Code (skill) mais rápido que código. Reversa precisava de sync explícito. Com múltiplos ambientes (Windows local, Cursor, agente cloud), surgiu risco de cópias locais defasadas serem tratadas como verdade.

## Decisão

1. **GitHub `origin/main` é a fonte da verdade** do repositório
   `https://github.com/cbrener89052/calendarioprovas` — skill, scripts Python,
   referência do semestre e specs versionadas.
2. **`.claude/skills/calendario-provas/SKILL.md`** = fonte humana principal de regras
   (versionada no GitHub, não só na máquina local).
3. **`.reversa/context/sources.json`** declara fontes canônicas + hashes; agentes
   devem `git pull` antes de comparar.
4. **`_reversa_sdd/`** = documentação derivada (Reversa); **nunca prevalece** sobre
   skill/código em `main` quando houver divergência.
5. Novas regras podem entrar só na skill primeiro (ex.: PR #14 LP/LIT/RED 10 dias).
6. **`origin/producao`** = snapshot validado (pós-verificador OK), promovido a partir de `main`.

## Hierarquia

```
GitHub origin/main  →  skill + código + referencia/
        ↓ pull
Cópia local / agente cloud
        ↓ extração opcional
_reversa_sdd/  (derivado)
        ↓ seed (plataforma)
PostgreSQL regra_catalogo  (operacional por coordenador)
```

## Consequências

- Lacunas documentadas quando skill > código
- Adendos em `_reversa_sdd/addenda/` até re-extração
- PDF (`exportar_regras_pdf.py`) é resumo estático, pode defasar
- Agentes cloud: commit + push ao concluir; nunca assumir local atualizado
- Conflito local vs remoto: **prevalece GitHub `main`** (salvo merge acordado)

## Referências

- `.reversa/context/sync-regras.md`
- `referencia/fluxo-git-main-producao.md`
- Skill: seção "Fonte da verdade — GitHub"
