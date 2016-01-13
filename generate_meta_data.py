#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math
from Bio import SeqIO

from predicted import predicted_map
from mirna_host_target_gene_expression import mirna_host_target_gene_expression

accession_map = {}
family_accession_map = {}
all_target_genes = {}

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


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


# def include_gene_transcript_count_to_gene_metadata():
# 	for mirna in mirna_host_target_gene_expression.keys():
# 		if "Host Gene":
# 			pass
# 		if not mirna_host_target_gene_expression[mirna]["Host Gene"] == '' :
# 			all_target_genes[mirna_host_target_gene_expression[mirna]["Host Gene"]] = mirna_host_target_gene_expression[mirna]["Host Gene Transcript Count"]
# 		if "Target Gene with Transcript Count" in mirna_host_target_gene_expression[mirna].keys():
# 			for each in mirna_host_target_gene_expression[mirna]["Target Gene with Transcript Count"]:
# 				all_target_genes[each[0]] = each[1]
# 		# print all_target_genes
# 	with open('gene_ID_Store.json') as gene_data:
# 		data = json.load(gene_data)
# 		for gene in all_target_genes:
# 			if gene in data.keys():
# 				data[gene]["Gene Transcript Count"] = all_target_genes[gene]
# 			else:
# 				data[gene]["Gene Transcript Count"] = None
# 		jsonify(data, 'gene_ID_Store_transcript_count.py', 'gene_meta_data')



if __name__ == '__main__':
	for data in SeqIO.parse('C:\Users\Pragya\Documents\GitHub\miRNA-target-gene-network\mature\mature.fa', 'fasta'):
		if 'Homo sapiens' in data.description:
			
			accession_map[(data.description).split()[0]] = (data.description).split()[1]
	
	with open('C:\Users\Pragya\Documents\GitHub\miRNA-target-gene-network\miFam\miFam.dat', 'r') as infile:
		data = [line.rstrip('\n') for line in infile]
		for index, line in enumerate(data):
			lis = line.split()
			if len(lis) > 2:
				if 'hsa' in lis[2]:
					family_accession_map[lis[2]] = lis[1]
	append_data()
	# include_gene_transcript_count_to_gene_metadata()