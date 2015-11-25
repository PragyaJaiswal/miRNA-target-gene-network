#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math

from predicted import predicted_map
from mirna_host_gene_map_with_transcript_count import mirna_host_gene_map_with_transcript_count

def find_k_equivalent():
	for mirna in predicted_map.keys():
		for targets in predicted_map[mirna].keys():
			print mirna
			print targets
			# print predicted_map[mirna][targets][19]
			del_g_binding = predicted_map[mirna][targets][19]
			keq = math.exp(-1 * del_g_binding/(0.008314 * 298))
			# print del_g_binding
			# print keq
			predicted_map[mirna][targets].append(keq)
			# print predicted_map[mirna][targets]
			'''
			if not mirna_host_gene_map_with_transcript_count[mirna]["Host Gene"] == "":
				# ------- m = NOT KNOWN ----------
				mi = mirna_host_gene_map_with_transcript_count[mirna]["Gene Transcript Count"]
				mmi = keq * m * mi
				print mmi
			'''
	jsonify(predicted_map, 'predicted_with_keq.py', 'predicted_map_with_keq')
			# raw_input('Enter')


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	# with open('predicted.py', 'r') as infile:
	# 	data = json.loads(infile.read())
	# print data
	find_k_equivalent()