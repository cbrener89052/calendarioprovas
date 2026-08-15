# Máquinas de estado — calendarioprovas

> Gerado pelo Detetive (Reversa) em 2026-08-15

---

## 1. Ciclo de vida do calendário (semestre)

Entidade central do domínio. Estados inferidos do fluxo Git + scripts + requisitos de plataforma.

```mermaid
stateDiagram-v2
    [*] --> EntradasCarregadas: upload grade/modelo/simulados
    
    EntradasCarregadas --> RegrasConfiguradas: Tela 1+2 regras (plataforma)
    EntradasCarregadas --> RegrasImplicitas: legado CLI hoje
    
    RegrasConfiguradas --> PropostaGerada: fatoração (solver)
    RegrasImplicitas --> PropostaGerada: gerar_calendario.py
    
    PropostaGerada --> EmRefracao: ajustes manuais xlsx
    EmRefracao --> EmRefracao: mais edições
    EmRefracao --> Verificado: verificar_calendario OK
    
    Verificado --> Fechado: coordenador aprova
    Fechado --> EmProducao: merge main → producao
    
    Fechado --> EmailsPendentes: cessões existem
    EmailsPendentes --> EmailsEnviados: coordenador confirma envio
    EmailsEnviados --> EmRefracao: mudança pós-envio (🔴 política)
    
    Fechado --> [*]: entrega escola
    EmProducao --> [*]
```

| Transição | Gatilho | Confiança |
|---|---|---|
| → PropostaGerada | `python gerar_calendario.py` | 🟢 |
| → EmRefracao | Edição células Proposta_3 xlsx | 🟢 |
| → Verificado | `verificar_calendario.py` sem PROBLEMA | 🟢 |
| → Fechado | Decisão humana / publicar | 🟡 |
| → EmProducao | `promover_para_producao.bat` | 🟢 |
| → EmailsEnviados | Ação manual coordenador | 🟡 (requisito) |

---

## 2. Relaxamento de cessão (por turma, Proposta 3)

Submáquina dentro do solver quando limites estritos não fecham.

```mermaid
stateDiagram-v2
    [*] --> Estrito: regras C1-C5 integrais
    
    Estrito --> Regra4Relaxada: falhou após escada interna
    Regra4Relaxada --> Regra3Relaxada: ainda falhou
    Regra3Relaxada --> FolgaExtra: folga_extra +1..+3
    
    FolgaExtra --> FechouTurma: alocação OK
    Regra4Relaxada --> FechouTurma
    Regra3Relaxada --> FechouTurma
    Estrito --> FechouTurma
    
    FechouTurma --> [*]
    FolgaExtra --> FalhouTurma: 12 iterações esgotadas
    FalhouTurma --> [*]
```

🟢 Confirmado em `montar_proposta()` / `main()` L2079–2126.

---

## 3. Escada interna do solver (por tentativa)

```mermaid
stateDiagram-v2
    [*] --> S0: max_intervalo=0, max_tarde=0, max_g1=1
    S0 --> S1: falhou
    S1 --> S2: incrementa limites
    S2 --> Sucesso: backtracking OK
    S2 --> Sn: escada esgotada
    Sucesso --> [*]
    Sn --> [*]
```

🟢 `escada()` L789–809.

---

## 4. Envio de e-mail ao doador (plataforma futura)

```mermaid
stateDiagram-v2
    [*] --> NaoAplicavel: calendário não fechado
    
    NaoAplicavel --> PreviewDisponivel: calendario.status = fechado
    
    PreviewDisponivel --> PreviewDisponivel: refração antes de enviar (lista atualiza)
    PreviewDisponivel --> Enviando: coordenador confirma
    Enviando --> ParcialmenteEnviado: falha SMTP em alguns
    Enviando --> Enviado: todos OK
    ParcialmenteEnviado --> Enviado: retry manual
    
    Enviado --> Desatualizado: calendário mudou pós-envio
    Desatualizado --> PreviewDisponivel: coordenador revisa
    
    Enviado --> [*]
```

🔴 Política de `Desatualizado` a definir com usuário.

---

## 5. Item de cessão (rastreabilidade e-mail)

| Estado | Significado |
|---|---|
| `calculada` | Existe no relatório de trocas |
| `email_pendente` | Calendário fechado, e-mail não enviado |
| `email_enviado` | Registro em `enviado_em` |
| `email_obsoleta` | Cessão removida ou alterada após envio |

🟡 Inferido dos requisitos de auditoria.
