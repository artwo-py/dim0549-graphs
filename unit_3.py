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

from lib.algorithms.nearest import nearest_neighbor
from lib.algorithms.local_searches import two_opt

inicio_timer = time.time()
directory = 'data/unit_3'

grafo = ler_diretorio(directory)[0]

print(f"Grafo carregado: {grafo.nome_arquivo}")
print(f"Número de vértices: {len(grafo.vertices)}")
print(f"Número de arestas: {len(grafo.arestas)}")

print(f"\n--- Unidade 3: Algoritmo do Vizinho Mais Próximo ---\n")
ciclos = []
custos = [] 

ciclos_melhorados = []
custos_melhorados = []

inicio = list(grafo.vertices)[0].id
ciclo, custo = nearest_neighbor(grafo, inicio)
ciclo_melhorado, custo_melhorado = two_opt(grafo, ciclo)

ciclos.append(ciclo)
custos.append(custo)

ciclos_melhorados.append(ciclo_melhorado)
custos_melhorados.append(custo_melhorado)

print("Ciclos Hamiltonianos encontrados:")

for ciclo in ciclos:
    print(ciclo)

for custo in custos:
    print(f"Custo total do ciclo: {custo}") 

print("\nCiclos Hamiltonianos melhorados com 2-opt:")
for ciclo_melhorado in ciclos_melhorados:
    print(ciclo_melhorado)
for custo_melhorado in custos_melhorados:
    print(f"Custo total do ciclo melhorado: {custo_melhorado}")

print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))