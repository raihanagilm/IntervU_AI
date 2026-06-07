"""
Konfigurasi aplikasi untuk IntervU AI.
Membaca semua environment variables dari file .env menggunakan Pydantic Settings.
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Class untuk mengelola semua konfigurasi aplikasi.
    Semua field akan otomatis dibaca dari environment variables atau file .env.
    """
    
    # ==========================================
    # SUPABASE
    # ==========================================
    supabase_url: str = "https://brecmcrdeiwevthcxgam.supabase.co"
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""
    database_url: str = ""
    
    # ==========================================
    # GOOGLE OAUTH
    # ==========================================
    google_client_id: str = ""
    google_client_secret: str = ""
    
    # ==========================================
    # LLM APIs
    # ==========================================
    groq_api_key: str = ""
    gemini_api_key: str = ""
    
    # ==========================================
    # CLOUDINARY
    # ==========================================
    cloudinary_url: str = ""
    cloudinary_cloud_name: str = ""
    cloudinary_api_key: str = ""
    cloudinary_api_secret: str = ""
    
    # ==========================================
    # APP CONFIG
    # ==========================================
    app_env: str = "development"
    app_debug: bool = True
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Instance global yang bisa di-import di seluruh aplikasi
settings = Settings()