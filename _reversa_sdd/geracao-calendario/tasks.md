# Geração de Calendário — Tarefas de Implementação

## Pré-requisitos

- [ ] Grade-base disponível (dict ou tabela BD por turma)
- [ ] Modelo xlsx do semestre com células de ocupação
- [ ] openpyxl instalado (adicionar `requirements.txt`)
- [ ] Catálogo de simulados, feriados e semanas vetadas (hoje constantes; futuro GRUPO)

## Tarefas

- [ ] T-01 — Extrair constantes para módulo `config/` ou tabela BD
  - Origem: `gerar_calendario.py` (FERIADOS, SIMULADOS, GRADES, etc.)
  - Critério de pronto: Gerador lê parâmetros de arquivo/BD sem alterar lógica
  - Confiança: 🟢

- [ ] T-02 — Implementar classe `Cessoes` com regras 1–5
  - Origem: `gerar_calendario.py:Cessoes`
  - Critério de pronto: Testes unitários cobrem teto 11%, regra 2, regra 4 pós-prova
  - Confiança: 🟢

- [ ] T-03 — Backtracking `_tentar` + `slots_da_disciplina`
  - Origem: `gerar_calendario.py:_tentar`, `slots_da_disciplina`
  - Critério de pronto: 8 turmas resolvem com seed 7 em ambiente de referência
  - Confiança: 🟢

- [ ] T-04 — Ordem pares irmãos + escada afrouxamento em `montar_proposta`
  - Origem: `gerar_calendario.py:montar_proposta`
  - Critério de pronto: Relatório lista regras relaxadas quando aplicável
  - Confiança: 🟢

- [ ] T-05 — Escrita xlsx 8 abas + relatório trocas
  - Origem: funções `escrever` / export no gerador
  - Critério de pronto: xlsx abre; verificador passa checklist base
  - Confiança: 🟢

- [ ] T-06 — Implementar RN-08 LP/LIT/RED ≥10 dias antes conselho
  - Origem: `.claude/skills/calendario-provas/SKILL.md`, PR #14
  - Critério de pronto: Verificador inclui check; gerador rejeita slot inválido
  - Confiança: 🔴 (lacuna atual)

- [ ] T-07 — Integrar `RuleContext` com toggles (plataforma)
  - Origem: ADR-006, `regras-negocio/design.md`
  - Critério de pronto: Desativar regra 3 via toggle impede relaxamento
  - Confiança: 🟡

- [ ] T-08 — Worker assíncrono FastAPI
  - Origem: `plataforma-multi-coordenador/design.md`
  - Critério de pronto: POST gera job; GET retorna status e blob xlsx
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01 — Happy path: proposta 3 completa 8 turmas, seed 7
- [ ] TT-02 — Cessão bloqueada véspera da prova (regra 4 dura)
- [ ] TT-03 — Afrouxamento regra 4 só após data da prova
- [ ] TT-04 — LP/LIT/RED 10 dias (quando T-06 implementado)
- [ ] TT-05 — MAX_NOS: falha graciosa com lista `falharam`

## Tarefas de Migração de Dados

- [ ] TM-01 — Importar grades de `extrair_grade_*.py` para tabela `grade_celula`
- [ ] TM-02 — Mapear “grupos de viagem” hardcoded → entidade GRUPO (ADR-006)

## Ordem Sugerida

1. T-01 (externalizar config) — desbloqueia multi-coordenador
2. T-02 → T-03 → T-04 → T-05 (paridade legado)
3. T-06 (lacuna PR #14)
4. T-07 → T-08 (plataforma)

## Lacunas Pendentes (🔴)

- LP/LIT/RED 10 dias no código
- Formato exato de `RuleContext` na API
- Customização IA: entra como pré-processamento ou pós-validação?
