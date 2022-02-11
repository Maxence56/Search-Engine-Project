# -*- coding: utf-8 -*-
"""
Projet codev créer par 

Maxence ELFATIHI
Adrien GIRARD
Charles-Alexandre MATYJASIK 
Marc SERRE

Ce module sert à extraitre les meta_donnees du pdf.
"""

import PyPDF2

def obtention_metadonnees(pdf):
    """
    ce programme récupère les metadonnees.
    """
    reader = PyPDF2.PdfFileReader(open(pdf, 'rb'))
    metadonnees = reader.getDocumentInfo()
    return metadonnees

def traitement_meta(meta):
    """
    Cette fonction extrait les informations utiles et les met au format voulu
    meta est le résultat de obtention_metadonnees.
    """
    titre=meta['/Title']
    auteurs=meta['/Author'].split(",")
    date=meta['/CreationDate']
    date=int(date[2:6])
    return [titre, auteurs, date,"","",""]