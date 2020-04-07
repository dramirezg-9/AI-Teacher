import operation_tree as o
import abstract_tree as a


class equation:
    """
    Representa una ecuación.

    Atributos:
    left(o_tree): Árbol de operaciones que representa el lado izquierdo de la ecuación.
    right(o_tree): Árbol de operaciones que representa el lado derecho de la ecuación.
    """
    def __init__(self, expression: str):
        sides = expression.split("=")
        self.left = o.o_tree(o.make_tree(sides[0]))
        self.right = o.o_tree(o.make_tree(sides[1]))


class abstract_equation(equation):
    """
    Extiende a equation. Representa a una ecuación general.

    Atributos:

    left y right son ahora abstract_tree
    references: Ecuaciones en las cuales se puede transformar una ecuación con la misma estructura.
    """
    def __init__(self, expression: str, references={}, strict=[]):
        sides = expression.split("=")
        self.left = a.abstract_tree(o.make_tree(sides[0]), references=references.get("left", {}), strict=strict)
        self.right = a.abstract_tree(o.make_tree(sides[1]), references=references.get("right", {}), strict=strict)
        self.references = references.get("general", {})

    def match(self, check_equation: equation, posibilities={0: {}}) -> bool:
        """
        Verifica que una ecuación cumple con la estructura de una ecuación abstracta.
        :param check_equation: Ecuación a ser evaluada
        :param posibilities: El diccionario que guarda la correspondencia entre variables y valores
        entre ambas ecuaciones. (Ejemplo: ab y 2x, {0: {a: 2,b: x}, 1: {a: x, b:2}}
        :return: True si la ecuación cumple con la estructura de la ecuación abstracta, False de lo contrario.
        """
        if not self.left.match(check_equation.left, posibilities=posibilities, parent=True):
            return False
        pos_right = {0: {}}
        if not self.right.match(check_equation.right, posibilities=pos_right, parent=True):
            return False
        if not self.left.join_posibilities(posibilities, pos_right):
            return False
        return True
