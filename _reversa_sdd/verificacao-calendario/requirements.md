# Requirements: Verificação de Calendário

> Identificador: `002-verificacao-calendario`
> Data: `2026-08-16`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

A feature **verificacao-calendario** valida a planilha **Proposta 3** já gravada,
reexecutando o checklist da skill (itens 0–11) **relendo o xlsx** — sem confiar
na memória do gerador. Produz lista de **PROBLEMA** (falha) e **AVISO** (regra
relaxada aceitável na Proposta 3). É o gate de qualidade antes de fechar o
horário e alimenta o **copiloto OpenAI** com diagnósticos (siglas reais na UI).

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confiança |
|-------|------------------|-------------|
| `_reversa_sdd/code-analysis.md#Módulo: verificacao-calendario` | `main()` importa `G`, lê xlsx, checklist 0–11 | 🟢 |
| `_reversa_sdd/flowcharts/verificacao-calendario.md` | Fluxo parse células → checklist | 🟢 |
| `_reversa_sdd/domain.md#Regras de domínio` | Mapeamento regras R-P1, R-SEM, C1–C5 | 🟢 |
| `_reversa_sdd/adrs/002-relatorios-releem-planilha.md` | Princípio releitura independente | 🟢 |
| `_reversa_sdd/adrs/006-filosofia-sociologia-excecao-coordenacao.md` | `COORDENACAO_EXCECAO` só no verificador | 🟢 |
| `.reversa/context/user-requirements.md#Copiloto de IA` | Verificador alimenta Q&A e refração | 🟢 |
| `_reversa_sdd/adrs/009-pseudonimizacao-professores-openai.md` | UI coordenador: siglas reais | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador (legado) | Confirmar calendário antes de entregar | `python verificar_calendario.py` após gerar/editar xlsx |
| Coordenador (plataforma) | Ver painel de falhas no browser | Após fatoração/refração, abre VerificationPanel |
| Copiloto OpenAI | Explicar e priorizar correções | Consome `get_verification_report` (tokens só backend) |
| Sistema | Bloquear fechamento com PROBLEMA | CalendarLifecycle consulta verificador |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Verificação **sempre** relê planilha persistida (blob/xlsx), nunca estado RAM do solver. 🟢
   - Origem: ADR-002
   - Tipo: confirmada
2. **RN-02:** Saída classifica achados em **PROBLEMA** vs **AVISO** (item 7b tarde, cessão relaxada 10b). 🟢
   - Origem: `_reversa_sdd/domain.md#I-05`
   - Tipo: confirmada
3. **RN-03:** Zero PROBLEMA é pré-requisito para promover a `producao` / fechar horário. 🟢
   - Origem: `_reversa_sdd/domain.md`, ADR-004
   - Tipo: confirmada
4. **RN-04:** Itens do checklist respeitam **RuleSetSnapshot** — regra desativada não gera PROBLEMA; regra flexibilizada pode gerar AVISO em vez de PROBLEMA. 🟡
   - Origem: user-requirements seleção de regras
   - Tipo: nova (plataforma)
5. **RN-05:** Relatório exposto ao coordenador usa **siglas reais**; pseudonimização só na fronteira OpenAI. 🟢
   - Origem: ADR-009
   - Tipo: confirmada

## 5. Requisitos Funcionais — checklist legado 🟢

| ID | Item | Regra domínio | Saída |
|----|------|---------------|-------|
| RF-01 | 0 | R-P1 professor presente no bloco | PROBLEMA |
| RF-02 | 1 | R-SEM máx. 3 aval/semana | PROBLEMA |
| RF-03 | 2 | R-G1 grupo 1 (exceção Inglês) | PROBLEMA |
| RF-04 | 3 | R-DIA uma prova/dia | PROBLEMA |
| RF-05 | 4 | Período, feriados, semana vetada | PROBLEMA |
| RF-06 | 5, 5a, 5a-bis, 5b, 5c | Contagem provas, distância, LP/LIT/RED, simulados | PROBLEMA |
| RF-07 | 6, 7, 7c | 1 tempo, disciplinas sem prova, veto doador 1 aula | PROBLEMA |
| RF-08 | 7b | Prova tarde 7–11 com opção manhã | **AVISO** (P3) |
| RF-09 | 8 | Simulados datas oficiais | PROBLEMA |
| RF-10 | 9 | R-INT intervalo recreio | PROBLEMA |
| RF-11 | 10 | R-FIX `FORCAR_DATA` | PROBLEMA |
| RF-12 | 10b | Cessão C1–C5 (só Proposta 3) | PROBLEMA / AVISO |
| RF-13 | 11 | R-IRM professor comum irmãs (+ exceção Fil/Soc) | PROBLEMA |

## 6. Requisitos Funcionais — plataforma 🟡

| ID | Requisito | Prioridade | Critério de aceite | Confiança |
|----|-----------|------------|--------------------|-------------|
| RF-14 | API `GET .../verification` retorna JSON estruturado | Must | Lista `{item, turma, severidade, mensagem, regra_id}` | 🟡 |
| RF-15 | Re-executar verificação após refração/copilot apply | Must | Idempotente; atualiza painel e RAG | 🟡 |
| RF-16 | Bloquear "Fechar horário" se `problemas.length > 0` | Must | UI + API retornam 409 | 🟡 |
| RF-17 | Exportar mesmo texto legado (stdout) para log/auditoria | Should | Paridade com CLI | 🟢 |
| RF-18 | Alimentar copiloto via tool `get_verification_report` | Must | Backend deanonymize antes UI | 🟢 |

## 7. Requisitos Não Funcionais

| Tipo | Requisito | Evidência | Confiança |
|------|-----------|-----------|-------------|
| Confiabilidade | Independente do gerador (releitura) | ADR-002 | 🟢 |
| Performance | Full scan 8 turmas × 20 semanas | CLI atual aceitável | 🟡 |
| Consistência | Importa constantes/funções de `gerar_calendario as G` | Legado acoplado | 🟢 |
| Privacidade | Siglas reais na UI; tokens só OpenAI | ADR-009 | 🟢 |

## 8. Critérios de Aceitação

```gherkin
Cenário: Calendário válido
  Dado Proposta_3 xlsx gerada e sem edição inválida
  Quando o coordenador executa verificação
  Então o resultado é OK
  E avisos podem existir sem impedir fechamento 🟡

Cenário: Falha professor presente
  Dado célula com prova sem professor no bloco (item 0)
  Quando verificação roda
  Então existe PROBLEMA citando turma/semana/disciplina
  E fechar horário é bloqueado

Cenário: Aviso tarde Proposta 3
  Dado prova no 8º tempo com slot manhã disponível na grade
  Quando verificação roda na Proposta 3
  Então gera AVISO item 7b, não PROBLEMA

Cenário: Copiloto explica falha
  Dado verificação com PROBLEMA item 10b
  Quando coordenador pergunta no chat copiloto
  Então resposta cita sigla real do professor e regra C4 🟡
```

## 9. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 a RF-13 | Must | Paridade checklist legado |
| RF-14, RF-15, RF-16, RF-18 | Must | Plataforma + copiloto |
| RF-17 | Should | Auditoria |
| RuleSetSnapshot no verificador | Should | Alinhamento seleção regras |

## 10. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 11. Lacunas

- 🔴 `FERIADOS` vs `BLOQUEIOS` dessincronizados
- 🟢 ENEM — Must checklist automático quando `EnemWeekConfig` persistido (ADR-015)
- 🟢 R-2CH / véspera 2CH — Won't automático; item manual skill (ADR-015)
- 🟡 Item 10b AVISO vs PROBLEMA quando cessão relaxada

## 12. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-16 | Versão inicial — Redator | reversa-writer |
