/**
 * Home Page - Landing Page IntervU AI
 * 
 * Fitur:
 * - Hero section dengan judul dan CTA
 * - Fully responsive (mobile-first)
 * - Animasi smooth saat rotate device
 */
import { Link } from 'react-router-dom'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'

function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-slate-50">
      {/* Navigation */}
      <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">I</span>
              </div>
              <span className="text-xl font-bold text-slate-800">IntervU AI</span>
            </div>
            <div className="hidden sm:flex items-center space-x-4">
              <Button variant="secondary" size="sm">Login</Button>
              <Button size="sm">Mulai Gratis</Button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 sm:py-32 layout-transition">
          <div className="text-center layout-transition">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-slate-800 mb-6 leading-tight">
              Selamat Datang di{' '}
              <span className="text-primary-500">IntervU AI</span>
            </h1>
            <p className="text-lg sm:text-xl text-slate-600 mb-8 max-w-2xl mx-auto">
              Simulasi Wawancara Kerja Berbasis AI. Latih kemampuan interview Anda dengan feedback instan dan personalisasi.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link to="/interview">
                <Button size="lg" className="w-full sm:w-auto">
                  🎯 Mulai Wawancara
                </Button>
              </Link>
              <Button variant="secondary" size="lg" className="w-full sm:w-auto">
                📖 Pelajari Lebih Lanjut
              </Button>
            </div>
          </div>
        </div>
        
        {/* Decorative background elements */}
        <div className="absolute top-0 left-0 -z-10 w-full h-full overflow-hidden">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-100 rounded-full blur-3xl opacity-30"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-200 rounded-full blur-3xl opacity-30"></div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold text-slate-800 mb-4">
              Kenapa IntervU AI?
            </h2>
            <p className="text-lg text-slate-600 max-w-2xl mx-auto">
              Platform simulasi wawancara paling lengkap dengan teknologi AI terbaru
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 layout-transition">
            <Card hoverable className="layout-transition">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">AI Interviewer</h3>
              <p className="text-slate-600">
                Berinteraksi dengan AI yang bertindak sebagai interviewer profesional dengan pertanyaan relevan.
              </p>
            </Card>
            
            <Card hoverable className="layout-transition">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">⚡</span>
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Feedback Instan</h3>
              <p className="text-slate-600">
                Dapatkan feedback detail dan skor untuk setiap jawaban secara real-time.
              </p>
            </Card>
            
            <Card hoverable className="layout-transition">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="text-xl font-semibold text-slate-800 mb-2">Personalisasi</h3>
              <p className="text-slate-600">
                Pertanyaan disesuaikan dengan posisi, level, dan industri yang Anda targetkan.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-slate-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <div className="flex items-center justify-center space-x-2 mb-4">
              <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">I</span>
              </div>
              <span className="text-xl font-bold">IntervU AI</span>
            </div>
            <p className="text-slate-400">
              © 2024 IntervU AI. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
