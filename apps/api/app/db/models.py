import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.enums import (
    ArquivoTipo,
    CalendarioStatus,
    JobStatus,
    PapelCoordenador,
    RelatorioTipo,
)


class Instituicao(Base):
    __tablename__ = "instituicao"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    coordenadores: Mapped[list["Coordenador"]] = relationship(back_populates="instituicao")
    regras_catalogo: Mapped[list["RegraCatalogo"]] = relationship(back_populates="instituicao")


class Coordenador(Base):
    __tablename__ = "coordenador"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instituicao_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.instituicao.id"), nullable=False
    )
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    papel: Mapped[PapelCoordenador] = mapped_column(nullable=False)
    senha_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    instituicao: Mapped["Instituicao"] = relationship(back_populates="coordenadores")
    segmento: Mapped["Segmento | None"] = relationship(back_populates="coordenador", uselist=False)


class Segmento(Base):
    __tablename__ = "segmento"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    coordenador_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.coordenador.id"), unique=True, nullable=False
    )
    nome: Mapped[str] = mapped_column(String(255), nullable=False)

    coordenador: Mapped["Coordenador"] = relationship(back_populates="segmento")
    grupos: Mapped[list["Grupo"]] = relationship(back_populates="segmento")
    semestres: Mapped[list["Semestre"]] = relationship(back_populates="segmento")
    regras_config: Mapped[list["RegraConfig"]] = relationship(back_populates="segmento")
    customizacoes_ia: Mapped[list["CustomizacaoIA"]] = relationship(back_populates="segmento")


class Grupo(Base):
    __tablename__ = "grupo"
    __table_args__ = (
        Index("ix_grupo_segmento_id", "segmento_id"),
        {"schema": "calendario"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segmento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.segmento.id"), nullable=False
    )
    nome: Mapped[str] = mapped_column(String(64), nullable=False)
    data_inicio_semestre: Mapped[date] = mapped_column(Date, nullable=False)
    data_fim_semestre: Mapped[date] = mapped_column(Date, nullable=False)
    datas_segunda_chamada: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    conselho_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    conselho_fim: Mapped[date] = mapped_column(Date, nullable=False)

    segmento: Mapped["Segmento"] = relationship(back_populates="grupos")
    turmas: Mapped[list["Turma"]] = relationship(back_populates="grupo")


class Turma(Base):
    __tablename__ = "turma"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grupo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.grupo.id"), nullable=False
    )
    codigo: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)

    grupo: Mapped["Grupo"] = relationship(back_populates="turmas")


class Semestre(Base):
    __tablename__ = "semestre"
    __table_args__ = (
        Index("ix_semestre_segmento_id", "segmento_id"),
        {"schema": "calendario"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segmento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.segmento.id"), nullable=False
    )
    ano: Mapped[int] = mapped_column(Integer, nullable=False)
    periodo: Mapped[int] = mapped_column(Integer, nullable=False)
    inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fim: Mapped[date] = mapped_column(Date, nullable=False)

    segmento: Mapped["Segmento"] = relationship(back_populates="semestres")
    arquivos: Mapped[list["ArquivoEntrada"]] = relationship(back_populates="semestre")
    jobs: Mapped[list["Job"]] = relationship(back_populates="semestre")
    calendarios: Mapped[list["CalendarioGerado"]] = relationship(back_populates="semestre")
    regras_config: Mapped[list["RegraConfig"]] = relationship(back_populates="semestre")
    customizacoes_ia: Mapped[list["CustomizacaoIA"]] = relationship(back_populates="semestre")


class RegraCatalogo(Base):
    __tablename__ = "regra_catalogo"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    instituicao_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.instituicao.id"), nullable=True
    )
    codigo: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    descricao: Mapped[str] = mapped_column(Text, nullable=False)
    implementada_solver: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    skill_ref: Mapped[str | None] = mapped_column(String(512))

    instituicao: Mapped["Instituicao | None"] = relationship(back_populates="regras_catalogo")
    configs: Mapped[list["RegraConfig"]] = relationship(back_populates="regra")


class RegraConfig(Base):
    __tablename__ = "regra_config"
    __table_args__ = (
        UniqueConstraint("segmento_id", "semestre_id", "regra_id", name="uq_regra_config_segmento_semestre_regra"),
        Index("ix_regra_config_segmento_id", "segmento_id"),
        {"schema": "calendario"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segmento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.segmento.id"), nullable=False
    )
    semestre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.semestre.id"), nullable=False
    )
    regra_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.regra_catalogo.id"), nullable=False
    )
    ativo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    params: Mapped[dict | None] = mapped_column(JSONB)

    segmento: Mapped["Segmento"] = relationship(back_populates="regras_config")
    semestre: Mapped["Semestre"] = relationship(back_populates="regras_config")
    regra: Mapped["RegraCatalogo"] = relationship(back_populates="configs")


class CustomizacaoIA(Base):
    __tablename__ = "customizacao_ia"
    __table_args__ = (
        Index("ix_customizacao_ia_segmento_id", "segmento_id"),
        {"schema": "calendario"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    segmento_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.segmento.id"), nullable=False
    )
    semestre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.semestre.id"), nullable=False
    )
    instrucao: Mapped[str] = mapped_column(Text, nullable=False)
    contexto: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    segmento: Mapped["Segmento"] = relationship(back_populates="customizacoes_ia")
    semestre: Mapped["Semestre"] = relationship(back_populates="customizacoes_ia")


class ArquivoEntrada(Base):
    __tablename__ = "arquivo_entrada"
    __table_args__ = (
        UniqueConstraint("semestre_id", "tipo", name="uq_arquivo_entrada_semestre_tipo"),
        {"schema": "calendario"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    semestre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.semestre.id"), nullable=False
    )
    tipo: Mapped[ArquivoTipo] = mapped_column(nullable=False)
    blob_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    checksum: Mapped[str] = mapped_column(String(64), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    semestre: Mapped["Semestre"] = relationship(back_populates="arquivos")


class Job(Base):
    __tablename__ = "job"
    __table_args__ = (
        Index("ix_job_status_created_at", "status", "created_at"),
        {"schema": "calendario"},
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    semestre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.semestre.id"), nullable=False
    )
    status: Mapped[JobStatus] = mapped_column(nullable=False, default=JobStatus.queued)
    payload: Mapped[dict | None] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error: Mapped[str | None] = mapped_column(Text)

    semestre: Mapped["Semestre"] = relationship(back_populates="jobs")
    calendario: Mapped["CalendarioGerado | None"] = relationship(back_populates="job", uselist=False)


class CalendarioGerado(Base):
    __tablename__ = "calendario_gerado"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    semestre_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.semestre.id"), nullable=False
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.job.id"), unique=True, nullable=False
    )
    status: Mapped[CalendarioStatus] = mapped_column(nullable=False)
    xlsx_blob_path: Mapped[str | None] = mapped_column(String(1024))
    verificacao_result: Mapped[dict | None] = mapped_column(JSONB)
    publicado_em: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    semestre: Mapped["Semestre"] = relationship(back_populates="calendarios")
    job: Mapped["Job"] = relationship(back_populates="calendario")
    relatorios: Mapped[list["Relatorio"]] = relationship(back_populates="calendario")


class Relatorio(Base):
    __tablename__ = "relatorio"
    __table_args__ = {"schema": "calendario"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    calendario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendario.calendario_gerado.id"), nullable=False
    )
    tipo: Mapped[RelatorioTipo] = mapped_column(nullable=False)
    blob_path: Mapped[str] = mapped_column(String(1024), nullable=False)

    calendario: Mapped["CalendarioGerado"] = relationship(back_populates="relatorios")
