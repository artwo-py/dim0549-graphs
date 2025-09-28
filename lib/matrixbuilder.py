def construir_matriz_adj(ordem):
    adj_matrix = []
    for i in range(ordem):
        linha = []
        for j in range(ordem):
            linha.append(0)
        
        adj_matrix.append(linha)

    return adj_matrix

def lista_para_matriz(lista_adj):
    vertices = list(lista_adj.keys())
    n = len(vertices)
    indice = {v: i for i, v in enumerate(vertices)}
    matriz = construir_matriz_adj(n)
    
    for v, adjacencias in lista_adj.items():
        i = indice[v]
        for w in adjacencias:
            j = indice[w]
            matriz[i][j] = 1

    return matriz, vertices

