'''
# Script not used anymore.

Script to map between the host-gene mapping obtained 
from inmirna.org and the list of mirna obtained from
mirBase.
596 miRNAs from miRBase.
hsa-host2miRNA.py/hsa-host2miRNA.txt gives the host
list obtained from inmirna.org.
Finding host of the 596 miRNAs in this host list
results in only 158 out of 596 results which are
miRNAs whose host genes are known.
Result and data discarded for poor performance.

Host gene mapping now obtained from Ensembl gene
coordinates.
'''

import requests
from bs4 import BeautifulSoup
import re, json, itertools, csv

from mirna_map_dict import mirna_map_dict
from mirna_host_gene_map import mirna_host_gene_map

#------ global mirna_host_gene_map
#------ mirna_host_gene_map = {}


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
		# jsonify(inmirna_dict, 'hsa-host2miRNA.py', 'hsa-host2miRNA')
		return inmirna_dict
		# print inmirna_dict

def mapper(inmirna_dict, used_mirna_lis, data):
	# print used_mirna_lis
	lis = []
	original_name_lis = []
	dictionary = {}

	# Remove the 3p, 5p from the mirna names.
	for each in mirna_map_dict.keys():
		# print 'Each: ' + str(each)
		original_name = each
		if 'p' in each:
			mirna_modified_name = "-".join(_ for _ in each.split('-') if not 'p' in _)
		else:
			mirna_modified_name = str(each)
		# print 'Modified name: ' + str(mirna_modified_name)
		lis.append(mirna_modified_name)
		original_name_lis.append(original_name)
	print len(lis)
	# print inmirna_dict
	
	# Convert Ensembl ids to Gene Name kinda Ids.
	for mirna in inmirna_dict.keys():
		dictionary[mirna] = []
		# for i in range(0,len(inmirna_dict[mirna])):
		for key in data.keys():
			for x in inmirna_dict[mirna]:
				if data[key]["names"][0] == str(x):
					# print data[key]["names"][0]
					# print "Key: " + str(key)
					# print str(x)
					dictionary[mirna].append(str(key))
			# dictionary[mirna].append(_ for _ in inmirna_dict[mirna] if data[key]["names"][0] == _)
		inmirna_dict[mirna] = dictionary[mirna]
		# print inmirna_dict[mirna]
	# print inmirna_dict
	# print len(inmirna_dict.keys())

	# Remove those miRNAs from the inmirna dict whose host gene is not present.
	for mirna in inmirna_dict.keys():
		if mirna in lis:
			# print inmirna_dict[mirna]
			mirna_host_gene_map[original_name_lis[lis.index(mirna)]] = inmirna_dict[mirna]
			# mirna_host_gene_map
		else:
			del inmirna_dict[mirna]
	# print len(inmirna_dict.keys())
	
	jsonify(mirna_host_gene_map, 'mirna_host_gene_map.py', 'mirna_host_gene_map')
	# print inmirna_dict.keys()


'''
def get_host_gene(original_mirna_name, mirna_modified_name, data, mirna_host_gene_map):
	URL = 'http://hoctar.tigem.it/'
	payload = {'param' : '{0}'.format(mirna_modified_name), 'Start+Search' : 'Start+Search'}
	search_request = requests.get(URL + '/view_mirna.php', params = payload, timeout = 32)
	mirna_url = search_request.url
	mirna_data = BeautifulSoup(search_request.text.encode())
	mirna_host_gene_map[original_mirna_name] = []

	head = mirna_data.find_all('td')
	data_around_hostgene = []
	for i in range(0,len(head)):
		if 'Hostgene:' in head[i].text:
			data_around_hostgene.append(head[i].text)
			data_around_hostgene.append(head[i+1].text)
			data_around_hostgene.append(head[i+2].text)
			# print str(data_around_hostgene)
	if 'Hostgene:' in str(data_around_hostgene):
		# count = 0
		data_around_hostgene[1] = data_around_hostgene[1].replace(u'\xa0', u' ')
		print str(data_around_hostgene[1])
		if '(' in data_around_hostgene[1]:
			data_around_hostgene[1] = data_around_hostgene[1].split('(')[0]
		# print data_around_hostgene[1]
		name = re.split(r'[()/  ]', data_around_hostgene[1])
		pattern = re.compile(r'[A-Z][A-Z\d]+')
		# for gene in data.keys():
		# 	# count+=1
		for x in name:
			if pattern.match(x):
				print 'Name: ' + str(x)
				mirna_host_gene_map[original_mirna_name].append(str(x))
				# for gene in data.keys():
				# 	if str(gene) == str(x):
				# 		print 'Gene : ' + str(gene)
				# 		mirna_host_gene_map[original_mirna_name].append(gene)
		# print count
	jsonify(mirna_host_gene_map, 'mirna_host_gene_map.py', 'mirna_host_gene_map')


def get_expression(data):
	new_map_with_expression_levels = {}
	with open('./mRNA concentration data/data.tsv', 'r') as infile:
		expression_data = csv.reader(infile, dialect = 'excel-tab', skipinitialspace = True)
		next(expression_data, None)
		# expression_data = [line.rstrip('\n') for line in infile]

		for index, ele in enumerate(mirna_host_gene_map.keys()):
			if not mirna_host_gene_map[ele]:
				pass
			else:
				print 'In else for {0}'.format(ele)
				for x in mirna_host_gene_map[ele]:
					new_map_with_expression_levels[ele] = {}
					new_map_with_expression_levels[ele]['Gene'] = x
					new_map_with_expression_levels[ele]['Gene Expression Level'] = ''
					if x in data.keys():
						ensembl_id = data[x]["names"][0]
						print ensembl_id
						for line in expression_data:
							# print line[2]
							if ensembl_id == str(line[2]):
								print 'Here'
								mrna_expression = line[6]
								# new_map_with_expression_levels[ele] = {}
								# new_map_with_expression_levels[ele]['Gene'] = x
								new_map_with_expression_levels[ele]['Gene Expression Level'] = float(mrna_expression)
								print mrna_expression
								jsonify(new_map_with_expression_levels, 'mirna_host_gene_map_with_expression_levels.py', 'mirna_host_gene_map_with_expression_levels')
								break
						infile.seek(0)
						next(expression_data, None)

'''
def jsonify(dictionary, filename, text='None'):
	a = json.dumps(dictionary, sort_keys=True, indent=4, separators=(',', ': '))
	with open(str(filename), 'w') as outfile:
		if text == 'None':
			outfile.write(a)
		else:
			outfile.write(text + ' = ')
			outfile.write(a)


if __name__ == '__main__':
	inmirna_dict = get_inmirna_data()
	with open('gene_ID_Store.json') as gene_data_file:
		data = json.load(gene_data_file)
	mapper(inmirna_dict, mirna_map_dict.keys(), data)
	# #------ mirna_host_gene_map = {}
	# get_expression(data)
	# # for mirna in mirna_map_dict.keys():
	# # 	print 'Extracting host_gene for mirna {0}'.format(mirna)
	# # 	mirna_modified_name = "-".join(_ for _ in mirna.split('-') if not 'p' in _)
	# # 	# print "-".join(_ if not '3p' in _ else "LOL" for _ in mirna.split('-'))
	# # 	# print "-".join(mirna.split('-')[i] if not 'p' in mirna.split('-')[i] for i in range(0, len(mirna.split('-'))))
	# # 	get_host_gene(mirna, mirna_modified_name, data, mirna_host_gene_map)