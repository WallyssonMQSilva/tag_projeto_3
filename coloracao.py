import matplotlib.colors as colors
import random

plot_colors = list(colors.CSS4_COLORS)
plot_colors.remove('black')
plot_colors.remove('white')
random.shuffle(plot_colors)


'''def f(v):
	if v == -1:
		return True
	cp = set()
	for adj in grafo[v]:
		cp.add(cor_vertice[adj])
	for c in cores:
		if not c in cp:
			cor_vertice[v] = c
			if f(v-1):
				return True
			else:
				cor_vertice[v] = -1
	else:
		return False
		
if f(pilha[-1]):
	return cor_vertice
else:
	return []'''


def coloracao(grafo, max_cores):
	#retorna uma coloracao valida do grafo
	#grafo tem identificadores consecutivos iniciando em 0
	cor_vertice = [-1 for i in range(len(grafo))] #cor comeca em 0
	pilha = list(grafo.keys()) #pilha de vertices a serem analisados
	cores = plot_colors[0:max_cores] #cores a serem usadas
	cores_ja_testadas = [set() for i in range(len(grafo))] #cores ja testadas no vertice na iteracao atual
	
	while len(pilha):
		v = pilha[-1] #vertice atual
		if v == len(grafo):
			return [] #nao achamos coloracao com essa quantidade de cores
			
		cor_vertice[v] = -1 #tentar colorir o vertice atual
		cores_proibidas = set() #nao usar cores dos vizinhos e ja testadas por esse vertice
		
		for adj in grafo[v]:
			cores_proibidas.add(cor_vertice[adj])
		for c in cores_ja_testadas[v]:
			cores_proibidas.add(c)
		
		for c in cores:
			if not c in cores_proibidas:
				cor_vertice[v] = c
				cores_ja_testadas[v].add(c)
				pilha.pop()
				break
				
		if cor_vertice[v] == -1:
			cores_ja_testadas[v] = set() #vamos retestar as cores
			pilha.append(v+1) #voltamos a testar com o vertice anterior
	
	return cor_vertice
				
		