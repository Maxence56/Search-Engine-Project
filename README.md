# Search-Engine-Project

## Contexte 

De plus en plus de sites webs intègrent un moteur de recherche pour accéder rapidement au contenu qu’ils fournissent. Cet outil devient indispensable dès lors que le nombre de pages mises à disposition devient conséquent et que la recherche dans un sommaire s'avère fastidieuse. Les articles scientifiques sont aujourd’hui très nombreux et dispersés sur de nombreux sites et revues scientifiques disponibles sur le web.

## Projet

J’ai proposé et participé avec trois camarades à la réalisation d’un petit moteur de recherche d’articles scientifiques qui implémente quelques fonctionnalités pratiques absentes sur certains moteurs de recherches connues comme HAL. Le moteur de recherche peut recommander des articles en s’appuyant sur ceux consultés précédemment et identifier certains articles classiques ou novateurs. Ces fonctionnalités s’appuient sur l’extraction et le traitement de la bibliographie présente sur chaque article. Ce projet a été réalisé entièrement en langage Python.

Ce projet constitue une preuve de concept initialement réalisé sur Google Colab et s'appuyant pour les tests sur des articles présents sur le moteur de recherche HAL  


## Utilisation des scripts

Se référer aux commentaires présents sur les fichiers pour comprendre leur fonctionnement  

### Telechargement des fichiers pdf : fichier download.py 

Il faut exécuter la fonction extractall avec comme arguments un répertoire pour sauvegarder les fichiers pdf et un lien de résultats de recherche HAL.
La conversion en fichiers texte des fichiers pdf se fait manuellement en utilisant le logiciel Calibre.


### Moteur de recherche : fichier search_engine.py

D’abord, il faut créer le fichier contenant les données à exploiter en utilisant la fonction extractall qui prend en arguments une liste de liens de résultats de recherche HAL et un répertoire pour sauvegarder les données.

Ensuite, utiliser la fonction search qui prend comme arguments la requête et le répertoire où se trouvent les données.


### Fonctionnalité catégorisation et recommandation : programme_general.py recuperation.py

Ce module utilise de nombreuses bibliothèques que nous avons développées pour le faire fonctionner. Comme l’utilisateur n’a pas à les manipuler, nous n'appliquerons pas leur fonctionnement ici.

Il permet de créer les listes d’articles, pour avoir accès aux articles à partir de son identifiant, Le dictionnaire des articles qui sont cités par la clé, celui des articles qui citent la clé., le graphe des liens entre les articles, le dictionnaire des suggestions et le dictionnaire de la nature des articles.

Il permet aussi de sauvegarder ces données dans un fichier txt pour ne pas avoir à refaire les calculs.

Pour fonctionner, il y a deux possibilités : on crée un nouveau fichier qui importe le programme général où on écrit le script directement dans le programme général.

Le script doit appliquer à chaque article la procédure mise_jour_base_de_donnees(). Après cette opération qui a permis de créer les 3 premières variables. Il doit être écrit avant les lignes :

Graphe_lien = creation_arbre_des_liens(Dico_source_article, Dico_production_article)
Graphe_suggestion = creation_graphe_suggestion()
naturalisation("classique")
naturalisation("novateur") 

Toutes nos variables sont désormais créées. 
Elles s'enregistrent dans un fichier dont le nom par défaut est donnees_topologie. 

Pour récupérer les données enregistrées, on lance simplement le module récupération (avec le bon titre de fichier).
Pour obtenir la nature d’un article utilisé plutôt la fonction obtention_nature(indice_article) que dico_nature car ce dernier ne contient que les articles ayant une nature.
