#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Jaccard.py
#  
# Author:Raymond Aarseth <raa062@student.uib.no>
# 
#  

#import libraries:
import networkx as nx

def compute_jaccard_index(set_1, set_2):
	""" #computes the jaccard-score of two nodes.
		#arg1: list of nodes connected to node1
		#arg2: list of nodes connected to node2
		#Return: the jaccard-score of 
	"""
	n = len(set_1.intersection(set_2))
	return n / float(len(set_1) + len(set_2) - n) 

def finn_nabo(g,navn):
	""" #Finds all neighbours of a node
		#arg1: a graph
		#arg2: name of a node to find neighbours of
		#Return: a set of neighbours.
	"""
	nb = g[navn]
	naboer= []
	for i in nb:
		naboer.append(i)
		
	return set(naboer)
		
def jaccard(g,d1,d2)	:
	""" #finds the Jaccard-score of all neighbours of a node (in this case ylvis)
		#arg1: a dictionary to lookup names
		#arg2: a dictionary to lookup titles
		#Return: nothing. Prints the jaccard-scores.
	"""
	ylvis = "jofNR_WkoCE"
	naboer =finn_nabo(g,ylvis)
	jaccard = 0.0
	hi=""
	nr = 0.0
	for nabo in naboer:
		a = compute_jaccard_index(naboer,finn_nabo(g,nabo))
		jaccard += a
		if a > nr:
			nr=a
			hi = str(nabo)
			
		print "jaccard-score: " ,a, "for",  d2[str(nabo)][:40]
	jaccard = jaccard / len(naboer)
	
	print "highest jaccard-score: " , d2[hi] ," with ", str(nr)
	print "snitt for jaccard: " , str(jaccard)
	print
	

def fileToList(file):
	""" #creates a list from a file
		#arg1: file to read from
		#Return: a list conatining all the lines in the file
	"""
	liste = []
	
	for line in file:
		liste.append(line[:-2])
		
	return liste
	
def todic(liste1,liste2):
	""" #Creates a lookup dictionary from to lists.
		#arg1: list to add
		#arg2: list to add
		#Return: two lookup dictionaries
	"""
	dic = {}
	dic2  = {}
	for i in range(len(liste1)):
		dic[liste1[i]]=liste2[i]
		dic2[liste2[i]]=liste1[i]
	return dic,dic2
	
def main():
	titles = open("fox titles.txt")
	titles = fileToList(titles)
	names = open("fox vertex.txt")
	names = fileToList(names)
	d1,d2 = todic(titles,names)	
	
	ylvis = "jofNR_WkoCE"
	g = nx.Graph()
	g =nx.read_graphml("foxsay.graphml")
	
	outdeg =g.degree()
	rm = [n for n in outdeg if outdeg[n] ==0]
	
	g.remove_nodes_from(rm)
	
	jaccard(g,d1,d2)
	print compute_jaccard_index(finn_nabo(g,"xO_a7OKmh7Q"),finn_nabo(g,"xiKiAlv9wWw"))
	q = nx.cliques_containing_node(g,ylvis)
	
	
	print "cliques containing the fox: "
	d2["jofNR_WkoCE"]= "ylvis original fox -tvn"
	for clique in q:
		print len(clique)
		for node in clique:
			print d2[str(node)[:40]]
		print "\n"
	

	return 0

if __name__ == '__main__':
	main()

