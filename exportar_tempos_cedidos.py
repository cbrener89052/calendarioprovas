#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta o relatorio de tempos cedidos, por turma, a partir das propostas
ja geradas.

Para cada disciplina/professor da grade-base de cada turma, mostra quantas
aulas semanais ela tem e quantas dessas aulas foram cedidas, ao longo do
semestre, para a aplicacao de provas de OUTRAS disciplinas (tempo
emprestado).

Nao confia na memoria do gerador: rele as celulas de prova ja gravadas nas
planilhas e cruza, tempo a tempo, com a grade-base (GRADES) para descobrir
de quem era originalmente cada tempo usado por uma prova. Quando o tempo
nao e da propria disciplina examinada (nem, no caso de LP/LIT/RED, de uma
das tres disciplinas que compoem a prova combinada), conta como cedencia
do dono daquele tempo na grade.

Le  : Horario desenvolvido/Proposta_N_Calendario_Provas_2026_2SEM.xlsx
      siglas/siglas_profs_aux_etc.xlsx  (sigla -> nome do professor)
Grava: Horario desenvolvido/Relatorio_Tempos_Cedidos_Proposta_N.xlsx
       (uma aba por turma)
"""
import openpyxl, os, re, collections
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import gerar_calendario as G
from exportar_tabelas_turma import carregar_siglas, nomes_dos_profs

OUT = G.OUT
COLS = {"E": 1, "F": 2, "G": 3, "H": 4, "I": 5}
SIM_COD = re.compile(r"^(AG9|AG10|S\d-\d\d|EX\S+)")

# nome legivel -> codigo da grade (inverso de G.NOME; em caso de nomes
# repetidos - ex. "port"/"plit" -> "Port" -, fica o primeiro, que e o
# codigo realmente usado na grade)
REV_NOME = {}
for _cod, _nome in G.NOME.items():
    REV_NOME.setdefault(_nome, _cod)


def ler_exames(caminho, turma):
    """[(w, d, disc_nome, t_ini, n_tempos), ...] das celulas de prova.

    Simulados/AG ficam de fora: sao bloco fixo, nao passam pela logica de
    tempo emprestado.
    """
    wb = openpyxl.load_workbook(caminho, data_only=True)
    ws = wb[turma]
    exames = []
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
            partes = [p.strip() for p in txt.split("\n")]
            cabeca = partes[0]
            if SIM_COD.match(cabeca):
                continue
            disc = cabeca.split(" - ")[0].strip()
            ult = partes[-1] if len(partes) > 1 else ""
            nums = [int(x) for x in re.findall(r"(\d+)º", ult)]
            if not nums:
                continue
            t_ini = nums[0]
            n_t = (max(nums) - min(nums) + 1) if len(nums) >= 2 else 1
            exames.append((w, d, disc, t_ini, n_t))
    return exames


def cedencias_por_turma(caminho, turma):
    """{(codigo, prof): nº de aulas cedidas no semestre} da turma."""
    cont = collections.Counter()
    for (_w, d, disc, t_ini, n_t) in ler_exames(caminho, turma):
        if disc == "LP/LIT/RED":
            familia = G.COMBINA_PORT
        else:
            cod = REV_NOME.get(disc)
            if cod is None:
                print(f"  !! {turma}: disciplina não reconhecida '{disc}', "
                      "pulando na contagem de cedências")
                continue
            familia = {cod}
        for t in range(t_ini, t_ini + n_t):
            dono = G.GRADES[turma].get((d, t))
            if not dono:
                continue
            codigo, prof = dono
            if codigo in familia:
                continue          # tempo proprio da disciplina examinada
            cont[(codigo, prof)] += 1
    return cont


def exportar(proposta, siglas):
    origem = os.path.join(
        OUT, f"Proposta_{proposta}_Calendario_Provas_2026_2SEM.xlsx")
    destino = os.path.join(
        OUT, f"Relatorio_Tempos_Cedidos_Proposta_{proposta}.xlsx")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    cab_fill = PatternFill("solid", fgColor="1F3864")
    cab_font = Font(bold=True, color="FFFFFF", size=11)
    borda = Border(*[Side(style="thin", color="BFBFBF")] * 4)
    zebra = PatternFill("solid", fgColor="F2F2F2")
    total_fill = PatternFill("solid", fgColor="D9E1F2")

    for turma in G.GRADES:
        cedidas = cedencias_por_turma(origem, turma)
        semanais = collections.Counter(
            (codigo, prof) for (codigo, prof) in G.GRADES[turma].values())

        linhas = [(G.NOME.get(codigo, codigo), prof, n_sem,
                   cedidas.get((codigo, prof), 0))
                  for (codigo, prof), n_sem in semanais.items()]
        linhas.sort(key=lambda x: (-x[3], x[0], x[1]))

        ws = wb.create_sheet(turma)
        ws["A1"] = (f"Tempos Cedidos para Provas — {turma} — "
                    f"2º semestre 2026 (Proposta {proposta})")
        ws["A1"].font = Font(bold=True, size=13)
        ws.merge_cells("A1:D1")
        ws["A1"].alignment = Alignment(horizontal="center")

        cabecalhos = ["Disciplina", "Professor(es)", "Nº de aulas semanais",
                      "Nº de aulas cedidas para provas de outras disciplinas"]
        for c, t in enumerate(cabecalhos, 1):
            cel = ws.cell(2, c, t)
            cel.fill, cel.font = cab_fill, cab_font
            cel.alignment = Alignment(horizontal="center", vertical="center",
                                      wrap_text=True)
            cel.border = borda

        i = 3
        for (disc, prof, n_sem, n_ced) in linhas:
            prof_txt = "—" if prof == "-" else nomes_dos_profs(prof, siglas)
            ws.cell(i, 1, disc)
            ws.cell(i, 2, prof_txt)
            ws.cell(i, 3, n_sem).alignment = Alignment(horizontal="center")
            ws.cell(i, 4, n_ced).alignment = Alignment(horizontal="center")
            for c in range(1, 5):
                cel = ws.cell(i, c)
                cel.border = borda
                cel.alignment = Alignment(
                    vertical="center", wrap_text=(c == 2),
                    horizontal="center" if c in (3, 4) else "left")
                if i % 2:
                    cel.fill = zebra
            i += 1

        ws.cell(i, 1, "Total")
        ws.cell(i, 1).font = Font(bold=True)
        ws.cell(i, 4, sum(x[3] for x in linhas))
        for c in range(1, 5):
            cel = ws.cell(i, c)
            cel.border = borda
            cel.fill = total_fill
            cel.font = Font(bold=True)
            cel.alignment = Alignment(horizontal="center" if c in (3, 4) else "left")

        for col, larg in zip("ABCD", (16, 46, 16, 30)):
            ws.column_dimensions[col].width = larg
        ws.freeze_panes = "A3"
        ws.auto_filter.ref = f"A2:D{i}"

    wb.save(destino)
    return destino


def main():
    siglas = carregar_siglas()
    for p in (1, 2):
        print("Gerado:", exportar(p, siglas))


if __name__ == "__main__":
    main()
