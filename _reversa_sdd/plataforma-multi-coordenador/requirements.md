# Requirements: Plataforma Multi-Coordenador

> Identificador: `007-plataforma-multi-coordenador`  
> Data: `2026-08-09`

## 1. Resumo executivo

Plataforma web para 5 coordenadores gerarem calendários de provas com dados isolados por segmento, persistência PostgreSQL, blobs para arquivos, motor de regras com toggles, GRUPOS customizáveis e customizações IA. Evolução do CLI Python via FastAPI + worker solver, deploy híbrido (nuvem + Docker on-prem).

## 2. Contexto

| Fonte | Trecho | Conf. |
|-------|--------|-------|
| `.reversa/context/user-requirements.md` | 5 coords, FastAPI, Postgres | 🟢 |
| `_reversa_sdd/adrs/005-plataforma-fastapi-postgres.md` | Stack | 🟢 |
| `_reversa_sdd/adrs/006-segmento-regras-configuraveis-ia.md` | Segmento, GRUPOS, toggles | 🟢 |
| `_reversa_sdd/permissions.md` | RBAC | 🟢 |
| `_reversa_sdd/erd-complete.md` | Modelo dados | 🟡 |

## 3. Personas

| Persona | Objetivo | Cenário |
|---------|----------|---------|
| Coordenador | Configurar segmento e gerar calendário | Login → upload grade → gerar → publicar |
| Admin instituição | Gerenciar usuários e catálogo regras | CRUD coords + templates 🟢 |
| Leitor | Consultar calendário publicado | Somente leitura |

## 4. Regras de negócio

1. **RN-01:** Isolamento: coordenador acessa apenas seu segmento 🟢
2. **RN-02:** GRUPO customizável: nome, início/fim semestre, datas 2ª chamada[], conselho início/fim 🟢
3. **RN-03:** Turma ligada a um GRUPO; períodos vêm do grupo, não hardcode 🟢
4. **RN-04:** Login individual (5 contas) 🟢
5. **RN-05:** Deploy nuvem padrão + Docker Compose on-prem 🟢
6. **RN-06:** Worker Python reutiliza lógica `gerar_calendario.py` 🟢
7. **RN-07:** Verificação automática pós-job 🟡
8. **RN-08:** Versionamento entradas/saídas por semestre 🟡

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério | Conf. |
|----|-----------|------------|----------|-------|
| RF-01 | Auth login individual (JWT/sessão) | Must | 5 usuários isolados | 🟢 |
| RF-02 | CRUD Segmento (1:1 coordenador) | Must | Turmas e params do segmento | 🟢 |
| RF-03 | CRUD GRUPO (nome, datas semestre, 2CH, conselho) | Must | Turmas associadas via grupo_id | 🟢 |
| RF-04 | CRUD Semestre por segmento | Must | ano, periodo, datas | 🟢 |
| RF-05 | Upload entradas (grade PDF/xlsx, modelo, siglas, simulados) | Must | Blob + metadados BD | 🟢 |
| RF-06 | Job gerar calendário (Proposta 3) | Must | Async; xlsx + relatórios | 🟢 |
| RF-07 | Verificação automática pós-job | Must | Bloqueia publish se erro crítico | 🟡 |
| RF-08 | Download relatórios (tabela, cessões, trocas) | Must | Paridade exportadores | 🟢 |
| RF-09 | Toggles regras codificadas por semestre | Must | ADR-006 | 🟢 |
| RF-10 | CRUD customização IA | Must | Texto por segmento; usado em verificador + relatório | 🟢 |
| RF-11 | Publicar versão calendário | Should | Flag publicado + timestamp | 🟡 |
| RF-12 | Admin catálogo regras + leitura cross-segmento (Brener) | Must | Papel `admin_instituicao`; coords isolados | 🟢 |
| RF-13 | Docker Compose (API + Postgres + worker + frontend) | Must | `docker compose up` on-prem | 🟢 |
| RF-14 | Frontend web React Vite + Tailwind | Must | ADR-007; toggles e job solver na UI | 🟢 |

## 6. RNFs

| Tipo | Requisito | Evidência | Conf. |
|------|-----------|-----------|-------|
| Segurança | Tenant isolation por segmento_id | permissions.md | 🟢 |
| Disponibilidade | On-prem opera sem internet diária | user-requirements | 🟢 |
| Escalabilidade | Worker separado da API | architecture.md | 🟡 |
| Storage | S3 nuvem / filesystem local | ADR-005 | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Coordenador gera calendário
  Dado coordenador autenticado com segmento configurado e GRUPO "10/12"
  Quando faz upload da grade e dispara geração Proposta 3
  Então job completa com xlsx, verificação OK e relatórios disponíveis

Cenário: Isolamento entre coordenadores
  Dado coordenador A e coordenador B com segmentos distintos
  Quando A lista semestres
  Então não vê dados do segmento de B

Cenário: GRUPO define conselho
  Dado GRUPO com conselho_inicio 2026-11-24
  Quando solver aloca provas
  Então semana vetada reflete datas do GRUPO, não constante hardcoded
```

## 8. MoSCoW

RF-01–RF-06, RF-08, RF-09, RF-12–RF-14 Must; RF-07, RF-11 Should.

## 10. Lacunas

- 🔴 PR #14 LP/LIT/RED 10 dias no código — ver `questions.md#pergunta-4`
- 🟡 Context vs Redux — decidir na implementação

## 11. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | IA verificador+relatório; admin Brener | reversa-reviewer |
| 2026-08-09 | Versão inicial Fase 4 | reversa-writer |
