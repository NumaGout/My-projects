### =============== Importation des bibliothèques ======================== ###

from PIL import Image
im = Image.open('Image10.bmp')
px = im.load() # Matrice des pixels variable globale
from math import sqrt
w,h = im.size
L_regions = [] # On initialise la liste des régions 
               # qui est une variable globale 





### ================ Initialise les fonctions de bases =================== ###

def valeur_px(i,j): 
    ''' Permet de lire le pixel (i,j) '''
    global px
    
    return px[i,j]

def changer_px(RVB,i,j): 
    ''' Change la couleur du pixel (i,j) '''    
    global px
    
    px[i,j] = RVB
    
def changer_reg(RVB,coin_x,coin_y,largeur,hauteur): 
    ''' Change la couleur de la région '''
    global px
    
    for i in range(coin_x,coin_x+largeur):
        for j in range(coin_y,coin_y+hauteur):
            changer_px(RVB,i,j)
            

def moyenne_matrice_RVB(coin_x,coin_y,largeur,hauteur): 
    ''' Calcule la moyenne des couleurs RVB d'une région '''
    
    N = largeur*hauteur
    (r,v,b) = (0,0,0)
    for i in range(coin_x,coin_x+largeur):
        for j in range(coin_y,coin_y+hauteur):
            (r,v,b) = (r+valeur_px(i,j)[0],
                       v+valeur_px(i,j)[1],
                       b+valeur_px(i,j)[2])
    
    return r//N,v//N,b//N

def mesurer_ecart_type(coin_x,coin_y,largeur,hauteur): 
    ''' Calcule l'écart-type des couleurs RVB de la région '''
    
    N = largeur*hauteur
    (R,V,B) = moyenne_matrice_RVB(coin_x,coin_y,largeur,hauteur)
    (r,v,b) = (0,0,0)
    for i in range(coin_x,coin_x+largeur):
        for j in range(coin_y,coin_y+hauteur):
            (r,v,b) = (r+(valeur_px(i,j)[0]-R)**2,
                       v+(valeur_px(i,j)[1]-V)**2,
                       b+(valeur_px(i,j)[2]-B)**2)
    
    return r//N,v//N,b//N






### ============================= Méthode Split ========================== ###

def homogene(coin_x,coin_y,largeur,hauteur,seuil): 
    ''' Vérifie si une région est homogène '''
    
    (r,v,b) = mesurer_ecart_type(coin_x,coin_y,largeur,hauteur)
    if sqrt(r)<seuil and sqrt(v)<seuil and sqrt(b)<seuil: 
        # Regarde si les écart-type sont sous le seuil
        return True
    else:
        return False
    
def split(coin_x,coin_y,largeur,hauteur,seuil): 
    ''' Découpe une image en régions homogènes '''
    global L_regions # Liste les régions
    
    
    # Cas d'arrêt si la région est sécable (ie si c'est qu'un pixel)
    if largeur <= 1 or hauteur <= 1:
        # Ajoute la région à la liste de région
        L_regions.append([coin_x,coin_y,largeur,hauteur,px[coin_x,coin_y]])
    
    # Vérifie si la région est homogène
    elif homogene(coin_x,coin_y,largeur,hauteur,seuil): 
        # Calcule la couleur moyenne
        couleur = moyenne_matrice_RVB(coin_x,coin_y,largeur,hauteur) 
        # Change la couleur de toute la région
        changer_reg(couleur,coin_x,coin_y,largeur,hauteur)
        # Ajoute la région à la liste de région
        L_regions.append([coin_x,coin_y,largeur,hauteur,couleur]) 
        
    # Si la région n'est pas homogène on réapplique 
    # la fonction split aux 4 parties de la région
    else: 
        split(coin_x,coin_y,largeur//2,hauteur//2,seuil)
        split(coin_x+largeur//2,coin_y,largeur//2,hauteur//2,seuil)
        split(coin_x+largeur//2,coin_y+hauteur//2,largeur//2,hauteur//2,seuil)
        split(coin_x,coin_y+hauteur//2,largeur//2,hauteur//2,seuil)





### ============================ Méthode Merge =========================== ###

def contact(reg1,reg2): 
    ''' Vérifie si 2 régions sont en contact '''
    
    [num1,x1,y1,l1,h1,c1] = reg1
    [num2,x2,y2,l2,h2,c2] = reg2
    
    # Définition des 4 cas de non contact
    cas1 = x1 + l1 == x2 and not(y2+h2<y1 or y1+h1<y2) 
    cas2 = y1 + h1 == y2 and not(x2+l2<x1 or x1+l1<x2)
    cas3 = x2 + l2 == x1 and not(y1+h1<y2 or y2+h2<y1)
    cas4 = y2 + h2 == y1 and not(x1+l1<x2 or x2+l2<x1)
    
    if cas1 or cas2 or cas3 or cas4:
        return True
    else:
        return False
    
def adj_i(L_regions,i):
    ''' Donne la liste des voisins du la région i '''
    
    adj = []
    for region in L_regions:
        if contact(region,L_regions[i]):
            adj.append(region)
    return adj

def couleur_proche(reg1,reg2,seuil):
    ''' Vérifie si la couleur de 2 régions est proche
        et donne la couleur moyenne '''
    
    [num1,x1,y1,l1,h1,c1] = reg1
    [num2,x2,y2,l2,h2,c2] = reg2
    poids_tot = l1*h1+l2*h2 # Nombre total des pixels
    
    # Calcul de la moyenne pondérée
    moy = ((l1*h1*c1[0]+l2*h2*c2[0])//poids_tot,
           (l1*h1*c1[1]+l2*h2*c2[1])//poids_tot,
           (l1*h1*c1[2]+l2*h2*c2[2])//poids_tot)
    
    # Calcul de l'écart-type non pondéré
    ec_type = (sqrt(((c1[0]-moy[0])**2+(c2[0]-moy[0])**2)//2),
               sqrt(((c1[1]-moy[1])**2+(c2[1]-moy[1])**2)//2),
               sqrt(((c1[2]-moy[2])**2+(c2[2]-moy[2])**2)//2)) 
    
    if ec_type[0] < seuil and ec_type[1] < seuil and ec_type[2] < seuil:
        return True,moy # Les couleurs sont proche
    else:
        return False,moy


def fusion(seuil):
    ''' Fusionne les régions adjacentes de couleur proche '''
    global L_regions
    
    # On numérote les régions
    L_regions = [[i]+L_regions[i] for i in range(len(L_regions))] 
    # Les régions sont donc représenté comme 
    # ça [numero,coin_x,coin_y,largeur,hauteur,couleur]
    
    
    # Initialise la liste des régions non traitées
    region_non_traitee = [i for i in range(len(L_regions))] 
    
    # Cas d'arrêt si toutes les régions sont traitées
    while len(region_non_traitee) > 0: 
        reg1 = region_non_traitee[0] 
        region_non_traitee.remove(reg1)
        
        # Initialise la file d'attente
        file_attente = [k[0] for k in adj_i(L_regions,reg1)]
        
        while len(file_attente) >= 1 : # Cas d'arrêt
            # Retire le dernier élément de la file et est mis dans reg2
            reg2 = file_attente.pop() 
            
            # Vérifie si on a déjà traitée la région
            if reg2 in region_non_traitee:
                [b,moy] = couleur_proche(L_regions[reg1],L_regions[reg2],seuil)
                
                if b: # Si les couleurs sont proches
                    ''' On change les couleurs des régions '''
                    changer_reg(moy,L_regions[reg1][1],
                                L_regions[reg1][2],
                                L_regions[reg1][3],
                                L_regions[reg1][4])
                    L_regions[reg1][5]=moy
                    
                    
                    changer_reg(moy,L_regions[reg2][1],
                                L_regions[reg2][2],
                                L_regions[reg2][3],
                                L_regions[reg2][4])
                    L_regions[reg2][5]=moy
                    
                    # Boucle rajoutant les voisins de reg2 à la file d'attente
                    for k in adj_i(L_regions,reg2):
                        if ((k[0] in region_non_traitee) 
                             and (k[0] not in file_attente)):
                            
                            file_attente.append(k[0])
                    region_non_traitee.remove(reg2)
                
        
