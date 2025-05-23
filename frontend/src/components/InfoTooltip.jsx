import { useState } from 'react'
import { InformationCircleIcon } from '@heroicons/react/24/outline'

function InfoTooltip() {
    const [show, setShow] = useState(false)

    return (
        <div className="relative">
            <button
                onMouseEnter={() => setShow(true)}
                onMouseLeave={() => setShow(false)}
                className="px-4 py-3 bg-gray-700 hover:bg-gray-600 rounded-xl transition-all duration-200"
            >
                <InformationCircleIcon className="w-5 h-5 text-white" />
            </button>
            {show && (
                <div className="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 w-72 bg-white text-black p-4 rounded-lg shadow-xl z-10 text-sm animate-fade-in">
                    Esta aplicación resuelve sistemas de ecuaciones lineales de hasta 6x6 haciendo uso de los metodos vistos en el semestre
                </div>
            )}
        </div>
    )
}

export default InfoTooltip
