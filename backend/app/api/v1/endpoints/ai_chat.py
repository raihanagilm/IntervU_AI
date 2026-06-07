"""
FastAPI endpoints untuk AI chat dan wawancara.
Endpoint untuk berinteraksi dengan LLM (Groq/Gemini) selama sesi wawancara.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any, Optional
import uuid

from app.core.database import get_db
from app.models.session import Session
from app.models.user import Profile
from app.api.v1.endpoints.profiles import get_current_user_id
from app.services.ai_service import ai_service


router = APIRouter(prefix="/ai", tags=["AI Chat"])


@router.post("/chat")
async def chat_with_ai(
    message: str = Body(..., embed=True),
    session_id: Optional[uuid.UUID] = Body(None, embed=True),
    conversation_history: Optional[List[Dict[str, str]]] = Body(None, embed=True),
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Kirim pesan ke AI dan dapatkan respons.
    Digunakan selama sesi wawancara untuk interaksi real-time.
    """
    # Ambil context dari session jika session_id disediakan
    context = {}
    if session_id:
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
        
        # Tambahkan context dari session
        context = {
            "posisi": session.posisi,
            "level": session.level,
            "bahasa": session.bahasa
        }
    
    # Get user profile untuk context tambahan
    profile_result = await db.execute(
        select(Profile).where(Profile.id == current_user_id)
    )
    profile = profile_result.scalar_one_or_none()
    
    if profile and profile.data_cv:
        context["data_cv"] = profile.data_cv
    
    # Call AI service
    ai_response = ai_service.chat(
        message=message,
        conversation_history=conversation_history,
        context=context
    )
    
    return {
        "message": ai_response,
        "session_id": str(session_id) if session_id else None,
        "user_message": message,
        "metadata": {
            "model": "groq-llama2/gemini-pro",
            "context_used": bool(context)
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
    Menggunakan LangChain + Groq/Gemini untuk generate pertanyaan custom.
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
    
    # Get user profile untuk data_cv
    profile_result = await db.execute(
        select(Profile).where(Profile.id == current_user_id)
    )
    profile = profile_result.scalar_one_or_none()
    
    data_cv = profile.data_cv if profile else None
    
    # Generate questions using AI service
    questions = ai_service.generate_interview_questions(
        posisi=session.posisi,
        level=session.level,
        bahasa=session.bahasa,
        data_cv=data_cv,
        total_questions=session.total_pertanyaan
    )
    
    return {
        "session_id": str(session_id),
        "questions": questions,
        "total": len(questions),
        "generated_by": "AI (Groq/Gemini)"
    }


@router.post("/evaluate-answer")
async def evaluate_answer(
    session_id: uuid.UUID,
    question_id: int,
    answer: str,
    question_text: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Evaluasi jawaban pengguna menggunakan AI.
    Mengembalikan skor dan feedback konstruktif.
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
    
    # Get question text dari session atau parameter
    question = question_text or f"Pertanyaan {question_id}"
    if session.pertanyaan and len(session.pertanyaan) >= question_id:
        question = session.pertanyaan[question_id - 1].get("question", question)
    
    # Get user profile
    profile_result = await db.execute(
        select(Profile).where(Profile.id == current_user_id)
    )
    profile = profile_result.scalar_one_or_none()
    
    data_cv = profile.data_cv if profile else None
    
    # Evaluate using AI service
    evaluation = ai_service.evaluate_answer(
        question=question,
        answer=answer,
        posisi=session.posisi,
        level=session.level,
        bahasa=session.bahasa,
        data_cv=data_cv
    )
    
    return {
        "session_id": str(session_id),
        "question_id": question_id,
        "evaluation": evaluation,
        "evaluated_by": "AI (Groq/Gemini)"
    }