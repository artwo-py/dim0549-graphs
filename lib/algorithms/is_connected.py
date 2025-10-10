from lib.core.graph import Grafo
from lib.algorithms.bfs import bfs

def is_connected(grafo: Grafo) -> bool:
    """
    (11) Verifica a conectividade de um grafo.

    Info: Para grafos não-direcionados, verifica se há um único componente conexo
          utilizando a ordem de visita retornada pela BFS. Para grafos direcionados,
          verifica se o grafo subjacente não-direcionado é conexo (conectividade fraca).

    Args:
        grafo (Grafo): O objeto grafo a ser verificado.

    Returns:
        bool: True se o grafo for conexo (ou fracamente conectado), False caso contrário.
    """
    if grafo.num_vertices() <= 1:
        return True

    ordem_visita, _ = bfs(grafo)

    if not ordem_visita:
        return True

    num_componentes = 0
    for _, pai_id in ordem_visita:
        if pai_id == '-':
            num_componentes += 1
            
    return num_componentes == 1
