"""
Módulo:    Kruskal
Objetivo:  Implementa o algoritmo de Kruskal para encontrar a árvore geradora mínima.
Funções:   kruskal(grafo)
"""

from lib.core.graph import Grafo, Aresta, Vertice
from lib.algorithms.dfs import dfs
from lib.utils.renderer import renderizar_dfs_classificada

def kruskal(grafo):
    """
    Tarefa: (1).
    Info: Implementa o algoritmo de Kruskal para encontrar a árvore geradora mínima de um grafo ponderado.

    Args:
        grafo (Grafo): O objeto grafo ponderado.

    Returns:
        agm: Lista de arestas que compõem a árvore geradora mínima.
    """
    
    for a in grafo.arestas:
        if a.peso is None:
            raise ValueError("Todas as arestas precisam ser ponderadas para execução do algoritmo.")

    arestas = sorted(grafo.arestas, key=lambda x: x.peso)

    # --------------------------------------------------------------------------
    # Implementação de verificação de ciclos usando busca em profundidade (DFS)
    # --------------------------------------------------------------------------
    
    agm = Grafo(direcionado=grafo.direcionado, nome_arquivo="KRUSKAL")
    for v in grafo.vertices:
        agm.adicionar_vertice(v.id)

    temp = Grafo(direcionado=grafo.direcionado)
    for v in grafo.vertices:
        temp.adicionar_vertice(v.id)

    for aresta in arestas:
        temp.adicionar_aresta(aresta.v1.id, aresta.v2.id, aresta.peso)
        resultado = dfs(grafo=temp, id_vertice_inicial="1", classificar_arestas=True)
        arestas_retorno = resultado['arestas_retorno']
        
        if arestas_retorno:
            temp.remover_aresta(aresta.v1.id, aresta.v2.id)
            continue
        else:
            agm.adicionar_aresta(aresta.v1.id, aresta.v2.id, aresta.peso)
            continue
    
    print("Arestas inseridas: ")
    for aresta in agm.arestas:
        print(f"({aresta.v1.id},{aresta.v2.id}, {{{aresta.peso}}})")

    return agm





    


