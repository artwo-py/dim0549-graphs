# lib/dfs.py

def dfs(adj_list, start_node):
    if start_node not in adj_list:
        raise ValueError(f"O vértice de início '{start_node}' não existe no grafo.")

    color = {node: 'white' for node in adj_list}
    parent = {node: None for node in adj_list}
    
    ordem = []
    arestas_retorno = []

    def _dfs_visit(u):
        color[u] = 'gray'
        pai = parent[u] if parent[u] is not None else "-"
        ordem.append((u, pai))

        for v in adj_list.get(u, []):
            if color[v] == 'white':
                parent[v] = u
                _dfs_visit(v)
            elif color[v] == 'gray':
                arestas_retorno.append((u, v))
        
        color[u] = 'black'

    _dfs_visit(start_node)

    for node in adj_list:
        if color[node] == 'white':
            _dfs_visit(node)
            
    return ordem, arestas_retorno