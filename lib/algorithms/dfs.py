"""
Módulo:    DFS
Objetivo:  Implementa o algoritmo de Busca em Profundidade (Depth-First Search).
Funções:   dfs(grafo, id_vertice_inicial)
"""
def dfs(grafo, id_vertice_inicial=None):
    """
    Tarefas: (14), (20).
    Info:   Percorre o grafo em profundidade a partir de um vértice, para grafo
            e dígrafo. Lida com grafos desconexos e identifica arestas de retorno.
    E: - grafo (Grafo): O objeto grafo a ser percorrido.
       - id_vertice_inicial (str/int, opcional): ID do vértice para iniciar a busca. Se omitido, começa pelo primeiro vértice do grafo.
    S: (list, list) - Tupla contendo:
       - A ordem de visita em formato [(v, pai), ...].
       - A lista de arestas de retorno encontradas.
    """
    adj = grafo.lista_adj
    vertice_inicial_obj = None
    if id_vertice_inicial:
        vertice_inicial_obj = grafo.indice_vertices.get(id_vertice_inicial)
        if not vertice_inicial_obj:
            raise ValueError(f"Vértice inicial '{id_vertice_inicial}' não está no grafo.")
    elif grafo.vertices:
        vertice_inicial_obj = grafo.vertices[0]
    else:
        return [], [] 
    todos_vertices = grafo.get_vertices()
    ordem_de_busca = ([vertice_inicial_obj] + 
                      [v for v in todos_vertices if v != vertice_inicial_obj])
    visitados = set()
    visitando = set() 
    pred = {}
    ordem = []
    arestas_retorno = []
    
    def dfs_visit(vertice_obj, predecessor_obj):
        visitados.add(vertice_obj)
        visitando.add(vertice_obj)
        pred[vertice_obj] = predecessor_obj
        pred_id = str(predecessor_obj.id) if predecessor_obj else "-"
        ordem.append((str(vertice_obj.id), pred_id))
        for vizinho_obj in adj.get(vertice_obj, []):
            if vizinho_obj in visitando:
                aresta = (str(vertice_obj.id), str(vizinho_obj.id))
                arestas_retorno.append(aresta)
            elif vizinho_obj not in visitados:
                dfs_visit(vizinho_obj, vertice_obj)
        visitando.remove(vertice_obj)
        
    for inicio_obj in ordem_de_busca:
        if inicio_obj not in visitados:
            dfs_visit(inicio_obj, None)
    if ordem and ordem[0][1] is None:
        primeiro_v, _ = ordem[0]
        ordem[0] = (primeiro_v, "-")
    return ordem, arestas_retorno