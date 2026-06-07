"""
FastAPI endpoints untuk AI chat dan wawancara.
Endpoint untuk berinteraksi dengan LLM (Groq/Gemini) selama sesi wawancara.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.core.database import get_db
from app.models.session import Session
from app.api.v1.endpoints.profiles import get_current_user_id


router = APIRouter(prefix="/ai", tags=["AI Chat"])


@router.post("/chat")
async def chat_with_ai(
    message: str,
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Kirim pesan ke AI dan dapatkan respons.
    Digunakan selama sesi wawancara untuk interaksi real-time.
    
    TODO: Implementasi LangChain dengan Groq/Gemini
    """
    # Verifikasi sesi ada dan milik user
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
    
    # TODO: Implementasi actual AI chat menggunakan LangChain
    # Untuk sekarang return dummy response
    return {
        "message": "AI response placeholder",
        "session_id": str(session_id),
        "user_message": message,
        "ai_response": "Halo! Saya AI interviewer Anda. Silakan jawab pertanyaan berikutnya dengan percaya diri.",
        "metadata": {
            "model": "groq-llama2",
            "tokens_used": 0,
            "response_time_ms": 0
        }
    }


@router.post("/generate-questions")
async def generate_questions(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Generate daftar pertanyaan wawancara berdasarkan profil user dan posisi target.
    
    TODO: Implementasi LangChain untuk generate pertanyaan custom
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
    
    # TODO: Generate questions using LangChain based on:
    # - session.posisi
    # - session.level
    # - session.bahasa
    # - user.data_cv
    
    # Dummy questions untuk development
    questions = [
        {
            "id": 1,
            "question": "Bisa ceritakan tentang pengalaman kerja Anda yang paling relevan?",
            "category": "experience"
        },
        {
            "id": 2,
            "question": "Apa kelebihan dan kekurangan Anda dalam bekerja?",
            "category": "self-awareness"
        },
        {
            "id": 3,
            "question": "Mengapa Anda tertarik dengan posisi ini?",
            "category": "motivation"
        },
        {
            "id": 4,
            "question": "Bagaimana cara Anda menangani tekanan dalam pekerjaan?",
            "category": "soft-skills"
        },
        {
            "id": 5,
            "question": "Di mana Anda melihat diri Anda dalam 5 tahun ke depan?",
            "category": "career-goals"
        }
    ]
    
    return {
        "session_id": str(session_id),
        "questions": questions,
        "total": len(questions)
    }


@router.post("/evaluate-answer")
async def evaluate_answer(
    session_id: uuid.UUID,
    question_id: int,
    answer: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Evaluasi jawaban pengguna menggunakan AI.
    Mengembalikan skor dan feedback konstruktif.
    
    TODO: Implementasi LangChain untuk evaluasi jawaban
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
    
    # TODO: Evaluate answer using LangChain
    # Return score (0-100) and detailed feedback
    
    # Dummy evaluation untuk development
    return {
        "session_id": str(session_id),
        "question_id": question_id,
        "score": 75,
        "feedback": "Jawaban Anda cukup baik. Coba berikan contoh lebih spesifik untuk memperkuat argumen.",
        "strengths": ["Struktur jawaban jelas", "Menunjukkan antusiasme"],
        "improvements": ["Berikan contoh konkret", "Gunakan metode STAR"],
        "metadata": {
            "model": "gemini-pro",
            "evaluation_time_ms": 0
        }
    }