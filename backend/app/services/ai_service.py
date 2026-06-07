"""
AI Service untuk IntervU AI.
Menangani interaksi dengan LLM (Groq/Gemini) menggunakan LangChain.
"""
from typing import Optional, Dict, Any, List
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from app.core.config import settings


class AIService:
    """
    Service class untuk berinteraksi dengan AI models.
    Mendukung Groq (Llama2) dan Google Gemini.
    """
    
    def __init__(self):
        self.groq_client = None
        self.gemini_client = None
        
        # Initialize Groq client jika API key tersedia
        if settings.groq_api_key:
            self.groq_client = ChatGroq(
                api_key=settings.groq_api_key,
                model_name="llama2-70b-4096",
                temperature=0.7,
            )
        
        # Initialize Gemini client jika API key tersedia
        if settings.gemini_api_key:
            self.gemini_client = ChatGoogleGenerativeAI(
                api_key=settings.gemini_api_key,
                model="gemini-pro",
                temperature=0.7,
            )
    
    def generate_interview_questions(
        self,
        posisi: str,
        level: str,
        bahasa: str = "id",
        data_cv: Optional[Dict] = None,
        total_questions: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Generate daftar pertanyaan wawancara berdasarkan profil dan posisi.
        
        Args:
            posisi: Posisi pekerjaan yang dilamar
            level: Level posisi (intern, junior, mid, senior, lead)
            bahasa: Bahasa pertanyaan ('id' atau 'en')
            data_cv: Data CV terstruktur
            total_questions: Jumlah pertanyaan yang akan digenerate
            
        Returns:
            List of questions dengan format:
            [
                {
                    "id": 1,
                    "question": "...",
                    "category": "experience|technical|behavioral|motivation|career-goals"
                },
                ...
            ]
        """
        # Gunakan Groq sebagai default, fallback ke Gemini
        client = self.groq_client or self.gemini_client
        
        if not client:
            return self._get_dummy_questions(posisi, level, bahasa, total_questions)
        
        # Build prompt untuk generate questions
        prompt = self._build_questions_prompt(
            posisi, level, bahasa, data_cv, total_questions
        )
        
        try:
            response = client.invoke([HumanMessage(content=prompt)])
            # Parse response menjadi list questions
            questions = self._parse_questions_response(response.content)
            return questions
        except Exception as e:
            print(f"Error generating questions: {e}")
            return self._get_dummy_questions(posisi, level, bahasa, total_questions)
    
    def evaluate_answer(
        self,
        question: str,
        answer: str,
        posisi: str,
        level: str,
        bahasa: str = "id",
        data_cv: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Evaluasi jawaban pengguna dan berikan feedback.
        
        Args:
            question: Pertanyaan yang diajukan
            answer: Jawaban pengguna
            posisi: Posisi pekerjaan
            level: Level posisi
            bahasa: Bahasa ('id' atau 'en')
            data_cv: Data CV terstruktur
            
        Returns:
            {
                "score": 0-100,
                "feedback": "Feedback detail",
                "strengths": ["list kekuatan"],
                "improvements": ["list perbaikan"],
                "suggested_answer": "Contoh jawaban ideal"
            }
        """
        client = self.groq_client or self.gemini_client
        
        if not client:
            return self._get_dummy_evaluation()
        
        # Build prompt untuk evaluasi
        prompt = self._build_evaluation_prompt(
            question, answer, posisi, level, bahasa, data_cv
        )
        
        try:
            response = client.invoke([HumanMessage(content=prompt)])
            evaluation = self._parse_evaluation_response(response.content)
            return evaluation
        except Exception as e:
            print(f"Error evaluating answer: {e}")
            return self._get_dummy_evaluation()
    
    def chat(
        self,
        message: str,
        conversation_history: List[Dict[str, str]] = None,
        context: Optional[Dict] = None
    ) -> str:
        """
        Chat biasa dengan AI interviewer.
        
        Args:
            message: Pesan dari user
            conversation_history: Riwayat percakapan
            context: Konteks tambahan (posisi, CV, dll)
            
        Returns:
            Response dari AI
        """
        client = self.groq_client or self.gemini_client
        
        if not client:
            return "Maaf, layanan AI sedang tidak tersedia."
        
        messages = []
        
        # Add system message dengan context
        system_prompt = self._build_system_prompt(context)
        messages.append(SystemMessage(content=system_prompt))
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-10:]:  # Last 10 messages
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        # Add current message
        messages.append(HumanMessage(content=message))
        
        try:
            response = client.invoke(messages)
            return response.content
        except Exception as e:
            print(f"Error in chat: {e}")
            return "Maaf, terjadi kesalahan saat memproses pesan Anda."
    
    def _build_questions_prompt(
        self,
        posisi: str,
        level: str,
        bahasa: str,
        data_cv: Optional[Dict],
        total_questions: int
    ) -> str:
        """Build prompt untuk generate pertanyaan wawancara."""
        lang_name = "Bahasa Indonesia" if bahasa == "id" else "English"
        
        cv_context = ""
        if data_cv:
            cv_context = f"""
            Informasi Kandidat:
            - Ringkasan: {data_cv.get('ringkasan_profesional', 'N/A')}
            - Pendidikan: {len(data_cv.get('pendidikan', []))} institusi
            - Pengalaman Kerja: {len(data_cv.get('pengalaman_kerja', []))} posisi
            - Keahlian: {', '.join([k['nama'] for k in data_cv.get('keahlian', [])[:5]])}
            """
        
        prompt = f"""
Anda adalah interviewer profesional yang sedang menyiapkan pertanyaan wawancara untuk posisi {posisi} level {level}.

{cv_context}

Tugas:
Buat {total_questions} pertanyaan wawancara yang relevan dan menantang dalam {lang_name}.

Kategori pertanyaan yang harus ada:
1. Experience (pengalaman kerja)
2. Technical/Role-specific (keahlian teknis)
3. Behavioral (situasional)
4. Motivation (motivasi dan ketertarikan)
5. Career Goals (tujuan karir)

Format output HARUS JSON array seperti ini:
[
  {{"id": 1, "question": "...", "category": "experience"}},
  {{"id": 2, "question": "...", "category": "technical"}},
  ...
]

Jangan tambahkan teks lain selain JSON array.
"""
        return prompt.strip()
    
    def _build_evaluation_prompt(
        self,
        question: str,
        answer: str,
        posisi: str,
        level: str,
        bahasa: str,
        data_cv: Optional[Dict]
    ) -> str:
        """Build prompt untuk evaluasi jawaban."""
        lang_name = "Bahasa Indonesia" if bahasa == "id" else "English"
        
        prompt = f"""
Anda adalah interviewer profesional yang sedang mengevaluasi jawaban kandidat.

Posisi: {posisi} (Level: {level})
Pertanyaan: {question}
Jawaban Kandidat: {answer}

Tugas:
Evaluasi jawaban ini secara objektif dan konstruktif dalam {lang_name}.

Berikan:
1. Score (0-100) berdasarkan:
   - Relevansi dengan pertanyaan
   - Struktur dan kejelasan
   - Contoh konkret yang diberikan
   - Kesesuaian dengan level posisi

2. Feedback detail yang membangun

3. Strengths (kekuatan jawaban)

4. Improvements (yang bisa diperbaiki)

5. Suggested answer (contoh jawaban ideal singkat)

Format output HARUS JSON seperti ini:
{{
  "score": 75,
  "feedback": "...",
  "strengths": ["...", "..."],
  "improvements": ["...", "..."],
  "suggested_answer": "..."
}}

Jangan tambahkan teks lain selain JSON.
"""
        return prompt.strip()
    
    def _build_system_prompt(self, context: Optional[Dict]) -> str:
        """Build system prompt untuk chat."""
        base_prompt = """Anda adalah AI interviewer profesional untuk IntervU AI. 
Tugas Anda adalah membantu kandidat mempersiapkan wawancara kerja dengan memberikan:
- Pertanyaan yang relevan dan menantang
- Feedback konstruktif dan detail
- Dorongan positif
- Tips dan saran perbaikan

Gaya komunikasi:
- Profesional namun ramah
- Supportive dan encouraging
- Objektif dalam evaluasi
- Jelas dan mudah dipahami"""

        if context:
            if context.get('posisi'):
                base_prompt += f"\n- Kandidat melamar posisi: {context['posisi']}"
            if context.get('level'):
                base_prompt += f"\n- Level: {context['level']}"
        
        return base_prompt
    
    def _parse_questions_response(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse response text menjadi list questions."""
        import json
        try:
            # Extract JSON from response
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                questions = json.loads(json_str)
                return questions
        except Exception as e:
            print(f"Error parsing questions: {e}")
        return []
    
    def _parse_evaluation_response(self, response_text: str) -> Dict[str, Any]:
        """Parse response text menjadi evaluation dict."""
        import json
        try:
            # Extract JSON from response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                evaluation = json.loads(json_str)
                return evaluation
        except Exception as e:
            print(f"Error parsing evaluation: {e}")
        return {}
    
    def _get_dummy_questions(
        self,
        posisi: str,
        level: str,
        bahasa: str,
        total_questions: int
    ) -> List[Dict[str, Any]]:
        """Return dummy questions jika AI tidak tersedia."""
        return [
            {"id": i+1, "question": f"Pertanyaan {i+1} untuk posisi {posisi}", "category": "general"}
            for i in range(min(total_questions, 5))
        ]
    
    def _get_dummy_evaluation(self) -> Dict[str, Any]:
        """Return dummy evaluation jika AI tidak tersedia."""
        return {
            "score": 70,
            "feedback": "Jawaban Anda cukup baik. Coba berikan contoh lebih spesifik.",
            "strengths": ["Struktur jelas", "Menunjukkan antusiasme"],
            "improvements": ["Berikan contoh konkret", "Gunakan metode STAR"],
            "suggested_answer": "Contoh: Pada pengalaman saya sebelumnya..."
        }


# Singleton instance
ai_service = AIService()