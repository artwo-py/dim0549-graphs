import os
from .matrixbuilder import build_adjacency_matrix
from .classes import Vertex, Graph

def read_graph(file_path, directed=False):
        vertices = []
        file_name = file_path.replace('/', '-').replace('.', '-').split("-")[1]
        graph = Graph(directed, file_name)
        try:
            print(f"\nArquivo: {file_path}")
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


            print("   " + " ".join(vertices))
            for label, row in zip(vertices, adj_matrix):
                print(f"{label:>2} " + " ".join(map(str, row)))

            return graph

        except Exception as e:
            print(f"Erro ao ler o arquivo {file_path}: {e}")

def read_directory(directory):
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

            
