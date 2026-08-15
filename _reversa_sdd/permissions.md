# Permissões e papéis — calendarioprovas

> Gerado pelo Detetive (Reversa) em 2026-08-15  
> Prioridade: evolução **multi-coordenador** (requisito usuário 2026-08-09)

---

## Legado atual (CLI + arquivos locais)

| Papel | Quem | Permissões | Confiança |
|---|---|---|---|
| **Operador único** | Coordenador(es) com acesso à pasta/Git | Tudo: gerar, editar, verificar, exportar, commit | 🟢 |
| **Professor** | Destinatário passivo | Nenhum acesso ao sistema; recebe relatório/e-mail manual | 🟡 |
| **Escola (consumidor)** | Recebe xlsx final | Leitura dos artefatos em `producao` | 🟡 |

**RBAC no código:** 🔴 ausente — sem autenticação, sem ACL.

**Controle de acesso implícito:** 🟡 quem tem clone Git + pasta local = controle total.

---

## Plataforma futura (🟡 inferido de user-requirements)

### Papéis propostos

| Papel | Descrição | Confiança |
|---|---|---|
| **coordenador** | Monta calendário do seu escopo; fecha; envia e-mails | 🟢 |
| **coordenador_senior** | 🔴 LACUNA — templates institucionais? | 🔴 |
| **admin_instituicao** | Usuários, SMTP, templates e-mail, catálogo regras global | 🟡 |
| **professor** | 🔴 LACUNA — portal read-only das próprias cessões? | 🔴 |

Quantidade acordada: **5 coordenadores** com login individual 🟢.

---

## Matriz de permissões — coordenador (plataforma)

| Recurso / ação | coordenador (próprios dados) | outro coordenador | admin |
|---|---|---|---|
| Upload grade/modelo | ✅ | ❌ 🟡 | ✅ |
| Configurar regras (Tela 1–2) | ✅ | ❌ | ✅ read |
| Fatoração (gerar proposta) | ✅ | ❌ | ✅ |
| Refração (editar células) | ✅ | ❌ | ✅ |
| Verificar checklist | ✅ | ❌ | ✅ |
| Fechar calendário | ✅ | ❌ | ✅ |
| Exportar relatórios | ✅ | ❌ | ✅ |
| **Enviar e-mail doadores** | ✅ (manual) | ❌ | ✅ audit |
| Ver log envios e-mail | ✅ próprios | ❌ | ✅ todos |
| Promover a produção | 🟡 | ❌ | ✅ |
| Templates regras institucionais | read 🟡 | read 🟡 | write |

🟡 Isolamento entre coordenadores: **provável** dados isolados + templates compartilhados (pendente Arquiteto).

---

## Matriz — funcionalidade e-mail doadores

| Ação | Quem | Pré-condição | Confiança |
|---|---|---|---|
| Pré-visualizar cessões + e-mails | coordenador | `calendario.status >= fechado` | 🟢 |
| Confirmar envio em lote | coordenador | preview confirmado | 🟢 |
| Reenviar item obsoleto | coordenador | 🔴 política | 🔴 |
| Disparo automático pós-refração | — | **Proibido** (requisito explícito) | 🟢 |

---

## Dados sensíveis

| Dado | Classificação | Restrição |
|---|---|---|
| E-mail professor | PII | Só coordenador dono do calendário + admin |
| Grade horária | Operacional | Por coordenador 🟡 |
| Calendário fechado | Oficial escola | Branch `producao` 🟢 |

---

## Lacunas 🔴

1. Coordenador A pode **ver** calendário de B (read-only) ou isolamento total?
2. Existe papel **direção** que só aprova `producao`?
3. Professor autenticado no futuro ou só e-mail unidirecional?
4. Quem edita catálogo de regras **institucionais** vs **por coordenador**?
