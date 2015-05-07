#!/usr/bin/env/python -W ignore::VisibleDeprecationWarning

import networkx as nx
import matplotlib.pyplot as plt
import pylab
from mirna_map_dict import mirna_map_dict
from target_gene_map_dict import target_gene_map_dict
import itertools

def call(mi):
	for i in target_gene_map_dict:
		print(i)
		print(type(target_gene_map_dict[x]))
		if mi in target_gene_map_dict[x]:
			print(mi)
			# return (True, i)

# if __name__ == '__main__':
# 	flag = False
# 	print(len(target_gene_map_dict))
# 	g = nx.Graph()
# 	g.add_nodes_from(mirna_map_dict.keys(), color = 'red')
# 	print(g.nodes())
# 	print(g.order())
# 	g.add_nodes_from(target_gene_map_dict.keys(), color = 'blue')
# 	print(g.nodes())
# 	print(g.order())
# 	for x in mirna_map_dict.keys():
# 		targets = len(mirna_map_dict[x])
# 		g.add_nodes_from()
# 		break

def remove_duplicates(viruses):
	output = []
	visited = set()
	for virus in viruses:
		if virus not in visited:
			output.append(virus)
			visited.add(virus)
	return output

if __name__ == '__main__':
	genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
	mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
	gene_list = remove_duplicates(genes)
	mirna_list = remove_duplicates(mirna)

	g = nx.Graph()
	# Target genes - x, get red color
	# miRNA - y, get blue color
	g.add_nodes_from(gene_list[:20], bipartite=0)
	nx.draw_random(g, node_color='red')
	g.add_nodes_from(mirna_list[:20], bipartite=1)
	nx.draw_random(g, node_color='blue')
	print(g.order())	# gives the number of nodes in the graph
	for x,y in itertools.izip_longest(genes, mirna):
		g.add_edge(x, y)
		if g.size() == 20:
			break
	print(g.size()) # gives the number of edges
	# _xlim = plt.gca().get_xlim()
	# _ylim = plt.gca().get_ylim()
	# print(_xlim)
	# print(_ylim)
	nx.draw_random(g)
	plt.show()

# G = nx.star_graph(targets)
# pos = nx.spring_layout(G)
# colors = range(targets)
# nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors, width=4, edge_cmap=plt.cm.Reds, with_labels=False)
# plt.savefig('edge_colormap.png')
# plt.show()