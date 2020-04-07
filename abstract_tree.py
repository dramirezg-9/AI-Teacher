import operation_tree as o


class abstract_tree(o.o_tree):
    """
    Extiende a o_tree.
    Representa una expresión algebraica general o estructura. Útil para aplicar propiedades.

    Atributos:
    references(dict): Diccionario de árboles en los que se puede transformar un árbol con la misma estructura del árbol
                      abstracto.
    strict(list): Variables que obligatoriamente tienen que tomar su propio nombre. (Ejemplo: ["x"] en ax, x siempre
                  debe ser x, mientras que a puede tomar cualquier valor)
    """
    def __init__(self, tree: list, references={}, strict=[]):
        """
        Crea un nuevo árbol abstracto.
        :param tree: El árbol (en su versión de lista de listas) del cual se generará el árbol abstracto.
        :param references: Los árboles en los que se puede "transformar" el árbol abstracto si se cumple el método "match".
        :param strict: Variables que obligatoriamente deben tomar su nombre (x siempre debe ser x por ejemplo).
        """
        self.key = tree[0][0][0]
        self.branches = []
        if 1 < len(tree):
            for i in range(len(tree[1])):
                self.branches.append(abstract_tree(o.sub_tree(tree, 1, i)))
        self.references = references
        self.strict = strict

    # posibilities es un diccionario de diccionarios y cada diccionario tiene una posibilidad de asignación de
    # valores de variables
    def match(self, check_tree: o.o_tree, posibilities={0: {}}, parent=True) -> bool:
        """
        Mira que un árbol tenga la misma estructura que el árbol abstracto.
        :param check_tree: Árbol a ser evaluado.
        :param posibilities: El diccionario que guarda la correspondencia entre variables y valores
        entre ambos árboles. (Ejemplo: ab y 2x, {0: {a: 2,b: x}, 1: {a: x, b:2}}
        :param parent: Indica si el árbol es el padre o es un hijo.
        :return:
        """
        # evitarse código innecesario (all es puesto en Falso cuando alguna variable se queda sin posibilidades)
        if not posibilities.get("all", True):
            return False
        # funciones
        if self.branches:
            # cuando hay sumatorias con una cantidad indeterminada de números
            if check_tree.key == '+' and self.key == 'summation':
                for i in check_tree.branches:
                    if not self.check_in_summation(i, posibilities, self):
                        return False
            # cuando son el mismo operador
            elif self.key == check_tree.key:
                if self.key != '+' and self.key != '*':
                    # el orden importa en los operadores diferentes a '+' y '*', por eso zip
                    for i, j in zip(self.branches, check_tree.branches):
                        if i and j:
                            # se crea un diccionario de posibilidades vacío que será incoporado en el principal
                            maybe = {0: {}}
                            if not i.match(j, posibilities=maybe, parent=False):
                                return False
                            # aqui es incorporado. Si la incorporación no fue exitosa, se retorna falso.
                            if not i.join_posibilities(posibilities, maybe):
                                return False
                        else:
                            return False
                # ya que + y * tienen tamaño variable, es necesario preguntarse eso
                elif len(self.branches) == len(check_tree.branches):
                    # el orden no importa, por lo cual es necesario hacer nested fors (un for dentro de otro)
                    for m, i in enumerate(self.branches):
                        i_exist = False
                        maybe = {}
                        for k, j in enumerate(check_tree.branches):
                            # maybe es la reunión de todos los temp
                            temp = {0: {}}
                            if i.match(j, posibilities=temp, parent=False):
                                i_exist = True
                                # add posibilities tiene un protocolo diferente a join posibilities, cumplen
                                # funciones diferentes
                                i.add_posibilities(maybe, temp)
                        if not (i_exist and i.join_posibilities(posibilities, maybe)):
                            return False
                # significa que '+' y '*' no tienen la misma longitud
                else:
                    return False
            # significa que los operadores no coinciden
            else:
                return False
            # código de ser ejecutado por el árbol padre
            if parent:
                if not posibilities.get("all", True):
                    return False
                # se eliminan todas las posibilidades que no cumplan con las variables estrictas
                for var in self.strict:
                    iterable = list(posibilities.keys()).copy()
                    for posibility in iterable:
                        if posibilities[posibility].get(var, False):
                            if posibilities[posibility][var].str_tree() != var:
                                del posibilities[posibility]
                if not posibilities:
                    return False

        # variable
        elif is_variable(self.key):
            posibilities[0][self.key] = check_tree
            # join_posibilities() va a ser lo que determine después si existe valor que pueda reemplazar a la variable
            return True
        # número
        else:
            if self.key == check_tree.key:
                return True
            else:
                return False
        return True

    def check_in_summation(self, check_tree: list, posibilities: dict) -> bool:
        """
        Función en desarrollo.
        :param check_tree:
        :param posibilities:
        :return:
        """
        return True

    def join_posibilities(self, posibilities: dict, sub: dict) -> bool:
        """
        Diferente de add_posibilities. Une 2 diccionarios de posibilidades. (Ejemplo:
        {0:{a:1, b:2}, 1:{a:0,b:1}} y
        {0:{b:2, c:1}, 1:{b:3, c:0}, 2:{b:2, c:0}}
        -> {0: {a:1, b:2, c:1}, 1: {a:1, b:2, c:0}} Nótese que las posibilidades 1 de ambos diccionarios son descartadas
        ya que b nunca coincide.)
        :param posibilities: Primer diccionario de posibilidades. Este diccionario será modificado.
        :param sub: Segundo diccionario de posibilidades.
        :return: True si la unión fue exitosa, False si no lo fue.
        """
        pending = []
        verify = []
        new_posibilities = []
        # determina si una variable debe "verificarse" porque ya está añadida
        # o debe añadirse porque todavía no lo está
        for x in sub[0].keys():
            if posibilities[0].get(x, "Pending") == "Pending":
                pending.append(x)
            else:
                verify.append(x)
        iterable = list(posibilities.keys()).copy()
        for pos in iterable:
            for pos2 in sub:
                temp = {}
                aligns = True
                # verifica que todas las variables correspondan
                for y in verify:
                    if not posibilities[pos][y].is_equal(sub[pos2][y]):
                        aligns = False
                        break
                if aligns:
                    # verificará que las variables que se añaden no están "repetidas"
                    # (mejor dicho, que no están contenidas en ninguna variable existente)
                    sons = []
                    temp = posibilities[pos].copy()
                    for z in temp:
                        sons += temp[z].get_all_trees()
                    for x in pending:
                        for y in sub[pos2][x].get_all_trees():
                            if y in sons:
                                aligns = False
                                break
                        if aligns:
                            temp[x] = sub[pos2][x]
                        else:
                            break
                if aligns:
                    new_posibilities.append(temp)
        # se cambia el libro diccionario de posibilidades
        if new_posibilities:
            posibilities.clear()
            for i in range(len(new_posibilities)):
                posibilities[i] = new_posibilities[i]
            return True
        return False

    def add_posibilities(self, p1: dict, p2: dict) -> None:
        """
        Diferente de join_posibilities. Añade posibilidades a un diccionario.
        :param p1: Primer diccionario, a este serán añadidas las posibilidades del segundo diccionario.
        :param p2: Segundo diccionario.
        """
        if not p2.get("all", True):
            return
        maxi = -1
        if p1:
            maxi = max(p1.keys())
        for i in p2.keys():
            p1[maxi+i+1] = p2[i]

    def update_references(self, new_references: dict) -> None:
        self.references = new_references

def is_variable(a_ref: str):
    return a_ref.isalpha() and len(a_ref) == 1 and a_ref != "e"
