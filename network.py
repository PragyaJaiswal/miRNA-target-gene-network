import os, sys

'''
.xls data from mirTarBase. 'http://mirtarbase.mbc.nctu.edu.tw/index.php'
Implemented for miRNA target genes in homo sapiens.
596 miRNA and 12104 target genes.
'''

genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
# print(genes)

print('Genes original: ' + str(len(genes)))
print('miRNA original: ' + str(len(mirna)))

# def remove_duplicates(viruses):
# 	output = []
# 	visited = set()
# 	for virus in viruses:
# 		if virus not in visited:
# 			output.append(virus)
# 			visited.add(virus)
# 	return output

# output_gene = remove_duplicates(genes)
# output_mirna = remove_duplicates(mirna)
# print('Gene duplicates removed: ' + str(len(output_gene)))
# print('miRNA duplicates removed: ' + str(len(output_mirna)))


def find_target(mirna, genes):
	target = {}
	c = 0
	# i is the index number
	# j is the element at that index
	for x in mirna:
		c+=1
		p = 0
		print('Iteration: ' + str(c))
		for i, j in enumerate(mirna):
			p+=1
			# print('Iteration: ' + str(p) + ' of ' + str(c))
			if j == str(x) and j not in target.keys():
				print(str(j) + ': ' + str(i))
				target[j] = genes[i]
		# if c == '25':
		# 	break
	return target

if __name__ == '__main__':
	target = find_target(mirna, genes)
	print(target)
	print(len(target))
	# find(target)