import os, sys, json

'''
.xls data from mirTarBase. 'http://mirtarbase.mbc.nctu.edu.tw/index.php'
Implemented for miRNA target genes in homo sapiens.
596 miRNA and 12104 target genes.
'''

def remove_duplicates(viruses):
	output = []
	visited = set()
	for virus in viruses:
		if virus not in visited:
			output.append(virus)
			visited.add(virus)
	return output

# output_gene = remove_duplicates(genes)
# output_mirna = remove_duplicates(mirna)
# print('Gene duplicates removed: ' + str(len(output_gene)))
# print('miRNA duplicates removed: ' + str(len(output_mirna)))

'''
map_dict : Contains miRNA names as keys and their target genes as values.
Maps miRNA to their target genes.
'''

def mirna_mapper():
	for i, j in enumerate(mirna):
		map_dict.setdefault(j, []).append(genes[i])
		# if i == 25:
		# 	break
	jsonify(map_dict, 'mirna_map_dict.json')
	return map_dict

def gene_mapper():
	for i, j in enumerate(genes):
		pass

# Export dictionary to JSON for showing count in a presentable form.
def jsonify(dict, location=None):
	a = json.dumps(dict, sort_keys=True, indent=4, separators=(',', ': '))
	filename = str(location.split('.')[0])
	if location == None:
		with open('map_dict.json', 'w') as outfile:
			outfile.write(a)
	else:
		with open(str(location), 'a+') as outfile:
			outfile.write(a)
		with open(str(filename) + '.py', 'a+') as outfile:
			outfile.write(filename + ' = ')
			outfile.write(a)
	# print(a)

if __name__ == '__main__':
	map_dict = {}
	genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
	mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
	# print('Genes original: ' + str(len(genes)))
	# print('miRNA original: ' + str(len(mirna)))
	mirna_map_dict = mirna_mapper()
