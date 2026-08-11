# Addendum — PR #14 Must deploy (Brener 2026-08-09)

> Resposta à Pergunta 4 do Revisor (`questions.md`).

## Decisão

- **LP/LIT/RED ≥10 dias antes do conselho** é **Must** antes do deploy da plataforma.
- Endpoint/ação **publicar** calendário deve **bloquear** se gerador ou verificador não implementarem RN-08.
- **Claude Code agendado** para atualizar skill/código (implementação em curso).

## Rastreio

| Artefato | Ação |
|----------|------|
| `geracao-calendario/tasks.md` T-06 | Implementar no solver |
| `verificacao-calendario/tasks.md` T-04 | Check automático |
| `regras-negocio/tasks.md` T-09 | Marcar `implementada_solver=true` após merge |
| `plataforma-multi-coordenador/requirements.md` RF-11 | Gate publish |

## Sync

Após implementação no código, rodar fluxo `.reversa/context/sync-regras.md` para alinhar hashes Reversa.
