# Perguntas para Validação — calendarioprovas

> Gerado pelo Revisor em 2026-08-09  
> Brener, responda cada pergunta abaixo (campo **Resposta:**) e avise quando terminar — digite `reversa` ou responda no chat.

---

## Pergunta 1

**Contexto:** RBAC futuro — `permissions.md` define papel `admin_instituicao` com CRUD de catálogo de regras e leitura cross-segmento, mas `user-requirements.md` lista como pendente.  
**Spec afetada:** [`_reversa_sdd/plataforma-multi-coordenador/requirements.md`], [`_reversa_sdd/permissions.md`]  
**Pergunta:** Você (Brener) será o **admin institucional inicial** com acesso a todos os segmentos, ou cada um dos 5 coordenadores terá apenas o papel `coordenador` (sem admin)? Haverá um 6º usuário admin?  
**Impacto:** Define RF-12, matriz de permissões e escopo do MVP de auth.

**Resposta:** <!-- preencha aqui -->

---

## Pergunta 2

**Contexto:** ADR-006 — customizações assistidas por IA persistidas em `CUSTOMIZACAO_IA`. Specs divergem sobre onde a camada IA atua após o solver determinístico.  
**Spec afetada:** [`_reversa_sdd/regras-negocio/design.md`], [`_reversa_sdd/verificacao-calendario/requirements.md`]  
**Pergunta:** Customizações IA devem entrar no **verificador** (checks adicionais interpretados por IA), apenas no **relatório auxiliar** pós-geração, ou **ambos**?  
**Impacto:** Escopo de RF do verificador, pipeline worker e custo de API IA.

**Resposta:** <!-- preencha aqui -->

---

## Pergunta 3

**Contexto:** Stack declarada: FastAPI + PostgreSQL + frontend “a definir” (`user-requirements.md`). OpenAPI e user stories assumem browser.  
**Spec afetada:** [`_reversa_sdd/plataforma-multi-coordenador/design.md`], [`_reversa_sdd/plataforma-multi-coordenador/tasks.md` T-13]  
**Pergunta:** O MVP da plataforma pode ser **API-only** (coordenadores usam via Claude/Cursor/scripts temporariamente) ou exige **frontend web** na v1? Se web, há preferência (Next.js, React simples, outro)?  
**Impacto:** Escopo T-13, Docker Compose (serviço frontend), cronograma de migração.

**Resposta:** <!-- preencha aqui -->

---

## Pergunta 4 (confirmacao rapida)

**Contexto:** PR #14 mergeada — LP/LIT/RED ≥10 dias antes do conselho. Skill ✅, `gerar_calendario.py` / `verificar_calendario.py` 🔴.  
**Spec afetada:** [`_reversa_sdd/geracao-calendario/tasks.md` T-06], [`_reversa_sdd/regras-negocio/tasks.md` T-08]  
**Pergunta:** Confirma que a implementação desta regra no código é **prioridade Must** antes do deploy da plataforma (não pode ir para produção sem ela)?  
**Impacto:** Ordenação do backlog; bloqueio de “publicar” na plataforma.

**Resposta:** <!-- preencha aqui -->
