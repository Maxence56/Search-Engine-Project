# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Cette bibliothèque sert de module pour réaliser toutes les opérations élémentaires sur des chaines de caractères.
"""


def split_espace(chaine): #à refaire
  """
  Cette fonction remplit le rôle de .split() mais en conservant les \n
  """
  liste_inter = chaine.split("\n")
  rliste = liste_inter[0].split()
  for i in range(1, len(liste_inter)):
    rliste+=["\n"]+liste_inter[i].split()
  return rliste

#traitement d'une chaine de caractère
def normalisation(mot, accent=False):
    """
    Cette fonction normalise un mot (enlève la ponctuation à la fin, met tout en minuscule).
    Par défaut elle laisse les accents intacts mais elle peut les supprimer si demandé.
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
      
        dico_accent={"ê":"e","ë":"e","é":"e","è":"e","â":"a","ä":"a","à":"a","ü":"u","û":"u","ù":"u","ï":"i","î":"i","ö":"o","ô":"o","ÿ":"y","É":"e"}
        L_accent = dico_accent.keys()

        for i in range(len(mot)):
            if mot[i] in L_accent:
                mot=mot[:i]+dico_accent[mot[i]]+mot[i+1:]
    
    return mot #le return est necesssaire.

def motSimilaire(mot1, mot2, deux_a_traiter=True, accent=True):
    """
    Cette fonction sert a comparer deux mots malgré la presence de majuscule, de virgule et autres ponctuation, et si on le désire d'accent. Elle renvoie un boolean.
    Par défaut cette fonction épure les deux mots. Pour un gain de temps, il est possible de n'épurer que le second mot. Les accents peuvent ou non être pris en compte. Par défaut il ne sont pas traités marche et marché sont donc considérer comme différent.
    """
    if deux_a_traiter:
        mot1=normalisation(mot1, accent)
    mot2=normalisation(mot2, accent)
    return mot1==mot2
        

def suiteMot(mot, chaine):  #a perfectionnner l'egalite de mot
    """
    Cette fonction sert obtenir les mots qui suivent une un mot, ceux qui suivent le mot bibliographie par exemple.
    """
    Lmot=split_espace(chaine)
    for i in range(len(Lmot)):
        if motSimilaire(mot,Lmot[i],False,True):#pour un gain de temps on suppose que le mot que l'on cherche est normalisé.
            return Lmot[i+1:]
    return []

def chaineComprise(mot1,mot2,chaine):
    """
    Cette fonction permet dans une chaine de selection une liste de mot comprise entre deux "mots" ou symboles. Cela s'arrete après avoir trouvé une chaine correspondante.
    Les bornes sont exclues.
    """
    Lmot=suiteMot(mot1,chaine)  #on selection le debut
    resultat=[]
    i=0
    while i<len(Lmot) and not motSimilaire(mot2, Lmot[i], False):  # on rajoute tant que l'on a pas atteint la fin.
        resultat.append(Lmot[i])
        i=i+1
    return resultat

def convertir_liste_chaine_en_chaine(liste):
    """
    Cette fonction prend une liste de chaine de caractère et renvoie une chaine avec un espace entre chaque element de la liste
    """
    chaine=""
    for el in liste:
        chaine= chaine +" "+el
    return chaine[1:]  #il faut retirer l'espace avant du debut
    

def chainesComprises(mot1,mot2,chaine):  
    """
    Cette fonction permet d'obtenir toutes les listes comprise entre deux "mots" ou symboles et non juste la première.
    Renvoie une liste de liste.
    """
    if suiteMot(mot1,chaine)==[]:  #cela signifie qu'il n'y a plus de chaine a prendre
        return []
    else:
        liste1=chaineComprise(mot1,mot2,chaine) 
        
        #determination de la nouvelle chaine
        chaine_recherche=convertir_liste_chaine_en_chaine(suiteMot(mot1,chaine))  # au cas où il existerai une bornes de fin avant la première bornes de début on s'assure qu'on n'a passer la borne de début
        nouvelle_chaine=convertir_liste_chaine_en_chaine(suiteMot(mot2,chaine_recherche)) #on prend la chaine à partir de la borne de fin
        
        return [liste1]+chainesComprises(mot1,mot2,nouvelle_chaine)

#fonctions à bornes multiples

def suiteMotSyl(debut_mot, chaine):
    """
    Cette fonction sert à obtenir les mots qui suivent un début de mot, ceux qui suivent le debut de mot biblio par exemple.
    la borne est exclue. Fonctionne aussi avec des mots complets.
    """
    Lmot=split_espace(chaine)
    for i in range(len(Lmot)):
        if len(Lmot[i])>=len(debut_mot):
            if motSimilaire(debut_mot,Lmot[i][:len(debut_mot)], False, True):#pour un gain de temps on suppose que le mot que l'on cherche est normalisé.
                return Lmot[i+1:]
    return []

def mot_in_Lmot(mot, liste_mot):
    """
    Cette fonction indique si un début de mot est dans la liste de mot
    True signifie qu'il en fait partie.
    mot doit être normalisé (pour un gain de temps)
    """
    for m in liste_mot:
        if motSimilaire(mot[:len(m)], m, False):
            return True
    return False
    
def chaineCompriseV2(mot1, motsDeFin, chaine, accent=False): #accent = True normalise en supprimant les accents
    """
    cette fonction retourne la chaine comprise entre un debut de mot et plusieurs fins possibles. 
    Elle peut servir pour reperer la zone de la bibliographie dans un document.
    """
    Lmot=suiteMotSyl(mot1, chaine)  #on selection le debut
    resultat=[]
    i=0
    while i<len(Lmot) and not mot_in_Lmot(normalisation(Lmot[i], accent), motsDeFin):  # il faut normalisé le mot pour éviter tout problème 
        resultat.append(Lmot[i])
        i=i+1
    return resultat

def chainesComprisesPlusieursSeparateur(liste_couple_separateur,chaine):
    """
    Cette fonction accomplie la même chose que chainesComprises mais permet de selection plusieurs types possible de séparateurs utile quand on ne sait pas exactement quoi choisir.
    """
    for couple in liste_couple_separateur:
        Lmot=chainesComprises(couple[0],couple[1],chaine)
        if Lmot!=[]:
            return Lmot
    return []

#fonction qui permettent de passer des mots

def suiteMotPasse(debut_mot, chaine, passe=0):
    """ 
    Parameters
    ----------
    debut_mot : TYPE str
        DESCRIPTION. le début de mot qu'on cherche
    chaine : TYPE str
        DESCRIPTION. la chaine où on le cherche
    passe : TYPE int, optional
        DESCRIPTION. The default is 0. le nombre de fois où on le passe.

    Returns str[]
    -------
    TYPE
        DESCRIPTION.
        
    Cette fonction est une version améliorer de suiteMotSyl qui permet de passer les premier mot dans le texte si ils sont non intéressants.

    """
    Lmot=split_espace(chaine)
    vu=0 # le nombre de fois où on a déjà passé le mot
    for i in range(len(Lmot)):
        if len(Lmot[i])>=len(debut_mot):
            if motSimilaire(debut_mot,Lmot[i][:len(debut_mot)],False):#pour un gain de temps on suppose que le mot que l'on cherche est normalisé.
                if vu==passe:
                    return Lmot[i+1:]
                else: #le else n'est pas nécessaire à cause du return
                    vu=+1
    return []

def chaineCompriseV3(mot1, motsDeFin, chaine, accent=False, passe=0): #accent = True normalise en supprimant les accents
    """
    Cette fonction retourne la chaine comprise entre un debut de mot et plusieurs fins possibles. 
    Elle peut servir à reperé la zone ou est la bibliographie dans un document.
    
    Version améliorer de V2 qui utilise suiteMotPasse au lieu de SuiteMotSyl ce qui permet de passer un nombre voulu de fois le mot de départ avant de commencer l'extraction de l'information.
    """
    Lmot=suiteMotPasse(mot1, chaine, passe)  #on selection le debut
    resultat=[]
    i=0
    while i<len(Lmot) and not mot_in_Lmot(normalisation(Lmot[i], accent), motsDeFin):  # il faut normalisé le mot pour éviter tout problème 
        resultat.append(Lmot[i])
        i=i+1
    return resultat
