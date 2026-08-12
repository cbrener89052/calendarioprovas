# Scripts CLI legado (referência / paridade)

Durante a fase **Strangler Fig**, os scripts operacionais permanecem na **raiz do repositório**:

| Script | Função |
|--------|--------|
| `gerar_calendario.py` | Solver Proposta 3 |
| `verificar_calendario.py` | Checklist pós-geração |
| `exportar_*.py` | Relatórios |

A extração para `packages/solver/` foi concluída na **Tarefa 5** (`reconstruction-plan.md`).

**Fonte da verdade:** scripts canônicos permanecem na **raiz do repositório GitHub
`main`**. `packages/solver/` é wrapper importável — sincronize sempre com `git pull`
antes de comparar paridade.

## API importável (plataforma)

```python
from ingest.models import GradeSnapshot
from solver import generate_proposta3, verify_xlsx

result = generate_proposta3(snapshot, modelo_xlsx=..., output_dir=...)
verification = verify_xlsx(result.xlsx_path)
# verification.problemas → bloqueia entrega (ADR-010)
# verification.avisos → informativo
```

Para paridade com o CLI hardcoded:

```python
from solver import generate_proposta3_legacy
result = generate_proposta3_legacy()
```

## Paridade

Comparar saídas CLI vs plataforma conforme `cutover_plan.md` e `parity_tests/`.

Testes: `pytest packages/solver/tests -m "not slow"` (rápido). Smoke completo: `RUN_SLOW=1 pytest packages/solver/tests -m slow`.
