S1 = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000,20000,50000] # Jeu de pièces disponible
S2 = [1,7,23] # Jeu de pièce disponible

### ================= II.1 : Technique Gloutonne ======================= ###

def Monnaie_Gloutonne(S,M):
    ''' Rend le vecteur T qui est solution de l'approche Gloutonne, sans tenir
    compte du nombre de pieces disponibles '''
    m = M
    n = len(S)
    T = [0 for k in range(n)] # Vecteur Solution
    for i in range(1,n+1): # On parcourt la liste à l'envers
        if S[-i] <= m:
            q = m//S[-i]
            r = m - q*S[-i]
            T[-i] += q
            m = r
    return T

def Monnaie_Gloutonne_D(S,D,M):
    ''' Rend la solution à l'approche Gloutonne T, en tenant compte des pieces
    disponibles '''
    n = len(S)
    m = M
    T = [0 for k in range(n)] # Vecteur Solution
    
     # Liste de booléens qui indique s'il reste des pièces
    R = [D[k] != 0 for k in range(n)]
    for i in range(1,n+1): # On parcourt la liste à l'envers
         # Si R[-i] = True alors il reste des pieces S[i] sinon non
        if S[-i] <= m and R[-i]:
            q = m//S[-i]
            T[-i] += min(q,D[-i])
            m = m - S[-i]*min(q,D[-i])
            R[-i] = False
    if m == 0:
        return T
    else:
        return None
    
### ============== II.2 : Chemin minimal dans un arbre =============== ###
        
def Graphe_Monnaie(S,M):
    ''' Renvoie Arbre qui représente le graphe des solutions au probleme '''
    Arbre = {} 
    a = {} # Sous-dico
    file_attente = [] # Liste des noeuds à traiter 
    
     # Initialise l'Arbre
    for i in S:
        if M-i >= 0:
            a[M-i] = None
            file_attente.append(M-i) # On place les fils de M dans la file
    Arbre[M] = a
    
    for i in file_attente:
        if i == 0:
            return Arbre # Cas d'arret
        a = {} # Sous-dico
        for k in S: 
            if i-k >= 0 :
                a[i-k] = None
                if (i-k) not in Arbre:
                    file_attente.append(i-k) # On place les fils non-traites
        Arbre[i] = a
        
                    
def Solution_Monnaie_Arbre(S,M):
    '''  Renvoie la solution optimale T de Q(S,M) grace au graphe crée
    dans la fonction Graphe_Monnaie '''
    Arbre = Graphe_Monnaie(S,M)
    T = [0 for i in range(len(S))] # Init de la solution
    m = 0 # Initialise la valeur de depart
    l = list(Arbre.keys()) # Liste des clefs de Arbre
    
    while m != M: # Condition d'arret si m = M
        i = 0 # Compteur qui parcours l
        while m not in Arbre[l[i]]: # On cherche le noeud ayant m en fils
            i += 1
        T[S.index(l[i]-m)] += 1 # On ajoute la valeur de la piece
        m = l[i] # On actualise m 
        
    return T
            
### =============== III : Programmation Dynamique ====================== ###
    
def Matrice_Prog_Dyn(S,M):
    ''' Renvoie mat qui est la matrice du nombre de piece minimum utilisées
    pour atteindre M '''
    mat = [[0 for i in range(M+1)] for j in range(len(S)+1)]
    
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i == 0:
                mat[i][m] = float("inf")
            else:
                if m-S[i-1] < 0:
                    mat[i][m] = mat[i-1][m]
                else:
                    mat[i][m] = min(1+mat[i][m-S[i-1]],mat[i-1][m])
    return mat

def Solution_Prog_Dyn(S,M):
    ''' Renvoie T solution du nombre de pièce minimum utilisées pour atteindre
    M par la méthode de programmation dynamique, c'est une amélioration du 
    programme précédent '''
    
    # Matrice composée en i,j de (nombre minimal de piece,
    #                             valeur de la dernière piece ajoutée)
    mat = [[(0,0) for i in range(M+1)] for j in range(len(S)+1)]
    
    T = [0 for i in range(len(S))] # Vecteur solution
    
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0,0
            elif i == 0:
                mat[i][m] = float("inf"),None
            else:
                if m-S[i-1] < 0:
                    mat[i][m] = mat[i-1][m] 
                else:
                    if 1+mat[i][m-S[i-1]][0] <= mat[i-1][m][0]:
                        mat[i][m] = (1+mat[i][m-S[i-1]][0],S[i-1])
                    else:
                        mat[i][m] = mat[i-1][m]
    m = M           
    while m != 0: # On retrace la solution, donc on parcourt la dernière ligne
        T[S.index(mat[-1][m][1])] += 1
        m += -mat[-1][m][1] # On enlève la denière piece ajoutée
    return T
        
    
print('### ================ Première expérience ===================== ###\n')
print('S = '+ str(S1))
print('M = 900\n\nGlouton:')

print(Monnaie_Gloutonne(S1,900))
print('\nArbre: ')
print(Solution_Monnaie_Arbre(S1,900))
print('\nProgDyn: ')
print(Solution_Prog_Dyn(S1,900))


print('\n### =============== Deuxième expérience ===================== ###\n')
print('S = '+ str(S1))
print('M = 198900\n\nGlouton: ')

print(Monnaie_Gloutonne(S1,198900))
print('\nProgDyn: ')
print(Solution_Prog_Dyn(S1,198900))


print('\n### ================= Troisième expérience ==================== ###\n')
print('S = '+ str(S2))
print('M = 28\n\nGlouton:')

print(Monnaie_Gloutonne(S2,28))
print('\nArbre: ')
print(Solution_Monnaie_Arbre(S2,28))
print('\nProgDyn: ')
print(Solution_Prog_Dyn(S2,28))          
    
    
            
            
                
                