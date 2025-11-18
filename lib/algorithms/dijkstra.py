"""
Módulo:    Dijkstra
Objetivo:  Implementa o algoritmo de Dijkstra para encontrar a árvore geradora mínima.
Funções:   dijkstra(grafo: Grafo, inicio_id=None)
"""

from lib.core.graph import Grafo
import itertools
import heapq
from math import inf as INF

# desempatador
count = itertools.count()

def dijkstra(grafo: Grafo, inicio_id=None):
    """
    Tarefa: (5).
    Info: Implementa o algoritmo de Dijkstra para encontrar a Árvore de Caminho Mínimo (Shortest Path Tree) de um grafo ponderado, gerando os caminhos de menor custo a partir de um vértice de origem.

    Args:
        grafo (Grafo): O objeto grafo ponderado.
        inicio_id: O id do Vertice pelo qual se deseja iniciar. Se não for fornecido (None), será iniciado pelo 1º vértice na lista de vértices do grafo (grafo.vertices[0]).

    Returns:
        spt (Grafo): O subgrafo (Árvore de Caminho Mínimo) gerado pelo algoritmo.
    """

    distancias = {vertice: INF for vertice in grafo.vertices}
    predecessores = {vertice: None for vertice in grafo.vertices}

    for a in grafo.arestas:
        if a.peso is None:
            raise ValueError("Todas as arestas precisam ser ponderadas para execução do algoritmo.")

    if inicio_id is not None:
        s = grafo.indice_vertices.get(str(inicio_id))
        if s is None:
            raise ValueError(f"Vértice com ID '{inicio_id}' não encontrado.")
    else:
        s = grafo.vertices[0]
        
    distancias[s] = 0

    #Iniciando loop que visita todas as arestas
    fila_prioridade = [(0, next(count), s)]
    while fila_prioridade:
        dist_u, _, u = heapq.heappop(fila_prioridade)
        
        # já achou caminho melhor
        if dist_u > distancias[u]:
            continue
        
        # vizinhos
        arestas_u = [
            aresta for aresta in grafo.arestas
            if aresta.v1 == u
        ]

        #relaxamento
        for aresta in arestas_u:
            v = aresta.v2
            peso_uv = aresta.peso if aresta.peso is not None else 0

            nova_distancia = distancias[u] + peso_uv

            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                predecessores[v] = u

                heapq.heappush(fila_prioridade, (nova_distancia, next(count), v))

    # construindo grafo
    spt = Grafo(direcionado=grafo.direcionado, ponderado=grafo.ponderado, nome_arquivo="DIJKSTRA")
    
    for vertice in grafo.vertices:      
        spt.adicionar_vertice(vertice.id) 
        
    for v, pred_v in predecessores.items():
        if pred_v is not None:
            v_id = v.id
            pred_id = pred_v.id
            
            aresta_original = grafo.get_aresta(pred_id, v_id)
            
            if aresta_original:
                peso = aresta_original.peso
                spt.adicionar_aresta(pred_id, v_id, w=peso)
            else:
                 spt.adicionar_aresta(pred_id, v_id, 0)

    return spt, distancias, predecessores



def formatar_caminho_dijkstra(grafo, id_inicio: str, id_fim: str):
    """
    Executa Dijkstra (com a assinatura modificada), reconstrói o caminho 
    de custo mínimo e formata o texto para o vértice final especificado.

    E: grafo (Grafo)
    E: id_inicio (str)
    E: id_fim (str)
    S: (str, list[Vertice] or None)
    """
    titulo = f"\n==== CAMINHO MAIS CURTO (DIJKSTRA {id_inicio} -> {id_fim}) ===="

    if not grafo.ponderado:
        return titulo + "\n  Algoritmo não aplicável (grafo não ponderado).", None
    
    try:
        _, distancias_obj, predecessores_obj = dijkstra(grafo, id_inicio)

        dist_id = {v.id: d for v, d in distancias_obj.items()}
        pred_id = {v.id: p.id if p else None for v, p in predecessores_obj.items()}
        
        report = ""
        
        custo = dist_id.get(str(id_fim), INF) 
        
        if custo == INF:
            report += f"  Não há caminho entre {id_inicio} e {id_fim}."
            return titulo + "\n" + report, None

        caminho_ids = []
        atual = str(id_fim)

        if atual not in pred_id:
            report += f"  Vértice final '{id_fim}' não encontrado no grafo."
            return titulo + "\n" + report, None

        while atual is not None and atual != "":
            caminho_ids.append(atual)
            if atual == str(id_inicio):
                break

            if atual not in pred_id:
                 break
                 
            atual = pred_id[atual]

        caminho_ids.reverse()
        
        if not caminho_ids or caminho_ids[0] != str(id_inicio) or caminho_ids[-1] != str(id_fim):
            report += f"  Não foi possível reconstruir um caminho válido de {id_inicio} para {id_fim}."
            return titulo + "\n" + report, None
            
        report += f"  Custo: {custo}\n"
        report += "  Caminho: " + " -> ".join(caminho_ids)
        
        vertices_map = {v.id: v for v in grafo.vertices}
        caminho_vertices = [vertices_map[v_id] for v_id in caminho_ids]
        
        return titulo + "\n" + report, caminho_vertices
        
    except Exception as e:
        return titulo + f"\n  Erro inesperado ao executar Dijkstra: {e}", None