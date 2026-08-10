# Scripts CLI legado (referência / paridade)

Durante a fase **Strangler Fig**, os scripts operacionais permanecem na **raiz do repositório**:

| Script | Função |
|--------|--------|
| `gerar_calendario.py` | Solver Proposta 3 |
| `verificar_calendario.py` | Checklist pós-geração |
| `exportar_*.py` | Relatórios |

A extração para `packages/solver/` ocorre na **Tarefa 4** do `reconstruction-plan.md`. Até lá, use os scripts da raiz para Parallel Run.

## Paridade

Comparar saídas CLI vs plataforma conforme `cutover_plan.md` e `parity_tests/`.
