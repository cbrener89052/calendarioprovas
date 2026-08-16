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

1. Separar conceitos:
   - **`ExamCatalog`** — lista `(turma, disciplina, n_tempos[, periodo])`
   - **`CalendarTemplate`** — malha xlsx semanal (opcional na plataforma)
2. **Três modos de preenchimento** do `ExamCatalog` (plataforma Must):
   - **A — Importar** modelo/prova anterior (xlsx ou blob)
   - **B — Editar tabela** na interface (grid editável)
   - **C — Derivar da grade** (paridade legado `montar_exames()`)
3. Modelo Klausurplan **completo** deixa de ser obrigatório; simulados e
   bloqueios podem vir de import parcial, tela dedicada ou constantes 🟡.
4. Saída continua **Proposta_3 xlsx** — se não houver template, o sistema
   **gera** malha a partir de template institucional vazio + semestre 🟡.
5. Solver consome `ExamCatalog` unificado, independente da origem.

## Consequências

- ✅ Coordenador sem Klausurplan do semestre ainda pode fatorar
- ✅ Reuso de modelos de semestres/provas anteriores
- ⚠️ UI nova: `ExamCatalogEditor` (turma · disciplina · tempos)
- ⚠️ Validar consistência catálogo × grade (disciplina existe na turma?)
- ⚠️ Legado CLI permanece acoplado ao xlsx até refatoração forward

## Evidência

- `.reversa/context/user-requirements.md#Catálogo de provas`
