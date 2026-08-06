#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera propostas de calendario de provas para as turmas C do 2o semestre 2026.

Le  : Klausurplan_2026_2SEM.xlsx  (aba 10C2 = template com as datas corretas)
Grava: Horario desenvolvido/Proposta_N_...xlsx  (uma aba por turma)
       Horario desenvolvido/Relatorio_trocas_de_tempo.md

As grades das turmas foram extraidas do PDF turmas9a12_2osemestre2026.pdf
por leitura visual e conferidas contra siglas_profs_aux_etc.xlsx.
"""
import openpyxl, shutil, os, random, copy
from openpyxl.styles import Alignment, PatternFill
from openpyxl.utils import get_column_letter

# destaque visual para provas que precisaram cruzar o intervalo do recreio
# por falta de qualquer outra alternativa (ver regra na skill)
DESTAQUE_INTERVALO = PatternFill(start_color="FFC000", end_color="FFC000",
                                  fill_type="solid")

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "Klausurplan_2026_2SEM.xlsx")
OUT = os.path.join(BASE, "Horario desenvolvido")

DIAS = {1: "Seg", 2: "Ter", 3: "Qua", 4: "Qui", 5: "Sex"}
COL = {1: "E", 2: "F", 3: "G", 4: "H", 5: "I"}


def week_row(w):
    return 3 + 3 * (w - 1)


# ---------------------------------------------------------------- GRADES
# Notacao compacta: turma -> dia -> {tempo: "disciplina/professor"}
# dia: 1=Seg ... 5=Sex
# TODAS as aulas entram (inclusive as sem prova), porque um tempo sem prova
# ainda pode ser doado para a 2a parte de uma prova.
GRADE_TXT = {
    "9C1": {
        1: {1: "bio/Ale", 2: "geo/Mar", 3: "ing/APa-PaH-Velo", 4: "esp/-", 5: "esp/-",
            6: "GL/Caro-EFr-Eth", 7: "pred/Raf", 9: "apoio/Caro"},
        2: {1: "port/Jana", 2: "DaF/Caro-SGa-EFr", 3: "mat/BrSa", 4: "his/JuLa",
            5: "DaF/Caro-SGa-EFr", 6: "ing/APa-PaH-Velo", 8: "tec/SJu",
            9: "mat/BrSa", 10: "his/JuLa"},
        3: {1: "DaF/Caro-SGa-EFr", 2: "geo/Mar", 3: "bio/Ale", 4: "mat/BrSa",
            5: "mat/BrSa", 6: "GL/Caro-EFr-Eth", 7: "port/Jana", 9: "apoio/FBri"},
        4: {1: "DaF/Caro-SGa-EFr", 2: "DaF/Caro-SGa-EFr", 3: "art/-", 4: "art/-",
            5: "mat/BrSa", 6: "pred/Raf", 7: "fis/VSi", 9: "apoio/SMo"},
        5: {1: "pred/Raf", 2: "ing/APa-PaH-Velo", 3: "ing/APa-PaH-Velo",
            4: "DaF/Caro-SGa-EFr", 5: "GL/Caro-EFr-Eth", 6: "socem/DiS", 7: "qui/Fab"},
    },
    "9C2": {
        1: {1: "pred/Raf", 2: "fis/VSi", 3: "ing/APa-PaH-Velo", 4: "esp/-", 5: "esp/-",
            6: "GL/Caro-EFr-Eth", 7: "his/JuLa", 9: "apoio/Caro"},
        2: {1: "bio/Ale", 2: "DaF/Caro-SGa-EFr", 3: "tec/Tac", 4: "mat/BrSa",
            5: "DaF/Caro-SGa-EFr", 6: "ing/APa-PaH-Velo", 8: "bio/Ale",
            9: "his/JuLa", 10: "mat/BrSa"},
        3: {1: "DaF/Caro-SGa-EFr", 2: "qui/Fab", 3: "mat/BrSa", 4: "port/Jana",
            5: "port/Jana", 6: "GL/Caro-EFr-Eth", 7: "geo/Mar", 9: "apoio/FBri"},
        4: {1: "DaF/Caro-SGa-EFr", 2: "DaF/Caro-SGa-EFr", 3: "art/-", 4: "art/-",
            5: "pred/Raf", 6: "mat/BrSa", 7: "mat/BrSa", 9: "apoio/SMo"},
        5: {1: "socem/DiS", 2: "ing/APa-PaH-Velo", 3: "ing/APa-PaH-Velo",
            4: "DaF/Caro-SGa-EFr", 5: "GL/Caro-EFr-Eth", 6: "geo/Mar", 7: "pred/Raf"},
    },
    "10C1": {
        1: {1: "mat/FBri", 2: "DaF/Eth-EFr-Swa", 3: "pred/BPad", 4: "fis/VSi",
            5: "ing/APa", 6: "tec/SJu", 7: "bio/Lza", 9: "proj/-", 10: "proj/-"},
        2: {1: "DaF/Eth-EFr-Swa", 2: "elet/-", 3: "art/-", 4: "art/-", 5: "port/MFo",
            6: "qui/CAl", 7: "bio/Lza", 9: "gram/SMo", 10: "his/ALu", 11: "mat/BrSa"},
        3: {1: "fil/LAn", 2: "DaF/Eth-EFr-Swa", 3: "GL/EFr-Car-Swa", 4: "ing/APa",
            5: "soc/Kle", 6: "mat/BrSa", 7: "mat/BrSa", 9: "apoio/SGa"},
        4: {1: "fis/VSi", 2: "ing/APa", 3: "ing/APa", 4: "geo/Mlo",
            5: "DaF/Eth-EFr-Swa", 6: "his/ALu", 8: "esp/-", 9: "esp/-",
            10: "pred/BPad", 11: "bio/Lza"},
        5: {1: "GL/EFr-Car-Swa", 2: "geo/Mlo", 3: "DaF/Eth-EFr-Swa", 4: "port/MFo",
            5: "qui/CAl", 6: "mat/FBri", 7: "finan/Mlo"},
    },
    "10C2": {
        1: {1: "port/MFo", 2: "DaF/Eth-EFr-Swa", 3: "mat/FBri", 4: "qui/CAl",
            5: "pred/BPad", 6: "bio/Lza", 7: "fis/VSi", 9: "proj/-", 10: "proj/-"},
        2: {1: "DaF/Eth-EFr-Swa", 2: "elet/-", 3: "art/-", 4: "art/-", 5: "ing/Vir",
            6: "mat/BrSa", 7: "mat/BrSa", 9: "bio/Lza", 10: "bio/Lza", 11: "his/ALu"},
        3: {1: "geo/Mlo", 2: "DaF/Eth-EFr-Swa", 3: "GL/EFr-Car-Swa", 4: "ing/Vir",
            5: "ing/Vir", 6: "mat/FBri", 7: "fil/LAn", 9: "apoio/SGa"},
        4: {1: "geo/Mlo", 2: "port/MFo", 3: "his/ALu", 4: "mat/BrSa",
            5: "DaF/Eth-EFr-Swa", 6: "finan/Mlo", 8: "esp/-", 9: "esp/-",
            10: "fis/VSi", 11: "gram/SMo"},
        5: {1: "GL/EFr-Car-Swa", 2: "ing/Vir", 3: "DaF/Eth-EFr-Swa", 4: "qui/CAl",
            5: "soc/Kle", 6: "tec/Tac", 7: "pred/BPad"},
    },
    "11C1": {
        1: {1: "qui/CAl", 2: "mat/ClaMe", 3: "geo/Mar", 4: "pred/ACo",
            5: "GL/CBu-Swa-SGa", 6: "DaF/CBu-SGa-Swa", 7: "ing/Bea",
            9: "proj/APa", 10: "proj/APa"},
        2: {1: "mat/JJ", 2: "his/Ver", 3: "his/Ver", 4: "DaF/CBu-SGa-Swa", 5: "art/-",
            6: "art/-", 8: "qui/CAl", 9: "bio/Ale", 10: "pred/ACo", 11: "fis/Cadu",
            12: "prve/-", 13: "prve/-"},
        3: {1: "his/Ver", 2: "mat/ClaMe", 3: "apr/-", 4: "GL/CBu-Swa-SGa", 5: "apr/-",
            6: "DaF/CBu-SGa-Swa", 7: "apr/-", 9: "fil/LAn", 10: "bio/Ale",
            11: "mat/ClaMe", 12: "prve/-", 13: "prve/-"},
        4: {1: "fis/Cadu", 2: "fis/Cadu", 3: "mat/JJ", 4: "port/AMu", 5: "ing/Bea",
            6: "ing/Bea", 7: "DaF/CBu-SGa-Swa", 9: "ing/Bea", 10: "esp/-", 11: "esp/-",
            12: "prve/-", 13: "prve/-"},
        5: {1: "apr/-", 2: "soc/Kle", 3: "bio/Ale", 4: "geo/Mar",
            5: "DaF/CBu-SGa-Swa", 6: "gram/Raf", 7: "port/AMu",
            10: "prve/-", 11: "prve/-"},
    },
    "11C2": {
        1: {1: "pred/ACo", 2: "bio/Ale", 3: "mat/ClaMe", 4: "ing/PaH",
            5: "GL/CBu-Swa-SGa", 6: "DaF/CBu-SGa-Swa", 7: "geo/Mar",
            9: "proj/APa", 10: "proj/APa"},
        2: {1: "qui/CAl", 2: "mat/JJ", 3: "qui/CAl", 4: "DaF/CBu-SGa-Swa", 5: "art/-",
            6: "art/-", 8: "fis/Cadu", 9: "pred/ACo", 10: "his/Ver", 11: "his/Ver",
            12: "prve/-", 13: "prve/-"},
        3: {1: "geo/Mar", 2: "his/Ver", 3: "apr/-", 4: "GL/CBu-Swa-SGa", 5: "apr/-",
            6: "DaF/CBu-SGa-Swa", 7: "apr/-", 9: "fis/Cadu", 10: "mat/ClaMe",
            11: "fil/LAn", 12: "prve/-", 13: "prve/-"},
        4: {1: "mat/JJ", 2: "ing/PaH", 3: "bio/Ale", 4: "fis/Cadu", 5: "port/AMu",
            6: "port/AMu", 7: "DaF/CBu-SGa-Swa", 9: "gram/Raf", 10: "esp/-",
            11: "esp/-", 12: "prve/-", 13: "prve/-"},
        5: {1: "apr/-", 2: "bio/Ale", 3: "mat/ClaMe", 4: "soc/Kle",
            5: "DaF/CBu-SGa-Swa", 6: "ing/PaH", 7: "ing/PaH",
            10: "prve/-", 11: "prve/-"},
    },
    "12C1": {
        1: {1: "ing/PaH", 2: "ing/PaH", 3: "bio/Ale", 4: "DaF/CBu-EFr-Eth",
            5: "geo/Mar", 6: "geo/Mar", 7: "qui/CAl", 12: "prve/-", 13: "prve/-"},
        2: {1: "mat/Bre", 2: "bio/Ale", 3: "fis/Cadu", 4: "apr/-", 5: "apr/-",
            6: "GL/CBu-EFr-Eth", 8: "his/Wag", 9: "apr/-", 10: "apr/-",
            11: "port/Deb", 12: "prve/-", 13: "prve/-"},
        3: {1: "bio/Ale", 2: "soc/Kle", 3: "mat/Bre", 4: "fis/Cadu",
            5: "DaF/CBu-EFr-Eth", 6: "qui/Fab", 8: "esp/-", 9: "esp/-",
            10: "fil/LAn", 11: "his/Wag", 12: "prve/-", 13: "prve/-"},
        4: {1: "art/-", 2: "art/-", 3: "pred/AMu", 4: "ing/PaH", 5: "port/Deb",
            6: "mat/JJ", 7: "mat/JJ", 9: "GL/CBu-EFr-Eth", 10: "DaF/CBu-EFr-Eth",
            11: "port/Deb", 12: "prve/-", 13: "prve/-"},
        5: {1: "port/Deb", 2: "geo/Mar", 3: "qui/Fab", 4: "his/Wag", 5: "pred/AMu",
            6: "DaF/CBu-EFr-Eth", 7: "DaF/CBu-EFr-Eth"},
    },
    "12C2": {
        1: {1: "geo/Mar", 2: "qui/CAl", 3: "mat/Bre", 4: "DaF/CBu-EFr-Eth",
            5: "ing/Isb", 6: "ing/Isb", 7: "bio/Ale", 12: "prve/-", 13: "prve/-"},
        2: {1: "fis/Cadu", 2: "port/Deb", 3: "bio/Ale", 4: "apr/-", 5: "apr/-",
            6: "GL/CBu-EFr-Eth", 7: "mat/Bre", 9: "apr/-", 10: "apr/-",
            11: "his/Wag", 12: "prve/-", 13: "prve/-"},
        3: {1: "qui/Fab", 2: "his/Wag", 3: "pred/AMu", 4: "fil/LAn",
            5: "DaF/CBu-EFr-Eth", 6: "soc/Kle", 8: "esp/-", 9: "esp/-",
            10: "port/Deb", 11: "geo/Mar", 12: "prve/-", 13: "prve/-"},
        4: {1: "art/-", 2: "art/-", 3: "fis/Cadu", 4: "mat/JJ", 5: "mat/JJ",
            6: "bio/Ale", 7: "port/Deb", 9: "GL/CBu-EFr-Eth", 10: "DaF/CBu-EFr-Eth",
            11: "ing/Isb", 12: "prve/-", 13: "prve/-"},
        5: {1: "his/Wag", 2: "port/Deb", 3: "geo/Mar", 4: "pred/AMu", 5: "qui/Fab",
            6: "DaF/CBu-EFr-Eth", 7: "DaF/CBu-EFr-Eth"},
    },
}

# disciplinas que NAO geram prova (mas cujo tempo pode ser doado)
SEM_PROVA = {"esp", "art", "tec", "finan", "socem", "apoio", "proj",
             "apr", "elet", "prve"}

GRADES = {
    turma: {(d, t): tuple(v.split("/"))
            for d, tempos in dias.items() for t, v in tempos.items()}
    for turma, dias in GRADE_TXT.items()
}

_GRADES_ANTIGO = {
    "9C1": {
        (1, 1): ("bio", "Ale"), (1, 2): ("geo", "Mar"), (1, 3): ("ing", "APa-PaH-Velo"),
        (1, 6): ("GL", "Caro-EFr-Eth"), (1, 7): ("pred", "Raf"),
        (2, 1): ("port", "Jana"), (2, 2): ("DaF", "Caro-SGa-EFr"), (2, 3): ("mat", "BrSa"),
        (2, 4): ("his", "JuLa"), (2, 5): ("DaF", "Caro-SGa-EFr"), (2, 6): ("ing", "APa-PaH-Velo"),
        (2, 10): ("his", "JuLa"),
        (3, 1): ("DaF", "Caro-SGa-EFr"), (3, 2): ("geo", "Mar"), (3, 3): ("bio", "Ale"),
        (3, 4): ("mat", "BrSa"), (3, 5): ("mat", "BrSa"), (3, 6): ("GL", "Caro-EFr-Eth"),
        (3, 7): ("port", "Jana"),
        (4, 1): ("DaF", "Caro-SGa-EFr"), (4, 2): ("DaF", "Caro-SGa-EFr"), (4, 5): ("mat", "BrSa"),
        (4, 6): ("pred", "Raf"), (4, 7): ("fis", "VSi"),
        (5, 1): ("pred", "Raf"), (5, 2): ("ing", "APa-PaH-Velo"), (5, 4): ("DaF", "Caro-SGa-EFr"),
        (5, 5): ("GL", "Caro-EFr-Eth"), (5, 7): ("qui", "Fab"),
    },
    "9C2": {
        (1, 1): ("pred", "Raf"), (1, 2): ("fis", "VSi"), (1, 3): ("ing", "APa-PaH-Velo"),
        (1, 6): ("GL", "Caro-EFr-Eth"), (1, 7): ("his", "JuLa"),
        (2, 1): ("bio", "Ale"), (2, 2): ("DaF", "Caro-SGa-EFr"), (2, 4): ("mat", "BrSa"),
        (2, 5): ("DaF", "Caro-SGa-EFr"), (2, 6): ("ing", "APa-PaH-Velo"), (2, 8): ("bio", "Ale"),
        (2, 9): ("his", "JuLa"), (2, 10): ("mat", "BrSa"),
        (3, 1): ("DaF", "Caro-SGa-EFr"), (3, 2): ("qui", "Fab"), (3, 3): ("mat", "BrSa"),
        (3, 4): ("port", "Jana"), (3, 6): ("GL", "Caro-EFr-Eth"), (3, 7): ("geo", "Mar"),
        (4, 1): ("DaF", "Caro-SGa-EFr"), (4, 2): ("DaF", "Caro-SGa-EFr"), (4, 5): ("pred", "Raf"),
        (4, 6): ("mat", "BrSa"),
        (5, 2): ("ing", "APa-PaH-Velo"), (5, 4): ("DaF", "Caro-SGa-EFr"),
        (5, 5): ("GL", "Caro-EFr-Eth"), (5, 6): ("geo", "Mar"), (5, 7): ("pred", "Raf"),
    },
    "10C1": {
        (1, 1): ("mat", "FBri"), (1, 2): ("DaF", "Eth-EFr-Swa"), (1, 3): ("pred", "BPad"),
        (1, 4): ("fis", "VSi"), (1, 5): ("ing", "APa"), (1, 7): ("bio", "Lza"),
        (2, 1): ("DaF", "Eth-EFr-Swa"), (2, 5): ("port", "MFo"), (2, 6): ("qui", "CAl"),
        (2, 7): ("bio", "Lza"), (2, 10): ("his", "ALu"), (2, 11): ("mat", "BrSa"),
        (3, 1): ("fil", "LAn"), (3, 2): ("DaF", "Eth-EFr-Swa"), (3, 3): ("GL", "EFr-Car-Swa"),
        (3, 4): ("ing", "APa"), (3, 5): ("soc", "Kle"), (3, 6): ("mat", "BrSa"),
        (3, 7): ("mat", "BrSa"),
        (4, 1): ("fis", "VSi"), (4, 2): ("ing", "APa"), (4, 3): ("ing", "APa"),
        (4, 4): ("geo", "Mlo"), (4, 5): ("DaF", "Eth-EFr-Swa"), (4, 6): ("his", "ALu"),
        (4, 10): ("pred", "BPad"), (4, 11): ("bio", "Lza"),
        (5, 1): ("GL", "EFr-Car-Swa"), (5, 2): ("geo", "Mlo"), (5, 3): ("DaF", "Eth-EFr-Swa"),
        (5, 4): ("port", "MFo"), (5, 5): ("qui", "CAl"), (5, 6): ("mat", "FBri"),
    },
    "10C2": {
        (1, 1): ("port", "MFo"), (1, 2): ("DaF", "Eth-EFr-Swa"), (1, 3): ("mat", "FBri"),
        (1, 4): ("qui", "CAl"), (1, 5): ("pred", "BPad"), (1, 6): ("bio", "Lza"),
        (1, 7): ("fis", "VSi"),
        (2, 1): ("DaF", "Eth-EFr-Swa"), (2, 5): ("ing", "Vir"), (2, 6): ("mat", "BrSa"),
        (2, 7): ("mat", "BrSa"), (2, 9): ("bio", "Lza"), (2, 10): ("bio", "Lza"),
        (2, 11): ("his", "ALu"),
        (3, 1): ("geo", "Mlo"), (3, 2): ("DaF", "Eth-EFr-Swa"), (3, 3): ("GL", "EFr-Car-Swa"),
        (3, 4): ("ing", "Vir"), (3, 5): ("ing", "Vir"), (3, 6): ("mat", "FBri"),
        (3, 7): ("fil", "LAn"),
        (4, 1): ("geo", "Mlo"), (4, 2): ("port", "MFo"), (4, 3): ("his", "ALu"),
        (4, 4): ("mat", "BrSa"), (4, 5): ("DaF", "Eth-EFr-Swa"), (4, 10): ("fis", "VSi"),
        (4, 11): ("port", "SMo"),
        (5, 1): ("GL", "EFr-Car-Swa"), (5, 2): ("ing", "Vir"), (5, 3): ("DaF", "Eth-EFr-Swa"),
        (5, 4): ("qui", "CAl"), (5, 5): ("soc", "Kle"), (5, 7): ("pred", "BPad"),
    },
    "11C1": {
        (1, 1): ("qui", "CAl"), (1, 2): ("mat", "ClaMe"), (1, 3): ("geo", "Mar"),
        (1, 4): ("pred", "ACo"), (1, 5): ("GL", "CBu-Swa-SGa"), (1, 6): ("DaF", "CBu-SGa-Swa"),
        (1, 7): ("ing", "Bea"),
        (2, 1): ("mat", "JJ"), (2, 2): ("his", "Ver"), (2, 3): ("his", "Ver"),
        (2, 4): ("DaF", "CBu-SGa-Swa"), (2, 8): ("qui", "CAl"), (2, 9): ("bio", "Ale"),
        (2, 10): ("pred", "ACo"), (2, 11): ("fis", "Cadu"),
        (3, 1): ("his", "Ver"), (3, 2): ("mat", "ClaMe"), (3, 4): ("GL", "CBu-Swa-SGa"),
        (3, 6): ("DaF", "CBu-SGa-Swa"), (3, 9): ("fil", "LAn"), (3, 10): ("bio", "Ale"),
        (3, 11): ("mat", "ClaMe"),
        (4, 1): ("fis", "Cadu"), (4, 2): ("fis", "Cadu"), (4, 3): ("mat", "JJ"),
        (4, 4): ("port", "AMu"), (4, 5): ("ing", "Bea"), (4, 6): ("ing", "Bea"),
        (4, 7): ("DaF", "CBu-SGa-Swa"), (4, 9): ("ing", "Bea"),
        (5, 2): ("soc", "Kle"), (5, 3): ("bio", "Ale"), (5, 4): ("geo", "Mar"),
        (5, 5): ("DaF", "CBu-SGa-Swa"), (5, 6): ("port", "Raf"), (5, 7): ("port", "AMu"),
    },
    "11C2": {
        (1, 1): ("pred", "ACo"), (1, 2): ("bio", "Ale"), (1, 3): ("mat", "ClaMe"),
        (1, 4): ("ing", "PaH"), (1, 5): ("GL", "CBu-Swa-SGa"), (1, 6): ("DaF", "CBu-SGa-Swa"),
        (1, 7): ("geo", "Mar"),
        (2, 1): ("qui", "CAl"), (2, 2): ("mat", "JJ"), (2, 3): ("qui", "CAl"),
        (2, 4): ("DaF", "CBu-SGa-Swa"), (2, 8): ("fis", "Cadu"), (2, 9): ("pred", "ACo"),
        (2, 10): ("his", "Ver"), (2, 11): ("his", "Ver"),
        (3, 1): ("geo", "Mar"), (3, 2): ("his", "Ver"), (3, 4): ("GL", "CBu-Swa-SGa"),
        (3, 6): ("DaF", "CBu-SGa-Swa"), (3, 9): ("fis", "Cadu"), (3, 10): ("mat", "ClaMe"),
        (3, 11): ("fil", "LAn"),
        (4, 1): ("mat", "JJ"), (4, 2): ("ing", "PaH"), (4, 3): ("bio", "Ale"),
        (4, 4): ("fis", "Cadu"), (4, 5): ("port", "AMu"), (4, 6): ("port", "AMu"),
        (4, 7): ("DaF", "CBu-SGa-Swa"), (4, 9): ("port", "Raf"),
        (5, 2): ("bio", "Ale"), (5, 3): ("mat", "ClaMe"), (5, 4): ("soc", "Kle"),
        (5, 5): ("DaF", "CBu-SGa-Swa"), (5, 6): ("ing", "PaH"), (5, 7): ("ing", "PaH"),
    },
    "12C1": {
        (1, 1): ("ing", "PaH"), (1, 2): ("ing", "PaH"), (1, 3): ("bio", "Ale"),
        (1, 4): ("DaF", "CBu-EFr-Eth"), (1, 5): ("geo", "Mar"), (1, 6): ("geo", "Mar"),
        (1, 7): ("qui", "CAl"),
        (2, 1): ("mat", "Bre"), (2, 2): ("bio", "Ale"), (2, 3): ("fis", "Cadu"),
        (2, 6): ("GL", "CBu-EFr-Eth"), (2, 8): ("his", "Wag"), (2, 11): ("port", "Deb"),
        (3, 1): ("bio", "Ale"), (3, 2): ("soc", "Kle"), (3, 3): ("mat", "Bre"),
        (3, 4): ("fis", "Cadu"), (3, 5): ("DaF", "CBu-EFr-Eth"), (3, 6): ("qui", "Fab"),
        (3, 10): ("fil", "LAn"), (3, 11): ("his", "Wag"),
        (4, 3): ("pred", "AMu"), (4, 4): ("ing", "PaH"), (4, 5): ("port", "Deb"),
        (4, 6): ("mat", "JJ"), (4, 7): ("mat", "JJ"), (4, 9): ("GL", "CBu-EFr-Eth"),
        (4, 11): ("port", "Deb"),
        (5, 1): ("port", "Deb"), (5, 2): ("geo", "Mar"), (5, 3): ("qui", "Fab"),
        (5, 4): ("his", "Wag"), (5, 5): ("pred", "AMu"), (5, 6): ("DaF", "CBu-EFr-Eth"),
        (5, 7): ("DaF", "CBu-EFr-Eth"),
    },
    "12C2": {
        (1, 1): ("geo", "Mar"), (1, 2): ("qui", "CAl"), (1, 3): ("mat", "Bre"),
        (1, 4): ("DaF", "CBu-EFr-Eth"), (1, 5): ("ing", "Isb"), (1, 6): ("ing", "Isb"),
        (1, 7): ("bio", "Ale"),
        (2, 1): ("fis", "Cadu"), (2, 2): ("port", "Deb"), (2, 3): ("bio", "Ale"),
        (2, 6): ("GL", "CBu-EFr-Eth"), (2, 7): ("mat", "Bre"), (2, 11): ("his", "Wag"),
        (3, 1): ("qui", "Fab"), (3, 2): ("his", "Wag"), (3, 3): ("pred", "AMu"),
        (3, 4): ("fil", "LAn"), (3, 5): ("DaF", "CBu-EFr-Eth"), (3, 6): ("soc", "Kle"),
        (3, 10): ("port", "Deb"), (3, 11): ("geo", "Mar"),
        (4, 3): ("fis", "Cadu"), (4, 4): ("mat", "JJ"), (4, 5): ("mat", "JJ"),
        (4, 6): ("bio", "Ale"), (4, 7): ("port", "Deb"), (4, 9): ("GL", "CBu-EFr-Eth"),
        (4, 11): ("ing", "Isb"),
        (5, 1): ("his", "Wag"), (5, 2): ("port", "Deb"), (5, 3): ("geo", "Mar"),
        (5, 4): ("pred", "AMu"), (5, 5): ("qui", "Fab"), (5, 6): ("DaF", "CBu-EFr-Eth"),
        (5, 7): ("DaF", "CBu-EFr-Eth"),
    },
}

# nome legivel da disciplina
NOME = {
    "mat": "Mat", "DaF": "DaF", "GL": "GL", "port": "Port", "plit": "Port",
    "gram": "Gram", "ing": "Ing", "pred": "Redação", "his": "Hist", "geo": "Geo",
    "bio": "Bio", "fis": "Fis", "qui": "Qui", "fil": "Fil", "soc": "Soc",
    "LPLITRED": "LP/LIT/RED",
    "esp": "Ed.Física", "art": "Artes", "tec": "Tec", "finan": "Finanças",
    "socem": "Socioem.", "apoio": "Apoio", "proj": "Projeto", "apr": "Aprof.",
    "elet": "Eletiva", "prve": "Proj.Vestibular",
}

# Turmas 10, 11 e 12: Portugues + Redacao + Gramatica sao UMA prova de
# 3 tempos seguidos, no mesmo dia, com os tres professores.
# Turmas 9: Portugues (2 tempos) e Redacao (2 tempos) sao provas separadas.
COMBINA_PORT = {"port", "pred", "gram"}

# Grupo 1 = Matematica, Alemao (DaF), Portugues e Ingles.
# GL nao entra: e disciplina propria, com prova, mas fora do grupo 1.
GRUPO1 = {"mat", "DaF", "port", "LPLITRED", "ing"}

# Evitar ao maximo provas nos tempos 7 a 11 (o 7o tempo comeca 12h45).
# Nao e proibicao: algumas disciplinas so tem aula nesses horarios.
PRIMEIRO_TEMPO_TARDE = 7         # nao podem coincidir na mesma semana
DOIS_TEMPOS = {"mat", "DaF", "GL", "port", "ing", "pred", "his", "geo", "bio", "fis", "qui"}
UM_TEMPO = {"fil", "soc"}                       # 1 tempo, 1 prova no semestre
NOVE_UM_TEMPO = {"bio", "fis", "qui"}           # nas turmas 9C: 1 tempo, 1 prova no semestre

# ---------------------------------------------------- CALENDARIO / BLOQUEIOS
# semanas: 3..6 = periodo 1 ; 7..16 = periodo 2
P1_SEMANAS = [3, 4, 5, 6]
P2_SEMANAS_10_12 = [7, 8, 9, 10, 12, 13, 14, 15]   # ate 12/11 (quinta da sem 15)
P2_SEMANAS_9_11 = [7, 8, 9, 10, 12, 13, 14, 15, 16]  # ate 21/11 (sem 16, sem sexta 20/11)

BLOQUEIOS = {
    (6, 1),    # 07/09 seg - Independencia
    (14, 1),   # 02/11 seg - Finados
    (16, 5),   # 20/11 sex - Consciencia Negra
    # 12/10 (N. Sra. Aparecida) cai na semana 11, ja vetada por inteiro
}
SEMANA_BLOQUEADA = {11}   # 12/10 a 16/10

LIMITE_DIA = {           # ultima (semana, dia) permitida por grupo de turma
    "10_12": (15, 4),    # 12/11 = quinta da semana 15
    "9_11": (16, 4),     # 20/11 e feriado -> ultimo dia util e quinta 19/11
}

# celulas ja preenchidas no modelo (2CH, CC, unterrichtsfrei...) por turma.
# Preenchido em tempo de execucao por carregar_ocupadas().
OCUPADAS = {}


def carregar_ocupadas():
    """Le do modelo quais (semana, dia) ja tem conteudo, por turma.

    O modelo so traz a aba 10C2 pronta; as demais sao copiadas dela. As
    marcacoes "2CH 10,12" / "CC 9,11" valem so para as series citadas, entao
    sao filtradas por turma.
    """
    wb = openpyxl.load_workbook(SRC, data_only=True)
    ws = wb["10C2"]
    base = {}
    for w in range(1, 21):
        r = week_row(w)
        for d, c in COL.items():
            v = ws[f"{c}{r}"].value
            if v and str(v).strip():
                base[(w, d)] = str(v).strip()
    for turma in GRADE_TXT:
        serie = "9" if turma.startswith("9") else turma[:2]
        ocup = set()
        for (w, d), txt in base.items():
            t = txt.replace("\n", " ")
            if t.startswith(("AG9", "AG10", "S1-", "S2-", "S3-", "S4-", "EX")):
                continue                      # simulados: tratados a parte
            if t.startswith(("2CH", "CC")):
                series = [s.strip() for s in t.split(None, 1)[-1].split(",")]
                if serie not in series:
                    continue                  # marcacao de outra serie
            if "Fach |" in t or "Matéria |" in t or "Raumwunsch" in t \
               or "U-Stunden" in t or "Solicitação" in t or "Horário" in t:
                continue                      # legenda do modelo
            ocup.add((w, d))
        OCUPADAS[turma] = ocup


SIMULADOS = {
    "9C1": [(9, 5, "AG9", "2º ao 7º tempos")],
    "9C2": [(9, 5, "AG9", "2º ao 7º tempos")],
    "10C1": [(6, 5, "AG10", "2º ao 7º tempos")],
    "10C2": [(6, 5, "AG10", "2º ao 7º tempos")],
    "11C1": [(4, 2, "S3-11", "2º ao 7º tempos"), (4, 3, "S3-11", "2º ao 7º tempos"),
             (13, 1, "S4-11", "2º ao 7º tempos"), (13, 2, "S4-11", "2º ao 7º tempos")],
    "11C2": [(4, 2, "S3-11", "2º ao 7º tempos"), (4, 3, "S3-11", "2º ao 7º tempos"),
             (13, 1, "S4-11", "2º ao 7º tempos"), (13, 2, "S4-11", "2º ao 7º tempos")],
    "12C1": [(7, 3, "S4-12", "2º ao 7º tempos"), (7, 4, "S4-12", "2º ao 7º tempos")],
    "12C2": [(7, 3, "S4-12", "2º ao 7º tempos"), (7, 4, "S4-12", "2º ao 7º tempos")],
}


def grupo_turma(t):
    return "9_11" if t.startswith(("9", "11")) else "10_12"


def semanas_p2(t):
    return P2_SEMANAS_9_11 if grupo_turma(t) == "9_11" else P2_SEMANAS_10_12


def dia_permitido(turma, w, d):
    if w in SEMANA_BLOQUEADA:
        return False
    if (w, d) in BLOQUEIOS:
        return False
    lw, ld = LIMITE_DIA[grupo_turma(turma)]
    if w > lw or (w == lw and d > ld):
        return False
    return True


# ---------------------------------------------------------------- EXAMES
def montar_exames(turma):
    """Retorna lista de exames: (disc, prof, n_tempos, periodo|None)."""
    grade = GRADES[turma]
    discs = {}
    for (d, t), (disc, prof) in grade.items():
        discs.setdefault(disc, set()).add(prof)

    combina = not turma.startswith("9")
    e = []
    if combina:
        profs = sorted({p for d in COMBINA_PORT for p in discs.get(d, ())
                        if p != "-"})
        if profs:
            nome = "/".join(profs)
            e.append(("LPLITRED", nome, 3, 1))
            e.append(("LPLITRED", nome, 3, 2))

    for disc, profs in sorted(discs.items()):
        if disc in SEM_PROVA:
            continue
        if combina and disc in COMBINA_PORT:
            continue                                       # ja entrou combinada
        prof = "/".join(sorted(p for p in profs if p != "-"))
        if disc in UM_TEMPO:
            e.append((disc, prof, 1, None))                # 1 prova no semestre
        elif turma.startswith("9") and disc in NOVE_UM_TEMPO:
            e.append((disc, prof, 1, None))                # 9C: bio/fis/qui 1x, 1 tempo
        elif disc in DOIS_TEMPOS:
            e.append((disc, prof, 2, 1))
            e.append((disc, prof, 2, 2))
    return e


def nao_doadoras(turma):
    """Disciplinas que NAO podem ceder tempo para prova de outra.

    Regra da escola: quem tem um unico tempo de aula na semana (Filosofia,
    Sociologia e afins) nao pode perder esse tempo — seria a aula inteira
    da semana.
    """
    import collections as _c
    cont = _c.Counter(d for (d, _p) in GRADES[turma].values())
    return {d for d, c in cont.items() if c == 1} | UM_TEMPO


def _tarde(t, n):
    """True se a prova encostar nos tempos 7 a 11 (a partir das 12h45)."""
    return (t + n - 1) >= PRIMEIRO_TEMPO_TARDE


INTERVALOS = (3, 5)   # recreio depois do 3o tempo e depois do 5o tempo


def cruza_intervalo(t, n):
    """True se o bloco [t, t+n-1] atravessar o recreio (depois do 3o ou do
    5o tempo). Restricao de maior prioridade: so aceita como ultimo
    recurso (ver 'Regras de distribuicao das provas' na skill)."""
    fim = t + n - 1
    return any(t <= b and fim >= b + 1 for b in INTERVALOS)


def slots_da_disciplina(turma, disc, n_tempos):
    """(dia, tempo_inicial, doador) onde cabe a prova.

    Para provas de 2 tempos o par pode ser (t, t+1) ou (t-1, t): o tempo
    emprestado tanto pode vir depois quanto antes do tempo da disciplina.
    """
    grade = GRADES[turma]
    out = []

    veto = nao_doadoras(turma)

    if disc == "LPLITRED":
        # trio de tempos consecutivos; quanto mais tempos ja forem de
        # Portugues/Redacao/Gramatica, melhor (menos tempo emprestado)
        cand = []
        for (d, t) in sorted(grade):
            trio = [grade.get((d, t + k)) for k in range(3)]
            if any(x is None for x in trio):
                continue
            proprios = sum(1 for x in trio if x[0] in COMBINA_PORT)
            if proprios == 0:
                continue
            doadores = [x for x in trio if x[0] not in COMBINA_PORT]
            if any(x[0] in veto for x in doadores):
                continue                      # disciplina de 1 tempo nao doa
            cand.append((cruza_intervalo(t, 3), _tarde(t, 3), -proprios, d, t,
                         tuple(doadores)))
        cand.sort()
        return [(d, t, doad or None) for (_, _, _, d, t, doad) in cand]

    for (d, t), (dd, _) in sorted(grade.items()):
        if dd != disc:
            continue
        if n_tempos == 1:
            out.append((d, t, None))
            continue
        prox = grade.get((d, t + 1))
        if prox is not None and (prox[0] == disc or prox[0] not in veto):
            out.append((d, t, None if prox[0] == disc else prox))
        ant = grade.get((d, t - 1))
        if ant is not None and ant[0] != disc and ant[0] not in veto:
            out.append((d, t - 1, ant))
    # remove duplicatas e poe os horarios sem cruzar intervalo e da manha
    # na frente
    vistos, unicos = set(), []
    for s in sorted(out, key=lambda s: (cruza_intervalo(s[1], n_tempos),
                                        _tarde(s[1], n_tempos), s[0], s[1])):
        k = (s[0], s[1])
        if k not in vistos:
            vistos.add(k)
            unicos.append(s)
    return unicos


MAX_NOS = 60000

# Provas com dia/tempo forcados por exigencia externa (turma, disc, periodo)
# -> (semana, dia). Ex.: 1a prova de Ingles da 10C2 tem que cair em
# 01/09/2026 (terca, semana 5) -- pedido da coordenacao.
FORCAR_DATA = {
    ("10C2", "ing", 1): (5, 2),
}


def par_g1_permitido(atuais, disc):
    """Excecao confirmada pela escola: duas provas do grupo 1 na mesma
    semana so sao aceitaveis quando uma delas for Ingles."""
    g1 = [a for a in atuais if eh_grupo1(a)] + [disc]
    return any(x == "ing" or x == "__forcado_ing__" for x in g1)


def eh_grupo1(nome):
    """True para disciplina do grupo 1 ou para o marcador de reserva de uma
    prova do grupo 1 com data forcada (ver FORCAR_DATA)."""
    if nome in GRUPO1:
        return True
    if nome.startswith("__forcado_") and nome.endswith("__"):
        return nome[len("__forcado_"):-2] in GRUPO1
    return False


def doador_discs(doador):
    """Nomes de disciplina dos tempos doados (0, 1 ou varios)."""
    if not doador:
        return set()
    if isinstance(doador[0], tuple):
        return {dd for (dd, _dp) in doador}
    return {doador[0]}


def _tentar(turma, seed, max_g1, max_tarde, max_intervalo,
            preocupado_dia=None, pre_por_semana=None, excluir=None):
    """Backtracking sob tres folgas controladas, da de maior para a de
    menor prioridade (quem chama itera max_intervalo por fora de
    max_tarde, que fica por fora de max_g1):

    max_intervalo : quantas provas podem cruzar o intervalo do recreio
                    (3o/4o ou 5o/6o tempos) -- maior prioridade de todas
    max_g1        : quantas disciplinas do grupo 1 podem cair na mesma semana
    max_tarde     : quantas provas da turma podem usar os tempos 7 a 11
    preocupado_dia, pre_por_semana : (w,d) e disciplinas ja comprometidas
        por provas conjuntas com a turma irma (ver resolver_par) -- contam
        para os limites desta turma mas nao sao realocadas aqui.
    excluir : nomes de disciplina ja resolvidos por resolver_par (nao
        entram nesta busca, so contam via preocupado_dia/pre_por_semana).
    """
    rnd = random.Random(seed)
    exames = [e for e in montar_exames(turma) if e[0] not in (excluir or ())]
    rnd.shuffle(exames)
    exames.sort(key=lambda e: len(slots_da_disciplina(turma, e[0], e[2])))

    ocupado_dia = set(preocupado_dia or ())        # (w, d)
    por_semana = {w: list(v) for w, v in (pre_por_semana or {}).items()}
    for (w, d, cod, _lab) in SIMULADOS[turma]:
        ocupado_dia.add((w, d))
        atuais = por_semana.setdefault(w, [])
        if cod not in atuais:
            atuais.append(cod)
    # dias reservados so para segurar o lugar de uma prova com data forcada
    # (ver resolver_par) -- aqui e onde essa prova de fato vai ser alocada,
    # entao o dia precisa ficar livre para ela.
    for (turma2, _disc2, _per2), (w, d) in FORCAR_DATA.items():
        if turma2 == turma:
            ocupado_dia.discard((w, d))

    resultado = []
    nos = [0]
    tarde = [0]
    intervalo_cnt = [0]

    def cabe(w, d, disc, marcador=None):
        if not dia_permitido(turma, w, d):
            return False
        if (w, d) in OCUPADAS.get(turma, ()):
            return False
        if (w, d) in ocupado_dia:
            return False
        atuais = por_semana.get(w, [])
        # o marcador de reserva (ver FORCAR_DATA) representa esta mesma
        # prova -- nao conta como uma avaliacao extra na semana
        n_atuais = len(atuais) - (1 if marcador and marcador in atuais else 0)
        if n_atuais >= 3:
            return False
        if disc in atuais:
            return False
        if disc in GRUPO1:
            if sum(1 for a in atuais if eh_grupo1(a)) >= max_g1:
                return False
            if sum(1 for a in atuais if eh_grupo1(a)) >= 1 and \
               not par_g1_permitido(atuais, disc):
                return False
        return True

    SLOTS = {}
    for (disc, prof, n, per) in exames:
        SLOTS[(disc, n)] = slots_da_disciplina(turma, disc, n)

    def semanas_do(per):
        if per == 1:
            return P1_SEMANAS
        if per == 2:
            return semanas_p2(turma)
        # exame unico no semestre: prefere o periodo 2, que tem mais folga
        return list(semanas_p2(turma)) + list(P1_SEMANAS)

    def opcoes(ex):
        disc, prof, n, per = ex
        forc = FORCAR_DATA.get((turma, disc, per))
        marcador = f"__forcado_{disc}__" if forc else None
        out = []
        semanas = [forc[0]] if forc else semanas_do(per)
        for w in semanas:
            for (d, t, doador) in SLOTS[(disc, n)]:
                if forc and d != forc[1]:
                    continue
                if cruza_intervalo(t, n) and intervalo_cnt[0] >= max_intervalo:
                    continue
                if _tarde(t, n) and tarde[0] >= max_tarde:
                    continue
                if cabe(w, d, disc, marcador):
                    out.append((w, d, t, doador))
        return out

    def donor_hist():
        hist = {}
        for (_w, _d, _t, _n, dc, _p, doad) in resultado:
            hist.setdefault(dc, set()).update(doador_discs(doad))
        return hist

    def bt(restantes):
        nos[0] += 1
        if nos[0] > MAX_NOS:
            raise TimeoutError
        if not restantes:
            return True
        # MRV: resolve primeiro o exame com menos opcoes
        melhor, melhor_ops = None, None
        for ex in restantes:
            ops = opcoes(ex)
            if not ops:
                return False
            if melhor_ops is None or len(ops) < len(melhor_ops):
                melhor, melhor_ops = ex, ops
                if len(ops) == 1:
                    break
        disc, prof, n, per = melhor
        rnd.shuffle(melhor_ops)
        # Ordem de preferencia (da maior para a menor prioridade):
        # 1) nunca cruzar o intervalo do recreio
        # 2) evitar os tempos 7-11
        # 3) espalhar (semanas menos cheias)
        # 4) alternar de qual lado vem o tempo emprestado, quando a mesma
        #    disciplina ja tomou tempo do mesmo doador numa prova anterior
        #    do semestre (desempate, nunca piora os criterios acima)
        # 5) slot melhor ranqueado em SLOTS (LP/LIT/RED = menos tempo
        #    emprestado)
        hist = donor_hist().get(disc, set())
        ordem = {(d, t): i for i, (d, t, _) in enumerate(SLOTS[(disc, n)])}
        melhor_ops.sort(key=lambda o: (
            cruza_intervalo(o[2], n),
            _tarde(o[2], n),
            len(por_semana.get(o[0], [])),
            1 if doador_discs(o[3]) & hist else 0,
            ordem.get((o[1], o[2]), 99),
        ))
        resto = [e for e in restantes if e is not melhor]
        for (w, d, t, doador) in melhor_ops:
            cruza = cruza_intervalo(t, n)
            if cruza and intervalo_cnt[0] >= max_intervalo:
                continue
            eh_tarde = _tarde(t, n)
            if eh_tarde and tarde[0] >= max_tarde:
                continue
            if cruza:
                intervalo_cnt[0] += 1
            if eh_tarde:
                tarde[0] += 1
            ocupado_dia.add((w, d))
            marcador = f"__forcado_{disc}__" if FORCAR_DATA.get((turma, disc, per)) else None
            semana_atual = por_semana.setdefault(w, [])
            tinha_marcador = marcador is not None and marcador in semana_atual
            if tinha_marcador:
                semana_atual.remove(marcador)
            semana_atual.append(disc)
            resultado.append((w, d, t, n, disc, prof, doador))
            if bt(resto):
                return True
            resultado.pop()
            por_semana[w].remove(disc)
            if tinha_marcador:
                por_semana[w].append(marcador)
            ocupado_dia.discard((w, d))
            if eh_tarde:
                tarde[0] -= 1
            if cruza:
                intervalo_cnt[0] -= 1
        return False

    try:
        return bt(list(exames)), resultado
    except TimeoutError:
        return False, []


def resolver(turma, seed, preocupado_dia=None, pre_por_semana=None, excluir=None):
    """Procura a melhor solucao, afrouxando as folgas na ordem de
    prioridade: primeiro tenta nunca cruzar o intervalo do recreio; so
    depois de esgotar isso passa a tentar reduzir provas nos tempos 7-11;
    e so por ultimo aceita sobreposicao do grupo 1."""
    n_exames = len([e for e in montar_exames(turma) if e[0] not in (excluir or ())])
    for max_intervalo in range(0, n_exames + 1):
        for max_tarde in range(0, n_exames + 1):
            for max_g1 in (1, 2, 3):
                ok, res = _tentar(turma, seed + 17 * max_tarde + 131 * max_intervalo,
                                  max_g1, max_tarde, max_intervalo,
                                  preocupado_dia, pre_por_semana, excluir)
                if ok:
                    usadas = sum(1 for (_w, _d, t, n, *_r) in res if _tarde(t, n))
                    cruzadas = sum(1 for (_w, _d, t, n, *_r) in res
                                   if cruza_intervalo(t, n))
                    return ok, res, max_g1, usadas, cruzadas
    return False, [], 3, 0, 0


# ------------------------------------------------- PROVAS ENTRE TURMAS IRMAS
# Quando a mesma pessoa leciona uma disciplina nas duas turmas de uma serie
# (ex.: 10C1/10C2), a prova tem que ser aplicada simultaneamente -- o
# professor nao pode estar em dois lugares ao mesmo tempo. Isso vale mesmo
# quando a disciplina ja e "grupo paralelo" que abrange as duas turmas
# (Alemao/DaF, GL, Ingles em algumas series): mesmo la, a SEMANA da prova
# ainda e uma escolha unica que tem que ser igual nas duas abas. Ver a
# regra "Disciplina com professor comum entre turmas irmas" na skill.
PARES_IRMAS = [("9C1", "9C2"), ("10C1", "10C2"), ("11C1", "11C2"), ("12C1", "12C2")]


def _discs_de(disc):
    return COMBINA_PORT if disc == "LPLITRED" else {disc}


def profs_do_disc(turma, disc):
    alvo = _discs_de(disc)
    return {p for (dd, p) in GRADES[turma].values() if dd in alvo}


def posicoes_do_disc(turma, disc):
    alvo = _discs_de(disc)
    return {(d, t) for (d, t), (dd, _p) in GRADES[turma].items() if dd in alvo}


def classificar_par(a, b):
    """disc -> ('combinada'|'coordenar', profs) para as disciplinas com
    professor comum entre as turmas irmas a/b. 'combinada': mesmo
    dia/tempo hoje na grade (ja e grupo paralelo entre as duas turmas,
    so falta escolher a semana). 'coordenar': mesmo professor, tempos
    diferentes em cada turma (precisa achar um dia/tempo em comum)."""
    exa = {d: p for (d, p, _n, _per) in montar_exames(a)}
    exb = {d: p for (d, p, _n, _per) in montar_exames(b)}
    out = {}
    for disc in sorted(set(exa) & set(exb)):
        if exa[disc] != exb[disc]:
            continue                       # professores diferentes -> independente
        pa, pb = posicoes_do_disc(a, disc), posicoes_do_disc(b, disc)
        tipo = "combinada" if pa == pb else "coordenar"
        out[disc] = (tipo, exa[disc])
    return out


def bloco(turma, e_propria, d, t, n, veto):
    """Tempos [t, t+n-1] do dia d na turma: lista de n itens, cada um None
    (tempo proprio da disciplina) ou (disc, prof) de quem doa aquele
    tempo. None (o retorno inteiro) se algum tempo nao existir na grade
    (dia sem aula ou almoco) ou for de disciplina que nao pode doar."""
    out = []
    for k in range(n):
        cell = GRADES[turma].get((d, t + k))
        if cell is None:
            return None
        dd, dp = cell
        if e_propria(dd):
            out.append(None)
        else:
            if dd in veto:
                return None
            out.append((dd, dp))
    return out


def doador_de_bloco(bl):
    doados = [x for x in bl if x is not None]
    if not doados:
        return None
    if len(doados) == 1:
        return doados[0]
    return tuple(doados)


def _tentar_par(a, b, seed, max_g1, max_tarde, max_intervalo):
    """Como _tentar(), mas decide de uma vez as provas de professor comum
    entre as turmas irmas a/b, no mesmo dia e tempo nas duas."""
    comuns = classificar_par(a, b)
    exames = []
    for (d, p, n, per) in montar_exames(a):
        if d in comuns:
            exames.append((d, p, n, per))
    if not exames:
        return True, [], [], set(), {}, set(), {}

    rnd = random.Random(seed)
    rnd.shuffle(exames)

    veto_a, veto_b = nao_doadoras(a), nao_doadoras(b)

    ocupado_a, ocupado_b = set(), set()
    por_semana_a, por_semana_b = {}, {}
    for (turma, ocup, psem) in ((a, ocupado_a, por_semana_a), (b, ocupado_b, por_semana_b)):
        for (w, d, cod, _lab) in SIMULADOS[turma]:
            ocup.add((w, d))
            atuais = psem.setdefault(w, [])
            if cod not in atuais:
                atuais.append(cod)
        # reserva os dias de provas com data forcada (ex.: Ingles 10C2 em
        # 01/09) para que as provas conjuntas desta secao nao os ocupem.
        # Usa um marcador (nao o nome real da disciplina) para nao colidir
        # com a checagem "disciplina ja nessa semana" quando a prova real
        # for alocada depois, no resolver() da propria turma.
        for (turma2, disc2, _per2), (w, d) in FORCAR_DATA.items():
            if turma2 != turma:
                continue
            ocup.add((w, d))
            marcador = f"__forcado_{disc2}__"
            atuais = psem.setdefault(w, [])
            if marcador not in atuais:
                atuais.append(marcador)

    resultado_a, resultado_b = [], []
    nos = [0]
    tarde = [0]
    intervalo_cnt = [0]

    def cabe(turma, ocup, psem, w, d, disc):
        if not dia_permitido(turma, w, d):
            return False
        if (w, d) in OCUPADAS.get(turma, ()):
            return False
        if (w, d) in ocup:
            return False
        atuais = psem.get(w, [])
        if len(atuais) >= 3:
            return False
        if disc in atuais:
            return False
        if disc in GRUPO1:
            if sum(1 for x in atuais if eh_grupo1(x)) >= max_g1:
                return False
            if sum(1 for x in atuais if eh_grupo1(x)) >= 1 and \
               not par_g1_permitido(atuais, disc):
                return False
        return True

    def semanas_do(per):
        if per == 1:
            return P1_SEMANAS
        if per == 2:
            return semanas_p2(a)           # a e b sao do mesmo grupo de turma
        return list(semanas_p2(a)) + list(P1_SEMANAS)

    def opcoes(ex):
        disc, prof, n, per = ex
        e_propria = (lambda dd: dd in COMBINA_PORT) if disc == "LPLITRED" \
            else (lambda dd: dd == disc)
        out = []
        for w in semanas_do(per):
            for d in range(1, 6):
                for t in range(1, 12):
                    if cruza_intervalo(t, n) and intervalo_cnt[0] >= max_intervalo:
                        continue
                    if _tarde(t, n) and tarde[0] >= max_tarde:
                        continue
                    bl_a = bloco(a, e_propria, d, t, n, veto_a)
                    if bl_a is None:
                        continue
                    bl_b = bloco(b, e_propria, d, t, n, veto_b)
                    if bl_b is None:
                        continue
                    if all(x is not None for x in bl_a) and all(x is not None for x in bl_b):
                        continue    # nenhuma das duas turmas tem tempo proprio ali
                    if not cabe(a, ocupado_a, por_semana_a, w, d, disc):
                        continue
                    if not cabe(b, ocupado_b, por_semana_b, w, d, disc):
                        continue
                    custo = sum(x is not None for x in bl_a) + sum(x is not None for x in bl_b)
                    out.append((w, d, t, bl_a, bl_b, custo))
        return out

    def bt(restantes):
        nos[0] += 1
        if nos[0] > MAX_NOS:
            raise TimeoutError
        if not restantes:
            return True
        melhor, melhor_ops = None, None
        for ex in restantes:
            ops = opcoes(ex)
            if not ops:
                return False
            if melhor_ops is None or len(ops) < len(melhor_ops):
                melhor, melhor_ops = ex, ops
                if len(ops) == 1:
                    break
        disc, prof, n, per = melhor
        rnd.shuffle(melhor_ops)
        melhor_ops.sort(key=lambda o: (
            cruza_intervalo(o[2], n),
            _tarde(o[2], n),
            len(por_semana_a.get(o[0], [])) + len(por_semana_b.get(o[0], [])),
            o[5],
        ))
        resto = [e for e in restantes if e is not melhor]
        for (w, d, t, bl_a, bl_b, _custo) in melhor_ops:
            cruza = cruza_intervalo(t, n)
            eh_tarde = _tarde(t, n)
            if cruza:
                intervalo_cnt[0] += 1
            if eh_tarde:
                tarde[0] += 1
            ocupado_a.add((w, d)); ocupado_b.add((w, d))
            por_semana_a.setdefault(w, []).append(disc)
            por_semana_b.setdefault(w, []).append(disc)
            resultado_a.append((w, d, t, n, disc, prof, doador_de_bloco(bl_a)))
            resultado_b.append((w, d, t, n, disc, prof, doador_de_bloco(bl_b)))
            if bt(resto):
                return True
            resultado_a.pop(); resultado_b.pop()
            por_semana_a[w].remove(disc); por_semana_b[w].remove(disc)
            ocupado_a.discard((w, d)); ocupado_b.discard((w, d))
            if eh_tarde:
                tarde[0] -= 1
            if cruza:
                intervalo_cnt[0] -= 1
        return False

    try:
        ok = bt(list(exames))
    except TimeoutError:
        ok = False
    return ok, resultado_a, resultado_b, ocupado_a, por_semana_a, ocupado_b, por_semana_b


def resolver_par(a, b, seed):
    """Resolve, na ordem de prioridade (intervalo > tarde > grupo1), todas
    as provas de professor comum entre as turmas irmas a/b, aplicadas
    simultaneamente. Retorna as alocacoes conjuntas mais o que cada turma
    ja tem ocupado, para o resolver() de cada turma completar o resto."""
    comuns = classificar_par(a, b)
    n_exames = len(comuns)
    for max_intervalo in range(0, n_exames + 1):
        for max_tarde in range(0, n_exames + 1):
            for max_g1 in (1, 2, 3):
                (ok, res_a, res_b, ocup_a, psem_a, ocup_b, psem_b) = _tentar_par(
                    a, b, seed + 17 * max_tarde + 131 * max_intervalo,
                    max_g1, max_tarde, max_intervalo)
                if ok:
                    return res_a, res_b, ocup_a, psem_a, ocup_b, psem_b, comuns
    print(f"  !! {a}/{b}: NAO foi possivel coordenar as provas de professor comum")
    return [], [], set(), {}, set(), {}, comuns


# ---------------------------------------------------------------- ESCRITA
def rotulo_tempo(t, n):
    if n == 1:
        return f"{t}º tempo"
    if n == 2:
        return f"{t}º e {t+1}º tempos"
    return f"{t}º ao {t+n-1}º tempos"


def escrever(proposta, alocacoes):
    dst = os.path.join(OUT, f"Proposta_{proposta}_Calendario_Provas_2026_2SEM.xlsx")
    shutil.copy(SRC, dst)
    wb = openpyxl.load_workbook(dst)

    base = wb["10C2"]
    for turma in GRADES:
        if turma == "10C2":
            continue
        idx = wb.sheetnames.index(turma)
        del wb[turma]
        nova = wb.copy_worksheet(base)
        nova.title = turma
        nova["A1"] = f"Prüfungsplan Klasse {turma} | Plano das Provas Turma {turma}"
        # o template e a aba 10C2: apaga o AG10 dela nas turmas de outra serie
        serie = "9" if turma.startswith("9") else turma[:2]
        for r in range(3, nova.max_row + 1):
            for c in "EFGHIJ":
                v = nova[f"{c}{r}"].value
                if not v:
                    continue
                t = str(v).strip().replace("\n", " ")
                if t.startswith(("AG9", "AG10", "S1-", "S2-", "S3-", "S4-", "EX")):
                    nova[f"{c}{r}"] = None            # simulado da outra serie
                elif t.startswith(("2CH", "CC")):
                    series = [x.strip() for x in t.split(None, 1)[-1].split(",")]
                    if serie not in series:
                        nova[f"{c}{r}"] = None
        wb.move_sheet(turma, offset=idx - wb.sheetnames.index(turma))

    for turma, itens in alocacoes.items():
        ws = wb[turma]
        for (w, d, t, n, disc, prof, doador) in itens:
            r = week_row(w)
            c = COL[d]
            cell = ws[f"{c}{r}"]
            if cell.value:      # nunca sobrescrever
                print(f"  !! {turma}: {disc} sem 'celula livre' em "
                      f"sem {w} {DIAS[d]} (ja ocupada)")
                continue
            cell.value = f"{NOME[disc]} - {prof}\n\n{rotulo_tempo(t, n)}"
            cell.alignment = Alignment(wrap_text=True, vertical="center",
                                       horizontal="center")
            if cruza_intervalo(t, n):
                cell.fill = DESTAQUE_INTERVALO
        for (w, d, cod, lab) in SIMULADOS[turma]:
            r = week_row(w)
            c = COL[d]
            cell = ws[f"{c}{r}"]
            atual = str(cell.value or "").strip()
            if atual and not atual.startswith(("AG9", "AG10", "S1-", "S2-",
                                               "S3-", "S4-", "EX")):
                continue                       # celula com outra informacao
            cell.value = f"{cod}\n\n{lab}"
            cell.alignment = Alignment(wrap_text=True, vertical="center",
                                       horizontal="center")
    wb.save(dst)
    return dst


def relatorio(alocacoes_por_proposta, comuns_por_par):
    irma = {a: b for a, b in PARES_IRMAS}
    irma.update({b: a for a, b in PARES_IRMAS})

    linhas = ["# Relatório de trocas de tempo entre professores",
              "",
              "Provas de tempos seguidos em que algum tempo pertence a outra",
              "disciplina. O professor doador precisa ceder o tempo naquele dia.",
              ""]

    linhas += ["## Provas coordenadas entre turmas irmãs", "",
               "Disciplinas com o mesmo professor nas duas turmas de uma série",
               "(ver regra na skill). \"Já combinada\" é grupo paralelo que já",
               "abrange as duas turmas hoje (Alemão/DaF, GL...); \"coordenada\"",
               "precisou de um dia/tempo em comum novo, porque o professor dá",
               "aula em horários diferentes em cada turma.", "",
               "| Turmas | Disciplina | Situação |",
               "|---|---|---|"]
    for (a, b), comuns in comuns_por_par.items():
        for disc, (tipo, _profs) in sorted(comuns.items()):
            situ = "Já combinada (grupo paralelo)" if tipo == "combinada" \
                else "Coordenada (professor comum, tempos diferentes)"
            linhas.append(f"| {a}/{b} | {NOME.get(disc, disc)} | {situ} |")
    linhas.append("")

    for prop, alocacoes in alocacoes_por_proposta.items():
        linhas += [f"## Proposta {prop}", "",
                   "| Turma | Disciplina/Prof. solicitante | Tempo necessário | "
                   "Prof. doador | Disciplina do tempo doado | Ação | Observação |",
                   "|---|---|---|---|---|---|---|"]
        for turma, itens in alocacoes.items():
            comuns = comuns_por_par.get(tuple(sorted((turma, irma.get(turma, turma)))), {})
            for (w, d, t, n, disc, prof, doador) in sorted(itens):
                obs = []
                if cruza_intervalo(t, n):
                    obs.append("⚠ Cruza o intervalo do recreio — nenhuma "
                                "outra combinação coube")
                if disc in comuns:
                    tipo, _ = comuns[disc]
                    if tipo == "coordenar":
                        obs.append(f"Prova conjunta com {irma[turma]} "
                                   "(professor comum, tempos coordenados)")
                    else:
                        obs.append(f"Grupo paralelo já combinado com {irma[turma]}")
                obs_txt = "; ".join(obs)
                if not doador:
                    if obs_txt:
                        linhas.append(f"| {turma} | {NOME[disc]} / {prof} | — | — | — | — | {obs_txt} |")
                    continue
                doadores = doador if isinstance(doador[0], tuple) else (doador,)
                for (dd, dp) in doadores:
                    tempos = [t + k for k in range(n)
                              if GRADES[turma].get((d, t + k), (None,))[0] == dd]
                    tl = ", ".join(f"{x}º" for x in tempos) or f"{t+1}º"
                    linhas.append(
                        f"| {turma} | {NOME[disc]} / {prof} | {tl} tempo(s) "
                        f"({DIAS[d]}, semana {w}) | {dp} | {NOME.get(dd, dd)} | "
                        f"Solicitar ao prof. {dp} a cessão do(s) tempo(s) {tl} de "
                        f"{NOME.get(dd, dd)} para a prova de {NOME[disc]} | {obs_txt} |")
        linhas.append("")
    p = os.path.join(OUT, "Relatorio_trocas_de_tempo.md")
    with open(p, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))
    return p


def main():
    os.makedirs(OUT, exist_ok=True)
    carregar_ocupadas()

    comuns_por_par = {(a, b): classificar_par(a, b) for a, b in PARES_IRMAS}

    todas = {}
    for prop, seed in [(1, 20260806), (2, 99887766)]:
        aloc = {}
        preocup_dia, pre_psem, excluir_por_turma = {}, {}, {}

        # 1) provas de professor comum entre turmas irmas, coordenadas ou
        #    ja combinadas -- decididas antes, para as duas turmas de vez.
        for (a, b) in PARES_IRMAS:
            res_a, res_b, ocup_a, psem_a, ocup_b, psem_b, comuns = resolver_par(
                a, b, seed + sum(map(ord, a + b)))
            aloc[a] = list(res_a)
            aloc[b] = list(res_b)
            preocup_dia[a], pre_psem[a] = ocup_a, psem_a
            preocup_dia[b], pre_psem[b] = ocup_b, psem_b
            excluir_por_turma[a] = set(comuns)
            excluir_por_turma[b] = set(comuns)
            if len(res_a) < len(comuns):
                print(f"  !! {a}/{b}: só {len(res_a)} de {len(comuns)} provas "
                      "comuns foram coordenadas")

        # 2) o resto de cada turma (disciplinas independentes, ex. Ingles
        #    nas turmas 10/11/12), preenchendo ao redor do que ja foi
        #    decidido acima.
        for turma in GRADES:
            ok, res, g1, tarde, cruzadas = resolver(
                turma, seed + sum(map(ord, turma)),
                preocupado_dia=preocup_dia.get(turma),
                pre_por_semana=pre_psem.get(turma),
                excluir=excluir_por_turma.get(turma))
            if not ok:
                print(f"  !! {turma}: NAO foi possivel alocar tudo")
            else:
                avisos = []
                if g1 > 1:
                    avisos.append(f"{g1} disciplinas do grupo 1 na mesma semana")
                if tarde:
                    tardias = ", ".join(
                        f"{NOME[dc]} ({rotulo_tempo(t, n)})"
                        for (_w, _d, t, n, dc, *_r) in sorted(res) if _tarde(t, n))
                    avisos.append(f"{tarde} prova(s) nos tempos 7-11: {tardias}")
                if cruzadas:
                    avisos.append(f"{cruzadas} prova(s) cruzando o intervalo do recreio")
                if avisos:
                    print(f"  ~  {turma}: " + "; ".join(avisos))
            aloc[turma].extend(res)
        caminho = escrever(prop, aloc)
        todas[prop] = aloc
        print(f"Proposta {prop} -> {caminho}")
    print("Relatorio ->", relatorio(todas, comuns_por_par))


if __name__ == "__main__":
    main()
