# Requisitos declarados pelo usuário

> Registrado em 2026-08-09 por Brener, antes do Scout.

## Contexto

O sistema **calendarioprovas** hoje é um conjunto de scripts Python + planilhas/PDFs
locais, usado para montar o calendário de provas da Escola Alemã Corcovado.

## Requisito de evolução (prioritário)

O sistema será utilizado por **outros coordenadores da instituição**. Por isso,
precisa existir um **banco de dados** para armazenar:

1. **Saídas** — calendários gerados (**Excel** `Proposta_3`), relatórios, tabelas-resumo, tempos cedidos — **visualizáveis na plataforma** sem abrir o arquivo (ADR-013)
2. **Arquivos de entrada** — bases que alimentam o sistema de **cada coordenador**:
   - horário-base das turmas (PDF/planilha) — **obrigatório** para fatoração
   - **catálogo de provas** por turma: disciplina + nº de tempos (ver seção abaixo)
   - modelo de calendário xlsx (Klausurplan) — **opcional** na plataforma
   - calendário de simulados / bloqueios — **tela visual** (clique no calendário por turma/série; ver ADR-012)
   - planilha de siglas de professores
   - referências e regras do semestre

## Implicações arquiteturais (a detalhar nas specs)

- Multi-usuário / multi-coordenador (isolamento por coordenador ou por unidade?)
- Persistência centralizada substituindo (ou complementando) pastas locais
- Versionamento de entradas e saídas por semestre/rodada
- Autenticação e controle de acesso (a confirmar)
- Migração do fluxo atual (git + arquivos locais) para plataforma compartilhada

## Pendências para o usuário confirmar

- [x] Cada coordenador vê **só os seus dados** ou há templates/regras compartilhadas? → **A definir no Arquiteto** (provável: dados isolados por coordenador + templates institucionais compartilhados)
- [x] Haverá **login** (conta por coordenador) ou acesso interno da rede? → **Login individual** (5 coordenadores)
- [x] O sistema roda **na nuvem** ou **servidor da escola**? → **Nuvem como padrão**, com capacidade de rodar **localmente em servidor/on-prem** quando necessário (deploy híbrido)
- [x] Os scripts Python atuais viram **API/backend** ou reescrita completa? → **Manter Python** (evolução do código existente)

## Decisões de plataforma (2026-08-09)

| Decisão | Valor |
|---|---|
| Deploy | Nuvem + opção **self-hosted/local** (Docker) |
| Backend | **Python** (FastAPI) — reaproveitar lógica de `gerar_calendario.py` etc. |
| Usuários | **5 coordenadores**, login individual |
| Banco | **PostgreSQL** (metadados, regras, versionamento) |
| Arquivos | Storage de blobs (S3 na nuvem / pasta local no deploy on-prem) |
| Frontend | A definir na fase de design (provável web app — Next.js ou similar) |
| Copiloto IA | **OpenAI** (API) + **RAG** sobre documentos e xlsx gerado |

### Implicação do deploy híbrido

- Mesma aplicação empacotada em **Docker Compose**: API Python + Postgres + (opcional) frontend
- Na nuvem: serviços gerenciados (ex.: Vercel/Railway/Fly + Neon Postgres + S3)
- On-prem: `docker compose up` em servidor local da escola, sem dependência de internet para operação diária

---

## Catálogo de provas — modelo Klausurplan opcional

> Registrado em 2026-08-16 por Brener.  
> **Atualizado 2026-08-16 (4):** bloqueios/feriados via **tela visual**
> calendário (clique dia/semana por turma e série) — Excel descartado como
> entrada principal (ADR-012).

### Contexto

Tipos de artefato **não devem ser confundidos**:

| Tipo | O que é | Como o coordenador usa |
|------|---------|------------------------|
| **Layout Klausurplan** | Malha semanal do **calendário de saída** | Automático na Proposta 3 (GitHub) |
| **Catálogo de provas** | O que fatorar (disciplina, ordem, tempos) | UI `ExamCatalogEditor` ou máscara xlsx provas 🟡 |
| **Bloqueios / sem prova** | Dias e semanas vetados | **Tela visual `CalendarBlockPicker`** — clique no calendário 🟢 |

Preencher **tabelas Excel** para bloqueios foi **rejeitado** pelo usuário
(má experiência). A entrada de constraints é **100% visual** na plataforma.
Export xlsx de bloqueios permanece **opcional** (backup/migração legado).

O Klausurplan do 2º semestre no repositório é o **modelo de layout** usado
para **montar/escrever** o calendário de provas — não é o formulário que o
coordenador preenche com disciplinas a cada rodada.

Nem sempre o coordenador terá um Klausurplan **do semestre corrente** já
preenchido. O sistema deve oferecer uma **máscara institucional padronizada**
para alimentar o catálogo de provas.

### O que continua obrigatório 🟢

| Entrada | Motivo |
|---------|--------|
| **Grade horária** | Slots, professor presente (R-P1), cessões, doadores |
| **Catálogo de provas** | O que fatorar: turma + disciplina + `n_tempos` |
| **Regras da rodada** | RuleSetSnapshot (Telas 1–2) |
| **Simulados / bloqueios** | Datas fixas e dias/semanas vetadas | **`CalendarBlockPicker`** (visual) 🟢 |

### Princípio: recálculo sem IA (Must) 🟢

Máscaras/UI estruturadas definem **limites e provas** antes da fatoração.
**Recalcular** o horário **Must not** invocar OpenAI — `ExamCatalog` +
`CalendarConstraints` (salvos na tela visual) alimentam o solver diretamente.

O **copiloto** permanece opcional para refração, diagnóstico e perguntas
**após** geração — não substitui as máscaras na ingestão (ADR-011).

### O que deixa de ser obrigatório 🟡

| Entrada | Plataforma |
|---------|------------|
| Modelo Klausurplan xlsx **preenchido** do semestre | **Opcional** — layout institucional sim; dados no catálogo |
| Klausurplan como **layout de saída** | **Sim** — template `Klausurplan_2026_2SEM.xlsx` (GitHub) 🟢 |

### Máscara padrão de provas — download (Must) 🟢

A plataforma disponibiliza **`Mascara_Entrada_Provas.xlsx`**
com link **"Baixe planilha de provas"**. Duas abas:

| Aba | Conteúdo |
|-----|----------|
| `catalogo` | Resumo: turma, disciplina, nº provas/semestre, nº aulas/semana |
| `provas` | **Uma linha por prova:** ordem (1ª/2ª), nº tempos de aplicação, nº aulas/semana |

Colunas mínimas da aba **`provas`** (preferencial):

| Coluna | Significado |
|--------|-------------|
| **Turma** | ex.: `10C1` |
| **Disciplina** | ex.: Mat, LP/LIT/RED |
| **Ordem da prova** | 1, 2, … |
| **Nº tempos da prova** | Duração em tempos de aula (1–3) |
| **Nº tempos de aula/semana** | Carga semanal na grade |

Especificação: `_reversa_sdd/templates/mascara-entrada-provas-spec.md`.

### Bloqueios e calendário — tela visual (Must) 🟢

**Pré-requisito:** antes da fatoração, o coordenador define onde **não pode
haver prova** usando a tela **`CalendarBlockPicker`** — malha de calendário
(no formato Klausurplan), **sem planilha Excel**.

| Interação | Efeito |
|-----------|--------|
| **Clicar em um dia** | Marca/desmarca “sem prova” para a turma ou série selecionada |
| **Clicar em uma semana** | Marca/desmarca **semana inteira** sem prova |
| **Seletor por série** | ex.: série **10** → bloqueio vale para 10C1 e 10C2 |
| **Seletor por turma** | ex.: **11C1** → bloqueio só naquela turma |

Feriados institucionais podem aparecer **pré-marcados** no grid. Simulados
fixos usam indicador visual distinto (★) na mesma malha ou painel adjacente 🟡.

Fluxo:

```
Abrir calendário visual → escolher série ou turma → clicar dias/semanas
  → Salvar → CalendarConstraints → fatoração (sem IA)
```

Especificação UI: `_reversa_sdd/ui/calendar-block-picker-spec.md` (ADR-012).

Export xlsx (`Mascara_Bloqueios_Calendario.xlsx`) — **opcional** (backup,
seed legado 2SEM 2026); **não** é o fluxo principal.

### Máscara de layout Klausurplan (institucional) 🟢

- **Fonte viva:** `Klausurplan_2026_2SEM.xlsx` (raiz do repo GitHub).
- Papel: estrutura visual/semanal onde `escrever()` grava a Proposta 3.
- Mantida como **template institucional** — não exige upload por coordenador
  se o sistema aplicar layout automaticamente na saída.
- Referências: `Horario modelo/Klausurplan_2026_1SEM.xlsx`,
  `provas2sem_2025/Klausurplan_ramoC_2025_2SEM.xlsx`.

### Três formas de montar o catálogo de provas (Must)

O coordenador escolhe **uma ou combina** (com merge validado):

#### Modo A — Upload da máscara padrão preenchida (Must — preferencial)

- Coordenador baixa **`Mascara_Entrada_Provas.xlsx`**, preenche disciplinas,
  nº provas/semestre e nº tempos de aula/semana, e faz upload.
- Parser valida e converte → `ExamCatalog`.
- Preview antes de confirmar.

#### Modo A′ — Importar xlsx de referência (semestre anterior)

- Upload de planilha histórica (ex.: calendário já usado no 2º sem).
- Parser tenta extrair catálogo; se formato = layout Klausurplan, extrair
  só metadados de provas 🟡.

#### Modo B — Tabela manual na interface (Must)

Tela **`ExamCatalogEditor`** — mesmas colunas da máscara padrão:

| Coluna | Tipo | Obrigatório |
|--------|------|-------------|
| Turma / grupo | `10C1`, `11C2`, … | sim |
| Disciplina | Mat, LP/LIT/RED, … | sim |
| Nº provas no semestre | 1 ou 2 (…) | sim |
| Nº tempos de aula/semana | inteiro | sim |
| Nº tempos por prova | 1, 2 ou 3 | não — default skill |
| Período | 1, 2 ou único | não 🟡 |
| Professor | sigla(s) | não — default grade 🟡 |

Ações: adicionar linha, duplicar turma, **baixar máscara vazia**, validar.

#### Modo C — Derivar da grade (legado)

- Equivalente a `montar_exames(turma)` no `gerar_calendario.py`.
- Útil quando não há import nem tabela manual; regras da skill definem
  quantas provas e tempos por disciplina.

### Fluxo na plataforma (atualizado)

```
Grade horária (upload)
  → Provas: ExamCatalogEditor ou máscara xlsx (opcional)
  → Bloqueios: CalendarBlockPicker (clique dia/semana por turma/série)
  → Layout Klausurplan institucional na saída
  → Telas 1–2 regras
  → Fatoração → Proposta_3 xlsx (sem OpenAI na ingestão)
  → Visualização in-app (CalendarPreviewView) + download Excel
```

---

## Saída Excel e visualização in-app

> Registrado em 2026-08-16 por Brener. ADR-013.

### Saída oficial — Excel (Must) 🟢

A **saída permanece Excel**, como no legado:

| Arquivo | Papel |
|---------|-------|
| `Proposta_3_<semestre>.xlsx` | Calendário de provas — layout Klausurplan institucional |
| Relatório de trocas / exports | Derivados do xlsx gravado (ADR-002) |

`escrever()` + blob storage; botão **Baixar Excel** na plataforma.

### Visualização na tela (Must) 🟢

O coordenador **Must** poder **ver o horário/calendário das turmas na
plataforma** — **sem abrir o Excel**:

| View | Conteúdo | Modo |
|------|----------|------|
| **`CalendarPreviewView`** | Malha Klausurplan com provas alocadas (por turma) | Read-only |
| Aba **grade horária** 🟡 | Slots semanais de aula da turma | Read-only |

- Seletor de turma (9C1 … 12C2) — equivalente às abas do xlsx.
- Conteúdo **Must** ser paridade com o Excel baixável (mesmo parse/blob).
- Edição manual → `CalendarEditor`; preview atualiza após refração.

Spec: `_reversa_sdd/ui/calendar-preview-view-spec.md`.

```
Fatoração → grava Proposta_3.xlsx
  → CalendarPreviewView (browser)
  → Baixar Excel (distribuição / arquivo oficial)
```

### Validações (Must)

- Disciplina do catálogo deve existir na grade da turma (ou AVISO 🟡).
- `n_tempos` coerente com disciplina (ex.: LP/LIT/RED → 3 nas séries 10–12).
- Turmas irmãs: catálogo consistente onde coordenação exige 🟡.

### Implicações

- Entidade **`ExamCatalog`** / `catalogo_prova` no PostgreSQL.
- `CalendarSolver` recebe catálogo normalizado, não só `montar_exames()`.
- **`CalendarBlockPicker`** — UI visual bloqueios (primário; ADR-012).
- **`CalendarConstraintsService`** — persiste cliques → solver/verificador.
- **`IntakeTemplateService`** — máscara provas (opcional) + export bloqueios (backup).
- ADR-010 … ADR-013 + specs em `_reversa_sdd/ui/` e `templates/`.
- **`CalendarPreviewView`** + **`CalendarViewsService`** — preview read-only pós-geração.

### Pendências 🔴

- [x] Bloqueios — tela visual por turma/série (ADR-012) 🟢
- [x] Formato máscara provas — spec + aba `provas` 🟡 validar com coordenação
- Export xlsx bloqueios — backup legado 2SEM 2026 (opcional)
- Merge quando coordenador usa upload + edição manual
- Simulados sem Klausurplan preenchido: tela dedicada ou import PDF `SIMULADOS/`

---

## Seleção e flexibilização de regras antes de gerar/refinar o horário

> Registrado em 2026-08-15 por Brener, durante retomada do `/reversa`.

### Contexto

Hoje as regras de montagem do calendário estão descritas na skill
`calendario-provas` e hardcoded no gerador (`gerar_calendario.py`,
`verificar_calendario.py`). Propostas diferentes (1, 2, 3) aplicam
conjuntos distintos — ex.: limites de cessão só na Proposta 3.

Na plataforma futura, **antes de iniciar a fatoração ou a refração do
horário**, o coordenador deve poder escolher explicitamente quais regras
usar e quais podem ser flexibilizadas.

### Fluxo de telas desejado

#### Tela 1 — Regras existentes (catálogo da skill)

- Listar as regras já descritas na skill / no domínio do sistema.
- **Default na 1ª execução:** após apresentar a tela ao usuário, todas as
  regras vêm **marcadas como aplicar**; o coordenador desmarca o que não
  quiser usar nesta rodada.
- Para cada regra, o usuário marca:
  - **Aplicar** — entra no conjunto desta rodada.
  - **Pode flexibilizar** — o solver/checklist pode relaxar esta regra
    (na ordem de afrouxamento documentada na skill, quando aplicável).
- Regras **inegociáveis** (ex.: presença do professor, simulados fixos)
  aparecem **na mesma tela**, junto com as demais — o sistema pergunta
  explicitamente sobre elas; por padrão ficam aplicadas e **sem** opção de
  flexibilizar (bloqueadas), salvo decisão explícita futura do produto.
- Regras não marcadas como "aplicar" ficam **fora** desta rodada.

#### Tela 2 — Regras novas (opcional)

- Perguntar: *"Deseja estabelecer alguma regra adicional?"*
- Para **cada** regra nova informada, em seguida perguntar:
  - **Fixa** — persiste no perfil do coordenador / instituição para
    rodadas futuras.
  - **Somente nesta fatoração/refração** — vale só para a sessão atual.

#### Durante fatoração e refração

- O solver e o verificador usam **exatamente** o conjunto de regras
  definido nas telas 1 e 2.
- Relaxamentos automáticos respeitam apenas regras marcadas como
  "pode flexibilizar".

#### Gate antes de fechar o horário

Antes de **fechar** (aprovar / publicar) o calendário, o sistema deve
permitir **revisar e ajustar** o conjunto de regras:

- marcar ou desmarcar regras existentes;
- incluir regras novas;
- confirmar se mantém o perfil de regras ou altera para esta entrega.

### Terminologia confirmada (2026-08-15)

| Termo | Significado |
|---|---|
| **Fatoração** | Geração automática do horário (solver / proposta) |
| **Refração** | Refinamento ou reajuste do horário já gerado |
| **Fechar horário** | Aprovar a versão final para entrega / produção (ex.: publicar na `main`) |

### Implicações para specs e arquitetura

- **Catálogo de regras** versionado (origem: skill + regras custom do
  coordenador), com metadados: id, descrição, prioridade, ordem de
  relaxamento, se é institucional ou por sessão.
- **Perfil de regras por rodada** persistido (PostgreSQL) ligado ao
  calendário / proposta gerada — rastreabilidade do que foi aplicado.
- **Verificador** deve distinguir **falha** (regra aplicada e violada)
  de **aviso** (regra flexibilizada e relaxada), alinhado ao que a skill
  já exige para cessão.
- Regras inegociáveis entram na **Tela 1** com flexibilização bloqueada
  por padrão (ver fluxo acima).

### Pendências

- [x] Confirmar significado exato de *refração* vs *fatoração*
- [x] Confirmar se "fechar horário" = publicar na `main` / entregar à escola
- [x] Definir defaults na 1ª execução (todas as regras ativas após pergunta)
- [ ] Definir se perfil de regras é por coordenador, por semestre ou ambos

---

## Copiloto de IA — agente analista do horário

> Registrado em 2026-08-15 por Brener.  
> **Atualizado 2026-08-15:** papel de **copiloto analista** pós-geração
> (experiência equivalente ao uso da skill no Cursor / Claude Code).  
> **Atualizado 2026-08-15 (2):** provedor **OpenAI**, grounding **RAG**
> (documentos + xlsx gerado), orquestração de **ações Python** no backend
> para refração/refatoração conforme solicitações do coordenador.

### Contexto

Hoje o coordenador monta o calendário com scripts locais e apoio de um
**agente de IA externo** (Cursor, Claude Code) que lê a skill
`calendario-provas`, os **documentos de base** enviados (grade, modelo,
simulados, siglas, referências) e o **horário gerado**, respondendo
perguntas, cruzando estatísticas e sugerindo ajustes.

Na plataforma futura, esse papel deve existir **embutido**: após a
**análise das entradas** e a **geração do horário** (fatoração), o
coordenador acessa um **chat copiloto** conectado via API a um agente
de IA que:

- **responde perguntas** sobre o calendário produzido;
- **analisa** documentos de base **e** saídas geradas (planilha, checklist
  do verificador, relatório de trocas, visões estatísticas);
- **sugere alterações** com base em inteligência e estatísticas — como
  analista, não como substituto do coordenador;
- apoia a **refração e refatoração** do horário conforme solicitações do
  coordenador, orientando **comandos executados pelo backend Python**
  (solver, patch de alocação, re-verificação) — sempre em parceria com o
  humano, nunca autonomia total.

O agente **não substitui** solver, verificador nem fechamento do horário.

### Decisões confirmadas (2026-08-15)

| Decisão | Valor |
|---|---|
| Provedor LLM | **OpenAI** (API oficial; modelo específico 🟡 a definir na implementação) |
| Grounding | **RAG** sobre documentos de base **e** xlsx gerado (Proposta + derivados) |
| Papel | **Copiloto** — trabalha **junto** do coordenador na solução de problemas |
| Execução de alterações | Backend **Python** (FastAPI) via ações estruturadas / tool-calling — **não** `eval` arbitrário no servidor |
| Confirmação humana | Must antes de aplicar alteração no calendário persistido |

O copiloto **reanalisa** o horário a cada turno relevante usando RAG +
estado atual + resultado do verificador, para orientar próximos passos.

### Quando o copiloto fica disponível

| Momento | Disponível? | Capacidades |
|---|---|---|
| Antes de subir entradas mínimas | Não | — |
| Entradas carregadas, sem proposta | Opcional 🟡 | Perguntas sobre grade/modelo/regras |
| **Após fatoração (PropostaGerada)** | **Sim — Must** | Q&A, estatísticas, explicações |
| **Após verificação** | **Sim — Must** | Explicar PROBLEMA/AVISO, priorizar correções |
| **Durante refração (EmRefracao)** | **Sim — Must** | Q&A + propostas de alteração |
| Após fechar horário | Should | Consulta read-only + comparativos 🟡 |

### Comportamento desejado

#### 1. Modo analista (perguntas e respostas) — Must

O coordenador faz perguntas em linguagem natural; o agente responde com
base em **evidências rastreáveis** (cita turma/semana/regra/arquivo):

- distribuição de provas por turma, semana, professor;
- cessões e doadores; carga semanal; distâncias entre provas;
- comparação entre turmas irmãs; simulados e datas fixas;
- o que o **verificador** apontou e **por quê**;
- cruzamento com **documentos de base** (ex.: grade vs alocação gerada).

Respostas devem distinguir 🟢 fato extraído dos dados vs 🟡 inferência.

#### 2. Modo copiloto de refração / refatoração — Must

Quando o coordenador pede mudanças ou pede ajuda para resolver um problema
("mova Biologia da semana 9 para 10", "corrija item 10b da turma 10C2",
"refatore só as turmas irmãs 12C"), o copiloto:

- reanalisa **RAG + xlsx gerado + verificador + estatísticas**;
- explica o diagnóstico e o plano em linguagem natural;
- propõe **ações estruturadas** mapeadas para o **backend Python**
  (equivalentes operacionais aos scripts legados `gerar_calendario.py`,
  `verificar_calendario.py`, patch de células);
- pode exibir ao coordenador a **equivalência legível** do comando Python
  que será executado (transparência), sem expor execução livre de código;
- devolve **preview / diff** antes de persistir;
- o coordenador **confirma** — copiloto e coordenador trabalham **juntos**;
- após aceite, backend executa, atualiza xlsx e dispara **re-verificação**.

#### 3. RAG — documentos e xlsx gerado — Must

Índice RAG **por calendário/rodada** inclui no mínimo:

| Corpus RAG | Formato | Uso |
|---|---|---|
| Grade horária | pdf/xlsx/txt parseado | Cruzar professor presente, slots |
| Modelo calendário | xlsx | Estrutura de abas e simulados |
| Simulados, siglas, referências | xlsx/md/pdf | Regras e metadados do semestre |
| **Proposta gerada** | **xlsx** | Estado atual pós-fatoração/refração |
| Relatório trocas / exports | xlsx/md | Cessões e impacto |
| Catálogo de regras (skill) | texto indexado | Explicar violações por id |
| Saída verificador | json/texto | PROBLEMA/AVISO por item |

Reindexar após cada alteração aceita no horário 🟡.

#### 4. Contexto obrigatório da sessão — Must

Cada sessão de chat recebe contexto montado pela plataforma:

| Fonte | Exemplos |
|---|---|
| Documentos de base (blob) | grade horária, modelo xlsx, simulados, siglas, `estado_2sem_*.md` |
| Saídas geradas | `Proposta_3`, relatório trocas, exportações derivadas |
| Metadados | `RuleSetSnapshot`, seed, semestre, coordenador |
| Verificação | checklist 0–11, PROBLEMA/AVISO |
| Catálogo de regras | ids + descrição (skill espelhada no BD) |
| Estatísticas / visões | agregações JSON (cessões, conflitos, semanas críticas) |

Equivalente funcional ao workspace que o coordenador monta hoje no
**Cursor** ou **Claude Code** com a skill e os arquivos do repositório.

#### 5. OpenAI via API da plataforma — Must

- Chave OpenAI apenas no **backend** (variável de ambiente / secret).
- Frontend → FastAPI → **OpenAI API** (chat completions + **function/tool
  calling** para ações Python permitidas).
- Tools expostas ao modelo 🟡 (lista inicial):
  - `rag_search` — busca no índice da rodada;
  - `get_calendar_view` — visão estatística;
  - `get_verification_report` — checklist;
  - `propose_allocation_patch` — move/troca prova (preview);
  - `run_partial_solver` — re-fatoração parcial (turmas/seed);
  - `apply_proposal` — só após confirmação explícita do coordenador.
- Deploy on-prem: requer conectividade à API OpenAI ou **Azure OpenAI**
  equivalente 🔴 detalhar na migração.

#### 6. Conexão via API — Must

- Chat no **frontend** chama API da plataforma (não expor chave OpenAI no browser).
- API orquestra RAG, estatísticas, OpenAI e execução Python.
- Contrato **OpenAPI** documentando copiloto + tools.

#### 7. Mesmo contrato de regras — Must

Solver, verificador e copiloto compartilham `RuleSetSnapshot`; regras
inegociáveis não podem ser flexibilizadas pelo agente.

#### 8. Rastreabilidade — Must

Registrar: `calendario_id`, `copilot_session_id`, mensagens, fontes
citadas, propostas, aceites/rejeições, `coordenador_id`, timestamps.

### Fluxo provisório na plataforma

```
Entradas carregadas → Fatoração → PropostaGerada
  → Verificador (checklist + estatísticas)
  → Coordenador abre Chat Copiloto
  → Perguntas: "por que 10C2 falhou item 10b?", "quantas cessões MFo?"
  → Agente (OpenAI + RAG) responde citando documentos + xlsx + verificador
  → Pedido de refatoração → plano + tools Python (backend) → preview
  → Coordenador confirma → backend executa → RAG reindexa → re-verificação
  → Repete até Verificado → Fechar horário (humano)
```

### Implicações arquiteturais

- **`ScheduleCopilotService`** — orquestra chat, **OpenAI**, tools, propostas.
- **`DocumentContextService`** + **`RagIndexService`** — ingestão, chunking,
  embedding e busca sobre uploads **e xlsx gerado** (OpenAI embeddings 🟡).
- **`CalendarViewsService`** — visões/estatísticas JSON.
- **`PythonActionBridge`** — mapeia tool-calls OpenAI → métodos Python
  (`CalendarSolver`, patch alocação, `CalendarVerifier`).
- Endpoints copiloto: `POST .../copilot/sessions`, `.../messages`,
  `.../proposals/{id}/apply`, `POST .../copilot/rag/reindex`.
- **UI:** `ScheduleCopilotChat` + `ProblemViewsPanel`.
- **Fallback:** OpenAI indisponível → refração manual + verificador seguem;
  chat exibe aviso.

### Relação com outros requisitos

| Mecanismo | Papel |
|---|---|
| Fatoração (solver Python) | Gera horário automaticamente |
| Verificador (Python) | Objetiva falhas; alimenta copiloto |
| Refração manual | Edição direta no grid |
| **Copiloto OpenAI + RAG** | Analista + parceiro na refração/refatoração |
| Fechar horário | Sempre ação humana explícita |

### Pendências

- [x] Provedor LLM → **OpenAI**
- [x] Grounding → **RAG** (documentos + xlsx gerado)
- [x] Interface → **chat embutido** + API
- [x] Execução → **backend Python** via tools (não código arbitrário)
- [ ] Modelo OpenAI específico (gpt-4o, o1, etc.)
- [ ] Lista fechada de **tools** e **tipos de visão** na v1
- [ ] Autonomia: aplicar lote com um clique vs confirmar ação a ação
- [ ] Política PII professores enviada à OpenAI (retenção, DPA escola)
- [x] Pseudonimização **transparente** para coordenador (nunca vê tokens) 🟢
- [ ] Criptografia at-rest opcional do mapping (AES) 🟡
- [ ] Deploy on-prem + OpenAI (internet vs Azure OpenAI)
- [ ] Copiloto read-only após fechar horário (Should)

---

## Privacidade — pseudonimização de professores para OpenAI

> Registrado em 2026-08-15 por Brener.  
> **Atualizado 2026-08-15:** pseudonimização **transparente** — coordenador
> nunca vê tokens; experiência idêntica ao uso sem camada OpenAI.

### Pergunta

É possível usar siglas e horários dos professores enviando à OpenAI apenas
dados **anonimizados**, atribuindo um **código** por professor no Python e
**revertendo** ao receber a resposta?

### Resposta 🟢

**Sim.** A abordagem correta é **pseudonimização reversível no backend**
(não anonimização irreversível):

| Camada | Dados |
|---|---|
| OpenAI (prompt, RAG, tools para LLM) | Tokens `PROF_*` — **sem** siglas/nomes reais |
| Backend Python (solver, verificador, patch) | **Siglas reais** — como hoje |
| UI do coordenador (chat, grid, relatórios) | **Siglas reais** — após de-tokenização |

Horários (tempos 1–11, semanas, datas, turmas `10C1`) **podem** seguir em
claro — não identificam professor sozinhos. O que se protege são **siglas e
nomes** da planilha `siglas_profs_aux_etc.xlsx`.

### Comportamento desejado — Must

1. Ao iniciar rodada/calendário, gerar mapa `sigla_real ↔ token` único por
   `calendario_id` (persistido PostgreSQL).
2. **Antes** de cada chamada OpenAI: função `anonymize_for_llm(texto|json)`.
3. **Depois** de cada resposta OpenAI: `deanonymize_for_ui(texto)` antes de
   mostrar ao coordenador.
4. Mensagens do coordenador que mencionem siglas reais são tokenizadas no
   backend antes do envio ao modelo.
5. Índice **RAG** indexado/recuperado na forma **tokenizada** para trechos
   que contenham professores.
6. **`apply_proposal` / tools Python**: argumentos vindos do LLM usam tokens;
   backend traduz para siglas reais **antes** de executar código.
7. Logs de auditoria: armazenar tokens + hash; **não** logar prompts com
   siglas reais enviados à OpenAI.

### Transparência para o coordenador — Must 🟢

A pseudonimização é **100% invisível** para quem usa o aplicativo. O
coordenador **nunca** interage com tokens `PROF_*` nem precisa saber que
existem.

| Superfície | O que o coordenador vê |
|---|---|
| Chat copiloto | Sempre **siglas/nomes reais** (ex.: MFo, Kle) |
| Grid / refração | Siglas reais — como planilha xlsx hoje |
| Preview / diff de proposta do copiloto | Siglas reais |
| Painel verificador | Siglas reais nos PROBLEMA/AVISO |
| Relatórios (cessões, trocas, e-mail preview) | Siglas reais |
| Mensagens que **ele digita** | Digita siglas reais; backend tokeniza sozinho |

**Proibido na UI de coordenador:**

- Exibir tokens `PROF_*` ou códigos pseudônimos
- Pedir ao coordenador para "traduzir" ou escolher código de professor
- Toggle "modo anonimizado" ou configuração de privacidade visível
- Erros do copiloto contendo token não de-tokenizado

**Permitido apenas** em ferramentas **admin/dev** (fora do fluxo normal):
visualizar mapa token↔sigla para suporte — com RBAC restrito 🟡.

A experiência deve ser **indistinguível** de um copiloto que recebesse
siglas reais, exceto pela proteção de privacidade na fronteira OpenAI.

### Componente

- **`ProfessorPseudonymService`** — create map, anonymize, deanonymize;
  **garantia:** nenhuma API exposta ao frontend retorna texto com tokens
  destinado ao coordenador.

### Limites (privacidade, não UX)

- Pseudonimização **reduz** PII direta; **não elimina** risco de inferência
  (padrão de horário + turma pequena).
- Ainda exige **DPA/contrato** com OpenAI ou Azure OpenAI.
- "Descriptografia" na prática é **lookup seguro** do mapa; criptografia
  AES adicional no mapa at-rest é opcional 🟡.

Detalhes: `_reversa_sdd/adrs/009-pseudonimizacao-professores-openai.md`

---

## Notificação por e-mail aos professores doadores (cessão de tempo)

> Registrado em 2026-08-15 por Brener, durante fase de Interpretação do `/reversa`.

### Contexto

Quando uma disciplina/professor **cede** tempo de aula para a aplicação de
prova de **outra** disciplina, o professor doador precisa ser informado. Hoje
isso é feito manualmente a partir do **relatório de trocas de tempo**
(`Relatorio_trocas_de_tempo.md` / `.xlsx`, gerado por
`exportar_relatorio_trocas.py` a partir da planilha final).

### Comportamento desejado na plataforma

1. **Não enviar automaticamente** a cada fatoração ou refração do horário.
   Gerar ou ajustar o calendário **não dispara** e-mail.
2. **Ação explícita do coordenador** — funcionalidade dedicada do tipo
   *"Enviar e-mails aos professores doadores"*, disponível quando o
   coordenador estiver **seguro** de que o horário (ou trecho relevante)
   está correto — tipicamente **após fechar** o calendário ou após revisão
   manual estável.
3. **Origem dos destinatários:** o sistema identifica, no calendário
   **fechado/aprovado** da rodada, todas as **cessões de tempo** (mesma
   lógica do relatório de trocas: turma, disciplina solicitante, professor
   solicitante, tempo(s), dia/data, disciplina/professor **doador**).
4. **Conteúdo do e-mail (mínimo):** informar ao professor doador que a
   disciplina **[nome/código]**, professor(a) **[nome]**, utilizará o
   **tempo de aula [Nº tempo(s)]** do dia **[data / dia da semana]** para
   aplicação de prova (turma **[turma]** quando aplicável).
5. **Um e-mail por cessão** (ou agrupado por professor/dia — 🔴 a definir
   na fase de design; default sugerido: **um e-mail por linha de cessão**
   espelhando o relatório de trocas).

### Fluxo na plataforma (provisório)

```
Calendário fechado/aprovado
  → Coordenador abre "Comunicação com professores"
  → Pré-visualiza lista de cessões + e-mails dos doadores
  → Confirma envio
  → Sistema registra quem recebeu e quando (auditoria)
```

### Implicações arquiteturais

- **Cadastro de e-mail** por professor (hoje só sigla + nome em
  `siglas/siglas_profs_aux_etc.xlsx` — 🔴 confirmar se há coluna de e-mail
  ou se será novo campo na plataforma).
- **Serviço de e-mail** (SMTP institucional ou provedor transacional —
  SendGrid/SES/etc. na nuvem; SMTP local no on-prem).
- **Estado de envio** persistido: `calendario_id`, `cessao_id`, `enviado_em`,
  `enviado_por` — permite reenvio se o calendário mudar **depois** do
  primeiro envio (🔴 política de reenvio a definir).
- **Reprocessar lista** se o coordenador refizer refração **antes** de enviar;
  após envio, mudanças no calendário devem **sinalizar** cessões alteradas
  (novas, removidas, datas mudadas).

### Legado equivalente 🟢

| Legado | Papel |
|---|---|
| `exportar_relatorio_trocas.py` | Extrai cessões da planilha final |
| `Relatorio_trocas_de_tempo.xlsx` | Pré-visualização humana hoje |
| `gerar_calendario.relatorio()` | Formata trocas a partir de `(doador)` |

### Pendências

- [ ] Existe e-mail dos professores na planilha de siglas ou em outro sistema?
- [ ] Idioma do e-mail (PT / DE / bilíngue)?
- [ ] Um e-mail por cessão ou agrupado por professor?
- [ ] Reenvio automático quando cessão muda após envio, ou só aviso ao coordenador?
