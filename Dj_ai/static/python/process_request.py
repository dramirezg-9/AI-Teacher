from static.python.evaluador_numerico import operacion_global


def transform_history(history: dict) -> list:
    res = None
    if 'main' in history:
        main = history['main']
        letters = []
        for key in history:
            if key != 'main':
                letters.append((key, history[key]))
        res = []
        for i in range(len(main)):

            # inicializaciones
            equation: str
            ID: str
            equation = main[i]
            ID = None
            eq_type = 'guardar'

            letter: str
            equations: list
            for letter, equations in letters:
                num = 0
                try:
                    num = equations.index(i)
                except:
                    num = -1
                if num != -1:
                    ID = letter + str(num)
                    break

            # inicializacion
            if ID:
                equation = adapt_equation(equation)
                if ID[0] == 'E':
                    eq_type = 'inicializacion'
                else:
                    eq_type = 'guardar'

            # cambio de ambiente
            elif not ID and (('con' in equation) or ('en' in equation) or ('apl' in equation)):
                eq_type = 'cambio'
                equation = equation.replace(',', ' ')
                equation = equation.replace('&', ' ')
                equation = equation.replace(' y ', ' ')

            # ecuacion y desarrollo
            else:
                equation = adapt_equation(equation)
                eq_type = 'desarrollo'

            numeros = {
                'inicializacion': 0,
                'cambio': 1,
                'guardar': 2,
                'desarrollo': 3
            }
            number = numeros[eq_type]
            add = equation
            if ID:
                add = ID + ':' + equation
            res.append([add, number])
        return res


def adapt_equation(equation: str) -> str:
    temp = equation.replace(' ', '')
    operators = ['+', '-', '*', '/', '^', '=']
    last = ''
    res = ''
    for x in temp:
        if x.isalpha():
            if last in operators or not last:
                res += x
            else:
                res += '*' + x
        else:
            res += x
        last = x
    return res


def process_request(history: dict):
    history2 = transform_history(history)
    print(history2)
    return {'error': operacion_global(history2)}
