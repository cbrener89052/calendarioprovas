# Análise das aulas cedidas no 2º semestre de 2025

Contagem do que ocorreu no 2º semestre de **2025**, para comparar com o 2º
semestre de 2026 planejado (Propostas 1 a 3). É a comparação mais justa
das três, porque confronta o mesmo semestre do calendário escolar — o 1º
semestre tem mais semanas letivas e por isso dilui os percentuais.

## Arquivos de entrada

- `provas2sem_2025/` — calendário de provas de 2025.
- `horarios2025/` — grade de aulas das turmas em 2025.

**Pendente**: as duas pastas ainda não foram enviadas ao repositório.

## Período letivo (confirmado pela escola)

Início igual para todas as turmas; o fim varia porque as turmas 10 e 12
viajam antes:

| Turmas | Início | Fim |
|---|---|---|
| 9C1, 9C2, 11C1, 11C2 | 28/07/2025 | 28/11/2025 |
| 10C1, 10C2, 12C1, 12C2 | 28/07/2025 | 07/11/2025 |

## Horários dos tempos

**Iguais aos de 2026** (confirmado): 1º = 7h15, 2º = 8h05, 3º = 8h55,
intervalo, 4º = 10h00, 5º = 10h50, 6º = 11h55, 7º = 12h45, 8º = 13h30,
9º = 14h15, 10º = 15h10, 11º = 15h55.

## Como inferir os tempos das provas (confirmado pela escola)

O calendário de 2025 registra **o dia da prova, mas não os tempos**. Sem
isso não dá para cruzar com a grade diretamente, como foi feito em 2026.
As regras abaixo foram confirmadas para reconstruir a informação:

1. **Duração da prova**: o padrão da disciplina — 2 tempos para a maioria,
   3 para a prova combinada de Português/Redação/Gramática, 1 para
   Filosofia e Sociologia.
2. **Tempos próprios**: as aulas que aquela disciplina tem com aquela
   turma no dia da prova contam como tempo próprio. Se tem 1 aula no dia,
   1 tempo é próprio; se tem 2, os 2 são próprios.
3. **Tempo emprestado**: o que faltar para completar a duração vem do
   tempo **vizinho** (imediatamente antes ou depois do tempo próprio),
   preferindo o que **não** seja de disciplina com aula única na semana —
   mesma regra do gerador de 2026, já que essa disciplina perderia a aula
   inteira do período.
4. **Provas simultâneas entre turmas irmãs**: provas no mesmo dia nas duas
   turmas de uma série são a mesma prova, aplicada ao mesmo tempo.

**Atenção ao ler o resultado**: diferente de 2026 e do 1º semestre, aqui a
atribuição do doador é uma **reconstrução**, não um dado do arquivo. O
número total de tempos cedidos é confiável (depende só da duração da prova
e das aulas do dia); já *de quem* veio cada tempo emprestado é a melhor
estimativa possível pela regra 3. Isso precisa ficar sinalizado no
relatório.

## Comparação entre semestres

Use sempre o **percentual**, nunca a contagem absoluta: os semestres têm
números diferentes de semanas letivas, e o mesmo número de provas
espalhado por menos aulas empurra o percentual para cima sozinho.
