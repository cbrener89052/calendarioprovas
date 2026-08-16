# ADR-011 — Máscaras estruturadas e recálculo sem IA

> Status: **aceito** (requisito usuário 2026-08-16)  
> Confiança: 🟢

## Contexto

Brener esclareceu que a plataforma deve oferecer **máscaras padrão
downloadáveis** para:

1. **Provas a registrar** — tabela com ordem de cada prova e nº de tempos
   de aplicação (e carga semanal da disciplina).
2. **Bloqueios e calendário** — feriados, recessos, semanas vetadas, dias
   sem prova, simulados fixos.

**Objetivo explícito:** evitar uso de IA (tokens OpenAI) **toda vez** que
for necessário **recalcular** o horário. Entradas estruturadas definem os
limites permitidos/vetados; o solver consome dados determinísticos.

O copiloto (`ScheduleCopilotService`, ADR-008) permanece para **refração
colaborativa**, diagnóstico e Q&A — **não** como canal obrigatório de
entrada de constraints a cada rodada.

## Decisão

1. **Três máscaras de entrada** (download/upload), além do layout Klausurplan:
   - `Mascara_Entrada_Provas.xlsx` — catálogo + aba `provas` (uma linha por prova)
   - `Mascara_Bloqueios_Calendario.xlsx` — feriados, bloqueios, simulados
   - Layout Klausurplan — apenas saída visual (ADR-010)
2. **`IntakeTemplateService`** gera e faz parse das **duas** máscaras de dados.
3. Persistência em **`ExamCatalog`** + **`CalendarConstraints`** antes da fatoração.
4. **Recálculo Must:** pipeline grade + catálogo + constraints + RuleSetSnapshot
   → `CalendarSolver` **sem** chamada OpenAI.
5. Copiloto **Must not** ser invocado para interpretar uploads de máscara;
   parser validado substitui LLM na ingestão.

## Consequências

- ✅ Recálculo repetível sem custo de tokens
- ✅ Fim da dessincronia manual feriados (entrada única)
- ⚠️ Dois downloads na UI (provas + bloqueios) ou pacote zip institucional
- ⚠️ Migração legado: exportar `BLOQUEIOS`/`SIMULADOS` → máscara exemplo 2SEM 2026

## Evidência

- `.reversa/context/user-requirements.md#Máscaras estruturadas`
- `_reversa_sdd/templates/mascara-entrada-provas-spec.md`
- `_reversa_sdd/templates/mascara-bloqueios-calendario-spec.md`
