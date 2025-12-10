from lib.core.graph import Grafo
from math import inf as INF
from lib.utils.converter import get_decimal

def cheapest_insertion(grafo : Grafo, v_inicial):
    """Implementa o algoritmo de Inserção Mais Próxima.
    
    Args:
        grafo (Grafo): O grafo onde o ciclo será encontrado.
        v_inicial (str): O vértice de início para o ciclo.

    Returns:
        ciclo: Uma lista contendo os vértices no ciclo.

    """
    distancias = grafo.matriz_adj

    nao_visitados = grafo.vertices
    nao_visitados.remove(v_inicial)

    v_prox = min(nao_visitados, key=lambda v:distancias[v_inicial][v])

    nao_visitados.remove(v_prox)

    circuito = [v_inicial, v_prox]

    while nao_visitados:
        min_custo_marginal = INF
        v_para_inserir = None
        posicao_insercao = None

        # encontra vértice mais barato
        for v in nao_visitados:
            #melhor aresta (u,w) para inserir v
            for i in range(len(circuito)):
                u = circuito[i]
                w = circuito[(i+1) % len(circuito)]

                custo_marginal = distancias[u][v] + distancias[v][w] - distancias[u][w]

                if custo_marginal < min_custo_marginal:
                    min_custo_marginal = custo_marginal
                    v_para_inserir = v
                    posicao_insercao = i+1
        
        #insere o melhor após verificar todos e achar melhor
        if v_para_inserir != None:
            circuito.insert(posicao_insercao, v_para_inserir)
            nao_visitados.remove(v_para_inserir)

    circuito.append(v_inicial)

    #calculando custo total
    custo_total = get_decimal(0)
    for i in range(len(circuito)-1):
        u = circuito[i]
        w = circuito[(i+1)]
        
        peso = grafo.get_peso(u, w)

        if peso is not None:
            custo_total += peso

    return circuito, custo_total