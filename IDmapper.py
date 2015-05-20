import urllib
import json

def convert(genes, mirna, location=None):
	for x, y in zip(genes, mirna):
		print(x)
		url = 'http://biodbnet.abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.json?method=dbfind&inputValues=' + str(x) + '&output=ensemblgeneid&taxonId=9606&format=row'
		u = urllib.urlopen(url)
		response = u.read()
		jsonify(response, location)

def jsonify(response, filename):
	with open(str(filename) + '.json', 'a+') as outfile:
		outfile.write(response)


if __name__ == '__main__':
	genes = open('./dat/hsa/target gene.txt', 'r').read().splitlines()
	mirna = open('./dat/hsa/miRNA.txt', 'r').read().splitlines()
	convert(genes, mirna, 'IDmapper')