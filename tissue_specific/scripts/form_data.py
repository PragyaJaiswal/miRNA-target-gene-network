#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import operator

sys.path.insert(0, '../data/')

from normal_tissue_test import normal_tissue

class restructure_data(object):
	"""docstring for restructure_data"""
	def __init__(self):
		pass

	def form_json(self, data):
		headers = data.next()
		next(data)
		print headers
		dictionary = {}
		for line in data:
			if line[2] in dictionary.keys():
				if line[1] not in dictionary[line[2]].keys():
					dictionary[line[2]][line[1]] = {}
					if line[3] in dictionary[line[2]][line[1]].keys():
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
					else:
						dictionary[line[2]][line[1]][line[3]] = {}
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
				else:
					if line[3] in dictionary[line[2]][line[1]].keys():
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
					else:
						dictionary[line[2]][line[1]][line[3]] = {}
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
			else:
				dictionary[line[2]] = {}
				if line[1] not in dictionary[line[2]].keys():
					dictionary[line[2]][line[1]] = {}
					if line[3] in dictionary[line[2]][line[1]].keys():
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
					else:
						dictionary[line[2]][line[1]][line[3]] = {}
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
				else:
					if line[3] in dictionary[line[2]][line[1]].keys():
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]
					else:
						dictionary[line[2]][line[1]][line[3]] = {}
						dictionary[line[2]][line[1]][line[3]]['ID'] = line[0]
						dictionary[line[2]][line[1]][line[3]]['Cell Type'] = line[3]
						dictionary[line[2]][line[1]][line[3]]['Level'] = line[4]
						dictionary[line[2]][line[1]][line[3]]['Expression Type'] = line[5]
						dictionary[line[2]][line[1]][line[3]]['Reliability'] = line[6]

			# jsonify(dictionary, '../data/normal_tissue.py', 'normal_tissue')
			jsonify(dictionary, '../data/normal_tissue.json')

	def find_tissue(self):
		print max(normal_tissue.iteritems(), key=operator.itemgetter(1))[0]
		print min(normal_tissue.iteritems(), key=operator.itemgetter(1))[0]
		for gland in normal_tissue.keys():
			tup = (gland, len(normal_tissue[gland].keys()))
			print tup
			raw_input('Enter')
			for gene in normal_tissue[gland].keys():
				for cells in normal_tissue[gland][gene]:
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
	instance = restructure_data()

	# with open('../data/normal_tissue.csv', 'r') as infile:
	# 	normal_data_reader = csv.reader(infile)
	# 	instance.form_json(normal_data_reader)

	# with open('../data/normal_tissue_test.json', 'r') as infile:
	# 	normal_tissue_test = json.loads(infile)
	# 	instance.find_tissue(normal_tissue_test)
	instance.find_tissue()