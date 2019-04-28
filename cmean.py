import math
import numpy as np

def Diff_R_RNew(R, RNew, n, K):
    diff_R = [0] * K

    for j in range(K):
        diff_R.append(EuclidDistance(R[j], RNew[j], n))

    DiffMax = max(diff_R)

    return DiffMax


def CalculeNouveauRepresentants(R, O, n, K, classe, CardClass):
    RNew = [[0] * n] * K

    # add all representatives
    for i in range(len(O)):
        RNew[classe[i] - 1] = np.add(RNew[classe[i] - 1], O[i]).tolist()

    # get average of representatives
    for i in range(K):
        RNew[i] = np.divide(RNew[i], CardClass[i]).tolist()

    return RNew


def EuclidDistance(v1, v2, n):
    d = 0
    for i in range(n):
        d = d + (v1[i] - v2[i]) ** 2

    return math.sqrt(d)


def CalculeDistance(R, O, n, K):
    CardClass = [0] * K
    Classe = []

    for i in range(len(O)):
        dmoy = []
        for j in range(K):
            dmoy.append(EuclidDistance(R[j], O[i], n))

        Valeur = min(dmoy)
        Indice = dmoy.index(Valeur)
        Classe.append(Indice + 1)
        CardClass[Indice] = CardClass[Indice] + 1

    return [Classe, CardClass]


def CMean(O, n, K, DiffMax, Seuil):
    # Affecter chaque objet de la collection à l'une des classes en
    # fonction du représentant le plus proche
    R = []
    for j in range(K):
        R.append(O[j])

    while DiffMax > Seuil:
        # assigns each data point to a class based on who is closest
        # to first two data points
        ClasseCard = CalculeDistance(R, O, n, K)

        # Calculer de nouveaux représentants pour les classes.
        # Ces nouveaux représentants correspondent à la moyenne
        # des objets de la classe
        RNew = CalculeNouveauRepresentants(R, O, n, K, ClasseCard[0], ClasseCard[1])

        DiffMax = Diff_R_RNew(R, RNew, n, K)
        R = RNew

    return R
