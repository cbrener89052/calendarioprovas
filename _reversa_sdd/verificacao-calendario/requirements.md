# Requirements: Verificação de Calendário

> Identificador: `002-verificacao-calendario`  
> Data: `2026-08-09`  
> Confidência: 🟢 / 🟡 / 🔴

## 1. Resumo executivo

Valida planilhas xlsx de calendário geradas contra checklist de ~30 regras espelhando a skill `calendario-provas`. Produz relatório de problemas por turma com severidade (erro/aviso). É o gate de qualidade pós-geração antes de publicar o calendário.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confidência |
|-------|------------------|-------------|
| `_reversa_sdd/domain.md#entregáveis` | Verificação obrigatória pós-geração | 🟢 |
| `_reversa_sdd/code-analysis.md#verificacao-calendario` | 11+ checks automáticos | 🟢 |
| `_reversa_sdd/flowcharts/verificacao-calendario.md` | Lê xlsx gravado, não memória | 🟢 |
| `_reversa_sdd/addenda/pr14-lp-lit-red-10dias-conselho.md` | Check 10 dias — 🔴 ausente | 🔴 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador | Confirmar calendário antes de divulgar | Roda verificador após gerar xlsx |
| Pipeline plataforma | Gate automático pós-job | API chama verificador; bloqueia publish se erro |
| IA assistente | Diagnosticar violações | Interpreta stdout/lista ProblemaValidacao |

## 4. Regras de negócio

1. **RN-01:** Checklist espelha skill calendario-provas (~30 itens) 🟢
2. **RN-02:** Cessão antes ou no dia da prova = **falha**, mesmo com regra 4 relaxada 🟢
3. **RN-03:** Regra 4 relaxada documentada = **aviso**, não erro 🟢
4. **RN-04:** Verificador opera sobre **arquivo xlsx**, não estado do gerador 🟢
5. **RN-05:** LP/LIT/RED ≥10 dias antes conselho — must quando implementado 🔴

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Ler xlsx gerado (8 abas) | Must | Parse correto de datas, disciplinas, tempos | 🟢 |
| RF-02 | Validar máx. 3 avaliações/semana | Must | Erro se 4+ na mesma semana | 🟢 |
| RF-03 | Validar 1 prova/dia | Must | Erro se 2+ provas normais no mesmo dia | 🟢 |
| RF-04 | Validar distância 4 semanas entre mesma disciplina | Must | Erro se <4 semanas | 🟢 |
| RF-05 | Validar cessões vs grade-base | Must | Detecta tempo de outra disciplina usado | 🟢 |
| RF-06 | Validar simulados (2º–7º tempo, datas fixas) | Must | Erro se fora do slot esperado | 🟢 |
| RF-07 | Emitir ProblemaValidacao (turma, regra, msg, severidade) | Must | Lista agrupada por turma | 🟢 |
| RF-08 | Check LP/LIT/RED 10 dias conselho | Must | Erro se violação; **bloqueia publish** | 🔴 código; 🟢 Must |
| RF-09 | Validar cores ARGB (destaque laranja recreio) | Could | Aviso se skill pede e cor ausente | 🔴 |
| RF-10 | Endpoint automático pós-job (plataforma) | Should | 422 se erros críticos | 🟡 |
| RF-11 | Checks IA a partir de CUSTOMIZACAO_IA | Must | Avisos interpretados por IA; não substituem checks codificados | 🟢 |
| RF-12 | Relatório auxiliar IA pós-verificação | Must | Documenta preferências/exceções do segmento | 🟢 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência | Confiança |
|------|-----------|-----------|-----------|
| Acoplamento | Importa `gerar_calendario` para constantes | `verificar_calendario.py` | 🟢 |
| Desempenho | Batch síncrono CLI | Sem async no legado | 🟢 |
| Segurança | Sem auth no CLI | N/A legado | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Calendário válido
  Dado xlsx gerado por Proposta 3 sem violações
  Quando verificar_calendario.py é executado
  Então exit code 0 e nenhum erro crítico

Cenário: Violação cessão véspera
  Dado prova de História na terça e cessão de História na segunda
  Quando verificador analisa a turma
  Então emite erro severidade crítica independente de regra 4 relaxada

Cenário: Regra relaxada documentada
  Dado calendário com regra 3 relaxada conforme relatório gerador
  Quando verificador encontra gap de 2 semanas sem contato
  Então emite aviso, não erro

Cenário: Check IA por customização
  Dado customização IA "evitar provas Geo às segundas" ativa no segmento
  Quando verificador conclui checks codificados
  Então camada IA emite aviso se prova Geo cair em segunda
  E relatório auxiliar lista a preferência avaliada
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01–RF-07 | Must | Gate de qualidade |
| RF-08 | Must | PR #14 |
| Desacoplar import gerador | Should | Manutenção plataforma |
| RF-09 cores | Could | Lacuna conhecida |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda.

## 10. Lacunas

- 🟡 Check LP/LIT/RED 10 dias — Must deploy; Claude agendado
- 🔴 Validação ARGB de cores

## 11. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial Fase 4 | reversa-writer |
