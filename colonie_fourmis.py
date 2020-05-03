# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 18:01:49 2020

@author: Numa Gout
"""

import numpy as np
import matplotlib.pyplot as plt

class Civilisation:
    ''' Classe Civilisation, contient l'information de toutes les fourmis, 
        villes, routes
        
        Attribut : nom = Nom de la civilisation
                   nest = Identifiant de la ville nid
                   food = Identifiant de la ville nourriture
                   routes = liste contenant toutes les routes
                   villes = liste contenant toutes les villes
                   fourmis = liste contenant toutes les fourmis
                   quantite_nourriture = Quantite de nourriture 
                                         ramenee dans le nid
                   selec_naturelle = Bouffe avant la selections naturelles'''
    
    def __init__(self, nom, nest, food, villes, routes):
        ''' Methode qui creer une civilisation'''
        self.nom = nom # Nom de la civilisation
        self.nest = nest # ID de la ville nid
        self.food = food # ID de la ville nourriture
        
        # Liste qui acceuille toutes les routes
        self.villes = [Ville(self, i, villes[i]) for i in range(len(villes))] 
        
        # Liste qui acceuille toutes les routes
        self.routes = [Route(self, routes[i], 10) for i in range(len(routes))]
        
        for i in range(len(villes)): 
            # Boucle qui rajoute les arretes voisines a une ville
            voisin = []
            for routes in self.routes:
                (r, s) = routes.link
                if i in (r, s):
                    voisin.append(routes)
            self.villes[i].set_voisin(voisin)
        
        # Liste contenant toutes les fourmis
        self.fourmis = [Fourmi(self, i, alpha = (np.random.rand())*5, 
                               beta = (np.random.rand())*5, 
                               gamma = (np.random.rand())*5)
                               for i in range(np.random.randint(50, 101))] 
        
        # Quantite de nourriture dans le nid 
        self.quantite_nourriture = 0 
        
        self.numero_generation = 0

    def tour_suivant(self):
        global duree_generation
        ''' Fait avancer le temps de 1, 
            chaque fourmis fait une action, 
            toutes les routes evaporent un peu de pheromone '''
        for ant in self.fourmis:
            ant.tour_suivant()
        for route in self.routes:
            route.evaporation_pheromone(p)
        
        if self.quantite_nourriture >= duree_generation:
            self.numero_generation += 1
            self.new_gen()
            
    def new_gen(self):
        ''' Méthode générant la nouvelle génération de fourmi '''
        global prop1
        global prop2
        self.quantite_nourriture = 0
        for ant in self.fourmis:
            if len(ant.trajet_effectue) == 0:
                ant.trajet_effectue.append(sum([r.longueur 
                                                for r in ant.historique]))
        # Liste triant les meilleurs fourmis
        best_travail = []
        for i in range(len(self.fourmis)):
            l = self.fourmis[i].trajet_effectue
            best_travail.append((self.fourmis[i].nourriture_ramenee,
                                 sum(l)/len(l), i))
        
        best_travail.sort(reverse = True, key = lambda x: (x[0], -x[1]))
        
        # Accouplement des fourmis
        n = len(self.fourmis)
        for i in range(n):
            if i>n*prop1 and i<=n*prop2+n*prop1:
                self.fourmis[best_travail[i][2]].accouplement(self.fourmis[best_travail[0][2]])
            else:
                self.fourmis[best_travail[i][2]] = Fourmi(self, 
                                                          best_travail[i][2], 
                                                          (np.random.rand())*5, 
                                                          np.random.rand()*5, 
                                                          np.random.rand()*5)
                
        # Réinitialisation des paramètres de route
        for r in self.routes:
            r.pheromone = 10
        for f in self.fourmis:
            f.nourriture_ramenee = 0
        
    def simulation(self, nb_generation):
        ''' Méthode lançant la simulation de la colonie de fourmis '''
        while self.numero_generation <= nb_generation:
            self.tour_suivant()
                
        
            
class Ville:
    ''' Classe Ville, contient l'information sur les villes
        Attribut : civ = Civilisation où elle est rattachée
                   numero = Identifiant de la ville
                   coord = Coordonnée de la ville (position dans le plan)'''
    
    def __init__(self, civilisation, numero, coord):
        ''' Creer une ville '''
        self.civ = civilisation 
        self.numero = numero
        self.coord = coord
        
    def set_voisin(self, voisin):
        ''' Change les voisins de la villes, 
            (sert a la creation de la civilisation '''
        self.voisin = voisin
        
class Route:
    ''' Classe Route, contient l'information sur les routes
        Attributs : civ = Civilisation où elle est rattachée
                    link = Identifiant des villes qu'elle lie 
                    pheromone = Taux de pheromone sur la routes
                    longueur = longueur de la routes (norme euclidienne)'''
    
    def __init__(self, civilisation, link, pheromone):
        ''' Construit une Route '''
        self.civ = civilisation
        self.link = link
        self.pheromone = pheromone
        r, s = self.link
        self.longueur = np.linalg.norm(np.array(self.civ.villes[r].coord)-
                                       np.array(self.civ.villes[s].coord))
        
    def evaporation_pheromone(self, p):
        ''' fait evaporer la pheromone de maniere exponentielle '''
        self.pheromone *= (1-p)
        
    def ajout_pheromone(self, pheromone):
        ''' ajoute une quantite definie de pheromone '''
        self.pheromone += pheromone
        
class Fourmi:
    ''' Classe Foumi, contient toutes les informations sur les fourmis
        Attributs : civ = Civilisation où elle est rattachée
                    alpha = coefficient changeant le comportement 
                            face aux choix de routes
                    beta = coefficient changeant le comportement 
                           face aux choix de routes
                    gamma = coefficient changeant le comportement 
                            face aux choix de routes
                    id = Identifiant de la fourmi
                    porte_food = booleen indiquant si la fourmi 
                                 porte de la nourriture
                    position = indique où se situe la fourmi 
                               (quelle route ou quelle villes)
                    historique = liste indiquant toutes les routes
                                 empruntées par la fourmis avant de 
                                 trouver la nourriture
                    distance_parcourue = distance parcourue sur un route 
                                         (se reinitialise a chaque changement 
                                         de route)
                    nourriture_ramenee = Quantité de nourriture ramenee par la
                                         fourmi
                    trajet_effectuee = liste des distances des trajets
                                       effectuees'''
    
    def __init__(self, civilisation, i, alpha, beta, gamma):
        ''' Construit une fourmi '''
        self.civ = civilisation
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.nourriture_ramenee = 0
        self.trajet_effectue = []
        self.id = i
        self.porte_food = False
        # La fourmi se situe au nid au debut
        self.position = self.civ.villes[self.civ.nest] 
        self.historique = []
        self.distance_parcourue = 0
        
    def prendre_food(self):
        ''' La fourmi prend de la nourriture '''
        self.porte_food = True
        
    def deposer_food(self):
        ''' La fourmi depose de la nourriture, 
            la qqte de nourriture de la civilisation augmente '''
        self.porte_food = False
        # Augmente la qqte de nourriture de la civilisation
        self.civ.quantite_nourriture += 1 
        self.nourriture_ramenee += 1
        
    def depot_pheromone(self):
        ''' Depose de la pheromone sur une route, 
        le taux de pheromone deposee varie suivant la longueur de la route '''
        self.position.ajout_pheromone(1/self.position.longueur)        
    
    def avancer(self):
        ''' Si la fourmi se situe sur une route, fait un pas en avant
            De plus, si la fourmi a traverse la route entiere, 
            change l'attribut position'''
        self.distance_parcourue += 1
        self.depot_pheromone()
        
        if self.distance_parcourue >= self.position.longueur: 
            # Condition de fin de route
            # On cherche vers quel villes la fourmi se dirigeait
            self.distance_parcourue = 0 
            (r, s) = self.position.link
            if self.porte_food: # 1er cas : la fourmi porte de la nourriture
                if len(self.historique) == 0:
                    # Si son historique est vide, elle est alors arrivee au nid
                    self.position = self.civ.villes[self.civ.nest]
                else:
                    # Sinon il faut trouver vers quelle ville elle se dirigeait
                    # La ville commune entre la route empruntée et la route 
                    # suivante à emprunter est la ville d'arrivee
                    t, u = self.historique[-1].link 
                    if t in (r, s):
                        self.position = self.civ.villes[t]
                    elif u in (r, s):
                        self.position = self.civ.villes[u]
                
            else: # 2e cas : elle ne porte pas de nourriture
                if len(self.historique) == 0:
                    # Si son historique est vide alors elle part du nid, 
                    # la ville d'arrivee est donc la ville qui relie le nid
                    self.historique.append(self.position)
                    r, s = self.position.link
                    if r == self.civ.nest:
                        # Si r est le nid et que la fourmi est sur la route 
                        # (r, s) alors s est la ville d'arrivee
                        self.position = self.civ.villes[s]
                    elif s == self.civ.nest:
                        # Sinon c'est r la ville d'arrivee
                        self.position = self.civ.villes[r]
                else:
                    # Si son historique n'est pas vide  
                    
                    # il faut trouver la ville vers laquelle elle se dirigeait
                    # La ville commune entre la route empruntee et la route 
                    # deja empruntee est la ville de depart de la fourmi
                    (r, s) = self.historique[-1].link
                    (t, u) = self.position.link
                    self.historique.append(self.position)
                    if t in (r, s):
                        self.position = self.civ.villes[u]
                    elif u in (r, s):
                        self.position = self.civ.villes[t]
                

    def choix_route(self):
        ''' Si la fourmi se situe sur une Ville, 
            choisi une ville a emprunter '''
        if self.porte_food: 
        # Si la fourmi porte de la nourriture alors il faut 
        # emprunter la ville de l'historique
            self.position = self.historique.pop()
        else: 
            if len(self.position.voisin) == 1: # Si cul-de-sac
                self.position = self.position.voisin[0]
        # Sinon on calcul les poids de chaque route puis on en choisit 
        # un aleatoire en fonction des poids
            else:
                poids = []
                for route in self.position.voisin:
                    if len(self.historique) == 0:
            # Calcul des poids des routes voisines qui ne sont pas demi-tour
                        P = ((route.pheromone**self.alpha)*
                            ((1/route.longueur)**self.beta))
                        poids.append(P)
                    else:
                        if self.historique[-1].link == route.link:
                            P = 0
                            poids.append(P)
                        else:
                            P = ((route.pheromone**self.alpha)*
                                (route.longueur**self.beta))
                            poids.append(P)
                            
                total = sum(poids)
                probabilite = [P/total for P in poids] # liste des probabilites
                choix = np.random.rand()
                seuil = 0
                for i in range(len(probabilite)):
                    seuil += probabilite[i]
                    if choix <= seuil:
                        self.position = self.position.voisin[i]
                        break
                    
            
    def tour_suivant(self):
        ''' Fait avancer les fourmis de 1 etapes'''
        if self.distance_parcourue != 0:
            # Si les fourmis sont sur une route elles font un pas en avant
            self.avancer()
        else:
            # Sinon elles sont sur une villes
            if self.position.numero == self.civ.food:
                # Si la fourmi est a la ville nourriture
                if self.porte_food:
                    # Si elle porte de la nourriture elle revient sur ses pas
                    self.choix_route()
                    self.distance_parcourue += 1
                else:
                    # Sinon elle ramasse de la nourriture
                    self.prendre_food()
                    self.trajet_effectue.append(sum([r.longueur 
                                                     for r in self.historique]))
            elif self.position.numero == self.civ.nest:
                # Si la fourmi est au nid
                if self.porte_food:
                    # Si elle porte de la nourriture elle la depose
                    self.deposer_food()
                else:
                    # Sinon elle choisit une route pour avancer
                    self.choix_route()
                    self.distance_parcourue += 1
            else:
                # Si la fourmi est dans une ville quelconque elle avance
                self.choix_route()
                self.distance_parcourue += 1
                
    def accouplement(self, ant):
        ''' Fait s'accoupler 2 fourmis '''
        global taux_mutation
        for n in range(3):
            choix = np.random.randint(2)
            if n == 0:
                if choix == 1:
                    self.alpha = ant.alpha
            elif n == 1:
                if choix == 1:
                    self.beta = ant.beta
            else:
                if choix == 1:
                    self.gamma = ant.gamma
            
        # On fait muter la fourmi avec peu de chance
        if np.random.rand() < taux_mutation:
            self.mutation()
        
    def mutation(self):
        ''' Fait muter une fourmi '''
        choix = np.random.randint(0, 3)
        if choix == 0:
            self.alpha = (np.random.rand())*5
        elif choix == 1:
            self.beta = (np.random.rand())*5
        else:
            self.gamma = (np.random.rand())*5
               
            
p = 0.3 # Taux d'evaporation
prop1 = 1/2
prop2 = 1/3
taux_mutation = 0.1
duree_generation = 400


villes = [(0, 0), (1, 1), (-5, 1), (0, 2)]
routes = [(0, 1), (0, 2), (1, 3), (2, 3)]
Fourmiland = Civilisation('Fourmiland', 0, 3, villes, routes)
Fourmiland.simulation(10)
    
ville_x = [v[0] for v in villes]
ville_y = [v[1] for v in villes]
for i in range(len(routes)):
    plt.plot([ville_x[routes[i][0]], ville_x[routes[i][1]]], 
             [ville_y[routes[i][0]], ville_y[routes[i][1]]], 
             color = 'black', zorder = 0, 
             linewidth = Fourmiland.routes[i].pheromone)
plt.scatter(ville_x, ville_y, color = 'blue', s = 100)
plt.scatter(ville_x[Fourmiland.nest], ville_y[Fourmiland.nest], 
            color = 'red', label = 'Nid', s = 100)
plt.scatter(ville_x[Fourmiland.food], ville_y[Fourmiland.food], 
            color = 'green', label = 'Nourriture', s = 100)
plt.legend()
#plt.savefig('Graphe_3_gene')