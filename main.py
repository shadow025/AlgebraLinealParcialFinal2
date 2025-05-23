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

def mostrar_ecuaciones(matriz):
    """Muestra el sistema de ecuaciones en formato estándar"""
    print("\nSistema de ecuaciones:")
    for i, fila in enumerate(matriz):
        ecuacion = ""
        for j, coef in enumerate(fila[:-1]):
            if j == 0:
                if coef != 0:
                    if coef == 1:
                        ecuacion += f"x{j+1}"
                    elif coef == -1:
                        ecuacion += f"-x{j+1}"
                    else:
                        ecuacion += f"{coef}x{j+1}"
            else:
                if coef > 0:
                    if coef == 1:
                        ecuacion += f" + x{j+1}"
                    else:
                        ecuacion += f" + {coef}x{j+1}"
                elif coef < 0:
                    if coef == -1:
                        ecuacion += f" - x{j+1}"
                    else:
                        ecuacion += f" - {abs(coef)}x{j+1}"
        ecuacion += f" = {fila[-1]}"
        print(f"Ecuación {i+1}: {ecuacion}")

def eliminacion_gaussiana(matriz, formato):
    """Realiza eliminación gaussiana básica (no Gauss-Jordan)"""
    if not matriz:
        raise ValueError("La matriz está vacía")
        
    filas = len(matriz)
    columnas = len(matriz[0])
    paso = 1
    
    # Copiamos la matriz para no modificar la original
    matriz_trabajo = [fila[:] for fila in matriz]
    
    print("\n══════════════════════════════════════════")
    print("  MÉTODO: ELIMINACIÓN GAUSSIANA")
    print("══════════════════════════════════════════")
    
    for i in range(min(filas, columnas - 1)):
        # Pivoteo parcial
        max_fila = i
        max_valor = abs(matriz_trabajo[i][i]) if i < len(matriz_trabajo) and i < len(matriz_trabajo[i]) else 0
        
        for k in range(i + 1, filas):
            if k < len(matriz_trabajo) and i < len(matriz_trabajo[k]) and abs(matriz_trabajo[k][i]) > max_valor:
                max_fila = k
                max_valor = abs(matriz_trabajo[k][i])
        
        # Si el máximo es cero, continuar
        if max_valor < 1e-10:
            print(f"\nPaso {paso}: El pivote es cero, se omite la columna {i+1}")
            paso += 1
            continue
            
        # Intercambiar filas si es necesario
        if max_fila != i:
            matriz_trabajo[i], matriz_trabajo[max_fila] = matriz_trabajo[max_fila], matriz_trabajo[i]
            print(f"\nPaso {paso}: Intercambiar F{i+1} ↔ F{max_fila+1}")
            mostrar_matriz(matriz_trabajo, formato)
            paso += 1
        
        # Eliminación hacia abajo
        for k in range(i + 1, filas):
            if abs(matriz_trabajo[k][i]) > 1e-10:
                factor = matriz_trabajo[k][i] / matriz_trabajo[i][i]
                for j in range(i, columnas):
                    matriz_trabajo[k][j] -= factor * matriz_trabajo[i][j]
                    
                print(f"\nPaso {paso}: F{k+1} = F{k+1} - ({Fraction(factor).limit_denominator()} × F{i+1})")
                mostrar_matriz(matriz_trabajo, formato)
                paso += 1
                
    return matriz_trabajo

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
    
    print("\n══════════════════════════════════════════")
    print("  MÉTODO: GAUSS-JORDAN")
    print("══════════════════════════════════════════")
    
    for i in range(min(filas, columnas - 1)):
        # Pivoteo parcial
        max_fila = i
        max_valor = abs(matriz_trabajo[i][i]) if i < len(matriz_trabajo) and i < len(matriz_trabajo[i]) else 0
        
        for k in range(i + 1, filas):
            if k < len(matriz_trabajo) and i < len(matriz_trabajo[k]) and abs(matriz_trabajo[k][i]) > max_valor:
                max_fila = k
                max_valor = abs(matriz_trabajo[k][i])
        
        # Si el máximo es cero, continuar
        if max_valor < 1e-10:
            print(f"\nPaso {paso}: El pivote es cero, se omite la columna {i+1}")
            paso += 1
            continue
            
        # Intercambiar filas si es necesario
        if max_fila != i:
            matriz_trabajo[i], matriz_trabajo[max_fila] = matriz_trabajo[max_fila], matriz_trabajo[i]
            print(f"\nPaso {paso}: Intercambiar F{i+1} ↔ F{max_fila+1}")
            mostrar_matriz(matriz_trabajo, formato)
            paso += 1
        
        # Normalización (hacer el pivote = 1)
        pivote = matriz_trabajo[i][i]
        if abs(pivote) < 1e-10:
            continue
            
        for j in range(i, columnas):
            matriz_trabajo[i][j] /= pivote
            
        print(f"\nPaso {paso}: Normalizar F{i+1} (÷ {Fraction(pivote).limit_denominator()})")
        mostrar_matriz(matriz_trabajo, formato)
        paso += 1
        
        # Eliminación completa (hacia arriba y hacia abajo)
        for k in range(filas):
            if k != i and abs(matriz_trabajo[k][i]) > 1e-10:
                factor = matriz_trabajo[k][i]
                for j in range(i, columnas):
                    matriz_trabajo[k][j] -= factor * matriz_trabajo[i][j]
                    
                print(f"\nPaso {paso}: F{k+1} = F{k+1} - ({Fraction(factor).limit_denominator()} × F{i+1})")
                mostrar_matriz(matriz_trabajo, formato)
                paso += 1
                
    # Limpiar valores muy pequeños
    for i in range(filas):
        for j in range(columnas):
            if abs(matriz_trabajo[i][j]) < 1e-10:
                matriz_trabajo[i][j] = 0.0
                
    return matriz_trabajo

def metodo_sustitucion(matriz, formato):
    """Resuelve por sustitución (para sistemas 2x2 principalmente)"""
    print("\n══════════════════════════════════════════")
    print("  MÉTODO: SUSTITUCIÓN")
    print("══════════════════════════════════════════")
    
    if len(matriz) != 2 or len(matriz[0]) != 3:
        print("El método de sustitución está optimizado para sistemas 2x2")
        print("Aplicando eliminación gaussiana...")
        return eliminacion_gaussiana(matriz, formato)
    
    # Sistema 2x2: ax + by = e, cx + dy = f
    a, b, e = matriz[0]
    c, d, f = matriz[1]
    
    print(f"Sistema original:")
    print(f"Ecuación 1: {a}x + {b}y = {e}")
    print(f"Ecuación 2: {c}x + {d}y = {f}")
    
    # Resolver x en términos de y desde la primera ecuación
    if abs(a) > 1e-10:
        print(f"\nPaso 1: Despejar x de la primera ecuación")
        print(f"x = ({e} - {b}y) / {a}")
        print(f"x = {e/a} - {b/a}y")
        
        # Sustituir en la segunda ecuación
        print(f"\nPaso 2: Sustituir en la segunda ecuación")
        print(f"{c}({e/a} - {b/a}y) + {d}y = {f}")
        
        # Simplificar
        coef_y = -c*b/a + d
        termino_independiente = f - c*e/a
        
        print(f"{c*e/a} - {c*b/a}y + {d}y = {f}")
        print(f"{coef_y}y = {termino_independiente}")
        
        if abs(coef_y) > 1e-10:
            y = termino_independiente / coef_y
            x = (e - b*y) / a
            
            print(f"\nPaso 3: Resolver para y")
            print(f"y = {termino_independiente} / {coef_y} = {y}")
            
            print(f"\nPaso 4: Sustituir y calcular x")
            print(f"x = ({e} - {b}*{y}) / {a} = {x}")
            
            if formato == 2:
                print(f"\nSOLUCIÓN:")
                print(f"x = {Fraction(x).limit_denominator()}")
                print(f"y = {Fraction(y).limit_denominator()}")
            else:
                print(f"\nSOLUCIÓN:")
                print(f"x = {x:.6f}")
                print(f"y = {y:.6f}")
                
            return [[1, 0, x], [0, 1, y]]
        else:
            print("Sistema inconsistente o con infinitas soluciones")
            return matriz
    else:
        print("No se puede despejar x de la primera ecuación, usando método alternativo...")
        return eliminacion_gaussiana(matriz, formato)

def metodo_igualacion(matriz, formato):
    """Resuelve por igualación (para sistemas 2x2 principalmente)"""
    print("\n══════════════════════════════════════════")
    print("  MÉTODO: IGUALACIÓN")
    print("══════════════════════════════════════════")
    
    if len(matriz) != 2 or len(matriz[0]) != 3:
        print("El método de igualación está optimizado para sistemas 2x2")
        print("Aplicando eliminación gaussiana...")
        return eliminacion_gaussiana(matriz, formato)
    
    # Sistema 2x2: ax + by = e, cx + dy = f
    a, b, e = matriz[0]
    c, d, f = matriz[1]
    
    print(f"Sistema original:")
    print(f"Ecuación 1: {a}x + {b}y = {e}")
    print(f"Ecuación 2: {c}x + {d}y = {f}")
    
    # Despejar x de ambas ecuaciones
    if abs(a) > 1e-10 and abs(c) > 1e-10:
        print(f"\nPaso 1: Despejar x de ambas ecuaciones")
        print(f"De la ecuación 1: x = ({e} - {b}y) / {a}")
        print(f"De la ecuación 2: x = ({f} - {d}y) / {c}")
        
        print(f"\nPaso 2: Igualar las expresiones")
        print(f"({e} - {b}y) / {a} = ({f} - {d}y) / {c}")
        
        print(f"\nPaso 3: Resolver la ecuación resultante")
        print(f"{c}({e} - {b}y) = {a}({f} - {d}y)")
        print(f"{c*e} - {c*b}y = {a*f} - {a*d}y")
        print(f"{c*e} - {a*f} = {c*b}y - {a*d}y")
        print(f"{c*e - a*f} = {c*b - a*d}y")
        
        denominador_y = c*b - a*d
        if abs(denominador_y) > 1e-10:
            y = (c*e - a*f) / denominador_y
            x = (e - b*y) / a
            
            print(f"y = {c*e - a*f} / {denominador_y} = {y}")
            
            print(f"\nPaso 4: Calcular x")
            print(f"x = ({e} - {b}*{y}) / {a} = {x}")
            
            if formato == 2:
                print(f"\nSOLUCIÓN:")
                print(f"x = {Fraction(x).limit_denominator()}")
                print(f"y = {Fraction(y).limit_denominator()}")
            else:
                print(f"\nSOLUCIÓN:")
                print(f"x = {x:.6f}")
                print(f"y = {y:.6f}")
                
            return [[1, 0, x], [0, 1, y]]
        else:
            print("Sistema inconsistente o con infinitas soluciones")
            return matriz
    else:
        print("No se pueden despejar las variables, usando método alternativo...")
        return eliminacion_gaussiana(matriz, formato)

def resolver_sistema(matriz, metodo, formato):
    """Resuelve un sistema de ecuaciones con el método seleccionado"""
    try:
        filas = len(matriz)
        columnas = len(matriz[0]) - 1
        
        # Mostrar sistema original
        mostrar_ecuaciones(matriz)
        mostrar_matriz(matriz, formato)
        
        # Aplicar el método seleccionado
        if metodo == 1:  # Eliminación Gaussiana
            resultado = eliminacion_gaussiana(matriz.copy(), formato)
        elif metodo == 2:  # Gauss-Jordan
            resultado = gauss_jordan(matriz.copy(), formato)
        elif metodo == 3:  # Sustitución
            resultado = metodo_sustitucion(matriz.copy(), formato)
        elif metodo == 4:  # Igualación
            resultado = metodo_igualacion(matriz.copy(), formato)
        
        # Para eliminación gaussiana, necesitamos sustitución hacia atrás
        if metodo == 1:
            print("\n══════════════════════════════════════════")
            print("  SUSTITUCIÓN HACIA ATRÁS")
            print("══════════════════════════════════════════")
            soluciones = sustitucion_hacia_atras(resultado, formato)
            mostrar_solucion_final(soluciones, formato)
        elif metodo in [2, 3, 4]:
            # Verificar consistencia y mostrar solución
            verificar_y_mostrar_solucion(resultado, formato)
                
    except Exception as e:
        print(f"\nError durante el cálculo: {str(e)}")

def sustitucion_hacia_atras(matriz, formato):
    """Realiza sustitución hacia atrás después de eliminación gaussiana"""
    filas = len(matriz)
    columnas = len(matriz[0]) - 1
    soluciones = [0] * columnas
    
    # Empezar desde la última fila
    for i in range(filas - 1, -1, -1):
        # Encontrar la primera variable no cero
        pivote_col = -1
        for j in range(columnas):
            if abs(matriz[i][j]) > 1e-10:
                pivote_col = j
                break
        
        if pivote_col == -1:
            continue
            
        # Calcular el valor de la variable
        suma = 0
        for j in range(pivote_col + 1, columnas):
            suma += matriz[i][j] * soluciones[j]
        
        soluciones[pivote_col] = (matriz[i][-1] - suma) / matriz[i][pivote_col]
        
        print(f"x{pivote_col+1} = ({matriz[i][-1]} - {suma}) / {matriz[i][pivote_col]} = {soluciones[pivote_col]}")
    
    return soluciones

def verificar_y_mostrar_solucion(resultado, formato):
    """Verifica la consistencia del sistema y muestra la solución"""
    filas = len(resultado)
    columnas = len(resultado[0]) - 1
    
    # Verificar inconsistencia
    for i in range(filas):
        if all(abs(resultado[i][j]) < 1e-10 for j in range(columnas)) and abs(resultado[i][-1]) > 1e-10:
            print("\n¡SISTEMA INCONSISTENTE! No existe solución.")
            return
    
    # Mostrar solución
    print("\n═══════════════════════════════════════")
    print("SOLUCIÓN DEL SISTEMA:")
    
    for i in range(min(filas, columnas)):
        if abs(resultado[i][i]) > 1e-10:
            valor = resultado[i][-1]
            if formato == 2:
                print(f"x_{i+1} = {Fraction(valor).limit_denominator()}")
            else:
                print(f"x_{i+1} = {valor:.6f}")

def mostrar_solucion_final(soluciones, formato):
    """Muestra la solución final del sistema"""
    print("\n═══════════════════════════════════════")
    print("SOLUCIÓN FINAL DEL SISTEMA:")
    
    for i, sol in enumerate(soluciones):
        if formato == 2:
            print(f"x_{i+1} = {Fraction(sol).limit_denominator()}")
        else:
            print(f"x_{i+1} = {sol:.6f}")

def main():
    print("══════════════════════════════════════════════")
    print("  SISTEMA DE RESOLUCIÓN DE ECUACIONES LINEALES")
    print("══════════════════════════════════════════════\n")
    print("MÉTODOS DISPONIBLES:")
    print("1. Eliminación Gaussiana")
    print("2. Gauss-Jordan")
    print("3. Sustitución")
    print("4. Igualación")
    print("5. Ejemplos de demostración")
    print("6. Salir")
    
    while True:
        try:
            opcion = int(input("\nSeleccione una opción (1-6): "))
            if opcion not in [1, 2, 3, 4, 5, 6]:
                raise ValueError
            break
        except:
            print("Error: Ingrese un número entre 1 y 6.")
    
    if opcion == 6:
        print("¡Gracias por usar el sistema!")
        return
    
    if opcion == 5:
        ejecutar_ejemplos()
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
    
    # Ingreso del sistema
    print("\n═══════════════════════════════════════")
    print("  INGRESO DEL SISTEMA DE ECUACIONES")
    print("═══════════════════════════════════════\n")
    
    while True:
        try:
            filas = int(input("Número de ecuaciones: "))
            columnas = int(input("Número de variables: "))
            if filas < 1 or columnas < 1:
                raise ValueError
            break
        except:
            print("Error: Ingrese números enteros positivos.\n")
    
    # Ingreso de coeficientes
    print("\nINGRESO DE COEFICIENTES:")
    print("Ejemplos de formato aceptado:")
    print("- Números: 2, -3.5, 0")
    print("- Fracciones: 1/2, 3/4")
    print("- Exponentes: 2^3, 5^2")
    print("- Raíces: √2, 3√8")
    print("- Constantes: π, e")
    
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
    
    # Resolver el sistema
    resolver_sistema(matriz_aumentada, opcion, formato)

def ejecutar_ejemplos():
    """Ejecuta ejemplos demostrativos con diferentes métodos"""
    print("\n═══════════════════════════════════════")
    print("  EJEMPLOS DE DEMOSTRACIÓN")
    print("═══════════════════════════════════════\n")
    
    print("1. Sistema 2x2 - Todos los métodos")
    print("2. Sistema 3x3 - Eliminación Gaussiana")
    print("3. Sistema 3x3 - Gauss-Jordan")
    print("4. Volver al menú principal")
    
    while True:
        try:
            sub_opcion = int(input("\nSeleccione un ejemplo (1-4): "))
            if sub_opcion not in [1, 2, 3, 4]:
                raise ValueError
            break
        except:
            print("Error: Ingrese 1, 2, 3 o 4.")
    
    if sub_opcion == 4:
        return
    
    if sub_opcion == 1:
        # Sistema 2x2
        print("\nEjemplo: Sistema 2x2")
        print("2x + 3y = 7")
        print("x - y = 1")
        
        matriz = [[2, 3, 7], [1, -1, 1]]
        
        for metodo in range(1, 5):
            metodos = ["", "Eliminación Gaussiana", "Gauss-Jordan", "Sustitución", "Igualación"]
            print(f"\n{'='*50}")
            print(f"RESOLVIENDO CON: {metodos[metodo]}")
            print(f"{'='*50}")
            resolver_sistema([fila[:] for fila in matriz], metodo, 1)
            input("\nPresione Enter para continuar...")
    
    elif sub_opcion == 2:
        # Sistema 3x3 - Eliminación Gaussiana
        print("\nEjemplo: Sistema 3x3 con Eliminación Gaussiana")
        print("2x + y - z = 8")
        print("-3x - y + 2z = -11")
        print("-2x + y + 2z = -3")
        
        matriz = [[2, 1, -1, 8], [-3, -1, 2, -11], [-2, 1, 2, -3]]
        resolver_sistema(matriz, 1, 1)
    
    elif sub_opcion == 3:
        # Sistema 3x3 - Gauss-Jordan
        print("\nEjemplo: Sistema 3x3 con Gauss-Jordan")
        print("x + 2y + 3z = 6")
        print("2x + 3y + z = 7")
        print("3x + y + 2z = 8")
        
        matriz = [[1, 2, 3, 6], [2, 3, 1, 7], [3, 1, 2, 8]]
        resolver_sistema(matriz, 2, 2)
    
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