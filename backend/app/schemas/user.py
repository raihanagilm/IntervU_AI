"""
Pydantic schemas untuk tabel profiles.
Digunakan untuk validasi input dan serialisasi output API.
"""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import date, datetime
import uuid


# ==========================================
# Schema untuk CV Data (JSONB)
# ==========================================
class PendidikanSchema(BaseModel):
    """Schema untuk setiap entri pendidikan dalam CV."""
    institusi: str = Field(..., description="Nama institusi pendidikan")
    jurusan: str = Field(..., description="Jurusan/program studi")
    gelar: Optional[str] = Field(None, description="Gelar yang diperoleh")
    tanggal_mulai: Optional[date] = Field(None, description="Tanggal mulai")
    tanggal_selesai: Optional[date] = Field(None, description="Tanggal selesai")
    ipk: Optional[str] = Field(None, description="IPK (jika ada)")
    deskripsi: Optional[str] = Field(None, description="Deskripsi tambahan")


class PengalamanKerjaSchema(BaseModel):
    """Schema untuk setiap entri pengalaman kerja dalam CV."""
    perusahaan: str = Field(..., description="Nama perusahaan")
    posisi: str = Field(..., description="Posisi/jabatan")
    lokasi: Optional[str] = Field(None, description="Lokasi kerja")
    tanggal_mulai: Optional[date] = Field(None, description="Tanggal mulai")
    tanggal_selesai: Optional[date] = Field(None, description="Tanggal selesai")
    masih_bekerja: bool = Field(default=False, description="Apakah masih bekerja di sini")
    deskripsi: Optional[str] = Field(None, description="Deskripsi tanggung jawab dan pencapaian")


class PengalamanOrganisasiSchema(BaseModel):
    """Schema untuk setiap entri pengalaman organisasi dalam CV."""
    organisasi: str = Field(..., description="Nama organisasi")
    posisi: str = Field(..., description="Posisi/jabatan dalam organisasi")
    tanggal_mulai: Optional[date] = Field(None, description="Tanggal mulai")
    tanggal_selesai: Optional[date] = Field(None, description="Tanggal selesai")
    deskripsi: Optional[str] = Field(None, description="Deskripsi kegiatan dan pencapaian")


class KeahlianSchema(BaseModel):
    """Schema untuk keahlian/skill."""
    nama: str = Field(..., description="Nama keahlian")
    kategori: Optional[str] = Field(None, description="Kategori keahlian (technical, soft skill, dll)")
    level: Optional[str] = Field("intermediate", description="Level keahlian: beginner, intermediate, advanced, expert")


class TautanProfesionalSchema(BaseModel):
    """Schema untuk tautan profesional."""
    platform: str = Field(..., description="Nama platform (LinkedIn, GitHub, dll)")
    url: str = Field(..., description="URL profil")


class CvDataSchema(BaseModel):
    """
    Schema utama untuk data_cv (JSONB).
    Merepresentasikan struktur CV yang terparse.
    """
    ringkasan_profesional: Optional[str] = Field(None, description="Ringkasan profesional/career objective")
    tautan_profesional: List[TautanProfesionalSchema] = Field(default_factory=list, description="Daftar tautan profesional")
    pendidikan: List[PendidikanSchema] = Field(default_factory=list, description="Riwayat pendidikan")
    pengalaman_kerja: List[PengalamanKerjaSchema] = Field(default_factory=list, description="Riwayat pengalaman kerja")
    pengalaman_organisasi: List[PengalamanOrganisasiSchema] = Field(default_factory=list, description="Riwayat pengalaman organisasi")
    keahlian: List[KeahlianSchema] = Field(default_factory=list, description="Daftar keahlian")
    
    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Schema untuk Profiles
# ==========================================
class ProfileBase(BaseModel):
    """Schema dasar untuk profile - field umum untuk create dan update."""
    nama_lengkap: str = Field(..., min_length=2, max_length=100, description="Nama lengkap pengguna")
    email: EmailStr = Field(..., description="Email pengguna")
    telepon: Optional[str] = Field(None, max_length=20, description="Nomor telepon")
    tanggal_lahir: Optional[date] = Field(None, description="Tanggal lahir")
    jenis_kelamin: Optional[str] = Field(None, pattern="^(pria|wanita|prefer_tidak_menyebutkan)$", description="Jenis kelamin")
    url_avatar: Optional[str] = Field(None, description="URL foto avatar")
    url_foto_cv: Optional[str] = Field(None, description="URL foto CV")
    penyedia_auth: str = Field(default="google", pattern="^(google|email)$", description="Provider autentikasi")
    posisi_target: Optional[str] = Field(None, max_length=100, description="Posisi pekerjaan yang ditargetkan")
    bahasa_preferensi: str = Field(default="id", pattern="^(id|en)$", description="Bahasa preferensi")
    data_cv: CvDataSchema = Field(default_factory=CvDataSchema, description="Data CV terstruktur")


class ProfileCreate(ProfileBase):
    """Schema untuk membuat profile baru."""
    id: Optional[uuid.UUID] = Field(None, description="User ID dari Supabase auth (opsional, akan digenerate jika tidak ada)")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "nama_lengkap": "John Doe",
            "email": "john.doe@example.com",
            "posisi_target": "Software Engineer",
            "bahasa_preferensi": "id",
            "data_cv": {
                "ringkasan_profesional": "Software engineer dengan 3 tahun pengalaman...",
                "pendidikan": [],
                "pengalaman_kerja": [],
                "keahlian": []
            }
        }
    })


class ProfileUpdate(BaseModel):
    """Schema untuk mengupdate profile - semua field optional."""
    nama_lengkap: Optional[str] = Field(None, min_length=2, max_length=100)
    telepon: Optional[str] = Field(None, max_length=20)
    tanggal_lahir: Optional[date] = Field(None)
    jenis_kelamin: Optional[str] = Field(None, pattern="^(pria|wanita|prefer_tidak_menyebutkan)$")
    url_avatar: Optional[str] = Field(None)
    url_foto_cv: Optional[str] = Field(None)
    posisi_target: Optional[str] = Field(None, max_length=100)
    bahasa_preferensi: Optional[str] = Field(None, pattern="^(id|en)$")
    data_cv: Optional[CvDataSchema] = Field(None)
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "posisi_target": "Senior Software Engineer",
            "bahasa_preferensi": "en"
        }
    })


class ProfileResponse(ProfileBase):
    """Schema untuk response profile - termasuk metadata."""
    id: uuid.UUID = Field(..., description="User ID")
    tanggal_dibuat: datetime = Field(..., description="Waktu pembuatan profile")
    tanggal_diperbarui: datetime = Field(..., description="Waktu update terakhir")
    
    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "nama_lengkap": "John Doe",
            "email": "john.doe@example.com",
            "posisi_target": "Software Engineer",
            "bahasa_preferensi": "id",
            "tanggal_dibuat": "2024-01-01T00:00:00Z",
            "tanggal_diperbarui": "2024-01-01T00:00:00Z"
        }
    })