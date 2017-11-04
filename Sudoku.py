

def Sudoku2dim(ime, n, sez, info=""):
    sq_n = int(n ** 0.5)
    assert (sq_n)**2 == n    # preverimo da je n naravni kvadrat
    zapis = ""
    #vpisani kvadratki
    for y, x, i  in sez:
        zapis += str((x-1)*n + (y-1)*n**2 + i)+" 0\n"
    dolz = len(sez)
    dolz += 4*((n**4 - n**3)//2 + n**2)


    # vsaj en v vsakem kvadratku
    for i in range(n**2):
        a = " ".join(str(j + i*n +1) for j in range(n))
        zapis += a + " 0\n"

    # največ en v vsakem kvadratku
    for i in range(n**2):
        k = n*i
        for a in range(1,n+1): #teče 1 2 3 ... n
            for b in range(a+1,n+1):
                zapis += "{0} {1} 0\n".format(-(a+k), -(b+k))


    VK = []
    for b in range(sq_n):
        for a in range(sq_n):
            VK.append(a * n + b * (n ** 2))

    # vsaj en v vsakem kvadratu
    for st in range(1, n+1):
        for i in range(sq_n):
            for j in range(sq_n):
                rob = i*sq_n*n**2 + j*sq_n*n
                kvadrat = ""
                kvadrat += " ".join(str(rob + x + st) for x in VK)
                kvadrat += " "
                zapis += kvadrat + "0\n"

    # največ en v vsakem kvadratu
    for st in range(1, n + 1):
        for i in range(sq_n):
            for j in range(sq_n):
                rob = i * sq_n * n**2 + j * sq_n * n
                for a in range(n):
                    for b in range(a+1, n):
                        zapis += "{0} {1} 0\n".format(-(rob+st+VK[a]), -(rob+st+VK[b]))

    # vsaj en v vsaki vrstici
    for st in range(1, n + 1):
        for i in range(n):
            a = " ".join(str(i*(n**2) + j*n + st) for j in range(n))
            zapis += a + " 0\n"

    # največ en v vsaki vrstici
    for st in range(1, n + 1):
        for i in range(n):
           for a in range(n):
               for b in range(a+1, n):
                   zapis += "{0} {1} 0\n".format(-(i*(n**2) + a*n + st), -(i*(n**2) + b*n + st))
    # dolz += ((n ** 3) * (n - 1)) // 2

    # vsaj en v vsakem stolpcu
    for st in range(1, n + 1):
        for j in range(n):
            a = " ".join(str(i * (n ** 2) + j * n + st) for i in range(n))
            zapis += a + " 0\n"

    # največ en v vsakem stolpcu
    for st in range(1, n + 1):
        for i in range(n):
            for a in range(n):
                for b in range(a + 1, n):
                    zapis += "{0} {1} 0\n".format(-(a * (n ** 2) + i * n + st), -(b * (n ** 2) + i * n + st))



    ime += ".txt"
    glava = "c SLO:\nc Sudoku velikosti:{0}x{0}\nc Atom p(m n i) je predstavljen kot {1}*(m-1)+{0}*(n-1)+i\n".format(n, n**2)
    glava += "c ENG:\nc Sudoku of size:{0}x{0}\nc Atom p(m n i) is represented by {1}*(m-1)+{0}*(n-1)+i\n".format(n, n**2)

    with open(ime, 'w') as f:
        f.write(glava)
        f.write("c " + info + "\n")
        f.write("c\n")
        f.write("p cnf {0} {1}\n".format(n**3 + len(sez), dolz))
        f.write(zapis)


def dim2Sudoku(ime,n):
    with open(ime, 'r') as f:
        for el in f:
            resitev = el.strip().split()
    resitev = list(map(int, resitev))
    sudoku=[[0 for j in range(n)] for i in range(n)]
    for el in resitev:
        if el > 0:
            vrednost = el % n
            if vrednost == 0:
                vrednost = n

            if el % n**2 == 0:
                y = el // n**2
                y = y-1
                x = n-1

            else:
                y = el // n**2
                x = el % n**2
                if x % n == 0:
                    x = x // n
                    x = x-1
                else:
                    x = x // n
                
            sudoku[y][x] = vrednost
    return sudoku

