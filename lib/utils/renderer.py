from graphviz import Digraph, Graph
from collections import defaultdict

def encontrar_arestas_de_retorno(grafo):
    adj = grafo.lista_adj
    visitando = set()
    visitado = set()
    arestas_retorno = set()
    def dfs_visit(vertice_obj):
        visitando.add(vertice_obj)
        for vizinho_obj in adj[vertice_obj]:
            if vizinho_obj in visitando:
                arestas_retorno.add((str(vertice_obj.id), str(vizinho_obj.id)))
            elif vizinho_obj not in visitado:
                dfs_visit(vizinho_obj)
        
        visitando.remove(vertice_obj)
        visitado.add(vertice_obj)
    for vertice in grafo.vertices:
        if vertice not in visitado:
            dfs_visit(vertice)
    return arestas_retorno

def renderizar_grafo(grafo):
    if grafo.direcionado:
        dot = Digraph(comment='My Directed Graph', format="png")
    else:
        dot = Graph(comment='My Undirected Graph', format="png")
    dot.graph_attr.update({
        "layout": "neato",
        "rankdir": "LR",
        "splines": "true",
        "overlap": "false",
    })
    for vertice in grafo.vertices:
        dot.node(str(vertice.id), style="solid", penwidth='2.0')
    arestas_de_retorno = set()
    if grafo.direcionado:
        arestas_de_retorno = encontrar_arestas_de_retorno(grafo)
    for aresta in grafo.arestas:
        v1_id = str(aresta.v1.id)
        v2_id = str(aresta.v2.id)
        if (v1_id, v2_id) in arestas_de_retorno:
            dot.edge(v1_id, v2_id, style="dashed", penwidth='1.5', color="gray50", constraint='false')
        else:
            dot.edge(v1_id, v2_id, style="solid", penwidth='2.0', constraint='true')
    return dot

def renderizar_bfs(ordem, arestas_retorno=None,
                    nome_grafo="BFS", ranksep=1.0, nodesep=0.6):
    nivel = defaultdict(int)
    for v, p in ordem:
        nivel[v] = 0 if p == "-" else nivel[p] + 1
    dot = Digraph(nome_grafo,
                  graph_attr={
                    "layout": "neato",
                    "rankdir": "TB",
                              "ranksep": str(ranksep),
                              "nodesep": str(nodesep)}, format="png")
    for v, _ in ordem:
        dot.node(v, style="solid", penwidth='2.0')
    arestas_percurso = {(p, v) for v, p in ordem if p != "-"}
    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, style="solid", penwidth='2.0', constraint='true')
    if arestas_retorno:
        for u, v in arestas_retorno:
            if (u, v) not in arestas_percurso:
                dot.edge(u, v, style="dashed", penwidth='1.5', color="gray50", constraint='false')
    nivel_max = max(nivel.values()) if nivel else -1
    for k in range(nivel_max + 1):
        mesmo_rank = [v for v, nv in nivel.items() if nv == k]
        if mesmo_rank:
            dot.body.append("{rank=same; " + "; ".join(mesmo_rank) + "}")
    return dot

def renderizar_dfs(ordem, arestas_retorno=None, nome_grafo="DFS"):
    dot = Digraph(nome_grafo,
                  graph_attr={
                      "layout": "neato",
                      "rankdir": "TB"
                      },
                  format="png")
    for v, _ in ordem:
        dot.node(v, style="solid", penwidth='2.0')
    arestas_percurso = {(p, v) for v, p in ordem if p != "-"}
    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, style="solid", penwidth='2.0', constraint='true')
    if arestas_retorno:
        for u, v in arestas_retorno:
            if (u,v) not in arestas_percurso:
                dot.edge(u, v, style="dashed", penwidth='1.5', color="gray50", constraint='false')

    return dot