# Fluxo Git — main vs producao

## Fonte da verdade

**GitHub** (`https://github.com/cbrener89052/calendarioprovas`) é a **fonte da
verdade**. Nenhuma pasta local — Windows, Cursor ou agente cloud — prevalece
sobre o remoto sem `git pull` / `git push` explícitos.

| Onde | Papel |
|---|---|
| **`origin/main` no GitHub** | Canônico — skill, scripts, referência, specs |
| Pasta local | Cópia de trabalho; pode estar defasada |
| **`origin/producao`** | Release validada (pós-verificador) |

**Regra:** conflito entre local e GitHub → **prevalece GitHub `main`**, salvo
merge deliberado acordado.

## Duas branches

| Branch | Papel | Quem usa |
|---|---|---|
| **`main`** | Desenvolvimento contínuo: scripts, Reversa, specs, rascunhos | Cursor (agente) + voce no dia a dia |
| **`producao`** | Versao **validada e estavel** para a escola | Coordenadores quando querem o que ja passou no verificador |

> O nome da branch e `producao` (sem acento) — Git funciona melhor assim.

## Fluxo visual

```
  Cursor / Windows (dev)
         │
         │  commit + push a cada evolucao
         v
    GitHub / main  ──────────────────────┐
         │                               │
         │  quando validado (OK)         │  atualizar_do_github.bat
         v                               v
  promover_para_producao.bat      Pasta local (main)
         │
         v
    GitHub / producao  ◄── git checkout producao (versao estavel)
```

## O que vai em cada branch

### main (sempre)
- Alteracoes de codigo Python
- Artefatos Reversa (`_reversa_sdd/`, `.reversa/`)
- README, skill, scripts `.bat`
- Propostas em elaboracao em `Horario desenvolvido/`

### producao (so quando promover)
- Mesmo codigo da `main`, **no ponto em que voce validou**
- Idealmente apos `python verificar_calendario.py` terminar com **OK**
- Calendarios finais que a escola vai usar

## Comandos no Windows

### Desenvolvimento (padrao)

```powershell
git checkout main
git pull --rebase origin main
# ... editar ...
# commit_github.bat
```

Ou: **`atualizar_do_github.bat`** (baixar) / **`commit_github.bat`** (enviar).

### Promover para producao

Dois cliques em **`promover_para_producao.bat`**

Ou manualmente:

```powershell
git checkout main
git pull origin main
git checkout producao
git merge main -m "Promove versao validada"
git push origin producao
git checkout main
```

### Usar a versao estavel

```powershell
git fetch origin
git checkout producao
git pull origin producao
```

### Voltar ao desenvolvimento

```powershell
git checkout main
git pull origin main
```

## Regra para o agente Cursor

**GitHub é a fonte da verdade.** A cada evolução concluída:

1. **`git pull origin main`** no início da sessão (ou confirmar que o usuário
   puxou no Windows).
2. **Commit + push em `main`** (ou PR mergeado em `main`) ao concluir.
3. **Promover para `producao`** somente quando:
   - `verificar_calendario.py` passou com OK, ou
   - voce pedir explicitamente
4. **Nunca** tratar `_reversa_sdd/` como verdade se divergir de skill/código em `main`.

## Quando NAO promover

- Trabalho Reversa em andamento (specs incompletas)
- Proposta ainda nao verificada
- Experimentos / Proposta 1 e 2 se so a 3 for oficial
