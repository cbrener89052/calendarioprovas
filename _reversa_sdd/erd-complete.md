# ERD Completo — calendarioprovas

> Legado (conceitual, hoje em arquivos) + plataforma futura (PostgreSQL proposto).

---

## Legado — entidades em arquivos 🟢

```mermaid
erDiagram
    TURMA }o--|| GRUPO : pertence
    TURMA ||--o{ CELULA_GRADE : tem
    TURMA ||--o{ ALOCACAO : recebe
    DISCIPLINA ||--o{ CELULA_GRADE : ocupa
    PROFESSOR ||--o{ CELULA_GRADE : leciona
    PROPOSTA ||--o{ ALOCACAO : contem
    SIMULADO ||--o{ ALOCACAO : fixa

    TURMA {
        string codigo PK
        string grupo_codigo FK "legado: 10_12, 9_11 → futuro: GRUPO.id"
    }
    GRUPO {
        string codigo PK "legado: 10_12, 9_11"
        date inicio_semestre
        date fim_semestre
        date segunda_chamada
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
    INSTITUICAO ||--o{ COORDENADOR : emprega
    COORDENADOR ||--|| SEGMENTO : configura
    SEGMENTO ||--o{ GRUPO : define
    GRUPO ||--o{ TURMA : agrupa
    SEGMENTO ||--o{ SEMESTRE : escopo
    SEMESTRE ||--o{ ARQUIVO_ENTRADA : tem
    SEMESTRE ||--o{ CALENDARIO_GERADO : produz
    CALENDARIO_GERADO ||--o{ RELATORIO : gera
    INSTITUICAO ||--o{ REGRA_CATALOGO : publica
    SEGMENTO ||--o{ REGRA_CONFIG : toggles
    SEGMENTO ||--o{ CUSTOMIZACAO_IA : preferencias
    REGRA_CATALOGO ||--o{ REGRA_CONFIG : instancia

    COORDENADOR {
        uuid id PK
        string email UK
        string nome
    }
    SEGMENTO {
        uuid id PK
        uuid coordenador_id FK UK
        string nome
    }
    GRUPO {
        uuid id PK
        uuid segmento_id FK
        string nome
        date data_inicio_semestre
        date data_fim_semestre
        jsonb datas_segunda_chamada
        date conselho_inicio
        date conselho_fim
    }
    TURMA {
        uuid id PK
        uuid grupo_id FK
        string codigo UK
    }
    SEMESTRE {
        uuid id PK
        uuid segmento_id FK
        int ano
        int periodo
        date inicio
        date fim
    }
    REGRA_CATALOGO {
        uuid id PK
        string codigo UK
        string descricao
        bool implementada_solver
        string skill_ref
    }
    REGRA_CONFIG {
        uuid id PK
        uuid segmento_id FK
        uuid regra_id FK
        uuid semestre_id FK
        bool ativo
        jsonb params
    }
    CUSTOMIZACAO_IA {
        uuid id PK
        uuid segmento_id FK
        uuid semestre_id FK
        text instrucao
        text contexto
        datetime created_at
    }
    ARQUIVO_ENTRADA {
        uuid id PK
        uuid semestre_id FK
        enum tipo
        string blob_path
    }
    INGEST_SNAPSHOT {
        uuid id PK
        uuid semestre_id FK
        uuid arquivo_entrada_id FK
        enum status
        enum source_format
        string checksum
        jsonb warnings
    }
    GRADE_CELULA {
        uuid id PK
        uuid ingest_snapshot_id FK
        uuid turma_id FK
        int dia
        int tempo
        string disciplina
        string professor
    }
    CALENDARIO_GERADO {
        uuid id PK
        uuid semestre_id FK
        uuid job_id FK
        int versao
        string rotulo
        enum status
        bool referencia_ativa
        string xlsx_blob_path
        jsonb verificacao_result
        timestamptz publicado_em
        timestamptz deleted_at
    }
    RELATORIO {
        uuid id PK
        uuid calendario_id FK
        enum tipo
        string blob_path
    }
```

> Nota: entidade `INSTITUICAO` e `REGRA_CATALOGO` substituem o modelo anterior `TEMPLATE_REGRAS` único — catálogo + toggles por segmento.

### Tipos enum propostos

| Enum | Valores |
|---|---|
| `arquivo_tipo` | grade, modelo, simulados, siglas, referencia |
| `relatorio_tipo` | trocas, tabela_turma, tempos_cedidos |
| `calendario_status` | pending, running, validating, completed, failed |
| `ingest_snapshot_status` | draft, pending_review, approved, rejected |
| `ingest_source_format` | pdf, xlsx, legacy_py |

---

## Mapeamento legado → BD

| Legado | Tabela/coluna futura |
|---|---|
| `LIMITE` / `grupo_turma()` | `grupo.data_fim_semestre` |
| `SEMANA_VETADA` | `grupo.conselho_inicio/fim` |
| 2CH no modelo xlsx | `grupo.datas_segunda_chamada` |
| Turmas 9C–12C | `turma.grupo_id` → GRUPO nomeado pelo coordenador |
| `GRADES` hardcoded | `grade_celula` + import de PDF |
| `Horario desenvolvido/*.xlsx` | `calendario_gerado` + blob |
| `siglas/*.xlsx` | `arquivo_entrada` tipo siglas |
| SKILL.md | `regra_catalogo` (seed) + toggles |
| Toggles hardcoded → config | `regra_config.ativo` |
| Preferências textuais | `customizacao_ia` |

---

## Lacunas 🔴

- ~~Normalização grade (por semestre vs snapshot imutável)~~ → ADR-008 snapshot aprovado
- ~~Versionamento de propostas (histórico de reruns)~~ → ADR-009 histórico calendários
- Audit trail de quem relaxou regra 4
