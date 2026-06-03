import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/shared/Navbar'
import Home from './pages/Home'
import Evaluate from './pages/Evaluate'
import Results from './pages/Results'

const App = () => {
    return (
        <BrowserRouter>
            <div className="min-h-screen" style={{ background: '#0a0a0a' }}>
                <Navbar />
                <main className="max-w-6xl mx-auto px-8 pt-24 pb-10">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/evaluate" element={<Evaluate />} />
                        <Route path="/results" element={<Results />} />
                    </Routes>
                </main>
            </div>
        </BrowserRouter>
    )
}

export default App