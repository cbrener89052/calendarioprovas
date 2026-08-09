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
