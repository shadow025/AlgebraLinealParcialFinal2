function MethodPanel({ methods, selectedMethod, onChange, hasError }) {
    return (
        <div className="bg-white shadow-lg rounded-xl p-6 w-full md:w-64">
            <h3 className="text-lg font-semibold mb-2 text-gray-800 text-center">
                Método de resolución
            </h3>
            <select
                value={selectedMethod}
                onChange={e => onChange(e.target.value)}
                className={`w-full p-2 border rounded ${hasError ? 'border-red-500' : 'border-gray-300'}`}
            >
                <option value="" disabled>
                    Seleccione un método
                </option>
                {methods.map((method, index) => (
                    <option key={index} value={method}>
                        {method}
                    </option>
                ))}
            </select>
        </div>
    )
}

export default MethodPanel
