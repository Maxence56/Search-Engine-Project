# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 21:31:30 2021

@author: marc2
"""

import matplotlib.pyplot as plt
import networkx as nx
import random as rd

def tri_par_arrite(dico):
  L=[]
  for el in dico:
    L.append((len(dico[el]),el))
  L.sort()
  L_prime=[e[1] for e in L]
  for i in range(len(L_prime)):
    L_prime[i]=[L_prime[i],(rd.uniform(-i,i),rd.uniform(-i,i))]
  return L_prime

dico={1: [2, 3, 4], 2: [1,3,4],3:[1,2,4], 4:[1,2,3,5], 5:[4,6,7],6: [7,5], 7:[5,6]}
print(tri_par_arrite(dico))

def creation_graphe(dico):
  G = nx.Graph()
  K = dico.keys()
  n = len(dico)
  for i in dico:
    G.add_node(i)
  for i in dico:
    for j in dico[i]:
      if j in K:
        G.add_edge(i,j)
  print(G.edges)
  return G

G = creation_graphe(dico)
options = {
      'node_color' : 'yellow',
      'node_size'  : 550,
      'edge_color' : 'tab:grey',
      'with_labels': True
    }
plt.figure()
nx.draw(G,**options)
plt.show()

from networkx.algorithms import community
partition = community.greedy_modularity_communities(G)
print(len(partition))

couleurs_num = [0] *G.number_of_nodes()
print(couleurs_num)

for i in range(len(partition)):
  for j in partition[i]:
    couleurs_num[j-1] = i
print(couleurs_num)

options = {
      'cmap'       : plt.get_cmap('jet'), 
      'node_color' : couleurs_num,
      'node_size'  : 550,
      'edge_color' : 'tab:grey',
      'with_labels': True
    }
plt.figure()
nx.draw(G,**options)
plt.show()

def randdict():
  N=100
  c_min=5
  c_max=10
  d={}
  for i in range(1,N+1):
    a=rd.randint(c_min,c_max)
    def randlist(a):
      L=[]
      for j in range(a):
        L.append(rd.randint(1,N+1))
      return L
    L=randlist(a)
    d[i]=L
  return d

d=randdict()

G=creation_graphe(d)


partition = community.greedy_modularity_communities(G)
print(len(partition))

couleurs_num = [0] *G.number_of_nodes()
print(couleurs_num)

for i in range(len(partition)):
  for j in partition[i]:
    couleurs_num[j-1] = i
print(couleurs_num)

options = {
      'cmap'       : plt.get_cmap('jet'), 
      'node_color' : couleurs_num,
      'node_size'  : 550,
      'edge_color' : 'tab:grey',
      'with_labels': False
    }
plt.figure()
nx.draw(G,**options)
plt.show()