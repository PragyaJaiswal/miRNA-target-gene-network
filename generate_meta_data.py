#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math
from Bio import SeqIO

from predicted import predicted_map
from mirna_host_target_gene_expression import mirna_host_target_gene_expression

# from miRNA_meta_data import miRNA_meta_data

accession_map = {}
family_accession_map = {}
all_target_genes = {}

'''
For miRNA meta data.
'''
def append_data():
	for mirna in mirna_host_target_gene_expression:
		for target in predicted_map[mirna].keys():
			seq = predicted_map[mirna][target][3]
			mirna_host_target_gene_expression[mirna]["miRNA Sequence"] = seq

			if mirna in family_accession_map.keys():
				fam_mirna_link = 'http://mirbase.org/cgi-bin/mirna_entry.pl?acc=' + str(family_accession_map[mirna])
				mirna_host_target_gene_expression[mirna]["miRNA family entry"] = fam_mirna_link
			else:
				mirna_host_target_gene_expression[mirna]["miRNA family entry"] = None

			# print accession_map[mirna]
			if mirna in accession_map.keys():
				mature_mirna_link = 'http://mirbase.org/cgi-bin/mature.pl?mature_acc=' + str(accession_map[mirna])
				mirna_host_target_gene_expression[mirna]["mature miRNA entry"] = mature_mirna_link
			else:
				mirna_host_target_gene_expression[mirna]["mature miRNA entry"] = None
	jsonify(mirna_host_target_gene_expression, 'miRNA_meta_data.py', 'miRNA_meta_data')
	jsonify(mirna_host_target_gene_expression, 'miRNA_meta_data.json')
	return mirna_host_target_gene_expression

'''
For gene meta data.
'''
def reverse_map(miRNA_meta_data):
	reverse = {}
	for mirna in miRNA_meta_data.keys():
		if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
			for target in miRNA_meta_data[mirna]['Target Gene with Transcript Count']:
				# print target[0]
				reverse[target[0]] = []

	for mirna in miRNA_meta_data.keys():
		if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
			for target in miRNA_meta_data[mirna]['Target Gene with Transcript Count']:
				reverse[target[0]].append(mirna)
	jsonify(reverse, 'map_reverse.py', 'miRNA_reverse')
	return reverse


def extend_reverse_map_for_genes(miRNA_meta_data, gene_data, map_reverse):
	gene_data_new = {}
	for mirna in miRNA_meta_data.keys():
		if 'Host Gene' in miRNA_meta_data[mirna].keys() and not miRNA_meta_data[mirna]['Host Gene'] == '':
			gene = miRNA_meta_data[mirna]['Host Gene']
			gene_data_new[gene] = {}
			gene_data_new[gene]['Host for'] = mirna
			if gene in map_reverse.keys():
				gene_data_new[gene]['Target for'] = map_reverse[gene]
			else:
				gene_data_new[gene]['Target for'] = ''
			if gene in gene_data.keys():
				for key, value in gene_data[gene].iteritems():
					gene_data_new[gene][key] = value
		if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
			for target in miRNA_meta_data[mirna]['Target Gene with Transcript Count']:
				gene = target[0]
				if gene in gene_data_new.keys():
					pass
				else:
					gene_data_new[gene] = {}
					gene_data_new[gene]['Host for'] = ''
					if gene in map_reverse.keys():
						gene_data_new[gene]['Target for'] = map_reverse[gene]
					else:
						gene_data_new[gene]['Target for'] = ''
					if gene in gene_data.keys():
						for key, value in gene_data[gene].iteritems():
							gene_data_new[gene][key] = value
	jsonify(gene_data_new, 'gene_meta_data.py', 'gene_meta_data')

'''
def include_gene_transcript_count_to_gene_metadata():
	for mirna in mirna_host_target_gene_expression.keys():
		if "Host Gene" in mirna_host_target_gene_expression[mirna].keys() and not mirna_host_target_gene_expression[mirna]["Host Gene"] == '':
			all_target_genes[mirna_host_target_gene_expression[mirna]["Host Gene"]] = mirna_host_target_gene_expression[mirna]["Host Gene Transcript Count"]
		if "Target Gene with Transcript Count" in mirna_host_target_gene_expression[mirna].keys():
			for each in mirna_host_target_gene_expression[mirna]["Target Gene with Transcript Count"]:
				all_target_genes[each[0]] = each[1]
		# print all_target_genes
	with open('gene_ID_Store.json') as gene_data:
		data = json.load(gene_data)
		for gene in all_target_genes:
			if gene in data.keys():
				data[gene]["Gene Transcript Count"] = all_target_genes[gene]
			# else:
			# 	data[gene]["Gene Transcript Count"] = None
		jsonify(data, 'gene_ID_Store_transcript_count.py', 'gene_meta_data')
'''

def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)

if __name__ == '__main__':
	# for data in SeqIO.parse('C:\Users\Pragya\Documents\GitHub\miRNA-target-gene-network\mature\mature.fa', 'fasta'):
	for data in SeqIO.parse('./mature/mature.fa', 'fasta'):
		if 'Homo sapiens' in data.description:
			accession_map[(data.description).split()[0]] = (data.description).split()[1]
	
	# with open('C:\Users\Pragya\Documents\GitHub\miRNA-target-gene-network\miFam\miFam.dat', 'r') as infile:
	with open('./miFam/miFam.dat', 'r') as infile:
		data = [line.rstrip('\n') for line in infile]
		for index, line in enumerate(data):
			lis = line.split()
			if len(lis) > 2:
				if 'hsa' in lis[2]:
					family_accession_map[lis[2]] = lis[1]
	miRNA_meta_data = append_data()
	# include_gene_transcript_count_to_gene_metadata()
	map_reverse = reverse_map(miRNA_meta_data)
	with open('./gene_ID_Store.json', 'r') as infile:
		gene_data = json.loads(infile.read())
		extend_reverse_map_for_genes(miRNA_meta_data, gene_data, map_reverse)