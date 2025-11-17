from lib.core.graph import Grafo, Aresta, Vertice
from lib.algorithms.dfs import dfs

import heapq
from math import inf as INF

def dijkstra(grafo: Grafo):
    distancias = {vertice: INF for vertice in grafo.vertices}
    predecessores = {vertice: None for vertice in grafo.vertices}
    visitados = {vertice: False for vertice in grafo.vertices}

    s = grafo.vertices[0]
    distancias[s] = 0
    visitados[s] = 1
    arestas_origem = [
            aresta for aresta in grafo.arestas 
            if str(aresta.v1.id) == str(s)
        ]

    #Inicializando os vertices ligados ao inicial
    for aresta in arestas_origem:
        v = aresta.v2
        peso_sv = aresta.peso if aresta.peso is not None else 0
        predecessores[v] = s
        distancias[v] = peso_sv

    #Iniciando loop que visita todo mundo    
    while False in visitados.values():
        menor_distancia = INF
        u = None

        for vertice in grafo.vertices:
            if not visitados[vertice] and distancias[vertice] < menor_distancia:
                menor_distancia = distancias[vertice]
                u = vertice
        
        if u is None:
            break

        visitados[u] = True

        # corre pelos vizinhos
        arestas_de_u = [
            aresta for aresta in grafo.arestas
            if aresta.v1 == u
        ]

        #relaxamento
        for aresta in arestas_de_u:
            uv = aresta.v2
            peso_uv = aresta.peso if aresta.peso is not None else 0

            if distancias[u] + peso_uv < distancias[uv]:
                distancias[uv] = distancias[u] + peso_uv
                predecessores[uv] = u

    # construindo grafo
    agm = Grafo(direcionado=grafo.direcionado, ponderado=grafo.ponderado, nome_arquivo="DIJKSTRA")
    
    for vertice in grafo.vertices: 
        agm.adicionar_vertice(vertice.id) 
        
    for v, pred_v in predecessores.items():
        if pred_v is not None:
            v_id = v.id
            pred_id = pred_v.id
            
            aresta_original = grafo.get_aresta(pred_id, v_id)
            
            if aresta_original:
                peso = aresta_original.peso
                agm.adicionar_aresta(pred_id, v_id, w=peso)
            else:
                agm.adicionar_aresta(pred_id, v_id)

    return agm