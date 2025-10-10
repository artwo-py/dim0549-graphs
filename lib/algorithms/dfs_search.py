# dfs_search.py

from ..core.graph import Grafo, Aresta

def busca_profundidade_com_classificacao(grafo, id_raiz):
    """
    (20) Busca em profundidade, com determinação de profundidade de entrada e de saída
    de cada vértice, arestas de árvore, retorno, avanço e cruzamento
    
    Args:
        grafo: O objeto Grafo (deve ser direcionado para a classificação fornecida).
        id_raiz: O ID do vértice inicial da busca.
    Returns: 
        1. Lista de tuplas (vértice_id, pai_id) representando a ordem de visitação.
        2. Lista de arestas de árvore.
        3. Lista de arestas de retorno.
        4. Lista de arestas de avanço.
        5. Lista de arestas de cruzamento.
        6. Ids de PE
        7. Ids de PS
    """
    
    tempo = 0
    tempo_ps = 0
    cor = {}    # Cor do vértice
    pe = {}     # Profundidade de Entrada (PE)
    ps = {}     # Profundidade de Saída (PS)
    parent = {} # rastreador do pai na Árvore DFS
    
    arestas_arvore = []
    arestas_retorno = []
    arestas_avanco = []
    arestas_cruzamento = []
    ordem_visita = [] 

    for v in grafo.vertices:
        cor[v] = 'branco'
        pe[v] = 0
        ps[v] = 0
        parent[v] = None # Inicializa o pai
        
    raiz = grafo.indice_vertices.get(str(id_raiz))
    if not raiz:
        print(f"Erro: Vértice raiz com ID '{id_raiz}' não encontrado.")
        return ([], [], [], [], []) 

    def dfs_visit(u):
        nonlocal tempo, tempo_ps
        nonlocal ordem_visita, arestas_arvore, arestas_retorno, arestas_avanco, arestas_cruzamento
        
        tempo += 1
        pe[u] = tempo
        cor[u] = 'cinza'
        
        ordem_visita.append((u.id, parent[u].id if parent[u] is not None else "-"))

        for v in grafo.lista_adj[u]:
            
            if cor[v] == 'branco':
                # Aresta de árvore
                arestas_arvore.append(Aresta(u, v))
                parent[v] = u # define o pai na aresta de árvore
                dfs_visit(v)
                
            elif cor[v] == 'cinza':
                # aresta de retorno 
                arestas_retorno.append(Aresta(u, v))
                
            elif cor[v] == 'preto':
                if pe[u] < pe[v]:
                    # aresta de avanço
                    arestas_avanco.append(Aresta(u, v))
                else: 
                    # aresta de cruzamento
                    arestas_cruzamento.append(Aresta(u, v))
                
        cor[u] = 'preto'
        tempo_ps += 1
        ps[u] = tempo_ps


    # Iniciar a busca a partir da raiz
    dfs_visit(raiz)
    
    # Se o grafo não for conexo, continuar a busca nos demais vértices
    for u in grafo.vertices:
        if cor[u] == 'branco':
            # Inicia uma nova Árvore DFS
            dfs_visit(u)
            
    pe_ids = {u.id: pe[u] for u in grafo.vertices}
    ps_ids = {u.id: ps[u] for u in grafo.vertices}    
    #print("--- Resultados de PE e PS ---")
    #print(f"PE: {pe_ids}")
    #print(f"PS: {ps_ids}")
    #print("-----------------------------")
            
    return (ordem_visita, arestas_arvore, arestas_retorno, arestas_avanco, arestas_cruzamento, pe_ids, ps_ids)