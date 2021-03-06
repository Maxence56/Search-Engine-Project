# -*- coding: utf-8 -*-
"""Download final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1znnj2mtdY8PQY9l7NXMeP8QQX2bs4YHI
"""

# -*- coding: utf-8 -*-
"""download.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1V771Rz5l4iFR17ZBVbuyDdy2hOtCgpfs
"""

import urllib.request

#page resultats bourbaki
lelien="https://hal.archives-ouvertes.fr/search/index/?q=bourbaki&docType_s=OUV+OR+ART+OR+LECTURE+OR+THESE+OR+COMM+OR+COUV+OR+REPORT&rows=100"

def recuphtml(link) : 
  #retourne le code source d'un URL
  # open a connection to a URL using urllib
  webUrl  = urllib.request.urlopen(link)
  # class="media-body"
  data = webUrl.read()
  return data

def recupid (data) :
  # retourne une liste d'ids d'articles à partir du code source de la page de recherche Hal
  data=data.decode('utf-8')
  chaine = 'class="ref-halid">'
  lon = len(chaine)
  liste = data.split()
  results = []
  for element in liste :
    if chaine in element :
      ind = element.index('<')
      results.append(element[lon:ind]+element[ind+7:ind+9])
  return results



def getlink(ids):
  #retourne une liste de liens à telecharger pour récuperer les articles à partir d'une liste d'ids
  links = []
  for k in ids :
    links = links + ["https://hal.archives-ouvertes.fr/"+k+"/document"]
  return ids,links
#on utilisera plus tard ces fonctions pour le moteur de recherche
"""def keywords(id):
    # ecrit dans un fichier du nom keyword id_du_doc les mots clés avec entre eux des espaces
    chaine='btn-xs">'
    chaine2 = '</a>'
    data = recuphtml("https://hal.archives-ouvertes.fr/"+id)
    data=data.decode('utf-8')
    liste=data.split()
    kw=[]
    for k in range(len(liste)):
        if chaine in liste[k]:
            if chaine2 in liste[k]:
                kw.append(liste[k][8:-4])
            else :
                kw.append(liste[k][8:])
                k+=1
                while chaine2 not in liste[k]:
                    kw.append(liste[k])
                    k+=1
                kw.append(liste[k][:-4])
    if len(kw) == 0 :
        return
    f = open('/home/lapis/Desktop/codevdownloads/'+'keyword '+id+'.txt','w')
    
    for k in kw[:-2] :
        f.write(k+" ")
    
    f.write(kw[len(kw)-1])
    f.close()
    return 'keywords '+id

def abstract(id):
    #Ecrit dans un fichier du nom abstract id_du_doc le contenu des abstracts d'un article: Sur certains articles, on retrouve des fois plusieurs abstracts ecrits dans des langues differentes
    chaine=""abstract-content">""
    chaine2 = '</div>'
    data = recuphtml("https://hal.archives-ouvertes.fr/"+id)
    data=data.decode('utf-8')
    liste=data.split()
    ab=[]
    for k in range (len(liste)):
        if chaine in liste[k]:
            k+=1
            while ':' not in liste[k]:
                k+=1
            while chaine2 not in liste[k]:
                ab.append(liste[k])
                k+=1
    if len(ab) == 0 :
        return
    f = open('/home/lapis/Desktop/codevdownloads/'+'abstract '+id+'.txt','w')                
    ab = [k for k in ab[1:] ] 
    for k in ab :
        f.write(k +' ')
    f.close()
      
    return 'abstract '+id
    
    """

def download(info):
  #telecharge les articles à partir de la liste des liens sur un répertoire 
  ids,links = info
  i=0
  for link in links:
    try:
        urllib.request.urlretrieve(link, '/home/lapis/Desktop/codevdownloads/'+ids[i]+'.pdf')
        print(i,"th file downloaded")
    except:
        print("Oops!")
    i+=1
  
  print("All PDF files downloaded")
#fonction qui fait appel à tout ce qu'il y a au dessus pour telecharger les fichiers à partir du lien
def extractall(link):
    ids = recupid(recuphtml(link))
    download(getlink(ids))