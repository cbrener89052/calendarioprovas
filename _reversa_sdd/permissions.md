# Permissões — calendarioprovas

> Gerado pelo Detetive (Reversa).  
> Atualizado 2026-08-09 com decisões RBAC de Brener.

---

## Estado atual (legado CLI)

| Ator | Acesso | Confiança |
|---|---|---|
| Operador local (coordenação) | Todos os scripts, todos os arquivos na pasta | 🟢 |
| Sistema | Nenhuma autenticação, nenhum RBAC | 🟢 |

---

## Modelo futuro — segmento por coordenador 🟢

Cada **coordenador** configura o **segmento de atuação** na escola:

| Dimensão do segmento | Exemplo |
|---|---|
| Turmas/séries | 9C–12C, ou subset |
| Grupos de viagem | 10/12 vs 9/11 |
| Simulados do segmento | AG9, S4-12… |
| Regras ativas | toggles do catálogo |
| Customizações IA | preferências textuais, exceções documentadas |

**Tenant:** `coordenador_id` + `segmento_id` — dados isolados por coordenador.

---

## Papéis

| Papel | Escopo |
|---|---|
| **coordenador** | CRUD do próprio segmento, semestres, entradas, geração, toggles de regras |
| **admin_instituicao** | Catálogo institucional de regras, usuários, leitura cross-segmento 🟡 |
| **leitor** | Somente calendários publicados do segmento (opcional) |

---

## Matriz de permissões

| Recurso | coordenador | admin | leitor |
|---|---|---|---|
| Segmento próprio (config) | CRUD | R | — |
| Segmento de outro | — | R | — |
| Semestre / entradas / saídas | CRUD (próprio) | R | R (publicado) |
| Catálogo de regras (template) | R | CRUD | — |
| Toggle regra codificada | ✅ (próprio semestre) | ✅ | — |
| Customização IA (sem código) | CRUD (próprio) | R | — |
| Gerar / validar calendário | ✅ | ✅ | — |
| Publicar versão final | ✅ (próprio) | ✅ | — |

---

## Motor de regras — dois trilhos 🟢

```mermaid
flowchart LR
    subgraph Codificado
        CAT[Catálogo regras skill]
        TOG[Toggle ativo/inativo]
        SOL[Solver Python]
        CAT --> TOG --> SOL
    end
    subgraph IA
        CFG[Config coordenador]
        IA[Camada IA assistida]
        CFG --> IA
    end
    SOL --> OUT[Calendário]
    IA --> OUT
```

| Trilho | Quando usar | Persistência |
|---|---|---|
| **Codificado** | Restrição determinística (cessão, grupo 1, intervalo…) | `regra_config.ativo` + params JSON |
| **IA assistida** | Nuances, exceções pontuais, preferências que não viram PR | `customizacao_ia.texto` + contexto segmento |

**Regra de ouro:** customização IA **não substitui** verificação automática das regras codificadas ativas — complementa ou documenta exceções humanas.

---

## Lacunas 🔴

- Admin inicial (Brener) vs todos iguais?
- Customização IA entra no verificador ou só no relatório?
- Audit log de toggles e customizações
