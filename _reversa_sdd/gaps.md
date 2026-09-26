# Lacunas — calendarioprovas

> Gerado pelo Revisor (Fase 5), doc_level=completo.  
> Lacunas que permanecem sem resposta do usuário após revisão cruzada.

---

## Crítico (bloqueiam reimplementação fiel ou deploy)

| ID | Lacuna | Specs afetadas | Status |
|----|--------|----------------|--------|
| G-C01 | ~~LP/LIT/RED ≥10 dias~~ | geracao, verificacao, regras | ✅ PR #18 |
| ~~G-C02~~ | ~~Customização IA — escopo pipeline~~ | regras, verificacao | ✅ **Ambos** (verificador + relatório) |
| ~~G-C03~~ | ~~Admin institucional~~ | plataforma, permissions | ✅ Brener admin; coords isolados |

---

## Moderado

| ID | Lacuna | Specs afetadas | Status |
|----|--------|----------------|--------|
| ~~G-M01~~ | ~~Frontend web vs API-only~~ | plataforma | ✅ React Vite + Tailwind (ADR-007) |
| G-M02 | `RuleContext` / toggles — spec 🟡, zero código | geracao, regras | ADR-006; depende externalizar constantes |
| G-M03 | Validação cores ARGB no verificador | verificacao | Skill pede; verificador só texto |
| G-M04 | `requirements.txt` ausente | todas | Dependências implícitas |
| G-M05 | Testes automatizados ausentes | todas | architecture.md dívida alta |

---

## Cosmético / documentação

| ID | Lacuna | Nota |
|----|--------|------|
| G-K01 | Scripts utilitários sem spec dedicada | `limpar_grade_2025.py`, `contar_2sem_2025.py` — 🟡 na matrix |
| G-K02 | `*.bat` git sync | Substituído por CI na plataforma; n/a OK |
| G-K03 | OpenAPI draft 🟡 | Alinhado a contracts.md após revisão (customizacoes-ia adicionado) |

---

## Inconsistências corrigidas nesta revisão

| Item | Correção | Origem |
|------|----------|--------|
| MAX_NOS | Valores corretos 60000 / 5000 (não “~600 nós” como limite) | `[Revisão]` `gerar_calendario.py:657-664` |
| OpenAPI vs contracts | Endpoints `/customizacoes-ia` adicionados ao YAML | `[Revisão]` cross-spec |
| code-spec-matrix | `limpar_grade_2025.py`, `contar_2sem_2025.py` mapeados | `[Revisão]` inventory.md |

---

## Revisão cruzada entre features

| Verificação | Resultado |
|-------------|-----------|
| 7 features × 3 arquivos canônicos | ✅ Completo |
| Contradições internas (requirements ↔ design ↔ tasks) | ✅ Nenhuma crítica |
| Contradições entre features | ✅ Consistente (GRUPOS, RuleContext, PR #14) |
| `code-spec-matrix` vs inventory | 🟡 2 utilitários adicionados |
| `spec-impact-matrix` vs dependências | ✅ Alinhado |
| Codex revisão externa | Não realizada (engine indisponível) |

---

## Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial pós-revisão Fase 5 | reversa-reviewer |
