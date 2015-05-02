import os, sys

'''
.xls data from mirTarBase. 'http://mirtarbase.mbc.nctu.edu.tw/index.php'
Implemented for miRNA target genes in homo sapiens.
597 miRNA and 12105 target genes.
'''

genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
# print(genes)

print('Genes original: ' + str(len(genes)))
print('miRNA original: ' + str(len(mirna)))

def remove_duplicates(viruses):
	output = []
	visited = set()
	for virus in viruses:
		if virus not in visited:
			output.append(virus)
			visited.add(virus)
	return output

output_gene = remove_duplicates(genes)
output_mirna = remove_duplicates(mirna)
print('Gene duplicates removed: ' + str(len(output_gene)))
print('miRNA duplicates removed: ' + str(len(output_mirna)))

# if __name__ == '__main__':
# 	main()