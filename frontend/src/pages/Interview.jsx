/**
 * Interview Page - Halaman Wawancara dengan Layout Dinamis
 * 
 * Fitur Utama:
 * - Mobile (Portrait): Kamera full screen, overlay chat di bawah
 * - Desktop/Landscape: Split screen (60% kamera, 40% panel chat)
 * - Auto-rotate animation smooth dengan CSS transition
 * - Fully responsive mobile-first design
 */
import { useState, useEffect } from 'react'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

function Interview() {
  const [isLandscape, setIsLandscape] = useState(false)
  const [currentQuestion, setCurrentQuestion] = useState(1)
  const [userAnswer, setUserAnswer] = useState('')
  const [isRecording, setIsRecording] = useState(false)

  // Detect orientation change
  useEffect(() => {
    const handleOrientationChange = () => {
      // Check if width > height (landscape)
      setIsLandscape(window.innerWidth > window.innerHeight)
    }

    // Initial check
    handleOrientationChange()

    // Listen for resize events (covers orientation change on desktop too)
    window.addEventListener('resize', handleOrientationChange)

    return () => {
      window.removeEventListener('resize', handleOrientationChange)
    }
  }, [])

  // Dummy questions
  const questions = [
    "Bisa ceritakan tentang pengalaman kerja Anda yang paling relevan?",
    "Apa kelebihan dan kekurangan Anda dalam bekerja?",
    "Mengapa Anda tertarik dengan posisi ini?",
    "Bagaimana cara Anda menangani tekanan dalam pekerjaan?",
    "Di mana Anda melihat diri Anda dalam 5 tahun ke depan?"
  ]

  const handleStartRecording = () => {
    setIsRecording(!isRecording)
  }

  const handleSubmitAnswer = () => {
    console.log('Answer submitted:', userAnswer)
    // Move to next question or finish
    if (currentQuestion < questions.length) {
      setCurrentQuestion(currentQuestion + 1)
      setUserAnswer('')
    } else {
      alert('Wawancara selesai! Terima kasih.')
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 layout-transition">
      {/* Header */}
      <header className="bg-white border-b border-slate-100 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-lg font-bold text-slate-800">IntervU AI</span>
            <span className="text-slate-300">|</span>
            <span className="text-sm text-slate-600">Pertanyaan {currentQuestion} dari {questions.length}</span>
          </div>
          <Button variant="secondary" size="sm" onClick={() => window.location.href = '/'}>
            Keluar
          </Button>
        </div>
      </header>

      {/* Main Content - Dynamic Layout based on orientation */}
      <main className={`layout-transition ${
        isLandscape 
          ? 'flex flex-row max-w-7xl mx-auto' 
          : 'flex flex-col'
      }`}>
        
        {/* Camera Section - 60% width on landscape */}
        <section className={`relative bg-black layout-transition ${
          isLandscape 
            ? 'w-full md:w-[60%] h-[calc(100vh-4rem)]' 
            : 'w-full h-[60vh]'
        }`}>
          {/* Placeholder untuk camera feed */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center text-white">
              <div className="w-20 h-20 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-4xl">📹</span>
              </div>
              <p className="text-lg font-medium">Kamera Aktif</p>
              <p className="text-sm text-slate-400 mt-2">
                {isRecording ? '● Sedang merekam...' : 'Siap merekam'}
              </p>
            </div>
          </div>

          {/* Recording indicator overlay */}
          {isRecording && (
            <div className="absolute top-4 left-4 flex items-center space-x-2 bg-red-500/90 text-white px-3 py-1.5 rounded-full text-sm animate-pulse">
              <div className="w-2 h-2 bg-white rounded-full"></div>
              <span>REC</span>
            </div>
          )}

          {/* Progress bar */}
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-slate-800">
            <div 
              className="h-full bg-primary-500 transition-all duration-500"
              style={{ width: `${(currentQuestion / questions.length) * 100}%` }}
            ></div>
          </div>
        </section>

        {/* Chat Panel - 40% width on landscape, overlay on mobile portrait */}
        <section className={`layout-transition ${
          isLandscape 
            ? 'w-full md:w-[40%] h-[calc(100vh-4rem)] overflow-y-auto' 
            : 'w-full flex-1 p-4'
        }`}>
          <div className={`h-full flex flex-col ${
            !isLandscape ? 'max-w-7xl mx-auto' : ''
          }`}>
            
            {/* Question Card */}
            <Card className="mb-4 flex-shrink-0 layout-transition">
              <div className="flex items-start space-x-3">
                <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center flex-shrink-0">
                  <span className="text-xl">🤖</span>
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-slate-800 mb-2">
                    Pertanyaan {currentQuestion}
                  </h3>
                  <p className="text-slate-700 leading-relaxed">
                    {questions[currentQuestion - 1]}
                  </p>
                </div>
              </div>
            </Card>

            {/* Answer Input Area - Show only in landscape or when scrolled on mobile */}
            <div className={`flex-1 flex flex-col layout-transition ${
              isLandscape ? '' : 'mt-4'
            }`}>
              <Card className="flex-1 flex flex-col">
                <label className="block text-sm font-medium text-slate-700 mb-2">
                  Jawaban Anda
                </label>
                <textarea
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="Ketik atau rekam jawaban Anda di sini..."
                  className="flex-1 w-full px-4 py-3 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 resize-none layout-transition"
                  rows={isLandscape ? 8 : 4}
                />
                
                {/* Control Bar */}
                <div className="mt-4 flex flex-col sm:flex-row gap-3">
                  <Button
                    variant={isRecording ? 'primary' : 'secondary'}
                    onClick={handleStartRecording}
                    className={isRecording ? 'bg-red-500 hover:bg-red-600' : ''}
                  >
                    {isRecording ? '⏹ Stop Recording' : '🎤 Rekam Jawaban'}
                  </Button>
                  <Button 
                    onClick={handleSubmitAnswer}
                    disabled={!userAnswer.trim()}
                  >
                    {currentQuestion === questions.length ? '✅ Selesai' : '➡ Lanjut'}
                  </Button>
                </div>
              </Card>
            </div>
          </div>
        </section>
      </main>

      {/* Mobile-only floating info */}
      {!isLandscape && (
        <div className="fixed bottom-4 left-4 right-4 z-40 md:hidden">
          <Card className="py-3 px-4 bg-white/95 backdrop-blur-sm shadow-lg">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-600">
                Pertanyaan {currentQuestion}/{questions.length}
              </span>
              <span className="text-xs text-slate-400">
                Putar device untuk mode split-screen
              </span>
            </div>
          </Card>
        </div>
      )}
    </div>
  )
}

export default Interview
