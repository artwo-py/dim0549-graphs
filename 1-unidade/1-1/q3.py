graph_order = None
graph_order = int(input("Insira a ordem do grafo: "))

adj_matrix = []
inc_matrix = []

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
            row = []
            
            for j in range(graph_order):
                row.append(0)
            
            row[v1-1] = -1
            row[v2-1] = 1
            
            inc_matrix.append(row)
        else:
            print(f"Insira um valor dentro dos limites da matriz (1 - {graph_order})")

    elif option == '2':
        for i in range(graph_order):
            for j in range(graph_order):
                print(adj_matrix[i][j], end=" ")
            print()
    
    elif option == '3':
        for i in range(len(inc_matrix)):
            for j in range(graph_order):
                print(inc_matrix[i][j], end=' ')