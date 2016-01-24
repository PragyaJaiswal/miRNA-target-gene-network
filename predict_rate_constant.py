#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Outputs - mirna_host_target_gene_expression.py, predicted_with_keq_mmi_exp.py
import os, sys
import json, csv, re
import math

from mirna_host_gene_map_with_transcript_count_new_release import mirna_host_gene_map_with_transcript_count

def find_k_equivalent(predicted_map):
	mirna_host_target_gene_expression = {}
	for mirna in predicted_map.keys():
		mirna_host_target_gene_expression[mirna] = {}
		
		for key, value in mirna_host_gene_map_with_transcript_count[mirna].iteritems():
			mirna_host_target_gene_expression[mirna][key] = value
		
		if predicted_map[mirna].keys():
			mirna_host_target_gene_expression[mirna]["Target Gene with Transcript Count"] = []
		
		for targets in predicted_map[mirna].keys():
			if not predicted_map[mirna][targets] == []:
				'''
				Extract del_g and evaluate keq using that.
				del_G could only be evaluated for targets
				whose affinity is known.
				'''
				del_g_binding = predicted_map[mirna][targets][19]
				
				# Gibbs Free Energy equation at R = 0.008314 kJ/(mol.K) and T = 298 K
				keq = float(math.exp(-1 * del_g_binding/(0.008314 * 298)))
				
				predicted_map[mirna][targets].append(keq)
				# predicted_map[mirna][targets].append(0)	# Putting mmi = 0 by default for each mirna-target gene combination so that each list has same structure.
				# print predicted_map[mirna][targets]

				'''
				Evaluate mmi concentration for those whose host gene
				expression and target gene expression are known.
				'''
				if "Host Gene" in mirna_host_gene_map_with_transcript_count[mirna].keys():
					# print mirna, targets
					# print mirna_host_gene_map_with_transcript_count[mirna]["Host Gene"]
					# raw_input('Enter')
					m = find_target_gene_expression(targets)
					mi = int(mirna_host_gene_map_with_transcript_count[mirna]["Host Gene Transcript Count"])
					
					# Uses host gene transcript count for mirna conc, target gene transcript count for mRNA conc
					mmi = keq * m * mi

					predicted_map[mirna][targets].append(mmi)

			'''
			Append target gene list containing tuples of format
			(targets, transcript count, affinity) to the final
			dictionary containing host genes (if known) and
			target genes, both with transcript counts.
			'''
			if mirna in mirna_host_gene_map_with_transcript_count.keys():
				m = find_target_gene_expression(targets)
				if not predicted_map[mirna][targets] == []:
					affinity = predicted_map[mirna][targets][19]
				else:
					affinity = None
				tup = (targets, m, affinity)
				
				# if "miRNA Transcript Count" in mirna_host_gene_map_with_transcript_count[mirna].keys():
				# 	mirna_host_target_gene_expression[mirna]["miRNA Transcript Count"] = mirna_host_gene_map_with_transcript_count[mirna]["miRNA Transcript Count"]
				# else:
				# 	# Not known
				# 	mirna_host_target_gene_expression[mirna]["miRNA Transcript Count"] = None
				
				# if "miRNA Name" in mirna_host_gene_map_with_transcript_count[mirna].keys():
				# 	mirna_host_target_gene_expression[mirna]["miRNA Name"] = mirna_host_gene_map_with_transcript_count[mirna]["miRNA Name"]
				# else:
				# 	# Not known
				# 	mirna_host_target_gene_expression[mirna]["miRNA Name"] = None
				
				mirna_host_target_gene_expression[mirna]["Target Gene with Transcript Count"].append(tup)
				# mirna_host_target_gene_expression[mirna]["Host Gene"] = ''
				# mirna_host_target_gene_expression[mirna]["Host Gene Transcript Count"] = 0
				

	for mirna in mirna_host_gene_map_with_transcript_count.keys():
		if "Host Gene" in mirna_host_gene_map_with_transcript_count[mirna].keys():
			mirna_host_target_gene_expression[mirna]["Host Gene"] = mirna_host_gene_map_with_transcript_count[mirna]["Host Gene"]
			mirna_host_target_gene_expression[mirna]["Host Gene Transcript Count"] = mirna_host_gene_map_with_transcript_count[mirna]["Host Gene Transcript Count"]
	jsonify(predicted_map, 'predicted_with_keq_mmi_exp.py', 'predicted_map_with_keq_mmi_exp')
	# jsonify(mirna_host_target_gene_expression, 'mirna_host_target_gene_expression.json')
	jsonify(mirna_host_target_gene_expression, 'mirna_host_target_gene_expression.py', 'mirna_host_target_gene_expression')


def find_target_gene_expression(target_gene):
	# print target_gene
	with open('./data_used_for_mapping/gene_coordinates_from_ensembl.tsv', 'r') as gene_file:
		gene_data = csv.reader(gene_file, dialect = 'excel-tab', skipinitialspace = True)
		next(gene_data, None)
		for each_line in gene_data:
			if str(each_line[4]) == str(target_gene):
				value = int(each_line[5])
				gene_file.seek(0)
				return value
			else:
				# Also returns 0 for the genes whose transcript count is not known to us
				value = int(0)
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
	with open('./prediction_Store.json', 'r') as infile:
		predicted_map = json.loads(infile.read())
		find_k_equivalent(predicted_map)