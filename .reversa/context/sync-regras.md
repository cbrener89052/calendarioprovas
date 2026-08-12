# Sincronizar regras (Claude Code) ↔ Reversa (Cursor)

**GitHub é a fonte da verdade.** Skill, código Python, referência do semestre e
specs versionadas vivem no repositório remoto
`https://github.com/cbrener89052/calendarioprovas`. Cópias locais e snapshots
Reversa são **derivados** — sempre reconciliar com `origin/main` antes de
confiar no conteúdo.

## Hierarquia de fontes

| Prioridade | Camada | Onde | Papel |
|---|---|---|---|
| **0** | **GitHub remoto** | `origin/main` (dev), `origin/producao` (validado) | **Fonte da verdade** — o que não está no remoto não existe para a equipe |
| 1 | Fonte viva (no repo) | `.claude/skills/calendario-provas/SKILL.md` | Regras em linguagem humana (editadas no repo → push) |
| 2 | Código | `gerar_calendario.py`, `verificar_calendario.py` | Implementação e checklist |
| 3 | Rodada | `referencia/estado_*.md` | Períodos, simulados, exceções deste semestre |
| 4 | Snapshot Reversa | `_reversa_sdd/` | Specs extraídas — **documentação derivada**, não operacional |
| 5 | PDF | `referencia/Regras_*.pdf` | Resumo estático; pode defasar — regenerar após mudar skill |

A lista oficial de arquivos canônicos e hashes está em **`.reversa/context/sources.json`**.

## Fluxo enquanto você atualiza regras

```
Claude Code / Cursor (qualquer máquina)
  │  editar SKILL.md + scripts Python
  │  commit + push → origin/main
  v
GitHub / main  ◄── FONTE DA VERDADE
  │  git pull (outra máquina, agente cloud, Windows)
  v
Cópia local alinhada
  │  Reversa lê sources.json → compara hashes
  │  (opcional) re-gerar PDF e re-extração parcial
  v
_reversa_sdd/ alinhado de novo (derivado)
```

### Passo a passo

1. **Em qualquer ambiente** — termine o lote de alterações na skill e/ou nos scripts.
2. **Commit + push para GitHub** — `commit_github.bat` (Windows) ou `git push origin main`.
3. **Nas outras máquinas / agente cloud** — **obrigatório** `git pull origin main`
   (`atualizar_do_github.bat` no Windows) **antes** de gerar calendário ou continuar Reversa.
4. **Regenerar PDF** (recomendado após mudar a skill):
   ```bash
   python exportar_regras_pdf.py
   ```
   Commit do PDF gerado junto, se for distribuído à escola.
5. **Avise o Reversa** no chat, por exemplo:
   > "Atualizei as regras na skill no GitHub. Re-sincronize regras-negocio, geracao-calendario e verificacao-calendario a partir de sources.json."

## Regra para agentes Cursor / Cloud

1. **Nunca** assumir que a cópia local está atualizada — verificar `git fetch` +
   comparar com `origin/main` (ou pedir ao usuário que rode `atualizar_do_github.bat`).
2. **Antes de implementar** reconstrução ou gerar calendário: ler arquivos canônicos
   **após** pull; comparar hashes com `sources.json`.
3. **Após concluir trabalho:** commit + push em `main` (branch de feature → PR → merge).
4. Se `_reversa_sdd/` divergir da skill/código em `main`, **GitHub prevalece** —
   atualizar specs via sync/re-extração, não o contrário.

## O que pedir ao Reversa (sem refazer tudo)

| O que mudou | O que re-rodar |
|---|---|
| Só texto da skill / PDF | Arqueólogo `regras-negocio` + `exportar_regras_pdf.py` + Detetive (domain) |
| Regras + código do gerador | Arqueólogo `geracao-calendario` + `verificacao-calendario` + Detetive |
| Mudança grande / nova feature | `/reversa` completo (re-extração; adendos antigos viram histórico) |
| Já codou algo no ciclo forward | `/reversa-sync` entre entregas (ponte até a próxima re-extração) |

Não é obrigatório reiniciar o Reversa do zero: diga **CONTINUAR** e peça para **atualizar só os módulos afetados**, lendo primeiro `.reversa/context/sources.json` **depois de pull do GitHub**.

## Como o Reversa sabe se está defasado

Após cada sincronização, o agente deve:

1. Garantir `main` atualizada com `origin/main`
2. Calcular `sha256` dos arquivos em `sources.json` → `canonical[].content_hash_sha256`
3. Se o hash mudou em relação ao valor salvo → marcar módulos afetados para re-análise
4. Atualizar `synced_to_reversa_at` quando `_reversa_sdd/` for regenerado

Comando útil (Linux / cloud):

```bash
git pull origin main
sha256sum .claude/skills/calendario-provas/SKILL.md gerar_calendario.py verificar_calendario.py
```

## Regra prática

- **GitHub `main` = verdade operacional** (skill + código + referência versionados)
- **`_reversa_sdd/` = documentação derivada** — atualize quando quiser specs/ERD alinhados, ou deixe o Reversa ler a skill direto na fase Interpretação/Geração
- **Pasta local sem push = rascunho privado** — não use para decidir regras da escola

## Branches

- Desenvolvimento contínuo (skill, Reversa, rascunhos): **`main`** → sempre sincronizada via GitHub
- Versão validada para a escola: **`producao`** (só após `verificar_calendario.py` OK)

Veja também: `referencia/fluxo-git-main-producao.md`.
