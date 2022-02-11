# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert de bibliothèque pour tester l'égalité entre deux articles.
"""

from traitement_chaineV2 import normalisation

def normalisation_auteur(mot, accent=False):
    """
    Cette fonction normalise un mot (enlève la ponctuation à la fin, met tout en minuscule).
    Par défaut elle laisse les accents intacts mais elle peut les supprimé si demandé.
    """
    #traitement ponctuation
    ponctuation=[",",";",".","?","!",":",")"]
    for el in ponctuation:
        mot=mot.rstrip(el)
        
    #traitement majuscule
    L_majuscule=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    dico_lettre={"A":"a","B":"b","C":"c","D":"d","E":"e","F":"f","G":"g","H":"h","I":"i","J":"j","K":"k","L":"l","M":"m","N":"n","O":"o","P":"p","Q":"q","R":"r","S":"s","T":"t","U":"u","V":"v","W":"w","X":"x","Y":"y","Z":"z"}
    
    for i in range(len(mot)):
        if mot[i] in L_majuscule:
            mot=mot[:i]+dico_lettre[mot[i]]+mot[i+1:] 
    
    #traitement accent
    if accent:
        L_accent=["â","ê","î","ô","û","ä","ë","ï","ö","ü","ÿ","é","è","à","ù"]
        dico_accent={"ê":"e","ë":"e","é":"e","è":"e","â":"a","ä":"a","à":"a","ü":"u","û":"u","ù":"u","ï":"i","î":"i","ö":"o","ô":"o","ÿ":"y"}
        
        for i in range(len(mot)):
            if mot[i] in L_accent:
                mot=mot[:i]+dico_accent[mot[i]]+mot[i+1:]
    
    return mot #le return est necesssaire.

def egalite_auteursV2(a1,a2):
  """
  Cette fonction permet de comparer deux auteurs.
  Elle part du principe que le nom sera avant le prenom.
  Elle ne compare pas les prenoms
  """
  b1,b2=normalisation_auteur(a1),normalisation_auteur(a2) #preparation
  l1,l2=b1.split(),b2.split()

  if len(l1)==len(l2): 
    if len(l1)>1: # on peut dans ce cas supposer que les deux contiennent le prénom
      p1 = l1.pop() # dans ce cas on l'enlève car on ne peut pas le normaliser
      p2 = l2.pop()
      return l1==l2 and p1[0]==p2[0] #dans ce cas on en profite pour comparer l'initial du prénom aussi
    return l1==l2

  elif len(l1)>len(l2):
    l1.pop() # ça nous permet de supposer que l1 a le prénom et l2 ne la pas
    return l1==l2

  else: 
    l2.pop()
    return l1==l2

def normalisation_titres(mot, accent=False):
    """
    Cette fonction normalise un mot (enlève la ponctuation à la fin, met tout en minuscule).
    Par défaut elle laisse les accents intacts mais elle peut les supprimé si demandé.
    """
        
    #traitement majuscule
    L_majuscule=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    dico_lettre={"A":"a","B":"b","C":"c","D":"d","E":"e","F":"f","G":"g","H":"h","I":"i","J":"j","K":"k","L":"l","M":"m","N":"n","O":"o","P":"p","Q":"q","R":"r","S":"s","T":"t","U":"u","V":"v","W":"w","X":"x","Y":"y","Z":"z"}
    
    for i in range(len(mot)):
        if mot[i] in L_majuscule:
            mot=mot[:i]+dico_lettre[mot[i]]+mot[i+1:] 
    
    #traitement accent
    if accent:
        L_accent=["â","ê","î","ô","û","ä","ë","ï","ö","ü","ÿ","é","è","à","ù"]
        dico_accent={"ê":"e","ë":"e","é":"e","è":"e","â":"a","ä":"a","à":"a","ü":"u","û":"u","ù":"u","ï":"i","î":"i","ö":"o","ô":"o","ÿ":"y"}

        for i in range(len(mot)):
            if mot[i] in L_accent:
                mot=mot[:i]+dico_accent[mot[i]]+mot[i+1:]
    
    return mot #le return est necesssaire.

def egalite_titres(t1,t2):
  b1,b2=normalisation_titres(t1),normalisation_titres(t2)
  l1,l2=b1.split(),b2.split()
  return l1==l2

def egalite_articles(a1, a2):  #la fonction normalisation doit être importée
  """
  un article sous forme (titre, liste des auteurs, date, ouvrage, ISBN, url)
  Cette fonction retourne True si a1==a2 et False sinon.
  """
  url1, url2 = a1[5], a2[5]
  ISBN1, ISBN2 = a1[4], a2[4]
  if (url1!="" and url1==url2) or (ISBN1==ISBN2 and ISBN1!="" ):
    return True
  titre1, titre2 = a1[0], a2[0]
  titre1 = normalisation(titre1, accent=True)
  titre2 = normalisation(titre2, accent=True)
  longueur_ressemblance = 0
  l1 = len(titre1)
  l2 = len(titre2)
  l_min=min(l1,l2)
  if l1==l_min:
    return comparaison_titre(titre1, titre2)
  else:
    return comparaison_titre(titre2, titre1)


def comparaison_titre(titre_min, titre2,taux_de_ressemblance=.9):
  long_res=-1
  l_min=len(titre_min)
  flag=True
  while flag:
    long_res+=1
    flag=False
    for i in range(l_min-long_res):
      section=titre_min[i:i+long_res]
      if section in titre2:
        flag=True
        break
  if l_min!=0:
      return (long_res / l_min)>taux_de_ressemblance
  else:
      return False
