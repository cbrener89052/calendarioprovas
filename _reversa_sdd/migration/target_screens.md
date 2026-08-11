---
schemaVersion: 1
generatedAt: 2026-08-10T02:15:00Z
reversa:
  version: "1.2.58"
kind: target_screens
producedBy: screen_translator
mode: modernizado
---

# Target Screens — calendarioprovas

> Modo **modernizado**. Legado CLI sem UI; specs derivadas de ADR-007 e plataforma MVP.

## Design tokens (Tailwind)

| Token | Valor | Uso |
|-------|-------|-----|
| primary | blue-600 | CTAs, links |
| success | green-600 | Job OK, verificação pass |
| error | red-600 | Erros verificador |
| warning | amber-500 | Regras relaxadas |
| surface | gray-50 | Background |

Ver `_reversa_sdd/design-system/` se existir; senão tokens-default acima.

---

## SCR-01 — Login

**Rota**: `/login`  
**Atores**: coordenador, admin

```yaml
componentes:
  - Logo escola
  - Form: email, senha
  - Button: Entrar
  - Alert: erro auth
estados:
  idle: form vazio
  loading: button disabled + spinner
  error: "Email ou senha inválidos"
  success: redirect /dashboard
eventos:
  submit: POST /auth/login
```

---

## SCR-02 — Dashboard / Segmento

**Rota**: `/dashboard`  
**Atores**: coordenador

```yaml
componentes:
  - Header: nome segmento, logout
  - Card: semestre ativo
  - Nav: GRUPOS, Semestres, Regras, IA, Gerar, Calendários
estados:
  idle: dados segmento carregados
  loading: skeleton cards
  error: toast "Falha ao carregar segmento"
  success: —
eventos:
  mount: GET /segmento/me
```

---

## SCR-03 — GRUPOS (CRUD)

**Rota**: `/grupos`  
**Atores**: coordenador

```yaml
componentes:
  - Table: nome, início, fim, conselho, turmas count
  - Modal: criar/editar GRUPO
  - Fields: nome, data_inicio_semestre, data_fim_semestre,
            datas_segunda_chamada (multi-date), conselho_inicio, conselho_fim
  - Sub-table turmas por grupo
estados:
  idle: lista grupos
  loading: table skeleton
  error: validation messages inline
  success: toast "GRUPO salvo"
eventos:
  save: POST/PATCH /segmento/grupos
```

---

## SCR-04 — Semestre + Upload entradas

**Rota**: `/semestres/:id/entradas`  
**Atores**: coordenador

```yaml
componentes:
  - Breadcrumb: semestre ano/periodo
  - Upload zones: grade (xlsx/pdf), modelo, siglas, simulados
  - List: arquivos uploaded com checksum OK
estados:
  idle: uploads parciais ou completos
  loading: progress bar upload
  error: "Formato inválido" / "Upload falhou"
  success: badge verde por tipo
eventos:
  upload: POST /semestres/{id}/upload/{tipo}
```

---

## SCR-05 — Toggles regras

**Rota**: `/semestres/:id/regras`  
**Atores**: coordenador

```yaml
componentes:
  - Table: codigo, descricao, implementada_solver, toggle ativo
  - Badge: "só skill" se implementada_solver=false
  - Expand: params JSON editor (Should)
estados:
  idle: toggles refletem BD
  loading: switches disabled
  error: toast rollback
  success: toggle animado
eventos:
  toggle: PATCH /semestres/{id}/regras/{codigo}
```

---

## SCR-06 — Customizações IA

**Rota**: `/customizacoes-ia`  
**Atores**: coordenador

```yaml
componentes:
  - List: instrucoes registradas
  - Form: instrucao (textarea), contexto (textarea)
  - Hint: "Usado em verificador + relatório auxiliar; não altera solver"
estados:
  idle: lista + form
  loading: submit disabled
  error: validation
  success: item na lista
eventos:
  create: POST /segmento/customizacoes-ia
  delete: DELETE /segmento/customizacoes-ia/{id}
```

---

## SCR-07 — Gerar calendário (job)

**Rota**: `/semestres/:id/gerar`  
**Atores**: coordenador

```yaml
componentes:
  - Checklist pré-requisitos: entradas OK, GRUPOS OK
  - Button: Gerar Proposta 3
  - Progress: job status polling
  - Log panel: mensagens worker (opcional)
estados:
  idle: checklist
  loading: progress bar + "Gerando…"
  error: job failed + error message
  success: link para verificação/downloads
eventos:
  gerar: POST /semestres/{id}/gerar
  poll: GET /jobs/{id}
```

---

## SCR-08 — Verificação + Downloads

**Rota**: `/calendarios/:id`  
**Atores**: coordenador

```yaml
componentes:
  - Status badge: verificação OK / erros
  - Accordion: checks verificador (1-5, 5a-bis)
  - Buttons: download xlsx, tabela, cessões, trocas, relatório IA
  - Button: Publicar (disabled se erro crítico)
estados:
  idle: resultados carregados
  loading: fetching verificacao_result
  error: lista erros críticos
  success: publish enabled
eventos:
  download: GET /calendarios/{id}/download
  publish: POST /calendarios/{id}/publicar
```

---

## SCR-10 — Consulta de períodos e calendários gerados

**Rota**: `/calendarios`  
**Atores**: coordenador  
**Origem**: ADR-009, RF-15–RF-19 (Brener 2026-08-11)

> **Tela única:** consulta de **períodos letivos anteriores** e acesso aos **calendários já gerados** em cada período. Não existe rota separada de “histórico”.

```yaml
layout: master-detail
componentes:
  painel_periodos:
    - Filtros: ano (select), periodo (1|2|todos), ordenar (recente|antigo)
    - Lista/table: ano/periodo, inicio-fim, total_versoes, ultima_geracao, badge referencia_ativa
    - Empty: "Nenhum período com calendário — configure semestre e gere Proposta 3"
  painel_versoes:
    - Visível ao selecionar período (mesmo layout que antes era /semestres/:id/historico)
    - Table: versao, rotulo, gerado_em, status verificação, publicado
    - Row actions: Abrir (→ SCR-08), Download xlsx, Restaurar referência, Apagar
    - Modal confirmar apagar: "Esta ação não pode ser desfeita"
estados:
  idle: períodos carregados; versões vazias até seleção
  loading: skeleton em painel ativo
  error: toast por painel
  success: toast "Referência atualizada" / "Versão apagada"
eventos:
  list_periodos: GET /calendarios/consulta?ano=&periodo=&ordenar=
  select_periodo: GET /semestres/{id}/calendarios
  open: navigate /calendarios/{id}  # alias SCR-08 detalhe
  download: GET /calendarios/{id}/download
  restore: POST /calendarios/{id}/restaurar-referencia
  delete: DELETE /calendarios/{id} body { confirm: true }
navegacao:
  - Dashboard → Calendários
  - Pós-geração SCR-07 → redirect /calendarios?semestre={id} (período pré-selecionado)
  - Deep link SCR-08 → breadcrumb volta para /calendarios?semestre={id}
```

**Transparência:** após job OK em SCR-07, nova versão aparece no painel de versões do período (sem botão "Salvar").

---

## SCR-09 — Admin catálogo regras (Brener)

**Rota**: `/admin/regras`  
**Atores**: admin_instituicao

```yaml
componentes:
  - Table global regra_catalogo
  - CRUD: codigo, descricao, implementada_solver, skill_ref
  - Link: sync skill
estados: [idle, loading, error, success]
eventos:
  crud: /admin/regras/*
```

## Rastreabilidade

| Tela | Origem spec |
|------|-------------|
| SCR-01–08 | plataforma-multi-coordenador/design.md |
| SCR-10 | ADR-009, RF-15–RF-19 — consulta períodos + calendários |
| SCR-09 | permissions.md, RF-12 |
| Fluxo | user-stories/fluxo-calendario-semestre.md |
