"""
Módulo:    main
Descriçao: Ponto de entrada da aplicação. Orquestra a leitura dos dados,
           execução de algoritmos (BFS, DFS, LowPT), geração de relatórios
           textuais e renderização visual dos resultados usando Graphviz.
"""
import os
import time
from lib.utils.filereader import ler_diretorio # Leitura de arquivos de grafos
from lib.utils.formater import (
    gerar_relatorio_completo,
    formatar_caminho_floyd_warshall 
)
from lib.algorithms.kruskal import kruskal # Implementação do algoritmo de Kruskal
from lib.algorithms.prim import prim # Implementação do algoritmo de Prim
from lib.algorithms.floyd_warshall import floyd_warshall, reconstruir_caminho # Implementação do algoritmo de Floyd-Warshall
from lib.utils.renderer import (
    renderizar_bfs, # Renderiza o percurso BFS
    renderizar_dfs, # Renderiza o percurso DFS
    renderizar_grafo, # Renderiza o grafo/dígrafo original
    renderizar_agm, # Renderiza a AGM
    renderizar_dfs_classificada, # Renderiza DFS com classificação de arestas (dígrafo)
    renderizar_caminho_curto
)

inicio_timer = time.time()
directory = 'data/unit_2'
grafos = ler_diretorio(directory) # Carrega todos os grafos da pasta 'data'

arvores_geradoras = []

for grafo in grafos:
    agm_kruskal = kruskal(grafo)
    arvores_geradoras.append(agm_kruskal)
    agm_prim = prim(grafo)
    arvores_geradoras.append(agm_prim)

print("--- Renderizando Grafos e Dígrafos Originais ---")
for grafo in grafos:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = os.path.splitext(grafo.nome_arquivo)[0]
    dot = renderizar_grafo(grafo) # Cria objeto DOT para grafo/dígrafo
    dot.render(f'render/{base_name}', view=False, cleanup=True) # Renderiza para PNG


print("--- Renderizando AGMs ---")
for grafo in arvores_geradoras:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = grafo.nome_arquivo
    dot = renderizar_agm(grafo) # Cria objeto DOT para AGM
    dot.render(f'render/agm/{base_name}', view=False, cleanup=True) # Renderiza para PNG

print("--- Renderizando Caminho Mais Curto ---")
ID_INICIO = "1"
ID_FIM = "15"
for grafo in grafos:
    if not grafo.ponderado:
        continue
    report_string, caminho_data = formatar_caminho_floyd_warshall(grafo, ID_INICIO, ID_FIM)
    if caminho_data:
        base_name = os.path.splitext(grafo.nome_arquivo)[0]
        print(f"Renderizando: FLOYD_WARSHALL") 
        dot_caminho = renderizar_caminho_curto(grafo, caminho_data, 
                         nome_grafo=f"Caminho_{ID_INICIO}-{ID_FIM}_{base_name}")
        os.makedirs('render/caminho_mais_curto', exist_ok=True) 
        output_path = f'render/caminho_mais_curto/FLOY_WARSHALL-{ID_INICIO}-{ID_FIM}'
        dot_caminho.render(output_path, view=False, cleanup=True)
        
print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))

