import os
import time
from lib.utils.filereader import ler_diretorio
from lib.utils.formater import gerar_relatorio_completo
from lib.algorithms.bfs import bfs
from lib.algorithms.dfs import dfs
from lib.utils.renderer import renderizar_bfs, renderizar_dfs, renderizar_grafo

inicio_timer = time.time()
directory = 'data'
grafos = ler_diretorio(directory)

print("--- Gerando Relatório de Análise (resultados.txt) ---")
output_filename = 'resultados.txt'
with open(output_filename, 'w', encoding='utf-8') as f:
    grafos_ordenados = sorted(grafos, key=lambda g: g.nome_arquivo)
    for i, grafo in enumerate(grafos_ordenados):
        print(f"Analisando: {grafo.nome_arquivo}")
        relatorio = gerar_relatorio_completo(grafo)
        f.write(relatorio)
        if i < len(grafos_ordenados) - 1:
            f.write("\n\n\n")
print("Relatório de análise gerado com sucesso!\n")

print("--- Renderizando Grafos Originais ---")
for grafo in grafos:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = os.path.splitext(grafo.nome_arquivo)[0]
    dot = renderizar_grafo(grafo)
    dot.render(f'render/{base_name}', view=False, cleanup=True)

print("\n--- Executando e Renderizando BFS ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando BFS em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id)
        order, back_edges = bfs(grafo, vertice_inicial)
        dot = renderizar_bfs(order, back_edges, ranksep=1.2, nodesep=0.8)
        dot.render(f'render/bfs/BFS_{base_name}', view=False, cleanup=True)

print("\n--- Executando e Renderizando DFS ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando DFS em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id)
        ordem_dfs, arestas_de_retorno = dfs(grafo, vertice_inicial)
        dot_dfs = renderizar_dfs(ordem_dfs, arestas_de_retorno)
        dot_dfs.render(f'render/dfs/DFS_{base_name}', view=False, cleanup=True)


print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))