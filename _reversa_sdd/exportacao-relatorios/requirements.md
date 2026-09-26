# Requirements: Exportação de Relatórios

> Identificador: `003-exportacao-relatorios`  
> Data: `2026-08-09`

## 1. Resumo executivo

Deriva relatórios Excel a partir do calendário gerado: tabela-resumo por turma (disciplina, professor, dia, tempos) e relatório de tempos cedidos por disciplina/professor com percentual sobre aulas programadas no semestre.

## 2. Contexto a partir do legado

| Fonte | Trecho | Confiança |
|-------|--------|-----------|
| `_reversa_sdd/domain.md#entregáveis` | Tabela-resumo + tempos cedidos obrigatórios | 🟢 |
| `_reversa_sdd/code-analysis.md#exportacao-relatorios` | Dois scripts exportadores | 🟢 |
| `exportar_tabelas_turma.py`, `exportar_tempos_cedidos.py` | Implementação | 🟢 |

## 3. Personas

| Persona | Objetivo | Cenário |
|---------|----------|---------|
| Coordenador | Entregar resumo à direção/professores | Exporta após gerar+verificar |
| Plataforma | Download de artefatos | API lista blobs por calendário |

## 4. Regras de negócio

1. **RN-01:** Cessão = tempo de prova que na grade-base pertence a outra disciplina 🟢
2. **RN-02:** Percentual cedido = aulas_cedidas / aulas_programadas no semestre 🟢
3. **RN-03:** Siglas de professores vêm de planilha externa 🟢
4. **RN-04:** Proposta 3 obrigatória para relatório de cessões 🟢

## 5. Requisitos Funcionais

| ID | Requisito | Prioridade | Critério | Conf. |
|----|-----------|------------|----------|-------|
| RF-01 | Tabela-resumo por turma (disciplina, prof, quando, n_tempos) | Must | 8 arquivos ou abas | 🟢 |
| RF-02 | Relatório tempos cedidos por turma | Must | Colunas: disc, aulas/sem, prog, cedidas, % | 🟢 |
| RF-03 | Carregar siglas professores | Must | Mapa disc→sigla | 🟢 |
| RF-04 | API download relatórios (futuro) | Should | URLs assinadas blob | 🟡 |

## 6. Requisitos Não Funcionais

| Tipo | Requisito | Evidência | Conf. |
|------|-----------|-----------|-------|
| Dependência | Requer xlsx calendário + grade | exportadores | 🟢 |

## 7. Critérios de Aceitação

```gherkin
Cenário: Tabela-resumo completa
  Dado calendário xlsx válido e siglas carregadas
  Quando exportar_tabelas_turma.py executa
  Então gera planilha com uma linha por prova por turma

Cenário: Percentual cessão
  Dado turma com 2 cessões de História em 36 aulas programadas
  Quando exportar_tempos_cedidos.py executa
  Então percentual ≈ 5,6% para História
```

## 8. MoSCoW

RF-01–RF-03 Must; RF-04 Should.

## 9–10. Esclarecimentos / Lacunas

- 🟡 Formato único consolidado vs múltiplos xlsx na plataforma

## 11. Histórico

| Data | Alteração | Autor |
|------|-----------|-------|
| 2026-08-09 | Versão inicial | reversa-writer |
