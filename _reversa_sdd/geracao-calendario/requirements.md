# Requirements: Geração de Calendário

> Identificador: `001-geracao-calendario`  
> Data: `2026-08-09`  
> Pasta da extração reversa: `_reversa_sdd/`  
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

Gera o calendário de provas do 2º semestre para turmas C via backtracking com cessão de tempos (Proposta 3). Entrega planilha Excel com 8 abas e relatório de trocas de tempo entre professores. Resolve alocação combinatória respeitando limites semanais, distância entre provas, simulados fixos e regras de cessão.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confiança |
|-------|------------------|-------------|
| `_reversa_sdd/domain.md#regras-de-domínio` | Máx. 3 avaliações/semana, distância 4 semanas, cessão Proposta 3 | 🟢 |
| `_reversa_sdd/code-analysis.md#geracao-calendario` | Backtracking, `Cessoes`, seed fixa 7 | 🟢 |
| `_reversa_sdd/flowcharts/geracao-calendario.md` | Fluxo main → montar_proposta → resolver → xlsx | 🟢 |
| `_reversa_sdd/adrs/002-limites-cessao-proposta-3.md` | Regras 1–5 de cessão e escada de afrouxamento | 🟢 |
| `_reversa_sdd/addenda/sync-skill-2026-08-10.md` | PR #18 implementado | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador escolar | Montar calendário de provas do semestre | Executa gerador após atualizar grade-base e modelo xlsx |
| Assistente IA (Claude/Cursor) | Regenerar proposta com parâmetros | Invoca script com flags de relaxamento |
| Worker futuro (plataforma) | Job assíncrono pós-upload | API dispara solver com `RuleContext` do segmento |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** Máximo 3 avaliações por semana por turma (simulado de 2 dias conta como 1) 🟢  
   - Origem: `_reversa_sdd/domain.md#distribuição-temporal`  
   - Tipo: confirmada (legado)

2. **RN-02:** Uma prova por dia por turma 🟢  
   - Origem: `_reversa_sdd/domain.md#distribuição-temporal`  
   - Tipo: confirmada

3. **RN-03:** Distância mínima de 4 semanas entre provas da mesma disciplina 🟢  
   - Origem: `_reversa_sdd/domain.md#distribuição-temporal`  
   - Tipo: confirmada

4. **RN-04:** Provas dentro do período do GRUPO da turma, excluindo feriados e semana vetada de conselho 🟢  
   - Origem: `_reversa_sdd/domain.md#distribuição-temporal`  
   - Tipo: alterada (antes hardcoded por “grupo de viagem”; futuro vem de GRUPO configurável — ADR-006)

5. **RN-05:** Cessão Proposta 3 — regras 1, 2 e 5 duras; 3 e 4 relaxáveis na escada de afrouxamento 🟢  
   - Origem: `_reversa_sdd/adrs/002-limites-cessao-proposta-3.md`  
   - Tipo: confirmada

6. **RN-06:** Regra 4 relaxada libera cessão somente **depois** da prova, nunca antes ou no dia 🟢  
   - Origem: `_reversa_sdd/adrs/003-regra-4-so-depois-da-prova.md`  
   - Tipo: confirmada

7. **RN-07:** LP/LIT/RED (10–12): bloco de 3 tempos na 1ª ou 2ª semana de cada rodada 🟢  
   - Origem: skill + `gerar_calendario.py`  
   - Tipo: confirmada

8. **RN-08:** LP/LIT/RED ≥10 dias corridos antes da semana vetada de conselho 🟢 (PR #18)

9. **RN-09:** Relatório de trocas deve incluir seção **Regras relaxadas** quando afrouxamento ocorrer 🟢  
   - Origem: `gerar_calendario.py:detectar_regras_relaxadas`  
   - Tipo: confirmada

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Carregar grade-base, modelo xlsx, simulados e constantes do semestre | Must | Solver inicia com dados corretos para 8 turmas C | 🟢 |
| RF-02 | Resolver pares de turmas irmãs antes das turmas individuais | Must | 10C1/10C2, 11C1/11C2 etc. alinhados quando mesmo professor | 🟢 |
| RF-03 | Backtracking com classe `Cessoes` aplicando regras 1–5 | Must | Nenhuma alocação viola teto 11% nem regra 2 (1 aula/sem) | 🟢 |
| RF-04 | Escada de afrouxamento: regra 4 → regra 3 → tetos +1 | Must | Ordem respeitada; `FORCAR_DATA` nunca relaxa | 🟢 |
| RF-05 | Gravar calendário xlsx com 8 abas (uma por turma) | Must | Arquivo abre no Excel com provas, simulados e cores esperadas | 🟢 |
| RF-06 | Gerar relatório de trocas de tempo entre professores | Must | Lista cessões com origem/destino disciplina e professor | 🟢 |
| RF-07 | Respeitar toggles de regras codificadas (plataforma futura) | Should | Regras desativadas no `RuleContext` não são aplicadas | 🟡 |
| RF-08 | Validar LP/LIT/RED ≥10 dias antes conselho | Must | `LIMITE_LPLITRED_CONSELHO=9` | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confiança |
|------|-----------|----------------------------|-------------|
| Desempenho | `MAX_NOS=60000` (sem cessão) / `MAX_NOS_CESSAO=5000` (Proposta 3); ~600 nós/s com limites de cessão | `gerar_calendario.py:657-664` | 🟢 |
| Determinismo | Semente `SEED_PROPOSTA_3 = 3` (PR #18) | `gerar_calendario.py:678` | 🟢 |
| Manutenibilidade | Constantes hardcoded (feriados, simulados, grades) | Scout + code-analysis | 🟢 |
| Escalabilidade | Job assíncrono na plataforma (futuro) | ADR-005, architecture.md | 🟡 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Geração bem-sucedida Proposta 3
  Dado grade-base e modelo xlsx válidos para 8 turmas C
  Quando o coordenador executa gerar_calendario.py
  Então é criado calendário xlsx com 8 abas
  E é criado relatório de trocas sem violações duras de cessão

Cenário: Afrouxamento com documentação
  Dado que a solução exige relaxar regra 4 para turma 11C1
  Quando montar_proposta conclui com sucesso
  Então o relatório contém seção "Regras relaxadas" citando turma e regra

Cenário: Falha por impossibilidade combinatória
  Dado restrições que impedem alocação mesmo após escada completa
  Quando o backtracking esgota MAX_NOS
  Então o processo termina com falha explícita e lista de disciplinas não alocadas

Cenário: LP/LIT/RED respeita distância do conselho
  Dado semana vetada de conselho configurada no GRUPO da turma 12C1
  Quando LP/LIT/RED é alocada na rodada P2
  Então a data da prova é ≥10 dias antes do início da semana vetada
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 a RF-06 | Must | Caminho crítico; sem isso não há calendário |
| RF-08 | Must | Regra institucional mergeada (PR #14) |
| RF-07 | Should | Necessário na plataforma, não no CLI legado |
| Externalizar constantes | Should | Pré-requisito multi-coordenador |
| Otimização MAX_NOS | Could | Funciona hoje com limite atual |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

- 🟡 Integração `RuleContext` com toggles ADR-006 — plataforma

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial gerada por `/reversa-writer` (Fase 4) | reversa-writer |
