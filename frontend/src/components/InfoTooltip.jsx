import { useState } from 'react'

function InfoTooltip() {
    const [show, setShow] = useState(false)

    return (
        <div className="relative">
            <button
                onMouseEnter={() => setShow(true)}
                onMouseLeave={() => setShow(false)}
                className="px-4 py-3 bg-gray-700 rounded-lg"
            >
                ℹ️ Info
            </button>
            {show && (
                <div className="absolute top-full mt-2 w-64 bg-white text-black p-4 rounded shadow-lg z-10">
                    Esta aplicación resuelve sistemas de ecuaciones lineales de hasta 6x6. Escoge el método y sigue los pasos.
                </div>
            )}
        </div>
    )
}

export default InfoTooltip
