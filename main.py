from lib.filereader import ler_diretorio
from lib.bfs import bfs
from lib.rendering import renderizar_bfs, renderizar_grafo
import graphviz
import time

inicio_timer = time.time()
directory = 'data'

grafos = ler_diretorio(directory)

for grafo in grafos:
    dot = renderizar_grafo(grafo)
    
    dot.render(f'render/{grafo.nome_arquivo}', view=False, cleanup=True)
        
for grafo in grafos:
    if grafo.direcionado:
        print("Renderizando:", grafo.nome_arquivo)
        
        order, back_edges = bfs(grafo, str(grafo.vertices[0]))
        
        dot = renderizar_bfs(order, back_edges, ranksep=1.2, nodesep=0.8)
            
        dot.render(f'render/bfs/BFS_{grafo.nome_arquivo}', view=False, cleanup=True)


print("Tempo total: %f segundos" % (time.time() - inicio_timer))


