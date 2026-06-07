import React, { useState, useRef, useEffect } from 'react'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

const Interview = () => {
  const [isRecording, setIsRecording] = useState(false)
  const [messages, setMessages] = useState([
    { id: 1, sender: 'ai', text: 'Halo! Saya AI Interviewer kamu hari ini. Selamat datang di sesi wawancara simulasi. Bisa ceritakan sedikit tentang dirimu?', timestamp: new Date() }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const videoRef = useRef(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Request camera access
  useEffect(() => {
    const getCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: 1280, height: 720 },
          audio: true 
        })
        if (videoRef.current) {
          videoRef.current.srcObject = stream
        }
      } catch (err) {
        console.error('Error accessing camera:', err)
        setMessages(prev => [...prev, {
          id: Date.now(),
          sender: 'system',
          text: 'Tidak dapat mengakses kamera. Pastikan izin kamera diberikan.',
          timestamp: new Date()
        }])
      }
    }

    getCamera()

    return () => {
      // Cleanup stream on unmount
      if (videoRef.current?.srcObject) {
        videoRef.current.srcObject.getTracks().forEach(track => track.stop())
      }
    }
  }, [])

  const handleSendMessage = () => {
    if (!inputMessage.trim()) return

    const newUserMessage = {
      id: Date.now(),
      sender: 'user',
      text: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, newUserMessage])
    setInputMessage('')

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        id: Date.now() + 1,
        sender: 'ai',
        text: 'Terima kasih atas jawabanmu. Itu sangat menarik! Bisa kamu jelaskan lebih detail tentang pengalaman kerjamu sebelumnya?',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, aiResponse])
    }, 1500)
  }

  const toggleRecording = () => {
    setIsRecording(!isRecording)
  }

  return (
    <div className="min-h-screen bg-slate-50 transition-layout">
      {/* Top Bar */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b border-slate-200 px-4 py-3">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">I</span>
            </div>
            <span className="font-semibold text-slate-800 hidden sm:inline">IntervU AI</span>
          </div>
          <div className="flex items-center space-x-4">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full ${isRecording ? 'bg-red-100' : 'bg-slate-100'}`}>
              <div className={`w-2 h-2 rounded-full ${isRecording ? 'bg-red-500 animate-pulse' : 'bg-slate-400'}`}></div>
              <span className="text-sm text-slate-600">{isRecording ? 'Merekam' : 'Siap'}</span>
            </div>
            <Button 
              variant={isRecording ? 'outline' : 'primary'} 
              onClick={toggleRecording}
              className="px-4 py-2 text-sm"
            >
              {isRecording ? 'Stop' : 'Mulai'}
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content - Responsive Layout */}
      <main className="pt-16 pb-20 md:pb-4 transition-layout">
        <div className="h-[calc(100vh-4rem)] md:h-[calc(100vh-8rem)] max-w-7xl mx-auto px-4 flex flex-col md:flex-row gap-4">
          
          {/* Video Section - Left Side on Desktop, Full on Mobile */}
          <div className="flex-1 relative bg-black rounded-xl overflow-hidden shadow-lg transition-layout">
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
            
            {/* Overlay Info */}
            <div className="absolute top-4 left-4 bg-black/50 backdrop-blur-sm px-3 py-2 rounded-lg">
              <p className="text-white text-sm font-medium">Kamera Aktif</p>
              <p className="text-white/70 text-xs">1280x720</p>
            </div>

            {/* Recording Indicator */}
            {isRecording && (
              <div className="absolute top-4 right-4 bg-red-500/90 backdrop-blur-sm px-3 py-2 rounded-lg flex items-center space-x-2">
                <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                <span className="text-white text-sm font-medium">REC</span>
              </div>
            )}
          </div>

          {/* Chat Panel - Right Side on Desktop, Bottom Sheet on Mobile */}
          <div className="md:w-96 flex flex-col bg-white rounded-xl shadow-lg border border-slate-200 overflow-hidden transition-layout">
            {/* Chat Header */}
            <div className="p-4 border-b border-slate-200 bg-slate-50">
              <h2 className="font-semibold text-slate-800">AI Interviewer</h2>
              <p className="text-sm text-slate-500">Sesi Wawancara #1</p>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] px-4 py-2 rounded-2xl ${
                      message.sender === 'user'
                        ? 'bg-primary-500 text-white'
                        : message.sender === 'system'
                        ? 'bg-yellow-100 text-yellow-800'
                        : 'bg-slate-100 text-slate-800'
                    }`}
                  >
                    <p className="text-sm">{message.text}</p>
                    <p className={`text-xs mt-1 ${
                      message.sender === 'user' ? 'text-white/70' : 'text-slate-500'
                    }`}>
                      {message.timestamp.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 border-t border-slate-200 bg-white">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ketik jawabanmu..."
                  className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-sm"
                />
                <Button onClick={handleSendMessage} className="px-4 py-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Mobile Control Bar - Fixed at Bottom */}
      <div className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 px-4 py-3 z-50">
        <div className="flex justify-around items-center">
          <button className="flex flex-col items-center space-y-1 text-slate-600">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
            <span className="text-xs">Mic</span>
          </button>
          
          <button 
            onClick={toggleRecording}
            className={`w-14 h-14 rounded-full flex items-center justify-center ${
              isRecording ? 'bg-red-500' : 'bg-primary-500'
            } text-white shadow-lg transform hover:scale-105 transition-all`}
          >
            {isRecording ? (
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
            ) : (
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" />
                <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" />
              </svg>
            )}
          </button>
          
          <button className="flex flex-col items-center space-y-1 text-slate-600">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
            <span className="text-xs">Video</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default Interview
