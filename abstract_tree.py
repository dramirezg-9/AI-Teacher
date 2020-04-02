import operation_tree as o

class abstract_tree(o.o_tree):
    def __init__(self, tree: list, references={}):
        self.key = tree[0][0][0]
        self.branches = []
        if 1 < len(tree):
            for i in range(len(tree[1])):
                self.branches.append(abstract_tree(o.sub_tree(tree, 1, i)))
        self.references = references

    def match(self, check_tree: o.o_tree, posibilities={}, parent=True) -> bool:
        # evitarse código innecesario
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
                    # el orden importa en el resto de operadores
                    for i, j in zip(self.branches, check_tree.branches):
                        if i and j:
                            maybe = {}
                            if not i.match(j, posibilities=maybe, parent=False):
                                return False
                            if not i.join_posibilities(posibilities, maybe):
                                return False
                        else:
                            return False
                # ya que + y * tienen tamaño variable, es necesario preguntarse eso
                elif len(self.branches) == len(check_tree.branches):
                    # el orden no importa
                    local_posible = {}
                    for m, i in enumerate(self.branches):
                        i_exist = False
                        maybe = {}
                        for k, j in enumerate(check_tree.branches):
                            temp = {}
                            if i.match(j, posibilities=temp, parent=False):
                                i_exist = True
                                i.add_posibilities(maybe, temp)
                        if not (i_exist and i.join_posibilities(posibilities, maybe)):
                            return False
                else:
                    return False
            else:
                return False
            if parent:
                if not posibilities.get("all", True):
                    return False
                temp = {}
                delete = []
                for x, y in posibilities.items():
                    if len(y) > 1:
                        temp[x] = []
                        for z in y:
                            temp[x].append(z.get_all_trees())
                    delete += y
                for x, y in posibilities.items():
                    if len(y) > 1:
                        for d in delete:
                            for i, z in enumerate(temp[x].copy()):
                                if d in z[1:]:
                                    posibilities[x].remove(z[0])
                                    del temp[x][i]
                                    break
                print(posibilities)

        # variable
        elif is_variable(self.key) and self.key != 'e':
            if posibilities.get(self.key, "Pending") == "Pending":
                posibilities[self.key] = []
            temp = posibilities[self.key]
            temp.append(check_tree)
            # join_posibilities() va a ser lo que determine después si existe valor que pueda reemplazar a la variable
            return True
        else:
            if self.key == check_tree.key:
                return True
            else:
                return False
        return True

    def check_in_summation(self, check_tree: list, posibilities: dict) -> bool:
        return True

    def join_posibilities(self,posibilities: dict,sub: dict)-> bool:
        keys = sub.keys()
        for x in keys:
            if posibilities.get(x, "Pending") == "Pending":
                posibilities[x] = sub[x]
            else:
                for k in posibilities[x].copy():
                    found = False
                    for l in sub[x]:
                        if k.is_equal(l):
                            found = True
                            break
                    if not found:
                        posibilities[x].remove(k)
                if not posibilities[x]:
                    return False
        return True

    def add_posibilities(self, p1:dict, p2:dict) -> None:
        keys = p2.keys()
        if not p2.get("all", True):
            return
        for x in keys:
            if p1.get(x, "Pending") == "Pending":
                p1[x] = p2[x]
            else:
                for k in p2[x]:
                    done = False
                    for l in p1[x]:
                        if k.is_equal(l):
                            done = True
                            break
                    if not done:
                        p1[x].append(k)



def is_variable(a_ref: str):
    return a_ref.isalpha() and len(a_ref) == 1 and a_ref != "e"
