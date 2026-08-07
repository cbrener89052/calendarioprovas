#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Converte o texto bruto da grade de 2025 (lido por OCR em
extrair_grade_2025.py) em {(dia, tempo): [(codigo, professor), ...]}.

Uma celula pode ter mais de um (codigo, professor) -- grupos paralelos,
varias linhas de professores diferentes na mesma disciplina e mesmo
tempo (ver texto_em_ordem_de_leitura em extrair_grade_2025.py, que ja
separa as linhas corretamente).

O texto vem de OCR sobre uma imagem, entao tem ruido: codigos de sala
lidos errado (A307 -> AS07), letras extras, tokens colados sem espaco
('ecSJu'). A DISCIPLINA e confiavel (e a primeira palavra da linha,
reconhecida contra um vocabulario fechado). O PROFESSOR e melhor
esforço: pega a proxima palavra que nao seja marcador de grupo ('t', 'c',
'D') nem pareça codigo de sala.
"""
import re, unicodedata, sys, os, pprint

BASE = os.path.dirname(os.path.abspath(__file__))

# token (minusculo, sem acento) -> codigo da disciplina, igual ao 2o
# semestre de 2026 sempre que possivel, para os relatorios ficarem
# comparaveis.
CODE_MAP = {
    "ingt": "ingT", "ing": "ing", "pgram": "gram", "pred": "pred",
    "plit": "port", "p": "port", "mat": "mat", "qui": "qui", "fis": "fis",
    "bio": "bio", "geo": "geo", "hist": "his", "his": "his", "daf": "DaF",
    "gl": "GL", "fil": "fil", "soc": "soc",
    # sem prova, mas podem doar tempo
    "elet": "elet", "art": "art", "artt": "art", "mus": "mus", "esp": "esp",
    "tec": "tec", "ec": "tec", "ap": "apoio", "apmat": "apoio",
    "appor": "apoio", "prve": "prve",
    # nao sao aula (ficam de fora da grade util)
    "ag": None, "app": None, "equip": None, "equipe": None,
}

# marcadores de subgrupo ('elet t', 'elet c', 'ap D') e ruido -- nunca sao
# nome de professor
MARCADORES = {"t", "c", "d"}

SALA = re.compile(r"^[A-Z]?\d{2,4}[A-Za-z]{0,2}$|^Sp\d?", re.I)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def prefixo_do_codigo(palavra):
    """(codigo, resto) se 'palavra' comeca com uma chave de CODE_MAP,
    None senao. 'resto' e o que sobra depois da chave -- cobre tokens
    colados por falha do OCR sem espaco, ex. 'plitDeb' = 'plit' + 'Deb'.

    So aceita quando a correspondencia e a palavra INTEIRA (resto vazio),
    ou quando o resto comeca com maiuscula (sinal de palavra colada). Sem
    essa checagem, chaves curtas como 'p' (Portugues) capturavam por
    engano siglas de professor que so por acaso comecam com a mesma
    letra, ex. 'PaH'.
    """
    p = sem_acento(palavra.lower())
    candidatos = [k for k in CODE_MAP if p.startswith(k)]
    if not candidatos:
        return None
    chave = max(candidatos, key=len)
    restante = palavra[len(chave):]
    if restante and not restante[0].isupper():
        return None
    return chave, restante


def linha_para_disciplinas(linha_txt):
    """[(codigo, professor)] de uma linha de texto (ex.: 'DaF Swa A312
    DaF EFr A317 DaF SGa A308' -> 3 pares)."""
    palavras = linha_txt.split()
    out, i = [], 0
    while i < len(palavras):
        achado = prefixo_do_codigo(palavras[i])
        if not achado:
            i += 1
            continue
        cod_bruto, embutido = achado
        codigo = CODE_MAP[cod_bruto]
        i += 1
        prof = None
        if embutido:                    # 'plitDeb' -> profesor ja veio junto
            prof = embutido
        else:
            while i < len(palavras) and palavras[i].lower() in MARCADORES:
                i += 1
            if i < len(palavras) and not SALA.match(palavras[i]) and \
               prefixo_do_codigo(palavras[i]) is None:
                prof = palavras[i]
                i += 1
        while i < len(palavras) and (SALA.match(palavras[i]) or
                                     palavras[i] in ("|",)):
            i += 1
        if codigo:                      # None = AG/equip: nao e aula util
            out.append((codigo, prof or "?"))
    return out


def grade_limpa(grade_bruta):
    """{turma: {(dia, tempo): [(codigo, prof), ...]}}"""
    out = {}
    for turma, celulas in grade_bruta.items():
        limpa = {}
        for k, txt in celulas.items():
            pares = linha_para_disciplinas(txt)
            if pares:
                limpa[k] = pares
        out[turma] = limpa
    return out


def main():
    sys.path.insert(0, os.path.join(BASE, "horarios2025"))
    from grade_2sem_2025 import GRADE_BRUTA_2025
    limpa = grade_limpa(GRADE_BRUTA_2025)
    destino = os.path.join(BASE, "horarios2025", "grade_2sem_2025_limpa.py")
    with open(destino, "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""Grade de 2025 ja interpretada: {turma: {(dia, tempo):\n')
        f.write("[(codigo, professor), ...]}}. Gerado por limpar_grade_2025.py\n")
        f.write('a partir de grade_2sem_2025.py (texto bruto do OCR).\n"""\n\n')
        f.write("GRADE_2025 = ")
        f.write(pprint.pformat(limpa, width=100))
        f.write("\n")
    print("Gravado:", destino)
    for t, g in limpa.items():
        n_multi = sum(1 for v in g.values() if len(v) > 1)
        print(f"  {t}: {len(g)} tempos preenchidos, {n_multi} com "
              f"grupos paralelos/vários professores")


if __name__ == "__main__":
    main()
