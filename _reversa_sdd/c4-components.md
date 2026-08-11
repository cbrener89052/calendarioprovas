# C4 — Componentes (Nível 3)

## Container: Scripts Python CLI (legado)

```mermaid
C4Component
    title Componentes — geracao-calendario

    Container_Boundary(gerador, "gerar_calendario.py") {
        Component(main, "main", "Orquestra pipeline")
        Component(montar, "montar_proposta", "Escada afrouxamento")
        Component(resolver, "resolver / _tentar", "Backtracking")
        Component(resolver_par, "resolver_par", "Pares irmãos")
        Component(cessoes, "Cessoes", "Regras 1-5")
        Component(slots, "slots_da_disciplina", "Pré-computação")
        Component(escrever, "escrever", "openpyxl + cores")
        Component(relatorio, "relatorio", "MD trocas + relaxadas")
    }

    Rel(main, montar, "seed=7")
    Rel(montar, resolver_par, "primeiro")
    Rel(montar, resolver, "por turma")
    Rel(resolver, cessoes, "valida cada slot")
    Rel(resolver, slots, "consulta")
    Rel(main, escrever, "alocações OK")
    Rel(main, relatorio, "pós-escrita")
```

## Container: API Backend (futuro) 🟡

```mermaid
C4Component
    title Componentes propostos — FastAPI

    Container_Boundary(api, "API") {
        Component(auth, "AuthRouter", "JWT / OAuth")
        Component(semestre, "SemestreService", "CRUD semestre")
        Component(upload, "UploadService", "Blob + metadados")
        Component(job, "CalendarioJobService", "Dispara solver")
        Component(rules, "RulesService", "Skill versionada")
    }

    Rel(auth, semestre, "tenant scope")
    Rel(semestre, upload, "anexos")
    Rel(job, upload, "I/O arquivos")
```

## Acoplamentos críticos

| De | Para | Tipo |
|---|---|---|
| `verificar_calendario.py` | `gerar_calendario` | import direto 🟢 |
| `exportar_tempos_cedidos.py` | `gerar_calendario` + `exportar_tabelas_turma` | import 🟢 |
| Exportadores | xlsx em disco | leitura pós-gravação 🟢 |
