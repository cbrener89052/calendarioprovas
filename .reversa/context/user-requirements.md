# Requisitos declarados pelo usuário

> Registrado em 2026-08-09 por Brener, antes do Scout.

## Contexto

O sistema **calendarioprovas** hoje é um conjunto de scripts Python + planilhas/PDFs
locais, usado para montar o calendário de provas da Escola Alemã Corcovado.

## Requisito de evolução (prioritário)

O sistema será utilizado por **outros coordenadores da instituição**. Por isso,
precisa existir um **banco de dados** para armazenar:

1. **Saídas** — calendários gerados, relatórios, tabelas-resumo, tempos cedidos
2. **Arquivos de entrada** — bases que alimentam o sistema de **cada coordenador**:
   - horário-base das turmas (PDF/planilha)
   - modelo de calendário (xlsx)
   - calendário de simulados
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

### Implicação do deploy híbrido

- Mesma aplicação empacotada em **Docker Compose**: API Python + Postgres + (opcional) frontend
- Na nuvem: serviços gerenciados (ex.: Vercel/Railway/Fly + Neon Postgres + S3)
- On-prem: `docker compose up` em servidor local da escola, sem dependência de internet para operação diária

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
- apoia a **refração** quando o coordenador pede mudanças concretas.

O agente **não substitui** solver, verificador nem fechamento do horário.

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

#### 2. Modo copiloto de alteração — Should

Quando o coordenador pede mudanças ("mova Biologia da semana 9 para 10",
"reduza cessões do professor X"), o agente:

- usa **visões analíticas** e estatísticas do estado atual;
- devolve **propostas estruturadas** (diff preview), não mutação silenciosa;
- o coordenador **confirma** antes de persistir;
- dispara **re-verificação** automática após aceite.

#### 3. Contexto obrigatório da sessão — Must

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

#### 4. Conexão via API — Must

- Chat no **frontend** chama API da plataforma (não expor chave LLM no browser).
- API orquestra contexto, estatísticas, provedor LLM e propostas.
- Contrato **OpenAPI** para integração alternativa (ferramenta externa).

#### 5. Mesmo contrato de regras — Must

Solver, verificador e copiloto compartilham `RuleSetSnapshot`; regras
inegociáveis não podem ser flexibilizadas pelo agente.

#### 6. Rastreabilidade — Must

Registrar: `calendario_id`, `copilot_session_id`, mensagens, fontes
citadas, propostas, aceites/rejeições, `coordenador_id`, timestamps.

### Fluxo provisório na plataforma

```
Entradas carregadas → Fatoração → PropostaGerada
  → Verificador (checklist + estatísticas)
  → Coordenador abre Chat Copiloto
  → Perguntas: "por que 10C2 falhou item 10b?", "quantas cessões MFo?"
  → Agente responde citando planilha + verificador + grade
  → (Opcional) Pedido de alteração → proposta estruturada → preview
  → Aceite → EmRefracao → re-verificação
  → Repete até Verificado → Fechar horário (humano)
```

### Implicações arquiteturais

- **`ScheduleCopilotService`** — orquestra chat, contexto, LLM, propostas
  (evolução do nome provisório `RefractionAgentGateway`).
- **`CalendarViewsService`** — visões/estatísticas JSON reutilizáveis pela UI
  e pelo agente.
- **`DocumentContextService`** — indexação/resumo dos blobs de entrada e
  saída para grounding do agente (RAG ou leitura estruturada 🟡).
- Endpoints de visão: `GET .../views/{tipo}`.
- Endpoints de copiloto: `POST .../copilot/sessions`,
  `POST .../copilot/sessions/{id}/messages` (pergunta ou instrução),
  `GET/POST .../copilot/proposals/{id}` (apply/reject).
- **UI:** painel `ScheduleCopilotChat` + `ProblemViewsPanel` no frontend.
- Provedor LLM configurável por deploy; **fallback:** chat indisponível,
  refração manual e verificador seguem funcionando.

### Relação com outros requisitos

| Mecanismo | Papel |
|---|---|
| Fatoração (solver) | Gera horário automaticamente |
| Verificador | Objetiva falhas; alimenta respostas do copiloto |
| Refração manual | Edição direta no grid |
| **Copiloto IA** | Analista + Q&A + sugestões com estatísticas |
| Fechar horário | Sempre ação humana explícita |

### Pendências

- [ ] Agente **interno** vs **externo** (Anthropic/OpenAI — alinhar ao Cursor/Claude)
- [x] Interface: **chat embutido** no frontend (copiloto) + API para integrações
- [ ] RAG vs leitura estruturada dos xlsx/pdf de base
- [ ] Lista fechada de **tipos de visão/estatística** na v1
- [ ] Autonomia: só sugestão vs aplicar lote com um clique
- [ ] Política de dados enviados ao LLM (PII, retenção, on-prem sem internet)
- [ ] Copiloto read-only após fechar horário (Should)

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
