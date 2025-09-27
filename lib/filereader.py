import os
from .matrixbuilder import build_adjacency_matrix, list_to_matrix
from .classes import Vertex, Graph

def read_graph(file_path, directed=False):
        print(f"Arquivo: {file_path}\n")
        vertices = []
        file_name = file_path.replace('/', '-').replace('.', '-').split("-")[1]
        graph = Graph(directed, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                graph_order = int(f.readline())
                adj_matrix = build_adjacency_matrix(graph_order)

                for line in f:
                    parts = [p.strip() for p in line.split(',')]
                    
                    if len(parts) < 2 or not parts[0] or not parts[1]:
                        continue

                    v1, v2 = parts[0], parts[1]

                    if v1 not in vertices:
                        vertices.append(v1)
                        graph.add_vertex(v1)
                    if v2 not in vertices:
                        vertices.append(v2)
                        graph.add_vertex(v2)

                    i = vertices.index(v1)
                    j = vertices.index(v2)

                    adj_matrix[i][j] = 1
                    if not directed:
                        adj_matrix[j][i] = 1
            
                for i in range(graph_order):
                    for j in range(graph_order):
                        if adj_matrix[i][j] == 1:
                            graph.add_edge(graph.vertices[i], graph.vertices[j], directed)

            with open("results.txt", "a") as file:
                file.write(f"Arquivo: {file_path}\n")
                file.write("==== MATRIZ DE ADJACÊNCIA ==== \n")
                file.write("   " + " ".join(vertices)+"\n")
                for label, row in zip(vertices, adj_matrix):
                        file.write(f"{label:>2} " + " ".join(map(str, row))+"\n")

                adj_list = {}

                for i in range(graph_order):
                        adj_list[str(vertices[i])] = []
                        for j in range(graph_order):
                            if adj_matrix[i][j] == 1:
                                adj_list[str(vertices[i])] += [str(graph.vertices[j])]

                adjacencies = adj_list.items()

                file.write("\n==== MATRIZ DE ADJACÊNCIA -> LISTA DE ADJACÊNCIA ====")
                for adjacency in adjacencies:
                    file.write(f"\n{adjacency[0]}: {adjacency[1]}")
                file.write("\n")
                
                new_matrix, new_matrix_vertices = list_to_matrix(adj_list)
                
                file.write("\n==== LISTA DE ADJACÊNCIA -> MATRIZ DE ADJACÊNCIA ==== \n")
                file.write("   " + " ".join(new_matrix_vertices)+"\n")
                
                for v, row in zip(new_matrix_vertices, new_matrix):
                    file.write(f"{v:>2} " + " ".join(map(str, row))+"\n")
                
                degrees = {}

                for vertex in graph.vertices:
                    if directed:
                        degrees[str(vertex.id)] = [0, 0]
                    else:
                        degrees[str(vertex.id)] = 0
                    
                    for edge in graph.edges:
                        if directed:
                            if edge.v1.id == vertex.id:
                                degrees[str(vertex.id)][0] -= 1
                            
                            if edge.v2.id == vertex.id:
                                degrees[str(vertex.id)][1] += 1

                        else:
                            if edge.v1.id == vertex.id or edge.v2.id == vertex.id:
                                degrees[str(vertex.id)] += 1
                
                file.write("\n==== GRAU DE CADA VÉRTICE NO GRAFO ==== \n")

                if not graph.directed:
                    for v, d in degrees.items():
                        file.write(f"d({v}) = {d}\n")
                    file.write("\n")
                
                else:
                    for v, d in degrees.items():
                        file.write(f"d-({v}) = {d[0]}, d+({v}) = {d[1]}\n")
                    file.write("\n")

            return graph

        except Exception as e:
            print(f"Erro ao ler o arquivo {file_path}: {e}")

def read_directory(directory):
    with open("results.txt", "w") as file:
        file.write("")
    try:
        files = os.listdir(directory)
    except FileNotFoundError:
        print(f"ERRO: A pasta '{directory}' não foi encontrada.")
        return

    graph_list = []

    for file_name in files:

        full_path = os.path.join(directory, file_name)
        
        if os.path.isfile(full_path):
            if file_name.lower().startswith('grafo') and file_name.lower().endswith('.txt'):
                graph = read_graph(full_path)
                graph_list.append(graph)
            
            elif file_name.lower().startswith('digrafo') and file_name.lower().endswith('.txt'):
                graph = read_graph(full_path, True)
                graph_list.append(graph)
    
    return graph_list

            
