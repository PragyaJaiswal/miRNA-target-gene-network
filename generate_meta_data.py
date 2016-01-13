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


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)

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