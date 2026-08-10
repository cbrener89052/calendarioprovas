# language: pt
# spec-id: PT-001
# rastreabilidade:
#   process_flows: geracao-calendario/flowcharts
#   target_architecture: packages/solver, apps/worker
#   paradigma_alvo: hibrido-procedural-wrap

Funcionalidade: Geração Proposta 3 — paridade CLI vs plataforma
  Como coordenador
  Quero gerar calendário na plataforma
  Para obter o mesmo resultado do CLI legado

  @paridade @critico
  Cenário: Mesmas entradas produzem xlsx equivalente
    Dado entradas idênticas carregadas no CLI e na plataforma para semestre "2026-2"
    E GRUPO "10/12" com datas equivalentes ao legado hardcoded
    E RuleContext com todas regras codificadas ativas
    Quando executo gerar_calendario.py no CLI
    E disparo POST /semestres/{id}/gerar na plataforma
    Então ambos jobs completam com sucesso
    E o xlsx da plataforma é equivalente ao xlsx do CLI dentro das normalizationRules
    E ambos têm 8 abas (turmas C)

  @paridade @critico
  Cenário: SEED determinística
    Dado SEED_PROPOSTA_3 = 3
    Quando gero duas vezes na plataforma com mesmas entradas
    Então os xlsx resultantes são idênticos

  @paridade
  Cenário: Relatório regras relaxadas
    Dado solução exige relaxar regra 4 para turma 11C1
    Quando geração completa na plataforma
    Então relatório de trocas contém seção "Regras relaxadas"
