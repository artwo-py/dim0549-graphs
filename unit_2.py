"""
Módulo:    main
Descriçao: Ponto de entrada da aplicação. Orquestra a leitura dos dados,
           execução de algoritmos, geração de relatórios textuais
           e renderização visual dos resultados.
"""
import os
import time
from lib.utils.file_handler import ler_diretorio  # Leitura de arquivos de grafos
from lib.utils.formater import ( # Geração do relatório textual completo
    formatar_caminho_floyd_warshall,
    gerar_relatorio_unidade_2
)
from lib.utils.renderer import (
    renderizar_grafo,
    renderizar_agm,
    renderizar_caminho_curto
)

from lib.algorithms.kruskal import kruskal # Implementação do algoritmo de Kruskal
from lib.algorithms.prim import prim # Implementação do algoritmo de Prim
from lib.algorithms.dijkstra import dijkstra # Implementação do algoritmo de Dijkstra
from lib.algorithms.bellman_ford import formatar_caminho_bellman_ford
from lib.algorithms.chu_liu_edmonds import chu_liu_edmonds
inicio_timer = time.time()
directory = 'data/unit_2'
# 1. Leitura de dados (Imprime "Lendo arquivo: ...")
grafos = ler_diretorio(directory)

arvores_geradoras = []

for grafo in grafos:
    agm_kruskal = kruskal(grafo)
    arvores_geradoras.append(agm_kruskal)
    agm_prim = prim(grafo)
    arvores_geradoras.append(agm_prim)
    agm_dijkstra = dijkstra(grafo)
    arvores_geradoras.append(agm_dijkstra)

# --- 2. Renderização de Grafos Originais ---
print("\n--- Renderizando Grafos e Dígrafos Originais ---")
os.makedirs('render', exist_ok=True)
for grafo in grafos:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = os.path.splitext(grafo.nome_arquivo)[0]
    dot = renderizar_grafo(grafo)
    dot.render(f'render/{base_name}', view=False, cleanup=True)

# --- 3. Processamento de AGMs ---
for grafo in grafos:
    if 'AGM' in grafo.nome_arquivo:
        try:
            agm_kruskal = kruskal(grafo)
            arvores_geradoras.append(agm_kruskal)
            agm_prim = prim(grafo)
            arvores_geradoras.append(agm_prim)
        except Exception as e:
            print(f"  Erro ao gerar AGM para {grafo.nome_arquivo}: {e}")
    if "CHU_LIU_EDMONDS" in grafo.nome_arquivo:
        agm_chu, erro = chu_liu_edmonds(grafo, raiz="1")
        if agm_chu:
            arvores_geradoras.append(agm_chu)
        else:
            print(f"  Aviso: Erro no {grafo.nome_arquivo} usando Chu-Liu/Edmonds: {erro}")
# --- 4. Renderização de AGMs ---
print("\n--- Renderizando AGMs ---")
os.makedirs('render/agm', exist_ok=True)
for grafo in arvores_geradoras:
    print("Renderizando:", grafo.nome_arquivo)
    base_name = grafo.nome_arquivo
    dot = renderizar_agm(grafo)
    dot.render(f'render/agm/{base_name}', view=False, cleanup=True)

# --- 5. Renderização do Caminho Mais Curto ---
print("\n--- Renderizando Caminho Mais Curto ---")
ID_INICIO = "1"
ID_FIM = "15"
os.makedirs('render/caminho_mais_curto', exist_ok=True)

for grafo in grafos:
    if 'AGM' in grafo.nome_arquivo and grafo.ponderado:
        _ , caminho_data = formatar_caminho_floyd_warshall(grafo, ID_INICIO, ID_FIM)

        if caminho_data:
            print(f"Renderizando: FLOYD_WARSHALL")

            dot_caminho = renderizar_caminho_curto(grafo, caminho_data,
                             nome_grafo=f"Caminho_{ID_INICIO}-{ID_FIM}")
            output_path = f'render/caminho_mais_curto/FLOYD_WARSHALL'
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

# --- 6. "Renderização" de Hierholzer ---
print("\n--- Renderizando Grafos Eulerianos ---")
print("Renderizando: Hierholzer Caminhos")
print("Renderizando: Hierholzer Ciclos")

gerar_relatorio_unidade_2(grafos)

print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))