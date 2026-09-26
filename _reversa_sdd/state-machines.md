# Máquinas de estado — calendarioprovas

> Gerado pelo Detetive (Reversa).

---

## 1. Ciclo de vida de uma Proposta de calendário

```mermaid
stateDiagram-v2
    [*] --> CarregarModelo: main()
    CarregarModelo --> ResolverPares: carregar_ocupadas()
    ResolverPares --> ResolverTurmas: resolver_par() OK
    ResolverTurmas --> EscreverXlsx: resolver() todas turmas
    EscreverXlsx --> Relatorio: escrever()
    Relatorio --> [*]: relatorio() + verificar (manual)

    ResolverPares --> Afrouxar: falhou
    ResolverTurmas --> Afrouxar: falhou
    Afrouxar --> Regra4: sem_regra4 += turma
    Regra4 --> Regra3: ainda falhou
    Regra3 --> Tetos: sem_regra3 += turma
    Tetos --> FalhaFinal: ainda falhou
    FalhaFinal --> [*]: log erro
    Regra4 --> ResolverPares: retry montar_proposta
    Regra3 --> ResolverPares: retry
    Tetos --> ResolverPares: retry folga+1
```

**Estados implícitos:** `folga` (incremento de tetos), `sem_regra3`, `sem_regra4` por turma 🟢

---

## 2. Backtracking por turma (`resolver`)

```mermaid
stateDiagram-v2
    [*] --> OrdenarExames: escada()
    OrdenarExames --> TentarExame: índice i
    TentarExame --> AplicarCessao: slot válido
    AplicarCessao --> Recursao: Cessoes.aplicar()
    Recursao --> Sucesso: i == n
    Recursao --> TentarExame: próximo slot
    Recursao --> Desfazer: falhou
    Desfazer --> TentarExame: Cessoes.desfazer()
    Sucesso --> [*]
    TentarExame --> Falha: sem slots / MAX_NOS
    Falha --> [*]
```

---

## 3. Classe `Cessoes` — decisão por slot candidato

```mermaid
flowchart TD
    A[pode_ceder_bloco] --> B{1 aula/sem?}
    B -->|Sim| N[Não cede]
    B -->|Não| C{Teto regra 1/5?}
    C -->|Estourou| N
    C -->|OK| D{Regra 3 sem contato?}
    D -->|Viola| N
    D -->|OK| E{Regra 4 vésperas?}
    E -->|Viola estrita| N
    E -->|Relaxada: só depois prova| F{Antes/no dia prova?}
    F -->|Sim| N
    F -->|Não| OK[Permite cessão]
    E -->|OK estrita| OK
```

---

## 4. Fluxo Git de validação (operacional)

```mermaid
stateDiagram-v2
    [*] --> MainDev: edição skill/código
    MainDev --> Gerar: python gerar_calendario.py
    Gerar --> Verificar: python verificar_calendario.py
    Verificar --> MainDev: problemas
    Verificar --> Promover: OK
    Promover --> Producao: promover_para_producao.bat
    Producao --> [*]
```

🟡 Inferido de `referencia/fluxo-git-main-producao.md`

---

## 5. Plataforma futura — job de geração (proposto)

```mermaid
stateDiagram-v2
    [*] --> Pending: POST /calendarios
    Pending --> Running: worker inicia
    Running --> Validating: solver OK
    Validating --> Completed: verificar OK
    Validating --> Failed: checklist falhou
    Running --> Failed: solver falhou
    Completed --> [*]
    Failed --> [*]
```

🔴 Lacuna — não implementado; 🟡 inferido para FastAPI + fila
