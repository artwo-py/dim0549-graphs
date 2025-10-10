"""
Módulo:    is_adjacent
Descriçao: Contém algoritmos para verificar a adjacência entre vértices
           usando as diferentes representações de dados de um grafo.
"""
from lib.core.graph import Grafo

def are_adjacent_by_list(grafo: Grafo, v1_id, v2_id) -> bool:
    """
    Info: Verifica se dois vértices são adjacentes usando a LISTA de adjacência.
    E: grafo (Grafo), v1_id (str/int), v2_id (str/int)
    S: bool - True se forem adjacentes, False caso contrário.
    """
    try:
        v1 = grafo.indice_vertices[str(v1_id)]
        v2 = grafo.indice_vertices[str(v2_id)]

        if v2 in grafo.lista_adj.get(v1, []):
            return True
        if not grafo.direcionado and v1 in grafo.lista_adj.get(v2, []):
            return True
            
    except KeyError:
        return False
    return False

def are_adjacent_by_adj_matrix(grafo: Grafo, v1_id, v2_id) -> bool:
    """
    Info: Verifica se dois vértices são adjacentes usando a MATRIZ de adjacência.
    E: grafo (Grafo), v1_id (str/int), v2_id (str/int)
    S: bool - True se forem adjacentes, False caso contrário.
    """
    try:
        v1 = grafo.indice_vertices[str(v1_id)]
        v2 = grafo.indice_vertices[str(v2_id)]
        idx1 = grafo.vertices.index(v1)
        idx2 = grafo.vertices.index(v2)
        
        return grafo.matriz_adj[idx1][idx2] == 1 or \
              (not grafo.direcionado and grafo.matriz_adj[idx2][idx1] == 1)
              
    except (KeyError, ValueError, IndexError):
        return False

def are_adjacent_by_inc_matrix(grafo: Grafo, v1_id, v2_id) -> bool:
    """
    Info: Verifica se dois vértices são adjacentes usando a MATRIZ de incidência.
          Dois vértices são adjacentes se eles incidem sobre la mesma aresta.
    E: grafo (Grafo), v1_id (str/int), v2_id (str/int)
    S: bool - True se forem adjacentes, False caso contrário.
    """
    try:
        v1 = grafo.indice_vertices[str(v1_id)]
        v2 = grafo.indice_vertices[str(v2_id)]
        idx1 = grafo.vertices.index(v1)
        idx2 = grafo.vertices.index(v2)

        if not grafo.matriz_incidencia or not grafo.matriz_incidencia[0]:
            return False

        for j in range(grafo.num_arestas()):
            coluna_v1 = grafo.matriz_incidencia[idx1][j]
            coluna_v2 = grafo.matriz_incidencia[idx2][j]

            if coluna_v1 != 0 and coluna_v2 != 0:
                if grafo.direcionado and coluna_v1 != coluna_v2:
                    return True
                elif not grafo.direcionado:
                    return True
                
    except (KeyError, ValueError, IndexError):
        return False
    return False