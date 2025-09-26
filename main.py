from lib.filereader import read_directory
import graphviz

directory = 'data'

graphs = read_directory(directory)

d = 0
u = 0
for graph in graphs:
    if graph.directed:
        dot = graphviz.Digraph(comment='My Directed Graph')
    else:
        dot = graphviz.Graph(comment='My Undirected Graph')

    for vertex in graph.vertices:
        dot.node(str(vertex.id))
    
    for edge in graph.edges:
        dot.edge(str(edge.v1.id), str(edge.v2.id))
    
    dot.render(f'render/{graph.file_name}', view=False)
        
    


