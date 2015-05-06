import networkx as nx
import matplotlib.pyplot as plt
from mirna_map_dict import mirna_map_dict
from target_gene_map_dict import target_gene_map_dict
import itertools

def call(mi):
	for i in target_gene_map_dict:
		print(i)
		print(type(target_gene_map_dict[x]))
		if mi in target_gene_map_dict[x]:
			print(mi)
			# return (True, i)

if __name__ == '__main__':
	flag = False
	print(len(target_gene_map_dict))
	g = nx.Graph()
	g.add_nodes_from(mirna_map_dict.keys(), color = 'red')
	print(g.nodes())
	print(g.order())
	g.add_nodes_from(target_gene_map_dict.keys(), color = 'blue')
	print(g.nodes())
	print(g.order())
	# for x in mirna_map_dict.keys():
	# 	targets = len(mirna_map_dict[x])
	# 	g.add_nodes_from()
	# 	break


# G = nx.star_graph(targets)
# pos = nx.spring_layout(G)
# colors = range(targets)
# nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors, width=4, edge_cmap=plt.cm.Reds, with_labels=False)
# plt.savefig('edge_colormap.png')
# plt.show()g