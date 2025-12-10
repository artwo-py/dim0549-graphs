import random
from lib.algorithms.local_searches import shift

try:
    import numpy as np
    from numba import jit
    from lib.algorithms.local_searches import jit_custo_caminho
    HAS_NUMBA = True    
except ImportError: 
    HAS_NUMBA = False

# Implementação original, lenta, interpretada e com o objeto Graph e seus derivados
def gerar_populacao(grafo, tam_populacao):
    """
    (1) Geração da População Inicial.
    Info: Cria indivíduos com permutações aleatórias dos vértices.
    E: grafo (Grafo), tam_populacao (int)
    S: list - Lista de ciclos (listas de IDs).
    """
    vertices = [v.id for v in grafo.vertices]
    populacao = []
    for _ in range(tam_populacao):
        rota = vertices[:]
        random.shuffle(rota)
        populacao.append(rota + [rota[0]])
    return populacao

def avaliar_fitness(grafo, populacao):
    """
    (2) Avaliação de Fitness.
    Info: Calcula o custo de cada cromossomo e ordena a população pelo melhor (menor custo).
    E: grafo (Grafo), populacao (list)
    S: list - População ordenada por fitness.
    """
    def calcular_custo(ciclo):
        soma = 0
        for i in range(len(ciclo) - 1):
            soma += grafo.get_peso(ciclo[i], ciclo[i+1])
        return soma
    
    populacao.sort(key=calcular_custo)
    return populacao

def selecao_torneio(grafo, populacao, k=3):
    """
    (3.1) Seleção (Torneio).
    Info: Seleciona um pai comparando k indivíduos aleatórios.
    """
    competidores = random.sample(populacao, k)
    def custo(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma
    return min(competidores, key=custo)

def cruzamento_ox(pai1, pai2):
    """
    (3.2) Cruzamento (Ordered Crossover - OX1).
    Info: Preserva ordem relativa e garante integridade do ciclo.
    """
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
    """
    (3.3) Mutação (Swap).
    Info: Troca dois genes de lugar com base na taxa/probabilidade.
    """
    if random.random() < taxa_mutacao and len(individuo) > 3:
        idx1, idx2 = random.sample(range(1, len(individuo) - 1), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo

def criar_nova_geracao(grafo, populacao, taxa_mutacao):
    """
    (3) Nova Geração.
    Info: Orquestra Seleção, Cruzamento e Mutação para criar novos indivíduos.
    """
    tam_pop = len(populacao)
    nova_populacao = []
    
    # Elitismo
    nova_populacao.append(populacao[0])
    
    while len(nova_populacao) < tam_pop:
        pai1 = selecao_torneio(grafo, populacao)
        pai2 = selecao_torneio(grafo, populacao)
        
        filho = cruzamento_ox(pai1, pai2)
        filho = aplicar_mutacao(filho, taxa_mutacao)
        
        nova_populacao.append(filho)
        
    return nova_populacao

def algoritmo_genetico(grafo, geracoes=100, tam_populacao=50, taxa_mutacao=0.1):
    """
    Tarefa 2: Orquestrador do Algoritmo Genético (Padrão).
    Info: Executa o ciclo evolutivo.
    """
    # 1 - Início
    populacao = gerar_populacao(grafo, tam_populacao)
    
    # 5 - Teste (Loop de Gerações)
    for _ in range(geracoes):
        # 2 - Fitness
        populacao = avaliar_fitness(grafo, populacao)
        
        # 3 - Nova Geração & 4 - Renovar
        populacao = criar_nova_geracao(grafo, populacao, taxa_mutacao)
    
    populacao = avaliar_fitness(grafo, populacao)
    melhor_solucao = populacao[0]
    
    custo_final = 0
    for i in range(len(melhor_solucao) - 1):
        custo_final += grafo.get_peso(melhor_solucao[i], melhor_solucao[i+1])
        
    return melhor_solucao, custo_final

# Implementação acelerada com numba, rápida, compilada e com matriz de adj direta float32
if HAS_NUMBA:
    
    @jit(nopython=True)
    def jit_selecao_torneio(populacao, fitness, top_half):
        """
        (3.1) Seleção JIT.
        Info: Seleciona índice de um pai via torneio simplificado na metade superior.
        """
        idx = np.random.randint(0, top_half)
        return populacao[idx]

    @jit(nopython=True)
    def jit_crossover_ox(pai1, pai2):
        """
        (3.2) Cruzamento OX1 JIT.
        Info: Implementação vetorial do Ordered Crossover.
        """
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
        """
        (3.3) Mutação Swap JIT.
        Info: Realiza a troca de genes se a probabilidade for atendida.
        """
        n = len(filho)
        if np.random.random() < taxa_mutacao:
            idx_a = np.random.randint(1, n - 1)
            idx_b = np.random.randint(1, n - 1)
            while idx_a == idx_b:
                idx_b = np.random.randint(1, n - 1)
                
            temp = filho[idx_a]
            filho[idx_a] = filho[idx_b]
            filho[idx_b] = temp
        return filho

    @jit(nopython=True)
    def jit_algoritmo_genetico(matriz_adj, pop_size=50, geracoes=100, taxa_mutacao=0.2):
        """
        Tarefa: Orquestrador do Algoritmo Genético (Acelerado JIT).
        Info: Implementa o ciclo (1) a (5) inteiramente compilado para a CPU.
        """
        n_cidades = matriz_adj.shape[0]
        
        # Geração da População Inicial
        populacao = np.zeros((pop_size, n_cidades + 1), dtype=np.int32)
        base = np.arange(n_cidades, dtype=np.int32)
        for i in range(pop_size):
            np.random.shuffle(base)
            populacao[i, :n_cidades] = base
            populacao[i, n_cidades] = base[0]
            
        # Teste: Loop de Gerações
        for _ in range(geracoes):
            
            #Fitness: Avaliar cada cromossomo
            fitness = np.zeros(pop_size, dtype=np.float32)
            for i in range(pop_size):
                fitness[i] = jit_custo_caminho(populacao[i], matriz_adj)
            
            # Ordenação para Elitismo e Seleção
            idx_sorted = np.argsort(fitness)
            populacao = populacao[idx_sorted]
            
            # Nova Geração (Preparo)
            nova_pop = np.empty_like(populacao)
            nova_pop[0] = populacao[0] # Elitismo
            
            top_half = pop_size // 2
            
            # Loop de Reprodução
            for k in range(1, pop_size):
                # Seleção
                pai1 = jit_selecao_torneio(populacao, fitness, top_half)
                pai2 = jit_selecao_torneio(populacao, fitness, top_half)
                
                # Cruzamento
                filho = jit_crossover_ox(pai1, pai2)
                
                # Mutação
                filho = jit_mutacao(filho, taxa_mutacao)
                
                nova_pop[k] = filho
            
            # Renovar População
            populacao = nova_pop

        melhor_ind = populacao[0]
        custo_final = jit_custo_caminho(melhor_ind, matriz_adj)
        
        return melhor_ind, custo_final
