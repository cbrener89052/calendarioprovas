# Adendo — notificação por e-mail aos professores doadores

**Requisito declarado:** 2026-08-15 (Brener)  
**Cenário:** evolução plataforma (greenfield sobre legado)  
**Vigente desde:** 2026-08-15.

## Resumo

Funcionalidade para o coordenador **enviar e-mails**, quando estiver seguro,
aos professores que **cedem** tempo de aula para provas de outras
disciplinas. **Não** dispara a cada fatoração/refração.

## Conteúdo mínimo do e-mail

Informar ao doador: disciplina solicitante, professor solicitante, tempo(s)
cedido(s), data/dia da prova, turma (quando aplicável).

## Legado 🟢

Dados equivalentes já existem em `exportar_relatorio_trocas.py` /
`Relatorio_trocas_de_tempo.*` — tupla `(doador)` nas alocações.

## Pendências 🔴

E-mail na planilha de siglas; idioma; agrupamento; política de reenvio.

## Fontes

- `.reversa/context/user-requirements.md` (seção Notificação por e-mail)
- `exportar_relatorio_trocas.py`
