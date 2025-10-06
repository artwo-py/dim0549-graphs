from lib.filereader import ler_diretorio
from lib.bfs import bfs
from lib.dfs import dfs
from lib.listbuilder import construir_lista_adj 
from lib.rendering import renderizar_bfs, renderizar_dfs, renderizar_grafo 
import time

inicio_timer = time.time()
directory = 'data'

grafos = ler_diretorio(directory)

print("--- Renderizando Grafos Originais ---")
for grafo in grafos:
    print("Renderizando:", grafo.nome_arquivo)
    dot = renderizar_grafo(grafo)
    dot.render(f'render/{grafo.nome_arquivo}', view=False, cleanup=True)

print("\n--- Executando e Renderizando BFS ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando BFS em:", grafo.nome_arquivo)
        
        vertice_inicial = str(grafo.vertices[0].id)
        order, back_edges = bfs(grafo, vertice_inicial)
        
        dot = renderizar_bfs(order, back_edges, ranksep=1.2, nodesep=0.8)
            
        dot.render(f'render/bfs/BFS_{grafo.nome_arquivo}', view=False, cleanup=True)

print("\n--- Executando e Renderizando DFS ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando DFS em:", grafo.nome_arquivo)

        adj_list = construir_lista_adj(grafo)
        
        vertice_inicial = str(grafo.vertices[0].id)
        
        ordem_dfs, arestas_de_retorno = dfs(adj_list, vertice_inicial)
        dot_dfs = renderizar_dfs(ordem_dfs, arestas_de_retorno)
            
        dot_dfs.render(f'render/dfs/DFS_{grafo.nome_arquivo}', view=False, cleanup=True)


print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))