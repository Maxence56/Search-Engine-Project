# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module prepare toutes les données dont l'utilisateur a besoin.
"""

from extraction_bibliographie import*
from categorisation import*
from gestion_lien import*
from stockage_donnees import*
from obtention_metadonnees import*
from egalites import*
from analyse_donnees import*

#variables globales de stockage
global L_article #cette liste permet avec les indices d'obtenir les articles
global Dico_source_article #ce dico contient [indice_article]:[sources]
global Dico_production_article #ce dico contient [indice_article]:[articles qui s'en inspirent]

#initialisation
L_article = []
Dico_source_article = {}
Dico_production_article = {}

def obtention_indice(article):
  """
  Cette fonction permet à partir d'un article d'obtenir son indice.
  """
  for i in range(len(L_article)):
    if egalite_articles(L_article[i], article):
      return i
  return 'not trouve'

def mise_en_forme(pdf, chaine):
  """
  Cette fonction doit extraire d'un pdf les donnees de l'article et de ses sources.
  """
  article_en_cours = traitement_meta(obtention_metadonnees(pdf))
  l_donnees_article_cite = extraction_biblio(chaine)
  l_article_cite = []
  for el in l_donnees_article_cite: 
    nouvel_article = procesus_complet(el)
    if len(nouvel_article)!=0:  #les listes vides doivent être enlevée pour éviter des erreurs de traitements
      l_article_cite.append(nouvel_article)
  return [article_en_cours]+l_article_cite

def indice_article(article):
  """
  Cette procédure permet de rajouter un article dans les bases de donnees
  Variable L_article
  """
  #on verifie si il a déjà été mémorisé
  i = 0
  est_dedans = False
  while i<len(L_article) and not est_dedans:
    if egalite_articles(article, L_article[i]):
      est_dedans = True
    i+=1

  #sinon on le mémorise (fonctionne même si L_article est vide)
  if not est_dedans:
    L_article.append(article)

def mise_jour_base_de_donnees(pdf, chaine):
  """
  Cette procédure permet de mettre à jour les 3 variables globales à chaque q'on traite un nouvelle article.
  """
  articles_a_traiter = mise_en_forme(pdf, chaine)  #On met en forme les articles à traiter
  nb_article_a_traiter=len(articles_a_traiter)  #ce nombre est utilisé plusieurs fois aussi autant le mémorise dans une variable
  
  for article in articles_a_traiter: #on leur donne un indice
    indice_article(article)
  
  articles_a_traiter_indice = [obtention_indice(articles_a_traiter[i]) for i in range(nb_article_a_traiter)]  #Pour faciliter le traitement on creer la liste des indice des article à traiter (avec lesquels on va travailler)

  Dico_source_article[articles_a_traiter_indice[0]] = [articles_a_traiter_indice[i] for i in range(1, nb_article_a_traiter)]  #on ajoute ce qu'il faut dans dico_production_article
                                                                                                
  ajout={}
  for i in range(1, nb_article_a_traiter):
    ajout[articles_a_traiter_indice[i]] = articles_a_traiter_indice[0]
  ajouter_base_donnees(Dico_production_article, ajout)  #on ajoute ce qu'il faut à Dico_source_article


"""
donnees = open("PROBLEMES DE MODULES FORMELS vsanserreursdecode.txt")
chaine = donnees.read()
pdf = "PROBLEMES DE MODULES FORMELS.pdf"
m = mise_en_forme(pdf, chaine)
print(len(m))

print("\n----\n")
mise_jour_base_de_donnees(pdf, chaine)


print(L_article)
print('\n --------\n')
print("Dico_source_article : ", Dico_source_article)
print('\n --------\n')
print("Dico_production_article : ", Dico_production_article)
print('\n --------\n')
print(obtention_indice(L_article[3]))
"""






#il ne reste plus qu'a faire un grosse boucle avec tout les articles que va traiter notre moteur de recherche avec mise_jour_base_de_donnees
#apres on va pouvoir lancer la categorisation, la suggestion ...
global Graphe_lien #dictionnaire contenant [indice_article]:[article en lien direct] 

Graphe_lien = creation_arbre_des_liens(Dico_source_article, Dico_production_article)

def attribution_point_auteur(indice_article): #non teste
  """
  Cette fonction permet d'attribuer 10 points de ressemblance à un article s'il a au moins un auteur en commun avec l'article de référence.
  """
  graphe_point = {}
  article = L_article[indice_article]
  for el in L_article:
    if not egalite_articles(article, el):
      for a1 in article[1]:
        for a2 in el[1]:
          if egalite_auteursV2(a1, a2):
            graphe_point[obtention_indice(el)] = 10
  return graphe_point


def suggestion_article(indice_article, graphe_lien): #non teste
  """
  Cette fonction prend un article et le graphe des liens et renvoie le 10 articles les plus proches (sans prendre en compte les point attribué pour être du même auteurs)
  """
  graphe_distance = chemin_taille_max_nb_chemin(graphe_lien, indice_article, taille_max=3)
  graphe_points = attribution_point_nb_lien(graphe_distance)
  point_auteur = attribution_point_auteur(indice_article)
  fusion_dico_emplace(graphe_points, point_auteur)
  return selection_articles_pour_suggestion(graphe_points)[:10]  #on retourne les 10 meilleurs articles


def creation_graphe_suggestion(): #non teste
  graphe_suggestion={}
  for indice_article in range(len(L_article)):
    graphe_suggestion[indice_article] = suggestion_article(indice_article, Graphe_lien)
  return graphe_suggestion

#variables globales de exploiter par l'utilisateur
global Graphe_suggestion #dictionnaire contenant pour chaque article la liste de ses suggestions (le graphe ne travaille qu'avec leur indice)
global dico_nature  # Ce dico permet de faire correspondre à chaque article sa nature (reference, novateur)

#initialisation
#Graphe_suggestion = creation_graphe_suggestion()
dico_nature = {}  

def insertion_liste_ordonnee(liste, el):
  """
  Cette procédure sert a insérer un el dans une liste triée
  """
  i = 0
  inf = False
  while i<len(liste) and not inf:
    if el>liste[i]:
      inf = True
    else:
      i+=1
  liste.insert(i,el)

def obtention_seuil_dico_points(nature): #non teste
  dico_point_reference = {}
  l_points_ordonnees = []
  for indice_article in range(len(L_article)):
      if nature == "classique":
          points = points_reference(indice_article, Dico_production_article, L_article)
      else:
          points = novateur(indice_article, Dico_production_article, L_article)
      dico_point_reference[indice_article] = points
      insertion_liste_ordonnee(l_points_ordonnees, points)
  if len(l_points_ordonnees)!=0:
      indice_premier_quartile = int(len(l_points_ordonnees)/4)
      return dico_point_reference, l_points_ordonnees[indice_premier_quartile]+1  #le +1 permet en cas de sujet très récent de ne pas mettre la valeur seuil à 0.
  
  else:  #sinon cela signifie que les scores de tous les articles est de 0 (Il n'a donc pas été calculer)
      return dico_point_reference, 10

def obtention_liste_elements_superieur(dico_points, seuil): 
  """
  Cette fonction permet d'obtenir les articles dont la valeur en points est superieur à un seuil.
  """
  l_article_selectionne = []
  for indice in dico_points.keys():
    if dico_points[indice]>=seuil:
      l_article_selectionne.append(indice)
  return l_article_selectionne

def naturalisation(nature): #non teste   
  """
  Cette procédure permet de completer dico_nature pour la nature rentrée (classique ou novateur)
  Avec ce système un article est soit novateur soit classique.
  """
  dico_points, seuil = obtention_seuil_dico_points(nature)
  l_article_classique = obtention_liste_elements_superieur(dico_points, seuil)
  for indice_article in l_article_classique:
    dico_nature[indice_article] = nature



import os

#remplissage des variables de stockage
adres_calibre = 'D:/Calibre'   #cette adresse devra sans doute être modifier si utilisation sur une autre machine
dossiers = os.listdir(adres_calibre)
i=0
for dossierAuteur in dossiers:
    dossierTitres = os.listdir(adres_calibre+'/'+dossierAuteur)
    #print(dossierTitres)
    for dossierTitre in dossierTitres:
        documents=os.listdir(adres_calibre+'/'+dossierAuteur+'/'+dossierTitre)
        for pdf in documents:
            if pdf[-1]=='f': #pdf
                titreTxt=pdf[:-4]+".txt"
                if titreTxt in documents and titreTxt!="() - ().txt":
                    donnees = open(adres_calibre+'/'+dossierAuteur+'/'+dossierTitre+'/'+titreTxt,"r", encoding='utf-8')
                    chaine=donnees.read()
                    mise_jour_base_de_donnees(adres_calibre+'/'+dossierAuteur+'/'+dossierTitre+'/'+pdf, chaine)
                    donnees.close()
                    i+=1
                    print(i)
            if i>30:  #Pour limiter le temps d'execution
                break
        if i>30:
            break
    if i>30:
        break


print(L_article)
print("\n---------\n")
print(Dico_source_article)
print("\n--------\n")
print(Dico_production_article)
#initialisation des variables de travaille
Graphe_lien = creation_arbre_des_liens(Dico_source_article, Dico_production_article)
Graphe_suggestion = creation_graphe_suggestion()

print("\n-----------\n")
#print(Graphe_suggestion)
print("\n-----------\n")

naturalisation("classique")
naturalisation("novateur") 

print(dico_nature)

"""
import os

#remplissage des variables de stockage
adres_calibre = 'D:/Calibre'
dossiers = os.listdir(adres_calibre)
for dossierAuteur in dossiers:
    dossierTitres = os.listdir(adres_calibre+'/'+dossierAuteur)
    #print(dossierTitres)
    for dossierTitre in dossierTitres:
        documents=os.listdir(adres_calibre+'/'+dossierAuteur+'/'+dossierTitre)
        for pdf in documents:
            if pdf[-1]=='f': #pdf
                titreTxt=pdf[:-4]+".txt"
                if titreTxt in documents and titreTxt!="() - ().txt":
                    donnees = open(adres_calibre+'/'+dossierAuteur+'/'+dossierTitre+'/'+titreTxt,"r", encoding='utf-8')
                    chaine=donnees.read()
                    mise_jour_base_de_donnees(adres_calibre+'/'+dossierAuteur+'/'+dossierTitre+'/'+pdf, chaine)
                    donnees.close()
                    
                    



Graphe_lien = creation_arbre_des_liens(Dico_source_article, Dico_production_article)

Graphe_suggestion = creation_graphe_suggestion()

naturalisation("classique")
naturalisation("novateur") 

"""

def obtention_nature(article):
    """
    Cette fonction permet d'obtenir la nature d'un article. dico_nature ne contient pas tous les articles pour des soucis de place.
    """
    if article not in dico_nature.keys():
        return "sans nature spécifique"
    return dico_nature[article]


###fonction d'encodage sur un fichier txt
def transformation_article_chaine(article):
    """
    Cette fonction permet de transforme un article en une chaine de caractère pour pouvoir le stocker sur un fichier txt
    """
    chaine = article[0] #non article
    chaine+=","+transformation_liste_chaine(article[1], "/") #auteurs
    chaine+=","+str(article[2])
    for i in range(3,6):
        chaine+=","+article[i]
    return chaine

def transformation_liste_chaine(liste, separateur):
    """
    Cette fonction transforme un liste en chaine de caractère.
    """
    chaine = ""
    for el in liste:
        chaine+=str(el)+separateur
    return chaine.rstrip(separateur)

def transforme_liste_article_chaine():
    """
    Cette fonction transforme Liste_article en chaine (sans affecter Liste_article)
    """
    chaine=""
    for article in L_article:
        chaine+=transformation_article_chaine(article)+";"
    return chaine.rstrip(";")
    
def transformation_dico_chaine(dico):
    """
    Cette fonction créer une chaine a partir d'un dico de int.
    """
    chaine = ""
    liste_cle = dico.keys()
    for cle in liste_cle:
        chaine+=str(cle)+":"+transformation_liste_chaine(dico[cle], ".")+";"
    return chaine.rstrip(";")

def transformation_dico_chaine_chaine(dico):
    """
    Cette fonction permet de convertir dico_nature en chaine de caractère.
    """
    chaine=""
    liste_cle = dico.keys()
    for cle in liste_cle:
        chaine+=str(cle)+":"+dico[cle]+";"
    return chaine.rstrip(";")

import io

#donnees="L_article\n"+transforme_liste_article_chaine()+"\nDico_source_article\n"+transformation_dico_chaine(Dico_source_article)+"\nDico_production_article\n"+transformation_dico_chaine(Dico_production_article)+"\nGraphe_lien\n"+transformation_dico_chaine(Graphe_lien)+"\nGraphe_suggestion\n"+transformation_dico_chaine(Graphe_suggestion)+"\ndico_nature\n"+transformation_dico_chaine(dico_nature)
fichier = io.open("donnees_topologie", "w", encoding="utf-8")

#fichier.write(donnees)

fichier.write("L_article\n")
fichier.write(transforme_liste_article_chaine())  #créer un fonction pour transformer une Liste en chaine de caractère
fichier.write("\n")

fichier.write("Dico_source_article\n")
fichier.write(transformation_dico_chaine(Dico_source_article)) #créer une fonction pour transformer un dico en chaine de caractère 
fichier.write("\n")

fichier.write("Dico_production_article\n")
fichier.write(transformation_dico_chaine(Dico_production_article))
fichier.write("\n")

fichier.write("Graphe_lien\n")
fichier.write(transformation_dico_chaine(Graphe_lien))
fichier.write("\n")

fichier.write("Graphe_suggestion\n")
fichier.write(transformation_dico_chaine(Graphe_suggestion))
fichier.write("\n")

fichier.write("dico_nature\n")
fichier.write(transformation_dico_chaine_chaine(dico_nature))
fichier.write("\n") 

fichier.close()