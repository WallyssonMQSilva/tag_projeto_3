import networkx as nx
import matplotlib.pyplot as plt

def visualizar(grafo, title, cores=None):
	if not cores:
		cores = ['white' for i in grafo]
	arestas = []
	for i in grafo:
		for j in grafo[i]:
			if i < j:
				arestas.append((i, j)) #colocar arestas bidirecionais apenas uma vez
	
	G = nx.Graph(arestas)
	nodelist = [v for v in grafo]
	node_size = 50
	node_color = [cores[i] for i in grafo]
	width = 0.8
	edgelist = arestas
	font_size = 5
	label = title
	nx.draw_networkx(G,
		pos=nx.circular_layout(G),
		nodelist=nodelist,
		node_size=node_size,
		node_color=node_color,
		width=width,
		edgelist=edgelist,
		font_size=font_size,
		label=label
	)
	plt.show()