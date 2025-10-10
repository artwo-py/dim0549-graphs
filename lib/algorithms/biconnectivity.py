# biconnectivity.py
from ..core.graph import Grafo, Aresta

def biconnectivity(grafo, start_node=None):
    """
    (15) Determinação de articulações e blocos (biconectividade)

    Args:
        grafo (Grafo): O objeto Grafo a ser analisado.
        start_node (str, optional): ID do vértice de início para o DFS.
                                    Se None, usa o primeiro vértice da lista.

    Returns:
        articulacoes: set de ids dos vertices articulações encontrados
        blocos: lista de listas de Aresta, cada lista representando um bloco biconexo.
    """
    if grafo.direcionado:
        return set(), []
    
    if not grafo.vertices:
        return set(), []

    time = 0
    disc = {}  # tempo de descoberta 
    low = {}   # menor tempo de Descobert
    parent = {}  # Pai na árvore DFS
    articulacoes = set()
    blocos = []
    stack = []  # pilha para rastrear as arestas do caminho atual do DFS
    
    for v in grafo.vertices:
        disc[v] = -1
        low[v] = -1
        parent[v] = None

    def _dfs_biconectividade(u):
        nonlocal time
        children = 0
        disc[u] = low[u] = time
        time += 1

        for v in grafo.lista_adj[u]:
            if v == parent[u]:
                continue

            if disc[v] == -1:  # vértice v não visitado
                parent[v] = u
                children += 1
                
                stack.append((u, v)) # Adiciona a aresta à pilha

                _dfs_biconectividade(v)

                low[u] = min(low[u], low[v]) # Atualiza o low de u

                # Condição de pont de articulação (v é um bloco em si)
                if parent[u] is None and children > 1: # caso da Raiz da Árvore DFS
                    articulacoes.add(u.id)
                    _extrair_bloco(u, v)
                if parent[u] is not None and low[v] >= disc[u]: # caso de Vértice Interno, Nnão raiz
                    articulacoes.add(u.id)
                    _extrair_bloco(u, v)

            elif disc[v] < disc[u]: # aresta retorno
                low[u] = min(low[u], disc[v]) # 'e aresta de retorno, atualiza low de u
                print
                
                stack.append((u, v)) # adiciona a aresta a pilha (para o caso de ser uma aresta inicial de um bloco
                
    def _extrair_bloco(u, v):
        """Extrai as arestas da pilha até a aresta (u, v) ou (v, u) e forma um bloco."""
        bloco_atual = []
        if not stack:
            return

        aresta_do_bloco = stack.pop()
        while True:
            # grante que a aresta (u,v) ou (v,u) seja a última a ser retirada
            if not ((aresta_do_bloco[0] == u and aresta_do_bloco[1] == v) or 
                    (aresta_do_bloco[0] == v and aresta_do_bloco[1] == u)):
                bloco_atual.append(Aresta(aresta_do_bloco[0].id, aresta_do_bloco[1].id))
            else:
                bloco_atual.append(Aresta(aresta_do_bloco[0].id, aresta_do_bloco[1].id))
                break # a aresta de corte foi encontrada

            if not stack: break
            aresta_do_bloco = stack.pop()

        if bloco_atual:
            blocos.append(bloco_atual)


    # seleciona o vértice de início, se não for fornecido
    start_v = None
    if start_node is not None and str(start_node) in grafo.indice_vertices:
        start_v = grafo.indice_vertices[str(start_node)]
    elif grafo.vertices:
        start_v = grafo.vertices[0]
    
    # Realiza o dfs
    if start_v:
        _dfs_biconectividade(start_v)

    # ldar com grafos desconexos (partes não visitadas
    for v_comp in grafo.vertices:
        if disc[v_comp] == -1:
            _dfs_biconectividade(v_comp)

    # se ainda houver arestas na pilha, elas formam o último bloco , ou o único
    if stack:
        bloco_final = [Aresta(e[0].id, e[1].id) for e in stack]
        blocos.append(bloco_final)
        stack.clear()

    return articulacoes, [[str(a) for a in bloco] for bloco in blocos]



def Biconectividade(grafo, vertice_inicial):    
    # Testando implementação com função LOWPT (dada pelo professor)
    # Em construção

    # Mapas
    visitado = {} # Marca se o vértice foi visitado
    profundidade = {} # Profundidade do vértice na árvore dfs
    alcanceVertice = {} # Valor 'lowpt'
    
    # Listas/Pilhas/Conjuntos
    arestasRetorno = [] # Armazena as arestas de retorno
    P = [] # Pilha para armazenar arestas
    articulacoes = set() # Armazena os vértices de articulação
    arestasDFS = [] # Arestas da árvore DFS (ordem de visitação)
    blocos = [] # Armazena os blocos biconexos

    for v in grafo.vertices:
        visitado[v] = False
        profundidade[v] = None
        alcanceVertice[v] = None

    raiz = grafo.indice_vertices.get(str(vertice_inicial))
    if not raiz:
        print(f"Erro: Vértice raiz com ID '{vertice_inicial}' não encontrado.")
    
    def BP_Visita(raiz):
        """
        Função auxiliar recursiva que executa a DFS.
        Identifica articulações e blocos.
        """
        visitado[u] = True
        P.append(u)
        profundidade[u] = P.index(u)

        for v in grafo.lista_adj[u]:

            ordem_visita.append((u.id, parent[u].id if parent[u] is not None else "-"))

            if visitado[v] == False:
                parent[v] = u # Define o pai na aresta de árvore
                BP_Visita(v)
            else:
                if (v != P[-2]):
                    arestas_retorno.append(str(v),str(u))

            lowpt_valor = lowpt(P.pop(v), profundidade, arestasRetorno)

            if lowpt_valor == v or lowpt_valor == u:
                if (profundidade[u] == 0 and len(grafo.lista_adj[u]) > 1) or profundidade[u] != 0:
                    articulacoes.append(u)

    def lowpt(v, profundidade, arestasRetorno):
        print("calculando lowpt de " + str(v))