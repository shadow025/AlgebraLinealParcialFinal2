import { useNavigate } from 'react-router-dom'
import InfoTooltip from '../components/InfoTooltip'
import { motion } from 'framer-motion'
import { PlayIcon } from '@heroicons/react/24/solid'

function Home() {
    const navigate = useNavigate()

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-blue-900 to-blue-800 text-white px-4 pt-10">

            {/* Título animado */}
            <motion.h1
                initial={{ opacity: 0, y: -50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8 }}
                className="text-6xl font-extrabold mb-12 text-center drop-shadow-md"
            >
                Sistema de Ecuaciones Lineales
            </motion.h1>

            {/* Tarjeta animada */}
            <motion.div
                initial={{ opacity: 0, y: 50 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 1, delay: 0.3 }}
                className="bg-white/10 backdrop-blur-lg p-10 rounded-2xl shadow-2xl text-center max-w-md w-full"
            >
                <ul className="text-white mb-8 font-bold text-base">
                    <li className='m-2'>Alejandro Santos</li>
                    <li>Luis Carlos Gomez</li>
                </ul>


                <div className="flex justify-center gap-4 w-full">
                    <button
                        onClick={() => navigate('/solver')}
                        className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl transition-all duration-200"
                    >
                        <PlayIcon className="w-5 h-5" />
                        Iniciar
                    </button>

                    <InfoTooltip />
                </div>
            </motion.div>
        </div>
    )
}

export default Home
