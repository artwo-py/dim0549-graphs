"""
Módulo: main
Descrição: Ponto de entrada da aplicação para problemas da unidade 3.
"""
import time
import numpy as np
from lib.utils.file_handler import ler_diretorio
from lib.utils.formater import gerar_relatorio_unidade_3, gerar_relatorio_genetico, gerar_relatorio_memetico
from lib.algorithms.local_searches import two_opt, shift, swap, HAS_NUMBA as JIT_LOCAL
from lib.algorithms.nearest import nearest_neighbor, HAS_NUMBA as JIT_NEAREST
from lib.algorithms.genetic import algoritmo_genetico, HAS_NUMBA as JIT_GENETIC
from lib.algorithms.cheapest import cheapest_insertion

if JIT_LOCAL:
    from lib.algorithms.local_searches import two_opt_acelerado

if JIT_NEAREST:
    from lib.algorithms.nearest import nearest_neighbor_acelerado

if JIT_GENETIC:
    from lib.algorithms.genetic import jit_algoritmo_evolutivo

MODO_ACELERADO = JIT_LOCAL and JIT_NEAREST and JIT_GENETIC

BL_NONE = 0
BL_SHIFT = 1
BL_SWAP = 2
BL_2OPT = 3

def main():
    inicio_timer = time.time()
    directory = 'data/unit_3'
    
    destinos = [
        range(1, 49), range(1, 37), range(1, 25), 
        range(1, 13), [1, 7, 8, 9, 10, 11, 12], range(1, 7)
    ]

    grafos = []
    for it, destino in enumerate(destinos):
        grafos += ler_diretorio(directory, destinos=destino, it=it)

    print(f"\n--- 1. Heurísticas Construtivas + Busca Local ---")
    if MODO_ACELERADO: print("--> MODO ACELERADO (JIT) ATIVADO")

    ciclos, custos, rotas = [], [], []
    ciclos_mel, custos_mel, rotas_mel = [], [], []
    ciclos_ni, custos_ni, rotas_ni = [], [], []
    ciclos_ni_mel, custos_ni_mel, rotas_ni_mel = [], [], []

    for i, grafo in enumerate(grafos):
        t_inicio = time.time()
        inicio_id = list(grafo.vertices)[0].id
        
        if JIT_NEAREST:
            ciclo, custo = nearest_neighbor_acelerado(grafo, inicio_id)
        else:
            ciclo, custo = nearest_neighbor(grafo, inicio_id)
        
        if JIT_LOCAL:
            ciclo_melhorado, custo_melhorado = two_opt_acelerado(grafo, ciclo)
        else:
            ciclo_melhorado, custo_melhorado = two_opt(grafo, ciclo)
        
        ciclo_ni_res, custo_ni_res = cheapest_insertion(grafo, grafo.vertices[0])
        ciclo_ni_m, custo_ni_m = swap(grafo, ciclo_ni_res)

        duracao = time.time() - t_inicio
        print(f"  > Grafo {i+1:02d} | NN+2opt: {custo_melhorado:.2f} | NI+Swap: {custo_ni_m:.2f} | Tempo: {duracao:.4f}s")

        ciclos.append(ciclo); custos.append(custo)
        rota_dict = {}; rota_dict[tuple(ciclo)] = custo; rotas.append(rota_dict)
        ciclos_mel.append(ciclo_melhorado); custos_mel.append(custo_melhorado)
        rota_mel_dict = {}; rota_mel_dict[tuple(ciclo_melhorado)] = custo_melhorado; rotas_mel.append(rota_mel_dict)

        ciclos_ni.append(ciclo_ni_res); custos_ni.append(custo_ni_res)
        rota_ni_dict = {}; rota_ni_dict[tuple(ciclo_ni_res)] = custo_ni_res; rotas_ni.append(rota_ni_dict)
        ciclos_ni_mel.append(ciclo_ni_m); custos_ni_mel.append(custo_ni_m)
        rota_ni_m_dict = {}; rota_ni_m_dict[tuple(ciclo_ni_m)] = custo_ni_m; rotas_ni_mel.append(rota_ni_m_dict)

    gerar_relatorio_unidade_3(rotas, rotas_mel, rotas_ni, rotas_ni_mel)

    EXPERIMENTOS = [
        ("Genético Puro", BL_NONE, None, 100),
        ("Memético (Shift)", BL_SHIFT, shift, 30),
        ("Memético (Swap)", BL_SWAP, swap, 50),
        ("Memético (2-opt)", BL_2OPT, two_opt, 15)
    ]

    stats_genetico = []
    stats_memetico = []

    for nome_variante, id_bl, func_bl, n_geracoes in EXPERIMENTOS:
        print(f"\n--- {nome_variante} ({n_geracoes} gerações, 20 execuções) ---")
        
        for i, grafo in enumerate(grafos):
            print(f"Processando {nome_variante} - {grafo.nome_arquivo}...")
            
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
                
                if id_bl == BL_NONE:
                    exec_pop_size = 250
                    exec_geracoes = 500
                    exec_taxa_mutacao = 0.05
                else:
                    exec_pop_size = 50
                    exec_geracoes = n_geracoes
                    exec_taxa_mutacao = 0.1

                if JIT_GENETIC:
                    indices_final, custo_final = jit_algoritmo_evolutivo(
                        matriz_np, 
                        pop_size=exec_pop_size, 
                        geracoes=exec_geracoes, 
                        taxa_mutacao=exec_taxa_mutacao, 
                        freq_bl=0.1,
                        tipo_bl=id_bl
                    )
                    ciclo_final = [ids[idx] for idx in indices_final]
                    
                else:
                    c_ga, _ = algoritmo_genetico(
                        grafo, 
                        geracoes=exec_geracoes, 
                        tam_populacao=exec_pop_size, 
                        taxa_mutacao=exec_taxa_mutacao
                    )
                    if func_bl:
                        ciclo_final, custo_final = func_bl(grafo, c_ga)
                    else:
                        ciclo_final, custo_final = c_ga, _
                    
                duracao = time.time() - t_ini
                soma_custos += custo_final
                soma_tempos += duracao
                
                if custo_final < melhor_global['custo']:
                    melhor_global['custo'] = custo_final
                    melhor_global['rota'] = ciclo_final

            dados = {
                'variante': nome_variante,
                'instancia': i + 1,
                'melhor_custo': melhor_global['custo'],
                'melhor_rota': melhor_global['rota'],
                'media_custo': soma_custos / 20,
                'media_tempo': soma_tempos / 20
            }
            
            if id_bl == BL_NONE:
                stats_genetico.append(dados)
            else:
                stats_memetico.append(dados)

    print("\nGerando relatórios...")
    gerar_relatorio_genetico(stats_genetico)
    gerar_relatorio_memetico(stats_memetico)

    print(f"\nTempo total: {time.time() - inicio_timer:.4f}s")

if __name__ == "__main__":
    main()
