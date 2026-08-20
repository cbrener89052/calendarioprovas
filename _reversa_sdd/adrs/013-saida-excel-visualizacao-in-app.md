# ADR-013 — Saída Excel + visualização in-app do calendário

> Status: **aceito** (requisito usuário 2026-08-16)  
> Confiança: 🟢

## Contexto

Brener confirmou:

1. A **saída oficial** continua sendo **Excel** (`Proposta_3_<semestre>.xlsx`
   no layout Klausurplan), como já definido no legado e ADR-010.
2. Na **tela do usuário**, o coordenador **Must** poder **visualizar o
   horário/calendário das turmas** **sem abrir o Excel** — view de
   visualização read-only na plataforma.

Entrada visual (bloqueios) ≠ saída: bloqueios são clicáveis na ingestão;
**resultado da fatoração** é espelhado na UI e **exportado** em xlsx.

## Decisão

1. **Saída Must:** `escrever()` grava `Proposta_3_*.xlsx` + blob storage;
   botão **Baixar Excel** sempre disponível após geração.
2. **UI Must:** componente **`CalendarPreviewView`** — malha Klausurplan
   read-only, uma aba/seletor por turma, paridade visual com o xlsx.
3. **`CalendarViewsService`** alimenta a preview a partir do **mesmo parse**
   usado por `verificar_calendario` / exports (ADR-002 — releitura xlsx).
4. Após refração/copiloto, preview **Must** atualizar quando o xlsx persistido mudar.
5. Distinção de componentes:
   - `CalendarPreviewView` — **visualização** (read-only)
   - `CalendarEditor` — **refração** (edição manual de células)
   - `CalendarBlockPicker` — **bloqueios** pré-fatoração

## Consequências

- ✅ Coordenador revisa calendário no browser; Excel para distribuição/arquivo
- ✅ Uma fonte de verdade (xlsx blob) → preview + download idênticos
- ⚠️ Frontend deve renderizar malha multi-aba (8 turmas)
- ⚠️ Grade horária semanal (PDF parseado) pode ter preview separada 🟡

## Evidência

- `.reversa/context/user-requirements.md#Saída Excel e visualização`
- `_reversa_sdd/ui/calendar-preview-view-spec.md`
