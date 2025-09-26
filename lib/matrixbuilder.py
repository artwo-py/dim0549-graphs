def build_adjacency_matrix(order):
    adj_matrix = []
    for i in range(order):
        row = []
        for j in range(order):
            row.append(0)
        
        adj_matrix.append(row)

    return adj_matrix

def list_to_matrix(adj_list):
    vertices = list(adj_list.keys())
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    matrix = build_adjacency_matrix(n)
    
    for v, adjacencies in adj_list.items():
        i = index[v]
        for w in adjacencies:
            j = index[w]
            matrix[i][j] = 1

    return matrix, vertices

