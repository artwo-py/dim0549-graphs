"""
Módulo:    BFS
Objetivo:  Implementa o algoritmo de Busca em Largura (Breadth-First Search).
Funções:   bfs(grafo, id_inicio)
"""
from collections import deque
from lib.core.graph import Grafo

def bfs(grafo: Grafo, id_inicio=None) -> (list, list):
    """
    Tarefas: (13), (19).
    Info: Percorre o grafo em largura a partir de um vértice, para grafo e dígrafo. 
          Lida com grafos desconexos e identifica arestas que não são da árvore de busca.

    Args:
        grafo (Grafo): O objeto grafo a ser percorrido.
        id_inicio (str/int, opcional): ID do vértice para iniciar a busca. 
                                        Se omitido, começa pelo primeiro vértice do grafo.

    Returns:
        (list, list): Tupla contendo:
                      - A ordem de visita em formato [(v, pai), ...].
                      - A lista de arestas encontradas que não pertencem à árvore.
    """
    adj = grafo.lista_adj 
    vertice_inicial_obj = None

    if id_inicio:
        vertice_inicial_obj = grafo.indice_vertices.get(str(id_inicio))
        if not vertice_inicial_obj:
            print(f"Alerta: Vértice inicial '{id_inicio}' não encontrado no grafo '{grafo.nome_arquivo}'.")
            return [], []
    elif grafo.vertices:
        vertice_inicial_obj = grafo.vertices[0]
    else:
        return [], [] 

    # CORREÇÃO: Trocado grafo.get_vertices() pelo acesso direto ao atributo grafo.vertices
    todos_vertices = grafo.vertices
    
    # Garante que a busca comece pelo vértice especificado
    ordem_de_busca = ([vertice_inicial_obj] + 
                      [v for v in todos_vertices if v != vertice_inicial_obj])
    
    visitados = set()
    pred = {} 
    ordem = [] 
    arestas_retorno = []

    for inicio_obj in ordem_de_busca:
        if inicio_obj in visitados:
            continue
            
        pred[inicio_obj] = "-"           
        fila = deque([inicio_obj])
        visitados.add(inicio_obj)
        
        while fila:
            atual_obj = fila.popleft()
            pred_obj = pred[atual_obj]
            pred_id = str(pred_obj.id) if pred_obj != "-" else "-"
            ordem.append((str(atual_obj.id), pred_id))
            
            # Adicionado sorted para garantir uma ordem de visita determinística
            for prox_obj in sorted(adj.get(atual_obj, []), key=lambda v: str(v.id)):
                if prox_obj not in visitados:
                    visitados.add(prox_obj)
                    pred[prox_obj] = atual_obj
                    fila.append(prox_obj)
                else:
                    # Verifica se a aresta não é a aresta de volta para o pai em grafos não direcionados
                    if not grafo.direcionado and pred.get(atual_obj) == prox_obj:
                        continue
                    aresta = (str(atual_obj.id), str(prox_obj.id))
                    arestas_retorno.append(aresta)
                    
    return ordem, arestas_retorno

