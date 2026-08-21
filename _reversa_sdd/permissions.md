# Permissões e papéis — calendarioprovas

> Gerado pelo Detetive (Reversa) em 2026-08-15  
> **Atualizado 2026-08-21:** Auth confirmado ADR-015 (conta + PIN)

---

## Legado atual (CLI + arquivos locais)

| Papel | Quem | Permissões | Confiança |
|---|---|---|---|
| **Operador único** | Coordenador(es) com acesso à pasta/Git | Tudo: gerar, editar, verificar, exportar, commit | 🟢 |
| **Professor** | Destinatário passivo | Nenhum acesso ao sistema; recebe relatório/e-mail manual | 🟡 |
| **Escola (consumidor)** | Recebe xlsx final | Leitura dos artefatos em `producao` | 🟡 |

**RBAC no código:** 🔴 ausente — sem autenticação, sem ACL.

---

## Plataforma futura (ADR-015 🟢)

### Modelo de acesso

1. **Login institucional** — uma conta compartilhada (credencial escola).
2. **Seleção de PIN** — após login, coordenador informa PIN de 4–6 dígitos (5 cadastrados).
3. **Sessão** — `coordenador_id` + nome exibido; toda ação auditada com PIN/usuário.
4. **Isolamento** — calendários, uploads e exports filtrados por `coordenador_id` do PIN ativo.

### Papéis

| Papel | Descrição | Confiança |
|---|---|---|
| **coordenador** | PIN individual; ciclo completo nos próprios dados | 🟢 |
| **admin_instituicao** | Gerencia PINs, SMTP, templates | 🟢 |
| **professor** | Fora do escopo v1 | 🟡 |

Quantidade: **5 coordenadores** = **5 PINs** 🟢.

---

## Matriz de permissões — coordenador (plataforma)

| Recurso / ação | coordenador (próprio PIN) | outro PIN | admin |
|---|---|---|---|
| Upload grade/modelo | ✅ | ❌ | ✅ |
| `EnemWeekConfigPanel` | ✅ | ❌ | ✅ read |
| Configurar regras (Tela 1–2) | ✅ | ❌ | ✅ read |
| Fatoração | ✅ | ❌ | ✅ |
| Fechar calendário | ✅ | ❌ | ✅ |
| Enviar e-mail doadores | ✅ | ❌ | ✅ audit |

🟢 Isolamento: row-level por `coordenador_id` do PIN; templates institucionais read-only compartilhados.

---

## Matriz — funcionalidade e-mail doadores

| Ação | Quem | Pré-condição | Confiança |
|---|---|---|---|
| Preview cessões | Coordenador (PIN ativo) | Calendário fechado | 🟢 |
| Enviar e-mail | Coordenador (PIN ativo) | Confirmação explícita | 🟢 |

---

## Lacunas RBAC

- 🔴 Rotação/revogação de PIN — política a definir na forward
- 🟡 Timeout sessão após inatividade com PIN "lembrado" no browser
