#!/usr/bin/env python3
"""
Extrai questões de um capítulo do livro "Matemática para Vestibular" a
partir do PDF (mesmo padrão em todos os capítulos: teoria, exercícios em
blocos Nível-A/B/C, seção "Respostas" com os mesmos blocos de nível
contendo o gabarito, casado pela numeração).

Por que PDF e não .docx
-----------------------
No .docx, o Word grava símbolos matemáticos como caractere especial de
fonte (<w:sym>) e fórmulas maiores como objeto OLE do Equation Editor/
MathType (uma imagem .wmf, sem texto algum no XML). O PDF gerado pelo
Acrobat PDFMaker resolve os dois problemas de uma vez: os símbolos saem
com o Unicode correto e as fórmulas do Equation Editor saem como texto
de verdade (confirmado comparando os dois formatos do mesmo capítulo).
Por isso este script lê o PDF com `pdftotext`, não o .docx — é mais
simples e não depende de IA para reconstruir fórmula nenhuma.

Figuras/diagramas genuínos (aqueles que são mesmo uma imagem no livro,
ex: diagrama de Venn, tabuleiro, cartões) continuam sendo apenas imagem
mesmo no PDF. Esses casos são detectados por palavra-chave ("figura",
"diagrama", "esquema" etc.) e marcados em vez de processados por IA —
a ideia é só chamar atenção humana (ou IA, se você pedir depois) para
essas poucas questões, sem gastar IA nas outras que o script já resolve
sozinho.

USO
---
    python extrair_capitulo_pdf.py capitulo.pdf \\
        --livro "Matemática para Vestibular Vol 01" \\
        --capitulo "Lógica e Conjuntos" \\
        --output banco_matvest.db
"""

import argparse
import re
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

NIVEL_RE = re.compile(r"^n[íi]vel[\s\-]*([A-Za-z0-9]+)$", re.IGNORECASE)
RESPOSTAS_RE = re.compile(r"^respostas?$", re.IGNORECASE)
QUESTAO_RE = re.compile(r"^(\d+)[.)]\s*(.*)$")
ALTERNATIVA_RE = re.compile(r"\([A-E]\)")
LETRA_UNICA_RE = re.compile(r"^[A-E]$")
PALAVRAS_FIGURA = re.compile(
    r"\b(figura|diagrama|esquema|gr[áa]fico|ilustra|hachurad|cart[ãa]o|cart[õo]es|tabuleiro)\b",
    re.IGNORECASE,
)


@dataclass
class Questao:
    nivel: str
    numero: int
    tipo: str = ""
    enunciado: str = ""
    pagina: int = 0
    tem_figura: bool = False
    gabarito: str = ""
    pagina_gabarito: int = 0


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------
# Leitura do PDF, página por página (pra saber de qual página cada
# questão veio, útil pra exportar a página como imagem depois)
# --------------------------------------------------------------------------

def num_paginas(caminho_pdf: str) -> int:
    saida = subprocess.run(
        ["pdfinfo", caminho_pdf], capture_output=True, text=True, check=True
    ).stdout
    m = re.search(r"^Pages:\s+(\d+)", saida, re.MULTILINE)
    if not m:
        raise RuntimeError("Não consegui ler o número de páginas (pdfinfo).")
    return int(m.group(1))


def extrair_linhas_com_pagina(caminho_pdf: str) -> list:
    """Retorna lista de (texto_da_linha, numero_da_pagina), já sem linhas
    vazias e sem o caractere de quebra de página (\\f) do pdftotext."""
    total = num_paginas(caminho_pdf)
    linhas = []
    for pagina in range(1, total + 1):
        saida = subprocess.run(
            ["pdftotext", "-layout", "-f", str(pagina), "-l", str(pagina), caminho_pdf, "-"],
            capture_output=True, text=True, check=True,
        ).stdout
        for linha in saida.replace("\f", "\n").splitlines():
            texto = re.sub(r"[ \t]{2,}", " ", linha).strip()
            if texto:
                linhas.append((texto, pagina))
    return linhas


# --------------------------------------------------------------------------
# Segmentação em níveis / questões (mesma lógica da versão .docx)
# --------------------------------------------------------------------------

def segmentar_por_nivel(linhas: list) -> dict:
    blocos = {}
    nivel_atual = None
    for texto, pagina in linhas:
        m = NIVEL_RE.match(texto)
        if m:
            nivel_atual = m.group(1).upper()
            blocos[nivel_atual] = []
            continue
        if nivel_atual is not None:
            blocos[nivel_atual].append((texto, pagina))
    return blocos


def extrair_questoes_do_bloco(linhas: list) -> dict:
    questoes = {}
    numero_atual = None
    for texto, pagina in linhas:
        m = QUESTAO_RE.match(texto)
        if m:
            numero_atual = int(m.group(1))
            questoes[numero_atual] = {"partes": [(m.group(2), pagina)], "pagina": pagina}
        elif numero_atual is not None:
            questoes[numero_atual]["partes"].append((texto, pagina))
    resultado = {}
    for numero, info in questoes.items():
        texto_completo = "\n".join(t for t, _ in info["partes"] if t)
        resultado[numero] = (texto_completo, info["pagina"])
    return resultado


def classificar_tipo(enunciado: str, gabarito: str) -> str:
    gabarito_limpo = gabarito.strip().rstrip(".")
    if LETRA_UNICA_RE.match(gabarito_limpo):
        return "Múltipla escolha"
    if ALTERNATIVA_RE.search(enunciado):
        return "Múltipla escolha"
    if re.search(r"verdadeir[oa]\s*\(V\)|falso\s*\(F\)", enunciado, re.IGNORECASE):
        return "Verdadeiro/Falso"
    return "Analítica"


# --------------------------------------------------------------------------
# Banco de dados
# --------------------------------------------------------------------------

def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro TEXT,
            capitulo TEXT,
            nivel TEXT,
            numero INTEGER,
            tipo TEXT,
            enunciado TEXT,
            pagina INTEGER,
            tem_figura INTEGER,
            imagem_pagina TEXT,
            gabarito TEXT,
            pagina_gabarito INTEGER,
            arquivo_origem TEXT,
            capturado_em TEXT,
            UNIQUE(livro, capitulo, nivel, numero)
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_capitulo_nivel ON questoes(capitulo, nivel)")
    conn.commit()
    return conn


def salvar_questao(conn: sqlite3.Connection, livro: str, capitulo: str,
                    arquivo_origem: str, q: Questao, imagem_pagina: str) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO questoes (
            livro, capitulo, nivel, numero, tipo, enunciado, pagina,
            tem_figura, imagem_pagina, gabarito, pagina_gabarito,
            arquivo_origem, capturado_em
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            livro, capitulo, q.nivel, q.numero, q.tipo, q.enunciado, q.pagina,
            int(q.tem_figura), imagem_pagina, q.gabarito, q.pagina_gabarito,
            arquivo_origem, datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()


# --------------------------------------------------------------------------
# Exportação de página como imagem (só pras questões com figura/diagrama)
# --------------------------------------------------------------------------

def exportar_pagina_como_imagem(caminho_pdf: str, pagina: int, pasta_saida: Path) -> str:
    pasta_saida.mkdir(parents=True, exist_ok=True)
    prefixo = pasta_saida / f"pagina_{pagina:03d}"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", "-f", str(pagina), "-l", str(pagina),
         caminho_pdf, str(prefixo)],
        check=True, capture_output=True,
    )
    candidatos = list(pasta_saida.glob(f"pagina_{pagina:03d}*.png"))
    return str(candidatos[0]) if candidatos else ""


# --------------------------------------------------------------------------
# Pipeline principal
# --------------------------------------------------------------------------

def processar_arquivo(caminho_pdf: str) -> list:
    linhas = extrair_linhas_com_pagina(caminho_pdf)

    idx_respostas = next(
        (i for i, (t, _) in enumerate(linhas) if RESPOSTAS_RE.match(t)), None
    )
    if idx_respostas is None:
        raise ValueError("Não encontrei o cabeçalho 'Respostas' no documento.")

    linhas_exercicios = linhas[:idx_respostas]
    linhas_gabaritos = linhas[idx_respostas + 1:]

    blocos_exercicios = segmentar_por_nivel(linhas_exercicios)
    blocos_gabaritos = segmentar_por_nivel(linhas_gabaritos)

    if not blocos_exercicios:
        raise ValueError("Não encontrei nenhum cabeçalho 'Nível-X' nos exercícios.")

    questoes = []
    for nivel, linhas_nivel in blocos_exercicios.items():
        exercicios = extrair_questoes_do_bloco(linhas_nivel)
        gabaritos = extrair_questoes_do_bloco(blocos_gabaritos.get(nivel, []))
        numeros = sorted(set(exercicios) | set(gabaritos))
        for numero in numeros:
            enunciado, pagina = exercicios.get(numero, ("", 0))
            gabarito, pagina_gab = gabaritos.get(numero, ("", 0))
            if not enunciado:
                log(f"AVISO: Nível-{nivel} questão {numero} sem enunciado (só gabarito). Pulando.")
                continue
            if not gabarito:
                log(f"AVISO: Nível-{nivel} questão {numero} sem gabarito correspondente.")
            tipo = classificar_tipo(enunciado, gabarito)
            tem_figura = bool(PALAVRAS_FIGURA.search(enunciado))
            questoes.append(Questao(
                nivel=nivel, numero=numero, tipo=tipo, enunciado=enunciado,
                pagina=pagina, tem_figura=tem_figura, gabarito=gabarito,
                pagina_gabarito=pagina_gab,
            ))
    return questoes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", help="Arquivo .pdf do capítulo")
    parser.add_argument("--livro", required=True, help="Nome do livro (ex: 'Matemática para Vestibular Vol 01')")
    parser.add_argument("--capitulo", required=True, help="Nome do capítulo/assunto (ex: 'Lógica e Conjuntos')")
    parser.add_argument("--output", default="banco_matvest.db", help="Caminho do SQLite de saída")
    parser.add_argument("--exportar-figuras", action="store_true",
                         help="Renderiza em PNG a página de cada questão marcada com figura/diagrama")
    parser.add_argument("--pasta-figuras", default="figuras", help="Pasta onde salvar as páginas exportadas")
    args = parser.parse_args()

    if shutil.which("pdftotext") is None or shutil.which("pdfinfo") is None:
        raise SystemExit("ERRO: 'pdftotext'/'pdfinfo' não encontrados. Instale poppler-utils.")

    log(f"Processando {args.pdf} ...")
    questoes = processar_arquivo(args.pdf)

    conn = init_db(args.output)
    arquivo_origem = Path(args.pdf).name
    pasta_figuras = Path(args.pasta_figuras)

    for q in questoes:
        imagem_pagina = ""
        if q.tem_figura and args.exportar_figuras:
            imagem_pagina = exportar_pagina_como_imagem(args.pdf, q.pagina, pasta_figuras)
        salvar_questao(conn, args.livro, args.capitulo, arquivo_origem, q, imagem_pagina)
    conn.close()

    total = len(questoes)
    com_figura = sum(1 for q in questoes if q.tem_figura)
    sem_gabarito = sum(1 for q in questoes if not q.gabarito)

    log(f"Concluído. {total} questões salvas em {args.output}.")
    log(f"  - {com_figura} marcadas com possível figura/diagrama (revisão manual)")
    log(f"  - {sem_gabarito} sem gabarito correspondente encontrado")
    if com_figura and not args.exportar_figuras:
        log("  (rode de novo com --exportar-figuras pra salvar a página dessas questões como imagem)")


if __name__ == "__main__":
    main()
