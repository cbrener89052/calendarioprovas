# ADR-010 — Catálogo de provas sem modelo Klausurplan obrigatório

> Status: **aceito** (requisito usuário 2026-08-16)  
> Confiança: 🟢

## Contexto

As specs assumiam **modelo xlsx Klausurplan** como entrada fixa. Brener
esclareceu: **nem sempre** haverá esse modelo completo.

Alternativas válidas:

1. **Modelo de provas anteriores** — descreve turma/grupo, disciplina e
   quantidade de tempos exigidos, sem malha semanal completa.
2. **Tabela manual na UI** — coordenador informa turma, disciplina e
   `n_tempos` (aplicação da prova).

A **grade horária** continua necessária para slots, presença do professor
e cessões. O que flexibiliza é a **origem da lista de exames** que hoje
`montar_exames()` deriva só da grade + regras hardcoded.

## Decisão

1. Separar **três** artefatos xlsx:
   - **`ExamCatalog`** — dados `(turma, disciplina, n_provas, n_aulas_semanais, n_tempos[, periodo])`
   - **`IntakeTemplate`** — máscara padrão download/upload (`Mascara_Entrada_Provas.xlsx`)
   - **`CalendarLayoutTemplate`** — malha Klausurplan (`Klausurplan_2026_2SEM.xlsx` no GitHub)
2. **Máscara padrão (Must):** plataforma gera link *"Baixe sua planilha padrão
   aqui"*; coordenador preenche disciplinas, nº provas/disciplina e nº tempos
   de aula/semana; upload alimenta `ExamCatalog`.
3. **Layout Klausurplan (Must institucional):** template de **design** do
   calendário semanal — já no repo; usado em `escrever()`, não substitui
   máscara de entrada.
4. Três modos de catálogo: **A** upload máscara | **B** UI | **C** derivar grade.
5. Klausurplan preenchido do semestre **não** é entrada obrigatória.
6. Saída **Proposta_3 xlsx** usa layout institucional Klausurplan.
7. Solver consome `ExamCatalog` unificado.

## Atualização 2026-08-16 (3)

ADR-011: segunda máscara (`Mascara_Bloqueios_Calendario.xlsx`) + aba `provas`
por ordem; recálculo determinístico sem IA.

Ver:
- `_reversa_sdd/templates/mascara-bloqueios-calendario-spec.md`
- `_reversa_sdd/adrs/011-mascaras-estruturadas-sem-ia-recalculo.md`

## Atualização 2026-08-16 (2)

Ver `_reversa_sdd/templates/mascara-entrada-provas-spec.md`.

## Consequências

- ✅ Coordenador sem Klausurplan do semestre ainda pode fatorar
- ✅ Reuso de modelos de semestres/provas anteriores
- ⚠️ UI nova: `ExamCatalogEditor` (turma · disciplina · tempos)
- ⚠️ Validar consistência catálogo × grade (disciplina existe na turma?)
- ⚠️ Legado CLI permanece acoplado ao xlsx até refatoração forward

## Evidência

- `.reversa/context/user-requirements.md#Catálogo de provas`
