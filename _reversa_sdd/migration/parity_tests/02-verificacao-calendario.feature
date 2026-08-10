# language: pt
# spec-id: PT-002
# rastreabilidade:
#   process_flows: verificacao-calendario
#   target_architecture: apps/worker VerificadorPipeline
#   paradigma_alvo: hibrido-procedural-wrap

Funcionalidade: Verificação de calendário — paridade checks
  Como worker
  Quero verificar calendário gerado
  Para bloquear publish se equivalente ao verificador CLI falhar

  @paridade @critico
  Cenário: Verificador OK em calendário válido
    Dado calendário xlsx gerado com sucesso
    Quando worker executa verificador plataforma
    Então todos checks 1 a 5 passam
    E check 5a-bis LP/LIT/RED ≥10 dias passa quando aplicável

  @paridade @critico
  Cenário: Erro crítico bloqueia publish
    Dado calendário com violação max 3 avaliações/semana
    Quando verificador plataforma executa
    Então status é failed
    E botão Publicar permanece disabled na UI

  @paridade
  Cenário: Customização IA no relatório auxiliar
    Dado customização IA "preferir provas Geo às sextas" registrada
    Quando verificação completa com camada IA
    Então relatório auxiliar menciona a preferência
    E solver determinístico não foi alterado
