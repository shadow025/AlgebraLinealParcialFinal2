import { useNavigate } from 'react-router-dom'
import InfoTooltip from '../components/InfoTooltip'

function Home() {
    const navigate = useNavigate()

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-blue-900 text-white">
            <h1 className="text-4xl font-bold mb-8 text-center">Sistema de Ecuaciones Lineales</h1>
            <div className="flex gap-4">
                <button
                    onClick={() => navigate('/solver')}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-lg transition"
                >
                    Iniciar
                </button>

                <InfoTooltip />
            </div>
        </div>
    )
}

export default Home
