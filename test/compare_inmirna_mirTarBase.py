'''
Script not used anymore.
Routine incorporated in
generate_meta_data.py
'''

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
from Bio import SeqIO

# from miRNA_meta_data import miRNA_meta_data
from miRNA_meta_data_new import miRNA_meta_data

miRNA_meta_data_new = {}

'''
Script to map between the mapping obtained from inmirna.org 
and the list of mirna obtained from mirBase.
Results in 359 intronic miRNAs found in both the above, when
1495 in inmirna data and 596 mirna in miRBase.
'''
def compare(data):
	lis = []
	for mirna in data:
		lis.append(mirna.name.split('|')[0])
	# print 'Total number of intronic miRNAs:\n' + str(len(lis))
	
	# count = 0
	for mirna in miRNA_meta_data.keys():
		if mirna in lis:
			# count+=1
			miRNA_meta_data_new[mirna] = {}
			for key, value in miRNA_meta_data[mirna].iteritems():
				miRNA_meta_data_new[mirna][key] = value
	print len(miRNA_meta_data_new.keys())
	jsonify(miRNA_meta_data_new, 'miRNA_meta_data_new.json', 'miRNA_meta_data')
	jsonify(miRNA_meta_data_new, 'miRNA_meta_data_new.py', 'miRNA_meta_data')


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	with open('../intronic_mirna_data/hsa-mat-miRNA.fasta') as data_file:
		data = SeqIO.parse(data_file, 'fasta')
		compare(data)