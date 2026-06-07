"""
Konfigurasi database untuk IntervU AI.
Menggunakan SQLAlchemy dengan asyncpg untuk koneksi async ke PostgreSQL/Supabase.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings


# Create async engine untuk koneksi ke Supabase
# pool_pre_ping=True memastikan koneksi yang dropped akan di-reconnect otomatis
engine = create_async_engine(
    settings.database_url,
    echo=settings.app_debug,  # Log SQL queries jika debug mode
    pool_pre_ping=True,
)

# Session factory untuk membuat session database
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Mencegah error saat akses objek setelah commit
)


class Base(DeclarativeBase):
    """
    Base class untuk semua SQLAlchemy models.
    Semua model harus inherit dari class ini.
    """
    pass


async def get_db():
    """
    Dependency untuk mendapatkan database session.
    Digunakan di FastAPI endpoints untuk inject database session.
    
    Usage:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Inisialisasi database - membuat semua tabel berdasarkan models.
    Dipanggil sekali saat aplikasi start.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)