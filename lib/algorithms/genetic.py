import random
from lib.algorithms.local_searches import shift

try:
    import numpy as np
    from numba import jit
    from lib.algorithms.local_searches import jit_custo_caminho, jit_shift_search
    HAS_NUMBA = True    
except ImportError: 
    HAS_NUMBA = False

# --- FUNÇÕES ACELERADAS (JIT - COMPILAÇÃO TOTAL) ---
if HAS_NUMBA:
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
    def executar_ga_acelerado(matriz_adj, pop_size=50, geracoes=100, taxa_mutacao=0.2):
        """
        Tarefa: (3*) Execução otimizada de Algoritmo Genético.
        Info: Implementação de alta performance compilada (JIT). Utiliza Ordered Crossover (OX1),
              seleção por torneio, mutação Swap e aplica busca local Shift no melhor indivíduo.
              
        E: matriz_adj (np.array) - Matriz de adjacência (pesos) do grafo.
           pop_size (int) - Tamanho da população.
           geracoes (int) - Número de iterações do ciclo evolutivo.
           taxa_mutacao (float) - Probabilidade de mutação por indivíduo.
           
        S: (np.array, float) - Uma tupla contendo:
                               - Array de índices representando a melhor rota encontrada.
                               - Custo total (fitness) dessa rota.
        """
        n_cidades = matriz_adj.shape[0]
        
        populacao = np.zeros((pop_size, n_cidades + 1), dtype=np.int32)
        base = np.arange(n_cidades, dtype=np.int32)
        
        for i in range(pop_size):
            np.random.shuffle(base)
            populacao[i, :n_cidades] = base
            populacao[i, n_cidades] = base[0]
            
        for _ in range(geracoes):
            fitness = np.zeros(pop_size, dtype=np.float32)
            for i in range(pop_size):
                fitness[i] = jit_custo_caminho(populacao[i], matriz_adj)
            
            idx_sorted = np.argsort(fitness)
            populacao = populacao[idx_sorted]
            
            nova_pop = np.empty_like(populacao)
            nova_pop[0] = populacao[0] # Elitismo
            
            # Crossover e Mutação
            top_half = pop_size // 2
            
            for k in range(1, pop_size):
                idx_p1 = np.random.randint(0, top_half)
                idx_p2 = np.random.randint(0, top_half)
                
                filho = jit_crossover_ox(populacao[idx_p1], populacao[idx_p2])
                
                # Mutação (Swap simples)
                if np.random.random() < taxa_mutacao:
                    idx_a = np.random.randint(1, n_cidades - 1)
                    idx_b = np.random.randint(1, n_cidades - 1)
                    while idx_a == idx_b:
                        idx_b = np.random.randint(1, n_cidades - 1)
                        
                    temp = filho[idx_a]
                    filho[idx_a] = filho[idx_b]
                    filho[idx_b] = temp
                    
                nova_pop[k] = filho
            
            populacao = nova_pop

        melhor_ind = populacao[0]
        melhor_ind, custo_final = jit_shift_search(melhor_ind, matriz_adj)
        
        return melhor_ind, custo_final

# --- FUNÇÕES PADRÃO (Python Puro - Lento) ---
def algoritmo_genetico(grafo, geracoes=100, tam_populacao=50, taxa_mutacao=0.1):
    """
    Tarefa: (3) Execução padrão de Algoritmo Genético para o PCV.
    Info: Utiliza representação de rotas por listas de IDs, crossover ordenado (OX1) e seleção por torneio.
          Esta versão é flexível mas menos performática que a acelerada.

    E: grafo (Grafo) - O objeto Grafo contendo vértices e arestas.
       geracoes (int) - Número de gerações a evoluir.
       tam_populacao (int) - Quantidade de indivíduos na população.
       taxa_mutacao (float) - Probabilidade de mutação (0.0 a 1.0).

    S: (list, float) - Uma tupla contendo:
                       - Lista com os IDs dos vértices da melhor rota.
                       - Custo total calculado dessa rota.
    """
    vertices = [v.id for v in grafo.vertices]
    def criar_individuo():
        rota = vertices[:]
        random.shuffle(rota)
        return rota + [rota[0]]
    def calcular_fitness(ciclo):
        soma = 0
        for i in range(len(ciclo) - 1):
            soma += grafo.get_peso(ciclo[i], ciclo[i+1])
        return soma
    populacao = [criar_individuo() for _ in range(tam_populacao)]
    for _ in range(geracoes):
        populacao.sort(key=calcular_fitness)
        nova_populacao = [populacao[0]]
        while len(nova_populacao) < tam_populacao:
            pai1 = selecao_torneio(grafo, populacao)
            pai2 = selecao_torneio(grafo, populacao)
            filho = crossover_ox(pai1, pai2)
            if random.random() < taxa_mutacao:
                mutacao_troca(filho)
            nova_populacao.append(filho)
        populacao = nova_populacao
    melhor_solucao = min(populacao, key=calcular_fitness)
    return melhor_solucao, calcular_fitness(melhor_solucao)

def selecao_torneio(grafo, populacao, k=3):
    competidores = random.sample(populacao, k)
    def custo(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma
    return min(competidores, key=custo)

def crossover_ox(pai1, pai2):
    genes_p1 = pai1[:-1]
    genes_p2 = pai2[:-1]
    tamanho = len(genes_p1)
    inicio = random.randint(0, tamanho - 1)
    fim = random.randint(inicio, tamanho - 1)
    filho_genes = [None] * tamanho
    filho_genes[inicio:fim+1] = genes_p1[inicio:fim+1]
    pos_atual = (fim + 1) % tamanho
    pos_p2 = (fim + 1) % tamanho
    while None in filho_genes:
        gene = genes_p2[pos_p2]
        if gene not in filho_genes:
            filho_genes[pos_atual] = gene
            pos_atual = (pos_atual + 1) % tamanho
        pos_p2 = (pos_p2 + 1) % tamanho
    return filho_genes + [filho_genes[0]]

def mutacao_troca(ciclo):
    if len(ciclo) > 3:
        idx1, idx2 = random.sample(range(1, len(ciclo) - 1), 2)
        ciclo[idx1], ciclo[idx2] = ciclo[idx2], ciclo[idx1]
