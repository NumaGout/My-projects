import numpy as np
import time

voisin=[[1,2], [1,-2], [-1,2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]]
#liste des coordonnées de déplacement d'un cavalier

####### ----------------------- Version normale ---------------------- ########


def initialisation_1(N,x,y):
    """ Prend la taille de l'échiquier et les coordonnées de départ
    et créer un échiquier avec des -1 partout et un 1 su le départ"""
    global echiquier
    echiquier = np.full((N,N),-1)
    echiquier[x,y]=1

def prometteur_1(G,N,case):
    """ Vérifie si une case respecte les conditions: dans l'échiquier et pas
    explorée"""
    return (case[0]>=0 and case[0]<N and
            case[1]>=0 and case[1]<N and
            G[case[0],case[1]] == -1)

def main_1(N,d):
    """ Programme de base, renvoie la solution si elle existe"""
    global voisin
    global count
    count = 0
    initialisation_1(N,d[0],d[1])

    def aux(G,case,num):
        """ fonction auxilliaire récursive"""
        if num>N**2: #condition d'arrêt si toutes les cases ont été visitées
            return True
        else:
            (x,y)=case
            for i in range(8): #pour tous les voisins éligibles on regarde si
                               #ils donnent une solution
                next_x = x+voisin[i][0]
                next_y = y+voisin[i][1]
                if prometteur_1(G,N,(next_x,next_y)):
                    G[next_x,next_y]=num
                    global count
                    count+=1
                    if aux(G,(next_x,next_y),num+1):
                        return True
                    G[next_x,next_y]=-1
            return False

    if aux(echiquier,d,2):
        return echiquier
    return 'Non nul'



####### -------------------- Version normale + bande ------------------- ######


def initialisation_2(N,x,y):
    """ pareil que le premier sauf la -2 en plus """
    global echiquier
    echiquier = np.full((N+4,N+4),-1)
    echiquier[x,y]=1

    for i in range(2):
        for j in range(N+4):
            echiquier[i,j]=-2
            echiquier[j,i]=-2
            echiquier[-i-1,j]=-2
            echiquier[j,-i-1]=-2

def prometteur_2(G,N,case):
    """ pareil que le premier mais un seul test """
    return G[case[0],case[1]] == -1

def main_2(N,d):
    """ pareil que le premier """
    global voisin
    global count
    #compte le nombre d'appel de la fonction aux
    count = 0
    initialisation_2(N,d[0]+2,d[1]+2)

    def aux(G,case,num):
        if num>N**2:
            return True
        else:
            (x,y)=case
            for i in range(8):
                next_x = x+voisin[i][0]
                next_y = y+voisin[i][1]
                if prometteur_2(G,N,(next_x,next_y)):
                    G[next_x,next_y]=num
                    global count
                    count+=1
                    if aux(G,(next_x,next_y),num+1):
                        return True
                    G[next_x,next_y]=-1
            return False

    if aux(echiquier,(d[0]+2,d[1]+2),2):
        return echiquier[2:N+2,2:N+2]
    return 'Non nul'



####### ---------------- Version heuristique + bande ------------------ #######


def initialisation_3(N,x,y):
    """ pareil que le premier mais avec la matrice des voisins dispo en plus"""
    global echiquier
    echiquier = np.full((N+4,N+4),-1)
    echiquier[x,y]=1

    for i in range(2):
        for j in range(N+4):
            echiquier[i,j]=-2
            echiquier[j,i]=-2
            echiquier[-i-1,j]=-2
            echiquier[j,-i-1]=-2

    global mat_voisin
    mat_voisin = np.full((N+4,N+4),0)

    for i in range(2,N+2): #boucles qui vérifient le nombre de voisin dispo
        for j in range(2,N+2):
            liste_voisin = [(i+voisin[k][0],j+voisin[k][1]) for k in range(8)]
            nb_voisin_disp = 0
            for k in liste_voisin:
                if prometteur_3(echiquier,N,k):
                    nb_voisin_disp += 1
            mat_voisin[i,j]=nb_voisin_disp
            
def prometteur_3(G,N,case):
    """ comme le deuxième """
    return G[case[0],case[1]] == -1

def meilleur_voisin(G,mat_vois,N,case):
    """ renvoie la liste de voisin triée du meilleur au plus nul, renvoie False
    si aucun voisin dispo """
    l_voisin = []
    for i in range(8):
        a = (case[0]+voisin[i][0],case[1]+voisin[i][1])
        if prometteur_3(G,N,a):
            l_voisin.append((mat_voisin[a],a))
    if len(l_voisin) != 0:
        l_voisin.sort()
        return True,l_voisin
    return False,[(0,0)]

def main_3(N,d):
    """ renvoie la solution """
    global voisin
    global count
    count = 0
    initialisation_3(N,d[0]+2,d[1]+2)



    def aux(G,case,num):
        """ comme le premier sauf que la liste des voisins change, on utilise
        la liste des voisins triée du meilleur au plus nul """
        if num>N**2:
            return True
        else:
            (b,meil_vois) = meilleur_voisin(G,mat_voisin,N,case)
            if b:
                for k in meil_vois:
                    G[k[1]] = num
                    for i in range(8):
                        mat_voisin[(case[0]+voisin[i][0],
                                    case[1]+voisin[i][1])]-=1
                global count
                count+=1
                if aux(G,k[1],num+1):
                    return True
                G[k[1]]=-1
                for i in range(8):
                    mat_voisin[(case[0]+voisin[i][0],
                                case[1]+voisin[i][1])]+=1
            return False



    if aux(echiquier,(d[0]+2,d[1]+2),2):
        return echiquier[2:N+2,2:N+2]
    return 'Non nul'

####### ------------------------ TEST DE TEMPS ---------------------- #######

""" Classique sans bande """

t0 = time.perf_counter()
main_1(5,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('===================================='+'\n'+'CLASSIQUE SANS BANDE'+'\n')
print('Réussite 5x5: '+str(T)+'\n')
print(echiquier)
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_1(5,(2,3))
t1 = time.perf_counter()
T = t1-t0
print('Echec 5x5: '+str(T))
print('Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_1(6,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 6x6: '+str(T)+'\n')
print(echiquier)
print('\n'+'Nb appels : '+str(count)+'\n')

""" Classique avec bande """

t0 = time.perf_counter()
main_2(5,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('===================================='+'\n'+'CLASSIQUE AVEC BANDE'+'\n')
print('Réussite 5x5: '+str(T)+'\n')
print(echiquier[2:5+2,2:5+2])
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_2(5,(2,3))
t1 = time.perf_counter()
T = t1-t0
print('Echec 5x5: '+str(T))
print('Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_2(6,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 6x6: '+str(T)+'\n')
print(echiquier[2:6+2,2:6+2])
print('\n'+'Nb appels : '+str(count)+'\n')

""" Heuristique + bande """

t0 = time.perf_counter()
main_3(5,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('===================================='+'\n'+'HEURISTIQUE'+'\n')
print('Réussite 5x5: '+str(T)+'\n')
print(echiquier[2:5+2,2:5+2])
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(5,(2,3))
t1 = time.perf_counter()
T = t1-t0
print('Echec 5x5: '+str(T))
print('Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(6,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 6x6: '+str(T)+'\n')
print(echiquier[2:6+2,2:6+2])
print('Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(7,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 7x7: '+str(T)+'\n')
print(echiquier[2:7+2,2:7+2])
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(8,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 8x8: '+str(T)+'\n')
print(echiquier[2:8+2,2:8+2])
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(9,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 9x9: '+str(T)+'\n')
print(echiquier[2:9+2,2:9+2])
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(10,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 10x10: '+str(T)+'\n')
print(echiquier[2:10+2,2:10+2])
print('\n'+'Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(20,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 20x20: '+str(T))
print('Nb appels : '+str(count)+'\n')

t0 = time.perf_counter()
main_3(30,(0,0))
t1 = time.perf_counter()
T = t1-t0
print('Réussite 30x30: '+str(T))
print('Nb appels : '+str(count)+'\n')