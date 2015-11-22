'''
Script to map between the mapping obtained from inmirna.org 
and the list of mirna obtained from mirBase.
'''

import requests
from bs4 import BeautifulSoup
import json, itertools

from mirna_map_dict import mirna_map_dict

global mirna_host_gene_map
mirna_host_gene_map = {}

'''
def get_inmirna_data():
	inmirna_dict = {}
	with open('hsa-host2miRNA.txt', 'r') as inmirna_map:
		data = [line.rstrip('\n') for line in inmirna_map]
		for line in data:
			host_gene = line.split('\t')[0]
			mirna = line.split('\t')[1]
			if ';' in mirna:
				# mirna.split(';')
				for each in mirna.split(';'):
					if 'mir' in each:
						each = "".join(ele.upper() if index == 6 else ele for index, ele in enumerate(each))
					if each in inmirna_dict.keys():
						# print each, host_gene
						inmirna_dict[each].append(host_gene)
					else:
						inmirna_dict[each] = []
						inmirna_dict[each].append(host_gene)
			else:
				inmirna_dict[mirna] = []
				inmirna_dict[mirna].append(host_gene)
		print (len(inmirna_dict.keys()))
		jsonify(inmirna_dict, 'hsa-host2miRNA.py', 'hsa-host2miRNA')
		return inmirna_dict
		# print inmirna_dict

def mapper(inmirna_dict, used_mirna_lis):
	# print used_mirna_lis
	for mirna in inmirna_dict.keys():
		if mirna in mirna_map_dict.keys():
			pass
		else:
			del inmirna_dict[mirna]
	print len(inmirna_dict.keys())
	print inmirna_dict.keys()

'''

def get_host_gene(mirna, data, mirna_host_gene_map):
	URL = 'http://hoctar.tigem.it/'
	payload = {'param' : '{0}'.format(mirna), 'Start+Search' : 'Start+Search'}
	search_request = requests.get(URL + '/view_mirna.php', params = payload, timeout = 32)
	mirna_url = search_request.url
	mirna_data = BeautifulSoup(search_request.text.encode())
	for gene in data.keys():
		if str(gene) in str(mirna_data):
			if mirna in mirna_host_gene_map:
				mirna_host_gene_map[mirna].append(gene)
			else:
				mirna_host_gene_map[mirna] = []
				mirna_host_gene_map[mirna].append(gene)
	# print mirna_host_gene_map
	jsonify(mirna_host_gene_map, 'mirna_host_gene_map.py', 'mirna_host_gene_map')


def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	# inmirna_dict = get_inmirna_data()
	# mapper(inmirna_dict, mirna_map_dict.keys())
	with open('gene_ID_Store.json') as gene_data_file:
		data = json.load(gene_data_file)
	mirna_host_gene_map = {}
	for mirna in mirna_map_dict.keys():
		print 'Extracting host_gene for mirna {0}'.format(mirna)
		get_host_gene(mirna, data, mirna_host_gene_map)