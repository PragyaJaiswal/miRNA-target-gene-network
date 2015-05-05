import networkx as nx
import matplotlib.pyplot as plt
from mirna_map_dict import mirna_map_dict

for x in mirna_map_dict.keys():
	targets = len(mirna_map_dict[x])
	G = nx.star_graph(targets)
	pos = nx.spring_layout(G)
	colors = range(targets)
	nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors, width=4, edge_cmap=plt.cm.Reds, with_labels=False)
	# plt.savefig('edge_colormap.png')
	plt.show()
	break