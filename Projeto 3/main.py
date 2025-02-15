import coloracao

def montagem_grafo(times, partidas, rodadas, restricoes_mandantes, restricoes_rodadas):
	#todo vertice no grafo recebera um identificador numerico
    #vertice de partida: posicao na lista de partidas
    #vertice de rodadas: len(partidas) + posicao na lista de rodadas
    
    id_num = {} #identificador do vertice
    for i in range(len(partidas)):
    	id_num[partidas[i]] = i
    for i in range(len(rodadas)):
    	id_num[rodadas[i]] = i + len(partidas)
    valor_vertice = [] #valor do vertice
    for i in range(len(partidas)):
    	valor_vertice.append(partidas[i])
    for i in range(len(rodadas)):
    	valor_vertice.append(rodadas[i])
    
    grafo = {x: [] for x in range(len(partidas)+len(rodadas))} #lista de adjacencias
    def add_aresta(v1, v2): #adiciona uma aresta bidirecional no grafo
    	a, b = id_num[v1], id_num[v2]
    	grafo[a].append(b)
    	grafo[b].append(a)
		
    #vertices tem aresta se nao podem estar na mesma rodada
    for i in range(len(partidas)):
    	for j in range(i+1, len(partidas)): #passar por todo par apenas uma vez
    		tem_aresta = False
    		m1, v1 = partidas[i]
    		m2, v2 = partidas[j]
    		if m1 == m2 or m1 == v2 or v1 == m2 or v1 == v2:
    			tem_aresta = True #times em comum nas partidas
    		for a, b in restricoes_mandantes:
    			if m1 == a and m2 == b:
    				tem_aresta = True #restricoes de times mandantes pela liga
    		if tem_aresta:
    			add_aresta(partidas[i], partidas[j])
    	for j in range(len(rodadas)):
    		tem_aresta = False
    		for a, b in restricoes_rodadas:
    			if partidas[i] == a and rodadas[j] == b: #restricoes de rodadas da liga
    				tem_aresta = True
    		if tem_aresta:
    			add_aresta(partidas[i], rodadas[j])
    for i in range(len(rodadas)):
    	for j in range(i+1, len(rodadas)): #passar por todo par apenas uma vez
    		add_aresta(rodadas[i], rodadas[j]) #rodadas formam um clique
    		
    return grafo, id_num, valor_vertice #grafo montado

def main():
	
    times = ["DFC", "TFC", "AFC", "LFC", "FFC", "OFC", "CFC"] #lista dos times
    partidas = [] #lista das partidas
    for i in range(0, len(times)):
    	for j in range(0, len(times)):
    		if i != j:
    			partidas.append((times[i], times[j]))
    rodadas = [i+1 for i in range(14)] #lista das rodadas
    
    #restricoes da liga
    restricoes_mandantes = [
    	("TFC", "OFC"),
    	("AFC", "FFC")
    ]
    
    restricoes_rodadas = [
    	(("DFC", "CFC"), 1),
    	(("DFC", "CFC"), 14),
    	(("LFC", "FFC"), 7),
    	(("LFC", "FFC"), 13),
    	(("OFC", "LFC"), 10),
    	(("OFC", "LFC"), 11),
    	(("AFC", "FFC"), 12),
    	(("AFC", "FFC"), 13),
    	(("CFC", "TFC"), 2),
    	(("CFC", "TFC"), 3)
    ]
    
    grafo, v_to_id, id_to_v = montagem_grafo(times, partidas, rodadas, restricoes_mandantes, restricoes_rodadas)
    
    cores = coloracao.coloracao(grafo, 14)
    for i in range(len(rodadas)):
    	print("Rodada", rodadas[i])
    	for j in range(len(grafo)):
    		if cores[j] == cores[v_to_id[rodadas[i]]]:
    			print(id_to_v[j])
    	print()


if __name__ == "__main__":
    main()
    