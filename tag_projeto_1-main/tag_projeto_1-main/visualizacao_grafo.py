"""Este módulo é responsável por gerar a visualização de um grafo, destacando
por cores seus cliques maximais."""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import random

plot_colors = list(colors.CSS4_COLORS)
plot_colors.remove('black')
plot_colors.remove('white')
random.shuffle(plot_colors)

def visualizar_cliques(lista_adjacencias, cliques_maximais):
    """Gera, usando as bibliotecas networkx e matplotlib, uma visualização do grafo
de forma que os cliques maximais sejam distinguidos por cores diferentes."""
    #conferimos se há cores suficientes para pintar todos os cliques maximais de forma distinta
    assert len(cliques_maximais) <= len(plot_colors)
    #associamos uma cor a cada clique maximal
    cor_clique = {i: plot_colors[i] for i in range(len(cliques_maximais))}
    
    #montagem da lista das arestas do grafo
    arestas = []
    posicao_aresta = {} #iremos precisar recuperar a posição de cada aresta na lista
    for vertice in lista_adjacencias:
        for vizinho in lista_adjacencias[vertice]:
            if vertice < vizinho: #colocamos cada aresta apenas uma vez, em vez de duas, na lista
                posicao_aresta[(vertice, vizinho)] = len(arestas)
                arestas.append((vertice, vizinho))

    #guardaremos pra todo vértice e aresta os cliques maximais aos quais pertence
    cliques_aresta = {a: [] for a in arestas}
    cliques_vertice = {v: [] for v in lista_adjacencias}
    for i in range(len(cliques_maximais)): #iteramos todos os cliques maximais
        clique = cliques_maximais[i]
        for v1 in clique:
            cliques_vertice[v1].append(i) #todo vértice do clique está neste clique maximal
            for v2 in clique: #iteramos todos os pares de vértices dentro do clique maximal
                if v1 < v2:
                    cliques_aresta[(v1, v2)].append(i) #toda aresta do clique está neste clique maximal

    #registro dos argumentos para o método de visualização da networkx
    G = nx.Graph(arestas) #grafo networkx
    nodelist = [v for v in lista_adjacencias] #lista dos vértices
    node_size = 50 #tamanho dos vértices
    #cada vértice pode estar em muitos cliques maximais, então iremos usar a cor do último clique do qual participa
    node_color = [cor_clique[cliques_vertice[v][-1]] for v in nodelist]
    width = 0.8 #espessura das arestas
    edgelist = arestas #lista das arestas
    #cada aresta pode fazer parte de muitos cliques maximais, então iremos usar a cor do primeiro (diferenciando dos vértices)
    edge_color = list(range(len(arestas)))
    for a in arestas:
        edge_color[posicao_aresta[a]] = cor_clique[cliques_aresta[a][0]]
    font_size = 5 #fonte da visualização
    label = "Visualização dos cliques maximais do grafo" #título
    nx.draw_networkx(G,
                     pos=nx.forceatlas2_layout(G,scaling_ratio=1.0), #posicionamento dos vértices
                     nodelist=nodelist,
                     node_size=node_size,
                     node_color=node_color,
                     width=width,
                     edgelist=edgelist,
                     edge_color=edge_color,
                     font_size=font_size,
                     label=label
                     ) #função de visualização da networkx
    plt.show() #comando matplotlib para exibir a visualização
    

if __name__ == "__main__":
    g = {'A': ['H'],
         'B': ['D', 'G', 'J', 'C', 'I'],
         'C': ['B', 'F', 'J'],
         'D': ['B'],
         #'E': [],
         'F': ['C'],
         'G': ['B'],
         'H': ['A'],
         'I': ['B'],
         'J': ['B', 'C']
         }
    cliques = [
        ['A','H'],
        ['B','D'],
        #['E'],
        ['I','B'],
        ['G','B'],
        ['B','C','J'],
        ['F','C']
        ]
    visualizar_cliques(g, cliques)
