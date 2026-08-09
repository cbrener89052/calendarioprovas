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

## Decisões RBAC e regras (2026-08-09 — confirmado por Brener)

### Segmento de atuação por coordenador

Cada coordenador configura o **seu segmento de atuação** na escola, com as características do seu contexto:

- Séries/turmas sob sua responsabilidade (ex.: só Ensino Médio C, ou segmento específico)
- Períodos letivos, grupos de viagem, calendário de simulados do segmento
- Parâmetros locais (datas-limite, feriados adicionais, exceções de disciplina)

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

Regra **LP/LIT/RED ≥10 dias antes do conselho** — na skill ✅; implementação no gerador/verificador 🔴 pendente.

### Pendências resolvidas

- [x] Isolamento por coordenador → **sim**, via segmento de atuação
- [x] Templates compartilhados → catálogo institucional de regras + toggles
- [ ] Admin institucional vs coordenador puro — a detalhar (provável: Brener admin inicial)

### Implicação do deploy híbrido

- Mesma aplicação empacotada em **Docker Compose**: API Python + Postgres + (opcional) frontend
- Na nuvem: serviços gerenciados (ex.: Vercel/Railway/Fly + Neon Postgres + S3)
- On-prem: `docker compose up` em servidor local da escola, sem dependência de internet para operação diária
