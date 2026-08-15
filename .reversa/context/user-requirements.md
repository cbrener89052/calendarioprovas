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

## Agente de refração conectado via API

> Registrado em 2026-08-15 por Brener, durante fase de Geração do `/reversa`.

### Contexto

Além da **fatoração** automática (solver) e da **refração manual** (edição
direta do calendário), o coordenador frequentemente precisa **diagnosticar e
resolver conflitos** envolvendo tempos, cessões, turmas irmãs e regras
violadas. Hoje isso é feito com planilha + verificador + apoio externo
(skill/agente de IA fora da plataforma).

Na plataforma futura, deve existir a **possibilidade** de conectar um
**agente de IA via API** para apoiar a refração — não substituindo o solver
nem o verificador, mas operando sobre o **mesmo estado** do calendário e
sobre os **problemas detectados**, com **visões analíticas** que facilitem
a resolução.

### Comportamento desejado

1. **Conexão via API** — a plataforma expõe endpoints estáveis (REST ou
   equivalente) para um agente externo ou interno consumir:
   - estado atual do calendário / proposta em refração;
   - conjunto de regras ativo (`RuleSetSnapshot`);
   - saída do verificador (`PROBLEMA` / `AVISO` por item);
   - metadados de cessões e alocações relevantes.
2. **Visões para resolução de problemas** — o agente (e/ou a UI que o
   hospeda) deve poder solicitar **visões** agregadas do calendário, por
   exemplo:
   - conflitos por **turma** / **semana** / **dia**;
   - sobrecarga de **avaliações por semana**;
   - **cessões** por professor doador ou solicitante;
   - **coordenação entre turmas irmãs** (professor comum, Fil/Soc);
   - violações por **regra de domínio** (id R-P1, C4, R-G1, etc.);
   - slots **candidatos** para mover uma prova sem quebrar regras rígidas.
3. **Escopo: refração** — o agente atua principalmente no estado
   `EmRefracao` e em rodadas de **re-fatoração parcial** (re-solver
   subconjunto de turmas ou re-seed), não no envio de e-mail nem no
   fechamento/publicação sem confirmação humana.
4. **Propostas, não mutações silenciosas** — por padrão o agente **propõe**
   ações estruturadas (ex.: mover prova, trocar doador, marcar regra
   flexível, pedir nova fatoração com seed X); o **coordenador confirma**
   antes de persistir. Autonomia total 🔴 a definir.
5. **Mesmo contrato de regras** — solver, verificador e agente usam o
   **mesmo** `RuleSetSnapshot` da rodada; o agente não pode flexibilizar
   regra marcada como inegociável.
6. **Rastreabilidade** — cada sessão de agente registra: `calendario_id`,
   `agent_session_id`, propostas, aceites/rejeições, `coordenador_id`,
   timestamp — auditoria equivalente à edição manual.

### Fluxo provisório na plataforma

```
PropostaGerada / EmRefracao
  → Verificador lista PROBLEMA/AVISO
  → Coordenador abre "Assistente de refração" (chat ou painel)
  → Frontend chama API da plataforma
  → Plataforma agrega visões + contexto
  → Agente (via API) analisa e devolve propostas estruturadas
  → Coordenador revisa preview (grid + diff)
  → Aceite → persiste alocação / dispara re-verificação
  → Repete até Verificado ou Fechado
```

### Implicações arquiteturais

- **`RefractionAgentGateway`** (ou nome equivalente) na API FastAPI:
  orquestra contexto, visões, chamada ao provedor de agente e aplicação
  de propostas aceitas.
- **Endpoints de visão** (`GET .../views/{tipo}`) retornando JSON
  normalizado — independentes do LLM, úteis também para UI humana.
- **Endpoints de sessão de agente** (`POST .../agent/sessions`,
  `POST .../agent/sessions/{id}/messages`, `POST .../agent/proposals/{id}/apply`).
- **Integração LLM** desacoplada: chave/API do provedor configurável por
  deploy (nuvem vs on-prem); fallback **desligado** se agente indisponível
  (refração manual continua).
- **OpenAPI** documentando contrato agente ↔ plataforma (feature
  `plataforma-multi-coordenador` + global `openapi/`).
- Skill `calendario-provas` permanece **fonte semântica** das regras;
  o agente recebe resumo/id de regras do catálogo, não texto livre
  dessincronizado.

### Relação com outros requisitos

| Mecanismo | Papel |
|---|---|
| Fatoração (solver) | Geração / regeneração automática global ou parcial |
| Refração manual | Edição direta célula a célula (grid) |
| **Agente via API** | Diagnóstico + propostas guiadas por visões e checklist |
| Verificador | Árbitro objetivo pós-proposta (humana ou agente) |
| Fechar horário | Sempre ação humana explícita |

### Pendências

- [ ] Agente **interno** (módulo Python) vs **externo** (OpenAI/Anthropic/etc.)
- [ ] Interface: chat embutido no frontend vs apenas API para ferramenta externa
- [ ] Lista fechada de **tipos de visão** na v1
- [ ] Autonomia: só sugestão vs aplicar lote com um clique
- [ ] Política de dados enviados ao LLM (PII professores, retenção, on-prem)

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
