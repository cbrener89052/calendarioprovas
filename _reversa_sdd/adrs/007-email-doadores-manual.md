# ADR-007 — E-mail aos doadores: ação manual pós-fechamento

**Status:** Proposto (requisito usuário)  
**Data:** 2026-08-15  
**Confiança:** 🟢 (intenção) | 🔴 (implementação)

## Contexto

Professores que cedem tempo precisam ser informados. Hoje: relatório de trocas manual. Refrações frequentes antes do calendário estabilizar.

## Decisão

- **Não** enviar e-mail automaticamente a cada fatoração/refração
- Funcionalidade explícita **"Enviar e-mails aos doadores"** após calendário fechado
- Dados = cessões do relatório de trocas (`exportar_relatorio_trocas.py`)
- Persistir auditoria (`enviado_em`, `enviado_por`)

## Consequências

- ✅ Evita spam durante iterações
- ✅ Coordenador controla momento da comunicação
- 🔴 Requer cadastro e-mail professor
- 🔴 Política pós-envio se calendário mudar

## Evidência

- `.reversa/context/user-requirements.md` (seção Notificação por e-mail)
