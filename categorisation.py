# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert de bibliothèque pour calculer les points de nature.
"""

def points_reference(article, graphe_est_cite, liste_correspondance_article_indice):
  """
  Cette fonction donne un score à l'article pour déterminer si l'article est une reference.
  Comme d'habitude article désigne l'indice de l'article et non les données associé comme son nom ou sa date de parution.
  Pour identifier si l'article est une reference. On donne des points pour chaque article qui le cite.
  Plus l'article qui le cite est récent plus il rapporte de points. Cela permet de prendre en compte le veillissement des articles qui passent de références à obsolètes.  
  """
  if article in graphe_est_cite.keys():
    liste_article_citeur = graphe_est_cite[article]
    points = 0
    dates = [2050-10*k for k in range(10)]#on va de 2050 à 1950
    for article in liste_article_citeur:
      if article == "not trouve": #En cas de probleme on considere qu'il n'existe pas
          date_ecriture = 0
      else:
          date_ecriture = liste_correspondance_article_indice[article][2] #On extrait la date d'écriture de l'article
      i=0
      decennie = False
      while i<len(dates) and not decennie:
        if date_ecriture>dates[i]: #on identifie la décennie de l'article
          decennie = True
          points+=10-i # plus l'article citeur est recent plus on ajoute de points
        i+=1
    
  else:
      points = 0 # Il n'est jamais cité Ce n'est pas une référence.
  return points

def novateur(indice_article, graphe_est_cite, liste_correspondance_article_indice, annee_min=2015):
  annee_parution = liste_correspondance_article_indice[indice_article][2]
  if annee_parution<annee_min:  #il est trop vieux pour être considéré comme novateur
    return 0
  return points_reference(indice_article, graphe_est_cite, liste_correspondance_article_indice)
