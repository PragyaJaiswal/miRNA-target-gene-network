'''
Script to map between the mapping obtained from inmirna.org 
and the list of mirna obtained from mirBase.
'''

from mirna_map_dict import mirna_map_dict
import json, itertools

def get_inmirna_mirna_lis():
	inmirna_list = {}
	with open('hsa-host2miRNA.txt', 'r') as inmirna_map:
		data = [line.rstrip('\n') for line in inmirna_map]
		for line in data:
			host_gene = line.split('\t')[0]
			mirna = line.split('\t')[1]
			if ';' in mirna:
				# mirna.split(';')
				for each in mirna.split(';'):
					if each in inmirna_list.keys():
						# print each, host_gene
						inmirna_list[each].append(host_gene)
					else:
						inmirna_list[each] = []
						inmirna_list[each].append(host_gene)
			else:
				inmirna_list[mirna] = []
				inmirna_list[mirna].append(host_gene)
		print (len(inmirna_list.keys()))
		jsonify(inmirna_list, 'hsa-host2miRNA.py', 'hsa-host2miRNA')
		return inmirna_list
		# print inmirna_list

def mapper(inmirna_list, used_mirna_lis):
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
	inmirna_list = get_inmirna_mirna_lis()
	mapper(inmirna_list, mirna_map_dict.keys())