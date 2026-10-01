#!/usr/bin/env python3
"""
Extrai questões de um capítulo do livro "Matemática para Vestibular" (.docx)
para o banco de dados local BANCO MATVEST (SQLite).

Cada capítulo é organizado assim: teor teórico, depois blocos de exercícios
"Nível-A" / "Nível-B" / "Nível-C", depois uma seção "Respostas" com os
mesmos blocos de nível contendo o gabarito de cada questão (pela mesma
numeração usada nos exercícios).

LIMITAÇÃO IMPORTANTE
---------------------
O Word grava símbolos matemáticos/gregos de duas formas diferentes:

1. Como <w:sym font="Symbol" char="..."/> dentro de um run — isso este
   script resolve corretamente via symbol_font_map.py (∩, ∪, ∈, ≤, ≥, →
   etc. saem certos).
2. Como objeto OLE incorporado (equação do Equation Editor/MathType
   antigo, comum para frações, expoentes, matrizes, expressões maiores)
   — isso é salvo como uma imagem vetorial (.wmf) sem nenhuma
   representação em texto no XML. Este script NÃO consegue reconstruir
   essas fórmulas (não há renderizador de WMF funcional neste ambiente).
   Cada ocorrência é marcada no texto como "[FÓRMULA_FALTANTE]" e contada
   em formulas_faltantes_enunciado/gabarito, para você saber exatamente
   quais questões precisam de revisão manual.

USO
---
    python extrair_capitulo.py capitulo.docx \\
        --livro "Matemática para Vestibular Vol 01" \\
        --capitulo "Lógica e Conjuntos" \\
        --output banco_matvest.db
"""

import argparse
import re
import sqlite3
import zipfile
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from lxml import etree

from symbol_font_map import SYMBOL_FONT_MAP

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}

NIVEL_RE = re.compile(r"^n[íi]vel[\s\-]*([A-Za-z0-9]+)$", re.IGNORECASE)
RESPOSTAS_RE = re.compile(r"^respostas?$", re.IGNORECASE)
QUESTAO_RE = re.compile(r"^(\d+)[.)]\s*(.*)$")
ALTERNATIVA_RE = re.compile(r"\([A-E]\)")
LETRA_UNICA_RE = re.compile(r"^[A-E]$")


@dataclass
class Questao:
    nivel: str
    numero: int
    tipo: str = ""
    enunciado: str = ""
    formulas_faltantes_enunciado: int = 0
    gabarito: str = ""
    formulas_faltantes_gabarito: int = 0


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------
# Leitura do XML do docx com resolução de símbolos e marcação de fórmulas
# --------------------------------------------------------------------------

def carregar_paragrafos(caminho_docx: str) -> list:
    """Usa .iter() (não .findall direto) para também capturar parágrafos
    dentro de tabelas (w:tbl > w:tr > w:tc > w:p), que de outro modo seriam
    silenciosamente ignorados (ex: tabelas-verdade, grades de resposta)."""
    with zipfile.ZipFile(caminho_docx) as z:
        xml_bytes = z.read("word/document.xml")
    root = etree.fromstring(xml_bytes)
    body = root.find("w:body", NS)
    return list(body.iter("{%s}p" % NS["w"]))


def texto_e_fórmulas_faltantes(p_elem) -> tuple:
    partes = []
    faltantes = 0
    for node in p_elem.iter():
        qname = etree.QName(node.tag)
        tag, ns = qname.localname, qname.namespace
        if tag == "t" and ns == NS["w"]:
            partes.append(node.text or "")
        elif tag == "sym" and ns == NS["w"]:
            code = node.get("{%s}char" % NS["w"])
            if code:
                c = int(code, 16) & 0xFF
                partes.append(SYMBOL_FONT_MAP.get(c, f"[SYM:{code}]"))
        elif tag == "tab" and ns == NS["w"]:
            partes.append("\t")
        elif tag in ("br", "cr") and ns == NS["w"]:
            partes.append("\n")
        elif tag == "t" and ns == NS["m"]:
            partes.append(node.text or "")
        elif tag == "object" and ns == NS["w"]:
            partes.append(" [FÓRMULA_FALTANTE] ")
            faltantes += 1
    texto = "".join(partes)
    texto = re.sub(r"[ \t]{2,}", " ", texto).strip()
    return texto, faltantes


# --------------------------------------------------------------------------
# Segmentação em níveis / questões
# --------------------------------------------------------------------------

def segmentar_por_nivel(linhas: list) -> dict:
    """linhas: lista de (texto, qtd_formulas_faltantes). Retorna
    {nivel: [(texto, qtd), ...]} cortando nos cabeçalhos 'Nível-X'."""
    blocos = {}
    nivel_atual = None
    for texto, qtd in linhas:
        m = NIVEL_RE.match(texto)
        if m:
            nivel_atual = m.group(1).upper()
            blocos[nivel_atual] = []
            continue
        if nivel_atual is not None:
            blocos[nivel_atual].append((texto, qtd))
    return blocos


def extrair_questoes_do_bloco(linhas: list) -> dict:
    """Agrupa as linhas de um bloco de nível em questões por número."""
    questoes = {}
    numero_atual = None
    for texto, qtd in linhas:
        m = QUESTAO_RE.match(texto)
        if m:
            numero_atual = int(m.group(1))
            questoes[numero_atual] = [(m.group(2), qtd)]
        elif numero_atual is not None:
            questoes[numero_atual].append((texto, qtd))
    resultado = {}
    for numero, partes in questoes.items():
        texto_completo = "\n".join(t for t, _ in partes if t)
        qtd_total = sum(q for _, q in partes)
        resultado[numero] = (texto_completo, qtd_total)
    return resultado


def classificar_tipo(enunciado: str, gabarito: str) -> str:
    gabarito_limpo = gabarito.strip().rstrip(".")
    if LETRA_UNICA_RE.match(gabarito_limpo):
        return "Múltipla escolha"
    if ALTERNATIVA_RE.search(enunciado):
        return "Múltipla escolha"
    if re.search(r"\bV\b.*\bF\b|verdadeir|falso", enunciado, re.IGNORECASE):
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
            formulas_faltantes_enunciado INTEGER,
            gabarito TEXT,
            formulas_faltantes_gabarito INTEGER,
            arquivo_origem TEXT,
            capturado_em TEXT,
            UNIQUE(livro, capitulo, nivel, numero)
        )
        """
    )
    conn.commit()
    return conn


def salvar_questao(conn: sqlite3.Connection, livro: str, capitulo: str,
                    arquivo_origem: str, q: Questao) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO questoes (
            livro, capitulo, nivel, numero, tipo, enunciado,
            formulas_faltantes_enunciado, gabarito,
            formulas_faltantes_gabarito, arquivo_origem, capturado_em
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            livro, capitulo, q.nivel, q.numero, q.tipo, q.enunciado,
            q.formulas_faltantes_enunciado, q.gabarito,
            q.formulas_faltantes_gabarito, arquivo_origem,
            datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()


# --------------------------------------------------------------------------
# Pipeline principal
# --------------------------------------------------------------------------

def processar_arquivo(caminho_docx: str) -> list:
    paragrafos = carregar_paragrafos(caminho_docx)
    linhas = [texto_e_fórmulas_faltantes(p) for p in paragrafos]
    linhas = [(t, q) for t, q in linhas if t]

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
            enunciado, qtd_falt_enun = exercicios.get(numero, ("", 0))
            gabarito, qtd_falt_gab = gabaritos.get(numero, ("", 0))
            if not enunciado:
                log(f"AVISO: Nível-{nivel} questão {numero} não tem enunciado "
                    f"(só gabarito). Pulando.")
                continue
            if not gabarito:
                log(f"AVISO: Nível-{nivel} questão {numero} não tem gabarito "
                    f"correspondente.")
            tipo = classificar_tipo(enunciado, gabarito)
            questoes.append(Questao(
                nivel=nivel, numero=numero, tipo=tipo, enunciado=enunciado,
                formulas_faltantes_enunciado=qtd_falt_enun, gabarito=gabarito,
                formulas_faltantes_gabarito=qtd_falt_gab,
            ))
    return questoes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("docx", help="Arquivo .docx do capítulo")
    parser.add_argument("--livro", required=True, help="Nome do livro (ex: 'Matemática para Vestibular Vol 01')")
    parser.add_argument("--capitulo", required=True, help="Nome do capítulo/assunto (ex: 'Lógica e Conjuntos')")
    parser.add_argument("--output", default="banco_matvest.db", help="Caminho do SQLite de saída")
    args = parser.parse_args()

    log(f"Processando {args.docx} ...")
    questoes = processar_arquivo(args.docx)

    conn = init_db(args.output)
    arquivo_origem = Path(args.docx).name
    for q in questoes:
        salvar_questao(conn, args.livro, args.capitulo, arquivo_origem, q)
    conn.close()

    total = len(questoes)
    com_falta_enun = sum(1 for q in questoes if q.formulas_faltantes_enunciado > 0)
    com_falta_gab = sum(1 for q in questoes if q.formulas_faltantes_gabarito > 0)
    sem_gabarito = sum(1 for q in questoes if not q.gabarito)

    log(f"Concluído. {total} questões salvas em {args.output}.")
    log(f"  - {com_falta_enun} com fórmula ausente no enunciado")
    log(f"  - {com_falta_gab} com fórmula ausente no gabarito")
    log(f"  - {sem_gabarito} sem gabarito correspondente encontrado")


if __name__ == "__main__":
    main()
