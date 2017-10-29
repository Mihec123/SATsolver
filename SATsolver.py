from boolean import *

evaluacija = []

def SATsolver(CNF):
    global evaluacija
    #ce je CNF dolzine 0 pomeni da smo zaradi praznih And ali Or dobili T ali F
    if len(CNF) == 0:
        return CNF.evaluate({})
    
    #ce je dolzina CNF enaka 1, to spremenljivko dodamo med evaluacijske in s tem dobimo True
    elif len(CNF) == 1:
        evaluacija.append(CNF)
        return True

    #poiscemo vse unit clause
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
    #za novo evaluacijsko spremenljivko izberemo tisto, ki se
    #pojavi najveckrat
    b=maxpojavitev(CNF)
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


def maxpojavitev(CNF):
    """dobi CNF in vrne element, ki se v CNF pojavi najveckrat"""
    dict = {}
    max = (None, 0)
    for el in CNF:
        for e in el:
            if e in dict:
                dict[e] += 1
                vr = dict[e]
                if max[1] < vr:
                    max = (e, vr)
            else:
                dict[e] = 1
                if max[1] < 1:
                    max = (e, 1)
    return max[0]
    
    

def dimToSat(file):
    """Funkcija nam vrne CNF narejen iz datoteke, ki je v dimacs formatu"""
    conj = []
    with open(file) as f:
        for line in iter(f.readline, ''):
            if line[0] == "p" or line[0] == "c":
                pass
            else:
                ali = []
                temp = line.strip().split()
                for el in temp:
                    if el[0] == "-":
                        ali.append(Not(el[1:]))
                    elif el[0] == "0":
                        break
                    else:
                        ali.append(el)
                conj.append(Or(*ali))
    return And(*conj)
                        


#test = And(Or("p","q"),Or(Not("p"),"r"),Or(Not("q"),Not("r")),Or("q",Not("p"),Not("r")))
# #STRESSTEST
##print("reziltat")
##print(SATsolver(test))
##for el in evaluacija:
##    print(el)
