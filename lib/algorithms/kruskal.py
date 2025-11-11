"""
Módulo:    Kruskal
Objetivo:  Implementa o algoritmo de Kruskal para encontrar a árvore geradora mínima.
Funções:   kruskal(grafo)
"""

from lib.core.graph import Grafo, Aresta, Vertice

def kruskal(grafo):
    """
    Tarefas: (1), (2).
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
    # Implementação de Union-Find com union by rank e compressão de caminhos
    # --------------------------------------------------------------------------
    
    pai = {}
    rank = {}

    def find(x):
        if pai[x] != x:
            pai[x] = find(pai[x])
        return pai[x]

    def union(x, y):
        rx = find(x)
        ry = find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            pai[rx] = ry
        elif rank[rx] > rank[ry]:
            pai[ry] = rx
        else:
            pai[ry] = rx
            rank[rx] += 1
        return True

    for v in grafo.vertices:
        pai[v.id] = v.id
        rank[v.id] = 0

    agm = Grafo(direcionado=True, nome_arquivo="Kruskal")

    for v in grafo.vertices:
        agm.adicionar_vertice(v.id)

    for a in arestas:
        if union(a.v1.id, a.v2.id):
            agm.adicionar_aresta(a.v1.id, a.v2.id, w=a.peso)
            print(f"Aresta {a} adicionada na AGM")
        else:
            print(f"Aresta {a} NÃO adicionada na AGM")

    for aresta in agm.arestas:
        print(aresta)

    return agm


