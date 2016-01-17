#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json, csv, re
import math

from gene_meta_data import gene_meta_data
from miRNA_meta_data import miRNA_meta_data

class competition(object):
	"""docstring for competition"""
	def __init__(self):
		pass

	def ranking_parameter(self):
		for mirna in miRNA_meta_data.keys():
			if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
				for each_target in miRNA_meta_data[mirna]['Target Gene with Transcript Count']:
					del_g_binding = each_target[2]
					keq = float(math.exp(-1 * del_g_binding/(0.008314 * 298)))
					if 'Host Gene'in miRNA_meta_data[mirna].keys() and not miRNA_meta_data[mirna]['Host Gene'] == '':
						m = each_target[1]
						mi = miRNA_meta_data[mirna]['Host Gene Transcript Count']
						mmi = keq * m * mi
						print mmi

class dissociate(object):
	"""docstring for dissociate"""
	def __init__(self):
		super(dissociate, self).__init__()
		pass

	def ranking_parameter_gene_rrna(self):
		pass

	def ranking_parameter_gene_mirna(self):
		pass

	def degrade():
		pass	

class bind(object):
	"""docstring for bind"""
	def __init__(self):
		super(bind, self).__init__()
		pass

	def ranking_parameter():
		pass

if __name__ == '__main__':
	x = competition()
	x.find_k_equivalent()