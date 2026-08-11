# ADR-010 — Verificador como auditoria independente do xlsx

**Status:** Aceito  
**Data:** 2026-08-11  
**Confiança:** 🟢 (confirmado por Brener + `verificar_calendario.py`)

## Contexto

`verificar_calendario.py` **não é um teste unitário do gerador**. É o **script de auditoria** do calendário: ele **nunca confia na memória do gerador** — relê o `.xlsx` já gravado (`Proposta_3_Calendario_Provas_2026_2SEM.xlsx`), **célula por célula**, e confere se o que está escrito de fato obedece a todas as regras da skill.

Roda as **8 turmas** (8 abas) e imprime dois grupos de resultado:

| Grupo | Significado | Bloqueia entrega? |
|-------|-------------|-------------------|
| **PROBLEMA** | Falha real do checklist | Sim |
| **AVISO** | Regra relaxada por inviabilidade, já documentada como aceitável | Não |

Exemplos de AVISO (Proposta 3): regra 4 relaxada (cessão véspera), regra 7b (prova à tarde quando havia opção de manhã), regras 1/5 quando o gerador documentou relaxamento.

## Decisão

1. **Fonte da verdade pós-geração = arquivo xlsx**, não estruturas Python do solver (`alocacoes`, `Cessoes`, etc.).
2. **Pipeline plataforma:** worker grava blob xlsx → **sempre** invoca verificador sobre o blob → persiste `verificacao_result` com severidade `erro` | `aviso`.
3. **Publish gate:** bloqueado se existir `PROBLEMA` (erro crítico); **AVISO** não impede publicação, mas deve aparecer na UI (SCR-08).
4. **Parallel Run:** paridade medida com verificador rodando sobre xlsx CLI **e** xlsx plataforma — mesma bateria de checks.
5. **Refactor alvo (`packages/solver`):** separar `packages/verifier` (ou submódulo) que recebe **caminho/blob xlsx** + `RuleContext` + grade aprovada; **não** expor API “verificar memória do solver”.

## Alternativas consideradas

| Opção | Rejeitada porque |
|---|---|
| Verificar só estado in-memory pós-`montar_proposta` | Edições manuais no xlsx, bugs de escrita e drift gerador↔arquivo passam despercebidos |
| Unificar gerador+verificador num único passo | Perde o gate independente que hoje protege entrega |
| Tratar AVISO como erro | Contradiz skill e prática atual (relaxamentos documentados) |

## Consequências

- Worker T6: ordem fixa `solver → write xlsx → verifier(xlsx) → persist`
- API `POST /calendarios/{id}/verificar` re-lê blob, idempotente
- Specs `verificacao-calendario` e `geracao-calendario` referenciam este ADR
- Testes paridade: comparar stdout/lista PROBLEMA+AVISO, não só bytes do xlsx

## Evidência legado

```5:6:verificar_calendario.py
Le os arquivos .xlsx ja gravados (nao confia na memoria do gerador).
```

```383:393:verificar_calendario.py
    if problemas:
        print(f"{len(problemas)} PROBLEMA(S):")
        ...
    if avisos:
        print(f"\n{len(avisos)} AVISO(S) — regras relaxadas por inviabilidade, "
              "não são falhas do checklist:")
```
