import operation_tree as o
import abstract_tree as a
import equation as e
compare1 = e.equation("2x+3y=5")
compare2 = e.equation("1x+6y=10")
evaluator = e.abstract_equation("ax+by=c", strict=["x", "y"])
maybe1 = {0: {}}
maybe2 = {0: {}}
evaluator.match(compare1, posibilities=maybe1)
evaluator.match(compare2, posibilities=maybe2)
# maybe[#][w] Posibilidad #, variable w
a1 = int(maybe1[0]["a"].str_tree())
a2 = int(maybe2[0]["a"].str_tree())
b1 = int(maybe1[0]["b"].str_tree())
b2 = int(maybe2[0]["b"].str_tree())
c1 = int(maybe1[0]["c"].str_tree())
c2 = int(maybe2[0]["c"].str_tree())
if a1*b2-a2*b1 != 0:
    print("x:", (b2*c1-b1*c2)/(a1*b2-a2*b1))
    print("y:", (a2*c1-a1*c2)/(a2*b1-a1*b2))
elif b2*c1-b1*c2 == 0:
    print("Misma recta, infinitas soluciones.")
else:
    print("Rectas paralelas, ninguna solución.")