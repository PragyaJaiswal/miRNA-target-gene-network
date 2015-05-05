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
mirna_map_dict : Contains miRNA names as keys and their target genes as values.
Maps miRNA to their target genes.

target_gene_map_dict : Contains target genes as names and the miRNAs that target them as values.
Maps target genes to their miRNAs.
'''

def mapper(item, name, other_item):
	dictionary = {}
	# abc = item.name()
	for i, j in enumerate(item):
		dictionary.setdefault(j, []).append(other_item[i])
	jsonify(dictionary, str(name) + '.json')
	return dictionary

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


if __name__ == '__main__':
	mirna_dict = {}
	target_dict = {}
	genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
	mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
	# print('Genes original: ' + str(len(genes)))
	# print('miRNA original: ' + str(len(mirna)))
	mirna_dict = mapper(mirna, 'mirna_map_dict', genes)
	target_dict = mapper(genes, 'target_gene_map_dict', mirna)
