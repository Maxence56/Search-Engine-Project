# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert à gérer les liens entre les articles
"""

from stockage_donnees import super_copy

def fusion_dico_emplace(dico1, dico2):  #cette fonction sera utile pour fusionner les dico d'attributions de points
  """
  Cette procédure permet de fusionner deux dictionnaires qui contiennent le même type d'objet (liste, int,...) (sans écrasement).
  Elle rajoute dico2 au dico1
  """
  liste_cle1 = dico1.keys()
  liste_cle2 = dico2.keys()
  for cle in liste_cle2:
    if cle in liste_cle1:
      dico1[cle]+=dico2[cle]
    else:
      dico1[cle] = dico2[cle]


def fusion_memoire_nb_chemin(dico1, dico2):  
  """
  Cette procédure permet de fusionner deux dictionnaires sans écrasement
  Elle rajoute dico2 au dico1.
  dico1 et dico2 sont de la forme [distance]:{[article]:nb_lien}
  """
  liste_cle1 = dico1.keys()
  liste_cle2 = dico2.keys()

  for cle in liste_cle2:
    if cle in liste_cle1:

      liste_nouveaux_articles = dico2[cle].keys()
      liste_anciens_articles = dico1[cle].keys()

      for article in liste_nouveaux_articles:
        if article in liste_anciens_articles:
          dico1[cle][article]+=1  #on a trouve un nouveau chemin liant ces deux articles aussi on rajoute +1 en distance
        else:
          dico1[cle][article] = 1
    else:
      dico1[cle] = dico2[cle]
    
def obtention_dico_taille(taille, graphe, article_depart):
    """
    Cette fonction sert à réaliser le travaille de l'étape taille lors de la réalisation de la fonction chemin_taille_max_nb_chemin
    """

    if article_depart in graphe.keys():  #on vérifie que ce n'est pas un cul de sac (dû au fait qu'on empêche les allers-retours)
      liste_article_connecte = graphe[article_depart]
    else:
      liste_article_connecte = []

    dico_inter={}
    for article in liste_article_connecte:
      dico_inter[article] = 1  #on a trouvé 1 chemin

    dico={}
    dico[taille] = dico_inter
    return dico

def suppression_noeud(dico, noeud):
    """
    dico : dico avec en valeur une liste de noeuds
    noeud : int qui représente  un article (un noeud du graphe)
    
    Cette procédure enlève le noeud passe en paramètre du graphe (il permet d'eviter les boucles et les allers-retours)
    """
    liste_valeurs = list(dico.values()) #il sera possible d'améliorer en la supprimant seulement des valeurs des voisins du noeud
    for liste_voisin in liste_valeurs:
        if noeud in liste_voisin:
            liste_voisin.remove(noeud)

def chemin_taille_max_nb_chemin(graphe, article_depart, taille_max, taille=1):
  """
  Cette fonction prend un article et renvoie un dico avec en cle la distance et en valeur un dictionnaire contenant en cle les articles qui lui sont lié en valeur le nb de chemin de cette distance qui permet de lier l'article de départ à l'article en clé.
  Quand on veut l'appeler on rentre graphe, article_depart, taille_max(la taille max sera inclus dans le dictionnaire).
  taille correspond à l'etape actuelle où on en est (la taille du chemin actuel)
  liste _resultat_taille_inf correspond aux résultats precedants
  """

  if taille==taille_max:
    return obtention_dico_taille(taille, graphe, article_depart)

  else:
    dico = obtention_dico_taille(taille, graphe, article_depart)
    n_graphe = super_copy(graphe)

    if article_depart in graphe.keys():
      liste_article_connecte = graphe[article_depart]
      del n_graphe[article_depart] 
      suppression_noeud(n_graphe, article_depart)# On empêche le retour en arrière.
    else:
      liste_article_connecte = []

    for article in liste_article_connecte: #on progresse dans le chemin
      fusion_memoire_nb_chemin(dico, chemin_taille_max_nb_chemin(n_graphe, article, taille_max, taille=taille+1))

    return dico

def attribution_point_nb_lien(graphe_distance):
  """
  Cette fonction retourne le dictionnaire qui contient les articles en cle leurs points attribués par les liens bibliographiques en citation.
  Pour des économies de mémoire le dico ne contient que les articles qui ont obtenu des points grâce à cette fontion.
  graphe_distance correspond au résultat de chemin_taille_max_nb_chemin. 
  Le resultat est de la forme [article]:points
  """
  liste_distance = list(graphe_distance.keys())
  point_dist1 = 10
  point_dist2 = 5
  point_dist3 = 3

  # initialisation du dico
  dico_article = {}
  liste_article_inter = list(graphe_distance.values())
  liste_article_inter = [list(liste_article_inter[i].keys()) for i in range(len(liste_article_inter))]
  liste_article_concerne = []
  for el in liste_article_inter:
    liste_article_concerne+=el  #on obtient la liste de tous les articles qui obtiendront des points grâce à cette fonction
  for article in liste_article_concerne:
    dico_article[article] = 0  #on initialise une valeur pour faciliter l'attribution des points après
  
  #attribution des points
  for distance in liste_distance:
    liste_article =  list(graphe_distance[distance].keys())
    if distance==1:
      point = point_dist1
    elif distance==2:
      point = point_dist2
    else:
      point = point_dist3
    for article in liste_article:
      dico_article[article]+=point*graphe_distance[distance][article]  #on multiplie par le nb de lien

  return dico_article

def insert(article, liste, graphe_points):
  """
  Cette fonction prend un article, une liste ordonnée par ordre décroissant, le dico indiquant le taux de similarité.
  Elle renvoie la liste passé en paramètre avec l'article inseré dedans. 
  """
  i = 0
  mis = False
  points_article = graphe_points[article]  #pour éviter d'avoir à toujours le rechercher dans le dictionnaire

  while i<len(liste) and not mis:  #insertion de l'article
    if graphe_points[liste[i]]<points_article:
      liste = liste[:i]+[article]+liste[i:]
      mis = True
    i+=1

  if not mis: #si l'article n'a pas été rajouté, on le rajoute à la fin
    liste = liste+[article]

  return liste #le return est nécessaire


def selection_articles_pour_suggestion(graphe_points):
  """
  Cette fonction prend un graphe de point et renvoie la liste ordonnées des articles similaires par ordre décroissants de points (le premier à le nb max et le dernier le nb min)
  """
  liste_article = list(graphe_points.keys())
  
  if liste_article==[]:
      return []
  
  resultat = [liste_article[0]]
  for i in range(1, len(liste_article)):
    resultat = insert(liste_article[i], resultat, graphe_points)
  return resultat
      