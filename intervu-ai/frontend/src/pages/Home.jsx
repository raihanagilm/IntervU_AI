import React from 'react'
import { Link } from 'react-router-dom'
import Button from '../components/ui/Button'

const Home = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-white transition-layout">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">I</span>
              </div>
              <span className="text-xl font-semibold text-slate-800">IntervU AI</span>
            </div>
            <nav className="hidden md:flex space-x-8">
              <a href="#features" className="text-slate-600 hover:text-primary-500 transition-colors">Fitur</a>
              <a href="#about" className="text-slate-600 hover:text-primary-500 transition-colors">Tentang</a>
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="pt-24 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-slate-800 mb-6 leading-tight">
            Selamat Datang di{' '}
            <span className="text-primary-500">IntervU AI</span>
          </h1>
          
          <p className="text-lg sm:text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
            Simulasi Wawancara Kerja Berbasis AI yang akan membantumu mempersiapkan diri 
            untuk menghadapi wawancara kerja impian dengan lebih percaya diri.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link to="/interview">
              <Button className="w-full sm:w-auto text-lg px-8 py-4">
                Mulai Wawancara
              </Button>
            </Link>
            <Button variant="secondary" className="w-full sm:w-auto text-lg px-8 py-4">
              Pelajari Lebih Lanjut
            </Button>
          </div>

          {/* Features Preview */}
          <div id="features" className="mt-20 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-2">AI Interviewer</h3>
              <p className="text-slate-600 text-sm">Interviewer AI yang realistis dengan pertanyaan adaptif sesuai posisi targetmu.</p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-2">Video Analysis</h3>
              <p className="text-slate-600 text-sm">Analisis bahasa tubuh, kontak mata, dan ekspresi wajah secara real-time.</p>
            </div>

            <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4 mx-auto">
                <svg className="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="text-lg font-semibold text-slate-800 mb-2">Instant Feedback</h3>
              <p className="text-slate-600 text-sm">Dapatkan feedback mendetail dan saran perbaikan setelah setiap sesi.</p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-8">
        <div className="max-w-7xl mx-auto px-4 text-center text-slate-500 text-sm">
          <p>&copy; 2024 IntervU AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}

export default Home
