# Verificação de Calendário — Design Técnico

## Interface

| Símbolo | Assinatura | Retorno | Observação |
|---------|-----------|---------|------------|
| `main` | `()` | `void` | Itera abas xlsx, acumula problemas |
| `data_da` | `(ws, w, d)` | `date` | Converte semana/dia → data calendário |

### Entidade

| Campo | Tipo | Descrição |
|-------|------|-----------|
| ProblemaValidacao.turma | string | Aba/turma |
| ProblemaValidacao.regra | string | ID ou nome da regra |
| ProblemaValidacao.mensagem | string | Detalhe humano-legível |
| ProblemaValidacao.severidade | string | `erro` \| `aviso` |

### API futura 🟡

| Método | Caminho | Saída |
|--------|---------|-------|
| POST | `/api/v1/calendarios/{id}/verificar` | `{ ok, problemas[] }` |

## Fluxo Principal

1. Abrir xlsx calendário gerado 🟢
2. Para cada aba (turma): extrair provas, simulados, cessões implícitas 🟢
3. Executar bateria de checks (semanais, diários, distância, cessão, simulados…) 🟢
4. Cruzar com grade-base importada de `gerar_calendario` 🟢
5. Imprimir/agregar `ProblemaValidacao` 🟢
6. Exit code ≠ 0 se erro crítico 🟢

## Fluxos Alternativos

- **Arquivo inexistente/malformado:** Erro imediato 🟢
- **Avisos vs erros:** Regras relaxadas conforme relatório gerador → aviso 🟢

## Dependências

- openpyxl 🟢
- `gerar_calendario` (constantes, grades) — **acoplamento a remover** 🟢
- Grade-base 🟢

## Decisões de Design

| Decisão | Evidência | Confiança |
|---------|-----------|-----------|
| Leitura xlsx, não memória | docstring | 🟢 |
| Espelho da skill | comentários main | 🟢 |
| Sem validação ARGB | lacuna domain.md | 🔴 |

## Riscos e Lacunas

- 🔴 PR #14 check ausente
- 🟡 Refactor: `RuleCatalog` compartilhado gerador+verificador
- 🔴 IA customizations: escopo do verificador indefinido
