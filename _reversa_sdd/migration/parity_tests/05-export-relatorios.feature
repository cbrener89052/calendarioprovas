# language: pt
# spec-id: PT-005
# rastreabilidade:
#   process_flows: exportacao-relatorios
#   target_architecture: apps/worker exportadores
#   paradigma_alvo: hibrido-procedural-wrap

Funcionalidade: Exportação de relatórios — paridade
  Como coordenador
  Quero baixar relatórios da plataforma
  Para obter mesmos artefatos do CLI

  @paridade @critico
  Cenário: Downloads disponíveis pós-job
    Dado calendário gerado e verificado
    Quando GET /calendarios/{id}/download
    E GET /relatorios/trocas
    E GET /relatorios/cessoes
    E GET /relatorios/tabela
    Então arquivos correspondem aos gerados pelo CLI legado

  @paridade
  Cenário: Tabela-resumo por turma
    Dado calendário publicado
    Quando baixo relatório tabela
    Então contém disciplina, professor, dia, tempos, n_tempos por turma
