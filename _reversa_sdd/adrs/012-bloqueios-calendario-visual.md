# ADR-012 — Bloqueios via calendário visual (não planilha)

> Status: **aceito** (requisito usuário 2026-08-16)  
> Suplementa ADR-011 | Confiança: 🟢

## Contexto

ADR-011 previa **`Mascara_Bloqueios_Calendario.xlsx`** como entrada principal.
Brener revisou: **preencher tabelas no Excel seria péssima experiência** para
o coordenador.

Nova proposta: **tela visual em formato de calendário** (malha semanal como o
Klausurplan), onde o usuário **clica** nos dias ou nas semanas em que **não
pode haver prova** — configurável **por turma** e **por série**.

Objetivo mantido (ADR-011): constraints persistidas → recálculo **sem IA**.

## Decisão

1. **Entrada primária (Must):** componente **`CalendarBlockPicker`** — grid
   semanal clicável, escopo turma ou série.
2. **Planilha de bloqueios:** **opcional** — apenas export/import/backup e
   migração legado; **não** é o fluxo principal na UI.
3. Feriados institucionais podem ser **pré-carregados** no grid (somente leitura
   ou editável conforme perfil); bloqueios do coordenador somam-se a eles.
4. Simulados fixos: mesma malha ou painel adjacente 🟡 — mesma persistência
   `CalendarConstraints`.
5. Dados clicados → `CalendarConstraints` (PostgreSQL) → solver + verificador.

## Interação (Must)

| Ação | Efeito |
|------|--------|
| Clicar **dia** | Alterna “sem prova” para turma/série selecionada |
| Clicar **cabeçalho da semana** | Alterna “semana inteira sem prova” |
| Seletor **série** | Aplica bloqueio a todas turmas da série (ex.: 10 → 10C1, 10C2) |
| Seletor **turma** | Bloqueio só na turma escolhida |

## Consequências

- ✅ UX alinhada ao trabalho mental do coordenador (calendário, não tabela)
- ✅ Recálculo continua determinístico (sem tokens OpenAI na ingestão)
- ⚠️ Frontend mais complexo que parser xlsx
- ⚠️ Export xlsx mantido para auditoria e seed do legado 2SEM 2026

## Evidência

- `.reversa/context/user-requirements.md#Bloqueios e calendário — tela visual`
- `_reversa_sdd/ui/calendar-block-picker-spec.md`
