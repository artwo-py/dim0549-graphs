"""
Módulo:    is_bipartite
Descriçao: Contém o algoritmo para determinar se um grafo é bipartido.
Funções:   - is_bipartite(grafo): Verifica a bipartição de um grafo.
"""
import collections
from lib.core.graph import Grafo

def is_bipartite(grafo: Grafo) -> bool:
    """
    Tarefa: (extra) Determina se o grafo é bipartido.
    Info: Usa um algoritmo de coloração com BFS. Um grafo é bipartido se puder ser
          dividido em dois conjuntos de vértices disjuntos, U e V, tal que toda
          aresta conecta um vértice em U a um em V.
    E: grafo (Grafo) - O objeto Grafo a ser analisado.
    S: bool - True se o grafo for bipartido, False caso contrário.
    """
    if not grafo.vertices:
        return True

    cores = {}  # 0: não visitado, 1: cor A, -1: cor B
    for v_inicial in grafo.vertices:
        if v_inicial not in cores:
            cores[v_inicial] = 1
            fila = collections.deque([v_inicial])

            while fila:
                u = fila.popleft()

                # Usa a lista de adjacência do grafo para encontrar vizinhos
                for v_vizinho in grafo.lista_adj.get(u, []):
                    if v_vizinho not in cores:
                        cores[v_vizinho] = -cores[u]
                        fila.append(v_vizinho)
                    elif cores[v_vizinho] == cores[u]:
                        return False
    return True