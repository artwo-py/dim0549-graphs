"""
Módulo:   main
Descriçao: Ponto de entrada da aplicação para problemas da unidade 3.
"""
import time
import numpy as np
from lib.utils.file_handler import ler_diretorio
from lib.utils.formater import gerar_relatorio_unidade_3, gerar_relatorio_genetico, gerar_relatorio_memetico
from lib.algorithms.local_searches import two_opt, shift, swap, HAS_NUMBA as JIT_LOCAL
if JIT_LOCAL:
    from lib.algorithms.local_searches import (
        jit_shift_search, 
        jit_swap_search, 
        jit_two_opt
    )

from lib.algorithms.nearest import nearest_neighbor, HAS_NUMBA as JIT_NEAREST
if JIT_NEAREST:
    from lib.algorithms.nearest import nearest_neighbor_acelerado

from lib.algorithms.genetic import algoritmo_genetico, HAS_NUMBA as JIT_GENETIC
if JIT_GENETIC:
    from lib.algorithms.genetic import jit_algoritmo_genetico

from lib.algorithms.memetico import memetico, HAS_NUMBA as JIT_MEMETIC
if JIT_MEMETIC:
    from lib.algorithms.memetico import memetico_acelerado
from lib.algorithms.cheapest import cheapest_insertion


# Define flag global se tudo estiver acelerado
MODO_ACELERADO = JIT_LOCAL and JIT_NEAREST and JIT_GENETIC and JIT_MEMETIC


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
    
    # 1. Vizinho Mais Próximo (Acelerado ou Puro)
    if JIT_NEAREST:
        ciclo, custo = nearest_neighbor_acelerado(grafo, inicio)
    else:
        ciclo, custo = nearest_neighbor(grafo, inicio)
    
    # 2. Two-Opt (Acelerado ou Puro)
    if JIT_LOCAL:
        from lib.algorithms.local_searches import two_opt_acelerado
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


# --- 2: Inserção Mais Barata + Swap ---
ciclos_ci, custos_ci, rotas_ci = [], [], []
ciclos_ci_melhorados, custos_ci_melhorados, rotas_ci_melhoradas = [], [], []

print(f"\n--- Algoritmo de Inserção Mais Barata + Swap ---\n")
print("--> Usando a versão Decimal/Padrão")

print(f"Processando {len(grafos)} grafos...\n")

for i, grafo in enumerate(grafos):
    t_inicio_grafo = time.time()
    rota_dict, rota_melhorada_dict = {}, {}
    inicio = grafo.vertices[0]

    ciclo, custo = cheapest_insertion(grafo, inicio)

    ciclo_melhorado, custo_melhorado = swap(grafo, ciclo)

    duracao = time.time() - t_inicio_grafo
    print(f" > Grafo {i+1:02d} ({grafo.nome_arquivo}) | CI: {custo:.2f} -> Swap: {custo_melhorado:.2f} | Tempo: {duracao:.4f}s")

    ciclos_ci.append(ciclo); custos_ci.append(custo)
    rota_dict[tuple(ciclo)] = custo; rotas_ci.append(rota_dict)

    ciclos_ci_melhorados.append(ciclo_melhorado); custos_ci_melhorados.append(custo_melhorado)
    rota_melhorada_dict[tuple(ciclo_melhorado)] = custo_melhorado
    rotas_ci_melhoradas.append(rota_melhorada_dict)

gerar_relatorio_unidade_3(rotas, rotas_melhoradas, rotas_ci, rotas_ci_melhoradas)

# --- 3: Heurísticas Estocásticas - Algoritmos Evolutivos (4 Variantes) ---
VARIANCES = [
    ("Genético Puro", None),
    ("Memético (Shift)", "SHIFT"),
    ("Memético (Swap)", "SWAP"),
    ("Memético (2-opt)", "2OPT")
]

all_stats = []

for nome_variante, tipo_busca in VARIANCES:
    print(f"\n--- {nome_variante} (20 execuções por grafo) ---")
    if JIT_GENETIC: print("--> MODO ACELERADO (JIT) ATIVADO")
    
    estatisticas_variante = []

    for i, grafo in enumerate(grafos):
        print(f"\nProcessando {nome_variante} - Instância {i+1}/{len(grafos)} ({grafo.nome_arquivo})...")
        
        melhor_global = {'custo': float('inf'), 'rota': []}
        soma_custos, soma_tempos = 0, 0
        
        # Prepara Matriz (Modo Acelerado)
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
                # 1. Roda GA Puro (retorna indices)
                indices_ga, custo_ga = jit_algoritmo_genetico(matriz_np)
                
                # 2. Aplica Busca Local (se houver)
                if tipo_busca == "SHIFT":
                    indices_final, custo_final = jit_shift_search(indices_ga, matriz_np)
                elif tipo_busca == "SWAP":
                    indices_final, custo_final = jit_swap_search(indices_ga, matriz_np)
                elif tipo_busca == "2OPT":
                    indices_final, custo_final = jit_two_opt(indices_ga, matriz_np)
                else: # Puro
                    indices_final, custo_final = indices_ga, custo_ga
                
                ciclo_final = [ids[idx] for idx in indices_final]
                
            else:
                # 1. Roda GA Puro (retorna IDs)
                c_ga, custo_ga = algoritmo_genetico(grafo)
                
                # 2. Aplica Busca Local
                if tipo_busca == "SHIFT":
                    ciclo_final, custo_final = shift(grafo, c_ga)
                elif tipo_busca == "SWAP":
                    ciclo_final, custo_final = swap(grafo, c_ga)
                elif tipo_busca == "2OPT":
                    ciclo_final, custo_final = two_opt(grafo, c_ga)
                else:
                    ciclo_final, custo_final = c_ga, custo_ga
                
            duracao = time.time() - t_ini
            soma_custos += custo_final
            soma_tempos += duracao
            
            if execucao % 5 == 0 or execucao == 1:
                print(f"    > Exec {execucao:02d} | Custo: {custo_final:.2f}")
            
            if custo_final < melhor_global['custo']:
                melhor_global['custo'] = custo_final
                melhor_global['rota'] = ciclo_final

        estatisticas_variante.append({
            'variante': nome_variante,
            'melhor_custo': melhor_global['custo'],
            'melhor_rota': melhor_global['rota'],
            'media_custo': soma_custos / 20,
            'media_tempo': soma_tempos / 20
        })
        
    all_stats.append(estatisticas_variante)


with open("resultados_evolutivos.txt", "w", encoding='utf-8') as f:
    for i_var, stats_lista in enumerate(all_stats):
        nome = VARIANCES[i_var][0]
        f.write(f"\n======================================================\n")
        f.write(f"=== RESULTADOS: {nome.upper()} ===\n")
        f.write(f"======================================================\n")
        
        for i_inst, dados in enumerate(stats_lista):
            f.write(f"\nInstância {i_inst+1}:\n")
            f.write(f"  Melhor Custo: {dados['melhor_custo']}\n")
            f.write(f"  Média Custo:  {dados['media_custo']:.2f}\n")
            f.write(f"  Tempo Médio:  {dados['media_tempo']:.4f}s\n")
            f.write(f"  Melhor Rota:  {dados['melhor_rota']}\n")



print(f"\n\n--- Algoritmo Memético (20 execuções por grafo) ---")
estatisticas_memetico_2opt = []
for i, grafo in enumerate(grafos):
    print(f"\nProcessando Memético Instância {i+1}/{len(grafos)} ({grafo.nome_arquivo})...")
    
    melhor_global = {'custo': float('inf'), 'rota': []}
    soma_custos, soma_tempos = 0, 0

    if JIT_MEMETIC:
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

        if JIT_MEMETIC:
            indices, custo = memetico_acelerado(matriz_np)
            ciclo_final = [ids[idx] for idx in indices]
        else:
            ciclo_final, custo = memetico(grafo)
            
        duracao = time.time() - t_ini
        soma_custos += custo
        soma_tempos += duracao
        
        print(f"    > Execução {execucao:02d}/20 | Custo Final: {custo:.2f} | Tempo: {duracao:.4f}s")
        
        if custo < melhor_global['custo']:
            melhor_global['custo'] = custo
            melhor_global['rota'] = ciclo_final

    estatisticas_memetico_2opt.append({
        'melhor_custo': melhor_global['custo'],
        'melhor_rota': melhor_global['rota'],
        'media_custo': soma_custos / 20,
        'media_tempo': soma_tempos / 20
    })

gerar_relatorio_memetico(estatisticas_memetico_2opt)


print("\nProcessamento concluído.")
print("\nTempo total: %.4f segundos" % (time.time() - inicio_timer))
