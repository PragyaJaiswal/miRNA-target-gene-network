import urllib
import json
import re

def convert(genes, mirna, location=None):
	for x, y in zip(genes, mirna):
		print(x)
		url = 'http://biodbnet.abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json?method=dbfind&inputValues=' + str(x) + '&output=ensemblgeneid&taxonId=9606&format=row'
		u = urllib.urlopen(url)
		response = u.read()
		find(response)
		# jsonify(response, location)

def jsonify(response, filename):
	with open(str(filename) + '.json', 'a+') as outfile:
		outfile.write(response)

def find(response):
	out = str.replace(response, '\n', '')
	list = out.split()
	for x in list:
		if re.search('ENSG', str.replace(x, '"', '')):
			with open('./dat/hsa/ensemblIDs', 'a+') as outfile:
				outfile.write(str.replace(x, '"', '') + '\n')

if __name__ == '__main__':
	genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
	mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
	convert(genes, mirna, './dat/hsa/IDmapper')