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
- Para cada regra, o usuário marca:
  - **Aplicar** — entra no conjunto desta rodada.
  - **Pode flexibilizar** — o solver/checklist pode relaxar esta regra
    (na ordem de afrouxamento documentada na skill, quando aplicável).
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

*(O usuário mencionou "faturar o horário" — interpretado como **fechar**
o horário; confirmar terminologia.)*

### Terminologia a confirmar com o usuário

| Termo usado | Interpretação provisória |
|---|---|
| **Fatoração** | Geração automática do horário (solver / proposta) |
| **Refração** | Refinamento ou reajuste do horário já gerado |
| **Fechar horário** | Aprovar a versão final para entrega / produção |

### Implicações para specs e arquitetura

- **Catálogo de regras** versionado (origem: skill + regras custom do
  coordenador), com metadados: id, descrição, prioridade, ordem de
  relaxamento, se é institucional ou por sessão.
- **Perfil de regras por rodada** persistido (PostgreSQL) ligado ao
  calendário / proposta gerada — rastreabilidade do que foi aplicado.
- **Verificador** deve distinguir **falha** (regra aplicada e violada)
  de **aviso** (regra flexibilizada e relaxada), alinhado ao que a skill
  já exige para cessão.
- **Regras inegociáveis** (ex.: presença do professor na aplicação,
  datas fixas de simulados) não devem aparecer como flexibilizáveis
  no UI — ou devem estar bloqueadas por padrão.

### Pendências

- [ ] Confirmar significado exato de *refração* vs *fatoração*
- [ ] Confirmar se "fechar horário" = publicar na `main` / entregar à escola
- [ ] Definir se perfil de regras é por coordenador, por semestre ou ambos
- [ ] Definir defaults na 1ª execução (todas as regras da skill ativas?)
