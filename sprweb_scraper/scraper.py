#!/usr/bin/env python3
"""
Captura questões do banco de itens do Super Professor (interno.superprofessor.com.br)
e monta um banco de dados local (SQLite) categorizado por ensino/matéria/tópico/subtópico.

USO BÁSICO
----------
    pip install -r requirements.txt
    playwright install chromium

    export SPRWEB_EMAIL="voce@exemplo.com"
    export SPRWEB_SENHA="sua-senha"

    python scraper.py --ensino Medio --materia Matematica --max-questions 5 --headed --debug

Rode primeiro com --headed --debug e --max-questions baixo (2 a 5) para validar que os
cliques na tela estão funcionando antes de rodar uma captura grande.

Por padrão, entre uma questão e outra o script espera um intervalo aleatório de 10 a
90 segundos (--delay-min / --delay-max), para não se comportar como um robô batendo
sempre no mesmo ritmo. Isso deixa uma captura grande bem mais lenta — é intencional.

CREDENCIAIS
-----------
Nunca passe e-mail/senha na linha de comando (fica no histórico do shell). Use as
variáveis de ambiente SPRWEB_EMAIL / SPRWEB_SENHA, ou deixe em branco que o script
pede interativamente (senha oculta, via getpass).

SE ALGO NÃO CLICAR CERTO
-------------------------
Este script foi escrito a partir de prints de tela, sem acesso ao HTML real do site.
Os pontos mais prováveis de precisar de ajuste estão marcados com "AJUSTE AQUI" nos
comentários. Rode com --debug: ao primeiro erro ele abre o Playwright Inspector e
pausa a execução, permitindo testar seletores manualmente (use a aba "Pick locator").
Copie o seletor que funcionou e me mande para eu corrigir o código.
"""

import argparse
import getpass
import json
import os
import random
import re
import sqlite3
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

LOGIN_URL = "https://interno.superprofessor.com.br/"
STORAGE_STATE_FILE = "storage_state.json"
DEFAULT_DB_FILE = "questoes.db"
IMAGES_DIR = "imagens"

LABELS_ATRIBUTOS = [
    "ID",
    "Fonte",
    "Ano",
    "Região",
    "Dificuldade",
    "Tipo",
    "Data de publicação",
    "Tempo de leitura estimado",
]


@dataclass
class Questao:
    id_site: str
    ensino: str = ""
    materia: str = ""
    topico: str = ""
    subtopico: str = ""
    fonte: str = ""
    ano: str = ""
    regiao: str = ""
    dificuldade: str = ""
    tipo: str = ""
    data_publicacao: str = ""
    tempo_leitura: str = ""
    enunciado_texto: str = ""
    alternativas: list = field(default_factory=list)
    resposta_correta: str = ""
    resolucao_texto: str = ""
    imagens: list = field(default_factory=list)
    raw_text: str = ""
    captured_at: str = ""


def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------
# Banco de dados local
# --------------------------------------------------------------------------

def init_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS questoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_site TEXT UNIQUE NOT NULL,
            ensino TEXT,
            materia TEXT,
            topico TEXT,
            subtopico TEXT,
            fonte TEXT,
            ano TEXT,
            regiao TEXT,
            dificuldade TEXT,
            tipo TEXT,
            data_publicacao TEXT,
            tempo_leitura TEXT,
            enunciado_texto TEXT,
            alternativas_json TEXT,
            resposta_correta TEXT,
            resolucao_texto TEXT,
            imagens_json TEXT,
            raw_text TEXT,
            captured_at TEXT
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_materia ON questoes(materia)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_topico ON questoes(topico, subtopico)")
    conn.commit()
    return conn


def already_captured(conn: sqlite3.Connection, id_site: str) -> bool:
    row = conn.execute("SELECT 1 FROM questoes WHERE id_site = ?", (id_site,)).fetchone()
    return row is not None


def save_questao(conn: sqlite3.Connection, q: Questao) -> None:
    conn.execute(
        """
        INSERT OR REPLACE INTO questoes (
            id_site, ensino, materia, topico, subtopico, fonte, ano, regiao,
            dificuldade, tipo, data_publicacao, tempo_leitura, enunciado_texto,
            alternativas_json, resposta_correta, resolucao_texto, imagens_json,
            raw_text, captured_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            q.id_site, q.ensino, q.materia, q.topico, q.subtopico, q.fonte, q.ano,
            q.regiao, q.dificuldade, q.tipo, q.data_publicacao, q.tempo_leitura,
            q.enunciado_texto, json.dumps(q.alternativas, ensure_ascii=False),
            q.resposta_correta, q.resolucao_texto,
            json.dumps(q.imagens, ensure_ascii=False), q.raw_text, q.captured_at,
        ),
    )
    conn.commit()


# --------------------------------------------------------------------------
# Login e navegação
# --------------------------------------------------------------------------

def _first_visible(page: Page, candidatos, descricao: str, timeout_each: int = 3000):
    """Tenta várias estratégias de seletor em sequência e retorna a primeira que
    achar um elemento visível. Cada `candidato` é uma função `() -> Locator`.
    Falha rápido em cada tentativa (timeout_each) em vez de esperar o timeout
    padrão do Playwright (30s) em cada uma."""
    for candidato in candidatos:
        try:
            loc = candidato().first
            loc.wait_for(state="visible", timeout=timeout_each)
            return loc
        except PlaywrightTimeoutError:
            continue
    raise RuntimeError(
        f"Não encontrei o elemento '{descricao}' com nenhum dos seletores tentados. "
        f"Rode com --debug e --headed, e quando pausar use o Playwright Inspector "
        f"(botão 'Pick locator') para achar o seletor certo."
    )


def login(page: Page, email: str, senha: str) -> None:
    log("Abrindo página de login...")
    page.goto(LOGIN_URL, wait_until="domcontentloaded")

    # AJUSTE AQUI: ordem de tentativas para achar os campos. O site pode não
    # associar o texto "E-mail"/"Senha" como <label for=...> de verdade, então
    # não dependemos só de get_by_label.
    campo_email = _first_visible(page, [
        lambda: page.get_by_label("E-mail"),
        lambda: page.get_by_placeholder(re.compile("e-?mail", re.I)),
        lambda: page.locator("input[type=email]"),
        lambda: page.locator("input[type=text]"),
    ], descricao="campo de e-mail")
    campo_email.fill(email)

    campo_senha = _first_visible(page, [
        lambda: page.get_by_label("Senha"),
        lambda: page.get_by_placeholder(re.compile("senha", re.I)),
        lambda: page.locator("input[type=password]"),
    ], descricao="campo de senha")
    campo_senha.fill(senha)

    botao_entrar = _first_visible(page, [
        lambda: page.get_by_role("button", name="Entrar"),
        lambda: page.get_by_text("Entrar", exact=True),
    ], descricao="botão Entrar")
    botao_entrar.click()

    # Espera a home carregar (aparece o menu "Montar prova").
    page.get_by_text("Montar prova", exact=False).first.wait_for(timeout=20000)
    log("Login OK.")


def abrir_montar_prova(page: Page) -> None:
    log("Abrindo 'Montar prova'...")
    page.get_by_text("Montar prova", exact=False).first.click()
    page.get_by_text("Selecione um ensino").first.wait_for(timeout=15000)


def selecionar_ensino(page: Page, ensino: str) -> None:
    log(f"Selecionando ensino: {ensino}")
    page.get_by_text("Selecione um ensino").click()
    try:
        page.get_by_role("option", name=ensino).click(timeout=3000)
    except PlaywrightTimeoutError:
        # AJUSTE AQUI: dropdown pode não expor role=option (componente custom).
        page.get_by_text(ensino, exact=True).last.click()


def click_checkbox_near_text(page: Page, texto: str) -> None:
    """Marca o checkbox mais próximo de um texto visível (ex: nome da matéria).

    AJUSTE AQUI se a árvore de assuntos não usar <li>/<div> com input[type=checkbox]
    ou [role=checkbox] como container do rótulo.
    """
    label = page.get_by_text(texto, exact=True).first
    label.wait_for(timeout=10000)
    container = label.locator(
        "xpath=ancestor-or-self::*[self::li or self::div]"
        "[.//input[@type='checkbox'] or .//*[@role='checkbox']][1]"
    )
    checkbox = container.locator("input[type=checkbox], [role=checkbox]").first
    checkbox.click()


def selecionar_materia(page: Page, materia: str) -> None:
    log(f"Selecionando matéria: {materia}")
    click_checkbox_near_text(page, materia)
    # Espera o painel de questões carregar ("Questão 1 de N").
    page.get_by_text(re.compile(r"Questão\s+\d+\s+de\s+\d+")).first.wait_for(timeout=20000)


def get_total_questoes(page: Page) -> int:
    texto = page.get_by_text(re.compile(r"de\s+\d+")).first.inner_text()
    m = re.search(r"de\s+(\d+)", texto)
    return int(m.group(1)) if m else 0


def ir_para_proxima_questao(page: Page) -> bool:
    """Clica na seta 'próxima questão'. Retorna False se não havia próxima.

    AJUSTE AQUI: seletor por posição relativa ao texto 'de N'. Se o botão de
    próxima não for o primeiro <button> depois desse texto, será preciso
    localizar de outra forma (ex: aria-label, ícone com título específico).
    """
    marcador = page.get_by_text(re.compile(r"de\s+\d+")).first
    next_btn = marcador.locator("xpath=following::button[1]")
    if next_btn.count() == 0:
        return False
    if next_btn.is_disabled():
        return False
    next_btn.click()
    return True


# --------------------------------------------------------------------------
# Extração dos dados da questão
# --------------------------------------------------------------------------

def parse_atributos(bloco_texto: str) -> dict:
    """Extrai pares 'Rótulo: valor' de um bloco de texto livre, na ordem de
    LABELS_ATRIBUTOS, tolerando espaços/quebras de linha entre eles."""
    valores = {}
    for i, label in enumerate(LABELS_ATRIBUTOS):
        proximos = "|".join(re.escape(l) for l in LABELS_ATRIBUTOS[i + 1:])
        if proximos:
            padrao = rf"{re.escape(label)}\*?:\s*(.+?)(?=\s{{2,}}(?:{proximos})\*?:|\n(?:{proximos})\*?:|$)"
        else:
            padrao = rf"{re.escape(label)}\*?:\s*(.+?)(?:\n|$)"
        m = re.search(padrao, bloco_texto, flags=re.DOTALL)
        valores[label] = m.group(1).strip() if m else ""
    return valores


def extrair_questao_atual(page: Page) -> Optional[Questao]:
    # Painel central: melhor esforço para achar um container amplo que cubra
    # do enunciado até "Dados e estatísticas". AJUSTE AQUI se pegar texto
    # demais (barras laterais) ou de menos.
    ancora = page.get_by_text("Dados e estatísticas").first
    ancora.wait_for(timeout=15000)
    painel = ancora.locator(
        "xpath=ancestor::*[self::main or self::div][1]"
    )
    texto_completo = painel.inner_text()

    if "Resposta e resolução" not in texto_completo:
        log("AVISO: seção 'Resposta e resolução' não encontrada no painel extraído.")

    antes, _, depois = texto_completo.partition("Resposta e resolução")
    resolucao_bloco, _, stats_bloco = depois.partition("Dados e estatísticas")

    # ID da questão (necessário para dedupe) — tenta achar no bloco de stats.
    m_id = re.search(r"ID:\s*(\d+)", stats_bloco)
    if not m_id:
        log("ERRO: não encontrei o ID da questão neste painel, pulando.")
        return None
    id_site = m_id.group(1)

    # Assunto (trilha materia > topico > subtopico), primeira ocorrência tipo "A > B > C".
    m_assunto = re.search(r"([^\n>]+?>\s*[^\n>]+(?:>\s*[^\n>]+)?)", antes)
    trilha = [p.strip() for p in m_assunto.group(1).split(">")] if m_assunto else []
    materia = trilha[0] if len(trilha) > 0 else ""
    topico = trilha[1] if len(trilha) > 1 else ""
    subtopico = trilha[2] if len(trilha) > 2 else ""

    # Alternativas: linhas que começam com "A." "B." etc.
    linhas = [l.strip() for l in antes.splitlines() if l.strip()]
    alt_idx = [i for i, l in enumerate(linhas) if re.match(r"^[A-H]\.\s", l)]
    if alt_idx:
        enunciado_linhas = linhas[:alt_idx[0]]
        alternativas = []
        for i in alt_idx:
            m = re.match(r"^([A-H])\.\s*(.+)$", linhas[i])
            if m:
                alternativas.append({"letra": m.group(1), "texto": m.group(2)})
    else:
        enunciado_linhas = linhas
        alternativas = []

    # Remove a linha da trilha de assunto e as tags de topo (fonte/ano/dificuldade/tipo)
    # do enunciado, se tiverem sido capturadas junto.
    enunciado_linhas = [
        l for l in enunciado_linhas
        if not re.match(r"^[^\n>]+>\s*[^\n>]+", l)
        and "Ocultar detalhes" not in l and "Mostrar detalhes" not in l
    ]
    enunciado_texto = "\n".join(enunciado_linhas).strip()

    m_resp = re.search(r"\[([A-Z])\]", resolucao_bloco)
    resposta_correta = m_resp.group(1) if m_resp else ""
    resolucao_texto = resolucao_bloco.strip()

    atributos = parse_atributos(stats_bloco)

    imagens = []
    try:
        for img in painel.locator("img").all():
            src = img.get_attribute("src")
            if src:
                imagens.append(src)
    except Exception as e:
        log(f"AVISO: falha ao coletar imagens: {e}")

    return Questao(
        id_site=id_site,
        materia=materia,
        topico=topico,
        subtopico=subtopico,
        fonte=atributos.get("Fonte", ""),
        ano=atributos.get("Ano", ""),
        regiao=atributos.get("Região", ""),
        dificuldade=atributos.get("Dificuldade", ""),
        tipo=atributos.get("Tipo", ""),
        data_publicacao=atributos.get("Data de publicação", ""),
        tempo_leitura=atributos.get("Tempo de leitura estimado", ""),
        enunciado_texto=enunciado_texto,
        alternativas=alternativas,
        resposta_correta=resposta_correta,
        resolucao_texto=resolucao_texto,
        imagens=imagens,
        raw_text=texto_completo,
        captured_at=datetime.now().isoformat(timespec="seconds"),
    )


def baixar_imagens(page: Page, questao: Questao, pasta_imagens: Path) -> list:
    """Baixa as imagens da questão para disco e retorna os caminhos locais."""
    pasta_imagens.mkdir(parents=True, exist_ok=True)
    caminhos = []
    for i, url in enumerate(questao.imagens):
        try:
            resp = page.request.get(url)
            if resp.ok:
                ext = Path(url.split("?")[0]).suffix or ".png"
                destino = pasta_imagens / f"{questao.id_site}_{i}{ext}"
                destino.write_bytes(resp.body())
                caminhos.append(str(destino))
        except Exception as e:
            log(f"AVISO: falha ao baixar imagem {url}: {e}")
    return caminhos


# --------------------------------------------------------------------------
# Loop principal
# --------------------------------------------------------------------------

def rodar(args: argparse.Namespace) -> None:
    email = args.email or os.environ.get("SPRWEB_EMAIL") or input("E-mail SPR Web: ").strip()
    senha = args.senha or os.environ.get("SPRWEB_SENHA") or getpass.getpass("Senha SPR Web: ")

    saida_dir = Path(args.output).parent if Path(args.output).parent != Path("") else Path(".")
    saida_dir.mkdir(parents=True, exist_ok=True)
    pasta_imagens = saida_dir / IMAGES_DIR
    storage_state_path = saida_dir / STORAGE_STATE_FILE

    conn = init_db(args.output)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=not args.headed)
        context_kwargs = {}
        if storage_state_path.exists() and not args.force_login:
            context_kwargs["storage_state"] = str(storage_state_path)
        context = browser.new_context(**context_kwargs)
        page = context.new_page()

        try:
            if "storage_state" not in context_kwargs:
                login(page, email, senha)
                context.storage_state(path=str(storage_state_path))
            else:
                page.goto(LOGIN_URL, wait_until="domcontentloaded")
                if page.get_by_label("E-mail").count() > 0:
                    log("Sessão salva expirou, fazendo login novamente...")
                    login(page, email, senha)
                    context.storage_state(path=str(storage_state_path))

            abrir_montar_prova(page)
            selecionar_ensino(page, args.ensino)
            selecionar_materia(page, args.materia)

            total = get_total_questoes(page)
            log(f"Total de questões disponíveis para {args.materia}/{args.ensino}: {total}")

            limite = args.max_questions if args.max_questions else total
            capturadas = 0
            puladas = 0

            for i in range(1, limite + 1):
                if args.debug:
                    log(f"--- questão {i}/{limite} (debug: page.pause() ativo) ---")

                try:
                    questao = extrair_questao_atual(page)
                except Exception as e:
                    log(f"ERRO ao extrair questão na posição {i}: {e}")
                    if args.debug:
                        page.pause()
                    questao = None

                if questao is not None:
                    if already_captured(conn, questao.id_site) and not args.reprocessar:
                        puladas += 1
                    else:
                        questao.ensino = args.ensino
                        if args.baixar_imagens and questao.imagens:
                            questao.imagens = baixar_imagens(page, questao, pasta_imagens)
                        save_questao(conn, questao)
                        capturadas += 1
                        log(f"[{i}/{limite}] capturada id_site={questao.id_site} "
                            f"({questao.subtopico or questao.topico or questao.materia})")

                if i < limite:
                    avancou = ir_para_proxima_questao(page)
                    if not avancou:
                        log("Não há próxima questão, encerrando.")
                        break
                    espera = random.uniform(args.delay_min, args.delay_max)
                    log(f"Aguardando {espera:.1f}s antes da próxima questão...")
                    time.sleep(espera)

            log(f"Concluído. Capturadas: {capturadas}. Já existentes (puladas): {puladas}.")

        except KeyboardInterrupt:
            log("Interrompido pelo usuário.")
        except Exception:
            log("Erro inesperado, entrando em modo debug (se --debug ativo).")
            if args.debug:
                page.pause()
            raise
        finally:
            context.close()
            browser.close()
            conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--email", default=None, help="E-mail (evite: use SPRWEB_EMAIL)")
    parser.add_argument("--senha", default=None, help="Senha (evite: use SPRWEB_SENHA)")
    parser.add_argument("--ensino", default="Médio", help="Ex: Médio, Fundamental, Superior")
    parser.add_argument("--materia", required=True, help="Ex: Matemática, Português")
    parser.add_argument("--output", default=DEFAULT_DB_FILE, help="Caminho do arquivo SQLite de saída")
    parser.add_argument("--max-questions", type=int, default=None, help="Limite de questões a capturar nesta execução")
    parser.add_argument("--delay-min", type=float, default=10.0, help="Espera mínima (segundos) entre questões")
    parser.add_argument("--delay-max", type=float, default=90.0, help="Espera máxima (segundos) entre questões")
    parser.add_argument("--headed", action="store_true", help="Mostra o navegador (recomendado na primeira vez)")
    parser.add_argument("--debug", action="store_true", help="Pausa no Playwright Inspector em caso de erro")
    parser.add_argument("--force-login", action="store_true", help="Ignora sessão salva e faz login de novo")
    parser.add_argument("--reprocessar", action="store_true", help="Recaptura questões já existentes no banco")
    parser.add_argument("--baixar-imagens", action="store_true", help="Baixa as imagens da questão para disco")
    args = parser.parse_args()
    rodar(args)


if __name__ == "__main__":
    sys.exit(main())
