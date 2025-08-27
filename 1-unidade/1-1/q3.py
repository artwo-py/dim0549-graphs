graph_order = None
graph_order = int(input("Insira a ordem do grafo: "))

adj_matrix = []
edges = []

if graph_order:
    for i in range(graph_order):
        row = []
        for j in range(graph_order):
            row.append(0)
        
        adj_matrix.append(row)        

while True:
    print("\n====Menu====")
    print("1. Adicionar uma aresta")
    print("2. Exibir matriz de adjacência")
    print("3. Exibir matriz de incidência")
    print("6. Sair")
    option = input("Escolha uma opção: ")

    if option == '1':
        v1 = int(input("Insira o ID do vértice de origem: "))
        v2 = int(input("Insira o ID do vértice de destino: "))

        if (v1 >= 1 and v2 < graph_order) or (v2 >= 1 and v1 < graph_order):
            adj_matrix[v1-1][v2-1] = 1
            edges.append((v1-1, v2-1))
        else:
            print(f"Insira um valor dentro dos limites da matriz (1 - {graph_order})")

    elif option == '2':
        for i in range(graph_order):
            for j in range(graph_order):
                print(adj_matrix[i][j], end=" ")
            print()
    
    elif option == '3':
        inc_matrix = [[0]*graph_order for _ in range(len(edges))]

        for idx, (v1, v2) in enumerate(edges):
            inc_matrix[idx][v1] = -1 
            inc_matrix[idx][v2] = 1   

        for row in inc_matrix:
            print(" ".join(map(str, row)))

    elif option == '6':
        break
                    