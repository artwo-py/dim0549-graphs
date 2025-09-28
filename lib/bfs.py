from collections import deque
from .classes import Graph

def build_adj(graph: Graph):
    adj = {}
    for vertex in graph.get_vertices():
        adj[vertex.id] = []

    for edge in graph.get_edges():
        v1 = edge.v1.id if hasattr(edge.v1, "id") else edge.v1
        v2 = edge.v2.id if hasattr(edge.v2, "id") else edge.v2
        
        adj.setdefault(v1, [])
        adj.setdefault(v2, [])
        
        adj[v1].append(v2)
        
        if not graph.directed:
            adj[v2].append(v1)
    
    return adj

def bfs(graph: Graph, start_id=None):
    adj = build_adj(graph)

    all_ids = graph.vertex_index.keys()
    
    if start_id is not None and start_id not in adj:
        raise ValueError(f"start_id '{start_id}' não está no grafo")

    vertices_order = ([start_id] + [i for i in all_ids if i != start_id]) if start_id else all_ids

    visited = set()
    pred = {}
    order = []
    return_edges = []

    for start in vertices_order:
        if start in visited:
            continue
        
        pred[start] = "-"           
        queue = deque([start])
        visited.add(start)
        while queue:
            current = queue.popleft()
            order.append((current, pred[current]))
            for next in adj.get(current, []):
                if next not in visited:
                    visited.add(next)
                    pred[next] = current
                    queue.append(next)
                else:
                    edge = (current, next)
                    return_edges.append(edge)
    
    return order, return_edges