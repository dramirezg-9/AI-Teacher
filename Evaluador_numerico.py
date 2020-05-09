from sympy import var, Eq
from numpy import zeros
from string import ascii_letters


def operacion_binari_ecuaciones(lista_ecuaciones: list, procesos=0) -> int:
    numero_pasos = len(lista_ecuaciones) - 1
    if procesos == 0:
        procesos = zeros(numero_pasos)

    primer_par = lista_ecuaciones[:-1]
    segundo_par = lista_ecuaciones[1:]

    error = False
    i = 0
    while not error and i < numero_pasos:
        e1 = primer_par[i]
        e2 = segundo_par[i]
        proceso = procesos[i]
        error = evaluar(e1, e2, proceso)



def evaluar(e1: str, e2: str, despejar=False, solucion=None) -> bool:
    # transformar a sympy

    paso1 = transformar_a_sympy(e1, despejar)
    paso2 = transformar_a_sympy(e1, despejar)
    print("jj")
    correcto = False
    if despejar:
        if paso1.equals(paso2):
            correcto = True
    else:
        if solucion is None:
            solucion = solve(paso1)

    return correcto


def transformar_a_sympy(linea: str, despejar=False):
    variables = ""
    operadores = ["**", "*", "/", "+", "-", "=", "==", ")"]

    i = 0
    print(len(linea))
    while i < len(linea):
        if linea[i] in ascii_letters and linea[i] not in variables:
            if 0 < i < (len(linea) - 1) and linea[i + 1] in operadores and linea[i - 1] in operadores or \
                    i == 0 and linea[i + 1] in operadores or \
                    i == (len(linea) - 1) and linea[i - 1] in operadores:
                variables += linea[i] + " "
            variables += linea[i] + " "
            print(variables)
        i += 1

    if len(variables) > 0:
        var(variables)

    if despejar:
        convertida = eval(linea)
    else:
        partes = linea.split("=")
        convertida = Eq(partes[0], partes[1])

    return convertida
