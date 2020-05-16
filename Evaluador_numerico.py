from typing import List, Any, Dict
from sympy import var, Eq, solve, sqrt, Equality, Add
from string import ascii_letters

ecuaciones: Dict[str, Any or Add] = {}
lista_sympy = []


def operacion_global(matrix: List[list]):
    """se encarga de ejecutar la evaluacion global paso a paso, aplicando las
    tres posibles alternativas de ejecucion segun la linea, cambiar de ambiente,
    guardar linea, evaluar linea"""

    error = False
    linea_error = -1
    solucion_temporal = []
    for i in range(len(matrix)):
        lectura = matrix[2][i]
        linea = matrix[1][i]
        # cambio de ambiente
        if lectura == 0:
            solucion_temporal = cambio_ambiente(linea)
        # guardar ecuacion/solucion
        elif lectura == 1:
            guardar_ecuacuacion(linea)
        # evaluar
        elif lectura == 2:
            igual = operacion_binaria(linea, solucion_temporal)
            if not igual:
                linea_error = i
                break
        else:
            print("Sintax error, en:", i)
            break


    return linea_error


def guardar_ecuacuacion(e1: str) -> None:
    """guarda la ecuacion o solucion que este de la forma:
     nombre: equacion o nombre: solucion"""
    partes = e1.split(":")
    nombre = partes[0]
    ecuacion = transformar_a_sympy(partes[1])
    ecuaciones[nombre] = ecuacion


def cambio_ambiente(intruccion: str) -> list:
    """ crea una solucion o soluciones aplicando la instruccion ingresada"""
    pass


def operacion_binaria(ecuacion: str, solucion: list) -> bool:
    """evalua numericamente tanto """
    ecuacion = transformar_a_sympy(ecuacion)
    igual = False

    if type(ecuacion) is Equality:

        ecuacion_s = solve(ecuacion)
        for e_sol in ecuacion_s:
            parcial = False
            for sol in solucion:
                if e_sol.equals(sol):
                    parcial = True
            if not parcial:
                igual = False
                break

    else:
        if ecuacion.equals(solucion):
            igual = True

    return igual


def transformar_a_sympy(ecuacion: str):
    """transforma un str a una ecuacion simbolica en sympy, por el momento solo
    se permite nombres de variables con una letra"""

    str_vars = ""
    operadores = ["(", "**", "*", "/", "+", "-", "=", ")"]

    for i in range(len(ecuacion)):
        if ecuacion[i] in ascii_letters and ecuacion[i] not in str_vars:
            if 0 < i < (len(ecuacion) - 1) and ecuacion[i + 1] in operadores and ecuacion[i - 1] in operadores or \
                    i == 0 and ecuacion[i + 1] in operadores or \
                    i == (len(ecuacion) - 1) and ecuacion[i - 1] in operadores:
                str_vars += ecuacion[i] + " "

    if len(str_vars) > 0:
        var(str_vars)

    if "=" not in ecuacion:
        convertida = eval(ecuacion)
    else:
        partes = ecuacion.split("=")
        convertida = Eq(eval(partes[0]), eval(partes[1]))

    return convertida
