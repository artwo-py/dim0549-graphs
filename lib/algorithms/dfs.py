"""
Módulo:    DFS
Objetivo:  Implementa o algoritmo de Busca em Profundidade (Depth-First Search)
           de forma modular, com funcionalidades básicas e avançadas.
Funções:   dfs(grafo, id_vertice_inicial, classificar_arestas, retornar_tempos)
"""

def dfs(grafo, id_vertice_inicial=None, classificar_arestas=False, retornar_tempos=False):
    """
    Info: Executa a Busca em Profundidade (DFS). Opera em modo simples (retornando a 
        ordem de visita e arestas de retorno) ou em modo avançado, que pode 
        classificar todos os tipos de arestas e calcular tempos de entrada/saída.
    E: - grafo (Grafo): O objeto grafo a ser percorrido.
       - id_vertice_inicial (str/int, opcional): Vértice de início da busca. Se omitido, usa o primeiro do grafo.
       - classificar_arestas (bool, opcional): Se True, ativa a classificação arestas (árvore, avanço, etc.).
       - retornar_tempos (bool, opcional): Se True, retorna os tempos de entrada (PE) e saída (PS) dos vértices.
    S: - Modo Padrão: (list, list) - Tupla com (ordem_visita, arestas_retorno).
       - Modo Avançado: dict - Dicionário com os resultados solicitados.
    """
    adj = grafo.lista_adj
    todos_vertices = grafo.get_vertices()

    vertice_inicial_obj = None
    if id_vertice_inicial:
        vertice_inicial_obj = grafo.indice_vertices.get(str(id_vertice_inicial))
        if not vertice_inicial_obj:
            raise ValueError(f"Vértice inicial '{id_vertice_inicial}' não está no grafo.")
    elif todos_vertices:
        vertice_inicial_obj = todos_vertices[0]
    else:
        return ([], []) if not classificar_arestas and not retornar_tempos else {}

    ordem_de_busca = ([vertice_inicial_obj] +
                      [v for v in todos_vertices if v != vertice_inicial_obj])

    cor = {v: 'branco' for v in todos_vertices}
    parent = {v: None for v in todos_vertices}
    ordem_visita = []
    
    tempo = 0
    pe = {v: 0 for v in todos_vertices}  
    ps = {v: 0 for v in todos_vertices}  
    arestas_arvore = []
    arestas_retorno = []
    arestas_avanco = []
    arestas_cruzamento = []

    def dfs_visit(u):
        nonlocal tempo
        
        cor[u] = 'cinza'
        tempo += 1
        pe[u] = tempo
        
        pai_id = parent[u].id if parent[u] else "-"
        ordem_visita.append((str(u.id), str(pai_id)))

        for v in adj.get(u, []):
            if cor[v] == 'branco':
                parent[v] = u
                if classificar_arestas:
                    try:
                        from .core.graph import Aresta
                        arestas_arvore.append(Aresta(u, v))
                    except (ImportError, AttributeError):
                        arestas_arvore.append((str(u.id), str(v.id)))

                dfs_visit(v)
            
            elif cor[v] == 'cinza':
                try:
                    from .core.graph import Aresta
                    arestas_retorno.append(Aresta(u, v))
                except (ImportError, AttributeError):
                    arestas_retorno.append((str(u.id), str(v.id)))
            
            elif cor[v] == 'preto' and classificar_arestas:
                if pe[u] < pe[v]:
                    try:
                        from .core.graph import Aresta
                        arestas_avanco.append(Aresta(u, v))
                    except (ImportError, AttributeError):
                        arestas_avanco.append((str(u.id), str(v.id)))
                else:
                    try:
                        from .core.graph import Aresta
                        arestas_cruzamento.append(Aresta(u, v))
                    except (ImportError, AttributeError):
                        arestas_cruzamento.append((str(u.id), str(v.id)))

        cor[u] = 'preto'
        tempo += 1
        ps[u] = tempo

    for v_inicio in ordem_de_busca:
        if cor[v_inicio] == 'branco':
            dfs_visit(v_inicio)

    if classificar_arestas or retornar_tempos:
        resultados = {
            'ordem_visita': [(v_id, p_id) for v_id, p_id in ordem_visita],
            'arestas_retorno': arestas_retorno
        }
        if classificar_arestas:
            resultados['arestas_arvore'] = arestas_arvore
            resultados['arestas_avanco'] = arestas_avanco
            resultados['arestas_cruzamento'] = arestas_cruzamento
        if retornar_tempos:
            resultados['tempos_entrada'] = {v.id: pe[v] for v in pe}
            resultados['tempos_saida'] = {v.id: ps[v] for v in ps}
        return resultados
    
    else:
        return ordem_visita, arestas_retorno