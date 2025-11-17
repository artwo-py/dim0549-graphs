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
from lib.algorithms.hierholzer_ciclos import hierholzer_ciclos
from lib.algorithms.hierholzer_caminhos import hierholzer_caminhos
from lib.algorithms.bellman_ford import formatar_caminho_bellman_ford
from lib.algorithms.chu_liu_edmonds import chu_liu_edmonds

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

print("\n--- Renderizando Grafos e Dígrafos Originais ---")
for grafo in grafos:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = os.path.splitext(grafo.nome_arquivo)[0]
    dot = renderizar_grafo(grafo) # Cria objeto DOT para grafo/dígrafo
    dot.render(f'render/{base_name}', view=False, cleanup=True) # Renderiza para PNG

for grafo in grafos:
    if 'HIERHOLZER' in grafo.nome_arquivo:
        continue
    agm_kruskal = kruskal(grafo)
    arvores_geradoras.append(agm_kruskal)
    agm_prim = prim(grafo)
    arvores_geradoras.append(agm_prim)
    if "CHU_LIU_EDMONDS" in grafo.nome_arquivo:
        agm_chu, erro = chu_liu_edmonds(grafo, raiz="1")
        if agm_chu:
            arvores_geradoras.append(agm_chu)
        else:
            print(f"  Aviso: Erro no {grafo.nome_arquivo} usando Chu-Liu/Edmonds: {erro}")
print("\n--- Gerando Relatório de Análise para Hierholzer (resultados.txt) ---")
with open('resultados.txt', 'a', encoding='utf-8') as f:
    for grafo in grafos:
        if 'HIERHOLZER' in grafo.nome_arquivo:
            relatorio = f"Grafo: {grafo.nome_arquivo} (Direcionado: {grafo.direcionado})\n"
            if 'CICLO_HIERHOLZER'in grafo.nome_arquivo:
                ciclo = hierholzer_ciclos(grafo)
                relatorio += f"  Ciclo euleriano: {' -> '.join(map(str, ciclo))}\n"
            elif 'CAMINHO_HIERHOLZER' in grafo.nome_arquivo:
                caminho = hierholzer_caminhos(grafo)
                relatorio += f"  Caminho euleriano: {' -> '.join(map(str, caminho))}\n"
            f.write(relatorio + "\n")
print("Relatório de análise gerado com sucesso!")

print("\n--- Renderizando AGMs ---")
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
        bf_string, caminho_bf = formatar_caminho_bellman_ford(grafo, ID_INICIO, ID_FIM)
        if caminho_bf:
            print("Renderizando: BELLMAN-FORD")
            dot_bf = renderizar_caminho_curto(
                grafo, caminho_bf,
                nome_grafo=f"BELLMAN_FORD_{ID_INICIO}_{ID_FIM}"
            )
            dot_bf.render(
                f"render/caminho_mais_curto/BELLMAN_FORD-{ID_INICIO}-{ID_FIM}",
                view=False, cleanup=True
            )

print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))

