# Dependências — calendarioprovas

> Gerado pelo Scout (Reversa) em 2026-08-09

## Gerenciador de pacotes

**Nenhum formalizado.** Não existe `requirements.txt`, `pyproject.toml` nem `Pipfile`.
Instalação documentada no README: `pip install openpyxl`.

## Dependências Python identificadas

| Biblioteca | Uso | Scripts |
|---|---|---|
| **openpyxl** | Leitura/escrita Excel, estilos, merge | `gerar_calendario.py`, `verificar_calendario.py`, `exportar_*.py`, `analisar_*.py`, `comparar_semestres.py` |
| **pymupdf** (PyMuPDF) | Extração de texto/geometria de PDF | `extrair_grade_2025.py`, `extrair_grade_1semestre.py`, `esqueleto_grade_2025.py` |
| **fpdf2** | Geração de PDF | `exportar_regras_pdf.py` |

## Biblioteca padrão (stdlib)

Usada extensivamente: `os`, `shutil`, `collections`, `copy`, `random`, `re`,
`datetime`, `unicodedata`, `csv`, `glob`, `subprocess`, `sys`, `pprint`.

## Dependências internas (entre scripts)

```
gerar_calendario.py  ←── verificar_calendario.py
                     ←── exportar_tabelas_turma.py
                     ←── exportar_tempos_cedidos.py

exportar_tabelas_turma.py ←── exportar_tempos_cedidos.py

analisar_2sem_2025.py ←── contar_2sem_2025.py
grade_2sem_2025_limpa.py ←── contar_2sem_2025.py
```

## Versões

Versões **não pinadas** no repositório. Recomendação para specs:

```
openpyxl>=3.1.0
pymupdf>=1.24.0
fpdf2>=2.7.0
```

## Dependências futuras (evolução planejada)

Conforme `.reversa/context/user-requirements.md`:

| Camada | Tecnologia prevista |
|---|---|
| API | FastAPI |
| Banco | PostgreSQL |
| Auth | Login individual (5 coordenadores) |
| Storage | S3 (nuvem) / filesystem (on-prem Docker) |
| Deploy | Docker Compose (híbrido nuvem + local) |
