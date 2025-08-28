from classes import AdjacencyList

CLI_LINE_LENGHT=25

graph_order = None
graph_order = int(input("Insira a ordem do grafo: "))

adj_matrix = []

if graph_order:
    for i in range(graph_order):
        row = []
        for j in range(graph_order):
            row.append(0)
        
        adj_matrix.append(row)

while True:
    print("\n====MENU GRAFOS-CLI====")
    print("1. Adicionar uma aresta")
    print("2. Exibir matriz de adjacência")
    print("3. Exibir lista de adjacência")
    print("4. Sair")
    option = input("(Escolha uma opção): ")

    if option == '1':
        print("-"*CLI_LINE_LENGHT)
        v1 = int(input("Insira o ID do primeiro vértice: "))
        v2 = int(input("Insira o ID do segundo vértice: "))

        if 1 <= v1 <= graph_order and 1 <= v2 <= graph_order:
            adj_matrix[v1-1][v2-1] = 1
            adj_matrix[v2-1][v1-1] = 1

    elif option == '2':
        print("-"*CLI_LINE_LENGHT)
        for i in range(graph_order):
            for j in range(graph_order):
                print(adj_matrix[i][j], end=" ")
            print()
    
    elif option == '3':
        print("-"*CLI_LINE_LENGHT)
        adj_list = [AdjacencyList(v) for v in range(1, graph_order + 1)]
        for i in range(graph_order):
            for j in range(i, graph_order):
                if adj_matrix[i][j] == 1:
                    adj_list[i].adjacencies.append(j+1)
                    adj_list[j].adjacencies.append(i+1)

        for item in adj_list:
            print(str(item.vertex) + " -> " + ", ".join(map(str, item.adjacencies)))
