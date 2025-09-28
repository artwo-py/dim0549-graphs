from collections import deque
from .classes import Grafo

def lista_adj(grafo: Grafo):
    adj = {}
    for vertice in grafo.get_vertices():
        adj[vertice.id] = []

    for aresta in grafo.get_arestas():
        v1 = aresta.v1.id if hasattr(aresta.v1, "id") else aresta.v1
        v2 = aresta.v2.id if hasattr(aresta.v2, "id") else aresta.v2
        
        adj.setdefault(v1, [])
        adj.setdefault(v2, [])
        
        adj[v1].append(v2)
        
        if not grafo.direcionado:
            adj[v2].append(v1)
    
    return adj

def bfs(grafo: Grafo, id_inicio=None):
    adj = lista_adj(grafo)

    todos_ids = grafo.indice_vertices.keys()
    
    if id_inicio is not None and id_inicio not in adj:
        raise ValueError(f"id_inicio '{id_inicio}' não está no grafo")

    ordem_vertices = ([id_inicio] + [i for i in todos_ids if i != id_inicio]) if id_inicio else todos_ids

    visitados = set()
    pred = {}
    ordem = []
    arestas_retorno = []

    for inicio in ordem_vertices:
        if inicio in visitados:
            continue
        
        pred[inicio] = "-"           
        fila = deque([inicio])
        visitados.add(inicio)
        while fila:
            atual = fila.popleft()
            ordem.append((atual, pred[atual]))
            for prox in adj.get(atual, []):
                if prox not in visitados:
                    visitados.add(prox)
                    pred[prox] = atual
                    fila.append(prox)
                else:
                    aresta = (atual, prox)
                    arestas_retorno.append(aresta)
    
    return ordem, arestas_retorno