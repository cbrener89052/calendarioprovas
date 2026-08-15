# C4 — Containers (Nível 2)

> Gerado pelo Arquiteto (Reversa) em 2026-08-15

## Legado 🟢

```mermaid
C4Container
    title Containers — Legado CLI

    Person(coord, "Coordenador")

    Container_Boundary(local, "Máquina local / Cloud Agent VM") {
        Container(cli, "Python CLI", "Python 3", "gerar/verificar/exportar")
        Container(fs, "Filesystem", "Pastas projeto", "xlsx, pdf, md")
        Container(git, "Git client", "Git", "main, producao")
    }

    Rel(coord, cli, "python script.py")
    Rel(cli, fs, "read/write")
    Rel(coord, git, "commit_github.bat")
```

## Alvo 🟡 — Docker Compose

```mermaid
C4Container
    title Containers — Plataforma (deploy híbrido)

    Person(coord, "Coordenador")

    Container_Boundary(docker, "Docker Compose") {
        Container(web, "Frontend Web", "Next.js ou similar", "UI coordenador")
        Container(api, "API Backend", "Python FastAPI", "REST + jobs")
        Container(db, "PostgreSQL", "PostgreSQL 16", "metadados, regras, auditoria")
        Container(store, "Blob Storage", "S3 / volume local", "arquivos xlsx/pdf")
    }

    Container_Ext(smtp, "SMTP", "E-mail transacional")

    Rel(coord, web, "HTTPS")
    Rel(web, api, "JSON/REST", "HTTPS")
    Rel(api, db, "SQL", "asyncpg/SQLAlchemy")
    Rel(api, store, "upload/download", "S3 API ou filesystem")
    Rel(api, smtp, "send mail", "SMTP/TLS")
```

### Responsabilidades por container

| Container | Responsabilidade | Origem legado |
|---|---|---|
| **Frontend** | Telas regras, fatoração, refração, fechar, envio e-mail | Novo |
| **API** | Orquestra solver, verificador, exportadores, auth | `gerar_calendario.py` + satélites |
| **PostgreSQL** | Usuários, calendários, perfis regras, log e-mails | Novo |
| **Blob** | Modelos, grades PDF, propostas xlsx | Pastas locais atuais |
| **SMTP** | E-mail doadores | Relatório trocas (manual hoje) |
