# Verificação de Calendário — Design Técnico

> Feature: `verificacao-calendario` | Legado: `verificar_calendario.py`

## Interface

### Legado (CLI)

| Entrada | Formato | Origem |
|---------|---------|--------|
| Proposta xlsx | `Proposta_3_Calendario_Provas_*_2SEM.xlsx` | pasta `OUT` hardcoded |
| Grade/regras | import `gerar_calendario as G` | módulo compartilhado |
| Ocupação prévia | `G.carregar_ocupadas()` | modelo xlsx |

| Saída | Formato | Destino |
|-------|---------|---------|
| PROBLEMA | lista strings | stdout, exit implícito |
| AVISO | lista strings | stdout |
| OK | mensagem | stdout |

### Plataforma alvo (🟡)

| Método | Caminho | Entrada | Saída |
|--------|---------|---------|-------|
| GET | `/api/v1/calendars/{id}/verification` | — | `VerificationReport` JSON |
| POST | `/api/v1/calendars/{id}/verify` | force refresh | `VerificationReport` |

```typescript
// VerificationReport (conceitual)
{
  calendario_id: string;
  proposta: 3;
  ok: boolean;
  problemas: VerificationFinding[];
  avisos: VerificationFinding[];
  checked_at: string;
}

interface VerificationFinding {
  item: string;       // "0", "10b", "11"
  regra_id?: string;  // "R-P1", "C4"
  turma: string;
  semana?: number;
  mensagem: string;   // siglas reais — UI coordenador
  severidade: "PROBLEMA" | "AVISO";
}
```

Componente: `CalendarVerifier` em `_reversa_sdd/c4-components.md`.

## Fluxo Principal

1. **`carregar_ocupadas()`** — preenche limites LP/LIT/RED conselho 🟢
2. **Classificar pares irmãos** — `comuns_por_par` via `G.classificar_par` 🟢
3. **Carregar workbook** — `openpyxl.load_workbook(..., data_only=True)` 🟢
4. **Por turma/aba** — parse células colunas E–I, semanas 1–20 🟢
5. **Extrair provas** — disciplina, professor, tempos, simulado, destaque cor 🟢
6. **Executar checklist 0–11** — acumula `problemas` / `avisos` 🟢
7. **Emitir resultado** — imprime contagens ou retorna JSON 🟢

Referência: `_reversa_sdd/flowcharts/verificacao-calendario.md`.

## Checklist — detalhe por item 🟢

| Item | Função legado | Notas |
|------|---------------|-------|
| 0 | `G.professor_presente_no_bloco` | Prioridade 1; turma ou irmã |
| 1 | contagem `por_sem` | Simulado multi-dia conta 1× |
| 2 | filtro grupo 1 | Exceção 2× com Inglês |
| 3 | `Counter` dias | |
| 4 | `INICIO_P1`, `LIMITE`, `FERIADOS`, `SEMANA_VETADA` | 🔴 sync feriados |
| 5–5c | contadores por disciplina | Port/Red/Gram separados = erro |
| 7b | `slots_da_disciplina` + `cedo` | P3 → `avisos` |
| 8 | `G.SIMULADOS` vs achados | |
| 9 | `G.cruza_intervalo` + cor célula | |
| 10 | `G.FORCAR_DATA` | |
| 10b | cessões agregadas por doador | C1–C5; relax → AVISO |
| 11 | `comuns_por_par` + `COORDENACAO_EXCECAO` | Fil/Soc isentas |

## Fluxos Alternativos

- **Proposta ≠ 3:** legado só itera `prop in (3,)` — outras propostas ignoradas 🟢
- **Célula vazia / cabeçalho:** filtrada (`unterrichtsfrei`, `Fach |`, etc.) 🟢
- **Regra flexibilizada (plataforma):** finding reclassificado PROBLEMA→AVISO se `RuleSetSnapshot` permite 🟡
- **Copiloto:** `ProfessorPseudonymService.anonymize_for_llm(report)` só na chamada OpenAI 🟢

## Dependências

- **openpyxl** — leitura xlsx 🟢
- **gerar_calendario (G)** — grade, funções domínio, constantes 🟢
- **geracao-calendario** — produz xlsx verificado 🟢
- **regras-negocio** — RuleSetSnapshot 🟡
- **plataforma-multi-coordenador** — VerificationPanel, gate fechar 🟡

## Decisões de Design Identificadas

| Decisão | Evidência | Confiança |
|---------|-----------|-----------|
| Releitura xlsx, não memória solver | ADR-002, início `main()` | 🟢 |
| AVISO tarde só Proposta 3 | L265 `destino = avisos if prop == 3` | 🟢 |
| COORDENACAO_EXCECAO hardcoded verificador | ADR-006 | 🟢 |
| Acoplamento import G | monolito legado | 🟢 |
| API JSON na plataforma | architecture CalendarVerifier | 🟡 |

## Estado Interno

| Estado | Onde | Ciclo |
|--------|------|-------|
| `provas_por_turma` | memória durante run | parse → checklist |
| `problemas`, `avisos` | listas acumuladoras | emit |
| `VerificationReport` | PostgreSQL cache 🟡 | invalidate on xlsx change |

## Observabilidade

- Legado: stdout contagem PROBLEMA/AVISO 🟢
- Plataforma: métricas por item/turma; feed copiloto 🟡

## Riscos e Lacunas

- 🔴 Divergência feriados gerador vs verificador
- 🟡 Duplicação lógica gerador/verificador — drift ao evoluir regras
- 🟡 Extração modular de checklist sem import circular ao refatorar
