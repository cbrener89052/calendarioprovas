# Permissões — calendarioprovas

> Gerado pelo Detetive (Reversa).

---

## Estado atual (legado CLI)

| Ator | Acesso | Confiança |
|---|---|---|
| Operador local (coordenação) | Todos os scripts, todos os arquivos na pasta | 🟢 |
| Sistema | Nenhuma autenticação, nenhum RBAC | 🟢 |

**Conclusão:** RBAC **não é central** no legado — matriz vazia por design.

---

## Estado futuro (plataforma multi-coordenador) 🟡

Decisões em `.reversa/context/user-requirements.md`: 5 coordenadores, login individual, dados isolados por coordenador (provável).

### Papéis propostos

| Papel | Descrição |
|---|---|
| **coordenador** | CRUD dos próprios semestres, grades, modelos, geração |
| **admin_instituicao** | Templates compartilhados, regras institucionais, usuários |
| **leitor** | Somente leitura dos calendários publicados (opcional) |

### Matriz de permissões (proposta)

| Recurso | coordenador | admin_instituicao | leitor |
|---|---|---|---|
| Próprio semestre (entradas/saídas) | CRUD | R | R |
| Semestre de outro coordenador | — | R | — |
| Templates institucionais (skill base) | R | CRUD | R |
| Gerar calendário | ✅ próprio | ✅ qualquer | — |
| Promover/publicar versão final | ✅ próprio | ✅ | — |
| Gerenciar usuários | — | CRUD | — |

### Isolamento de dados

- **Tenant key:** `coordenador_id` em todas as tabelas de negócio 🟡
- **Blobs:** prefixo `{coordenador_id}/{semestre_id}/` no storage 🟡
- **Regras compartilhadas:** versão read-only da skill institucional; override por semestre 🔴 a definir

---

## Lacunas 🔴

- Admin vs coordenador: Brener é único admin inicial?
- Coordenadores compartilham turmas entre si?
- Audit log obrigatório?

Detalhar na fase **Redator** após validação com usuário.
