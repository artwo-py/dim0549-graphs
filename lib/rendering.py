from graphviz import Digraph, Graph
from collections import defaultdict

def render_graph(graph):
    if graph.directed:
        dot = Digraph(comment='My Directed Graph', format="png")
    else:
        dot = Graph(comment='My Undirected Graph', format="png")

    for vertex in graph.vertices:
        dot.node(str(vertex.id))
    
    for edge in graph.edges:
        dot.edge(str(edge.v1.id), str(edge.v2.id))
    
    return dot

def render_bfs(order, return_edges=None,
                    graph_name="BFS", ranksep=1.0, nodesep=0.6):
    level = defaultdict(int)
    for v, p in order:
        level[v] = 0 if p == "-" else level[p] + 1

    dot = Digraph(graph_name,
                  graph_attr={"rankdir": "TB",
                              "ranksep": str(ranksep),
                              "nodesep": str(nodesep)}, format="png")

    for v, _ in order:
        dot.node(v)

    for v, p in order:
        if p != "-":
            dot.edge(p, v, color="black")

    if return_edges:
        for u, v in return_edges:
            dot.edge(u, v, color="red", style="dashed")

    max_level = max(level.values())
    for k in range(max_level + 1):
        same_rank = [v for v, lvl in level.items() if lvl == k]
        if same_rank:
            dot.body.append("{rank=same; " + "; ".join(same_rank) + "}")

    return dot