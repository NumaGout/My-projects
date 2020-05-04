# -*- coding: utf-8 -*-
"""
Created on Mon May  4 17:37:44 2020

@author: Numa Gout
"""

from datetime import date
l_bibliotheque = [] #Liste des bibliothèques


# ***** classe Personne *****
class Personne:
    ''' Classe Personne, modélise un humain '''
    
    def __init__(self,nom,prenom,adresse):
        ''' Init d'un humain '''
        self.__nom = nom
        self.__prenom = prenom
        self.__adresse = adresse
    
    def set_nom(self,nom):
        ''' Change le nom '''
        self.__nom = nom
    
    def get_nom(self):
        ''' Lit le nom '''
        return self.__nom
    
    def set_prenom(self,prenom):
        ''' Change le prénom '''
        self.__prenom = prenom
    
    def get_prenom(self):
        ''' Lit le prénom '''
        return self.__prenom
    
    def set_adresse(self,adresse):
        ''' Change l'adresse '''
        self.__adresse = adresse
    
    def get_adresse(self):
        ''' Lit l'adresse '''
        return self.__adresse
    
# ***** classe Lecteur *****
class Lecteur(Personne):
    ''' Classe Lecteur, hérite de la classe Personne et modélise un lecteur d'une bibliothèque '''
 
    def __init__(self,nom,prenom,adresse,numero):
        ''' Créer un lecteur '''
        Personne.__init__(self,nom,prenom,adresse)
        self.__numero = numero
        self.__nb_emprunts = 0
    
    def set_numero(self,numero):
        ''' Change le numéro '''
        self.__numero = numero
    
    def get_numero(self):
        ''' Lit le numéro '''
        return self.__numero
    
    def set_nb_emprunts(self,nb_emprunts):
        ''' Change le nom de ses emprunts '''
        self.__nb_emprunts = nb_emprunts
    
    def get_nb_emprunts(self):
        ''' Lit le nombre de ses emprunts '''
        return self.__nb_emprunts

# ***** classe Bibliothecaire *****
class Bibliothecaire(Personne):
    ''' Classe bibliothecaire, modélise un bibliothècaire, hérite de la classe Personne '''
 
    def __init__(self,nom, prenom, adresse, numero):
        ''' Créer un bibliothecaire '''
        Personne.__init__(self,nom,prenom,adresse)
        self.__numero = numero

    def set_numero(self,numero):
        ''' Change le numéro '''
        self.__numero = numero
    
    def get_numero(self):
        ''' Lit le numéro '''
        return self.__numero
    
# ***** classe Conservateur *****
class Conservateur(Personne):
    ''' Classe conservateur, hérite de la classe Personne, humain qui gère une bibliothèque '''
    
    def __init__(self,nom,prenom,adresse):
        ''' Créer un conservateur '''
        Personne.__init__(self,nom,prenom,adresse)

    def info(self):
        ''' Renvoie le nom de la bibliothèque gérée par le conservateur '''
        for b in l_bibliotheque:
            if b.get_conservateur() == self.get_nom():
                return b.get_nom()
            
# ***** classe Livre *****
class Livre:
    ''' Classe Livre, modélise un livre '''
    
    def __init__(self,titre,auteur,numero,nb_tot):
        ''' Créer un livre '''
        self.__titre = titre
        self.__auteur = auteur
        self.__numero = numero
        self.__nb_tot = nb_tot
        self.__nb_disp = nb_tot
        
    def set_auteur(self,auteur):
        ''' Change l'auteur '''
        self.__auteur = auteur
        
    def get_auteur(self):
        ''' Renvoie l'auteur '''
        return self.__auteur
    
    def set_titre(self,titre):
        ''' Change le titre '''
        self.__titre = titre
        
    def get_titre(self):
        ''' Renvoie le titre '''
        return self.__titre
    
    def set_num(self,numero):
        ''' Change le numero '''
        self.__numero = numero
   
    def get_num(self):
        ''' Renvoie le numéro '''
        return self.__numero
    
    def set_nb_tot(self,nb_total):
        ''' Change le nombre d'exemplaire du livre total '''
        self.__nb_tot = nb_total
    
    def get_nb_tot(self):
        ''' Renvoie le nombre d'exemplaire du livre total '''
        return self.__nb_tot
    
    def set_nb_disp(self,nb_dispo):
        ''' Change le nombre d'exemplaire du livre disponible '''
        self.__nb_disp = nb_dispo
    
    def get_nb_disp(self):
        ''' Renvoie le nombre d'exemplaire du livre disponible '''
        return self.__nb_disp
    
# ***** classe Emprunt *****
class Emprunt:
    ''' Classe Emprunt, modélise un emprunt avec les infos nécéssaire '''
    
    def __init__(self,numero_lecteur,numero_livre,numero_bibliothecaire):
        ''' Créer un emprunt '''
        self.__numero_lecteur = numero_lecteur
        self.__numero_livre = numero_livre
        self.__numero_bibliothecaire = numero_bibliothecaire
        self.__date = date.isoformat(date.today())
    
    def get_numero_lecteur(self):
        ''' Renvoie le numéro du lecteur associé '''
        return self.__numero_lecteur
    
    def get_numero_livre(self):
        ''' Renvoie le numéro du livre associé '''
        return self.__numero_livre
    
    def get_numero_bibliothecaire(self):
        ''' Renvoie le numéro du bibliothécaire qui à enregistré l'emprunt '''
        return self.__numero_bibliothecaire
    
    def get_date(self):
        ''' Renvoie la date de l'emprunt '''
        return self.__date
    
# ***** classe Bibliotheque *****
class Bibliotheque:
    ''' Classe Bibliotheque, modélise une bibliotheque '''
    
    def __init__(self,nom):
        ''' Créer une bibliothèque '''
        self.__nom = nom
        self.__lecteurs = []
        self.__livres = []
        self.__emprunts = []
        self.__bibliothecaire = []
        self.__conservateur = []
        l_bibliotheque.append(self)

    def get_nom(self):
         ''' Renvoie le nom de la bibliothèque '''
         return self.__nom

    def get_conservateur(self):
        ''' Renvoie le nom du conservateur de la bibliothèque '''
        return self.__conservateur[0]

    def ajout_lecteur(self,nom,prenom,adresse,numero):
        ''' Ajoute un lecteur dans la bibliothèque '''
        self.__lecteurs.append(Lecteur(nom,prenom,adresse,numero))
        
    def retrait_lecteur(self,numero):
        ''' Retire un lecteur de la bibliothèque '''
        # On cherche le lecteur
        lecteur = self.chercher_lecteur_numero(numero)
        if lecteur == None:
            return False
        # On verifie qu'il n'a pas d'emprunt en cours
        for e in self.__emprunts:
            if e.get_numero_lecteur()==numero:
                return False
        # On peut ici retirer le lecteur de la liste
        self.__lecteurs.remove(lecteur)
        return True

    def ajout_livre(self,auteur,titre,numero,nb_total):
        ''' Ajoute un livre '''
        self.__livres.append(Livre(auteur,titre,numero,nb_total))

    def ajout_bibliothecaire(self,nom,prenom,adresse,numero):
        ''' Ajoute un bibliothécaire '''
        self.__bibliothecaire.append(Bibliothecaire(nom,prenom,adresse,numero))

    def ajout_conservateur(self,nom,prenom,adresse):
        ''' Ajoute un conservateur '''
        if len(self.__conservateur) != 0:
            return None

        self.__conservateur.append(Conservateur(nom,prenom,adresse))
        
    def depart_conservateur(self):
        ''' Retire un conservateur '''
        self.__conservateur.clear
        
    def depart_bibliothecaire(self,num):
        ''' Retire un bibliothécaire '''
        bibli = self.chercher_bibliothecaire(num)
        if bibli == None:
            return False

        self.__bibliothecaire.remove(bibli)
        return True

    def retrait_livre(self,numero):
        ''' Retire un livre de la bibliothèque '''
        # On cherche le livre
        livre = self.chercher_livre_numero(numero)
        if livre == None:
            return False
        # On verifie que le livre n'est pas en cours d'emprunt
        for e in self.__emprunts:
            if e.get_numero_livre()==numero:
                return False
        # On peut ici retirer le livre de la liste
        self.__livres.remove(livre)
        return True
    
    def chercher_lecteur_numero(self,numero):
        ''' Recherche un lecteur par son numéro '''
        for l in self.__lecteurs:
            if l.get_numero() == numero:
                return l
        return None
    
    def chercher_lecteur_nom(self,nom,prenom):
        ''' Recherche un lecteur par son nom, prénom '''
        for l in self.__lecteurs:
            if l.get_nom() == nom and l.get_prenom() == prenom:
                return l
        return None
    
    def chercher_livre_numero(self,numero):
        ''' Recherche un livre par son numéro '''
        for l in self.__livres:
            if l.get_num() == numero:
                return l
        return None
    
    def chercher_livre_titre(self,titre):
        ''' Recherche un livre par son titre '''
        for l in self.__livres:
            if l.get_titre() == titre:
                return l
        return None
    
    def chercher_emprunt(self, numero_lecteur, numero_livre):
        ''' Recherche un emprunt '''
        for e in self.__emprunts:
            if e.get_numero_lecteur() == numero_lecteur and e.get_numero_livre() == numero_livre:
                return e
        return None

    def chercher_bibliothecaire(self,numero):
        ''' Recherche un bibliothécaire '''
        for b in self.__bibliothecaire:
            if b.get_numero() == numero:
                return b
        return None
    
    def emprunt_livre(self, numero_lecteur, numero_livre, numero_bibliothecaire):
        ''' Emprunte un livre '''
        # On verifie que le numero de livre est valide
        livre = self.chercher_livre_numero(numero_livre)
        if livre == None:
            print('Emprunt impossible : livre inexistant')
            return None
        # On verifie qu'il reste des exemplaires disponibles pour ce livre
        if livre.get_nb_disp() == 0:
            print('Emprunt impossible : plus d\'exemplaires disponibles')
            return None
        # On verifie que le numero de lecteur est valide
        lecteur = self.chercher_lecteur_numero(numero_lecteur)
        if lecteur == None:
            print('Emprunt impossible : lecteur inexistant')
            return None
        # On verifie que ce lecteur n'a pas deja emprunte ce livre
        e = self.chercher_emprunt(numero_lecteur, numero_livre)
        if e != None:
            print('Emprunt impossible : deja en cours')
            return None
        
        if self.chercher_bibliothecaire(numero_bibliothecaire) == None:
            print('Emprunt impossible : Bibliothecaire inexistant')
            return None
        # Les conditions sont reunies pour pouvoir faire cet emprunt
        self.__emprunts.append(Emprunt(numero_lecteur, numero_livre,numero_bibliothecaire))
        livre.set_nb_disp(livre.get_nb_disp()-1)
        lecteur.set_nb_emprunts(lecteur.get_nb_emprunts()+1)
        return self.__emprunts[-1]
    
    def retour_livre(self, numero_lecteur, numero_livre):
        ''' Retour d'un livre emprunté '''
        # On recherche l'emprunt identifie par le numero de livre et de lecteur
        e = self.chercher_emprunt(numero_lecteur, numero_livre)
        if e != None: # l'emprunt existe, on le retire de la liste et on met a jour nb_emprunt pour le lecteur et nb_dispo pour le livre
            self.__emprunts.remove(e)
            lecteur = self.chercher_lecteur_numero(numero_lecteur)
            if lecteur != None : lecteur.set_nb_emprunts(lecteur.get_nb_emprunts()-1)
            livre = self.chercher_livre_numero(numero_livre)
            if livre != None: livre.set_nb_disp(livre.get_nb_disp()+1)
            print('Retour effectue')
            return True
        else:
            print('Aucun emprunt ne correspond a ces informations')
            return False

    def affiche_lecteurs(self):
        ''' Affiche les lecteurs enregistrés dans la bibliothèque '''
        for l in self.__lecteurs:
            print(l)
    
    def affiche_livres(self):
        ''' Affiche les livres enregistrés dans la bibliothèque '''
        for l in self.__livres:
            print(l)
    
    def affiche_emprunts(self):
        ''' Affiche tous les emprunts '''
        for e in self.__emprunts:
            print(e)
    
    def affiche_bibliothecaire(self):
        ''' Affiche tous les bibliothécaires de la bibliothèque '''
        for b in self.__bibliothecaire:
            print(b)
