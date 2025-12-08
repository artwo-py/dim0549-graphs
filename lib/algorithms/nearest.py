from lib.utils.converter import get_decimal
from decimal import Decimal

try:
    import numpy as np
    from numba import jit
    HAS_NUMBA = True
except ImportError:
    HAS_NUMBA = False

#  IMPLEMENTAÇÃO OTIMIZADA (JIT / NUMBA)
if HAS_NUMBA:
    @jit(nopython=True)
    def jit_nearest_neighbor(matriz, start_idx):
        """Kernel compilado: Lógica matemática pura em arrays."""
        n = matriz.shape[0]
        visitados = np.zeros(n, dtype=np.bool_)
        rota_indices = np.zeros(n + 1, dtype=np.int32)
        
        atual = start_idx
        visitados[atual] = True
        rota_indices[0] = atual
        custo_total = 0.0
        for i in range(1, n):
        
            proximo = -1
            menor_dist = np.inf
            
            for vizinho in range(n):
                if not visitados[vizinho]:
                    dist = matriz[atual, vizinho]
                    if dist < menor_dist:
                        menor_dist = dist
                        proximo = vizinho
            
            if proximo == -1: break 
                
            visitados[proximo] = True
            rota_indices[i] = proximo
            custo_total += menor_dist
            atual = proximo
            
        custo_total += matriz[atual, start_idx]
        rota_indices[n] = start_idx
        
        return rota_indices, custo_total

    def nearest_neighbor_acelerado(grafo, inicio=0):
        """
        Tarefa: (1*) Heurística construtiva Vizinho Mais Próximo (Acelerada).
        Info: Prepara os dados do grafo convertendo-os para matrizes numéricas e
              executa o kernel JIT compilado. Esta versão é otimizada para performance
              extrema utilizando Numba.

        E: grafo (Grafo) - O objeto Grafo a ser processado.
           inicio (str/int) - ID do vértice inicial.

        S: (list, float) - Uma tupla contendo:
                           - Lista com os IDs da rota encontrada.
                           - Custo total do ciclo.
        """
        # (Objeto -> Numpy)
        ids = [v.id for v in grafo.vertices]
        n = len(ids)
        mapa = {id_v: i for i, id_v in enumerate(ids)}
        
        # Cria matriz float32 
        matriz = np.full((n, n), np.inf, dtype=np.float32)
        
        for v in grafo.vertices:
            idx1 = mapa[v.id]
            for viz_id, peso in grafo.get_vizinhos(v.id).items():
                matriz[idx1, mapa[viz_id]] = float(peso)
        
        id_inicio = inicio.id if hasattr(inicio, "id") else inicio
        idx_inicio = mapa.get(id_inicio, 0)
        
        indices, custo = jit_nearest_neighbor(matriz, idx_inicio)
        
        rota_final = [ids[i] for i in indices]
        return rota_final, float(custo)

#  IMPLEMENTAÇÃO ORIGINAL (PYTHON PURO + DECIMAL)
def nearest_neighbor(grafo, inicio=0):
    """
    Tarefa: (1) Heurística construtiva Vizinho Mais Próximo (Padrão).
    Info: Constrói um ciclo hamiltoniano guloso escolhendo sempre a aresta de
          menor custo disponível a partir do vértice atual. Utiliza a biblioteca
          Decimal para precisão numérica.

    E: grafo (Grafo) - O objeto Grafo onde o ciclo será encontrado.
       inicio (str/int) - O vértice de início para o ciclo (ou seu ID).

    S: (list, Decimal) - Uma tupla contendo:
                         - Lista de vértices (IDs) no ciclo.
                         - Custo total do ciclo com precisão Decimal.
    """
    visitados = set()
    ciclo = []
    custo_total = get_decimal(0)
    atual = inicio.id if hasattr(inicio, "id") else inicio

    while len(visitados) < len(grafo.vertices):
        visitados.add(atual)
        ciclo.append(atual)

        vizinhos = grafo.get_vizinhos(atual)
        proximo = None
        menor_custo = Decimal('Infinity')

        for vizinho, peso in vizinhos.items():
            peso = get_decimal(peso)
            if vizinho not in visitados and peso < menor_custo:
                menor_custo = peso
                proximo = vizinho

        if proximo is None:
            break
        
        custo_total += menor_custo
        atual = proximo

    custo_total += grafo.get_peso(atual, inicio)
    ciclo.append(inicio)

    return ciclo, custo_total
