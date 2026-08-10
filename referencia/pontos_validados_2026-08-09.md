# Pontos de sucesso validados — sessão de 09/08/2026

Registro do que foi **efetivamente implementado, testado e confirmado**
nesta sessão (não é um resumo de intenção — cada item abaixo tem uma
verificação concreta por trás). Datas/PRs conferidos direto no GitHub e
no `git log` no momento da escrita deste arquivo.

## 1. Regra de negócio: LP/LIT/RED ≥ 10 dias antes do conselho de classe

**Pedido do usuário**: a prova combinada LP/LIT/RED (Português + Redação
+ Gramática), por exigir 3 tempos de aplicação, precisa cair com pelo
menos 10 dias corridos de antecedência do início da semana vetada de
conselho de classe.

- **Documentação na skill** — PR [#14](https://github.com/cbrener89052/calendarioprovas/pull/14)
  (merged, commit `fe5a96b`): regra registrada em `SKILL.md`, com
  exemplo numérico (conselho 12/10/2026 → prova não pode passar de
  02/10/2026) e novo item de checklist.
- **Implementação no gerador** — PR [#18](https://github.com/cbrener89052/calendarioprovas/pull/18)
  (merged, commit `5bcd2ae`): novo limite `LIMITE_LPLITRED_CONSELHO`
  (semana 9) em `gerar_calendario.py`, aplicado em `dia_permitido()`;
  checagem equivalente em `verificar_calendario.py`.
- **Validado**: `verificar_calendario.py` roda limpo — nenhuma ocorrência
  de LP/LIT/RED além da semana 9 nas 8 turmas.

## 2. Três bugs pré-existentes descobertos e corrigidos

Nenhum foi pedido explicitamente — surgiram ao endurecer a busca com a
regra acima, que expôs falhas que a versão anterior nunca tinha
disparado.

### 2.1 Falha silenciosa na coordenação de provas entre turmas irmãs

Quando `resolver_par()` não conseguia coordenar todas as provas de
professor comum entre duas turmas irmãs (ex.: 10C1/10C2), o calendário
"fechava" mesmo assim — as provas não coordenadas simplesmente
desapareciam do resultado, sem acionar a escada de afrouxamento e sem
aviso nenhum além de uma linha de log facilmente perdida.

- **Corrigido**: falha de coordenação agora entra no conjunto
  `falharam`, acionando a escada de afrouxamento normalmente.
- **Validado**: reproduzido o bug original (0 de 11 provas comuns
  coordenadas para 10C1/10C2 com a semente antiga, calendário "fechando"
  como se nada tivesse faltado) e confirmado que, após a correção, a
  mesma situação passa a acionar a escada e resolver corretamente.

### 2.2 Teto de cessão afrouxado globalmente em vez de por turma

Quando nenhuma turma fechava nem relaxando as regras 3/4, o único
recurso restante (subir o teto de cessões) valia para as **8 turmas de
uma vez** — uma turma difícil podia estourar o teto de turmas que já
fechavam com as regras integrais.

- **Corrigido**: `folga_extra` — dicionário por turma — substitui o
  `folga` global nessa etapa da escada.
- **Validado**: rodada final mostra teto elevado **só na 10C1**; as
  outras 7 turmas continuam cumprindo as cinco regras de cessão
  integralmente (conferido linha a linha no relatório e no
  `verificar_calendario.py`).

### 2.3 Contagem em dobro no relatório "Regras relaxadas"

Quando um único professor doava 2 tempos do mesmo bloco de prova (comum
em LP/LIT/RED, que tem 3 tempos), a reconstrução usada no relatório
contava essa doação **em dobro** — ex.: Ing/APa aparecia como "10 de 54
aulas cedidas (18,5%)" quando o valor real, batendo com a leitura direta
da planilha, era "6 de 54 (11,1%)".

- **Corrigido**: nova função `posicoes_por_doador()`, usada tanto em
  `detectar_regras_relaxadas()` quanto na tabela de trocas de tempo do
  relatório.
- **Validado**: comparação direta, célula a célula, entre a reconstrução
  em memória e a releitura do `.xlsx` já escrito — os dois métodos batem
  exatamente após a correção (antes divergiam em `ing/APa`, `GL`, etc.).

## 3. Escolha da semente de busca (`SEED_PROPOSTA_3`)

A semente 7 (documentada anteriormente como "fecha as 8 turmas sem
exceção") deixou de fechar a 10C1 sob a nova regra — não por
inviabilidade real (confirmado: sem nenhum limite de cessão a 10C1
fecha instantaneamente), mas por "azar" de busca dentro do orçamento de
nós (`MAX_NOS_CESSAO`).

- **Testado**: aumentar o orçamento de nós em 8× não resolveu com a
  semente 7; troca de semente resolveu em segundos.
- **Semente final**: `3`. Resultado: as 8 turmas fecham; única exceção
  é a **10C1**, com regra 3, regra 4 e teto de cessões (+1) relaxados —
  **só nela**, e devidamente divulgado no relatório.

## 4. Verificação final

`verificar_calendario.py` na Proposta 3 final:

```
OK: as propostas passaram em todos os itens do checklist.
20 AVISO(S) — regras relaxadas por inviabilidade, não são falhas do checklist
```

Zero PROBLEMA. Os 20 avisos são todos esperados e documentados: 15 já
existiam antes desta rodada (preferência por tempos 7-11 em 11C1/11C2/
12C1/12C2) e 5 são a exceção localizada da 10C1 descrita acima.

## 5. Entregáveis regenerados e no PR #18

- `Horario desenvolvido/Proposta_3_Calendario_Provas_2026_2SEM.xlsx`
- `Horario desenvolvido/Relatorio_trocas_de_tempo.md`
- `Horario desenvolvido/Relatorio_Tempos_Cedidos_Proposta_3.xlsx`
- `Horario desenvolvido/Tabela_Provas_por_Turma_Proposta_3.xlsx`
- `referencia/estado_2sem_2026.md` atualizado com o novo resultado

PR #18 mergeado em `main` (commit `5bcd2ae`), 8 arquivos alterados,
+372/-238 linhas.

## 6. Comparação da 12C1 (1º semestre) com dado oficial real

O usuário forneceu o `.xls` com as 20 provas **de fato aplicadas** na
12C1 no 1º semestre (exportação oficial, com data/hora/professor). Comparado
contra a extração que eu tinha feito do `Klausurplan_2026_1SEM.xlsx`:

- **Data e tempo (horário) bateram em 20 de 20 provas** — a extração via
  posição da célula na grade é confiável.
- **Disciplina errou em 8 de 20 provas (40%)** — texto de célula vizinha
  contaminando a leitura (arquivo já documentado como "muito
  irregular"). Química nunca apareceu certa nas duas ocorrências reais.
- **Implicação**: `referencia/analise_1sem_2026.md` (percentuais de
  cessão do 1º semestre) tem números incorretos para a 12C1 em pelo
  menos Química, DaF, Filosofia, Biologia e Geografia-Aprofundamento —
  **ainda não corrigido**, pendente de decisão do usuário (corrigir só a
  12C1 agora, ou esperar os dados reais das outras 7 turmas).
