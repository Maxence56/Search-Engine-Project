# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module permet de récupérer les données encodés sur un fichier txt.
"""

import io

def obtention_L_article(chaine_liste_article):
    """
    Cette fonction permet d'obtenir L_article à partir des données encodé dans le fichier txt
    """
    liste_article_str = chaine_liste_article.split(";")
    liste_article = []
    for article_str in liste_article_str:
        article = article_str.split(",")
        try:
            article[2] = int(article[2])  #traitement date
        except:
            article[2] = 0 #si une erreur survient on doit perdre la date pour éviter d'annulé le traitement.
        article[1] = article[1].split("/")  #traitement auteur
        liste_article.append(article)
    return liste_article

def obtention_dico(chaine):
    """
    Cette fonction permet d'obtenir un dico de int à partir des données du fichier
    """
    chaine.rstrip(";")
    liste_couple = chaine.split(";")
    dico = {}
    for couple in liste_couple:
        duo = couple.split(":")
        try:    
            cle = int(duo[0])
        except:
            cle = "not trouve"
            
        valeur_str = duo[1].split(".")
        valeur = []  #on convertie en nombre en prenant en considération les not trouve
        for el in valeur_str:
            try:
                valeur.append(int(el))
            except:
                valeur.append(el)
                
        dico[cle] = valeur
    return dico

def obtention_dico_nature(chaine):
    """
    Permet d'obtenir dico_nature à partir des données du fichier
    """
    liste_couple = chaine.split(";")
    dico = {}
    for couple in liste_couple:
        duo = couple.split(":")
        cle = int(duo[0])
        dico[cle] = duo[1]
    return dico

fichier = io.open("donnees_topologie", "r", encoding="utf-8")
donnees = fichier.readlines()
fichier.close()

for ligne in donnees:  #on retire le \n qui a été inserer en fin de ligne
    ligne.rstrip("\n")

L_article = obtention_L_article(donnees[1])
Dico_source_article = obtention_dico(donnees[3])
Dico_production_article = obtention_dico(donnees[5])
Graphe_lien = obtention_dico(donnees[7])
Graphe_suggestion = obtention_dico(donnees[9])
dico_nature = obtention_dico_nature(donnees[11])

def obtention_nature(article):
    """
    Cette fonction permet d'obtenir la nature d'un article. dico_nature ne contient pas tous les articles pour des soucis de place.
    """
    if article not in dico_nature.keys():
        return "sans nature spécifique"
    return dico_nature[article]

liste_nom=[L_article[i][0] for i in range(len(L_article))]
liste_nom.sort()

liste_date=[L_article[i][2] for i in range(len(L_article))]
liste_date.sort()
#une partie des erreurs vient du fait que je n'ai pas utiliser de bon séparateur pour encoder mes données  (les virgules et les points   On peut les remplacer par des | et des %  pour les limiter)