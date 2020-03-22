def parsing(expression: str) -> list:
    nums = []
    # nums es lo que devolverá el programa y será tratado como un stack de strings

    operations = []
    # operations será el stack donde almacenaremos las operaciones para después
    # trasladarlas a nums

    elevated_buffer = []
    # elevated_buffer tendrá los nums de las expresiones a las que se elevan
    # únicamente las funciones (sen^(2)) -> ["2"]

    last = ""
    # last acumulará los números
    beforegoes = "nothing"
    # beforegoes dirá qué es lo que viene antes de la expresión que se está evaluando

    length = len(expression)
    # length nos servirá para hacer un forloop un poco rudimentario.

    i = 0
    while i < length:
        x = expression[i]
        numeric = _isnumber(x)
        operator = _isoperator(x)
        letter = x.isalpha()
        if numeric:
            last += x
        else:
            if last:
                nums.append(last)
                if (beforegoes == "number" or beforegoes == "letter" or
                        beforegoes == "closed_parenthesis"):
                    nums.append("*")
                last = ""
                beforegoes = "number"
            if operator:
                temp = _getlast(operations, "(")
                while (_op_compare(temp, x)):
                    nums.append(temp)
                    operations.pop()
                    if not _isoperator(temp) and temp != "(":  # o, es función
                        _elevate_function(nums, elevated_buffer)
                    temp = _getlast(operations, "(")
                if x == "-" and (beforegoes != "nothing" or beforegoes != "function"):
                    operations.append("+")
                operations.append(x)
                beforegoes = "operator"
            elif x == "(":
                if (beforegoes == "number" or beforegoes == "letter" or
                        beforegoes == "closed_parenthesis"):
                    operations.append("*")
                operations.append(x)
                beforegoes = "nothing"
            elif x == "," or x == ")":
                temp = operations[-1]
                while temp != "(":
                    nums.append(temp)
                    if not _isoperator(temp):  # o, es función
                        _elevate_function(nums, elevated_buffer)
                    operations.pop()
                    temp = operations[-1]
                if x == ")":
                    operations.pop()
                    beforegoes = "closed_parenthesis"
                else:
                    beforegoes = "nothing"
            elif letter:
                temp = ""
                j = i
                size = 1
                tentative = ""
                tentative_index = j
                # another rudimentary for
                while j < length:
                    temp += expression[j]
                    check = _check_is_function(temp, size)
                    if check["tentative"]:
                        tentative = temp
                        tentative_index = j
                    if check["count"] == 0:
                        if tentative:
                            if expression[tentative_index + 1] == "^":
                                count = 0
                                k = tentative_index + 2
                                len2 = 1
                                # another rudimentary for
                                while k < length:
                                    if expression[k] == "(":
                                        count += 1
                                    elif expression[k] == ")":
                                        count -= 1
                                    if count == 0:
                                        break
                                    len2 += 1
                                    k += 1
                                elevation = expression[tentative_index + 2:tentative_index + 2 + len2]
                                if elevation == "(-1)":
                                    tentative += "^(-1)"
                                    elevated_buffer.append(parsing("1"))
                                else:
                                    elevated_buffer.append(parsing(elevation))

                                operations.append("^")
                                i = tentative_index + 1 + len2
                            else:
                                i = tentative_index
                                elevated_buffer.append(parsing("1"))
                            if (beforegoes == "number" or beforegoes == "letter" or
                                    beforegoes == "closed_parenthesis"):
                                operations.append("*")
                            operations.append(tentative)
                            beforegoes = "function"
                        else:
                            nums.append(x)
                            if (beforegoes == "number" or beforegoes == "letter" or
                                    beforegoes == "closed_parenthesis"):
                                nums.append("*")
                            beforegoes = "letter"
                        break
                    j += 1
                    size += 1

        i += 1
    if last:
        nums.append(last)
        if (beforegoes == "number" or beforegoes == "letter" or
                beforegoes == "closed_parenthesis"):
            nums.append("*")
    while operations:
        temp = operations.pop()
        nums.append(temp)
        if not _isoperator(temp):  # o, es función
            _elevate_function(nums, elevated_buffer)
    return nums


def _isnumber(char: str) -> bool:
    return char.isdecimal() or char == "."


def _isoperator(char: str) -> bool:
    return (char == "+" or char == "-" or char == "*"
            or char == "/" or char == "^")


def _getlast(array: list, ifnot: str) -> str:
    if array:
        return array[-1]
    return ifnot


def _elevate_function(nums: list, elevated_buffer: list) -> None:
    temp2 = elevated_buffer.pop()
    if temp2 != parsing("1"):
        while temp2:
            nums.append(temp2.pop(0))


def _check_is_function(string: str, size: int) -> dict:
    respuesta = {"tentative": False}
    count = 0
    for y in [z[:size] for z in function_index]:
        if string == y:
            count += 1
            if string in function_index:
                respuesta["tentative"] = True
    respuesta["count"] = count
    return respuesta


def _op_compare(x: str, y: str) -> bool:
    x0 = (x == "(")
    x1 = (x == "^")
    x3 = (x == "*" or x == "/")
    x4 = (x == "+" or x == "-")
    x2 = (not (x0 or x1 or x3 or x4))
    y1 = (y == '^')
    y3 = (y == '+' or y == '-')
    if x0 or y1:
        return False
    elif y3:
        return x1 or x2 or x3 or x4
    return x1 or x2 or x3


function_index = ["sin", "sen", "csc", "sinh", "senh", "arcsen", "arcsin",
                  "cos", "sec", "cosh", "arccos", "tan", "tanh", "arctan",
                  "cot", "log", "ln"]