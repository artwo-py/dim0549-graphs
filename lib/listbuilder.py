from collections import defaultdict

def construir_lista_adj(grafo):
    lista_adj = defaultdict(list)

    for vertice in grafo.vertices:
        lista_adj[vertice.id]
        
    for aresta in grafo.arestas:
        v1_id = aresta.v1.id
        v2_id = aresta.v2.id
        
        lista_adj[v1_id].append(v2_id)
        
        if not grafo.direcionado:
            lista_adj[v2_id].append(v1_id)
            
    return dict(lista_adj)

def matriz_para_lista(matriz_adj, vertices_labels):
    lista_adj = defaultdict(list)
    ordem = len(vertices_labels)

    for i in range(ordem):
        vertice_i = vertices_labels[i]
        lista_adj[vertice_i]
        
        for j in range(ordem):
            if matriz_adj[i][j] == 1:
                vertice_j = vertices_labels[j]
                lista_adj[vertice_i].append(vertice_j)
                
    return dict(lista_adj)