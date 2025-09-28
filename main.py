from lib.filereader import read_directory
from lib.bfs import bfs
from lib.rendering import render_bfs, render_graph
import graphviz
import time

start_time = time.time()
directory = 'data'

graphs = read_directory(directory)

for graph in graphs:
    dot = render_graph(graph)
    
    dot.render(f'render/{graph.file_name}', view=False, cleanup=True)
        
for graph in graphs:
    if graph.directed:
        print("Renderizando:", graph.file_name)
        
        order, back_edges = bfs(graph, str(graph.vertices[0]))
        
        dot = render_bfs(order, back_edges, ranksep=1.2, nodesep=0.8)
            
        dot.render(f'render/bfs/BFS_{graph.file_name}', view=False, cleanup=True)


print("Tempo total: %f segundos" % (time.time() - start_time))


