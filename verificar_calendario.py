#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere as planilhas geradas contra o checklist da skill calendario-provas.

Le os arquivos .xlsx ja gravados (nao confia na memoria do gerador).
"""
import openpyxl, os, re, collections, datetime
import gerar_calendario as G

OUT = G.OUT
COLS = {"E": 1, "F": 2, "G": 3, "H": 4, "I": 5}

LIMITE = {"10_12": datetime.date(2026, 11, 12),
          "9_11": datetime.date(2026, 11, 21)}
INICIO_P1 = datetime.date(2026, 8, 17)
FERIADOS = {datetime.date(2026, 9, 7), datetime.date(2026, 11, 20)}
SEMANA_VETADA = (datetime.date(2026, 10, 12), datetime.date(2026, 10, 16))

SIM_COD = re.compile(r"^(AG9|AG10|S\d-\d\d|EX\S+)")


SEMANA1 = datetime.date(2026, 8, 3)


def data_da(ws, w, d):
    """Semana 1 comeca em 03/08/2026 (as celulas de data sao formulas)."""
    return SEMANA1 + datetime.timedelta(days=7 * (w - 1) + d - 1)


def main():
    problemas = []
    for prop in (1, 2):
        caminho = os.path.join(OUT, f"Proposta_{prop}_Calendario_Provas_2026_2SEM.xlsx")
        wb = openpyxl.load_workbook(caminho, data_only=True)
        for turma in G.GRADES:
            ws = wb[turma]
            provas = []          # (data, w, d, disc, texto)
            for w in range(1, 21):
                r = G.week_row(w)
                for col, d in COLS.items():
                    v = ws[f"{col}{r}"].value
                    if not v:
                        continue
                    txt = str(v).strip()
                    if "unterrichtsfrei" in txt or "Fach |" in txt or \
                       "Matéria |" in txt or txt.startswith(("2CH", "CC")):
                        continue
                    disc = txt.split("\n")[0].split(" - ")[0].strip()
                    provas.append((data_da(ws, w, d), w, d, disc, txt))

            pre = f"P{prop}/{turma}"
            grupo = G.grupo_turma(turma)

            # 1. max 3 avaliacoes por semana (simulado de 2 dias conta 1x)
            por_sem = collections.defaultdict(set)
            for (dt, w, d, disc, _) in provas:
                cod = SIM_COD.match(disc)
                por_sem[w].add(cod.group(1) if cod else disc)
            for w, s in por_sem.items():
                if len(s) > 3:
                    problemas.append(f"{pre}: semana {w} com {len(s)} avaliações {sorted(s)}")

            # 2. grupo 1 nao coincide
            for w, s in por_sem.items():
                g1 = [x for x in s if x.lower() in
                      {"mat", "daf", "port", "lp/lit/red", "ing"}]
                if len(g1) > 1:
                    problemas.append(f"{pre}: semana {w} com grupo 1 repetido {g1}")

            # 3. um exame por dia
            dias = collections.Counter((w, d) for (_, w, d, _, _) in provas)
            for k, c in dias.items():
                if c > 1:
                    problemas.append(f"{pre}: {c} provas no mesmo dia {k}")

            # 4. datas: dentro do periodo, sem feriado, sem a semana vetada
            for (dt, w, d, disc, _) in provas:
                if dt < INICIO_P1:
                    problemas.append(f"{pre}: {disc} em {dt} antes de 17/08")
                if dt > LIMITE[grupo]:
                    problemas.append(f"{pre}: {disc} em {dt} depois do limite "
                                     f"{LIMITE[grupo]}")
                if dt in FERIADOS:
                    problemas.append(f"{pre}: {disc} em feriado {dt}")
                if SEMANA_VETADA[0] <= dt <= SEMANA_VETADA[1]:
                    problemas.append(f"{pre}: {disc} na semana vetada {dt}")

            # 5. numero de provas por disciplina
            cont = collections.Counter(
                disc for (_, _, _, disc, _) in provas if not SIM_COD.match(disc))
            for disc, c in cont.items():
                esperado = 1 if disc in ("Fil", "Soc") or \
                    (turma.startswith("9") and disc in ("Bio", "Fis", "Qui")) else 2
                if disc in ("Port", "Redação", "Gram") and not turma.startswith("9"):
                    problemas.append(f"{pre}: {disc} separado (deveria ser LP/LIT/RED)")
                if c != esperado:
                    problemas.append(f"{pre}: {disc} tem {c} provas (esperado {esperado})")

            # 5b. LP/LIT/RED usa 3 tempos nas turmas 10/11/12
            for (_, _, _, disc, txt) in provas:
                if disc == "LP/LIT/RED":
                    ult = txt.split("\n")[-1]
                    if "ao" not in ult:
                        problemas.append(f"{pre}: LP/LIT/RED sem 3 tempos ({ult})")

            # 5c. simulados do 2o ao 7o tempo
            for (_, _, _, disc, txt) in provas:
                if SIM_COD.match(disc) and "2º ao 7º" not in txt:
                    problemas.append(f"{pre}: simulado {disc} fora do 2o-7o tempo")

            # 6. disciplinas de 1 tempo usam 1 tempo
            for (_, _, _, disc, txt) in provas:
                um_tempo = disc in ("Fil", "Soc") or \
                    (turma.startswith("9") and disc in ("Bio", "Fis", "Qui"))
                if um_tempo and " e " in txt.split("\n")[-1]:
                    problemas.append(f"{pre}: {disc} com 2 tempos ({txt.split(chr(10))[-1]})")

            # 7. Ed. Fisica e afins nao tem prova
            for (_, _, _, disc, _) in provas:
                if disc.lower() in ("esp", "art", "tec", "finan", "socem", "proj"):
                    problemas.append(f"{pre}: prova indevida de {disc}")

            # 8. simulados nas datas oficiais
            oficiais = {(w, d) for (w, d, c, l) in G.SIMULADOS[turma]}
            achados = {(w, d) for (_, w, d, disc, _) in provas if SIM_COD.match(disc)}
            if oficiais != achados:
                problemas.append(f"{pre}: simulados {sorted(achados)} != "
                                 f"oficiais {sorted(oficiais)}")

    if problemas:
        print(f"{len(problemas)} PROBLEMA(S):")
        for p in problemas:
            print("  -", p)
    else:
        print("OK: as duas propostas passaram em todos os itens do checklist.")


if __name__ == "__main__":
    main()
