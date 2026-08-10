import enum


class PapelCoordenador(str, enum.Enum):
    admin_instituicao = "admin_instituicao"
    coordenador = "coordenador"


class ArquivoTipo(str, enum.Enum):
    grade = "grade"
    modelo = "modelo"
    siglas = "siglas"
    simulados = "simulados"


class JobStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"


class CalendarioStatus(str, enum.Enum):
    verified = "verified"
    published = "published"
    failed = "failed"


class RelatorioTipo(str, enum.Enum):
    trocas = "trocas"
    cessoes = "cessoes"
    tabela = "tabela"
    auxiliar_ia = "auxiliar_ia"
