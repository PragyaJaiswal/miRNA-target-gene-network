# Outputs - mirna_host_gene_map_with_transcript_count.py
import re, json, csv, itertools
import os, sys

sys.path.insert(0, './data_used_for_mapping/')

from mirna_map_dict_new_release import mirna_map_dict
from gene_coordinates_from_ensembl import gene_coordinates_from_ensembl as gene_dict

'''
Form gene coordinates data from esembl.
'''
def main():
	global mirna_data, gene_data
	gene_dict = {}
	with open('./data_used_for_mapping/chr_coordinates_of_mirna.csv', 'r') as mirna_file:
		mirna_data = csv.reader(mirna_file, dialect = 'excel', skipinitialspace = True)

	with open('./data_used_for_mapping/gene_coordinates_from_ensembl.tsv', 'r') as gene_file:
		gene_data = csv.reader(gene_file, dialect = 'excel-tab', skipinitialspace = True)
		next(gene_data, None)
		for each_line in gene_data:
			if each_line[1] in gene_dict.keys():
				if each_line[0] in gene_dict[each_line[1]].keys():
					gene_dict[each_line[1]][each_line[0]]['start'] = int(each_line[2])
					gene_dict[each_line[1]][each_line[0]]['end'] = int(each_line[3])
					gene_dict[each_line[1]][each_line[0]]['gene_name'] = str(each_line[4])
					gene_dict[each_line[1]][each_line[0]]['transcript_count'] = int(each_line[5])
				else:
					gene_dict[each_line[1]][each_line[0]] = {}
					gene_dict[each_line[1]][each_line[0]]['start'] = int(each_line[2])
					gene_dict[each_line[1]][each_line[0]]['end'] = int(each_line[3])
					gene_dict[each_line[1]][each_line[0]]['gene_name'] = str(each_line[4])
					gene_dict[each_line[1]][each_line[0]]['transcript_count'] = int(each_line[5])
			else:
				gene_dict[each_line[1]] = {}
				if each_line[0] in gene_dict[each_line[1]].keys():
					gene_dict[each_line[1]][each_line[0]]['start'] = int(each_line[2])
					gene_dict[each_line[1]][each_line[0]]['end'] = int(each_line[3])
					gene_dict[each_line[1]][each_line[0]]['gene_name'] = str(each_line[4])
					gene_dict[each_line[1]][each_line[0]]['transcript_count'] = int(each_line[5])
				else:
					gene_dict[each_line[1]][each_line[0]] = {}
					gene_dict[each_line[1]][each_line[0]]['start'] = int(each_line[2])
					gene_dict[each_line[1]][each_line[0]]['end'] = int(each_line[3])
					gene_dict[each_line[1]][each_line[0]]['gene_name'] = str(each_line[4])
					gene_dict[each_line[1]][each_line[0]]['transcript_count'] = int(each_line[5])
			# raw_input('Enter')
		print len(gene_dict.keys())
		jsonify(gene_dict, '.\data_used_for_mapping\gene_coordinates_from_ensembl.py', 'gene_coordinates_from_ensembl')


'''
Find host for miRNAs.
'''
def compare_coordinates():
	final_dict = {}
	with open('./data_used_for_mapping/chr_coordinates_of_mirna.csv', 'r') as mirna_file:
		mirna_data = csv.reader(mirna_file, dialect = 'excel', skipinitialspace = True)
		
		for line in mirna_data:
			if line[3] in mirna_map_dict.keys():
				final_dict[line[3]] = {}
				print 'For miRNA : ' + str(line[3])
				chro = str(line[0])
				mirna_start = line[1]
				mirna_end = line[2]
				for each in gene_dict[chro].keys():
					# final_dict[line[3]]['miRNA Transcript Count'] = ''
					# final_dict[line[3]]['Host Gene'] = ''
					# final_dict[line[3]]['Gene Transcript Count'] = ''
					if gene_dict[chro][each]['start'] <= int(mirna_start) and int(mirna_end) <= gene_dict[chro][each]['end']:
						if 'MIR' in str(gene_dict[chro][each]['gene_name']):
							final_dict[line[3]]['miRNA Transcript Count'] = gene_dict[chro][each]['transcript_count']
							final_dict[line[3]]['miRNA Name'] = gene_dict[chro][each]['gene_name']
						else:
							final_dict[line[3]]['Host Gene'] = gene_dict[chro][each]['gene_name']
							final_dict[line[3]]['Host Gene Transcript Count'] = gene_dict[chro][each]['transcript_count']
							print 'Gene : ' + str(gene_dict[chro][each]['gene_name'])
							print 'Normal: ' + str(gene_dict[chro][each]['gene_name'])
							print 'In dict: ' + final_dict[line[3]]['Host Gene']
							print 'Transcript count : ' + str(gene_dict[chro][each]['transcript_count'])
						# print final_dict
						# raw_input('Enter')
				# jsonify(final_dict, 'mirna_host_gene_map_with_transcript_count.py', 'mirna_host_gene_map_with_transcript_count')
		# print final_dict
		# for mirna in mirna_map_dict.keys():
		# 	if mirna in final_dict:
		# 		pass
		# 	else:
		# 		final_dict[mirna] = {}

		
		for mirna in mirna_map_dict.keys():
			final_dict[mirna]['Target Gene with Transcript Count'] = []
			for target in mirna_map_dict[mirna]:
				m = find_target_gene_expression(target)
				tup = (target, m)
				final_dict[mirna]['Target Gene with Transcript Count'].append(tup)
		jsonify(final_dict, 'mirna_host_target_gene_expression_new_release_test.py', 'mirna_host_gene_map_with_transcript_count')
		

		# jsonify(final_dict, 'mirna_host_gene_map_with_transcript_count_new_release.py', 'mirna_host_gene_map_with_transcript_count')


def find_target_gene_expression(target_gene):
	# print target_gene
	with open('./data_used_for_mapping/gene_coordinates_from_ensembl.tsv', 'r') as gene_file:
		gene_data = csv.reader(gene_file, dialect = 'excel-tab', skipinitialspace = True)
		next(gene_data, None)
		for each_line in gene_data:
			if str(each_line[4]) == str(target_gene):
				value = int(each_line[5])
				gene_file.seek(0)
				return value
			else:
				# Also returns 0 for the genes whose transcript count is not known to us
				value = int(0)
		gene_file.seek(0)
		return value


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	# main()
	compare_coordinates()