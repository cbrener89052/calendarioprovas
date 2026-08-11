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
| Frontend | **React (Vite) + Tailwind CSS** — Lucide React; estado Context ou Redux (ADR-007) |

## Decisões RBAC e regras (2026-08-09 — confirmado por Brener)

### Segmento de atuação por coordenador

Cada coordenador configura o **seu segmento de atuação** na escola, com as características do seu contexto:

- Séries/turmas sob sua responsabilidade (ex.: só Ensino Médio C, ou segmento específico)
- **GRUPOS** customizáveis (ver abaixo), calendário de simulados do segmento
- Parâmetros locais (feriados adicionais, exceções de disciplina)

### GRUPOS (customizáveis por coordenador)

Substituem o conceito fixo “grupos de viagem” (ex.: 10/12 vs 9/11). Cada coordenador define **GRUPOS** com:

| Campo | Descrição |
|---|---|
| **Nome** | Rótulo livre (ex.: “Turmas que viajam cedo”, “9º e 11º”) |
| **Início / fim do semestre** | Janela letiva do grupo para provas |
| **Datas de 2ª chamada** | Uma ou mais datas por grupo |
| **Datas de conselho de classe** | Período vetado (início/fim) por grupo |

Turmas são associadas a um GRUPO; limites de período, 2CH e conselho vêm do grupo, não de código hardcoded.

**Isolamento:** cada coordenador vê e opera **apenas os dados do seu segmento** (tenant = coordenador + segmento).

### Motor de regras configurável (futuro)

Hoje as regras estão **hardcoded** em `gerar_calendario.py` e na skill. Na plataforma:

| Tipo | Comportamento |
|---|---|
| **Regra codificada** | Implementada no solver; no menu: **ativar / desativar** por coordenador/semestre |
| **Regra institucional (template)** | Catálogo derivado da skill; toggles no menu |
| **Customização assistida por IA** | Adaptações que **não entram no código** — interpretadas pela IA conforme configs do coordenador (ex.: preferências textuais, exceções pontuais documentadas) |

**Princípio:** o que exige lógica determinística no solver → toggle on/off de regra codificada. O que é nuance contextual → camada IA + config, sem deploy de código.

### PR #14 mergeada em `main`

Regra **LP/LIT/RED ≥10 dias** — skill ✅; código ✅ (PR #18 mergeada em `main`).

### Pendências resolvidas

- [x] Isolamento por coordenador → **sim**, via segmento de atuação
- [x] Templates compartilhados → catálogo institucional de regras + toggles
- [x] Admin institucional vs coordenador puro → **Brener = admin_instituicao**; coords só no próprio segmento
- [x] Frontend v1 → **React Vite + Tailwind + Lucide** (ADR-007)
- [x] Customização IA → **verificador + relatório auxiliar**

### Implicação do deploy híbrido

- Mesma aplicação empacotada em **Docker Compose**: API Python + Postgres + **frontend Vite** + worker
- Na nuvem: serviços gerenciados (ex.: Vercel/Railway/Fly + Neon Postgres + S3)
- On-prem: `docker compose up` em servidor local da escola, sem dependência de internet para operação diária

## Histórico de calendários gerados (2026-08-11 — Brener)

À medida que os calendários forem **gerados**, o sistema deve **gravar automaticamente**
na base de dados (metadados + blobs de arquivo) cada versão produzida, para evitar
perda por exclusão ou sobrescrita acidental.

O coordenador deve poder, **pela interface web**, de forma transparente:

| Ação | Comportamento |
|------|----------------|
| **Consultar histórico** | Listar versões anteriores do semestre (data, status, verificação) |
| **Abrir versão antiga** | Ver detalhes, verificação e downloads como na geração atual |
| **Restaurar referência** | Marcar uma versão antiga como referência ativa do semestre (sem apagar as mais novas) |
| **Download** | Baixar xlsx e relatórios de qualquer versão não apagada |
| **Apagar** | Excluir versão escolhida, com confirmação; some da lista padrão |

**Princípio:** persistência automática no fim de cada job OK; nenhum passo manual de “salvar backup”.

### Tela única de consulta (2026-08-11)

A **mesma tela** de acesso aos calendários gerados serve também para **consultar períodos anteriores** (semestres letivos do segmento). Fluxo master-detail:

1. Filtros: ano, período (1º/2º semestre), ordenação (mais recente primeiro)
2. Lista de semestres que possuem (ou possam possuir) calendários gerados
3. Ao selecionar um período → lista de versões geradas (download, apagar, restaurar referência, abrir detalhe)

Rota UI: `/calendarios` (SCR-10). Não duplicar em “Histórico” separado.

Ver ADR-009 e `plataforma-multi-coordenador/requirements.md` RF-15–RF-19.
