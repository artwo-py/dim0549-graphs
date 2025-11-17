"""
Módulo:    Dijkstra
Objetivo:  Implementa o algoritmo de Dijkstra para encontrar a árvore geradora mínima.
Funções:   dijkstra(grafo: Grafo, inicio_id=None)
"""

from lib.core.graph import Grafo
import itertools
import heapq
from math import inf as INF

# desempatador
count = itertools.count()

def dijkstra(grafo: Grafo, inicio_id=None):
    """
    Tarefa: (5).
    Info: Implementa o algoritmo de Dijkstra para encontrar a Árvore de Caminho Mínimo (Shortest Path Tree) de um grafo ponderado, gerando os caminhos de menor custo a partir de um vértice de origem.

    Args:
        grafo (Grafo): O objeto grafo ponderado.
        inicio_id: O id do Vertice pelo qual se deseja iniciar. Se não for fornecido (None), será iniciado pelo 1º vértice na lista de vértices do grafo (grafo.vertices[0]).

    Returns:
        spt (Grafo): O subgrafo (Árvore de Caminho Mínimo) gerado pelo algoritmo.
    """

    distancias = {vertice: INF for vertice in grafo.vertices}
    predecessores = {vertice: None for vertice in grafo.vertices}

    for a in grafo.arestas:
        if a.peso is None:
            raise ValueError("Todas as arestas precisam ser ponderadas para execução do algoritmo.")

    if inicio_id is not None:
        s = grafo.indice_vertices.get(str(inicio_id))
        if s is None:
            raise ValueError(f"Vértice com ID '{inicio_id}' não encontrado.")
    else:
        s = grafo.vertices[0]
        
    distancias[s] = 0

    #Iniciando loop que visita todas as arestas
    fila_prioridade = [(0, next(count), s)]
    while fila_prioridade:
        dist_u, _, u = heapq.heappop(fila_prioridade)
        
        # já achou caminho melhor
        if dist_u > distancias[u]:
            continue
        
        # vizinhos
        arestas_u = [
            aresta for aresta in grafo.arestas
            if aresta.v1 == u
        ]

        #relaxamento
        for aresta in arestas_u:
            v = aresta.v2
            peso_uv = aresta.peso if aresta.peso is not None else 0

            nova_distancia = distancias[u] + peso_uv

            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                predecessores[v] = u

                heapq.heappush(fila_prioridade, (nova_distancia, next(count), v))

    # construindo grafo
    spt = Grafo(direcionado=grafo.direcionado, ponderado=grafo.ponderado, nome_arquivo="DIJKSTRA")
    
    for vertice in grafo.vertices:      
        spt.adicionar_vertice(vertice.id) 
        
    for v, pred_v in predecessores.items():
        if pred_v is not None:
            v_id = v.id
            pred_id = pred_v.id
            
            aresta_original = grafo.get_aresta(pred_id, v_id)
            
            if aresta_original:
                peso = aresta_original.peso
                spt.adicionar_aresta(pred_id, v_id, w=peso)
            else:
                 spt.adicionar_aresta(pred_id, v_id)

    return spt