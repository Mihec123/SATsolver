from boolean import *
import sys
import time as t

# definirajmo objek ki je v bistvu seznam literalov, pri katerih je formula "satisfiable", če je drugače vrne false
class literal_table:
    def __init__(self, CNF):
        self.evaluacija = []        # seznam literalov
        self.dolzina = 0            # dolžina seznama, dobro imeti zato, da ne rabimo vedno gledati dolžine evaluacije
        self.resljivost = None      # boolean, ki nam pove če je naš CNF sploh "satisfiable" None pomeni, da smo se "predali"
        self.resljivost = self.generete_from_CNF(CNF)

    def generete_from_CNF(self, CNF):
        # ce je CNF dolzine 0 pomeni da smo zaradi praznih And ali Or dobili T ali F
        if len(CNF) == 0:
            return CNF.evaluate({})

        # ce je dolzina CNF enaka 1, to spremenljivko dodamo med evaluacijske in s tem dobimo True
        elif len(CNF) == 1:
            self.evaluacija.append(CNF)
            self.dolzina += 1
            return True

        # poiscemo vse unit clause
        start_uc = t.time()
        najdeno = False
        literali ={}
        for fi in CNF:
            if len(fi) == 1:
                najdeno = True
                a = fi
                self.evaluacija.append(a)
                self.dolzina += 1
                if isinstance(a, Not):
                    aa = a.x
                    #CNF = CNF.simplifyby(aa, F)
                    literali[aa] = F
                else:
                    #CNF = CNF.simplifyby(a, T)
                    literali[a] = T
        if najdeno:
            end_uc = t.time()
            print("unit clouse: " + str(end_uc - start_uc))
            t_st = t.time()
            CNF = CNF.simplifyby(literali)
            t_end = t.time()
            return self.generete_from_CNF(CNF)
        else:
            end_uc = t.time()
            print("unit clouse: " + str(end_uc - start_uc))

        # if all else fails
        # za novo evaluacijsko spremenljivko izberemo tisto, ki se
        # pojavi najveckrat
        start_maxlit = t.time()
        bb, bool = max_literal(CNF)
        if bool.evaluate({}):
            b = bb
        else:
            b = Not(bb)
        end_maxlit = t.time()
        print("max literal: " + str(end_maxlit - start_maxlit))

        i = self.dolzina + 1
        CNF2 = CNF.simplifyby({bb: bool})
        self.evaluacija.append(b)
        if self.generete_from_CNF(CNF2):
            return True
        else:
            self.evaluacija = self.evaluacija[0:i-1]
            self.dolzina = i
            self.evaluacija.append(Not(b).simplify())
            if bool:
                return self.generete_from_CNF(CNF.simplifyby({bb: F}))
            else:
                return self.generete_from_CNF(CNF.simplifyby({bb: T}))

                                          
def SATsolver(CNF):
    """SATsolver, s pomočjo objekta literal_table in funkcije max_literal"""
    temp = literal_table(CNF)
    if temp.resljivost:
        return (True,temp.evaluacija)
    else:
        return (False, None)




def max_literal(CNF):
    """Funkcija vzame tisti litaral, ki se v eni obliki pojavlja čibmolj večkrat kot v drugi"""
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
    """Funkcija vrne slovar {fi:(#T,#F)}. Ta slovar ki šteje pojavitve literala v trdilni in negalni obliki"""
    dict = {}
    # fi:(#T,#F)
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


# def maxpojavitev(CNF):
#     """dobi CNF in vrne element, ki se v CNF pojavi najveckrat"""
#     dict = {}
#     max = (None, 0)
#     for el in CNF:
#         for e in el:
#             if e in dict:
#                 dict[e] += 1
#                 vr = dict[e]
#                 if max[1] < vr:
#                     max = (e, vr)
#             else:
#                 dict[e] = 1
#                 if max[1] < 1:
#                     max = (e, 1)
#     return max[0]
    

