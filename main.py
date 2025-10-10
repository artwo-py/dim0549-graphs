import os
import time
from lib.build_from_matrix import escrever_digrafo_grafo_em_arquivo_a_partir_de_matriz
from lib.utils.filereader import ler_diretorio
from lib.utils.formater import gerar_relatorio_completo
from lib.algorithms.bfs import bfs
from lib.algorithms.dfs import dfs
from lib.algorithms.dfs_search import busca_profundidade_com_classificacao
from lib.utils.renderer import renderizar_bfs, renderizar_dfs, renderizar_grafo, renderizar_grafo_subjacente, renderizar_dfs_classificada

inicio_timer = time.time()
directory = 'data'
subdirectory = 'matrix_incidencia'

print("--- Escrevendo Arquivos de Grafos com Base na Matriz ---")
escrever_digrafo_grafo_em_arquivo_a_partir_de_matriz(directory, subdirectory)

print("\n--------------------------------------------------\n")
grafos = ler_diretorio(directory)

print("\n--- Gerando Relatório de Análise (resultados.txt) ---")
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
        dot = renderizar_bfs(order, back_edges, ranksep=1.6, nodesep=1.2)
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


print("\n--- Executando e Renderizando Busca em Profundidade ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando Busca em Profundidade em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id)
        ordem, arestas_arvore, arestas_retorno, arestas_avanco, arestas_cruzamento, pe_ids, ps_ids = busca_profundidade_com_classificacao(grafo, vertice_inicial)
        dot_dfs = renderizar_dfs_classificada(ordem, arestas_arvore, arestas_retorno, arestas_avanco, arestas_cruzamento)
        dot_dfs.render(f'render/dfs/Busca_Classificacao', view=False, cleanup=True)

print("\n--- Executando e Renderizando Grafos Subjacentes ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Gerando Subjacente em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        dot = renderizar_grafo_subjacente(grafo)
        dot.render(f'render/subjacente/SUBJACENTE_{base_name}', view=False, cleanup=True)

print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))