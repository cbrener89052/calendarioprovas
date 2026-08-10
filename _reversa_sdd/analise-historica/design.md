# Análise Histórica — Design Técnico

## Interface

| Símbolo | Assinatura | Retorno |
|---------|-----------|---------|
| `tempos_do_texto` | `(txt)` | `list[int]` |
| `main` (comparar) | `()` | void + stdout |

## Entidade ComparativoCessao

turma, disciplina, pct_1sem, pct_p3, variacao_pp

## Fluxo

1. Ler xlsx históricos 🟢
2. Calcular cessões (mesma lógica exportador) 🟢
3. Normalizar percentuais 🟢
4. Diff por turma/disciplina 🟢
5. Emitir relatório 🟢

## Dependências

- openpyxl 🟢
- Lógica cessão (compartilhar com exportacao-relatorios) 🟡

## Riscos

- 🟡 Formatos xlsx legados podem divergir — parser defensivo
