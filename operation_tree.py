import parsing


class o_tree:

    def __init__(self, tree: list):
        self.key = tree[0][0][0]
        self.branches = []
        if 1 < len(tree):
            for i in range(len(tree[1])):
                self.branches.append(o_tree(sub_tree(tree, 1, i)))


def make_tree(expression: str) -> list:
    raw = parsing.parsing(expression)
    processed = _level_processing(raw)
    tree1 = _levels_to_tree(processed)
    asociative = _asociative_levels(tree1, "")
    return _levels_to_tree(asociative)


def _asociative_levels(tree: list, operation: str) -> list:
    pre1 = []
    insert = False
    if not operation:
        operation = tree[0][0][0]
        insert = True
    temp = []
    for i, x in enumerate(tree[1]):
        if x[0] == operation and operation in asociative_operations:
            temp.append(_asociative_levels(sub_tree(tree, 1, i), operation))
        elif x[1] < x[2]:
            temp.append(_asociative_levels(sub_tree(tree, 1, i), ""))
        else:
            temp.append([[(x[0], 0)]])
    pre2 = _list_list_sum(temp)
    if insert:
        pre2.insert(0, None)
        pre1.append([(operation, len(pre2[1]))])
    return _list_list_sum([pre1, pre2])


def simplify_tree(tree: list) -> list:
    return [[(x[0], x[2] - x[1]) for x in y] for y in tree]


def sub_tree(tree: list, x: int, y: int) -> list:
    n1 = tree[x][y][1]
    n2 = tree[x][y][2]
    start = [[tree[x][y]]]
    temp = []
    if n1 < n2:
        for z in range(n1, n2):
            temp.append(sub_tree(tree, x + 1, z))
    end = _list_list_sum(temp)
    end.insert(0, None)
    levels = simplify_tree(_list_list_sum([start, end]))
    return _levels_to_tree(levels)


def _levels_to_tree(levels: list) -> list:
    indexes = lambda x: [y[1] for y in x]
    indexed_tree = [indexes(x) for x in levels]

    pre_tree1 = []
    for y in indexed_tree:
        count = 0
        pre_tree1.append([])
        for x in y:
            pre_tree1[-1].append(count)
            count += x

    pre_tree2 = []
    for y in indexed_tree:
        count = 0
        pre_tree2.append([])
        for x in y:
            count += x
            pre_tree2[-1].append(count)

    unir = lambda j: [(levels[j][i][0], pre_tree1[j][i], pre_tree2[j][i]) for i in range(len(levels[j]))]
    return [unir(j) for j in range(len(levels))]


def _level_processing(rpa: list) -> list:
    ans = []
    cant = [1]
    level = 0
    for x in reversed(rpa):
        if level < len(ans):
            ans[level].append((x, function_parameters.get(x, 0)))
        else:
            ans.append([(x, function_parameters.get(x, 0))])

        if x in function_parameters:
            level += 1
            if level < len(cant):
                cant[level] += function_parameters[x]
            else:
                cant.append(function_parameters[x])
        if level < len(ans):
            while level > (-1) and cant[level] == len(ans[level]):
                level -= 1
    return ans


def _list_list_sum(lists: list) -> list:
    if not lists:
        return []
    maxl = max(lists, key=lambda x: len(x))
    mini = min(lists, key=lambda x: len(x))
    respuesta = [_func1([x[i] for x in lists]) for i in range(len(mini))]
    respuesta += maxl[len(mini):]
    return respuesta


def _func1(lists: list) -> list:
    respuesta = []
    for x in lists:
        if not (x is None):
            respuesta += x
    return respuesta


function_parameters = {
    "sin": 1,
    "sen": 1,
    "csc": 1,
    "sinh": 1,
    "senh": 1,
    "arcsen": 1,
    "arcsin": 1,
    "cos": 1,
    "sec": 1,
    "cosh": 1,
    "arccos": 1,
    "tan": 1,
    "tanh": 1,
    "arctan": 1,
    "cot": 1,
    "log": 2,
    "ln": 1,
    "-": 1,
    "+": 2,
    "*": 2,
    "/": 2,
    "^": 2
}

asociative_operations = ["+", "*"]
