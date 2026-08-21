# UI — Configuração das semanas do ENEM

> Spec `EnemWeekConfig` | ADR-015 | Confirmado Brener 2026-08-21

## Objetivo

Permitir que o coordenador **customize** quais disciplinas/provas podem ocorrer
na semana anterior a **cada** data do ENEM — sem listas fixas hardcoded no
código. O sistema **Must** perguntar as **duas datas** do ENEM a cada rodada.

## Contexto

A skill sugere listas padrão por janela (1ª prova vs 2ª prova), mas o produto
trata isso como **default editável**, não como regra imutável no solver.

## Componente

**`EnemWeekConfigPanel`** — etapa de ingestão, antes da fatoração (junto a
bloqueios/catálogo ou Tela 0 regras especiais).

## Fluxo

```
Informar data ENEM #1 (domingo) → selecionar disciplinas permitidas na janela
Informar data ENEM #2 (domingo) → selecionar disciplinas permitidas na janela
Salvar → EnemWeekConfig no RuleSetSnapshot / CalendarConstraints
Fatoração → solver só aloca disciplinas permitidas em cada janela
```

## Regras 🟢

| ID | Regra |
|----|-------|
| E-01 | **Sempre duas datas** ENEM por rodada (domingos). |
| E-02 | Janela = **6 dias corridos imediatamente anteriores** a cada domingo (seg–sáb). |
| E-03 | Coordenador **marca** quais disciplinas **podem** ter prova na janela. |
| E-04 | Disciplinas **não marcadas** = bloqueadas na janela (solver + verificador). |
| E-05 | Defaults 🟡 pré-preenchidos a partir da skill (editáveis antes de salvar). |
| E-06 | Vale para **todas as turmas** que tenham a disciplina no catálogo. |

## UI

| Elemento | Comportamento |
|----------|---------------|
| Campo **Data ENEM 1** | Date picker; validar domingo 🟡 |
| Campo **Data ENEM 2** | Idem; distinta da primeira |
| Lista disciplinas janela 1 | Multi-select (checkboxes) agrupadas por área |
| Lista disciplinas janela 2 | Idem |
| Botão **Usar sugestão skill** | Preenche listas padrão da skill |
| Preview calendário 🟡 | Destaca as duas janelas de 6 dias no grid |

## Persistência

```json
{
  "enem_dates": ["2026-11-08", "2026-11-15"],
  "windows": [
    { "enem_date": "2026-11-08", "allowed_disciplines": ["LP/LIT/RED", "Hist", "..."] },
    { "enem_date": "2026-11-15", "allowed_disciplines": ["Mat", "Bio", "..."] }
  ]
}
```

Entidade: `EnemWeekConfig` ligada a `calendario_id` / `RuleSetSnapshot`.

## Integração

| Consumidor | Uso |
|------------|-----|
| `CalendarSolver` | Rejeita slot se disciplina ∉ allowed na janela |
| `CalendarVerifier` | PROBLEMA se violação |
| `RulesSelectionWizard` | Regra R-ENEM aplicável/flexível 🟡 |
| Copiloto RAG | Explica violações citando config salva |

## Fora de escopo (confirmado L-01)

- **R-2CH** e **véspera 2CH série 9** permanecem **checklist manual** (skill/copiloto), não automatizados no solver v1.
