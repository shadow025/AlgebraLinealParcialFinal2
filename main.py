import re
import math
from fractions import Fraction
import sympy as sp
import numpy as np

def parse_expression(expr):
    """
    Convierte una expresión matemática en texto a un valor numérico.
    Maneja fracciones, exponentes, raíces, factoriales, logaritmos, constantes y decimales.
    """
    try:
        # Reemplazar constantes
        expr = expr.replace('e', str(math.e))
        expr = expr.replace('π', str(math.pi))
        expr = expr.replace('pi', str(math.pi))
        
        # Manejar logaritmos: log(x) → log10(x), ln(x) → log(x)
        expr = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expr)
        expr = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expr)
        
        # Manejar raíces cuadradas: √x → sqrt(x)
        expr = re.sub(r'√(\d+\.?\d*|\([^)]+\))', r'math.sqrt(\1)', expr)
        
        # Manejar raíces n-ésimas: x√y → y**(1/x)
        expr = re.sub(r'(\d+\.?\d*)√(\d+\.?\d*|\([^)]+\))', r'(\2)**(1/\1)', expr)
        
        # Manejar factorial: x! → factorial(x)
        expr = re.sub(r'(\d+\.?\d*)!', r'math.factorial(int(\1))', expr)
        
        # Manejar fracciones: a/b → Fraction(a, b)
        frac_parts = expr.split('/')
        if len(frac_parts) == 2 and not any(op in expr for op in ['+', '-', '*', '^', '**']):
            try:
                return float(Fraction(eval(frac_parts[0], {"__builtins__": {}}, {"math": math})) / Fraction(eval(frac_parts[1], {"__builtins__": {}}, {"math": math})))
            except:
                pass
        
        # Reemplazar exponentes: x^y → x**y
        expr = expr.replace('^', '**')
        
        # Evaluar la expresión con acceso a todas las funciones matemáticas necesarias
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
        raise ValueError(f"Expresión no válida: {expr}. Error: {str(e)}")

def mostrar_matriz(matriz, formato):
    """Muestra la matriz en el formato seleccionado (1=decimal, 2=fracción)"""
    if not matriz:
        print("Matriz vacía")
        return
        
    print("\nMatriz aumentada:")
    for fila in matriz:
        if formato == 2:  # Fracción
            print("| " + " | ".join(f"{Fraction(x).limit_denominator():>8}" for x in fila) + " |")
        else:  # Decimal
            print("| " + " | ".join(f"{x:>12.6f}" for x in fila) + " |")

def gauss_jordan(matriz, formato):
    """Realiza eliminación Gauss-Jordan mostrando pasos"""
    if not matriz:
        raise ValueError("La matriz está vacía")
        
    filas = len(matriz)
    if filas == 0:
        raise ValueError("La matriz no tiene filas")
        
    columnas = len(matriz[0])
    paso = 1
    
    # Copiamos la matriz para no modificar la original
    matriz_trabajo = [fila[:] for fila in matriz]
    
    for i in range(filas):
        # Asegurarse de que estamos dentro de los límites de columnas
        if i >= columnas - 1:
            break
            
        # Pivoteo parcial
        max_fila = i
        max_valor = abs(matriz_trabajo[i][i]) if i < len(matriz_trabajo) and i < len(matriz_trabajo[i]) else 0
        
        for k in range(i + 1, filas):
            if k < len(matriz_trabajo) and i < len(matriz_trabajo[k]) and abs(matriz_trabajo[k][i]) > max_valor:
                max_fila = k
                max_valor = abs(matriz_trabajo[k][i])
        
        # Si el máximo es cero, la matriz es singular
        if max_valor < 1e-10:
            print(f"\nPaso {paso}: El pivote es cero, la columna {i+1} se omite")
            paso += 1
            continue
            
        # Intercambiar filas si es necesario
        if max_fila != i:
            matriz_trabajo[i], matriz_trabajo[max_fila] = matriz_trabajo[max_fila], matriz_trabajo[i]
            print(f"\nPaso {paso}: Intercambiar F{i+1} ↔ F{max_fila+1}")
            mostrar_matriz(matriz_trabajo, formato)
            paso += 1
        
        # Normalización
        pivote = matriz_trabajo[i][i]
        if abs(pivote) < 1e-10:  # Evitar división por cero
            continue
            
        for j in range(i, columnas):
            matriz_trabajo[i][j] /= pivote
            
        print(f"\nPaso {paso}: Normalizar F{i+1} (÷ {Fraction(pivote).limit_denominator()})")
        mostrar_matriz(matriz_trabajo, formato)
        paso += 1
        
        # Eliminación
        for k in range(filas):
            if k != i and abs(matriz_trabajo[k][i]) > 1e-10:
                factor = matriz_trabajo[k][i]
                for j in range(i, columnas):
                    matriz_trabajo[k][j] -= factor * matriz_trabajo[i][j]
                    
                print(f"\nPaso {paso}: F{k+1} = F{k+1} - ({Fraction(factor).limit_denominator()} × F{i+1})")
                mostrar_matriz(matriz_trabajo, formato)
                paso += 1
                
    # Limpiar valores muy pequeños (errores de redondeo)
    for i in range(filas):
        for j in range(columnas):
            if abs(matriz_trabajo[i][j]) < 1e-10:
                matriz_trabajo[i][j] = 0.0
                
    return matriz_trabajo

def metodo_euler(f, x0, y0, h, n, formato):
    """Implementa el método de Euler para ecuaciones diferenciales"""
    resultados = []
    x = x0
    y = y0
    
    print("\nMétodo de Euler:")
    print(f"Condiciones iniciales: x₀ = {x0}, y₀ = {y0}")
    print(f"Paso h = {h}, Número de iteraciones = {n}\n")
    
    try:
        # Almacenar el punto inicial
        resultados.append((x, y))
        
        # Realizar n iteraciones (no n+1 como estaba antes)
        for i in range(n):
            if formato == 2:
                print(f"Iteración {i}: x = {x:.6f}, y = {Fraction(y).limit_denominator()}")
            else:
                print(f"Iteración {i}: x = {x:.6f}, y = {y:.6f}")
            
            # Calcular la pendiente en el punto actual
            try:
                pendiente = f(x, y)
            except Exception as e:
                print(f"Error al evaluar la función en x={x}, y={y}: {str(e)}")
                break
                
            # Actualizar y utilizando la pendiente
            y_nuevo = y + h * pendiente
            
            # Actualizar x
            x_nuevo = x + h
            
            # Actualizar valores para la siguiente iteración
            x, y = x_nuevo, y_nuevo
            
            # Almacenar el nuevo punto
            resultados.append((x, y))
        
        # Mostrar la última iteración
        if formato == 2:
            print(f"Iteración {n}: x = {x:.6f}, y = {Fraction(y).limit_denominator()}")
        else:
            print(f"Iteración {n}: x = {x:.6f}, y = {y:.6f}")
            
    except Exception as e:
        print(f"Error en el método de Euler: {str(e)}")
    
    return resultados

def resolver_sistema(matriz, formato):
    """Resuelve un sistema de ecuaciones y muestra la solución"""
    try:
        filas = len(matriz)
        columnas = len(matriz[0]) - 1  # Excluyendo la columna de términos independientes
        
        # Resolver el sistema
        resultado = gauss_jordan(matriz.copy(), formato)
        
        # Verificar si el sistema es inconsistente
        for i in range(filas):
            # Si toda una fila tiene coeficientes cero pero término independiente no cero
            if all(abs(resultado[i][j]) < 1e-10 for j in range(columnas)) and abs(resultado[i][-1]) > 1e-10:
                print("\n¡SISTEMA INCONSISTENTE! No existe solución.")
                return
        
        # Verificar si el sistema tiene infinitas soluciones
        libre_count = 0
        for i in range(min(filas, columnas)):
            if abs(resultado[i][i]) < 1e-10:
                libre_count += 1
        
        if libre_count > 0:
            print(f"\nEl sistema tiene infinitas soluciones con {libre_count} variable(s) libre(s).")
        
        # Mostrar solución
        print("\n═══════════════════════════════════════")
        print("SOLUCIÓN DEL SISTEMA:")
        
        # Crear un array para almacenar las soluciones
        soluciones = [None] * columnas
        
        # Recorrer las filas de la matriz en forma escalonada
        for i in range(min(filas, columnas)):
            # Buscar la primera columna con un coeficiente no cero
            pivote_col = -1
            for j in range(columnas):
                if abs(resultado[i][j]) > 1e-10:
                    pivote_col = j
                    break
            
            if pivote_col != -1:
                # Esta variable está determinada
                valor = resultado[i][-1]
                if formato == 2:
                    print(f"x_{pivote_col+1} = {Fraction(valor).limit_denominator()}")
                else:
                    print(f"x_{pivote_col+1} = {valor:.6f}")
                soluciones[pivote_col] = valor
        
        # Verificar variables libres
        for j in range(columnas):
            if soluciones[j] is None:
                print(f"x_{j+1} = Parámetro libre (puede tomar cualquier valor)")
                
    except Exception as e:
        print(f"\nError durante el cálculo: {str(e)}")

def main():
    print("══════════════════════════════════════════════")
    print("  SISTEMA AVANZADO DE RESOLUCIÓN MATEMÁTICA")
    print("══════════════════════════════════════════════\n")
    print("1. Resolver sistema de ecuaciones (Gauss-Jordan)")
    print("2. Método de Euler para ecuaciones diferenciales")
    print("3. Ejemplos de demostración")
    print("4. Salir")
    
    while True:
        try:
            opcion = int(input("\nSeleccione una opción (1-4): "))
            if opcion not in [1, 2, 3, 4]:
                raise ValueError
            break
        except:
            print("Error: Ingrese un número entre 1 y 4.")
    
    if opcion == 4:
        print("¡Gracias por usar el sistema!")
        return
    
    # Selección de formato
    print("\nFORMATO DE RESULTADOS:")
    print("1. Decimal")
    print("2. Fracción")
    while True:
        try:
            formato = int(input("Elija formato (1/2): "))
            if formato not in [1, 2]:
                raise ValueError
            break
        except:
            print("Error: Ingrese 1 (decimal) o 2 (fracción).")
    
    if opcion == 1:
        # Resolver sistema de ecuaciones
        print("\n═══════════════════════════════════════")
        print("  RESOLUCIÓN DE SISTEMAS DE ECUACIONES")
        print("═══════════════════════════════════════\n")
        
        while True:
            try:
                filas = int(input("Número de ecuaciones (filas): "))
                columnas = int(input("Número de variables (columnas): "))
                if filas < 1 or columnas < 1:
                    raise ValueError
                break
            except:
                print("Error: Ingrese números enteros positivos.\n")
        
        # Ingreso de coeficientes
        print("\nINGRESO DE COEFICIENTES:")
        print("Ejemplos de formato aceptado:")
        print("- Fracciones: 1/2, 3/4")
        print("- Exponentes: 2^3, 5e^2")
        print("- Raíces: √2, 3√8 (raíz cúbica de 8)")
        print("- Factoriales: 5!, 3!")
        print("- Logaritmos: log(10), ln(e)")
        print("- Funciones trigonométricas: sin(π/2), cos(0)")
        print("- Combinaciones: 2!3^4/6, (1/2)e^3, ln(π)+√4")
        print("- Negativos y decimales: -3.14, 0.5")
        
        matriz_aumentada = []
        for i in range(filas):
            fila = []
            # Ingresar coeficientes
            while True:
                try:
                    entrada = input(f"\nCoeficientes ecuación {i+1} (separados por espacios): ")
                    elementos = entrada.split()
                    if len(elementos) != columnas:
                        print(f"Error: Debe ingresar exactamente {columnas} coeficientes.")
                        continue
                    
                    fila = [parse_expression(elem) for elem in elementos]
                    break
                except Exception as e:
                    print(f"Error: {str(e)}. Intente nuevamente.")
            
            # Ingresar término independiente
            while True:
                try:
                    valor = parse_expression(input(f"Término independiente ecuación {i+1}: "))
                    fila.append(valor)
                    break
                except Exception as e:
                    print(f"Error: {str(e)}. Intente nuevamente.")
            
            matriz_aumentada.append(fila)
        
        # Mostrar sistema original
        print("\n═══════════════════════════════════════")
        print("SISTEMA ORIGINAL:")
        mostrar_matriz(matriz_aumentada, formato)
        
        # Resolver el sistema
        resolver_sistema(matriz_aumentada, formato)
    
    elif opcion == 2:
        # Método de Euler
        print("\n═══════════════════════════════════════")
        print("  MÉTODO DE EULER PARA EDOS")
        print("═══════════════════════════════════════\n")
        
        print("La ecuación diferencial debe estar en forma dy/dx = f(x, y)")
        print("Ejemplos aceptados:")
        print("- Para dy/dx = x + y, ingrese 'x + y'")
        print("- Para dy/dx = x*y + sin(x), ingrese 'x*y + sin(x)'")
        print("- Para dy/dx = e^x - ln(y), ingrese 'exp(x) - log(y)'")
        print("- Para dy/dx = √(x²+y²), ingrese 'sqrt(x**2 + y**2)'")
        
        while True:
            try:
                expr = input("\nIngrese f(x, y): ")
                x, y = sp.symbols('x y')
                f_expr = sp.sympify(expr)
                
                # Verificar que la expresión contiene variables válidas
                variables = [str(var) for var in f_expr.free_symbols]
                if not all(var in ['x', 'y'] for var in variables):
                    print("Error: La expresión solo debe contener las variables x e y.")
                    continue
                
                # Crear una función lambda segura
                def f_segura(x_val, y_val):
                    try:
                        return float(f_expr.subs({'x': x_val, 'y': y_val}))
                    except Exception as e:
                        raise ValueError(f"Error al evaluar f({x_val}, {y_val}): {str(e)}")
                
                # Verificar que la función es evaluable
                test_val = f_segura(0, 0)
                if not isinstance(test_val, (int, float)) or math.isnan(test_val) or math.isinf(test_val):
                    print("Error: La función no produce un resultado numérico válido.")
                    continue
                
                break
            except Exception as e:
                print(f"Error: Expresión no válida. {str(e)}")
        
        while True:
            try:
                x0 = float(input("Valor inicial x0: "))
                y0 = float(input("Valor inicial y0: "))
                h = float(input("Tamaño de paso h: "))
                if h <= 0:
                    print("Error: El tamaño de paso debe ser positivo.")
                    continue
                    
                n = int(input("Número de iteraciones: "))
                if n < 1:
                    print("Error: El número de iteraciones debe ser al menos 1.")
                    continue
                    
                break
            except Exception as e:
                print(f"Error: Ingrese valores numéricos válidos. {str(e)}")
        
        resultados = metodo_euler(f_segura, x0, y0, h, n, formato)
        
        if resultados:
            print("\nRESULTADOS FINALES:")
            for i, (x, y) in enumerate(resultados):
                if formato == 2:
                    print(f"Punto {i}: x = {x:.6f}, y ≈ {Fraction(y).limit_denominator()}")
                else:
                    print(f"Punto {i}: x = {x:.6f}, y ≈ {y:.6f}")
    
    elif opcion == 3:
        # Ejecutar ejemplos de demostración
        ejecutar_ejemplos()

def ejecutar_ejemplo_sistema():
    """Ejecuta un ejemplo de sistema de ecuaciones complejo"""
    print("\n═══════════════════════════════════════")
    print("  EJEMPLO: SISTEMA DE ECUACIONES COMPLEJAS")
    print("═══════════════════════════════════════\n")
    
    print("Resolviendo el siguiente sistema de ecuaciones:")
    print("1. 2.5x + √2y - 3z = π")
    print("2. -x + 3/4y + 1.2z = e^1.1")
    print("3. 5!/(10)x - ln(2)y + z = 2^3 - 1")
    
    # Crear la matriz aumentada
    matriz = [
        [2.5, math.sqrt(2), -3, math.pi],
        [-1, 3/4, 1.2, math.exp(1.1)],
        [math.factorial(5)/10, -math.log(2), 1, math.pow(2, 3) - 1]
    ]
    
    print("\nMatriz aumentada del sistema:")
    mostrar_matriz(matriz, 1)  # Mostrar en formato decimal
    
    print("\nResolviendo por el método de Gauss-Jordan...")
    resultado = gauss_jordan(matriz.copy(), 1)
    
    print("\n═══════════════════════════════════════")
    print("SOLUCIÓN DEL SISTEMA DE EJEMPLO:")
    for i in range(3):
        print(f"x_{i+1} = {resultado[i][3]:.6f}")
        
    print("\nLa misma solución en formato fraccionario:")
    for i in range(3):
        print(f"x_{i+1} ≈ {Fraction(resultado[i][3]).limit_denominator()}")

def ejecutar_ejemplo_euler():
    """Ejecuta un ejemplo del método de Euler con una EDO compleja"""
    print("\n═══════════════════════════════════════")
    print("  EJEMPLO: MÉTODO DE EULER CON EDO COMPLEJA")
    print("═══════════════════════════════════════\n")
    
    print("Resolviendo la EDO: dy/dx = sin(x) + ln(y+1) - √(x²)")
    print("Condiciones: x₀ = 0, y₀ = 1, h = 0.1, n = 10")
    
    # Definir la función diferencial
    def f(x, y):
        return math.sin(x) + math.log(y+1) - math.sqrt(x**2)
    
    # Ejecutar el método de Euler
    resultados = metodo_euler(f, 0, 1, 0.1, 10, 1)
    
    print("\nRESULTADOS FINALES:")
    for i, (x, y) in enumerate(resultados):
        print(f"Punto {i}: x = {x:.6f}, y ≈ {y:.6f}")
    
    print("\nLa misma solución en formato fraccionario:")
    for i, (x, y) in enumerate(resultados):
        print(f"Punto {i}: x = {x:.6f}, y ≈ {Fraction(y).limit_denominator()}")

def ejecutar_ejemplos():
    """Ejecuta ejemplos demostrativos del programa"""
    print("\n═══════════════════════════════════════")
    print("  EJEMPLOS DE DEMOSTRACIÓN")
    print("═══════════════════════════════════════\n")
    
    print("1. Sistema de ecuaciones complejas")
    print("2. Método de Euler con EDO compleja")
    print("3. Volver al menú principal")
    
    while True:
        try:
            sub_opcion = int(input("\nSeleccione un ejemplo (1-3): "))
            if sub_opcion not in [1, 2, 3]:
                raise ValueError
            break
        except:
            print("Error: Ingrese 1, 2 o 3.")
    
    if sub_opcion == 1:
        ejecutar_ejemplo_sistema()
    elif sub_opcion == 2:
        ejecutar_ejemplo_euler()
    elif sub_opcion == 3:
        return
    
    input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    try:
        while True:
            main()
            if input("\n¿Desea realizar otra operación? (s/n): ").lower() != 's':
                print("¡Gracias por usar el sistema!")
                break
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        print("El programa se cerrará.")