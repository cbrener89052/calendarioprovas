# ERD Completo — calendarioprovas

> Gerado pelo Arquiteto (Reversa) em 2026-08-15  
> Inclui modelo **legado conceitual** (arquivos) e **alvo PostgreSQL** (multi-coordenador)

---

## 1. Legado — modelo conceitual (sem BD) 🟢

Entidades inferidas de pastas e scripts; persistência = filesystem.

```mermaid
erDiagram
    MODELO_XLSX ||--o{ PROPOSTA_XLSX : "template"
    GRADE_PDF ||--o{ GRADE_DADOS : "extrai"
    PROPOSTA_XLSX ||--o{ ALOCACAO : "contém"
    PROPOSTA_XLSX ||--o{ RELATORIO : "gera"
    SIGLAS_XLSX ||--o{ PROFESSOR : "mapeia"
    ALOCACAO }o--|| PROFESSOR : "solicitante"
    ALOCACAO }o--o| PROFESSOR : "doador"

    MODELO_XLSX {
        string path PK
        string semestre
    }
    PROPOSTA_XLSX {
        string path PK
        int numero_proposta
        string status "rascunho|verificado|fechado"
    }
    ALOCACAO {
        int semana
        int dia
        int tempo_ini
        int n_tempos
        string disciplina
        string prof_solicitante
        string prof_doador "nullable"
    }
    PROFESSOR {
        string sigla PK
        string nome
    }
    RELATORIO {
        string tipo "trocas|cedidos|turma|prof"
        string path
    }
```

---

## 2. Alvo — PostgreSQL multi-coordenador 🟡

### Diagrama principal

```mermaid
erDiagram
    USUARIO ||--o{ CALENDARIO : "possui"
    USUARIO {
        uuid id PK
        string email UK
        string nome
        string papel "coordenador|admin"
        timestamp criado_em
    }

    CALENDARIO ||--|| PERFIL_REGRAS : "usa"
    CALENDARIO ||--o{ ARQUIVO_BLOB : "anexos"
    CALENDARIO ||--o{ ALOCACAO_PROVA : "contém"
    CALENDARIO ||--o{ ENVIO_EMAIL : "dispara"
    CALENDARIO {
        uuid id PK
        uuid usuario_id FK
        string semestre
        string status "rascunho|gerado|verificado|fechado|producao"
        int seed_solver
        timestamp fechado_em
        timestamp criado_em
    }

    PERFIL_REGRAS ||--o{ PERFIL_REGRA_ITEM : "itens"
    PERFIL_REGRAS {
        uuid id PK
        uuid calendario_id FK
        string escopo "rodada|fixo"
    }

    REGRA_CATALOGO ||--o{ PERFIL_REGRA_ITEM : "referencia"
    REGRA_CATALOGO {
        uuid id PK
        string codigo UK
        string descricao
        boolean flexivel_padrao
        boolean inegociavel
        int ordem_relaxamento
        boolean institucional
    }

    PERFIL_REGRA_ITEM {
        uuid id PK
        uuid perfil_id FK
        uuid regra_id FK
        boolean aplicar
        boolean flexibilizar
    }

    ALOCACAO_PROVA ||--o| CESSAO : "pode ter"
    ALOCACAO_PROVA {
        uuid id PK
        uuid calendario_id FK
        string turma
        int semana
        int dia
        int tempo_ini
        int n_tempos
        string disciplina
        string prof_solicitante
    }

    CESSAO {
        uuid id PK
        uuid alocacao_id FK
        string disc_doadora
        string prof_doador
        int tempo_doado
    }

    PROFESSOR_INST ||--o{ CESSAO : "doador"
    PROFESSOR_INST {
        uuid id PK
        string sigla UK
        string nome
        string email "nullable LACUNA"
    }

    ENVIO_EMAIL ||--o{ ENVIO_EMAIL_ITEM : "itens"
    ENVIO_EMAIL {
        uuid id PK
        uuid calendario_id FK
        uuid usuario_id FK
        timestamp enviado_em
        string status "enviado|parcial|falha"
    }

    ENVIO_EMAIL_ITEM {
        uuid id PK
        uuid envio_id FK
        uuid cessao_id FK
        string email_destino
        string status "ok|falha|obsoleto"
    }

    ARQUIVO_BLOB {
        uuid id PK
        uuid calendario_id FK
        string tipo "modelo|grade|proposta|relatorio"
        string storage_key
        string mime
    }
```

---

## 3. Cardinalidades e constraints

| Relacionamento | Cardinalidade | Regra |
|---|---|---|
| Usuario → Calendario | 1:N | Coordenador só vê os seus 🟡 |
| Calendario → PerfilRegras | 1:1 | Um perfil por rodada de geração |
| RegraCatalogo → PerfilRegraItem | 1:N | Catálogo institucional + overrides |
| Alocacao → Cessao | 1:0..1 | Nem toda prova empresta tempo |
| Calendario → EnvioEmail | 1:N | Múltiplos envios possíveis 🔴 política |
| Cessao → EnvioEmailItem | 1:N | Reenvio / obsoleto |

---

## 4. Índices sugeridos 🟡

- `calendario(usuario_id, semestre, status)`
- `alocacao_prova(calendario_id, turma, semana, dia)`
- `cessao(prof_doador_id)` — listagem e-mail
- `envio_email(calendario_id, enviado_em DESC)`

---

## 5. Migração legado → BD 🔴

| Legado | Tabela alvo |
|---|---|
| `Klausurplan_*.xlsx` | `arquivo_blob` tipo=modelo |
| `Horario desenvolvido/Proposta_3_*.xlsx` | `arquivo_blob` + parse → `alocacao_prova` |
| Tupla `(doador)` no solver | `cessao` |
| `siglas_profs_aux_etc.xlsx` | `professor_inst` |
| Skill regras | seed `regra_catalogo` |
| `Relatorio_trocas` | view/query sobre `cessao` |
