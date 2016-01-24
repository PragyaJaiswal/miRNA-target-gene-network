import os, sys, json

'''
.xls data from mirTarBase. 'http://mirtarbase.mbc.nctu.edu.tw/index.php' v4.5
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
def mapper(item, name, other_item, text):
	dictionary = {}
	# abc = item.name()
	for i, j in enumerate(item):
		dictionary.setdefault(j, []).append(other_item[i])
		# dictionary.setdefault(j, []).append(another_item[i])
	jsonify(dictionary, str(name) + '.json')
	jsonify(dictionary, str(name) + '.py', text)
	return dictionary

'''
Export dictionary to JSON for showing count in a presentable form.
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
	mirna_dict = {}
	target_dict = {}
	genes = open('./dat/hsa/target_gene_new_release.txt', 'r').read().splitlines()
	mirna = open('./dat/hsa/miRNA_new_release.txt', 'r').read().splitlines()
	ensemblIDs = open('./dat/hsa/ensemblIDs.txt', 'r').read().splitlines()
	# print('Genes original: ' + str(len(genes)))
	# print('miRNA original: ' + str(len(mirna)))
	mirna_dict = mapper(mirna, 'mirna_map_dict_new_release', genes, 'mirna_map_dict')
	target_dict = mapper(genes, 'target_gene_map_dict_new_release', mirna, 'target_gene_map_dict')
