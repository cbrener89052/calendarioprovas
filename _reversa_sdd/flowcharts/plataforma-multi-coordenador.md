# Fluxograma — plataforma-multi-coordenador (futuro)

> 🔴 LACUNA — não implementado. Requisitos em `.reversa/context/user-requirements.md`.

```mermaid
flowchart TD
    LOGIN[Login coordenador] --> T1[Tela 1: catálogo regras skill]
    T1 --> D1[Default: todas aplicar]
    T1 --> D2[Marcar flexibilizáveis]
    T1 --> D3[Inegociáveis: mesma tela, flex bloqueado]
    T1 --> T2[Tela 2: regras novas?]
    T2 --> E{Fixa ou sessão?}
    E --> FAT[Fatoração automática solver]
    FAT --> VER0[Verificador + estatísticas]
    VER0 --> COPILOT[Chat Copiloto OpenAI + RAG]
    COPILOT --> QA[Perguntas sobre horário gerado]
    COPILOT --> VIEWS[Visões e documentos de base]
    FAT --> REF[Refração manual opcional]
    REF --> COPILOT
    QA --> PROP[Propostas de alteração opcionais]
    PROP --> REF
    REF --> VER[Re-verificação]
    VER --> GATE[Revisar regras antes de fechar]
    GATE --> FECHAR[Fechar horário / publicar]
    FECHAR --> EMAIL[Enviar e-mails doadores — manual]
    
    FAT --> PG[(PostgreSQL perfil regras)]
    FECHAR --> PG
    EMAIL --> AUDIT[(Log envios e-mail)]
```

**Nota:** o nó `EMAIL` é **ação explícita** do coordenador, não automática após refração.
