# IntervU AI - Simulasi Wawancara Kerja Berbasis AI

Platform simulasi wawancara kerja yang menggunakan AI untuk memberikan pengalaman interview realistis dengan feedback instan dan personalisasi.

## 🚀 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy Async** - Async ORM untuk database operations
- **PostgreSQL (Supabase)** - Database cloud
- **LangChain** - Framework untuk aplikasi LLM
- **Groq & Gemini** - LLM providers untuk AI interviewer
- **Cloudinary** - Cloud storage untuk gambar/CV
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **Vite** - Build tool modern
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client

## 📁 Struktur Project

```
/workspace
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/
│   │   │   ├── profiles.py      # CRUD profiles
│   │   │   ├── sessions.py      # CRUD sessions
│   │   │   └── ai_chat.py       # AI endpoints
│   │   ├── core/
│   │   │   ├── config.py        # App configuration
│   │   │   ├── database.py      # DB connection
│   │   │   └── security.py      # Auth utilities
│   │   ├── models/
│   │   │   ├── user.py          # Profile model
│   │   │   └── session.py       # Session model
│   │   ├── schemas/
│   │   │   ├── user.py          # Profile schemas
│   │   │   └── session.py       # Session schemas
│   │   └── main.py              # FastAPI app entry
│   ├── .env                     # Environment variables
│   └── requirements.txt         # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── components/ui/
    │   │   ├── Button.jsx       # Reusable button
    │   │   └── Card.jsx         # Reusable card
    │   ├── pages/
    │   │   ├── Home.jsx         # Landing page
    │   │   └── Interview.jsx    # Interview page (responsive)
    │   ├── App.jsx              # Main app component
    │   ├── main.jsx             # React entry point
    │   └── index.css            # Global styles + Tailwind
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── index.html
```

## 🔧 Setup & Installation

### Backend Setup

1. Navigate to backend folder:
```bash
cd /workspace/backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Update `.env` file dengan credentials Anda (sudah ada template)

5. Run development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend akan berjalan di: `http://localhost:8000`
API Docs (Swagger): `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend folder:
```bash
cd /workspace/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run development server:
```bash
npm run dev
```

Frontend akan berjalan di: `http://localhost:5173`

## 🎯 Fitur Utama

### 1. Profile Management
- Upload CV (gambar/PDF)
- Parse CV otomatis dengan AI
- Kelola data profil lengkap
- Support multi-bahasa (ID/EN)

### 2. Session Management
- Buat sesi wawancara custom
- Pilih posisi, level, dan bahasa
- Track progress sesi
- Riwayat sesi lengkap

### 3. AI Interviewer
- Pertanyaan kontekstual berdasarkan CV
- Real-time chat dengan AI
- Feedback instan per jawaban
- Skor evaluasi detail

### 4. Responsive Design
- **Mobile Portrait**: Full-screen camera dengan overlay chat
- **Desktop/Landscape**: Split screen (60% camera, 40% chat panel)
- Smooth transition saat rotate device
- Mobile-first approach

## 📱 Responsive Layout Demo

### Mobile Portrait (< 768px)
```
┌─────────────────────┐
│   Header (Nav)      │
├─────────────────────┤
│                     │
│                     │
│   Camera Feed       │
│   (Full Width)      │
│                     │
│                     │
├─────────────────────┤
│ Question Card       │
├─────────────────────┤
│ Answer Input        │
│ + Controls          │
└─────────────────────┘
```

### Desktop/Landscape (≥ 768px)
```
┌───────────────────────────────────────────────┐
│               Header (Nav)                    │
├───────────────────────┬───────────────────────┤
│                       │                       │
│                       │  Question Card        │
│   Camera Feed         ├───────────────────────┤
│   (60% width)         │                       │
│                       │  Answer Input         │
│                       │  + Controls           │
│                       │                       │
└───────────────────────┴───────────────────────┘
```

## 🔑 API Endpoints

### Profiles
- `GET /api/v1/profiles/me` - Get current user profile
- `POST /api/v1/profiles/` - Create new profile
- `PATCH /api/v1/profiles/me` - Update profile
- `DELETE /api/v1/profiles/me` - Delete profile

### Sessions
- `GET /api/v1/sessions/` - List all sessions
- `GET /api/v1/sessions/{id}` - Get session detail
- `POST /api/v1/sessions/` - Create new session
- `PATCH /api/v1/sessions/{id}` - Update session
- `POST /api/v1/sessions/{id}/start` - Start session
- `POST /api/v1/sessions/{id}/complete` - Complete session

### AI Chat
- `POST /api/v1/ai/chat` - Chat with AI interviewer
- `POST /api/v1/ai/generate-questions` - Generate questions
- `POST /api/v1/ai/evaluate-answer` - Evaluate answer

## 🔐 Authentication

Menggunakan Supabase Auth dengan JWT tokens. Setiap request ke protected endpoints harus menyertakan header:

```
Authorization: Bearer <your_jwt_token>
```

## 🛠 Development

### Running Tests (TODO)
```bash
# Backend tests
pytest

# Frontend tests
npm test
```

### Code Style
```bash
# Backend linting
black app/
flake8 app/

# Frontend linting
npm run lint
```

## 📝 License

MIT License - see LICENSE file for details

## 👥 Contributors

- Your Name - Initial work

---

Built with ❤️ using FastAPI, React, and AI
