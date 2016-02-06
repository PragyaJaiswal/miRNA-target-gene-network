#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Script to cross-check miRNAs available in
mature.fa and the 1710 intrnic computed by us. 
'''
import json
from Bio import SeqIO

def check():
	lis = []
	with open('./mature/mature.fa', 'r') as m:
		data = SeqIO.parse(m, 'fasta')
		for record in data:
			if 'hsa' in record.id:
				lis.append(record.id)
		print(len(lis))

	with open('mirna_meta_data_complete.json', 'r') as m:
		data = json.load(m)
		print(len(data))
		for mirna in data.keys():
			if mirna in lis:
				pass
			else:
				print(mirna)

if __name__ == '__main__':
	check()