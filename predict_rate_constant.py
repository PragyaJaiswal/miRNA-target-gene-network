#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math

from predicted import predicted_map
from mirna_host_gene_map_with_transcript_count import mirna_host_gene_map_with_transcript_count

def find_k_equivalent():
	for mirna in predicted_map.keys():
		for targets in predicted_map[mirna].keys():
			print mirna
			print targets
			# print predicted_map[mirna][targets][19]
			del_g_binding = predicted_map[mirna][targets][19]
			keq = float(math.exp(-1 * del_g_binding/(0.008314 * 298)))
			# print del_g_binding
			# print keq
			predicted_map[mirna][targets].append(keq)
			predicted_map[mirna][targets].append(0)	# Putting mmi = 0 by default for each mirna-target gene combination so that each list has same structure.
			# print predicted_map[mirna][targets]
			if mirna in mirna_host_gene_map_with_transcript_count.keys():
				if not mirna_host_gene_map_with_transcript_count[mirna]["Host Gene"] == "":
					m = find_target_gene_expression(targets)
					mi = float(mirna_host_gene_map_with_transcript_count[mirna]["Gene Transcript Count"])
					mmi = keq * m * mi
					predicted_map[mirna][targets].append(mmi)
	jsonify(predicted_map, 'predicted_with_keq_mmi_exp.py', 'predicted_map_with_keq_mmi_exp')
			# raw_input('Enter')


def find_target_gene_expression(target_gene):
	with open('./data_used_for_mapping/gene_coordinates_from_ensembl.tsv', 'r') as gene_file:
		gene_data = csv.reader(gene_file, dialect = 'excel-tab', skipinitialspace = True)
		next(gene_data, None)
		for each_line in gene_data:
			if each_line[4] == target_gene:
				return float(each_line[5])
		gene_file.seek(0)
				# return each_line[5]


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