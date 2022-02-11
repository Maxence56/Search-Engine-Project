# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert à extraitre la création des dictionnaires.
"""

### fonction qui permet la création du dictionnaire dico_source_article
"""
base de donnees 
un dico avec en clé l'indice d'un article et en valeur la liste des indices des article qui le cite
"""
def ajouter_base_donnees(base_donnees,ajout):
  """
  Cette fonction permet d'ajouter un article et les articles cité dans la base de donnees.
  C'est une procédure qui modifie directement base_donnees

  ajout est un dico pour un article
  il est sous la forme {indice_article1 : indice_article_en_cours, indice_article2 : indice_article_en_cours}. Il n'y aura pas de répétition car l'article en cours ne sera traiter qu'une fois.
  """
  L_keys_b=base_donnees.keys()
  L_keys_a=ajout.keys()
  for el in L_keys_a:
    if el in L_keys_b:
      base_donnees[el].append(ajout[el])
    else:
      base_donnees[el]=[ajout[el]]

def creer_base_donnees(premier_article):
  """
  Cette fonction permet de creer une base de données avec le premier article au format {indice_article1 : indice_article_en_cours, indice_article2 : indice_article_en_cours}.
  """
  base_donnees={}
  ajouter_base_donnees(base_donnees,premier_article)
  return base_donnees
###

"""
idée de stockage des donnees:

une liste d'article [article1, article2] qui permet de stocker qu'une fois nos articles. Il faudra après avoir un dico liant l'article à l'indice.  

article=["nom",["auteurs"],annee]

lien entre les articles

{indice_article1 : liste_indice_article_citeurs}


On veut aussi un dico avec en clé un article et en valeur touts les articles en lien c'est à dire ce qui le citent et ceux qu'il cite.

Pour cela on va faire un autre dico [article]--->[articles qu'il cite]. 
Comme la on va rajouter à la nouvelle base de donnees un dico avec en valeurs un article qui n'existait pas dans avant dans la nouvelle base de donnees on peut tout simplement faire nouvelle_base_donnees.update(nouv_article).
Cette procédure sera suffisante.

Puis on va creer un nouveau dico qui sera une fusion de ce deux dicos. (On ne peut pas utiliser update car il y aura de l'écrasement et on n'aura plus acces à certaines donnees)
"""

def super_copy(dico_de_liste):
  """
  Cette fonction permet de faire un deepcopy pour un dictionnaire de list (Pour des raisons inconnues deepcopy() ne fonctionnne pas).
  """
  new_dict = {}
  list_keys = dico_de_liste.keys()
  for keys in list_keys:
    new_dict[keys] = dico_de_liste[keys].copy()
  return new_dict

def creation_arbre_des_liens(dico_source_article, dico_production_article):
  """
  Cette fonction permet de fusionner deux dictionnaires de liste (sans écrasement).
  """
  Liste_cle_source_article = dico_source_article.keys()
  Liste_cle_production_article = dico_production_article.keys()
  arbre_des_liens = super_copy(dico_source_article) #un .copy() ne suffit pas car si l'addresse des dictionnaires sont différentes celle des liste sur lesquelles ils travaillent sont les mêmes donc un .copy() provoquerait quand même des changement sur dico_source_article.
  for cle in Liste_cle_production_article:
    if cle in Liste_cle_source_article:
      arbre_des_liens[cle]+=dico_production_article[cle]
    else:
      arbre_des_liens[cle] = dico_production_article[cle]
  return arbre_des_liens
