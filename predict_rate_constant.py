#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math

from predicted import predicted_map
from mirna_host_gene_map_with_transcript_count import mirna_host_gene_map_with_transcript_count


def find_k_equivalent():
	mirna_host_target_gene_expression = {}
	for mirna in predicted_map.keys():
		mirna_host_target_gene_expression[mirna] = {}
		for targets in predicted_map[mirna].keys():
			# print mirna
			# print targets
			# print predicted_map[mirna][targets][19]
			del_g_binding = predicted_map[mirna][targets][19]
			# Gibbs Free Energy equation at R = 0.008314 kJ/(mol.K) and T = 298 K
			keq = float(math.exp(-1 * del_g_binding/(0.008314 * 298)))
			# print del_g_binding
			# print keq
			predicted_map[mirna][targets].append(keq)
			# predicted_map[mirna][targets].append(0)	# Putting mmi = 0 by default for each mirna-target gene combination so that each list has same structure.
			# print predicted_map[mirna][targets]
			if mirna in mirna_host_gene_map_with_transcript_count.keys():
				m = find_target_gene_expression(targets)
				if "miRNA Transcript Count" in mirna_host_gene_map_with_transcript_count[mirna].keys():
					mirna_host_target_gene_expression[mirna]["miRNA Transcript Count"] = float(mirna_host_gene_map_with_transcript_count[mirna]["miRNA Transcript Count"])
				mirna_host_target_gene_expression[mirna]["Target Gene"] = targets
				mirna_host_target_gene_expression[mirna]["Target Gene Transcript Count"] = m
				mirna_host_target_gene_expression[mirna]["Host Gene"] = ''
				mirna_host_target_gene_expression[mirna]["Host Gene Transcript Count"] = float(0.0)
				if "Host Gene" in mirna_host_gene_map_with_transcript_count[mirna].keys():
					# print mirna, targets
					# print mirna_host_gene_map_with_transcript_count[mirna]["Host Gene"]
					# raw_input('Enter')
					m = find_target_gene_expression(targets)
					mi = float(mirna_host_gene_map_with_transcript_count[mirna]["Host Gene Transcript Count"])
					
					# if m == None or mi == None or keq == None:
					# 	pass
					# Uses host gene transcript count for mirna conc, target gene transcript count for mRNA conc
					mmi = keq * m * mi
					# print m, mi, mmi
					# raw_input('Enter')
					mirna_host_target_gene_expression[mirna]["Host Gene"] = mirna_host_gene_map_with_transcript_count[mirna]["Host Gene"]
					mirna_host_target_gene_expression[mirna]["Host Gene Transcript Count"] = mi

					predicted_map[mirna][targets].append(mmi)
			# jsonify(predicted_map, 'predicted_with_keq_mmi_exp.py', 'predicted_map_with_keq_mmi_exp')
			jsonify(mirna_host_target_gene_expression, 'mirna_host_target_gene_expression.py', 'mirna_host_target_gene_expression')


def find_target_gene_expression(target_gene):
	# print target_gene
	with open('./data_used_for_mapping/gene_coordinates_from_ensembl.tsv', 'r') as gene_file:
		gene_data = csv.reader(gene_file, dialect = 'excel-tab', skipinitialspace = True)
		next(gene_data, None)
		for each_line in gene_data:
			if str(each_line[4]) == str(target_gene):
				value = float(each_line[5])
				gene_file.seek(0)
				return value
			else:
				# Also returns 0 for the genes whose transcript count is not known to us
				value = float(0)
		gene_file.seek(0)
		return value


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	find_k_equivalent()