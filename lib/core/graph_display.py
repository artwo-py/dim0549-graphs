"""
Módulo:    display
Descriçao: Contém funções para gerar representações textuais das estruturas
           de dados de um objeto Grafo (lista, matriz de adjacência, etc.).
"""
from lib.core.graph import Grafo

def imprimir_lista_adj(grafo: Grafo):
    """
    Info: (Função de relatórios) Imprime a lista de adjacências de um grafo
          no console de forma legível.
    E: grafo (Grafo) - A instância do grafo a ser impressa.
    S: None.
    """
    print("\n--- Lista de Adjacências ---")
    if not grafo.lista_adj:
        print("Vazia.")
        return
    for vertice, vizinhos in sorted(grafo.lista_adj.items(), key=lambda item: str(item[0].id)):
        vizinhos_ids = sorted([v.id for v in vizinhos])
        print(f"{vertice.id}: {vizinhos_ids}")

def imprimir_matriz_adj(grafo: Grafo):
    """
    Info: (Função de relatórios) Imprime a matriz de adjacências de um grafo
          no console de forma legível.
    E: grafo (Grafo) - A instância do grafo a ser impressa.
    S: None.
    """
    print("\n--- Matriz de Adjacências ---")
    if not grafo.matriz_adj:
        print("Vazia.")
        return
    
    ids = [v.id for v in grafo.vertices]
    header = "  | " + " ".join(map(str, ids))
    print(header)
    print("-" * len(header))

    for i, linha in enumerate(grafo.matriz_adj):
        print(f"{ids[i]:<2}| " + " ".join(map(str, linha)))

def imprimir_matriz_incidencia(grafo: Grafo):
    """
    Info: (Função de relatórios) Imprime a matriz de incidência de um grafo
          no console de forma legível.
    E: grafo (Grafo) - A instância do grafo a ser impressa.
    S: None.
    """
    print("\n--- Matriz de Incidência ---")
    if not grafo.matriz_incidencia or not grafo.matriz_incidencia[0]:
        print("Vazia.")
        return
    
    header_arestas = [f"e{i+1}" for i in range(grafo.num_arestas())]
    print("  | " + " ".join(header_arestas))
    print("-" * (len(header_arestas) * 3 + 3))

    ids_vertices = [v.id for v in grafo.vertices]
    for i, linha in enumerate(grafo.matriz_incidencia):
        linha_formatada = " ".join(f"{val: >2}" for val in linha)
        print(f"{ids_vertices[i]:<2}| {linha_formatada}")