from lib.core.graph import Grafo


try:
    import numpy as np
    from numba import jit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

#  FUNÇÕES ACELERADAS (JIT / NUMBA)
if HAS_NUMBA:
    @jit(nopython=True)
    def jit_custo_caminho(rota, matriz):
        """Calcula custo total de uma rota (indices) via matriz de pesos."""
        soma = 0.0
        n = len(rota)
        for i in range(n - 1):
            soma += matriz[rota[i], rota[i+1]]
        return soma

    @jit(nopython=True)
    def jit_two_opt(rota, matriz):
        """
        Versão compilada (JIT) da heurística 2-opt.
        Inverte segmentos da rota para reduzir cruzamentos.
        """
        melhor_rota = rota.copy()
        melhor_custo = jit_custo_caminho(melhor_rota, matriz)
        n = len(rota)
        melhoria = True
        
        while melhoria:
            melhoria = False
            for i in range(1, n - 2):
                for j in range(i + 1, n - 1):
                    
                    nova_rota = np.empty_like(melhor_rota)
                    
                    nova_rota[:i] = melhor_rota[:i]           
                    nova_rota[i:j] = melhor_rota[i:j][::-1]   
                    nova_rota[j:] = melhor_rota[j:]           
                    
                    novo_custo = jit_custo_caminho(nova_rota, matriz)
                    
                    if novo_custo < melhor_custo:
                        melhor_rota = nova_rota
                        melhor_custo = novo_custo
                        melhoria = True
                        break 
                if melhoria: break
        
        return melhor_rota, melhor_custo

    @jit(nopython=True)
    def jit_shift_search(rota, matriz):
        """Versão compilada (JIT) da heurística Shift para arrays Numpy."""
        melhor_rota = rota.copy()
        melhor_custo = jit_custo_caminho(melhor_rota, matriz)
        n = len(rota)
        melhoria = True
        
        while melhoria:
            melhoria = False
            for i in range(1, n - 1):
                for j in range(1, n - 1):
                    if i == j: continue
                    
                    # Simulação manual de pop/insert usando arrays
                    temp = np.zeros(n-1, dtype=np.int32)
                    idx = 0
                    val = melhor_rota[i]
                    
                    # Remove i
                    for k in range(n):
                        if k != i:
                            temp[idx] = melhor_rota[k]
                            idx += 1
                    
                    # Insere val na posição j
                    novo_ciclo = np.zeros(n, dtype=np.int32)
                    novo_ciclo[:j] = temp[:j]
                    novo_ciclo[j] = val
                    novo_ciclo[j+1:] = temp[j:]
                    
                    novo_custo = jit_custo_caminho(novo_ciclo, matriz)
                    
                    if novo_custo < melhor_custo:
                        melhor_rota = novo_ciclo
                        melhor_custo = novo_custo
                        melhoria = True
                        break 
                if melhoria: break
                
        return melhor_rota, melhor_custo

    def two_opt_acelerado(grafo, ciclo_ids):
        """Wrapper que prepara os dados e chama o 2-opt JIT."""
        # (Grafo -> Matriz/Indices)
        ids = [v.id for v in grafo.vertices]
        mapa = {id_v: i for i, id_v in enumerate(ids)}
        n = len(ids)
        
        # Matriz float32 para velocidade
        matriz = np.full((n, n), np.inf, dtype=np.float32)
        for v in grafo.vertices:
            idx1 = mapa[v.id]
            for viz_id, peso in grafo.get_vizinhos(v.id).items():
                matriz[idx1, mapa[viz_id]] = float(peso)
        
        # Converte rota de IDs para Índices
        indices_rota = np.array([mapa[vid] for vid in ciclo_ids], dtype=np.int32)
        
        melhor_indices, melhor_custo = jit_two_opt(indices_rota, matriz)
        
        rota_final = [ids[i] for i in melhor_indices]
        return rota_final, float(melhor_custo)

#  FUNÇÕES PADRÃO (PYTHON PURO / OBJETOS)
def two_opt(grafo, ciclo):
    """Busca melhoria de um ciclo usando a heurística 2-opt."""
    melhoria = True
    melhor_ciclo = ciclo[:]

    def custo_total(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma

    melhor_custo = custo_total(melhor_ciclo)

    while melhoria:
        melhoria = False
        for i in range(1, len(melhor_ciclo) - 2):
            for j in range(i+1, len(melhor_ciclo) - 1):

                novo_ciclo = (
                    melhor_ciclo[:i] +
                    list(reversed(melhor_ciclo[i:j])) +
                    melhor_ciclo[j:]
                )

                novo_custo = custo_total(novo_ciclo)
                if novo_custo < melhor_custo:
                    melhor_ciclo = novo_ciclo
                    melhor_custo = novo_custo
                    melhoria = True
                    break 
            if melhoria: break

    return melhor_ciclo, melhor_custo

def shift(grafo, ciclo):
    """Busca melhoria de um ciclo usando a heurística Shift (ou Relocate)."""
    melhoria = True
    melhor_ciclo = ciclo[:]

    def custo_total(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma

    melhor_custo = custo_total(melhor_ciclo)

    while melhoria:
        melhoria = False
        for i in range(1, len(melhor_ciclo) - 1): 
            for j in range(1, len(melhor_ciclo) - 1):
                if i == j: continue

                candidato = melhor_ciclo[:]
                cidade = candidato.pop(i)
                candidato.insert(j, cidade)

                novo_custo = custo_total(candidato)

                if novo_custo < melhor_custo:
                    melhor_ciclo = candidato
                    melhor_custo = novo_custo
                    melhoria = True
                    break
            if melhoria: break

    return melhor_ciclo, melhor_custo


def swap(grafo: Grafo, ciclo_inicial):
    """Busca melhoria de um ciclo usando a heurística Vertex Swap (troca de dois vértices)."""
    
    def custo_total(c):
        soma = 0
        for i in range(len(c) - 1):
            soma += grafo.get_peso(c[i], c[i+1])
        return soma
    
    ciclo_atual = ciclo_inicial[:] 
    custo_atual = custo_total(ciclo_atual)
    n = len(ciclo_atual) - 1 # núm. vértices únicos (0 a tam_ciclo_orig-1)
    
    melhoria_encontrada = True

    while melhoria_encontrada:
        melhoria_encontrada = False
        melhor_delta_custo = 0.0
        melhor_i, melhor_j = -1, -1

        # i vai de 0 até (tam_ciclo_orig - 2) e j vai de i+1 até (tam_ciclo_orig - 1).
        for i in range(0, n - 1): 
            for j in range(i + 1, n):

                v_i = ciclo_atual[i]
                v_j = ciclo_atual[j]
                
                v_i_anterior = ciclo_atual[(i - 1 + n) % n]
                v_i_posterior = ciclo_atual[(i + 1) % n]
                v_j_anterior = ciclo_atual[(j - 1 + n) % n]
                v_j_posterior = ciclo_atual[(j + 1) % n]
                
                delta_custo = 0.0
                
                if j == i + 1:  #adjacentes são 3 arestas ( - A - B - )
                    custo_removido = (
                        grafo.get_peso(v_i_anterior, v_i) + 
                        grafo.get_peso(v_i, v_j) + 
                        grafo.get_peso(v_j, v_j_posterior)
                    )
                    custo_adicionado = (
                        grafo.get_peso(v_i_anterior, v_j) + 
                        grafo.get_peso(v_j, v_i) + 
                        grafo.get_peso(v_i, v_j_posterior)
                    )

                else:   # separados são 4 arestas ( - A - ? - B - )
                    custo_removido = (
                        grafo.get_peso(v_i_anterior, v_i) + grafo.get_peso(v_i, v_i_posterior) + 
                        grafo.get_peso(v_j_anterior, v_j) + grafo.get_peso(v_j, v_j_posterior)
                    )
                    custo_adicionado = (
                        grafo.get_peso(v_i_anterior, v_j) + grafo.get_peso(v_j, v_i_posterior) + 
                        grafo.get_peso(v_j_anterior, v_i) + grafo.get_peso(v_i, v_j_posterior)
                    )

                delta_custo = custo_adicionado - custo_removido

                if delta_custo < melhor_delta_custo:
                    melhor_delta_custo = delta_custo
                    melhor_i = i
                    melhor_j = j
                    melhoria_encontrada = True
        
        if melhoria_encontrada:
            ciclo_atual[melhor_i], ciclo_atual[melhor_j] = ciclo_atual[melhor_j], ciclo_atual[melhor_i]
            custo_atual += melhor_delta_custo
            if melhor_i == 0 or melhor_j == 0:
                ciclo_atual[n] = ciclo_atual[0]
            
    return ciclo_atual, custo_atual