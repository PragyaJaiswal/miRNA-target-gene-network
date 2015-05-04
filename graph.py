import networkx as nx
import matplotlib.pyplot as plt
from map_dict import map_dict

G = nx.star_graph(10)
pos = nx.spring_layout(G)
colors = range(10)
nx.draw(G, pos, node_color='#A0CBE2', edge_color=colors, width=4, edge_cmap=plt.cm.Reds, with_labels=False)
# plt.savefig('edge_colormap.png')
plt.show()