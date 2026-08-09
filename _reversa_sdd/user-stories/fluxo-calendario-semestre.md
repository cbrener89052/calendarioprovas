# User Story — Fluxo calendário semestre (coordenador)

> Persona: Coordenador escolar (segmento Ensino Médio C)  
> Confiança: 🟢 requisitos declarados + 🟡 detalhes UI

---

## US-01 — Configurar segmento e GRUPOS

**Como** coordenador  
**Quero** definir GRUPOS com datas de semestre, 2ª chamada e conselho  
**Para** que turmas com calendários diferentes tenham períodos corretos sem editar código

**Critérios de aceite:**
- Crio GRUPO "10/12" com conselho 24–28/11/2026
- Associo turmas 10C1, 10C2, 12C1, 12C2 ao grupo
- Outro coordenador não vê meus GRUPOS

**Rastreio:** `plataforma-multi-coordenador/requirements.md` RF-02, RF-03

---

## US-02 — Upload entradas do semestre

**Como** coordenador  
**Quero** enviar grade PDF, modelo xlsx e siglas  
**Para** alimentar o gerador sem pastas locais

**Critérios:**
- Upload grade Untis → job extração (se PDF) ou import direto
- Modelo xlsx e siglas ficam versionados no semestre
- Arquivos isolados no meu segmento

**Rastreio:** RF-05, `extracao-grade/`

---

## US-03 — Configurar regras do semestre

**Como** coordenador  
**Quero** ativar/desativar regras codificadas e registrar preferências IA  
**Para** adaptar o calendário ao meu segmento sem PR no GitHub

**Critérios:**
- Vejo catálogo institucional (~30 regras)
- Desativo toggle "regra 3 relaxável" se política local proibir
- Registro texto "evitar provas Geo às segundas" em customização IA

**Rastreio:** ADR-006, `regras-negocio/`

---

## US-04 — Gerar e validar calendário Proposta 3

**Como** coordenador  
**Quero** disparar geração e receber verificação automática  
**Para** publicar calendário conforme skill institucional

**Critérios:**
- Job completa com xlsx 8 abas + relatório trocas
- Verificador retorna OK ou lista erros por turma
- Não consigo publicar se houver erro crítico

**Rastreio:** `geracao-calendario/`, `verificacao-calendario/`

---

## US-05 — Baixar relatórios

**Como** coordenador  
**Quero** baixar tabela-resumo e tempos cedidos  
**Para** distribuir à equipe docente

**Critérios:**
- Downloads em Excel equivalentes aos scripts `exportar_*.py`
- Percentuais de cessão batem com Proposta 3

**Rastreio:** `exportacao-relatorios/`

---

## US-06 — Sincronizar regras após atualização da skill (dev)

**Como** mantenedor (Brener)  
**Quero** sync skill → catálogo Reversa/BD  
**Para** detectar drift entre skill e código

**Critérios:**
- `sources.json` hashes atualizados
- Lacunas (ex. PR #14) documentadas em addenda

**Rastreio:** `.reversa/context/sync-regras.md`

---

## US-07 — Benchmark histórico (opcional v2)

**Como** coordenador  
**Quero** comparar cessões com semestre anterior  
**Para** validar melhoria da Proposta 3

**Rastreio:** `analise-historica/` — Could
