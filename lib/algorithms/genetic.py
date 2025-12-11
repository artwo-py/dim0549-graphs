import random

try:
    import numpy as np
    from numba import jit
    from lib.algorithms.local_searches import (
        jit_custo_caminho, 
        jit_shift_search, 
        jit_swap_search, 
        jit_two_opt
    )
    HAS_NUMBA = True    
except ImportError: 
    HAS_NUMBA = False

#  IMPLEMENTAÇÃO PADRÃO (PYTHON PURO)

def gerar_populacao(grafo, tam_populacao):
    vertices = [v.id for v in grafo.vertices]
    populacao = []
    for _ in range(tam_populacao):
        rota = vertices[:]
        random.shuffle(rota)
        populacao.append(rota + [rota[0]])
    return populacao

def avaliar_fitness(grafo, populacao):
    def calcular_custo(ciclo):
        soma = 0
        for i in range(len(ciclo) - 1):
            soma += grafo.get_peso(ciclo[i], ciclo[i+1])
        return soma
    
    populacao.sort(key=calcular_custo)
    return populacao

def selecao_torneio(grafo, populacao, k=3):
    competidores = random.sample(populacao, k)
    def custo(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma
    return min(competidores, key=custo)

def cruzamento_ox(pai1, pai2):
    genes_p1 = pai1[:-1]
    genes_p2 = pai2[:-1]
    tamanho = len(genes_p1)

    inicio = random.randint(0, tamanho - 1)
    fim = random.randint(inicio, tamanho - 1)

    filho = [None] * tamanho
    filho[inicio:fim+1] = genes_p1[inicio:fim+1]

    pos_atual = (fim + 1) % tamanho
    pos_p2 = (fim + 1) % tamanho

    while None in filho:
        gene = genes_p2[pos_p2]
        if gene not in filho:
            filho[pos_atual] = gene
            pos_atual = (pos_atual + 1) % tamanho
        pos_p2 = (pos_p2 + 1) % tamanho

    return filho + [filho[0]]

def aplicar_mutacao(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao and len(individuo) > 3:
        idx1 = random.randint(1, len(individuo) - 2)
        idx2 = random.randint(1, len(individuo) - 2)
        
        start, end = min(idx1, idx2), max(idx1, idx2)
        
        individuo[start:end+1] = individuo[start:end+1][::-1]
        
    return individuo

def algoritmo_genetico(grafo, geracoes=100, tam_populacao=100, taxa_mutacao=0.02):
    populacao = gerar_populacao(grafo, tam_populacao)
    
    for _ in range(geracoes):
        populacao = avaliar_fitness(grafo, populacao)
        
        nova_populacao = [list(ind) for ind in populacao[:10]]
        
        while len(nova_populacao) < tam_populacao:
            pai1 = selecao_torneio(grafo, populacao)
            pai2 = selecao_torneio(grafo, populacao)
            
            if random.random() < 0.9:
                filho = cruzamento_ox(pai1, pai2)
            else:
                filho = list(pai1)
                
            filho = aplicar_mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)
            
        populacao = nova_populacao
    
    populacao = avaliar_fitness(grafo, populacao)
    
    melhor = populacao[0]
    custo = 0
    for i in range(len(melhor)-1): custo += grafo.get_peso(melhor[i], melhor[i+1])
    
    return melhor, custo

#  IMPLEMENTAÇÃO ACELERADA (JIT / NUMBA)

if HAS_NUMBA:
    
    @jit(nopython=True)
    def jit_criar_individuo(num_vertices):
        rota_genes = np.arange(num_vertices, dtype=np.int32)
        np.random.shuffle(rota_genes)
        rota = np.empty(num_vertices + 1, dtype=np.int32)
        rota[:num_vertices] = rota_genes
        rota[num_vertices] = rota_genes[0]
        return rota

    @jit(nopython=True)
    def jit_selecao_torneio(populacao, matriz_adj, k=3):
        pop_size = len(populacao)
        melhor_indice = -1
        menor_custo = np.inf

        for _ in range(k):
            idx = np.random.randint(0, pop_size)
            custo = jit_custo_caminho(populacao[idx], matriz_adj)
            if custo < menor_custo:
                menor_custo = custo
                melhor_indice = idx
                
        return populacao[melhor_indice]

    @jit(nopython=True)
    def jit_crossover_ox(pai1, pai2):
        tamanho = len(pai1) - 1
        filho = np.full(tamanho + 1, -1, dtype=np.int32)
        
        r1 = np.random.randint(0, tamanho)
        r2 = np.random.randint(0, tamanho)
        start, end = min(r1, r2), max(r1, r2)
        
        filho[start:end+1] = pai1[start:end+1]
        
        pos_atual = (end + 1) % tamanho
        pos_p2 = (end + 1) % tamanho
        
        count = 0
        while count < tamanho:
            gene = pai2[pos_p2]
            in_child = False
            for k in range(start, end + 1):
                if filho[k] == gene:
                    in_child = True
                    break
            if not in_child:
                while filho[pos_atual] != -1:
                    pos_atual = (pos_atual + 1) % tamanho
                filho[pos_atual] = gene
            pos_p2 = (pos_p2 + 1) % tamanho
            count += 1
            
        filho[tamanho] = filho[0]
        return filho

    @jit(nopython=True)
    def jit_mutacao(filho, taxa_mutacao):
        n = len(filho)
        if np.random.random() < taxa_mutacao:
            limit = n - 1 
            if limit >= 2:
                idx1 = np.random.randint(0, limit)
                idx2 = np.random.randint(0, limit)
                
                start, end = min(idx1, idx2), max(idx1, idx2)
                
                while start < end:
                    temp = filho[start]
                    filho[start] = filho[end]
                    filho[end] = temp
                    start += 1
                    end -= 1
                
                filho[limit] = filho[0]
        return filho

    @jit(nopython=True)
    def jit_algoritmo_evolutivo(matriz_adj, pop_size=100, geracoes=100, taxa_mutacao=0.02, freq_bl=0.1, tipo_bl=0):
        n_cidades = matriz_adj.shape[0]
        
        pop_matrix = np.zeros((pop_size, n_cidades + 1), dtype=np.int32)
        for i in range(pop_size):
            pop_matrix[i] = jit_criar_individuo(n_cidades)
            
        melhor_custo_global = np.inf
        melhor_ind_global = np.empty(n_cidades + 1, dtype=np.int32)

        for _ in range(geracoes):
            
            custos = np.empty(pop_size, dtype=np.float32)
            for i in range(pop_size):
                custos[i] = jit_custo_caminho(pop_matrix[i], matriz_adj)
            
            indices_ordenados = np.argsort(custos)
            
            melhor_da_geracao_idx = indices_ordenados[0]
            melhor_da_geracao = pop_matrix[melhor_da_geracao_idx]
            custo_melhor = custos[melhor_da_geracao_idx]
            
            if custo_melhor < melhor_custo_global:
                melhor_custo_global = custo_melhor
                melhor_ind_global[:] = melhor_da_geracao[:]
            
            nova_pop = np.empty_like(pop_matrix)
            
            elitismo_count = 10
            for e in range(elitismo_count):
                idx = indices_ordenados[e]
                nova_pop[e] = pop_matrix[idx].copy()
            
            for k in range(elitismo_count, pop_size):
                pai1 = jit_selecao_torneio(pop_matrix, matriz_adj)
                pai2 = jit_selecao_torneio(pop_matrix, matriz_adj)
                
                if np.random.random() < 0.9:
                    filho = jit_crossover_ox(pai1, pai2)
                else:
                    filho = pai1.copy()
                
                filho = jit_mutacao(filho, taxa_mutacao)
                
                if tipo_bl > 0 and np.random.random() < freq_bl:
                    if tipo_bl == 1:
                        filho, _ = jit_shift_search(filho, matriz_adj)
                    elif tipo_bl == 2:
                        filho, _ = jit_swap_search(filho, matriz_adj)
                    elif tipo_bl == 3:
                        filho, _ = jit_two_opt(filho, matriz_adj)
                
                nova_pop[k] = filho
            
            pop_matrix = nova_pop

        return melhor_ind_global, melhor_custo_global
