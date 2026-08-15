# Sincronizar regras (Claude Code) ↔ Reversa (Cursor)

Você edita regras no **Claude Code** (skill + scripts). O **Reversa** mantém um **snapshot** em `_reversa_sdd/`. Esse snapshot **não se atualiza sozinho** — mas os agentes podem sempre ler a **fonte viva** se você seguir este fluxo.

## Três camadas

| Camada | Onde | Papel |
|---|---|---|
| **1. Fonte viva** | `.claude/skills/calendario-provas/SKILL.md` | Regras em linguagem humana (você edita aqui) |
| **2. Código** | `gerar_calendario.py`, `verificar_calendario.py` | Implementação e checklist |
| **3. Snapshot Reversa** | `_reversa_sdd/` | Specs extraídas para Detetive, Arquiteto, Writer |

A lista oficial de fontes vivas está em **`.reversa/context/sources.json`**.

Espelho Cursor: **`.agents/skills/calendario-provas/SKILL.md`** (cópia da fonte viva após cada sync).

## Fluxo enquanto você atualiza regras

```
Claude Code (Windows)
  │  editar SKILL.md + scripts Python
  │  commit_github.bat  →  push main
  v
GitHub / main
  │  git pull (Cursor ou atualizar_do_github.bat)
  v
Reversa lê sources.json → SKILL.md + código atuais
  │  (opcional) re-gerar PDF e re-extração parcial
  v
_reversa_sdd/ alinhado de novo
```

### Passo a passo

1. **No Claude Code** — termine o lote de alterações na skill e/ou nos scripts.
2. **Commit + push** — `commit_github.bat` (branch `main`).
3. **No Cursor / agente cloud** — antes de continuar o Reversa, garanta `main` atualizada (`git pull origin main`).
4. **Regenerar PDF** (recomendado após mudar a skill):
   ```bash
   python exportar_regras_pdf.py
   ```
5. **Avise o Reversa** no chat, por exemplo:
   > "Atualizei as regras na skill. Re-sincronize a partir de sources.json."

## O que pedir ao Reversa (sem refazer tudo)

| O que mudou | O que re-rodar |
|---|---|
| Só texto da skill / PDF | Arqueólogo `regras-negocio` + `exportar_regras_pdf.py` + Detetive (domain) |
| Regras + código do gerador | Arqueólogo `geracao-calendario` + `verificacao-calendario` + Detetive |
| Mudança grande / nova feature | `/reversa` completo (re-extração; adendos antigos viram histórico) |
| Já codou algo no ciclo forward | `/reversa-sync` entre entregas (ponte até a próxima re-extração) |

Não é obrigatório reiniciar o Reversa do zero: diga **CONTINUAR** e peça para **atualizar só os módulos afetados**, lendo primeiro `.reversa/context/sources.json`.

## Como o Reversa sabe se está defasado

Após cada sincronização, o agente deve:

1. Calcular `sha256` dos arquivos em `sources.json` → `canonical[].content_hash_sha256`
2. Se o hash mudou em relação ao valor salvo → marcar módulos afetados para re-análise
3. Atualizar `synced_to_reversa_at` quando `_reversa_sdd/` for regenerado

Comando útil (Linux / cloud):

```bash
sha256sum .claude/skills/calendario-provas/SKILL.md gerar_calendario.py verificar_calendario.py
```

## Regra prática

- **Skill + código no Git = verdade operacional**
- **`_reversa_sdd/` = documentação derivada** — atualize quando quiser specs/ERD alinhados, ou deixe o Reversa ler a skill direto na fase Interpretação/Geração

## Branches

- Desenvolvimento contínuo (skill, Reversa, rascunhos): **`main`**
- Versão validada para a escola: **`producao`** (só após `verificar_calendario.py` OK)

Veja também: `referencia/fluxo-git-main-producao.md`.
