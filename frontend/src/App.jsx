import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Interview from './pages/Interview'

function App() {
  return (
    <div className="min-h-screen bg-slate-50">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/interview" element={<Interview />} />
      </Routes>
    </div>
  )
}

export default App
