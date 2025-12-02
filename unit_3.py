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
    gerar_relatorio_unidade_3
)
from lib.utils.renderer import (
    renderizar_grafo,
    renderizar_agm,
    renderizar_caminho_curto
)

from lib.algorithms.nearest import nearest_neighbor
from lib.algorithms.local_searches import two_opt

inicio_timer = time.time()
directory = 'data/unit_3'

destinos = [
    range(1, 49),
    range(1, 37),
    range(1, 25),
    range(1, 13),
    [1, 7, 8, 9, 10, 11, 12],
    range(1, 7)
]

grafos = []

for it, destino in enumerate(destinos):
    print(destino)
    grafos += ler_diretorio(directory, destinos=destino, it=it)

ciclos = []
custos = [] 

ciclos_melhorados = []
custos_melhorados = []

rotas = []
rotas_melhoradas = []

print(f"\n--- Unidade 3: Algoritmo do Vizinho Mais Próximo ---\n")

print(f"Processando {len(grafos)} grafos...\n")

for grafo in grafos:
    rota = {}
    rota_melhorada = {}

    inicio = list(grafo.vertices)[0].id
    ciclo, custo = nearest_neighbor(grafo, inicio)
    ciclo_melhorado, custo_melhorado = two_opt(grafo, ciclo)

    ciclos.append(ciclo)
    custos.append(custo)
    rota[tuple(ciclo)] = custo
    rotas.append(rota)

    ciclos_melhorados.append(ciclo_melhorado)
    custos_melhorados.append(custo_melhorado)
    rota_melhorada[tuple(ciclo_melhorado)] = custo_melhorado
    rotas_melhoradas.append(rota_melhorada)

gerar_relatorio_unidade_3(rotas, rotas_melhoradas)

print("\nProcessamento concluído.")
print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))