from boolean import *

evaluacija = []

def SATsolver(CNF):
    global evaluacija
    if len(CNF) == 0:
        return CNF.evaluate({})

    elif len(CNF) == 1:
        evaluacija.append(CNF)
        return True

    for fi in CNF:
        if len(fi)==1:
            a = fi
            evaluacija.append(a)
            if isinstance(a, Not):
                aa = a.x
                CNF = CNF.simplifyby(aa, F)
            else:
                CNF = CNF.simplifyby(a,T)
            return SATsolver(CNF)

    #if all else fails
    b=next(iter((next((iter(CNF))))))
    #print(b)
    if isinstance(b, Not):
        bb = b.x
        bool = F

    else:
        bb = b
        bool = T

    i = len(evaluacija)
    CNF2 = CNF.simplifyby(bb, bool)
    evaluacija.append(b)
    if SATsolver(CNF2):
        return True
    else:
        evaluacija = evaluacija[0:i]
        evaluacija.append(Not(b).simplify())
        return SATsolver(CNF.simplifyby(bb, Not(bool).simplify()))


test = And(Or("p","q"),Or(Not("p"),"r"),Or(Not("q"),Not("r")),Or("q",Not("p"),Not("r")))
# #STRESSTEST
for _ in range(999):
    print("reziltat")
    print(SATsolver(test))
    for el in evaluacija:
        print(el)