def adicionar_vertice_lista(lista_adj, novo_vertice_id):
    if novo_vertice_id not in lista_adj:
        lista_adj[novo_vertice_id] = []
        print(f"Vértice '{novo_vertice_id}' adicionado à Lista de Adjacências.")
    else:
        print(f"Vértice '{novo_vertice_id}' já existe na lista.")
    
    return lista_adj

def adicionar_vertice_matriz(matriz_adj, vertices_labels, novo_vertice_id):
    if novo_vertice_id in vertices_labels:
        print(f"Vértice '{novo_vertice_id}' já existe na matriz.")
        return matriz_adj, vertices_labels
    
    vertices_labels.append(novo_vertice_id)
    
    for linha in matriz_adj:
        linha.append(0)
        
    nova_ordem = len(vertices_labels)
    matriz_adj.append([0] * nova_ordem)
    
    print(f"Vértice '{novo_vertice_id}' adicionado à Matriz de Adjacências.")
    
    return matriz_adj, vertices_labels