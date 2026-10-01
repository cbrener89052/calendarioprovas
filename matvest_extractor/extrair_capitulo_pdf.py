#!/usr/bin/env python3
"""
Extrai questões de um capítulo do livro "Matemática para Vestibular" a
partir do PDF (mesmo padrão em todos os capítulos: teoria, exercícios em
blocos Nível-A/B/C, seção "Respostas" com os mesmos blocos de nível
contendo o gabarito, casado pela numeração).

Por que PDF e não .docx
-----------------------
No .docx, o Word grava símbolos matemáticos como caractere especial de
fonte (<w:sym>) e fórmulas maiores como objeto OLE do Equation Editor/
MathType (uma imagem .wmf, sem texto algum no XML). O PDF gerado pelo
Acrobat PDFMaker resolve os dois problemas de uma vez: os símbolos saem
com o Unicode correto e as fórmulas do Equation Editor saem como texto
de verdade (confirmado comparando os dois formatos do mesmo capítulo).
Por isso este script lê o PDF com `pdftotext`, não o .docx — é mais
simples e não depende de IA para reconstruir fórmula nenhuma.

Figuras/diagramas genuínos (aqueles que são mesmo uma imagem no livro,
ex: diagrama de Venn, tabuleiro, cartões) continuam sendo apenas imagem
mesmo no PDF. Esses casos são detectados por palavra-chave ("figura",
"diagrama", "esquema" etc.) e marcados em vez de processados por IA —
a ideia é só chamar atenção humana (ou IA, se você pedir depois) para
essas poucas questões, sem gastar IA nas outras que o script já resolve
sozinho.

USO
---
    python extrair_capitulo_pdf.py capitulo.pdf \\
        --livro "Matemática para Vestibular Vol 01" \\
        --capitulo "Lógica e Conjuntos" \\
        --output banco_matvest.db
"""

import argparse
import re
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

## O cabeçalho que marca um bloco de nível varia MUITO entre capítulos:
## "Nível-A", "NIVEL A", "NÍVEL - A", "GABARITO NÍVEL C", "GABARITO A", e em
## alguns capítulos ("Função") não existe nenhuma palavra "Respostas"/
## "Gabarito" separada — só os blocos "Nível X" aparecem duas vezes (a
## primeira é o enunciado, a segunda é o gabarito). Por isso a segmentação
## não depende de achar a palavra "Respostas": cada ocorrência de um nível
## é contada, e a 1ª ocorrência de cada letra é tratada como exercícios,
## a 2ª como gabarito — funciona em todas as variações observadas.
NIVEL_TOKEN_RE = re.compile(
    r"^(?:gabarito[\s\-]*n[íi]vel|n[íi]vel|gabarito)[\s\-]*([ABC])$",
    re.IGNORECASE,
)
## Limitado a 1-2 dígitos de propósito: números de 4 dígitos (anos como
## "2010", "2016" citados no enunciado) às vezes ficam sozinhos no início
## de uma linha por causa da quebra de linha do PDF, e sem esse limite
## eram capturados como se fossem o número de uma questão, corrompendo a
## questão seguinte.
QUESTAO_RE = re.compile(r"^(\d{1,2})[.)]\s*(.*)$")
ALTERNATIVA_RE = re.compile(r"\([A-E]\)")
LETRA_UNICA_RE = re.compile(r"^[A-E]$")
PALAVRAS_FIGURA = re.compile(
    r"\b(figura|diagrama|esquema|gr[áa]fico|ilustra|hachurad|cart[ãa]o|cart[õo]es|tabuleiro)\b",
    re.IGNORECASE,
)


@dataclass
class Questao:
    nivel: str
    numero: int
    tipo: str = ""
    enunciado: str = ""
    pagina: int = 0
    tem_figura: bool = False
    gabarito: str = ""
    pagina_gabarito: int = 0


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------
# Leitura do PDF, página por página (pra saber de qual página cada
# questão veio, útil pra exportar a página como imagem depois)
# --------------------------------------------------------------------------

def num_paginas(caminho_pdf: str) -> int:
    saida = subprocess.run(
        ["pdfinfo", caminho_pdf], capture_output=True, text=True, check=True
    ).stdout
    m = re.search(r"^Pages:\s+(\d+)", saida, re.MULTILINE)
    if not m:
        raise RuntimeError("Não consegui ler o número de páginas (pdfinfo).")
    return int(m.group(1))


## Tabela de gabarito com várias colunas (comum quando o nível tem muitas
## questões de múltipla escolha) vira UMA linha só em "pdftotext -layout",
## por exemplo "1) C 11) C 21) C 31) E 41) C" (5 respostas lado a lado).
## Sem desdobrar isso, só a primeira resposta de cada linha da tabela seria
## capturada, perdendo as outras colunas inteiras.
## O lookbehind negativo evita confundir "17)" de uma tabela de verdade
## com o "17)" de dentro de "f(17)" (notação de função — comum no
## capítulo de Função) ou de um par ordenado "(3, 5)": nesses casos o
## dígito vem logo depois de "(" ou de outro dígito (quando é só o final
## de um número de 2 dígitos), nunca depois de espaço/início de linha
## como numa coluna de tabela de verdade.
TABELA_GABARITO_RE = re.compile(r"(?<![(\d])(\d{1,2})\)\s*(.*?)(?=\s*(?<![(\d])\d{1,2}\)|$)")


def desdobrar_linha_tabela(texto: str) -> list:
    ## Exige 3+ ocorrências (não 2) como segunda camada de proteção contra
    ## falso positivo — uma linha de tabela de gabarito de verdade tem bem
    ## mais colunas que isso (observado: 5 por linha).
    if len(re.findall(r"(?<![(\d])\d{1,2}\)", texto)) < 3:
        return [texto]
    partes = [(n, v.strip()) for n, v in TABELA_GABARITO_RE.findall(texto) if v.strip()]
    if len(partes) < 3:
        return [texto]
    return [f"{numero}) {valor}" for numero, valor in partes]


def extrair_linhas_com_pagina(caminho_pdf: str) -> list:
    """Retorna lista de (texto_da_linha, numero_da_pagina), já sem linhas
    vazias e sem o caractere de quebra de página (\\f) do pdftotext."""
    total = num_paginas(caminho_pdf)
    linhas = []
    for pagina in range(1, total + 1):
        saida = subprocess.run(
            ["pdftotext", "-layout", "-f", str(pagina), "-l", str(pagina), caminho_pdf, "-"],
            capture_output=True, text=True, check=True,
        ).stdout
        for linha in saida.replace("\f", "\n").splitlines():
            texto = re.sub(r"[ \t]{2,}", " ", linha).strip()
            if texto:
                for sublinha in desdobrar_linha_tabela(texto):
                    linhas.append((sublinha, pagina))
    return linhas


# --------------------------------------------------------------------------
# Segmentação em níveis / questões
# --------------------------------------------------------------------------

GABARITO_WORD_RE = re.compile(r"gabarito", re.IGNORECASE)


def segmentar(linhas: list, divisoes_manuais: list = None) -> dict:
    """Quebra o documento em blocos de exercício/gabarito por nível (A/B/C),
    usando os cabeçalhos explícitos ('Nível-A', 'NÍVEL - B', 'GABARITO
    NÍVEL C', 'GABARITO A' ...).

    Um cabeçalho com a palavra 'gabarito' é SEMPRE gabarito, não importa
    quantas vezes a letra já apareceu antes — em alguns capítulos só o
    lado do gabarito usa essa palavra. Um cabeçalho 'Nível X' sem
    'gabarito' é ambíguo: a 1ª vez que aparece é exercício, a 2ª é
    gabarito (é assim que a maioria dos capítulos marca as duas seções).

    Os blocos de EXERCÍCIO (sem rótulo 'gabarito') são atribuídos a A, B, C
    pela ORDEM em que aparecem no documento (sempre nessa ordem nos
    capítulos observados). Os blocos de GABARITO usam a letra do próprio
    cabeçalho, não a posição — a ordem de impressão do gabarito às vezes
    sai fora de ordem (ex: C, A, B).

    Alguns capítulos têm um nível de exercício SEM cabeçalho nenhum (nem
    texto nem imagem reconhecível) — só a numeração reinicia do 1 sem
    aviso. Detectar isso automaticamente por toda a extensão do documento
    se mostrou arriscado demais (gera falso positivo dentro do próprio
    gabarito de outros capítulos, corrompendo dado que já estava certo).
    Por isso, em vez de heurística automática, `divisoes_manuais` permite
    indicar manualmente onde um nível começa: lista de tuplas
    (nivel, texto_que_comeca_a_questao_1_desse_nivel). Use só quando o
    script avisar que não achou o nível X."""
    cabecalhos = []  # (índice_da_linha_do_cabeçalho, nivel, é_gabarito)
    for i, (texto, _pagina) in enumerate(linhas):
        m = NIVEL_TOKEN_RE.match(texto)
        if m:
            cabecalhos.append((i, m.group(1).upper(), bool(GABARITO_WORD_RE.search(texto))))

    contagem_nivel_puro = {}
    cabecalhos_classificados = []  # (índice_inicio_do_bloco, nivel, é_gabarito_de_verdade)
    for i, nivel, eh_gabarito in cabecalhos:
        if eh_gabarito:
            cabecalhos_classificados.append((i + 1, nivel, True))
        else:
            contagem_nivel_puro[nivel] = contagem_nivel_puro.get(nivel, 0) + 1
            cabecalhos_classificados.append((i + 1, nivel, contagem_nivel_puro[nivel] >= 2))

    # Limites vindos de cabeçalho de verdade: a própria linha do cabeçalho
    # (índice i) vira um "segmento" de 1 linha só, descartado a seguir por
    # não ter nenhuma questão — isso impede a linha do cabeçalho de grudar
    # como última linha do bloco anterior.
    limites_cabecalho = []
    for i, _nivel, _gab in cabecalhos:
        limites_cabecalho.append(i)
        limites_cabecalho.append(i + 1)

    # Divisão manual: não existe linha de cabeçalho pra descartar, o
    # início do bloco já é a própria questão 1 do nível — só 1 limite.
    for nivel, texto_alvo in (divisoes_manuais or []):
        idx = next((i for i, (t, _p) in enumerate(linhas) if t.strip().startswith(texto_alvo.strip())), None)
        if idx is None:
            raise ValueError(f"Divisão manual não encontrada: não achei uma linha começando com {texto_alvo!r}")
        cabecalhos_classificados.append((idx, nivel.upper(), False))
        limites_cabecalho.append(idx)

    cabecalhos_classificados.sort(key=lambda h: h[0])

    limites = sorted(set([0, len(linhas)] + limites_cabecalho))

    segmentos = []
    for ini, fim in zip(limites, limites[1:]):
        bloco = linhas[ini:fim]
        if not any(QUESTAO_RE.match(t) for t, _ in bloco):
            continue
        header = next((h for h in cabecalhos_classificados if h[0] == ini), None)
        segmentos.append({"linhas": bloco, "header": header})

    blocos = {nivel: {"exercicios": [], "gabaritos": []} for nivel in "ABC"}

    # O trecho ANTES do primeiro cabeçalho (teoria do capítulo) nunca é um
    # segmento de exercício de verdade, mesmo que, por coincidência, tenha
    # alguma linha que pareça número de questão (ex: passos numerados de
    # uma demonstração, "1) ... 2) ... 3) ..."). Por isso exige header
    # (explícito ou de --divisao-manual) pra contar como exercício, não só
    # "não ter a palavra gabarito".
    segmentos_exercicio = [s for s in segmentos if s["header"] and not s["header"][2]]
    for nivel, seg in zip("ABC", segmentos_exercicio):
        blocos[nivel]["exercicios"] = seg["linhas"]

    segmentos_gabarito = [s for s in segmentos if s["header"] and s["header"][2]]
    for seg in segmentos_gabarito:
        nivel = seg["header"][1]
        blocos[nivel]["gabaritos"] = seg["linhas"]

    return blocos


def extrair_questoes_do_bloco(linhas: list) -> dict:
    """Agrupa as linhas de um bloco em questões por número. Ignora
    'questão 0' — sempre é artefato de um número decimal (ex: '0,333...')
    que a quebra de linha do PDF deixou sozinho no início da linha, nunca
    uma questão de verdade."""
    questoes = {}
    numero_atual = None
    for texto, pagina in linhas:
        m = QUESTAO_RE.match(texto)
        if m and m.group(1) == "0":
            m = None
        if m:
            numero_atual = int(m.group(1))
            questoes[numero_atual] = {"partes": [(m.group(2), pagina)], "pagina": pagina}
        elif numero_atual is not None:
            questoes[numero_atual]["partes"].append((texto, pagina))
    resultado = {}
    for numero, info in questoes.items():
        texto_completo = "\n".join(t for t, _ in info["partes"] if t)
        resultado[numero] = (texto_completo, info["pagina"])
    return resultado


def classificar_tipo(enunciado: str, gabarito: str) -> str:
    gabarito_limpo = gabarito.strip().rstrip(".")
    if LETRA_UNICA_RE.match(gabarito_limpo):
        return "Múltipla escolha"
    if ALTERNATIVA_RE.search(enunciado):
        return "Múltipla escolha"
    if re.search(r"verdadeir[oa]\s*\(V\)|falso\s*\(F\)", enunciado, re.IGNORECASE):
        return "Verdadeiro/Falso"
    return "Analítica"


# --------------------------------------------------------------------------
# Banco de dados
# --------------------------------------------------------------------------

def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            livro TEXT,
            capitulo TEXT,
            nivel TEXT,
            numero INTEGER,
            tipo TEXT,
            enunciado TEXT,
            pagina INTEGER,
            tem_figura INTEGER,
            imagem_pagina TEXT,
            gabarito TEXT,
            pagina_gabarito INTEGER,
            arquivo_origem TEXT,
            capturado_em TEXT,
            UNIQUE(livro, capitulo, nivel, numero)
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_capitulo_nivel ON questoes(capitulo, nivel)")
    conn.commit()
    return conn


def salvar_questao(conn: sqlite3.Connection, livro: str, capitulo: str,
                    arquivo_origem: str, q: Questao, imagem_pagina: str) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO questoes (
            livro, capitulo, nivel, numero, tipo, enunciado, pagina,
            tem_figura, imagem_pagina, gabarito, pagina_gabarito,
            arquivo_origem, capturado_em
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            livro, capitulo, q.nivel, q.numero, q.tipo, q.enunciado, q.pagina,
            int(q.tem_figura), imagem_pagina, q.gabarito, q.pagina_gabarito,
            arquivo_origem, datetime.now().isoformat(timespec="seconds"),
        ),
    )
    conn.commit()


# --------------------------------------------------------------------------
# Exportação de página como imagem (só pras questões com figura/diagrama)
# --------------------------------------------------------------------------

def exportar_pagina_como_imagem(caminho_pdf: str, pagina: int, pasta_saida: Path) -> str:
    pasta_saida.mkdir(parents=True, exist_ok=True)
    prefixo = pasta_saida / f"pagina_{pagina:03d}"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "200", "-f", str(pagina), "-l", str(pagina),
         caminho_pdf, str(prefixo)],
        check=True, capture_output=True,
    )
    candidatos = list(pasta_saida.glob(f"pagina_{pagina:03d}*.png"))
    return str(candidatos[0]) if candidatos else ""


# --------------------------------------------------------------------------
# Pipeline principal
# --------------------------------------------------------------------------

def processar_arquivo(caminho_pdf: str, divisoes_manuais: list = None) -> list:
    linhas = extrair_linhas_com_pagina(caminho_pdf)
    blocos = segmentar(linhas, divisoes_manuais)

    if not any(blocos[n]["exercicios"] for n in "ABC"):
        raise ValueError(
            "Não encontrei nenhum cabeçalho de nível (Nível-A/B/C, "
            "GABARITO NÍVEL X etc.) neste documento."
        )

    questoes = []
    for nivel in "ABC":
        linhas_exercicios = blocos[nivel]["exercicios"]
        linhas_gabaritos = blocos[nivel]["gabaritos"]
        if not linhas_exercicios and not linhas_gabaritos:
            continue  # este capítulo não usa esse nível
        exercicios = extrair_questoes_do_bloco(linhas_exercicios)
        gabaritos = extrair_questoes_do_bloco(linhas_gabaritos)
        numeros = sorted(set(exercicios) | set(gabaritos))
        for numero in numeros:
            enunciado, pagina = exercicios.get(numero, ("", 0))
            gabarito, pagina_gab = gabaritos.get(numero, ("", 0))
            if not enunciado:
                log(f"AVISO: Nível-{nivel} questão {numero} sem enunciado (só gabarito). Pulando.")
                continue
            if not gabarito:
                log(f"AVISO: Nível-{nivel} questão {numero} sem gabarito correspondente.")
            tipo = classificar_tipo(enunciado, gabarito)
            tem_figura = bool(PALAVRAS_FIGURA.search(enunciado))
            questoes.append(Questao(
                nivel=nivel, numero=numero, tipo=tipo, enunciado=enunciado,
                pagina=pagina, tem_figura=tem_figura, gabarito=gabarito,
                pagina_gabarito=pagina_gab,
            ))
    return questoes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf", help="Arquivo .pdf do capítulo")
    parser.add_argument("--livro", required=True, help="Nome do livro (ex: 'Matemática para Vestibular Vol 01')")
    parser.add_argument("--capitulo", required=True, help="Nome do capítulo/assunto (ex: 'Lógica e Conjuntos')")
    parser.add_argument("--output", default="banco_matvest.db", help="Caminho do SQLite de saída")
    parser.add_argument("--exportar-figuras", action="store_true",
                         help="Renderiza em PNG a página de cada questão marcada com figura/diagrama")
    parser.add_argument("--pasta-figuras", default="figuras", help="Pasta onde salvar as páginas exportadas")
    parser.add_argument(
        "--divisao-manual", action="append", default=[], metavar="NIVEL:TEXTO",
        help=(
            "Use só quando o script não achar um nível (acontece em capítulos "
            "onde o cabeçalho 'Nível X' dos exercícios é uma imagem sem texto "
            "nenhum, em vez de um banner de texto normal). Formato "
            "'B:texto que começa a questão 1 desse nível', ex: "
            "--divisao-manual \"B:1. (UNIRIO) O valor de\". Pode repetir a "
            "opção para mais de um nível."
        ),
    )
    args = parser.parse_args()

    if shutil.which("pdftotext") is None or shutil.which("pdfinfo") is None:
        raise SystemExit("ERRO: 'pdftotext'/'pdfinfo' não encontrados. Instale poppler-utils.")

    divisoes_manuais = []
    for item in args.divisao_manual:
        nivel, _, texto = item.partition(":")
        if not texto:
            raise SystemExit(f"ERRO: --divisao-manual mal formatado: {item!r}. Use NIVEL:texto")
        divisoes_manuais.append((nivel.strip(), texto.strip()))

    log(f"Processando {args.pdf} ...")
    questoes = processar_arquivo(args.pdf, divisoes_manuais)

    conn = init_db(args.output)
    arquivo_origem = Path(args.pdf).name
    pasta_figuras = Path(args.pasta_figuras)

    for q in questoes:
        imagem_pagina = ""
        if q.tem_figura and args.exportar_figuras:
            imagem_pagina = exportar_pagina_como_imagem(args.pdf, q.pagina, pasta_figuras)
        salvar_questao(conn, args.livro, args.capitulo, arquivo_origem, q, imagem_pagina)
    conn.close()

    total = len(questoes)
    com_figura = sum(1 for q in questoes if q.tem_figura)
    sem_gabarito = sum(1 for q in questoes if not q.gabarito)

    log(f"Concluído. {total} questões salvas em {args.output}.")
    log(f"  - {com_figura} marcadas com possível figura/diagrama (revisão manual)")
    log(f"  - {sem_gabarito} sem gabarito correspondente encontrado")
    if com_figura and not args.exportar_figuras:
        log("  (rode de novo com --exportar-figuras pra salvar a página dessas questões como imagem)")


if __name__ == "__main__":
    main()
