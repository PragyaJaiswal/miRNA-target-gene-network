#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
from Bio import SeqIO

from miRNA_meta_data import miRNA_meta_data

def extract(fam_mirna, mirna, data):
	for record in data:
		if fam_mirna in record.name:
			print 'Here'
			print 'Family name: ' + str(fam_mirna)
			print 'mirna name: ' + str(mirna)
			if 'accessions' in record.annotations.keys():
				miRNA_meta_data[mirna]['Accession ID'] = record.annotations['accessions']
			else:
				miRNA_meta_data[mirna]['Accession ID'] = record.id
			
			miRNA_meta_data[mirna]['Name'] = record.name
			miRNA_meta_data[mirna]['Description'] = record.description
			miRNA_meta_data[mirna]['Database cross-references'] = record.dbxrefs
			
			if 'comment' in record.annotations.keys():
				miRNA_meta_data[mirna]['comment'] = record.annotations['comment']
			if 'references' in record.annotations.keys():
				# print type(record.annotations['references'])
				miRNA_meta_data[mirna]['citations'] = {}
				for i in xrange(0,len(record.annotations['references'])):
					miRNA_meta_data[mirna]['citations'][i] = {}
					miRNA_meta_data[mirna]['citations'][i]['title'] = record.annotations['references'][i].title
					miRNA_meta_data[mirna]['citations'][i]['authors'] = record.annotations['references'][i].authors
					miRNA_meta_data[mirna]['citations'][i]['journal'] = record.annotations['references'][i].journal
			break


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	with open('./miRNA.dat') as data_file:
		data = SeqIO.parse(data_file, 'embl')
		# print type(data)
		for mirna in miRNA_meta_data.keys():
			string = ''
			lis = mirna.split('-')
			for x in range(0,len(lis)):
				if 'p' in lis[x]:
					pass
				else:
					base = lis[x] + '-'
					string+=base
			fam_mirna = str.lower(string[:-1])
			extract(fam_mirna, mirna, data)
	jsonify(miRNA_meta_data, 'miRNA_meta_data_new.py', 'miRNA_meta_data')
	jsonify(miRNA_meta_data, 'miRNA_meta_data_new.json')