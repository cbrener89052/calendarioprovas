# Especificação — Máscara padrão de entrada de provas

> Template institucional para download/upload na plataforma  
> Requisito usuário 2026-08-16 | ADR-010 (atualizado)  
> Confiança: 🟢 requisito | 🟡 colunas finais sujeitas a validação com coordenação

## Propósito

Arquivo xlsx **simples** (não é o Klausurplan semanal) que o coordenador:

1. **Baixa** na plataforma — *"Baixe sua planilha padrão aqui"*
2. **Preenche** offline com os dados pedidos
3. **Envia** de volta → sistema popula `ExamCatalog`

Distinto da **máscara de layout** Klausurplan (malha semanal de calendário).

## Nome do arquivo (provisório)

`Mascara_Entrada_Provas_<semestre>.xlsx`

## Aba: `catalogo` (única aba na v1)

| Coluna | Cabeçalho PT | Tipo | Obrigatório | Descrição |
|--------|--------------|------|-------------|-----------|
| A | `turma` | texto | sim | Grupo/turma ex.: `10C1` |
| B | `disciplina` | texto | sim | Nome ou código (Mat, Fil, LP/LIT/RED) |
| C | `n_provas_semestre` | inteiro 1–2 | sim | Quantidade de **provas** da disciplina no semestre |
| D | `n_aulas_semanais` | inteiro 0–11 | sim | **Tempos de aula por semana** na grade (carga semanal) |
| E | `n_tempos_aplicacao` | inteiro 1–3 | não | Duração de **cada** prova em tempos; default pela skill |
| F | `periodo` | 1 \| 2 \| vazio | não | 1ª/2ª prova ou única (Fil/Soc, Fis/Qui 9º) |
| G | `observacao` | texto | não | Notas livres (ignorado pelo solver) |

### Linhas de exemplo (pré-preenchidas no template, apagar antes de enviar)

```
10C1 | Mat | 2 | 4 | 2 | |
10C1 | LP/LIT/RED | 2 | 3 | 3 | |
10C1 | Fil | 1 | 1 | 1 | |
```

## Validação no upload

| Regra | Severidade |
|-------|------------|
| Turma existe na grade carregada | PROBLEMA se ausente |
| Disciplina existe na turma (grade) | AVISO se divergir |
| `n_provas_semestre` coerente com skill (ex.: Fil=1) | PROBLEMA |
| `n_aulas_semanais` coerente com `aulas_semanais(turma)` | AVISO |
| LP/LIT/RED com `n_tempos_aplicacao`=3 (10–12) | PROBLEMA |

## Mapeamento → `ExamCatalog`

Cada combinação `(turma, disciplina, periodo)` gera uma linha de exame:

- `n_tempos` ← coluna E ou inferido (LP/LIT/RED → 3)
- `periodo` ← coluna F ou inferido por `n_provas_semestre`
- `n_aulas_semanais` ← coluna D (metadado cessão C1)

## UI plataforma

- Botão **"Baixar planilha padrão"** → gera xlsx vazio com cabeçalhos + 1 linha exemplo
- Botão **"Enviar planilha preenchida"** → parser → preview → confirmar
- Alternativa: mesmo grid na tela (`ExamCatalogEditor`) — paridade de colunas

## Referência legado (layout calendário — outro arquivo)

| Arquivo GitHub | Papel |
|----------------|-------|
| `Klausurplan_2026_2SEM.xlsx` | **Layout** malha semanal 2º sem 2026 |
| `Horario modelo/Klausurplan_2026_1SEM.xlsx` | Layout 1º sem |
| `provas2sem_2025/Klausurplan_ramoC_2025_2SEM.xlsx` | Layout referência 2025 |
| `Horario desenvolvido/Proposta_3_*.xlsx` | Saída gerada (usa layout) |
