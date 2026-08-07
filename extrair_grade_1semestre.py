#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extrai a grade de aulas do 1o semestre de 2026 do PDF do Untis.

A grade do 1o semestre e DIFERENTE da do 2o, entao nao da para reaproveitar
a que esta em gerar_calendario.py.

O PDF nao numera os tempos, mas cada celula traz a HORA DE INICIO da aula
(7.15, 8.05, ...), e a escola confirmou a correspondencia hora -> tempo
(TEMPOS abaixo). Isso e melhor do que deduzir o tempo pela posicao
vertical: nao depende de calibrar coordenadas nem de a linha ter rotulo.

Layout de cada celula (3 linhas):
    disciplina   hora-de-inicio
    *Professor
    Sala

Grava: horarios_1semestre/grade_1semestre.py  (dict pronto para importar)
"""
import pymupdf, os, re, collections, pprint

BASE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(BASE, "horarios_1semestre",
                   "EM C Horarios Turmas 20260130.pdf")
DESTINO = os.path.join(BASE, "horarios_1semestre", "grade_1semestre.py")

# hora de inicio -> numero do tempo (confirmado pela escola)
TEMPOS = {
    "7.15": 1, "8.05": 2, "8.55": 3, "10.00": 4, "10.50": 5, "11.55": 6,
    "12.45": 7, "13.30": 8, "14.15": 9, "15.10": 10, "15.55": 11,
}

DIAS = {"Mo": 1, "Di": 2, "Mi": 3, "Do": 4, "Fr": 5}

HORA = re.compile(r"^\d{1,2}\.\d{2}$")
SALA = re.compile(r"^[A-Z]\d{3}$|^SPH|^Aula$|^Bib", re.I)


def paginas(caminho=PDF):
    """[(turma, [palavras])] — uma pagina por turma."""
    doc = pymupdf.open(caminho)
    out = []
    for i in range(doc.page_count):
        ws = doc[i].get_text("words")
        turma = None
        for w in ws:
            if re.fullmatch(r"(9|10|11|12)C[12]", w[4]):
                turma = w[4]
                break
        if turma:
            out.append((turma, ws))
    return out


def limites_das_colunas(ws):
    """Fronteiras horizontais das 5 colunas de dia.

    O rotulo do dia vem centralizado na coluna, entao as fronteiras sao os
    pontos medios entre rotulos vizinhos, estendidos meia coluna para fora
    nas pontas.
    """
    centros = {}
    for w in ws:
        if w[4] in DIAS:
            centros[DIAS[w[4]]] = (w[0] + w[2]) / 2
    if len(centros) != 5:
        raise SystemExit(f"cabeçalho de dias incompleto: {centros}")
    c = [centros[d] for d in (1, 2, 3, 4, 5)]
    meios = [(c[i] + c[i + 1]) / 2 for i in range(4)]
    return [c[0] - (meios[0] - c[0])] + meios + [c[4] + (c[4] - meios[3])]


def extrair_turma(ws):
    """({(dia, tempo): (disciplina, professor)}, [avisos]) de uma pagina.

    O tempo vem da HORA, que e propriedade da LINHA: todas as celulas de
    uma mesma linha trazem a mesma hora de inicio. Ler a hora pela linha
    (e nao por celula) evita a ambiguidade de a qual coluna pertence o
    rotulo, que fica na divisa entre duas colunas.
    """
    bordas = limites_das_colunas(ws)

    def dia_de(x):
        for i in range(5):
            if bordas[i] <= x < bordas[i + 1]:
                return i + 1
        return None

    # agrupa em linhas de texto (~4px de tolerancia vertical)
    linhas = collections.defaultdict(list)
    for w in ws:
        if w[1] < 85:                        # cabeçalho da pagina
            continue
        linhas[round(w[1] / 4)].append((w[0], w[4]))

    celulas, avisos = {}, []
    chaves = sorted(linhas)
    for i, k in enumerate(chaves):
        itens = sorted(linhas[k])
        horas = {t for (_x, t) in itens if HORA.match(t) and t in TEMPOS}
        if not horas:
            continue                          # linha de professor ou sala
        if len(horas) > 1:
            avisos.append(f"linha y~{k * 4} com horas diferentes: {horas}")
            continue
        tempo = TEMPOS[horas.pop()]

        # disciplinas desta linha, por dia
        porta = collections.defaultdict(list)
        for (x, t) in itens:
            if HORA.match(t) or t.startswith("*") or SALA.match(t):
                continue
            if re.fullmatch(r"\d{1,2}\.\d{1,2}", t):
                continue                      # rotulo de hora truncado
            d = dia_de(x)
            if d:
                porta[d].append(t)

        # professores: nas linhas seguintes, ate a proxima linha que traga
        # hora (ou seja, ate a proxima aula). A distancia entre a linha da
        # disciplina e a do professor varia, entao nao da para olhar so a
        # linha imediatamente seguinte.
        profs = {}
        for k2 in chaves[i + 1:]:
            itens2 = sorted(linhas[k2])
            if any(HORA.match(t) and t in TEMPOS for (_x, t) in itens2):
                break
            for (x, t) in itens2:
                if t.startswith("*"):
                    d = dia_de(x)
                    if d and d not in profs:
                        profs[d] = t.lstrip("*").rstrip(".")

        for d, discs in porta.items():
            escolhida = discs[0]
            if len(discs) > 1:
                # celula com grupos paralelos: fica a disciplina regular, e
                # nao a trilha opcional de apoio/aprofundamento, que e quem
                # se divide em grupos
                regulares = [x for x in discs
                             if not re.fullmatch(r"ap|apr|ap[a-z]+", x)]
                escolhida = regulares[0] if regulares else discs[0]
                avisos.append(f"dia {d} tempo {tempo}: grupos paralelos "
                              f"{discs} — mantida '{escolhida}'")
            celulas[(d, tempo)] = (escolhida, profs.get(d, "-"))
    return celulas, avisos


def main():
    grades = {}
    for (turma, ws) in paginas():
        grades[turma], avisos = extrair_turma(ws)
        print(f"{turma}: {len(grades[turma])} aulas na semana")
        for a in avisos:
            print(f"    ~ {a}")

    ordem = ["9C1", "9C2", "10C1", "10C2", "11C1", "11C2", "12C1", "12C2"]
    grades = {t: grades[t] for t in ordem if t in grades}

    with open(DESTINO, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""Grade de aulas do 1o semestre de 2026, extraida do PDF\n')
        f.write("do Untis por extrair_grade_1semestre.py. Nao editar a mao.\n")
        f.write('"""\n\nGRADE_1SEM = ')
        f.write(pprint.pformat(grades, width=78))
        f.write("\n")
    print("Gravado:", DESTINO)

    discs = collections.Counter(d for g in grades.values()
                                for (d, _p) in g.values())
    print("\ndisciplinas encontradas:")
    for d, n in sorted(discs.items()):
        print(f"   {d}: {n}")


if __name__ == "__main__":
    main()
