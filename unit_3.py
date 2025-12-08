"""
Módulo:   main
Descriçao: Ponto de entrada da aplicação.
"""
import time
import numpy as np
from lib.utils.file_handler import ler_diretorio
from lib.utils.formater import gerar_relatorio_unidade_3, gerar_relatorio_genetico
from lib.algorithms.local_searches import two_opt, shift, HAS_NUMBA as JIT_LOCAL

if JIT_LOCAL:
    from lib.algorithms.local_searches import two_opt_acelerado
from lib.algorithms.nearest import nearest_neighbor, HAS_NUMBA as JIT_NEAREST
if JIT_NEAREST:
    from lib.algorithms.nearest import nearest_neighbor_acelerado
from lib.algorithms.genetic import algoritmo_genetico, HAS_NUMBA as JIT_GENETIC
if JIT_GENETIC:
    from lib.algorithms.genetic import executar_ga_acelerado

MODO_ACELERADO = JIT_LOCAL and JIT_NEAREST and JIT_GENETIC

inicio_timer = time.time()
directory = 'data/unit_3'

destinos = [
    range(1, 49), range(1, 37), range(1, 25), 
    range(1, 13), [1, 7, 8, 9, 10, 11, 12], range(1, 7)
]

grafos = []
for it, destino in enumerate(destinos):
    print(destino)
    grafos += ler_diretorio(directory, destinos=destino, it=it)

# --- 1: Vizinho Mais Próximo + 2-opt ---
ciclos, custos, rotas = [], [], []
ciclos_melhorados, custos_melhorados, rotas_melhoradas = [], [], []

print(f"\n--- Algoritmo do Vizinho Mais Próximo + 2-opt ---\n")
if MODO_ACELERADO:
    print("--> MODO ACELERADO (JIT) ATIVADO")

print(f"Processando {len(grafos)} grafos...\n")

for i, grafo in enumerate(grafos):
    t_inicio_grafo = time.time()
    rota_dict, rota_melhorada_dict = {}, {}
    inicio = list(grafo.vertices)[0].id
    
    if JIT_NEAREST:
        ciclo, custo = nearest_neighbor_acelerado(grafo, inicio)
    else:
        ciclo, custo = nearest_neighbor(grafo, inicio)
    
    if JIT_LOCAL:
        ciclo_melhorado, custo_melhorado = two_opt_acelerado(grafo, ciclo)
    else:
        ciclo_melhorado, custo_melhorado = two_opt(grafo, ciclo)
    
    duracao = time.time() - t_inicio_grafo
    print(f"  > Grafo {i+1:02d} ({grafo.nome_arquivo}) | NN: {custo:.2f} -> 2-opt: {custo_melhorado:.2f} | Tempo: {duracao:.4f}s")

    ciclos.append(ciclo); custos.append(custo)
    rota_dict[tuple(ciclo)] = custo; rotas.append(rota_dict)

    ciclos_melhorados.append(ciclo_melhorado); custos_melhorados.append(custo_melhorado)
    rota_melhorada_dict[tuple(ciclo_melhorado)] = custo_melhorado
    rotas_melhoradas.append(rota_melhorada_dict)

gerar_relatorio_unidade_3(rotas, rotas_melhoradas)

# --- 2: Algoritmo Genético + Shift ---
print(f"\n--- Algoritmo Genético + Shift (20 execuções por grafo) ---\n")
if JIT_GENETIC: 
    print("--> MODO ACELERADO (JIT) ATIVADO")

estatisticas_genetico = []

for i, grafo in enumerate(grafos):
    print(f"\nProcessando Genético Instância {i+1}/{len(grafos)} ({grafo.nome_arquivo})...")
    
    melhor_global = {'custo': float('inf'), 'rota': []}
    soma_custos, soma_tempos = 0, 0
    
    if JIT_GENETIC:
        ids = [v.id for v in grafo.vertices]
        mapa = {id_v: idx for idx, id_v in enumerate(ids)}
        n = len(ids)
        matriz_np = np.full((n, n), np.inf, dtype=np.float32)
        for v in grafo.vertices:
            idx1 = mapa[v.id]
            for viz, peso in grafo.get_vizinhos(v.id).items():
                matriz_np[idx1, mapa[viz]] = float(peso)

    for execucao in range(1, 21):
        t_ini = time.time()
        
        if JIT_GENETIC:
            indices, custo = executar_ga_acelerado(matriz_np)
            ciclo_final = [ids[idx] for idx in indices]
        else:
            c, _ = algoritmo_genetico(grafo)
            ciclo_final, custo = shift(grafo, c)
            
        duracao = time.time() - t_ini
        soma_custos += custo
        soma_tempos += duracao
        
        print(f"    > Execução {execucao:02d}/20 | Custo Final: {custo:.2f} | Tempo: {duracao:.4f}s")
        
        if custo < melhor_global['custo']:
            melhor_global['custo'] = custo
            melhor_global['rota'] = ciclo_final

    estatisticas_genetico.append({
        'melhor_custo': melhor_global['custo'],
        'melhor_rota': melhor_global['rota'],
        'media_custo': soma_custos / 20,
        'media_tempo': soma_tempos / 20
    })

gerar_relatorio_genetico(estatisticas_genetico)

print("\nProcessamento concluído.")
print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))
