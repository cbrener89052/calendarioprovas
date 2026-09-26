# Exportação de Relatórios — Design Técnico

## Interface

| Símbolo | Assinatura | Retorno |
|---------|-----------|---------|
| `carregar_siglas` | `()` | `dict[str,str]` |
| `exportar` (tabelas) | `(proposta, siglas)` | `str` path |
| `cedencias_por_turma` | `(caminho, turma)` | `Counter` |

## Entidades

- **LinhaTabelaProvas:** disciplina, professores, quando, n_tempos
- **LinhaCessao:** disciplina, aulas_semanais, aulas_programadas, aulas_cedidas, percentual

## Fluxo Principal

1. Carregar siglas (`siglas_professores.xlsx` ou equivalente) 🟢
2. Ler calendário xlsx por turma 🟢
3. **Tabelas:** extrair linhas de prova formatadas 🟢
4. **Cessões:** cruzar células de prova com grade-base; contar desvios 🟢
5. Calcular percentuais 🟢
6. Gravar xlsx de saída 🟢

## Dependências

- openpyxl, gerar_calendario (grades), calendário xlsx 🟢

## API futura 🟡

| Método | Caminho |
|--------|---------|
| GET | `/api/v1/calendarios/{id}/relatorios/tabela-resumo` |
| GET | `/api/v1/calendarios/{id}/relatorios/tempos-cedidos` |

## Riscos

- 🟡 Duplicação lógica parse xlsx vs verificador — extrair lib comum
