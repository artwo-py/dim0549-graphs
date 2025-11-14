"""
Módulo:    Prim
Objetivo:  Implementa o algoritmo de Prim para encontrar a árvore geradora mínima.
Funções:   prim(grafo)
"""

from lib.core.graph import Grafo, Aresta, Vertice
from lib.core.graph_display import imprimir_matriz_adj
from lib.core.graph_converter import get_grafo_subjacente
from math import inf as infinito

def prim(grafo):
    """
    Tarefa: (2).
    Info: Implementa o algoritmo de Prim para encontrar a árvore geradora mínima de um grafo ponderado.

    Args:
        grafo (Grafo): O objeto grafo ponderado.

    Returns:
        agm (Grafo): Subgrafo gerador do grafo fornecido.
    """

    grafo = get_grafo_subjacente(grafo)

    for a in grafo.arestas:
        if a.peso is None:
            raise ValueError("Todas as arestas precisam ser ponderadas para execução do algoritmo.")

    z = []
    n = grafo.vertices.copy()
    t = []

    vertice_inicial = grafo.indice_vertices["1"]
    z.append(vertice_inicial)
    n.remove(vertice_inicial)

    agm = Grafo(direcionado=grafo.direcionado, nome_arquivo="PRIM", ponderado=True)
    for v in grafo.vertices:
        agm.adicionar_vertice(v.id)

    while n:

        melhor_aresta = None
        melhor_peso = infinito

        for vertice_z in z:
            indice_z = grafo.vertices.index(vertice_z)

            for vertice_n in n:
                indice_n = grafo.vertices.index(vertice_n)
                w = grafo.matriz_adj[indice_z][indice_n]

                if w != grafo.vazio and w < melhor_peso:
                    melhor_peso = w
                    melhor_aresta = (vertice_z, vertice_n)

        if melhor_aresta is None:
            break 

        v1, v2 = melhor_aresta

        t.append(grafo.get_aresta(v1.id, v2.id))
        z.append(v2)
        n.remove(v2)

        for aresta in t:
            agm.adicionar_aresta(aresta.v1.id, aresta.v2.id, aresta.peso)

    return agm


    

        
