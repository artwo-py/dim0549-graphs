"""
Módulo:    Formatador
Descriçao: Contém funções para gerar representações textuais das estruturas
           de dados e resultados de análise de um objeto Grafo.
"""
import math
from math import inf as infinito
from lib.core.graph import Grafo
from lib.algorithms.is_bipartite import is_bipartite
from lib.algorithms.is_connected import is_connected
from lib.algorithms.lowpt import lowpt 
from lib.core.graph_converter import matriz_adj_para_lista_adj, lista_adj_para_matriz_adj, get_grafo_subjacente
from lib.algorithms.floyd_warshall import floyd_warshall, reconstruir_caminho

def formatar_lista_adj(grafo: Grafo):
    """
    Info: (Função de relatórios) Formata a lista de adjacências do grafo
          em uma representação textual legível.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A representação textual da lista de adjacências.
    """
    titulo = "\n==== (1) REPRESENTAÇÃO POR LISTA DE ADJACÊNCIA ===="
    output = [titulo]
    if not grafo.vertices:
        output.append("Vazia.")
        return "\n".join(output)
    
    sorted_vertices = sorted(grafo.lista_adj.keys(), key=lambda v: str(v.id))
    for vertice in sorted_vertices:
        vizinhos_ids = sorted([str(v.id) for v in grafo.lista_adj.get(vertice, [])])
        output.append(f"{vertice.id}: {vizinhos_ids}")
    return "\n".join(output)

def formatar_matriz_adj(grafo: Grafo):
    """
    Info: (Função de relatórios) Formata a matriz de adjacências do grafo
          em uma representação textual legível.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A representação textual da matriz de adjacências.
    """
    titulo = "\n==== (2) REPRESENTAÇÃO POR MATRIZ DE ADJACÊNCIA ===="
    if grafo.direcionado:
        titulo = "\n==== (16) REPRESENTAÇÃO POR MATRIZ DE ADJACÊNCIA ===="

    output = [titulo]
    ids = [str(v.id) for v in grafo.vertices]
    if not ids:
        output.append("Vazia.")
        return "\n".join(output)
        
    max_width = max(len(id) for id in ids)
    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(ids) * (max_width + 1))}")
    for i, linha in enumerate(grafo.matriz_adj):
        row_str = f"{ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
    return "\n".join(output)

def formatar_matriz_incidencia(grafo: Grafo):
    """
    Info: (Função de relatórios) Formata a matriz de incidência do grafo
          em uma representação textual legível.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A representação textual da matriz de incidência.
    """
    titulo = "\n==== (3) REPRESENTAÇÃO POR MATRIZ DE INCIDÊNCIA ===="
    if grafo.direcionado:
        titulo = "\n==== (17) REPRESENTAÇÃO POR MATRIZ DE INCIDÊNCIA ===="
    
    output = [titulo]
    if not grafo.vertices or not grafo.arestas:
        output.append("Vazia.")
        return "\n".join(output)

    v_ids = [str(v.id) for v in grafo.vertices]
    e_ids = [f"e{i+1}" for i in range(grafo.num_arestas())]
    
    max_width = 0
    if v_ids: max_width = max(max_width, max(len(id) for id in v_ids))
    if e_ids: max_width = max(max_width, max(len(id) for id in e_ids))

    header = f"{' ' * max_width} |" + "".join(f" {id:>{max_width}}" for id in e_ids)
    output.append(header)
    output.append(f"{'-' * (max_width + 1)}+{'-' * (len(e_ids) * (max_width + 1))}")

    for i, linha in enumerate(grafo.matriz_incidencia):
        row_str = f"{v_ids[i]:>{max_width}} |" + "".join(f" {val:>{max_width}}" for val in linha)
        output.append(row_str)
        
    return "\n".join(output)

def formatar_conversoes(grafo: Grafo):
    """
    Info: (Função de relatórios) Demonstra a conversão entre as representações
          de lista e matriz de adjacências. As representações originais
          do grafo são restauradas após o teste.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado textual da conversão.
    """
    output = ["\n==== (4) CONVERSÃO ENTRE REPRESENTAÇÕES ===="]
    lista_adj_original = {k: list(v) for k, v in grafo.lista_adj.items()}
    matriz_adj_original = [row[:] for row in grafo.matriz_adj]
    output.append("\n--- Matriz -> Lista ---")
    matriz_adj_para_lista_adj(grafo)
    # Pega apenas o corpo (sem o cabeçalho) da representação
    output.append(formatar_lista_adj(grafo).split('\n', 2)[-1])
    grafo.lista_adj = lista_adj_original
    output.append("\n--- Lista -> Matriz ---")
    lista_adj_para_matriz_adj(grafo)
    # Pega apenas o corpo (sem o cabeçalho) da representação
    output.append(formatar_matriz_adj(grafo).split('\n', 2)[-1])
    grafo.lista_adj = lista_adj_original
    grafo.matriz_adj = matriz_adj_original
    return "\n".join(output)

def formatar_graus(grafo: Grafo):
    """
    Info: (Função de relatórios) Lista o grau de cada vértice. Para dígrafos,
          as funções de grau podem retornar tuplas (grau_entrada, grau_saída).
          Esta função ignora tuplas, focando no grau total para grafos não-direcionados.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A lista de graus formatada.
    """
    output = ["\n==== (5) GRAU DE CADA VÉRTICE ===="]
    if not grafo.vertices:
        output.append("Vazio.")
        return "\n".join(output)
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    degree_strings = []
    for v in sorted_vertices:
        grau = grafo.get_grau(v.id)
        if grau is not None and not isinstance(grau, tuple):
            degree_strings.append(f"d({v.id}) = {grau}")
    
    # Formatação em colunas para melhor legibilidade
    num_cols = 3
    max_len = max(len(s) for s in degree_strings) if degree_strings else 0
    padded_strings = [s.ljust(max_len) for s in degree_strings]
    num_rows = math.ceil(len(padded_strings) / num_cols)
    for i in range(num_rows):
        row_parts = [padded_strings[i + j * num_rows] for j in range(num_cols) if i + j * num_rows < len(padded_strings)]
        output.append("   ".join(row_parts))
    return "\n".join(output)

def formatar_adjacencias_por_vertice(grafo: Grafo):
    """
    Info: (Função de relatórios) Lista os vizinhos adjacentes para cada vértice.
    E: grafo (Grafo) - A instância do grafo.
    S: str - A lista de adjacências formatada.
    """
    output = ["\n==== (6) ADJACÊNCIAS DE CADA VÉRTICE ===="]
    if not grafo.vertices:
        output.append("Vazio.")
        return "\n".join(output)
    sorted_vertices = sorted(grafo.vertices, key=lambda v: str(v.id))
    for v in sorted_vertices:
        adjacentes_ids = sorted([str(adj.id) for adj in grafo.lista_adj.get(v, [])])
        output.append(f"Adjacentes de {v.id}: {adjacentes_ids}")
    return "\n".join(output)

def formatar_info_gerais(grafo: Grafo):
    """
    Info: (Função de relatórios) Informa o número total de vértices e arestas.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resumo das informações gerais.
    """
    output = [
        f"\n==== (7) NÚMERO TOTAL DE VÉRTICES ====\n{grafo.num_vertices()}",
        f"\n==== (8) NÚMERO TOTAL DE ARESTAS ====\n{grafo.num_arestas()}"
    ]
    return "\n".join(output)

def formatar_eh_conexo(grafo: Grafo):
    """
    Info: (Função de relatórios) Verifica e reporta se o grafo é conexo.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado da conectividade.
    """
    output = ["\n==== (11) CONECTIVIDADE ===="]
    resultado = "Sim" if is_connected(grafo) else "Não"
    output.append(f"O grafo é conexo? {resultado}")
    return "\n".join(output)

def formatar_bipartido(grafo: Grafo):
    """
    Info: (Função de relatórios) Verifica e reporta se o grafo é bipartido.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado da bipartição.
    """
    output = ["\n==== (12) BIPARTIÇÃO (OPC) ===="]
    resultado = "Sim" if is_bipartite(grafo) else "Não"
    output.append(f"O grafo é bipartido? {resultado}")
    return "\n".join(output)

def formatar_biconectividade(grafo: Grafo):
    """
    Info: (Função de relatórios) Encontra e reporta os pontos de articulação
          e as pontes do grafo usando o algoritmo lowpt.
    E: grafo (Grafo) - A instância do grafo.
    S: str - O resultado da análise de biconectividade.
    """
    output = ["\n==== (15) BICONECTIVIDADE (ARTICULAÇÕES E PONTES) ===="]
    if grafo.num_vertices() == 0:
        output.append("Grafo vazio.")
        return "\n".join(output)
    articulacoes, pontes = lowpt(grafo)
    if not articulacoes:
        output.append("Pontos de Articulação: Nenhum.")
    else:
        # Ordena a lista de IDs para exibição consistente
        output.append(f"Pontos de Articulação: {sorted(list(articulacoes), key=str)}")
    if not pontes:
        output.append("Pontes: Nenhuma.")
    else:
        # Pontes são tuplas (v1_id, v2_id), ordenadas para exibição consistente
        output.append(f"Pontes: {sorted(list(pontes))}")
    return "\n".join(output)
    
def formatar_grafo_subjacente(grafo: Grafo):
    """
    Info: (Função de relatórios) Gera a representação textual do grafo
          subjacente (não-direcionado) de um dígrafo.
    E: grafo (Grafo) - A instância do dígrafo.
    S: str - A representação textual do grafo subjacente.
    """
    output = ["\n==== (18) GRAFO SUBJACENTE (OPC) ===="]
    subjacente = get_grafo_subjacente(grafo)
    # Chama formatar_lista_adj no grafo subjacente e remove o título (1)
    texto_lista = formatar_lista_adj(subjacente).split('\n', 2)[-1]
    output.append(texto_lista)
    return "\n".join(output)

def gerar_relatorio_completo(grafo: Grafo):
    """
    Info: (Função de relatórios) Agrega todos os resultados de análise em
          um relatório textual completo, formatando-o de forma diferente
          dependendo se o objeto é um Grafo (não-direcionado) ou Dígrafo.
    E: grafo (Grafo) - A instância do grafo a ser analisada.
    S: str - O relatório completo.
    """
    header = [
        "*********************************************************************",
        f"Arquivo: {grafo.nome_arquivo}",
    ]
    if not grafo.direcionado:
        report_body = [
            "Análise para: GRAFO NÃO-DIRECIONADO",
            formatar_lista_adj(grafo),                 # (1)
            formatar_matriz_adj(grafo),                # (2)
            formatar_matriz_incidencia(grafo),         # (3)
            formatar_conversoes(grafo),                # (4)
            formatar_graus(grafo),                     # (5)
            formatar_adjacencias_por_vertice(grafo),   # (6)
            formatar_info_gerais(grafo),               # (7) e (8)
            "\n==== (9) e (10) INCLUSÃO E EXCLUSÃO DE VÉRTICES ====\nINFO: Funções implementadas na classe Grafo para manipulação dos dados.",
            formatar_eh_conexo(grafo),                 # (11)
            formatar_bipartido(grafo),                 # (12)
            "\n==== (13) e (14) BUSCAS BFS E DFS ====\nINFO: As buscas são executadas e seus resultados renderizados visualmente.",
            formatar_biconectividade(grafo),           # (15)
        ]
    else:
        report_body = [
            "Análise para: DÍGRAFO",
            formatar_matriz_adj(grafo),                # (16)
            formatar_matriz_incidencia(grafo),         # (17)
            formatar_grafo_subjacente(grafo),          # (18)
            "\n==== (19) e (20) BUSCAS BFS E DFS ====\nINFO: As buscas são executadas e seus resultados (com classificação completa de arestas para DFS) são renderizados visualmente.",
        ]
    return "\n".join(header + report_body)

def formatar_caminho_floyd_warshall(grafo: Grafo, id_inicio: str, id_fim: str):
    """
    Info: (Função de relatórios) Executa o Floyd-Warshall, reconstrói o caminho
          mais curto entre dois vértices e formata o resultado textual.
          
    E: grafo (Grafo) - A instância do grafo.
    E: id_inicio (str) - ID do vértice inicial.
    E: id_fim (str) - ID do vértice final.
    
    S: tupla (str, list[Vertice] or None) 
         - str: O relatório textual formatado (para impressão).
         - list or None: Os dados do caminho (para o renderer), ou None se não houver.
    """
    
    # --- ALTERAÇÃO AQUI ---
    # Título segue o padrão do relatório
    titulo = f"\n==== (21) CAMINHO MAIS CURTO (FLOYD-WARSHALL {id_inicio} -> {id_fim}) ===="
    
    if not grafo.ponderado:
        report = "  Algoritmo não aplicável (grafo não ponderado)."
        return (titulo + "\n" + report, None)
    
    try:
        # (O resto da função permanece idêntico)
        dist, pred, vertices = floyd_warshall(grafo)
        
        idx_map = {v.id: i for i, v in enumerate(vertices)}
        idx_inicio = idx_map.get(id_inicio)
        idx_fim = idx_map.get(id_fim)

        if idx_inicio is None or idx_fim is None:
            report = f"  Erro: Vértice {id_inicio} ou {id_fim} não encontrado."
            return (titulo + "\n" + report, None)

        custo = dist[idx_inicio][idx_fim]
        caminho = reconstruir_caminho(pred, vertices, idx_inicio, idx_fim)

        if caminho:
            custo_str = f"{custo:.0f}" if custo != infinito else "INF"
            caminho_str = " -> ".join([v.id for v in caminho])
            report = f"  Custo: {custo_str}\n  Caminho: {caminho_str}"
            return (titulo + "\n" + report, caminho)
        else:
            report = "  Não há caminho entre os vértices."
            return (titulo + "\n" + report, None)
            
    except Exception as e:
        report = f"  Ocorreu um erro inesperado: {e}"
        return (titulo + "\n" + report, None)