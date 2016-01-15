#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math
import random
import networkx as nx
from networkx.algorithms import bipartite
from networkx.readwrite import json_graph

from miRNA_meta_data import miRNA_meta_data
mirna_dict = {}
gene_lis_for_mirna_subgraph = []

'''
Forms data and subgraph for any miRNA as user input.
'''
def form_data_mirna():
	mirna_lis = random.sample(miRNA_meta_data.keys(), 10)
	loop = int(raw_input('Enter number of miRNAs you wish to choose.\n'))
	for i in xrange(0,loop):
		print mirna_lis
		user_input = str(raw_input('Choose miRNAs from above list.\n'))
		if user_input in mirna_lis:
			if user_input in miRNA_meta_data.keys():
				mirna_dict, gene_lis_for_mirna_subgraph = collect_gene_info(user_input)
		else:
			print "Wrong input. Please enter again"
			exit(0)

	subgraph(mirna_dict, gene_lis_for_mirna_subgraph)


def collect_gene_info(user_input):
	target_gene_lis_for_mirna_subgraph = []
	host_gene_lis_for_mirna_subgraph = []
	mirna_dict[user_input] = {}
	if "Target Gene with Transcript Count" in miRNA_meta_data[user_input].keys():
		target_gene_lis_for_mirna_subgraph = miRNA_meta_data[user_input]["Target Gene with Transcript Count"]
		
	if "Host Gene" in miRNA_meta_data[user_input].keys():
		host_gene_lis_for_mirna_subgraph.append(miRNA_meta_data[user_input]["Host Gene"])

	for each in host_gene_lis_for_mirna_subgraph:
		gene_lis_for_mirna_subgraph.append(each)
	for each in target_gene_lis_for_mirna_subgraph:
		gene_lis_for_mirna_subgraph.append(each[0])

	mirna_dict[user_input]['Target Genes'] = target_gene_lis_for_mirna_subgraph
	mirna_dict[user_input]['Host Genes'] = host_gene_lis_for_mirna_subgraph
	
	# print gene_lis_for_mirna_subgraph
	# print mirna_dict

	return mirna_dict, gene_lis_for_mirna_subgraph

def subgraph(mirna_dict, gene_lis_for_mirna_subgraph):
	G = nx.DiGraph()
	G.add_nodes_from(gene_lis_for_mirna_subgraph)
	G.add_nodes_from(mirna_dict.keys())
	
	for mirna in mirna_dict:
		# G.add_node(mirna)
		for target_gene in mirna_dict[mirna]['Target Genes']:
			G.add_edge(mirna, target_gene[0])
		for host_gene in mirna_dict[mirna]['Host Genes']:
			G.add_edge(host_gene, mirna)
		# g.add_edges_from(mirna, mirna_dict[mirna]['Target Genes'])
		# g.add_edges_from(mirna_dict[mirna]['Host Genes'], mirna)
	nx.write_gexf(G,"subgraph.gexf")
	print 'Done!'


'''
Forms data for any gene as user input.
'''
def form_data_genes(gene_data):
	gene_lis = random.sample(gene_data.keys(), 10)


if __name__ == '__main__':
	form_data_mirna()
	with open('./gene_ID_Store.json', 'r') as infile:
		gene_data = json.loads(infile.read())
		form_data_genes(gene_data)