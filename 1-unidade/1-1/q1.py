from classes import Vertice, Graph

graph = Graph()

CLI_LINE_LENGHT=25

while True:
    print("\n====MENU GRAFOS-CLI====")
    print("1. Adicionar um vértice")
    print("2. Adicionar uma aresta")
    print("3. Remover um vértice")
    print("4. Remover uma aresta")
    print("5. Listar vértices e arestas")
    print("6. Sair")
    option = input("(Escolha uma opção): ")

    if option == '1':
        print("-"*CLI_LINE_LENGHT)
        id = input("Digite o ID do vértice: ")
        unique = True
        
        for v in graph.vertices:
            if v.id == id:
                print("Vértice com esse ID já existe.")
                unique = False
            
        if unique:
            vertex = Vertice(id)
            graph.add_vertex(vertex)
    
    elif option == '2':
        print("-"*CLI_LINE_LENGHT)
        if graph.vertices == []:
            print("Não há vértices no grafo.")
        else:
            id1 = input("Digite o ID do vértice 1: ")
            id2 = input("Digite o ID do vértice 2: ")

            v1 = v2 = None
            if id1 and id2:
                for vertex in graph.vertices:
                    if vertex.id == id1:
                        v1 = vertex
                    if vertex.id == id2:
                        v2 = vertex
                
                if v1 and v2:
                    graph.add_edge(v1, v2)
                    print(f"Aresta de {id1} para {id2} adicionada.")
                else:
                    print("Vértice(s) não encontrado(s).")
    
    elif option == '3':
        print("-"*CLI_LINE_LENGHT)
        vertex_id = input("Insira o ID do vértice a ser removido: ")
        graph.remove_vertex(vertex_id)
    
    elif option == '4':
        print("-"*CLI_LINE_LENGHT)
        if graph.edges == []:
            print("Não há arestas no grafo.")
        else:
            id1 = input("Digite o ID do vértice de origem: ")
            id2 = input("Digite o ID do vértice de destino: ")

            v1 = v2 = e = None
            if id1 and id2:
                for edge in graph.edges:
                    if {edge.v1.id, edge.v2.id} == {id1, id2}:
                        v1 = edge.v1
                        v2 = edge.v2
                        graph.remove_edge(v1, v2)
                    else:
                        print("Vértice(s) não encontrado(s).")

    elif option == '5':
        print("-"*CLI_LINE_LENGHT)
        print("Vértices: ", graph.get_vertices())
        print("Arestas: ", graph.get_edges())
    
    elif option == '6':
        break
    
    else:
        print("Opção inválida!")
        
            

