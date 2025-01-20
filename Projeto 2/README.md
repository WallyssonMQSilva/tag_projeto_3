Descrição

Este projeto implementa uma variação do algoritmo de Gale-Shapley para emparelhamento estável entre alunos e projetos. A cada iteração, um aluno é escolhido aleatoriamente como ponto de partida, permitindo diferentes configurações de alocação.

Instalação e Execução

1. Dependências

Este código utiliza as bibliotecas:

networkx para manipulação de grafos

random para seleção aleatória de alunos

os para manipulação de arquivos

Caso ainda não tenha o networkx instalado, execute:

pip install networkx

2. Execução do programa

Coloque o arquivo de entrada entradaProj2.24TAG.txt no mesmo diretório do script e execute:

python nome_do_arquivo.py

Estrutura do Código

Principais Funções

ler_arquivo(nome_arquivo): Lê o arquivo de entrada e retorna os dados de projetos e alunos.

criar_grafo(projetos, alunos): Cria um grafo bipartido baseado nas preferências e requisitos.

gale_shapley(projetos, alunos, G, ordem_alunos, aluno_inicio): Implementa o algoritmo de Gale-Shapley.

emparelhamento_maximo_estavel(projetos, alunos): Realiza várias execuções do Gale-Shapley e retorna a melhor alocação.

main(): Função principal que coordena a execução.

Variação do Algoritmo de Gale-Shapley

Diferentemente do algoritmo tradicional, onde a ordem de execução dos alunos é fixa, esta implementação:

Escolhe um aluno aleatório a cada iteração para iniciar o processo.

Mantém a ordem de preferência dos alunos e projetos, mas altera a ordem de processamento.

Repete o processo por 10 iterações para encontrar a melhor solução (com maior preenchimento de vagas).