from flask import Flask, render_template, request, jsonify
import math
import re
from fractions import Fraction

app = Flask(__name__)

def parse_expression(expr):
    try:
        if not expr or expr.strip() == '':
            return 0.0
        expr = expr.strip()
        expr = expr.replace('e', str(math.e)).replace('π', str(math.pi)).replace('pi', str(math.pi))
        expr = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expr)
        expr = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expr)
        expr = re.sub(r'√(\d+\.?\d*|\([^)]+\))', r'math.sqrt(\1)', expr)
        expr = re.sub(r'(\d+\.?\d*)!', r'math.factorial(int(\1))', expr)
        if '/' in expr and not any(op in expr for op in ['+', '-', '*', '^', '**', '(', ')']):
            parts = expr.split('/')
            if len(parts) == 2:
                return float(Fraction(parts[0].strip(), parts[1].strip()))
        expr = expr.replace('^', '**')
        math_functions = { "math": math, "sqrt": math.sqrt, "factorial": math.factorial, "log": math.log, "log10": math.log10, "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "abs": abs }
        return float(eval(expr, {"__builtins__": {}}, math_functions))
    except Exception as e:
        raise ValueError(f"Expresión no válida: {expr}")

class SistemaEcuaciones:
    def __init__(self, matriz):
        self.matriz = matriz
        self.pasos = []

    def agregar_paso(self, descripcion, matriz_estado):
        self.pasos.append({'descripcion': descripcion, 'matriz': [fila[:] for fila in matriz_estado]})

    def eliminacion_gaussiana(self):
        filas = len(self.matriz)
        columnas = len(self.matriz[0])
        m = [fila[:] for fila in self.matriz]
        self.agregar_paso("Matriz inicial", m)
        for i in range(min(filas, columnas - 1)):
            max_fila = max(range(i, filas), key=lambda r: abs(m[r][i]))
            if abs(m[max_fila][i]) < 1e-10:
                self.agregar_paso(f"Pivote nulo en columna {i+1}", m)
                continue
            if max_fila != i:
                m[i], m[max_fila] = m[max_fila], m[i]
                self.agregar_paso(f"Intercambio F{i+1} ↔ F{max_fila+1}", m)
            for k in range(i+1, filas):
                factor = m[k][i] / m[i][i]
                for j in range(i, columnas):
                    m[k][j] -= factor * m[i][j]
                self.agregar_paso(f"F{k+1} = F{k+1} - {Fraction(factor).limit_denominator()}×F{i+1}", m)
        return self.sustitucion_hacia_atras(m)

    def sustitucion_hacia_atras(self, matriz):
        filas = len(matriz)
        columnas = len(matriz[0]) - 1
        soluciones = [0] * columnas
        for i in range(filas - 1, -1, -1):
            suma = sum(matriz[i][j] * soluciones[j] for j in range(i+1, columnas))
            soluciones[i] = (matriz[i][-1] - suma) / matriz[i][i]
            self.agregar_paso(f"x{i+1} = {soluciones[i]}", matriz)
        return soluciones

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        data = request.get_json()
        matriz_data = data['matriz']
        metodo = data['metodo']
        formato = data.get('formato', 'decimal')

        matriz = []
        for fila in matriz_data:
            fila_procesada = []
            for valor in fila:
                fila_procesada.append(parse_expression(str(valor)))
            matriz.append(fila_procesada)

        sistema = SistemaEcuaciones(matriz)

        if metodo == 'gaussiana':
            soluciones = sistema.eliminacion_gaussiana()
        else:
            raise ValueError("Método no válido")

        response = {
            'exito': True,
            'pasos': sistema.pasos,
            'soluciones': soluciones,
            'formato': formato
        }

        if formato == 'fraccion':
            response['soluciones_fraccion'] = [str(Fraction(sol).limit_denominator()) for sol in soluciones]

        return jsonify(response)
    except Exception as e:
        return jsonify({'exito': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
