# User Stories — Ciclo do Calendário de Provas

> Gerado pelo Redator (Reversa) | doc_level: completo

## US-01 — Carregar entradas

**Como** coordenador  
**Quero** enviar grade PDF, definir bloqueios clicando no calendário e registrar provas  
**Para** preparar a fatoração sem depender de Excel ou IA

**Critérios:**
- Upload grade Untis
- `CalendarBlockPicker` por turma/série (ADR-012)
- `ExamCatalogEditor` ou máscara provas (ADR-010)
- `EnemWeekConfigPanel` — 2 datas ENEM + disciplinas/janela (ADR-015)

---

## US-01b — Identificar coordenador (PIN)

**Como** coordenador  
**Quero** entrar com a conta da escola e informar meu PIN  
**Para** que meus calendários fiquem isolados dos outros coordenadores

**Critérios:**
- Login institucional compartilhado + seleção PIN (ADR-015)
- Auditoria de ações por PIN
- Sessão exibe nome do coordenador

---

## US-01c — Configurar semanas do ENEM

**Como** coordenador  
**Quero** informar as duas datas do ENEM e marcar quais disciplinas podem ter prova na semana anterior  
**Para** customizar a restrição a cada semestre

**Critérios:**
- Sempre 2 datas (domingos)
- Janela = 6 dias anteriores a cada data
- Multi-select disciplinas por janela; sugestão skill editável
- Solver e verificador respeitam config salva

---

## US-02 — Selecionar regras

**Como** coordenador  
**Quero** marcar quais regras aplicar e quais podem flexibilizar  
**Para** controlar a rodada antes de gerar

**Critérios:**
- Tela 1: catálogo skill; default todas aplicar
- Regras inegociáveis bloqueadas para flex
- Tela 2: regras novas opcionais

---

## US-03 — Fatorar calendário

**Como** coordenador  
**Quero** gerar Proposta 3 automaticamente  
**Para** obter calendário de provas respeitando cessões e coordenação

**Critérios:**
- Job async com progresso
- Saída `Proposta_3.xlsx` layout Klausurplan
- Lista turmas falhadas se inviável

---

## US-04 — Visualizar sem Excel

**Como** coordenador  
**Quero** ver o calendário por turma na plataforma  
**Para** revisar antes de distribuir o arquivo

**Critérios:**
- `CalendarPreviewView` read-only (ADR-013)
- Paridade com Excel baixável
- Aba grade horária opcional

---

## US-05 — Verificar e corrigir

**Como** coordenador  
**Quero** checklist automático e refração assistida  
**Para** fechar horário sem violações

**Critérios:**
- `VerificationPanel` itens 0–11
- `CalendarEditor` ou copiloto com confirmação (ADR-008)

---

## US-06 — Exportar e comunicar

**Como** coordenador  
**Quero** relatórios derivados e e-mail manual a doadores  
**Para** informar professores que cederam tempo

**Critérios:**
- Exports RF-01–04
- `DonorEmailPanel` manual pós-fechar (ADR-007)

---

## US-07 — Recalcular sem IA

**Como** coordenador  
**Quero** refatorar com novas entradas persistidas  
**Para** não consumir tokens OpenAI a cada tentativa

**Critérios:**
- Pipeline determinístico ADR-011
- Copiloto opcional só pós-geração
