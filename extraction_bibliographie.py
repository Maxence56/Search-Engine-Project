# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert à extraitre la biblio.
"""

from traitement_chaineV2 import*

def extraction_biblio(chaine):
  """
  Cette fonction prend le document convertie en chaine.
  Et renvoie une Liste contenant les refs bibliographiques séparés par bloc. Un bloc rassemble les informations contenant une ref bibliographique.
  """
  chaine=chaine[len(chaine)//2:]  # On ne s'occupe pas de la première moitié il n'y a pas de biblio dedans.
  L_debut_biblio=["bibliogra","references","sources"]
  biblio=[]
  i=0
  while i<len(L_debut_biblio) and (biblio==[] or biblio==['']):
    donnees=chaineCompriseV2(L_debut_biblio[i],["index","annex"],chaine) #Bibliographie peut se retrouver dans le sommaire. Si on doit traiter le sommaire il faut passer ce mot et dans ce cas utiliser la V3. Le sommaire ne sera pas traiter le V3 est inutile
    donnees=convertir_liste_chaine_en_chaine(donnees)  #les /n disparaissent avec l'utilisation de ces fonctions
    biblio = donnees.split("\n")
    i+=1
  return biblio[1:] # le premier element sera soit "" soit lié au titre biblio  les refs commencant apres un retour à la ligne (peut avoir  un "" à la fin car on termine sans doute par un retour a la ligne sauf si la biblio est en dernier donc il ne faut pas le retirer) #a verifier 


