# Requirements: Geração de Calendário

> Identificador: `001-geracao-calendario`
> Data: `2026-08-15`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

A feature **geracao-calendario** produz automaticamente a Proposta 3 do calendário de provas por turma, respeitando grade horária, simulados fixos, coordenação entre turmas irmãs e limites de cessão de tempo. Atende o coordenador que hoje executa `gerar_calendario.py` no terminal e, na plataforma futura, dispara a **fatoração** após selecionar quais regras aplicar e quais podem flexibilizar.

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confiança |
|-------|------------------|-------------|
| `_reversa_sdd/code-analysis.md#Módulo: geracao-calendario` | Pipeline `montar_proposta` → backtracking por par/turma → relaxamento regra 4→3→folga | 🟢 |
| `_reversa_sdd/domain.md#Regras de domínio — distribuição` | R-P1, R-SEM, R-G1, R-DIST, cessões C1–C5 | 🟢 |
| `_reversa_sdd/flowcharts/geracao-calendario.md` | Fluxo Mermaid do solver e escada de relaxamento | 🟢 |
| `_reversa_sdd/adrs/001-apenas-proposta-3-cessao.md` | Apenas Proposta 3 é gerada e mantida | 🟢 |
| `_reversa_sdd/architecture.md#Arquitetura legada (as-is)` | CLI monolítico openpyxl, seed fixa | 🟢 |
| `.reversa/context/user-requirements.md#Seleção e flexibilização de regras` | RuleSetSnapshot configurável | 🟡 |
| `.reversa/context/user-requirements.md#Copiloto de IA` | OpenAI + RAG + ações Python | 🟢 |
| `.reversa/context/user-requirements.md#Catálogo de provas` | ExamCatalog sem modelo obrigatório | 🟢 |
| `_reversa_sdd/adrs/010-catalogo-provas-sem-modelo-obrigatorio.md` | ADR catálogo | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador (legado) | Gerar Proposta 3 para o semestre | Executa `python gerar_calendario.py` após atualizar grade e modelo xlsx |
| Coordenador (plataforma) | Fatorar horário com regras escolhidas | Seleciona regras nas Telas 1–2, inicia solver, revisa xlsx e relatório de trocas |
| Sistema (batch) | Reexecutar geração após mudança de entrada | Nova rodada com mesma seed ou seed alternativa se falhar |

## 4. Regras de negócio novas ou alteradas

1. **RN-01:** O solver usa **exclusivamente** o conjunto de regras marcadas como "aplicar" na sessão (Tela 1 + Tela 2). 🟡
   - Origem no legado: `.reversa/context/user-requirements.md#Durante fatoração e refração`
   - Tipo: nova (plataforma)
2. **RN-02:** Relaxamentos automáticos (escada externa regra 4→3→folga e escada interna intervalo→tarde→grupo 1) só ocorrem em regras marcadas "pode flexibilizar". 🟡
   - Origem no legado: `_reversa_sdd/domain.md#Cessão de aula (Proposta 3)` + requisito usuário
   - Tipo: alterada (comportamento hoje incondicional no legado)
3. **RN-03:** Regras inegociáveis (R-P1 professor presente, R-FIX simulados/datas forçadas) permanecem sempre ativas; flexibilização bloqueada por padrão. 🟢
   - Origem no legado: `_reversa_sdd/domain.md#Prioridade e invioláveis`
   - Tipo: confirmada
4. **RN-04:** Apenas **Proposta 3** é produzida; Propostas 1 e 2 não fazem parte do escopo. 🟢
   - Origem no legado: `_reversa_sdd/adrs/001-apenas-proposta-3-cessao.md`
   - Tipo: confirmada
5. **RN-05:** Saída inclui planilha `Proposta_3_<semestre>.xlsx` e relatório markdown de trocas de tempo. 🟢
   - Origem no legado: `_reversa_sdd/code-analysis.md#Módulo: geracao-calendario`
   - Tipo: confirmada
6. **RN-06:** Re-fatoração parcial (subconjunto de turmas / nova seed) pode ser acionada via API — inclusive pelo **copiloto** — respeitando `RuleSetSnapshot`. 🟡
   - Origem: `.reversa/context/user-requirements.md#Copiloto de IA`
   - Tipo: nova (plataforma)
7. **RN-07:** Após fatoração e verificação, o **copiloto OpenAI** (RAG sobre documentos + xlsx gerado) responde perguntas e orienta refração **junto** do coordenador. 🟢
   - Origem: requisito usuário 2026-08-15; ADR-008
   - Tipo: nova (plataforma)
8. **RN-08:** Alterações solicitadas ao copiloto executam **ações Python** whitelist no backend (`PythonActionBridge`), com preview e confirmação humana — sem código arbitrário. 🟢
   - Origem: requisito usuário 2026-08-15
   - Tipo: nova (plataforma)
9. **RN-09:** Modelo Klausurplan xlsx **não** é entrada obrigatória na plataforma; o **catálogo de provas** (turma, disciplina, n_tempos) pode vir de import anterior, tabela manual ou derivação da grade. 🟢
   - Origem: requisito usuário 2026-08-16; ADR-010
   - Tipo: nova (plataforma)

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério de aceite | Confidência |
|----|-----------|------------|--------------------|-------------|
| RF-01 | Carregar ocupação prévia e simulados do modelo xlsx | Must | Células amarelas/simulados refletidas antes do backtracking | 🟢 |
| RF-02 | Montar lista de exames por turma a partir da grade (`montar_exames`) | Must | Cada disciplina elegível vira exame com `n_tempos` e período corretos | 🟢 |
| RF-03 | Resolver turmas irmãs em pares (`resolver_par`) antes das demais | Must | Pares derivados de regex série+letra+número; coordenação simultânea quando aplicável | 🟢 |
| RF-04 | Backtracking por turma com heurística MRV e preferências (intervalo, tarde, G1, doador) | Must | Alocação `(w,d,t,n,disc,prof,doador)` válida ou falha explícita | 🟢 |
| RF-05 | Aplicar limites de cessão via classe `Cessoes` (regras C1–C5) | Must | Contadores por turma respeitam teto 11% e regras semanais | 🟢 |
| RF-06 | Escada de relaxamento externa: regra 4 → regra 3 → `folga_extra` (até 12 iterações) | Must | Loop documentado em `montar_proposta`; falha reporta turmas não resolvidas | 🟢 |
| RF-07 | Usar seed configurável; legado fixa `SEED_PROPOSTA_3=3` | Should | Mesma seed + mesmas entradas → mesma alocação (determinismo observado) | 🟢 |
| RF-08 | Gravar xlsx final via `escrever(3, alocacoes)` | Must | Arquivo abre no modelo esperado; uma aba por turma | 🟢 |
| RF-09 | Emitir relatório de trocas (`relatorio`) | Must | Lista cessões com doador, solicitante, data e tempo | 🟢 |
| RF-10 | Respeitar `FORCAR_DATA` e bloqueios de feriado/semana | Must | Datas bloqueadas não recebem provas móveis | 🟢 |
| RF-11 | Integrar perfil de regras da sessão (plataforma) | Should | API recebe `RuleSetSnapshot` antes de invocar solver | 🟡 |
| RF-12 | Registrar turmas que falharam após esgotar relaxamentos | Must | Lista `falharam` retornada/consumida pela UI | 🟢 |
| RF-13 | Expor re-fatoração parcial via API (turmas subset, seed) | Should | Endpoint invocável pelo copiloto | 🟡 |
| RF-14 | Disponibilizar snapshot do calendário gerado para contexto do copiloto | Must | API retorna alocações + metadados pós-`escrever` | 🟡 |
| RF-15 | Aceitar `ExamCatalog` via import de prova anterior | Must | Parser → preview → persistência | 🟡 |
| RF-16 | UI `ExamCatalogEditor`: turma, disciplina, n_tempos | Must | CRUD + validação básica | 🟡 |
| RF-17 | Alternativa `montar_exames()` derivar catálogo da grade | Should | Paridade legado modo C | 🟢 |
| RF-18 | Gerar malha xlsx saída sem Klausurplan de entrada | Should | Template institucional vazio | 🟡 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência ou justificativa | Confidência |
|------|-----------|----------------------------|-------------|
| Desempenho | Limitar exploração do backtracking (`MAX_NOS=60000`, `MAX_NOS_CESSAO=5000`) | Constantes em `gerar_calendario.py` | 🟢 |
| Confiabilidade | Falha parcial não corrompe xlsx parcial — só grava após sucesso global ou política explícita | Comportamento `main()` legado | 🟡 |
| Observabilidade | Log de iterações de relaxamento e turmas falhadas | stdout legado; métricas na plataforma 🟡 | 🟡 |
| Portabilidade | Manter núcleo em Python reutilizável por CLI e FastAPI | ADR stack FastAPI | 🟡 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Geração bem-sucedida da Proposta 3
  Dado grade horária, modelo xlsx e simulados válidos para o semestre
  E o conjunto de regras com todas as regras obrigatórias marcadas como "aplicar"
  Quando o coordenador dispara a fatoração com seed 3
  Então o sistema produz Proposta_3_<semestre>.xlsx
  E produz relatório de trocas com todas as cessões registradas
  E nenhuma turma aparece na lista de falhas

Cenário: Relaxamento de cessão quando solver não fecha
  Dado turmas onde o backtracking falha sem relaxar regra C4
  E a regra C4 está marcada como "pode flexibilizar"
  Quando o solver executa a escada externa
  Então a regra C4 é relaxada antes de C3 e folga_extra
  E a geração conclui ou reporta turmas ainda inviáveis

Cenário: Regra inegociável bloqueada
  Dado R-P1 (professor presente) sempre ativa e sem flexibilização
  Quando o solver tenta alocar prova sem professor no bloco
  Então a alocação é rejeitada
  E o relaxamento automático não desativa R-P1

Cenário: Falha após esgotar relaxamentos
  Dado entradas incompatíveis mesmo após 12 iterações de relaxamento
  Quando montar_proposta termina
  Então turmas não resolvidas constam em falharam
  E o coordenador recebe mensagem acionável (sem xlsx final inválido)
```

## 8. Prioridade MoSCoW

| Item | MoSCoW | Justificativa |
|------|--------|---------------|
| RF-01 a RF-06, RF-08 a RF-10, RF-12 | Must | Caminho crítico do legado; sem isso não há calendário |
| RF-07 | Should | Reprodutibilidade operacional já usada (seed 3) |
| RF-11 | Should | Requisito de plataforma; não existe no CLI atual |
| RNF desempenho (limites de nós) | Must | Evita travamento em backtracking |
| Integração RuleSetSnapshot | Should | Depende de feature `regras-negocio` |

## 9. Esclarecimentos

> Nenhuma sessão de dúvidas registrada ainda. Rode `/reversa-clarify` quando houver `[DÚVIDA]` pendente.

## 10. Lacunas

- 🔴 Regras ENEM e véspera 2CH descritas na skill mas não implementadas no gerador — escopo desta feature ou de `regras-negocio`?
- 🟡 Sincronização `FERIADOS` vs `BLOQUEIOS` — risco de divergência gerador/verificador
- 🟡 Política de gravação parcial quando apenas algumas turmas falham na plataforma

## 11. Histórico de alterações

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-15 | Versão inicial gerada pelo Redator (Reversa) | reversa-writer |
