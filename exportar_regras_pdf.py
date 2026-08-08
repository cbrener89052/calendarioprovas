#!/usr/bin/env python3
"""Gera PDF com as regras de negócio do calendário de provas."""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).parent / "referencia" / "Regras_Negocio_Calendario_Provas.pdf"


class PDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, f"Calendário de Provas — Escola Alemã Corcovado  |  Página {self.page_no()}", align="C")


def section_title(pdf, text):
    pdf.ln(4)
    pdf.set_font("DejaVu", "B", 13)
    pdf.set_text_color(30, 60, 100)
    pdf.multi_cell(pdf.epw, 7, text)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)


def subsection(pdf, text):
    pdf.set_font("DejaVu", "B", 11)
    pdf.multi_cell(pdf.epw, 6, text)
    pdf.ln(1)


def body(pdf, text):
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(pdf.epw, 5.5, text)
    pdf.ln(1)


def bullet(pdf, text):
    pdf.set_font("DejaVu", "", 10)
    pdf.multi_cell(pdf.epw, 5.5, f"  •  {text}")
    pdf.ln(0.5)


def table_row(pdf, cols, widths, bold=False):
    pdf.set_font("DejaVu", "B" if bold else "", 9)
    h = 6
    for col, w in zip(cols, widths):
        pdf.cell(w, h, col, border=1)
    pdf.ln(h)


def build_pdf():
    pdf = PDF()
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    pdf.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    pdf.add_page()
    w = pdf.epw

    pdf.set_font("DejaVu", "B", 18)
    pdf.set_text_color(20, 50, 90)
    pdf.multi_cell(w, 10, "Regras de Negócio\nCalendário de Provas")
    pdf.set_font("DejaVu", "", 11)
    pdf.set_text_color(80, 80, 80)
    pdf.multi_cell(w, 6, "Escola Alemã Corcovado — 2º semestre 2026\nGerado a partir da skill calendario-provas")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(4)

    body(
        pdf,
        "Este documento descreve as regras para geração do calendário de provas. "
        "O sistema lê o horário-base semanal (grade Untis) e distribui as provas "
        "conforme as regras abaixo. O horário semanal em si não é gerado por este sistema.",
    )

    section_title(pdf, "1. Entradas obrigatórias")
    bullets = [
        "Períodos de prova por turma ou grupo (turmas que viajam terminam antes)",
        "Feriados e semanas vetadas",
        "Limite de horário do dia (preferência: evitar tempos 7 a 11)",
        "Datas e tempos dos simulados/AG por série",
        "Provas combinadas (ex.: LP/LIT/RED)",
        "Quantos tempos cada prova usa",
        "Exceções de prova única no semestre por série",
        "Disciplinas sem prova",
        "Grupos paralelos (Alemão/DaF etc.)",
        "Estrutura do arquivo-modelo de saída",
    ]
    for b in bullets:
        bullet(pdf, b)

    section_title(pdf, "2. Períodos e bloqueios (2º sem 2026)")
    subsection(pdf, "Períodos de prova")
    tw = [45, 55, pdf.epw - 100]
    table_row(pdf, ["Grupo", "P1", "P2"], tw, bold=True)
    table_row(pdf, ["Todas", "24/08 a 18/09/2026", "—"], tw)
    table_row(pdf, ["10C e 12C", "—", "14/09 a 12/11/2026"], tw)
    table_row(pdf, ["9C e 11C", "—", "14/09 a 26/11/2026"], tw)
    pdf.ln(3)
    subsection(pdf, "Bloqueios")
    bullet(pdf, "Feriados: 07/09, 02/11, 20/11")
    bullet(pdf, "Semana vetada: 12 a 16/10 (conselho de classe, sem aula)")
    bullet(pdf, "Simulados/AG: datas fixas, não podem ser movidos")

    section_title(pdf, "3. Regras de distribuição")
    subsection(pdf, "Limites gerais")
    bullet(pdf, "Máximo 3 avaliações por semana por turma (simulado de 2 dias = 1)")
    bullet(pdf, "Uma prova por dia por turma")
    bullet(pdf, "Distância mínima de 4 semanas entre as 2 provas da mesma disciplina/professor")
    bullet(pdf, "Não usar feriados, semana vetada, antes do início ou depois da data-limite")

    subsection(pdf, "Intervalo / recreio (prioridade máxima)")
    bullet(pdf, "Prova não pode cruzar o recreio: pares proibidos 3º+4º e 5º+6º tempos")
    bullet(pdf, "Só aceitar cruzamento se não houver alternativa → célula laranja + relatório")

    subsection(pdf, "Grupo 1")
    bullet(pdf, "Matemática, Alemão (DaF), Português/LP-LIT-RED, Inglês — não coincidem na mesma semana")
    bullet(pdf, "GL não pertence ao grupo 1")
    bullet(pdf, "Exceção: 2 do grupo 1 na mesma semana se uma for Inglês")
    bullet(pdf, "Nunca 3 do grupo 1; nunca par sem Inglês (ex.: Mat + LP/LIT/RED)")

    subsection(pdf, "LP/LIT/RED")
    bullet(pdf, "Turmas 10, 11, 12: prova única de 3 tempos, mesmo dia, 3 professores")
    bullet(pdf, "Deve cair na 1ª ou 2ª semana de cada rodada (P1 e P2)")
    bullet(pdf, "Turma 9: Português e Redação separadas, 2 tempos cada")

    subsection(pdf, "Horário do dia")
    bullet(pdf, "Evitar tempos 7 a 11 (a partir de 12h45) — preferência forte, não proibição")
    bullet(pdf, "Minimizar provas à tarde; listar as inevitáveis ao final")

    subsection(pdf, "Prova única no semestre (1 tempo)")
    bullet(pdf, "Filosofia e Sociologia (todas as séries)")
    bullet(pdf, "Biologia, Química e Física — só no 9º ano")
    bullet(pdf, "Demais séries: 1 prova por período (2 no semestre)")

    subsection(pdf, "Sem prova")
    body(
        pdf,
        "Educação Física, Artes/Música/Teatro, Técnicas, Finanças, Socioemocional, "
        "apoio/aprofundamento, eletivas, Projeto Vestibular.",
    )

    subsection(pdf, "Grupos paralelos")
    bullet(pdf, "1 prova só, aplicada simultaneamente; cada professor com seu grupo")
    bullet(pdf, "Conta como 1 avaliação da turma")

    subsection(pdf, "Turmas irmãs (mesmo professor)")
    bullet(pdf, "Aula já combinada (mesmo dia/tempo): trata como grupos paralelos")
    bullet(pdf, "Mesmo professor, tempos diferentes: priorizar prova simultânea nas duas turmas")
    bullet(pdf, "Professores diferentes: provas independentes")

    subsection(pdf, "Tempo de aplicação e empréstimo")
    bullet(pdf, "Preferir tempo(s) da própria disciplina")
    bullet(pdf, "Tempo extra vem de outra disciplina no mesmo dia, antes ou depois")
    bullet(pdf, "Disciplina com 1 aula/semana não pode ceder")
    bullet(pdf, "Alternar de qual lado vem o empréstimo entre provas duplas no semestre")

    section_title(pdf, "4. Limites de cessão (Proposta 3)")
    body(pdf, "Por (disciplina, professor, turma):")
    w2 = [15, pdf.epw - 15]
    rows = [
        ("1", "2–3 aulas/semana → máx. 2 cessões (3 para Hist, Geo, GL)"),
        ("2", "1 aula/semana → não cede"),
        ("3", "Não ficar 2 semanas seguidas sem contato com a turma"),
        ("4", "Não ceder na semana da própria prova nem na anterior"),
        ("5", "Máximo 11% das aulas programadas no semestre (alvo 10%)"),
    ]
    table_row(pdf, ["#", "Regra"], w2, bold=True)
    for n, r in rows:
        table_row(pdf, [n, r], w2)
    pdf.ln(3)
    body(
        pdf,
        "Ordem de afrouxamento se não fechar: regra 4 → regra 3 → tetos (+1). "
        "Regras 1, 2 e 5 nunca são relaxadas. Datas fixas da coordenação são inegociáveis.",
    )

    section_title(pdf, "5. Simulados (2º sem 2026)")
    w3 = [30, 55, pdf.epw - 85]
    table_row(pdf, ["Código", "Data(s)", "Turmas"], w3, bold=True)
    sims = [
        ("S3-11", "25 e 26/08/2026", "11C1, 11C2"),
        ("S4-12", "16 e 17/09/2026", "12C1, 12C2"),
        ("AG10", "25/09/2026", "10C1, 10C2"),
        ("AG9", "02/10/2026", "9C1, 9C2"),
        ("S4-11", "26 e 27/10/2026", "11C1, 11C2"),
    ]
    for row in sims:
        table_row(pdf, list(row), w3)
    pdf.ln(3)
    bullet(pdf, "Ocupam do 2º ao 7º tempo")
    bullet(pdf, "Cor amarela exclusiva na planilha")
    bullet(pdf, "Contam no limite de 3 avaliações/semana")

    section_title(pdf, "6. Formato de saída")
    body(pdf, "Cada prova ocupa 3 linhas na célula mesclada:")
    pdf.set_font("DejaVu", "", 9)
    pdf.multi_cell(pdf.epw, 5, "  Disciplina - Sigla(s) professor\n  [sala — em branco]\n  Tempo(s)")
    pdf.ln(2)
    bullet(pdf, "Cor fixa por disciplina (paleta pastel)")
    bullet(pdf, "Simulados: amarelo #FFFF00")
    bullet(pdf, "Cruzamento de intervalo: laranja #FFC000")
    bullet(pdf, '2ª chamada: vermelho, texto "2CH <séries>"')

    section_title(pdf, "7. Entregáveis")
    bullet(pdf, "Calendário xlsx (aba por turma)")
    bullet(pdf, "Relatório de trocas de tempo entre professores")
    bullet(pdf, "Tabela-resumo por turma")
    bullet(pdf, "Relatório de tempos cedidos (Proposta 3)")

    section_title(pdf, "Referências no repositório")
    bullet(pdf, ".claude/skills/calendario-provas/SKILL.md — regras completas")
    bullet(pdf, "gerar_calendario.py — implementação")
    bullet(pdf, "verificar_calendario.py — checklist automático")
    bullet(pdf, "referencia/estado_2sem_2026.md — dados desta rodada")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUT))
    print(f"PDF gerado: {OUT}")


if __name__ == "__main__":
    build_pdf()
