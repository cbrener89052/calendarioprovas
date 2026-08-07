#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai a grade de aulas do 2o semestre de 2025 do PDF (7 turmas: 9C1,
9C2, 10C1, 10C2, 11C1, 11C2, 12C1 -- nao existia 12C2).

O PDF nao tem camada de texto (os rotulos sao curvas), entao o caminho e
OCR (tesseract) sobre um render em alta resolucao (400 dpi), com as
palavras agrupadas pela GEOMETRIA das celulas — que essa, sim, e dado
exato do PDF (ver esqueleto_grade_2025.py). O OCR preenche o texto; a
geometria decide a que celula e a que tempo ele pertence.

Uso:
    python extrair_grade_2025.py            # roda o OCR de novo
    python extrair_grade_2025.py --tsv      # reusa os .tsv ja gerados
"""
import pymupdf, os, csv, re, glob, collections, pprint, sys, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(BASE, "horarios2025", "horarios2025.pdf")
DESTINO = os.path.join(BASE, "horarios2025", "grade_2sem_2025.py")
TMP = "/tmp/claude-0/-home-user-calendarioprovas/0ed50719-fdee-5a75-b535-90c8452a29a6/scratchpad"

TURMAS = ["12C1", "11C2", "11C1", "10C2", "10C1", "9C2", "9C1"]  # ordem das paginas
DIAS = {1: "Seg", 2: "Ter", 3: "Qua", 4: "Qui", 5: "Sex"}

# Faixas verticais dos 11 tempos, em pontos do PDF (ver esqueleto_grade_2025.py)
FAIXAS = [(104, 135), (140, 171), (176, 207), (223, 254), (259, 290),
          (306, 337), (342, 373), (374, 405), (406, 437), (446, 477),
          (478, 509)]
COLS_X = [95, 166, 238, 310, 382]        # x0 de cada coluna de dia, em pontos
DPI_ESCALA = 400 / 72                    # pontos -> pixels do render a 400dpi


def gerar_tsv(pagina_idx):
    doc = pymupdf.open(PDF)
    p = doc[pagina_idx]
    pix = p.get_pixmap(dpi=400)
    png = os.path.join(TMP, f"p{pagina_idx + 1}_hires.png")
    pix.save(png)
    saida = os.path.join(TMP, f"p{pagina_idx + 1}_ocr")
    subprocess.run(["tesseract", png, saida, "--psm", "11", "-l", "por", "tsv"],
                   check=True, capture_output=True)
    return saida + ".tsv"


def palavras_do_tsv(caminho):
    out = []
    with open(caminho) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            txt = row["text"].strip()
            if not txt or row["conf"] in ("-1", ""):
                continue
            x = int(row["left"]) / DPI_ESCALA
            y = int(row["top"]) / DPI_ESCALA
            w = int(row["width"]) / DPI_ESCALA
            h = int(row["height"]) / DPI_ESCALA
            out.append((x, y, w, h, txt))
    return out


CENTROS = [(a + b) / 2 for (a, b) in FAIXAS]
DIST_MAX = 22   # px: além disso, e melhor nao atribuir a nenhum tempo


def celula_da(x, y):
    """(dia, tempo) mais provavel para uma palavra em (x, y).

    O tempo e escolhido pelo CENTRO da faixa mais proximo, nao por
    conter o y — os retangulos de celulas vizinhas vazias as vezes se
    fundem visualmente num bloco mais alto que o de um tempo so (inclusive
    atravessando o intervalo do recreio), e nesse caso o texto continua
    centrado no tempo real dele, nao no meio do retangulo desenhado.
    """
    dia = None
    for i, x0 in enumerate(COLS_X):
        x1 = COLS_X[i + 1] if i + 1 < len(COLS_X) else x0 + 72
        if x0 - 3 <= x < x1 - 3:
            dia = i + 1
    if dia is None:
        return None
    i_mais_perto = min(range(11), key=lambda i: abs(y - CENTROS[i]))
    if abs(y - CENTROS[i_mais_perto]) > DIST_MAX:
        return None
    return (dia, i_mais_perto + 1)


LINHA_TOL = 4.5     # px: palavras com y a menos disso sao a MESMA linha


def texto_em_ordem_de_leitura(itens):
    """itens: [(y, x, txt)]. Agrupa em linhas por proximidade vertical
    (o texto tem ~7px de altura e o OCR erra o baseline em 2-3px, o que
    inverte a ordem se sortearmos direto por (y, x)) e devolve as linhas
    de cima para baixo, cada uma da esquerda para a direita."""
    itens = sorted(itens)                     # ordena por y bruto primeiro
    linhas, atual, y0 = [], [], None
    for (y, x, txt) in itens:
        if y0 is not None and y - y0 > LINHA_TOL:
            linhas.append(atual)
            atual = []
        atual.append((x, txt))
        y0 = y
    if atual:
        linhas.append(atual)
    return " ".join(t for linha in linhas
                    for (_x, t) in sorted(linha))


def agrupar_celulas(palavras):
    """{(dia, tempo): "texto da célula"} — junta as palavras de uma
    celula e as ordena por posicao de leitura (linha, depois coluna)."""
    grupos = collections.defaultdict(list)
    for (x, y, w, h, txt) in palavras:
        if x < 90 or y < 100:                 # fora da grade (cabecalho)
            continue
        c = celula_da(x, y)
        if c:
            grupos[c].append((y, x, txt))
    return {c: texto_em_ordem_de_leitura(itens) for c, itens in grupos.items()}


def main():
    usar_tsv = "--tsv" in sys.argv
    grades = {}
    for i, turma in enumerate(TURMAS):
        tsv = os.path.join(TMP, f"p{i + 1}_ocr.tsv") if usar_tsv else gerar_tsv(i)
        palavras = palavras_do_tsv(tsv)
        grades[turma] = agrupar_celulas(palavras)
        print(f"{turma}: {len(grades[turma])} células com texto")

    ordem = ["9C1", "9C2", "10C1", "10C2", "11C1", "11C2", "12C1"]
    grades = {t: grades[t] for t in ordem}
    with open(DESTINO, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""Texto BRUTO (nao interpretado) de cada celula da grade\n')
        f.write("de 2025, por OCR + geometria (extrair_grade_2025.py). Formato:\n")
        f.write("{turma: {(dia, tempo): texto_da_celula}}. Precisa ser conferido\n")
        f.write('e depois convertido em (disciplina, professor) -- ver revisar_grade_2025.py.\n"""\n\n')
        f.write("GRADE_BRUTA_2025 = ")
        f.write(pprint.pformat(grades, width=100))
        f.write("\n")
    print("Gravado:", DESTINO)


if __name__ == "__main__":
    main()
