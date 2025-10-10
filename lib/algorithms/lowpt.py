"""
Módulo:    lowpt (Biconectividade)
Objetivo:  Implementa o algoritmo de Tarjan para encontrar pontos de articulação
           e pontes em um grafo não-direcionado.
Funções:   - find_articulations_and_bridges(grafo)
"""
from lib.core.graph import Grafo

def lowpt(grafo: Grafo):
    """
    Tarefa: (15) Determinação de articulações e pontes.
    Info: Encontra pontos de articulação e pontes em um grafo usando o
          algoritmo de Tarjan, que se baseia em uma DFS e nos valores de
          tempo de descoberta (d) e low-link (lowpt).
          O algoritmo opera em grafos não-direcionados. Se um dígrafo for
          passado, a análise será feita em seu grafo subjacente.

    E: grafo (Grafo) - O objeto Grafo a ser analisado.
    S: (set, set) - Uma tupla contendo:
                    - Um conjunto com os IDs dos vértices de articulação.
                    - Um conjunto de tuplas representando as pontes.
    """
    if grafo.direcionado:
        print("Aviso: O algoritmo de biconectividade opera sobre o grafo subjacente não-direcionado.")

    adj = grafo.lista_adj
    todos_vertices = grafo.vertices
    
    visitados = set()
    tempos_descoberta = {}
    low_link = {} 
    parentes = {}
    
    pontos_articulacao = set()
    pontes = set()
    tempo = 0

    def dfs_visit(u):
        nonlocal tempo
        visitados.add(u)
        
        tempo += 1
        tempos_descoberta[u] = tempo
        low_link[u] = tempo
        
        filhos_dfs = 0

        for v in adj.get(u, []):
            if v == parentes.get(u):
                continue

            if v in visitados:
                low_link[u] = min(low_link[u], tempos_descoberta[v])
            else:
                parentes[v] = u
                filhos_dfs += 1
                dfs_visit(v)

                low_link[u] = min(low_link[u], low_link[v])

                if parentes.get(u) is None and filhos_dfs > 1:
                    pontos_articulacao.add(u.id)
                
                if parentes.get(u) is not None and low_link[v] >= tempos_descoberta[u]:
                    pontos_articulacao.add(u.id)

                if low_link[v] > tempos_descoberta[u]:
                    aresta_ordenada = tuple(sorted((str(u.id), str(v.id))))
                    pontes.add(aresta_ordenada)

    for vertice in todos_vertices:
        if vertice not in visitados:
            dfs_visit(vertice)

    return pontos_articulacao, pontes