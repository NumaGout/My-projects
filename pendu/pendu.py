from tkinter import *
from random import randint

class ZoneAffichage(Canvas):
    ''' Classe où sera affiché le pendu '''
    
    def __init__(self,parent,largeur,longueur,couleur):
        ''' Init méthode '''
        Canvas.__init__(self,master=parent,width=largeur,height=longueur,bg=couleur)
        self.__pendu = ['ImagesPendu/pendu'+str(i+1)+'.gif' for i in range(8)]
        # On créer une liste avec tout les liens des images
        Image = PhotoImage(file=self.__pendu[0]) # On adapte la taille de la Zone à celle des Images.
        self.config(height=Image.height(),width=Image.width())
    
    def affiche(self,nb):
        ''' Affiche le pendu au fur et à mesure des erreurs '''
        #On met à jour l'image du pendu en fonction du nombre d'erreurs
        nomImage ='ImagesPendu/pendu'+str(nb)+'.gif'
        self.__image = PhotoImage(file=nomImage)
        self.create_image(0,0, anchor=NW, image=self.__image)
        
class MonBouton(Button):
    ''' Classe MonBouton, les touches du clavier '''
    
    def __init__(self,parent,fen,t,largeur): 
        ''' Initialisation methode '''
        Button.__init__(self,master=parent,text=t,width=largeur)
        self.__lettre = t 
        self.__fenetrePrincipale = fen 
        
    def cliquer(self):
        ''' Méthode après avoir cliqué sur un bouton du clavier '''
        self.config(state=DISABLED) # Désactive le bouton
        self.__fenetrePrincipale.traitement(self.__lettre) # lance la méthode de la classe FenPrincipale

class FenPrincipale(Tk):
    ''' Fenetre tkinter, contient toutes les informations sur le pendu '''
    
    def __init__(self):
        ''' Initialisation de la fenêtre '''
        Tk.__init__(self)
        self.title('Jeu du Pendu')
        
        # Initialisation des attributs de bases
        self.__mot = '' # Mot à deviner
        self.__motAffiche = '' # Mot affiché
        fichiermot = open('mots.txt','r')
        self.__mots = fichiermot.read().splitlines() # Liste des mots possibles
        fichiermot.close()
        self.__nbManque = 0 # Nb d'erreurs
        self.__Joueur = None # Nom du joueur
        fichierscore = open('scores.txt','r')
        l = fichierscore.read().splitlines()
        fichierscore.close()
        self.__scores = [l[i].split(' ') for i in range(len(l))] # Table des scores
        
        # Initialisation des boutons Nouvelle partie etc ...
        self.__frameControle = Frame(self)
        self.__frameControle.pack(side=TOP,padx=5,pady=5)
        self.__BoutonNew = Button(self.__frameControle,text = 'Nouvelle Partie', width = 13, command = self.nouvellePartie)
        self.__BoutonNew.pack(side=LEFT,padx=5,pady=5)
        self.__BoutonQuit = Button(self.__frameControle,text = 'Quitter', width = 13, command=self.destroy)
        self.__BoutonQuit.pack(side=LEFT,padx=5,pady=5)
        # Bouton qui affiche le score sur une autre fenetre
        self.__BoutonScore = Button(self.__frameControle,text = 'Score',width=13, command=self.affichageScore)
        self.__BoutonScore.pack(side=LEFT,padx=5,pady=5)
        # Bouton pour changer le joueur qui joue
        self.__BoutonJoueur = Button(self.__frameControle,text = 'Changer Joueur',width=13,command=self.ChangementJoueur)
        self.__BoutonJoueur.pack(side=LEFT,padx=5,pady=5)
        
        # Placement de la Zone d'affichage
        self.__ZoneAff = ZoneAffichage(self,320,320,'snow2')
        self.__ZoneAff.pack(side=TOP,padx=5,pady=5)
        
        # Placement du mot à trouver
        self.__lmot = Label(self,text='Mot : ')
        self.__lmot.pack(side=TOP)
        
        # Placement du clavier
        self.__frameBouton = Frame(self)
        self.__frameBouton.pack(side=TOP,padx=5,pady=5)
        self.__boutons = []
        for i in range(26):
            t = chr(ord('A')+i)
            self.__boutons.append(MonBouton(self.__frameBouton,self,t,4))
            self.__boutons[i].config(command=self.__boutons[i].cliquer)

        for i in range(3):
            for j in range(7):
                self.__boutons[i*7+j].grid(row=i,column=j)
                
        for j in range(5):
            self.__boutons[21+j].grid(row=3,column=j+1)
        
        self.actualiseMot() # Pour afficher le mot
        self.nouvellePartie()
        
    def nouvellePartie(self):
        ''' Lance une nouvelle partie '''
        if self.__Joueur == None: # Lors de la première partie cette attribut est None
            self.ChangementJoueur()
            
        self.nouveauMot()
        self.actualiseMot()
        self.__ZoneAff.delete(ALL)
        self.__nbManque = 0
        
        for b in self.__boutons:
            b.config(state='normal')
            
    def traitement(self,lettre):
        ''' Vérifie si la lettre est dans le mot et agis en conséquence '''
        s = ''
        b = True # Booléen qui donne si la lettre est présente
        for i in range(len(self.__mot)):
            if self.__mot[i] == lettre:
                s += lettre
                b=False
            else:
                s += self.__motAffiche[i]
        self.__motAffiche = s[:]
        if b:
            self.__nbManque += 1
            self.__ZoneAff.affiche(self.__nbManque)
            if self.__nbManque == 8:
                self.finPartie(b)
        else:
            self.actualiseMot()
            if self.__mot==self.__motAffiche:
                self.finPartie(b)
                
    def nouveauMot(self):
        ''' Change de mot à deviner '''
        self.__mot = self.__mots[randint(0,len(self.__mots))]
        self.__motAffiche = len(self.__mot)*'*'
        
    def actualiseMot(self):
        ''' Change l'affichage du mot à deviner '''
        self.__lmot.config(text = 'Mot : '+self.__motAffiche)
        
    def ChangementJoueur(self): 
        ''' Change de joueur '''
        fenetreJoueur = Toplevel() # Une fenetre secondaire qui demande le nom du joueur
        fenetreJoueur.transient(self)
        fenetreJoueur.title('Quel-est ton pseudo ? ')
        Label(fenetreJoueur,text= 'Quel-est ton pseudo ?').pack(side=TOP)
        nom = StringVar()
        texte = Entry(fenetreJoueur,textvariable = nom)
        texte.pack()
        def repondre():
            self.__Joueur = nom.get()
            fenetreJoueur.destroy()
        Button(fenetreJoueur,text='Valider',command=repondre).pack(side=TOP)
        
    def affichageScore(self):
        ''' Affiche le score sur une nouvelle fenetre '''
        fenetreScore = Toplevel() # Nouvelle fenetre avec Joueur : Victoire :  Défaite :  Ratio :
        fenetreScore.title('Table des Scores')
        
        for i in range(len(self.__scores)):
            Label(fenetreScore,text ='Joueur : '+ self.__scores[i][0]+' Nombre de victoires : '+self.__scores[i][1]+ ' Nombres de défaites : '+self.__scores[i][2]+ ' Ratio : '+self.__scores[i][3]).pack(side=TOP)
 
        Button(fenetreScore,text='Quitter',command=fenetreScore.destroy).pack(side=TOP)
        
    def finPartie(self,b):
        ''' Méthode de fin de partie, si b = True c'est une victoire, sinon une défaite '''
        for k in self.__boutons: # Désactivation des boutons
            k.config(state=DISABLED)
        
        if b:
            self.__lmot.config(text = 'Vous avez perdu le mot était : '+self.__mot)
            presence = False # Booléen si le joueur est nouveau dans la table des scores
            for i in range(len(self.__scores)): # On parcours les joueurs
                if self.__scores[i][0] == self.__Joueur:
                    self.__scores[i][2] =str(int(self.__scores[i][2])+1) # +1 défaite
                    self.__scores[i][3] = str(int(int(self.__scores[i][1])/(int(self.__scores[i][1])+int(self.__scores[i][2]))*100))+'%' # recalcul du ratio
                    presence = True
            if not presence:
                self.__scores.append([self.__Joueur,'0','1','0']) # ajout d'un joueur
        else:
            self.__lmot.config(text='Vous avez gagné le mot était bien : '+self.__mot)
            presence = False # Booléen si le joueur est nouveau dans la table des scores
            for i in range(len(self.__scores)): # On parcours les joueurs
                if self.__scores[i][0] == self.__Joueur:
                    self.__scores[i][1] = str(int(self.__scores[i][1])+1) # +1 victoire
                    self.__scores[i][3] = str(int(int(self.__scores[i][1])/(int(self.__scores[i][1])+int(self.__scores[i][2]))*100))+'%' # On recalcule le ratio
                    presence = True
            if not presence:
                self.__scores.append([self.__Joueur,'1','0','100']) # Ajout d'un joueur
        fichierScore = open('scores.txt','w')
        fichierScore.write('\n'.join([' '.join(l) for l in self.__scores])) # ecrit le tableau des scores
        fichierScore.close
        
               
fen=FenPrincipale()
fen.mainloop()
