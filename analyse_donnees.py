# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert à analyser les informations de la bibliographie:
    elle transforme une reference biblio en  (titre, liste des auteurs, date, ouvrage, ISBN, url)
"""

from extraction_bibliographie import *  #permet l'importation de traitement_chaineV2 avec.

Liste_separateur=[",",";"]  #si on tombe sur un auteur qui utilise les : comme séparateur on lui fait un procès car ça pourri les titres avec des : et les URLs.

def decoupage(chaine):
  """
  Cette fonction permet de découper chaque bloc de texte de ref bibliographique en une liste de chaine contenant chaque information du bloc.
  Cela permet de les traiter.
  """
  liste1=chaine.split(Liste_separateur[0])
  liste2=[]
  for el in liste1:
    liste2+=el.split(Liste_separateur[1])
  return liste2

#identification des elements des bibliographies
#liste correspond au résultat de decoupage(chaine)

def est_ce_une_edition(el):
  """
  Cette fonction permet de vérifier que la plus longue chaine n'est pas une édition. 
  Elle renvoie True si le mot edition est trouvé.
  """
  l = el.split()
  for mot in l:
    if motSimilaire("edition", mot[:7], deux_a_traiter=False, accent=True):
      return True
  return False

def obtention_nom_article(liste):
  """
  Cette fonction permet de repérer le titre de l'article.
  Elle s'appuie sur le principe empirique que le nom de l'article est la plus longue chaine du bloc de la ref bibliographique.
  """
  try:  #le indice est normalement toujours existant mais il ne faut surtout pas que notre programme plante.
      el=""
      for i in range(len(liste)):
          if len(liste[i])>len(el) and not("http"in liste[i]) and not est_ce_une_edition(liste[i]):
              el=liste[i]
              indice=i
      return el,indice  
  except:
      return "",0



def extraction_nombre(chaine):
    """
    Cette fonction extrait tous les nombres d'une chaine de caractère.
    Elle renvoie la liste des nombre sous format str.
    """
    l_chiffres=[str(k) for k in range(10)] #liste des chiffres sous format str
    L_nombres=[]
    i=0
    while i<len(chaine):
        if chaine[i] in l_chiffres:
            L_nombres.append(chaine[i])
            i+=1
            while i<len(chaine) and chaine[i] in l_chiffres:
                L_nombres[-1]+= chaine[i]
                i+=1
        i+=1
    return L_nombres

def extraction_dateV2(L_nombres):
  """
  Cette fonction sert à extraire l'année (potentielle) de cette liste de nombre.
  S'il n'y a pas de nombre pouvant correspondre à l'année,
  elle renvoie un 0 de manière en renvoie une information qui permettent le bon fonctionnent de obtention_dateV2.
  L_nombre est une liste de nombre EN Chaine de caractères
  """
  for el in L_nombres:
    if len(el)!=4:
      L_nombres.remove(el)
  if len(L_nombres)==1:
    return L_nombres[0]
  return 0  #si il contient plusieurs nombre de 4 chiffre ca ne doit pas être la date mais des numéro de page aussi autant ne rien renvoyer. 

def obtention_dateV2(liste, annee_max=2050, annee_min=1700):
  """
  Cette fonction permet d'obtenir la date de l'article.
  Elle s'appuie sur l'idée que la date soit le nombre le plus élévé qu'on puisse récupérer inférieur à 2050 (ou l'année en cours)
  """
  l=[extraction_dateV2(extraction_nombre(chaine)) for chaine in liste]
  l_int=[int(i) for i in l]
  for i in range(len(l_int)):  #On ne peut pas faire <<for date in l_int>> car date est une autre variable que l_int[i]
    if l_int[i]> annee_max:
      l_int[i] = 0
    if l_int[i]<annee_min:
      l_int[i] = 0
  date_max=max(l_int)
  index_date_max=l_int.index(date_max)
  return date_max,index_date_max



###fonction permettant de faire fonctionner obtention_auteur
def sum_string(liste):
  """
  Cette fonction prend une liste de chaine de caractère et renvoie une chaine avec un espace entre chaque element de la liste.
  """
  if liste==[]:
      return ""
  
  somme=liste[0]
  for j in range(1,len(liste)):
    somme+=" "+liste[j]
  return somme

def separateur_esperluette(liste_debut):
    """
    Cette fonction sert à traiter le cas où deux auteurs sont séparé par un esperluette (Max : je savais meme pas que ce mot existait) et non par une virgule.
    Elle prend en paramètre la partie de la liste contenant les auteurs et extraie les noms deux auteurs séparé par l'esperluette.
    C'est une procédure elle modifie directement liste_début.
    """
    if liste_debut!=[]:
      dernier_elmt=liste_debut[-1]  # On ne s'occupe que du dernier element car le symbole esperluette ne separera que les deux derniers auteurs de la liste.
      if '&' in dernier_elmt:
        liste_debut.pop(-1)
        i=dernier_elmt.index('&')
        dernier_auteur=dernier_elmt[i+2:]
        penultieme_auteur=dernier_elmt[:i-1]
        liste_debut.append(penultieme_auteur)
        liste_debut.append(dernier_auteur)

def suppression_crochets(liste_debut):
    """
    Cette procédure permet de supprimer d'eventuelles crochets et leur contenu (un numero souvent) devant le nom d'un auteur.
    """
    if liste_debut!=[]:
      prem=liste_debut[0]
      i=0
      if '[' in prem:
        while prem[0]!=']':
          prem=prem[1:]
        prem=prem[1:]
        liste_debut[0]=prem

def suppression_chaine_interdite(liste_debut,chaine="et"):
    """
    Cette procédure joue le même rôle que separateur_esperluette mais avec n'importe quelle chaine de caractère (par défaut 'et').
    """
    if liste_debut!=[]:
      for el in liste_debut:
        el_split=el.split()
        if chaine in el_split:
          i=el_split.index(chaine)
          debut,fin=el_split[:i],el_split[i+1:]
          del liste_debut[liste_debut.index(el)]
          debut_str=sum_string(debut)   
          fin_str=sum_string(fin)
          liste_debut.append(debut_str)
          liste_debut.append(fin_str)

def enlever_les_M(liste_debut):
  l_chaine_a_enlever=["Mme", "M.", "Mme.", "Monsieur", "Madame", "Messieurs", "Mesdames", "MM", "mm", "MM.", "mm."]
  for i in range(len(liste_debut)):
    el = liste_debut[i]
    mots = el.split()
    if len(mots)!=0 and mots[0] in l_chaine_a_enlever:
      mots.remove(mots[0])
      nouv_el = sum_string(mots)
      liste_debut[i] = nouv_el

###fin fonctions intermédiaire
def obtention_auteur(liste, indice_titre,indice_date):
  """
  Cette fonction permet d'obtenir le nom des auteurs. Elle utilise le principe empirique que les noms des auteurs soit avant le nom de l'article.
  Indice rentré en argument correspond à l'indice du titre de l'article.
  """
  indice=min(indice_titre,indice_date)
  liste_debut=liste[:indice]
  separateur_esperluette(liste_debut)
  suppression_crochets(liste_debut)
  suppression_chaine_interdite(liste_debut,"et")
  suppression_chaine_interdite(liste_debut,"avec")
  enlever_les_M(liste_debut)
  return liste_debut


def extraction_ISBN(liste):
  """
  Cette fonction prend une liste contenant les informations d'une ref bibliographique et renvoie un ISBN et son indice s'il y en a un 
  et une chaine de caractère vide et 0 sinon.
  """
  for i in range(len(liste)):
    if "978-"in liste[i] or "979-"in liste[i]:
      return liste[i],i
  return "",0 

def extraction_url(liste):
  """
  Cette fonction fait la même chose que extraction_ISBN mais avec les URLs.
  """
  for i in range(len(liste)):
    if "http"in liste[i] or "www."in liste[i]:
      return liste[i],i
  return "",0

def auteur_est_journal(auteurs):
  journaux=["Le Monde","Le Figaro","Libération","Combat nature","Les Echos","L'Humanité","Le Parisien","La Tribune","Dépêche du Midi","La Dépêche du Midi","La Charente Libre"]
  return auteurs!=[] and (auteurs[0] in journaux)

def nom_avt_prenom(auteur):
  if len(auteur)>=1 and auteur[0]==" ":
    auteur=auteur[1:]
  if len(auteur)>=2:
    if "." in auteur:
      if auteur[-1]==".":
        pass
      elif auteur[2]==" "and auteur[1]==".":
        auteur= auteur[3:]+" "+auteur[:2]
  return auteur

def protocole_droit(liste_chaine):
  auteurs=liste_chaine[2]
  auteurs=nom_avt_prenom(auteurs)
  ouvrage=liste_chaine[0]+liste_chaine[1]
  i=0
  l=len(liste_chaine)
  flag=False
  res=""
  while i<l and liste_chaine[i][-1]!='»' :
    if liste_chaine[i][0]=='«' or liste_chaine[i][1]=='«':
      flag=True
    if flag:
      res+=liste_chaine[i]
    i+=1
  res+=liste_chaine[i]
  return [auteurs],res, ouvrage


def recombinaison_nom_prenom(auteurs):
  l=len(auteurs)
  initiales=[len(chaine)<7 and len(chaine)>0 and chaine[-1]=="."for chaine in auteurs]
  caps=[chaine==chaine.upper() for chaine in auteurs]
  res=[]
  if caps[0]:
    for i in range(l):
      if caps[i]:
        res.append(auteurs[i])
        i+=1
        while i<l-1 and (not caps[i] or initiales[i]):
          res[-1]=sum_string([res[-1],auteurs[i]])
          i+=1
  else:
    for i in range(l):
      if not caps[i]:
        res.append(auteurs[i])
        i+=1
        while i<l and initiales[i]:
          res[-1]=sum_string([res[-1],auteurs[i]])
          i+=1
  return res

def correction_style1(titre,auteurs):
    title=titre
    aut=auteurs
    if titre[2]==".":
      if titre[3]==" ":
        aut.append(titre[:3])
        title=titre[12:]
    if titre[5]==".":
      if titre[6]==" ":
        aut.append(titre[4:6])
        title=titre[15:]
    return title,aut

def procesus_complet(chaine):
  """
  retourne un article sous forme (titre, liste des auteurs, date, ouvrage, ISBN, url), respectivement, string,string list,integer,string,string,string
  """
  liste_chaine_decoupee=decoupage(chaine)
  date,indice_date=obtention_dateV2(liste_chaine_decoupee, annee_max=2050)
  titre,indice_titre=obtention_nom_article(liste_chaine_decoupee)
  auteurs = obtention_auteur(liste_chaine_decoupee, indice_titre,indice_date)
  url=extraction_url(liste_chaine_decoupee)[0]
  ISBN=extraction_ISBN(liste_chaine_decoupee)[0]
  ouvrage=''
  if len(titre)<=5:
    return ()
  if auteurs==[] and date==0 :
    return ()
  if auteur_est_journal(auteurs):
    auteurs,titre,ouvrage=protocole_droit(liste_chaine_decoupee)
  for a in auteurs:
    a=nom_avt_prenom(a)
  titre,auteurs=correction_style1(titre,auteurs)
  if auteurs!=[]:
    auteurs=recombinaison_nom_prenom(auteurs)
  return titre,auteurs, date, ouvrage,ISBN, url