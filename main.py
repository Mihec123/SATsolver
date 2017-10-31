from SATsolver import SATsolver
from boolean import *

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


def SatToDim(evaluacija, file):
    zapis = ""
    for el in evaluacija:
        if isinstance(el, Not):
            zapis += "-" + str(el.x) + " "
        else:
            zapis += str(el) + " "
    with open(file, 'w') as f:
        f.write(zapis)


def main(argv):
    """funkcija kot argument dobi seznam argv = [input.txt, output.txt] in resi SAT problem podan z input.txt
    ce resitve ne najdemo v output.txt zapise le 0"""
    global evaluacija

    # Najprej klicemo zapis v file na seznamu, ki vsebuje samo nulo. V primeru
    # da uporabnik prekine program bo torej resitev 0
    SatToDim(["0"], argv[1])

    CNF = dimToSat(argv[0])
    boolean = SATsolver(CNF)
    SatToDim(evaluacija, argv[1])


# del, ki se zazene ko klicemo program
##if __name__ == "__main__":
##    main(sys.argv[1:])


