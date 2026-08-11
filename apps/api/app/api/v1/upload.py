from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.db.enums import ArquivoTipo
from app.db.models import ArquivoEntrada, Semestre
from app.schemas.ingest import UploadResponse
from app.services.blob_storage import save_bytes

router = APIRouter(prefix="/semestres", tags=["upload"])

_TIPO_MAP = {
    "grade": ArquivoTipo.grade,
    "modelo": ArquivoTipo.modelo,
    "siglas": ArquivoTipo.siglas,
    "simulados": ArquivoTipo.simulados,
}


@router.post("/{semestre_id}/upload/{tipo}", response_model=UploadResponse)
async def upload_entrada(
    semestre_id: uuid.UUID,
    tipo: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> UploadResponse:
    if tipo not in _TIPO_MAP:
        raise HTTPException(status_code=400, detail=f"tipo inválido: {tipo}")

    semestre = db.get(Semestre, semestre_id)
    if semestre is None:
        raise HTTPException(status_code=404, detail="semestre não encontrado")

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="arquivo vazio")

    filename = file.filename or "upload.bin"
    blob_path, checksum = save_bytes(
        data,
        prefix=f"semestres/{semestre_id}/{tipo}",
        filename=filename,
    )

    arquivo_tipo = _TIPO_MAP[tipo]
    existing = db.scalar(
        select(ArquivoEntrada).where(
            ArquivoEntrada.semestre_id == semestre_id,
            ArquivoEntrada.tipo == arquivo_tipo,
        )
    )
    if existing:
        existing.blob_path = blob_path
        existing.checksum = checksum
        db.commit()
        db.refresh(existing)
        return UploadResponse(
            arquivo_id=existing.id,
            tipo=tipo,
            blob_path=blob_path,
            checksum=checksum,
        )

    arquivo = ArquivoEntrada(
        semestre_id=semestre_id,
        tipo=arquivo_tipo,
        blob_path=blob_path,
        checksum=checksum,
    )
    db.add(arquivo)
    db.commit()
    db.refresh(arquivo)
    return UploadResponse(
        arquivo_id=arquivo.id,
        tipo=tipo,
        blob_path=blob_path,
        checksum=checksum,
    )
