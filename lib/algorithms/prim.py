from lib.core.graph import Grafo, Aresta, Vertice
from lib.core.graph_display import imprimir_matriz_adj
from lib.core.graph_converter import get_grafo_subjacente
from math import inf as infinito

def prim(grafo):
    """
    Tarefa: (2).
    Info: Implementa o algoritmo de Prim para encontrar a árvore geradora mínima de um grafo ponderado.
    """

    grafo = get_grafo_subjacente(grafo)

    for a in grafo.arestas:
        if a.peso is None:
            raise ValueError("Todas as arestas precisam ser ponderadas para execução do algoritmo.")

    z = [] # Vértices na AGM
    n = grafo.vertices.copy() # Vértices fora da AGM
    t = [] 

    if "1" not in grafo.indice_vertices:
        if not n:
            return Grafo(direcionado=grafo.direcionado, nome_arquivo="PRIM_VAZIO", ponderado=True) # Grafo vazio
        vertice_inicial = n[0]
    else:
        vertice_inicial = grafo.indice_vertices["1"]
    
    z.append(vertice_inicial)
    n.remove(vertice_inicial)
    
    while n:
        melhor_aresta_dados = None
        melhor_peso = infinito

        for vertice_z in z:
            indice_z = grafo.vertices.index(vertice_z)
            for vertice_n in n:
                indice_n = grafo.vertices.index(vertice_n)
                
                w1 = grafo.matriz_adj[indice_z][indice_n] # z -> n
                w2 = grafo.matriz_adj[indice_n][indice_z] # n -> z
                
                w = min(w1, w2) 

                if w != grafo.vazio and w < melhor_peso:
                    melhor_peso = w
                    melhor_aresta_dados = (vertice_z, vertice_n, melhor_peso)

        if melhor_aresta_dados is None:
            break 
        
        v1, v2, peso_encontrado = melhor_aresta_dados

        t.append(Aresta(v1, v2, peso_encontrado))
        
        z.append(v2)
        n.remove(v2)

    agm = Grafo(direcionado=grafo.direcionado, nome_arquivo="PRIM", ponderado=True)
    for v in grafo.vertices:
        agm.adicionar_vertice(v.id)

    for aresta in t:
        agm.adicionar_aresta(aresta.v1.id, aresta.v2.id, aresta.peso)

    return agm