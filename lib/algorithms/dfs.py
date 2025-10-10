"""
Módulo:    DFS
Objetivo:  Implementa o algoritmo de Busca em Profundidade (Depth-First Search)
           de forma modular, com funcionalidades básicas e avançadas.
Funções:   dfs(grafo, id_vertice_inicial, classificar_arestas, retornar_tempos)
"""
from lib.core.graph import Grafo, Aresta

def dfs(grafo: Grafo, id_vertice_inicial=None, classificar_arestas=False, retornar_tempos=False):
    """
    Info: Executa a Busca em Profundidade (DFS). Opera em modo simples (retornando a 
        ordem de visita e arestas de retorno) ou em modo avançado, que pode 
        classificar todos os tipos de arestas e calcular tempos de entrada/saída.
        
    Args:
       - grafo (Grafo): O objeto grafo a ser percorrido.
       - id_vertice_inicial (str/int, opcional): Vértice de início da busca. Se omitido, usa o primeiro do grafo.
       - classificar_arestas (bool, opcional): Se True, ativa a classificação arestas (árvore, avanço, etc.).
       - retornar_tempos (bool, opcional): Se True, retorna os tempos de entrada (PE) e saída (PS) dos vértices.

    Returns:
       - Modo Padrão: (list, list) - Tupla com (ordem_visita, arestas_retorno).
       - Modo Avançado: dict - Dicionário com os resultados solicitados.
    """
    adj = grafo.lista_adj
    todos_vertices = grafo.vertices

    vertice_inicial_obj = None
    if id_vertice_inicial:
        vertice_inicial_obj = grafo.indice_vertices.get(str(id_vertice_inicial))
        if not vertice_inicial_obj:
            print(f"Alerta: Vértice inicial '{id_vertice_inicial}' não encontrado no grafo '{grafo.nome_arquivo}'.")
            return ([], []) if not classificar_arestas and not retornar_tempos else {}
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
        
        pai_obj = parent.get(u)
        pai_id = str(pai_obj.id) if pai_obj else "-"
        ordem_visita.append((str(u.id), pai_id))

        for v in sorted(adj.get(u, []), key=lambda vertice: str(vertice.id)):
            if cor[v] == 'branco':
                parent[v] = u
                if classificar_arestas:
                    arestas_arvore.append(Aresta(u, v))
                dfs_visit(v)
            
            elif cor[v] == 'cinza':
                arestas_retorno.append(Aresta(u, v))
            
            elif cor[v] == 'preto' and classificar_arestas:
                if pe[u] < pe[v]:
                    arestas_avanco.append(Aresta(u, v))
                else:
                    arestas_cruzamento.append(Aresta(u, v))

        cor[u] = 'preto'
        tempo += 1
        ps[u] = tempo

    for v_inicio in ordem_de_busca:
        if cor[v_inicio] == 'branco':
            dfs_visit(v_inicio)

    if classificar_arestas or retornar_tempos:
        resultados = {
            'ordem_visita': ordem_visita,
            'arestas_retorno': arestas_retorno
        }
        if classificar_arestas:
            resultados['arestas_arvore'] = arestas_arvore
            resultados['arestas_avanco'] = arestas_avanco
            resultados['arestas_cruzamento'] = arestas_cruzamento
        if retornar_tempos:
            resultados['tempos_entrada'] = {str(v.id): pe[v] for v in pe}
            resultados['tempos_saida'] = {str(v.id): ps[v] for v in ps}
        return resultados
    
    else:
        arestas_retorno_tuplas = [(str(a.v1.id), str(a.v2.id)) for a in arestas_retorno]
        return ordem_visita, arestas_retorno_tuplas
