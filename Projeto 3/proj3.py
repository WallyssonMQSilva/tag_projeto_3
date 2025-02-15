import networkx as nx

def criar_grafo_rodadas(times):
    """Cria um grafo bipartido de jogos e rodadas."""
    G = nx.Graph()

    # Criação dos jogos (ida e volta)
    jogos = []
    for i in range(len(times)):
        for j in range(i + 1, len(times)):
            jogo_ida = (times[i], times[j])
            jogo_volta = (times[j], times[i])
            jogos.append(jogo_ida)
            jogos.append(jogo_volta)

    # Nós das rodadas
    rodadas = [f"R{i+1}" for i in range(14)]

    G.add_nodes_from(jogos, bipartite=0)  # Jogos são um conjunto
    G.add_nodes_from(rodadas, bipartite=1)  # Rodadas são outro conjunto

    return G, jogos, rodadas

def verifica_restricoes(jogo, rodada, coloracao, restricoes):
    """Verifica se um jogo pode ser colocado em uma rodada considerando as restrições."""
    mandante, visitante = jogo
    rodada_num = int(rodada[1:])

    # Verificar se existe restrição específica para este jogo
    if (mandante, visitante) in restricoes and rodada_num in restricoes[(mandante, visitante)]:
        return False  

    # Restrições de mando de campo
    for (time1, cond1), (time2, cond2) in restricoes.items():
        if cond1 == "_" and cond2 == "_":
            if mandante == time1 or visitante == time1:
                for outro_jogo, r in coloracao.items():
                    if r == rodada and (outro_jogo[0] == time2 or outro_jogo[1] == time2):
                        return False  

    # Impedir que um time jogue mais de uma vez na mesma rodada
    for outro_jogo, r in coloracao.items():
        if r == rodada and (mandante in outro_jogo or visitante in outro_jogo):
            return False  

    return True  

def guloso_coloring(G, jogos, rodadas, restricoes):
    """Aplica o algoritmo guloso considerando as restrições e balanceando os jogos nas rodadas."""
    coloracao = {}

    # Distribuir os jogos entre as rodadas de maneira balanceada
    rodada_atual = 0
    for jogo in jogos:
        alocado = False
        tentativas = 0
        
        while not alocado and tentativas < len(rodadas):
            rodada = rodadas[rodada_atual]

            if verifica_restricoes(jogo, rodada, coloracao, restricoes):
                coloracao[jogo] = rodada
                alocado = True

            rodada_atual = (rodada_atual + 1) % len(rodadas)  
            tentativas += 1

    return coloracao

def main():
    times = ["DFC", "TFC", "AFC", "LFC", "FFC", "OFC", "CFC"]

    restricoes = {
        ("DFC", "CFC"): {1, 14},
        ("TFC", "_"): ("OFC", "_"),
        ("AFC", "_"): ("FFC", "_"),
        ("LFC", "FFC"): {7, 13},
        ("OFC", "LFC"): {10, 11},
        ("OFC", "FFC"): {12, 13},
        ("CFC", "TFC"): {2, 3}
    }

    # Criação do grafo de rodadas e jogos
    G, jogos, rodadas = criar_grafo_rodadas(times)

    # Aplicação do algoritmo guloso considerando restrições
    distribuicao = guloso_coloring(G, jogos, rodadas, restricoes)

    # Exibição a tabela de jogos e rodadas
    print("\n Distribuição dos Jogos nas 14 Rodadas:")
    for jogo, rodada in sorted(distribuicao.items(), key=lambda x: int(x[1][1:])):
        print(f"{rodada}: {jogo[0]} x {jogo[1]}")


if __name__ == "__main__":
    main()
