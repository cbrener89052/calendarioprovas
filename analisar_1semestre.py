#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta as aulas cedidas para provas no 1o semestre de 2026 (o que de fato
ocorreu), no mesmo formato do relatorio do 2o semestre.

Diferente do 2o semestre, aqui nada e planejado: o calendario de provas ja
foi executado e esta em Horario modelo/Klausurplan_2026_1SEM.xlsx. O
trabalho e ler o que aconteceu e cruzar com a grade de aulas do 1o
semestre (que e DIFERENTE da do 2o).

Saida, uma aba por turma:
  Disciplina | Professor | aulas/semana | aulas no semestre | cedidas | %

Cuidado com o arquivo do 1o semestre: o preenchimento foi manual e e
bem irregular -- os tempos aparecem ora na linha do titulo, ora na da
sala, com ou sem "º", por extenso ("primeiro e segundo"), como fracao
("4.5") ou como intervalo ("1-7"). Por isso o parser abaixo e tolerante,
e tudo que ele NAO conseguir ler com seguranca e reportado em vez de
adivinhado.
"""
import openpyxl, os, re, collections, datetime, unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Horario modelo", "Klausurplan_2026_1SEM.xlsx")
OUT = os.path.join(BASE, "Horario desenvolvido")

TURMAS = ["9C1", "9C2", "10C1", "10C2", "11C1", "11C2", "12C1", "12C2"]
COLS = {"E": 1, "F": 2, "G": 3, "H": 4, "I": 5}
SEMANA1 = datetime.date(2026, 2, 2)     # segunda da semana 1 do 1o semestre

# Marcacoes que NAO sao prova de disciplina (nao consomem tempo de colega
# de forma atribuivel a uma disciplina).
NAO_PROVA = ("unterrichtsfrei", "fach |", "matéria |", "materia |", "cc ",
             "2ch", "viagem", "sim ", "ag1", "ag9", "ag10", "s1-", "s2-",
             "s3-", "s4-", "sip", "conselho", "recesso", "feriado",
             "alemun", "dsd")

EXTENSO = {"primeiro": 1, "segundo": 2, "terceiro": 3, "quarto": 4,
           "quinto": 5, "sexto": 6, "setimo": 7, "oitavo": 8, "nono": 9,
           "decimo": 10}


def week_row(w):
    return 3 + 3 * (w - 1)


def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def _limpar(txt):
    """Normaliza o texto para leitura dos tempos.

    Tira acentos, remove codigos de sala (E301, A 314...) para os numeros
    deles nao virarem 'tempos', e uniformiza o ordinal: no arquivo o mesmo
    tempo aparece como '1º', '1o', '1°' e '1ª'.
    """
    t = sem_acento(txt.lower())
    t = re.sub(r"\b[a-z]\s*\d{3}\b", " ", t)        # sala: E301, A 304
    t = re.sub(r"(\d)\s*[o°ºa](?![a-z0-9])", r"\1º", t)
    return t


def tempos_do_texto(txt):
    """Lista de tempos (1..11) que a prova ocupou, lida de um texto solto.

    Devolve [] quando nao houver nada reconhecivel -- nunca chuta.
    """
    # so os trechos que falam de tempo/aula interessam; 'Sala de aula' e
    # 'Sala de provas' sao descricao de local e nao podem entrar
    partes = []
    for seg in txt.split("|"):
        s = _limpar(seg)
        if re.match(r"\s*sala\b", s) and not re.search(r"temp", s):
            continue
        partes.append(s)
    t = " ".join(partes)

    # "1-7", "1 a 7": intervalo
    m = re.search(r"\b(\d{1,2})\s*º?\s*(?:-|a|ao|ate)\s*(\d{1,2})\s*º?\s*temp", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if 1 <= a <= b <= 11:
            return list(range(a, b + 1))

    # por extenso: "primeiro e segundo tempos"
    achados = [v for k, v in EXTENSO.items() if re.search(rf"\b{k}\b", t)]
    if achados:
        return sorted(set(achados))

    # "4.5" ou "2,3" (duas aulas coladas por ponto/virgula)
    m = re.search(r"(?<!\d)(\d)\s*[.,]\s*(\d)(?!\d)", t)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if 1 <= a <= 11 and 1 <= b <= 11:
            return sorted({a, b})

    # forma geral: numeros num trecho que fala de tempo/aula --
    # "4º, 5 e 6º tempos", "2 e 3 tempos", "6 tempo", "4º e 5º temp"
    if re.search(r"temp|aula", t):
        nums = [int(x) for x in re.findall(r"(?<!\d)(\d{1,2})(?!\d)", t)]
        nums = [n for n in nums if 1 <= n <= 11]
        if nums:
            return sorted(set(nums))

    # numeros com marcador de ordinal, mesmo sem a palavra "tempo"
    nums = [int(x) for x in re.findall(r"(?<!\d)(\d{1,2})\s*º", t)]
    nums = [n for n in nums if 1 <= n <= 11]
    return sorted(set(nums))


# Como a disciplina aparece escrita no arquivo -> codigo usado na grade.
# No 1o semestre o preenchimento foi livre, entao a mesma disciplina
# aparece de varias formas ("MAT", "MATEMÁTICA", "MAT/ClaMe e JJ").
ALIAS = [
    ("lp/lit/red", "LPLITRED"), ("pred", "pred"), ("redacao", "pred"),
    ("port", "port"), ("portugues", "port"), ("gram", "gram"),
    ("matematica", "mat"), ("mat", "mat"),
    ("quimica", "qui"), ("qui", "qui"),
    ("fisica", "fis"), ("fis", "fis"),
    ("biologia", "bio"), ("bio", "bio"),
    ("geografia", "geo"), ("geo", "geo"),
    ("historia", "his"), ("hist", "his"), ("his", "his"),
    ("ingles", "ing"), ("ing", "ing"),
    ("alemao", "DaF"), ("daf", "DaF"),
    ("gl", "GL"),
    ("filosofia", "fil"), ("fil", "fil"),
    ("sociologia", "soc"), ("soc", "soc"),
]


def disciplina_do_texto(txt):
    """Codigo da disciplina, procurado em QUALQUER linha da celula.

    No arquivo do 1o semestre a ordem das 3 linhas nao e confiavel: em
    varias celulas o tempo esta na linha do titulo e o nome da disciplina
    na de baixo (ou falta). Devolve None quando nao houver nome.
    """
    t = sem_acento(txt.lower())
    t = re.sub(r"\b[a-z]\s*\d{3}\b", " ", t)     # tira codigo de sala
    for alias, cod in ALIAS:
        if re.search(rf"(?<![a-z]){re.escape(alias)}(?![a-z])", t):
            return cod
    return None


def ler_provas(caminho=SRC):
    """[(turma, semana, dia, texto, [tempos])] do que foi aplicado.

    Tambem devolve a lista do que nao deu para interpretar.
    """
    wb = openpyxl.load_workbook(caminho, data_only=True)
    provas, ilegiveis = [], []
    for turma in TURMAS:
        ws = wb[turma]
        for w in range(1, 25):
            r = week_row(w)
            if r + 2 > ws.max_row:
                break
            for col, d in COLS.items():
                v = ws[f"{col}{r}"].value
                if not v:
                    continue
                cabeca = str(v).strip()
                baixo = sem_acento(cabeca.lower())
                if any(x in baixo for x in NAO_PROVA):
                    continue
                linhas = [cabeca,
                          str(ws[f"{col}{r + 1}"].value or ""),
                          str(ws[f"{col}{r + 2}"].value or "")]
                junto = " | ".join(x for x in linhas if x.strip())
                tempos = tempos_do_texto(junto)
                disc = disciplina_do_texto(junto)
                if not tempos or not disc:
                    falta = []
                    if not tempos:
                        falta.append("tempos")
                    if not disc:
                        falta.append("disciplina")
                    ilegiveis.append((turma, w, d, junto, "+".join(falta)))
                    continue
                provas.append((turma, w, d, junto, tempos, disc))
    return provas, ilegiveis


def main():
    provas, ilegiveis = ler_provas()
    print(f"Provas lidas: {len(provas)}")
    print(f"Não interpretadas: {len(ilegiveis)}")
    for x in ilegiveis:
        print("   ?", x)
    for t in TURMAS:
        cont = collections.Counter(p[5] for p in provas if p[0] == t)
        print(f"  {t}: {sum(cont.values())} provas — " +
              ", ".join(f"{k}:{v}" for k, v in sorted(cont.items())))


if __name__ == "__main__":
    main()
