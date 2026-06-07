"""
SQLAlchemy model untuk tabel profiles.
Menyimpan data profil pengguna termasuk CV data dalam format JSONB.
"""
from sqlalchemy import Column, String, Date, CheckConstraint, ForeignKey, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import date, datetime
from app.core.database import Base
import uuid


class Profile(Base):
    """
    Model untuk tabel profiles.
    
    Tabel ini menyimpan informasi lengkap profil pengguna,
    termasuk data CV yang diparsing dalam format JSONB.
    """
    __tablename__ = "profiles"
    
    # Primary Key - UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Primary key, referensi ke auth.users Supabase"
    )
    
    # Informasi Pribadi
    nama_lengkap: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Nama lengkap pengguna"
    )
    
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        comment="Email pengguna (unique)"
    )
    
    telepon: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Nomor telepon"
    )
    
    tanggal_lahir: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        comment="Tanggal lahir"
    )
    
    jenis_kelamin: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
        comment="Jenis kelamin: pria, wanita, atau prefer_tidak_menyebutkan"
    )
    
    url_avatar: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="URL foto avatar di Cloudinary"
    )
    
    url_foto_cv: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        comment="URL foto CV di Cloudinary"
    )
    
    # Auth Provider
    penyedia_auth: Mapped[str] = mapped_column(
        String(20),
        default="google",
        comment="Provider autentikasi: google atau email"
    )
    
    # Preferensi Wawancara
    posisi_target: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Posisi pekerjaan yang ditargetkan"
    )
    
    bahasa_preferensi: Mapped[str] = mapped_column(
        String(5),
        default="id",
        comment="Bahasa preferensi: 'id' (Indonesia) atau 'en' (English)"
    )
    
    # Data CV dalam format JSONB
    data_cv: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
        comment="Data CV terstruktur dalam format JSONB"
    )
    
    # Timestamps
    tanggal_dibuat: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Waktu pembuatan record"
    )
    
    tanggal_diperbarui: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        comment="Waktu update terakhir"
    )
    
    # Relationships
    sessions = relationship("Session", back_populates="profile", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "jenis_kelamin IN ('pria', 'wanita', 'prefer_tidak_menyebutkan')",
            name="check_jenis_kelamin"
        ),
        CheckConstraint(
            "penyedia_auth IN ('google', 'email')",
            name="check_penyedia_auth"
        ),
        CheckConstraint(
            "bahasa_preferensi IN ('id', 'en')",
            name="check_bahasa_preferensi"
        ),
    )
    
    def __repr__(self) -> str:
        return f"<Profile(id={self.id}, nama_lengkap='{self.nama_lengkap}', email='{self.email}')>"