from boolean import *
import sys

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

def max_literal(CNF):
    # funkcija vzame tisti litaral, ki se v eni obliki pojavlja čibmolj večkrat kot v drugi
    # če se pojavlja samo v eni obliki, bo pač vzel tistega
    variables = strip_info(CNF)
    max_k = None
    # razmerje je podano z obratnim številom da se izognemo deljenju z 0
    max_val = 2
    for k,v in variables.items():
        t,f = v
        if t>f:
            if f/t < max_val:
                max_k,max_val = (k, T), f/t
        else:
            if t/f < max_val:
                max_k, max_val = (k, F), t/f
        if max_val == 0:
            return max_k
    return max_k


def strip_info(CNF):
    dict = {}
    # fi:(#T,#F) slovar ki šteje kolikokrat se pojavi literal v trdilni in negalni obliki
    for dis in CNF:
        for fi in dis:
            if isinstance(fi, Not):
                if fi.x in dict:
                    t, f = dict[fi.x]
                    dict[fi.x] = t, f + 1
                else:
                    dict[fi.x] = (0,1)
            else:
                if fi in dict:
                    t, f = dict[fi]
                    dict[fi] = t + 1, f
                else:
                    dict[fi] = (1,0)
    return dict



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
                dict = line.strip().split()
                for el in dict:
                    if el[0] == "-":
                        ali.append(Not(el[1:]))
                    elif el[0] == "0":
                        break
                    else:
                        ali.append(el)
                conj.append(Or(*ali))
    return And(*conj)


def SatToDim(evaluacija,file):
    zapis = ""
    for el in evaluacija:
        if isinstance(el, Not):
            zapis += "-" + str(el.x)+ " "
        else:
            zapis += str(el)+ " "
    with open(file, 'w') as f:
        f.write(zapis)
    
        

def main(argv):
    """funkcija kot argument dobi seznam argv = [input.txt, output.txt] in resi SAT problem podan z input.txt
    ce resitve ne najdemo v output.txt zapise le 0"""
    global evaluacija
    
    #Najprej klicemo zapis v file na seznamu, ki vsebuje samo nulo. V primeru
    #da uporabnik prekine program bo torej resitev 0
    SatToDim(["0"],argv[1])
    
    CNF = dimToSat(argv[0])
    boolean = SATsolver(CNF)
    SatToDim(evaluacija,argv[1])

    #nastavimo evaluacijo na prazen seznam, da lahko ponovno poklicemo metodo
    evaluacija = []
    
#del, ki se zazene ko klicemo program    
##if __name__ == "__main__":
##    main(sys.argv[1:])


