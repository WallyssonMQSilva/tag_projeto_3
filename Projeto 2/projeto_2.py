import os
import networkx as nx
import random

def ler_arquivo(nome_arquivo):
    """
    Lê o arquivo de entrada e retorna os dados de projetos e alunos.
    """
    projetos = {}
    alunos = {}

    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    secao_projetos = True

    for linha in linhas:
        linha = linha.strip()

        if not linha or linha.startswith('//'):
            continue

        if linha.startswith('(A'):
            secao_projetos = False

        if secao_projetos:
            partes = linha.strip('()').split(', ')
            codigo = partes[0]
            vagas = int(partes[1])
            requisito = int(partes[2])
            projetos[codigo] = {'vagas': vagas, 'requisito': requisito}
        else:
            aluno, resto = linha.split(':')
            preferencias, nota = resto.split(') (')
            preferencias = preferencias.strip('()').split(', ')
            nota = int(nota.strip(')'))
            alunos[aluno] = {'preferencias': preferencias, 'nota': nota}

    return projetos, alunos

def criar_grafo(projetos, alunos):
    """
    Cria um grafo bipartido com base nos projetos e alunos fornecidos.
    """
    G = nx.Graph()

    # Adiciona os nós de projetos
    for projeto in projetos:
        G.add_node(projeto, bipartite=0)

    # Adiciona os nós de alunos
    for aluno in alunos:
        G.add_node(aluno, bipartite=1)

    # Adiciona as arestas entre alunos e projetos, conforme as preferências e requisitos
    for aluno, dados in alunos.items():
        nota_aluno = dados['nota']
        for projeto in dados['preferencias']:
            if projeto in projetos and nota_aluno >= projetos[projeto]['requisito']:
                G.add_edge(aluno, projeto)

    return G

def gale_shapley(projetos, alunos, G, ordem_alunos, aluno_inicio):
    """
    Implementa o algoritmo de Gale-Shapley para encontrar um emparelhamento estável.
    """
    alocacao = {}
    vagas_disponiveis = {p: projetos[p]['vagas'] for p in projetos}
    preferencia_alunos = {a: list(alunos[a]['preferencias']) for a in alunos}  # Cópia das preferências para não modificar o original

    # Reorganizar a lista de alunos para começar a partir de aluno_inicio
    indice_inicio = ordem_alunos.index(aluno_inicio)
    alunos_livres = ordem_alunos[indice_inicio:] + ordem_alunos[:indice_inicio]
    alunos_livres = set(alunos_livres)

    projeto_atual = {p: [] for p in projetos}

    while alunos_livres:
        aluno = alunos_livres.pop()
        while preferencia_alunos[aluno]:
            projeto = preferencia_alunos[aluno].pop(0)
            if not G.has_edge(aluno, projeto):
                continue

            if len(projeto_atual[projeto]) < vagas_disponiveis[projeto]:
                projeto_atual[projeto].append(aluno)
                alocacao[aluno] = projeto
                break
            else:
                pior_aluno = min(projeto_atual[projeto], key=lambda x: alunos[x]['nota'])
                if alunos[aluno]['nota'] > alunos[pior_aluno]['nota']:
                    projeto_atual[projeto].remove(pior_aluno)
                    projeto_atual[projeto].append(aluno)
                    alocacao[aluno] = projeto
                    alunos_livres.add(pior_aluno)
                    break

    return alocacao, sum(len(projeto_atual[projeto]) for projeto in projeto_atual)

def emparelhamento_maximo_estavel(projetos, alunos):
    """
    Encontra o emparelhamento máximo e estável, realizando múltiplas iterações.
    """
    melhor_alocacao = {}
    max_vagas = 0
    melhor_iteracao = 0

    for i in range(10):
        print(f"Iteração {i + 1}:")

        # Criar o grafo com a ordem fixa de preferências
        G = criar_grafo(projetos, alunos)

        # Escolher um aluno aleatório para começar
        ordem_alunos = list(alunos.keys())
        aluno_inicio = random.choice(ordem_alunos)
        print(f"Aluno inicial: {aluno_inicio}")

        # Executar o algoritmo Gale-Shapley
        alocacao, num_vagas = gale_shapley(projetos, alunos, G, ordem_alunos, aluno_inicio)

        print(f"Alocação da iteração {i + 1}: {alocacao}")
        print(f"Vagas preenchidas: {num_vagas}\n")

        if num_vagas > max_vagas:
            max_vagas = num_vagas
            melhor_alocacao = alocacao
            melhor_iteracao = i + 1

    print(f"Melhor iteração: {melhor_iteracao} com {max_vagas} vagas preenchidas\n")
    return melhor_iteracao, max_vagas, melhor_alocacao

def main():
    """
    Função principal que executa o programa.
    """
    diretorio = os.path.dirname(__file__)
    arquivo_txt = os.path.join(diretorio, "entradaProj2.24TAG.txt")

    projetos, alunos = ler_arquivo(arquivo_txt)
    melhor_iteracao, max_vagas, melhor_alocacao = emparelhamento_maximo_estavel(projetos, alunos)

    print("Melhor Emparelhamento Estável:")
    for aluno, projeto in melhor_alocacao.items():
        print(f"{aluno} -> {projeto}")
    print(f"Número total de vagas alocadas na melhor iteração: {max_vagas}")

if __name__ == "__main__":
    main()
