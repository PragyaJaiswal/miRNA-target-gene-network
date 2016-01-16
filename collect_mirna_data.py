#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
from Bio import SeqIO
import Bio

from miRNA_meta_data_new import miRNA_meta_data
# from mirna_complete_data
mirna_complete_data = {}

def extract(data):
	for record in data:
		mirna = record.name
		if 'hsa' in mirna:
			mirna_complete_data[mirna] = {}
			abc = {}
			if 'accessions' in record.annotations.keys():
				mirna_complete_data[mirna]['Accession ID'] = record.annotations['accessions']
			else:
				mirna_complete_data[mirna]['Accession ID'] = record.id

			mirna_complete_data[mirna]['Name'] = record.name
			mirna_complete_data[mirna]['Description'] = record.description
			mirna_complete_data[mirna]['Database cross-references'] = record.dbxrefs
			
			if 'comment' in record.annotations.keys():
				mirna_complete_data[mirna]['comment'] = record.annotations['comment']
			if 'references' in record.annotations.keys():
				# print type(record.annotations['references'])
				mirna_complete_data[mirna]['citations'] = {}
				for i in xrange(0,len(record.annotations['references'])):
					mirna_complete_data[mirna]['citations'][i] = {}
					mirna_complete_data[mirna]['citations'][i]['title'] = record.annotations['references'][i].title
					mirna_complete_data[mirna]['citations'][i]['authors'] = record.annotations['references'][i].authors
					mirna_complete_data[mirna]['citations'][i]['journal'] = record.annotations['references'][i].journal
			
			product_dict = {}
			for feature in record.features:
				# feature - contains a undecipherable format of the features
				# feature.qualifiers - a Python dictionary of additional decipherable information about the feature.
				# products - returns a list, but generally contains one product only
				# print feature.qualifiers
				if 'product' in feature.qualifiers.keys():
					products = feature.qualifiers['product']
					for product in products:
						product_dict[product] = {}
						for key, value in feature.qualifiers.iteritems():
							product_dict[product][key] = value
						# print feature.qualifiers['experiment']
			mirna_complete_data[mirna]['products'] = product_dict


def extend_meta_data():
	for mirna in miRNA_meta_data:
		for fam_mirna in mirna_complete_data.keys():
			if mirna in mirna_complete_data[fam_mirna]['products'].keys():
				for keys, info in mirna_complete_data[fam_mirna]['products'][mirna].iteritems():
					miRNA_meta_data[mirna][keys] = info

				for key, value in mirna_complete_data[fam_mirna].iteritems():
					if not key == 'products':
						miRNA_meta_data[mirna][key] = value
		jsonify(miRNA_meta_data, 'miRNA_meta_data_complete.py', 'miRNA_meta_data')
		jsonify(miRNA_meta_data, 'miRNA_meta_data_complete.json', 'miRNA_meta_data')


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
		extract(data)
		extend_meta_data()
	jsonify(mirna_complete_data, 'mirna_data_from_mirbase.py', 'mirna_data_from_mirbase')
	jsonify(mirna_complete_data, 'mirna_data_from_mirbase.json', 'mirna_data_from_mirbase')