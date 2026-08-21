# Requirements: Exportação de Relatórios

> Identificador: `003-exportacao-relatorios`
> Data: `2026-08-16`
> Pasta da extração reversa: `_reversa_sdd/`
> Confidência: 🟢 CONFIRMADO, 🟡 INFERIDO, 🔴 LACUNA / DÚVIDA

## 1. Resumo executivo

A feature **exportacao-relatorios** deriva **relatórios e tabelas** a partir da
planilha **Proposta 3 final** (xlsx), relendo células com openpyxl — **nunca**
a memória do solver. Inclui tabela por turma, tempos cedidos, trocas
(doadores/solicitantes), provas por professor e PDF estático de regras. Na
plataforma, alimenta preview de **e-mail aos doadores** (ADR-007).

## 2. Contexto a partir do legado

| Fonte | Trecho relevante | Confiança |
|-------|------------------|-------------|
| `_reversa_sdd/code-analysis.md#Módulo: exportacao-relatorios` | 5 scripts, saídas nomeadas | 🟢 |
| `_reversa_sdd/adrs/002-relatorios-releem-planilha.md` | Princípio releitura pós-edição | 🟢 |
| `_reversa_sdd/flowcharts/exportacao-relatorios.md` | Fluxo por script | 🟢 |
| `_reversa_sdd/adrs/007-email-doadores-manual.md` | Origem lista cessões | 🟢 |
| `.reversa/context/user-requirements.md#Notificação por e-mail` | Preview manual pós-fechar | 🟢 |

## 3. Personas e cenários de uso

| Persona | Objetivo | Cenário-chave |
|---------|----------|---------------|
| Coordenador | Ver calendário sem abrir Excel | `CalendarPreviewView` (ADR-013) — mesmo blob Proposta_3 |
| Coordenador | Publicar tabelas para escola/professores | Roda 4 exportadores após editar xlsx |
| Coordenador | Revisar cessões antes de e-mail | Abre relatório trocas (.md/.xlsx) |
| Sistema (plataforma) | Gerar blobs derivados | `ReportExporter` pós-verificação OK |
| Copiloto OpenAI | Contexto RAG de cessões | Corpus inclui export trocas tokenizado 🟡 |

## 4. Regras de negócio

1. **RN-01:** Toda exportação **reparseia** xlsx gravado; ordem pós-edição manual documentada na skill. 🟢
2. **RN-02:** Escopo **Proposta 3** apenas (nomes de arquivo hardcoded). 🟢
3. **RN-03:** Relatório trocas lista: turma, solicitante, tempo(s), data, **doador**. 🟢
4. **RN-04:** E-mail doadores usa **mesma lógica** que `exportar_relatorio_trocas` — envio manual. 🟢
5. **RN-05:** UI coordenador vê **siglas reais**; RAG/copilot tokeniza no backend (ADR-009). 🟢

## 5. Requisitos Funcionais — por script 🟢

| ID | Script legado | Saída | Must |
|----|---------------|-------|------|
| RF-01 | `exportar_tabelas_turma.py` | `Tabela_Provas_por_Turma_Proposta_3.xlsx` | Must |
| RF-02 | `exportar_tempos_cedidos.py` | `Relatorio_Tempos_Cedidos_Proposta_3.xlsx` | Must |
| RF-03 | `exportar_relatorio_trocas.py` | `.md` + `.xlsx` (3 abas) | Must |
| RF-04 | `exportar_provas_por_professor.py` | `Provas_por_Professor_Proposta_3.xlsx` | Must |
| RF-05 | `exportar_regras_pdf.py` | `referencia/Regras_Negocio_*.pdf` | Could 🟡 ADR-014 |

## 6. Requisitos Funcionais — plataforma 🟡

| ID | Requisito | Prioridade | Critério de aceite |
|----|-----------|------------|--------------------|
| RF-06 | `ReportExporter` gera todos RF-01–04 sob demanda | Must | Blobs no storage por `calendario_id` |
| RF-07 | API download por tipo de relatório | Must | GET `/calendars/{id}/exports/{type}` |
| RF-08 | Re-export após refração (idempotente) | Must | Nova versão blob + timestamp |
| RF-09 | `DonorEmailService` consome export trocas | Must | Preview lista cessões ADR-007 |
| RF-10 | Registrar export em auditoria | Should | `exportado_em`, `exportado_por` |

## 7. Critérios de Aceitação

```gherkin
Cenário: Export após edição manual
  Dado Proposta_3 xlsx editada manualmente
  Quando coordenador dispara exportação completa
  Então tabelas refletem células atuais do xlsx
  E não valores cacheados do solver

Cenário: Relatório trocas para e-mail
  Dado calendário fechado com cessões
  Quando exportar_relatorio_trocas roda
  Então cada linha identifica doador e solicitante com siglas reais
  E DonorEmailPanel pode pré-visualizar destinatários
```

## 8. Lacunas

- 🟡 `exportar_regras_pdf` — adicionar `fpdf` ao legado (Could); plataforma v1 HTML regras, PDF v1.1 (ADR-014)
- 🟡 Duplicação parse xlsx entre exportadores (DT-07)
- 🟡 Ordem batch dos 5 scripts na plataforma (job único vs paralelo)

## 9. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-16 | Versão inicial | reversa-writer |
