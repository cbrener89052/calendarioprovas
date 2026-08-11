#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera Horario desenvolvido/Relatorio_trocas_de_tempo.md a partir da
planilha FINAL da Proposta 3 (nao confia na memoria do gerador nem exige
rodar o solver de novo -- por isso e seguro de rodar a qualquer momento,
mesmo depois de edicoes manuais na Proposta 3, sem risco de sobrescrever
o calendario ja fechado).

Reusa a mesma funcao de escrita `gerar_calendario.relatorio()` que o
`main()` usa, só que alimentada com os itens (w, d, t, n, disc, prof,
doador) reconstruidos da planilha gravada, em vez das alocacoes do
backtracking.
"""
import openpyxl, re
import gerar_calendario as G

COLS = {"E": 1, "F": 2, "G": 3, "H": 4, "I": 5}
SIM_COD = re.compile(r"^(AG9|AG10|S\d-\d\d|EX\S+)")


def ler_itens(caminho, turma):
    wb = openpyxl.load_workbook(caminho, data_only=True)
    ws = wb[turma]
    itens = []
    for w in range(1, 21):
        r = G.week_row(w)
        for col, d in COLS.items():
            v = ws[f"{col}{r}"].value
            if not v:
                continue
            txt = str(v).strip()
            if ("unterrichtsfrei" in txt or "Fach |" in txt or "Matéria |" in txt
                    or txt.startswith(("2CH", "CC", "Raumwunsch", "U-Stunden"))):
                continue
            cabeca = txt.split("\n")[0]
            if SIM_COD.match(cabeca) or " - " not in cabeca:
                continue
            disc_nome, prof_txt = cabeca.split(" - ", 1)
            disc_nome, prof_txt = disc_nome.strip(), prof_txt.strip()
            ult = txt.split("\n")[-1]
            nums = [int(x) for x in re.findall(r"(\d+)º", ult)]
            if not nums:
                continue
            t_ini, n_t = min(nums), max(nums) - min(nums) + 1
            chave = [k for k, vv in G.NOME.items() if vv == disc_nome]
            if not chave:
                print(f"  [AVISO] {turma} sem{w} {G.DIAS[d]}: disciplina "
                      f"'{disc_nome}' não reconhecida, ignorada no relatório")
                continue
            disc_code = chave[0]
            doador = bool(G.posicoes_por_doador(turma, disc_code, d, t_ini, n_t))
            itens.append((w, d, t_ini, n_t, disc_code, prof_txt, doador))
    return itens


def main():
    G.carregar_ocupadas()
    caminho = f"{G.OUT}/Proposta_3_Calendario_Provas_2026_2SEM.xlsx"
    comuns_por_par = {(a, b): G.classificar_par(a, b) for a, b in G.PARES_IRMAS}
    alocacoes = {turma: ler_itens(caminho, turma) for turma in G.GRADES}
    p = G.relatorio({3: alocacoes}, comuns_por_par)
    print("Gerado:", p)


if __name__ == "__main__":
    main()
