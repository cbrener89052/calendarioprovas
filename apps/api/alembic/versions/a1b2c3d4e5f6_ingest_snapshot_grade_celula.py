"""ingest snapshot and grade_celula

Revision ID: a1b2c3d4e5f6
Revises: 48f843bb6ab4
Create Date: 2026-08-10 22:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "48f843bb6ab4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ingest_snapshot",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("semestre_id", sa.UUID(), nullable=False),
        sa.Column("arquivo_entrada_id", sa.UUID(), nullable=True),
        sa.Column(
            "status",
            sa.Enum(
                "draft",
                "pending_review",
                "approved",
                "rejected",
                name="ingestsnapshotstatus",
            ),
            nullable=False,
        ),
        sa.Column(
            "source_format",
            sa.Enum("pdf", "xlsx", "legacy_py", name="ingestsourceformat"),
            nullable=False,
        ),
        sa.Column("extracted_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_by_id", sa.UUID(), nullable=True),
        sa.Column("warnings", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="[]"),
        sa.Column("metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default="{}"),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["semestre_id"], ["calendario.semestre.id"]),
        sa.ForeignKeyConstraint(["arquivo_entrada_id"], ["calendario.arquivo_entrada.id"]),
        sa.ForeignKeyConstraint(["approved_by_id"], ["calendario.coordenador.id"]),
        sa.PrimaryKeyConstraint("id"),
        schema="calendario",
    )
    op.create_index(
        "ix_ingest_snapshot_semestre_status",
        "ingest_snapshot",
        ["semestre_id", "status"],
        unique=False,
        schema="calendario",
    )

    op.create_table(
        "grade_celula",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("ingest_snapshot_id", sa.UUID(), nullable=False),
        sa.Column("turma_id", sa.UUID(), nullable=False),
        sa.Column("dia", sa.Integer(), nullable=False),
        sa.Column("tempo", sa.Integer(), nullable=False),
        sa.Column("disciplina", sa.String(length=32), nullable=False),
        sa.Column("professor", sa.String(length=128), nullable=False),
        sa.ForeignKeyConstraint(["ingest_snapshot_id"], ["calendario.ingest_snapshot.id"]),
        sa.ForeignKeyConstraint(["turma_id"], ["calendario.turma.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "ingest_snapshot_id",
            "turma_id",
            "dia",
            "tempo",
            name="uq_grade_celula_snapshot_turma_slot",
        ),
        schema="calendario",
    )
    op.create_index(
        "ix_grade_celula_snapshot_id",
        "grade_celula",
        ["ingest_snapshot_id"],
        unique=False,
        schema="calendario",
    )


def downgrade() -> None:
    op.drop_index("ix_grade_celula_snapshot_id", table_name="grade_celula", schema="calendario")
    op.drop_table("grade_celula", schema="calendario")
    op.drop_index("ix_ingest_snapshot_semestre_status", table_name="ingest_snapshot", schema="calendario")
    op.drop_table("ingest_snapshot", schema="calendario")
    op.execute("DROP TYPE IF EXISTS ingestsourceformat")
    op.execute("DROP TYPE IF EXISTS ingestsnapshotstatus")
