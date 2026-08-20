# ADR-011 — Máscaras estruturadas e recálculo sem IA

> Status: **aceito** (requisito usuário 2026-08-16)  
> **Atualizado:** ADR-012 — bloqueios via tela visual; xlsx secundário  
> Confiança: 🟢

## Contexto

Brener esclareceu que a plataforma deve oferecer entradas estruturadas para:

1. **Provas a registrar** — ordem e nº de tempos (máscara xlsx ou UI).
2. **Bloqueios e calendário** — feriados, semanas/dias sem prova, simulados.

**Revisão 2026-08-16 (4):** planilha Excel para bloqueios foi **rejeitada**
(UX ruim). Entrada primária = **`CalendarBlockPicker`** (clique no calendário
por turma e série). Ver ADR-012.

**Objetivo explícito:** evitar uso de IA (tokens OpenAI) **toda vez** que
for necessário **recalcular** o horário. Entradas estruturadas definem os
limites permitidos/vetados; o solver consome dados determinísticos.

O copiloto (`ScheduleCopilotService`, ADR-008) permanece para **refração
colaborativa**, diagnóstico e Q&A — **não** como canal obrigatório de
entrada de constraints a cada rodada.

## Decisão

1. **Entradas estruturadas** (além do layout Klausurplan de saída):
   - **Provas:** `Mascara_Entrada_Provas.xlsx` ou `ExamCatalogEditor`
   - **Bloqueios:** **`CalendarBlockPicker`** (Must) — ADR-012
   - **Bloqueios xlsx:** export/import **opcional** (backup, legado)
2. **`CalendarConstraintsService`** persiste cliques da UI (+ feriados seed).
3. Persistência **`ExamCatalog`** + **`CalendarConstraints`** antes da fatoração.
4. **Recálculo Must:** pipeline determinístico **sem** chamada OpenAI.
5. Copiloto **Must not** interpretar bloqueios; UI + persistência substituem LLM.

## Consequências

- ✅ Recálculo repetível sem custo de tokens
- ✅ Fim da dessincronia manual feriados (entrada única)
- ✅ UX bloqueios via calendário clicável (ADR-012)
- ⚠️ Export xlsx bloqueios mantido para migração/backup

## Evidência

- `.reversa/context/user-requirements.md#Máscaras estruturadas`
- `_reversa_sdd/templates/mascara-entrada-provas-spec.md`
- `_reversa_sdd/ui/calendar-block-picker-spec.md`
- `_reversa_sdd/adrs/012-bloqueios-calendario-visual.md`
