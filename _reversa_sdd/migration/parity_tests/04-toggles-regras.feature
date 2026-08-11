# language: pt
# spec-id: PT-004
# rastreabilidade:
#   process_flows: regras-negocio RuleContext
#   target_architecture: RuleContextBuilder, packages/solver
#   paradigma_alvo: hibrido-procedural-wrap

Funcionalidade: Toggles de regras codificadas
  Como coordenador
  Quero desativar regra no semestre
  Para que solver não aplique restrição

  @paridade @critico
  Cenário: Toggle off remove restrição do RuleContext
    Dado regra "max_3_avaliacoes_semana" ativa no catálogo
    Quando coordenador desativa toggle via PATCH /semestres/{id}/regras/max_3_avaliacoes_semana
    E dispara geração
    Então RuleContext enviado ao solver não inclui max_3_avaliacoes_semana
    E calendário gerado pode diferir do CLI com regra ativa (comportamento esperado)

  @paridade @idempotencia
  Cenário: Toggle idempotente
    Dado toggle desativado
    Quando PATCH desativar novamente
    Então estado permanece inativo sem efeito colateral
