#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math

from predicted import predicted_map
from map_reverse import miRNA_reverse

mirna_target_gene_affinity = {}
target_gene_mirna_affinity = {}

def extract_affinity():
	for mirna in predicted_map.keys():
		mirna_target_gene_affinity[mirna] = []
		for target in predicted_map[mirna].keys():
			# print mirna
			# print target
			# print predicted_map[mirna][target][19]
			del_g_binding = predicted_map[mirna][target][19]
			tup = (target, del_g_binding)
			mirna_target_gene_affinity[mirna].append(tuple(tup))
	# print mirna_target_gene_affinity
	jsonify(mirna_target_gene_affinity, 'mirna_target_gene_affinity.py', 'mirna_target_gene_affinity')

def reverse_map_with_affinity():
	for gene in miRNA_reverse.keys():
		target_gene_mirna_affinity[gene] = []
		mirnas = miRNA_reverse[gene]
		for mirna in mirnas:
			if gene in predicted_map[mirna].keys():
				del_g_binding = predicted_map[mirna][gene][19]
				tup = (mirna, del_g_binding)
				target_gene_mirna_affinity[gene].append(tuple(tup))
	jsonify(target_gene_mirna_affinity, 'target_gene_mirna_affinity.py', 'target_gene_mirna_affinity')


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)

if __name__ == '__main__':
	extract_affinity()
	reverse_map_with_affinity()