from sympy import var, Eq, solve, sqrt, Equality, Add, Symbol
from string import ascii_letters

soluciones_desarrollo = {}
premisas = {}
lista_sympy = []
ecuaciones_totales = {}


# ecuaciones totales es la mezcla entre premisas y soluciones de desarrollo

def operacion_global(matrix: list) -> int:
    """se encarga de ejecutar la evaluacion global paso a paso, aplicando las
    tres posibles alternativas de ejecucion segun la linea, cambiar de ambiente,
    guardar linea, evaluar linea"""
    solucion_temporal = None
    linea_error = -1
    for i in range(len(matrix)):
        print(solucion_temporal)
        lectura = matrix[i][1]
        linea = matrix[i][0]
        # inclusion de premisas:
        print(linea)
        if lectura == 0:
            completo = guardar_ecuacuacion(linea, [], False)
            if not completo:
                print("no se pudo guardar")
                linea_error = i
                break
        # cambio de ambiente
        elif lectura == 1:
            solucion_temporal = cambio_ambiente(linea, solucion_temporal)
            if solucion_temporal is None:
                print("error_de_uso")
                linea_error = i
                break
        # guardar ecuacion/solucion
        elif lectura == 2:
            completo = guardar_ecuacuacion(linea, solucion_temporal)
            if not completo:
                print("operacion incorrecta/no se pudo guardar")
                linea_error = i
                break
        # evaluar
        elif lectura == 3:
            igual = operacion_binaria(linea, solucion_temporal)
            if not igual:
                print("operacion incorrecta")
                linea_error = i
        else:
            print("hay un error en la linea {0} tienes que hablar con Diego\nes su asunto, no mio,\nel fue quien no "
                  "supo que hacer con lo que escribiste\nyo estoy tomando "
                  "la siesta".format(i))

    return linea_error


def guardar_ecuacuacion(e1: str, solucion: list, evaluar=True) -> bool:
    """guarda la ecuacion o solucion que este de la forma:
     nombre: equacion o nombre: solucion"""
    partes = e1.split(":")
    nombre = partes[0]
    good = False
    igual = False
    if evaluar:
        igual = operacion_binaria(partes[1], solucion)
        print(igual)
    else:
        igual = True
    if igual:
        good = True
        ecuacion = transformar_a_sympy(partes[1])
        ecuaciones_totales[nombre] = ecuacion
        if igual:
            soluciones_desarrollo[nombre] = ecuacion
        elif not evaluar:
            premisas[nombre] = ecuacion

    return good


def cambio_ambiente(instruccion: str, antiguas: Add or list or None) -> list or None:
    """ crea una solucion o soluciones aplicando la instruccion ingresada"""
    cambio_amb = []
    listado = instruccion.split()
    etiquetas = ["en", "con", "apl", "aplicando", "y", ","]
    procesos = {"/en/": 1, "en": 1, "con": 2, "/apl/": 3, "apl": 3, "aplicando": 3, "&": "c"}
    niveles = []
    dead_end = False
    base = antiguas
    for elemento in listado:
        niveles.append(procesos.get(elemento, 0))
    # definicion de caminos muertos
    if not camino_muerto(niveles):
        # definir la base
        # cambia la ecuacuacion a trabajar? etiquetas "En" y "con" y otras de nivel 1 o nivel 2:
        if niveles[0] == 3:  # no cambia la ecuacuacion/solucion base
            pass
        else:  # cambia la ecuacuacion a trabajar
            if niveles[0] == 2:
                lista_ecuaciones_base = []
                i = 1
                apply = False
                if listado[0] == 1:
                    while i < len(niveles) and not apply:
                        if niveles[i] == 0:
                            ecuacuion = ecuaciones_totales[listado[i]]
                            lista_ecuaciones_base.append(ecuacuion)
                        elif niveles[i] == 3:
                            apply = True
                    i += 1
                base = solve(lista_ecuaciones_base)
            elif niveles[0] == 1:
                if listado[0] == "/en/":
                    base = transformar_a_sympy(listado[1])
                else:
                    base = ecuaciones_totales[listado[1]]

    else:
        dead_end = True

    # hay aplicaciones ?00
    if not dead_end and 3 in niveles:
        # Definir las aplicaciones(llamadas sustituciones)
        sustituciones = []
        comienzo = niveles.index(3) + 1
        for elemento, nivel in listado[comienzo:], niveles[comienzo:]:
            if nivel == 0:
                sustituciones.append(elemento)

        for eq in base:
            nueva_eq = eq
            for sustitucion in sustituciones:
                susti = soluciones_desarrollo[sustitucion].args
                nueva_eq = nueva_eq.sub(susti[0], susti[1])
            cambio_amb.append(nueva_eq)

    return cambio_amb


def operacion_binaria(ecuacion: str, solucion: list) -> bool:
    """evalua numericamente tanto """
    ecuacion = transformar_a_sympy(ecuacion)
    igual = False

    if solucion is None:
        igual = True

    elif type(ecuacion) is Equality:
        ecuacion_s = solve(ecuacion, variable_despeje(ecuacion))
        for e_sol in ecuacion_s:
            parcial = False
            for sol in solucion:
                if e_sol == sol:
                    parcial = True
            if not parcial:
                break
        if parcial:
            igual = True

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


def variable_despeje(ecuacuacion: Add or Equality) -> Symbol:
    lista_variables = list(ecuacuacion.free_symbols)
    generica = lista_variables[0]
    for opc in lista_variables:
        if str(generica) > str(opc):
            generica = opc
    return generica


def camino_muerto(niveles: list) -> bool:
    dead_end = False
    if 1 in niveles:
        if niveles.count(1) > 1:  # #solo puede haber una aplicacion nivel 1
            dead_end = True
        if niveles.index(1) != 0:  # solo puede estar al inicio
            dead_end = True
        elif 2 in niveles:  # no puede haber los dos mismos tipos de sentencia
            dead_end = True
        elif 3 in niveles and niveles.index(3) > 2:  # solo se puede hacer una por cada llamda
            dead_end = True
        elif len(niveles) > 2:  # solo puede haber una aplicacion nivel 1
            dead_end = True
    elif 2 in niveles:
        if niveles.count(2) > 1:  # #solo puede haber una aplicacion nivel 2
            dead_end = True
        if niveles.index(2) != 0:  # solo puede estar al inicio
            dead_end = True
    elif niveles.count(3) > 1 or niveles.index(3) != 0:
        dead_end = True

    return dead_end

