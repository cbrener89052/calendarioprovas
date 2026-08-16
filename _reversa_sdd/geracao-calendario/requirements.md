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
| `_reversa_sdd/templates/mascara-entrada-provas-spec.md` | Colunas máscara provas + aba `provas` | 🟢 |
| `_reversa_sdd/templates/mascara-bloqueios-calendario-spec.md` | Máscara bloqueios/feriados | 🟢 |
| `_reversa_sdd/adrs/011-mascaras-estruturadas-sem-ia-recalculo.md` | Recálculo sem IA | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador (legado) | Gerar Proposta 3 para o semestre | Executa `python gerar_calendario.py` após atualizar grade e modelo xlsx |
| Coordenador (plataforma) | Alimentar catálogo via máscara padrão | Baixa `Mascara_Entrada_Provas.xlsx`, preenche disciplinas/nº provas/nº aulas semanais, faz upload |
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
10. **RN-10:** A plataforma oferece **máscara padrão de entrada** (`Mascara_Entrada_Provas.xlsx`) distinta do Klausurplan de layout; o coordenador preenche turma, disciplina, nº provas/semestre e nº tempos de aula/semana antes da fatoração. 🟢
   - Origem: requisito usuário 2026-08-16 (2); ADR-010
   - Tipo: nova (plataforma)
11. **RN-11:** O template Klausurplan no GitHub (`Klausurplan_2026_2SEM.xlsx`) é **layout institucional de saída**; não substitui a máscara de entrada nem exige upload preenchido por coordenador. 🟢
   - Origem: requisito usuário 2026-08-16 (2)
   - Tipo: confirmada (plataforma)
12. **RN-12:** Cada prova registrada no sistema **Must** ter ordem (1ª/2ª) e `n_tempos_aplicacao` explícitos — preferencialmente via aba `provas` da máscara ou grid equivalente na UI. 🟢
   - Origem: requisito usuário 2026-08-16 (3); ADR-011
   - Tipo: nova (plataforma)
13. **RN-13:** Feriados, recessos, semanas vetadas, dias bloqueados e simulados fixos **Must** ser informados via **`Mascara_Bloqueios_Calendario.xlsx`** (ou UI equivalente), não via interpretação de IA a cada recálculo. 🟢
   - Origem: requisito usuário 2026-08-16 (3); ADR-011
   - Tipo: nova (plataforma)
14. **RN-14:** Re-fatoração e recálculo do horário **Must not** invocar OpenAI para parse de entradas quando `ExamCatalog` e `CalendarConstraints` estão persistidos. 🟢
   - Origem: requisito usuário 2026-08-16 (3)
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
| RF-15 | Gerar e disponibilizar download da máscara padrão `Mascara_Entrada_Provas.xlsx` | Must | Link *"Baixe sua planilha padrão aqui"*; aba `catalogo` com cabeçalhos + linha exemplo | 🟢 |
| RF-16 | Parser upload máscara preenchida → `ExamCatalog` | Must | Valida colunas; preview; confirmação; origem `mascara` | 🟢 |
| RF-17 | UI `ExamCatalogEditor` com paridade de colunas da máscara | Must | turma, disciplina, n_provas_semestre, n_aulas_semanais, n_tempos, periodo | 🟡 |
| RF-18 | Aceitar `ExamCatalog` via import de prova anterior (modo A′) | Should | Parser layout Klausurplan → metadados provas | 🟡 |
| RF-19 | Alternativa `montar_exames()` derivar catálogo da grade (modo C) | Should | Paridade legado | 🟢 |
| RF-20 | Aplicar `CalendarLayoutTemplate` (`Klausurplan_2026_2SEM.xlsx`) na saída | Must | `escrever()` usa layout GitHub; independente de upload de entrada | 🟢 |
| RF-21 | Validar catálogo × grade (turma/disciplina, LP/LIT/RED 3 tempos, Fil=1) | Must | PROBLEMA/AVISO conforme spec máscara | 🟡 |
| RF-22 | Botão *baixar máscara vazia* também no `ExamCatalogEditor` | Should | Mesmo arquivo gerado por RF-15 | 🟡 |
| RF-23 | Aba `provas`: uma linha por prova com `ordem_prova` e `n_tempos_aplicacao` | Must | Parser → N exames em `ExamCatalog` | 🟢 |
| RF-24 | Gerar/download `Mascara_Bloqueios_Calendario.xlsx` | Must | Abas feriados, semanas_vetadas, dias_bloqueados, simulados | 🟢 |
| RF-25 | Parser upload bloqueios → `CalendarConstraints` | Must | Unifica gerador e verificador; preview calendário | 🟢 |
| RF-26 | UI `CalendarConstraintsEditor` com paridade das abas da máscara | Should | CRUD + validação | 🟡 |
| RF-27 | Fatoração/recálculo sem chamada OpenAI quando constraints persistidas | Must | Pipeline determinístico ADR-011 | 🟢 |

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

Cenário: Catálogo via máscara padrão de entrada
  Dado grade horária carregada para o semestre
  E o coordenador baixou Mascara_Entrada_Provas.xlsx e preencheu turma, disciplina, n_provas_semestre e n_aulas_semanais
  Quando faz upload e confirma o preview
  Então o sistema persiste ExamCatalog com origem mascara
  E a fatoração usa esse catálogo em vez de montar_exames() exclusivamente

Cenário: Layout Klausurplan na saída sem upload de entrada
  Dado catálogo válido e grade carregada
  E o coordenador não enviou Klausurplan preenchido do semestre
  Quando a fatoração conclui com sucesso
  Então Proposta_3_<semestre>.xlsx segue o layout institucional Klausurplan_2026_2SEM.xlsx

Cenário: Recálculo com máscaras sem consumo de IA
  Dado ExamCatalog e CalendarConstraints persistidos de uploads válidos
  Quando o coordenador dispara nova fatoração (seed ou regras alteradas)
  Então o solver executa sem invocar ScheduleCopilotService na ingestão
  E feriados/bloqueios aplicados coincidem com a máscara de bloqueios enviada

Cenário: Registro de provas por ordem na aba provas
  Dado máscara com aba provas: Mat ordem 1 e 2 com 2 tempos cada
  Quando o upload é confirmado
  Então ExamCatalog contém duas entradas (10C1, Mat) com ordem 1 e 2 e n_tempos=2
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
| 2026-08-16 | RN-10/11 e RF-15–22 — máscara padrão vs layout Klausurplan | reversa-writer |
| 2026-08-16 | RN-12–14, RF-23–27 — aba provas, máscara bloqueios, recálculo sem IA | reversa-writer |
