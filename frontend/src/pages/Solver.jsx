import { useNavigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import MethodPanel from '../components/MethodPanel'

function Solver() {
    const navigate = useNavigate()
    const [size, setSize] = useState(3)
    const [matrix, setMatrix] = useState(generateEmptyMatrix(3))
    const [selectedMethod, setSelectedMethod] = useState("")
    const [availableMethods] = useState(['Igualacion', 'Sustitucion', 'Gauss', 'Gauss-Jordan'])
    const [errors, setErrors] = useState([]);
    const [methodError, setMethodError] = useState(false);


    function generateEmptyMatrix(n) {
        return Array.from({ length: n }, () => Array(n + 1).fill(''))
    }

    const handleSizeChange = (e) => {
        const newSize = parseInt(e.target.value)
        setSize(newSize)
    }

    useEffect(() => {
        setMatrix(generateEmptyMatrix(size))
    }, [size])

    const handleChange = (i, j, value) => {
        const updated = [...matrix]
        updated[i][j] = value
        setMatrix(updated)
    }

    const handleRandom = () => {
        const randomMatrix = matrix.map(row =>
            row.map(() => (Math.random() * 10).toFixed(0))
        )
        setMatrix(randomMatrix)
    }

    const handleSubmit = () => {
        if (!validateInputs()) return;

        const payload = {
            method: selectedMethod,
            matrix: matrix.map(row => row.map(Number)),
        };

        console.log("📤 Enviando al backend:", payload);
        // fetch(...) cuando esté listo el backend
    };

    const validateInputs = () => {
        const newErrors = Array.from({ length: size }, () =>
            Array(size + 1).fill(false)
        );

        let hasError = false;

        if (!selectedMethod) {
            setMethodError(true);
            hasError = true;
        } else {
            setMethodError(false);
        }

        for (let i = 0; i < size; i++) {
            for (let j = 0; j < size + 1; j++) {
                const val = matrix[i][j];
                if (val === '' || isNaN(val)) {
                    newErrors[i][j] = true;
                    hasError = true;
                }
            }
        }

        setErrors(newErrors);

        if (hasError) {
            alert("⚠️ Hay campos vacíos, no numéricos o método no seleccionado.");
            return false;
        }

        return true;
    };


    return (
        <div className="p-8 bg-gray-100 min-h-screen">
            <h2 className="text-2xl font-bold mb-6 text-center">Resolver Sistema</h2>

            <div className="flex gap-8 justify-center">
                <div className="space-y-4">
                    <MethodPanel
                        methods={availableMethods}
                        selectedMethod={selectedMethod}
                        onChange={setSelectedMethod}
                    />

                    <div>
                        <label className="font-semibold mr-2">Tamaño del sistema:</label>
                        <select
                            value={size}
                            onChange={handleSizeChange}
                            className="border px-3 py-1 rounded"
                        >
                            {[2, 3, 4, 5, 6].map(n => (
                                <option key={n} value={n}>{n}x{n}</option>
                            ))}
                        </select>
                    </div>
                </div>

                <div className="space-y-4">
                    {matrix.map((row, i) => (
                        <div key={i} className="flex gap-2">
                            {row.map((val, j) => (
                                <input
                                    key={j}
                                    type="text"
                                    className={`w-16 p-2 border rounded text-center ${errors[i]?.[j] ? 'border-red-500' : 'border-gray-300'}`}
                                    value={val}
                                    onChange={e => handleChange(i, j, e.target.value)}
                                />
                            ))}
                        </div>
                    ))}

                    <div className="flex gap-4 mt-4">
                        <button
                            onClick={handleRandom}
                            className="px-4 py-2 bg-yellow-500 hover:bg-yellow-600 text-white rounded"
                        >
                            Generar Aleatorios
                        </button>

                        <button
                            onClick={handleSubmit}
                            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded"
                        >
                            Calcular
                        </button>

                        <button
                            onClick={() => navigate('/')}
                            className="px-6 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded"
                        >
                            Inicio
                        </button>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Solver
