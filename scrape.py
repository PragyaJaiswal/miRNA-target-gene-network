#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math
import requests
from bs4 import BeautifulSoup
import urllib

from miRNA_meta_data_intronic_complete import miRNA_meta_data

class scrape(object):
	"""docstring for scrape"""
	def __init__(self):
		pass
		
	def rfam(self):
		url = 'http://rfam.xfam.org/family/'
		for mirna in miRNA_meta_data.keys():
			if 'Database cross-references' in miRNA_meta_data[mirna].keys() and not miRNA_meta_data[mirna]['Database cross-references'] == []:
				for entry in miRNA_meta_data[mirna]['Database cross-references']:
					if 'RFAM' in entry:
						print entry
						param = entry.split(':')[1]
						url = url + str(param)
						doc = urllib.urlopen(url).read()
						soup = BeautifulSoup(doc)
						# texts = soup.findAll(text=True)
						# print texts
						print soup.find('p').string
						# mydivs = soup.find("div", { "class" : "wpData controlTabContent" })
						# for section in mydivs.findAll('p'):
						# 	print section.string
						# 	raw_input('Enter')
						for data in soup.find_all('p'):
							if data.string == None:
								pass
							else:
								print data.string
								print data.parent
							# for post in soup.findAll('h2'):
							# 	nextNode = post
							# 	print nextNode
							# 	while True:
							# 		nextNode = nextNode.nextSibling
							# 		try:
							# 			tag_name = nextNode.name
							# 		except AttributeError:
							# 			tag_name = ""
							# 		if tag_name == "p":
							# 			print nextNode.string
							# 		else:
							# 			print "*****"
							# 			break
						# towrite = ''
						# with open('./text.txt', 'wb') as outfile:
						# 	data = soup.find(class='wpData controlTabContent')
						# 	for each in data:
						# 		towrite = towrite + each.text
						# 	outfile.write(towrite.encode("utf-8"))
						# print soup.find(id='relatedarticlesinpubmed').find_all('a')

'''
Adds more database cross-references to miRNA_meta_data_intronic_complete
and gives miRNA_meta_data_intronic_complete_new.
Homo_sapiens.gene_info obtained from the following website -
ftp://ftp.ncbi.nih.gov/gene/DATA/GENE_INFO/Mammalia/
'''
def append_ids(dictionary):
	more_ids = {}
	for mirna in miRNA_meta_data.keys():
		if 'Accession ID' in miRNA_meta_data[mirna].keys():
			accession = miRNA_meta_data[mirna]['Accession ID'][0]
			lis = dictionary[accession]
			# print lis
			miRNA_meta_data[mirna]['Database cross-references'].extend(lis)
			# print miRNA_meta_data[mirna]
			# raw_input('Enter')

	# jsonify(miRNA_meta_data, 'miRNA_meta_data_intronic_complete_new.py', 'miRNA_meta_data')
	jsonify(miRNA_meta_data, 'miRNA_meta_data_intronic_complete_new.json')


def id_dict(data):
	dictionary = {}
	for line in data:
		if 'miRBase' in line[5]:
			accession = line[5].split('miRBase:')[1]
			dictionary[accession] = line[5].split('|')
	# print dictionary
	append_ids(dictionary)


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)

if __name__ == '__main__':
	instance = scrape()
	# instance.rfam()
	with open('./mirna_data/Homo_sapiens.gene_info', 'r') as infile:
		data = csv.reader(infile, 'excel-tab')
		next(data)
		id_dict(data)
