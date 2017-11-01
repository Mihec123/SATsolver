def primerjava(file1,file2):
    """Funkcija nam vrne CNF narejen iz datoteke, ki je v dimacs formatu"""
    with open(file1) as f:
        for line in iter(f.readline, ''):
            seznam1 = line.split()
            print(len(seznam1))

    with open(file2) as f:
        for line in iter(f.readline, ''):
            seznam2 = line.split()
            print(len(seznam2))

    seznam = []
    seznam_drug = []

    for el in seznam1:
        if el in seznam2:
            pass
        else:
            seznam.append(el)
    for el in seznam2:
        if el in seznam1:
            pass
        else:
            seznam_drug.append(el)
    return seznam,seznam_drug
            
