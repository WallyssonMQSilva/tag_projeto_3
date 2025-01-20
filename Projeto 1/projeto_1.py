import os
import networkx as nx

# Função para ler o arquivo e retornar as linhas válidas
def ler_arquivo(arquivo):
    with open(arquivo, "r") as f:
        linhas = f.readlines()
    linhas_validas = [linha.strip() for linha in linhas if not linha.startswith("%")]
    return linhas_validas

# Função para extrair informações iniciais do grafo
def extrair_informacoes(linhas_validas):
    num_nos, _, num_arestas = map(int, linhas_validas.pop(0).split())
    return num_nos, num_arestas

# Função para criar o grafo com NetworkX
def criar_grafo(linhas_validas):
    return nx.parse_edgelist(linhas_validas, nodetype=int)

# Função para criar a lista de adjacências
def criar_lista_adjacencia(linhas_validas):
    lista_adjacencia = {}
    for linha in linhas_validas:
        u, v = map(int, linha.split())  
        if u not in lista_adjacencia:
            lista_adjacencia[u] = []
        lista_adjacencia[u].append(v)
        if v not in lista_adjacencia:
            lista_adjacencia[v] = []
        lista_adjacencia[v].append(u)
    return lista_adjacencia

# Função para exibir o grau de cada vértice
def exibir_grau(lista_adjacencia):
    print("Lista de adjacências e graus:")
    for vertice, adjacentes in lista_adjacencia.items():
        grau = len(adjacentes)
        print(f"Vértice {vertice}: Grau {grau}")

# Função para econtrar os cliques maximais
def bron_kerbosch(R, P, X, lista_adjacencia, cliques_maximais):
    if not P and not X:
        cliques_maximais.append(R)
        return

    for v in list(P):
        bron_kerbosch(
            R.union({v}),
            P.intersection(lista_adjacencia[v]),
            X.intersection(lista_adjacencia[v]),
            lista_adjacencia,
            cliques_maximais
        )
        P.remove(v)
        X.add(v)

# Função principal
def main():
    diretorio = os.path.dirname(__file__)  
    arquivo_mtx = os.path.join(diretorio, "soc-dolphins.mtx")

    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_mtx):
        raise FileNotFoundError(f"Arquivo .mtx não encontrado no caminho: {arquivo_mtx}")

    #Ler o arquivo
    linhas_validas = ler_arquivo(arquivo_mtx)

    #Extrair informações iniciais
    num_nos, num_arestas = extrair_informacoes(linhas_validas)

    #Criar o grafo usando NetworkX
    grafo = criar_grafo(linhas_validas)

    # Exibir informações do grafo
    print(f"Número de nós: {grafo.number_of_nodes()}")
    print(f"Número de arestas: {grafo.number_of_edges()}")

    #Criar a lista de adjacências
    lista_adjacencia = criar_lista_adjacencia(linhas_validas)

    #Exibir grau de cada vértice
    exibir_grau(lista_adjacencia)

    #Encontrar cliques maximais usando o algoritmo Bron-Kerbosch
    cliques_maximais = []
    R = set()  # Conjunto vazio
    P = set(lista_adjacencia.keys())  # Todos os vértices no início
    X = set()  # Conjunto vazio

    bron_kerbosch(R, P, X, lista_adjacencia, cliques_maximais)

    #Exibir os cliques maximais encontrados
    print("\nCliques maximais encontrados:")
    for clique in cliques_maximais:
        print(f"Clique com {len(clique)} vértices: {sorted(clique)}")

if __name__ == "__main__":
    main()
