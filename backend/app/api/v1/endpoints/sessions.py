"""
FastAPI endpoints untuk operasi sessions.
CRUD operations untuk tabel sessions wawancara.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models.session import Session
from app.schemas.session import SessionCreate, SessionUpdate, SessionResponse, SessionListItem
from app.api.v1.endpoints.profiles import get_current_user_id


router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get("/", response_model=List[SessionListItem])
async def get_all_sessions(
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Dapatkan semua sesi wawancara untuk user yang login.
    """
    result = await db.execute(
        select(Session)
        .where(Session.user_id == current_user_id)
        .order_by(Session.tanggal_dibuat.desc())
    )
    sessions = result.scalars().all()
    return sessions


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Dapatkan detail sesi wawancara berdasarkan ID.
    """
    result = await db.execute(
        select(Session).where(
            Session.id == session_id,
            Session.user_id == current_user_id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesi tidak ditemukan"
        )
    
    return session


@router.post("/", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Buat sesi wawancara baru.
    """
    # Gunakan user_id dari token jika tidak disediakan
    user_id = session_data.user_id or current_user_id
    
    new_session = Session(
        user_id=user_id,
        **session_data.model_dump(exclude={'user_id'})
    )
    
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    return new_session


@router.patch("/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: uuid.UUID,
    session_data: SessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Update sesi wawancara.
    """
    result = await db.execute(
        select(Session).where(
            Session.id == session_id,
            Session.user_id == current_user_id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesi tidak ditemukan"
        )
    
    # Update field yang disediakan
    update_data = session_data.model_dump(exclude_unset=True)
    
    # Set tanggal_selesai jika status berubah menjadi completed
    if update_data.get('status') == 'completed' and not session.tanggal_selesai:
        update_data['tanggal_selesai'] = datetime.utcnow()
    
    for key, value in update_data.items():
        setattr(session, key, value)
    
    await db.commit()
    await db.refresh(session)
    
    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Hapus sesi wawancara.
    """
    result = await db.execute(
        select(Session).where(
            Session.id == session_id,
            Session.user_id == current_user_id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesi tidak ditemukan"
        )
    
    await db.delete(session)
    await db.commit()
    
    return None


@router.post("/{session_id}/start", response_model=SessionResponse)
async def start_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Mulai sesi wawancara (ubah status ke ongoing).
    """
    result = await db.execute(
        select(Session).where(
            Session.id == session_id,
            Session.user_id == current_user_id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesi tidak ditemukan"
        )
    
    session.status = "ongoing"
    session.pertanyaan_ke = 0
    
    await db.commit()
    await db.refresh(session)
    
    return session


@router.post("/{session_id}/complete", response_model=SessionResponse)
async def complete_session(
    session_id: uuid.UUID,
    skor_akhir: int = None,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Selesaikan sesi wawancara dan hitung skor.
    """
    result = await db.execute(
        select(Session).where(
            Session.id == session_id,
            Session.user_id == current_user_id
        )
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sesi tidak ditemukan"
        )
    
    session.status = "completed"
    session.tanggal_selesai = datetime.utcnow()
    
    if skor_akhir is not None:
        session.skor_akhir = min(max(skor_akhir, 0), 100)
    
    await db.commit()
    await db.refresh(session)
    
    return session