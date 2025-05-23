from flask import Flask, render_template, request, jsonify
import re
import math
from fractions import Fraction
import json

app = Flask(__name__)

def parse_expression(expr):
    """Convierte una expresión matemática en texto a un valor numérico."""
    try:
        if not expr or expr.strip() == '':
            return 0.0
            
        expr = str(expr).strip()
        
        # Reemplazar constantes
        expr = expr.replace('e', str(math.e))
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('pi', str(math.pi))
        
        # Manejar logaritmos
        expr = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expr)
        expr = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expr)
        
        # Manejar raíces cuadradas
        expr = re.sub(r'√(\d+\.?\d*|\([^)]+\))', r'math.sqrt(\1)', expr)
        
        # Manejar factorial
        expr = re.sub(r'(\d+\.?\d*)!', r'math.factorial(int(\1))', expr)
        
        # Manejar fracciones simples
        if '/' in expr and not any(op in expr for op in ['+', '-', '*', '^', '**', '(', ')']):
            parts = expr.split('/')
            if len(parts) == 2:
                try:
                    return float(Fraction(parts[0].strip(), parts[1].strip()))
                except:
                    pass
        
        # Reemplazar exponentes
        expr = expr.replace('^', '**')
        
        # Funciones matemáticas disponibles
        math_functions = {
            "math": math,
            "sqrt": math.sqrt,
            "factorial": math.factorial,
            "log": math.log,
            "log10": math.log10,
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "exp": math.exp,
            "abs": abs
        }
        
        return float(eval(expr, {"__builtins__": {}}, math_functions))
    except Exception as e:
        raise ValueError(f"Expresión no válida: {expr}")

class SistemaEcuaciones:
    def __init__(self, matriz):
        self.matriz = matriz
        self.pasos = []
        self.paso_actual = 0
    
    def agregar_paso(self, descripcion, matriz_estado, tipo="operacion"):
        """Agrega un paso al historial"""
        self.pasos.append({
            'paso': len(self.pasos) + 1,
            'descripcion': descripcion,
            'matriz': [fila[:] for fila in matriz_estado],
            'tipo': tipo
        })
    
    def eliminacion_gaussiana(self):
        """Realiza eliminación gaussiana con registro de pasos"""
        if not self.matriz:
            raise ValueError("La matriz está vacía")
        
        filas = len(self.matriz)
        columnas = len(self.matriz[0])
        matriz_trabajo = [fila[:] for fila in self.matriz]
        
        self.agregar_paso("Matriz inicial", matriz_trabajo, "inicial")
        
        for i in range(min(filas, columnas - 1)):
            # Pivoteo parcial
            max_fila = i
            max_valor = abs(matriz_trabajo[i][i]) if i < len(matriz_trabajo) and i < len(matriz_trabajo[i]) else 0
            
            for k in range(i + 1, filas):
                if k < len(matriz_trabajo) and i < len(matriz_trabajo[k]) and abs(matriz_trabajo[k][i]) > max_valor:
                    max_fila = k
                    max_valor = abs(matriz_trabajo[k][i])
            
            if max_valor < 1e-10:
                self.agregar_paso(f"El pivote en columna {i+1} es cero, se omite", matriz_trabajo, "info")
                continue
            
            # Intercambiar filas si es necesario
            if max_fila != i:
                matriz_trabajo[i], matriz_trabajo[max_fila] = matriz_trabajo[max_fila], matriz_trabajo[i]
                self.agregar_paso(f"Intercambiar F{i+1} ↔ F{max_fila+1}", matriz_trabajo, "intercambio")
            
            # Eliminación hacia abajo
            for k in range(i + 1, filas):
                if abs(matriz_trabajo[k][i]) > 1e-10:
                    factor = matriz_trabajo[k][i] / matriz_trabajo[i][i]
                    for j in range(i, columnas):
                        matriz_trabajo[k][j] -= factor * matriz_trabajo[i][j]
                    
                    factor_str = f"{Fraction(factor).limit_denominator()}" if abs(factor) != 1 else "1"
                    self.agregar_paso(f"F{k+1} = F{k+1} - ({factor_str}) × F{i+1}", matriz_trabajo)
        
        # Sustitución hacia atrás
        soluciones = self.sustitucion_hacia_atras(matriz_trabajo)
        return soluciones
    
    def gauss_jordan(self):
        """Realiza eliminación Gauss-Jordan con registro de pasos"""
        if not self.matriz:
            raise ValueError("La matriz está vacía")
        
        filas = len(self.matriz)
        columnas = len(self.matriz[0])
        matriz_trabajo = [fila[:] for fila in self.matriz]
        
        self.agregar_paso("Matriz inicial", matriz_trabajo, "inicial")
        
        for i in range(min(filas, columnas - 1)):
            # Pivoteo parcial
            max_fila = i
            max_valor = abs(matriz_trabajo[i][i]) if i < len(matriz_trabajo) and i < len(matriz_trabajo[i]) else 0
            
            for k in range(i + 1, filas):
                if k < len(matriz_trabajo) and i < len(matriz_trabajo[k]) and abs(matriz_trabajo[k][i]) > max_valor:
                    max_fila = k
                    max_valor = abs(matriz_trabajo[k][i])
            
            if max_valor < 1e-10:
                self.agregar_paso(f"El pivote en columna {i+1} es cero, se omite", matriz_trabajo, "info")
                continue
            
            # Intercambiar filas si es necesario
            if max_fila != i:
                matriz_trabajo[i], matriz_trabajo[max_fila] = matriz_trabajo[max_fila], matriz_trabajo[i]
                self.agregar_paso(f"Intercambiar F{i+1} ↔ F{max_fila+1}", matriz_trabajo, "intercambio")
            
            # Normalización
            pivote = matriz_trabajo[i][i]
            if abs(pivote) > 1e-10:
                for j in range(i, columnas):
                    matriz_trabajo[i][j] /= pivote
                
                pivote_str = f"{Fraction(pivote).limit_denominator()}"
                self.agregar_paso(f"Normalizar F{i+1} (÷ {pivote_str})", matriz_trabajo, "normalizacion")
            
            # Eliminación completa
            for k in range(filas):
                if k != i and abs(matriz_trabajo[k][i]) > 1e-10:
                    factor = matriz_trabajo[k][i]
                    for j in range(i, columnas):
                        matriz_trabajo[k][j] -= factor * matriz_trabajo[i][j]
                    
                    factor_str = f"{Fraction(factor).limit_denominator()}"
                    self.agregar_paso(f"F{k+1} = F{k+1} - ({factor_str}) × F{i+1}", matriz_trabajo)
        
        # Limpiar valores muy pequeños
        for i in range(filas):
            for j in range(columnas):
                if abs(matriz_trabajo[i][j]) < 1e-10:
                    matriz_trabajo[i][j] = 0.0
        
        self.agregar_paso("Resultado final", matriz_trabajo, "final")
        return self.extraer_solucion(matriz_trabajo)
    
    def sustitucion_hacia_atras(self, matriz):
        """Realiza sustitución hacia atrás"""
        filas = len(matriz)
        columnas = len(matriz[0]) - 1
        soluciones = [0] * columnas
        
        self.agregar_paso("Iniciando sustitución hacia atrás", matriz, "sustitucion")
        
        for i in range(filas - 1, -1, -1):
            pivote_col = -1
            for j in range(columnas):
                if abs(matriz[i][j]) > 1e-10:
                    pivote_col = j
                    break
            
            if pivote_col == -1:
                continue
            
            suma = 0
            for j in range(pivote_col + 1, columnas):
                suma += matriz[i][j] * soluciones[j]
            
            soluciones[pivote_col] = (matriz[i][-1] - suma) / matriz[i][pivote_col]
            
            desc = f"x{pivote_col+1} = ({matriz[i][-1]:.4f} - {suma:.4f}) / {matriz[i][pivote_col]:.4f} = {soluciones[pivote_col]:.4f}"
            self.agregar_paso(desc, matriz, "calculo")
        
        return soluciones
    
    def extraer_solucion(self, matriz):
        """Extrae la solución de una matriz en forma escalonada reducida"""
        filas = len(matriz)
        columnas = len(matriz[0]) - 1
        soluciones = [0] * columnas
        
        for i in range(min(filas, columnas)):
            if abs(matriz[i][i]) > 1e-10:
                soluciones[i] = matriz[i][-1]
        
        return soluciones

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resolver', methods=['POST'])
def resolver():
    try:
        data = request.get_json()
        
        # Extraer datos
        matriz_data = data['matriz']
        metodo = data['metodo']
        formato = data.get('formato', 'decimal')
        
        # Procesar matriz
        matriz = []
        for fila in matriz_data:
            fila_procesada = []
            for valor in fila:
                if valor is None or valor == '':
                    fila_procesada.append(0.0)
                else:
                    fila_procesada.append(parse_expression(str(valor)))
            matriz.append(fila_procesada)
        
        # Resolver sistema
        sistema = SistemaEcuaciones(matriz)
        
        if metodo == 'gaussiana':
            soluciones = sistema.eliminacion_gaussiana()
        elif metodo == 'gauss_jordan':
            soluciones = sistema.gauss_jordan()
        else:
            raise ValueError("Método no válido")
        
        # Formatear respuesta
        response = {
            'exito': True,
            'pasos': sistema.pasos,
            'soluciones': soluciones,
            'formato': formato
        }
        
        # Convertir a fracciones si es necesario
        if formato == 'fraccion':
            response['soluciones_fraccion'] = [str(Fraction(sol).limit_denominator()) for sol in soluciones]
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'exito': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True)