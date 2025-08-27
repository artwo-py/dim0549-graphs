from classes import WeightedEdge

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
    print("\n====Menu====")
    print("1. Adicionar uma aresta")
    print("2. Exibir matriz de adjacência")
    print("3. Exibir estrela direta")
    print("6. Sair")
    option = input("Escolha uma opção: ")

    if option == '1':
        weight = None
        v1 = int(input("Insira o ID do vértice de origem: "))
        v2 = int(input("Insira o ID do vértice de destino: "))
        weight = int(input("Insira o peso do arco: "))
        if (v1 >= 1 and v2 < graph_order) or (v2 >= 1 and v1 < graph_order):
            if weight:  
                adj_matrix[v1-1][v2-1] = weight    
            else:
                print("Insira um valor válido para o peso.")
        else:
            print(f"Insira um valor dentro dos limites da matriz (1 - {graph_order})")

    elif option == '2':
        for i in range(graph_order):
            for j in range(graph_order):
                print(adj_matrix[i][j], end=" ")
            print()
    
    elif option == '3':
        arcs = []
        point = []
        star = []

        for i in range(graph_order):
            for j in range(graph_order):
                if adj_matrix[i][j] != 0:
                    arc = WeightedEdge(i+1, j+1, adj_matrix[i][j])
                    arcs.append(arc)
        
        point = [0] * (graph_order + 1)
        idx = 0
        for v in range(graph_order):
            point[v] = idx
            
            while idx < len(arcs) and arcs[idx].start == v+1:
                idx += 1
        point[graph_order] = len(arcs)

        star = []
        for a_idx, arc in enumerate(arcs):
            v = arc.start
            star.append([arc.weight, (arc.start, arc.end), point[v]])
        
        print("Tabela final:")
        for row in star:
            print(row)


    elif option == '6':
        break
                    