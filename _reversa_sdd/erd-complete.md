# ERD Completo — calendarioprovas

> Legado (conceitual, hoje em arquivos) + plataforma futura (PostgreSQL proposto).

---

## Legado — entidades em arquivos 🟢

```mermaid
erDiagram
    TURMA ||--o{ CELULA_GRADE : tem
    TURMA ||--o{ ALOCACAO : recebe
    DISCIPLINA ||--o{ CELULA_GRADE : ocupa
    PROFESSOR ||--o{ CELULA_GRADE : leciona
    PROPOSTA ||--o{ ALOCACAO : contem
    SIMULADO ||--o{ ALOCACAO : fixa

    TURMA {
        string codigo PK
        string grupo
    }
    DISCIPLINA {
        string codigo PK
        string nome_exibicao
    }
    PROFESSOR {
        string sigla PK
        string nome_completo
    }
    CELULA_GRADE {
        int dia
        int tempo
        string turma FK
    }
    ALOCACAO {
        int semana
        int dia
        int tempo_inicio
        int n_tempos
        string disciplina
    }
    PROPOSTA {
        int numero PK
        datetime gerado_em
    }
```

---

## Plataforma futura — PostgreSQL 🟡

```mermaid
erDiagram
    COORDENADOR ||--o{ SEMESTRE : possui
    SEMESTRE ||--o{ ARQUIVO_ENTRADA : tem
    SEMESTRE ||--o{ CALENDARIO_GERADO : produz
    CALENDARIO_GERADO ||--o{ RELATORIO : gera
    INSTITUICAO ||--o{ COORDENADOR : emprega
    INSTITUICAO ||--o{ TEMPLATE_REGRAS : compartilha

    COORDENADOR {
        uuid id PK
        string email UK
        string nome
        string papel
    }
    INSTITUICAO {
        uuid id PK
        string nome
    }
    SEMESTRE {
        uuid id PK
        uuid coordenador_id FK
        int ano
        int periodo
        date inicio
        date fim
        jsonb config_grupos
    }
    ARQUIVO_ENTRADA {
        uuid id PK
        uuid semestre_id FK
        enum tipo
        string blob_path
        string content_hash
        datetime uploaded_at
    }
    CALENDARIO_GERADO {
        uuid id PK
        uuid semestre_id FK
        int proposta
        enum status
        string xlsx_blob_path
        datetime created_at
    }
    RELATORIO {
        uuid id PK
        uuid calendario_id FK
        enum tipo
        string blob_path
    }
    TEMPLATE_REGRAS {
        uuid id PK
        uuid instituicao_id FK
        string skill_version
        text conteudo_md
    }
```

### Tipos enum propostos

| Enum | Valores |
|---|---|
| `arquivo_tipo` | grade, modelo, simulados, siglas, referencia |
| `relatorio_tipo` | trocas, tabela_turma, tempos_cedidos |
| `calendario_status` | pending, running, validating, completed, failed |

---

## Mapeamento legado → BD

| Legado | Tabela/coluna futura |
|---|---|
| `GRADES` hardcoded | `grade_celula` + import de PDF |
| `Horario desenvolvido/*.xlsx` | `calendario_gerado` + blob |
| `siglas/*.xlsx` | `arquivo_entrada` tipo siglas |
| SKILL.md | `template_regras` + versionamento |
| `FORCAR_DATA`, simulados | `semestre.config` JSON ou tabelas filhas |

---

## Lacunas 🔴

- Normalização grade (por semestre vs snapshot imutável)
- Versionamento de propostas (histórico de reruns)
- Audit trail de quem relaxou regra 4
