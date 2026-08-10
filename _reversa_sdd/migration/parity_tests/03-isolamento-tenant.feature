# language: pt
# spec-id: PT-003
# rastreabilidade:
#   process_flows: plataforma-multi-coordenador
#   target_architecture: apps/api tenant isolation
#   paradigma_alvo: camadas-di

Funcionalidade: Isolamento tenant por segmento
  Como coordenador A
  Quero acessar apenas meu segmento
  Para garantir privacidade entre coordenadores

  @paridade @critico
  Cenário: Coordenador não vê dados de outro segmento
    Dado coordenador A autenticado com segmento_id SA
    E coordenador B com segmento_id SB
    E semestre criado em SB
    Quando A lista GET /semestres
    Então resposta não contém semestre de B

  @paridade @critico
  Cenário: Admin Brener vê catálogo global
    Dado usuário Brener com papel admin_instituicao
    Quando GET /admin/regras
    Então lista catálogo completo REGRA_CATALOGO

  @paridade
  Cenário: Coordenador não acessa admin
    Dado coordenador autenticado sem papel admin
    Quando GET /admin/regras
    Então resposta é 403 Forbidden
