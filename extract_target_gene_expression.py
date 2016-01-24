#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Outputs - mirna_host_target_gene_expression_new_release.py, predicted_with_keq_mmi_exp.py

'''
FOR NEW RELEASE.
TEMPORARY.
Only till free_energy.py doesn't give results for this data.
'''
import os, sys
import json, csv, re
import math

from mirna_host_gene_map_with_transcript_count_new_release import mirna_host_gene_map_with_transcript_count
from mirna_map_dict_new_release import mirna_map_dict

def target_transcript_count():
	for mirna in mirna_map_dict.keys():
		mirna_host_gene_map_with_transcript_count[mirna]['Target Gene with Transcript Count'] = []
		for target in mirna_map_dict[mirna]:
			m = find_target_gene_expression(target)
			tup = (target, m)
			mirna_host_gene_map_with_transcript_count[mirna]['Target Gene with Transcript Count'].append(tup)
		# print mirna_host_gene_map_with_transcript_count[mirna]
		# raw_input('Enter')
	jsonify(mirna_host_gene_map_with_transcript_count, 'mirna_host_target_gene_expression_new_release.py', 'mirna_host_target_gene_expression')


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


def check_intronic(mirna_data):
	with open('./intronic_mirna_data/introns.tsv') as infile:
		intron_reader = csv.reader(infile, dialect = 'excel-tab', skipinitialspace = True)
		for line in mirna_data:
			chro = line[0]
			start = line[1]
			end = line[2]
			mirna = line[3]
			# if mirna in mirna_host_gene_map_with_transcript_count.keys():
			for each_line in intron_reader:
				if each_line[0].split('chr')[1] == chro:
					if each_line[1] <= start <= each_line[2] and each_line[1] <= end <= each_line[2]:
						final_intronic_dict[mirna] = mirna_host_gene_map_with_transcript_count[mirna]
					else:
						pass
		

def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	# target_transcript_count()
	
	with open('./data_used_for_mapping/chr_coordinates_of_mirna.csv', 'r') as mirna_file:
		mirna_data = csv.reader(mirna_file, dialect = 'excel', skipinitialspace = True)
		check_intronic(mirna_data)