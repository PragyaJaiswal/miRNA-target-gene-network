#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import json
import math
import operator

from miRNA_meta_data_intronic_complete_new import miRNA_meta_data
from predicted_with_keq_mmi_exp import predicted_map_with_keq_mmi_exp
from gene_meta_data_new import gene_meta_data

class stats(object):
	"""docstring for stats"""
	def __init__(self):
		pass
		
	def range_of_gene_trans_count_affinity(self):
		target_transcript_count_dict = {}
		target_affinity_dict = {}
		for mirna in miRNA_meta_data:
			if 'Host Gene' in miRNA_meta_data[mirna].keys():
				gene = miRNA_meta_data[mirna]['Host Gene']
				target_transcript_count_dict[gene] = miRNA_meta_data[mirna]['Host Gene Transcript Count']
			
			if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
				for target in miRNA_meta_data[mirna]['Target Gene with Transcript Count']:
					target_transcript_count_dict[target[0]] = target[1]
					target_affinity_dict[target[0]] = target[2]

		mini_trans_count = min(target_transcript_count_dict.values())
		maxi_trans_count = max(target_transcript_count_dict.values())		
		mini_trans_count_lis = []
		maxi_trans_count_lis = []
		
		for key, value in target_transcript_count_dict.iteritems():
			if value == mini_trans_count:
				mini_trans_count_lis.append(key)
			if value == maxi_trans_count:
				maxi_trans_count_lis.append(key)

		trans_range = (mini_trans_count, maxi_trans_count)
		
		# Negative values. Larger negative value means smaller affinity.
		lis = [x for x in target_affinity_dict.values() if x is not None]

		mini_affinity = max(lis)
		maxi_affinity = min(lis)
		mini_affinity_lis = []
		maxi_affinity_lis = []

		for key, value in target_affinity_dict.iteritems():
			if value == mini_affinity:
				maxi_affinity_lis.append(key)
			if value == maxi_affinity:
				mini_affinity_lis.append(key)

		affinity_range = (mini_affinity, maxi_affinity)

		print 'Range for transcript counts of genes:\n' + str(trans_range)
		print 'Range for affinity values of genes:\n' + str(affinity_range)


	# Has issues.
	def mmi_cutoff_value(self):
		mmi_dict = {}
		for mirna in predicted_map_with_keq_mmi_exp.keys():
			for target in predicted_map_with_keq_mmi_exp[mirna].keys():
				if not predicted_map_with_keq_mmi_exp[mirna][target] == []:
					# if len(predicted_map_with_keq_mmi_exp[mirna][target]) == 31:
					# 	print mirna
					mmi_dict[target] = predicted_map_with_keq_mmi_exp[mirna][target][-1]

		# print min(mmi_dict.values())
		# print max(mmi_dict.values())

		ranges = (min(mmi_dict.values()), max(mmi_dict.values()))
		print 'Range for [m-mi] complex:\n' + str(ranges)


class mirna_stats(object):
	"""docstring for mirna_stats"""
	def __init__(self):
		pass
		
	def mirna_with_max_interactions(self):
		mirna_interact_dict = {}
		lis = []
		for mirna in miRNA_meta_data.keys():
			if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
				mirna_interact_dict[mirna] = len(miRNA_meta_data[mirna]['Target Gene with Transcript Count'])

		mirna_having_max_interactions = max(mirna_interact_dict.iteritems(), key=operator.itemgetter(1))
		number_of_interactions = max(mirna_interact_dict.values())

		for key, value in mirna_interact_dict.iteritems():
			if value == number_of_interactions:
				lis.append((key,value))

		print '\nmiRNA with maximum interactions:\n' + str(lis)

	def mirna_interacting_with_host(self):
		miRNA_lis = []
		for mirna in miRNA_meta_data.keys():
			target_lis = []
			if 'Host Gene' in miRNA_meta_data[mirna].keys():
				host = miRNA_meta_data[mirna]['Host Gene']
				if 'Target Gene with Transcript Count' in miRNA_meta_data[mirna].keys():
					for target in miRNA_meta_data[mirna]['Target Gene with Transcript Count']:
						target_lis.append(target[0])
			if host in target_lis:
				miRNA_lis.append(mirna)
		
		print 'Number of miRNAs targeting the host genes:\n' + str(len(miRNA_lis))
		print 'miRNAs targeting the host genes:\n' + str(miRNA_lis)


class gene_stats(object):
	"""docstring for gene_stats"""
	def __init__(self):
		pass

	def gene_with_maximum_interactions(self):
		gene_interact_dict = {}
		lis = []
		for gene in gene_meta_data.keys():
			if 'Target for' in gene_meta_data[gene].keys():
				gene_interact_dict[gene] = len(gene_meta_data[gene]['Target for'])

		gene_having_max_interactions = max(gene_interact_dict.iteritems(), key=operator.itemgetter(1))
		number_of_interactions = max(gene_interact_dict.values())

		for key, value in gene_interact_dict.iteritems():
			if value == number_of_interactions:
				lis.append((key,value))

		print '\nGene being targetted most by miRNAs:\n' + str(lis)

	def gene_having_mirna_as_host_and_target(self):
		gene_lis = []
		for gene in gene_meta_data.keys():
			target_lis = gene_meta_data[gene]['Target for']
			host_lis = gene_meta_data[gene]['Host for']
			for mirna in target_lis:
				if mirna in host_lis:
					gene_lis.append(gene)

			for mirna in host_lis:
				if mirna in target_lis:
					if gene not in gene_lis:
						gene_lis.append(gene)
		
		gene_lis = list(set(gene_lis))
		print 'Number of host genes being targetted by miRNAs:\n' + str(len(gene_lis))
		print 'Host Genes being targetted by miRNAs:\n' + str(gene_lis)


class network(object):
	def __init__(self):
		pass

	def total_edges():
		pass
		

if __name__ == '__main__':
	stats_instance = stats()
	stats_instance.range_of_gene_trans_count_affinity()
	mmi_cutoff_value = stats_instance.mmi_cutoff_value()

	mirna_stats_instance = mirna_stats()
	mirna_stats_instance.mirna_with_max_interactions()
	mirna_stats_instance.mirna_interacting_with_host()

	gene_stats_instance = gene_stats()
	gene_stats_instance.gene_with_maximum_interactions()
	gene_stats_instance.gene_having_mirna_as_host_and_target()