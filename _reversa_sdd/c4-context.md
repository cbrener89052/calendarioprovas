# C4 — Contexto (Nível 1)

> calendarioprovas — Escola Alemã Corcovado

```mermaid
C4Context
    title Diagrama de Contexto — calendarioprovas

    Person(coord, "Coordenador de provas", "Monta e valida calendário semestral")
    Person(prof, "Professor", "Recebe relatório de trocas de tempo")
    Person_Ext(future_coord, "Coordenador (futuro)", "5 usuários na plataforma")

    System(calendario, "calendarioprovas", "Gera, valida e exporta calendário de provas")

    System_Ext(untis, "Untis / PDF horários", "Horário-base semanal")
    System_Ext(excel, "Planilhas Excel", "Modelo Klausurplan, siglas, saídas")
    System_Ext(github, "GitHub", "Versionamento main/producao")
    System_Ext(simulados_pdf, "Calendário simulados", "Datas AG/S oficiais")

    Rel(coord, calendario, "Executa scripts, edita skill", "CLI / IDE")
    Rel(calendario, untis, "Lê grades", "PDF / OCR")
    Rel(calendario, excel, "Lê/escreve", "openpyxl")
    Rel(calendario, simulados_pdf, "Referência datas", "Manual / PDF")
    Rel(calendario, github, "Sync código e artefatos", "Git")
    Rel(calendario, prof, "Entrega relatórios", "xlsx / md")
    Rel(future_coord, calendario, "Usará plataforma web", "HTTPS 🔴 futuro")
```

## Personas

| Persona | Objetivo |
|---|---|
| Coordenador | Fechar calendário respeitando regras e carga docente |
| Professor | Saber quando cedeu tempo e quando aplica prova |
| Coordenador futuro | Mesmo fluxo, dados isolados na nuvem |
