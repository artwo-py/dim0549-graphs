"""
Módulo:    main
Descriçao: Ponto de entrada da aplicação. Orquestra a leitura dos dados,
           execução de algoritmos (BFS, DFS, LowPT), geração de relatórios
           textuais e renderização visual dos resultados usando Graphviz.
"""
import os
import time
from lib.utils.filereader import ler_diretorio # Leitura de arquivos de grafos
from lib.utils.formater import gerar_relatorio_completo # Geração do relatório textual completo
from lib.algorithms.bfs import bfs # Implementação do algoritmo BFS
from lib.algorithms.dfs import dfs # Implementação do algoritmo DFS (com ou sem classificação de arestas)
from lib.utils.renderer import (
    renderizar_bfs, # Renderiza o percurso BFS
    renderizar_dfs, # Renderiza o percurso DFS
    renderizar_grafo, # Renderiza o grafo/dígrafo original
    renderizar_grafo_subjacente, # Renderiza o grafo subjacente
    renderizar_dfs_classificada # Renderiza DFS com classificação de arestas (dígrafo)
)

inicio_timer = time.time()
directory = 'data/unit_1'
grafos = ler_diretorio(directory) # Carrega todos os grafos da pasta 'data'

print("\n--- Gerando Relatório de Análise (resultados.txt) ---")
output_filename = 'resultados.txt'
with open(output_filename, 'w', encoding='utf-8') as f:
    grafos_ordenados = sorted(grafos, key=lambda g: g.nome_arquivo)
    for i, grafo in enumerate(grafos_ordenados):
        print(f"Analisando: {grafo.nome_arquivo}")
        relatorio = gerar_relatorio_completo(grafo) # Gera relatório textual
        f.write(relatorio)
        if i < len(grafos_ordenados) - 1:
            f.write("\n\n\n")
print("Relatório de análise gerado com sucesso!\n")

print("--- Renderizando Grafos e Dígrafos Originais ---")
for grafo in grafos:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = os.path.splitext(grafo.nome_arquivo)[0]
    dot = renderizar_grafo(grafo) # Cria objeto DOT para grafo/dígrafo
    dot.render(f'render/{base_name}', view=False, cleanup=True) # Renderiza para PNG

print("\n--- Executando BFS para GRAFOS (Req. 13) ---")
for grafo in grafos:
    if not grafo.direcionado and grafo.vertices:
        print("Executando BFS em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id) # Usa o primeiro vértice como inicial
        order, back_edges = bfs(grafo, vertice_inicial) # Executa BFS
        dot = renderizar_bfs(order, back_edges, direcionado=False) # Renderiza BFS (grafo)
        dot.render(f'render/bfs/{base_name}_BFS', view=False, cleanup=True)

print("\n--- Executando BFS para DÍGRAFOS (Req. 19) ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando BFS em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id)
        order, back_edges = bfs(grafo, vertice_inicial) # Executa BFS
        dot = renderizar_bfs(order, back_edges, direcionado=True) # Renderiza BFS (dígrafo)
        dot.render(f'render/bfs/{base_name}_BFS', view=False, cleanup=True)

print("\n--- Executando DFS para GRAFOS (Req. 14) ---")
for grafo in grafos:
    if not grafo.direcionado and grafo.vertices:
        print("Executando DFS em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id)
        ordem_dfs, arestas_de_retorno = dfs(grafo, vertice_inicial) # Executa DFS (grafo)
        dot_dfs = renderizar_dfs(ordem_dfs, arestas_de_retorno) # Renderiza DFS
        dot_dfs.render(f'render/dfs/{base_name}_DFS', view=False, cleanup=True)

print("\n--- Executando DFS para DÍGRAFOS (Req. 20) ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Executando DFS em:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        vertice_inicial = str(grafo.vertices[0].id)
        
        resultados_dfs = dfs(grafo, vertice_inicial, classificar_arestas=True) # Executa DFS c/ classificação
        
        dot_dfs = renderizar_dfs_classificada( # Renderiza DFS classificada
            ordem_visita=resultados_dfs['ordem_visita'],
            arestas_arvore=resultados_dfs.get('arestas_arvore', []),
            arestas_retorno=resultados_dfs.get('arestas_retorno', []),
            arestas_avanco=resultados_dfs.get('arestas_avanco', []),
            arestas_cruzamento=resultados_dfs.get('arestas_cruzamento', [])
        )
        dot_dfs.render(f'render/dfs/{base_name}_DFS', view=False, cleanup=True)

print("\n--- Renderizando Grafos Subjacentes para DÍGRAFOS (Req. 18) ---")
for grafo in grafos:
    if grafo.direcionado and grafo.vertices:
        print("Gerando Subjacente de:", grafo.nome_arquivo)
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        dot = renderizar_grafo_subjacente(grafo) # Cria objeto DOT do grafo subjacente
        dot.render(f'render/subjacente/SUBJACENTE_{base_name}', view=False, cleanup=True)

print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))