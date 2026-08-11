# ADR-009 — Versionamento automático de calendários gerados

**Status:** Aceito  
**Data:** 2026-08-11  
**Confiança:** 🟢 (pedido explícito de Brener)

## Contexto

Cada geração de calendário produz xlsx e relatórios valiosos. Hoje no legado os arquivos ficam em pasta local (`Horario desenvolvido/`) e podem ser sobrescritos ou apagados acidentalmente. Na plataforma, o coordenador precisa **consultar versões anteriores**, **baixar** e **apagar** arquivos de forma explícita — tudo pela interface, sem passos manuais de backup.

O ERD já previa `calendario_gerado`, mas a lacuna “versionamento de propostas (histórico de reruns)” não estava fechada.

## Decisão

1. **Persistência automática e imutável por geração** — cada job concluído com sucesso cria um **novo** registro `calendario_gerado` + blobs (`xlsx`, relatórios). Nunca sobrescrever o blob de uma versão existente.
2. **Histórico transparente** — a UI lista todas as versões do semestre (data, job, status verificação, publicado ou não) sem o coordenador precisar “salvar” manualmente.
3. **Consultar versão antiga** — abrir detalhe (SCR-08) de qualquer versão não apagada; downloads idênticos aos da versão atual.
4. **Restaurar referência** — ação “Usar esta versão” define a versão de **referência ativa** do semestre (para comparação/publicação); não apaga versões mais novas.
5. **Exclusão explícita** — DELETE na UI com confirmação; soft-delete (`deleted_at`) + remoção do blob após confirmação; versão some da lista padrão.
6. **Isolamento tenant** — histórico filtrado por `segmento_id` do JWT.

## Alternativas consideradas

| Opção | Rejeitada porque |
|---|---|
| Sobrescrever único calendário por semestre | Perde histórico; risco de exclusão acidental |
| Backup manual (download obrigatório) | Não transparente; depende do usuário |
| Git por coordenador | Fora do fluxo web; não escala |
| Hard delete imediato sem confirmação | Contradiz pedido de proteção contra acidentes |

## Consequências

- Colunas em `calendario_gerado`: `versao`, `rotulo`, `deleted_at`, `referencia_ativa` (bool, no máximo 1 true por semestre)
- API: `GET /semestres/{id}/calendarios`, `DELETE /calendarios/{id}`, `POST /calendarios/{id}/restaurar-referencia`
- UI: SCR-10 Histórico + integração no dashboard e pós-geração
- Worker T6/T10: INSERT-only na persistência de saídas
- Reconstruction-plan: tarefa dedicada T10b ou extensão T10/T13
