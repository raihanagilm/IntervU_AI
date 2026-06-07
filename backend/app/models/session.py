"""
SQLAlchemy model untuk tabel sessions.
Menyimpan data sesi wawancara pengguna.
"""
from sqlalchemy import String, Text, DateTime, func, ForeignKey, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from app.core.database import Base
import uuid


class Session(Base):
    """
    Model untuk tabel sessions.
    
    Tabel ini menyimpan setiap sesi wawancara yang dilakukan pengguna,
    termasuk pertanyaan, jawaban, dan feedback dari AI.
    """
    __tablename__ = "sessions"
    
    # Primary Key - UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key untuk sesi wawancara"
    )
    
    # Foreign Key ke profiles
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Referensi ke user yang melakukan sesi"
    )
    
    # Informasi Sesi
    judul: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Judul sesi wawancara"
    )
    
    deskripsi: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="Deskripsi sesi"
    )
    
    posisi: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Posisi yang diwawancarai"
    )
    
    level: Mapped[str] = mapped_column(
        String(50),
        default="mid",
        comment="Level posisi: intern, junior, mid, senior, lead"
    )
    
    bahasa: Mapped[str] = mapped_column(
        String(5),
        default="id",
        comment="Bahasa wawancara: 'id' atau 'en'"
    )
    
    # Status dan Progress
    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        comment="Status: draft, ongoing, completed, cancelled"
    )
    
    pertanyaan_ke: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="Index pertanyaan saat ini"
    )
    
    total_pertanyaan: Mapped[int] = mapped_column(
        Integer,
        default=5,
        comment="Total pertanyaan dalam sesi"
    )
    
    skor_akhir: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
        comment="Skor akhir (0-100)"
    )
    
    # Data Sesi dalam JSONB
    pertanyaan: Mapped[dict] = mapped_column(
        JSONB,
        default=list,
        comment="List pertanyaan yang diajukan"
    )
    
    jawaban: Mapped[dict] = mapped_column(
        JSONB,
        default=list,
        comment="List jawaban pengguna"
    )
    
    feedback: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        comment="Feedback AI untuk setiap jawaban"
    )
    
    metadata_sesi: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        comment="Metadata tambahan (durasi, model AI, dll)"
    )
    
    # Timestamps
    tanggal_dibuat: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Waktu pembuatan sesi"
    )
    
    tanggal_diperbarui: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Waktu update terakhir"
    )
    
    tanggal_selesai: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        comment="Waktu sesi selesai"
    )
    
    # Relationships
    profile = relationship("Profile", back_populates="sessions")
    
    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user_id={self.user_id}, judul='{self.judul}', status='{self.status}')>"