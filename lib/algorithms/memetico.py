import random
from decimal import Decimal
from lib.algorithms.local_searches import two_opt, shift, swap

try:
    import numpy as np
    from numba import jit
    from lib.algorithms.local_searches import jit_custo_caminho, jit_two_opt
    HAS_NUMBA = True    
except ImportError: 
    HAS_NUMBA = False

#  FUNÇÕES ACELERADAS (JIT / NUMBA)
if HAS_NUMBA:
    #funcoes memetico em jit
    @jit(nopython=True)
    def jit_criar_individuo(num_vertices):
        """Cria um indivíduo aleatório (rota) como array NumPy."""
        rota_genes = np.arange(num_vertices, dtype=np.int32)
        np.random.shuffle(rota_genes)
        rota = np.empty(num_vertices + 1, dtype=np.int32)
        rota[:num_vertices] = rota_genes
        rota[num_vertices] = rota_genes[0]
        return rota

    @jit(nopython=True)
    def jit_selecao_torneio(matriz_adj, populacao, k=3):
        """Seleção por torneio: retorna o índice do melhor competidor"""
        pop_size = len(populacao)
        melhor_indice = -1
        menor_custo = np.inf

        indices_competidores = np.random.choice(pop_size, k, replace=False)

        for i in indices_competidores:
            custo = jit_custo_caminho(populacao[i], matriz_adj)
            if custo < menor_custo:
                menor_custo = custo
                melhor_indice = i
        
        return melhor_indice

    @jit(nopython=True)
    def jit_mutacao_troca(ciclo):
        tamanho_genes = len(ciclo) - 1
        if tamanho_genes >= 2:
            idx = np.random.choice(tamanho_genes, 2, replace=False)
            idx1, idx2 = idx[0], idx[1]
            
            ciclo[idx1], ciclo[idx2] = ciclo[idx2], ciclo[idx1]
            
            ciclo[tamanho_genes] = ciclo[0]
            
        return ciclo

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
    def memetico_acelerado(matriz_adj, pop_size=50, geracoes=15, taxa_mutacao=0.1, frequencia_bl=0.1):
        """
        Tarefa: Execução otimizada de algoritmo memético.
        Info: Implementação de alta performance compilada (JIT). Utiliza Ordered Crossover,
              seleção por torneio e busca local 2-opt, inversao.
              
        E: matriz_adj (np.array) - Matriz de adjacência (pesos) do grafo.
           pop_size (int) - Tamanho da população.
           geracoes (int) - Número de iterações do ciclo evolutivo.
           taxa_mutacao (float) - Probabilidade de mutação por indivíduo.
           
        S: (np.array, float) - Uma tupla contendo:
                               - Array de índices representando a melhor rota encontrada.
                               - Custo total (fitness) dessa rota.
        """
        num_vertices = matriz_adj.shape[0]

        # 1. Inicialização da População
        populacao = [
            jit_criar_individuo(num_vertices) for _ in range(pop_size)
        ]
        
        melhor_custo_global = np.inf
        melhor_rota_global = np.empty_like(populacao[0])

        for _ in range(geracoes):
            custos = np.empty(pop_size, dtype=matriz_adj.dtype)
            for i in range(pop_size):
                custos[i] = jit_custo_caminho(populacao[i], matriz_adj)

            idx_melhor_atual = np.argmin(custos)
            custo_melhor_atual = custos[idx_melhor_atual]
            rota_melhor_atual = populacao[idx_melhor_atual]

            if custo_melhor_atual < melhor_custo_global:
                melhor_custo_global = custo_melhor_atual
                melhor_rota_global[:] = rota_melhor_atual[:]

            nova_populacao = [rota_melhor_atual.copy()]

            while len(nova_populacao) < pop_size:
                idx_pai1 = jit_selecao_torneio(matriz_adj, populacao)
                idx_pai2 = jit_selecao_torneio(matriz_adj, populacao)
                
                pai1 = populacao[idx_pai1]
                pai2 = populacao[idx_pai2]

                filho = jit_crossover_ox(pai1, pai2)

                if np.random.rand() < taxa_mutacao:
                    filho = jit_mutacao_troca(filho)

                if np.random.rand() < frequencia_bl:
                    filho, _ = jit_two_opt(filho, matriz_adj) 

                nova_populacao.append(filho)

            populacao = nova_populacao

        # Retorna o melhor global encontrado após todas as gerações
        return melhor_rota_global, melhor_custo_global

def criar_individuo(vertices_id):
    rota = vertices_id[:]
    random.shuffle(rota)
    return rota + [rota[0]]

def calcular_fitness(grafo, ciclo):
    soma = Decimal(0)
    for i in range(len(ciclo) - 1):
        soma += grafo.get_peso(ciclo[i], ciclo[i+1])
    return soma

def selecao_torneio(grafo, populacao, k = 3):
    competidores = random.sample(populacao, k)
    return min(competidores, key=lambda c: calcular_fitness(grafo, c))

def crossover_ox(pai1, pai2):
    genes_p1 = pai1[:-1]
    genes_p2 = pai2[:-1]
    tamanho = len(genes_p1)
    inicio = random.randint(0, tamanho - 1)
    fim = random.randint(inicio, tamanho - 1)
    filho_genes: List[int] = [0] * tamanho
    filho_genes[inicio:fim+1] = genes_p1[inicio:fim+1]

    pos_atual = (fim + 1) % tamanho
    pos_p2 = (fim + 1) % tamanho

    while None in filho_genes: # preenche os genes restantes na ordem de P2
        gene = genes_p2[pos_p2]
        if gene not in filho_genes:
            filho_genes[pos_atual] = gene
            pos_atual = (pos_atual + 1) % tamanho
        pos_p2 = (pos_p2 + 1) % tamanho
    return filho_genes + [filho_genes[0]]

def mutacao_troca(ciclo):
    genes = ciclo[:-1]
    if len(genes) >= 2:
        idx1, idx2 = random.sample(range(len(genes)), 2)
        genes[idx1], genes[idx2] = genes[idx2], genes[idx1]
        ciclo[:] = genes + [genes[0]]

def memetico(grafo, geracoes: int=100, tam_populacao: int=50,
                  taxa_mutacao: float =0.1, frequencia_bl: float=0.1):
    """
    Tarefa: (4) Implementa um algoritmo memético com 2-OPT.
    Info: Utiliza representação de rotas por listas de IDs, crossover ordenado e seleção por torneio.

    E: grafo (Grafo) - O objeto Grafo contendo vértices e arestas.
       geracoes (int) - Número de gerações a evoluir.
       tam_populacao (int) - Quantidade de indivíduos na população.
       taxa_mutacao (float) - Probabilidade de mutação.
       frequencia_bl (float) - Probabilidade de aplicar busca local.

    S: (list, float) - Uma tupla contendo:
                       - Lista com os IDs dos vértices da melhor rota.
                       - Custo total calculado dessa rota.    """
    vertices_id = [v.id for v in grafo.vertices]
    
    populacao = [criar_individuo(vertices_id) for _ in range(tam_populacao)]

    for _ in range(geracoes):
        populacao.sort(key=lambda c: calcular_fitness(grafo, c))

        nova_populacao = [populacao[0]]

        while len(nova_populacao) < tam_populacao:
            pai1 = selecao_torneio(grafo, populacao)
            pai2 = selecao_torneio(grafo, populacao)

            filho = crossover_ox(pai1, pai2)

            if random.random() < taxa_mutacao:
                mutacao_troca(filho)

            if random.random() < frequencia_bl:
                filho_otimizado, _ = two_opt(grafo, filho)
                filho = filho_otimizado
                
            nova_populacao.append(filho)

        populacao = nova_populacao

    melhor_solucao = min(populacao, key=lambda c: calcular_fitness(grafo, c))
    return melhor_solucao, calcular_fitness(grafo, melhor_solucao)