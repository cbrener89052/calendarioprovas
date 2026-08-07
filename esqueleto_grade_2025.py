#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai a ESTRUTURA da grade de 2025 do PDF (quais celulas existem, em
que dia e em que tempos), sem os rotulos.

O PDF de 2025 nao tem camada de texto: os rotulos foram convertidos em
curvas, entao nao ha o que extrair e nao ha OCR disponivel aqui. O que da
para recuperar com precisao e a GEOMETRIA -- os retangulos das celulas.

As alturas das celulas caem em 11 faixas regulares que correspondem
exatamente aos 11 tempos do dia, com as folgas nos horarios de intervalo
(depois do 3o e do 5o tempo) e no fim da tarde. Com isso, a leitura visual
dos rotulos fica ancorada: basta dizer o que esta escrito em cada celula,
sem precisar julgar a qual tempo ela pertence.

Uso: python esqueleto_grade_2025.py > /tmp/esqueleto.txt
"""
import pymupdf, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(BASE, "horarios2025", "horarios2025.pdf")

DIAS = {1: "Seg", 2: "Ter", 3: "Qua", 4: "Qui", 5: "Sex"}


# Faixas verticais dos 11 tempos, em pontos do PDF. Sao as mesmas em todas
# as paginas (mesma impressao do Untis) -- por isso ficam fixas aqui, e nao
# deduzidas pagina a pagina: numa turma sem aula em determinado tempo a
# faixa correspondente simplesmente nao seria desenhada.
# As folgas entre faixas sao os intervalos: depois do 3o (9h40-10h), depois
# do 5o (11h35-11h55) e depois do 9o (15h-15h10).
FAIXAS = [(104, 135), (140, 171), (176, 207), (223, 254), (259, 290),
          (306, 337), (342, 373), (374, 405), (406, 437), (446, 477),
          (478, 509)]


def faixas_dos_tempos(pagina):
    return FAIXAS


def colunas(pagina):
    """x inicial de cada coluna de dia."""
    xs = sorted({round(dr["rect"].x0) for dr in pagina.get_drawings()
                 if dr["rect"].width > 40 and dr["rect"].x0 > 90})
    # colunas vizinhas diferem em ~1px por causa da espessura da borda
    limpo = []
    for x in xs:
        if not limpo or x - limpo[-1] > 10:
            limpo.append(x)
    return limpo


def celulas(pagina):
    """[(dia, [tempos])] de cada celula desenhada na pagina."""
    faixas = faixas_dos_tempos(pagina)
    cols = colunas(pagina)
    if len(faixas) != 11 or len(cols) != 5:
        return None, faixas, cols

    def tempos_de(y0, y1):
        return [i + 1 for i, (a, b) in enumerate(faixas)
                if y0 - 4 <= a and b <= y1 + 4]

    vistas, out = set(), []
    for dr in pagina.get_drawings():
        r = dr["rect"]
        if not (r.width > 40 and r.height > 8 and r.x0 > 90 and r.y0 > 100):
            continue
        if r.height > 200:                 # moldura externa da grade
            continue
        d = None
        for i, x in enumerate(cols):
            if abs(r.x0 - x) <= 3:
                d = i + 1
        if d is None:
            continue
        ts = tempos_de(round(r.y0), round(r.y1))
        if not ts:
            continue
        chave = (d, tuple(ts))
        if chave in vistas:
            continue
        vistas.add(chave)
        out.append((d, ts))
    # mantem so a celula mais especifica quando uma engloba a outra
    out.sort(key=lambda x: (x[0], x[1][0], len(x[1])))
    final, ocupado = [], collections.defaultdict(set)
    for (d, ts) in out:
        if any(t in ocupado[d] for t in ts):
            continue
        final.append((d, ts))
        ocupado[d].update(ts)
    return final, faixas, cols


def main():
    doc = pymupdf.open(PDF)
    for i in range(doc.page_count):
        cel, faixas, cols = celulas(doc[i])
        print(f"=== página {i + 1}  ({len(faixas)} faixas, {len(cols)} colunas)")
        if cel is None:
            print("   !! estrutura inesperada")
            continue
        for d in range(1, 6):
            desta = sorted([c for c in cel if c[0] == d], key=lambda x: x[1][0])
            marca = ", ".join(
                (f"T{t[1][0]}" if len(t[1]) == 1
                 else f"T{t[1][0]}-{t[1][-1]}") for t in desta)
            print(f"   {DIAS[d]}: {marca}")


if __name__ == "__main__":
    main()
