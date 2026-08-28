# Domínio — calendarioprovas

> Gerado pelo Detetive (Reversa) em 2026-08-15  
> Fontes: código legado, skill `calendario-provas`, Git, `.reversa/context/user-requirements.md`  
> Escala: 🟢 CONFIRMADO | 🟡 INFERIDO | 🔴 LACUNA

---

## Glossário

| Termo | Definição | Confiança |
|---|---|---|
| **Turma** | Classe identificada por série + letra + número (ex.: `10C1`) | 🟢 |
| **Turma irmã** | Mesma série e letra, número final diferente (`10C1` ↔ `10C2`) | 🟢 |
| **Tempo** | Período do dia (1–11); preferência por evitar 7–11 (tarde) | 🟢 |
| **Prova / avaliação** | Evento de aplicação de exame; simulado conta como 1 avaliação/semana | 🟢 |
| **Simulado / AG** | Data fixa no calendário; amarelo exclusivo; não move | 🟢 |
| **Cessão / troca de tempo** | Disciplina doadora empresta slot para prova de outra | 🟢 |
| **Proposta** | Versão gerada do calendário; hoje só **Proposta 3** é desenvolvida | 🟢 |
| **Fatoração** | Geração automática (solver/backtracking) | 🟢 (requisito usuário) |
| **Refração** | Ajuste manual do calendário já gerado | 🟢 (requisito usuário) |
| **Fechar horário** | Aprovar versão final para entrega (`main` → `producao`) | 🟢 |
| **Grupo 1** | Mat, DaF, port/LPLITRED, Inglês — máx. 1/semana (exc. par com Inglês) | 🟢 |
| **LP/LIT/RED** | Prova combinada 3 tempos (10–12); port/pred separados no 9º | 🟢 |
| **Coordenador** | Usuário que monta o calendário (hoje: 1; futuro: 5 com login) | 🟡 |
| **Perfil de regras** | Conjunto de regras ativas/flexíveis por rodada (plataforma futura) | 🟡 |

---

## Entidades de negócio

### Calendário de provas (semestre)

- **Entrada:** grade horária, modelo xlsx, simulados, siglas, regras do semestre
- **Saída:** planilha por turma + relatórios derivados
- **Ciclo de vida:** rascunho → proposta gerada → refração manual → verificado → fechado → (opcional) promovido a `producao`

### Cessão de tempo

Tupla de negócio 🟢:

- Turma solicitante, disciplina/professor solicitante
- Data, tempo(s) emprestados
- Disciplina/professor **doador** (perde aula naquele slot)

Origem: campo `doador` na alocação `(w, d, t, n, disc, prof, doador)`.

### Professor

- Identificado por **sigla** na grade (ex.: `MFo`)
- Nome completo via planilha `siglas/siglas_profs_aux_etc.xlsx`
- Pode lecionar em várias turmas; pode ser doador ou solicitante de cessão
- 🔴 E-mail não confirmado no legado

---

## Regras de domínio — distribuição (🟢 confirmadas no código/skill)

### Prioridade e invioláveis

| ID | Regra | Relaxável? | Confiança |
|---|---|---|---|
| R-P1 | Professor presente no bloco de aplicação (turma ou irmã) | **Nunca** | 🟢 |
| R-FIX | Datas fixas (simulados, `FORCAR_DATA`) | **Nunca** | 🟢 |
| R-INT | Não cruzar intervalo recreio (3↔4, 5↔6) | Só último recurso | 🟢 |
| R-SEM | Máx. 3 avaliações/semana/turma | Não documentado relaxar | 🟢 |
| R-DIA | Uma prova por dia/turma | Não | 🟢 |
| R-G1 | Grupo 1: máx. 1/semana; exceção 2 com uma sendo Inglês | Sim, avisar | 🟢 |
| R-DIST | Distância mín. 4 semanas entre 2 provas mesma disc.; alvo 7 | Piso 4 rígido | 🟢 |

### Coordenação entre turmas irmãs

| ID | Regra | Confiança |
|---|---|---|
| R-IRM | Mesmo professor, horários diferentes → prova simultânea | 🟢 |
| R-IRM-COMB | Mesmo slot na grade → grupos paralelos, sem coordenação extra | 🟢 |
| R-FIL-SOC | Filosofia e Sociologia: **não** simultâneas entre irmãs (tempo próprio cada turma) | 🟢 |

Implementação: `COORDENACAO_EXCECAO` no verificador; regra fixa na skill (commit `e7b2202`).

### Cessão de aula (Proposta 3)

| # | Regra | Confiança |
|---|---|---|
| C1 | 2–3 aulas/semana → máx. 2 cessões (his/geo/GL → 3) | 🟢 |
| C2 | 1 aula/semana → não cede | 🟢 |
| C3 | Nunca 2 semanas seguidas sem contato | Relaxável (2º) | 🟢 |
| C4 | Não ceder véspera/própria prova (relaxação só **depois** da prova) | Relaxável (1º) | 🟢 |
| C5 | Teto 11% das aulas programadas | Relaxável (3º, +folga) | 🟢 |

Escada externa no `main()`: regra 4 → regra 3 → `folga_extra` por turma.

---

## Regras implícitas (🟡 inferidas do código/Git)

| ID | Regra implícita | Evidência | Confiança |
|---|---|---|---|
| I-01 | **Solver pode falhar** — relaxamento é feature, não bug | `montar_proposta` + loop 12 iterações | 🟢 |
| I-02 | **Seed importa** — mesma regra pode fechar ou não | `SEED_PROPOSTA_3=3`, comentários | 🟢 |
| I-03 | **Edição manual é normal** — relatórios releem planilha | `exportar_relatorio_trocas.py` docstring | 🟢 |
| I-04 | **Proposta 3 é a única oficial em desenvolvimento** | `main()` só gera prop 3; verificador `for p in (3,)` | 🟢 |
| I-05 | **Checklist distingue PROBLEMA vs AVISO** para cessão relaxada | `verificar_calendario.py` item 10b | 🟢 |
| I-06 | **Feriados duplicados** em `BLOQUEIOS` e `FERIADOS` — sync manual | Bug 02/11 documentado na skill | 🟢 |
| I-07 | **Grade 2º sem 2026 hardcoded** — não vem de PDF | `GRADE_TXT` em `gerar_calendario.py` | 🟢 |
| I-08 | **Consolidação de semanas** é revisão humana pós-solver | Skill: não é regra do algoritmo | 🟡 |
| I-09 | **ENEM configurável** — Must na plataforma (`EnemWeekConfig`); 🔴 legado | ADR-015; skill item 15 | 🟡 |
| I-10 | **Véspera 2ª chamada 9C** — Won't automatizar v1; checklist manual | ADR-015 alinhado L-01 | 🟢 |
| I-11 | **Comunicação com doadores** hoje = relatório manual; e-mail = plataforma | user-requirements 2026-08-15 | 🟢 |

---

## Regras futuras (plataforma — 🟡/🔴)

Declaradas em `.reversa/context/user-requirements.md`:

| Feature | Descrição | Confiança |
|---|---|---|
| **Seleção de regras** | Tela 1: aplicar/flexibilizar; Tela 2: regras novas fixas ou sessão | 🟢 |
| **E-mail doadores** | Envio manual pós-fechamento; não a cada refração | 🟢 |
| **Multi-coordenador** | Conta compartilhada + 5 PINs; dados por PIN; PostgreSQL | 🟢 ADR-015 |
| **Catálogo 37 regras** | Commit `74568b4` menciona seed catálogo — 🔴 não no workspace atual | 🔴 |

---

## Invariantes de qualidade

1. **`verificar_calendario.py` → zero PROBLEMA** antes de entregar 🟢
2. Após edição manual: rodar 5 scripts exportadores 🟢 (skill)
3. Promover `main` → `producao` só após validação 🟡 (`fluxo-git-main-producao.md`)
4. Nunca regenerar calendário só para atualizar relatório — usar exportadores 🟢

---

## Lacunas 🟡 (moderadas)

1. E-mail dos professores na planilha de siglas
2. Perfil de regras: por coordenador, semestre ou ambos
3. Idioma oficial dos e-mails (PT/DE)
4. Export PDF regras v2+ (Could — M-08)
