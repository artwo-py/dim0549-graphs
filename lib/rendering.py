from graphviz import Digraph, Graph
from collections import defaultdict

def renderizar_grafo(grafo):
    if grafo.direcionado:
        dot = Digraph(comment='My Directed Graph', format="png")
    else:
        dot = Graph(comment='My Undirected Graph', format="png")

    for vertice in grafo.vertices:
        dot.node(str(vertice.id))
    
    for aresta in grafo.arestas:
        dot.edge(str(aresta.v1.id), str(aresta.v2.id))
    
    return dot

def renderizar_bfs(ordem, arestas_retorno=None,
                    nome_grafo="BFS", ranksep=1.0, nodesep=0.6):
    nivel = defaultdict(int)
    for v, p in ordem:
        nivel[v] = 0 if p == "-" else nivel[p] + 1

    dot = Digraph(nome_grafo,
                  graph_attr={"rankdir": "TB",
                              "ranksep": str(ranksep),
                              "nodesep": str(nodesep)}, format="png")

    for v, _ in ordem:
        dot.node(v)

    for v, p in ordem:
        if p != "-":
            dot.edge(p, v, color="black")

    if arestas_retorno:
        for u, v in arestas_retorno:
            dot.edge(u, v, color="red", style="dashed")

    nivel_max = max(nivel.values())
    for k in range(nivel_max + 1):
        mesmo_rank = [v for v, nv in nivel.items() if nv == k]
        if mesmo_rank:
            dot.body.append("{rank=same; " + "; ".join(mesmo_rank) + "}")

    return dot