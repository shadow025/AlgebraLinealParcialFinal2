function App() {

  return (
    <>
      <body class="bg-slate-900 text-slate-100 min-h-screen flex flex-col items-center justify-start p-6">
        <header class="text-3xl font-bold mb-6 animate-fade-in">SolverX - Álgebra Lineal Visual</header>

        <section id="config" class="w-full max-w-2xl mb-6 p-4 bg-slate-800 rounded-2xl shadow-xl">
          {/* <!-- Número de ecuaciones --> */}
          <label for="numEcuaciones" class="block mb-2">¿Cuántas ecuaciones deseas resolver?</label>
          <input type="number" id="numEcuaciones" min="2" max="6" class="w-full p-2 rounded bg-slate-700 text-white" />
          <button onclick="generarInputs()" class="mt-4 bg-blue-500 px-4 py-2 rounded hover:bg-blue-600 transition">Generar Inputs</button>
        </section>

        <section id="formularioInputs" class="w-full max-w-4xl mb-6 hidden animate-fade-in">
          {/* <!-- Aquí se inyectará la tabla de inputs dinámicamente --> */}
        </section>

        <section id="selectorMetodo" class="w-full max-w-2xl mb-6 hidden">
          <label>Método de resolución:</label>
          <select class="w-full p-2 rounded bg-slate-700 text-white mt-2">
            <option>Gauss</option>
            <option>Gauss-Jordan</option>
            <option>LU</option>
            <option>Inversa</option>
            <option>Cramer</option>
          </select>
          <button class="mt-4 bg-yellow-400 text-slate-900 px-4 py-2 rounded hover:bg-yellow-300 transition">Resolver</button>
        </section>

        <section id="resultado" class="w-full max-w-4xl bg-slate-800 p-4 rounded-xl shadow-lg hidden">
          {/* <!-- Aquí se mostrarán los pasos animados --> */}
        </section>
      </body>

    </>
  )
}

export default App
