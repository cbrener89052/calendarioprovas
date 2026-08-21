# Requirements: Plataforma Multi-Coordenador

> Identificador: `007-plataforma-multi-coordenador`
> Data: `2026-08-21`
> Requisitos: `.reversa/context/user-requirements.md`

## 1. Resumo executivo

Evolução de CLI monolítico + arquivos locais para **plataforma web** com
**5 coordenadores**, PostgreSQL, blob storage, FastAPI e UI web. Inclui
seleção de regras, ingestão visual (bloqueios, catálogo), fatoração,
visualização/export Excel, copiloto OpenAI opcional e e-mail manual a doadores.

## 2. Stack acordada 🟢

| Camada | Tecnologia |
|--------|------------|
| Backend | Python FastAPI |
| BD | PostgreSQL |
| Blobs | S3 / pasta local (Docker on-prem) |
| Auth | Login individual (5 coord.) 🟡 |
| Frontend | Web app 🟡 |
| IA | OpenAI API backend-only (ADR-008) |

## 3. Personas

| Persona | Necessidade |
|---------|-------------|
| Coordenador | Ciclo completo: entradas → regras → fatorar → revisar → fechar |
| Coordenador | Ver calendário **sem Excel** (ADR-013) |
| Coordenador | Bloqueios **clicando no calendário** (ADR-012) |
| Admin escola | Templates institucionais compartilhados 🟡 |

## 4. Regras de negócio

1. **RN-01:** Isolamento de dados por coordenador (ou unidade) — a confirmar RBAC. 🟡
2. **RN-02:** Versionamento entradas/saídas por semestre/rodada. 🟢
3. **RN-03:** Saída oficial **Excel** Proposta_3 + preview in-app. 🟢 ADR-013
4. **RN-04:** Recálculo **sem IA** quando entradas estruturadas persistidas. 🟢 ADR-011
5. **RN-05:** Copiloto **após** geração — Q&A/refração colaborativa. 🟢 ADR-008
6. **RN-06:** Pseudonimização professores só backend↔OpenAI (ADR-009). 🟢
7. **RN-07:** E-mail doadores **manual** pós-fechar (ADR-007). 🟢
8. **RN-08:** Deploy nuvem + Docker on-prem híbrido. 🟢

## 5. Componentes UI (Must)

| Componente | Feature | ADR |
|------------|---------|-----|
| `RulesSelectionWizard` | Telas 1–2 regras | — |
| `CalendarBlockPicker` | Bloqueios dia/semana turma/série | 012 |
| `ExamCatalogEditor` | Catálogo provas | 010 |
| `IntakeTemplatePanel` | Upload máscara provas (opcional) | 010 |
| `CalendarPreviewView` | Visualização read-only Proposta_3 | 013 |
| `CalendarEditor` | Refração manual | — |
| `ScheduleCopilotChat` | Copiloto pós-geração | 008 |
| `VerificationPanel` | Checklist PROBLEMA/AVISO | — |
| `DonorEmailPanel` | Preview e-mail doadores | 007 |
| `CloseCalendarAction` | Fechar horário | — |

## 6. Requisitos Funcionais

| ID | Requisito | Must |
|----|-----------|------|
| RF-01 | Auth login 5 coordenadores | Must |
| RF-02 | CRUD calendário por semestre | Must |
| RF-03 | Upload grade PDF | Must |
| RF-04 | CalendarBlockPicker + persist constraints | Must |
| RF-05 | ExamCatalog (UI ou máscara) | Must |
| RF-06 | RuleSetSnapshot + fatoração job async | Must |
| RF-07 | CalendarPreviewView + download Excel | Must |
| RF-08 | Verificação integrada pós-geração | Must |
| RF-09 | ReportExporter + exports | Must |
| RF-10 | ScheduleCopilotService pós-PropostaGerada | Must |
| RF-11 | DonorEmailService manual | Must |
| RF-12 | Estados: rascunho → gerado → verificado → fechado | Must |
| RF-13 | RAG reindex pós-alteração aceita | Should |

## 7. Critérios de Aceitação

```gherkin
Cenário: Ciclo completo coordenador
  Dado grade uploadada e bloqueios clicados na malha visual
  E catálogo provas e regras selecionadas
  Quando fatoração conclui
  Então coordenador vê CalendarPreviewView e baixa Proposta_3.xlsx
  E verificador lista PROBLEMA/AVISO
  E copiloto disponível para refração

Cenário: Recálculo sem tokens OpenAI
  Dado constraints e catálogo persistidos
  Quando nova fatoração
  Então nenhuma chamada OpenAI na ingestão
```

## 8. Lacunas

- 🔴 Auth provider específico
- 🔴 DPA OpenAI / on-prem + OpenAI
- 🟡 Frontend framework (Next.js provável)

## 9. Histórico

| Data | Alteração |
|------|-----------|
| 2026-08-21 | Versão inicial consolidando ADRs 007–013 |
