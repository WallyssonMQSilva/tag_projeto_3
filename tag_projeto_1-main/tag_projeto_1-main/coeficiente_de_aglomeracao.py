"""Este módulo contém funções para calcular o coeficiente de aglomeração dos
vértices em um grafo e também calcular o coeficiente de aglomeração médio do grafo."""

def coeficiente_de_aglomeracao(lista_adjacencias, vertice):
    """Retorna o coeficiente de aglomeração de um vértice."""
    vizinhos = lista_adjacencias[vertice] #vizinhos do vértice "vertice"
    n = len(vizinhos) #quantidade de vizinhos
    t = 0 #quantidade de "triângulos": arestas entre vizinhos de um vértice
    if n < 2:
        return 0.0 #não há como formar nenhum triâgulo com 1 ou 0 vizinhos
    for v1 in vizinhos:
        for v2 in vizinhos:
            if v1 < v2 and v1 in lista_adjacencias[v2]: #verificamos v1<v2 para evitar contar todos os triângulos duas vezes
                t += 1
    return (2*t)/(n*(n-1)) #fórmula do coeficiente de aglomeração

def coeficiente_medio_de_aglomeracao(lista_adjacencias):
    """Retorna o coeficiente de médio de aglomeração do grafo."""
    soma = 0 #soma dos coeficientes de aglomeração dos vértices
    quantidade = 0 #número de vértices no grafo
    for vertice in lista_adjacencias:
        soma += coeficiente_de_aglomeracao(lista_adjacencias, vertice)
        quantidade += 1
    return soma/quantidade #retorna a média dos coeficientes de aglomeração dos vértices do grafo
         
if __name__ == "__main__":
    g = {'A': ['H'],
         'B': ['D', 'G', 'J', 'C', 'I'],
         'C': ['B', 'F', 'J'],
         'D': ['B'],
         'E': [],
         'F': ['C'],
         'G': ['B'],
         'H': ['A'],
         'I': ['B'],
         'J': ['B', 'C']
         }
    for v in g:
        print(coeficiente_de_aglomeracao(g, v))
    print(coeficiente_medio_de_aglomeracao(g))
