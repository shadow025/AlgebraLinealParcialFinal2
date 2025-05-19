import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Solver from './pages/Solver'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/solver" element={<Solver />} />
      </Routes>
    </Router>
  )
}

export default App
