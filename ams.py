# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE


"""

import urllib.request
import unidecode

from telechargement import recuphtml

def create_link(reference):
  """
  Cette fonction permet a partir de la reference d'obtenir le lien en partant de la reference.
  """
  debut='https://mathscinet.ams.org/mathscinet-mref?ref='
  fin='+&mref-submit=Search&dataType=bibtex'
  def milieu(ref):
    """
    Cette fonction convertie la référence en caractère_lien. Elle permet d'obtenir le mileu du lien. 
    """
    st=''
    for i in ref:
      if i==' ':
        st+='+'
      elif i==',':
        st+='%2C'
      elif i=='(':
        st+='%28'
      elif i==')':
        st+='%29'
      elif i=='é':
        st+='%C3%A9'
      elif i=='è' or i=='ë' or i=='ö' or i=='ü' or i=='ï' or i=='ä' or i=='ç' or i=='à' or i=='ù'or i=='â'or i=='î'or i=='ê'or i=='ô'or i=='û' :
        st+='�'
      else:
        st+=i
    return st
  return debut+milieu(reference)+fin
def notfound(data):
  nf='No Unique Match Found'
  return nf in data

def supprSpecChar(a):
  #supprime les caractères spéciaux
  b = """!@#{}\\'"$"""
  for char in b:
    a = a.replace(char,"")
  return a

def ams(reference):
    link=create_link(reference)
    #print(link)
    data=recuphtml(link)
    chaine="""<td align="left"><pre>@"""
    chaine2 = '</pre></td></tr>'
    data=data.decode('latin-1')
    if notfound(data):
      print('not found')
      return 0 #un truc approximatif
    else:
      #Recupere les données sur le site l'American Mathematical Society
      #print('ams')
      k=data.find(chaine)
      l=data.find(chaine2)
      data=data[k+len(chaine):l]
      #print(data)
    return structuration(data)

def structuration(data):
  resul=[]
  def addType(data,r):
    i=data.find('{')
    return data[:i-1]
  def addStuff(data,ch):
    ch2="},"
    if ch in data:
      i=data.find(ch)
      data2=data[i:]
      i2=data2.find(ch2)
      l=len(ch)
      return(data2[l:i2])
    else:
      return ""

  aut=[addStuff(data,"AUTHOR = {")]
  titre=supprSpecChar(addStuff(data,"TITLE = {"))
  date=int(addStuff(data,"YEAR = {"))
  ouvrage=addStuff(data,"JOURNAL = {")
  isbn=addStuff(data,"ISSN = {")+addStuff(data,"ISBN = {")
  url=addStuff(data,"URL = {")
  return [titre,aut,date,ouvrage,isbn,url]