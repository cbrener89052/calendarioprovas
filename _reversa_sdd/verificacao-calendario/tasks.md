# Verificação de Calendário — Tarefas de Implementação

> Feature: `verificacao-calendario` | Legado: `verificar_calendario.py`

## Pré-requisitos

- [ ] Módulo `gerar_calendario` (ou extrato) com `professor_presente_no_bloco`, `slots_da_disciplina`, constantes
- [ ] Proposta xlsx disponível no blob/path de teste
- [ ] Golden file com PROBLEMA/AVISO conhecidos do semestre referência

## Tarefas

- [ ] T-01, Extrair parser de células (colunas E–I, semanas 1–20)
  - Origem: `verificar_calendario.py` L76–97
  - Critério de pronto: lista `provas` igual ao legado para turma piloto
  - Confiança: 🟢

- [ ] T-02, Implementar itens 0–4 do checklist
  - Origem: L104–163
  - Critério de pronto: golden tests R-P1, R-SEM, R-G1, R-DIA, datas
  - Confiança: 🟢

- [ ] T-03, Implementar itens 5–5c (contagem, distância, LP/LIT/RED, simulados)
  - Origem: L165–215
  - Critério de pronto: casos 9C Fis/Qui 1 prova; LP/LIT/RED 3 tempos
  - Confiança: 🟢

- [ ] T-04, Implementar itens 6–7c
  - Origem: L217–291
  - Critério de pronto: Fil 1 tempo; veto doador 1 aula/semana
  - Confiança: 🟢

- [ ] T-05, Implementar item 7b (AVISO tarde P3)
  - Origem: L229–267
  - Critério de pronto: AVISO quando `cedo` não vazio; PROBLEMA em P1/P2 legado N/A
  - Confiança: 🟢

- [ ] T-06, Implementar itens 8–10 (`FORCAR_DATA`)
  - Origem: L293–320
  - Critério de pronto: simulados oficiais; intervalo recreio
  - Confiança: 🟢

- [ ] T-07, Implementar item 10b cessão C1–C5
  - Origem: L322–380
  - Critério de pronto: PROBLEMA regra 2 (1 aula); AVISO relaxadas
  - Confiança: 🟢

- [ ] T-08, Implementar item 11 coordenação irmãs + `COORDENACAO_EXCECAO`
  - Origem: L402–418, ADR-006
  - Critério de pronto: Fil/Soc não exigem coincidência
  - Confiança: 🟢

- [ ] T-09, Unificar `FERIADOS` e `BLOQUEIOS` com gerador
  - Origem: lacuna code-analysis
  - Critério de pronto: mesmo caso 02/11 passa gerador e verificador
  - Confiança: 🔴

- [ ] T-10, Expor `CalendarVerifier` API + `VerificationReport` JSON
  - Origem: `_reversa_sdd/architecture.md`
  - Critério de pronto: GET verification; UI VerificationPanel
  - Confiança: 🟡

- [ ] T-11, Integrar RuleSetSnapshot (regra off / flex → AVISO)
  - Origem: user-requirements
  - Critério de pronto: desativar C4 não gera PROBLEMA 10b
  - Confiança: 🟡

- [ ] T-12, Tool `get_verification_report` para copiloto + deanonymize UI
  - Origem: ADR-008, ADR-009
  - Critério de pronto: chat explica item 0 com sigla real
  - Confiança: 🟡

- [ ] T-13, Gate fechar horário se `problemas.length > 0`
  - Origem: `_reversa_sdd/state-machines.md`
  - Critério de pronto: API 409; botão desabilitado
  - Confiança: 🟡

## Tarefas de Teste

- [ ] TT-01, Golden: xlsx referência → zero PROBLEMA (ou set conhecido)
- [ ] TT-02, Inject violação item 0 → PROBLEMA único identificável
- [ ] TT-03, Item 7b → AVISO não bloqueia fechamento
- [ ] TT-04, Paridade stdout CLI vs JSON API

## Ordem Sugerida

1. T-01 → T-08 (paridade legado)
2. T-09 (feriados)
3. T-10 → T-13 (plataforma + copiloto)

## Lacunas Pendentes (🔴)

- ENEM / véspera 2CH no checklist
- Critério exato AVISO 10b pós-relaxamento solver
