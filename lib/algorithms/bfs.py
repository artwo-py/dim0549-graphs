"""
Módulo:    BFS
Objetivo:  Implementa o algoritmo de Busca em Largura (Breadth-First Search).
Funções:   bfs(grafo, id_inicio)
"""
from collections import deque

def bfs(grafo, id_inicio=None):
    """
    Tarefas: (13), (19).
    Info: Percorre o grafo em largura a partir de um vértice, para grafo e dígrafo. 
          Lida com grafos desconexos e
          identifica arestas de (retorno/cruzamento).
    E: - grafo (Grafo): O objeto grafo a ser percorrido.
       - id_inicio (str/int, opcional): ID do vértice para iniciar a busca. Se omitido, começa pelo primeiro vértice do grafo.
    S: (list, list) - Tupla contendo:
    - A ordem de visita em formato [(v, pai), ...].
    - A lista de arestas de encontradas.
    """
    adj = grafo.lista_adj 
    vertice_inicial_obj = None
    if id_inicio:
        vertice_inicial_obj = grafo.indice_vertices.get(id_inicio)
        if not vertice_inicial_obj:
            raise ValueError(f"Vértice inicial '{id_inicio}' não está no grafo")
    elif grafo.vertices:
        vertice_inicial_obj = grafo.vertices[0]
    else:
        return [], [] 
    todos_vertices = grafo.get_vertices()
    ordem_de_busca = ([vertice_inicial_obj] + 
                      [v for v in todos_vertices if v != vertice_inicial_obj])
    visitados = set()
    pred = {} 
    ordem = [] 
    arestas_retorno = []
    for inicio_obj in ordem_de_busca:
        if inicio_obj in visitados:
            continue
        pred[inicio_obj] = "-"           
        fila = deque([inicio_obj])
        visitados.add(inicio_obj)
        while fila:
            atual_obj = fila.popleft()
            pred_obj = pred[atual_obj]
            pred_id = str(pred_obj.id) if pred_obj != "-" else "-"
            ordem.append((str(atual_obj.id), pred_id))
            for prox_obj in adj.get(atual_obj, []):
                if prox_obj not in visitados:
                    visitados.add(prox_obj)
                    pred[prox_obj] = atual_obj
                    fila.append(prox_obj)
                else:
                    aresta = (str(atual_obj.id), str(prox_obj.id))
                    arestas_retorno.append(aresta)
    return ordem, arestas_retorno