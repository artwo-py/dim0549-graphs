def build_adjacency_matrix(order):
    adj_matrix = []
    for i in range(order):
        row = []
        for j in range(order):
            row.append(0)
        
        adj_matrix.append(row)

    return adj_matrix

