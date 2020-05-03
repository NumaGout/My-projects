import numpy as np
import random as rnd
from tkinter import *

###############################################################################
### ----------------------------------------------------------------------- ###
### ----------------------------- CODE SOURCE ----------------------------- ###
### ----------------------------------------------------------------------- ###
###############################################################################


global dimension 
dimension = 3
global profondeur_origine
profondeur_origine = 6

def init_G():
    global VB
    global VN
    global VV
    global G
    """ Initialise le plateau de taille dimension """
    VV = []
    VB = []
    VN = []
    for i in range(dimension):
        for j in range(dimension):
            VV.append((i+1,j+1))
    G = (VB,VN,VV)
    
def illustration(G):
    """ Affiche le plateau pour le code source """
    m = np.full([dimension,dimension],' ')
    (VB,VN,VV) = G    
    for (i,j) in VB:
        m[i-1,j-1] = 'B'
    for (i,j) in VN:
        m[i-1,j-1] = 'N'
    
    return m

init_G()

### ------------------------ JEU AVEC ALEATOIRE --------------------------  ###

def chgt_couleur(couleur):
    """ Change de couleur """
    if couleur == 'Noir':
        return 'Blanc'
    return 'Noir'

def gagnant(G,color):
    """ Verifie si la couleur color a gagné """
    (VB,VN,VV) = G
    
    if color == 'Noir':
        if len(VN) != dimension: # Si il y a assez de pion
            return False
        b = True
        for i in range(dimension-1): # Si ils sont sur une colonne
            b = b and (VN[i][1] == VN[i+1][1])
        if b:
            return b
        b = True
        for i in range(dimension-1): # Si ils sont sur une ligne
            b = b and (VN[i][0] == VN[i+1][0])
        if b:
            return b
        b = True
        for i in range(dimension): # Premiere diagonale
            (m,n) = VN[i]
            b = b and (m == n)
        if b:
            return b
        b = True
        for i in range(dimension): # Deuxième diagonale
            (m,n) = VN[i]
            b = b and (m+n == dimension+1)
        if b:
            return b
    else:
        if len(VB) != dimension:
            return False
        b = True
        for i in range(dimension-1):
            b = b and (VB[i][1] == VB[i+1][1])
        if b:
            return b
        b = True
        for i in range(dimension-1):
            b = b and (VB[i][0] == VB[i+1][0])
        if b:
            return b
        b = True
        for i in range(dimension):
            (m,n) = VB[i]
            b = b and (m == n)
        if b:
            return b
        b = True
        for i in range(dimension):
            (m,n) = VB[i]
            b = b and (m+n == dimension+1)
        if b:
            return b 
     
        
def retirer_un_pion(G,color,ij):
    """ Retire le pion de couleur color de coordonnee ij """
    (VB,VN,VV) = G
    VV.append(ij)
    eval('V'+color[0]+'.remove(ij)')
    
    
def placer_un_pion(G,color,ij):
    """ Place le pion de couleur color de coordonnee ij """
    (VB,VN,VV) = G
    VV.remove(ij)
    eval('V'+color[0]+'.append(ij)')
       
        

def placer_un_pion_P(G,color):
    """ Version console du placement de pion par l'humain """
    (VB,VN,VV) = G
    if color == 'Noir':
        if len(VN) != dimension:
            print(illustration(G))
            choix = eval(input('Où veux-tu jouer ? '))
            placer_un_pion(G,color,choix)
        else:
            print(illustration(G))
            choix1 = eval(input('Quelle case veux-tu enlever ? '))
            choix2 = eval(input('Où veux-tu jouer ? '))
            retirer_un_pion(G,color,choix1)
            placer_un_pion(G,color,choix2)
            
    else:
        if len(VB) != dimension:
            print(illustration(G))
            choix = eval(input('Où veux-tu jouer ? '))
            placer_un_pion(G,color,choix)
        else:
            print(illustration(G))
            choix1 = eval(input('Quelle case veux-tu enlever ? '))
            choix2 = eval(input('Où veux-tu jouer ? '))
            retirer_un_pion(G,color,choix1)
            placer_un_pion(G,color,choix2)      
        
def placer_un_pion_RND(G,color):
    """ Placer un pion de manière aleatoire renvoie le pion placé et celui
        enlevé """
    (VB,VN,VV) = G
    choix = (rnd.randint(1,dimension),rnd.randint(1,dimension)) # Pion placé
    while choix not in VV:
        choix = (rnd.randint(1,dimension),rnd.randint(1,dimension))
    VV.remove(choix)
    x = None
    
    if color == 'Noir':
        if len(VN) != dimension:
            VN.append(choix)
        else:
            a = rnd.randint(0,dimension-1) # Choix du pion a enlever
            x=VN[a]
            VV.append(VN[a])
            del VN[a]
            VN.append(choix)
    else:
        if len(VB) != dimension:
            VB.append(choix)
        else:
            a = rnd.randint(0,dimension-1)
            x = VB[a]
            VV.append(VB[a])
            del VB[a]
            VB.append(choix)
    return(choix,x)
    
    
def jouer(players):
    """ Boucle du jeu """
    init_G()
    [J1,J2]=players # J1,J2 désignent humain ou ordi
    color = 'Blanc'
    
    fin = False
    while not fin:
        eval('placer_un_pion_'+J1+'(G,color)')
        fin = gagnant(G,color)
        if not fin:
            color = chgt_couleur(color)
        else:
            break
        eval('placer_un_pion_'+J2+'(G,color)')
        fin = gagnant(G,color)
        if not fin:
            color = chgt_couleur(color)
    print(color+' est gagnant')
    print(illustration(G)) 
    return G,color

    
### ----------------------------- IA Best-First --------------------------- ### 
    
def evaluation_BEST(G,color,ij):
    """ calcule la valeur de la case ij """
    VB,VN,VV = G
    i,j = ij
    NbL1 = 0
    NbL2 = 0
    NbC1 = 0
    NbC2 = 0
    NbD1 = 0
    NbD2 = 0
    
    for k in range(1,dimension+1): # Ligne et colonne de (i,j)
        if (i,k) in G[0]: 
            NbL1 += 1
        if (k,j) in G[0]:
            NbC1 += 1
        if (i,k) in G[1]:
            NbL2 += 1
        if (k,j) in G[1]:
            NbC2 += 1
            
    if i == j: # Premiere diagonale
        for k in range(1,dimension+1):
            if (k,k) in G[0]:
                NbD1 += 1
            elif (k,k) in G[1]:
                NbD2 += 1
    if i+j == dimension+1: # Deuxième diagonale
        for k in range(1,dimension+1):
            if (k,dimension-k+1) in G[0]:
                NbD1 += 1
            elif (k,dimension-k+1) in G[1]:
                NbD2 += 1
    g = (NbL1-NbL2)**2 + (NbC1-NbC2)**2 + (NbD1-NbD2)**2
    
    if color == 'Blanc': # calcul des facteurs
        if NbL2 > 1:
            facteur_L = 2
        else:
            facteur_L = 1
        if NbC2 > 1:
            facteur_C = 2
        else:
            facteur_C = 1
        if NbD2 > 1:
            facteur_D = 2
        else:
            facteur_D = 1
    else:
        if NbL1 > 1:
            facteur_L = 2
        else:
            facteur_L = 1
        if NbC1 > 1:
            facteur_C = 2
        else:
            facteur_C = 1
        if NbD1 > 1:
            facteur_D = 2
        else:
            facteur_D = 1
        
    return g*facteur_L*facteur_C*facteur_D

def Nb_de_droite(G,ij):
    """ calcule combien de possibilitées un pion possède """
    i,j = ij
    Nb = 2
    if i == j:
        Nb += 1
    if i+j == dimension+1:
        Nb += 1
    return Nb
        
def meilleur_choix(G,l):  
    """ Renvoie le meilleur choix du pion a placer, privilégie les diago """
    VB,VN,VV=G      
    p = [(0,0)]
    for i in range(len(l)):
        if l[i][0] > p[0][0]:
            p = []
            p.append(l[i])
        elif l[i][0] == p[0][0]:
            p.append(l[i])
    
    meilleur = ((0,0),0)
    for k in p:
        c = Nb_de_droite(G,VV[k[1]])
        if c > meilleur[1]:
            meilleur = k,c
    
    return meilleur[0]
        
def matrice_point_BEST(G,color):
    """ Renvoie les listes de valeur des coups possibles """
    VB,VN,VV=G
    if color == 'Blanc':
        x=0
    else:
        x=1
    
    liste_point_placer = []
    liste_point_retirer = []
        
    for k in range(len(VV)):
        point = evaluation_BEST(G,color,VV[k])
        liste_point_placer.append((point,k))
    for k in range(len(G[x])):
        point = evaluation_BEST(G,color,G[x][k])
        liste_point_retirer.append((point,k))
        
    return(liste_point_placer,liste_point_retirer)
    
def placer_un_pion_BEST(G,color):
    """ PLace un pion de manière Best-first """
    VB,VN,VV=G
    if color == 'Blanc':
        x=0
    else:
        x=1
        
    evaluation = matrice_point_BEST(G,color)
    if len(evaluation[1]) > 0:
        meilleur_enlever = min(evaluation[1])
    meilleur_placement = meilleur_choix(G,evaluation[0])
    a = None
    
    if len(G[x]) != dimension:
        c = VV[meilleur_placement[1]]
        placer_un_pion(G,color,c)
    else:
        c = VV[meilleur_placement[1]]
        a = G[x][meilleur_enlever[1]]
        retirer_un_pion(G,color,a)
        placer_un_pion(G,color,c)
    
    return(c,a) 
    
### ----------------------------- Min-Max --------------------------------- ###
    
def Valeur(etat,color):
    """ Calcul de la valeur min-max """
    VB,VN,VV=G
    l_Blanc = [0 for i in range(2*dimension+2)]
    l_Noir = [0 for i in range(2*dimension+2)]
    
    for k in VB:
        i,j = k
        l_Blanc[i] = 1
        l_Blanc[j] = 1+dimension
        if i == j:
            l_Blanc[-2]
        if i+j == dimensions+1:
            l.Blanc[-1]
    for k in VN:
        i,j = k
        l_Noir[i] = 1
        l_Noir[j] = 1+dimension
        if i == j:
            l_Noir[-2]
        if i+j == dimensions+1:
            l.Noir[-1]
            
    if color == 'Blanc':
        return sum(l_Blanc)-sum(l_Noir)
    else:
        return sum(l_Noir)-sum(l_Blanc)
    
def autre_mode(mode):
    if mode == 'max':
        return 'min'
    else:
        return 'max'
    
def placer_un_pion_MINMAX(G,color):
    VB,VN,VV=G
    if color == 'Blanc':
        x=0
    else:
        x=1
        
    mode = 'max'
    a = None
    profondeur = profondeur_origine        
    futur_plateau,valeur = minmax(G,profondeur,'max',color)
    if len(G[x]) == dimension:
        VB,VN,VV = ([futur_plateau[0][i]for i in range(len(futur_plateau[0]))],
                    [futur_plateau[1][i]for i in range(len(futur_plateau[1]))],
                    [futur_plateau[2][i]for i in range(len(futur_plateau[2]))])
                     
        G= VB,VN,VV
        a = VV[-1]
        choix = G[x][-1]
    else:
        VB,VN,VV = ([futur_plateau[0][i]for i in range(len(futur_plateau[0]))],
                    [futur_plateau[1][i]for i in range(len(futur_plateau[1]))],
                    [futur_plateau[2][i]for i in range(len(futur_plateau[2]))])
        G=VB,VN,VV
        choix = G[x][-1]
    return(choix,a)
    
    
def minmax(G,profondeur,mode,color):
    """ Algorithme min max """
    VB,VN,VV=G
    if color == 'Blanc':
        x = 0
    else:
        x = 1
        
    if len(VV)!=0:
        if profondeur == 0 or gagnant(G,chgt_couleur(color)):
            valeur = Valeur(G,chgt_couleur(color))
            return G,valeur
    
    minscore = float('infinity')
    maxscore = -float('infinity')
    meilleure_case_a_jouer = None
    liste_plateau_successeur = []
    if len(G[x]) < dimension:
         for k in VV:
             VBbis = [i for i in VB] # Copie du plateau
             VNbis = [i for i in VN]
             VVbis = [i for i in VV]
             placer_un_pion((VBbis,VNbis,VVbis),color,k)
             liste_plateau_successeur.append((VBbis,VNbis,VVbis))
    else:
         for k in G[x]:
             VBbis = [i for i in VB]
             VNbis = [i for i in VN]
             VVbis = [i for i in VV]
             for l in VV:
                 print((VBbis,VNbis,VVbis))
                 retirer_un_pion((VBbis,VNbis,VVbis),color,k)
                 placer_un_pion((VBbis,VNbis,VVbis),color,l)
                 liste_plateau_successeur.append((VBbis,VNbis,VVbis))
    
    for Gbis in liste_plateau_successeur:
        plateau1,score = minmax(Gbis,
                                profondeur-1,
                                autre_mode(mode),
                                chgt_couleur(color))
        
        if mode == 'max':
            if score > maxscore:
                best_score = score
                best_plateau=([plateau1[0][i] for i in range(len(plateau1[0]))],
                             [plateau1[1][i] for i in range(len(plateau1[1]))],
                             [plateau1[2][i] for i in range(len(plateau1[2]))])
                maxscore = best_score
        else:
            if score<minscore:
                best_score=score
                best_plateau=([plateau1[0][i] for i in range(len(plateau1[0]))],
                             [plateau1[1][i] for i in range(len(plateau1[1]))],
                             [plateau1[2][i] for i in range(len(plateau1[2]))])
                minscore=best_score
    
    if profondeur == profondeur_origine:
        return best_plateau,best_score
    else:
        return G,best_score

###############################################################################    
### ----------------------------------------------------------------------- ###    
### --------------------- Implémentation graphique ------------------------ ###
### ----------------------------------------------------------------------- ###
###############################################################################    

class Case(Button):
    """ Classe des cases du plateau """
    
    def __init__(self,parent,fenetre,coordonnee,largeur,texte,color):
        Button.__init__(self,master=parent,
                             width=largeur,
                             height=largeur//2,
                             text = texte,
                             command = self.cliquer)
        
        self.__coordonnee = coordonnee
        self.__color  =color
        self.__fenetre = fenetre
        
    def get_color(self):
        return self.__color
    
    def set_color(self,color):
        self.__color = color
        
    def get_coordonnee(self):
        return self.__coordonnee
    
    def set_texte(self,texte):
        self['text'] = texte
        
    def cliquer(self):
        result = self.__fenetre.traitement(self.get_color(),
                                           self.get_coordonnee())
        if result:
            if self.get_color() != 'Vide':
                self.set_color('Vide')
                self.set_texte(' ')
            else:
                if self.__fenetre.get_joueur() == 'Blanc':
                    #On alterne car traitement fait un changement de joueur
                    self.set_texte('O')
                    self.set_color('Noir')
                else:
                    self.set_texte('X')
                    self.set_color('Blanc')
        
class FenPrincipale(Tk):
    
    def __init__(self):
        Tk.__init__(self)
        self.title('Morpion')
        
        self.__players = ['RND','RND']

        self.__joueur = 'Blanc'
        self.__dimension = 3
        self.__VV = [(i+1,j+1) for i in range(self.__dimension) 
                               for j in range(self.__dimension)]
        self.__VB = []
        self.__VN = []
        
        self.__fin = False
        
        
        self.__frameControle = Frame(self)
        self.__frameControle.pack(side=TOP,padx=5,pady=5)
        
        self.__boutonQuit = Button(self.__frameControle,
                                   text = 'Quitter',
                                   width=7,
                                   command=self.destroy)
        self.__boutonQuit.pack(side=LEFT,padx=5,pady=5)
        
        self.__boutonNew = Button(self.__frameControle,
                                  text = 'Nouvelle partie',
                                  width = 15,
                                  command=self.NouvellePartie)
        self.__boutonNew.pack(side = LEFT, padx=5,pady=5)
        
        self.__boutonDim = Button(self.__frameControle,
                                  text = 'Dimension',
                                  width=9,
                                  command=self.Dimension)
        self.__boutonDim.pack(side=LEFT,padx=5,pady=5)
        
        self.__boutonJoueur1 = Button(self.__frameControle,
                                      text = 'Joueur 1',
                                      width = 8,
                                      command=lambda j=1:self.choix_joueur(j))
        self.__boutonJoueur1.pack(side=LEFT,padx=5,pady=5)
        
        self.__boutonJoueur2 = Button(self.__frameControle,
                                      text = 'Joueur 2',
                                      width = 8,
                                      command=lambda j=2:self.choix_joueur(j))
        self.__boutonJoueur2.pack(side=LEFT,padx=5,pady=5)
        
        self.__frameMorpion = Frame(self)
        self.__frameMorpion.pack(side = TOP, padx=5,pady=5)
        
        self.__frameBottom = Frame(self)
        self.__frameBottom.pack(side=TOP,padx=5,pady=5)
        
        self.__boutonCoup = Button(self.__frameBottom,
                                   text = 'Coup',
                                   width = 8,
                                   command=self.coup)
        self.__boutonCoup.pack(side=LEFT,padx=5,pady=5)
        
        self.__frameNotif = Frame(self)
        self.__frameNotif.pack(side = TOP,padx=5,pady=5)
        self.__motNotif = StringVar()
        self.__Notif = Label(self.__frameNotif,
                             textvariable=self.__motNotif,
                             fg='red')
        self.__Notif.pack(side=LEFT,padx=5, pady=5)       
        
        self.__cases = []
        
        self.NouvellePartie()
        
    def get_plateau(self):
        return self.__VB,self.__VN,self.__VV
    
    def get_fin(self):
        return self.__fin
    
    def get_dimension(self):
        return self.__dimension
                
    def get_joueur(self):
            return self.__joueur
    
    def get_players(self):
        return self.__players
        
    def set_notif(self,texte):
        self.__motNotif.set(texte)
        
    def choix_joueur(self,j):
        """ fenetre popup de choix de joueur """
        global profondeur_origine
        fenetreJ = Toplevel()
        fenetreJ.transient(self)
        fenetreJ.title('Joueur '+str(j))
        frameBout = Frame(fenetreJ)
        frameBout.pack(side=TOP,padx=5,pady=5)
        frameErr = Frame(fenetreJ)
        frameErr.pack(side=TOP,padx=5,pady=5)
        erreur = StringVar()
        label_err = Label(frameErr,textvariable = erreur,fg = 'red')
        label_err.pack(side=TOP,padx=5,pady=5)
        
        def click(i):
            """ fonction aux si on clique sur le choix joueur """
            global profondeur_origine
            
            def changer_prof(p):
                """ fonction aux si on clique sur la profondeur """
                global profondeur_origine
                profondeur_origine = p
                fenProf.destroy()
            
            if 'MINMAX' in self.__players and i == 'MINMAX':
                erreur.set('/!\ Il y a déja un Min Max')
            else:
                self.__players[j-1]=i
                fenetreJ.destroy()
                if i == 'MINMAX':
                    fenProf = Toplevel()
                    fenProf.transient(self)
                    fenProf.title('Profondeur')
                    for k in range(7):
                        b = Button(fenProf,
                                   text=str(k),
                                   command=lambda p=k: changer_prof(p))
                        b.pack(side=LEFT,padx=5,pady=5)
        Button(frameBout,
               text='Humain',
               width=10,
               command=lambda i='P':click(i)).pack(side=LEFT,padx=5)
        Button(frameBout,
               text='Aleatoire',
               width=10,
               command=lambda i='RND':click(i)).pack(side=LEFT,padx=5)
        Button(frameBout,
               text='Best-First',
               width=10,
               command=lambda i='BEST':click(i)).pack(side=LEFT,padx=5)    
        Button(frameBout,
               text='MinMax',
               width=10,
               command=lambda i='MINMAX':click(i)).pack(side=LEFT,padx=5)
        self.NouvellePartie()
        
    def NouvellePartie(self):
        self.__VV = [(i+1,j+1) for i in range(self.__dimension) 
                               for j in range(self.__dimension)]
        self.__VB = []
        self.__VN = []
        self.__joueur = 'Blanc'
        self.__fin = False
        self.__motNotif.set('')
        
        for b in self.__cases:
            b.destroy()
        self.__cases = []
        for i in range(self.__dimension):
            for j in range(self.__dimension):
                self.__cases.append(Case(self.__frameMorpion,
                                         self,(i+1,j+1),
                                         5,
                                         ' ',
                                         'Vide'))
                self.__cases[i*self.__dimension+j].grid(row=i,column=j) 
            
    def Dimension(self):
        """ fenetre popup choix de dimension """
        global dimension
        fenetreDim = Toplevel()
        fenetreDim.transient(self)
        fenetreDim.title('Quelle dimension ? ')
        dim = IntVar()
        dim.set(self.__dimension)
        def ajout(i):
            """ aux qui incrémente la dimension """
            dim.set(dim.get()+i)
        
        for k in [-10,-1]:
            Button(fenetreDim,
                   text=str(k),
                   command=lambda i=k : ajout(i)).pack(side=LEFT)
        Label(fenetreDim,textvariable = dim).pack(side=LEFT,padx=20)
        for k in [1,10]:
            Button(fenetreDim,
                   text='+'+str(k),
                   command=lambda i=k : ajout(i)).pack(side=LEFT)
            
        def repondre():
            """ aux qui confirme la dimension """
            global dimension
            self.__dimension = dim.get()
            dimension = self.get_dimension()
            self.NouvellePartie()
            fenetreDim.destroy()
            
        Button(fenetreDim,text='OK',command=repondre).pack(side=LEFT,padx=20)
        
    def traitement(self,color,ij):
        """ analyse le clic sur une case """
        G = self.__VB,self.__VN,self.__VV   
        
        if self.__joueur == 'Blanc':
            x = 0
        else:
            x=1
        result = True    
        
        if not self.__fin and self.__players[x] == 'P':
            if color == 'Vide':
                if len(self.get_plateau()[x])<self.__dimension:
                    placer_un_pion(G,self.__joueur,ij)
                    self.__fin = gagnant(G,self.get_joueur())
                    self.__joueur=chgt_couleur(self.__joueur)
                    self.__motNotif.set('')
                else:
                    self.__motNotif.set("/!\ Tu n'as pas le droit")
                    result = False
            else:
                if (len(self.get_plateau()[x])>=self.__dimension and 
                    color == self.__joueur):
                    
                    retirer_un_pion(G,color,ij)
                    self.__motNotif.set('')
                else:
                    self.__motNotif.set("/!\ Tu n'as pas le droit")
                    result = False
                
            if self.__fin:
                self.__joueur=chgt_couleur(self.__joueur)
                self.__motNotif.set(self.__joueur+' a gagné !')
                self.__joueur=chgt_couleur(self.__joueur)
        elif self.__fin:
            self.__motNotif.set("La partie est déjà finie")
            result = False
        else:
            self.__motNotif.set("C'est à l'ordi de jouer")
            result = False
        return result

            
    def coup(self):
        """ Fait jouer l'ordi """
        G = self.__VB,self.__VN,self.__VV
        [J1,J2]=self.__players
        if self.__fin:
            self.__motNotif.set("La partie est déjà finie")
        else:
            if self.__joueur == 'Blanc':
                if J1 != 'P':
                    (c,a)=eval('placer_un_pion_'+J1+'(G,self.get_joueur())')
                    self.__fin = gagnant(G,self.get_joueur())
                    case = self.__cases[(c[0]-1)*self.__dimension+c[1]-1]
                    case.set_texte('X')
                    case.set_color('Blanc')
                    if a !=None:
                        case = self.__cases[(a[0]-1)*self.__dimension+a[1]-1]
                        case.set_texte(' ')
                        case.set_color('Vide')  
                    if not self.__fin:
                        self.__joueur = chgt_couleur(self.__joueur)
                    self.__motNotif.set('')    
                else:
                    self.__motNotif.set("/!\ Blanc c'est à toi de joueur")
            else:
                if J2 != 'P':
                    (c,a)=eval('placer_un_pion_'+J2+'(G,self.get_joueur())')
                    self.__fin = gagnant(G,self.get_joueur())
                    case = self.__cases[(c[0]-1)*self.__dimension+c[1]-1]
                    case.set_texte('O ')
                    case.set_color('Noir')
                    if a !=None:
                        case = self.__cases[(a[0]-1)*self.__dimension+a[1]-1]
                        case.set_texte(' ')
                        case.set_color('Vide')
                    if not self.__fin:
                        self.__joueur = chgt_couleur(self.__joueur)
                    self.__motNotif.set('')
                else:
                    self.__motNotif.set("/!\ Noir c'est à toi de joueur")
            
            if self.__fin:
                self.__motNotif.set(self.__joueur+" a gagné !")


fen = FenPrincipale()
fen.mainloop()


    
    
