"""
Main entry point untuk FastAPI application IntervU AI.
Menginisialisasi app, middleware, dan routers.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import init_db
from app.api.v1.endpoints import profiles, sessions, ai_chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager untuk setup dan shutdown aplikasi.
    Dipanggil saat aplikasi start dan stop.
    """
    # Startup: Inisialisasi database
    print("🚀 Starting IntervU AI API...")
    await init_db()
    print("✅ Database initialized")
    yield
    # Shutdown: Cleanup jika diperlukan
    print("👋 Shutting down IntervU AI API...")


# Initialize FastAPI app
app = FastAPI(
    title="IntervU AI API",
    description="""
## API untuk Aplikasi Simulasi Wawancara Berbasis AI

IntervU AI membantu Anda mempersiapkan wawancara kerja dengan simulasi berbasis AI.

### Fitur Utama:
- **Profile Management**: Kelola profil dan CV Anda
- **Session Management**: Buat dan kelola sesi wawancara
- **AI Chat**: Interaksi real-time dengan AI interviewer
- **Smart Evaluation**: Feedback otomatis dari AI untuk setiap jawaban

### Tech Stack:
- Backend: FastAPI + SQLAlchemy Async + PostgreSQL (Supabase)
- AI: LangChain + Groq/Gemini
- Storage: Cloudinary untuk upload gambar/CV
    """,
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - allow frontend React akses API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite default port
        "http://localhost:3000",  # Create React App default port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Include routers dari v1 endpoints
app.include_router(profiles.router, prefix="/api/v1")
app.include_router(sessions.router, prefix="/api/v1")
app.include_router(ai_chat.router, prefix="/api/v1")


@app.get("/")
async def root():
    """
    Root endpoint - informasi umum API.
    """
    return {
        "message": "Selamat datang di IntervU AI API!",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",  # Swagger UI
        "redoc": "/redoc"  # ReDoc
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint untuk monitoring.
    """
    return {
        "status": "healthy",
        "environment": settings.app_env,
        "debug": settings.app_debug
    }


# Debug endpoint untuk test (hanya development)
if settings.app_debug:
    @app.get("/debug/config")
    async def debug_config():
        """
        Debug endpoint untuk melihat konfigurasi (tanpa secrets).
        HANYA AKTIF DI DEVELOPMENT MODE!
        """
        return {
            "app_env": settings.app_env,
            "app_debug": settings.app_debug,
            "supabase_url": settings.supabase_url,
            "has_groq_key": bool(settings.groq_api_key),
            "has_gemini_key": bool(settings.gemini_api_key),
            "has_cloudinary": bool(settings.cloudinary_cloud_name),
        }