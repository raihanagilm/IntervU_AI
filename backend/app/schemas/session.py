"""
Pydantic schemas untuk tabel sessions.
Digunakan untuk validasi input dan serialisasi output API sesi wawancara.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


# ==========================================
# Schema untuk Sessions
# ==========================================
class SessionBase(BaseModel):
    """Schema dasar untuk session - field umum untuk create dan update."""
    judul: str = Field(..., min_length=3, max_length=200, description="Judul sesi wawancara")
    deskripsi: Optional[str] = Field(None, description="Deskripsi sesi")
    posisi: str = Field(..., min_length=2, max_length=100, description="Posisi yang diwawancarai")
    level: str = Field(default="mid", pattern="^(intern|junior|mid|senior|lead)$", description="Level posisi")
    bahasa: str = Field(default="id", pattern="^(id|en)$", description="Bahasa wawancara")
    total_pertanyaan: int = Field(default=5, ge=1, le=20, description="Total pertanyaan dalam sesi")


class SessionCreate(SessionBase):
    """Schema untuk membuat session baru."""
    user_id: Optional[uuid.UUID] = Field(None, description="User ID (opsional, diambil dari token jika tidak disediakan)")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "judul": "Simulasi Wawancara Software Engineer",
            "deskripsi": "Latihan wawancara untuk posisi backend developer",
            "posisi": "Software Engineer",
            "level": "mid",
            "bahasa": "id",
            "total_pertanyaan": 5
        }
    })


class SessionUpdate(BaseModel):
    """Schema untuk mengupdate session - semua field optional."""
    judul: Optional[str] = Field(None, min_length=3, max_length=200)
    deskripsi: Optional[str] = Field(None)
    posisi: Optional[str] = Field(None, min_length=2, max_length=100)
    level: Optional[str] = Field(None, pattern="^(intern|junior|mid|senior|lead)$")
    bahasa: Optional[str] = Field(None, pattern="^(id|en)$")
    status: Optional[str] = Field(None, pattern="^(draft|ongoing|completed|cancelled)$")
    pertanyaan_ke: Optional[int] = Field(None, ge=0)
    total_pertanyaan: Optional[int] = Field(None, ge=1, le=20)
    skor_akhir: Optional[int] = Field(None, ge=0, le=100)
    pertanyaan: Optional[List[Dict[str, Any]]] = Field(None)
    jawaban: Optional[List[Dict[str, Any]]] = Field(None)
    feedback: Optional[Dict[str, Any]] = Field(None)
    metadata_sesi: Optional[Dict[str, Any]] = Field(None)
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "status": "ongoing",
            "pertanyaan_ke": 2
        }
    })


class SessionResponse(SessionBase):
    """Schema untuk response session - termasuk semua metadata."""
    id: uuid.UUID = Field(..., description="Session ID")
    user_id: uuid.UUID = Field(..., description="User ID")
    status: str = Field(..., description="Status sesi")
    pertanyaan_ke: int = Field(..., description="Index pertanyaan saat ini")
    skor_akhir: Optional[int] = Field(None, description="Skor akhir (0-100)")
    pertanyaan: List[Dict[str, Any]] = Field(default_factory=list, description="List pertanyaan")
    jawaban: List[Dict[str, Any]] = Field(default_factory=list, description="List jawaban")
    feedback: Dict[str, Any] = Field(default_factory=dict, description="Feedback AI")
    metadata_sesi: Dict[str, Any] = Field(default_factory=dict, description="Metadata tambahan")
    tanggal_dibuat: datetime = Field(..., description="Waktu pembuatan sesi")
    tanggal_diperbarui: datetime = Field(..., description="Waktu update terakhir")
    tanggal_selesai: Optional[datetime] = Field(None, description="Waktu sesi selesai")
    
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
            "judul": "Simulasi Wawancara Software Engineer",
            "posisi": "Software Engineer",
            "level": "mid",
            "bahasa": "id",
            "status": "ongoing",
            "pertanyaan_ke": 2,
            "total_pertanyaan": 5,
            "tanggal_dibuat": "2024-01-01T00:00:00Z",
            "tanggal_diperbarui": "2024-01-01T00:00:00Z"
        }
    })


class SessionListItem(BaseModel):
    """Schema ringkas untuk list sessions."""
    id: uuid.UUID
    judul: str
    posisi: str
    status: str
    skor_akhir: Optional[int]
    tanggal_dibuat: datetime
    tanggal_selesai: Optional[datetime]
    
    model_config = ConfigDict(from_attributes=True)